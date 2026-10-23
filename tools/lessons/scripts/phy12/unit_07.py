import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import (Cylinder, Gas, Stream, arrow, clock, curve, example, heat_color, neby_in, neby_out, pv_axes,  # noqa: E402
                   readout, spring)

C_E, C_R, C_V, C_N, C_L = th.AMBER, th.PINK, th.SKY, th.CORAL, th.MINT


def chain_sim(k, m, n=26, T_end=7.0, dt=0.002, amp=0.45):
    """Masses joined by springs, the first one given a single push. Returns (times, displacements[time, i])."""
    steps = int(T_end / dt)
    u = np.zeros(n)
    v = np.zeros(n)
    out_t, out_u = [], []
    for s in range(steps):
        t = s * dt
        u[0] = amp * np.exp(-((t - 0.45) / 0.18) ** 2)
        acc = np.zeros(n)
        acc[1:-1] = k / m * (u[2:] - 2 * u[1:-1] + u[:-2])
        acc[-1] = k / m * (u[-2] - u[-1])
        v[1:] += acc[1:] * dt
        u[1:] += v[1:] * dt
        if s % 10 == 0:
            out_t.append(t)
            out_u.append(u.copy())
    return np.array(out_t), np.array(out_u)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 7
    TITLE = "Mechanical Waves"
    SUBTITLE = "What decides the speed of sound"
    SECTIONS = ["Speed of a wave", "Sound in solids and liquids", "Newton's formula for a gas", "Laplace's correction",
                "Temperature, pressure, humidity"]
    NEXT = "Unit 8 · Waves in Pipes and Strings"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        rail_y = -1.2
        rails = VGroup(Line([-6.8, rail_y, 0], [6.8, rail_y, 0], color=th.MUTED, stroke_width=8),
                       *[Rectangle(width=0.18, height=0.5, fill_color="#5a4632", fill_opacity=1, stroke_width=0).move_to([x, rail_y - 0.1, 0]) for x in np.arange(-6.6, 6.8, 0.6)])
        rails[0].set_z_index(1)
        train = VGroup(RoundedRectangle(corner_radius=0.12, width=2.0, height=1.1, fill_color=th.CORAL, fill_opacity=1, stroke_width=0),
                       Rectangle(width=0.5, height=0.35, fill_color=th.SKY, fill_opacity=0.9, stroke_width=0).shift(UP * 0.15 + RIGHT * 0.5),
                       Circle(radius=0.16, fill_color=th.INK, fill_opacity=1, stroke_width=0).shift(DOWN * 0.55 + LEFT * 0.55),
                       Circle(radius=0.16, fill_color=th.INK, fill_opacity=1, stroke_width=0).shift(DOWN * 0.55 + RIGHT * 0.55)).move_to([-5.6, rail_y + 0.75, 0])
        ear = VGroup(Circle(radius=0.32, fill_color="#E9B48A", fill_opacity=1, stroke_width=0), Arc(radius=0.14, start_angle=-PI / 2, angle=PI, color="#8a5a3a", stroke_width=4).shift(LEFT * 0.08)).move_to([5.6, rail_y + 0.35, 0])
        el = T("ear on the rail", size=22, color=th.BODY).next_to(ear, UP, buff=0.2)
        tag = T("Janakpur railway", size=24, color=th.MUTED).to_edge(UP, buff=0.6)
        with self.say("On the Janakpur railway, a boy puts his ear to the rail. A train is coming, far away down the line. He blows nothing, says nothing. He just listens."):
            self.play(FadeIn(tag), Create(rails), FadeIn(train), FadeIn(ear), FadeIn(el))
        t = ValueTracker(0)
        L = 11.0
        vr, va = 5.0, 0.34
        rp = always_redraw(lambda: VGroup(*[Line([-4.6 + vr * t.get_value() - d, rail_y + 0.12, 0], [-4.6 + vr * t.get_value() - d, rail_y - 0.12, 0], color=th.AMBER, stroke_width=5).set_opacity(1 - d) for d in (0, 0.25, 0.5)])
                            if vr * t.get_value() < L - 0.4 else VGroup())
        ap = always_redraw(lambda: VGroup(*[Arc(radius=max(0.05, va * t.get_value() * 3 - d), start_angle=-0.6, angle=1.2, arc_center=[-4.6, rail_y + 0.8, 0], color=th.SKY, stroke_width=4).set_opacity(max(0, 1 - d)) for d in (0, 0.3, 0.6)]))
        lab = VGroup(T("through steel", size=24, color=th.AMBER), T("through air", size=24, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 2.0, 0])
        self.add(rp, ap)
        with self.say("The train's rumble sets off two sound waves at once. One through the steel rail, one through the air. Watch which one reaches him first."):
            self.play(FadeIn(lab))
            self.play(t.animate.set_value(2.2), run_time=2.2, rate_func=linear)
            self.sfx("tick", gain=-4)
            self.play(Flash(ear.get_center(), color=th.AMBER, flash_radius=0.6), t.animate.set_value(3.0), run_time=0.8, rate_func=linear)
        nb = neby_in(self, "surprised", corner=UR)
        q = para("Steel is six thousand times denser than air, yet sound races through it fifteen times faster. Why?", width=10, size=30, color=th.AMBER, align="center").to_edge(DOWN, buff=0.4)
        with self.say("The rail wins, by miles. He hears the train through the steel long before the air carries the sound to him. But steel is about six thousand times denser than air. Shouldn't heavy stuff be slower? What really decides the speed of a wave?"):
            self.play(FadeIn(q, shift=UP * 0.2))
        self.play(FadeOut(VGroup(rails, train, ear, el, tag, lab, q)), FadeOut(rp), FadeOut(ap))
        self.remove(rp, ap)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 7: Mechanical Waves. This unit answers one question: what fixes the speed of sound? The answer depends on just two properties of the medium, how stiff it is and how heavy it is, plus one subtle point about heat that took physics more than a century to get right."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. The general formula for wave speed, sound in solids and liquids, Newton's formula for a gas, Laplace's famous correction, and finally how temperature, pressure, humidity and wind change the speed of sound.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        eq = M(r"v = f\lambda", size=72).move_to([0, 1.8, 0])
        with self.say("Every wave obeys v equals f lambda. But that only links speed, frequency and wavelength together. It does not tell you what the speed is."):
            self.play(Write(eq))
        t = ValueTracker(0)
        y1, y2 = 0.2, -1.4
        sp = 2.2
        def pulse(y, f, col, A):
            def mk():
                x = -6 + sp * t.get_value()
                return curve(lambda s: y + A * np.exp(-((s - x) / 0.8) ** 2) * np.sin(f * (s - x)), -6.3, 6.3, n=260, color=col, width=4)
            return always_redraw(mk)
        lo = pulse(y1, 4, th.SKY, 0.3)
        hi = pulse(y2, 12, th.CORAL, 0.6)
        tl = VGroup(T("soft, low pitch", size=22, color=th.SKY).move_to([-5.0, y1 + 0.7, 0]), T("loud, high pitch", size=22, color=th.CORAL).move_to([-5.0, y2 + 0.9, 0]))
        fin = DashedLine([5.2, 1.0, 0], [5.2, -2.4, 0], color=th.MINT, stroke_width=3)
        with self.say("Sound a horn softly at a low pitch, and loudly at a high pitch. Both sounds arrive at exactly the same moment. The speed is decided by the medium, not by the source."):
            self.add(lo, hi)
            self.play(FadeIn(tl), Create(fin))
            self.play(t.animate.set_value(5.2), run_time=4.5, rate_func=linear)
        self.play(FadeOut(VGroup(eq, tl, fin)), FadeOut(lo), FadeOut(hi))
        self.remove(lo, hi)
        self.chains()
        self.moduli()

    def chains(self):
        title = T("Stiffness speeds a wave up; mass slows it down", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        n = 26
        x0, dx = -6.0, 0.48
        sims = [chain_sim(4.0, 1.0, n), chain_sim(16.0, 1.0, n), chain_sim(16.0, 4.0, n)]
        ys = [1.4, -0.2, -1.8]
        cols = [th.SKY, C_E, C_R]
        names = ["normal springs", "4 × stiffer springs", "4 × stiffer AND 4 × heavier"]
        tt = ValueTracker(0)

        def chain(k):
            ts, us = sims[k]

            def mk():
                i = min(len(ts) - 1, int(tt.get_value() / (ts[1] - ts[0])))
                u = us[i]
                xs = [x0 + j * dx + 0.9 * u[j] for j in range(n)]
                g = VGroup()
                for j in range(n - 1):
                    g.add(spring([xs[j] + 0.09, ys[k], 0], [xs[j + 1] - 0.09, ys[k], 0], coils=3, width=0.08, color=th.FAINT, stroke=2))
                for j in range(n):
                    sq = (0.18 if k < 2 else 0.24) * (1 + 2.2 * abs(u[j]))
                    g.add(Square(sq, fill_color=interpolate_color(ManimColor(cols[k]), ManimColor(WHITE), min(1, 2.5 * abs(u[j]))), fill_opacity=1, stroke_width=0).move_to([xs[j], ys[k], 0]))
                return g
            return always_redraw(mk)
        cs = [chain(k) for k in range(3)]
        labs = VGroup(*[T(nm, size=22, color=c).move_to([4.6, y + 0.45, 0]) for nm, c, y in zip(names, cols, ys)])
        with self.say("Why does the medium matter? Think of it as a line of masses joined by springs. Push the first mass, and it squeezes its spring, which pushes the next mass, and so on down the line. The springs supply elasticity. The masses supply inertia."):
            self.play(FadeIn(title))
            self.add(cs[0])
            self.play(FadeIn(cs[0]), FadeIn(labs[0]))
            self.play(tt.animate.set_value(6.5), run_time=6.5, rate_func=linear)
        tt.set_value(0)
        with self.say("Now race three chains. Make the springs four times stiffer, and the push races along twice as fast. Make the masses four times heavier as well, and it slows back down to where it started. Speed goes as the square root of stiffness over inertia."):
            self.add(cs[1], cs[2])
            self.play(FadeIn(cs[1]), FadeIn(cs[2]), FadeIn(labs[1]), FadeIn(labs[2]))
            self.play(tt.animate.set_value(6.5), run_time=6.5, rate_func=linear)
        self.play(FadeOut(VGroup(title, labs)), *[FadeOut(c) for c in cs])
        self.remove(*cs)

    def moduli(self):
        eq = M(r"v", r"=", r"\sqrt{\frac{E}{\rho}}", size=96).move_to([0, 1.6, 0])
        eq[0].set_color(C_V)
        b1 = T("E: modulus of elasticity (stiffness)", size=26, color=C_E)
        b2 = T("ρ: density (inertia)", size=26, color=C_R)
        VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eq, DOWN, buff=0.4)
        with self.say("Newton showed that these two combine in one formula. The speed of a mechanical wave is the square root of E over rho, where rho is the density of the medium, and E is its modulus of elasticity."):
            self.sfx("impact", gain=-12)
            self.play(Write(eq))
            self.play(FadeIn(b1), FadeIn(b2))
        with self.say("The whole skill of this unit is choosing the right modulus, the one that matches the kind of squeezing the wave produces."):
            self.play(Circumscribe(eq, color=C_E))
        self.play(FadeOut(VGroup(b1, b2)), eq.animate.scale(0.55).to_edge(UP, buff=0.75))
        rows = [("thin solid rod", "squeezed along its length", "Young's modulus Y", r"v = \sqrt{Y/\rho}"),
                ("liquid", "change of volume", "bulk modulus B", r"v = \sqrt{B/\rho}"),
                ("gas", "change of volume", "bulk modulus of gas", r"v = \sqrt{B/\rho}"),
                ("stretched string", "change of shape", "tension T, mass per length μ", r"v = \sqrt{T/\mu}")]
        grid = VGroup()
        for i, (a, b, c, d) in enumerate(rows):
            r = VGroup(T(a, size=23, color=th.INK, weight="SEMIBOLD"), T(b, size=21, color=th.BODY), T(c, size=21, color=C_E), M(d, size=34, color=C_V))
            for j, x in enumerate([-5.1, -1.7, 1.8, 5.2]):
                r[j].move_to([x, 1.2 - i * 0.95, 0])
            grid.add(r)
        with self.say("Here is the table to learn. A longitudinal wave in a long thin rod stretches and squeezes it, so use Young's modulus. In a liquid or a gas, the volume changes, so use the bulk modulus. And for a transverse wave on a stretched string, the tension plays the role of stiffness, and the mass per unit length plays the role of density.") as v_:
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.6)
                self.hold(v_.dur / 4 - 0.7)
        self.play(FadeOut(VGroup(eq, grid)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        self.quake()
        self.speeds_chart()
        self.quiz("Sound travels fastest in",
                  ["vacuum", "air", "water", "steel"], 3,
                  "Pause and think. In which of these does sound travel fastest?",
                  "D, steel. Its Young's modulus is enormous. And vacuum is the trap: sound is a mechanical wave, so with no medium at all, it does not travel at all.")
        example(self, "The velocity of sound in a liquid is 1500 m/s and its density is 1200 kg/m³. Find the bulk modulus of the liquid.",
                [r"v = \sqrt{\frac{B}{\rho}} \;\Rightarrow\; B = \rho v^{2}",
                 r"B = 1200 \times (1500)^{2} = 1200 \times 2.25\times10^{6} = 2.7\times10^{9}\ \text{Pa}"],
                ["Now run the formula backwards. Sound travels at fifteen hundred metres per second in a liquid of density twelve hundred kilograms per cubic metre. What is its bulk modulus?",
                 "Square both sides of v equals root B over rho, and B equals rho v squared.",
                 "Twelve hundred times fifteen hundred squared: two point seven times ten to the nine pascals. A little stiffer than water."], size=44)

    def quake(self):
        title = T("Solids carry two kinds of wave", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        ground = Rectangle(width=13.6, height=4.2, stroke_width=0, fill_color="#3b3020", fill_opacity=0.6).move_to([0, -1.1, 0])
        surf = Line([-6.8, 1.0, 0], [6.8, 1.0, 0], color="#8a7a5a", stroke_width=4)
        F = np.array([-4.8, -2.4, 0])
        S = np.array([4.6, 1.0, 0])
        fl = VGroup(Star(n=6, outer_radius=0.25, fill_color=th.CORAL, fill_opacity=1, stroke_width=0).move_to(F), T("focus", size=20, color=th.CORAL).next_to(F, DOWN, buff=0.25))
        st = VGroup(Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).scale(0.2).move_to(S + UP * 0.2), T("seismograph", size=20).next_to(S, UP, buff=0.4))
        t = ValueTracker(0)
        D = np.linalg.norm(S - F)
        vp, vs = 3.0, 1.75
        P = always_redraw(lambda: VGroup(*[Arc(radius=max(0.05, vp * t.get_value() - d), start_angle=-0.1, angle=1.2, arc_center=F, color=th.AMBER, stroke_width=4) for d in (0, 0.3)]) if vp * t.get_value() < D + 0.5 else VGroup())
        Sw = always_redraw(lambda: VGroup(*[Arc(radius=max(0.05, vs * t.get_value() - d), start_angle=-0.1, angle=1.2, arc_center=F, color=th.PINK, stroke_width=4) for d in (0, 0.15)]) if vs * t.get_value() < D + 0.5 else VGroup())
        ax = Axes(x_range=[0, 7, 1], y_range=[-1, 1, 1], x_length=5.0, y_length=1.2, tips=False, axis_config={"color": th.FAINT, "include_ticks": False}).move_to([-2.6, 2.2, 0])
        tp, ts = D / vp, D / vs

        def trace(s):
            y = 0
            if s > tp:
                y += 0.35 * np.sin(18 * (s - tp)) * np.exp(-1.5 * (s - tp))
            if s > ts:
                y += 0.9 * np.sin(9 * (s - ts)) * np.exp(-1.0 * (s - ts))
            return y
        tr = always_redraw(lambda: ax.plot(trace, x_range=[0, max(0.02, min(7, t.get_value()))], color=th.INK, stroke_width=2))
        pl = T("P", size=24, color=th.AMBER, weight="BOLD").next_to(ax.c2p(tp, -0.5), DOWN, buff=0.05)
        sl = T("S", size=24, color=th.PINK, weight="BOLD").next_to(ax.c2p(ts, -0.9), DOWN, buff=0.0)
        with self.say("Liquids and gases cannot be sheared. They have no rigidity, so sound in a fluid is always longitudinal. But a solid resists both squeezing and shearing, so it carries longitudinal and transverse waves."):
            self.play(FadeIn(title))
        with self.say("You felt this in the Gorkha earthquake of two thousand fifteen. The rock slipped deep underground and sent out two body waves. The fast, longitudinal P wave, and the slower, transverse S wave."):
            self.play(FadeOut(title), FadeIn(ground), Create(surf), FadeIn(fl), FadeIn(st), Create(ax))
            self.add(P, Sw, tr)
            self.play(t.animate.set_value(7.0), run_time=7.0, rate_func=linear)
            self.play(FadeIn(pl), FadeIn(sl))
        gap = BraceBetweenPoints(ax.c2p(tp, 1.0), ax.c2p(ts, 1.0), UP, color=th.MUTED)
        gl = T("the gap tells the distance", size=20, color=th.MUTED).next_to(gap, RIGHT, buff=0.15)
        with self.say("The seismograph records the P wave first, then the S wave. The longer the gap between them, the further away the earthquake was. That is how the National Seismological Centre locates an epicentre."):
            self.play(GrowFromCenter(gap), FadeIn(gl))
        self.play(FadeOut(VGroup(ground, surf, fl, st, ax, pl, sl, gap, gl)), FadeOut(P), FadeOut(Sw), FadeOut(tr))
        self.remove(P, Sw, tr)

    def speeds_chart(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("Find the speed of sound (a) in a steel rail: Y = 2.0 × 10¹¹ Pa, ρ = 7800 kg/m³, and (b) in water: B = 2.2 × 10⁹ Pa, ρ = 1000 kg/m³.", width=12.2, size=27, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(M(r"v_{\text{steel}} = \sqrt{\frac{2.0\times10^{11}}{7800}} = \sqrt{2.56\times10^{7}} = 5.06\times10^{3}\ \text{m s}^{-1}", size=36),
                       M(r"v_{\text{water}} = \sqrt{\frac{2.2\times10^{9}}{1000}} = \sqrt{2.2\times10^{6}} = 1.48\times10^{3}\ \text{m s}^{-1}", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        with self.say("Let us settle the railway puzzle with a worked example. Find the speed of sound in a steel rail, and in water."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("A rail is a long thin solid, so use Young's modulus. Two times ten to the eleven, over seven thousand eight hundred: the square root comes to about five thousand and sixty metres per second."):
            self.play(Write(steps[0]))
        with self.say("Water is a liquid, so use its bulk modulus. Two point two times ten to the nine, over one thousand: about fourteen hundred and eighty metres per second."):
            self.play(Write(steps[1]))
        self.play(FadeOut(prob), steps.animate.scale(0.8).next_to(head, DOWN, aligned_edge=LEFT, buff=0.3))
        base = -2.9
        data = [("air", 340, 1.29, 1.42e5), ("water", 1480, 1000, 2.2e9), ("steel", 5060, 7800, 2.0e11)]
        bars = VGroup()
        for i, (nm, v, rho, E) in enumerate(data):
            x = -4.2 + i * 1.6
            b = Rectangle(width=1.0, height=max(0.04, 3.2 * v / 5060), fill_color=C_V, fill_opacity=0.9, stroke_width=0).move_to([x, base, 0], aligned_edge=DOWN)
            l = T(nm, size=22).next_to(b, DOWN, buff=0.1)
            vl = T(f"{v}", size=20, color=C_V).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, l, vl))
        rb = VGroup()
        for i, (nm, v, rho, E) in enumerate(data):
            x = 1.6 + i * 1.6
            b = Rectangle(width=1.0, height=max(0.04, 3.2 * rho / 7800), fill_color=C_R, fill_opacity=0.9, stroke_width=0).move_to([x, base, 0], aligned_edge=DOWN)
            l = T(nm, size=22).next_to(b, DOWN, buff=0.1)
            rb.add(VGroup(b, l))
        h1 = T("speed (m/s)", size=24, color=C_V).move_to([-2.6, 0.75, 0])
        h2 = T("density", size=24, color=C_R).move_to([3.2, 0.75, 0])
        with self.say("Put them side by side with air at about three hundred and forty. Steel is about eight times denser than water, yet sound is more than three times faster in it. Density alone never decides the answer."):
            self.play(FadeIn(h1), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2), *[FadeIn(b[1:]) for b in bars])
            self.play(FadeIn(h2), LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in rb], lag_ratio=0.2), *[FadeIn(b[1]) for b in rb])
        with self.say("Steel's Young's modulus is about a hundred times the bulk modulus of water. Stiffness wins over inertia. That is why the boy on the railway heard the train through the rail first."):
            self.play(Indicate(bars[2], color=th.AMBER))
        nb = neby_in(self, "success")
        self.wait(0.3)
        self.play(FadeOut(VGroup(head, steps, bars, rb, h1, h2)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        cube = Square(2.4, stroke_color=th.BODY, stroke_width=4, fill_color=th.SKY, fill_opacity=0.15).move_to([-3.6, -0.2, 0])
        sq = ValueTracker(1.0)
        cube.add_updater(lambda m: m.stretch_to_fit_width(2.4 * sq.get_value()).move_to([-3.6 - 1.2 * (1 - sq.get_value()), -0.2, 0]))
        pushes = always_redraw(lambda: VGroup(*[Arrow([cube.get_right()[0] + 1.0, y, 0], [cube.get_right()[0] + 0.05, y, 0], buff=0, color=C_N, stroke_width=5) for y in (-0.9, -0.2, 0.5)]))
        bm = M(r"B", r"=", r"-\frac{\Delta P}{\Delta V / V}", size=62).move_to([2.8, 1.0, 0])
        bm[0].set_color(C_E)
        note = para("minus sign: more pressure means less volume, so B stays positive", width=4.6, size=22, color=th.MUTED).next_to(bm, DOWN, buff=0.3)
        with self.say("Now the hard case: sound in a gas. The deformation is a change of volume, so we need the bulk modulus: B equals minus the change in pressure, divided by the fractional change in volume, delta V over V."):
            self.add(cube, pushes)
            self.play(FadeIn(cube), FadeIn(pushes), Write(bm))
            self.play(sq.animate.set_value(0.75), run_time=1.5)
        with self.say("The minus sign is there because pressing harder makes the volume smaller. It keeps B positive."):
            self.play(FadeIn(note))
            self.play(sq.animate.set_value(1.0), run_time=1.2)
        self.play(FadeOut(VGroup(bm, note)), FadeOut(pushes), FadeOut(cube))
        cube.clear_updaters()
        self.remove(pushes, cube)
        cx, yb = -3.6, -2.4
        Vt = ValueTracker(3.0)
        Tt = ValueTracker(300)
        cyl = Cylinder(cx, yb, 2.2, 4.4, lambda: Vt.get_value(), lambda: Tt.get_value(), n=24, rod=0.5)
        heat = VGroup(*[Arrow([cx + s * 1.15, yb + 0.9, 0], [cx + s * 2.0, yb + 0.9, 0], buff=0, color=C_N, stroke_width=4) for s in (-1, 1)])
        nw = VGroup(T("Newton, 1686:", size=28, color=th.INK, weight="BOLD"),
                    para("compressions are slow and gentle, so their heat leaks away at once. The temperature stays constant: an isothermal change.", width=5.6, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 1.2, 0])
        with self.say("In sixteen eighty six, Newton had to decide how the gas is squeezed as sound passes. He argued that the squeezing is gentle, so any heat produced in a compression leaks away at once. The temperature stays constant. In other words, an isothermal change."):
            self.play(Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(nw))
            self.play(Vt.animate.set_value(2.0), Tt.animate.set_value(340), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in heat], lag_ratio=0.2), Tt.animate.set_value(300), run_time=1.5)
        self.play(FadeOut(VGroup(nw, heat)))
        cyl.drop(self)
        title = T("Newton's formula", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(M(r"PV = \text{constant}", size=44), M(r"P\,dV + V\,dP = 0", size=44),
                   M(r"-\frac{dP}{dV/V} = P \;\Rightarrow\; B_{\text{iso}} = P", size=44), M(r"v = \sqrt{\frac{P}{\rho}}", size=64, color=C_N)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.4)
        says = ["For an isothermal change of an ideal gas, Boyle's law holds: P V is constant.",
                "Differentiate the product: P d V plus V d P equals zero.",
                "Rearrange. Minus d P over d V by V equals P. The left side is exactly the bulk modulus. So the isothermal bulk modulus of a gas is simply its pressure.",
                "Put that into v equals root E over rho, and you get Newton's formula: v equals the square root of P over rho."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        self.play(FadeOut(VGroup(L[:3])), VGroup(title, L[3]).animate.shift(UP * 0.0))
        self.play(L[3].animate.next_to(title, DOWN, buff=0.4))
        tst = M(r"v = \sqrt{\frac{1.013\times10^{5}}{1.293}} = \sqrt{7.835\times10^{4}} = 280\ \text{m s}^{-1}", size=40).next_to(L[3], DOWN, buff=0.5)
        with self.say("Test it on air at normal temperature and pressure. P is one point zero one three times ten to the five pascals, and rho is one point two nine three kilograms per cubic metre. The square root comes out at two hundred and eighty metres per second."):
            self.play(Write(tst))
        base = -2.9
        b1 = Rectangle(width=1.4, height=3.0 * 280 / 332, fill_color=C_N, fill_opacity=0.9, stroke_width=0).move_to([-1.2, base, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.4, height=3.0 * 0.0 + 3.0, fill_color=C_L, fill_opacity=0.9, stroke_width=0).move_to([1.2, base, 0], aligned_edge=DOWN)
        b2.stretch_to_fit_height(1.6).move_to([1.2, base, 0], aligned_edge=DOWN)
        b1.stretch_to_fit_height(1.6 * 280 / 332).move_to([-1.2, base, 0], aligned_edge=DOWN)
        bl = VGroup(T("Newton 280", size=22, color=C_N).next_to(b1, LEFT, buff=0.15), T("measured 332", size=22, color=C_L).next_to(b2, RIGHT, buff=0.15))
        err = T("16 % too low!", size=28, color=C_N, weight="BOLD").move_to([0, -0.95, 0])
        with self.say("But the measured value at zero degrees is about three hundred and thirty two. Newton was short by fifty two metres per second, an error of about sixteen percent. No experiment of that era was that bad. The assumption had to be wrong."):
            self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(bl))
            self.play(FadeIn(err, scale=1.3))
        nb = neby_in(self, "think", corner=DL)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, L[3], tst, b1, b2, bl, err)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        t = clock(self, 1.0)
        f = 1.3
        xs = np.linspace(-6.2, 6.2, 44)
        k = TAU / 3.2
        layers = VGroup(*[Line([x, -0.6, 0], [x, 1.4, 0], stroke_width=3) for x in xs])

        def upd(m):
            ph = TAU * f * t.get_value()
            for ln, x in zip(m, xs):
                dens = np.cos(ph - k * x)
                ln.set_x(x + 0.28 * np.sin(ph - k * x))
                ln.set_color(heat_color(0.5 + 0.5 * dens))
        layers.add_updater(upd)
        lab = VGroup(T("compressions warm up", size=24, color=C_N), T("rarefactions cool down", size=24, color=th.SKY)).arrange(RIGHT, buff=1.2).move_to([0, 2.2, 0])
        with self.say("In eighteen sixteen, Laplace found the mistake. When a sound wave squeezes a layer of air, the layer warms up. When it stretches it, the layer cools. The question is whether that heat has time to escape."):
            self.add(layers)
            self.play(FadeIn(layers), FadeIn(lab))
            self.wait(3)
        pts = VGroup(T("• even the lowest sound, 20 Hz, squeezes each layer 20 times a second", size=24, color=th.BODY),
                     T("• at 1000 Hz a compression lasts about half a millisecond", size=24, color=th.BODY),
                     T("• and air is a very poor conductor of heat", size=24, color=th.BODY),
                     T("no heat has time to flow: the changes are ADIABATIC", size=28, color=th.AMBER, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.1, 0])
        with self.say("It does not. Even the lowest sound we can hear, twenty hertz, squeezes each layer twenty times a second. At a thousand hertz, a compression lasts only half a millisecond. And air is a very poor conductor of heat. So practically no heat leaves a compression, or enters a rarefaction. The changes are not isothermal. They are adiabatic.") as v_:
            for p_ in pts:
                self.play(FadeIn(p_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v_.dur / 4 - 0.7)
        self.play(FadeOut(VGroup(lab, pts)), FadeOut(layers))
        layers.clear_updaters()
        self.remove(layers, t)
        title = T("Laplace's correction", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(M(r"PV^{\gamma} = \text{constant},\qquad \gamma = \frac{C_p}{C_v}", size=42), M(r"\gamma PV^{\gamma - 1}\,dV + V^{\gamma}\,dP = 0", size=42),
                   M(r"-\frac{dP}{dV/V} = \gamma P \;\Rightarrow\; B_{\text{adi}} = \gamma P", size=42), M(r"v = \sqrt{\frac{\gamma P}{\rho}}", size=64, color=C_L)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.4)
        says = ["For an adiabatic change of an ideal gas, P V to the gamma is constant, where gamma is C p over C v.",
                "Differentiate the product: gamma P V to the gamma minus one d V, plus V to the gamma d P, equals zero.",
                "Divide through by V to the gamma minus one, and rearrange. The adiabatic bulk modulus is gamma P, gamma times the isothermal one.",
                "So the corrected speed is the square root of gamma P over rho."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        self.play(FadeOut(L[1:3]), L[3].animate.next_to(L[0], DOWN, buff=0.4))
        res = M(r"v = \sqrt{1.4}\times 280 = 1.183\times 280 = 331\ \text{m s}^{-1}\ \checkmark", size=42, color=C_L).next_to(L[3], DOWN, buff=0.5)
        with self.say("For air, gamma is one point four. Multiply Newton's two hundred and eighty by root one point four, one point one eight three, and you get three hundred and thirty one metres per second. It agrees with experiment."):
            self.play(Write(res))
            nb = neby_in(self, "celebrate", corner=DR)
        self.play(FadeOut(VGroup(title, L, res)))
        neby_out(self, nb)
        self.steeper()
        self.compare_table()
        example(self, "Calculate the velocity of sound in hydrogen at 0 °C: γ = 1.4, P = 1.013 × 10⁵ Pa, density 0.09 kg/m³. Compare it with air (1.293 kg/m³).",
                [r"v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{1.4\times1.013\times10^{5}}{0.09}} = \sqrt{1.576\times10^{6}} = 1.26\times10^{3}\ \text{m s}^{-1}",
                 r"\frac{v_{\text{H}}}{v_{\text{air}}} = \sqrt{\frac{\rho_{\text{air}}}{\rho_{\text{H}}}} = \sqrt{\frac{1.293}{0.09}} = 3.79"],
                ["Worked example. Find the velocity of sound in hydrogen at zero degrees Celsius, and compare it with air.",
                 "Use Laplace's formula. One point four times one point zero one three times ten to the five, over zero point zero nine. The square root is about twelve hundred and sixty metres per second.",
                 "Both are diatomic, with the same gamma and the same pressure, so the ratio of speeds is the square root of the inverse ratio of densities: root of one point two nine three over zero point zero nine, about three point eight. Sound is nearly four times faster in hydrogen, because it is so light while just as stiff."], size=36)
        self.quiz("Laplace's correction to Newton's formula multiplies the velocity by",
                  [M(r"\gamma", size=40), M(r"\sqrt{\gamma}", size=40), M(r"1/\gamma", size=40), M(r"\gamma^{2}", size=40)], 1,
                  "Pause and think. Laplace's correction multiplies Newton's velocity by what?",
                  "B, root gamma. The modulus changes from P to gamma P, and the speed is the square root of the modulus, so it goes up by the square root of gamma. If you picked gamma, you forgot the square root.")

    def steeper(self):
        g = pv_axes(xr=(0, 6, 1), yr=(0, 6, 1), x_len=5.6, y_len=4.2).move_to([-3.0, -0.4, 0])
        ax = g[0]
        iso = ax.plot(lambda v: 8 / v, x_range=[1.4, 5.8], color=C_N, stroke_width=5)
        adi = ax.plot(lambda v: 4 * (2 / v) ** 1.4, x_range=[1.3, 5.8], color=C_L, stroke_width=5)
        A = ax.c2p(2, 4)
        lab = VGroup(T("isothermal: B = P", size=20, color=C_N).move_to(ax.c2p(4.2, 3.2)),
                     T("adiabatic: B = γP", size=20, color=C_L).next_to(ax.c2p(1.6, 1.2), RIGHT, buff=0.1))
        txt = para("Through the same state, the adiabatic curve is γ times steeper: the gas is harder to squeeze, so the wave travels faster.", width=4.4, size=26, color=th.INK).move_to([4.3, 0.4, 0])
        with self.say("Here is the picture behind the gamma. Through the same state, the adiabatic curve is steeper than the isothermal, by exactly the factor gamma. A steeper curve means a bigger pressure rise for the same squeeze. The gas is stiffer, so the wave travels faster."):
            self.play(Create(g), Create(iso), Create(adi), FadeIn(Dot(A, color=WHITE)), FadeIn(lab))
            self.play(FadeIn(txt))
        self.clear_stage(run_time=0.5)

    def compare_table(self):
        title = T("Newton vs Laplace", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        rows = [("", "Newton", "Laplace"), ("process", "isothermal", "adiabatic"), ("reason", "heat escapes at once", "fast changes, poor conductor"),
                ("bulk modulus", "B = P", "B = γP"), ("formula", "v = √(P/ρ)", "v = √(γP/ρ)"), ("air at 0 °C", "280 m/s, 16 % low", "331 m/s, agrees")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=26 if i else 30, color=(th.BG if not c else ([th.MUTED, C_N, C_L][j] if i == 0 or j == 0 else th.BODY)),
                             weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            row.scale(0.92)
            for j, x in enumerate([-4.9, -1.3, 3.3]):
                row[j].move_to([x, 2.0 - i * 0.72, 0])
            grid.add(row)
        with self.say("Side by side. Newton assumed isothermal changes, so B equals P, giving two hundred and eighty metres per second, sixteen percent too low. Laplace realised the changes are adiabatic, so B equals gamma P, giving three hundred and thirty one, which agrees.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(title, grid)))
        self.tip("Laplace did not change the formula v = √(B/ρ), only the modulus: compressions are adiabatic, so B = γP instead of P. It has nothing to do with sound being longitudinal.",
                 "A very common slip in exams: writing that Laplace's correction is needed because sound is longitudinal. That has nothing to do with it. The only change is that the compressions are adiabatic, so the bulk modulus is gamma P, not P. Say that sentence, and the mark is yours.", state="wink")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("Where did the pressure go?", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(M(r"\rho = \frac{nM}{V},\qquad PV = nRT", size=44), M(r"\frac{P}{\rho} = \frac{RT}{M}", size=48),
                   M(r"v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{\gamma R T}{M}}", size=60, color=C_L)).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.5)
        with self.say("To see what really matters, get rid of the density. For n moles of gas of molar mass M in volume V, rho is n M over V, and P V equals n R T."):
            self.play(FadeIn(title), Write(L[0]))
        with self.say("Divide, and P over rho is R T over M. So the speed of sound in a gas is the square root of gamma R T over M. Look closely: there is no pressure in it at all."):
            self.play(Write(L[1]))
            self.sfx("impact", gain=-12)
            self.play(Write(L[2]))
        self.play(FadeOut(VGroup(title, L[0], L[1])), L[2].animate.scale(0.7).to_corner(UR, buff=0.7))
        self.pressure_demo()
        self.temperature_graph()
        self.play(FadeOut(L[2]))
        example(self, "The velocity of sound in air at 0 °C is 332 m/s. Find its value at 27 °C (a) exactly, (b) using the linear rule.",
                [r"v_{27} = 332\sqrt{\frac{300}{273}} = 332 \times 1.0483 = 348\ \text{m s}^{-1}",
                 r"v_{27} \approx 332 + 0.61\times 27 = 332 + 16.5 = 348.5\ \text{m s}^{-1}"],
                ["Worked example. Sound travels at three hundred and thirty two metres per second at zero degrees. Find its speed at twenty seven degrees, exactly, and with the linear rule.",
                 "Exactly: three hundred and thirty two, times the square root of three hundred over two seventy three. That is three hundred and thirty two times one point zero four eight three, about three hundred and forty eight.",
                 "With the rule: three thirty two plus zero point six one times twenty seven, three hundred and forty eight point five. The two agree within half a metre per second, so the linear rule is perfectly safe for everyday temperatures."], size=40)
        self.quiz("If the absolute temperature of a gas is made four times, the velocity of sound in it becomes",
                  ["half", "twice", "four times", "unchanged"], 1,
                  "Pause and think. Make the absolute temperature of a gas four times bigger. What happens to the speed of sound?",
                  "B, twice. The speed goes as the square root of T, and the square root of four is two. Four times is the trap for anyone who forgets the square root.")
        self.humidity_wind()
        self.quiz("The velocity of sound in moist air is",
                  ["greater than in dry air", "less than in dry air", "equal to that in dry air", "zero"], 0,
                  "Pause and think. Compared with dry air at the same temperature and pressure, is sound faster or slower in moist air?",
                  "A, greater. Water vapour, with molar mass eighteen, is lighter than the nitrogen and oxygen it replaces, so moist air is less dense, and v goes as one over root rho. Many students guess slower, thinking wet air is heavier. It is the other way round.")
        self.echo()
        example(self, "A gun is fired in a valley at Pokhara and the echo from a cliff is heard after 2.5 s at 20 °C (v₀ = 332 m/s). Find the distance of the cliff. By how much does the echo time change when the air cools to 5 °C?",
                [r"v_{20} = 332 + 0.61\times 20 = 344.2\ \text{m s}^{-1}",
                 r"2d = 344.2 \times 2.5 = 860.5\ \text{m} \;\Rightarrow\; d = 430\ \text{m}",
                 r"v_{5} = 332 + 0.61\times 5 = 335.05\ \text{m s}^{-1}",
                 r"t = \frac{860.5}{335.05} = 2.57\ \text{s}\quad (\text{about } 0.07\ \text{s longer})"],
                ["One more, a full long question. A gun is fired in a valley at Pokhara, and the echo from a cliff comes back after two and a half seconds, at twenty degrees. Find the distance of the cliff. Then the air cools to five degrees. How does the echo time change?",
                 "At twenty degrees, the speed is three thirty two plus zero point six one times twenty: three hundred and forty four point two.",
                 "There and back is two d: three forty four point two times two point five, eight hundred and sixty point five metres. So the cliff is about four hundred and thirty metres away.",
                 "At five degrees, the speed drops to three hundred and thirty five point zero five.",
                 "The cliff has not moved, so the echo now takes eight sixty point five over three thirty five point zero five: two point five seven seconds. About seven hundredths of a second longer. Small, but measurable, which is why every echo or resonance tube experiment must record the air temperature."], size=40)

    def pressure_demo(self):
        cx, yb = -3.4, -2.6
        s = ValueTracker(1.0)
        cyl = Cylinder(cx, yb, 2.4, 4.4, lambda: 3.6 * s.get_value(), lambda: 300, n=40, rod=0.4)
        ro = VGroup(readout("P =", lambda: 1 / s.get_value(), "× P₀", decimals=2, size=28, color=th.CORAL),
                    readout("ρ =", lambda: 1 / s.get_value(), "× ρ₀", decimals=2, size=28, color=C_R),
                    readout("P/ρ =", lambda: 1.0, "", decimals=2, size=28, color=C_L),
                    readout("v =", lambda: 331.0, "m/s", decimals=0, size=28, color=C_V)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -0.4, 0])
        with self.say("First, pressure. Keep the temperature fixed, and squeeze the gas to double its pressure. By Boyle's law its volume halves, so its density doubles too. P over rho does not change, and neither does the speed."):
            self.play(Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(ro))
            self.play(s.animate.set_value(0.5), run_time=3)
            self.play(Indicate(ro[3], color=WHITE))
        with self.say("So sound in Kathmandu, high up where the pressure is lower, travels no faster than in Biratnagar at the same temperature. Any difference you notice comes from temperature, not pressure."):
            self.play(s.animate.set_value(1.0), run_time=2.5)
        self.play(FadeOut(ro))
        cyl.drop(self)

    def temperature_graph(self):
        ax = Axes(x_range=[-10, 45, 10], y_range=[320, 362, 10], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([-2.6, -0.6, 0])
        xl = T("temperature t (°C)", size=22, color=th.BODY).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = T("v (m/s)", size=22, color=C_V).next_to(ax.y_axis.get_top(), UP, buff=0.1)
        exact = ax.plot(lambda t: 332 * np.sqrt((273 + t) / 273), x_range=[-10, 45], color=C_V, stroke_width=5)
        lin = DashedVMobject(ax.plot(lambda t: 332 + 0.61 * t, x_range=[-10, 45], color=th.AMBER, stroke_width=3), num_dashes=40)
        eqs = VGroup(M(r"v \propto \sqrt{T}\quad (T \text{ in K})", size=36), M(r"v_t = v_0\sqrt{1 + \frac{t}{273}} \approx v_0\left(1 + \frac{t}{546}\right)", size=34),
                     M(r"v_t \approx 332 + 0.61\,t", size=40, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 0.6, 0])
        if eqs.width > 4.6:
            eqs.scale_to_fit_width(4.6).move_to([4.3, 0.4, 0])
        tt = ValueTracker(-10)
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), 332 * np.sqrt((273 + tt.get_value()) / 273)), color=WHITE))
        ro = readout("v =", lambda: 332 * np.sqrt((273 + tt.get_value()) / 273), "m/s", decimals=1, size=26, color=C_V).move_to([4.2, -1.9, 0])
        rt = readout("t =", lambda: tt.get_value(), "°C", decimals=0, size=26).next_to(ro, UP, buff=0.15).align_to(ro, LEFT)
        with self.say("Temperature is the one that matters. From root gamma R T over M, at a fixed composition the speed goes as the square root of the absolute temperature."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Write(eqs[0]))
            self.play(Create(exact))
            self.add(dot)
            self.play(FadeIn(rt), FadeIn(ro))
            self.play(tt.animate.set_value(40), run_time=3)
        with self.say("So if v nought is the speed at zero degrees, the speed at t degrees is v nought times the root of one plus t over two seventy three. For small t, the binomial approximation turns the square root into one plus t over five forty six."):
            self.play(Write(eqs[1]))
        with self.say("With v nought equal to three hundred and thirty two, that is three hundred and thirty two plus zero point six one t. The speed of sound in air rises by about zero point six one metres per second for every degree. The dashed line shows how good this rule is over ordinary Nepali temperatures."):
            self.play(Write(eqs[2]), Create(lin))
            self.play(tt.animate.set_value(15), run_time=2)
        self.play(FadeOut(VGroup(ax, xl, yl, exact, lin, eqs, ro, rt)), FadeOut(dot))
        self.remove(dot)

    def humidity_wind(self):
        box1 = Square(3.0, stroke_color=th.BODY, stroke_width=3).move_to([-4.4, 0.3, 0])
        box2 = Square(3.0, stroke_color=th.BODY, stroke_width=3).move_to([-0.8, 0.3, 0])
        g1 = Gas(lambda: (box1.get_left()[0] + 0.05, box1.get_right()[0] - 0.05, box1.get_bottom()[1] + 0.05, box1.get_top()[1] - 0.05), n=24, seed=2, fill=th.BODY, radius=0.1)
        g2 = Gas(lambda: (box2.get_left()[0] + 0.05, box2.get_right()[0] - 0.05, box2.get_bottom()[1] + 0.05, box2.get_top()[1] - 0.05), n=24, seed=3, fill=th.BODY, radius=0.1)
        for i in range(0, 24, 3):
            g2[i].set_color(th.SKY).scale(0.7)
        l1 = T("dry air  (M ≈ 28.8)", size=22).next_to(box1, DOWN, buff=0.15)
        l2 = T("moist air: some H₂O (M = 18)", size=22, color=th.SKY).next_to(box2, DOWN, buff=0.15)
        txt = para("Same P and T, same number of molecules, but lighter ones: moist air is less dense, so sound is slightly faster.", width=4.4, size=24, color=th.INK).move_to([4.4, 0.3, 0])
        with self.say("Humidity raises the speed a little. A water molecule has a molar mass of eighteen, while dry air averages about twenty nine. At the same pressure and temperature, water vapour replaces some of the heavier nitrogen and oxygen molecules. So moist air is less dense, and sound travels slightly faster. That is one reason distant sounds carry so well in the heavy air before a monsoon shower."):
            self.add(g1, g2)
            self.play(Create(box1), Create(box2), FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2))
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(box1, box2, l1, l2, txt)), FadeOut(g1), FadeOut(g2))
        self.remove(g1, g2)
        th_ = ValueTracker(0.0)
        O = np.array([-3.0, -0.4, 0])
        va = Arrow(O, O + RIGHT * 3.5, buff=0, color=C_V, stroke_width=7)
        wa = always_redraw(lambda: Arrow(O + RIGHT * 3.5, O + RIGHT * 3.5 + 1.4 * np.array([np.cos(th_.get_value()), np.sin(th_.get_value()), 0]), buff=0, color=th.MINT, stroke_width=6))
        eq = M(r"v_{\text{eff}} = v + w\cos\theta", size=50).move_to([3.6, 1.8, 0])
        ro = readout("v_eff =", lambda: 340 + 15 * np.cos(th_.get_value()), "m/s", decimals=0, size=28, color=th.MINT).move_to([3.6, -1.8, 0])
        labs = VGroup(T("sound, v = 340", size=22, color=C_V).next_to(va, DOWN, buff=0.15), T("wind, w = 15", size=22, color=th.MINT).move_to(O + RIGHT * 4.3 + UP * 1.0))
        with self.say("Wind is different. It does not change the speed of sound relative to the air. It carries the air itself along. If a wind of speed w blows at an angle theta to the sound, the speed over the ground is v plus w cos theta. Downwind, the sound gets a push. Upwind, it is held back. That is why sound carries further downwind."):
            self.play(GrowArrow(va), FadeIn(labs[0]), Write(eq))
            self.add(wa)
            self.play(FadeIn(wa), FadeIn(labs[1]), FadeIn(ro))
            self.play(th_.animate.set_value(PI), run_time=3)
            self.play(th_.animate.set_value(0), run_time=2)
        self.play(FadeOut(VGroup(va, eq, ro, labs)), FadeOut(wa))
        self.remove(wa)
        title = T("What changes the speed of sound in air?", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        rows = [("pressure (T fixed)", "no effect", th.MUTED), ("temperature", "increases, v ∝ √T", th.CORAL), ("humidity", "increases slightly", th.SKY),
                ("wind", "adds: v + w cos θ", th.MINT), ("loudness", "no effect", th.MUTED), ("pitch", "no effect", th.MUTED)]
        grid = VGroup(*[VGroup(T(a, size=26, color=th.INK), T(b, size=26, color=c, weight="SEMIBOLD")).arrange(RIGHT, buff=0.6) for a, b, c in rows]).arrange(DOWN, buff=0.28)
        for r in grid:
            r[0].set_x(-2.8)
            r[1].next_to(r[0], RIGHT, buff=0).set_x(1.0, direction=LEFT)
        grid.next_to(title, DOWN, buff=0.45)
        with self.say("Here is the summary table. Pressure at a fixed temperature: no effect. Temperature: the speed rises as root T. Humidity: a slight increase. Wind: adds as a vector. And loudness and pitch have no effect at all, because the speed is a property of the medium.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(title, grid)))

    def echo(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A trekker in Godavari claps facing a cliff and hears the echo 3.0 s later. The air is at 15 °C and sound travels at 332 m/s at 0 °C. How far is the cliff?", width=12.2, size=27, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        with self.say("A last worked example. A trekker in Godavari claps her hands facing a cliff, and hears the echo three seconds later. The air is at fifteen degrees. How far away is the cliff?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        P = np.array([-5.0, -1.6, 0])
        C = np.array([4.6, -1.6, 0])
        cliff = Polygon([4.6, -2.6, 0], [4.6, 0.8, 0], [5.4, 1.0, 0], [6.6, 1.0, 0], [6.6, -2.6, 0], stroke_width=0, fill_color="#5a4a3a", fill_opacity=1)
        ground = Line([-6.8, -2.6, 0], [6.8, -2.6, 0], color=th.MUTED, stroke_width=4)
        person = VGroup(Circle(radius=0.2, fill_color="#E9B48A", fill_opacity=1, stroke_width=0).move_to(P + UP * 0.55), Line(P + UP * 0.35, P + DOWN * 0.5, color=th.INK, stroke_width=5),
                        Line(P + DOWN * 0.5, P + DOWN * 1.0 + LEFT * 0.2, color=th.INK, stroke_width=5), Line(P + DOWN * 0.5, P + DOWN * 1.0 + RIGHT * 0.2, color=th.INK, stroke_width=5))
        t = ValueTracker(0)
        D = C[0] - P[0]

        def wave():
            s = t.get_value() * 2 * D
            if s <= D:
                return Arc(radius=max(0.05, s), start_angle=-0.5, angle=1.0, arc_center=P, color=C_V, stroke_width=5)
            r = 2 * D - s
            return Arc(radius=max(0.05, s - D), start_angle=PI - 0.5, angle=1.0, arc_center=C, color=th.AMBER, stroke_width=5)
        w = always_redraw(wave)
        self.play(prob.animate.scale(0.75).next_to(head, DOWN, aligned_edge=LEFT, buff=0.2), FadeIn(cliff), FadeIn(ground), FadeIn(person))
        self.add(w)
        self.sfx("pop", gain=-6)
        self.play(t.animate.set_value(1), run_time=3, rate_func=linear)
        self.sfx("pop", gain=-10)
        self.remove(w)
        steps = VGroup(M(r"v = 332 + 0.61\times 15 = 341.2\ \text{m s}^{-1}", size=38), M(r"2d = vt = 341.2 \times 3.0 = 1023.6\ \text{m}", size=38),
                       M(r"d = 512\ \text{m}\quad (\text{with } 332 \text{ alone: } 498\ \text{m})", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.2, 0.0, 0])
        with self.say("First, correct the speed for temperature: three thirty two plus zero point six one times fifteen, three hundred and forty one point two metres per second."):
            self.play(Write(steps[0]))
        with self.say("The sound goes to the cliff and back, so the path is two d. Two d equals v t: three forty one point two times three, one thousand and twenty three point six metres."):
            self.play(Write(steps[1]))
        with self.say("So the cliff is about five hundred and twelve metres away. Using the uncorrected three thirty two would have given four ninety eight, fourteen metres short. That is why the temperature correction is worth doing."):
            self.play(Write(steps[2]))
            nb = neby_in(self, "success", corner=UR)
        self.play(FadeOut(VGroup(head, prob, cliff, ground, person, steps)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"v = \sqrt{E/\rho}:\ \text{stiffness over inertia; the medium sets the speed}", size=34),
            M(r"\text{rod } \sqrt{Y/\rho}\ (\approx 5060),\ \ \text{liquid } \sqrt{B/\rho}\ (\approx 1480)\ \text{m s}^{-1}", size=34),
            "Fluids carry only longitudinal sound; solids carry longitudinal (P) and transverse (S) waves.",
            M(r"\text{Newton (isothermal): } B = P,\ v = \sqrt{P/\rho} = 280\ \text{m s}^{-1}\ (16\%\ \text{low})", size=32),
            M(r"\text{Laplace (adiabatic): } B = \gamma P,\ v = \sqrt{\gamma P/\rho} = 331\ \text{m s}^{-1}", size=32),
            M(r"v = \sqrt{\gamma RT/M}:\ \text{no } P;\ \ v_t \approx v_0 + 0.61\,t", size=34),
            "Humidity raises v slightly; wind adds v + w cos θ; loudness and pitch change nothing.",
        ], "Let us recap. The speed of a mechanical wave is the square root of the right elastic modulus over the density. Sound races through steel at about five thousand metres per second, and through water at about fifteen hundred. Fluids carry only longitudinal waves. Newton assumed isothermal changes and got two eighty, sixteen percent low. Laplace showed they are adiabatic, so B is gamma P, giving three thirty one. The speed depends on temperature, not pressure, rising by about zero point six one metres per second per degree.")
        self.outro("That is the speed of mechanical waves. Next, we trap waves inside pipes and on strings, and find out why a flute and a sarangi sing the notes they do. See you there, on NEBians.")
