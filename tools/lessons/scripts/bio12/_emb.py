"""Embryology drawing helpers: flower parts, an anther in transverse section, pollen grains, an anatropous ovule,
the 7-celled 8-nucleate embryo sac, and the stages of the Capsella embryo."""
import numpy as np
from manim import *

from kit import T, th

EGG = "#FF8FB1"
SYN = "#C77DFF"
ANT = "#4CC9F0"
POLAR = "#FFD166"
MALE = "#7BE495"
TUBE = "#FFB547"
EXINE = "#E9C46A"
NUC = "#8FD18B"
INTEG = "#9C8CFF"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


def nucleus(c, r=0.12, color=WHITE):
    return Dot(np.array(c, dtype=float), radius=r, color=color)


def pollen(r=0.7, cells=2, spikes=True):
    """Mature pollen grain: spiky exine, thin intine, vegetative nucleus + generative cell (cells=2) or two male gametes (cells=3)."""
    pts = []
    for a in np.linspace(0, TAU, 160, endpoint=False):
        k = 1 + (0.07 * max(0, np.cos(18 * a)) ** 6 if spikes else 0)
        pts.append(polar(r * k, a))
    ex = VMobject(stroke_color=EXINE, stroke_width=4, fill_color="#3A3220", fill_opacity=1).set_points_as_corners(pts + [pts[0]])
    intine = Circle(radius=r * 0.86, stroke_color="#F6E3A1", stroke_width=1.6)
    pores = VGroup(*[Line(polar(r * 0.86, a), polar(r * 1.05, a), color=th.BG, stroke_width=9) for a in (PI / 2, PI * 7 / 6, -PI / 6)])
    veg = nucleus(polar(r * 0.3, PI * 0.8), r * 0.16, "#B6F5C4")
    g = VGroup(ex, pores, intine, veg)
    gen = VGroup()
    if cells == 2:
        gen = VGroup(Ellipse(width=r * 0.62, height=r * 0.26, stroke_color=MALE, stroke_width=2, fill_color="#1E4A2C", fill_opacity=1).rotate(0.4).move_to(polar(r * 0.32, -0.3)),
                     nucleus(polar(r * 0.32, -0.3), r * 0.08, MALE))
    elif cells == 3:
        gen = VGroup(*[VGroup(Ellipse(width=r * 0.4, height=r * 0.2, stroke_color=MALE, stroke_width=2, fill_color="#1E4A2C", fill_opacity=1).rotate(0.4), nucleus(ORIGIN, r * 0.07, MALE)).move_to(polar(r * 0.38, a)) for a in (-0.6, 0.2)])
    g.add(gen)
    g.parts = dict(exine=ex, intine=intine, pores=pores, veg=veg, gen=gen)
    return g


def anther_ts(s=1.0):
    """Butterfly-shaped TS of a dithecous anther: four microsporangia, each with four wall layers and pollen inside."""
    g = VGroup()
    out = VGroup()
    sacs = []
    centres = [(-1.15, 0.62), (-1.15, -0.62), (1.15, 0.62), (1.15, -0.62)]
    for x, y in centres:
        c = np.array([x, y, 0]) * s
        out.add(Circle(radius=0.78 * s, stroke_width=0, fill_color="#2A3A2E", fill_opacity=1).move_to(c))
    conn = RoundedRectangle(corner_radius=0.3 * s, width=1.2 * s, height=1.9 * s, stroke_width=0, fill_color="#2A3A2E", fill_opacity=1)
    bundle = Circle(radius=0.16 * s, stroke_width=0, fill_color="#4CC9F0", fill_opacity=0.7)
    layers = VGroup()
    for x, y in centres:
        c = np.array([x, y, 0]) * s
        ep = Circle(radius=0.74 * s, stroke_color="#2EC4B6", stroke_width=3).move_to(c)
        en = Circle(radius=0.66 * s, stroke_color="#F4A261", stroke_width=5).move_to(c)
        md = Circle(radius=0.57 * s, stroke_color="#8189B0", stroke_width=2.5).move_to(c)
        tp = Circle(radius=0.5 * s, stroke_color="#C77DFF", stroke_width=6).move_to(c)
        pol = VGroup(*[Circle(radius=0.07 * s, stroke_color=EXINE, stroke_width=1.5, fill_color="#3A3220", fill_opacity=1).move_to(c + polar(rr * s, a))
                       for rr, n in [(0.0, 1), (0.2, 6), (0.37, 10)] for a in np.linspace(0, TAU, n, endpoint=False)])
        layers.add(VGroup(ep, en, md, tp, pol))
        sacs.append(c)
    g.add(out, conn, bundle, layers)
    g.parts = dict(epidermis=VGroup(*[l[0] for l in layers]), endothecium=VGroup(*[l[1] for l in layers]), middle=VGroup(*[l[2] for l in layers]),
                   tapetum=VGroup(*[l[3] for l in layers]), pollen=VGroup(*[l[4] for l in layers]), connective=VGroup(conn, bundle))
    return g


