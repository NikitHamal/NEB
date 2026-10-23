"""Shared drawing helpers for the Class 12 Chemistry (chem12) lesson videos.

Nothing in here speaks: every narration line stays as a literal in the unit scripts, so
prefetch.py can find and cache it. Helpers take the Lesson scene `s` only when they
need to play something."""
from manim import *
import numpy as np

from kit import M, T, para, th

# element colours (CPK-ish, tuned for the dark background)
EL = {"H": "#E8ECF8", "O": "#FF6B6B", "C": "#5B6275", "N": "#5C8DFF", "Cl": "#7BE495", "Na": "#B18CFF",
      "S": "#FFD84D", "Mn": "#C77DFF", "Fe": "#FF9F5A", "Cr": "#5FD3B0", "K": "#9D7BFF", "Ba": "#4CC9F0",
      "Ag": "#C0C6D8", "Cu": "#E39A5B", "Zn": "#9FB3C8", "Mg": "#A4F08B", "Al": "#B9C2D9", "Ca": "#8AE6C8",
      "P": "#FFA552", "I": "#A05CFF", "Br": "#C1543A", "X": th.AMBER}

PURPLE = "#B03BD6"       # permanganate
PINK_END = "#F7A8D8"     # first permanent pink / phenolphthalein
MO_RED = "#FF5A4E"       # methyl orange, acid
MO_YEL = "#FFC94A"       # methyl orange, alkali
WATER = "#4CC9F0"


def chem(tex, size=40, color=th.INK):
    """A formula or equation set upright: chem(r"H_2SO_4")."""
    return M(r"\mathrm{" + tex + "}", size=size, color=color)


def atom(sym, r=0.32, color=None, size=None, label_color=None):
    c = color or EL.get(sym, th.MUTED)
    ball = Circle(radius=r, fill_color=c, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5)
    shine = Circle(radius=r * 0.32, fill_color=WHITE, fill_opacity=0.35, stroke_width=0).shift(UL * r * 0.35)
    lab = T(sym, size=size or int(r * 62), color=label_color or ("#10131f" if sym in ("H", "S", "Cl", "Mg", "Ag", "Ca", "Al", "Zn") else WHITE), weight="BOLD")
    lab.move_to(ball)
    return VGroup(ball, shine, lab)


def ion(sym, charge, r=0.34, color=None):
    a = atom(sym, r=r, color=color)
    ch = T(charge, size=int(r * 50), color=th.INK, weight="BOLD").move_to(a.get_corner(UR) + RIGHT * 0.05)
    return VGroup(a, ch)


def electron(r=0.11):
    return VGroup(Circle(radius=r, fill_color=th.SKY, fill_opacity=1, stroke_color=WHITE, stroke_width=1),
                  T("−", size=int(r * 150), color="#0b0e1a", weight="BOLD"))


def example_head(s, problem, width=12.2, size=27):
    head = T(s.S["example"], size=26, color=s.color, weight="BOLD").to_corner(UL, buff=0.75)
    prob = para(problem, width=width, size=size, color=th.INK)
    prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
    return head, prob


def steps(*lines, size=38, buff=0.38):
    g = VGroup(*[M(l, size=size) if isinstance(l, str) else l for l in lines])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return g


def show_neby(s, state="idle", height=1.5, corner=DR, buff=0.45, at=None):
    nb = s.neby(state, height=height)
    if at is not None:
        nb.move_to(at)
    else:
        nb.to_corner(corner, buff=buff)
    s.add(nb)
    s.play(FadeIn(nb, scale=0.5), run_time=0.4)
    return nb


def hide_neby(s, nb):
    s.play(FadeOut(nb, scale=0.6), run_time=0.35)
    s.remove(nb)


def card(s, title, body, w=3.9, h=2.4, color=None, tsize=28, bsize=22):
    box = s.panel(w, h, color=color)
    hh = T(title, size=tsize, color=color or s.color, weight="BOLD")
    bb = para(body, width=w - 0.5, size=bsize, color=th.BODY) if isinstance(body, str) else body
    VGroup(hh, bb).arrange(DOWN, buff=0.22).move_to(box)
    return VGroup(box, hh, bb)


def table(rows, col_w, row_h=0.52, size=24, head_color=None, colors=None):
    """rows: list of lists of str/mobject; first row is the header. Returns VGroup of row VGroups."""
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


