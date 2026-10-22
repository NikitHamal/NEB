"""Shared helpers for the Class 12 English lessons: quotation cards, season/plot timelines, character cards,
houses and fences, emotion curves and sentence-transformation strips for the grammar units. Reuses the maths/biology
helpers (head, bullets, table, Captions …)."""
import os
import sys

import numpy as np
from manim import *

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "math12"))
sys.path.insert(0, os.path.join(HERE, "..", "bio12"))
from kit import M, T, para, th  # noqa: E402
from _m import head, bullets, reveal_list, table, reveal_table, neby_in, neby_out, Captions, example_head  # noqa: E402,F401


def quote(text, who=None, width=9.0, size=30, color=th.INK, accent=th.AMBER):
    """A quotation card: big opening mark, the words, an optional attribution. Keep quotations short."""
    body = para(text, width=width, size=size, color=color)
    mark = T("“", size=size * 3, color=accent, weight="BOLD").next_to(body, LEFT, buff=0.25).align_to(body, UP).shift(UP * 0.25)
    g = VGroup(mark, body)
    if who:
        g.add(T("— " + who, size=max(22, size - 6), color=th.MUTED).next_to(body, DOWN, buff=0.25).align_to(body, RIGHT))
    bar = Line(g.get_corner(UL) + LEFT * 0.2, g.get_corner(DL) + LEFT * 0.2, color=accent, stroke_width=4)
    out = VGroup(bar, g)
    out.body = body
    return out


def card(title, text, color, w=3.9, h=3.2, tsize=28, size=24):
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    inner = VGroup(T(title, size=tsize, color=color, weight="BOLD"), para(text, width=w - 0.5, size=size, color=th.BODY)).arrange(DOWN, buff=0.25)
    inner.scale_to_fit_width(min(inner.width, w - 0.3))
    if inner.height > h - 0.3:
        inner.scale_to_fit_height(h - 0.3)
    return VGroup(box, inner.move_to(box))


def timeline(labels, x0=-6.0, x1=6.0, y=0.0, colors=None, size=22, up_down=True, wrap=2.4):
    """Arrow with a dot per label; labels alternate above/below. Returns group with .dots, .labels, .line."""
    line = Arrow([x0, y, 0], [x1, y, 0], buff=0, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.03)
    n = len(labels)
    xs = np.linspace(x0 + 0.5, x1 - 0.7, n)
    dots, labs = VGroup(), VGroup()
    for k, (x, l_) in enumerate(zip(xs, labels)):
        c_ = colors[k] if colors else th.PALETTE[k % len(th.PALETTE)]
        dots.add(Dot([x, y, 0], radius=0.11, color=c_))
        lab = para(l_, width=wrap, size=size, color=c_)
        side = UP if (k % 2 == 0 or not up_down) else DOWN
        lab.next_to(dots[-1], side, buff=0.3)
        labs.add(lab)
    g = VGroup(line, dots, labs)
    g.line, g.dots, g.labels = line, dots, labs
    return g


def house(color, w=2.2, h=1.5, label=None, size=22):
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.12)
    roof = Polygon(body.get_corner(UL) + LEFT * 0.15, body.get_corner(UR) + RIGHT * 0.15, body.get_top() + UP * h * 0.55, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    door = Rectangle(width=w * 0.22, height=h * 0.5, stroke_color=color, stroke_width=2).align_to(body, DOWN)
    win = VGroup(*[Square(w * 0.18, stroke_color=color, stroke_width=2).move_to(body.get_center() + np.array([dx * w * 0.28, h * 0.12, 0])) for dx in (-1, 1)])
    g = VGroup(body, roof, door, win)
    if label:
        g.add(para(label, width=w + 0.6, size=size, color=color).next_to(body, DOWN, buff=0.2))
    return g


def fence(x, y0=-1.6, y1=-0.2, n=6, color=th.MUTED):
    ys = np.linspace(y0, y1, n)
    posts = VGroup(*[Line([x - 0.12, yy, 0], [x + 0.12, yy, 0], color=color, stroke_width=3) for yy in ys])
    rail = Line([x, y0 - 0.1, 0], [x, y1 + 0.1, 0], color=color, stroke_width=4)
    return VGroup(rail, posts)


def chip(text, color, size=22):
    t = T(text, size=size, color=th.BG if color != th.INK else th.BG, weight="BOLD")
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.35, height=t.height + 0.25, stroke_width=0, fill_color=color, fill_opacity=0.95)
    return VGroup(r, t.move_to(r))


def arc_curve(ax, xs, ys, color=th.AMBER, width=5):
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts)


def device_slide(s, rows, say, widths=(3.0, 5.0, 4.6), y=0.4, size=22):
    """Literary devices table: device | example | effect."""
    tb = table([["device", "example", "effect"]] + rows, list(widths), row_h=0.62, size=size, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, y, 0])
    with s.say(say) as v:
        reveal_table(s, tb, v.dur * 0.85)
    s.play(FadeOut(tb))


def transform_strip(before, after, label=None, size=30, bcolor=th.INK, acolor=th.MINT, y=0.0):
    """Sentence transformation: before → after, with an optional rule label beneath."""
    b = T(before, size=size, color=bcolor)
    a = T(after, size=size, color=acolor)
    g = VGroup(b, Arrow(LEFT * 0.5, RIGHT * 0.5, color=th.MUTED, stroke_width=4), a).arrange(RIGHT, buff=0.3)
    if g.width > 12.6:
        g = VGroup(b, Arrow(UP * 0.3, DOWN * 0.3, color=th.MUTED, stroke_width=4), a).arrange(DOWN, buff=0.15)
        for m_ in (b, a):
            if m_.width > 12.6:
                m_.scale_to_fit_width(12.6)
    g.move_to([0, y, 0])
    if label:
        g.add(T(label, size=24, color=th.AMBER).next_to(g, DOWN, buff=0.25))
    return g


# ---------------------------------------------------------------- grammar helpers
def sentence(s, size=34, color=th.INK, weight="NORMAL"):
    """A sentence as one Text, with .words[i] = the glyphs of the i-th space-separated word (for marking and moving)."""
    t = T(s, size=size, color=color, weight=weight)
    ws, k = VGroup(), 0
    for w in s.split():
        ws.add(VGroup(*t[k:k + len(w)]))
        k += len(w)
    t.words = ws
    return t


def mark(m, color=th.AMBER, buff=0.07):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.06, stroke_width=3)


def strike(m, color=th.CORAL):
    return Line(m.get_left() + LEFT * 0.05, m.get_right() + RIGHT * 0.05, color=color, stroke_width=4)


def wrong_right(wrong, right, size=28, rule=None, rule_color=th.MUTED):
    """✗ wrong (struck) above ✓ right, with an optional rule line underneath. Returns group with .wrong .right .cross."""
    w = VGroup(T("✗", size=size, color=th.CORAL, weight="BOLD"), T(wrong, size=size, color=th.CORAL)).arrange(RIGHT, buff=0.25)
    r = VGroup(T("✓", size=size, color=th.MINT, weight="BOLD"), T(right, size=size, color=th.MINT)).arrange(RIGHT, buff=0.25)
    g = VGroup(w, r).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    if rule:
        g.add(T(rule, size=max(22, size - 6), color=rule_color).next_to(g, DOWN, buff=0.15).align_to(g, LEFT))
    g.cross = strike(w[1])
    g.add(g.cross)  # a submobject, so it travels with the group; animate it in with Create(g.cross)
    g.wrong, g.right = w, r
    return g
