"""Props and characters, drawn through a Painter so each one works in every look."""
import math

from kit import f, smooth, star_path
from painter import circle_d, rrect_d, shade_hex


def P(x, y):
    return "%s %s" % (f(x), f(y))


def poly(*pts):
    return "M" + "L".join(P(x, y) for x, y in pts) + "Z"


# ---------------------------------------------------------------- characters
def soul(p, x, ground, size, body="c", head="a", lean=0.0, mood="smile", glow=True, arm=True):
    """The monumental soft figure of the references: a cloak-body spreading to the ground, sloped
    shoulders, a small round head lit from within, a tiny dot-eye face."""
    w, h = size, size * 1.05
    top = ground - h
    d = ("M" + P(x - w * 0.78, ground) +
         "C" + P(x - w * 0.70, top + h * 0.55) + " " + P(x - w * 0.42 + lean, top + h * 0.05) + " " + P(x + lean * 0.6, top + h * 0.02) +
         "C" + P(x + w * 0.36 + lean, top) + " " + P(x + w * 0.62, top + h * 0.42) + " " + P(x + w * 0.70, top + h * 0.78) +
         "C" + P(x + w * 0.74, top + h * 0.9) + " " + P(x + w * 0.70, ground - h * 0.02) + " " + P(x + w * 0.66, ground) + "Z")
    p.form(d, body, size * 1.4, light=(0.45, 0.0))
    if arm:
        ad = ("M" + P(x - w * 0.05, top + h * 0.38) + "C" + P(x + w * 0.25, top + h * 0.42) + " " + P(x + w * 0.52, top + h * 0.62) + " " + P(x + w * 0.5, top + h * 0.8) +
              "C" + P(x + w * 0.38, top + h * 0.86) + " " + P(x + w * 0.12, top + h * 0.7) + " " + P(x - w * 0.05, top + h * 0.56) + "Z")
        p.solid(ad, "dark", op=0.35)
    hr = size * 0.12
    hx, hy = x + lean * 0.6, top - hr * 0.5
    if glow:
        p.glow(hx, hy, hr * 3.6, head, 0.85)
    p.circle(hx, hy, hr, head)
    face(p, hx, hy + hr * 0.1, hr, mood)
    return hx, hy, hr, top


def face(p, cx, cy, size, mood="smile"):
    e = size * 0.17
    if mood == "sleep":
        for sx in (-1, 1):
            p.line("M" + P(cx + sx * size * 0.42, cy - size * 0.02) + "Q" + P(cx + sx * size * 0.28, cy + size * 0.12) + " " + P(cx + sx * size * 0.14, cy - size * 0.02), "ink", size * 0.1)
    else:
        p.circle(cx - size * 0.28, cy - size * 0.05, e, "ink")
        p.circle(cx + size * 0.28, cy - size * 0.05, e, "ink")
    if mood in ("smile", "sleep"):
        p.line("M" + P(cx - size * 0.2, cy + size * 0.22) + "Q" + P(cx, cy + size * 0.42) + " " + P(cx + size * 0.2, cy + size * 0.22), "ink", size * 0.1)
    elif mood == "o":
        p.circle(cx, cy + size * 0.3, size * 0.1, "ink")
    elif mood == "calm":
        p.line("M" + P(cx - size * 0.14, cy + size * 0.3) + "L" + P(cx + size * 0.14, cy + size * 0.3), "ink", size * 0.09)


def orb(p, x, y, r, body="c", mood="smile", ring=True):
    """Neby, the app's round mascot, as an orb: a body lit from the top left, a horizon of
    deeper colour across its lower half, and the dot-eye face."""
    p.glow(x, y, r * 2.2, "a", 0.5)
    p.form(circle_d(x, y, r), body, r * 2, light=(0.3, 0.15))
    low = "M" + P(x - r, y + r * 0.1) + "Q" + P(x, y + r * 0.35) + " " + P(x + r, y + r * 0.1) + "A%s %s 0 0 1 %s Z" % (f(r), f(r), P(x - r, y + r * 0.1))
    p.solid(low, "dark", op=0.45)
    p.circle(x - r * 0.38, y - r * 0.42, r * 0.16, "e", op=0.85)
    face(p, x, y - r * 0.05, r * 0.55, mood)
    if ring:
        p.line("M" + P(x - r * 1.5, y + r * 0.2) + "Q" + P(x, y + r * 0.75) + " " + P(x + r * 1.5, y + r * 0.2), "a", r * 0.06, op=0.8)


# ---------------------------------------------------------------- study things
def open_book(p, cx, cy, w, cover="d", tilt=0.0, lines=True):
    h = w * 0.3

    def draw():
        for sx in (-1, 1):
            p.form("M" + P(cx + sx * w * 0.54, cy + h * 0.15) + "Q" + P(cx + sx * w * 0.25, cy - h * 0.55) + " " + P(cx, cy - h * 0.05) +
                   "L" + P(cx, cy + h * 0.38) + "Q" + P(cx + sx * w * 0.25, cy + h * 0.02) + " " + P(cx + sx * w * 0.54, cy + h * 0.6) + "Z", cover, w, shade=False)
        for sx, role in ((-1, "page"), (1, "e")):
            d = ("M" + P(cx + sx * w / 2, cy) + "Q" + P(cx + sx * w / 4, cy - h) + " " + P(cx, cy - h * 0.2) +
                 "L" + P(cx, cy + h * 0.25) + "Q" + P(cx + sx * w / 4, cy - h * 0.6) + " " + P(cx + sx * w / 2, cy + h * 0.4) + "Z")
            p.form(d, role, w * 0.5, shade=False)
            p.line(d, "ink", max(1, w * 0.006), op=0.5)
        if lines:
            for k in range(4):
                yy = cy - h * 0.28 + k * h * 0.17
                for sx in (-1, 1):
                    a, b = (cx + sx * w * 0.07, cx + sx * w * 0.4)
                    p.detail("M" + P(a, yy + h * 0.06) + "Q" + P(cx + sx * w * 0.22, yy - h * 0.12) + " " + P(b, yy + h * 0.2), "c", max(1, w * 0.006), 0.9)
    p.s.group(draw, tf=("rotate(%s %s %s)" % (f(tilt), f(cx), f(cy))) if tilt else None)


