"""M3 Expressive shapes and glyphs for the Open Graph cards.

Flat only: no gradient, no glow, no shadow, no grain, no stroke on a portrait.
A card is a light surface, one big tonal shape on the right, one solid accent
shape inside it, and a plain white glyph that says what the page is about.
No Django and no isometric solids; Pillow only.
"""
from __future__ import annotations

import math
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw

from . import og_logo

Colour = Tuple[int, int, int]


def mix(a, b, t: float):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def lum(c) -> float:
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def roles(accent) -> dict:
    """Role pairs from one subject colour: fill + on-fill, container + on-container."""
    a = tuple(accent)
    while lum(a) > 0.2:
        a = mix(a, (0, 0, 0), 0.12)
    white = (255, 255, 255)
    return {
        'accent': a,
        'on_accent': white,
        'surface': mix(white, a, 0.035),
        'container': mix(white, a, 0.12),
        'container_hi': mix(white, a, 0.24),
        'on_container': mix(a, (0, 0, 0), 0.55),
        'ink': (18, 21, 27),
        'muted': (75, 83, 97),
        'chip': mix(white, a, 0.10),
    }


# ── Shapes (polygons, drawn supersampled) ────────────────────────────────
def cookie(cx, cy, r, lobes=9, depth=0.07, rot=0.0, n=360) -> List[Tuple[float, float]]:
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        rr = r * (1 + depth * math.cos(lobes * th + rot))
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    return pts


def squircle(cx, cy, r, p=4.4, rot=0.0, n=300) -> List[Tuple[float, float]]:
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        c, s = math.cos(th), math.sin(th)
        x = r * math.copysign(abs(c) ** (2 / p), c)
        y = r * math.copysign(abs(s) ** (2 / p), s)
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot),
                    cy + x * math.sin(rot) + y * math.cos(rot)))
    return pts


def star4(cx, cy, r, pinch=0.22, n=240):
    """Four-point sparkle with concave sides."""
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        k = abs(math.cos(2 * th))
        rr = r * (pinch + (1 - pinch) * k ** 1.7)
        pts.append((cx + rr * math.cos(th - math.pi / 2), cy + rr * math.sin(th - math.pi / 2)))
    return pts


def _scale(pts, s):
    return [(x * s, y * s) for x, y in pts]


def poly(d: ImageDraw.ImageDraw, pts, fill, ss: int):
    d.polygon(_scale(pts, ss), fill=tuple(fill) + (255,))


def rrect(d, box, radius, fill, ss: int):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 * ss, y0 * ss, x1 * ss, y1 * ss), radius=radius * ss,
                        fill=tuple(fill) + (255,))


