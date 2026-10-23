import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

PALE_BLUE = "#8EC9F0"
ROYAL = "#2F4FE0"
CU_COL = "#D9824B"
METALS = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
CONF = [(1, 2), (2, 2), (3, 2), (5, 1), (5, 2), (6, 2), (7, 2), (8, 2), (10, 1), (10, 2)]


def box_row(n, w=0.42, h=0.46, color=th.MUTED):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=2) for _ in range(n)]).arrange(RIGHT, buff=0)


def spin(up=True, color=th.AMBER, h=0.34):
    a = Arrow(DOWN * h / 2, UP * h / 2, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.35)
    return a if up else a.rotate(PI)


def fill(boxes, electrons, color=th.AMBER, order=None, h=0.34, off=0.08):
    """Hund filling of `electrons` into a row of boxes; returns VGroup of arrows positioned in the boxes."""
    n = len(boxes)
    g = VGroup()
    idx = order or list(range(n))
    for k in range(electrons):
        b = idx[k % n] if k < 2 * n else None
        if b is None:
            break
        first = k < n
        a = spin(first, color, h=h)
        a.move_to(boxes[b].get_center() + (LEFT * off if first else RIGHT * off))
        g.add(a)
    return g


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 6
    TITLE = "Transition Metals"
    SUBTITLE = "d electrons: colour, complexes and catalysis"
    SECTIONS = ["Characteristics", "Oxidation states", "Complex ions", "Shapes of complex ions",
                "Crystal field theory", "Why they are coloured", "Catalytic properties"]
    NEXT = "Unit 7 · Studies of Heavy Metals"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        b1 = C.Beaker(center=[-3.2, -1.0, 0], w=2.6, h=2.8, level=0.65, color=PALE_BLUE, opacity=0.55)
        b2 = C.Beaker(center=[3.2, -1.0, 0], w=2.6, h=2.8, level=0.65, color="#E6E9F2", opacity=0.12)
        l1 = chem(r"CuSO_4(aq)", size=36, color=PALE_BLUE).next_to(b1.g, DOWN, buff=0.25)
        l2 = chem(r"ZnSO_4(aq)", size=36, color=th.BODY).next_to(b2.g, DOWN, buff=0.25)
        with self.say("Two beakers. Copper sulphate on the left, zinc sulphate on the right. Copper and zinc sit side by side in the periodic table, and both salts are sulphates. Yet one solution is blue, and the other has no colour at all."):
            self.play(FadeIn(b1.g, shift=UP * 0.3), FadeIn(l1))
            self.play(FadeIn(b2.g, shift=UP * 0.3), FadeIn(l2))
        drops = VGroup(*[Circle(radius=0.09, fill_color=WHITE, fill_opacity=0.8, stroke_width=0).move_to([-3.2 + 0.25 * (k - 1), 2.8, 0]) for k in range(3)])
        nh3 = chem(r"+\ NH_3(aq)", size=34).next_to(drops, RIGHT, buff=0.3)
        with self.say("Now add ammonia to the copper sulphate. Watch."):
            self.play(FadeIn(drops), FadeIn(nh3))
            self.play(drops.animate.shift(DOWN * 3.0).set_opacity(0), run_time=0.8, rate_func=rate_functions.ease_in_quad)
            self.sfx("impact", gain=-10)
            self.play(b1.liq.animate.set_fill(ROYAL, opacity=0.85), FadeOut(nh3), run_time=2.0)
        nb = C.show_neby(self, "surprised", height=1.5, at=[0, 1.2, 0])
        q = para("Why is copper coloured and zinc not? Why does ammonia deepen the blue?", width=6.5, size=28, color=th.INK).to_edge(UP, buff=0.5)
        with self.say("The pale blue turns a deep royal blue. Why is copper coloured and zinc not? And how can adding a colourless liquid make the colour deeper? The answer lies in five d orbitals, and how they split apart. By the end of this lesson you will be able to explain both."):
            self.play(FadeIn(q))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(b1.g, b2.g, l1, l2, q, drops)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 6: Transition Metals. The d block: metals with many oxidation states, beautiful colours, complex ions, and the power to catalyse half of industry."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. The characteristics of transition metals, and their oxidation states. Complex ions, and their shapes. Then crystal field theory, which explains why transition metal compounds are coloured. And finally, their catalytic properties.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        d = self.callout("key", "Transition element: an element whose atom, or one of whose common ions, has a partially filled d subshell.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("A transition element is one whose atom, or one of whose common ions, has a partially filled d subshell. In the first series, that runs from scandium to zinc."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        cards = VGroup()
        for i, (sym, (dn, sn)) in enumerate(zip(METALS, CONF)):
            box = self.panel(1.22, 1.6, color=th.PANEL_EDGE)
            s = T(sym, size=34, color=th.INK, weight="BOLD")
            z = T(str(21 + i), size=18, color=th.MUTED)
            c = M(r"3d^{" + str(dn) + r"}4s^{" + str(sn) + "}", size=30, color=th.SKY)
            VGroup(z, s, c).arrange(DOWN, buff=0.08).move_to(box)
            cards.add(VGroup(box, z, s, c))
        cards.arrange(RIGHT, buff=0.1).next_to(d, DOWN, buff=0.5)
        with self.say("Here they are, with their electron configurations after the argon core. The 3d subshell fills one electron at a time, from one in scandium to ten in zinc.") as v:
            for cd in cards:
                self.play(FadeIn(cd, shift=UP * 0.2), run_time=0.3)
                self.hold(v.dur / 10 - 0.35)
        self.play(FadeOut(d), cards.animate.to_edge(UP, buff=0.8))
        for k in (3, 8):
            self.play(Indicate(cards[k], color=th.AMBER, scale_factor=1.08), run_time=0.6)
        dbox = box_row(5, w=0.7, h=0.75).move_to([-1.2, -0.9, 0])
        sbox = box_row(1, w=0.7, h=0.75).next_to(dbox, RIGHT, buff=0.8)
        dl = T("3d", size=26, color=th.SKY).next_to(dbox, DOWN, buff=0.15)
        sl = T("4s", size=26, color=th.MINT).next_to(sbox, DOWN, buff=0.15)
        expect = VGroup(*[spin(True, th.AMBER, h=0.55).move_to(dbox[k].get_center() + LEFT * 0.12) for k in range(4)])
        s_pair = VGroup(spin(True, th.MINT, h=0.55).move_to(sbox.get_center() + LEFT * 0.12), spin(False, th.MINT, h=0.55).move_to(sbox.get_center() + RIGHT * 0.12))
        name = T("chromium", size=28, color=th.AMBER, weight="BOLD").next_to(VGroup(dbox, sbox), UP, buff=0.4)
        with self.say("Two break the pattern. Chromium should be 3d four, 4s two. Instead one 4s electron moves into the d subshell, making 3d five, 4s one: a half filled d subshell, which is extra stable."):
            self.play(FadeIn(name), Create(dbox), Create(sbox), FadeIn(dl), FadeIn(sl))
            self.play(FadeIn(expect), FadeIn(s_pair))
            jump = s_pair[1]
            self.play(jump.animate.rotate(PI).move_to(dbox[4].get_center() + LEFT * 0.12), run_time=1.0)
            self.play(Flash(dbox, color=th.AMBER, flash_radius=1.6))
        cu = T("copper: 3d¹⁰ 4s¹, a completely filled d subshell", size=28, color=CU_COL).next_to(VGroup(dbox, sbox), DOWN, buff=0.7)
        with self.say("Copper does the same, ending as 3d ten, 4s one, a completely filled d subshell."):
            self.play(FadeIn(cu))
        self.play(FadeOut(VGroup(dbox, sbox, dl, sl, expect, s_pair, name, cu)))
        zn = T("Zn: 3d¹⁰ in atom and in Zn²⁺, so not a typical transition metal", size=26, color=th.CORAL).next_to(cards, DOWN, buff=0.4)
        with self.say("Zinc is the odd one. Its atom is 3d ten, and its only ion, zinc two plus, is still 3d ten. No partly filled d subshell anywhere, so zinc is not a typical transition metal, and that is the first clue to our cold open."):
            self.play(Indicate(cards[9], color=th.CORAL, scale_factor=1.08), FadeIn(zn))
        self.play(FadeOut(VGroup(cards, zn)))
        title = T("Characteristic properties", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        props = [("Hard, high melting", "unpaired d electrons join the metallic bond. W melts at 3410 °C; Zn only 420 °C.", th.AMBER),
                 ("Dense", "small atoms, heavy nuclei.", th.MUTED),
                 ("Variable oxidation states", "4s and 3d are close in energy.", th.SKY),
                 ("Coloured ions", "d–d transitions (part 6).", th.PINK),
                 ("Paramagnetic", "unpaired electrons: μ = √(n(n+2)) BM.", th.MINT),
                 ("Complexes", "small, charged ions with vacant d orbitals.", th.CORAL),
                 ("Catalysts", "variable states and active surfaces.", th.LIME),
                 ("Alloys", "similar radii: steel, brass, bronze.", th.SKY),
                 ("Interstitial compounds", "H, C, N fill lattice holes: steel, TiC.", th.AMBER)]
        cards = VGroup(*[C.card(self, a, b, w=4.0, h=1.75, color=c, tsize=24, bsize=19) for a, b, c in props]).arrange_in_grid(rows=3, cols=3, buff=(0.2, 0.15)).next_to(title, DOWN, buff=0.3)
        with self.say("These elements share a set of properties. They are hard, dense metals with high melting points, because their unpaired d electrons join in metallic bonding. They show variable oxidation states, coloured ions and paramagnetism. They form complexes and alloys, trap small atoms in interstitial compounds, and they are excellent catalysts.") as v:
            self.play(FadeIn(title))
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.35)
                self.hold(v.dur / 9 - 0.4)
        self.play(FadeOut(VGroup(title, cards)))
        self.magnetism()

    def magnetism(self):
        f = M(r"\mu = \sqrt{n(n+2)}\ \ \text{BM}", size=56, color=th.MINT).to_edge(UP, buff=0.8)
        fl = T("n = number of unpaired electrons", size=24, color=th.MUTED).next_to(f, DOWN, buff=0.2)
        base = -2.6
        bars = VGroup()
        for n in range(6):
            mu = np.sqrt(n * (n + 2))
            b = Rectangle(width=0.9, height=max(0.03, mu * 0.62), fill_color=th.MINT, fill_opacity=0.85, stroke_width=0).move_to([-4.0 + 1.6 * n, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, T(f"{mu:.2f}", size=22, color=th.INK).next_to(b, UP, buff=0.08), T(f"n = {n}", size=22, color=th.MUTED).next_to([-4.0 + 1.6 * n, base, 0], DOWN, buff=0.12)))
        with self.say("Unpaired d electrons make these ions paramagnetic, attracted into a magnetic field. The spin only magnetic moment is the square root of n times n plus two, in Bohr magnetons, where n is the number of unpaired electrons. One unpaired electron gives one point seven three. Five give five point nine two. Iron, cobalt and nickel go further: they are ferromagnetic.") as v:
            self.play(Write(f), FadeIn(fl))
            for b in bars:
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1:]), run_time=0.45)
        self.play(FadeOut(VGroup(f, fl, bars)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        states = {"Sc": [3], "Ti": [2, 3, 4], "V": [2, 3, 4, 5], "Cr": [2, 3, 6], "Mn": [2, 3, 4, 6, 7], "Fe": [2, 3], "Co": [2, 3], "Ni": [2], "Cu": [1, 2], "Zn": [2]}
        ax = Axes(x_range=[0, 11, 1], y_range=[0, 8, 1], x_length=10.5, y_length=4.8, tips=False,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([0.3, -0.5, 0])
        ylab = VGroup(*[T(f"+{k}", size=26, color=th.MUTED).next_to(ax.c2p(0, k), LEFT, buff=0.1) for k in range(1, 8)])
        xlab = VGroup(*[T(m, size=30, color=th.INK, weight="BOLD").next_to(ax.c2p(i + 1, 0), DOWN, buff=0.15) for i, m in enumerate(METALS)])
        title = T("Common oxidation states", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        dots = VGroup()
        for i, m in enumerate(METALS):
            col = VGroup(*[Dot(ax.c2p(i + 1, k), radius=0.13, color=th.AMBER if k == max(states[m]) else th.SKY) for k in states[m]])
            dots.add(col)
        with self.say("Transition metals show many oxidation states. The reason: the 4s and 3d orbitals are so close in energy that after the two 4s electrons go, d electrons can follow one at a time. So the states usually differ by one."):
            self.play(FadeIn(title), Create(ax), FadeIn(ylab), FadeIn(xlab))
        with self.say("Plot them. Almost every element shows plus two, from losing the 4s pair. Scandium prefers plus three. The highest state climbs, plus four for titanium, plus five for vanadium, plus six for chromium, up to plus seven for manganese, which uses all five d and both s electrons.") as v:
            for c in dots:
                self.play(LaggedStart(*[GrowFromCenter(d_) for d_ in c], lag_ratio=0.2), run_time=0.5)
                self.hold(v.dur / 10 - 0.55)
        peak = VMobject(color=th.AMBER, stroke_width=3).set_points_as_corners([ax.c2p(i + 1, max(states[m])) for i, m in enumerate(METALS)])
        mn = T("MnO₄⁻: +7", size=24, color=th.AMBER).next_to(ax.c2p(5, 7), UP, buff=0.15)
        with self.say("After manganese the nuclear charge holds the d electrons too tightly. Iron rarely goes beyond plus three, and nickel, copper and zinc stop at plus two, with copper also showing plus one. The highest states appear only with oxygen and fluorine, as in permanganate and dichromate."):
            self.play(Create(peak), FadeIn(mn))
        ox = para("Oxides: low state basic (MnO) → intermediate amphoteric (Cr₂O₃) → high state acidic (Mn₂O₇, CrO₃)", width=6.0, size=22, color=th.BODY).move_to([3.2, 1.7, 0])
        with self.say("And the oxides follow a pattern: low oxidation state oxides are basic, intermediate ones amphoteric, and high ones acidic."):
            self.play(FadeIn(ox, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, ax, ylab, xlab, dots, peak, mn, ox)))
        head, prob = C.example_head(self, "Find the oxidation state of the metal in (a) KMnO₄, (b) K₂Cr₂O₇, (c) K₄[Fe(CN)₆], (d) [Ni(CO)₄].")
        st = C.steps(r"(a)\ (+1) + x + 4(-2) = 0 \Rightarrow x = +7",
                     r"(b)\ 2(+1) + 2x + 7(-2) = 0 \Rightarrow x = +6",
                     r"(c)\ [\mathrm{Fe(CN)_6}]^{4-}:\ x + 6(-1) = -4 \Rightarrow x = +2",
                     r"(d)\ \mathrm{CO}\ \text{is neutral}:\ x + 4(0) = 0 \Rightarrow x = 0", size=40).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example six point one. Take oxygen as minus two, potassium plus one, cyanide minus one, and carbon monoxide as neutral. Permanganate: plus seven. Dichromate: two chromiums share plus twelve, so plus six each. Ferrocyanide: the complex ion is minus four, so iron is plus two."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st[:3]:
                self.play(Write(s_))
        nb = C.show_neby(self, "surprised", height=1.3)
        with self.say("And nickel tetracarbonyl: carbon monoxide is neutral, so nickel is in the zero oxidation state. Only transition metals do this, with ligands like carbon monoxide that can take electron density back from the metal."):
            self.play(Write(st[3]))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "25.0 cm³ of 0.020 M KMnO₄ exactly oxidises acidified iron(II) sulphate. Write the ionic equation and find the mass of FeSO₄ (152 g mol⁻¹).")
        st = C.steps(r"\mathrm{MnO_4^- + 5Fe^{2+} + 8H^+ \rightarrow Mn^{2+} + 5Fe^{3+} + 4H_2O}",
                     r"\text{charge: } -1 + 10 + 8 = +17 = +2 + 15\ \checkmark",
                     r"n(\mathrm{MnO_4^-}) = 0.020 \times 0.0250 = 5.0\times10^{-4}\ \mathrm{mol}",
                     r"n(\mathrm{Fe^{2+}}) = 5 \times 5.0\times10^{-4} = 2.5\times10^{-3}\ \mathrm{mol}",
                     r"m = 2.5\times10^{-3} \times 152 = 0.38\ \mathrm{g}", size=36).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        st[4].set_color(th.AMBER)
        with self.say("Worked example six point two. Manganese falls from plus seven to plus two, gaining five electrons. Each iron loses one. So five iron two plus ions for every permanganate. Check the charge: plus seventeen on both sides."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Moles of permanganate: zero point zero two times zero point zero two five, five times ten to the minus four. Five times that is two point five times ten to the minus three moles of iron. Times one fifty two: zero point three eight grams of iron two sulphate."):
            for s_ in st[2:]:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("The oxidation state of nickel in [Ni(CO)₄] is",
                  ["0", "+2", "+4", "−4"], 0,
                  "Pause and think. What is the oxidation state of nickel in nickel tetracarbonyl?",
                  "A, zero. Carbon monoxide is a neutral ligand and the complex has no charge, so nickel must be zero. Plus two is the trap, from assuming nickel always forms its usual ion.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        c = np.array([-2.6, -0.8, 0])
        cu = VGroup(Circle(radius=0.55, fill_color=CU_COL, fill_opacity=1, stroke_color=WHITE, stroke_width=2), T("Cu²⁺", size=24, color=WHITE, weight="BOLD")).move_to(c)
        dirs = [UP, RIGHT, DOWN, LEFT]
        ligs = VGroup(*[VGroup(Circle(radius=0.42, fill_color=C.EL["N"], fill_opacity=0.9, stroke_width=0), T("NH₃", size=20, color=WHITE, weight="BOLD")).move_to(c + d_ * 2.6) for d_ in dirs])
        pairs = VGroup(*[VGroup(Dot(radius=0.06, color=th.AMBER), Dot(radius=0.06, color=th.AMBER)).arrange(RIGHT, buff=0.06) for _ in dirs])
        for p_, l_, d_ in zip(pairs, ligs, dirs):
            p_.move_to(l_.get_center() - d_ * 0.55)
        eq = chem(r"[Cu(H_2O)_4]^{2+} + 4NH_3 \rightarrow [Cu(NH_3)_4]^{2+} + 4H_2O", size=34).to_edge(UP, buff=0.8)
        with self.say("Remember the deep blue from the cold open? Four ammonia molecules replaced four water molecules around the copper ion. The result is a complex ion: a central metal ion, joined to surrounding molecules by coordinate bonds."):
            self.play(Write(eq))
            self.play(FadeIn(cu, scale=0.5))
            self.play(FadeIn(ligs), FadeIn(pairs))
        arrows = VGroup()
        for l_, d_ in zip(ligs, dirs):
            arrows.add(Arrow(c + d_ * 1.55, c + d_ * 0.6, buff=0, color=th.AMBER, stroke_width=5))
        with self.say("Each ammonia has a lone pair on nitrogen. It moves in and donates both electrons to the copper. Each bond is a dative bond, drawn as an arrow from ligand to metal."):
            self.play(*[l_.animate.move_to(c + d_ * 2.0) for l_, d_ in zip(ligs, dirs)], *[p_.animate.move_to(c + d_ * 1.45) for p_, d_ in zip(pairs, dirs)], run_time=1.2)
            self.play(FadeOut(pairs), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
        rows = [["Term", "Meaning", "In [Cu(NH₃)₄]SO₄"], ["central ion", "electron-pair acceptor (Lewis acid)", "Cu²⁺"], ["ligand", "electron-pair donor (Lewis base)", "NH₃"],
                ["coordination number", "number of dative bonds", "4"], ["coordination sphere", "the part in square brackets", "[Cu(NH₃)₄]²⁺"], ["counter ion", "outside the brackets", "SO₄²⁻"]]
        tb = C.table(rows, [3.0, 4.6, 2.6], row_h=0.66, size=24, colors=[th.AMBER, th.BODY, th.INK]).move_to([1.6, -0.8, 0])
        with self.say("The vocabulary. The central ion accepts electron pairs, a Lewis acid. The ligand donates them, a Lewis base. The number of dative bonds is the coordination number, here four. The bracketed part is the coordination sphere, and the sulphate outside is the counter ion.") as v:
            self.play(VGroup(cu, ligs, arrows).animate.scale(0.6).move_to([-5.4, -0.8, 0]))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(VGroup(eq, cu, ligs, arrows, tb)))
        title = T("Ligands by number of donor atoms", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cols = VGroup(
            C.card(self, "Monodentate · 1", "NH₃, H₂O, CN⁻, Cl⁻, OH⁻, CO, NO₂⁻", w=3.9, h=2.0, color=th.SKY, bsize=22),
            C.card(self, "Bidentate · 2", "ethane-1,2-diamine (en), oxalate C₂O₄²⁻", w=3.9, h=2.0, color=th.AMBER, bsize=22),
            C.card(self, "Hexadentate · 6", "EDTA⁴⁻: wraps the whole ion", w=3.9, h=2.0, color=th.MINT, bsize=22),
        ).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.4)
        mc = np.array([0, -1.9, 0])
        m = Circle(radius=0.35, fill_color=th.PINK, fill_opacity=1, stroke_width=0).move_to(mc)
        claw = VGroup(*[Arc(radius=0.95, start_angle=a, angle=PI / 3.2, arc_center=mc, color=th.MINT, stroke_width=6) for a in np.linspace(0, TAU, 6, endpoint=False)])
        donors = VGroup(*[Dot(mc + 0.95 * np.array([np.cos(a), np.sin(a), 0]), radius=0.1, color=th.AMBER) for a in np.linspace(0, TAU, 6, endpoint=False)])
        ch = T("chelate: a ring-forming ligand grips like a claw, very stable", size=22, color=th.MINT).next_to(claw, DOWN, buff=0.2)
        with self.say("Ligands are classed by how many donor atoms they use. Monodentate ligands like ammonia use one. Bidentate ligands like ethane diamine and oxalate use two. E D T A uses six, wrapping right around the metal. A ring forming ligand is a chelate, from the Greek for claw, and chelates are very stable. That is why E D T A softens water and treats lead poisoning."):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.4))
            self.play(FadeIn(m), Create(claw), FadeIn(donors), FadeIn(ch))
        self.play(FadeOut(VGroup(title, cols, m, claw, donors, ch)))
        d = M(r"\text{EAN} = Z - \text{oxidation state} + 2 \times \text{coordination number}", size=40).to_edge(UP, buff=0.8)
        sd = para("Sidgwick: a complex is especially stable if its EAN equals the next noble gas (36 Kr, 54 Xe, 86 Rn).", width=11, size=24, color=th.MUTED).next_to(d, DOWN, buff=0.2)
        st = C.steps(r"[\mathrm{Fe(CN)_6}]^{4-}:\ 26 - 2 + 2(6) = 36\ \ (\mathrm{Kr})",
                     r"[\mathrm{Co(NH_3)_6}]^{3+}:\ 27 - 3 + 2(6) = 36\ \ (\mathrm{Kr})",
                     r"[\mathrm{Ni(CO)_4}]:\ 28 - 0 + 2(4) = 36\ \ (\mathrm{Kr})",
                     r"[\mathrm{Cu(NH_3)_4}]^{2+}:\ 29 - 2 + 2(4) = 35\ \ (\text{not a noble gas})", size=38).next_to(sd, DOWN, buff=0.5)
        st[3].set_color(th.CORAL)
        with self.say("Worked example six point three, the effective atomic number. Start from the atomic number, subtract the oxidation state, and add two electrons for every ligand bond. Ferrocyanide: twenty six minus two plus twelve, thirty six, the same as krypton. Cobalt hexammine and nickel carbonyl also reach thirty six."):
            self.play(Write(d), FadeIn(sd))
            for s_ in st[:3]:
                self.play(Write(s_))
        with self.say("But copper tetrammine comes to thirty five, not a noble gas number, and yet it is perfectly stable. The E A N rule is a useful guide, not a law."):
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(d, sd, st)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        title = T("Shape follows coordination number", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)

        def mol(center, vecs, mcol, lcol=th.SKY, depth=None):
            c = np.array(center, dtype=float)
            g = VGroup()
            for i, v in enumerate(vecs):
                p = c + 1.25 * np.array(v)
                dashed = depth is not None and depth[i] < 0
                g.add(DashedLine(c, p, color=th.MUTED, stroke_width=4) if dashed else Line(c, p, color=th.MUTED, stroke_width=5))
            for i, v in enumerate(vecs):
                op = 0.55 if (depth is not None and depth[i] < 0) else 1
                g.add(Circle(radius=0.24, fill_color=lcol, fill_opacity=op, stroke_width=0).move_to(c + 1.25 * np.array(v)))
            g.add(Circle(radius=0.36, fill_color=mcol, fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to(c))
            return g
        lin = mol([-5.2, 0.6, 0], [[-1.0, 0, 0], [1.0, 0, 0]], C.EL["Ag"])
        tet = mol([-1.85, 0.6, 0], [[0, 1.0, 0], [-0.95, -0.45, 0], [0.95, -0.45, 0], [0.15, -0.25, 0]], C.EL["Ni"] if "Ni" in C.EL else th.MINT, depth=[1, 1, 1, -1])
        sqp = mol([1.55, 0.6, 0], [[-0.9, 0.35, 0], [0.9, -0.35, 0], [0.45, 0.6, 0], [-0.45, -0.6, 0]], th.PINK)
        octa = mol([5.0, 0.6, 0], [[0, 1.05, 0], [0, -1.05, 0], [-1.0, 0.0, 0], [1.0, 0.0, 0], [0.45, 0.35, 0], [-0.45, -0.35, 0]], th.AMBER, depth=[1, 1, 1, 1, -1, 1])
        names = [("linear", "CN 2 · sp", "[Ag(NH₃)₂]⁺"), ("tetrahedral", "CN 4 · sp³", "[NiCl₄]²⁻, [Zn(NH₃)₄]²⁺"),
                 ("square planar", "CN 4 · dsp²", "[Ni(CN)₄]²⁻, [Cu(NH₃)₄]²⁺"), ("octahedral", "CN 6 · d²sp³ / sp³d²", "[Fe(CN)₆]³⁻, [Co(NH₃)₆]³⁺")]
        shapes = [lin, tet, sqp, octa]
        labs = VGroup()
        for s_, (a, b, c_) in zip(shapes, names):
            labs.add(VGroup(T(a, size=30, color=th.INK, weight="BOLD"), T(b, size=24, color=th.AMBER), T(c_, size=21, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(s_, DOWN, buff=0.4))
        with self.say("The shape of a complex follows from its coordination number and the hybridisation of the metal. Two ligands, s p hybrid: linear, like the silver diammine ion in Tollens reagent.") :
            self.play(FadeIn(title))
            self.play(GrowFromCenter(lin), FadeIn(labs[0]))
        with self.say("Four ligands can give two shapes. With s p three hybrids, tetrahedral, as in tetrachloronickelate. With d s p two hybrids, square planar, as in tetracyanonickelate and copper tetrammine."):
            self.play(GrowFromCenter(tet), FadeIn(labs[1]))
            self.play(Rotate(tet, angle=TAU, axis=UP, about_point=tet[-1].get_center()), run_time=2.0)
            self.play(GrowFromCenter(sqp), FadeIn(labs[2]))
        with self.say("Six ligands, using d two s p three or s p three d two hybrids, sit at the corners of an octahedron: ferricyanide, cobalt hexammine, hexaaqua chromium. Octahedral is the most common shape of all."):
            self.play(GrowFromCenter(octa), FadeIn(labs[3]))
            self.play(Rotate(octa, angle=TAU, axis=UP, about_point=octa[-1].get_center()), run_time=2.5)
        self.play(FadeOut(VGroup(title, *shapes, labs)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        posts = VGroup(*[para(s, width=11.5, size=30, color=th.BODY) for s in [
            "1. Metal–ligand bonding is purely electrostatic: ligands are point negative charges.",
            "2. In a free ion, the five d orbitals have equal energy (degenerate).",
            "3. Approaching ligands repel d electrons; orbitals pointing AT them rise most."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 0.4)
        for p_ in posts:
            p_.scale_to_fit_width(min(p_.width, 12.4))
        with self.say("Valence bond theory gives shapes, but not colours or magnetism. Crystal field theory does both. It treats the ligands as point negative charges. In a free ion all five d orbitals have the same energy. When ligands approach, they repel the d electrons, and orbitals that point straight at the ligands are pushed up the most.") as v:
            for p_ in posts:
                self.play(FadeIn(p_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v.dur / 3 - 0.7)
        self.play(FadeOut(posts))
        # orbital lobes: d_x2-y2 (points at ligands) vs d_xy (between)
        def lobes(c, ang, col):
            g = VGroup()
            for k in range(4):
                a = ang + k * PI / 2
                g.add(Ellipse(width=1.3, height=0.55, fill_color=col, fill_opacity=0.55, stroke_width=0).rotate(a).move_to(c + 0.7 * np.array([np.cos(a), np.sin(a), 0])))
            return g
        c1, c2 = np.array([-3.4, 0.2, 0]), np.array([3.4, 0.2, 0])
        lx = lobes(c1, 0, th.CORAL)
        lxy = lobes(c2, PI / 4, th.SKY)
        ligs = VGroup(*[Dot(c + 1.75 * d_, radius=0.16, color=th.AMBER) for c in (c1, c2) for d_ in (UP, DOWN, LEFT, RIGHT)])
        n1 = VGroup(M(r"d_{x^2-y^2}", size=36, color=th.CORAL), T("points AT the ligands: raised", size=22, color=th.CORAL)).arrange(DOWN, buff=0.1).next_to(lx, DOWN, buff=1.3)
        n2 = VGroup(M(r"d_{xy}", size=36, color=th.SKY), T("points BETWEEN them: lowered", size=22, color=th.SKY)).arrange(DOWN, buff=0.1).next_to(lxy, DOWN, buff=1.3)
        with self.say("In an octahedral complex, six ligands sit on the x, y and z axes. Look at two orbitals in the x y plane. d x squared minus y squared has its lobes pointing straight at the ligands, so its electrons are repelled strongly. d x y points between them, and is repelled less. The same goes for d z squared, along z, versus d y z and d z x."):
            self.play(FadeIn(lx), FadeIn(lxy))
            self.play(LaggedStart(*[FadeIn(l_, scale=2) for l_ in ligs], lag_ratio=0.08))
            self.play(FadeIn(n1), FadeIn(n2))
            self.play(Indicate(lx, color=th.CORAL, scale_factor=1.05), Indicate(lxy, color=th.SKY, scale_factor=0.95))
        self.play(FadeOut(VGroup(lx, lxy, ligs, n1, n2)))
        self.splitting()
        self.example_64()
        self.spectro()

    def splitting(self):
        sp = ValueTracker(0)
        x0 = -1.4
        base = -0.1

        def levels():
            k = sp.get_value()
            g = VGroup()
            g.add(VGroup(*[Line([-6.3 + 0.55 * q, base, 0], [-5.9 + 0.55 * q, base, 0], color=th.INK, stroke_width=6) for q in range(5)]))
            yt = base - 0.4 * 3.2 * k
            ye = base + 0.6 * 3.2 * k
            g.add(VGroup(*[Line([x0 + 0.8 * q, yt, 0], [x0 + 0.6 + 0.8 * q, yt, 0], color=th.SKY, stroke_width=6) for q in range(3)]))
            g.add(VGroup(*[Line([x0 + 0.4 + 0.8 * q, ye, 0], [x0 + 1.0 + 0.8 * q, ye, 0], color=th.CORAL, stroke_width=6) for q in range(2)]))
            g.add(DashedLine([-3.5, base, 0], [x0 - 0.2, base, 0], color=th.FAINT, stroke_width=2))
            return g
        lv = always_redraw(levels)
        fl = T("free ion: 5 equal d orbitals", size=24, color=th.INK).next_to([-6.4, base - 0.45, 0], RIGHT, buff=0)
        with self.say("Now the energy picture. In the free ion, five d orbitals at the same level. Bring in the octahedral field of ligands. The set splits."):
            self.add(lv)
            self.play(FadeIn(lv), FadeIn(fl))
            self.play(sp.animate.set_value(1), run_time=2.5, rate_func=smooth)
        yt, ye = base - 1.28, base + 1.92
        egl = VGroup(M(r"e_g", size=44, color=th.CORAL), M(r"d_{x^2-y^2},\ d_{z^2}", size=32, color=th.CORAL)).arrange(RIGHT, buff=0.3).next_to([x0 + 1.9, ye, 0], RIGHT, buff=0.3)
        t2l = VGroup(M(r"t_{2g}", size=44, color=th.SKY), M(r"d_{xy},\ d_{yz},\ d_{zx}", size=32, color=th.SKY)).arrange(RIGHT, buff=0.3).next_to([x0 + 2.2, yt, 0], RIGHT, buff=0.3)
        dlt = DoubleArrow([5.6, yt, 0], [5.6, ye, 0], buff=0, color=th.AMBER, stroke_width=5, tip_length=0.25)
        dl = M(r"\Delta_o", size=48, color=th.AMBER).next_to(dlt, RIGHT, buff=0.1)
        b1 = M(r"+0.6\Delta_o", size=32, color=th.CORAL).next_to([x0 - 0.2, (base + ye) / 2, 0], LEFT, buff=0.15)
        b2 = M(r"-0.4\Delta_o", size=32, color=th.SKY).next_to([x0 - 0.2, (base + yt) / 2, 0], LEFT, buff=0.15)
        with self.say("The two orbitals pointing at the ligands, d x squared minus y squared and d z squared, rise: the e g set. The three pointing between, d x y, d y z and d z x, fall: the t two g set. The gap between them is the crystal field splitting energy, delta o. The t two g set falls by zero point four delta o, the e g set rises by zero point six delta o, so the average energy stays the same."):
            self.play(FadeIn(egl), FadeIn(t2l))
            self.play(GrowFromCenter(dlt), Write(dl))
            self.play(FadeIn(b1), FadeIn(b2))
        cf = M(r"\text{CFSE} = (-0.4\,n_{t_{2g}} + 0.6\,n_{e_g})\,\Delta_o", size=44, color=th.MINT).to_edge(UP, buff=0.75)
        with self.say("Putting electrons into this split set gains a net energy, the crystal field stabilisation energy: minus zero point four delta o for every t two g electron, plus zero point six for every e g electron."):
            self.play(Write(cf))
        self.play(FadeOut(VGroup(fl, egl, t2l, dlt, dl, b1, b2, cf)), FadeOut(lv))
        self.remove(lv)

    def example_64(self):
        title = T("Fe²⁺ (3d⁶): high spin or low spin?", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        sub = T("depends on Δo versus the pairing energy P", size=24, color=th.MUTED).next_to(title, DOWN, buff=0.2)

        def diagram(cx, gap, high):
            t = box_row(3, w=0.8, h=0.85).move_to([cx, -2.3, 0])
            e = box_row(2, w=0.8, h=0.85).move_to([cx, -2.3 + gap, 0])
            if high:
                arrows = VGroup(fill(t, 3, h=0.6, off=0.14), fill(e, 2, h=0.6, off=0.14), spin(False, h=0.6).move_to(t[0].get_center() + RIGHT * 0.14))
            else:
                arrows = fill(t, 6, h=0.6, off=0.14)
            gl = DoubleArrow(t.get_right() + RIGHT * 0.35, t.get_right() + RIGHT * 0.35 + UP * gap, buff=0, color=th.AMBER, stroke_width=4, tip_length=0.2)
            return VGroup(t, e), arrows, gl
        lb, la, lg = diagram(-3.4, 1.3, True)
        rb, ra, rg = diagram(3.2, 2.3, False)
        hl = VGroup(chem(r"[Fe(H_2O)_6]^{2+}", size=34), T("H₂O: weak field, Δo < P: high spin", size=24, color=th.SKY)).arrange(DOWN, buff=0.12).move_to([-3.4, 1.35, 0])
        hr = VGroup(chem(r"[Fe(CN)_6]^{4-}", size=34), T("CN⁻: strong field, Δo > P: low spin", size=24, color=th.CORAL)).arrange(DOWN, buff=0.12).move_to([3.2, 1.35, 0])
        with self.say("Worked example six point four. Both hexaaqua iron two and ferrocyanide contain iron two plus, 3d six. With six electrons, there is a choice. Spread out over all five orbitals, or pair up in the lower three? It depends on whether delta o is smaller or larger than the pairing energy, the cost of squeezing two electrons into one orbital."):
            self.play(FadeIn(title), FadeIn(sub))
        with self.say("Water is a weak field ligand, so the gap is small. Electrons spread out: four up the ladder, t two g four, e g two, with four unpaired electrons. High spin."):
            self.play(FadeIn(hl), Create(lb), GrowFromCenter(lg))
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in la], lag_ratio=0.15), run_time=1.5)
        with self.say("Cyanide is a strong field ligand, the gap is large, and it is cheaper to pair up. All six electrons crowd into t two g. No unpaired electrons. Low spin, and diamagnetic."):
            self.play(FadeIn(hr), Create(rb), GrowFromCenter(rg))
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in ra], lag_ratio=0.15), run_time=1.5)
        self.play(FadeOut(VGroup(title, sub)))
        calc = VGroup(
            M(r"\text{CFSE} = [-0.4(4) + 0.6(2)]\Delta_o = -0.4\Delta_o", size=34), M(r"\mu = \sqrt{4 \times 6} = 4.90\ \mathrm{BM}", size=36, color=th.SKY),
        ).arrange(DOWN, buff=0.2).move_to([-3.4, 2.2, 0])
        calc2 = VGroup(
            M(r"\text{CFSE} = -0.4(6)\Delta_o = -2.4\Delta_o", size=34), M(r"\mu = 0\ \ (\text{diamagnetic})", size=36, color=th.CORAL),
        ).arrange(DOWN, buff=0.2).move_to([3.2, 2.2, 0])
        self.play(FadeOut(hl), FadeOut(hr))
        with self.say("Now the numbers. High spin: minus zero point four times four, plus zero point six times two, gives a C F S E of minus zero point four delta o, and four unpaired electrons give a moment of root twenty four, four point nine zero Bohr magnetons. Low spin: minus two point four delta o, and zero moment. That much larger stabilisation pays for the pairing."):
            self.play(Write(calc))
            self.play(Write(calc2))
        self.play(FadeOut(VGroup(lb, la, lg, rb, ra, rg, calc, calc2)))

    def spectro(self):
        title = T("The spectrochemical series", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ligs = ["I⁻", "Br⁻", "Cl⁻", "F⁻", "OH⁻", "H₂O", "NH₃", "en", "NO₂⁻", "CN⁻", "CO"]
        row = VGroup(*[T(l_, size=30, color=interpolate_color(ManimColor(th.SKY), ManimColor(th.CORAL), i / 10), weight="BOLD") for i, l_ in enumerate(ligs)])
        row.arrange(RIGHT, buff=0.42).move_to(UP * 0.6)
        lt = VGroup(*[T("<", size=26, color=th.MUTED).move_to((a.get_right() + b.get_left()) / 2) for a, b in zip(row, row[1:])])
        arr = Arrow(row.get_left() + DOWN * 0.8, row.get_right() + DOWN * 0.8, buff=0, color=th.AMBER, stroke_width=5)
        al = VGroup(T("weak field: small Δ, high spin", size=22, color=th.SKY).next_to(arr.get_start(), DOWN, buff=0.2).align_to(arr, LEFT),
                    T("strong field: large Δ, low spin", size=22, color=th.CORAL).next_to(arr.get_end(), DOWN, buff=0.2).align_to(arr, RIGHT))
        with self.say("Ligands can be ranked by how strongly they split the d orbitals. This is the spectrochemical series. Iodide, bromide, chloride and fluoride are weak: small splitting, high spin. Then hydroxide, water, ammonia, ethane diamine, nitrite. Cyanide and carbon monoxide are the strongest: large splitting, low spin.") as v:
            self.play(FadeIn(title))
            for i, l_ in enumerate(row):
                self.play(FadeIn(l_, shift=UP * 0.15), *([FadeIn(lt[i - 1])] if i else []), run_time=0.25)
                self.hold(v.dur / 14 - 0.3)
            self.play(GrowArrow(arr), FadeIn(al))
        tet = para("Tetrahedral field: the pattern is inverted (e below t₂) and Δt is only 4/9 of Δo, so tetrahedral complexes are almost always high spin.", width=11, size=24, color=th.BODY).to_edge(DOWN, buff=0.6)
        with self.say("One more fact. In a tetrahedral complex only four ligands approach, between the axes, so the pattern flips and the splitting is just four ninths as large. Tetrahedral complexes are almost always high spin."):
            self.play(FadeIn(tet, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, row, lt, arr, al, tet)))
        self.tip("Spectrochemical series: I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O < NH₃ < en < NO₂⁻ < CN⁻ < CO. Halides weak, CN⁻ and CO strong.",
                 "Learn the series as a sentence: halides at the weak end, then hydroxide, water, ammonia, en, nitrite, and cyanide and carbon monoxide at the strong end. Weak field means high spin and pale colours. Strong field means low spin and deep colours.", state="wink")

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        x0, w = -6.0, 8.4
        spec = VGroup()
        for k in range(60):
            lam = 400 + k * 5
            spec.add(Rectangle(width=w / 60, height=0.5, stroke_width=0, fill_opacity=1, fill_color=self.wl_color(lam)).move_to([x0 + (k + 0.5) * w / 60, 2.0, 0]))
        sl = VGroup(T("400 nm", size=20, color=th.MUTED).next_to(spec, DOWN, buff=0.1).align_to(spec, LEFT), T("700 nm", size=20, color=th.MUTED).next_to(spec, DOWN, buff=0.1).align_to(spec, RIGHT))
        t = box_row(3, w=0.8, h=0.85).move_to([-3.0, -1.9, 0])
        e = box_row(2, w=0.8, h=0.85).move_to([-3.0, 0.4, 0])
        el = spin(True, th.AMBER, h=0.6).move_to(t[0].get_center() + LEFT * 0.14)
        tl = M("t_{2g}", size=40, color=th.SKY).next_to(t, LEFT, buff=0.25)
        elb = M("e_g", size=40, color=th.CORAL).next_to(e, LEFT, buff=0.25)
        key = para("Δo is about 150–400 kJ mol⁻¹: exactly the energy of visible light. A d electron absorbs a photon and jumps from t₂g to e_g: a d–d transition.", width=5.6, size=24, color=th.INK).move_to([3.4, -0.6, 0])
        with self.say("Now the colours. The splitting delta o happens to be about one hundred and fifty to four hundred kilojoules per mole, which is exactly the energy of visible light. A d electron can absorb a photon and jump from the lower t two g level to the upper e g level. This is a d d transition."):
            self.play(FadeIn(spec), FadeIn(sl))
            self.play(Create(t), Create(e), FadeIn(tl), FadeIn(elb), FadeIn(el))
            ph = FunctionGraph(lambda x: 0.12 * np.sin(12 * x), x_range=[0, 2.4], color="#55D46A").move_to([-5.6, -0.7, 0])
            self.play(Create(ph))
            self.play(ph.animate.move_to(t.get_left() + LEFT * 0.4).scale(0.5).set_opacity(0), run_time=0.8)
            self.play(el.animate.move_to(e[0].get_center() + LEFT * 0.14), run_time=0.6)
            self.play(FadeIn(key))
        ring = VGroup()
        cols = ["#FF4040", "#FF9A3C", "#FFE14A", "#55D46A", "#3FA0FF", "#8A5CFF"]
        names = ["red", "orange", "yellow", "green", "blue", "violet"]
        rc = np.array([3.4, -0.6, 0])
        for k, (c_, n_) in enumerate(zip(cols, names)):
            a = PI / 2 - k * TAU / 6
            ring.add(AnnularSector(inner_radius=0.7, outer_radius=1.5, angle=TAU / 6, start_angle=a - TAU / 12, fill_color=c_, fill_opacity=0.9, stroke_width=0, arc_center=rc))
            ring.add(T(n_, size=18, color=WHITE, weight="BOLD").move_to(rc + 1.1 * np.array([np.cos(a), np.sin(a), 0])))
        rl = T("colour seen = complement of colour absorbed", size=22, color=th.AMBER).next_to(ring, DOWN, buff=0.25)
        with self.say("The light that is absorbed is removed, and we see the rest, the complementary colour, directly opposite on the colour wheel. Absorb green, and the solution looks violet or purple. Absorb yellow, and it looks blue. Absorb red, and it looks blue green."):
            self.play(FadeOut(key))
            self.play(FadeIn(ring), FadeIn(rl))
            self.play(Indicate(VGroup(ring[6], ring[7]), color=WHITE, scale_factor=1.1))
            self.play(Indicate(VGroup(ring[10], ring[11]), color=WHITE, scale_factor=1.1))
        self.play(FadeOut(VGroup(spec, sl, t, e, el, tl, elb, ring, rl, ph)))
        self.example_65()
        self.three_rules()
        self.quiz("Which of these ions is colourless in aqueous solution?",
                  ["Cu²⁺", "Fe³⁺", "Zn²⁺", "Ni²⁺"], 2,
                  "Pause and think. Which of these four ions gives a colourless solution?",
                  "C, zinc two plus. It is 3d ten: the d subshell is full, so there is no vacancy in the upper level for an electron to jump into. No d d transition, no colour. Copper two plus is 3d nine, iron three plus 3d five, nickel two plus 3d eight: all have partly filled d subshells.")

    def wl_color(self, lam):
        stops = [(400, "#8A5CFF"), (450, "#3F6BFF"), (490, "#3FC8FF"), (530, "#55D46A"), (580, "#FFE14A"), (620, "#FF9A3C"), (700, "#FF3030")]
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if lam <= b:
                return interpolate_color(ManimColor(ca), ManimColor(cb), (lam - a) / (b - a))
        return ManimColor(stops[-1][1])

    def example_65(self):
        head, prob = C.example_head(self, "[Ti(H₂O)₆]³⁺ absorbs most strongly at 500 nm. Find Δo in kJ mol⁻¹ and explain its violet colour. (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, NA = 6.022 × 10²³ mol⁻¹)")
        st = C.steps(r"E = \frac{hc}{\lambda} = \frac{(6.626\times10^{-34})(3.0\times10^{8})}{500\times10^{-9}} = 3.976\times10^{-19}\ \mathrm{J}",
                     r"\Delta_o = E \times N_A = 3.976\times10^{-19} \times 6.022\times10^{23} = 2.394\times10^{5}\ \mathrm{J\,mol^{-1}}",
                     r"\Delta_o \approx 239\ \mathrm{kJ\,mol^{-1}}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example six point five. Titanium three plus in water absorbs most strongly at five hundred nanometres. The energy of one photon is h c over lambda: three point nine seven six times ten to the minus nineteen joules."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Multiply by Avogadro's number for a mole: two point three nine four times ten to the five joules, about two hundred and thirty nine kilojoules per mole. That is delta o."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        sw = VGroup(Square(side_length=0.9, fill_color="#55D46A", fill_opacity=1, stroke_width=0), T("absorbed: green", size=20, color=th.BODY),
                    Square(side_length=0.9, fill_color="#9A5CFF", fill_opacity=1, stroke_width=0), T("seen: violet", size=20, color=th.BODY))
        sw[1].next_to(sw[0], DOWN, buff=0.1)
        sw[2].next_to(sw[0], RIGHT, buff=1.3)
        sw[3].next_to(sw[2], DOWN, buff=0.1)
        sw.to_edge(DOWN, buff=0.5)
        with self.say("Titanium three plus is 3d one. Its single electron jumps from t two g to e g by absorbing green light at five hundred nanometres. The light that gets through is the complement of green, so the solution looks violet."):
            self.play(FadeIn(sw))
        self.play(FadeOut(VGroup(head, prob, st, sw)))

    def three_rules(self):
        title = T("Three consequences", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        b1 = C.Beaker(center=[-4.7, -0.9, 0], w=1.6, h=2.0, level=0.7, color="#E6E9F2", opacity=0.1)
        b2 = C.Beaker(center=[-1.8, -0.9, 0], w=1.6, h=2.0, level=0.7, color=PALE_BLUE, opacity=0.55)
        b3 = C.Beaker(center=[0.1, -0.9, 0], w=1.6, h=2.0, level=0.7, color=ROYAL, opacity=0.85)
        b4 = C.Beaker(center=[3.3, -0.9, 0], w=1.5, h=2.0, level=0.7, color="#B7E39B", opacity=0.6)
        b5 = C.Beaker(center=[5.2, -0.9, 0], w=1.5, h=2.0, level=0.7, color="#D9A03A", opacity=0.6)
        h1 = VGroup(T("1. d⁰ and d¹⁰: colourless", size=24, color=th.INK, weight="BOLD"), T("Zn²⁺, Sc³⁺, Ti⁴⁺, Cu⁺, Ag⁺", size=20, color=th.MUTED)).arrange(DOWN, buff=0.06).next_to(b1.g, UP, buff=0.3)
        h2 = VGroup(T("2. the ligand changes Δ", size=24, color=th.INK, weight="BOLD"), T("[Cu(H₂O)₄]²⁺ → [Cu(NH₃)₄]²⁺", size=20, color=th.MUTED)).arrange(DOWN, buff=0.06).next_to(VGroup(b2.g, b3.g), UP, buff=0.3)
        h3 = VGroup(T("3. so does oxidation state", size=24, color=th.INK, weight="BOLD"), T("Fe²⁺ pale green, Fe³⁺ yellow-brown", size=20, color=th.MUTED)).arrange(DOWN, buff=0.06).next_to(VGroup(b4.g, b5.g), UP, buff=0.3)
        with self.say("Three consequences follow, and they answer our cold open. First, d zero and d ten ions are colourless: no d electron to promote, or no empty place to promote it to. Zinc two plus is d ten, so zinc sulphate is colourless. Copper two plus is d nine, with one vacancy, so it is blue."):
            self.play(FadeIn(title), FadeIn(b1.g), FadeIn(h1))
        with self.say("Second, the ligand changes the colour by changing delta o. Ammonia is higher than water in the spectrochemical series. It splits the d orbitals more, the absorption shifts to higher energy, and the pale blue aqua complex becomes the deep royal blue ammine complex. That is the cold open, solved."):
            self.play(FadeIn(b2.g), FadeIn(h2))
            self.play(TransformFromCopy(b2.g, b3.g), run_time=1.2)
            nb = C.show_neby(self, "celebrate", height=1.3, corner=DL)
        C.hide_neby(self, nb)
        with self.say("Third, the oxidation state matters too. Iron two plus is pale green, iron three plus yellow brown."):
            self.play(FadeIn(b4.g), FadeIn(b5.g), FadeIn(h3))
        self.play(FadeOut(VGroup(title, b1.g, b2.g, b3.g, b4.g, b5.g, h1, h2, h3)))
        care = self.callout("careful", "MnO₄⁻ (purple) and Cr₂O₇²⁻ (orange) are NOT coloured by d–d transitions: Mn(VII) and Cr(VI) are d⁰. Their intense colours come from charge transfer, an electron moving from oxygen to the metal.", width=11, size=27)
        with self.say("A careful point. Permanganate is intensely purple, but manganese seven is d zero, with no d electrons at all. Its colour comes from charge transfer: light moves an electron from an oxygen lone pair onto the metal. The same goes for dichromate. That is why these colours are so much more intense."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        title = T("1. Variable oxidation state", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        c = np.array([0, -0.4, 0])
        n1 = c + np.array([-2.8, 0, 0])
        n2 = c + np.array([2.8, 0, 0])
        f3 = chem(r"Fe^{3+}", size=64, color=th.AMBER).move_to(n1)
        f2 = chem(r"Fe^{2+}", size=64, color=th.MINT).move_to(n2)
        a1 = CurvedArrow(n1 + RIGHT * 0.8 + UP * 0.3, n2 + LEFT * 0.8 + UP * 0.3, angle=-TAU / 5, color=th.MUTED)
        a2 = CurvedArrow(n2 + LEFT * 0.8 + DOWN * 0.3, n1 + RIGHT * 0.8 + DOWN * 0.3, angle=-TAU / 5, color=th.MUTED)
        t1 = chem(r"2I^- \rightarrow I_2", size=42, color=C.EL["I"]).next_to(a1, UP, buff=0.1)
        t2 = chem(r"S_2O_8^{2-} \rightarrow 2SO_4^{2-}", size=42, color=th.SKY).next_to(a2, DOWN, buff=0.1)
        net = chem(r"\text{net: } S_2O_8^{2-} + 2I^- \xrightarrow{Fe^{3+}} 2SO_4^{2-} + I_2", size=36).to_edge(DOWN, buff=0.5)
        with self.say("Transition metals are superb catalysts, for two reasons. First, variable oxidation states. Persulphate and iodide are both negative ions, so they repel and react slowly. Add iron three plus. It oxidises iodide to iodine, becoming iron two plus. Then persulphate oxidises it back to iron three plus. The iron goes round and round, and is not used up."):
            self.play(FadeIn(title), FadeIn(f3), FadeIn(f2))
            self.play(Create(a1), FadeIn(t1))
            self.play(Create(a2), FadeIn(t2))
            self.play(Write(net))
        self.play(FadeOut(VGroup(title, f3, f2, a1, a2, t1, t2, net)))
        title = T("2. Surface adsorption", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        surf = Rectangle(width=10, height=0.5, fill_color="#8C93A8", fill_opacity=1, stroke_width=0).move_to([0, -2.3, 0])
        sl = T("iron surface (Haber process)", size=22, color=th.BG, weight="BOLD").move_to(surf)
        n2s = VGroup(*[VGroup(C.atom("N", r=0.32), C.atom("N", r=0.32).shift(RIGHT * 0.6)).move_to([-3.6 + 3.6 * k, 1.4, 0]) for k in range(3)])
        h2s = VGroup(*[VGroup(C.atom("H", r=0.22), C.atom("H", r=0.22).shift(RIGHT * 0.42)).move_to([-1.8 + 3.6 * k, 0.4, 0]) for k in range(2)])
        with self.say("Second, surfaces. The partly filled d orbitals and unsatisfied valencies on a metal surface adsorb gas molecules, hold them close together in the right orientation, and weaken their bonds. In the Haber process, nitrogen and hydrogen are adsorbed on iron, the strong nitrogen triple bond is loosened, and ammonia forms and leaves."):
            self.play(FadeIn(title), FadeIn(surf), FadeIn(sl), FadeIn(n2s), FadeIn(h2s))
            self.play(*[m.animate.move_to([m.get_x(), -1.7, 0]) for m in n2s], *[m.animate.move_to([m.get_x(), -1.8, 0]) for m in h2s], run_time=1.4)
            self.play(*[m[1].animate.shift(RIGHT * 0.45) for m in n2s], *[m[1].animate.shift(RIGHT * 0.35) for m in h2s], run_time=0.8)
            nh3 = VGroup(*[T("NH₃", size=36, color=C.EL["N"], weight="BOLD").move_to([-3.6 + 3.6 * k, -1.6, 0]) for k in range(3)])
            self.play(FadeOut(n2s), FadeOut(h2s), FadeIn(nh3))
            self.play(nh3.animate.shift(UP * 2.6), run_time=1.2)
        self.play(FadeOut(VGroup(title, surf, sl, nh3)))
        rows = [["Catalyst", "Process", "Reaction"], ["Fe + Mo promoter", "Haber", "N₂ + 3H₂ ⇌ 2NH₃"], ["V₂O₅", "contact", "2SO₂ + O₂ ⇌ 2SO₃"],
                ["Pt / Rh gauze", "Ostwald", "4NH₃ + 5O₂ → 4NO + 6H₂O"], ["Ni", "vanaspati ghee", "oil + H₂ → fat"], ["MnO₂", "lab oxygen", "2KClO₃ → 2KCl + 3O₂"],
                ["TiCl₄ + Al(C₂H₅)₃", "Ziegler–Natta", "n CH₂=CH₂ → polythene"]]
        tb = C.table(rows, [3.6, 3.0, 5.0], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.BODY]).move_to(UP * 0.2)
        with self.say("And so transition metals run industry. Iron for ammonia, vanadium pentoxide for sulphuric acid, platinum and rhodium gauze for nitric acid, nickel for vanaspati ghee, manganese dioxide for oxygen in the lab, and Ziegler Natta catalysts of titanium for polythene.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Transition element: partly filled d subshell in atom or common ion. Cr 3d⁵4s¹, Cu 3d¹⁰4s¹; Zn is not typical.",
            "Hard, dense, high-melting, alloys, interstitial compounds; paramagnetic, μ = √(n(n+2)) BM.",
            "Many oxidation states differing by one; maximum +7 at Mn (MnO₄⁻); Ni(CO)₄ has Ni(0).",
            "Complex: central ion (acceptor) + ligands (donors) by dative bonds; EAN = Z − ox. state + 2 × CN.",
            "CN 2 linear, 4 tetrahedral or square planar, 6 octahedral.",
            "CFT: octahedral field splits d into t₂g (−0.4Δo) and e_g (+0.6Δo); strong field ligands give low spin.",
            "Colour: d–d transition absorbs visible light; we see the complement. d⁰ and d¹⁰ colourless.",
            "Catalysis: variable oxidation states (Fe³⁺/Fe²⁺) and surface adsorption (Fe, V₂O₅, Pt, Ni).",
        ], "Let us recap. Transition elements have a partly filled d subshell, with chromium and copper as exceptions in configuration and zinc not a typical member. They are hard, dense, paramagnetic metals with many oxidation states, up to plus seven in manganese. Their ions form complexes through dative bonds, with shapes set by the coordination number. Crystal field theory splits the d orbitals into t two g and e g. Electrons jumping across that gap absorb visible light, giving colour. And variable oxidation states and active surfaces make them excellent catalysts.")
        self.outro("That is the transition metals. Next, we meet some of them in detail, in the studies of heavy metals: copper, zinc, mercury, iron and silver. See you in the next lesson on NEBians.")
