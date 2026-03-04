# Stage 3 修复执行清单（P0/P1）

基于：
- `/Volumes/SAMSUNG/fyb/myProjects/Findings-HighRisk.md`
- `/Volumes/SAMSUNG/fyb/myProjects/Findings-Full.md`
- `/Volumes/SAMSUNG/fyb/myProjects/Dependency-Risk.md`

目标：把高优先级风险转成可直接执行、可回归、可上线的任务清单（按仓库/模块分组）。

## 执行进度（2026-03-04）
- `S-A1`：已完成（订单写链路归属校验）
- `S-A2`：已完成（测试支付入口下线）
- `S-B1`：已完成（API 默认鉴权 + 白名单放行，移除 address 公共白名单）
- `S-B2`：已完成（JWT secret 环境化 + expiresIn + 算法限制）
- `W-B3`：已完成（admin 生产禁用 mock 注入）
- `S-C1`：已完成（后台抓图 SSRF 防护：协议限制 + DNS/IP 拒绝内网 + 重定向校验 + MIME/体积限制）
- `S-C2`：已完成（管理员密码迁移 bcrypt，兼容旧 md5 并在登录时自动升级）
- `S-C3`：进行中（已升级 `jsonwebtoken` 到 9.x；`admin/api express`、`api/service/weixin`、`api/controller/auth|order|qrcode`、`admin/service/token`、`api/service/oss`、迁移脚本均已移除 `request/request-promise`；并已清理 `node-wget/jushuitan/gm/querystring/xml2js` 直依赖，`moment/nanoid` 已升级；当前剩余以 `thinkjs/cos-nodejs-sdk-v5/weixinpay/xlsx` 传递风险为主）
- `W-C4`：已完成（admin-web `axios` 升级到 1.x，构建脚本已兼容 Node 17+ OpenSSL）
- 构建验证：`hioshop-server npm run compile` 通过
- 构建验证：`hioshop-admin-web npm run build:prod` 通过（脚本已内置 OpenSSL 兼容参数）
- 依赖验证：`hioshop-server npm audit --omit=dev --audit-level=high` 收敛至 `58`；`hioshop-admin-web` 收敛至 `4`（无高危）

## 0. 执行原则
1. 先封堵可被直接利用的 P0（订单越权、测试支付入口），再做架构性 P1（统一鉴权、JWT、SSRF、口令存储）。
2. 每个任务必须包含：代码变更点、回归用例、上线门禁、回滚策略。
3. 采用小批次发布：每批次只覆盖同一风险域，避免联动回归爆炸。

## 1. 发布批次与顺序

### Batch A（当天热修）
- A1: 订单归属校验（HR-001, P0）
- A2: 下线测试支付接口（HR-002, P0）

### Batch B（1-3 天）
- B1: API 统一鉴权拦截（HR-003, P1）
- B2: JWT 安全改造（HR-004, P1）
- B3: 后台生产禁用 mock（HR-007, P1）

### Batch C（3-7 天）
- C1: SSRF 防护（HR-005, P1）
- C2: 管理员密码哈希迁移（HR-006, P1）
- C3: 高风险依赖修复第一波（DEP-002, DEP-006, DEP-003）

## 2. 可执行任务清单（按仓库/模块）

## 2.1 hioshop-server

### A1. 订单写链路归属校验（P0）
- task_id: `S-A1`
- source_findings: `HR-001`
- module: `api/order`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/controller/order.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/model/order.js`
- 实施步骤:
  1. 给 `getOrderHandleOption` 增加 `userId` 参数，并在 model 层按 `id + user_id` 查单。
  2. `delete/confirm/complete/update/express/cancel` 全部 where 条件统一加 `user_id`。
  3. `updateAction` 增加地址归属校验（address.id + user_id），并处理空对象返回 400/404。
  4. 对“订单不存在”和“无权限访问”统一错误码与文案（推荐 404/403）。
- 回归用例:
  1. A token + B orderId：删除/确认/改地址/物流查询全部失败。
  2. A token + A orderId：合法状态可成功。
  3. 无 token：相关接口返回统一未登录错误。
- 门禁:
  - `curl` 探测不再出现匿名进入业务分支。
- 回滚策略:
  - 保留旧逻辑分支 tag，若线上误伤可按 action 级别回退（不回退统一鉴权）。
- 预估: `1 人日`

### A2. 关闭测试支付入口 preWeixinPaya（P0）
- task_id: `S-A2`
- source_findings: `HR-002`
- module: `api/pay`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/controller/pay.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/common/config/router.js`（若有显式映射）
- 实施步骤:
  1. 生产环境彻底移除 `preWeixinPayaAction` 暴露路径。
  2. 若必须保留测试能力，仅允许非生产 + 管理员白名单 + 审计日志。
  3. 检查小程序端仅使用 `preWeixinPay`。
