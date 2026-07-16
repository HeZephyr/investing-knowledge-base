#!/usr/bin/env bash
set -euo pipefail

url="${1:-}"
commit="${2:-}"
name="${3:-}"

if [[ ! "$url" =~ ^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo "error: only canonical https://github.com/OWNER/REPO URLs are allowed" >&2
  exit 2
fi
if [[ -z "$commit" || ! "$commit" =~ ^[0-9a-f]{40}$ ]]; then
  echo "error: commit must be a full 40-character SHA" >&2
  exit 2
fi
if [[ -z "$name" || "$name" == *"/"* || "$name" == *".."* ]]; then
  echo "error: target name must be a simple directory name" >&2
  exit 2
fi

root="$(git rev-parse --show-toplevel)"
target="$root/data/reference-repos/$name"
mkdir -p "$(dirname "$target")"
if [[ -e "$target" ]]; then
  echo "error: target already exists: $target" >&2
  exit 3
fi

git clone --filter=blob:none --no-checkout "$url" "$target"
git -C "$target" checkout --detach "$commit"
echo "$target"
