import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem, push  # noqa: E402

ORANGE = "#F08A24"
GREEN_CR = "#3FAE6A"
OC = "#FF6B6B"

MAP = [("hx", r"C_2H_5Cl", "PCl₅ or SOCl₂", th.SKY),
       ("na", r"C_2H_5ONa + H_2", "Na", th.MINT),
       ("ene", r"CH_2{=}CH_2", "conc. H₂SO₄, 170 °C", th.CORAL),
       ("ether", r"C_2H_5OC_2H_5", "conc. H₂SO₄, 140 °C", th.PINK),
       ("ox", r"CH_3CHO \rightarrow CH_3COOH", "K₂Cr₂O₇ / H⁺", th.AMBER),
       ("cu", r"CH_3CHO + H_2", "Cu, 300 °C", th.LIME),
       ("ester", r"CH_3COOC_2H_5", "CH₃COOH, conc. H₂SO₄", th.TEAL),
       ("iodo", r"CHI_3\downarrow", "I₂ + NaOH", "#F2D43C")]


def node(txt, pos, color=th.INK, size=34):
    return T(txt, size=size, color=color, weight="BOLD").move_to(pos)


def bond(a, b, color=th.MUTED, w=5, shrink=0.28):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    u = (b - a) / np.linalg.norm(b - a)
    return Line(a + u * shrink, b - u * shrink, color=color, stroke_width=w)


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 10
    TITLE = "Alcohols"
    SUBTITLE = "The –OH group, from raksi to the breathalyser"
    SECTIONS = ["Naming, isomers and classes", "Victor Meyer and Lucas tests", "Preparation", "Industrial preparation",
                "Common terms", "Physical properties", "Chemical properties"]
    NEXT = "Unit 11 · Phenols"

    def lesson(self):
        self.rmap = C.ReactionMap(r"C_2H_5OH", MAP)
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        tube = RoundedRectangle(corner_radius=0.25, width=1.0, height=3.6, stroke_color=th.INK, stroke_width=3).move_to([-2.8, -0.3, 0])
        fill = Rectangle(width=0.86, height=3.3, fill_color=ORANGE, fill_opacity=0.85, stroke_width=0).move_to(tube)
        lab = T("acidified K₂Cr₂O₇", size=24, color=ORANGE).next_to(tube, DOWN, buff=0.25)
        mouth = Polygon([-6.0, 0.6, 0], [-4.6, 0.3, 0], [-4.6, -0.3, 0], [-6.0, -0.6, 0], fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0)
        ml = T("breath", size=22, color=th.MUTED).next_to(mouth, DOWN, buff=0.15)
        with self.say("A traffic police checkpoint on the Ring Road, late on a Saturday night. The officer hands the driver a small tube to breathe into. Inside the old style tube are orange crystals of acidified potassium dichromate."):
            self.play(FadeIn(tube), FadeIn(fill), FadeIn(lab), FadeIn(mouth), FadeIn(ml))
        rng = np.random.default_rng(3)
        puffs = VGroup(*[Dot([-4.5, rng.uniform(-0.25, 0.25), 0], radius=0.07, color=WHITE, fill_opacity=0.6) for _ in range(14)])
        lvl = ValueTracker(0)
        green = always_redraw(lambda: Rectangle(width=0.86, height=max(0.01, 3.3 * lvl.get_value()), fill_color=GREEN_CR, fill_opacity=0.9, stroke_width=0).align_to(fill, DOWN).set_x(fill.get_x()))
        with self.say("The driver breathes out. Watch the crystals. The orange turns green, and the green creeps up the tube. The further it goes, the more alcohol was in the breath."):
            self.play(LaggedStart(*[p.animate.move_to([-2.8 + rng.uniform(-0.3, 0.3), -1.8 + rng.uniform(0, 1), 0]).set_opacity(0) for p in puffs], lag_ratio=0.08), run_time=2)
            self.add(green)
            self.play(lvl.animate.set_value(0.55), run_time=3)
        nb = C.show_neby(self, "surprised", height=1.5, at=[2.4, -0.6, 0])
        q = para("What is the alcohol doing to the dichromate, and why does the colour change?", width=6.2, size=28, color=th.INK).move_to([3.0, 1.8, 0])
        with self.say("What is the alcohol doing to the dichromate? Why orange to green? By the end of this lesson, you will be able to write the equation the police are relying on."):
            self.play(FadeIn(q))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(tube, fill, lab, mouth, ml, q)), FadeOut(green))
        self.remove(green)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 10: Alcohols. Compounds with an hydroxyl group on a saturated carbon. From the raksi distilled in the hills, to power alcohol in petrol, to the breathalyser."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. Naming, isomers and classes of alcohols. Telling primary, secondary and tertiary apart, with the Victor Meyer and Lucas tests. Laboratory preparation, and industrial preparation. Common terms like absolute and power alcohol. Physical properties. And finally the chemical reactions, which we will gather into one reaction map.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        gen = VGroup(chem(r"C_nH_{2n+1}OH", size=60, color=th.AMBER), T("monohydric: one –OH · dihydric: glycol · trihydric: glycerol", size=24, color=th.BODY)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.9)
        with self.say("An alcohol with one hydroxyl group is monohydric, general formula C n H two n plus one O H. Two hydroxyl groups make a dihydric alcohol like glycol, three a trihydric one like glycerol. The carbon carrying the O H is called the carbinol carbon."):
            self.play(Write(gen[0]))
            self.play(FadeIn(gen[1]))
        cls = []
        xs = [-4.4, 0.0, 4.4]
        names = [("primary 1°", "1 carbon attached", th.SKY), ("secondary 2°", "2 carbons", th.AMBER), ("tertiary 3°", "3 carbons", th.CORAL)]
        groups = VGroup()
        for k, x in enumerate(xs):
            c = np.array([x, -0.6, 0])
            carb = Circle(radius=0.36, fill_color=names[k][2], fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to(c)
            ct = T("C", size=26, color=th.BG, weight="BOLD").move_to(c)
            oh = node("OH", c + UP * 1.2, color=OC, size=28)
            g = VGroup(bond(c, c + UP * 1.2), carb, ct, oh)
            dirs = [LEFT, RIGHT, DOWN][: k + 1]
            others = [LEFT, RIGHT, DOWN]
            for j, d in enumerate(others):
                p = c + d * 1.2
                if j <= k:
                    g.add(bond(c, p), Circle(radius=0.26, fill_color=C.EL["C"], fill_opacity=1, stroke_width=0).move_to(p), T("C", size=18, color=WHITE, weight="BOLD").move_to(p))
                else:
                    g.add(bond(c, p, shrink=0.25), node("H", p, color=C.EL["H"], size=24))
            g.add(VGroup(T(names[k][0], size=26, color=names[k][2], weight="BOLD"), T(names[k][1], size=20, color=th.BODY)).arrange(DOWN, buff=0.06).move_to(c + DOWN * 2.0))
            groups.add(g.scale(1.25, about_point=c))
        self.play(FadeOut(gen[1]), gen[0].animate.scale(0.6).to_edge(UP, buff=0.75))
        with self.say("Classify by counting the carbons joined to the carbinol carbon. One carbon: primary. Two: secondary. Three: tertiary. Methanol has none, and is counted as primary."):
            for g in groups:
                self.play(FadeIn(g, shift=UP * 0.2), run_time=0.8)
        self.play(FadeOut(VGroup(gen[0], groups)))
        rows = [["Structure", "IUPAC name", "Common name", "Class"], ["CH₃OH", "methanol", "methyl alcohol", "1°"], ["CH₃CH₂OH", "ethanol", "ethyl alcohol", "1°"],
                ["(CH₃)₂CHOH", "propan-2-ol", "isopropyl alcohol", "2°"], ["CH₃CH₂CH(OH)CH₃", "butan-2-ol", "sec-butyl alcohol", "2°"],
                ["(CH₃)₃COH", "2-methylpropan-2-ol", "tert-butyl alcohol", "3°"], ["C₆H₅CH₂OH", "phenylmethanol", "benzyl alcohol", "1°"]]
        tb = C.table(rows, [3.6, 3.8, 3.6, 1.4], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.BODY, th.MINT]).move_to(UP * 0.4)
        with self.say("In I U P A C names, the ending o l replaces the final e of the alkane, and the O H gets the lowest possible locant. Ethanol, propan two ol, butan two ol, two methyl propan two ol, which is tertiary butyl alcohol.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))
        title = T("C₄H₁₀O: four alcohols and three ethers", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        al = VGroup(*[chem(t, size=42, color=th.AMBER) for t in [r"CH_3CH_2CH_2CH_2OH", r"CH_3CH_2CH(OH)CH_3", r"(CH_3)_2CHCH_2OH", r"(CH_3)_3COH"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.0, -0.2, 0])
        et = VGroup(*[chem(t, size=42, color=th.SKY) for t in [r"CH_3OCH_2CH_2CH_3", r"CH_3OCH(CH_3)_2", r"C_2H_5OC_2H_5"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.2, 0])
        kinds = VGroup(T("chain: butan-1-ol vs 2-methylpropan-1-ol", size=24, color=th.BODY), T("position: butan-1-ol vs butan-2-ol", size=24, color=th.BODY),
                       T("functional: alcohol vs ether", size=24, color=th.BODY), T("optical: butan-2-ol is chiral", size=24, color=th.PINK)).arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.15), col_alignments="ll").to_edge(DOWN, buff=0.4)
        with self.say("Alcohols show four kinds of isomerism: chain, position, functional, with ethers of the same formula, and optical. C four H ten O has four alcohols: butan one ol, butan two ol, two methyl propan one ol, and two methyl propan two ol. And three ethers. Butan two ol has a carbon with four different groups, so it is chiral."):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in al], lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(e, shift=LEFT * 0.2) for e in et], lag_ratio=0.3))
            self.play(FadeIn(kinds))
        self.play(FadeOut(VGroup(title, al, et, kinds)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Victor Meyer's method", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        steps_ = VGroup(chem(r"R{-}OH \xrightarrow{HI,\ red\ P} R{-}I \xrightarrow{AgNO_2} R{-}NO_2", size=42), chem(r"R{-}NO_2 \xrightarrow{HNO_2} \ ? \xrightarrow{NaOH} \text{colour}", size=42)).arrange(RIGHT, buff=0.7).next_to(title, DOWN, buff=0.4)
        steps_.scale_to_fit_width(min(steps_.width, 12.8))
        with self.say("Victor Meyer's method tells primary, secondary and tertiary alcohols apart. Convert the alcohol to an iodide with hydrogen iodide and red phosphorus, then to a nitroalkane with silver nitrite. Then add nitrous acid, and finally alkali."):
            self.play(FadeIn(title))
            for s_ in steps_:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.7)
        cards = VGroup()
        info = [("1°", "R–CH₂–NO₂", "2 α-H", "nitrolic acid", "#D8252A", "blood red"), ("2°", "R₂CH–NO₂", "1 α-H", "pseudonitrole", "#2F5FE0", "blue"), ("3°", "R₃C–NO₂", "no α-H", "no reaction", "#E6E9F2", "colourless")]
        for cl, f, ah, prod, col, cname in info:
            sw = RoundedRectangle(corner_radius=0.15, width=1.6, height=1.0, fill_color=col, fill_opacity=0.85 if cname != "colourless" else 0.08, stroke_color=th.INK, stroke_width=2)
            g = VGroup(T(cl, size=40, color=th.AMBER, weight="BOLD"), T(f, size=24, color=th.INK), T(ah, size=24, color=th.SKY, weight="BOLD"), T(prod, size=20, color=th.BODY), sw, T(cname, size=22, color=th.INK)).arrange(DOWN, buff=0.15)
            cards.add(g)
        cards.arrange(RIGHT, buff=1.4).next_to(steps_, DOWN, buff=0.5)
        with self.say("The key is the number of alpha hydrogens, hydrogens on the carbon carrying the nitro group, because nitrous acid attacks there. A primary nitroalkane has two: it forms a nitrolic acid, which gives a blood red colour with alkali. A secondary has one: it forms a pseudonitrole, blue. A tertiary has none: no reaction, colourless.") as v:
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)
                self.hold(v.dur / 3 - 0.65)
        care = T("red = 1°, blue = 2°, colourless = 3°: the absence of colour IS the test for 3°", size=24, color=th.CORAL).to_edge(DOWN, buff=0.4)
        with self.say("Students swap these colours every year. Red for primary, blue for secondary, and for tertiary, no colour at all."):
            self.play(FadeIn(care))
        self.play(FadeOut(VGroup(title, steps_, cards, care)))
        title = T("The Lucas test: a race to turbidity", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        sub = T("conc. HCl + anhydrous ZnCl₂ at 25 °C; an SN1 reaction", size=24, color=th.MUTED).next_to(title, DOWN, buff=0.2)
        tt = ValueTracker(0)
        tubes = VGroup()
        clouds = []
        onset = [7.0, 5.0, 0.15]
        labels = ["1° (ethanol)", "2° (propan-2-ol)", "3° (2-methylpropan-2-ol)"]
        for k, x in enumerate([-4.0, 0.0, 4.0]):
            tb = RoundedRectangle(corner_radius=0.25, width=0.9, height=2.8, stroke_color=th.INK, stroke_width=3).move_to([x, -0.4, 0])
            liq = Rectangle(width=0.78, height=2.0, fill_color=th.SKY, fill_opacity=0.15, stroke_width=0).align_to(tb, DOWN).shift(UP * 0.12).set_x(x)
            cl = Rectangle(width=0.78, height=2.0, fill_color=WHITE, fill_opacity=0.0, stroke_width=0).move_to(liq)
            clouds.append((cl, onset[k]))
            tubes.add(VGroup(tb, liq, cl, T(labels[k], size=22, color=th.INK).next_to(tb, DOWN, buff=0.2)))
        for cl, on in clouds:
            cl.add_updater(lambda m, on=on: m.set_fill(opacity=0.75 * np.clip((tt.get_value() - on) / 0.6, 0, 1)))
        clock = DecimalNumber(0, num_decimal_places=1, font_size=44, color=th.AMBER, unit=r"\,\text{min}")
        clock.add_updater(lambda m: m.set_value(min(tt.get_value(), 6)).to_corner(UR, buff=0.8).shift(DOWN * 0.8))
        with self.say("The quicker bench test is the Lucas test. Add Lucas reagent, concentrated hydrochloric acid with anhydrous zinc chloride, and start a clock. The tertiary alcohol turns cloudy at once, as the insoluble chloride separates. The secondary takes about five minutes. The primary stays clear at room temperature and only reacts on heating."):
            self.play(FadeIn(title), FadeIn(sub), FadeIn(tubes))
            self.add(clock)
            self.play(tt.animate.set_value(6), run_time=5, rate_func=linear)
        why = T("SN1: the more stable the carbocation (3° > 2° > 1°), the faster the chloride forms", size=24, color=th.AMBER).to_edge(DOWN, buff=0.4)
        with self.say("Why this order? The reaction goes through a carbocation, S N one, and a tertiary carbocation forms fastest."):
            self.play(FadeIn(why))
        for cl, _ in clouds:
            cl.clear_updaters()
        clock.clear_updaters()
        self.play(FadeOut(VGroup(title, sub, tubes, why, clock)))
        rows = [["Test", "1°", "2°", "3°"], ["Victor Meyer", "blood red", "blue", "colourless"], ["Lucas", "clear (heat)", "~5 min", "at once"],
                ["K₂Cr₂O₇ / H⁺", "aldehyde → acid", "ketone", "no reaction"], ["Cu, 300 °C", "aldehyde + H₂", "ketone + H₂", "alkene + H₂O"]]
        tb = C.table(rows, [3.2, 3.0, 3.0, 3.0], row_h=0.68, size=25, colors=[th.AMBER, th.SKY, th.MINT, th.CORAL]).move_to(UP * 0.3)
        with self.say("Four ways to tell the classes apart, side by side. Victor Meyer colours, Lucas timing, and two more we will meet soon: oxidation with dichromate, and dehydrogenation over hot copper.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(tb))
        self.quiz("Which alcohol gives a BLUE colour in Victor Meyer's test?",
                  ["ethanol", "propan-2-ol", "2-methylpropan-2-ol", "methanol"], 1,
                  "Pause and think. Which of these gives a blue colour in Victor Meyer's test?",
                  "B, propan two ol. It is secondary, so its nitroalkane has one alpha hydrogen and gives the blue pseudonitrole. Ethanol and methanol are primary, red. Two methyl propan two ol is tertiary, colourless.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        title = T("Three laboratory routes", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        hub = VGroup(RoundedRectangle(corner_radius=0.2, width=2.8, height=1.1, fill_color=th.AMBER, fill_opacity=1, stroke_width=0), chem(r"C_2H_5OH", size=48, color=th.BG)).move_to([0, -0.5, 0])
        srcs = [(r"C_2H_5Br", "KOH(aq), boil", [-4.4, 1.3, 0], th.SKY), (r"C_2H_5NH_2", "HNO₂ (NaNO₂ + HCl, 0–5 °C)", [4.4, 1.3, 0], th.MINT), (r"CH_3COOC_2H_5", "hydrolysis, or LiAlH₄", [0, 1.9, 0], th.PINK)]
        nodes = []
        for p_, lab, pos, col in srcs:
            n = VGroup(chem(p_, size=44, color=col), T(lab, size=24, color=col)).arrange(DOWN, buff=0.12).move_to(pos)
            tgt = hub.get_top() if pos[0] == 0 else (hub.get_left() + UP * 0.2 if pos[0] < 0 else hub.get_right() + UP * 0.2)
            a = Arrow(n.get_bottom(), tgt, buff=0.1, color=col, stroke_width=5)
            nodes.append((n, a))
        e1 = chem(r"C_2H_5Br + KOH(aq) \rightarrow C_2H_5OH + KBr", size=36).to_edge(DOWN, buff=0.6)
        with self.say("Alcohols can be made in the laboratory from three kinds of compound. From a haloalkane, by boiling with aqueous potassium hydroxide. Remember, aqueous: alcoholic potash would give an alkene."):
            self.play(FadeIn(title), FadeIn(hub))
            self.play(FadeIn(nodes[0][0]), GrowArrow(nodes[0][1]))
            self.play(Write(e1))
        e2 = chem(r"C_2H_5NH_2 + HNO_2 \rightarrow C_2H_5OH + N_2\uparrow + H_2O", size=36).to_edge(DOWN, buff=0.6)
        with self.say("From a primary amine, with nitrous acid made from sodium nitrite and hydrochloric acid in ice. The unstable diazonium salt loses nitrogen at once, and the brisk fizz of nitrogen is also the test for a primary amine."):
            self.play(FadeIn(nodes[1][0]), GrowArrow(nodes[1][1]), FadeTransform(e1, e2))
            bub = VGroup(*[Circle(radius=0.09, stroke_color=WHITE, stroke_width=2).move_to(nodes[1][1].get_center() + RIGHT * 0.25 * k) for k in range(3)])
            self.play(bub.animate.shift(UP * 1.0).set_opacity(0), run_time=0.8)
        e3 = VGroup(chem(r"CH_3COOC_2H_5 + NaOH \rightarrow CH_3COONa + C_2H_5OH", size=34), chem(r"CH_3COOC_2H_5 + 4[H] \xrightarrow{LiAlH_4} CH_3CH_2OH + C_2H_5OH", size=34)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.say("And from esters. Acid hydrolysis is reversible. Alkaline hydrolysis, saponification, goes to completion because the acid is removed as its salt. Reducing an ester with lithium aluminium hydride gives two alcohols, one from each half of the ester."):
            self.play(FadeIn(nodes[2][0]), GrowArrow(nodes[2][1]), FadeOut(e2), Write(e3))
        self.play(FadeOut(VGroup(title, hub, e3, bub, *[VGroup(n, a) for n, a in nodes])))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        title = T("Oxo process: the chain grows by one", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e = VGroup(chem(r"CH_2{=}CH_2 + CO + H_2 \xrightarrow{Co_2(CO)_8,\ 150^{\circ}C,\ 100\ atm} CH_3CH_2CHO", size=42),
                   chem(r"CH_3CH_2CHO + H_2 \xrightarrow{Ni} CH_3CH_2CH_2OH", size=42)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.5)
        n_ = T("ethene (2 C) → propan-1-ol (3 C): a primary alcohol", size=26, color=th.AMBER).next_to(e, DOWN, buff=0.4)
        with self.say("Industry makes alcohols on a huge scale. In the oxo process, an alkene, carbon monoxide and hydrogen pass over a cobalt carbonyl catalyst at about a hundred and fifty degrees and a hundred atmospheres, giving an aldehyde, which is then hydrogenated. The chain grows by one carbon: ethene gives propan one ol."):
            self.play(FadeIn(title), Write(e[0]))
            self.play(Write(e[1]))
            self.play(FadeIn(n_))
        self.play(FadeOut(VGroup(title, e, n_)))
        title = T("Hydroboration–oxidation: anti-Markovnikov", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e = VGroup(chem(r"3CH_2{=}CH_2 + BH_3 \xrightarrow{\text{dry ether}} (CH_3CH_2)_3B", size=40),
                   chem(r"(CH_3CH_2)_3B + 3H_2O_2 \xrightarrow{NaOH} 3CH_3CH_2OH + H_3BO_3", size=40)).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.4)
        prop = chem(r"CH_3CH{=}CH_2", size=48).move_to([0, -0.7, 0])
        l = VGroup(chem(r"CH_3CH(OH)CH_3", size=42, color=th.CORAL), T("H₂O / H⁺: propan-2-ol (Markovnikov)", size=24, color=th.CORAL)).arrange(DOWN, buff=0.08).move_to([-3.8, -2.4, 0])
        r = VGroup(chem(r"CH_3CH_2CH_2OH", size=42, color=th.MINT), T("B₂H₆, then H₂O₂/OH⁻: propan-1-ol", size=24, color=th.MINT)).arrange(DOWN, buff=0.08).move_to([3.8, -2.4, 0])
        a1 = Arrow(prop.get_left(), l.get_top(), buff=0.15, color=th.CORAL, stroke_width=4)
        a2 = Arrow(prop.get_right(), r.get_top(), buff=0.15, color=th.MINT, stroke_width=4)
        with self.say("In hydroboration oxidation, diborane adds across the double bond, and alkaline hydrogen peroxide then swaps boron for O H. Boron goes to the carbon with more hydrogens, so the result is anti Markovnikov. Propene gives propan one ol this way, but propan two ol by ordinary acid catalysed hydration. With ethene both give ethanol."):
            self.play(FadeIn(title), Write(e))
            self.play(FadeIn(prop))
            self.play(GrowArrow(a1), FadeIn(l))
            self.play(GrowArrow(a2), FadeIn(r))
        self.play(FadeOut(VGroup(title, e, prop, l, r, a1, a2)))
        self.fermentation()

    def fermentation(self):
        title = T("Fermentation: jaand, chhyang and raksi", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        chain = [("starch", th.BODY), ("maltose", th.SKY), ("glucose", th.AMBER), ("ethanol + CO₂", th.MINT)]
        enz = ["diastase", "maltase", "zymase"]
        boxes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.15, width=2.5, height=0.95, fill_color=th.PANEL, fill_opacity=1, stroke_color=c, stroke_width=3), T(n, size=26, color=c, weight="BOLD")) for n, c in chain]).arrange(RIGHT, buff=0.95).next_to(title, DOWN, buff=0.5)
        for b in boxes:
            b[1].move_to(b[0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=th.MUTED, stroke_width=4) for a, b in zip(boxes, boxes[1:])])
        el = VGroup(*[T(e_, size=22, color=th.PINK).next_to(a, DOWN, buff=0.35) for e_, a in zip(enz, arrows)])
        eq = chem(r"C_6H_{12}O_6 \xrightarrow{zymase} 2C_2H_5OH + 2CO_2\uparrow", size=48, color=th.MINT).move_to([0, 0.3, 0])
        with self.say("The oldest route of all is fermentation. Starch from rice, millet or maize is broken down by the enzyme diastase to maltose, maltase splits maltose into glucose, and zymase in yeast turns glucose into ethanol and carbon dioxide, at twenty five to thirty degrees, without air. For cane sugar the first enzyme is invertase."):
            self.play(FadeIn(title))
            for k, b in enumerate(boxes):
                self.play(FadeIn(b, shift=RIGHT * 0.2), *([GrowArrow(arrows[k - 1]), FadeIn(el[k - 1])] if k else []), run_time=0.7)
            self.play(Write(eq))
        bk = C.Beaker(center=[-3.2, -2.0, 0], w=2.2, h=1.8, level=0.7, color="#D9C38A", opacity=0.45)
        tt = ValueTracker(0)
        bub = always_redraw(lambda: VGroup(*[Circle(radius=0.05, stroke_color=WHITE, stroke_width=2).move_to([-3.2 + 0.7 * np.sin(2.3 * k), -2.6 + ((tt.get_value() + k / 8) % 1) * 1.1, 0]) for k in range(8)]))
        stop = VGroup(T("stops near 14 %:", size=24, color=th.CORAL, weight="BOLD"), T("zymase is killed by its own product", size=22, color=th.BODY), T("→ concentrate the wash by distillation (raksi)", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, -2.0, 0])
        with self.say("Fermentation stops near fourteen percent alcohol, because zymase is destroyed by the ethanol it makes. That is how jaand and chhyang are made from millet and rice in the hills. Distil the wash, and you get raksi."):
            self.play(FadeIn(bk.g))
            self.add(bub)
            self.play(tt.animate.set_value(3), FadeIn(stop), run_time=4, rate_func=linear)
        self.play(FadeOut(VGroup(title, boxes, arrows, el, eq, bk.g, stop)), FadeOut(bub))
        self.remove(bub)
        head, prob = C.example_head(self, "90 g of glucose is fermented completely. Find (a) the mass of ethanol, (b) its volume (density 0.789 g cm⁻³), (c) the volume of CO₂ at STP. If only 38.0 g of ethanol is recovered, what is the percentage yield?")
        st = C.steps(r"n(\text{glucose}) = \tfrac{90}{180} = 0.50\ \mathrm{mol} \Rightarrow 1.00\ \mathrm{mol\ C_2H_5OH}",
                     r"(a)\ 1.00 \times 46 = 46\ \mathrm{g};\quad (b)\ V = \tfrac{46}{0.789} = 58.3\ \mathrm{cm^3}",
                     r"(c)\ 1.00\ \mathrm{mol\ CO_2} = 22.4\ \mathrm{dm^3}",
                     r"\text{yield} = \tfrac{38.0}{46.0}\times100 = 82.6\,\%", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example ten point one. Ninety grams of glucose is half a mole, which gives one mole of ethanol: forty six grams, or fifty eight point three cubic centimetres. And one mole of carbon dioxide, twenty two point four litres at S T P. Recovering only thirty eight grams means a yield of eighty two point six percent."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("Why 95.6 % is a wall", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = NumberLine(x_range=[0, 100, 10], length=10, include_numbers=True, font_size=24, color=th.MUTED).move_to([0, -1.6, 0])
        axl = T("% ethanol", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.4)
        pct = ValueTracker(14)
        bar = always_redraw(lambda: Rectangle(width=max(0.02, ax.n2p(pct.get_value())[0] - ax.n2p(0)[0]), height=0.6, fill_color=th.SKY, fill_opacity=0.85, stroke_width=0).move_to(ax.n2p(0) + UP * 0.6, aligned_edge=LEFT))
        rd = DecimalNumber(14, num_decimal_places=1, font_size=48, color=th.SKY, unit=r"\,\%")
        rd.add_updater(lambda m: m.set_value(pct.get_value()).move_to([0, 1.2, 0]))
        wall = Line(ax.n2p(95.6) + UP * 0.1, ax.n2p(95.6) + UP * 1.4, color=th.CORAL, stroke_width=6)
        wl = T("azeotrope: 95.6 %, b.p. 78.15 °C", size=22, color=th.CORAL).next_to(wall, UP, buff=0.1)
        with self.say("Distil a fermented wash, and the alcohol concentration climbs. But it stops dead at ninety five point six percent. At that point ethanol and water form an azeotrope, a constant boiling mixture whose vapour has exactly the same composition as the liquid. No amount of extra distillation gets past it. This is rectified spirit."):
            self.play(FadeIn(title), Create(ax), FadeIn(axl))
            self.add(bar, rd)
            self.play(FadeIn(bar), FadeIn(rd))
            self.play(pct.animate.set_value(95.6), run_time=3, rate_func=rate_functions.ease_out_cubic)
            self.play(Create(wall), FadeIn(wl))
            self.play(pct.animate.set_value(96.5), run_time=0.4)
            self.play(pct.animate.set_value(95.6), run_time=0.4)
        cao = T("reflux with quicklime, CaO, then distil → 100 %: absolute alcohol", size=24, color=th.MINT).to_edge(DOWN, buff=0.4)
        with self.say("To get past the wall you need chemistry: reflux rectified spirit with quicklime, which takes up the water as calcium hydroxide, and distil. That gives absolute alcohol, one hundred percent. Industry uses azeotropic distillation with benzene. And never calcium chloride, which forms a compound with ethanol."):
            self.play(FadeIn(cao))
            self.play(pct.animate.set_value(100), run_time=1.5)
        rd.clear_updaters()
        self.play(FadeOut(VGroup(title, ax, axl, wall, wl, cao, rd)), FadeOut(bar))
        self.remove(bar)
        cards = VGroup(*[C.card(self, a, b, w=4.0, h=2.6, color=c, tsize=28, bsize=23) for a, b, c in [
            ("Rectified spirit", "95.6 % ethanol: the azeotrope", th.SKY), ("Absolute alcohol", "100 %: rectified spirit + CaO, distilled", th.MINT),
            ("Denatured alcohol", "made undrinkable: ~5 % methanol, pyridine, a trace of CuSO₄", th.CORAL), ("Power alcohol", "petrol with 20–25 % ethanol; benzene keeps it mixed", th.AMBER),
            ("Beverages", "fermented: beer 4–8 %, wine, chhyang; distilled: whisky, raksi 30–45 %", th.PINK)]]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(UP * 0.2)
        with self.say("Five terms you must define. Rectified spirit, ninety five point six percent. Absolute alcohol, a hundred percent. Denatured alcohol, made undrinkable with methanol, pyridine and a little copper sulphate, so industry can use it free of drinks tax. Power alcohol, petrol with twenty to twenty five percent ethanol, which saves imported fuel. And alcoholic beverages, fermented like beer and chhyang, or distilled like raksi.") as v:
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.45)
                self.hold(v.dur / 5 - 0.5)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Same mass, very different boiling points", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        data = [("propane", "44", -42, th.MUTED), ("methoxymethane", "46", -24, th.SKY), ("ethanol", "46", 78, th.AMBER)]
        base = -0.3
        bars = VGroup()
        for i, (n, mm, bp, col) in enumerate(data):
            x = -4.9 + i * 2.1
            h = abs(bp) * 0.03
            b = Rectangle(width=1.3, height=max(0.05, h), fill_color=col, fill_opacity=0.85, stroke_width=0)
            if bp >= 0:
                b.move_to([x, base, 0], aligned_edge=DOWN)
            else:
                b.move_to([x, base, 0], aligned_edge=UP)
            val = T(f"{bp} °C", size=26, color=th.INK, weight="BOLD").next_to(b, UP if bp >= 0 else DOWN, buff=0.1)
            nm = VGroup(T(n, size=22, color=col, weight="BOLD"), T(f"M = {mm}", size=20, color=th.MUTED)).arrange(DOWN, buff=0.04).move_to([x, -3.0, 0])
            bars.add(VGroup(b, val, nm))
        zero = Line([-6.0, base, 0], [-0.6, base, 0], color=th.FAINT, stroke_width=2)
        mols = VGroup()
        cs = [np.array([2.0, 1.0, 0]), np.array([4.4, 0.4, 0]), np.array([2.6, -1.4, 0]), np.array([5.0, -1.9, 0])]
        for c in cs:
            o = Circle(radius=0.3, fill_color=OC, fill_opacity=1, stroke_width=0).move_to(c)
            h = Circle(radius=0.17, fill_color=C.EL["H"], fill_opacity=1, stroke_width=0).move_to(c + np.array([0.45, -0.25, 0]))
            r = VGroup(Circle(radius=0.3, fill_color=C.EL["C"], fill_opacity=1, stroke_width=0), T("Et", size=16, color=WHITE, weight="BOLD")).move_to(c + np.array([-0.55, 0.2, 0]))
            mols.add(VGroup(Line(c, h.get_center(), color=th.MUTED, stroke_width=4), Line(c, r.get_center(), color=th.MUTED, stroke_width=4), r, o, h))
        hb = VGroup(*[DashedLine(mols[a][4].get_center(), mols[b][3].get_center(), color=th.SKY, stroke_width=3, dash_length=0.08) for a, b in [(0, 1), (2, 0), (3, 1), (2, 3)]])
        hl = T("hydrogen bonds, about 20 kJ mol⁻¹ each", size=22, color=th.SKY).move_to([3.4, 2.3, 0])
        with self.say("Propane, methoxymethane and ethanol have almost the same molar mass. Yet propane boils at minus forty two, the ether at minus twenty four, and ethanol at plus seventy eight degrees. The reason is hydrogen bonding. The O H hydrogen of one ethanol molecule is attracted to the oxygen of the next, and boiling means breaking that whole network."):
            self.play(FadeIn(title), Create(zero))
            for b in bars:
                self.play(GrowFromEdge(b[0], DOWN if b[0].get_y() > base else UP), FadeIn(b[1:]), run_time=0.6)
            self.play(FadeIn(mols))
            self.play(LaggedStart(*[Create(h) for h in hb], lag_ratio=0.3), FadeIn(hl))
        self.play(FadeOut(VGroup(title, bars, zero, mols, hb, hl)))
        rows = [["Property", "Trend and reason"], ["branching", "b.p. falls: butan-1-ol 117.7, butan-2-ol 99.5, tert-butanol 82.4 °C"],
                ["solubility", "C1–C3 mix with water fully; falls as the chain grows"],
                ["density", "less than water (ethanol 0.789 g cm⁻³)"], ["acidity", "very weak acids, pKa about 16–18: neutral to litmus"]]
        tb = C.table(rows, [2.6, 10.0], row_h=0.8, size=27, colors=[th.AMBER, th.BODY]).move_to(UP * 0.3)
        with self.say("Branching lowers the boiling point, since a compact molecule has less surface contact. The small alcohols mix with water in all proportions, because they hydrogen bond with it, but solubility falls as the oily carbon chain grows. Alcohols are less dense than water, and such weak acids that they do not affect litmus.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.45)
                self.hold(v.dur / 5 - 0.45)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        c = np.array([0, -0.2, 0])
        mol = VGroup(node("CH₃", c + LEFT * 2.6, size=40), node("C", c, size=40), node("O", c + RIGHT * 2.0, color=OC, size=40), node("H", c + RIGHT * 3.4, color=C.EL["H"], size=36),
                     node("H", c + UP * 1.2, color=C.EL["H"], size=32), node("H", c + DOWN * 1.2, color=C.EL["H"], size=32))
        bonds = VGroup(bond(mol[0].get_center(), mol[1].get_center(), shrink=0.5), bond(mol[1].get_center(), mol[2].get_center()), bond(mol[2].get_center(), mol[3].get_center()),
                       bond(mol[1].get_center(), mol[4].get_center()), bond(mol[1].get_center(), mol[5].get_center()))
        hl = [SurroundingRectangle(bonds[2], color=th.MINT, buff=0.18), SurroundingRectangle(bonds[1], color=th.SKY, buff=0.18), SurroundingRectangle(VGroup(bonds[3], mol[4]), color=th.AMBER, buff=0.1)]
        tags = [T("O–H: acidic H (Na)", size=24, color=th.MINT).next_to(hl[0], UP, buff=0.2), T("C–O: –OH replaced (HX, PCl₅) or lost (dehydration)", size=24, color=th.SKY).next_to(hl[1], DOWN, buff=1.4),
                T("α C–H: oxidation, dehydrogenation", size=24, color=th.AMBER).next_to(hl[2], UP, buff=0.2)]
        with self.say("Alcohols react at three places. The O H bond, where the hydrogen is weakly acidic. The carbon oxygen bond, where the O H is replaced or lost. And the alpha carbon hydrogen bonds, which are attacked in oxidation. Keep this picture in mind, and every reaction falls into place. We will collect them all into one map as we go."):
            self.play(FadeIn(mol), Create(bonds))
            for h, t_ in zip(hl, tags):
                self.play(Create(h), FadeIn(t_), run_time=0.7)
        self.play(FadeOut(VGroup(mol, bonds, *hl, *tags)))
        self.halides()
        self.sodium()
        self.dehydration()
        self.oxidation()
        self.esterification()
        self.tests()
        g = self.rmap
        with self.say("Here is the whole reaction map of ethanol, built up through this lesson. Every product comes from the same three places in the molecule. If you can redraw this map from memory, you can answer almost any question on alcohols."):
            grp = g.show(self, [e[0] for e in MAP], [])
            self.play(Indicate(grp[1], color=th.AMBER, scale_factor=1.1))
        self.play(FadeOut(grp))
        self.tip("Iodoform test (I₂ + NaOH → yellow CHI₃) is positive only for CH₃CH(OH)– alcohols and methyl ketones: ethanol, propan-2-ol, butan-2-ol. Methanol and propan-1-ol give NO iodoform.",
                 "A favourite trap. The iodoform test is not a test for alcohols in general. It works only for ethanol and alcohols with the C H three C H O H group, like propan two ol, and for methyl ketones. Methanol and propan one ol give no yellow precipitate.", state="wink")
        self.quiz("Ethanol heated with conc. H₂SO₄ at 140 °C gives mainly",
                  ["ethene", "ethoxyethane", "ethanal", "ethyl hydrogen sulphate only"], 1,
                  "Last one. Ethanol with concentrated sulphuric acid at one hundred and forty degrees. What forms? Pause and think.",
                  "B, ethoxyethane, diethyl ether. At one forty degrees two ethanol molecules lose one water between them. At one seventy degrees, each molecule loses its own water, giving ethene. Ethanal needs an oxidising agent.")

    def halides(self):
        title = T("Replacing –OH by halogen", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Reagent", "Equation", "Note"], ["HCl + anhyd. ZnCl₂", "C₂H₅OH + HCl → C₂H₅Cl + H₂O", "Groves; 3° > 2° > 1°"], ["PBr₃ (red P + Br₂)", "3C₂H₅OH + PBr₃ → 3C₂H₅Br + H₃PO₃", ""],
                ["PCl₅", "C₂H₅OH + PCl₅ → C₂H₅Cl + POCl₃ + HCl", "HCl fumes: a test for –OH"], ["SOCl₂ + pyridine", "C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑", "Darzen: the best"]]
        tb = C.table(rows, [3.4, 6.4, 3.2], row_h=0.66, size=22, colors=[th.AMBER, th.INK, th.MUTED]).next_to(title, DOWN, buff=0.4)
        with self.say("First, at the carbon oxygen bond: replacing O H by halogen, as we saw in haloalkanes. Hydrogen halides with zinc chloride, phosphorus halides, and best of all thionyl chloride, whose by products are both gases. Phosphorus pentachloride gives fumes of hydrogen chloride, which is also a test for an O H group.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(title, tb)))
        with self.say("Our first spoke on the reaction map: ethanol to chloroethane."):
            g = self.rmap.show(self, [], ["hx"])
        self.play(FadeOut(g))

    def sodium(self):
        title = T("Sodium: the O–H hydrogen is acidic", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e = VGroup(chem(r"2C_2H_5OH + 2Na \rightarrow 2C_2H_5ONa + H_2\uparrow", size=40), chem(r"6C_2H_5OH + 2Al \rightarrow 2(C_2H_5O)_3Al + 3H_2\uparrow", size=34)).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.4)
        bk1 = C.Beaker(center=[-3.2, -1.6, 0], w=2.4, h=1.8, level=0.7, color=C.WATER, opacity=0.3)
        bk2 = C.Beaker(center=[3.2, -1.6, 0], w=2.4, h=1.8, level=0.7, color="#E6E9F2", opacity=0.15)
        l1 = T("Na + water: violent", size=22, color=th.CORAL).next_to(bk1.g, DOWN, buff=0.15)
        l2 = T("Na + ethanol: steady fizz", size=22, color=th.MINT).next_to(bk2.g, DOWN, buff=0.15)
        tt = ValueTracker(0)
        bub = always_redraw(lambda: VGroup(*[Circle(radius=0.05 + 0.03 * (k % 2), stroke_color=WHITE, stroke_width=2).move_to([cx + 0.6 * np.sin(3.1 * k + cx), -2.2 + ((tt.get_value() * sp + k / n) % 1) * 1.4, 0])
                                              for cx, sp, n in ((-3.2, 2.5, 14), (3.2, 0.8, 6)) for k in range(n)]))
        order = T("water > 1° > 2° > 3° alcohol: alkyl groups push charge onto the alkoxide oxygen", size=22, color=th.AMBER).to_edge(DOWN, buff=0.3)
        with self.say("At the O H bond, reactive metals like sodium replace the hydrogen, giving sodium ethoxide and hydrogen gas. Aluminium does the same. But compare with water: sodium reacts violently with water and only steadily with ethanol. Alcohols are weaker acids than water. Primary alcohols react fastest and tertiary slowest, because extra alkyl groups push charge onto the oxygen of the alkoxide ion and destabilise it."):
            self.play(FadeIn(title), Write(e))
            self.play(FadeIn(bk1.g), FadeIn(bk2.g), FadeIn(l1), FadeIn(l2))
            self.add(bub)
            self.play(tt.animate.set_value(3), run_time=3, rate_func=linear)
            self.play(FadeIn(order))
        self.play(FadeOut(VGroup(title, e, bk1.g, bk2.g, l1, l2, order)), FadeOut(bub))
        self.remove(bub)
        head, prob = C.example_head(self, "9.2 g of absolute ethanol is treated with excess sodium. Find (a) the volume of H₂ at STP, (b) the mass of sodium ethoxide. (Na = 23)")
        st = C.steps(r"n(\mathrm{C_2H_5OH}) = \tfrac{9.2}{46} = 0.20\ \mathrm{mol}",
                     r"(a)\ 2\ \mathrm{mol\ ethanol} \rightarrow 1\ \mathrm{mol\ H_2}:\ 0.10 \times 22.4 = 2.24\ \mathrm{dm^3}",
                     r"(b)\ M(\mathrm{C_2H_5ONa}) = 68:\ 0.20 \times 68 = 13.6\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example ten point two. Nine point two grams of ethanol is zero point two moles. Two ethanols give one hydrogen molecule, so zero point one mole, two point two four litres at S T P. And zero point two moles of sodium ethoxide, molar mass sixty eight: thirteen point six grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        with self.say("A second spoke on the map: ethanol to sodium ethoxide."):
            g = self.rmap.show(self, ["hx"], ["na"])
        self.play(FadeOut(g))

    def dehydration(self):
        title = T("Dehydration at 170 °C: the E1 mechanism", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        y = -0.3
        c1, c2, o = np.array([-3.4, y, 0]), np.array([-1.6, y, 0]), np.array([0.2, y, 0])
        a_c1 = node("CH₂", c1, size=36)
        a_c2 = node("CH₂", c2, size=36)
        a_o = node("O", o, color=OC, size=40)
        h_o = node("H", o + np.array([1.0, 0.55, 0]), color=C.EL["H"], size=32)
        h_c1 = node("H", c1 + UP * 1.2, color=C.EL["H"], size=32)
        b12 = bond(c1, c2, shrink=0.45)
        b2o = bond(c2, o, shrink=0.42)
        boh = bond(o, h_o.get_center(), shrink=0.25)
        bch = bond(c1, h_c1.get_center(), shrink=0.3)
        lp = VGroup(Dot(o + np.array([-0.15, -0.42, 0]), radius=0.05, color=th.AMBER), Dot(o + np.array([0.15, -0.42, 0]), radius=0.05, color=th.AMBER))
        hplus = node("H⁺", o + np.array([1.6, -1.3, 0]), color=th.CORAL, size=34)
        s1 = T("1. protonation: the –OH becomes –OH₂⁺, a good leaving group", size=24, color=th.CORAL).to_edge(DOWN, buff=0.7)
        with self.say("Now the most important mechanism in this unit. Heat ethanol with concentrated sulphuric acid at one hundred and seventy degrees. Step one: a lone pair on the oxygen grabs a hydrogen ion from the acid. The curved arrow shows that pair of electrons moving. The O H becomes O H two plus, protonated."):
            self.play(FadeIn(title), FadeIn(VGroup(a_c1, a_c2, a_o, h_o, h_c1)), Create(VGroup(b12, b2o, boh, bch)), FadeIn(lp))
            self.play(FadeIn(hplus))
            ar1 = push(lp.get_center() + DOWN * 0.05, hplus.get_left() + LEFT * 0.05, angle=TAU / 5)
            self.play(Create(ar1), FadeIn(s1))
            h2 = node("H", o + np.array([1.0, -0.55, 0]), color=C.EL["H"], size=32)
            bh2 = bond(o, h2.get_center(), shrink=0.25)
            plus = T("+", size=34, color=th.CORAL, weight="BOLD").next_to(a_o, UP, buff=0.05).shift(LEFT * 0.15)
            self.play(Transform(hplus, h2), FadeOut(lp), FadeOut(ar1), Create(bh2), FadeIn(plus), run_time=1.2)
        water = VGroup(a_o, h_o, hplus, boh, bh2, plus)
        s2 = T("2. slow step: water leaves, leaving a carbocation", size=24, color=th.AMBER).to_edge(DOWN, buff=0.7)
        with self.say("Step two, the slow step. The carbon oxygen bond breaks, both electrons going to the oxygen, and a neutral water molecule leaves. That leaves a carbocation, carbon with only six electrons and a positive charge."):
            ar2 = push(b2o.get_center() + UP * 0.1, a_o.get_top() + UP * 0.05, angle=-TAU / 4)
            self.play(Create(ar2), FadeOut(s1), FadeIn(s2))
            cplus = T("+", size=40, color=th.AMBER, weight="BOLD").next_to(a_c2, UP, buff=0.05)
            self.play(FadeOut(ar2), FadeOut(b2o), water.animate.shift(RIGHT * 2.2 + DOWN * 0.4), FadeIn(cplus), run_time=1.4)
            wl = T("H₂O", size=26, color=C.WATER).next_to(water, DOWN, buff=0.2)
            self.play(FadeIn(wl))
        base = node("HSO₄⁻", c1 + np.array([-1.2, 2.2, 0]), color=th.SKY, size=30)
        s3 = T("3. a base removes a β-hydrogen; its electrons make the C=C", size=24, color=th.MINT).to_edge(DOWN, buff=0.7)
        with self.say("Step three. A base, hydrogen sulphate ion, pulls off a hydrogen from the neighbouring carbon. The electrons from that carbon hydrogen bond swing in to form the second bond between the two carbons. Ethene."):
            self.play(FadeIn(base), FadeOut(s2), FadeIn(s3))
            ar3 = push(base.get_bottom() + RIGHT * 0.3, h_c1.get_left(), angle=TAU / 6)
            ar4 = push(bch.get_center() + RIGHT * 0.1, b12.get_center() + UP * 0.15, angle=-TAU / 4)
            self.play(Create(ar3), Create(ar4))
            dbl = bond(c1 + UP * 0.14, c2 + UP * 0.14, color=th.MINT, w=5, shrink=0.45)
            self.play(FadeOut(ar3), FadeOut(ar4), FadeOut(bch), h_c1.animate.move_to(base.get_center() + RIGHT * 1.0), FadeOut(cplus), Create(dbl), run_time=1.4)
            self.sfx("pop")
        self.play(FadeOut(VGroup(title, a_c1, a_c2, h_c1, b12, dbl, water, wl, base, s3)))
        ax = Arrow([-6.0, -2.8, 0], [-6.0, 2.4, 0], buff=0, color=th.MUTED, stroke_width=3)
        el = T("energy", size=20, color=th.MUTED).next_to(ax, UP, buff=0.05)
        pts = [[-5.6, -1.0], [-4.8, -1.0], [-4.0, 0.0], [-3.2, -0.5], [-2.0, 1.6], [-0.8, 0.6], [0.2, 1.1], [1.2, -0.4], [2.6, -0.8], [3.4, -0.8]]
        curve = VMobject(stroke_color=th.INK, stroke_width=4).set_points_smoothly([np.array([x, y_, 0]) for x, y_ in pts])
        labs = VGroup(T("ROH₂⁺", size=22, color=th.CORAL).move_to([-3.2, -0.95, 0]), T("carbocation", size=22, color=th.AMBER).move_to([-0.8, 0.15, 0]),
                      T("slow step: highest barrier", size=22, color=th.AMBER).move_to([-2.0, 2.05, 0]), T("ethene + H₂O", size=22, color=th.MINT).move_to([3.0, -1.25, 0]))
        with self.say("On a reaction coordinate diagram, the slowest step has the highest barrier: the loss of water to form the carbocation. The carbocation sits in a shallow well, a real but short lived intermediate. And because tertiary carbocations are the most stable, tertiary alcohols dehydrate most easily: tertiary, then secondary, then primary."):
            self.play(GrowArrow(ax), FadeIn(el))
            self.play(Create(curve), run_time=2)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.3))
        self.play(FadeOut(VGroup(ax, el, curve, labs)))
        title = T("Temperature decides the product", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        top = chem(r"C_2H_5OH + \text{conc. } H_2SO_4", size=40).move_to([0, 1.6, 0])
        a1 = Arrow([-0.8, 1.2, 0], [-3.4, -0.1, 0], buff=0, color=th.CORAL, stroke_width=5)
        a2 = Arrow([0.8, 1.2, 0], [3.4, -0.1, 0], buff=0, color=th.PINK, stroke_width=5)
        p1 = VGroup(T("170 °C", size=28, color=th.CORAL, weight="BOLD"), chem(r"CH_2{=}CH_2 + H_2O", size=38, color=th.CORAL), T("intramolecular: one molecule loses water", size=20, color=th.BODY)).arrange(DOWN, buff=0.12).move_to([-3.6, -0.9, 0])
        p2 = VGroup(T("140 °C", size=28, color=th.PINK, weight="BOLD"), chem(r"C_2H_5OC_2H_5 + H_2O", size=38, color=th.PINK), T("intermolecular: two molecules share one water", size=20, color=th.BODY)).arrange(DOWN, buff=0.12).move_to([3.6, -0.9, 0])
        say_ = T("butan-2-ol → mainly but-2-ene (Saytzeff); alumina at 350 °C avoids charring", size=22, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("Change the temperature, and the product changes. At one seventy degrees each ethanol molecule loses its own water: ethene. At one forty degrees, with excess alcohol, two molecules share one water, giving ethoxyethane, diethyl ether. Where two alkenes are possible, Saytzeff's rule applies again: butan two ol gives mainly but two ene."):
            self.play(FadeIn(title), Write(top))
            self.play(GrowArrow(a1), FadeIn(p1))
            self.play(GrowArrow(a2), FadeIn(p2))
            self.play(FadeIn(say_))
        self.play(FadeOut(VGroup(title, top, a1, a2, p1, p2, say_)))
        head, prob = C.example_head(self, "4.6 g of ethanol is heated with excess conc. H₂SO₄ at 170 °C with 80 % conversion. What volume of ethene is collected at STP? What if it were heated at 140 °C instead?")
        st = C.steps(r"n = \tfrac{4.6}{46} = 0.10\ \mathrm{mol};\ \ 0.80 \times 0.10 = 0.080\ \mathrm{mol\ C_2H_4}",
                     r"V = 0.080 \times 22.4 = 1.79\ \mathrm{dm^3}",
                     r"140^{\circ}C:\ \text{ether, a liquid: no gas!}\ \ 0.040 \times 74 = 2.96\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        nb = C.show_neby(self, "wink", height=1.3)
        with self.say("Worked example ten point four. Point one mole of ethanol, eighty percent converted: zero point zero eight moles of ethene, one point seven nine litres. At one forty degrees, the trick: the product is ether, a liquid boiling at thirty four point six degrees, so no gas is collected at all. Two point nine six grams of ether instead."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))
        with self.say("Two more spokes: ethene at one seventy degrees, and ether at one forty."):
            g = self.rmap.show(self, ["hx", "na"], ["ene", "ether"])
        self.play(FadeOut(g))

    def oxidation(self):
        title = T("Oxidation: the breathalyser chemistry", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"3CH_3CH_2OH + K_2Cr_2O_7 + 4H_2SO_4 \rightarrow 3CH_3CHO + K_2SO_4 + Cr_2(SO_4)_3 + 7H_2O", size=28).next_to(title, DOWN, buff=0.35)
        sw1 = VGroup(Square(side_length=1.0, fill_color=ORANGE, fill_opacity=1, stroke_width=0), T("Cr(VI), Cr₂O₇²⁻", size=22, color=ORANGE)).arrange(DOWN, buff=0.15).move_to([-2.4, 0.4, 0])
        sw2 = VGroup(Square(side_length=1.0, fill_color=GREEN_CR, fill_opacity=1, stroke_width=0), T("Cr(III), Cr³⁺", size=22, color=GREEN_CR)).arrange(DOWN, buff=0.15).move_to([2.4, 0.4, 0])
        arr = Arrow(sw1.get_right(), sw2.get_left(), buff=0.3, color=th.MUTED, stroke_width=5)
        al = T("gains electrons from ethanol", size=20, color=th.BODY).next_to(arr, UP, buff=0.1)
        with self.say("Now the cold open. Ethanol is oxidised by acidified potassium dichromate. Ethanol loses hydrogen from the alpha carbon and becomes ethanal. Chromium is reduced from plus six in orange dichromate to plus three, which is green. That orange to green change, measured along the tube, is the breathalyser."):
            self.play(FadeIn(title), Write(eq))
            self.play(FadeIn(sw1), GrowArrow(arr), FadeIn(al), FadeIn(sw2))
        nb = C.show_neby(self, "success", height=1.3, corner=DL)
        with self.say("Mystery solved: the alcohol on a driver's breath reduces the dichromate."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(eq, sw1, sw2, arr, al)))
        lad = VGroup(
            VGroup(T("1°", size=36, color=th.SKY, weight="BOLD"), chem(r"RCH_2OH \xrightarrow{[O]} RCHO \xrightarrow{[O]} RCOOH", size=42), T("aldehyde, then acid: distil the aldehyde off as it forms", size=24, color=th.BODY)),
            VGroup(T("2°", size=36, color=th.MINT, weight="BOLD"), chem(r"R_2CHOH \xrightarrow{[O]} R_2CO", size=42), T("ketone, and it stops there", size=24, color=th.BODY)),
            VGroup(T("3°", size=36, color=th.CORAL, weight="BOLD"), chem(r"R_3COH \xrightarrow{[O]} \text{no reaction}", size=42), T("no α-hydrogen to remove", size=24, color=th.BODY)))
        for r in lad:
            r[2].next_to(r[1], DOWN, buff=0.1, aligned_edge=LEFT)
            VGroup(r[1], r[2]).next_to(r[0], RIGHT, buff=0.5)
        lad.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.5)
        with self.say("Oxidation needs a hydrogen on the alpha carbon. A primary alcohol has two, so it goes to an aldehyde and then on to a carboxylic acid, unless the volatile aldehyde is distilled off as it forms. A secondary alcohol has one, so it stops at a ketone. A tertiary alcohol has none, and resists mild oxidation."):
            for r in lad:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeOut(lad))
        cu = VGroup(T("Catalytic dehydrogenation: vapour over Cu at 300 °C", size=28, color=th.LIME, weight="BOLD"),
                    chem(r"CH_3CH_2OH \rightarrow CH_3CHO + H_2\uparrow", size=40), chem(r"(CH_3)_2CHOH \rightarrow CH_3COCH_3 + H_2\uparrow", size=40),
                    chem(r"(CH_3)_3COH \rightarrow (CH_3)_2C{=}CH_2 + H_2O\ (\text{dehydration})", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)
        with self.say("Hot copper does a similar job by removing hydrogen rather than adding oxygen. Primary gives an aldehyde, secondary a ketone, both with hydrogen gas. Tertiary cannot lose hydrogen this way, so it loses water instead, giving an alkene. Another clean way to tell the three classes apart."):
            for line in cu:
                self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(title, cu)))
        with self.say("Two more spokes: oxidation to ethanal and ethanoic acid, and dehydrogenation over copper."):
            g = self.rmap.show(self, ["hx", "na", "ene", "ether"], ["ox", "cu"])
        self.play(FadeOut(g))

    def esterification(self):
        title = T("Esterification: whose oxygen ends up in the water?", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        y = 0.2
        acid = VGroup(node("CH₃C", [-4.6, y, 0], size=36), node("O", [-4.3, y + 1.0, 0], color=OC, size=32), node("OH", [-3.2, y, 0], color=OC, size=34))
        dbl = VGroup(bond(acid[0].get_center() + RIGHT * 0.25, acid[1].get_center(), shrink=0.3), bond(acid[0].get_center() + RIGHT * 0.37, acid[1].get_center() + RIGHT * 0.12, shrink=0.3))
        ab = bond(acid[0].get_center() + RIGHT * 0.3, acid[2].get_center(), shrink=0.35)
        alc = VGroup(node("H", [0.6, y, 0], color=C.EL["H"], size=34), node("O*", [1.6, y, 0], color=th.AMBER, size=36), node("C₂H₅", [3.0, y, 0], size=36))
        b1 = bond(alc[0].get_center(), alc[1].get_center(), shrink=0.3)
        b2 = bond(alc[1].get_center(), alc[2].get_center(), shrink=0.45)
        star = T("O* = ¹⁸O label", size=22, color=th.AMBER).move_to([1.6, y - 1.0, 0])
        with self.say("Warm an alcohol with a carboxylic acid and a little concentrated sulphuric acid, and you get a sweet smelling ester. Ethanoic acid and ethanol give ethyl ethanoate and water. But which molecule loses its oxygen to the water? Label the alcohol's oxygen with the heavy isotope, oxygen eighteen, and follow it."):
            self.play(FadeIn(title), FadeIn(acid), Create(dbl), Create(ab))
            self.play(FadeIn(alc), Create(b1), Create(b2), FadeIn(star))
        with self.say("The acid loses its whole O H group, and the alcohol loses only its hydrogen. They form water. The labelled oxygen stays in the ester, bonded to the acid's carbon. So the water comes from the acid's O H, not the alcohol's."):
            w = VGroup(acid[2], alc[0])
            self.play(FadeOut(ab), FadeOut(b1), w.animate.arrange(RIGHT, buff=0.05).move_to([0, -1.8, 0]), run_time=1.4)
            wl = T("water", size=24, color=C.WATER).next_to(w, DOWN, buff=0.1)
            self.play(FadeIn(wl), VGroup(alc[1], alc[2], b2).animate.shift(LEFT * 3.4))
            newb = bond(acid[0].get_center() + RIGHT * 0.3, alc[1].get_center(), color=th.AMBER, shrink=0.35)
            self.play(Create(newb))
            self.sfx("pop")
        eq = chem(r"CH_3COOH + C_2H_5OH \rightleftharpoons CH_3COOC_2H_5 + H_2O", size=36, color=th.TEAL).to_edge(DOWN, buff=0.5)
        nt = T("reversible; rate 1° > 2° > 3°; with CH₃COCl it is fast and complete", size=22, color=th.MUTED).next_to(eq, UP, buff=0.15)
        with self.say("The reaction is reversible, so the sulphuric acid acts both as catalyst and as a water remover. Primary alcohols esterify fastest. With an acid chloride instead of the acid, the reaction is fast and goes to completion."):
            self.play(Write(eq), FadeIn(nt))
        self.play(FadeOut(VGroup(title, acid, dbl, alc, b2, newb, star, w, wl, eq, nt)))
        with self.say("Another spoke: esterification."):
            g = self.rmap.show(self, ["hx", "na", "ene", "ether", "ox", "cu"], ["ester"])
        self.play(FadeOut(g))

    def tests(self):
        title = T("Tests for ethanol", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        tb_ = RoundedRectangle(corner_radius=0.25, width=1.0, height=2.8, stroke_color=th.INK, stroke_width=3).move_to([-4.6, -0.6, 0])
        liq = Rectangle(width=0.86, height=1.8, fill_color="#C08A3A", fill_opacity=0.5, stroke_width=0).align_to(tb_, DOWN).shift(UP * 0.12).set_x(-4.6)
        rng = np.random.default_rng(10)
        crys = VGroup(*[Square(side_length=0.09, fill_color="#F2D43C", fill_opacity=1, stroke_width=0).rotate(rng.uniform(0, 1)).move_to([-4.6 + rng.uniform(-0.3, 0.3), -1.75 + rng.uniform(0, 0.4), 0]) for _ in range(26)])
        tl = VGroup(T("iodoform test", size=24, color="#F2D43C", weight="BOLD"), T("I₂ + NaOH, warm 60 °C", size=20, color=th.BODY), T("yellow CHI₃, antiseptic smell", size=20, color=th.BODY)).arrange(DOWN, buff=0.06).next_to(tb_, DOWN, buff=0.2)
        eq = chem(r"CH_3CH_2OH + 4I_2 + 6NaOH \rightarrow CHI_3\downarrow + 5NaI + HCOONa + 5H_2O", size=28, color="#F2D43C").next_to(title, DOWN, buff=0.35).shift(RIGHT * 1.0)
        rows = [["Test", "Observation"], ["ester test (CH₃COOH + H₂SO₄)", "fruity smell"], ["sodium", "steady fizz of H₂"], ["acidified K₂Cr₂O₇", "orange → green"], ["neutral FeCl₃", "no colour (phenol gives violet)"]]
        tb = C.table(rows, [4.6, 4.2], row_h=0.62, size=23, colors=[th.AMBER, th.BODY]).move_to([2.3, -1.1, 0])
        with self.say("Finally, the tests for ethanol. The iodoform test: warm with iodine and sodium hydroxide, and yellow crystals of iodoform appear, with a sharp antiseptic smell. Ethanol also gives a fruity ester with ethanoic acid, a steady fizz with sodium, turns dichromate green, and gives no colour with neutral iron three chloride, which is how it is told apart from phenol, our next unit."):
            self.play(FadeIn(title), FadeIn(tb_), FadeIn(liq), Write(eq))
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.3) for c_ in crys], lag_ratio=0.03), FadeIn(tl), run_time=1.5)
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
        self.play(FadeOut(VGroup(title, tb_, liq, crys, tl, eq, tb)))
        with self.say("The last spoke: the iodoform test."):
            g = self.rmap.show(self, ["hx", "na", "ene", "ether", "ox", "cu", "ester"], ["iodo"])
        self.play(FadeOut(g))
        head, prob = C.example_head(self, "Alcohol A, C₄H₁₀O, gives Lucas turbidity after about 5 min, a blue Victor Meyer colour, and a positive iodoform test. Oxidation gives B, C₄H₈O, which does not reduce Fehling's solution. Identify A and B.")
        st = VGroup(T("Lucas ~5 min → secondary", size=26, color=th.SKY), T("Victor Meyer blue → secondary (one α-H)", size=26, color=th.SKY),
                    T("only 2° C₄H₁₀O: butan-2-ol, CH₃CH(OH)CH₂CH₃ = A", size=26, color=th.AMBER), T("has CH₃CH(OH)–: iodoform positive ✓", size=26, color=th.MINT),
                    chem(r"CH_3CH(OH)CH_2CH_3 \xrightarrow{[O]} CH_3COCH_2CH_3\ (\text{butanone} = B)", size=32, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        with self.say("Worked example ten point three, a detective problem. Lucas turbidity in five minutes says secondary. A blue Victor Meyer colour confirms it. The only secondary alcohol with formula C four H ten O is butan two ol. It has the C H three C H O H group, so the iodoform test fits. Oxidising a secondary alcohol gives a ketone, butanone, which cannot reduce Fehling's solution. So A is butan two ol and B is butanone."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "CₙH₂ₙ₊₁OH; 1°, 2°, 3° by carbons on the carbinol carbon.",
            "Victor Meyer: red 1°, blue 2°, colourless 3°; Lucas: 3° at once.",
            "Made from RX (aq KOH), RNH₂ (HNO₂), esters; oxo, hydroboration, fermentation.",
            "Rectified spirit 95.6 % (azeotrope); absolute alcohol needs CaO.",
            "High b.p. from hydrogen bonding; branching lowers b.p.",
            "Conc. H₂SO₄: 170 °C → ethene (E1), 140 °C → ether.",
            "K₂Cr₂O₇: 1° → aldehyde → acid, 2° → ketone, 3° none (orange → green).",
            "Esterification: water from the acid's –OH; iodoform for CH₃CH(OH)–.",
        ], "Let us recap. Alcohols are primary, secondary or tertiary, and Victor Meyer and Lucas tests tell them apart. They are made from haloalkanes, amines and esters, and industrially by the oxo process, hydroboration and fermentation. Distillation stops at ninety five point six percent. Hydrogen bonding gives high boiling points. Concentrated sulphuric acid dehydrates them to alkenes or ethers, depending on temperature. Dichromate oxidises primary and secondary alcohols, turning green. And esters form with water coming from the acid.")
        self.outro("That is alcohols. Next, we put the hydroxyl group directly on a benzene ring, and meet a far more acidic family, the phenols. See you in the next lesson on NEBians.")
