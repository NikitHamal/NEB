#!/usr/bin/env bash
# Build the no-op libEGL / libGL that skia-python insists on linking.
#
# skia-python's wheel links libEGL.so.1 and libGL.so.1 even when you only use
# the CPU raster backend, and this container has neither.  The symbols it needs
# are the entry points it would call to talk to a GPU; on the raster path none
# of them are ever reached, so a shared library that answers every one of them
# with 0 is enough to satisfy the dynamic linker.
#
#   tools/manim/make_gl_stubs.sh [output-dir]
#
# The .so files are build artefacts, not source, and are not committed -- run
# this (or tools/manim/bootstrap.sh, which calls it) after a fresh checkout.
set -euo pipefail

OUT="${1:-${NEB_GL_STUB_DIR:-/home/user/.nebvideo/stublibs}}"
PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
    for candidate in /home/user/.nebvideo-venv/bin/python python3; do
        if command -v "$candidate" >/dev/null 2>&1; then PYTHON="$candidate"; break; fi
    done
fi

mkdir -p "$OUT"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# Find the skia extension module without importing it: importing skia is
# exactly what fails until the stubs exist.
SITE="$("$PYTHON" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
SKIA_SO="$(find "$SITE" -maxdepth 1 -name 'skia.*.so' | head -1)"
if [ -z "$SKIA_SO" ]; then
    echo "could not find the skia extension module under $SITE" >&2
    exit 1
fi
echo "skia module: $SKIA_SO"

nm -D --undefined-only "$SKIA_SO" \
    | awk '$1 == "U" { print $2 }' \
    | grep -E '^(egl|gl)[A-Za-z0-9_]*$' \
    | sort -u > "$WORK/syms.txt"

COUNT="$(wc -l < "$WORK/syms.txt")"
echo "$COUNT undefined EGL/GL symbols -> stubbing"

for LIB in EGL GL; do
    # Symbols are matched case-insensitively on the prefix, because the EGL
    # entry points are camelCase (eglGetCurrentDisplay) and the GL ones are
    # PascalCase (glActiveTexture).
    : > "$WORK/stub.c"
    while read -r sym; do
        printf 'long %s(void) { return 0; }\n' "$sym" >> "$WORK/stub.c"
    done < <(grep -iE "^${LIB}" "$WORK/syms.txt" || true)
    if [ ! -s "$WORK/stub.c" ]; then
        echo "  lib$LIB.so.1: no symbols needed, skipping"
        continue
    fi
    gcc -shared -fPIC -o "$OUT/lib$LIB.so.1" "$WORK/stub.c"
    echo "  wrote $OUT/lib$LIB.so.1 ($(wc -l < "$WORK/stub.c") symbols)"
done

echo "done. Use it with:"
echo "  LD_LIBRARY_PATH=$OUT"
