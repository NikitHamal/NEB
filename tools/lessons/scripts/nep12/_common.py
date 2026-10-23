"""Shared helpers for the Class 12 Nepali (nep12) lesson videos.

Everything here draws with shapes and Devanagari text only, so nothing Latin can reach
the screen. Functions that need narration or Nepali digits take the Lesson scene `s`."""
from manim import *
import numpy as np

from kit import T, para, th

SKIN = "#C98B5E"
SKIN2 = "#B5774B"
HAIR = "#1E1A22"
SARI = "#C2394B"
SARI2 = "#E2A93B"
SHIRT = "#3E7CB1"
LEAF = "#5FBF6A"
EARTH = "#3A2F2A"


# ------------------------------------------------------------------ kinetic typography
def kline(text, size=44, color=th.INK, hl=None, weight="BOLD"):
    """One line of text whose words are addressable as .words (for word-by-word reveals).
    hl maps a substring to a colour; any word containing it is coloured."""
    t = T(text, size=size, color=color, weight=weight)
    words = text.split()
    parts = VGroup()
    idx = 0
    ok = True
    for w in words:
        n = len(T(w, size=size, weight=weight).submobjects)
        if idx + n > len(t.submobjects):
            ok = False
            break
        parts.add(VGroup(*t.submobjects[idx: idx + n]))
        idx += n
    if not ok or idx != len(t.submobjects):
        parts = VGroup(VGroup(*t.submobjects))
        words = [text]
    if hl:
        for w, p in zip(words, parts):
            for key, col in hl.items():
                if key in w:
                    p.set_color(col)
    t.words = parts
    return t


def kblock(lines, size=44, color=th.INK, hl=None, buff=0.28, weight="BOLD"):
    g = VGroup(*[kline(l, size=size, color=color, hl=hl, weight=weight) for l in lines])
    g.arrange(DOWN, buff=buff)
    return g


def words_of(block):
    out = []
    for line in block:
        out.extend(list(line.words))
    return out


def type_in(s, block, run_time=2.0, shift=UP * 0.18, lag=None):
    ws = words_of(block)
    if not ws:
        return
    lag = lag if lag is not None else min(0.5, 2.4 / max(1, len(ws)))
    s.play(LaggedStart(*[FadeIn(w, shift=shift, scale=1.08) for w in ws], lag_ratio=lag), run_time=run_time)


def quote_frame(block, color, pad=0.45):
    """Decorative frame for a quoted line: a glowing left bar and two drawn quote ticks."""
    box = RoundedRectangle(corner_radius=0.2, width=block.width + pad * 2 + 0.3, height=block.height + pad * 2,
                           stroke_color=color, stroke_width=2, fill_color=th.PANEL, fill_opacity=0.9).move_to(block)
    bar = Rectangle(width=0.1, height=box.height - 0.35, stroke_width=0, fill_color=color, fill_opacity=1)
    bar.move_to(box.get_left() + RIGHT * 0.22)
    ticks = VGroup()
    for k in range(2):
        d = Dot(radius=0.07, color=color)
        tail = Line(ORIGIN, DOWN * 0.18 + LEFT * 0.06, color=color, stroke_width=4)
        tail.shift(d.get_center() + RIGHT * 0.05)
        ticks.add(VGroup(d, tail).shift(RIGHT * 0.2 * k))
    ticks.move_to(box.get_corner(UL) + RIGHT * 0.65 + DOWN * 0.05)
    bg = BackgroundRectangle(ticks, color=th.BG, fill_opacity=1, buff=0.08)
    return VGroup(box, bar, bg, ticks)


def show_quote(s, lines, narration, color=None, size=44, hl=None, where=ORIGIN, keep=False, after=None):
    """Kinetic reveal of a key line inside a frame while narration plays."""
    color = color or s.color
    block = kblock(lines, size=size, hl=hl)
    if block.width > 12.0:
        block.scale_to_fit_width(12.0)
    block.move_to(where)
    fr = quote_frame(block, color)
    with s.say(narration) as v:
        s.play(FadeIn(fr, scale=0.96), run_time=0.5)
        s.sfx("type", gain=-14)
        type_in(s, block, run_time=min(max(1.2, v.dur * 0.6), 4.0))
        if after:
            after(block)
    g = VGroup(fr, block)
    if not keep:
        s.play(FadeOut(g), run_time=0.45)
    return g


# ------------------------------------------------------------------ boxes, cards, bubbles
def box(w, h, color=th.PANEL_EDGE, fill=th.PANEL, opacity=0.92, r=0.18, sw=2):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=fill, fill_opacity=opacity)


def card(head, body, color, w=3.8, h=2.0, hsize=30, bsize=22):
    b = box(w, h, color=color)
    hh = T(head, size=hsize, color=color, weight="BOLD")
    if hh.width > w - 0.4:
        hh.scale_to_fit_width(w - 0.4)
    items = [hh]
    if body:
        bb = para(body, width=w - 0.5, size=bsize, color=th.BODY, align="center")
        items.append(bb)
    inner = VGroup(*items).arrange(DOWN, buff=0.2)
    if inner.height > h - 0.3:
        inner.scale_to_fit_height(h - 0.3)
    inner.move_to(b)
    return VGroup(b, inner)


