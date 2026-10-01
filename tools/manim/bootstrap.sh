#!/usr/bin/env bash
# Rebuild everything the Manim pipeline needs that is not committed.
#
# The video pipeline runs on a pure-Python toolchain: a Skia-backed stand-in
# for pycairo and a FreeType-backed stand-in for manimpango, both of which live
# in tools/manim/shims and *are* committed.  What is not committed is the
# virtualenv, the two stub libraries skia-python demands, and an ffmpeg binary
# -- so this script makes all three.  Run it once per machine:
#
#   tools/manim/bootstrap.sh
#
# It is idempotent, and safe to re-run after the sandbox is reset.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"

VENV="${NEB_VENV:-/home/user/.nebvideo-venv}"
STUBS="${NEB_GL_STUB_DIR:-/home/user/.nebvideo/stublibs}"
BIN="${NEB_BIN_DIR:-/home/user/.nebvideo/bin}"
PYTHON="${PYTHON:-$VENV/bin/python}"

echo "==> virtualenv at $VENV"
if [ ! -x "$PYTHON" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip

echo "==> python packages (manim, skia-python, freetype-py, matplotlib, ffmpeg)"
# manim's own dependency list includes pycairo, which has no wheel for this
# platform and cannot compile here -- the shim in tools/manim/shims/cairo
# replaces it.  So manim is installed --no-deps and its real dependencies are
# listed explicitly, which is also exactly what requirements.txt says.  The
# whole file is installed --no-deps for the same reason.
"$VENV/bin/pip" install -q --no-deps -r "$HERE/requirements.txt"

echo "==> libEGL / libGL stubs for skia-python"
NEB_GL_STUB_DIR="$STUBS" PYTHON="$PYTHON" bash "$HERE/make_gl_stubs.sh" "$STUBS"

echo "==> ffmpeg"
mkdir -p "$BIN"
if [ ! -e "$BIN/ffmpeg" ]; then
    ln -s "$("$PYTHON" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" "$BIN/ffmpeg"
    echo "  linked $BIN/ffmpeg"
fi
"$BIN/ffmpeg" -version 2>/dev/null | head -1

cat <<EOF

Ready.  Render with:

  tools/manim/scripts/render.sh videos/phy11_unit01.py PhysicalQuantities

or, to do it by hand:

  LD_LIBRARY_PATH=$STUBS PATH=$BIN:\$PATH \\
  PYTHONPATH=$ROOT/tools/manim/shims:$ROOT/tools/manim \\
  $PYTHON -m manim render ...
EOF
