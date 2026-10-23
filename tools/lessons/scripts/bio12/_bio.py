"""Drawing helpers for the Class 12 Biology lessons: cells, tissues, conducting elements and
transverse sections built from real cell geometry, plus the captions, cards and tables the
lessons share. One colour per tissue across every unit (see the constants below)."""
import numpy as np
from manim import *

from kit import M, T, para, th

XYL = "#4CC9F0"
PHL = "#F472B6"
CAMB = "#FFB547"
CORK = "#B9875A"
SCL = "#FF8C69"
COL = "#C5F05C"
PAR = "#7BE495"
PARF = "#1C3326"
EPI = "#2EC4B6"
ENDO = "#F6E3A1"
PERI = "#B8A1FF"
PITH = "#8189B0"
CHL = "#57D163"
WATER = "#7FD8FF"
FOOD = "#FFC46B"


def R(seed):
    return np.random.default_rng(seed)


def blob(c, r, n=8, jit=0.1, seed=0, stroke=PAR, fill=PARF, sw=1.6, fo=1.0, round_=True):
    rg = R(seed)
    a0 = rg.uniform(0, TAU)
    pts = [np.array(c, dtype=float) + r * (1 + rg.uniform(-jit, jit)) * np.array([np.cos(a), np.sin(a), 0])
           for a in a0 + np.linspace(0, TAU, n, endpoint=False)]
    p = Polygon(*pts, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=fo)
    if round_:
        p.round_corners(r * 0.4)
    return p


def hex_centres(w, h, r, center=ORIGIN, jit=0.0, seed=0, keep=None):
    rg = R(seed)
    dx, dy = 2 * r, np.sqrt(3) * r
    out = []
    y = -h / 2
    row = 0
    while y <= h / 2 + 1e-6:
        x = -w / 2 + (r if row % 2 else 0)
        while x <= w / 2 + 1e-6:
            p = np.array([x, y, 0]) + np.array([rg.uniform(-jit, jit), rg.uniform(-jit, jit), 0])
            if keep is None or keep(p):
                out.append(p + np.array(center, dtype=float))
            x += dx
        y += dy
        row += 1
    return out


def ring_centres(r, cell, phase=0.0):
    n = max(6, int(round(TAU * r / cell)))
    return [np.array([r * np.cos(phase + TAU * k / n), r * np.sin(phase + TAU * k / n), 0]) for k in range(n)], n


# ------------------------------------------------------------------ simple tissues
def parenchyma(w=3.0, h=2.0, r=0.28, center=ORIGIN, seed=1, nuclei=True, chloro=False, air=False):
    g = VGroup()
    rg = R(seed)
    cs = hex_centres(w, h, r, center, jit=r * 0.12, seed=seed)
    for i, c in enumerate(cs):
        rr = r * (0.62 if air else 0.9)
        g.add(blob(c, rr, n=9, jit=0.12, seed=seed * 1000 + i, fill=PARF if not chloro else "#173A1E"))
        if chloro:
            for k in range(5):
                a = rg.uniform(0, TAU)
                g.add(Ellipse(width=r * 0.32, height=r * 0.18, stroke_width=0, fill_color=CHL, fill_opacity=0.95)
                      .rotate(a).move_to(c + rr * 0.62 * np.array([np.cos(a), np.sin(a), 0])))
        if nuclei:
            a = rg.uniform(0, TAU)
            g.add(Dot(c + rr * 0.35 * np.array([np.cos(a), np.sin(a), 0]), radius=r * 0.13, color="#B6F5C4"))
    return g


def collenchyma(w=3.0, h=2.0, r=0.28, center=ORIGIN, seed=2, kind="angular"):
    g = VGroup()
    cs = hex_centres(w, h, r * 1.0, center, seed=seed)
    walls, thick = VGroup(), VGroup()
    for i, c in enumerate(cs):
        hx = RegularPolygon(6, radius=r * 1.155, stroke_color=COL, stroke_width=1.6, fill_color="#26331A", fill_opacity=1).rotate(PI / 6).move_to(c)
        walls.add(hx)
        vs = hx.get_vertices()
        if kind == "angular":
            for v in vs:
                thick.add(Dot(v, radius=r * 0.26, color=COL))
        elif kind == "lamellar":
            thick.add(Line(vs[0], vs[1], stroke_width=7, color=COL), Line(vs[3], vs[4], stroke_width=7, color=COL))
        g.add(Dot(c, radius=r * 0.14, color="#E4FFB0"))
    if kind == "lacunar":
        for i, c in enumerate(cs):
            vs = walls[i].get_vertices()
            for v in vs[::2]:
                thick.add(Circle(radius=r * 0.22, stroke_color=COL, stroke_width=5, fill_color=th.BG, fill_opacity=1).move_to(v))
    return VGroup(walls, thick, *g)


