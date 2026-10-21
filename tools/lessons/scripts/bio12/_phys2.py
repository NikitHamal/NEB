"""Extra drawing helpers for Class 12 Biology, Unit 2 (Plant Physiology): guard cells that open with a
single parameter, coleoptiles/roots that bend with constant curvature, molecule chips, a running tally
board and a Mimosa leaf that folds. Colours come from _bio so tissues look the same in every unit."""
import numpy as np
from manim import *

from kit import M, T, para, th
from _bio import XYL, PHL, CHL, WATER, FOOD, PAR, PARF, EPI

GC_STROKE = "#9FF0D9"
GC_FILL = "#1F6B4F"
SHOOT = "#7BE495"
SHOOT_F = "#24452E"
ROOT = "#C9A27A"
ROOT_F = "#3A2E1F"
AUX = "#FFD166"
KION = "#FFD166"


def guard_pair(o, c=ORIGIN, H=1.25, w=0.6, n=26, micel=False, chl=True):
    """Two kidney guard cells joined at their ends. o = 0 closed .. 1 wide open. The cells keep their
    width and bow apart as they open (radial micellation turns turgor into length)."""
    c = np.array(c, dtype=float)
    g = VGroup()
    ys = np.linspace(-H, H, n)
    f = np.clip(1 - (ys / H) ** 2, 0, 1)
    for sgn in (-1, 1):
        xin = sgn * (0.03 + o * 0.42 * f)
        xout = xin + sgn * w * np.sqrt(f)
        inner = [c + np.array([x, y, 0]) for x, y in zip(xin, ys)]
        outer = [c + np.array([x, y, 0]) for x, y in zip(xout[::-1], ys[::-1])]
        cell = Polygon(*inner, *outer[1:-1], stroke_color=GC_STROKE, stroke_width=2.4, fill_color=GC_FILL, fill_opacity=1)
        wall = VMobject(stroke_color="#D8FFF2", stroke_width=6).set_points_smoothly(inner)
        g.add(cell, wall)
        if micel:
            for yy in np.linspace(-0.75 * H, 0.75 * H, 7):
                ff = 1 - (yy / H) ** 2
                a = c + np.array([sgn * (0.03 + o * 0.42 * ff), yy, 0])
                b = a + np.array([sgn * w * np.sqrt(ff), 0, 0])
                g.add(Line(a, b, stroke_width=1.6, color="#D8FFF2", stroke_opacity=0.7))
        if chl:
            for yy in (-0.55 * H, -0.18 * H, 0.18 * H, 0.55 * H):
                ff = 1 - (yy / H) ** 2
                x = sgn * (0.03 + o * 0.42 * ff) + sgn * w * np.sqrt(ff) * 0.55
                g.add(Ellipse(width=0.16, height=0.1, stroke_width=0, fill_color=CHL, fill_opacity=1).move_to(c + [x, yy, 0]))
    return g


def guard_inside(o, c, H=1.25, w=0.6, k=0, sgn=1):
    """A point inside one guard cell (for ions to fly to). k picks one of a few slots."""
    ys = [-0.45, -0.1, 0.25, 0.55, -0.7, 0.75]
    yy = ys[k % len(ys)] * H
    ff = 1 - (yy / H) ** 2
    x = sgn * (0.03 + o * 0.42 * ff) + sgn * w * np.sqrt(ff) * 0.5
    return np.array(c, dtype=float) + np.array([x, yy, 0])


def _arc_pts(L, theta, s):
    if abs(theta) < 1e-4:
        return np.stack([np.zeros_like(s), s], 1), np.zeros_like(s)
    R = L / theta
    phi = theta * s / L
    return np.stack([R * (1 - np.cos(phi)), R * np.sin(phi)], 1), phi


