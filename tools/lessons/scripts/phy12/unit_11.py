import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import clock, curve, example, neby_in, neby_out, readout  # noqa: E402

C_1, C_2, C_S, C_I = th.SKY, th.PINK, WHITE, th.AMBER


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


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 11
    TITLE = "Interference"
    SUBTITLE = "Light plus light can make darkness"
    SECTIONS = ["Superposition of light", "Bright and dark", "Coherent sources", "Young's double slit",
                "Fringe positions and width", "What changes the fringes"]
    NEXT = "Unit 12 · Diffraction"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        wall_x = 4.6
        a = ValueTracker(0.0)
        lam = 600
        col = wl_rgb(lam)
        wall = always_redraw(lambda: strip(wall_x, -2.8, 2.8, 1.0, lambda y: col * (0.5 * (1 - a.get_value()) * (np.exp(-y ** 2 / 9) * 1.0)
                                                                                     + a.get_value() * np.exp(-y ** 2 / 12) * np.cos(PI * y / 0.55) ** 2), n=90))
        t1 = VGroup(RoundedRectangle(corner_radius=0.08, width=1.0, height=0.4, fill_color=th.MUTED, fill_opacity=1, stroke_width=0)).move_to([-4.6, 1.2, 0])
        t2 = t1.copy().move_to([-4.6, -1.2, 0])
        beams = VGroup(Polygon([-4.1, 1.2, 0], [wall_x - 0.5, 2.8, 0], [wall_x - 0.5, -1.6, 0], stroke_width=0, fill_color=ManimColor.from_rgb(col), fill_opacity=0.12),
                       Polygon([-4.1, -1.2, 0], [wall_x - 0.5, 1.6, 0], [wall_x - 0.5, -2.8, 0], stroke_width=0, fill_color=ManimColor.from_rgb(col), fill_opacity=0.12))
        lab = T("two torches", size=26, color=th.MUTED).move_to([-4.6, 2.4, 0])
        with self.say("Point two orange torches at the same wall. Where the beams overlap, the wall is simply brighter. Light plus light gives more light. Obviously."):
            self.add(wall)
            self.play(FadeIn(wall), FadeIn(t1), FadeIn(t2), FadeIn(beams), FadeIn(lab))
        lamp = Dot([-5.6, 0, 0], color=ManimColor.from_rgb(col), radius=0.15)
        bar = VGroup(Line([-3.4, 2.8, 0], [-3.4, 0.25, 0]), Line([-3.4, 0.15, 0], [-3.4, -0.15, 0]), Line([-3.4, -0.25, 0], [-3.4, -2.8, 0])).set_stroke(th.BODY, 6)
        slits = VGroup(Line([-3.4, 0.25, 0], [-3.4, 0.15, 0], stroke_opacity=0), Line([-3.4, -0.15, 0], [-3.4, -0.25, 0], stroke_opacity=0))
        lab2 = T("one lamp, two narrow slits", size=26, color=th.MUTED).move_to([-4.0, 2.4, 0])
        with self.say("Now use a single lamp, and let its light pass through two very narrow slits, close together. Same colour, same wall."):
            self.play(FadeOut(VGroup(t1, t2, beams, lab)), FadeIn(lamp), Create(bar), FadeIn(lab2))
            self.play(a.animate.set_value(1.0), run_time=2.5)
        nb = neby_in(self, "surprised", corner=DL)
        q = T("Light + light = darkness?", size=34, color=th.AMBER, weight="BOLD").move_to([0.4, -3.0, 0])
        with self.say("Stripes. Bright bands, and between them, completely dark bands. In those dark places, light from one slit plus light from the other gives no light at all. How can light cancel light? Thomas Young showed this in eighteen hundred and one, and it finally proved that light is a wave."):
            self.play(FadeIn(q, shift=UP * 0.2))
        self.play(FadeOut(VGroup(lamp, bar, lab2, q)), FadeOut(wall))
        self.remove(wall)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 11: Interference. In this short unit you will learn when light can cancel light, why ordinary lamps never show it, and how to predict exactly where every stripe in Young's experiment appears."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. Superposition of light waves, the conditions for bright and dark, coherent sources, Young's double slit experiment, the positions and width of the fringes, and what changes them.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        t = clock(self, 1.0)
        phi = ValueTracker(0.0)
        a1, a2 = 0.6, 0.6
        k, w = TAU / 2.6, 2.2
        y1 = always_redraw(lambda: curve(lambda x: 1.9 + a1 * np.sin(w * t.get_value() - k * x), -6.3, 0.4, color=C_1, width=3))
        y2 = always_redraw(lambda: curve(lambda x: 0.4 + a2 * np.sin(w * t.get_value() - k * x + phi.get_value()), -6.3, 0.4, color=C_2, width=3))
        ys = always_redraw(lambda: curve(lambda x: -1.6 + a1 * np.sin(w * t.get_value() - k * x) + a2 * np.sin(w * t.get_value() - k * x + phi.get_value()), -6.3, 0.4, color=C_S, width=5))
        labs = VGroup(T("wave 1", size=22, color=C_1).move_to([-5.6, 2.75, 0]), T("wave 2", size=22, color=C_2).move_to([-5.6, 1.25, 0]), T("sum", size=22, color=C_S).move_to([-5.6, -0.4, 0]))
        O = np.array([4.0, -0.4, 0])
        sc = 1.6

        def phasor():
            p = phi.get_value()
            e1 = O + RIGHT * a1 * sc
            e2 = e1 + a2 * sc * np.array([np.cos(p), np.sin(p), 0])
            g = VGroup(Arrow(O, e1, buff=0, color=C_1, stroke_width=5), Arrow(e1, e2, buff=0, color=C_2, stroke_width=5) if np.linalg.norm(e2 - e1) > 0.1 else VGroup())
            if np.linalg.norm(e2 - O) > 0.12:
                g.add(Arrow(O, e2, buff=0, color=C_S, stroke_width=6))
            return g
        ph = always_redraw(phasor)
        ro = VGroup(readout("φ =", lambda: np.degrees(phi.get_value()), "°", decimals=0, size=26, color=th.AMBER),
                    readout("A =", lambda: np.sqrt(a1 ** 2 + a2 ** 2 + 2 * a1 * a2 * np.cos(phi.get_value())) / a1, "× a", decimals=2, size=26, color=C_S)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 2.3, 0])
        with self.say("When two waves arrive at the same point, the principle of superposition says the displacements simply add. Here are two light waves of the same frequency. When they arrive in step, the sum has double the amplitude."):
            self.add(y1, y2, ys)
            self.play(FadeIn(y1), FadeIn(y2), FadeIn(ys), FadeIn(labs))
            self.add(ph)
            self.play(FadeIn(ph), FadeIn(ro))
            self.wait(1.5)
        with self.say("Now slide wave two out of step. The phase difference, phi, grows. On the right, the two amplitudes add like arrows, head to tail. At a phase difference of pi, half a cycle, the crests of one sit on the troughs of the other, and the sum is zero."):
            self.play(phi.animate.set_value(PI), run_time=4)
            self.wait(1)
            self.play(phi.animate.set_value(PI / 2), run_time=2)
        eq = VGroup(M(r"A = \sqrt{a_1^{2} + a_2^{2} + 2a_1a_2\cos\phi}", size=38), M(r"I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi", size=38, color=C_I)).arrange(DOWN, buff=0.3).scale(0.85).move_to([4.2, -2.4, 0])
        with self.say("The arrows give the resultant amplitude: A equals the square root of a one squared plus a two squared plus two a one a two cos phi. Intensity goes as amplitude squared, so I equals I one plus I two plus two root I one I two cos phi. That last part is the interference term: positive in step, negative out of step."):
            self.play(FadeOut(ph), FadeOut(ro))
            self.remove(ph)
            self.play(Write(eq[0]))
            self.play(Write(eq[1]))
        self.play(FadeOut(VGroup(labs, eq)), FadeOut(y1), FadeOut(y2), FadeOut(ys))
        self.remove(y1, y2, ys, t)
        d = self.callout("key", "Interference: the change in intensity produced when two or more light waves superpose. Maximum intensity: constructive. Minimum: destructive.", width=11, size=28)
        with self.say("That is interference: the modification of intensity when light waves superpose. Where the intensity is greatest, the interference is constructive. Where it is least, it is destructive."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        t = clock(self, 1.0)
        S1, S2 = np.array([-5.0, 0.9, 0]), np.array([-5.0, -0.9, 0])
        lam, v = 0.9, 0.9

        def fronts():
            g = VGroup()
            tt = t.get_value()
            for S, c in ((S1, C_1), (S2, C_2)):
                for k_ in range(14):
                    r = (tt * v) % lam + k_ * lam
                    if 0.05 < r < 11:
                        g.add(Circle(radius=r, stroke_color=c, stroke_width=2.5, stroke_opacity=max(0.2, 0.9 - r / 13)).move_to(S))
            return g
        fr = always_redraw(fronts)
        dots = VGroup(Dot(S1, color=C_1), Dot(S2, color=C_2))
        with self.say("Picture two sources sending out identical waves in step, like two fingers dipping into a pond together. Each circle is a crest."):
            self.add(fr)
            self.play(FadeIn(dots), FadeIn(fr))
            self.wait(2.5)
        lines = VGroup()
        for n in range(-1, 2):
            ang = np.arcsin(np.clip(n * lam / 1.8, -1, 1))
            lines.add(DashedLine(np.array([-5.0, 0, 0]), np.array([-5.0, 0, 0]) + 11.5 * np.array([np.cos(ang), np.sin(ang), 0]), color=WHITE, stroke_width=3 if n == 0 else 2, stroke_opacity=0.8))
        with self.say("Where a crest of one meets a crest of the other, the waves reinforce. Those points lie along these lines, fanning out. In between, a crest of one meets a trough of the other, and they cancel."):
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1), run_time=2)
            self.wait(1.5)
        self.play(FadeOut(VGroup(dots, lines)), FadeOut(fr))
        self.remove(fr, t)
        title = T("Path difference decides it", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        eq = M(r"\phi = \frac{2\pi}{\lambda}\,\Delta", size=52).next_to(title, DOWN, buff=0.35)
        rows = VGroup(
            VGroup(T("bright (constructive)", size=26, color=C_I, weight="BOLD"), M(r"\Delta = n\lambda,\quad \phi = 2n\pi", size=36), M(r"A = a_1 + a_2,\ \ I_{\max} = (\sqrt{I_1} + \sqrt{I_2})^{2}", size=32)),
            VGroup(T("dark (destructive)", size=26, color=th.SKY, weight="BOLD"), M(r"\Delta = (2n - 1)\frac{\lambda}{2},\quad \phi = (2n - 1)\pi", size=36), M(r"A = |a_1 - a_2|,\ \ I_{\min} = (\sqrt{I_1} - \sqrt{I_2})^{2}", size=32)))
        for r in rows:
            r.arrange(DOWN, buff=0.15)
        rows.arrange(RIGHT, buff=0.9).next_to(eq, DOWN, buff=0.5)
        with self.say("What decides it is the path difference, delta: how much further one wave has travelled than the other. A path difference delta means a phase difference of two pi over lambda, times delta."):
            self.play(FadeIn(title), Write(eq))
        with self.say("If the path difference is a whole number of wavelengths, the waves arrive in step: a bright point. The amplitudes add, and the intensity is root I one plus root I two, all squared."):
            self.play(FadeIn(rows[0], shift=UP * 0.2))
        with self.say("If it is an odd number of half wavelengths, they arrive exactly out of step: a dark point. The amplitudes subtract, and the intensity is root I one minus root I two, squared."):
            self.play(FadeIn(rows[1], shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, eq, rows)))
        ax = Axes(x_range=[-3 * PI, 3 * PI, PI], y_range=[0, 4.4, 1], x_length=10, y_length=3.2, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([0, -0.2, 0])
        Ic = ax.plot(lambda p: 4 * np.cos(p / 2) ** 2, x_range=[-3 * PI, 3 * PI], color=C_I, stroke_width=5)
        avg = DashedLine(ax.c2p(-3 * PI, 2), ax.c2p(3 * PI, 2), color=th.MUTED)
        eq2 = M(r"I = 4I_0\cos^{2}\frac{\phi}{2}", size=50, color=C_I).to_edge(UP, buff=1.0)
        lb = VGroup(M("4I_0", size=30).next_to(ax.c2p(-3 * PI, 4), LEFT, buff=0.15), M("2I_0", size=30, color=th.MUTED).next_to(ax.c2p(-3 * PI, 2), LEFT, buff=0.15),
                    T("phase difference φ", size=22, color=th.BODY).next_to(ax, DOWN, buff=0.2))
        with self.say("For two equal sources of intensity I nought each, this becomes I equals four I nought cos squared phi by two. Bright points reach four I nought, dark points fall to zero."):
            self.play(Write(eq2), Create(ax), FadeIn(lb))
            self.play(Create(Ic), run_time=2)
        cau = para("Energy is not destroyed: it is redistributed. The average of 4I₀ cos²(φ/2) is exactly 2I₀, the sum of the two beams.", width=10, size=26, color=th.AMBER).to_edge(DOWN, buff=0.45)
        with self.say("But wait: where did the light at the dark points go? Nowhere. It was moved. Without interference, every point would get two I nought. With it, bright points get four I nought and dark points zero. Average it over one fringe, and you get exactly two I nought. Interference redistributes energy. It never destroys it."):
            self.play(Create(avg))
            self.play(FadeIn(cau))
        self.play(FadeOut(VGroup(ax, Ic, avg, eq2, lb, cau)))
        example(self, "Two coherent sources have intensities in the ratio 4 : 1. Find the amplitude ratio and Imax : Imin. For two equal sources, what fraction of Imax is the intensity where the path difference is λ/3?",
                [r"\frac{a_1}{a_2} = \sqrt{\frac{4}{1}} = 2",
                 r"\frac{I_{\max}}{I_{\min}} = \frac{(a_1 + a_2)^{2}}{(a_1 - a_2)^{2}} = \frac{(2 + 1)^{2}}{(2 - 1)^{2}} = \frac{9}{1}",
                 r"\phi = \frac{2\pi}{\lambda}\cdot\frac{\lambda}{3} = \frac{2\pi}{3}:\ \ I = 4I_0\cos^{2}\frac{\pi}{3} = 4I_0(0.5)^{2} = I_0 = \frac{I_{\max}}{4}"],
                ["Worked example. Two coherent sources have intensities in the ratio four to one. Find the ratio of amplitudes, and of maximum to minimum intensity. Then, for equal sources, find the intensity where the path difference is lambda by three.",
                 "Intensity goes as amplitude squared, so the amplitudes are in the ratio root four, two to one.",
                 "Maximum over minimum is a one plus a two, squared, over a one minus a two, squared: three squared over one squared, nine to one.",
                 "For equal sources, a path difference of lambda by three is a phase of two pi by three. Four I nought cos squared of pi by three is four I nought times a quarter: just I nought, a quarter of the maximum."], size=38)
        self.quiz("At a point where the path difference is λ/2, the intensity due to two equal coherent sources (I₀ each) is",
                  [M("4I_0", size=40), M("2I_0", size=40), M("I_0", size=40), M("0", size=40)], 3,
                  "Pause and think. Two equal coherent sources, a path difference of half a wavelength. What is the intensity?",
                  "D, zero. Half a wavelength is a phase difference of pi, and cos squared of pi by two is zero. Two I nought is the trap: that is what you would get from two incoherent sources, which never interfere.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        d = self.callout("key", "Coherent sources emit light of the same frequency with a constant phase difference that does not change with time.", width=11, size=28)
        d.to_edge(UP, buff=0.8)
        with self.say("So why did the two torches show no stripes? The stripes only stay still if the phase difference at each point stays the same from moment to moment. That needs coherent sources: same frequency, and a constant phase difference."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        rng = np.random.default_rng(5)
        phase = ValueTracker(0.0)
        col = wl_rgb(600)
        scr = always_redraw(lambda: strip(4.6, -2.9, 0.3, 0.9, lambda y: col * np.cos(PI * y / 0.5 + phase.get_value() / 2) ** 2, n=70))
        ro = readout("phase difference:", lambda: np.degrees(phase.get_value()) % 360, "°", decimals=0, size=26, color=th.AMBER).move_to([-2.2, -0.2, 0])
        bulbs = VGroup(Dot([-5.0, 0.3, 0], color=ManimColor.from_rgb(col), radius=0.18), Dot([-5.0, -1.9, 0], color=ManimColor.from_rgb(col), radius=0.18))
        note = para("An ordinary lamp emits bursts lasting about 10⁻⁸ s, each with a random phase.", width=6.6, size=24, color=th.BODY).move_to([-1.4, -1.5, 0])
        with self.say("An ordinary lamp emits light in short bursts, each lasting about ten to the minus eight seconds, and each starting with a random phase. With two separate lamps, the phase difference between them reshuffles about a hundred million times a second."):
            self.add(scr)
            self.play(FadeIn(bulbs), FadeIn(scr), FadeIn(ro), FadeIn(note))
            for _ in range(10):
                phase.set_value(rng.uniform(0, TAU))
                self.wait(0.35)
        avg = strip(4.6, -2.9, 0.3, 0.9, lambda y: col * 0.5, n=20)
        eq = M(r"\overline{\cos\phi} = 0\ \Rightarrow\ I = I_1 + I_2", size=40, color=C_I).move_to([-1.4, -2.6, 0])
        with self.say("The fringes jump about far faster than any eye or detector can follow. On average, cos phi is zero, the interference term vanishes, and the intensities just add. A smooth, even glow. No fringes."):
            for _ in range(6):
                phase.set_value(rng.uniform(0, TAU))
                self.wait(0.25)
            self.remove(scr)
            self.add(avg)
            self.play(Write(eq))
        self.play(FadeOut(VGroup(d, bulbs, ro, note, avg, eq)))
        title = T("The trick: make both beams from ONE source", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        cards = VGroup()
        for h, b, c in [("Division of wavefront", "two parts of the same wavefront: Young's double slit, Fresnel's biprism, Lloyd's mirror", th.SKY),
                        ("Division of amplitude", "one beam partly reflected, partly transmitted: thin films, soap bubbles, oil on a wet Kathmandu road, Newton's rings", th.PINK)]:
            box = self.panel(5.8, 2.8)
            g = VGroup(T(h, size=28, color=c, weight="BOLD"), para(b, width=5.2, size=22, color=th.BODY)).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange(RIGHT, buff=0.35).next_to(title, DOWN, buff=0.5)
        laser = para("A laser is naturally coherent: that is why a laser pointer makes this experiment easy in a school lab.", width=10, size=24, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("The way round it is to take both beams from a single source. Then whatever random phase jump happens, happens in both beams at once, and cancels out of the phase difference. There are two ways. Division of wavefront: use two parts of the same wavefront, as in Young's double slit. Division of amplitude: split one beam by partial reflection, as in a soap bubble, or the rainbow colours of oil on a wet road. And lasers are naturally coherent, which makes all this easy."):
            self.play(FadeIn(title))
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            self.play(FadeIn(laser))
        self.play(FadeOut(VGroup(title, cards, laser)))
        self.quiz("Two sources are coherent if they have the same frequency and",
                  ["a constant phase difference", "zero phase difference", "the same amplitude only", "the same intensity only"], 0,
                  "Pause and think. Two sources are coherent if they have the same frequency and what else?",
                  "A, a constant phase difference. It does not have to be zero. It just must not change with time. Same amplitude helps the dark fringes go fully dark, but it is not what coherence means.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        t = clock(self, 1.0)
        Sx, sx, scx = -5.8, -3.0, 4.2
        d2 = 0.7
        S = np.array([Sx, 0, 0])
        S1, S2 = np.array([sx, d2, 0]), np.array([sx, -d2, 0])
        lam = 0.55
        col = wl_rgb(589)
        b1 = VGroup(Line([Sx + 0.4, 2.8, 0], [Sx + 0.4, 0.08, 0]), Line([Sx + 0.4, -0.08, 0], [Sx + 0.4, -2.8, 0])).set_stroke(th.BODY, 5)
        b2 = VGroup(Line([sx, 2.8, 0], [sx, d2 + 0.08, 0]), Line([sx, d2 - 0.08, 0], [sx, -d2 + 0.08, 0]), Line([sx, -d2 - 0.08, 0], [sx, -2.8, 0])).set_stroke(th.BODY, 5)
        lamp = Dot(S + LEFT * 0.4, color=ManimColor.from_rgb(col), radius=0.16)

        def fronts():
            g = VGroup()
            tt = t.get_value()
            ph = (tt * 0.6) % lam
            for k_ in range(6):
                r = ph + k_ * lam
                if Sx + 0.4 + r < sx:
                    g.add(Arc(radius=r, start_angle=-0.9, angle=1.8, arc_center=[Sx + 0.4, 0, 0], color=ManimColor.from_rgb(col), stroke_width=2))
            for P in (S1, S2):
                for k_ in range(14):
                    r = ph + k_ * lam
                    if r < 7.5:
                        g.add(Arc(radius=r, start_angle=-1.2, angle=2.4, arc_center=P, color=ManimColor.from_rgb(col), stroke_width=2, stroke_opacity=max(0.15, 0.8 - r / 9)))
            return g
        fr = always_redraw(fronts)
        D = scx - sx
        beta = lam * D / (2 * d2)
        scr = strip(scx + 0.4, -2.8, 2.8, 0.6, lambda y: col * np.cos(PI * y / beta) ** 2, n=100)
        labs = VGroup(M("S", size=30).next_to([Sx + 0.4, 0, 0], UP, buff=0.25).shift(RIGHT * 0.3), M("S_1", size=30).next_to(S1, UL, buff=0.08), M("S_2", size=30).next_to(S2, DL, buff=0.08),
                      T("screen", size=22, color=th.MUTED).next_to([scx + 0.4, 2.8, 0], UP, buff=0.1))
        with self.say("Here is Young's experiment. Light from a monochromatic source falls on a narrow slit S. The wavefront spreading from S reaches two more narrow slits, S one and S two, a small distance d apart."):
            self.play(FadeIn(lamp), Create(b1), Create(b2), FadeIn(labs[:3]))
            self.add(fr)
            self.play(FadeIn(fr))
            self.wait(1.5)
        with self.say("S one and S two are carved out of the same wavefront, so they are coherent. They act as two sources in step, and where their waves overlap on a screen, a distance D away, a steady pattern of bright and dark fringes appears."):
            self.play(FadeIn(scr), FadeIn(labs[3]))
            self.wait(2.5)
        self.play(FadeOut(VGroup(lamp, b1, b2, labs, scr)), FadeOut(fr))
        self.remove(fr, t)
        title = T("The path difference", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        A1, A2 = np.array([-5.2, 0.6, 0]), np.array([-5.2, -0.6, 0])
        sx2 = -0.6
        O = np.array([sx2, 0, 0])
        y = ValueTracker(1.6)
        P = lambda: np.array([sx2, y.get_value(), 0])
        geo = always_redraw(lambda: VGroup(Line(A1, P(), color=C_1, stroke_width=4), Line(A2, P(), color=C_2, stroke_width=4), Dot(P(), color=WHITE),
                                           M("P", size=30).next_to(P(), RIGHT, buff=0.1)))
        scrl = Line([sx2, -2.8, 0], [sx2, 2.8, 0], color=th.MUTED, stroke_width=4)
        mid = DashedLine([-5.2, 0, 0], O, color=th.FAINT)
        lb = VGroup(M("S_1", size=28).next_to(A1, LEFT, buff=0.1), M("S_2", size=28).next_to(A2, LEFT, buff=0.1), M("O", size=28).next_to(O, RIGHT, buff=0.1),
                    BraceBetweenPoints(A1, A2, LEFT, color=th.MUTED), BraceBetweenPoints([-5.2, -1.4, 0], [sx2, -1.4, 0], DOWN, color=th.MUTED))
        lb.add(M("d", size=28).next_to(lb[3], LEFT, buff=0.05), M("D", size=28).next_to(lb[4], DOWN, buff=0.05))
        yb = always_redraw(lambda: VGroup(Line([sx2 + 0.5, 0, 0], [sx2 + 0.5, y.get_value(), 0], color=th.AMBER, stroke_width=3), M("y", size=28, color=th.AMBER).move_to([sx2 + 0.75, y.get_value() / 2, 0])))
        with self.say("Now the geometry. Let O be the point on the screen straight opposite the middle of the slits, and P a point at height y above it. Light from S two travels further to reach P than light from S one."):
            self.play(FadeIn(title), Create(scrl), Create(mid), FadeIn(lb))
            self.add(geo, yb)
            self.play(FadeIn(geo), FadeIn(yb))
            self.play(y.animate.set_value(2.2), run_time=1.5)
        L = VGroup(VGroup(M(r"(S_2P)^{2} = D^{2} + \left(y + \tfrac{d}{2}\right)^{2}", size=30), M(r"(S_1P)^{2} = D^{2} + \left(y - \tfrac{d}{2}\right)^{2}", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
                   M(r"(S_2P)^{2} - (S_1P)^{2} = 2yd", size=32), M(r"(S_2P - S_1P)(S_2P + S_1P) = 2yd", size=32),
                   M(r"S_2P + S_1P \approx 2D", size=32), M(r"\Delta = S_2P - S_1P = \frac{yd}{D}", size=46, color=C_I)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        L.scale_to_fit_width(min(L.width, 5.4)).move_to([3.7, -0.3, 0])
        says = ["By Pythagoras, S two P squared is D squared plus y plus d by two, all squared. And S one P squared is D squared plus y minus d by two, squared.",
                "Subtract, and almost everything cancels, leaving two y d.",
                "Factorise the left side as a difference of two squares.",
                "In practice D is about a metre, while y and d are less than a millimetre. Both paths are very nearly D, so their sum is about two D.",
                "So the path difference is y d over D. Remember this one line: every result in the unit follows from it."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(Circumscribe(L[-1], color=C_I))
        self.play(FadeOut(VGroup(title, scrl, mid, lb, L)), FadeOut(geo), FadeOut(yb))
        self.remove(geo, yb)

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("Where the fringes fall", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        L = VGroup(M(r"\text{bright: } \frac{y_nd}{D} = n\lambda\ \Rightarrow\ y_n = \frac{n\lambda D}{d}", size=40, color=C_I),
                   M(r"\text{dark: } \frac{y_nd}{D} = (2n - 1)\frac{\lambda}{2}\ \Rightarrow\ y_n = \frac{(2n - 1)\lambda D}{2d}", size=40, color=th.SKY),
                   M(r"\beta = y_{n+1} - y_n = \frac{(n + 1)\lambda D}{d} - \frac{n\lambda D}{d}", size=40),
                   M(r"\beta = \frac{\lambda D}{d}", size=72, color=th.INK)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.35)
        says = ["Bright fringes need a path difference of a whole number of wavelengths. So y n d over D equals n lambda, and the n th bright fringe is at n lambda D over d.",
                "Dark fringes need an odd number of half wavelengths. The n th dark fringe is at two n minus one, lambda D, over two d.",
                "The fringe width, beta, is the distance between two neighbouring bright fringes: y n plus one minus y n.",
                "Everything cancels except lambda D over d. Do the same with the dark fringes, and you get the same answer. So the fringes are equally spaced, and equally bright. Turn it round, and lambda equals beta d over D: that is how Young measured the wavelength of light."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        box = SurroundingRectangle(L[3], color=C_I, buff=0.2, corner_radius=0.1)
        self.sfx("impact", gain=-12)
        self.play(Create(box))
        self.play(FadeOut(VGroup(title, L, box)))
        self.quiz("In Young's double slit experiment the fringe width is",
                  [M(r"\lambda d/D", size=40), M(r"\lambda D/d", size=40), M(r"Dd/\lambda", size=40), M(r"\lambda/Dd", size=40)], 1,
                  "Quick check before we look at the pattern. Which is the fringe width? Pause and think.",
                  "B, lambda D over d. A sanity check helps: a far screen spreads the fringes, so D must be on top; slits further apart squeeze them, so d must be underneath.")
        col = wl_rgb(600)
        beta = 1.1
        scr = strip(-5.4, -2.9, 2.9, 0.8, lambda y: col * np.cos(PI * y / beta) ** 2, n=120)
        ax = Axes(x_range=[0, 4.4, 1], y_range=[-2.9, 2.9, 1], x_length=3.0, y_length=5.8, tips=False, axis_config={"color": th.FAINT, "include_ticks": False}).move_to([-3.2, 0, 0])
        Ic = ax.plot_parametric_curve(lambda yy: np.array([4 * np.cos(PI * yy / beta) ** 2, yy, 0]), t_range=[-2.9, 2.9], color=C_I, stroke_width=4)
        tags = VGroup(*[T(s, size=20, color=C_I).next_to([-4.9, n * beta, 0], RIGHT, buff=0.1).shift(RIGHT * 2.9) for n, s in zip((-2, -1, 0, 1, 2), ("n = 2", "n = 1", "central", "n = 1", "n = 2"))])
        yP = ValueTracker(0.0)
        mark = always_redraw(lambda: Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI / 2).move_to([-4.85, yP.get_value(), 0]))
        ro = VGroup(readout("Δ =", lambda: yP.get_value() / beta, "λ", decimals=2, size=30, color=C_I),
                    readout("I =", lambda: 4 * np.cos(PI * yP.get_value() / beta) ** 2, "I₀", decimals=2, size=30, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 1.4, 0])
        eqI = M(r"I = 4I_0\cos^{2}\left(\frac{\pi y d}{\lambda D}\right)", size=40, color=C_I).move_to([3.4, -0.6, 0])
        with self.say("Here is the pattern on the screen, with its intensity graph. The central fringe, at O, has zero path difference. Move up the screen, and the path difference grows steadily."):
            self.play(FadeIn(scr), Create(ax), Create(Ic))
            self.add(mark)
            self.play(FadeIn(ro), FadeIn(tags[2]))
            self.play(yP.animate.set_value(beta / 2), run_time=1.5)
        with self.say("Half a wavelength: dark. One whole wavelength: the first bright fringe. One and a half: dark again. Two wavelengths: the second bright fringe. Every fringe width adds exactly one wavelength of path difference. The intensity follows four I nought cos squared of pi y d over lambda D."):
            self.play(yP.animate.set_value(beta), FadeIn(tags[3]), run_time=1.5)
            self.play(yP.animate.set_value(2 * beta), FadeIn(tags[4]), run_time=2.0)
            self.play(Write(eqI))
            self.play(yP.animate.set_value(-2 * beta), FadeIn(tags[0]), FadeIn(tags[1]), run_time=3.0)
        self.play(FadeOut(VGroup(scr, ax, Ic, tags, ro, eqI)), FadeOut(mark))
        self.remove(mark)
        example(self, "In Young's experiment the slits are 0.50 mm apart, the screen is 1.5 m away and λ = 600 nm. Find the fringe width and the distances of the 3rd bright and 3rd dark fringes from the centre.",
                [r"\beta = \frac{\lambda D}{d} = \frac{600\times10^{-9}\times 1.5}{0.50\times10^{-3}} = 1.8\times10^{-3}\ \text{m} = 1.8\ \text{mm}",
                 r"\text{3rd bright: } y_3 = 3\beta = 5.4\ \text{mm}",
                 r"\text{3rd dark: } \Delta = (2\times3 - 1)\frac{\lambda}{2} = 2.5\lambda\ \Rightarrow\ y = 2.5\beta = 4.5\ \text{mm}"],
                ["Worked example. Slits half a millimetre apart, a screen one and a half metres away, light of six hundred nanometres. Find the fringe width, and the positions of the third bright and third dark fringes.",
                 "Beta is lambda D over d: six hundred times ten to the minus nine, times one point five, over zero point five times ten to the minus three. One point eight millimetres.",
                 "The third bright fringe is three fringe widths out: five point four millimetres.",
                 "The third dark fringe has a path difference of five half wavelengths, two and a half lambda, so it sits at two and a half beta: four point five millimetres. Careful: it is not three beta."], size=38)
        example(self, "The distance between the 2nd and 7th bright fringes on the same side is 9.0 mm. With d = 0.50 mm and D = 1.5 m, find the wavelength.",
                [r"7 - 2 = 5\ \text{fringe widths}:\ 5\beta = 9.0\ \text{mm}\ \Rightarrow\ \beta = 1.8\ \text{mm}",
                 r"\lambda = \frac{\beta d}{D} = \frac{1.8\times10^{-3}\times 0.50\times10^{-3}}{1.5} = 6.0\times10^{-7}\ \text{m} = 600\ \text{nm}"],
                ["Now backwards. The second and seventh bright fringes on the same side are nine millimetres apart. Find the wavelength.",
                 "Between the second and seventh there are five fringe widths, so beta is one point eight millimetres.",
                 "Lambda is beta d over D: one point eight times ten to the minus three, times zero point five times ten to the minus three, over one point five. Six times ten to the minus seven metres, six hundred nanometres. Orange red light."], size=40)
        example(self, "In a double slit experiment d = 0.28 mm, D = 1.4 m and λ = 600 nm. Find the fringe width and the distance of the 4th dark fringe from the central bright fringe.",
                [r"\beta = \frac{600\times10^{-9}\times 1.4}{0.28\times10^{-3}} = 3.0\times10^{-3}\ \text{m} = 3.0\ \text{mm}",
                 r"y = \frac{(2\times4 - 1)\lambda D}{2d} = 3.5\beta = 10.5\ \text{mm}"],
                ["One more, from the short questions. Slits zero point two eight millimetres apart, screen one point four metres away, six hundred nanometres. Find beta, and the fourth dark fringe.",
                 "Beta is six hundred nanometres times one point four, over zero point two eight millimetres: three millimetres.",
                 "The fourth dark fringe is at seven halves of beta: ten point five millimetres from the centre."], size=40)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        lam = ValueTracker(600.0)
        dd = ValueTracker(0.5)
        DD = ValueTracker(1.5)
        beta = lambda: lam.get_value() * 1e-9 * DD.get_value() / (dd.get_value() * 1e-3) * 1e3
        scale = 0.55
        scr = always_redraw(lambda: strip(-3.6, -2.9, 2.9, 2.2, lambda y: wl_rgb(lam.get_value()) * np.cos(PI * (y / scale) / beta()) ** 2, n=130))
        ro = VGroup(readout("λ =", lambda: lam.get_value(), "nm", decimals=0, size=28, color=th.INK), readout("d =", lambda: dd.get_value(), "mm", decimals=2, size=28),
                    readout("D =", lambda: DD.get_value(), "m", decimals=2, size=28), readout("β =", beta, "mm", decimals=2, size=34, color=C_I)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 1.4, 0])
        eq = M(r"\beta = \frac{\lambda D}{d}", size=56).move_to([3.0, -1.4, 0])
        with self.say("Now let us play with the fringe width formula, beta equals lambda D over d. Here is the pattern for six hundred nanometre light, with d half a millimetre and D one and a half metres."):
            self.add(scr)
            self.play(FadeIn(scr), FadeIn(ro), Write(eq))
        with self.say("Switch to longer, redder light, and the fringes spread out. Bluer light, and they squeeze together. Beta is proportional to lambda."):
            self.play(lam.animate.set_value(700), run_time=2)
            self.play(lam.animate.set_value(440), run_time=2.5)
            self.play(lam.animate.set_value(600), run_time=1.5)
        with self.say("Move the slits further apart, and the fringes get closer. Move the screen further back, and they spread out."):
            self.play(dd.animate.set_value(1.0), run_time=2)
            self.play(dd.animate.set_value(0.5), run_time=1)
            self.play(DD.animate.set_value(3.0), run_time=2)
            self.play(DD.animate.set_value(1.5), run_time=1)
        water = T("in water, n = 4/3: λ → λ/n, so β → β/n", size=26, color=th.SKY).move_to([3.0, -2.6, 0])
        with self.say("Put the whole apparatus under water, of index four thirds. The wavelength inside shrinks to lambda over n, so the fringes shrink by the same factor."):
            self.play(FadeIn(water))
            self.play(lam.animate.set_value(450), run_time=2)
            self.play(lam.animate.set_value(600), run_time=1)
        self.play(FadeOut(VGroup(ro, eq, water)), FadeOut(scr))
        self.remove(scr)
        one = strip(-3.6, -2.9, 2.9, 2.2, lambda y: wl_rgb(600) * 0.55 * np.exp(-(y / 4.5) ** 2), n=40)
        ol = para("Cover one slit: no second wave, no interference. Just even illumination.", width=5.4, size=26, color=th.BODY).move_to([3.0, 0.8, 0])
        with self.say("Cover one slit, and the fringes vanish. With no second wave to interfere with, you just get an even patch of light."):
            self.play(FadeIn(one), FadeIn(ol))
        self.play(FadeOut(VGroup(one, ol)))
        bw = 1.8 / scale

        def white(y):
            s = np.zeros(3)
            for nm in np.linspace(410, 690, 15):
                s += wl_rgb(nm) * np.cos(PI * (y / scale) / (bw * nm / 600)) ** 2
            return s / 15 * 1.6
        ws = strip(-3.6, -2.9, 2.9, 2.2, white, n=150)
        wl_ = para("White light: a white central fringe, a few coloured fringes with violet nearest the centre, then a blur.", width=5.4, size=26, color=th.BODY).move_to([3.0, 0.8, 0])
        with self.say("Finally, use white light. At the centre, the path difference is zero for every colour, so every colour is bright there, and the central fringe is white. Away from the centre, each colour has its own fringe width, violet the narrowest and red the widest. So you see a few coloured fringes, violet edges nearest the centre, before they overlap into a blur of white."):
            self.play(FadeIn(ws), FadeIn(wl_))
            self.wait(1)
        self.play(FadeOut(VGroup(ws, wl_)))
        self.quiz("In white-light interference, the central fringe is",
                  ["violet", "red", "white", "dark"], 2,
                  "Pause and think. With white light, what colour is the central fringe?",
                  "C, white. At the centre the path difference is zero for every wavelength, so every colour is bright together. Dark is the trap: the centre of Young's pattern is always bright, never dark.")
        self.tip("Central fringe is always bright (Δ = 0 for every λ). The nth dark fringe sits at (n − ½)β, not nβ. In a medium, use λ/n.",
                 "Three quick exam habits. The central fringe is always bright, because the path difference there is zero for every wavelength. The n th dark fringe sits at n minus a half, times beta, not n beta. And inside a medium, always use lambda over n.", state="wink")
        self.quiz("If the whole double-slit apparatus is immersed in water, the fringe width",
                  ["increases", "decreases", "is unchanged", "becomes zero"], 1,
                  "Pause and think. Immerse the whole double slit apparatus in water. What happens to the fringe width?",
                  "B, it decreases. The wavelength in water is lambda over n, so beta becomes beta over n. The frequency does not change, but the wavelength does, and beta depends on wavelength.")
        example(self, "The apparatus of the first example (β = 1.8 mm) is immersed in water of index 4/3. Find the new fringe width. What would β become in air if D were doubled and d halved?",
                [r"\beta_w = \frac{\beta}{n} = \frac{1.8}{4/3} = 1.8\times\frac{3}{4} = 1.35\ \text{mm}",
                 r"D \to 2D,\ d \to \tfrac{d}{2}:\quad \beta \to 4\beta = 7.2\ \text{mm}"],
                ["Worked example. Take our first set up, with a fringe width of one point eight millimetres, and immerse it in water of index four thirds. Then, back in air, double D and halve d.",
                 "In water, beta becomes beta over n: one point eight times three quarters, one point three five millimetres.",
                 "Doubling D doubles beta, and halving d doubles it again: four times, seven point two millimetres."], size=42)
        example(self, "Light of 589 nm falls on slits 1.0 mm apart; the screen is 1.0 m away. Find β, the distance between the 3rd bright fringe on one side and the 3rd dark fringe on the other, and β for 442 nm light.",
                [r"\beta = \frac{589\times10^{-9}\times 1.0}{1.0\times10^{-3}} = 0.589\ \text{mm}",
                 r"3\beta = 1.767\ \text{mm},\quad 2.5\beta = 1.4725\ \text{mm}",
                 r"\text{opposite sides: } 1.767 + 1.4725 = 3.24\ \text{mm}",
                 r"\beta' = \frac{442\times10^{-9}\times 1.0}{1.0\times10^{-3}} = 0.442\ \text{mm}"],
                ["A full long question to finish. Sodium light of five hundred and eighty nine nanometres, slits one millimetre apart, screen one metre away. Find beta, then the distance between the third bright fringe on one side and the third dark fringe on the other side, then beta for blue light of four hundred and forty two nanometres.",
                 "Beta is five eight nine nanometres times one metre over one millimetre: zero point five eight nine millimetres.",
                 "The third bright fringe is at three beta, one point seven six seven millimetres. The third dark fringe is at two and a half beta, one point four seven two five.",
                 "They are on opposite sides of the centre, so add them: three point two four millimetres.",
                 "And for blue light, beta is zero point four four two millimetres. Narrower fringes, just as the slider showed."], size=38)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi,\qquad \phi = \frac{2\pi}{\lambda}\Delta", size=34),
            M(r"\text{bright: } \Delta = n\lambda;\ \ \text{dark: } \Delta = (2n - 1)\tfrac{\lambda}{2};\ \ I = 4I_0\cos^{2}\tfrac{\phi}{2}", size=34),
            "Coherent sources: same frequency, constant phase difference; made from one source by dividing the wavefront or the amplitude.",
            M(r"\text{Young: } \Delta = \frac{yd}{D},\ \ y_n = \frac{n\lambda D}{d},\ \ \text{dark at } \frac{(2n - 1)\lambda D}{2d}", size=34),
            M(r"\beta = \frac{\lambda D}{d};\ \ \text{in a medium } \beta/n;\ \ \text{white light: white centre}", size=34),
            "Energy is redistributed, not destroyed: the average intensity is 2I₀.",
        ], "Let us recap. Superposed light waves give I one plus I two plus two root I one I two cos phi. A path difference of n lambda gives a bright point, an odd number of half wavelengths a dark one. Only coherent sources, with a constant phase difference, give steady fringes, so we make them from one source. In Young's experiment the path difference is y d over D, and the fringe width is lambda D over d. And interference never destroys energy; it only moves it around.")
        self.outro("That is interference. Next, light bends around the edges of obstacles and spreads out from single slits, in Diffraction. See you there, on NEBians.")