def sclerenchyma(w=3.0, h=2.0, r=0.28, center=ORIGIN, seed=3, pits=True):
    g = VGroup()
    for c in hex_centres(w, h, r, center, seed=seed):
        hx = RegularPolygon(6, radius=r * 1.155, stroke_color="#FFC2AE", stroke_width=1.2, fill_color=SCL, fill_opacity=0.95).rotate(PI / 6).move_to(c)
        lum = RegularPolygon(6, radius=r * 0.33, stroke_width=0, fill_color=th.BG, fill_opacity=1).rotate(PI / 6).move_to(c)
        g.add(hx, lum)
        if pits:
            for k in range(3):
                a = TAU * k / 3 + 0.4
                d = np.array([np.cos(a), np.sin(a), 0])
                g.add(Line(c + d * r * 0.3, c + d * r * 0.85, stroke_width=1.4, color=th.BG))
    return g


def meristem(w=3.0, h=2.0, s=0.34, center=ORIGIN, seed=4):
    g = VGroup()
    rg = R(seed)
    nx, ny = int(w / s), int(h / s)
    for i in range(nx):
        for j in range(ny):
            c = np.array(center, dtype=float) + np.array([(i - (nx - 1) / 2) * s, (j - (ny - 1) / 2) * s, 0])
            g.add(Square(side_length=s, stroke_color="#C9B8FF", stroke_width=1.4, fill_color="#3B2F6B", fill_opacity=1).move_to(c))
            g.add(Dot(c + rg.uniform(-0.03, 0.03, 3) * [1, 1, 0], radius=s * 0.24, color="#E6DCFF"))
    return g


def fibre(length=3.0, w=0.22, center=ORIGIN, color=SCL):
    pts = [[-length / 2, 0, 0], [0, w / 2, 0], [length / 2, 0, 0], [0, -w / 2, 0]]
    outer = VMobject(stroke_color="#FFC2AE", stroke_width=1.5, fill_color=color, fill_opacity=0.95)
    outer.set_points_smoothly([*pts, pts[0]])
    lum = Line([-length * 0.38, 0, 0], [length * 0.38, 0, 0], stroke_width=1.6, color=th.BG)
    return VGroup(outer, lum).move_to(center)


def sclereid(r=0.7, center=ORIGIN, rings=5, seed=5):
    rg = R(seed)
    g = VGroup(blob(ORIGIN, r, n=9, jit=0.12, seed=seed, stroke="#FFC2AE", fill=SCL, sw=2))
    for k in range(1, rings):
        g.add(blob(ORIGIN, r * (1 - k * 0.15), n=9, jit=0.1, seed=seed, stroke="#FFD9CC", fill=SCL, sw=1, fo=0.0))
    g.add(Circle(radius=r * 0.16, stroke_width=0, fill_color=th.BG, fill_opacity=1))
    for k in range(7):
        a = TAU * k / 7 + rg.uniform(-0.2, 0.2)
        g.add(Line(r * 0.14 * np.array([np.cos(a), np.sin(a), 0]), r * 0.9 * np.array([np.cos(a), np.sin(a), 0]), stroke_width=1.6, color=th.BG))
    return g.move_to(center)


# ------------------------------------------------------------------ conducting elements
def vessel(h=4.0, w=0.7, center=ORIGIN, kind="pitted", segs=4, color=XYL, open_ends=True):
    g = VGroup()
    x0, x1 = -w / 2, w / 2
    g.add(Line([x0, -h / 2, 0], [x0, h / 2, 0], color=color, stroke_width=4), Line([x1, -h / 2, 0], [x1, h / 2, 0], color=color, stroke_width=4))
    sh = h / segs
    for k in range(1, segs):
        y = -h / 2 + k * sh
        if open_ends:
            g.add(Line([x0, y, 0], [x0 + w * 0.18, y, 0], color=color, stroke_width=3), Line([x1 - w * 0.18, y, 0], [x1, y, 0], color=color, stroke_width=3))
        else:
            g.add(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3))
    if kind == "annular":
        for y in np.arange(-h / 2 + 0.2, h / 2, 0.45):
            g.add(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3.5))
    elif kind == "spiral":
        ys = np.linspace(-h / 2, h / 2, 400)
        g.add(VMobject(stroke_color=color, stroke_width=3.2).set_points_as_corners(
            [[x0 + (x1 - x0) * (0.5 + 0.5 * np.sin(y * 9)), y, 0] for y in ys]))
    elif kind == "scalariform":
        for y in np.arange(-h / 2 + 0.1, h / 2, 0.16):
            g.add(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2.2))
    elif kind == "reticulate":
        for y in np.arange(-h / 2, h / 2, 0.3):
            g.add(Line([x0, y, 0], [x1, y + 0.3, 0], color=color, stroke_width=2), Line([x1, y, 0], [x0, y + 0.3, 0], color=color, stroke_width=2))
    elif kind == "pitted":
        for y in np.arange(-h / 2 + 0.15, h / 2, 0.24):
            for x in np.linspace(x0 + 0.14, x1 - 0.14, 3):
                g.add(Ellipse(width=0.1, height=0.06, stroke_color=color, stroke_width=1.6).move_to([x, y, 0]))
    return g.move_to(center)


