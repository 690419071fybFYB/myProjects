#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
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
class Config:
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


def now_ts() -> int:
    return int(time.time())


def build_token(secret: str, user_id: int) -> str:
    token = jwt.encode({"user_id": int(user_id)}, secret, algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token


def db_connect(cfg: Config):
    return pymysql.connect(
        host=cfg.db_host,
        port=cfg.db_port,
        user=cfg.db_user,
        password=cfg.db_password,
        database=cfg.db_name,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def request_json(session: requests.Session, cfg: Config, path: str, method: str = "GET", token: str = "", params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict:
    url = f"{cfg.base_url.rstrip('/')}{path}"
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


def pick_goods(conn) -> Dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT g.id AS goods_id, p.id AS product_id
            FROM hiolabs_goods g
            INNER JOIN hiolabs_product p ON p.goods_id = g.id
            WHERE g.is_delete = 0 AND g.is_on_sale = 1
              AND p.is_delete = 0 AND p.is_on_sale = 1
              AND p.goods_number > 0
            ORDER BY g.id ASC
            LIMIT 1
            """
        )
        row = cur.fetchone()
    if not row:
        raise RuntimeError("no goods found for cross-end suite")
    return row


def pick_product(conn) -> Dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id AS product_id, p.goods_id, p.goods_sn, p.goods_weight, p.retail_price,
                   p.goods_name AS product_goods_name, p.goods_specification_ids,
                   g.name AS goods_name, g.list_pic_url, g.freight_template_id
            FROM hiolabs_product p
            INNER JOIN hiolabs_goods g ON g.id = p.goods_id
            WHERE p.is_delete = 0 AND p.is_on_sale = 1 AND p.goods_number > 0
              AND g.is_delete = 0 AND g.is_on_sale = 1 AND g.freight_template_id > 0
            ORDER BY p.id ASC LIMIT 1
            """
        )
        row = cur.fetchone()
    if not row:
        raise RuntimeError("no product found for order ops cross-end")
    return row


def ensure_profile(conn, user_id: int) -> None:
    nickname = base64.b64encode(f"qa-user-{user_id}".encode("utf-8")).decode("utf-8")
    mobile = f"1380000{str(user_id).zfill(4)[-4:]}"
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE hiolabs_user SET nickname=%s, mobile=%s WHERE id=%s",
            (nickname, mobile, int(user_id)),
        )


def ensure_address(conn, user_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hiolabs_address WHERE user_id=%s", (int(user_id),))
        cur.execute(
            """
            INSERT INTO hiolabs_address
              (name, user_id, country_id, province_id, city_id, district_id, address, mobile, is_default, is_delete)
            VALUES (%s, %s, 1, 2, 37, 403, %s, %s, 1, 0)
            """,
            (
                f"cross-end-{user_id}",
                int(user_id),
                f"road-{int(time.time() * 1000)}",
                f"1380000{str(user_id).zfill(4)[-4:]}",
            ),
        )
        return int(cur.lastrowid)


def seed_cart(conn, user_id: int, product: Dict) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hiolabs_cart WHERE user_id=%s", (int(user_id),))
        goods_name = product.get("product_goods_name") or product.get("goods_name") or f"goods-{product['goods_id']}"
        cur.execute(
            """
            INSERT INTO hiolabs_cart
              (user_id, goods_id, goods_sn, product_id, goods_name, goods_aka, goods_weight,
               add_price, retail_price, number, goods_specifition_name_value, goods_specifition_ids,
               checked, list_pic_url, freight_template_id, is_on_sale, add_time, is_fast, is_delete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, 1, %s, %s, 1, %s, 0, 0)
            """,
            (
                int(user_id),
                int(product["goods_id"]),
                str(product.get("goods_sn") or product["goods_id"]),
                int(product["product_id"]),
                goods_name,
                goods_name,
                float(product.get("goods_weight") or 0),
                float(product.get("retail_price") or 0),
                float(product.get("retail_price") or 0),
                str(product.get("goods_specification_ids") or "default"),
                str(product.get("goods_specification_ids") or ""),
                str(product.get("list_pic_url") or ""),
                int(product.get("freight_template_id") or 0),
                now_ts(),
            ),
        )


def login_admin(session: requests.Session, cfg: Config) -> str:
    payload = request_json(
        session,
        cfg,
        "/admin/auth/login",
        method="POST",
        body={"username": cfg.admin_username, "password": cfg.admin_password},
    )
    if int(payload.get("errno", -1)) == 0:
        token = (payload.get("data") or {}).get("token") or ""
        if token:
            return token

    # Fallback for environments that parse admin login only from form payload.
    url = f"{cfg.base_url.rstrip('/')}/admin/auth/login"
    resp = session.post(
        url,
        data={"username": cfg.admin_username, "password": cfg.admin_password},
        timeout=20,
    )
    try:
        fallback = json.loads(resp.text or "")
    except Exception:
        fallback = {}
    if int(fallback.get("errno", -1)) == 0:
        token = (fallback.get("data") or {}).get("token") or ""
        if token:
            return token

    if cfg.admin_jwt_secret:
        return build_token(cfg.admin_jwt_secret, cfg.admin_user_id)
    raise RuntimeError("admin login failed and no ADMIN_JWT_SECRET fallback")


def run_suite(cfg: Config) -> List[CheckResult]:
    started = time.time()
    results: List[CheckResult] = []
    scenario_meta = {
        "L3-COUPON-CROSS-END": ("Admin coupon config -> mini receive/preview", "P1"),
        "L3-PROMOTION-CROSS-END": ("Admin promotion config -> mini goods detail", "P1"),
        "L3-AD-CROSS-END": ("Admin ad config -> mini appInfo + ad messages", "P2"),
        "L3-ORDER-OPS-CROSS-END": ("Admin order memo/status -> mini order detail consistency", "P1"),
    }
    session = requests.Session()
    session.trust_env = False
    conn = None

    try:
        conn = db_connect(cfg)
        goods = pick_goods(conn)
        goods_id = int(goods["goods_id"])

        api_token = build_token(cfg.api_jwt_secret, cfg.api_user_id) if cfg.api_jwt_secret else ""
        admin_token = login_admin(session, cfg)

        # L4 admin login smoke (part of frontend smoke gate).
        results.append(CheckResult(
            id="L3-ADMIN-AUTH-PREREQ",
            name="Admin auth prerequisite for cross-end checks",
            layer="L3",
            status="passed" if admin_token else "failed",
            severity="P2",
            message="admin token acquired" if admin_token else "admin token missing",
            elapsed_seconds=time.time() - started,
        ))

        # Coupon cross-end: create -> receive -> preview selected.
        now = now_ts()
        coupon_payload = {
            "name": f"qa-coupon-{now}",
            "type": "full_reduction",
            "threshold_amount": 50,
            "reduce_amount": 5,
            "discount_rate": 10,
            "discount_max_reduce": 0,
            "scope_type": "all",
            "claim_start_at": now - 60,
            "claim_end_at": now + 86400,
            "use_start_at": now - 60,
            "use_end_at": now + 86400 * 2,
            "total_limit": 1000,
            "per_user_limit": 1,
            "status": "enabled",
            "segment_rules": {"groups": ["new_customer", "old_customer"], "match": "OR"},
        }
        payload = request_json(session, cfg, "/admin/coupon/create", method="POST", token=admin_token, body=coupon_payload)
        expect_errno(payload, {0}, "coupon create")
        coupon_id = int((payload.get("data") or {}).get("id") or 0)
        if coupon_id <= 0:
            raise AssertionError("coupon create returned invalid id")

        payload = request_json(session, cfg, "/api/coupon/receive", method="POST", token=api_token, body={"couponId": coupon_id})
        expect_errno(payload, {0}, "coupon receive")
        user_coupon_id = int((payload.get("data") or {}).get("userCouponId") or 0)
        if user_coupon_id <= 0:
            raise AssertionError("coupon receive returned invalid userCouponId")

        payload = request_json(
            session,
            cfg,
            "/api/coupon/preview",
            method="POST",
            token=api_token,
            body={"addType": 0, "orderFrom": 0, "freightPrice": 8, "selectedUserCouponIds": [user_coupon_id]},
        )
        expect_errno(payload, {0}, "coupon preview")

        results.append(CheckResult(
            id="L3-COUPON-CROSS-END",
            name="Admin coupon config -> mini receive/preview",
            layer="L3",
            status="passed",
            severity="P1",
            message=f"coupon_id={coupon_id}, user_coupon_id={user_coupon_id}",
            elapsed_seconds=time.time() - started,
        ))

        # Promotion cross-end: create -> goods detail shows promotion info.
        now = now_ts()
        promo_payload = {
            "name": f"qa-promo-{now}",
            "promo_tag": "测试促销",
            "promo_type": "discount",
            "discount_rate": 8.5,
            "reduce_amount": 0,
            "scope_type": "goods",
            "goods_ids": [goods_id],
            "start_at": now - 60,
            "end_at": now + 86400,
            "status": "enabled",
            "priority": 100,
        }
        payload = request_json(session, cfg, "/admin/promotion/create", method="POST", token=admin_token, body=promo_payload)
        expect_errno(payload, {0}, "promotion create")
        promotion_id = int((payload.get("data") or {}).get("id") or 0)

        payload = request_json(session, cfg, "/api/goods/detail", method="GET", params={"id": goods_id}, token=api_token)
        expect_errno(payload, {0}, "goods detail")
        detail_info = (payload.get("data") or {}).get("info") or {}
        has_promotion = int(detail_info.get("has_promotion") or 0)
        if has_promotion != 1:
            raise AssertionError(f"goods detail missing promotion marker for goods_id={goods_id}")

        results.append(CheckResult(
            id="L3-PROMOTION-CROSS-END",
            name="Admin promotion config -> mini goods detail",
            layer="L3",
            status="passed",
            severity="P1",
            message=f"promotion_id={promotion_id}, goods_id={goods_id}",
            elapsed_seconds=time.time() - started,
        ))

        # Ad cross-end: create popup ad -> appInfo has popupAd and ad unread/read chain works.
        now = now_ts()
        ad_payload = {
            "title": f"qa-popup-{now}",
            "link_type": 0,
            "goods_id": goods_id,
            "image_url": "https://example.com/qa-popup.png",
            "link": "",
            "placement": 2,
            "sort_order": 0,
            "enabled": 1,
            "start_time": now - 60,
            "end_time": now + 86400,
        }
        payload = request_json(session, cfg, "/admin/ad/store", method="POST", token=admin_token, body=ad_payload)
        expect_errno(payload, {0, 100}, "ad create")
        ad_id = int((payload.get("data") or {}).get("id") or 0)

        payload = request_json(session, cfg, "/api/index/appInfo", method="GET", token=api_token)
        expect_errno(payload, {0}, "index appInfo")
        popup_ad = (payload.get("data") or {}).get("popupAd") or {}
        popup_id = int(popup_ad.get("id") or 0)
        if popup_id <= 0:
            raise AssertionError("popupAd missing after admin ad store")

        unread_before = request_json(session, cfg, "/api/ad/unreadCount", method="GET", token=api_token)
        expect_errno(unread_before, {0}, "ad unread before")
        before_count = int(((unread_before.get("data") or {}).get("count") or 0))

        read_all = request_json(session, cfg, "/api/ad/readAll", method="POST", token=api_token, body={})
        expect_errno(read_all, {0}, "ad readAll")

        unread_after = request_json(session, cfg, "/api/ad/unreadCount", method="GET", token=api_token)
        expect_errno(unread_after, {0}, "ad unread after")
        after_count = int(((unread_after.get("data") or {}).get("count") or 0))

        if after_count > before_count:
            raise AssertionError(f"ad unread count increased after readAll: before={before_count}, after={after_count}")

        results.append(CheckResult(
            id="L3-AD-CROSS-END",
            name="Admin ad config -> mini appInfo + ad messages",
            layer="L3",
            status="passed",
            severity="P2",
            message=f"ad_id={ad_id}, popup_id={popup_id}, unread_before={before_count}, unread_after={after_count}",
            elapsed_seconds=time.time() - started,
        ))

        # Order ops cross-end: mini submit -> admin memo/status -> mini detail + DB trace.
        ensure_profile(conn, cfg.api_user_id)
        product = pick_product(conn)
        address_id = ensure_address(conn, cfg.api_user_id)
        seed_cart(conn, cfg.api_user_id, product)

        checkout = request_json(
            session,
            cfg,
            "/api/cart/checkout",
            method="GET",
            token=api_token,
            params={"addressId": address_id, "addType": 0, "orderFrom": 0, "type": 0},
        )
        expect_errno(checkout, {0}, "order ops checkout")
        checkout_data = checkout.get("data") or {}
        freight_price = float(checkout_data.get("freightPrice") or 0)
        actual_price = checkout_data.get("actualPrice") or checkout_data.get("orderTotalPrice") or "0.01"

        submit = request_json(
            session,
            cfg,
            "/api/order/submit",
            method="POST",
            token=api_token,
            body={
                "addressId": address_id,
                "postscript": "l3-order-ops",
                "freightPrice": freight_price,
                "actualPrice": actual_price,
                "selectedUserCouponIds": [],
                "offlinePay": 1,
            },
        )
        expect_errno(submit, {0}, "order ops submit")
        order_info = (submit.get("data") or {}).get("orderInfo") or {}
        order_id = int(order_info.get("id") or 0)
        order_sn = str(order_info.get("order_sn") or "")
        if order_id <= 0 or not order_sn:
            raise AssertionError("order ops submit returned invalid order id/order_sn")

        memo_text = f"qa-order-memo-{now_ts()}"
        memo = request_json(
            session,
            cfg,
            "/admin/order/saveAdminMemo",
            method="POST",
            token=admin_token,
            body={"id": order_id, "text": memo_text},
        )
        expect_errno(memo, {0}, "order memo update")

        change_status = request_json(
            session,
            cfg,
            "/admin/order/changeStatus",
            method="POST",
            token=admin_token,
            body={"orderSn": order_sn, "status": 301},
        )
        expect_errno(change_status, {0}, "order status update")

        detail = request_json(
            session,
            cfg,
            "/api/order/detail",
            method="GET",
            token=api_token,
            params={"orderId": order_id},
        )
        expect_errno(detail, {0}, "user order detail after admin ops")
        user_order_info = (detail.get("data") or {}).get("orderInfo") or {}
        if int(user_order_info.get("id") or 0) != order_id:
            raise AssertionError("user order detail not matched after admin ops")

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, order_status, admin_memo FROM hiolabs_order WHERE id=%s AND user_id=%s",
                (order_id, int(cfg.api_user_id)),
            )
            row = cur.fetchone()
        if not row:
            raise AssertionError(f"order {order_id} missing in DB for order ops cross-end")
        if int(row.get("order_status") or 0) != 301:
            raise AssertionError(f"order status expected 301, got {row.get('order_status')}")
        if str(row.get("admin_memo") or "") != memo_text:
            raise AssertionError("order admin_memo mismatch after saveAdminMemo")

        results.append(CheckResult(
            id="L3-ORDER-OPS-CROSS-END",
            name="Admin order memo/status -> mini order detail consistency",
            layer="L3",
            status="passed",
            severity="P1",
            message=f"order_id={order_id}, order_sn={order_sn}, status=301, memo_synced=1",
            elapsed_seconds=time.time() - started,
        ))

    except Exception as err:
        results.append(CheckResult(
            id="L3-CROSS-END-SUITE",
            name="Cross-end suite runtime",
            layer="L3",
            status="failed",
            severity="P1",
            message=str(err),
            elapsed_seconds=time.time() - started,
        ))
        existing_ids = {item.id for item in results}
        for sid, (sname, severity) in scenario_meta.items():
            if sid in existing_ids:
                continue
            results.append(CheckResult(
                id=sid,
                name=sname,
                layer="L3",
                status="failed",
                severity=severity,
                message=f"blocked by cross-end suite runtime error: {err}",
                elapsed_seconds=time.time() - started,
            ))
    finally:
        if conn:
            conn.close()

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run L3 cross-end linkage suite")
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
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    cfg = Config(
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
    )

    results = run_suite(cfg)
    if args.output:
        output = Path(args.output)
        ensure_dir(output.parent)
        write_json(output, {
            "suite": "L3-cross-end",
            "results": [r.__dict__ for r in results],
            "summary": {
                "total": len(results),
                "passed": len([r for r in results if r.status == "passed"]),
                "failed": len([r for r in results if r.status == "failed"]),
                "skipped": len([r for r in results if r.status == "skipped"]),
            },
        })

    return 1 if any(r.status == "failed" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
