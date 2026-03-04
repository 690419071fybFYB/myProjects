# Stage 3 Release Snapshot

- Generated at: `2026-03-04 18:48:46 CST`
- Scope: `hioshop-server` + `hioshop-miniprogram` + `hioshop-admin-web` + root release docs.

## 1) Published Commits
- `hioshop-server` (`master`): `4f4d4d2d7de5b97e5e5060504dda377eceb04544`
  - message: `feat(server): harden auth/upload/profile flows and modernize cos/excel pipeline`
- `hioshop-miniprogram` (`master`): `340086eaf51780afe905db342cc797e6954d74c1`
  - message: `feat(miniprogram): simplify profile completion flow and isolate category scrolling`
- `hioshop-admin-web` (`main`): `8481b569d2d277bba355915f17dc252b74e0302a`
  - message: `chore(admin): restore lint gate and harden prod build/runtime defaults`
- root (`main`): `b321a804f784a5b757809def9306b9a8dbc291fe`
  - message: `docs: update stage3 remediation, verification runbook, and release snapshot`

## 2) Push Status
- `hioshop-server`: pushed to `origin/master`
- `hioshop-miniprogram`: pushed to `origin/master`
- `hioshop-admin-web`: pushed to `origin/main`
- root: pushed to `origin/main`
- Current state: all repos `working tree clean`, no local ahead commits.

## 3) Verification Baseline (Executed)
- One-shot verify script: `deploy/stage3-release-verify.sh` passed.
- Server checks passed:
  - `npm run compile`
  - `npm run test:goods-import`
  - `npm run test:coupon`
  - `npm run test:cos-smoke`
  - `npm audit --omit=dev --omit=optional --audit-level=high`
- Miniprogram checks passed:
  - syntax checks on key changed JS files
- Admin checks passed:
  - `npm run lint`
  - `npm run test:unit -- --passWithNoTests`
  - `npm run build:prod`
  - `npm audit --omit=dev --audit-level=high`

## 4) Current Risk Summary
- `hioshop-server`: `22 vulnerabilities (1 low, 21 moderate)`, no high/critical.
- `hioshop-admin-web`: `4 vulnerabilities (2 low, 2 moderate)`, no high.
- `hioshop-miniprogram`: client-side package audit未单独执行（当前以语法+联调回归为准）。

## 5) Operational Notes
- COS path validated in real environment:
  - signed PUT upload success
  - remote HTTPS fetch-upload success
  - uploaded objects accessible via HEAD
- Release checklist and rollback runbook:
  - `Stage3-Release-Checklist.md`
  - `deploy/stage3-release-verify.sh`