def tracheid(h=3.6, w=0.42, center=ORIGIN, color=XYL):
    outer = VMobject(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.08)
    outer.set_points_smoothly([[0, h / 2, 0], [w / 2, h * 0.3, 0], [w / 2, -h * 0.3, 0], [0, -h / 2, 0], [-w / 2, -h * 0.3, 0], [-w / 2, h * 0.3, 0], [0, h / 2, 0]])
    pits = VGroup()
    for y in np.linspace(-h * 0.3, h * 0.3, 7):
        pits.add(VGroup(Circle(radius=0.07, stroke_color=color, stroke_width=1.6), Dot([0, 0, 0], radius=0.025, color=color)).move_to([0, y, 0]))
    return VGroup(outer, pits).move_to(center)


def sieve_tube(h=4.0, w=0.7, center=ORIGIN, segs=3):
    g = VGroup()
    x0, x1 = -w / 2, w / 2
    g.add(Rectangle(width=w, height=h, stroke_color=PHL, stroke_width=3.5, fill_color=PHL, fill_opacity=0.1))
    sh = h / segs
    for k in range(1, segs):
        y = -h / 2 + k * sh
        g.add(DashedLine([x0, y, 0], [x1, y, 0], color=PHL, stroke_width=4, dash_length=0.06, dashed_ratio=0.55))
    for k in range(segs):
        y = -h / 2 + (k + 0.5) * sh
        g.add(Line([x0 + 0.06, y - sh * 0.4, 0], [x0 + 0.06, y + sh * 0.4, 0], color=PHL, stroke_width=2, stroke_opacity=0.5))
    comp = VGroup()
    for k in range(segs):
        y = -h / 2 + (k + 0.5) * sh
        cc = RoundedRectangle(corner_radius=0.06, width=0.24, height=sh * 0.92, stroke_color="#FFB3D9", stroke_width=2.2, fill_color="#5A2246", fill_opacity=1).move_to([x1 + 0.14, y, 0])
        comp.add(cc, Dot([x1 + 0.14, y, 0], radius=0.07, color="#FFD6EC"))
    g.add(comp)
    return g.move_to(center), comp


class Flow(VGroup):
    """Dots carried along a straight segment a -> b (or both ways when twoway)."""

    def __init__(self, a, b, n=8, color=WATER, r=0.05, speed=0.6, twoway=False, width=0.0, seed=7):
        super().__init__()
        rg = R(seed)
        self.a, self.b = np.array(a, dtype=float), np.array(b, dtype=float)
        self.L = np.linalg.norm(self.b - self.a)
        u = (self.b - self.a) / self.L
        self.perp = np.array([-u[1], u[0], 0])
        self.speed = speed
        self.st = []
        for k in range(n):
            d = Dot(radius=r, color=color)
            self.st.append([k / n, (1 if not twoway or k % 2 == 0 else -1), rg.uniform(-width / 2, width / 2)])
            self.add(d)
        self._place()
        self.add_updater(lambda m, dt: m._step(dt))

    def _place(self):
        for d, (s, _, o) in zip(self.submobjects, self.st):
            d.move_to(self.a + (self.b - self.a) * s + self.perp * o)
            d.set_opacity(min(1, 6 * min(s, 1 - s)) if 0 <= s <= 1 else 0)

    def _step(self, dt):
        for st in self.st:
            st[0] = (st[0] + st[1] * dt * self.speed / self.L) % 1.0
        self._place()


# ------------------------------------------------------------------ transverse sections
def cell_ring(r, cell, stroke, fill, sw=1.4, phase=0.0, squash=0.85, shape="round"):
    cs, n = ring_centres(r, cell, phase)
    g = VGroup()
    for k, c in enumerate(cs):
        ang = np.arctan2(c[1], c[0])
        if shape == "rect":
            m = RoundedRectangle(corner_radius=cell * 0.15, width=cell * 0.95, height=cell * squash, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1)
            m.rotate(ang + PI / 2).move_to(c)
        else:
            m = Ellipse(width=cell * 0.95, height=cell * squash, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1).rotate(ang + PI / 2).move_to(c)
        g.add(m)
    return g