def organ(base, L, theta, w=0.2, n=30, rot=0.0, tip=True, color=SHOOT, fill=SHOOT_F, aux=None, aux_shift=0.0, aux_n=8, aux_side=1, sw=2.5):
    """A shoot/coleoptile/root of length L, bent with constant curvature theta (radians, + = to the
    right of its growing direction), base at `base`, initially pointing up then rotated by rot.
    aux: draw auxin dots; aux_shift 0 = evenly on both flanks, 1 = all on side aux_side (+1 = left
    flank of the organ seen looking along it)."""
    base = np.array(base, dtype=float)
    s = np.linspace(0, L, n)
    p, phi = _arc_pts(L, theta, s)
    t = np.stack([np.sin(phi), np.cos(phi)], 1)
    nrm = np.stack([-np.cos(phi), np.sin(phi)], 1)
    left = p + nrm * w
    right = p - nrm * w
    pts = [list(q) + [0] for q in left]
    if tip:
        an = np.arctan2(nrm[-1][1], nrm[-1][0])
        for a in np.linspace(an, an - PI, 9)[1:-1]:
            pts.append([p[-1][0] + w * np.cos(a), p[-1][1] + w * np.sin(a), 0])
    pts += [list(q) + [0] for q in right[::-1]]
    body = Polygon(*[np.array(q) for q in pts], stroke_color=color, stroke_width=sw, fill_color=fill, fill_opacity=1)
    g = VGroup(body)
    dots = VGroup()
    if aux is not None:
        half = max(1, aux_n // 2)
        for k in range(aux_n):
            j, side = k // 2, (1 if k % 2 == 0 else -1)
            fr = 0.2 + 0.7 * j / max(1, half - 1)
            i = int(fr * (n - 1))
            if side == aux_side:
                off = side * 0.55
            else:
                off = side * 0.55 + (aux_side * 0.15 - side * 0.55) * aux_shift
            q = p[i] + nrm[i] * w * off + t[i] * w * 0.6 * aux_shift * (k % 2)
            dots.add(Dot([q[0], q[1], 0], radius=min(0.07, w * 0.28), color=aux))
        g.add(dots)
    g.rotate(rot, about_point=ORIGIN)
    g.shift(base)
    g.top = base + rotate_vector(np.array([p[-1][0], p[-1][1], 0]), rot)
    g.phi = phi[-1]
    return g


def chip(text, color=th.INK, size=20, edge=None, fill=th.PANEL, pad=0.13, weight="SEMIBOLD"):
    t = T(text, size=size, color=color, weight=weight)
    b = RoundedRectangle(corner_radius=0.1, width=t.width + 2 * pad, height=max(t.height, 0.2) + 1.6 * pad,
                         stroke_color=edge or color, stroke_width=2, fill_color=fill, fill_opacity=0.96)
    return VGroup(b, t.move_to(b))


def mchip(tex, color=th.INK, size=30, edge=None, pad=0.13):
    t = M(tex, size=size, color=color)
    b = RoundedRectangle(corner_radius=0.1, width=t.width + 2 * pad, height=t.height + 1.6 * pad,
                         stroke_color=edge or color, stroke_width=2, fill_color=th.PANEL, fill_opacity=0.96)
    return VGroup(b, t.move_to(b))


class Tally(VGroup):
    """A small scoreboard: rows of (name, colour) with an Integer each."""

    def __init__(self, rows, title=None, w=3.0, size=26, gap=0.62):
        super().__init__()
        self.vals = {}
        body = VGroup()
        for i, (name, col) in enumerate(rows):
            lab = T(name, size=size, color=col, weight="SEMIBOLD")
            num = Integer(0, font_size=size * 1.45, color=th.INK)
            lab.move_to([-w / 2 + 0.3 + lab.width / 2, -i * gap, 0])
            num.move_to([w / 2 - 0.3 - num.width / 2, -i * gap, 0])
            body.add(VGroup(lab, num))
            self.vals[name] = num
        hh = T(title, size=22, color=th.MUTED) if title else VGroup()
        inner = VGroup(hh, body).arrange(DOWN, buff=0.3) if title else body
        box = RoundedRectangle(corner_radius=0.18, width=w, height=inner.height + 0.6, stroke_color=th.PANEL_EDGE,
                               stroke_width=2, fill_color=th.PANEL, fill_opacity=0.92).move_to(inner)
        self.add(box, inner)
        self.box, self.title = box, hh

    def bump(self, name, value):
        return ChangeDecimalToValue(self.vals[name], value, rate_func=rate_functions.smooth)


def mimosa(f, drop, P=ORIGIN, L=2.6, a0=1.05, n_leaf=7, pinnae=(0.35, -0.35)):
    """Mimosa leaf: petiole from pulvinus P at angle a0 - drop (radians from +x), with pinnae fanning
    from its tip, each with paired leaflets. f = 0 spread .. 1 folded (leaflets press forward together)."""
    P = np.array(P, dtype=float)
    a = a0 - drop
    tip = P + L * np.array([np.cos(a), np.sin(a), 0])
    g = VGroup()
    g.add(Line(P, tip, stroke_width=5, color=SHOOT))
    for da in pinnae:
        b = a + da * (1 - 0.6 * f)
        d = np.array([np.cos(b), np.sin(b), 0])
        nv = np.array([-np.sin(b), np.cos(b), 0])
        pl = 2.0
        g.add(Line(tip, tip + d * pl, stroke_width=3, color=SHOOT))
        for k in range(n_leaf):
            q = tip + d * (0.35 + k * (pl - 0.4) / (n_leaf - 1))
            for sgn in (1, -1):
                ang = (PI / 2) * (1 - f) + 0.18 * f
                v = d * np.cos(ang) + sgn * nv * np.sin(ang)
                lf = Ellipse(width=0.42, height=0.15, stroke_color=SHOOT, stroke_width=1.5, fill_color="#2E7D32", fill_opacity=1)
                lf.rotate(np.arctan2(v[1], v[0])).move_to(q + v * 0.22)
                g.add(lf)
    g.add(Ellipse(width=0.42, height=0.3, stroke_color=SHOOT, stroke_width=2, fill_color="#3F7A3A", fill_opacity=1).rotate(a).move_to(P))
    return g


def banana(c, ang=0.0, color="#6BAA3A", s=1.0):
    arc = Arc(radius=0.75 * s, start_angle=PI + 0.55, angle=-PI + 1.1, stroke_color=color, stroke_width=20 * s)
    return arc.rotate(ang).move_to(c)