def book_stack(p, x, ground, w, n=4, roles=("d", "b", "a", "g", "c", "f")):
    y = ground
    for k in range(n):
        bh = w * (0.16 + 0.03 * (k % 2))
        off = (k % 3 - 1) * w * 0.05
        bw = w * (1 - 0.06 * (k % 3))
        d = rrect_d(x - bw / 2 + off, y - bh, bw, bh, bh * 0.2)
        p.form(d, roles[k % len(roles)], bw, light=(0.3, 0.0))
        p.solid(rrect_d(x - bw / 2 + off + bw * 0.04, y - bh * 0.78, bw * 0.08, bh * 0.56, 2), "e", op=0.8)
        p.solid(rrect_d(x + bw / 2 + off - bw * 0.1, y - bh * 0.7, bw * 0.06, bh * 0.4, 2), "page", op=0.9)
        y -= bh


def upright_books(p, x, ground, w, n=6, roles=("d", "b", "a", "g", "c", "f")):
    xx = x
    for k in range(n):
        bw = w / n * (0.8 + 0.3 * ((k * 7) % 3) / 2)
        bh = w * (0.42 + 0.12 * ((k * 5) % 4) / 3)
        lean = 6 if k == n - 1 else 0
        d = rrect_d(xx, ground - bh, bw * 0.92, bh, 3)
        p.s.group(lambda d=d, r=roles[k % len(roles)], bw=bw: p.form(d, r, bw * 2, shade=False),
                  tf="rotate(%s %s %s)" % (lean, f(xx), f(ground)) if lean else None)
        p.solid(rrect_d(xx + bw * 0.12, ground - bh * 0.8, bw * 0.6, bh * 0.08, 1), "e", op=0.7)
        xx += bw


def pencil(p, x, y, length, angle=-35, body="a"):
    w = length * 0.11

    def draw():
        p.form(rrect_d(x, y - w / 2, length * 0.78, w, w * 0.15), body, length, light=(0.5, 0.0))
        p.solid(rrect_d(x - length * 0.1, y - w / 2, length * 0.12, w, w * 0.4), "f")
        p.solid(rrect_d(x - length * 0.01, y - w / 2, length * 0.05, w, 1), "e", op=0.9)
        p.solid(poly((x + length * 0.78, y - w / 2), (x + length, y), (x + length * 0.78, y + w / 2)), "h")
        p.solid(poly((x + length * 0.93, y - w * 0.16), (x + length, y), (x + length * 0.93, y + w * 0.16)), "ink")
        p.detail("M" + P(x + length * 0.05, y) + "L" + P(x + length * 0.74, y), "e", 1.2, 0.5)
    p.s.group(draw, tf="rotate(%s %s %s)" % (f(angle), f(x), f(y)))


def lamp_diyo(p, x, y, w):
    """A clay diyo with its flame, the light of study and of Tihar."""
    p.glow(x, y - w * 0.5, w * 1.1, "a", 0.6)
    bowl = "M" + P(x - w / 2, y - w * 0.12) + "Q" + P(x, y + w * 0.38) + " " + P(x + w / 2, y - w * 0.12) + "Q" + P(x + w * 0.1, y - w * 0.02) + " " + P(x - w / 2, y - w * 0.12) + "Z"
    p.form(bowl, "b", w, light=(0.4, 0.0))
    p.solid("M" + P(x - w / 2, y - w * 0.12) + "Q" + P(x, y - w * 0.22) + " " + P(x + w / 2, y - w * 0.12) + "Q" + P(x, y - w * 0.02) + " " + P(x - w / 2, y - w * 0.12) + "Z", "d", op=0.6)
    fl = "M" + P(x, y - w * 0.85) + "C" + P(x + w * 0.16, y - w * 0.55) + " " + P(x + w * 0.12, y - w * 0.22) + " " + P(x, y - w * 0.2) + "C" + P(x - w * 0.12, y - w * 0.22) + " " + P(x - w * 0.16, y - w * 0.5) + " " + P(x, y - w * 0.85) + "Z"
    p.solid(fl, "a")
    p.solid("M" + P(x, y - w * 0.58) + "C" + P(x + w * 0.07, y - w * 0.4) + " " + P(x + w * 0.05, y - w * 0.24) + " " + P(x, y - w * 0.23) + "C" + P(x - w * 0.05, y - w * 0.24) + " " + P(x - w * 0.07, y - w * 0.4) + " " + P(x, y - w * 0.58) + "Z", "e")


def paper(p, x, y, w, h, tilt=-6, ticks=True, role="page"):
    def draw():
        d = rrect_d(x, y, w, h, w * 0.04)
        p.form(d, role, w, light=(0.2, 0.0), shade=False)
        p.line(d, "ink", 1.3, op=0.35)
        for k in range(6):
            yy = y + h * (0.18 + k * 0.12)
            p.detail("M" + P(x + w * 0.24, yy) + "L" + P(x + w * (0.85 - (k % 3) * 0.1), yy), "c", max(1.2, w * 0.012), 0.9)
            if ticks:
                if k % 2 == 0:
                    p.line("M" + P(x + w * 0.08, yy) + "L" + P(x + w * 0.12, yy + h * 0.03) + "L" + P(x + w * 0.18, yy - h * 0.035), "g", max(1.5, w * 0.018))
                else:
                    p.circle(x + w * 0.13, yy, w * 0.03, "b", op=0.9)
    p.s.group(draw, tf="rotate(%s %s %s)" % (f(tilt), f(x + w / 2), f(y + h / 2)))


