"""How an Open Graph card is laid out.

The drawing primitives and the hero sculptures live in og_art and og_heroes;
this is the page. Left column: the lockup, a kicker, the title, a meta line.
Right: one sculpture bleeding off the edge. Bottom-left: the address. That is
the whole grid, and it is the same grid on every card -- what changes is the
colour, the kicker, the words and the sculpture.

A card is read in a chat window at about 300 by 157 pixels, so the title is
large enough to read at half size and the rest is hierarchy rather than
information.
"""
from __future__ import annotations

import hashlib
import math
import os
from typing import List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

from . import og_logo
from .og_art import (H, SS, W, Rng, Stage, face_palette, grain, ground, lift,
                     mix, radial_glow, saturate)
from .og_heroes import HEROES, set_font_dir, _font

def _hex(value: str):
    value = (value or '').lstrip('#')
    if len(value) != 6:
        return None
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def accent_for(subject: str, override: str = ''):
    """(accent, tint) for a subject, from the app's own hue table.

    Returns the accent already lifted for an ink ground: a subject blue at
    #1D4ED8 is a fine chip on white and nearly invisible as a light source.
    """
    explicit = _hex(override)
    if explicit:
        return explicit, mix(explicit, (0, 0, 0), 0.55)
    try:
        from .templatetags import subject_tokens
        hues = subject_tokens.subject_hue(subject or '')
        ink = _hex(hues[0])
    except Exception:
        ink = None
    if not ink:
        ink = (0, 74, 198)
    return ink, mix(ink, (0, 0, 0), 0.55)


FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/web/fonts')
set_font_dir(FONT_DIR)

# ── Grid, in card units ───────────────────────────────────────────────────
MARGIN = 68
TEXT_W = 620          # where the title gives up and the sculpture begins
HERO_CX, HERO_CY = 968, 320
HERO_R = 268

# Per-sculpture placement: (dx, dy, units-per-card-pixel). A stack of books is
# wide and short so it wants pulling up; a mindmap is wide so it wants pulling
# left and shrinking, or its outer cards run under the frame.
HERO_TUNING = {
    'graph': (-26, 54, 78),
    'books': (2, 62, 92),
    'paper': (-6, 54, 88),
    'bubbles': (-10, 40, 82),
    'cards': (6, 48, 86),
    'question': (0, 34, 80),
    'flask': (10, 66, 88),
    'spark': (4, 52, 86),
}

TITLE_MAX = 86
TITLE_MIN = 40
KICKER_SIZE = 19
META_SIZE = 21
ADDRESS_SIZE = 17

PAPER = (247, 249, 255)
MUTED = (150, 160, 184)
DIM = (104, 114, 140)

_font_cache: dict = {}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    """Cached: a card draws its title a dozen times while fitting, and
    ImageFont.truetype re-reads the file every call."""
    key = (weight, int(size))
    hit = _font_cache.get(key)
    if hit is None:
        hit = _font(weight, max(4, int(size)))
        _font_cache[key] = hit
    return hit


def seed_of(*parts) -> int:
    raw = '|'.join(str(p) for p in parts)
    return int(hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8], 16)


# ── Text ──────────────────────────────────────────────────────────────────

def _wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont,
          width: int) -> List[str]:
    words = (text or '').split()
    lines: List[str] = []
    current = ''
    for word in words:
        trial = (current + ' ' + word).strip()
        if not current or d.textlength(trial, font=f) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _balanced(lines: List[str], d, f, width: int) -> List[str]:
    """Greedy wrapping leaves a single orphan word on the last line, which on a
    poster-sized title is the difference between tight and amateur. If the last
    line is under a third of the measure, steal a word from the line above."""
    if len(lines) < 2:
        return lines
    last = lines[-1]
    if d.textlength(last, font=f) > width * 0.34:
        return lines
    prev = lines[-2].split()
    if len(prev) < 2:
        return lines
    moved = prev[-1]
    trial_prev = ' '.join(prev[:-1])
    trial_last = (moved + ' ' + last).strip()
    if d.textlength(trial_last, font=f) <= width:
        return lines[:-2] + [trial_prev, trial_last]
    return lines


