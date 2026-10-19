"""Shared layout pieces for the Class 8 Science lessons.

Every helper measures what it draws, so a panel is always exactly big enough for
its text — the most common way a hand-placed slide breaks is a box that was sized
by eye.
"""
from manim import *
import numpy as np

from kit import T, para, th


def card(scene, title, body, color=None, width=4.2, size=20, title_size=26,
         body_color=None, pad=0.42, align="center"):
    """A titled panel that grows to fit its contents."""
    col = color or scene.color
    h = T(title, size=title_size, color=col, weight="BOLD")
    b = para(body, width=width - 2 * pad, size=size, color=body_color or th.BODY) \
        if isinstance(body, str) else body
    inner = VGroup(h, b).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    if inner.width < width - 2 * pad:
        inner.shift(RIGHT * ((width - 2 * pad) - inner.width) / 2)
    box = scene.panel(width, inner.height + 2 * pad * 0.8, color=col)
    inner.move_to(box)
    return VGroup(box, inner)


def table(header, rows, widths, size=23, hsize=19, row_h=0.5, ink=None, mut=None,
          rule=True):
    """A simple ruled table with properly aligned columns. Origin is the top-left."""
    ink = ink or th.INK
    mut = mut or th.MUTED
    xs = []
    x = 0.0
    for w in widths:
        xs.append(x + w / 2)
        x += w
    g = VGroup()
    g.add(VGroup(*[T(h, size=hsize, color=mut).move_to([c, 0, 0]) for h, c in zip(header, xs)]))
    if rule:
        g.add(Line([0, -row_h * 0.55, 0], [sum(widths), -row_h * 0.55, 0],
                   color=th.PANEL_EDGE, stroke_width=2))
    for i, r in enumerate(rows):
        y = -row_h * (i + 1) - 0.05
        g.add(VGroup(*[T(str(v), size=size, color=ink).move_to([c, y, 0])
                       for v, c in zip(r, xs)]))
    return g


def bullets(scene, items, width=9.6, size=24, color=None, mark="dot", buff=0.26):
    """A left-aligned list with a coloured marker per line."""
    col = color or scene.color
    g = VGroup()
    for it in items:
        if mark == "num":
            m = T(str(len(g) + 1), size=size * 0.9, color=col, weight="BOLD")
        elif mark == "check":
            m = VGroup(Circle(radius=0.11, stroke_color=col, stroke_width=2.5))
        else:
            m = Dot(radius=0.06, color=col)
        t = para(it, width=width - 0.5, size=size, color=th.INK) if isinstance(it, str) else it
        g.add(VGroup(m, t).arrange(RIGHT, buff=0.26, aligned_edge=UP))
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return g


def chip(text, color=None, size=22, pad=0.3, fill=th.PANEL):
    """A small rounded label."""
    col = color or th.SKY
    t = T(text, size=size, color=col, weight="SEMIBOLD")
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 2 * pad, height=t.height + 1.6 * pad,
                           stroke_color=col, stroke_width=1.8, fill_color=fill, fill_opacity=0.9)
    t.move_to(box)
    return VGroup(box, t)


def stat(value, label, color=None, size=44, lsize=20):
    """A big number over a small caption."""
    col = color or th.AMBER
    v = T(value, size=size, color=col, weight="BOLD", display=True)
    l = T(label, size=lsize, color=th.MUTED)
    return VGroup(v, l).arrange(DOWN, buff=0.12)


def ring(n, center, radius, color=None, labels=None, label_gap=0.95, label_size=21,
         node_r=0.24, start=PI / 2, clockwise=True):
    """n nodes evenly on a circle, with labels outside. Returns (nodes, labels, ring)."""
    col = color or th.SKY
    nodes, tags = VGroup(), VGroup()
    for i in range(n):
        a = start + (-1 if clockwise else 1) * i * TAU / n
        p = center + radius * np.array([np.cos(a), np.sin(a), 0])
        nodes.add(VGroup(Circle(radius=node_r, fill_color=th.PANEL, fill_opacity=1,
                                stroke_color=col, stroke_width=2.5).move_to(p),
                         T(str(i + 1), size=node_r * 78, color=col, weight="BOLD").move_to(p)))
        if labels:
            lp = center + (radius + label_gap) * np.array([np.cos(a), np.sin(a), 0])
            tags.add(T(labels[i], size=label_size, color=th.INK, weight="SEMIBOLD").move_to(lp))
    circ = Circle(radius=radius, color=th.FAINT, stroke_width=2).move_to(center).set_stroke(opacity=0.45)
    return nodes, tags, circ


def angle_of(i, n, start=PI / 2, clockwise=True):
    return start + (-1 if clockwise else 1) * i * TAU / n


def at(center, radius, i, n, start=PI / 2, clockwise=True):
    a = angle_of(i, n, start, clockwise)
    return center + radius * np.array([np.cos(a), np.sin(a), 0])


def arrow_between(a, b, color=None, width=3.0, tip=0.16, dashed=False):
    col = color or th.FAINT
    if dashed:
        l = DashedLine(a, b, color=col, stroke_width=width, dash_length=0.12)
    else:
        l = Line(a, b, color=col, stroke_width=width)
    return l.add_tip(tip_length=tip) if hasattr(l, "add_tip") else l


def callout_text(scene, kind, body, width=10.0, size=26):
    return scene.callout(kind, body, width=width, size=size)
