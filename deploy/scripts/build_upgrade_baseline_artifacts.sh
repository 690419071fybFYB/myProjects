#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/deploy/artifacts"
STAMP="${1:-$(date +%Y%m%d-%H%M%S)}"
ARTIFACT_DIR="${OUT_DIR}/${STAMP}"

mkdir -p "${ARTIFACT_DIR}"

echo "[artifact] output directory: ${ARTIFACT_DIR}"

echo "[artifact] build server image"
docker build \
  -t "hioshop-server:${STAMP}" \
  "${ROOT_DIR}/hioshop-server"

echo "[artifact] build admin image"
docker build \
  -t "hioshop-admin-web:${STAMP}" \
  "${ROOT_DIR}/hioshop-admin-web"

echo "[artifact] export image archive"
docker save \
  "hioshop-server:${STAMP}" \
  "hioshop-admin-web:${STAMP}" \
  | gzip > "${ARTIFACT_DIR}/images-${STAMP}.tar.gz"

echo "[artifact] export miniprogram source"
tar -czf "${ARTIFACT_DIR}/hioshop-miniprogram-${STAMP}.tar.gz" -C "${ROOT_DIR}" hioshop-miniprogram

cat > "${ARTIFACT_DIR}/manifest.txt" <<EOF
STAMP=${STAMP}
SERVER_IMAGE=hioshop-server:${STAMP}
ADMIN_IMAGE=hioshop-admin-web:${STAMP}
MINIPROGRAM_ARCHIVE=hioshop-miniprogram-${STAMP}.tar.gz
EOF

echo "[artifact] done"
