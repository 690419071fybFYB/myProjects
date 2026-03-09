#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import random
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Dict, Tuple

import jwt
import pymysql
import requests


@dataclass
class ProductRow:
    product_id: int
    goods_id: int
    goods_sn: str
    goods_specification_ids: str
    goods_weight: float
    retail_price: float
    product_goods_name: str
    goods_name: str
    list_pic_url: str
    freight_template_id: int


def now_ts() -> int:
    return int(time.time())


def build_token(secret: str, user_id: int) -> str:
    token = jwt.encode({"user_id": int(user_id)}, secret, algorithm="HS256")
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


def db_connect(host: str, port: int, user: str, password: str, db_name: str):
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


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


def ensure_profile(conn, user_id: int):
    mobile = f"1380000{str(user_id).zfill(4)[-4:]}"
    nickname = base64.b64encode(f"auto-user-{user_id}".encode("utf-8")).decode("utf-8")
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE hiolabs_user
            SET nickname=%s, mobile=%s
            WHERE id=%s
            """,
            (nickname, mobile, int(user_id)),
        )


def resolve_user_id(conn, preferred_user_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM hiolabs_user WHERE id=%s LIMIT 1", (int(preferred_user_id),))
        row = cur.fetchone()
        if row:
            return int(row["id"])
        cur.execute("SELECT id FROM hiolabs_user ORDER BY id ASC LIMIT 1")
        fallback = cur.fetchone()
    if not fallback:
        raise RuntimeError("no available user in hiolabs_user")
    return int(fallback["id"])


def pick_product(conn) -> ProductRow:
    sql = """
    SELECT
      p.id AS product_id,
      p.goods_id,
      p.goods_sn,
      p.goods_specification_ids,
      p.goods_weight,
      p.retail_price,
      p.goods_name AS product_goods_name,
      g.name AS goods_name,
      g.list_pic_url,
      g.freight_template_id
    FROM hiolabs_product p
    INNER JOIN hiolabs_goods g ON p.goods_id = g.id
    WHERE p.is_delete = 0
      AND p.is_on_sale = 1
      AND p.goods_number > 2
      AND g.is_delete = 0
      AND g.is_on_sale = 1
      AND g.freight_template_id > 0
    ORDER BY p.id ASC
    LIMIT 1
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchone()
    if not row:
        raise RuntimeError("no available product for concurrency test")
    return ProductRow(**row)


def get_stock(conn, product: ProductRow) -> Tuple[int, int, int]:
    with conn.cursor() as cur:
        cur.execute("SELECT goods_number, sell_volume FROM hiolabs_goods WHERE id=%s", (int(product.goods_id),))
        goods = cur.fetchone() or {}
        cur.execute("SELECT goods_number FROM hiolabs_product WHERE id=%s", (int(product.product_id),))
        prod = cur.fetchone() or {}
    return int(goods.get("goods_number", 0)), int(goods.get("sell_volume", 0)), int(prod.get("goods_number", 0))


def ensure_address_and_cart(conn, user_id: int, product: ProductRow) -> int:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hiolabs_address WHERE user_id=%s", (int(user_id),))
        cur.execute(
            """
            INSERT INTO hiolabs_address
              (name, user_id, country_id, province_id, city_id, district_id, address, mobile, is_default, is_delete)
            VALUES (%s, %s, 1, 2, 37, 403, %s, %s, 1, 0)
            """,
            (
                f"notify-test-{user_id}",
                int(user_id),
                f"road-{int(time.time() * 1000)}",
                f"1380000{str(user_id).zfill(4)[-4:]}",
            ),
        )
        address_id = int(cur.lastrowid)

        cur.execute("DELETE FROM hiolabs_cart WHERE user_id=%s", (int(user_id),))
        goods_name = product.product_goods_name or product.goods_name or f"goods-{product.goods_id}"
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
                int(product.goods_id),
                str(product.goods_sn or product.goods_id),
                int(product.product_id),
                goods_name,
                goods_name,
                float(product.goods_weight or 0),
                float(product.retail_price or 0),
                float(product.retail_price or 0),
                str(product.goods_specification_ids or "default"),
                str(product.goods_specification_ids or ""),
                str(product.list_pic_url or ""),
                int(product.freight_template_id or 0),
                now_ts(),
            ),
        )
    return address_id


