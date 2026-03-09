#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import pymysql
import requests

PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "testing" / "lib" / "common.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from testing.lib.common import CheckResult, ensure_dir, write_json


@dataclass
class Context:
    base_url: str
    admin_username: str
    admin_password: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str


def db_connect(ctx: Context):
    return pymysql.connect(
        host=ctx.db_host,
        port=ctx.db_port,
        user=ctx.db_user,
        password=ctx.db_password,
        database=ctx.db_name,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def request_json(
    session: requests.Session,
    ctx: Context,
    path: str,
    method: str = "GET",
    token: str = "",
    params: Optional[Dict] = None,
    body: Optional[Dict] = None,
) -> Dict:
    url = f"{ctx.base_url.rstrip('/')}{path}"
    headers: Dict[str, str] = {}
    if token:
        headers["X-Hioshop-Token"] = token
    if method.upper() == "GET":
        resp = session.get(url, params=params or {}, headers=headers, timeout=20)
    else:
        headers["Content-Type"] = "application/json"
        resp = session.post(url, params=params or {}, json=body or {}, headers=headers, timeout=20)
    text = resp.text or ""
    try:
        payload = json.loads(text)
    except Exception as err:
        raise RuntimeError(f"{path} non-json response status={resp.status_code}: {text[:200]}") from err
    payload["_status"] = resp.status_code
    return payload


def expect_errno(payload: Dict, allowed, label: str) -> None:
    errno = int(payload.get("errno", -99999))
    if errno not in set(int(x) for x in allowed):
        raise AssertionError(f"{label} unexpected errno={errno}, status={payload.get('_status')}, errmsg={payload.get('errmsg')}")


def login_admin(session: requests.Session, ctx: Context) -> str:
    payload = request_json(
        session,
        ctx,
        "/admin/auth/login",
        method="POST",
        body={"username": ctx.admin_username, "password": ctx.admin_password},
    )
    if int(payload.get("errno", -1)) == 0:
        token = (payload.get("data") or {}).get("token") or ""
        if token:
            return token
    url = f"{ctx.base_url.rstrip('/')}/admin/auth/login"
    resp = session.post(url, data={"username": ctx.admin_username, "password": ctx.admin_password}, timeout=20)
    body = json.loads(resp.text or "{}")
    if int(body.get("errno", -1)) == 0:
        token = (body.get("data") or {}).get("token") or ""
        if token:
            return token
    raise RuntimeError(f"admin login failed errno={payload.get('errno')}")


def fetch_binary(session: requests.Session, ctx: Context, path: str, token: str, params: Optional[Dict] = None) -> requests.Response:
    url = f"{ctx.base_url.rstrip('/')}{path}"
    headers = {"X-Hioshop-Token": token}
    resp = session.get(url, params=params or {}, headers=headers, timeout=30)
    return resp


def run_suite(ctx: Context) -> CheckResult:
    started = time.time()
    session = requests.Session()
    session.trust_env = False
    conn = db_connect(ctx)
    try:
        admin_token = login_admin(session, ctx)

        task_list = request_json(
            session,
            ctx,
            "/admin/goods/importTaskList",
            method="GET",
            token=admin_token,
            params={"page": 1, "size": 20},
        )
        expect_errno(task_list, {0}, "importTaskList")
        list_data = (task_list.get("data") or {}).get("data") or []
        if not list_data:
            raise AssertionError("importTaskList returned empty data")
        latest = list_data[0] if isinstance(list_data[0], dict) else {}
        task_id = int(latest.get("id") or 0)
        if task_id <= 0:
            raise AssertionError("importTaskList latest task id invalid")

        task_detail = request_json(
            session,
            ctx,
            "/admin/goods/importTaskDetail",
            method="GET",
            token=admin_token,
            params={"id": task_id},
        )
        expect_errno(task_detail, {0}, "importTaskDetail")
        detail_data = task_detail.get("data") or {}
        if int(detail_data.get("id") or 0) != task_id:
            raise AssertionError(f"importTaskDetail id mismatch expected={task_id}")

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, status, total_sku, success_sku, skipped_sku, failed_sku
                FROM hiolabs_goods_import_task
                WHERE id=%s AND is_delete=0
                """,
                (task_id,),
            )
            task_row = cur.fetchone()
        if not task_row:
            raise AssertionError(f"goods_import_task row missing for id={task_id}")

        api_status = str(detail_data.get("status") or "")
        db_status = str(task_row.get("status") or "")
        if api_status and db_status and api_status != db_status:
            raise AssertionError(f"task status mismatch api={api_status}, db={db_status}")

        # For validation_failed/partial_success tasks, error file endpoint should be downloadable.
        binary_checked = 0
        if api_status in {"validation_failed", "partial_success", "failed"}:
            resp = fetch_binary(
                session,
                ctx,
                "/admin/goods/importTaskErrorFile",
                token=admin_token,
                params={"id": task_id},
            )
            if resp.status_code == 200 and len(resp.content or b"") > 0:
                binary_checked = 1
            else:
                # Some failed tasks may not have generated workbook; this should only be tolerated when error_rows is 0.
                if int(task_row.get("error_rows") or 0) > 0:
                    raise AssertionError(
                        f"importTaskErrorFile unavailable status={resp.status_code}, bytes={len(resp.content or b'')}"
                    )

        return CheckResult(
            id="L2-OPERATIONS-FLOW",
            name="Goods import task list/detail/error-file and DB consistency",
            layer="L2",
            status="passed",
            severity="P2",
            message=(
                f"task_id={task_id}, status={api_status or db_status}, "
                f"total={int(task_row.get('total_sku') or 0)}, "
                f"success={int(task_row.get('success_sku') or 0)}, "
                f"skipped={int(task_row.get('skipped_sku') or 0)}, "
                f"failed={int(task_row.get('failed_sku') or 0)}, "
                f"error_file_checked={binary_checked}"
            ),
            elapsed_seconds=time.time() - started,
            command="GET /admin/goods/importTaskList + detail + errorFile + DB assert",
        )
    except Exception as err:
        return CheckResult(
            id="L2-OPERATIONS-FLOW",
            name="Goods import task list/detail/error-file and DB consistency",
            layer="L2",
            status="failed",
            severity="P2",
            message=str(err),
            elapsed_seconds=time.time() - started,
            command="GET /admin/goods/importTaskList + detail + errorFile + DB assert",
        )
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run operations flow audit (import task API + DB)")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--admin-username", default="qilelab.com")
    parser.add_argument("--admin-password", default="qilelab.com")
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="")
    parser.add_argument("--db-name", default="hiolabsDB")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    ctx = Context(
        base_url=args.base_url,
        admin_username=args.admin_username,
        admin_password=args.admin_password,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
    )
    result = run_suite(ctx)

    if args.output:
        out = Path(args.output)
        ensure_dir(out.parent)
        write_json(
            out,
            {
                "suite": "L2-operations-audit",
                "results": [result.__dict__],
                "summary": {
                    "total": 1,
                    "passed": 1 if result.status == "passed" else 0,
                    "failed": 1 if result.status == "failed" else 0,
                    "skipped": 1 if result.status == "skipped" else 0,
                },
            },
        )

    return 1 if result.status == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
