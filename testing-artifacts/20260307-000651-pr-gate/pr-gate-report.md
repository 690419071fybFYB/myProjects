# Hioshop PR Gate

- mode: `pr-gate`
- started_at: `2026-03-07T00:06:51+08:00`
- finished_at: `2026-03-07T00:06:53+08:00`
- summary: `passed=2`, `failed=20`, `skipped=4`, `total=26`

## Layer Summary

| layer | passed | failed | skipped | total |
|---|---:|---:|---:|---:|
| L1 | 0 | 8 | 0 | 8 |
| L2 | 0 | 10 | 0 | 10 |
| L3 | 0 | 1 | 3 | 4 |
| L4 | 2 | 1 | 1 | 4 |

## Results

| id | layer | status | severity | message |
|---|---|---|---|---|
| L2-ADDRESS-FLOW | L2 | failed | P0 | return self._jws.encode( |
| L2-CART-FLOW | L2 | failed | P0 | return self._jws.encode( |
| L2-CHECKOUT-FLOW | L2 | failed | P0 | return self._jws.encode( |
| L2-COUPON-LIFECYCLE | L2 | failed | P0 | Coupon 自动化测试失败: Access denied for user 'root'@'172.18.0.1' (using password: YES) |
| L2-GOODS-FLOW | L2 | failed | P0 | return self._jws.encode( |
| L2-LOGIN-GATE | L2 | failed | P0 | return self._jws.encode( |
| L2-ORDER-LIFECYCLE | L2 | failed | P0 | return self._jws.encode( |
| L2-PAY-FLOW | L2 | failed | P0 | pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'172.18.0.1' (using password: YES)") |
| L2-PROMOTION-LIFECYCLE | L2 | failed | P0 | Promotion V1 mock 联调验证失败: service.previewCartPromotions is not a function |
| L2-SUBMIT-FLOW | L2 | failed | P0 | return self._jws.encode( |
| L1-CORE-ADDRESS | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/address/getAddresses (Caused by NewConnectionError("HTTPConnection(host='127.0.0... |
| L1-CORE-AUTH | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/auth/loginByWeixin (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1... |
| L1-CORE-CART | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/cart/index?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='127... |
| L1-CORE-COUPON | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/coupon/center?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='... |
| L1-CORE-ORDER | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/order/list?page=1&size=1&showType=0 (Caused by NewConnectionError("HTTPConnectio... |
| L1-CORE-PAY | L1 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/pay/notify (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=... |
| L3-CROSS-END-SUITE | L3 | failed | P1 | (1045, "Access denied for user 'root'@'172.18.0.1' (using password: YES)") |
| L4-ADMIN-LOGIN-SMOKE | L4 | failed | P1 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /admin/auth/login (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', por... |
| L3-COUPON-CROSS-END | L3 | skipped | P1 | Scenario is defined in matrix but not yet automated in this mode |
| L3-PROMOTION-CROSS-END | L3 | skipped | P1 | Scenario is defined in matrix but not yet automated in this mode |
| L4-MINI-REQUEST-SMOKE | L4 | passed | P1 | 401/412/network handling smoke passed |
| NIGHTLY-COS-REAL-SMOKE | L4 | skipped | P1 | missing env: COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET |
| L1-CORE-AD | L1 | failed | P2 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/ad/messages?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='12... |
| L1-CORE-SETTINGS | L1 | failed | P2 | request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/settings/showSettings (Caused by NewConnectionError("HTTPConnection(host='127.0.... |
| L3-AD-CROSS-END | L3 | skipped | P2 | Scenario is defined in matrix but not yet automated in this mode |
| L4-MINI-SYNTAX-SMOKE | L4 | passed | P2 | syntax checks passed |

## Failures

- `L2-ADDRESS-FLOW` [P0] Address create/default/use flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-CART-FLOW` [P0] Cart select/update/delete/count flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-CHECKOUT-FLOW` [P0] Checkout freight/promotion/coupon flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-COUPON-LIFECYCLE` [P0] Coupon receive/preview/lock/use/release flow: Coupon 自动化测试失败: Access denied for user 'root'@'172.18.0.1' (using password: YES)
  - command: `node scripts/test-coupon.js`
  - evidence: `Coupon 自动化测试失败: Access denied for user 'root'@'172.18.0.1' (using password: YES)`
- `L2-GOODS-FLOW` [P0] Goods detail/spec/add-cart/buy-now flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-LOGIN-GATE` [P0] Login gate and profile completeness checks: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-ORDER-LIFECYCLE` [P0] Order lifecycle cancel/status flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L2-PAY-FLOW` [P0] Pay notify and idempotency flow: pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'172.18.0.1' (using password: YES)")
  - command: `python3 testing/scripts/pay_notify_concurrency.py --base-url http://127.0.0.1:1 --workers 1 --user-id 1 --api-jwt-secret ci_api --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `Traceback (most recent call last):
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 383, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 315, in main
    conn = db_connect(args.db_host, args.db_port, args.db_user, args.db_password, args.db_name)
  File "/Volumes/SAMSUNG/fyb/myProjects/testing/scripts/pay_notify_concurrency.py", line 45, in db_conne`
- `L2-PROMOTION-LIFECYCLE` [P0] Promotion and best-price flow: Promotion V1 mock 联调验证失败: service.previewCartPromotions is not a function
  - command: `node scripts/test-promotion-v1.js`
  - evidence: `Promotion V1 mock 联调验证失败: service.previewCartPromotions is not a function`
- `L2-SUBMIT-FLOW` [P0] Submit order and anti-tamper flow: return self._jws.encode(
  - command: `python3 testing/scripts/core_user_journey.py --base-url http://127.0.0.1:1 --api-jwt-secret ci_api --api-user-id 1 --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password root --db-name hiolabsDB`
  - evidence: `/Volumes/SAMSUNG/fyb/.global_env/lib/python3.13/site-packages/jwt/api_jwt.py:153: InsecureKeyLengthWarning: The HMAC key is 6 bytes long, which is below the minimum recommended length of 32 bytes for SHA256. See RFC 7518 Section 3.2.
  return self._jws.encode(`
- `L1-CORE-ADDRESS` [P1] Address core contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/address/getAddresses (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/address/getAddresses`
- `L1-CORE-AUTH` [P1] Auth loginByWeixin contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/auth/loginByWeixin (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `POST /api/auth/loginByWeixin`
- `L1-CORE-CART` [P1] Cart core contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/cart/index?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/cart/index`
- `L1-CORE-COUPON` [P1] Coupon core contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/coupon/center?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/coupon/center`
- `L1-CORE-ORDER` [P1] Order core contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/order/list?page=1&size=1&showType=0 (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/order/list`
- `L1-CORE-PAY` [P1] Pay core contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/pay/notify (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `POST /api/pay/notify`
- `L3-CROSS-END-SUITE` [P1] Cross-end suite runtime: (1045, "Access denied for user 'root'@'172.18.0.1' (using password: YES)")
- `L4-ADMIN-LOGIN-SMOKE` [P1] Admin login smoke: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /admin/auth/login (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `POST /admin/auth/login`
- `L1-CORE-AD` [P2] Ad message contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/ad/messages?page=1&size=1 (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/ad/messages`
- `L1-CORE-SETTINGS` [P2] Settings contract: request error: HTTPConnectionPool(host='127.0.0.1', port=1): Max retries exceeded with url: /api/settings/showSettings (Caused by NewConnectionError("HTTPConnection(host='127.0.0.1', port=1): Failed to establish a new connection: [Errno 61] Connection refused"))
  - command: `GET /api/settings/showSettings`
