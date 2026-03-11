# Cross-Generation Upgrade Report

## 1) Delivered Changes

### Root / CI / Release Safety

- Unified Node runtime baseline to `20` via `.nvmrc` in root and all subrepos.
- Updated CI to Node 20 for admin and miniprogram jobs.
- Added baseline and rollback tooling:
  - `deploy/scripts/create_upgrade_baseline_tags.sh`
  - `deploy/scripts/build_upgrade_baseline_artifacts.sh`
  - `deploy/scripts/rollback_to_upgrade_baseline.sh`
- Added compatibility contract:
  - `upgrade-compat-contract.md`

### `hioshop-server` (ThinkJS 3 -> 4 alpha)

- Upgraded `thinkjs` to `4.0.0-alpha.0`.
- Replaced legacy transpiler startup with shared bootstrap:
  - `bootstrap.js`
  - updated `development.js` / `production.js`
- Replaced Babel compile script with Node20 compile utility:
  - `scripts/compile.js`
  - `npm run compile` now validates runtime compile path (no Babel dependency).
- Introduced ESLint 9 flat config:
  - `eslint.config.cjs`
  - updated lint scripts.

### `hioshop-admin-web` (Vue2/CLI -> Vue3 + Vite)

- Migrated build toolchain from Vue CLI to Vite:
  - `vite.config.js`
  - new root `index.html` (removed legacy `public/index.html`).
- Upgraded runtime stack:
  - Vue 3
  - Vue Router 5
  - Pinia (introduced session store for route auth state sync)
  - Element Plus
- Updated app entry:
  - `src/main.js` now uses `createApp`, Pinia, Element Plus, router guard integration.
- Updated router implementation to modern Router API (compatible with Router 5):
  - `src/router/index.js`
  - `src/router/guards.js` (shared guard logic for testability and router5-style return guards)
  - `src/router/guards.spec.js` (TDD regression cases for auth/permission guard behavior)
- Replaced legacy `vue-quill-editor` dependency with in-repo Quill2 compat layer:
  - `src/components/Common/QuillEditorCompat.vue`
  - `src/components/Common/quill-utils.js`
  - `src/components/Common/quill-utils.spec.js`
  - adapted consumers: `src/components/Goods/GoodsAddPage.vue`, `src/components/Goods/new_file.vue`
- Updated env model for frontend runtime:
  - `.env.development`
  - `.env.staging`
  - `.env.production`
  - `src/config/api.js` supports `VITE_ADMIN_API_ROOT`.
- Removed Vue2 compatibility bridge and completed syntax migration to Vue3 template conventions:
  - removed `@vue/compat` dependency and Vite compat compiler mode
  - replaced legacy slot/事件/双向绑定语法（`slot-scope`、`slot=""`、`.sync`、`.native`）为 Vue3 写法
  - upgraded `GoodsPickerDialog` to Vue3 `v-model` contract (`modelValue` / `update:modelValue`)
  - replaced `this.$set` / `this.$delete` in selector drawer with Vue3 reactive assignments
- Migrated to ESLint 9 flat config:
  - `eslint.config.cjs`

### `hioshop-miniprogram` (native major uplift baseline)

- Added Node20 baseline and ESLint 9 flat config:
  - `.nvmrc`
  - `eslint.config.cjs`
- Added lint/syntax gate scripts:
  - `npm run lint`
  - `npm run test:syntax`
  - `npm run test:request-smoke`

### Dependency Drift Control (latest stable + compatibility-first)

- Upgraded compatible packages to latest stable where low-risk:
  - `hioshop-server`: `dotenv` -> `^17.3.1`, `globals` -> `^17.4.0`, `mime-types` -> `^3.0.2`, `bcryptjs` -> `^3.0.3`
  - `hioshop-server`: removed unused dependencies `nanoid`, `pinyin` (code-side dead import cleaned)
  - `hioshop-admin-web`: `globals` -> `^17.4.0`, `jquery` -> `^4.0.0`, `cropperjs` -> `^2.1.0`
  - `hioshop-admin-web`: `vue-router` -> `^5.0.3`
  - `hioshop-admin-web`: removed `@vue/compat` (switched to native Vue3 runtime path)
  - `hioshop-admin-web`: removed `vue-quill-editor` (dropped transitive `quill@1.3.7`)
  - `hioshop-admin-web`: removed `vue-cropperjs`, replaced with direct `cropperjs@2` integration in `AdAddPage.vue`
  - `hioshop-admin-web`: removed dead legacy `summernote + jQuery` code paths in `GoodsAddPage.vue` and `new_file.vue`
  - `hioshop-miniprogram`: `globals` -> `^17.4.0`
- Deferred breaking majors intentionally to preserve runtime compatibility:
  - admin: `vuedraggable` 当前 `4.1.0` 为 Vue3 兼容线，npm `latest` 标签为旧 Vue2 支线版本，保持 `4.1.0`

## 2) Test Evidence

### Build / Lint Gates

- `hioshop-server`
  - `npm run compile` ✅
  - `npm run lint` ✅
- `hioshop-admin-web`
  - `npm run lint` ✅
  - `npm run test:unit` ✅ (`src/router/guards.spec.js`, `src/components/Common/quill-utils.spec.js`, 12 tests passed)
  - `npm run build:prod` ✅
- `hioshop-miniprogram`
  - `npm run lint` ✅
  - `npm run test:syntax` ✅
  - `node testing/scripts/miniprogram_request_smoke.js` ✅

### Security / Business Regression (server targeted)

- Ran local regression against MySQL + ThinkJS4 runtime:
  - `npm run test:coupon` ✅
  - `npm run test:security-regression` ✅

### Cross-End Full Gate

- `testing/run_pr_gate.py` ✅
  - report: `testing-artifacts/20260311-154428-pr-gate/pr-gate-report.md`
  - summary: `total=27, passed=27, failed=0, skipped=0`
- `testing/run_nightly_full.py` ✅
  - report: `testing-artifacts/20260311-154433-nightly-full/nightly-report.md`
  - summary: `total=291, passed=291, failed=0, skipped=0`

## 3) Known Residual Items

- Admin build still reports Sass `@import` deprecation warnings (non-blocking, should be migrated to `@use` in a follow-up).
- Vite build warns for unresolved runtime stylesheet path `/admin/css/font-awesome.min.css` at build time; runtime path is preserved intentionally.
- `hioshop-admin-web` still has 1 low-severity advisory on `quill@2.0.3` (`GHSA-v3m3-f69x-jf25`), with no patched latest line in current ecosystem path; use strict server-side sanitize on rich-text persistence/output.
- Several transitive dependency vulnerabilities remain and are tied to upstream ecosystems (ThinkJS alpha / legacy plugin trees). They require selective replacement, not blind `npm audit fix --force`.

## 4) Rollback Readiness

- Baseline tag script and artifact script are ready for release snapshots.
- Rollback script can reset each subrepo to baseline tags by stamp.
