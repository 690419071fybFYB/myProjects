#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


ALLOWED_ERRNOS_DEFAULT = {0, 100, 400, 401, 403, 404, 405, 412, 500, 1000}
SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


@dataclass
class CheckResult:
    id: str
    name: str
    layer: str
    status: str  # passed | failed | skipped
    severity: str  # P0-P3
    message: str
    elapsed_seconds: float = 0.0
    evidence: str = ""
    command: str = ""


@dataclass
class CommandResult:
    status: str
    exit_code: int
    elapsed_seconds: float
    stdout: str
    stderr: str


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _parse_env_line(line: str) -> Optional[Tuple[str, str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    if not key:
        return None
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return key, value


def load_dotenv_files(paths: Sequence[Path], override: bool = False) -> Dict[str, str]:
    loaded: Dict[str, str] = {}
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for line in content.splitlines():
            parsed = _parse_env_line(line)
            if not parsed:
                continue
            key, value = parsed
            if not override and key in os.environ:
                continue
            os.environ[key] = value
            loaded[key] = value
    return loaded


def run_command(
    cmd: str,
    cwd: Path,
    timeout_seconds: int = 1800,
    extra_env: Optional[Dict[str, str]] = None,
) -> CommandResult:
    env = os.environ.copy()
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})

    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
        )
        elapsed = time.time() - started
        return CommandResult(
            status="passed" if proc.returncode == 0 else "failed",
            exit_code=proc.returncode,
            elapsed_seconds=elapsed,
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
        )
    except subprocess.TimeoutExpired as err:
        elapsed = time.time() - started
        return CommandResult(
            status="failed",
            exit_code=124,
            elapsed_seconds=elapsed,
            stdout=(err.stdout or "") if isinstance(err.stdout, str) else "",
            stderr=(err.stderr or "") if isinstance(err.stderr, str) else f"timeout after {timeout_seconds}s",
        )


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sort_results(results: Sequence[CheckResult]) -> List[CheckResult]:
    return sorted(
        list(results),
        key=lambda r: (
            SEVERITY_ORDER.get(r.severity, 9),
            0 if r.status == "failed" else 1,
            r.layer,
            r.id,
        ),
    )


def summarize_results(results: Sequence[CheckResult]) -> Dict[str, Any]:
    total = len(results)
    passed = len([r for r in results if r.status == "passed"])
    failed = len([r for r in results if r.status == "failed"])
    skipped = len([r for r in results if r.status == "skipped"])
    severity_failed = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    for item in results:
        if item.status == "failed":
            severity_failed[item.severity] = severity_failed.get(item.severity, 0) + 1
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "failed_by_severity": severity_failed,
    }


def merge_layer_results(layers: Dict[str, List[CheckResult]]) -> List[CheckResult]:
    merged: List[CheckResult] = []
    for _layer_name, items in layers.items():
        merged.extend(items)
    return merged


def to_markdown(
    run_name: str,
    mode: str,
    started_at: str,
    finished_at: str,
    layers: Dict[str, List[CheckResult]],
) -> str:
    all_results = sort_results(merge_layer_results(layers))
    summary = summarize_results(all_results)

    lines: List[str] = []
    lines.append(f"# {run_name}")
    lines.append("")
    lines.append(f"- mode: `{mode}`")
    lines.append(f"- started_at: `{started_at}`")
    lines.append(f"- finished_at: `{finished_at}`")
    lines.append(
        f"- summary: `passed={summary['passed']}`, `failed={summary['failed']}`, `skipped={summary['skipped']}`, `total={summary['total']}`"
    )
    lines.append("")

    lines.append("## Layer Summary")
    lines.append("")
    lines.append("| layer | passed | failed | skipped | total |")
    lines.append("|---|---:|---:|---:|---:|")
    for layer_name, items in layers.items():
        stat = summarize_results(items)
        lines.append(
            f"| {layer_name} | {stat['passed']} | {stat['failed']} | {stat['skipped']} | {stat['total']} |"
        )

    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| id | layer | status | severity | message |")
    lines.append("|---|---|---|---|---|")
    for item in all_results:
        msg = (item.message or "").replace("|", "/").replace("\n", " ").strip()
        if len(msg) > 180:
            msg = msg[:177] + "..."
        lines.append(f"| {item.id} | {item.layer} | {item.status} | {item.severity} | {msg} |")

    failed_items = [r for r in all_results if r.status == "failed"]
    if failed_items:
        lines.append("")
        lines.append("## Failures (With Repro)")
        lines.append("")
        for item in failed_items:
            lines.append(f"- `{item.id}` [{item.severity}] {item.name}: {item.message}")
            if item.command:
                lines.append(f"  - repro_step: run `{item.command}`")
            if item.evidence:
                lines.append(f"  - evidence: `{item.evidence}`")

    return "\n".join(lines).strip() + "\n"


def persist_run_report(
    output_dir: Path,
    run_name: str,
    mode: str,
    started_at: str,
    finished_at: str,
    layers: Dict[str, List[CheckResult]],
) -> Tuple[Path, Path, Dict[str, Any]]:
    ensure_dir(output_dir)
    all_results = sort_results(merge_layer_results(layers))
    payload = {
        "run_name": run_name,
        "mode": mode,
        "started_at": started_at,
        "finished_at": finished_at,
        "summary": summarize_results(all_results),
        "layers": {
            k: [asdict(item) for item in sort_results(v)]
            for k, v in layers.items()
        },
    }
    json_path = output_dir / f"{mode}-report.json"
    md_path = output_dir / f"{mode}-report.md"
    write_json(json_path, payload)
    write_text(md_path, to_markdown(run_name, mode, started_at, finished_at, layers))
    return json_path, md_path, payload


def load_scenario_matrix(path: Path) -> List[Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def attach_missing_scenarios(
    existing: Sequence[CheckResult],
    matrix: Sequence[Dict[str, Any]],
    mode: str,
) -> List[CheckResult]:
    existing_ids = {item.id for item in existing}
    synthetic: List[CheckResult] = []
    for item in matrix:
        sid = str(item.get("id") or "").strip()
        if not sid or sid in existing_ids:
            continue
        profiles = item.get("profiles") or ["pr", "nightly", "pre-release"]
        if mode not in profiles:
            continue
        synthetic.append(
            CheckResult(
                id=sid,
                name=str(item.get("name") or sid),
                layer=str(item.get("layer") or "L2"),
                status="skipped",
                severity=str(item.get("severity") or "P2"),
                message="Scenario is defined in matrix but not yet automated in this mode",
            )
        )
    return synthetic


def format_cmd(cmd: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(x)) for x in cmd)
