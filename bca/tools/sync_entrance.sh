#!/usr/bin/env bash
# Mirror the canonical entrance sources (notes/content/bca-*) into the public bca/entrance/ tree.
set -e
cd "$(dirname "$0")/../.."
declare -A MAP=( [bca-math]=mathematics [bca-eng]=english [bca-gk]=gk-and-it [bca-mock]=model-papers )
for src in "${!MAP[@]}"; do
  dst="bca/entrance/${MAP[$src]}"; mkdir -p "$dst"
  if grep -qx "${MAP[$src]}" bca/entrance/.polished 2>/dev/null; then echo "skip polished book ${MAP[$src]} (edit it in bca/entrance directly)"; continue; fi
  rm -f "$dst"/unit-*.md
  cp notes/content/$src/unit-*.md "$dst"/
  cp notes/curriculum/$src.md "$dst/SPINE.md"
done
echo "synced entrance sources"
