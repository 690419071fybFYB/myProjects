#!/usr/bin/env bash
set -euo pipefail

SERVER_HOST=${SERVER_HOST:-}
SERVER_USER=${SERVER_USER:-root}
SERVER_PORT=${SERVER_PORT:-22}
TARGET_DIR=${TARGET_DIR:-/opt/hioshop}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if ! command -v rsync >/dev/null 2>&1; then
  echo "[ERROR] rsync is required"
  exit 1
fi

if [ -z "${SERVER_HOST}" ]; then
  echo "[ERROR] SERVER_HOST is required. Example:"
  echo "SERVER_HOST=106.54.21.65 SERVER_USER=root bash deploy/scripts/upload_bundle.sh"
  exit 1
fi

echo "[INFO] Uploading project bundle to ${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}"

ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p ${TARGET_DIR}"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude '.env' \
  --exclude 'dist' \
  "${PROJECT_ROOT}/deploy/" "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/deploy/"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'runtime' \
  "${PROJECT_ROOT}/hioshop-server/" "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/hioshop-server/"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'dist' \
  "${PROJECT_ROOT}/hioshop-admin-web/" "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/hioshop-admin-web/"

echo "[DONE] Upload complete"
