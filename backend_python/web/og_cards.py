"""Open Graph cards, drawn rather than templated.

Every shareable URL on the site used to point at the same 1200x630 PNG of the
logo, except profiles, which had a two-panel card with a gradient slab on the
left. Neither says what the link is. A link to a Class 12 Physics past paper and
a link to the privacy policy previewed identically.

So each kind of page draws its own. The language is the one from the reference
card this was asked to follow: a paper ground, one hairline frame, a scatter of
small muted doodles, a very large bold title on the left, a dot-separated meta
line under it, and a single illustration bleeding off the right edge. Minimal
and hand-drawn rather than photographic or gradient-heavy -- an OG card is
mostly seen at 300px wide in a chat window, where a big word and one shape read
and a screenshot does not.

What makes them ours rather than a copy of the reference is where the colour
comes from: templatetags/subject_tokens.py, which is generated from the app's
Color.kt. A physics card is physics-blue in the card, in the app's banner art,
and in the subject chip on the page, because all three read the same table.

Nothing here imports Django at module level, so the drawing can be exercised
from a plain interpreter (see tools/og/preview.py).
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from typing import List, Optional, Sequence, Tuple

from PIL import Image, ImageChops, ImageDraw, ImageFont

# ── Geometry ──────────────────────────────────────────────────────────────
# Drawn at 2x and resampled down. PIL has no antialiasing of its own, so this
# is the whole reason the curves are not staircases.
W, H = 1200, 630
SS = 2

MARGIN = 96          # left text column
TEXT_MAX = 630       # title wrap width; the rest of the card is the illustration
HERO_CX, HERO_CY = 1010, 322
HERO_R = 268

# ── Colour ────────────────────────────────────────────────────────────────
PAPER = (245, 242, 235)
FRAME = (218, 215, 209)
RULE = (236, 232, 224)
INK = (24, 24, 27)
MUTED = (110, 106, 99)
BRAND = (0, 74, 198)

# Doodle colours: the reference's muted pastel set, desaturated enough that a
# dozen of them scattered over a card still read as texture rather than confetti.
CONFETTI = (
    (226, 140, 160),
    (232, 160, 96),
    (224, 190, 96),
    (122, 176, 136),
    (124, 146, 216),
    (186, 150, 206),
)

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/web/fonts')
_FONTS = {'bold': 'poppins_bold.ttf', 'medium': 'poppins_medium.ttf',
          'regular': 'poppins_regular.ttf'}
_font_cache: dict = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (weight, size)
    hit = _font_cache.get(key)
    if hit is None:
        path = os.path.join(FONT_DIR, _FONTS.get(weight, _FONTS['regular']))
        try:
            hit = ImageFont.truetype(path, size)
        except OSError:
            hit = ImageFont.load_default()
        _font_cache[key] = hit
    return hit


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


def seed_of(*parts) -> int:
    raw = '|'.join(str(p) for p in parts)
    return int(hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8], 16)


# ── Subject colour ────────────────────────────────────────────────────────

def _hex(value: str) -> Tuple[int, int, int]:
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def accent_for(subject: str) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """(ink accent, tint) for a subject, from the app's own table."""
    try:
        from .templatetags import subject_tokens
        hues = subject_tokens.subject_hue(subject or '')
    except Exception:
        hues = ('#004AC6', '#DBE1FF')
    return _hex(hues[0]), _hex(hues[1])


def mix(a, b, t: float):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


# ── Doodles ───────────────────────────────────────────────────────────────
# Each takes the 2x canvas, a centre and a radius in card units. They are drawn
# small on purpose: nothing here is above 20px on the finished card.

