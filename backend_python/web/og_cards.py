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
import os
from typing import List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

from . import og_logo, og_m3x as m3x
from .og_art import (H, SS, W, Rng, Stage, face_palette, ground, lift, mix,
                     radial_glow, saturate)
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

TITLE_MAX = 148          # one short word may be this big
TITLE_MIN = 40
TITLE_BUDGET = 452       # vertical room the title may use, in card pixels
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


# ── Pieces ────────────────────────────────────────────────────────────────

def _chip(d: ImageDraw.ImageDraw, x, y, text, f, fill, ink, pad=(18, 9), track=0.0):
    """A tonal pill. Returns its right edge in card pixels."""
    if track:
        w = sum(d.textlength(ch, font=f) + track for ch in text) / float(SS)
    else:
        w = d.textlength(text, font=f) / float(SS)
    h = f.size / float(SS)
    box = (x, y, x + w + pad[0] * 2, y + h * 1.32 + pad[1] * 2 - 4)
    d.rounded_rectangle([v * SS for v in box], radius=(box[3] - box[1]) / 2 * SS, fill=tuple(fill) + (255,))
    tx, ty = (x + pad[0]) * SS, (y + pad[1] - 1) * SS
    if track:
        _tracked(d, (tx, ty), text, f, tuple(ink) + (255,), track)
    else:
        d.text((tx, ty), text, font=f, fill=tuple(ink) + (255,))
    return box[2]


def render(kind: str, title: str, *, meta: Sequence[str] = (), kicker: str = '',
           subject: str = '', seed: str = '', hero: str = 'mark',
           avatar: Optional[Image.Image] = None, accent_hex: str = '') -> Image.Image:
    """One card, M3 Expressive light: a tonal surface, one big expressive shape
    on the right holding a solid accent shape and a white glyph, the words on
    the left. Flat colour only; `kind` and `seed` pick the shape variant."""
    accent = accent_for(subject or '', accent_hex)[0]
    c = m3x.roles(accent)
    variant = seed_of(kind, seed or title, subject) % 4

    canvas = Image.new('RGBA', (W * SS, H * SS), tuple(c['surface']) + (255,))
    d = ImageDraw.Draw(canvas, 'RGBA')

    # ── The shapes ──
    cx, cy = 925, 322
    big = [(cx, cy, 262, 9, .065, .3),
           (cx + 8, cy + 6, 258, 8, .08, .1),
           (cx - 4, cy - 2, 266, 10, .05, .6),
           (cx + 4, cy + 2, 260, 7, .09, .9)][variant]
    m3x.poly(d, m3x.cookie(*big), c['container'], SS)
    small_dx = (-196, 205, -190, 196)[variant]
    small_dy = (-206, 214, 208, -204)[variant]
    m3x.poly(d, m3x.squircle(cx + small_dx, cy + small_dy, 52, 4.0, .4), c['container_hi'], SS)
    m3x.poly(d, m3x.cookie(cx - small_dx * .92, cy + small_dy * .1, 26, 7, .14, .5), c['container_hi'], SS)
    if hero == 'avatar':
        m3x.portrait(canvas, avatar, cx, cy, 168, c, SS, font)
    else:
        if hero not in HEROES:
            hero = 'mark'
        m3x.poly(d, m3x.squircle(cx, cy, 172, 4.4, [0.0, .12, -.1, .06][variant]), c['accent'], SS)
        m3x.glyph(hero, d, canvas, cx, cy, 82, c, SS, font)

    # ── Lockup, top left ──
    art = og_logo.mark(40 * SS)
    canvas.alpha_composite(art, (MARGIN * SS, 58 * SS))
    d = ImageDraw.Draw(canvas, 'RGBA')
    d.text(((MARGIN + art.size[0] / SS + 14) * SS, 62 * SS), 'NEBians', font=font('bold', 26 * SS),
           fill=tuple(c['ink']) + (255,))

    # ── The words ──
    kicker_h = 62 if kicker else 0
    meta_h = 74 if meta else 0
    budget = H - 132 - 112 - kicker_h - meta_h
    cap = TITLE_MAX
    while True:
        f_title, lines = _fit_title(d, title, TEXT_W, max_size=cap)
        size = f_title.size / float(SS)
        leading = size * 1.10
        if leading * len(lines) <= budget or cap <= TITLE_MIN:
            break
        cap = int(min(cap, size)) - 4
    title_h = leading * len(lines)
    block_h = kicker_h + title_h + meta_h
    top = 132 + (H - 132 - 112 - block_h) / 2.0

    y = top
    if kicker:
        _chip(d, MARGIN, y, kicker.upper(), font('bold', 18 * SS), c['container_hi'], c['on_container'],
              pad=(18, 9), track=2.2 * SS)
        y += kicker_h
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f_title)
        d.text((MARGIN * SS, y * SS - bbox[1]), line, font=f_title, fill=tuple(c['ink']) + (255,))
        y += leading
    if meta:
        fm = font('medium', 20 * SS)
        mx, my = MARGIN, y + 22
        for part in meta:
            part = str(part)
            if not part:
                continue
            w = d.textlength(part, font=fm) / float(SS) + 36
            if mx + w > MARGIN + TEXT_W:
                break
            mx = _chip(d, mx, my, part, fm, c['chip'], c['on_container'], pad=(18, 8)) + 10

    d.text((MARGIN * SS, (H - 62) * SS), 'nebians.consica.com.np', font=font('medium', 19 * SS),
           fill=tuple(c['muted']) + (255,))

    return canvas.convert('RGB').resize((W, H), Image.LANCZOS)


def to_png(img: Image.Image) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    # 256 colours, error diffusion. These are gradient grounds, so the dither
    # matters: quantising them flat produces visible rings in the corners where
    # the vignette is softest.
    img.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT,
                                dither=Image.NONE).save(
        buf, format='PNG', optimize=True)
    return buf.getvalue()
