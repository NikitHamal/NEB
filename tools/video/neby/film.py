"""NEBians launch film, starring Neby. Every frame is a pure function of t (seconds)."""
import math

import skia

from characters import blobatar, logo, neby
from kit import (AMBER, BLUE, BLUE_BRIGHT, BLUE_WASH, CORAL, H, INK, MINT, MUTED,
                 NAVY, PAPER, PINK, PURPLE, SKY, TEAL, W, WHITE, clamp, ease_in_cubic,
                 ease_in_out, ease_out_back, ease_out_cubic, ease_out_expo, font, lerp,
                 linear, mix, paint, partial_path, polygon, rrect, seg, shadow_rrect,
                 spring, text, with_alpha)

DURATION = 18.0
FPS = 60
BPM = 120

# Every cue drives a sound in score.py; the picture uses the same times.
CUES = [
    (0.05, "whoosh_down"), (0.62, "thud"), (0.70, "boing"), (1.15, "pop"), (1.30, "bubble"),
    (2.00, "kick_in"),
    (2.25, "swish"), (2.50, "swish"), (2.75, "swish"), (3.00, "swish"),
    (2.10, "type"), (4.70, "whoosh_up"),
    (5.05, "tock"), (5.20, "tock"), (5.35, "tock"), (5.50, "tock"), (5.65, "tock"), (5.80, "tock"),
    (5.25, "hop"), (5.70, "land"), (5.85, "count"), (6.45, "cap"), (6.50, "sparkle"), (7.30, "pop"),
    (8.20, "whoosh_up"),
    (8.55, "page"), (9.00, "word"), (9.50, "word"), (10.00, "word"),
    (10.05, "tick"), (10.20, "tick"), (10.35, "tick"),
    (11.20, "whoosh_up"),
    (11.65, "pop"), (11.80, "pop"), (11.95, "pop"), (12.10, "pop"), (12.25, "pop"), (12.40, "pop"),
    (12.00, "word"), (12.80, "bubble"), (13.20, "bubble"),
    (13.90, "riser"),
    (14.50, "whoosh_up"), (15.00, "boom"), (15.00, "facet"), (15.12, "facet"), (15.24, "facet"), (15.36, "facet"),
    (15.55, "type"), (15.95, "sparkle"), (16.20, "hop"), (16.45, "pop"), (17.05, "wink"),
    (15.00, "chord"),
]

CONFETTI = []
_r = 7
for i in range(26):
    _r = (_r * 1103515245 + 12345) & 0x7FFFFFFF
    a = _r / 0x7FFFFFFF
    _r = (_r * 1103515245 + 12345) & 0x7FFFFFFF
    b = _r / 0x7FFFFFFF
    _r = (_r * 1103515245 + 12345) & 0x7FFFFFFF
    d = _r / 0x7FFFFFFF
    CONFETTI.append((a * W, b * H, 0.4 + d * 0.9, i % 4, [BLUE_BRIGHT, AMBER, CORAL, MINT, PURPLE][i % 5], d))


def background(c, t, energy=1.0):
    c.clear(PAPER)
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.42), W * 0.75,
                                                [0xFFFFFFFF, 0xFFF1F5FF, 0xFFE6EEFF], [0, 0.6, 1]))
    c.drawPaint(p)
    for x, y, s, kind, col, d in CONFETTI:
        drift = t * (14 + d * 22)
        px = (x + math.sin(t * 0.6 + d * 9) * 18) % W
        py = (y - drift) % (H + 80) - 40
        a = 0.16 * energy
        size = 9 * s
        c.save()
        c.translate(px, py)
        c.rotate(t * 40 * (d - 0.5))
        if kind == 0:
            c.drawCircle(0, 0, size, paint(with_alpha(col, a)))
        elif kind == 1:
            rrect(c, -size, -size, 2 * size, 2 * size, size * 0.45, paint(with_alpha(col, a)))
        elif kind == 2:
            q = paint(with_alpha(col, a), stroke=size * 0.45)
            c.drawLine(-size, 0, size, 0, q)
            c.drawLine(0, -size, 0, size, q)
        else:
            c.drawCircle(0, 0, size, paint(with_alpha(col, a), stroke=size * 0.35))
        c.restore()


