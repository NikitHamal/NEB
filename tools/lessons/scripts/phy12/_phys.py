"""Shared drawing helpers for the Physics 12 lessons."""
from manim import *
import numpy as np

from kit import M, T, para, th


def spring(a, b, coils=9, width=0.22, color=th.BODY, stroke=3):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = b - a
    L = np.linalg.norm(d) + 1e-9
    u = d / L
    p = np.array([-u[1], u[0], 0])
    lead = min(0.18, L * 0.12)
    pts = [a, a + u * lead]
    n = coils * 2
    for i in range(n):
        s = lead + (L - 2 * lead) * (i + 0.5) / n
        pts.append(a + u * s + p * width * (1 if i % 2 == 0 else -1))
    pts += [b - u * lead, b]
    return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)


def hatch(center, width=1.6, vertical=False, color=th.MUTED):
    c = np.array(center, dtype=float)
    g = VGroup()
    if vertical:
        g.add(Line(c + UP * width / 2, c + DOWN * width / 2, color=th.BODY, stroke_width=4))
        for y in np.linspace(-width / 2 + 0.1, width / 2 - 0.1, 7):
            g.add(Line(c + UP * y, c + UP * y + LEFT * 0.18 + UP * 0.14, color=color, stroke_width=2))
    else:
        g.add(Line(c + LEFT * width / 2, c + RIGHT * width / 2, color=th.BODY, stroke_width=4))
        for x in np.linspace(-width / 2 + 0.1, width / 2 - 0.1, 8):
            g.add(Line(c + RIGHT * x, c + RIGHT * x + UP * 0.18 + RIGHT * 0.14, color=color, stroke_width=2))
    return g


def block(center, w=0.9, h=0.7, color=th.SKY, label="m"):
    b = RoundedRectangle(corner_radius=0.08, width=w, height=h, fill_color=color, fill_opacity=0.85,
                         stroke_color=WHITE, stroke_width=2).move_to(center)
    if not label:
        return VGroup(b)
    return VGroup(b, M(label, size=34, color=th.BG).move_to(center))


def nothing(a):
    return Line(a, np.array(a, dtype=float) + RIGHT * 0.001, stroke_width=0, stroke_opacity=0)


