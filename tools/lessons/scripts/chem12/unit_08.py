import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

BR = "#C1543A"
CL = "#7BE495"
OHC = "#FF6B6B"


def skeleton(carbons, bonds, halo, center=ORIGIN, scale=0.8, hsym="Br"):
    """carbons: list of (x, y) grid points; bonds: pairs of indices; halo: (carbon index, dx, dy)."""
    c = np.array(center, dtype=float)
    pts = [c + scale * np.array([x, y, 0]) for x, y in carbons]
    g = VGroup()
    for a, b in bonds:
        g.add(Line(pts[a], pts[b], color=th.MUTED, stroke_width=5))
    hi, dx, dy = halo
    hp = pts[hi] + scale * np.array([dx, dy, 0])
    g.add(Line(pts[hi], hp, color=th.MUTED, stroke_width=5))
    for p in pts:
        g.add(C.atom("C", r=0.26).move_to(p))
    g.add(C.atom(hsym, r=0.36, color=BR if hsym == "Br" else CL).move_to(hp))
    return g


def profile(r, peaks, p, x0=-5.5, x1=5.5, y0=-2.6, sc=1.0):
    """Energy curve through reactant level r, list of (x, height) peaks/wells, product level p."""
    xs = [x0, x0 + 1.0] + [px for px, _ in peaks] + [x1 - 1.0, x1]
    ys = [r, r] + [h for _, h in peaks] + [p, p]
    pts = [np.array([x, y0 + sc * y, 0]) for x, y in zip(xs, ys)]
    m = VMobject(stroke_color=th.INK, stroke_width=4).set_points_as_corners(pts)
    return m


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 8
    TITLE = "Haloalkanes"
    SUBTITLE = "The C–X bond, SN1, SN2 and chloroform"
    SECTIONS = ["Naming, isomers and classes", "Preparation", "Physical properties", "SN1 and SN2",
                "Eight substitution products", "Elimination, reduction, Wurtz", "Making chloroform", "Reactions of chloroform"]
    NEXT = "Unit 9 · Haloarenes"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        bottle = VGroup(RoundedRectangle(corner_radius=0.3, width=1.8, height=2.6, fill_color="#5A3A1A", fill_opacity=0.95, stroke_color=th.INK, stroke_width=3),
                        Rectangle(width=0.7, height=0.5, fill_color="#5A3A1A", fill_opacity=0.95, stroke_color=th.INK, stroke_width=3))
        bottle[1].next_to(bottle[0], UP, buff=0)
        lab = VGroup(T("CHCl₃", size=30, color=WHITE, weight="BOLD"), T("chloroform", size=18, color=th.BODY)).arrange(DOWN, buff=0.05).move_to(bottle[0])
        bot = VGroup(bottle, lab).move_to([-3.4, -0.2, 0])
        facts = VGroup(T("1847: the first general anaesthetic", size=26, color=th.INK), T("always in a dark brown bottle", size=26, color=th.AMBER),
                       T("always filled to the brim", size=26, color=th.AMBER), T("always with 1 % ethanol added", size=26, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.2, 0])
        with self.say("This is chloroform, trichloromethane. In eighteen forty seven it became one of the first general anaesthetics. Look at how it is stored. Always in a dark brown bottle. Always filled right to the brim. And always with about one percent of ethanol added."):
            self.play(FadeIn(bot, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in facts], lag_ratio=0.5), run_time=3)
        nb = C.show_neby(self, "think", height=1.5, at=[0, -2.4, 0])
        with self.say("Why all three precautions? What could light, air and a little alcohol possibly have to do with a bottle of solvent? The answer is a poison gas used in the First World War. We will meet it at the very end of this lesson."):
            self.play(Indicate(facts[1:], color=th.AMBER))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(bot, facts)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 8: Haloalkanes, the first unit of organic chemistry. Alkanes with a halogen attached. One polar bond, between carbon and halogen, explains almost everything they do."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. Naming, isomers and classes of haloalkanes. How to prepare them. Their physical properties. The two great mechanisms, S N one and S N two. Eight substitution products from one reaction. Elimination, reduction and the Wurtz reaction. And finally chloroform: how it is made, and how it reacts.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        gen = VGroup(chem(r"R{-}X", size=72, color=th.AMBER), M(r"\mathrm{C_nH_{2n+1}X}", size=48)).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        with self.say("A haloalkane, or alkyl halide, is an alkane with a hydrogen replaced by a halogen. A monohaloalkane has one halogen, general formula C n H two n plus one X, written R X."):
            self.play(Write(gen))
        rows = [["Structure", "IUPAC name", "Common name"], ["CH₃Cl", "chloromethane", "methyl chloride"], ["CH₃CH₂Br", "bromoethane", "ethyl bromide"],
                ["(CH₃)₂CHCl", "2-chloropropane", "isopropyl chloride"], ["(CH₃)₃CBr", "2-bromo-2-methylpropane", "tert-butyl bromide"],
                ["CH₃CH(CH₃)CH₂Cl", "1-chloro-2-methylpropane", "isobutyl chloride"]]
        tb = C.table(rows, [3.6, 4.6, 3.6], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.BODY]).next_to(gen, DOWN, buff=0.45)
        with self.say("In I U P A C names the halogen is a prefix, fluoro, chloro, bromo, iodo, on the longest chain containing it, numbered to give the lowest locants. The common name is simply the alkyl group followed by halide.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(VGroup(gen, tb)))
        prim = skeleton([(0, 0), (1, 0.5), (2, 0)], [(0, 1), (1, 2)], (2, 1.0, 0.5), center=[-5.6, 0.4, 0], scale=1.05)
        sec = skeleton([(0, 0), (1, 0.5), (2, 0)], [(0, 1), (1, 2)], (1, 0, 1.1), center=[-1.05, 0.0, 0], scale=1.05)
        tert = skeleton([(0, 0), (1, 0.5), (2, 0), (1, 1.6)], [(0, 1), (1, 2), (1, 3)], (1, 0.9, -0.6), center=[3.2, -0.2, 0], scale=1.05)
        labs = VGroup(*[VGroup(T(a, size=30, color=c, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, buff=0.08).move_to([x, -2.0, 0])
                        for a, b, c, x in [("primary 1°", "C–X carbon joined to 1 carbon", th.SKY, -4.3), ("secondary 2°", "joined to 2 carbons", th.AMBER, 0.0), ("tertiary 3°", "joined to 3 carbons", th.CORAL, 4.3)]])
        with self.say("Haloalkanes are classified by the carbon that carries the halogen. If that carbon is joined to one other carbon, it is primary. Two others, secondary. Three, tertiary. This is not just bookkeeping. It decides the mechanism: primary halides react by S N two, tertiary ones by S N one."):
            self.play(GrowFromCenter(prim), FadeIn(labs[0]))
            self.play(GrowFromCenter(sec), FadeIn(labs[1]))
            self.play(GrowFromCenter(tert), FadeIn(labs[2]))
        self.play(FadeOut(VGroup(prim, sec, tert, labs)))
        title = T("C₄H₉Br: four structural isomers", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        iso = [skeleton([(0, 0), (1, 0.5), (2, 0), (3, 0.5)], [(0, 1), (1, 2), (2, 3)], (3, 0.9, 0), scale=0.6),
               skeleton([(0, 0), (1, 0.5), (2, 0), (3, 0.5)], [(0, 1), (1, 2), (2, 3)], (2, 0, -1.0), scale=0.6),
               skeleton([(0, 0), (1, 0.5), (2, 0), (1, 1.5)], [(0, 1), (1, 2), (1, 3)], (2, 0.9, -0.4), scale=0.6),
               skeleton([(0, 0), (1, 0.5), (2, 0), (1, 1.5)], [(0, 1), (1, 2), (1, 3)], (1, 0.9, -0.7), scale=0.6)]
        names = [("1-bromobutane", "1°"), ("2-bromobutane", "2° · chiral"), ("1-bromo-2-methylpropane", "1°"), ("2-bromo-2-methylpropane", "3°")]
        grid = VGroup()
        for m, (n, c) in zip(iso, names):
            grid.add(VGroup(m.scale(1.3), T(n, size=24, color=th.INK), T(c, size=22, color=th.AMBER)).arrange(DOWN, buff=0.25))
        grid.arrange_in_grid(rows=2, cols=2, buff=(1.6, 0.4)).next_to(title, DOWN, buff=0.4)
        kinds = VGroup(T("chain isomers: different skeleton", size=24, color=th.SKY), T("position isomers: halogen moves along the chain", size=24, color=th.MINT),
                       T("optical isomers: 2-bromobutane has a carbon with four different groups", size=24, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.say("Haloalkanes show chain isomerism, position isomerism, and optical isomerism. C four H nine B r has exactly four structural isomers, asked year after year: one bromobutane, two bromobutane, one bromo two methyl propane, and two bromo two methyl propane. Two bromobutane also has a carbon carrying four different groups, so it exists as a pair of mirror image optical isomers.") as v:
            self.play(FadeIn(title))
            for g_ in grid:
                self.play(FadeIn(g_, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur / 6 - 0.55)
            self.play(FadeIn(kinds))
        self.play(FadeOut(VGroup(title, grid, kinds)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("From alkanes: free-radical halogenation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"CH_4 + Cl_2 \xrightarrow{UV} CH_3Cl + HCl", size=44).next_to(title, DOWN, buff=0.35)
        steps_ = VGroup(
            VGroup(T("initiation", size=24, color=th.AMBER, weight="BOLD"), chem(r"Cl_2 \xrightarrow{h\nu} 2Cl\bullet", size=38)),
            VGroup(T("propagation", size=24, color=th.SKY, weight="BOLD"), chem(r"CH_4 + Cl\bullet \rightarrow CH_3\bullet + HCl;\ \ CH_3\bullet + Cl_2 \rightarrow CH_3Cl + Cl\bullet", size=34)),
            VGroup(T("termination", size=24, color=th.CORAL, weight="BOLD"), chem(r"CH_3\bullet + Cl\bullet \rightarrow CH_3Cl;\ \ 2Cl\bullet \rightarrow Cl_2;\ \ 2CH_3\bullet \rightarrow C_2H_6", size=34)))
        for r in steps_:
            r.arrange(RIGHT, buff=0.4)
        steps_.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.45)
        with self.say("From alkanes, by free radical halogenation in ultraviolet light. Light splits a chlorine molecule into two radicals, initiation. A chlorine radical pulls a hydrogen off methane, making a methyl radical, which grabs chlorine and releases a new chlorine radical. That loop, propagation, repeats thousands of times. It ends when two radicals meet, termination.") as v:
            self.play(FadeIn(title), Write(eq))
            for r in steps_:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
                self.hold(v.dur / 3 - 0.8)
        poor = T("a poor lab method: CH₂Cl₂, CHCl₃, CCl₄ and position isomers also form", size=24, color=th.CORAL).to_edge(DOWN, buff=0.5)
        with self.say("It is cheap but messy: the product is attacked again, giving dichloromethane, chloroform and carbon tetrachloride, and bigger alkanes give mixtures of isomers. Fluorination is explosive and iodination reversible, so only chlorine and bromine are useful."):
            self.play(FadeIn(poor))
        self.play(FadeOut(VGroup(title, eq, steps_, poor)))
        title = T("From alkenes: adding HX", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e1 = chem(r"CH_3CH{=}CH_2 + HBr \rightarrow CH_3CHBrCH_3\ \ (\text{major})", size=40).next_to(title, DOWN, buff=0.5)
        mk = T("Markovnikov: H goes to the carbon that already has more H", size=26, color=th.AMBER).next_to(e1, DOWN, buff=0.3)
        cat = VGroup(chem(r"CH_3\overset{+}{C}HCH_3\ \ 2^{\circ}\ \text{cation: more stable}", size=40, color=th.MINT), chem(r"CH_3CH_2\overset{+}{C}H_2\ \ 1^{\circ}\ \text{cation: less stable}", size=40, color=th.MUTED)).arrange(DOWN, buff=0.25).next_to(mk, DOWN, buff=0.4)
        with self.say("From alkenes, by adding a hydrogen halide. Propene with hydrogen bromide gives mainly two bromopropane. Markovnikov's rule: the hydrogen goes to the double bonded carbon that already has more hydrogens. The reason is the intermediate: the secondary carbocation is more stable than the primary one."):
            self.play(FadeIn(title), Write(e1))
            self.play(FadeIn(mk))
            self.play(FadeIn(cat, shift=UP * 0.2))
        e2 = chem(r"CH_3CH{=}CH_2 + HBr \xrightarrow{\text{peroxide}} CH_3CH_2CH_2Br", size=38, color=th.SKY).to_edge(DOWN, buff=0.9)
        k2 = T("Kharasch peroxide effect: HBr only (free-radical path)", size=24, color=th.SKY).next_to(e2, DOWN, buff=0.2)
        with self.say("But add a peroxide, and hydrogen bromide adds the other way, giving one bromopropane. This is the Kharasch or peroxide effect. It works only for hydrogen bromide, because the mechanism switches to free radicals."):
            self.play(Write(e2), FadeIn(k2))
        self.play(FadeOut(VGroup(title, e1, mk, cat, e2, k2)))
        rows = [["Reagent", "Equation", "Note"], ["conc. HCl + ZnCl₂", "C₂H₅OH + HCl → C₂H₅Cl + H₂O", "Lucas reagent"], ["NaBr + conc. H₂SO₄", "C₂H₅OH + HBr → C₂H₅Br + H₂O", "HBr made in situ"],
                ["red P + I₂", "3C₂H₅OH + PI₃ → 3C₂H₅I + H₃PO₃", ""], ["PCl₅", "C₂H₅OH + PCl₅ → C₂H₅Cl + POCl₃ + HCl", ""],
                ["SOCl₂", "C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑", "Darzen: the best"]]
        tb = C.table(rows, [3.4, 6.6, 2.8], row_h=0.62, size=22, colors=[th.AMBER, th.INK, th.MUTED]).move_to(UP * 0.6)
        with self.say("The standard laboratory route is from alcohols, because it gives one clean product. Hydrochloric acid with zinc chloride, the Lucas reagent. Sodium bromide with sulphuric acid. Red phosphorus and iodine. Phosphorus pentachloride. And best of all, thionyl chloride, Darzen's process, because both by products are gases that simply escape.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
            self.play(Indicate(tb[5], color=th.MINT, scale_factor=1.02))
        lucas = VGroup(T("Lucas test (ease 3° > 2° > 1°):", size=24, color=th.INK, weight="BOLD"), T("3° turbid at once · 2° in about 5 min · 1° only on heating", size=26, color=th.BODY)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.5)
        with self.say("The ease of replacing the hydroxyl group is tertiary, then secondary, then primary. That is the Lucas test: a tertiary alcohol turns cloudy at once, secondary in about five minutes, primary only on heating."):
            self.play(FadeIn(lucas))
        self.play(FadeOut(VGroup(tb, lucas)))
        f1 = VGroup(T("Finkelstein", size=30, color=th.SKY, weight="BOLD"), chem(r"R{-}Cl + NaI \xrightarrow{\text{dry acetone}} R{-}I + NaCl\downarrow", size=34),
                    T("NaCl is insoluble in acetone, so it drops out and drives the reaction", size=22, color=th.BODY)).arrange(DOWN, buff=0.2)
        f2 = VGroup(T("Swarts", size=30, color=th.MINT, weight="BOLD"), chem(r"CH_3Br + AgF \rightarrow CH_3F + AgBr", size=34),
                    T("how fluoroalkanes and freons are made (also Hg₂F₂, SbF₃)", size=22, color=th.BODY)).arrange(DOWN, buff=0.2)
        VGroup(f1, f2).arrange(DOWN, buff=0.7)
        with self.say("Two named reactions swap one halogen for another. The Finkelstein reaction makes iodides from chlorides with sodium iodide in dry acetone, where the sodium chloride precipitates and drives the change. The Swarts reaction makes fluorides with silver fluoride, which is how freons are made."):
            self.play(FadeIn(f1, shift=UP * 0.2))
            self.play(FadeIn(f2, shift=UP * 0.2))
        self.play(FadeOut(VGroup(f1, f2)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        title = T("Boiling points", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        data = [("CH₃F", -78), ("CH₃Cl", -24), ("CH₃Br", 4), ("CH₃I", 42)]
        base = -2.3
        bars = VGroup()
        for i, (n, bp) in enumerate(data):
            h = (bp + 90) * 0.025
            b = Rectangle(width=1.0, height=h, fill_color=[th.MINT, CL, BR, th.PINK][i], fill_opacity=0.85, stroke_width=0).move_to([-5.6 + 1.35 * i, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, T(f"{bp} °C", size=20, color=th.INK).next_to(b, UP, buff=0.08), T(n, size=22, color=th.BODY).next_to([-5.6 + 1.35 * i, base, 0], DOWN, buff=0.12)))
        notes = VGroup(T("RI > RBr > RCl > RF: heavier, more polarisable halogen", size=22, color=th.BODY), T("longer chain: higher b.p.", size=22, color=th.BODY),
                       T("branching LOWERS b.p.: more spherical, less contact", size=22, color=th.BODY), T("insoluble in water; RBr and RI sink", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -0.2, 0])
        with self.say("Haloalkanes are colourless liquids with a sweetish smell, apart from the first few, which are gases. Boiling points rise from fluoride to iodide, because a bigger, more polarisable halogen gives stronger van der Waals forces. They rise with chain length, and fall with branching, since a branched molecule is more spherical and touches its neighbours less. They do not dissolve in water, and the bromides and iodides are denser than water.") as v:
            self.play(FadeIn(title))
            for b in bars:
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1:]), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(n_, shift=LEFT * 0.2) for n_ in notes], lag_ratio=0.4), run_time=2)
        self.play(FadeOut(VGroup(title, bars, notes)))
        title = T("Dipole moments: a trap", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        dm = [("CH₃Cl", 1.86), ("CH₃F", 1.85), ("CH₃Br", 1.79), ("CH₃I", 1.64)]
        bars = VGroup()
        for i, (n, d) in enumerate(dm):
            b = Rectangle(width=d * 3.0, height=0.6, fill_color=th.AMBER if i == 0 else th.SKY, fill_opacity=0.85, stroke_width=0).move_to([-3.0, 1.2 - 0.85 * i, 0], aligned_edge=LEFT)
            bars.add(VGroup(b, T(n, size=24, color=th.INK).next_to(b, LEFT, buff=0.2), T(f"{d} D", size=22, color=th.INK).next_to(b, RIGHT, buff=0.15)))
        why = para("Fluorine is the most electronegative, but the C–F bond is so short that the charges sit close together. Dipole moment = charge × distance, so CH₃Cl wins.", width=11, size=26, color=th.BODY).to_edge(DOWN, buff=0.5)
        nb = C.show_neby(self, "surprised", height=1.3, corner=UR, buff=0.9)
        self.play(FadeIn(title))
        with self.say("A favourite short question. Which methyl halide has the largest dipole moment? Not the fluoride, even though fluorine is the most electronegative. Chloromethane, one point eight six debye. The carbon fluorine bond is so short that the charges are close together, and dipole moment is charge times distance."):
            for b in bars:
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1:]), run_time=0.5)
            self.play(FadeIn(why))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, bars, why)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        cpos = np.array([-1.0, 0.4, 0])
        cc = C.atom("C", r=0.35).move_to(cpos)
        xx = C.atom("Br", r=0.42, color=BR).move_to(cpos + RIGHT * 1.6)
        bond = Line(cpos, cpos + RIGHT * 1.6, color=th.MUTED, stroke_width=6)
        d1 = M(r"\delta+", size=40, color=th.SKY).next_to(cc, UP, buff=0.15)
        d2 = M(r"\delta-", size=40, color=th.CORAL).next_to(xx, UP, buff=0.15)
        nu = VGroup(Circle(radius=0.38, fill_color=OHC, fill_opacity=1, stroke_width=0), T("OH⁻", size=22, color=WHITE, weight="BOLD")).move_to(cpos + LEFT * 3.2)
        with self.say("Everything haloalkanes do starts with one polar bond. Halogen is more electronegative than carbon, so the carbon is slightly positive and the halogen slightly negative. A nucleophile, an electron rich species like hydroxide, cyanide or ammonia, attacks that positive carbon, and the halide leaves with the bonding pair. This is nucleophilic substitution."):
            self.play(FadeIn(cc), FadeIn(xx), Create(bond))
            self.play(FadeIn(d1), FadeIn(d2))
            self.play(FadeIn(nu, shift=RIGHT * 0.3))
            self.play(nu.animate.shift(RIGHT * 1.2), run_time=1.0)
        self.play(FadeOut(VGroup(cc, xx, bond, d1, d2, nu)))
        rows = [["Bond", "C–F", "C–Cl", "C–Br", "C–I"], ["length / pm", "139", "178", "193", "214"], ["enthalpy / kJ mol⁻¹", "452", "351", "293", "234"], ["reactivity", "least", "", "", "greatest"]]
        tb = C.table(rows, [3.6, 1.8, 1.8, 1.8, 1.8], row_h=0.7, size=26, colors=[th.MUTED, th.INK, th.INK, th.INK, th.AMBER]).move_to(UP * 0.5)
        ordr = T("R–I > R–Br > R–Cl > R–F: the weakest bond breaks most easily", size=28, color=th.AMBER).next_to(tb, DOWN, buff=0.45)
        with self.say("The carbon halogen bond gets longer and weaker down the group, so iodide is the best leaving group and iodoalkanes react fastest, even though iodine is the least electronegative."):
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(ordr))
        self.play(FadeOut(VGroup(tb, ordr)))
        self.sn2()
        self.sn1()
        self.compare()
        self.example_81()

    def sn2(self):
        title = T("SN2: one step, backside attack", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        t = ValueTracker(0)
        c = np.array([0, -0.3, 0])
        angs = [PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3]
        cols = [th.SKY, th.MINT, th.AMBER]
        labs = ["H", "CH₃", "C₂H₅"]
        balls = [VGroup(Circle(radius=0.4, fill_color=col, fill_opacity=1, stroke_width=0), T(lab, size=20, color=th.BG, weight="BOLD")) for col, lab in zip(cols, labs)]
        nub_ = VGroup(Circle(radius=0.38, fill_color=OHC, fill_opacity=1, stroke_width=0), T("OH⁻", size=20, color=WHITE, weight="BOLD"))
        lgb_ = VGroup(Circle(radius=0.45, fill_color=BR, fill_opacity=1, stroke_width=0), T("Br", size=22, color=WHITE, weight="BOLD"))
        cat_ = C.atom("C", r=0.32)

        def mol():
            s = t.get_value()
            flip = np.clip((s - 0.35) / 0.4, 0, 1)
            g = VGroup()
            for a, ball in zip(angs, balls):
                yz = np.array([0, np.sin(a), np.cos(a)])
                x = 0.85 * (1 - 2 * flip)
                p = c + np.array([x, 1.5 * yz[1], 0]) + np.array([0.35 * yz[2], 0, 0])
                g.add(Line(c, p, color=th.MUTED, stroke_width=5))
                g.add(ball.copy().move_to(p))
            nu_x = -5.0 + 3.2 * np.clip(s / 0.5, 0, 1)
            lg_x = 1.8 + 3.2 * np.clip((s - 0.5) / 0.5, 0, 1)
            nup = c + np.array([nu_x, 0, 0])
            lgp = c + np.array([lg_x, 0, 0])
            nub = 1 - abs(np.clip(s / 0.5, 0, 1) - 1) if s < 1 else 1
            g.add(DashedLine(nup + RIGHT * 0.4, c + LEFT * 0.3, color=OHC, stroke_width=3, stroke_opacity=np.clip(s * 3, 0, 1)) if s > 0.15 else VGroup())
            g.add(DashedLine(c + RIGHT * 0.3, lgp + LEFT * 0.45, color=BR, stroke_width=3, stroke_opacity=1) if s > 0.3 else Line(c, lgp, color=th.MUTED, stroke_width=5))
            g.add(nub_.copy().move_to(nup))
            g.add(lgb_.copy().move_to(lgp))
            g.add(cat_.copy().move_to(c))
            return g
        m = always_redraw(mol)
        rate = M(r"\text{rate} = k[\mathrm{RX}][\mathrm{OH^-}]", size=40, color=th.AMBER).to_edge(DOWN, buff=0.9)
        with self.say("S N two: substitution, nucleophilic, bimolecular. It happens in one step. The hydroxide comes in from the side exactly opposite the bromine, backside attack."):
            self.play(FadeIn(title))
            self.add(m)
            self.play(t.animate.set_value(0.42), run_time=3.0, rate_func=smooth)
        ts = T("transition state: five groups around carbon, three in a plane", size=24, color=th.AMBER).next_to(title, DOWN, buff=0.3)
        with self.say("Halfway, carbon is partly bonded to both: the transition state, with the three other groups flat in a plane. Then the bromide leaves, and the three groups snap through to the other side, like an umbrella turning inside out in the wind."):
            self.play(FadeIn(ts))
            self.play(t.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        wi = T("Walden inversion: the product has the opposite configuration", size=26, color=th.MINT).next_to(ts, DOWN, buff=0.2)
        with self.say("The product has the opposite configuration. This is Walden inversion, the proof of the S N two mechanism. Because both the haloalkane and the nucleophile are in the single step, the rate equals k times both concentrations: second order."):
            self.play(FadeIn(wi))
            self.play(Write(rate))
        self.play(FadeOut(VGroup(title, ts, wi, rate)), FadeOut(m))
        self.remove(m)

    def sn1(self):
        title = T("SN1: two steps, via a carbocation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        c = np.array([-0.5, -0.2, 0])
        t = ValueTracker(0)
        me_ = [VGroup(Circle(radius=0.4, fill_color=col, fill_opacity=1, stroke_width=0), T("CH₃", size=20, color=th.BG, weight="BOLD")) for col in (th.SKY, th.MINT, th.AMBER)]
        br0 = VGroup(Circle(radius=0.45, fill_color=BR, fill_opacity=1, stroke_width=0), T("Br", size=22, color=WHITE, weight="BOLD"))
        br1 = VGroup(Circle(radius=0.45, fill_color=BR, fill_opacity=1, stroke_width=0), T("Br⁻", size=22, color=WHITE, weight="BOLD"))
        ca_ = C.atom("C", r=0.32)
        plus_ = T("+", size=34, color=th.AMBER, weight="BOLD")

        def mol():
            s = t.get_value()
            g = VGroup()
            tilt = 0.35 * (1 - np.clip(s / 0.6, 0, 1))
            for k, ball in enumerate(me_):
                a = PI / 2 + k * TAU / 3
                p = c + np.array([-tilt * 1.5, 1.5 * np.sin(a), 0]) + np.array([0.5 * np.cos(a), 0, 0])
                g.add(Line(c, p, color=th.MUTED, stroke_width=5))
                g.add(ball.copy().move_to(p))
            bx = 1.5 + 3.0 * np.clip(s / 0.6, 0, 1)
            bp = c + np.array([bx, 0, 0])
            if s < 0.15:
                g.add(Line(c, bp, color=th.MUTED, stroke_width=5))
            g.add((br1 if s > 0.3 else br0).copy().move_to(bp))
            g.add(ca_.copy().move_to(c))
            if s > 0.5:
                g.add(plus_.copy().move_to(c + UR * 0.35))
            return g
        m = always_redraw(mol)
        s1 = T("step 1 (slow): C–Br breaks on its own → flat carbocation", size=26, color=th.CORAL).next_to(title, DOWN, buff=0.3)
        with self.say("S N one: substitution, nucleophilic, unimolecular, typical of tertiary halides like tertiary butyl bromide. It happens in two steps. First, slowly, the carbon bromine bond breaks all by itself, leaving a carbocation. The carbocation is flat."):
            self.play(FadeIn(title))
            self.add(m)
            self.play(FadeIn(s1))
            self.play(t.animate.set_value(1), run_time=3, rate_func=smooth)
        top = VGroup(Circle(radius=0.38, fill_color=OHC, fill_opacity=1, stroke_width=0), T("OH⁻", size=20, color=WHITE, weight="BOLD")).move_to(c + LEFT * 3.0)
        bot = top.copy().move_to(c + RIGHT * 2.2 + DOWN * 1.3)
        s2 = T("step 2 (fast): OH⁻ attacks either face → 50 : 50, racemisation", size=26, color=th.MINT).next_to(s1, DOWN, buff=0.15)
        rate = M(r"\text{rate} = k[\mathrm{RX}]\ \ (\text{no } [\mathrm{OH^-}]!)", size=40, color=th.AMBER).to_edge(DOWN, buff=0.9)
        with self.say("Second, quickly, the nucleophile attacks. Because the carbocation is flat, it can attack from either face with equal ease, so a single enantiomer gives a fifty fifty mixture of both products: racemisation. And since hydroxide only arrives after the slow step, it does not appear in the rate law at all. Rate equals k times the haloalkane concentration only."):
            self.play(FadeIn(s2), FadeIn(top), FadeIn(bot))
            self.play(top.animate.move_to(c + LEFT * 1.05), bot.animate.move_to(c + RIGHT * 1.05 + DOWN * 0.2), run_time=1.2)
            self.play(Write(rate))
        self.play(FadeOut(VGroup(title, s1, s2, top, bot, rate)), FadeOut(m))
        self.remove(m)
        ax = Arrow([-6.0, -2.8, 0], [-6.0, 2.4, 0], buff=0, color=th.MUTED, stroke_width=3)
        el = T("energy", size=20, color=th.MUTED).next_to(ax, UP, buff=0.05)
        c1 = profile(0.6, [(-2.0, 3.6)], 0.2, x0=-5.8, x1=-0.4, sc=1.0)
        c2 = profile(0.6, [(2.4, 3.8), (3.6, 2.4), (4.8, 3.2)], 0.2, x0=0.6, x1=6.2, sc=1.0)
        l1 = T("SN2: one hump, no intermediate", size=22, color=th.SKY).move_to([-3.1, 1.8, 0])
        l2 = T("SN1: two humps; the well is the carbocation", size=22, color=th.CORAL).move_to([3.4, 1.9, 0])
        well = Dot([3.6, -2.6 + 2.4, 0], color=th.AMBER, radius=0.12)
        with self.say("On energy profiles the difference is clear. S N two has one hump, a single transition state, no intermediate. S N one has two humps with a well between them. That well is the carbocation, a real, if short lived, species."):
            self.play(GrowArrow(ax), FadeIn(el))
            self.play(Create(c1), FadeIn(l1))
            self.play(Create(c2), FadeIn(l2))
            self.play(FadeIn(well, scale=2))
        self.play(FadeOut(VGroup(ax, el, c1, c2, l1, l2, well)))

    def compare(self):
        rows = [["", "SN1", "SN2"], ["steps", "two", "one"], ["rate law", "k[RX]", "k[RX][Nu⁻]"], ["intermediate", "carbocation", "none"],
                ["stereochemistry", "racemisation", "inversion (Walden)"], ["favoured by", "3° > 2° > 1°", "CH₃X > 1° > 2° > 3°"], ["nucleophile", "weak", "strong, concentrated"],
                ["solvent", "polar protic (water, ethanol)", "polar aprotic (acetone, DMSO)"]]
        tb = C.table(rows, [3.2, 4.6, 4.8], row_h=0.6, size=23, colors=[th.MUTED, th.CORAL, th.SKY]).move_to(UP * 0.4)
        with self.say("Here is the whole comparison. Two steps against one. Rate depending on the haloalkane only, against both. A carbocation against no intermediate. Racemisation against inversion. Tertiary halides favour S N one, methyl and primary favour S N two. Weak nucleophiles and protic solvents like water favour S N one. Strong nucleophiles and aprotic solvents like acetone favour S N two.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 8 - 0.4)
        self.play(FadeOut(tb))
        care = self.callout("careful", "The two reactivity orders are opposite. SN1: 3° > 2° > 1° (most stable carbocation). SN2: CH₃X > 1° > 2° > 3° (bulky groups block the backside: steric hindrance). Only the leaving-group order, I > Br > Cl > F, is the same for both.", width=11, size=26)
        with self.say("Do not mix up the two orders. For S N one, tertiary is fastest, because three alkyl groups stabilise the carbocation. For S N two it is exactly reversed, because three bulky groups block the backside attack. That is steric hindrance. Only the leaving group order is the same for both."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))

    def example_81(self):
        head, prob = C.example_head(self, "CH₃Br + OH⁻ has rate 2.0 × 10⁻⁴ mol L⁻¹ s⁻¹ when [CH₃Br] = [OH⁻] = 0.10 M. (a) Find k. (b) Rate if [OH⁻] alone is doubled? (c) The same for 2-bromo-2-methylpropane?")
        st = C.steps(r"(a)\ \text{SN2: rate} = k[\mathrm{CH_3Br}][\mathrm{OH^-}] \Rightarrow k = \frac{2.0\times10^{-4}}{0.10\times0.10} = 2.0\times10^{-2}\ \mathrm{L\,mol^{-1}s^{-1}}",
                     r"(b)\ \text{rate} = 2.0\times10^{-2}\times0.10\times0.20 = 4.0\times10^{-4}\ \text{(doubled)}",
                     r"(c)\ 3^{\circ}\Rightarrow \text{SN1: rate} = k[\mathrm{RBr}] \Rightarrow \text{unchanged}", size=34).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example eight point one. Bromomethane is a methyl halide, so S N two, with rate equals k times both concentrations. k is two times ten to the minus four over zero point one times zero point one: two times ten to the minus two. Doubling hydroxide doubles the rate, to four times ten to the minus four. But for the tertiary halide, the mechanism is S N one, hydroxide is not in the rate law, and doubling it changes nothing."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("Which statement about the SN1 reaction of (CH₃)₃CBr with OH⁻ is correct?",
                  ["rate doubles if [OH⁻] doubles", "it gives inversion of configuration", "it goes through a carbocation", "it is a one-step reaction"], 2,
                  "Pause and think. Tertiary butyl bromide with hydroxide, by S N one. Which statement is true?",
                  "C, it goes through a carbocation. The rate does not depend on hydroxide at all, so A is wrong. Inversion and a single step are features of S N two, not S N one.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        rows = [["Reagent", "Nucleophile", "Product from C₂H₅Br", "Class"],
                ["KOH(aq), warm / moist Ag₂O", "OH⁻", "C₂H₅OH", "alcohol"],
                ["KCN, alcoholic", "C≡N⁻ via C", "C₂H₅CN", "nitrile"],
                ["AgCN, alcoholic", "via N", "C₂H₅NC", "isocyanide"],
                ["NH₃, excess, sealed tube", "NH₃", "C₂H₅NH₂", "1° amine"],
                ["C₂H₅ONa, dry (Williamson)", "C₂H₅O⁻", "C₂H₅OC₂H₅", "ether"],
                ["C₂H₅SNa", "C₂H₅S⁻", "C₂H₅SC₂H₅", "thioether"],
                ["KNO₂", "O–N=O⁻ via O", "C₂H₅–O–N=O", "alkyl nitrite"],
                ["AgNO₂", "via N", "C₂H₅NO₂", "nitroalkane"]]
        tb = C.table(rows, [4.6, 2.6, 3.4, 2.4], row_h=0.6, size=22, colors=[th.AMBER, th.SKY, th.INK, th.MINT]).move_to(UP * 0.2)
        with self.say("Every reaction in this table is the same reaction: nucleophilic substitution on bromoethane, with eight different nucleophiles. Aqueous potassium hydroxide gives ethanol. Potassium cyanide gives a nitrile. Silver cyanide gives an isocyanide. Excess ammonia gives an amine. Sodium ethoxide gives an ether, the Williamson synthesis. A thiolate gives a thioether. Potassium nitrite gives an alkyl nitrite, and silver nitrite a nitroalkane.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 9 - 0.38)
        self.play(FadeOut(tb))
        title = T("The silver-salt rule", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cn1 = VGroup(T("K⁺", size=30, color=C.EL["K"], weight="BOLD"), T("  ⁻C≡N", size=34, color=th.INK, weight="BOLD")).arrange(RIGHT, buff=0.2).move_to([-3.4, 1.4, 0])
        cn2 = VGroup(T("Ag–C≡N", size=34, color=th.INK, weight="BOLD")).move_to([3.4, 1.4, 0])
        a1 = Arrow(cn1[1].get_left() + DOWN * 0.3, [-3.4, -0.4, 0], buff=0.1, color=th.AMBER, stroke_width=5)
        a2 = Arrow(cn2.get_right() + DOWN * 0.3 + LEFT * 0.4, [3.4, -0.4, 0], buff=0.1, color=th.SKY, stroke_width=5)
        r1 = VGroup(chem(r"C_2H_5{-}C{\equiv}N", size=52, color=th.AMBER), T("attacks through C: nitrile", size=24, color=th.AMBER)).arrange(DOWN, buff=0.15).move_to([-3.4, -1.0, 0])
        r2 = VGroup(chem(r"C_2H_5{-}N{\equiv}C", size=52, color=th.SKY), T("attacks through N: isocyanide", size=24, color=th.SKY)).arrange(DOWN, buff=0.15).move_to([3.4, -1.0, 0])
        h1 = T("ionic", size=26, color=th.MUTED).next_to(cn1, UP, buff=0.2)
        h2 = T("covalent", size=26, color=th.MUTED).next_to(cn2, UP, buff=0.2)
        rule = T("potassium → through C or O;  silver → through N", size=30, color=th.MINT, weight="BOLD").to_edge(DOWN, buff=0.6)
        with self.say("Why do potassium and silver salts give different products? Cyanide and nitrite can attack through two different atoms. Potassium cyanide is ionic: the free cyanide ion attacks through carbon, the atom carrying the charge, giving a nitrile. Silver cyanide is largely covalent: the carbon is tied up in the bond to silver, so attack must come through nitrogen, giving an isocyanide. Nitrite is just the same: potassium nitrite attacks through oxygen, silver nitrite through nitrogen. Potassium, carbon or oxygen. Silver, nitrogen. This is asked every single year."):
            self.play(FadeIn(title), FadeIn(cn1), FadeIn(h1))
            self.play(GrowArrow(a1), FadeIn(r1))
            self.play(FadeIn(cn2), FadeIn(h2))
            self.play(GrowArrow(a2), FadeIn(r2))
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, cn1, cn2, a1, a2, r1, r2, h1, h2, rule)))
        am = para("Ammonolysis does not stop: the amine formed is itself a nucleophile, giving 2° and 3° amines and finally a quaternary salt. A large excess of NH₃ favours the 1° amine.", width=11.5, size=28, color=th.BODY)
        with self.say("One more note. With ammonia, the amine formed is itself a nucleophile, so it keeps reacting, giving secondary and tertiary amines and finally a quaternary ammonium salt. A large excess of ammonia keeps the product mostly primary."):
            self.play(FadeIn(am))
        self.play(FadeOut(am))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Same KOH, two solvents, two products", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        top = chem(r"CH_3CH_2Br", size=48).move_to([0, 1.6, 0])
        a1 = Arrow([-0.8, 1.2, 0], [-3.6, -0.2, 0], buff=0, color=th.SKY, stroke_width=5)
        a2 = Arrow([0.8, 1.2, 0], [3.6, -0.2, 0], buff=0, color=th.CORAL, stroke_width=5)
        l1 = T("KOH in water", size=26, color=th.SKY, weight="BOLD").next_to(a1.get_center(), UL, buff=0.1)
        l2 = T("KOH in alcohol, heat", size=26, color=th.CORAL, weight="BOLD").next_to(a2.get_center(), UR, buff=0.1)
        p1 = VGroup(chem(r"CH_3CH_2OH", size=44, color=th.SKY), T("OH⁻ acts as a nucleophile: substitution", size=22, color=th.BODY)).arrange(DOWN, buff=0.15).move_to([-3.8, -1.0, 0])
        p2 = VGroup(chem(r"CH_2{=}CH_2 + KBr + H_2O", size=40, color=th.CORAL), T("OH⁻ acts as a base: β-elimination", size=22, color=th.BODY)).arrange(DOWN, buff=0.15).move_to([3.8, -1.0, 0])
        with self.say("Now a classic trap. The same reagent, potassium hydroxide, gives two different products depending on the solvent. In water, hydroxide acts as a nucleophile, and bromoethane gives ethanol: substitution. In hot alcohol, hydroxide acts as a base. It pulls off a hydrogen from the carbon next to the halogen, the beta carbon, and the molecule loses H B r to become ethene: elimination."):
            self.play(FadeIn(title), Write(top))
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(p1))
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(p2))
        nb = C.show_neby(self, "oops", height=1.3)
        with self.say("Aqueous gives the alcohol, alcoholic gives the alkene. Losing a mark here is the most avoidable mistake in the unit."):
            self.play(Indicate(VGroup(l1, l2), color=th.AMBER))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, top, a1, a2, l1, l2, p1, p2)))
        title = T("Saytzeff's rule", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        start = chem(r"CH_3CH_2CHBrCH_3", size=46).move_to([0, 1.5, 0])
        m1 = VGroup(chem(r"CH_3CH{=}CHCH_3", size=42, color=th.MINT), T("but-2-ene: 80 %, more substituted, major", size=22, color=th.MINT)).arrange(DOWN, buff=0.12).move_to([-3.4, -0.8, 0])
        m2 = VGroup(chem(r"CH_3CH_2CH{=}CH_2", size=42, color=th.MUTED), T("but-1-ene: 20 %, minor", size=22, color=th.MUTED)).arrange(DOWN, buff=0.12).move_to([3.4, -0.8, 0])
        a1 = Arrow([-0.6, 1.1, 0], [-3.0, -0.3, 0], buff=0, color=th.MINT, stroke_width=7)
        a2 = Arrow([0.6, 1.1, 0], [3.0, -0.3, 0], buff=0, color=th.MUTED, stroke_width=3)
        rule = T("the major alkene is the more substituted (more stable) one", size=26, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("When there are two different beta carbons, two alkenes are possible. Two bromobutane can lose a hydrogen from either side. Saytzeff's rule: the major product is the more substituted alkene, the one with more alkyl groups on the double bond, because it is more stable. So but two ene is major. The ease of elimination is tertiary, then secondary, then primary."):
            self.play(FadeIn(title), Write(start))
            self.play(GrowArrow(a1), FadeIn(m1))
            self.play(GrowArrow(a2), FadeIn(m2))
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(title, start, m1, m2, a1, a2, rule)))
        red = VGroup(T("Reduction", size=30, color=th.SKY, weight="BOLD"), chem(r"C_2H_5Br + 2[H] \xrightarrow{Zn/HCl} C_2H_6 + HBr", size=36),
                     T("also Zn–Cu couple, LiAlH₄, H₂/Ni", size=22, color=th.MUTED)).arrange(DOWN, buff=0.2).move_to(UP * 1.6)
        with self.say("Reduction replaces the halogen by hydrogen, giving back the alkane, using zinc and hydrochloric acid, a zinc copper couple, lithium aluminium hydride, or hydrogen over nickel."):
            self.play(FadeIn(red))
        w1 = VGroup(chem(r"C_2H_5", size=52, color=th.SKY), C.atom("Br", r=0.4, color=BR)).arrange(RIGHT, buff=0.12).move_to([-3.8, -0.8, 0])
        w2 = VGroup(C.atom("Br", r=0.4, color=BR), chem(r"C_2H_5", size=52, color=th.SKY)).arrange(RIGHT, buff=0.12).move_to([3.8, -0.8, 0])
        na = VGroup(*[VGroup(Circle(radius=0.36, fill_color=C.EL["Na"], fill_opacity=1, stroke_width=0), T("Na", size=22, color=WHITE, weight="BOLD")).move_to([x, -2.1, 0]) for x in (-1.6, 1.6)])
        eq = chem(r"2C_2H_5Br + 2Na \xrightarrow{\text{dry ether}} C_4H_{10} + 2NaBr", size=36, color=th.AMBER).to_edge(DOWN, buff=0.4)
        with self.say("The Wurtz reaction joins two molecules. Two bromoethane molecules with sodium in dry ether: the sodium takes both bromines, and the two ethyl groups bond together, giving butane. It doubles the carbon chain, so from a single halide it can only make alkanes with an even number of carbons. Mixing two halides gives a messy mixture of three alkanes."):
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(na))
            self.play(w1[1].animate.move_to(na[0].get_center() + UP * 0.55), w2[0].animate.move_to(na[1].get_center() + UP * 0.55), w1[0].animate.move_to([-0.75, -0.8, 0]), w2[1].animate.move_to([0.75, -0.8, 0]), run_time=1.6)
            bond = Line([-0.12, -0.8, 0], [0.12, -0.8, 0], color=th.AMBER, stroke_width=8)
            self.play(Create(bond), Write(eq))
        self.play(FadeOut(VGroup(red, w1, w2, na, eq, bond)))
        head, prob = C.example_head(self, "21.8 g of bromoethane is treated with excess sodium in dry ether. Find the mass and volume at STP of the alkane formed. (C 12, H 1, Br 80)")
        st = C.steps(r"M(\mathrm{C_2H_5Br}) = 24 + 5 + 80 = 109;\ \ n = \tfrac{21.8}{109} = 0.200\ \mathrm{mol}",
                     r"2\ \mathrm{C_2H_5Br} \rightarrow 1\ \mathrm{C_4H_{10}}:\ n = 0.100\ \mathrm{mol}",
                     r"m = 0.100 \times 58 = 5.8\ \mathrm{g},\quad V = 0.100 \times 22.4 = 2.24\ \mathrm{L}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example eight point two. Bromoethane has molar mass one hundred and nine, so we have zero point two moles. Two molecules make one butane, so zero point one mole of butane: five point eight grams, or two point two four litres at S T P."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "A monobromoalkane contains 58.4 % bromine by mass. Find its molecular formula. (C 12, H 1, Br 80)")
        st = C.steps(r"\mathrm{C_nH_{2n+1}Br}:\ M = 12n + (2n+1) + 80 = 14n + 81",
                     r"\frac{80}{14n + 81} = 0.584 \Rightarrow 14n + 81 = 137.0",
                     r"14n = 56.0 \Rightarrow n = 4:\ \ \mathrm{C_4H_9Br}", size=40).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example eight point three. A monobromoalkane has molar mass fourteen n plus eighty one. Eighty over that equals zero point five eight four, so fourteen n plus eighty one is one thirty seven, and n is four. C four H nine B r, whose four isomers we met at the start."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        bp = chem(r"CaOCl_2 + H_2O \rightarrow Ca(OH)_2 + Cl_2", size=40).to_edge(UP, buff=0.8)
        bl = T("bleaching powder supplies both the chlorine and the alkali", size=24, color=th.AMBER).next_to(bp, DOWN, buff=0.2)
        with self.say("Chloroform is made by the haloform reaction, using bleaching powder, which supplies both chlorine and the alkali, calcium hydroxide."):
            self.play(Write(bp), FadeIn(bl))
        r1 = VGroup(T("from ethanol: 3 steps", size=26, color=th.SKY, weight="BOLD"),
                    chem(r"CH_3CH_2OH + Cl_2 \rightarrow CH_3CHO + 2HCl\ \ (\text{oxidation})", size=36),
                    chem(r"CH_3CHO + 3Cl_2 \rightarrow CCl_3CHO\ (\text{chloral}) + 3HCl", size=36),
                    chem(r"2CCl_3CHO + Ca(OH)_2 \rightarrow 2CHCl_3 + (HCOO)_2Ca", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        r2 = VGroup(T("from propanone: 2 steps", size=26, color=th.MINT, weight="BOLD"),
                    chem(r"CH_3COCH_3 + 3Cl_2 \rightarrow CCl_3COCH_3 + 3HCl", size=36),
                    chem(r"2CCl_3COCH_3 + Ca(OH)_2 \rightarrow 2CHCl_3 + (CH_3COO)_2Ca", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(bl, DOWN, buff=0.35)
        rr = VGroup(r1, r2)
        if rr.width > 12.8:
            rr.scale_to_fit_width(12.8)
        with self.say("From ethanol it takes three steps. Chlorine first oxidises ethanol to ethanal. Then it replaces the three hydrogens of the methyl group, giving trichloroethanal, chloral. Finally calcium hydroxide splits chloral into chloroform and calcium methanoate.") as v:
            for line in r1:
                self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.65)
        with self.say("Propanone already has its carbonyl group, so no oxidation is needed. Just chlorination and hydrolysis: two steps and a better yield. That is why propanone is the preferred starting material."):
            for line in r2:
                self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(bp, bl, r1, r2)))
        pur = para("The crude chloroform distils with steam; it is shaken with conc. H₂SO₄, washed with dilute alkali and water, dried over anhydrous CaCl₂ and redistilled at 334 K.", width=11.5, size=26, color=th.BODY).move_to(UP * 1.6)
        with self.say("The crude product is purified by washing with concentrated sulphuric acid and dilute alkali, drying over calcium chloride, and redistilling at three hundred and thirty four kelvin."):
            self.play(FadeIn(pur))
        head, prob = C.example_head(self, "Chloroform is made from 9.20 g of ethanol by the bleaching-powder method. Find the theoretical mass, and the actual mass at 60 % yield. (C 12, H 1, O 16, Cl 35.5)")
        st = C.steps(r"1\ \mathrm{C_2H_5OH} \rightarrow 1\ \mathrm{CHCl_3};\ \ n = \tfrac{9.20}{46} = 0.200\ \mathrm{mol}",
                     r"M(\mathrm{CHCl_3}) = 12 + 1 + 3(35.5) = 119.5",
                     r"m = 0.200 \times 119.5 = 23.9\ \mathrm{g};\ \ 60\,\%:\ 0.60 \times 23.9 = 14.3\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        self.play(FadeOut(pur))
        with self.say("Worked example eight point four. One ethanol gives one chloroform over the three steps. Nine point two grams of ethanol is zero point two moles, so zero point two moles of chloroform, molar mass one nineteen point five: twenty three point nine grams in theory, and at sixty percent yield, fourteen point three grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        props = para("colourless, sweet-smelling, dense (1.49 g cm⁻³), b.p. 61 °C, non-inflammable, a solvent for fats and iodine", width=11.5, size=24, color=th.MUTED, align="center").to_edge(UP, buff=0.7)
        eq = chem(r"2CHCl_3 + O_2 \xrightarrow{\text{light}} 2COCl_2 + 2HCl", size=46, color=th.CORAL).move_to(UP * 1.2)
        ph = T("COCl₂ = phosgene: a deadly war gas, used in 1915", size=28, color=th.CORAL, weight="BOLD").next_to(eq, DOWN, buff=0.3)
        with self.say("Now the cold open's answer. Chloroform is a heavy, sweet smelling, non flammable liquid. But in air and sunlight it is slowly oxidised to phosgene, carbonyl chloride, an extremely poisonous gas used as a weapon in nineteen fifteen."):
            self.play(FadeIn(props))
            self.play(Write(eq))
            self.play(FadeIn(ph))
        sol = VGroup(T("dark brown bottle: keeps out light", size=26, color=th.AMBER), T("filled to the brim: keeps out air", size=26, color=th.AMBER),
                     T("1 % ethanol: destroys any phosgene", size=26, color=th.AMBER), chem(r"COCl_2 + 2C_2H_5OH \rightarrow (C_2H_5O)_2CO + 2HCl", size=32, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ph, DOWN, buff=0.45)
        nb = C.show_neby(self, "success", height=1.3)
        with self.say("So the three precautions: a dark brown bottle keeps out the light, filling it to the brim keeps out the air, and one percent ethanol destroys any phosgene that does form, turning it into harmless diethyl carbonate. Mystery solved."):
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in sol], lag_ratio=0.4), run_time=2.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(props, eq, ph, sol)))
        rows = [["Reagent", "Product", "Name"], ["Zn / HCl", "CH₂Cl₂ (excess: CH₄)", "dichloromethane"], ["Ag powder, heat", "2CHCl₃ + 6Ag → C₂H₂ + 6AgCl", "ethyne"],
                ["conc. HNO₃", "CHCl₃ + HNO₃ → CCl₃NO₂ + H₂O", "chloropicrin (tear gas)"], ["propanone + dil. KOH", "(CH₃)₂C(OH)CCl₃", "chloretone (hypnotic)"],
                ["NaOH(aq), boil", "CHCl₃ + 4NaOH → HCOONa + 3NaCl + 2H₂O", "sodium methanoate"], ["RNH₂ + alc. KOH", "RNC, foul smell", "carbylamine test (1° amines)"]]
        tb = C.table(rows, [3.4, 6.0, 3.6], row_h=0.62, size=22, colors=[th.AMBER, th.INK, th.MINT]).move_to(UP * 0.3)
        with self.say("Its other reactions, one line each. Reduction gives dichloromethane. Heating with silver powder strips all the chlorine and joins two carbons: ethyne. Nitric acid gives chloropicrin, a tear gas and soil fumigant. Propanone with dilute alkali gives chloretone, a sedative. Boiling alkali gives sodium methanoate. And with a primary amine and alcoholic potash, it gives an isocyanide with an appalling smell: the carbylamine test for primary amines.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))
        carb = VGroup(chem(r"C_6H_5NH_2 + CHCl_3 + 3KOH \rightarrow C_6H_5NC + 3KCl + 3H_2O", size=36, color=th.AMBER),
                      para("Uses: solvent for fats, oils, rubber and iodine; making Freon-22, chloretone and chloropicrin; preserving specimens. No longer an anaesthetic: it damages the liver.", width=11.5, size=24, color=th.BODY)).arrange(DOWN, buff=0.5)
        with self.say("Chloroform is still used as a solvent, and to make the refrigerant Freon twenty two. It is no longer used as an anaesthetic, because it damages the liver."):
            self.play(FadeIn(carb))
        self.play(FadeOut(carb))
        self.tip("KCN → nitrile, AgCN → isocyanide; KNO₂ → alkyl nitrite, AgNO₂ → nitroalkane. KOH(aq) → alcohol, KOH(alc) → alkene.",
                 "Two pairs win marks every year. Potassium salts attack through carbon or oxygen, silver salts through nitrogen. And aqueous potash gives the alcohol, alcoholic potash gives the alkene.", state="wink")
        self.quiz("Bromoethane reacts with AgNO₂ to give mainly",
                  ["ethyl nitrite", "nitroethane", "ethanol", "ethene"], 1,
                  "Last one. Bromoethane with silver nitrite. What is the main product? Pause and think.",
                  "B, nitroethane. Silver nitrite is covalent, so the attack comes through nitrogen, giving the nitro compound. Potassium nitrite, being ionic, attacks through oxygen and gives ethyl nitrite, the trap in option A.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "R–X: 1°, 2°, 3° by the carbon holding X; C₄H₉Br has 4 isomers.",
            "Make from alcohols: SOCl₂ best; HX to alkenes follows Markovnikov.",
            "b.p.: RI > RBr > RCl > RF; branching lowers b.p.",
            "SN2: one step, rate k[RX][Nu], inversion; CH₃X > 1° > 2° > 3°.",
            "SN1: carbocation, rate k[RX], racemisation; 3° > 2° > 1°.",
            "K salts attack via C or O; Ag salts via N.",
            "KOH(aq) → alcohol; KOH(alc) → alkene (Saytzeff); Wurtz doubles the chain.",
            "CHCl₃ from propanone + bleaching powder; light + air → phosgene.",
        ], "Let us recap. Haloalkanes are primary, secondary or tertiary by the carbon holding the halogen. They are best made from alcohols, with thionyl chloride. Boiling points rise from fluoride to iodide and fall with branching. S N two is one step, second order, with inversion, favoured by methyl and primary halides. S N one goes through a carbocation, is first order, gives racemisation, and is favoured by tertiary halides. Potassium salts attack through carbon or oxygen, silver salts through nitrogen. Aqueous potash substitutes, alcoholic potash eliminates. And chloroform, made from propanone and bleaching powder, must be protected from light and air.")
        self.outro("That is haloalkanes. Next, we attach a halogen to a benzene ring instead, and find out why it suddenly refuses to be substituted, in haloarenes. See you in the next lesson on NEBians.")