def bubble(c, x, y, s, k, color=WHITE, ink=INK, big=1.0):
    """A round speech bubble with a single glyph, popping in with k in 0..1."""
    if k <= 0:
        return
    e = ease_out_back(clamp(k), 2.2)
    r = 46 * big
    c.save()
    c.translate(x, y)
    c.scale(e, e)
    c.drawCircle(0, 8, r, paint(with_alpha(NAVY, 0.15), blur=12))
    tail = polygon([(-r * 0.55, r * 0.55), (-r * 0.95, r * 1.05), (-r * 0.05, r * 0.82)])
    c.drawPath(tail, paint(color))
    c.drawCircle(0, 0, r, paint(color))
    text(c, s, 0, r * 0.36, font("ExtraBold", r * 1.05), ink, "center")
    c.restore()


def rising_word(c, s, x, y, f, color, t0, t, align="left", stagger=0.03, dur=0.42):
    """Letters rise from a mask line with a small overshoot."""
    total = f.measureText(s)
    if align == "center":
        x -= total / 2
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x - 40, y - f.getSize() * 1.25, total + 80, f.getSize() * 1.55))
    pos = x
    for i, ch in enumerate(s):
        k = seg(t, t0 + i * stagger, t0 + i * stagger + dur)
        dy = (1 - ease_out_back(k, 1.6)) * f.getSize() * 1.1
        if k > 0:
            c.drawString(ch, pos, y + dy, f, paint(color))
        pos += f.measureText(ch)
    c.restore()
    return total


def chip_word(c, s, x, y, size, t0, t, fg=BLUE, bg=BLUE_WASH):
    f = font("ExtraBold", size)
    w = f.measureText(s)
    k = ease_out_back(seg(t, t0, t0 + 0.45), 1.8)
    padx, h = size * 0.28, size * 1.18
    cw = (w + 2 * padx) * clamp(k, 0, 1.2)
    rrect(c, x, y - size * 0.95, cw, h, h * 0.32, paint(bg))
    if k > 0.25:
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(x, y - size * 1.2, cw, size * 1.6))
        c.drawString(s, x + padx, y, f, paint(fg))
        c.restore()
    return w + 2 * padx


# ------------------------------------------------------------------ scene A: hello

def neby_track(t):
    """Where Neby stands, its size and its squash for the whole film."""
    if t < 0.62:
        k = ease_in_cubic(seg(t, 0.0, 0.62))
        return dict(x=960, by=760, r=120, lift=lerp(900, 0, k), sq=-0.22 * k)
    if t < 2.05:
        u = t - 0.62
        sq = 0.30 * math.exp(-u * 6) * math.cos(u * 26)
        lift = max(0.0, 160 * math.sin(math.pi * seg(u, 0.05, 0.50))) if u < 0.5 else 0.0
        return dict(x=960, by=760, r=120, lift=lift, sq=sq if lift == 0 else -0.08)
    if t < 2.45:
        k = ease_in_out(seg(t, 2.05, 2.45))
        return dict(x=lerp(960, 640, k), by=lerp(760, 830, k), r=lerp(120, 110, k),
                    lift=140 * math.sin(math.pi * k), sq=-0.10 * math.sin(math.pi * k))
    if t < 5.25:
        u = t - 2.45
        return dict(x=640, by=830, r=110, lift=0, sq=0.18 * math.exp(-u * 7) * math.cos(u * 24))
    if t < 5.70:
        k = seg(t, 5.25, 5.70)
        return dict(x=lerp(640, BOOK3[0], ease_in_out(k)), by=lerp(830, BOOK3[1], ease_out_cubic(k)), r=lerp(110, 84, k),
                    lift=170 * math.sin(math.pi * k), sq=-0.12 * math.sin(math.pi * k))
    if t < 8.25:
        u = t - 5.70
        return dict(x=BOOK3[0], by=BOOK3[1], r=84, lift=0, sq=0.24 * math.exp(-u * 7) * math.cos(u * 26))
    if t < 8.75:
        k = ease_in_out(seg(t, 8.25, 8.75))
        return dict(x=lerp(BOOK3[0], 1560, k), by=lerp(BOOK3[1], 1000, k), r=84,
                    lift=120 * math.sin(math.pi * k), sq=0)
    if t < 11.25:
        return dict(x=1560, by=1000, r=84, lift=0, sq=0.02 * math.sin(t * 4))
    if t < 11.75:
        k = ease_in_out(seg(t, 11.25, 11.75))
        return dict(x=lerp(1560, 960, k), by=lerp(1000, 720, k), r=lerp(84, 112, k),
                    lift=200 * math.sin(math.pi * k), sq=-0.1 * math.sin(math.pi * k))
    u = t - 11.75
    hop = 0.0
    if 14.15 < t < 14.5:
        hop = 70 * math.sin(math.pi * seg(t, 14.15, 14.5))
    return dict(x=960, by=720, r=112, lift=hop, sq=0.2 * math.exp(-u * 7) * math.cos(u * 24))


