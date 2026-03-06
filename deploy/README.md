# hioshop Docker deployment (Caddy only)

This deployment uses Docker for all runtime components, including Caddy as the only public entry.

## Services

- `mysql`: private database
- `server`: ThinkJS API (`server:8360`)
- `admin`: admin static site (`admin:80`)
- `caddy`: reverse proxy + HTTPS

## Local verification

```bash
cd /Volumes/SAMSUNG/fyb/myProjects/deploy
cp .env.example .env

docker compose up -d --build

# admin (local https)
curl -k -I https://admin.localhost:18443

# api (local https)
curl -k -I https://api.localhost:18443/api/index/appInfo
```

## Production deployment

On server `/opt/hioshop/deploy/.env`, set:

```env
CADDYFILE_PATH=./caddy/Caddyfile
CADDY_HTTP_PORT=80
CADDY_HTTPS_PORT=443
ACME_EMAIL=you@example.com
API_DOMAIN=api.fybshop.site
ADMIN_DOMAIN=admin.fybshop.site
BT_CERTS_PATH=/www/server/panel/vhost/cert
```

Then deploy:

```bash
cd /opt/hioshop/deploy
bash scripts/deploy_remote.sh
```

If ACME validation is blocked by DNS/ISP policy, switch to Tencent cert files:

```env
CADDYFILE_PATH=./caddy/Caddyfile.bt-cert
BT_CERTS_PATH=/www/server/panel/vhost/cert
```

Then restart:

```bash
docker compose up -d --force-recreate caddy
```

## Verify

```bash
curl -I https://api.fybshop.site
curl -I https://admin.fybshop.site
curl -s -X POST https://api.fybshop.site/admin/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=qilelab.com&password=qilelab.com'
```

## Notes

- MySQL imports `../hioshop-server/hiolabsDB.sql` only on first startup.
- Keep `3306` closed to public network.
- If server has host Nginx on `80/443`, stop it before starting Caddy container.

## CI/CD (GitHub Actions)

Repository includes:

- `.github/workflows/ci.yml`: PR/push quality checks
- `.github/workflows/cd.yml`: auto deploy on `main` (or manual trigger)

Required GitHub repository secrets:

- `DEPLOY_HOST`: server IP/domain
- `DEPLOY_USER`: SSH login user (for example `root`)
- `DEPLOY_SSH_PRIVATE_KEY`: private key content for the deploy user
- `DEPLOY_PORT` (optional): SSH port, default `22`
- `DEPLOY_TARGET_DIR` (optional): default `/opt/hioshop`

Deployment flow:

1. Push code to `main`
2. Workflow uploads `deploy/`, `hioshop-server/`, `hioshop-admin-web/` via `rsync`
3. Workflow runs `bash scripts/deploy_remote.sh` on remote server

Important:

- Keep production secrets only in server-side `deploy/.env`; CI upload excludes `.env`.
- Never commit real credentials into repo files.
