#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/Volumes/SAMSUNG/fyb/myProjects"
SERVER_DIR="$ROOT_DIR/hioshop-server"
MINI_DIR="$ROOT_DIR/hioshop-miniprogram"
ADMIN_DIR="$ROOT_DIR/hioshop-admin-web"

echo "[1/3] Verify hioshop-server"
cd "$SERVER_DIR"
npm run compile
npm run test:goods-import
npm run test:coupon
npm run test:cos-smoke
npm audit --omit=dev --omit=optional --audit-level=high

echo "[2/3] Verify hioshop-miniprogram"
cd "$MINI_DIR"
node -c components/login-profile-sheet/index.js
node -c pages/category/index.js
node -c pages/ucenter/settings/index.js
node -c utils/request/index.js
node -c utils/util.js

echo "[3/3] Verify hioshop-admin-web"
cd "$ADMIN_DIR"
npm run lint
npm run test:unit -- --passWithNoTests
npm run build:prod
npm audit --omit=dev --audit-level=high

echo "Stage 3 release verification passed."
