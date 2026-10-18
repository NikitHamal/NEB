"""NEBians launch film (Dashain release). Every frame is a pure function of t (seconds)."""
import math
import os
import sys

import numpy as np
import skia
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "neby"))
from characters import logo  # noqa: E402
from kit import (AMBER, BLUE, BLUE_BRIGHT, BLUE_WASH, CORAL, CX, H, INK, MINT, MUTED,  # noqa: E402
                 NAVY, VERT, PURPLE, TEAL, W, WHITE, clamp, ease_in_cubic, ease_in_out,
                 ease_out_back, ease_out_cubic, ease_out_expo, font, lerp, linear, mix,
                 paint, partial_path, polygon, rrect, seg, shadow_rrect, text, with_alpha)
from neby_player import Neby  # noqa: E402

DURATION = 20.0
FPS = 60
BPM = 120
TIKA = 0xFFE0313B
MARIGOLD = 0xFFFFA62B
SKY_TOP, SKY_BOT = 0xFFBFE2FF, 0xFFF4F9FF

NEBY = None


def neby():
    global NEBY
    if NEBY is None:
        NEBY = Neby(DURATION, FPS)
    return NEBY


# One list drives the sound (score.py) and documents the picture's beats.
CUES = [
    (0.00, "air"), (0.25, "rise"), (0.95, "shimmer"), (1.05, "word"), (1.80, "word"), (2.30, "chip"),
    (2.85, "whoosh"), (3.25, "word"),
    (3.70, "kite"), (4.15, "kite"), (4.60, "kite"), (5.05, "kite"),
    (3.80, "land"), (4.25, "land"), (4.70, "land"), (5.15, "land"),
    (5.60, "count"), (6.55, "chip"),
    (6.95, "whoosh"), (7.20, "page"), (7.55, "page"), (7.90, "word"), (8.30, "write"),
    (8.75, "tick"), (8.95, "tick"), (9.15, "tick"), (9.30, "word"),
    (9.60, "pop"), (9.72, "pop"), (9.84, "pop"), (9.96, "pop"), (10.08, "pop"), (10.20, "pop"),
    (10.45, "whoosh"), (10.80, "word"), (11.10, "bubble"), (11.70, "bubble"), (12.30, "bubble"),
    (12.55, "like"), (12.75, "like"), (12.95, "like"),
    (13.40, "whoosh"), (13.70, "word"), (14.55, "tap"), (14.75, "sheet"), (15.00, "type"),
    (15.45, "riser"),
    (16.00, "boom"), (16.10, "confetti"), (16.55, "facet"), (16.67, "facet"), (16.79, "facet"), (16.91, "facet"),
    (17.15, "word"), (17.70, "chip"), (18.05, "chip"), (18.40, "word"), (18.30, "wink"), (19.0, "bells"),
]

# ------------------------------------------------------------------ helpers

_DEVA = {}
_FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")
DEVA_FONT = os.environ.get("NEBY_DEVA_FONT", os.path.join(_FONTS, "Poppins-ExtraBold.ttf"))


def deva_image(s, size, color, weight=None):
    """Devanagari needs real shaping (HarfBuzz via raqm); Skia's drawString cannot do it."""
    key = (s, size, color, weight)
    if key not in _DEVA:
        path = os.path.join(_FONTS, f"Poppins-{weight}.ttf") if weight else DEVA_FONT
        f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
        l, t, r, b = f.getbbox(s)
        im = Image.new("RGBA", (r - l + 20, b - t + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        rgba = ((color >> 16) & 255, (color >> 8) & 255, color & 255, (color >> 24) & 255)
        d.text((10 - l, 10 - t), s, font=f, fill=rgba)
        arr = np.ascontiguousarray(np.array(im))
        _DEVA[key] = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType)
    return _DEVA[key]


def draw_deva(c, s, cx, baseline_y, size, color, alpha=1.0, scale=1.0, weight=None):
    img = deva_image(s, size, color, weight)
    c.save()
    c.translate(cx, baseline_y - img.height() * 0.5)
    c.scale(scale, scale)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(alpha))
    c.drawImage(img, -img.width() / 2, -img.height() / 2, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()


def rise_text(c, s, x, y, f, color, t0, t, align="left", stagger=0.028, dur=0.45, alpha=1.0):
    total = f.measureText(s)
    if align == "center":
        x -= total / 2
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x - 60, y - f.getSize() * 1.25, total + 120, f.getSize() * 1.6))
    pos = x
    for i, ch in enumerate(s):
        k = seg(t, t0 + i * stagger, t0 + i * stagger + dur)
        if k > 0:
            dy = (1 - ease_out_back(k, 1.5)) * f.getSize() * 1.1
            c.drawString(ch, pos, y + dy, f, paint(with_alpha(color, alpha)))
        pos += f.measureText(ch)
    c.restore()
    return total


def chip(c, s, x, y, size, t0, t, fg=BLUE, bg=BLUE_WASH, weight="ExtraBold"):
    f = font(weight, size)
    w = f.measureText(s)
    k = ease_out_back(seg(t, t0, t0 + 0.45), 1.8)
    padx, h = size * 0.30, size * 1.2
    cw = (w + 2 * padx) * clamp(k, 0, 1.25)
    if cw <= 0:
        return w + 2 * padx
    rrect(c, x, y - size * 0.96, cw, h, h * 0.30, paint(bg))
    if k > 0.2:
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(x, y - size * 1.3, cw, size * 1.8))
        c.drawString(s, x + padx, y + (1 - clamp(k)) * size * 0.5, f, paint(fg))
        c.restore()
    return w + 2 * padx


def pop_scale(t, t0, dur=0.42, s=2.0):
    return ease_out_back(seg(t, t0, t0 + dur), s)


def star(c, x, y, s, color):
    if s <= 0.5:
        return
    p = skia.Path()
    p.moveTo(x, y - s)
    p.quadTo(x, y, x + s, y)
    p.quadTo(x, y, x, y + s)
    p.quadTo(x, y, x - s, y)
    p.quadTo(x, y, x, y - s)
    c.drawPath(p, paint(color))


# ------------------------------------------------------------------ the Dashain sky


CUES = [
    (0.00, "air"), (0.25, "rise"), (0.95, "shimmer"), (1.05, "word"), (1.80, "word"), (2.30, "chip"),
    (2.85, "whoosh"), (3.25, "word"),
    (3.70, "kite"), (4.15, "kite"), (4.60, "kite"), (5.05, "kite"),
    (3.80, "land"), (4.25, "land"), (4.70, "land"), (5.15, "land"),
    (5.60, "count"), (6.55, "chip"),
    (6.95, "whoosh"), (7.20, "page"), (7.55, "page"), (7.90, "word"), (8.30, "write"),
    (8.75, "tick"), (8.95, "tick"), (9.15, "tick"), (9.30, "word"),
    (9.60, "pop"), (9.72, "pop"), (9.84, "pop"), (9.96, "pop"), (10.08, "pop"), (10.20, "pop"),
    (10.45, "whoosh"), (10.80, "word"), (11.10, "bubble"), (11.70, "bubble"), (12.30, "bubble"),
    (12.55, "like"), (12.75, "like"), (12.95, "like"),
    (13.35, "whoosh"), (13.65, "word"), (14.05, "page"), (14.45, "write"), (14.78, "tap"), (14.90, "sheet"),
    (15.12, "type"), (15.62, "type"),
    (15.55, "riser"),
    (16.00, "boom"), (16.10, "confetti"), (16.55, "facet"), (16.67, "facet"), (16.79, "facet"), (16.91, "facet"),
    (17.15, "word"), (17.35, "bells"), (17.70, "chip"), (18.05, "chip"), (18.40, "word"), (18.30, "wink"),
    (19.0, "bells"),
]

