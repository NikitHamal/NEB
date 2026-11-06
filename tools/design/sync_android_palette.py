#!/usr/bin/env python3
"""Copy the m3x colour roles from the web tokens into the Android Palette.kt.

Source of truth: backend_python/web/static/web/css/m3x/tokens.css (:root = light,
[data-theme="dark"] = dark). Roles the web does not define (error, scrim, the
secondary fixed set) are left alone. Run with --check to fail on drift.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKENS = ROOT / "backend_python/web/static/web/css/m3x/tokens.css"
PALETTE = ROOT / "app/src/main/java/com/neb/ians/ui/theme/Palette.kt"


# The app's light page is paper white; the web keeps its blue-tinted page and lifts
# raised surfaces to white instead. Cards on Android are outlined or tonal on white.
ANDROID_LIGHT_OVERRIDES = {"background": "FFFFFF", "surface": "FFFFFF"}


def camel(name):
    head, *rest = name.split("-")
    return head + "".join(p.capitalize() for p in rest)


def block(css, opener):
    start = css.index(opener)
    depth, i = 0, css.index("{", start)
    begin = i
    while True:
        depth += css[i] == "{"
        depth -= css[i] == "}"
        i += 1
        if depth == 0:
            return css[begin:i]


def roles(body):
    out = {}
    for m in re.finditer(r"--md-([a-z-]+):\s*(#[0-9a-fA-F]{6})", body):
        out[camel(m.group(1))] = m.group(2).upper().lstrip("#")
    return out


def main():
    css = TOKENS.read_text()
    light = roles(block(css, ":root"))
    dark = {**light, **roles(block(css, '[data-theme="dark"]'))}
    src = PALETTE.read_text()
    new = src

    def sub(prefix, role, hexv):
        nonlocal new
        pat = re.compile(r"(val %s_%s = Color\(0xFF)[0-9A-Fa-f]{6}(\))" % (prefix, role))
        new = pat.sub(lambda m: m.group(1) + hexv + m.group(2), new)

    for role, hexv in {**light, **ANDROID_LIGHT_OVERRIDES}.items():
        sub("md_theme_light", role, hexv)
    for role, hexv in dark.items():
        sub("md_theme_dark", role, hexv)
    for role in ("primaryFixed", "primaryFixedDim", "onPrimaryFixed", "onPrimaryFixedVariant",
                 "tertiaryFixed", "tertiaryFixedDim", "onTertiaryFixed", "onTertiaryFixedVariant"):
        if role in light:
            pat = re.compile(r"(val md_theme_%s = Color\(0xFF)[0-9A-Fa-f]{6}(\))" % role)
            new = pat.sub(lambda m: m.group(1) + light[role] + m.group(2), new)
    if "--check" in sys.argv:
        sys.exit(0 if new == src else 1)
    PALETTE.write_text(new)


main()