def ground_disc(r_out, r_in, cell, stroke=PAR, fill=PARF, sw=1.2, seed=11):
    g = VGroup()
    r = r_out
    k = 0
    while r > r_in + cell * 0.4:
        g.add(*cell_ring(r, cell, stroke, fill, sw=sw, phase=k * 0.37, squash=0.92))
        r -= cell * 0.92
        k += 1
    if r_in <= 0:
        g.add(Circle(radius=max(r, cell * 0.5), stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1))
    return g


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class RootTS(VGroup):
    """Primary root in transverse section. arms = number of xylem groups (2-6 dicot, many monocot)."""

    def __init__(self, R=2.7, arms=4, monocot=False, hairs=True, cell=0.2):
        super().__init__()
        self.R = R
        stele = 1.35 if monocot else 0.95
        epi = cell_ring(R, cell, EPI, "#163B38", sw=1.4, shape="rect")
        hair = VGroup()
        if hairs:
            for k in range(0, len(epi), 9):
                a = np.arctan2(*epi[k].get_center()[[1, 0]])
                base = polar(R + cell * 0.4, a)
                pts = [base + polar(t, a) + polar(0.06 * np.sin(t * 8), a + PI / 2) for t in np.linspace(0, 0.75, 12)]
                hair.add(VMobject(stroke_color=EPI, stroke_width=2.4).set_points_smoothly(pts))
        cortex = ground_disc(R - cell * 1.0, stele + 0.15, cell * 1.25)
        endo, endo_n = cell_ring(stele + 0.06, 0.17, ENDO, "#3D3820", sw=1.6, shape="rect"), None
        casp = VGroup()
        cs, n = ring_centres(stele + 0.06, 0.17)
        passage_angles = [TAU * k / arms for k in range(arms)]
        for k in range(n):
            a = TAU * (k + 0.5) / n
            near = min(abs((a - pa + PI) % TAU - PI) for pa in passage_angles)
            if near > 0.12:
                casp.add(Dot(polar(stele + 0.06, a), radius=0.028, color="#FF9F43"))
        peri = cell_ring(stele - 0.1, 0.14, PERI, "#2E2650", sw=1.2)
        xyl, phl, conj = VGroup(), VGroup(), VGroup()
        core = stele - 0.22
        if monocot:
            pith = ground_disc(core - 0.42, 0, 0.18, stroke=PITH, fill="#22284A")
            for k in range(arms):
                a = TAU * k / arms
                xyl.add(Circle(radius=0.075, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.25).move_to(polar(core - 0.06, a)))
                xyl.add(Circle(radius=0.035, stroke_color=XYL, stroke_width=1.6).move_to(polar(core + 0.06, a)))
                phl.add(Circle(radius=0.07, stroke_width=0, fill_color=PHL, fill_opacity=0.85).move_to(polar(core - 0.02, a + PI / arms)))
            for c in ring_centres(core - 0.2, 0.09)[0]:
                conj.add(Dot(c, radius=0.03, color=SCL))
        else:
            pith = VGroup()
            for k in range(arms):
                a = TAU * k / arms
                for j, (rr, sz) in enumerate([(0.12, 0.12), (0.33, 0.1), (0.52, 0.075), (0.68, 0.05)]):
                    if rr < core:
                        xyl.add(Circle(radius=sz, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.25).move_to(polar(rr, a)))
                b = a + PI / arms
                for d in [0, 0.12, -0.12]:
                    phl.add(Circle(radius=0.06, stroke_width=0, fill_color=PHL, fill_opacity=0.85).move_to(polar(core - 0.12 - abs(d) * 0.5, b + d * 0.5)))
            xyl.add(Circle(radius=0.13, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.25))
        self.parts = dict(epi=epi, hairs=hair, cortex=cortex, endo=endo, casp=casp, peri=peri, xylem=xyl, phloem=phl, pith=pith, conj=conj)
        self.add(cortex, pith, conj, endo, casp, peri, phl, xyl, epi, hair)


def stem_bundle(r_mid, a, width=0.55, depth=0.85, cap=True):
    """Dicot collateral open bundle at angle a: phloem out, cambium, xylem in (endarch)."""
    u = polar(1, a)
    v = polar(1, a + PI / 2)
    out_r = r_mid + depth / 2
    in_r = r_mid - depth / 2
    back = Polygon(u * (in_r - 0.02) + v * width * 0.22, u * (out_r + 0.02) + v * width * 0.62, u * (out_r + 0.02) - v * width * 0.62, u * (in_r - 0.02) - v * width * 0.22,
                   stroke_color=th.FAINT, stroke_width=1.2, fill_color="#171329", fill_opacity=1)
    back.round_corners(0.06)
    ph = VGroup(*[Circle(radius=0.055, stroke_width=0, fill_color=PHL, fill_opacity=0.9).move_to(u * (r_mid + 0.15 + 0.11 * (j % 2)) + v * (i - 2) * 0.1)
                  for i in range(5) for j in range(2)])
    cb = Line(u * r_mid + v * (-width / 2), u * r_mid + v * (width / 2), color=CAMB, stroke_width=5)
    xy = VGroup()
    for k, (rr, sz) in enumerate([(r_mid - 0.12, 0.085), (r_mid - 0.27, 0.07), (r_mid - 0.4, 0.05)]):
        n = 3 - k
        for i in range(n):
            xy.add(Circle(radius=sz, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.25).move_to(u * rr + v * (i - (n - 1) / 2) * 0.19))
    capm = VGroup()
    if cap:
        capm = Polygon(u * (out_r - 0.05) + v * (width * 0.5), u * (out_r + 0.14) + v * (width * 0.2), u * (out_r + 0.14) - v * (width * 0.2), u * (out_r - 0.05) - v * (width * 0.5),
                       stroke_width=0, fill_color=SCL, fill_opacity=0.9)
        capm.round_corners(0.05)
    return VGroup(ph, cb, xy, capm, back)


