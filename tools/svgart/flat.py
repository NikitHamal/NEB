"""The flat look: warm cream ground, two-tone organic shapes, hairline details, sprigs of leaves."""
import math

from kit import FLAT as P, Rng, Svg, f, leaf, petal_flower, smooth, star_path


def ground(s, color=P["bg"], dots=True, rng=None):
    s.rect(0, 0, s.w, s.h, color)
    if dots and rng:
        for k in range(int(s.w * s.h / 9000)):
            s.circle(rng.u(0, s.w), rng.u(0, s.h), rng.u(1.2, 2.6), P["bg2"])


def sprig(s, x, y, length, angle, rng, color=P["olive"], dark=P["oliveD"], leaves=5, vein=True, curl=0.25):
    """A thin curving stem with alternating leaves; the tip curls a little."""
    a = math.radians(angle)
    pts = []
    for k in range(7):
        t = k / 6
        bend = math.sin(t * math.pi * 0.9) * curl * length * 0.3
        px = x + math.cos(a) * length * t - math.sin(a) * bend
        py = y + math.sin(a) * length * t + math.cos(a) * bend
        pts.append((px, py))
    s.path(smooth(pts), stroke=dark, sw=max(1.4, length * 0.012))
    for k in range(leaves):
        t = 0.25 + 0.7 * k / max(1, leaves - 1)
        i = min(5, int(t * 6))
        px, py = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * (t * 6 - i), pts[i][1] + (pts[i + 1][1] - pts[i][1]) * (t * 6 - i)
        side = 1 if k % 2 == 0 else -1
        la = angle + side * rng.u(35, 55)
        ln = length * rng.u(0.22, 0.32) * (1.1 - t * 0.4)
        d, rib = leaf(px, py, ln, ln * 0.34, la)
        s.path(d, color if k % 3 else dark)
        if vein:
            s.path(rib, stroke=P["cream"], sw=1.1, op=0.7)
    return pts[-1]


def big_leaf(s, x, y, length, angle, color=P["olive"], dark=P["oliveD"]):
    """A large two-tone leaf: one half lighter, a midrib and a few side veins in hairline."""
    d, rib = leaf(x, y, length, length * 0.3, angle)
    s.path(d, color)
    a = math.radians(angle)
    half = "M%s %s" % (f(x), f(y))
    tx, ty = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * length * 0.3, math.cos(a) * length * 0.3
    m = (x + math.cos(a) * length * 0.45, y + math.sin(a) * length * 0.45)
    half += "Q%s %s %s %sQ%s %s %s %sZ" % (f(m[0] - nx), f(m[1] - ny), f(tx), f(ty), f(m[0]), f(m[1]), f(x), f(y))
    s.path(half, dark, op=0.55)
    s.path(rib, stroke=P["cream"], sw=1.3, op=0.6)
    for k in range(1, 5):
        t = k / 5.5
        bx, by = x + math.cos(a) * length * t, y + math.sin(a) * length * t
        s.path("M%s %sQ%s %s %s %s" % (f(bx), f(by), f(bx + nx * 0.3 + math.cos(a) * length * 0.04), f(by + ny * 0.3 + math.sin(a) * length * 0.04),
                                      f(bx + nx * 0.55 + math.cos(a) * length * 0.1), f(by + ny * 0.55 + math.sin(a) * length * 0.1)),
               stroke=P["cream"], sw=0.9, op=0.45)


def flower(s, x, y, r, color, dark, rot=0.0, n=5, centre=None):
    for k, d in enumerate(petal_flower(x, y, r, n, rot)):
        s.path(d, color if k % 2 == 0 else dark)
    for k, d in enumerate(petal_flower(x, y, r * 0.95, n, rot)):
        s.path(d, stroke=dark, sw=0.9, op=0.5)
    s.circle(x, y + r * 0.08, r * 0.2, centre or P["oliveD"])


def stem_flower(s, x, y, h, angle, color, dark, rng, r=None):
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * h, y + math.sin(a) * h
    cx, cy = x + math.cos(a) * h * 0.5 + 18 * math.sin(a), y + math.sin(a) * h * 0.5
    s.path("M%s %sQ%s %s %s %s" % (f(x), f(y), f(cx), f(cy), f(tx), f(ty)), stroke=P["oliveD"], sw=1.6)
    flower(s, tx, ty, r or h * 0.22, color, dark, rot=angle + 90)
    return tx, ty


