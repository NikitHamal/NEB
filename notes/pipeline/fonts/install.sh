#!/usr/bin/env bash
# Fetch the five book fonts from Google Fonts into the user font directory.
set -euo pipefail

DEST="${1:-$HOME/.local/share/fonts/nebians}"
mkdir -p "$DEST"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

BASE="https://github.com/google/fonts/raw/main"
FILES=(
  "ofl/poppins/Poppins-Light.ttf"
  "ofl/poppins/Poppins-Regular.ttf"
  "ofl/poppins/Poppins-SemiBold.ttf"
  "ofl/poppins/Poppins-Bold.ttf"
  "ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
  "ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf"
  "ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
  "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
)

for f in "${FILES[@]}"; do
  name="$(basename "${f%%%5B*}" .ttf)"
  echo "  $name"
  curl -fsSL "$BASE/$f" -o "$DEST/$(basename "$f" | python3 -c \
    'import sys,urllib.parse;print(urllib.parse.unquote(sys.stdin.read().strip()))')"
done

fc-cache -f "$DEST" >/dev/null
echo "installed to $DEST"
fc-list : family | tr ',' '\n' | sort -u | grep -iE \
  'poppins|inter|source serif|noto sans devanagari|jetbrains' || true
