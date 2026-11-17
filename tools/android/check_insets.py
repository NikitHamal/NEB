#!/usr/bin/env python3
"""Fail the build when a screen can draw under the status bar, or a ghost action row is hand-aligned.

The app is edge to edge, so every full screen has to put its first row below the status bar. The one way to do
that is `NebTopBar(...)` (it applies `statusBarsPadding()` itself). A screen that draws its own back arrow row
must use one of the markers below, or carry `// inset-ok: <reason>` in the file (embedded in a host that
already pads, a dialog, a reader with its own chrome).

Rule 2: a ghost action row (like, reply, comments) under a post or comment uses `Modifier.nebGhostRowStart()`
so its first icon sits under the left edge of the text, never 12dp inside it.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / "app/src/main/java/com/neb/ians/ui"
OK = re.compile(r"NebTopBar|statusBarsPadding|Scaffold|TopAppBar|WindowInsets\.statusBars|safeDrawing|systemBars|NebScreenHeader|inset-ok:")
bad = []
for f in list(UI.glob("screens/**/*.kt")) + list(UI.glob("sim/**/*.kt")):
    t = f.read_text()
    if "ArrowBack" in t and "Icons.AutoMirrored.Outlined.ArrowBack" in re.sub(r"^import .*$", "", t, flags=re.M) and not OK.search(t):
        bad.append(f"{f.relative_to(ROOT)}: back arrow row without NebTopBar/statusBarsPadding (clashes with the status bar)")
for f in [UI / "components/CommentCard.kt", UI / "components/PostExtras.kt", UI / "screens/resource/ResourceDetailComponents.kt"]:
    if "LikePill(" in f.read_text() and "nebGhostRowStart" not in f.read_text():
        bad.append(f"{f.relative_to(ROOT)}: LikePill row without nebGhostRowStart()")
if bad:
    print("\n".join(bad))
    sys.exit(1)
print("insets ok")
