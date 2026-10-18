"""NEBians launch film (Dashain release). Every frame is a pure function of t (seconds)."""
import math
import os
import sys

import numpy as np
import skia
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "neby"))
from characters import logo  # noqa: E402
from kit import (AMBER, BLUE, BLUE_BRIGHT, BLUE_WASH, CORAL, H, INK, MINT, MUTED,  # noqa: E402
                 NAVY, PURPLE, TEAL, W, WHITE, clamp, ease_in_cubic, ease_in_out,
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
DEVA_FONT = os.environ.get("NEBY_DEVA_FONT", os.path.expanduser(
    "~/.local/share/fonts/nebians/NotoSansDevanagari-Bold-static.ttf"))


def deva_image(s, size, color):
    """Devanagari needs real shaping (HarfBuzz via raqm); Skia's drawString cannot do it."""
    key = (s, size, color)
    if key not in _DEVA:
        f = ImageFont.truetype(DEVA_FONT, size, layout_engine=ImageFont.Layout.RAQM)
        l, t, r, b = f.getbbox(s)
        im = Image.new("RGBA", (r - l + 20, b - t + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        rgba = ((color >> 16) & 255, (color >> 8) & 255, color & 255, (color >> 24) & 255)
        d.text((10 - l, 10 - t), s, font=f, fill=rgba)
        arr = np.ascontiguousarray(np.array(im))
        _DEVA[key] = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType)
    return _DEVA[key]


def draw_deva(c, s, cx, baseline_y, size, color, alpha=1.0, scale=1.0):
    img = deva_image(s, size, color)
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

KITES = []
_r = 99
for i in range(7):
    vals = []
    for _ in range(4):
        _r = (_r * 1103515245 + 12345) & 0x7FFFFFFF
        vals.append(_r / 0x7FFFFFFF)
    KITES.append(dict(x=vals[0] * W, y=90 + vals[1] * 640, s=0.30 + vals[2] * 0.32, ph=vals[3] * 6.28,
                      col=[TIKA, MARIGOLD, BLUE_BRIGHT, MINT, PURPLE, CORAL, TEAL][i % 7]))


def kite(c, x, y, s, col, t, ph, alpha=1.0):
    sway = math.sin(t * 1.6 + ph) * 8
    c.save()
    c.translate(x, y)
    c.rotate(sway)
    c.scale(s, s)
    body = polygon([(0, -60), (44, -6), (0, 62), (-44, -6)])
    c.drawPath(body, paint(with_alpha(col, alpha)))
    c.drawPath(polygon([(0, -60), (44, -6), (0, -6)]), paint(with_alpha(mix(col, WHITE, 0.35), alpha)))
    c.drawPath(polygon([(0, -6), (-44, -6), (0, 62)]), paint(with_alpha(mix(col, NAVY, 0.15), alpha)))
    tail = skia.Path()
    tail.moveTo(0, 62)
    for k in range(1, 7):
        tail.lineTo(math.sin(t * 4 + ph + k * 0.9) * 14, 62 + k * 22)
    c.drawPath(tail, paint(with_alpha(mix(col, NAVY, 0.2), alpha * 0.8), stroke=3))
    for k in (2, 4):
        bx, by = math.sin(t * 4 + ph + k * 0.9) * 14, 62 + k * 22
        c.drawPath(polygon([(bx - 9, by - 5), (bx + 9, by - 5), (bx, by + 7)]), paint(with_alpha(col, alpha)))
    string = skia.Path()
    string.moveTo(0, 62)
    string.quadTo(60, 320, 30, 700)
    c.drawPath(string, paint(with_alpha(NAVY, 0.10 * alpha), stroke=1.4))
    c.restore()


def sky(c, t, kite_alpha=1.0):
    p = paint(WHITE)
    p.setShader(linear((0, 0), (0, H), [SKY_TOP, SKY_BOT]))
    c.drawPaint(p)
    sun = paint(with_alpha(0xFFFFF4D6, 0.85), blur=60)
    c.drawCircle(1560, 210, 150, sun)
    for i, (cx, cy, s, sp) in enumerate([(300, 230, 1.0, 9), (1250, 140, 0.8, 6), (900, 360, 0.6, 12), (1700, 420, 0.7, 8)]):
        x = (cx + t * sp) % (W + 400) - 200
        cloud = paint(with_alpha(WHITE, 0.75))
        for dx, dy, r in [(-60, 10, 48), (0, -14, 66), (64, 6, 52), (110, 22, 36), (-110, 24, 34)]:
            c.drawCircle(x + dx * s, cy + dy * s, r * s, cloud)
    if kite_alpha > 0:
        for k in KITES:
            x = (k["x"] + t * 22 * k["s"]) % (W + 240) - 120
            y = k["y"] + math.sin(t * 0.9 + k["ph"]) * 18
            kite(c, x, y, k["s"], k["col"], t, k["ph"], alpha=0.55 * kite_alpha)


def hills(c, t, rise=1.0, alpha=1.0):
    if rise <= 0:
        return
    off = (1 - rise) * 420
    layers = [(0xFFD7E8FA, 760, 0.0016, 70), (0xFFB4D2F2, 830, 0.0022, 60), (0xFF8DB8E8, 900, 0.003, 45)]
    for col, base, f, amp in layers:
        p = skia.Path()
        p.moveTo(0, H)
        for x in range(0, W + 41, 40):
            y = base + off + math.sin(x * f + base) * amp + math.sin(x * f * 2.7) * amp * 0.35
            p.lineTo(x, y)
        p.lineTo(W, H)
        p.close()
        c.drawPath(p, paint(with_alpha(col, alpha)))
    peaks = skia.Path()
    peaks.moveTo(0, 760 + off)
    for x, y in [(160, 690), (300, 610), (380, 650), (520, 560), (640, 640), (760, 600), (900, 700)]:
        peaks.lineTo(x * 1.0 + 1020, y + off)
    peaks.lineTo(W, 760 + off)
    peaks.lineTo(W, H)
    peaks.lineTo(0, H)


# ------------------------------------------------------------------ S1 hook (0–3)

def s1_hook(c, t):
    if t > 3.4:
        return
    out = ease_in_cubic(seg(t, 2.85, 3.3))
    c.save()
    c.translate(0, -out * 340)
    f = font("ExtraBold", 112)
    rise_text(c, "This Dashain,", 960, 250, f, INK, 1.05, t, align="center")
    f2 = font("ExtraBold", 112)
    w1 = f2.measureText("your ")
    w2 = font("ExtraBold", 112).measureText("books") + 2 * 0.30 * 112
    w3 = f2.measureText(" are here.")
    x0 = 960 - (w1 + w2 + w3) / 2
    rise_text(c, "your ", x0, 390, f2, INK, 1.80, t)
    chip(c, "books", x0 + w1, 390, 112, 2.30, t)
    rise_text(c, " are here.", x0 + w1 + w2, 390, f2, INK, 1.95, t)
    c.restore()


# ------------------------------------------------------------------ S2 notes & question banks (3–7)

GRADES = [("8", "Class 8", BLUE_BRIGHT), ("10", "Class 10", TIKA), ("11", "Class 11", MINT), ("12", "Class 12", PURPLE)]


def grade_book(c, x, y, w, h, num, label, col, t, k_inner):
    shadow_rrect(c, x, y, w, h, 22, alpha=0.20, dy=22, blur=28)
    p = paint(WHITE)
    p.setShader(linear((x, y), (x + w, y + h), [mix(col, WHITE, 0.10), col, mix(col, NAVY, 0.25)], [0, 0.5, 1]))
    rrect(c, x, y, w, h, 22, p)
    rrect(c, x, y, 26, h, 12, paint(with_alpha(NAVY, 0.18)))
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
    c.translate(0, -out * 300)
    f = font("ExtraBold", 92)
    rise_text(c, "Notes & question banks", 110, 200, f, INK, 3.25, t)
    ks = seg(t, 3.6, 4.0)
    if ks > 0:
        text(c, "Full books, chapter by chapter, for NEB and SEE.", 116, 268, font("Medium", 40), with_alpha(MUTED, ks))
    c.restore()
    for i, (num, label, col) in enumerate(GRADES):
        t0 = 3.70 + i * 0.45
        k = seg(t, t0 - 0.30, t0 + 0.10)
        if k <= 0:
            continue
        w, h = 300, 420
        tx = 150 + i * 345
        ty = 450 + (1 if i % 2 else 0) * 26
        e = ease_out_cubic(k)
        x = lerp(tx + 700, tx, e)
        y = lerp(ty - 650, ty, e) + math.sin(math.pi * clamp(k)) * -80
        rot = lerp(-38, -4 + i * 2.5, e)
        settle = t - (t0 + 0.10)
        sq = 0.05 * math.exp(-max(settle, 0) * 8) * math.cos(max(settle, 0) * 28) if settle > 0 else 0
        y -= out * (900 + 80 * i)
        bob = math.sin(t * 2 + i) * 6 if settle > 0 else 0
        c.save()
        c.translate(x + w / 2, y + h + bob)
        c.rotate(rot)
        c.scale(1 + sq, 1 - sq)
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
        f = font("ExtraBold", 60)
        x = 116
        text(c, lab, x, 372, f, with_alpha(BLUE, a))
        fw = f.measureText("6,000+")
        text(c, "pages", x + fw + 16, 372, font("SemiBold", 38), with_alpha(MUTED, a))
        kf = seg(t, 6.55, 6.95)
        if kf > 0:
            e = ease_out_back(kf, 2.4)
            px = x + fw + 16 + font("SemiBold", 38).measureText("pages") + 30 + 92
            c.save()
            c.translate(px, 352)
            c.scale(e, e)
            rrect(c, -92, -32, 184, 64, 32, paint(MINT))
            text(c, "All free", 0, 12, font("ExtraBold", 32), WHITE, "center")
            c.restore()


# ------------------------------------------------------------------ S3 inside a book (7–10.5)

SUBJECTS = [("Physics", BLUE_BRIGHT), ("Chemistry", MINT), ("Biology", CORAL), ("Mathematics", PURPLE),
            ("नेपाली", TIKA), ("English", TEAL), ("सामाजिक", MARIGOLD), ("Accountancy", BLUE),
            ("Computer Science", NAVY), ("Science", MINT), ("Economics", CORAL), ("Health", TEAL)]


def s3_inside(c, t):
    if t < 6.9 or t > 10.8:
        return
    k_in = ease_out_back(seg(t, 7.0, 7.45), 1.2)
    k_out = ease_in_cubic(seg(t, 10.35, 10.75))
    alpha = clamp(seg(t, 7.0, 7.2)) * (1 - k_out)
    cx, cy, bw, bh = 960, 590, 1180, 540
    c.save()
    c.translate(cx, cy + k_out * 160)
    s = lerp(0.55, 1.0, k_in) * (1 - 0.35 * k_out)
    c.scale(s, s)
    c.saveLayerAlpha(None, int(255 * alpha))
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
    for j, tf in enumerate([7.2, 7.55]):
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
    if t > 7.9:
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
        rx = 80
        base = -40
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
    c.restore()
    c.restore()
    up = k_out * 220
    f = font("ExtraBold", 88)
    k1 = seg(t, 7.9, 8.3)
    k1o = ease_in_cubic(seg(t, 9.05, 9.3))
    if k1 > 0 and k1o < 1:
        e = ease_out_back(k1, 1.8)
        c.save()
        c.translate(960, 190 - k1o * 150)
        c.scale(e, e)
        text(c, "Every chapter.", 0, 0, f, with_alpha(INK, 1 - k1o), "center")
        c.restore()
    k2 = seg(t, 9.3, 9.7)
    if k2 > 0:
        e = ease_out_back(k2, 1.8)
        c.save()
        c.translate(960, 190 - up)
        c.scale(e, e)
        w1 = f.measureText("Every answer ")
        w2 = f.measureText("worked out.")
        text(c, "Every answer ", -(w1 + w2) / 2, 0, f, INK)
        text(c, "worked out.", -(w1 + w2) / 2 + w1, 0, f, BLUE_BRIGHT)
        c.restore()
    fw = font("Bold", 31)

    def chip_w(sname):
        deva = any("\u0900" <= ch <= "\u097f" for ch in sname)
        return (deva_image(sname, 31, WHITE).width() - 20 if deva else fw.measureText(sname)) + 48, deva

    for row in range(2):
        items = SUBJECTS[row * 6:(row + 1) * 6]
        widths = [chip_w(n)[0] for n, _ in items]
        total = sum(widths) + 26 * (len(items) - 1)
        x = 960 - total / 2
        for j, (sname, col) in enumerate(items):
            pw, deva = chip_w(sname)
            t0 = 9.6 + j * 0.12 + row * 0.06
            k = seg(t, t0, t0 + 0.5)
            cxp = x + pw / 2
            x += pw + 26
            if k <= 0:
                continue
            e = ease_out_back(k, 2.2)
            y = 948 + row * 76 + (1 - e) * 120 + k_out * 300
            c.save()
            c.translate(cxp, y)
            c.scale(e, e)
            shadow_rrect(c, -pw / 2, -32, pw, 64, 32, alpha=0.14, dy=8, blur=12)
            rrect(c, -pw / 2, -32, pw, 64, 32, paint(col))
            if deva:
                draw_deva(c, sname, 0, 20, 31, WHITE)
            else:
                text(c, sname, 0, 12, fw, WHITE, "center")
            c.restore()


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
    f = font("ExtraBold", 96)
    c.save()
    c.translate(0, -out * 320)
    w = rise_text(c, "Ask.", 110, 230, f, INK, 10.80, t)
    w2 = rise_text(c, "Answer.", 110 + w + 30, 230, f, INK, 10.95, t)
    chip(c, "Study together.", 110 + w + w2 + 60, 230, 96, 11.15, t, fg=0xFFB84B0B, bg=0xFFFFEFCF)
    c.restore()
    for i, (name, ini, col, msg, t0, likes) in enumerate(THREAD):
        k = seg(t, t0, t0 + 0.45)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.6)
        bw, bh = 980, 128
        x = 560 + (90 if i == 1 else 0)
        y = 380 + i * 158 + (1 - e) * 60 + out * 900
        c.save()
        c.translate(x, y)
        c.scale(lerp(0.8, 1.0, e), lerp(0.8, 1.0, e))
        a = clamp(k * 3)
        shadow_rrect(c, 0, 0, bw, bh, 30, alpha=0.14 * a, dy=14, blur=20)
        rrect(c, 0, 0, bw, bh, 30, paint(with_alpha(WHITE, a)))
        c.drawCircle(68, bh / 2, 40, paint(with_alpha(col, a)))
        text(c, ini, 68, bh / 2 + 15, font("ExtraBold", 40), with_alpha(WHITE, a), "center")
        text(c, name, 130, 52, font("Bold", 30), with_alpha(INK, a))
        n_chars = int(len(msg) * clamp(seg(t, t0 + 0.15, t0 + 0.7)))
        text(c, msg[:n_chars], 130, 96, font("Medium", 32), with_alpha(MUTED, a))
        if likes:
            kl = seg(t, 12.55 + (0.2 if i == 2 else 0), 12.85 + (0.2 if i == 2 else 0))
            if kl > 0:
                el = ease_out_back(kl, 3)
                c.save()
                c.translate(bw - 90, bh / 2)
                c.scale(el, el)
                rrect(c, -56, -28, 112, 56, 28, paint(BLUE_WASH))
                c.drawPath(polygon([(-34, 8), (-34, -6), (-24, -6), (-14, -22), (-8, -18), (-12, -6), (0, -6), (-4, 12), (-34, 12)]), paint(BLUE))
                text(c, likes, 22, 11, font("Bold", 30), BLUE, "center")
                c.restore()
        c.restore()


# ------------------------------------------------------------------ S5 Android app (13.5–16)

def phone(c, x, y, w, h, t, k_sheet, k_tap):
    shadow_rrect(c, x, y, w, h, 64, alpha=0.28, dy=34, blur=40)
    rrect(c, x, y, w, h, 64, paint(0xFF101828))
    sx, sy, sw, sh = x + 18, y + 18, w - 36, h - 36
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx, sy, sw, sh), 48, 48), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(sx, sy, sw, sh), paint(0xFFF2F4F8))
    rrect(c, sx + 60, sy + 60, sw - 120, sh - 120, 10, paint(WHITE))
    text(c, "Physics · Chapter 4", sx + 90, sy + 120, font("Bold", 28), BLUE_BRIGHT)
    for i in range(12):
        L = (sw - 200) * (0.95 if i % 4 else 0.6)
        c.drawLine(sx + 90, sy + 170 + i * 44, sx + 90 + L, sy + 170 + i * 44, paint(mix(BLUE_WASH, MUTED, 0.3), stroke=10))
    rrect(c, sx + 90, sy + 330, sw - 180, 140, 14, paint(mix(AMBER, WHITE, 0.85)))
    fx, fy = sx + sw - 210, sy + sh - 150
    pulse = 1 + 0.06 * math.sin(t * 8) * (1 - k_tap)
    c.save()
    c.translate(fx + 80, fy + 36)
    c.scale(pulse * (1 - 0.1 * math.sin(math.pi * k_tap)), pulse * (1 - 0.1 * math.sin(math.pi * k_tap)))
    rrect(c, -100, -38, 200, 76, 38, paint(BLUE_BRIGHT))
    star(c, -68, 0, 15, WHITE)
    text(c, "Ask Neby", 22, 11, font("Bold", 30), WHITE, "center")
    c.restore()
    if 0 < k_tap < 1:
        c.drawCircle(fx + 80, fy + 36, 30 + 140 * k_tap, paint(with_alpha(BLUE_BRIGHT, 0.35 * (1 - k_tap))))
    if k_sheet > 0:
        e = ease_out_cubic(k_sheet)
        top = sy + sh - 560 * e
        c.drawRect(skia.Rect.MakeXYWH(sx, sy, sw, sh), paint(with_alpha(NAVY, 0.25 * e)))
        rrect(c, sx, top, sw, 620, 40, paint(WHITE))
        rrect(c, sx + sw / 2 - 40, top + 16, 80, 8, 4, paint(mix(BLUE_WASH, MUTED, 0.3)))
        text(c, "Ask Neby", sx + 170, top + 92, font("Bold", 34), INK)
        text(c, "about this page", sx + 170, top + 132, font("Medium", 26), MUTED)
        rrect(c, sx + sw - 380, top + 170, 330, 66, 33, paint(BLUE_BRIGHT))
        text(c, "Explain Newton's 2nd law", sx + sw - 215, top + 212, font("SemiBold", 22), WHITE, "center")
        kt = seg(t, 15.0, 15.8)
        for i in range(4):
            kk = clamp(kt * 2.2 - i * 0.35)
            if kk > 0:
                rrect(c, sx + 50, top + 270 + i * 46, (sw - 140) * (0.9 if i < 3 else 0.5) * kk, 18, 9, paint(mix(BLUE_WASH, MUTED, 0.25)))
    c.restore()
    return (sx, sy, sw, sh)