# ------------------------------------------------------------------ glassware
class Burette:
    """A 50 cm³ burette whose liquid level follows the ValueTracker `vol` (cm³ delivered)."""

    def __init__(self, x=0.0, top=2.9, bottom=-0.2, w=0.34, color=th.SKY, labels=True, cap=50.0):
        self.x, self.top, self.bottom, self.w, self.cap = x, top, bottom, w, cap
        self.vol = ValueTracker(0)
        self.color = color
        self.y0 = top - 0.25                     # the 0 mark
        self.y50 = bottom + 0.25                 # the 50 mark
        tube = Rectangle(width=w, height=top - bottom, stroke_color=th.INK, stroke_width=2.5).move_to([x, (top + bottom) / 2, 0])
        ticks = VGroup()
        nums = VGroup()
        for k in range(0, 51):
            y = self.y_of(k)
            L = w * 0.55 if k % 10 == 0 else (w * 0.35 if k % 5 == 0 else w * 0.2)
            ticks.add(Line([x - w / 2, y, 0], [x - w / 2 + L, y, 0], color=th.MUTED, stroke_width=1.2 if k % 5 else 2))
            if labels and k % 10 == 0:
                nums.add(T(str(k), size=16, color=th.MUTED).next_to([x - w / 2, y, 0], LEFT, buff=0.08))
        cock = VGroup(Circle(radius=0.11, fill_color=th.BG, fill_opacity=1, stroke_color=th.INK, stroke_width=2).move_to([x, bottom - 0.12, 0]),
                      Line([x - 0.22, bottom - 0.12, 0], [x + 0.22, bottom - 0.12, 0], color=th.INK, stroke_width=4))
        tip = Polygon([x - 0.07, bottom - 0.24, 0], [x + 0.07, bottom - 0.24, 0], [x + 0.025, bottom - 0.62, 0], [x - 0.025, bottom - 0.62, 0],
                      stroke_color=th.INK, stroke_width=2, fill_opacity=0)
        self.tip_point = np.array([x, bottom - 0.66, 0])
        self.glass = VGroup(tube, ticks, nums, cock, tip)
        self.liquid = always_redraw(self._liquid)

    def y_of(self, v):
        return self.y0 - (self.y0 - self.y50) * v / self.cap

    def _liquid(self):
        yl = self.y_of(self.vol.get_value())
        h = max(0.01, yl - self.bottom)
        return Rectangle(width=self.w - 0.05, height=h, stroke_width=0, fill_color=self.color, fill_opacity=0.55).move_to(
            [self.x, self.bottom + h / 2, 0])

    def group(self):
        return VGroup(self.liquid, self.glass)


class Flask:
    """A conical flask; .liq is the liquid polygon (recolour it with set_fill)."""

    def __init__(self, center=ORIGIN, scale=1.0, color=th.MUTED, opacity=0.5):
        c = np.array(center, dtype=float)
        s = scale
        pts = [[-0.22, 0.95], [0.22, 0.95], [0.22, 0.45], [0.85, -0.75], [-0.85, -0.75], [-0.22, 0.45]]
        self.body = Polygon(*[c + s * np.array([p[0], p[1], 0]) for p in pts], stroke_color=th.INK, stroke_width=2.5, fill_opacity=0)
        lv = -0.2
        wl = 0.22 + (0.85 - 0.22) * (0.45 - lv) / 1.2
        lpts = [[-wl, lv], [wl, lv], [0.85, -0.75], [-0.85, -0.75]]
        self.liq = Polygon(*[c + s * np.array([p[0], p[1], 0]) for p in lpts], stroke_width=0, fill_color=color, fill_opacity=opacity)
        self.surface = c + s * np.array([0, lv, 0])
        self.g = VGroup(self.liq, self.body)


