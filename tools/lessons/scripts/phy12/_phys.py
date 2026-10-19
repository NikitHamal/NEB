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