KITES = []
_r = 99
for i in range(7):
    vals = []
    for _ in range(4):
        _r = (_r * 1103515245 + 12345) & 0x7FFFFFFF
        vals.append(_r / 0x7FFFFFFF)
    KITES.append(dict(x=vals[0] * W, y=(90 + vals[1] * 640) * (H / 1080 if VERT else 1) * (0.6 if VERT else 1),
                      s=0.30 + vals[2] * 0.32, ph=vals[3] * 6.28,
                      col=[TIKA, MARIGOLD, BLUE_BRIGHT, MINT, PURPLE, CORAL, TEAL][i % 7]))


def kite(c, x, y, s, col, t, ph, alpha=1.0):
    sway = math.sin(t * 1.6 + ph) * 8
    c.save()
    c.translate(x, y)
    c.rotate(sway)
    c.scale(s, s)
    c.drawPath(polygon([(0, -60), (44, -6), (0, 62), (-44, -6)]), paint(with_alpha(col, alpha)))
    c.drawPath(polygon([(0, -60), (44, -6), (0, -6)]), paint(with_alpha(mix(col, WHITE, 0.35), alpha)))
    c.drawPath(polygon([(0, -6), (-44, -6), (0, 62)]), paint(with_alpha(mix(col, NAVY, 0.15), alpha)))
    c.drawLine(0, -60, 0, 62, paint(with_alpha(mix(col, NAVY, 0.35), alpha * 0.6), stroke=2))
    c.drawLine(-44, -6, 44, -6, paint(with_alpha(mix(col, NAVY, 0.35), alpha * 0.6), stroke=2))
    tail = skia.Path()
    tail.moveTo(0, 62)
    for k in range(1, 7):
        tail.lineTo(math.sin(t * 4 + ph + k * 0.9) * 14, 62 + k * 22)
    c.drawPath(tail, paint(with_alpha(mix(col, NAVY, 0.2), alpha * 0.8), stroke=3))
    for k in (2, 4, 6):
        bx, by = math.sin(t * 4 + ph + k * 0.9) * 14, 62 + k * 22
        c.drawPath(polygon([(bx - 9, by - 5), (bx + 9, by - 5), (bx, by + 7)]), paint(with_alpha(col, alpha)))
    string = skia.Path()
    string.moveTo(0, 62)
    string.quadTo(60, 320, 30, 900)
    c.drawPath(string, paint(with_alpha(NAVY, 0.10 * alpha), stroke=1.4))
    c.restore()


def sky(c, t, kite_alpha=1.0):
    p = paint(WHITE)
    p.setShader(linear((0, 0), (0, H), [0xFF9FD2FF, 0xFFD6ECFF, 0xFFFFF1DC], [0, 0.55, 1]))
    c.drawPaint(p)
    sx, sy = (W * 0.80, H * 0.17) if VERT else (1560, 210)
    c.drawCircle(sx, sy, 230, paint(with_alpha(0xFFFFE2A6, 0.55), blur=90))
    c.drawCircle(sx, sy, 92, paint(with_alpha(0xFFFFF6E0, 0.95), blur=6))
    clouds = [(300, 230, 1.0, 9), (1250, 140, 0.8, 6), (900, 360, 0.6, 12), (1700, 420, 0.7, 8)]
    for cx0, cy0, s, sp in clouds:
        cy = cy0 * (1.55 if VERT else 1)
        x = (cx0 + t * sp) % (W + 400) - 200
        cloud = paint(with_alpha(WHITE, 0.8))
        for dx, dy, r in [(-60, 10, 48), (0, -14, 66), (64, 6, 52), (110, 22, 36), (-110, 24, 34)]:
            c.drawCircle(x + dx * s, cy + dy * s, r * s, cloud)
    if kite_alpha > 0:
        for k in KITES:
            x = (k["x"] + t * 22 * k["s"]) % (W + 240) - 120
            y = k["y"] + math.sin(t * 0.9 + k["ph"]) * 18
            kite(c, x, y, k["s"] * (1.15 if VERT else 1), k["col"], t, k["ph"], alpha=0.6 * kite_alpha)


def marigold(c, x, y, r, col):
    c.drawCircle(x, y, r, paint(col))
    for i in range(8):
        a = i * math.pi / 4
        c.drawCircle(x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55, r * 0.42, paint(mix(col, 0xFFFFFFFF, 0.18)))
    c.drawCircle(x, y, r * 0.42, paint(mix(col, 0xFF8A3B00, 0.35)))


def garland(c, t, y0=0.0, alpha=1.0, swags=None):
    """Strings of marigolds swagged across the top of the frame."""
    if alpha <= 0:
        return
    swags = swags or (3 if not VERT else 2)
    span = (W + 80) / swags
    c.saveLayerAlpha(None, int(255 * clamp(alpha)))
    for s in range(swags):
        x0 = -40 + s * span
        sag = 70 + 14 * math.sin(t * 1.3 + s)
        n = 15
        pts = []
        for i in range(n + 1):
            u = i / n
            pts.append((x0 + span * u, y0 + 18 + sag * 4 * u * (1 - u)))
        thread = skia.Path()
        thread.moveTo(*pts[0])
        for q in pts[1:]:
            thread.lineTo(*q)
        c.drawPath(thread, paint(0xFF2E7D32, stroke=3))
        for i, (x, y) in enumerate(pts):
            if i % 3 == 1:
                for side in (-1, 1):
                    leaf = skia.Path()
                    leaf.moveTo(x, y)
                    leaf.quadTo(x + side * 18, y + 6, x + side * 26, y + 22)
                    leaf.quadTo(x + side * 6, y + 18, x, y)
                    c.drawPath(leaf, paint(0xFF3D9A45))
            marigold(c, x, y + 6, 15, MARIGOLD if i % 2 else 0xFFFF7A1A)
        tx, ty = pts[0]
        for j in range(3):
            marigold(c, tx, ty + 30 + j * 26, 12, 0xFFFF7A1A if j % 2 else MARIGOLD)
    c.restore()


def ping(c, t, gx, gy, h, alpha=1.0):
    """A Dashain bamboo swing: two crossed bamboo pairs and a rope seat."""
    if alpha <= 0:
        return
    bam = with_alpha(0xFFC79A55, alpha)
    dark = with_alpha(0xFF8A6430, alpha)
    top = (gx, gy - h)
    for dx in (-0.42, 0.42):
        for lean in (-1, 1):
            foot = (gx + dx * h + lean * h * 0.10, gy)
            head = (gx + dx * h * 0.25 - lean * h * 0.05, gy - h * 1.06)
            c.drawLine(foot[0], foot[1], head[0], head[1], paint(bam, stroke=h * 0.03))
            for k in (0.3, 0.55, 0.8):
                c.drawCircle(lerp(foot[0], head[0], k), lerp(foot[1], head[1], k), h * 0.018, paint(dark))
    c.drawLine(gx - h * 0.18, top[1], gx + h * 0.18, top[1], paint(bam, stroke=h * 0.03))
    ang = math.sin(t * 1.9) * 0.42
    L = h * 0.80
    sx, sy = top[0] + math.sin(ang) * L, top[1] + math.cos(ang) * L
    for off in (-h * 0.05, h * 0.05):
        c.drawLine(top[0] + off, top[1], sx + off, sy, paint(with_alpha(0xFF6B4A22, alpha), stroke=2.5))
    c.save()
    c.translate(sx, sy)
    c.rotate(-math.degrees(ang))
    rrect(c, -h * 0.09, -h * 0.012, h * 0.18, h * 0.03, h * 0.012, paint(dark))
    c.restore()


