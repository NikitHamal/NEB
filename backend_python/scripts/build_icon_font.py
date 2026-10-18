"""Rebuild the self-hosted Material Symbols subset (web/static/web/fonts/app/).

The full font is about 460 KB; the site uses a few hundred icons, so we ship only those
(about 90 KB). Run this after adding an icon that web/test_icon_font.py reports missing:

    pip install fonttools brotli
    python scripts/build_icon_font.py [extra_icon ...]

Every word in the templates, scripts and Python files that is also an icon name is kept,
which over-includes a little and never misses a literal icon name.
"""
import os
import re
import sys
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/static/web/fonts/app'
CSS = ('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:'
       'opsz,wght,FILL,GRAD@24,400,0..1,0&display=block')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36'}
SKIP = ('node_modules', 'venv', 'scratch', 'staticfiles', 'media')


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def ligatures(font):
    cmap, out = font.getBestCmap(), {}
    for lookup in font['GSUB'].table.LookupList.Lookup:
        for st in lookup.SubTable:
            st = getattr(st, 'ExtSubTable', st)
            if getattr(st, 'LookupType', None) != 4:
                continue
            for first, ligs in st.ligatures.items():
                for lig in ligs:
                    out[tuple([first] + list(lig.Component))] = lig.LigGlyph
    return cmap, out


def main(extra):
    full = OUT / 'material-symbols-full.woff2'
    url = re.search(rb'url\((https://[^)]+)\)', fetch(CSS)).group(1).decode()
    full.write_bytes(fetch(url))
    font = TTFont(full)
    cmap, ligs = ligatures(font)
    words = set(extra)
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for name in files:
            if name.endswith(('.html', '.js', '.py', '.css', '.json')) and not name.endswith('.min.js'):
                text = Path(root, name).read_text(encoding='utf-8', errors='ignore')
                words.update(re.findall(r'[a-z][a-z0-9_]{1,40}', text))
    used, glyphs = [], set()
    names = set(font.getGlyphOrder())
    for word in sorted(words):
        glyph = ligs.get(tuple(cmap.get(ord(c)) for c in word))
        if glyph and len(word) > 1:
            used.append(word)
            glyphs.update(g for g in (glyph, glyph + '.fill') if g in names)
    options = subset.Options()
    options.layout_closure = False
    options.layout_features = ['*']
    options.flavor = 'woff2'
    sub = subset.Subsetter(options)
    sub.populate(glyphs=sorted(glyphs), text='abcdefghijklmnopqrstuvwxyz0123456789_')
    sub.subset(font)
    font.save(OUT / 'material-symbols-outlined.woff2')
    (OUT / 'material-symbols-outlined.txt').write_text('\n'.join(used) + '\n')
    full.unlink()
    print(f'{len(used)} icons, {(OUT / "material-symbols-outlined.woff2").stat().st_size // 1024} KB')


if __name__ == '__main__':
    main(sys.argv[1:])