- 回归用例:
  1. `/api/pay/preWeixinPaya` 在生产返回 404/403。
  2. `/api/pay/preWeixinPay` 正常可用。
- 门禁:
  - 线上 smoke 中禁止出现 `preWeixinPaya` 可达。
- 回滚策略:
  - 回退到“环境变量开关”版本，不回退到全开放。
- 预估: `0.5 人日`

### B1. API 统一鉴权拦截（P1）
- task_id: `S-B1`
- source_findings: `HR-003`（关联 `FULL-010`）
- module: `api/base + 白名单配置`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/controller/base.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/config/config.js`
- 实施步骤:
  1. 在 `__before` 实现“默认鉴权，白名单放行”。
  2. 控制器/Action 匹配统一小写，避免大小写绕过。
  3. 非白名单未登录统一返回 `401`。
  4. 同步梳理现有 publicAction/publicController，删除不必要公开项。
- 回归用例:
  1. `order/list` 未登录应 401。
  2. `index/catalog/goods/region` 等公开接口匿名可用。
- 门禁:
  - 全部 API 错误码一致性检查通过（最少覆盖登录、订单、资料、优惠券）。
- 回滚策略:
  - 白名单回滚（按路径级增补），不回退到“全局不拦截”。
- 预估: `1 人日`

### B2. JWT 密钥与过期策略改造（P1）
- task_id: `S-B2`
- source_findings: `HR-004`, `DEP-002`
- module: `api/admin token service`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/api/service/token.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/service/token.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/common/config/config*.js`
- 实施步骤:
  1. secret 改为环境变量（区分 api/admin）。
  2. `jwt.sign` 增加 `expiresIn`（例如 7d / 12h，按业务定）。
  3. `jwt.verify` 显式限制算法，拒绝弱算法回退。
  4. 引入 token 版本戳或黑名单机制（最小实现可先做版本戳）。
- 回归用例:
  1. 过期 token 被拒绝。
  2. 正常 token 在有效期内可访问。
  3. 密钥轮换后旧 token 失效符合预期。
- 门禁:
  - 配置中心中不再出现硬编码 secret。
- 回滚策略:
  - 双密钥短期兼容窗口（old+new verify，新签发只用 new）。
- 预估: `1-1.5 人日`

### C1. 后台抓图 SSRF 防护（P1）
- task_id: `S-C1`
- source_findings: `HR-005`, `DEP-003`
- module: `admin/goods + admin/oss`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/controller/goods.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/service/oss.js`
- 实施步骤:
  1. 仅允许 `https`，禁止 `http/file/gopher` 等协议。
  2. URL 解析后做 DNS/IP 校验：拒绝内网、回环、链路本地、保留地址段。
  3. `strictSSL=true`，限制重定向次数并校验重定向目标。
  4. 限制最大响应体与 MIME 白名单（仅图片）。
  5. 增加审计日志：请求人、目标域名、结果。
- 回归用例:
  1. `127.0.0.1`、`169.254.169.254`、私网网段均拒绝。
  2. 白名单 CDN 图片可成功上传。
- 门禁:
  - SSRF 用例集全部通过。
- 回滚策略:
  - 仅回滚白名单，不关闭整套校验。
- 预估: `1.5 人日`

### C2. 管理员密码哈希迁移（P1）
- task_id: `S-C2`
- source_findings: `HR-006`
- module: `admin/auth + admin/admin`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/controller/auth.js`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/controller/admin.js`
  - （可新增）`/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/src/admin/service/password.js`
- 实施步骤:
  1. 新增 bcrypt/argon2 哈希服务。
  2. 新创建管理员改为强哈希。
  3. 登录时兼容旧 md5：验证成功后立即升级为新哈希（渐进迁移）。
  4. 移除固定盐生成逻辑。
- 回归用例:
  1. 新管理员可登录。
  2. 老管理员首次登录后自动升级并继续可登录。
  3. 错误密码稳定失败。
- 门禁:
  - 数据库中新增管理员密码不再是 md5 格式。
- 回滚策略:
  - 保留 md5 校验兜底一个发布周期。
- 预估: `2 人日`

### C3. 高风险依赖修复第一波（P1）
- task_id: `S-C3`
- source_findings: `DEP-002`, `DEP-003`
- module: `server dependencies`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server/package.json`
  - 相关调用代码（request -> 新 HTTP 客户端）