class DicotStemTS(VGroup):
    def __init__(self, R=2.7, n=8, cell=0.2, ring=None):
        super().__init__()
        ring = ring or R * 0.48
        epi = cell_ring(R, cell * 0.8, EPI, "#163B38", sw=1.3, shape="rect")
        cut = Circle(radius=R + cell * 0.45, stroke_color="#BFF5EF", stroke_width=3.5)
        hyp = VGroup()
        for k in range(2):
            rr = R - cell * (0.85 + 0.75 * k)
            ring_ = cell_ring(rr, cell * 0.75, COL, "#26331A", sw=1.2, phase=k * 0.3)
            hyp.add(ring_)
            cs, nn = ring_centres(rr, cell * 0.75, k * 0.3)
            for c in cs:
                hyp.add(Dot(c + polar(cell * 0.33, np.arctan2(c[1], c[0]) + PI / 2), radius=0.028, color=COL))
        endo_r = ring + 0.66
        cortex = ground_disc(R - cell * 2.3, endo_r + 0.1, cell * 1.15)
        endo = cell_ring(endo_r, 0.15, ENDO, "#3D3820", sw=1.4, shape="rect")
        starch = VGroup(*[Dot(polar(endo_r, TAU * k / 70), radius=0.018, color="#FFF6C9") for k in range(70)])
        pith = ground_disc(endo_r - 0.12, 0, 0.24, stroke=PITH, fill="#22284A")
        bundles = VGroup(*[stem_bundle(ring, TAU * k / n + PI / 2) for k in range(n)])
        for b in bundles:
            b.submobjects.insert(0, b.submobjects.pop())
        rays = VGroup(*[Line(polar(ring - 0.45, TAU * (k + 0.5) / n + PI / 2), polar(ring + 0.45, TAU * (k + 0.5) / n + PI / 2), stroke_width=0)
                        for k in range(n)])
        trich = VGroup()
        for a in [0.5, 1.9, 3.3, 4.6, 5.7]:
            trich.add(VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.09, height=0.12, stroke_color=EPI, stroke_width=1.4).rotate(a - PI / 2).move_to(polar(R + 0.2 + 0.12 * j, a)) for j in range(3)]))
        self.ring = ring
        self.parts = dict(epi=VGroup(epi, cut, trich), hyp=hyp, cortex=cortex, endo=VGroup(endo, starch), pith=pith, bundles=bundles, rays=rays,
                          phloem=VGroup(*[b[1] for b in bundles]), cambium=VGroup(*[b[2] for b in bundles]),
                          xylem=VGroup(*[b[3] for b in bundles]), caps=VGroup(*[b[4] for b in bundles]))
        self.add(cortex, pith, endo, starch, bundles, hyp, epi, cut, trich)


def mono_bundle(size=1.0):
    """Monocot closed bundle, phloem up: the 'skull' (two metaxylem eyes, protoxylem, lysigenous cavity)."""
    s = size
    sheath = Ellipse(width=0.62 * s, height=0.78 * s, stroke_color=SCL, stroke_width=3.2 * s, fill_color="#26203A", fill_opacity=1)
    ph = VGroup(*[Circle(radius=0.035 * s, stroke_width=0, fill_color=PHL, fill_opacity=0.9).move_to([x * s, y * s, 0])
                  for x, y in [(-0.1, 0.2), (0, 0.24), (0.1, 0.2), (-0.05, 0.13), (0.05, 0.13)]])
    mx = VGroup(*[Circle(radius=0.075 * s, stroke_color=XYL, stroke_width=2.2 * s, fill_color=XYL, fill_opacity=0.3).move_to([x * s, 0.0, 0]) for x in (-0.16, 0.16)])
    px = VGroup(Circle(radius=0.04 * s, stroke_color=XYL, stroke_width=1.8 * s, fill_color=XYL, fill_opacity=0.3).move_to([0, -0.08 * s, 0]),
                Circle(radius=0.035 * s, stroke_color=XYL, stroke_width=1.8 * s, fill_color=XYL, fill_opacity=0.3).move_to([0, -0.17 * s, 0]))
    cav = Circle(radius=0.07 * s, stroke_color="#9AA3D8", stroke_width=1.5 * s, fill_color=th.BG, fill_opacity=1).move_to([0, -0.27 * s, 0])
    g = VGroup(sheath, ph, mx, px, cav)
    g.parts = dict(sheath=sheath, phloem=ph, meta=mx, proto=px, cavity=cav)
    return g


