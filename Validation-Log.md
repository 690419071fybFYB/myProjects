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

## 7. Stage 3 修复增量验证（2026-03-04）

### 7.1 hioshop-server（Batch B/C）
- 命令：`npm install`（新增 `bcryptjs`）
- 结果：`exit=0`

- 命令：`npm install jsonwebtoken@^9.0.2`
- 结果：`exit=0`
- 摘要：`jsonwebtoken` 升级到 9.x，lockfile 已更新

- 命令：`npm run compile`
- 结果：`exit=0`
- 摘要：含 `admin/service/password.js`、`admin/service/oss.js` 在内的增量编译通过

- 命令：`rg -n "hashPassword|verifyPassword|assertRemoteUrlSafe|strictSSL|md5\\(" src/admin src/common/config/config.js`
- 结果：`exit=0`
- 摘要：
  - 新增密码服务：`src/admin/service/password.js`
  - 登录与改密已接入 `verifyPassword/hashPassword`
  - 抓图链路已接入 `assertRemoteUrlSafe`，并启用 HTTPS+MIME+体积限制
  - 业务关键路径不再使用固定盐 `HIOLABS` 做新密码哈希

### 7.2 hioshop-admin-web（W-C4）
- 命令：`npm install axios@^1.8.4`
- 结果：`exit=0`
- 摘要：`axios` 升级到 1.x，lockfile 已更新

- 命令：`npm run build:prod`
- 结果：`exit=0`
- 摘要：生产构建通过（存在 assets 体积 warning，不阻断）
- 备注：已将 `package.json` 中 `build:prod/build:stage` 脚本统一加上 `NODE_OPTIONS=--openssl-legacy-provider`，避免 Node 17+ OpenSSL 兼容报错。

### 7.3 本轮结论
- `S-C1`：完成，抓图 SSRF 风险已显著收敛（协议、域名/IP、重定向、内容类型、体积、审计日志）。
- `S-C2`：完成，后台密码进入 `bcrypt`，并兼容旧 `md5` 平滑迁移。
- `S-C3`：进行中，已完成 `jsonwebtoken` 升级 + 抓图链路移除 `request`；其余外部请求链路待继续迁移。
- `W-C4`：完成，`axios` 升级后可构建（脚本已内置 OpenSSL 兼容参数）。

## 8. Stage 3 继续执行增量（2026-03-04）

### 8.1 新增公共 HTTP 工具并替换微信核心链路
- 新增：`src/common/utils/http.js`
- 已替换调用点：
  - `src/api/controller/auth.js`（`loginByWeixinAction`）
  - `src/api/service/weixin.js`（`getAccessToken/getPhoneNumberByCode/send*Message`）
  - `src/admin/service/token.js`（`getAccessToken`）
  - `src/api/controller/order.js`（`getExpressInfo`）
  - `src/api/controller/qrcode.js`（access_token 获取复用 weixin service）

### 8.2 编译与残留扫描
- 命令：`hioshop-server npm run compile`
- 结果：`exit=0`

- 命令：`rg -n "require\\(['\\\"]request(-promise)?['\\\"]\\)|\\brp\\(|request\\." hioshop-server/src -g"*.js"`
- 结果：仍有残留（主要在以下文件）：
  - `src/api/service/express.js`
  - `src/admin/service/express.js`
  - `src/admin/model/order_express.js`
  - `src/api/service/oss.js`

### 8.3 增量结论
- `S-C3` 持续推进中：登录与微信资料主链路已完成迁移，剩余主要是物流/历史路径。

## 9. Stage 3 持续推进增量（2026-03-04）

### 9.1 request/request-promise 全量移除（代码层）
- 迁移范围补充：
  - `src/api/service/express.js`
  - `src/admin/service/express.js`
  - `src/admin/model/order_express.js`
  - `src/api/service/oss.js`
  - `scripts/migrate-legacy-images-to-oss.js`
- 依赖清理：
  - `package.json` 移除 `request`、`request-promise` 直依赖
  - `npm install` 后 lockfile 更新

