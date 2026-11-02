#!/usr/bin/env bash
# Linux release build:  scripts/build.sh            -> target/release/nebians
#                       scripts/build.sh windows    -> target/x86_64-pc-windows-gnu/release/nebians.exe
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${1:-}" = "windows" ]; then
  command -v x86_64-w64-mingw32-gcc >/dev/null || { echo "Install mingw-w64:  sudo apt install mingw-w64"; exit 1; }
  rustup target add x86_64-pc-windows-gnu
  # Rust's std for the -gnu target needs the *posix* threading flavour of mingw.
  sudo update-alternatives --set x86_64-w64-mingw32-gcc /usr/bin/x86_64-w64-mingw32-gcc-posix 2>/dev/null || true
  cargo build --release --target x86_64-pc-windows-gnu
  ls -lh target/x86_64-pc-windows-gnu/release/nebians.exe
else
  cargo build --release
  ls -lh target/release/nebians
fi