- 实施步骤:
  1. 升级 `jsonwebtoken` 到 9.x 并改 verify 参数。
  2. 将关键外部请求路径（支付、微信、抓图）逐步从 `request` 迁移。
  3. 建立统一 HTTP 客户端封装（超时、重试、域名策略）。
- 回归用例:
  1. 登录、手机号、支付、物流查询均通过回归。
- 门禁:
  - `npm audit --audit-level=high` 风险数量显著下降。
- 回滚策略:
  - 采用模块级灰度切换，不做一次性全量替换。
- 预估: `3-5 人日`

## 2.2 hioshop-admin-web

### B3. 生产禁用 mock 注入（P1）
- task_id: `W-B3`
- source_findings: `HR-007`
- module: `bootstrap/main`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-admin-web/src/main.js`
- 实施步骤:
  1. 删除 `NODE_ENV=production` 下的 `mockXHR()` 调用。
  2. mock 仅允许开发态显式开关（例如 `VUE_APP_ENABLE_MOCK=true`）。
  3. CI 增加静态扫描，防止生产入口再次注入 mock。
- 回归用例:
  1. 生产构建后网络请求全部命中真实后端。
  2. 开发环境按开关可继续使用 mock。
- 门禁:
  - 打包产物中不含 mock 注入代码路径。
- 回滚策略:
  - 回滚到“开发开关”模式，不恢复生产默认 mock。
- 预估: `0.5 人日`

### C4. 管理后台网络层高危依赖升级（P1）
- task_id: `W-C4`
- source_findings: `DEP-006`
- module: `axios/network`
- 目标文件:
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-admin-web/package.json`
  - `/Volumes/SAMSUNG/fyb/myProjects/hioshop-admin-web/src/config/*`
- 实施步骤:
  1. 升级 axios 至 1.x 并验证拦截器行为。
  2. 梳理上传、下载、鉴权 header 注入兼容性。
  3. 回归登录、商品、订单、分类、权限页面核心请求。
- 回归用例:
  1. 全核心页面 CRUD 正常。
  2. 401/403 处理符合预期。
- 门禁:
  - audit 中 axios/follow-redirects 高危告警清除。
- 回滚策略:
  - 保留 axios 0.x 分支热修兜底。
- 预估: `1-2 人日`

## 3. 联调与验收门禁（全局）

1. 安全门禁：
- 未登录访问非白名单 API 必须 401。
- 非本人订单 ID 访问必须失败。
- `preWeixinPaya` 生产不可达。
- SSRF 样例地址全部拒绝。

2. 业务门禁：
- 小程序：登录/资料完善/下单/订单列表/地址管理可用。
- 后台：登录、商品、分类、订单核心流程可用。

3. 工程门禁：
- server `compile` 通过。
- admin `build:prod` 在固定 Node LTS 环境可通过。
- 回归脚本和 `Validation-Log` 更新为最新结果。

## 4. 建议排期（可直接派单）
1. D0：`S-A1` + `S-A2`。
2. D1-D2：`S-B1` + `S-B2` + `W-B3`。
3. D3-D5：`S-C1` + `S-C2`。
4. D5+：`S-C3` + `W-C4`（依赖升级专项）。

## 5. 交付物与状态模板

每个任务提交时附：
- PR 链接
- 变更文件列表
- 回归结果（通过/失败+截图或日志）
- 风险说明与回滚点

推荐状态：`TODO -> IN_PROGRESS -> IN_REVIEW -> VERIFIED -> RELEASED`。

## 12. Stage 3 持续推进增量（2026-03-04，第四批）