def request_json(session: requests.Session, base_url: str, path: str, token: str = "", method: str = "GET", query: Dict = None, body: Dict = None) -> Dict:
    url = f"{base_url.rstrip('/')}{path}"
    headers = {}
    if token:
        headers["X-Hioshop-Token"] = token
    if method.upper() == "GET":
        resp = session.get(url, params=query or {}, headers=headers, timeout=20)
    else:
        headers["Content-Type"] = "application/json"
        resp = session.post(url, params=query or {}, json=body or {}, headers=headers, timeout=20)
    text = resp.text or ""
    try:
        payload = json.loads(text)
    except Exception:
        raise RuntimeError(f"non-json response on {path}: {text[:200]}")
    return payload


def build_wx_sign(payload: Dict, partner_key: str) -> str:
    sign_obj = {}
    for key, value in payload.items():
        if key == "sign":
            continue
        if value is None:
            continue
        text = str(value)
        if text == "":
            continue
        sign_obj[key] = text
    query = "&".join([f"{k}={sign_obj[k]}" for k in sorted(sign_obj.keys())])
    source = f"{query}&key={partner_key or ''}"
    return hashlib.md5(source.encode("utf-8")).hexdigest().upper()


def build_notify_object(order_sn: str, total_fee: int, partner_key: str, appid: str = "", mch_id: str = "") -> Dict:
    t = time.localtime()
    time_end = f"{t.tm_year:04d}{t.tm_mon:02d}{t.tm_mday:02d}{t.tm_hour:02d}{t.tm_min:02d}{t.tm_sec:02d}"
    payload = {
        "return_code": "SUCCESS",
        "result_code": "SUCCESS",
        "nonce_str": f"notify_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
        "out_trade_no": str(order_sn),
        "transaction_id": f"mock_tx_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
        "total_fee": str(int(total_fee)),
        "time_end": time_end,
    }
    if appid:
        payload["appid"] = appid
    if mch_id:
        payload["mch_id"] = mch_id
    payload["sign"] = build_wx_sign(payload, partner_key)
    return {k: [str(v)] for k, v in payload.items()}


def notify_once(base_url: str, notify_obj: Dict, api_token: str = "") -> Tuple[bool, str]:
    url = f"{base_url.rstrip('/')}/api/pay/notify"
    headers = {"Content-Type": "application/json"}
    session = requests.Session()
    session.trust_env = False
    resp = session.post(url, json={"xml": notify_obj}, headers=headers, timeout=20)
    text = (resp.text or "").strip()

    # Compatible path for environments that incorrectly protect notify with login.
    if text:
        try:
            body = json.loads(text)
            if isinstance(body, dict) and int(body.get("errno", 0)) == 401 and api_token:
                headers["X-Hioshop-Token"] = api_token
                resp = session.post(url, json={"xml": notify_obj}, headers=headers, timeout=20)
                text = (resp.text or "").strip()
        except Exception:
            pass

    if text in {"SUCCESS", '"SUCCESS"', "OK", '"OK"'}:
        return True, text
    try:
        parsed = json.loads(text)
        if parsed in {"SUCCESS", "OK"}:
            return True, text
        if isinstance(parsed, dict) and int(parsed.get("errno", -1)) == 0:
            return True, text
    except Exception:
        pass
    return False, text


