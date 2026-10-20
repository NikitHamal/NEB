import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import (Stream, clock, curve, example, flame, galvo, heat_color, neby_in, neby_out, needle_meter,  # noqa: E402
                   readout, wire)

CU, FE = "#E08A4A", "#9AA3C7"
C_E, C_H, C_C = th.AMBER, th.CORAL, th.SKY


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 15
    TITLE = "Thermoelectric Effects"
    SUBTITLE = "Where heat and electricity meet"
    SECTIONS = ["Seebeck effect", "Thermoelectric series", "Thermocouple thermometers", "Peltier effect",
                "Neutral and inversion temperatures", "Thermopile"]
    NEXT = "Unit 16 · Magnetic Field"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ the copper–iron thermocouple loop
    def couple(self, dT, x0=-3.0, x1=3.0, yt=1.5, yb=-1.6, gx=0.0, scale=1.0):
        J1, J2 = np.array([x0, 0, 0]), np.array([x1, 0, 0])
        cu = VGroup(wire(J1, [x0, yt, 0], [x1, yt, 0], J2, color=CU, stroke=7))
        fe = VGroup(wire(J1, [x0, yb, 0], [gx - 0.4, yb, 0], color=FE, stroke=7), wire([gx + 0.4, yb, 0], [x1, yb, 0], J2, color=FE, stroke=7))
        g = galvo([gx, yb, 0], r=0.38)
        hot = always_redraw(lambda: VGroup(Circle(radius=0.32, stroke_width=0, fill_color=heat_color(dT() / 300), fill_opacity=0.9).move_to(J1),
                                           flame(J1 + DOWN * 0.75, 0.9 * min(1.2, 0.3 + dT() / 300)) if dT() > 5 else VGroup()))
        ice = VGroup(RoundedRectangle(corner_radius=0.08, width=0.9, height=0.7, fill_color="#bfe6ff", fill_opacity=0.6, stroke_color=WHITE, stroke_width=2).move_to(J2), Dot(J2, radius=0.12, color=C_C))
        labs = VGroup(T("copper", size=24, color=CU).next_to([0, yt, 0], UP, buff=0.12), T("iron", size=24, color=FE).next_to([(x0 + gx) / 2, yb, 0], DOWN, buff=0.12),
                      T("hot junction", size=22, color=C_H).next_to(J1, LEFT, buff=0.45), T("cold junction (ice)", size=22, color=C_C).next_to(J2, RIGHT, buff=0.55))
        return VGroup(cu, fe, g), hot, ice, labs, (J1, J2, yt, yb)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        stars = VGroup(*[Dot([x, y, 0], radius=0.02, color=WHITE).set_opacity(o) for x, y, o in np.random.default_rng(2).uniform([-6.8, -3.4, 0.2], [6.8, 3.4, 0.9], (90, 3))])
        dish = Arc(radius=1.0, start_angle=PI / 2 + 0.9, angle=PI - 1.8, color=WHITE, stroke_width=5).rotate(PI / 2).move_to([-0.6, 0.4, 0])
        body = VGroup(Rectangle(width=1.0, height=0.7, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([0.4, 0.4, 0]),
                      Line([0.9, 0.4, 0], [2.6, 0.4, 0], color=th.MUTED, stroke_width=4), Rectangle(width=0.5, height=0.36, fill_color=th.CORAL, fill_opacity=1, stroke_width=0).move_to([2.8, 0.4, 0]),
                      Line([0.4, 0.75, 0], [0.4, 2.2, 0], color=th.MUTED, stroke_width=2))
        probe = VGroup(dish, body)
        glow = Circle(radius=0.45, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.35).move_to([2.8, 0.4, 0])
        lab = T("Voyager 1, more than 24 billion km from the Sun", size=26, color=th.MUTED).to_edge(UP, buff=0.6)
        rtg = T("power source: a warm lump of plutonium, and no moving parts", size=24, color=th.CORAL).to_edge(DOWN, buff=0.7)
        with self.say("Voyager one, launched in nineteen seventy seven, is now more than twenty four billion kilometres away, far beyond the reach of useful sunlight. Yet it is still talking to us. Where does its electricity come from?"):
            self.play(FadeIn(stars), FadeIn(lab))
            self.play(FadeIn(probe, shift=LEFT * 0.5))
        with self.say("From a warm lump of radioactive plutonium. No turbine, no engine, no moving parts at all. The heat flows out through rows of junctions between two different materials, and wherever there is a temperature difference across such a junction, a voltage appears."):
            self.play(FadeIn(glow), FadeIn(rtg))
            self.play(glow.animate.scale(1.4).set_opacity(0.2), rate_func=there_and_back, run_time=2)
        self.play(FadeOut(VGroup(stars, probe, glow, lab, rtg)))
        dT = ValueTracker(0)
        loop, hot, ice, labs, _ = self.couple(lambda: dT.get_value())
        dial, needle = needle_meter([4.6, 2.2, 0], lambda: dT.get_value() / 220, r=0.8, label="μV")
        with self.say("You can do it on a desk. Twist a copper wire and an iron wire together at both ends, put a galvanometer in the loop, and dip one junction in ice. Now heat the other junction with a candle."):
            self.play(Create(loop), FadeIn(ice), FadeIn(labs))
            self.add(hot, needle)
            self.play(FadeIn(hot), FadeIn(dial), FadeIn(needle))
            self.play(dT.animate.set_value(180), run_time=3)
        nb = neby_in(self, "surprised", corner=DL)
        q = T("No battery. Just a flame. Where does the current come from?", size=28, color=th.AMBER, weight="BOLD").to_edge(DOWN, buff=0.35)
        with self.say("The needle moves. There is no battery anywhere in this circuit, yet a current flows. Heat has been turned directly into electricity."):
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(loop, ice, labs, dial, q)), FadeOut(hot), FadeOut(needle))
        self.remove(hot, needle)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 15: Thermoelectric Effects. At the junction of two different metals, heat and electricity are directly linked. A temperature difference makes a voltage, and a current makes a temperature difference. These effects run every industrial thermocouple, every thermopile, and the little solid state coolers in portable fridges."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. The Seebeck effect, the thermoelectric series, thermocouple thermometers, the Peltier effect, how the e m f varies with temperature, with its neutral and inversion temperatures, and finally the thermopile.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        dT = ValueTracker(0)
        loop, hot, ice, labs, (J1, J2, yt, yb) = self.couple(lambda: dT.get_value(), x0=-4.4, x1=1.6, gx=-1.4)
        dial, needle = needle_meter([4.6, 2.2, 0], lambda: dT.get_value() / 220, r=0.8, label="μV")
        ro = readout("ΔT =", lambda: dT.get_value(), "°C", decimals=0, size=26, color=C_H).move_to([4.6, 0.9, 0])
        st = always_redraw(lambda: VGroup(*[Dot(VMobject().set_points_as_corners([J2, [1.6, yb, 0], [-4.4, yb, 0], J1, [-4.4, yt, 0], [1.6, yt, 0], J2]).point_from_proportion(((k / 10) + 0.05 * dT.get_value() / 60 * self.renderer.time) % 1), radius=0.06, color=C_E)
                                           for k in range(10)]) if dT.get_value() > 3 else VGroup())
        d = self.callout("key", "Seebeck effect (1821): two different metals in a closed loop, junctions at different temperatures: an e.m.f. appears and a current flows. The pair is a thermocouple.", width=5.4, size=22)
        d.move_to([4.2, -1.2, 0])
        with self.say("This is the Seebeck effect, discovered by Thomas Seebeck in eighteen twenty one. Two wires of different metals form a closed circuit. Keep the two junctions at different temperatures, and an e m f appears, and a current flows. The e m f is the thermo e m f, and the pair of metals is a thermocouple."):
            self.play(Create(loop), FadeIn(ice), FadeIn(labs[:2]))
            self.add(hot, needle, st)
            self.play(FadeIn(hot), FadeIn(dial), FadeIn(needle), FadeIn(ro))
            self.play(dT.animate.set_value(120), run_time=3)
            self.play(FadeIn(d))
        self.play(FadeOut(d))
        dep = VGroup(T("depends on:", size=26, color=th.INK, weight="BOLD"), T("✓ the two metals", size=24, color=C_E), T("✓ the temperature DIFFERENCE", size=24, color=C_E),
                     T("does not depend on:", size=26, color=th.INK, weight="BOLD"), T("✗ thickness, length, shape of the wires", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.4, -1.1, 0])
        with self.say("The e m f is small, tens of microvolts per degree. It depends on only two things: which two metals you use, and the temperature difference between the junctions. Make the difference bigger, and the e m f grows. Make it zero, and the e m f vanishes. The thickness, length and shape of the wires make no difference at all."):
            self.play(FadeIn(dep))
            self.play(dT.animate.set_value(200), run_time=2)
            self.play(dT.animate.set_value(0), run_time=2)
            self.play(dT.animate.set_value(100), run_time=1.5)
        self.play(FadeOut(VGroup(loop, ice, labs[:2], dial, dep, ro)), FadeOut(hot), FadeOut(needle), FadeOut(st))
        self.remove(hot, needle, st)
        self.why_seebeck()

    def why_seebeck(self):
        title = T("Why does it happen?", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        A = Rectangle(width=4.0, height=2.6, stroke_color=CU, stroke_width=4, fill_color=CU, fill_opacity=0.12).move_to([-2.0, 0.2, 0])
        B = Rectangle(width=4.0, height=2.6, stroke_color=FE, stroke_width=4, fill_color=FE, fill_opacity=0.12).move_to([2.0, 0.2, 0])
        rng = np.random.default_rng(1)
        ea = VGroup(*[Dot([x, y, 0], radius=0.06, color=th.SKY) for x, y in rng.uniform([-3.9, -1.0], [-0.1, 1.4], (46, 2))])
        eb = VGroup(*[Dot([x, y, 0], radius=0.06, color=th.SKY) for x, y in rng.uniform([0.1, -1.0], [3.9, 1.4], (20, 2))])
        la = VGroup(T("metal A: more free electrons", size=22, color=CU).next_to(A, DOWN, buff=0.15), T("metal B: fewer", size=22, color=FE).next_to(B, DOWN, buff=0.15))
        movers = ea[:8]
        with self.say("The two metals have different concentrations of free electrons. Where they touch, electrons diffuse across, from the crowded metal into the less crowded one."):
            self.play(FadeIn(title), FadeIn(A), FadeIn(B), FadeIn(ea), FadeIn(eb), FadeIn(la))
            self.play(*[m.animate.move_to([rng.uniform(0.2, 1.0), rng.uniform(-0.9, 1.3), 0]) for m in movers], run_time=2)
        pm = VGroup(*[T("+", size=30, color=th.CORAL, weight="BOLD").move_to([-0.25, y, 0]) for y in (-0.6, 0.2, 1.0)], *[T("−", size=34, color=th.SKY, weight="BOLD").move_to([0.25, y, 0]) for y in (-0.6, 0.2, 1.0)])
        cp = para("A contact potential difference builds up and stops the flow. Its size depends on temperature.", width=10, size=26, color=C_E).to_edge(DOWN, buff=0.6)
        with self.say("That leaves one side positive and the other negative. A contact potential difference builds up, just big enough to stop any more electrons crossing. And the size of that contact p d depends on the temperature of the junction."):
            self.play(FadeIn(pm))
            self.play(FadeIn(cp))
        fin = para("Both junctions at the same temperature: the two contact p.d.s cancel round the loop. Different temperatures: they no longer cancel, and the difference is the thermo-e.m.f.", width=11, size=26, color=th.INK).to_edge(DOWN, buff=0.6)
        with self.say("A thermocouple has two junctions, and their contact p ds point opposite ways round the loop. At the same temperature they cancel exactly. At different temperatures they no longer cancel, and the difference is the thermo e m f."):
            self.play(FadeOut(cp), FadeIn(fin))
        self.play(FadeOut(VGroup(title, A, B, ea, eb, la, pm, fin)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        series = ["Sb", "Fe", "Cd", "Zn", "Ag", "Au", "Cr", "Sn", "Pb", "Hg", "Mn", "Cu", "Pt", "Co", "Ni", "Bi"]
        chips = VGroup()
        for i, s in enumerate(series):
            box = RoundedRectangle(corner_radius=0.1, width=0.72, height=0.62, stroke_color=th.PANEL_EDGE, fill_color=th.PANEL, fill_opacity=1)
            chips.add(VGroup(box, T(s, size=24, color=th.INK, weight="BOLD").move_to(box)))
        chips.arrange(RIGHT, buff=0.08).move_to([0, 1.9, 0])
        title = T("The Seebeck (thermoelectric) series", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("Which way does the current flow? Metals can be arranged in a list called the Seebeck, or thermoelectric, series: antimony, iron, cadmium, zinc, silver, gold, chromium, tin, lead, mercury, manganese, copper, platinum, cobalt, nickel, and bismuth.") as v_:
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.12), run_time=min(6, v_.dur * 0.9))
        rule = VGroup(T("Direction:", size=26, color=C_E, weight="BOLD"), para("through the COLD junction, current flows from the metal EARLIER in the series to the metal LATER in it.", width=11, size=26, color=th.BODY),
                      T("Size:", size=26, color=C_E, weight="BOLD"), para("the further apart the two metals, the bigger the e.m.f. Sb–Bi, at the two ends, gives the most.", width=11, size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -0.3, 0])
        with self.say("Two rules follow. Direction: through the cold junction, the current flows from the metal that comes earlier in the series to the one that comes later. Through the hot junction it goes the other way. And size: the further apart the two metals are in the list, the bigger the e m f. Antimony and bismuth sit at the two ends, so an antimony bismuth couple gives the biggest e m f of all."):
            self.play(FadeIn(rule[:2]))
            self.play(Indicate(chips[1], color=th.AMBER), Indicate(chips[11], color=th.AMBER))
            self.play(FadeIn(rule[2:]))
            self.play(chips[0][0].animate.set_stroke(th.CORAL, 5), chips[15][0].animate.set_stroke(th.CORAL, 5))
        self.play(FadeOut(rule))
        dT = ValueTracker(150)
        loop, hot, ice, labs, (J1, J2, yt, yb) = self.couple(lambda: dT.get_value(), x0=-3.6, x1=2.4, yt=0.9, yb=-2.0, gx=-0.6)
        path_cold = Stream([[2.4, -2.0, 0], J2, [2.4, 0.9, 0]], n=4, speed=0.8, color=C_E)
        path_all = Stream([J2, [2.4, 0.9, 0], [-3.6, 0.9, 0], J1, [-3.6, -2.0, 0], [2.4, -2.0, 0], J2], n=14, speed=1.0, color=C_E)
        txt = VGroup(T("Fe comes before Cu:", size=24, color=th.BODY), T("cold junction: Fe → Cu", size=24, color=C_C), T("hot junction: Cu → Fe", size=24, color=C_H)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.0, -0.5, 0])
        mn = VGroup(T("“A-B-C”: Antimony to Bismuth through the Cold junction", size=22, color=th.AMBER), T("“hot coffee”: COpper to FE through the HOT junction", size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.say("Try it on copper and iron. Iron comes before copper. So through the cold junction, the current flows from iron to copper, and through the hot junction, from copper to iron. Round the loop it goes."):
            self.play(Create(loop), FadeIn(ice), FadeIn(labs[:2]))
            self.add(hot, path_all)
            self.play(FadeIn(hot), FadeIn(txt))
        with self.say("Two memory aids. A B C: antimony to bismuth through the cold junction. And hot coffee: C O for copper, F E for iron, copper to iron through the hot junction."):
            self.play(FadeIn(mn))
        self.play(FadeOut(VGroup(title, chips, loop, ice, labs[:2], txt, mn)), FadeOut(hot), FadeOut(path_all))
        self.remove(hot, path_all)
        self.quiz("Antimony and bismuth are chosen for a thermopile because",
                  ["they are cheap", "high melting points", "opposite ends of the series", "they are black"], 2,
                  "Pause and think. Why are antimony and bismuth chosen for thermopiles?",
                  "C, because they lie at opposite ends of the thermoelectric series, and the further apart the metals, the bigger the e m f.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        title = T("The thermocouple thermometer", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        kiln = VGroup(RoundedRectangle(corner_radius=0.3, width=4.2, height=3.0, fill_color="#5a2a1a", fill_opacity=1, stroke_color=th.CORAL, stroke_width=3).move_to([-3.6, -0.3, 0]),
                      *[Rectangle(width=0.7, height=0.3, fill_color="#b0502a", fill_opacity=1, stroke_width=1, stroke_color=th.BG).move_to([-4.9 + 0.75 * (k % 4), -1.2 + 0.32 * (k // 4), 0]) for k in range(12)])
        fire = VGroup(*[flame([-4.6 + 0.9 * k, -1.7, 0], 0.7) for k in range(3)])
        probe = VGroup(Line([-2.6, 0.3, 0], [1.4, 0.3, 0], color=CU, stroke_width=6), Line([-2.6, 0.1, 0], [1.4, 0.1, 0], color=FE, stroke_width=6), Dot([-2.6, 0.2, 0], radius=0.12, color=th.CORAL))
        icej = VGroup(RoundedRectangle(corner_radius=0.08, width=1.0, height=0.8, fill_color="#bfe6ff", fill_opacity=0.6, stroke_color=WHITE).move_to([1.8, 0.2, 0]), T("ice, 0 °C", size=20, color=C_C).move_to([1.8, -0.45, 0]))
        meter = VGroup(RoundedRectangle(corner_radius=0.1, width=2.0, height=1.2, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.BODY).move_to([4.6, 0.2, 0]))
        val = ValueTracker(20)
        rd = always_redraw(lambda: T(f"{int(val.get_value())} °C", size=30, color=th.AMBER, weight="BOLD").move_to([4.6, 0.2, 0]))
        leads = wire([2.3, 0.2, 0], [3.6, 0.2, 0], color=th.BODY)
        lab = T("a brick kiln in Hetauda", size=22, color=th.MUTED).next_to(kiln, DOWN, buff=0.15)
        with self.say("To use a thermocouple as a thermometer, keep the cold junction in melting ice, a fixed zero degree reference, and put the hot junction where you want the temperature. The meter reading is turned into a temperature with a calibration curve. This is how the kilns of a brick factory, or a cement plant in Hetauda, are monitored, from a control room far away."):
            self.play(FadeIn(title), FadeIn(kiln), FadeIn(fire), FadeIn(lab))
            self.play(Create(probe), FadeIn(icej), Create(leads), FadeIn(meter))
            self.add(rd)
            self.play(val.animate.set_value(950), run_time=3)
        self.play(FadeOut(VGroup(kiln, fire, probe, icej, meter, leads, lab)), FadeOut(rd))
        self.remove(rd)
        rows = [("copper–constantan", "−200 to 400 °C"), ("iron–constantan", "−200 to 750 °C"), ("chromel–alumel", "−200 to 1100 °C"), ("platinum–platinum/rhodium", "0 to 1600 °C")]
        tbl = VGroup(*[VGroup(T(a, size=24, color=th.INK), T(b, size=24, color=th.AMBER)) for a, b in rows])
        for k, r in enumerate(tbl):
            r[0].move_to([-2.8, 1.6 - k * 0.6, 0], aligned_edge=LEFT).set_x(-5.6, direction=LEFT)
            r[1].move_to([-1.5, 1.6 - k * 0.6, 0], aligned_edge=LEFT)
        adv = VGroup(T("Advantages", size=26, color=C_E, weight="BOLD"), T("• very wide range", size=22), T("• tiny junction: fast response, measures at a point", size=22),
                     T("• readable far away", size=22), T("Disadvantages", size=26, color=th.CORAL, weight="BOLD"), T("• tiny e.m.f.: needs a sensitive meter", size=22),
                     T("• non-linear calibration; needs a reference junction", size=22)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        adv.scale_to_fit_width(min(adv.width, 5.6)).move_to([3.7, 0.2, 0])
        with self.say("Different pairs cover different ranges: copper constantan up to four hundred degrees, iron constantan to seven fifty, chromel alumel to eleven hundred, and platinum with platinum rhodium all the way to sixteen hundred. The advantages: a huge range, a tiny junction that responds in a fraction of a second and measures the temperature at a point, and readings from hundreds of metres away. The disadvantages: the e m f is tiny, the calibration is not linear, and you must keep a reference junction.") as v_:
            self.play(FadeIn(title))
            for r in tbl:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(a) for a in adv], lag_ratio=0.25), run_time=3)
        self.play(FadeOut(VGroup(title, tbl, adv)))
        cau = self.callout("careful", "The e.m.f. depends on the temperature DIFFERENCE. If the reference junction drifts up to the hot temperature, the reading falls to zero even though the furnace is white hot. Check the reference junction first.", width=11, size=26)
        with self.say("A warning. The e m f depends on the difference between the junctions. If the reference junction is allowed to warm up to the same temperature as the hot one, the reading drops to zero, even though the furnace is white hot. Always check the reference junction first."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        self.quiz("The Seebeck effect converts",
                  ["electrical energy into heat", "heat into electrical energy", "chemical energy into heat", "magnetic energy into heat"], 1,
                  "Pause and think. What energy change happens in the Seebeck effect?",
                  "B, heat into electrical energy: a temperature difference makes an e m f. The reverse, electricity moving heat about, is the Peltier effect, coming next.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        I = ValueTracker(1.0)
        x0, x1, yt, yb = -3.6, 2.4, 1.2, -1.6
        J1, J2 = np.array([x0, 0, 0]), np.array([x1, 0, 0])
        loop = VGroup(wire(J1, [x0, yt, 0], [x1, yt, 0], J2, color=CU, stroke=7), wire(J1, [x0, yb, 0], [-1.0, yb, 0], color=FE, stroke=7),
                      wire([-0.2, yb, 0], [x1, yb, 0], J2, color=FE, stroke=7))
        bat = always_redraw(lambda: VGroup(Line([-1.0, yb, 0], [-0.75, yb, 0], color=th.BODY, stroke_width=4), Line([-0.45, yb, 0], [-0.2, yb, 0], color=th.BODY, stroke_width=4),
                                           Line([-0.75 if I.get_value() > 0 else -0.45, yb - 0.35, 0], [-0.75 if I.get_value() > 0 else -0.45, yb + 0.35, 0], color=th.BODY, stroke_width=4),
                                           Line([-0.45 if I.get_value() > 0 else -0.75, yb - 0.18, 0], [-0.45 if I.get_value() > 0 else -0.75, yb + 0.18, 0], color=th.BODY, stroke_width=7)))
        pts = [J1, [x0, yt, 0], [x1, yt, 0], J2, [x1, yb, 0], [x0, yb, 0], J1]
        pv = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts])
        tclk = clock(self, 1.0)
        dots = always_redraw(lambda: VGroup(*[Dot(pv.point_from_proportion((k / 14 + 0.12 * I.get_value() * tclk.get_value()) % 1), radius=0.06, color=C_E) for k in range(14)]))
        j1 = always_redraw(lambda: Circle(radius=0.45, stroke_width=0, fill_color=th.SKY if I.get_value() > 0 else th.CORAL, fill_opacity=0.55).move_to(J1))
        j2 = always_redraw(lambda: Circle(radius=0.45, stroke_width=0, fill_color=th.CORAL if I.get_value() > 0 else th.SKY, fill_opacity=0.55).move_to(J2))
        l1 = always_redraw(lambda: T("cools" if I.get_value() > 0 else "warms", size=28, color=th.SKY if I.get_value() > 0 else th.CORAL).next_to(J1, LEFT, buff=0.55))
        l2 = always_redraw(lambda: T("warms" if I.get_value() > 0 else "cools", size=28, color=th.CORAL if I.get_value() > 0 else th.SKY).next_to(J2, RIGHT, buff=0.55))
        mt = VGroup(T("copper", size=22, color=CU).next_to([0, yt, 0], UP, buff=0.1), T("iron", size=22, color=FE).next_to([1.2, yb, 0], DOWN, buff=0.1))
        with self.say("Now run it backwards. Instead of heating a junction, push a current round the same copper iron loop with a battery. In eighteen thirty four, Jean Peltier found that one junction warms up, while the other actually cools down below room temperature."):
            self.play(Create(loop), FadeIn(mt))
            self.add(bat, dots, j1, j2, l1, l2)
            self.play(FadeIn(bat), FadeIn(dots), FadeIn(j1), FadeIn(j2), FadeIn(l1), FadeIn(l2))
            self.wait(2)
        with self.say("Reverse the current, and the two junctions swap roles. The cold one becomes hot, and the hot one cold. This is the Peltier effect, the converse of the Seebeck effect."):
            self.play(I.animate.set_value(-1.0), run_time=0.6)
            self.wait(2.5)
        self.play(FadeOut(VGroup(loop, mt)), FadeOut(bat), FadeOut(dots), FadeOut(j1), FadeOut(j2), FadeOut(l1), FadeOut(l2))
        self.remove(bat, dots, j1, j2, l1, l2, tclk)
        eq = VGroup(M(r"H = \pi q = \pi I t", size=60, color=C_E), T("π: Peltier coefficient, heat per unit charge crossing the junction (J/C = volt)", size=24, color=th.BODY),
                    T("for metal junctions, a few millivolts", size=22, color=th.MUTED)).arrange(DOWN, buff=0.25).move_to([0, 1.4, 0])
        rule = para("The junction that absorbs heat is the one where the current flows as it would through the HOT junction of a Seebeck couple of the same pair: for Cu–Fe, from copper to iron. A working thermocouple is a heat engine: it takes heat in at the hot junction.", width=11, size=24, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("The Peltier coefficient, pi, of a junction is the heat absorbed or given out when one coulomb of charge crosses it. A current I carries a charge I t, so the heat is pi I t. Pi is measured in joules per coulomb, which is volts, and for metals it is only a few millivolts."):
            self.play(Write(eq[0]))
            self.play(FadeIn(eq[1:]))
        with self.say("Which junction cools? The one where the current flows in the same direction it would through the hot junction of a Seebeck circuit of the same metals: for copper and iron, from copper to iron. That makes sense: a working thermocouple is a heat engine, taking in heat at its hot junction."):
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(eq, rule)))
        title = T("Peltier heat is NOT Joule heat", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        rows = [("", "Peltier heat", "Joule heat"), ("where", "only at a junction of two metals", "in any conductor"), ("law", "H = πIt  (∝ I)", "H = I²Rt  (∝ I²)"),
                ("reverse I", "reversible: heating ↔ cooling", "irreversible: always heats"), ("can it cool?", "yes, below room temperature", "never")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=24 if i else 28, color=(th.BG if not c else ([th.MUTED, C_E, th.CORAL][j] if i == 0 or j == 0 else th.BODY)), weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.8, -0.9, 3.6]):
                row[j].move_to([x, 1.8 - i * 0.8, 0])
            grid.add(row)
        thom = para("Thomson effect: heat is also absorbed or given out along a SINGLE conductor whose ends are at different temperatures (positive for Cu, Ag, Zn; negative for Fe, Co, Ni; zero for Pb).", width=11.5, size=22, color=th.MUTED).to_edge(DOWN, buff=0.45)
        with self.say("Do not confuse Peltier heat with Joule heat. Peltier heat happens only at a junction of two different metals; Joule heat in any conductor. Peltier heat goes as I; Joule heat as I squared. Reverse the current, and Peltier heating becomes cooling; Joule heating stays heating. Peltier can cool a junction below room temperature; Joule never can. For completeness, there is a third effect, the Thomson effect, along a single wire with a temperature gradient. It is zero for lead, which is why lead is used as the reference metal.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
            self.play(FadeIn(thom))
        self.play(FadeOut(VGroup(title, grid, thom)))
        example(self, "A junction has Peltier coefficient 12 mV and resistance 0.50 Ω. A current of 2.0 A flows for 5.0 minutes. Find the Peltier heat and the Joule heat, and comment.",
                [r"t = 5.0\times 60 = 300\ \text{s}",
                 r"H_P = \pi It = (12\times10^{-3})(2.0)(300) = 7.2\ \text{J}",
                 r"H_J = I^{2}Rt = (2.0)^{2}(0.50)(300) = 600\ \text{J}\quad(\approx 83\times H_P)"],
                ["Worked example. A junction with a Peltier coefficient of twelve millivolts and a resistance of half an ohm carries two amps for five minutes. Compare the Peltier heat and the Joule heat.",
                 "Five minutes is three hundred seconds.",
                 "Peltier heat is pi I t: twelve millivolts times two amps times three hundred seconds, seven point two joules.",
                 "Joule heat is I squared R t: four times a half times three hundred, six hundred joules, about eighty three times bigger, and always given out. Reversing the current turns the seven point two joules from heating into cooling, but the six hundred joules stay. That is why real Peltier coolers use semiconductor pellets, with Peltier coefficients hundreds of times bigger."], size=40)
        self.quiz("The Peltier heat developed at a junction is proportional to",
                  [M("I^{2}", size=40), M("I", size=40), M(r"\sqrt{I}", size=40), M("1/I", size=40)], 1,
                  "Pause and think. Peltier heat at a junction goes as what power of the current?",
                  "B, the first power: H equals pi I t. I squared belongs to Joule heating, which is exactly why Peltier heat can be reversed and Joule heat cannot.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        al, be = 25.0, -0.1
        E = lambda th_: al * th_ + 0.5 * be * th_ ** 2
        ax = Axes(x_range=[0, 600, 100], y_range=[-1500, 3500, 1000], x_length=7.4, y_length=4.6, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 20}).move_to([-2.2, -0.3, 0])
        xl = T("hot junction θ (°C), cold at 0 °C", size=20).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = T("E (μV)", size=22, color=C_E).next_to(ax.y_axis, UP, buff=0.1)
        cur = ax.plot(E, x_range=[0, 560], color=C_E, stroke_width=5)
        tt = ValueTracker(50)
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), E(tt.get_value())), color=WHITE))
        tan = always_redraw(lambda: Line(ax.c2p(tt.get_value() - 45, E(tt.get_value()) - 45 * (al + be * tt.get_value())), ax.c2p(tt.get_value() + 45, E(tt.get_value()) + 45 * (al + be * tt.get_value())), color=th.PINK, stroke_width=3))
        eq = M(r"E = \alpha\theta + \tfrac12\beta\theta^{2}", size=44, color=C_E).move_to([4.2, 2.4, 0])
        ro = VGroup(readout("θ =", lambda: tt.get_value(), "°C", decimals=0, size=24), readout("S = dE/dθ =", lambda: al + be * tt.get_value(), "μV/°C", decimals=1, size=24, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 1.2, 0])
        with self.say("Keep the cold junction at zero, and raise the hot junction. The e m f does not grow in proportion. It follows a parabola: E equals alpha theta plus half beta theta squared, where alpha and beta are constants for the pair of metals. For most pairs, beta is small and negative, so the curve rises, turns over, and comes back down."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Write(eq))
            self.play(Create(cur), run_time=2.5)
        with self.say("The slope of this curve, d E by d theta, is the thermoelectric power: the e m f per degree. It equals alpha plus beta theta, and it falls steadily as the temperature rises."):
            self.add(dot, tan)
            self.play(FadeIn(dot), FadeIn(tan), FadeIn(ro))
            self.play(tt.animate.set_value(200), run_time=2.5)
        nl = DashedLine(ax.c2p(250, -1500), ax.c2p(250, 3125), color=th.MINT)
        nll = T("neutral θn", size=22, color=th.MINT).next_to(ax.c2p(250, 3125), UP, buff=0.1)
        il = Dot(ax.c2p(500, 0), color=th.CORAL, radius=0.1)
        ill = T("inversion θi", size=22, color=th.CORAL).next_to(ax.c2p(500, 0), UR, buff=0.1)
        with self.say("At the top, the slope is zero. The e m f is a maximum. That temperature is the neutral temperature. Keep heating, and the e m f falls, reaches zero at the temperature of inversion, and then reverses."):
            self.play(tt.animate.set_value(250), run_time=2)
            self.play(Create(nl), FadeIn(nll))
            self.play(tt.animate.set_value(540), run_time=3)
            self.play(FadeIn(il), FadeIn(ill))
        self.play(FadeOut(VGroup(ro)), FadeOut(dot), FadeOut(tan))
        self.remove(dot, tan)
        g = VGroup(ax, xl, yl, cur, nl, nll, il, ill)
        self.play(g.animate.scale(0.62).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3), eq.animate.scale(0.8).move_to([-3.8, 2.6, 0]))
        L = VGroup(M(r"S = \frac{dE}{d\theta} = \alpha + \beta\theta", size=36), M(r"\text{max: } \alpha + \beta\theta_n = 0\ \Rightarrow\ \theta_n = -\frac{\alpha}{\beta}", size=36, color=th.MINT),
                   M(r"E_{\max} = -\frac{\alpha^{2}}{2\beta}", size=36), M(r"E = 0:\ \theta\left(\alpha + \tfrac12\beta\theta\right) = 0\ \Rightarrow\ \theta_i = -\frac{2\alpha}{\beta} = 2\theta_n", size=34, color=th.CORAL),
                   M(r"\text{cold junction at } \theta_c:\ \ \theta_i = 2\theta_n - \theta_c", size=38, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        L.scale_to_fit_width(min(L.width, 7.0)).move_to([3.0, 0.0, 0])
        says = ["Now the derivation. The thermoelectric power is d E by d theta: alpha plus beta theta.",
                "The e m f is greatest where this is zero. Alpha plus beta theta n equals zero, so the neutral temperature is minus alpha over beta. Notice it contains only alpha and beta: it depends only on the pair of metals.",
                "Putting that back in, the maximum e m f is minus alpha squared over two beta.",
                "The e m f is zero again when theta times alpha plus half beta theta is zero. Apart from theta equals zero, that gives theta i equals minus two alpha over beta: twice the neutral temperature.",
                "And if the cold junction is at theta c instead of zero, the neutral temperature always lies exactly midway between the cold junction and the inversion temperature. So theta i equals two theta n minus theta c."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(FadeOut(VGroup(g, eq, L)))
        self.shift_demo()
        self.tip("θn = −α/β depends ONLY on the metals. θi = 2θn − θc moves with the cold junction: raise the cold junction by 10 °C and θi falls by 10 °C.",
                 "The classic slip: saying both temperatures depend on the cold junction. Only the inversion temperature does. Raise the cold junction by ten degrees, and theta i falls by ten degrees, while theta n does not move at all.", state="wink")
        example(self, "For a thermocouple with cold junction at 0 °C, E = 25θ − 0.05θ² μV. Find α, β, θn, θi, Emax, the thermoelectric power at 100 °C, and the hot-junction temperatures for E = 3000 μV.",
                [r"\alpha = 25\ \mu\text{V}/^{\circ}\text{C},\quad \tfrac12\beta = -0.05\ \Rightarrow\ \beta = -0.1\ \mu\text{V}/^{\circ}\text{C}^{2}",
                 r"\theta_n = -\frac{25}{-0.1} = 250^{\circ}\text{C},\quad \theta_i = 2(250) - 0 = 500^{\circ}\text{C}",
                 r"E_{\max} = 25(250) - 0.05(250)^{2} = 6250 - 3125 = 3125\ \mu\text{V}",
                 r"S_{100} = 25 - 0.1(100) = 15\ \mu\text{V}/^{\circ}\text{C}",
                 r"\theta^{2} - 500\theta + 60000 = 0\ \Rightarrow\ \theta = \frac{500 \pm 100}{2} = 200^{\circ}\text{C or } 300^{\circ}\text{C}"],
                ["The big worked example. A thermocouple with E equals twenty five theta minus zero point zero five theta squared microvolts. Find everything.",
                 "Compare with alpha theta plus half beta theta squared. Alpha is twenty five, and half beta is minus zero point zero five, so beta is minus zero point one.",
                 "The neutral temperature is minus alpha over beta: two hundred and fifty degrees. The inversion temperature is twice that: five hundred.",
                 "The maximum e m f, at two fifty: six thousand two fifty minus three thousand one twenty five, three thousand one hundred and twenty five microvolts.",
                 "At one hundred degrees, the thermoelectric power is twenty five minus ten, fifteen microvolts per degree.",
                 "And E equals three thousand gives a quadratic with two roots: two hundred and three hundred degrees, one on each side of the neutral temperature, as the parabola demands."], size=34)
        example(self, "The neutral temperature of a Cu–Fe couple is 270 °C. Find θi with the cold junction at 0 °C and at 20 °C. If α = 13.5 μV/°C, find β and E at 100 °C (cold junction 0 °C).",
                [r"\theta_i = 2(270) - 0 = 540^{\circ}\text{C};\quad \theta_i = 540 - 20 = 520^{\circ}\text{C}",
                 r"\beta = -\frac{\alpha}{\theta_n} = -\frac{13.5}{270} = -0.05\ \mu\text{V}/^{\circ}\text{C}^{2}",
                 r"E = 13.5(100) + \tfrac12(-0.05)(100)^{2} = 1350 - 250 = 1100\ \mu\text{V} = 1.10\ \text{mV}"],
                ["Another. Copper iron, with a neutral temperature of two seventy degrees.",
                 "With the cold junction at zero, theta i is five forty. At twenty degrees, five twenty: twenty degrees lower.",
                 "Beta is minus alpha over theta n: minus thirteen point five over two seventy, minus zero point zero five.",
                 "At one hundred degrees, E is thirteen fifty minus two fifty: eleven hundred microvolts, one point one millivolts."], size=38)
        self.quiz("The neutral temperature of a thermocouple is 270 °C. With the cold junction at 10 °C the temperature of inversion is",
                  ["260 °C", "280 °C", "530 °C", "550 °C"], 2,
                  "Pause and think. Neutral temperature two seventy, cold junction at ten. What is the inversion temperature?",
                  "C, five thirty: two times two seventy, minus ten. Five fifty is the trap: adding the cold junction temperature instead of subtracting it.")

    def shift_demo(self):
        al, be = 25.0, -0.1
        th_c = ValueTracker(0.0)
        ax = Axes(x_range=[0, 600, 100], y_range=[-1500, 3500, 1000], x_length=8.0, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 20}).move_to([-1.2, -0.4, 0])
        E = lambda t: (al * t + 0.5 * be * t ** 2) - (al * th_c.get_value() + 0.5 * be * th_c.get_value() ** 2)
        cur = always_redraw(lambda: ax.plot(E, x_range=[th_c.get_value(), 560], color=C_E, stroke_width=5))
        nl = DashedLine(ax.c2p(250, -1500), ax.c2p(250, 3300), color=th.MINT)
        cd = always_redraw(lambda: Dot(ax.c2p(th_c.get_value(), 0), color=th.SKY, radius=0.1))
        idt = always_redraw(lambda: Dot(ax.c2p(500 - th_c.get_value(), 0), color=th.CORAL, radius=0.1))
        ro = VGroup(readout("θc =", lambda: th_c.get_value(), "°C", decimals=0, size=26, color=th.SKY), readout("θn =", lambda: 250, "°C", decimals=0, size=26, color=th.MINT),
                    readout("θi =", lambda: 500 - th_c.get_value(), "°C", decimals=0, size=26, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.8, 1.0, 0])
        with self.say("Watch it happen. Warm the cold junction from zero up to one hundred degrees. The neutral temperature stays fixed at two fifty, but the inversion point slides down, always as far beyond two fifty as the cold junction is below it."):
            self.add(cur, cd, idt)
            self.play(Create(ax), FadeIn(cur), Create(nl), FadeIn(cd), FadeIn(idt), FadeIn(ro))
            self.play(th_c.animate.set_value(100), run_time=4)
            self.play(th_c.animate.set_value(0), run_time=2)
        self.play(FadeOut(VGroup(ax, nl, ro)), FadeOut(cur), FadeOut(cd), FadeOut(idt))
        self.remove(cur, cd, idt)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        n = 8
        xs = np.linspace(-3.6, 1.6, n * 2 + 1)
        pts = [np.array([x, 1.0 if k % 2 == 0 else -1.0, 0]) for k, x in enumerate(xs)]
        segs = VGroup(*[Line(pts[k], pts[k + 1], color=CU if k % 2 == 0 else FE, stroke_width=6) for k in range(len(pts) - 1)])
        front = VGroup(*[Dot(p, radius=0.14, color=th.INK) for k, p in enumerate(pts) if k % 2 == 0])
        back = VGroup(*[Dot(p, radius=0.12, color=th.MUTED) for k, p in enumerate(pts) if k % 2 == 1])
        cone = Polygon([-5.6, 2.6, 0], [-3.8, 1.3, 0], [-3.8, -1.3, 0], [-5.6, -2.6, 0], stroke_color=th.BODY, stroke_width=3, fill_color=th.FAINT, fill_opacity=0.25)
        rays = VGroup(*[Arrow([-6.8, y, 0], [-3.9, y * 0.35 + 1.0 * 0, 0], buff=0, color=th.CORAL, stroke_width=3, max_tip_length_to_length_ratio=0.12) for y in (-2.0, -1.0, 0.0, 1.0, 2.0)])
        shield = Rectangle(width=6.0, height=0.6, fill_color=th.PANEL, fill_opacity=0.8, stroke_width=0).move_to([-1.0, -1.0, 0])
        lead = VGroup(wire(pts[0], [-3.6, -2.4, 0], [2.6, -2.4, 0]), wire(pts[-1], [2.6, 1.0, 0], [2.6, -2.0, 0]), galvo([2.6, -2.2, 0], r=0.3))
        lab = VGroup(T("blackened junctions face the radiation", size=22, color=th.INK).move_to([-1.0, 1.7, 0]), T("shielded junctions stay at room temperature", size=22, color=th.MUTED).move_to([-1.0, -1.65, 0]))
        with self.say("A single thermocouple gives only microvolts. A thermopile joins a large number of them in series, so that their e m fs add. Antimony bismuth pairs are used, because they give the most."):
            self.play(Create(segs), FadeIn(front), FadeIn(back))
        with self.say("Alternate junctions are blackened and face the front, at the narrow end of a polished cone. The other junctions are shielded inside, at room temperature. Radiation falling into the cone heats the black junctions, and the many small e m fs add up to drive a current through a sensitive galvanometer."):
            self.play(FadeIn(cone), FadeIn(shield), FadeIn(lab), Create(lead))
            self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.1))
            self.play(front.animate.set_color(th.CORAL), run_time=1.5)
        uses = para("So sensitive it registers the warmth of a person a few metres away, or of the Moon. Used for radiant heat measurement, radiation pyrometers, infrared detectors and burglar alarms; and run as Peltier devices, in portable coolers. Thermoelectric generators power deep-space probes like Voyager.", width=11.5, size=24, color=th.AMBER).to_edge(DOWN, buff=0.35)
        with self.say("A thermopile is astonishingly sensitive. It can register the warmth of a person standing a few metres away, or of the Moon. It is used to measure radiant heat, in radiation pyrometers for furnaces, in infrared detectors and burglar alarms. Run the Peltier way, the same kind of device makes portable coolers. And thermoelectric generators, heated by plutonium, power deep space probes like Voyager."):
            self.play(FadeOut(VGroup(lab, segs, front, back, cone, rays, shield, lead)))
            uses.move_to(ORIGIN)
            self.play(FadeIn(uses))
        nb = neby_in(self, "cool", corner=UR)
        self.wait(0.3)
        self.play(FadeOut(uses))
        neby_out(self, nb)
        example(self, "A copper–constantan thermocouple has thermoelectric power 42 μV/°C; the galvanometer just detects 2.1 μV. Find the smallest temperature difference it can measure, and the e.m.f. of a 40-couple thermopile for a difference of 0.50 °C.",
                [r"\Delta\theta = \frac{\Delta E}{S} = \frac{2.1\ \mu\text{V}}{42\ \mu\text{V}/^{\circ}\text{C}} = 0.050^{\circ}\text{C}",
                 r"E = NS\,\Delta\theta = 40\times 42\times 0.50 = 840\ \mu\text{V} = 0.84\ \text{mV}"],
                ["Worked example. A copper constantan couple gives forty two microvolts per degree, and the galvanometer can just detect two point one microvolts. What is the smallest temperature difference it can measure? And what does a forty couple thermopile give for half a degree?",
                 "Delta theta is delta E over S: two point one over forty two, five hundredths of a degree.",
                 "Forty couples in series: forty times forty two times zero point five, eight hundred and forty microvolts, comfortably measurable. That is the whole point of a thermopile."], size=40)
        self.quiz("In a thermopile the thermocouples are joined",
                  ["in parallel", "in series", "in a bridge", "back to back"], 1,
                  "Last check. How are the thermocouples in a thermopile connected?",
                  "B, in series, so that their tiny e m fs add up. In parallel, the e m f would stay the size of just one couple.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Seebeck: two different metals, junctions at different temperatures, an e.m.f. Depends only on the metals and ΔT.",
            "Series Sb, Fe, Cd, Zn, Ag, Au, Cr, Sn, Pb, Hg, Mn, Cu, Pt, Co, Ni, Bi: earlier → later through the cold junction; Sb–Bi gives most.",
            M(r"\text{Peltier: } H = \pi It\ (\propto I,\ \text{reversible});\ \text{Joule: } I^{2}Rt\ (\text{irreversible})", size=34),
            M(r"E = \alpha\theta + \tfrac12\beta\theta^{2},\ \ S = \frac{dE}{d\theta} = \alpha + \beta\theta", size=34),
            M(r"\theta_n = -\frac{\alpha}{\beta}\ (\text{metals only}),\ \ \theta_i = 2\theta_n - \theta_c,\ \ E_{\max} = -\frac{\alpha^{2}}{2\beta}", size=34),
            "Thermopile: many Sb–Bi couples in series, blackened junctions, detects heat radiation.",
        ], "Let us recap. In the Seebeck effect, a temperature difference between two junctions of different metals makes an e m f, set by the metals and the temperature difference. The thermoelectric series gives the direction: earlier to later through the cold junction. In the Peltier effect, a current heats one junction and cools the other, H equals pi I t, reversible, unlike Joule heating. The e m f follows a parabola, with the neutral temperature at minus alpha over beta and inversion at two theta n minus theta c. And a thermopile adds many couples in series to detect radiation.")
        self.outro("That is thermoelectricity. Next, we turn to magnetism: the force on moving charges and currents, and the fields that currents create, in Magnetic Field. See you there, on NEBians.")