### 12.1 服务端支付依赖替换（S-C3 继续）
- 变更：
  - `hioshop-server/src/api/service/weixin.js`
    - 移除 `weixinpay` 调用，改为官方统一下单接口 `pay/unifiedorder` 的直连实现（HTTP + MD5 签名 + XML 编解码）。
    - 保持返回字段兼容（`appid/timeStamp/nonceStr/package/signType/paySign`）。
    - 增加 access_token 内存缓存与过期前保护窗口，手机号获取在 token 失效时自动重试一次。
  - `hioshop-server/src/admin/service/token.js`
    - 增加 access_token 内存缓存，减少重复请求与瞬时失败概率。
- 依赖：
  - `hioshop-server/package.json` 移除 `weixinpay`。

### 12.2 商品详情输入安全加固（后台录入 + 批量导入）
- 新增：
  - `hioshop-server/src/common/utils/sanitize_html.js`
    - 对富文本进行标签与属性白名单清洗，禁止危险协议与标签。
- 接入点：
  - `hioshop-server/src/admin/controller/goods.js`（单品保存）
  - `hioshop-server/src/admin/service/goods_import.js`（批量导入）
- 目标：
  - 后台写入 `goods_desc` 前统一清洗，降低富文本 XSS 注入风险。

### 12.3 小程序登录弹窗稳定性优化
- 变更：
  - `hioshop-miniprogram/components/login-profile-sheet/index.wxml|js|wxss`
    - 移除“微信一键填充昵称头像”路径（避免回填 `微信用户` 的误导行为）。
    - 头像区域改为 `open-type="chooseAvatar"`，直接支持微信头像/上传头像。
    - 头像上传本地兜底从 `chooseMedia` 切换为兼容性更高的 `chooseImage`。
    - 昵称输入框保留 `type="nickname"`，直接触发微信昵称选择；仅保留昵称+手机号两项必填。

### 12.4 当前收敛状态
- `S-C3`：持续推进中，`weixinpay` 已清理完成，`request` 仅剩 `cos-nodejs-sdk-v5` 传递依赖。
- 输入安全：`goods_desc` 的主要写入链路已完成服务端收口。
- 小程序登录体验：去除冗余入口并提升头像/昵称/手机号采集可用性。

### 12.5 批量导入稳态防护补充
- 变更：`hioshop-server/src/admin/controller/goods.js`
  - 新增导入文件校验：
    - 文件不能为空
    - 文件大小上限 `5MB`
    - MIME 类型白名单 + `.xlsx` 后缀双重校验
- 目标：
  - 降低异常大文件与伪造文件造成的解析风险与性能抖动。

## 13. Stage 3 持续推进增量（2026-03-04，第五批）

### 13.1 API 输入校验与上传防护加固
- 新增：
  - `hioshop-server/src/common/utils/validate.js`
    - 通用输入清洗与校验：文本清洗、手机号、微信 code、base64 形态、头像 URL 白名单。
- 接入：
  - `hioshop-server/src/api/controller/auth.js`
    - `loginByWeixin` 增加 code 合法性校验与微信请求异常兜底。
    - `phoneNumber` 增加 code/base64 参数格式校验，手机号结果二次校验。
  - `hioshop-server/src/api/controller/settings.js`
    - 登录态强校验；昵称/手机号输入校验；头像 URL 白名单处理；昵称解码容错。
  - `hioshop-server/src/api/controller/upload.js`
    - 头像上传增加登录态校验、空文件/大小上限（5MB）校验、MIME+后缀双重白名单。

### 13.2 小程序设置页与登录弹窗一致化
- 变更：
  - `hioshop-miniprogram/pages/ucenter/settings/index.js`
    - 头像上传失败回滚到旧头像并提示。
    - 手机号改为必填且统一 `^1[3-9]\d{9}$` 校验。
    - 保存成功提示从错误提示改为成功提示。
  - `hioshop-miniprogram/components/login-profile-sheet/index.js`
    - 清理冗余 `profileAuthorized` 状态，降低组件复杂度。

### 13.3 当前效果
- 登录资料链路在前后端均增加参数边界与异常兜底。
- 头像上传失败、手机号格式异常等场景行为更可控。

## 14. Stage 3 持续推进增量（2026-03-04，第六批）