def pill(text, color, size=24, fill_opacity=0.18):
    t = T(text, size=size, color=color, weight="SEMIBOLD")
    b = RoundedRectangle(corner_radius=0.22, width=t.width + 0.5, height=t.height + 0.32, stroke_color=color,
                         stroke_width=2, fill_color=color, fill_opacity=fill_opacity)
    t.move_to(b)
    return VGroup(b, t)


def bubble(text, color=th.INK, size=28, width=4.6, tail=DOWN + LEFT, fill="#20264A"):
    body = para(text, width=width, size=size, color=color, align="center")
    b = RoundedRectangle(corner_radius=0.3, width=body.width + 0.6, height=body.height + 0.45, stroke_color=th.PANEL_EDGE,
                         stroke_width=2, fill_color=fill, fill_opacity=1)
    body.move_to(b)
    edge = b.get_bottom() if tail[1] < 0 else b.get_top()
    x = -0.4 if tail[0] < 0 else 0.4
    p0 = edge + RIGHT * x
    tip = p0 + RIGHT * (x * 0.9) + (DOWN if tail[1] < 0 else UP) * 0.42
    tri = Polygon(p0 + LEFT * 0.18, p0 + RIGHT * 0.18, tip, stroke_width=0, fill_color=fill, fill_opacity=1)
    tri.shift((UP if tail[1] < 0 else DOWN) * 0.03)
    return VGroup(tri, b, body)


def badge(s, n, color, r=0.28):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_width=0)
    t = T(s.num(n), size=int(r * 80), color=th.BG, weight="BOLD").move_to(c)
    return VGroup(c, t)


def heading(text, color=th.INK, size=40):
    return T(text, size=size, color=color, weight="BOLD").to_edge(UP, buff=0.75)


# ------------------------------------------------------------------ scenery
def sky(top="#141A3A", bottom="#2B2350", n=10):
    w, h = config.frame_width, config.frame_height
    bands = VGroup()
    for i in range(n):
        c = interpolate_color(ManimColor(top), ManimColor(bottom), i / (n - 1))
        r = Rectangle(width=w + 0.2, height=h / n + 0.02, stroke_width=0, fill_color=c, fill_opacity=1)
        r.move_to([0, h / 2 - h / n * (i + 0.5), 0])
        bands.add(r)
    return bands


def stars(n=40, seed=3, y0=0.3):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        x = rng.uniform(-6.9, 6.9)
        y = rng.uniform(y0, 3.6)
        g.add(Dot([x, y, 0], radius=rng.uniform(0.012, 0.035), color=WHITE, fill_opacity=rng.uniform(0.4, 0.95)))
    return g


def ridge(seed, base=-3.7, y_lo=-1.0, y_hi=1.2, n=9, color="#2C3566", snow=False, x0=-7.3, x1=7.3):
    rng = np.random.default_rng(seed)
    xs = np.linspace(x0, x1, n)
    ys = rng.uniform(y_lo, y_hi, n)
    ys[::2] = rng.uniform(y_lo, y_lo + (y_hi - y_lo) * 0.45, len(ys[::2]))
    pts = [[x0, base, 0]] + [[x, y, 0] for x, y in zip(xs, ys)] + [[x1, base, 0]]
    poly = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=1)
    g = VGroup(poly)
    if snow:
        caps = VGroup()
        for i in range(1, n - 1):
            if ys[i] > ys[i - 1] and ys[i] > ys[i + 1] and ys[i] > y_lo + (y_hi - y_lo) * 0.55:
                p = np.array([xs[i], ys[i], 0])
                l = np.array([xs[i - 1], ys[i - 1], 0])
                r = np.array([xs[i + 1], ys[i + 1], 0])
                a = p + (l - p) * 0.22
                b = p + (r - p) * 0.22
                mid = (a + b) / 2 + DOWN * 0.05
                caps.add(Polygon(p, a, mid + LEFT * 0.08 + UP * 0.04, mid, mid + RIGHT * 0.08 + UP * 0.04, b,
                                 stroke_width=0, fill_color="#EEF3FF", fill_opacity=0.95))
        g.add(caps)
    return g


def himalaya(seed=1, far="#36407A", mid="#232B57", near="#1A2045"):
    return VGroup(
        ridge(seed, y_lo=0.0, y_hi=2.0, n=11, color=far, snow=True),
        ridge(seed + 5, y_lo=-1.2, y_hi=0.3, n=9, color=mid),
        ridge(seed + 9, y_lo=-2.4, y_hi=-1.6, n=7, color=near),
    )


def sun(r=0.7, color=th.AMBER, rays=12):
    glow = VGroup(*[Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=0.07) for k in (1.6, 2.1, 2.7)])
    disc = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)
    ry = VGroup(*[Line(ORIGIN, RIGHT * r * 0.45, color=color, stroke_width=4).shift(RIGHT * r * 1.2).rotate(a, about_point=ORIGIN)
                  for a in np.linspace(0, TAU, rays, endpoint=False)])
    return VGroup(glow, ry, disc)