def hills(c, t, rise=1.0, alpha=1.0):
    if rise <= 0:
        return
    off = (1 - rise) * 520
    base0 = H - (320 if not VERT else 360)
    layers = [(0xFFD9E9F7, base0, 0.0016, 70), (0xFFB7D3EE, base0 + 70, 0.0022, 60), (0xFF92BAE3, base0 + 140, 0.003, 45)]
    for li, (col, base, f, amp) in enumerate(layers):
        if li == 1:
            gx = W * (0.80 if not VERT else 0.74)
            gy = base + off + math.sin(gx * f + base) * amp + math.sin(gx * f * 2.7) * amp * 0.35 + 8
            ping(c, t, gx, gy, 260 if not VERT else 300, alpha)
        p = skia.Path()
        p.moveTo(0, H)
        for x in range(0, W + 41, 40):
            y = base + off + math.sin(x * f + base) * amp + math.sin(x * f * 2.7) * amp * 0.35
            p.lineTo(x, y)
        p.lineTo(W, H)
        p.close()
        c.drawPath(p, paint(with_alpha(col, alpha)))


# ------------------------------------------------------------------ S1 hook (0–3)

def s1_hook(c, t):
    if t > 3.4:
        return
    out = ease_in_cubic(seg(t, 2.85, 3.3))
    c.save()
    c.translate(0, -out * 400)
    if not VERT:
        f = font("ExtraBold", 112)
        rise_text(c, "This Dashain,", CX, 250, f, INK, 1.05, t, align="center")
        w1 = f.measureText("your ")
        w2 = f.measureText("books") + 2 * 0.30 * 112
        w3 = f.measureText(" are here.")
        x0 = CX - (w1 + w2 + w3) / 2
        rise_text(c, "your ", x0, 390, f, INK, 1.80, t)
        chip(c, "books", x0 + w1, 390, 112, 2.30, t)
        rise_text(c, " are here.", x0 + w1 + w2, 390, f, INK, 1.95, t)
    else:
        f = font("ExtraBold", 112)
        rise_text(c, "This Dashain,", CX, 430, f, INK, 1.05, t, align="center")
        w1 = f.measureText("your ")
        w2 = f.measureText("books") + 2 * 0.30 * 112
        x0 = CX - (w1 + w2) / 2
        rise_text(c, "your ", x0, 570, f, INK, 1.80, t)
        chip(c, "books", x0 + w1, 570, 112, 2.30, t)
        rise_text(c, "are here.", CX, 710, f, INK, 1.95, t, align="center")
    kk = seg(t, 2.45, 2.85)
    if kk > 0:
        e = ease_out_back(kk, 2.0)
        img = deva_image("विजया दशमीको शुभकामना", 40, WHITE, "SemiBold")
        py = 480 if not VERT else 830
        pw = img.width() + 60
        c.save()
        c.translate(CX, py)
        c.scale(e, e)
        rrect(c, -pw / 2, -38, pw, 76, 38, paint(TIKA))
        c.restore()
        draw_deva(c, "विजया दशमीको शुभकामना", CX, py + img.height() / 2 + 2, 40, WHITE, alpha=clamp(kk * 2), scale=e, weight="SemiBold")
    c.restore()


# ------------------------------------------------------------------ S2 notes & question banks (3–7)

GRADES = [("8", "Class 8", BLUE_BRIGHT), ("10", "Class 10", TIKA), ("11", "Class 11", MINT), ("12", "Class 12", PURPLE)]


def grade_book(c, x, y, w, h, num, label, col, t, k_inner):
    shadow_rrect(c, x, y, w, h, 22, alpha=0.20, dy=22, blur=28)
    p = paint(WHITE)
    p.setShader(linear((x, y), (x + w, y + h), [mix(col, WHITE, 0.10), col, mix(col, NAVY, 0.25)], [0, 0.5, 1]))
    rrect(c, x, y, w, h, 22, p)
    rrect(c, x, y, 26, h, 12, paint(with_alpha(NAVY, 0.18)))
    for k in range(5):
        c.drawCircle(x + w - 28, y + 40 + k * 18, 4, paint(with_alpha(MARIGOLD, 0.9)))
    text(c, num, x + w / 2 + 10, y + h * 0.50, font("ExtraBold", 150 if len(num) < 2 else 132), WHITE, "center")
    text(c, label.upper(), x + w / 2 + 10, y + 64, font("Bold", 24), with_alpha(WHITE, 0.85), "center")
    for j, lab in enumerate(["Notes", "Question bank"]):
        kj = seg(k_inner, 0.2 + j * 0.25, 0.6 + j * 0.25)
        if kj > 0:
            e = ease_out_back(kj, 2)
            fw = font("Bold", 26)
            pw = fw.measureText(lab) + 34
            c.save()
            c.translate(x + w / 2 + 10, y + h - 112 + j * 54)
            c.scale(e, e)
            rrect(c, -pw / 2, -22, pw, 44, 22, paint(WHITE))
            text(c, lab, 0, 9, fw, col, "center")
            c.restore()