def arrow(a, b, color, width=5):
    """An arrow that never breaks when it shrinks to nothing inside an always_redraw."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if np.linalg.norm(b - a) < 0.2:
        return nothing(a)
    return Arrow(a, b, buff=0, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.3,
                 max_stroke_width_to_length_ratio=12)


def sdash(a, b, **kw):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if np.linalg.norm(b - a) < 0.08:
        return nothing(a)
    return DashedLine(a, b, **kw)


def example(scene, problem, lines, says, size=38, buff=0.4, width=12.2, colors=None, top=None):
    """Worked example: problem statement, then each line written while its sentence is spoken."""
    head = T(scene.S["example"], size=26, color=scene.color, weight="BOLD").to_corner(UL, buff=0.75)
    prob = para(problem, width=width, size=27, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
    steps = VGroup(*[M(l, size=size) if isinstance(l, str) else l for l in lines])
    for i, c in enumerate(colors or []):
        if c:
            steps[i].set_color(c)
    steps.arrange(DOWN, aligned_edge=LEFT, buff=buff).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
    if steps.width > 12.6:
        steps.scale_to_fit_width(12.6).align_to(prob, LEFT)
    if steps.get_bottom()[1] < -3.3:
        steps.scale_to_fit_height(max(0.5, steps.get_top()[1] + 3.3)).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
    with scene.say(says[0]):
        scene.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
    k = 0
    for say in says[1:]:
        n = 1
        if isinstance(say, tuple):
            say, n = say
        with scene.say(say):
            for _ in range(n):
                if k < len(steps):
                    scene.play(Write(steps[k]), run_time=1.3)
                    k += 1
    while k < len(steps):
        scene.play(Write(steps[k]))
        k += 1
    scene.play(Circumscribe(steps[-1], color=th.AMBER), run_time=1.0)
    scene.wait(0.4)
    scene.play(FadeOut(VGroup(head, prob, steps)))


class Flow(VGroup):
    """Tracer particles carried along a 2D pipe. `half(x)` is the half-width, `mid(x)` the centre line,
    and the speed at x follows continuity: v = q / half(x)."""

    def __init__(self, x0, x1, half, mid, q=0.5, lanes=7, per_lane=9, color=th.SKY, radius=0.05, profile=None):
        super().__init__()
        self.x0, self.x1, self.half, self.mid, self.q = x0, x1, half, mid, q
        self.profile = profile
        self.speed = 1.0
        self.items = []
        fr = np.linspace(-0.8, 0.8, lanes)
        for i, f in enumerate(fr):
            for k in range(per_lane):
                x = x0 + (x1 - x0) * ((k + (i % 2) * 0.5) / per_lane)
                d = Dot(radius=radius, color=color)
                self.items.append([x, f])
                self.add(d)
        self._place()
        self.add_updater(Flow._step)

    def _place(self):
        for d, (x, f) in zip(self.submobjects, self.items):
            d.move_to([x, self.mid(x) + f * self.half(x), 0])

    def _step(self, dt):
        L = self.x1 - self.x0
        for it in self.items:
            x, f = it
            v = self.q / self.half(x)
            if self.profile is not None:
                v *= self.profile(f)
            x += v * dt * self.speed
            if x > self.x1:
                x -= L
            it[0] = x
        self._place()


def pipe_walls(x0, x1, half, mid, color=th.BODY, n=120, stroke=4):
    xs = np.linspace(x0, x1, n)
    top = VMobject(stroke_color=color, stroke_width=stroke).set_points_smoothly([[x, mid(x) + half(x), 0] for x in xs])
    bot = VMobject(stroke_color=color, stroke_width=stroke).set_points_smoothly([[x, mid(x) - half(x), 0] for x in xs])
    fill = Polygon(*[[x, mid(x) + half(x), 0] for x in xs], *[[x, mid(x) - half(x), 0] for x in xs[::-1]],
                   stroke_width=0, fill_color=th.SKY, fill_opacity=0.12)
    return VGroup(fill, top, bot)


# ---------------------------------------------------------------- shared by units 4+
def neby_in(scene, state="idle", corner=DR, height=1.4, buff=0.45, at=None):
    """Pop the pixel Neby in for a reaction; pair with neby_out."""
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


class Gas(VGroup):
    """Molecules bouncing inside a box. `box()` returns (x0, x1, y0, y1) every frame (absolute coordinates,
    so a piston that moves squeezes the gas and a removed partition lets it stream out). `speed()` scales the
    molecular speed (use sqrt(T/T0)); `color()` optionally recolours the molecules (hot/cold)."""

    def __init__(self, box, n=36, speed=None, color=None, radius=0.055, base=1.6, seed=3, fill=th.SKY, region=None):
        super().__init__()
        rng = np.random.default_rng(seed)
        self.box, self.speed_fn, self.color_fn, self.r = box, speed, color, radius
        x0, x1, y0, y1 = region or box()
        self.pos = np.column_stack([rng.uniform(x0 + radius, x1 - radius, n), rng.uniform(y0 + radius, y1 - radius, n)])
        ang = rng.uniform(0, TAU, n)
        sp = base * rng.uniform(0.6, 1.4, n)
        self.vel = np.column_stack([np.cos(ang) * sp, np.sin(ang) * sp])
        self.paused = False
        for i in range(n):
            self.add(Dot(radius=radius, color=fill))
        self._place()
        self.add_updater(Gas._step)

    def _place(self):
        col = self.color_fn() if self.color_fn else None
        for d, p in zip(self.submobjects, self.pos):
            d.move_to([p[0], p[1], 0])
            if col is not None:
                d.set_color(col)

    def _step(self, dt):
        if self.paused:
            return
        s = self.speed_fn() if self.speed_fn else 1.0
        x0, x1, y0, y1 = self.box()
        r = self.r
        self.pos += self.vel * s * min(dt, 0.1)
        for k, (lo, hi) in enumerate(((x0 + r, x1 - r), (y0 + r, y1 - r))):
            p, v = self.pos[:, k], self.vel[:, k]
            m = p < lo
            p[m] = lo
            v[m] = np.abs(v[m])
            m = p > hi
            p[m] = hi
            v[m] = -np.abs(v[m])
        self._place()


def heat_color(t):
    """0 -> cold blue, 1 -> hot red."""
    t = float(np.clip(t, 0, 1))
    return interpolate_color(ManimColor(th.SKY), ManimColor(th.CORAL), t)


def pv_axes(xr=(0, 6, 1), yr=(0, 6, 1), x_len=5.0, y_len=3.6, xl="V", yl="P", size=34):
    """Axes for an indicator diagram: returns VGroup(axes, x_label, y_label); use g[0].c2p."""
    ax = Axes(x_range=list(xr), y_range=list(yr), x_length=x_len, y_length=y_len, tips=True,
              axis_config={"color": th.MUTED, "include_ticks": False, "tip_width": 0.16, "tip_height": 0.16, "stroke_width": 3})
    lx = M(xl, size=size, color=th.BODY).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
    ly = M(yl, size=size, color=th.BODY).next_to(ax.y_axis.get_end(), LEFT, buff=0.15)
    return VGroup(ax, lx, ly)


def flame(center, scale=1.0):
    c = np.array(center, dtype=float)
    outer = VMobject(fill_color=th.AMBER, fill_opacity=0.95, stroke_width=0).set_points_smoothly(
        [c + scale * np.array(p) for p in [(0, 0.55, 0), (0.22, 0.12, 0), (0.18, -0.12, 0), (0, -0.2, 0), (-0.18, -0.12, 0), (-0.22, 0.12, 0), (0, 0.55, 0)]])
    inner = VMobject(fill_color=th.CORAL, fill_opacity=0.95, stroke_width=0).set_points_smoothly(
        [c + scale * np.array(p) for p in [(0, 0.28, 0), (0.1, 0.02, 0), (0, -0.14, 0), (-0.1, 0.02, 0), (0, 0.28, 0)]])
    return VGroup(outer, inner)


class Cylinder:
    """A gas cylinder with a piston. `h()` is the gas height above the base yb, `T()` the gas temperature in K.
    Molecules speed up as sqrt(T/T0) and redden between Tlo and Thi. Use .all() to add / fade, .drop(scene) to clean."""

    def __init__(self, cx, yb, w, H, h, T, T0=300.0, Tlo=250.0, Thi=700.0, n=34, rod=0.8, seed=3, piston_color="#9AA3C7"):
        self.cx, self.yb, self.w, self.H, self.h, self.T = cx, yb, w, H, h, T
        L, R = cx - w / 2, cx + w / 2
        self.walls = VGroup(Line([L, yb + H, 0], [L, yb, 0]), Line([L, yb, 0], [R, yb, 0]), Line([R, yb, 0], [R, yb + H, 0])).set_stroke(th.BODY, 5)
        col = lambda: heat_color((T() - Tlo) / (Thi - Tlo))
        self.fill = always_redraw(lambda: Rectangle(width=w - 0.06, height=max(0.02, h()), stroke_width=0, fill_color=col(), fill_opacity=0.16)
                                  .move_to([cx, yb + h() / 2, 0]))
        self.piston = always_redraw(lambda: VGroup(
            Rectangle(width=w - 0.06, height=0.24, stroke_color=WHITE, stroke_width=1.5, fill_color=piston_color, fill_opacity=1).move_to([cx, yb + h() + 0.12, 0]),
            Line([cx, yb + h() + 0.24, 0], [cx, yb + h() + 0.24 + rod, 0], color=piston_color, stroke_width=7)))
        self.gas = Gas(lambda: (L + 0.03, R - 0.03, yb + 0.03, yb + h()), n=n, seed=seed,
                       speed=lambda: np.sqrt(max(T(), 1) / T0), color=col)

    def all(self):
        return VGroup(self.fill, self.walls, self.gas, self.piston)

    def piston_y(self):
        return self.yb + self.h() + 0.24

    def drop(self, scene, extra=()):
        scene.play(FadeOut(self.all()), *[FadeOut(e) for e in extra], run_time=0.5)
        scene.remove(self.fill, self.piston, self.gas)


def readout(label, fn, unit="", decimals=0, size=30, color=th.INK):
    """Live label = number unit, driven by fn() through an updater (cheap: no Text rebuilt per frame)."""
    lab = T(label, size=size, color=color)
    num = DecimalNumber(fn(), num_decimal_places=decimals, font_size=size * 1.3, color=color, group_with_commas=False)
    un = T(unit, size=size, color=color) if unit else VGroup()
    g = VGroup(lab, num, un).arrange(RIGHT, buff=0.12)
    num.add_updater(lambda m: m.set_value(fn()))
    if unit:
        un.add_updater(lambda m: m.next_to(num, RIGHT, buff=0.12))
    return g


class Stream(VGroup):
    """Dots flowing for ever along a polyline (energy flow, current, refrigerant). `color(t)` may tint by
    position t in [0, 1); `speed` is in scene units per second and may be changed live."""

    def __init__(self, points, n=8, speed=1.2, color=th.AMBER, radius=0.06, smooth=False):
        super().__init__()
        self.path = VMobject()
        if smooth:
            self.path.set_points_smoothly([np.array(p, dtype=float) for p in points])
        else:
            self.path.set_points_as_corners([np.array(p, dtype=float) for p in points])
        self.length = max(1e-3, sum(np.linalg.norm(np.array(points[i + 1], dtype=float) - np.array(points[i], dtype=float)) for i in range(len(points) - 1)))
        self.speed = speed
        self.color_fn = color if callable(color) else None
        self.ts = [i / n for i in range(n)]
        for i in range(n):
            self.add(Dot(radius=radius, color=color if not callable(color) else WHITE))
        self._place()
        self.add_updater(Stream._step)

    def _place(self):
        for d, t in zip(self.submobjects, self.ts):
            d.move_to(self.path.point_from_proportion(t % 1.0))
            if self.color_fn is not None:
                d.set_color(self.color_fn(t % 1.0))

    def _step(self, dt):
        dt = min(dt, 0.1)
        self.ts = [(t + self.speed * dt / self.length) % 1.0 for t in self.ts]
        self._place()


def clock(scene, rate=1.0):
    """A ValueTracker that ticks by itself (t += rate * dt) while it is in the scene; set .rate to slow, freeze or reverse."""
    t = ValueTracker(0)
    t.rate = rate
    t.add_updater(lambda m, dt: m.increment_value(dt * m.rate))
    scene.add(t)
    return t


def curve(fn, x0, x1, n=160, color=th.SKY, width=4, smooth=False):
    """A plain VMobject through (x, fn(x)) in scene coordinates; cheap enough to rebuild every frame."""
    xs = np.linspace(x0, x1, n)
    pts = [np.array([x, fn(x), 0]) for x in xs]
    m = VMobject(stroke_color=color, stroke_width=width)
    if smooth:
        m.set_points_smoothly(pts)
    else:
        m.set_points_as_corners(pts)
    return m


def wl_rgb(nm):
    """Rough visible colour for a wavelength in nm, as an (r, g, b) tuple in 0..1."""
    if nm < 440:
        r, g, b = -(nm - 440) / 60, 0.0, 1.0
    elif nm < 490:
        r, g, b = 0.0, (nm - 440) / 50, 1.0
    elif nm < 510:
        r, g, b = 0.0, 1.0, -(nm - 510) / 20
    elif nm < 580:
        r, g, b = (nm - 510) / 70, 1.0, 0.0
    elif nm < 645:
        r, g, b = 1.0, -(nm - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    return np.clip(np.array([r, g, b]), 0, 1)


def strip(x, y0, y1, width, rgb_fn, n=110):
    """A vertical screen made of n thin bands; rgb_fn(y) gives the colour (r, g, b) in 0..1 at height y."""
    g = VGroup()
    h = (y1 - y0) / n
    for k in range(n):
        y = y0 + (k + 0.5) * h
        c = np.clip(rgb_fn(y), 0, 1)
        g.add(Rectangle(width=width, height=h * 1.02, stroke_width=0, fill_color=ManimColor.from_rgb(np.array(c, dtype=float)), fill_opacity=1).move_to([x, y, 0]))
    return g


# ---------------------------------------------------------------- circuit symbols (units 14+)
def resistor(a, b, color=th.BODY, zig=6, w=0.16, frac=0.5, stroke=4):
    """Zigzag resistor between points a and b (the zigzag fills `frac` of the length, centred)."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = b - a
    L = np.linalg.norm(d)
    u = d / L
    p = np.array([-u[1], u[0], 0])
    s0, s1 = (1 - frac) / 2 * L, (1 + frac) / 2 * L
    pts = [a, a + u * s0]
    for i in range(zig):
        s = s0 + (s1 - s0) * (i + 0.5) / zig
        pts.append(a + u * s + p * w * (1 if i % 2 == 0 else -1))
    pts += [a + u * s1, b]
    return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)


