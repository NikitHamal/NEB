"""One hero sculpture per kind of page, all in the logo's projection.

Each is a small function taking the accent colour, a seeded rng and a Stage.
They are deliberately built from the same three things -- a slab, a sheet and
a rim -- so the library's books and the forum's speech plates are obviously
relatives. One idea per card: an OG preview is read at 300px in a chat window.

Coordinates are symmetric about the plan centre: a solid of plan size 3 spans
-1.5..1.5 on both axes, so it sits centred on the stage's origin no matter how
tall it is. The mark itself is not redrawn here; it is the real logo file,
composited by og_cards.
"""
from __future__ import annotations

import math

from PIL import Image, ImageDraw

from .og_art import (RIM, Stage, face_palette, mix, soft_shadow)


# ── Helpers ───────────────────────────────────────────────────────────────

def _shadow(canvas, stage, rx: float, alpha: int = 130, dz: float = 0.0):
    """A soft ellipse on the ground plane, in canvas pixels."""
    cx, cy = stage.project(0, 0, 0)
    soft_shadow(canvas, cx, cy + dz * stage.u, rx * stage.u, rx * stage.u * 0.42, alpha)


def _line3d(d, stage, x0, y0, x1, y1, z, colour, width):
    a = stage.project(x0, y0, z)
    b = stage.project(x1, y1, z)
    d.line([a, b], fill=colour, width=max(1, int(width)))


def _rubber(canvas, base: Image.Image, mask_box, radius: int) -> None:
    """Round the corners of an already-composited region. Used for plates whose
    corners read too sharp at card scale."""


# ── The sculptures ────────────────────────────────────────────────────────

def hero_books(accent, rng, stage: Stage) -> None:
    """Library and subject pages: a stack of books with one open on top."""
    pal = face_palette(accent)
    page = (247, 244, 236)
    _shadow(stage.canvas, stage, 2.50, alpha=150)

    # Each cover is the subject hue at a different depth of shade -- a shelf
    # all in one tone reads as a single block wherever a stack is smaller than
    # it looks. The tilt is per book so the edges are not one flat wall.
    other = mix(pal[2], (255, 255, 255), 0.22)
    covers = (pal[2], other, mix(pal[0], (0, 0, 0), 0.18))
    z = 0.0
    for i, (w, d, h, ox, oy) in enumerate(((2.94, 2.06, 0.30, 0.02, 0.00),
                                           (2.72, 1.94, 0.24, -0.12, 0.06),
                                           (2.56, 1.86, 0.22, 0.07, -0.03))):
        cover = covers[i]
        # Pages first, a shade larger and a hair lower: the pale fore-edge then
        # rings the coloured cover, which is what says "book" from above.
        stage.box(ox - w / 2 - 0.03, oy - d / 2 - 0.03, z, w + 0.06, d + 0.06, h * 0.5,
                  (page, mix(page, (0, 0, 0), 0.08), mix(page, (0, 0, 0), 0.16)),
                  rim=mix(page, (0, 0, 0), 0.24))
        stage.box(ox - w / 2, oy - d / 2, z + h * 0.5, w, d, h * 0.5,
                  (mix(cover, (255, 255, 255), 0.10), cover,
                   mix(cover, (0, 0, 0), 0.24)),
                  rim=RIM)
        z += h + 0.02

    # The open book: two boards hinged along x = 0, tilted down from the spine.
    top = z + 0.015
    for side in (-1, 1):
        x0 = 0.0 if side > 0 else -1.44
        cover = mix(pal[2], (0, 0, 0), 0.10)
        tones = (mix(cover, (255, 255, 255), 0.18), cover,
                 mix(cover, (0, 0, 0), 0.26))
        stage.box(x0, -1.04, top, 1.44, 2.08, 0.09, tones,
                  rim=mix(RIM, pal[0], 0.10))
        stage.box(x0 + 0.06, -0.96, top + 0.09, 1.32, 1.92, 0.05,
                  (page, mix(page, (0, 0, 0), 0.05), mix(page, (0, 0, 0), 0.12)),
                  rim=mix(page, (0, 0, 0), 0.20))
        d = ImageDraw.Draw(stage.canvas, 'RGBA')
        for i in range(3):
            ly = -0.76 + i * 0.62
            _line3d(d, stage, x0 + 0.18, ly, x0 + 1.20, ly, top + 0.141,
                    mix(accent, (255, 255, 255), 0.48) + (150,), stage.u * 0.04)

    # The spine seam.
    d = ImageDraw.Draw(stage.canvas, 'RGBA')
    _line3d(d, stage, 0, -1.04, 0, 1.04, top + 0.142,
            mix(pal[2], (0, 0, 0), 0.50) + (220,), stage.u * 0.045)


