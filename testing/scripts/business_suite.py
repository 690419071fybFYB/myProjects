#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import jwt
import requests

PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "testing" / "lib" / "common.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from testing.lib.common import CheckResult, ensure_dir, format_cmd, run_command, write_json


SCENARIO_META: Dict[str, Dict[str, str]] = {
    "L2-HOME-PAGE": {"name": "Home page load and popup/channel visibility", "severity": "P1"},
    "L2-LOGIN-GATE": {"name": "Login gate and profile completeness checks", "severity": "P0"},
    "L2-GOODS-FLOW": {"name": "Goods detail/spec/add-cart/buy-now flow", "severity": "P0"},
    "L2-CART-FLOW": {"name": "Cart select/update/delete/count flow", "severity": "P0"},
    "L2-ADDRESS-FLOW": {"name": "Address create/default/use flow", "severity": "P0"},
    "L2-CHECKOUT-FLOW": {"name": "Checkout freight/promotion/coupon flow", "severity": "P0"},
    "L2-SUBMIT-FLOW": {"name": "Submit order and anti-tamper flow", "severity": "P0"},
    "L2-PAY-FLOW": {"name": "Pay notify and idempotency flow", "severity": "P0"},
    "L2-ORDER-LIFECYCLE": {"name": "Order lifecycle cancel/status flow", "severity": "P0"},
    "L2-COUPON-LIFECYCLE": {"name": "Coupon receive/preview/lock/use/release flow", "severity": "P0"},
    "L2-PROMOTION-LIFECYCLE": {"name": "Promotion and best-price flow", "severity": "P0"},
    "L2-INVITE-FLOW": {"name": "Invite summary and records flow", "severity": "P2"},
    "L2-AD-MESSAGE-FLOW": {"name": "Ad unread/list/readAll flow", "severity": "P2"},
    "L2-OPERATIONS-FLOW": {"name": "Admin import/export operation flow", "severity": "P2"},
    "L2-SEARCH-FOOTPRINT": {"name": "Search and footprint flow", "severity": "P2"},
}


def now_ts() -> int:
    return int(time.time())


@dataclass
class Config:
    scope: str
    workspace: Path
    base_url: str
    api_jwt_secret: str
    admin_jwt_secret: str
    api_user_id: int
    admin_user_id: int
    admin_username: str
    admin_password: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    pay_workers: int


