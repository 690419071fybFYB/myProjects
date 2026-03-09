#!/usr/bin/env bash
set -euo pipefail

API_DOMAIN=${API_DOMAIN:-api.fybshop.site}
ADMIN_DOMAIN=${ADMIN_DOMAIN:-admin.fybshop.site}
TARGET_DIR=${TARGET_DIR:-/opt/hioshop}

if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] docker is not installed"
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "[ERROR] docker compose plugin is not available"
  exit 1
fi

cd "$TARGET_DIR/deploy"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "[WARN] .env created from .env.example. Fill secrets before rerun."
  exit 1
fi

docker compose pull || true
docker compose up -d --build

wait_http() {
  local url="$1"
  local label="$2"
  local max_attempts="${3:-40}"
  for i in $(seq 1 "$max_attempts"); do
    if curl -fsS --max-time 5 "$url" >/dev/null; then
      echo "[OK] ${label} reachable (${url})"
      return 0
    fi
    echo "[WAIT] ${label} not ready (${i}/${max_attempts})"
    sleep 2
  done
  echo "[ERROR] ${label} not reachable after ${max_attempts} attempts (${url})"
  return 1
}

echo "[INFO] Running basic checks..."
docker compose ps
wait_http "http://127.0.0.1:8360/api/index/appInfo" "API"
wait_http "http://127.0.0.1:8080/" "Admin"

for i in $(seq 1 20); do
  login_response=$(curl -sS --max-time 5 -X POST "http://127.0.0.1:8360/admin/auth/login" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data 'username=qilelab.com&password=qilelab.com' || true)
  if printf '%s' "$login_response" | grep -q '"errno":0'; then
    printf '%s\n' "$login_response" | head -c 240
    echo
    echo "[OK] Admin login API reachable"
    break
  fi
  if [ "$i" -eq 20 ]; then
    echo "[ERROR] Admin login API check failed after retries"
    printf '%s\n' "$login_response" | head -c 240
    echo
    exit 1
  fi
  echo "[WAIT] Admin login API not ready (${i}/20)"
  sleep 2
done

echo "[INFO] Caddy entry is enabled."
echo "[INFO] Local test: https://api.localhost:${CADDY_HTTPS_PORT:-18443} and https://admin.localhost:${CADDY_HTTPS_PORT:-18443}"
echo "[INFO] Production domains: https://${API_DOMAIN} and https://${ADMIN_DOMAIN}"

echo "\n[DONE] Deployment finished"
