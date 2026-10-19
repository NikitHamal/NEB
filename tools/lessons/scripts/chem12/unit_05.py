import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

ZN = "#9FB3C8"
CU = "#D9824B"
AG = "#D5DAE6"
CUSO4 = "#3E8EDE"


class Cell:
    """A two-beaker galvanic cell. Everything is built at construction; play pieces from the scene."""

    def __init__(self, left=("Zn", ZN, "#B9C4D6", "ZnSO₄"), right=("Cu", CU, CUSO4, "CuSO₄"), y=-1.2):
        self.y = y
        self.bl = C.Beaker(center=[-3.2, y, 0], w=2.6, h=2.4, level=0.7, color=left[2], opacity=0.3)
        self.br = C.Beaker(center=[3.2, y, 0], w=2.6, h=2.4, level=0.7, color=right[2], opacity=0.45)
        self.rl = Rectangle(width=0.36, height=3.0, fill_color=left[1], fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to([-3.5, y + 0.6, 0])
        self.rr = Rectangle(width=0.36, height=3.0, fill_color=right[1], fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to([3.5, y + 0.6, 0])
        self.ll = T(left[0], size=26, color=left[1], weight="BOLD").next_to(self.rl, UP, buff=0.1)
        self.lr = T(right[0], size=26, color=right[1], weight="BOLD").next_to(self.rr, UP, buff=0.1)
        self.sl = T(left[3], size=22, color=th.BODY).next_to(self.bl.g, DOWN, buff=0.15)
        self.sr = T(right[3], size=22, color=th.BODY).next_to(self.br.g, DOWN, buff=0.15)
        top = y + 2.4
        self.wire = VMobject(stroke_color=th.INK, stroke_width=3).set_points_as_corners([self.rl.get_top() + UP * 0.35, [-3.5, top, 0], [-0.6, top, 0]])
        self.wire2 = VMobject(stroke_color=th.INK, stroke_width=3).set_points_as_corners([[0.6, top, 0], [3.5, top, 0], self.rr.get_top() + UP * 0.35])
        self.meter = VGroup(Circle(radius=0.6, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.INK, stroke_width=3), T("V", size=28, color=th.AMBER, weight="BOLD")).move_to([0, top, 0])
        bx = 1.3
        self.bridge = VMobject(stroke_color="#E8E2C8", stroke_width=26, stroke_opacity=0.55).set_points_as_corners([[-2.3, y + 0.1, 0], [-2.3, y + 1.5, 0], [2.3, y + 1.5, 0], [2.3, y + 0.1, 0]])
        self.bl_lab = T("salt bridge (KCl in agar)", size=20, color="#E8E2C8").next_to([0, y + 1.5, 0], DOWN, buff=0.25)
        self.top = top

    def static(self):
        return VGroup(self.bl.g, self.br.g, self.rl, self.rr, self.ll, self.lr, self.sl, self.sr)

    def circuit(self):
        return VGroup(self.wire, self.wire2, self.meter)

    def electrons(self, phase):
        """Electrons flowing left to right along the wire; phase in [0, 1)."""
        path = [self.rl.get_top() + UP * 0.35, np.array([-3.5, self.top, 0]), np.array([3.5, self.top, 0]), self.rr.get_top() + UP * 0.35]
        segs = [np.linalg.norm(b - a) for a, b in zip(path, path[1:])]
        L = sum(segs)
        g = VGroup()
        for k in range(10):
            s = ((k / 10 + phase) % 1.0) * L
            p = path[-1]
            for a, b, l in zip(path, path[1:], segs):
                if s <= l:
                    p = a + (b - a) * s / l
                    break
                s -= l
            if abs(p[0]) < 0.62 and abs(p[1] - self.top) < 0.1:
                continue
            g.add(Dot(p, radius=0.07, color=th.SKY))
        return g


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 5
    TITLE = "Electrochemistry"
    SUBTITLE = "Turning reactions into electricity"
    SECTIONS = ["Electrode potential", "Hydrogen and calomel electrodes", "Electrochemical series", "Voltaic cells: Zn-Cu, Ag-Cu",
                "Cell potential", "Cell potential and free energy", "Batteries and fuel cells"]
    NEXT = "Unit 6 · Transition Metals"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        bk = C.Beaker(center=[-2.2, -1.0, 0], w=2.8, h=2.8, level=0.72, color=CUSO4, opacity=0.6)
        strip = Rectangle(width=0.4, height=3.0, fill_color=ZN, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to([-2.2, 2.6, 0])
        sl = T("zinc strip", size=24, color=ZN).next_to(strip, RIGHT, buff=0.3)
        bl = T("copper sulphate solution", size=24, color=CUSO4).next_to(bk.g, DOWN, buff=0.2)
        Tt = ValueTracker(25)
        rd = DecimalNumber(25.0, num_decimal_places=1, font_size=54, color=th.CORAL, unit=r"^{\circ}\mathrm{C}")
        rd.add_updater(lambda m: m.set_value(Tt.get_value()).move_to([3.0, 0.6, 0]))
        eq = chem(r"Zn + Cu^{2+} \rightarrow Zn^{2+} + Cu", size=42).move_to([3.0, 2.2, 0])
        with self.say("Drop a strip of zinc into blue copper sulphate solution. A reaction starts at once."):
            self.play(FadeIn(bk.g), FadeIn(bl), FadeIn(strip), FadeIn(sl))
            self.play(strip.animate.move_to([-2.2, -0.4, 0]), FadeOut(sl), run_time=1.0)
        coat = Rectangle(width=0.44, height=1.9, fill_color=CU, fill_opacity=0.0, stroke_width=0).move_to([-2.2, -1.0, 0])
        self.add(coat)
        with self.say("A brown layer of copper grows on the zinc. The blue colour fades as copper ions leave the solution. And the beaker gets warm."):
            self.add(rd)
            self.play(Write(eq), FadeIn(rd))
            self.play(coat.animate.set_fill(CU, opacity=0.9), bk.liq.animate.set_fill("#9DB8D0", opacity=0.3), Tt.animate.set_value(31), run_time=4)
        nb = C.show_neby(self, "think", height=1.5, at=[3.0, -1.4, 0])
        with self.say("Electrons are jumping straight from zinc atoms to copper ions, and all that energy is wasted as heat. What if we could make those electrons travel through a wire instead? Then the same reaction would light a bulb. That is the whole idea of a battery, and by the end of this lesson, we will build one."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        rd.clear_updaters()
        self.play(FadeOut(VGroup(bk.g, bl, strip, coat, rd, eq)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 5: Electrochemistry. How redox reactions produce electricity, how we measure the push behind them, and how that push is tied to free energy and to the batteries in your phone and your inverter."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. Electrode potentials. The standard hydrogen and calomel electrodes. The electrochemical series and its uses. Voltaic cells, zinc copper and silver copper. Cell potential and the Nernst equation. The link between cell potential and free energy, with Faraday's laws. And finally, commercial batteries and the fuel cell.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        bk = C.Beaker(center=[-3.2, -0.9, 0], w=3.2, h=3.0, level=0.75, color=C.WATER, opacity=0.2)
        rod = Rectangle(width=0.6, height=3.6, fill_color=ZN, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to([-3.2, -0.2, 0])
        rl = T("Zn", size=28, color=ZN, weight="BOLD").next_to(rod, UP, buff=0.1)
        eq = chem(r"Zn(s) \rightleftharpoons Zn^{2+}(aq) + 2e^-", size=44).move_to([2.8, 2.0, 0])
        with self.say("Dip a strip of zinc into water. A few zinc atoms leave the metal as zinc ions, leaving their two electrons behind in the metal."):
            self.play(FadeIn(bk.g), FadeIn(rod), FadeIn(rl))
            self.play(Write(eq))
        ions = VGroup()
        es = VGroup()
        for k in range(6):
            y = -1.9 + 0.45 * k
            ion = VGroup(Circle(radius=0.16, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0), T("+", size=20, color=WHITE, weight="BOLD")).move_to([-3.2 + 0.3, y, 0])
            ions.add(ion)
            es.add(VGroup(Circle(radius=0.1, fill_color=th.SKY, fill_opacity=1, stroke_width=0), T("−", size=16, color=th.BG, weight="BOLD")).move_to([-3.2 + 0.18, y, 0]))
        with self.say("The metal becomes slightly negative. The layer of solution next to it becomes slightly positive. This electrical double layer quickly stops any more ions leaving, and an equilibrium potential difference is set up across the boundary."):
            self.play(FadeIn(es), FadeIn(ions))
            self.play(ions.animate.shift(RIGHT * 0.55), run_time=1.2)
            self.play(Indicate(es, color=th.SKY), Indicate(ions, color=th.CORAL))
        d = self.callout("key", "Electrode potential: the potential difference between a metal and its solution at equilibrium. It measures the tendency to lose electrons (oxidation potential) or gain them (reduction potential).", width=6.4, size=22).move_to([3.0, -0.4, 0])
        with self.say("That potential difference is the electrode potential. It measures how strongly the electrode tends to lose electrons, its oxidation potential, or to gain them, its reduction potential."):
            self.play(FadeIn(d, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(bk.g, rod, rl, eq, ions, es, d)))
        conv = M(r"E_{\text{oxidation}} = -\,E_{\text{reduction}}", size=56, color=th.AMBER).move_to(UP * 1.8)
        cnote = T("By convention, tables always list REDUCTION potentials.", size=28, color=th.BODY).next_to(conv, DOWN, buff=0.3)
        with self.say("Zinc, which gives up electrons easily, has a positive oxidation potential. Copper prefers to take electrons back. To avoid confusion, the world agreed to tabulate only reduction potentials. An oxidation potential is just the same number with the sign flipped."):
            self.play(Write(conv))
            self.play(FadeIn(cnote))
        std = self.callout("remember", "Standard electrode potential E°: at 298 K, every ion at 1 M, every gas at 1 bar, measured against the standard hydrogen electrode (0.000 V).", width=11, size=26).next_to(cnote, DOWN, buff=0.5)
        with self.say("Electrode potentials depend on concentration, temperature and gas pressure. So we fix standard conditions: two ninety eight kelvin, all ions at one molar, all gases at one bar. Measured against the hydrogen electrode, that gives the standard electrode potential, E nought."):
            self.play(FadeIn(std, shift=UP * 0.2))
        self.play(FadeOut(VGroup(conv, cnote, std)))
        vm = VGroup(Circle(radius=0.8, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.INK, stroke_width=3), T("V", size=36, color=th.AMBER, weight="BOLD")).move_to([0, 0.8, 0])
        lead1 = Line([-0.6, 0.3, 0], [-2.2, -1.6, 0], color=th.CORAL, stroke_width=4)
        lead2 = Line([0.6, 0.3, 0], [2.2, -1.6, 0], color=th.INK, stroke_width=4)
        one = Rectangle(width=0.4, height=1.6, fill_color=ZN, fill_opacity=1, stroke_width=0).move_to([-2.2, -2.2, 0])
        q = T("?", size=60, color=th.CORAL, weight="BOLD").move_to([2.2, -2.2, 0])
        nb = C.show_neby(self, "oops", height=1.3, corner=DR)
        with self.say("Can we measure one electrode's potential on its own? No. A voltmeter needs two contacts, and the second wire dipping in the solution would itself be a second electrode. Every measurement is a difference between two electrodes. So all E nought values are relative, measured against one agreed reference."):
            self.play(FadeIn(vm), Create(lead1), Create(lead2), FadeIn(one))
            self.play(FadeIn(q, scale=1.5))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(vm, lead1, lead2, one, q)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        c = np.array([-3.0, -0.6, 0])
        bk = C.Beaker(center=c + DOWN * 0.6, w=3.0, h=2.6, level=0.75, color=C.WATER, opacity=0.25)
        tube = VGroup(Line(c + LEFT * 0.45 + UP * 2.6, c + LEFT * 0.45 + DOWN * 0.6, color=th.INK, stroke_width=3),
                      Line(c + RIGHT * 0.45 + UP * 2.6, c + RIGHT * 0.45 + DOWN * 0.6, color=th.INK, stroke_width=3))
        inlet = Line(c + LEFT * 0.45 + UP * 1.8, c + LEFT * 1.6 + UP * 1.8, color=th.INK, stroke_width=3)
        pt = Rectangle(width=0.5, height=0.6, fill_color="#3A3A3A", fill_opacity=1, stroke_color=WHITE, stroke_width=1).move_to(c + DOWN * 1.2)
        wire = Line(c + UP * 2.8, pt.get_top(), color=th.MUTED, stroke_width=2)
        labs = VGroup(T("H₂ gas, 1 bar", size=22, color=th.SKY).next_to(inlet, UP, buff=0.1),
                      T("Pt foil coated with Pt black", size=22, color=th.BODY).next_to(pt, RIGHT, buff=1.0).shift(DOWN * 0.5),
                      T("1 M H⁺, 298 K", size=22, color=C.WATER).next_to(bk.g, DOWN, buff=0.2))
        arrow_pt = Arrow(labs[1].get_left(), pt.get_right(), buff=0.1, color=th.FAINT, stroke_width=2)
        bt = ValueTracker(0)

        def bubbles():
            g = VGroup()
            for k in range(6):
                f = (bt.get_value() + k / 6) % 1
                g.add(Circle(radius=0.07, stroke_color=th.SKY, stroke_width=2).move_to(pt.get_top() + UP * 1.6 * f + RIGHT * 0.12 * np.sin(6 * f + k)))
            return g
        bub = always_redraw(bubbles)
        eq = VGroup(chem(r"2H^+(aq) + 2e^- \rightleftharpoons H_2(g)", size=40), M(r"E^{\circ} = 0.000\ \mathrm{V}\ (\text{by definition})", size=38, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([3.2, 1.6, 0])
        with self.say("The reference is the standard hydrogen electrode. A platinum foil, coated with finely divided platinum black, dips into a one molar solution of hydrogen ions at two ninety eight kelvin, while pure hydrogen gas at one bar bubbles over it. The platinum does not react. It only provides a surface for electrons to change hands."):
            self.play(FadeIn(bk.g), Create(tube), Create(inlet), FadeIn(pt), Create(wire))
            self.add(bub)
            self.play(FadeIn(labs), GrowArrow(arrow_pt), bt.animate.set_value(2), run_time=3, rate_func=linear)
        with self.say("Its half reaction, two hydrogen ions plus two electrons giving hydrogen gas, is assigned exactly zero volts. Every other E nought is measured against it."):
            nb = C.show_neby(self, "read", height=1.3, corner=DR)
            self.play(Write(eq[0]))
            self.play(Write(eq[1]), bt.animate.set_value(4), run_time=2, rate_func=linear)
        C.hide_neby(self, nb)
        dis = para("But it is awkward: it needs very pure H₂ at constant pressure, exactly 1 M acid, and the platinum is easily poisoned by arsenic or sulphide.", width=6.2, size=24, color=th.CORAL).move_to([3.2, -0.1, 0])
        with self.say("It is the primary reference, but it is awkward to use. It needs a supply of very pure hydrogen at constant pressure, an exactly one molar acid, and its platinum surface is easily poisoned by traces of arsenic or sulphide."):
            self.play(FadeIn(dis), bt.animate.set_value(6), run_time=3, rate_func=linear)
        self.play(FadeOut(VGroup(bk.g, tube, inlet, pt, wire, labs, arrow_pt, eq, dis)), FadeOut(bub))
        self.remove(bub)
        cc = np.array([-3.2, -0.4, 0])
        outer = RoundedRectangle(corner_radius=0.3, width=1.8, height=4.4, stroke_color=th.INK, stroke_width=3).move_to(cc)
        kcl = Rectangle(width=1.7, height=3.2, fill_color=C.WATER, fill_opacity=0.2, stroke_width=0).move_to(cc + DOWN * 0.55)
        inner = RoundedRectangle(corner_radius=0.15, width=0.7, height=3.0, stroke_color=th.INK, stroke_width=2).move_to(cc + UP * 0.4)
        hg = Rectangle(width=0.6, height=0.4, fill_color="#C8CDD8", fill_opacity=1, stroke_width=0).move_to(cc + DOWN * 0.85)
        paste = Rectangle(width=0.6, height=0.35, fill_color="#F1F1E6", fill_opacity=1, stroke_width=0).next_to(hg, UP, buff=0)
        ptw = Line(cc + UP * 2.4, hg.get_center(), color=th.MUTED, stroke_width=2)
        frit = Rectangle(width=0.3, height=0.15, fill_color="#8C93A8", fill_opacity=1, stroke_width=0).move_to(cc + DOWN * 2.6)
        cl = VGroup(T("Pt wire", size=20, color=th.MUTED), T("Hg₂Cl₂ paste (calomel)", size=20, color=th.INK), T("mercury", size=20, color="#C8CDD8"), T("KCl solution", size=20, color=C.WATER))
        anchors = [cc + UP * 2.0, paste.get_center(), hg.get_center(), cc + DOWN * 1.9]
        for t, a, dy in zip(cl, anchors, [0, 0.3, -0.3, 0]):
            t.next_to([-1.9, a[1] + dy, 0], RIGHT, buff=0)
        arrows = VGroup(*[Arrow(t.get_left(), a + RIGHT * 0.35, buff=0.1, color=th.FAINT, stroke_width=2, max_tip_length_to_length_ratio=0.15) for t, a in zip(cl, anchors)])
        ceq = VGroup(chem(r"Hg(l)\,|\,Hg_2Cl_2(s)\,|\,KCl(aq)", size=34), chem(r"Hg_2Cl_2(s) + 2e^- \rightleftharpoons 2Hg(l) + 2Cl^-(aq)", size=32)).arrange(DOWN, buff=0.25).move_to([3.4, 2.3, 0])
        with self.say("So for everyday work we use a secondary reference, the calomel electrode. Mercury, covered with a paste of mercury one chloride, called calomel, in contact with potassium chloride solution, with a platinum wire dipping into the mercury."):
            self.play(Create(outer), FadeIn(kcl), Create(inner), FadeIn(hg), FadeIn(paste), Create(ptw), FadeIn(frit))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(t), GrowArrow(a)) for t, a in zip(cl, arrows)], lag_ratio=0.3))
            self.play(Write(ceq))
        rows = [["KCl", "E / V"], ["saturated", "+0.242"], ["1.0 M", "+0.280"], ["0.1 M", "+0.334"]]
        tb = C.table(rows, [2.4, 2.0], row_h=0.55, size=24, colors=[th.INK, th.AMBER]).move_to([3.6, -0.9, 0])
        with self.say("Its potential depends only on the chloride concentration, which is easy to fix. Plus zero point two four two volts with saturated potassium chloride. It is compact, robust and steady, which is why it is the reference half of almost every pH meter."):
            self.play(FadeIn(tb))
        self.play(FadeOut(VGroup(outer, kcl, inner, hg, paste, ptw, frit, cl, arrows, ceq, tb)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        data = [("Li", -3.04), ("K", -2.93), ("Ca", -2.87), ("Na", -2.71), ("Mg", -2.37), ("Al", -1.66), ("Zn", -0.76), ("Fe", -0.44),
                ("Ni", -0.25), ("Sn", -0.14), ("Pb", -0.13), ("H", 0.00), ("Cu", 0.34), ("Ag", 0.80), ("Au", 1.50)]
        title = T("The electrochemical series (E°, reduction)", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        x0, sc, top, rh = -0.6, 1.25, 2.35, 0.355
        axis = Line([x0, top + 0.25, 0], [x0, top - rh * 15 + 0.1, 0], color=th.MUTED, stroke_width=2)
        zl = T("0 V", size=18, color=th.MUTED).next_to(axis, UP, buff=0.05)
        el = VGroup()
        for i, (sy, v) in enumerate(data):
            y = top - rh * i
            col = th.AMBER if sy == "H" else (th.CORAL if v < 0 else th.MINT)
            w = max(0.04, abs(v) * sc)
            bar = Rectangle(width=w, height=rh * 0.7, fill_color=col, fill_opacity=0.85, stroke_width=0)
            bar.move_to([x0 - w / 2 if v < 0 else x0 + w / 2, y, 0])
            nm = T(sy, size=22, color=col, weight="BOLD").move_to([-6.2, y, 0])
            val = T(f"{v:+.2f}" if v else "0.00", size=18, color=th.BODY)
            if v < 0:
                val.next_to(bar, LEFT, buff=0.08)
            else:
                val.next_to(bar, RIGHT, buff=0.08)
            el.add(VGroup(bar, nm, val))
        with self.say("Arrange the standard reduction potentials in order, and you get the electrochemical series. Lithium, potassium, calcium, sodium, magnesium, aluminium, zinc, iron, nickel, tin, lead, then hydrogen at zero, then copper, silver and gold.") as v:
            self.play(FadeIn(title), Create(axis), FadeIn(zl))
            for e in el:
                self.play(FadeIn(e, shift=RIGHT * 0.15), run_time=0.25)
                self.hold(v.dur / 16 - 0.3)
        a1 = Arrow([3.4, top - rh * 14, 0], [3.4, top, 0], buff=0, color=th.CORAL, stroke_width=5)
        a1l = para("stronger reducing agent: loses electrons more easily", width=2.8, size=22, color=th.CORAL).next_to(a1, RIGHT, buff=0.2).shift(UP * 1.2)
        mem = para("Memory line: Little Katie Can Name Mg All Zinc Ferrous Nickel Snow Pblue Here Cup Hg Again Pt Au", width=2.8, size=20, color=th.MUTED).next_to(a1, RIGHT, buff=0.2).shift(DOWN * 1.2)
        with self.say("The more negative the potential, the stronger the reducing agent. Lithium is the strongest in the list. The more positive, the stronger the oxidising agent. A memory line helps: Little Katie Can Name Magnesium All Zinc Ferrous Nickel Snow P blue Here Cup H g Again Platinum Gold."):
            self.play(GrowArrow(a1), FadeIn(a1l))
            self.play(FadeIn(mem))
        self.play(FadeOut(VGroup(title, axis, zl, el, a1, a1l, mem)))
        title = T("Using the series", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        b1 = C.Beaker(center=[-3.6, -0.8, 0], w=2.4, h=2.4, level=0.7, color=CUSO4, opacity=0.5)
        b2 = C.Beaker(center=[0.0, -0.8, 0], w=2.4, h=2.4, level=0.7, color="#9DB8D0", opacity=0.3)
        z = Rectangle(width=0.3, height=2.2, fill_color=ZN, fill_opacity=1, stroke_width=0).move_to([-3.6, -0.3, 0])
        cu = Rectangle(width=0.3, height=2.2, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([0.0, -0.3, 0])
        l1 = VGroup(T("Zn in CuSO₄", size=22, color=th.INK), T("copper deposits ✓", size=20, color=th.MINT)).arrange(DOWN, buff=0.08).next_to(b1.g, DOWN, buff=0.15)
        l2 = VGroup(T("Cu in ZnSO₄", size=22, color=th.INK), T("nothing happens ✗", size=20, color=th.CORAL)).arrange(DOWN, buff=0.08).next_to(b2.g, DOWN, buff=0.15)
        coat = Rectangle(width=0.36, height=1.5, fill_color=CU, fill_opacity=0, stroke_width=0).move_to([-3.6, -0.75, 0])
        with self.say("Its first use: predicting displacement. A metal pushes out of solution any metal below it in the series. Zinc, at minus zero point seven six, displaces copper, at plus zero point three four. Copper cannot displace zinc."):
            self.play(FadeIn(title), FadeIn(b1.g), FadeIn(b2.g), FadeIn(z), FadeIn(cu))
            self.add(coat)
            self.play(coat.animate.set_fill(CU, opacity=0.9), b1.liq.animate.set_fill("#9DB8D0", opacity=0.3), FadeIn(l1), run_time=2)
            self.play(FadeIn(l2))
        b3 = C.Beaker(center=[3.8, -0.8, 0], w=2.4, h=2.4, level=0.7, color=th.CORAL, opacity=0.15)
        mg = Rectangle(width=0.3, height=2.2, fill_color=C.EL["Mg"], fill_opacity=1, stroke_width=0).move_to([3.5, -0.3, 0])
        cu2 = Rectangle(width=0.3, height=2.2, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([4.2, -0.3, 0])
        l3 = VGroup(T("Mg and Cu in dilute HCl", size=22, color=th.INK), T("only Mg fizzes: above H", size=20, color=th.AMBER)).arrange(DOWN, buff=0.08).next_to(b3.g, DOWN, buff=0.15)
        bt = ValueTracker(0)
        bub = always_redraw(lambda: VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=2).move_to([3.5 + 0.12 * np.sin(5 * k), -1.7 + ((bt.get_value() + k / 7) % 1) * 1.5, 0]) for k in range(7)]))
        with self.say("Second, metals above hydrogen, like zinc, iron, magnesium and aluminium, liberate hydrogen from dilute acids. Copper, silver and gold, below hydrogen, do not."):
            self.play(FadeIn(b3.g), FadeIn(mg), FadeIn(cu2), FadeIn(l3))
            self.add(bub)
            self.play(bt.animate.set_value(3), run_time=3, rate_func=linear)
        more = VGroup(*[T(s, size=22, color=th.BODY) for s in ["• which electrode is the anode, and the cell EMF", "• whether a redox reaction is feasible (E°cell > 0)", "• which ion is discharged first in electrolysis", "• galvanising: zinc corrodes to protect iron"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=1.4).shift(RIGHT * 2.6)
        self.play(FadeOut(title))
        with self.say("It also tells us which electrode is the anode in a cell and the cell's E M F, whether a redox reaction is feasible, which ion is discharged first in electrolysis, and why zinc coating protects iron: zinc corrodes first, sacrificially."):
            self.play(FadeIn(more, shift=DOWN * 0.2))
        self.play(FadeOut(VGroup(b1.g, b2.g, b3.g, z, cu, coat, l1, l2, l3, mg, cu2, more)), FadeOut(bub))
        self.remove(bub)
        self.quiz("Which metal will NOT liberate hydrogen from dilute HCl?",
                  ["Zn", "Mg", "Fe", "Cu"], 3,
                  "Quick check. Which of these metals cannot give hydrogen gas with dilute hydrochloric acid? Pause and think.",
                  "D, copper. Its standard reduction potential, plus zero point three four volts, is above hydrogen's zero, so it is a weaker reducing agent than hydrogen and cannot push hydrogen ions to hydrogen gas. Zinc, magnesium and iron all have negative potentials.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        cell = Cell()
        with self.say("Now we capture the electrons. Put the zinc in zinc sulphate in one beaker, and copper in copper sulphate in another. The zinc never touches the copper ions."):
            self.play(FadeIn(cell.static()))
        with self.say("Join the two metals with a wire through a voltmeter. Nothing yet. The circuit is not complete. Now add the salt bridge: an upside down U tube full of potassium chloride set in agar jelly."):
            self.play(Create(cell.wire), Create(cell.wire2), FadeIn(cell.meter))
            self.play(Create(cell.bridge), FadeIn(cell.bl_lab))
        ph = ValueTracker(0)
        el = always_redraw(lambda: cell.electrons(ph.get_value()))
        rd = DecimalNumber(1.10, num_decimal_places=2, font_size=28, color=th.AMBER, unit=r"\,\mathrm{V}").move_to(cell.meter).shift(DOWN * 0.18)
        cell.meter[1].generate_target()
        cell.meter[1].target.scale(0.7).shift(UP * 0.22)
        an = VGroup(T("anode (−)", size=22, color=th.CORAL, weight="BOLD"), T("oxidation", size=18, color=th.BODY), chem(r"Zn \rightarrow Zn^{2+} + 2e^-", size=26)).arrange(DOWN, buff=0.06).move_to([-5.5, 1.3, 0])
        ca = VGroup(T("cathode (+)", size=22, color=th.MINT, weight="BOLD"), T("reduction", size=18, color=th.BODY), chem(r"Cu^{2+} + 2e^- \rightarrow Cu", size=26)).arrange(DOWN, buff=0.06).move_to([5.5, 1.3, 0])
        with self.say("The needle jumps: one point one zero volts. Zinc atoms lose electrons and dissolve as zinc ions. Zinc is the anode, where oxidation happens, and it is negative. The electrons flow through the wire to the copper, where copper ions pick them up and deposit as copper. Copper is the cathode, where reduction happens, and it is positive."):
            self.add(el)
            self.play(MoveToTarget(cell.meter[1]), FadeIn(rd), FadeIn(el))
            self.play(ph.animate.set_value(1), FadeIn(an), run_time=2.5, rate_func=linear)
            self.play(ph.animate.set_value(2), FadeIn(ca), run_time=2.5, rate_func=linear)
        bulb = VGroup(Circle(radius=0.3, fill_color=th.AMBER, fill_opacity=0.0, stroke_color=th.AMBER, stroke_width=3)).move_to([0, cell.top + 0.95, 0])
        with self.say("That is the cold open's dream come true. The same reaction, but the electrons are forced through a wire, where they can do work."):
            nb = C.show_neby(self, "celebrate", height=1.3, corner=DR)
            self.play(FadeIn(bulb))
            self.play(bulb[0].animate.set_fill(th.AMBER, opacity=0.9), ph.animate.set_value(3), cell.rl.animate.stretch(0.8, 0), cell.rr.animate.stretch(1.25, 0), run_time=2, rate_func=linear)
        C.hide_neby(self, nb)
        ions = VGroup()
        for k in range(3):
            ions.add(T("Cl⁻", size=18, color=th.MINT, weight="BOLD").move_to([-1.0 - 0.5 * k, cell.y + 1.5, 0]))
            ions.add(T("K⁺", size=18, color=th.AMBER, weight="BOLD").move_to([1.0 + 0.5 * k, cell.y + 1.5, 0]))
        jobs = VGroup(T("Salt bridge:", size=24, color="#E8E2C8", weight="BOLD"), T("1. completes the circuit", size=22, color=th.BODY), T("2. keeps both solutions neutral", size=22, color=th.BODY), T("3. stops the solutions mixing", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        jobs.to_corner(UL, buff=0.75).shift(DOWN * 0.3)
        self.play(FadeOut(an), FadeOut(ca))
        with self.say("Why the salt bridge? The zinc side keeps gaining positive zinc ions, and the copper side keeps losing positive copper ions. Charge would build up and stop the cell in a moment. The bridge sends negative chloride ions towards the zinc side and positive potassium ions towards the copper side. It completes the circuit, keeps both solutions neutral, and stops them mixing."):
            self.play(FadeIn(ions), FadeIn(jobs))
            self.play(*[i.animate.shift(LEFT * 1.4 + DOWN * 1.2) for i in ions[0::2]], *[i.animate.shift(RIGHT * 1.4 + DOWN * 1.2) for i in ions[1::2]], ph.animate.set_value(5), run_time=3, rate_func=linear)
        note = chem(r"Zn(s)\,|\,Zn^{2+}(1\,M)\,||\,Cu^{2+}(1\,M)\,|\,Cu(s)", size=40, color=th.AMBER)
        note.to_edge(UP, buff=0.7).shift(RIGHT * 1.6)
        nn = T("anode left · single bar: phase boundary · double bar: salt bridge", size=20, color=th.MUTED).next_to(note, DOWN, buff=0.1)
        with self.say("This is the Daniell cell. We write it with the anode on the left, a single bar for each phase boundary, and a double bar for the salt bridge."):
            self.play(FadeOut(jobs), FadeOut(bulb), Write(note), FadeIn(nn))
        self.play(FadeOut(VGroup(cell.static(), cell.circuit(), cell.bridge, cell.bl_lab, rd, bulb, ions, note, nn)), FadeOut(el))
        self.remove(el)
        cell2 = Cell(left=("Cu", CU, CUSO4, "CuSO₄"), right=("Ag", AG, "#E6E9F2", "AgNO₃"))
        ph2 = ValueTracker(0)
        el2 = always_redraw(lambda: cell2.electrons(ph2.get_value()))
        hdr = chem(r"Cu(s)\,|\,Cu^{2+}(1\,M)\,||\,Ag^+(1\,M)\,|\,Ag(s)", size=36, color=th.AMBER).to_edge(UP, buff=0.75)
        hs = VGroup(chem(r"Cu \rightarrow Cu^{2+} + 2e^-", size=26), chem(r"2Ag^+ + 2e^- \rightarrow 2Ag", size=26)).arrange(RIGHT, buff=4.4).next_to(hdr, DOWN, buff=0.25)
        tot = M(r"\mathrm{Cu + 2Ag^+ \rightarrow Cu^{2+} + 2Ag},\quad E^{\circ}_{cell} = 0.80 - 0.34 = 0.46\ \mathrm{V}", size=32, color=th.MINT).to_edge(DOWN, buff=0.35)
        with self.say("Swap in silver. In a silver copper cell, copper is now the more easily oxidised metal, so copper becomes the anode and silver the cathode. Copper dissolves, silver deposits, and the cell gives zero point four six volts."):
            self.play(FadeIn(cell2.static()), Create(cell2.wire), Create(cell2.wire2), FadeIn(cell2.meter), Create(cell2.bridge))
            self.add(el2)
            self.play(Write(hdr), FadeIn(el2))
            self.play(FadeIn(hs), ph2.animate.set_value(1.5), run_time=2, rate_func=linear)
            self.play(Write(tot))
        self.play(FadeOut(VGroup(cell2.static(), cell2.circuit(), cell2.bridge, hdr, hs, tot)), FadeOut(el2))
        self.remove(el2)
        care = self.callout("careful", "Never multiply E° by the stoichiometric number. The silver half-reaction was doubled, but E° stays +0.80 V: potential is energy per unit charge, an intensive property. Only ΔG scales with n.", width=11, size=27)
        with self.say("A trap. The silver half reaction had to be doubled to balance two electrons, but its E nought stays plus zero point eight zero. Electrode potential is energy per unit charge, so it does not depend on how much reaction you write. Only delta G scales with the number of electrons."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))
        rows = [["", "Galvanic cell", "Electrolytic cell"], ["energy", "chemical → electrical", "electrical → chemical"], ["reaction", "spontaneous, ΔG < 0", "driven, ΔG > 0"],
                ["anode", "negative, oxidation", "positive, oxidation"], ["cathode", "positive, reduction", "negative, reduction"], ["example", "Daniell cell, dry cell", "electroplating, Na and Al extraction"]]
        tb = C.table(rows, [2.2, 4.6, 5.4], row_h=0.64, size=24, colors=[th.MUTED, th.MINT, th.AMBER]).move_to(UP * 0.3)
        with self.say("Push current the other way with an outside source, and you drive a non spontaneous reaction. That is an electrolytic cell, used for electroplating and extracting sodium and aluminium. Notice: oxidation is always at the anode and reduction always at the cathode. Only the signs swap.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        d = M(r"E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode}", size=60, color=th.AMBER).to_edge(UP, buff=0.8)
        dn = T("both as standard reduction potentials · positive means spontaneous as written", size=24, color=th.MUTED).next_to(d, DOWN, buff=0.25)
        with self.say("The cell potential, or electromotive force, is the potential difference between the electrodes when no current flows. Under standard conditions, E nought cell equals E nought of the cathode minus E nought of the anode, both written as reduction potentials. If it comes out positive, the reaction runs as written. If negative, you have written the cell backwards."):
            self.play(Write(d))
            self.play(FadeIn(dn))
        nl = NumberLine(x_range=[-1.0, 1.0, 0.25], length=4.6, rotation=PI / 2, include_numbers=False, color=th.MUTED).move_to([-3.6, -1.2, 0])
        zt = VGroup(Dot(nl.n2p(-0.76), color=ZN), T("Zn  −0.76", size=30, color=ZN).next_to(nl.n2p(-0.76), LEFT, buff=0.2))
        ct = VGroup(Dot(nl.n2p(0.34), color=CU), T("Cu  +0.34", size=30, color=CU).next_to(nl.n2p(0.34), LEFT, buff=0.2))
        ht = VGroup(Dot(nl.n2p(0.0), color=th.AMBER), T("H  0.00", size=26, color=th.AMBER).next_to(nl.n2p(0.0), LEFT, buff=0.2))
        gap = DoubleArrow(nl.n2p(-0.76) + RIGHT * 0.4, nl.n2p(0.34) + RIGHT * 0.4, buff=0, color=th.MINT, stroke_width=4, tip_length=0.18)
        gl = M(r"0.34 - (-0.76) = 1.10\ \mathrm{V}", size=46, color=th.MINT).next_to(gap, RIGHT, buff=0.3)
        with self.say("Think of it as the gap between the two electrodes on the potential ladder. For the Daniell cell, copper at plus zero point three four is the cathode, zinc at minus zero point seven six is the anode. The gap is one point one zero volts."):
            self.play(Create(nl), FadeIn(ht), FadeIn(zt), FadeIn(ct))
            self.play(GrowFromCenter(gap), Write(gl))
        self.play(FadeOut(VGroup(dn, nl, zt, ct, ht, gap, gl)), d.animate.scale(0.7).to_edge(UP, buff=0.7))
        ne = M(r"E_{cell} = E^{\circ}_{cell} - \frac{0.0591}{n}\log Q \quad (298\ \mathrm{K})", size=50).next_to(d, DOWN, buff=0.4)
        nn = M(r"\frac{2.303RT}{F} = \frac{2.303 \times 8.314 \times 298}{96500} = 0.0591\ \mathrm{V}", size=34, color=th.MUTED).next_to(ne, DOWN, buff=0.3)
        with self.say("When concentrations are not one molar, the Nernst equation corrects the E M F: E cell equals E nought cell, minus zero point zero five nine one over n, times log Q. Pure solids and liquids do not appear in Q. The zero point zero five nine one is just two point three zero three R T over F, at twenty five degrees."):
            self.play(Write(ne))
            self.play(FadeIn(nn))
        self.play(FadeOut(nn))
        lq = ValueTracker(0)
        ax = Axes(x_range=[-3, 3, 1], y_range=[0.95, 1.25, 0.05], x_length=6.0, y_length=3.0, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 24}).move_to([-2.6, -1.2, 0])
        xl = T("log Q = log [Zn²⁺]/[Cu²⁺]", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.15)
        ln = ax.plot(lambda x: 1.10 - 0.0591 / 2 * x, x_range=[-3, 3], color=th.AMBER, stroke_width=4)
        dot = always_redraw(lambda: Dot(ax.c2p(lq.get_value(), 1.10 - 0.02955 * lq.get_value()), color=WHITE, radius=0.09))
        rd = DecimalNumber(1.10, num_decimal_places=3, font_size=48, color=th.AMBER, unit=r"\,\mathrm{V}")
        rd.add_updater(lambda m: m.set_value(1.10 - 0.02955 * lq.get_value()).move_to([3.6, -0.6, 0]))
        rl = T("EMF of Daniell cell", size=22, color=th.MUTED).move_to([3.6, 0.1, 0])
        with self.say("Watch the Daniell cell. As the cell runs, zinc ions pile up and copper ions are used, so Q rises, and the E M F slowly falls. Run it long enough, and Q reaches K, the E M F reaches zero, and the battery is flat."):
            self.play(Create(ax), FadeIn(xl), Create(ln), FadeIn(rl))
            self.add(dot, rd)
            self.play(FadeIn(dot), FadeIn(rd))
            self.play(lq.animate.set_value(3), run_time=3)
            self.play(lq.animate.set_value(-3), run_time=3)
            self.play(lq.animate.set_value(0), run_time=1)
        rd.clear_updaters()
        self.play(FadeOut(VGroup(d, ne, ax, xl, ln, rd, rl)), FadeOut(dot))
        self.remove(dot)
        head, prob = C.example_head(self, "Daniell cell, 298 K: E°(Zn²⁺/Zn) = −0.76 V, E°(Cu²⁺/Cu) = +0.34 V. Find E°cell, then the EMF when [Zn²⁺] = 0.10 M and [Cu²⁺] = 0.010 M.")
        st = C.steps(r"\text{cathode Cu, anode Zn}:\ E^{\circ}_{cell} = 0.34 - (-0.76) = 1.10\ \mathrm{V},\ n = 2",
                     r"Q = \frac{[\mathrm{Zn^{2+}}]}{[\mathrm{Cu^{2+}}]} = \frac{0.10}{0.010} = 10,\ \ \log Q = 1",
                     r"E = 1.10 - \frac{0.0591}{2}(1) = 1.10 - 0.0296 = 1.07\ \mathrm{V}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example five point one. Copper has the higher reduction potential, so it is the cathode. E nought cell is zero point three four minus minus zero point seven six, one point one zero volts. Two electrons transfer."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Q is zinc ion over copper ion, the solids left out: zero point one over zero point zero one, ten. Log Q is one. So E is one point one zero minus zero point zero two nine six, about one point zero seven volts. More product ions, lower E M F, just as Le Chatelier predicts."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.tip("Put the PRODUCTS of the cell reaction on top of Q. Q > 1 lowers the EMF below E°; Q < 1 raises it.",
                 "To get the Nernst sign right every time, put the products of the cell reaction on top of Q. If Q is greater than one, the log is positive and the E M F drops below E nought. If Q is less than one, it rises above.", state="wink")

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        f = VGroup(M(r"F = N_A\,e = (6.022\times10^{23})(1.602\times10^{-19}) \approx 96\,500\ \mathrm{C\,mol^{-1}}", size=38),
                   T("one faraday: the charge on one mole of electrons", size=24, color=th.MUTED)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.8)
        with self.say("The electrical work a cell delivers is charge times potential difference. The charge on one mole of electrons is the Faraday constant, F: Avogadro's number times the electron's charge, about ninety six thousand five hundred coulombs per mole."):
            self.play(Write(f[0]), FadeIn(f[1]))
        der = VGroup(M(r"w_{max} = \Delta G", size=40), M(r"\text{electrical work done by the cell} = nFE_{cell}", size=40),
                     M(r"\Delta G = -nFE_{cell},\qquad \Delta G^{\circ} = -nFE^{\circ}_{cell}", size=50, color=th.AMBER)).arrange(DOWN, buff=0.35).next_to(f, DOWN, buff=0.5)
        with self.say("From Unit 4, the maximum useful work a process can deliver equals delta G. A cell pushing n moles of electrons through a potential E does n F E of work on the surroundings. Work done by the system is negative, so delta G equals minus n F E."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
            self.sfx("impact", gain=-12)
            self.play(Write(der[2]))
        k = VGroup(M(r"-nFE^{\circ} = -2.303RT\log K", size=40), M(r"\log K = \frac{nE^{\circ}_{cell}}{0.0591}\quad(298\ \mathrm{K})", size=46, color=th.MINT)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.say("And since delta G nought is also minus two point three zero three R T log K, we get log K equals n E nought over zero point zero five nine one. So a positive E M F means negative delta G, a spontaneous reaction, and a large E M F means a huge equilibrium constant."):
            self.play(FadeOut(f), der.animate.shift(UP * 0.8))
            self.play(Write(k[0]))
            self.play(Write(k[1]))
        self.play(FadeOut(VGroup(der, k)))
        tri = VGroup(*[RoundedRectangle(corner_radius=0.2, width=2.4, height=1.0, fill_color=th.PANEL, fill_opacity=1, stroke_color=c, stroke_width=3).move_to(p)
                       for p, c in (([0, 1.8, 0], th.AMBER), ([-3.4, -1.6, 0], th.SKY), ([3.4, -1.6, 0], th.MINT))])
        tl = VGroup(M(r"\Delta G^{\circ}", size=40, color=th.AMBER).move_to(tri[0]), M(r"E^{\circ}_{cell}", size=40, color=th.SKY).move_to(tri[1]), M("K", size=44, color=th.MINT).move_to(tri[2]))
        e1 = Line(tri[0].get_bottom() + LEFT * 0.4, tri[1].get_top(), color=th.FAINT, stroke_width=3)
        e2 = Line(tri[0].get_bottom() + RIGHT * 0.4, tri[2].get_top(), color=th.FAINT, stroke_width=3)
        e3 = Line(tri[1].get_right(), tri[2].get_left(), color=th.FAINT, stroke_width=3)
        l1 = M(r"-nFE^{\circ}", size=30).next_to(e1.get_center(), LEFT, buff=0.2)
        l2 = M(r"-2.303RT\log K", size=30).next_to(e2.get_center(), RIGHT, buff=0.2)
        l3 = M(r"\log K = nE^{\circ}/0.0591", size=30).next_to(e3, DOWN, buff=0.2)
        with self.say("Three quantities, all tied together. Know any one of free energy, cell potential or equilibrium constant, and you can find the other two."):
            self.play(FadeIn(tri), FadeIn(tl))
            self.play(Create(e1), FadeIn(l1), Create(e2), FadeIn(l2), Create(e3), FadeIn(l3))
        self.play(FadeOut(VGroup(tri, tl, e1, e2, e3, l1, l2, l3)))
        head, prob = C.example_head(self, "For Cu | Cu²⁺(1 M) || Ag⁺(1 M) | Ag, E°(Cu²⁺/Cu) = +0.34 V, E°(Ag⁺/Ag) = +0.80 V. Find E°cell, ΔG° and K at 298 K.")
        st = C.steps(r"\mathrm{Cu + 2Ag^+ \rightarrow Cu^{2+} + 2Ag},\ n = 2,\ E^{\circ}_{cell} = 0.80 - 0.34 = 0.46\ \mathrm{V}",
                     r"\Delta G^{\circ} = -(2)(96500)(0.46) = -88\,780\ \mathrm{J} = -88.8\ \mathrm{kJ\,mol^{-1}}",
                     r"\log K = \frac{2 \times 0.46}{0.0591} = 15.57 \Rightarrow K = 3.7\times10^{15}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.MINT)
        with self.say("Worked example five point two. The silver copper cell: two electrons, E nought of zero point four six volts. Delta G nought is minus two times ninety six thousand five hundred times zero point four six, minus eighty eight point eight kilojoules per mole."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Log K is two times zero point four six over zero point zero five nine one, fifteen point five seven. So K is three point seven times ten to the fifteen. Copper reduces silver ions essentially completely, which is why a copper wire left in silver nitrate grows shining silver crystals."):
            nb = C.show_neby(self, "surprised", height=1.3, corner=DR)
            self.play(Write(st[2]))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "The EMF of Zn | Zn²⁺(1 M) || H⁺(?) | H₂(1 bar), Pt is 0.5827 V at 298 K. E°(Zn²⁺/Zn) = −0.76 V. Find the pH of the acid.")
        st = C.steps(r"\mathrm{Zn + 2H^+ \rightarrow Zn^{2+} + H_2},\ n = 2,\ E^{\circ} = 0.00 - (-0.76) = 0.76\ \mathrm{V}",
                     r"E = 0.76 - \frac{0.0591}{2}\log\frac{1}{[\mathrm{H^+}]^{2}} = 0.76 - 0.0591\,\mathrm{pH}",
                     r"\mathrm{pH} = \frac{0.76 - 0.5827}{0.0591} = \frac{0.1773}{0.0591} = 3.00", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        nb = C.show_neby(self, "think", height=1.3)
        with self.say("Worked example five point three: measuring p H with a cell. Zinc against a hydrogen electrode in an acid of unknown strength. E nought is zero point seven six volts, and two electrons transfer."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("In the Nernst equation, log of one over hydrogen ion squared is two p H. So E equals zero point seven six minus zero point zero five nine one times p H. Solve: zero point one seven seven three over zero point zero five nine one, p H three. That is exactly how a p H meter works, with glass and calomel electrodes."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            nb.set_state("success", once=True)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))
        self.faraday()

    def faraday(self):
        title = T("Faraday's laws of electrolysis", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        laws = VGroup(VGroup(T("First law", size=26, color=th.AMBER, weight="BOLD"), M(r"m = Z\,i\,t,\quad Q = it", size=40)).arrange(RIGHT, buff=0.5),
                      VGroup(T("Second law", size=26, color=th.AMBER, weight="BOLD"), T("same charge → masses in ratio of equivalent weights", size=24, color=th.BODY)).arrange(RIGHT, buff=0.5),
                      T("1 faraday (96 500 C) deposits one gram-equivalent: molar mass ÷ n grams", size=26, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.4)
        with self.say("The same constant governs electrolysis. Faraday's first law: the mass deposited is proportional to the charge passed, current times time. His second law: the same charge deposits masses in the ratio of their equivalent weights. In practice, one faraday deposits one gram equivalent, molar mass over n grams."):
            self.play(FadeIn(title))
            for l in laws:
                self.play(FadeIn(l, shift=RIGHT * 0.2))
        self.play(FadeOut(laws))
        bk = C.Beaker(center=[-3.4, -1.2, 0], w=3.4, h=2.6, level=0.75, color=CUSO4, opacity=0.5)
        cath = Rectangle(width=0.3, height=2.4, fill_color="#5A6070", fill_opacity=1, stroke_width=0).move_to([-4.4, -0.6, 0])
        anod = Rectangle(width=0.3, height=2.4, fill_color="#5A6070", fill_opacity=1, stroke_width=0).move_to([-2.4, -0.6, 0])
        plate = Rectangle(width=0.36, height=1.6, fill_color=CU, fill_opacity=0, stroke_width=0).move_to([-4.4, -1.4, 0])
        lab = VGroup(T("cathode: Cu²⁺ + 2e⁻ → Cu", size=18, color=CU).next_to(cath, UP, buff=0.15).shift(LEFT * 0.4), T("anode: O₂ bubbles", size=18, color=th.SKY).next_to(anod, UP, buff=0.15).shift(RIGHT * 0.5))
        bt = ValueTracker(0)
        bub = always_redraw(lambda: VGroup(*[Circle(radius=0.05, stroke_color=WHITE, stroke_width=2).move_to([-2.2 + 0.1 * np.sin(3 * k), -2.0 + ((bt.get_value() + k / 6) % 1) * 1.6, 0]) for k in range(6)]))
        st = C.steps(r"Q = it = 5.0 \times 1800 = 9000\ \mathrm{C}",
                     r"n(e^-) = \frac{9000}{96500} = 0.09326\ \mathrm{mol}",
                     r"\mathrm{Cu}: \frac{0.09326}{2} \times 63.5 = 2.96\ \mathrm{g}",
                     r"\mathrm{O_2}: \frac{0.09326}{4} \times 22400 = 522\ \mathrm{cm^3}", size=36).move_to([2.8, -0.6, 0])
        st[2].set_color(CU)
        st[3].set_color(th.SKY)
        prob = T("5.0 A for 30 min through CuSO₄, inert electrodes", size=24, color=th.INK).next_to(title, DOWN, buff=0.3)
        with self.say("Worked example five point four. Five amperes for thirty minutes through copper sulphate. The charge is five times eighteen hundred seconds, nine thousand coulombs, which is zero point zero nine three three moles of electrons."):
            self.play(FadeIn(prob), FadeIn(bk.g), FadeIn(cath), FadeIn(anod), FadeIn(lab))
            self.add(plate, bub)
            self.play(Write(st[0]), bt.animate.set_value(1), run_time=1.5, rate_func=linear)
            self.play(Write(st[1]), bt.animate.set_value(2), run_time=1.5, rate_func=linear)
        with self.say("Each copper ion needs two electrons, so we get half that many moles of copper, times sixty three point five: two point nine six grams on the cathode. Each oxygen molecule releases four electrons, so a quarter as many moles, times twenty two thousand four hundred: five hundred and twenty two cubic centimetres of oxygen at S T P."):
            self.play(Write(st[2]), plate.animate.set_fill(CU, opacity=0.9), bk.liq.animate.set_fill("#7FA9D6", opacity=0.4), bt.animate.set_value(3), run_time=2, rate_func=linear)
            self.play(Write(st[3]), bt.animate.set_value(4), run_time=2, rate_func=linear)
        self.play(FadeOut(VGroup(title, prob, bk.g, cath, anod, plate, lab, st)), FadeOut(bub))
        self.remove(bub)

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        rows = [["Battery", "Anode", "Cathode", "Electrolyte", "EMF", "Type"],
                ["dry (Leclanché)", "Zn can", "C rod in MnO₂", "NH₄Cl + ZnCl₂ paste", "≈1.5 V", "primary"],
                ["lead storage", "Pb", "PbO₂", "38 % H₂SO₄", "2.0 V/cell", "secondary"],
                ["nickel–cadmium", "Cd", "NiO(OH)", "KOH", "≈1.2 V", "secondary"],
                ["lithium-ion", "graphite + Li", "LiCoO₂", "Li salt, organic", "≈3.7 V", "secondary"]]
        tb = C.table(rows, [2.6, 1.9, 2.2, 3.0, 1.5, 1.6], row_h=0.66, size=22, colors=[th.AMBER, th.CORAL, th.MINT, th.BODY, th.INK, th.MUTED]).move_to(UP * 0.5)
        with self.say("A battery is one or more galvanic cells packaged for use. Primary cells cannot be recharged, because their reactions are not reversible. Secondary cells, or accumulators, can. Here are the four you should know: the dry cell, the lead storage battery, nickel cadmium, and lithium ion, the one in your phone at about three point seven volts.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(tb))
        can = Rectangle(width=2.0, height=3.4, fill_color=ZN, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2).move_to([-4.0, -0.6, 0])
        paste = Rectangle(width=1.6, height=3.0, fill_color="#3A3F52", fill_opacity=1, stroke_width=0).move_to(can)
        mno = Rectangle(width=0.9, height=2.6, fill_color="#25262B", fill_opacity=1, stroke_width=0).move_to(can)
        rod = Rectangle(width=0.22, height=3.2, fill_color="#555A66", fill_opacity=1, stroke_width=0).move_to(can.get_center() + UP * 0.2)
        cap = Rectangle(width=0.4, height=0.2, fill_color=th.INK, fill_opacity=1, stroke_width=0).next_to(rod, UP, buff=0)
        dl = VGroup(T("zinc can: anode", size=20, color=ZN), T("NH₄Cl/ZnCl₂ paste", size=20, color=th.BODY), T("MnO₂ + carbon", size=20, color=th.MUTED), T("graphite rod: cathode", size=20, color=th.INK))
        dl.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(can, RIGHT, buff=0.4)
        eqs = VGroup(chem(r"Zn \rightarrow Zn^{2+} + 2e^-", size=30), chem(r"2MnO_2 + 2NH_4^+ + 2e^- \rightarrow Mn_2O_3 + 2NH_3 + H_2O", size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.8)
        with self.say("The dry cell, inside every torch. The zinc can itself is the anode, slowly eaten away. A graphite rod in a mixture of manganese dioxide and carbon is the cathode, and a moist paste of ammonium chloride and zinc chloride is the electrolyte. It gives about one and a half volts, and dies as the zinc is consumed and ammonia collects round the cathode."):
            self.play(FadeIn(can), FadeIn(paste), FadeIn(mno), FadeIn(rod), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.2) for d in dl], lag_ratio=0.3))
            self.play(Write(eqs))
        self.play(FadeOut(VGroup(can, paste, mno, rod, cap, dl, eqs)))
        self.lead_acid()
        self.fuel_cell()
        self.quiz("In a hydrogen–oxygen fuel cell, the only chemical product is",
                  ["CO₂", "H₂O", "H₂O₂", "NO₂"], 1,
                  "Last one. What comes out of a hydrogen oxygen fuel cell? Pause and think.",
                  "B, water. Hydrogen is oxidised at the anode and oxygen reduced at the cathode, and the overall reaction is two hydrogen plus oxygen giving two water. No carbon, so no carbon dioxide, and no smoke.")

    def lead_acid(self):
        title = T("Lead storage battery", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        dis = ValueTracker(0)
        box = Rectangle(width=4.0, height=3.4, stroke_color=th.INK, stroke_width=3).move_to([-3.4, -0.8, 0])
        acid = always_redraw(lambda: Rectangle(width=3.9, height=3.0, stroke_width=0, fill_color=interpolate_color(ManimColor("#F2D43C"), ManimColor(C.WATER), dis.get_value()), fill_opacity=0.25).move_to([-3.4, -1.0, 0]))
        pb = Rectangle(width=0.5, height=2.8, fill_color="#7A808F", fill_opacity=1, stroke_width=0).move_to([-4.4, -0.7, 0])
        pbo = Rectangle(width=0.5, height=2.8, fill_color="#6B3A2A", fill_opacity=1, stroke_width=0).move_to([-2.4, -0.7, 0])
        coat = always_redraw(lambda: VGroup(Rectangle(width=0.62, height=2.8 * dis.get_value() + 0.01, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).align_to(pb, DOWN).set_x(-4.4),
                                            Rectangle(width=0.62, height=2.8 * dis.get_value() + 0.01, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).align_to(pbo, DOWN).set_x(-2.4)))
        pl = VGroup(T("Pb (anode)", size=20, color=th.MUTED).next_to(box, UP, buff=0.12).align_to(box, LEFT), T("PbO₂ (cathode)", size=20, color="#C9805F").next_to(box, UP, buff=0.12).align_to(box, RIGHT))
        eqs = VGroup(chem(r"Pb + SO_4^{2-} \rightarrow PbSO_4 + 2e^-", size=28),
                     chem(r"PbO_2 + SO_4^{2-} + 4H^+ + 2e^- \rightarrow PbSO_4 + 2H_2O", size=28),
                     chem(r"Pb + PbO_2 + 2H_2SO_4 \rightleftharpoons 2PbSO_4 + 2H_2O", size=32, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.8, 0.6, 0])
        dens = DecimalNumber(1.28, num_decimal_places=2, font_size=36, color=th.AMBER)
        dens.add_updater(lambda m: m.set_value(1.28 - 0.13 * dis.get_value()).move_to([3.4, -2.2, 0]))
        dl = T("acid density (g cm⁻³)", size=20, color=th.MUTED).next_to([3.4, -2.2, 0], LEFT, buff=0.8)
        with self.say("The lead storage battery, in every car and in the inverters that keep Nepali homes lit during load shedding. A lead plate is the anode, lead dioxide the cathode, both in about thirty eight percent sulphuric acid. On discharge, both plates turn into lead sulphate, and the sulphuric acid is used up, turning to water."):
            self.play(FadeIn(title), Create(box))
            self.add(acid, coat, dens)
            self.play(FadeIn(acid), FadeIn(pb), FadeIn(pbo), FadeIn(pl), FadeIn(dens), FadeIn(dl))
            self.add(coat)
            self.play(Write(eqs[0]), Write(eqs[1]))
            self.play(dis.animate.set_value(1), Write(eqs[2]), run_time=3)
        with self.say("To recharge it, push current the other way. The reaction reverses, rebuilding lead and lead dioxide and restoring the acid. Since the acid's density falls on discharge, a hydrometer tells you how charged the battery is."):
            self.play(dis.animate.set_value(0), run_time=3)
        dens.clear_updaters()
        self.play(FadeOut(VGroup(title, box, pb, pbo, pl, eqs, dens, dl)), FadeOut(acid), FadeOut(coat))
        self.remove(acid, coat)

    def fuel_cell(self):
        title = T("Hydrogen–oxygen fuel cell", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        an = Rectangle(width=0.4, height=3.0, fill_color="#5A6070", fill_opacity=1, stroke_width=0).move_to([-1.6, -0.1, 0])
        ca = Rectangle(width=0.4, height=3.0, fill_color="#5A6070", fill_opacity=1, stroke_width=0).move_to([1.6, -0.1, 0])
        el = Rectangle(width=2.8, height=3.0, fill_color=th.SKY, fill_opacity=0.15, stroke_width=0).move_to([0, -0.1, 0])
        ell = T("KOH(aq)", size=22, color=th.SKY).move_to([0, -0.1, 0])
        wire = VMobject(stroke_color=th.INK, stroke_width=3).set_points_as_corners([an.get_top(), [-1.6, 2.0, 0], [1.6, 2.0, 0], ca.get_top()])
        bulb = Circle(radius=0.3, fill_color=th.AMBER, fill_opacity=0.9, stroke_color=th.AMBER).move_to([0, 2.0, 0])
        t = ValueTracker(0)
        h2 = always_redraw(lambda: VGroup(*[VGroup(C.atom("H", r=0.13), C.atom("H", r=0.13).shift(RIGHT * 0.24)).move_to([-5.0 + ((t.get_value() + k / 4) % 1) * 3.0, -1.2 + 0.7 * k, 0]) for k in range(4)]))
        o2 = always_redraw(lambda: VGroup(*[VGroup(C.atom("O", r=0.15), C.atom("O", r=0.15).shift(RIGHT * 0.28)).move_to([5.0 - ((t.get_value() + k / 4) % 1) * 3.0, -1.2 + 0.7 * k, 0]) for k in range(4)]))
        es = always_redraw(lambda: VGroup(*[Dot([-1.6 + ((t.get_value() * 2 + k / 6) % 1) * 3.2, 2.0, 0], radius=0.07, color=th.SKY) for k in range(6) if abs(-1.6 + ((t.get_value() * 2 + k / 6) % 1) * 3.2) > 0.35]))
        lab = VGroup(T("H₂ in", size=24, color=th.INK).move_to([-4.2, 1.2, 0]), T("O₂ in", size=24, color=C.EL["O"]).move_to([4.2, 1.2, 0]), T("H₂O out", size=22, color=C.WATER).move_to([0, -1.95, 0]))
        eqs = VGroup(chem(r"\text{anode: } 2H_2 + 4OH^- \rightarrow 4H_2O + 4e^-", size=28), chem(r"\text{cathode: } O_2 + 2H_2O + 4e^- \rightarrow 4OH^-", size=28),
                     chem(r"2H_2 + O_2 \rightarrow 2H_2O,\quad E^{\circ} = 1.23\ V", size=32, color=th.AMBER))
        with self.say("Finally, the fuel cell. Unlike a battery, its reactants are fed in continuously from outside, so it never runs down. Hydrogen flows past the anode, oxygen past the cathode, with potassium hydroxide between them. This is the cell that powered the Apollo spacecraft."):
            self.play(FadeIn(title), FadeIn(el), FadeIn(ell), FadeIn(an), FadeIn(ca), Create(wire), FadeIn(bulb))
            self.add(h2, o2, es)
            self.play(FadeIn(lab), t.animate.set_value(2), run_time=4, rate_func=linear)
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        self.play(FadeOut(lab[2]), run_time=0.3)
        with self.say("Hydrogen is oxidised at the anode, oxygen is reduced at the cathode, and the overall reaction is hydrogen plus oxygen giving water, at one point two three volts. The only product is drinkable water."):
            nb = C.show_neby(self, "love", height=1.3, corner=DR)
            self.play(LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.5), t.animate.set_value(4), run_time=4, rate_func=linear)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, an, ca, el, ell, wire, bulb, lab[:2], eqs)), FadeOut(h2), FadeOut(o2), FadeOut(es))
        self.remove(h2, o2, es)
        pros = C.card(self, "Advantages", "70–75 % efficient (a thermal power station manages about 40 %); no smoke, no NOx or SO₂; only water; runs as long as fuel is fed.", w=5.6, h=3.0, color=th.MINT, bsize=23)
        cons = C.card(self, "Disadvantages", "the platinum catalyst is expensive; hydrogen is hard to store and transport safely.", w=5.6, h=3.0, color=th.CORAL, bsize=23)
        VGroup(pros, cons).arrange(RIGHT, buff=0.4)
        with self.say("Its advantages: seventy to seventy five percent efficiency, against about forty percent for a thermal power station, because the energy never has to become heat first. No smoke, no oxides of nitrogen or sulphur. Its drawbacks: expensive platinum catalysts, and hydrogen that is hard to store and transport safely."):
            self.play(FadeIn(pros, shift=UP * 0.2))
            self.play(FadeIn(cons, shift=UP * 0.2))
        self.play(FadeOut(VGroup(pros, cons)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Electrode potential: the p.d. at a metal–solution boundary. Tables list reduction potentials, vs SHE = 0.000 V.",
            "SHE: Pt, 1 M H⁺, H₂ at 1 bar (primary). Calomel: Hg | Hg₂Cl₂ | KCl, +0.242 V saturated (secondary).",
            "Electrochemical series: more negative E° = stronger reducing agent; metals above H release H₂ from acids.",
            "Zn | Zn²⁺ || Cu²⁺ | Cu: anode Zn (−, oxidation), cathode Cu (+, reduction), 1.10 V; salt bridge completes the circuit.",
            M(r"E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode};\quad E = E^{\circ} - \tfrac{0.0591}{n}\log Q", size=38),
            M(r"\Delta G^{\circ} = -nFE^{\circ},\quad \log K = \tfrac{nE^{\circ}}{0.0591};\quad m = \tfrac{Q}{96500}\cdot\tfrac{M}{n}", size=38),
            "Dry cell (primary), lead storage (secondary), H₂–O₂ fuel cell: 1.23 V, only water, 70–75 % efficient.",
        ], "Let us recap. Every electrode has a potential, measured as a reduction potential against the standard hydrogen electrode, or in practice against calomel. The electrochemical series ranks reducing and oxidising power. In a voltaic cell, oxidation happens at the negative anode, reduction at the positive cathode, and a salt bridge closes the circuit. E nought cell is cathode minus anode, corrected by the Nernst equation. Delta G is minus n F E, which links cell potential to the equilibrium constant, and one faraday deposits one gram equivalent. And batteries and fuel cells put all of it to work.")
        self.outro("That is electrochemistry, and the end of physical chemistry for Class 12. Next, we move to inorganic chemistry, starting with the transition metals: their colours, complexes and catalytic power. See you in the next lesson on NEBians.")
