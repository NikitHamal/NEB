#!/usr/bin/env python3
"""Regenerate the two logo cuts the Open Graph cards draw (web/og_logo.py).

Only needs running when n-logo-tight.svg changes. cairosvg is a build-time
tool, not a backend dependency -- the PNGs it writes are committed, so a
deploy of the site never needs a cairo in the box.

    python3 tools/og/build_logo.py
"""
import io
import os
import sys

try:
    import cairosvg
except ImportError:
    sys.exit('cairosvg is needed to rasterise the SVG: pip install cairosvg')

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, 'backend_python', 'web', 'static', 'web', 'img')
SOURCE = os.path.join(IMG, 'n-logo-tight.svg')
HEIGHT = 900            # 2x the tallest on-card use, so cards downsample


def main():
    png = cairosvg.svg2png(url=SOURCE, output_width=int(HEIGHT * 1.4),
                           background_color='transparent')
    art = Image.open(io.BytesIO(png)).convert('RGBA')
    box = art.getchannel('A').getbbox()
    if not box:
        sys.exit('the SVG rasterised empty')
    art = art.crop(box)
    scale = HEIGHT / float(art.size[1])
    art = art.resize((max(1, int(round(art.size[0] * scale))), HEIGHT), Image.LANCZOS)
    art.save(os.path.join(IMG, 'n-logo-og.png'), optimize=True)

    mono = Image.new('RGBA', art.size, (255, 255, 255, 0))
    mono.putalpha(art.getchannel('A'))
    mono.save(os.path.join(IMG, 'n-logo-og-mono.png'), optimize=True)

    print('n-logo-og.png    %dx%d' % art.size)
    print('n-logo-og-mono.png %dx%d' % mono.size)


if __name__ == '__main__':
    main()