def draw_neby(c, t, alpha=1.0):
    s = neby_track(t)
    look = (0.0, 0.0)
    if 1.6 < t < 2.0:
        look = (math.sin((t - 1.6) * 12) * 0.8, 0)
    elif 2.2 < t < 4.6:
        look = (1.0, -0.4)
    elif 5.0 < t < 5.6:
        look = (1.0, -0.6)
    elif 5.8 < t < 8.2:
        look = (-1.0, 0.3)
    elif 8.8 < t < 11.2:
        look = (-1.0, -0.6)
    elif 12.6 < t < 13.1:
        look = (-0.9, -0.5)
    blink = 1.0 if (1.85 < t < 1.95 or 4.1 < t < 4.2 or 7.6 < t < 7.7 or 10.6 < t < 10.7 or 13.5 < t < 13.6) else 0.0
    eyes = clamp((t - 1.0) / 0.15)
    blink = max(blink, 1 - eyes)
    cap = ease_out_back(seg(t, 6.45, 6.75), 2.0) if t >= 6.45 else 0.0
    smile = 1.0 if t > 1.1 else 0.3
    neby(c, s["x"], s["by"], s["r"], t, sq=s["sq"], look=look, blink=blink, smile=smile,
         cap=cap, lift=s["lift"], alpha=alpha)
    return s


def scene_hello(c, t):
    k = seg(t, 1.30, 1.75)
    if 1.30 < t < 2.15:
        out = 1 - seg(t, 1.95, 2.15)
        bubble_pill(c, 1110, 520, "Hi, I'm Neby!", k * out)


def bubble_pill(c, x, y, s, k):
    if k <= 0:
        return
    e = ease_out_back(clamp(k), 2.0)
    f = font("Bold", 46)
    w = f.measureText(s) + 70
    c.save()
    c.translate(x, y)
    c.scale(e, e)
    shadow_rrect(c, -20, -50, w, 96, 48, alpha=0.14, dy=10, blur=16)
    c.drawPath(polygon([(4, 30), (-34, 78), (52, 40)]), paint(WHITE))
    rrect(c, -20, -50, w, 96, 48, paint(WHITE))
    text(c, s, 15, 16, f, INK)
    c.restore()


# ------------------------------------------------------------------ scene B: materials

CARDS = [
    ("Notes", BLUE_BRIGHT, "lines"),
    ("Diagrams", PURPLE, "chart"),
    ("Solutions", MINT, "check"),
    ("Model papers", CORAL, "paper"),
]


def card_glyph(c, kind, x, y, w, h, color, k):
    p = paint(with_alpha(color, 0.9), stroke=7)
    q = paint(with_alpha(mix(color, WHITE, 0.6), 1))
    if kind == "lines":
        for i in range(5):
            L = (w - 40) * (0.95 if i % 2 == 0 else 0.7) * clamp(k * 1.6 - i * 0.15)
            if L > 0:
                c.drawLine(x + 20, y + 22 + i * 30, x + 20 + L, y + 22 + i * 30, paint(mix(color, WHITE, 0.55), stroke=10))
    elif kind == "chart":
        for i, v in enumerate([0.45, 0.8, 0.6, 1.0]):
            bh = (h - 40) * v * clamp(k * 1.5 - i * 0.12)
            rrect(c, x + 22 + i * (w - 44) / 4, y + h - 14 - bh, (w - 44) / 4 - 14, bh, 6, q if i != 3 else paint(color))
    elif kind == "check":
        path = skia.Path()
        path.moveTo(x + w * 0.22, y + h * 0.52)
        path.lineTo(x + w * 0.42, y + h * 0.74)
        path.lineTo(x + w * 0.80, y + h * 0.24)
        c.drawCircle(x + w / 2, y + h / 2, h * 0.46, paint(mix(color, WHITE, 0.8)))
        c.drawPath(partial_path(path, clamp(k * 1.4)), paint(color, stroke=16))
    else:
        for i in range(3):
            c.drawCircle(x + 34, y + 30 + i * 46, 11, paint(color) if i == 1 else paint(mix(color, WHITE, 0.6)))
            c.drawLine(x + 62, y + 30 + i * 46, x + w - 24, y + 30 + i * 46, paint(mix(color, WHITE, 0.6), stroke=9))


