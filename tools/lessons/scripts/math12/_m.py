"""Shared helpers for the Class 12 Mathematics lessons: step-by-step worked examples, captions, tables,
slot boxes, letter tiles, round tables, Pascal's triangle and simple plotting conveniences."""
import os
import sys

import numpy as np
from manim import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bio12"))
from kit import M, T, para, th  # noqa: E402
from _bio import Captions, table, reveal_table, neby_in, neby_out, example_head, card, label, legend  # noqa: E402,F401

GOLD = "#FFD166"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


def worked(s, problem, lines, says, size=36, colors=None, buff=0.32, psize=25):
    """Problem at top-left, then one line per narration sentence (says[0] reads the problem). Lines may be LaTeX strings or mobjects."""
    head, prob = example_head(s, problem, size=psize)
    steps = VGroup(*[M(l_, size=size) if isinstance(l_, str) else l_ for l_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    steps.next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
    for st in steps:
        if st.width > 12.6:
            st.scale_to_fit_width(12.6).align_to(prob, LEFT)
    if steps.get_bottom()[1] < -3.3:
        top = steps.get_top()
        steps.scale((top[1] + 3.3) / steps.height, about_point=steps.get_corner(UL))
    if colors:
        for i, c in enumerate(colors):
            if c:
                steps[i].set_color(c)
    else:
        steps[-1].set_color(th.AMBER)
    with s.say(says[0]):
        s.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
    k = 0
    for sy in says[1:]:
        n = 1
        if isinstance(sy, tuple):
            sy, n = sy
        with s.say(sy):
            for _ in range(n):
                if k < len(steps):
                    s.play(Write(steps[k]), run_time=1.2)
                    k += 1
    while k < len(steps):
        s.play(Write(steps[k]), run_time=0.8)
        k += 1
    s.play(Circumscribe(steps[-1], color=th.AMBER), run_time=0.8)
    s.play(FadeOut(VGroup(head, prob, steps)))


def slots(n, w=1.0, h=1.0, buff=0.25, color=th.MUTED):
    return VGroup(*[RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=3) for _ in range(n)]).arrange(RIGHT, buff=buff)


def num_in(box, v, color=th.AMBER, size=40):
    return T(str(v), size=size, color=color, weight="BOLD").move_to(box)


def tile(ch, color=th.INK, fill=th.PANEL, w=0.62, size=32, stroke=None):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=w * 1.1, stroke_color=stroke or color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    return VGroup(r, T(ch, size=size, color=color, weight="BOLD").move_to(r))


def word(s, vowels="AEIOU", vc=th.AMBER, cc=th.SKY, w=0.62, buff=0.08, size=32):
    return VGroup(*[tile(ch, color=vc if ch in vowels else cc, w=w, size=size) for ch in s]).arrange(RIGHT, buff=buff)


def person(color, r=0.28, label_=None, size=20):
    g = VGroup(Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.9))
    if label_:
        g.add(T(label_, size=size, color="#0B0E1A", weight="BOLD").move_to(g[0]))
    return g


def round_table(n, R=1.6, center=ORIGIN, colors=None, labels=None, r=0.3):
    tab = Circle(radius=R * 0.62, stroke_color=th.MUTED, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to(center)
    seats = VGroup()
    for i in range(n):
        a = PI / 2 - TAU * i / n
        c = (colors[i] if colors else th.PALETTE[i % len(th.PALETTE)])
        seats.add(person(c, r, labels[i] if labels else None).move_to(np.array(center, dtype=float) + polar(R, a)))
    return tab, seats


def pascal(rows, dx=0.85, dy=0.62, size=26, top=(0, 2.6, 0), color=th.INK):
    g = VGroup()
    from math import comb
    for n in range(rows):
        row = VGroup()
        for r in range(n + 1):
            row.add(T(str(comb(n, r)), size=size, color=color, weight="BOLD").move_to(np.array(top) + np.array([(r - n / 2) * dx, -n * dy, 0])))
        g.add(row)
    return g


def head(s, text, size=30):
    return T(text, size=size, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)


def bullets(items, width=11.5, size=24, color=th.INK, buff=0.28):
    return VGroup(*[para(i_, width=width, size=size, color=color) for i_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def reveal_list(s, items, dur, shift=RIGHT * 0.2):
    per = max(0.4, dur / max(1, len(items)))
    for it in items:
        s.play(FadeIn(it, shift=shift), run_time=0.4)
        s.hold(per - 0.4)


def clipped(ax, f, x0, x1, lo, hi, color, width=4, step=0.01):
    """Graph of f on [x0, x1] drawn only where lo <= f <= hi (no flat clamps at the frame edge)."""
    g, cur = VGroup(), []
    for x in np.arange(x0, x1 + step / 2, step):
        y = f(x)
        if lo <= y <= hi:
            cur.append(ax.c2p(x, y))
        else:
            if len(cur) > 1:
                g.add(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(cur))
            cur = []
    if len(cur) > 1:
        g.add(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(cur))
    return g


def grid(rows, bar=None, size=34, dx=0.95, dy=0.62, color=th.INK, bcolor=th.MUTED):
    """Matrix drawn as cells in square brackets; `bar` = column index before which an augmented bar is drawn.
    g.cells[i][j] is each entry, g.rows_ is the list of row groups."""
    nr, nc = len(rows), len(rows[0])
    cells = VGroup()
    for i, r in enumerate(rows):
        row = VGroup()
        for j, v in enumerate(r):
            x = (j - (nc - 1) / 2) * dx + (0.25 if bar is not None and j >= bar else 0)
            row.add(M(str(v), size=size, color=color).move_to([x, -(i - (nr - 1) / 2) * dy, 0]))
        cells.add(row)
    h = nr * dy + 0.1
    left = cells.get_left()[0] - 0.25
    right = cells.get_right()[0] + 0.25
    lb = VMobject(stroke_color=bcolor, stroke_width=3).set_points_as_corners([[left + 0.15, h / 2, 0], [left, h / 2, 0], [left, -h / 2, 0], [left + 0.15, -h / 2, 0]])
    rb = VMobject(stroke_color=bcolor, stroke_width=3).set_points_as_corners([[right - 0.15, h / 2, 0], [right, h / 2, 0], [right, -h / 2, 0], [right - 0.15, -h / 2, 0]])
    g = VGroup(lb, rb, cells)
    if bar is not None:
        bx = ((bar - 0.5) - (nc - 1) / 2) * dx + 0.125
        g.add(DashedLine([bx, h / 2 - 0.05, 0], [bx, -h / 2 + 0.05, 0], color=bcolor, stroke_width=2))
    g.cells = cells
    return g


def set_row(s, g, i, vals, op=None, size=34, color=th.INK, hl=th.AMBER, run_time=0.9):
    """Replace row i of a grid with new values (a row operation), flashing the row and showing the operation label."""
    new = VGroup(*[M(str(v), size=size, color=color).move_to(c) for v, c in zip(vals, g.cells[i])])
    anims = [Transform(c, n_) for c, n_ in zip(g.cells[i], new)]
    lab = None
    if op:
        lab = M(op, size=28, color=hl).next_to(g, RIGHT, buff=0.4).set_y(g.cells[i].get_y())
        s.play(FadeIn(lab, shift=LEFT * 0.2), run_time=0.4)
    rect = SurroundingRectangle(g.cells[i], color=hl, buff=0.08)
    s.play(Create(rect), *anims, run_time=run_time)
    s.play(FadeOut(rect), *([FadeOut(lab)] if lab else []), run_time=0.4)