def hero_paper(accent, rng, stage: Stage) -> None:
    """Past papers, notes, model questions, articles: a sheet in the air."""
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 2.20, alpha=120, dz=0.6)

    # Three sheets, fanned. The top one carries the writing; the two behind it
    # are tone only, so the fan reads as a ream rather than as a solid slab.
    for dz, ox, oy, tint in ((0.0, 0.30, 0.34, 0.0),
                             (0.24, 0.15, 0.16, 0.30),
                             (0.48, 0.00, 0.00, 0.62)):
        face = mix(pal[0], (255, 255, 255), 0.72 - tint * 0.05)
        stage.box(-1.00 + ox, -1.40 + oy, dz, 2.00, 2.80, 0.035,
                  (face,
                   mix(pal[1], (255, 255, 255), 0.10 - tint * 0.10),
                   mix(pal[2], (255, 255, 255), 0.06 - tint * 0.06)),
                  rim=mix(RIM, pal[0], 0.10 + tint * 0.30))

    # Rules on the top sheet. The top sheet is drawn at (-1.00, -1.40) with a
    # 2.00 x 2.80 footprint, and on this projection its long axis is y -- so a
    # line of writing steps down x and runs along y, inset from both edges.
    d = ImageDraw.Draw(stage.canvas, 'RGBA')
    top = 0.48 + 0.036
    x_in, y_in = -1.00, -1.40
    for i in range(7):
        lx = x_in + 0.34 + i * 0.26
        wide = (2.80 - 2 * 0.30) * (0.55 if i == 0 else (0.78 if i in (3, 5) else 1.0))
        colour = (mix(pal[0], (255, 255, 255), 0.02) if i == 0
                  else mix(pal[0], (255, 255, 255), 0.22))
        _line3d(d, stage, lx, y_in + 0.30, lx, y_in + 0.30 + wide, top,
                colour + (245 if i == 0 else 185,),
                stage.u * (0.105 if i == 0 else 0.042))


def hero_bubbles(accent, rng, stage: Stage) -> None:
    """The forum: two speech plates, one answering the other.

    The plates are separated in plan and in height, not stacked: two boxes at
    the same place read as one thick slab however many lines are drawn on
    them. A tail on the lower-left of the back plate is what makes it speech.
    """
    pal = face_palette(accent)

    # (z, ox, oy, w, d, h, tail)
    plates = ((0.72, -0.46, -0.62, 2.50, 1.42, 0.30, 'left'),
              (0.06, 0.56, 0.62, 1.82, 1.10, 0.26, None))
    for i, (z, ox, oy, w, d_, h, tail) in enumerate(plates):
        cx, cy = stage.project(ox, oy, 0)
        soft_shadow(stage.canvas, cx, cy + h * 0.7 * stage.u,
                    (w + d_) * 0.36 * stage.u, (w + d_) * 0.13 * stage.u,
                    80 if i == 0 else 55)

        if i == 0:
            tones = (mix(pal[0], (255, 255, 255), 0.14),
                     mix(pal[1], (255, 255, 255), 0.02),
                     pal[2])
        else:
            tones = (mix(pal[0], (255, 255, 255), 0.64),
                     mix(pal[1], (0, 0, 0), 0.22),
                     mix(pal[2], (0, 0, 0), 0.16))

        d = ImageDraw.Draw(stage.canvas, 'RGBA')
        if tail:
            # The wedge sits on the plate's own plane, overlapping its left
            # edge, and is drawn before the plate so the join disappears. A
            # tail that only touches the edge reads as a sliver.
            ty = oy + d_ / 2 - 0.30
            tx = ox - w / 2 + 0.06
            p0 = stage.project(tx, ty - 0.46, z + h)
            p1 = stage.project(tx, ty, z + h)
            p2 = stage.project(tx - 0.72, ty + 0.52, z + h)
            d.polygon([p0, p1, p2], fill=tones[0] + (255,))
            d.line([p0, p2], fill=RIM + (170,), width=max(1, int(stage.u * 0.016)))
            d.line([p1, p2], fill=RIM + (170,), width=max(1, int(stage.u * 0.016)))

        stage.box(ox - w / 2, oy - d_ / 2, z, w, d_, h, tones, rim=RIM)

        for j in range(3 if i == 0 else 2):
            ly = oy - d_ / 2 + 0.26 + j * 0.34
            lw = w - 0.44 - j * 0.28
            _line3d(d, stage, ox - w / 2 + 0.22, ly,
                    ox - w / 2 + 0.22 + lw, ly, z + h + 0.003,
                    (mix(pal[0], (255, 255, 255), 0.34) if i == 0
                     else mix(pal[0], (255, 255, 255), 0.08)) + (220,),
                    stage.u * 0.065)


