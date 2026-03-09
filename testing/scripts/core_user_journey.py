#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import time
from dataclasses import dataclass
from typing import Dict, Optional

import jwt
import pymysql
import requests


@dataclass
class Context:
    base_url: str
    api_secret: str
    user_id: int
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


def request_json(session: requests.Session, ctx: Context, path: str, method: str = "GET", token: str = "", params: Optional[Dict] = None, body: Optional[Dict] = None) -> Dict:
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
        raise RuntimeError(f"{path} non-json response: {text[:200]}") from err
    payload["_status"] = resp.status_code
    return payload


def assert_errno(payload: Dict, allowed, label: str) -> None:
    errno = int(payload.get("errno", -99999))
    if errno not in set(int(x) for x in allowed):
        raise AssertionError(f"{label} unexpected errno={errno}, status={payload.get('_status')}, errmsg={payload.get('errmsg')}")


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
        raise RuntimeError("no available product for user journey")
    return row


def ensure_profile(conn, user_id: int, complete: bool) -> None:
    if complete:
        nickname = base64.b64encode(f"qa-user-{user_id}".encode("utf-8")).decode("utf-8")
        mobile = f"1380000{str(user_id).zfill(4)[-4:]}"
    else:
        nickname = base64.b64encode("微信用户".encode("utf-8")).decode("utf-8")
        mobile = ""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM hiolabs_user WHERE id=%s LIMIT 1", (int(user_id),))
        exists = cur.fetchone()
        if not exists:
            # Ensure deterministic test identity exists before profile gate checks.
            cur.execute(
                """
                INSERT INTO hiolabs_user
                  (id, nickname, name, username, password, mobile, register_time, last_login_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(user_id),
                    nickname,
                    f"qa-user-{user_id}",
                    f"qa-user-{user_id}",
                    "",
                    mobile,
                    now_ts(),
                    now_ts(),
                ),
            )
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
                f"journey-{user_id}",
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


def assert_order_exists(conn, order_id: int, user_id: int) -> Dict:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, user_id, order_status, offline_pay, actual_price, pay_status FROM hiolabs_order WHERE id=%s AND user_id=%s",
            (int(order_id), int(user_id)),
        )
        row = cur.fetchone()
    if not row:
        raise AssertionError(f"order {order_id} not found")
    return row


def run(ctx: Context) -> None:
    if not ctx.api_secret:
        raise RuntimeError("missing API_JWT_SECRET for core user journey")

    token = build_token(ctx.api_secret, ctx.user_id)
    session = requests.Session()
    session.trust_env = False

    conn = db_connect(ctx)
    try:
        product = pick_product(conn)

        # 1) Unauthorized contract: order list should reject when no token.
        payload = request_json(session, ctx, "/api/order/list", method="GET", params={"page": 1, "size": 1, "showType": 0})
        assert_errno(payload, {401}, "order list unauthorized")

        # 2) Profile incomplete should hit 412 on checkout.
        ensure_profile(conn, ctx.user_id, complete=False)
        payload = request_json(session, ctx, "/api/cart/checkout", method="GET", token=token, params={"addressId": 0, "addType": 0, "orderFrom": 0, "type": 0})
        assert_errno(payload, {412}, "profile gate")

        # 3) Restore profile and prepare address/cart.
        ensure_profile(conn, ctx.user_id, complete=True)
        address_id = ensure_address(conn, ctx.user_id)
        seed_cart(conn, ctx.user_id, product)

        payload = request_json(session, ctx, "/api/cart/index", method="GET", token=token)
        assert_errno(payload, {0}, "cart index")

        payload = request_json(
            session,
            ctx,
            "/api/cart/checkout",
            method="GET",
            token=token,
            params={"addressId": address_id, "addType": 0, "orderFrom": 0, "type": 0},
        )
        assert_errno(payload, {0}, "checkout")
        data = payload.get("data") or {}
        freight_price = float(data.get("freightPrice") or 0)

        # 4) Submit offline order and verify DB.
        payload = request_json(
            session,
            ctx,
            "/api/order/submit",
            method="POST",
            token=token,
            body={
                "addressId": address_id,
                "postscript": "core-journey",
                "freightPrice": freight_price,
                "actualPrice": data.get("actualPrice") or data.get("orderTotalPrice") or "0.01",
                "selectedUserCouponIds": [],
                "offlinePay": 1,
            },
        )
        assert_errno(payload, {0}, "submit offline order")
        order_id = int((payload.get("data") or {}).get("orderInfo", {}).get("id") or 0)
        if order_id <= 0:
            raise AssertionError("submit order returned invalid id")

        order_row = assert_order_exists(conn, order_id, ctx.user_id)
        if int(order_row.get("offline_pay") or 0) != 1:
            raise AssertionError(f"order {order_id} offline_pay expected 1")

        # 5) Cancel order path.
        payload = request_json(session, ctx, "/api/order/cancel", method="POST", token=token, body={"orderId": order_id})
        assert_errno(payload, {0, 1000}, "cancel order")

        # 6) Additional domain smoke endpoints.
        payload = request_json(session, ctx, "/api/coupon/center", method="GET", token=token)
        assert_errno(payload, {0, 401}, "coupon center")

        payload = request_json(session, ctx, "/api/invite/mySummary", method="GET", token=token)
        assert_errno(payload, {0, 401}, "invite summary")

        payload = request_json(session, ctx, "/api/ad/unreadCount", method="GET", token=token)
        assert_errno(payload, {0, 401}, "ad unread count")

        payload = request_json(session, ctx, "/api/search/index", method="GET")
        assert_errno(payload, {0}, "search index")

        payload = request_json(session, ctx, "/api/footprint/list", method="GET", token=token, params={"page": 1, "size": 5})
        assert_errno(payload, {0, 401, 412}, "footprint list")

    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Core user journey business-chain smoke with DB assertions")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--api-jwt-secret", default="")
    parser.add_argument("--api-user-id", type=int, default=1048)
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="")
    parser.add_argument("--db-name", default="hiolabsDB")
    args = parser.parse_args()

    ctx = Context(
        base_url=args.base_url,
        api_secret=args.api_jwt_secret,
        user_id=args.api_user_id,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
    )

    try:
        run(ctx)
        print("core user journey passed")
        return 0
    except Exception as err:
        print(f"core user journey failed: {err}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