def s5_app(c, t):
    if t < 13.3 or t > 16.2:
        return
    k_in = ease_out_cubic(seg(t, 13.4, 13.95))
    k_out = ease_in_cubic(seg(t, 15.75, 16.05))
    f = font("ExtraBold", 96)
    c.save()
    c.translate(-k_out * 900, 0)
    rise_text(c, "Read anywhere.", 120, 380, f, INK, 13.70, t)
    ks = seg(t, 14.0, 14.4)
    if ks > 0:
        text(c, "Every book in the Android app.", 126, 460, font("SemiBold", 42), with_alpha(MUTED, ks))
        text(c, "Stuck on a line? Ask Neby, right in the PDF reader.", 126, 520, font("Medium", 36), with_alpha(MUTED, ks))
    kg = seg(t, 14.4, 14.8)
    if kg > 0:
        e = ease_out_back(kg, 2)
        c.save()
        c.translate(126 + 170, 610)
        c.scale(e, e)
        rrect(c, -170, -38, 340, 76, 38, paint(INK))
        c.drawPath(polygon([(-130, -20), (-130, 20), (-96, 0)]), paint(MINT))
        text(c, "Google Play", 20, 12, font("Bold", 32), WHITE, "center")
        c.restore()
    c.restore()
    w, h = 520, 1000
    x = 1180
    y = lerp(1180, 150, k_in) + k_out * 1100
    tilt = (1 - k_in) * 10
    c.save()
    c.rotate(tilt, x + w / 2, y + h / 2)
    k_tap = seg(t, 14.55, 14.85)
    k_sheet = seg(t, 14.75, 15.15)
    sx, sy, sw, sh = phone(c, x, y, w, h, t, k_sheet, k_tap)
    if k_sheet > 0:
        top = sy + sh - 560 * ease_out_cubic(k_sheet)
        neby().draw(c, t, sx + 95, top + 108, 120, shadow=False)
    c.restore()


