"""The drawing half of the Open Graph cards.

Everything here is geometry and pixels; nothing knows about Django, the
database or routes. `og_cards` composes; this module draws.

The house language is the logo's own: the NEBians mark is an isometric book-N,
so the cards are built from the same projection -- 30-degree axes, three visible
faces per solid, a light top, a mid left, a dark right, and a paper-white rim on
every edge. That is why a card for Physics and a card for the library look like
they came from the same hand instead of from the same template.

Drawn at SS times the final size and resampled down: PIL has no antialiasing of
its own, so supersampling is what keeps the diagonals clean at 300px wide, which
is where most people will actually see these.
"""
from __future__ import annotations

import math
import random
from typing import Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFilter

SS = 2
W, H = 1200, 630

ISO_COS = math.cos(math.radians(30))   # 0.8660
ISO_SIN = math.sin(math.radians(30))   # 0.5

# ── Ink ───────────────────────────────────────────────────────────────────
# The card ground is a night sky rather than paper. Two reasons: the mark is a
# lit object and only reads against something dark, and a dark card is the one
# that stands out in a feed of white ones.
INK_TOP = (10, 16, 31)
INK_BOTTOM = (5, 8, 18)
INK_LINE = (255, 255, 255)


def mix(a, b, t: float):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def lum(c) -> float:
    """Perceived brightness, 0..255. Used to lift a subject colour until it is
    legible on ink without losing which subject it is."""
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def lift(c, to: float = 168.0):
    """The same hue, bright enough to sit on the ink."""
    if lum(c) >= to:
        return c
    lo, hi = 0.0, 1.0
    for _ in range(18):
        mid = (lo + hi) / 2
        if lum(mix(c, (255, 255, 255), mid)) < to:
            lo = mid
        else:
            hi = mid
    return mix(c, (255, 255, 255), hi)


def saturate(c, amount: float = 1.25):
    """Push a hue away from grey. Subject tints arrive pale; on ink a pale
    colour reads as white, and white reads as no subject at all."""
    grey = (lum(c),) * 3
    return tuple(max(0, min(255, int(round(grey[i] + (c[i] - grey[i]) * amount))))
                 for i in range(3))


# ── Determinism ───────────────────────────────────────────────────────────