def scene_materials(c, t):
    if t < 2.0 or t > 5.1:
        return
    out = ease_in_cubic(seg(t, 4.70, 5.05))
    c.save()
    c.translate(0, -out * 380)
    f = font("ExtraBold", 132)
    w = rising_word(c, "Study", 150, 300, f, INK, 2.08, t)
    chip_word(c, "materials.", 150 + w + 34, 300, 132, 2.40, t)
    sub = font("Medium", 42)
    k = seg(t, 2.9, 3.3)
    if k > 0:
        text(c, "Written for the NEB and SEE syllabus.", 156, 390 + (1 - ease_out_cubic(k)) * 30, sub, with_alpha(MUTED, k))
    c.restore()

    for i, (label, color, kind) in enumerate(CARDS):
        t0 = 2.25 + i * 0.25
        k = seg(t, t0, t0 + 0.55)
        if k <= 0:
            continue
        e = ease_out_back(k, 1.5)
        ang = -15 + i * 10
        px = 1010 + i * 262
        py = 640 + abs(i - 1.5) * 34
        sx, sy = 640, 690
        x = lerp(sx, px, e)
        y = lerp(sy, py, ease_out_cubic(k)) - math.sin(math.pi * clamp(k)) * 120
        rot = lerp(-90 + i * 30, ang, e)
        y -= out * (700 + i * 60)
        x += out * (i - 1.5) * 120
        bob = math.sin(t * 2.2 + i) * 6
        c.save()
        c.translate(x, y + bob)
        c.rotate(rot)
        s = lerp(0.3, 1.08, ease_out_cubic(clamp(k * 1.4)))
        c.scale(s, s)
        cw, ch = 260, 330
        shadow_rrect(c, -cw / 2, -ch / 2, cw, ch, 26, alpha=0.18)
        rrect(c, -cw / 2, -ch / 2, cw, ch, 26, paint(WHITE))
        rrect(c, -cw / 2 + 18, -ch / 2 + 18, cw - 36, 170, 18, paint(mix(color, WHITE, 0.88)))
        card_glyph(c, kind, -cw / 2 + 18, -ch / 2 + 18, cw - 36, 170, color, seg(t, t0 + 0.2, t0 + 0.9))
        text(c, label, -cw / 2 + 24, ch / 2 - 70, font("Bold", 34 if len(label) < 10 else 30), INK)
        c.drawLine(-cw / 2 + 24, ch / 2 - 42, -cw / 2 + 24 + 120, ch / 2 - 42, paint(mix(color, WHITE, 0.5), stroke=8))
        c.restore()


# ------------------------------------------------------------------ scene C: full books

BOOKS = [
    (130, 410, BLUE_BRIGHT, "atom"), (112, 360, AMBER, "pi"), (124, 452, MINT, "leaf"),
    (104, 330, PURPLE, "Aa"), (128, 400, CORAL, "globe"), (110, 372, TEAL, "flask"),
]
SHELF_Y = 860
BOOK3 = (820 + 130 + 14 + 112 + 14 + 62, SHELF_Y - 452)


def book_icon(c, kind, cx, cy, s):
    w = paint(WHITE, stroke=s * 0.12)
    if kind == "atom":
        for a in (0, 60, 120):
            c.save()
            c.rotate(a, cx, cy)
            c.drawOval(skia.Rect.MakeXYWH(cx - s * 0.5, cy - s * 0.2, s, s * 0.4), w)
            c.restore()
        c.drawCircle(cx, cy, s * 0.09, paint(WHITE))
    elif kind == "pi":
        text(c, "π", cx, cy + s * 0.32, font("Bold", s * 0.95), WHITE, "center")
    elif kind == "Aa":
        text(c, "Aa", cx, cy + s * 0.25, font("Bold", s * 0.7), WHITE, "center")
    elif kind == "leaf":
        p = skia.Path()
        p.moveTo(cx - s * 0.4, cy + s * 0.4)
        p.cubicTo(cx - s * 0.4, cy - s * 0.3, cx + s * 0.2, cy - s * 0.5, cx + s * 0.45, cy - s * 0.45)
        p.cubicTo(cx + s * 0.45, cy + s * 0.1, cx + s * 0.1, cy + s * 0.45, cx - s * 0.4, cy + s * 0.4)
        c.drawPath(p, w)
        c.drawLine(cx - s * 0.4, cy + s * 0.4, cx + s * 0.15, cy - s * 0.15, w)
    elif kind == "globe":
        c.drawCircle(cx, cy, s * 0.45, w)
        c.drawOval(skia.Rect.MakeXYWH(cx - s * 0.2, cy - s * 0.45, s * 0.4, s * 0.9), w)
        c.drawLine(cx - s * 0.45, cy, cx + s * 0.45, cy, w)
    else:
        p = polygon([(cx - s * 0.15, cy - s * 0.45), (cx + s * 0.15, cy - s * 0.45), (cx + s * 0.15, cy - s * 0.1),
                     (cx + s * 0.42, cy + s * 0.42), (cx - s * 0.42, cy + s * 0.42), (cx - s * 0.15, cy - s * 0.1)])
        c.drawPath(p, w)


