"""Port of blobatar/src/shape.ts — superellipse, blob, polygon, capsule and taper primitives."""

import math


def _r2(v):
    s = math.floor(v * 100 + 0.5) / 100
    if s == 0:
        return "0"
    if s.is_integer():
        return str(int(s))
    return str(s)


def superellipse(cx, cy, rx, ry, n=4, rot=0):
    k = min(1, (8 * math.pow(2, -1 / n) - 4) / 3)
    a = rx
    b = ry
    ak = a * k
    bk = b * k

    pts = [
        (a, 0),
        (a, bk), (ak, b), (0, b),
        (-ak, b), (-a, bk), (-a, 0),
        (-a, -bk), (-ak, -b), (0, -b),
        (ak, -b), (a, -bk), (a, 0),
    ]

    t = (rot * math.pi) / 180
    cos = math.cos(t)
    sin = math.sin(t)

    def at(i):
        x, y = pts[i]
        return "%s %s" % (_r2(cx + x * cos - y * sin), _r2(cy + x * sin + y * cos))

    d = "M%s" % at(0)
    for i in range(1, 13, 3):
        d += "C%s %s %s" % (at(i), at(i + 1), at(i + 2))
    return d + "Z"


def blob_path(cx, cy, rx, ry, radii, rot=0):
    n = len(radii)
    t0 = (rot * math.pi) / 180
    p = []
    for i, m in enumerate(radii):
        a = t0 + (2 * math.pi * i) / n
        p.append((cx + rx * m * math.cos(a), cy + ry * m * math.sin(a)))

    def at(i):
        return p[i % n]

    d = "M%s %s" % (_r2(at(0)[0]), _r2(at(0)[1]))

    for i in range(n):
        x0, y0 = at(i - 1)
        x1, y1 = at(i)
        x2, y2 = at(i + 1)
        x3, y3 = at(i + 2)
        d += (
            "C%s %s" % (_r2(x1 + (x2 - x0) / 6), _r2(y1 + (y2 - y0) / 6))
            + " %s %s" % (_r2(x2 - (x3 - x1) / 6), _r2(y2 - (y3 - y1) / 6))
            + " %s %s" % (_r2(x2), _r2(y2))
        )

    return d + "Z"


def arc(cx, cy, w, depth):
    """A quadratic arc, stroked — used only for smiles and frowns."""
    return "M%s %sQ%s %s %s %s" % (
        _r2(cx - w), _r2(cy), _r2(cx), _r2(cy + depth), _r2(cx + w), _r2(cy),
    )


def polygon(cx, cy, rx, ry, sides, round_=0.3, rot=0):
    """A regular polygon with rounded corners. round_ is 0 (sharp) to 1 (all curve)."""
    k = round_ / 2 if 0 < round_ < 1 else (0.5 if round_ > 0 else 0)
    t0 = (rot * math.pi) / 180 - math.pi / 2
    v = [
        (cx + rx * math.cos(t0 + (2 * math.pi * i) / sides),
         cy + ry * math.sin(t0 + (2 * math.pi * i) / sides))
        for i in range(sides)
    ]

    def at(i):
        return v[i % sides]

    def cut(i, j):
        x0, y0 = at(i)
        x1, y1 = at(j)
        return "%s %s" % (_r2(x0 + (x1 - x0) * k), _r2(y0 + (y1 - y0) * k))

    d = "M%s" % cut(0, -1)
    for i in range(sides):
        x, y = at(i)
        d += "Q%s %s %s" % (_r2(x), _r2(y), cut(i, i + 1))
        if k < 0.5:
            d += "L%s" % cut(i + 1, i)
    return d + "Z"


def box(cx, cy, rx, ry):
    """The straight run of a capsule, as a plain box drawn with its cap circles."""
    l = _r2(cx - rx)
    r = _r2(cx + rx)
    return "M%s %sH%sV%sH%sZ" % (l, _r2(cy - ry), r, _r2(cy + ry), l)


def taper(cx, cy, rx, ry, tip):
    """The taper of a droplet: two tangents from an apex to the body ellipse."""
    t = max(1.05, tip)
    tx = rx * math.sqrt(1 - 1 / (t * t))
    ty = cy - ry / t
    apex = cy - t * ry
    px = tx * 0.14
    py = ty + 0.86 * (apex - ty)
    return (
        "M%s %s" % (_r2(cx - tx), _r2(ty))
        + "L%s %s" % (_r2(cx - px), _r2(py))
        + "Q%s %s %s %s" % (_r2(cx), _r2(apex), _r2(cx + px), _r2(py))
        + "L%s %sZ" % (_r2(cx + tx), _r2(ty))
    )