def embryo_sac(w=2.0, h=4.2):
    """Mature Polygonum-type embryo sac, micropyle at the bottom: 3 antipodals (top), central cell with 2 polar nuclei, egg + 2 synergids (bottom)."""
    sac = Ellipse(width=w, height=h, stroke_color=th.INK, stroke_width=3, fill_color="#1A1F38", fill_opacity=1)
    top, bot = h / 2, -h / 2
    ants = VGroup(*[VGroup(Circle(radius=w * 0.13, stroke_color=ANT, stroke_width=2.5, fill_color=ANT, fill_opacity=0.25), nucleus(ORIGIN, w * 0.04, ANT)).move_to([dx * w, top - h * 0.12 - dy, 0])
                    for dx, dy in [(-0.13, 0.05), (0.13, 0.05), (0.0, 0.32 * w)]])
    syn = VGroup(*[VGroup(Ellipse(width=w * 0.26, height=h * 0.17, stroke_color=SYN, stroke_width=2.5, fill_color=SYN, fill_opacity=0.25), nucleus(ORIGIN, w * 0.04, SYN)).move_to([dx * w, bot + h * 0.12, 0])
                   for dx in (-0.14, 0.14)])
    fil = VGroup(*[Line([dx * w, bot + h * 0.035, 0], [dx * w, bot + h * 0.07, 0], color=SYN, stroke_width=4) for dx in (-0.16, -0.12, 0.12, 0.16)])
    egg = VGroup(Circle(radius=w * 0.16, stroke_color=EGG, stroke_width=3, fill_color=EGG, fill_opacity=0.3), nucleus(ORIGIN, w * 0.05, EGG)).move_to([0, bot + h * 0.27, 0])
    pol = VGroup(nucleus([-w * 0.08, 0.05, 0], w * 0.06, POLAR), nucleus([w * 0.08, -0.05, 0], w * 0.06, POLAR))
    g = VGroup(sac, ants, syn, fil, egg, pol)
    g.parts = dict(sac=sac, antipodals=ants, synergids=syn, filiform=fil, egg=egg, polar=pol)
    return g


def ovule(s=1.0):
    """Anatropous ovule (body inverted, micropyle beside the hilum at the bottom left)."""
    body = Ellipse(width=2.6 * s, height=3.6 * s, stroke_color=INTEG, stroke_width=4, fill_color="#231E40", fill_opacity=1)
    inner = Ellipse(width=2.1 * s, height=3.1 * s, stroke_color=INTEG, stroke_width=3)
    nuc = Ellipse(width=1.6 * s, height=2.6 * s, stroke_width=0, fill_color="#2F4A36", fill_opacity=1)
    gap = Rectangle(width=0.22 * s, height=0.6 * s, stroke_width=0, fill_color=th.BG, fill_opacity=1).move_to([0, -1.6 * s, 0])
    funicle = VMobject(stroke_color="#C5F05C", stroke_width=10 * s).set_points_smoothly([[1.0 * s, -2.7 * s, 0], [0.75 * s, -2.0 * s, 0], [1.2 * s, -1.1 * s, 0], [1.38 * s, 0.6 * s, 0], [1.0 * s, 1.6 * s, 0]])
    raphe = T("raphe", size=int(20 * s), color="#C5F05C").next_to(funicle, RIGHT, buff=0.1)
    es = embryo_sac(0.75 * s, 1.6 * s).move_to([0, -0.35 * s, 0])
    g = VGroup(body, inner, nuc, es, gap, funicle)
    g.parts = dict(integuments=VGroup(body, inner), nucellus=nuc, embryo_sac=es, micropyle=gap, funicle=funicle, raphe=raphe)
    return g