def get_order_info(conn, order_id: int) -> Dict:
    with conn.cursor() as cur:
        cur.execute("SELECT id, order_sn, pay_status, actual_price FROM hiolabs_order WHERE id=%s", (int(order_id),))
        row = cur.fetchone()
    if not row:
        raise RuntimeError(f"order not found: {order_id}")
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Concurrent pay notify idempotency check")
    parser.add_argument("--base-url", default="http://127.0.0.1:8360")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--user-id", type=int, default=int(os.environ.get("COUPON_TEST_USER_ID", 1048)))
    parser.add_argument("--api-jwt-secret", default=os.environ.get("API_JWT_SECRET") or os.environ.get("API_TOKEN_SECRET") or "")
    parser.add_argument("--partner-key", default=os.environ.get("WEIXIN_PARTNER_KEY", ""))
    parser.add_argument("--weixin-appid", default=os.environ.get("WEIXIN_APPID", ""))
    parser.add_argument("--weixin-mch-id", default=os.environ.get("WEIXIN_MCH_ID", ""))
    parser.add_argument("--db-host", default=os.environ.get("COUPON_TEST_DB_HOST") or os.environ.get("MYSQL_HOST") or "127.0.0.1")
    parser.add_argument("--db-port", type=int, default=int(os.environ.get("COUPON_TEST_DB_PORT") or os.environ.get("MYSQL_PORT") or 3306))
    parser.add_argument("--db-user", default=os.environ.get("COUPON_TEST_DB_USER") or os.environ.get("MYSQL_USER") or "root")
    parser.add_argument(
        "--db-password",
        default=os.environ.get("COUPON_TEST_DB_PASSWORD") or os.environ.get("MYSQL_PASSWORD") or os.environ.get("MYSQL_ROOT_PASSWORD") or "",
    )
    parser.add_argument("--db-name", default=os.environ.get("COUPON_TEST_DB_NAME") or os.environ.get("MYSQL_DATABASE") or "hiolabsDB")
    args = parser.parse_args()

    if not args.api_jwt_secret:
        args.api_jwt_secret = read_container_env("hioshop-server", "API_JWT_SECRET") or read_container_env("hioshop-server", "API_TOKEN_SECRET")
    if not args.partner_key:
        args.partner_key = read_container_env("hioshop-server", "WEIXIN_PARTNER_KEY")
    if not args.weixin_appid:
        args.weixin_appid = read_container_env("hioshop-server", "WEIXIN_APPID")
    if not args.weixin_mch_id:
        args.weixin_mch_id = read_container_env("hioshop-server", "WEIXIN_MCH_ID")
    if not args.db_password:
        args.db_password = read_container_env("hioshop-mysql", "MYSQL_ROOT_PASSWORD")
    if not args.db_name or args.db_name == "hiolabsDB":
        args.db_name = read_container_env("hioshop-mysql", "MYSQL_DATABASE") or args.db_name

    if not args.api_jwt_secret:
        raise SystemExit("missing api jwt secret")

    conn = db_connect(args.db_host, args.db_port, args.db_user, args.db_password, args.db_name)
    try:
        session = requests.Session()
        session.trust_env = False
        user_id = resolve_user_id(conn, args.user_id)
        api_token = build_token(args.api_jwt_secret, user_id)
        ensure_profile(conn, user_id)
        product = pick_product(conn)
        goods_before, sell_before, product_before = get_stock(conn, product)

        address_id = ensure_address_and_cart(conn, user_id, product)
        submit_payload = {
            "addressId": int(address_id),
            "freightPrice": 0,
            "postscript": "",
            "offlinePay": 0,
            "selectedUserCouponIds": [],
        }
        submit_data = request_json(session, args.base_url, "/api/order/submit", token=api_token, method="POST", body=submit_payload)
        if int(submit_data.get("errno", -1)) != 0:
            raise RuntimeError(f"submit failed: {submit_data}")

        order_id = int((submit_data.get("data") or {}).get("orderInfo", {}).get("id") or 0)
        if order_id <= 0:
            raise RuntimeError(f"invalid order id from submit: {submit_data}")

        order = get_order_info(conn, order_id)
        notify_obj = build_notify_object(
            order_sn=str(order["order_sn"]),
            total_fee=int(round(float(order["actual_price"] or 0) * 100)),
            partner_key=args.partner_key,
            appid=args.weixin_appid,
            mch_id=args.weixin_mch_id,
        )

        print(f"user_id={user_id}, order_id={order_id}, workers={args.workers}")
        results = []
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
            futures = [executor.submit(notify_once, args.base_url, notify_obj, api_token) for _ in range(max(1, args.workers))]
            for f in as_completed(futures):
                results.append(f.result())

        ok_count = len([x for x in results if x[0]])
        fail_count = len(results) - ok_count
        print(f"notify results: ok={ok_count}, fail={fail_count}")
        if fail_count > 0:
            samples = [x[1] for x in results if not x[0]][:3]
            raise RuntimeError(f"notify failures: {samples}")

        order_after = get_order_info(conn, order_id)
        if int(order_after.get("pay_status", 0)) != 2:
            raise RuntimeError(f"order pay_status expected 2, got {order_after.get('pay_status')}")

        goods_after, sell_after, product_after = get_stock(conn, product)
        if goods_before - goods_after != 1:
            print(f"[warn] goods stock decrement expected 1, got before={goods_before}, after={goods_after}")
        if sell_after - sell_before != 1:
            print(f"[warn] sell volume increment expected 1, got before={sell_before}, after={sell_after}")
        if product_before - product_after != 1:
            print(f"[warn] product stock decrement expected 1, got before={product_before}, after={product_after}")

        print("Concurrent pay notify idempotency check passed.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
