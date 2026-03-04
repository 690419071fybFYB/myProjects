# Stage 3 Release Checklist

## 1) Release Scope
- `hioshop-server`: 安全加固、登录资料门禁、上传链路加固、Excel 导入导出重构、COS 客户端重构、依赖治理。
- `hioshop-miniprogram`: 登录资料弹窗流程收敛、请求层 `412` 联动、分类页左右滚动隔离。
- `hioshop-admin-web`: 生产禁用 mock、构建参数修复、lint 门禁恢复、依赖升级。
- 根目录报告：审查与验证记录更新。

## 2) Suggested Commit Order (By Repo)
1. `hioshop-server`
2. `hioshop-miniprogram`
3. `hioshop-admin-web`
4. root reports (`Remediation-Stage3-P0P1.md`, `Validation-Log.md`)

## 3) Commit Units

### 3.1 hioshop-server
- Working dir: `/Volumes/SAMSUNG/fyb/myProjects/hioshop-server`
- Stage command:
```bash
git add package.json package-lock.json
git add scripts/migrate-legacy-images-to-oss.js scripts/test-goods-import.js scripts/test-cos-smoke.js
git add src/admin src/api src/common
git rm src/admin/service/qiniu.js src/api/service/qiniu.js
```
- Recommended commit message:
```bash
git commit -m "feat(server): harden auth/upload/profile flows and modernize cos/excel pipeline"
```
- Mandatory verify before push:
```bash
npm run compile
npm run test:goods-import
npm run test:coupon
npm run test:cos-smoke
npm audit --omit=dev --omit=optional --audit-level=high
```

### 3.2 hioshop-miniprogram
- Working dir: `/Volumes/SAMSUNG/fyb/myProjects/hioshop-miniprogram`
- Stage command:
```bash
git add components/login-profile-sheet/index.js
git add components/login-profile-sheet/index.wxml
git add components/login-profile-sheet/index.wxss
git add pages/category/index.json
git add pages/ucenter/settings/index.js
git add utils/request/index.js utils/util.js
```
- Recommended commit message:
```bash
git commit -m "feat(miniprogram): simplify profile completion flow and isolate category scrolling"
```
- Mandatory verify before push:
```bash
node -c components/login-profile-sheet/index.js
node -c pages/category/index.js
node -c pages/ucenter/settings/index.js
node -c utils/request/index.js
node -c utils/util.js
```

### 3.3 hioshop-admin-web
- Working dir: `/Volumes/SAMSUNG/fyb/myProjects/hioshop-admin-web`
- Stage command:
```bash
git add package.json package-lock.json src/main.js .eslintrc.cjs .eslintignore
```
- Recommended commit message:
```bash
git commit -m "chore(admin): restore lint gate and harden prod build/runtime defaults"
```
- Mandatory verify before push:
```bash
npm run lint
npm run test:unit -- --passWithNoTests
npm run build:prod
npm audit --omit=dev --audit-level=high
```

### 3.4 root reports
- Working dir: `/Volumes/SAMSUNG/fyb/myProjects`
- Stage command:
```bash
git add Remediation-Stage3-P0P1.md Validation-Log.md Stage3-Release-Checklist.md deploy/stage3-release-verify.sh
```
- Recommended commit message:
```bash
git commit -m "docs: update stage3 remediation and verification runbook"
```

## 4) Release Gates
- Gate A: 三端验证全部通过（见 `deploy/stage3-release-verify.sh`）。
- Gate B: `hioshop-server` 的 `test:cos-smoke` 成功。
- Gate C: 小程序真机验证通过（iOS + Android）。
- Gate D: 预发布环境 smoke（登录、分类、下单、地址、订单、后台上传）通过。

## 5) Rollback Plan

### 5.1 Code rollback
- 每个仓库独立回滚，按提交粒度执行：
```bash
git revert <commit_sha>
```
- 建议回滚顺序：
1. `hioshop-miniprogram`
2. `hioshop-admin-web`
3. `hioshop-server`

### 5.2 Runtime fallback knobs
- 小程序：
  - `hioshop-miniprogram/config/api.js`
  - 可临时设置 `features.newUiV2=false`、`features.vantEnabled=false`，仅保留老 UI 路径。
- 服务端：
  - `hioshop-server/src/api/config/config.js`
  - 紧急时可将 `profileRequiredController` 与 `profileRequiredAction` 置空，临时关闭资料完整性门禁。

### 5.3 COS fallback
- 若新 COS SDK 线上异常：
1. 先回滚 `hioshop-server` 对应提交。
2. 立即执行 `npm run test:cos-smoke` 验证回滚结果。
3. 再恢复发布流量。

## 6) Post-release Checks
- 10 分钟内检查：
  - 登录成功率
  - 下单成功率
  - 头像上传成功率
  - 后台图片上传成功率
  - 订单接口 4xx/5xx 波动
- 30 分钟内检查：
  - COS 对象写入量是否与业务操作匹配
  - 服务端错误日志是否出现新增高频错误
