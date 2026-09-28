#!/usr/bin/env python3
"""Make the variable fonts usable by matplotlib, which cannot read weight axes.

Inter and Noto Sans Devanagari ship as variable fonts. matplotlib picks a font
file by family + weight and has no idea a single file can be every weight, so
`fontweight="bold"` on a figure label silently resolved back to 400 and printed
`findfont: Failed to find font weight bold for Inter`. Every bold label in every
book was rendering regular.

The fix is to snap static instances out of the variable fonts once and drop them
beside the originals, where fontconfig and matplotlib both already look. Runs on
import of figrun; a no-op after the first time, and a no-op (not an error) if
fontTools is unavailable or the source fonts are somewhere else, in which case
figures render exactly as they did before.
"""
from __future__ import annotations

import os

DIR = os.path.expanduser("~/.local/share/fonts/nebians")

# (variable source, family matplotlib should see, axis values, style name)
JOBS = [
    ("Inter[opsz,wght].ttf", "Inter", {"wght": 600, "opsz": 14}, "SemiBold"),
    ("Inter[opsz,wght].ttf", "Inter", {"wght": 700, "opsz": 14}, "Bold"),
    ("NotoSansDevanagari[wdth,wght].ttf", "Noto Sans Devanagari",
     {"wght": 700, "wdth": 100}, "Bold"),
]


def _path(family: str, style: str) -> str:
    return os.path.join(DIR, f"{family.replace(' ', '')}-{style}-static.ttf")


def ensure() -> list[str]:
    """Write any missing static instances. Returns the paths that now exist."""
    made = []
    todo = [j for j in JOBS if not os.path.exists(_path(j[1], j[3]))]
    if not todo:
        return [_path(f, s) for _, f, _, s in JOBS if os.path.exists(_path(f, s))]
    try:
        from fontTools import ttLib
        from fontTools.varLib import instancer
    except ImportError:
        return []

    for src, family, axes, style in todo:
        source = os.path.join(DIR, src)
        out = _path(family, style)
        if not os.path.exists(source):
            continue
        try:
            inst = instancer.instantiateVariableFont(
                ttLib.TTFont(source), axes, inplace=False, updateFontNames=False)
            # Rewrite the name table, or matplotlib files the instance under the
            # variable font's own name and we are back where we started.
            name = inst["name"]
            for nid, val in ((1, family), (2, style), (4, f"{family} {style}"),
                             (6, f"{family}-{style}"), (16, family), (17, style)):
                name.setName(val, nid, 3, 1, 0x409)
            inst["OS/2"].usWeightClass = axes["wght"]
            if style == "Bold":
                os2 = inst["OS/2"]
                os2.fsSelection = (os2.fsSelection & ~0x40) | 0x20
                inst["head"].macStyle |= 0x01
            inst.save(out)
            made.append(out)
        except Exception:
            continue

    if made:
        # matplotlib caches the font list; it must be rebuilt to see new files.
        try:
            from matplotlib import font_manager
            font_manager._load_fontmanager(try_read_cache=False)
        except Exception:
            pass
    return made


if __name__ == "__main__":
    got = ensure()
    print(f"{len(got)} static instance(s) written" if got
          else "nothing to do (already present, or fontTools/sources missing)")
    for p in got:
        print("  " + p)