def moon(r=0.5, color="#F3EBC8"):
    m = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1)
    glow = VGroup(*[Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=0.06) for k in (1.5, 2.1)])
    craters = VGroup(Circle(radius=r * 0.16, stroke_width=0, fill_color="#D9CFA6", fill_opacity=1).shift(LEFT * r * 0.3 + UP * r * 0.2),
                     Circle(radius=r * 0.1, stroke_width=0, fill_color="#D9CFA6", fill_opacity=1).shift(RIGHT * r * 0.35 + DOWN * r * 0.25))
    return VGroup(glow, m, craters)


def tree(h=1.6, color=LEAF, trunk="#6B4A32"):
    tr = Rectangle(width=h * 0.09, height=h * 0.35, stroke_width=0, fill_color=trunk, fill_opacity=1)
    tiers = VGroup()
    for k in range(3):
        w = h * (0.62 - k * 0.14)
        tri = Triangle(stroke_width=0, fill_color=interpolate_color(ManimColor(color), ManimColor("#1F4D2A"), 0.25 * k),
                       fill_opacity=1).stretch_to_fit_width(w).stretch_to_fit_height(h * 0.42)
        tri.move_to(UP * (h * 0.3 + k * h * 0.2))
        tiers.add(tri)
    tr.move_to(UP * h * 0.08)
    g = VGroup(tr, tiers)
    g.shift(-g.get_bottom())
    return g


def forest(n=9, x0=-6.5, x1=6.5, y=-2.6, seed=2, hmin=1.2, hmax=2.2, color=LEAF):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for x in np.linspace(x0, x1, n):
        t = tree(rng.uniform(hmin, hmax), color=color)
        t.move_to([x + rng.uniform(-0.25, 0.25), y, 0], aligned_edge=DOWN)
        g.add(t)
    return g


def hut(w=2.2, wall="#8A6A4A", roof="#5A3A28", lamp=True):
    body = Rectangle(width=w, height=w * 0.62, stroke_width=0, fill_color=wall, fill_opacity=1)
    rf = Polygon(body.get_corner(UL) + LEFT * 0.25, body.get_corner(UR) + RIGHT * 0.25,
                 body.get_top() + UP * w * 0.42, stroke_width=0, fill_color=roof, fill_opacity=1)
    door = Rectangle(width=w * 0.22, height=w * 0.38, stroke_width=0, fill_color="#3A271B", fill_opacity=1)
    door.move_to(body.get_bottom(), aligned_edge=DOWN).shift(LEFT * w * 0.18)
    win = Rectangle(width=w * 0.2, height=w * 0.18, stroke_width=0, fill_color="#FFD27A" if lamp else "#2A2A3A", fill_opacity=1)
    win.move_to(body.get_center() + RIGHT * w * 0.22 + UP * w * 0.04)
    g = VGroup(body, rf, door, win)
    if lamp:
        glow = VGroup(*[Circle(radius=w * k, stroke_width=0, fill_color="#FFD27A", fill_opacity=0.05).move_to(win) for k in (0.18, 0.28, 0.4)])
        g.add(glow)
    return g


def mother(h=2.6, sari=SARI, border=SARI2):
    """A seated-free standing woman in a sari, built from shapes. Bottom at origin."""
    u = h / 2.6
    head = Circle(radius=0.27 * u, stroke_width=0, fill_color=SKIN, fill_opacity=1).move_to(UP * 2.25 * u)
    hair = Circle(radius=0.29 * u, stroke_width=0, fill_color=HAIR, fill_opacity=1).move_to(UP * 2.32 * u)
    bun = Circle(radius=0.15 * u, stroke_width=0, fill_color=HAIR, fill_opacity=1).move_to(UP * 2.3 * u + LEFT * 0.3 * u)
    tika = Dot(UP * 2.32 * u + RIGHT * 0.12 * u, radius=0.035 * u, color="#E5383B")
    neck = Rectangle(width=0.14 * u, height=0.18 * u, stroke_width=0, fill_color=SKIN2, fill_opacity=1).move_to(UP * 1.95 * u)
    body = Polygon([-0.38 * u, 1.85 * u, 0], [0.38 * u, 1.85 * u, 0], [0.62 * u, 0, 0], [-0.62 * u, 0, 0],
                   stroke_width=0, fill_color=sari, fill_opacity=1)
    hem = Polygon([-0.62 * u, 0, 0], [0.62 * u, 0, 0], [0.58 * u, 0.14 * u, 0], [-0.58 * u, 0.14 * u, 0],
                  stroke_width=0, fill_color=border, fill_opacity=1)
    pallu = Polygon([0.38 * u, 1.85 * u, 0], [-0.15 * u, 1.85 * u, 0], [-0.5 * u, 0.7 * u, 0], [-0.3 * u, 0.62 * u, 0],
                    stroke_width=0, fill_color=border, fill_opacity=0.85)
    arm = Line([0.36 * u, 1.7 * u, 0], [0.55 * u, 1.0 * u, 0], color=SKIN, stroke_width=9 * u)
    g = VGroup(body, hem, pallu, arm, neck, hair, bun, head, tika)
    g.head = head
    return g


