import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402


def thermometer(x, y, h=3.0, getter=None, lo=0, hi=40, color=th.CORAL):
    tube = RoundedRectangle(corner_radius=0.09, width=0.18, height=h, stroke_color=th.INK, stroke_width=2).move_to([x, y, 0])
    bulb = Circle(radius=0.2, fill_color=color, fill_opacity=1, stroke_color=th.INK, stroke_width=2).move_to(tube.get_bottom() + DOWN * 0.08)

    def col():
        v = getter() if getter else lo
        f = np.clip((v - lo) / (hi - lo), 0.02, 1)
        hh = (h - 0.2) * f
        return Rectangle(width=0.09, height=hh, fill_color=color, fill_opacity=1, stroke_width=0).move_to(tube.get_bottom() + UP * (0.1 + hh / 2))
    return VGroup(tube, bulb), always_redraw(col)


def level_bar(x, y0, y1, color, label, w=1.6, size=22):
    g = VGroup(Line([x - w / 2, y1, 0], [x + w / 2, y1, 0], color=color, stroke_width=6))
    g.add(T(label, size=size, color=color).next_to(g[0], UP, buff=0.08))
    return g


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 4
    TITLE = "Thermodynamics"
    SUBTITLE = "Energy, entropy and the direction of change"
    SECTIONS = ["Energy in chemical reactions", "Internal energy", "First law", "Enthalpy: endo and exo",
                "Enthalpies of reaction", "Laplace and Hess's laws", "Entropy and spontaneity", "Second law",
                "Gibbs free energy", "ΔG and equilibrium constant"]
    NEXT = "Unit 5 · Electrochemistry"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.p9, self.p10, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        Tt = ValueTracker(25.0)
        bk = C.Beaker(center=[-2.4, -1.0, 0], w=2.6, h=2.8, level=0.6, color=C.WATER, opacity=0.3)
        tg, tc = thermometer(-0.4, -0.2, h=3.4, getter=Tt.get_value, lo=0, hi=40, color=th.SKY)
        rd = DecimalNumber(25.0, num_decimal_places=1, font_size=60, color=th.SKY, unit=r"^{\circ}\mathrm{C}")
        rd.add_updater(lambda m: m.set_value(Tt.get_value()).move_to([3.2, 0.6, 0]))
        lab = T("water", size=24, color=th.MUTED).next_to(bk.g, DOWN, buff=0.2)
        salt = VGroup(*[Square(side_length=0.14, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to([-2.4 + 0.25 * (i - 4), 2.6 + 0.1 * (i % 3), 0]) for i in range(9)])
        sl = chem(r"NH_4Cl(s)", size=34).next_to(salt, RIGHT, buff=0.4)
        with self.say("A beaker of water at twenty five degrees, and a spoonful of ammonium chloride. This is the inside of an instant cold pack, the kind a doctor presses on a sprained ankle."):
            self.play(FadeIn(bk.g), FadeIn(lab), FadeIn(tg))
            self.add(tc, rd)
            self.play(FadeIn(tc), FadeIn(rd), FadeIn(salt), FadeIn(sl))
        with self.say("Tip it in. It dissolves all by itself, and the temperature falls. Twenty, fifteen, below twelve."):
            self.play(salt.animate.move_to(bk.c + DOWN * 0.4).set_opacity(0), FadeOut(sl), run_time=1.0)
            self.play(Tt.animate.set_value(11.5), bk.liq.animate.set_fill(th.SKY, opacity=0.45), run_time=4.0, rate_func=smooth)
        nb = C.show_neby(self, "surprised", height=1.5, at=[3.2, -1.6, 0])
        q = para("It absorbs heat, yet it happens on its own. Why?", width=6.0, size=30, color=th.INK).move_to([3.0, 2.5, 0])
        with self.say("Wait. We usually think things happen on their own when they release energy, like a ball rolling downhill. This one sucks energy in from its surroundings, and still goes, all by itself. Why? Energy alone cannot be the whole story. By the end of this lesson you will know the second driving force of all chemistry."):
            self.play(FadeIn(q, shift=UP * 0.2))
        C.hide_neby(self, nb)
        rd.clear_updaters()
        self.play(FadeOut(VGroup(bk.g, lab, tg, rd, q, salt)), FadeOut(tc))
        self.remove(tc)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 4: Thermodynamics. The study of energy changes in chemistry: heat and work, enthalpy and entropy, and the free energy that decides which way a reaction can go."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. Energy in reactions, internal energy and the first law. Enthalpy, and the different enthalpy changes. Laplace's law and Hess's law. Then entropy, the second law, Gibbs free energy, and finally how free energy fixes the equilibrium constant.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        d = T("System: the part under study.  Surroundings: everything else.", size=28, color=th.INK).to_edge(UP, buff=0.8)
        with self.say("Thermodynamics studies energy changes in bulk matter, using measurable properties like pressure, volume and temperature. It says nothing about speed, and nothing about individual molecules. First, two words. The system is the part of the universe we are studying. The surroundings are everything else."):
            self.play(FadeIn(d))
        xs = [-4.4, 0, 4.4]
        cup = VGroup(Line([-0.8, 0.6, 0], [-0.7, -0.9, 0], color=th.INK, stroke_width=4), Line([-0.7, -0.9, 0], [0.7, -0.9, 0], color=th.INK, stroke_width=4), Line([0.7, -0.9, 0], [0.8, 0.6, 0], color=th.INK, stroke_width=4),
                     Rectangle(width=1.4, height=1.1, fill_color="#C08040", fill_opacity=0.7, stroke_width=0).move_to([0, -0.35, 0])).move_to([xs[0], -0.6, 0])
        bulb = VGroup(Circle(radius=0.9, stroke_color=th.INK, stroke_width=4, fill_color=th.AMBER, fill_opacity=0.2)).move_to([xs[1], -0.6, 0])
        flask = VGroup(RoundedRectangle(corner_radius=0.3, width=1.6, height=2.0, stroke_color=th.INK, stroke_width=6, fill_color=th.CORAL, fill_opacity=0.2),
                       RoundedRectangle(corner_radius=0.25, width=1.3, height=1.7, stroke_color=th.MUTED, stroke_width=2)).move_to([xs[2], -0.6, 0])
        names = VGroup(*[VGroup(T(a, size=28, color=c, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([x, -2.6, 0])
                         for x, a, b, c in zip(xs, ["Open", "Closed", "Isolated"], ["matter and energy cross", "only energy crosses", "nothing crosses"], [th.AMBER, th.SKY, th.CORAL])])
        steam = VGroup(*[Dot([xs[0] + 0.3 * (k - 2), 0.3, 0], radius=0.06, color=WHITE, fill_opacity=0.7) for k in range(5)])
        heat1 = VGroup(*[Arrow([xs[0] + 1.0, -0.6 + 0.3 * k, 0], [xs[0] + 1.8, -0.6 + 0.3 * k, 0], buff=0, color=th.CORAL, stroke_width=3) for k in range(2)])
        heat2 = VGroup(*[Arrow([xs[1] + 1.0, -0.6 + 0.3 * k, 0], [xs[1] + 1.8, -0.6 + 0.3 * k, 0], buff=0, color=th.CORAL, stroke_width=3) for k in range(2)])
        with self.say("A system can be open, like tea in an open cup: steam, which is matter, and heat both escape. Closed, like a reaction in a sealed glass bulb: heat can cross, matter cannot. Or isolated, like hot water in a perfect thermos flask: nothing crosses at all."):
            self.play(FadeIn(cup), FadeIn(names[0]))
            self.play(steam.animate.shift(UP * 1.4).set_opacity(0), GrowArrow(heat1[0]), GrowArrow(heat1[1]))
            self.play(FadeIn(bulb), FadeIn(names[1]))
            self.play(GrowArrow(heat2[0]), GrowArrow(heat2[1]))
            self.play(FadeIn(flask), FadeIn(names[2]))
            self.play(Indicate(flask, color=th.CORAL))
        self.play(FadeOut(VGroup(d, cup, bulb, flask, names, steam, heat1, heat2)))
        # state vs path function
        title = T("State functions and path functions", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        base = Polygon([-6, -2.8, 0], [-1.0, 2.0, 0], [3.5, -2.8, 0], fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3)
        a, b = np.array([-4.5, -2.4, 0]), np.array([-1.0, 2.0, 0])
        p1 = Line(a, b, color=th.SKY, stroke_width=5)
        p2 = VMobject(color=th.AMBER, stroke_width=5).set_points_smoothly([a, [-3.0, -1.6, 0], [0.4, -1.0, 0], [-2.2, 0.2, 0], [0.2, 0.9, 0], b])
        h = DoubleArrow([1.4, -2.4, 0], [1.4, 2.0, 0], buff=0, color=th.MINT, stroke_width=4)
        hl = T("height gained: same", size=24, color=th.MINT).next_to(h, RIGHT, buff=0.15)
        txt = VGroup(T("State functions: p, V, T, U, H, S, G", size=26, color=th.MINT), T("Path functions: heat q, work w", size=26, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 1.7, 0])
        with self.say("Climb from a village to a hilltop. Take the steep direct path, or the long winding trail. The height you gain is the same either way: it depends only on where you start and end. The distance you walk depends on the route."):
            self.play(FadeIn(title), FadeIn(base))
            self.play(Create(p1))
            self.play(Create(p2), run_time=1.5)
            self.play(GrowFromCenter(h), FadeIn(hl))
        with self.say("Properties like height are state functions: pressure, volume, temperature, internal energy, enthalpy, entropy and free energy. Heat and work are like the distance walked. They are path functions."):
            self.play(FadeIn(txt, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, base, p1, p2, h, hl, txt)))
        rows = [["Process", "Held constant", "Consequence"], ["isothermal", "temperature", "ΔT = 0"], ["isobaric", "pressure", "Δp = 0"],
                ["isochoric", "volume", "ΔV = 0, so w = 0"], ["adiabatic", "no heat exchange", "q = 0"], ["cyclic", "returns to start", "ΔU = 0, ΔH = 0"]]
        tb = C.table(rows, [3.0, 3.6, 4.0], row_h=0.62, size=25, colors=[th.AMBER, th.INK, th.BODY]).move_to(UP * 0.3)
        with self.say("And five kinds of process. Isothermal, constant temperature. Isobaric, constant pressure. Isochoric, constant volume, so no expansion work. Adiabatic, no heat exchanged. And cyclic, returning to the start, so every state function change is zero.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))
        self.bond_energy()

    def bond_energy(self):
        title = T("Where the energy comes from: bonds", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"H_2 + Cl_2 \rightarrow 2HCl", size=40).next_to(title, DOWN, buff=0.25)
        y0 = -1.4
        sc = 0.0038
        start = Line([-5.6, y0, 0], [-3.4, y0, 0], color=th.SKY, stroke_width=6)
        sl = VGroup(chem(r"H_2 + Cl_2", size=30, color=th.SKY)).next_to(start, DOWN, buff=0.15)
        top_y = y0 + 678 * sc
        top = Line([-2.2, top_y, 0], [0.2, top_y, 0], color=th.AMBER, stroke_width=6)
        tl = chem(r"2H + 2Cl", size=30, color=th.AMBER).next_to(top, UP, buff=0.15)
        end_y = y0 - 184 * sc
        end = Line([1.4, end_y, 0], [3.6, end_y, 0], color=th.MINT, stroke_width=6)
        el = chem(r"2HCl", size=30, color=th.MINT).next_to(end, DOWN, buff=0.15)
        up = Arrow([-2.9, y0, 0], [-2.9, top_y, 0], buff=0, color=th.CORAL, stroke_width=5)
        ul = VGroup(T("break H–H and Cl–Cl", size=20, color=th.CORAL), M(r"436 + 242 = +678", size=30, color=th.CORAL)).arrange(DOWN, buff=0.08).next_to(up, LEFT, buff=0.15)
        dn = Arrow([0.9, top_y, 0], [0.9, end_y, 0], buff=0, color=th.MINT, stroke_width=5)
        dl = VGroup(T("form two H–Cl", size=20, color=th.MINT), M(r"2 \times 431 = -862", size=30, color=th.MINT)).arrange(DOWN, buff=0.08).next_to(dn, RIGHT, buff=0.15).shift(UP * 0.6)
        net = M(r"\Delta H = 678 - 862 = -184\ \mathrm{kJ\,mol^{-1}}", size=44, color=th.AMBER).to_edge(DOWN, buff=0.4)
        with self.say("Where does a reaction's energy come from? Every reaction breaks bonds and makes new ones. Breaking a bond always costs energy. For hydrogen and chlorine, breaking one H H bond and one Cl Cl bond costs four thirty six plus two forty two, six hundred and seventy eight kilojoules."):
            self.play(FadeIn(title), Write(eq))
            self.play(Create(start), FadeIn(sl))
            self.play(GrowArrow(up), FadeIn(ul))
            self.play(Create(top), FadeIn(tl))
        with self.say("Making bonds always releases energy. Two H Cl bonds release two times four thirty one, eight hundred and sixty two. More comes out than went in. The net change is minus one hundred and eighty four kilojoules per mole. The measured value is minus one eight four point six."):
            nb = C.show_neby(self, "success", height=1.3, corner=DR)
            self.play(GrowArrow(dn), FadeIn(dl))
            self.play(Create(end), FadeIn(el))
            self.play(Write(net))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, eq, start, sl, top, tl, end, el, up, ul, dn, dl, net)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Internal energy U", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        tt = ValueTracker(0)
        c1, c2, c3 = np.array([-4.2, 0.2, 0]), np.array([0, 0.2, 0]), np.array([4.2, 0.2, 0])

        def mol(c, a=0.0, stretch=0.0):
            d = np.array([np.cos(a), np.sin(a), 0]) * (0.55 + stretch)
            return VGroup(Line(c - d, c + d, color=th.MUTED, stroke_width=7), Dot(c - d, radius=0.27, color=th.SKY), Dot(c + d, radius=0.27, color=th.CORAL))
        m1 = always_redraw(lambda: mol(c1 + np.array([1.2 * np.sin(tt.get_value() * 1.3), 0.5 * np.sin(tt.get_value() * 2.1), 0])))
        m2 = always_redraw(lambda: mol(c2, a=tt.get_value() * 2.5))
        m3 = always_redraw(lambda: mol(c3, stretch=0.15 * np.sin(tt.get_value() * 9)))
        labs = VGroup(*[T(s, size=26, color=th.AMBER).move_to(c + DOWN * 1.4) for s, c in zip(["translation", "rotation", "vibration"], (c1, c2, c3))])
        more = T("+ electronic, nuclear and intermolecular energy", size=26, color=th.BODY).to_edge(DOWN, buff=1.0)
        with self.say("The internal energy U of a system is the total energy stored inside it. Molecules moving from place to place, spinning, and vibrating. Plus the energy of electrons, nuclei, and the attractions between molecules. It is a state function, and it grows with the amount of matter."):
            self.play(FadeIn(title))
            self.add(m1, m2, m3)
            self.play(FadeIn(labs))
            self.play(tt.animate.set_value(6), run_time=5, rate_func=linear)
            self.play(FadeIn(more))
        dU = M(r"\Delta U = U_2 - U_1", size=50, color=th.AMBER).next_to(title, DOWN, buff=0.4)
        with self.say("We can never measure U itself, only changes in it: delta U, final minus initial."):
            self.play(Write(dU))
            self.play(tt.animate.set_value(9), run_time=2, rate_func=linear)
        self.play(FadeOut(VGroup(title, labs, more, dU)), FadeOut(m1), FadeOut(m2), FadeOut(m3))
        self.remove(m1, m2, m3)
        bomb = VGroup(RoundedRectangle(corner_radius=0.3, width=2.4, height=2.8, fill_color="#5A6070", fill_opacity=1, stroke_color=th.INK, stroke_width=3),
                      Rectangle(width=1.6, height=0.4, fill_color="#5A6070", fill_opacity=1, stroke_color=th.INK, stroke_width=3).shift(UP * 1.6)).move_to([-3.6, -0.6, 0])
        bath = Rectangle(width=4.2, height=4.0, fill_color=C.WATER, fill_opacity=0.18, stroke_color=th.INK, stroke_width=3).move_to([-3.6, -0.8, 0])
        fl = Star(n=7, outer_radius=0.5, inner_radius=0.22, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to(bomb[0])
        eqs = VGroup(M(r"\Delta V = 0 \Rightarrow \text{no work}", size=40), M(r"q_v = \Delta U", size=60, color=th.AMBER)).arrange(DOWN, buff=0.4).move_to([2.8, 0.4, 0])
        lab = T("bomb calorimeter: a sealed steel vessel", size=24, color=th.MUTED).next_to(bath, DOWN, buff=0.2)
        with self.say("If the volume cannot change, no expansion work can be done, so all the heat goes into internal energy. q at constant volume equals delta U. That is why combustion energies are measured in a bomb calorimeter, a sealed steel vessel of fixed volume, sitting in water."):
            self.play(FadeIn(bath), FadeIn(bomb), FadeIn(lab))
            self.play(GrowFromCenter(fl), bath.animate.set_fill(th.CORAL, opacity=0.25), run_time=1.0)
            self.play(FadeOut(fl))
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]))
        self.play(FadeOut(VGroup(bomb, bath, lab, eqs)))
        care = self.callout("careful", "A system contains internal energy, not heat. Heat is energy in transit across the boundary. Say 'the system absorbed 200 J of heat', never 'the system has 200 J of heat'.", width=11, size=27)
        with self.say("A careful point of language. A system contains internal energy. It does not contain heat. Heat is energy on the move across the boundary. So never say the system has two hundred joules of heat. Say it absorbed two hundred joules of heat."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        law = M(r"\Delta U", r"=", r"q", r"+", r"w", size=96).move_to(UP * 1.4)
        law[2].set_color(th.CORAL)
        law[4].set_color(th.SKY)
        st = T("Energy can neither be created nor destroyed, only converted.", size=28, color=th.BODY).next_to(law, DOWN, buff=0.4)
        with self.say("The first law of thermodynamics. Energy can neither be created nor destroyed, only converted from one form to another. For any process, the change in internal energy equals the heat absorbed, plus the work done on the system."):
            self.play(Write(law))
            self.play(FadeIn(st))
        sysb = RoundedRectangle(corner_radius=0.2, width=2.6, height=1.8, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.AMBER, stroke_width=3).move_to([0, -1.9, 0])
        sl = T("system", size=26, color=th.AMBER).move_to(sysb)
        qin = Arrow([-5.2, -1.5, 0], [-1.5, -1.5, 0], buff=0, color=th.CORAL, stroke_width=6)
        qout = Arrow([1.5, -1.5, 0], [5.2, -1.5, 0], buff=0, color=th.CORAL, stroke_width=6)
        win = Arrow([-5.2, -2.4, 0], [-1.5, -2.4, 0], buff=0, color=th.SKY, stroke_width=6)
        wout = Arrow([1.5, -2.4, 0], [5.2, -2.4, 0], buff=0, color=th.SKY, stroke_width=6)
        lq1 = T("q > 0: heat absorbed", size=20, color=th.CORAL).next_to(qin, UP, buff=0.05)
        lq2 = T("q < 0: heat released", size=20, color=th.CORAL).next_to(qout, UP, buff=0.05)
        lw1 = T("w > 0: work done on it", size=20, color=th.SKY).next_to(win, DOWN, buff=0.05)
        lw2 = T("w < 0: work done by it", size=20, color=th.SKY).next_to(wout, DOWN, buff=0.05)
        with self.say("Signs are everything, and we take the system's point of view. Anything coming in is positive: heat absorbed, or work done on the system by compressing it. Anything going out is negative: heat released, or work done by the system as it expands."):
            self.play(FadeIn(sysb), FadeIn(sl))
            self.play(GrowArrow(qin), FadeIn(lq1), GrowArrow(win), FadeIn(lw1))
            self.play(GrowArrow(qout), FadeIn(lq2), GrowArrow(wout), FadeIn(lw2))
        self.play(FadeOut(VGroup(law, st, sysb, sl, qin, qout, win, wout, lq1, lq2, lw1, lw2)))
        # piston
        yv = ValueTracker(0.0)
        cyl = VGroup(Line([-4.6, -2.6, 0], [-4.6, 1.6, 0], color=th.INK, stroke_width=5), Line([-2.0, -2.6, 0], [-2.0, 1.6, 0], color=th.INK, stroke_width=5),
                     Line([-4.6, -2.6, 0], [-2.0, -2.6, 0], color=th.INK, stroke_width=5))
        gas = always_redraw(lambda: Rectangle(width=2.5, height=1.6 + yv.get_value(), fill_color=th.CORAL, fill_opacity=0.25, stroke_width=0).move_to([-3.3, -2.6 + (1.6 + yv.get_value()) / 2, 0]))
        pist = always_redraw(lambda: VGroup(Rectangle(width=2.5, height=0.25, fill_color="#8C93A8", fill_opacity=1, stroke_width=0).move_to([-3.3, -0.87 + yv.get_value(), 0]),
                                            Arrow([-3.3, 0.9 + yv.get_value(), 0], [-3.3, -0.6 + yv.get_value(), 0], buff=0, color=th.SKY, stroke_width=5)))
        pl = M(r"p_{ext}", size=34, color=th.SKY).move_to([-5.3, 1.2, 0])
        der = VGroup(M(r"F = p_{ext}A", size=40), M(r"\text{work by gas} = F\,\Delta l = p_{ext}A\,\Delta l = p_{ext}\Delta V", size=38),
                     M(r"w = -p_{ext}\,\Delta V", size=56, color=th.SKY), M(r"\Delta U = q - p_{ext}\,\Delta V", size=46, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.0, 0])
        with self.say("The work a chemist meets is pressure volume work. A gas in a cylinder, under a piston of area A, with a constant outside pressure pushing down. The force on the piston is p times A."):
            self.play(Create(cyl))
            self.add(gas, pist)
            self.play(FadeIn(gas), FadeIn(pist), FadeIn(pl))
            self.play(Write(der[0]))
        with self.say("Heat the gas. It expands, pushing the piston out a distance delta l. The work done by the gas is force times distance, p A delta l, and A delta l is just the volume change. Work done by the system is negative, so w equals minus p delta V."):
            self.play(yv.animate.set_value(1.3), run_time=2.0)
            self.play(Write(der[1]))
            self.play(Write(der[2]))
        with self.say("Put it in the first law: delta U equals q minus p delta V. At constant volume, delta V is zero, and we are back to delta U equals q v."):
            self.play(Write(der[3]))
        self.play(FadeOut(VGroup(cyl, pl, der)), FadeOut(gas), FadeOut(pist))
        self.remove(gas, pist)
        head, prob = C.example_head(self, "2 mol of an ideal gas expand from 10.0 L to 25.0 L against a constant 1.50 atm, absorbing 3.50 kJ of heat. Find w and ΔU. (1 L atm = 101.3 J)")
        st = C.steps(r"w = -p_{ext}\Delta V = -(1.50)(15.0) = -22.5\ \mathrm{L\,atm} = -2279\ \mathrm{J} = -2.28\ \mathrm{kJ}",
                     r"q = +3.50\ \mathrm{kJ}",
                     r"\Delta U = q + w = 3.50 - 2.28 = +1.22\ \mathrm{kJ}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example four point one. The volume rises by fifteen litres against one and a half atmospheres. So w is minus twenty two point five litre atmospheres, which is minus two thousand two hundred and seventy nine joules, minus two point two eight kilojoules. Negative, because the gas did the work."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        base = -2.9
        bars = VGroup(Rectangle(width=1.0, height=3.5 * 0.5, fill_color=th.CORAL, fill_opacity=0.85, stroke_width=0),
                      Rectangle(width=1.0, height=2.28 * 0.5, fill_color=th.SKY, fill_opacity=0.85, stroke_width=0),
                      Rectangle(width=1.0, height=1.22 * 0.5, fill_color=th.AMBER, fill_opacity=0.85, stroke_width=0))
        for i, b in enumerate(bars):
            b.move_to([2.6 + 1.4 * i, base, 0], aligned_edge=DOWN)
        bl = VGroup(*[T(s, size=18, color=th.INK).next_to(b, UP, buff=0.08) for s, b in zip(["q in 3.50", "w out 2.28", "ΔU 1.22"], bars)])
        with self.say("Heat absorbed is plus three point five zero. So delta U is three point five zero minus two point two eight, plus one point two two kilojoules. Of the heat taken in, most was spent pushing back the atmosphere, and only one point two two kilojoules was stored."):
            nb = C.show_neby(self, "think", height=1.3, corner=DL)
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(bl))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st, bars, bl)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = M(r"H = U + pV", size=80, color=th.AMBER).move_to(UP * 1.8)
        why = T("most reactions run in open vessels, at constant atmospheric pressure", size=26, color=th.BODY).next_to(h, DOWN, buff=0.35)
        with self.say("Most reactions in the laboratory happen in open vessels, at the constant pressure of the atmosphere, not at constant volume. For constant pressure we use a new state function, enthalpy: H equals U plus p V."):
            self.play(Write(h))
            self.play(FadeIn(why))
        der = VGroup(M(r"\Delta H = \Delta U + p\Delta V", size=42), M(r"\Delta U = q_p - p\Delta V", size=42),
                     M(r"\Delta H = (q_p - p\Delta V) + p\Delta V = q_p", size=46, color=th.AMBER)).arrange(DOWN, buff=0.35).next_to(why, DOWN, buff=0.5)
        with self.say("At constant pressure, delta H is delta U plus p delta V. And the first law says delta U is q p minus p delta V. Add them, and the p delta V terms cancel. Delta H is just the heat exchanged at constant pressure, exactly what a calorimeter open to the air measures."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
            self.play(Write(der[2]))
        gas = M(r"\Delta H = \Delta U + \Delta n_g RT", size=52, color=th.MINT).to_edge(DOWN, buff=0.5)
        with self.say("For reactions with gases, p delta V equals delta n g R T, where delta n g is the change in moles of gas only. So delta H equals delta U plus delta n g R T."):
            self.play(Write(gas))
        self.play(FadeOut(VGroup(h, why, der, gas)))
        title = T("Exothermic and endothermic", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        axl = Arrow([-6.2, -2.8, 0], [-6.2, 2.2, 0], buff=0, color=th.MUTED, stroke_width=3)
        axr = Arrow([0.4, -2.8, 0], [0.4, 2.2, 0], buff=0, color=th.MUTED, stroke_width=3)
        hl = VGroup(T("H", size=24, color=th.MUTED).next_to(axl, UP, buff=0.05), T("H", size=24, color=th.MUTED).next_to(axr, UP, buff=0.05))
        rx = Line([-5.6, 1.0, 0], [-3.8, 1.0, 0], color=th.SKY, stroke_width=6)
        px = Line([-3.0, -1.8, 0], [-1.2, -1.8, 0], color=th.MINT, stroke_width=6)
        ax_ = Arrow([-3.4, 1.0, 0], [-3.4, -1.8, 0], buff=0, color=th.CORAL, stroke_width=5)
        tx = VGroup(T("exothermic", size=28, color=th.CORAL, weight="BOLD"), M(r"\Delta H < 0", size=36, color=th.CORAL), T("heat out: surroundings warm", size=20, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([-3.3, -2.5, 0])
        rn = Line([1.0, -1.6, 0], [2.8, -1.6, 0], color=th.SKY, stroke_width=6)
        pn = Line([3.6, 1.2, 0], [5.4, 1.2, 0], color=th.MINT, stroke_width=6)
        an = Arrow([3.2, -1.6, 0], [3.2, 1.2, 0], buff=0, color=th.SKY, stroke_width=5)
        tn = VGroup(T("endothermic", size=28, color=th.SKY, weight="BOLD"), M(r"\Delta H > 0", size=36, color=th.SKY), T("heat in: surroundings cool", size=20, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([3.4, -2.5, 0])
        labs = VGroup(T("reactants", size=20, color=th.SKY).next_to(rx, UP, buff=0.08), T("products", size=20, color=th.MINT).next_to(px, UP, buff=0.08),
                      T("reactants", size=20, color=th.SKY).next_to(rn, UP, buff=0.08), T("products", size=20, color=th.MINT).next_to(pn, UP, buff=0.08))
        with self.say("On an enthalpy diagram, an exothermic reaction goes downhill. Products sit below reactants, heat flows out, and delta H is negative. An endothermic reaction goes uphill: products above reactants, heat flows in, delta H positive."):
            self.play(FadeIn(title), GrowArrow(axl), GrowArrow(axr), FadeIn(hl))
            self.play(Create(rx), FadeIn(labs[0]), GrowArrow(ax_), Create(px), FadeIn(labs[1]), FadeIn(tx))
            self.play(Create(rn), FadeIn(labs[2]), GrowArrow(an), Create(pn), FadeIn(labs[3]), FadeIn(tn))
        self.play(FadeOut(VGroup(title, axl, axr, hl, rx, px, ax_, tx, rn, pn, an, tn, labs)))
        care = self.callout("careful", "The sign is part of the answer: methane combustion has ΔH = −890 kJ mol⁻¹, not 890. And an exothermic reaction (ΔH negative) makes the thermometer RISE: the thermometer is in the surroundings.", width=11, size=27)
        with self.say("Two sign traps. Writing delta H equals eight ninety for burning methane loses the mark. Heat is released, so it is minus eight ninety. And an exothermic reaction has a negative delta H, yet the thermometer rises, because the thermometer is in the surroundings, which gain the heat."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))
        head, prob = C.example_head(self, "CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l), ΔH° = −890.3 kJ mol⁻¹ at 298 K. Find ΔU°. (R = 8.314 J K⁻¹ mol⁻¹)")
        st = C.steps(r"\Delta n_g = 1 - (1 + 2) = -2 \quad (\text{liquid water does not count})",
                     r"\Delta U = \Delta H - \Delta n_g RT = -890.3 - (-2)(8.314\times10^{-3})(298)",
                     r"\Delta U = -890.3 + 4.96 = -885.3\ \mathrm{kJ\,mol^{-1}}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example four point two. Count gas moles only. Three moles of gas react, methane and two oxygen, and only one, carbon dioxide, is produced. Liquid water does not count. So delta n g is minus two."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Delta U equals delta H minus delta n g R T. Remember R in kilojoules: eight point three one four times ten to the minus three. Minus eight ninety point three plus four point nine six gives minus eight eighty five point three kilojoules per mole."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        ss = para("Standard state: most stable form at 1 bar and the stated temperature (usually 298 K). Written ΔH°.", width=12, size=22, color=th.MUTED).to_edge(UP, buff=0.7)
        cards = VGroup(
            C.card(self, "Reaction", "molar amounts in the balanced equation react. N₂ + 3H₂ → 2NH₃: −92.2 kJ", w=4.0, h=2.3, color=th.AMBER, bsize=21),
            C.card(self, "Formation", "ONE mole of compound from its elements. C + 2H₂ → CH₄: −74.8 kJ mol⁻¹", w=4.0, h=2.3, color=th.SKY, bsize=21),
            C.card(self, "Combustion", "ONE mole burns completely in O₂. Ethanol: −1367 kJ mol⁻¹", w=4.0, h=2.3, color=th.CORAL, bsize=21),
            C.card(self, "Solution", "one mole dissolves in so much solvent that more dilution gives no heat. NH₄Cl: +15.1 kJ mol⁻¹", w=4.0, h=2.3, color=th.MINT, bsize=21),
            C.card(self, "Neutralisation", "one equivalent of acid by base, dilute. H⁺ + OH⁻ → H₂O: −57.1 kJ", w=4.0, h=2.3, color=th.PINK, bsize=21),
            C.card(self, "Elements", "ΔHf° of an element in its standard state is zero: O₂(g), C(graphite), Br₂(l)", w=4.0, h=2.3, color=th.LIME, bsize=21),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25)).next_to(ss, DOWN, buff=0.35)
        with self.say("Enthalpy changes get names. The enthalpy of reaction, for the amounts in the balanced equation. The enthalpy of formation, for one mole of a compound made from its elements. Combustion, for one mole burnt completely in oxygen. Solution, for one mole dissolved in a large excess of solvent. Neutralisation, for one equivalent of acid. And remember, the formation enthalpy of any element in its standard state is zero.") as v:
            self.play(FadeIn(ss))
            for c in cards:
                self.sfx("pop", gain=-16)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)
                self.hold(v.dur / 6 - 0.55)
        self.play(FadeOut(VGroup(ss, cards)))
        f = M(r"\Delta H_r^{\circ} = \sum \Delta H_f^{\circ}(\text{products}) - \sum \Delta H_f^{\circ}(\text{reactants})", size=46, color=th.AMBER).move_to(UP * 2.0)
        with self.say("Once a table of formation enthalpies exists, any reaction enthalpy follows: the sum for the products, minus the sum for the reactants."):
            self.play(Write(f))
        self.play(FadeOut(f))
        y0 = -1.2
        start = Line([-5.4, y0, 0], [-3.6, y0, 0], color=th.SKY, stroke_width=6)
        sl = T("NH₄Cl(s) + water", size=22, color=th.SKY).next_to(start, DOWN, buff=0.15)
        top = Line([-2.2, y0 + 2.2, 0], [-0.4, y0 + 2.2, 0], color=th.CORAL, stroke_width=6)
        tl = T("gaseous ions", size=22, color=th.CORAL).next_to(top, UP, buff=0.1)
        end = Line([1.0, y0 + 0.3, 0], [2.8, y0 + 0.3, 0], color=th.MINT, stroke_width=6)
        el = T("NH₄⁺(aq) + Cl⁻(aq)", size=22, color=th.MINT).next_to(end, DOWN, buff=0.15)
        up = Arrow([-2.9, y0, 0], [-2.9, y0 + 2.2, 0], buff=0, color=th.CORAL, stroke_width=5)
        ul = T("lattice enthalpy (+)", size=22, color=th.CORAL).next_to(up, LEFT, buff=0.1)
        dn = Arrow([0.3, y0 + 2.2, 0], [0.3, y0 + 0.3, 0], buff=0, color=th.MINT, stroke_width=5)
        dl = T("hydration (−)", size=22, color=th.MINT).next_to(dn, RIGHT, buff=0.1).shift(UP * 0.6)
        net = M(r"\Delta H_{sol} = +15.1\ \mathrm{kJ\,mol^{-1}}", size=38, color=th.AMBER).move_to([4.0, -1.8, 0])
        with self.say("Enthalpy of solution is itself a tug of war. Pulling the ionic lattice apart costs energy, the lattice enthalpy. Water molecules wrapping the separated ions release energy, the hydration enthalpy. For ammonium chloride, the lattice term wins by a little. Net, plus fifteen point one kilojoules per mole. That is our cold pack."):
            self.play(Create(start), FadeIn(sl))
            self.play(GrowArrow(up), FadeIn(ul), Create(top), FadeIn(tl))
            self.play(GrowArrow(dn), FadeIn(dl), Create(end), FadeIn(el))
            self.play(Write(net))
        self.play(FadeOut(VGroup(start, sl, top, tl, end, el, up, ul, dn, dl, net)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        e1 = chem(r"C(s) + O_2(g) \rightarrow CO_2(g)", size=44)
        e2 = chem(r"CO_2(g) \rightarrow C(s) + O_2(g)", size=44)
        v1 = M(r"\Delta H = -393.5\ \mathrm{kJ}", size=44, color=th.CORAL)
        v2 = M(r"\Delta H = +393.5\ \mathrm{kJ}", size=44, color=th.SKY)
        r1 = VGroup(e1, v1).arrange(RIGHT, buff=0.6).move_to(UP * 1.4)
        r2 = VGroup(e2, v2).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        law = T("Lavoisier–Laplace: reversing a reaction reverses the sign of ΔH.", size=28, color=th.AMBER).to_edge(DOWN, buff=0.9)
        with self.say("The Lavoisier Laplace law. The enthalpy change of a reaction is equal in size and opposite in sign to that of the reverse reaction. Burning carbon releases three ninety three point five kilojoules, so decomposing carbon dioxide into carbon and oxygen needs exactly that much. If not, you could run the reaction round in a loop and make energy from nothing."):
            self.play(Write(r1))
            self.play(TransformFromCopy(e1, e2), TransformFromCopy(v1, v2))
            self.play(FadeIn(law))
        self.play(FadeOut(VGroup(r1, r2, law)))
        title = T("Hess's law: the route does not matter", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        A = np.array([-4.5, 1.2, 0])
        B = np.array([4.5, -1.8, 0])
        I = np.array([0.0, 2.2, 0])
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.15, width=2.0, height=0.8, fill_color=th.PANEL, fill_opacity=1, stroke_color=c, stroke_width=3).move_to(p) for p, c in ((A, th.SKY), (B, th.MINT), (I, th.AMBER))])
        bl = VGroup(T("start", size=24, color=th.SKY).move_to(A), T("finish", size=24, color=th.MINT).move_to(B), T("intermediate", size=22, color=th.AMBER).move_to(I))
        d1 = Arrow(A + DOWN * 0.45, B + LEFT * 1.05, buff=0.1, color=th.MINT, stroke_width=5)
        d2 = Arrow(A + RIGHT * 1.05, I + LEFT * 1.05, buff=0.1, color=th.AMBER, stroke_width=5)
        d3 = Arrow(I + RIGHT * 0.6 + DOWN * 0.4, B + UP * 0.45, buff=0.1, color=th.AMBER, stroke_width=5)
        l1 = M(r"\Delta H", size=36, color=th.MINT).next_to(d1.get_center(), DL, buff=0.1)
        l2 = M(r"\Delta H_1", size=36, color=th.AMBER).next_to(d2.get_center(), UP, buff=0.1)
        l3 = M(r"\Delta H_2", size=36, color=th.AMBER).next_to(d3.get_center(), RIGHT, buff=0.1)
        res = M(r"\Delta H = \Delta H_1 + \Delta H_2", size=52, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("Hess's law of constant heat summation. The total enthalpy change is the same whether a reaction happens in one step or in several, as long as it starts and ends in the same states. It follows directly from enthalpy being a state function, like the height of our hilltop."):
            self.play(FadeIn(title), FadeIn(boxes), FadeIn(bl))
            self.play(GrowArrow(d1), FadeIn(l1))
            self.play(GrowArrow(d2), FadeIn(l2))
            self.play(GrowArrow(d3), FadeIn(l3))
            self.play(Write(res))
        self.play(FadeOut(VGroup(title, boxes, bl, d1, d2, d3, l1, l2, l3, res)))
        self.example_43()
        self.born_haber()

    def example_43(self):
        head, prob = C.example_head(self, "Find ΔHf° of methane from: (i) C + O₂ → CO₂, −393.5; (ii) H₂ + ½O₂ → H₂O(l), −285.8; (iii) CH₄ + 2O₂ → CO₂ + 2H₂O(l), −890.3 kJ mol⁻¹.")
        target = VGroup(T("target:", size=24, color=th.MUTED), chem(r"C(s) + 2H_2(g) \rightarrow CH_4(g)", size=38, color=th.AMBER)).arrange(RIGHT, buff=0.3).next_to(prob, DOWN, buff=0.35).align_to(prob, LEFT)
        plain = VGroup(
            VGroup(chem(r"C + O_2 \rightarrow CO_2", size=36), M(r"-393.5", size=36)),
            VGroup(chem(r"2H_2 + O_2 \rightarrow 2H_2O", size=36), M(r"2(-285.8) = -571.6", size=36)),
            VGroup(chem(r"CO_2 + 2H_2O \rightarrow CH_4 + 2O_2", size=36), M(r"+890.3", size=36, color=th.SKY)),
        )
        plain.arrange(DOWN, buff=0.35).next_to(target, DOWN, buff=0.4)
        for r in plain:
            r[0].next_to([-5.6, r[0].get_y(), 0], RIGHT, buff=0)
            r[1].move_to([4.4, r[0].get_y(), 0])
        summ = M(r"\mathrm{C + 2H_2}", r"\mathrm{\ + 2O_2 + CO_2 + 2H_2O}", r"\rightarrow", r"\mathrm{CH_4}", r"\mathrm{\ + 2O_2 + CO_2 + 2H_2O}", size=36)
        summ.next_to(plain, DOWN, buff=0.35).set_x(0)
        strikes = VGroup(*[Line(summ[k].get_left(), summ[k].get_right(), color=th.CORAL, stroke_width=4) for k in (1, 4)])
        res = M(r"\Delta H_f^{\circ}(\mathrm{CH_4}) = -393.5 - 571.6 + 890.3 = -74.8\ \mathrm{kJ\,mol^{-1}}", size=40, color=th.AMBER).to_edge(DOWN, buff=0.45)
        with self.say("Worked example four point three. We want the formation of methane from carbon and hydrogen, which cannot be measured directly. Take equation one as written. Add two times equation two."):
            self.play(FadeIn(head), FadeIn(prob), FadeIn(target))
            self.play(FadeIn(plain[0]))
            self.play(FadeIn(plain[1]))
        with self.say("Then reverse equation three, which by Laplace's law flips its sign to plus eight ninety point three. Now add all three. Carbon dioxide cancels. Water cancels. The oxygen cancels: one plus one minus two. What is left is exactly our target."):
            self.play(FadeIn(plain[2]))
            self.play(Write(summ))
            self.play(Create(strikes), summ[1].animate.set_opacity(0.35), summ[4].animate.set_opacity(0.35))
        with self.say("So the formation enthalpy of methane is minus three ninety three point five, minus five seventy one point six, plus eight ninety point three: minus seventy four point eight kilojoules per mole."):
            self.play(Write(res))
            self.sfx("correct", gain=-10)
        self.play(FadeOut(VGroup(head, prob, target, plain, summ, strikes, res)))

    def born_haber(self):
        title = T("The Born–Haber cycle for NaCl", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)

        def y(e):
            return -0.75 + e * 0.0042
        lv = [("Na(s) + ½Cl₂(g)", 0, th.INK), ("Na(g) + ½Cl₂(g)", 108, th.AMBER), ("Na(g) + Cl(g)", 229, th.AMBER),
              ("Na⁺(g) + e⁻ + Cl(g)", 725, th.CORAL), ("Na⁺(g) + Cl⁻(g)", 376, th.SKY), ("NaCl(s)", -411, th.MINT)]
        lines = VGroup()
        for nm, e, c in lv:
            ln = Line([-4.0, y(e), 0], [-1.8, y(e), 0], color=c, stroke_width=5)
            lines.add(VGroup(ln, T(nm, size=22, color=c).next_to(ln, RIGHT, buff=0.15)))
        steps = [("sublimation  +108", 0, 1, th.AMBER), ("½ × 242 = +121", 1, 2, th.AMBER), ("ionisation  +496", 2, 3, th.CORAL), ("electron affinity  −349", 3, 4, th.SKY)]
        arrows = VGroup()
        for k, (lab, a_, b_, c) in enumerate(steps):
            x = -3.75 + 0.45 * k
            ar = Arrow([x, y(lv[a_][1]), 0], [x, y(lv[b_][1]), 0], buff=0, color=c, stroke_width=4, max_tip_length_to_length_ratio=0.12)
            tl = T(lab, size=22, color=c).move_to([3.3, 2.4 - 0.45 * k, 0])
            arrows.add(VGroup(ar, tl))
        fa = Arrow([-4.4, y(0), 0], [-4.4, y(-411), 0], buff=0, color=th.MINT, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        fal = T("ΔHf = −411", size=22, color=th.MINT).next_to(fa, LEFT, buff=0.1)
        U = Arrow([-2.05, y(376), 0], [-2.05, y(-411), 0], buff=0, color=th.PINK, stroke_width=6, max_tip_length_to_length_ratio=0.08)
        Ul = T("lattice enthalpy U = ?", size=24, color=th.PINK, weight="BOLD").move_to([3.3, 0.4, 0])
        with self.say("Hess's law also lets us find the lattice enthalpy of an ionic solid, which can never be measured directly. This is the Born Haber cycle for sodium chloride. Start from sodium metal and chlorine gas. Turn sodium into a gas: plus one oh eight. Break half a mole of chlorine bonds: half of two forty two, plus one twenty one."):
            self.play(FadeIn(title), FadeIn(lines[0]))
            for k in range(2):
                self.play(GrowArrow(arrows[k][0]), FadeIn(arrows[k][1]), FadeIn(lines[k + 1]))
        with self.say("Ionise sodium: plus four ninety six. Give the electron to chlorine: the electron affinity, minus three forty nine. Now we have gaseous ions. Letting them collapse into the crystal releases the lattice enthalpy, U. The direct route, formation of sodium chloride, is minus four eleven."):
            for k in range(2, 4):
                self.play(GrowArrow(arrows[k][0]), FadeIn(arrows[k][1]), FadeIn(lines[k + 1]))
            self.play(GrowArrow(U), FadeIn(Ul))
            self.play(GrowArrow(fa), FadeIn(fal), FadeIn(lines[5]))
        res = VGroup(M(r"-411 = 108 + 121 + 496 - 349 + U = 376 + U", size=32), M(r"U = -787\ \mathrm{kJ\,mol^{-1}}", size=44, color=th.PINK)).arrange(DOWN, buff=0.2).move_to([3.0, -1.4, 0])
        with self.say("Both routes must give the same total. Minus four eleven equals three seventy six plus U, so U is minus seven eighty seven kilojoules per mole. A huge number, which is why salt melts at eight hundred and one degrees."):
            nb = C.show_neby(self, "surprised", height=1.3, corner=DR)
            self.play(Write(res[0]))
            self.play(Write(res[1]))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, lines, arrows, fa, fal, U, Ul, res)))
        self.tip("The formation equation has ½Cl₂, so only HALF the Cl–Cl bond enthalpy (121 kJ) enters the cycle.",
                 "The commonest Born Haber error. The formation equation uses half a mole of chlorine gas, so only half the bond enthalpy, one twenty one, goes into the cycle. Use the whole two forty two, and your answer is off by one hundred and twenty one kilojoules.")

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        ex = VGroup(T("ice melts above 0 °C", size=26, color=th.SKY), T("a gas fills a vacuum", size=26, color=th.SKY), T("NH₄Cl dissolves and cools", size=26, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.6, 0.6, 0])
        nb = T("all spontaneous, all absorb heat or need none", size=26, color=th.AMBER).next_to(ex, DOWN, buff=0.5)
        with self.say("A spontaneous process happens on its own, without continuous help. Many spontaneous processes give out heat. But not all. Ice melts at room temperature, absorbing heat. A gas spreads into a vacuum with no energy change at all. And our cold pack absorbs heat. So energy is not the only driving force."):
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in ex], lag_ratio=0.4))
            self.play(FadeIn(nb))
        L = np.array([2.2, 0.0, 0])
        box = Rectangle(width=4.4, height=3.2, stroke_color=th.INK, stroke_width=3).move_to(L + RIGHT * 1.0)
        wall = Line(L + RIGHT * 1.0 + UP * 1.6, L + RIGHT * 1.0 + DOWN * 1.6, color=th.CORAL, stroke_width=5)
        rng = np.random.default_rng(5)
        dots = VGroup(*[Dot(L + np.array([rng.uniform(-1.0, 0.8), rng.uniform(-1.4, 1.4), 0]), radius=0.08, color=th.AMBER) for _ in range(30)])
        with self.say("Watch the gas. Remove the wall, and the molecules spread out through the whole box. They never all gather back on one side. There are vastly more ways to be spread out than to be bunched up. Nature drifts towards disorder."):
            self.play(Create(box), Create(wall), FadeIn(dots))
            self.play(FadeOut(wall))
            self.play(*[d.animate.move_to(L + RIGHT * 1.0 + np.array([rng.uniform(-2.0, 2.0), rng.uniform(-1.4, 1.4), 0])) for d in dots], run_time=2.5)
        self.play(FadeOut(VGroup(ex, nb, box, dots)))
        d = VGroup(M(r"\Delta S = \frac{q_{rev}}{T}", size=64, color=th.AMBER), T("entropy S: a measure of disorder.  Unit J K⁻¹ mol⁻¹", size=26, color=th.BODY)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.8)
        with self.say("That tendency is measured by entropy, S, a measure of the randomness or disorder of a system. It is a state function. For a change carried out reversibly at temperature T, delta S is the heat absorbed reversibly, divided by T."):
            self.play(Write(d[0]), FadeIn(d[1]))
        cells = VGroup()
        for k, (name, jit, sp) in enumerate([("solid", 0.02, 0.36), ("liquid", 0.12, 0.42), ("gas", 0.55, 0.9)]):
            c = np.array([-4.2 + 4.2 * k, -1.2, 0])
            frame = Square(side_length=2.6, stroke_color=th.PANEL_EDGE, stroke_width=3).move_to(c)
            pts = VGroup()
            for i in range(4):
                for j in range(4):
                    p = c + np.array([(i - 1.5) * sp * (0.6 if k == 2 else 1), (j - 1.5) * sp * (0.6 if k == 2 else 1), 0]) + np.array([rng.uniform(-jit, jit) * 2.2, rng.uniform(-jit, jit) * 2.2, 0])
                    p = np.clip(p, c - 1.15, c + 1.15)
                    pts.add(Dot(p, radius=0.1, color=th.SKY))
            cells.add(VGroup(frame, pts, T(name, size=24, color=th.INK).next_to(frame, DOWN, buff=0.15)))
        order = M(r"S_{solid} < S_{liquid} \ll S_{gas}", size=40, color=th.MINT).to_edge(DOWN, buff=0.35)
        with self.say("Entropy rises from solid to liquid to gas. It rises when a reaction makes more gas molecules, when a solid dissolves, when things mix, and whenever anything is heated."):
            for c in cells:
                self.play(FadeIn(c), run_time=0.6)
            self.play(Write(order))
        self.play(FadeOut(VGroup(d, cells, order)))
        st = C.steps(r"\text{melting ice: } \Delta S = \frac{6010}{273} = 22.0\ \mathrm{J\,K^{-1}mol^{-1}}",
                     r"\text{boiling water: } \Delta S = \frac{40\,700}{373} = 109.1\ \mathrm{J\,K^{-1}mol^{-1}}", size=42).move_to(UP * 0.6)
        third = self.callout("remember", "Third law: the entropy of a perfect crystal at absolute zero is zero. So entropies have an absolute scale, and tables list S° itself.", width=11, size=26).to_edge(DOWN, buff=0.5)
        with self.say("At a melting or boiling point the change is reversible, so delta S is delta H over T. Melting ice: six thousand and ten over two seventy three, twenty two joules per kelvin per mole. Boiling water: forty thousand seven hundred over three seventy three, one hundred and nine. Boiling creates far more disorder. And the third law: a perfect crystal at absolute zero has zero entropy, which gives entropy an absolute scale."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
            self.play(FadeIn(third, shift=UP * 0.2))
        self.play(FadeOut(VGroup(st, third)))
        self.quiz("For which process is ΔS negative?",
                  ["CaCO₃(s) → CaO(s) + CO₂(g)", "ice → water", "N₂ + 3H₂ → 2NH₃", "dissolving NaCl in water"], 2,
                  "Which of these has a negative entropy change? Pause and think.",
                  "C. Four moles of gas become two, so the system becomes more ordered. Decomposing limestone makes a gas, melting and dissolving increase disorder, so all three of those have positive delta S.")

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        intro = T("The first law conserves energy. It does not say which way a change goes.", size=28, color=th.BODY).to_edge(UP, buff=0.8)
        hot = RoundedRectangle(corner_radius=0.2, width=2.6, height=2.0, fill_color=th.CORAL, fill_opacity=0.6, stroke_width=0).move_to([-3.6, 0.2, 0])
        cold = RoundedRectangle(corner_radius=0.2, width=2.6, height=2.0, fill_color=th.SKY, fill_opacity=0.6, stroke_width=0).move_to([3.6, 0.2, 0])
        hl = T("hot", size=30, color=WHITE, weight="BOLD").move_to(hot)
        cl = T("cold", size=30, color=WHITE, weight="BOLD").move_to(cold)
        arr = Arrow(hot.get_right(), cold.get_left(), buff=0.3, color=th.AMBER, stroke_width=8)
        al = T("heat flows this way, on its own", size=24, color=th.AMBER).next_to(VGroup(hot, cold), UP, buff=0.3)
        back = Arrow(cold.get_left() + DOWN * 0.6, hot.get_right() + DOWN * 0.6, buff=0.3, color=th.FAINT, stroke_width=6)
        bx = Cross(back, stroke_color=th.CORAL, scale_factor=0.3)
        with self.say("The first law says energy is conserved. But it does not tell us which way a change will go. Energy would be conserved just as well if heat flowed from a cold body into a hot one. It never does. The second law supplies the direction."):
            self.play(FadeIn(intro))
            self.play(FadeIn(hot), FadeIn(cold), FadeIn(hl), FadeIn(cl))
            self.play(GrowArrow(arr), FadeIn(al), hot.animate.set_fill(th.AMBER), cold.animate.set_fill(th.AMBER), run_time=2.0)
            self.play(GrowArrow(back), Create(bx))
        self.play(FadeOut(VGroup(intro, hot, cold, hl, cl, arr, al, back, bx)))
        title = T("The second law: three statements", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        sts = VGroup(
            C.card(self, "Entropy", "In every spontaneous process the total entropy of the universe increases.", w=4.0, h=2.6, color=th.AMBER, bsize=22),
            C.card(self, "Clausius", "Heat cannot flow on its own from a colder body to a hotter body.", w=4.0, h=2.6, color=th.SKY, bsize=22),
            C.card(self, "Kelvin–Planck", "No engine working in a cycle can turn heat completely into work.", w=4.0, h=2.6, color=th.CORAL, bsize=22),
        ).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.5)
        with self.say("The second law can be stated three equivalent ways. In any spontaneous process, the total entropy of the universe increases. Heat cannot flow by itself from a colder body to a hotter one. And no engine working in a cycle can convert heat completely into work, without rejecting some to a colder place.") as v:
            self.play(FadeIn(title))
            for c in sts:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur / 3 - 0.6)
        eq = M(r"\Delta S_{total} = \Delta S_{system} + \Delta S_{surroundings} > 0", size=44, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("In symbols, the entropy change of the system plus that of the surroundings must be positive for any spontaneous change."):
            self.play(Write(eq))
        self.play(FadeOut(VGroup(title, sts, eq)))
        sysb = Circle(radius=1.1, fill_color=th.SKY, fill_opacity=0.35, stroke_color=th.SKY, stroke_width=3).move_to([-2.2, -0.2, 0])
        sl = T("water freezing", size=24, color=th.SKY).next_to(sysb, DOWN, buff=0.2)
        b1 = Rectangle(width=0.9, height=1.2, fill_color=th.CORAL, fill_opacity=0.8, stroke_width=0).move_to([2.0, -1.5, 0], aligned_edge=UP)
        b2 = Rectangle(width=0.9, height=2.0, fill_color=th.MINT, fill_opacity=0.8, stroke_width=0).move_to([3.4, -1.5, 0], aligned_edge=DOWN)
        l1 = T("ΔS system < 0", size=22, color=th.CORAL).next_to(b1, DOWN, buff=0.1)
        l2 = T("ΔS surroundings > 0", size=22, color=th.MINT).next_to(b2, UP, buff=0.1)
        zero = Line([1.2, -1.5, 0], [4.2, -1.5, 0], color=th.MUTED, stroke_width=2)
        note = para("Water freezing in a Mustang winter: the system gets more ordered, but the heat it releases disorders the surroundings even more.", width=11, size=26, color=th.BODY).to_edge(UP, buff=0.8)
        with self.say("So the entropy of the system alone can fall. Water freezing on a Mustang winter night becomes more ordered. But the heat it releases makes the cold surroundings more disordered by an even larger amount. The total still rises."):
            nb = C.show_neby(self, "cool", height=1.3, corner=DR)
            self.play(FadeIn(note))
            self.play(FadeIn(sysb), FadeIn(sl), Create(zero))
            self.play(GrowFromEdge(b1, UP), FadeIn(l1))
            self.play(GrowFromEdge(b2, DOWN), FadeIn(l2))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(note, sysb, sl, zero, b1, b2, l1, l2)))

    # ------------------------------------------------------------------ part 9
    def p9(self):
        self.section(8)
        g = M(r"G = H - TS", size=72, color=th.AMBER).to_edge(UP, buff=0.8)
        with self.say("Measuring the surroundings is awkward. Josiah Willard Gibbs found a way to judge spontaneity from the system alone. He defined the free energy, G equals H minus T S."):
            self.play(Write(g))
        der = VGroup(M(r"\Delta S_{surr} = -\frac{\Delta H_{sys}}{T}", size=40),
                     M(r"\Delta S_{sys} - \frac{\Delta H_{sys}}{T} > 0", size=40),
                     M(r"\times(-T):\quad \Delta H_{sys} - T\Delta S_{sys} < 0", size=40),
                     M(r"\Delta G = \Delta H - T\Delta S < 0 \;\Leftrightarrow\; \text{spontaneous}", size=46, color=th.AMBER)).arrange(DOWN, buff=0.32).next_to(g, DOWN, buff=0.4)
        with self.say("Here is why. At constant temperature and pressure, the heat a reaction releases, minus delta H, flows into the surroundings, so their entropy changes by minus delta H over T. The second law needs the total to be positive."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
        with self.say("Multiply through by minus T, which flips the inequality: delta H minus T delta S must be negative. That combination is delta G. A process is spontaneous if and only if delta G is negative. At equilibrium, delta G is zero."):
            self.play(Write(der[2]))
            self.sfx("impact", gain=-12)
            self.play(Write(der[3]))
            self.play(Circumscribe(der[3], color=th.AMBER))
        self.play(FadeOut(VGroup(g, der)))
        title = T("ΔG = ΔH − TΔS: four cases", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Axes(x_range=[0, 10, 2], y_range=[-5, 5, 5], x_length=6.4, y_length=4.6, tips=False,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-2.6, -0.6, 0])
        xl = T("T", size=24, color=th.MUTED).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = M(r"\Delta G", size=30, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1)
        zone = Rectangle(width=6.4, height=2.3, fill_color=th.MINT, fill_opacity=0.08, stroke_width=0).move_to(ax.c2p(5, -2.5))
        zl = T("spontaneous", size=20, color=th.MINT).move_to(ax.c2p(8.6, -4.4))
        cases = [(-2, 0.4, th.MINT, "ΔH −, ΔS +: always"), (-2.0, -0.6, th.SKY, "ΔH −, ΔS −: low T only"),
                 (3.5, 0.6, th.AMBER, "ΔH +, ΔS +: high T only"), (2, -0.25, th.CORAL, "ΔH +, ΔS −: never")]
        lines = VGroup()
        tags = VGroup()
        for i, (h, s, c, lab) in enumerate(cases):
            ln = ax.plot(lambda t, h=h, s=s: h - t * s, x_range=[0, 10], color=c, stroke_width=4)
            lines.add(ln)
            tags.add(T(lab, size=22, color=c).move_to([3.9, 1.6 - 0.75 * i, 0]))
        with self.say("Delta G depends on temperature. Plot it against T for the four sign combinations. If delta H is negative and delta S positive, delta G is negative at every temperature: always spontaneous. If delta H is positive and delta S negative, never."):
            self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(zone), FadeIn(zl))
            for k in (0, 3):
                self.play(Create(lines[k]), FadeIn(tags[k]))
        with self.say("The other two cross the axis. Negative delta H with negative delta S is spontaneous only at low temperature. Positive delta H with positive delta S, only at high temperature. The crossover is at T equals delta H over delta S."):
            for k in (1, 2):
                self.play(Create(lines[k]), FadeIn(tags[k]))
            cross = Dot(ax.c2p(3.5 / 0.6, 0), color=WHITE, radius=0.1)
            cl = M(r"T = \frac{\Delta H}{\Delta S}", size=32, color=th.AMBER).next_to(cross, UP, buff=0.2)
            self.play(FadeIn(cross, scale=2), Write(cl))
        work = T("−ΔG = the maximum useful work the change can deliver", size=24, color=th.BODY).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(work))
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, ax, xl, yl, zone, zl, lines, tags, cross, cl, work)))
        self.example_45()
        nb = C.show_neby(self, "success", height=1.5, at=[4.6, -1.4, 0])
        res = VGroup(T("The cold pack:", size=30, color=th.SKY, weight="BOLD"),
                     M(r"\Delta H = +15.1\ \mathrm{kJ\,mol^{-1}}\ (\text{uphill in energy})", size=36),
                     M(r"\Delta S \gg 0\ (\text{ordered crystal} \rightarrow \text{free ions})", size=36),
                     M(r"\Delta G = \Delta H - T\Delta S < 0", size=44, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-1.4, 0.2, 0])
        with self.say("And now the cold pack makes sense. Dissolving ammonium chloride is uphill in energy, plus fifteen point one kilojoules. But an ordered crystal breaking into freely moving ions is a huge increase in entropy. At room temperature, T delta S beats delta H, so delta G is negative. The reaction is driven not by energy, but by disorder. That is the second driving force of chemistry."):
            for r in res:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
            self.play(Circumscribe(res[3], color=th.MINT))
        C.hide_neby(self, nb)
        self.play(FadeOut(res))
        care = self.callout("careful", "ΔG < 0 means possible, not fast. Diamond → graphite has ΔG° = −2.9 kJ mol⁻¹, yet a diamond lasts millions of years: its activation energy is enormous.", width=11, size=27)
        with self.say("One caution, and it ties back to Unit 3. Negative delta G means a reaction can happen, not that it happens quickly. Diamond to graphite has delta G of minus two point nine kilojoules per mole, yet a diamond lasts for ever, because its activation energy is enormous."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))

    def example_45(self):
        head, prob = C.example_head(self, "CaCO₃(s) → CaO(s) + CO₂(g): ΔH° = +178.3 kJ mol⁻¹, ΔS° = +160.6 J K⁻¹ mol⁻¹. (a) Spontaneous at 298 K? (b) Above what temperature does it become spontaneous?")
        st = C.steps(r"\Delta S^{\circ} = 0.1606\ \mathrm{kJ\,K^{-1}mol^{-1}}",
                     r"\Delta G^{\circ} = 178.3 - (298)(0.1606) = 178.3 - 47.9 = +130.4\ \mathrm{kJ\,mol^{-1}}",
                     r"T = \frac{\Delta H^{\circ}}{\Delta S^{\circ}} = \frac{178.3}{0.1606} = 1110\ \mathrm{K}\ (837\ ^{\circ}\mathrm{C})", size=36).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example four point five, limestone. First, convert entropy to kilojoules: zero point one six zero six. At two ninety eight kelvin, delta G is one seventy eight point three minus forty seven point nine, plus one thirty point four kilojoules. Positive, so limestone does not decompose at room temperature. Lucky, since so many buildings in Nepal are made of it."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        ax = Axes(x_range=[0, 1600, 400], y_range=[-80, 180, 60], x_length=5.4, y_length=2.6, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": False}).to_corner(DR, buff=0.5)
        ln = ax.plot(lambda t: 178.3 - 0.1606 * t, x_range=[0, 1600], color=th.AMBER, stroke_width=4)
        dot = Dot(ax.c2p(1110, 0), color=WHITE, radius=0.08)
        al = VGroup(M(r"\Delta G^{\circ}", size=24, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.05), T("T (K)", size=18, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.1))
        with self.say("It becomes spontaneous where delta G crosses zero: T equals delta H over delta S, one seventy eight point three over zero point one six zero six, about eleven hundred and ten kelvin. That is why a cement kiln runs at around fourteen hundred degrees Celsius."):
            self.play(Write(st[2]))
            self.play(Create(ax), FadeIn(al), Create(ln))
            self.play(FadeIn(dot, scale=2))
        self.play(FadeOut(VGroup(head, prob, st, ax, ln, dot, al)))

    # ------------------------------------------------------------------ part 10
    def p10(self):
        self.section(9)
        e = M(r"\Delta G = \Delta G^{\circ} + RT\ln Q", size=60).to_edge(UP, buff=0.8)
        ql = T("Q: the reaction quotient, with actual (not equilibrium) concentrations", size=24, color=th.MUTED).next_to(e, DOWN, buff=0.25)
        with self.say("Away from standard conditions, the free energy change depends on the mixture: delta G equals delta G standard plus R T ln Q, where Q is the reaction quotient, the same expression as K but with the concentrations you actually have."):
            self.play(Write(e))
            self.play(FadeIn(ql))
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 4, 1], x_length=5.2, y_length=3.6, tips=False,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-3.5, -1.2, 0])
        gx = lambda x: 3.2 - 1.6 * x + 1.2 * (x * np.log(max(x, 1e-6)) + (1 - x) * np.log(max(1 - x, 1e-6))) + 0.8
        curve = ax.plot(gx, x_range=[0.001, 0.999, 0.005], color=th.AMBER, stroke_width=4)
        xs = np.linspace(0.01, 0.99, 400)
        xm = xs[np.argmin([gx(x) for x in xs])]
        s = ValueTracker(0.05)
        ball = always_redraw(lambda: Dot(ax.c2p(s.get_value(), gx(s.get_value())) + UP * 0.12, radius=0.12, color=th.SKY))
        labs = VGroup(T("pure reactants", size=20, color=th.MUTED).next_to(ax.c2p(0, 0), DOWN, buff=0.15), T("pure products", size=20, color=th.MUTED).next_to(ax.c2p(1, 0), DOWN, buff=0.15),
                      T("G", size=24, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1))
        eqm = T("equilibrium: ΔG = 0, Q = K", size=24, color=th.MINT).next_to(ax.c2p(xm, gx(xm)), DOWN, buff=0.35)
        with self.say("Picture the free energy of the mixture as the reaction proceeds. From either end, G runs downhill, and the reaction moves until G reaches its lowest point. At that minimum, there is no further tendency to change. That is equilibrium. There, delta G is zero, and Q has become K."):
            self.play(Create(ax), FadeIn(labs), Create(curve))
            self.add(ball)
            self.play(s.animate.set_value(xm), run_time=2.0, rate_func=rate_functions.ease_out_quad)
            self.play(s.animate.set_value(0.95), run_time=0.01)
            self.play(s.animate.set_value(xm), run_time=2.0, rate_func=rate_functions.ease_out_quad)
            self.play(FadeIn(eqm))
        der = VGroup(M(r"0 = \Delta G^{\circ} + RT\ln K", size=40), M(r"\Delta G^{\circ} = -RT\ln K = -2.303\,RT\log K", size=44, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([3.4, 0.9, 0])
        der.scale_to_fit_width(min(der.width, 6.4))
        with self.say("Put delta G equals zero and Q equals K into the equation: delta G standard equals minus R T ln K, or minus two point three zero three R T log K."):
            nb = C.show_neby(self, "success", height=1.3, corner=DR)
            self.play(Write(der[0]))
            self.sfx("impact", gain=-12)
            self.play(Write(der[1]))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(e, ql, ax, curve, labs, eqm, der)), FadeOut(ball))
        self.remove(ball)
        rows = [["ΔG°", "K", "At equilibrium"], ["negative", "K > 1", "products favoured"], ["zero", "K = 1", "neither favoured"], ["positive", "K < 1", "reactants favoured"]]
        tb = C.table(rows, [3.0, 2.6, 4.4], row_h=0.7, size=28, colors=[th.AMBER, th.INK, th.MINT]).move_to(UP * 0.6)
        with self.say("So the sign of delta G standard tells you where equilibrium lies. Negative, K is greater than one, and products are favoured. Positive, K is less than one, reactants favoured."):
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.5)
        self.play(FadeOut(tb))
        head, prob = C.example_head(self, "At 298 K, Kp = 0.145 for N₂O₄(g) ⇌ 2NO₂(g). Find ΔG°. (R = 8.314 J K⁻¹ mol⁻¹)")
        st = C.steps(r"2.303RT = 2.303 \times 8.314 \times 298 = 5706\ \mathrm{J\,mol^{-1}}",
                     r"\log K = \log 0.145 = -0.8386",
                     r"\Delta G^{\circ} = -(5706)(-0.8386) = +4785\ \mathrm{J\,mol^{-1}} = +4.79\ \mathrm{kJ\,mol^{-1}}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example four point six. Two point three zero three R T at two ninety eight kelvin is five thousand seven hundred and six joules per mole. Log of zero point one four five is minus zero point eight three eight six. So delta G standard is plus four thousand seven hundred and eighty five joules, plus four point seven nine kilojoules per mole. Positive, with K less than one: at room temperature, dinitrogen tetroxide is favoured."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("If ΔG° for a reaction is negative, its equilibrium constant K is",
                  ["less than 1", "equal to 1", "greater than 1", "zero"], 2,
                  "Final check. A reaction has a negative standard free energy change. What can you say about its K? Pause and think.",
                  "C, greater than one. From delta G standard equals minus R T ln K, a negative delta G standard needs a positive ln K, so K is greater than one, and products are favoured.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "System and surroundings: open, closed, isolated. U, H, S, G are state functions; q and w are not.",
            M(r"\Delta U = q + w,\quad w = -p_{ext}\Delta V,\quad q_v = \Delta U", size=40),
            M(r"H = U + pV,\quad q_p = \Delta H,\quad \Delta H = \Delta U + \Delta n_g RT", size=40),
            M(r"\Delta H_r^{\circ} = \sum\Delta H_f^{\circ}(\text{prod}) - \sum\Delta H_f^{\circ}(\text{react})", size=40),
            "Laplace: reverse reaction, reverse sign. Hess: ΔH is route-independent (Born–Haber: U(NaCl) = −787).",
            M(r"\Delta S = q_{rev}/T;\quad \Delta S_{total} > 0 \text{ for a spontaneous change}", size=40),
            M(r"\Delta G = \Delta H - T\Delta S < 0;\quad T = \Delta H/\Delta S", size=40),
            M(r"\Delta G^{\circ} = -RT\ln K = -2.303RT\log K", size=40),
        ], "Let us recap. The first law: delta U equals q plus w, with w equals minus p delta V. At constant pressure the heat is delta H, which equals delta U plus delta n g R T. Reaction enthalpies come from formation enthalpies, Laplace's law and Hess's law, including the Born Haber cycle. Entropy measures disorder, and the second law says the total entropy always rises in a spontaneous change. Gibbs combined both: a change is spontaneous when delta G is negative. And delta G standard equals minus R T ln K.")
        self.outro("That is thermodynamics. Next, we turn free energy into electricity, in electrochemistry: electrode potentials, cells and batteries. See you in the next lesson on NEBians.")
