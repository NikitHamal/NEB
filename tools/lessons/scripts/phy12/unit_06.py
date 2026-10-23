import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import arrow, clock, curve, example, neby_in, neby_out, nothing, readout, sdash  # noqa: E402

C_A, C_L, C_V, C_P, C_1, C_2 = th.AMBER, th.MINT, th.SKY, th.CORAL, th.SKY, th.PINK
WATER = "#1E5A8A"


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 6
    TITLE = "Wave Motion"
    SUBTITLE = "Travelling and standing waves"
    SECTIONS = ["Progressive waves", "Describing a wave", "The equation of a wave", "Phase and particle velocity",
                "Stationary waves", "Nodes and antinodes"]
    NEXT = "Unit 7 · Mechanical Waves"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        y0, x0 = -0.6, -5.2
        A, lam, v = 0.45, 2.2, 1.6
        k, w = TAU / lam, TAU * v / lam
        t = ValueTracker(-1.0)

        def y(x):
            tt = t.get_value()
            d = x - x0
            if tt <= 0 or d > v * tt or d < 0:
                return y0
            return y0 + A * np.exp(-0.06 * d) * np.sin(w * tt - k * d) * min(1, (v * tt - d) * 2)

        def surf():
            xs = np.linspace(-6.8, 6.8, 220)
            pts = [np.array([x, y(abs(x - x0) + x0) if x < x0 else y(x), 0]) for x in xs]
            water = Polygon(*pts, [6.8, -3.4, 0], [-6.8, -3.4, 0], stroke_width=0, fill_color=WATER, fill_opacity=0.75)
            line = VMobject(stroke_color=th.SKY, stroke_width=4).set_points_as_corners(pts)
            return VGroup(water, line)
        lake = always_redraw(surf)
        LX = 2.4
        leaf = always_redraw(lambda: Ellipse(width=0.7, height=0.2, fill_color=th.LIME, fill_opacity=1, stroke_width=0).move_to([LX, y(LX) + 0.08, 0]))
        stone = Dot([x0, 3.0, 0], radius=0.16, color=th.MUTED)
        title = T("Phewa Lake, Pokhara", size=26, color=th.MUTED).to_edge(UP, buff=0.6)
        self.add(lake)
        with self.say("A still morning on Phewa Lake in Pokhara. A leaf floats quietly on the water. Now somebody drops a stone in."):
            self.play(FadeIn(lake), FadeIn(title))
            self.add(leaf)
            self.play(FadeIn(leaf))
            self.play(FadeIn(stone))
            self.play(stone.animate.move_to([x0, y0, 0]), run_time=0.8, rate_func=rate_functions.ease_in_quad)
            self.sfx("thud", gain=-8)
            self.remove(stone)
        guide = DashedLine([LX, 1.2, 0], [LX, -2.2, 0], color=th.FAINT, stroke_width=2)
        with self.say("Ripples race outwards across the lake. Watch the leaf as they pass under it."):
            self.play(t.animate.set_value(6.0), run_time=6.0, rate_func=linear)
        q = T("The ripple travels. Does the leaf?", size=32, color=th.AMBER, weight="BOLD", display=True).to_edge(UP, buff=1.2)
        with self.say("The ripple has travelled several metres. But the leaf has not gone anywhere. It only bobs up and down, on the same spot."):
            self.play(FadeIn(guide), FadeIn(q))
            self.play(t.animate.set_value(10.0), run_time=4.0, rate_func=linear)
        nb = neby_in(self, "surprised", corner=UR)
        with self.say("So what exactly is moving? Not the water. Something else is travelling across the lake, carrying energy with it. That something is a wave, and in this lesson we will learn to describe it exactly, with one equation."):
            self.play(t.animate.set_value(15.0), run_time=5.0, rate_func=linear)
        self.play(FadeOut(VGroup(title, guide, q)), FadeOut(lake), FadeOut(leaf))
        self.remove(lake, leaf)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 6: Wave Motion. This short unit gives you the language and the equation of a wave. Sound, strings, pipes, and even light, in the units ahead, are all built on it."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. What a progressive wave is, the five quantities that describe it, the equation of a travelling wave, phase and particle velocity, and then what happens when two waves meet head on: stationary waves, with their nodes and antinodes.")

    # ------------------------------------------------------------------ part 1
    def beads(self, t, y0=0.4, n=29, A=0.7, lam=4.0, v=2.0, x0=-6.2, x1=6.2, front=True, color=th.SKY):
        k, w = TAU / lam, TAU * v / lam
        xs = np.linspace(x0, x1, n)

        def dy(x):
            d = x - x0
            tt = t.get_value()
            if front and d > v * tt:
                return 0.0
            return A * np.sin(w * tt - k * d)
        g = VGroup(*[Dot([x, y0, 0], radius=0.09, color=color) for x in xs])

        def upd(m):
            for d, x in zip(m, xs):
                d.move_to([x, y0 + dy(x), 0])
        g.add_updater(upd)
        line = always_redraw(lambda: curve(lambda x: y0 + dy(x), x0, x1, n=180, color=th.FAINT, width=2))
        return g, line, dy

    def p1(self):
        self.section(0)
        t = ValueTracker(0)
        g, line, dy = self.beads(t)
        hi = 14
        g[hi].set_color(C_P)
        hand = Arrow([-6.6, -0.6, 0], [-6.6, 1.4, 0], buff=0, color=th.MUTED, stroke_width=4)
        with self.say("Here is a row of beads, joined to each other along a stretched string. Shake the first one up and down, and watch."):
            self.add(line, g)
            self.play(FadeIn(g), FadeIn(line), FadeIn(hand))
            self.play(t.animate.set_value(3.5), run_time=3.5, rate_func=linear)
        guide = DashedLine([g[hi].get_x(), 1.5, 0], [g[hi].get_x(), -0.7, 0], color=C_P, stroke_width=2)
        en = Arrow([-4.0, 2.2, 0], [4.0, 2.2, 0], buff=0, color=C_A, stroke_width=6)
        enl = T("energy travels this way", size=26, color=C_A).next_to(en, UP, buff=0.12)
        with self.say("The shape moves along the row from left to right. But follow the red bead. It never moves along. It only goes up and down about its own place, exactly like the leaf."):
            self.play(FadeIn(guide))
            self.play(t.animate.set_value(8.0), run_time=4.5, rate_func=linear)
        defn = self.callout("key", "A progressive wave is a disturbance that travels through a medium in a definite direction, carrying energy and momentum, without any net transport of the medium itself.", width=11, size=26)
        defn.to_edge(DOWN, buff=0.55)
        with self.say("That is a progressive, or travelling, wave. A disturbance that travels through a medium in a definite direction, transferring energy and momentum from point to point, without any net transport of the medium itself."):
            self.play(GrowArrow(en), FadeIn(enl))
            self.play(FadeIn(defn, shift=UP * 0.2), t.animate.set_value(12.0), run_time=4, rate_func=linear)
        need = VGroup(T("elasticity: a restoring force pulls each bead back", size=24, color=th.BODY),
                      T("inertia: the moving bead overshoots and keeps going", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(defn)
        with self.say("A mechanical wave needs a medium with two properties. Elasticity, to pull each displaced particle back. And inertia, so that the particle overshoots and passes the motion on. Light and radio waves are different: they need no medium at all."):
            self.play(FadeOut(defn), FadeIn(need), t.animate.set_value(17.0), run_time=5, rate_func=linear)
        self.play(FadeOut(VGroup(guide, en, enl, need, hand)), FadeOut(g), FadeOut(line))
        g.clear_updaters()
        self.remove(g, line)
        self.two_kinds()

    def two_kinds(self):
        t = clock(self, 1.0)
        lam, v = 4.0, 2.0
        k, w = TAU / lam, TAU * v / lam
        g, line, dy = self.beads(t, y0=1.6, A=0.55, front=False, n=31)
        tl = T("Transverse: particles vibrate across the direction of travel", size=24, color=C_V).move_to([0, 2.75, 0])
        xs = np.linspace(-6.2, 6.2, 41)
        s = 0.32
        layers = VGroup(*[Line([x, -2.3, 0], [x, -0.7, 0], color=C_L, stroke_width=3) for x in xs])

        def lupd(m):
            for ln, x in zip(m, xs):
                ln.set_x(x + s * np.sin(w * t.get_value() - k * (x + 6.2)))
        layers.add_updater(lupd)

        def cpos(n):
            return ((w * t.get_value() / k) % lam) - 6.2 + n * lam
        cl = always_redraw(lambda: VGroup(*[T("C", size=24, color=th.CORAL, weight="BOLD").move_to([cpos(n), -2.6, 0]) for n in range(4) if -6.2 < cpos(n) < 6.2]))
        rl = always_redraw(lambda: VGroup(*[T("R", size=24, color=th.MUTED, weight="BOLD").move_to([cpos(n) + lam / 2, -2.6, 0]) for n in range(-1, 4) if -6.2 < cpos(n) + lam / 2 < 6.2]))
        ll = T("Longitudinal: particles vibrate along the direction of travel", size=24, color=C_L).move_to([0, -0.3, 0])
        with self.say("Waves come in two kinds, sorted by how the particles move. In a transverse wave, they vibrate at right angles to the direction the wave travels, forming crests and troughs. A wave on a string, a ripple on water, and light are all transverse."):
            self.add(line, g)
            self.play(FadeIn(g), FadeIn(line), FadeIn(tl))
            self.wait(2)
        with self.say("In a longitudinal wave, the particles vibrate back and forth along the direction of travel. They crowd together in compressions, marked C, and spread apart in rarefactions, marked R. Sound in air is longitudinal."):
            self.add(layers, cl, rl)
            self.play(FadeIn(layers), FadeIn(ll), FadeIn(cl), FadeIn(rl))
            self.wait(3)
        self.play(FadeOut(VGroup(tl, ll)), FadeOut(g), FadeOut(line), FadeOut(layers), FadeOut(cl), FadeOut(rl))
        g.clear_updaters()
        layers.clear_updaters()
        self.remove(g, line, layers, cl, rl, t)
        rows = [("", "Transverse", "Longitudinal"), ("vibration", "across the travel", "along the travel"), ("form", "crests and troughs", "compressions, rarefactions"),
                ("travels in", "solids, liquid surfaces", "solids, liquids, gases"), ("polarised?", "yes", "no"), ("examples", "string, ripples, light", "sound, pushed spring")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c, size=26 if i else 28, color=[th.MUTED, C_V, C_L][j] if i == 0 or j == 0 else th.BODY, weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.4, -0.6, 3.6]):
                row[j].move_to([x, 2.2 - i * 0.78, 0])
            grid.add(row)
        with self.say("Here are the differences side by side. Notice especially that only transverse waves can be polarised, and that only longitudinal waves can travel through a gas. Air has no stiffness against sideways shearing, so it cannot carry a transverse wave.") as v_:
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(grid))
        self.quiz("Sound waves travelling through air are",
                  ["transverse", "longitudinal", "electromagnetic", "always stationary"], 1,
                  "Quick check. Sound waves travelling through air are which kind? Pause and think.",
                  "B, longitudinal. Air has no stiffness against sideways shearing, so it cannot pass on a transverse vibration. The air molecules can only push on their neighbours along the direction of travel, making compressions and rarefactions.")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        lam, v, A = 4.0, 2.0, 0.9
        t = clock(self, 0.0)
        k, w = TAU / lam, TAU * v / lam
        y0 = 0.3
        wave = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(w * t.get_value() - k * (x + 6)), -6.3, 6.3, color=C_V, width=5))
        axis = DashedLine([-6.3, y0, 0], [6.3, y0, 0], color=th.FAINT, stroke_width=2)
        xc = -6 + lam / 4 * 3
        cr = [-6 + 0.75 * lam + n * lam for n in range(3)]
        ab = BraceBetweenPoints([cr[1] + 0.25, y0, 0], [cr[1] + 0.25, y0 - A, 0], RIGHT, color=C_A)
        abl = M("a", size=38, color=C_A).next_to(ab, RIGHT, buff=0.1)
        lb = BraceBetweenPoints([cr[0], y0 + A + 0.1, 0], [cr[1], y0 + A + 0.1, 0], UP, color=C_L)
        lbl = M(r"\lambda", size=40, color=C_L).next_to(lb, UP, buff=0.1)
        with self.say("Five quantities describe any progressive wave. Freeze the wave for a moment. The amplitude, a, is the greatest displacement of a particle from its mean position."):
            self.add(wave)
            self.play(FadeIn(wave), FadeIn(axis))
            self.play(GrowFromCenter(ab), FadeIn(abl))
        with self.say("The wavelength, lambda, is the distance between two successive particles in the same phase. Crest to crest, trough to trough, or compression to compression."):
            self.play(GrowFromCenter(lb), FadeIn(lbl))
        self.play(FadeOut(VGroup(ab, abl, lb, lbl)))
        Px = 0.0
        pd = always_redraw(lambda: Dot([Px, y0 + A * np.sin(w * t.get_value() - k * (Px + 6)), 0], radius=0.13, color=C_P))
        gx = Axes(x_range=[0, 4.2, 1], y_range=[-1, 1, 1], x_length=5.2, y_length=1.3, tips=False, axis_config={"color": th.FAINT, "include_ticks": False}).move_to([2.6, -2.05, 0])
        tg = always_redraw(lambda: gx.plot(lambda s: np.sin(w * s - k * (Px + 6)), x_range=[0, max(0.01, min(4.0, t.get_value()))], color=C_P, stroke_width=4))
        gl = T("one particle: y against time", size=20, color=C_P).next_to(gx, UP, buff=0.05)
        Tb = BraceBetweenPoints(gx.c2p(0, -1.05), gx.c2p(2, -1.05), DOWN, color=th.INK)
        Tl = M("T", size=32).next_to(Tb, DOWN, buff=0.05)
        eqs = VGroup(M(r"f = \frac{1}{T}", size=40), T("vibrations per second: hertz", size=22, color=th.MUTED)).arrange(DOWN, buff=0.1).move_to([-4.0, -2.3, 0])
        with self.say("Now let it run, and follow one particle. The period, T, is the time it takes to make one complete vibration. The frequency, f, is the number of vibrations per second, one over T, measured in hertz."):
            self.add(pd, tg)
            self.play(FadeIn(pd), Create(gx), FadeIn(gl))
            t.rate = 1.0
            self.wait(2.2)
            self.play(GrowFromCenter(Tb), FadeIn(Tl), FadeIn(eqs))
            self.wait(1.0)
        t.rate = 0.0
        self.play(FadeOut(VGroup(gx, gl, Tb, Tl, eqs)), FadeOut(tg), FadeOut(pd))
        self.remove(tg, pd)
        c0 = t.get_value()
        def crest_x():
            return -6 + (0.75 * lam + v * (t.get_value() - c0)) + lam * 0.0
        flag = always_redraw(lambda: VGroup(Triangle(fill_color=C_A, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI).move_to([crest_x() + lam, y0 + A + 0.3, 0])))
        startl = DashedLine([-6 + 0.75 * lam + lam, y0 + A + 0.6, 0], [-6 + 0.75 * lam + lam, y0 - A - 0.2, 0], color=C_A, stroke_width=2)
        clk = readout("t =", lambda: (t.get_value() - c0), "s", decimals=2, size=28).move_to([4.6, 2.5, 0])
        with self.say("Here is the key link. Put a flag on one crest, and start a stopwatch. In exactly one period, the wave advances by exactly one wavelength."):
            self.add(flag)
            self.play(FadeIn(flag), FadeIn(startl), FadeIn(clk))
            self.play(t.animate.set_value(c0 + 2.0), run_time=3.0, rate_func=linear)
        endl = DashedLine([-6 + 0.75 * lam + 2 * lam, y0 + A + 0.6, 0], [-6 + 0.75 * lam + 2 * lam, y0 - A - 0.2, 0], color=C_A, stroke_width=2)
        lb2 = BraceBetweenPoints(startl.get_bottom(), endl.get_bottom(), DOWN, color=C_L)
        eq = M(r"v = \frac{\lambda}{T} = f\lambda", size=64, color=th.INK).move_to([0, -2.4, 0])
        with self.say("Speed is distance over time, so v equals lambda over T, which is f lambda. This wave equation holds for every wave there is, mechanical or electromagnetic."):
            self.play(Create(endl), GrowFromCenter(lb2))
            self.sfx("impact", gain=-12)
            self.play(Write(eq))
        self.play(FadeOut(VGroup(flag, startl, endl, lb2, clk, eq, wave, axis)))
        self.remove(flag, wave, t)
        self.freq_slider()

    def freq_slider(self):
        v, A, y0 = 2.0, 0.8, 0.6
        f = ValueTracker(0.5)
        ph = ValueTracker(0)
        ph.add_updater(lambda m, dt: m.increment_value(TAU * f.get_value() * dt))
        self.add(ph)
        wave = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(ph.get_value() - TAU * f.get_value() / v * (x + 6)), -6.3, 6.3, n=260, color=C_V, width=5))
        src = always_redraw(lambda: Dot([-6.3, y0 + A * np.sin(ph.get_value()), 0], radius=0.14, color=C_P))
        ro = VGroup(readout("f =", lambda: f.get_value(), "Hz", decimals=2, size=28, color=C_P),
                    readout("λ =", lambda: v / f.get_value(), "m", decimals=2, size=28, color=C_L),
                    readout("v = fλ =", lambda: v, "m/s", decimals=2, size=28, color=th.INK)).arrange(RIGHT, buff=0.7).move_to([0, -1.9, 0])
        with self.say("In a given medium, the speed is fixed by the medium itself: its elasticity and its density. So what happens if the source vibrates faster?"):
            self.add(wave, src)
            self.play(FadeIn(wave), FadeIn(src), FadeIn(ro))
            self.wait(2)
        with self.say("Double the frequency, and the wavelength halves. Triple it, and the wavelength is a third. The product, f lambda, the speed, never changes. Changing the frequency of the source changes the wavelength, not the speed."):
            self.play(f.animate.set_value(1.0), run_time=2.5)
            self.wait(1)
            self.play(f.animate.set_value(1.5), run_time=2.0)
            self.wait(1)
            self.play(f.animate.set_value(0.5), run_time=2.0)
        notes = VGroup(T("• every particle has the same amplitude and frequency", size=24, color=th.BODY),
                       T("• each particle starts a little later than the one before it", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.55)
        with self.say("Two more facts to remember. In a progressive wave, every particle vibrates with the same amplitude and the same frequency. But each one starts its vibration slightly later than the one before it. The phase lags steadily along the direction of travel."):
            self.play(FadeIn(notes, shift=UP * 0.2))
            self.wait(2)
        self.play(FadeOut(VGroup(ro, notes)), FadeOut(wave), FadeOut(src))
        self.remove(wave, src, ph)

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        t = clock(self, 0.0)
        lam, v, A, y0 = 4.0, 2.0, 0.8, 0.9
        k, w = TAU / lam, TAU * v / lam
        X = 3.0

        def yy(x):
            d = x + 6
            if d > v * t.get_value():
                return 0.0
            return A * np.sin(w * t.get_value() - k * d)
        wave = always_redraw(lambda: curve(lambda x: y0 + yy(x), -6.3, 6.3, n=220, color=C_V, width=4))
        O = always_redraw(lambda: Dot([-6.0, y0 + yy(-6.0), 0], radius=0.13, color=C_A))
        P = always_redraw(lambda: Dot([-6.0 + X, y0 + yy(-6.0 + X), 0], radius=0.13, color=C_P))
        Ol = M("O", size=30, color=C_A).move_to([-6.0, y0 - 1.25, 0])
        Pl = M("P", size=30, color=C_P).move_to([-6.0 + X, y0 - 1.25, 0])
        xb = BraceBetweenPoints([-6.0, y0 - 1.0, 0], [-6.0 + X, y0 - 1.0, 0], DOWN, color=th.MUTED)
        xl = M("x", size=30).next_to(xb, DOWN, buff=0.05)
        e1 = M(r"\text{at } O:\quad y = a\sin\omega t", size=40, color=C_A).move_to([3.4, -1.4, 0])
        with self.say("Let us build the equation. The particle at the origin, O, performs simple harmonic motion: y equals a sine omega t."):
            self.add(wave, O, P)
            self.play(FadeIn(wave), FadeIn(O), FadeIn(Ol), Write(e1))
            t.rate = 1.0
            self.wait(1.5)
        e2 = M(r"\text{delay} = \frac{x}{v}", size=40).next_to(e1, DOWN, buff=0.3)
        e3 = M(r"\text{at } P:\quad y = a\sin\omega\left(t - \frac{x}{v}\right)", size=40, color=C_P).next_to(e2, DOWN, buff=0.3)
        with self.say("The wave moves right at speed v. It reaches a particle P, a distance x away, only after a delay of x over v. From then on, P simply repeats exactly what O did, x over v seconds earlier."):
            self.play(FadeIn(P), FadeIn(Pl), GrowFromCenter(xb), FadeIn(xl), Write(e2))
            self.wait(2)
        with self.say("So the displacement of P at time t is a sine omega, bracket t minus x over v. One equation, for every particle, at every instant."):
            self.play(Write(e3))
            self.wait(1.5)
        t.rate = 0
        self.play(FadeOut(VGroup(e1, e2, e3, Ol, Pl, xb, xl)), FadeOut(wave), FadeOut(O), FadeOut(P))
        self.remove(wave, O, P, t)
        title = T("The standard forms", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(
            M(r"y = a\sin\omega\left(t - \frac{x}{v}\right)", size=42),
            M(r"\omega = \frac{2\pi}{T},\ v = \frac{\lambda}{T}:\quad y = a\sin 2\pi\left(\frac{t}{T} - \frac{x}{\lambda}\right)", size=42),
            M(r"k = \frac{2\pi}{\lambda}:\quad y = a\sin(\omega t - kx),\qquad v = \frac{\omega}{k}", size=46, color=C_V),
            M(r"y = a\sin\frac{2\pi}{\lambda}(vt - x)", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(title, DOWN, buff=0.45)
        says = ["Now tidy it up. Start from y equals a sine omega, t minus x over v.",
                "Put omega equals two pi over T, and v equals lambda over T. It becomes a sine two pi, bracket t over T minus x over lambda.",
                "Give two pi over lambda a name: k, the propagation constant, or wave number. Then the wave is y equals a sine, omega t minus k x. And the wave speed is omega over k.",
                "Another form NEB often quotes: y equals a sine two pi over lambda, bracket v t minus x. All four say exactly the same thing."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        box = SurroundingRectangle(L[2], color=C_V, buff=0.12, corner_radius=0.1)
        self.play(Create(box))
        self.play(FadeOut(VGroup(L[0], L[1], L[3], title)), VGroup(L[2], box).animate.to_edge(UP, buff=0.8))
        t2 = clock(self, 1.0)
        right = always_redraw(lambda: curve(lambda x: 0.4 + 0.7 * np.sin(w * t2.get_value() - k * x), -6.3, 6.3, color=C_V, width=4))
        left = always_redraw(lambda: curve(lambda x: -1.9 + 0.7 * np.sin(w * t2.get_value() + k * x), -6.3, 6.3, color=C_2, width=4))
        rl = VGroup(M(r"\omega t - kx", size=34, color=C_V), Arrow(LEFT, RIGHT, color=C_V, buff=0).scale(0.6)).arrange(RIGHT, buff=0.2).move_to([4.6, 1.5, 0])
        ll = VGroup(Arrow(RIGHT, LEFT, color=C_2, buff=0).scale(0.6), M(r"\omega t + kx", size=34, color=C_2)).arrange(RIGHT, buff=0.2).move_to([4.6, -0.8, 0])
        with self.say("Minus k x means the wave travels in the positive x direction. For a wave travelling the other way, replace x by minus x: y equals a sine, omega t plus k x."):
            self.add(right, left)
            self.play(FadeIn(right), FadeIn(rl))
            self.play(FadeIn(left), FadeIn(ll))
            self.wait(2)
        self.play(FadeOut(VGroup(L[2], box, rl, ll)), FadeOut(right), FadeOut(left))
        self.remove(right, left, t2)
        example(self, "A progressive wave is given by y = 0.05 sin(100πt − 0.5πx) in SI units. Find the amplitude, frequency, wavelength, wave speed and maximum particle velocity.",
                [r"a = 0.05\ \text{m},\quad \omega = 100\pi\ \text{rad s}^{-1},\quad k = 0.5\pi\ \text{rad m}^{-1}",
                 r"f = \frac{\omega}{2\pi} = \frac{100\pi}{2\pi} = 50\ \text{Hz},\qquad \lambda = \frac{2\pi}{k} = \frac{2\pi}{0.5\pi} = 4\ \text{m}",
                 r"v = \frac{\omega}{k} = \frac{100\pi}{0.5\pi} = 200\ \text{m s}^{-1}\quad (f\lambda = 50 \times 4\ \checkmark)",
                 r"(v_p)_{\max} = a\omega = 0.05 \times 100\pi = 15.7\ \text{m s}^{-1}"],
                ["Worked example. A wave is given by y equals zero point zero five sine, one hundred pi t minus zero point five pi x, in S I units. Find the amplitude, frequency, wavelength, wave speed and maximum particle velocity.",
                 "Compare it with y equals a sine, omega t minus k x. The amplitude is zero point zero five metres, omega is one hundred pi, and k is zero point five pi.",
                 "Frequency is omega over two pi: fifty hertz. Wavelength is two pi over k: two pi over half pi, four metres.",
                 "Wave speed is omega over k: one hundred pi over half pi, two hundred metres per second. Check: f lambda is fifty times four, two hundred. It agrees.",
                 "And the maximum particle velocity, which we meet next, is a omega: zero point zero five times one hundred pi, fifteen point seven metres per second."], size=36)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        lam, v, A, y0 = 4.0, 1.0, 0.9, 0.4
        k, w = TAU / lam, TAU * v / lam
        t = clock(self, 1.0)
        dx = ValueTracker(1.0)
        xP = -3.0
        wave = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(w * t.get_value() - k * x), -6.3, 6.3, color=C_V, width=4))
        P = always_redraw(lambda: Dot([xP, y0 + A * np.sin(w * t.get_value() - k * xP), 0], radius=0.14, color=C_A))
        Q = always_redraw(lambda: Dot([xP + dx.get_value(), y0 + A * np.sin(w * t.get_value() - k * (xP + dx.get_value())), 0], radius=0.14, color=C_P))
        br = always_redraw(lambda: BraceBetweenPoints([xP, y0 - 1.1, 0], [xP + max(0.05, dx.get_value()), y0 - 1.1, 0], DOWN, color=th.MUTED))
        eq = M(r"\Delta\phi = \frac{2\pi}{\lambda}\,\Delta x", size=56).move_to([0, 2.5, 0])
        ro = VGroup(readout("Δx / λ =", lambda: dx.get_value() / lam, "", decimals=2, size=28),
                    readout("Δφ =", lambda: 360 * dx.get_value() / lam, "°", decimals=0, size=28, color=C_A)).arrange(RIGHT, buff=0.8).move_to([0, -1.9, 0])
        with self.say("The quantity inside the sine, omega t minus k x, is called the phase. It tells you where in its cycle a particle is. Two particles separated by a distance delta x differ in phase by two pi over lambda, times delta x."):
            self.add(wave, P, Q, br)
            self.play(FadeIn(wave), FadeIn(P), FadeIn(Q), FadeIn(br), Write(eq), FadeIn(ro))
            self.wait(2)
        tag = always_redraw(lambda: T("in step" if abs(dx.get_value() - lam) < 0.05 else ("exactly opposite" if abs(dx.get_value() - lam / 2) < 0.05 else ""), size=30,
                                      color=th.MINT, weight="BOLD").move_to([0, -2.7, 0]) if (abs(dx.get_value() - lam) < 0.05 or abs(dx.get_value() - lam / 2) < 0.05) else VGroup())
        self.add(tag)
        with self.say("Separate them by one whole wavelength, and the phase difference is two pi. They move exactly in step, as if they were the same particle."):
            self.play(dx.animate.set_value(lam), run_time=2.0)
            self.wait(2.5)
        with self.say("Separate them by half a wavelength, and the phase difference is pi. One is at a crest when the other is at a trough. Exactly out of step."):
            self.play(dx.animate.set_value(lam / 2), run_time=2.0)
            self.wait(2.5)
        self.play(FadeOut(VGroup(eq, ro)), FadeOut(wave), FadeOut(P), FadeOut(Q), FadeOut(br), FadeOut(tag))
        self.remove(wave, P, Q, br, tag, t)
        example(self, "A sound wave of frequency 500 Hz travels through air at 350 m/s. Find its wavelength and the phase difference between two points 0.175 m apart along the direction of travel.",
                [r"\lambda = \frac{v}{f} = \frac{350}{500} = 0.7\ \text{m}",
                 r"\Delta\phi = \frac{2\pi}{\lambda}\Delta x = \frac{2\pi}{0.7}\times 0.175 = 2\pi \times 0.25 = \frac{\pi}{2}\ \text{rad} = 90^{\circ}"],
                ["Worked example. A sound wave of frequency five hundred hertz travels through air at three hundred and fifty metres per second. Find its wavelength, and the phase difference between two points zero point one seven five metres apart.",
                 "Wavelength is v over f: three fifty over five hundred, zero point seven metres.",
                 "The two points are zero point one seven five over zero point seven, a quarter of a wavelength apart. So the phase difference is a quarter of two pi: pi by two, ninety degrees. When one is at a crest, the other is passing its mean position."], size=40)
        self.particle_velocity()
        example(self, "A wave of frequency 250 Hz and amplitude 2 cm travels along a string at 400 m/s. Find λ and T, the phase difference and time lag between points 0.4 m apart, the wave equation and the maximum particle velocity.",
                [r"\lambda = \frac{v}{f} = \frac{400}{250} = 1.6\ \text{m},\qquad T = \frac{1}{f} = 4\ \text{ms}",
                 r"\Delta\phi = \frac{2\pi}{1.6}\times 0.4 = \frac{\pi}{2}\ \text{rad},\qquad \Delta t = \frac{\Delta x}{v} = \frac{0.4}{400} = 1\ \text{ms} = \frac{T}{4}",
                 r"\omega = 2\pi f = 500\pi,\quad k = \frac{2\pi}{1.6} = 1.25\pi \;\Rightarrow\; y = 0.02\sin(500\pi t - 1.25\pi x)\ \text{m}",
                 r"(v_p)_{\max} = a\omega = 0.02 \times 500\pi = 10\pi = 31.4\ \text{m s}^{-1}"],
                ["Now a full eight mark question, the kind that closes many papers. A wave of frequency two hundred and fifty hertz and amplitude two centimetres travels along a string at four hundred metres per second. Find everything.",
                 "Wavelength is v over f: four hundred over two fifty, one point six metres. The period is one over f, four milliseconds.",
                 "Points zero point four metres apart are a quarter wavelength apart, so the phase difference is pi by two. The wave takes zero point four over four hundred, one millisecond, to cover that gap. That is exactly a quarter of the period, as it should be.",
                 "For the equation, omega is two pi f, five hundred pi, and k is two pi over one point six, one point two five pi. With the amplitude in metres, y equals zero point zero two sine, five hundred pi t minus one point two five pi x.",
                 "And the maximum particle velocity is a omega: zero point zero two times five hundred pi, ten pi, about thirty one point four metres per second. Far slower than the wave's four hundred, as you would expect."], size=34)
        self.quiz("Two points in a progressive wave are λ/4 apart. Their phase difference is",
                  [M(r"\pi/4", size=36), M(r"\pi/2", size=36), M(r"\pi", size=36), M(r"2\pi", size=36)], 1,
                  "Pause and think. Two points in a progressive wave are a quarter of a wavelength apart. What is their phase difference?",
                  "B, pi by two. Two pi over lambda, times lambda over four. If you chose pi by four, you divided the angle and the distance by the same four twice. A whole wavelength is two pi, so a quarter of it is pi by two.")

    def particle_velocity(self):
        lam, v, A, y0 = 4.0, 1.0, 0.9, 0.2
        k, w = TAU / lam, TAU * v / lam
        t = clock(self, 1.0)
        xs = np.linspace(-6.0, 6.0, 25)
        wave = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(w * t.get_value() - k * x), -6.3, 6.3, color=th.FAINT, width=3))

        def arrows():
            g = VGroup()
            tt = t.get_value()
            for x in xs:
                yv = y0 + A * np.sin(w * tt - k * x)
                vp = A * w * np.cos(w * tt - k * x)
                g.add(Dot([x, yv, 0], radius=0.08, color=C_V), arrow([x, yv, 0], [x, yv + 0.55 * vp, 0], C_P, width=4))
            return g
        ar = always_redraw(arrows)
        wv = Arrow([-2.0, 2.4, 0], [2.0, 2.4, 0], buff=0, color=C_A, stroke_width=6)
        wl = T("wave velocity v = fλ: constant", size=26, color=C_A).next_to(wv, UP, buff=0.1)
        eq = M(r"v_p = \frac{\partial y}{\partial t} = a\omega\cos(\omega t - kx),\qquad (v_p)_{\max} = a\omega", size=40, color=C_P).to_edge(DOWN, buff=0.6)
        with self.say("Now a classic confusion. Differentiate y with respect to time, holding x fixed, and you get the particle velocity: a omega cos, omega t minus k x. The red arrows show it."):
            self.add(wave, ar)
            self.play(FadeIn(wave), FadeIn(ar), Write(eq))
            self.wait(2)
        with self.say("Look closely. The particle velocity is zero at every crest and every trough, and greatest, a omega, as each particle rushes through its mean position. Meanwhile the wave itself glides along at one steady speed, f lambda."):
            self.play(GrowArrow(wv), FadeIn(wl))
            self.wait(4)
        cau = self.callout("careful", "Particle velocity aω cos(ωt − kx) changes from instant to instant. Wave velocity fλ is a constant of the medium. They are linked by vp = −v (∂y/∂x).", width=11, size=26)
        cau.move_to([0, 0.2, 0])
        self.play(FadeOut(VGroup(eq, wv, wl)), FadeOut(wave), FadeOut(ar))
        self.remove(wave, ar, t)
        with self.say("So never mix them up. The particle velocity keeps changing. The wave velocity is a fixed property of the medium. Differentiating with respect to x instead gives the slope of the wave, and the two are linked: particle velocity equals minus v times the slope."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        self.reflection()
        lam, v, A, y0 = 4.0, 1.0, 0.55, 0.2
        k, w = TAU / lam, TAU * v / lam
        t = clock(self, 1.0)
        x0 = -6.0
        y1 = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(w * t.get_value() - k * (x - x0)), -6.0, 6.0, color=C_1, width=3))
        y2 = always_redraw(lambda: curve(lambda x: y0 + A * np.sin(w * t.get_value() + k * (x - x0)), -6.0, 6.0, color=C_2, width=3))
        ys = always_redraw(lambda: curve(lambda x: y0 + 2 * A * np.cos(k * (x - x0)) * np.sin(w * t.get_value()), -6.0, 6.0, color=WHITE, width=6))
        lab1 = VGroup(T("incident", size=24, color=C_1), Arrow(LEFT, RIGHT, color=C_1, buff=0).scale(0.5)).arrange(RIGHT, buff=0.15).move_to([-4.6, 2.3, 0])
        lab2 = VGroup(Arrow(RIGHT, LEFT, color=C_2, buff=0).scale(0.5), T("reflected", size=24, color=C_2)).arrange(RIGHT, buff=0.15).move_to([4.6, 2.3, 0])
        with self.say("Now let two waves meet head on. They have the same amplitude, the same frequency and the same speed, but they travel in opposite directions. In practice the second is usually the reflection of the first, from the fixed end of a sarangi string, or the end of the air column in a flute."):
            self.add(y1)
            self.play(FadeIn(y1), FadeIn(lab1))
            self.add(y2)
            self.play(FadeIn(y2), FadeIn(lab2))
            self.wait(2)
        sl = T("sum", size=26, color=WHITE, weight="BOLD").move_to([0, 2.3, 0])
        with self.say("By the principle of superposition, the displacement at every point is the sum of the two. And look what the sum does. It does not travel at all. It just swells and shrinks in place."):
            self.add(ys)
            self.play(FadeIn(ys), FadeIn(sl))
            self.wait(4)
        with self.say("Fade out the two travelling waves, and here it is on its own: a stationary, or standing, wave. Some points never move at all. Others swing with double the amplitude."):
            self.play(FadeOut(y1), FadeOut(y2), FadeOut(lab1), FadeOut(lab2))
            self.remove(y1, y2)
            self.wait(4)
        self.play(FadeOut(ys), FadeOut(sl))
        self.remove(ys, t)
        title = T("Equation of a stationary wave", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(
            M(r"y_1 = a\sin(\omega t - kx),\qquad y_2 = a\sin(\omega t + kx)", size=40),
            M(r"y = y_1 + y_2,\qquad \sin C + \sin D = 2\sin\frac{C + D}{2}\cos\frac{C - D}{2}", size=38),
            M(r"y = 2a\cos kx\,\sin\omega t = \left[2a\cos\frac{2\pi x}{\lambda}\right]\sin\frac{2\pi t}{T}", size=44, color=th.INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.45)
        says = ["Let us prove it. The incident wave travels in the plus x direction: y one equals a sine, omega t minus k x. The reflected wave travels in the minus x direction: y two equals a sine, omega t plus k x.",
                "Add them, using the identity sine C plus sine D equals two sine of half the sum, times cos of half the difference. Here C is omega t plus k x, and D is omega t minus k x.",
                "Half the sum is omega t, and half the difference is k x. So y equals two a cos k x, times sine omega t."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.4)
        b1 = Brace(L[2][0][2:9], DOWN, color=C_A)
        b1l = T("amplitude, depends on x", size=24, color=C_A).next_to(b1, DOWN, buff=0.1)
        note = para("Not of the form f(vt − x): x and t have separated, so nothing travels. Every particle does SHM of period T, with its own amplitude A = 2a cos(2πx/λ).", width=11, size=26, color=th.BODY).to_edge(DOWN, buff=0.6)
        with self.say("Look carefully at the form. It is not a function of v t minus x. The x part and the t part have separated, so nothing travels. Every particle performs simple harmonic motion of period T, but with its own amplitude, two a cos two pi x over lambda, which depends on where the particle is."):
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            self.play(FadeIn(note, shift=UP * 0.2))
        nb = neby_in(self, "think", corner=DR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, L, b1, b1l, note)))
        neby_out(self, nb)

    def reflection(self):
        xw, v, A = 4.5, 2.0, 1.0
        t = ValueTracker(0)
        g = lambda s_: A * np.exp(-(s_ / 0.45) ** 2)
        xs0 = -6.5
        y0 = 0.0
        yy = lambda x: g(x - (xs0 + v * t.get_value())) - g((2 * xw - x) - (xs0 + v * t.get_value()))
        string = always_redraw(lambda: curve(lambda x: y0 + yy(x), -6.3, xw, n=260, color=C_V, width=5))
        wall = VGroup(Line([xw, -1.6, 0], [xw, 1.6, 0], color=th.BODY, stroke_width=6),
                      *[Line([xw, y, 0], [xw + 0.25, y + 0.2, 0], color=th.MUTED, stroke_width=2) for y in np.linspace(-1.5, 1.4, 9)])
        wl = T("fixed end", size=24, color=th.MUTED).next_to(wall, DOWN, buff=0.15)
        with self.say("First, where does the second wave come from? Send a single pulse along a string tied to a wall."):
            self.add(string)
            self.play(FadeIn(string), FadeIn(wall), FadeIn(wl))
            self.play(t.animate.set_value(4.0), run_time=3.0, rate_func=linear)
        note = T("reflected upside down: a phase change of π", size=28, color=th.AMBER).to_edge(UP, buff=0.9)
        with self.say("At the fixed end, the string cannot move. The wall pulls back on it, and the pulse comes back upside down. Reflection at a fixed end reverses the phase by pi. Send a continuous wave instead, and the reflected wave overlaps the incoming one all along the string."):
            self.play(t.animate.set_value(9.5), run_time=4.0, rate_func=linear)
            self.play(FadeIn(note, shift=DOWN * 0.2))
        self.play(FadeOut(VGroup(wall, wl, note)), FadeOut(string))
        self.remove(string)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        lam, v, A, y0 = 4.0, 1.0, 0.6, 0.6
        k, w = TAU / lam, TAU * v / lam
        x0 = -6.0
        t = clock(self, 1.0)
        env = VGroup(curve(lambda x: y0 + 2 * A * np.cos(k * (x - x0)), -6, 6, color=C_A, width=2), curve(lambda x: y0 - 2 * A * np.cos(k * (x - x0)), -6, 6, color=C_A, width=2))
        env = VGroup(*[DashedVMobject(e, num_dashes=60) for e in env])
        ys = always_redraw(lambda: curve(lambda x: y0 + 2 * A * np.cos(k * (x - x0)) * np.sin(w * t.get_value()), -6.0, 6.0, color=WHITE, width=6))
        nodes = [x0 + lam / 4 + n * lam / 2 for n in range(6)]
        antis = [x0 + n * lam / 2 for n in range(7)]
        nd = VGroup(*[Dot([x, y0, 0], radius=0.11, color=th.CORAL) for x in nodes])
        ndl = VGroup(*[T("N", size=24, color=th.CORAL, weight="BOLD").move_to([x, y0 - 1.65, 0]) for x in nodes])
        ad = VGroup(*[T("A", size=24, color=th.MINT, weight="BOLD").move_to([x, y0 + 1.65, 0]) for x in antis])
        with self.say("The amplitude, two a cos k x, is zero at some points and greatest at others. The dashed envelope shows it."):
            self.add(ys)
            self.play(FadeIn(ys), Create(env))
            self.wait(2)
        en = VGroup(M(r"\cos\frac{2\pi x}{\lambda} = 0", size=34), M(r"x = \frac{\lambda}{4},\ \frac{3\lambda}{4},\ \frac{5\lambda}{4},\ \ldots", size=34)).arrange(DOWN, buff=0.15)
        ea = VGroup(M(r"\cos\frac{2\pi x}{\lambda} = \pm 1", size=34), M(r"x = 0,\ \frac{\lambda}{2},\ \lambda,\ \ldots", size=34)).arrange(DOWN, buff=0.15)
        en.move_to([-3.2, -2.55, 0])
        ea.move_to([3.2, -2.55, 0])
        enl = T("nodes: never move", size=24, color=th.CORAL).next_to(en, UP, buff=0.12)
        eal = T("antinodes: amplitude 2a", size=24, color=th.MINT).next_to(ea, UP, buff=0.12)
        with self.say("Nodes are points of permanently zero displacement, where cos two pi x over lambda is zero. That happens at x equals lambda by four, three lambda by four, five lambda by four, and so on."):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in nd], lag_ratio=0.1), FadeIn(ndl))
            self.play(FadeIn(enl), Write(en))
        with self.say("Antinodes are points of maximum amplitude, two a, where the cos is plus or minus one: at x equals zero, lambda by two, lambda, and so on."):
            self.play(FadeIn(ad))
            self.play(FadeIn(eal), Write(ea))
        self.play(FadeOut(VGroup(en, ea, enl, eal)))
        b1 = BraceBetweenPoints([nodes[1], y0 - 2.0, 0], [nodes[2], y0 - 2.0, 0], DOWN, color=th.CORAL)
        b1l = M(r"\lambda/2", size=34, color=th.CORAL).next_to(b1, DOWN, buff=0.08)
        b2 = BraceBetweenPoints([antis[4], y0 - 2.0, 0], [nodes[4], y0 - 2.0, 0], DOWN, color=C_A)
        b2l = M(r"\lambda/4", size=34, color=C_A).next_to(b2, DOWN, buff=0.08)
        with self.say("So successive nodes are half a wavelength apart, successive antinodes are half a wavelength apart, and a node is a quarter wavelength from the next antinode. Measuring the distance between nodes is the standard laboratory way to find a wavelength."):
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            self.play(GrowFromCenter(b2), FadeIn(b2l))
            self.wait(1.5)
        alt = T("Origin at a node instead: y = 2a sin kx cos ωt. Same spacings.", size=24, color=th.BODY).to_edge(DOWN, buff=0.5)
        with self.say("If you put the origin at a node instead of an antinode, the same working gives y equals two a sine k x cos omega t. Only the labels change. The spacings, lambda by two and lambda by four, stay the same."):
            self.play(FadeOut(VGroup(b1, b1l, b2, b2l)), FadeIn(alt))
            self.wait(1)
        self.play(FadeOut(VGroup(env, nd, ndl, ad, alt)), FadeOut(ys))
        self.remove(ys, t)
        self.compare()
        example(self, "A stationary wave is y = 4 sin(0.5πx) cos(200πt), with y and x in cm and t in s. Find the amplitude of each component wave, the wavelength, frequency, wave speed and the distance between successive nodes.",
                [r"2a = 4\ \text{cm} \;\Rightarrow\; a = 2\ \text{cm}",
                 r"k = 0.5\pi\ \text{cm}^{-1} \;\Rightarrow\; \lambda = \frac{2\pi}{0.5\pi} = 4\ \text{cm}",
                 r"\omega = 200\pi \;\Rightarrow\; f = \frac{\omega}{2\pi} = 100\ \text{Hz}",
                 r"v = f\lambda = 100 \times 0.04 = 4\ \text{m s}^{-1}",
                 r"\text{nodes } \tfrac{\lambda}{2} = 2\ \text{cm apart}\ \ (x = 0, 2, 4, 6\ \text{cm})"],
                ["Worked example. A stationary wave on a string is y equals four sine, zero point five pi x, cos two hundred pi t, with y and x in centimetres. Find the amplitude of each component wave, the wavelength, the frequency, the wave speed, and the distance between nodes.",
                 "Compare with y equals two a sine k x cos omega t. Two a is four centimetres, so each component wave has amplitude two centimetres.",
                 "k is zero point five pi per centimetre, so lambda is two pi over half pi, four centimetres.",
                 "Omega is two hundred pi, so f is one hundred hertz.",
                 "The wave speed of each component is f lambda: one hundred times zero point zero four metres, four metres per second. Careful with the centimetres.",
                 "And nodes are lambda by two apart: two centimetres. Check: sine of half pi x is zero at x equals zero, two, four, six."], size=38)
        example(self, "A stationary wave is y = 5 sin(0.4πx) cos(100πt), with y and x in cm. Find the wavelength, frequency, wave speed and the distance between a node and the next antinode.",
                [r"k = 0.4\pi \;\Rightarrow\; \lambda = \frac{2\pi}{0.4\pi} = 5\ \text{cm}",
                 r"\omega = 100\pi \;\Rightarrow\; f = 50\ \text{Hz},\qquad v = f\lambda = 50 \times 0.05 = 2.5\ \text{m s}^{-1}",
                 r"\text{node to next antinode} = \frac{\lambda}{4} = 1.25\ \text{cm}"],
                ["One more for practice. A stationary wave is y equals five sine, zero point four pi x, cos one hundred pi t, in centimetres. Find the wavelength, frequency, speed, and the distance from a node to the next antinode.",
                 "k is zero point four pi, so lambda is two pi over zero point four pi: five centimetres.",
                 "Omega is one hundred pi, so f is fifty hertz, and the speed is fifty times zero point zero five metres: two point five metres per second.",
                 "Node to the next antinode is a quarter wavelength: one point two five centimetres."], size=40)
        self.quiz("In a stationary wave, the net energy transported across a node is",
                  ["maximum", "zero", "equal to 2a", "proportional to f"], 1,
                  "Pause and think. In a stationary wave, how much energy is carried across a node?",
                  "B, zero. A node never moves, so no work is done across it, and no energy can cross. The energy only sloshes back and forth between the neighbouring nodes. That is exactly why a stationary wave does not transport energy.")
        self.quiz("The distance between two consecutive nodes of a stationary wave is",
                  [M(r"\lambda", size=38), M(r"\lambda/2", size=38), M(r"\lambda/4", size=38), M(r"2\lambda", size=38)], 1,
                  "Pause and think. What is the distance between two consecutive nodes of a stationary wave?",
                  "B, lambda by two. Nodes come at lambda by four, three lambda by four, five lambda by four: half a wavelength apart. Lambda by four is the distance from a node to the next antinode, the most common slip.")
        self.tip("Read the form first: y = a sin(ωt − kx) travels; y = 2a cos kx sin ωt (x and t in separate factors) stands still. Then ω gives f, k gives λ, and v = ω/k.",
                 "Here is a quick exam habit. Before you calculate anything, look at the form of the equation. If x and t sit together inside one sine, the wave travels. If they sit in separate factors, it is a stationary wave. Then omega gives f, k gives lambda, and omega over k gives the speed.", state="wink")

    def compare(self):
        title = T("Progressive vs stationary", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        rows = [("", "Progressive", "Stationary"), ("disturbance", "advances", "stays between boundaries"), ("energy", "carried along", "not transported"),
                ("amplitude", "same for all particles", "0 at nodes to 2a at antinodes"), ("phase", "changes steadily with x", "same between two nodes"),
                ("nodes", "none", "λ/2 apart, never move")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=26 if i else 28, color=(th.BG if not c else ([th.MUTED, C_V, C_A][j] if i == 0 or j == 0 else th.BODY)),
                             weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.6, -0.9, 3.6]):
                row[j].move_to([x, 2.0 - i * 0.78, 0])
            grid.add(row)
        with self.say("Here are the differences the exam asks for. A progressive wave advances through the medium and carries energy along. A stationary wave stays put, and transports no energy: energy just sloshes back and forth between neighbouring nodes. In a progressive wave every particle has the same amplitude. In a stationary wave the amplitude runs from zero at the nodes to two a at the antinodes. And all the particles between two nodes move in phase, reversing across each node.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.7)
        self.play(FadeOut(VGroup(title, grid)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "A progressive wave carries energy, not matter. Transverse: vibration across travel. Longitudinal: along it.",
            M(r"v = f\lambda = \frac{\lambda}{T}\quad(\text{fixed by the medium: raise } f, \lambda \text{ shrinks})", size=34),
            M(r"y = a\sin(\omega t - kx) = a\sin 2\pi\left(\tfrac{t}{T} - \tfrac{x}{\lambda}\right),\ \ k = \tfrac{2\pi}{\lambda},\ \ v = \tfrac{\omega}{k}", size=32),
            M(r"\Delta\phi = \frac{2\pi}{\lambda}\Delta x,\qquad v_p = a\omega\cos(\omega t - kx),\ (v_p)_{\max} = a\omega", size=32),
            M(r"\text{stationary: } y = 2a\cos kx\,\sin\omega t", size=34),
            M(r"\text{nodes } \tfrac{\lambda}{4}, \tfrac{3\lambda}{4}, \ldots;\ \text{antinodes } 0, \tfrac{\lambda}{2}, \ldots;\ \text{N to N} = \tfrac{\lambda}{2},\ \text{N to A} = \tfrac{\lambda}{4}", size=32),
        ], "Let us recap. A progressive wave carries energy, not matter, and can be transverse or longitudinal. v equals f lambda, and the medium fixes v. The travelling wave is y equals a sine, omega t minus k x. Phase difference is two pi over lambda times the path difference, and particle velocity peaks at a omega. Two equal waves travelling in opposite directions make a stationary wave, two a cos k x sine omega t, with nodes half a wavelength apart, and a node a quarter wavelength from each antinode.")
        self.outro("That is wave motion. Next, we ask what decides the speed of a wave, in a string, in a solid, and in air, in Mechanical Waves. See you there, on NEBians.")