def berry_sprig(s, x, y, h, angle, color=P["coral"], n=3):
    a = math.radians(angle)
    for k in range(n):
        da = math.radians(angle + (k - (n - 1) / 2) * 22)
        tx, ty = x + math.cos(da) * h, y + math.sin(da) * h
        s.path("M%s %sQ%s %s %s %s" % (f(x), f(y), f((x + tx) / 2 + 6), f((y + ty) / 2), f(tx), f(ty)), stroke=P["oliveD"], sw=1.1)
        s.circle(tx, ty, 4.5, color)


def sparkle(s, x, y, r, color=P["must"]):
    s.path(star_path(x, y, r, r * 0.28, 4), color)


def curl(s, x, y, r, color=P["oliveD"], turns=1.4):
    pts = []
    for k in range(24):
        t = k / 23 * turns * 2 * math.pi
        rr = r * (1 - k / 30)
        pts.append((x + math.cos(t) * rr, y + math.sin(t) * rr))
    s.path(smooth(pts), stroke=color, sw=1.2)


def hand(s, x, y, size, skin=P["brown"], dark=P["brownD"], angle=-8, spread=1.0):
    """A raised open hand from the wrist at (x, y): palm, four tapering fingers fanned a little, a
    thumb, nails and creases in hairline. Drawn upright then rotated by [angle]."""
    w = size
    palm = ("M%s %s" % (f(x - w * 0.26), f(y)) +
            "C%s %s %s %s %s %s" % (f(x - w * 0.3), f(y - w * 0.4), f(x - w * 0.34), f(y - w * 0.62), f(x - w * 0.26), f(y - w * 0.78)) +
            "Q%s %s %s %s" % (f(x), f(y - w * 0.86), f(x + w * 0.27), f(y - w * 0.78)) +
            "C%s %s %s %s %s %s" % (f(x + w * 0.32), f(y - w * 0.55), f(x + w * 0.3), f(y - w * 0.3), f(x + w * 0.24), f(y)) + "Z")
    fingers = []
    for k, (fx, fl, fa) in enumerate([(-0.19, 0.48, -9), (-0.065, 0.58, -3), (0.065, 0.56, 3), (0.185, 0.44, 9)]):
        bx, by = x + w * fx, y - w * 0.74
        a = math.radians(-90 + fa * spread)
        L = w * fl
        tx, ty = bx + math.cos(a) * L, by + math.sin(a) * L
        nx, ny = -math.sin(a), math.cos(a)
        r0, r1 = w * 0.066, w * 0.052
        fingers.append(((bx, by), (tx, ty), (nx, ny), r0, r1, a))
    tf = "rotate(%s %s %s)" % (f(angle), f(x), f(y))

    def capsule(b, t, n, r0, r1, a):
        (bx, by), (tx, ty), (nx, ny) = b, t, n
        return ("M%s %sL%s %s" % (f(bx + nx * r0), f(by + ny * r0), f(tx + nx * r1), f(ty + ny * r1)) +
                "A%s %s 0 0 0 %s %s" % (f(r1), f(r1), f(tx - nx * r1), f(ty - ny * r1)) +
                "L%s %sZ" % (f(bx - nx * r0), f(by - ny * r0)))

    def draw():
        for k, (b, t, n, r0, r1, a) in enumerate(fingers):
            s.path(capsule(b, t, n, r0, r1, a), skin if k % 2 == 0 else skin)
            # the nail and a knuckle crease
            s.path("M%s %sQ%s %s %s %s" % (f(t[0] - n[0] * r1 * 0.6 - math.cos(a) * r1 * 0.9), f(t[1] - n[1] * r1 * 0.6 - math.sin(a) * r1 * 0.9),
                                          f(t[0] - math.cos(a) * r1 * 0.2), f(t[1] - math.sin(a) * r1 * 0.2),
                                          f(t[0] + n[0] * r1 * 0.6 - math.cos(a) * r1 * 0.9), f(t[1] + n[1] * r1 * 0.6 - math.sin(a) * r1 * 0.9)), stroke=P["mustL"], sw=1.1, op=0.8)
            mx, my = b[0] + (t[0] - b[0]) * 0.42, b[1] + (t[1] - b[1]) * 0.42
            s.path("M%s %sL%s %s" % (f(mx - n[0] * r0 * 0.5), f(my - n[1] * r0 * 0.5), f(mx + n[0] * r0 * 0.5), f(my + n[1] * r0 * 0.5)), stroke=dark, sw=1, op=0.5)
        s.path(palm, skin)
        # the shaded edge of the palm, and the thumb across it
        s.path("M%s %sC%s %s %s %s %s %sL%s %sC%s %s %s %s %s %sZ" % (f(x + w * 0.24), f(y), f(x + w * 0.3), f(y - w * 0.3), f(x + w * 0.32), f(y - w * 0.55), f(x + w * 0.27), f(y - w * 0.78),
                                                                   f(x + w * 0.18), f(y - w * 0.74), f(x + w * 0.22), f(y - w * 0.5), f(x + w * 0.2), f(y - w * 0.25), f(x + w * 0.12), f(y)), dark, op=0.55)
        thumb = ("M%s %s" % (f(x - w * 0.24), f(y - w * 0.3)) +
                 "C%s %s %s %s %s %s" % (f(x - w * 0.42), f(y - w * 0.38), f(x - w * 0.56), f(y - w * 0.56), f(x - w * 0.58), f(y - w * 0.72)) +
                 "A%s %s 0 0 1 %s %s" % (f(w * 0.06), f(w * 0.06), f(x - w * 0.47), f(y - w * 0.74)) +
                 "C%s %s %s %s %s %s" % (f(x - w * 0.42), f(y - w * 0.62), f(x - w * 0.34), f(y - w * 0.52), f(x - w * 0.22), f(y - w * 0.5)) + "Z")
        s.path(thumb, skin)
        s.path("M%s %sC%s %s %s %s %s %s" % (f(x - w * 0.24), f(y - w * 0.3), f(x - w * 0.42), f(y - w * 0.38), f(x - w * 0.56), f(y - w * 0.56), f(x - w * 0.58), f(y - w * 0.72)), stroke=dark, sw=1.2, op=0.55)
        s.path("M%s %sQ%s %s %s %s" % (f(x - w * 0.16), f(y - w * 0.5), f(x + w * 0.02), f(y - w * 0.44), f(x + w * 0.18), f(y - w * 0.58)), stroke=dark, sw=1.2, op=0.55)
        s.path("M%s %sQ%s %s %s %s" % (f(x - w * 0.02), f(y - w * 0.38), f(x + w * 0.08), f(y - w * 0.2), f(x + w * 0.06), f(y - w * 0.02)), stroke=dark, sw=1.1, op=0.45)
    s.group(draw, tf=tf)


