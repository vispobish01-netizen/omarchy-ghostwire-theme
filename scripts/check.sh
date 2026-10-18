#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "==> Verifying theme files are in sync with colors.toml..."
python3 "$SCRIPT_DIR/generate.py" --check

echo "==> Running syntax validation across configs..."
# Validate TOML
python3 -c '
import tomllib, glob
for f in glob.glob("**/*.toml", recursive=True):
    with open(f, "rb") as fp:
        tomllib.load(fp)
'
# Validate JSON
python3 -c '
import json, glob
for f in glob.glob("**/*.json", recursive=True):
    with open(f, "r") as fp:
        json.load(fp)
'

# Validate Lua if luac is available
if command -v luac &>/dev/null; then
    for f in "$ROOT_DIR"/*.lua "$ROOT_DIR"/*.lua.example; do
        [ -f "$f" ] && luac -p "$f"
    done
fi

echo "==> All integrity and synchronization checks passed successfully!"
