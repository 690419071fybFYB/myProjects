#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAMP="${1:-$(date +%Y%m%d-%H%M%S)}"
TAG_PREFIX="upgrade-baseline-${STAMP}"

repos=(
  "hioshop-server"
  "hioshop-admin-web"
  "hioshop-miniprogram"
)

echo "[baseline] tag prefix: ${TAG_PREFIX}"

for repo in "${repos[@]}"; do
  repo_dir="${ROOT_DIR}/${repo}"
  if [[ ! -d "${repo_dir}/.git" ]]; then
    echo "[baseline] skip ${repo}: missing git metadata"
    continue
  fi

  dirty="$(git -C "${repo_dir}" status --porcelain)"
  if [[ -n "${dirty}" ]]; then
    echo "[baseline] ${repo} has uncommitted changes, skip tagging to avoid ambiguous rollback point"
    continue
  fi

  tag_name="${TAG_PREFIX}-${repo}"
  git -C "${repo_dir}" tag -a "${tag_name}" -m "Pre cross-generation upgrade baseline (${repo})"
  echo "[baseline] tagged ${repo} -> ${tag_name}"
done

echo "[baseline] done"