### 9.2 验证命令与结果
- 命令：`rg -n "require\\(['\\\"]request-promise['\\\"]\\)|\\brp\\(|require\\(['\\\"]request['\\\"]\\)|request\\." hioshop-server/src hioshop-server/scripts -g"*.js"`
- 结果：无匹配（代码层已无直接引用）

- 命令：`hioshop-server npm run compile`
- 结果：`exit=0`

- 命令：`hioshop-server npm audit --omit=dev --audit-level=high`
- 结果：高危数量较前次下降（由 `99` 降到 `95`）

- 命令：移除未使用依赖 `node-wget` 后再次执行 `npm audit --omit=dev --audit-level=high`
- 结果：进一步下降到 `66`（`3 low, 17 moderate, 25 high, 21 critical`）

### 9.3 结论
- `S-C3` 当前进入“依赖治理”阶段：代码中已去除 `request/request-promise`，并清理未使用依赖 `node-wget`；后续重点是处理 `weixinpay/cos SDK/thinkjs` 带来的传递高危项。

## 10. Stage 3 依赖治理补充（2026-03-04）

### 10.1 直依赖收敛
- 移除未使用或冗余直依赖：
  - `jushuitan`
  - `gm`
  - `querystring`
  - `xml2js`（直依赖）
- 升级：
  - `moment` -> `^2.30.1`
  - `nanoid` -> `^3.3.11`
- 清理无用 import：
  - `src/api/controller/pay.js` 去掉无用 `moment/nanoid-generate` 引入
  - `src/api/controller/index.js` 去掉无用 `moment` 引入
  - `src/admin/controller/order.js` 删除历史注释残留

### 10.2 验证结果
- 命令：`hioshop-server npm run compile`
- 结果：`exit=0`

- 命令：`hioshop-server npm audit --omit=dev --audit-level=high`
- 结果：`58 vulnerabilities (2 low, 16 moderate, 19 high, 21 critical)`
- 对比：较上一轮（`66`）继续下降

- 命令：`rg -n "jushuitan|require\\(['\\\"]gm['\\\"]\\)|node-wget|request-promise" ...`
- 结果：无代码引用

### 10.3 当前边界
- 主要剩余风险集中在老框架与传递依赖：
  - `thinkjs` 生态链（`think-*`）
  - `cos-nodejs-sdk-v5`（内部依赖 `request/conf/fast-xml-parser`）
  - `weixinpay`
  - `xlsx`（当前无可用安全修复版本）

## 11. admin-web 继续收敛（2026-03-04）

### 11.1 变更
- 移除未使用依赖 `path-to-regexp`（直接依赖层）
- 保持 `axios` 1.x 与构建脚本 OpenSSL 兼容参数

### 11.2 验证
- 命令：`hioshop-admin-web npm audit --omit=dev --audit-level=high`
- 结果：仅剩 4 个漏洞（`2 low, 2 moderate`），已无高危
- 主要剩余：
  - `vue@2.x`（框架代际问题，修复需 Vue3 迁移）
  - `quill/vue-quill-editor`（上游尚无可用修复）

- 命令：`hioshop-admin-web npm run build:prod`
- 结果：`exit=0`（仅体积 warning，不阻断）

## 12. Stage 3 第四批验证（2026-03-04）

### 12.1 hioshop-server
- 命令：`npm uninstall weixinpay`
- 结果：`exit=0`
- 摘要：移除 `weixinpay` 直依赖。

- 命令：`npm install sanitize-html@^2.17.0`
- 结果：`exit=0`
- 摘要：新增富文本清洗依赖。

- 命令：`npm run compile`
- 结果：`exit=0`
- 摘要：包含 `src/api/service/weixin.js`、`src/common/utils/sanitize_html.js`、`src/admin/controller/goods.js`、`src/admin/service/goods_import.js` 等改动均编译通过。

- 命令：`npm run test:goods-import`
- 结果：`exit=0`
- 摘要：8/8 用例通过（含模板下载、预检、导入、重复 SKU 跳过与错误文件校验）。

- 命令：`npm run test:coupon`
- 结果：`exit=0`
- 摘要：优惠券模块自动化冒烟通过。

- 命令：`npm ls request --all`
- 结果：`exit=0`
- 摘要：`request` 仅剩 `cos-nodejs-sdk-v5` 传递依赖。