def clock(p, x, y, r, t=0.33):
    p.form(circle_d(x, y, r), "b", r * 2)
    p.solid(circle_d(x, y, r * 0.8), "page")
    for k in range(12):
        a = k / 12 * 2 * math.pi
        rr = r * (0.66 if k % 3 else 0.6)
        p.line("M" + P(x + math.cos(a) * rr, y + math.sin(a) * rr) + "L" + P(x + math.cos(a) * r * 0.72, y + math.sin(a) * r * 0.72), "ink", max(1, r * 0.04), op=0.6)
    a1, a2 = (t * 12) / 12 * 2 * math.pi - math.pi / 2, (t * 12 % 1) * 2 * math.pi - math.pi / 2
    p.line("M" + P(x, y) + "L" + P(x + math.cos(a1) * r * 0.38, y + math.sin(a1) * r * 0.38), "ink", r * 0.07)
    p.line("M" + P(x, y) + "L" + P(x + math.cos(a2) * r * 0.58, y + math.sin(a2) * r * 0.58), "ink", r * 0.045)
    p.circle(x, y, r * 0.06, "b")


def cap(p, x, y, w):
    """A graduation cap, for exams and results."""
    top = poly((x - w / 2, y), (x, y - w * 0.22), (x + w / 2, y), (x, y + w * 0.22))
    p.form("M" + P(x - w * 0.3, y + w * 0.05) + "L" + P(x - w * 0.3, y + w * 0.3) + "Q" + P(x, y + w * 0.45) + " " + P(x + w * 0.3, y + w * 0.3) + "L" + P(x + w * 0.3, y + w * 0.05) + "Z", "ink", w)
    p.form(top, "d", w, light=(0.3, 0.0))
    p.line("M" + P(x, y) + "Q" + P(x + w * 0.35, y + w * 0.08) + " " + P(x + w * 0.38, y + w * 0.38), "a", max(2, w * 0.03))
    p.circle(x + w * 0.38, y + w * 0.42, w * 0.045, "a")


# ---------------------------------------------------------------- science
def flask(p, x, ground, h, liquid="g", bubbles=True):
    w = h * 0.75
    neck = h * 0.36
    d = ("M" + P(x - w * 0.14, ground - h) + "L" + P(x - w * 0.14, ground - h + neck) + "L" + P(x - w * 0.5, ground - h * 0.08) +
         "Q" + P(x - w * 0.52, ground) + " " + P(x - w * 0.42, ground) + "L" + P(x + w * 0.42, ground) + "Q" + P(x + w * 0.52, ground) + " " + P(x + w * 0.5, ground - h * 0.08) +
         "L" + P(x + w * 0.14, ground - h + neck) + "L" + P(x + w * 0.14, ground - h) + "Z")
    p.form(d, "e", h, light=(0.3, 0.0), shade=False)
    lvl = ground - h * 0.42
    cid = p.s.clip(d)
    p.s.group(lambda: p.form("M" + P(x - w, lvl) + "Q" + P(x - w * 0.25, lvl - h * 0.05) + " " + P(x, lvl) + "T" + P(x + w, lvl) + "L" + P(x + w, ground + 5) + "L" + P(x - w, ground + 5) + "Z", liquid, w), clip=cid)
    p.line(d, "ink", max(1.5, h * 0.012), op=0.55)
    p.solid(rrect_d(x - w * 0.2, ground - h - h * 0.04, w * 0.4, h * 0.06, h * 0.02), "ink", op=0.7)
    p.detail("M" + P(x - w * 0.3, ground - h * 0.32) + "Q" + P(x - w * 0.36, ground - h * 0.14) + " " + P(x - w * 0.28, ground - h * 0.06), "e", max(1.5, h * 0.02), 0.8)
    if bubbles:
        for k, (bx, by, br) in enumerate(((0.05, 0.6, 0.035), (-0.08, 0.75, 0.025), (0.1, 0.88, 0.02), (0.02, 1.05, 0.03), (-0.04, 1.2, 0.022))):
            p.circle(x + w * bx, ground - h * by, h * br, "e" if by > 0.95 else "a", op=0.85)


def atom(p, x, y, r, nucleus="b", orbit="c"):
    for k in range(3):
        a = k * 60
        p.s.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s" transform="rotate(%s %s %s)" opacity="0.9"/>' % (
            f(x), f(y), f(r), f(r * 0.36), p.c(orbit), f(max(1.5, r * 0.035)), a, f(x), f(y)))
    p.glow(x, y, r * 0.6, "a", 0.8)
    p.disc(x, y, r * 0.18, nucleus)
    for k, ang in enumerate((20, 145, 260)):
        a = math.radians(ang)
        ex, ey = r * math.cos(a), r * 0.36 * math.sin(a)
        rot = math.radians(k * 60)
        p.circle(x + ex * math.cos(rot) - ey * math.sin(rot), y + ex * math.sin(rot) + ey * math.cos(rot), r * 0.07, "a")


def prism(p, x, y, size, beam=True):
    """A glass prism splitting a beam of light into a fan of colours."""
    tri = poly((x, y - size * 0.55), (x - size * 0.5, y + size * 0.35), (x + size * 0.5, y + size * 0.35))
    if beam:
        p.solid(poly((x - size * 1.6, y + size * 0.05), (x - size * 0.28, y - size * 0.08), (x - size * 0.26, y + size * 0.02), (x - size * 1.6, y + size * 0.12)),
                "e" if p.look == "riso" else "a", op=0.85)
        for k, role in enumerate(("f", "b", "a", "g", "c", "d")):
            a0 = math.radians(-8 + k * 6)
            a1 = math.radians(-8 + (k + 1) * 6)
            ox, oy = x + size * 0.24, y - size * 0.02
            L = size * 1.7
            p.solid(poly((ox, oy), (ox + math.cos(a0) * L, oy + math.sin(a0) * L), (ox + math.cos(a1) * L, oy + math.sin(a1) * L)), role, op=0.9)
    p.form(tri, "e", size, light=(0.2, 0.0))
    p.solid(poly((x, y - size * 0.55), (x + size * 0.5, y + size * 0.35), (x + size * 0.12, y + size * 0.35)), "c", op=0.35)
    p.line(tri, "ink", max(1.5, size * 0.015), op=0.5)