def person(s, x, ground, h, skin=P["brown"], top=P["coral"], hair=P["ink"], rng=None, sitting=False, book=None):
    """A simple editorial figure: oval head with a hair cap, a rounded torso, no outlines."""
    hr = h * 0.11
    hx, hy = x, ground - h + hr
    body = ("M%s %s" % (f(x - h * 0.2), f(ground)) + "C%s %s %s %s %s %s" % (f(x - h * 0.22), f(hy + hr * 2.2), f(x - h * 0.12), f(hy + hr * 1.4), f(x), f(hy + hr * 1.35)) +
            "C%s %s %s %s %s %s" % (f(x + h * 0.12), f(hy + hr * 1.4), f(x + h * 0.22), f(hy + hr * 2.2), f(x + h * 0.2), f(ground)) + "Z")
    s.path(body, top)
    s.path("M%s %sQ%s %s %s %s" % (f(x - h * 0.05), f(hy + hr * 1.9), f(x), f(hy + hr * 2.6), f(x + h * 0.04), f(ground - h * 0.05)), stroke=P["cream"], sw=1, op=0.4)
    s.ellipse(hx, hy, hr * 0.92, hr, skin)
    s.path("M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" % (f(hx - hr * 0.95), f(hy + hr * 0.1), f(hx - hr), f(hy - hr * 1.3), f(hx + hr), f(hy - hr * 1.3),
                                                         f(hx + hr * 0.95), f(hy - hr * 0.05), f(hx + hr * 0.4), f(hy - hr * 0.6), f(hx - hr * 0.3), f(hy - hr * 0.55), f(hx - hr * 0.95), f(hy + hr * 0.1)), hair)
    return hx, hy, hr


