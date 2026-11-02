#!/usr/bin/env bash
# Make a self-contained, redistributable folder: binary + the study content it reads.
#   scripts/bundle-content.sh [linux|windows] [--with-pdfs]
set -euo pipefail
cd "$(dirname "$0")/.."
OS="${1:-linux}"; REPO="$(cd .. && pwd)"
OUT="dist/NEBians-Desktop-$OS"; rm -rf "$OUT"; mkdir -p "$OUT/content/static/web"
if [ "$OS" = windows ]; then cp target/x86_64-pc-windows-gnu/release/nebians.exe "$OUT/"; else cp target/release/nebians "$OUT/"; fi
cp -r "$REPO/backend_python/web/data" "$OUT/content/data"
cp -r "$REPO/backend_python/web/static/web/study" "$OUT/content/static/web/study"
if [ "${2:-}" = "--with-pdfs" ]; then mkdir -p "$OUT/content/pdf"; cp "$REPO"/notes/pdf/*.pdf "$OUT/content/pdf/"; fi
cat > "$OUT/README.txt" <<TXT
NEBians Desktop. Run nebians$( [ "$OS" = windows ] && echo .exe ) — it finds the content/ folder next to it.
Use another checkout with:  nebians --content <path-to-NEB>
TXT
( cd dist && zip -qr "NEBians-Desktop-$OS.zip" "NEBians-Desktop-$OS" ) && ls -lh "dist/NEBians-Desktop-$OS.zip"
