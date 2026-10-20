import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem, push, benzene  # noqa: E402

OC = "#FF6B6B"
VIOLET = "#7B3FC4"

MAP = [("naoh", r"C_6H_5ONa", "NaOH or Na", th.MINT),
       ("nh3", r"C_6H_5NH_2", "NH₃, ZnCl₂, 300 °C", th.SKY),
       ("zn", r"C_6H_6", "Zn dust, heat", th.MUTED),
       ("azo", r"HO{-}C_6H_4{-}N{=}N{-}C_6H_5", "C₆H₅N₂Cl, OH⁻, 0–5 °C", "#F08A24"),
       ("br", r"C_6H_2Br_3OH\downarrow", "bromine water", th.LIME),
       ("nit", r"\text{picric acid}", "conc. HNO₃ + H₂SO₄", "#F2D43C"),
       ("rt", r"\text{salicylaldehyde}", "CHCl₃ + NaOH, 60 °C", th.PINK),
       ("kolbe", r"\text{salicylic acid}", "CO₂, 125 °C; then H⁺", th.AMBER),
       ("ac", r"CH_3COOC_6H_5", "CH₃COCl", th.TEAL)]


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 11
    TITLE = "Phenols"
    SUBTITLE = "When –OH sits on a benzene ring"
    SECTIONS = ["Introduction and naming", "Preparation", "Physical properties", "Acidic nature",
                "NH₃, Zn, Na, diazonium, phthalic anhydride", "Acylation, Kolbe, Reimer–Tiemann",
                "Electrophilic substitution", "Tests and uses"]
    NEXT = "Unit 12 · Ethers"

    def lesson(self):
        self.rmap = C.ReactionMap(r"C_6H_5OH", MAP)
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        e = VGroup(chem(r"C_2H_5{-}OH", size=56, color=th.SKY), T("ethanol", size=26, color=th.SKY)).arrange(DOWN, buff=0.2).move_to([-3.6, 1.6, 0])
        p = VGroup(benzene(r=0.75, subs={0: ("OH", OC)}), T("phenol (carbolic acid)", size=26, color=OC)).arrange(DOWN, buff=0.2).move_to([3.4, 1.4, 0])
        with self.say("Two compounds, both with an O H group. Ethanol, in every bottle of raksi. And phenol, an O H on a benzene ring, the carbolic acid that Joseph Lister sprayed in his operating theatre in eighteen sixty seven, the birth of antiseptic surgery."):
            self.play(FadeIn(e, shift=UP * 0.2))
            self.play(FadeIn(p, shift=UP * 0.2))
        b1 = C.Beaker(center=[-3.6, -1.6, 0], w=2.2, h=1.8, level=0.7, color=th.SKY, opacity=0.3)
        b2 = C.Beaker(center=[3.4, -1.6, 0], w=2.2, h=1.8, level=0.7, color=th.SKY, opacity=0.3)
        lab = T("each added to sodium hydroxide solution", size=24, color=th.MUTED).move_to([0, -0.2, 0])
        drop1 = VGroup(*[Circle(radius=0.12, fill_color=th.SKY, fill_opacity=0.5, stroke_width=0).move_to([-3.6 + 0.3 * (k - 1), -1.35, 0]) for k in range(3)])
        cr = VGroup(*[Square(side_length=0.18, fill_color="#F6E6EA", fill_opacity=1, stroke_width=0).move_to([3.4 + 0.3 * (k - 1), -2.2, 0]) for k in range(3)])
        r1 = T("no reaction: stays neutral", size=22, color=th.SKY).next_to(b1.g, DOWN, buff=0.15)
        r2 = T("dissolves completely!", size=22, color=OC, weight="BOLD").next_to(b2.g, DOWN, buff=0.15)
        with self.say("Add each to sodium hydroxide solution. Ethanol just mixes, with no reaction at all: it is no acid. But phenol dissolves completely, reacting with the alkali like an acid. It even burns skin."):
            self.play(FadeIn(b1.g), FadeIn(b2.g), FadeIn(lab))
            self.play(FadeIn(drop1), FadeIn(cr))
            self.play(FadeIn(r1), cr.animate.scale(0.2).set_opacity(0), FadeIn(r2), run_time=1.6)
        nb = C.show_neby(self, "surprised", height=1.5, at=[0, 1.6, 0])
        with self.say("Same O H group. Why is one an acid and the other not? The answer is the benzene ring, and how it spreads charge around. We will see it move in part four."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(e, p, b1.g, b2.g, lab, drop1, cr, r1, r2)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 11: Phenols. Compounds with an O H group directly on a benzene ring. They are acids, they are antiseptics, and they are the starting point for aspirin, dyes, indicators and plastics."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. What phenols are and how they are named. Three ways to prepare phenol. Physical properties. Why phenol is acidic. Its reactions with ammonia, zinc, sodium, diazonium salts and phthalic anhydride. Acylation, and the Kolbe and Reimer Tiemann reactions. Electrophilic substitution. And finally, tests and uses.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        a = VGroup(benzene(r=0.8, subs={0: ("OH", OC)}), T("phenol: –OH on the ring", size=26, color=OC, weight="BOLD"), T("violet with FeCl₃", size=22, color=th.BODY)).arrange(DOWN, buff=0.2).move_to([-3.4, 0.0, 0])
        b = VGroup(benzene(r=0.8, subs={0: ("CH₂OH", th.SKY)}), T("benzyl alcohol: –OH on a side chain", size=26, color=th.SKY, weight="BOLD"), T("a normal 1° alcohol, no FeCl₃ colour", size=22, color=th.BODY)).arrange(DOWN, buff=0.2).move_to([3.4, 0.0, 0])
        with self.say("A phenol has an O H directly on an aromatic ring, general formula A r O H. Do not confuse it with an aromatic alcohol like benzyl alcohol, where the O H is on a side chain carbon. Benzyl alcohol behaves like an ordinary primary alcohol."):
            self.play(FadeIn(a, shift=UP * 0.2))
            self.play(FadeIn(b, shift=UP * 0.2))
        self.play(FadeOut(VGroup(a, b)))
        title = T("Phenols you should recognise", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        items = [({0: ("OH", OC)}, "phenol", "carbolic acid"), ({0: ("OH", OC), 1: ("CH₃", th.MUTED)}, "2-methylphenol", "o-cresol"),
                 ({0: ("OH", OC), 3: ("CH₃", th.MUTED)}, "4-methylphenol", "p-cresol"), ({0: ("OH", OC), 1: ("OH", OC)}, "benzene-1,2-diol", "catechol"),
                 ({0: ("OH", OC), 2: ("OH", OC)}, "benzene-1,3-diol", "resorcinol"), ({0: ("OH", OC), 3: ("OH", OC)}, "benzene-1,4-diol", "quinol"),
                 ({0: ("OH", OC), 1: ("OH", OC), 2: ("OH", OC)}, "benzene-1,2,3-triol", "pyrogallol"), ({0: ("OH", OC), 1: ("NO₂", "#5C8DFF"), 3: ("NO₂", "#5C8DFF"), 5: ("NO₂", "#5C8DFF")}, "2,4,6-trinitrophenol", "picric acid")]
        cards = VGroup()
        for subs, n1, n2 in items:
            cards.add(VGroup(benzene(r=0.6, subs=subs, label_size=22), T(n1, size=22, color=th.INK), T(n2, size=22, color=th.AMBER, weight="BOLD")).arrange(DOWN, buff=0.12))
        cards.arrange_in_grid(rows=2, cols=4, buff=(0.6, 0.25)).next_to(title, DOWN, buff=0.3)
        if cards.height > 5.9:
            cards.scale_to_fit_height(5.9).next_to(title, DOWN, buff=0.3)
        with self.say("Here are the ones to recognise. Phenol itself. The cresols, with a methyl group. The dihydric phenols: catechol, resorcinol and quinol. Pyrogallol with three O H groups. And picric acid, two four six trinitrophenol. Number the ring from the O H carbon, and use o, m and p for two substituents.") as v:
            self.play(FadeIn(title))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 8 - 0.45)
        self.play(FadeOut(VGroup(title, cards)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Three routes to phenol", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cl = benzene([-4.6, 1.0, 0], r=0.7, subs={0: ("Cl", "#7BE495")}, label_size=26)
        so = benzene([-0.4, 1.0, 0], r=0.7, subs={0: ("SO₃H", "#F2D43C")}, label_size=26)
        dz = benzene([4.4, 1.0, 0], r=0.7, subs={0: ("N₂⁺Cl⁻", th.PINK)}, label_size=26)
        lab = VGroup(VGroup(T("Dow process", size=26, color="#7BE495", weight="BOLD"), para("NaOH, 300 °C, 150 atm", width=3.6, size=22, color=th.BODY, align="center")).arrange(DOWN, buff=0.06).next_to(cl, DOWN, buff=0.3),
                     VGroup(T("warm the diazonium salt", size=26, color=th.PINK, weight="BOLD"), para("aqueous acid, above 5 °C; N₂ bubbles off", width=3.6, size=22, color=th.BODY, align="center")).arrange(DOWN, buff=0.06).next_to(dz, DOWN, buff=0.3),
                     VGroup(T("alkali fusion", size=26, color="#F2D43C", weight="BOLD"), para("fuse the Na salt with NaOH, 300–350 °C", width=3.6, size=22, color=th.BODY, align="center")).arrange(DOWN, buff=0.06).next_to(so, DOWN, buff=0.3))
        mid = VGroup(chem(r"C_6H_5ONa", size=44, color=th.MINT), T("sodium phenoxide", size=22, color=th.MINT)).arrange(DOWN, buff=0.08).move_to([-2.4, -2.1, 0])
        ph = chem(r"C_6H_5OH", size=50, color=OC).move_to([3.4, -2.0, 0])
        ars = VGroup(Arrow(lab[0].get_bottom(), mid.get_top() + LEFT * 0.4, buff=0.1, color=th.MUTED, stroke_width=4),
                     Arrow(lab[2].get_bottom(), mid.get_top() + RIGHT * 0.4, buff=0.1, color=th.MUTED, stroke_width=4))
        dza = Arrow(lab[1].get_bottom(), ph.get_top(), buff=0.12, color=th.PINK, stroke_width=4)
        fin = VGroup(Arrow(mid.get_right(), ph.get_left(), buff=0.25, color=th.AMBER, stroke_width=6), T("+ HCl", size=28, color=th.AMBER, weight="BOLD"))
        fin[1].next_to(fin[0], UP, buff=0.08)
        with self.say("Three ways to make phenol. From chlorobenzene, by the Dow process: sodium hydroxide at three hundred degrees and a hundred and fifty atmospheres, since chlorobenzene is so unreactive. From benzene diazonium chloride, simply by warming its acidic solution above five degrees, so nitrogen bubbles off: the mild laboratory method. And from benzene sulphonic acid, by fusing its sodium salt with solid sodium hydroxide."):
            self.play(FadeIn(title))
            for r_, l_ in ((cl, lab[0]), (dz, lab[1]), (so, lab[2])):
                self.play(Create(r_), FadeIn(l_), run_time=0.8)
        with self.say("Notice something. The Dow process and alkali fusion stop at sodium phenoxide, a salt that dissolves in water. You must acidify at the end, with hydrochloric acid or even carbon dioxide, to set phenol free. Forgetting that step costs a mark every year."):
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in ars], lag_ratio=0.2), FadeIn(mid), GrowArrow(dza), FadeIn(ph))
            self.play(GrowArrow(fin[0]), FadeIn(fin[1]))
            self.play(Indicate(fin[1], color=th.AMBER, scale_factor=1.3))
        self.play(FadeOut(VGroup(title, cl, dz, so, lab, mid, ars, dza, fin, ph)))
        eqs = VGroup(chem(r"C_6H_5Cl + 2NaOH \xrightarrow{300^{\circ}C,\ 150\ atm} C_6H_5ONa + NaCl + H_2O", size=42),
                     chem(r"C_6H_5N_2Cl + H_2O \xrightarrow{\text{warm}} C_6H_5OH + N_2\uparrow + HCl", size=42),
                     chem(r"C_6H_5SO_3Na + 2NaOH \xrightarrow{\text{fuse}} C_6H_5ONa + Na_2SO_3 + H_2O", size=42),
                     chem(r"C_6H_5ONa + HCl \rightarrow C_6H_5OH + NaCl", size=46, color=th.AMBER)).arrange(DOWN, buff=0.4)
        with self.say("Here are the equations in full."):
            self.play(LaggedStart(*[FadeIn(e_, shift=RIGHT * 0.2) for e_ in eqs], lag_ratio=0.3), run_time=2.5)
        self.play(FadeOut(eqs))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        rng = np.random.default_rng(4)
        needles = VGroup(*[Line(ORIGIN, RIGHT * 1.2, color="#F6E6EA", stroke_width=8).rotate(rng.uniform(0, PI)).move_to([-4.6 + rng.uniform(-1.2, 1.2), -0.2 + rng.uniform(-1.2, 1.2), 0]) for _ in range(22)])
        facts = VGroup(para("colourless needles, m.p. 40.9 °C, b.p. 181.8 °C", width=7.4, size=28, color=th.INK), para("turns pink in air and light (slow oxidation)", width=7.4, size=28, color=th.PINK),
                       para("sharp carbolic smell; corrosive, blisters skin", width=7.4, size=28, color=OC), para("8.3 g per 100 g water at 20 °C; miscible above 66 °C", width=7.4, size=28, color=th.SKY),
                       para("high b.p. for M = 94: hydrogen bonding", width=7.4, size=28, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.2, -0.1, 0])
        with self.say("Phenol is a colourless solid that forms long needle shaped crystals, melting at forty one degrees and boiling at one eighty two. Left in air and light it slowly turns pink. It has a sharp carbolic smell, and it is corrosive, raising painful blisters on skin. It dissolves only a little in cold water, about eight grams per hundred, but mixes completely above sixty six degrees. Like alcohols, its molecules are linked by hydrogen bonds, which explains its high boiling point.") as v:
            self.play(LaggedStart(*[Create(n_) for n_ in needles], lag_ratio=0.05), run_time=1.5)
            for f in facts:
                self.play(FadeIn(f, shift=LEFT * 0.2), run_time=0.45)
                self.hold(v.dur / 5 - 0.6)
            self.play(needles.animate.set_color("#F7B8C8"), run_time=1.0)
        self.play(FadeOut(VGroup(needles, facts)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        eq = chem(r"C_6H_5OH + H_2O \rightleftharpoons C_6H_5O^- + H_3O^+,\quad K_a = 1.0\times10^{-10}", size=38).to_edge(UP, buff=0.8)
        with self.say("Phenol ionises slightly in water, with K a of one times ten to the minus ten, p K a ten. Why is it an acid at all, when ethanol is not? Look at what is left behind when the proton goes: the phenoxide ion."):
            self.play(Write(eq))
        base = np.array([0, -0.9, 0])
        ring_ = benzene(base, r=1.45, kekule=True)
        v = ring_.verts
        o = v[0] + UP * 1.0
        ob = Line(v[0], o + DOWN * 0.25, color=th.MUTED, stroke_width=5)
        ol = T("O", size=48, color=OC, weight="BOLD").move_to(o)
        minus = T("−", size=44, color=OC, weight="BOLD").next_to(ol, UR, buff=0.0)
        lp = VGroup(Dot(o + np.array([-0.3, 0.12, 0]), radius=0.05, color=th.AMBER), Dot(o + np.array([-0.3, -0.08, 0]), radius=0.05, color=th.AMBER))
        self.play(Create(ring_), Create(ob), FadeIn(ol), FadeIn(minus), FadeIn(lp))
        charge = Dot(o + RIGHT * 0.45, radius=0.15, color=OC)
        tag = T("negative charge", size=22, color=OC).to_edge(RIGHT, buff=0.7).shift(UP * 1.2)
        with self.say("The oxygen carries a negative charge and a lone pair. Watch the electrons move. The lone pair swings in to form a carbon oxygen double bond, and the ring's pi electrons shift along, pushing the negative charge onto the ortho carbon."):
            self.play(FadeIn(tag))
            a1 = push(lp.get_center() + LEFT * 0.05, (o + v[0]) / 2 + LEFT * 0.15, angle=TAU / 4)
            a2 = push((v[0] + v[1]) / 2 + RIGHT * 0.05, v[1] + RIGHT * 0.2, angle=-TAU / 4)
            self.play(Create(a1), Create(a2))
            self.play(charge.animate.move_to(v[1] + RIGHT * 0.35 + UP * 0.1), FadeOut(minus), run_time=1.0)
            self.play(FadeOut(a1), FadeOut(a2))
        with self.say("Shift again, and the charge lands on the para carbon. Again, on the other ortho carbon. The negative charge is not stuck on oxygen. It is spread over oxygen and three ring carbons, the ortho and para positions."):
            for target in (v[3] + DOWN * 0.35, v[5] + LEFT * 0.35 + UP * 0.1):
                self.play(charge.animate.move_to(target), run_time=0.9)
                self.play(Flash(target, color=OC, flash_radius=0.4), run_time=0.4)
            spread = VGroup(*[Dot(p_, radius=0.12, color=OC, fill_opacity=0.6) for p_ in (o + RIGHT * 0.45, v[1] + RIGHT * 0.35 + UP * 0.1, v[3] + DOWN * 0.35, v[5] + LEFT * 0.35 + UP * 0.1)])
            self.play(FadeOut(charge), FadeIn(spread))
        key = para("Spreading the charge stabilises the phenoxide ion, so phenol gives up its proton more readily.", width=4.6, size=26, color=th.MINT).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        eth = VGroup(chem(r"CH_3CH_2O^-", size=40, color=th.SKY), para("ethoxide: charge stuck on O, and the ethyl group (+I) pushes in even more: unstable", width=4.2, size=22, color=th.BODY)).arrange(DOWN, buff=0.15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.8)
        with self.say("Spreading charge lowers energy, so the phenoxide ion is unusually stable, and phenol gives up its proton more readily. In the ethoxide ion there is no ring to spread into. The charge is stuck on oxygen, and the ethyl group pushes even more electron density onto it. So ethanol is far weaker. A second reason: in phenol itself, oxygen's lone pair already leaks into the ring, so the oxygen holds the O H electrons more tightly, and the proton leaves more easily."):
            self.play(FadeOut(tag), FadeIn(key))
            self.play(FadeIn(eth))
        nb = C.show_neby(self, "success", height=1.3, corner=UR, buff=0.9)
        with self.say("That is the cold open solved."):
            self.wait(0.3)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(eq, ring_, ob, ol, lp, spread, key, eth)))
        self.ladder()

    def ladder(self):
        title = T("How acidic? A pKa ladder", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        items = [("ethanol", 16.0, th.SKY), ("water", 15.7, C.WATER), ("phenol", 10.0, OC), ("carbonic acid", 6.35, th.MUTED), ("ethanoic acid", 4.76, th.AMBER)]
        ax = Arrow([-3.6, 2.6, 0], [-3.6, -2.55, 0], buff=0, color=th.MUTED, stroke_width=4)
        al = T("stronger acid", size=22, color=th.MUTED).next_to(ax.get_end(), DOWN, buff=0.1)
        rows = VGroup()
        for n, pk, col in items:
            yy = 2.3 - (16.5 - pk) * 0.38
            rows.add(VGroup(Dot([-3.6, yy, 0], radius=0.1, color=col), T(n, size=26, color=col, weight="BOLD").next_to([-3.3, yy, 0], RIGHT, buff=0), T(f"pKa {pk:g}", size=22, color=th.BODY).next_to([-3.85, yy, 0], LEFT, buff=0)))
        rows[0][1].shift(UP * 0.12)
        rows[0][2].shift(UP * 0.12)
        rows[1][1].shift(DOWN * 0.22)
        rows[1][2].shift(DOWN * 0.22)
        with self.say("Where does phenol stand? Its p K a is ten. Ethanol, about sixteen, and water fifteen point seven, are far weaker acids. But carbonic acid, six point three five, and ethanoic acid, four point seven six, are stronger. Phenol sits in between: stronger than water and alcohol, weaker than carbonic acid."):
            self.play(FadeIn(title), GrowArrow(ax), FadeIn(al))
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(rows[2], color=OC, scale_factor=1.1))
        rows_t = [["Reagent", "phenol", "ethanol", "carboxylic acid"], ["Na", "H₂", "H₂", "H₂"], ["NaOH(aq)", "dissolves", "no reaction", "dissolves"], ["NaHCO₃(aq)", "no CO₂", "no reaction", "CO₂ fizz"]]
        tb = C.table(rows_t, [2.6, 2.4, 2.4, 2.8], row_h=0.62, size=24, colors=[th.AMBER, OC, th.SKY, th.MINT]).move_to([3.1, -0.6, 0])
        tb.scale_to_fit_width(7.4)
        tb.move_to([2.8, -0.6, 0])
        with self.say("So sodium hydroxide dissolves phenol but not ethanol, and sodium bicarbonate gives carbon dioxide with a carboxylic acid but not with phenol. That is how the three are separated."):
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
        self.play(FadeOut(VGroup(title, ax, al, rows, tb)))
        subs = VGroup(*[VGroup(T(n, size=26, color=c, weight="BOLD"), T(f"pKa {p}", size=24, color=th.BODY)).arrange(DOWN, buff=0.06) for n, p, c in
                        [("picric acid", "0.38", "#F2D43C"), ("p-nitrophenol", "7.15", "#5C8DFF"), ("phenol", "10.0", OC), ("p-cresol", "10.26", th.MUTED)]]).arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        gts = VGroup(*[T(">", size=36, color=th.MUTED).move_to((a_.get_right() + b_.get_left()) / 2) for a_, b_ in zip(subs, subs[1:])])
        expl = para("electron-withdrawing NO₂ spreads the charge further: stronger acid. Electron-releasing CH₃: weaker.", width=11, size=26, color=th.AMBER, align="center").next_to(subs, DOWN, buff=0.7)
        with self.say("Substituents tune the acidity. Electron withdrawing nitro groups pull charge away from the phenoxide ion and stabilise it, so para nitrophenol is stronger, and picric acid, with three nitro groups, is almost as strong as a mineral acid. An electron releasing methyl group does the opposite: para cresol is slightly weaker than phenol."):
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in subs], lag_ratio=0.3), FadeIn(gts))
            self.play(FadeIn(expl))
        self.play(FadeOut(VGroup(subs, gts, expl)))
        head, prob = C.example_head(self, "Ka of phenol is 1.0 × 10⁻¹⁰ at 25 °C. Find the pH and the degree of ionisation of 0.01 M phenol.")
        st = C.steps(r"[\mathrm{H^+}] = \sqrt{K_aC} = \sqrt{(1.0\times10^{-10})(1.0\times10^{-2})} = 1.0\times10^{-6}",
                     r"pH = -\log(1.0\times10^{-6}) = 6.0",
                     r"\alpha = \sqrt{K_a/C} = \sqrt{10^{-10}/10^{-2}} = 1.0\times10^{-4} = 0.01\,\%", size=40).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example eleven point one, straight from Unit 2. Hydrogen ion is the square root of K a C: the square root of ten to the minus twelve, ten to the minus six. So p H six. And the degree of ionisation is root K a over C, ten to the minus four: only one molecule in ten thousand. Acidic, but only just."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "Phenol dissolves in NaOH but gives no CO₂ with NaHCO₃. Justify with Ka(phenol) = 1.0 × 10⁻¹⁰, Ka1(H₂CO₃) = 4.5 × 10⁻⁷, Kw = 1.0 × 10⁻¹⁴.")
        st = C.steps(r"\mathrm{C_6H_5OH + OH^- \rightleftharpoons C_6H_5O^- + H_2O}:\ K = \frac{K_a}{K_w} = 1.0\times10^{4} \gg 1",
                     r"\mathrm{C_6H_5OH + HCO_3^- \rightleftharpoons C_6H_5O^- + H_2CO_3}:\ K = \frac{1.0\times10^{-10}}{4.5\times10^{-7}} = 2.2\times10^{-4} \ll 1", size=34).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        with self.say("Worked example eleven point two. With hydroxide, the equilibrium constant is K a over K w, ten thousand: the reaction goes to completion, and phenol dissolves. With bicarbonate, it is K a of phenol over K a of carbonic acid, two point two times ten to the minus four: almost no reaction, so no carbonic acid, and no carbon dioxide. Phenol is weaker than carbonic acid."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("Which of these is the strongest acid?",
                  ["ethanol", "phenol", "p-cresol", "p-nitrophenol"], 3,
                  "Pause and think. Which of these four is the strongest acid?",
                  "D, para nitrophenol. The nitro group withdraws electrons and spreads the phenoxide's negative charge further, stabilising it. Para cresol's methyl group does the opposite, and ethanol has no ring at all to spread the charge.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("Four quick reactions", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eqs = VGroup(
            VGroup(T("ammonia", size=28, color=th.SKY, weight="BOLD"), chem(r"C_6H_5OH + NH_3 \xrightarrow{ZnCl_2,\ 300^{\circ}C} C_6H_5NH_2 + H_2O", size=42)),
            VGroup(T("zinc dust", size=28, color=th.MUTED, weight="BOLD"), chem(r"C_6H_5OH + Zn \xrightarrow{\text{distil}} C_6H_6 + ZnO", size=42)),
            VGroup(T("sodium", size=28, color=th.MINT, weight="BOLD"), chem(r"2C_6H_5OH + 2Na \rightarrow 2C_6H_5ONa + H_2\uparrow", size=42)),
            VGroup(T("sodium hydroxide", size=28, color=th.MINT, weight="BOLD"), chem(r"C_6H_5OH + NaOH \rightarrow C_6H_5ONa + H_2O", size=42)))
        for e_ in eqs:
            e_.arrange(RIGHT, buff=0.4)
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.5)
        with self.say("Some quick reactions first. Over zinc chloride at three hundred degrees, ammonia replaces the O H to give aniline. Distilling phenol with zinc dust removes the oxygen, giving benzene. And sodium metal, or sodium hydroxide, gives sodium phenoxide.") as v:
            self.play(FadeIn(title))
            for e_ in eqs:
                self.play(FadeIn(e_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.65)
        self.play(FadeOut(VGroup(title, eqs)))
        with self.say("Let us start the reaction map of phenol with these."):
            g = self.rmap.show(self, [], ["naoh", "nh3", "zn"])
        self.play(FadeOut(g))
        title = T("Coupling: making an azo dye", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        a = benzene([-4.0, 0.0, 0], r=0.8, subs={1: ("N≡N⁺", th.PINK)}, label_size=24)
        b = benzene([1.2, 0.0, 0], r=0.8, subs={0: ("O⁻", OC)}, label_size=24)
        para_ = Dot(b.verts[3], radius=0.12, color=th.AMBER)
        with self.say("Now a beautiful one. Benzene diazonium chloride is a weak electrophile. It can only attack a strongly activated ring, like the phenoxide ion in cold alkali, at zero to five degrees. It attacks the para position."):
            self.play(FadeIn(title), Create(a), Create(b))
            self.play(FadeIn(para_, scale=2))
            arr = push(b.verts[3] + DOWN * 0.1 + LEFT * 0.1, a[3].get_right() + RIGHT * 0.1, angle=-TAU / 4)
            self.play(Create(arr))
        dye = VGroup(benzene(r=0.9), T("N=N", size=40, color=th.PINK, weight="BOLD"), benzene(r=0.9, subs={0: ("OH", OC)}, label_size=28)).arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
        swatch = Rectangle(width=12, height=6, fill_color="#F08A24", fill_opacity=0, stroke_width=0)
        name = T("p-hydroxyazobenzene: an orange dye", size=28, color="#F08A24", weight="BOLD").next_to(dye, DOWN, buff=0.6)
        with self.say("The two rings join through an N equals N bridge, giving para hydroxy azobenzene, a bright orange dye. This coupling is the basis of the whole azo dye industry."):
            self.play(FadeOut(VGroup(a, b, para_, arr)), FadeIn(dye, scale=0.8))
            self.add(swatch)
            self.play(swatch.animate.set_fill(opacity=0.12), FadeIn(name))
            self.play(swatch.animate.set_fill(opacity=0), run_time=0.8)
        self.remove(swatch)
        self.play(FadeOut(VGroup(title, dye, name)))
        title = T("Phthalic anhydride → phenolphthalein", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"C_6H_4(CO)_2O + 2C_6H_5OH \xrightarrow{\text{conc. } H_2SO_4,\ \text{heat}} C_{20}H_{14}O_4 + H_2O", size=42).next_to(title, DOWN, buff=0.5)
        f1 = C.Flask(center=[-2.2, -1.4, 0], scale=1.1, color="#E6E9F2", opacity=0.2)
        f2 = C.Flask(center=[2.2, -1.4, 0], scale=1.1, color="#FF4FB8", opacity=0.7)
        l1 = T("in acid: colourless", size=22, color=th.BODY).next_to(f1.g, DOWN, buff=0.15)
        l2 = T("in alkali: pink", size=22, color="#FF4FB8").next_to(f2.g, DOWN, buff=0.15)
        with self.say("Heat two molecules of phenol with phthalic anhydride and concentrated sulphuric acid, and you get phenolphthalein, the indicator from Unit 1: colourless in acid, pink in alkali."):
            self.play(FadeIn(title), Write(eq))
            self.play(FadeIn(f1.g), FadeIn(l1), FadeIn(f2.g), FadeIn(l2))
        self.play(FadeOut(VGroup(title, eq, f1.g, f2.g, l1, l2)))
        with self.say("Coupling adds the azo dye to our map."):
            g = self.rmap.show(self, ["naoh", "nh3", "zn"], ["azo"])
        self.play(FadeOut(g))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Acylation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eqs = VGroup(chem(r"C_6H_5OH + CH_3COCl \rightarrow CH_3COOC_6H_5 + HCl", size=44), chem(r"C_6H_5OH + (CH_3CO)_2O \rightarrow CH_3COOC_6H_5 + CH_3COOH", size=44),
                     T("phenyl ethanoate; pyridine or NaOH mops up the acid", size=28, color=th.BODY),
                     T("Fries rearrangement: heat with AlCl₃ → o- and p-hydroxyacetophenone", size=28, color=th.AMBER)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.5)
        with self.say("Phenol is a poor nucleophile, so to make its esters we use an acid chloride or anhydride, with a base to remove the acid formed. Phenyl ethanoate results. Heat that ester with aluminium chloride, and the acetyl group hops onto the ring: the Fries rearrangement."):
            self.play(FadeIn(title))
            for e_ in eqs:
                self.play(FadeIn(e_, shift=UP * 0.2), run_time=0.7)
        self.play(FadeOut(VGroup(title, eqs)))
        title = T("Kolbe's reaction: CO₂ → salicylic acid → aspirin", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ph = benzene([-3.8, -0.4, 0], r=1.25, subs={0: ("O⁻ Na⁺", OC)}, label_size=30)
        co2 = T("O=C=O", size=42, color=th.AMBER, weight="BOLD").move_to([-0.4, 1.6, 0])
        ortho = Dot(ph.verts[1], radius=0.12, color=th.AMBER)
        with self.say("Kolbe's reaction. Dry sodium phenoxide absorbs carbon dioxide at one hundred and twenty five degrees under four to seven atmospheres. Carbon dioxide is a weak electrophile. It attacks the ortho position of the activated phenoxide ring."):
            self.play(FadeIn(title), Create(ph), FadeIn(co2))
            self.play(FadeIn(ortho, scale=2))
            arr = push(ph.verts[1] + RIGHT * 0.15, co2.get_left() + LEFT * 0.05, angle=-TAU / 5)
            self.play(Create(arr))
        sal = benzene([2.6, -0.4, 0], r=1.25, subs={0: ("OH", OC), 1: ("COOH", th.AMBER)}, label_size=30)
        sl = T("salicylic acid (after H⁺)", size=28, color=th.AMBER).next_to(sal, DOWN, buff=0.3)
        asp = chem(r"\xrightarrow{(CH_3CO)_2O} \text{aspirin (acetylsalicylic acid)}", size=42, color=th.MINT).to_edge(DOWN, buff=0.45)
        with self.say("Acidify, and you get salicylic acid, with the carboxylic acid group next to the O H. Acetylate it with ethanoic anhydride, and you have aspirin, one of the most used drugs in the world."):
            ka = Arrow([-1.9, -0.4, 0], [0.7, -0.4, 0], color=th.AMBER, buff=0)
            self.play(FadeOut(arr), FadeOut(co2), FadeOut(ortho), GrowArrow(ka))
            self.play(FadeIn(sal, shift=RIGHT * 0.4), FadeIn(sl))
            self.play(Write(asp))
        self.play(FadeOut(VGroup(title, ph, sal, sl, asp, ka)))
        title = T("Reimer–Tiemann: a carbene attacks", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        gen = chem(r"CHCl_3 + NaOH \rightarrow {:}CCl_2 + NaCl + H_2O", size=44, color=th.PINK).next_to(title, DOWN, buff=0.4)
        cb = VGroup(T("C", size=50, color=th.PINK, weight="BOLD"), T("Cl", size=28, color="#7BE495", weight="BOLD"), T("Cl", size=28, color="#7BE495", weight="BOLD"))
        cb[0].move_to([2.6, 0.0, 0])
        cb[1].move_to([3.5, 0.5, 0])
        cb[2].move_to([3.5, -0.5, 0])
        cbl = VGroup(Line(cb[0].get_center(), cb[1].get_center(), color=th.MUTED, stroke_width=4), Line(cb[0].get_center(), cb[2].get_center(), color=th.MUTED, stroke_width=4))
        lpc = VGroup(Dot([2.15, 0.12, 0], radius=0.05, color=th.AMBER), Dot([2.15, -0.12, 0], radius=0.05, color=th.AMBER))
        cl_lab = T("dichlorocarbene: neutral, only 6 electrons on C", size=22, color=th.PINK).next_to(cb, DOWN, buff=0.4)
        ph = benzene([-3.0, -0.6, 0], r=1.25, subs={0: ("O⁻", OC)}, label_size=30)
        with self.say("The Reimer Tiemann reaction. Warm phenol with chloroform and sodium hydroxide at sixty to seventy degrees. The alkali pulls hydrogen chloride out of chloroform, creating dichlorocarbene, a neutral carbon with only six electrons. It is electron hungry, a weak electrophile."):
            self.play(FadeIn(title), Write(gen))
            self.play(FadeIn(cb), Create(cbl), FadeIn(lpc), FadeIn(cl_lab))
        with self.say("Once again only the phenoxide ion is activated enough. The carbene attacks the ortho position, and after hydrolysis and acidification, the C C l two group becomes an aldehyde: salicylaldehyde, two hydroxybenzaldehyde. Use carbon tetrachloride instead, and you get salicylic acid."):
            self.play(Create(ph))
            arr = push(ph.verts[1] + RIGHT * 0.1, cb[0].get_left() + LEFT * 0.05, angle=-TAU / 6)
            self.play(Create(arr))
            prod = benzene([-3.0, -0.6, 0], r=1.25, subs={0: ("OH", OC), 1: ("CHO", th.PINK)}, label_size=30)
            self.play(FadeOut(VGroup(arr, cb, cbl, lpc, cl_lab)), Transform(ph, prod))
            pl = T("salicylaldehyde", size=34, color=th.PINK, weight="BOLD").next_to(ph, RIGHT, buff=1.2)
            self.play(FadeIn(pl))
        care = T("both Kolbe and Reimer–Tiemann need the PHENOXIDE: leave out the NaOH and nothing happens", size=24, color=th.AMBER).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(care))
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, gen, ph, pl, care)))
        with self.say("Three more spokes: the ester, salicylic acid, and salicylaldehyde."):
            g = self.rmap.show(self, ["naoh", "nh3", "zn", "azo"], ["ac", "kolbe", "rt"])
        self.play(FadeOut(g))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        title = T("–OH makes the ring very reactive at 2, 4, 6", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        r = benzene([-3.4, -0.3, 0], r=1.1, subs={0: ("OH", OC)})
        dots = VGroup(*[Dot(r.verts[k], radius=0.16, color=th.AMBER) for k in (1, 3, 5)])
        dl = VGroup(*[T(t, size=24, color=th.AMBER).next_to(r.verts[k], d, buff=0.25) for t, k, d in (("2", 1, RIGHT), ("4", 3, DOWN), ("6", 5, LEFT))])
        txt = para("The –OH lone pair feeds into the ring (the same resonance as before), piling electron density at ortho and para. Phenol reacts far faster than benzene, even without a catalyst.", width=6.0, size=26, color=th.BODY).move_to([2.8, -0.3, 0])
        with self.say("The same resonance that makes phenol acidic also makes its ring extremely reactive. The O H group feeds its lone pair into the ring, piling up electron density at the ortho and para positions, carbons two, four and six. Electrophiles attack there, far faster than with benzene."):
            self.play(FadeIn(title), Create(r))
            self.play(LaggedStart(*[GrowFromCenter(d_) for d_ in dots], lag_ratio=0.3), FadeIn(dl))
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(txt, dl)))
        bw = C.Beaker(center=[3.2, -0.8, 0], w=2.4, h=2.4, level=0.7, color="#C88A2A", opacity=0.55)
        bl = T("bromine water", size=22, color="#C88A2A").next_to(bw.g, DOWN, buff=0.15)
        rng = np.random.default_rng(3)
        ppt = VGroup(*[Dot(bw.c + np.array([rng.uniform(-1, 1), rng.uniform(-1.0, 0.3), 0]), radius=0.06, color=WHITE) for _ in range(40)])
        tri = benzene([-3.4, -0.3, 0], r=1.1, subs={0: ("OH", OC), 1: ("Br", "#C1543A"), 3: ("Br", "#C1543A"), 5: ("Br", "#C1543A")})
        eq = chem(r"C_6H_5OH + 3Br_2 \xrightarrow{\text{water}} C_6H_2Br_3OH\downarrow + 3HBr", size=36, color=th.LIME).to_edge(DOWN, buff=0.45)
        with self.say("Watch bromine water. Add phenol, and the orange colour vanishes at once, and a white precipitate forms: two four six tribromophenol. All three activated positions are brominated in one go, with no catalyst. In a non polar solvent like carbon disulphide at zero degrees, the reaction is gentler and gives mainly para bromophenol."):
            self.play(FadeIn(bw.g), FadeIn(bl))
            self.play(bw.liq.animate.set_fill("#E6E9F2", opacity=0.15), LaggedStart(*[FadeIn(p_, scale=0.3) for p_ in ppt], lag_ratio=0.02), Transform(r, tri), FadeOut(dots), run_time=2)
            self.play(Write(eq))
        self.play(FadeOut(VGroup(title, r, bw.g, bl, ppt, eq)))
        rows = [["Reaction", "Reagent", "Product"], ["nitration", "dilute HNO₃, 25 °C", "o- + p-nitrophenol"], ["nitration", "conc. HNO₃ + H₂SO₄", "picric acid (2,4,6-trinitro)"],
                ["sulphonation", "conc. H₂SO₄, 25 °C / 100 °C", "mainly o- / mainly p-"], ["bromination", "Br₂ in CS₂, 0 °C", "p-bromophenol"],
                ["bromination", "bromine water", "2,4,6-tribromophenol, white"], ["Friedel–Crafts", "CH₃Cl, AlCl₃", "o- and p-cresol"]]
        tb = C.table(rows, [3.0, 4.8, 4.8], row_h=0.62, size=24, colors=[th.AMBER, th.BODY, th.INK]).move_to(UP * 0.3)
        with self.say("The full set. Dilute nitric acid gives ortho and para nitrophenol. Concentrated nitric and sulphuric acids give picric acid. Sulphuric acid gives mainly the ortho sulphonic acid at room temperature, and mainly para at a hundred degrees. And Friedel Crafts methylation gives the cresols.") as v:
            for r_ in tb:
                self.play(FadeIn(r_, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))
        title = T("Separating o- and p-nitrophenol by steam distillation", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        o_ = benzene([-3.4, -0.3, 0], r=0.9, subs={0: ("OH", OC), 1: ("NO₂", "#5C8DFF")}, label_size=24)
        hb = DashedLine(o_[3].get_center() + RIGHT * 0.25, o_[5].get_center() + UP * 0.1 + LEFT * 0.2, color=th.SKY, stroke_width=4)
        ol = VGroup(T("ortho: INTRAmolecular H-bond", size=24, color=th.SKY, weight="BOLD"), T("no free O–H: volatile, distils with steam", size=22, color=th.BODY)).arrange(DOWN, buff=0.06).next_to(o_, DOWN, buff=0.5)
        ps = VGroup(*[benzene(r=0.62, subs={0: ("OH", OC), 3: ("NO₂", "#5C8DFF")}, label_size=20) for _ in range(2)]).arrange(DOWN, buff=0.35).move_to([3.4, -0.2, 0])
        hb2 = DashedLine(ps[0][-1].get_center() + DOWN * 0.15, ps[1][3].get_center() + UP * 0.15, color=th.SKY, stroke_width=4)
        pl = VGroup(T("para: INTERmolecular H-bonds", size=24, color=th.SKY, weight="BOLD"), T("molecules associate: stays behind", size=22, color=th.BODY)).arrange(DOWN, buff=0.06).next_to(ps, DOWN, buff=0.3)
        with self.say("The two nitrophenols are separated by steam distillation. In the ortho isomer, the O H and nitro groups are close enough to hydrogen bond to each other, inside one molecule. With no free O H to bond to its neighbours, it is volatile and distils over with steam. In the para isomer the groups are too far apart, so it hydrogen bonds to other molecules, associates, and stays behind."):
            self.play(FadeIn(title), Create(o_))
            self.play(Create(hb), FadeIn(ol))
            self.play(FadeIn(ps))
            self.play(Create(hb2), FadeIn(pl))
        self.play(FadeOut(VGroup(title, o_, hb, ol, ps, hb2, pl)))
        head, prob = C.example_head(self, "0.94 g of phenol is shaken with excess bromine water. Find (a) the mass of 2,4,6-tribromophenol, (b) the mass of Br₂ used. (C 12, H 1, O 16, Br 79.9)")
        st = C.steps(r"n(\text{phenol}) = \tfrac{0.94}{94} = 0.010\ \mathrm{mol}",
                     r"M(\mathrm{C_6H_2Br_3OH}) = 72 + 3 + 239.7 + 16 = 330.7",
                     r"(a)\ 0.010 \times 330.7 = 3.31\ \mathrm{g}",
                     r"(b)\ 3 \times 0.010 = 0.030\ \mathrm{mol\ Br_2} \times 159.8 = 4.79\ \mathrm{g}", size=40).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example eleven point three. Zero point nine four grams of phenol is zero point zero one mole. Tribromophenol has molar mass three thirty point seven, so three point three one grams. And three bromine molecules per phenol: zero point zero three moles, four point seven nine grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        with self.say("Two more spokes: tribromophenol and picric acid."):
            g = self.rmap.show(self, ["naoh", "nh3", "zn", "azo", "ac", "kolbe", "rt"], ["br", "nit"])
        self.play(FadeOut(g))

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        title = T("Tests for phenol", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        t1 = C.Beaker(center=[-4.0, -0.3, 0], w=2.0, h=2.0, level=0.7, color="#D9A03A", opacity=0.4)
        t2 = C.Beaker(center=[0.0, -0.3, 0], w=2.0, h=2.0, level=0.7, color="#C88A2A", opacity=0.55)
        t3 = C.Beaker(center=[4.0, -0.3, 0], w=2.0, h=2.0, level=0.7, color="#3A8F7A", opacity=0.5)
        l1 = VGroup(T("neutral FeCl₃", size=24, color=th.AMBER, weight="BOLD"), T("violet colour", size=22, color=VIOLET)).arrange(DOWN, buff=0.06).next_to(t1.g, DOWN, buff=0.2)
        l2 = VGroup(T("bromine water", size=24, color=th.AMBER, weight="BOLD"), T("white precipitate", size=22, color=th.BODY)).arrange(DOWN, buff=0.06).next_to(t2.g, DOWN, buff=0.2)
        l3 = VGroup(T("Liebermann test", size=24, color=th.AMBER, weight="BOLD"), T("blue-green → red → blue-green", size=22, color=th.BODY)).arrange(DOWN, buff=0.06).next_to(t3.g, DOWN, buff=0.2)
        rng = np.random.default_rng(8)
        ppt = VGroup(*[Dot(t2.c + np.array([rng.uniform(-0.8, 0.8), rng.uniform(-0.85, 0.2), 0]), radius=0.05, color=WHITE) for _ in range(28)])
        with self.say("Three tests for phenol. Neutral iron three chloride gives a violet colour, from a complex of iron with phenoxide groups. Ethanol gives none. Bromine water is decolourised, with a white precipitate of tribromophenol. And Liebermann's nitroso test: warm with sodium nitrite and concentrated sulphuric acid, and the solution turns deep blue green, red on dilution, and blue green again with excess alkali."):
            self.play(FadeIn(title), FadeIn(VGroup(t1.g, t2.g, t3.g)))
            self.play(t1.liq.animate.set_fill(VIOLET, opacity=0.85), FadeIn(l1), run_time=1.2)
            self.play(t2.liq.animate.set_fill("#E6E9F2", opacity=0.15), FadeIn(ppt), FadeIn(l2), run_time=1.2)
            self.play(t3.liq.animate.set_fill("#D8252A", opacity=0.7), FadeIn(l3), run_time=1.0)
            self.play(t3.liq.animate.set_fill("#3A8F7A", opacity=0.6), run_time=1.0)
        fe = chem(r"6C_6H_5OH + FeCl_3 \rightarrow [Fe(OC_6H_5)_6]^{3-} + 3Cl^- + 6H^+", size=30, color=VIOLET).to_edge(DOWN, buff=0.35)
        nb = C.show_neby(self, "think", height=1.2, corner=UR, buff=0.9)
        with self.say("Why must the ferric chloride be neutral? Ordinary ferric chloride solution is acidic, and acid suppresses phenol's ionisation, so the violet complex never forms."):
            self.play(Write(fe))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, t1.g, t2.g, t3.g, l1, l2, l3, ppt, fe)))
        cards = VGroup(*[C.card(self, a, b, w=4.0, h=2.2, color=c, tsize=26, bsize=21) for a, b, c in [
            ("Bakelite", "phenol + methanal: the first synthetic plastic", th.AMBER), ("Antiseptics", "carbolic soap; cresols in Lysol and creosote", OC),
            ("Drugs", "salicylic acid → aspirin; paracetamol; oil of wintergreen", th.MINT), ("Dyes", "azo dyes by coupling; picric acid", "#F08A24"),
            ("Indicator", "phenolphthalein for titrations", th.PINK), ("Polymers", "nylon-6,6 (via cyclohexanol), epoxy resins", th.SKY)]]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(UP * 0.2)
        with self.say("Phenol's uses are everywhere: bakelite, the first plastic, made with methanal; antiseptics like carbolic soap and creosote for electric poles; drugs from aspirin to paracetamol; azo dyes and picric acid; phenolphthalein; and nylon and epoxy resins.") as v:
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 6 - 0.45)
        self.play(FadeOut(cards))
        with self.say("Here is the complete reaction map of phenol. Notice how many reactions use the phenoxide ion, and how many attack the ortho and para positions. Two ideas, resonance and ring activation, explain nearly all of it."):
            g = self.rmap.show(self, [e[0] for e in MAP], [])
            self.play(Indicate(g[1], color=th.AMBER, scale_factor=1.1))
        self.play(FadeOut(g))
        head, prob = C.example_head(self, "P, C₇H₈O, is insoluble in water and NaHCO₃ but dissolves in NaOH. It gives violet with FeCl₃ and a white ppt with bromine water. With CHCl₃ + NaOH it gives an aldehyde Q. Identify P and Q.")
        st = VGroup(T("dissolves in NaOH, not NaHCO₃ → a phenol, not a carboxylic acid", size=26, color=th.SKY), T("violet FeCl₃ + white Br₂ ppt → phenolic –OH on the ring", size=26, color=th.SKY),
                    T("C₇H₈O = CH₃C₆H₄OH, a cresol: P = 4-methylphenol (p-cresol)", size=26, color=th.AMBER), T("Reimer–Tiemann puts –CHO ortho to –OH:", size=26, color=th.BODY),
                    T("Q = 2-hydroxy-5-methylbenzaldehyde, C₈H₈O₂ (M = 136)", size=26, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example eleven point four. Soluble in sodium hydroxide but not bicarbonate: a phenol, not a carboxylic acid. Violet with ferric chloride and a white precipitate with bromine confirm it. C seven H eight O is a cresol, and the standard answer is para cresol, with both ortho positions free. Reimer Tiemann puts a C H O group ortho to the O H, giving two hydroxy five methyl benzaldehyde."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(head, prob, st)))
        self.tip("Phenol vs ethanol vs carboxylic acid: NaOH dissolves phenol (not ethanol); NaHCO₃ fizzes only with the carboxylic acid; neutral FeCl₃ is violet only with phenol.",
                 "To tell them apart in one line each: sodium hydroxide dissolves phenol but not ethanol. Sodium bicarbonate fizzes only with a carboxylic acid. And neutral ferric chloride turns violet only with phenol.", state="wink")
        self.quiz("Phenol + CHCl₃ + aqueous NaOH (60–70 °C), then acid, gives",
                  ["salicylic acid", "salicylaldehyde", "picric acid", "phenyl ethanoate"], 1,
                  "Last one. Phenol warmed with chloroform and sodium hydroxide, then acidified. What forms? Pause and think.",
                  "B, salicylaldehyde. This is the Reimer Tiemann reaction: dichlorocarbene attacks the ortho position and becomes an aldehyde group. Salicylic acid comes from Kolbe's reaction with carbon dioxide, or from carbon tetrachloride in place of chloroform.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Phenol: –OH on the ring; benzyl alcohol is not a phenol.",
            "Made by Dow process, warming a diazonium salt, or alkali fusion; then acidify.",
            "Acidic (pKa 10): phenoxide charge spread to o and p by resonance.",
            "NaOH dissolves phenol; NaHCO₃ does not (weaker than H₂CO₃).",
            "Coupling → orange azo dye; phthalic anhydride → phenolphthalein.",
            "Kolbe (CO₂) → salicylic acid → aspirin; Reimer–Tiemann (CHCl₃) → salicylaldehyde.",
            "Br₂ water → white 2,4,6-tribromophenol; conc. HNO₃ → picric acid.",
            "Tests: violet with neutral FeCl₃; Liebermann nitroso test.",
        ], "Let us recap. A phenol has its O H on the ring. It is made by the Dow process, from a diazonium salt, or by alkali fusion, with a final acidification. It is acidic because the phenoxide ion's charge spreads over the ring, so it dissolves in sodium hydroxide, though not in bicarbonate. It couples to make azo dyes, gives phenolphthalein, aspirin by way of Kolbe's reaction, and salicylaldehyde by Reimer Tiemann. Its activated ring is brominated and nitrated at two, four and six. And neutral ferric chloride turns it violet.")
        self.outro("That is phenols. Next, we join two carbon groups through an oxygen, and meet the ethers, including the famous anaesthetic, diethyl ether. See you in the next lesson on NEBians.")
