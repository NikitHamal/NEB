"""Port of blobatar/src/shape.ts — superellipse and blob path primitives."""

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
