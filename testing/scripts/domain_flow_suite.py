#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import jwt
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
    api_jwt_secret: str
    api_user_id: int
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str


def now_ts() -> int:
    return int(time.time())


def build_token(secret: str, user_id: int) -> str:
    token = jwt.encode({"user_id": int(user_id)}, secret, algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token


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


def has_table(conn, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(1) AS total
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
            """,
            (table_name,),
        )
        row = cur.fetchone() or {}
    return int(row.get("total") or 0) > 0


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


def run_invite_flow(session: requests.Session, conn, ctx: Context, token: str) -> CheckResult:
    started = time.time()
    try:
        summary = request_json(session, ctx, "/api/invite/mySummary", method="GET", token=token)
        expect_errno(summary, {0}, "invite summary")
        records = request_json(session, ctx, "/api/invite/myRecords", method="GET", token=token, params={"page": 1, "size": 10})
        expect_errno(records, {0}, "invite records")

        summary_data = summary.get("data") or {}
        schema_ready = has_table(conn, "hiolabs_invite_relation")
        evidence = "schema_ready=0"
        if schema_ready:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(1) AS total FROM hiolabs_invite_relation WHERE inviter_user_id=%s",
                    (int(ctx.api_user_id),),
                )
                row = cur.fetchone() or {}
            db_total = int(row.get("total") or 0)
            api_total = int(summary_data.get("total_invite_count") or 0)
            if api_total != db_total:
                raise AssertionError(f"invite total mismatch api={api_total}, db={db_total}")
            evidence = f"schema_ready=1, invite_total={api_total}"

        return CheckResult(
            id="L2-INVITE-FLOW",
            name="Invite summary/records and optional relation consistency",
            layer="L2",
            status="passed",
            severity="P2",
            message=evidence,
            elapsed_seconds=time.time() - started,
            command="GET /api/invite/mySummary + GET /api/invite/myRecords",
        )
    except Exception as err:
        return CheckResult(
            id="L2-INVITE-FLOW",
            name="Invite summary/records and optional relation consistency",
            layer="L2",
            status="failed",
            severity="P2",
            message=str(err),
            elapsed_seconds=time.time() - started,
            command="GET /api/invite/mySummary + GET /api/invite/myRecords",
        )


def run_ad_flow(session: requests.Session, conn, ctx: Context, token: str) -> CheckResult:
    started = time.time()
    try:
        has_read_table = has_table(conn, "hiolabs_user_ad_read")
        read_rows_before = None
        if has_read_table:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(1) AS total FROM hiolabs_user_ad_read WHERE user_id=%s",
                    (int(ctx.api_user_id),),
                )
                row = cur.fetchone() or {}
            read_rows_before = int(row.get("total") or 0)

        unread_before = request_json(session, ctx, "/api/ad/unreadCount", method="GET", token=token)
        expect_errno(unread_before, {0}, "ad unread before")
        before_count = int(((unread_before.get("data") or {}).get("count") or 0))

        messages = request_json(session, ctx, "/api/ad/messages", method="GET", token=token, params={"page": 1, "size": 20})
        expect_errno(messages, {0}, "ad messages")

        read_all = request_json(session, ctx, "/api/ad/readAll", method="POST", token=token, body={})
        expect_errno(read_all, {0}, "ad read all")

        unread_after = request_json(session, ctx, "/api/ad/unreadCount", method="GET", token=token)
        expect_errno(unread_after, {0}, "ad unread after")
        after_count = int(((unread_after.get("data") or {}).get("count") or 0))
        if after_count > before_count:
            raise AssertionError(f"ad unread count increased: before={before_count}, after={after_count}")

        evidence = f"before={before_count}, after={after_count}"
        if has_read_table:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(1) AS total FROM hiolabs_user_ad_read WHERE user_id=%s",
                    (int(ctx.api_user_id),),
                )
                row = cur.fetchone() or {}
            read_rows_after = int(row.get("total") or 0)
            if read_rows_before is not None and read_rows_after < read_rows_before:
                raise AssertionError(f"user_ad_read rows decreased unexpectedly: before={read_rows_before}, after={read_rows_after}")
            evidence += f", user_ad_read_before={read_rows_before}, user_ad_read_after={read_rows_after}"

        return CheckResult(
            id="L2-AD-MESSAGE-FLOW",
            name="Ad unread/messages/readAll consistency",
            layer="L2",
            status="passed",
            severity="P2",
            message=evidence,
            elapsed_seconds=time.time() - started,
            command="GET /api/ad/unreadCount + GET /api/ad/messages + POST /api/ad/readAll",
        )
    except Exception as err:
        return CheckResult(
            id="L2-AD-MESSAGE-FLOW",
            name="Ad unread/messages/readAll consistency",
            layer="L2",
            status="failed",
            severity="P2",
            message=str(err),
            elapsed_seconds=time.time() - started,
            command="GET /api/ad/unreadCount + GET /api/ad/messages + POST /api/ad/readAll",
        )


def run_search_footprint_flow(session: requests.Session, conn, ctx: Context, token: str) -> CheckResult:
    started = time.time()
    keyword = f"qa-search-{now_ts()}"
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO hiolabs_search_history (`keyword`, `from`, `add_time`, `user_id`) VALUES (%s, %s, %s, %s)",
                (keyword, "qa-suite", now_ts(), str(ctx.api_user_id)),
            )

        search_index = request_json(session, ctx, "/api/search/index", method="GET", token=token)
        expect_errno(search_index, {0}, "search index")
        history = (search_index.get("data") or {}).get("historyKeywordList") or []
        if keyword not in [str(x) for x in history]:
            raise AssertionError("search history missing inserted keyword")

        clear_history = request_json(session, ctx, "/api/search/clearHistory", method="GET", token=token)
        expect_errno(clear_history, {0}, "search clear history")
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(1) AS total FROM hiolabs_search_history WHERE user_id=%s",
                (str(ctx.api_user_id),),
            )
            row = cur.fetchone() or {}
        remain = int(row.get("total") or 0)
        if remain != 0:
            raise AssertionError(f"search history not cleared, remain={remain}")

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM hiolabs_goods WHERE is_delete=0 ORDER BY id ASC LIMIT 1"
            )
            goods = cur.fetchone() or {}
        goods_id = int(goods.get("id") or 0)
        if goods_id <= 0:
            raise AssertionError("no goods id found for footprint flow")

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO hiolabs_footprint (user_id, goods_id, add_time) VALUES (%s, %s, %s)",
                (int(ctx.api_user_id), goods_id, now_ts()),
            )
            footprint_id = int(cur.lastrowid)

        footprint_list = request_json(session, ctx, "/api/footprint/list", method="GET", token=token, params={"page": 1, "size": 20})
        expect_errno(footprint_list, {0}, "footprint list")
        list_data = (footprint_list.get("data") or {}).get("data") or []
        listed_ids = {int(item.get("id") or 0) for item in list_data if isinstance(item, dict)}
        if footprint_id not in listed_ids:
            raise AssertionError(f"new footprint id={footprint_id} not found in first page list")

        footprint_delete = request_json(
            session,
            ctx,
            "/api/footprint/delete",
            method="POST",
            token=token,
            body={"footprintId": footprint_id},
        )
        expect_errno(footprint_delete, {0}, "footprint delete")
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(1) AS total FROM hiolabs_footprint WHERE id=%s", (footprint_id,))
            row = cur.fetchone() or {}
        still_exists = int(row.get("total") or 0)
        if still_exists != 0:
            raise AssertionError(f"footprint {footprint_id} still exists after delete")

        return CheckResult(
            id="L2-SEARCH-FOOTPRINT",
            name="Search history and footprint create/list/delete consistency",
            layer="L2",
            status="passed",
            severity="P2",
            message=f"keyword={keyword}, footprint_id={footprint_id}",
            elapsed_seconds=time.time() - started,
            command="search index/clear + footprint list/delete",
        )
    except Exception as err:
        return CheckResult(
            id="L2-SEARCH-FOOTPRINT",
            name="Search history and footprint create/list/delete consistency",
            layer="L2",
            status="failed",
            severity="P2",
            message=str(err),
            elapsed_seconds=time.time() - started,
            command="search index/clear + footprint list/delete",
        )


def run_suite(ctx: Context) -> List[CheckResult]:
    if not ctx.api_jwt_secret:
        return [
            CheckResult(
                id="L2-DOMAIN-SUITE",
                name="Domain long-tail suite",
                layer="L2",
                status="failed",
                severity="P2",
                message="missing API_JWT_SECRET",
            )
        ]

    session = requests.Session()
    session.trust_env = False
    token = build_token(ctx.api_jwt_secret, ctx.api_user_id)
    conn = db_connect(ctx)
    try:
        return [
            run_invite_flow(session, conn, ctx, token),
            run_ad_flow(session, conn, ctx, token),
            run_search_footprint_flow(session, conn, ctx, token),
        ]
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run domain long-tail business suite (invite/ad/search/footprint)")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--api-jwt-secret", default="")
    parser.add_argument("--api-user-id", type=int, default=1048)
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="")
    parser.add_argument("--db-name", default="hiolabsDB")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    ctx = Context(
        base_url=args.base_url,
        api_jwt_secret=args.api_jwt_secret,
        api_user_id=args.api_user_id,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
    )
    results = run_suite(ctx)

    if args.output:
        out = Path(args.output)
        ensure_dir(out.parent)
        write_json(
            out,
            {
                "suite": "L2-domain-long-tail",
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