def book_top(i):
    x = 820
    for j in range(i):
        x += BOOKS[j][0] + 14
    w, h, _, _ = BOOKS[i]
    return x, SHELF_Y - h, w, h


def scene_books(c, t):
    if t < 4.9 or t > 8.6:
        return
    fade = 1 - seg(t, 8.25, 8.55)
    c.saveLayerAlpha(None, int(255 * fade))
    drop = ease_in_cubic(seg(t, 8.2, 8.55))
    k = seg(t, 4.95, 5.4)
    sw = 960 * ease_out_expo(k)
    rrect(c, 790 - 20, SHELF_Y, sw + 40, 18, 9, paint(mix(BLUE_WASH, NAVY, 0.10)))
    for i, (w, h, color, icon) in enumerate(BOOKS):
        x, top, _, _ = book_top(i)
        t0 = 5.05 + i * 0.15
        kk = seg(t, t0 - 0.25, t0)
        if kk <= 0:
            continue
        settle = t - t0
        y = top - (1 - ease_in_cubic(kk)) * 900 + drop * (300 + i * 40)
        sq = 0.06 * math.exp(-max(settle, 0) * 9) * math.cos(max(settle, 0) * 30) if settle > 0 else 0
        c.save()
        c.translate(x + w / 2, SHELF_Y)
        c.scale(1 + sq, 1 - sq)
        c.translate(-(x + w / 2), -SHELF_Y)
        rrect(c, x + 6, y + 10, w, h, 16, paint(with_alpha(NAVY, 0.12), blur=10))
        p = paint(WHITE)
        p.setShader(linear((x, y), (x + w, y), [mix(color, WHITE, 0.12), color, mix(color, NAVY, 0.15)], [0, 0.55, 1]))
        rrect(c, x, y, w, h, 16, p)
        rrect(c, x + 12, y + 30, w - 24, 12, 6, paint(with_alpha(WHITE, 0.55)))
        rrect(c, x + 12, y + h - 44, w - 24, 12, 6, paint(with_alpha(WHITE, 0.55)))
        book_icon(c, icon, x + w / 2, y + h * 0.42, w * 0.62)
        c.restore()

    c.save()
    c.translate(0, -drop * 300)
    f = font("ExtraBold", 132)
    rising_word(c, "Full books.", 150, 300, f, INK, 5.05, t)
    x = 156
    for j, g in enumerate(["Grade 8", "10", "11", "12"]):
        kj = seg(t, 5.45 + j * 0.12, 5.8 + j * 0.12)
        if kj <= 0:
            break
        e = ease_out_back(kj, 2)
        ff = font("Bold", 40)
        pw = ff.measureText(g) + 48
        c.save()
        c.translate(x + pw / 2, 392)
        c.scale(e, e)
        rrect(c, -pw / 2, -36, pw, 72, 36, paint(WHITE))
        rrect(c, -pw / 2, -36, pw, 72, 36, paint(mix(BLUE_WASH, BLUE, 0.15), stroke=3))
        text(c, g, 0, 14, ff, BLUE, "center")
        c.restore()
        x += pw + 16
    kc = seg(round(t * FPS) / FPS, 5.85, 7.1)
    n = int(round(6000 * ease_out_cubic(kc) / 10) * 10)
    if kc > 0:
        big = font("ExtraBold", 168)
        a = clamp(kc * 5)
        label = f"{n:,}" + ("+" if kc >= 1 else "")
        text(c, label, 150, 660, big, with_alpha(BLUE, a))
        text(c, "pages of study books.", 158, 730, font("SemiBold", 44), with_alpha(MUTED, a))
        k2 = seg(t, 7.30, 7.70)
        if k2 > 0:
            e = ease_out_back(k2, 2.4)
            c.save()
            c.translate(158 + 120, 806)
            c.scale(e, e)
            rrect(c, -120, -40, 240, 80, 40, paint(MINT))
            text(c, "All free", 0, 15, font("ExtraBold", 40), WHITE, "center")
            c.restore()
    c.restore()
    c.restore()


# ------------------------------------------------------------------ scene D: open book