def capsella(stage, s=1.0, color="#7BE495"):
    """Capsella embryo stages: 'two', 'octant', 'globular', 'heart', 'torpedo', 'mature'. Suspensor points down (micropyle)."""
    sus = VGroup(*[Rectangle(width=0.22 * s, height=0.2 * s, stroke_color="#B8A1FF", stroke_width=2, fill_color="#2E2650", fill_opacity=1).move_to([0, -0.35 * s - 0.2 * s * k, 0]) for k in range(6)])
    hau = Circle(radius=0.2 * s, stroke_color="#B8A1FF", stroke_width=2, fill_color="#2E2650", fill_opacity=1).next_to(sus, DOWN, buff=0)
    if stage == "two":
        return VGroup(Rectangle(width=0.35 * s, height=0.28 * s, stroke_color=color, stroke_width=2.5, fill_color="#1E4A2C", fill_opacity=1).move_to([0, -0.1 * s, 0]),
                      Rectangle(width=0.45 * s, height=0.5 * s, stroke_color="#B8A1FF", stroke_width=2.5, fill_color="#2E2650", fill_opacity=1).move_to([0, -0.5 * s, 0]))
    if stage == "octant":
        o = VGroup(Circle(radius=0.32 * s, stroke_color=color, stroke_width=2.5, fill_color="#1E4A2C", fill_opacity=1),
                   Line([-0.32 * s, 0, 0], [0.32 * s, 0, 0], color=color, stroke_width=2), Line([0, -0.32 * s, 0], [0, 0.32 * s, 0], color=color, stroke_width=2))
        return VGroup(o.move_to([0, 0.0, 0]), sus, hau)
    if stage == "globular":
        return VGroup(Circle(radius=0.45 * s, stroke_color=color, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1).move_to([0, 0.05, 0]), sus, hau)
    if stage == "heart":
        pts = [[0, -0.35, 0], [0.45, -0.1, 0], [0.55, 0.35, 0], [0.32, 0.55, 0], [0.12, 0.42, 0], [0, 0.28, 0], [-0.12, 0.42, 0], [-0.32, 0.55, 0], [-0.55, 0.35, 0], [-0.45, -0.1, 0], [0, -0.35, 0]]
        h = VMobject(stroke_color=color, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1).set_points_smoothly([np.array(p) * s * 1.1 for p in pts])
        return VGroup(h, sus, hau)
    if stage == "torpedo":
        pts = [[0, -0.4, 0], [0.32, -0.1, 0], [0.38, 0.6, 0], [0.22, 1.1, 0], [0.08, 0.6, 0], [0, 0.45, 0], [-0.08, 0.6, 0], [-0.22, 1.1, 0], [-0.38, 0.6, 0], [-0.32, -0.1, 0], [0, -0.4, 0]]
        h = VMobject(stroke_color=color, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1).set_points_smoothly([np.array(p) * s * 1.1 for p in pts])
        return VGroup(h, sus, hau)
    pts = [[0, -0.4, 0], [0.3, -0.1, 0], [0.32, 0.5, 0], [0.9, 1.0, 0], [1.2, 0.5, 0], [0.55, 0.3, 0], [0.08, 0.45, 0], [-0.08, 0.45, 0], [-0.55, 0.3, 0], [-1.2, 0.5, 0], [-0.9, 1.0, 0], [-0.32, 0.5, 0], [-0.3, -0.1, 0], [0, -0.4, 0]]
    h = VMobject(stroke_color=color, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1).set_points_smoothly([np.array(p) * s * 1.1 for p in pts])
    return VGroup(h, sus.copy().set_opacity(0.4), hau.copy().set_opacity(0.4))


def flower(s=1.0):
    """LS of a simple bisexual flower: receptacle, sepals, petals, stamens (filament + anther), pistil (ovary with ovules, style, stigma)."""
    rec = Ellipse(width=1.6 * s, height=0.5 * s, stroke_width=0, fill_color="#3E7A4A", fill_opacity=1).move_to([0, -1.6 * s, 0])
    stalk = Rectangle(width=0.22 * s, height=1.2 * s, stroke_width=0, fill_color="#3E7A4A", fill_opacity=1).move_to([0, -2.3 * s, 0])
    sep = VGroup(*[Ellipse(width=0.5 * s, height=1.1 * s, stroke_width=0, fill_color="#5FB04A", fill_opacity=1).rotate(d * 0.7).move_to([d * 0.95 * s, -1.25 * s, 0]) for d in (-1, 1)])
    pet = VGroup(*[Ellipse(width=0.9 * s, height=2.3 * s, stroke_width=0, fill_color="#F472B6", fill_opacity=0.85).rotate(d * 0.45).move_to([d * 1.3 * s, -0.2 * s, 0]) for d in (-1, 1)])
    ov = Ellipse(width=0.9 * s, height=1.1 * s, stroke_color="#C5F05C", stroke_width=3, fill_color="#2E5A3C", fill_opacity=1).move_to([0, -1.0 * s, 0])
    ovs = VGroup(*[Ellipse(width=0.18 * s, height=0.26 * s, stroke_width=0, fill_color=INTEG, fill_opacity=1).move_to([dx * s, dy * s, 0]) for dx, dy in [(-0.15, -1.15), (0.15, -1.15), (-0.15, -0.8), (0.15, -0.8)]])
    sty = Rectangle(width=0.16 * s, height=1.6 * s, stroke_width=0, fill_color="#C5F05C", fill_opacity=1).move_to([0, 0.35 * s, 0])
    stg = Ellipse(width=0.55 * s, height=0.25 * s, stroke_width=0, fill_color="#E9F99A", fill_opacity=1).move_to([0, 1.2 * s, 0])
    stam = VGroup()
    for d in (-1, 1):
        fil = Line([d * 0.55 * s, -1.4 * s, 0], [d * 0.75 * s, 0.4 * s, 0], color="#E9F99A", stroke_width=4 * s)
        ant = Ellipse(width=0.3 * s, height=0.55 * s, stroke_width=0, fill_color=EXINE, fill_opacity=1).move_to([d * 0.75 * s, 0.65 * s, 0])
        stam.add(VGroup(fil, ant))
    g = VGroup(stalk, rec, pet, sep, ov, ovs, sty, stg, stam)
    g.parts = dict(sepals=sep, petals=pet, stamens=stam, ovary=ov, ovules=ovs, style=sty, stigma=stg, receptacle=rec)
    return g