def s2_books(c, t):
    if t < 2.9 or t > 7.4:
        return
    out = ease_in_cubic(seg(t, 6.9, 7.3))
    c.save()
    c.translate(0, -out * 400)
    if not VERT:
        rise_text(c, "Notes & question banks", 110, 200, font("ExtraBold", 92), INK, 3.25, t)
        sub_y, sub_lines = 268, ["Full books, chapter by chapter, for NEB and SEE."]
        cy_counter = 372
    else:
        rise_text(c, "Notes &", 80, 330, font("ExtraBold", 108), INK, 3.25, t)
        rise_text(c, "question banks", 80, 450, font("ExtraBold", 108), INK, 3.40, t)
        sub_y, sub_lines = 530, ["Full books, chapter by chapter,", "for NEB and SEE."]
        cy_counter = 700
    ks = seg(t, 3.6, 4.0)
    if ks > 0:
        for i, ln in enumerate(sub_lines):
            text(c, ln, (116 if not VERT else 84), sub_y + i * 52, font("Medium", 40), with_alpha(MUTED, ks))
    c.restore()
    for i, (num, label, col) in enumerate(GRADES):
        t0 = 3.70 + i * 0.45
        k = seg(t, t0 - 0.30, t0 + 0.10)
        if k <= 0:
            continue
        if not VERT:
            w, h, sc = 300, 420, 1.0
            tx, ty = 150 + i * 345, 450 + (1 if i % 2 else 0) * 26
        else:
            w, h, sc = 300, 420, 1.18
            tx = 150 + (i % 2) * 430
            ty = 820 + (i // 2) * 540 + (1 if i % 2 else 0) * 24
        e = ease_out_cubic(k)
        x = lerp(tx + 700, tx, e)
        y = lerp(ty - 650, ty, e) + math.sin(math.pi * clamp(k)) * -80
        rot = lerp(-38, -4 + i * 2.5, e)
        settle = t - (t0 + 0.10)
        sq = 0.05 * math.exp(-max(settle, 0) * 8) * math.cos(max(settle, 0) * 28) if settle > 0 else 0
        y -= out * (1300 + 80 * i)
        bob = math.sin(t * 2 + i) * 6 if settle > 0 else 0
        c.save()
        c.translate(x + w * sc / 2, y + h * sc + bob)
        c.rotate(rot)
        c.scale((1 + sq) * sc, (1 - sq) * sc)
        if k < 1:
            tail = skia.Path()
            tail.moveTo(0, -h / 2)
            for q in range(1, 6):
                tail.lineTo(80 * q + math.sin(t * 9 + q) * 14, -h / 2 - 70 * q)
            c.drawPath(tail, paint(with_alpha(col, 0.5 * (1 - k)), stroke=6))
        grade_book(c, -w / 2, -h, w, h, num, label, col, t, seg(t, t0, t0 + 0.9))
        c.restore()
    kc = seg(round(t * FPS) / FPS, 5.6, 6.5)
    if kc > 0 and out < 1:
        a = clamp(kc * 4) * (1 - out)
        n = int(round(6000 * ease_out_cubic(kc) / 10) * 10)
        lab = f"{n:,}" + ("+" if kc >= 1 else "")
        f = font("ExtraBold", 60 if not VERT else 72)
        x = 116 if not VERT else 84
        yy = cy_counter - out * 400
        text(c, lab, x, yy, f, with_alpha(BLUE, a))
        fw = f.measureText("6,000+")
        fs = font("SemiBold", 38 if not VERT else 44)
        text(c, "pages", x + fw + 16, yy, fs, with_alpha(MUTED, a))
        kf = seg(t, 6.55, 6.95)
        if kf > 0:
            e = ease_out_back(kf, 2.4)
            px = x + fw + 16 + fs.measureText("pages") + 30 + 92
            c.save()
            c.translate(px, yy - 20)
            c.scale(e, e)
            rrect(c, -92, -32, 184, 64, 32, paint(MINT))
            text(c, "All free", 0, 12, font("ExtraBold", 32), WHITE, "center")
            c.restore()


# ------------------------------------------------------------------ S3 inside a book (7–10.5)

SUBJECTS = [("Physics", BLUE_BRIGHT), ("Chemistry", MINT), ("Biology", CORAL), ("Mathematics", PURPLE),
            ("नेपाली", TIKA), ("English", TEAL), ("सामाजिक", MARIGOLD), ("Accountancy", BLUE),
            ("Computer Science", NAVY), ("Science", MINT), ("Economics", CORAL), ("Health", TEAL)]


def open_book(c, t, bw, bh):
    c.drawOval(skia.Rect.MakeXYWH(-bw * 0.52, bh * 0.46, bw * 1.04, 70), paint(with_alpha(NAVY, 0.16), blur=24))
    rrect(c, -bw / 2 - 20, -bh / 2 + 14, bw + 40, bh + 16, 30, paint(BLUE))
    for side in (-1, 1):
        p = skia.Path()
        p.moveTo(0, -bh / 2 + 18)
        p.cubicTo(side * bw * 0.18, -bh / 2 - 10, side * bw * 0.36, -bh / 2 + 4, side * bw / 2, -bh / 2 + 2)
        p.lineTo(side * bw / 2, bh / 2 - 6)
        p.cubicTo(side * bw * 0.36, bh / 2 - 2, side * bw * 0.18, bh / 2 - 16, 0, bh / 2 + 6)
        p.close()
        c.drawPath(p, paint(WHITE))
        sh = paint(WHITE)
        sh.setShader(linear((0, 0), (side * 100, 0), [with_alpha(NAVY, 0.10), with_alpha(NAVY, 0.0)]))
        c.drawPath(p, sh)
    for tf in (7.2, 7.55):
        kf = seg(t, tf, tf + 0.35)
        if 0 < kf < 1:
            ang = math.pi * ease_in_out(kf)
            pw = bw / 2 * math.cos(ang)
            p = skia.Path()
            p.moveTo(0, -bh / 2 + 18)
            p.lineTo(pw, -bh / 2 + 2 - math.sin(ang) * 40)
            p.lineTo(pw, bh / 2 - 6 - math.sin(ang) * 40)
            p.lineTo(0, bh / 2 + 6)
            p.close()
            c.drawPath(p, paint(mix(WHITE, BLUE_WASH, 0.4 * math.sin(ang))))
    c.drawLine(0, -bh / 2 + 22, 0, bh / 2 + 2, paint(with_alpha(NAVY, 0.15), stroke=3))
    if t <= 7.9:
        return
    lx = -bw / 2 + 70
    text(c, "Worked example 4.2", lx, -bh / 2 + 90, font("Bold", 30), BLUE_BRIGHT)
    kl = seg(t, 8.0, 8.9)
    for i in range(4):
        kk = clamp(kl * 2.0 - i * 0.22)
        if kk > 0:
            c.drawLine(lx, -bh / 2 + 150 + i * 44, lx + (bw / 2 - 160) * (0.9 if i % 2 == 0 else 0.65) * ease_out_cubic(kk),
                       -bh / 2 + 150 + i * 44, paint(mix(BLUE_WASH, MUTED, 0.25), stroke=11))
    kb = seg(t, 8.3, 8.8)
    if kb > 0:
        bx, by = lx, -bh / 2 + 340
        rrect(c, bx, by, 440 * ease_out_cubic(kb), 96, 16, paint(mix(AMBER, WHITE, 0.82)))
        rrect(c, bx, by, 8, 96, 4, paint(AMBER))
        if kb > 0.6:
            text(c, "F = m × a", bx + 40, by + 64, font("Bold", 44), with_alpha(INK, (kb - 0.6) / 0.4))
    rx, base = 80, -40
    circle = skia.Path()
    circle.addCircle(rx + 150, base - 110, 100)
    c.drawPath(partial_path(circle, seg(t, 8.1, 8.6)), paint(CORAL, stroke=6))
    tri = polygon([(rx + 150, base - 210), (rx + 237, base - 60), (rx + 63, base - 60)])
    c.drawPath(partial_path(tri, seg(t, 8.4, 8.9)), paint(PURPLE, stroke=6))
    for q in range(3):
        y = 60 + q * 62
        kk = seg(t, 8.75 + q * 0.2, 9.05 + q * 0.2)
        c.drawLine(rx + 70, y + 2, rx + 400, y + 2, paint(mix(BLUE_WASH, MUTED, 0.2), stroke=11))
        if kk > 0:
            e = ease_out_back(kk, 2.5)
            c.drawCircle(rx + 22, y, 24 * e, paint(MINT))
            ck = skia.Path()
            ck.moveTo(rx + 11, y + 1)
            ck.lineTo(rx + 19, y + 10)
            ck.lineTo(rx + 34, y - 9)
            c.drawPath(partial_path(ck, kk), paint(WHITE, stroke=6))


def subject_chips(c, t, rows, y0, dy, k_out, size=31):
    fw = font("Bold", size)

    def chip_w(sname):
        deva = any("ऀ" <= ch <= "ॿ" for ch in sname)
        return (deva_image(sname, size, WHITE, "Bold").width() - 20 if deva else fw.measureText(sname)) + 48, deva

    idx = 0
    for row, items in enumerate(rows):
        widths = [chip_w(n)[0] for n, _ in items]
        total = sum(widths) + 26 * (len(items) - 1)
        x = CX - total / 2
        for j, (sname, col) in enumerate(items):
            pw, deva = chip_w(sname)
            t0 = 9.6 + j * 0.12 + row * 0.06
            k = seg(t, t0, t0 + 0.5)
            cxp = x + pw / 2
            x += pw + 26
            idx += 1
            if k <= 0:
                continue
            e = ease_out_back(k, 2.2)
            y = y0 + row * dy + (1 - e) * 120 + k_out * 400
            c.save()
            c.translate(cxp, y)
            c.scale(e, e)
            shadow_rrect(c, -pw / 2, -32, pw, 64, 32, alpha=0.14, dy=8, blur=12)
            rrect(c, -pw / 2, -32, pw, 64, 32, paint(col))
            if deva:
                draw_deva(c, sname, 0, 20, size, WHITE, weight="Bold")
            else:
                text(c, sname, 0, 12, fw, WHITE, "center")
            c.restore()


def s3_inside(c, t):
    if t < 6.9 or t > 10.8:
        return
    k_in = ease_out_back(seg(t, 7.0, 7.45), 1.2)
    k_out = ease_in_cubic(seg(t, 10.35, 10.75))
    alpha = clamp(seg(t, 7.0, 7.2)) * (1 - k_out)
    cx, cy = (960, 590) if not VERT else (CX, 1090)
    bw, bh = 1180, 540
    base_s = 1.0 if not VERT else 0.86
    c.save()
    c.translate(cx, cy + k_out * 160)
    s = lerp(0.55, 1.0, k_in) * (1 - 0.35 * k_out) * base_s
    c.scale(s, s)
    c.saveLayerAlpha(None, int(255 * alpha))
    open_book(c, t, bw, bh)
    c.restore()
    c.restore()
    up = k_out * 260
    f = font("ExtraBold", 88 if not VERT else 96)
    k1 = seg(t, 7.9, 8.3)
    k1o = ease_in_cubic(seg(t, 9.05, 9.3))
    ty = 190 if not VERT else 610
    if k1 > 0 and k1o < 1:
        e = ease_out_back(k1, 1.8)
        c.save()
        c.translate(CX, ty - k1o * 150)
        c.scale(e, e)
        text(c, "Every chapter.", 0, 0, f, with_alpha(INK, 1 - k1o), "center")
        c.restore()
    k2 = seg(t, 9.3, 9.7)
    if k2 > 0:
        e = ease_out_back(k2, 1.8)
        c.save()
        c.translate(CX, ty - up)
        c.scale(e, e)
        if not VERT:
            w1, w2 = f.measureText("Every answer "), f.measureText("worked out.")
            text(c, "Every answer ", -(w1 + w2) / 2, 0, f, INK)
            text(c, "worked out.", -(w1 + w2) / 2 + w1, 0, f, BLUE_BRIGHT)
        else:
            text(c, "Every answer", 0, -110, f, INK, "center")
            text(c, "worked out.", 0, 0, f, BLUE_BRIGHT, "center")
        c.restore()
    if not VERT:
        subject_chips(c, t, [SUBJECTS[:6], SUBJECTS[6:]], 948, 76, k_out)
    else:
        subject_chips(c, t, [SUBJECTS[0:3], SUBJECTS[3:6], SUBJECTS[6:9], SUBJECTS[9:12]], 1500, 84, k_out, size=34)


# ------------------------------------------------------------------ S4 community (10.5–13.5)

THREAD = [
    ("Aarav", "A", CORAL, "Any trick for balancing chemical equations?", 11.10, None),
    ("Sita", "S", MINT, "Balance the metals first, oxygen last.", 11.70, "12"),
    ("Bikash", "B", PURPLE, "That trick just saved my SEE prep!", 12.30, "8"),
]


def s4_together(c, t):
    if t < 10.4 or t > 13.8:
        return
    out = ease_in_cubic(seg(t, 13.35, 13.75))
    c.save()
    c.translate(0, -out * 420)
    if not VERT:
        f = font("ExtraBold", 96)
        w = rise_text(c, "Ask.", 110, 230, f, INK, 10.80, t)
        w2 = rise_text(c, "Answer.", 110 + w + 30, 230, f, INK, 10.95, t)
        chip(c, "Study together.", 110 + w + w2 + 60, 230, 96, 11.15, t, fg=0xFFB84B0B, bg=0xFFFFEFCF)
    else:
        f = font("ExtraBold", 112)
        w = rise_text(c, "Ask.", 80, 380, f, INK, 10.80, t)
        rise_text(c, "Answer.", 80 + w + 30, 380, f, INK, 10.95, t)
        chip(c, "Study together.", 80, 530, 104, 11.15, t, fg=0xFFB84B0B, bg=0xFFFFEFCF)
    c.restore()
    for i, (name, ini, col, msg, t0, likes) in enumerate(THREAD):
        k = seg(t, t0, t0 + 0.45)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        if not VERT:
            bw, bh = 980, 128
            x = 560 + (90 if i == 1 else 0)
            y = 380 + i * 158
            fs = 32
        else:
            bw, bh = 940, 150
            x = 70 + (60 if i == 1 else 0)
            y = 650 + i * 190
            fs = 30
        y += (1 - e) * 60 + out * 1200
        c.save()
        c.translate(x, y)
        c.scale(lerp(0.8, 1.0, e), lerp(0.8, 1.0, e))
        a = clamp(k * 3)
        shadow_rrect(c, 0, 0, bw, bh, 30, alpha=0.14 * a, dy=14, blur=20)
        rrect(c, 0, 0, bw, bh, 30, paint(with_alpha(WHITE, a)))
        c.drawCircle(68, bh / 2, 40, paint(with_alpha(col, a)))
        text(c, ini, 68, bh / 2 + 15, font("ExtraBold", 40), with_alpha(WHITE, a), "center")
        text(c, name, 130, bh / 2 - 12, font("Bold", 30), with_alpha(INK, a))
        n_chars = int(len(msg) * clamp(seg(t, t0 + 0.15, t0 + 0.7)))
        text(c, msg[:n_chars], 130, bh / 2 + 32, font("Medium", fs), with_alpha(MUTED, a))
        if likes:
            kl = seg(t, 12.55 + (0.2 if i == 2 else 0), 12.85 + (0.2 if i == 2 else 0))
            if kl > 0:
                el = ease_out_back(kl, 3)
                c.save()
                c.translate(bw - 90, (bh / 2) if not VERT else 40)
                c.scale(el, el)
                rrect(c, -56, -28, 112, 56, 28, paint(BLUE_WASH))
                c.drawPath(polygon([(-34, 8), (-34, -6), (-24, -6), (-14, -22), (-8, -18), (-12, -6), (0, -6), (-4, 12), (-34, 12)]), paint(BLUE))
                text(c, likes, 22, 11, font("Bold", 30), BLUE, "center")
                c.restore()
        c.restore()


# ------------------------------------------------------------------ S5 read anywhere (13.4–16)

def phone_ui(c, x, y, w, t):
    """An Android reader, drawn in a 500 x 980 design space scaled to width w."""
    s = w / 500.0
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    shadow_rrect(c, 0, 0, 500, 980, 66, alpha=0.30, dy=34, blur=40)
    rrect(c, 0, 0, 500, 980, 66, paint(0xFF0F1626))
    rrect(c, 4, 4, 492, 972, 62, paint(0xFF1C2638, stroke=3))
    sx, sy, sw, sh = 16, 16, 468, 948
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx, sy, sw, sh), 52, 52), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(sx, sy, sw, sh), paint(0xFFF3F5FA))
    text(c, "10:08", sx + 44, sy + 42, font("SemiBold", 20), INK)
    c.drawCircle(sx + sw / 2, sy + 30, 9, paint(0xFF0F1626))
    for k in range(3):
        rrect(c, sx + sw - 92 + k * 22, sy + 28 - k * 4, 14, 12 + k * 4, 3, paint(INK))
    c.drawRect(skia.Rect.MakeXYWH(sx, sy + 58, sw, 92), paint(WHITE))
    arrow = skia.Path()
    arrow.moveTo(sx + 44, sy + 92)
    arrow.lineTo(sx + 32, sy + 104)
    arrow.lineTo(sx + 44, sy + 116)
    c.drawPath(arrow, paint(INK, stroke=4))
    text(c, "Science & Technology", sx + 70, sy + 100, font("Bold", 24), INK)
    text(c, "Class 10 · NEBians notes", sx + 70, sy + 130, font("Medium", 18), MUTED)
    page_no = "83" if t < 14.2 else "84"
    rrect(c, sx + sw - 120, sy + 86, 96, 38, 19, paint(BLUE_WASH))
    text(c, f"{page_no} / 275", sx + sw - 72, sy + 112, font("Bold", 18), BLUE, "center")
    px, py, pw, ph = sx + 22, sy + 168, sw - 44, sh - 200
    turn = ease_in_out(seg(t, 14.05, 14.40))
    for which, off in (("A", -turn), ("B", 1 - turn)):
        if (which == "A" and turn >= 1) or (which == "B" and turn <= 0):
            continue
        ox = off * (pw + 40)
        c.save()
        c.translate(ox, 0)
        shadow_rrect(c, px, py, pw, ph, 14, alpha=0.08, dy=6, blur=10)
        rrect(c, px, py, pw, ph, 14, paint(WHITE))
        if which == "A":
            text(c, "5.1 Reflection of light", px + 28, py + 56, font("Bold", 24), BLUE_BRIGHT)
            for i in range(14):
                L = (pw - 56) * (0.95 if i % 4 else 0.62)
                c.drawLine(px + 28, py + 100 + i * 38, px + 28 + L, py + 100 + i * 38, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=9))
        else:
            text(c, "5.2 Refraction of light", px + 28, py + 56, font("Bold", 24), BLUE_BRIGHT)
            hk = ease_out_cubic(seg(t, 14.45, 14.70))
            for i in range(3):
                yy = py + 100 + i * 38
                if i == 1 and hk > 0:
                    rrect(c, px + 22, yy - 16, (pw - 44) * hk, 32, 8, paint(with_alpha(0xFFFFD84D, 0.75)))
                c.drawLine(px + 28, yy, px + 28 + (pw - 56) * (0.95 if i < 2 else 0.7), yy, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=9))
            gx, gy, gw, gh = px + 40, py + 230, pw - 80, 210
            rrect(c, gx, gy, gw, gh, 12, paint(0xFFF2F7FF))
            rrect(c, gx + gw * 0.30, gy + 60, gw * 0.40, gh - 100, 6, paint(with_alpha(0xFF9CC9F5, 0.55)))
            c.drawLine(gx + 20, gy + 20, gx + gw * 0.30, gy + 60, paint(CORAL, stroke=4))
            c.drawLine(gx + gw * 0.30, gy + 60, gx + gw * 0.70, gy + gh - 40, paint(CORAL, stroke=4))
            c.drawLine(gx + gw * 0.70, gy + gh - 40, gx + gw - 20, gy + gh - 4, paint(CORAL, stroke=4))
            c.drawLine(gx + gw * 0.30, gy + 20, gx + gw * 0.30, gy + 110, paint(with_alpha(MUTED, 0.6), stroke=2))
            text(c, "i", gx + gw * 0.24, gy + 50, font("Bold", 20), MUTED)
            text(c, "r", gx + gw * 0.36, gy + 104, font("Bold", 20), MUTED)
            rrect(c, px + 28, py + 470, pw - 56, 70, 12, paint(mix(AMBER, WHITE, 0.84)))
            rrect(c, px + 28, py + 470, 6, 70, 3, paint(AMBER))
            text(c, "n = sin i ÷ sin r", px + 54, py + 516, font("Bold", 28), INK)
            for i in range(4):
                yy = py + 590 + i * 38
                c.drawLine(px + 28, yy, px + 28 + (pw - 56) * (0.9 if i % 3 else 0.6), yy, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=9))
        c.restore()
    ka = seg(t, 14.75, 14.98)
    fx, fy = sx + sw - 120, sy + sh - 96
    pulse = 1 + 0.05 * math.sin(t * 8) * (1 if t < 14.75 else 0)
    c.save()
    c.translate(fx, fy)
    sc = pulse * (1 - 0.12 * math.sin(math.pi * ka))
    c.scale(sc, sc)
    rrect(c, -96, -36, 192, 72, 36, paint(with_alpha(NAVY, 0.25), blur=10))
    rrect(c, -96, -36, 192, 72, 36, paint(BLUE_BRIGHT))
    star(c, -62, 0, 14, WHITE)
    text(c, "Ask Neby", 18, 10, font("Bold", 26), WHITE, "center")
    c.restore()
    if 0 < ka < 1:
        c.drawCircle(fx, fy, 30 + 150 * ka, paint(with_alpha(BLUE_BRIGHT, 0.35 * (1 - ka))))
    ksh = ease_out_cubic(seg(t, 14.88, 15.18))
    sheet_top = None
    if ksh > 0:
        c.drawRect(skia.Rect.MakeXYWH(sx, sy, sw, sh), paint(with_alpha(NAVY, 0.28 * ksh)))
        top = sy + sh - 600 * ksh
        sheet_top = top
        rrect(c, sx, top, sw, 640, 40, paint(WHITE))
        rrect(c, sx + sw / 2 - 40, top + 14, 80, 8, 4, paint(mix(BLUE_WASH, MUTED, 0.3)))
        text(c, "Ask Neby", sx + 150, top + 78, font("Bold", 30), INK)
        text(c, "about page 84", sx + 150, top + 112, font("Medium", 20), MUTED)
        q = "Why does a pencil look bent in water?"
        kq = seg(t, 15.10, 15.42)
        if kq > 0:
            fq = font("SemiBold", 20)
            n = max(1, int(len(q) * kq))
            qw = fq.measureText(q) + 40
            rrect(c, sx + sw - 24 - qw, top + 150, qw, 54, 27, paint(BLUE_BRIGHT))
            text(c, q[:n], sx + sw - 24 - qw + 20, top + 184, fq, WHITE)
        kd = seg(t, 15.42, 15.60)
        if kd > 0:
            bx, by, bwid = sx + 24, top + 228, sw - 90
            ans = ["Light bends when it leaves water", "and enters air, so the pencil seems", "to break. That is refraction (5.2)."]
            ka2 = seg(t, 15.60, 15.98)
            lines = len(ans) if ka2 > 0 else 1
            bh2 = 30 + 34 * lines + 10
            rrect(c, bx, by, bwid, bh2, 22, paint(0xFFEFF3FB))
            if ka2 <= 0:
                for d in range(3):
                    c.drawCircle(bx + 34 + d * 22, by + 36, 6 + 2 * math.sin(t * 14 + d), paint(MUTED))
            else:
                total = sum(len(a) for a in ans)
                n = int(total * ka2)
                for i, ln in enumerate(ans):
                    m = max(0, min(len(ln), n))
                    n -= len(ln)
                    if m > 0:
                        text(c, ln[:m], bx + 22, by + 44 + i * 34, font("Medium", 20), INK)
                if ka2 > 0.9:
                    rrect(c, bx, by + bh2 + 14, 170, 40, 20, paint(BLUE_WASH))
                    text(c, "From page 84", bx + 85, by + bh2 + 41, font("SemiBold", 18), BLUE, "center")
    c.restore()
    c.restore()
    if sheet_top is not None:
        return (x + (sx + 78) * s, y + (sheet_top + 86) * s, 110 * s)
    return None