def child(h=1.5, shirt=SHIRT, topi=True):
    u = h / 1.5
    head = Circle(radius=0.22 * u, stroke_width=0, fill_color=SKIN, fill_opacity=1).move_to(UP * 1.26 * u)
    hair = Circle(radius=0.23 * u, stroke_width=0, fill_color=HAIR, fill_opacity=1).move_to(UP * 1.3 * u)
    parts = [hair, head]
    if topi:
        cap = Polygon([-0.21 * u, 1.42 * u, 0], [0.21 * u, 1.42 * u, 0], [0.17 * u, 1.62 * u, 0], [-0.14 * u, 1.6 * u, 0],
                      stroke_width=0, fill_color="#B23A48", fill_opacity=1)
        dots = VGroup(*[Dot([x * u, 1.5 * u, 0], radius=0.02 * u, color=SARI2) for x in (-0.1, 0.0, 0.1)])
        parts += [cap, dots]
    body = Polygon([-0.25 * u, 1.04 * u, 0], [0.25 * u, 1.04 * u, 0], [0.3 * u, 0.5 * u, 0], [-0.3 * u, 0.5 * u, 0],
                   stroke_width=0, fill_color=shirt, fill_opacity=1)
    legs = VGroup(Line([-0.12 * u, 0.5 * u, 0], [-0.14 * u, 0, 0], color="#2B2B3A", stroke_width=10 * u),
                  Line([0.12 * u, 0.5 * u, 0], [0.14 * u, 0, 0], color="#2B2B3A", stroke_width=10 * u))
    g = VGroup(legs, body, *parts)
    g.head = head
    return g


def person(h=1.6, color="#6C7AA8"):
    """A plain silhouette for crowds."""
    u = h / 1.6
    head = Circle(radius=0.19 * u, stroke_width=0, fill_color=color, fill_opacity=1).move_to(UP * 1.42 * u)
    body = RoundedRectangle(corner_radius=0.15 * u, width=0.52 * u, height=1.0 * u, stroke_width=0, fill_color=color,
                            fill_opacity=1).move_to(UP * 0.55 * u)
    return VGroup(body, head)


def leaf(size=0.35, color=LEAF):
    a = ArcBetweenPoints(LEFT * size, RIGHT * size, angle=-PI / 2.2)
    b = ArcBetweenPoints(RIGHT * size, LEFT * size, angle=-PI / 2.2)
    shape = VMobject(stroke_width=0, fill_color=color, fill_opacity=1)
    shape.set_points(np.concatenate([a.points, b.points]))
    rib = Line(LEFT * size * 0.9, RIGHT * size * 0.9, color=interpolate_color(ManimColor(color), ManimColor(BLACK), 0.35), stroke_width=1.5)
    return VGroup(shape, rib)


def flame(h=1.0, color=th.CORAL, inner=th.AMBER):
    def drop(hh, col):
        pts = [np.array([0, hh, 0]), np.array([0.32 * hh, 0.25 * hh, 0]), np.array([0, -0.05 * hh, 0]), np.array([-0.32 * hh, 0.25 * hh, 0])]
        v = VMobject(stroke_width=0, fill_color=col, fill_opacity=1)
        v.set_points_smoothly(pts + [pts[0]])
        return v
    o = drop(h, color)
    i = drop(h * 0.55, inner).shift(DOWN * 0.02)
    return VGroup(o, i)


def snowflake(r=0.5, color="#BFE3FF"):
    g = VGroup()
    for a in np.linspace(0, TAU, 6, endpoint=False):
        arm = VGroup(Line(ORIGIN, RIGHT * r, color=color, stroke_width=4),
                     Line(RIGHT * r * 0.55, RIGHT * r * 0.55 + np.array([0.18, 0.16, 0]) * r, color=color, stroke_width=3),
                     Line(RIGHT * r * 0.55, RIGHT * r * 0.55 + np.array([0.18, -0.16, 0]) * r, color=color, stroke_width=3))
        g.add(arm.rotate(a, about_point=ORIGIN))
    return g


def flute(L=4.0, color="#C8A165"):
    body = RoundedRectangle(corner_radius=0.09, width=L, height=0.2, stroke_width=0, fill_color=color, fill_opacity=1)
    holes = VGroup(*[Dot([x, 0, 0], radius=0.045, color="#4A3420") for x in np.linspace(-L * 0.05, L * 0.4, 6)])
    mouth = Dot([-L * 0.38, 0, 0], radius=0.05, color="#4A3420")
    bands = VGroup(*[Rectangle(width=0.05, height=0.22, stroke_width=0, fill_color="#8A6A3A", fill_opacity=1).move_to([x, 0, 0])
                     for x in (-L * 0.46, L * 0.47)])
    return VGroup(body, holes, mouth, bands)