def planet(p, x, y, r, body="b", ring="a"):
    back = "M" + P(x - r * 1.75, y) + "A%s %s -12 0 1 %s" % (f(r * 1.75), f(r * 0.42), P(x + r * 1.75, y))
    p.s.add('<path d="%s" fill="none" stroke="%s" stroke-width="%s" transform="rotate(-14 %s %s)"/>' % (back, p.c(ring), f(r * 0.12), f(x), f(y)))
    p.form(circle_d(x, y, r), body, r * 2, light=(0.3, 0.2))
    for k in range(3):
        p.detail("M" + P(x - r * 0.9, y - r * 0.4 + k * r * 0.4) + "Q" + P(x, y - r * 0.3 + k * r * 0.4) + " " + P(x + r * 0.9, y - r * 0.45 + k * r * 0.4), "e", max(1.5, r * 0.04), 0.4)
    front = "M" + P(x - r * 1.75, y) + "A%s %s -12 0 0 %s" % (f(r * 1.75), f(r * 0.42), P(x + r * 1.75, y))
    p.s.add('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" transform="rotate(-14 %s %s)"/>' % (front, p.c(ring), f(r * 0.12), f(x), f(y)))


def telescope(p, x, ground, h):
    tube = "M" + P(x - h * 0.12, ground - h * 0.6) + "L" + P(x + h * 0.55, ground - h * 1.05) + "L" + P(x + h * 0.62, ground - h * 0.93) + "L" + P(x - h * 0.05, ground - h * 0.45) + "Z"
    for dx in (-0.25, 0.0, 0.25):
        p.line("M" + P(x + h * 0.08, ground - h * 0.6) + "L" + P(x + h * dx, ground), "ink", max(2, h * 0.025))
    p.form(tube, "d", h, light=(0.4, 0.0))
    p.solid("M" + P(x + h * 0.5, ground - h * 1.07) + "L" + P(x + h * 0.6, ground - h * 1.13) + "L" + P(x + h * 0.7, ground - h * 0.95) + "L" + P(x + h * 0.6, ground - h * 0.89) + "Z", "a")
    p.disc(x + h * 0.08, ground - h * 0.6, h * 0.05, "b")


def microscope(p, x, ground, h):
    p.form(rrect_d(x - h * 0.32, ground - h * 0.1, h * 0.64, h * 0.1, h * 0.03), "ink", h)
    arm = "M" + P(x + h * 0.15, ground - h * 0.1) + "C" + P(x + h * 0.35, ground - h * 0.45) + " " + P(x + h * 0.25, ground - h * 0.75) + " " + P(x + h * 0.02, ground - h * 0.85) + "L" + P(x - h * 0.04, ground - h * 0.74) + "C" + P(x + h * 0.15, ground - h * 0.65) + " " + P(x + h * 0.2, ground - h * 0.45) + " " + P(x + h * 0.02, ground - h * 0.1) + "Z"
    p.form(arm, "d", h)
    p.s.group(lambda: p.form(rrect_d(x - h * 0.1, ground - h * 0.95, h * 0.16, h * 0.45, h * 0.04), "c", h), tf="rotate(-28 %s %s)" % (f(x), f(ground - h * 0.7)))
    p.form(rrect_d(x - h * 0.24, ground - h * 0.42, h * 0.42, h * 0.06, h * 0.02), "b", h)
    p.circle(x - h * 0.05, ground - h * 0.48, h * 0.04, "a")


def leaf_cell(p, x, y, r):
    """A plant cell: rounded wall, chloroplasts, a nucleus."""
    d = rrect_d(x - r, y - r * 0.75, r * 2, r * 1.5, r * 0.45)
    p.form(d, "leaf2", r * 2)
    p.solid(rrect_d(x - r * 0.88, y - r * 0.64, r * 1.76, r * 1.28, r * 0.38), "e", op=0.35)
    p.disc(x + r * 0.25, y - r * 0.1, r * 0.28, "d")
    p.circle(x + r * 0.3, y - r * 0.15, r * 0.1, "c")
    for k, (cx, cy) in enumerate(((-0.55, -0.35), (-0.3, 0.35), (0.6, 0.4), (-0.65, 0.25), (0.1, 0.45), (0.65, -0.4))):
        p.s.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (
            f(x + cx * r), f(y + cy * r), f(r * 0.16), f(r * 0.08), p.c("leaf"), k * 37, f(x + cx * r), f(y + cy * r)))


def leaf(p, x, y, length, angle, role="leaf", vein=True):
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * length * 0.32, math.cos(a) * length * 0.32
    m = (x + math.cos(a) * length * 0.45, y + math.sin(a) * length * 0.45)
    d = "M" + P(x, y) + "Q" + P(m[0] + nx, m[1] + ny) + " " + P(tx, ty) + "Q" + P(m[0] - nx, m[1] - ny) + " " + P(x, y) + "Z"
    p.form(d, role, length, light=(0.3, 0.1))
    if vein:
        p.detail("M" + P(x, y) + "Q" + P(m[0] + nx * 0.12, m[1] + ny * 0.12) + " " + P(tx - math.cos(a) * length * 0.1, ty - math.sin(a) * length * 0.1), "e", max(1, length * 0.012), 0.6)


def sprig(p, x, y, length, angle, leaves=5, role="leaf", curl=0.3):
    a = math.radians(angle)
    pts = []
    for k in range(7):
        t = k / 6
        bend = math.sin(t * math.pi * 0.9) * curl * length * 0.3
        pts.append((x + math.cos(a) * length * t - math.sin(a) * bend, y + math.sin(a) * length * t + math.cos(a) * bend))
    p.line(smooth(pts), role, max(1.4, length * 0.012))
    for k in range(leaves):
        t = 0.3 + 0.65 * k / max(1, leaves - 1)
        i = min(5, int(t * 6))
        u = t * 6 - i
        px, py = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u
        side = 1 if k % 2 == 0 else -1
        leaf(p, px, py, length * (0.28 - 0.1 * t), angle + side * 45, role if k % 2 else "leaf2", vein=False)


