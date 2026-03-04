# Findings-HighRisk (P0/P1)

审查时间：2026-03-04（Asia/Shanghai）  
审查基线：
- workspace commit: `933b39b05623e24fa7a99efd0bf907af46767d36`
- `hioshop-miniprogram`: `master@fd676c0d28ae8c7acbfcf437e0195356be465181`（含未提交改动）
- `hioshop-server`: `master@98fcffd047f96546796e31d98d63769f44e4b9e7`（含未提交改动）
- `hioshop-admin-web`: `main@92ff44c2b2372b68acf0014a372fc525034e3618`

## Finding 1
- id: `HR-001`
- priority: `P0`
- repo: `hioshop-server`
- file: `src/api/controller/order.js; src/api/model/order.js`
- line: `257-265, 271-287, 293-304, 454-481, 487-531; model 38-48`
- title: `订单关键写操作未按 user_id 做归属校验（IDOR）`
- impact: `攻击者只要知道/猜到 orderId，可跨账号执行删除、确认收货、完成、改地址、查物流，导致订单状态篡改和隐私泄露。`
- evidence: `order.js 中 delete/confirm/complete/update/express 仅按 id 或 order_id 更新/查询；order model 的 getOrderHandleOption 仅按 id 取单，未传 user_id。`
- repro_steps:
  1. `POST /api/order/confirm` 传入任意 `orderId`（无需 token）
  2. 观察返回并非统一 401，而是进入业务分支（本次对假 id 返回“订单不能确认”）
  3. 对真实存在且状态可操作的 orderId 将触发跨账号状态变更
- fix_recommendation: `所有订单写操作统一 where 条件追加 user_id=this.getLoginUserId()；getOrderHandleOption 改为 getOrderHandleOption(orderId, userId) 并强制校验；不存在/无权统一返回 404/403。`
- regression_tests:
  1. `A 用户 token + B 用户 orderId` 调用删除/确认/改地址必须失败
  2. `A 用户 token + A 用户 orderId` 在合法状态应成功
  3. `expressAction` 对非本人订单必须拒绝
- confidence: `0.98`

## Finding 2
- id: `HR-002`
- priority: `P0`
- repo: `hioshop-server`
- file: `src/api/controller/pay.js`
- line: `11-27`
- title: `测试支付接口 preWeixinPaya 暴露在生产路由，且可直接推进支付状态`
- impact: `可绕过真实支付回调，直接执行 updatePayData/consumeCoupons/afterPay，造成订单和优惠券资产异常。`
- evidence: `preWeixinPayaAction 直接构造 transaction_id/time_end 并调用 orderModel.updatePayData + couponService.consumeCouponsForOrder + afterPay，无鉴权/归属校验。`
- repro_steps:
  1. 访问 `GET /api/pay/preWeixinPaya?orderId=<id>`
  2. 观察该 action 在生产 API 可达（本次用假 id 返回 500，但路径已暴露）
  3. 对合法 orderId 可直接触发支付后置逻辑
- fix_recommendation: `生产环境移除该 action 路由；若保留仅用于测试，需环境开关+白名单+鉴权并校验 user_id。`
- regression_tests:
  1. 生产环境访问该路径应 404/403
  2. 支付状态仅可由微信回调或受控内部任务推进
- confidence: `0.97`