class MonocotStemTS(VGroup):
    def __init__(self, R=2.7, cell=0.2, seed=21):
        super().__init__()
        epi = cell_ring(R, cell * 0.8, EPI, "#163B38", sw=1.3, shape="rect")
        cut = Circle(radius=R + cell * 0.45, stroke_color="#BFF5EF", stroke_width=4.5)
        hyp = VGroup(*[cell_ring(R - cell * (0.8 + 0.6 * k), cell * 0.6, "#FFC2AE", SCL, sw=1, phase=0.2 * k) for k in range(2)])
        ground = ground_disc(R - cell * 2.0, 0, cell * 1.25, stroke="#6FAF86", fill=PARF, sw=1.0)
        rng = np.random.default_rng(seed)
        pts = []
        tries = 0
        while len(pts) < 70 and tries < 9000:
            tries += 1
            r = (R - 0.45) * np.sqrt(rng.uniform(0, 1))
            a = rng.uniform(0, TAU)
            s = 0.42 + 0.7 * (1 - r / (R - 0.45)) ** 1.5
            p = polar(r, a)
            if all(np.linalg.norm(p - q) > 0.3 * (s + t) + 0.1 for q, t in pts):
                pts.append((p, s))
        bundles = VGroup()
        for p, s in pts:
            b = mono_bundle(s * 0.75)
            b.rotate(np.arctan2(p[1], p[0]) - PI / 2).move_to(p)
            bundles.add(b)
        self.parts = dict(epi=VGroup(epi, cut), hyp=hyp, ground=ground, bundles=bundles)
        self.add(ground, hyp, bundles, epi, cut)


class DicotLeafTS(VGroup):
    """A strip of a dorsiventral leaf, upper surface up; width w, centred at origin."""

    def __init__(self, w=9.0, seed=31, vein_x=0.0):
        super().__init__()
        rg = np.random.default_rng(seed)
        y_ue, y_pal, y_sp, y_le = 1.35, 0.72, -0.35, -1.3
        cut = Line([-w / 2, y_ue + 0.2, 0], [w / 2, y_ue + 0.2, 0], color="#FFE08A", stroke_width=7)
        cutl = Line([-w / 2, y_le - 0.2, 0], [w / 2, y_le - 0.2, 0], color="#FFE08A", stroke_width=3)
        ue = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.34, height=0.32, stroke_color=EPI, stroke_width=1.6, fill_color="#163B38", fill_opacity=1).move_to([x, y_ue, 0])
                      for x in np.arange(-w / 2 + 0.17, w / 2, 0.36)])
        pal = VGroup()
        for x in np.arange(-w / 2 + 0.13, w / 2, 0.26):
            if abs(x - vein_x) < 0.55:
                continue
            c = RoundedRectangle(corner_radius=0.1, width=0.22, height=0.82, stroke_color=PAR, stroke_width=1.4, fill_color="#173A1E", fill_opacity=1).move_to([x, y_pal, 0])
            pal.add(c, *[Dot([x + 0.055 * (-1) ** k, y_pal - 0.33 + 0.11 * k, 0], radius=0.033, color=CHL) for k in range(7)])
        xs = list(np.arange(-w / 2 + 0.15, w / 2, 0.3))
        stx = [x for i, x in enumerate(xs) if i % 7 == 3 and abs(x - vein_x) > 0.6]
        sp = VGroup()
        for i, c in enumerate(hex_centres(w - 0.3, 1.0, 0.2, [0, y_sp, 0], jit=0.06, seed=seed)):
            if abs(c[0] - vein_x) < 0.65 or rg.uniform() < 0.18 or (c[1] < y_le + 0.62 and min(abs(c[0] - x) for x in stx) < 0.42):
                continue
            sp.add(blob(c, 0.165, n=7, jit=0.25, seed=i + seed, fill="#173A1E"))
            sp.add(Dot(c + rg.uniform(-0.05, 0.05, 3) * [1, 1, 0], radius=0.03, color=CHL))
        le, stom = VGroup(), VGroup()
        for x in xs:
            if any(abs(x - s) < 0.2 for s in stx):
                continue
            le.add(RoundedRectangle(corner_radius=0.05, width=0.28, height=0.24, stroke_color=EPI, stroke_width=1.4, fill_color="#163B38", fill_opacity=1).move_to([x, y_le, 0]))
        for s in stx:
            gc = VGroup(*[Ellipse(width=0.2, height=0.3, stroke_color="#9FF0D9", stroke_width=1.6, fill_color="#1F6B4F", fill_opacity=1).move_to([s + d, y_le, 0]) for d in (-0.11, 0.11)])
            cav = Ellipse(width=0.62, height=0.36, stroke_color=th.MUTED, stroke_width=1.4, fill_color=th.BG, fill_opacity=1).move_to([s, y_le + 0.3, 0])
            stom.add(VGroup(cav, gc))
        vx = vein_x
        sheath = Circle(radius=0.55, stroke_color="#D8F5B0", stroke_width=2.2, fill_color="#20301C", fill_opacity=1).move_to([vx, 0.05, 0])
        vx_x = VGroup(*[Circle(radius=0.07, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.3).move_to([vx + dx, 0.22 + dy, 0])
                        for dx, dy in [(-0.18, 0), (0, 0.04), (0.18, 0), (-0.09, -0.12), (0.09, -0.12)]])
        vx_p = VGroup(*[Circle(radius=0.05, stroke_width=0, fill_color=PHL, fill_opacity=0.9).move_to([vx + dx, -0.2 + dy, 0])
                        for dx, dy in [(-0.16, 0), (0, -0.05), (0.16, 0), (-0.08, -0.14), (0.08, -0.14)]])
        self.parts = dict(cuticle=VGroup(cut, cutl), ue=ue, palisade=pal, spongy=sp, le=le, stomata=stom, vein=VGroup(sheath, vx_x, vx_p),
                          xylem=vx_x, phloem=vx_p, sheath=sheath)
        self.add(sp, pal, sheath, vx_x, vx_p, stom, le, ue, cut, cutl)