class Rng:
    """The same 32-bit LCG the app and neb-art.js use, so a seed means the same
    picture everywhere it is drawn."""

    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF or 0x9E3779B9

    def next(self) -> float:
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0

    def between(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.next()

    def pick(self, seq: Sequence):
        return seq[int(self.next() * len(seq)) % len(seq)]


# ── Ground ────────────────────────────────────────────────────────────────

def _vertical(w: int, h: int, top, bottom) -> Image.Image:
    strip = Image.new('RGB', (1, h))
    px = strip.load()
    for y in range(h):
        px[0, y] = mix(top, bottom, y / max(1, h - 1))
    return strip.resize((w, h), Image.BILINEAR)


def radial_glow(size: int, colour, alpha: int, falloff: float = 2.1) -> Image.Image:
    """A soft disc. Drawn small and upscaled -- a gaussian this wide is both
    slower and no smoother."""
    n = 96
    img = Image.new('L', (n, n), 0)
    px = img.load()
    c = (n - 1) / 2.0
    for y in range(n):
        for x in range(n):
            d = math.hypot(x - c, y - c) / c
            if d >= 1:
                continue
            v = (1 - d) ** falloff
            px[x, y] = int(v * 255)
    if alpha < 255:
        img = img.point(lambda v: int(v * alpha / 255))
    disc = Image.new('RGBA', (n, n), colour + (0,))
    disc.putalpha(img)
    return disc.resize((size, size), Image.BICUBIC)


def isometric_grid(w: int, h: int, step: float, colour, alpha: int) -> Image.Image:
    """Faint 30-degree diagonals. The same lattice the logo is built on, kept
    far enough under the surface that it registers as texture, not paper."""
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    colour = colour + (alpha,)
    run = int((w + h) / math.tan(math.radians(30))) + 1
    n = 0
    x = -run
    while x < w + run:
        d.line([(x, 0), (x + run * 0.5774, h)], fill=colour, width=1)
        x += step * 1.1547
        n += 1
    y = -run
    while y < h + run:
        d.line([(0, y), (w, y + w * 0.5774)], fill=colour, width=1)
        y += step * 1.1547
    return layer


def grain(size: Tuple[int, int], amount: int, seed: int) -> Image.Image:
    """Film grain. A flat dark gradient bands on an 8-bit PNG; a little
    noise is what makes it read as a photograph of a surface."""
    w, h = size
    rnd = random.Random(seed)
    small = Image.new('L', (max(1, w // 2), max(1, h // 2)))
    small.putdata([128 + int(rnd.gauss(0, amount)) for _ in range(small.size[0] * small.size[1])])
    return small.resize((w, h), Image.NEAREST)


def ground(w: int, h: int, accent, rng: Rng, glow_at=(0.80, 0.46), glow_r=0.92) -> Image.Image:
    """The card's sky: a vertical gradient, a subject-coloured light behind the
    hero, a lattice, a vignette and grain."""
    canvas = _vertical(w, h, INK_TOP, INK_BOTTOM).convert('RGBA')

    halo = radial_glow(int(min(w, h) * glow_r), saturate(accent, 1.15),
                       alpha=64, falloff=2.3)
    canvas.alpha_composite(halo, (int(w * glow_at[0]) - halo.size[0] // 2,
                                  int(h * glow_at[1]) - halo.size[1] // 2))

    # A second, tighter core: one glow is fog, two are a light source.
    core = radial_glow(int(min(w, h) * 0.52), mix(lift(accent, 150), (255, 255, 255), 0.25),
                       alpha=54, falloff=2.6)
    canvas.alpha_composite(core, (int(w * glow_at[0]) - core.size[0] // 2,
                                  int(h * glow_at[1]) - core.size[1] // 2))

    lattice = isometric_grid(w, h, 58 * SS, (255, 255, 255), 7)
    canvas.alpha_composite(lattice)

    # Vignette: the corners fall away, so the eye goes to the type and the hero.
    vig = Image.new('L', (w, h), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse((-w * 0.28, -h * 0.42, w * 1.28, h * 1.42), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(min(w, h) * 0.10))
    shade = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shade.putalpha(vig.point(lambda v: int((255 - v) * 0.46)))
    canvas.alpha_composite(shade)

    g = grain((w, h), 7, seed=rng.state ^ 0x5EED)
    grain_layer = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    grain_layer.putalpha(g.point(lambda v: abs(v - 128)))
    canvas.alpha_composite(grain_layer, (0, 0), )
    return canvas


# ── The isometric solids ──────────────────────────────────────────────────

class Stage:
    """An isometric camera over a canvas.

    `unit` is pixels per world unit, `ox/oy` the origin on the canvas. World
    coordinates: x runs down-right, y runs down-left, z runs straight up. A
    point maps to ((x-y)cos30, (x+y)sin30 - z) -- the projection the logo was
    drawn in.
    """

    def __init__(self, canvas: Image.Image, ox: float, oy: float, unit: float):
        self.canvas = canvas
        self.ox = ox
        self.oy = oy
        self.u = unit

    def project(self, x: float, y: float, z: float) -> Tuple[float, float]:
        return (self.ox + (x - y) * ISO_COS * self.u,
                self.oy + (x + y) * ISO_SIN * self.u - z * self.u)

    def _poly(self, d: ImageDraw.ImageDraw, pts, fill, outline=None, width=0):
        d.polygon(pts, fill=fill)
        if outline and width > 0:
            d.line(list(pts) + [pts[0]], fill=outline, width=width, joint='curve')

    def box(self, x, y, z, w, d, h, palette, rim=None, rim_w=1.0):
        """rim_w is in card pixels, not world units -- an edge is an edge at
        any zoom, and scaling it with the stage made a 2px line into 25."""
        rim_w = max(1, int(round(rim_w * SS)))
        """An axis-aligned box: top, left and right faces, light from above."""
        top, left, right = palette
        p = self.project
        draw = ImageDraw.Draw(self.canvas, 'RGBA')
        # Right face (x + w)
        self._poly(draw, [p(x + w, y, z), p(x + w, y + d, z),
                          p(x + w, y + d, z + h), p(x + w, y, z + h)],
                   right, rim, rim_w)
        # Left face (y + d)
        self._poly(draw, [p(x, y + d, z), p(x + w, y + d, z),
                          p(x + w, y + d, z + h), p(x, y + d, z + h)],
                   left, rim, rim_w)
        # Top (z + h)
        self._poly(draw, [p(x, y, z + h), p(x + w, y, z + h),
                          p(x + w, y + d, z + h), p(x, y + d, z + h)],
                   top, rim, rim_w)

    def slab(self, x, y, z, w, d, h, palette, rim=None):
        """A box with softly rounded corners in plan -- a book, a card, a tile.
        Rounded by insetting a second, smaller top face: at card scale a true
        rounded prism is invisible, but a hard 90-degree corner is not."""
        self.box(x, y, z, w, d, h, palette, rim)


def face_palette(accent, deep: float = 0.46, lift_to: float = 150.0):
    """The three tones of one solid, from the subject colour.

    The relationship is the logo's: a face turned to the light, a mid face and
    a dark face. The key is that all three keep the hue -- a sculpture rendered
    in near-white reads as crockery, and the subject colour is half of what
    tells a Physics card from a Chemistry one at a glance.
    """
    base = lift(accent, lift_to)
    return (mix(base, (255, 255, 255), 0.16),      # top: catching the light
            mix(base, (0, 0, 0), deep * 0.30),      # left
            mix(base, (0, 0, 0), deep))             # right


RIM = (238, 245, 255)


def soft_shadow(canvas: Image.Image, cx: float, cy: float, rx: float, ry: float,
                alpha: int = 120) -> None:
    """The shadow an object floats over. Without it a sculpture is a sticker."""
    layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(2, 5, 14, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(max(6, int(rx * 0.22))))
    canvas.alpha_composite(layer)
