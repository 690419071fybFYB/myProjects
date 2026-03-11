# Cross-Generation Upgrade Tracker

## Batch 0 - Baseline and Rollback

- [x] Node 20 baseline aligned in CI and Docker.
- [x] Added `.nvmrc` for root/server/admin/miniprogram.
- [x] Added baseline/rollback scripts under `deploy/scripts/`.
- [x] Added compatibility contract document.

## Batch 1 - ThinkJS 4 alpha (Server)

- [x] Upgrade `thinkjs` and bootstrapping.
- [x] Remove legacy Babel runtime dependency from startup path.
- [x] Keep API compatibility and pass targeted security/coupon gate checks.

## Batch 2 - Vue3 + Vite (Admin Web)

- [x] Migrate to Vue 3 runtime with Vite build.
- [x] Upgrade router to v5 and introduce Pinia.
- [x] Replace Element UI with Element Plus and keep pages functional.
- [x] Add route-guard unit tests (auth redirect + permission gate + token header handling).
- [x] Remove `vue-quill-editor` and migrate to in-repo Quill2 compat component.
- [x] Remove `@vue/compat` and migrate Vue2 template syntax (`slot-scope/.sync/.native/slot`) to Vue3 syntax.

## Batch 3 - Miniprogram Major Upgrade

- [x] Upgrade `@vant/weapp` to latest stable (already latest in registry).
- [x] Validate request/auth compatibility with upgraded server.
- [x] Run smoke checks for key user paths.

## Batch 4 - ESLint 9 Unified Governance

- [x] Migrate all repos to ESLint 9 flat config.
- [x] Enforce error-blocking policy in CI.
- [x] Record warning backlog for phased cleanup.

## Batch 5 - Integration / Release / Acceptance

- [x] Execute full cross-end PR gate and nightly regression.
- [x] Capture release verification report.
- [x] Capture rollback evidence and residual-risk list.

Verification artifacts:
- `testing-artifacts/20260311-154428-pr-gate/pr-gate-report.md`
- `testing-artifacts/20260311-154433-nightly-full/nightly-report.md`
