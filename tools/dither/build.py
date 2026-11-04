#!/usr/bin/env python3
"""Render the dither art set.

    python3 tools/dither/build.py              # everything -> web/static/web/art/dither/ + dither.json
    python3 tools/dither/build.py moon-orb     # only matching slugs
    python3 tools/dither/build.py --sheet /tmp/sheet.png   # also a contact sheet for a quick look

Needs numpy and Pillow. Every piece is deterministic.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'backend_python', 'web', 'static', 'web', 'art', 'dither')

from engine import Canvas  # noqa: E402
from kit import REG, P  # noqa: E402
import scenes_a, scenes_b, scenes_c  # noqa: E402,F401

METHODS = {
    'bayer2': 'Ordered 2x2', 'bayer4': 'Ordered 4x4', 'bayer8': 'Ordered 8x8', 'floyd': 'Floyd-Steinberg',
    'atkinson': 'Atkinson', 'jjn': 'Jarvis', 'sierra': 'Sierra', 'blue': 'Blue noise', 'white': 'White noise',
    'halftone': 'Halftone', 'lines': 'Line screen', 'cross': 'Cross hatch', 'radial': 'Radial', 'spiral': 'Spiral',
    'ign': 'Gradient noise',
}


def render(item, variant):
    pal_name, method, kw = variant
    c = Canvas(item['w'], item['h'], '#000000', seed=1)
    item['fn'](c, P[pal_name], method, **kw)
    return c


def main(argv):
    sheet = None
    only = []
    i = 0
    while i < len(argv):
        if argv[i] == '--sheet':
            sheet = argv[i + 1]
            i += 2
        else:
            only.append(argv[i])
            i += 1
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    thumbs = []
    for item in REG:
        if only and not any(o in item['slug'] for o in only):
            continue
        for pal_name, method, kw in item['variants']:
            c = render(item, (pal_name, method, kw))
            name = '%s-%s' % (item['slug'], pal_name)
            im = c.image(item['scale'])
            im.save(os.path.join(OUT, name + '.png'), optimize=True)
            thumbs.append(im)
            if name == 'dune-library-bone':
                import numpy as np
                from PIL import Image
                a = (np.asarray(im.convert('L')) > 128).astype(np.uint8) * 255
                m = np.zeros(a.shape + (4,), dtype=np.uint8)
                m[..., 3] = a
                Image.fromarray(m, 'RGBA').save(os.path.join(OUT, 'cover-dunes-mask.png'), optimize=True)
            manifest.append({
                'slug': name, 'title': item['title'], 'era': item['era'], 'palette': pal_name,
                'colors': P[pal_name].hex, 'method': method, 'method_label': METHODS.get(method, method),
                'w': im.width, 'h': im.height, 'cells': '%dx%d' % (item['w'], item['h']),
                'file': 'dither/%s.png' % name,
            })
            print(name, im.size)
    if not only:
        with open(os.path.join(os.path.dirname(OUT), 'dither.json'), 'w', encoding='utf-8') as fh:
            json.dump({'items': manifest}, fh, indent=1)
    if sheet and thumbs:
        from PIL import Image
        th = 260
        ims = [t.resize((int(t.width * th / t.height), th), Image.NEAREST) for t in thumbs]
        cols = 8
        rows = (len(ims) + cols - 1) // cols
        cw = max(i.width for i in ims)
        S = Image.new('RGB', (cols * cw, rows * th), (30, 30, 30))
        for n, im in enumerate(ims):
            S.paste(im, ((n % cols) * cw, (n // cols) * th))
        S.save(sheet)


if __name__ == '__main__':
    main(sys.argv[1:])