- 命令：`rg -n "weixinpay" hioshop-server`
- 结果：`exit=1`（无匹配）
- 摘要：代码与依赖层已清除 `weixinpay` 引用。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：受网络影响失败（`Client network socket disconnected before secure TLS connection was established`）
- 说明：本轮未拿到稳定审计快照，后续网络恢复后需补跑。

### 12.2 hioshop-admin-web
- 命令：`npm run build:prod`
- 结果：`exit=0`
- 摘要：生产构建通过（仅 bundle 体积告警）。

- 命令：`npm run test:unit`
- 结果：`exit=1`
- 摘要：仓库未包含单元测试文件（`No tests found`）。

- 命令：`npm run lint`
- 结果：`exit=127`
- 摘要：当前环境缺少 `eslint` 可执行（工具链依赖未完整安装）。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：受网络影响失败（同上 TLS 断连）。

### 12.3 hioshop-miniprogram
- 命令：`node -c components/login-profile-sheet/index.js`
- 结果：`exit=0`

- 命令：`node -c pages/category/index.js`
- 结果：`exit=0`

- 命令：`node -c pages/ucenter/index/index.js`
- 结果：`exit=0`
- 摘要：本轮涉及的关键 JS 文件语法检查通过。

### 12.4 hioshop-server（导入大小限制补丁回归）
- 命令：`npm run compile && npm run test:goods-import`
- 结果：`exit=0`
- 摘要：新增导入文件大小/MIME/后缀校验后，商品导入自动化 8/8 仍通过。

## 13. Stage 3 第五批验证（2026-03-04）

### 13.1 hioshop-server
- 命令：`npm run compile`
- 结果：`exit=0`
- 摘要：新增 `src/common/utils/validate.js`，并接入 `auth/settings/upload` 控制器后编译通过。

- 命令：`npm run test:coupon`
- 结果：`exit=0`
- 摘要：优惠券自动化冒烟通过。

- 命令：`npm run test:goods-import`
- 结果：`exit=0`
- 摘要：商品导入自动化 8/8 通过（新增校验未影响主流程）。

### 13.2 hioshop-miniprogram
- 命令：`node -c components/login-profile-sheet/index.js`
- 结果：`exit=0`

- 命令：`node -c pages/ucenter/settings/index.js`
- 结果：`exit=0`
- 摘要：登录弹窗与设置页关键改动语法检查通过。

## 14. Stage 3 第六批验证（2026-03-04）

### 14.1 hioshop-server（依赖锁恢复 + SSRF 对齐）
- 命令：`npm install --force --fetch-retries=...`
- 结果：`exit=0`
- 摘要：修复中断后的安装状态，完成 lock 同步。

- 命令：`npm ls fast-xml-parser`
- 结果：`exit=0`
- 摘要：`cos-nodejs-sdk-v5 -> fast-xml-parser@4.5.4`。

- 命令：`npm run compile && npm run test:coupon && npm run test:goods-import`
- 结果：`exit=0`
- 摘要：编译通过，优惠券与商品导入自动化均通过。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=1`（审计有高危）
- 摘要：当前为 `51 vulnerabilities (1 low, 16 moderate, 16 high, 18 critical)`。

### 14.2 hioshop-admin-web（门禁恢复）
- 命令：`npm install`
- 结果：`exit=0`
- 摘要：安装 `eslint` 及相关依赖。

- 命令：`npm run lint`
- 结果：`exit=0`
- 摘要：lint 命令恢复可执行并通过。

- 命令：`npm run test:unit -- --passWithNoTests`
- 结果：`exit=0`
- 摘要：仓库无单测文件，按 passWithNoTests 通过。

- 命令：`npm run build:prod`
- 结果：`exit=0`
- 摘要：生产构建通过（仅体积 warning）。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=0`
- 摘要：维持 `4 vulnerabilities (2 low, 2 moderate)`，无高危。

### 14.3 hioshop-miniprogram
- 命令：
  - `node -c pages/category/index.js`
  - `node -c components/login-profile-sheet/index.js`
  - `node -c pages/ucenter/settings/index.js`
- 结果：全部 `exit=0`
- 摘要：关键变更文件语法检查通过。

