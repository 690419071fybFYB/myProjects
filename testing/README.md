# Hioshop Fullstack Release Gate

This folder implements the multi-layer quality gate for the three-repo stack:

- `hioshop-server`
- `hioshop-miniprogram`
- `hioshop-admin-web`

## Layers

- `L1` Contract checks for `api` and `admin` actions.
- `L2` Business chain checks with DB assertions.
- `L3` Cross-end linkage checks (admin change -> mini behavior -> order effect).
- `L4` Frontend smoke checks (mini request/sdk logic and admin login-operation smoke).

## Entry Points

- PR gate: `python3 testing/run_pr_gate.py --workspace /abs/path/myProjects`
- Nightly full: `python3 testing/run_nightly_full.py --workspace /abs/path/myProjects`
- L2 business only:
  - core: `python3 testing/scripts/business_suite.py --scope core --workspace /abs/path/myProjects`
  - full: `python3 testing/scripts/business_suite.py --scope full --workspace /abs/path/myProjects`
- L2 长尾域链路（邀请/广告消息/搜索/足迹）：
  - `python3 testing/scripts/domain_flow_suite.py --base-url http://127.0.0.1:8360 --api-jwt-secret <secret> --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password <pwd> --db-name hiolabsDB`
- L2 运营导入审计链路（任务列表/详情/错误文件+DB）：
  - `python3 testing/scripts/operations_audit_suite.py --base-url http://127.0.0.1:8360 --admin-username qilelab.com --admin-password qilelab.com --db-host 127.0.0.1 --db-port 3306 --db-user root --db-password <pwd> --db-name hiolabsDB`

Reports are written to:

- `testing-artifacts/<timestamp>-pr-gate/pr-gate-report.{json,md}`
- `testing-artifacts/<timestamp>-nightly-full/nightly-report.{json,md}`

## CI/CD

- PR core gate is wired in `.github/workflows/ci.yml` job `PR Business Gate`.
- Nightly full regression is wired in `.github/workflows/nightly-full.yml`.
- Both workflows bootstrap MySQL 8, import `hioshop-server/hiolabsDB.sql`, start server with CI test secrets, then execute the Python runners above and upload `testing-artifacts`.

## Environment

Common env vars used by scripts:

- `BASE_URL` (default `http://127.0.0.1:8360`)
- `API_JWT_SECRET`, `ADMIN_JWT_SECRET`
- `API_TOKEN_SECRET`, `ADMIN_TOKEN_SECRET` (compat aliases for legacy scripts)
- `TEST_DB_HOST`, `TEST_DB_PORT`, `TEST_DB_USER`, `TEST_DB_PASSWORD`, `TEST_DB_NAME`
- `TEST_API_USER_ID`, `TEST_ADMIN_USER_ID`
- `TEST_ADMIN_USERNAME`, `TEST_ADMIN_PASSWORD`

Before local execution:

- `python3 -m pip install -r testing/requirements.txt`
- run commands from workspace root `/Volumes/SAMSUNG/fyb/myProjects` so relative paths to the three repos resolve correctly.

## Scenarios

Scenario IDs and intended coverage are maintained in:

- `testing/scenarios/business_flow_matrix.json`

This matrix is used to surface not-yet-automated scenarios as explicit `skipped` items in reports.
