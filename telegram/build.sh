#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEME_NAME="ghostwire.tdesktop-theme"

echo "==> Building Telegram Desktop theme package: ${THEME_NAME}..."

cd "$SCRIPT_DIR"

if [[ ! -f "colors.tdesktop-theme" ]]; then
    echo "Error: colors.tdesktop-theme not found!" >&2
    exit 1
fi

if [[ ! -f "background.jpg" ]]; then
    echo "Error: background.jpg not found!" >&2
    exit 1
fi

# Remove older build if present
rm -f "$THEME_NAME"

# Zip colors.tdesktop-theme and background.jpg into ghostwire.tdesktop-theme
# The .tdesktop-theme file is standard zip format with exact root entries
zip -q -9 "$THEME_NAME" colors.tdesktop-theme background.jpg

echo "==> Successfully packaged ${THEME_NAME} ($(du -h "$THEME_NAME" | cut -f1))"