def flower(p, x, y, r, role="b", n=5, rot=0.0):
    """A cup flower (rhododendron, gurans) fanned upward; two tones alternate."""
    for k in range(n):
        a = math.radians(rot - 150 + 120 * k / max(1, n - 1))
        tx, ty = x + math.cos(a) * r, y + math.sin(a) * r
        nx, ny = -math.sin(a) * r * 0.42, math.cos(a) * r * 0.42
        d = "M" + P(x, y) + "Q" + P(x + (tx - x) * 0.6 + nx, y + (ty - y) * 0.6 + ny) + " " + P(tx, ty) + "Q" + P(x + (tx - x) * 0.6 - nx, y + (ty - y) * 0.6 - ny) + " " + P(x, y) + "Z"
        p.form(d, role, r * 1.4, shade=k % 2 == 1)
    p.circle(x, y + r * 0.08, r * 0.2, "leaf")


def stem_flower(p, x, y, h, angle, role="b", r=None):
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * h, y + math.sin(a) * h
    p.line("M" + P(x, y) + "Q" + P(x + math.cos(a) * h * 0.5 + 18 * math.sin(a), y + math.sin(a) * h * 0.5) + " " + P(tx, ty), "leaf", max(1.5, h * 0.012))
    flower(p, tx, ty, r or h * 0.2, role, rot=angle + 90)


def butterfly(p, x, y, size, rot=-20, wing="c", dark="d"):
    def draw():
        back = "M" + P(x, y) + "C" + P(x - size * 0.2, y - size * 0.9) + " " + P(x - size * 0.45, y - size * 0.9) + " " + P(x - size * 0.5, y - size * 0.4) + "C" + P(x - size * 0.5, y - size * 0.1) + " " + P(x - size * 0.2, y + size * 0.1) + " " + P(x, y) + "Z"
        up = "M" + P(x, y) + "C" + P(x - size * 0.3, y - size * 1.1) + " " + P(x + size * 0.9, y - size * 1.2) + " " + P(x + size * 0.75, y - size * 0.25) + "C" + P(x + size * 0.6, y) + " " + P(x + size * 0.2, y + size * 0.05) + " " + P(x, y) + "Z"
        lo = "M" + P(x, y) + "C" + P(x + size * 0.5, y + size * 0.05) + " " + P(x + size * 0.7, y + size * 0.45) + " " + P(x + size * 0.35, y + size * 0.6) + "C" + P(x + size * 0.1, y + size * 0.65) + " " + P(x - size * 0.05, y + size * 0.3) + " " + P(x, y) + "Z"
        p.solid(back, dark)
        p.form(lo, wing, size, shade=False)
        p.form(up, wing, size, shade=False)
        for k in range(4):
            t = 0.25 + k * 0.17
            p.detail("M" + P(x + size * 0.05, y - size * 0.05) + "Q" + P(x + size * t * 0.8, y - size * (0.9 - t * 0.4)) + " " + P(x + size * (0.25 + t * 0.6), y - size * (0.65 - t * 0.5)), "e", 1.1, 0.7)
        p.circle(x + size * 0.42, y - size * 0.62, size * 0.17, "e")
        p.circle(x + size * 0.42, y - size * 0.62, size * 0.1, "b")
        p.circle(x + size * 0.42, y - size * 0.62, size * 0.05, "a")
        p.line("M" + P(x - size * 0.05, y + size * 0.2) + "L" + P(x + size * 0.05, y - size * 0.25), dark, size * 0.08)
        p.line("M" + P(x + size * 0.05, y - size * 0.25) + "Q" + P(x + size * 0.4, y - size * 0.7) + " " + P(x + size * 0.9, y - size * 0.75), dark, 1.2)
    p.s.group(draw, tf="rotate(%s %s %s)" % (f(rot), f(x), f(y)))


# ---------------------------------------------------------------- maths, computing, commerce, world
def geometry(p, x, y, s):
    """A set square, a protractor and a compass laid together."""
    tri = poly((x - s * 0.5, y + s * 0.4), (x - s * 0.5, y - s * 0.5), (x + s * 0.45, y + s * 0.4))
    p.form(tri, "c", s, light=(0.2, 0.1))
    p.solid(poly((x - s * 0.36, y + s * 0.26), (x - s * 0.36, y - s * 0.15), (x + s * 0.05, y + s * 0.26)), "e", op=0.85 if p.look == "flat" else 0.5)
    pro = "M" + P(x - s * 0.05, y + s * 0.42) + "A%s %s 0 0 1 %s Z" % (f(s * 0.55), f(s * 0.55), P(x + s * 1.05, y + s * 0.42))
    p.form(pro, "a", s, light=(0.4, 0.0))
    for k in range(13):
        a = math.pi + k / 12 * math.pi
        cx, cy = x + s * 0.5, y + s * 0.42
        p.line("M" + P(cx + math.cos(a) * s * 0.55, cy + math.sin(a) * s * 0.55) + "L" + P(cx + math.cos(a) * s * (0.47 if k % 3 else 0.42), cy + math.sin(a) * s * (0.47 if k % 3 else 0.42)), "ink", 1.3, op=0.6)
    hx, hy = x + s * 0.95, y - s * 0.55
    p.line("M" + P(hx, hy) + "L" + P(hx - s * 0.28, y + s * 0.38), "ink", s * 0.035)
    p.line("M" + P(hx, hy) + "L" + P(hx + s * 0.25, y + s * 0.38), "d", s * 0.035)
    p.disc(hx, hy, s * 0.05, "b")


