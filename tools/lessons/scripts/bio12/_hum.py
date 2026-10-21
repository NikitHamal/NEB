"""Human biology drawing helpers: gut, villus, lungs, heart with valves and flow, ECG and action-potential traces,
nephron, eye ray diagrams, ear chain and menstrual-cycle hormone curves."""
import numpy as np
from manim import *

from kit import T, para, th

OXY = "#FF5A5F"
DEOXY = "#5C7CFA"
GUT = "#E8A0BF"
BILE = "#C5F05C"
LYMPH = "#FFE08A"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


def gut_path():
    """Centre-line of a simplified alimentary canal from mouth (top) to anus (bottom), in a 5 x 6 box at origin."""
    pts = [[0, 3.0], [0, 2.2], [0.05, 1.2], [0.6, 0.9], [1.3, 0.6], [1.1, 0.0], [0.4, 0.05], [0.1, -0.3], [-0.6, -0.3], [-0.9, -0.7], [0.0, -0.9], [0.8, -0.8],
           [0.9, -1.3], [0.0, -1.5], [-0.8, -1.4], [-1.5, -1.2], [-1.5, 0.5], [1.6, 0.5], [1.6, -1.9], [0.3, -2.3], [0.3, -3.0]]
    return VMobject().set_points_smoothly([np.array([x, y, 0]) for x, y in pts])


def villus(h=3.0, w=1.0):
    pts = [[-w / 2, 0, 0], [-w / 2, h * 0.8, 0], [0, h, 0], [w / 2, h * 0.8, 0], [w / 2, 0, 0]]
    outer = VMobject(stroke_color=GUT, stroke_width=4, fill_color="#3A2030", fill_opacity=1).set_points_smoothly(pts)
    brush = VGroup(*[Line(p_, p_ + (p_ - np.array([0, h * 0.45, 0])) / np.linalg.norm(p_ - np.array([0, h * 0.45, 0])) * 0.12, color=GUT, stroke_width=2)
                     for p_ in [outer.point_from_proportion(t) for t in np.linspace(0.03, 0.97, 34)]])
    cap = VMobject(stroke_color=OXY, stroke_width=4).set_points_smoothly([[-w * 0.3, 0.1, 0], [-w * 0.3, h * 0.7, 0], [0, h * 0.85, 0], [w * 0.3, h * 0.7, 0], [w * 0.3, 0.1, 0]])
    lac = Line([0, 0.1, 0], [0, h * 0.72, 0], color=LYMPH, stroke_width=7)
    g = VGroup(outer, brush, cap, lac)
    g.parts = dict(wall=outer, brush=brush, capillary=cap, lacteal=lac)
    return g


def heart(s=1.0):
    """Four-chamber schematic, viewed from the front (patient's right on screen left)."""
    RA = RoundedRectangle(corner_radius=0.3, width=1.6 * s, height=1.4 * s, stroke_color=DEOXY, stroke_width=4, fill_color=DEOXY, fill_opacity=0.25).move_to([-0.95 * s, 0.85 * s, 0])
    LA = RoundedRectangle(corner_radius=0.3, width=1.6 * s, height=1.4 * s, stroke_color=OXY, stroke_width=4, fill_color=OXY, fill_opacity=0.25).move_to([0.95 * s, 0.85 * s, 0])
    RV = RoundedRectangle(corner_radius=0.4, width=1.6 * s, height=2.0 * s, stroke_color=DEOXY, stroke_width=4, fill_color=DEOXY, fill_opacity=0.25).move_to([-0.95 * s, -1.0 * s, 0])
    LV = RoundedRectangle(corner_radius=0.4, width=1.6 * s, height=2.0 * s, stroke_color=OXY, stroke_width=8, fill_color=OXY, fill_opacity=0.25).move_to([0.95 * s, -1.0 * s, 0])
    sept = Line([0, 1.55 * s, 0], [0, -2.0 * s, 0], color=th.MUTED, stroke_width=6)
    tri = VGroup(*[Line([-0.95 * s + d * 0.35 * s, 0.15 * s, 0], [-0.95 * s + d * 0.15 * s, -0.25 * s, 0], color=WHITE, stroke_width=4) for d in (-1, 1)])
    bi = VGroup(*[Line([0.95 * s + d * 0.35 * s, 0.15 * s, 0], [0.95 * s + d * 0.15 * s, -0.25 * s, 0], color=WHITE, stroke_width=4) for d in (-1, 1)])
    g = VGroup(RA, LA, RV, LV, sept, tri, bi)
    g.parts = dict(RA=RA, LA=LA, RV=RV, LV=LV, septum=sept, tricuspid=tri, bicuspid=bi)
    return g


