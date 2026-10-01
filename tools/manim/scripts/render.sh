#!/usr/bin/env bash
# Render one episode with the Manim pipeline.
#
#   tools/manim/scripts/render.sh <scene.py> <SceneClass> [extra manim args]
#
# Wraps the environment the shims need (LD_LIBRARY_PATH for the EGL/GL stubs,
# PYTHONPATH so the cairo and manimpango stand-ins shadow the real -- absent --
# packages, and an ffmpeg on PATH) and forwards everything else to manim.
#
# The scene also writes build/beats.json: the scene time at which each line of
# narration starts.  mux.py reads it back to place the voice-over, so it follows
# whatever --media_dir you pass here.
#
# Examples:
#   tools/manim/scripts/render.sh videos/phy11_unit01.py PhysicalQuantities -ql
#   tools/manim/scripts/render.sh videos/phy11_unit01.py PhysicalQuantities -qh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE="$(cd "$HERE/.." && pwd)"          # tools/manim
ROOT="$(cd "$PIPELINE/../.." && pwd)"       # repository root

if [ "$#" -lt 2 ]; then
    sed -n '2,14p' "${BASH_SOURCE[0]}" >&2
    exit 1
fi

SCENE="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
CLASS="$2"
shift 2

VENV="${NEB_VENV:-/home/user/.nebvideo-venv}"
STUBS="${NEB_GL_STUB_DIR:-/home/user/.nebvideo/stublibs}"
BIN="${NEB_BIN_DIR:-/home/user/.nebvideo/bin}"
MEDIA="${NEB_MEDIA_DIR:-$PIPELINE/build}"

# --media_dir wins over NEB_MEDIA_DIR, so the beat log has to follow it.  The
# rest of the arguments are handed to manim untouched.
EXTRA=()
while [ "$#" -gt 0 ]; do
    case "$1" in
        --media_dir)
            MEDIA="$2"
            shift 2
            ;;
        --media_dir=*)
            MEDIA="${1#--media_dir=}"
            shift
            ;;
        *)
            EXTRA+=("$1")
            shift
            ;;
    esac
done

export LD_LIBRARY_PATH="$STUBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="$BIN:$PATH"
export PYTHONPATH="$PIPELINE/shims:$PIPELINE${PYTHONPATH:+:$PYTHONPATH}"
export NEB_BEAT_LOG="${NEB_BEAT_LOG:-$MEDIA/beats.json}"
mkdir -p "$MEDIA"

exec "$VENV/bin/python" -m manim render \
    --media_dir "$MEDIA" \
    --disable_caching \
    "${EXTRA[@]}" \
    "$SCENE" "$CLASS"