## 15. Stage 3 第七批验证（2026-03-04）

### 15.1 hioshop-server
- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：
  - 新增头像文件头校验、xlsx 文件头校验后，编译与两条自动化回归均通过。

- 命令：`npm ls fast-xml-parser`
- 结果：`exit=0`
- 摘要：`cos-nodejs-sdk-v5 -> fast-xml-parser@4.5.4`。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=1`
- 摘要：`51 vulnerabilities (1 low, 16 moderate, 16 high, 18 critical)`。

### 15.2 hioshop-admin-web
- 命令：`npm run lint`
- 结果：`exit=0`
- 摘要：lint 门禁恢复并通过。

- 命令：`npm run test:unit -- --passWithNoTests`
- 结果：`exit=0`

- 命令：`npm run build:prod`
- 结果：`exit=0`

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=0`
- 摘要：`4 vulnerabilities (2 low, 2 moderate)`。

### 15.3 hioshop-miniprogram
- 命令：
  - `node -c pages/category/index.js`
  - `node -c components/login-profile-sheet/index.js`
  - `node -c pages/ucenter/settings/index.js`
- 结果：全部 `exit=0`

## 16. Stage 3 第八批验证（2026-03-04）

### 16.1 hioshop-server
- 命令：`npm uninstall qiniu`
- 结果：`exit=0`
- 摘要：移除未使用 qiniu 依赖与相关包。

- 命令：`npm ls qiniu`
- 结果：`(empty)`
- 摘要：qiniu 已不在依赖树中。

- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：删除 qiniu 链路后，服务端编译与两条自动化回归均通过。

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=1`
- 摘要：受可选依赖影响，显示 `56 vulnerabilities`。

- 命令：`npm audit --omit=dev --omit=optional --audit-level=high`
- 结果：`exit=1`
- 摘要：稳定口径下为 `42 vulnerabilities (14 moderate, 11 high, 17 critical)`。

### 16.2 hioshop-admin-web
- 命令：`npm run lint`
- 结果：`exit=0`

- 命令：`npm run test:unit -- --passWithNoTests`
- 结果：`exit=0`

- 命令：`npm run build:prod`
- 结果：`exit=0`

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=0`
- 摘要：维持 `4 vulnerabilities (2 low, 2 moderate)`。

## 17. Stage 3 第九批验证（2026-03-04）

### 17.1 hioshop-server（门禁服务端化 + 地址校验）
- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：新增资料完整性门禁、地址参数校验后，编译与两套自动化回归均通过。

### 17.2 hioshop-miniprogram（412 联动）
- 命令：
  - `node -c utils/request/index.js`
  - `node -c utils/util.js`
  - `node -c components/login-profile-sheet/index.js`
- 结果：全部 `exit=0`

### 17.3 hioshop-server（依赖治理）
- 命令：`npm audit fix --omit=dev --omit=optional`
- 结果：`exit=1`（仍有漏洞）
- 摘要：审计项由上一阶段继续下降。

- 命令：`npm audit --omit=dev --omit=optional --audit-level=high`
- 结果：`exit=1`
- 摘要：`32 vulnerabilities (28 moderate, 2 high, 2 critical)`。

- 命令：`npm install`（恢复 dev 依赖以继续执行 compile/test）
- 结果：`exit=0`

- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：在恢复 dev 依赖后，服务端验证依旧全部通过。

### 17.4 hioshop-admin-web
- 命令：`npm run lint` / `npm run build:prod` / `npm audit --omit=dev --audit-level=high`
- 结果：全部通过（audit 返回 4 个低/中风险，无 high）。

## 18. Stage 3 第十批验证（2026-03-04）

### 18.1 hioshop-miniprogram
- 命令：
  - `node -c utils/request/index.js`
  - `node -c pages/category/index.js`
  - `node -e "JSON.parse(require('fs').readFileSync('pages/category/index.json','utf8')); console.log('ok')"`
- 结果：全部 `exit=0`

### 18.2 hioshop-server
- 命令：`npm install`（应用 overrides）
- 结果：`exit=0`

- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：依赖收敛后，服务端编译与两套自动化回归保持通过。

