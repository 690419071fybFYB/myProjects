# hioshop Docker deployment (BaoTa entry mode)

This deployment uses Docker for app services and BaoTa/Nginx for HTTPS + reverse proxy.

## Service topology

- `mysql` container: private only
- `server` container: `127.0.0.1:8360`
- `admin` container: `127.0.0.1:8080`
- Public traffic enters via BaoTa:
  - `https://api.fybshop.site` -> `http://127.0.0.1:8360`
  - `https://admin.fybshop.site` -> `http://127.0.0.1:8080`

## 1) Upload code to server

```bash
cd /Volumes/SAMSUNG/fyb/myProjects
SERVER_HOST=<YOUR_SERVER_IP> SERVER_USER=<YOUR_USER> bash deploy/scripts/upload_bundle.sh
```

## 2) Prepare server

```bash
ssh <YOUR_USER>@<YOUR_SERVER_IP>
sudo mkdir -p /opt/hioshop
sudo chown -R $USER:$USER /opt/hioshop
```

Install Docker + Compose plugin if missing.

## 3) Configure environment and start containers

```bash
cd /opt/hioshop/deploy
cp .env.example .env
vi .env
# set MYSQL_ROOT_PASSWORD and your WEIXIN/OSS secrets

bash scripts/deploy_remote.sh
```

## 4) Configure BaoTa reverse proxy + SSL

Create two BaoTa sites:

- `api.fybshop.site`
- `admin.fybshop.site`

For each site:

1. Install the matching SSL certificate in BaoTa.
2. Enable force HTTPS.
3. Configure reverse proxy:
   - `api.fybshop.site` => `http://127.0.0.1:8360`
   - `admin.fybshop.site` => `http://127.0.0.1:8080`

Reference Nginx snippets:

- `deploy/baota/nginx-api.conf`
- `deploy/baota/nginx-admin.conf`

## 5) Verify

```bash
curl -I https://api.fybshop.site
curl -I https://admin.fybshop.site
curl -s -X POST https://api.fybshop.site/admin/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=qilelab.com&password=qilelab.com'
```

## Optional: run Caddy mode instead of BaoTa

If you later migrate to Caddy-managed HTTPS:

```bash
cd /opt/hioshop/deploy
ENABLE_CADDY=1 bash scripts/deploy_remote.sh
```

## Notes

- MySQL imports `../hioshop-server/hiolabsDB.sql` on first startup only.
- To re-import SQL, remove `mysql_data` volume before next startup.
- Do not expose `3306` to public network.
