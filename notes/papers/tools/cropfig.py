"""Crop one figure out of a cached page image, clean it, save it under notes/papers/figures/.

    python3 cropfig.py <cache-key> <page> x0 y0 x1 y1 <out-name> [--scale 3] [--lo 70] [--hi 150]

Coordinates are pixels of /tmp/psrc/<key>/p<page>.jpg. The crop is converted to grey, up-scaled and the levels are
stretched (lo..hi) so a faint overlay (paper-aggregator watermark) drops out to white while the ink stays dark.
Only the figure region is cropped, so no logo or caption text ends up in the output.
Use it in a paper as:   ![caption](figures/<out-name>.png){width=45%}   -> see build_paper.py (@img blocks).
"""
import sys, os
from PIL import Image, ImageFilter

CACHE = os.environ.get("PAPER_CACHE", "/tmp/psrc")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")


def crop(key, page, box, name, scale=3, lo=70, hi=150, keep_colour=False):
    im = Image.open(os.path.join(CACHE, key, f"p{page}.jpg")).convert("RGB").crop(box)
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    g = im.convert("L").point(lambda v: 0 if v <= lo else 255 if v >= hi else int((v - lo) * 255 / (hi - lo)))
    g = g.filter(ImageFilter.GaussianBlur(0.6)).point(lambda v: 0 if v < 100 else 255 if v > 190 else int((v - 100) * 255 / 90))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name + ".png")
    g.save(p, optimize=True)
    return p


if __name__ == "__main__":
    a = sys.argv[1:]
    opts = {a[i][2:]: int(a[i + 1]) for i in range(len(a)) if a[i].startswith("--")}
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or not a[i - 1].startswith("--"))]
    key, page, x0, y0, x1, y1, name = pos[:7]
    print(crop(key, page, tuple(int(v) for v in (x0, y0, x1, y1)), name, **opts))