def feature_rows(c, t, x, y0, dy, size):
    rows = [("All notes & question banks", BLUE_BRIGHT, "book"), ("A clean reader, page by page", PURPLE, "page"),
            ("Stuck? Ask Neby about the page", MINT, "neby")]
    for i, (label, col, kind) in enumerate(rows):
        k = seg(t, 14.0 + i * 0.15, 14.4 + i * 0.15)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.8)
        yy = y0 + i * dy
        c.save()
        c.translate(x + 30, yy)
        c.scale(e, e)
        c.drawCircle(0, 0, 30, paint(mix(col, WHITE, 0.82)))
        if kind == "book":
            rrect(c, -14, -16, 28, 32, 4, paint(col))
            c.drawLine(-6, -16, -6, 16, paint(WHITE, stroke=2))
        elif kind == "page":
            rrect(c, -12, -16, 24, 32, 4, paint(col, stroke=3))
            c.drawLine(-6, -6, 6, -6, paint(col, stroke=3))
            c.drawLine(-6, 2, 6, 2, paint(col, stroke=3))
        else:
            star(c, 0, 0, 16, col)
        c.restore()
        text(c, label, x + 80, yy + size * 0.36, font("SemiBold", size), with_alpha(INK, clamp(k * 2)))


def play_badge(c, cx, cy, k):
    if k <= 0:
        return
    e = ease_out_back(k, 2)
    c.save()
    c.translate(cx, cy)
    c.scale(e, e)
    rrect(c, -190, -46, 380, 92, 22, paint(0xFF0F1626))
    tri = [(-150, -24), (-150, 24), (-104, 0)]
    cols = [0xFF34A853, 0xFF4285F4, 0xFFFBBC04, 0xFFEA4335]
    c.drawPath(polygon([tri[0], tri[1], (-127, 0)]), paint(cols[1]))
    c.drawPath(polygon([tri[0], (-127, 0), tri[2]]), paint(cols[0]))
    c.drawPath(polygon([tri[1], (-127, 0), tri[2]]), paint(cols[3]))
    text(c, "GET IT ON", -84, -8, font("SemiBold", 18), with_alpha(WHITE, 0.85))
    text(c, "Google Play", -84, 28, font("Bold", 34), WHITE)
    c.restore()


