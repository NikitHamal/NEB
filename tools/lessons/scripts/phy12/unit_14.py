import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import (Stream, cell, clock, curve, example, galvo, neby_in, neby_out, needle_meter, readout,  # noqa: E402
                   resistor, wire)

C_I, C_V, C_R, C_E = th.AMBER, th.SKY, th.PINK, th.MINT


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 14
    TITLE = "Electrical Circuits"
    SUBTITLE = "Kirchhoff, bridges, potentiometers and heat"
    SECTIONS = ["Kirchhoff's laws", "Wheatstone and metre bridge", "The potentiometer", "Superconductors",
                "Ammeters, voltmeters, ohmmeters", "Joule's law"]
    NEXT = "Unit 15 · Thermoelectric Effects"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ the two-cell network of example 14.1
    def network(self, cur=(2.0, 1.0, 3.0), show_flow=True, labels=True):
        xl, xm, xr, yt, yb = -4.0, 0.0, 4.0, 1.6, -1.8
        g = VGroup(wire([xl, yt, 0], [xr, yt, 0]), wire([xl, yb, 0], [xr, yb, 0]),
                   wire([xl, yt, 0], [xl, 0.6, 0]), cell([xl, -0.1, 0], [xl, 0.6, 0]), resistor([xl, -0.1, 0], [xl, -1.2, 0], zig=4), wire([xl, -1.2, 0], [xl, yb, 0]),
                   wire([xr, yt, 0], [xr, 0.6, 0]), cell([xr, -0.1, 0], [xr, 0.6, 0]), resistor([xr, -0.1, 0], [xr, -1.2, 0], zig=4), wire([xr, -1.2, 0], [xr, yb, 0]),
                   wire([xm, yt, 0], [xm, 0.5, 0]), resistor([xm, 0.5, 0], [xm, -0.7, 0], zig=5), wire([xm, -0.7, 0], [xm, yb, 0]),
                   Dot([xm, yt, 0], color=WHITE), Dot([xm, yb, 0], color=WHITE))
        lab = VGroup(M(r"E_1 = 10\,\text{V}", size=28, color=C_E).next_to([xl, 0.25, 0], LEFT, buff=0.45), M(r"r_1 = 2\,\Omega", size=28).next_to([xl, -0.65, 0], LEFT, buff=0.35),
                     M(r"E_2 = 9\,\text{V}", size=28, color=C_E).next_to([xr, 0.25, 0], RIGHT, buff=0.45), M(r"r_2 = 3\,\Omega", size=28).next_to([xr, -0.65, 0], RIGHT, buff=0.35),
                     M(r"R = 2\,\Omega", size=28).next_to([xm, -0.1, 0], RIGHT, buff=0.35), M("A", size=30).next_to([xm, yt, 0], UP, buff=0.12), M("B", size=30).next_to([xm, yb, 0], DOWN, buff=0.12)) if labels else VGroup()
        flows = VGroup()
        if show_flow:
            i1, i2, i3 = cur
            flows = VGroup(Stream([[xl, yb, 0], [xl, yt, 0], [xm, yt, 0]], n=8, speed=0.6 * i1, color=C_I),
                           Stream([[xr, yb, 0], [xr, yt, 0], [xm, yt, 0]], n=8, speed=0.6 * i2, color=C_V),
                           Stream([[xm, yt, 0], [xm, yb, 0]], n=6, speed=0.6 * i3, color=th.CORAL),
                           Stream([[xm, yb, 0], [xl, yb, 0]], n=5, speed=0.6 * i1, color=C_I),
                           Stream([[xm, yb, 0], [xr, yb, 0]], n=5, speed=0.6 * i2, color=C_V))
        return g, lab, flows

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        g, lab, fl = self.network()
        qs = VGroup(*[T("?", size=44, color=th.AMBER, weight="BOLD").move_to(p) for p in ([-4.6, 1.1, 0], [4.6, 1.1, 0], [0.5, 1.0, 0])])
        with self.say("Two batteries, one of ten volts and one of nine, wired into the same circuit with a resistor between them. Which way does the current flow in each wire? And how much?"):
            self.play(Create(g), run_time=2)
            self.play(FadeIn(lab))
            self.play(LaggedStart(*[FadeIn(q, scale=1.5) for q in qs], lag_ratio=0.2))
        nb = neby_in(self, "think", corner=DR)
        with self.say("Ohm's law alone cannot tell you. The circuit is neither series nor parallel, and the two cells push against each other. You need two rules that can solve any circuit at all. They are Kirchhoff's laws, and by the end of part one, you will know every current here."):
            self.play(Indicate(qs, color=WHITE))
        self.play(FadeOut(VGroup(g, lab, qs)))
        neby_out(self, nb)
        g_, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 14: Electrical Circuits. We will learn Kirchhoff's laws, use them on the Wheatstone bridge, the metre bridge and the potentiometer, meet superconductors, turn a galvanometer into ammeters and voltmeters, and finish with what current actually does in a resistor: it heats it."):
            pass
        self.end_title(g_, nb)
        self.roadmap("Here is the path. Kirchhoff's laws, the Wheatstone and metre bridges, the potentiometer, superconductors, converting a galvanometer into an ammeter, voltmeter and ohmmeter, and Joule's law of heating.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        J = np.array([-2.6, 0.2, 0])
        ins = [(np.array([-5.6, 2.0, 0]), 3), (np.array([-5.6, -1.6, 0]), 2)]
        outs = [(np.array([0.4, 2.0, 0]), 4), (np.array([0.4, -1.6, 0]), 1)]
        wires_ = VGroup(*[Line(p, J, color=th.BODY, stroke_width=4) for p, _ in ins + outs])
        st = VGroup(*[Stream([p, J], n=6, speed=0.35 * i, color=C_I) for p, i in ins], *[Stream([J, p], n=6, speed=0.35 * i, color=C_V) for p, i in outs])
        labs = VGroup(*[T(f"{i} A in", size=24, color=C_I).next_to(p, UP, buff=0.1) for p, i in ins], *[T(f"{i} A out", size=24, color=C_V).next_to(p, UP, buff=0.1) for p, i in outs])
        jd = Dot(J, radius=0.12, color=WHITE)
        law1 = VGroup(T("First law (junction law)", size=28, color=C_I, weight="BOLD"), M(r"\sum I = 0", size=56),
                      para("Currents in count positive, currents out negative. Charge cannot pile up at a point: conservation of charge.", width=5.0, size=22, color=th.BODY)).arrange(DOWN, buff=0.25).move_to([4.0, 0.3, 0])
        with self.say("A junction is a point where three or more wires meet. Here, three amps and two amps flow in. Four amps and one amp flow out. Five in, five out."):
            self.play(Create(wires_), FadeIn(jd))
            self.add(st)
            self.play(FadeIn(labs))
        with self.say("That is Kirchhoff's first law, the junction law. The algebraic sum of the currents at a junction is zero, counting currents in as positive and currents out as negative. Charge cannot pile up at a point, so it is really the conservation of charge."):
            self.play(FadeIn(law1, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(wires_, jd, labs, law1)), FadeOut(st))
        self.remove(st)
        self.loop_law()
        self.solve_network()

    def loop_law(self):
        pts = [np.array(p) for p in ([-5.6, 1.6, 0], [-0.6, 1.6, 0], [-0.6, -1.8, 0], [-5.6, -1.8, 0])]
        loop = VGroup(cell([-5.6, -0.6, 0], [-5.6, 0.4, 0]), wire([-5.6, 0.4, 0], pts[0], pts[1], [-0.6, 1.0, 0]), resistor([-0.6, 1.0, 0], [-0.6, -0.4, 0], zig=5),
                      wire([-0.6, -0.4, 0], pts[2], [-3.6, -1.8, 0]), resistor([-3.6, -1.8, 0], [-5.0, -1.8, 0], zig=4), wire([-5.0, -1.8, 0], pts[3], [-5.6, -0.6, 0]))
        t = ValueTracker(0)
        path = [np.array([-5.6, -0.6, 0]), np.array([-5.6, 1.6, 0]), np.array([-0.6, 1.6, 0]), np.array([-0.6, -1.8, 0]), np.array([-5.6, -1.8, 0]), np.array([-5.6, -0.6, 0])]
        pv = VMobject().set_points_as_corners(path)
        V = lambda s: (10 if s > 0.0 else 0) - (6 if s > 0.45 else 0) - (4 if s > 0.75 else 0)
        dot = always_redraw(lambda: Dot(pv.point_from_proportion(min(t.get_value(), 0.999)), radius=0.14, color=th.AMBER))
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 11, 5], x_length=4.4, y_length=2.4, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([3.8, -1.6, 0])
        hist = always_redraw(lambda: ax.plot(lambda s: (10 if s > 0.01 else 0) - (6 if s > 0.42 else 0) - (4 if s > 0.78 else 0), x_range=[0, max(0.005, t.get_value()), 0.002], color=th.AMBER, stroke_width=4, use_smoothing=False))
        yl = T("potential (V)", size=20, color=th.AMBER).next_to(ax, UP, buff=0.1)
        lab = VGroup(T("E = 10 V", size=22, color=C_E).next_to([-5.6, -0.1, 0], RIGHT, buff=0.45), T("6 V drop", size=22, color=th.CORAL).next_to([-0.6, 0.3, 0], RIGHT, buff=0.35),
                     T("4 V drop", size=22, color=th.CORAL).next_to([-4.3, -1.8, 0], DOWN, buff=0.3))
        with self.say("The second law is about loops: any closed path round a circuit. Carry a unit charge once round this loop. The cell lifts it up by ten volts. The resistors take it back down, six volts and then four."):
            self.play(Create(loop), FadeIn(lab))
            self.add(dot, hist)
            self.play(Create(ax), FadeIn(yl))
            self.play(t.animate.set_value(1.0), run_time=5, rate_func=linear)
        law2 = VGroup(T("Second law (loop law)", size=28, color=C_E, weight="BOLD"), M(r"\sum E = \sum IR", size=52),
                      para("Back where it started, the charge is at the same potential: conservation of energy.", width=4.6, size=22, color=th.BODY)).arrange(DOWN, buff=0.2).move_to([3.8, 1.85, 0])
        with self.say("Back at the start, it is at the same potential it began with. All the lifts must equal all the drops. Around any closed loop, the sum of the e m fs equals the sum of the I R drops. That is Kirchhoff's second law, and it is the conservation of energy."):
            self.play(FadeIn(law2, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(loop, lab, ax, yl, law2)), FadeOut(dot), FadeOut(hist))
        self.remove(dot, hist)
        title = T("Sign rules that never fail", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        rows = [("resistor, walking WITH the assumed current", "− IR"), ("resistor, walking AGAINST the assumed current", "+ IR"),
                ("cell, entering at − and leaving at +", "+ E"), ("cell, entering at + and leaving at −", "− E")]
        grid = VGroup(*[VGroup(T(a, size=26, color=th.BODY), T(b, size=30, color=th.AMBER, weight="BOLD")) for a, b in rows])
        for k, r in enumerate(grid):
            r[0].move_to([-1.4, 1.6 - k * 0.8, 0])
            r[1].move_to([4.6, 1.6 - k * 0.8, 0])
        note = para("Set the sum to zero. If a current comes out negative, it simply flows the other way: the size is still right. Never redraw.", width=11, size=26, color=C_E).to_edge(DOWN, buff=0.6)
        with self.say("Here are the sign rules. Pick a direction to walk round the loop. A resistor walked along the assumed current gives minus I R; against it, plus I R. A cell walked from minus to plus gives plus E; from plus to minus, minus E. Set the total to zero. And if a current comes out negative, it just flows the other way. The size is still right, so never redraw.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v_.dur / 5 - 0.6)
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(title, grid, note)))

    def solve_network(self):
        g, lab, fl = self.network()
        grp = VGroup(g, lab)
        self.play(FadeIn(grp))
        self.play(grp.animate.scale(0.62).to_edge(LEFT, buff=0.3).shift(UP * 0.5))
        L = VGroup(M(r"\text{junction A: } I_3 = I_1 + I_2", size=34),
                   M(r"\text{loop 1: } 10 = 2I_1 + 2(I_1 + I_2) = 4I_1 + 2I_2", size=34),
                   M(r"\text{loop 2: } 9 = 3I_2 + 2(I_1 + I_2) = 2I_1 + 5I_2", size=34),
                   M(r"I_2 = 5 - 2I_1\ \Rightarrow\ 2I_1 + 5(5 - 2I_1) = 9\ \Rightarrow\ I_1 = 2\ \text{A}", size=34),
                   M(r"I_1 = 2\ \text{A},\quad I_2 = 1\ \text{A},\quad I_3 = 3\ \text{A}", size=40, color=C_I)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        L.scale_to_fit_width(min(L.width, 7.0)).move_to([3.0, 0.2, 0])
        says = ["Now solve the opening puzzle. Let I one and I two flow up through the two cells towards junction A, and I three flow down through R. The junction law at A says I three equals I one plus I two.",
                "Walk round the left loop, with the currents: ten volts equals two I one plus two I three, which is four I one plus two I two.",
                "Walk round the right loop: nine volts equals three I two plus two I three, which is two I one plus five I two.",
                "From the first equation, I two is five minus two I one. Substitute into the second, and I one comes out at two amps.",
                "So I one is two amps, I two is one amp, and I three is three amps. All positive, so every guess about direction was right."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(FadeOut(grp), FadeOut(L))
        g, lab, fl = self.network(cur=(2.0, 1.0, 3.0))
        cl = VGroup(T("2 A", size=26, color=C_I).move_to([-4.6, 1.15, 0]), T("1 A", size=26, color=C_V).move_to([4.6, 1.15, 0]), T("3 A", size=26, color=th.CORAL).move_to([0.6, 1.1, 0]))
        chk = para("Check: A sits at I₃R = 6 V. The left cell drops 10 − 6 = 4 V across 2 Ω: 2 A. The right cell drops 9 − 6 = 3 V across 3 Ω: 1 A.", width=11, size=24, color=C_E).to_edge(DOWN, buff=0.4)
        with self.say("Watch the currents flow. And check: A sits six volts above B, because three amps flow through two ohms. The left cell has ten minus six, four volts, across its two ohms: two amps. The right cell has nine minus six, three volts, across three ohms: one amp. It all fits."):
            self.play(FadeIn(g), FadeIn(lab))
            self.add(fl)
            self.play(FadeIn(cl))
            self.play(FadeIn(chk))
            self.wait(1)
        nb = neby_in(self, "success", corner=UR)
        self.wait(0.3)
        self.play(FadeOut(VGroup(g, lab, cl, chk)), FadeOut(fl))
        self.remove(fl)
        neby_out(self, nb)
        self.quiz("Kirchhoff's junction law is a consequence of the conservation of",
                  ["energy", "charge", "momentum", "magnetic flux"], 1,
                  "Pause and think. The junction law comes from conserving what?",
                  "B, charge. Charge cannot pile up at a junction, so what flows in must flow out. Energy is the trap: that is the loop law.")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        A, B, C, D = np.array([-3.4, 0.2, 0]), np.array([0, 2.2, 0]), np.array([3.4, 0.2, 0]), np.array([0, -1.8, 0])
        Sv = ValueTracker(3.0)
        P, Q, R = 2.0, 4.0, 3.0
        br = VGroup(resistor(A, B, zig=5), resistor(B, C, zig=5), resistor(A, D, zig=5), resistor(D, C, zig=5),
                    wire(A, [-4.6, 0.2, 0], [-4.6, -2.9, 0], [-0.4, -2.9, 0]), cell([-0.4, -2.9, 0], [0.4, -2.9, 0]), wire([0.4, -2.9, 0], [4.6, -2.9, 0], [4.6, 0.2, 0], C),
                    wire(B, [0, 0.62, 0]), wire([0, -0.22, 0], D), galvo([0, 0.2, 0]))
        nm = VGroup(M("A", size=30).next_to(A, LEFT, buff=0.1), M("B", size=30).next_to(B, UP, buff=0.1), M("C", size=30).next_to(C, RIGHT, buff=0.1), M("D", size=30).next_to(D, DOWN, buff=0.1),
                    M("P", size=32, color=C_I).move_to((A + B) / 2 + UL * 0.4), M("Q", size=32, color=C_I).move_to((B + C) / 2 + UR * 0.4),
                    M("R", size=32, color=C_V).move_to((A + D) / 2 + DL * 0.4), M("S", size=32, color=C_V).move_to((D + C) / 2 + DR * 0.4))
        dev = lambda: 3.0 * (Q / (P + Q) - Sv.get_value() / (R + Sv.get_value()))
        dial, needle = needle_meter([4.6, 2.2, 0], dev, r=0.9)
        ro = readout("S =", lambda: Sv.get_value(), "Ω", decimals=2, size=26, color=C_V).move_to([4.6, 0.9, 0])
        with self.say("Four resistors, P, Q, R and S, joined in a diamond A B C D. A cell across one diagonal, A C, and a galvanometer across the other, B D. This is the Wheatstone bridge."):
            self.play(Create(br), run_time=2)
            self.play(FadeIn(nm))
        with self.say("Adjust S, and watch the galvanometer. For most values it swings one way or the other. At exactly one value, it reads zero. Then the bridge is balanced."):
            self.add(needle)
            self.play(FadeIn(dial), FadeIn(needle), FadeIn(ro))
            self.play(Sv.animate.set_value(12.0), run_time=2.5)
            self.play(Sv.animate.set_value(6.0), run_time=2.5)
        grp = VGroup(br, nm)
        self.play(FadeOut(VGroup(dial, ro)), FadeOut(needle), grp.animate.scale(0.62).to_edge(LEFT, buff=0.3).shift(UP * 0.3))
        self.remove(needle)
        L = VGroup(M(r"I_g = 0:\ I_1 \text{ through } P, Q;\ \ I_2 \text{ through } R, S", size=32), M(r"V_B = V_D", size=34),
                   M(r"ABD:\ I_1P = I_2R\quad (1)", size=34), M(r"BCD:\ I_1Q = I_2S\quad (2)", size=34),
                   M(r"(1) \div (2):\quad \frac{P}{Q} = \frac{R}{S}", size=50, color=C_I)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        L.scale_to_fit_width(min(L.width, 6.8)).move_to([3.2, 0.2, 0])
        says = ["Now the balance condition, a favourite long question. At balance, no current flows through the galvanometer. So by the junction law, the current I one through P also flows on through Q, and I two through R flows on through S.",
                "No current through the galvanometer also means B and D are at the same potential.",
                "So the drop from A to B equals the drop from A to D: I one P equals I two R.",
                "And the drop from B to C equals the drop from D to C: I one Q equals I two S.",
                "Divide one by the other. The currents cancel, and P over Q equals R over S."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        note = para("No E, no internal resistance, no galvanometer resistance in the result: a null method, and very accurate.", width=6.6, size=22, color=th.AMBER).next_to(L, DOWN, buff=0.3)
        with self.say("Notice what is missing: the cell's e m f, its internal resistance, the galvanometer's resistance. None of them matter. That is why this null method is so accurate."):
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(grp, L, note)))
        self.metre_bridge()

    def metre_bridge(self):
        x0, x1, yw = -5.0, 5.0, -1.2
        Xv, Rv = 6.0, 4.0
        l = ValueTracker(30.0)
        wire_ = Line([x0, yw, 0], [x1, yw, 0], color=th.AMBER, stroke_width=6)
        scale = VGroup(*[Line([x0 + k * 1.0, yw - 0.25, 0], [x0 + k * 1.0, yw - 0.4 if k % 5 else yw - 0.5, 0], color=th.MUTED, stroke_width=2) for k in range(11)],
                       *[T(str(10 * k), size=16, color=th.MUTED).move_to([x0 + k * 1.0, yw - 0.7, 0]) for k in range(0, 11, 2)])
        strips = VGroup(wire([x0, yw, 0], [x0, 1.4, 0], [-3.2, 1.4, 0]), resistor([-3.2, 1.4, 0], [-1.2, 1.4, 0], zig=5), wire([-1.2, 1.4, 0], [0, 1.4, 0]),
                        resistor([0, 1.4, 0], [3.2, 1.4, 0], zig=5), wire([3.2, 1.4, 0], [x1, 1.4, 0], [x1, yw, 0]),
                        wire([x0, yw, 0], [x0, -2.5, 0], [-0.4, -2.5, 0]), cell([-0.4, -2.5, 0], [0.4, -2.5, 0]), wire([0.4, -2.5, 0], [x1, -2.5, 0], [x1, yw, 0]))
        labs = VGroup(M("X", size=34, color=C_R).next_to([-2.2, 1.4, 0], UP, buff=0.3), M(r"R = 4\,\Omega", size=30, color=C_V).next_to([1.6, 1.4, 0], UP, buff=0.3))
        jx = lambda: x0 + l.get_value() / 10
        jock = always_redraw(lambda: VGroup(wire([0, 1.4, 0], [0, 0.65, 0]), galvo([0, 0.3, 0], r=0.3), wire([0, -0.0, 0], [jx(), -0.4, 0], [jx(), yw + 0.1, 0]),
                                            Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to([jx(), yw + 0.12, 0])))
        dev = lambda: 2.5 * (l.get_value() / (100 - l.get_value()) - Xv / Rv) / (1 + Xv / Rv)
        dial, needle = needle_meter([4.6, 2.6, 0], dev, r=0.7)
        ro = readout("l =", lambda: l.get_value(), "cm", decimals=1, size=26, color=C_I).move_to([-4.6, 2.6, 0])
        with self.say("The metre bridge is a Wheatstone bridge built from one uniform wire, exactly a metre long, stretched along a scale. The unknown resistance X goes in the left gap, a known resistance R in the right gap. The two parts of the wire, either side of a sliding jockey, act as the other two arms."):
            self.play(Create(wire_), FadeIn(scale), Create(strips), FadeIn(labs))
            self.add(jock, needle)
            self.play(FadeIn(jock), FadeIn(dial), FadeIn(needle), FadeIn(ro))
        with self.say("Slide the jockey along until the galvanometer reads zero. Here, with R equal to four ohms, the balance point is sixty centimetres from the left end."):
            self.play(l.animate.set_value(80), run_time=2.5)
            self.play(l.animate.set_value(60), run_time=2.0)
        eq = VGroup(M(r"\frac{X}{R} = \frac{\sigma l}{\sigma(100 - l)}", size=36), M(r"X = R\,\frac{l}{100 - l}", size=46, color=C_R),
                    M(r"X = 4\times\frac{60}{40} = 6\ \Omega", size=36)).arrange(DOWN, buff=0.25).move_to([3.2, -0.2, 0]).scale(0.95)
        bg = BackgroundRectangle(eq, color=th.BG, fill_opacity=0.9, buff=0.15)
        with self.say("If the wire has resistance sigma per centimetre, the two parts are sigma l and sigma times one hundred minus l. The balance condition gives X equals R, l over one hundred minus l. Four times sixty over forty: six ohms."):
            self.play(FadeIn(bg), Write(eq))
        self.play(FadeOut(VGroup(wire_, scale, strips, labs, dial, ro, eq, bg)), FadeOut(jock), FadeOut(needle))
        self.remove(jock, needle)
        self.tip("Keep the null point between 40 cm and 60 cm (choose R to do this): the error in X is smallest near 50 cm. Then interchange X and R and average, to cancel the end resistances.",
                 "Two lab habits examiners love. Choose R so that the balance point lands near the middle, between forty and sixty centimetres, because that is where the error is smallest. Then swap X and R, take the reading again, and average. That cancels the small extra resistance of the copper strips at the ends.", state="wink")
        example(self, "In a metre bridge, X is in the left gap and 4 Ω in the right gap; the balance point is 60 cm from the left. Find X and the new balance point when X and R are interchanged.",
                [r"X = 4\times\frac{60}{40} = 6\ \Omega",
                 r"\frac{4}{6} = \frac{l'}{100 - l'}\ \Rightarrow\ 400 - 4l' = 6l'\ \Rightarrow\ l' = 40\ \text{cm}"],
                ["Worked example. The same bridge: X on the left, four ohms on the right, balance at sixty centimetres. Find X, and the balance point after swapping them.",
                 "X is four times sixty over forty: six ohms.",
                 "Swapped, four ohms is on the left: four over six equals l dash over one hundred minus l dash. So l dash is forty centimetres, simply one hundred minus sixty, as symmetry demands."], size=42)
        example(self, "In a metre bridge X is in the left gap and 6 Ω in the right gap; the balance point is 40 cm from the left end. Find X and the new balance length if they are interchanged.",
                [r"X = 6\times\frac{40}{60} = 4\ \Omega", r"\text{interchanged: } l' = 100 - 40 = 60\ \text{cm}"],
                ["One for you to check. Six ohms on the right, balance at forty centimetres.",
                 "X is six times forty over sixty: four ohms.",
                 "Interchange them, and the balance point moves to sixty centimetres."], size=44)
        self.quiz("In a balanced Wheatstone bridge, the current through the galvanometer is",
                  ["maximum", "zero", "half the main current", "equal to the main current"], 1,
                  "Pause and think. In a balanced Wheatstone bridge, how much current flows through the galvanometer?",
                  "B, zero. That null reading is the very definition of balance, and it is why B and D are at the same potential.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        x0, x1, yw = -5.5, 5.5, 0.6
        Lcm = 400.0
        k_ = 2.0e-3
        wire_ = Line([x0, yw, 0], [x1, yw, 0], color=th.AMBER, stroke_width=6)
        drv = VGroup(wire([x0, yw, 0], [x0, 2.4, 0], [-0.4, 2.4, 0]), cell([-0.4, 2.4, 0], [0.4, 2.4, 0], plus_at_b=False), wire([0.4, 2.4, 0], [x1, 2.4, 0], [x1, yw, 0]))
        drl = T("driver cell E₀ (steady current)", size=22, color=C_E).next_to([0, 2.4, 0], UP, buff=0.3)
        lbl = VGroup(M("A", size=30).next_to([x0, yw, 0], DL, buff=0.1), M("B", size=30).next_to([x1, yw, 0], DR, buff=0.1))
        pos = ValueTracker(0.0)
        Vmark = always_redraw(lambda: VGroup(Dot([x0 + (x1 - x0) * pos.get_value(), yw, 0], color=WHITE)))
        vr = readout("V across length l =", lambda: k_ * Lcm * pos.get_value(), "V", decimals=2, size=26, color=C_V).move_to([0, -0.4, 0])
        kk = M(r"V = kl,\qquad k = \frac{V_{AB}}{L}\ \ (\text{potential gradient})", size=40).move_to([0, -1.5, 0])
        with self.say("A potentiometer is a long uniform wire, several metres, carrying a steady current from a driver cell. Because the wire is uniform, the potential falls evenly along it. The potential difference across any length l is k l, where k, the potential gradient in volts per metre, stays constant as long as the current is steady."):
            self.play(Create(wire_), Create(drv), FadeIn(drl), FadeIn(lbl))
            self.add(Vmark)
            self.play(FadeIn(vr))
            self.play(pos.animate.set_value(1.0), run_time=3, rate_func=linear)
            self.play(Write(kk))
        self.play(FadeOut(VGroup(vr, kk)), FadeOut(Vmark))
        self.remove(Vmark)
        l = ValueTracker(100.0)
        E = 0.48
        jx = lambda: x0 + (x1 - x0) * l.get_value() / Lcm
        tst = always_redraw(lambda: VGroup(wire([x0, yw, 0], [x0, -1.2, 0], [-3.4, -1.2, 0]), cell([-3.4, -1.2, 0], [-2.6, -1.2, 0], plus_at_b=False), wire([-2.6, -1.2, 0], [-1.0, -1.2, 0]),
                                           galvo([-0.6, -1.2, 0], r=0.3), wire([-0.2, -1.2, 0], [jx(), -1.2, 0], [jx(), yw - 0.1, 0]),
                                           Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.12).move_to([jx(), yw - 0.12, 0])))
        tl = T("cell under test, E", size=22, color=C_R).move_to([-3.0, -1.75, 0])
        dev = lambda: 2.0 * (k_ * l.get_value() - E) / E
        dial, needle = needle_meter([4.4, -1.6, 0], dev, r=0.8)
        ro = readout("l =", lambda: l.get_value(), "cm", decimals=0, size=26, color=C_I).move_to([4.4, -2.7, 0])
        with self.say("Now connect a cell under test, through a galvanometer, to a jockey that touches the wire. Its positive terminal goes to the same end, A, as the driver's. Slide the jockey until the galvanometer reads zero."):
            self.add(tst, needle)
            self.play(FadeIn(tst), FadeIn(tl), FadeIn(dial), FadeIn(needle), FadeIn(ro))
            self.play(l.animate.set_value(350), run_time=2.5)
            self.play(l.animate.set_value(240), run_time=2.0)
        key = para("At balance NO current is drawn from the cell, so there is no internal drop: the potentiometer measures the true e.m.f. It behaves like a voltmeter of infinite resistance.", width=7.4, size=22, color=C_E).move_to([-1.6, -2.65, 0])
        with self.say("At the balance point, no current flows through the cell under test. So there is no I r drop inside it, and the potentiometer measures its true e m f, not the terminal voltage. A voltmeter always draws a little current and reads slightly low. The potentiometer behaves like a voltmeter of infinite resistance."):
            self.play(FadeIn(key))
        self.play(FadeOut(key))
        cmp_ = VGroup(M(r"E_1 = kl_1,\quad E_2 = kl_2\ \Rightarrow\ \frac{E_1}{E_2} = \frac{l_1}{l_2}", size=36, color=C_R)).move_to([-0.8, -2.65, 0])
        with self.say("To compare two cells, balance each in turn, at lengths l one and l two. Since each e m f is k times its length, E one over E two equals l one over l two."):
            self.play(Write(cmp_))
        self.play(FadeOut(cmp_))
        self.internal_r(l, x0, x1, yw, Lcm, jx, tst, tl, dial, needle, ro, k_)

    def internal_r(self, l, x0, x1, yw, Lcm, jx, tst, tl, dial, needle, ro, k_):
        Rk = ValueTracker(0.0)
        Rl = always_redraw(lambda: VGroup(wire([-3.6, -1.2, 0], [-3.6, -2.4, 0], [-3.3, -2.4, 0]), resistor([-3.3, -2.4, 0], [-2.7, -2.4, 0], zig=4),
                                          wire([-2.7, -2.4, 0], [-2.4, -2.4, 0]),
                                          Line([-2.4, -2.4, 0], [-2.4 + 0.5 * np.cos(0.6 * (1 - Rk.get_value())), -2.4 + 0.5 * np.sin(0.6 * (1 - Rk.get_value())), 0], color=th.BODY, stroke_width=4),
                                          wire([-1.9, -2.4, 0], [-1.6, -2.4, 0], [-1.6, -1.2, 0])))
        kl = T("K₂ and R = 5 Ω", size=20, color=th.MUTED).move_to([-2.6, -2.85, 0])
        with self.say("Now the internal resistance, a long question favourite. With key K two open, the cell drives no current, and balances at its full e m f: two hundred and forty centimetres."):
            self.add(Rl)
            self.play(FadeIn(Rl), FadeIn(kl), FadeOut(tl))
        with self.say("Close K two. Now the cell drives a current through the known resistance R. The potentiometer now matches the terminal voltage, which is lower. The balance point falls to two hundred centimetres."):
            self.play(Rk.animate.set_value(1.0), run_time=0.8)
            self.play(l.animate.set_value(200), run_time=2.5)
        self.play(FadeOut(VGroup(dial, ro, kl)), FadeOut(needle), FadeOut(tst), FadeOut(Rl))
        self.remove(tst, Rl, needle)
        self.clear_stage()
        title = T("Internal resistance from two balance lengths", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        L = VGroup(M(r"K_2\ \text{open: } E = kl_1", size=40), M(r"K_2\ \text{closed: } V = kl_2,\quad V = \frac{ER}{R + r}", size=40),
                   M(r"\frac{E}{V} = \frac{l_1}{l_2} = \frac{R + r}{R}\ \Rightarrow\ \frac{l_1}{l_2} - 1 = \frac{r}{R}", size=40),
                   M(r"r = R\left(\frac{l_1 - l_2}{l_2}\right)", size=58, color=C_R)).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.4)
        says = ["Write it down. With K two open, E equals k l one.",
                "With K two closed, the terminal voltage V equals k l two, and V is E R over R plus r.",
                "Divide. E over V is l one over l two, which is R plus r over R. Subtract one from both sides.",
                "And the internal resistance is R times l one minus l two, over l two."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(FadeOut(VGroup(title, L)))
        example(self, "A cell balances at 240 cm on a potentiometer. With 5 Ω across its terminals the balance length falls to 200 cm. Find the internal resistance, and the e.m.f. if the potential gradient is 2.0 mV/cm.",
                [r"r = R\left(\frac{l_1 - l_2}{l_2}\right) = 5\left(\frac{240 - 200}{200}\right) = 5\times 0.2 = 1\ \Omega",
                 r"E = kl_1 = (2.0\times10^{-3}\ \text{V cm}^{-1})(240\ \text{cm}) = 0.48\ \text{V}"],
                ["Now the numbers we just watched. Balance at two forty centimetres, then at two hundred with five ohms across the cell. Find r, and E with a gradient of two millivolts per centimetre.",
                 "r is five times forty over two hundred: five times zero point two, one ohm.",
                 "And E is k l one: two millivolts per centimetre times two hundred and forty centimetres, zero point four eight volts."], size=40)
        example(self, "A cell balances against 150 cm of potentiometer wire. With a 4 Ω resistor across it the balance length becomes 120 cm. Find the internal resistance.",
                [r"r = 4\left(\frac{150 - 120}{120}\right) = 4\times 0.25 = 1\ \Omega"],
                ["Another from the five mark questions. Balance at one fifty centimetres, then one twenty with four ohms across the cell.",
                 "r is four times thirty over one twenty: four times a quarter, one ohm."], size=46)
        cau = self.callout("careful", "No balance point? If the driver e.m.f. E₀ is smaller than the e.m.f. being measured, or the cells' positive terminals are not joined to the same end, the galvanometer deflects the same way everywhere. Always take E₀ > E.", width=11, size=26)
        with self.say("One practical trap. If the galvanometer deflects the same way at both ends of the wire, there is no balance point. Either the driver cell's e m f is too small, smaller than the one you are measuring, or a cell has been connected the wrong way round. Always make E nought bigger than E, and join both positive terminals to the same end."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        self.quiz("A potentiometer measures the e.m.f. of a cell more accurately than a voltmeter because at balance it",
                  ["has a very low resistance", "draws no current from the cell", "uses a longer wire", "is calibrated in volts"], 1,
                  "Pause and think. Why is a potentiometer better than a voltmeter for measuring e m f?",
                  "B, because at balance it draws no current from the cell, so there is no internal drop. A longer wire helps the precision, but the real reason is the null method.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1.1, 0.5], x_length=6.4, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-2.6, 0.0, 0])
        xl = T("temperature T (K)", size=22).next_to(ax.x_axis, DOWN, buff=0.25)
        yl = T("resistivity ρ", size=22).next_to(ax.y_axis, UP, buff=0.1)
        metal = ax.plot(lambda T_: 0.18 + 0.008 * T_ ** 2, x_range=[0, 10], color=th.SKY, stroke_width=4)
        tc = 4.2
        sc = VGroup(ax.plot(lambda T_: 0.3 + 0.006 * T_ ** 2, x_range=[tc, 10], color=th.AMBER, stroke_width=5),
                    Line(ax.c2p(tc, 0.3 + 0.006 * tc ** 2), ax.c2p(tc, 0), color=th.AMBER, stroke_width=5), Line(ax.c2p(0, 0), ax.c2p(tc, 0), color=th.AMBER, stroke_width=7))
        labs = VGroup(T("normal metal: residual resistivity at 0 K", size=22, color=th.SKY).move_to([3.6, -0.4, 0]), T("mercury: exactly zero below Tc = 4.2 K", size=22, color=th.AMBER).move_to([3.6, 0.6, 0]))
        with self.say("Cool a normal metal, and its resistance falls, because the lattice ions vibrate less and scatter the electrons less. But it never reaches zero. Impurities and defects leave a residual resistivity, even at absolute zero."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(metal), FadeIn(labs[0]))
        with self.say("In nineteen eleven, Kamerlingh Onnes cooled mercury with liquid helium, and found something astonishing. At four point two kelvin, its resistance suddenly vanished. Not very small. Zero, as far as any instrument can tell. That sharp temperature is the critical temperature, T c."):
            self.play(Create(sc), FadeIn(labs[1]), run_time=2)
        self.play(FadeOut(VGroup(ax, xl, yl, metal, sc, labs)))
        Tt = ValueTracker(1.0)
        C = np.array([-3.0, -0.2, 0])

        def field():
            g = VGroup()
            sup = Tt.get_value() < 0.5
            for y in np.linspace(-2.2, 2.2, 9):
                if not sup or abs(y) > 1.25:
                    if not sup:
                        g.add(Line([C[0] - 2.6, C[1] + y, 0], [C[0] + 2.6, C[1] + y, 0], color=th.SKY, stroke_width=2.5))
                    else:
                        bulge = 1.25 * np.sign(y) * max(0, 1 - (abs(y) - 1.25) / 1.5) * 0.8
                        g.add(VMobject(stroke_color=th.SKY, stroke_width=2.5).set_points_smoothly([[C[0] - 2.6, C[1] + y, 0], [C[0] - 1.0, C[1] + y + bulge * 0.5, 0], [C[0], C[1] + y + bulge, 0], [C[0] + 1.0, C[1] + y + bulge * 0.5, 0], [C[0] + 2.6, C[1] + y, 0]]))
                else:
                    sgn = 1 if y >= 0 else -1
                    off = 1.3 + abs(y) * 0.35
                    g.add(VMobject(stroke_color=th.SKY, stroke_width=2.5).set_points_smoothly([[C[0] - 2.6, C[1] + y, 0], [C[0] - 1.1, C[1] + y + sgn * 0.3, 0], [C[0], C[1] + sgn * off, 0], [C[0] + 1.1, C[1] + y + sgn * 0.3, 0], [C[0] + 2.6, C[1] + y, 0]]))
            return g
        fl = always_redraw(field)
        ball = always_redraw(lambda: Circle(radius=1.0, stroke_color=WHITE, stroke_width=3, fill_color=th.AMBER if Tt.get_value() < 0.5 else th.MUTED, fill_opacity=0.35).move_to(C))
        st = always_redraw(lambda: T("T < Tc: superconducting" if Tt.get_value() < 0.5 else "T > Tc: normal", size=24, color=th.AMBER if Tt.get_value() < 0.5 else th.MUTED).next_to(C + DOWN * 2.4, DOWN, buff=0.1))
        mt = VGroup(T("Meissner effect", size=30, color=th.AMBER, weight="BOLD"), para("Below Tc a superconductor pushes the magnetic field out: B = 0 inside.", width=5.2, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 1.4, 0])
        with self.say("Zero resistance is only half the story. In nineteen thirty three, Meissner found that a superconductor also expels magnetic field. Above T c, field lines pass straight through the material. Cool it below T c, and the field is pushed out completely. B is zero inside. That is the Meissner effect."):
            self.add(fl, ball, st)
            self.play(FadeIn(fl), FadeIn(ball), FadeIn(st))
            self.wait(1)
            self.play(Tt.animate.set_value(0.0), run_time=0.5)
            self.play(FadeIn(mt))
            self.wait(1.5)
        d = para("A superconductor: zero resistivity below Tc AND expulsion of magnetic flux, B = 0 inside.", width=5.2, size=24, color=C_E).next_to(mt, DOWN, buff=0.5)
        with self.say("So a superconductor is a material whose resistivity becomes exactly zero below a critical temperature, and which also expels magnetic flux from its interior."):
            self.play(FadeIn(d))
        self.play(FadeOut(VGroup(mt, d)), FadeOut(fl), FadeOut(ball), FadeOut(st))
        self.remove(fl, ball, st)
        title = T("Perfect conductor vs superconductor", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        rows = [("", "Perfect conductor", "Superconductor"), ("resistivity", "zero", "zero"), ("defined by", "ρ = 0 only", "ρ = 0 AND B = 0 inside"),
                ("cooled in a field", "TRAPS the flux inside", "EXPELS the flux"), ("final state", "depends on history", "always the same: a true phase"), ("exists?", "no, an idealisation", "yes, below Tc")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=24 if i else 26, color=(th.BG if not c else ([th.MUTED, th.SKY, th.AMBER][j] if i == 0 or j == 0 else th.BODY)), weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.6, -0.9, 3.4]):
                row[j].move_to([x, 2.0 - i * 0.72, 0])
            grid.add(row)
        with self.say("Examiners like this distinction. A perfect conductor is an imaginary material with zero resistance and nothing else. Cool it in a magnetic field, and it traps whatever flux was inside, so its final state depends on its history. A real superconductor expels the flux whichever order you do things in. Its state is always the same: a true thermodynamic phase.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(title, grid)))
        title = T("Limits and uses", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        pts = VGroup(para("• Too strong a magnetic field (the critical field) or too large a current destroys superconductivity.", width=11, size=26, color=th.BODY),
                     para("• 1986–87: ceramic oxides like YBa₂Cu₃O₇ superconduct up to about 92 K, above liquid nitrogen's cheap 77 K.", width=11, size=26, color=th.BODY),
                     para("• Uses: MRI magnets, accelerator magnets, maglev trains, SQUID magnetometers, loss-free cables.", width=11, size=26, color=th.AMBER),
                     VGroup()).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)
        with self.say("Superconductivity has limits: too strong a magnetic field, the critical field, or too large a current, destroys it. In nineteen eighty six and seven, ceramic oxides were found that superconduct up to about ninety two kelvin, warmer than liquid nitrogen at seventy seven kelvin, which is cheap. Today superconductors power M R I scanners in hospitals, particle accelerator magnets, maglev trains, ultra sensitive SQUID magnetometers, and loss free power cables.") as v_:
            self.play(FadeIn(title))
            for p in pts:
                self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v_.dur / 4 - 0.7)
        self.play(FadeOut(VGroup(title, pts)))
        self.quiz("Below its critical temperature a superconductor",
                  ["has infinite resistance", "becomes an insulator", "expels magnetic flux", "traps all the flux inside"], 2,
                  "Pause and think. Below its critical temperature, what does a superconductor do?",
                  "C, it expels magnetic flux: the Meissner effect. Trapping the flux is what a merely perfect conductor would do. That difference is exactly what the examiners test.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        self._gt = ValueTracker(0)
        dial, needle = needle_meter([-3.4, 0.4, 0], lambda: -1 + 2 * (0.5 + 0.5 * np.sin(self._gt.get_value())), r=1.6, label="G")
        info = VGroup(T("Moving-coil galvanometer", size=28, color=th.INK, weight="BOLD"), M(r"\text{resistance } G,\ \ \text{full scale at a small } I_g", size=34),
                      T("(a few milliamperes)", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.8, 1.0, 0])
        with self.say("Inside every analogue meter is a moving coil galvanometer. It has a resistance G, and gives a full scale deflection for a small current, I g, a few milliamperes. Only the resistor bolted onto it decides what kind of meter it becomes."):
            self.add(needle)
            self.play(FadeIn(dial), FadeIn(needle), FadeIn(info))
            self.play(self._gt.animate.set_value(2 * PI), run_time=3)
        self.play(FadeOut(VGroup(dial, info)), FadeOut(needle))
        self.remove(needle)
        a, b = np.array([-5.6, 0.4, 0]), np.array([0.4, 0.4, 0])
        top = VGroup(wire(a, [-4.4, 0.4, 0], [-4.4, 1.4, 0], [-3.0, 1.4, 0]), galvo([-2.6, 1.4, 0]), wire([-2.2, 1.4, 0], [-0.8, 1.4, 0], [-0.8, 0.4, 0], b))
        bot = VGroup(wire([-4.4, 0.4, 0], [-4.4, -0.6, 0], [-3.4, -0.6, 0]), resistor([-3.4, -0.6, 0], [-1.8, -0.6, 0], zig=5, color=C_V), wire([-1.8, -0.6, 0], [-0.8, -0.6, 0], [-0.8, 0.4, 0]))
        st = VGroup(Stream([a, [-4.4, 0.4, 0]], n=4, speed=1.2, color=C_I), Stream([[-4.4, 0.4, 0], [-4.4, 1.4, 0], [-0.8, 1.4, 0], [-0.8, 0.4, 0]], n=3, speed=0.4, color=th.CORAL),
                    Stream([[-4.4, 0.4, 0], [-4.4, -0.6, 0], [-0.8, -0.6, 0], [-0.8, 0.4, 0]], n=10, speed=1.2, color=C_I), Stream([[-0.8, 0.4, 0], b], n=4, speed=1.2, color=C_I))
        labs = VGroup(M("I", size=30, color=C_I).next_to(a, UP, buff=0.1), M("I_g", size=30, color=th.CORAL).next_to([-2.6, 1.8, 0], UP, buff=0.05),
                      M(r"I - I_g", size=28, color=C_I).next_to([-2.6, -0.6, 0], DOWN, buff=0.3), M("S", size=30, color=C_V).next_to([-2.6, -0.6, 0], UP, buff=0.25))
        L = VGroup(T("Ammeter: small shunt S in parallel", size=26, color=C_V, weight="BOLD"), M(r"I_gG = (I - I_g)S", size=36), M(r"S = \frac{I_gG}{I - I_g}", size=48, color=C_V),
                   M(r"R_A = \frac{GS}{G + S}\ \text{(very small; in series)}", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.4, 0])
        with self.say("To make an ammeter that reads up to a big current I, connect a small resistance, the shunt S, in parallel with the galvanometer. Only I g goes through the coil, and the rest, I minus I g, bypasses it through the shunt."):
            self.play(Create(top), Create(bot))
            self.add(st)
            self.play(FadeIn(labs))
            self.play(FadeIn(L[0]))
        with self.say("The two are in parallel, so they have the same voltage: I g G equals I minus I g, times S. So S equals I g G over I minus I g. The finished ammeter has a very small resistance, G S over G plus S, because it goes in series, and must not disturb the current. An ideal ammeter has zero resistance."):
            self.play(Write(L[1]))
            self.play(Write(L[2]))
            self.play(Write(L[3]))
        self.play(FadeOut(VGroup(top, bot, labs, L)), FadeOut(st))
        self.remove(st)
        ckt = VGroup(wire([-5.6, 0.4, 0], [-4.4, 0.4, 0]), galvo([-4.0, 0.4, 0]), wire([-3.6, 0.4, 0], [-3.0, 0.4, 0]), resistor([-3.0, 0.4, 0], [-0.6, 0.4, 0], zig=8, color=C_R),
                     wire([-0.6, 0.4, 0], [0.4, 0.4, 0]))
        st = Stream([[-5.6, 0.4, 0], [0.4, 0.4, 0]], n=8, speed=0.4, color=th.CORAL)
        br = BraceBetweenPoints([-5.6, -0.1, 0], [0.4, -0.1, 0], DOWN, color=th.MUTED)
        bl = M("V", size=32).next_to(br, DOWN, buff=0.1)
        rl = M("R", size=30, color=C_R).next_to([-1.8, 0.4, 0], UP, buff=0.35)
        L = VGroup(T("Voltmeter: large multiplier R in series", size=26, color=C_R, weight="BOLD"), M(r"V = I_g(G + R)", size=36), M(r"R = \frac{V}{I_g} - G", size=48, color=C_R),
                   M(r"R_V = G + R\ \text{(very large; in parallel)}", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.1, 0.4, 0])
        with self.say("To make a voltmeter that reads up to V, connect a large resistance R, the multiplier, in series. Choose it so that exactly I g flows when the full voltage V is across the meter: V equals I g times G plus R. So R equals V over I g, minus G."):
            self.play(Create(ckt), FadeIn(rl))
            self.add(st)
            self.play(GrowFromCenter(br), FadeIn(bl), FadeIn(L[0]))
            self.play(Write(L[1]))
            self.play(Write(L[2]))
        with self.say("The finished voltmeter has a very large resistance, G plus R. It goes in parallel across the thing being measured, and must draw as little current as possible. An ideal voltmeter has infinite resistance."):
            self.play(Write(L[3]))
        self.play(FadeOut(VGroup(ckt, br, bl, rl, L)), FadeOut(st))
        self.remove(st)
        self.ohmmeter()
        example(self, "A galvanometer of resistance 50 Ω gives full-scale deflection for 2 mA. Convert it into (a) an ammeter reading 0–5 A and (b) a voltmeter reading 0–10 V. Find the resistance of each instrument.",
                [r"S = \frac{I_gG}{I - I_g} = \frac{(2\times10^{-3})(50)}{5 - 0.002} = \frac{0.100}{4.998} = 0.0200\ \Omega\ (\text{parallel})",
                 r"R_A = \frac{GS}{G + S} = \frac{50\times 0.0200}{50.02} = 0.0200\ \Omega",
                 r"R = \frac{V}{I_g} - G = \frac{10}{2\times10^{-3}} - 50 = 4950\ \Omega\ (\text{series})",
                 r"R_V = G + R = 5000\ \Omega\quad (500\ \Omega\ \text{per volt})"],
                ["Worked example. A galvanometer of fifty ohms gives full scale for two milliamps. Make an ammeter reading up to five amps, and a voltmeter reading up to ten volts.",
                 "Shunt: I g G over I minus I g. Two milliamps times fifty, zero point one, over four point nine nine eight: about zero point zero two ohms, in parallel.",
                 "The ammeter's resistance is G S over G plus S: still about zero point zero two ohms. Tiny, as it should be.",
                 "Multiplier: ten volts over two milliamps is five thousand, minus fifty: four thousand nine hundred and fifty ohms, in series.",
                 "The voltmeter's resistance is five thousand ohms, five hundred ohms per volt."], size=34)
        example(self, "A galvanometer of resistance 100 Ω gives full-scale deflection for 1 mA. Find the resistance needed to make (a) an ammeter reading up to 1 A, (b) a voltmeter reading up to 5 V.",
                [r"S = \frac{(10^{-3})(100)}{1 - 0.001} = \frac{0.1}{0.999} = 0.100\ \Omega\ \text{in parallel}",
                 r"R = \frac{5}{10^{-3}} - 100 = 4900\ \Omega\ \text{in series}"],
                ["One more conversion. One hundred ohms, full scale at one milliamp.",
                 "For one amp: zero point one over zero point nine nine nine, about zero point one ohms, in parallel.",
                 "For five volts: five thousand minus one hundred, four thousand nine hundred ohms, in series."], size=40)
        self.quiz("To convert a galvanometer into an ammeter, we connect a",
                  ["high resistance in series", "high resistance in parallel", "low resistance in series", "low resistance in parallel"], 3,
                  "Pause and think. To make an ammeter from a galvanometer, what do we connect, and how?",
                  "D, a low resistance in parallel: the shunt. A high resistance in series makes a voltmeter instead, the most common mix up.")

    def ohmmeter(self):
        C = np.array([-2.8, -0.6, 0])
        r = 2.4
        title = T("The ohmmeter", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        arc = Arc(radius=r, start_angle=PI / 2 - 1.0, angle=2.0, arc_center=C, color=th.BODY, stroke_width=3)
        GR = 1.0
        marks = VGroup()
        for X, lab in [(0, "0"), (0.25, "¼"), (0.5, "½"), (1, "1"), (2, "2"), (4, "4"), (10, "10"), (1e9, "∞")]:
            f = GR / (GR + X)
            a = PI / 2 + 1.0 - 2.0 * f
            p = C + r * np.array([np.cos(a), np.sin(a), 0])
            marks.add(Line(p, p + 0.2 * (p - C) / r, color=th.BODY, stroke_width=2), T(lab, size=20, color=th.AMBER).move_to(C + (r + 0.45) * np.array([np.cos(a), np.sin(a), 0])))
        Xv = ValueTracker(0.0)
        needle = always_redraw(lambda: Line(C, C + (r - 0.1) * np.array([np.cos(PI / 2 + 1.0 - 2.0 * GR / (GR + Xv.get_value())), np.sin(PI / 2 + 1.0 - 2.0 * GR / (GR + Xv.get_value())), 0]), color=th.CORAL, stroke_width=4))
        cap = T("unknown X, in units of (G + R)", size=20, color=th.MUTED).next_to(C, DOWN, buff=0.2)
        L = VGroup(M(r"\text{leads shorted: } I_g = \frac{E}{G + R}", size=34), M(r"\text{with } X:\ I = \frac{E}{G + R + X}", size=34),
                   T("scale is REVERSED: 0 Ω at full scale (right)", size=22, color=th.AMBER), T("and NON-UNIFORM: cramped at large X", size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        with self.say("An ohmmeter is a galvanometer, a cell and an adjustable resistor in series, with two test leads. Touch the leads together, and adjust R so the needle sits exactly at full scale. That is zero ohms."):
            self.play(FadeIn(title), Create(arc), FadeIn(marks), FadeIn(cap))
            self.add(needle)
            self.play(FadeIn(needle), Write(L[0]))
        with self.say("Now put an unknown resistance X between the leads. The current falls to E over G plus R plus X. Watch the needle as X grows: it moves left, slowly at first and then crowding up. So the scale is reversed, with zero on the right and infinity on the left, and it is non uniform, cramped at large X."):
            self.play(Write(L[1]))
            self.play(Xv.animate.set_value(10), run_time=4, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(L[2]), FadeIn(L[3]))
        self.play(FadeOut(VGroup(title, arc, marks, cap, L)), FadeOut(needle))
        self.remove(needle)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        t = clock(self, 1.0)
        rng = np.random.default_rng(4)
        box = Rectangle(width=8.0, height=2.0, stroke_color=th.BODY, stroke_width=3).move_to([0, 1.0, 0])
        ions = VGroup(*[Dot([x, y, 0], radius=0.09, color=th.MUTED) for x in np.linspace(-3.6, 3.6, 13) for y in (0.4, 1.0, 1.6)])
        base = [d.get_center().copy() for d in ions]
        heat = ValueTracker(0.0)

        def jig(m):
            for d, b in zip(m, base):
                a = 0.03 + 0.12 * heat.get_value()
                d.move_to(b + a * np.array([np.sin(17 * t.get_value() + b[0] * 3), np.cos(13 * t.get_value() + b[1] * 5), 0]))
                d.set_color(interpolate_color(ManimColor(th.MUTED), ManimColor(th.CORAL), heat.get_value()))
        ions.add_updater(jig)
        el = Stream([[-4.0, 0.7, 0], [4.0, 0.7, 0]], n=12, speed=0.9, color=th.SKY, radius=0.05)
        el2 = Stream([[-4.0, 1.3, 0], [4.0, 1.3, 0]], n=12, speed=0.9, color=th.SKY, radius=0.05)
        with self.say("Why does a current heat a wire? The electric field speeds the electrons up, but they keep crashing into the vibrating ions of the lattice, handing over the energy they gained. The ions jiggle harder, and that is heat. The drift speed stays steady, so all the electrical energy turns into heat."):
            self.add(ions, el, el2)
            self.play(Create(box), FadeIn(ions), FadeIn(el), FadeIn(el2))
            self.play(heat.animate.set_value(1.0), run_time=4)
        L = VGroup(M(r"W = qV = VIt", size=40), M(r"H = I^{2}Rt = VIt = \frac{V^{2}}{R}t", size=48, color=th.CORAL), M(r"P = I^{2}R = \frac{V^{2}}{R}", size=40)).arrange(DOWN, buff=0.3).move_to([0, -1.6, 0])
        with self.say("In time t, a charge I t moves through a potential difference V. The work done on it is V I t, and all of it becomes heat. Using V equals I R, the heat is I squared R t, or V squared t over R. And the rate of heating, the power, is I squared R, or V squared over R. This is Joule's law."):
            self.play(Write(L[0]))
            self.play(Write(L[1]))
            self.play(Write(L[2]))
        self.play(FadeOut(VGroup(box, L)), FadeOut(ions), FadeOut(el), FadeOut(el2))
        ions.clear_updaters()
        self.remove(ions, el, el2, t)
        laws = VGroup(T("Joule's laws, hidden in H = I²Rt:", size=28, color=th.INK, weight="BOLD"), M(r"H \propto I^{2}\ (R, t\ \text{fixed})", size=36), M(r"H \propto R\ (I, t\ \text{fixed})", size=36),
                      M(r"H \propto t\ (I, R\ \text{fixed})", size=36), M(r"\text{in calories: } H = \frac{I^{2}Rt}{J},\ J = 4.2\ \text{J cal}^{-1}", size=32, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.4, 0])
        with self.say("The three statements called Joule's laws are just the three proportionalities in I squared R t. Heat goes as the current squared, as the resistance, and as the time. To get calories, divide by J, four point two joules per calorie."):
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in laws], lag_ratio=0.3), run_time=3)
        self.play(FadeOut(laws))
        self.series_parallel()
        example(self, "A kettle marked 1500 W, 230 V heats 1.0 kg of water from 20 °C to 100 °C. If 80 % of the energy reaches the water, how long does it take? Find the resistance of the element (c = 4200 J/kg/K).",
                [r"Q = mc\,\Delta\theta = (1.0)(4200)(100 - 20) = 3.36\times10^{5}\ \text{J}",
                 r"P_{\text{useful}} = 0.80\times 1500 = 1200\ \text{W}\ \Rightarrow\ t = \frac{3.36\times10^{5}}{1200} = 280\ \text{s} = 4\ \text{min}\ 40\ \text{s}",
                 r"R = \frac{V^{2}}{P} = \frac{230^{2}}{1500} = \frac{52900}{1500} = 35.3\ \Omega"],
                ["Worked example. A kettle marked fifteen hundred watts, two hundred and thirty volts, heats one kilogram of water from twenty to one hundred degrees. Eighty percent of the energy reaches the water. How long does it take, and what is the element's resistance?",
                 "The water needs m c delta theta: one times forty two hundred times eighty, three point three six times ten to the five joules.",
                 "Useful power is eighty percent of fifteen hundred, twelve hundred watts. So the time is three point three six times ten to the five over twelve hundred: two hundred and eighty seconds, four minutes forty.",
                 "And the element's resistance is V squared over P: fifty two thousand nine hundred over fifteen hundred, about thirty five point three ohms."], size=34)
        uses = VGroup(T("Heaters, irons, kettles: nichrome, high resistivity, high melting point", size=24, color=th.BODY),
                      T("Fuse: low-melting tin–lead wire that melts when I²R heating gets dangerous", size=24, color=th.BODY),
                      M(r"1\ \text{kWh} = 1000\times 3600 = 3.6\times10^{6}\ \text{J}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        with self.say("Joule heating is used everywhere. Heaters, irons and kettles use nichrome, an alloy with high resistivity and a high melting point. A fuse does the opposite job: a short tin lead wire that melts and breaks the circuit when the heating gets dangerous. And the Nepal Electricity Authority bills you in kilowatt hours: one kilowatt hour is three point six million joules."):
            self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.2) for u in uses], lag_ratio=0.4), run_time=3)
        self.play(FadeOut(uses))
        self.quiz("2 Ω and 4 Ω resistors are joined in parallel across a battery. The ratio of the heat produced in them in a given time is",
                  ["1 : 2", "2 : 1", "1 : 4", "4 : 1"], 1,
                  "Last check. Two ohms and four ohms in parallel across a battery. What is the ratio of the heat produced in them?",
                  "B, two to one. In parallel the voltage is common, so H goes as one over R, and the two ohm resistor makes twice the heat. If you used I squared R, you would get one to two, exactly backwards.")

    def series_parallel(self):
        title = T("Which resistor gets hotter?", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        s = VGroup(wire([-6.0, 0.8, 0], [-5.4, 0.8, 0]), resistor([-5.4, 0.8, 0], [-4.0, 0.8, 0], zig=4, color=th.CORAL), wire([-4.0, 0.8, 0], [-3.4, 0.8, 0]),
                   resistor([-3.4, 0.8, 0], [-1.4, 0.8, 0], zig=6, color=th.CORAL, stroke=7), wire([-1.4, 0.8, 0], [-0.8, 0.8, 0]))
        sl = VGroup(T("series: same I", size=24, color=C_I, weight="BOLD").move_to([-3.4, 1.8, 0]), M(r"H = I^{2}Rt", size=34).move_to([-3.4, -0.2, 0]),
                    T("BIGGER R gets hotter", size=24, color=th.CORAL).move_to([-3.4, -0.9, 0]), T("2 Ω", size=20).move_to([-4.7, 0.3, 0]), T("4 Ω", size=20).move_to([-2.4, 0.3, 0]))
        p = VGroup(wire([1.0, 0.8, 0], [1.6, 0.8, 0], [1.6, 1.5, 0], [2.4, 1.5, 0]), resistor([2.4, 1.5, 0], [4.4, 1.5, 0], zig=6, color=th.CORAL, stroke=7), wire([4.4, 1.5, 0], [5.2, 1.5, 0], [5.2, 0.8, 0], [5.8, 0.8, 0]),
                   wire([1.6, 0.8, 0], [1.6, 0.1, 0], [2.4, 0.1, 0]), resistor([2.4, 0.1, 0], [4.4, 0.1, 0], zig=6, color=th.CORAL, stroke=3), wire([4.4, 0.1, 0], [5.2, 0.1, 0], [5.2, 0.8, 0]))
        pl = VGroup(T("parallel: same V", size=24, color=C_V, weight="BOLD").move_to([3.4, 2.3, 0]), M(r"H = \frac{V^{2}}{R}t", size=34).move_to([3.4, -0.8, 0]),
                    T("SMALLER R gets hotter", size=24, color=th.CORAL).move_to([3.4, -1.6, 0]), T("2 Ω", size=20).move_to([3.4, 1.95, 0]), T("4 Ω", size=20).move_to([3.4, -0.35, 0]))
        glow1 = VGroup(Circle(radius=0.55, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.35).move_to([-2.4, 0.8, 0]))
        glow2 = VGroup(Circle(radius=0.55, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.35).move_to([3.4, 1.5, 0]))
        with self.say("A favourite trap. Which resistor gets hotter, two ohms or four ohms? In series, the current is the same in both, so use I squared R t: the bigger resistance gets hotter."):
            self.play(FadeIn(title), Create(s), FadeIn(sl[0]), FadeIn(sl[3:]))
            self.play(Write(sl[1]), FadeIn(sl[2]), FadeIn(glow1))
        with self.say("In parallel, the voltage is the same across both, so use V squared t over R: now the smaller resistance gets hotter. Pick the wrong formula, and you reverse the answer."):
            self.play(Create(p), FadeIn(pl[0]), FadeIn(pl[3:]))
            self.play(Write(pl[1]), FadeIn(pl[2]), FadeIn(glow2))
        self.play(FadeOut(VGroup(title, s, sl, p, pl, glow1, glow2)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"\text{junction: } \sum I = 0\ (\text{charge});\quad \text{loop: } \sum E = \sum IR\ (\text{energy})", size=34),
            M(r"\text{Wheatstone: } \frac{P}{Q} = \frac{R}{S};\quad \text{metre bridge: } X = R\frac{l}{100 - l}", size=34),
            M(r"\text{potentiometer: } V = kl,\ \frac{E_1}{E_2} = \frac{l_1}{l_2},\ r = R\frac{l_1 - l_2}{l_2}", size=34),
            "Superconductor: ρ = 0 below Tc AND flux expelled (Meissner); a perfect conductor would trap it.",
            M(r"\text{ammeter: } S = \frac{I_gG}{I - I_g}\ \parallel;\quad \text{voltmeter: } R = \frac{V}{I_g} - G\ \text{in series}", size=32),
            M(r"H = I^{2}Rt = VIt = \frac{V^{2}}{R}t;\quad 1\ \text{kWh} = 3.6\times10^{6}\ \text{J}", size=34),
        ], "Let us recap. Kirchhoff's junction law conserves charge, and his loop law conserves energy. A balanced Wheatstone bridge gives P over Q equals R over S, and the metre bridge gives X equals R l over one hundred minus l. A potentiometer draws no current at balance, so it compares e m fs and finds internal resistance exactly. A superconductor has zero resistance and expels magnetic flux. A shunt in parallel makes an ammeter, a multiplier in series makes a voltmeter. And Joule's law says the heat is I squared R t.")
        self.outro("That is electrical circuits. Next, we find that heat and electricity are linked in surprising ways: a junction of two metals that makes a voltage when heated, in Thermoelectric Effects. See you there, on NEBians.")