def hero_flask(accent, rng, stage: Stage) -> None:
    """Study Lab, tools: a flask on a plinth, something rising out of it."""
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 2.30, alpha=150)
    stage.box(-1.42, -1.42, 0.0, 2.84, 2.84, 0.26,
              (mix(pal[0], (255, 255, 255), 0.10), pal[1], pal[2]), rim=RIM)

    canvas = stage.canvas
    d = ImageDraw.Draw(canvas, 'RGBA')
    cx, cy = stage.project(0, 0, 0.26)
    u = stage.u
    body_r = u * 0.86
    stem_w = u * 0.26
    stem_h = u * 1.05
    glass = mix(pal[0], (255, 255, 255), 0.70)

    # Neck and collar.
    d.rounded_rectangle((cx - stem_w, cy - stem_h - body_r * 0.86, cx + stem_w, cy),
                        radius=int(u * 0.10), fill=glass + (255,))
    d.rounded_rectangle((cx - stem_w * 1.45, cy - stem_h - body_r * 0.95,
                         cx + stem_w * 1.45, cy - stem_h - body_r * 0.72),
                        radius=int(u * 0.07), fill=mix(pal[0], (255, 255, 255), 0.35) + (255,))

    # Body.
    box = (cx - body_r, cy - body_r * 0.80, cx + body_r, cy + body_r * 0.96)
    d.ellipse(box, fill=glass + (255,))

    # Liquid: the lower chord of the body, clipped exactly to the glass.
    liquid = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(liquid).ellipse((box[0] + u * 0.02, box[1] + u * 0.02,
                                    box[2] - u * 0.02, box[3] - u * 0.02),
                                   fill=mix(pal[0], (255, 255, 255), 0.0) + (255,))
    keep = Image.new('L', canvas.size, 255)
    ImageDraw.Draw(keep).rectangle((0, 0, canvas.size[0], cy - body_r * 0.10), fill=0)
    liquid.putalpha(Image.composite(liquid.getchannel('A'),
                                    Image.new('L', canvas.size, 0), keep))
    canvas.alpha_composite(liquid)

    # Meniscus, then the glass rim over everything so the liquid stays inside.
    d.ellipse((cx - body_r * 0.94, cy - body_r * 0.22, cx + body_r * 0.94, cy + body_r * 0.10),
              fill=mix(pal[0], (255, 255, 255), 0.62) + (200,))
    d.ellipse(box, outline=RIM + (225,), width=max(1, int(u * 0.055)))
    d.rounded_rectangle((cx - stem_w, cy - stem_h - body_r * 0.86, cx + stem_w, cy),
                        radius=int(u * 0.10), outline=RIM + (200,),
                        width=max(1, int(u * 0.045)))

    # Rising motes.
    for i in range(8):
        mx = cx + rng.between(-body_r * 0.75, body_r * 0.75)
        my = cy - stem_h - body_r * rng.between(0.5, 2.0)
        r = rng.between(2.0, 5.5) * u * 0.05
        d.ellipse((mx - r, my - r, mx + r, my + r),
                  fill=mix(pal[0], (255, 255, 255), 0.45) + (int(rng.between(90, 210)),))