def s5_app(c, t):
    if t < 13.3 or t > 16.25:
        return
    k_in = ease_out_back(seg(t, 13.40, 13.95), 1.25)
    k_out = ease_in_cubic(seg(t, 15.82, 16.05))
    if not VERT:
        c.save()
        c.translate(-k_out * 900, 0)
        rise_text(c, "Read anywhere.", 120, 300, font("ExtraBold", 100), INK, 13.65, t)
        ks = seg(t, 13.9, 14.3)
        if ks > 0:
            text(c, "Every book, right in your pocket.", 126, 378, font("Medium", 40), with_alpha(MUTED, ks))
        feature_rows(c, t, 120, 480, 92, 34)
        play_badge(c, 120 + 190, 800, seg(t, 14.45, 14.85))
        c.restore()
        w = 470
        x, y = 1180, lerp(1250, 75, k_in)
        tilt = (1 - clamp(k_in)) * 12 - 2
    else:
        c.save()
        c.translate(0, -k_out * 600)
        rise_text(c, "Read anywhere.", CX, 260, font("ExtraBold", 110), INK, 13.65, t, align="center")
        ks = seg(t, 13.9, 14.3)
        if ks > 0:
            text(c, "Every book, right in your pocket.", CX, 340, font("Medium", 40), with_alpha(MUTED, ks), "center")
        c.restore()
        play_badge(c, CX, 1790 + k_out * 400, seg(t, 14.45, 14.85))
        w = 640
        x, y = CX - w / 2, lerp(2000, 420, k_in) + k_out * 1600
        tilt = (1 - clamp(k_in)) * 10
    c.save()
    hw = w * 490 / 500
    c.rotate(tilt, x + w / 2, y + hw)
    sheet = phone_ui(c, x, y, w, t)
    if sheet:
        nx, ny, ns = sheet
        neby().draw(c, t, nx, ny, ns * 1.35, shadow=False)
    c.restore()


