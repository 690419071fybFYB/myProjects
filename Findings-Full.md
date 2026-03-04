# Findings-Full (P0-P3)

审查时间：2026-03-04（Asia/Shanghai）  
覆盖范围：`hioshop-miniprogram`、`hioshop-server`、`hioshop-admin-web`（包含当前未提交改动）

## P0/P1

### Finding 1
- id: `FULL-001`
- priority: `P0`
- repo: `hioshop-server`
- file: `src/api/controller/order.js; src/api/model/order.js`
- line: `257-265, 271-287, 293-304, 454-481, 487-531; model 38-48`
- title: `订单关键写操作未按 user_id 做归属校验（IDOR）`
- impact: `可跨账号篡改订单状态、地址、物流可见性。`
- evidence: `delete/confirm/complete/update/express 仅以 orderId 为主键操作；getOrderHandleOption 未绑定 userId。`
- repro_steps:
  1. 未登录或他人 token 调用 `/api/order/confirm`、`/api/order/delete`、`/api/order/update`
  2. 观察进入业务逻辑而非统一鉴权阻断
- fix_recommendation: `所有订单读写强制 where(id, user_id)；模型接口签名增加 userId。`
- regression_tests:
  1. 非本人订单操作全部失败
  2. 本人订单合法状态可操作
- confidence: `0.98`

### Finding 2
- id: `FULL-002`
- priority: `P0`
- repo: `hioshop-server`
- file: `src/api/controller/pay.js`
- line: `11-27`
- title: `测试支付接口 preWeixinPaya 可在生产路径访问`
- impact: `可直接推进订单支付后状态，影响资金与券资产一致性。`
- evidence: `preWeixinPayaAction 内部伪造交易结果并调用 updatePayData/consumeCoupons/afterPay。`
- repro_steps:
  1. 请求 `GET /api/pay/preWeixinPaya?orderId=<id>`
  2. 对可用订单可绕过真实支付链路
- fix_recommendation: `生产环境移除；若保留需环境隔离+严格鉴权+审计。`
- regression_tests:
  1. 生产不可访问该 action
  2. 支付状态变更仅来自回调/受控任务
- confidence: `0.97`

### Finding 3
- id: `FULL-003`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/api/controller/base.js; src/api/controller/order.js`
- line: `base 2-7; order 15-53`
- title: `API 缺少统一登录拦截，受限逻辑出现匿名可达`
- impact: `保护依赖业务代码自觉，易产生漏拦截和权限绕过。`
- evidence: base.__before 不做拒绝；动态探测 `/api/order/list` 未登录返回 errno=0。
- repro_steps:
  1. 不带 token 请求 `/api/order/list?showType=0&page=1&size=1`
  2. 返回 `{"errno":0,...}`
- fix_recommendation: `实现统一白名单拦截机制，默认拒绝。`
- regression_tests:
  1. 非白名单未登录全部 401
  2. 白名单路径保持可访问
- confidence: `0.95`

### Finding 4
- id: `FULL-004`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/api/service/token.js; src/admin/service/token.js`
- line: `api 2,27-29; admin 2,41-43`
- title: `JWT 密钥硬编码且无过期`
- impact: `密钥泄露后可伪造长期 token，难以失效治理。`
- evidence: `secret 为固定字符串；jwt.sign 未设置 expiresIn。`
- repro_steps:
  1. 检查 token service
  2. 验证无动态密钥与 TTL
- fix_recommendation: `环境变量密钥 + 轮换 + 过期 + jti。`
- regression_tests:
  1. 过期 token 拒绝
  2. 密钥轮换后旧 token 失效
- confidence: `0.99`

