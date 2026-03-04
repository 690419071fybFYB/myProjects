# Dependency-Risk

审查时间：2026-03-04（Asia/Shanghai）

## 审查输入
- `hioshop-server`: `npm audit --omit=dev --audit-level=high` -> `77 vulnerabilities (3 low, 21 moderate, 31 high, 22 critical)`
- `hioshop-admin-web`: `npm audit --omit=dev --audit-level=high` -> `7 vulnerabilities (2 low, 2 moderate, 3 high)`
- `hioshop-miniprogram`: `npm audit --omit=dev --audit-level=high` -> `0 vulnerabilities`

## 分级结果（按可利用性+调用可达性）

### DEP-001
- id: `DEP-001`
- priority: `P1`
- repo: `hioshop-server`
- package: `koa <=2.16.3`（经 `thinkjs` 链路可达）
- impact: `存在 Host Header 注入、Open Redirect、XSS/正则复杂度问题，属于 Web 框架核心面风险。`
- evidence: `audit 报告标记 critical；服务端主框架为 thinkjs/koa 链路。`
- exploitability: `高（入口面广）`
- fix_recommendation: `规划 thinkjs/koa 升级窗口，先在预发布回归路由、中间件、异常处理。`
- confidence: `0.88`

### DEP-002
- id: `DEP-002`
- priority: `P1`
- repo: `hioshop-server`
- package: `jsonwebtoken <=8.5.1`
- impact: `历史算法/密钥处理缺陷可能导致 token 验签绕过风险放大。`
- evidence: `audit 报告 high；项目核心鉴权直接依赖 jsonwebtoken。`
- exploitability: `高（鉴权核心路径）`
- fix_recommendation: `升级到 9.x 并显式限制算法；同步改造签发/验签参数。`
- confidence: `0.92`

### DEP-003
- id: `DEP-003`
- priority: `P1`
- repo: `hioshop-server`
- package: `request/request-promise/form-data/hawk`（多项高危+已弃用链）
- impact: `SSRF、头部泄露、随机边界不安全等问题叠加，且链路维护停止。`
- evidence: `audit 中 form-data critical、hawk high、follow-redirects 高危等。`
- exploitability: `中-高（项目内广泛用于外部请求）`
- fix_recommendation: 逐步替换为 `undici` / `axios@latest` / `node-fetch`，并统一出站请求安全策略。
- confidence: `0.90`

### DEP-004
- id: `DEP-004`
- priority: `P2`
- repo: `hioshop-server`
- package: `xlsx@0.18.5`
- impact: `存在 Prototype Pollution/ReDoS，且当前 audit 显示 no fix。`
- evidence: `audit 标记 high 且 no fix；项目含商品导入链路。`
- exploitability: `中（取决于是否处理不可信 Excel）`
- fix_recommendation: `限制导入源可信范围+文件大小与结构校验；评估替代库或隔离解析服务。`
- confidence: `0.84`

### DEP-005
- id: `DEP-005`
- priority: `P2`
- repo: `hioshop-server`
- package: `moment <=2.29.3`
- impact: `路径遍历/正则复杂度漏洞，可能影响日期解析相关路径。`
- evidence: `audit 标记 high；项目多个控制器使用 moment。`
- exploitability: `中`
- fix_recommendation: `升级 moment 或迁移 dayjs/luxon，并回归格式化输出。`
- confidence: `0.78`

### DEP-006
- id: `DEP-006`
- priority: `P1`
- repo: `hioshop-admin-web`
- package: `axios@0.18.1 + follow-redirects`
- impact: `SSRF/凭据泄露/DoS 等问题，且该依赖用于后台全部 API 调用。`
- evidence: `audit high；package.json 固定 axios 0.18.1。`
- exploitability: `高（核心网络层）`
- fix_recommendation: `升级 axios 到 1.x，逐页回归拦截器、错误处理、上传下载流程。`
- confidence: `0.94`

### DEP-007
- id: `DEP-007`
- priority: `P2`
- repo: `hioshop-admin-web`
- package: `path-to-regexp@2.4.0`
- impact: `ReDoS 风险可影响前端路由匹配性能与稳定性。`
- evidence: `audit high；依赖在 package.json 显式声明。`
- exploitability: `中`
- fix_recommendation: `升级并验证路由兼容。`
- confidence: `0.80`

### DEP-008
- id: `DEP-008`
- priority: `P3`
- repo: `hioshop-admin-web`
- package: `vue@2.6.10 / quill`
- impact: `存在 ReDoS/XSS 公告，是否可达取决于具体输入与渲染路径。`
- evidence: `audit 给出 moderate/high；quill 仍有 no-fix 项。`
- exploitability: `中-低（需结合富文本输入路径）`
- fix_recommendation: `短期做输入净化与 CSP；中期评估 Vue 3 与编辑器替代迁移。`
- confidence: `0.73`

### DEP-009
- id: `DEP-009`
- priority: `P3`
- repo: `hioshop-miniprogram`
- package: `@vant/weapp`
- impact: `audit 未发现 npm 高危；当前依赖面较小。`
- evidence: `npm audit 返回 0 vulnerabilities。`
- exploitability: `低`
- fix_recommendation: `继续锁版本并在发布前做 npm audit。`
- confidence: `0.96`

## 升级路线（建议）
1. 第一优先（1-2 周）：`jsonwebtoken`、`axios`、生产 mock 移除、出站请求安全策略落地。
2. 第二优先（2-4 周）：request 生态替换、SSRF 白名单策略、xlsx 风险隔离。
3. 第三优先（4+ 周）：框架升级（thinkjs/koa、Vue2->3）与大版本回归。

## 不做“纯版本焦虑”说明
本报告仅保留“可达链路 + 业务可利用性”高的依赖项；未把所有 low/moderate 机械罗列为必须立即处理。