class MonocotLeafTS(VGroup):
    def __init__(self, w=9.0, seed=41):
        super().__init__()
        rg = np.random.default_rng(seed)
        y_ue, y_le = 1.05, -1.05
        cuts = VGroup(Line([-w / 2, y_ue + 0.2, 0], [w / 2, y_ue + 0.2, 0], color="#FFE08A", stroke_width=4),
                      Line([-w / 2, y_le - 0.2, 0], [w / 2, y_le - 0.2, 0], color="#FFE08A", stroke_width=4))
        veins = [(-3.3, 1.0), (-1.65, 0.6), (0.0, 1.0), (1.65, 0.6), (3.3, 1.0)]
        bull_x = [-2.47, -0.82, 0.82, 2.47]
        ue, le, stom, bull = VGroup(), VGroup(), VGroup(), VGroup()
        st_x = [-4.0, -2.47, -0.82, 0.82, 2.47, 4.0]
        for x in np.arange(-w / 2 + 0.15, w / 2, 0.3):
            near_b = min(abs(x - b) for b in bull_x) < 0.42
            near_s = min(abs(x - b) for b in st_x) < 0.22
            if not near_b and not near_s:
                ue.add(RoundedRectangle(corner_radius=0.05, width=0.28, height=0.24, stroke_color=EPI, stroke_width=1.4, fill_color="#163B38", fill_opacity=1).move_to([x, y_ue, 0]))
            if near_s:
                continue
            le.add(RoundedRectangle(corner_radius=0.05, width=0.28, height=0.24, stroke_color=EPI, stroke_width=1.4, fill_color="#163B38", fill_opacity=1).move_to([x, y_le, 0]))
        for b in bull_x:
            for d, hh in [(-0.3, 0.42), (0, 0.55), (0.3, 0.42)]:
                bull.add(RoundedRectangle(corner_radius=0.08, width=0.29, height=hh, stroke_color="#A8F0FF", stroke_width=1.8, fill_color="#1D3F52", fill_opacity=1)
                         .move_to([b + d, y_ue + 0.12 - hh / 2, 0]))
        for x in st_x:
            for y, sgn in [(y_ue, -1), (y_le, 1)]:
                if y == y_ue and x in bull_x:
                    continue
                stom.add(VGroup(*[Ellipse(width=0.2, height=0.1, stroke_color="#9FF0D9", stroke_width=1.6, fill_color="#1F6B4F", fill_opacity=1).move_to([x + 0.1 * s_, y, 0]) for s_ in (-1, 1)]))
        mes = VGroup()
        for i, c in enumerate(hex_centres(w - 0.2, 1.4, 0.17, ORIGIN, jit=0.04, seed=seed)):
            if any(abs(c[0] - vx) < 0.42 * s + 0.1 for vx, s in veins):
                continue
            mes.add(blob(c, 0.14, n=7, jit=0.15, seed=i, fill="#173A1E"), Dot(c, radius=0.03, color=CHL))
        vb = VGroup()
        gird = VGroup()
        for vx, s in veins:
            b = mono_bundle(s * 1.2).rotate(PI).move_to([vx, 0, 0])
            vb.add(b)
            if s > 0.8:
                gird.add(Rectangle(width=0.32, height=y_ue - 0.47 * s * 1.2 - 0.12, stroke_width=0, fill_color=SCL, fill_opacity=0.85).next_to(b, UP, buff=0).shift(DOWN * 0.04),
                         Rectangle(width=0.32, height=-y_le - 0.47 * s * 1.2 - 0.12, stroke_width=0, fill_color=SCL, fill_opacity=0.85).next_to(b, DOWN, buff=0).shift(UP * 0.04))
        self.parts = dict(cuticle=cuts, ue=ue, le=le, stomata=stom, bulliform=bull, mesophyll=mes, bundles=vb, girders=gird)
        self.add(mes, gird, vb, ue, le, bull, stom, cuts)


