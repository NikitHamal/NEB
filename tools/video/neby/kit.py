import math
import os

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "assets", "fonts")

W, H = 1920, 1080

BLUE = 0xFF004AC6
BLUE_BRIGHT = 0xFF0058DF
BLUE_WASH = 0xFFDBE1FF
NAVY = 0xFF021B54
INK = 0xFF0E2035
MUTED = 0xFF334E68
SKY = 0xFFDFF3FF
PAPER = 0xFFF7F9FF
WHITE = 0xFFFFFFFF
PURPLE = 0xFF6246D7
AMBER = 0xFFF2A516
CORAL = 0xFFFF6B5E
MINT = 0xFF2BB673
PINK = 0xFFFF8FB1
TEAL = 0xFF14A3B8

_TF = {}


def typeface(weight):
    if weight not in _TF:
        _TF[weight] = skia.Typeface.MakeFromFile(os.path.join(FONTS, f"Poppins-{weight}.ttf"))
    return _TF[weight]


def font(weight, size):
    f = skia.Font(typeface(weight), size)
    f.setEdging(skia.Font.Edging.kSubpixelAntiAlias)
    f.setSubpixel(True)
    return f


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def lerp(a, b, k):
    return a + (b - a) * k


def ease_out_cubic(k):
    return 1 - (1 - k) ** 3


def ease_in_cubic(k):
    return k ** 3


def ease_in_out(k):
    return 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2


def ease_out_back(k, s=1.70158):
    k -= 1
    return k * k * ((s + 1) * k + s) + 1


def ease_out_expo(k):
    return 1.0 if k >= 1 else 1 - 2 ** (-10 * k)


def spring(k, freq=3.2, damp=6.0):
    if k <= 0:
        return 0.0
    return 1 - math.exp(-damp * k) * math.cos(2 * math.pi * freq * k)


def with_alpha(color, a):
    a = clamp(a)
    return (int(((color >> 24) & 0xFF) * a) << 24) | (color & 0x00FFFFFF)


def mix(c1, c2, k):
    k = clamp(k)
    out = 0
    for sh in (24, 16, 8, 0):
        v = round(lerp((c1 >> sh) & 0xFF, (c2 >> sh) & 0xFF, k))
        out |= v << sh
    return out


def paint(color, stroke=None, cap=True, blur=0.0):
    p = skia.Paint(AntiAlias=True, Color=color)
    p.setDither(True)
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def linear(p0, p1, colors, pos=None):
    return skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)], colors, pos)


def rrect(c, x, y, w, h, r, p):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), p)


def shadow_rrect(c, x, y, w, h, r, alpha=0.16, dy=18, blur=26):
    rrect(c, x, y + dy, w, h, r, paint(with_alpha(NAVY, alpha), blur=blur))


def text(c, s, x, y, f, color, align="left"):
    w = f.measureText(s)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    c.drawString(s, x, y, f, paint(color))
    return w


def partial_path(path, k):
    if k >= 1:
        return path
    pm = skia.PathMeasure(path, False)
    out = skia.Path()
    while True:
        L = pm.getLength()
        pm.getSegment(0, L * clamp(k), out, True)
        if not pm.nextContour():
            break
    return out


def polygon(points):
    p = skia.Path()
    p.moveTo(*points[0])
    for q in points[1:]:
        p.lineTo(*q)
    p.close()
    return p