def cell(a, b, color=th.BODY, stroke=4, plus_at_b=True, gap=0.16):
    """Cell symbol on the wire from a to b: long plate (+) and short plate (-), leads to both ends."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = b - a
    L = np.linalg.norm(d)
    u = d / L
    p = np.array([-u[1], u[0], 0])
    m = (a + b) / 2
    pa, pb = m - u * gap / 2, m + u * gap / 2
    long_at = pb if plus_at_b else pa
    short_at = pa if plus_at_b else pb
    g = VGroup(Line(a, pa, color=color, stroke_width=stroke), Line(pb, b, color=color, stroke_width=stroke),
               Line(long_at - p * 0.32, long_at + p * 0.32, color=color, stroke_width=stroke),
               Line(short_at - p * 0.17, short_at + p * 0.17, color=color, stroke_width=stroke + 3))
    return g


def galvo(center, r=0.32, color=th.BODY, label="G"):
    c = np.array(center, dtype=float)
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=th.BG, fill_opacity=1).move_to(c),
                  T(label, size=24, color=color, weight="BOLD").move_to(c))


def wire(*pts, color=th.BODY, stroke=4):
    return VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners([np.array(p, dtype=float) for p in pts])


def needle_meter(center, frac_fn, r=1.0, color=th.AMBER, label="G"):
    """Analogue meter dial; frac_fn() in [-1, 1] sets the needle (0 = centre zero)."""
    c = np.array(center, dtype=float)
    dial = VGroup(Arc(radius=r, start_angle=PI / 2 - 1.0, angle=2.0, arc_center=c, color=th.BODY, stroke_width=3),
                  *[Line(c + (r - 0.12) * np.array([np.cos(PI / 2 - k), np.sin(PI / 2 - k), 0]), c + r * np.array([np.cos(PI / 2 - k), np.sin(PI / 2 - k), 0]), color=th.BODY, stroke_width=2)
                    for k in np.linspace(-1.0, 1.0, 9)],
                  T(label, size=22, color=th.MUTED).move_to(c + DOWN * 0.25))
    needle = always_redraw(lambda: Line(c, c + (r - 0.05) * np.array([np.cos(PI / 2 - float(np.clip(frac_fn(), -1, 1))), np.sin(PI / 2 - float(np.clip(frac_fn(), -1, 1))), 0]),
                                        color=color, stroke_width=4))
    return dial, needle