def scene_book(c, t):
    if t < 8.4 or t > 11.6:
        return
    k_in = ease_out_back(seg(t, 8.45, 8.95), 1.2)
    k_out = ease_in_cubic(seg(t, 11.2, 11.55))
    cx, cy = 900, 640
    bw, bh = 1180, 560
    c.save()
    c.translate(cx, cy + k_out * 120)
    s = lerp(0.6, 1.0, k_in) * (1 - 0.4 * k_out)
    c.scale(s, s)
    alpha = clamp(seg(t, 8.45, 8.7)) * (1 - k_out)
    c.saveLayerAlpha(None, int(255 * alpha))
    open_k = ease_out_cubic(seg(t, 8.55, 9.05))
    c.drawOval(skia.Rect.MakeXYWH(-bw * 0.52, bh * 0.44, bw * 1.04, 70), paint(with_alpha(NAVY, 0.14), blur=22))
    rrect(c, -bw / 2 - 18, -bh / 2 + 16, bw + 36, bh + 14, 30, paint(BLUE))
    for side in (-1, 1):
        pw = bw / 2 * (open_k if side == 1 else 1)
        x0 = 0 if side == 1 else -bw / 2
        p = skia.Path()
        if side == -1:
            p.moveTo(0, -bh / 2 + 18)
            p.cubicTo(-bw * 0.18, -bh / 2 - 10, -bw * 0.36, -bh / 2 + 4, -bw / 2, -bh / 2 + 2)
            p.lineTo(-bw / 2, bh / 2 - 6)
            p.cubicTo(-bw * 0.36, bh / 2 - 2, -bw * 0.18, bh / 2 - 16, 0, bh / 2 + 6)
        else:
            p.moveTo(0, -bh / 2 + 18)
            p.cubicTo(pw * 0.36, -bh / 2 - 10, pw * 0.72, -bh / 2 + 4, pw, -bh / 2 + 2)
            p.lineTo(pw, bh / 2 - 6)
            p.cubicTo(pw * 0.72, bh / 2 - 2, pw * 0.36, bh / 2 - 16, 0, bh / 2 + 6)
        p.close()
        c.drawPath(p, paint(WHITE))
        sh = paint(WHITE)
        sh.setShader(linear((0, 0), (side * 90, 0), [with_alpha(NAVY, 0.10), with_alpha(NAVY, 0.0)]))
        c.drawPath(p, sh)
    c.drawLine(0, -bh / 2 + 22, 0, bh / 2 + 2, paint(with_alpha(NAVY, 0.15), stroke=3))

    lx = -bw / 2 + 70
    kl = seg(t, 8.95, 9.6)
    rrect(c, lx, -bh / 2 + 70, 300 * ease_out_cubic(seg(t, 8.9, 9.2)), 26, 13, paint(BLUE_BRIGHT))
    for i in range(7):
        L = (bw / 2 - 150) * (0.92 if i % 3 else 0.6)
        kk = clamp(kl * 2.2 - i * 0.18)
        if kk > 0:
            c.drawLine(lx, -bh / 2 + 140 + i * 46, lx + L * ease_out_cubic(kk), -bh / 2 + 140 + i * 46,
                       paint(mix(BLUE_WASH, MUTED, 0.25), stroke=12))
    hl = seg(t, 9.25, 9.5)
    if hl > 0:
        c.drawLine(lx - 6, -bh / 2 + 186, lx - 6 + 260 * ease_out_cubic(hl), -bh / 2 + 186, paint(with_alpha(AMBER, 0.45), stroke=26, cap=False))

    if open_k > 0.95:
        rx = 70
        base = -20
        for i, v in enumerate([0.35, 0.62, 0.48, 0.85, 1.0]):
            kk = ease_out_back(seg(t, 9.45 + i * 0.06, 9.85 + i * 0.06), 1.8)
            bhh = 190 * v * kk
            rrect(c, rx + i * 52, base - bhh, 36, bhh, 8, paint(PURPLE if i == 4 else mix(PURPLE, WHITE, 0.55)))
        c.drawLine(rx - 12, base + 2, rx + 262, base + 2, paint(with_alpha(INK, 0.5), stroke=4))
        tri = polygon([(380, base), (520, base), (380, base - 180)])
        c.drawPath(partial_path(tri, seg(t, 9.55, 10.0)), paint(CORAL, stroke=7))
        if t > 9.95:
            c.drawPath(polygon([(380, base), (404, base), (404, base - 24), (380, base - 24)]), paint(CORAL, stroke=4))
        for i in range(3):
            y = 60 + i * 66
            kk = seg(t, 10.05 + i * 0.15, 10.35 + i * 0.15)
            c.drawLine(rx + 70, y + 2, rx + 70 + 330, y + 2, paint(mix(BLUE_WASH, MUTED, 0.2), stroke=11))
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

    words = [("Explained.", 9.0, BLUE_BRIGHT), ("Drawn.", 9.5, PURPLE), ("Solved.", 10.0, MINT)]
    f = font("ExtraBold", 104)
    gap = 40
    widths = [f.measureText(wd) for wd, _, _ in words]
    vis = 0.0
    for i, (wd, t0, _) in enumerate(words):
        vis += (widths[i] + (gap if i else 0)) * ease_out_cubic(seg(t, t0, t0 + 0.3))
    x = 960 - vis / 2
    up = k_out * 200
    for i, (wd, t0, col) in enumerate(words):
        k = seg(t, t0, t0 + 0.35)
        wdw = widths[i]
        if k > 0:
            e = ease_out_back(k, 2.0)
            active = t < t0 + 0.5 or wd == "Solved."
            c.save()
            c.translate(x + wdw / 2, 250 - up)
            c.scale(e, e)
            text(c, wd, 0, 0, f, col if active else INK, "center")
            c.restore()
        x += wdw + gap


