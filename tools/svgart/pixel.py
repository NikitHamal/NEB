#!/usr/bin/env python3
"""The pixel look, made from the flat scenes.

Each flat SVG (without its paper grain) is rendered by Chromium at a pixel-art resolution, its
colours reduced to a small palette, and every pixel snapped to the nearest palette colour or
dithered between the two nearest with a 4x4 Bayer matrix, which is how pixel art fakes a
gradient. The result is written back as SVG: one path per colour made of horizontal runs, drawn
crisp at any size.

    /tmp/pw/bin/python tools/svgart/pixel.py      (needs Playwright's Chromium and Pillow)
then re-run build.py so the manifest lists the pixel files.
"""
import asyncio
import io
import json
import os
import re
import sys

from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(ROOT, "backend_python", "web", "static", "web", "art")

# pixels across, per set: the app's own pixel-art sizes where it has them
GRID = {"covers": 300, "banners": 200, "onboarding": 150, "empty": 112, "backgrounds": None}
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]
COLOURS = 28


def grid_for(key, w, h):
    across = GRID[key] or (108 if h > w else 200)
    return across, max(1, round(across * h / w))


def dither(img):
    """Ordered dithering against an adaptive palette."""
    # flat areas first: the commonest exact colours go into the palette as they are, so a flat
    # ground maps to itself instead of falling between two entries and dithering into a checker
    counts = sorted(img.getcolors(img.size[0] * img.size[1]), reverse=True)
    pal = []
    for n, c in counts:
        if n < img.size[0] * img.size[1] * 0.004 or len(pal) >= COLOURS - 8:
            break
        if all(sum((a - b) ** 2 for a, b in zip(c, m)) > 14 ** 2 for m in pal):
            pal.append(tuple(c[:3]))
    # then max-coverage for the rest: small saturated details (an eye, a flower, a flag)
    q = img.quantize(colors=COLOURS, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE).getpalette()[:COLOURS * 3]
    for c in (tuple(q[i:i + 3]) for i in range(0, len(q), 3)):
        if len(pal) < COLOURS and all(sum((a - b) ** 2 for a, b in zip(c, m)) > 22 ** 2 for m in pal):
            pal.append(c)
    w, h = img.size
    src = img.load()
    out = [[None] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            c = src[x, y][:3]
            d = sorted(((sum((a - b) ** 2 for a, b in zip(c, p)), i) for i, p in enumerate(pal)))
            (d0, i0), (d1, i1) = d[0], d[1]
            # dither only inside a gradient (the two nearest colours are neighbours on a ramp);
            # an anti-aliased edge between unrelated colours just snaps, so outlines stay clean
            gap = sum((a - b) ** 2 for a, b in zip(pal[i0], pal[i1])) ** 0.5
            t = (d0 ** 0.5) / max(1e-6, d0 ** 0.5 + d1 ** 0.5)
            thr = (BAYER[(y & 3) * 4 + (x & 3)] + 0.5) / 16
            out[y][x] = pal[i1] if gap < 75 and t > thr else pal[i0]
    return out


def outline(px, w, h, bg):
    """Pixel art reads by its outlines: every ground pixel (the ground colour or one close to it)
    touching a strong foreground colour becomes a darker shade of that colour."""
    def d2(a, b):
        return sum((x - y) ** 2 for x, y in zip(a, b))
    groundish = [[d2(px[y][x], bg) < 40 ** 2 for x in range(w)] for y in range(h)]
    out = [row[:] for row in px]
    for y in range(h):
        for x in range(w):
            if not groundish[y][x]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and not groundish[yy][xx] and d2(px[yy][xx], bg) > 90 ** 2:
                    out[y][x] = tuple(int(v * 0.5) for v in px[yy][xx])
                    break
    return out


def to_svg(px, w, h, scale, title):
    runs = {}
    for y in range(h):
        x = 0
        while x < w:
            c = px[y][x]
            x2 = x
            while x2 + 1 < w and px[y][x2 + 1] == c:
                x2 += 1
            runs.setdefault(c, []).append("M%d %dh%dv1h-%dz" % (x, y, x2 - x + 1, x2 - x + 1))
            x = x2 + 1
    body = "".join('<path fill="#%02x%02x%02x" d="%s"/>' % (c[0], c[1], c[2], "".join(r)) for c, r in sorted(runs.items(), key=lambda kv: -len(kv[1])))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" shape-rendering="crispEdges" '
            'style="image-rendering:pixelated"><title>%s</title>%s</svg>' % (w, h, w * scale, h * scale, title, body))


async def main():
    manifest = json.load(open(os.path.join(ART, "manifest.json")))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page()
        for st in manifest["sets"]:
            for it in st["items"]:
                src = os.path.join(ART, it["files"]["flat"])
                svg = open(src, encoding="utf-8").read()
                svg = re.sub(r'<rect[^>]*filter="url\(#paper\)"[^>]*/>', "", svg)   # no paper grain in pixels
                gw, gh = grid_for(st["key"], it["w"], it["h"])
                await page.set_viewport_size({"width": gw, "height": gh})
                html = '<html><body style="margin:0">%s</body></html>' % svg.replace(
                    'width="%d" height="%d"' % (it["w"], it["h"]), 'width="%d" height="%d"' % (gw, gh), 1)
                await page.set_content(html)
                shot = await page.screenshot(clip={"x": 0, "y": 0, "width": gw, "height": gh})
                img = Image.open(io.BytesIO(shot)).convert("RGB")
                px = dither(img)
                # the ground colour is the commonest one along the top edge
                top = [px[0][x] for x in range(gw)]
                bg = max(set(top), key=top.count)
                if st["key"] in ("banners", "empty", "onboarding"):
                    px = outline(px, gw, gh, bg)
                scale = max(1, round(it["w"] / gw))
                rel = "%s/%s-pixel.svg" % (st["key"], it["name"])
                with open(os.path.join(ART, rel), "w", encoding="utf-8") as fh:
                    fh.write(to_svg(px, gw, gh, scale, "%s %s (pixel)" % (st["title"], it["name"])))
                print(rel, gw, gh)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main())