def numbers(p, x, y, size, glyphs="π √ ∑ ÷ ∞ =", role="d"):
    for k, g in enumerate(glyphs.split()):
        gx, gy = x + (k % 3) * size * 1.4 + (k // 3) * size * 0.5, y + (k // 3) * size * 1.3 + ((k * 7) % 3) * size * 0.2
        p.s.add('<text x="%s" y="%s" font-family="Georgia, \'Times New Roman\', serif" font-size="%s" fill="%s" opacity="0.85" font-style="italic">%s</text>' % (f(gx), f(gy), f(size), p.c(role), g))


def laptop(p, x, ground, w, code=True):
    h = w * 0.6
    screen = rrect_d(x - w / 2, ground - h - w * 0.05, w, h, w * 0.04)
    p.form(screen, "ink", w)
    p.solid(rrect_d(x - w / 2 + w * 0.04, ground - h - w * 0.01, w * 0.92, h - w * 0.08, w * 0.02), "d")
    if code:
        rows = [(0.06, 0.4, "a"), (0.12, 0.55, "g"), (0.12, 0.3, "b"), (0.18, 0.45, "e"), (0.06, 0.25, "c"), (0.12, 0.5, "a"), (0.18, 0.3, "g")]
        for k, (ind, ln, role) in enumerate(rows):
            yy = ground - h + w * 0.05 + k * h * 0.11
            p.solid(rrect_d(x - w / 2 + w * (0.08 + ind), yy, w * ln, h * 0.045, h * 0.02), role, op=0.9)
    base = "M" + P(x - w * 0.62, ground) + "L" + P(x - w * 0.52, ground - w * 0.05) + "L" + P(x + w * 0.52, ground - w * 0.05) + "L" + P(x + w * 0.62, ground) + "Z"
    p.form(base, "c", w, light=(0.3, 0.0))


def coins_chart(p, x, ground, w):
    bars = (0.35, 0.55, 0.45, 0.8, 1.0)
    bw = w / len(bars) * 0.62
    for k, v in enumerate(bars):
        bx = x - w / 2 + k * w / len(bars)
        p.form(rrect_d(bx, ground - w * 0.8 * v, bw, w * 0.8 * v, bw * 0.15), ("c", "g", "c", "b", "a")[k], bw * 2, light=(0.3, 0.0))
    pts = [(x - w / 2 + k * w / len(bars) + bw / 2, ground - w * 0.8 * v - w * 0.12) for k, v in enumerate(bars)]
    p.line(smooth(pts), "d", max(2, w * 0.02))
    tip = pts[-1]
    p.solid(poly((tip[0] + w * 0.06, tip[1] - w * 0.06), (tip[0] - w * 0.02, tip[1] - w * 0.04), (tip[0] + w * 0.04, tip[1] + w * 0.03)), "d")
    for k in range(4):
        cx, cy = x + w * 0.62, ground - k * w * 0.06
        p.form("M" + P(cx - w * 0.14, cy) + "A%s %s 0 0 0 %s" % (f(w * 0.14), f(w * 0.04), P(cx + w * 0.14, cy)) + "L" + P(cx + w * 0.14, cy - w * 0.045) + "A%s %s 0 0 0 %s Z" % (f(w * 0.14), f(w * 0.04), P(cx - w * 0.14, cy - w * 0.045)), "a", w * 0.3, shade=False)
        p.line("M" + P(cx - w * 0.14, cy) + "A%s %s 0 0 0 %s" % (f(w * 0.14), f(w * 0.04), P(cx + w * 0.14, cy)), "b", 1.3, op=0.7)
    p.s.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(x + w * 0.62), f(ground - w * 0.225), f(w * 0.14), f(w * 0.04), p.c("h")))


def globe(p, x, y, r):
    p.form(circle_d(x, y, r), "g", r * 2, light=(0.3, 0.2))
    cid = p.s.clip(circle_d(x, y, r))

    def lands():
        for (cx, cy, rx, ry, rot) in ((-0.35, -0.3, 0.42, 0.25, 20), (0.35, 0.05, 0.3, 0.45, -15), (-0.2, 0.5, 0.25, 0.15, 0), (0.55, -0.55, 0.2, 0.12, 30)):
            p.s.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (
                f(x + cx * r), f(y + cy * r), f(rx * r), f(ry * r), p.c("leaf2"), rot, f(x + cx * r), f(y + cy * r)))
        for k in range(1, 4):
            p.detail('M%s %sQ%s %s %s %s' % (f(x - r), f(y - r + k * r / 2), f(x), f(y - r + k * r / 2 + r * 0.15), f(x + r), f(y - r + k * r / 2)), "e", 1.2, 0.5)
    p.s.group(lands, clip=cid)
    p.line("M" + P(x - r * 1.15, y + r * 1.25) + "A%s %s 0 0 0 %s" % (f(r * 1.25), f(r * 1.25), P(x + r * 1.0, y - r * 1.2)), "ink", max(2, r * 0.05), op=0.7)
    p.form(rrect_d(x - r * 0.45, y + r * 1.28, r * 0.9, r * 0.12, r * 0.05), "ink", r)


def heart_pulse(p, x, y, s):
    d = ("M" + P(x, y + s * 0.42) + "C" + P(x - s * 0.7, y - s * 0.05) + " " + P(x - s * 0.5, y - s * 0.62) + " " + P(x, y - s * 0.3) +
         "C" + P(x + s * 0.5, y - s * 0.62) + " " + P(x + s * 0.7, y - s * 0.05) + " " + P(x, y + s * 0.42) + "Z")
    p.glow(x, y, s * 1.1, "f", 0.5)
    p.form(d, "f", s, light=(0.3, 0.1))
    p.line("M" + P(x - s * 1.2, y) + "L" + P(x - s * 0.4, y) + "L" + P(x - s * 0.25, y - s * 0.25) + "L" + P(x - s * 0.05, y + s * 0.25) + "L" + P(x + s * 0.12, y - s * 0.12) + "L" + P(x + s * 0.25, y) + "L" + P(x + s * 1.2, y), "e", max(2, s * 0.05))