# ------------------------------------------------------------------ scene E: together

FRIENDS = [(-1, 0.0, CORAL), (1, 0.0, AMBER), (-1, 1.0, MINT), (1, 1.0, PURPLE), (-0.5, -0.9, TEAL), (0.5, -0.9, PINK)]


FRIEND_AT = [(700, 520, 56), (1220, 520, 56), (500, 740, 68), (1420, 740, 68), (690, 950, 62), (1230, 950, 62)]


def friend_pos(i):
    return FRIEND_AT[i]


def scene_together(c, t):
    if t < 11.5 or t > 14.6:
        return
    f = font("ExtraBold", 120)
    up = ease_in_cubic(seg(t, 14.25, 14.5)) * 300
    rising_word(c, "Study together.", 960, 250 - up, f, INK, 12.0, t, align="center")
    nx, nby = 960, 720
    ncy = nby - 112
    for i in range(len(FRIENDS)):
        x, by, r = friend_pos(i)
        k = seg(t, 12.45 + i * 0.06, 12.85 + i * 0.06)
        if k > 0:
            p = skia.Path()
            p.moveTo(nx, ncy)
            p.quadTo((nx + x) / 2, min(ncy, by - r) - 90, x, by - r)
            c.drawPath(partial_path(p, ease_out_cubic(k)), paint(with_alpha(BLUE_BRIGHT, 0.35 * (1 - seg(t, 14.3, 14.5))), stroke=5))
    for i in range(len(FRIENDS)):
        x, by, r = friend_pos(i)
        t0 = 11.65 + i * 0.15
        k = seg(t, t0, t0 + 0.4)
        if k <= 0:
            continue
        e = ease_out_back(k, 2.6)
        hop = 0.0
        if 14.15 < t < 14.5:
            hop = 60 * math.sin(math.pi * seg(t, 14.15 + i * 0.02, 14.45))
        out = 1 - seg(t, 14.45, 14.6)
        u = t - t0
        blobatar(c, x, by, r * e, t, FRIENDS[i][2], alpha=out, look=((nx - x) / 600, -0.3), seed=i,
                 sq=0.25 * math.exp(-u * 8) * math.cos(u * 26) if u > 0 else 0)
    x0, by0, r0 = friend_pos(0)
    bubble(c, x0 + 70, by0 - r0 * 2 - 60, "?", seg(t, 12.8, 13.1) * (1 - seg(t, 14.0, 14.2)), WHITE, CORAL)
    bubble(c, 960 + 90, 720 - 112 * 2 - 80, "!", seg(t, 13.2, 13.5) * (1 - seg(t, 14.0, 14.2)), BLUE_BRIGHT, WHITE)
    for j in range(5):
        kk = seg(t, 13.25 + j * 0.05, 13.75 + j * 0.05)
        if 0 < kk < 1:
            a = 2 * math.pi * j / 5 + 0.4
            rr = 120 + 90 * ease_out_cubic(kk)
            sparkle(c, 960 + 90 + math.cos(a) * rr * 0.6, 720 - 304 + math.sin(a) * rr * 0.5, 16 * (1 - kk), AMBER)