# ------------------------------------------------------------------ S6 end card (16–20)

PETALS = []
_q = 3
for i in range(34):
    v = []
    for _ in range(4):
        _q = (_q * 1103515245 + 12345) & 0x7FFFFFFF
        v.append(_q / 0x7FFFFFFF)
    PETALS.append(v)


def petals(c, t, t0):
    if t < t0:
        return
    u = t - t0
    for i, (a, b, d, e) in enumerate(PETALS):
        y = -60 + (u * (140 + 160 * d) + b * H * 0.4) - 60 * (1 - min(1, u * 2))
        if y > H + 40:
            continue
        x = a * W + math.sin(u * (1.2 + d) + i) * 50
        c.save()
        c.translate(x, y)
        c.rotate(u * (90 + 160 * e) * (1 if i % 2 else -1) + i * 30)
        col = MARIGOLD if i % 3 else 0xFFFF7A1A
        if i % 7 == 0:
            col = TIKA
        c.scale(1, 0.55 + 0.45 * abs(math.sin(u * 3 + i)))
        c.drawOval(skia.Rect.MakeXYWH(-9, -14, 18, 28), paint(with_alpha(col, 0.95)))
        c.restore()


def s6_end(c, t):
    if t < 15.85:
        return
    k = ease_in_out(seg(t, 15.90, 16.25))
    p = paint(WHITE)
    origin = (1220, 560) if not VERT else (CX, 1150)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(origin[0], origin[1] - 40), 1600,
                                                [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
    c.drawCircle(origin[0], origin[1], 2800 * k, p)
    if t < 16.0:
        return
    glow = paint(with_alpha(0xFFFFB347, 0.20), blur=160)
    c.drawCircle(origin[0], (520 if not VERT else 1000), 520, glow)
    for i, kk in enumerate(KITES[:6]):
        x = (kk["x"] * 0.9 + t * 30 * kk["s"]) % (W + 240) - 120
        y = 140 + (i * 157) % (760 if not VERT else 1500) + math.sin(t + kk["ph"]) * 16
        kite(c, x, y, kk["s"] * 0.55, mix(kk["col"], WHITE, 0.15), t, kk["ph"], alpha=0.22)
    garland(c, t, y0=-10, alpha=seg(t, 16.05, 16.45))
    petals(c, t, 16.15)
    if not VERT:
        lx, tile_y, word_y, sub_y, url_y, free_y, d_y = 1220, 300, 560, 630, 730, 830, 940
        nx, ny, ns = 470, 600, 500
    else:
        lx, tile_y, word_y, sub_y, url_y, free_y, d_y = CX, 870, 1150, 1225, 1335, 1430, 1570
        nx, ny, ns = CX, 460, 470
    fy = math.sin(t * 2.0) * 5
    kt0 = seg(t, 16.35, 16.75)
    if kt0 > 0:
        e = ease_out_back(kt0, 1.7)
        c.save()
        c.translate(lx, tile_y + fy)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -130, -130 + 18, 260, 260, 64, paint(with_alpha(0xFF001A66, 0.35), blur=26))
        rrect(c, -130, -130, 260, 260, 64, paint(WHITE))
        c.restore()
    logo(c, lx - 5, tile_y + fy, 180, seg(t, 16.5, 17.3) * 1.25, t, on_blue=False)
    rise_text(c, "NEBians", lx, word_y, font("ExtraBold", 136), WHITE, 17.15, t, align="center", stagger=0.04)
    kt = seg(t, 17.5, 17.9)
    if kt > 0:
        text(c, "Notes & question banks · Class 8, 10, 11, 12", lx, sub_y + (1 - ease_out_cubic(kt)) * 20,
             font("SemiBold", 38 if not VERT else 34), with_alpha(0xFFDCE6FF, kt), "center")
    ku = seg(t, 17.7, 18.1)
    if ku > 0:
        e = ease_out_back(ku, 1.8)
        fu = font("Bold", 42)
        url = "nebians.consica.com.np"
        uw = fu.measureText(url) + 80
        c.save()
        c.translate(lx, url_y)
        c.scale(e, e)
        rrect(c, -uw / 2, -42, uw, 84, 42, paint(WHITE))
        text(c, url, 0, 15, fu, BLUE, "center")
        c.restore()
    ks = seg(t, 18.05, 18.45)
    if ks > 0:
        text(c, "Free on the web  ·  Android app on Google Play", lx, free_y, font("Medium", 32 if not VERT else 30),
             with_alpha(0xFFC9D8FF, ks), "center")
    kd = seg(t, 18.4, 18.9)
    if kd > 0:
        e = ease_out_back(kd, 2.2)
        img = deva_image("शुभ दशैँ", 60, WHITE)
        pw = img.width() + 150
        c.save()
        c.translate(lx, d_y)
        c.scale(e, e)
        rrect(c, -pw / 2, -54, pw, 108, 54, paint(TIKA))
        rrect(c, -pw / 2 + 6, -48, pw - 12, 96, 48, paint(with_alpha(MARIGOLD, 0.9), stroke=3))
        marigold(c, -pw / 2 + 48, 0, 16, MARIGOLD)
        marigold(c, pw / 2 - 48, 0, 16, 0xFFFF7A1A)
        c.restore()
        draw_deva(c, "शुभ दशैँ", lx, d_y + img.height() / 2 + 2, 60, WHITE, alpha=clamp(kd * 2), scale=e)
        kv = seg(t, 18.75, 19.15)
        if kv > 0:
            draw_deva(c, "विजया दशमीको हार्दिक शुभकामना", lx, d_y + 110 + deva_image("विजया दशमीको हार्दिक शुभकामना", 34, 0xFFFFE3B0, "SemiBold").height() / 2,
                      34, 0xFFFFE3B0, alpha=kv, weight="SemiBold")
    for (sx, sy, d) in ([(1000, 160, 0.0), (1460, 210, 0.15), (1500, 420, 0.25), (930, 430, 0.35)] if not VERT else
                        [(230, 760, 0.0), (850, 800, 0.15), (880, 1000, 0.25), (200, 1010, 0.35)]):
        kk = seg(t, 17.2 + d, 17.9 + d)
        if 0 < kk < 1:
            star(c, sx, sy, 24 * math.sin(math.pi * kk), WHITE)
    kn = ease_out_back(seg(t, 16.05, 16.6), 1.5)
    if kn > 0:
        bob = math.sin(t * 2.4) * 10
        start = (CX, H * 0.55)
        neby().draw(c, t, lerp(start[0], nx, ease_in_out(seg(t, 16.05, 16.6))), ny + bob, lerp(300, ns, kn), shadow=False)


