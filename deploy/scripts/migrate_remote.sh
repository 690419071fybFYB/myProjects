#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR=${TARGET_DIR:-/opt/hioshop}
DB_CONTAINER=${DB_CONTAINER:-hioshop-mysql}
SQL_DIR="${TARGET_DIR}/hioshop-server/sql"

if ! command -v docker >/dev/null 2>&1; then
  echo "[ERROR] docker is not installed"
  exit 1
fi

if [ ! -d "$SQL_DIR" ]; then
  echo "[ERROR] SQL directory not found: $SQL_DIR"
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$DB_CONTAINER"; then
  echo "[ERROR] MySQL container is not running: $DB_CONTAINER"
  exit 1
fi

create_table_sql="
CREATE TABLE IF NOT EXISTS schema_migrations (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  version VARCHAR(255) NOT NULL,
  applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uniq_version (version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"

docker exec -i "$DB_CONTAINER" sh -lc 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' <<SQL
${create_table_sql}
SQL

applied_count=0
skipped_count=0

while IFS= read -r sql_file; do
  [ -n "$sql_file" ] || continue
  version="$(basename "$sql_file")"
  escaped_version=${version//\'/\'\'}

  already_applied="$(docker exec "$DB_CONTAINER" sh -lc "mysql -uroot -p\"\$MYSQL_ROOT_PASSWORD\" -N -B \"\$MYSQL_DATABASE\" -e \"SELECT COUNT(1) FROM schema_migrations WHERE version='${escaped_version}'\"")"

  if [ "$already_applied" != "0" ]; then
    echo "[SKIP] ${version} already applied"
    skipped_count=$((skipped_count + 1))
    continue
  fi

  echo "[APPLY] ${version}"
  docker exec -i "$DB_CONTAINER" sh -lc 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"' < "$sql_file"
  docker exec "$DB_CONTAINER" sh -lc "mysql -uroot -p\"\$MYSQL_ROOT_PASSWORD\" \"\$MYSQL_DATABASE\" -e \"INSERT INTO schema_migrations (version) VALUES ('${escaped_version}')\""
  applied_count=$((applied_count + 1))
done < <(find "$SQL_DIR" -maxdepth 1 -type f -name '*.sql' | sort)

echo "[DONE] migrations applied=${applied_count}, skipped=${skipped_count}"
