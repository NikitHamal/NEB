import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import clock, curve, example, neby_in, neby_out, readout, strip, wl_rgb  # noqa: E402

C_I, C_A, C_G = th.AMBER, th.SKY, th.MINT


def sinc2(x):
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    m = np.abs(x) > 1e-9
    out[m] = (np.sin(x[m]) / x[m]) ** 2
    return out


def s2(x):
    return float(sinc2(np.array([x]))[0])


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 12
    TITLE = "Diffraction"
    SUBTITLE = "Light bends round corners"
    SECTIONS = ["What diffraction is", "Single-slit minima", "The central maximum", "Diffraction vs interference",
                "Diffraction grating", "Resolving power"]
    NEXT = "Unit 13 · Polarization"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ spreading wavefronts after a gap
    def gap_waves(self, t, xg, a, lam, color, y0=0.0, maxr=8.0, per_speed=1.0):
        """Plane waves arrive from the left at a gap of width a (scene units) at x = xg and spread with half-angle ~ asin(lam/a)."""
        phi = np.arcsin(min(1.0, lam / a)) if a > 0 else PI / 2

        def mk():
            g = VGroup()
            tt = t.get_value() * per_speed
            ph = tt % lam
            for k in range(30):
                x = xg - 6 + ph + k * lam
                if x < xg:
                    if x > -6.8:
                        g.add(Line([x, y0 + 2.6, 0], [x, y0 - 2.6, 0], color=color, stroke_width=2.5))
                else:
                    r = x - xg
                    if r > maxr:
                        break
                    op = max(0.15, 1 - r / maxr)
                    top, bot = np.array([xg, y0 + a / 2, 0]), np.array([xg, y0 - a / 2, 0])
                    g.add(Line(top + RIGHT * r, bot + RIGHT * r, color=color, stroke_width=2.5, stroke_opacity=op),
                          Arc(radius=max(r, 0.01), start_angle=0, angle=phi, arc_center=top, color=color, stroke_width=2.5, stroke_opacity=op),
                          Arc(radius=max(r, 0.01), start_angle=-phi, angle=phi, arc_center=bot, color=color, stroke_width=2.5, stroke_opacity=op))
            return g
        return always_redraw(mk)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        t = clock(self, 1.0)
        wall = VGroup(Line([0, 3.2, 0], [0, 0.6, 0]), Line([0, -0.6, 0], [0, -3.2, 0])).set_stroke(th.BODY, 10)
        lab = T("an open doorway", size=24, color=th.MUTED).next_to([0, 0.6, 0], UR, buff=0.2)
        snd = self.gap_waves(t, 0.0, 1.2, 1.4, th.PINK, maxr=6.5)
        who = VGroup(Circle(radius=0.25, fill_color="#E9B48A", fill_opacity=1, stroke_width=0), T("you", size=22).shift(DOWN * 0.45)).move_to([4.0, 2.3, 0])
        with self.say("You can hear somebody talking in the next room, round the edge of the doorway, even though you cannot see them. Sound, with a wavelength of about a metre, spreads round the edge into the shadow."):
            self.play(Create(wall), FadeIn(lab), FadeIn(who))
            self.add(snd)
            self.play(FadeIn(snd))
            self.wait(3)
        self.play(FadeOut(snd))
        self.remove(snd)
        light = self.gap_waves(t, 0.0, 1.2, 0.12, th.AMBER, maxr=6.5, per_speed=0.3)
        with self.say("Light through the same doorway goes almost straight. Its wavelength is two million times smaller than the gap, so the spreading is far too small to see. That is why you cannot see round corners."):
            self.add(light)
            self.play(FadeIn(light))
            self.wait(3)
        self.play(FadeOut(VGroup(wall, lab, who)), FadeOut(light))
        self.remove(light)
        a = ValueTracker(1.0)
        col = wl_rgb(600)
        bar = always_redraw(lambda: VGroup(Line([-3.0, 3.0, 0], [-3.0, a.get_value() * 0.4, 0]), Line([-3.0, -a.get_value() * 0.4, 0], [-3.0, -3.0, 0])).set_stroke(th.BODY, 8))
        scr = always_redraw(lambda: strip(4.6, -3.0, 3.0, 0.9, lambda y: col * min(1.0, 1.3 / max(a.get_value(), 0.15) * 0.25) * s2(PI * y * a.get_value() / 1.6), n=90))
        beam = always_redraw(lambda: Polygon([-6.5, 0.5, 0], [-3.0, a.get_value() * 0.4, 0], [-3.0, -a.get_value() * 0.4, 0], [-6.5, -0.5, 0], stroke_width=0, fill_color=ManimColor.from_rgb(col), fill_opacity=0.25))
        ro = readout("slit width:", lambda: 0.2 * a.get_value(), "mm", decimals=2, size=26).move_to([0.8, 2.9, 0])
        with self.say("But make the gap really tiny, a fraction of a millimetre, and something strange happens. Squeeze the slit narrower, and the patch of light on the screen gets wider, with dark and bright bands at its edges."):
            self.add(beam, bar, scr)
            self.play(FadeIn(beam), FadeIn(bar), FadeIn(scr), FadeIn(ro))
            self.play(a.animate.set_value(0.3), run_time=4)
        nb = neby_in(self, "surprised", corner=DL)
        q = T("Narrower slit, WIDER patch of light?", size=32, color=th.AMBER, weight="BOLD").move_to([0.8, -2.9, 0])
        with self.say("A narrower slit gives a wider patch of light. Ray optics says the opposite. This is diffraction, and by the end of the lesson you will predict the width of that patch exactly."):
            self.play(FadeIn(q))
            self.play(a.animate.set_value(0.6), run_time=1.5)
            self.play(a.animate.set_value(0.3), run_time=1.5)
        self.play(FadeOut(VGroup(q, ro)), FadeOut(beam), FadeOut(bar), FadeOut(scr))
        self.remove(beam, bar, scr, t)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 12: Diffraction. Light bends round obstacles and spreads after passing through narrow openings. It is Huygens' wavelets interfering with one another. It limits every telescope and microscope ever built, and it powers the diffraction grating, our most accurate way to measure wavelength."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. What diffraction is, the minima of a single slit, the central maximum and its intensity, how diffraction differs from interference, the diffraction grating, and the resolving power of telescopes and microscopes.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        d = self.callout("key", "Diffraction: the bending of waves round the edges of an obstacle or aperture, and the redistribution of intensity that follows, when the size of the obstacle or aperture is comparable with the wavelength.", width=11.5, size=26)
        d.to_edge(UP, buff=0.8)
        with self.say("Diffraction is the bending of waves round the edges of an obstacle or an opening, and the redistribution of intensity that follows. It only becomes noticeable when the size of the opening is comparable with the wavelength."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        self.play(FadeOut(d))
        t = clock(self, 1.0)
        aw = ValueTracker(4.0)
        lam = 0.55

        def mk():
            a = aw.get_value()
            phi = np.arcsin(min(1.0, lam / a))
            g = VGroup()
            ph = (t.get_value() * 0.6) % lam
            for k in range(30):
                x = -7.5 + ph + k * lam
                if x < -1.5:
                    if x > -6.8:
                        g.add(Line([x, 2.6, 0], [x, -2.6, 0], color=th.SKY, stroke_width=2.5))
                else:
                    r = x + 1.5
                    if r > 7.5:
                        break
                    op = max(0.15, 1 - r / 7.5)
                    top, bot = np.array([-1.5, a / 2, 0]), np.array([-1.5, -a / 2, 0])
                    g.add(Line(top + RIGHT * r, bot + RIGHT * r, color=th.SKY, stroke_width=2.5, stroke_opacity=op),
                          Arc(radius=max(r, 0.01), start_angle=0, angle=phi, arc_center=top, color=th.SKY, stroke_width=2.5, stroke_opacity=op),
                          Arc(radius=max(r, 0.01), start_angle=-phi, angle=phi, arc_center=bot, color=th.SKY, stroke_width=2.5, stroke_opacity=op))
            return g
        wv = always_redraw(mk)
        walls = always_redraw(lambda: VGroup(Line([-1.5, 3.0, 0], [-1.5, aw.get_value() / 2, 0]), Line([-1.5, -aw.get_value() / 2, 0], [-1.5, -3.0, 0])).set_stroke(th.BODY, 8))
        ro = readout("gap / λ =", lambda: aw.get_value() / lam, "", decimals=1, size=28, color=th.AMBER).move_to([4.4, 2.8, 0])
        with self.say("Watch plane waves arriving at a gap. When the gap is many wavelengths wide, the waves pass almost straight through, with just a little bending at the edges."):
            self.add(wv, walls)
            self.play(FadeIn(wv), FadeIn(walls), FadeIn(ro))
            self.wait(2.5)
        with self.say("Narrow the gap down towards one wavelength. Now the waves fan out into the shadow, almost in circles. The gap acts like a new source. That is Huygens' principle at work: with only a few points across the gap sending out wavelets, there is nothing to keep the front flat."):
            self.play(aw.animate.set_value(0.7), run_time=4)
            self.wait(2)
        self.play(FadeOut(ro), FadeOut(wv), FadeOut(walls))
        self.remove(wv, walls, t)
        title = T("Two kinds of diffraction", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        cards = VGroup()
        for i, (h, rows, c) in enumerate([("Fresnel", ["source and screen at finite distances", "spherical or cylindrical wavefronts", "no lenses; hard mathematics"], th.PINK),
                                           ("Fraunhofer", ["source and screen effectively at infinity", "plane wavefronts", "two lenses; simple mathematics"], th.SKY)]):
            box = self.panel(5.8, 3.4)
            g = VGroup(T(h, size=30, color=c, weight="BOLD"), *[T("• " + r_, size=22, color=th.BODY) for r_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange(RIGHT, buff=0.35).next_to(title, DOWN, buff=0.4)
        note = para("Everything in this unit is Fraunhofer: parallel light in, parallel light out, focused by a lens.", width=10, size=24, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("There are two classes. In Fresnel diffraction, the source and screen are at finite distances, the wavefronts are curved, and the mathematics is hard. In Fraunhofer diffraction, source and screen are effectively at infinity, the wavefronts are plane, and lenses are used. Everything in this unit is Fraunhofer: parallel light in, parallel light out, brought to a focus by a lens."):
            self.play(FadeIn(title))
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(title, cards, note)))
        self.quiz("Diffraction is most easily observed when the size of the aperture is",
                  ["much larger than λ", "comparable with λ", "exactly zero", "infinite"], 1,
                  "Pause and think. When is diffraction easiest to see?",
                  "B, when the aperture is comparable with the wavelength. Much larger, and the waves go almost straight, which is why ray optics works for windows and doors with light.")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Fraunhofer diffraction at a single slit", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        xs = -2.6
        a = 2.4
        A, B = np.array([xs, a / 2, 0]), np.array([xs, -a / 2, 0])
        Mid = np.array([xs, 0, 0])
        walls = VGroup(Line([xs, 3.0, 0], A), Line(B, [xs, -3.0, 0])).set_stroke(th.BODY, 8)
        inc = VGroup(*[Arrow([-6.4, y, 0], [xs - 0.1, y, 0], buff=0, color=th.SKY, stroke_width=3, max_tip_length_to_length_ratio=0.06) for y in np.linspace(-1.0, 1.0, 5)])
        th_ = ValueTracker(0.35)
        L = 4.2

        def rays():
            ang = th_.get_value()
            dvec = np.array([np.cos(ang), np.sin(ang), 0])
            g = VGroup()
            for y in np.linspace(a / 2, -a / 2, 7):
                p = np.array([xs, y, 0])
                g.add(Line(p, p + dvec * L, color=th.AMBER, stroke_width=2.5))
            foot = B + dvec * np.dot(A - B, dvec)
            g.add(DashedLine(A, foot, color=WHITE, stroke_width=2), Line(B, foot, color=th.CORAL, stroke_width=6))
            return g
        rg = always_redraw(rays)
        labs = VGroup(M("A", size=30).next_to(A, UL, buff=0.06), M("B", size=30).next_to(B, DL, buff=0.06), BraceBetweenPoints(A, B, LEFT, color=th.MUTED))
        labs.add(M("a", size=30).next_to(labs[2], LEFT, buff=0.05))
        dl = always_redraw(lambda: M(r"a\sin\theta", size=30, color=th.CORAL).next_to(B + np.array([np.cos(th_.get_value()), np.sin(th_.get_value()), 0]) * a * np.sin(th_.get_value()) * 0.5, DR, buff=0.12))
        with self.say("A plane wavefront of wavelength lambda falls on a slit A B of width a. By Huygens, every point across the slit sends out secondary wavelets. Pick the ones that leave at some angle theta. A lens will bring them all to one point P on the screen."):
            self.play(FadeIn(title), Create(walls), FadeIn(labs))
            self.play(LaggedStart(*[GrowArrow(r) for r in inc], lag_ratio=0.1))
            self.add(rg)
            self.play(FadeIn(rg))
        with self.say("Drop a perpendicular from A onto the ray from B. The wavelet from the bottom edge travels further than the one from the top, by a sine theta. That red length."):
            self.add(dl)
            self.play(FadeIn(dl))
            self.play(th_.animate.set_value(0.55), run_time=2)
        self.play(FadeOut(title))
        L1 = VGroup(M(r"\text{split into halves AM, MB: pair points } \tfrac{a}{2} \text{ apart}", size=32),
                    M(r"\frac{a}{2}\sin\theta = \frac{\lambda}{2}\ \Rightarrow\ a\sin\theta = \lambda:\ \text{every pair cancels, P dark}", size=32),
                    M(r"4\ \text{strips: } a\sin\theta = 2\lambda,\quad 6\ \text{strips: } a\sin\theta = 3\lambda", size=32),
                    M(r"\text{minima: } a\sin\theta = n\lambda,\quad n = \pm1, \pm2, \ldots", size=42, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        L1.scale_to_fit_width(min(L1.width, 8.0)).move_to([2.4, 0.2, 0])
        halves = VGroup(Line(A + RIGHT * 0.15, Mid + RIGHT * 0.15, color=th.SKY, stroke_width=10), Line(Mid + RIGHT * 0.15, B + RIGHT * 0.15, color=th.PINK, stroke_width=10))
        pairs = VGroup(*[VGroup(Dot([xs, y, 0], color=th.SKY, radius=0.08), Dot([xs, y - a / 2, 0], color=th.PINK, radius=0.08)) for y in np.linspace(a / 2 - 0.1, 0.1, 4)])
        self.play(VGroup(walls, labs, inc).animate.shift(LEFT * 1.6), rg.animate.shift(LEFT * 1.6), dl.animate.shift(LEFT * 1.6))
        self.remove(rg, dl)
        for m in (A, B, Mid):
            pass
        xs2 = xs - 1.6
        halves.shift(LEFT * 1.6)
        pairs.shift(LEFT * 1.6)
        with self.say("Now the clever argument. Split the slit into two halves, A M and M B. Pair each point in the top half with the point exactly a by two below it, in the bottom half."):
            self.play(Create(halves))
            self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.2))
            self.play(Write(L1[0]))
        with self.say("Each pair has a path difference of a by two sine theta. If that is half a wavelength, the two wavelets of every pair cancel. Every wavelet from the top half is wiped out by its partner from the bottom half, and P is dark. That happens when a sine theta equals lambda."):
            self.play(Write(L1[1]))
            self.play(*[Indicate(p, color=WHITE) for p in pairs])
        with self.say("Split the slit into four strips instead, and pair neighbouring strips: darkness again when a sine theta is two lambda. Six strips give three lambda. So the minima are at a sine theta equals n lambda, for n equal to plus or minus one, two, three."):
            self.play(Write(L1[2]))
            self.sfx("impact", gain=-12)
            self.play(Write(L1[3]))
        note = T("n = 0 is excluded: at θ = 0 every wavelet arrives in step, the brightest point.", size=22, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("Notice that n equals zero is not allowed. Straight ahead, at theta equals zero, every wavelet arrives in step, and the centre is the brightest point of all."):
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(walls, labs, inc, halves, pairs, L1, note)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        a = ValueTracker(1.0)
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 1.1, 0.5], x_length=8.0, y_length=3.0, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-0.6, 0.4, 0])
        Ic = always_redraw(lambda: ax.plot(lambda u: s2(PI * u * a.get_value()), x_range=[-3.2, 3.2, 0.01], color=C_I, stroke_width=4))
        col = wl_rgb(600)
        scr = always_redraw(lambda: VGroup(*[Rectangle(width=8.0 / 120 * 1.03, height=0.8, stroke_width=0, fill_color=ManimColor.from_rgb(np.clip(col * s2(PI * u * a.get_value()) ** 0.6, 0, 1)), fill_opacity=1).move_to([-0.6 + 8.0 * (u / 6.4), -1.9, 0])
                                           for u in np.linspace(-3.2, 3.2, 120)]))
        eq = M(r"I = I_0\left(\frac{\sin\beta}{\beta}\right)^{2},\quad \beta = \frac{\pi a\sin\theta}{\lambda}", size=36).move_to([0, 2.7, 0])
        xl = M(r"\sin\theta", size=28).next_to(ax.x_axis, RIGHT, buff=0.1)
        with self.say("Here is the full pattern. The intensity follows I equals I nought, sine beta over beta, all squared, where beta is pi a sine theta over lambda. A broad, bright central maximum, and on each side much weaker secondary maxima."):
            self.play(Write(eq), Create(ax), FadeIn(xl))
            self.add(Ic, scr)
            self.play(FadeIn(Ic), FadeIn(scr))
        tags = VGroup(T("4.7 %", size=22, color=th.MUTED).move_to(ax.c2p(1.43, 0.17)), T("1.7 %", size=22, color=th.MUTED).move_to(ax.c2p(2.46, 0.12)))
        with self.say("The secondary maxima lie roughly halfway between the minima, near a sine theta equals n plus a half, lambda. And they are faint. The first is only about four point seven percent of the central intensity, the second about one point seven."):
            self.play(FadeIn(tags))
        self.play(FadeOut(tags))
        mk = always_redraw(lambda: VGroup(DashedLine(ax.c2p(-1 / a.get_value(), 0), ax.c2p(-1 / a.get_value(), 1.05), color=th.CORAL),
                                          DashedLine(ax.c2p(1 / a.get_value(), 0), ax.c2p(1 / a.get_value(), 1.05), color=th.CORAL)) if 1 / a.get_value() < 3.2 else VGroup())
        ro = readout("slit width a =", lambda: 0.2 * a.get_value(), "mm", decimals=2, size=26).move_to([5.0, 1.0, 0])
        ws = VGroup(M(r"\sin\theta_1 = \pm\frac{\lambda}{a}", size=34), M(r"2\theta_1 = \frac{2\lambda}{a}", size=34), M(r"w = \frac{2\lambda D}{a}", size=44, color=C_I)).arrange(DOWN, buff=0.25).move_to([5.1, -1.2, 0])
        with self.say("The first minima on each side are at sine theta equals plus or minus lambda over a. For small angles, the central maximum spans an angle of two lambda over a. On a screen a distance D away, its width is two lambda D over a. Or two lambda f over a, in the focal plane of a lens."):
            self.add(mk)
            self.play(FadeIn(mk), FadeIn(ro))
            self.play(Write(ws[0]))
            self.play(Write(ws[1]))
            self.play(Write(ws[2]))
        with self.say("Now squeeze the slit. Halve its width, and the central maximum doubles in width. That is the puzzle from the start, explained. Only when the slit is very wide compared with lambda does the patch shrink to a sharp shadow of the slit, which is why ray optics works for ordinary openings."):
            self.play(a.animate.set_value(0.5), run_time=3)
            self.play(a.animate.set_value(2.0), run_time=3)
            self.play(a.animate.set_value(1.0), run_time=1.5)
        self.play(FadeOut(VGroup(eq, ax, xl, ro, ws)), FadeOut(Ic), FadeOut(scr), FadeOut(mk))
        self.remove(Ic, scr, mk)
        example(self, "A slit 0.20 mm wide is lit normally by 600 nm light; the screen is 1.5 m away. Find the angle of the first minimum, the width of the central maximum, and the distance of the second minimum from the centre.",
                [r"\sin\theta_1 = \frac{\lambda}{a} = \frac{600\times10^{-9}}{0.20\times10^{-3}} = 3.0\times10^{-3}\ \Rightarrow\ \theta_1 = 3.0\times10^{-3}\ \text{rad} = 0.17^{\circ}",
                 r"w = \frac{2\lambda D}{a} = 2\times 3.0\times10^{-3}\times 1.5 = 9.0\ \text{mm}",
                 r"\sin\theta_2 = \frac{2\lambda}{a} = 6.0\times10^{-3}\ \Rightarrow\ y_2 \approx 1.5\times 6.0\times10^{-3} = 9.0\ \text{mm}"],
                ["Worked example. A slit zero point two millimetres wide, light of six hundred nanometres, a screen one and a half metres away. Find the first minimum's angle, the width of the central maximum, and the position of the second minimum.",
                 "Sine theta one is lambda over a: six hundred nanometres over zero point two millimetres, three times ten to the minus three. That is three milliradians, about zero point one seven degrees. Tiny.",
                 "The width of the central maximum is two lambda D over a: two times three times ten to the minus three, times one point five. Nine millimetres.",
                 "The second minimum has sine theta equal to two lambda over a, six times ten to the minus three, so it lies nine millimetres from the centre. Notice: the central maximum is as wide as the distance from the centre to the second minimum."], size=34)
        self.tip("Narrower slit → WIDER central maximum (w = 2λD/a). And a sin θ = nλ gives DARK fringes here, the opposite of Young's d sin θ = nλ for bright ones.",
                 "Two traps. First, a narrower slit gives a wider central maximum, because w is two lambda D over a. Second, in single slit diffraction, a sine theta equals n lambda gives the dark fringes. In Young's experiment and the grating, the same looking formula gives the bright ones. Read carefully which you are using.", state="wink")
        example(self, "Light of 500 nm falls normally on a slit 0.10 mm wide; the screen is 1.0 m away. Find the distance between the first minima on the two sides of the centre.",
                [r"\sin\theta_1 = \frac{500\times10^{-9}}{1.0\times10^{-4}} = 5.0\times10^{-3}",
                 r"y_1 = D\theta_1 = 1.0\times 5.0\times10^{-3} = 5.0\ \text{mm}",
                 r"\text{separation} = 2y_1 = 10\ \text{mm} = 1.0\ \text{cm}"],
                ["One more. Five hundred nanometre light, a slit zero point one millimetres wide, a screen one metre away. How far apart are the first minima on the two sides?",
                 "Sine theta one is lambda over a: five times ten to the minus three.",
                 "Each first minimum is D theta from the centre: five millimetres.",
                 "So they are ten millimetres apart, one centimetre. That is just the width of the central maximum."], size=40)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        col = wl_rgb(600)
        y_s = strip(-3.6, -2.6, 2.4, 1.6, lambda y: col * np.cos(PI * y / 0.6) ** 2 * 0.95, n=120)
        d_s = strip(3.6, -2.6, 2.4, 1.6, lambda y: col * np.clip(s2(PI * y / 1.0) ** 0.6, 0, 1), n=120)
        hl = VGroup(T("Interference (Young)", size=26, color=th.SKY, weight="BOLD").next_to(y_s, UP, buff=0.2), T("Diffraction (single slit)", size=26, color=th.PINK, weight="BOLD").next_to(d_s, UP, buff=0.2))
        with self.say("Geometrical optics says the image of a slit is a sharp bright rectangle. What you actually see is this: a broad central band, flanked by fainter and fainter bands. Every optical image is really a diffraction pattern. A point is never imaged as a point."):
            self.play(FadeIn(d_s), FadeIn(hl[1]))
        with self.say("Put it beside Young's fringes, and the two look related, because both are superposition. But the exam wants you to tell them apart."):
            self.play(FadeIn(y_s), FadeIn(hl[0]))
        self.play(FadeOut(VGroup(y_s, d_s, hl)))
        rows = [("Interference", "Diffraction"), ("waves from two separate coherent sources", "wavelets from different parts of one wavefront"), ("fringes of equal width", "central band twice as wide"),
                ("bright fringes equally bright", "intensity falls off fast"), ("dark fringes perfectly dark", "minima dark, pattern never repeats exactly"), ("bright: Δ = nλ", "dark: a sin θ = nλ")]
        grid = VGroup()
        for i, (l, r) in enumerate(rows):
            row = VGroup(T(l, size=21 if i else 28, color=th.SKY if i == 0 else th.BODY, weight="BOLD" if i == 0 else "NORMAL"),
                         T(r, size=21 if i else 28, color=th.PINK if i == 0 else th.BODY, weight="BOLD" if i == 0 else "NORMAL"))
            row[0].move_to([-3.4, 2.5 - i * 0.78, 0])
            row[1].move_to([3.4, 2.5 - i * 0.78, 0])
            grid.add(row)
        with self.say("Interference comes from waves from two separate coherent sources. Diffraction comes from wavelets from different parts of the same wavefront. Interference fringes are equally wide and equally bright. In diffraction, the central band is twice as wide as the rest, and the intensity falls off fast. And the formulas: for interference, a path difference of n lambda gives brightness. For a single slit, a sine theta equals n lambda gives darkness.") as v_:
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(grid))
        self.quiz("The width of the central maximum in single-slit diffraction",
                  ["increases with slit width", "decreases with slit width", "does not depend on slit width", "is always zero"], 1,
                  "Pause and think. How does the width of the central maximum depend on the width of the slit?",
                  "B, it decreases as the slit gets wider, since w is two lambda D over a. The tempting answer A is the ray optics intuition, that a bigger hole makes a bigger patch. Diffraction does the opposite.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("The diffraction grating", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        plate = Rectangle(width=0.5, height=4.6, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.BODY).move_to([-4.2, -0.3, 0])
        lines = VGroup(*[Line([-4.45, y, 0], [-3.95, y, 0], color=th.MUTED, stroke_width=2) for y in np.linspace(-2.5, 1.9, 40)])
        zoom = VGroup(*[Rectangle(width=0.5, height=0.32, fill_color=th.INK, fill_opacity=1, stroke_width=0).move_to([-1.8, y, 0]) for y in np.linspace(-1.6, 1.4, 6)])
        gaps = VGroup(*[BraceBetweenPoints([-1.4, y + 0.16, 0], [-1.4, y + 0.6 - 0.16, 0], RIGHT, color=th.SKY) for y in np.linspace(-1.6, 0.8, 5)][:1])
        eb = VGroup(BraceBetweenPoints([-1.3, -1.6 + 0.16, 0], [-1.3, -1.0 - 0.16, 0], RIGHT, color=th.SKY), BraceBetweenPoints([-1.3, -1.0 - 0.16, 0], [-1.3, -1.0 + 0.16, 0], RIGHT, color=th.MUTED))
        ebl = VGroup(M("e", size=28, color=th.SKY).next_to(eb[0], RIGHT, buff=0.05), M("b", size=28, color=th.MUTED).next_to(eb[1], RIGHT, buff=0.05))
        eq = VGroup(M(r"d = e + b = \frac{1}{N}", size=46), T("grating element; N lines per metre", size=22, color=th.MUTED)).arrange(DOWN, buff=0.15).move_to([3.0, 1.4, 0])
        good = para("a good grating: 5000 to 15000 lines per cm, so d is about 1 to 2 μm", width=5.6, size=22, color=th.BODY).move_to([3.0, 0.0, 0])
        with self.say("Now take not two slits, but thousands. A diffraction grating is a glass plate ruled with a huge number of equally spaced parallel lines. The ruled lines are opaque, and the clear gaps between them act as slits."):
            self.play(FadeIn(title), FadeIn(plate), Create(lines))
            self.play(TransformFromCopy(lines[18:24], zoom))
        with self.say("If there are N lines per metre, the distance from one slit to the next is the grating element, d, equal to one over N. It is the width of a gap, e, plus the width of a line, b. A good grating has five to fifteen thousand lines per centimetre, so d is a micrometre or two."):
            self.play(GrowFromCenter(eb[0]), GrowFromCenter(eb[1]), FadeIn(ebl))
            self.play(Write(eq))
            self.play(FadeIn(good))
        self.play(FadeOut(VGroup(title, plate, lines, zoom, eb, ebl, eq, good)))
        xs = -3.0
        ys = np.linspace(1.6, -1.6, 5)
        thg = 0.45
        dv = np.array([np.cos(thg), np.sin(thg), 0])
        gr = VGroup(*[Line([xs, y + 0.32, 0], [xs, y + 0.48, 0], color=th.BODY, stroke_width=8) for y in ys] + [Line([xs, ys[-1] - 0.48, 0], [xs, ys[-1] - 0.32, 0], color=th.BODY, stroke_width=8)])
        rays = VGroup(*[Line([xs, y, 0], [xs, y, 0] + dv * 3.4, color=th.AMBER, stroke_width=3) for y in ys])
        p1, p2 = np.array([xs, ys[1], 0]), np.array([xs, ys[2], 0])
        foot = p1 + dv * np.dot(p2 - p1, dv)
        pd = Line(p2, p2 + dv * np.dot(p1 - p2, dv), color=th.CORAL, stroke_width=6)
        pdl = M(r"d\sin\theta", size=30, color=th.CORAL).next_to(pd, DOWN, buff=0.15)
        dbr = BraceBetweenPoints(p1, p2, LEFT, color=th.MUTED)
        dlb = M("d", size=30).next_to(dbr, LEFT, buff=0.05)
        L = VGroup(M(r"\text{adjacent slits: } \Delta = d\sin\theta", size=36), M(r"d\sin\theta = n\lambda,\quad n = 0, 1, 2, \ldots", size=46, color=C_G),
                   M(r"n_{\max} = \frac{d}{\lambda}\ (\text{rounded down})", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.7, 0.6, 0])
        with self.say("Light falls normally on the grating. Take the parallel rays leaving every slit at angle theta. Between any two neighbouring slits, the path difference is the same: d sine theta."):
            self.play(FadeIn(gr), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.1))
            self.play(GrowFromCenter(dbr), FadeIn(dlb), Create(pd), FadeIn(pdl))
            self.play(Write(L[0]))
        with self.say("All the slits reinforce each other only when that common path difference is a whole number of wavelengths. d sine theta equals n lambda: the grating equation. n is the order of the spectrum."):
            self.sfx("impact", gain=-12)
            self.play(Write(L[1]))
        with self.say("And since sine theta can never exceed one, the highest order you can get is d over lambda, rounded down."):
            self.play(Write(L[2]))
        self.play(FadeOut(VGroup(gr, rays, pd, pdl, dbr, dlb, L)))
        Nn = ValueTracker(2)
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[0, 1.05, 0.5], x_length=10, y_length=3.2, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([0, 0.2, 0])

        def grat(u):
            N = int(round(Nn.get_value()))
            ph = PI * u
            s = np.sin(ph)
            if abs(s) < 1e-6:
                return 1.0
            return (np.sin(N * ph) / (N * s)) ** 2
        Ic = always_redraw(lambda: ax.plot(grat, x_range=[-2.2, 2.2, 0.004], color=C_G, stroke_width=4))
        ro = readout("number of slits N =", lambda: int(round(Nn.get_value())), "", decimals=0, size=30, color=C_G).to_edge(UP, buff=0.9)
        ol = VGroup(*[T(s, size=22, color=th.MUTED).next_to(ax.c2p(n, 0), DOWN, buff=0.15) for n, s in zip((-2, -1, 0, 1, 2), ("n = −2", "n = −1", "n = 0", "n = 1", "n = 2"))])
        with self.say("Why are the maxima of a grating so sharp? Watch the pattern as the number of slits grows. Two slits give broad cos squared fringes. Five slits sharpen them. Twenty, and the bright lines are needle thin."):
            self.add(Ic)
            self.play(Create(ax), FadeIn(Ic), FadeIn(ro), FadeIn(ol))
            self.play(Nn.animate.set_value(5), run_time=2.5, rate_func=linear)
            self.play(Nn.animate.set_value(20), run_time=3, rate_func=linear)
        with self.say("With thousands of slits, the slightest step away from the exact condition throws distant slits out of step with each other, and they cancel. So the maxima are extremely sharp, which makes the grating a precision instrument for measuring wavelength."):
            self.wait(2)
        self.play(FadeOut(VGroup(ax, ro, ol)), FadeOut(Ic))
        self.remove(Ic)

        def spectrum(y):
            s = np.zeros(3)
            for nm in np.linspace(400, 700, 31):
                for n in (-2, -1, 0, 1, 2):
                    yy = n * 2.0 * nm / 550
                    s += wl_rgb(nm) * np.exp(-((y - yy) / 0.05) ** 2)
            return s / 6
        sp = strip(0, -5.6, 5.6, 1.0, spectrum, n=420).rotate(-PI / 2).move_to([0, 0.2, 0])
        spl = VGroup(T("white centre (n = 0)", size=22).next_to(sp, DOWN, buff=0.2), T("1st order", size=22, color=th.MUTED).move_to([2.0, 1.1, 0]), T("2nd order", size=22, color=th.MUTED).move_to([4.1, 1.1, 0]),
                     T("1st order", size=22, color=th.MUTED).move_to([-2.0, 1.1, 0]), T("2nd order", size=22, color=th.MUTED).move_to([-4.1, 1.1, 0]))
        with self.say("Shine white light on a grating, and each order spreads into a full spectrum. Since sine theta is proportional to lambda, violet is bent least, closest to the centre, and red the most. That is the opposite way round from a prism, where red is deviated least."):
            self.play(FadeIn(sp), FadeIn(spl))
            self.wait(1)
        self.play(FadeOut(VGroup(sp, spl)))
        example(self, "A plane grating has 5000 lines per cm; light of 500 nm falls normally on it. Find the angles of the first three orders and the highest order observed.",
                [r"d = \frac{10^{-2}}{5000} = 2.0\times10^{-6}\ \text{m},\quad \sin\theta = \frac{n\lambda}{d} = 0.25\,n",
                 r"n = 1: 14.5^{\circ},\quad n = 2: 30.0^{\circ},\quad n = 3: 48.6^{\circ}",
                 r"\frac{d}{\lambda} = 4:\ n = 4 \text{ gives } \theta = 90^{\circ} \ (\text{grazing}) \Rightarrow 3 \text{ orders each side}"],
                ["Worked example. A grating with five thousand lines per centimetre, and five hundred nanometre light. Find the angles of the first three orders, and the highest order you can see.",
                 "The grating element is one centimetre over five thousand: two micrometres. So sine theta is n lambda over d, zero point two five n.",
                 "First order: sine theta zero point two five, fourteen point five degrees. Second: zero point five, thirty degrees. Third: zero point seven five, forty eight point six degrees.",
                 "d over lambda is four. But the fourth order would come out at ninety degrees, grazing along the grating, where it can never be collected. So only three orders are seen on each side."], size=38)
        self.quiz("A grating has 2000 lines per centimetre. Its grating element is",
                  ["2 μm", "5 μm", "0.5 μm", "20 μm"], 1,
                  "Pause and think. Two thousand lines per centimetre. What is the grating element?",
                  "B, five micrometres. One centimetre over two thousand is five times ten to the minus four centimetres, which is five micrometres. Two micrometres is what you get if you forget the centimetre.")
        example(self, "A grating with 6000 lines/cm is lit normally by 600 nm light. Find d, the first and second order angles, the highest order, and the smallest wavelength difference resolved in 2nd order with 8000 lines illuminated.",
                [r"d = \frac{10^{-2}}{6000} = 1.667\ \mu\text{m},\quad \frac{\lambda}{d} = 0.36",
                 r"\sin\theta_1 = 0.36 \Rightarrow 21.1^{\circ},\quad \sin\theta_2 = 0.72 \Rightarrow 46.1^{\circ}",
                 r"n_{\max} = \frac{1}{0.36} = 2.78 \Rightarrow n = 2",
                 r"\frac{\lambda}{d\lambda} = nN = 2\times 8000 = 16000\ \Rightarrow\ d\lambda = \frac{600}{16000} = 0.0375\ \text{nm}"],
                ["A full long question. Six thousand lines per centimetre, six hundred nanometre light. Find d, the first two orders, the highest order, and the resolving limit in the second order with eight thousand lines lit.",
                 "d is one centimetre over six thousand: one point six six seven micrometres. So lambda over d is zero point three six.",
                 "First order: sine theta is zero point three six, twenty one point one degrees. Second order: zero point seven two, forty six point one degrees.",
                 "The highest order is d over lambda, two point seven eight, so only the second order is reached.",
                 "A grating's resolving power is n N, here sixteen thousand. So it can just separate two wavelengths zero point zero three seven five nanometres apart. Astonishingly precise, as we will see in the next part."], size=36)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        sep = ValueTracker(2.0)
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.6, 0.5], x_length=9, y_length=3.4, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-0.6, 0.0, 0])
        f1 = always_redraw(lambda: ax.plot(lambda u: s2(PI * (u + sep.get_value() / 2)), x_range=[-3, 3, 0.01], color=th.SKY, stroke_width=3))
        f2 = always_redraw(lambda: ax.plot(lambda u: s2(PI * (u - sep.get_value() / 2)), x_range=[-3, 3, 0.01], color=th.PINK, stroke_width=3))
        fs = always_redraw(lambda: ax.plot(lambda u: s2(PI * (u + sep.get_value() / 2)) + s2(PI * (u - sep.get_value() / 2)), x_range=[-3, 3, 0.01], color=WHITE, stroke_width=5))
        stars = VGroup(Star(n=5, outer_radius=0.15, fill_color=th.SKY, fill_opacity=1, stroke_width=0), Star(n=5, outer_radius=0.15, fill_color=th.PINK, fill_opacity=1, stroke_width=0))
        ro = readout("separation:", lambda: sep.get_value(), "× (first-minimum angle)", decimals=2, size=24).move_to([0, 2.6, 0])
        verdict = always_redraw(lambda: T("resolved" if sep.get_value() > 1.02 else ("just resolved (Rayleigh)" if sep.get_value() > 0.97 else "not resolved"), size=30,
                                          color=th.MINT if sep.get_value() > 0.97 else th.CORAL, weight="BOLD").move_to([0, -2.5, 0]))
        with self.say("Because every image is a diffraction patch, two nearby stars seen through a telescope give two overlapping patches. Far apart, you clearly see two peaks."):
            self.play(Create(ax), FadeIn(ro))
            self.add(f1, f2, fs, verdict)
            self.play(FadeIn(f1), FadeIn(f2), FadeIn(fs), FadeIn(verdict))
        with self.say("Bring them closer. The patches merge. At some point, the dip between them vanishes, and the two stars look like one."):
            self.play(sep.animate.set_value(0.6), run_time=3.5)
        with self.say("Lord Rayleigh drew the line here. Two point objects are just resolved when the central maximum of one falls exactly on the first minimum of the other. There is still a clear dip in the middle, down to about seventy four percent."):
            self.play(sep.animate.set_value(1.0), run_time=2.5)
            self.wait(1.5)
        self.play(FadeOut(VGroup(ax, ro)), FadeOut(f1), FadeOut(f2), FadeOut(fs), FadeOut(verdict))
        self.remove(f1, f2, fs, verdict)
        title = T("Resolving power", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        cols = VGroup(
            VGroup(T("Telescope", size=28, color=th.SKY, weight="BOLD"), M(r"\theta_{\min} = \frac{1.22\lambda}{a}", size=42), M(r"\text{R.P.} = \frac{1}{\theta_{\min}} = \frac{a}{1.22\lambda}", size=36),
                   T("bigger objective: sharper and brighter", size=20, color=th.MUTED)),
            VGroup(T("Microscope", size=28, color=th.PINK, weight="BOLD"), M(r"x_{\min} = \frac{1.22\lambda}{2\mu\sin\theta}", size=42), M(r"\text{R.P.} = \frac{2\mu\sin\theta}{1.22\lambda}", size=36),
                   T("μ sin θ = numerical aperture", size=20, color=th.MUTED)),
            VGroup(T("Grating", size=28, color=C_G, weight="BOLD"), M(r"\frac{\lambda}{d\lambda} = nN", size=42), T("N lines lit, order n", size=20, color=th.MUTED)))
        for c in cols:
            c.arrange(DOWN, buff=0.3)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).next_to(title, DOWN, buff=0.5)
        with self.say("For a telescope with a circular objective of diameter a, the first dark ring is at an angle one point two two lambda over a. The factor one point two two comes from the circular shape. So the smallest angle it can resolve is one point two two lambda over a, and its resolving power is the reciprocal, a over one point two two lambda. A bigger objective resolves better, and gathers more light too. That is why research telescopes have mirrors metres across."):
            self.play(FadeIn(title))
            self.play(FadeIn(cols[0], shift=UP * 0.2))
        with self.say("For a microscope, what matters is the smallest separation x between two points on the slide: one point two two lambda over two mu sine theta. Theta is the half angle of the cone of light entering the objective, and mu sine theta is the numerical aperture. So use shorter wavelengths, even electrons, or put a drop of cedar oil, index one point five, under the objective: oil immersion."):
            self.play(FadeIn(cols[1], shift=UP * 0.2))
        with self.say("And a grating's power to separate two close wavelengths is lambda over d lambda equals n N."):
            self.play(FadeIn(cols[2], shift=UP * 0.2))
        nb = neby_in(self, "cool", corner=DR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, cols)))
        neby_out(self, nb)
        example(self, "A telescope objective is 100 mm across. With λ = 550 nm, find its limit of resolution and the smallest separation it can resolve on the Moon, 3.84 × 10⁸ m away.",
                [r"\theta_{\min} = \frac{1.22\times 550\times10^{-9}}{0.100} = 6.71\times10^{-6}\ \text{rad}",
                 r"x = r\theta_{\min} = 3.84\times10^{8}\times 6.71\times10^{-6} = 2.58\times10^{3}\ \text{m}"],
                ["Worked example. A small telescope with a ten centimetre objective, and light of five hundred and fifty nanometres. What is its limit of resolution, and what is the smallest thing it can make out on the Moon?",
                 "Theta min is one point two two lambda over a: six point seven one times ten to the minus six radians.",
                 "At the Moon's distance, that angle spans r theta: about two point six kilometres. A small telescope cannot show anything on the Moon smaller than a large town."], size=40)
        example(self, "An oil-immersion microscope uses 500 nm light, a half-angle of 60° and oil of index 1.5. Find the smallest separation it can resolve.",
                [r"\mu\sin\theta = 1.5\times\sin 60^{\circ} = 1.5\times 0.866 = 1.299",
                 r"x_{\min} = \frac{1.22\times 500\times10^{-9}}{2\times 1.299} = \frac{6.10\times10^{-7}}{2.598} = 2.35\times10^{-7}\ \text{m}"],
                ["And a microscope. Oil immersion, five hundred nanometre light, a sixty degree half angle, oil of index one point five.",
                 "The numerical aperture is one point five times sine sixty: one point two nine nine.",
                 "x min is one point two two lambda over twice that: two hundred and thirty five nanometres. Smaller than a bacterium, but far bigger than a virus, which is why viruses need an electron microscope."], size=40)
        self.quiz("The resolving power of a telescope can be increased by",
                  ["increasing the wavelength", "increasing the aperture", "decreasing the aperture", "a stronger eyepiece"], 1,
                  "Last check. How can you increase the resolving power of a telescope?",
                  "B, a bigger aperture, since the resolving power is a over one point two two lambda. Eyepiece magnification is the trap: it makes the blurred patches bigger, but cannot separate what diffraction has already merged.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Diffraction: bending round edges, noticeable when the aperture is comparable with λ. Fraunhofer uses plane waves.",
            M(r"\text{single slit minima: } a\sin\theta = n\lambda,\ n = \pm1, \pm2, \ldots;\ \ I = I_0\left(\tfrac{\sin\beta}{\beta}\right)^{2}", size=32),
            M(r"\text{central maximum: } 2\theta_1 = \frac{2\lambda}{a},\ \ w = \frac{2\lambda D}{a}\ (\text{narrower slit, wider patch})", size=32),
            "Interference: two sources, equal fringes. Diffraction: one wavefront, wide central band, fading sides.",
            M(r"\text{grating: } d = \frac{1}{N},\ \ d\sin\theta = n\lambda,\ \ n_{\max} = \frac{d}{\lambda}", size=34),
            M(r"\theta_{\min} = \frac{1.22\lambda}{a};\ \ x_{\min} = \frac{1.22\lambda}{2\mu\sin\theta};\ \ \frac{\lambda}{d\lambda} = nN", size=34),
        ], "Let us recap. Diffraction is the spreading of waves at openings comparable with their wavelength. A single slit gives minima at a sine theta equals n lambda, and a central maximum two lambda D over a wide, so a narrower slit spreads the light more. Interference and diffraction are both superposition, but they differ in their sources and their patterns. A grating gives sharp maxima at d sine theta equals n lambda. And by Rayleigh's criterion, a telescope resolves one point two two lambda over a, so bigger is better.")
        self.outro("That is diffraction. Next, we discover that light waves vibrate in a particular direction, and that sunglasses and calculator screens can choose which direction gets through, in Polarization. See you there, on NEBians.")