def note_glyph(color=th.AMBER, s=0.3):
    head = Ellipse(width=s * 0.8, height=s * 0.55, stroke_width=0, fill_color=color, fill_opacity=1).rotate(0.4)
    stem = Line(head.get_right() + LEFT * 0.03, head.get_right() + LEFT * 0.03 + UP * s * 1.3, color=color, stroke_width=3)
    flag = Line(stem.get_end(), stem.get_end() + RIGHT * s * 0.4 + DOWN * s * 0.35, color=color, stroke_width=3)
    return VGroup(head, stem, flag)


def heart(s=0.5, color=th.CORAL):
    v = VMobject(stroke_width=0, fill_color=color, fill_opacity=1)
    t = np.linspace(0, TAU, 80)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    v.set_points_as_corners([[a * s / 17, b * s / 17, 0] for a, b in zip(x, y)])
    return v


def torch(h=1.2):
    stick = Line(ORIGIN, UP * h, color="#8A6A4A", stroke_width=10)
    fl = flame(h * 0.45).move_to(UP * (h + h * 0.2))
    return VGroup(stick, fl)


def scale_balance(w=5.0):
    post = Line(DOWN * 1.6, UP * 1.0, color=th.MUTED, stroke_width=6)
    beam = Line(LEFT * w / 2, RIGHT * w / 2, color=th.MUTED, stroke_width=6).move_to(UP * 1.0)
    base = Line(LEFT * 0.8, RIGHT * 0.8, color=th.MUTED, stroke_width=8).move_to(DOWN * 1.6)
    return VGroup(post, beam, base)


# ------------------------------------------------------------------ diagrams
def timeline(s, events, y=0.0, x0=-6.0, x1=6.0, color=None, label_w=2.3, size=21):
    """Animated life timeline. events: list of (year_int, label, narration). Labels alternate above/below."""
    color = color or s.color
    n = len(events)
    axis = Line([x0, y, 0], [x1, y, 0], color=th.FAINT, stroke_width=5)
    prog = Line([x0, y, 0], [x0 + 0.001, y, 0], color=color, stroke_width=6)
    s.play(Create(axis), run_time=0.6)
    s.add(prog)
    xs = np.linspace(x0 + 0.6, x1 - 0.6, n)
    made = VGroup(axis, prog)
    for i, ((yr, lab, narr), x) in enumerate(zip(events, xs)):
        up = (i % 2 == 0)
        dot = Dot([x, y, 0], radius=0.12, color=color)
        ring = Circle(radius=0.2, stroke_color=color, stroke_width=3).move_to(dot)
        yt = T(s.num(yr), size=size + 8, color=color, weight="BOLD")
        lt = para(lab, width=label_w, size=size, color=th.INK, align="center")
        stem = Line([x, y + (0.22 if up else -0.22), 0], [x, y + (0.75 if up else -0.75), 0], color=th.FAINT, stroke_width=2)
        grp = VGroup(yt, lt).arrange(DOWN, buff=0.12)
        if up:
            grp.next_to(stem, UP, buff=0.1)
        else:
            grp.next_to(stem, DOWN, buff=0.1)
        with s.say(narr):
            s.play(prog.animate.put_start_and_end_on([x0, y, 0], [x, y, 0]), run_time=0.6)
            s.sfx("pop", gain=-14)
            s.play(GrowFromCenter(dot), Create(ring), Create(stem), run_time=0.4)
            s.play(FadeIn(yt, shift=(DOWN if up else UP) * 0.2), FadeIn(lt, shift=(DOWN if up else UP) * 0.2), run_time=0.5)
        made.add(dot, ring, stem, grp)
    s.play(prog.animate.put_start_and_end_on([x0, y, 0], [x1, y, 0]), run_time=0.5)
    return made


def answer_frame(s, title, steps, color=None, width=11.6, size=24, top=2.45):
    """Answer-writing frame. steps: list of (head, body, narration). Builds a vertical ladder."""
    color = color or s.color
    head = T(title, size=34, color=color, weight="BOLD").move_to([0, top + 0.35, 0])
    s.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.5)
    rows = VGroup()
    built = []
    hw = max(T(h, size=size + 4, weight="BOLD").width for h, _, _ in steps)
    for i, (h, b, _) in enumerate(steps):
        bd = badge(s, i + 1, color, r=0.24)
        ht = T(h, size=size + 4, color=color, weight="BOLD")
        bt = para(b, width=width - hw - 1.2, size=size, color=th.BODY)
        ht.next_to(bd, RIGHT, buff=0.25)
        bt.next_to(bd, RIGHT, buff=0.25 + hw + 0.4).align_to(bd, UP).shift(UP * 0.05)
        row = VGroup(bd, ht, bt)
        built.append(row)
        rows.add(row)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    avail = top - (-3.1)
    if rows.height > avail:
        rows.scale_to_fit_height(avail)
    rows.next_to(head, DOWN, buff=0.35)
    if rows.width > 12.8:
        rows.scale_to_fit_width(12.8)
    rows.set_x(0)
    links = VGroup()
    for i, (row, (_, _, narr)) in enumerate(zip(built, steps)):
        with s.say(narr):
            s.sfx("tick", gain=-12)
            s.play(GrowFromCenter(row[0]), FadeIn(row[1], shift=RIGHT * 0.2), run_time=0.5)
            s.play(FadeIn(row[2], shift=UP * 0.1), run_time=0.6)
            if i > 0:
                ln = Line(built[i - 1][0].get_bottom(), row[0].get_top(), color=color, stroke_width=3)
                links.add(ln)
                s.play(Create(ln), run_time=0.3)
    return VGroup(head, rows, links)


