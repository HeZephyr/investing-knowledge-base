#!/usr/bin/env bash
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
python="$root/.venv/bin/python"
ruff="$root/.venv/bin/ruff"
temp="$(mktemp -d)"
trap 'rm -rf "$temp"' EXIT

cd "$root"
"$ruff" check src tests
"$ruff" format --check src tests
"$python" -m pytest -q
"$python" -m investkb.cli sources audit raw
"$python" -m investkb.cli wiki lint
"$python" -m investkb.cli coverage validate
"$python" -m investkb.publication
"$python" -m investkb.site
"$python" -m mkdocs build --strict

cd "$temp"
"$python" -m investkb.cli demo backtest --offline
test -f "$temp/output/reports/demo/report.md"
echo "PASS: offline demo report"