### 14.1 依赖锁状态恢复与审计收敛
- 问题：此前中断导致 `hioshop-server` 的 `package.json` override 与 `package-lock.json` 未完全同步。
- 处理：
  - 使用 `npm install --force` 完成 lock 同步。
  - `fast-xml-parser` 已被提升至 `4.5.4`（经 `npm ls fast-xml-parser` 验证）。
- 结果：
  - server 审计继续下降：`51 vulnerabilities (1 low, 16 moderate, 16 high, 18 critical)`。
  - `request` 仍仅来自 `cos-nodejs-sdk-v5` 传递依赖。

### 14.2 OSS 抓图链路 SSRF 防护对齐
- 变更：`hioshop-server/src/api/service/oss.js`
- 内容：
  - 对齐 `admin/service/oss.js` 的安全策略：
    - 强制 `https`
    - 主机名与私网/回环 IP 拦截
    - DNS 解析后 IP 风险校验
    - 重定向逐跳校验
    - 内容类型必须为图片
    - 响应体大小上限（默认 10MB）
- 目标：
  - 消除 API 侧抓图能力与后台抓图能力的安全策略差异。

### 14.3 admin-web 工程门禁可执行性修复
- 变更：
  - `hioshop-admin-web/package.json`
    - 新增 `eslint` 开发依赖
    - `lint` 调整为 `eslint --ext .js src`
  - 新增：
    - `hioshop-admin-web/.eslintrc.cjs`
    - `hioshop-admin-web/.eslintignore`
- 结果：
  - `npm run lint` 恢复可执行并通过。

### 14.4 小程序状态
- 当前仅完成代码级与语法级验证；真机授权链路（微信昵称/手机号弹窗）仍需你本地真机点测确认。

## 15. Stage 3 持续推进增量（2026-03-04，第七批）

### 15.1 文件类型防伪增强
- 变更：`hioshop-server/src/api/controller/upload.js`
  - 头像上传新增文件头（magic bytes）校验，支持 JPEG/PNG/GIF/WEBP。
  - 在 MIME/后缀校验基础上再做内容签名校验，降低伪装文件上传风险。

- 变更：`hioshop-server/src/admin/controller/goods.js`
  - 商品导入新增 xlsx 文件头校验（ZIP 头），防止仅改扩展名绕过。

### 15.2 依赖与工程门禁进展
- `hioshop-server`
  - override 生效后，`fast-xml-parser` 已固定在 `4.5.4`。
  - 高危审计继续下降（当前 51）。
- `hioshop-admin-web`
  - lint 门禁恢复可执行：新增 eslint 与基础配置。
  - `lint/test(build no tests)/build` 均可执行通过。

### 15.3 仍需后续专项处理
- server 剩余高危主要聚焦于 legacy 框架链与 `request` 传递依赖（`cos-nodejs-sdk-v5`）。
- 彻底清零需要框架代际升级或对象存储 SDK 替换专项。

## 16. Stage 3 持续推进增量（2026-03-04，第八批）

### 16.1 移除未使用七牛链路
- 变更：
  - 删除：
    - `hioshop-server/src/admin/service/qiniu.js`
    - `hioshop-server/src/api/service/qiniu.js`
  - 依赖移除：`hioshop-server/package.json` 删除 `qiniu`
- 依据：
  - 全仓库检索无控制器调用 `service('qiniu')`，当前生产链路已迁移 OSS。

### 16.2 审计口径澄清
- 因 macOS 可选依赖（`fsevents`）会放大审计噪音，增加一条“去可选依赖口径”用于稳定比较：
  - `npm audit --omit=dev --omit=optional --audit-level=high`
- 当前该口径结果：
  - `42 vulnerabilities (14 moderate, 11 high, 17 critical)`
- 结论：
  - 主要剩余风险仍集中在 legacy 框架链（thinkjs/koa/babel）与 `cos-nodejs-sdk-v5 -> request`。

## 17. Stage 3 持续推进增量（2026-03-04，第九批）

### 17.1 资料完整性门禁服务端化
- 新增：`hioshop-server/src/common/utils/profile.js`
  - `isProfileComplete`（昵称+手机号）统一判定。