def node(text, color, w=None, size=28, h=0.9, sub=None):
    t = T(text, size=size, color=th.INK, weight="BOLD")
    items = [t]
    if sub:
        items.append(T(sub, size=int(size * 0.7), color=color))
    inner = VGroup(*items).arrange(DOWN, buff=0.08)
    ww = w or inner.width + 0.7
    b = RoundedRectangle(corner_radius=0.25, width=ww, height=max(h, inner.height + 0.35), stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.16)
    inner.move_to(b)
    return VGroup(b, inner)


def link(a, b, color=th.MUTED, label=None, size=20, buff=0.1, curve=0.0, both=False):
    if curve:
        arr = CurvedArrow(a.get_center(), b.get_center(), angle=curve, color=color, stroke_width=3)
    else:
        arr = Arrow(a.get_center(), b.get_center(), buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.12)
    # trim to box edges
    start, end = a.get_center(), b.get_center()
    d = end - start
    nd = d / (np.linalg.norm(d) + 1e-9)

    def exit_point(m, direction):
        w, h = m.width / 2 + buff, m.height / 2 + buff
        tx = w / abs(direction[0]) if abs(direction[0]) > 1e-6 else 1e9
        ty = h / abs(direction[1]) if abs(direction[1]) > 1e-6 else 1e9
        return m.get_center() + direction * min(tx, ty)
    p0, p1 = exit_point(a, nd), exit_point(b, -nd)
    if curve:
        arr = CurvedArrow(p0, p1, angle=curve, color=color, stroke_width=3, tip_length=0.2)
    elif both:
        arr = DoubleArrow(p0, p1, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.1, tip_length=0.2)
    else:
        arr = Arrow(p0, p1, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.1, tip_length=0.22)
    g = VGroup(arr)
    if label:
        lt = T(label, size=size, color=color)
        mid = (p0 + p1) / 2
        perp = np.array([-nd[1], nd[0], 0])
        lt.move_to(mid + perp * 0.32)
        bg = BackgroundRectangle(lt, color=th.BG, fill_opacity=0.85, buff=0.06)
        g.add(bg, lt)
    return g


def two_col_table(s, head_l, head_r, rows, colors=(None, None), x_split=0.0, w=12.0, size=24, top=2.2, row_h=0.72):
    """A table with a header row; returns (header, row groups) unplayed."""
    cl = colors[0] or s.color
    cr = colors[1] or th.SKY
    hl = T(head_l, size=size + 4, color=cl, weight="BOLD")
    hr = T(head_r, size=size + 4, color=cr, weight="BOLD")
    hl.move_to([x_split - w / 4, top, 0])
    hr.move_to([x_split + w / 4, top, 0])
    line = Line([-w / 2, top - 0.38, 0], [w / 2, top - 0.38, 0], color=th.FAINT, stroke_width=2)
    out = []
    for i, (a, b) in enumerate(rows):
        y = top - 0.85 - i * row_h
        ta = para(a, width=w / 2 - 0.5, size=size, color=th.INK, align="center").move_to([x_split - w / 4, y, 0])
        tb = para(b, width=w / 2 - 0.5, size=size, color=th.INK, align="center").move_to([x_split + w / 4, y, 0])
        out.append(VGroup(ta, tb))
    return VGroup(hl, hr, line), out


def leaves_in_wind(n=14, seed=5, region=((-6.5, 6.5), (-2.8, 2.4))):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        c = rng.choice([LEAF, "#8BCB5A", "#D9A441", "#C8763A"])
        l = leaf(rng.uniform(0.15, 0.3), color=c).rotate(rng.uniform(0, TAU))
        l.move_to([rng.uniform(*region[0]), rng.uniform(*region[1]), 0])
        g.add(l)
    return g


def wind_lines(n=7, seed=8, color="#9FB4E8"):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        y = rng.uniform(-2.5, 2.5)
        x = rng.uniform(-6.5, 2.0)
        L = rng.uniform(2.0, 4.0)
        a = ArcBetweenPoints([x, y, 0], [x + L, y + rng.uniform(-0.3, 0.3), 0], angle=rng.uniform(-0.4, 0.4))
        a.set_stroke(color, width=rng.uniform(2, 4), opacity=0.7)
        g.add(a)
    return g


# ------------------------------------------------------------------ more figures (unit 2 onwards)
def woman(h=2.5, sari="#1F8A8A", border=SARI2):
    return mother(h, sari=sari, border=border)


