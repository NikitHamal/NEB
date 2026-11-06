#!/bin/bash
# Real screenshots of the real binary, headless: scripts/screenshots.sh [out-dir]
# Needs: xvfb, xauth, Mesa software GL, a running backend (NEB_API_BASE, default production).
set -e
cd "$(dirname "$0")/.."
OUT=${1:-screenshots}
BIN=target/release/nebians
for SZ in 1440x900 900x600; do
  CFG=$(mktemp -d)
  D=$OUT/$SZ; mkdir -p "$D"
  LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a -s "-screen 0 ${SZ%x*}x${SZ#*x}x24" \
    $BIN --config "$CFG" --reset --size $SZ --screenshots "$D"
done
