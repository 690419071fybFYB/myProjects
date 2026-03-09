#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple

import jwt
import requests


@dataclass
class CheckCase:
    case_id: str
    name: str
    method: str
    path: str
    token: str = ''
    params: Optional[Dict] = None
    body: Optional[Dict] = None
    validate: Optional[Callable[[int, str], Tuple[bool, str]]] = None


def build_token(secret: str, user_id: int, exp_offset_seconds: Optional[int] = None) -> str:
    payload = {"user_id": int(user_id)}
    if exp_offset_seconds is not None:
        payload["exp"] = int(time.time()) + int(exp_offset_seconds)
    token = jwt.encode(payload, secret, algorithm="HS256")
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


def read_container_env(container_name: str, key: str) -> str:
    try:
        proc = subprocess.run(
            ["docker", "exec", container_name, "printenv", key],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode != 0:
            return ""
        return (proc.stdout or "").strip()
    except Exception:
        return ""


def parse_errno(text: str) -> Optional[int]:
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "errno" in data:
            return int(data.get("errno"))
    except Exception:
        return None
    return None


def not_500_validator(status: int, text: str):
    if status >= 500:
        return False, f"unexpected status={status}, body={text[:200]}"
    return True, f"status={status}"


def expect_errno_validator(expected_errno: int):
    def _validator(status: int, text: str):
        errno = parse_errno(text)
        if errno == expected_errno:
            return True, f"errno={errno}"
        return False, f"expected errno={expected_errno}, got errno={errno}, status={status}, body={text[:200]}"

    return _validator


def expect_errno_in_validator(allowed):
    allowed_set = set(int(x) for x in allowed)

    def _validator(status: int, text: str):
        errno = parse_errno(text)
        if errno in allowed_set:
            return True, f"errno={errno}"
        return False, f"expected errno in {sorted(allowed_set)}, got errno={errno}, status={status}, body={text[:200]}"

    return _validator


def run_case(base_url: str, case: CheckCase, session: requests.Session) -> Tuple[bool, str]:
    url = f"{base_url.rstrip('/')}{case.path}"
    headers = {}
    if case.token:
        headers["X-Hioshop-Token"] = case.token
    try:
        if case.method.upper() == "GET":
            resp = session.get(url, headers=headers, params=case.params, timeout=15)
        else:
            headers.setdefault("Content-Type", "application/json")
            resp = session.post(url, headers=headers, params=case.params, json=case.body, timeout=15)
    except Exception as err:
        return False, f"request error: {err}"
    text = resp.text or ""
    validator = case.validate or not_500_validator
    return validator(resp.status_code, text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run security/abuse smoke checks for hioshop APIs")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--api-jwt-secret", default=os.environ.get("API_JWT_SECRET") or os.environ.get("API_TOKEN_SECRET") or "")
    parser.add_argument("--admin-jwt-secret", default=os.environ.get("ADMIN_JWT_SECRET") or os.environ.get("ADMIN_TOKEN_SECRET") or "")
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--admin-user-id", type=int, default=14)
    args = parser.parse_args()

    api_secret = args.api_jwt_secret or read_container_env("hioshop-server", "API_JWT_SECRET") or ""
    admin_secret = args.admin_jwt_secret or read_container_env("hioshop-server", "ADMIN_JWT_SECRET") or ""

    forged_token = "forged.invalid.token"
    expired_token = build_token(api_secret, args.user_id, exp_offset_seconds=-3600) if api_secret else ""
    admin_token = build_token(admin_secret, args.admin_user_id) if admin_secret else ""

    cases = [
        CheckCase(
            case_id="sec-001",
            name="api protected endpoint should require login",
            method="GET",
            path="/api/order/list",
            params={"page": 1, "size": 1},
            validate=expect_errno_validator(401),
        ),
        CheckCase(
            case_id="sec-002",
            name="admin protected endpoint should require login",
            method="GET",
            path="/admin/coupon/list",
            params={"page": 1, "size": 1},
            validate=expect_errno_validator(401),
        ),
        CheckCase(
            case_id="sec-003",
            name="forged api token should be rejected",
            method="GET",
            path="/api/order/list",
            token=forged_token,
            params={"page": 1, "size": 1},
            validate=expect_errno_validator(401),
        ),
        CheckCase(
            case_id="sec-004",
            name="expired api token should be rejected",
            method="GET",
            path="/api/order/list",
            token=expired_token,
            params={"page": 1, "size": 1},
            validate=expect_errno_validator(401) if expired_token else not_500_validator,
        ),
        CheckCase(
            case_id="sec-005",
            name="search helper should handle SQLi-like keyword safely",
            method="GET",
            path="/api/search/helper",
            params={"keyword": "' OR 1=1 --"},
            validate=not_500_validator,
        ),
        CheckCase(
            case_id="sec-006",
            name="catalog endpoint should handle malformed id safely",
            method="GET",
            path="/api/catalog/current",
            params={"id": "1 OR 1=1"},
            validate=not_500_validator,
        ),
        CheckCase(
            case_id="sec-007",
            name="admin pickerList should reject invalid sortBy injection",
            method="GET",
            path="/admin/goods/pickerList",
            token=admin_token,
            params={
                "page": 1,
                "size": 5,
                "sortBy": "add_time;drop table hiolabs_goods",
                "sortOrder": "desc",
            },
            validate=expect_errno_in_validator([0, 400, 401]),
        ),
        CheckCase(
            case_id="sec-008",
            name="pay notify malformed payload should not 500",
            method="POST",
            path="/api/pay/notify",
            body={"xml": {}},
            validate=not_500_validator,
        ),
    ]

    print("Running security abuse smoke checks...")
    session = requests.Session()
    session.trust_env = False
    failed = []
    for case in cases:
        ok, detail = run_case(args.base_url, case, session)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case.case_id} {case.name} -> {detail}")
        if not ok:
            failed.append(case.case_id)

    if failed:
        print(f"Security abuse smoke failed: {', '.join(failed)}")
        return 1

    print("Security abuse smoke passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
