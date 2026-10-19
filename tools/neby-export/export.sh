#!/usr/bin/env bash
# Regenerates static/web/img/neby/<look>/<state>.png from the app's pixel code (no app build).
# Needs kotlinc (KOTLINC=/path/to/kotlinc/bin/kotlinc) and a JDK. Usage: export.sh [state ...]
set -e
HERE=$(cd "$(dirname "$0")" && pwd); ROOT="$HERE/../.."
P="$ROOT/app/src/main/java/com/neb/ians/ui/pixel"
KOTLINC=${KOTLINC:-kotlinc}
"$KOTLINC" -nowarn "$P/PixelCanvas.kt" "$P/PixelSprite.kt" "$P/PixelNeby.kt" "$P/PixelNebyStates.kt" "$P/PixelNebyLooks.kt" "$HERE/Export.kt" -include-runtime -d /tmp/neby-export.jar
java -cp /tmp/neby-export.jar ExportKt "$ROOT/backend_python/web/static/web/img/neby" "$@"