# ------------------------------------------------------------------ Neby's path through the film

def neby_spot(t):
    """Neby's stage positions per scene, (x, y, size), for this aspect."""
    if not VERT:
        return {"hook": (960, 740, 420), "books": (1700, 860, 300), "inside": (1640, 330, 200),
                "together": (300, 700, 330)}
    return {"hook": (CX, 1290, 560), "books": (830, 250, 200), "inside": (930, 760, 180),
            "together": (CX, 1540, 440)}


def neby_main(c, t):
    if t >= 15.0:
        return
    S = neby_spot(t)

    def hop(a, b, p0, p1, h):
        k = ease_in_out(seg(t, a, b))
        return lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) - math.sin(math.pi * k) * h, lerp(p0[2], p1[2], k)

    if t < 3.0:
        k = ease_out_back(seg(t, 0.25, 0.95), 1.3)
        hx, hy, hs = S["hook"]
        x, y, s = hx, lerp(H + 300, hy, k), lerp(hs * 0.6, hs, k)
    elif t < 3.45:
        x, y, s = hop(3.0, 3.45, S["hook"], S["books"], 160)
    elif t < 6.9:
        x, y, s = S["books"]
        y += math.sin(t * 3) * 6
    elif t < 7.5:
        x, y, s = hop(6.9, 7.5, S["books"], S["inside"], 120)
    elif t < 10.4:
        x, y, s = S["inside"]
        y += math.sin(t * 3) * 5
    elif t < 10.9:
        x, y, s = hop(10.4, 10.9, S["inside"], S["together"], 220)
    elif t < 13.3:
        x, y, s = S["together"]
        y += math.sin(t * 3.2) * 8
    else:
        k = ease_in_cubic(seg(t, 13.3, 13.7))
        x, y, s = S["together"]
        x = lerp(x, -400, k) if not VERT else x
        y = y if not VERT else lerp(y, H + 500, k)
        if k >= 1:
            return
    sx = sy = 1.0
    rot = 0.0
    for a, b in ((3.0, 3.45), (6.9, 7.5), (10.4, 10.9)):
        if a <= t <= b:
            k = (t - a) / (b - a)
            st = math.sin(math.pi * k)
            sy, sx = 1 + 0.10 * st, 1 - 0.06 * st
            rot = 8 * st * (1 if a != 10.4 else -1)
        u = t - b
        if 0 < u < 0.6:
            sq = 0.12 * math.exp(-u * 9) * math.cos(u * 26)
            sx, sy = 1 + sq, 1 - sq
    if 0.95 < t < 1.6:
        u = t - 0.95
        sq = 0.10 * math.exp(-u * 8) * math.cos(u * 24)
        sx, sy = 1 + sq, 1 - sq
    neby().draw(c, t, x, y, s, rot=rot, sx=sx, sy=sy)


def frame(c, t):
    sky(c, t, kite_alpha=1.0)
    hills(c, t, rise=ease_out_cubic(seg(t, 0.0, 1.0)) * (1 - ease_in_cubic(seg(t, 2.9, 3.4))))
    garland(c, t, y0=-10, alpha=1.0 - seg(t, 15.85, 16.0))
    s1_hook(c, t)
    s2_books(c, t)
    s3_inside(c, t)
    s4_together(c, t)
    neby_main(c, t)
    s5_app(c, t)
    s6_end(c, t)