# ------------------------------------------------------------------ layout helpers
def label(text, at, target, color=th.INK, size=22, side=RIGHT, dot=True):
    """A text label at `at` with a leader line to `target` (a point)."""
    t = T(text, size=size, color=color).move_to(at)
    edge = t.get_left() if side is RIGHT else t.get_right()
    edge = edge + (LEFT * 0.08 if side is RIGHT else RIGHT * 0.08)
    ln = Line(edge, np.array(target, dtype=float), stroke_width=1.8, color=color)
    g = VGroup(ln, t)
    if dot:
        g.add(Dot(np.array(target, dtype=float), radius=0.045, color=color))
    return g


class Captions:
    """One caption at a time in a fixed slot: the previous one fades out as the next fades in."""

    def __init__(self, scene, at=(3.7, 0.2, 0), width=5.4, size=27):
        self.s, self.at, self.width, self.size = scene, np.array(at, dtype=float), width, size
        self.cur = None

    def make(self, text, color=th.INK, swatch=None, sub=None):
        head = para(text, width=self.width - (0.5 if swatch else 0), size=self.size, color=color, weight="SEMIBOLD")
        rows = [head]
        if sub:
            rows.append(para(sub, width=self.width, size=self.size - 5, color=th.BODY))
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if swatch:
            sw = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.3, stroke_width=0, fill_color=swatch, fill_opacity=1)
            g = VGroup(sw, g).arrange(RIGHT, buff=0.22, aligned_edge=UP)
        return g.move_to(self.at)

    def __call__(self, text, color=th.INK, swatch=None, sub=None, run_time=0.5):
        new = self.make(text, color, swatch, sub)
        anims = [FadeIn(new, shift=UP * 0.15)]
        if self.cur is not None:
            anims.append(FadeOut(self.cur, shift=UP * 0.15))
        self.s.play(*anims, run_time=run_time)
        self.cur = new
        return new

    def clear(self, run_time=0.4):
        if self.cur is not None:
            self.s.play(FadeOut(self.cur), run_time=run_time)
            self.cur = None


def legend(items, size=22, buff=0.16):
    rows = VGroup()
    for name, col in items:
        sw = RoundedRectangle(corner_radius=0.05, width=0.26, height=0.26, stroke_width=0, fill_color=col, fill_opacity=1)
        rows.add(VGroup(sw, T(name, size=size, color=th.INK)).arrange(RIGHT, buff=0.16))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def neby_in(scene, state="idle", corner=DR, height=1.4, buff=0.45, at=None):
    nb = scene.neby(state, height=height)
    if at is not None:
        nb.move_to(at)
    else:
        nb.to_corner(corner, buff=buff)
    scene.add(nb)
    scene.play(FadeIn(nb, scale=0.5), run_time=0.4)
    return nb


def neby_out(scene, nb):
    scene.play(FadeOut(nb), run_time=0.3)
    scene.remove(nb)


def example_head(s, problem, width=12.2, size=27):
    head = T(s.S["example"], size=26, color=s.color, weight="BOLD").to_corner(UL, buff=0.75)
    prob = para(problem, width=width, size=size, color=th.INK)
    prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
    return head, prob


def card(s, title, body, w=3.9, h=2.4, color=None, tsize=28, bsize=22):
    hh = T(title, size=tsize, color=color or s.color, weight="BOLD")
    bb = para(body, width=w - 0.5, size=bsize, color=th.BODY) if isinstance(body, str) else body
    inner = VGroup(hh, bb).arrange(DOWN, buff=0.22)
    box = s.panel(w, max(h, inner.height + 0.5), color=color)
    inner.move_to(box)
    return VGroup(box, hh, bb)


def table(rows, col_w, row_h=0.52, size=24, head_color=None, colors=None):
    out = VGroup()
    x0 = -sum(col_w) / 2
    for i, r in enumerate(rows):
        g = VGroup()
        bg = Rectangle(width=sum(col_w), height=row_h, stroke_width=0,
                       fill_color=th.PANEL_EDGE if i == 0 else th.PANEL, fill_opacity=0.9 if i == 0 else (0.75 if i % 2 else 0.45))
        bg.move_to([0, -i * row_h, 0])
        g.add(bg)
        x = x0
        for j, cell in enumerate(r):
            if isinstance(cell, str):
                col = (head_color or th.INK) if i == 0 else ((colors[j] if colors else th.BODY))
                m = T(cell, size=size, color=col, weight="SEMIBOLD" if i == 0 else "NORMAL")
            else:
                m = cell
            if m.width > col_w[j] - 0.2:
                m.scale_to_fit_width(col_w[j] - 0.2)
            m.move_to([x + col_w[j] / 2, -i * row_h, 0])
            g.add(m)
            x += col_w[j]
        out.add(g)
    return out


def reveal_table(scene, tb, dur, first=1):
    """Fade the header in, then each row, spread over `dur` seconds."""
    scene.play(FadeIn(tb[0]), run_time=0.4)
    per = max(0.35, (dur - 0.6) / max(1, len(tb) - 1))
    for r in tb[1:]:
        scene.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.35)
        scene.hold(per - 0.35)