# ── Glyphs: drawn white inside the solid accent shape, centred on (cx, cy) ──
def glyph(name: str, d: ImageDraw.ImageDraw, canvas: Image.Image, cx, cy, u, c: dict, ss: int, font_fn):
    """`u` is the half-size of the glyph box in card pixels."""
    W = (255, 255, 255)
    T = mix(c['accent'], W, 0.55)       # tint on the accent fill
    if name == 'books':
        rrect(d, (cx - u, cy + u * .18, cx + u * .86, cy + u * .62), u * .16, W, ss)
        rrect(d, (cx - u * .82, cy - u * .34, cx + u, cy + u * .10), u * .16, T, ss)
        rrect(d, (cx - u * .94, cy - u * .86, cx + u * .72, cy - u * .42), u * .16, W, ss)
    elif name == 'paper':
        rrect(d, (cx - u * .66, cy - u, cx + u * .66, cy + u), u * .22, W, ss)
        for i, w in enumerate((.82, .82, .82, .5)):
            y = cy - u * .56 + i * u * .30
            rrect(d, (cx - u * .42, y, cx - u * .42 + u * w * .84, y + u * .13), u * .065, T if i else c['accent'], ss)
    elif name == 'bubbles':
        rrect(d, (cx - u, cy - u * .78, cx + u * .30, cy + u * .12), u * .34, W, ss)
        poly(d, [(cx - u * .66, cy + u * .05), (cx - u * .72, cy + u * .50), (cx - u * .28, cy + u * .05)], W, ss)
        rrect(d, (cx - u * .12, cy - u * .06, cx + u, cy + u * .66), u * .30, T, ss)
        poly(d, [(cx + u * .64, cy + u * .56), (cx + u * .76, cy + u * .96), (cx + u * .34, cy + u * .58)], T, ss)
    elif name == 'flask':
        rrect(d, (cx - u * .22, cy - u, cx + u * .22, cy - u * .1), u * .08, W, ss)
        poly(d, [(cx - u * .18, cy - u * .2), (cx + u * .18, cy - u * .2),
                 (cx + u * .86, cy + u * .62), (cx + u * .70, cy + u * .92),
                 (cx - u * .70, cy + u * .92), (cx - u * .86, cy + u * .62)], W, ss)
        poly(d, [(cx - u * .56, cy + u * .34), (cx + u * .56, cy + u * .34),
                 (cx + u * .70, cy + u * .62), (cx + u * .58, cy + u * .78),
                 (cx - u * .58, cy + u * .78), (cx - u * .70, cy + u * .62)], T, ss)
        rrect(d, (cx - u * .34, cy - u * 1.02, cx + u * .34, cy - u * .86), u * .08, W, ss)
    elif name == 'graph':
        hs = (.50, .92, .70, 1.5)
        for i, h in enumerate(hs):
            x = cx - u + i * u * .54
            rrect(d, (x, cy + u * .85 - h * u * .95, x + u * .38, cy + u * .85), u * .12, W if i % 2 == 0 else T, ss)
    elif name == 'question':
        f = font_fn('bold', int(u * 2.2 * ss))
        bb = d.textbbox((0, 0), '?', font=f)
        d.text((cx * ss - (bb[0] + bb[2]) / 2, cy * ss - (bb[1] + bb[3]) / 2), '?', font=f, fill=W + (255,))
    elif name == 'cards':
        rrect(d, (cx - u * .86, cy - u * .86, cx + u * .30, cy + u * .20), u * .24, T, ss)
        rrect(d, (cx - u * .30, cy - u * .20, cx + u * .86, cy + u * .86), u * .24, W, ss)
        for i, w in enumerate((.9, .6)):
            y = cy + u * .04 + i * u * .30
            rrect(d, (cx - u * .10, y, cx - u * .10 + u * w * .8, y + u * .13), u * .065, c['accent'] if i == 0 else T, ss)
    elif name == 'spark':
        poly(d, star4(cx - u * .12, cy + u * .08, u * 1.0), W, ss)
        poly(d, star4(cx + u * .70, cy - u * .66, u * .38), T, ss)
    else:   # 'mark': the real logo on a white tile
        tile = u * 1.7
        poly(d, squircle(cx, cy, tile / 2, 4.6), W, ss)
        art = og_logo.mark(int(tile * .62 * ss))
        canvas.alpha_composite(art, (int(cx * ss - art.size[0] / 2), int(cy * ss - art.size[1] / 2)))


def portrait(canvas: Image.Image, avatar: Optional[Image.Image], cx, cy, r, c: dict, ss: int, font_fn):
    """Expressive-shaped portrait (a cookie), never a circle, never a stroke."""
    size = int(r * 2 * ss)
    tile = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    if avatar is None:
        td = ImageDraw.Draw(tile)
        td.rectangle((0, 0, size, size), fill=tuple(c['accent']) + (255,))
        f = font_fn('bold', int(size * .5))
        bb = td.textbbox((0, 0), 'N', font=f)
        td.text(((size - (bb[2] - bb[0])) / 2 - bb[0], (size - (bb[3] - bb[1])) / 2 - bb[1]), 'N',
                font=f, fill=(255, 255, 255, 255))
    else:
        from PIL import ImageOps
        tile = ImageOps.fit(avatar.convert('RGBA'), (size, size), method=Image.LANCZOS, centering=(0.5, 0.36))
    mask = Image.new('L', (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(_scale(cookie(r, r, r * .93, 10, .055, .2), ss), fill=255)
    tile.putalpha(mask)
    canvas.alpha_composite(tile, (int((cx - r) * ss), int((cy - r) * ss)))