def build_token(secret: str, user_id: int) -> str:
    token = jwt.encode({"user_id": int(user_id)}, secret, algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token


def scenario_info(sid: str) -> Dict[str, str]:
    return SCENARIO_META.get(sid, {"name": sid, "severity": "P2"})


def summarize_output(stdout: str, stderr: str) -> str:
    text = (stdout or "").strip() or (stderr or "").strip()
    if not text:
        return "command finished"
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "command finished"
    tail = lines[-1]
    if len(tail) > 220:
        return tail[:217] + "..."
    return tail


def fanout_command_result(
    scenario_ids: List[str],
    cmd: str,
    result,
) -> List[CheckResult]:
    status = "passed" if result.status == "passed" else "failed"
    message = summarize_output(result.stdout, result.stderr)
    evidence = ""
    if status == "failed":
        raw = (result.stderr or result.stdout or "").strip()
        if raw:
            evidence = raw[:500]
    checks: List[CheckResult] = []
    for sid in scenario_ids:
        meta = scenario_info(sid)
        checks.append(
            CheckResult(
                id=sid,
                name=meta["name"],
                layer="L2",
                status=status,
                severity=meta["severity"],
                message=message,
                elapsed_seconds=result.elapsed_seconds,
                evidence=evidence,
                command=cmd,
            )
        )
    return checks


def load_suite_results(output_path: Path) -> List[CheckResult]:
    if not output_path.exists():
        return []
    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    raw = payload.get("results")
    if not isinstance(raw, list):
        return []
    results: List[CheckResult] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        results.append(
            CheckResult(
                id=str(item.get("id") or "UNKNOWN"),
                name=str(item.get("name") or item.get("id") or "unknown check"),
                layer=str(item.get("layer") or "L2"),
                status=str(item.get("status") or "failed"),
                severity=str(item.get("severity") or "P2"),
                message=str(item.get("message") or ""),
                elapsed_seconds=float(item.get("elapsed_seconds") or 0.0),
                evidence=str(item.get("evidence") or ""),
                command=str(item.get("command") or ""),
            )
        )
    return results


def run_home_page_smoke(cfg: Config) -> CheckResult:
    started = time.time()
    session = requests.Session()
    session.trust_env = False
    token = build_token(cfg.api_jwt_secret, cfg.api_user_id) if cfg.api_jwt_secret else ""
    headers: Dict[str, str] = {}
    if token:
        headers["X-Hioshop-Token"] = token

    def fetch_json_with_retry(path: str, retries: int = 3):
        last_err = ""
        last_text = ""
        last_status = 0
        for i in range(retries):
            try:
                resp = session.get(f"{cfg.base_url.rstrip('/')}{path}", headers=headers, timeout=20)
                last_status = int(resp.status_code)
                raw = resp.text or ""
                last_text = raw
                try:
                    body = json.loads(raw)
                except Exception as err:
                    last_err = f"non-json attempt={i + 1}: {err}"
                    time.sleep(0.15)
                    continue
                errno = int(body.get("errno", -99999))
                if errno == 0:
                    return body, resp.status_code, raw
                last_err = f"errno={errno} attempt={i + 1}"
                time.sleep(0.15)
            except Exception as err:
                last_err = f"request error attempt={i + 1}: {err}"
                time.sleep(0.15)
        raise RuntimeError(f"{path} failed after retry, status={last_status}, last_err={last_err}, body={last_text[:180]}")

    try:
        app_info_body, app_status, app_raw = fetch_json_with_retry("/api/index/appInfo")
        app_errno = int(app_info_body.get("errno", -99999))
        if app_errno != 0:
            return CheckResult(
                id="L2-HOME-PAGE",
                name=scenario_info("L2-HOME-PAGE")["name"],
                layer="L2",
                status="failed",
                severity=scenario_info("L2-HOME-PAGE")["severity"],
                message=f"appInfo errno={app_errno}, status={app_status}",
                elapsed_seconds=time.time() - started,
                evidence=(app_raw or "")[:350],
                command="GET /api/index/appInfo",
            )

        data = app_info_body.get("data") or {}
        has_popup = 1 if (data.get("popupAd") or {}).get("id") else 0
        return CheckResult(
            id="L2-HOME-PAGE",
            name=scenario_info("L2-HOME-PAGE")["name"],
            layer="L2",
            status="passed",
            severity=scenario_info("L2-HOME-PAGE")["severity"],
            message=f"appInfo ok, popupAd_present={has_popup}",
            elapsed_seconds=time.time() - started,
            command="GET /api/index/appInfo",
        )
    except Exception as err:
        return CheckResult(
            id="L2-HOME-PAGE",
            name=scenario_info("L2-HOME-PAGE")["name"],
            layer="L2",
            status="failed",
            severity=scenario_info("L2-HOME-PAGE")["severity"],
            message=f"request error: {err}",
            elapsed_seconds=time.time() - started,
            command="GET /api/index/appInfo",
        )


def run_suite(cfg: Config) -> List[CheckResult]:
    results: List[CheckResult] = []
    server_dir = cfg.workspace / "hioshop-server"

    node_env = {
        "COUPON_TEST_BASE_URL": cfg.base_url,
        "COUPON_TEST_ADMIN_USER_ID": str(cfg.admin_user_id),
        "COUPON_TEST_USER_ID": str(cfg.api_user_id),
        "COUPON_TEST_DB_HOST": cfg.db_host,
        "COUPON_TEST_DB_PORT": str(cfg.db_port),
        "COUPON_TEST_DB_USER": cfg.db_user,
        "COUPON_TEST_DB_PASSWORD": cfg.db_password,
        "COUPON_TEST_DB_NAME": cfg.db_name,
        "API_TOKEN_SECRET": cfg.api_jwt_secret,
        "ADMIN_TOKEN_SECRET": cfg.admin_jwt_secret,
        "HIOSHOP_ADMIN_API": f"{cfg.base_url.rstrip('/')}/admin",
        "HIOSHOP_ADMIN_USER": cfg.admin_username,
        "HIOSHOP_ADMIN_PASS": cfg.admin_password,
    }

    if cfg.scope == "full":
        results.append(run_home_page_smoke(cfg))

    core_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/core_user_journey.py",
            "--base-url",
            cfg.base_url,
            "--api-jwt-secret",
            cfg.api_jwt_secret,
            "--api-user-id",
            str(cfg.api_user_id),
            "--db-host",
            cfg.db_host,
            "--db-port",
            str(cfg.db_port),
            "--db-user",
            cfg.db_user,
            "--db-password",
            cfg.db_password,
            "--db-name",
            cfg.db_name,
        ]
    )
    core_result = run_command(core_cmd, cfg.workspace, timeout_seconds=900, extra_env=node_env)
    core_ids = [
        "L2-LOGIN-GATE",
        "L2-GOODS-FLOW",
        "L2-CART-FLOW",
        "L2-ADDRESS-FLOW",
        "L2-CHECKOUT-FLOW",
        "L2-SUBMIT-FLOW",
        "L2-ORDER-LIFECYCLE",
    ]
    results.extend(fanout_command_result(core_ids, core_cmd, core_result))

    pay_cmd = format_cmd(
        [
            "python3",
            "testing/scripts/pay_notify_concurrency.py",
            "--base-url",
            cfg.base_url,
            "--workers",
            str(max(1, cfg.pay_workers)),
            "--user-id",
            str(cfg.api_user_id),
            "--api-jwt-secret",
            cfg.api_jwt_secret,
            "--db-host",
            cfg.db_host,
            "--db-port",
            str(cfg.db_port),
            "--db-user",
            cfg.db_user,
            "--db-password",
            cfg.db_password,
            "--db-name",
            cfg.db_name,
        ]
    )
    pay_result = run_command(pay_cmd, cfg.workspace, timeout_seconds=1200, extra_env=node_env)
    results.extend(fanout_command_result(["L2-PAY-FLOW"], pay_cmd, pay_result))

    coupon_cmd = "node scripts/test-coupon.js"
    coupon_result = run_command(coupon_cmd, server_dir, timeout_seconds=1200, extra_env=node_env)
    results.extend(fanout_command_result(["L2-COUPON-LIFECYCLE"], coupon_cmd, coupon_result))

    promo_cmd = "node scripts/test-promotion-v1.js"
    promo_result = run_command(promo_cmd, server_dir, timeout_seconds=600, extra_env=node_env)
    results.extend(fanout_command_result(["L2-PROMOTION-LIFECYCLE"], promo_cmd, promo_result))

    if cfg.scope == "full":
        import_cmd = "node scripts/test-goods-import.js"
        import_result = run_command(import_cmd, server_dir, timeout_seconds=1800, extra_env=node_env)
        import_check = fanout_command_result(["L2-OPERATIONS-FLOW"], import_cmd, import_result)[0]

        ops_output = cfg.workspace / "testing-artifacts" / f"operations-audit-{now_ts()}.json"
        ops_cmd = format_cmd(
            [
                "python3",
                "testing/scripts/operations_audit_suite.py",
                "--base-url",
                cfg.base_url,
                "--admin-username",
                cfg.admin_username,
                "--admin-password",
                cfg.admin_password,
                "--db-host",
                cfg.db_host,
                "--db-port",
                str(cfg.db_port),
                "--db-user",
                cfg.db_user,
                "--db-password",
                cfg.db_password,
                "--db-name",
                cfg.db_name,
                "--output",
                str(ops_output),
            ]
        )
        ops_result = run_command(ops_cmd, cfg.workspace, timeout_seconds=1200, extra_env=node_env)
        parsed_ops = load_suite_results(ops_output)
        ops_check = (
            parsed_ops[0]
            if parsed_ops
            else fanout_command_result(["L2-OPERATIONS-FLOW"], ops_cmd, ops_result)[0]
        )

        if import_check.status == "failed" or ops_check.status == "failed":
            status = "failed"
        elif import_check.status == "skipped" and ops_check.status == "skipped":
            status = "skipped"
        else:
            status = "passed"
        results.append(
            CheckResult(
                id="L2-OPERATIONS-FLOW",
                name="Admin goods import task records and exports",
                layer="L2",
                status=status,
                severity="P2",
                message=f"import_script={import_check.status}; operations_audit={ops_check.status}",
                elapsed_seconds=import_check.elapsed_seconds + ops_check.elapsed_seconds,
                evidence=f"import:{import_check.message}; audit:{ops_check.message}",
                command=f"{import_cmd} && {ops_cmd}",
            )
        )

        domain_output = cfg.workspace / "testing-artifacts" / f"domain-suite-{now_ts()}.json"
        domain_cmd = format_cmd(
            [
                "python3",
                "testing/scripts/domain_flow_suite.py",
                "--base-url",
                cfg.base_url,
                "--api-jwt-secret",
                cfg.api_jwt_secret,
                "--api-user-id",
                str(cfg.api_user_id),
                "--db-host",
                cfg.db_host,
                "--db-port",
                str(cfg.db_port),
                "--db-user",
                cfg.db_user,
                "--db-password",
                cfg.db_password,
                "--db-name",
                cfg.db_name,
                "--output",
                str(domain_output),
            ]
        )
        domain_result = run_command(domain_cmd, cfg.workspace, timeout_seconds=1200, extra_env=node_env)
        parsed = load_suite_results(domain_output)
        if parsed:
            results.extend(parsed)
        else:
            results.extend(
                fanout_command_result(
                    ["L2-INVITE-FLOW", "L2-AD-MESSAGE-FLOW", "L2-SEARCH-FOOTPRINT"],
                    domain_cmd,
                    domain_result,
                )
            )

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run L2 business-chain suite")
    parser.add_argument("--scope", choices=["core", "full"], default="core")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--api-jwt-secret", default="")
    parser.add_argument("--admin-jwt-secret", default="")
    parser.add_argument("--api-user-id", type=int, default=1048)
    parser.add_argument("--admin-user-id", type=int, default=14)
    parser.add_argument("--admin-username", default="qilelab.com")
    parser.add_argument("--admin-password", default="qilelab.com")
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="")
    parser.add_argument("--db-name", default="hiolabsDB")
    parser.add_argument("--pay-workers", type=int, default=1)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    cfg = Config(
        scope=args.scope,
        workspace=Path(args.workspace).resolve(),
        base_url=args.base_url,
        api_jwt_secret=args.api_jwt_secret,
        admin_jwt_secret=args.admin_jwt_secret,
        api_user_id=args.api_user_id,
        admin_user_id=args.admin_user_id,
        admin_username=args.admin_username,
        admin_password=args.admin_password,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
        pay_workers=args.pay_workers,
    )

    results = run_suite(cfg)
    payload = {
        "suite": "L2-business",
        "scope": cfg.scope,
        "results": [r.__dict__ for r in results],
        "summary": {
            "total": len(results),
            "passed": len([r for r in results if r.status == "passed"]),
            "failed": len([r for r in results if r.status == "failed"]),
            "skipped": len([r for r in results if r.status == "skipped"]),
        },
    }
    if args.output:
        out = Path(args.output)
        ensure_dir(out.parent)
        write_json(out, payload)

    return 1 if any(r.status == "failed" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