- 接入：
  - `hioshop-server/src/api/controller/base.js`
    - 对 `order/address/footprint` 及 `cart/checkout` 增加资料完整性门禁。
    - 未完善资料时返回 `412`（请先完善登录资料）。
  - `hioshop-server/src/api/config/config.js`
    - 新增 `profileRequiredController/profileRequiredAction` 配置。
- 价值：
  - 即使客户端绕过，也无法直接调用受限接口。

### 17.2 地址接口参数校验收敛
- 变更：`hioshop-server/src/api/controller/address.js`
  - 新增姓名、手机号、省市区ID、详细地址、地址ID严格校验。
  - 清理无用依赖与冗余语句。
- 价值：
  - 降低脏数据写入和异常参数导致的行为不确定性。

### 17.3 小程序请求层统一拦截 `412`
- 变更：
  - `hioshop-miniprogram/utils/request/index.js`
  - `hioshop-miniprogram/utils/util.js`
- 行为：
  - 当后端返回 `errno=412` 时，统一 toast 并跳转“我的”页面。
- 价值：
  - 与服务端资料门禁形成闭环，减少页面级重复处理。

### 17.4 依赖治理进一步收敛
- 执行：`hioshop-server npm audit fix --omit=dev --omit=optional`（非 force）。
- 结果：
  - 审计口径 `--omit=dev --omit=optional --audit-level=high` 收敛到：
    - `32 vulnerabilities (28 moderate, 2 high, 2 critical)`
  - 主要剩余集中在：
    - `cos-nodejs-sdk-v5 -> request/form-data/tough-cookie/qs`
    - `thinkjs` 生态链（`ms/xml2js/validator`）
    - `xlsx`（无可用修复）

## 18. Stage 3 持续推进增量（2026-03-04，第十批）

### 18.1 小程序登录态与资料态一致性修复
- 变更：`hioshop-miniprogram/utils/request/index.js`
  - `refreshTokenByWeixin` 改为统一调用 `session.saveSession`，不再手工写 `token/userInfo`。
  - `clearSession` 改为统一调用 `session.clearSession`。
- 价值：
  - 解决 token 刷新后 `profileCompleted` 可能不同步导致误拦截的问题。

### 18.2 分类页滚动区域隔离
- 变更：`hioshop-miniprogram/pages/category/index.json`
  - 新增 `"disableScroll": true`，禁用页面级滚动，只保留左右区域各自滚动。
- 价值：
  - 右侧商品区滑动时，左侧分类导航不再整体跟随页面位移，交互更稳定。

### 18.3 服务端依赖高危再收敛
- 变更：`hioshop-server/package.json`（overrides）
  - 新增：
    - `validator@^13.15.26`
    - `xml2js@^0.6.2`
    - `form-data@^2.5.4`
    - `qs@^6.14.1`
- 结果（稳定口径）：
  - `npm audit --omit=dev --omit=optional --audit-level=high`
  - 从 `32 vulnerabilities (28 moderate, 2 high, 2 critical)` 下降到：
    - `28 vulnerabilities (27 moderate, 1 high)`
- 当前剩余高危：
- `xlsx`（无官方可用修复版本；已通过导入大小限制、魔数校验、行数上限等措施降低利用面）。

## 19. Stage 3 持续推进增量（2026-03-04，第十一批）

### 19.1 移除服务端 `xlsx` 高危链路
- 变更：
  - `hioshop-server/src/admin/service/goods_import.js`
    - 读写 Excel 全部改为 `exceljs`（模板导出、导入校验、错误文件导出）。
  - `hioshop-server/src/admin/controller/goods.js`
    - 导出模板改为 `await service.getTemplateBuffer()`（异步安全调用）。
  - `hioshop-server/src/admin/controller/coupon.js`
    - 券记录导出改为 `exceljs` 生成 xlsx。
  - `hioshop-server/scripts/test-goods-import.js`
    - 自动化脚本同步改为 `exceljs`。
  - `hioshop-server/package.json`
    - 移除 `xlsx`，新增 `exceljs`；
    - 继续通过 `overrides` 固定 `minimist` 以消除 `exceljs` 传递链路 critical。

### 19.2 风险收敛结果
- 审计口径：`npm audit --omit=dev --omit=optional --audit-level=high`
- 收敛结果：
  - 从上一批 `28 vulnerabilities (1 low, 27 moderate, 1 high)` 进一步到：
  - `28 vulnerabilities (1 low, 27 moderate)`（`high/critical = 0`）