class Beaker:
    def __init__(self, center=ORIGIN, w=2.0, h=2.2, level=0.6, color=WATER, opacity=0.3):
        c = np.array(center, dtype=float)
        self.c, self.w, self.h = c, w, h
        self.outline = VMobject(stroke_color=th.INK, stroke_width=3).set_points_as_corners(
            [c + [-w / 2 - 0.1, h / 2, 0], c + [-w / 2, h / 2 - 0.1, 0], c + [-w / 2, -h / 2, 0], c + [w / 2, -h / 2, 0], c + [w / 2, h / 2 - 0.1, 0], c + [w / 2 + 0.1, h / 2, 0]])
        lh = h * level
        self.liq = Rectangle(width=w - 0.06, height=lh, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(c + [0, -h / 2 + lh / 2, 0])
        self.g = VGroup(self.liq, self.outline)

    def inside(self, rng, n, margin=0.15, level=None):
        lh = self.h * (level if level is not None else 0.6)
        xs = rng.uniform(-self.w / 2 + margin, self.w / 2 - margin, n)
        ys = rng.uniform(-self.h / 2 + margin, -self.h / 2 + lh - margin, n)
        return [self.c + np.array([a, b, 0]) for a, b in zip(xs, ys)]


def drip(s, bur, flask, n=1, run_time=0.35, color=None):
    """Play n drops falling from the burette tip to the flask's liquid surface."""
    for _ in range(n):
        d = Circle(radius=0.055, fill_color=color or bur.color, fill_opacity=0.95, stroke_width=0).move_to(bur.tip_point)
        s.add(d)
        s.play(d.animate.move_to(flask.surface), run_time=run_time, rate_func=rate_functions.ease_in_quad)
        s.remove(d)


# ------------------------------------------------------------------ titration curves
def ph_strong(vb, va=25.0, ca=0.1, cb=0.1):
    exc = (ca * va - cb * vb) / (va + vb)
    h = (exc + np.sqrt(exc * exc + 4e-14)) / 2
    return float(-np.log10(h))


def ph_weak_acid(vb, va=25.0, ca=0.1, cb=0.1, ka=1.8e-5):
    """Weak acid titrated with strong base, from the full charge balance (bisection)."""
    tot = va + vb
    Na = cb * vb / tot
    CT = ca * va / tot
    lo, hi = -14.0, 0.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        h = 10 ** mid
        f = Na + h - 1e-14 / h - CT * ka / (ka + h)
        if f < 0:
            lo = mid
        else:
            hi = mid
    return -0.5 * (lo + hi)


def ph_carbonate(va, v0=25.0, c0=0.05, ma=0.1, k1=4.45e-7, k2=4.69e-11):
    tot = v0 + va
    Na = 2 * c0 * v0 / tot
    Cl = ma * va / tot
    CT = c0 * v0 / tot
    lo, hi = -14.0, 0.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        h = 10 ** mid
        D = h * h + k1 * h + k1 * k2
        f = Na + h - Cl - 1e-14 / h - CT * (k1 * h / D + 2 * k1 * k2 / D)
        if f < 0:
            lo = mid
        else:
            hi = mid
    return -0.5 * (lo + hi)


def methyl_orange(pH):
    k = np.clip((pH - 3.1) / (4.4 - 3.1), 0, 1)
    return interpolate_color(ManimColor(MO_RED), ManimColor(MO_YEL), k)


def phenolphthalein(pH):
    k = np.clip((pH - 8.3) / (10.0 - 8.3), 0, 1)
    return interpolate_color(ManimColor("#DDE3F5"), ManimColor("#FF4FB8"), k)


def universal(pH):
    """Universal-indicator colour for a pH value."""
    stops = [(1, "#E8433A"), (4, "#F59A3A"), (6, "#F2D43C"), (7, "#5CC86A"), (9, "#3A8FE0"), (11, "#4B4BC9"), (13, "#7A3BB8")]
    pH = float(np.clip(pH, 1, 13))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if pH <= b:
            return interpolate_color(ManimColor(ca), ManimColor(cb), (pH - a) / (b - a))
    return ManimColor(stops[-1][1])


def water(center=ORIGIN, r=0.3, plus=False):
    """A bent water molecule (or hydronium with plus=True)."""
    c = np.array(center, dtype=float)
    o = atom("O", r=r).move_to(c)
    angs = [210, 330] + ([90] if plus else [])
    hs = VGroup(*[atom("H", r=r * 0.62).move_to(c + 1.55 * r * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])) for a in angs])
    bonds = VGroup(*[Line(c, h.get_center(), color=th.MUTED, stroke_width=5) for h in hs])
    g = VGroup(bonds, o, hs)
    if plus:
        g.add(T("+", size=int(r * 80), color=th.INK, weight="BOLD").move_to(c + np.array([r * 1.5, r * 1.3, 0])))
    return g


def proton(r=0.16):
    return VGroup(Circle(radius=r, fill_color=th.CORAL, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5),
                  T("H⁺", size=int(r * 110), color=WHITE, weight="BOLD"))


# ------------------------------------------------------------------ organic helpers
def push(a, b, angle=-TAU / 5, color=None):
    """An electron-pushing curved arrow from point a to point b."""
    return CurvedArrow(np.array(a, dtype=float), np.array(b, dtype=float), angle=angle, color=color or th.AMBER, stroke_width=4, tip_length=0.18)


