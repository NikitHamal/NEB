import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import (Cylinder, Gas, example, flame, heat_color, neby_in, neby_out, nothing, pv_axes,  # noqa: E402
                   readout, sdash)

C_Q, C_W, C_U, C_P, C_V, C_T = th.CORAL, th.MINT, th.AMBER, th.SKY, th.PINK, th.LIME


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 4
    TITLE = "First Law of Thermodynamics"
    SUBTITLE = "Heat, work and internal energy"
    SECTIONS = ["Thermodynamic systems", "Work done during volume change", "Heat, internal energy, first law",
                "Thermodynamic processes", "Heat capacities: Cp − Cv = R", "Isothermal and adiabatic changes"]
    NEXT = "Unit 5 · Second Law of Thermodynamics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ the diesel cylinder (cold open + example 4.4)
    def diesel(self, cx=-3.0):
        yb, w, H = -2.7, 2.4, 4.9
        h0 = 4.0
        s = ValueTracker(0.0)          # 0 = full volume, 1 = squeezed to one eighth
        h = lambda: h0 * (1 - s.get_value() * 7 / 8)
        Tk = lambda: 300 * (h0 / h()) ** 0.4
        cyl = Cylinder(cx, yb, w, H, h, Tk, Tlo=280, Thi=700, n=40, rod=0.5)
        inj = VGroup(Rectangle(width=0.3, height=0.35, fill_color=th.MUTED, fill_opacity=1, stroke_width=0),
                     Triangle(fill_color=th.MUTED, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)).arrange(DOWN, buff=0)
        inj.next_to(cyl.walls, RIGHT, buff=0.05).align_to(cyl.walls, DOWN).shift(UP * 0.1)
        return cyl, s, Tk, h, yb

    def cold_open(self):
        cyl, s, Tk, h, yb = self.diesel()
        tag = T("A diesel engine cylinder", size=26, color=th.MUTED).next_to(cyl.walls, UP, buff=0.9)
        temp = readout("T =", Tk, "K", size=40, color=th.INK).move_to([3.0, 1.9, 0])
        bulb = Circle(radius=0.32, fill_color=th.CORAL, fill_opacity=1, stroke_color=th.BODY, stroke_width=3).move_to([5.6, -2.2, 0])
        tube = RoundedRectangle(corner_radius=0.12, width=0.32, height=3.6, stroke_color=th.BODY, stroke_width=3).next_to(bulb, UP, buff=-0.08)
        merc = always_redraw(lambda: Rectangle(width=0.16, height=0.15 + 3.2 * (Tk() - 300) / 420, stroke_width=0,
                                               fill_color=heat_color((Tk() - 280) / 420), fill_opacity=1).align_to(tube, DOWN).shift(UP * 0.08).set_x(5.6))
        no = T("no spark plug", size=28, color=th.AMBER).move_to([3.0, 0.9, 0])
        with self.say("This is the cylinder of a diesel engine, the kind that hauls buses and trucks up the Prithvi Highway every day. Inside is nothing but air, at an ordinary temperature of three hundred kelvin."):
            self.play(Create(cyl.walls), FadeIn(tag))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(cyl.fill), FadeIn(temp))
            self.add(merc)
            self.play(FadeIn(bulb), Create(tube), FadeIn(merc))
        with self.say("Look closely. There is no spark plug. No match, no flame, nothing to light the fuel."):
            self.play(FadeIn(no, shift=UP * 0.2))
            self.play(Indicate(no, color=th.CORAL))
        with self.say("Now the piston slams down and squeezes the air into one eighth of its space. Watch the molecules, and watch the thermometer."):
            self.sfx("whoosh", gain=-8)
            self.play(s.animate.set_value(1.0), run_time=2.6, rate_func=rate_functions.ease_in_cubic)
            self.sfx("thud", gain=-6)
        spray = VGroup(*[Dot(radius=0.04, color=th.AMBER) for _ in range(14)])
        top = cyl.yb + h()
        for i, d in enumerate(spray):
            d.move_to([-3.0 + (i - 6.5) * 0.12, top - 0.05, 0])
        burst = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=c, fill_opacity=0.5).move_to([-3.0, cyl.yb + h() / 2, 0])
                         for r, c in [(0.9, th.AMBER), (0.6, th.CORAL), (0.35, WHITE)]])
        with self.say("A squirt of diesel goes in, and it bursts into flame by itself. Six hundred and eighty nine kelvin. Hot enough to ignite the fuel with no spark at all."):
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in spray], lag_ratio=0.05), run_time=0.6)
            self.sfx("impact", gain=-4)
            self.play(FadeIn(burst, scale=0.2), FadeOut(spray), run_time=0.4)
            self.play(FadeOut(burst, scale=1.6), run_time=0.8)
        nb = neby_in(self, "surprised", corner=DL)
        q = T("How can squeezing air make it hot?", size=34, color=th.AMBER, weight="BOLD", display=True).move_to([2.0, -0.4, 0])
        with self.say("How can simply squeezing air make it hot enough to light a fire? The answer is the first law of thermodynamics. By the end of this lesson, you will calculate that six hundred and eighty nine kelvin yourself."):
            self.play(FadeIn(q, shift=UP * 0.2))
        self.play(FadeOut(VGroup(tag, temp, bulb, tube, no, q)), FadeOut(merc))
        self.remove(merc)
        cyl.drop(self)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 4: the First Law of Thermodynamics. Thermodynamics is the book keeping of energy. Energy that goes into a gas must come out again, or stay inside it. Write that one sentence carefully, and you can explain engines, refrigerators, and even the weather."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is our path. Thermodynamic systems, the work done when a gas changes volume, the first law itself, the four standard processes, the two heat capacities of a gas, and finally the isothermal and adiabatic changes that every exam asks about.")

    # ------------------------------------------------------------------ part 1: systems
    def p1(self):
        self.section(0)
        box = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.6, stroke_width=0, fill_color=th.PANEL, fill_opacity=1).move_to([-2.4, -0.2, 0])
        gas = Gas(lambda: (box.get_left()[0] + 0.1, box.get_right()[0] - 0.1, box.get_bottom()[1] + 0.1, box.get_top()[1] - 0.1), n=26, seed=5)
        bound = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.6, height=2.6, stroke_color=th.AMBER, stroke_width=5).move_to(box), num_dashes=40)
        ls = T("system", size=30, color=th.SKY, weight="SEMIBOLD").next_to(box, DOWN, buff=0.2)
        lb = T("boundary", size=26, color=th.AMBER).next_to(bound, UP, buff=0.2)
        lsur = T("surroundings", size=30, color=th.MUTED, weight="SEMIBOLD").move_to([3.4, 1.6, 0])
        with self.say("Thermodynamics always starts by drawing a line. The system is the definite piece of matter we choose to study, usually a fixed mass of gas in a cylinder."):
            self.play(FadeIn(box))
            self.add(gas)
            self.play(FadeIn(gas), FadeIn(ls))
        with self.say("Everything outside that can exchange energy with it is the surroundings. And the real or imaginary surface between the two is the boundary."):
            self.play(FadeIn(lsur, shift=LEFT * 0.3))
            self.play(Create(bound), FadeIn(lb))
        self.play(FadeOut(VGroup(box, bound, ls, lb, lsur)), FadeOut(gas))
        self.remove(gas)
        self.three_systems()
        self.state_point()
        self.quasi_static()
        self.state_path()

    def three_systems(self):
        title = T("What can cross the boundary?", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        data = [("Open", "water boiling in an open pan", True, True), ("Closed", "gas sealed in a metal cylinder", False, True),
                ("Isolated", "hot tea in a perfect thermos", False, False)]
        cards = VGroup()
        for name, ex, mm, ee in data:
            panel = self.panel(3.9, 4.4)
            hd = T(name, size=32, color=th.INK, weight="BOLD").move_to(panel.get_top() + DOWN * 0.45)
            sysb = Square(1.3, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.12).move_to(panel.get_center() + RIGHT * 0.75 + UP * 0.15)
            if name == "Isolated":
                sysb.set_stroke(WHITE, 6)
            rows = VGroup()
            for k, (lab, ok, col) in enumerate([("matter", mm, th.MINT), ("energy", ee, th.CORAL)]):
                y = sysb.get_center()[1] + (0.35 if k == 0 else -0.35)
                a0 = np.array([panel.get_left()[0] + 0.25, y, 0])
                a1 = np.array([sysb.get_left()[0] + 0.25 if ok else sysb.get_left()[0] - 0.2, y, 0])
                ar = Arrow(a0, a1, buff=0, color=col if ok else th.MUTED, stroke_width=5, max_tip_length_to_length_ratio=0.25)
                tl = T(lab, size=20, color=col if ok else th.MUTED).next_to(Line(a0, a1), UP, buff=0.05)
                cross = VGroup() if ok else VGroup(Line(UL, DR), Line(DL, UR)).set_stroke(th.CORAL, 4).scale(0.13).move_to(a1 + LEFT * 0.35)
                rows.add(VGroup(ar, tl, cross))
            exl = para(ex, width=3.4, size=21, color=th.BODY, align="center").move_to(panel.get_bottom() + UP * 0.75)
            cards.add(VGroup(panel, hd, sysb, rows, exl))
        cards.arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.2))
        says = ["An open system lets both matter and energy cross. Water boiling in an open pan takes in heat from the stove, and loses steam into the room.",
                "A closed system lets energy cross, but not matter. Gas sealed in a metal cylinder can be heated or cooled, but no molecule gets in or out. This is the system we will use for the rest of the unit.",
                "And an isolated system lets nothing cross at all, neither matter nor energy. A perfect thermos flask of hot tea is the closest thing in your kitchen."]
        for cd, say in zip(cards, says):
            with self.say(say):
                self.play(FadeIn(cd[0]), FadeIn(cd[1]), FadeIn(cd[2]), run_time=0.6)
                for r in cd[3]:
                    self.play(GrowArrow(r[0]), FadeIn(r[1]), run_time=0.6)
                    if len(r[2]):
                        self.sfx("wrong", gain=-16)
                        self.play(Create(r[2]), run_time=0.4)
                self.play(FadeIn(cd[4]))
        self.play(FadeOut(VGroup(title, cards)))

    def state_point(self):
        cx, yb = -3.6, -2.4
        Vt = ValueTracker(2.0)
        nRT = 8.0
        h = lambda: 0.75 * Vt.get_value()
        cyl = Cylinder(cx, yb, 2.0, 4.6, h, lambda: 300, n=26, rod=0.4)
        g = pv_axes(xr=(0, 6.2, 1), yr=(0, 6.2, 1), x_len=5.6, y_len=4.2).move_to([2.6, -0.1, 0])
        ax = g[0]
        dot = always_redraw(lambda: Dot(ax.c2p(Vt.get_value(), nRT / Vt.get_value()), radius=0.1, color=th.AMBER))
        eq = M(r"PV = nRT", size=56).move_to([2.6, 2.75, 0])
        rv = VGroup(readout("P =", lambda: nRT / Vt.get_value(), "", decimals=2, size=26, color=C_P),
                    readout("V =", lambda: Vt.get_value(), "", decimals=2, size=26, color=C_V),
                    readout("T =", lambda: 300, "K", size=26, color=C_T)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rv.move_to([-1.3, 2.3, 0])
        with self.say("The condition of a gas is described by its state variables: pressure, volume, temperature, and the amount of gas. For an ideal gas they are tied together by one equation of state, P V equals n R T."):
            self.play(Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), Write(eq))
            self.play(FadeIn(rv))
        with self.say("So for a fixed amount of gas, only two of them can be chosen freely. Fix the volume and the temperature, and the pressure is decided. That means a state can be drawn as a single point on a pressure volume graph."):
            self.play(Create(g))
            self.add(dot)
            self.play(FadeIn(dot, scale=2))
        path = TracedPath(dot.get_center, stroke_color=th.AMBER, stroke_width=4)
        self.add(path)
        lab = T("indicator diagram", size=26, color=th.AMBER).next_to(ax.c2p(5.4, 1.6), UP, buff=0.3)
        with self.say("Let the gas expand slowly, keeping it at the same temperature. The point moves, and its track is a curve. A process is a curve on this graph, which is called an indicator diagram."):
            self.play(Vt.animate.set_value(5.5), run_time=3.0)
            self.play(FadeIn(lab))
            self.play(Vt.animate.set_value(1.6), run_time=2.5)
        self.play(FadeOut(VGroup(g, eq, rv, lab)), FadeOut(dot), FadeOut(path))
        self.remove(dot, path)
        cyl.drop(self)

    def quasi_static(self):
        title = T("Thermodynamic equilibrium", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        items = VGroup(*[T(s, size=28, color=th.BODY) for s in
                         ["mechanical  ·  no unbalanced pressure", "thermal  ·  one uniform temperature", "chemical  ·  no reaction going on"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        items.next_to(title, DOWN, buff=0.5)
        ticks = VGroup(*[T("✓", size=32, color=th.MINT).next_to(it, LEFT, buff=0.3) for it in items])
        with self.say("A point on that graph only makes sense if the gas is in thermodynamic equilibrium. That means three things at once. Mechanical equilibrium: no unbalanced pressure. Thermal equilibrium: one uniform temperature. And chemical equilibrium: no reaction in progress.") as v:
            self.play(FadeIn(title))
            for it, tk in zip(items, ticks):
                self.play(FadeIn(it, shift=RIGHT * 0.2), FadeIn(tk), run_time=0.6)
                self.hold(v.dur / 3 - 0.9)
        self.play(FadeOut(items), FadeOut(ticks), title.animate.become(T("Quasi-static: infinitely slow", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)))
        cx, yb = -3.6, -2.6
        N = 10
        left = ValueTracker(N)
        Pof = lambda k: 1.0 + 0.45 * k
        Vt = ValueTracker(8.0 / Pof(N))
        h = lambda: 0.85 * Vt.get_value()
        cyl = Cylinder(cx, yb, 2.0, 4.6, h, lambda: 300, n=24, rod=0.0)
        grains = VGroup(*[Rectangle(width=1.4, height=0.12, stroke_width=1, stroke_color=th.BG, fill_color=th.AMBER, fill_opacity=1) for _ in range(N)])

        def place_grains(m):
            top = cyl.piston_y()
            for i, gr in enumerate(m):
                gr.move_to([cx, top + 0.06 + 0.13 * i, 0])
        grains.add_updater(place_grains)
        g = pv_axes(xr=(0, 6.2, 1), yr=(0, 6.2, 1), x_len=5.4, y_len=4.0).move_to([2.6, -0.5, 0])
        ax = g[0]
        dot = always_redraw(lambda: Dot(ax.c2p(Vt.get_value(), 8.0 / Vt.get_value()), radius=0.09, color=th.AMBER))
        with self.say("To keep the gas in equilibrium all the time, the change must be made infinitely slowly. Picture the piston held down by a pile of sand. We take away one grain at a time."):
            self.play(Create(cyl.walls), Create(g))
            self.add(cyl.fill, cyl.gas, cyl.piston, grains, dot)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(grains), FadeIn(dot))
        path = TracedPath(dot.get_center, stroke_color=th.AMBER, stroke_width=4)
        self.add(path)
        with self.say("Each grain changes the pressure by only a tiny amount, so the gas is always almost exactly in equilibrium. The point creeps along a smooth curve. That idealised, infinitely slow process is called quasi static, and only quasi static processes can be drawn as curves.") as v:
            per = (v.dur - 0.5) / N
            for k in range(N - 1, -1, -1):
                gr = grains[-1]
                grains.remove(gr)
                self.play(FadeOut(gr, shift=RIGHT * 0.6), Vt.animate.set_value(8.0 / Pof(k)), run_time=min(0.9, per))
                self.hold(per - 0.9)
        self.play(FadeOut(VGroup(g, title, grains)), FadeOut(dot), FadeOut(path))
        self.remove(dot, path, grains)
        cyl.drop(self)

    def state_path(self):
        title = T("State function or path function?", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        A = np.array([-5.0, -1.4, 0])
        B = np.array([-0.6, 1.9, 0])
        road = Line(A, B, color=th.SKY, stroke_width=5)
        wind = VMobject(stroke_color=th.PINK, stroke_width=5).set_points_smoothly(
            [A, [-3.0, -1.8, 0], [-4.4, 0.0, 0], [-2.2, 0.0, 0], [-3.4, 1.3, 0], [-1.6, 1.1, 0], B])
        da = VGroup(Dot(A, color=WHITE), T("Kathmandu  1400 m", size=22, color=th.BODY).next_to(A, DOWN, buff=0.15))
        db = VGroup(Dot(B, color=WHITE), T("Nagarkot  2100 m", size=22, color=th.BODY).next_to(B, UP, buff=0.15))
        t = ValueTracker(0)
        w1 = always_redraw(lambda: Dot(road.point_from_proportion(t.get_value()), radius=0.11, color=th.SKY))
        w2 = always_redraw(lambda: Dot(wind.point_from_proportion(t.get_value()), radius=0.11, color=th.PINK))
        L1, L2 = 22.0, 41.0
        r1 = readout("straight road:", lambda: L1 * t.get_value(), "km", decimals=1, size=26, color=th.SKY)
        r2 = readout("winding trail:", lambda: L2 * t.get_value(), "km", decimals=1, size=26, color=th.PINK)
        r3 = T("height gained: 700 m either way", size=26, color=th.AMBER)
        rs = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.3, 0])
        with self.say("One more idea before we start. Two hikers go from Kathmandu up to Nagarkot. One takes the straight road, the other a winding trail."):
            self.play(FadeIn(title), FadeIn(da), FadeIn(db), Create(road), Create(wind))
            self.add(w1, w2)
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(r1), FadeIn(r2))
        with self.say("They walk very different distances. But they gain exactly the same height, seven hundred metres, because height depends only on where you start and where you finish."):
            self.play(t.animate.set_value(1), run_time=4, rate_func=smooth)
            self.play(FadeIn(r3, shift=UP * 0.2))
        defs = VGroup(
            T("State function: depends only on the state  ·  P, V, T, U", size=26, color=th.AMBER),
            T("Path function: depends on the route  ·  heat Q, work W", size=26, color=th.PINK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.say("Height is like a state function. Pressure, volume, temperature and internal energy are state functions: they depend only on the present state. Distance walked is like a path function. Heat and work are path functions: they depend on the route taken. That is why we write delta U, but never delta Q."):
            self.play(FadeIn(defs[0], shift=UP * 0.2))
            self.play(FadeIn(defs[1], shift=UP * 0.2))
        nb = neby_in(self, "think", corner=DR)
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, road, wind, da, db, rs, defs)), FadeOut(w1), FadeOut(w2))
        self.remove(w1, w2)
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 2: work
    def p2(self):
        self.section(1)
        cx, yb = -3.4, -2.6
        Vt = ValueTracker(1.6)
        h = lambda: Vt.get_value()
        cyl = Cylinder(cx, yb, 2.4, 4.8, h, lambda: 330, n=30, rod=0.6)
        arrows = always_redraw(lambda: VGroup(*[Arrow([cx + dx, yb + h() - 0.55, 0], [cx + dx, yb + h() - 0.05, 0], buff=0, color=C_P, stroke_width=4,
                                                       max_tip_length_to_length_ratio=0.35) for dx in (-0.7, 0, 0.7)]))
        F = always_redraw(lambda: VGroup(Arrow([cx + 1.6, yb + h() + 0.1, 0], [cx + 1.6, yb + h() + 1.1, 0], buff=0, color=C_W, stroke_width=6),
                                         M(r"F = PA", size=32, color=C_W).move_to([cx + 2.45, yb + h() + 0.7, 0])))
        eqs = VGroup(M(r"F = PA", size=46), M(r"dW = F\,dx = PA\,dx", size=46), M(r"A\,dx = dV", size=46),
                     M(r"dW = P\,dV", size=60, color=C_W)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.6, 0.6, 0])
        with self.say("Now the first big idea: how much work does a gas do when it expands? Take a gas at pressure P in a cylinder, closed by a frictionless piston of area A. The molecules hammer the piston, and push it with a force F equal to P A."):
            self.play(Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston))
            self.add(arrows, F)
            self.play(FadeIn(arrows), FadeIn(F))
            self.play(Write(eqs[0]))
        y1 = yb + 1.6 + 0.0
        slab = Rectangle(width=2.34, height=0.5, stroke_width=0, fill_color=C_W, fill_opacity=0.35).move_to([cx, y1 + 0.25, 0])
        br = BraceBetweenPoints([cx - 1.25, y1, 0], [cx - 1.25, y1 + 0.5, 0], LEFT, color=C_W)
        dxl = M("dx", size=30, color=C_W).next_to(br, LEFT, buff=0.1)
        with self.say("Let the piston move out a tiny distance d x, so slowly that the pressure hardly changes. The work done by the gas is force times distance, P A d x."):
            self.play(Vt.animate.set_value(2.1), run_time=1.5)
            self.play(FadeIn(slab), GrowFromCenter(br), FadeIn(dxl))
            self.play(Write(eqs[1]))
        with self.say("But A times d x is just the extra volume swept out, d V. So the work done by the gas in that small step is P d V."):
            self.play(Write(eqs[2]))
            self.play(Indicate(slab, color=C_W))
            self.sfx("impact", gain=-14)
            self.play(Write(eqs[3]))
        self.play(FadeOut(VGroup(eqs, slab, br, dxl)), FadeOut(arrows), FadeOut(F))
        self.remove(arrows, F)
        cyl.drop(self)
        self.area_work()
        self.signs_paths()

    def area_work(self):
        g = pv_axes(xr=(0, 6, 1), yr=(0, 7, 1), x_len=7.0, y_len=4.6).move_to([-1.6, -0.4, 0])
        ax = g[0]
        f = lambda v: 8.0 / v
        curve = ax.plot(f, x_range=[1.2, 5.6], color=th.ACCENT, stroke_width=5)
        A, B = ax.c2p(1.5, f(1.5)), ax.c2p(4.5, f(4.5))
        dots = VGroup(Dot(A, color=WHITE), Dot(B, color=WHITE), M("A", size=32).next_to(A, UR, buff=0.08), M("B", size=32).next_to(B, UR, buff=0.08))
        ticks = VGroup(M("V_1", size=30).next_to(ax.c2p(1.5, 0), DOWN, buff=0.15), M("V_2", size=30).next_to(ax.c2p(4.5, 0), DOWN, buff=0.15))
        with self.say("For a big change in volume, the pressure usually changes as the gas expands. So draw the process on the indicator diagram, from state A to state B."):
            self.play(Create(g), Create(curve), FadeIn(dots), FadeIn(ticks))
        x = ValueTracker(2.0)
        strip = always_redraw(lambda: Polygon(ax.c2p(x.get_value(), 0), ax.c2p(x.get_value() + 0.18, 0), ax.c2p(x.get_value() + 0.18, f(x.get_value() + 0.09)),
                                              ax.c2p(x.get_value(), f(x.get_value() + 0.09)), stroke_width=0, fill_color=C_W, fill_opacity=0.8))
        sl = always_redraw(lambda: M(r"P\,dV", size=30, color=C_W).next_to(ax.c2p(x.get_value() + 0.09, f(x.get_value() + 0.09)), UP, buff=0.12))
        with self.say("Each tiny step, P d V, is the area of a thin strip under the curve: height P, width d V."):
            self.add(strip, sl)
            self.play(FadeIn(strip), FadeIn(sl))
            self.play(x.animate.set_value(4.2), run_time=2.5)
            self.play(x.animate.set_value(2.6), run_time=1.5)
        self.play(FadeOut(strip), FadeOut(sl))
        self.remove(strip, sl)
        rects = [ax.get_riemann_rectangles(curve, x_range=[1.5, 4.5], dx=d, input_sample_type="center", stroke_width=0.5,
                                           stroke_color=th.BG, fill_opacity=0.6, color=[C_W, th.TEAL]) for d in (0.5, 0.25, 0.1, 0.04)]
        integ = M(r"W = \int_{V_1}^{V_2} P\,dV", size=58).move_to([4.2, 2.2, 0])
        lab = T("= area under the P–V curve", size=28, color=C_W).next_to(integ, DOWN, buff=0.3)
        with self.say("Add up all the strips from V one to V two. As the strips get thinner, the sum becomes exactly the area under the curve. And the sum of infinitely many thin strips is an integral: W equals the integral of P d V."):
            self.play(FadeIn(rects[0]))
            for r0, r1 in zip(rects, rects[1:]):
                self.play(Transform(rects[0], r1), run_time=0.9)
            self.play(Write(integ))
        with self.say("So here is the picture to remember. The work done by a gas is the area under its P V curve."):
            self.play(FadeIn(lab, shift=UP * 0.2))
            self.play(Circumscribe(rects[0], color=C_W, buff=0.05))
        self.play(FadeOut(VGroup(g, curve, dots, ticks, rects[0], integ, lab)))

    def signs_paths(self):
        g = pv_axes(xr=(0, 6, 1), yr=(0, 6, 1), x_len=5.4, y_len=4.0).move_to([-3.4, -0.6, 0])
        ax = g[0]
        f = lambda v: 7.0 / v
        x = ValueTracker(1.5)
        self._dir = 1
        area = always_redraw(lambda: ax.get_area(ax.plot(f, x_range=[1.5, max(1.51, x.get_value())]), x_range=[1.5, max(1.51, x.get_value())],
                                                 color=C_W if self._dir > 0 else C_Q, opacity=0.45))
        curve = ax.plot(f, x_range=[1.3, 5.2], color=th.ACCENT, stroke_width=4)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), f(x.get_value())), color=WHITE))
        sg = T("expansion: W positive", size=30, color=C_W).move_to([3.0, 1.8, 0])
        sg2 = T("compression: W negative", size=30, color=C_Q).move_to([3.0, 1.0, 0])
        with self.say("Two consequences follow at once. When the gas expands, d V is positive, so the work done by the gas is positive. The gas pushes on the surroundings."):
            self.play(Create(g), Create(curve))
            self.add(area, dot)
            self.play(x.animate.set_value(4.8), run_time=2.5)
            self.play(FadeIn(sg))
        with self.say("When the gas is compressed, d V is negative, and the work done by the gas is negative. The surroundings do work on the gas."):
            self._dir = -1
            self.play(x.animate.set_value(1.6), run_time=2.5)
            self.play(FadeIn(sg2))
        self.play(FadeOut(VGroup(g, curve, sg, sg2)), FadeOut(area), FadeOut(dot))
        self.remove(area, dot)
        g = pv_axes(xr=(0, 6, 1), yr=(0, 5.5, 1), x_len=6.0, y_len=4.2).move_to([-2.6, -0.5, 0])
        ax = g[0]
        A, B = (1.5, 4.0), (4.5, 1.5)
        pA, pB = ax.c2p(*A), ax.c2p(*B)
        top = VGroup(Line(pA, ax.c2p(4.5, 4.0)), Line(ax.c2p(4.5, 4.0), pB)).set_stroke(th.AMBER, 5)
        bot = VGroup(Line(pA, ax.c2p(1.5, 1.5)), Line(ax.c2p(1.5, 1.5), pB)).set_stroke(th.SKY, 5)
        aT = Polygon(ax.c2p(1.5, 0), ax.c2p(1.5, 4), ax.c2p(4.5, 4), ax.c2p(4.5, 0), stroke_width=0, fill_color=th.AMBER, fill_opacity=0.3)
        aB = Polygon(ax.c2p(1.5, 0), ax.c2p(1.5, 1.5), ax.c2p(4.5, 1.5), ax.c2p(4.5, 0), stroke_width=0, fill_color=th.SKY, fill_opacity=0.45)
        labs = VGroup(Dot(pA, color=WHITE), Dot(pB, color=WHITE), M("A", size=32).next_to(pA, LEFT, buff=0.1), M("B", size=32).next_to(pB, RIGHT, buff=0.1))
        w1 = M(r"W_{\text{top}} = 4 \times 3 = 12", size=40, color=th.AMBER)
        w2 = M(r"W_{\text{bottom}} = 1.5 \times 3 = 4.5", size=40, color=th.SKY)
        ws = VGroup(w1, w2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 1.2, 0])
        note = para("Same start, same finish, different work. Work is a path function.", width=4.6, size=26, color=th.INK).move_to([3.7, -1.2, 0])
        with self.say("And the second consequence. Take two routes between the same states A and B. On the top route, the gas first expands at high pressure, then cools at constant volume. The area under it is large."):
            self.play(Create(g), FadeIn(labs))
            self.play(Create(top), run_time=1.5)
            self.play(FadeIn(aT), Write(w1))
        with self.say("On the bottom route, it first cools, then expands at low pressure. The area is much smaller. Same start, same finish, very different work. Work depends on the path, exactly like the hiker's distance."):
            self.play(Create(bot), run_time=1.5)
            self.play(FadeIn(aB), Write(w2))
            self.play(FadeIn(note, shift=UP * 0.2))
        self.play(FadeOut(VGroup(g, top, bot, aT, aB, labs, ws, note)))

    # ------------------------------------------------------------------ part 3: first law
    def p3(self):
        self.section(2)
        cx, yb = -3.2, -2.3
        Tt = ValueTracker(300)
        Vt = ValueTracker(2.0)
        cyl = Cylinder(cx, yb, 2.4, 4.6, lambda: Vt.get_value(), lambda: Tt.get_value(), n=30, rod=0.5)
        fl = flame([cx, yb - 0.45, 0], 0.9)
        qa = Arrow([cx + 2.4, yb - 0.4, 0], [cx + 1.35, yb + 0.4, 0], buff=0, color=C_Q, stroke_width=6)
        ql = VGroup(M("Q", size=40, color=C_Q), T("heat: flows because of a temperature difference", size=22, color=C_Q)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ql.next_to(qa.get_start(), RIGHT, buff=0.15)
        wa = always_redraw(lambda: Arrow([cx, cyl.piston_y() + 0.6, 0], [cx, cyl.piston_y() + 1.5, 0], buff=0, color=C_W, stroke_width=6))
        wl = VGroup(M("W", size=40, color=C_W), T("work: a force moves through a distance", size=22, color=C_W)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        with self.say("Energy can cross the boundary of a gas in two ways. Heat, Q, is energy that flows because of a temperature difference: from the hot flame into the cooler gas."):
            self.play(Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston))
            self.play(FadeIn(fl, scale=0.5), GrowArrow(qa), FadeIn(ql))
            self.play(Tt.animate.set_value(420), run_time=2)
        with self.say("Work, W, is energy that crosses because a force moves its point of application, like the gas pushing the piston out. Both are energy in transit. Neither one is stored in the gas."):
            self.add(wa)
            wl.next_to(np.array([cx + 0.7, 2.0, 0]), RIGHT, buff=0)
            self.play(FadeIn(wa), FadeIn(wl), Vt.animate.set_value(3.0), run_time=2)
        self.play(FadeOut(VGroup(fl, qa, ql, wl)), FadeOut(wa))
        self.remove(wa)
        cyl.drop(self)
        self.internal_energy()
        self.first_law()
        self.example_41()
        self.quiz("A gas expands at a constant pressure of 1.5 × 10⁵ Pa from 2.0 L to 5.0 L, absorbing 800 J of heat. The change in its internal energy is",
                  ["350 J", "450 J", "1250 J", "−350 J"], 0,
                  "Your turn, straight from the five mark questions. A gas expands at one point five times ten to the five pascals, from two litres to five litres, and absorbs eight hundred joules. What is the change in internal energy? Pause and think.",
                  "A, three hundred and fifty joules. The work is P delta V: one point five times ten to the five, times three times ten to the minus three, which is four hundred and fifty joules. Then delta U is Q minus W, eight hundred minus four fifty. If you picked four hundred and fifty, you found the work, not the internal energy.")

    def internal_energy(self):
        box = Rectangle(width=4.4, height=3.4, stroke_color=th.BODY, stroke_width=4).move_to([-3.2, -0.2, 0])
        Tt = ValueTracker(300)
        gas = Gas(lambda: (box.get_left()[0] + 0.05, box.get_right()[0] - 0.05, box.get_bottom()[1] + 0.05, box.get_top()[1] - 0.05), n=30, seed=8,
                  speed=lambda: np.sqrt(Tt.get_value() / 300), color=lambda: heat_color((Tt.get_value() - 250) / 450), radius=0.08)
        eq = M(r"U = \tfrac{f}{2}\,nRT", size=60, color=C_U).move_to([3.0, 2.0, 0])
        sub = T("ideal gas: kinetic energy only", size=24, color=th.MUTED).next_to(eq, DOWN, buff=0.2)
        bar_bg = Rectangle(width=0.8, height=3.2, stroke_color=th.FAINT, stroke_width=2).move_to([3.0, -1.4, 0])
        bar = always_redraw(lambda: Rectangle(width=0.8, height=3.2 * (Tt.get_value() - 150) / 600, stroke_width=0, fill_color=C_U, fill_opacity=0.9)
                            .align_to(bar_bg, DOWN).set_x(3.0))
        bl = M("U", size=34, color=C_U).next_to(bar_bg, LEFT, buff=0.2)
        tr = readout("T =", lambda: Tt.get_value(), "K", size=28, color=C_T).next_to(bar_bg, RIGHT, buff=0.5)
        with self.say("So what is stored inside the gas? Its internal energy, U. It is the total kinetic energy of the random motion of all the molecules, plus the potential energy of the forces between them."):
            self.play(Create(box))
            self.add(gas)
            self.play(FadeIn(gas))
        with self.say("In an ideal gas, the molecules do not attract each other, so there is no potential energy part. U is f by two, n R T, where f is the number of degrees of freedom of each molecule."):
            self.play(Write(eq), FadeIn(sub))
            self.add(bar)
            self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(bl), FadeIn(tr))
        with self.say("Heat the gas, and the molecules move faster, so U goes up. Cool it, and U goes down. The key fact: for an ideal gas, U depends only on temperature."):
            self.play(Tt.animate.set_value(620), run_time=2.5)
            self.play(Tt.animate.set_value(380), run_time=2.0)
        with self.say("Squeeze it or stretch it at the same temperature, and U does not change at all. No change in temperature means no change in internal energy, whatever happens to pressure and volume."):
            self.play(box.animate.stretch(0.6, 0), run_time=1.5)
            self.play(box.animate.stretch(1 / 0.6, 0), run_time=1.5)
            self.play(Indicate(bar, color=WHITE))
        nb = neby_in(self, "cool", corner=DL)
        self.wait(0.4)
        self.play(FadeOut(VGroup(box, eq, sub, bar_bg, bl, tr)), FadeOut(gas), FadeOut(bar))
        self.remove(gas, bar)
        neby_out(self, nb)

    def first_law(self):
        title = T("Energy book-keeping", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        base = -2.2
        q = ValueTracker(0)
        Qbar = always_redraw(lambda: Rectangle(width=1.3, height=max(0.01, 4.0 * q.get_value()), stroke_width=0, fill_color=C_Q, fill_opacity=0.9)
                             .move_to([-5.2, base, 0], aligned_edge=DOWN))
        Ql = T("heat in, Q", size=24, color=C_Q).move_to([-5.2, base - 0.35, 0])
        Ubar = Rectangle(width=1.3, height=0.8, stroke_width=0, fill_color=C_U, fill_opacity=0.9).move_to([-3.0, base, 0], aligned_edge=DOWN)
        Wbar = Rectangle(width=1.3, height=3.2, stroke_width=0, fill_color=C_W, fill_opacity=0.9).move_to([-0.8, base, 0], aligned_edge=DOWN)
        Ul = T("stays inside, ΔU", size=22, color=C_U).move_to([-3.0, base - 0.35, 0])
        Wl = T("leaves as work, W", size=22, color=C_W).move_to([-0.8, base - 0.35, 0])
        with self.say("Energy cannot be created or destroyed. So think of a bank account. Heat supplied to the gas is a deposit."):
            self.play(FadeIn(title))
            self.add(Qbar)
            self.play(q.animate.set_value(1.0), FadeIn(Ql), run_time=1.5)
        with self.say("That energy has only two places to go. Some of it stays in the account, raising the internal energy. The rest is spent, leaving the gas as work done on the surroundings."):
            cp = Qbar.copy()
            self.play(Transform(cp, VGroup(Ubar, Wbar)), run_time=1.5)
            self.play(FadeIn(Ul), FadeIn(Wl))
        law = M(r"Q", r"=", r"\Delta U", r"+", r"W", size=76).move_to([3.9, 0.6, 0])
        law[0].set_color(C_Q)
        law[2].set_color(C_U)
        law[4].set_color(C_W)
        dif = M(r"dQ = dU + dW", size=46).next_to(law, DOWN, buff=0.4)
        with self.say("Written as an equation, this is the first law of thermodynamics. The heat supplied to a system equals the increase in its internal energy, plus the external work done by the system. Q equals delta U plus W, or in differential form, d Q equals d U plus d W."):
            self.sfx("impact", gain=-12)
            self.play(Write(law))
            self.play(Write(dif))
        with self.say("It is simply the law of conservation of energy, applied to heat. And it tells us that internal energy is a state function, even though heat and work on their own are not."):
            self.play(Circumscribe(law, color=th.AMBER))
        self.play(FadeOut(VGroup(title, Ql, Ul, Wl, cp, dif)), FadeOut(Qbar), law.animate.scale(0.6).to_edge(UP, buff=0.8))
        self.remove(Qbar)
        rows = [("Q", "heat absorbed by the gas", "heat given out", C_Q), ("W", "gas expands", "gas is compressed", C_W), ("ΔU", "temperature rises", "temperature falls", C_U)]
        hd = VGroup(T("·", size=24, color=th.BG), T("positive when", size=26, color=th.MINT, weight="SEMIBOLD"), T("negative when", size=26, color=th.CORAL, weight="SEMIBOLD"))
        grid = VGroup(hd)
        for a, b, c, col in rows:
            grid.add(VGroup(T(a, size=34, color=col, weight="BOLD"), T(b, size=26, color=th.BODY), T(c, size=26, color=th.BODY)))
        for r in grid:
            for k, x in enumerate([-4.6, -1.4, 3.0]):
                r[k].move_to([x, 0, 0])
        grid.arrange(DOWN, buff=0.45).move_to([0, -0.4, 0])
        for r in grid:
            for k, x in enumerate([-4.6, -1.4, 3.0]):
                r[k].set_x(x)
        with self.say("The signs decide your marks, so learn them now. Q is positive when heat is absorbed by the gas. W is positive when the gas expands and does work. And delta U is positive when the temperature rises.") as v:
            self.play(FadeIn(grid[0]))
            for r in grid[1:]:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v.dur / 3 - 0.8)
        self.play(FadeOut(grid), FadeOut(law))
        self.tip("NEB writes Q = ΔU + W, with W = work done BY the gas. Some books write ΔU = Q + W with W done ON the gas. Write the NEB form first and stick to it for the whole question.",
                 "Here is the trap. NEB uses Q equals delta U plus W, where W is the work done by the gas. Some books write delta U equals Q plus W, where W is the work done on the gas. Both are correct physics, but mixing them flips the sign of your answer. Write down the NEB form at the start, and stick to it.", state="think")

    def example_41(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A gas at a constant pressure of 2.0 × 10⁵ Pa expands from 1.0 × 10⁻³ m³ to 3.0 × 10⁻³ m³ while absorbing 500 J of heat. Find the work done by the gas and the change in its internal energy.",
                    width=12.2, size=27, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        with self.say("Let us try the first worked example. A gas at a constant pressure of two times ten to the five pascals expands from one litre to three litres, while absorbing five hundred joules of heat. Find the work done and the change in internal energy."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        g = pv_axes(xr=(0, 4, 1), yr=(0, 3, 1), x_len=5.0, y_len=3.2, xl=r"V\ (10^{-3}\,\text{m}^3)", yl=r"P\ (10^{5}\,\text{Pa})", size=26).move_to([-3.4, -1.3, 0])
        ax = g[0]
        v = ValueTracker(1.0)
        rect = always_redraw(lambda: Polygon(ax.c2p(1, 0), ax.c2p(1, 2), ax.c2p(max(1.001, v.get_value()), 2), ax.c2p(max(1.001, v.get_value()), 0),
                                             stroke_width=0, fill_color=C_W, fill_opacity=0.45))
        line = always_redraw(lambda: Line(ax.c2p(1, 2), ax.c2p(max(1.001, v.get_value()), 2), color=th.ACCENT, stroke_width=5))
        wr = readout("W =", lambda: 200 * (v.get_value() - 1), "J", size=28, color=C_W).move_to(ax.c2p(2, 2.75))
        tks = VGroup(*[M(s, size=26).next_to(ax.c2p(x, 0), DOWN, buff=0.12) for s, x in (("1", 1), ("3", 3))], M("2", size=26).next_to(ax.c2p(0, 2), LEFT, buff=0.12))
        steps = VGroup(M(r"W = P\,\Delta V = (2.0\times10^{5})(2.0\times10^{-3})", size=36), M(r"W = 400\ \text{J}", size=40, color=C_W),
                       M(r"\Delta U = Q - W = 500 - 400", size=36), M(r"\Delta U = +100\ \text{J}", size=40, color=C_U)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -1.2, 0])
        with self.say("At constant pressure, the P V graph is a flat line, and the area under it is a rectangle. Watch the work grow as the gas expands from one litre to three."):
            self.play(Create(g), FadeIn(tks))
            self.add(rect, line)
            self.play(FadeIn(wr))
            self.play(v.animate.set_value(3.0), run_time=2.5, rate_func=linear)
        with self.say("The area is P times delta V: two times ten to the five, times two times ten to the minus three. That is four hundred joules of work done by the gas."):
            self.play(Write(steps[0]))
            self.play(Write(steps[1]))
        with self.say("Now the first law. Delta U equals Q minus W, five hundred minus four hundred, which is one hundred joules. The internal energy rises, so the gas also gets warmer."):
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
            self.play(Circumscribe(steps[3], color=C_U))
        nb = neby_in(self, "success")
        self.wait(0.5)
        self.play(FadeOut(VGroup(head, prob, g, tks, steps, wr)), FadeOut(rect), FadeOut(line))
        self.remove(rect, line)
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 4: processes
    def p4(self):
        self.section(3)
        cx, yb = -4.3, -2.6
        s = ValueTracker(0)
        st = {"f": lambda u: (2.0, 4.0)}
        VP = lambda: st["f"](s.get_value())
        h = lambda: 0.62 * VP()[0]
        Tk = lambda: 300 * VP()[0] * VP()[1] / 8.0
        cyl = Cylinder(cx, yb, 2.0, 4.4, h, Tk, Tlo=150, Thi=650, n=26, rod=0.35)
        g = pv_axes(xr=(0, 6, 1), yr=(0, 6.5, 1), x_len=5.4, y_len=4.4).move_to([0.6, -0.3, 0])
        ax = g[0]
        dot = always_redraw(lambda: Dot(ax.c2p(*VP()), radius=0.1, color=WHITE))
        A = ax.c2p(2, 4)
        al = M("A", size=30).next_to(A, UL, buff=0.08)
        tr = readout("T =", Tk, "K", size=28, color=C_T).move_to([-4.3, 2.75, 0])
        with self.say("Now the four special processes that every NEB paper asks about. In each one, something is held fixed, and the first law collapses to a single, simple statement. All four start from the same state, A."):
            self.play(Create(cyl.walls), Create(g))
            self.add(cyl.fill, cyl.gas, cyl.piston, dot)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(dot), FadeIn(al), FadeIn(tr))
        board = VGroup()
        box_x = 5.0

        def card(name, cond, law, col, i):
            c = VGroup(T(name, size=26, color=col, weight="BOLD"), T(cond, size=20, color=th.MUTED), M(law, size=34, color=th.INK)).arrange(DOWN, buff=0.08)
            c.move_to([box_x, 2.3 - i * 1.45, 0])
            return c
        fl = flame([cx, yb - 0.4, 0], 0.8)
        clamps = VGroup(*[Rectangle(width=0.25, height=0.3, fill_color=th.INK, fill_opacity=1, stroke_width=0).move_to([cx + sx * 1.12, yb + 0.62 * 2 + 0.12, 0]) for sx in (-1, 1)])

        def run(f, dur, col, extra_in=(), extra_out=()):
            st["f"] = f
            s.set_value(0)
            trace = always_redraw(lambda: ax.plot_parametric_curve(lambda u: np.array([*f(u)]), t_range=[0, max(0.002, s.get_value())], color=col, stroke_width=5)
                                  if s.get_value() > 0.004 else nothing(A))
            self.add(trace)
            self.play(s.animate.set_value(1), run_time=dur, rate_func=smooth)
            self.remove(trace)
            final = ax.plot_parametric_curve(lambda u: np.array([*f(u)]), t_range=[0, 1], color=col, stroke_width=5)
            self.add(final)
            return final

        curves = VGroup()
        # isochoric
        with self.say("First, isochoric: constant volume. Clamp the piston so it cannot move, and heat the gas. The volume stays fixed, so d V is zero and no work is done. All the heat goes into internal energy. Q equals delta U. On the graph, a vertical line."):
            self.play(FadeIn(clamps), FadeIn(fl, scale=0.4))
            curves.add(run(lambda u: (2.0, 4.0 + 1.8 * u), 3.0, th.CORAL))
            board.add(card("Isochoric", "V constant  ·  W = 0", r"Q = \Delta U", th.CORAL, 0))
            self.play(FadeIn(board[-1], shift=LEFT * 0.3))
        self.play(FadeOut(clamps), s.animate.set_value(0), run_time=0.6)
        # isobaric
        wt = always_redraw(lambda: Rectangle(width=1.0, height=0.55, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([cx, cyl.piston_y() + 0.27, 0]))
        st["f"] = lambda u: (2.0, 4.0)
        with self.say("Second, isobaric: constant pressure. Put a fixed weight on a free piston and heat the gas. It warms and expands, pushing the piston up against the same pressure. A horizontal line. Now the heat does two jobs: Q equals delta U plus P delta V."):
            self.add(wt)
            self.play(FadeIn(wt))
            curves.add(run(lambda u: (2.0 + 3.0 * u, 4.0), 3.0, th.AMBER))
            board.add(card("Isobaric", "P constant", r"Q = \Delta U + P\Delta V", th.AMBER, 1))
            self.play(FadeIn(board[-1], shift=LEFT * 0.3))
        self.play(FadeOut(wt), FadeOut(fl), s.animate.set_value(0), run_time=0.6)
        self.remove(wt)
        # isothermal
        st["f"] = lambda u: (2.0, 4.0)
        bath = Rectangle(width=3.0, height=3.9, stroke_width=0, fill_color="#1E5A8A", fill_opacity=0.45).move_to([cx, yb + 1.7, 0])
        bl = T("large water bath, same T", size=18, color=th.SKY).next_to(bath, DOWN, buff=0.08)
        with self.say("Third, isothermal: constant temperature. Stand the cylinder in a big water bath and let it expand very slowly. Heat flows in just fast enough to keep the temperature fixed. No temperature change means delta U is zero, so Q equals W. The curve is P V equals constant, a rectangular hyperbola."):
            self.play(FadeIn(bath), FadeIn(bl))
            self.mobjects.remove(bath)
            self.mobjects.insert(3, bath)
            curves.add(run(lambda u: (2.0 + 3.0 * u, 8.0 / (2.0 + 3.0 * u)), 4.0, th.SKY))
            board.add(card("Isothermal", "T constant  ·  ΔU = 0", r"Q = W", th.SKY, 2))
            self.play(FadeIn(board[-1], shift=LEFT * 0.3))
        self.play(FadeOut(bath), FadeOut(bl), s.animate.set_value(0), run_time=0.6)
        # adiabatic
        st["f"] = lambda u: (2.0, 4.0)
        ins = VGroup(Rectangle(width=0.3, height=4.4, fill_color=th.FAINT, fill_opacity=1, stroke_width=0).next_to(cyl.walls, LEFT, buff=0),
                     Rectangle(width=0.3, height=4.4, fill_color=th.FAINT, fill_opacity=1, stroke_width=0).next_to(cyl.walls, RIGHT, buff=0),
                     Rectangle(width=2.6, height=0.3, fill_color=th.FAINT, fill_opacity=1, stroke_width=0).next_to(cyl.walls, DOWN, buff=0))
        il = T("insulated: Q = 0", size=20, color=th.BODY).next_to(ins, DOWN, buff=0.08)
        with self.say("Fourth, adiabatic: no heat flow at all. Wrap the cylinder in thick insulation and let it expand. The gas does work, but no heat comes in to pay for it, so the energy comes out of its own internal energy. Delta U equals minus W, and the gas cools. Watch the thermometer fall, and see the curve drop more steeply than the isothermal."):
            self.play(FadeIn(ins), FadeIn(il))
            curves.add(run(lambda u: (2.0 + 3.0 * u, 4.0 * (2.0 / (2.0 + 3.0 * u)) ** 1.4), 4.0, th.MINT))
            board.add(card("Adiabatic", "no heat flow  ·  Q = 0", r"\Delta U = -W", th.MINT, 3))
            self.play(FadeIn(board[-1], shift=LEFT * 0.3))
        with self.say("Four processes, four one line versions of the first law. These are worth memorising exactly as they appear on this board."):
            self.play(Circumscribe(board, color=th.AMBER, buff=0.15), run_time=1.5)
        self.play(FadeOut(VGroup(g, al, tr, curves, board, ins, il)), FadeOut(dot))
        self.remove(dot)
        cyl.drop(self)
        self.cyclic()
        self.free_expansion()

    def cyclic(self):
        g = pv_axes(xr=(0, 6, 1), yr=(0, 5.5, 1), x_len=6.0, y_len=4.4).move_to([-2.4, -0.4, 0])
        ax = g[0]
        pts = [(1.5, 4.0), (4.5, 4.0), (4.5, 1.5), (1.5, 1.5)]
        u = ValueTracker(0)

        def at(x):
            k = int(min(3.999, x * 4))
            a, b = np.array(pts[k]), np.array(pts[(k + 1) % 4])
            return a + (b - a) * (x * 4 - k)
        loop = always_redraw(lambda: VMobject(stroke_color=th.AMBER, stroke_width=5).set_points_as_corners(
            [ax.c2p(*at(x)) for x in np.linspace(0, max(0.002, u.get_value()), 60)]))
        dot = always_redraw(lambda: Dot(ax.c2p(*at(min(u.get_value(), 0.9999))), color=WHITE))
        area = Polygon(*[ax.c2p(*p) for p in pts], stroke_width=0, fill_color=th.AMBER, fill_opacity=0.35)
        eqs = VGroup(M(r"\Delta U = 0", size=46), M(r"Q = W", size=46), M(r"W = \text{area enclosed}", size=40, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.0, 1.0, 0])
        cw = T("clockwise: net work positive", size=24, color=th.MINT).move_to([4.0, -1.4, 0])
        acw = T("anticlockwise: negative", size=24, color=th.CORAL).next_to(cw, DOWN, buff=0.2)
        with self.say("A fifth case matters for every engine: a cyclic process. The gas goes through a series of changes and comes back to exactly where it started."):
            self.play(Create(g))
            self.add(loop, dot)
            self.play(u.animate.set_value(1), run_time=4, rate_func=linear)
        with self.say("It is back in the same state, and internal energy is a state function, so delta U is zero. The first law then says Q equals W. The net work is the area enclosed by the loop: work done by the gas on the top, minus the work done on it along the bottom."):
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]))
            self.play(FadeIn(area), Write(eqs[2]))
        with self.say("Traced clockwise, the net work done by the gas is positive. That is an engine. Traced anticlockwise, it is negative, and that is a refrigerator. We will meet both in the next unit."):
            self.play(FadeIn(cw), FadeIn(acw))
        self.play(FadeOut(VGroup(g, area, eqs, cw, acw)), FadeOut(loop), FadeOut(dot))
        self.remove(loop, dot)

    def free_expansion(self):
        L, R, Mx, B, Tp = -5.0, 1.0, -2.0, -2.3, 1.2
        wall = ValueTracker(Mx)
        gas = Gas(lambda: (L + 0.05, wall.get_value() - 0.05, B + 0.05, Tp - 0.05), n=40, seed=11, radius=0.06)
        box = Rectangle(width=R - L, height=Tp - B, stroke_color=th.BODY, stroke_width=4).move_to([(L + R) / 2, (B + Tp) / 2, 0])
        ins = SurroundingRectangle(box, buff=0.12, stroke_color=th.FAINT, stroke_width=10)
        part = Line([Mx, B, 0], [Mx, Tp, 0], color=th.AMBER, stroke_width=6)
        vac = T("vacuum", size=26, color=th.MUTED).move_to([(Mx + R) / 2, (B + Tp) / 2, 0])
        tr = T("T = 300 K", size=30, color=C_T).move_to([3.9, 0.8, 0])
        title = T("Free expansion", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Here is a strange one, and a favourite multiple choice question. An insulated box has a partition. On one side, an ideal gas. On the other side, nothing at all: a vacuum. What happens to the temperature when we break the partition?"):
            self.play(FadeIn(title), Create(box), Create(ins), Create(part), FadeIn(vac))
            self.add(gas)
            self.play(FadeIn(gas), FadeIn(tr))
        nb = neby_in(self, "surprised", corner=DR)
        with self.say("The gas rushes into the empty space and fills the whole box."):
            self.sfx("whoosh", gain=-10)
            self.play(FadeOut(part), FadeOut(vac), run_time=0.4)
            wall.set_value(R)
            self.wait(3.0)
        eqs = VGroup(M(r"Q = 0\ \ (\text{insulated})", size=36), M(r"W = 0\ \ (\text{nothing to push})", size=36), M(r"\Rightarrow\ \Delta U = 0", size=40, color=C_U),
                     T("ideal gas: T unchanged", size=26, color=C_T)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, -0.9, 0])
        with self.say("The box is insulated, so no heat enters. And the gas pushes against nothing, so it does no work. Q is zero and W is zero, so delta U is zero, and for an ideal gas, the temperature does not change at all. A similar irreversible expansion through a porous plug is called a throttling process."):
            for e in eqs:
                self.play(FadeIn(e, shift=LEFT * 0.2), run_time=0.7)
            self.play(Indicate(tr, color=C_T))
        self.play(FadeOut(VGroup(box, ins, tr, eqs, title)), FadeOut(gas))
        self.remove(gas)
        neby_out(self, nb)
        self.quiz("A gas expands freely into an evacuated, insulated vessel. Its temperature",
                  ["rises", "falls", "stays the same", "first rises, then falls"], 2,
                  "Pause and think. The same idea, as NEB asks it. A gas expands freely into an evacuated insulated vessel. What happens to its temperature?",
                  "C, it stays the same. Q is zero and W is zero, so delta U is zero, and for an ideal gas U depends only on temperature. Many students pick falls, because expanding gases usually cool. That only happens when the gas does work, as in an adiabatic expansion against a piston.")

    # ------------------------------------------------------------------ part 5: heat capacities
    def p5(self):
        self.section(4)
        d1 = M(r"C = \frac{dQ}{n\,dT}", size=56).to_edge(UP, buff=1.0)
        d1l = T("molar heat capacity: heat to warm one mole by one kelvin", size=26, color=th.MUTED).next_to(d1, DOWN, buff=0.2)
        with self.say("The molar heat capacity of a gas is the heat needed to raise the temperature of one mole by one kelvin. But a gas has two of them, because the answer depends on whether you let it expand."):
            self.play(Write(d1), FadeIn(d1l))
        self.play(FadeOut(d1), FadeOut(d1l))
        yb = -2.2
        q = ValueTracker(0)
        hL = lambda: 2.0
        hR = lambda: 2.0 + 0.55 * q.get_value()
        TL = lambda: 300 + 150 * q.get_value()
        TR = lambda: 300 + 107 * q.get_value()
        cl = Cylinder(-4.4, yb, 2.0, 3.8, hL, TL, n=22, rod=0.3, seed=4)
        cr = Cylinder(-0.6, yb, 2.0, 3.8, hR, TR, n=22, rod=0.3, seed=6)
        clamps = VGroup(*[Rectangle(width=0.25, height=0.3, fill_color=th.INK, fill_opacity=1, stroke_width=0).move_to([-4.4 + sx * 1.12, yb + 2.12, 0]) for sx in (-1, 1)])
        fls = VGroup(flame([-4.4, yb - 0.4, 0], 0.7), flame([-0.6, yb - 0.4, 0], 0.7))
        heads = VGroup(T("clamped: V constant", size=22, color=th.CORAL), T("free: P constant", size=22, color=th.AMBER))
        heads[0].move_to([-4.4, 2.6, 0])
        heads[1].move_to([-0.6, 2.6, 0])
        r1 = readout("T =", TL, "K", size=24, color=C_T).move_to([-4.4, 2.1, 0])
        r2 = readout("T =", TR, "K", size=24, color=C_T).move_to([-0.6, 2.1, 0])
        with self.say("Take two identical cylinders, each with one mole of gas. On the left, the piston is clamped. On the right, it is free to move. Give both exactly the same amount of heat."):
            self.play(Create(cl.walls), Create(cr.walls), FadeIn(heads))
            self.add(cl.fill, cl.gas, cl.piston, cr.fill, cr.gas, cr.piston)
            self.play(*[FadeIn(m) for m in (cl.fill, cl.gas, cl.piston, cr.fill, cr.gas, cr.piston, clamps, r1, r2)])
            self.play(FadeIn(fls, scale=0.4))
            self.play(q.animate.set_value(1), run_time=3.5, rate_func=linear)
        with self.say("The clamped gas gets hotter. On the right, part of the heat was spent pushing the piston and the atmosphere back, so less was left to raise the temperature. To get the same temperature rise at constant pressure, you must supply more heat. So C p is always bigger than C v."):
            self.play(Indicate(r1, color=WHITE), Indicate(r2, color=WHITE))
        bars = VGroup()
        bx = 3.6
        Ub = Rectangle(width=0.9, height=2.0, fill_color=C_U, fill_opacity=0.9, stroke_width=0).move_to([bx, -2.2, 0], aligned_edge=DOWN)
        Ub2 = Ub.copy().move_to([bx + 1.6, -2.2, 0], aligned_edge=DOWN)
        Wb = Rectangle(width=0.9, height=0.8, fill_color=C_W, fill_opacity=0.9, stroke_width=0).next_to(Ub2, UP, buff=0)
        bl = VGroup(M(r"C_v\,dT", size=30, color=th.CORAL).next_to(Ub, UP, buff=0.15), M(r"C_p\,dT", size=30, color=th.AMBER).next_to(Wb, UP, buff=0.15),
                    M("dU", size=26, color=th.BG).move_to(Ub), M("dU", size=26, color=th.BG).move_to(Ub2), M(r"P\,dV", size=24, color=th.BG).move_to(Wb))
        with self.say("In energy terms, for the same temperature rise d T: at constant volume the heat is C v d T, and all of it becomes d U. At constant pressure the heat is C p d T, which is the same d U plus the extra work P d V."):
            self.play(GrowFromEdge(Ub, DOWN), GrowFromEdge(Ub2, DOWN))
            self.play(GrowFromEdge(Wb, DOWN))
            self.play(FadeIn(bl))
        self.play(FadeOut(VGroup(heads, clamps, fls, r1, r2, Ub, Ub2, Wb, bl)))
        cl.drop(self)
        cr.drop(self)
        self.mayer()
        self.gamma_table()
        example(self, "For nitrogen γ = 1.40 and the molar mass is 28 g/mol. Calculate Cv, Cp and the two specific heat capacities per kilogram (R = 8.314 J/mol/K).",
                [r"\gamma C_v - C_v = R \;\Rightarrow\; C_v = \frac{R}{\gamma - 1} = \frac{8.314}{0.40} = 20.79\ \text{J mol}^{-1}\text{K}^{-1}",
                 r"C_p = \gamma C_v = 1.40 \times 20.79 = 29.10\ \text{J mol}^{-1}\text{K}^{-1}",
                 r"c_v = \frac{20.79}{0.028} = 742\ \text{J kg}^{-1}\text{K}^{-1},\quad c_p = \frac{29.10}{0.028} = 1039\ \text{J kg}^{-1}\text{K}^{-1}",
                 r"\text{check: } c_p - c_v = 297 = \frac{R}{M} = \frac{8.314}{0.028}\ \checkmark"],
                ["Worked example. For nitrogen, gamma is one point four zero, and the molar mass is twenty eight grams per mole. Find C v, C p, and the two specific heat capacities per kilogram.",
                 "We have two equations: C p minus C v equals R, and C p equals gamma C v. Substitute: gamma C v minus C v equals R, so C v equals R over gamma minus one. Eight point three one four over zero point four: twenty point seven nine joules per mole per kelvin.",
                 "Then C p is gamma times C v: one point four times twenty point seven nine, which is twenty nine point one zero.",
                 "Per kilogram, divide by the molar mass in kilograms, zero point zero two eight. Small c v is seven hundred and forty two, and small c p is one thousand and thirty nine joules per kilogram per kelvin.",
                 "And a quick check: their difference, two hundred and ninety seven, is exactly R over M. It works."], size=34)
        self.tip("Cp − Cv = R is per MOLE. Per kilogram it becomes cp − cv = R/M, with M in kg/mol (0.028 for N₂, not 28).",
                 "Watch your units here. C p minus C v equals R is for one mole. For specific heats per kilogram, the difference is R over M, and M must be in kilograms per mole. For nitrogen that is zero point zero two eight, not twenty eight.", state="wink")

    def mayer(self):
        title = T("Mayer's relation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(
            M(r"\text{constant } V:\quad dU = C_v\,dT", size=40),
            M(r"\text{constant } P:\quad C_p\,dT = dU + P\,dV", size=40),
            M(r"C_p\,dT = C_v\,dT + P\,dV", size=40),
            M(r"PV = RT \;\Rightarrow\; P\,dV = R\,dT", size=40),
            M(r"C_p\,dT = C_v\,dT + R\,dT", size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(title, DOWN, buff=0.35)
        final = M(r"C_p - C_v = R", size=64, color=th.AMBER).next_to(L, DOWN, buff=0.35)
        box = SurroundingRectangle(final, color=th.AMBER, buff=0.2, corner_radius=0.12)
        with self.say("Now we derive the exact difference. This is a five mark question almost every year. Take one mole and heat it through d T. At constant volume no work is done, so d U equals C v d T."):
            self.play(FadeIn(title))
            self.play(Write(L[0]))
        with self.say("Here is the clever step. U depends only on temperature, so this expression for d U is true for any process, not just the constant volume one."):
            self.play(Indicate(L[0], color=C_U))
        with self.say("At constant pressure, the heat is C p d T, and the gas also does work P d V. So C p d T equals d U plus P d V. Replace d U with C v d T."):
            self.play(Write(L[1]))
            self.play(TransformFromCopy(L[1], L[2]))
        with self.say("Now get rid of P d V. For one mole, P V equals R T. At constant pressure, differentiate both sides: P d V equals R d T."):
            self.play(Write(L[3]))
        with self.say("Substitute, cancel d T from every term, and out comes Mayer's relation: C p minus C v equals R."):
            self.play(TransformFromCopy(L[3], L[4]))
            self.sfx("impact", gain=-12)
            self.play(Write(final), Create(box))
        self.play(FadeOut(VGroup(title, L, final, box)))

    def gamma_table(self):
        title = T("Why γ depends on the molecule", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        eq = M(r"C_v = \tfrac{f}{2}R,\quad C_p = C_v + R,\quad \gamma = \frac{C_p}{C_v} = 1 + \frac{2}{f}", size=36).next_to(title, DOWN, buff=0.2)
        data = [("Monatomic", "He, Ar", 3, "1.67"), ("Diatomic", "N₂, O₂, H₂", 5, "1.40"), ("Polyatomic", "CO₂, NH₃", 6, "1.33")]
        cols = VGroup()
        for i, (nm, ex, f, gam) in enumerate(data):
            x = -4.2 + i * 4.2
            if i == 0:
                mol = Dot(radius=0.22, color=th.SKY)
            elif i == 1:
                mol = VGroup(Line(LEFT * 0.35, RIGHT * 0.35, color=th.BODY, stroke_width=5), Dot(LEFT * 0.35, radius=0.2, color=th.SKY), Dot(RIGHT * 0.35, radius=0.2, color=th.SKY))
            else:
                ps = [UP * 0.35, DL * 0.35 + LEFT * 0.1, DR * 0.35 + RIGHT * 0.1]
                mol = VGroup(*[Line(ps[a], ps[b], color=th.BODY, stroke_width=4) for a, b in ((0, 1), (1, 2), (2, 0))], *[Dot(p, radius=0.17, color=th.SKY) for p in ps])
            mol.move_to([x - 1.2, 0.55, 0])
            fl = M(f"f = {f}", size=34, color=th.AMBER).next_to(mol, RIGHT, buff=0.4)
            base = -2.6
            cv = Rectangle(width=0.7, height=0.45 * f / 2, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0).move_to([x - 0.5, base, 0], aligned_edge=DOWN)
            cp = Rectangle(width=0.7, height=0.45 * (f / 2 + 1), fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).move_to([x + 0.4, base, 0], aligned_edge=DOWN)
            lab = VGroup(M("C_v", size=26, color=th.CORAL).next_to(cv, DOWN, buff=0.08), M("C_p", size=26, color=th.AMBER).next_to(cp, DOWN, buff=0.08))
            g = M(rf"\gamma = {gam}", size=36, color=th.INK).move_to([x, -0.3, 0])
            nmt = T(f"{nm}  ({ex})", size=22, color=th.BODY).move_to([x, 1.25, 0])
            cols.add(VGroup(nmt, mol, fl, cv, cp, lab, g))
        with self.say("The ratio of the two heat capacities is called gamma. Since C v is f by two times R, gamma depends only on the degrees of freedom of the molecule."):
            self.play(FadeIn(title), Write(eq))
        says = ["A single atom, like helium or argon, can only move in three directions. Three degrees of freedom, and gamma is one point six seven.",
                "A two atom molecule, like nitrogen or oxygen, can also spin about two axes. Five degrees of freedom, and gamma is one point four zero.",
                "A bent many atom molecule, like carbon dioxide or ammonia in this simple picture, has six, and gamma is one point three three. More ways to store energy means a bigger C v, and a gamma closer to one."]
        for c, sy in zip(cols, says):
            with self.say(sy):
                self.play(FadeIn(c[0]), FadeIn(c[1], scale=0.5), FadeIn(c[2]))
                self.play(GrowFromEdge(c[3], DOWN), GrowFromEdge(c[4], DOWN), FadeIn(c[5]))
                self.play(Write(c[6]))
        self.play(FadeOut(VGroup(title, eq, cols)))

    # ------------------------------------------------------------------ part 6: isothermal and adiabatic
    def p6(self):
        self.section(5)
        g = pv_axes(xr=(0, 6, 1), yr=(0, 6, 1), x_len=5.6, y_len=4.2).move_to([-3.2, -0.5, 0])
        ax = g[0]
        iso = ax.plot(lambda v: 8.0 / v, x_range=[1.4, 5.6], color=th.SKY, stroke_width=5)
        conds = T("thin conducting walls  ·  very slow change", size=24, color=th.SKY).move_to([-3.2, 2.45, 0])
        with self.say("Let us now look closely at the two most important processes. In an isothermal change, the temperature stays fixed, so P V is constant, which is Boyle's law. In practice it needs thin, highly conducting walls, and a very slow change, so that heat can flow in fast enough."):
            self.play(Create(g), Create(iso), FadeIn(conds))
        area = ax.get_area(iso, x_range=[2, 5], color=th.SKY, opacity=0.35)
        ticks = VGroup(M("V_1", size=28).next_to(ax.c2p(2, 0), DOWN, buff=0.12), M("V_2", size=28).next_to(ax.c2p(5, 0), DOWN, buff=0.12))
        L = VGroup(
            M(r"W = \int_{V_1}^{V_2} P\,dV,\quad P = \frac{nRT}{V}", size=38),
            M(r"W = nRT\int_{V_1}^{V_2}\frac{dV}{V} = nRT\big[\ln V\big]_{V_1}^{V_2}", size=38),
            M(r"W = nRT\ln\frac{V_2}{V_1} = 2.303\,nRT\log_{10}\frac{V_2}{V_1}", size=38, color=th.SKY),
            M(r"= nRT\ln\frac{P_1}{P_2},\qquad \Delta U = 0,\ \ Q = W", size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.1, -0.3, 0])
        if L.width > 7.0:
            L.scale_to_fit_width(7.0).move_to([3.1, -0.3, 0])
        with self.say("The work is the area under this hyperbola. Write P as n R T over V. With T constant, n R T comes out of the integral, and the integral of d V over V is the natural log of V."):
            self.play(FadeIn(area), FadeIn(ticks))
            self.play(Write(L[0]))
            self.play(Write(L[1]))
        with self.say("So the isothermal work is n R T ln of V two over V one, or two point three zero three n R T log base ten. Since P one V one equals P two V two, you can also write it with the pressure ratio, P one over P two. And because delta U is zero, the heat absorbed equals this work."):
            self.play(Write(L[2]))
            self.play(Write(L[3]))
        self.play(FadeOut(VGroup(g, iso, conds, area, ticks, L)))
        example(self, "Two moles of an ideal gas at 300 K expand isothermally to three times the original volume. Find the work done by the gas and the heat absorbed (ln 3 = 1.0986).",
                [r"W = nRT\ln\frac{V_2}{V_1} = 2 \times 8.314 \times 300 \times 1.0986",
                 r"W = 4988.4 \times 1.0986 = 5.48\times10^{3}\ \text{J}",
                 r"\Delta U = 0 \;\Rightarrow\; Q = W = 5.48\ \text{kJ absorbed}"],
                ["Worked example. Two moles of an ideal gas at three hundred kelvin expand isothermally to three times their volume. Find the work done and the heat absorbed.",
                 "Use W equals n R T ln of V two over V one. Two times eight point three one four times three hundred, times ln three.",
                 "Two times eight point three one four times three hundred is four thousand nine hundred and eighty eight point four. Times one point zero nine eight six gives five point four eight times ten to the three joules.",
                 "The temperature did not change, so delta U is zero, and the heat absorbed equals the work: five point four eight kilojoules."], size=38)
        self.adiabatic_derive()
        self.adiabatic_work()
        self.slopes()
        self.example_44()
        self.quiz("At the same point on an indicator diagram, the slope of the adiabatic curve compared with the isothermal is",
                  ["equal", "γ times greater", "1/γ times", "zero"], 1,
                  "One last check. At the same point on a P V diagram, how does the slope of the adiabatic compare with the slope of the isothermal? Pause and think.",
                  "B, gamma times greater in magnitude. The isothermal slope is minus P over V, and the adiabatic slope is minus gamma P over V. Since gamma is bigger than one, the adiabatic is always the steeper curve.")

    def adiabatic_derive(self):
        title = T("The adiabatic equation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        why = T("thick insulation, or a change so fast heat cannot flow: diesel compression, sound waves", size=22, color=th.MINT).next_to(title, DOWN, buff=0.2)
        with self.say("In an adiabatic change, no heat enters or leaves. That needs thick insulation, or a change so fast that heat has no time to flow. The compression stroke of a diesel engine, and the squeezes and stretches in a sound wave, are both effectively adiabatic."):
            self.play(FadeIn(title), FadeIn(why))
        L = VGroup(
            M(r"dQ = 0:\quad C_v\,dT + P\,dV = 0", size=38),
            M(r"PV = RT \Rightarrow dT = \frac{P\,dV + V\,dP}{R}", size=38),
            M(r"\frac{C_v}{R}(P\,dV + V\,dP) + P\,dV = 0", size=38),
            M(r"C_v V\,dP + (C_v + R)P\,dV = 0 \;\Rightarrow\; C_v V\,dP + C_p P\,dV = 0", size=38),
            M(r"\frac{dP}{P} + \gamma\frac{dV}{V} = 0", size=42),
            M(r"\ln P + \gamma\ln V = \text{const}", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(why, DOWN, buff=0.35)
        if L.width > 12.4:
            L.scale_to_fit_width(12.4)
        L.set_x(0)
        says = ["For one mole, d U is C v d T and the work is P d V. With no heat, the first law says C v d T plus P d V equals zero.",
                "We want P and V only, so remove d T. Differentiate P V equals R T: P d V plus V d P equals R d T.",
                "Put that in for d T.",
                "Multiply through by R, and use R equals C p minus C v. The C v terms cancel, leaving C v V d P plus C p P d V equals zero.",
                "Divide by C v P V, and write gamma for C p over C v. We get d P over P plus gamma d V over V equals zero.",
                "Integrate: ln P plus gamma ln V is a constant."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.3)
        res = VGroup(M(r"PV^{\gamma} = \text{constant}", size=58, color=th.MINT),
                     M(r"TV^{\gamma-1} = \text{const},\quad P^{1-\gamma}T^{\gamma} = \text{const}", size=38)).arrange(DOWN, buff=0.3)
        with self.say("That is, P V to the power gamma is constant. Use P V equals n R T to swap variables, and you get two companion forms: T V to the gamma minus one is constant, and P to the one minus gamma times T to the gamma is constant."):
            self.play(FadeOut(L), FadeOut(why))
            self.sfx("impact", gain=-12)
            self.play(Write(res[0]))
            self.play(Write(res[1]))
            self.play(Circumscribe(res[0], color=th.MINT))
        self.play(FadeOut(VGroup(title, res)))

    def adiabatic_work(self):
        title = T("Work in an adiabatic change", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(
            M(r"P = KV^{-\gamma}:\quad W = \int_{V_1}^{V_2} KV^{-\gamma}\,dV = K\left[\frac{V^{1-\gamma}}{1-\gamma}\right]_{V_1}^{V_2}", size=38),
            M(r"K = P_1V_1^{\gamma} = P_2V_2^{\gamma} \;\Rightarrow\; KV_2^{1-\gamma} = P_2V_2,\ \ KV_1^{1-\gamma} = P_1V_1", size=38),
            M(r"W = \frac{P_1V_1 - P_2V_2}{\gamma - 1} = \frac{nR(T_1 - T_2)}{\gamma - 1}", size=50, color=th.MINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.5)
        if L.width > 12.4:
            L.scale_to_fit_width(12.4)
        L.set_x(0)
        with self.say("For the work, write P as K V to the minus gamma, and integrate. V to the minus gamma integrates to V to the one minus gamma, over one minus gamma."):
            self.play(FadeIn(title), Write(L[0]))
        with self.say("Now use K equals P one V one to the gamma, which also equals P two V two to the gamma. Then K V two to the one minus gamma is just P two V two, and the same for state one."):
            self.play(Write(L[1]))
        with self.say("So the adiabatic work is P one V one minus P two V two, over gamma minus one, or n R times T one minus T two, over gamma minus one. If the gas expands, T two is lower than T one, the work is positive, and the gas has cooled."):
            self.play(Write(L[2]))
            self.play(Circumscribe(L[2], color=th.MINT))
        self.play(FadeOut(VGroup(title, L)))

    def slopes(self):
        g = pv_axes(xr=(0, 6, 1), yr=(0, 6, 1), x_len=6.2, y_len=4.6).move_to([-2.6, -0.4, 0])
        ax = g[0]
        gam = ValueTracker(1.4)
        iso = ax.plot(lambda v: 8 / v, x_range=[1.4, 5.8], color=th.SKY, stroke_width=5)
        adi = always_redraw(lambda: ax.plot(lambda v: 4 * (2 / v) ** gam.get_value(), x_range=[max(1.25, 2 * (4 / 6) ** (1 / gam.get_value())), 5.8], color=th.MINT, stroke_width=5))
        A = ax.c2p(2, 4)
        dA = VGroup(Dot(A, color=WHITE), M("A", size=30).next_to(A, UR, buff=0.06))
        lab = VGroup(T("isothermal", size=24, color=th.SKY).next_to(ax.c2p(5.6, 8 / 5.6), UP, buff=0.12),
                     T("adiabatic", size=24, color=th.MINT).next_to(ax.c2p(5.6, 4 * (2 / 5.6) ** 1.4), DOWN, buff=0.12))
        s1 = M(r"\text{isothermal: } \frac{dP}{dV} = -\frac{P}{V}", size=38, color=th.SKY)
        s2 = M(r"\text{adiabatic: } \frac{dP}{dV} = -\gamma\frac{P}{V}", size=38, color=th.MINT)
        ss = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.7, 1.6, 0])
        gr = readout("γ =", lambda: gam.get_value(), "", decimals=2, size=30, color=th.MINT).move_to([3.7, -0.1, 0])
        with self.say("Draw both curves through the same point A. Differentiate P V equals constant, and the isothermal slope is minus P over V. Differentiate P V to the gamma, and the adiabatic slope is minus gamma P over V."):
            self.play(Create(g), Create(iso), FadeIn(dA))
            self.add(adi)
            self.play(Create(adi), FadeIn(lab))
            self.play(Write(s1))
            self.play(Write(s2))
        with self.say("Gamma is always bigger than one, so the adiabatic is gamma times steeper at every point. Turn gamma down towards one, and the two curves merge. Turn it up to one point six seven, for a monatomic gas, and the adiabatic falls even more steeply."):
            self.play(FadeIn(gr), FadeOut(lab[1]))
            self.play(gam.animate.set_value(1.02), run_time=2)
            self.play(gam.animate.set_value(1.67), run_time=2.5)
            self.play(gam.animate.set_value(1.4), run_time=1.2)
        area_a = always_redraw(lambda: ax.get_area(ax.plot(lambda v: 4 * (2 / v) ** gam.get_value(), x_range=[2, 5]), x_range=[2, 5], color=th.MINT, opacity=0.45))
        area_i = ax.get_area(iso, x_range=[2, 5], bounded_graph=ax.plot(lambda v: 4 * (2 / v) ** 1.4, x_range=[2, 5]), color=th.SKY, opacity=0.35)
        note = para("Expanding to the same volume, the adiabatic ends lower and does less work: it pays from its own internal energy, so it cools.", width=4.5, size=24, color=th.INK).move_to([4.2, -1.9, 0])
        with self.say("So expanding from A to the same final volume, the adiabatic path ends at a lower pressure, encloses less area, and does less work. With no heat coming in, it pays for every joule out of its own internal energy, and that is why an adiabatic expansion cools the gas."):
            self.add(area_a)
            self.play(FadeIn(area_a), FadeIn(area_i))
            self.play(FadeIn(note, shift=UP * 0.2))
        self.play(FadeOut(VGroup(g, iso, dA, lab[0], ss, gr, area_i, note)), FadeOut(adi), FadeOut(area_a))
        self.remove(adi, area_a)

    def example_44(self):
        head = T("Back to the diesel engine", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cyl, s, Tk, h, yb = self.diesel(cx=-4.6)
        temp = readout("T =", Tk, "K", size=28, color=th.INK).move_to([-4.6, -3.05, 0])
        with self.say("Now we can solve the mystery from the start of the lesson. One mole of air, with gamma equal to one point four, at twenty seven degrees Celsius, is compressed adiabatically to one eighth of its volume. Find the final temperature, and the work done on the gas."):
            self.play(FadeIn(head), Create(cyl.walls))
            self.add(cyl.fill, cyl.gas, cyl.piston)
            self.play(FadeIn(cyl.fill), FadeIn(cyl.gas), FadeIn(cyl.piston), FadeIn(temp))
        steps = VGroup(
            M(r"T_1 = 300\ \text{K},\quad \frac{V_1}{V_2} = 8", size=38),
            M(r"T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma - 1} = 300 \times 8^{0.4}", size=38),
            M(r"T_2 = 300 \times 2.297 = 689\ \text{K}\ \ (416\,^{\circ}\text{C})", size=38, color=th.CORAL),
            M(r"W = \frac{nR(T_1 - T_2)}{\gamma - 1} = \frac{8.314\,(300 - 689)}{0.40}", size=38),
            M(r"W = -8.09\times10^{3}\ \text{J}\ \Rightarrow\ \Delta U = +8.09\ \text{kJ}", size=38, color=th.MINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, -0.75, 0])
        if steps.width > 8.0:
            steps.scale_to_fit_width(8.0).move_to([2.2, -0.75, 0])
        with self.say("Change to kelvin first: twenty seven degrees is three hundred kelvin. The volume ratio V one over V two is eight."):
            self.play(Write(steps[0]))
        with self.say("Use T V to the gamma minus one is constant. So T two equals T one times V one over V two, to the power zero point four."):
            self.play(Write(steps[1]))
        with self.say("Eight to the zero point four is two point two nine seven, so T two is six hundred and eighty nine kelvin. That is four hundred and sixteen degrees Celsius. Watch it happen."):
            self.play(Write(steps[2]))
            self.sfx("whoosh", gain=-8)
            self.play(s.animate.set_value(1.0), run_time=2.4, rate_func=rate_functions.ease_in_cubic)
            self.sfx("thud", gain=-8)
        with self.say("The work done by the gas is n R times T one minus T two, over gamma minus one: eight point three one four times minus three hundred and eighty nine, over zero point four. That is minus eight point zero nine kilojoules."):
            self.play(Write(steps[3]))
            self.play(Write(steps[4]))
        with self.say("The minus sign means eight point zero nine kilojoules of work is done on the gas. No heat can leave, so all of that work stays inside as internal energy, and the temperature soars. That is why diesel fuel ignites with no spark."):
            self.play(Circumscribe(steps[4], color=th.MINT))
            nb = neby_in(self, "success", corner=UR)
        self.play(FadeOut(VGroup(head, temp, steps)))
        cyl.drop(self)
        neby_out(self, nb)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Open, closed, isolated systems. P, V, T and U are state functions; Q and W are path functions.",
            M(r"W = \int P\,dV = \text{area under the } P\text{–}V \text{ curve}", size=34),
            M(r"Q = \Delta U + W,\quad U = \tfrac{f}{2}nRT \text{ depends only on } T", size=34),
            M(r"\text{isochoric } Q = \Delta U;\ \text{isobaric } Q = \Delta U + P\Delta V;\ \text{isothermal } Q = W;\ \text{adiabatic } \Delta U = -W", size=30),
            M(r"\text{cyclic: } \Delta U = 0,\ Q = W = \text{loop area};\ \ \text{free expansion: } \Delta T = 0", size=32),
            M(r"C_p - C_v = R,\quad C_v = \frac{R}{\gamma - 1},\quad \gamma = 1.67,\ 1.40,\ 1.33", size=34),
            M(r"W_{\text{iso}} = nRT\ln\frac{V_2}{V_1};\quad PV^{\gamma} = \text{const},\ W_{\text{adi}} = \frac{nR(T_1 - T_2)}{\gamma - 1}", size=32),
        ], "Let us recap. A system is separated from its surroundings by a boundary. Work done by a gas is the area under its P V curve. The first law says Q equals delta U plus W, and for an ideal gas U depends only on temperature. Each of the four processes turns the first law into one simple line. In a cycle, delta U is zero and the work is the loop area. C p minus C v equals R. Isothermal work is n R T ln V two over V one, and in an adiabatic change P V to the gamma stays constant.")
        self.outro("That is the first law of thermodynamics: energy is never lost, only moved around. But it does not tell us which way energy likes to flow, or why no engine can be perfect. That is the second law, and it is our next lesson. See you there, on NEBians.")
