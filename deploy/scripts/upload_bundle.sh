#!/usr/bin/env bash
set -euo pipefail

SERVER_HOST=${SERVER_HOST:-}
SERVER_USER=${SERVER_USER:-root}
TARGET_DIR=${TARGET_DIR:-/opt/hioshop}

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

ssh "${SERVER_USER}@${SERVER_HOST}" "mkdir -p ${TARGET_DIR}"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'dist' \
  /Volumes/SAMSUNG/fyb/myProjects/deploy/ "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/deploy/"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'runtime' \
  /Volumes/SAMSUNG/fyb/myProjects/hioshop-server/ "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/hioshop-server/"

rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '.DS_Store' \
  --exclude 'dist' \
  /Volumes/SAMSUNG/fyb/myProjects/hioshop-admin-web/ "${SERVER_USER}@${SERVER_HOST}:${TARGET_DIR}/hioshop-admin-web/"

echo "[DONE] Upload complete"