def open_book(s, cx, cy, w, page="#fffaf0", cover=P["vio"], tilt=0):
    h = w * 0.3
    def draw():
        s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx - w * 0.54), f(cy + h * 0.15), f(cx - w * 0.25), f(cy - h * 0.55), f(cx), f(cy - h * 0.05),
                                                       f(cx), f(cy + h * 0.38), f(cx - w * 0.25), f(cy + h * 0.02), f(cx - w * 0.54), f(cy + h * 0.6)), cover)
        s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx + w * 0.54), f(cy + h * 0.15), f(cx + w * 0.25), f(cy - h * 0.55), f(cx), f(cy - h * 0.05),
                                                       f(cx), f(cy + h * 0.38), f(cx + w * 0.25), f(cy + h * 0.02), f(cx + w * 0.54), f(cy + h * 0.6)), cover)
        s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx - w / 2), f(cy), f(cx - w / 4), f(cy - h), f(cx), f(cy - h * 0.2),
                                                       f(cx), f(cy + h * 0.25), f(cx - w / 4), f(cy - h * 0.6), f(cx - w / 2), f(cy + h * 0.4)), page, stroke=P["ink"], sw=1.2)
        s.path("M%s %sQ%s %s %s %sL%s %sQ%s %s %s %sZ" % (f(cx + w / 2), f(cy), f(cx + w / 4), f(cy - h), f(cx), f(cy - h * 0.2),
                                                       f(cx), f(cy + h * 0.25), f(cx + w / 4), f(cy - h * 0.6), f(cx + w / 2), f(cy + h * 0.4)), "#f3e6cc", stroke=P["ink"], sw=1.2)
        for k in range(4):
            yy = cy - h * 0.28 + k * h * 0.17
            s.path("M%s %sQ%s %s %s %s" % (f(cx - w * 0.4), f(yy + h * 0.2), f(cx - w * 0.22), f(yy - h * 0.12), f(cx - w * 0.07), f(yy + h * 0.06)), stroke=P["lav"], sw=1.2)
            s.path("M%s %sQ%s %s %s %s" % (f(cx + w * 0.07), f(yy + h * 0.06), f(cx + w * 0.22), f(yy - h * 0.12), f(cx + w * 0.4), f(yy + h * 0.2)), stroke=P["lav"], sw=1.2)
    s.group(draw, tf=("rotate(%s %s %s)" % (f(tilt), f(cx), f(cy))) if tilt else None)


def butterfly(s, x, y, size, wing=P["lav"], dark=P["vio"], eye=P["coral"], rot=-20):
    def draw():
        up = "M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" % (f(x), f(y), f(x - size * 0.3), f(y - size * 1.1), f(x + size * 0.9), f(y - size * 1.2), f(x + size * 0.75), f(y - size * 0.25),
                                                           f(x + size * 0.6), f(y), f(x + size * 0.2), f(y + size * 0.05), f(x), f(y))
        lo = "M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" % (f(x), f(y), f(x + size * 0.5), f(y + size * 0.05), f(x + size * 0.7), f(y + size * 0.45), f(x + size * 0.35), f(y + size * 0.6),
                                                           f(x + size * 0.1), f(y + size * 0.65), f(x - size * 0.05), f(y + size * 0.3), f(x), f(y))
        back = "M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ" % (f(x), f(y), f(x - size * 0.2), f(y - size * 0.9), f(x - size * 0.45), f(y - size * 0.9), f(x - size * 0.5), f(y - size * 0.4),
                                                             f(x - size * 0.5), f(y - size * 0.1), f(x - size * 0.2), f(y + size * 0.1), f(x), f(y))
        s.path(back, dark)
        s.path(lo, wing)
        s.path(up, wing)
        for k in range(5):
            t = 0.2 + k * 0.15
            s.path("M%s %sQ%s %s %s %s" % (f(x + size * 0.05), f(y - size * 0.05), f(x + size * t * 0.8), f(y - size * (0.9 - t * 0.4)), f(x + size * (0.25 + t * 0.6)), f(y - size * (0.65 - t * 0.5))),
                   stroke=P["lavL"], sw=1.1, op=0.8)
        s.circle(x + size * 0.42, y - size * 0.62, size * 0.17, P["cream"])
        s.circle(x + size * 0.42, y - size * 0.62, size * 0.1, eye)
        s.circle(x + size * 0.42, y - size * 0.62, size * 0.05, P["must"])
        s.path("M%s %sL%s %s" % (f(x - size * 0.05), f(y + size * 0.2), f(x + size * 0.05), f(y - size * 0.25)), stroke=dark, sw=size * 0.08)
        s.path("M%s %sQ%s %s %s %s" % (f(x + size * 0.05), f(y - size * 0.25), f(x + size * 0.4), f(y - size * 0.7), f(x + size * 0.9), f(y - size * 0.75)), stroke=dark, sw=1)
        s.path("M%s %sQ%s %s %s %s" % (f(x + size * 0.05), f(y - size * 0.25), f(x + size * 0.45), f(y - size * 0.55), f(x + size * 0.95), f(y - size * 0.5)), stroke=dark, sw=1)
    s.group(draw, tf="rotate(%s %s %s)" % (f(rot), f(x), f(y)))