def man(h=2.5, shirt="#E8E0C8", coat="#5B4A8A", crown=False, topi=False, skin=SKIN):
    u = h / 2.5
    head = Circle(radius=0.26 * u, stroke_width=0, fill_color=skin, fill_opacity=1).move_to(UP * 2.18 * u)
    hair = Circle(radius=0.27 * u, stroke_width=0, fill_color=HAIR, fill_opacity=1).move_to(UP * 2.25 * u)
    neck = Rectangle(width=0.14 * u, height=0.15 * u, stroke_width=0, fill_color=SKIN2, fill_opacity=1).move_to(UP * 1.9 * u)
    body = Polygon([-0.42 * u, 1.85 * u, 0], [0.42 * u, 1.85 * u, 0], [0.36 * u, 0.85 * u, 0], [-0.36 * u, 0.85 * u, 0],
                   stroke_width=0, fill_color=coat, fill_opacity=1)
    sash = Polygon([-0.1 * u, 1.85 * u, 0], [0.1 * u, 1.85 * u, 0], [0.06 * u, 0.85 * u, 0], [-0.06 * u, 0.85 * u, 0],
                   stroke_width=0, fill_color=shirt, fill_opacity=1)
    legs = VGroup(Polygon([-0.34 * u, 0.88 * u, 0], [0.0, 0.88 * u, 0], [-0.06 * u, 0, 0], [-0.3 * u, 0, 0], stroke_width=0, fill_color=shirt, fill_opacity=1),
                  Polygon([0.0, 0.88 * u, 0], [0.34 * u, 0.88 * u, 0], [0.3 * u, 0, 0], [0.06 * u, 0, 0], stroke_width=0, fill_color=shirt, fill_opacity=1))
    arms = VGroup(Line([-0.4 * u, 1.75 * u, 0], [-0.55 * u, 1.0 * u, 0], color=coat, stroke_width=10 * u),
                  Line([0.4 * u, 1.75 * u, 0], [0.55 * u, 1.0 * u, 0], color=coat, stroke_width=10 * u))
    parts = [legs, arms, body, sash, neck, hair, head]
    if crown:
        cr = Polygon([-0.24 * u, 2.4 * u, 0], [0.24 * u, 2.4 * u, 0], [0.26 * u, 2.68 * u, 0], [0.12 * u, 2.52 * u, 0], [0, 2.72 * u, 0],
                     [-0.12 * u, 2.52 * u, 0], [-0.26 * u, 2.68 * u, 0], stroke_width=0, fill_color=th.AMBER, fill_opacity=1)
        parts.append(cr)
    if topi:
        cap = Polygon([-0.25 * u, 2.36 * u, 0], [0.25 * u, 2.36 * u, 0], [0.2 * u, 2.6 * u, 0], [-0.16 * u, 2.58 * u, 0],
                      stroke_width=0, fill_color="#B23A48", fill_opacity=1)
        parts.append(cap)
    g = VGroup(*parts)
    g.head = head
    return g


def elephant(h=1.6, color="#6E7391"):
    u = h / 1.6
    dark = interpolate_color(ManimColor(color), ManimColor(BLACK), 0.25)
    legs = VGroup(*[Rectangle(width=0.28 * u, height=0.7 * u, stroke_width=0, fill_color=dark if k % 2 else color, fill_opacity=1)
                    .move_to([x * u, 0.35 * u, 0]) for k, x in enumerate((-0.7, -0.38, 0.35, 0.65))])
    body = Ellipse(width=2.1 * u, height=1.25 * u, stroke_width=0, fill_color=color, fill_opacity=1).move_to(UP * 1.05 * u)
    head = Circle(radius=0.5 * u, stroke_width=0, fill_color=color, fill_opacity=1).move_to([1.05 * u, 1.3 * u, 0])
    ear = Ellipse(width=0.5 * u, height=0.75 * u, stroke_width=0, fill_color=dark, fill_opacity=1).move_to([0.85 * u, 1.3 * u, 0])
    trunk = VMobject(stroke_color=color, stroke_width=16 * u)
    trunk.set_points_smoothly([np.array(p) * u for p in ([1.4, 1.15, 0], [1.6, 0.75, 0], [1.55, 0.35, 0], [1.72, 0.2, 0])])
    tusk = ArcBetweenPoints([1.3 * u, 1.0 * u, 0], [1.55 * u, 0.8 * u, 0], angle=0.8).set_stroke("#F2EAD8", 5 * u)
    eye = Dot([1.2 * u, 1.45 * u, 0], radius=0.04 * u, color=BLACK)
    tail = Line([-1.05 * u, 1.1 * u, 0], [-1.25 * u, 0.6 * u, 0], color=dark, stroke_width=4 * u)
    return VGroup(tail, legs, body, ear, head, trunk, tusk, eye)


