import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem, push, benzene  # noqa: E402

OC = "#FF6B6B"
IC = "#B18CFF"
PINK = "#FF7AB6"
ETH = "#7BE495"

MAP = [("hic", r"C_2H_5OH + C_2H_5I", "HI, cold (1 mol)", th.SKY),
       ("hih", r"2C_2H_5I + H_2O", "excess HI, heat", "#5C8DFF"),
       ("hclc", r"[(C_2H_5)_2OH]^+Cl^-", "conc. HCl, cold", th.MINT),
       ("hclh", r"2C_2H_5Cl + H_2O", "conc. HCl, heat, pressure", th.LIME),
       ("so4c", r"[(C_2H_5)_2OH]^+HSO_4^-", "conc. H₂SO₄, cold", th.AMBER),
       ("so4h", r"2C_2H_5HSO_4", "conc. H₂SO₄, heat", "#F08A24"),
       ("o2", r"CH_3CH(OOH)OC_2H_5", "air + light, slow", th.CORAL),
       ("cld", r"(CH_3CHCl)_2O", "Cl₂, dark", PINK),
       ("cls", r"C_2Cl_5OC_2Cl_5", "Cl₂, sunlight", th.TEAL)]


def node(txt, pos, color=th.INK, size=34):
    return T(txt, size=size, color=color, weight="BOLD").move_to(pos)


def bond(a, b, color=th.MUTED, w=5, shrink=0.28):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    u = (b - a) / np.linalg.norm(b - a)
    return Line(a + u * shrink, b - u * shrink, color=color, stroke_width=w)


