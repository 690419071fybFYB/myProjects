#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

import jwt
import requests

PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "testing" / "lib" / "common.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from testing.lib.common import ALLOWED_ERRNOS_DEFAULT, CheckResult, ensure_dir, write_json


PUBLIC_API_CONTROLLERS = {"index", "catalog", "auth", "goods", "search", "region"}
PUBLIC_API_ACTIONS = {
    "cart/index",
    "cart/add",
    "cart/checked",
    "cart/update",
    "cart/delete",
    "cart/goodscount",
    "pay/notify",
    "settings/showsettings",
}

ALLOWED_ERRNOS_CORE = {0, 100, 400, 401, 403, 404, 405, 412, 1000}
NON_JSON_ACTION_PATTERNS = (
    "export",
    "template",
    "errorfile",
)


@dataclass
class ProbeCase:
    id: str
    name: str
    layer: str
    severity: str
    method: str
    path: str
    token_kind: str  # none | api | admin
    params: Optional[Dict] = None
    body: Optional[Dict] = None
    allow_non_json: bool = False
    expected_errnos: Optional[Set[int]] = None


def build_token(secret: str, user_id: int) -> str:
    token = jwt.encode({"user_id": int(user_id)}, secret, algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token


def parse_errno(text: str) -> Optional[int]:
    try:
        body = json.loads(text)
    except Exception:
        return None
    if isinstance(body, dict) and "errno" in body:
        try:
            return int(body.get("errno"))
        except Exception:
            return None
    return None


def discover_actions(controller_dir: Path) -> List[Tuple[str, str]]:
    actions: List[Tuple[str, str]] = []
    for path in sorted(controller_dir.glob("*.js")):
        controller = path.stem
        content = path.read_text(encoding="utf-8")
        for action in re.findall(r"async\s+([A-Za-z0-9_]+)Action\s*\(", content):
            actions.append((controller, action))
    return actions


def guess_method(action: str) -> str:
    lower = action.lower()
    if any(
        lower.startswith(prefix)
        for prefix in (
            "get",
            "list",
            "index",
            "detail",
            "info",
            "count",
            "current",
            "check",
            "show",
            "messages",
            "unread",
            "tree",
            "main",
        )
    ):
        return "GET"
    if lower in {"index", "list", "detail", "info", "count", "main", "tree"}:
        return "GET"
    return "POST"


def build_default_payload() -> Dict:
    return {
        "id": -1,
        "orderId": -1,
        "order_id": -1,
        "userId": -1,
        "couponId": -1,
        "promotionId": -1,
        "goodsId": -1,
        "productId": -1,
        "addressId": -1,
        "page": 1,
        "size": 1,
        "showType": 0,
        "status": "unused",
        "keyword": "contract-smoke",
        "name": "contract-smoke",
        "sort": 0,
    }


def is_non_json_action(action: str) -> bool:
    lower = action.lower()
    return any(p in lower for p in NON_JSON_ACTION_PATTERNS)


def token_kind_for_api(controller: str, action: str) -> str:
    key = f"{controller}/{action.lower()}"
    if controller in PUBLIC_API_CONTROLLERS or key in PUBLIC_API_ACTIONS:
        return "none"
    return "api"


def token_kind_for_admin(controller: str, action: str) -> str:
    if controller == "auth" and action.lower() == "login":
        return "none"
    return "admin"


def build_core_cases() -> List[ProbeCase]:
    payload = build_default_payload()
    return [
        ProbeCase("L1-CORE-AUTH", "Auth loginByWeixin contract", "L1", "P1", "POST", "/api/auth/loginByWeixin", "none", body={"code": "invalid-code"}, expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase("L1-CORE-CART", "Cart core contract", "L1", "P1", "GET", "/api/cart/index", "none", params={"page": 1, "size": 1}, expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase("L1-CORE-ORDER", "Order core contract", "L1", "P1", "GET", "/api/order/list", "api", params={"page": 1, "size": 1, "showType": 0}, expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase(
            "L1-CORE-PAY",
            "Pay core contract",
            "L1",
            "P1",
            "POST",
            "/api/pay/notify",
            "none",
            body={"xml": {}},
            allow_non_json=True,
            expected_errnos=ALLOWED_ERRNOS_CORE,
        ),
        ProbeCase("L1-CORE-COUPON", "Coupon core contract", "L1", "P1", "GET", "/api/coupon/center", "api", params={"page": 1, "size": 1}, expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase("L1-CORE-ADDRESS", "Address core contract", "L1", "P1", "GET", "/api/address/getAddresses", "api", expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase("L1-CORE-SETTINGS", "Settings contract", "L1", "P2", "GET", "/api/settings/showSettings", "none", expected_errnos=ALLOWED_ERRNOS_CORE),
        ProbeCase("L1-CORE-AD", "Ad message contract", "L1", "P2", "GET", "/api/ad/messages", "api", params={"page": 1, "size": 1}, expected_errnos=ALLOWED_ERRNOS_CORE),
    ]


def build_full_cases(workspace: Path) -> List[ProbeCase]:
    payload = build_default_payload()
    cases: List[ProbeCase] = []

    api_actions = discover_actions(workspace / "hioshop-server" / "src" / "api" / "controller")
    admin_actions = discover_actions(workspace / "hioshop-server" / "src" / "admin" / "controller")

    for controller, action in api_actions:
        route_action = action
        method = guess_method(route_action)
        token_kind = token_kind_for_api(controller, route_action)
        case_id = f"L1-FULL-API-ACTIONS::{controller}.{route_action}"
        route_path = f"/api/{controller}/{route_action}"
        allow_non_json = is_non_json_action(route_action) or (controller == "pay" and route_action.lower() == "notify")
        case = ProbeCase(
            id=case_id,
            name=f"API contract {controller}.{route_action}",
            layer="L1",
            severity="P2",
            method=method,
            path=route_path,
            token_kind=token_kind,
            params=payload if method == "GET" else None,
            body=payload if method == "POST" else None,
            allow_non_json=allow_non_json,
            expected_errnos=ALLOWED_ERRNOS_DEFAULT,
        )
        cases.append(case)

    for controller, action in admin_actions:
        route_action = action
        method = guess_method(route_action)
        token_kind = token_kind_for_admin(controller, route_action)
        case_id = f"L1-FULL-ADMIN-ACTIONS::{controller}.{route_action}"
        route_path = f"/admin/{controller}/{route_action}"
        allow_non_json = is_non_json_action(route_action)
        body = payload.copy()
        if controller == "auth" and route_action.lower() == "login":
            body = {"username": "contract-smoke", "password": "contract-smoke"}
            method = "POST"
        case = ProbeCase(
            id=case_id,
            name=f"Admin contract {controller}.{route_action}",
            layer="L1",
            severity="P2",
            method=method,
            path=route_path,
            token_kind=token_kind,
            params=payload if method == "GET" else None,
            body=body if method == "POST" else None,
            allow_non_json=allow_non_json,
            expected_errnos=ALLOWED_ERRNOS_DEFAULT,
        )
        cases.append(case)

    return cases


def run_case(
    session: requests.Session,
    base_url: str,
    case: ProbeCase,
    api_token: str,
    admin_token: str,
) -> CheckResult:
    started = time.time()
    headers: Dict[str, str] = {}

    if case.token_kind == "api":
        if not api_token:
            return CheckResult(case.id, case.name, case.layer, "skipped", case.severity, "API token unavailable")
        headers["X-Hioshop-Token"] = api_token
    elif case.token_kind == "admin":
        if not admin_token:
            return CheckResult(case.id, case.name, case.layer, "skipped", case.severity, "Admin token unavailable")
        headers["X-Hioshop-Token"] = admin_token

    url = f"{base_url.rstrip('/')}{case.path}"
    try:
        if case.method == "GET":
            resp = session.get(url, params=case.params or {}, headers=headers, timeout=20)
        else:
            headers.setdefault("Content-Type", "application/json")
            resp = session.post(url, params=case.params or {}, json=case.body or {}, headers=headers, timeout=20)
    except Exception as err:
        return CheckResult(
            case.id,
            case.name,
            case.layer,
            "failed",
            case.severity,
            f"request error: {err}",
            elapsed_seconds=time.time() - started,
            command=f"{case.method} {case.path}",
        )

    elapsed = time.time() - started
    text = resp.text or ""

    if resp.status_code >= 500:
        return CheckResult(
            case.id,
            case.name,
            case.layer,
            "failed",
            case.severity,
            f"status={resp.status_code} server error",
            elapsed_seconds=elapsed,
            command=f"{case.method} {case.path}",
            evidence=text[:300],
        )

    errno = parse_errno(text)
    if errno is None:
        if case.allow_non_json:
            return CheckResult(
                case.id,
                case.name,
                case.layer,
                "passed",
                case.severity,
                f"status={resp.status_code} non-json allowed",
                elapsed_seconds=elapsed,
                command=f"{case.method} {case.path}",
            )
        return CheckResult(
            case.id,
            case.name,
            case.layer,
            "failed",
            case.severity,
            f"status={resp.status_code} non-json response",
            elapsed_seconds=elapsed,
            command=f"{case.method} {case.path}",
            evidence=text[:300],
        )

    allowed = case.expected_errnos or ALLOWED_ERRNOS_DEFAULT
    if errno not in allowed:
        return CheckResult(
            case.id,
            case.name,
            case.layer,
            "failed",
            case.severity,
            f"unexpected errno={errno}, status={resp.status_code}",
            elapsed_seconds=elapsed,
            command=f"{case.method} {case.path}",
            evidence=text[:300],
        )

    return CheckResult(
        case.id,
        case.name,
        case.layer,
        "passed",
        case.severity,
        f"status={resp.status_code}, errno={errno}",
        elapsed_seconds=elapsed,
        command=f"{case.method} {case.path}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run L1 contract suite")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--scope", choices=["core", "full"], default="core")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--api-jwt-secret", default="")
    parser.add_argument("--admin-jwt-secret", default="")
    parser.add_argument("--api-user-id", type=int, default=1048)
    parser.add_argument("--admin-user-id", type=int, default=14)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    cases = build_core_cases() if args.scope == "core" else build_full_cases(workspace)

    api_token = ""
    admin_token = ""
    if args.api_jwt_secret:
        api_token = build_token(args.api_jwt_secret, args.api_user_id)
    if args.admin_jwt_secret:
        admin_token = build_token(args.admin_jwt_secret, args.admin_user_id)

    session = requests.Session()
    session.trust_env = False

    results: List[CheckResult] = []
    for case in cases:
        results.append(run_case(session, args.base_url, case, api_token, admin_token))

    if args.scope == "full":
        api_items = [r for r in results if r.id.startswith("L1-FULL-API-ACTIONS::")]
        admin_items = [r for r in results if r.id.startswith("L1-FULL-ADMIN-ACTIONS::")]

        def aggregate(summary_id: str, summary_name: str, items: List[CheckResult]) -> CheckResult:
            if not items:
                return CheckResult(
                    id=summary_id,
                    name=summary_name,
                    layer="L1",
                    status="failed",
                    severity="P2",
                    message="no actions discovered",
                )
            failed = len([x for x in items if x.status == "failed"])
            skipped = len([x for x in items if x.status == "skipped"])
            status = "passed"
            if failed > 0:
                status = "failed"
            elif skipped > 0:
                status = "skipped"
            return CheckResult(
                id=summary_id,
                name=summary_name,
                layer="L1",
                status=status,
                severity="P2",
                message=f"actions={len(items)}, failed={failed}, skipped={skipped}",
            )

        results.append(aggregate("L1-FULL-API-ACTIONS", "All API actions contract probing", api_items))
        results.append(aggregate("L1-FULL-ADMIN-ACTIONS", "All Admin actions contract probing", admin_items))

        def aggregate_core(summary_id: str, summary_name: str, selector_suffixes: Sequence[str], severity: str = "P1") -> CheckResult:
            matched = [
                item
                for item in api_items
                if any(item.id.endswith(suffix) for suffix in selector_suffixes)
            ]
            if not matched:
                return CheckResult(
                    id=summary_id,
                    name=summary_name,
                    layer="L1",
                    status="failed",
                    severity=severity,
                    message="missing mapped full-action probes",
                )
            failed = len([x for x in matched if x.status == "failed"])
            skipped = len([x for x in matched if x.status == "skipped"])
            status = "passed"
            if failed > 0:
                status = "failed"
            elif skipped > 0:
                status = "skipped"
            return CheckResult(
                id=summary_id,
                name=summary_name,
                layer="L1",
                status=status,
                severity=severity,
                message=f"mapped_actions={len(matched)}, failed={failed}, skipped={skipped}",
            )

        results.append(aggregate_core("L1-CORE-AUTH", "Auth and profile-gate contract responses", ("auth.loginByWeixin",)))
        results.append(aggregate_core("L1-CORE-CART", "Cart core contract responses", ("cart.index",)))
        results.append(aggregate_core("L1-CORE-ORDER", "Order core contract responses", ("order.list",)))
        results.append(aggregate_core("L1-CORE-PAY", "Pay core contract responses", ("pay.notify",)))
        results.append(aggregate_core("L1-CORE-COUPON", "Coupon core contract responses", ("coupon.center",)))
        results.append(aggregate_core("L1-CORE-ADDRESS", "Address core contract responses", ("address.getAddresses",)))
        results.append(aggregate_core("L1-CORE-SETTINGS", "Settings and app config contract responses", ("settings.showSettings",), severity="P2"))
        results.append(aggregate_core("L1-CORE-AD", "Ad message contract responses", ("ad.messages",), severity="P2"))

    payload = {
        "suite": "L1-contract",
        "scope": args.scope,
        "base_url": args.base_url,
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

    failed = len([r for r in results if r.status == "failed"])
    if failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