def _fit_title(d: ImageDraw.ImageDraw, text: str, width: int,
               max_lines: int = 3, max_size: int = TITLE_MAX
               ) -> Tuple[ImageFont.FreeTypeFont, List[str]]:
    """The largest size at which the title fits in `max_lines`. The ladder is
    walked downward rather than solved, because Poppins' advance widths are not
    linear in the point size -- hinting breaks the ratio at small sizes."""
    size = max_size
    while size >= TITLE_MIN:
        f = font('bold', size * SS)
        lines = _wrap(d, text, f, width * SS)
        if len(lines) <= max_lines and all(
                d.textlength(ln, font=f) <= width * SS for ln in lines):
            return f, _balanced(lines, d, f, width * SS)
        size -= 2
    f = font('bold', TITLE_MIN * SS)
    lines = _wrap(d, text, f, width * SS)
    if len(lines) > max_lines + 1:
        lines = lines[:max_lines + 1]
        lines[-1] = lines[-1].rstrip() + '…'
    return f, _balanced(lines, d, f, width * SS)


def _tracked(d: ImageDraw.ImageDraw, xy, text: str, f, fill, track: float):
    """Letter-spaced text. PIL has no tracking; an uppercase kicker without it
    is a shout instead of a label."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track
    return x


def _tracked_width(d: ImageDraw.ImageDraw, text: str, f, track: float) -> float:
    return sum(d.textlength(ch, font=f) for ch in text) + track * max(0, len(text) - 1)


def _pill(d: ImageDraw.ImageDraw, xy, text: str, f, fg, bg, border, pad_x, pad_y):
    w = d.textlength(text, font=f)
    h = f.size * 1.02
    x, y = xy
    box = (x, y, x + w + pad_x * 2, y + h + pad_y * 2)
    d.rounded_rectangle(box, radius=(h + pad_y * 2) / 2.0, fill=bg, outline=border,
                        width=max(1, int(1.2 * SS)))
    bbox = d.textbbox((0, 0), text, font=f)
    d.text((x + pad_x - bbox[0], y + pad_y + (h - (bbox[3] - bbox[1])) / 2.0 - bbox[1]),
           text, font=f, fill=fg)
    return box[2] - box[0]


# ── Pieces ────────────────────────────────────────────────────────────────

def _address(canvas: Image.Image, d: ImageDraw.ImageDraw, accent):
    """Bottom-left: the mark at lockup weight and the domain, so every card
    says whose card it is even when the title is cut in a preview."""
    y = H * SS - MARGIN * SS - 30 * SS
    art = og_logo.mark(30 * SS)
    canvas.alpha_composite(art, (MARGIN * SS, int(y)))
    f = font('bold', 19 * SS)
    x = MARGIN * SS + art.size[0] + 13 * SS
    d.text((x, y + 2 * SS), 'NEBians', font=f, fill=mix(PAPER, (255, 255, 255), 0.25))
    wm = d.textlength('NEBians', font=f)
    f2 = font('medium', 17 * SS)
    d.text((x + wm + 11 * SS, y + 4 * SS), 'nebians.consica.com.np', font=f2, fill=DIM)


def _bloom(canvas: Image.Image, cx: float, cy: float, r: float, colour, alpha: int):
    disc = radial_glow(int(r * 2), colour, alpha=alpha, falloff=2.4)
    canvas.alpha_composite(disc, (int(cx - r), int(cy - r)))


def _mark_stage(canvas: Image.Image, accent, rng: Rng):
    """The home page's hero: the real mark, lit, standing over a reflection."""
    height = int(HERO_R * 2.32)
    art = og_logo.mark(height * SS)
    x = int((HERO_CX + 10) * SS - art.size[0] / 2)
    y = int(HERO_CY * SS - art.size[1] / 2)

    _bloom(canvas, HERO_CX * SS, HERO_CY * SS, 330 * SS, saturate(accent, 1.2), 42)
    _bloom(canvas, HERO_CX * SS, HERO_CY * SS, 190 * SS,
           mix(lift(accent, 165), (255, 255, 255), 0.4), 60)

    canvas.alpha_composite(art, (x, y))

    # A hairline plinth under it, so the mark is standing rather than floating.
    d = ImageDraw.Draw(canvas, 'RGBA')
    py = y + art.size[1] * 0.985
    d.line([(HERO_CX * SS - 150 * SS, py), (HERO_CX * SS + 150 * SS, py)],
           fill=mix(accent, (255, 255, 255), 0.55) + (90,), width=int(1.4 * SS))


