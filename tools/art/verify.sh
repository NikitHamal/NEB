#!/usr/bin/env sh
# Regenerates neb-art.js from the shipping Kotlin and proves the two platforms
# draw the same picture. Run this after touching ResourceBannerArt.kt,
# ProfileCoverArt.kt, or Color.kt -- the generated JS is checked in, so it does
# not update itself.
set -e
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

echo "== generating =="
python3 "$HERE/genjs.py"
node --check "$HERE/../../backend_python/web/static/web/js/neb-art.js"
python3 "$HERE/gensubjects.py"

echo "== recording call streams =="
node "$HERE/rec.js" > "$HERE/js.json"
python3 "$HERE/recpy.py"

echo "== diffing Kotlin vs JS =="
python3 "$HERE/cmp.py"

echo "== browser-path smoke test =="
node "$HERE/smoke.js"

echo "== subject routing: art vs CSS class vs icon =="
python3 "$HERE/cmpsubjects.py"