def palace(w=4.0, color="#C9A46A", dark="#8A6A3A"):
    base = Rectangle(width=w, height=w * 0.42, stroke_width=0, fill_color=color, fill_opacity=1)
    base.move_to(UP * w * 0.21)
    dome = Sector(radius=w * 0.17, start_angle=0, angle=PI, stroke_width=0, fill_color=dark, fill_opacity=1)
    dome.move_to(base.get_top() + UP * w * 0.085)
    spire = Line(dome.get_top(), dome.get_top() + UP * w * 0.08, color=th.AMBER, stroke_width=4)
    towers = VGroup()
    for x in (-w * 0.45, w * 0.45):
        t = Rectangle(width=w * 0.12, height=w * 0.6, stroke_width=0, fill_color=dark, fill_opacity=1).move_to([x, w * 0.3, 0])
        cap = Triangle(stroke_width=0, fill_color=th.CORAL, fill_opacity=1).stretch_to_fit_width(w * 0.16).stretch_to_fit_height(w * 0.12)
        cap.next_to(t, UP, buff=0)
        towers.add(t, cap)
    wins = VGroup(*[Rectangle(width=w * 0.07, height=w * 0.1, stroke_width=0, fill_color="#FFD27A", fill_opacity=0.9).move_to([x, w * 0.3, 0])
                    for x in np.linspace(-w * 0.28, w * 0.28, 5)])
    door = Rectangle(width=w * 0.12, height=w * 0.18, stroke_width=0, fill_color="#3A271B", fill_opacity=1).move_to([0, w * 0.09, 0])
    balcony = VGroup(Rectangle(width=w * 0.36, height=w * 0.04, stroke_width=0, fill_color=dark, fill_opacity=1).move_to([0, w * 0.44, 0]),
                     *[Line([x, w * 0.44, 0], [x, w * 0.5, 0], color=dark, stroke_width=2) for x in np.linspace(-w * 0.17, w * 0.17, 7)])
    g = VGroup(base, towers, dome, spire, wins, door, balcony)
    g.balcony = balcony
    return g


def bell(s=0.5, color=th.AMBER):
    pts = [[-0.15, 0.45, 0], [0.15, 0.45, 0], [0.3, 0.0, 0], [0.45, -0.3, 0], [-0.45, -0.3, 0], [-0.3, 0.0, 0]]
    b = Polygon(*[np.array(p) * s * 2 for p in pts], stroke_width=0, fill_color=color, fill_opacity=1)
    clap = Dot(np.array([0, -0.4, 0]) * s * 2, radius=0.08 * s * 2, color=color)
    loop = Circle(radius=0.08 * s * 2, stroke_color=color, stroke_width=3).move_to(np.array([0, 0.55, 0]) * s * 2)
    return VGroup(loop, b, clap)


def dice(s=0.6, n=5, color="#F2EAD8"):
    sq = RoundedRectangle(corner_radius=s * 0.15, width=s, height=s, stroke_width=0, fill_color=color, fill_opacity=1)
    spots = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)], 4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
             5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)], 6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}[n]
    d = VGroup(*[Dot([x * s * 0.27, y * s * 0.27, 0], radius=s * 0.07, color="#3A2A2A") for x, y in spots])
    return VGroup(sq, d)


def lotus(s=0.5, color="#F48FB1"):
    petals = VGroup()
    for a in np.linspace(-1.0, 1.0, 5):
        p = Ellipse(width=s * 0.4, height=s, stroke_width=0, fill_color=color, fill_opacity=0.95)
        p.shift(UP * s * 0.45).rotate(a * 0.9, about_point=ORIGIN)
        petals.add(p)
    pad = Ellipse(width=s * 1.8, height=s * 0.35, stroke_width=0, fill_color=LEAF, fill_opacity=0.9).shift(DOWN * s * 0.05)
    return VGroup(pad, petals)


def saptarishi(s=1.0, color=WHITE):
    pts = [(-1.6, 0.3), (-1.0, 0.4), (-0.5, 0.25), (0.0, 0.0), (0.2, -0.6), (1.0, -0.65), (1.1, 0.0)]
    dots = VGroup(*[Dot([x * s, y * s, 0], radius=0.06 * s + 0.01, color=color) for x, y in pts])
    lines = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center(), color=color, stroke_width=1.5, stroke_opacity=0.5) for i in range(6)],
                   Line(dots[6].get_center(), dots[3].get_center(), color=color, stroke_width=1.5, stroke_opacity=0.5))
    return VGroup(lines, dots)


def milky_way(n=160, seed=6, a=(-6.5, -1.5), b=(6.5, 3.0), width=0.9):
    rng = np.random.default_rng(seed)
    A, B = np.array([*a, 0.0]), np.array([*b, 0.0])
    d = B - A
    nd = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
    g = VGroup()
    for _ in range(n):
        t = rng.uniform(0, 1)
        off = rng.normal(0, width * 0.35)
        g.add(Dot(A + d * t + nd * off, radius=rng.uniform(0.008, 0.03), color=rng.choice(["#FFFFFF", "#CFE3FF", "#F7E3FF"]),
                  fill_opacity=rng.uniform(0.3, 0.9)))
    return g


def cloud(w=2.0, color="#3A3F5E", opacity=0.85):
    return VGroup(*[Ellipse(width=w * (0.55 + 0.12 * k), height=w * 0.32, stroke_width=0, fill_color=color, fill_opacity=opacity)
                    .shift(RIGHT * (k - 1) * w * 0.28 + UP * (w * 0.06 if k == 1 else 0)) for k in range(3)])


def stick_path(points, color="#6B5A4A", width=18):
    p = VMobject(stroke_color=color, stroke_width=width)
    p.set_points_smoothly([np.array(q) for q in points])
    return p
