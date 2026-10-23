import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

CLC = "#7BE495"
NO2C = "#5C8DFF"


def ring(center=ORIGIN, r=0.9, subs=None, color=th.INK, label_size=28):
    """Benzene ring (hexagon + inner circle). subs: {vertex index 0..5 (0 = top, clockwise): (text, colour)}."""
    c = np.array(center, dtype=float)
    verts = [c + r * np.array([np.sin(k * PI / 3), np.cos(k * PI / 3), 0]) for k in range(6)]
    g = VGroup(Polygon(*verts, stroke_color=color, stroke_width=4, fill_opacity=0), Circle(radius=r * 0.58, stroke_color=color, stroke_width=3).move_to(c))
    for k, (txt, col) in (subs or {}).items():
        d = (verts[k] - c) / r
        end = verts[k] + d * 0.45 * r / 0.9
        g.add(Line(verts[k], end, color=th.MUTED, stroke_width=4))
        lab = T(txt, size=label_size, color=col, weight="BOLD")
        lab.next_to(end, d, buff=0.06)
        g.add(lab)
    return g


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 9
    TITLE = "Haloarenes"
    SUBTITLE = "A halogen on a benzene ring"
    SECTIONS = ["Naming and isomerism", "Preparing chlorobenzene", "Physical properties", "Low reactivity",
                "Reduction and electrophilic substitution", "Fittig, Wurtz–Fittig, chloral", "Uses"]
    NEXT = "Unit 10 · Alcohols"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        f1 = C.Flask(center=[-3.4, -0.9, 0], scale=1.3, color=th.SKY, opacity=0.35)
        f2 = C.Flask(center=[3.4, -0.9, 0], scale=1.3, color=th.SKY, opacity=0.35)
        l1 = VGroup(chem(r"CH_3CH_2Cl", size=36, color=th.AMBER), T("+ KOH(aq), warm", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(f1.g, UP, buff=0.3)
        l2 = VGroup(chem(r"C_6H_5Cl", size=36, color=CLC), T("+ KOH(aq), boil", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(f2.g, UP, buff=0.3)
        tt = ValueTracker(0)
        c1 = DecimalNumber(0, num_decimal_places=0, font_size=48, color=th.AMBER, unit=r"\text{ min}")
        c1.add_updater(lambda m: m.set_value(min(tt.get_value(), 5)).next_to(f1.g, DOWN, buff=0.3))
        c2 = DecimalNumber(0, num_decimal_places=1, font_size=48, color=CLC, unit=r"\text{ h}")
        c2.add_updater(lambda m: m.set_value(tt.get_value() / 10).next_to(f2.g, DOWN, buff=0.3))
        with self.say("Two flasks, two chlorides, the same reagent. On the left, chloroethane with warm aqueous potassium hydroxide. On the right, chlorobenzene, a chlorine on a benzene ring, boiled with the same alkali."):
            self.play(FadeIn(f1.g), FadeIn(f2.g), FadeIn(l1), FadeIn(l2))
            self.add(c1, c2)
            self.play(FadeIn(c1), FadeIn(c2))
        done = T("ethanol formed ✓", size=26, color=th.MINT, weight="BOLD").next_to(c1, DOWN, buff=0.15)
        none = T("nothing happens ✗", size=26, color=th.CORAL, weight="BOLD").next_to(c2, DOWN, buff=0.15)
        with self.say("Within a few minutes, the chloroethane has become ethanol. The chlorobenzene? Boil it for hours, and nothing happens at all. Its rate is something like a hundred thousand times slower."):
            self.play(tt.animate.set_value(5), f1.liq.animate.set_fill(th.MINT, opacity=0.4), run_time=2.5, rate_func=linear)
            self.play(FadeIn(done))
            self.play(tt.animate.set_value(60), run_time=3.0, rate_func=linear)
            self.play(FadeIn(none))
        nb = C.show_neby(self, "surprised", height=1.5, at=[0, 1.6, 0])
        with self.say("Same carbon chlorine bond, the same nucleophile. Why does putting chlorine on a ring make it so stubborn? There are four reasons, and you will be able to give all four by the middle of this lesson."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        c1.clear_updaters()
        c2.clear_updaters()
        self.play(FadeOut(VGroup(f1.g, f2.g, l1, l2, c1, c2, done, none)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 9: Haloarenes. Compounds with a halogen fixed directly to a benzene ring, how they are made, why they resist substitution, and what they are used for, from dyes to the insecticide D D T."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. Naming and isomerism. Making chlorobenzene from benzene and from a diazonium salt. Physical properties. The low reactivity, and its four reasons. Reduction and electrophilic substitution. The Fittig and Wurtz Fittig reactions and D D T. And finally, uses.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        a = ring([-3.3, 0.3, 0], subs={0: ("Cl", CLC)})
        b = ring([3.3, 0.0, 0], subs={0: ("CH₂Cl", th.AMBER)})
        la = VGroup(T("haloarene (aryl halide)", size=28, color=CLC, weight="BOLD"), T("Cl on a ring carbon, sp²", size=22, color=th.BODY), T("very unreactive to nucleophiles", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(a, DOWN, buff=0.4)
        lb = VGroup(T("aralkyl halide (benzyl chloride)", size=28, color=th.AMBER, weight="BOLD"), T("Cl on the side chain, sp³", size=22, color=th.BODY), T("reacts like a haloalkane: very reactive", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(b, DOWN, buff=0.4)
        with self.say("Two families of organic halogen compounds contain a benzene ring. In a haloarene, or aryl halide, the halogen sits directly on a ring carbon, like chlorobenzene. In an aralkyl halide, like benzyl chloride, it sits on the side chain. The two behave completely differently."):
            self.play(Create(a), FadeIn(la))
            self.play(Create(b), FadeIn(lb))
        care = T("benzyl chloride gives an instant white ppt with alcoholic AgNO₃; chlorobenzene does not", size=22, color=th.AMBER).to_edge(DOWN, buff=0.45)
        with self.say("Benzyl chloride is not a haloarene. It reacts like any haloalkane, and gives an instant white precipitate with alcoholic silver nitrate. Chlorobenzene gives none."):
            self.play(FadeIn(care))
        self.play(FadeOut(VGroup(a, b, la, lb, care)))
        rows = [["Structure", "IUPAC name", "Common name"], ["C₆H₅Cl", "chlorobenzene", "phenyl chloride"], ["1,2-C₆H₄Cl₂", "1,2-dichlorobenzene", "o-dichlorobenzene"],
                ["1,4-C₆H₄Cl₂", "1,4-dichlorobenzene", "p-dichlorobenzene"], ["4-CH₃C₆H₄Cl", "1-chloro-4-methylbenzene", "p-chlorotoluene"], ["4-O₂NC₆H₄Cl", "1-chloro-4-nitrobenzene", "p-nitrochlorobenzene"]]
        tb = C.table(rows, [3.4, 4.8, 4.0], row_h=0.64, size=25, colors=[th.AMBER, th.INK, th.BODY]).move_to(UP * 0.4)
        with self.say("Naming is simple: number the ring for the lowest locants, and use the halogen as a prefix. For two substituents the old prefixes still work: ortho for one two, meta for one three, and para for one four.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))
        title = T("C₆H₄Cl₂: three isomers", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        iso = VGroup(ring(subs={0: ("Cl", CLC), 1: ("Cl", CLC)}), ring(subs={0: ("Cl", CLC), 2: ("Cl", CLC)}), ring(subs={0: ("Cl", CLC), 3: ("Cl", CLC)})).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        info = [("1,2 · ortho", "m.p. −17 °C"), ("1,3 · meta", "m.p. −25 °C"), ("1,4 · para", "m.p. +53 °C")]
        labs = VGroup(*[VGroup(T(a_, size=26, color=th.INK, weight="BOLD"), T(b_, size=24, color=th.AMBER if k == 2 else th.BODY)).arrange(DOWN, buff=0.08).next_to(iso[k], DOWN, buff=0.45) for k, (a_, b_) in enumerate(info)])
        why = T("para is symmetrical and packs tightly in the crystal: much higher melting point", size=24, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("Chlorobenzene has no positional isomer, since all six ring carbons are equivalent. Isomerism starts with a second substituent: dichlorobenzene has exactly three, ortho, meta and para. Their boiling points are close, but para melts at plus fifty three degrees while the others melt far below zero. Its symmetrical shape stacks neatly in the crystal, so more energy is needed to break the lattice."):
            self.play(FadeIn(title))
            for k in range(3):
                self.play(Create(iso[k]), FadeIn(labs[k]), run_time=0.8)
            self.play(Indicate(VGroup(iso[2], labs[2]), color=th.AMBER, scale_factor=1.05), FadeIn(why))
        self.play(FadeOut(VGroup(title, iso, labs, why)))
        cnt = VGroup(
            VGroup(chem(r"C_6H_5Cl", size=44), T("1 compound: all six ring carbons are equivalent", size=26, color=th.BODY)).arrange(RIGHT, buff=0.5),
            VGroup(chem(r"C_6H_4ClBr", size=40), T("3 isomers: o, m, p", size=24, color=th.BODY)).arrange(RIGHT, buff=0.5),
            VGroup(chem(r"C_6H_3Cl_3", size=40), T("3 isomers: 1,2,3-, 1,2,4- and 1,3,5-", size=24, color=th.BODY)).arrange(RIGHT, buff=0.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        trio = VGroup(ring(r=0.72, subs={0: ("Cl", CLC), 1: ("Cl", CLC), 2: ("Cl", CLC)}, label_size=22), ring(r=0.72, subs={0: ("Cl", CLC), 1: ("Cl", CLC), 3: ("Cl", CLC)}, label_size=22),
                      ring(r=0.72, subs={0: ("Cl", CLC), 2: ("Cl", CLC), 4: ("Cl", CLC)}, label_size=22)).arrange(RIGHT, buff=1.4).to_edge(DOWN, buff=0.55)
        cnt.next_to(trio, UP, buff=0.5)
        with self.say("Counting isomers is a quick exam point. Chlorobenzene itself has only one form. Swap one chlorine for bromine, and C six H four C l B r again has three isomers, ortho, meta and para. With three identical chlorines there are also three: one two three, one two four, and the symmetrical one three five."):
            for c_ in cnt:
                self.play(FadeIn(c_, shift=RIGHT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[Create(t_) for t_ in trio], lag_ratio=0.3), run_time=2)
        self.play(FadeOut(VGroup(cnt, trio)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("From benzene: in the dark, with a catalyst", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        b0 = ring([-4.0, 0.2, 0])
        b1 = ring([2.6, 0.2, 0], subs={0: ("Cl", CLC)})
        arr = Arrow([-2.6, 0.2, 0], [1.0, 0.2, 0], buff=0, color=th.AMBER, stroke_width=6)
        al = VGroup(chem(r"+\,Cl_2", size=34), T("anhydrous AlCl₃, dark", size=22, color=th.AMBER)).arrange(DOWN, buff=0.1).next_to(arr, UP, buff=0.15)
        e = chem(r"C_6H_6 + Cl_2 \xrightarrow{AlCl_3,\ \text{dark}} C_6H_5Cl + HCl", size=38).to_edge(DOWN, buff=1.6)
        ep = chem(r"AlCl_3 + Cl_2 \rightarrow AlCl_4^- + Cl^+\ \ (\text{the electrophile})", size=32, color=th.SKY).next_to(e, DOWN, buff=0.3)
        with self.say("Chlorobenzene can be made directly from benzene and chlorine, in the dark, with a Lewis acid halogen carrier such as anhydrous aluminium chloride, iron three chloride, or iron filings. The catalyst creates the real attacker, a chlorine cation, which substitutes on the ring."):
            self.play(FadeIn(title), Create(b0))
            self.play(GrowArrow(arr), FadeIn(al))
            self.play(Create(b1), Write(e))
            self.play(Write(ep))
        uv = T("in UV light without catalyst, Cl₂ ADDS instead: C₆H₆ + 3Cl₂ → C₆H₆Cl₆", size=24, color=th.CORAL).next_to(title, DOWN, buff=0.3)
        with self.say("Why in the dark? In ultraviolet light and without a catalyst, chlorine adds to the ring instead, giving benzene hexachloride. Industrially, the Raschig process passes benzene, hydrogen chloride and air over copper chloride at about five hundred kelvin."):
            self.play(FadeIn(uv))
        self.play(FadeOut(VGroup(title, b0, b1, arr, al, e, ep, uv)))
        title = T("From the diazonium salt: precise and clean", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        an = ring([-4.6, 0.9, 0], r=0.75, subs={0: ("NH₂", th.SKY)}, label_size=24)
        dz = ring([-0.6, 0.9, 0], r=0.75, subs={0: ("N₂⁺Cl⁻", th.PINK)}, label_size=24)
        cb = ring([3.6, 0.9, 0], r=0.75, subs={0: ("Cl", CLC)}, label_size=24)
        a1 = Arrow([-3.6, 0.9, 0], [-1.6, 0.9, 0], buff=0, color=th.MUTED, stroke_width=5)
        a2 = Arrow([0.4, 0.9, 0], [2.6, 0.9, 0], buff=0, color=th.MUTED, stroke_width=5)
        t1 = VGroup(T("NaNO₂ + HCl", size=20, color=th.AMBER), T("273–278 K", size=20, color=th.AMBER)).arrange(DOWN, buff=0.05).next_to(a1, DOWN, buff=0.15)
        t2 = VGroup(T("CuCl / HCl", size=20, color=th.AMBER), T("− N₂↑", size=20, color=th.AMBER)).arrange(DOWN, buff=0.05).next_to(a2, DOWN, buff=0.15)
        with self.say("Direct chlorination cannot be stopped cleanly at one chlorine, and cannot put it at a chosen position. The diazonium route can. Aniline is diazotised with sodium nitrite and hydrochloric acid in ice, at two seventy three to two seventy eight kelvin, giving benzene diazonium chloride. Then the diazonium group is swapped for chlorine, and nitrogen gas bubbles off."):
            self.play(FadeIn(title), Create(an))
            self.play(GrowArrow(a1), FadeIn(t1), Create(dz))
            self.play(GrowArrow(a2), FadeIn(t2), Create(cb))
            bub = VGroup(*[Circle(radius=0.08, stroke_color=WHITE, stroke_width=2).move_to([1.5 + 0.15 * k, 0.9, 0]) for k in range(3)])
            self.play(bub.animate.shift(UP * 1.2).set_opacity(0), run_time=1.0)
        rows = [["Method", "Reagent", "Product"], ["Sandmeyer", "CuCl in conc. HCl, warm", "C₆H₅Cl + N₂"], ["Gattermann", "Cu powder + conc. HCl", "C₆H₅Cl + N₂"],
                ["(iodo)", "KI, warm: no catalyst", "C₆H₅I + N₂"], ["Balz–Schiemann", "HBF₄, then heat the dry salt", "C₆H₅F + N₂ + BF₃"]]
        tb = C.table(rows, [3.0, 5.2, 3.8], row_h=0.6, size=23, colors=[th.AMBER, th.BODY, CLC]).to_edge(DOWN, buff=0.45)
        with self.say("Two named methods give chlorobenzene. The Sandmeyer reaction uses copper one chloride in hydrochloric acid. The Gattermann reaction uses copper powder with hydrochloric acid. Iodobenzene needs no catalyst: just warm the diazonium salt with potassium iodide. And fluorobenzene comes from the Balz Schiemann reaction, heating the dry fluoroborate salt.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(title, an, dz, cb, a1, a2, t1, t2, tb, bub)))
        head, prob = C.example_head(self, "39.0 g of benzene is treated with excess Cl₂ over anhydrous AlCl₃ in the dark. If the yield is 80 %, what mass of chlorobenzene is obtained?")
        st = C.steps(r"n(\mathrm{C_6H_6}) = \tfrac{39.0}{78} = 0.500\ \mathrm{mol} \Rightarrow 0.500\ \mathrm{mol\ C_6H_5Cl}\ (1:1)",
                     r"M(\mathrm{C_6H_5Cl}) = 72 + 5 + 35.5 = 112.5;\ \ 0.500 \times 112.5 = 56.25\ \mathrm{g}",
                     r"80\,\%:\ 0.80 \times 56.25 = 45.0\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example. Benzene has molar mass seventy eight, so thirty nine grams is half a mole, giving half a mole of chlorobenzene in theory. Chlorobenzene's molar mass is one twelve point five, so fifty six point two five grams. At eighty percent yield, forty five grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "9.30 g of aniline is diazotised completely and decomposed by the Sandmeyer reaction at 75 % efficiency. Find (i) the volume of N₂ at STP, (ii) the mass of chlorobenzene.")
        st = C.steps(r"n(\mathrm{C_6H_5NH_2}) = \tfrac{9.30}{93} = 0.100\ \mathrm{mol}",
                     r"(i)\ 0.100\ \mathrm{mol\ N_2} \times 22.4 = 2.24\ \mathrm{L}",
                     r"(ii)\ 0.100 \times 112.5 = 11.25\ \mathrm{g};\ \ 75\,\%:\ 8.44\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("A second example. Aniline has molar mass ninety three, so nine point three grams is zero point one mole. Each mole gives one mole of nitrogen gas, two point two four litres at S T P. And eleven point two five grams of chlorobenzene in theory, or eight point four four grams at seventy five percent."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("Iodobenzene is best made from benzene diazonium chloride by warming it with",
                  ["CuCl / HCl", "Cu powder / HCl", "KI solution", "HBF₄, then heat"], 2,
                  "Quick check. Which reagent turns benzene diazonium chloride into iodobenzene? Pause and think.",
                  "C, potassium iodide. Iodide is a good enough nucleophile that no copper catalyst is needed. Copper one chloride is the Sandmeyer route to chlorobenzene, and fluoroboric acid is the Balz Schiemann route to fluorobenzene.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        rows = [["", "C₆H₅Cl", "C₆H₅Br", "C₆H₅I"], ["b.p. / °C", "132", "156", "188"], ["density / g cm⁻³", "1.11", "1.49", "1.83"], ["dipole / D", "1.69", "1.70", "1.70"]]
        tb = C.table(rows, [3.4, 2.4, 2.4, 2.4], row_h=0.7, size=28, colors=[th.MUTED, CLC, "#C1543A", th.PINK]).move_to(UP * 1.0)
        notes = VGroup(T("all denser than water, insoluble in it, soluble in organic solvents", size=24, color=th.BODY), T("b.p. rises Cl → Br → I: bigger, more polarisable", size=24, color=th.BODY),
                       T("colourless, sweet-smelling, poisonous, steam-volatile", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tb, DOWN, buff=0.45)
        with self.say("Chloro, bromo and iodobenzene are colourless, sweet smelling, poisonous liquids. All are denser than water and insoluble in it, but dissolve in organic solvents. Boiling points rise from chloro to iodo, as the molecule gets bigger and more polarisable. They are steam volatile, which is how chlorobenzene is separated in the laboratory.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(n_, shift=RIGHT * 0.2) for n_ in notes], lag_ratio=0.4))
        self.play(FadeOut(VGroup(tb, notes)))
        b1 = Rectangle(width=1.86 * 3.2, height=0.6, fill_color=th.AMBER, fill_opacity=0.85, stroke_width=0).move_to([-3.0, 0.8, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=1.69 * 3.2, height=0.6, fill_color=CLC, fill_opacity=0.85, stroke_width=0).move_to([-3.0, -0.2, 0], aligned_edge=LEFT)
        l1 = VGroup(chem(r"CH_3Cl", size=40).next_to(b1, LEFT, buff=0.2), T("1.86 D", size=24, color=th.INK).next_to(b1, RIGHT, buff=0.15))
        l2 = VGroup(chem(r"C_6H_5Cl", size=40).next_to(b2, LEFT, buff=0.2), T("1.69 D", size=24, color=th.INK).next_to(b2, RIGHT, buff=0.15))
        why = para("Why is chlorobenzene less polar? Chlorine's lone pair leaks into the ring, opposing the inductive pull, and the sp² carbon holds its electrons more tightly.", width=11, size=26, color=th.BODY).to_edge(DOWN, buff=0.6)
        with self.say("Notice the dipole moment. Chlorobenzene, one point six nine debye, is less polar than chloromethane, one point eight six. Chlorine's lone pair partly flows back into the ring, opposing the pull of its electronegativity, and the s p two carbon holds its electrons more tightly. Both ideas matter in the next part."):
            self.play(GrowFromEdge(b1, LEFT), FadeIn(l1))
            self.play(GrowFromEdge(b2, LEFT), FadeIn(l2))
            self.play(FadeIn(why))
        self.play(FadeOut(VGroup(b1, b2, l1, l2, why)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        title = T("Why chlorobenzene resists nucleophiles", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        self.play(FadeIn(title))
        # reason 1: resonance
        r1h = T("1. Resonance: partial double bond C=Cl", size=28, color=th.AMBER, weight="BOLD").next_to(title, DOWN, buff=0.3)
        rs = VGroup(ring(r=1.0, subs={0: ("Cl", CLC)}, label_size=30), ring(r=1.0, subs={0: ("Cl⁺", CLC)}, label_size=30), ring(r=1.0, subs={0: ("Cl⁺", CLC)}, label_size=30)).arrange(RIGHT, buff=1.5).move_to(DOWN * 0.3)
        rs[1][1].set_opacity(0)
        rs[2][1].set_opacity(0)
        minus = VGroup(T("−", size=48, color=th.CORAL, weight="BOLD").next_to(rs[1][0].get_vertices()[1], RIGHT, buff=0.08),
                       T("−", size=48, color=th.CORAL, weight="BOLD").next_to(rs[2][0].get_vertices()[3], DOWN, buff=0.08))
        arrs = VGroup(*[M(r"\leftrightarrow", size=48).move_to((rs[k].get_right() + rs[k + 1].get_left()) / 2) for k in range(2)])
        bl = VGroup(T("C–Cl in CH₃Cl: 177 pm", size=24, color=th.BODY), T("C–Cl in C₆H₅Cl: 169 pm, shorter and stronger", size=24, color=th.AMBER)).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.55)
        with self.say("Reason one, resonance. A lone pair on chlorine overlaps with the ring's pi system and spreads into it, putting negative charge on the ortho and para carbons. So the carbon chlorine bond gains partial double bond character. It shrinks from one seventy seven picometres in chloromethane to one sixty nine in chlorobenzene, and becomes much harder to break."):
            self.play(FadeIn(r1h), Create(rs[0]))
            self.play(FadeIn(arrs), Create(rs[1]), Create(rs[2]), FadeIn(minus))
            self.play(FadeIn(bl))
        self.play(FadeOut(VGroup(r1h, rs, minus, arrs, bl)))
        r2h = T("2. The carbon is sp²: shorter, less polar C–Cl", size=28, color=th.AMBER, weight="BOLD").next_to(title, DOWN, buff=0.3)
        bars = VGroup(*[VGroup(T(a, size=26, color=th.INK), Rectangle(width=w * 10, height=0.5, fill_color=c, fill_opacity=0.85, stroke_width=0), T(t_, size=22, color=th.BODY)).arrange(RIGHT, buff=0.3)
                        for a, w, c, t_ in [("sp³ (CH₃Cl)", 0.25, th.SKY, "25 % s-character"), ("sp² (C₆H₅Cl)", 0.33, CLC, "33 % s-character")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.2)
        n2 = T("more s-character → more electronegative carbon → smaller δ⁺ for a nucleophile to find", size=22, color=th.BODY).to_edge(DOWN, buff=0.6)
        with self.say("Reason two. The carbon holding chlorine is s p two, with thirty three percent s character, compared with twenty five in chloromethane. It is more electronegative, so the bond is shorter, stronger and less polar. The partial positive charge that a nucleophile looks for is smaller."):
            self.play(FadeIn(r2h))
            for b in bars:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]), run_time=0.7)
            self.play(FadeIn(n2))
        self.play(FadeOut(VGroup(r2h, bars, n2)))
        r3h = T("3. The π cloud repels the nucleophile", size=28, color=th.AMBER, weight="BOLD").next_to(title, DOWN, buff=0.3)
        flat = Line([-3.0, -0.6, 0], [3.0, -0.6, 0], color=th.INK, stroke_width=6)
        cloud = VGroup(Ellipse(width=6.4, height=0.9, fill_color=th.SKY, fill_opacity=0.3, stroke_width=0).move_to([0, -0.1, 0]),
                       Ellipse(width=6.4, height=0.9, fill_color=th.SKY, fill_opacity=0.3, stroke_width=0).move_to([0, -1.1, 0]))
        clb = T("π electron cloud", size=22, color=th.SKY).next_to(cloud, RIGHT, buff=0.2)
        nu = VGroup(Circle(radius=0.35, fill_color=th.CORAL, fill_opacity=1, stroke_width=0), T("OH⁻", size=20, color=WHITE, weight="BOLD")).move_to([0, 2.0, 0])
        with self.say("Reason three. The ring is wrapped in a thick sandwich of pi electrons above and below. An approaching nucleophile is itself electron rich, so it is repelled before it can reach the carbon."):
            self.play(FadeIn(r3h), Create(flat), FadeIn(cloud), FadeIn(clb), FadeIn(nu))
            self.play(nu.animate.shift(DOWN * 1.4), run_time=0.8, rate_func=rate_functions.ease_out_quad)
            self.play(nu.animate.shift(UP * 1.0), run_time=0.6, rate_func=rate_functions.ease_out_back)
        self.play(FadeOut(VGroup(r3h, flat, cloud, clb, nu)))
        r4h = T("4. Neither SN1 nor SN2 is possible", size=28, color=th.AMBER, weight="BOLD").next_to(title, DOWN, buff=0.3)
        c1 = C.card(self, "SN1 blocked", "needs a phenyl cation, C₆H₅⁺. Its empty orbital lies in the ring plane, so it gets no resonance help: far too unstable.", w=5.6, h=2.6, color=th.CORAL, bsize=22)
        c2 = C.card(self, "SN2 blocked", "needs attack from directly behind the C–Cl bond. That space is filled by the ring itself: physically impossible.", w=5.6, h=2.6, color=th.SKY, bsize=22)
        VGroup(c1, c2).arrange(RIGHT, buff=0.4).move_to(DOWN * 0.4)
        with self.say("Reason four. Neither mechanism is available. S N one would need a phenyl cation, whose empty orbital lies in the plane of the ring and gets no resonance help, so it is far too unstable. S N two needs attack from directly behind the carbon chlorine bond, and that space is occupied by the ring itself. That is our cold open solved."):
            self.play(FadeIn(r4h))
            self.play(FadeIn(c1, shift=UP * 0.2))
            self.play(FadeIn(c2, shift=UP * 0.2))
            nb = C.show_neby(self, "success", height=1.3, corner=DL)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, r4h, c1, c2)))
        dow = VGroup(T("Only under ferocious conditions: the Dow process", size=30, color=th.INK, weight="BOLD"),
                     chem(r"C_6H_5Cl + 2NaOH \xrightarrow{623\ K,\ 300\ atm} C_6H_5ONa + NaCl + H_2O", size=36),
                     chem(r"C_6H_5ONa + HCl \rightarrow C_6H_5OH + NaCl", size=36)).arrange(DOWN, buff=0.35).move_to(UP * 1.2)
        with self.say("Chlorobenzene does become phenol, but only under ferocious conditions: six hundred and twenty three kelvin and three hundred atmospheres, in the industrial Dow process. Never write it as a simple room temperature reaction."):
            self.play(FadeIn(dow, shift=UP * 0.2))
        self.play(FadeOut(dow))
        title = T("Nitro groups switch the reactivity back on", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        mols = [ring(r=0.8, subs={0: ("Cl", CLC)}, label_size=24), ring(r=0.8, subs={0: ("Cl", CLC), 3: ("NO₂", NO2C)}, label_size=24),
                ring(r=0.8, subs={0: ("Cl", CLC), 1: ("NO₂", NO2C), 3: ("NO₂", NO2C)}, label_size=24),
                ring(r=0.8, subs={0: ("Cl", CLC), 1: ("NO₂", NO2C), 3: ("NO₂", NO2C), 5: ("NO₂", NO2C)}, label_size=24)]
        conds = ["NaOH, 623 K, 300 atm", "NaOH(aq), 435 K", "warm Na₂CO₃(aq)", "boiling water alone"]
        cols = [th.CORAL, th.AMBER, th.LIME, th.MINT]
        g = VGroup()
        for m_, c_, col in zip(mols, conds, cols):
            g.add(VGroup(m_, T(c_, size=24, color=col, weight="BOLD")).arrange(DOWN, buff=0.35))
        g.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.2)
        if g.width > 13:
            g.scale_to_fit_width(13)
        n_ = T("a nitro group ortho or para spreads the negative charge onto its oxygens; meta does almost nothing", size=22, color=th.BODY).to_edge(DOWN, buff=0.45)
        with self.say("But electron withdrawing groups switch the reactivity back on. Put a nitro group para to the chlorine, and hydrolysis needs only aqueous sodium hydroxide at four thirty five kelvin. Two nitro groups, and warm sodium carbonate is enough. Three, picryl chloride, and boiling water alone does it. A nitro group ortho or para lets the negative charge of the intermediate spread onto its oxygens. In the meta position it has almost no effect.") as v:
            self.play(FadeIn(title))
            for x in g:
                self.play(FadeIn(x, shift=UP * 0.2), run_time=0.6)
                self.hold(v.dur / 5 - 0.65)
            self.play(FadeIn(n_))
        self.play(FadeOut(VGroup(title, g, n_)))
        title = T("Why ortho and para, not meta?", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        pa = ring([-3.3, -0.2, 0], r=1.0, subs={0: ("Cl  OH", CLC), 3: ("NO₂", NO2C)}, label_size=24)
        me = ring([3.3, -0.2, 0], r=1.0, subs={0: ("Cl  OH", CLC), 2: ("NO₂", NO2C)}, label_size=24)
        pa[1].set_opacity(0)
        me[1].set_opacity(0)
        vp = pa[0].get_vertices()
        vm = me[0].get_vertices()
        qp = Dot(vp[1], radius=0.16, color=th.CORAL)
        qm = Dot(vm[1], radius=0.16, color=th.CORAL)
        hp = VGroup(T("para-nitro", size=28, color=th.MINT, weight="BOLD"), T("the − charge reaches the NO₂ carbon", size=22, color=th.MINT), T("and spreads onto its oxygens: stabilised", size=22, color=th.MINT)).arrange(DOWN, buff=0.08).next_to(pa, DOWN, buff=0.5)
        hm = VGroup(T("meta-nitro", size=28, color=th.CORAL, weight="BOLD"), T("the − charge never lands", size=22, color=th.CORAL), T("on the NO₂ carbon: no help", size=22, color=th.CORAL)).arrange(DOWN, buff=0.08).next_to(me, DOWN, buff=0.5)
        with self.say("Here is why position matters. When hydroxide adds to the carbon carrying chlorine, the ring briefly holds an extra negative charge, before chloride leaves. That charge moves around the ring, landing on the carbons ortho and para to the point of attack. With a nitro group para, the charge reaches the nitro carbon and spreads onto its oxygens, so the intermediate is stabilised and the reaction is fast."):
            self.play(FadeIn(title), Create(pa))
            self.play(FadeIn(qp))
            self.play(qp.animate.move_to(vp[5]), run_time=0.6)
            self.play(qp.animate.move_to(vp[3]), run_time=0.6)
            self.play(Flash(vp[3], color=th.MINT, flash_radius=0.6), FadeIn(hp))
        with self.say("With the nitro group meta, the charge hops between the same three carbons, but none of them carries the nitro group. No extra stabilisation, so a meta nitro group hardly helps."):
            self.play(Create(me), FadeIn(qm))
            self.play(qm.animate.move_to(vm[5]), run_time=0.6)
            self.play(qm.animate.move_to(vm[3]), run_time=0.6)
            self.play(FadeIn(hm))
        self.play(FadeOut(VGroup(title, pa, me, qp, qm, hp, hm)))
        self.quiz("Chlorobenzene is far less reactive than chloroethane towards OH⁻ mainly because",
                  ["Cl is less electronegative", "partial C=Cl double bond", "it is a gas", "it has no lone pairs"], 1,
                  "Pause and think. What is the main reason chlorobenzene resists hydroxide?",
                  "B. Resonance gives the carbon chlorine bond partial double bond character, so it is shorter and stronger. The other points, the s p two carbon, the pi cloud, and the blocked mechanisms, all add to it. Chlorine's electronegativity is unchanged, and chlorobenzene is a liquid with lone pairs on chlorine.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        red = VGroup(T("Reduction", size=30, color=th.SKY, weight="BOLD"), chem(r"C_6H_5Cl + 2[H] \xrightarrow{Ni{-}Al\ alloy\ /\ NaOH} C_6H_6 + HCl", size=38),
                     T("also Zn/HCl or H₂/Pd. Not a nucleophilic substitution: H arrives as a neutral atom", size=22, color=th.BODY)).arrange(DOWN, buff=0.25).move_to(UP * 1.4)
        with self.say("Reduction is easy. Nickel aluminium alloy in alkali, or zinc and hydrochloric acid, replaces chlorine by hydrogen to give benzene. It works where hydroxide fails because the hydrogen arrives as a neutral atom, not as a nucleophile."):
            self.play(FadeIn(red))
        self.play(FadeOut(red))
        title = T("Chlorine: deactivating, but ortho–para directing", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rg = ring([-3.4, -0.4, 0], r=1.1, subs={0: ("Cl", CLC)}, label_size=30)
        vt = rg[0].get_vertices()
        dots = VGroup(*[Dot(vt[k], radius=0.14, color=th.CORAL) for k in (1, 3, 5)])
        dl = VGroup(T("o", size=24, color=th.CORAL).next_to(vt[1], RIGHT, buff=0.2), T("p", size=24, color=th.CORAL).next_to(vt[3], DOWN, buff=0.2), T("o", size=24, color=th.CORAL).next_to(vt[5], LEFT, buff=0.2))
        ef = VGroup(para("−I effect: Cl pulls electrons out, so the ring reacts more slowly than benzene", width=7.0, size=26, color=th.AMBER),
                    para("+R effect: Cl's lone pair puts extra density at ortho and para", width=7.0, size=26, color=th.MINT),
                    para("para usually dominates: ortho is crowded (steric hindrance)", width=7.0, size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.6, -0.4, 0])
        with self.say("The ring can still take part in electrophilic substitution, and chlorine has a split personality. Its inductive effect pulls electrons out of the ring, so the ring reacts more slowly than benzene: deactivating. But its resonance effect pushes lone pair density into the ring, specifically at the ortho and para positions, so that is where the electrophile goes: ortho para directing. Para usually wins, because the ortho position is crowded."):
            self.play(FadeIn(title), Create(rg))
            self.play(FadeIn(ef[0]))
            self.play(FadeIn(ef[1]), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2), FadeIn(dl))
            self.play(FadeIn(ef[2]))
        self.play(FadeOut(VGroup(title, rg, dots, dl, ef)))
        title = T("The intermediate decides the position", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        op = ring([-3.3, -0.1, 0], r=1.0, subs={0: ("Cl", CLC), 3: ("NO₂", NO2C)}, label_size=24)
        mt = ring([3.3, -0.1, 0], r=1.0, subs={0: ("Cl", CLC), 2: ("NO₂", NO2C)}, label_size=24)
        op[1].set_opacity(0)
        mt[1].set_opacity(0)
        pl = Dot(op[0].get_vertices()[3], radius=0.16, color=th.AMBER)
        plm = Dot(mt[0].get_vertices()[2], radius=0.16, color=th.AMBER)
        ex = para("para attack: the + charge can reach the C–Cl carbon, where Cl's lone pair forms C=Cl⁺: extra stability", width=5.6, size=24, color=th.MINT, align="center").next_to(op, DOWN, buff=0.45)
        exm = para("meta attack: the + charge never reaches the C–Cl carbon: no help from Cl", width=5.6, size=24, color=th.CORAL, align="center").next_to(mt, DOWN, buff=0.45)
        with self.say("Electrophilic substitution has its own intermediate, this time with a positive charge. When the electrophile attacks para to chlorine, that positive charge can land on the carbon holding chlorine, and chlorine's lone pair shares itself to form a C double bond C l plus structure. That extra resonance form stabilises the intermediate. The same is true for ortho attack."):
            self.play(FadeIn(title), Create(op), FadeIn(pl))
            self.play(pl.animate.move_to(op[0].get_vertices()[1]), run_time=0.6)
            self.play(pl.animate.move_to(op[0].get_vertices()[0]), run_time=0.6)
            self.play(Flash(op[0].get_vertices()[0], color=th.MINT, flash_radius=0.6), FadeIn(ex))
        with self.say("For meta attack, the positive charge never reaches the carbon holding chlorine, so it gets no such help. That is why chlorine directs ortho and para, even while its inductive pull slows the whole ring down."):
            self.play(Create(mt), FadeIn(plm))
            self.play(plm.animate.move_to(mt[0].get_vertices()[4]), run_time=0.6)
            self.play(FadeIn(exm))
        self.play(FadeOut(VGroup(title, op, mt, pl, plm, ex, exm)))
        rows = [["Reaction", "Reagents", "Products"], ["nitration", "conc. HNO₃ + conc. H₂SO₄, 320 K", "o- (30 %) and p- (70 %) nitro"],
                ["halogenation", "Cl₂, anhydrous AlCl₃", "o- and p-dichlorobenzene"], ["sulphonation", "conc. H₂SO₄, heat", "o- and p-sulphonic acids"],
                ["F–C alkylation", "CH₃Cl, anhydrous AlCl₃", "o- and p-chlorotoluene"], ["F–C acylation", "CH₃COCl, anhydrous AlCl₃", "o- and p-chloroacetophenone"]]
        tb = C.table(rows, [2.8, 4.8, 5.4], row_h=0.7, size=26, colors=[th.AMBER, th.BODY, th.INK]).move_to(UP * 0.3)
        with self.say("So every electrophilic substitution gives ortho and para products, with para the major one. Nitration with mixed acid, chlorination with aluminium chloride, sulphonation, and Friedel Crafts alkylation and acylation.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))
        head, prob = C.example_head(self, "45.0 g of chlorobenzene is nitrated; 90 % is converted to mononitro products with o : p = 30 : 70. Find the mass of p-nitrochlorobenzene.")
        st = C.steps(r"n = \tfrac{45.0}{112.5} = 0.400\ \mathrm{mol};\ \ \text{converted} = 0.400 \times 0.90 = 0.360",
                     r"\text{para} = 0.360 \times 0.70 = 0.252\ \mathrm{mol}",
                     r"M(\mathrm{C_6H_4ClNO_2}) = 72 + 4 + 35.5 + 14 + 32 = 157.5",
                     r"m = 0.252 \times 157.5 = 39.7\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example. Forty five grams of chlorobenzene is zero point four moles. Ninety percent converts: zero point three six moles. Seventy percent of that is para: zero point two five two moles. Para nitrochlorobenzene has molar mass one fifty seven point five, so thirty nine point seven grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Fittig and Wurtz–Fittig", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        a = ring([-3.0, 0.4, 0], r=0.7, subs={1: ("Cl", CLC)}, label_size=22)
        b = ring([3.0, 0.4, 0], r=0.7, subs={5: ("Cl", CLC)}, label_size=22)
        na = VGroup(*[VGroup(Circle(radius=0.3, fill_color=C.EL["Na"], fill_opacity=1, stroke_width=0), T("Na", size=18, color=WHITE, weight="BOLD")).move_to([x, -1.4, 0]) for x in (-0.6, 0.6)])
        e1 = chem(r"2C_6H_5Cl + 2Na \xrightarrow{\text{dry ether}} C_6H_5{-}C_6H_5 + 2NaCl", size=36, color=th.AMBER).to_edge(DOWN, buff=1.2)
        bl = T("biphenyl: white solid, m.p. 71 °C, a heat-transfer fluid", size=22, color=th.BODY).next_to(e1, DOWN, buff=0.2)
        with self.say("Haloarenes couple with sodium, just like the Wurtz reaction. Two chlorobenzene molecules with sodium in dry ether lose their chlorines to the sodium and join together, giving biphenyl. This is the Fittig reaction."):
            self.play(FadeIn(title), Create(a), Create(b), FadeIn(na))
            self.play(a[3].animate.move_to(na[0].get_center() + UP * 0.55), b[3].animate.move_to(na[1].get_center() + UP * 0.55), FadeOut(a[2]), FadeOut(b[2]),
                      VGroup(a[0], a[1]).animate.move_to([-0.95, 0.4, 0]), VGroup(b[0], b[1]).animate.move_to([0.95, 0.4, 0]), run_time=1.6)
            link = Line([-0.95 + 0.7, 0.4, 0], [0.95 - 0.7, 0.4, 0], color=th.AMBER, stroke_width=6)
            self.play(Create(link))
            self.play(Write(e1), FadeIn(bl))
        self.play(FadeOut(VGroup(a, b, na, e1, bl, link)))
        e2 = VGroup(chem(r"C_6H_5Cl + 2Na + CH_3Cl \xrightarrow{\text{dry ether}} C_6H_5CH_3 + 2NaCl", size=36, color=th.SKY),
                    chem(r"C_6H_5Br + 2Na + C_2H_5Br \rightarrow C_6H_5C_2H_5 + 2NaBr", size=34)).arrange(DOWN, buff=0.3).move_to(UP * 0.9)
        bars = VGroup(*[VGroup(T(a_, size=22, color=c_), Rectangle(width=w_, height=0.45, fill_color=c_, fill_opacity=0.8, stroke_width=0)).arrange(RIGHT, buff=0.3)
                        for a_, w_, c_ in [("aryl + alkyl: wanted", 4.0, th.MINT), ("aryl + aryl: biphenyl", 1.6, th.MUTED), ("alkyl + alkyl: alkane", 1.6, th.MUTED)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(e2, DOWN, buff=0.5)
        with self.say("Mix a haloarene with a haloalkane, and you get the Wurtz Fittig reaction: chlorobenzene and chloromethane give toluene. It puts a straight alkyl chain on a ring without rearrangement. But three couplings compete: aryl with alkyl, which we want, aryl with aryl, and alkyl with alkyl. And the ether must be perfectly dry, since sodium reacts violently with water."):
            self.play(Write(e2[0]))
            self.play(FadeIn(e2[1]))
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.3))
        self.play(FadeOut(VGroup(title, e2, bars)))
        title = T("Chloral + chlorobenzene → DDT", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"CCl_3CHO + 2C_6H_5Cl \xrightarrow{\text{conc. } H_2SO_4} (4{-}ClC_6H_4)_2CH{-}CCl_3 + H_2O", size=34).next_to(title, DOWN, buff=0.4)
        center = np.array([0, -0.4, 0])
        r1 = ring(center + LEFT * 2.4, r=0.65, subs={5: ("Cl", CLC)}, label_size=22)
        r2 = ring(center + RIGHT * 2.4, r=0.65, subs={1: ("Cl", CLC)}, label_size=22)
        ch = VGroup(T("CH", size=28, color=th.INK, weight="BOLD").move_to(center), T("CCl₃", size=28, color=CLC, weight="BOLD").move_to(center + UP * 1.1),
                    Line(center + UP * 0.25, center + UP * 0.85, color=th.MUTED, stroke_width=4), Line(center + LEFT * 0.35, center + LEFT * 1.75, color=th.MUTED, stroke_width=4),
                    Line(center + RIGHT * 0.35, center + RIGHT * 1.75, color=th.MUTED, stroke_width=4))
        nm = T("DDT, C₁₄H₉Cl₅", size=28, color=th.AMBER, weight="BOLD").next_to(ch, DOWN, buff=0.6)
        with self.say("With chloral, trichloroethanal, and concentrated sulphuric acid, two chlorobenzene molecules join at their para positions to one carbon. The product is D D T, the first modern synthetic insecticide."):
            self.play(FadeIn(title), Write(eq))
            self.play(Create(r1), Create(r2), FadeIn(ch), FadeIn(nm))
        warn = para("DDT saved millions of lives from malaria and typhus, but it is stable, fat-soluble and non-biodegradable, so it bioaccumulates up food chains. Banned for farm use in Nepal (Stockholm Convention); allowed only for malaria vector control.", width=11.5, size=24, color=th.CORAL).to_edge(DOWN, buff=0.4)
        self.play(FadeOut(nm), VGroup(r1, r2, ch).animate.shift(UP * 0.5))
        with self.say("D D T saved millions of lives from malaria and typhus. But it is stable, fat soluble and does not break down, so it builds up in food chains. Its farm use is now banned in Nepal under the Stockholm Convention, though small amounts are still allowed for malaria control."):
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(title, eq, r1, r2, ch, warn)))
        head, prob = C.example_head(self, "14.74 g of chloral (147.4 g mol⁻¹) condenses with excess chlorobenzene. Find (i) the chlorobenzene consumed, (ii) the DDT formed (354.5 g mol⁻¹).")
        st = C.steps(r"n(\text{chloral}) = \tfrac{14.74}{147.4} = 0.1000\ \mathrm{mol};\ \ \text{ratio } 1:2:1",
                     r"(i)\ 0.200 \times 112.5 = 22.5\ \mathrm{g\ C_6H_5Cl}",
                     r"(ii)\ 0.1000 \times 354.5 = 35.45\ \mathrm{g\ DDT}", size=40).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example. Fourteen point seven four grams of chloral is zero point one mole. It uses two moles of chlorobenzene per mole: zero point two moles, twenty two point five grams. And it gives zero point one mole of D D T, thirty five point four five grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        cards = VGroup(*[C.card(self, a, b, w=3.9, h=2.1, color=c, tsize=24, bsize=20) for a, b, c in [
            ("Solvent", "chlorobenzene for paints, rubber, waxes, adhesives", CLC), ("Phenol & aniline", "via the Dow process and ammonolysis", th.AMBER),
            ("Dyes & drugs", "via o- and p-nitrochlorobenzene", th.PINK), ("DDT", "with chloral: vector control only", th.CORAL),
            ("Moth balls", "p-dichlorobenzene: moth repellent, deodorant blocks", th.SKY), ("Lab reagents", "C₆H₅Br, C₆H₅I for Grignard reagents", th.MINT)]]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25)).move_to(UP * 0.3)
        warn = T("persistent in soil and water: never pour chlorinated residues down the sink", size=24, color=th.CORAL).to_edge(DOWN, buff=0.5)
        with self.say("Haloarenes are useful. Chlorobenzene is a solvent for paints and rubber, and the starting point for phenol, aniline, dyes and drugs, and D D T. Para dichlorobenzene is the moth repellent in moth balls and toilet blocks. Bromo and iodobenzene make Grignard reagents in the lab. But chlorinated aromatics persist in soil and water, so their residues must never go down the sink.") as v:
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 7 - 0.45)
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(cards, warn)))
        self.tip("Haloarenes are o/p directing but deactivating: −I effect slows the ring, +R effect points the electrophile to ortho and para (para major).",
                 "A favourite two marks. Chlorine on a ring is deactivating, because of its inductive pull, but ortho para directing, because its lone pair pushes density into those positions. And para is the major product.", state="wink")
        self.quiz("2,4,6-trinitrochlorobenzene is hydrolysed to the corresponding phenol by",
                  ["NaOH at 623 K, 300 atm", "boiling water alone", "no reagent at all", "Ni–Al alloy"], 1,
                  "Last one. Picryl chloride, with three nitro groups ortho and para to the chlorine. What does it take to hydrolyse it? Pause and think.",
                  "B, boiling water alone. Three nitro groups at ortho and para positions spread the negative charge of the intermediate onto their oxygens, making substitution easy. Six twenty three kelvin and three hundred atmospheres is what plain chlorobenzene needs.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Haloarene: X on a ring carbon; benzyl chloride is an aralkyl halide.",
            "C₆H₄Cl₂ has three isomers; para melts highest (symmetry).",
            "C₆H₆ + Cl₂ (AlCl₃, dark) → C₆H₅Cl; diazonium + CuCl/HCl (Sandmeyer).",
            "Low reactivity: resonance, sp² carbon, π cloud, no SN1 or SN2.",
            "Dow process: 623 K, 300 atm; o/p-NO₂ groups make it easy.",
            "Cl is deactivating but o/p directing; para product major.",
            "Fittig → biphenyl; Wurtz–Fittig → toluene; chloral → DDT.",
        ], "Let us recap. In a haloarene the halogen sits on a ring carbon. Dichlorobenzene has three isomers, and para melts highest. Chlorobenzene is made from benzene in the dark with aluminium chloride, or from a diazonium salt by the Sandmeyer reaction. It resists nucleophiles for four reasons: resonance, the s p two carbon, the pi cloud, and no available mechanism, unless nitro groups sit ortho or para. Chlorine is deactivating but ortho para directing. And sodium couples haloarenes in the Fittig and Wurtz Fittig reactions, while chloral gives D D T.")
        self.outro("That is haloarenes. Next, we replace the halogen with an hydroxyl group, and meet the alcohols. See you in the next lesson on NEBians.")
