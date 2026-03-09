#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

import requests

PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "testing" / "lib" / "common.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from testing.lib.common import CheckResult, run_command, ensure_dir, write_json


def run_node_syntax_checks(workspace: Path) -> CheckResult:
    started = time.time()
    mini_dir = workspace / "hioshop-miniprogram"
    cmd = (
        "node -c app.js && "
        "node -c utils/request/index.js && "
        "node -c utils/util.js && "
        "node -c pages/order-check/index.js && "
        "node -c pages/order-coupon/index.js && "
        "node -c pages/ucenter/index/index.js"
    )
    result = run_command(cmd, mini_dir, timeout_seconds=300)
    if result.status == "passed":
        return CheckResult(
            id="L4-MINI-SYNTAX-SMOKE",
            name="Mini key page JS syntax smoke",
            layer="L4",
            status="passed",
            severity="P2",
            message="syntax checks passed",
            elapsed_seconds=time.time() - started,
            command=cmd,
        )
    return CheckResult(
        id="L4-MINI-SYNTAX-SMOKE",
        name="Mini key page JS syntax smoke",
        layer="L4",
        status="failed",
        severity="P2",
        message=(result.stderr or result.stdout or "syntax check failed")[:300],
        elapsed_seconds=time.time() - started,
        command=cmd,
    )


def run_request_sdk_smoke(workspace: Path) -> CheckResult:
    started = time.time()
    cmd = "node testing/scripts/miniprogram_request_smoke.js"
    result = run_command(cmd, workspace, timeout_seconds=120)
    if result.status == "passed":
        return CheckResult(
            id="L4-MINI-REQUEST-SMOKE",
            name="Mini request SDK smoke",
            layer="L4",
            status="passed",
            severity="P1",
            message="401/412/network handling smoke passed",
            elapsed_seconds=time.time() - started,
            command=cmd,
        )
    return CheckResult(
        id="L4-MINI-REQUEST-SMOKE",
        name="Mini request SDK smoke",
        layer="L4",
        status="failed",
        severity="P1",
        message=(result.stderr or result.stdout or "request smoke failed")[:300],
        elapsed_seconds=time.time() - started,
        command=cmd,
    )


def run_admin_login_smoke(base_url: str, username: str, password: str) -> CheckResult:
    started = time.time()
    session = requests.Session()
    session.trust_env = False
    url = f"{base_url.rstrip('/')}/admin/auth/login"
    try:
        resp = session.post(url, json={"username": username, "password": password}, timeout=20)
        text = resp.text or ""
        body = json.loads(text)
        if int(body.get("errno", -99999)) != 0:
            # Fallback for environments that require form style payload.
            resp = session.post(url, data={"username": username, "password": password}, timeout=20)
            text = resp.text or ""
            body = json.loads(text)
        errno = int(body.get("errno", -99999))
        if errno == 0 and (body.get("data") or {}).get("token"):
            return CheckResult(
                id="L4-ADMIN-LOGIN-SMOKE",
                name="Admin login smoke",
                layer="L4",
                status="passed",
                severity="P1",
                message="admin login passed",
                elapsed_seconds=time.time() - started,
                command="POST /admin/auth/login",
            )
        return CheckResult(
            id="L4-ADMIN-LOGIN-SMOKE",
            name="Admin login smoke",
            layer="L4",
            status="failed",
            severity="P1",
            message=f"login errno={errno}, status={resp.status_code}",
            elapsed_seconds=time.time() - started,
            command="POST /admin/auth/login",
            evidence=text[:300],
        )
    except Exception as err:
        return CheckResult(
            id="L4-ADMIN-LOGIN-SMOKE",
            name="Admin login smoke",
            layer="L4",
            status="failed",
            severity="P1",
            message=f"request error: {err}",
            elapsed_seconds=time.time() - started,
            command="POST /admin/auth/login",
        )


def run_suite(workspace: Path, base_url: str, admin_username: str, admin_password: str) -> List[CheckResult]:
    results: List[CheckResult] = []
    results.append(run_request_sdk_smoke(workspace))
    results.append(run_node_syntax_checks(workspace))
    results.append(run_admin_login_smoke(base_url, admin_username, admin_password))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run L4 frontend smoke suite")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--admin-username", default="qilelab.com")
    parser.add_argument("--admin-password", default="qilelab.com")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    results = run_suite(workspace, args.base_url, args.admin_username, args.admin_password)

    if args.output:
        out = Path(args.output)
        ensure_dir(out.parent)
        write_json(
            out,
            {
                "suite": "L4-frontend-smoke",
                "results": [r.__dict__ for r in results],
                "summary": {
                    "total": len(results),
                    "passed": len([r for r in results if r.status == "passed"]),
                    "failed": len([r for r in results if r.status == "failed"]),
                    "skipped": len([r for r in results if r.status == "skipped"]),
                },
            },
        )

    return 1 if any(r.status == "failed" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
