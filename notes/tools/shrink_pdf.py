#!/usr/bin/env python3
"""Shrink a built book so it can be pushed through the connector.

The AgentSky connector rejects a single blob body above roughly 27 MB, and the
byte-for-byte base64 encoding adds a third on top. A 52 MB book therefore cannot
be committed as it stands. This tool re-encodes the embedded raster images at a
sensible screen resolution and JPEG quality and saves a new file, which is
lossless for the vector drawings, the maths and the text.

    python3 shrink_pdf.py <in.pdf> [out.pdf] [--target-mb 22]

Figures in these books are SVG (converted to vector paths by matplotlib), so the
only thing that changes is the resolution of the photographs, which are stored
at 1200-1300 px wide and never displayed larger than about 500 px.
"""
import os
import sys

import pymupdf


def shrink(src, dst=None, target_mb=22.0, verbose=True):
    dst = dst or src
    doc = pymupdf.open(src)
    before = os.path.getsize(src) / 1e6
    # dpi_target: photos are placed at about 90-100 mm wide, so 150 dpi already
    # gives more pixels than the print size needs; dpi_threshold leaves small
    # images alone.
    doc.rewrite_images(dpi_threshold=200, dpi_target=150, quality=72)
    tmp = dst + ".tmp"
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    os.replace(tmp, dst)
    after = os.path.getsize(dst) / 1e6
    if verbose:
        print("%-58s %.1f MB -> %.1f MB" % (os.path.basename(dst), before, after))
    return after


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tgt = 22.0
    for a in sys.argv[1:]:
        if a.startswith("--target-mb"):
            tgt = float(a.split("=", 1)[1])
    if not args:
        raise SystemExit(__doc__)
    source = args[0]
    dest = args[1] if len(args) > 1 else None
    size = shrink(source, dest, tgt)
    if size > 25.0:
        print("STILL TOO BIG: %.1f MB — lower dpi_target/quality" % size)
        sys.exit(1)