def ecg_points(beats=3, x0=-5.5, width=11.0, y0=0.0, amp=1.0):
    pts = []
    per = width / beats
    for b in range(beats):
        bx = x0 + b * per
        prof = [(0.00, 0), (0.10, 0), (0.15, 0.15), (0.20, 0), (0.28, 0), (0.31, -0.12), (0.34, 1.0), (0.37, -0.25), (0.40, 0), (0.55, 0), (0.62, 0.28), (0.70, 0), (1.00, 0)]
        for f, v in prof:
            pts.append(np.array([bx + f * per, y0 + v * amp, 0]))
    return pts


def action_potential(ax):
    def v(t):
        if t < 1.0:
            return -70
        if t < 1.3:
            return -70 + (t - 1.0) / 0.3 * 15
        if t < 1.7:
            return -55 + (t - 1.3) / 0.4 * 90
        if t < 2.6:
            return 35 - (t - 1.7) / 0.9 * 115
        if t < 3.6:
            return -80 + (t - 2.6) / 1.0 * 10
        return -70
    return ax.plot(v, x_range=[0, 5, 0.02], color=th.AMBER, stroke_width=5)


def nephron(s=1.0):
    """Schematic nephron: glomerulus + Bowman's capsule (top left), PCT, loop of Henle (down into medulla), DCT, collecting duct (right)."""
    cap = Arc(radius=0.55 * s, start_angle=PI * 0.2, angle=PI * 1.6, stroke_color=th.SKY, stroke_width=6).move_arc_center_to([-4.0 * s, 1.6 * s, 0])
    glom = VGroup(*[Circle(radius=0.12 * s, stroke_color=OXY, stroke_width=3).move_to([-4.0 * s + dx * s, 1.6 * s + dy * s, 0]) for dx, dy in [(-0.15, 0.1), (0.12, 0.15), (0.0, -0.12), (0.18, -0.08), (-0.18, -0.1)]])
    aff = Line([-5.2 * s, 2.0 * s, 0], [-4.2 * s, 1.7 * s, 0], color=OXY, stroke_width=9)
    eff = Line([-4.1 * s, 1.75 * s, 0], [-5.0 * s, 2.6 * s, 0], color=OXY, stroke_width=5)
    tub_pts = [[-3.55, 1.85], [-2.8, 2.3], [-2.2, 1.8], [-2.7, 1.3], [-2.0, 1.0], [-1.4, 1.4], [-1.0, 0.8], [-1.0, -2.2], [-0.6, -2.5], [-0.2, -2.2], [-0.2, 0.6],
               [0.4, 1.2], [1.0, 0.8], [0.7, 1.6], [1.3, 2.0], [1.9, 1.8]]
    tub = VMobject(stroke_color=th.MINT, stroke_width=8).set_points_smoothly([np.array([x * s, y * s, 0]) for x, y in tub_pts])
    cd = Line([1.9 * s, 2.6 * s, 0], [1.9 * s, -2.8 * s, 0], color=th.AMBER, stroke_width=10)
    medulla = Rectangle(width=6.6 * s, height=3.2 * s, stroke_width=0, fill_color="#3A1E2A", fill_opacity=0.6).move_to([-1.5 * s, -1.5 * s, 0])
    g = VGroup(medulla, aff, eff, glom, cap, tub, cd)
    g.parts = dict(capsule=cap, glomerulus=glom, afferent=aff, efferent=eff, tubule=tub, duct=cd, medulla=medulla)
    return g


def eye(length=3.0, s=1.0):
    ball = Ellipse(width=length * s, height=2.6 * s, stroke_color=WHITE, stroke_width=3)
    lens = Ellipse(width=0.35 * s, height=1.1 * s, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.3).move_to([-length / 2 * s + 0.45 * s, 0, 0])
    retina = Arc(radius=1.3 * s, start_angle=-PI / 2.6, angle=2 * PI / 2.6, stroke_color=th.CORAL, stroke_width=6).move_arc_center_to([length / 2 * s - 1.3 * s, 0, 0])
    return VGroup(ball, lens, retina)


def hormone_curves(ax):
    """FSH, LH, oestrogen and progesterone over a 28-day cycle (schematic, normalised 0..1)."""
    g = lambda d, m, w: np.exp(-((d - m) / w) ** 2)
    fsh = ax.plot(lambda d: 0.25 + 0.2 * g(d, 3, 3) + 0.35 * g(d, 13.5, 0.9), x_range=[0, 28, 0.1], color=th.SKY, stroke_width=4)
    lh = ax.plot(lambda d: 0.12 + 0.85 * g(d, 13.8, 0.8), x_range=[0, 28, 0.1], color=th.AMBER, stroke_width=4)
    oes = ax.plot(lambda d: 0.15 + 0.6 * g(d, 12.5, 2.2) + 0.3 * g(d, 21, 3.5), x_range=[0, 28, 0.1], color=th.PINK, stroke_width=4)
    pro = ax.plot(lambda d: 0.05 + 0.7 * g(d, 21, 3.5), x_range=[0, 28, 0.1], color=th.MINT, stroke_width=4)
    return VGroup(fsh, lh, oes, pro)
