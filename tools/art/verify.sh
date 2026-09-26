#!/usr/bin/env sh
# Regenerates the web's generated assets from the shipping Kotlin and proves the two
# platforms agree. Run this after touching ResourceBannerArt.kt, ProfileCoverArt.kt,
# Color.kt or NebLiquidGlass.kt -- everything it writes is checked in, so none of
# it updates itself.
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

echo "== liquid glass: displacement maps =="
python3 "$HERE/genglassmap.py"

echo "== liquid glass: CSS, filters and maps agree with the shader =="
python3 "$HERE/checkglass.py"