def _flower(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    # Five petals on a ring wide enough that they read as petals. Any tighter
    # and the discs merge into a pentagon, which is what the first pass drew.
    petal = r * 0.46
    for i in range(5):
        a = -math.pi / 2 + i * (2 * math.pi / 5)
        px, py = x + math.cos(a) * r * 0.60, y + math.sin(a) * r * 0.60
        d.ellipse((_s(px - petal), _s(py - petal), _s(px + petal), _s(py + petal)),
                  fill=colour + (200,))
    core = r * 0.26
    d.ellipse((_s(x - core), _s(y - core), _s(x + core), _s(y + core)),
              fill=mix(colour, PAPER, 0.7) + (255,))


def _sparkle(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    # A four-point star with concave sides: two crossed teardrops read as a
    # twinkle where a plain diamond reads as a lozenge.
    waist = r * 0.17
    pts = []
    for i in range(4):
        a = i * math.pi / 2
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        b = a + math.pi / 4
        pts.append((x + math.cos(b) * waist, y + math.sin(b) * waist))
    d.polygon([_s2(p) for p in pts], fill=colour + (185,))


def _plus(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    t = max(1.0, r * 0.22)
    d.rectangle((_s(x - r), _s(y - t), _s(x + r), _s(y + t)), fill=colour + (150,))
    d.rectangle((_s(x - t), _s(y - r), _s(x + t), _s(y + r)), fill=colour + (150,))


def _ring(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    d.ellipse((_s(x - r), _s(y - r), _s(x + r), _s(y + r)),
              outline=colour + (140,), width=max(1, int(r * 0.22 * SS)))


def _dot(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    r *= 0.34
    d.ellipse((_s(x - r), _s(y - r), _s(x + r), _s(y + r)), fill=colour + (175,))


def _squiggle(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    pts = []
    for i in range(25):
        t = i / 24.0
        pts.append((x - r + 2 * r * t, y + math.sin(t * math.pi * 2) * r * 0.36))
    d.line([_s2(p) for p in pts], fill=colour + (150,),
           width=max(1, int(r * 0.22 * SS)), joint='curve')


def _leaf(d: ImageDraw.ImageDraw, x: float, y: float, r: float, colour):
    box = (_s(x - r * 0.78), _s(y - r * 0.5), _s(x + r * 0.78), _s(y + r * 0.5))
    d.ellipse(box, fill=mix(colour, PAPER, 0.35) + (170,))


DOODLES = (_flower, _sparkle, _plus, _ring, _dot, _squiggle, _leaf)
# Flowers and sparkles carry the card; the rest are punctuation. Weighted so a
# scatter does not turn into a field of plus signs.
DOODLE_WEIGHTS = (_flower, _flower, _flower, _sparkle, _sparkle, _plus, _ring,
                  _dot, _dot, _squiggle, _leaf)


def _s(v: float) -> float:
    return v * SS


def _s2(p) -> Tuple[float, float]:
    return (p[0] * SS, p[1] * SS)


def scatter(d: ImageDraw.ImageDraw, rng: Rng, avoid: List[Tuple[float, float, float, float]],
            palette=CONFETTI, count: int = 26) -> None:
    """Sprinkle doodles over the whole card, skipping the rectangles the text
    and the illustration have claimed. Rejection sampling rather than a grid,
    because a grid is visible even when you cannot name it."""
    placed: List[Tuple[float, float, float]] = []
    tries = 0
    while len(placed) < count and tries < count * 40:
        tries += 1
        x = rng.between(24, W - 24)
        y = rng.between(24, H - 24)
        r = rng.between(5, 15)
        if any(ax - r < x < bx + r and ay - r < y < by + r for ax, ay, bx, by in avoid):
            continue
        # Doodles do not touch each other; overlapping ones read as a smudge.
        if any((x - px) ** 2 + (y - py) ** 2 < (r + pr + 20) ** 2 for px, py, pr in placed):
            continue
        placed.append((x, y, r))
        rng.pick(DOODLE_WEIGHTS)(d, x, y, r, rng.pick(palette))


# ── Illustrations ─────────────────────────────────────────────────────────
# Flat vector, two tones plus ink, drawn inside a circle that bleeds off the
# right edge. One shape, big; an OG card has room for exactly one idea.

def _circle_mask(r: int) -> Image.Image:
    m = Image.new('L', (r * 2 * SS, r * 2 * SS), 0)
    ImageDraw.Draw(m).ellipse((0, 0, r * 2 * SS - 1, r * 2 * SS - 1), fill=255)
    return m


def _hero_plate(accent, tint) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    size = HERO_R * 2 * SS
    plate = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.ellipse((0, 0, size - 1, size - 1), fill=mix(tint, PAPER, 0.25) + (255,))
    return plate, pd


def hero_books(accent, tint, rng: Rng) -> Image.Image:
    """A leaning stack. Library, subject pages, anything that is a shelf."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    shades = [accent, mix(accent, PAPER, 0.35), mix(accent, INK, 0.25),
              mix(accent, PAPER, 0.6)]
    y = c + 190 * SS
    for i, shade in enumerate(shades):
        h = int((34 + (i % 3) * 8) * SS)
        w = int((300 - i * 26) * SS)
        x = c - w // 2 + int(rng.between(-16, 16) * SS)
        pd.rounded_rectangle((x, y - h, x + w, y), radius=int(8 * SS),
                             fill=shade + (255,))
        # The page block, a lighter sliver along the top edge.
        pd.rounded_rectangle((x + int(14 * SS), y - h + int(6 * SS),
                              x + w - int(14 * SS), y - h + int(13 * SS)),
                             radius=int(3 * SS), fill=PAPER + (170,))
        y -= h + int(9 * SS)
    # An open book resting on top. The pages dip toward the spine, which is the
    # whole read: a book whose middle is higher than its edges is a saucer.
    top = y - int(54 * SS)
    cover = mix(accent, INK, 0.3)
    pd.polygon([(c - int(172 * SS), top + int(22 * SS)), (c, top + int(54 * SS)),
                (c + int(172 * SS), top + int(22 * SS)), (c + int(172 * SS), top + int(104 * SS)),
                (c, top + int(132 * SS)), (c - int(172 * SS), top + int(104 * SS))],
               fill=cover + (255,))
    pd.polygon([(c - int(158 * SS), top), (c - int(6 * SS), top + int(40 * SS)),
                (c - int(6 * SS), top + int(112 * SS)), (c - int(158 * SS), top + int(78 * SS))],
               fill=PAPER + (255,))
    pd.polygon([(c + int(158 * SS), top), (c + int(6 * SS), top + int(40 * SS)),
                (c + int(6 * SS), top + int(112 * SS)), (c + int(158 * SS), top + int(78 * SS))],
               fill=mix(PAPER, tint, 0.45) + (255,))
    for i in range(3):
        ly = top + int((16 + i * 18) * SS)
        pd.line([(c - int(132 * SS), ly), (c - int(28 * SS), ly + int(22 * SS))],
                fill=mix(accent, PAPER, 0.62) + (255,), width=int(5 * SS))
    return plate


def hero_paper(accent, tint, rng: Rng) -> Image.Image:
    """A question paper. Past papers, model questions, notes, any resource."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    for i, (dx, dy, rot_tint) in enumerate(((-72, 50, 0.30), (-36, 25, 0.15), (0, 0, 0.0))):
        w, h = int(268 * SS), int(348 * SS)
        x = c + int(dx * SS) - w // 2
        y = c + int(dy * SS) - h // 2
        # The back sheets are tinted toward the accent, not toward paper: the
        # plate behind them is already a pale tint, and paper-on-paper is a
        # sheet you cannot see.
        fill = mix(tint, accent, rot_tint) if i < 2 else PAPER
        pd.rounded_rectangle((x, y, x + w, y + h), radius=int(14 * SS), fill=fill + (255,))
    # Ruled lines on the front sheet, with one heading bar in the accent.
    x = c - int(134 * SS)
    y = c - int(174 * SS)
    pd.rounded_rectangle((x + int(34 * SS), y + int(44 * SS),
                          x + int(150 * SS), y + int(62 * SS)),
                         radius=int(9 * SS), fill=accent + (255,))
    for i in range(7):
        ly = y + int((96 + i * 30) * SS)
        right = x + int((234 - (58 if i in (2, 5) else 0)) * SS)
        pd.rounded_rectangle((x + int(34 * SS), ly, right, ly + int(11 * SS)),
                             radius=int(5 * SS), fill=mix(accent, PAPER, 0.62) + (255,))
    return plate


def hero_bubbles(accent, tint, rng: Rng) -> Image.Image:
    """Two speech bubbles, one answering the other. The forum."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS

    def bubble(cx, cy, w, h, fill, tail_left):
        pd.rounded_rectangle((cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2),
                             radius=int(34 * SS), fill=fill + (255,))
        ty = cy + h // 2
        tx = cx - w // 2 + int(44 * SS) if tail_left else cx + w // 2 - int(44 * SS)
        d = int(34 * SS) if tail_left else int(-34 * SS)
        pd.polygon([(tx, ty - int(4 * SS)), (tx + d, ty - int(4 * SS)),
                    (tx + d // 3, ty + int(38 * SS))], fill=fill + (255,))

    bubble(c - int(28 * SS), c - int(84 * SS), int(300 * SS), int(150 * SS), PAPER, True)
    for i in range(3):
        ly = c - int((132 - i * 30) * SS)
        pd.rounded_rectangle((c - int(154 * SS), ly,
                              c + int((94 - i * 40) * SS), ly + int(12 * SS)),
                             radius=int(6 * SS), fill=mix(accent, PAPER, 0.6) + (255,))
    bubble(c + int(40 * SS), c + int(104 * SS), int(276 * SS), int(132 * SS), accent, False)
    for i in range(2):
        ly = c + int((66 + i * 32) * SS)
        pd.rounded_rectangle((c - int(78 * SS), ly,
                              c + int((120 - i * 54) * SS), ly + int(12 * SS)),
                             radius=int(6 * SS), fill=mix(accent, PAPER, 0.55) + (255,))
    return plate


def hero_flask(accent, tint, rng: Rng) -> Image.Image:
    """A flask half full, with what is rising out of it. The AI study tools."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    # Sized to sit inside the plate with room to spare: the circle crops
    # anything that does not, and a cropped flask is a balloon.
    neck_w, neck_top = int(46 * SS), c - int(138 * SS)
    body_r = int(102 * SS)
    body_cy = c + int(62 * SS)
    pd.ellipse((c - body_r, body_cy - body_r, c + body_r, body_cy + body_r),
               fill=PAPER + (255,))
    pd.rounded_rectangle((c - neck_w // 2, neck_top, c + neck_w // 2, body_cy),
                         radius=int(10 * SS), fill=PAPER + (255,))
    pd.rounded_rectangle((c - int(38 * SS), neck_top - int(14 * SS),
                          c + int(38 * SS), neck_top + int(6 * SS)),
                         radius=int(10 * SS), fill=mix(accent, PAPER, 0.45) + (255,))
    # The liquid: a chord of the body circle, flat on top.
    liquid = Image.new('RGBA', plate.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(liquid)
    ld.ellipse((c - body_r, body_cy - body_r, c + body_r, body_cy + body_r),
               fill=accent + (255,))
    ld.rectangle((0, 0, plate.size[0], body_cy - int(28 * SS)), fill=(0, 0, 0, 0))
    plate.alpha_composite(liquid)
    # What is coming out of it, kept well inside the plate.
    for i, (dx, dy, r) in enumerate(((-96, -168, 20), (74, -198, 14), (-18, -212, 10))):
        _sparkle(pd, (c + dx * SS) / SS, (c + dy * SS) / SS, r,
                 mix(accent, INK, 0.1) if i == 0 else accent)
    return plate


def hero_graph(accent, tint, rng: Rng) -> Image.Image:
    """Nodes and edges. Canvas, mindmaps, anything that branches."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    nodes = [(0, -140, 46), (-150, 6, 34), (140, -6, 34),
             (-92, 158, 28), (96, 156, 28), (2, 62, 24)]
    for dx, dy, _ in nodes[1:]:
        pd.line([(c, c - int(140 * SS)), (c + int(dx * SS), c + int(dy * SS))],
                fill=mix(accent, PAPER, 0.55) + (255,), width=int(5 * SS))
    pd.line([(c - int(150 * SS), c + int(6 * SS)), (c - int(92 * SS), c + int(158 * SS))],
            fill=mix(accent, PAPER, 0.62) + (255,), width=int(4 * SS))
    pd.line([(c + int(140 * SS), c - int(6 * SS)), (c + int(96 * SS), c + int(156 * SS))],
            fill=mix(accent, PAPER, 0.62) + (255,), width=int(4 * SS))
    for i, (dx, dy, r) in enumerate(nodes):
        x, y, rr = c + int(dx * SS), c + int(dy * SS), int(r * SS)
        fill = accent if i == 0 else (PAPER if i % 2 else mix(accent, PAPER, 0.35))
        pd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=fill + (255,))
        if fill is PAPER:
            pd.ellipse((x - rr, y - rr, x + rr, y + rr),
                       outline=mix(accent, PAPER, 0.4) + (255,), width=int(4 * SS))
    return plate


def hero_question(accent, tint, rng: Rng) -> Image.Image:
    """A question mark built from a bubble. The FAQ."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    pd.rounded_rectangle((c - int(168 * SS), c - int(170 * SS),
                          c + int(168 * SS), c + int(128 * SS)),
                         radius=int(48 * SS), fill=PAPER + (255,))
    pd.polygon([(c - int(96 * SS), c + int(120 * SS)),
                (c - int(22 * SS), c + int(120 * SS)),
                (c - int(76 * SS), c + int(196 * SS))], fill=PAPER + (255,))
    f = font('bold', int(232 * SS))
    mark = '?'
    box = pd.textbbox((0, 0), mark, font=f)
    pd.text((c - (box[2] - box[0]) / 2 - box[0],
             c - int(20 * SS) - (box[3] - box[1]) / 2 - box[1]),
            mark, font=f, fill=accent + (255,))
    return plate


def hero_avatar(accent, tint, rng: Rng, avatar: Optional[Image.Image] = None) -> Image.Image:
    """A person, or their photo, filling the plate the way the reference's
    illustration does."""
    plate, pd = _hero_plate(accent, tint)
    size = HERO_R * 2 * SS
    if avatar is not None:
        from PIL import ImageOps
        fitted = ImageOps.fit(avatar.convert('RGBA'), (size, size),
                              method=Image.LANCZOS, centering=(0.5, 0.42))
        plate.paste(fitted, (0, 0), _circle_mask(HERO_R))
        return plate
    c = HERO_R * SS
    # A warm tone with a trace of the accent in it. Mixing the accent toward
    # paper on its own gives a grey-blue face, which is nobody.
    skin = mix((233, 197, 167), accent, 0.10)
    # Shoulders, then head: two shapes, no features -- a face with eyes drawn on
    # a card that might be about a school is a different product.
    pd.ellipse((c - int(212 * SS), c + int(96 * SS), c + int(212 * SS), c + int(420 * SS)),
               fill=mix(accent, INK, 0.12) + (255,))
    pd.ellipse((c - int(118 * SS), c - int(160 * SS), c + int(118 * SS), c + int(118 * SS)),
               fill=skin + (255,))
    pd.ellipse((c - int(132 * SS), c - int(186 * SS), c + int(132 * SS), c + int(30 * SS)),
               fill=mix(accent, INK, 0.45) + (255,))
    pd.ellipse((c - int(102 * SS), c - int(128 * SS), c + int(102 * SS), c + int(96 * SS)),
               fill=skin + (255,))
    return plate


def hero_mark(accent, tint, rng: Rng) -> Image.Image:
    """Concentric arcs around the brand mark. The home page and anything
    without a subject of its own."""
    plate, pd = _hero_plate(accent, tint)
    c = HERO_R * SS
    for i, r in enumerate((236, 190, 144)):
        rr = int(r * SS)
        pd.arc((c - rr, c - rr, c + rr, c + rr), start=200 + i * 26, end=430 + i * 26,
               fill=mix(accent, PAPER, 0.35 + i * 0.12) + (255,), width=int(7 * SS))
    rr = int(104 * SS)
    pd.ellipse((c - rr, c - rr, c + rr, c + rr), fill=accent + (255,))
    f = font('bold', int(150 * SS))
    box = pd.textbbox((0, 0), 'N', font=f)
    pd.text((c - (box[2] - box[0]) / 2 - box[0], c - (box[3] - box[1]) / 2 - box[1]),
            'N', font=f, fill=PAPER + (255,))
    return plate


HEROES = {
    'books': hero_books,
    'paper': hero_paper,
    'bubbles': hero_bubbles,
    'flask': hero_flask,
    'graph': hero_graph,
    'question': hero_question,
    'avatar': hero_avatar,
    'mark': hero_mark,
}


# ── Text ──────────────────────────────────────────────────────────────────

def _wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont,
          width: int, max_lines: int) -> Tuple[List[str], bool]:
    """Greedy wrap. Returns the lines and whether anything had to be dropped --
    the caller needs that second value, because a size that only "fits" by
    throwing away half the title is not a fit."""
    words = (text or '').split()
    lines: List[str] = []
    current = ''
    used = 0
    for word in words:
        trial = (current + ' ' + word).strip()
        if d.textlength(trial, font=f) <= width or not current:
            current = trial
            used += 1
        else:
            lines.append(current)
            if len(lines) == max_lines:
                current = ''
                break
            current = word
            used += 1
    if current:
        lines.append(current)
    truncated = used < len(words)
    if truncated and lines:
        last = lines[-1]
        while last and d.textlength(last + '\u2026', font=f) > width:
            last = last[:-1]
        lines[-1] = last.rstrip() + '\u2026'
    return lines, truncated


def _fit_title(d: ImageDraw.ImageDraw, text: str, width: int
               ) -> Tuple[ImageFont.FreeTypeFont, List[str]]:
    """Largest size at which the whole title still fits. A four-word title gets
    to be huge; a sentence gets to be small enough to be read. Only the last
    rung may ellipsize, and by then the title was a paragraph."""
    ladder = ((92, 2), (80, 2), (72, 3), (64, 3), (56, 3), (48, 4), (42, 4))
    for size, max_lines in ladder:
        f = font('bold', size * SS)
        lines, truncated = _wrap(d, text, f, width * SS, max_lines)
        if not truncated:
            return f, lines
    f = font('bold', ladder[-1][0] * SS)
    return f, _wrap(d, text, f, width * SS, ladder[-1][1])[0]


# ── The card ──────────────────────────────────────────────────────────────

def render(kind: str, title: str, *, meta: Sequence[str] = (), kicker: str = '',
           subject: str = '', seed: str = '', hero: str = 'mark',
           avatar: Optional[Image.Image] = None) -> Image.Image:
    """One card. `kind` is only used for the seed; `hero` picks the drawing."""
    accent, tint = accent_for(subject)
    rng = Rng(seed_of(kind, seed or title, subject))

    canvas = Image.new('RGBA', (W * SS, H * SS), PAPER + (255,))
    d = ImageDraw.Draw(canvas)

    # Frame: one hairline at the very edge and one faint rule inset from it.
    # Two weights of almost nothing is what makes the ground read as paper
    # rather than as a blank PNG.
    d.rectangle((0, 0, W * SS - 1, H * SS - 1), outline=FRAME + (255,), width=SS)
    d.rectangle((10 * SS, 10 * SS, (W - 10) * SS - 1, (H - 10) * SS - 1),
                outline=RULE + (255,), width=SS)

    plate = HEROES.get(hero, hero_mark)
    illo = plate(accent, tint, rng, avatar) if hero == 'avatar' else plate(accent, tint, rng)
    # Clip to the plate. The drawings deliberately overshoot -- shoulders, a
    # bubble tail, the top of a stack -- and the circle is what turns an
    # overshoot into a shape cropped by its own frame instead of a spill.
    illo.putalpha(ImageChops.multiply(illo.getchannel('A'), _circle_mask(HERO_R)))
    canvas.alpha_composite(illo, ((HERO_CX - HERO_R) * SS, (HERO_CY - HERO_R) * SS))

    # Text block, vertically centred on the card rather than on the hero: the
    # hero bleeds and the text does not, so aligning them looks wrong.
    f_title, lines = _fit_title(d, title, TEXT_MAX)
    title_size = f_title.size / SS
    leading = title_size * 1.14
    kicker_h = 34 if kicker else 0
    meta_h = 40 if meta else 0
    block_h = kicker_h + leading * len(lines) + meta_h
    y = (H - block_h) / 2

    if kicker:
        fk = font('bold', 21 * SS)
        text = kicker.upper()
        # Tracked by hand: PIL has no letter-spacing, and an uppercase kicker
        # without it is a shout instead of a label.
        x = MARGIN * SS
        for ch in text:
            d.text((x, y * SS), ch, font=fk, fill=accent + (255,))
            x += d.textlength(ch, font=fk) + 3.1 * SS
        y += kicker_h

    for line in lines:
        d.text((MARGIN * SS, y * SS), line, font=f_title, fill=INK + (255,))
        y += leading

    if meta:
        fm = font('medium', 25 * SS)
        x = MARGIN * SS
        y += 14
        for i, part in enumerate(meta):
            if i:
                r = 4 * SS
                cx, cy = x + 11 * SS, y * SS + 18 * SS
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=accent + (255,))
                x += 30 * SS
            d.text((x, y * SS), part, font=fm, fill=MUTED + (255,))
            x += d.textlength(part, font=fm)

    # Doodles last, so they can be told to stay off everything already drawn.
    avoid = [(24, (H - block_h) / 2 - 20, MARGIN + TEXT_MAX + 10,
              (H - block_h) / 2 + block_h + 20),
             (HERO_CX - HERO_R - 34, HERO_CY - HERO_R - 34, W, H)]
    scatter(d, rng, avoid, palette=CONFETTI + (mix(accent, PAPER, 0.35),))

    return canvas.convert('RGB').resize((W, H), Image.LANCZOS)


def to_png(img: Image.Image) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    # Palette-quantised: these are flat-colour drawings, so 128 colours is
    # visually lossless and about a fifth of the bytes. Under Twitter's 5MB
    # limit either way, but an OG image is fetched by every scraper that sees
    # the link.
    img.convert('RGB').quantize(colors=128, method=Image.MEDIANCUT,
                                dither=Image.NONE).save(buf, format='PNG', optimize=True)
    return buf.getvalue()