def hero_graph(accent, rng, stage: Stage) -> None:
    """Canvas and mindmaps: a hub note with satellites ringing it.

    A mindmap is flat cards at different heights with lines between them. The
    cards are turned slightly in the picture plane, which is what separates a
    wall of thoughts from a floor plan.
    """
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 1.80, alpha=70)

    hub = (-0.10, -0.10, 1.10, 1.34, 0.90, 0.0)
    # Six satellites on a ring, every 60 degrees, alternating heights.
    wings = []
    for i, ang in enumerate(range(0, 360, 60)):
        rad = 1.66 if i % 2 == 0 else 1.54
        x = math.cos(math.radians(ang)) * rad
        y = math.sin(math.radians(ang)) * rad
        z = 0.80 + (0.22 if i % 2 == 0 else -0.12)
        wings.append((x, y, z, 0.66, 0.44, (-9 if i % 2 else 8)))
    cards = [hub] + wings

    d = ImageDraw.Draw(stage.canvas, 'RGBA')
    hub_edge = (hub[0] + hub[3] / 2.0, hub[1] + hub[4] / 2.0, hub[2])
    for i, w in enumerate(wings, start=1):
        ax, ay = stage.project(hub_edge[0], hub_edge[1], hub_edge[2])
        bx, by = stage.project(w[0], w[1], w[2])
        d.line([(ax, ay), (bx, by)],
               fill=mix(accent, (255, 255, 255), 0.28) + (80,),
               width=max(1, int(stage.u * 0.022)))
        r = stage.u * 0.038
        for (px, py) in ((ax, ay), (bx, by)):
            d.ellipse((px - r, py - r, px + r, py + r),
                      fill=mix(accent, (255, 255, 255), 0.30) + (130,))

    # Satellites first, hub last: overlap reads as depth rather than clutter.
    for i in list(range(1, len(cards))) + [0]:
        x, y, z, w, d_, rot = cards[i]
        light = 0.34 if i == 0 else 0.02
        _card(stage, x - w / 2, y - d_ / 2, z, w, d_, rot,
              (mix(pal[0], (255, 255, 255), light + 0.10),
               mix(pal[1], (255, 255, 255), 0.06),
               mix(pal[2], (255, 255, 255), 0.02)),
              accent, hub=(i == 0))


def _card(stage: Stage, x, y, z, w, d_, rot, pal, accent, hub=False):
    """A flat card with rounded corners, rotated in the picture plane.

    Rounded and turned in screen space after projection: an isometric box has
    four square corners, and a note card does not. Drawing it flat and then
    shearing would be more honest to the projection and less legible at 300px,
    which is the size that matters.
    """
    from PIL import Image as _Image, ImageDraw as _D
    canvas = stage.canvas
    # Project the plan, then take the four corners into screen space.
    p00 = stage.project(x, y, z)
    p10 = stage.project(x + w, y, z)
    p11 = stage.project(x + w, y + d_, z)
    p01 = stage.project(x, y + d_, z)
    xs = [p[0] for p in (p00, p10, p11, p01)]
    ys = [p[1] for p in (p00, p10, p11, p01)]
    bw = max(2, int(max(xs) - min(xs)))
    bh = max(2, int(max(ys) - min(ys)))
    cx, cy = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0

    card = _Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    cd = _D.Draw(card)
    face = mix(pal[0], (255, 255, 255), 0.30 if hub else 0.06)
    cd.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=max(2, int(bw * 0.055)),
                         fill=face + (255,), outline=RIM + (225,),
                         width=max(1, int(stage.u * 0.018)))
    # Caption rules, in the accent.
    for j in range(2):
        ly = bh * (0.30 + j * 0.28)
        lw = bw * (0.62 if j == 0 else 0.40)
        cd.rounded_rectangle((bw * 0.13, ly, bw * 0.13 + lw, ly + max(2, bh * 0.07)),
                             radius=max(1, int(bh * 0.035)),
                             fill=mix(accent, (255, 255, 255), 0.10 if hub else 0.55) + (255,))
    if rot:
        card = card.rotate(rot, resample=_Image.BICUBIC, expand=True)
    canvas.alpha_composite(card, (int(cx - card.size[0] / 2), int(cy - card.size[1] / 2)))