# ------------------------------------------------------------------ S6 end card (16–20)

def s6_end(c, t):
    if t < 15.7:
        return
    k = ease_in_out(seg(t, 15.75, 16.15))
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(960, 520), 1500, [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
    c.drawCircle(1220, 560, 2400 * k, p)
    if t < 16.0:
        return
    for i, kk in enumerate(KITES[:6]):
        x = (kk["x"] * 0.9 + t * 30 * kk["s"]) % (W + 240) - 120
        y = 140 + (i * 157) % 760 + math.sin(t + kk["ph"]) * 16
        kite(c, x, y, kk["s"] * 0.55, mix(kk["col"], WHITE, 0.15), t, kk["ph"], alpha=0.22)
    for j in range(40):
        a = j * 2.399
        kk = seg(t, 16.1 + (j % 7) * 0.03, 17.6 + (j % 5) * 0.1)
        if 0 < kk < 1:
            r = 140 + 900 * ease_out_expo(kk)
            px = 1220 + math.cos(a) * r
            py = 470 + math.sin(a) * r * 0.7 + 200 * kk * kk
            col = [MARIGOLD, TIKA, WHITE, MINT, 0xFF9CC3FF][j % 5]
            c.save()
            c.translate(px, py)
            c.rotate(j * 37 + t * 300)
            rrect(c, -7, -3, 14, 6, 3, paint(with_alpha(col, 1 - kk)))
            c.restore()
    lx = 1220
    float_y = math.sin(t * 2.0) * 5
    kt0 = seg(t, 16.35, 16.75)
    if kt0 > 0:
        e = ease_out_back(kt0, 1.7)
        c.save()
        c.translate(lx, 300 + float_y)
        c.rotate((1 - e) * -14)
        c.scale(e, e)
        rrect(c, -130, -130 + 18, 260, 260, 64, paint(with_alpha(0xFF001A66, 0.35), blur=26))
        rrect(c, -130, -130, 260, 260, 64, paint(WHITE))
        c.restore()
    logo(c, lx - 5, 300 + float_y, 180, seg(t, 16.5, 17.3) * 1.25, t, on_blue=False)
    rise_text(c, "NEBians", lx, 560, font("ExtraBold", 136), WHITE, 17.15, t, align="center", stagger=0.04)
    kt = seg(t, 17.5, 17.9)
    if kt > 0:
        text(c, "Notes & question banks · Class 8, 10, 11, 12", lx, 630 + (1 - ease_out_cubic(kt)) * 20,
             font("SemiBold", 38), with_alpha(0xFFDCE6FF, kt), "center")
    ku = seg(t, 17.7, 18.1)
    if ku > 0:
        e = ease_out_back(ku, 1.8)
        fu = font("Bold", 42)
        url = "nebians.consica.com.np"
        uw = fu.measureText(url) + 80
        c.save()
        c.translate(lx, 730)
        c.scale(e, e)
        rrect(c, -uw / 2, -42, uw, 84, 42, paint(WHITE))
        text(c, url, 0, 15, fu, BLUE, "center")
        c.restore()
    ks = seg(t, 18.05, 18.45)
    if ks > 0:
        text(c, "Free on the web  ·  Android app on Google Play", lx, 830, font("Medium", 32),
             with_alpha(0xFFC9D8FF, ks), "center")
    kd = seg(t, 18.4, 18.9)
    if kd > 0:
        e = ease_out_back(kd, 2.2)
        c.save()
        c.translate(lx, 940)
        c.scale(e, e)
        rrect(c, -230, -50, 460, 100, 50, paint(TIKA))
        c.drawCircle(-182, 0, 13, paint(MARIGOLD))
        c.drawCircle(182, 0, 13, paint(MARIGOLD))
        c.restore()
        gh = deva_image("शुभ दशैँ", 56, WHITE).height()
        draw_deva(c, "शुभ दशैँ", lx, 940 + gh / 2 + 4, 56, WHITE, alpha=clamp(kd * 2), scale=e)
    for j, (sx, sy, d) in enumerate([(1000, 160, 0.0), (1460, 210, 0.15), (1500, 420, 0.25), (930, 430, 0.35)]):
        kk = seg(t, 17.2 + d, 17.9 + d)
        if 0 < kk < 1:
            star(c, sx, sy, 24 * math.sin(math.pi * kk), WHITE)
    kn = ease_out_back(seg(t, 16.05, 16.6), 1.5)
    if kn > 0:
        bob = math.sin(t * 2.4) * 10
        neby().draw(c, t, lerp(960, 470, ease_in_out(seg(t, 16.05, 16.6))), 560 + bob, lerp(300, 520, kn), shadow=False)


# ------------------------------------------------------------------ Neby's path through the film

def neby_main(c, t):
    if t >= 16.05:
        return
    if t < 3.0:
        k = ease_out_back(seg(t, 0.25, 0.95), 1.3)
        x, y, s = 960, lerp(1250, 740, k), lerp(260, 420, k)
        if t > 2.85:
            pass
    elif t < 3.45:
        k = ease_in_out(seg(t, 3.0, 3.45))
        x, y, s = lerp(960, 1700, k), lerp(740, 860, k), lerp(420, 300, k)
        y -= math.sin(math.pi * k) * 160
    elif t < 6.9:
        x, y, s = 1700, 860, 300
        y += math.sin(t * 3) * 6
    elif t < 7.5:
        k = ease_in_out(seg(t, 6.9, 7.5))
        x, y, s = lerp(1700, 1640, k), lerp(860, 330, k), lerp(300, 200, k)
        y -= math.sin(math.pi * k) * 120
    elif t < 10.4:
        x, y, s = 1640, 330, 200
        y += math.sin(t * 3) * 5
    elif t < 10.9:
        k = ease_in_out(seg(t, 10.4, 10.9))
        x, y, s = lerp(1640, 300, k), lerp(330, 700, k), lerp(200, 330, k)
        y -= math.sin(math.pi * k) * 220
    elif t < 13.3:
        x, y, s = 300, 700, 330
        y += math.sin(t * 3.2) * 8
    else:
        k = ease_in_cubic(seg(t, 13.3, 13.7))
        x, y, s = lerp(300, -300, k), 700, 330
        if k >= 1:
            return
    if t > 15.0:
        return
    sx = sy = 1.0
    rot = 0.0
    for a, b in ((3.0, 3.45), (6.9, 7.5), (10.4, 10.9)):
        if a <= t <= b:
            k = (t - a) / (b - a)
            st = math.sin(math.pi * k)
            sy, sx = 1 + 0.10 * st, 1 - 0.06 * st
            rot = 8 * math.sin(math.pi * k) * (1 if a != 10.4 else -1)
        u = t - b
        if 0 < u < 0.6:
            sq = 0.12 * math.exp(-u * 9) * math.cos(u * 26)
            sx, sy = 1 + sq, 1 - sq
    if t < 1.2:
        u = t - 0.95
        if u > 0:
            sq = 0.10 * math.exp(-u * 8) * math.cos(u * 24)
            sx, sy = 1 + sq, 1 - sq
    neby().draw(c, t, x, y, s, rot=rot, sx=sx, sy=sy)


def frame(c, t):
    sky(c, t, kite_alpha=1.0)
    hills(c, t, rise=ease_out_cubic(seg(t, 0.0, 1.0)) * (1 - ease_in_cubic(seg(t, 2.9, 3.4))))
    s1_hook(c, t)
    s2_books(c, t)
    s3_inside(c, t)
    s4_together(c, t)
    neby_main(c, t)
    s5_app(c, t)
    s6_end(c, t)