def _avatar_stage(canvas: Image.Image, accent, rng: Rng,
                  avatar: Optional[Image.Image]):
    """Profile: the photo on an isometric plate, or a monogram if there is
    none. The plate is the same solid as every other hero, so a profile card
    belongs to the set."""
    size = int(HERO_R * 1.62)
    cx, cy = HERO_CX, HERO_CY

    stage = Stage(canvas, cx + size * 0.06, cy + size * 0.10, size * 0.0075)
    stage.box(-36, -36, 0, 72, 72, 7, face_palette(accent), rim=(238, 245, 255))

    # Circular window for the portrait.
    plate = Image.new('RGBA', (size * SS, size * SS), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.ellipse((0, 0, size * SS - 1, size * SS - 1),
               fill=mix(accent, (0, 0, 0), 0.55) + (255,))

    if avatar is None:
        pd = ImageDraw.Draw(plate)
        f = font('bold', int(size * SS * 0.62))
        text = 'N'
        bbox = pd.textbbox((0, 0), text, font=f)
        pd.text(((size * SS - (bbox[2] - bbox[0])) / 2 - bbox[0],
                 (size * SS - (bbox[3] - bbox[1])) / 2 - bbox[1]),
                text, font=f, fill=mix(accent, (255, 255, 255), 0.75))
    else:
        from PIL import ImageOps
        fitted = ImageOps.fit(avatar.convert('RGBA'), (size * SS, size * SS),
                              method=Image.LANCZOS, centering=(0.5, 0.38))
        plate.paste(fitted, (0, 0), fitted)

    mask = Image.new('L', (size * SS, size * SS), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * SS - 1, size * SS - 1), fill=255)
    plate.putalpha(mask)

    # Two rings: a bright one at the photo edge and a wider accent halo.
    ring = Image.new('RGBA', (size * SS + 12 * SS, size * SS + 12 * SS), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((3 * SS, 3 * SS, (size + 9) * SS - 1, (size + 9) * SS - 1),
               outline=mix(accent, (255, 255, 255), 0.55) + (200,), width=int(2 * SS))

    _bloom(canvas, cx * SS, cy * SS, 300 * SS, saturate(accent, 1.2), 34)

    ox = int(cx * SS - size * SS / 2)
    oy = int(cy * SS - size * SS / 2)
    ring_layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ring_layer.alpha_composite(ring, (ox - 6 * SS, oy - 6 * SS))
    canvas.alpha_composite(ring_layer)
    canvas.alpha_composite(plate, (ox, oy))


# ── The card ──────────────────────────────────────────────────────────────

def render(kind: str, title: str, *, meta: Sequence[str] = (), kicker: str = '',
           subject: str = '', seed: str = '', hero: str = 'mark',
           avatar: Optional[Image.Image] = None, accent_hex: str = '') -> Image.Image:
    """One card. `kind` seeds the drawing; `hero` picks the sculpture."""
    accent = accent_for(subject or '', accent_hex)[0]
    rng = Rng(seed_of(kind, seed or title, subject))

    canvas = ground(W * SS, H * SS, accent, rng,
                    glow_at=((HERO_CX / float(W)) + 0.02, 0.50), glow_r=1.05)
    d = ImageDraw.Draw(canvas, 'RGBA')

    # Hairline frame, inset. One pixel of white at 10% is the whole difference
    # between "a picture" and "a card".
    d.rectangle((12 * SS, 12 * SS, W * SS - 12 * SS - 1, H * SS - 12 * SS - 1),
                outline=(255, 255, 255, 26), width=1)

    # ── The sculpture ──
    if hero == 'mark':
        _mark_stage(canvas, accent, rng)
    elif hero == 'avatar':
        _avatar_stage(canvas, accent, rng, avatar)
    else:
        # The stage works in canvas pixels, so the origin and the unit are both
        # at supersample scale. 92 units per card pixel: a 3-unit object then
        # spans about 480 card pixels, which leaves the sculpture room to sit
        # inside the frame rather than crowd the title.
        dx, dy, unit = HERO_TUNING.get(hero, (HERO_R * 0.02, HERO_R * 0.62, 92))
        stage = Stage(canvas, (HERO_CX + dx) * SS, (HERO_CY + dy) * SS, unit * SS)
        fn = HEROES.get(hero, HEROES['mark'])
        fn(accent, rng, stage)

    # ── The words ──
    d = ImageDraw.Draw(canvas, 'RGBA')
    f_title, lines = _fit_title(d, title, TEXT_W)
    size = f_title.size / float(SS)
    leading = size * 1.10
    kicker_h = (KICKER_SIZE * 1.9) if kicker else 0
    title_h = leading * len(lines)
    meta_h = (META_SIZE * 2.4) if meta else 0
    block_h = kicker_h + title_h + meta_h
    top = (H - block_h) / 2.0 - 6

    y = top
    if kicker:
        fk = font('bold', KICKER_SIZE * SS)
        # A short accent bar before the kicker: the cheapest way to put the
        # subject colour next to the words instead of only behind the picture.
        bar_w = 22
        bar_y = y + KICKER_SIZE * 0.42
        d.rounded_rectangle((MARGIN * SS, bar_y * SS, (MARGIN + bar_w) * SS,
                             (bar_y + 2.6) * SS), radius=1.3 * SS,
                            fill=mix(accent, (255, 255, 255), 0.30) + (255,))
        _tracked(d, ((MARGIN + bar_w + 13) * SS, y * SS), kicker.upper(), fk,
                 mix(accent, (255, 255, 255), 0.55) + (255,), 2.4 * SS)
        y += kicker_h

    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f_title)
        d.text((MARGIN * SS, y * SS - bbox[1]), line, font=f_title,
               fill=PAPER + (255,))
        y += leading

    if meta:
        fm = font('medium', META_SIZE * SS)
        mx = MARGIN
        my = y + 10
        for i, part in enumerate(meta):
            part = str(part)
            if not part:
                continue
            w = d.textlength(part, font=fm) / float(SS)
            if mx + w > MARGIN + TEXT_W:
                break
            if i:
                r = 2.2
                d.ellipse(((mx + 8 - r) * SS, (my + META_SIZE * 0.52 - r) * SS,
                           (mx + 8 + r) * SS, (my + META_SIZE * 0.52 + r) * SS),
                          fill=mix(accent, (255, 255, 255), 0.45) + (230,))
                mx += 22
            d.text((mx * SS, my * SS), part, font=fm, fill=MUTED + (255,))
            mx += w

    _address(canvas, d, accent)

    return canvas.convert('RGB').resize((W, H), Image.LANCZOS)


def to_png(img: Image.Image) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    # 256 colours, error diffusion. These are gradient grounds, so the dither
    # matters: quantising them flat produces visible rings in the corners where
    # the vignette is softest.
    img.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT,
                                dither=Image.FLOYDSTEINBERG).save(
        buf, format='PNG', optimize=True)
    return buf.getvalue()