### Finding 5
- id: `FULL-005`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/admin/controller/goods.js; src/admin/service/oss.js`
- line: `goods 1025-1033; oss 70-79,105-123`
- title: `后台远程抓图接口存在 SSRF`
- impact: `可能探测内网、访问元数据、扩大攻击面。`
- evidence: `任意 url 进入 request.get，未做协议/IP/域名限制，允许重定向且关闭 strictSSL。`
- repro_steps:
  1. 调用 `uploadHttpsImageAction` 传入内网地址或跳转链
  2. 观察服务端代发请求
- fix_recommendation: `HTTPS + 白名单 + 拒绝内网段 + 禁止任意重定向 + 证书校验。`
- regression_tests:
  1. 内网地址拒绝
  2. 白名单域名可用
- confidence: `0.94`

### Finding 6
- id: `FULL-006`
- priority: `P1`
- repo: `hioshop-server`
- file: `src/admin/controller/admin.js; src/admin/controller/auth.js`
- line: `admin 180-188; auth 12-13`
- title: `管理员密码方案为固定盐+MD5`
- impact: `弱口令防护不足，离线破解成本高风险。`
- evidence: `password_salt 固定 'HIOLABS'，登录 compare 使用 think.md5(password+salt)。`
- repro_steps:
  1. 查看管理员新增与登录代码
- fix_recommendation: `迁移 bcrypt/argon2，并做渐进升级。`
- regression_tests:
  1. 新密码使用 KDF
  2. 旧密码迁移可回归登录
- confidence: `0.96`

### Finding 7
- id: `FULL-007`
- priority: `P1`
- repo: `hioshop-admin-web`
- file: `src/main.js`
- line: `32-35`
- title: `生产环境启用 mockXHR`
- impact: `后台线上行为可能与真实 API 偏离，影响订单与权限决策。`
- evidence: `NODE_ENV=production 时调用 mockXHR()。`
- repro_steps:
  1. production 构建后启动
  2. 确认 mock 注入存在
- fix_recommendation: `仅 dev 开启 mock；生产构建强制剔除。`
- regression_tests:
  1. 产物中无 mock 入口
- confidence: `0.98`

## P2

### Finding 8
- id: `FULL-008`
- priority: `P2`
- repo: `hioshop-server`
- file: `src/api/controller/order.js`
- line: `460-471, 478-481`
- title: `order/update 对空地址对象直接解引用，导致 500`
- impact: `异常输入导致服务错误页泄露与接口不稳定。`
- evidence: `updateAddress.find() 结果未判空直接读取 name/mobile/...；动态探测假 id 返回 HTTP 500 HTML。`
- repro_steps:
  1. `POST /api/order/update` with `orderId=999999999&addressId=999999999`
  2. 返回 500 Internal Server Error
- fix_recommendation: `address/order 判空与归属校验，不合法返回 400/404，避免抛栈。`
- regression_tests:
  1. 非法地址 id 返回 4xx
  2. 响应不含框架错误页
- confidence: `0.99`

### Finding 9
- id: `FULL-009`
- priority: `P2`
- repo: `hioshop-server`
- file: `src/api/controller/settings.js`
- line: `12-35`
- title: `settings/save 缺少登录阻断与输入健壮性校验`
- impact: `可能出现异常写入、脏数据或运行时异常。`
- evidence: userId 未先校验；`Buffer.from(nickName)` 对非法值可抛错；mobile/name 无服务端格式校验。
- repro_steps:
  1. 未登录或提交异常类型 nickName 调用 `/api/settings/save`
  2. 观察异常行为（依赖运行时参数）
- fix_recommendation: `先校验登录态，再做字段 schema 校验（昵称、手机号长度与格式）。`
- regression_tests:
  1. 未登录统一 401
  2. 非法 nickName/mobile 返回 400
- confidence: `0.88`

### Finding 10
- id: `FULL-010`
- priority: `P2`
- repo: `hioshop-miniprogram + hioshop-server`
- file: `miniprogram utils/request/index.js; server auth.js/settings.js`
- line: `request 182-205; auth 89-91; settings 50`
- title: `鉴权错误码不一致（100/401）导致会话刷新链路不稳定`
- impact: `小程序仅对 errno=401 做自动续期，返回 errno=100 时会直接失败，触发“未授权手机号/未登录”体验问题。`
- evidence: request SDK 只在 body.errno===401 时 refreshToken；服务端多处未登录返回 100。动态探测 `/api/auth/phoneNumber` 未登录返回 `{\"errno\":100}`。
- repro_steps:
  1. 会话失效后触发手机号授权接口
  2. 接口返回 errno=100，不触发自动登录续期
- fix_recommendation: `统一未登录码为 401（或 SDK 同时处理 100/401）；约定全端错误码标准。`
- regression_tests:
  1. token 过期后手机号授权可自动续期并重试成功
  2. 未登录错误码全端一致
- confidence: `0.93`

### Finding 11
- id: `FULL-011`
- priority: `P2`
- repo: `hioshop-server`
- file: `src/api/controller/upload.js`
- line: `16-25`
- title: `头像上传接口允许匿名上传（仅跳过用户绑定）`
- impact: `可被滥用为匿名存储入口，带来成本与滥用风险。`
- evidence: `userId<=0 时仍返回上传成功并保留文件 URL。`
- repro_steps:
  1. 不带 token 调用 `/api/upload/uploadAvatar`
  2. 上传成功但不绑定用户
- fix_recommendation: `头像上传要求登录；或对匿名上传加验证码、频率限制与回收策略。`
- regression_tests:
  1. 未登录上传头像应 401
  2. 已登录上传并正确绑定用户头像
- confidence: `0.90`

### Finding 12
- id: `FULL-012`
- priority: `P2`
- repo: `hioshop-server`
- file: `src/api/config/config.js; src/api/controller/cart.js`
- line: `config 18-23; cart 10-25`
- title: `购物车匿名态使用 user_id=0，存在“游客购物车混用”风险`
- impact: `多个匿名请求可能共用同一 user_id 维度数据，造成脏数据/误操作。`
- evidence: `cart 系列 action 被标记为 public；cart controller 直接以 getLoginUserId() 结果作为 user_id 查询。`
- repro_steps:
  1. 在无 token 情况下多端操作购物车
  2. 检查后端 user_id=0 数据是否出现混用
- fix_recommendation: `游客购物车改为 sessionKey/deviceKey 隔离，不与固定 user_id 绑定。`
- regression_tests:
  1. 匿名 A 与匿名 B 购物车互不影响
- confidence: `0.86`

## P3（维护性/工程质量）

### Finding 13
- id: `FULL-013`
- priority: `P3`
- repo: `hioshop-server`
- file: `src/api/model/order.js`
- line: `7-10`
- title: `订单号生成规则存在可读性错误与潜在碰撞风险`
- impact: `getMonth/getDay 使用不当（月份从0起、day为星期），可导致时间片段语义错误；高并发下碰撞风险仍存在。`
- evidence: `generateOrderNumber 由日期片段+6位随机数组成，注释也标明“存在两个订单相同可能”。`
- repro_steps:
  1. 阅读 `generateOrderNumber` 实现
- fix_recommendation: `改用 getDate 且补零；引入数据库唯一索引+重试，或雪花/序列号。`
- regression_tests:
  1. 压测下订单号唯一
- confidence: `0.84`

### Finding 14
- id: `FULL-014`
- priority: `P3`
- repo: `hioshop-server + hioshop-admin-web`
- file: `server package.json; admin package.json`
- line: `server 5-12; admin 6-15`
- title: `静态质量门禁不可用（lint/test/build 基线不稳定）`
- impact: `缺陷进入主干概率上升，审查和回归成本增加。`
- evidence: `server lint 找不到 ESLint 配置；admin lint 缺少 eslint 可执行；admin unit 无测试；admin build 在 Node 23 下 OpenSSL 报错。`
- repro_steps:
  1. 执行 `npm run lint/test:unit/build:prod`
  2. 观察失败原因
- fix_recommendation: `补齐 eslint 配置与依赖；为 CI 锁定 Node LTS（如 18/20）；补最小单测集并允许 no-tests 策略显式声明。`
- regression_tests:
  1. CI 中 lint/test/build 全绿
- confidence: `0.99`

### Finding 15
- id: `FULL-015`
- priority: `P3`
- repo: `hioshop-miniprogram`
- file: `utils/util.js`
- line: `261-265`
- title: `客户端硬编码第三方 Trackingmore API Key`
- impact: `小程序包可被反编译提取 key，导致额度滥用与风控问题。`
- evidence: 请求头内写死 `Trackingmore-Api-Key: 1b70c67e-...`。
- repro_steps:
  1. 查看 util.js
- fix_recommendation: `迁移到服务端代理签名，客户端不持有长期密钥。`
- regression_tests:
  1. 客户端包不含第三方密钥
- confidence: `0.97`

### Finding 16
- id: `FULL-016`
- priority: `P3`
- repo: `hioshop-miniprogram`
- file: `components/login-profile-sheet/index.wxml; index.js`
- line: `wxml 22-31; js 72-93,117-143`
- title: `登录弹窗昵称授权路径依赖客户端能力，兼容性和可理解性弱`
- impact: `不同基础库/机型上可能出现“点击一键后仍为微信用户/需多次操作”的体验不一致。`
- evidence: 昵称 input 使用 `type=\"nickname\"` 且依赖禁用态按钮触发 actionSheet + getUserProfile；逻辑分支较多。
- repro_steps:
  1. 在不同微信版本测试昵称获取
  2. 对比是否稳定回填昵称与头像
- fix_recommendation: `简化交互：保留单一昵称输入与单一授权入口；失败后明确回退到手填。`
- regression_tests:
  1. 授权成功后昵称/头像稳定回填
  2. 授权拒绝后可无阻手填并提交
- confidence: `0.78`

---

## 未提交改动覆盖说明
已覆盖以下未提交改动并纳入审查上下文：
- `hioshop-miniprogram/pages/goods/*`（券后价展示）
- `hioshop-miniprogram/pages/index/*`（领券区状态）
- `hioshop-miniprogram/pages/order-check/index.js`（优惠券参数类型）
- `hioshop-miniprogram/pages/order-coupon/index.js`（服务端回填选券）
- `hioshop-server/src/api/controller/goods.js`（商品详情券后装饰）

本次未在这些增量改动中发现新的 P0/P1 问题；主要高风险仍集中在服务端既有鉴权/支付/订单写链路。