def lone_pair(p, d=UP, col=th.AMBER):
    d = np.array(d, dtype=float)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Dot(p + d * 0.36 + perp * 0.1, radius=0.05, color=col), Dot(p + d * 0.36 - perp * 0.1, radius=0.05, color=col))


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 12
    TITLE = "Ethers"
    SUBTITLE = "An oxygen between two carbons"
    SECTIONS = ["Introduction, naming and isomerism", "Williamson's synthesis", "Physical properties",
                "Chemical properties: HI, HCl, H₂SO₄, air, Cl₂", "Uses"]
    NEXT = "Unit 13 · Aldehydes and Ketones"

    def lesson(self):
        self.rmap = C.ReactionMap(r"C_2H_5OC_2H_5", MAP, center=(0, -0.15, 0), rx=4.9, ry=2.6)
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        yr = T("Boston, 16 October 1846", size=30, color=th.AMBER, weight="BOLD").move_to([0, 2.4, 0])
        sp = VGroup(Circle(radius=1.15, stroke_color=th.MUTED, stroke_width=4, fill_color=th.PANEL, fill_opacity=1),
                    Rectangle(width=0.4, height=1.6, stroke_color=th.MUTED, stroke_width=4).shift(UP * 1.5 + RIGHT * 0.45).rotate(-0.4),
                    T("ether", size=32, color=ETH, weight="BOLD")).move_to([-4.0, -0.8, 0])
        bed = RoundedRectangle(corner_radius=0.2, width=4.4, height=0.5, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0).move_to([3.0, -1.5, 0])
        body = RoundedRectangle(corner_radius=0.35, width=3.2, height=0.7, fill_color=th.SKY, fill_opacity=0.5, stroke_width=0).move_to([3.4, -0.95, 0])
        head = Circle(radius=0.45, fill_color="#F2C9A0", fill_opacity=1, stroke_width=0).move_to([1.35, -0.85, 0])
        pat = VGroup(bed, body, head)
        vap = VGroup(*[Circle(radius=0.1 + 0.04 * k, stroke_color=ETH, stroke_width=3).move_to([-3.0 + 0.62 * k, 0.4 + 0.35 * np.sin(1.3 * k), 0]) for k in range(7)])
        zz = T("asleep · no pain", size=34, color=th.MINT, weight="BOLD").move_to([3.6, 1.5, 0])
        zl = T("z z z", size=34, color=th.MINT, weight="BOLD").move_to([1.5, 0.0, 0])
        with self.say("Boston, October eighteen forty six. In front of a crowd of doctors, a dentist named William Morton holds a glass globe to a patient's mouth. The patient breathes in a sweet smelling vapour, falls asleep, and a tumour is cut from his neck without a cry of pain. The vapour was ether, and surgery was changed forever."):
            self.play(FadeIn(yr))
            self.play(FadeIn(sp, shift=UP * 0.2), FadeIn(pat))
            self.play(LaggedStart(*[FadeIn(v, shift=RIGHT * 0.3) for v in vap], lag_ratio=0.2), run_time=1.6)
            self.play(FadeIn(zl, shift=UP * 0.3), FadeIn(zz))
        self.play(FadeOut(VGroup(yr, sp, vap, zz, zl, pat)))
        a = VGroup(chem(r"C_2H_5{-}O{-}C_2H_5", size=48, color=ETH), T("ethoxyethane", size=26, color=ETH), T("b.p. 34.6 °C", size=40, color=ETH, weight="BOLD")).arrange(DOWN, buff=0.25).move_to([-3.3, 0.2, 0])
        b = VGroup(chem(r"CH_3CH_2CH_2CH_2{-}OH", size=48, color=th.SKY), T("butan-1-ol", size=26, color=th.SKY), T("b.p. 117.7 °C", size=40, color=th.SKY, weight="BOLD")).arrange(DOWN, buff=0.25).move_to([3.3, 0.2, 0])
        f = chem(r"\text{both } C_4H_{10}O,\ M = 74", size=40, color=th.AMBER).move_to([0, 2.3, 0])
        with self.say("Here is the puzzle. Ether, ethoxyethane, has the formula C four H ten O. So does butan one ol. Same atoms, same mass. Yet the ether boils at thirty four point six degrees, it evaporates from your palm, while the alcohol boils at one hundred and seventeen. A gap of eighty three degrees."):
            self.play(Write(f))
            self.play(FadeIn(a[0]), FadeIn(a[1]), FadeIn(b[0]), FadeIn(b[1]))
            self.play(FadeIn(a[2], scale=1.3), FadeIn(b[2], scale=1.3))
        nb = C.show_neby(self, "surprised", height=2.0, at=[0, -2.0, 0])
        with self.say("How can two molecules made of exactly the same atoms be so different? Hold that question. We will crack it in part three."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(a, b, f)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 12: Ethers. An oxygen atom with a carbon group on each side. Quiet, unreactive molecules, which is exactly what makes them the chemist's favourite solvent."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. What ethers are, how they are named, and their isomers. Williamson's synthesis, and why it must be planned the right way round. Physical properties, where we solve the boiling point puzzle. The reactions of ether with hydrogen iodide, hydrochloric and sulphuric acids, air and chlorine. And finally, the uses of ether.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        y = 0.9
        o = np.array([0, y, 0])
        ang = np.radians(111.7 / 2)
        l_, r_ = o + 2.2 * np.array([-np.sin(ang), -np.cos(ang), 0]), o + 2.2 * np.array([np.sin(ang), -np.cos(ang), 0])
        oo = node("O", o, color=OC, size=64)
        h1, h2 = node("H", l_, color=C.EL["H"], size=56), node("H", r_, color=C.EL["H"], size=56)
        b1, b2 = bond(o, l_, shrink=0.4, w=6), bond(o, r_, shrink=0.4, w=6)
        nm = T("water, H–O–H", size=36, color=th.SKY).move_to([0, -2.2, 0])
        with self.say("Start with a water molecule, H O H. Replace one hydrogen with an alkyl group and you get an alcohol. Replace both, and you have an ether: R O R dash. An oxygen atom bonded to two carbon groups."):
            self.play(FadeIn(VGroup(oo, h1, h2, b1, b2)), FadeIn(nm))
            r1 = node("R", l_, color=ETH, size=56)
            n2 = T("alcohol, R–O–H", size=36, color=th.MINT).move_to(nm)
            self.play(Transform(h1, r1), Transform(nm, n2))
            r2 = node("R′", r_, color=ETH, size=56)
            n3 = T("ether, R–O–R′", size=40, color=ETH, weight="BOLD").move_to(nm)
            self.play(Transform(h2, r2), Transform(nm, n3))
        gen = chem(r"C_nH_{2n+2}O", size=46, color=th.AMBER).move_to([3.9, 1.7, 0])
        note = T("same general formula as the alcohols", size=24, color=th.BODY).next_to(gen, DOWN, buff=0.15)
        with self.say("A saturated ether has the general formula C n H two n plus two O, exactly the same as a saturated alcohol. So every ether is an isomer of some alcohol. Remember that, it comes back."):
            self.play(Write(gen), FadeIn(note))
        self.play(FadeOut(VGroup(oo, h1, h2, b1, b2, nm, gen, note)))
        title = T("Three kinds of ether", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        c1 = VGroup(T("simple (symmetrical)", size=28, color=ETH, weight="BOLD"), chem(r"C_2H_5{-}O{-}C_2H_5", size=40), T("same group on both sides", size=22, color=th.BODY)).arrange(DOWN, buff=0.25)
        c2 = VGroup(T("mixed (unsymmetrical)", size=28, color=th.SKY, weight="BOLD"), chem(r"CH_3{-}O{-}C_2H_5", size=40), T("two different groups", size=22, color=th.BODY)).arrange(DOWN, buff=0.25)
        an = benzene(r=0.6, subs={0: ("OCH₃", OC)}, label_size=24)
        c3 = VGroup(T("aromatic (mixed)", size=28, color=th.AMBER, weight="BOLD"), an, T("anisole, C₆H₅OCH₃", size=22, color=th.BODY)).arrange(DOWN, buff=0.2)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.9).move_to([0, -0.3, 0])
        with self.say("Ethers come in two classes. A simple, or symmetrical, ether has the same group on both sides, like diethyl ether. A mixed, or unsymmetrical, ether has two different groups, like methoxyethane. If one group is an aryl ring, as in anisole, methoxybenzene, it is an aromatic ether."):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.4), run_time=2.2)
        self.play(FadeOut(VGroup(title, cards)))
        title = T("Naming: the smaller group becomes alkoxy", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        f = chem(r"CH_3{-}O{-}CH_2CH_3", size=60).move_to([0, 1.3, 0])
        lft = SurroundingRectangle(f[0][0:5], color=th.SKY, buff=0.1)
        rgt = SurroundingRectangle(f[0][6:], color=th.AMBER, buff=0.1)
        lt = T("methoxy", size=34, color=th.SKY, weight="BOLD").next_to(lft, DOWN, buff=0.4)
        rt = T("ethane", size=34, color=th.AMBER, weight="BOLD").next_to(rgt, DOWN, buff=0.4)
        full = T("methoxyethane", size=44, color=th.INK, weight="BOLD").move_to([0, -1.2, 0])
        com = T("common name: ethyl methyl ether (groups in alphabetical order, then 'ether')", size=24, color=th.MUTED).move_to([0, -2.2, 0])
        with self.say("In the I U P A C system, the smaller group together with the oxygen is named as an alkoxy substituent, and the larger group is the parent chain. So C H three O C H two C H three: methoxy, plus ethane, gives methoxyethane. The common name just lists the two groups and adds the word ether: ethyl methyl ether."):
            self.play(FadeIn(title), Write(f))
            self.play(Create(lft), FadeIn(lt))
            self.play(Create(rgt), FadeIn(rt))
            self.play(TransformFromCopy(VGroup(lt, rt), full))
            self.play(FadeIn(com))
        self.play(FadeOut(VGroup(f, lft, rgt, lt, rt, full, com)))
        rows = [["Structure", "IUPAC name", "Common name"],
                ["CH₃OCH₃", "methoxymethane", "dimethyl ether"],
                ["C₂H₅OC₂H₅", "ethoxyethane", "diethyl ether"],
                ["CH₃OCH₂CH₂CH₃", "1-methoxypropane", "methyl n-propyl ether"],
                ["CH₃OCH(CH₃)₂", "2-methoxypropane", "methyl isopropyl ether"],
                ["(CH₃)₃COCH₃", "2-methoxy-2-methylpropane", "MTBE"],
                ["C₆H₅OCH₃", "methoxybenzene", "anisole"],
                ["C₆H₅OC₆H₅", "phenoxybenzene", "diphenyl ether"]]
        tb = C.table(rows, [3.4, 4.4, 4.2], row_h=0.6, size=26, head_color=th.INK, colors=[ETH, th.INK, th.MUTED]).move_to([0, -0.6, 0])
        with self.say("Here are the ones to know. Methoxymethane, dimethyl ether. Ethoxyethane, diethyl ether, often just called ether. One methoxypropane and two methoxypropane. Two methoxy two methylpropane, known as M T B E, a petrol additive. And on the ring side, methoxybenzene, called anisole, and phenoxybenzene, diphenyl ether.") as v:
            self.play(FadeIn(tb[0]))
            for r in tb[1:]:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur / 10)
        self.play(FadeOut(VGroup(title, tb)))
        # ---- isomerism
        title = T("Metamerism: slide the oxygen along", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        xs = [-3.0, -1.5, 0.0, 1.5, 3.0]
        split = T("1 + 3", size=40, color=th.AMBER, weight="BOLD").move_to([0, -1.0, 0])
        nm = T("CH₃–O–CH₂CH₂CH₃, 1-methoxypropane", size=30, color=th.SKY).move_to([0, -2.0, 0])

        c4 = VGroup(*[node("C", [x, 0.4, 0], size=44) for x in [-3.0, -0.0, 1.5, 3.0]])
        o4 = node("O", [-1.5, 0.4, 0], color=OC, size=44)
        ln = VGroup(*[Line([xs[k] + 0.3, 0.4, 0], [xs[k + 1] - 0.3, 0.4, 0], color=th.MUTED, stroke_width=5) for k in range(4)])
        with self.say("Ethers show three kinds of isomerism. The special one is metamerism. Take C four H ten O. Put one carbon on the left of the oxygen and three on the right: one methoxypropane."):
            self.play(FadeIn(title))
            self.play(FadeIn(VGroup(c4, o4, ln)))
            self.play(FadeIn(split), FadeIn(nm))
        o5 = node("O", [0.0, 0.4, 0], color=OC, size=44)
        c5 = VGroup(*[node("C", [x, 0.4, 0], size=44) for x in [-3.0, -1.5, 1.5, 3.0]])
        split2 = T("2 + 2", size=40, color=th.AMBER, weight="BOLD").move_to(split)
        nm2 = T("CH₃CH₂–O–CH₂CH₃, ethoxyethane", size=30, color=ETH).move_to(nm)
        with self.say("Now slide the oxygen one place along. Two carbons on each side: ethoxyethane. Same formula, same functional group, but the carbons are shared out differently around the oxygen. Those two are metamers."):
            self.play(Transform(o4, o5), Transform(c4, c5), Transform(split, split2), Transform(nm, nm2), run_time=1.5)
            self.sfx("pop")
        self.play(FadeOut(VGroup(title, c4, o4, ln, split, nm)))
        title = T("C₄H₁₀O: seven isomers", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        alc = VGroup(*[T(s_, size=26, color=th.SKY) for s_ in ["butan-1-ol", "butan-2-ol", "2-methylpropan-1-ol", "2-methylpropan-2-ol"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eth = VGroup(*[T(s_, size=26, color=ETH) for s_ in ["ethoxyethane", "1-methoxypropane", "2-methoxypropane"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ah = T("4 alcohols", size=32, color=th.SKY, weight="BOLD")
        eh = T("3 ethers", size=32, color=ETH, weight="BOLD")
        A = VGroup(ah, alc).arrange(DOWN, buff=0.35).move_to([-3.2, -0.3, 0])
        E = VGroup(eh, eth).arrange(DOWN, buff=0.35).move_to([3.2, -0.3, 0])
        k1 = T("functional isomers", size=24, color=th.AMBER).move_to([0, 0.6, 0])
        ka = DoubleArrow([-1.1, 0.2, 0], [1.1, 0.2, 0], color=th.AMBER, buff=0, stroke_width=4)
        k2 = para("1- and 2-methoxypropane: chain (position) isomers", width=5.5, size=24, color=th.MINT).move_to([3.2, -2.6, 0])
        with self.say("Count them all for C four H ten O. Four alcohols, and three ethers, seven isomers in all. Any alcohol and any ether are functional isomers. And within the ethers, one methoxypropane and two methoxypropane differ only in the chain, so they are chain or position isomers, not metamers."):
            self.play(FadeIn(title))
            self.play(FadeIn(A, shift=UP * 0.2))
            self.play(FadeIn(E, shift=UP * 0.2))
            self.play(GrowFromCenter(ka), FadeIn(k1))
            self.play(FadeIn(k2))
        self.play(FadeOut(VGroup(title, A, E, k1, ka, k2)))
        # ---- worked example 12.1
        head, prob = C.example_head(self, "Write all the isomeric ethers of C₅H₁₂O with their IUPAC names, and say which pairs are metamers.")
        grp1 = VGroup(T("1 + 4: methoxybutanes", size=28, color=th.SKY, weight="BOLD"),
                      *[T(s_, size=25, color=th.INK) for s_ in ["CH₃OCH₂CH₂CH₂CH₃   1-methoxybutane", "CH₃OCH(CH₃)CH₂CH₃   2-methoxybutane",
                                                              "CH₃OCH₂CH(CH₃)₂   1-methoxy-2-methylpropane", "CH₃OC(CH₃)₃   2-methoxy-2-methylpropane"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        grp2 = VGroup(T("2 + 3: ethoxypropanes", size=28, color=th.AMBER, weight="BOLD"),
                      *[T(s_, size=25, color=th.INK) for s_ in ["C₂H₅OCH₂CH₂CH₃   1-ethoxypropane", "C₂H₅OCH(CH₃)₂   2-ethoxypropane"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(grp1, grp2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        ans = para("6 ethers. Any methoxybutane with any ethoxypropane is a pair of metamers (1 + 4 vs 2 + 3).", width=4.4, size=28, color=th.MINT).move_to([4.2, -1.2, 0])
        n_ = len(grp1) - 1 + len(grp2) - 1
        assert n_ == 6
        with self.say("Worked example twelve point one. Five carbons must be split around the oxygen, either one plus four, or two plus three. One plus four gives the methoxybutanes, and a butyl group has four arrangements, so four ethers. Two plus three gives the ethoxypropanes, with two arrangements of propyl. Six ethers in all. Any methoxybutane with any ethoxypropane is a pair of metamers."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(FadeIn(grp1[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in grp1[1:]], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(grp2[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in grp2[1:]], lag_ratio=0.4), run_time=1.2)
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(head, prob, grp1, grp2, ans)))
        self.quiz("CH₃–O–C₃H₇ and C₂H₅–O–C₂H₅ are",
                  ["chain isomers", "position isomers", "metamers", "functional isomers"], 2,
                  "Quick check. Methyl propyl ether and diethyl ether. What kind of isomers are they?",
                  "C, metamers. Same formula, same ether group, but the carbons are shared one plus three in one and two plus two in the other.")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Williamson's synthesis", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e1 = chem(r"C_2H_5ONa + C_2H_5I \xrightarrow{\text{dry, warm}} C_2H_5OC_2H_5 + NaI", size=44).move_to([0, 1.3, 0])
        e2 = chem(r"C_6H_5ONa + CH_3I \rightarrow C_6H_5OCH_3 + NaI", size=44).move_to([0, 0.1, 0])
        l2 = T("anisole", size=26, color=th.AMBER).next_to(e2, DOWN, buff=0.15).align_to(e2, RIGHT).shift(LEFT * 1.6)
        rule = para("a sodium alkoxide or phenoxide (the nucleophile) + a haloalkane", width=10, size=28, color=th.MINT, align="center").move_to([0, -1.6, 0])
        with self.say("The general way to make an ether is Williamson's synthesis. Warm a sodium alkoxide with a haloalkane, in dry conditions. Sodium ethoxide and iodoethane give diethyl ether and sodium iodide. Sodium phenoxide and iodomethane give anisole."):
            self.play(FadeIn(title))
            self.play(Write(e1))
            self.play(Write(e2), FadeIn(l2))
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(title, e1, e2, l2, rule)))
        self.sn2()
        self.coordinate()
        self.planning()
        self.dehydration()

    def sn2(self):
        title = T("The mechanism is SN2: backside attack", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        t = ValueTracker(0)
        c = np.array([0, -0.3, 0])
        angs = [PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3]
        cols = [th.SKY, th.MINT, th.AMBER]
        labs = ["H", "H", "CH₃"]
        balls = [VGroup(Circle(radius=0.4, fill_color=col, fill_opacity=1, stroke_width=0), T(lab, size=20, color=th.BG, weight="BOLD")) for col, lab in zip(cols, labs)]
        nub_ = VGroup(Circle(radius=0.5, fill_color=OC, fill_opacity=1, stroke_width=0), T("C₂H₅O⁻", size=18, color=WHITE, weight="BOLD"))
        lgb_ = VGroup(Circle(radius=0.48, fill_color=IC, fill_opacity=1, stroke_width=0), T("I", size=24, color=WHITE, weight="BOLD"))
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
            nu_x = -5.0 + 3.1 * np.clip(s / 0.5, 0, 1)
            lg_x = 1.8 + 3.2 * np.clip((s - 0.5) / 0.5, 0, 1)
            nup = c + np.array([nu_x, 0, 0])
            lgp = c + np.array([lg_x, 0, 0])
            if s > 0.15:
                if s < 0.8:
                    g.add(DashedLine(nup + RIGHT * 0.5, c + LEFT * 0.3, color=OC, stroke_width=3))
                else:
                    g.add(Line(nup + RIGHT * 0.5, c + LEFT * 0.3, color=th.MUTED, stroke_width=5))
            if s <= 0.3:
                g.add(Line(c, lgp, color=th.MUTED, stroke_width=5))
            elif s < 0.85:
                g.add(DashedLine(c + RIGHT * 0.3, lgp + LEFT * 0.45, color=IC, stroke_width=3))
            g.add(nub_.copy().move_to(nup))
            g.add(lgb_.copy().move_to(lgp))
            g.add(cat_.copy().move_to(c))
            return g
        m = always_redraw(mol)
        lp = lone_pair(c + np.array([-4.5, 0, 0]), RIGHT)
        with self.say("Why does this work? The ethoxide ion is a strong nucleophile, rich in electrons. It attacks the carbon carrying the iodine, and it must come in from the side exactly opposite the iodine. This is the S N two mechanism you met in haloalkanes."):
            self.play(FadeIn(title))
            self.add(m)
            arr = push(c + np.array([-4.4, 0.25, 0]), c + np.array([-0.3, 0.3, 0]), angle=-TAU / 6, color=th.AMBER)
            arr2 = push(c + np.array([0.9, 0.15, 0]), c + np.array([1.6, 0.5, 0]), angle=-TAU / 4, color=th.AMBER)
            self.play(FadeIn(lp))
            self.play(Create(arr), Create(arr2))
        ts = T("one step: the O–C bond forms as the C–I bond breaks", size=26, color=th.AMBER).next_to(title, DOWN, buff=0.3)
        with self.say("The curved arrows show the electrons moving. A lone pair on the oxygen forms the new carbon oxygen bond, while the carbon iodine bond breaks, and its electron pair leaves with the iodide. Both happen at once, in a single step, and the three hydrogens and the methyl flip through like an umbrella."):
            self.play(FadeOut(lp), FadeOut(arr), FadeOut(arr2), FadeIn(ts))
            self.play(t.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        pr = chem(r"C_2H_5{-}O{-}CH_2CH_3 + I^-", size=40, color=th.MINT).to_edge(DOWN, buff=0.7)
        with self.say("The result: diethyl ether and an iodide ion. Keep this backside attack in mind. It decides which way round the synthesis has to be planned."):
            self.play(Write(pr))
        self.play(FadeOut(VGroup(title, ts, pr)), FadeOut(m))
        self.remove(m)

    def coordinate(self):
        title = T("One step, one hump", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Arrow([-5.6, -2.8, 0], [-5.6, 2.2, 0], buff=0, color=th.MUTED, stroke_width=3)
        el = T("energy", size=22, color=th.MUTED).next_to(ax, UP, buff=0.05)
        ax2 = Arrow([-5.6, -2.8, 0], [5.4, -2.8, 0], buff=0, color=th.MUTED, stroke_width=3)
        xl = T("reaction coordinate", size=22, color=th.MUTED).next_to(ax2, DOWN, buff=0.1).align_to(ax2, RIGHT)
        pts = [[-5.2, -0.6], [-3.6, -0.6], [-1.6, 0.4], [0.0, 1.5], [1.6, 0.0], [3.4, -1.7], [5.0, -1.7]]
        curve = VMobject(stroke_color=th.INK, stroke_width=5).set_points_smoothly([np.array([x, y_, 0]) for x, y_ in pts])
        top = curve.point_from_proportion(0.5)
        r_ = T("C₂H₅O⁻ + C₂H₅I", size=24, color=OC).move_to([-4.2, -1.1, 0])
        p_ = T("C₂H₅OC₂H₅ + I⁻", size=24, color=th.MINT).move_to([4.1, -2.2, 0])
        tsl = chem(r"[C_2H_5O\cdots CH_2(CH_3)\cdots I]^{-\ddagger}", size=32, color=th.AMBER).move_to([0.6, 2.2, 0])
        ea = DoubleArrow([-3.0, -0.6, 0], [-3.0, top[1], 0], buff=0, color=th.AMBER, stroke_width=3, tip_length=0.18)
        eal = T("Ea", size=26, color=th.AMBER, weight="BOLD").next_to(ea, LEFT, buff=0.1)
        dl = DashedLine([-3.2, top[1], 0], top + LEFT * 0.1, color=th.FAINT, stroke_width=2)
        dot = Dot(curve.point_from_proportion(0), radius=0.12, color=th.AMBER)
        with self.say("Here is the same reaction on an energy diagram. Reactants on the left, products on the right, lower in energy. There is a single hump, because there is a single step. At the very top sits the transition state, with the oxygen and the iodine each half bonded to the same carbon. No intermediate, nowhere for the reaction to pause."):
            self.play(FadeIn(title), GrowArrow(ax), GrowArrow(ax2), FadeIn(el), FadeIn(xl))
            self.play(Create(curve), FadeIn(r_), run_time=1.6)
            self.add(dot)
            self.play(MoveAlongPath(dot, curve), run_time=2.5, rate_func=smooth)
            self.play(FadeIn(p_), FadeIn(tsl), Create(dl), GrowFromCenter(ea), FadeIn(eal))
        nb = C.show_neby(self, "think", height=1.3, corner=DR)
        with self.say("Anything that crowds the back of that carbon raises the hump. That is the key to the next step."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, ax, el, ax2, xl, curve, r_, p_, tsl, ea, eal, dl, dot)))

    def planning(self):
        title = T("Which partner is which? Making MTBE", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        tgt = chem(r"(CH_3)_3C{-}O{-}CH_3", size=46, color=ETH).next_to(title, DOWN, buff=0.35)
        good = VGroup(T("✓  bulky group as the alkoxide", size=30, color=th.MINT, weight="BOLD"),
                      chem(r"(CH_3)_3CONa + CH_3I \rightarrow (CH_3)_3COCH_3 + NaI", size=42, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 0.4, 0])
        bad = VGroup(T("✗  bulky group as the halide", size=30, color=th.CORAL, weight="BOLD"),
                     chem(r"CH_3ONa + (CH_3)_3CBr \rightarrow (CH_3)_2C{=}CH_2 + CH_3OH + NaBr", size=40, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -1.4, 0])
        with self.say("Every mixed ether can be cut two ways, and only one way works. Take M T B E, two methoxy two methylpropane. Route one: the bulky tertiary group as the alkoxide, and iodomethane as the halide. The methyl carbon is wide open at the back, so S N two goes smoothly."):
            self.play(FadeIn(title), Write(tgt))
            self.play(FadeIn(good, shift=UP * 0.2))
        with self.say("Route two: methoxide with tertiary butyl bromide. Now the back of the carbon is buried behind three methyl groups. The methoxide cannot reach it, so it acts as a base instead, and you get an alkene. Let's watch."):
            self.play(FadeIn(bad, shift=UP * 0.2))
        self.play(FadeOut(VGroup(good, bad, tgt)))
        # E2 animation
        c = np.array([1.2, -0.6, 0])
        cc = node("C", c, size=44)
        me1 = node("CH₃", c + np.array([0, 1.4, 0]), size=34)
        me2 = node("CH₃", c + np.array([0, -1.4, 0]), size=34)
        ch2 = node("CH₂", c + np.array([-1.9, 0, 0]), size=38)
        hh = node("H", c + np.array([-1.9, 1.35, 0]), color=C.EL["H"], size=34)
        br = node("Br", c + np.array([2.0, 0, 0]), color="#E07A5F", size=40)
        bcm1, bcm2 = bond(c, me1.get_center(), shrink=0.35), bond(c, me2.get_center(), shrink=0.35)
        bcc = bond(c, ch2.get_center(), shrink=0.42)
        bch = bond(ch2.get_center(), hh.get_center(), shrink=0.3)
        bbr = bond(c, br.get_center(), shrink=0.38)
        meo = node("CH₃O⁻", c + np.array([-4.6, 2.0, 0]), color=OC, size=36)
        sub = T("t-butyl bromide: the back of the C–Br carbon is blocked", size=24, color=th.BODY).to_edge(DOWN, buff=0.6)
        mol = VGroup(cc, me1, me2, ch2, hh, br, bcm1, bcm2, bcc, bch, bbr)
        with self.say("Here is tertiary butyl bromide. Three groups guard the carbon. The methoxide finds it much easier to grab a hydrogen from the outside of the molecule."):
            self.play(FadeIn(title), FadeIn(mol), FadeIn(sub))
            self.play(FadeIn(meo, shift=RIGHT * 0.3))
        a1 = push(meo.get_bottom() + RIGHT * 0.6, hh.get_left() + LEFT * 0.05, angle=TAU / 6, color=th.AMBER)
        a2 = push(bch.get_center() + RIGHT * 0.12, bcc.get_center() + UP * 0.12, angle=-TAU / 4, color=th.AMBER)
        a3 = push(bbr.get_center() + UP * 0.12, br.get_top() + UP * 0.05, angle=-TAU / 4, color=th.AMBER)
        e2 = T("E2: three arrows, one step", size=26, color=th.AMBER, weight="BOLD").move_to(sub)
        with self.say("Three curved arrows. The methoxide takes the hydrogen. The carbon hydrogen bond electrons swing in to make a carbon carbon double bond. And the carbon bromine bond breaks, bromide leaving. All in one step: elimination, E two."):
            self.play(Create(a1), FadeOut(sub), FadeIn(e2))
            self.play(Create(a2))
            self.play(Create(a3))
        dbl = bond(ch2.get_center() + UP * 0.14, c + UP * 0.14, color=th.MINT, w=5, shrink=0.42)
        brm = node("Br⁻", br.get_center() + RIGHT * 1.2 + DOWN * 0.3, color="#E07A5F", size=40)
        meoh = node("CH₃OH", meo.get_center() + RIGHT * 0.6, color=OC, size=36)
        pl = T("2-methylpropene: no ether at all", size=30, color=th.CORAL, weight="BOLD").move_to(e2)
        with self.say("The products: two methylpropene, methanol, and bromide. No ether at all."):
            self.play(FadeOut(VGroup(a1, a2, a3)), FadeOut(bch), FadeOut(hh, target_position=meo.get_center()), Transform(meo, meoh),
                      Create(dbl), FadeOut(bbr), Transform(br, brm), FadeOut(e2), run_time=1.5)
            self.play(FadeIn(pl))
            self.sfx("wrong", gain=-12)
        self.play(FadeOut(VGroup(mol, meo, dbl, pl, title)))
        title = T("Aromatic ethers: the ring must be the alkoxide", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ok = VGroup(benzene(r=0.65, subs={0: ("O⁻Na⁺", OC)}, label_size=24), T("+  CH₃I", size=34, color=th.INK), T("→ anisole ✓", size=34, color=th.MINT, weight="BOLD")).arrange(RIGHT, buff=0.4).move_to([0, 0.9, 0])
        no = VGroup(T("CH₃O⁻Na⁺  +", size=34, color=th.INK), benzene(r=0.65, subs={0: ("Cl", "#7BE495")}, label_size=26), T("→ no reaction ✗", size=34, color=th.CORAL, weight="BOLD")).arrange(RIGHT, buff=0.4).move_to([0, -1.4, 0])
        why = para("the C–Cl bond of a haloarene has partial double-bond character, and the ring blocks the back: no SN2", width=11, size=24, color=th.BODY, align="center").to_edge(DOWN, buff=0.45)
        with self.say("For an aromatic ether, the same logic. Sodium phenoxide plus iodomethane gives anisole. But methoxide plus chlorobenzene gives nothing at all. The ring carbon is s p two, its bond to chlorine has partial double bond character, and the ring itself blocks any backside attack."):
            self.play(FadeIn(title), FadeIn(ok, shift=UP * 0.2))
            self.play(FadeIn(no, shift=UP * 0.2))
            self.play(FadeIn(why))
        self.play(FadeOut(VGroup(title, ok, no, why)))
        self.tip("Williamson: make the BULKY or aryl group the alkoxide (RO⁻Na⁺), and the methyl or primary group the halide. Tertiary halide → alkene; haloarene → nothing.",
                 "Exam tip. In Williamson's synthesis, always make the bulky group, or the ring, the alkoxide, and the methyl or primary group the halide. A tertiary halide gives an alkene, and a haloarene gives nothing.")
        self.quiz("The best pair of reagents to make 2-methoxy-2-methylpropane is",
                  ["CH₃ONa + (CH₃)₃CBr", "(CH₃)₃CONa + CH₃I", "CH₃OH + (CH₃)₃COH", "CH₃Br + (CH₃)₃CBr"], 1,
                  "Your turn. Which pair is the right way to make M T B E?",
                  "B. The bulky tertiary butoxide is the nucleophile, and iodomethane, open at the back, takes the attack. Option A would give two methylpropene by elimination.")

    def dehydration(self):
        title = T("A second route: dehydrating an alcohol", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"2C_2H_5OH \xrightarrow{\text{conc. } H_2SO_4,\ 140^{\circ}C} C_2H_5OC_2H_5 + H_2O", size=46).move_to([0, 1.5, 0])
        mix = chem(r"ROH + R'OH \rightarrow ROR + ROR' + R'OR'", size=42, color=th.CORAL).move_to([0, -0.2, 0])
        cap = para("cheap and used industrially, but only for SIMPLE ethers: two different alcohols give a mixture of three ethers", width=10.5, size=26, color=th.BODY, align="center").move_to([0, -1.8, 0])
        with self.say("Recall from Unit 10: heat ethanol with concentrated sulphuric acid at one hundred and forty degrees, and two molecules share one water, giving diethyl ether. It is cheap and used in industry. But it only works for simple ethers. Mix two different alcohols and you get all three possible ethers, which are hard to separate."):
            self.play(FadeIn(title), Write(eq))
            self.play(Write(mix))
            self.play(FadeIn(cap))
        self.play(FadeOut(VGroup(title, eq, mix, cap)))
        head, prob = C.example_head(self, "6.8 g of sodium ethoxide is warmed with excess iodoethane. Find the mass and the volume of ethoxyethane at 75 % yield. (density 0.713 g cm⁻³; Na 23, C 12, H 1, O 16)")
        n = 6.8 / 68
        m = 0.75 * n * 74
        v = m / 0.713
        st = C.steps(r"M(\mathrm{C_2H_5ONa}) = 24 + 5 + 16 + 23 = 68;\ \ n = \tfrac{6.8}{68} = %.2f\ \mathrm{mol}" % n,
                     r"\text{theoretical: } %.2f \times 74 = %.1f\ \mathrm{g}" % (n, n * 74),
                     r"75\%%:\ m = 0.75 \times %.1f = %.2f\ \mathrm{g}" % (n * 74, m),
                     r"V = \tfrac{%.2f}{0.713} = %.2f\ \mathrm{cm^3}" % (m, v), size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example twelve point two. Sodium ethoxide has molar mass sixty eight, so six point eight grams is zero point one mole. Iodoethane is in excess, so the ethoxide limits the yield: zero point one mole of ether, molar mass seventy four, seven point four grams in theory. At seventy five percent, five point five five grams. Divide by the density, zero point seven one three, and the volume is seven point seven eight cubic centimetres."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        title = T("A bent, polar molecule", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        o = np.array([-3.0, 1.2, 0])
        t = ValueTracker(104.5)

        def shape():
            a = np.radians(t.get_value() / 2)
            L = 2.2
            l_ = o + L * np.array([-np.sin(a), -np.cos(a), 0])
            r_ = o + L * np.array([np.sin(a), -np.cos(a), 0])
            g = VGroup(Line(o, l_, color=th.MUTED, stroke_width=6), Line(o, r_, color=th.MUTED, stroke_width=6))
            g.add(Arc(radius=0.8, start_angle=-PI / 2 - a, angle=2 * a, arc_center=o, color=th.AMBER, stroke_width=4))
            return g
        sk = always_redraw(shape)
        oo = VGroup(Circle(radius=0.5, fill_color=OC, fill_opacity=1, stroke_width=0), T("O", size=40, color=WHITE, weight="BOLD")).move_to(o)
        lp = VGroup(lone_pair(o + UL * 0.25, UL * 0.8), lone_pair(o + UR * 0.25, UR * 0.8))
        a0 = np.radians(104.5 / 2)
        a1 = np.radians(111.7 / 2)
        hL = VGroup(Circle(radius=0.38, fill_color=C.EL["H"], fill_opacity=1, stroke_width=0), T("H", size=30, color=th.BG, weight="BOLD")).move_to(o + 2.2 * np.array([-np.sin(a0), -np.cos(a0), 0]))
        hR = hL.copy().move_to(o + 2.2 * np.array([np.sin(a0), -np.cos(a0), 0]))
        eL = VGroup(Circle(radius=0.62, fill_color=ETH, fill_opacity=1, stroke_width=0), T("C₂H₅", size=28, color=th.BG, weight="BOLD")).move_to(o + 2.2 * np.array([-np.sin(a1), -np.cos(a1), 0]))
        eR = eL.copy().move_to(o + 2.2 * np.array([np.sin(a1), -np.cos(a1), 0]))
        ang_lab = DecimalNumber(104.5, num_decimal_places=1, font_size=40, color=th.AMBER).move_to(o + DOWN * 1.35)
        ang_lab.add_updater(lambda m_: m_.set_value(t.get_value()).move_to(o + DOWN * 1.35))
        deg = T("°", size=36, color=th.AMBER)
        deg.add_updater(lambda m_: m_.next_to(ang_lab, RIGHT, buff=0.04).align_to(ang_lab, UP))
        facts = VGroup(T("O is sp³ with two lone pairs", size=26, color=th.INK),
                       T("C–O–C angle 111.7° (water 104.5°)", size=26, color=th.AMBER),
                       T("bulky ethyl groups push apart", size=26, color=th.BODY),
                       T("dipole moment 1.15 D", size=26, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.0, 0])
        with self.say("Start with the shape. The oxygen in an ether is s p three hybridised, with two lone pairs, just like the oxygen in water. In water the H O H angle is one hundred and four point five degrees."):
            self.play(FadeIn(title))
            self.add(sk)
            self.play(FadeIn(oo), FadeIn(lp), FadeIn(hL), FadeIn(hR), FadeIn(ang_lab), FadeIn(deg))
            self.play(FadeIn(facts[0]))
        with self.say("Swap the hydrogens for two bulky ethyl groups. They crowd each other and push apart, opening the angle to one hundred and eleven point seven degrees. The molecule is still bent, so the two carbon oxygen dipoles do not cancel. Ether is polar, with a dipole moment of one point one five debye."):
            self.play(Transform(hL, eL), Transform(hR, eR), t.animate.set_value(111.7), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[1:]], lag_ratio=0.4), run_time=2.0)
        deg.clear_updaters()
        ang_lab.clear_updaters()
        self.play(FadeOut(VGroup(title, oo, lp, hL, hR, facts, ang_lab, deg)), FadeOut(sk))
        self.remove(sk, ang_lab)
        # bp chart
        title = T("Boiling points of the C₄H₁₀O isomers", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        data = [("butan-1-ol", 117.7, th.SKY), ("2-methylpropan-1-ol", 107.9, th.SKY), ("butan-2-ol", 99.5, th.SKY), ("2-methylpropan-2-ol", 82.4, th.SKY),
                ("1-methoxypropane", 38.8, ETH), ("ethoxyethane", 34.6, ETH), ("2-methoxypropane", 30.8, ETH), ("pentane (M = 72)", 36.1, th.MUTED)]
        x0, sc = -2.2, 7.0 / 120
        bars = VGroup()
        for i, (nm, bp, col) in enumerate(data):
            yy = 1.9 - i * 0.55
            r = Rectangle(width=bp * sc, height=0.38, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([x0 + bp * sc / 2, yy, 0])
            ln = T(nm, size=22, color=col).next_to([x0, yy, 0], LEFT, buff=0.2)
            vl = T(f"{bp} °C", size=22, color=th.INK).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(r, ln, vl))
        gap = BraceBetweenPoints([x0 + 34.6 * sc, -2.3, 0], [x0 + 117.7 * sc, -2.3, 0], direction=DOWN, color=th.AMBER)
        gl = T("83 °C gap", size=26, color=th.AMBER, weight="BOLD").next_to(gap, DOWN, buff=0.08)
        with self.say("Now the boiling point puzzle, with all seven isomers of C four H ten O, plus pentane, an alkane of almost the same mass. The four alcohols boil between eighty two and one hundred and eighteen degrees. The three ethers all boil between thirty and thirty nine. And the ethers sit right next to pentane, which has no oxygen at all.") as v:
            self.play(FadeIn(title))
            for b_ in bars[:4]:
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[1]), FadeIn(b_[2]), run_time=0.5)
            for b_ in bars[4:]:
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[1]), FadeIn(b_[2]), run_time=0.5)
            self.play(GrowFromCenter(gap), FadeIn(gl))
        self.play(FadeOut(VGroup(title, bars, gap, gl)))
        self.hbonds()

    def hbonds(self):
        title = T("Solving the puzzle: who can hydrogen-bond?", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)

        def alcohol(p):
            o = np.array(p, dtype=float)
            return VGroup(Circle(radius=0.48, fill_color=th.SKY, fill_opacity=1, stroke_width=0).move_to(o + LEFT * 0.75),
                          T("C₄H₉", size=18, color=th.BG, weight="BOLD").move_to(o + LEFT * 0.75),
                          Circle(radius=0.3, fill_color=OC, fill_opacity=1, stroke_width=0).move_to(o),
                          Circle(radius=0.17, fill_color=C.EL["H"], fill_opacity=1, stroke_width=0).move_to(o + DR * 0.36))

        def ether(p):
            o = np.array(p, dtype=float)
            return VGroup(Circle(radius=0.42, fill_color=ETH, fill_opacity=1, stroke_width=0).move_to(o + LEFT * 0.65 + DOWN * 0.3),
                          Circle(radius=0.42, fill_color=ETH, fill_opacity=1, stroke_width=0).move_to(o + RIGHT * 0.65 + DOWN * 0.3),
                          Circle(radius=0.3, fill_color=OC, fill_opacity=1, stroke_width=0).move_to(o))
        al = VGroup(alcohol([-4.6, 1.1, 0]), alcohol([-3.4, 0.0, 0]), alcohol([-4.6, -1.1, 0]), alcohol([-3.4, -2.2, 0]))
        hb = VGroup(*[DashedLine(al[k][3].get_center(), al[k + 1][2].get_center(), color=th.AMBER, stroke_width=4, dash_length=0.08) for k in range(3)])
        et = VGroup(ether([2.2, 1.1, 0]), ether([4.4, 0.4, 0]), ether([2.4, -1.0, 0]), ether([4.6, -1.9, 0]))
        lal = T("butan-1-ol: O–H···O hydrogen bonds", size=24, color=th.SKY, weight="BOLD").move_to([-3.6, 2.3, 0])
        let = T("ether: no O–H, no H-bonds", size=24, color=ETH, weight="BOLD").move_to([3.4, 2.3, 0])
        with self.say("Here is the answer. Butan one ol has a hydrogen on its oxygen. That hydrogen reaches across to the oxygen of the next molecule, a hydrogen bond, and the molecules are tied together in chains. To boil the alcohol, you must break all those bonds."):
            self.play(FadeIn(title), FadeIn(al), FadeIn(lal))
            self.play(LaggedStart(*[Create(h) for h in hb], lag_ratio=0.3))
            self.sfx("pop")
        with self.say("An ether has oxygen, but no hydrogen on it. There is nothing to reach across with. Ether molecules are held only by weak dipole and dispersion forces, just like pentane. So they fly apart at thirty four point six degrees. That is the eighty three degree gap."):
            self.play(FadeIn(et), FadeIn(let))
            self.play(*[e.animate.shift(np.array([0.3 * (-1) ** k, 0.25, 0])) for k, e in enumerate(et)], rate_func=wiggle, run_time=1.5)
        nb = C.show_neby(self, "success", height=1.3, corner=DR)
        with self.say("Puzzle solved. Same atoms, but only one of them has a hydrogen to share."):
            self.wait(0.4)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(al, hb, et, lal, let)))
        # water solubility
        e = ether([-0.5, 0.2, 0])
        wt = VGroup(Circle(radius=0.3, fill_color=OC, fill_opacity=1, stroke_width=0), Circle(radius=0.17, fill_color=C.EL["H"], fill_opacity=1, stroke_width=0).shift(DL * 0.38),
                    Circle(radius=0.17, fill_color=C.EL["H"], fill_opacity=1, stroke_width=0).shift(DR * 0.38)).move_to([0.6, 1.9, 0])
        wt2 = wt.copy()
        lab = para("but water supplies the H, and the ether O ACCEPTS it: as soluble as butan-1-ol (6.5 g vs 7.9 g per 100 cm³)", width=6.0, size=26, color=th.SKY).move_to([3.6, -0.6, 0])
        e.move_to([-2.0, -0.4, 0])
        wt.move_to([-0.8, 1.2, 0])
        wt2.move_to([-3.3, 1.2, 0])
        hb1 = DashedLine(wt[1].get_center(), e[2].get_center(), color=th.AMBER, stroke_width=4, dash_length=0.08)
        hb2 = DashedLine(wt2[2].get_center(), e[2].get_center(), color=th.AMBER, stroke_width=4, dash_length=0.08)
        VGroup(e, wt, wt2, hb1, hb2).scale(1.35, about_point=np.array([-2.0, 0.3, 0]))
        with self.say("Then a twist. Ethers dissolve in water about as well as the alcohols do: six and a half grams per hundred, against seven point nine for butanol. Why? Because water brings its own hydrogens. The ether oxygen's lone pairs accept hydrogen bonds from water, even though the ether can never donate one."):
            self.play(FadeIn(e))
            self.play(FadeIn(wt, shift=DOWN * 0.2), FadeIn(wt2, shift=DOWN * 0.2))
            self.play(Create(hb1), Create(hb2))
            self.play(FadeIn(lab))
        self.play(FadeOut(VGroup(title, e, wt, wt2, hb1, hb2, lab)))
        title = T("Other physical properties", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cards = VGroup(C.card(self, "State", "CH₃OCH₃ and CH₃OC₂H₅ are gases; the rest are sweet-smelling liquids", w=4.1, h=2.8, color=th.SKY, tsize=26),
                       C.card(self, "Inflammable", "very volatile; the vapour is heavier than air, creeps along the bench and catches fire: no naked flames", w=4.1, h=2.8, color=th.CORAL, tsize=26),
                       C.card(self, "Light", "density of ethoxyethane 0.713 g cm⁻³: floats on water", w=4.1, h=2.8, color=th.MINT, tsize=26)).arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
        with self.say("A few more facts. Methoxymethane and methoxyethane are gases. The others are colourless, sweet smelling liquids. They are very volatile and very inflammable, and the heavy vapour creeps along the bench to the nearest flame. And ether is lighter than water, with a density of zero point seven one three."):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.35), run_time=2.0)
        self.play(FadeOut(VGroup(title, cards)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        title = T("Ethers are lazy", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        hub = chem(r"C_2H_5{-}O{-}C_2H_5", size=52, color=ETH).move_to([0, 0.6, 0])
        rs = ["Na metal", "NaOH", "KMnO₄", "reducing agents"]
        pos = [[-4.4, 1.9, 0], [4.4, 1.9, 0], [-4.4, -0.9, 0], [4.4, -0.9, 0]]
        items = VGroup()
        for r_, p_ in zip(rs, pos):
            tx = T(r_, size=32, color=th.MUTED, weight="BOLD").move_to(p_)
            x = Line(tx.get_left() + LEFT * 0.1, tx.get_right() + RIGHT * 0.1, color=th.CORAL, stroke_width=5)
            items.add(VGroup(tx, x))
        lb = para("but the O lone pairs make ether a weak LEWIS BASE: every reaction starts by grabbing H⁺", width=10, size=28, color=th.AMBER, align="center").move_to([0, -2.3, 0])
        with self.say("Ethers are remarkably unreactive. Sodium, alkalis, ordinary oxidising and reducing agents: nothing happens. That is why ether is such a good solvent. But the oxygen still has two lone pairs. That makes ether a weak Lewis base, and every reaction we study starts with the oxygen grabbing a proton."):
            self.play(FadeIn(title), Write(hub))
            self.play(LaggedStart(*[FadeIn(it[0]) for it in items], lag_ratio=0.2))
            self.play(LaggedStart(*[Create(it[1]) for it in items], lag_ratio=0.2))
            self.play(FadeIn(lb))
        self.play(FadeOut(VGroup(title, hub, items, lb)))
        self.hi_mech()
        self.hi_more()
        self.other_acids()
        self.peroxide()
        self.chlorine()

    def hi_mech(self):
        title = T("Cleavage by HI, step by step", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        y = -0.4
        o = np.array([-0.4, y, 0])
        cl_ = np.array([-2.4, y, 0])
        cr = np.array([1.4, y, 0])
        me = cr + np.array([0.6, 1.3, 0])
        L = node("C₂H₅", cl_, color=ETH, size=38)
        O = node("O", o, color=OC, size=44)
        CR = node("CH₂", cr, size=38)
        ME = node("CH₃", me, size=34)
        bL = bond(cl_, o, shrink=0.55)
        bR = bond(o, cr, shrink=0.42)
        bM = bond(cr, me, shrink=0.35)
        lp = lone_pair(o, UP)
        hp = node("H⁺", o + np.array([-0.2, 2.0, 0]), color=th.CORAL, size=36)
        s1 = T("1. the lone pair on O takes H⁺: a protonated ether (oxonium ion)", size=24, color=th.CORAL).to_edge(DOWN, buff=0.6)
        with self.say("Let us watch hydrogen iodide split diethyl ether. Step one. A lone pair on the oxygen reaches out and takes a proton from H I. The curved arrow starts at the lone pair and ends at the proton."):
            self.play(FadeIn(title), FadeIn(VGroup(L, O, CR, ME, bL, bR, bM)), FadeIn(lp))
            self.play(FadeIn(hp, shift=DOWN * 0.2))
            a1 = push(lp.get_center() + RIGHT * 0.12, hp.get_bottom() + RIGHT * 0.15, angle=-TAU / 4, color=th.AMBER)
            self.play(Create(a1), FadeIn(s1))
        hO = node("H", o + UP * 1.1, color=C.EL["H"], size=36)
        bH = bond(o, hO.get_center(), shrink=0.3)
        pls = T("+", size=34, color=th.CORAL, weight="BOLD").move_to(o + np.array([0.38, 0.35, 0]))
        with self.say("Now the oxygen carries three bonds and a positive charge: an oxonium ion. A positive oxygen pulls hard on its electrons, which makes the carbon oxygen bond weak, and the neighbouring carbon slightly positive."):
            self.play(FadeOut(a1), FadeOut(lp), Transform(hp, hO), Create(bH), FadeIn(pls), run_time=1.2)
            self.play(Indicate(bR, color=th.CORAL, scale_factor=1.0))
        iod = node("I⁻", cr + np.array([2.4, -0.2, 0]), color=IC, size=40)
        s2 = T("2. I⁻ attacks the back of the carbon (SN2); the C–O bond breaks", size=24, color=IC).to_edge(DOWN, buff=0.6)
        with self.say("Step two. The iodide ion, a very good nucleophile, attacks that carbon from the back, opposite the oxygen. As the carbon iodine bond forms, the carbon oxygen bond breaks, and its electron pair moves onto the oxygen. S N two again."):
            self.play(FadeIn(iod), FadeOut(s1), FadeIn(s2))
            a2 = push(iod.get_left() + LEFT * 0.05, CR.get_right() + RIGHT * 0.05, angle=-TAU / 5, color=th.AMBER)
            a3 = push(bR.get_center() + DOWN * 0.1, O.get_bottom() + DOWN * 0.05, angle=-TAU / 4, color=th.AMBER)
            self.play(Create(a2))
            self.play(Create(a3))
        alc = VGroup(L, O, bL, hp, bH)
        bI = bond(cr, cr + RIGHT * 1.4, shrink=0.42)
        lab1 = T("ethanol", size=28, color=th.MINT, weight="BOLD").move_to([-1.6, -1.6, 0])
        lab2 = T("iodoethane", size=28, color=IC, weight="BOLD").move_to([2.6, -1.6, 0])
        with self.say("The bond snaps. One half leaves as ethanol, the other becomes iodoethane. With one mole of cold H I, that is where it stops."):
            self.play(FadeOut(a2), FadeOut(a3), FadeOut(bR), FadeOut(pls), alc.animate.shift(LEFT * 0.8), iod.animate.move_to(cr + RIGHT * 1.4), run_time=1.0)
            self.play(Create(bI), Transform(iod, node("I", cr + RIGHT * 1.4, color=IC, size=40)), FadeIn(lab1), FadeIn(lab2))
            self.sfx("pop")
        self.play(FadeOut(VGroup(alc, CR, ME, bM, iod, bI, lab1, lab2, s2)))
        e1 = chem(r"C_2H_5OC_2H_5 + HI \xrightarrow{\text{cold}} C_2H_5OH + C_2H_5I", size=42, color=th.SKY).move_to([0, 1.4, 0])
        e2 = chem(r"C_2H_5OH + HI \xrightarrow{\text{hot}} C_2H_5I + H_2O", size=42, color=th.MUTED).move_to([0, 0.3, 0])
        ln = Line([-4.5, -0.3, 0], [4.5, -0.3, 0], color=th.FAINT)
        e3 = chem(r"C_2H_5OC_2H_5 + 2HI \xrightarrow{\text{hot, excess}} 2C_2H_5I + H_2O", size=42, color="#5C8DFF").move_to([0, -1.0, 0])
        ord_ = T("reactivity: HI > HBr > HCl (iodide is the best nucleophile)", size=26, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("With hot, excess H I, the ethanol formed is itself converted into iodoethane, by the same two steps. Add the two equations, and one ether plus two H I gives two iodoethane and water. Hydrogen iodide works best, then hydrogen bromide, then hydrogen chloride, following how good the halide ion is as a nucleophile."):
            self.play(FadeIn(title), Write(e1))
            self.play(Write(e2))
            self.play(Create(ln), Write(e3))
            self.play(FadeIn(ord_))
        self.play(FadeOut(VGroup(title, e1, e2, ln, e3, ord_)))
        with self.say("Two spokes on our ether reaction map: cold H I, and hot excess H I."):
            g = self.rmap.show(self, [], ["hic", "hih"])
        self.play(FadeOut(g))

    def hi_more(self):
        head, prob = C.example_head(self, "7.4 g of ethoxyethane is heated with excess HI. Find the masses of iodoethane and water. What forms, and how much, with only 0.10 mol of cold HI? (I = 126.9)")
        n = 7.4 / 74
        Mi = 24 + 5 + 126.9
        st = C.steps(r"n(\mathrm{ether}) = \tfrac{7.4}{74} = %.2f\ \mathrm{mol}" % n,
                     r"\text{hot, excess: } m(\mathrm{C_2H_5I}) = 2 \times %.2f \times %.1f = %.1f\ \mathrm{g}" % (n, Mi, 2 * n * Mi),
                     r"m(\mathrm{H_2O}) = %.2f \times 18 = %.1f\ \mathrm{g}" % (n, n * 18),
                     r"\text{cold, 1 mol HI: } %.2f \times 46 = %.1f\ \mathrm{g\ C_2H_5OH},\ \ %.2f \times %.1f = %.1f\ \mathrm{g\ C_2H_5I}" % (n, n * 46, n, Mi, n * Mi), size=34).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[1].set_color(th.SKY)
        st[2].set_color(th.SKY)
        st[3].set_color(th.AMBER)
        with self.say("Worked example twelve point three. Seven point four grams of ether is zero point one mole. Iodoethane has molar mass one hundred fifty five point nine. Hot and excess: two moles of iodoethane per mole of ether, so thirty one point two grams, plus one point eight grams of water. Cold, with only one mole of H I per mole: four point six grams of ethanol and fifteen point six grams of iodoethane."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        # anisole
        title = T("Anisole + HI: which bond breaks?", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ring = benzene([-3.2, -0.8, 0], r=1.0, label_size=30)
        top = ring.verts[0]
        o = top + UP * 0.9
        O = node("O", o, color=OC, size=42)
        bO = bond(top, o, shrink=0.25)
        me = o + RIGHT * 1.6
        ME = node("CH₃", me, size=38)
        bM = bond(o, me, shrink=0.48)
        hO = node("H", o + UP * 0.95, color=C.EL["H"], size=34)
        bH = bond(o, hO.get_center(), shrink=0.3)
        pls = T("+", size=30, color=th.CORAL, weight="BOLD").move_to(o + np.array([-0.4, 0.35, 0]))
        iod = node("I⁻", me + RIGHT * 2.0, color=IC, size=40)
        iod2 = node("I⁻", top + np.array([0.9, -2.4, 0]), color=IC, size=40)
        with self.say("Now the most tested reaction in this unit. Anisole, methoxybenzene, with H I. The oxygen is protonated as before. Now the iodide must choose: attack the methyl carbon, or the ring carbon?"):
            self.play(FadeIn(title), Create(ring), FadeIn(VGroup(O, bO, ME, bM)))
            self.play(FadeIn(hO), Create(bH), FadeIn(pls))
            self.play(FadeIn(iod), FadeIn(iod2))
        a_bad = push(iod2.get_top() + UP * 0.05, top + DOWN * 0.15 + RIGHT * 0.05, angle=TAU / 8, color=th.CORAL)
        xx = Cross(scale_factor=0.25, stroke_color=th.CORAL, stroke_width=6).move_to(a_bad.point_from_proportion(0.5))
        why = para("ring carbon: sp², C–O has partial double-bond character, the ring blocks the back", width=4.8, size=24, color=th.CORAL).move_to([3.3, -2.0, 0])
        with self.say("The ring carbon is s p two. Its bond to oxygen has partial double bond character, from the lone pair spreading into the ring, and the ring itself blocks the back of that carbon. So no attack there."):
            self.play(Create(a_bad))
            self.play(Create(xx), FadeIn(why))
            self.sfx("wrong", gain=-12)
        a_ok = push(iod.get_left() + LEFT * 0.05, ME.get_right() + RIGHT * 0.05, angle=-TAU / 5, color=th.MINT)
        a_b = push(bM.get_center() + DOWN * 0.1, O.get_bottom() + DOWN * 0.05, angle=-TAU / 4, color=th.MINT)
        with self.say("The methyl carbon is s p three, small and open at the back. The iodide attacks there, and the methyl oxygen bond breaks."):
            self.play(Create(a_ok), Create(a_b))
        eq = chem(r"C_6H_5OCH_3 + HI \rightarrow C_6H_5OH + CH_3I", size=42, color=th.MINT).to_edge(DOWN, buff=0.5)
        res = VGroup(T("phenol", size=30, color=th.MINT, weight="BOLD"), T("+ iodomethane", size=30, color=IC, weight="BOLD")).arrange(RIGHT, buff=0.3).move_to([2.8, -0.6, 0])
        with self.say("So anisole gives phenol and iodomethane. Never iodobenzene and methanol. That is the classic exam error."):
            self.play(FadeOut(VGroup(a_bad, xx, why, a_ok, a_b)), FadeOut(bM), FadeOut(pls), ME.animate.shift(RIGHT * 0.6), iod.animate.move_to(me + RIGHT * 1.7), run_time=1.0)
            ch3i = node("CH₃I", me + RIGHT * 0.9, color=IC, size=38)
            self.play(FadeOut(iod2), FadeOut(ME), FadeOut(iod), FadeIn(ch3i), FadeIn(res), Write(eq))
        nb = C.show_neby(self, "wink", height=1.3, corner=DR)
        self.wait(0.6)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, ring, O, bO, ch3i, hO, bH, eq, res)))
        head, prob = C.example_head(self, "10.8 g of anisole is refluxed with excess HI. Name and find the mass of each organic product. (I = 126.9)")
        n = 10.8 / 108
        st = C.steps(r"M(\mathrm{C_7H_8O}) = 84 + 8 + 16 = 108;\ \ n = \tfrac{10.8}{108} = %.2f\ \mathrm{mol}" % n,
                     r"\text{phenol: } %.2f \times 94 = %.1f\ \mathrm{g}" % (n, n * 94),
                     r"\text{iodomethane: } %.2f \times 141.9 = %.1f\ \mathrm{g}" % (n, n * 141.9), size=38).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[1].set_color(th.MINT)
        st[2].set_color(IC)
        with self.say("Worked example twelve point four. Anisole, C seven H eight O, has molar mass one hundred and eight, so ten point eight grams is zero point one mole. One mole gives one mole of each product. Phenol: nine point four grams. Iodomethane, molar mass one hundred forty one point nine: fourteen point two grams. And no iodobenzene."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("Anisole refluxed with excess HI gives",
                  ["iodobenzene + methanol", "phenol + iodomethane", "benzene + iodomethane", "phenol + methanol"], 1,
                  "Lock it in. What does anisole give with hydrogen iodide?",
                  "B, phenol and iodomethane. Only the s p three methyl carbon can take the backside attack, so the ring to oxygen bond survives.")

    def other_acids(self):
        title = T("Cold acid dissolves it; hot acid cuts it", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ox = chem(r"(C_2H_5)_2\ddot{O} + H^+ \rightarrow (C_2H_5)_2\overset{+}{O}{-}H", size=46, color=th.AMBER).move_to([0, 1.7, 0])
        rows = VGroup(
            VGroup(T("conc. HCl, cold", size=26, color=th.MINT, weight="BOLD"), chem(r"\rightarrow [(C_2H_5)_2OH]^+Cl^-", size=38, color=th.MINT)),
            VGroup(T("conc. HCl, heat + pressure", size=26, color=th.LIME, weight="BOLD"), chem(r"\rightarrow 2C_2H_5Cl + H_2O", size=38, color=th.LIME)),
            VGroup(T("conc. H₂SO₄, cold", size=26, color=th.AMBER, weight="BOLD"), chem(r"\rightarrow [(C_2H_5)_2OH]^+HSO_4^-", size=38, color=th.AMBER)),
            VGroup(T("conc. H₂SO₄, heat", size=26, color="#F08A24", weight="BOLD"), chem(r"+\,H_2SO_4 \rightarrow 2C_2H_5HSO_4 + H_2O", size=38, color="#F08A24")))
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.9, 0])
        with self.say("Hydrochloric and sulphuric acids behave the same way, only less vigorously. In the cold, concentrated acid simply protonates the oxygen. The ether dissolves in the acid as an oxonium salt. This is the clearest proof that ether is a base. Dilute with water, and the ether separates out again."):
            self.play(FadeIn(title), Write(ox))
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        with self.say("Heat it, and the carbon oxygen bonds are broken. Hot hydrochloric acid under pressure gives chloroethane. Hot sulphuric acid gives ethyl hydrogen sulphate."):
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
        self.play(FadeOut(VGroup(title, ox, rows)))
        with self.say("Four more spokes: the two oxonium salts, chloroethane, and ethyl hydrogen sulphate."):
            g = self.rmap.show(self, ["hic", "hih"], ["hclc", "hclh", "so4c", "so4h"], run_time=0.5)
        self.play(FadeOut(g))

    def peroxide(self):
        title = T("Air + light: the peroxide danger", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"C_2H_5OC_2H_5 + O_2 \xrightarrow{\text{air, light, slow}} CH_3CH(OOH)OC_2H_5", size=42, color=th.CORAL).next_to(title, DOWN, buff=0.35)
        fl = C.Flask(center=[-3.6, -0.9, 0], scale=1.9, color=ETH, opacity=0.45)
        heat = T("distilling…", size=24, color=th.AMBER).next_to(fl.g, DOWN, buff=0.2)
        lvl = T("ether boils off; the peroxide stays and concentrates", size=24, color=th.BODY).move_to([2.4, -0.4, 0])
        boom = Star(n=10, outer_radius=1.2, inner_radius=0.6, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).move_to(fl.g.get_center())
        bt = T("near dryness: EXPLOSION", size=30, color=th.CORAL, weight="BOLD").move_to([2.4, -1.4, 0])
        with self.say("Leave ether standing in air and light for months, and it slowly takes up oxygen at the carbon next to the oxygen, forming a hydroperoxide. The peroxide does not evaporate. When the old ether is distilled, the ether boils away, the peroxide concentrates in the flask, and near dryness it explodes."):
            self.play(FadeIn(title), Write(eq))
            self.play(FadeIn(fl.g), FadeIn(heat))
            self.play(FadeIn(lvl))
            self.play(fl.liq.animate.stretch(0.4, 1, about_edge=DOWN).set_fill(th.CORAL, opacity=0.85), run_time=1.4)
            self.sfx("thud", gain=-8)
            self.play(GrowFromCenter(boom), FadeIn(bt), run_time=0.4)
            self.play(FadeOut(boom), run_time=0.6)
        self.play(FadeOut(VGroup(fl.g, heat, lvl, bt)))
        tests = VGroup(C.card(self, "Test 1", "shake with acidified KI: I₂ is freed, blue with starch", w=3.8, h=2.2, color=th.SKY),
                       C.card(self, "Test 2", "FeSO₄ + KSCN: Fe²⁺ oxidised to Fe³⁺, blood-red colour", w=3.8, h=2.2, color=th.CORAL),
                       C.card(self, "Prevent", "dark bottles, over sodium wire or iron; never distil to dryness", w=3.8, h=2.2, color=th.MINT)).arrange(RIGHT, buff=0.35).move_to([0, -0.9, 0])
        with self.say("Peroxides are detected two ways. Shake with acidified potassium iodide: iodine is freed, blue with starch. Or add iron two sulphate and thiocyanate: the iron is oxidised, and you get a blood red colour. Prevent them by storing ether in dark bottles over sodium wire, and never distil ether to dryness."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in tests], lag_ratio=0.4), run_time=2.0)
        self.play(FadeOut(VGroup(title, eq, tests)))

    def chlorine(self):
        title = T("Chlorine: the α-hydrogens go first", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        f = chem(r"CH_3{-}CH_2{-}O{-}CH_2{-}CH_3", size=56).move_to([0, 1.2, 0])
        al = VGroup(SurroundingRectangle(f[0][4:7], color=PINK, buff=0.08), SurroundingRectangle(f[0][10:13], color=PINK, buff=0.08))
        alt = T("α-carbons, next to O", size=24, color=PINK).next_to(al, UP, buff=0.15)
        d = chem(r"+\,2Cl_2 \xrightarrow{\text{dark}} CH_3CHCl{-}O{-}CHClCH_3 + 2HCl", size=40, color=PINK).move_to([0, -0.5, 0])
        s_ = chem(r"+\,10Cl_2 \xrightarrow{\text{sunlight}} C_2Cl_5OC_2Cl_5 + 10HCl", size=40, color=th.TEAL).move_to([0, -1.8, 0])
        with self.say("Last reaction: chlorine substitutes hydrogen. In the dark, it is selective. Only the alpha hydrogens, on the carbons next to oxygen, are replaced, giving the alpha, alpha dichloro ether. In bright sunlight, every hydrogen goes: perchloro diethyl ether, with ten molecules of chlorine."):
            self.play(FadeIn(title), Write(f))
            self.play(Create(al), FadeIn(alt))
            self.play(Write(d))
            self.play(Write(s_))
        self.play(FadeOut(VGroup(title, f, al, alt, d, s_)))
        with self.say("Three final spokes: the peroxide, and the two chloro ethers. The whole chemistry of ether, on one page."):
            g = self.rmap.show(self, ["hic", "hih", "hclc", "hclh", "so4c", "so4h"], ["o2", "cld", "cls"], run_time=0.5)
        self.play(FadeOut(g))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("What ether is used for", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cs = [("Solvent", "fats, oils, waxes, resins, alkaloids; 'ether extraction' from water", th.SKY),
              ("Grignard reagents", "made and used in dry ether: its O lone pairs hold Mg in solution", th.MINT),
              ("Anaesthetic", "the first general anaesthetic (1846); now replaced by safer agents", ETH),
              ("Refrigerant", "and a starting fluid for diesel engines in the cold", "#5C8DFF"),
              ("Smokeless powder", "ether–alcohol mixture used to make cordite", th.CORAL),
              ("MTBE", "petrol anti-knock additive, replacing tetraethyl lead", th.AMBER)]
        cards = VGroup(*[C.card(self, a, b, w=4.1, h=2.35, color=c_, tsize=26) for a, b, c_ in cs]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).move_to([0, -0.45, 0])
        with self.say("Finally, uses. Ether is an excellent solvent for fats, oils, waxes and resins, and is used to extract organic compounds from water, because it is unreactive and boils off easily. Grignard reagents are made in dry ether. The ether oxygen donates its lone pairs to the magnesium and keeps it in solution.") as v:
            self.play(FadeIn(title))
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        with self.say("And our cold open: ether was the first general anaesthetic, in eighteen forty six. It works, but it is so inflammable that operating theatres switched to safer agents. Ether is also used as a refrigerant, to start diesel engines in cold weather, and to make smokeless powder. A close cousin, M T B E, is blended into petrol as an anti knock agent instead of poisonous lead."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards[3:]], lag_ratio=0.4), run_time=2.0)
        nb = C.show_neby(self, "success", height=1.3, corner=DR)
        self.wait(0.6)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, cards)))
        # separating funnel extraction
        title = T("Ether extraction", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        fun = VGroup(Polygon([-1.2, 1.4, 0], [1.2, 1.4, 0], [0.15, -1.6, 0], [-0.15, -1.6, 0], stroke_color=th.MUTED, stroke_width=4),
                     Line([0, -1.6, 0], [0, -2.5, 0], color=th.MUTED, stroke_width=4)).move_to([-2.6, -0.3, 0])
        top_l = Polygon([-1.05, 1.2, 0], [1.05, 1.2, 0], [0.62, -0.05, 0], [-0.62, -0.05, 0], fill_color=ETH, fill_opacity=0.5, stroke_width=0)
        bot_l = Polygon([-0.62, -0.05, 0], [0.62, -0.05, 0], [0.15, -1.45, 0], [-0.15, -1.45, 0], fill_color=C.WATER, fill_opacity=0.45, stroke_width=0)
        liq = VGroup(top_l, bot_l).move_to(fun[0].get_center() + DOWN * 0.07)
        dots = VGroup(*[Dot(bot_l.get_center() + np.array([0.25 * np.cos(k * 2.1), -0.35 + 0.18 * np.sin(k * 1.7), 0]), radius=0.07, color=th.AMBER) for k in range(6)])
        VGroup(fun, liq, dots).scale(1.35, about_point=fun.get_center()).move_to([-3.4, -0.4, 0])
        tl = T("ether layer (0.713 g cm⁻³) on top", size=26, color=ETH).move_to([2.6, 0.9, 0])
        bl = T("water layer below", size=26, color=C.WATER).move_to([2.6, -0.6, 0])
        dl = para("the organic compound moves into the ether; the ether is then boiled off at 35 °C", width=5.6, size=24, color=th.AMBER).move_to([2.6, -2.0, 0])
        with self.say("Here is ether extraction in a separating funnel. Ether does not mix much with water, and it floats on top. Shake, and the organic compound moves out of the water into the ether. Run off the water, then evaporate the ether at about thirty five degrees, and the compound is left behind."):
            self.play(FadeIn(title), Create(fun), FadeIn(liq), FadeIn(dots))
            self.play(FadeIn(tl), FadeIn(bl))
            self.play(fun.animate.rotate(0.15), liq.animate.rotate(0.15, about_point=fun.get_center()), dots.animate.rotate(0.15, about_point=fun.get_center()), run_time=0.4)
            self.play(fun.animate.rotate(-0.15), liq.animate.rotate(-0.15, about_point=fun.get_center()), dots.animate.rotate(-0.15, about_point=fun.get_center()), run_time=0.4)
            self.play(*[d_.animate.move_to(top_l.get_center() + np.array([0.3 * np.cos(k * 2.1), 0.25 * np.sin(k * 1.7), 0])) for k, d_ in enumerate(dots)], run_time=1.4)
            self.play(FadeIn(dl))
        self.play(FadeOut(VGroup(title, fun, liq, dots, tl, bl, dl)))
        with self.say("Here is the complete reaction map of diethyl ether. Notice that every reaction begins at the oxygen lone pairs, and that cold conditions give oxonium salts or break one bond, while hot conditions break both."):
            g = self.rmap.show(self, [k for k, *_ in MAP], [])
            self.wait(2)
        self.play(FadeOut(g))
        self.tip("Cold acid + ether → oxonium salt (dissolves). Hot excess HI → 2 RI + H₂O. Anisole + HI → phenol + CH₃I, never iodobenzene.",
                 "Exam tip. Cold concentrated acid only dissolves ether as an oxonium salt. Hot excess hydrogen iodide breaks both bonds, giving two iodoalkanes and water. And anisole with H I always gives phenol and iodomethane.", state="read")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Ether R–O–R′, CₙH₂ₙ₊₂O: a functional isomer of an alcohol; simple or mixed.",
            "IUPAC: smaller group + O = alkoxy (CH₃OC₂H₅ is methoxyethane).",
            "Metamerism: carbons shared differently about O (1 + 3 vs 2 + 2).",
            "Williamson: RO⁻Na⁺ + R′X, SN2; bulky or aryl group must be the alkoxide.",
            "No O–H, no self H-bonding: ether boils 83 °C below butan-1-ol, yet dissolves in water.",
            "Lewis base: cold acid → oxonium salt; hot excess HI → 2 RI + H₂O.",
            "Anisole + HI → phenol + CH₃I; air → explosive peroxide; Cl₂ dark → α-chloro.",
        ], "Let us recap. An ether is R O R dash, an isomer of an alcohol, simple or mixed. The smaller group is named as alkoxy. Ethers show metamerism. Williamson's synthesis is an S N two reaction, so the bulky group must be the alkoxide. With no O H, ethers cannot hydrogen bond to each other and boil low, yet dissolve in water. The oxygen is a Lewis base: cold acids give oxonium salts, hot H I breaks both bonds. Anisole gives phenol and iodomethane. Old ether forms explosive peroxides, and chlorine replaces the alpha hydrogens first.")
        self.outro("That is ethers. Next, we meet the carbonyl group, a carbon oxygen double bond, in the aldehydes and ketones. See you in the next lesson on NEBians.")
