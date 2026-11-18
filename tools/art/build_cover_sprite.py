#!/usr/bin/env python3
"""One request for the whole cover library on the web.

The picker used to ask for 175 SVGs one by one. This packs the cover files of one theme into a single
`<symbol>` sprite (`cover/light-sprite.svg`, `cover/dark-sprite.svg`), which the browser fetches once, compressed
and cached. The per-cover files stay: the Android app and the profile cover read them. Re-run after the art
export (`export_m3x_assets.js`). Check mode fails when a sprite is stale.

    python3 tools/art/build_cover_sprite.py [--check]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(ROOT, 'backend_python/web/static/web/img/m3x')
INNER = re.compile(r'^<svg[^>]*>(.*)</svg>\s*$', re.S)


def build(theme):
    ids = [r[0] for r in json.load(open(os.path.join(BASE, 'covers.json')))['covers']]
    out = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for cid in ids:
        text = open(os.path.join(BASE, 'cover', theme, cid + '.svg'), encoding='utf-8').read().strip()
        m = INNER.match(text)
        if not m:
            raise SystemExit('unexpected svg shape: %s/%s' % (theme, cid))
        out.append('<symbol id="%s" viewBox="0 0 1200 400" preserveAspectRatio="xMidYMid slice">%s</symbol>' % (cid, m.group(1)))
    out.append('</svg>\n')
    return ''.join(out)


def main():
    check = '--check' in sys.argv
    bad = 0
    for theme in ('light', 'dark'):
        path = os.path.join(BASE, 'cover', theme + '-sprite.svg')
        want = build(theme)
        have = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
        if have == want:
            print(theme, 'up to date', len(want))
        elif check:
            print(theme, 'STALE'); bad = 1
        else:
            open(path, 'w', encoding='utf-8').write(want)
            print(theme, 'written', len(want))
    sys.exit(bad)


main()
