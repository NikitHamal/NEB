"""The NEBians mark, pre-rasterised for the Open Graph cards.

The card drawing has no SVG renderer at runtime -- cairosvg is not a
dependency of the backend, and adding one for a logo would mean shipping a
native library for a picture that never changes. So the two cuts the cards
need are built once by tools/og/build_logo.py from n-logo-tight.svg and
committed next to it. Only Pillow is needed at render time.

Two cuts:

* ``n-logo-og.png``  -- the mark as drawn, transparent background.
* ``n-logo-og-mono.png`` -- the same silhouette in one colour, so a card can
  set it in paper white on a dark ground without repainting the gradients.

Both are cropped to their alpha box, so a caller asks for a height and gets a
picture whose edges are the ink -- no guessing at padding.
"""
from __future__ import annotations

import os
from functools import lru_cache

from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/web/img')
COLOUR_FILE = 'n-logo-og.png'
MONO_FILE = 'n-logo-og-mono.png'

ASPECT = 0.6837  # width / height of the cropped mark, measured on the master


@lru_cache(maxsize=8)
def _load(filename: str) -> Image.Image:
    img = Image.open(os.path.join(IMG_DIR, filename)).convert('RGBA')
    box = img.getchannel('A').getbbox()
    return img.crop(box) if box else img


@lru_cache(maxsize=64)
def mark(height: int, mono: bool = False) -> Image.Image:
    """The logo, `height` pixels tall, transparent around it."""
    img = _load(MONO_FILE if mono else COLOUR_FILE)
    height = max(8, int(height))
    width = max(1, int(round(height * img.size[0] / float(img.size[1]))))
    return img.resize((width, height), Image.LANCZOS)


