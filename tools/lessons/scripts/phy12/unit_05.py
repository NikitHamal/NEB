import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import (Cylinder, Gas, Stream, example, flame, heat_color, neby_in, neby_out, nothing, pv_axes,  # noqa: E402
                   readout)

C_Q1, C_Q2, C_W, C_S = th.CORAL, th.SKY, th.MINT, th.AMBER


def xmark(center, size=0.5, color=th.CORAL):
    return VGroup(Line(UL, DR), Line(DL, UR)).set_stroke(color, 10).scale(size).move_to(center)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 5
    TITLE = "Second Law of Thermodynamics"
    SUBTITLE = "Engines, refrigerators and the arrow of time"
    SECTIONS = ["Direction of processes", "The second law", "Heat engines", "Otto, Diesel and Carnot cycles",
                "Refrigerators", "Entropy and disorder"]
    NEXT = "Unit 6 · Wave Motion"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ helpers
    def flow(self, cx=0.0, fridge=False, q1=1.0, q2=0.6, hot="source", cold="sink", mid=None, scale=1.0):
        yh, yc = 2.1, -2.35
        hotb = RoundedRectangle(corner_radius=0.15, width=3.6, height=0.85, stroke_color=C_Q1, stroke_width=3, fill_color=C_Q1, fill_opacity=0.25).move_to([cx, yh, 0])
        coldb = RoundedRectangle(corner_radius=0.15, width=3.6, height=0.85, stroke_color=C_Q2, stroke_width=3, fill_color=C_Q2, fill_opacity=0.25).move_to([cx, yc, 0])
        hl = VGroup(T(hot, size=24, color=th.INK), M("T_1", size=32, color=C_Q1)).arrange(RIGHT, buff=0.25).move_to(hotb)
        cl = VGroup(T(cold, size=24, color=th.INK), M("T_2", size=32, color=C_Q2)).arrange(RIGHT, buff=0.25).move_to(coldb)
        eng = Circle(radius=0.72, stroke_color=th.INK, stroke_width=4, fill_color=th.PANEL, fill_opacity=1).move_to([cx, -0.1, 0])
        el = T(mid or ("fridge" if fridge else "engine"), size=22, color=th.INK).move_to(eng)
        top, bot = eng.get_top(), eng.get_bottom()
        a1 = [hotb.get_bottom(), top] if not fridge else [top, hotb.get_bottom()]
        a2 = [bot, coldb.get_top()] if not fridge else [coldb.get_top(), bot]
        a3 = [eng.get_right(), eng.get_right() + RIGHT * 2.1] if not fridge else [eng.get_right() + RIGHT * 2.1, eng.get_right()]
        sw = lambda q: 4 + 10 * q
        A1 = Arrow(*a1, buff=0.05, color=C_Q1, stroke_width=sw(q1), max_tip_length_to_length_ratio=0.3)
        A2 = Arrow(*a2, buff=0.05, color=C_Q2, stroke_width=sw(q2), max_tip_length_to_length_ratio=0.3)
        A3 = Arrow(*a3, buff=0.05, color=C_W, stroke_width=sw(abs(q1 - q2)), max_tip_length_to_length_ratio=0.3)
        L1 = M("Q_1", size=36, color=C_Q1).next_to(A1, LEFT, buff=0.2)
        L2 = M("Q_2", size=36, color=C_Q2).next_to(A2, LEFT, buff=0.2)
        L3 = M("W", size=36, color=C_W).next_to(A3, UP, buff=0.12)
        S = VGroup(Stream(a1, n=5, color=C_Q1, speed=1.0), Stream(a2, n=5, color=C_Q2, speed=1.0), Stream(a3, n=5, color=C_W, speed=1.0))
        g = VGroup(hotb, coldb, hl, cl, eng, el)
        out = VGroup(g, VGroup(A1, A2, A3), VGroup(L1, L2, L3))
        return out, S

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        floor_y = -2.2
        self._fh = 0.0
        floor = always_redraw(lambda: Rectangle(width=11, height=0.35, stroke_width=0, fill_color=heat_color(self._fh), fill_opacity=0.9).move_to([0, floor_y - 0.18, 0]))
        hs = [4.4 * 0.62 ** k for k in range(7)]
        tt = ValueTracker(0)
        g = 4.0
        segs = []
        t0 = np.sqrt(2 * hs[0] / g)
        segs.append(("fall", 0, t0, hs[0]))
        t = t0
        for h in hs[1:]:
            T_ = 2 * np.sqrt(2 * h / g)
            segs.append(("hop", t, t + T_, h))
            t += T_
        total = t

        def y_at(x):
            for kind, a, b, h in segs:
                if a <= x <= b:
                    if kind == "fall":
                        return hs[0] - 0.5 * g * (x - a) ** 2
                    tau = x - a
                    v0 = np.sqrt(2 * g * h)
                    return v0 * tau - 0.5 * g * tau ** 2
            return 0
        x_of = lambda x: -4.5 + 8.5 * x / total
        ball = always_redraw(lambda: Circle(radius=0.3, fill_color=th.AMBER, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
                             .move_to([x_of(tt.get_value()), floor_y + 0.3 + max(0, y_at(tt.get_value())), 0]))
        self.add(floor)
        with self.say("Watch a ball dropped onto a floor. Each bounce is a little lower than the one before, until the ball comes to rest."):
            self.add(ball)
            self.play(FadeIn(ball), FadeIn(floor))
            self.play(tt.animate.set_value(total), run_time=6, rate_func=linear)
        with self.say("Where did its energy go? Into the floor, as heat. The floor is now very slightly warmer. Energy was conserved all along."):
            self.play(UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self, "_fh", 0.6 * a)), run_time=1.5)
        rew = VGroup(Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).rotate(PI / 2).scale(0.18),
                     Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).rotate(PI / 2).scale(0.18)).arrange(RIGHT, buff=0).to_corner(UR, buff=0.6)
        rl = T("rewind", size=24, color=th.INK).next_to(rew, LEFT, buff=0.2)
        with self.say("Now run the film backwards. The warm floor cools down a little, and uses that heat to launch the ball, higher and higher, back into your hand."):
            self.play(FadeIn(rew), FadeIn(rl))
            self.play(tt.animate.set_value(0), UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(self, "_fh", 0.6 * (1 - a))), run_time=6, rate_func=linear)
        nb = neby_in(self, "laugh", corner=DL)
        q = T("Energy is conserved both ways. So why never backwards?", size=30, color=th.AMBER, weight="SEMIBOLD").to_edge(DOWN, buff=0.35)
        with self.say("You have never seen that happen, and you never will. But here is the puzzle: the backwards film conserves energy perfectly. The first law has no objection at all. So what forbids it? That is the second law of thermodynamics."):
            self.play(FadeIn(q, shift=DOWN * 0.2))
        self.play(FadeOut(VGroup(q, rew, rl)), FadeOut(ball), FadeOut(floor))
        self.remove(ball, floor)
        neby_out(self, nb)
        g_, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 5: the Second Law of Thermodynamics. The first law tells us energy is conserved. The second law tells us which way things go. From it come the limits on every engine and every refrigerator ever built."):
            pass
        self.end_title(g_, nb)
        self.roadmap("Here is our path. The direction of natural processes, the two statements of the second law, heat engines and their efficiency, the Otto, Diesel and Carnot cycles, refrigerators, and finally a first look at entropy.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        title = T("Nature runs one way", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        hotT, coldT = ValueTracker(90), ValueTracker(10)
        bh = Square(1.6, fill_color=C_Q1, fill_opacity=0.8, stroke_width=0).move_to([-4.6, 0.3, 0])
        bc = Square(1.6, fill_color=C_Q2, fill_opacity=0.8, stroke_width=0).next_to(bh, RIGHT, buff=0.04)
        bh.add_updater(lambda m: m.set_fill(heat_color((hotT.get_value() - 10) / 80)))
        bc.add_updater(lambda m: m.set_fill(heat_color((coldT.get_value() - 10) / 80)))
        rh = readout("T =", lambda: hotT.get_value(), "°C", size=24).next_to(bh, DOWN, buff=0.2)
        rc = readout("T =", lambda: coldT.get_value(), "°C", size=24).next_to(bc, DOWN, buff=0.2)
        hs = Stream([bh.get_center(), bc.get_center()], n=4, color=th.AMBER, speed=0.8)
        with self.say("Look around you, and every natural process runs in one direction only. Put hot tea against a cold cup, and heat flows from hot to cold, until they reach the same temperature. Never the other way."):
            self.play(FadeIn(title), FadeIn(bh), FadeIn(bc), FadeIn(rh), FadeIn(rc))
            self.add(hs)
            self.play(hotT.animate.set_value(50), coldT.animate.set_value(50), run_time=4)
            self.play(FadeOut(hs))
            self.remove(hs)
        box = Rectangle(width=4.2, height=2.4, stroke_color=th.BODY, stroke_width=4).move_to([1.8, 0.3, 0])
        wall = ValueTracker(box.get_left()[0] + 1.0)
        gas = Gas(lambda: (box.get_left()[0] + 0.05, wall.get_value(), box.get_bottom()[1] + 0.05, box.get_top()[1] - 0.05), n=30, seed=4)
        part = always_redraw(lambda: Line([wall.get_value(), box.get_bottom()[1], 0], [wall.get_value(), box.get_top()[1], 0], color=th.AMBER, stroke_width=4))
        with self.say("Let a gas out of a cylinder, and it spreads to fill the whole room. It never gathers itself back into the cylinder."):
            self.play(Create(box))
            self.add(gas, part)
            self.play(FadeIn(gas), FadeIn(part))
            self.play(FadeOut(part), run_time=0.3)
            self.remove(part)
            wall.set_value(box.get_right()[0] - 0.05)
            self.wait(2.5)
        note = para("Each reverse process would conserve energy. The first law allows it. Something else forbids it.", width=8.5, size=28, color=th.AMBER).to_edge(DOWN, buff=0.7)
        with self.say("And the bouncing ball never reverses. Every one of these backwards processes would conserve energy perfectly. Something other than the first law decides the direction."):
            self.play(FadeIn(note, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, bh, bc, rh, rc, box, note)), FadeOut(gas))
        bh.clear_updaters()
        bc.clear_updaters()
        self.remove(gas)
        self.reversible()

    def reversible(self):
        d = self.callout("key", "A reversible process can be made to retrace its path exactly, so that the system AND its surroundings both return to their initial states, leaving no trace anywhere. Anything else is irreversible.", width=11)
        d.to_edge(UP, buff=0.8)
        with self.say("This leads to an important idea. A reversible process is one that can be made to retrace its path exactly, so that both the system and its surroundings return to where they started, leaving no trace anywhere. Any process that cannot do that is irreversible."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        x = ValueTracker(0)
        blk = always_redraw(lambda: Rectangle(width=1.0, height=0.6, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).move_to([-4.6 + x.get_value(), -1.0, 0]))
        surf = Line([-5.4, -1.32, 0], [-0.6, -1.32, 0], color=th.BODY, stroke_width=4)
        sparks = always_redraw(lambda: VGroup(*[Dot([-4.6 + x.get_value() + dx, -1.32, 0], radius=0.04, color=th.CORAL) for dx in (-0.4, -0.1, 0.25)]).set_opacity(0.4 + 0.6 * abs(np.sin(8 * x.get_value()))))
        lab = T("friction: heat spreads into the floor", size=22, color=th.CORAL).next_to(surf, DOWN, buff=0.3)
        conds = VGroup(T("Reversible only if:", size=28, color=th.INK, weight="SEMIBOLD"),
                       T("1.  quasi-static: infinitely slow, always in equilibrium", size=24, color=th.BODY),
                       T("2.  no friction, viscosity or electrical resistance", size=24, color=th.BODY),
                       T("3.  no heat flow across a finite temperature gap", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -1.2, 0])
        with self.say("Slide a block across a rough floor. Friction turns its kinetic energy into heat, which spreads out into the floor. Push the block back, and friction heats the floor again. You can return the block, but never un-warm the floor."):
            self.play(Create(surf))
            self.add(blk, sparks)
            self.play(FadeIn(blk), FadeIn(lab))
            self.play(x.animate.set_value(3.2), run_time=2.5)
            self.play(x.animate.set_value(0), run_time=2.5)
        self.play(FadeOut(VGroup(surf, lab)), FadeOut(blk), FadeOut(sparks))
        self.remove(blk, sparks)
        conds.move_to([0, -1.3, 0])
        with self.say("So a process can be reversible only if it is quasi static, carried out infinitely slowly, and free of every dissipative effect: friction, viscosity, electrical resistance, and heat flowing across a finite temperature difference.") as v:
            for c in conds:
                self.play(FadeIn(c, shift=LEFT * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.7)
        self.play(FadeOut(VGroup(d, conds)))
        cols = VGroup(
            VGroup(T("Reversible (ideal)", size=28, color=th.MINT, weight="BOLD"), T("infinitely slow", size=24), T("no dissipation", size=24), T("Carnot cycle", size=24)),
            VGroup(T("Irreversible (real)", size=28, color=th.CORAL, weight="BOLD"), T("finite speed", size=24), T("friction, turbulence", size=24), T("free expansion, burning fuel, rubbing hands", size=24)),
        )
        for c in cols:
            c.arrange(DOWN, buff=0.3)
        cols.arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.2, 0])
        with self.say("No real process is ever truly reversible. Free expansion, burning fuel, rubbing your hands together: all irreversible. Reversibility is a limiting ideal, but it is a useful one, because it sets the best performance any real machine could ever approach."):
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in cols[0]], lag_ratio=0.2), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in cols[1]], lag_ratio=0.2), run_time=1.5)
        nb = neby_in(self, "think")
        self.wait(0.4)
        self.play(FadeOut(cols))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        d1, s1 = self.flow(cx=-3.4, q1=1.0, q2=0.0, hot="one reservoir", cold="no sink")
        head = T("Kelvin–Planck", size=32, color=th.CORAL, weight="BOLD").move_to([3.0, 2.6, 0])
        stmt = para("It is impossible to build a device that, operating in a cycle, produces no effect other than taking heat from a single reservoir and doing an equal amount of work.", width=5.8, size=24, color=th.INK).next_to(head, DOWN, buff=0.3)
        with self.say("There are two classical statements of the second law. First, the Kelvin Planck statement, the engine statement. Imagine an engine that takes heat from one reservoir, and turns all of it into work, with nothing thrown away."):
            self.play(FadeIn(d1[0][0]), FadeIn(d1[0][2]), FadeIn(d1[0][4]), FadeIn(d1[0][5]))
            self.play(GrowArrow(d1[1][0]), GrowArrow(d1[1][2]), FadeIn(d1[2][0]), FadeIn(d1[2][2]))
            self.add(s1[0], s1[2])
        x = xmark(d1[0][4].get_center(), 0.8)
        with self.say("Kelvin Planck says: impossible. No device working in a cycle can have, as its only effect, taking heat from a single reservoir and doing an equal amount of work. In plain words, no engine can be one hundred percent efficient."):
            self.play(FadeIn(head), FadeIn(stmt))
            self.sfx("wrong", gain=-8)
            self.play(Create(x))
        self.play(FadeOut(VGroup(d1[0], d1[1], d1[2], x, head, stmt)), FadeOut(s1[0]), FadeOut(s1[2]))
        self.remove(s1)
        d2, s2 = self.flow(cx=-3.4, fridge=True, q1=0.6, q2=0.6, hot="hot body", cold="cold body", mid="device")
        head2 = T("Clausius", size=32, color=th.SKY, weight="BOLD").move_to([3.0, 2.6, 0])
        stmt2 = para("It is impossible for a self-acting device, operating in a cycle, to transfer heat from a colder body to a hotter body without external work.", width=5.8, size=24, color=th.INK).next_to(head2, DOWN, buff=0.3)
        with self.say("Second, the Clausius statement, the refrigerator statement. Imagine a device that quietly pumps heat from a cold body into a hot one, with no power supply at all."):
            self.play(FadeIn(d2[0]))
            self.play(GrowArrow(d2[1][0]), GrowArrow(d2[1][1]), FadeIn(d2[2][0]), FadeIn(d2[2][1]))
            self.add(s2[0], s2[1])
        x2 = xmark(d2[0][4].get_center(), 0.8)
        with self.say("Clausius says: impossible. No self acting device working in a cycle can transfer heat from a colder body to a hotter body without external work being done on it. Every refrigerator needs to be plugged in."):
            self.play(FadeIn(head2), FadeIn(stmt2))
            self.sfx("wrong", gain=-8)
            self.play(Create(x2))
        self.play(FadeOut(VGroup(d2[0], d2[1][0], d2[1][1], d2[2][0], d2[2][1], x2, head2, stmt2)), FadeOut(s2[0]), FadeOut(s2[1]))
        self.remove(s2)
        self.equivalence()
        self.isothermal_small_print()
        self.quiz("The Clausius statement of the second law forbids",
                  ["a 100% efficient engine", "unaided heat flow cold → hot", "turning work into heat", "adiabatic expansion"], 1,
                  "Pause and think. Which one does the Clausius statement forbid?",
                  "B. Clausius is the refrigerator statement: no self acting device can move heat from cold to hot. Option A is also forbidden by the second law, but that is the Kelvin Planck statement. Turning work into heat, as friction does, is always allowed.")

    def equivalence(self):
        title = T("The two statements are equivalent", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        hot = RoundedRectangle(corner_radius=0.15, width=8.0, height=0.8, stroke_color=C_Q1, fill_color=C_Q1, fill_opacity=0.25).move_to([0, 2.0, 0])
        cold = RoundedRectangle(corner_radius=0.15, width=8.0, height=0.8, stroke_color=C_Q2, fill_color=C_Q2, fill_opacity=0.25).move_to([0, -2.4, 0])
        hl = T("source  T₁", size=24).move_to(hot)
        cl = T("sink  T₂", size=24).move_to(cold)
        E = Circle(radius=0.65, stroke_color=th.INK, fill_color=th.PANEL, fill_opacity=1).move_to([-2.0, -0.2, 0])
        F = Circle(radius=0.65, stroke_color=th.CORAL, fill_color=th.PANEL, fill_opacity=1).move_to([2.0, -0.2, 0])
        El, Fl = T("engine", size=20).move_to(E), T("cheat", size=20, color=th.CORAL).move_to(F)
        a1 = Arrow(hot.get_bottom() + LEFT * 2.0, E.get_top(), buff=0.05, color=C_Q1, stroke_width=10)
        a2 = Arrow(E.get_bottom(), cold.get_top() + LEFT * 2.0, buff=0.05, color=C_Q2, stroke_width=7)
        aw = Arrow(E.get_left(), E.get_left() + LEFT * 1.8, buff=0.05, color=C_W, stroke_width=6)
        b2 = Arrow(cold.get_top() + RIGHT * 2.0, F.get_bottom(), buff=0.05, color=C_Q2, stroke_width=7)
        b1 = Arrow(F.get_top(), hot.get_bottom() + RIGHT * 2.0, buff=0.05, color=C_Q2, stroke_width=7)
        labs = VGroup(M("Q_1", size=32, color=C_Q1).next_to(a1, LEFT, buff=0.1), M("Q_2", size=32, color=C_Q2).next_to(a2, LEFT, buff=0.1),
                      M("W = Q_1 - Q_2", size=30, color=C_W).next_to(aw, UP, buff=0.1), M("Q_2", size=32, color=C_Q2).next_to(b2, RIGHT, buff=0.1),
                      M("Q_2", size=32, color=C_Q2).next_to(b1, RIGHT, buff=0.1))
        with self.say("These two statements look different, but each implies the other. Suppose someone builds a cheat device that breaks Clausius: it moves heat Q two from the sink up to the source, for free."):
            self.play(FadeIn(title), FadeIn(hot), FadeIn(cold), FadeIn(hl), FadeIn(cl))
            self.play(FadeIn(F), FadeIn(Fl), GrowArrow(b2), GrowArrow(b1), FadeIn(labs[3]), FadeIn(labs[4]))
        with self.say("Couple it to an ordinary engine that takes Q one from the source, does work, and rejects exactly Q two into the sink."):
            self.play(FadeIn(E), FadeIn(El), GrowArrow(a1), GrowArrow(a2), GrowArrow(aw), FadeIn(labs[0]), FadeIn(labs[1]), FadeIn(labs[2]))
        with self.say("Now look at the sink. Every cycle it receives Q two, and loses Q two. Its net change is zero, so we can take it away altogether."):
            self.play(Indicate(VGroup(a2, b2), color=WHITE))
            self.play(FadeOut(VGroup(cold, cl, a2, b2, labs[1], labs[3])))
        box = SurroundingRectangle(VGroup(E, F, b1), color=th.AMBER, buff=0.3)
        res = T("one reservoir in, work out: breaks Kelvin–Planck!", size=26, color=th.CORAL).to_edge(DOWN, buff=0.7)
        with self.say("What is left is a single machine that draws Q one minus Q two from one reservoir, and turns all of it into work. That breaks Kelvin Planck. So breaking one statement breaks the other. They are the same law, seen from two sides."):
            self.play(Create(box))
            self.play(FadeIn(res, shift=UP * 0.2))
            self.sfx("wrong", gain=-10)
        self.play(FadeOut(VGroup(title, hot, hl, E, F, El, Fl, a1, aw, b1, labs[0], labs[2], labs[4], box, res)))

    def isothermal_small_print(self):
        cx, yb = -3.6, -2.5
        Vt = ValueTracker(1.5)
        cyl = Cylinder(cx, yb, 2.2, 4.6, lambda: Vt.get_value(), lambda: 330, n=26, rod=0.5)
        bath = Rectangle(width=3.0, height=0.5, stroke_width=0, fill_color=C_Q1, fill_opacity=0.6).next_to(cyl.walls, DOWN, buff=0)
        st = Stream([[cx, yb - 0.4, 0], [cx, yb + 0.6, 0]], n=4, color=C_Q1, speed=0.8)
        eqs = VGroup(M(r"\Delta U = 0 \Rightarrow Q = W", size=44), T("all the heat became work...", size=26, color=th.AMBER),
                     T("...but the gas is left expanded.", size=26, color=th.AMBER), T("Not a cycle, not the sole effect.", size=26, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.3, 0])
        with self.say("A careful student might object. In an isothermal expansion of an ideal gas, delta U is zero, so Q equals W. All the heat becomes work. Does that break the second law?"):
            self.play(Create(cyl.walls), FadeIn(bath))
            self.add(cyl.fill, cyl.gas, cyl.piston, st)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston))
            self.play(Vt.animate.set_value(3.6), run_time=3)
            self.play(Write(eqs[0]))
        with self.say("No. Read the small print. After the expansion the gas is left in a different state, bigger than before. Converting heat to work was not the only effect, and the process cannot be repeated in a cycle without pushing the piston back. The word cycle in both statements is doing real work. Never drop it."):
            for e in eqs[1:]:
                self.play(FadeIn(e, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeOut(VGroup(eqs, bath)), FadeOut(st))
        self.remove(st)
        cyl.drop(self)

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        d, s = self.flow(cx=-2.6)
        defn = para("A heat engine takes a working substance round a cycle: it absorbs Q₁ from a hot source, turns part into work W, and rejects Q₂ to a cold sink.", width=5.0, size=24, color=th.INK).move_to([3.6, 1.6, 0])
        with self.say("A heat engine converts heat into work continuously, by taking a working substance round and round a cycle. It absorbs heat Q one from a hot source, at temperature T one."):
            self.play(FadeIn(d[0]))
            self.play(GrowArrow(d[1][0]), FadeIn(d[2][0]))
            self.add(s[0])
        with self.say("It turns part of that heat into useful work, W. And it rejects the rest, Q two, into a cold sink at temperature T two."):
            self.play(GrowArrow(d[1][2]), FadeIn(d[2][2]))
            self.add(s[2])
            self.play(GrowArrow(d[1][1]), FadeIn(d[2][1]))
            self.add(s[1])
            self.play(FadeIn(defn))
        eqs = VGroup(M(r"\Delta U = 0\ \text{(cycle)}", size=40), M(r"W = Q_1 - Q_2", size=46, color=C_W),
                     M(r"\eta = \frac{W}{Q_1} = 1 - \frac{Q_2}{Q_1}", size=52, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, -1.3, 0])
        with self.say("The working substance comes back to its starting state every cycle, so delta U is zero. The first law then says the work out is Q one minus Q two."):
            self.play(FadeOut(defn), Write(eqs[0]))
            self.play(Write(eqs[1]))
        with self.say("The thermal efficiency, eta, is the useful work divided by the heat you paid for: W over Q one, which is one minus Q two over Q one."):
            self.play(Write(eqs[2]))
        self.play(FadeOut(VGroup(d, eqs)), FadeOut(s))
        self.remove(s)
        q2 = ValueTracker(0.7)
        A1 = Arrow([-3.0, 2.0, 0], [-3.0, 0.4, 0], buff=0, color=C_Q1, stroke_width=14)
        eng = Circle(radius=0.6, stroke_color=th.INK, fill_color=th.PANEL, fill_opacity=1).move_to([-3.0, -0.2, 0])
        A2 = always_redraw(lambda: Arrow([-3.0, -0.8, 0], [-3.0, -2.6, 0], buff=0, color=C_Q2, stroke_width=max(0.5, 14 * q2.get_value()),
                                         max_tip_length_to_length_ratio=0.25 if q2.get_value() > 0.03 else 0.0001).set_opacity(min(1, q2.get_value() * 6)))
        A3 = always_redraw(lambda: Arrow([-2.4, -0.2, 0], [-0.2, -0.2, 0], buff=0, color=C_W, stroke_width=max(1, 14 * (1 - q2.get_value()))))
        eta = readout("η =", lambda: 100 * (1 - q2.get_value()), "%", size=48, color=th.AMBER).move_to([3.0, 0.6, 0])
        with self.say("Now play with it. Throw less heat into the sink, and the efficiency rises. Could we make Q two zero, and reach one hundred percent?"):
            self.add(A2, A3)
            self.play(GrowArrow(A1), FadeIn(eng), FadeIn(A2), FadeIn(A3), FadeIn(eta))
            self.play(q2.animate.set_value(0.25), run_time=2.5)
            self.play(q2.animate.set_value(0.0), run_time=2)
        x = xmark([-3.0, -1.7, 0], 0.4)
        no = para("η = 1 needs Q₂ = 0: an engine with no sink. Kelvin–Planck forbids it.", width=5.4, size=26, color=th.CORAL).move_to([3.0, -1.0, 0])
        with self.say("That would need an engine with no sink at all, which is exactly what Kelvin Planck forbids. Every heat engine must have a sink, so its efficiency is always less than one hundred percent."):
            self.sfx("wrong", gain=-8)
            self.play(Create(x), FadeIn(no))
            self.play(q2.animate.set_value(0.6), FadeOut(x), run_time=1.5)
        self.play(FadeOut(VGroup(A1, eng, eta, no)), FadeOut(A2), FadeOut(A3))
        self.remove(A2, A3)
        cards = VGroup()
        for i, (h, b, col) in enumerate([("External combustion", "fuel burns outside the cylinder: the steam engine and the steam turbine", th.AMBER),
                                         ("Internal combustion", "fuel burns inside the cylinder: petrol and diesel engines, where the burning mixture is itself the working substance", th.CORAL)]):
            box = self.panel(5.6, 2.6)
            hh = T(h, size=28, color=col, weight="BOLD")
            bb = para(b, width=5.0, size=22, color=th.BODY)
            VGroup(hh, bb).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, hh, bb))
        cards.arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        with self.say("Engines are sorted by where the fuel burns. In an external combustion engine, like a steam turbine, it burns outside, and heats the working substance through a wall. In an internal combustion engine, like the petrol and diesel engines in our vehicles, the fuel burns inside the cylinder, and the burning mixture is itself the working substance."):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.play(FadeOut(cards))
        self.example_51()

    def example_51(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A heat engine absorbs 2000 J per cycle from a source at 500 K and rejects 1400 J to a sink at 300 K. Find the work per cycle and the efficiency. Is such an engine possible?",
                    width=12.2, size=27, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        with self.say("Worked example. A heat engine absorbs two thousand joules per cycle from a source at five hundred kelvin, and rejects one thousand four hundred joules to a sink at three hundred kelvin. Find the work and the efficiency. Is such an engine possible?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        base = -2.9
        b1 = Rectangle(width=1.1, height=3.4, fill_color=C_Q1, fill_opacity=0.9, stroke_width=0).move_to([-5.0, base, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.1, height=3.4 * 0.7, fill_color=C_Q2, fill_opacity=0.9, stroke_width=0).move_to([-3.5, base, 0], aligned_edge=DOWN)
        b3 = Rectangle(width=1.1, height=3.4 * 0.3, fill_color=C_W, fill_opacity=0.9, stroke_width=0).move_to([-3.5, base + 3.4 * 0.7, 0], aligned_edge=DOWN)
        bl = VGroup(M("Q_1 = 2000", size=26, color=C_Q1).next_to(b1, UP, buff=0.1), M("Q_2 = 1400", size=26, color=C_Q2).move_to(b2).rotate(PI / 2),
                    M("W = 600", size=26, color=C_W).next_to(b3, RIGHT, buff=0.1))
        steps = VGroup(M(r"W = Q_1 - Q_2 = 2000 - 1400 = 600\ \text{J}", size=36), M(r"\eta = \frac{600}{2000} = 0.30 = 30\%", size=38, color=th.AMBER),
                       M(r"\eta_{\max} = 1 - \frac{T_2}{T_1} = 1 - \frac{300}{500} = 40\%", size=36), M(r"30\% < 40\% \;\Rightarrow\; \text{possible}", size=38, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.4, -1.2, 0])
        with self.say("The work is Q one minus Q two: two thousand minus fourteen hundred, six hundred joules per cycle. So the efficiency is six hundred over two thousand, thirty percent."):
            self.play(GrowFromEdge(b1, DOWN), FadeIn(bl[0]))
            self.play(TransformFromCopy(b1, VGroup(b2, b3)), FadeIn(bl[1]), FadeIn(bl[2]))
            self.play(Write(steps[0]))
            self.play(Write(steps[1]))
        with self.say("Is it possible? We will soon prove that the best any engine can do between these temperatures is the Carnot efficiency, one minus T two over T one: one minus three hundred over five hundred, forty percent. Thirty is below forty, so this engine breaks no law. It is possible, though not reversible."):
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
        nb = neby_in(self, "success")
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, b1, b2, b3, bl, steps)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        self.otto()
        self.otto_curve()
        self.diesel()
        self.carnot()
        self.carnot_derive()
        example(self, "A Carnot engine works between a source at 227 °C and a sink at 27 °C, absorbing 6000 J per cycle. Find its efficiency, the work done and the heat rejected.",
                [r"T_1 = 227 + 273 = 500\ \text{K},\quad T_2 = 27 + 273 = 300\ \text{K}",
                 r"\eta = 1 - \frac{T_2}{T_1} = 1 - \frac{300}{500} = 0.40 = 40\%",
                 r"W = \eta Q_1 = 0.40 \times 6000 = 2400\ \text{J}",
                 r"Q_2 = Q_1 - W = 6000 - 2400 = 3600\ \text{J}\quad \left(\tfrac{Q_2}{Q_1} = 0.6 = \tfrac{T_2}{T_1}\ \checkmark\right)"],
                ["Worked example. A Carnot engine works between a source at two hundred and twenty seven degrees Celsius and a sink at twenty seven degrees, absorbing six thousand joules per cycle. Find the efficiency, the work, and the heat rejected.",
                 "Kelvin first, always. Add two seventy three: five hundred kelvin and three hundred kelvin.",
                 "The efficiency is one minus three hundred over five hundred: zero point four, forty percent.",
                 "The work is eta times Q one: zero point four times six thousand, two thousand four hundred joules.",
                 "And the heat rejected is the rest: three thousand six hundred joules. Check: three thousand six hundred over six thousand is zero point six, which is T two over T one. Consistent."], size=36)
        self.quiz("The efficiency of a Carnot engine working between 27 °C and 327 °C is",
                  ["50%", "25%", "75%", "92%"], 0,
                  "Your turn. A Carnot engine works between twenty seven and three hundred and twenty seven degrees Celsius. What is its efficiency? Pause and think.",
                  "A, fifty percent. In kelvin, the temperatures are three hundred and six hundred, so eta is one minus a half. If you got ninety two percent, you used Celsius: one minus twenty seven over three twenty seven. Always convert to kelvin.")

    def otto(self):
        cx, yb = -5.2, -2.6
        g = 1.4
        P2 = 3 ** g
        P3 = 2 * P2
        P4 = P3 / P2
        u = ValueTracker(0)

        def VP(x):
            k = int(min(3.999, max(0, x)))
            a = x - k
            if k == 0:
                V = 3 - 2 * a
                return V, (3 / V) ** g
            if k == 1:
                return 1.0, P2 + (P3 - P2) * a
            if k == 2:
                V = 1 + 2 * a
                return V, P3 * (1 / V) ** g
            return 3.0, P4 + (1 - P4) * a
        h = lambda: 0.95 * VP(u.get_value())[0]
        Tk = lambda: 100 * VP(u.get_value())[0] * VP(u.get_value())[1]
        cyl = Cylinder(cx, yb, 2.0, 3.6, h, Tk, Tlo=250, Thi=950, n=26, rod=0.4)
        plug = VGroup(Rectangle(width=0.2, height=0.35, fill_color=th.MUTED, fill_opacity=1, stroke_width=0)).move_to([cx + 0.75, yb + 0.15, 0])
        gp = pv_axes(xr=(0, 3.6, 1), yr=(0, 10.5, 1), x_len=5.0, y_len=4.6).move_to([-0.6, -0.3, 0])
        ax = gp[0]
        dot = always_redraw(lambda: Dot(ax.c2p(*VP(u.get_value())), radius=0.1, color=WHITE))
        trace = TracedPath(dot.get_center, stroke_color=th.AMBER, stroke_width=4)
        nums = VGroup(*[M(str(i + 1), size=30).next_to(ax.c2p(*VP(i)), d, buff=0.12) for i, d in zip(range(4), [RIGHT, LEFT, LEFT, RIGHT])])
        title = T("The Otto cycle: an ideal petrol engine", size=30, color=th.INK, weight="BOLD").move_to([-0.6, 2.75, 0])
        rows = VGroup()
        info = [("1 → 2", "adiabatic compression", th.SKY), ("2 → 3", "spark: heat in at constant V", th.CORAL), ("3 → 4", "adiabatic expansion: power", th.MINT), ("4 → 1", "exhaust: heat out at constant V", th.AMBER)]
        for a, b, c in info:
            rows.add(VGroup(T(a, size=22, color=c, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.05))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.5, -0.3, 0])
        with self.say("Real engines run on particular cycles. The four stroke petrol engine in a motorbike is modelled by the Otto cycle. Here is its cylinder, and beside it, its indicator diagram."):
            self.play(FadeIn(title), Create(cyl.walls), Create(gp))
            self.add(cyl.fill, cyl.gas, cyl.piston, dot)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(dot), FadeIn(nums[0]))
        self.add(trace)
        says = ["One to two: the piston compresses the fuel air mixture quickly, so there is no time for heat to escape. An adiabatic compression, and the temperature rises.",
                "Two to three: the spark plug fires at the top of the stroke. The mixture burns almost instantly, before the piston can move, so heat Q one goes in at constant volume. The pressure leaps.",
                "Three to four: the power stroke. The hot gas drives the piston out, adiabatically, doing work.",
                "Four to one: the exhaust valve opens, and the pressure drops at constant volume, throwing heat Q two away. Then the cycle repeats."]
        for k, sy in enumerate(says):
            with self.say(sy):
                self.play(FadeIn(rows[k], shift=LEFT * 0.2), FadeIn(nums[(k + 1) % 4]), run_time=0.5)
                if k == 1:
                    fl = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=c, fill_opacity=0.6) for r, c in ((0.5, th.AMBER), (0.25, WHITE))]).move_to([cx, yb + 0.5, 0])
                    self.sfx("impact", gain=-8)
                    self.play(FadeIn(fl, scale=0.3), run_time=0.3)
                    self.play(u.animate.set_value(2), FadeOut(fl, scale=2), run_time=1.6)
                else:
                    self.play(u.animate.set_value(k + 1), run_time=2.4, rate_func=smooth)
        area = ax.get_area(ax.plot(lambda v: P3 * (1 / v) ** g, x_range=[1, 3]), x_range=[1, 3],
                           bounded_graph=ax.plot(lambda v: (3 / v) ** g, x_range=[1, 3]), color=th.AMBER, opacity=0.35)
        with self.say("The loop is traced clockwise, and the area inside it is the net work done in each cycle."):
            self.play(FadeIn(area))
            u.set_value(0)
            self.play(u.animate.set_value(4), run_time=4, rate_func=linear)
        self.remove(trace)
        self.play(FadeOut(VGroup(title, gp, nums, rows, area)), FadeOut(dot))
        self.remove(dot)
        cyl.drop(self)

    def otto_curve(self):
        eq = M(r"\eta_{\text{Otto}} = 1 - \frac{1}{r^{\gamma - 1}},\qquad r = \frac{V_1}{V_2}", size=46).to_edge(UP, buff=0.85)
        sub = T("compression ratio r: how much the mixture is squeezed", size=24, color=th.MUTED).next_to(eq, DOWN, buff=0.15)
        with self.say("Using Q equals n C v delta T on the two constant volume steps, and T V to the gamma minus one on the two adiabatics, the ideal efficiency comes out as one minus one over r to the gamma minus one. Here r is the compression ratio, V one over V two."):
            self.play(Write(eq), FadeIn(sub))
        ax = Axes(x_range=[1, 23, 2], y_range=[0, 0.8, 0.2], x_length=8.8, y_length=3.6, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([-0.6, -0.85, 0])
        xl = T("compression ratio r", size=22, color=th.BODY).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = T("η", size=28, color=th.AMBER).next_to(ax.y_axis.get_top(), UP, buff=0.1)
        f = lambda r: 1 - r ** -0.4
        curve = ax.plot(f, x_range=[1, 22], color=th.AMBER, stroke_width=5)
        knock = Rectangle(width=ax.c2p(22, 0)[0] - ax.c2p(10, 0)[0], height=3.6, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.12).move_to(ax.c2p(16, 0.4))
        kl = T("petrol knocks here", size=20, color=th.CORAL).move_to(ax.c2p(16, 0.12))
        r = ValueTracker(2)
        dot = always_redraw(lambda: Dot(ax.c2p(r.get_value(), f(r.get_value())), color=WHITE))
        ro = VGroup(readout("r =", lambda: r.get_value(), "", decimals=1, size=26), readout("η =", lambda: 100 * f(r.get_value()), "%", decimals=1, size=26, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.3, -0.2, 0])
        with self.say("Notice it depends only on r and gamma, not on how much fuel you burn. Squeeze harder, and the efficiency climbs. With gamma equal to one point four, a compression ratio of eight gives fifty six point five percent."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(curve))
            self.add(dot)
            self.play(FadeIn(ro))
            self.play(r.animate.set_value(8), run_time=2.5)
        with self.say("Raise it to ten, and you get sixty point two percent. So why not squeeze even more? Above about ten, the petrol air mixture gets so hot that it explodes on its own before the spark. That is called knocking, and it limits petrol engines to ratios of about eight to ten. Real ones manage only twenty five to thirty percent, because of friction, heat loss and incomplete burning."):
            self.play(r.animate.set_value(10), run_time=1.5)
            self.play(FadeIn(knock), FadeIn(kl))
        self.play(FadeOut(VGroup(eq, sub, ax, xl, yl, curve, knock, kl, ro)), FadeOut(dot))
        self.remove(dot)

    def diesel(self):
        g = 1.4
        gp = pv_axes(xr=(0, 5.6, 1), yr=(0, 10.5, 1), x_len=5.6, y_len=4.4).move_to([-3.5, -0.4, 0])
        ax = gp[0]
        V1, V2, V3 = 5.0, 1.0, 2.0
        P2 = (V1 / V2) ** g * 1.0
        P2 = min(P2, 9.5)
        K = P2 * V2 ** g
        P4 = P2 * (V3 / V1) ** g
        segs = [ax.plot(lambda v: K / v ** g, x_range=[V2, V1], color=th.SKY, stroke_width=5),
                Line(ax.c2p(V2, P2), ax.c2p(V3, P2), color=th.CORAL, stroke_width=5),
                ax.plot(lambda v: P2 * (V3 / v) ** g, x_range=[V3, V1], color=th.MINT, stroke_width=5),
                Line(ax.c2p(V1, P4), ax.c2p(V1, K / V1 ** g), color=th.AMBER, stroke_width=5)]
        nums = VGroup(M("1", size=28).next_to(ax.c2p(V1, K / V1 ** g), RIGHT, buff=0.1), M("2", size=28).next_to(ax.c2p(V2, P2), LEFT, buff=0.1),
                      M("3", size=28).next_to(ax.c2p(V3, P2), UP, buff=0.1), M("4", size=28).next_to(ax.c2p(V1, P4), RIGHT, buff=0.1))
        title = T("The Diesel cycle", size=32, color=th.INK, weight="BOLD").move_to([2.9, 2.6, 0])
        pts = VGroup(T("compresses air alone: no knocking, r = 15 to 22", size=22, color=th.BODY),
                     T("hot air ignites the sprayed fuel", size=22, color=th.BODY),
                     T("heat added at constant PRESSURE (2 → 3)", size=22, color=th.CORAL),
                     T("cut-off ratio ρ = V₃ / V₂", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.9, 1.2, 0])
        eq = M(r"\eta_{\text{D}} = 1 - \frac{1}{\gamma r^{\gamma-1}}\left[\frac{\rho^{\gamma} - 1}{\rho - 1}\right]", size=38).move_to([2.9, -1.3, 0])
        with self.say("A diesel engine is different. It compresses air alone, so there is no fuel to knock, and the compression ratio can be fifteen to twenty two. As we saw in the last unit, the squeezed air gets hot enough to ignite the fuel sprayed in at the top."):
            self.play(FadeIn(title), Create(gp))
            self.play(Create(segs[0]), FadeIn(nums[0]), FadeIn(nums[1]))
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
        with self.say("The fuel burns as it is sprayed in, while the piston is already moving out, so heat is added at roughly constant pressure. A flat line from two to three. Then the power stroke, and the exhaust at constant volume."):
            self.play(Create(segs[1]), FadeIn(nums[2]), FadeIn(pts[2]))
            self.play(Create(segs[2]), FadeIn(nums[3]))
            self.play(Create(segs[3]))
        with self.say("Its efficiency includes the cut off ratio, rho, equal to V three over V two. For the same r, a diesel cycle is slightly less efficient than an Otto cycle. But because r can be made so much bigger, the real diesel engine wins comfortably. That is why trucks and buses run on diesel."):
            self.play(FadeIn(pts[3]), Write(eq))
        self.play(FadeOut(VGroup(title, gp, *segs, nums, pts, eq)))

    def carnot(self):
        gm = 2.2
        A, B, C, D = (1.0, 12.0), (2.2, 12.0 / 2.2), (3.9203, 1.5305), (1.7818, 3.3673)
        KH, KC = 12.0, 6.0
        u = ValueTracker(0)

        def VP(x):
            k = int(min(3.999, max(0, x)))
            a = x - k
            if k == 0:
                V = A[0] + (B[0] - A[0]) * a
                return V, KH / V
            if k == 1:
                V = B[0] + (C[0] - B[0]) * a
                return V, B[1] * (B[0] / V) ** gm
            if k == 2:
                V = C[0] + (D[0] - C[0]) * a
                return V, KC / V
            V = D[0] + (A[0] - D[0]) * a
            return V, A[1] * (A[0] / V) ** gm
        cx, yb = -5.4, -2.3
        h = lambda: 0.8 * VP(u.get_value())[0]
        Tk = lambda: 50 * VP(u.get_value())[0] * VP(u.get_value())[1]
        cyl = Cylinder(cx, yb, 1.8, 3.6, h, Tk, Tlo=250, Thi=650, n=22, rod=0.3)
        plate = {"hot": Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=C_Q1, fill_opacity=0.9),
                 "ins": Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=th.FAINT, fill_opacity=1),
                 "cold": Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=C_Q2, fill_opacity=0.9)}
        for p in plate.values():
            p.next_to(cyl.walls, DOWN, buff=0.02)
        pl = {"hot": T("source T₁", size=20, color=C_Q1), "ins": T("insulating stand", size=20, color=th.MUTED), "cold": T("sink T₂", size=20, color=C_Q2)}
        for k, t in pl.items():
            t.next_to(plate[k], DOWN, buff=0.08)
        gp = pv_axes(xr=(0, 4.5, 1), yr=(0, 13, 1), x_len=4.6, y_len=4.6).move_to([-1.1, -0.35, 0])
        ax = gp[0]
        dot = always_redraw(lambda: Dot(ax.c2p(*VP(u.get_value())), radius=0.1, color=WHITE))
        cols = [C_Q1, th.MINT, C_Q2, th.AMBER]
        curves = VGroup(*[ax.plot_parametric_curve(lambda a, k=k: np.array(VP(k + a)), t_range=[0, 0.999], color=cols[k], stroke_width=5) for k in range(4)])
        labs = VGroup(*[M(n, size=30).next_to(ax.c2p(*p), d, buff=0.1) for n, p, d in zip("ABCD", (A, B, C, D), (RIGHT, UR, RIGHT, DL))])
        title = T("The Carnot cycle", size=32, color=th.INK, weight="BOLD").move_to([-1.1, 2.75, 0])
        rows = VGroup(*[VGroup(T(a, size=22, color=c, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.05) for a, b, c in
                        [("A → B", "isothermal at T₁: absorbs Q₁", C_Q1), ("B → C", "adiabatic: cools to T₂", th.MINT),
                         ("C → D", "isothermal at T₂: rejects Q₂", C_Q2), ("D → A", "adiabatic: warms to T₁", th.AMBER)]])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.3, -0.3, 0])
        with self.say("Sadi Carnot asked the deepest question of all. What is the greatest efficiency any engine could have, working between two given temperatures? His answer was an imaginary engine, perfectly reversible, running this cycle. The working substance is an ideal gas in a cylinder with perfectly insulating walls and a perfectly conducting base."):
            self.play(FadeIn(title), Create(cyl.walls), Create(gp))
            self.add(cyl.fill, cyl.gas, cyl.piston, dot)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(dot), FadeIn(labs[0]))
        order = ["hot", "ins", "cold", "ins"]
        says = ["Step one, A to B. Stand the cylinder on the hot source at T one, and let the gas expand slowly. It stays at T one, absorbing heat Q one and doing work. An isothermal expansion.",
                "Step two, B to C. Move it onto an insulating stand, and let it keep expanding. No heat can enter, so the gas cools until it reaches T two. An adiabatic expansion.",
                "Step three, C to D. Put it on the cold sink at T two, and compress it slowly. It stays at T two, and rejects heat Q two into the sink. An isothermal compression.",
                "Step four, D to A. Back on the insulating stand, and compress it further. With no heat escaping, it warms back up to T one, and the cycle is closed. An adiabatic compression."]
        cur = None
        for k in range(4):
            with self.say(says[k]):
                new = VGroup(plate[order[k]], pl[order[k]])
                anims = [FadeIn(new)] + ([FadeOut(cur)] if cur is not None else [])
                self.play(*anims, FadeIn(rows[k], shift=LEFT * 0.2), FadeIn(labs[(k + 1) % 4]), run_time=0.6)
                self.play(u.animate.set_value(k + 0.999), Create(curves[k]), run_time=3.0, rate_func=linear)
                cur = new
        self.play(FadeOut(cur))
        area = Polygon(*[ax.c2p(*VP(x)) for x in np.linspace(0, 3.999, 160)], stroke_width=0, fill_color=th.AMBER, fill_opacity=0.25)
        with self.say("Two isothermals and two adiabatics, every step reversible. The enclosed area is the net work done per cycle."):
            self.play(FadeIn(area))
        self.play(FadeOut(VGroup(title, gp, curves, labs, rows, area)), FadeOut(dot))
        self.remove(dot)
        cyl.drop(self)

    def carnot_derive(self):
        title = T("Efficiency of the Carnot engine", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(
            M(r"A\to B:\ \ Q_1 = nRT_1\ln\frac{V_2}{V_1}", size=36),
            M(r"C\to D:\ \ Q_2 = nRT_2\ln\frac{V_3}{V_4}", size=36),
            M(r"T_1V_2^{\gamma-1} = T_2V_3^{\gamma-1},\quad T_1V_1^{\gamma-1} = T_2V_4^{\gamma-1}", size=36),
            M(r"\Rightarrow\ \frac{V_2}{V_1} = \frac{V_3}{V_4}", size=36),
            M(r"\frac{Q_2}{Q_1} = \frac{T_2}{T_1}", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.4)
        L.set_x(-0.5)
        says = ["Now the derivation, a long question favourite. Take n moles of ideal gas. On the isothermal A to B, delta U is zero, so the heat absorbed equals the work: n R T one ln of V two over V one.",
                "Likewise on C to D, the heat rejected is n R T two ln of V three over V four.",
                "Now the two adiabatics. Apply T V to the gamma minus one equals constant, from B to C, and from D to A.",
                "Divide one equation by the other. The temperatures cancel, and V two over V one equals V three over V four.",
                "So the two logarithms are equal, and they cancel in the ratio. Q two over Q one is simply T two over T one."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        res = M(r"\eta = 1 - \frac{Q_2}{Q_1} = 1 - \frac{T_2}{T_1}", size=56, color=th.AMBER).next_to(L, DOWN, buff=0.35)
        box = SurroundingRectangle(res, color=th.AMBER, buff=0.18, corner_radius=0.12)
        with self.say("And the Carnot efficiency is one minus T two over T one."):
            self.sfx("impact", gain=-12)
            self.play(Write(res), Create(box))
        self.play(FadeOut(L), VGroup(res, box).animate.next_to(title, DOWN, buff=0.4))
        notes = VGroup(T("• contains nothing about the working substance: air, steam, helium, all the same", size=24, color=th.BODY),
                       T("• η = 1 only if T₂ = 0 K, which can never be reached", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(box, DOWN, buff=0.4)
        thm = self.callout("key", "Carnot's theorem: (a) no engine between two temperatures can beat a reversible engine between the same temperatures; (b) all reversible engines between them have the same efficiency, whatever the working substance.", width=11.5, size=24)
        thm.next_to(notes, DOWN, buff=0.35)
        with self.say("Look at what is missing. Nothing about the working substance. Air, steam or helium, the answer is the same. And the efficiency would reach one only if the sink were at absolute zero, which can never be reached."):
            self.play(FadeIn(notes[0], shift=RIGHT * 0.2))
            self.play(FadeIn(notes[1], shift=RIGHT * 0.2))
        with self.say("This is Carnot's theorem. No engine working between two temperatures can be more efficient than a reversible engine between the same temperatures. And all reversible engines between them have the same efficiency, whatever the working substance."):
            self.play(FadeIn(thm, shift=UP * 0.2))
        nb = neby_in(self, "cool", corner=DL)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, res, box, notes, thm)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        d, s = self.flow(cx=-2.6, fridge=True, q1=1.0, q2=0.7, hot="kitchen", cold="inside")
        with self.say("A refrigerator is a heat engine run backwards. A compressor supplies work W. The machine pulls heat Q two out of the cold interior, and dumps heat Q one into the warmer kitchen."):
            self.play(FadeIn(d[0]))
            self.play(GrowArrow(d[1][1]), FadeIn(d[2][1]))
            self.play(GrowArrow(d[1][2]), FadeIn(d[2][2]))
            self.play(GrowArrow(d[1][0]), FadeIn(d[2][0]))
            self.add(s)
        eqs = VGroup(M(r"Q_1 = Q_2 + W", size=44), M(r"\beta = \frac{Q_2}{W} = \frac{Q_2}{Q_1 - Q_2}", size=48, color=th.AMBER),
                     M(r"\beta_{\max} = \frac{T_2}{T_1 - T_2}", size=48, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, 0.3, 0])
        with self.say("Energy is conserved, so the heat delivered to the kitchen is the heat removed plus the work: Q one equals Q two plus W. The Clausius statement is simply the claim that W can never be zero."):
            self.play(Write(eqs[0]))
        with self.say("What you want is heat removed from the food, and what you pay for is the work. So the performance figure is beta, Q two over W, called the coefficient of performance. It is not an efficiency, because it is usually bigger than one. A good fridge moves four or five joules of heat for every joule of electricity."):
            self.play(Write(eqs[1]))
        with self.say("For an ideal, reversible Carnot refrigerator, Q two over Q one equals T two over T one, so the best possible coefficient is T two over T one minus T two."):
            self.play(Write(eqs[2]))
        self.play(FadeOut(VGroup(d, eqs)), FadeOut(s))
        self.remove(s)
        self.cop_graph()
        self.fridge_loop()
        self.example_54()
        self.quiz("The maximum coefficient of performance of a refrigerator working between 250 K and 300 K is",
                  ["5", "6", "0.2", "1.2"], 0,
                  "Pause and think. A refrigerator works between two hundred and fifty and three hundred kelvin. What is its maximum coefficient of performance?",
                  "A, five. Beta max is T two over T one minus T two: two fifty over fifty. Six is the tempting wrong answer: that is T one over the difference, which is the coefficient of a heat pump, not a refrigerator.")

    def cop_graph(self):
        ax = Axes(x_range=[0, 100, 20], y_range=[0, 30, 10], x_length=7.5, y_length=4.0, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([-1.4, -0.6, 0])
        xl = T("temperature gap T₁ − T₂ (K), kitchen at 300 K", size=22, color=th.BODY).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = T("β max", size=24, color=th.MINT).next_to(ax.y_axis.get_top(), UP, buff=0.15)
        f = lambda d: (300 - d) / d
        curve = ax.plot(f, x_range=[9.7, 100], color=th.MINT, stroke_width=5)
        d = ValueTracker(15)
        dot = always_redraw(lambda: Dot(ax.c2p(d.get_value(), f(d.get_value())), color=WHITE))
        ro = readout("β =", lambda: f(d.get_value()), "", decimals=1, size=30, color=th.MINT).move_to([4.6, 1.2, 0])
        tags = VGroup(T("chiller", size=22, color=th.SKY).next_to(ax.c2p(15, f(15)), RIGHT, buff=0.2), T("deep freezer", size=22, color=th.CORAL).next_to(ax.c2p(80, f(80)), UP, buff=0.3))
        with self.say("Notice what happens as the temperature gap grows. The coefficient falls steeply. A chiller, keeping drinks just below room temperature, is cheap to run. A deep freezer, pumping heat across a big gap, costs far more."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(curve))
            self.add(dot)
            self.play(FadeIn(ro), FadeIn(tags[0]))
            self.play(d.animate.set_value(80), run_time=3)
            self.play(FadeIn(tags[1]))
        rel = M(r"\beta = \frac{1 - \eta}{\eta}", size=44).move_to([4.6, -0.3, 0])
        with self.say("And comparing with the engine formula gives a neat link: beta equals one minus eta, over eta."):
            self.play(Write(rel))
        self.play(FadeOut(VGroup(ax, xl, yl, curve, ro, tags, rel)), FadeOut(dot))
        self.remove(dot)

    def fridge_loop(self):
        cab = RoundedRectangle(corner_radius=0.15, width=3.6, height=4.8, stroke_color=th.BODY, stroke_width=4).move_to([-3.6, -0.3, 0])
        cabl = T("inside the cabinet", size=22, color=th.SKY).next_to(cab, UP, buff=0.12)
        food = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.6, height=0.45, fill_color=c, fill_opacity=0.8, stroke_width=0) for c in (th.LIME, th.CORAL, th.AMBER)]).arrange(RIGHT, buff=0.25).move_to([-3.6, -1.6, 0])
        pts = [[-4.8, 1.4, 0], [-2.4, 1.4, 0], [-2.4, 1.0, 0], [-4.8, 1.0, 0], [-4.8, 0.6, 0], [-2.4, 0.6, 0], [-1.0, 0.6, 0], [-1.0, -2.2, 0],
               [1.0, -2.2, 0], [1.0, -1.6, 0], [3.4, -1.6, 0], [3.4, -1.1, 0], [1.4, -1.1, 0], [1.4, -0.6, 0], [3.4, -0.6, 0], [3.4, -0.1, 0],
               [1.4, -0.1, 0], [1.4, 0.4, 0], [3.4, 0.4, 0], [3.4, 1.9, 0], [-1.4, 1.9, 0], [-4.8, 1.9, 0], [-4.8, 1.4, 0]]
        pipe = VMobject(stroke_color=th.FAINT, stroke_width=10).set_points_as_corners(pts)
        comp = Circle(radius=0.45, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=th.INK, stroke_width=3).move_to([0.0, -2.2, 0])
        valve = Square(0.4, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).rotate(PI / 4).move_to([-1.4, 1.9, 0])
        L = np.cumsum([0] + [np.linalg.norm(np.array(pts[i + 1]) - np.array(pts[i])) for i in range(len(pts) - 1)])
        Lt = L[-1]
        t_comp, t_valve = L[8] / Lt - 0.04, L[20] / Lt

        def col(t):
            if t < t_comp * 0.999 and t > L[6] / Lt:
                return th.SKY
            if t_comp <= t < L[10] / Lt:
                return th.CORAL
            if L[10] / Lt <= t < t_valve:
                return interpolate_color(ManimColor(th.CORAL), ManimColor(th.AMBER), (t - L[10] / Lt) / (t_valve - L[10] / Lt))
            if t >= t_valve or t < L[6] / Lt:
                return th.SKY
            return th.SKY
        st = Stream(pts, n=34, color=col, speed=1.3, radius=0.07)
        labs = VGroup(T("compressor (work W in)", size=20, color=th.INK).next_to(comp, DOWN, buff=0.15),
                      T("condenser coils at the back: Q₁ out", size=20, color=th.CORAL).move_to([2.4, 2.35, 0]),
                      T("throttle valve", size=20, color=th.BODY).next_to(valve, UP, buff=0.12).shift(RIGHT * 0.2),
                      T("evaporator: Q₂ in", size=20, color=th.SKY).move_to([-3.6, 0.15, 0]))
        heat_out = VGroup(*[Arrow([3.5, y, 0], [4.6, y, 0], buff=0, color=th.CORAL, stroke_width=4) for y in (-1.35, -0.35, 0.65)])
        with self.say("Inside a real fridge, a volatile liquid called the refrigerant does the carrying. Follow it round. The compressor squeezes the refrigerant vapour, making it hot."):
            self.play(Create(cab), FadeIn(cabl), FadeIn(food), Create(pipe))
            self.play(FadeIn(comp), FadeIn(valve), FadeIn(labs[0]))
            self.add(st)
        with self.say("The hot vapour flows through the coils at the back, where it gives heat Q one to the kitchen and condenses into a liquid. That is why the back of a fridge feels warm."):
            self.play(FadeIn(labs[1]), LaggedStart(*[GrowArrow(a) for a in heat_out], lag_ratio=0.2))
        with self.say("The liquid passes through a narrow throttle valve, where it expands and cools sharply. Then it evaporates in the coils inside the cabinet, soaking up heat Q two from the food, and returns to the compressor. Round and round."):
            self.play(FadeIn(labs[2]))
            self.play(FadeIn(labs[3]))
            self.wait(2)
        hp = T("A heat pump is the same machine, used for its hot end: COP = Q₁ / W", size=24, color=th.AMBER).to_edge(DOWN, buff=0.55)
        with self.say("A heat pump is exactly the same machine, used to warm a room with its hot end. Its coefficient is Q one over W."):
            self.play(FadeIn(hp, shift=UP * 0.2))
        self.play(FadeOut(VGroup(cab, cabl, food, pipe, comp, valve, labs, heat_out, hp)), FadeOut(st))
        self.remove(st)

    def example_54(self):
        example(self, "A refrigerator keeps its freezer at −13 °C in a kitchen at 27 °C. Assuming ideal operation, find its COP, the work needed to remove 1300 J of heat, and the heat delivered to the kitchen.",
                [r"T_2 = -13 + 273 = 260\ \text{K},\quad T_1 = 300\ \text{K}",
                 r"\beta = \frac{T_2}{T_1 - T_2} = \frac{260}{40} = 6.5",
                 r"W = \frac{Q_2}{\beta} = \frac{1300}{6.5} = 200\ \text{J}",
                 r"Q_1 = Q_2 + W = 1300 + 200 = 1500\ \text{J}"],
                ["Worked example. A refrigerator keeps its freezer at minus thirteen degrees Celsius, in a kitchen at twenty seven degrees. Assuming ideal operation, find its coefficient of performance, the work to remove thirteen hundred joules, and the heat delivered to the kitchen.",
                 "Kelvin again. Minus thirteen plus two seventy three is two hundred and sixty kelvin. The kitchen is three hundred.",
                 "Beta is T two over the difference: two sixty over forty, which is six point five.",
                 "The work needed is Q two over beta: thirteen hundred over six point five, just two hundred joules.",
                 "And the kitchen receives Q two plus W, fifteen hundred joules. So leaving the fridge door open warms your kitchen. It never cools it."], size=40)
        self.tip("Always convert to kelvin before using η = 1 − T₂/T₁ or β = T₂/(T₁ − T₂). COP is not an efficiency: it is often bigger than 1.",
                 "Two traps in this unit. First, every temperature formula here needs kelvin. Using Celsius gives nonsense. Second, the coefficient of performance is not an efficiency, so do not be alarmed when it comes out bigger than one.", state="wink")

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        d = M(r"dS = \frac{dQ_{\text{rev}}}{T},\qquad \Delta S = \int\frac{dQ_{\text{rev}}}{T}", size=54).to_edge(UP, buff=1.0)
        u = T("unit: J K⁻¹   ·   a state function", size=26, color=th.MUTED).next_to(d, DOWN, buff=0.25)
        with self.say("Clausius found a way to turn the second law from a prohibition into an equation. He defined a new state function, entropy, S. When a small amount of heat d Q is transferred reversibly at absolute temperature T, the change in entropy is d Q over T. Its unit is joules per kelvin."):
            self.play(Write(d))
            self.play(FadeIn(u))
        chk = VGroup(M(r"\text{Carnot cycle: gains } \frac{Q_1}{T_1},\ \text{loses } \frac{Q_2}{T_2}", size=38),
                     M(r"\frac{Q_2}{Q_1} = \frac{T_2}{T_1} \Rightarrow \frac{Q_1}{T_1} = \frac{Q_2}{T_2} \Rightarrow \Delta S_{\text{cycle}} = 0", size=38, color=th.MINT)).arrange(DOWN, buff=0.35).move_to([0, -0.6, 0])
        with self.say("Being a state function, entropy returns to its starting value round any cycle. Check it on the Carnot cycle. The gas gains Q one over T one, and loses Q two over T two. Since Q two over Q one equals T two over T one, these are equal. The net change is zero."):
            self.play(Write(chk[0]))
            self.play(Write(chk[1]))
        self.play(FadeOut(VGroup(d, u, chk)))
        self.disorder()
        self.universe()
        example(self, "One kilogram of ice at 0 °C melts completely into water at 0 °C. Find the change in entropy (latent heat of fusion 3.34 × 10⁵ J/kg).",
                [r"T = 0 + 273 = 273\ \text{K}\ \ (\text{constant})",
                 r"Q = mL = 1 \times 3.34\times10^{5} = 3.34\times10^{5}\ \text{J}",
                 r"\Delta S = \frac{Q}{T} = \frac{3.34\times10^{5}}{273} = 1.22\times10^{3}\ \text{J K}^{-1}"],
                ["Worked example. One kilogram of ice at zero degrees Celsius melts completely into water at zero degrees. Find the change in entropy.",
                 "Melting happens at a constant temperature, two hundred and seventy three kelvin, so the integral is easy: delta S is just Q over T.",
                 "The heat absorbed is m L: one times three point three four times ten to the five joules.",
                 "Divide by two seventy three: one point two two times ten to the three joules per kelvin. Positive, as it must be. Liquid water is more disordered than ice."], size=40)
        self.quiz("In every real (irreversible) process, the entropy of the universe",
                  ["decreases", "remains constant", "increases", "becomes zero"], 2,
                  "One last check. In every real, irreversible process, what happens to the entropy of the universe? Pause and think.",
                  "C, it increases. It stays constant only in the ideal reversible limit, and it never decreases. That is the second law in one line.")

    def disorder(self):
        title = T("Entropy measures disorder", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cols = []
        rng = np.random.default_rng(2)
        xs = [-4.4, 0, 4.4]
        names = [("ice", th.SKY), ("water", th.TEAL), ("steam", th.CORAL)]
        boxes = VGroup(*[Square(3.0, stroke_color=th.BODY, stroke_width=3).move_to([x, -0.3, 0]) for x in xs])
        labs = VGroup(*[T(n, size=28, color=c, weight="SEMIBOLD").next_to(b, DOWN, buff=0.2) for (n, c), b in zip(names, boxes)])
        jig = ValueTracker(0)
        lattice = VGroup(*[Dot([xs[0] - 1.0 + 0.5 * i, -1.3 + 0.5 * j, 0], radius=0.09, color=th.SKY) for i in range(5) for j in range(5)])
        base = [d.get_center().copy() for d in lattice]
        phases = rng.uniform(0, TAU, (25, 2))

        def jiggle(m):
            t = jig.get_value()
            for d, b, ph in zip(m, base, phases):
                d.move_to(b + 0.05 * np.array([np.sin(9 * t + ph[0]), np.sin(11 * t + ph[1]), 0]))
        lattice.add_updater(jiggle)
        liq = Gas(lambda: (xs[1] - 1.45, xs[1] + 1.45, -1.75, 0.0), n=25, base=0.5, seed=3, fill=th.TEAL, radius=0.09)
        vap = Gas(lambda: (xs[2] - 1.45, xs[2] + 1.45, -1.75, 1.15), n=25, base=2.2, seed=9, fill=th.CORAL, radius=0.09)
        bars = VGroup(*[Rectangle(width=0.5, height=h, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).next_to(b, RIGHT, buff=0.12).align_to(b, DOWN) for b, h in zip(boxes, (0.6, 1.4, 2.9))])
        sl = T("S", size=24, color=th.AMBER).next_to(bars[0], UP, buff=0.08)
        with self.say("What is entropy, physically? It measures disorder. More exactly, it counts how many microscopic arrangements of the molecules look the same from outside."):
            self.play(FadeIn(title), Create(boxes), FadeIn(labs))
        with self.say("In ice, the molecules are locked in a lattice. They can only jiggle in place. Few arrangements, low entropy."):
            self.add(lattice)
            self.play(FadeIn(lattice), jig.animate.set_value(3), run_time=2.5, rate_func=linear)
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(sl))
        with self.say("In water, they tumble freely past each other. Higher entropy. In steam, they fly anywhere in the whole space. Higher still."):
            self.add(liq, vap)
            self.play(FadeIn(liq), FadeIn(vap), jig.animate.set_value(5), run_time=1.5, rate_func=linear)
            self.play(GrowFromEdge(bars[1], DOWN), jig.animate.set_value(6), run_time=1, rate_func=linear)
            self.play(GrowFromEdge(bars[2], DOWN), jig.animate.set_value(7), run_time=1, rate_func=linear)
        self.play(FadeOut(VGroup(title, boxes, labs, bars, sl)), FadeOut(lattice), FadeOut(liq), FadeOut(vap))
        lattice.clear_updaters()
        self.remove(lattice, liq, vap)

    def universe(self):
        title = T("Why heat flows from hot to cold", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        hot = Square(2.0, fill_color=C_Q1, fill_opacity=0.7, stroke_width=0).move_to([-4.2, 0.6, 0])
        cold = Square(2.0, fill_color=C_Q2, fill_opacity=0.7, stroke_width=0).move_to([-1.0, 0.6, 0])
        hl = M("500\\ \\text{K}", size=32).move_to(hot)
        cl = M("250\\ \\text{K}", size=32).move_to(cold)
        st = Stream([hot.get_center(), cold.get_center()], n=4, color=th.AMBER, speed=0.9)
        ql = M(r"Q = 1000\ \text{J}", size=32, color=th.AMBER).next_to(VGroup(hot, cold), UP, buff=0.3)
        steps = VGroup(M(r"\Delta S_{\text{hot}} = -\frac{1000}{500} = -2\ \text{J K}^{-1}", size=34, color=C_Q1),
                       M(r"\Delta S_{\text{cold}} = +\frac{1000}{250} = +4\ \text{J K}^{-1}", size=34, color=C_Q2),
                       M(r"\Delta S_{\text{total}} = +2\ \text{J K}^{-1} > 0", size=38, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        with self.say("Now see why heat flows from hot to cold. Let one thousand joules leave a body at five hundred kelvin, and enter one at two hundred and fifty kelvin."):
            self.play(FadeIn(title), FadeIn(hot), FadeIn(cold), FadeIn(hl), FadeIn(cl))
            self.add(st)
            self.play(FadeIn(ql))
        with self.say("The hot body loses one thousand over five hundred, two joules per kelvin. The cold body gains one thousand over two fifty, four joules per kelvin. The total entropy goes up by two. Run it backwards, and the total would fall by two. That never happens."):
            for s_ in steps:
                self.play(Write(s_), run_time=1.0)
        law = self.callout("key", M(r"\Delta S_{\text{universe}} \ge 0", size=50, color=th.INK), width=7)
        law.to_edge(DOWN, buff=0.6)
        with self.say("This is the second law as an inequality. In any process, the total entropy of the system and its surroundings never decreases. It stays the same only for a reversible process. Every real process increases the entropy of the universe."):
            self.play(FadeIn(law, shift=UP * 0.2))
        nb = neby_in(self, "surprised", corner=DL)
        with self.say("And that is the answer to our bouncing ball. The ball's neat, ordered energy spreads into the jiggling of countless molecules in the floor. Entropy rises. The backwards film would need the entropy of the universe to fall, so it never plays. The second law gives time its arrow."):
            self.play(Circumscribe(law, color=th.AMBER))
        self.play(FadeOut(VGroup(title, hot, cold, hl, cl, ql, steps, law)), FadeOut(st))
        self.remove(st)
        neby_out(self, nb)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Real processes run one way. Reversible means quasi-static with no dissipation; no real process is reversible.",
            "Kelvin–Planck: no cyclic engine turns all heat from one reservoir into work. Clausius: no cyclic device moves heat cold → hot for free. They are equivalent.",
            M(r"\text{engine: } W = Q_1 - Q_2,\quad \eta = 1 - \frac{Q_2}{Q_1} < 1", size=34),
            M(r"\text{Otto: } \eta = 1 - \frac{1}{r^{\gamma-1}};\ \ \text{Diesel: heat in at constant } P,\ r = 15\text{–}22", size=32),
            M(r"\text{Carnot: } \eta = 1 - \frac{T_2}{T_1}\ (\text{maximum, any substance})", size=34),
            M(r"\text{fridge: } Q_1 = Q_2 + W,\ \ \beta = \frac{Q_2}{W},\ \ \beta_{\max} = \frac{T_2}{T_1 - T_2}", size=34),
            M(r"dS = \frac{dQ_{\text{rev}}}{T},\ \ \Delta S = \frac{mL}{T},\ \ \Delta S_{\text{universe}} \ge 0", size=34),
        ], "Let us recap. Natural processes run one way, and no real process is reversible. Kelvin Planck forbids a perfect engine, and Clausius forbids a fridge that needs no power. An engine's efficiency is one minus Q two over Q one. The Otto cycle gives one minus one over r to the gamma minus one, and the diesel cycle allows a bigger r. The Carnot efficiency, one minus T two over T one, is the maximum possible. A refrigerator's coefficient of performance is Q two over W. And entropy, d Q over T, never decreases for the universe as a whole.")
        self.outro("That is the second law of thermodynamics, the reason engines need a sink and time has a direction. Next, we leave heat behind and start a new adventure: wave motion. See you there, on NEBians.")
