from manim import *
import numpy as np

from kit import Lesson, M, T, para, th

C_X, C_V, C_A, C_K, C_U, C_E, C_F = th.SKY, th.MINT, th.CORAL, th.MINT, th.AMBER, th.ACCENT, th.PINK


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
    return VGroup(b, M(label, size=34, color=th.BG).move_to(center))


def arrow(a, b, color, width=5):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if np.linalg.norm(b - a) < 0.2:
        return Line(a, a + RIGHT * 0.001, stroke_width=0, stroke_opacity=0)
    return Arrow(a, b, buff=0, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12)


def sdash(a, b, **kw):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if np.linalg.norm(b - a) < 0.08:
        return Line(a, a + RIGHT * 0.001, stroke_width=0, stroke_opacity=0)
    return DashedLine(a, b, **kw)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 2
    TITLE = "Periodic Motion"
    SUBTITLE = "Springs, pendulums and resonance"
    SECTIONS = ["Equation of SHM", "Energy in SHM", "Mass on a vertical spring",
                "Angular SHM and the pendulum", "Damping, forcing, resonance"]
    NEXT = "Unit 3 · Fluid Statics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ helpers
    def buildings(self, t, drive, amp_scale=1.0, ramp=6.0):
        xs = [-4.8, -2.4, 0.0, 2.4, 4.8]
        hs = [1.3, 2.0, 2.9, 3.7, 4.4]
        ws = [3.3 / h for h in hs]
        ground_y = -2.55
        G = 0.08
        b = 0.18

        def amp(i):
            w0 = ws[i]
            A = drive ** 2 / np.sqrt((w0 ** 2 - drive ** 2) ** 2 + (b * drive) ** 2)
            ph = np.arctan2(b * drive, w0 ** 2 - drive ** 2)
            return A, ph

        def draw():
            tt = t.get_value()
            r = min(1.0, tt / ramp) if ramp > 0 else 1.0
            g0 = G * np.sin(drive * tt)
            grp = VGroup()
            grp.add(Rectangle(width=13.4, height=0.5, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0)
                    .move_to([g0, ground_y - 0.25, 0]))
            for i, (x, h) in enumerate(zip(xs, hs)):
                A, ph = amp(i)
                top = g0 + amp_scale * G * A * r * np.sin(drive * tt - ph)
                col = interpolate_color(ManimColor(th.SKY), ManimColor(th.CORAL), float(np.clip((A * r - 1.5) / 3.0, 0, 1)))
                w = 1.1
                bl = np.array([x - w / 2 + g0, ground_y, 0])
                br = np.array([x + w / 2 + g0, ground_y, 0])
                tl = np.array([x - w / 2 + top, ground_y + h, 0])
                tr = np.array([x + w / 2 + top, ground_y + h, 0])
                grp.add(Polygon(bl, br, tr, tl, fill_color=th.PANEL, fill_opacity=1, stroke_color=col, stroke_width=3))
                floors = int(h / 0.45)
                for k in range(1, floors):
                    y = k / floors
                    off = g0 + (top - g0) * y
                    grp.add(Line([x - w / 2 + off + 0.08, ground_y + h * y, 0], [x + w / 2 + off - 0.08, ground_y + h * y, 0],
                                 color=col, stroke_width=1.5, stroke_opacity=0.5))
            return grp
        return always_redraw(draw), xs, hs, ws

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        t = ValueTracker(0)
        drive = 3.3 / 2.9
        city, xs, hs, ws = self.buildings(t, drive, amp_scale=1.6, ramp=7.0)
        date = T("25 April 2015  ·  11:56 am  ·  Gorkha", size=28, color=th.MUTED).to_edge(UP, buff=0.7)
        with self.say("Twenty fifth of April, twenty fifteen. Eleven fifty six in the morning. The ground under Nepal begins to shake."):
            self.play(FadeIn(date, shift=DOWN * 0.2))
            self.add(city)
            self.play(FadeIn(city), run_time=0.8)
        self.sfx("thud", gain=-6)
        with self.say("Here is a strange fact from that day. In the same street, shaken by the same ground, one building can sway wildly while its neighbours, shorter and taller, barely move.") as v:
            self.play(t.animate.set_value(v.dur), run_time=v.dur, rate_func=linear)
        hot = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.6, height=hs[2] + 0.6, color=th.CORAL, stroke_width=3).move_to([xs[2], -2.55 + hs[2] / 2 + 0.15, 0]), num_dashes=40)
        q = T("Why this one?", size=40, color=th.CORAL, weight="BOLD", display=True).next_to(date, DOWN, buff=0.35)
        nb = self.neby("surprised", height=1.4).to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        with self.say("It is not the weakest building. It is not the tallest either. So why this one? Keep the question in mind. By the end of this lesson, one word will answer it.") as v:
            self.add(nb)
            self.play(FadeIn(q, scale=0.8), FadeIn(nb, scale=0.5), Create(hot), t.animate.set_value(t.get_value() + 2.0), run_time=2.0, rate_func=linear)
            self.play(t.animate.set_value(t.get_value() + v.dur - 2.0), run_time=max(0.5, v.dur - 2.0), rate_func=linear)
        self.play(FadeOut(VGroup(date, q, hot)), FadeOut(city), FadeOut(nb), run_time=0.7)
        self.remove(city, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 2: Periodic Motion. Swings, springs, sitar strings, clocks and earthquakes. They all dance to one simple rule, and today we learn it."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path: the equation of simple harmonic motion, the energy it carries, a mass bouncing on a spring, the simple pendulum, and finally damping, forced oscillation and resonance.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        y0 = 1.2
        wall_x = -6.0
        mean_x = -1.6
        A = 1.7
        s = ValueTracker(0)
        wall = hatch([wall_x, y0, 0], width=1.6, vertical=True)
        floor = Line([wall_x, y0 - 0.4, 0], [3.4, y0 - 0.4, 0], color=th.FAINT, stroke_width=3)
        mean = DashedLine([mean_x, y0 - 0.9, 0], [mean_x, y0 + 0.9, 0], color=th.MUTED, stroke_width=2)

        def X():
            return A * np.cos(s.get_value())

        def rig():
            x = X()
            c = np.array([mean_x + x, y0, 0])
            g = VGroup(spring([wall_x, y0, 0], c + LEFT * 0.45, coils=10), block(c))
            return g
        sys = always_redraw(rig)
        ticks = VGroup()
        for k, lab in [(-A, "-A"), (0, "0"), (A, "+A")]:
            ticks.add(Line([mean_x + k, y0 - 0.55, 0], [mean_x + k, y0 - 0.75, 0], color=th.MUTED, stroke_width=2),
                      M(lab, size=26, color=th.MUTED).move_to([mean_x + k, y0 - 1.0, 0]))
        with self.say("Start with the simplest oscillator of all: a block on a smooth table, tied to a spring. Pull it to one side and let go."):
            self.play(FadeIn(wall), Create(floor), FadeIn(mean))
            self.add(sys)
            self.play(FadeIn(sys))
            self.play(s.animate.set_value(TAU * 2), run_time=5, rate_func=linear)
        fx = always_redraw(lambda: arrow([mean_x + X(), y0 + 0.6, 0], [mean_x + X() - 0.75 * X(), y0 + 0.6, 0], C_F))
        flab = M(r"F = -kx", size=48).move_to([3.6, 2.5, 0])
        flab[0][0].set_color(C_F)
        with self.say("Watch the force from the spring, the pink arrow. Stretch the spring and it pulls back. Squash it and it pushes back. The further you go, the harder it pushes, and it always points towards the middle."):
            self.play(FadeIn(ticks))
            self.add(fx)
            self.play(s.animate.set_value(TAU * 4), run_time=7, rate_func=linear)
        with self.say("That is Hooke's law: F equals minus k x. The minus sign is the whole story. It says the force always points back towards the mean position."):
            self.play(Write(flab))
            self.play(s.animate.set_value(TAU * 5), run_time=3, rate_func=linear)
        defn = self.callout("key", "Simple harmonic motion: acceleration is proportional to the displacement from the mean position, and always directed towards it.", width=7.2, size=26)
        defn.move_to([2.6, -1.9, 0])
        law = M(r"a = -\omega^{2} x", r",\quad \omega^{2} = \frac{k}{m}", size=46).next_to(flab, DOWN, buff=0.35)
        with self.say("Divide by the mass, and the acceleration is minus k over m, times x. We write k over m as omega squared. So a equals minus omega squared x. Any motion that obeys this rule is called simple harmonic motion. Learn that sentence exactly. Every result in this chapter grows from it."):
            self.play(Write(law))
            self.play(FadeIn(defn, shift=UP * 0.3))
            self.play(s.animate.set_value(TAU * 6), run_time=3.5, rate_func=linear)
        self.play(FadeOut(VGroup(wall, floor, mean, ticks, flab, law, defn)), FadeOut(sys), FadeOut(fx))
        self.remove(sys, fx)
        self.circle_projection()
        self.derivation()
        self.phase_graphs()
        self.example_21()
        self.quiz("In simple harmonic motion, the acceleration is…",
                  ["constant", "∝ displacement, same direction", "∝ displacement, opposite direction", "∝ 1 / displacement"], 2,
                  "Group A, question one. Which statement describes the acceleration in simple harmonic motion? Pause and think.",
                  "C. The acceleration is proportional to the displacement, and opposite to it. That is the minus sign in a equals minus omega squared x. B is the tempting trap: it has the right proportion but the wrong direction, and that would push the body away for ever instead of back to the middle.")

    def circle_projection(self):
        O = np.array([-4.2, -0.2, 0])
        A = 1.7
        th_ = ValueTracker(0)
        circ = Circle(radius=A, color=th.FAINT, stroke_width=3).move_to(O)
        diam = Line(O + DOWN * (A + 0.3), O + UP * (A + 0.3), color=th.MUTED, stroke_width=2)
        ax = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.2, 1.2, 1], x_length=7.4, y_length=A * 2.4,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([2.6, -0.2, 0])
        ax.shift(UP * (O[1] - ax.c2p(0, 0)[1]))
        tl = T("time →", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT)

        def P():
            a = th_.get_value()
            return O + A * np.array([np.cos(a), np.sin(a), 0])

        radius = always_redraw(lambda: Line(O, P(), color=WHITE, stroke_width=3))
        pdot = always_redraw(lambda: Dot(P(), radius=0.1, color=th.AMBER))
        ndot = always_redraw(lambda: Dot([O[0], P()[1], 0], radius=0.12, color=C_X))
        drop = always_redraw(lambda: sdash(P(), [O[0], P()[1], 0], color=th.AMBER, stroke_width=2))
        link = always_redraw(lambda: sdash([O[0], P()[1], 0], ax.c2p(min(th_.get_value(), 4 * PI), np.sin(th_.get_value())), color=C_X, stroke_width=2, stroke_opacity=0.6))
        curve = always_redraw(lambda: ax.plot(np.sin, x_range=[0, max(0.06, min(th_.get_value(), 4 * PI)), 0.03], color=C_X, stroke_width=4))
        ang = always_redraw(lambda: Arc(radius=0.45, start_angle=0, angle=max(1e-3, th_.get_value() % TAU), arc_center=O, color=th.AMBER, stroke_width=3))
        with self.say("Here is the most beautiful picture in this chapter. A point P goes round a circle of radius A at a steady angular speed omega. Now shine a light from the side, and watch its shadow N on the vertical diameter."):
            self.play(Create(circ), FadeIn(diam))
            self.add(radius, ang, drop, pdot, ndot)
            self.play(th_.animate.set_value(TAU), run_time=5, rate_func=linear)
        with self.say("The shadow slides up and down. Fast through the middle, slowing near the ends, stopping for an instant, and turning back. That is exactly simple harmonic motion."):
            self.play(th_.animate.set_value(2 * TAU), run_time=6, rate_func=linear)
        th_.set_value(0)
        eq = M(r"y = A\sin\omega t", size=50, color=C_X).move_to([2.6, 2.4, 0])
        with self.say("Now let time run along a graph to the right, and record the height of the shadow. It draws a perfect sine curve. The height is A sine omega t."):
            self.play(Create(ax), FadeIn(tl))
            self.add(curve, link)
            self.play(th_.animate.set_value(4 * PI), run_time=8, rate_func=linear)
            self.play(Write(eq))
        with self.say("So simple harmonic motion is just uniform circular motion, seen edge on. The angle omega t is called the phase, and one full turn of the circle is one full oscillation."):
            self.play(Indicate(eq, color=th.AMBER), run_time=1.2)
        self.play(FadeOut(VGroup(circ, diam, ax, tl, eq)), FadeOut(radius), FadeOut(pdot), FadeOut(ndot), FadeOut(drop), FadeOut(link), FadeOut(curve), FadeOut(ang))
        self.remove(radius, pdot, ndot, drop, link, curve, ang)

    def derivation(self):
        head = T("Deriving the equation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        lines = [
            (M(r"a = v\frac{dv}{dx} = -\omega^{2}x", size=42), "Now the algebra, so you can derive it in the exam. Write the acceleration as v d v by d x, and set it equal to minus omega squared x."),
            (M(r"\int v\,dv = -\omega^{2}\int x\,dx \;\Rightarrow\; \frac{v^{2}}{2} = -\frac{\omega^{2}x^{2}}{2} + C", size=42), "Separate the variables and integrate both sides. v squared over two equals minus omega squared x squared over two, plus a constant C."),
            (M(r"x = A,\ v = 0 \;\Rightarrow\; C = \frac{\omega^{2}A^{2}}{2}", size=42), "At the extreme position, x equals the amplitude A and the body is momentarily at rest. That fixes C as omega squared A squared over two."),
            (M(r"v = \omega\sqrt{A^{2} - x^{2}}", size=50, color=C_V), "So the speed at any displacement is omega times the square root of A squared minus x squared. Remember this one, it is asked again and again."),
            (M(r"\int \frac{dx}{\sqrt{A^{2}-x^{2}}} = \int \omega\,dt \;\Rightarrow\; \sin^{-1}\frac{x}{A} = \omega t + \phi", size=42), "Write v as d x by d t, separate once more, and integrate. The left side is the inverse sine of x over A."),
            (M(r"x = A\sin(\omega t + \phi)", size=56, color=C_X), "And there it is. x equals A sine of omega t plus phi, where phi, the initial phase, just says where the body was when we started the clock."),
        ]
        ga = VGroup(*[l for l, _ in lines[:3]]).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.5)
        gb = VGroup(*[l for l, _ in lines[3:]]).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.5)
        for grp in (ga, gb):
            if grp.width > 12.4:
                grp.scale_to_fit_width(12.4).next_to(head, DOWN, buff=0.5)
        g = gb
        self.play(FadeIn(head, shift=DOWN * 0.2))
        for i, (l, say) in enumerate(lines):
            if i == 3:
                self.play(FadeOut(ga, shift=UP * 0.4), run_time=0.6)
            with self.say(say):
                self.play(Write(l), run_time=1.4)
        self.play(Circumscribe(gb[-1], color=C_X), Circumscribe(gb[0], color=C_V), run_time=1.4)
        g = gb
        nb = self.neby("success", height=1.4).to_corner(DR, buff=0.5)
        self.add(nb)
        self.play(FadeIn(nb, scale=0.5), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(VGroup(head, g)), FadeOut(nb))
        self.remove(nb)

    def phase_graphs(self):
        t = ValueTracker(0)
        rows = []
        names = [(r"x", C_X, np.sin, r"x = A\sin\omega t"), (r"v", C_V, np.cos, r"v = A\omega\cos\omega t"), (r"a", C_A, lambda u: -np.sin(u), r"a = -A\omega^{2}\sin\omega t")]
        allg = VGroup()
        for i, (n, c, f, lab) in enumerate(names):
            ax = Axes(x_range=[0, TAU, PI / 2], y_range=[-1.3, 1.3, 1], x_length=6.6, y_length=1.55,
                      axis_config={"color": th.FAINT, "stroke_width": 2, "include_tip": False}).move_to([2.6, 1.85 - i * 1.95, 0])
            curve = ax.plot(f, x_range=[0, TAU, 0.03], color=c, stroke_width=4)
            name = M(lab, size=30, color=c).next_to(ax, LEFT, buff=0.25)
            if name.get_left()[0] < -4.6:
                name.scale_to_fit_width(3.8).next_to(ax, LEFT, buff=0.2)
            rows.append((ax, curve, f, c))
            allg.add(VGroup(ax, curve, name))
        xl = VGroup(*[M(s, size=24, color=th.MUTED).next_to(rows[2][0].c2p(v, -1.3), DOWN, buff=0.1)
                      for s, v in [("0", 0), ("T/4", PI / 2), ("T/2", PI), ("3T/4", 3 * PI / 2), ("T", TAU)]])
        cursor = always_redraw(lambda: DashedLine(rows[0][0].c2p(t.get_value(), 1.3), rows[2][0].c2p(t.get_value(), -1.3), color=WHITE, stroke_width=2))
        dots = VGroup(*[always_redraw(lambda r=r: Dot(r[0].c2p(t.get_value(), r[2](t.get_value())), radius=0.08, color=r[3])) for r in rows])
        bx = -5.9
        base = np.array([bx, -0.1, 0])
        rail = Line(base + UP * 2.4, base + DOWN * 2.4, color=th.FAINT, stroke_width=3)
        ends = VGroup(*[Line(base + UP * k + LEFT * 0.25, base + UP * k + RIGHT * 0.25, color=th.MUTED, stroke_width=2) for k in (-1.9, 0, 1.9)])
        tags = VGroup(M("+A", size=24, color=th.MUTED).next_to(ends[2], LEFT), M("0", size=24, color=th.MUTED).next_to(ends[1], LEFT), M("-A", size=24, color=th.MUTED).next_to(ends[0], LEFT))

        def bob():
            u = t.get_value()
            p = base + UP * 1.9 * np.sin(u)
            g = VGroup(Dot(p, radius=0.16, color=C_X))
            v = np.cos(u)
            a = -np.sin(u)
            if abs(v) > 0.05:
                g.add(arrow(p + RIGHT * 0.35, p + RIGHT * 0.35 + UP * 1.0 * v, C_V))
            if abs(a) > 0.05:
                g.add(arrow(p + LEFT * 0.35, p + LEFT * 0.35 + UP * 1.0 * a, C_A))
            return g
        b = always_redraw(bob)
        with self.say("Differentiate x, and you get the velocity, A omega cosine omega t. Differentiate again, and you get the acceleration, minus A omega squared sine omega t, which is minus omega squared x, as promised."):
            self.play(LaggedStart(*[Create(r[0]) for r in allg], lag_ratio=0.2), run_time=1.2)
            for r in allg:
                self.play(Create(r[1]), FadeIn(r[2]), run_time=1.1)
            self.play(FadeIn(xl))
        with self.say("Now let the clock run, and watch the body on the left. Green is velocity, red is acceleration.") as v:
            self.play(FadeIn(rail), FadeIn(ends), FadeIn(tags))
            self.add(b, cursor, dots)
            self.play(t.animate.set_value(TAU), run_time=max(3, v.dur - 1), rate_func=linear)
        with self.say("At the mean position, the speed is greatest, A omega, and the acceleration is zero. At the extreme positions, the body stops for an instant, and the acceleration is greatest, omega squared A, pointing back to the middle."):
            self.play(t.animate.set_value(0), run_time=0.01)
            self.play(t.animate.set_value(PI / 2), run_time=2.5, rate_func=smooth)
            self.wait(0.6)
            self.play(t.animate.set_value(PI), run_time=2.5, rate_func=smooth)
            self.wait(0.6)
        with self.say("Look at the curves. Velocity peaks a quarter period before displacement. It leads by pi by two. And acceleration is always the mirror image of displacement, exactly pi out of phase."):
            self.play(t.animate.set_value(TAU), run_time=4, rate_func=linear)
        self.play(FadeOut(VGroup(allg, xl, rail, ends, tags)), FadeOut(cursor), FadeOut(dots), FadeOut(b))
        self.remove(cursor, dots, b)
        hdr = ["Position", "x", "speed", "acceleration"]
        data = [["mean,  x = 0", "0", "max  Aω", "0"], ["extreme,  x = ±A", "±A", "0", "max  ω²A"]]
        tbl = VGroup()
        widths = [3.8, 1.6, 2.4, 2.8]
        for r, row in enumerate([hdr] + data):
            cells = VGroup()
            x = -sum(widths) / 2
            for c, (txt, w) in enumerate(zip(row, widths)):
                col = th.MUTED if r == 0 else ([th.INK, C_X, C_V, C_A][c])
                cell = T(txt, size=26 if r else 22, color=col, weight="SEMIBOLD" if r == 0 else "NORMAL").move_to([x + w / 2, 1.0 - r * 0.9, 0])
                cells.add(cell)
                x += w
            tbl.add(cells)
        lines = VGroup(*[Line([-5.4, 0.55 - r * 0.9, 0], [5.4, 0.55 - r * 0.9, 0], color=th.FAINT, stroke_width=2) for r in range(2)])
        per = M(r"T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}}", r"\qquad f = \frac{1}{T} = \frac{\omega}{2\pi}", size=46).to_edge(DOWN, buff=1.0)
        with self.say("Here is that summary as a table, worth two easy marks. And one full circle is two pi radians, so the period is T equals two pi over omega, which for the spring is two pi root m over k. The frequency is one over T."):
            self.play(FadeIn(tbl[0]), Create(lines))
            self.play(LaggedStart(FadeIn(tbl[1], shift=UP * 0.2), FadeIn(tbl[2], shift=UP * 0.2), lag_ratio=0.4))
            self.play(Write(per))
        self.play(FadeOut(VGroup(tbl, lines, per)))

    def example_21(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A particle executes SHM of amplitude 5 cm and period 2 s. Find (a) its maximum velocity, (b) its maximum acceleration, (c) its velocity and acceleration when the displacement is 3 cm.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"\omega = \frac{2\pi}{T} = \frac{2\pi}{2} = \pi \approx 3.14\ \text{rad s}^{-1},\quad A = 0.05\ \text{m}", size=38),
            M(r"v_{\max} = A\omega = 0.05 \times 3.14 = 0.157\ \text{m s}^{-1}", size=38, color=C_V),
            M(r"a_{\max} = A\omega^{2} = 0.05 \times 9.87 = 0.493\ \text{m s}^{-2}", size=38, color=C_A),
            M(r"v = \omega\sqrt{A^{2}-x^{2}} = 3.14\sqrt{0.05^{2}-0.03^{2}} = 3.14 \times 0.04 = 0.126\ \text{m s}^{-1}", size=38, color=C_V),
            M(r"|a| = \omega^{2}x = 9.87 \times 0.03 = 0.296\ \text{m s}^{-2}\ \text{(towards the mean)}", size=38, color=C_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        if steps.width > 12.6:
            steps.scale_to_fit_width(12.6).align_to(prob, LEFT)
        with self.say("Let us use all of this. A particle performs simple harmonic motion with amplitude five centimetres and period two seconds. Find its maximum velocity, its maximum acceleration, and its velocity and acceleration at a displacement of three centimetres."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("First, omega is two pi over T, two pi over two, which is pi, about three point one four radians per second. And convert the amplitude to metres: zero point zero five."):
            self.play(Write(steps[0]))
        with self.say("The maximum velocity, at the mean position, is A omega: zero point zero five times three point one four, which is zero point one five seven metres per second."):
            self.play(Write(steps[1]))
        with self.say("The maximum acceleration, at the extremes, is A omega squared: zero point zero five times nine point eight seven, about zero point four nine three metres per second squared."):
            self.play(Write(steps[2]))
        with self.say("At three centimetres, the speed is omega root A squared minus x squared. Root of zero point zero five squared minus zero point zero three squared is zero point zero four. A three four five triangle, hiding in plain sight. Times pi gives zero point one two six metres per second."):
            self.play(Write(steps[3]))
        with self.say("And the acceleration there is omega squared x: nine point eight seven times zero point zero three, about zero point two nine six metres per second squared, pointing back towards the mean position."):
            self.play(Write(steps[4]))
        self.wait(0.5)
        self.play(FadeOut(VGroup(head, prob, steps)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        y0 = 2.0
        wall_x = -6.0
        mean_x = -2.6
        A = 1.5
        s = ValueTracker(0)
        Aval = ValueTracker(1.0)

        def X():
            return A * Aval.get_value() * np.cos(s.get_value())

        wall = hatch([wall_x, y0, 0], width=1.4, vertical=True)
        floor = Line([wall_x, y0 - 0.4, 0], [0.4, y0 - 0.4, 0], color=th.FAINT, stroke_width=3)
        sys = always_redraw(lambda: VGroup(spring([wall_x, y0, 0], [mean_x + X() - 0.45, y0, 0], coils=9), block([mean_x + X(), y0, 0], h=0.65)))
        ax = Axes(x_range=[-1.15, 1.15, 1], y_range=[0, 0.65, 0.5], x_length=6.2, y_length=3.4,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([-2.4, -1.5, 0])
        Uc = ax.plot(lambda x: 0.5 * x * x, x_range=[-1, 1, 0.02], color=C_U, stroke_width=4)
        Kc = ax.plot(lambda x: 0.5 * (1 - x * x), x_range=[-1, 1, 0.02], color=C_K, stroke_width=4)
        Ec = DashedLine(ax.c2p(-1.1, 0.5), ax.c2p(1.1, 0.5), color=C_E, stroke_width=3)
        xl = VGroup(M("-A", size=26, color=th.MUTED).next_to(ax.c2p(-1, 0), DOWN, buff=0.12), M("0", size=26, color=th.MUTED).next_to(ax.c2p(0, 0), DOWN, buff=0.12),
                    M("+A", size=26, color=th.MUTED).next_to(ax.c2p(1, 0), DOWN, buff=0.12))
        lu = M(r"U", size=32, color=C_U).next_to(ax.c2p(1, 0.5), RIGHT, buff=0.1).shift(DOWN * 0.25)
        lk = M(r"K", size=32, color=C_K).next_to(ax.c2p(0, 0.5), UP, buff=0.08).shift(LEFT * 0.4 + DOWN * 0.3)
        le = M(r"E", size=32, color=C_E).next_to(Ec, RIGHT, buff=0.1)

        def xn():
            return X() / A

        def tracers():
            x = np.clip(xn(), -1, 1)
            return VGroup(sdash(ax.c2p(x, 0), ax.c2p(x, 0.5), color=WHITE, stroke_width=1.5, stroke_opacity=0.5),
                          Dot(ax.c2p(x, 0.5 * x * x), radius=0.09, color=C_U), Dot(ax.c2p(x, 0.5 * (1 - x * x)), radius=0.09, color=C_K))
        tr = always_redraw(tracers)

        def bars():
            a = Aval.get_value()
            x = X() / A
            U = 0.5 * x * x
            K = 0.5 * (a * a - x * x)
            g = VGroup()
            for i, (val, col, nm) in enumerate([(K, C_K, "K"), (U, C_U, "U"), (K + U, C_E, "E")]):
                base = np.array([2.6 + i * 1.3, -3.0, 0])
                h = max(0.02, 4.4 * val)
                g.add(Rectangle(width=0.8, height=h, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to(base, aligned_edge=DOWN))
            return g
        bb = always_redraw(bars)
        blabs = VGroup(*[M(n, size=32, color=c).move_to([2.6 + i * 1.3, -3.25, 0]) for i, (n, c) in enumerate([("K", C_K), ("U", C_U), ("E", C_E)])])
        with self.say("A spring that is stretched stores energy, and a block that moves carries energy. In simple harmonic motion, the two keep trading places. Let us watch the trade."):
            self.play(FadeIn(wall), Create(floor))
            self.add(sys)
            self.play(FadeIn(sys))
            self.add(bb)
            self.play(FadeIn(blabs), FadeIn(bb))
            self.play(s.animate.set_value(TAU), run_time=4, rate_func=linear)
        eqs = VGroup(
            M(r"U = \int_0^x kx\,dx = \tfrac12 kx^{2} = \tfrac12 m\omega^{2}x^{2}", size=34, color=C_U),
            M(r"K = \tfrac12 mv^{2} = \tfrac12 m\omega^{2}(A^{2}-x^{2})", size=34, color=C_K),
            M(r"E = K + U = \tfrac12 m\omega^{2}A^{2} = \tfrac12 kA^{2}", size=40, color=C_E),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 2.3, 0])
        if eqs.width > 6.4:
            eqs.scale_to_fit_width(6.4).move_to([3.5, 2.3, 0])
        with self.say("The work done to stretch the spring by x, against the force k x, is stored as potential energy: half k x squared, which is half m omega squared x squared."):
            self.play(Write(eqs[0]))
            self.play(Create(ax), FadeIn(xl), Create(Uc), FadeIn(lu))
        with self.say("The kinetic energy is half m v squared. Use v equals omega root A squared minus x squared, and it becomes half m omega squared, times A squared minus x squared."):
            self.play(Write(eqs[1]))
            self.play(Create(Kc), FadeIn(lk))
        with self.say("Now add them. The x squared terms cancel, and the total is half m omega squared A squared, half k A squared. It does not depend on x at all. The total energy is constant."):
            self.play(Write(eqs[2]))
            self.play(Create(Ec), FadeIn(le))
            self.sfx("shimmer", gain=-14)
        self.add(tr)
        with self.say("Watch the dots ride the curves. At the mean position, everything is kinetic. At the extremes, everything is potential. In between, the two always add up to the same total, the dashed line."):
            self.play(s.animate.set_value(TAU * 3), run_time=9, rate_func=linear)
        with self.say("And notice, energy depends on the square of the amplitude. Double the amplitude, and the energy becomes four times as large."):
            self.play(FadeOut(tr), FadeOut(VGroup(Uc, Kc, Ec, lu, lk, le, xl, ax)))
            self.remove(tr)
            four = M(r"A \to 2A \;\Rightarrow\; E \to 4E", size=46, color=th.AMBER).move_to([-2.4, -1.4, 0])
            self.play(Aval.animate.set_value(1.0), run_time=0.01)
            self.play(FadeIn(four, shift=UP * 0.2))
        self.remove(bb)
        bb2 = always_redraw(lambda: VGroup(*[Rectangle(width=0.8, height=max(0.02, 4.4 * v), fill_color=c, fill_opacity=0.9, stroke_width=0)
                                               .move_to(np.array([2.6 + i * 1.3, -3.0, 0]), aligned_edge=DOWN)
                                               for i, (v, c) in enumerate([(0.5 * (1 - np.cos(s.get_value()) ** 2) * Aval.get_value() ** 2 * 0.25, C_K),
                                                                           (0.5 * np.cos(s.get_value()) ** 2 * Aval.get_value() ** 2 * 0.25, C_U),
                                                                           (0.5 * Aval.get_value() ** 2 * 0.25, C_E)])]))
        self.add(bb2)
        sys2 = always_redraw(lambda: VGroup(spring([wall_x, y0, 0], [mean_x + 0.75 * Aval.get_value() * np.cos(s.get_value()) - 0.45, y0, 0], coils=9),
                                            block([mean_x + 0.75 * Aval.get_value() * np.cos(s.get_value()), y0, 0], h=0.65)))
        self.remove(sys)
        self.add(sys2)
        with self.say("Here the amplitude goes from small to twice as big. Watch the purple bar: not twice as tall, but four times.") as v:
            self.play(s.animate.set_value(TAU * 4), run_time=2.5, rate_func=linear)
            self.play(Aval.animate.set_value(2.0), s.animate.set_value(TAU * 5), run_time=3, rate_func=linear)
            self.play(s.animate.set_value(TAU * 6), run_time=max(0.5, v.dur - 5.5), rate_func=linear)
        avg = M(r"\langle K \rangle = \langle U \rangle = \tfrac12 E", size=38, color=th.BODY).next_to(four, DOWN, buff=0.4)
        with self.say("One more fact for multiple choice: averaged over a whole cycle, the kinetic and potential energies are equal, each one half of the total."):
            self.play(FadeIn(avg, shift=UP * 0.2))
            self.play(s.animate.set_value(TAU * 7), run_time=3, rate_func=linear)
        self.play(FadeOut(VGroup(wall, floor, eqs, four, avg, blabs)), FadeOut(bb2), FadeOut(sys2))
        self.remove(bb2, sys2)
        self.example_22()

    def example_22(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A 0.5 kg body on a spring of force constant 200 N/m oscillates with amplitude 0.10 m. Find the period, the total energy, and K and U when the displacement is 0.05 m.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"\omega = \sqrt{k/m} = \sqrt{200/0.5} = 20\ \text{rad s}^{-1},\quad T = \frac{2\pi}{20} = 0.314\ \text{s}", size=38),
            M(r"E = \tfrac12 kA^{2} = \tfrac12(200)(0.10)^{2} = 1.0\ \text{J}", size=38, color=C_E),
            M(r"U = \tfrac12(200)(0.05)^{2} = 0.25\ \text{J}", size=38, color=C_U),
            M(r"K = E - U = 0.75\ \text{J},\quad v = \sqrt{2K/m} = \sqrt{3} = 1.73\ \text{m s}^{-1}", size=38, color=C_K),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        pie = VGroup()
        with self.say("A worked example. A half kilogram body on a spring of force constant two hundred newtons per metre oscillates with amplitude ten centimetres. Find the period, the total energy, and the kinetic and potential energies at five centimetres."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("Omega is root of k over m, root of four hundred, which is twenty radians per second. So T equals two pi over twenty, about zero point three one four seconds."):
            self.play(Write(steps[0]))
        with self.say("The total energy is half k A squared: half times two hundred times zero point one squared, exactly one joule."):
            self.play(Write(steps[1]))
        with self.say("At five centimetres, the potential energy is half times two hundred times zero point zero five squared, zero point two five joules. Half the amplitude gives only a quarter of the energy as potential."):
            self.play(Write(steps[2]))
        with self.say("The rest, zero point seven five joules, is kinetic. That gives a speed of root three, about one point seven three metres per second."):
            self.play(Write(steps[3]))
            c = np.array([4.6, -2.3, 0])
            pie = VGroup(Sector(radius=0.85, angle=TAU * 0.25, start_angle=PI / 2, fill_color=C_U, fill_opacity=0.9, stroke_width=0).move_arc_center_to(c),
                         Sector(radius=0.85, angle=TAU * 0.75, start_angle=PI / 2 + TAU * 0.25, fill_color=C_K, fill_opacity=0.9, stroke_width=0).move_arc_center_to(c))
            self.play(FadeIn(pie, scale=0.6))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps, pie)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        top_y = 2.8
        xs = [-5.6, -3.6, -1.6]
        e = 1.2
        L0 = 2.3
        ceil = VGroup(*[hatch([x, top_y, 0], width=1.4) for x in xs])
        s0 = spring([xs[0], top_y, 0], [xs[0], top_y - L0, 0], coils=8)
        end0 = DashedLine([xs[0] - 0.7, top_y - L0, 0], [xs[2] + 0.9, top_y - L0, 0], color=th.MUTED, stroke_width=2)
        l0 = T("unloaded", size=22, color=th.MUTED).move_to([xs[0], -2.9, 0])
        stretch = ValueTracker(0)
        s1 = always_redraw(lambda: VGroup(spring([xs[1], top_y, 0], [xs[1], top_y - L0 - stretch.get_value(), 0], coils=8),
                                          block([xs[1], top_y - L0 - stretch.get_value() - 0.32, 0], w=0.8, h=0.64)))
        l1 = T("equilibrium", size=22, color=th.MUTED).move_to([xs[1], -2.9, 0])
        with self.say("Now hang the spring vertically, and hook a mass m on its end. The spring stretches until its pull upward balances the weight."):
            self.play(FadeIn(ceil[0]), Create(s0), FadeIn(l0))
            self.play(Create(end0))
            self.play(FadeIn(ceil[1]))
            self.add(s1)
            self.play(FadeIn(s1), FadeIn(l1))
            self.play(stretch.animate.set_value(e), run_time=1.6, rate_func=rate_functions.ease_out_bounce)
        eb = DoubleArrow([xs[1] + 0.65, top_y - L0, 0], [xs[1] + 0.65, top_y - L0 - e, 0], buff=0, color=th.CORAL, stroke_width=4, tip_length=0.18)
        el = M("e", size=34, color=th.CORAL).next_to(eb, RIGHT, buff=0.1)
        eq1 = M(r"mg = ke", r"\;\Rightarrow\; k = \frac{mg}{e}", size=48).move_to([3.9, 1.6, 0])
        mean1 = DashedLine([xs[1] - 0.7, top_y - L0 - e - 0.32, 0], [xs[2] + 0.9, top_y - L0 - e - 0.32, 0], color=th.AMBER, stroke_width=2)
        ml = T("new mean", size=20, color=th.AMBER).next_to(mean1, LEFT, buff=0.12)
        with self.say("Call that static extension e. At balance, m g equals k e. So the force constant is m g over e. This stretched position is the new mean position."):
            self.play(GrowFromCenter(eb), FadeIn(el))
            self.play(Write(eq1))
            self.play(Create(mean1), FadeIn(ml))
        xd = ValueTracker(0.7)
        ph = ValueTracker(0)
        osc = ValueTracker(0)

        def ypos():
            return top_y - L0 - e - xd.get_value() * np.cos(ph.get_value()) * (1 if osc.get_value() > 0.5 else 1)

        def rig2():
            yb = ypos()
            g = VGroup(spring([xs[2], top_y, 0], [xs[2], yb, 0], coils=8), block([xs[2], yb - 0.32, 0], w=0.8, h=0.64))
            x = (top_y - L0 - e) - yb
            up = 0.55 * (e + x)
            g.add(arrow([xs[2] + 0.6, yb - 0.32, 0], [xs[2] + 0.6, yb - 0.32 + up, 0], th.MINT, 5))
            g.add(arrow([xs[2] - 0.6, yb - 0.32, 0], [xs[2] - 0.6, yb - 0.32 - 0.55 * e, 0], th.SKY, 5))
            return g
        s2 = always_redraw(rig2)
        l2 = T("displaced by x", size=22, color=th.MUTED).move_to([xs[2], -2.9, 0])
        fl = VGroup(M(r"k(e+x)", size=30, color=th.MINT), M(r"mg", size=30, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-0.1, -2.2, 0])
        with self.say("Now pull it down a further distance x, and let go. The spring, stretched by e plus x, pulls up with k times e plus x. The weight m g still pulls down."):
            self.play(FadeIn(ceil[2]), FadeIn(l2))
            self.add(s2)
            self.play(FadeIn(s2), FadeIn(fl))
        der = VGroup(
            M(r"F = mg - k(e+x)", size=40),
            M(r"\phantom{F} = ke - ke - kx", size=40),
            M(r"F = -kx", size=48, color=C_F),
            M(r"a = -\frac{k}{m}x", size=44),
            M(r"T = 2\pi\sqrt{\frac{m}{k}} = 2\pi\sqrt{\frac{e}{g}}", size=48, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.0, -0.4, 0])
        if der.height > 4.4:
            der.scale_to_fit_height(4.4).move_to([4.0, -0.5, 0])
        with self.say("The net force, taking down as positive, is m g minus k times e plus x. But m g is k e. So k e minus k e minus k x. The weight cancels completely, and F equals minus k x."):
            self.play(FadeOut(eq1), run_time=0.4)
            self.play(Write(der[0]))
            self.play(Write(der[1]))
            self.play(Write(der[2]))
            self.play(Circumscribe(der[2], color=C_F))
        with self.say("Gravity only shifts the mean position downward. About that new centre, the motion is the same simple harmonic motion, with a equals minus k over m, x."):
            self.play(Write(der[3]))
            self.play(ph.animate.set_value(TAU * 3), run_time=6, rate_func=linear)
        nb = self.neby("cool", height=1.3).move_to([-5.6, -1.6, 0])
        with self.say("So the period is two pi root m over k. And since k equals m g over e, the mass cancels again: T equals two pi root e over g. Measure how far a load stretches a spring, and you can predict its period without a stopwatch."):
            self.play(Write(der[4]))
            self.add(nb)
            self.play(FadeIn(nb, scale=0.5))
            self.play(ph.animate.set_value(TAU * 6), run_time=6, rate_func=linear)
        self.play(FadeOut(VGroup(ceil, s0, end0, l0, l1, l2, eb, el, mean1, ml, fl, der)), FadeOut(s1), FadeOut(s2), FadeOut(nb))
        self.remove(s1, s2, nb)
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A 0.5 kg mass hung from a light spiral spring stretches it by 10 cm. Find the force constant and the period of vertical oscillation. (g = 9.8 m/s²)", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"k = \frac{mg}{e} = \frac{0.5 \times 9.8}{0.10} = 49\ \text{N m}^{-1}", size=42),
            M(r"T = 2\pi\sqrt{\frac{e}{g}} = 2\pi\sqrt{\frac{0.10}{9.8}} = 2\pi(0.101) = 0.635\ \text{s}", size=42, color=th.AMBER),
            M(r"f = \frac{1}{T} = 1.58\ \text{Hz}", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(prob, DOWN, buff=0.6).align_to(prob, LEFT)
        with self.say("Try this one. A half kilogram mass hung from a spring stretches it by ten centimetres. Find the force constant and the period of vertical oscillation."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("k equals m g over e: zero point five times nine point eight, over zero point one, which is forty nine newtons per metre."):
            self.play(Write(steps[0]))
        with self.say("The period is two pi root e over g: root of zero point one over nine point eight is about zero point one zero one, so T is about zero point six three five seconds. That is a frequency of about one point five eight hertz."):
            self.play(Write(steps[1]))
            self.play(Write(steps[2]))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("A mass m hanging from a spring of force constant k oscillates with period…",
                  [M(r"2\pi\sqrt{k/m}", size=40), M(r"2\pi\sqrt{m/k}", size=40), M(r"2\pi\sqrt{mk}", size=40), M(r"\tfrac{1}{2\pi}\sqrt{m/k}", size=40)], 1,
                  "Quick check. A mass m hangs from a spring of force constant k. What is its period? Pause and think.",
                  "B, two pi root m over k. Check it with common sense: a heavier mass should swing more slowly, so m must be on top. A has it upside down, which is the most common slip, and D is the frequency formula mixed up with the period.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        self.torsion()
        self.pendulum()
        self.small_angle()
        self.laws()
        self.example_24()

    def torsion(self):
        O = np.array([-3.3, -0.6, 0])
        a = ValueTracker(0)
        sup = hatch([-3.3, 2.9, 0], width=1.4)
        wire = Line([-3.3, 2.9, 0], O + UP * 0.2, color=th.BODY, stroke_width=3)

        def disc():
            ang = a.get_value()
            g = VGroup(Ellipse(width=3.2, height=0.9, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=th.SKY, stroke_width=3).move_to(O))
            p = O + np.array([1.5 * np.cos(ang - PI / 2), 0.42 * np.sin(ang - PI / 2), 0])
            g.add(Line(O, p, color=th.AMBER, stroke_width=5), Dot(p, radius=0.08, color=th.AMBER))
            return g
        d = always_redraw(disc)
        eqs = VGroup(M(r"\tau = -c\theta", size=48), M(r"I\frac{d^{2}\theta}{dt^{2}} = -c\theta", size=44), M(r"T = 2\pi\sqrt{\frac{I}{c}}", size=52, color=th.AMBER)).arrange(DOWN, buff=0.4).move_to([3.3, 0.2, 0])
        with self.say("Simple harmonic motion can also be a twist. Hang a disc from a wire and turn it a little. The twisted wire pushes back with a restoring torque, proportional to the angle: tau equals minus c theta."):
            self.play(FadeIn(sup), Create(wire))
            self.add(d)
            self.play(FadeIn(d))
            self.play(Write(eqs[0]))
            self.play(a.animate.set_value(1.0), run_time=1.2)
            self.play(a.animate.set_value(-1.0), run_time=1.6, rate_func=smooth)
            self.play(a.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        with self.say("Torque equals I alpha, so I times d two theta by d t squared equals minus c theta. It is the same equation in angular clothes, so the period is two pi root I over c. This is angular simple harmonic motion, and it is how the coil of a galvanometer swings."):
            self.play(Write(eqs[1]))
            self.play(Write(eqs[2]))
            for k in range(2):
                self.play(a.animate.set_value(-1.0), run_time=1.6, rate_func=smooth)
                self.play(a.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        self.play(FadeOut(VGroup(sup, wire, eqs)), FadeOut(d))
        self.remove(d)

    def pendulum(self):
        P = np.array([-3.2, 2.9, 0])
        L = 4.2
        th0 = 0.42
        s = ValueTracker(0)

        def ang():
            return th0 * np.cos(s.get_value())

        def bobpos():
            a = ang()
            return P + L * np.array([np.sin(a), -np.cos(a), 0])

        sup = hatch(P, width=1.8)
        vert = DashedLine(P, P + DOWN * (L + 0.3), color=th.FAINT, stroke_width=2)
        rod = always_redraw(lambda: Line(P, bobpos(), color=th.BODY, stroke_width=3))
        bob = always_redraw(lambda: Circle(radius=0.26, fill_color=th.SKY, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2).move_to(bobpos()))
        arcm = always_redraw(lambda: Arc(radius=1.1, start_angle=-PI / 2, angle=ang() if abs(ang()) > 1e-3 else 1e-3, arc_center=P, color=th.CORAL, stroke_width=3))
        thl = always_redraw(lambda: M(r"\theta", size=30, color=th.CORAL).move_to(P + 1.45 * np.array([np.sin(ang() / 2), -np.cos(ang() / 2), 0])))
        Ll = M("L", size=32).move_to(P + 2.1 * np.array([np.sin(th0), -np.cos(th0), 0]) + RIGHT * 0.3)

        def forces():
            a = ang()
            B = bobpos()
            g = 1.5
            rad = np.array([np.sin(a), -np.cos(a), 0])
            tan = np.array([np.cos(a), np.sin(a), 0])
            grp = VGroup(arrow(B, B + DOWN * g, th.MINT, 5))
            grp.add(arrow(B, B + rad * g * np.cos(a), th.MUTED, 4))
            if abs(np.sin(a)) > 0.03:
                grp.add(arrow(B, B - tan * g * np.sin(a) * 2.2, th.CORAL, 6))
            return grp
        fr = always_redraw(forces)
        lab = VGroup(M(r"mg", size=30, color=th.MINT), M(r"mg\cos\theta", size=30, color=th.MUTED), M(r"mg\sin\theta", size=30, color=th.CORAL)).arrange(RIGHT, buff=0.5).move_to([1.6, -2.9, 0])
        with self.say("Now the most famous oscillator of all: the simple pendulum. A small heavy bob on a light string of length L, hung from a rigid support."):
            self.play(FadeIn(sup), Create(vert))
            self.add(rod, bob)
            self.play(FadeIn(rod), FadeIn(bob), FadeIn(Ll))
            self.add(arcm, thl)
            self.play(s.animate.set_value(TAU), run_time=3.5, rate_func=linear)
        with self.say("When the string makes an angle theta with the vertical, split the weight m g in two. Along the string, m g cos theta, which the tension balances. Across it, m g sine theta. That component has nothing to balance it. It is the restoring force, always pulling the bob back towards the lowest point."):
            self.add(fr)
            self.play(FadeIn(lab))
            self.play(s.animate.set_value(TAU * 3), run_time=8, rate_func=linear)
        der = VGroup(
            M(r"F = -mg\sin\theta", size=40),
            M(r"\sin\theta \approx \theta,\quad x = L\theta", size=40, color=th.AMBER),
            M(r"F = -mg\frac{x}{L} \;\Rightarrow\; a = -\frac{g}{L}x", size=40),
            M(r"\omega^{2} = \frac{g}{L} \;\Rightarrow\; T = 2\pi\sqrt{\frac{L}{g}}", size=46, color=th.SKY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.3, 0])
        with self.say("So F equals minus m g sine theta. That is not quite simple harmonic, because sine theta is not the same as theta. But for small angles, measured in radians, sine theta is very nearly theta. And the arc length x equals L theta."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
        with self.say("Then F equals minus m g x over L, so a equals minus g over L, times x. Simple harmonic motion, with omega squared equal to g over L. And the period is two pi root L over g."):
            self.play(Write(der[2]))
            self.play(Write(der[3]))
            self.sfx("impact", gain=-14)
            self.play(Circumscribe(der[3], color=th.SKY))
            self.play(s.animate.set_value(TAU * 5), run_time=6, rate_func=linear)
        self.play(FadeOut(VGroup(sup, vert, Ll, lab, der)), FadeOut(rod), FadeOut(bob), FadeOut(arcm), FadeOut(thl), FadeOut(fr))
        self.remove(rod, bob, arcm, thl, fr)

    def small_angle(self):
        ax = Axes(x_range=[0, 1.6, 0.5], y_range=[0, 1.6, 0.5], x_length=5.4, y_length=4.4,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([-3.3, -0.3, 0])
        lin = ax.plot(lambda x: x, x_range=[0, 1.55], color=th.AMBER, stroke_width=4)
        sn = ax.plot(np.sin, x_range=[0, 1.55], color=th.SKY, stroke_width=4)
        l1 = M(r"\theta", size=32, color=th.AMBER).next_to(ax.c2p(1.5, 1.5), LEFT, buff=0.15)
        l2 = M(r"\sin\theta", size=32, color=th.SKY).next_to(ax.c2p(1.55, np.sin(1.55)), DOWN, buff=0.2)
        xl = T("θ (radians)", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
        rows = [("5°", "0.0873", "0.0872", "0.13 %"), ("10°", "0.1745", "0.1736", "0.51 %"), ("20°", "0.3491", "0.3420", "2.1 %"), ("45°", "0.7854", "0.7071", "11 %")]
        hdr = VGroup(*[T(h, size=22, color=th.MUTED, weight="SEMIBOLD") for h in ["angle", "θ (rad)", "sin θ", "error"]])
        table = VGroup()
        for r, row in enumerate([None] + rows):
            cells = hdr if row is None else VGroup(*[T(c, size=26, color=[th.INK, th.AMBER, th.SKY, th.MINT if r < 3 else th.CORAL][i]) for i, c in enumerate(row)])
            for i, c in enumerate(cells):
                c.move_to([1.3 + i * 1.5, 1.6 - r * 0.7, 0])
            table.add(cells)
        with self.say("How small is small? Plot theta and sine theta together. Near zero, the two curves sit on top of each other. Further out, they drift apart."):
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(lin), FadeIn(l1))
            self.play(Create(sn), FadeIn(l2))
        with self.say("At five degrees, the error is a tenth of a percent. At ten degrees, half a percent. But at forty five degrees, it is eleven percent, and the formula breaks down. Keep the swing to a few degrees."):
            self.play(FadeIn(table[0]))
            for k in range(1, 5):
                self.sfx("tick", gain=-12)
                self.play(FadeIn(table[k], shift=UP * 0.15), run_time=0.6)
                self.wait(0.6)
            self.play(Indicate(table[4], color=th.CORAL))
        self.play(FadeOut(VGroup(ax, lin, sn, l1, l2, xl, table)))
        self.tip("T = 2π√(L/g) holds only for small amplitudes (a few degrees), with θ in radians. For large swings the motion is periodic but NOT simple harmonic, and the period is longer.",
                 "Exam tip. When you derive the pendulum formula, always state the assumption: small amplitude, so that sine theta is approximately theta in radians. Examiners give a mark for that line. For large swings, the motion is still periodic, but it is no longer simple harmonic, and the real period is longer.")

    def laws(self):
        title = T("Laws of the simple pendulum", size=38, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        s = ValueTracker(0)
        top = 2.2
        th0 = 0.35

        def pend(px, L, w, r, col):
            def f():
                a = th0 * np.cos(w * s.get_value())
                P = np.array([px, top, 0])
                B = P + L * np.array([np.sin(a), -np.cos(a), 0])
                return VGroup(Line(P + LEFT * 0.5, P + RIGHT * 0.5, color=th.BODY, stroke_width=4), Line(P, B, color=th.BODY, stroke_width=2.5),
                              Circle(radius=r, fill_color=col, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2).move_to(B))
            return always_redraw(f)
        a1 = pend(-5.6, 4.4, 1.0, 0.16, th.SKY)
        a2 = pend(-4.2, 4.4, 1.0, 0.34, th.AMBER)
        lm = T("same L, different mass", size=22, color=th.MUTED).move_to([-4.9, -2.85, 0])
        b1 = pend(-2.4, 1.1, 2.0, 0.2, th.MINT)
        b2 = pend(-0.9, 4.4, 1.0, 0.2, th.PINK)
        lL = VGroup(M("L", size=30, color=th.MINT).move_to([-1.9, 1.5, 0]), M("4L", size=30, color=th.PINK).move_to([-1.3, -1.2, 0]).shift(LEFT * 0.0))
        cnt = ValueTracker(0)
        laws = VGroup(
            M(r"T \propto \sqrt{L}", size=44), M(r"T \propto \frac{1}{\sqrt{g}}", size=44),
            T("independent of the mass", size=28, color=th.BODY), T("independent of small amplitude", size=28, color=th.BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.4, 0])
        if laws.width > 4.6:
            laws.scale_to_fit_width(4.6).move_to([4.3, -0.4, 0])
        self.play(FadeIn(title))
        self.add(a1, a2)
        with self.say("The formula hides four laws. First: mass does not appear. Hang a light bob and a heavy bob on equal strings, and they swing in perfect step. A heavier bob feels more pull, but it also has more inertia, and the two cancel."):
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(lm))
            self.play(s.animate.set_value(TAU * 2), run_time=7, rate_func=linear)
        self.add(b1, b2)
        with self.say("Second: the period grows as the square root of the length. Make the string four times longer, and the period only doubles. Count with me. The short pendulum swings twice, for every single swing of the long one."):
            self.play(FadeIn(b1), FadeIn(b2), FadeIn(lL))
            self.play(s.animate.set_value(TAU * 4), run_time=8, rate_func=linear)
        with self.say("Third, the period is inversely proportional to root g, so a pendulum runs slower on the Moon. And fourth, for small swings, the period does not depend on the amplitude. That is isochronism, the property that made pendulum clocks possible. A seconds pendulum has a period of exactly two seconds, one second each way."):
            self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in laws], lag_ratio=0.3), run_time=2.0)
            self.play(s.animate.set_value(TAU * 6), run_time=8, rate_func=linear)
        self.play(FadeOut(VGroup(title, lm, lL, laws)), *[FadeOut(m) for m in (a1, a2, b1, b2)])
        self.remove(a1, a2, b1, b2)

    def example_24(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("Find the length of a seconds pendulum where g = 9.8 m/s². If this pendulum clock is taken to a place where g = 9.78 m/s², how much time does it lose in a day?", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"L = \frac{gT^{2}}{4\pi^{2}} = \frac{9.8 \times 2^{2}}{4\pi^{2}} = 0.993\ \text{m}", size=36),
            M(r"T' = 2\pi\sqrt{\frac{0.993}{9.78}} = 2.002\ \text{s}", size=36),
            M(r"\text{swings in a day} = \frac{86400}{2.002} = 43156", size=36),
            M(r"\text{clock shows } 43156 \times 2 = 86312\ \text{s}", size=36),
            M(r"\text{loss} = 86400 - 86312 = 88\ \text{s} \approx 1\ \text{min}\ 28\ \text{s}", size=38, color=th.CORAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(prob, DOWN, buff=0.35).align_to(prob, LEFT).shift(RIGHT * 0.2)
        clock_c = np.array([4.8, -1.4, 0])
        face = Circle(radius=1.1, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.MUTED, stroke_width=3).move_to(clock_c)
        marks = VGroup(*[Line(clock_c + 0.95 * np.array([np.cos(a), np.sin(a), 0]), clock_c + 1.05 * np.array([np.cos(a), np.sin(a), 0]), color=th.MUTED, stroke_width=2) for a in np.arange(0, TAU, TAU / 12)])
        hand = ValueTracker(PI / 2)
        hd = always_redraw(lambda: Line(clock_c, clock_c + 0.85 * np.array([np.cos(hand.get_value()), np.sin(hand.get_value()), 0]), color=th.CORAL, stroke_width=4))
        with self.say("Here is a classic exam problem about a pendulum clock. Find the length of a seconds pendulum where g is nine point eight. Then the clock is carried to a place where g is nine point seven eight. How much time does it lose in one day?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("A seconds pendulum has T equals two seconds. Rearranging, L equals g T squared over four pi squared, which is zero point nine nine three metres. Almost exactly one metre."):
            self.play(Write(steps[0]))
        with self.say("At the new place, g is smaller, so the same pendulum swings more slowly. Its period becomes two point zero zero two seconds."):
            self.play(Write(steps[1]))
        with self.say("But the clock still counts every swing as two seconds. In one real day, eighty six thousand four hundred seconds, it makes only forty three thousand one hundred fifty six swings."):
            self.play(Write(steps[2]))
            self.play(FadeIn(face), FadeIn(marks))
            self.add(hd)
            self.play(hand.animate.set_value(PI / 2 - TAU * 1.5), run_time=2.0, rate_func=linear)
        with self.say("So it shows eighty six thousand three hundred twelve seconds. It has lost eighty eight seconds, about one minute twenty eight seconds every day. A tiny change in g, and a very noticeable error."):
            self.play(Write(steps[3]))
            self.play(Write(steps[4]))
            self.play(Circumscribe(steps[4], color=th.CORAL))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps, face, marks)), FadeOut(hd))
        self.remove(hd)
        self.quiz("The period of a simple pendulum does NOT depend on…",
                  ["its length", "the value of g", "the mass of the bob", "any of these"], 2,
                  "Pause and think. The period of a simple pendulum does not depend on which of these?",
                  "C, the mass of the bob. The restoring force m g sine theta and the inertia m both carry the mass, so it cancels. D is tempting if you remember that the pendulum ignores mass and amplitude, but length and g are right there in the formula: two pi root L over g.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        self.damped()
        self.three_cases()
        self.resonance()
        self.resolve_city()
        self.example_25()

    def damped(self):
        ax = Axes(x_range=[0, 12, 2], y_range=[-1.2, 1.2, 1], x_length=8.6, y_length=3.6,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([1.8, -0.6, 0])
        g = 0.22
        t = ValueTracker(0.01)
        f = lambda u: np.exp(-g * u) * np.cos(2.2 * u)
        curve = always_redraw(lambda: ax.plot(f, x_range=[0, max(0.06, t.get_value()), 0.02], color=C_X, stroke_width=4))
        top = 2.9
        mx = -5.2
        rig = always_redraw(lambda: VGroup(hatch([mx, top, 0], width=1.2),
                                           spring([mx, top, 0], [mx, top - 2.2 - 0.9 * f(t.get_value()), 0], coils=7),
                                           block([mx, top - 2.2 - 0.9 * f(t.get_value()) - 0.3, 0], w=0.8, h=0.6)))
        tl = T("time", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        with self.say("So far our oscillators run for ever. Real ones do not. Air resistance and friction take a little energy every cycle, and the swings die away. This is damped oscillation."):
            self.add(rig)
            self.play(FadeIn(rig), Create(ax), FadeIn(tl))
            self.add(curve)
            self.play(t.animate.set_value(7), run_time=7, rate_func=linear)
        eqs = VGroup(
            M(r"F_d = -bv", size=40),
            M(r"m\frac{d^{2}x}{dt^{2}} + b\frac{dx}{dt} + kx = 0", size=38),
            M(r"x = A_0 e^{-bt/2m}\sin(\omega' t + \phi)", size=40, color=C_X),
            M(r"\omega' = \sqrt{\frac{k}{m} - \frac{b^{2}}{4m^{2}}} < \omega_0", size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 2.15, 0])
        if eqs.height > 2.6:
            eqs.scale_to_fit_height(2.6).move_to([2.9, 2.1, 0])
        self.play(ax.animate.shift(DOWN * 0.7).scale(0.92), run_time=0.6)
        env1 = DashedVMobject(ax.plot(lambda u: np.exp(-g * u), x_range=[0, 12], color=th.AMBER, stroke_width=2.5), num_dashes=40)
        env2 = DashedVMobject(ax.plot(lambda u: -np.exp(-g * u), x_range=[0, 12], color=th.AMBER, stroke_width=2.5), num_dashes=40)
        with self.say("For slow motion, the resistance is proportional to the velocity: F equals minus b v. Add it to Newton's law, and the solution is a sine wave inside a shrinking exponential. The amplitude decays as A nought e to the minus b t over two m."):
            self.play(Write(eqs[0]), Write(eqs[1]))
            self.play(Write(eqs[2]))
            self.play(Create(env1), Create(env2))
            self.play(t.animate.set_value(12), run_time=4, rate_func=linear)
        with self.say("Damping also slows the oscillation slightly: the new angular frequency omega dash is a little less than the natural one. And because energy goes as amplitude squared, the energy decays twice as fast as the amplitude."):
            self.play(Write(eqs[3]))
        self.play(FadeOut(VGroup(ax, tl, eqs, env1, env2)), FadeOut(curve), FadeOut(rig))
        self.remove(curve, rig)

    def three_cases(self):
        title = T("How much damping?", size=38, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Axes(x_range=[0, 10, 2], y_range=[-0.8, 1.1, 0.5], x_length=9.0, y_length=4.0,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([-1.9, -0.5, 0])
        w = 1.6

        def under(u, z=0.12):
            wd = w * np.sqrt(1 - z * z)
            return np.exp(-z * w * u) * (np.cos(wd * u) + z * w / wd * np.sin(wd * u))

        def crit(u):
            return (1 + w * u) * np.exp(-w * u)

        def over(u, z=3.0):
            r1 = w * (-z + np.sqrt(z * z - 1))
            r2 = w * (-z - np.sqrt(z * z - 1))
            return (r2 * np.exp(r1 * u) - r1 * np.exp(r2 * u)) / (r2 - r1)
        cs = [(under, th.SKY, "under-damped", "pendulum in air"), (crit, th.MINT, "critically damped", "dead-beat galvanometer"),
              (over, th.AMBER, "over-damped", "pendulum in thick oil")]
        legend = VGroup()
        curves = VGroup()
        for f, c, n, ex in cs:
            curves.add(ax.plot(f, x_range=[0, 10, 0.03], color=c, stroke_width=4))
            legend.add(VGroup(Line(ORIGIN, RIGHT * 0.5, color=c, stroke_width=5), VGroup(T(n, size=24, color=c, weight="SEMIBOLD"), T(ex, size=20, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)).arrange(RIGHT, buff=0.2))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if legend.width > 3.6:
            legend.scale_to_fit_width(3.6)
        legend.move_to([4.7, -0.3, 0])
        says = ["With light damping, the body still oscillates, but each swing is smaller. This is under-damped motion, like a pendulum in air.",
                "Increase the damping to a special value, where b squared equals four m k, and the body returns to rest in the shortest possible time, without overshooting at all. That is critical damping. Galvanometers and car shock absorbers are designed this way.",
                "Add even more damping, and the body creeps back slowly, without oscillating. That is over-damped, like a pendulum moving through thick oil."]
        self.play(FadeIn(title), Create(ax))
        for cv, lg, sy in zip(curves, legend, says):
            with self.say(sy):
                self.play(Create(cv), FadeIn(lg, shift=LEFT * 0.2), run_time=2.0)
        self.play(FadeOut(VGroup(title, ax, curves, legend)))

    def resonance(self):
        title = T("Forced oscillation and resonance", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Axes(x_range=[0, 2.1, 0.5], y_range=[0, 5.5, 1], x_length=6.6, y_length=4.2,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([2.6, -0.6, 0])

        def amp(wd, b):
            return 1 / np.sqrt((1 - wd ** 2) ** 2 + (b * wd) ** 2)
        bs = [(0.2, th.CORAL, "light"), (0.45, th.AMBER, "medium"), (1.0, th.MINT, "heavy")]
        curves = VGroup(*[ax.plot(lambda u, b=b: amp(u, b), x_range=[0.02, 2.05, 0.01], color=c, stroke_width=4) for b, c, _ in bs])
        tags = VGroup(*[T(n + " damping", size=20, color=c).next_to(ax.c2p(1.0, amp(1.0, b)), RIGHT, buff=0.2) for b, c, n in bs])
        tags[1].shift(RIGHT * 0.15)
        xl = VGroup(M(r"\omega_d", size=30, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT),
                    M(r"\omega_0", size=30, color=th.INK).next_to(ax.c2p(1, 0), DOWN, buff=0.15))
        yl = T("amplitude", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        wd = ValueTracker(0.3)
        ph = ValueTracker(0)
        top = 2.3
        mx = -4.2

        def rig():
            u = wd.get_value()
            A = amp(u, 0.2)
            drv = 0.18 * np.sin(ph.get_value())
            resp = 0.18 * A * np.sin(ph.get_value() - np.arctan2(0.2 * u, 1 - u * u))
            yb = top - 2.2 - resp
            return VGroup(Line([mx - 0.6, top + drv, 0], [mx + 0.6, top + drv, 0], color=th.AMBER, stroke_width=6),
                          spring([mx, top + drv, 0], [mx, yb, 0], coils=7), block([mx, yb - 0.3, 0], w=0.8, h=0.6))

        def ticker(m, dt):
            ph.increment_value(dt * 5.0 * wd.get_value())
        clock = Mobject()
        clock.add_updater(ticker)
        r = always_redraw(rig)
        hand = T("driver", size=20, color=th.AMBER).move_to([mx + 1.2, top + 0.35, 0])
        dot = always_redraw(lambda: Dot(ax.c2p(wd.get_value(), min(5.4, amp(wd.get_value(), 0.2))), radius=0.1, color=WHITE))
        readout = always_redraw(lambda: VGroup(M(r"\omega_d/\omega_0 =", size=30), DecimalNumber(wd.get_value(), num_decimal_places=2, font_size=30, color=th.AMBER)).arrange(RIGHT, buff=0.15).move_to([5.0, 2.1, 0]))
        with self.say("Now, instead of leaving the oscillator alone, we shake its support with a periodic force at a driving frequency, omega d. At first it jerks around, but soon it settles into a steady oscillation at the driver's frequency, not its own. This is a forced oscillation."):
            self.play(FadeIn(title))
            self.add(clock, r)
            self.play(FadeIn(r), FadeIn(hand))
            self.wait(4)
        with self.say("Let us slowly turn up the driving frequency, and watch the amplitude. Low frequency, small response."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.add(dot, readout)
            self.play(Create(curves[0]), run_time=1.5)
        with self.say("Closer to the natural frequency, the amplitude climbs. And when the driving frequency equals the natural frequency, the amplitude shoots up to a maximum. This is resonance.") as v:
            self.play(wd.animate.set_value(1.0), run_time=v.dur - 0.5, rate_func=smooth)
        self.sfx("impact", gain=-10)
        defn = self.callout("key", "Resonance: the amplitude of a forced oscillation becomes maximum when the driving frequency equals the natural frequency.", width=5.4, size=21)
        defn.move_to([-3.85, -2.45, 0])
        with self.say("At resonance, every push arrives exactly in step with the motion, like pushing a child on a swing at just the right moment. So energy keeps flowing in, and only damping limits how big the swings become."):
            self.play(FadeIn(defn, shift=UP * 0.2))
        with self.say("Past the natural frequency, the oscillator cannot keep up, and the amplitude falls again."):
            self.play(wd.animate.set_value(1.8), run_time=4, rate_func=smooth)
        with self.say("And the damping decides the shape. Light damping gives a tall, sharp peak. Heavy damping gives a low, broad one."):
            self.play(Create(curves[1]), Create(curves[2]), FadeIn(tags), run_time=2)
        self.play(FadeOut(VGroup(title, ax, curves, tags, xl, yl, hand, defn)), FadeOut(r), FadeOut(dot), FadeOut(readout))
        self.remove(r, dot, readout, clock)
        uses = [("Radio tuning", "The circuit resonates with one station's frequency and ignores the rest.", th.MINT),
                ("Sitar strings", "Sympathetic strings ring by themselves when a played note matches them.", th.MINT),
                ("Marching soldiers", "They break step on a bridge, so their rhythm cannot match its natural frequency.", th.CORAL),
                ("Tacoma Narrows, 1940", "Wind drove the bridge into huge oscillations until it tore apart.", th.CORAL)]
        cards = VGroup()
        for h, b, c in uses:
            box = self.panel(6.0, 1.9, color=c)
            g = VGroup(T(h, size=26, color=c, weight="BOLD"), para(b, width=5.4, size=21, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            g.move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.say("Resonance is useful and dangerous in equal measure. A radio tunes in one station by resonating with it. The sympathetic strings of a sitar ring all by themselves. But soldiers break step when crossing a bridge, and in nineteen forty, wind drove the Tacoma Narrows bridge into resonance until it tore itself apart.") as v:
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.7)
        self.play(FadeOut(cards))

    def resolve_city(self):
        t = ValueTracker(0)
        drive = 3.3 / 2.9
        city, xs, hs, ws = self.buildings(t, drive, amp_scale=1.6, ramp=4.0)
        lab = VGroup(*[M(r"f_0", size=24, color=th.MUTED).move_to([x, -2.55 + h + 0.35, 0]) for x, h in zip(xs, hs)])
        q = T("Resonance.", size=44, color=th.CORAL, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        nb = self.neby("think", height=1.4).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        with self.say("Now we can answer our opening question. Every building has its own natural frequency. Tall buildings sway slowly. Short buildings sway quickly.") as v:
            self.add(city)
            self.play(FadeIn(city), FadeIn(lab))
            self.play(t.animate.set_value(max(1, v.dur - 1)), run_time=max(1, v.dur - 1), rate_func=linear)
        self.add(nb)
        with self.say("On that day in twenty fifteen, the ground shook at a particular frequency. The buildings whose natural frequency matched the shaking were driven at resonance. Their swings grew and grew. That one word is the answer: resonance. It is why engineers now tune buildings, and add damping, to keep them away from it.") as v:
            self.play(FadeIn(q, scale=0.8), FadeIn(nb, scale=0.5), FadeOut(lab))
            self.play(t.animate.set_value(t.get_value() + v.dur - 1), run_time=max(1, v.dur - 1), rate_func=linear)
        nb.set_state("success", once=True)
        self.wait(1.0)
        self.play(FadeOut(q), FadeOut(city), FadeOut(nb))
        self.remove(city, nb)

    def example_25(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A damped oscillator has mass 0.2 kg and damping constant b = 0.04 kg/s. After what time does (a) the amplitude, (b) the energy fall to 1/e of its initial value?", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"A = A_0 e^{-bt/2m} = \frac{A_0}{e} \;\Rightarrow\; \frac{bt}{2m} = 1", size=40),
            M(r"t = \frac{2m}{b} = \frac{2 \times 0.2}{0.04} = 10\ \text{s}", size=42, color=C_X),
            M(r"E \propto A^{2} \;\Rightarrow\; E = E_0 e^{-bt/m}", size=40),
            M(r"t = \frac{m}{b} = \frac{0.2}{0.04} = 5\ \text{s}", size=42, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.55).align_to(prob, LEFT)
        with self.say("One last example. A damped oscillator has mass zero point two kilograms and damping constant zero point zero four kilograms per second. When does the amplitude fall to one over e of its starting value? And when does the energy?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("The amplitude is A nought e to the minus b t over two m. It becomes A nought over e when b t over two m equals one. So t equals two m over b: zero point four over zero point zero four, ten seconds."):
            self.play(Write(steps[0]))
            self.play(Write(steps[1]))
        with self.say("Energy goes as amplitude squared, so it decays as e to the minus b t over m, twice as fast. It falls to one over e at m over b, which is five seconds. Half the time."):
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("At resonance, the amplitude of a forced oscillation is…",
                  ["zero", "minimum", "maximum, limited only by damping", "independent of damping"], 2,
                  "Final check. At resonance, the amplitude of a forced oscillation is what? Pause and think.",
                  "C. At resonance the driver feeds energy in step with the motion, so the amplitude is maximum, and the only thing holding it back is damping. That is exactly why D is wrong: less damping means a taller peak, so the amplitude at resonance depends very much on damping.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"\text{SHM: } a = -\omega^{2}x,\quad x = A\sin(\omega t + \phi)", size=34),
            M(r"v = \omega\sqrt{A^{2}-x^{2}},\ \ v_{\max} = A\omega,\ \ a_{\max} = \omega^{2}A", size=34),
            M(r"T = 2\pi/\omega = 2\pi\sqrt{m/k}", size=34),
            M(r"U = \tfrac12 kx^{2},\ \ K = \tfrac12 k(A^{2}-x^{2}),\ \ E = \tfrac12 kA^{2}", size=34),
            M(r"\text{vertical spring: } mg = ke,\ \ T = 2\pi\sqrt{e/g}", size=34),
            M(r"\text{pendulum: } T = 2\pi\sqrt{L/g}\ (\text{small }\theta);\ \ \text{angular: } T = 2\pi\sqrt{I/c}", size=34),
            M(r"\text{damped: } A = A_0e^{-bt/2m};\ \ \text{resonance at } \omega_d = \omega_0", size=34),
        ], "Let us recap. Simple harmonic motion means acceleration proportional to displacement and directed towards the mean: a equals minus omega squared x. Speed is greatest in the middle, acceleration at the ends. The period is two pi over omega. Energy swaps between kinetic and potential, with a constant total of half k A squared. On a vertical spring, gravity just shifts the mean. A pendulum's period is two pi root L over g for small swings. Damping makes the amplitude decay exponentially, and resonance happens when the driver matches the natural frequency.")
        self.outro("That is periodic motion. Next time, we dive into fluids: pressure, buoyancy, surface tension and flow. Keep practising, and see you in the next lesson on NEBians.")