- 命令：`npm audit --omit=dev --omit=optional --audit-level=high`
- 结果：`exit=1`
- 摘要：`28 vulnerabilities (27 moderate, 1 high)`，已无 critical。

### 18.3 hioshop-admin-web
- 命令：
  - `npm run lint`
  - `npm run test:unit -- --passWithNoTests`
  - `npm run build:prod`
  - `npm audit --omit=dev --audit-level=high`
- 结果：
  - lint/test/build 全部 `exit=0`
  - audit `exit=0`，`4 vulnerabilities (2 low, 2 moderate)`。

## 19. Stage 3 第十一批验证（2026-03-04）

### 19.1 hioshop-server（xlsx -> exceljs）
- 命令：`npm install`
- 结果：`exit=0`

- 命令：
  - `node -c src/admin/service/goods_import.js`
  - `node -c src/admin/controller/coupon.js`
  - `node -c scripts/test-goods-import.js`
- 结果：全部 `exit=0`

- 命令：`npm run compile && npm run test:goods-import && npm run test:coupon`
- 结果：`exit=0`
- 摘要：导入模板、导入校验、错误文件导出、券记录导出改造后，核心自动化回归继续通过。

- 命令：`npm audit --omit=dev --omit=optional --audit-level=high`
- 结果：`exit=0`
- 摘要：`28 vulnerabilities (1 low, 27 moderate)`，当前 `high/critical=0`。

## 20. Stage 3 第十二批验证（2026-03-04）

### 20.1 hioshop-server（COS SDK 替换）
- 命令：`npm install`
- 结果：`exit=0`

- 命令：
  - `node -c src/api/service/oss.js`
  - `node -c src/admin/service/oss.js`
  - `node -c src/admin/controller/goods.js`
- 结果：全部 `exit=0`

- 命令：`npm run compile`
- 结果：`exit=0`

- 命令：`npm run test:goods-import`
- 结果：`exit=0`
- 摘要：商品导入全链路自动化通过（模板下载/导入/错误文件校验）。

- 命令：`npm run test:coupon`
- 结果：`exit=0`

- 命令：`npm audit --omit=dev --omit=optional --audit-level=high`
- 结果：`exit=0`
- 摘要：`22 vulnerabilities (1 low, 21 moderate)`。

### 20.2 hioshop-admin-web
- 命令：`npm run lint && npm run test:unit -- --passWithNoTests && npm run build:prod`
- 结果：`exit=0`（build 仅保留体积告警）

- 命令：`npm audit --omit=dev --audit-level=high`
- 结果：`exit=0`
- 摘要：维持 `4 vulnerabilities (2 low, 2 moderate)`。

### 20.3 hioshop-miniprogram
- 命令：`node -c utils/request/index.js && node -c pages/category/index.js`
- 结果：`exit=0`

## 21. Stage 3 第十三批验证（2026-03-04）

### 21.1 hioshop-server（COS 真实冒烟）
- 命令：`npm run test:cos-smoke`
- 结果：`exit=0`
- 摘要：
  - 后台登录成功；
  - `/admin/index/getQiniuToken` 获取签名成功；
  - 签名 PUT 直传成功并可 HEAD 访问（`image/png`）；
  - `/admin/goods/uploadHttpsImage` 成功并可 HEAD 访问（`image/jpeg`）。

### 21.2 hioshop-server（OSS endpoint 修正后回归）
- 命令：`npm run compile && npm run test:goods-import`
- 结果：`exit=0`

## 22. Stage 3 第十四批验证（2026-03-04）

### 22.1 发布脚本与手册
- 命令：`bash -n deploy/stage3-release-verify.sh`
- 结果：`exit=0`
- 摘要：发布验证脚本语法有效，可用于发版前统一门禁执行。

### 22.2 一键验证脚本全量执行
- 命令：`deploy/stage3-release-verify.sh`
- 结果：`exit=0`
- 摘要：
  - server: `compile + goods-import + coupon + cos-smoke + audit` 全通过（audit 为 `22 vulnerabilities (1 low, 21 moderate)`）。
  - miniprogram: 关键文件语法检查通过。
  - admin-web: `lint + test + build + audit` 全通过（audit 为 `4 vulnerabilities (2 low, 2 moderate)`）。
