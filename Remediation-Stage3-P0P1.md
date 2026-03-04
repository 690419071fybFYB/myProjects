# Stage 3 修复执行清单（P0/P1）

基于：
- `/Volumes/SAMSUNG/fyb/myProjects/Findings-HighRisk.md`
- `/Volumes/SAMSUNG/fyb/myProjects/Findings-Full.md`
- `/Volumes/SAMSUNG/fyb/myProjects/Dependency-Risk.md`

目标：把高优先级风险转成可直接执行、可回归、可上线的任务清单（按仓库/模块分组）。

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