def school(p, x, ground, w, flag=True):
    """A Nepali school: whitewashed walls, a tiered pagoda roof, a door and windows, a flag."""
    h = w * 0.42
    wall = rrect_d(x - w / 2, ground - h, w, h, 4)
    p.form(wall, "e", w, light=(0.25, 0.0))
    for tier, (ww, yy, hh) in enumerate(((1.15, h, w * 0.14), (0.7, h + w * 0.17, w * 0.12))):
        roof = poly((x - w * ww / 2, ground - yy), (x - w * ww * 0.36, ground - yy - hh), (x + w * ww * 0.36, ground - yy - hh), (x + w * ww / 2, ground - yy))
        p.form(roof, "b", w, light=(0.3, 0.0))
        p.line("M" + P(x - w * ww / 2, ground - yy) + "L" + P(x + w * ww / 2, ground - yy), "d", 2, op=0.6)
    p.form(rrect_d(x - w * 0.18, ground - h - w * 0.17, w * 0.36, w * 0.17, 2), "e", w, shade=False)
    p.line("M" + P(x, ground - h - w * 0.31) + "L" + P(x, ground - h - w * 0.4), "d", 2)
    p.circle(x, ground - h - w * 0.41, 4, "a")
    p.form(rrect_d(x - w * 0.07, ground - h * 0.62, w * 0.14, h * 0.62, w * 0.06), "d", w)
    for sx in (-1, 1):
        for k in range(2):
            wx = x + sx * w * (0.22 + k * 0.16) - w * 0.05
            p.solid(rrect_d(wx, ground - h * 0.72, w * 0.1, h * 0.36, 2), "c")
            p.line("M" + P(wx + w * 0.05, ground - h * 0.72) + "L" + P(wx + w * 0.05, ground - h * 0.36), "e", 1.5)
    if flag:
        fx = x + w * 0.72
        p.line("M" + P(fx, ground) + "L" + P(fx, ground - w * 0.75), "ink", 2.5)
        # Nepal's flag: two stacked pennants, crimson with a blue border
        fl = poly((fx, ground - w * 0.75), (fx + w * 0.16, ground - w * 0.64), (fx + w * 0.06, ground - w * 0.64), (fx + w * 0.16, ground - w * 0.52), (fx, ground - w * 0.52))
        p.s.path(fl, "#c8102e", stroke="#1f3f8f", sw=2.5)
        p.circle(fx + w * 0.045, ground - w * 0.6, w * 0.018, "e")


def prayer_flags(p, x0, y0, x1, y1, n=12, sag=30):
    roles = ("c", "e", "f", "leaf", "a")
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + math.sin(t * math.pi) * sag))
    p.line(smooth(pts), "ink", 1.5, op=0.7)
    for k in range(n):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        fw = (bx - ax) * 0.7
        p.solid(poly((mx - fw / 2, my), (mx + fw / 2, my + (by - ay) * 0.35), (mx + fw / 2 + 2, my + fw * 1.1), (mx - fw / 2 + 1, my + fw * 1.05)), roles[k % 5])


def mountain_range(p, base, peaks, role=None, snow=True):
    p.mountains(base, peaks, role or ("dark" if p.look == "riso" else "c"), snow)


def lantern(p, x, y, h):
    p.glow(x, y, h * 1.4, "a", 0.9)
    p.line("M" + P(x, y - h * 0.62) + "L" + P(x, y - h * 0.9), "ink", 2)
    p.form(rrect_d(x - h * 0.22, y - h * 0.6, h * 0.44, h * 0.1, 3), "ink", h)
    p.form(rrect_d(x - h * 0.3, y - h * 0.5, h * 0.6, h * 0.82, h * 0.2), "a", h, light=(0.4, 0.3))
    for sx in (-0.16, 0, 0.16):
        p.line("M" + P(x + h * sx, y - h * 0.48) + "L" + P(x + h * sx, y + h * 0.3), "b", 1.6, op=0.6)
    p.form(rrect_d(x - h * 0.22, y + h * 0.32, h * 0.44, h * 0.1, 3), "ink", h)


