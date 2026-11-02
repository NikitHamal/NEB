#!/usr/bin/env bash
# Headless screenshot tour of every screen (needs xvfb, xauth, mesa software GL).
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="${1:-$(cd .. && pwd)}"; mkdir -p screenshots
xvfb-run -a -s "-screen 0 1400x900x24 +extension GLX" env NEB_CONFIG_DIR="$(mktemp -d)" LIBGL_ALWAYS_SOFTWARE=1 \
  target/release/nebians --content "$REPO" --screenshots screenshots --reset