class ReactionMap:
    """A hub-and-spoke 'reagent → product' map that grows over a lesson.

    entries: list of (key, product_tex, reagent_text, colour). Positions are fixed by the full list,
    so nodes never move as the map grows."""

    def __init__(self, hub_tex, entries, center=(0, -0.25, 0), rx=5.2, ry=2.55, hub_color=None):
        self.c = np.array(center, dtype=float)
        self.hub_tex, self.entries = hub_tex, entries
        self.rx, self.ry = rx, ry
        self.hub_color = hub_color or th.AMBER
        n = len(entries)
        self.pos = {}
        for i, e in enumerate(entries):
            a = PI / 2 - i * TAU / n
            self.pos[e[0]] = self.c + np.array([rx * np.cos(a), ry * np.sin(a), 0])

    def hub(self):
        t = chem(self.hub_tex, size=50, color=th.BG)
        box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.4, fill_color=self.hub_color, fill_opacity=1, stroke_width=0).move_to(self.c)
        t.move_to(box)
        return VGroup(box, t)

    @staticmethod
    def _edge(center, w, h, u):
        tx = (w / 2) / abs(u[0]) if abs(u[0]) > 1e-6 else 1e9
        ty = (h / 2) / abs(u[1]) if abs(u[1]) > 1e-6 else 1e9
        return center + u * min(tx, ty)

    def spoke(self, key):
        e = next(x for x in self.entries if x[0] == key)
        _, ptex, rtext, col = e
        p = self.pos[key]
        t = chem(ptex, size=36, color=th.INK)
        box = RoundedRectangle(corner_radius=0.15, width=max(t.width + 0.4, 1.4), height=t.height + 0.35, fill_color=th.PANEL, fill_opacity=1, stroke_color=col, stroke_width=3).move_to(p)
        t.move_to(box)
        hub = self.hub()
        d = p - self.c
        u = d / np.linalg.norm(d)
        start = self._edge(self.c, hub.width + 0.1, hub.height + 0.1, u)
        end = self._edge(p, box.width + 0.1, box.height + 0.1, -u)
        arr = Arrow(start, end, buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        lab = T(rtext, size=20, color=col)
        plate = RoundedRectangle(corner_radius=0.08, width=lab.width + 0.16, height=lab.height + 0.12, fill_color=th.BG, fill_opacity=0.9, stroke_width=0)
        lg = VGroup(plate, lab)
        if abs(u[1]) > 0.85:
            lg.next_to((start + end) / 2, RIGHT, buff=0.12)
        elif p[1] > self.c[1] + 0.1:
            lg.next_to(box, UP, buff=0.08)
        else:
            lg.next_to(box, DOWN, buff=0.08)
        return VGroup(arr, lg, VGroup(box, t))

    def show(self, s, shown, new, run_time=0.6):
        """Bring the map on stage: already-shown spokes appear at once, new ones grow in turn. Returns the group."""
        title = T("Reaction map", size=24, color=th.MUTED).to_corner(UR, buff=0.5)
        g = VGroup(title, self.hub())
        old = VGroup(*[self.spoke(k) for k in shown])
        g.add(old)
        s.play(FadeIn(g), run_time=0.5)
        for k in new:
            sp = self.spoke(k)
            s.sfx("pop", gain=-16)
            s.play(GrowArrow(sp[0]), FadeIn(sp[1]), FadeIn(sp[2], scale=0.6), run_time=run_time)
            s.remove(sp[0], sp[1], sp[2])
            g.add(sp)
            s.add(g)
        return g


def benzene(center=ORIGIN, r=0.9, subs=None, color=th.INK, label_size=28, kekule=False):
    """Benzene ring. subs: {vertex 0..5 (0 = top, clockwise): (text, colour)}. kekule=True draws
    alternating double bonds instead of the inner circle (needed for resonance pictures)."""
    c = np.array(center, dtype=float)
    verts = [c + r * np.array([np.sin(k * PI / 3), np.cos(k * PI / 3), 0]) for k in range(6)]
    g = VGroup(Polygon(*verts, stroke_color=color, stroke_width=4, fill_opacity=0))
    if kekule:
        inner = VGroup()
        for k in (0, 2, 4):
            a, b = verts[k], verts[(k + 1) % 6]
            m = (a + b) / 2
            d = (c - m) / np.linalg.norm(c - m) * 0.16 * r / 0.9
            inner.add(Line(a + (b - a) * 0.15 + d, b + (a - b) * 0.15 + d, color=color, stroke_width=4))
        g.add(inner)
    else:
        g.add(Circle(radius=r * 0.58, stroke_color=color, stroke_width=3).move_to(c))
    for k, (txt, col) in (subs or {}).items():
        d = (verts[k] - c) / r
        end = verts[k] + d * 0.45 * r / 0.9
        g.add(Line(verts[k], end, color=th.MUTED, stroke_width=4))
        lab = T(txt, size=label_size, color=col, weight="BOLD")
        lab.next_to(end, d, buff=0.06)
        g.add(lab)
    g.verts = verts
    return g