def hero_question(accent, rng, stage: Stage) -> None:
    """FAQ: an extruded question mark standing on a plinth."""
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 2.30, alpha=150)
    stage.box(-1.36, -1.36, 0.0, 2.72, 2.72, 0.28,
              (mix(pal[0], (255, 255, 255), 0.12), pal[1], pal[2]), rim=RIM)

    canvas = stage.canvas
    d = ImageDraw.Draw(canvas, 'RGBA')
    cx, cy = stage.project(0, 0, 0.28)
    cy -= stage.u * 0.20
    f = _font('bold', int(stage.u * 2.65))
    bbox = d.textbbox((0, 0), '?', font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = cx - tw / 2 - bbox[0]
    y = cy - th / 2 - bbox[1]
    # Extrusion: the glyph stamped down-right in the dark face, then the lit
    # face on top. Cheaper than building the curve, and truer to the mark's
    # own bevelled edges.
    depth = int(stage.u * 0.34)
    for i in range(depth, 0, -1):
        d.text((x + i * 0.62, y + i * 0.62), '?', font=f,
               fill=mix(pal[2], (0, 0, 0), 0.35) + (255,))
    d.text((x, y), '?', font=f, fill=mix(pal[0], (255, 255, 255), 0.50) + (255,))
    d.text((x - 1, y - 1), '?', font=f, fill=mix(RIM, (255, 255, 255), 0.15) + (90,))


def hero_cards(accent, rng, stage: Stage) -> None:
    """Marketplace: three courses laid out like a hand of cards, each with a
    cover band in the subject colour."""
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 2.25, alpha=130)
    for i, (z, ox, oy, w, d_, tint) in enumerate((
            (0.00, 0.86, 0.92, 1.70, 1.20, 0.00),
            (0.34, 0.16, 0.14, 1.70, 1.20, 0.30),
            (0.68, -0.52, -0.62, 1.70, 1.20, 0.62))):
        face = mix(pal[0], (255, 255, 255), 0.52 + tint * 0.34)
        stage.box(ox - w / 2, oy - d_ / 2, z, w, d_, 0.085,
                  (face,
                   mix(pal[1], (0, 0, 0), 0.12 + tint * 0.18),
                   mix(pal[2], (0, 0, 0), 0.22 + tint * 0.22)),
                  rim=mix(RIM, pal[0], 0.12 + tint * 0.22))
        d = ImageDraw.Draw(stage.canvas, 'RGBA')
        # Cover band: the top third of the face, in the pure accent.
        band = 0.42
        x0, y0 = stage.project(ox - w / 2 + 0.12, oy - d_ / 2 + 0.12, z + 0.086)
        x1, y1 = stage.project(ox + w / 2 - 0.12, oy - d_ / 2 + 0.12, z + 0.086)
        x2, y2 = stage.project(ox + w / 2 - 0.12, oy - d_ / 2 + 0.12 + band, z + 0.086)
        x3, y3 = stage.project(ox - w / 2 + 0.12, oy - d_ / 2 + 0.12 + band, z + 0.086)
        d.polygon([(x0, y0), (x1, y1), (x2, y2), (x3, y3)],
                  fill=mix(pal[2], (0, 0, 0), 0.06 + tint * 0.10) + (255,))
        # Two caption rules under it.
        for j in range(2):
            ly = oy - d_ / 2 + 0.68 + j * 0.26
            _line3d(d, stage, ox - w / 2 + 0.24, ly,
                    ox - w / 2 + 0.24 + (w - 0.48) * (1.0 if j == 0 else 0.62), ly,
                    z + 0.086, mix(accent, (255, 255, 255), 0.55) + (170,),
                    stage.u * 0.045)


def hero_spark(accent, rng, stage: Stage) -> None:
    """Credits, search, Neby: a lit tower on a plinth."""
    pal = face_palette(accent)
    _shadow(stage.canvas, stage, 2.20, alpha=140)
    stage.box(-1.30, -1.30, 0.0, 2.60, 2.60, 0.24,
              (mix(pal[0], (255, 255, 255), 0.10), pal[1], pal[2]), rim=RIM)
    stage.box(-0.52, -0.52, 0.24, 1.04, 1.04, 1.30,
              (mix(pal[0], (255, 255, 255), 0.52), pal[1], pal[2]), rim=RIM)
    stage.box(-0.20, -0.20, 1.54, 0.40, 0.40, 0.62,
              (mix((255, 255, 255), pal[0], 0.22), (238, 243, 255), (206, 216, 242)),
              rim=RIM)


def hero_avatar(accent, rng, stage: Stage) -> None:
    """Profile: the plate is drawn by og_cards, which knows whether there is a
    photo. Nothing to draw here."""
    return None


def hero_mark(accent, rng, stage: Stage) -> None:
    """Home: the real mark, composited by og_cards."""
    return None


HEROES = {
    'books': hero_books,
    'paper': hero_paper,
    'bubbles': hero_bubbles,
    'flask': hero_flask,
    'graph': hero_graph,
    'question': hero_question,
    'cards': hero_cards,
    'spark': hero_spark,
    'avatar': hero_avatar,
    'mark': hero_mark,
}


_FONT_DIR = None


def set_font_dir(path: str) -> None:
    global _FONT_DIR
    _FONT_DIR = path


def _font(weight: str, size: int):
    import os
    from PIL import ImageFont
    names = {'bold': 'poppins_bold.ttf', 'medium': 'poppins_medium.ttf',
             'regular': 'poppins_regular.ttf'}
    path = os.path.join(_FONT_DIR or '', names.get(weight, names['regular']))
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()
