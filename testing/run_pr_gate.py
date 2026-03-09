#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "testing" / "lib" / "common.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from testing.lib.common import (
    CheckResult,
    attach_missing_scenarios,
    ensure_dir,
    format_cmd,
    load_dotenv_files,
    load_scenario_matrix,
    merge_layer_results,
    now_iso,
    persist_run_report,
    run_command,
)


def env_or(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    return value


def to_check_result(item: Dict, default_layer: str) -> CheckResult:
    return CheckResult(
        id=str(item.get("id") or "UNKNOWN"),
        name=str(item.get("name") or item.get("id") or "unknown check"),
        layer=str(item.get("layer") or default_layer),
        status=str(item.get("status") or "failed"),
        severity=str(item.get("severity") or "P2"),
        message=str(item.get("message") or ""),
        elapsed_seconds=float(item.get("elapsed_seconds") or 0.0),
        evidence=str(item.get("evidence") or ""),
        command=str(item.get("command") or ""),
    )


def load_results_file(path: Path, default_layer: str) -> List[CheckResult]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    raw = payload.get("results")
    if not isinstance(raw, list):
        return []
    return [to_check_result(item, default_layer) for item in raw if isinstance(item, dict)]


def run_json_suite(
    cmd: str,
    cwd: Path,
    output_file: Path,
    default_layer: str,
    fallback_id: str,
    fallback_name: str,
    fallback_severity: str,
    extra_env: Dict[str, str],
    timeout_seconds: int = 1800,
) -> List[CheckResult]:
    result = run_command(cmd, cwd, timeout_seconds=timeout_seconds, extra_env=extra_env)
    parsed = load_results_file(output_file, default_layer)
    if parsed:
        return parsed

    status = "passed" if result.status == "passed" else "failed"
    message = (result.stderr or result.stdout or "suite finished").strip()
    if len(message) > 250:
        message = message[:247] + "..."
    evidence = ""
    if status == "failed":
        evidence = (result.stderr or result.stdout or "")[:500]
    return [
        CheckResult(
            id=fallback_id,
            name=fallback_name,
            layer=default_layer,
            status=status,
            severity=fallback_severity,
            message=message or "suite finished",
            elapsed_seconds=result.elapsed_seconds,
            evidence=evidence,
            command=cmd,
        )
    ]


def run_cos_real_smoke(
    workspace: Path,
    base_url: str,
    admin_username: str,
    admin_password: str,
    extra_env: Dict[str, str],
) -> CheckResult:
    required = ("COS_SECRET_ID", "COS_SECRET_KEY", "COS_BUCKET", "COS_REGION")
    missing = [name for name in required if not env_or(name)]
    if missing:
        return CheckResult(
            id="NIGHTLY-COS-REAL-SMOKE",
            name="COS real upload smoke and URL availability",
            layer="L4",
            status="skipped",
            severity="P1",
            message=f"missing env: {', '.join(missing)}",
        )

    cmd = "node scripts/test-cos-smoke.js"
    env = dict(extra_env)
    env.update(
        {
            "HIOSHOP_ADMIN_API": f"{base_url.rstrip('/')}/admin",
            "HIOSHOP_ADMIN_USER": admin_username,
            "HIOSHOP_ADMIN_PASS": admin_password,
        }
    )
    result = run_command(
        cmd,
        workspace / "hioshop-server",
        timeout_seconds=1200,
        extra_env=env,
    )
    status = "passed" if result.status == "passed" else "failed"
    message = (result.stderr or result.stdout or "cos smoke finished").strip().splitlines()
    tail = message[-1] if message else "cos smoke finished"
    if len(tail) > 220:
        tail = tail[:217] + "..."
    return CheckResult(
        id="NIGHTLY-COS-REAL-SMOKE",
        name="COS real upload smoke and URL availability",
        layer="L4",
        status=status,
        severity="P1",
        message=tail,
        elapsed_seconds=result.elapsed_seconds,
        evidence=((result.stderr or result.stdout or "")[:500] if status == "failed" else ""),
        command=cmd,
    )


def main() -> int:
    workspace_default = Path(".").resolve()
    load_dotenv_files(
        [
            workspace_default / ".env",
            workspace_default / "deploy/.env",
        ],
        override=False,
    )
    parser = argparse.ArgumentParser(description="Run Hioshop PR gate (core chain)")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--base-url", default=env_or("BASE_URL", "http://127.0.0.1:8360"))
    parser.add_argument("--api-jwt-secret", default=env_or("API_JWT_SECRET", env_or("API_TOKEN_SECRET", "")))
    parser.add_argument("--admin-jwt-secret", default=env_or("ADMIN_JWT_SECRET", env_or("ADMIN_TOKEN_SECRET", "")))
    parser.add_argument("--api-user-id", type=int, default=int(env_or("TEST_API_USER_ID", "1048")))
    parser.add_argument("--admin-user-id", type=int, default=int(env_or("TEST_ADMIN_USER_ID", "14")))
    parser.add_argument("--admin-username", default=env_or("TEST_ADMIN_USERNAME", "qilelab.com"))
    parser.add_argument("--admin-password", default=env_or("TEST_ADMIN_PASSWORD", "qilelab.com"))
    parser.add_argument("--db-host", default=env_or("TEST_DB_HOST", env_or("MYSQL_HOST", "127.0.0.1")))
    parser.add_argument("--db-port", type=int, default=int(env_or("TEST_DB_PORT", env_or("MYSQL_PORT", "3306"))))
    parser.add_argument("--db-user", default=env_or("TEST_DB_USER", env_or("MYSQL_USER", "root")))
    parser.add_argument(
        "--db-password",
        default=env_or("TEST_DB_PASSWORD", env_or("MYSQL_PASSWORD", env_or("MYSQL_ROOT_PASSWORD", ""))),
    )
    parser.add_argument("--db-name", default=env_or("TEST_DB_NAME", env_or("MYSQL_DATABASE", "hiolabsDB")))
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    started_at = now_iso()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = workspace / "testing-artifacts" / f"{timestamp}-pr-gate"
    layer_dir = output_dir / "layers"
    ensure_dir(layer_dir)

    shared_env = {
        "BASE_URL": args.base_url,
        "API_JWT_SECRET": args.api_jwt_secret,
        "ADMIN_JWT_SECRET": args.admin_jwt_secret,
        "API_TOKEN_SECRET": args.api_jwt_secret,
        "ADMIN_TOKEN_SECRET": args.admin_jwt_secret,
        "TEST_DB_HOST": args.db_host,
        "TEST_DB_PORT": str(args.db_port),
        "TEST_DB_USER": args.db_user,
        "TEST_DB_PASSWORD": args.db_password,
        "TEST_DB_NAME": args.db_name,
        "MYSQL_HOST": args.db_host,
        "MYSQL_PORT": str(args.db_port),
        "MYSQL_USER": args.db_user,
        "MYSQL_PASSWORD": args.db_password,
        "MYSQL_DATABASE": args.db_name,
        "TEST_API_USER_ID": str(args.api_user_id),
        "TEST_ADMIN_USER_ID": str(args.admin_user_id),
        "TEST_ADMIN_USERNAME": args.admin_username,
        "TEST_ADMIN_PASSWORD": args.admin_password,
        "COUPON_TEST_BASE_URL": args.base_url,
        "COUPON_TEST_ADMIN_USER_ID": str(args.admin_user_id),
        "COUPON_TEST_USER_ID": str(args.api_user_id),
        "COUPON_TEST_DB_HOST": args.db_host,
        "COUPON_TEST_DB_PORT": str(args.db_port),
        "COUPON_TEST_DB_USER": args.db_user,
        "COUPON_TEST_DB_PASSWORD": args.db_password,
        "COUPON_TEST_DB_NAME": args.db_name,
        "HIOSHOP_ADMIN_API": f"{args.base_url.rstrip('/')}/admin",
        "HIOSHOP_ADMIN_USER": args.admin_username,
        "HIOSHOP_ADMIN_PASS": args.admin_password,
    }

    l1_output = layer_dir / "l1-contract-core.json"
    l1_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/contract_suite.py",
            "--workspace",
            str(workspace),
            "--scope",
            "core",
            "--base-url",
            args.base_url,
            "--api-jwt-secret",
            args.api_jwt_secret,
            "--admin-jwt-secret",
            args.admin_jwt_secret,
            "--api-user-id",
            str(args.api_user_id),
            "--admin-user-id",
            str(args.admin_user_id),
            "--output",
            str(l1_output),
        ]
    )
    l1_results = run_json_suite(
        l1_cmd,
        workspace,
        l1_output,
        "L1",
        "L1-CORE-SUITE",
        "L1 core contract suite",
        "P1",
        shared_env,
        timeout_seconds=1800,
    )

    l2_output = layer_dir / "l2-business-core.json"
    l2_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/business_suite.py",
            "--scope",
            "core",
            "--workspace",
            str(workspace),
            "--base-url",
            args.base_url,
            "--api-jwt-secret",
            args.api_jwt_secret,
            "--admin-jwt-secret",
            args.admin_jwt_secret,
            "--api-user-id",
            str(args.api_user_id),
            "--admin-user-id",
            str(args.admin_user_id),
            "--admin-username",
            args.admin_username,
            "--admin-password",
            args.admin_password,
            "--db-host",
            args.db_host,
            "--db-port",
            str(args.db_port),
            "--db-user",
            args.db_user,
            "--db-password",
            args.db_password,
            "--db-name",
            args.db_name,
            "--pay-workers",
            "1",
            "--output",
            str(l2_output),
        ]
    )
    l2_results = run_json_suite(
        l2_cmd,
        workspace,
        l2_output,
        "L2",
        "L2-CORE-SUITE",
        "L2 core business suite",
        "P0",
        shared_env,
        timeout_seconds=3600,
    )

    l3_output = layer_dir / "l3-cross-end.json"
    l3_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/cross_end_suite.py",
            "--base-url",
            args.base_url,
            "--api-jwt-secret",
            args.api_jwt_secret,
            "--admin-jwt-secret",
            args.admin_jwt_secret,
            "--api-user-id",
            str(args.api_user_id),
            "--admin-user-id",
            str(args.admin_user_id),
            "--admin-username",
            args.admin_username,
            "--admin-password",
            args.admin_password,
            "--db-host",
            args.db_host,
            "--db-port",
            str(args.db_port),
            "--db-user",
            args.db_user,
            "--db-password",
            args.db_password,
            "--db-name",
            args.db_name,
            "--output",
            str(l3_output),
        ]
    )
    l3_results = run_json_suite(
        l3_cmd,
        workspace,
        l3_output,
        "L3",
        "L3-CROSS-END-SUITE",
        "L3 cross-end suite",
        "P1",
        shared_env,
        timeout_seconds=2400,
    )

    l4_output = layer_dir / "l4-frontend-smoke.json"
    l4_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/frontend_smoke_suite.py",
            "--workspace",
            str(workspace),
            "--base-url",
            args.base_url,
            "--admin-username",
            args.admin_username,
            "--admin-password",
            args.admin_password,
            "--output",
            str(l4_output),
        ]
    )
    l4_results = run_json_suite(
        l4_cmd,
        workspace,
        l4_output,
        "L4",
        "L4-FRONTEND-SUITE",
        "L4 frontend smoke suite",
        "P1",
        shared_env,
        timeout_seconds=1200,
    )
    l4_results.append(
        run_cos_real_smoke(
            workspace=workspace,
            base_url=args.base_url,
            admin_username=args.admin_username,
            admin_password=args.admin_password,
            extra_env=shared_env,
        )
    )

    layers: Dict[str, List[CheckResult]] = {
        "L1": l1_results,
        "L2": l2_results,
        "L3": l3_results,
        "L4": l4_results,
    }

    matrix_path = workspace / "testing/scenarios/business_flow_matrix.json"
    matrix = load_scenario_matrix(matrix_path)
    existing = merge_layer_results(layers)
    missing = attach_missing_scenarios(existing, matrix, mode="pr")
    for item in missing:
        layers.setdefault(item.layer, []).append(item)

    finished_at = now_iso()
    json_path, md_path, payload = persist_run_report(
        output_dir=output_dir,
        run_name="Hioshop PR Gate",
        mode="pr-gate",
        started_at=started_at,
        finished_at=finished_at,
        layers=layers,
    )

    failed = [r for r in merge_layer_results(layers) if r.status == "failed"]
    print(f"PR gate report json: {json_path}")
    print(f"PR gate report md: {md_path}")
    print(f"Summary: {payload.get('summary')}")
    print(f"Failed checks: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