### 19.3 兼容性验证
- 服务端 `compile + test:goods-import + test:coupon` 全量通过。
- 商品批量导入链路（模板下载、预检、导入、重复SKU跳过、错误文件下载）实测通过。
- 券记录导出链路保持可用（编译与冒烟通过）。

## 20. Stage 3 持续推进增量（2026-03-04，第十二批）

### 20.1 移除 `cos-nodejs-sdk-v5` 依赖链
- 变更：
  - `hioshop-server/src/api/service/oss.js`
  - `hioshop-server/src/admin/service/oss.js`
  - `hioshop-server/package.json`
- 内容：
  - OSS 客户端由 `cos-nodejs-sdk-v5` 切换为 AWS SDK v3 的 S3 兼容实现：
    - `@aws-sdk/client-s3`
    - `@aws-sdk/s3-request-presigner`
  - 保留现有行为：
    - 生成 PUT 直传签名 URL（10 分钟有效）
    - 服务端本地文件上传
    - 远程 HTTPS 图片抓取并上传
  - 强化配置校验：`region/bucket/accessKeyId/accessKeySecret` 缺一即报错。

### 20.2 风险收敛结果
- 审计口径：`npm audit --omit=dev --omit=optional --audit-level=high`
- 收敛：
  - 由上一批 `28 vulnerabilities (1 low, 27 moderate)` 下降到：
  - `22 vulnerabilities (1 low, 21 moderate)`
- 说明：
  - `request/tough-cookie/ajv` 相关链路已从生产依赖中清除。
  - 当前剩余主要为 ThinkJS 生态历史依赖（如 `ms`）和 `brace-expansion`。

### 20.3 回归验证
- 服务端 `compile + test:goods-import + test:coupon` 继续全通过。
- 管理端 `lint/test/build` 与审计口径复测保持稳定。
- 小程序变更点（资料态同步、分类页滚动隔离）语法检查通过。

## 21. Stage 3 持续推进增量（2026-03-04，第十三批）

### 21.1 真实 COS 冒烟脚本化
- 新增脚本：
  - `hioshop-server/scripts/test-cos-smoke.js`
  - `hioshop-server/package.json` 新增命令：`test:cos-smoke`
- 覆盖链路：
  - 后台登录获取 token
  - 获取 COS PUT 直传签名（`/admin/index/getQiniuToken`）
  - 使用签名 URL 直传 1x1 PNG
  - 回查文件 URL 可访问（HEAD）
  - 调用远程 HTTPS 抓图上传（`/admin/goods/uploadHttpsImage`）
  - 回查抓图上传产物可访问（HEAD）

### 21.2 真环境验证结论
- 本机实际执行结果：`npm run test:cos-smoke` 通过。
- 关键输出：
  - 签名上传 host：`fybshopbk-1369967353.cos.ap-shanghai.myqcloud.com`
  - 签名直传文件可访问（`image/png`）
  - 远程抓图上传文件可访问（`image/jpeg`）
- 结论：
  - 当前 COS 签名与上传链路在真实运行环境可用，AWS SDK S3 兼容实现满足腾讯 COS 使用场景。

## 22. Stage 3 持续推进增量（2026-03-04，第十四批）

### 22.1 发布与回滚手册落地
- 新增：
  - `Stage3-Release-Checklist.md`
  - `deploy/stage3-release-verify.sh`
- 内容：
  - 按仓库拆分提交单元（server/miniprogram/admin/docs）。
  - 每个提交单元包含推荐 `git add` 与 `git commit` 命令。
  - 发布 gate、回滚顺序、运行时兜底开关、发布后观察项。

### 22.2 一键验证入口
- `deploy/stage3-release-verify.sh` 聚合了三端关键门禁命令：
  - server: `compile + goods-import + coupon + cos-smoke + audit`
  - miniprogram: 关键文件语法检查
  - admin-web: `lint + test + build + audit`
- 作用：
  - 在发版前与回滚后可快速复跑同一套基线，降低人工遗漏风险。

### 22.3 脚本实跑结果
- 已执行：`deploy/stage3-release-verify.sh`
- 结果：全流程通过，输出 `Stage 3 release verification passed.`
