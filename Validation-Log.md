# Validation-Log

审查时间窗口：2026-03-04（Asia/Shanghai）  
执行策略：仅执行非破坏性命令与只读/最小化动态探测；未修改业务代码。

## 1. 基线冻结

### 1.1 Workspace
- 命令：`pwd && date '+%F %T %Z' && git rev-parse --abbrev-ref HEAD && git rev-parse HEAD`
- 结果：
  - cwd: `/Volumes/SAMSUNG/fyb/myProjects`
  - time: `2026-03-04 01:09:22 CST`
  - branch: `main`
  - commit: `933b39b05623e24fa7a99efd0bf907af46767d36`

### 1.2 三端仓库分支与未提交改动
- 命令：`for d in hioshop-miniprogram hioshop-server hioshop-admin-web; do ... git status --short; done`
- 结果：
  - `hioshop-miniprogram`: `master@fd676c0d28ae8c7acbfcf437e0195356be465181`
    - dirty:
      - `pages/goods/goods.js`
      - `pages/goods/goods.wxml`
      - `pages/goods/goods.wxss`
      - `pages/index/index.js`
      - `pages/index/index.wxml`
      - `pages/order-check/index.js`
      - `pages/order-coupon/index.js`
  - `hioshop-server`: `master@98fcffd047f96546796e31d98d63769f44e4b9e7`
    - dirty: `src/api/controller/goods.js`
  - `hioshop-admin-web`: `main@92ff44c2b2372b68acf0014a372fc525034e3618`
    - dirty: none

## 2. 自动化静态/构建验证

### 2.1 hioshop-server
- 命令：`npm run lint`
- 结果：`exit=1`
- 摘要：`ESLint couldn't find a configuration file`（从 `src/admin/config` 开始向上未找到）

- 命令：`npm run compile`
- 结果：`exit=0`
- 摘要：Babel compile 成功，`src/* -> app/*` 全量输出

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=1`
- 摘要：`77 vulnerabilities (3 low, 21 moderate, 31 high, 22 critical)`

### 2.2 hioshop-admin-web
- 命令：`npm run lint`
- 结果：`exit=127`
- 摘要：`sh: eslint: command not found`

- 命令：`npm run test:unit`
- 结果：`exit=1`
- 摘要：`No tests found`

- 命令：`npm run build:prod`
- 结果：`exit=1`
- 摘要：`ERR_OSSL_EVP_UNSUPPORTED`（Node 23 + webpack/OpenSSL 兼容问题）

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=1`
- 摘要：`7 vulnerabilities (2 low, 2 moderate, 3 high)`

### 2.3 hioshop-miniprogram
- 命令：`node -e "...scripts..."`
- 结果：`scripts []`
- 摘要：无 npm scripts（lint/test/build 未内置）

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=0`
- 摘要：`found 0 vulnerabilities`

### 2.4 接口可用性 smoke
- 命令：`./scripts/smoke_check.sh https://api.fybshop.site qilelab.com qilelab.com`
- 结果：`exit=0`
- 摘要：`all checks passed`
- 覆盖：
  - `GET /api/index/appInfo`
  - `GET /api/catalog/index`
  - `POST /admin/auth/login`
  - `GET /api/cart/goodsCount`

## 3. 动态验证（关键链路）

> 说明：以下均为最小化只读/无害探测，未执行破坏性操作。

### 3.1 未登录访问行为
- 命令：`GET /api/order/list?showType=0&page=1&size=1`
- 结果：`status=200`，body `{"errno":0,...}`
- 结论：未登录仍进入业务成功路径

- 命令：`GET /api/settings/userDetail`
- 结果：`status=200`，body `{"errno":100,"errmsg":"未登录"}`

- 命令：`GET /api/coupon/center`
- 结果：`status=200`，body `{"errno":401,"errmsg":"请先登录"}`

- 命令：`POST /api/auth/phoneNumber`（无 token）
- 结果：`status=200`，body `{"errno":100,"errmsg":"未登录"}`

### 3.2 订单写接口异常输入
- 命令：`POST /api/order/confirm` `orderId=999999999`
- 结果：`status=200`，body `{"errno":1000,"errmsg":"订单不能确认"}`

- 命令：`POST /api/order/delete` `orderId=999999999`
- 结果：`status=200`，body `{"errno":1000,"errmsg":"订单不能删除"}`

- 命令：`POST /api/order/update` `orderId=999999999&addressId=999999999`
- 结果：`status=500`，返回 ThinkJS Internal Server Error HTML

### 3.3 支付相关路径
- 命令：`GET /api/pay/preWeixinPay?orderId=999999999`
- 结果：`status=200`，body `{"errno":400,"errmsg":"订单已取消"}`

- 命令：`GET /api/pay/preWeixinPaya?orderId=999999999`
- 结果：`status=500`，返回 ThinkJS Internal Server Error HTML
- 结论：测试支付路径在生产 API 可达

## 4. 代码证据采样

已读取并定位关键证据文件（含行号）：
- `hioshop-server/src/api/controller/order.js`
- `hioshop-server/src/api/model/order.js`
- `hioshop-server/src/api/controller/pay.js`
- `hioshop-server/src/api/controller/base.js`
- `hioshop-server/src/api/service/token.js`
- `hioshop-server/src/admin/service/token.js`
- `hioshop-server/src/api/controller/settings.js`
- `hioshop-server/src/api/controller/upload.js`
- `hioshop-server/src/admin/controller/goods.js`
- `hioshop-server/src/admin/service/oss.js`
- `hioshop-admin-web/src/main.js`
- `hioshop-miniprogram/components/login-profile-sheet/index.js|wxml`
- `hioshop-miniprogram/utils/request/index.js`
- `hioshop-miniprogram/utils/util.js`
- 以及未提交改动 diff：
  - `hioshop-miniprogram/pages/goods/*`
  - `hioshop-miniprogram/pages/index/*`
  - `hioshop-miniprogram/pages/order-check/index.js`
  - `hioshop-miniprogram/pages/order-coupon/index.js`
  - `hioshop-server/src/api/controller/goods.js`

## 5. 阻塞与替代证据

### 5.1 受环境限制未执行项
- 小程序真机微信授权交互（头像/手机号）端到端链路：
  - 阻塞：当前终端无法直接驱动微信真机授权弹窗
  - 替代：基于前后端代码路径 + API 动态响应做静态可达性判定

- 真实支付回调全链路验证：
  - 阻塞：缺少支付沙箱/商户凭据
  - 替代：对 `preWeixinPay/preWeixinPaya` 做最小请求和代码审查

- 后台高权限操作真实写入验证：
  - 阻塞：未提供管理员测试账号
  - 替代：通过代码证据与只读接口验证风险路径

## 6. 结论性说明
- 本次验证覆盖了三端静态+动态检查与关键路径抽样。
- 已按计划输出可复验问题清单与依赖风险分级。
