#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <STAMP>"
  echo "Example: $0 20260311-190000"
  exit 1
fi

STAMP="$1"
TAG_PREFIX="upgrade-baseline-${STAMP}"

repos=(
  "hioshop-server"
  "hioshop-admin-web"
  "hioshop-miniprogram"
)

for repo in "${repos[@]}"; do
  repo_dir="${ROOT_DIR}/${repo}"
  tag_name="${TAG_PREFIX}-${repo}"
  if ! git -C "${repo_dir}" rev-parse -q --verify "refs/tags/${tag_name}" >/dev/null; then
    echo "[rollback] missing tag ${tag_name}, skip ${repo}"
    continue
  fi
  echo "[rollback] reset ${repo} to ${tag_name}"
  git -C "${repo_dir}" checkout "${tag_name}"
done

echo "[rollback] restore complete"