def key(p, x, y, s, angle=-30):
    """An old key: a ring bow (with its hole), a shaft and two bits."""
    def draw():
        bow = circle_d(x - s * 0.42, y, s * 0.28) + circle_d(x - s * 0.42, y, s * 0.13)
        p.s.add('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (bow, p.c("a")))
        p.form(rrect_d(x - s * 0.18, y - s * 0.065, s * 0.95, s * 0.13, s * 0.05), "a", s, light=(0.3, 0.0))
        p.form(rrect_d(x + s * 0.5, y + s * 0.04, s * 0.09, s * 0.2, s * 0.02), "a", s, shade=False)
        p.form(rrect_d(x + s * 0.66, y + s * 0.04, s * 0.09, s * 0.14, s * 0.02), "a", s, shade=False)
        p.line(circle_d(x - s * 0.42, y, s * 0.28), "b", max(1.5, s * 0.015), op=0.6)
        p.circle(x - s * 0.2, y, s * 0.06, "b")
    p.s.group(draw, tf="rotate(%s %s %s)" % (f(angle), f(x), f(y)))


def rosette(p, x, y, r, role="a", check=True):
    """A verified seal: a scalloped badge with a tick and two ribbon tails."""
    for sx in (-1, 1):
        p.form(poly((x + sx * r * 0.15, y + r * 0.5), (x + sx * r * 0.55, y + r * 1.5), (x + sx * r * 0.32, y + r * 1.38), (x + sx * r * 0.2, y + r * 1.62), (x - sx * r * 0.1, y + r * 0.6)), "b", r)
    pts = []
    for k in range(32):
        a = k / 32 * 2 * math.pi
        rr = r * (1 if k % 2 == 0 else 0.88)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    p.form(poly(*pts), role, r * 2, light=(0.3, 0.2))
    p.solid(circle_d(x, y, r * 0.7), "e" if p.look == "flat" else "h", op=0.9)
    if check:
        p.line("M" + P(x - r * 0.32, y + r * 0.02) + "L" + P(x - r * 0.08, y + r * 0.26) + "L" + P(x + r * 0.36, y - r * 0.24), "d", r * 0.14)


def shield(p, x, y, s, role="c"):
    d = "M" + P(x, y - s * 0.6) + "L" + P(x + s * 0.5, y - s * 0.4) + "Q" + P(x + s * 0.5, y + s * 0.3) + " " + P(x, y + s * 0.65) + "Q" + P(x - s * 0.5, y + s * 0.3) + " " + P(x - s * 0.5, y - s * 0.4) + "Z"
    p.form(d, role, s)
    p.line("M" + P(x - s * 0.18, y) + "L" + P(x - s * 0.02, y + s * 0.16) + "L" + P(x + s * 0.22, y - s * 0.16), "e", s * 0.08)


def bubble(p, x, y, w, h, role="e", tail=-1, dots=True):
    d = rrect_d(x - w / 2, y - h / 2, w, h, h * 0.45)
    t = poly((x + tail * w * 0.15, y + h * 0.4), (x + tail * w * 0.32, y + h * 0.8), (x + tail * w * 0.02, y + h * 0.45))
    p.form(t, role, w, shade=False)
    p.form(d, role, w, light=(0.3, 0.1), shade=False)
    p.line(d, "ink", max(1.2, w * 0.008), op=0.35)
    if dots:
        for k in (-1, 0, 1):
            p.circle(x + k * w * 0.2, y, h * 0.1, "d")


def bell(p, x, y, s, asleep=True):
    d = "M" + P(x - s * 0.42, y + s * 0.3) + "C" + P(x - s * 0.4, y - s * 0.1) + " " + P(x - s * 0.38, y - s * 0.5) + " " + P(x, y - s * 0.5) + "C" + P(x + s * 0.38, y - s * 0.5) + " " + P(x + s * 0.4, y - s * 0.1) + " " + P(x + s * 0.42, y + s * 0.3) + "Q" + P(x, y + s * 0.4) + " " + P(x - s * 0.42, y + s * 0.3) + "Z"
    p.form(d, "a", s)
    p.disc(x, y + s * 0.42, s * 0.09, "b")
    p.circle(x, y - s * 0.55, s * 0.06, "a")
    face(p, x, y - s * 0.05, s * 0.32, "sleep" if asleep else "smile")
    if asleep:
        for k, (zx, zy, zs) in enumerate(((0.5, -0.55, 0.16), (0.68, -0.78, 0.12))):
            p.s.add('<text x="%s" y="%s" font-family="Poppins, sans-serif" font-weight="700" font-size="%s" fill="%s">z</text>' % (f(x + s * zx), f(y + s * zy), f(s * zs * 1.6), p.c("d")))


def cloud(p, x, y, w, role="e", op=None):
    d = ("M" + P(x - w * 0.5, y) + "C" + P(x - w * 0.55, y - w * 0.18) + " " + P(x - w * 0.32, y - w * 0.28) + " " + P(x - w * 0.18, y - w * 0.2) +
         "C" + P(x - w * 0.12, y - w * 0.42) + " " + P(x + w * 0.2, y - w * 0.42) + " " + P(x + w * 0.22, y - w * 0.2) +
         "C" + P(x + w * 0.4, y - w * 0.26) + " " + P(x + w * 0.56, y - w * 0.12) + " " + P(x + w * 0.5, y) + "Z")
    p.form(d, role, w, light=(0.3, 0.0), shade=False)


def rain(p, x, y, w, n=7):
    for k in range(n):
        dx = x - w * 0.4 + k * w * 0.8 / (n - 1)
        dy = y + (k % 3) * w * 0.08
        p.line("M" + P(dx, dy) + "L" + P(dx - w * 0.04, dy + w * 0.12), "c", max(2, w * 0.025))


def magnifier(p, x, y, r):
    p.line("M" + P(x + r * 0.7, y + r * 0.7) + "L" + P(x + r * 1.5, y + r * 1.5), "ink", r * 0.22)
    p.form(circle_d(x, y, r), "c", r * 2, shade=False)
    p.solid(circle_d(x, y, r * 0.78), "e", op=0.8)
    p.detail("M" + P(x - r * 0.45, y - r * 0.1) + "Q" + P(x - r * 0.4, y - r * 0.45) + " " + P(x - r * 0.05, y - r * 0.5), "e", r * 0.08, 0.9)


def ribbon_bookmark(p, x, y, w, h, role="f"):
    d = "M" + P(x - w / 2, y) + "L" + P(x + w / 2, y) + "L" + P(x + w / 2, y + h) + "L" + P(x, y + h * 0.8) + "L" + P(x - w / 2, y + h) + "Z"
    p.form(d, role, w * 2)


def tray(p, x, y, w, role="c"):
    d = "M" + P(x - w / 2, y - w * 0.12) + "L" + P(x - w * 0.36, y + w * 0.18) + "L" + P(x + w * 0.36, y + w * 0.18) + "L" + P(x + w / 2, y - w * 0.12) + "L" + P(x + w * 0.2, y - w * 0.12) + "Q" + P(x, y + w * 0.02) + " " + P(x - w * 0.2, y - w * 0.12) + "Z"
    p.form(d, role, w)
    p.line("M" + P(x, y - w * 0.55) + "L" + P(x, y - w * 0.12), "d", w * 0.06)
    p.line("M" + P(x - w * 0.12, y - w * 0.24) + "L" + P(x, y - w * 0.1) + "L" + P(x + w * 0.12, y - w * 0.24), "d", w * 0.06)


def envelope(p, x, y, w, role="page"):
    h = w * 0.66
    d = rrect_d(x - w / 2, y - h / 2, w, h, w * 0.04)
    p.form(d, role, w, shade=False)
    p.line(d, "ink", 1.3, op=0.4)
    p.form(poly((x - w / 2, y - h / 2), (x, y + h * 0.08), (x + w / 2, y - h / 2)), "e" if p.look == "flat" else "h", w, shade=False)
    p.line("M" + P(x - w / 2, y - h / 2) + "L" + P(x, y + h * 0.08) + "L" + P(x + w / 2, y - h / 2), "ink", 1.3, op=0.4)
    p.disc(x, y + h * 0.05, w * 0.07, "f")