## Finding 3
- id: `HR-003`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/api/controller/base.js; src/api/controller/order.js`
- line: `base 2-7; order 15-53`
- title: `API 层未统一强制登录，存在“未登录进入业务逻辑”`
- impact: `保护能力依赖各 action 手工判断，容易出现遗漏，导致越权/信息探测面扩大。`
- evidence: `base.__before 仅解析 token 到 think.userId，不做鉴权阻断；动态验证：未带 token 请求 /api/order/list 返回 errno=0。`
- repro_steps:
  1. `GET /api/order/list?showType=0&page=1&size=1` 不带 token
  2. 返回 `{"errno":0,...}` 而非 401
- fix_recommendation: `在统一中间件/基类按白名单（publicController/publicAction）做鉴权拦截，其余默认拒绝；禁止“0 号用户”进入受限 action。`
- regression_tests:
  1. 所有非白名单 API 未登录应返回统一 401
  2. 白名单 API 继续可匿名访问
- confidence: `0.95`

## Finding 4
- id: `HR-004`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/api/service/token.js; src/admin/service/token.js`
- line: `api 2,27-29; admin 2,41-43`
- title: `JWT 密钥硬编码且未设置过期`
- impact: `源码泄露或日志外泄后可伪造长期有效 token；无法做有效会话回收。`
- evidence: `secret 以字符串常量硬编码；jwt.sign 未设置 expiresIn。`
- repro_steps:
  1. 阅读 token service 代码
  2. 确认无环境变量密钥与过期策略
- fix_recommendation: `密钥改为环境变量并轮换；签发 token 加 expiresIn + jti；服务端增加失效黑名单/版本戳。`
- regression_tests:
  1. 过期 token 请求应被拒绝
  2. 轮换密钥后旧 token 不可用
- confidence: `0.99`

## Finding 5
- id: `HR-005`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/admin/controller/goods.js; src/admin/service/oss.js`
- line: `goods 1025-1033; oss 70-79,105-123`
- title: `后台 URL 抓图接口存在 SSRF 面`
- impact: `攻击者可利用服务端请求内网地址/云元数据或探测内部网络，形成信息泄露与横向风险。`
- evidence: `uploadHttpsImageAction 接受外部 url 直接 fetchAndUpload；downloadRemote 未做协议/域名/IP 限制，且 strictSSL=false + followAllRedirects=true。`
- repro_steps:
  1. 登录后台后调用 `uploadHttpsImageAction` 传入内网/重定向 URL
  2. 服务端将代发请求并处理响应
- fix_recommendation: `仅允许 https + 域名白名单；解析并拦截内网/保留地址段；关闭 followAllRedirects；强制 strictSSL=true；限制响应大小/类型。`
- regression_tests:
  1. `127.0.0.1/169.254.169.254` 等地址必须被拒绝
  2. 非白名单域名必须拒绝
  3. 正常 CDN 图片可上传成功
- confidence: `0.94`

## Finding 6
- id: `HR-006`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/admin/controller/admin.js; src/admin/controller/auth.js`
- line: `admin 180-188; auth 12-13`
- title: `管理员口令存储使用固定盐+MD5`
- impact: `抗暴力破解能力弱，撞库/离线破解成本低于现代 KDF（bcrypt/argon2）。`
- evidence: `创建管理员时固定 password_salt='HIOLABS'，认证时 think.md5(password + salt) 比对。`
- repro_steps:
  1. 查看管理员创建与登录代码
  2. 确认固定盐 + md5 方案
- fix_recommendation: `迁移到 bcrypt/argon2（每用户随机盐、足够 cost）；支持渐进迁移（登录时重哈希）。`
- regression_tests:
  1. 新建管理员密码应为 bcrypt/argon2 哈希
  2. 老账号首次登录后自动迁移并可继续登录
- confidence: `0.96`

## Finding 7
- id: `HR-007`
- priority: `P1`
- repo: `hioshop-admin-web`
- file: `src/main.js`
- line: `32-35`
- title: `生产环境启用 MockXHR`
- impact: `线上可能被 mock 数据覆盖真实接口行为，导致权限/订单/商品管理判断失真。`
- evidence: `if (process.env.NODE_ENV === 'production') { mockXHR() }`。
- repro_steps:
  1. 构建 production 包并加载后台
  2. 观察 mock 层在生产环境被激活
- fix_recommendation: `仅在本地开发开启 mock；生产构建强制禁用；增加 CI 规则扫描禁止该条件进入产物。`
- regression_tests:
  1. 生产构建中不应包含 mock 注入入口
  2. 开发环境可按开关启用 mock
- confidence: `0.98`
