#!/usr/bin/env bash
set -euo pipefail

API_DOMAIN=${API_DOMAIN:-api.fybshop.site}
ADMIN_DOMAIN=${ADMIN_DOMAIN:-admin.fybshop.site}
ENABLE_CADDY=${ENABLE_CADDY:-0}

if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] docker is not installed"
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "[ERROR] docker compose plugin is not available"
  exit 1
fi

cd /opt/hioshop/deploy

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[WARN] .env created from .env.example. Fill secrets before rerun."
  exit 1
fi

docker compose pull || true
if [ "${ENABLE_CADDY}" = "1" ]; then
  docker compose --profile caddy up -d --build
else
  docker compose up -d --build
fi

echo "[INFO] Running basic checks..."
docker compose ps
curl -fsS http://127.0.0.1:8360/ >/dev/null && echo "[OK] API container reachable (127.0.0.1:8360)"
curl -fsS http://127.0.0.1:8080/ >/dev/null && echo "[OK] Admin container reachable (127.0.0.1:8080)"

curl -sS -X POST "http://127.0.0.1:8360/admin/auth/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=qilelab.com&password=qilelab.com' | head -c 240

if [ "${ENABLE_CADDY}" = "1" ]; then
  curl -fsS "https://${API_DOMAIN}" >/dev/null && echo "[OK] API domain reachable"
  curl -fsS "https://${ADMIN_DOMAIN}" >/dev/null && echo "[OK] Admin domain reachable"
fi

echo "\n[DONE] Deployment finished"