def sparkle(c, x, y, s, color):
    if s <= 0.5:
        return
    p = skia.Path()
    p.moveTo(x, y - s)
    p.quadTo(x, y, x + s, y)
    p.quadTo(x, y, x, y + s)
    p.quadTo(x, y, x - s, y)
    p.quadTo(x, y, x, y - s)
    p.close()
    c.drawPath(p, paint(color))


# ------------------------------------------------------------------ scene F: end card

def scene_end(c, t):
    if t < 14.5:
        return
    if t < 15.0:
        k = ease_in_cubic(seg(t, 14.5, 15.0))
        r = lerp(112, 2600, k)
        by = lerp(720, 540 + r * 0.95, ease_in_out(seg(t, 14.5, 14.8)))
        neby(c, 960, by, r, t, look=(0, 0), shadow=k < 0.1, smile=1.0, cap=1.0)
        d = seg(t, 14.86, 15.0)
        if d > 0:
            p = paint(WHITE)
            p.setShader(skia.GradientShader.MakeRadial(skia.Point(960, 600), 1400, [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
            p.setAlphaf(ease_in_out(d))
            c.drawPaint(p)
        return
    p = paint(WHITE)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(960, 600), 1400, [0xFF1466F0, BLUE, 0xFF0A2E8A], [0, 0.55, 1]))
    c.drawPaint(p)
    for i in range(6):
        a = t * 0.25 + i
        c.drawCircle(960 + math.cos(a) * 700, 540 + math.sin(a * 1.3) * 380, 220,
                     paint(with_alpha(0xFF5B9BFF, 0.10), blur=90))
    lp = seg(t, 15.1, 16.0)
    float_y = math.sin(t * 2.0) * 6
    glow = seg(t, 15.7, 16.1)
    if glow > 0:
        c.drawCircle(960, 360 + float_y, 210, paint(with_alpha(0xFF8FB8FF, 0.22 * glow), blur=70))
    kt0 = seg(t, 14.95, 15.35)
    if kt0 > 0:
        e = ease_out_back(kt0, 1.7)
        c.save()
        c.translate(960, 360 + float_y)
        c.rotate((1 - e) * -12)
        c.scale(e, e)
        rrect(c, -170, -170 + 22, 340, 340, 84, paint(with_alpha(0xFF001A66, 0.35), blur=30))
        rrect(c, -170, -170, 340, 340, 84, paint(WHITE))
        c.restore()
    logo(c, 960 - 6, 360 + float_y, 236, lp * 1.25, t, on_blue=False)
    f = font("ExtraBold", 150)
    rising_word(c, "NEBians", 960, 690, f, WHITE, 15.55, t, align="center", stagger=0.045)
    kt = seg(t, 16.0, 16.4)
    if kt > 0:
        text(c, "Nepal's learning community", 960, 760 + (1 - ease_out_cubic(kt)) * 24,
             font("Medium", 46), with_alpha(0xFFDCE6FF, kt), "center")
    ku = seg(t, 16.35, 16.75)
    if ku > 0:
        e = ease_out_back(ku, 1.8)
        fu = font("Bold", 46)
        url = "nebians.consica.com.np"
        uw = fu.measureText(url) + 90
        c.save()
        c.translate(960, 870)
        c.scale(e, e)
        rrect(c, -uw / 2, -46, uw, 92, 46, paint(WHITE))
        text(c, url, 0, 16, fu, BLUE, "center")
        c.restore()
    ks = seg(t, 16.75, 17.15)
    if ks > 0:
        text(c, "Free on the web  ·  Android app on Google Play", 960, 990, font("Medium", 36),
             with_alpha(0xFFC9D8FF, ks), "center")
    for j, (sx, sy, d) in enumerate([(700, 220, 0.0), (1240, 270, 0.12), (1300, 520, 0.2), (640, 560, 0.3)]):
        kk = seg(t, 15.95 + d, 16.6 + d)
        if 0 < kk < 1:
            sparkle(c, sx, sy, 26 * math.sin(math.pi * kk), WHITE)
    kp = ease_out_back(seg(t, 16.2, 16.65), 1.6)
    if kp > 0:
        wink = 1.0 if 17.05 < t < 17.45 else 0.0
        neby(c, 1690, 1080 + 150 - 175 * kp, 120, t, look=(-0.9, -0.5), wink=wink, cap=1.0, shadow=False)


def frame(c, t):
    background(c, t, energy=1.0)
    scene_materials(c, t)
    scene_books(c, t)
    scene_book(c, t)
    scene_together(c, t)
    if t < 14.5:
        draw_neby(c, t)
        scene_hello(c, t)
    scene_end(c, t)
