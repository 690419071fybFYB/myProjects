#!/usr/bin/env bash
set -euo pipefail

API_DOMAIN=${API_DOMAIN:-api.fybshop.site}
ADMIN_DOMAIN=${ADMIN_DOMAIN:-admin.fybshop.site}

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
docker compose up -d --build

echo "[INFO] Running basic checks..."
docker compose ps
curl -fsS http://127.0.0.1:8360/ >/dev/null && echo "[OK] API container reachable (127.0.0.1:8360)"
curl -fsS http://127.0.0.1:8080/ >/dev/null && echo "[OK] Admin container reachable (127.0.0.1:8080)"

curl -sS -X POST "http://127.0.0.1:8360/admin/auth/login" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=qilelab.com&password=qilelab.com' | head -c 240

echo "[INFO] Caddy entry is enabled."
echo "[INFO] Local test: https://api.localhost:${CADDY_HTTPS_PORT:-18443} and https://admin.localhost:${CADDY_HTTPS_PORT:-18443}"
echo "[INFO] Production domains: https://${API_DOMAIN} and https://${ADMIN_DOMAIN}"

echo "\n[DONE] Deployment finished"
