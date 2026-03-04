# Pre-Release Smoke Report

- Execution time: `2026-03-04 18:51 CST`
- Executor: Codex automated run
- Command: `deploy/stage3-release-verify.sh`
- Log file: `/Volumes/SAMSUNG/fyb/myProjects/deploy/logs/stage3-smoke-20260304-185157.log`

## 1) Overall Result
- Status: **PASS**
- Evidence: log line `448` contains `Stage 3 release verification passed.`

## 2) Automated Scenarios

### 2.1 Server (`hioshop-server`)
- Goods import full chain: **PASS**
  - Evidence lines: `88-95` (`[PASS]` x8)
- Coupon/order/address chain smoke: **PASS**
  - Evidence line: `109` (`Coupon 模块自动化冒烟通过。`)
- COS signed upload + remote fetch upload: **PASS**
  - Evidence line: `123` (`COS 冒烟通过。`)
- Security gate (`audit` high threshold): **PASS**
  - Evidence line: `213` (`22 vulnerabilities (1 low, 21 moderate)`, no high/critical)

### 2.2 Mini Program (`hioshop-miniprogram`)
- Syntax gate (changed key files): **PASS**
  - Evidence line: `220` (`[2/3] Verify hioshop-miniprogram`), script continued without failure.

### 2.3 Admin Web (`hioshop-admin-web`)
- Lint: **PASS**
- Unit test (no test files present): **PASS**
  - Evidence line: `231` (`No tests found, exiting with code 0`)
- Production build: **PASS with warnings**
  - Evidence line: `237` (`Compiled with 2 warnings`)
- Security gate (`audit` high threshold): **PASS**
  - Evidence line: `441` (`4 vulnerabilities (2 low, 2 moderate)`, no high)

## 3) Known Warnings (Non-blocking)
- Admin build bundle-size warnings remain (large JS/CSS assets).
- Browserslist update reminder appears during admin build/test.
- Remaining vulnerabilities are low/moderate only; no high/critical in release gate scope.

## 4) Manual/Device Checks Still Required
- Mini Program real-device check (iOS + Android):
  - 登录资料弹窗（头像/昵称/手机号）实际授权行为
  - 分类页左右独立滚动手感与稳定性
  - 412 拦截并跳转“我的”页
- WeChat real payment chain:
  - 真机下 `preWeixinPay -> 支付 -> 回调 -> 订单状态` 完整闭环

## 5) Release Recommendation
- Current automated pre-release smoke is green and can proceed to pre-production rollout.
- Require manual device checks above before full production rollout.
