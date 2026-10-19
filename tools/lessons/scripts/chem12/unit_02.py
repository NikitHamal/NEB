import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

KA = 1.8e-5


def buffer_ph(k):
    """pH of 1 L of 0.10 M acetic acid + 0.10 M acetate after k × 0.010 mol HCl."""
    return 4.74 + np.log10((0.10 - 0.010 * k) / (0.10 + 0.010 * k))


def water_ph(k):
    return -np.log10(0.010 * k + 1e-7)


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 2
    TITLE = "Ionic Equilibrium"
    SUBTITLE = "Acids, bases, pH, buffers and salts"
    SECTIONS = ["Limits of Arrhenius", "Bronsted-Lowry, conjugate pairs", "Relative strength", "Lewis definition",
                "Ostwald's dilution law", "Ionic product of water", "Ka, Kb, pKa and pKb", "pH of acids and bases",
                "Solubility product", "Common ion effect", "Precipitation reactions", "Buffer solutions",
                "Indicators", "Types of salts", "Hydrolysis of salts"]
    NEXT = "Unit 3 · Chemical Kinetics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8,
                   self.p9, self.p10, self.p11, self.p12, self.p13, self.p14, self.p15, self.ending)

    # ------------------------------------------------------------------ helpers
    def two_beakers(self, left_lab, right_lab, pl0, pr0):
        bl = C.Beaker(center=[-3.3, -0.8, 0], w=2.6, h=2.8, level=0.62, color=C.universal(pl0), opacity=0.55)
        br = C.Beaker(center=[3.3, -0.8, 0], w=2.6, h=2.8, level=0.62, color=C.universal(pr0), opacity=0.55)
        ll = T(left_lab, size=28, color=th.INK, weight="SEMIBOLD").next_to(bl.g, DOWN, buff=0.25)
        rl = T(right_lab, size=28, color=th.INK, weight="SEMIBOLD").next_to(br.g, DOWN, buff=0.25)
        return bl, br, ll, rl

    def meter(self, x, getter, color=th.INK):
        box = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.0, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE).move_to([x, 1.9, 0])
        lab = T("pH", size=24, color=th.MUTED).next_to(box, LEFT, buff=0.15)
        num = DecimalNumber(getter(), num_decimal_places=2, font_size=48, color=color).move_to(box)
        num.set_z_index(3)
        num.add_updater(lambda m: m.set_value(getter()))
        return VGroup(box, lab), num

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        k = ValueTracker(0)
        bl, br, ll, rl = self.two_beakers("1 L pure water", "1 L acetate buffer", 7.0, 4.74)
        ml, nl = self.meter(-3.3, lambda: water_ph(k.get_value()))
        mr, nr = self.meter(3.3, lambda: buffer_ph(k.get_value()))
        bl.liq.add_updater(lambda m: m.set_fill(C.universal(water_ph(k.get_value()))))
        br.liq.add_updater(lambda m: m.set_fill(C.universal(buffer_ph(k.get_value()))))
        with self.say("Two beakers. On the left, one litre of pure water. On the right, one litre of a special solution, a mixture of acetic acid and sodium acetate. Both have a few drops of universal indicator, and a pH meter."):
            self.play(FadeIn(bl.g, shift=UP * 0.3), FadeIn(ll), FadeIn(br.g, shift=UP * 0.3), FadeIn(rl))
            self.add(nl, nr)
            self.play(FadeIn(ml), FadeIn(nl), FadeIn(mr), FadeIn(nr))
        drops = VGroup(*[Circle(radius=0.12, fill_color=th.CORAL, fill_opacity=1, stroke_width=0).move_to([x, 3.0, 0]) for x in (-3.3, 3.3)])
        lab = T("+ 0.010 mol HCl to each", size=26, color=th.CORAL).move_to([0, 3.0, 0])
        with self.say("Now add exactly the same thing to each: a hundredth of a mole of hydrochloric acid. Watch the meters."):
            self.play(FadeIn(drops), FadeIn(lab))
            self.play(drops.animate.shift(DOWN * 3.2), run_time=0.6, rate_func=rate_functions.ease_in_quad)
            self.remove(drops)
            self.sfx("impact", gain=-10)
            self.play(k.animate.set_value(1), run_time=3.0, rate_func=rate_functions.ease_out_cubic)
        nb = C.show_neby(self, "surprised", height=1.4, at=[0, -0.6, 0])
        with self.say("The water crashes from pH seven to pH two, a hundred thousand times more acidic. The mixture on the right barely notices: four point seven four to four point six five."):
            self.play(Indicate(nl, color=th.CORAL, scale_factor=1.2))
            self.play(Indicate(nr, color=th.MINT, scale_factor=1.2))
        with self.say("Your blood is like the right hand beaker. It sits at pH seven point four, and a drift of just zero point four either way would kill you. How does a solution refuse to change its pH? That is the question this unit will answer."):
            nb.set_state("think")
            self.wait(1.0)
        for m in (bl.liq, br.liq, nl, nr):
            m.clear_updaters()
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(bl.g, br.g, ll, rl, ml, mr, nl, nr, lab)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 2: Ionic Equilibrium. It is the longest and most examined unit in physical chemistry. Acids and bases, the pH scale, solubility products, buffers, indicators and salt hydrolysis. Almost all of it rests on one idea: reversible reactions between ions, sitting in equilibrium."):
            pass
        self.end_title(g, nb)
        self.roadmap("Fifteen short stops. Three definitions of acids and bases, and how to compare their strength. Ostwald's dilution law, the ionic product of water, and the constants K a and K b. The pH of any acid or base. Solubility product, the common ion effect and precipitation. Then buffers, indicators, and the types and hydrolysis of salts.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        e1 = chem(r"HCl \rightarrow H^+ + Cl^-", size=48).move_to([-3.0, 1.6, 0])
        e2 = chem(r"NaOH \rightarrow Na^+ + OH^-", size=48).move_to([3.0, 1.6, 0])
        d1 = T("acid: gives H⁺ in water", size=28, color=th.CORAL).next_to(e1, DOWN, buff=0.3)
        d2 = T("base: gives OH⁻ in water", size=28, color=th.SKY).next_to(e2, DOWN, buff=0.3)
        who = T("Svante Arrhenius, 1887", size=24, color=th.MUTED).to_edge(UP, buff=0.8)
        with self.say("In eighteen eighty seven, Svante Arrhenius gave the first modern definition. An acid gives hydrogen ions in water. A base gives hydroxide ions in water. It works for hydrochloric acid and sodium hydroxide. But it fails in five ways, and the board asks about every one of them."):
            self.play(FadeIn(who))
            self.play(Write(e1), FadeIn(d1))
            self.play(Write(e2), FadeIn(d2))
        self.play(FadeOut(VGroup(e1, e2, d1, d2, who)))
        # failure 1: gas phase neutralisation
        rng = np.random.default_rng(1)
        a = VGroup(*[Dot([-6 + rng.uniform(0, 1.2), rng.uniform(-0.6, 0.6), 0], radius=0.07, color=C.EL["N"]) for _ in range(14)])
        b = VGroup(*[Dot([4.8 + rng.uniform(0, 1.2), rng.uniform(-0.6, 0.6), 0], radius=0.07, color=C.EL["Cl"]) for _ in range(14)])
        la = chem(r"NH_3(g)", size=34, color=C.EL["N"]).move_to([-5.4, 1.2, 0])
        lb = chem(r"HCl(g)", size=34, color=C.EL["Cl"]).move_to([5.4, 1.2, 0])
        eq = chem(r"NH_3(g) + HCl(g) \rightarrow NH_4Cl(s)", size=40).to_edge(DOWN, buff=0.9)
        n1 = T("1. Only in water", size=34, color=th.AMBER, weight="BOLD").to_edge(UP, buff=0.8)
        with self.say("One. It is restricted to water. Let ammonia gas and hydrogen chloride gas meet in air. A white smoke of ammonium chloride forms. That is clearly a neutralisation, but there is no water and no hydroxide ion anywhere."):
            self.play(FadeIn(n1), FadeIn(a), FadeIn(b), FadeIn(la), FadeIn(lb))
            smoke = VGroup(*[Dot([rng.uniform(-0.8, 0.8), rng.uniform(-0.7, 0.7), 0], radius=0.09, color=WHITE, fill_opacity=0.85) for _ in range(28)])
            self.play(*[d.animate.move_to([rng.uniform(-0.8, 0.0), rng.uniform(-0.5, 0.5), 0]) for d in a],
                      *[d.animate.move_to([rng.uniform(0.0, 0.8), rng.uniform(-0.5, 0.5), 0]) for d in b], run_time=2.0)
            self.play(FadeOut(a), FadeOut(b), FadeIn(smoke, scale=0.5), run_time=0.8)
            self.play(Write(eq))
        self.play(FadeOut(VGroup(smoke, la, lb, eq, n1)))
        # failure 2: free proton
        n2 = T("2. Free H⁺ does not exist in water", size=34, color=th.AMBER, weight="BOLD").to_edge(UP, buff=0.8)
        p = C.proton(0.2).move_to([-3.5, 0, 0])
        w = C.water([1.0, 0, 0], r=0.45)
        h3o = C.water([1.0, 0, 0], r=0.45, plus=True)
        lab = chem(r"H_3O^+", size=44, color=th.CORAL).next_to(h3o, DOWN, buff=0.5)
        note = T("a bare proton: about 10⁻¹⁵ m across, enormous charge density", size=24, color=th.BODY).to_edge(DOWN, buff=0.9)
        with self.say("Two. A free hydrogen ion is just a bare proton, about ten to the minus fifteen metres across, with an enormous charge density. It cannot float around alone. In water, it is grabbed at once by a water molecule, forming the hydronium ion, H three O plus."):
            self.play(FadeIn(n2), FadeIn(p, scale=0.5), FadeIn(w), FadeIn(note))
            self.play(p.animate.move_to(h3o[2][2].get_center()), run_time=1.2, rate_func=rate_functions.ease_in_quad)
            self.play(FadeOut(p), FadeOut(w), FadeIn(h3o), FadeIn(lab))
        self.play(FadeOut(VGroup(n2, h3o, lab, note)))
        cards = VGroup(
            C.card(self, "3. Acids with no H", "CO₂, SO₂, AlCl₃ and BF₃ behave as acids, yet have no ionisable hydrogen.", w=4.1, h=2.6, color=th.CORAL),
            C.card(self, "4. Bases with no OH", "NH₃, Na₂CO₃, CH₃NH₂ and NaHCO₃ turn red litmus blue, with no OH in the formula.", w=4.1, h=2.6, color=th.SKY),
            C.card(self, "5. Solvent ignored", "Dry HCl gas does not redden dry blue litmus, and HCl in benzene is not acidic.", w=4.1, h=2.6, color=th.MINT),
        ).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        with self.say("Three. Carbon dioxide, sulphur dioxide, aluminium chloride and boron trifluoride all act as acids, but contain no hydrogen to give. Four. Ammonia and sodium carbonate are bases, but have no hydroxide group. And five. It ignores the solvent. Dry hydrogen chloride gas does not even redden dry litmus. The water is an active partner, not a spectator.") as v:
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.3), run_time=0.5)
                self.hold(v.dur / 3 - 0.6)
        nb = C.show_neby(self, "think", height=1.3, corner=UR, buff=0.8)
        with self.say("We need a better definition. Two chemists found one in the same year."):
            self.wait(0.3)
        C.hide_neby(self, nb)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        d = self.callout("key", "Bronsted-Lowry (1923): an acid is a proton donor; a base is a proton acceptor. An acid-base reaction is a proton transfer.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("In nineteen twenty three, Bronsted and Lowry defined an acid as a proton donor, and a base as a proton acceptor. An acid base reaction is nothing more than a proton moving from one species to another."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        y = -1.1
        acid = VGroup(chem(r"CH_3COO", size=42), C.proton(0.2)).arrange(RIGHT, buff=0.05).move_to([-4.6, y, 0])
        w = C.water([-1.6, y, 0], r=0.4)
        arrow = M(r"\rightleftharpoons", size=60).move_to([0.2, y, 0])
        plus1 = M("+", size=48).move_to([-2.9, y, 0])
        h3o = C.water([2.0, y, 0], r=0.4, plus=True)
        ac = chem(r"CH_3COO^-", size=42).move_to([4.9, y, 0])
        plus2 = M("+", size=48).move_to([3.4, y, 0])
        with self.say("Acetic acid in water. The acid hands its proton to a water molecule. Water, here, is the base."):
            self.play(FadeIn(acid), FadeIn(plus1), FadeIn(w))
            self.play(FadeIn(arrow))
            pc = acid[1].copy()
            self.add(pc)
            self.play(TransformFromCopy(w, h3o), pc.animate.move_to(h3o[2][2].get_center()), run_time=1.4)
            self.play(FadeOut(pc), TransformFromCopy(acid[0], ac), FadeIn(plus2))
        tags = VGroup(T("acid", size=24, color=th.CORAL).next_to(acid, UP, buff=0.35), T("base", size=24, color=th.SKY).next_to(w, UP, buff=0.3),
                      T("acid", size=24, color=th.CORAL).next_to(h3o, UP, buff=0.3), T("base", size=24, color=th.SKY).next_to(ac, UP, buff=0.3))
        br1 = CurvedArrow(acid[0].get_bottom() + DOWN * 0.3, ac.get_bottom() + DOWN * 0.3, angle=TAU / 7, color=th.AMBER)
        br2 = CurvedArrow(w.get_bottom() + DOWN * 0.3, h3o.get_bottom() + DOWN * 0.3, angle=TAU / 5, color=th.MINT)
        cp = T("conjugate pairs: differ by one proton", size=26, color=th.AMBER).to_edge(DOWN, buff=0.55)
        with self.say("But the reaction is reversible. In the backward direction, hydronium gives a proton back to acetate. So there are two acids and two bases. Acetic acid and acetate differ by exactly one proton: they are a conjugate acid base pair. Water and hydronium are the other pair."):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tags], lag_ratio=0.3))
            self.play(Create(br1), Create(br2))
            self.play(FadeIn(cp))
        self.play(FadeOut(VGroup(d, acid[0], plus1, w, arrow, h3o, ac, plus2, tags, br1, br2, cp)))
        rows = [["Acid", "Conjugate base", "Base", "Conjugate acid"],
                ["HCl", "Cl⁻", "H₂O", "H₃O⁺"], ["CH₃COOH", "CH₃COO⁻", "NH₃", "NH₄⁺"],
                ["H₂SO₄", "HSO₄⁻", "OH⁻", "H₂O"], ["HSO₄⁻", "SO₄²⁻", "CO₃²⁻", "HCO₃⁻"],
                ["H₂CO₃", "HCO₃⁻", "HCO₃⁻", "H₂CO₃"], ["H₃O⁺", "H₂O", "H₂PO₄⁻", "H₃PO₄"]]
        tb = C.table(rows, [2.6, 3.0, 2.6, 3.0], row_h=0.6, size=26, colors=[th.CORAL, th.SKY, th.SKY, th.CORAL]).move_to(UP * 0.5)
        with self.say("Here are pairs you should know. Hydrochloric acid and chloride. Ammonia and ammonium. Hydroxide and water. Now look for species in both columns: water, hydrogen carbonate, hydrogen sulphate. They can give a proton or take one. They are called amphiprotic.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 14)
            amph = VGroup()
            for (i, k) in [(1, 3), (3, 4), (3, 2), (4, 1), (4, 4), (5, 2), (5, 3), (6, 2), (6, 3)]:
                amph.add(SurroundingRectangle(tb[i][k], color=th.AMBER, buff=0.04))
            self.play(Create(amph))
        auto = chem(r"H_2O + H_2O \rightleftharpoons H_3O^+ + OH^-", size=40, color=th.AMBER).next_to(tb, DOWN, buff=0.5)
        with self.say("Water is the most important amphiprotic species of all. One water molecule can even give a proton to another."):
            nb = C.show_neby(self, "wink", height=1.3, corner=DR)
            self.play(Write(auto))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(tb, amph, auto)))
        care = self.callout("careful", "Cl⁻ is the conjugate base of HCl, yet NaCl solution is neutral. HCl is so strong that Cl⁻ is an extremely weak base. 'Conjugate base' is a relationship, not a strength.", width=11, size=27)
        with self.say("A careful point. Chloride is the conjugate base of hydrochloric acid, yet salt water is neutral. Because hydrochloric acid is so strong, chloride is an extremely weak base, too weak to take protons back from water. Conjugate describes a relationship, not a strength. And one limitation remains: Bronsted needs a proton, so it cannot explain boron trifluoride reacting with ammonia."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        eq = chem(r"HA + H_2O \rightleftharpoons H_3O^+ + A^-", size=44).to_edge(UP, buff=0.8)
        ka = M(r"K_a = \frac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]}", size=48).next_to(eq, DOWN, buff=0.4)
        with self.say("The strength of an acid is how far it pushes its proton onto water. That extent is measured by the acid dissociation constant, K a. A larger K a, or a smaller p K a, means a stronger acid."):
            self.play(Write(eq))
            self.play(Write(ka))
        self.play(FadeOut(VGroup(eq, ka)))
        acids = [("HSO₄⁻", "SO₄²⁻", 1.92), ("HF", "F⁻", 3.17), ("HCOOH", "HCOO⁻", 3.75), ("CH₃COOH", "CH₃COO⁻", 4.74),
                 ("H₂CO₃", "HCO₃⁻", 6.35), ("HCN", "CN⁻", 9.31)]
        top_y = 2.4
        sc = 0.55

        def yk(pka):
            return top_y - (pka - 1.5) * sc
        axl = Arrow([-1.2, yk(1.5), 0], [-1.2, yk(10.2), 0], buff=0, color=th.CORAL, stroke_width=4)
        axr = Arrow([1.2, yk(10.2), 0], [1.2, yk(1.5), 0], buff=0, color=th.SKY, stroke_width=4)
        hl = T("stronger acid", size=22, color=th.CORAL).next_to(axl.get_start(), UP, buff=0.12)
        hr = T("stronger base", size=22, color=th.SKY).next_to(axr.get_start(), RIGHT, buff=0.2)
        rows = VGroup()
        for a, b, pk in acids:
            y = yk(pk)
            la = VGroup(T(a, size=26, color=th.CORAL, weight="SEMIBOLD"), T(f"pKa {pk:.2f}", size=20, color=th.MUTED)).arrange(RIGHT, buff=0.2)
            la.next_to([-1.4, y, 0], LEFT, buff=0.1)
            lb = VGroup(T(b, size=26, color=th.SKY, weight="SEMIBOLD"), T(f"pKb {14 - pk:.2f}", size=20, color=th.MUTED)).arrange(RIGHT, buff=0.2)
            lb.next_to([1.4, y, 0], RIGHT, buff=0.1)
            ln = DashedLine([-1.3, y, 0], [1.3, y, 0], color=th.FAINT, stroke_width=2)
            rows.add(VGroup(la, ln, lb))
        with self.say("Line up some acids by p K a, strongest at the top. Hydrogen sulphate, hydrofluoric, formic, acetic, carbonic, hydrocyanic acid. Now put each conjugate base beside its acid.") as v:
            self.play(GrowArrow(axl), FadeIn(hl))
            for r in rows:
                self.play(FadeIn(r[0], shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur / 8 - 0.4)
        with self.say("The pattern is perfect. The stronger the acid, the weaker its conjugate base. Sulphate hardly wants a proton back. Cyanide wants it badly."):
            self.play(GrowArrow(axr), FadeIn(hr))
            self.play(LaggedStart(*[AnimationGroup(Create(r[1]), FadeIn(r[2], shift=LEFT * 0.2)) for r in rows], lag_ratio=0.25), run_time=2.5)
        kk = M(r"K_a \times K_b = K_w, \qquad pK_a + pK_b = 14", size=40, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("In numbers, K a times K b equals K w for any conjugate pair, so p K a plus p K b equals fourteen at twenty five degrees. We will prove that shortly."):
            self.play(Write(kk))
        self.play(FadeOut(VGroup(axl, axr, hl, hr, rows, kk)))
        head, prob = C.example_head(self, "Compare the strengths of acetic acid (Ka = 1.8 × 10⁻⁵) and hydrocyanic acid (Ka = 4.9 × 10⁻¹⁰) at the same concentration.")
        st = C.steps(r"\frac{\text{strength}_1}{\text{strength}_2} = \frac{\alpha_1}{\alpha_2} = \sqrt{\frac{K_{a1}}{K_{a2}}}",
                     r"= \sqrt{\frac{1.8\times10^{-5}}{4.9\times10^{-10}}} = \sqrt{3.67\times10^{4}} \approx 192", size=42).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[1].set_color(th.AMBER)
        with self.say("How much stronger is acetic acid than hydrocyanic acid, at the same concentration? Strength goes as the degree of ionisation, which, as we will see, is the square root of K a over C. So the ratio is the square root of the ratio of the K a values."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("One point eight times ten to the minus five, over four point nine times ten to the minus ten, is about thirty six thousand seven hundred. Its square root is about one hundred and ninety two. Acetic acid is about a hundred and ninety times stronger."):
            self.play(Write(st[1]))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.levelling()

    def levelling(self):
        title = T("The levelling effect", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        names = ["HClO₄", "HI", "HBr", "HCl", "HNO₃"]
        true_h = [3.2, 2.7, 2.2, 1.7, 1.2]
        base = -2.4
        bars = VGroup()
        for i, (n, h) in enumerate(zip(names, true_h)):
            x = -4.6 + i * 2.3
            b = Rectangle(width=1.2, height=2.6, fill_color=th.CORAL, fill_opacity=0.8, stroke_width=0).move_to([x, base, 0], aligned_edge=DOWN)
            l = T(n, size=26, color=th.INK, weight="SEMIBOLD").next_to([x, base, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, l))
        cap = T("in water: all ionise completely, all look equal", size=26, color=th.BODY).next_to(title, DOWN, buff=0.3)
        cap2 = T("in glacial acetic acid: the true order appears", size=26, color=th.AMBER).next_to(title, DOWN, buff=0.3)
        with self.say("One more idea. Perchloric, hydroiodic, hydrobromic, hydrochloric and nitric acids all look equally strong in water. Each gives its proton to water completely, and the strongest acid that can exist in water is hydronium itself. Water levels them."):
            self.play(FadeIn(title), FadeIn(cap))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.15), *[FadeIn(b[1]) for b in bars])
        with self.say("Dissolve them in a weaker base, like glacial acetic acid, and the true order appears. Perchloric, then hydroiodic, hydrobromic, hydrochloric, and nitric acid."):
            self.play(FadeOut(cap), FadeIn(cap2))
            self.play(*[b[0].animate.stretch_to_fit_height(h).align_to([0, base, 0], DOWN) for b, h in zip(bars, true_h)], run_time=1.5)
        self.play(FadeOut(VGroup(title, cap2, bars)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        d = self.callout("key", "Lewis: an acid accepts a lone pair of electrons; a base donates a lone pair. Neutralisation forms a coordinate (dative) bond.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("Lewis took the proton out of the definition altogether. A Lewis acid accepts a lone pair of electrons. A Lewis base donates one. Neutralisation is the formation of a coordinate bond between them."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        bc = np.array([-2.6, -1.3, 0])
        b = C.atom("B", r=0.42, color="#FFB0B0").move_to(bc)
        fs = VGroup(*[C.atom("F", r=0.3, color="#9BE7A0").move_to(bc + 1.1 * np.array([np.cos(a), np.sin(a), 0])) for a in (np.pi / 2, np.pi * 7 / 6, np.pi * 11 / 6)])
        fb = VGroup(*[Line(bc, f.get_center(), color=th.MUTED, stroke_width=5) for f in fs])
        empty = Circle(radius=0.22, stroke_color=th.AMBER, stroke_width=3).set_stroke(opacity=0.9).move_to(bc + RIGHT * 0.75)
        nc = np.array([2.4, -1.3, 0])
        n = C.atom("N", r=0.42).move_to(nc)
        hs = VGroup(*[C.atom("H", r=0.24).move_to(nc + 1.0 * np.array([np.cos(a), np.sin(a), 0])) for a in (np.pi / 2, np.pi * 3 / 2, 0)])
        nb_ = VGroup(*[Line(nc, h.get_center(), color=th.MUTED, stroke_width=5) for h in hs])
        lp = VGroup(Dot(nc + LEFT * 0.62 + UP * 0.1, radius=0.07, color=th.AMBER), Dot(nc + LEFT * 0.62 + DOWN * 0.1, radius=0.07, color=th.AMBER))
        l1 = T("BF₃: only 6 electrons around B", size=24, color=th.CORAL).next_to(VGroup(fs, b), DOWN, buff=0.35)
        l2 = T("NH₃: a lone pair on N", size=24, color=th.SKY).next_to(VGroup(hs, n), DOWN, buff=0.35)
        mol1 = VGroup(fb, fs, b, empty)
        mol2 = VGroup(nb_, n, hs, lp)
        with self.say("Boron trifluoride has only six electrons around boron, an empty space in its octet. Ammonia has a lone pair on nitrogen, ready to share."):
            self.play(FadeIn(mol1), FadeIn(l1))
            self.play(FadeIn(mol2), FadeIn(l2))
            self.play(Indicate(empty, color=th.AMBER), Indicate(lp, color=th.AMBER))
        with self.say("Bring them together. The nitrogen lone pair moves into boron's empty orbital, and a dative bond forms, drawn as an arrow from nitrogen to boron. No proton anywhere, yet this is an acid base reaction."):
            self.play(FadeOut(VGroup(l1, l2)))
            self.play(mol1.animate.shift(RIGHT * 1.3), mol2.animate.shift(LEFT * 1.6), run_time=1.2)
            arr = Arrow(n.get_left(), b.get_right(), buff=0.05, color=th.AMBER, stroke_width=6)
            self.play(FadeOut(empty), lp.animate.move_to(arr.get_center()).set_opacity(0), GrowArrow(arr))
            self.sfx("pop")
            prod = chem(r"F_3B \leftarrow NH_3", size=48, color=th.AMBER).to_edge(DOWN, buff=0.5)
            self.play(Write(prod))
        self.play(FadeOut(VGroup(d, mol1, mol2, arr, prod)))
        rows = [["Lewis acids (pair acceptors)", "Lewis bases (pair donors)"],
                ["incomplete octet: BF₃, AlCl₃, BeCl₂", "lone pair: NH₃, H₂O, R–OH, R–NH₂"],
                ["cations: H⁺, Ag⁺, Cu²⁺, Fe³⁺", "anions: OH⁻, Cl⁻, CN⁻, F⁻"],
                ["expandable octet: SiF₄, PF₅, SF₄", "π electrons: C₂H₄, C₆H₆"],
                ["CO₂, SO₂, SO₃", "carbanions, alkoxides"]]
        tb = C.table(rows, [6.0, 6.0], row_h=0.62, size=24, colors=[th.CORAL, th.SKY]).move_to(UP * 1.0)
        cx = VGroup(chem(r"Ag^+ + 2NH_3 \rightarrow [Ag(NH_3)_2]^+", size=34), chem(r"Cu^{2+} + 4NH_3 \rightarrow [Cu(NH_3)_4]^{2+}", size=34)).arrange(RIGHT, buff=0.8).next_to(tb, DOWN, buff=0.45)
        with self.say("Lewis acids include molecules with incomplete octets, simple metal cations, and molecules that can expand their octet. Lewis bases include anything with a lone pair, anions, and even pi electrons. Complex formation, like silver ion with ammonia, or copper ion with ammonia, is a Lewis neutralisation.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 7 - 0.4)
            self.play(Write(cx))
        self.play(FadeOut(VGroup(tb, cx)))
        rows2 = [["", "Arrhenius", "Bronsted-Lowry", "Lewis"],
                 ["Acid", "gives H⁺ in water", "proton donor", "e⁻-pair acceptor"],
                 ["Base", "gives OH⁻ in water", "proton acceptor", "e⁻-pair donor"],
                 ["Solvent", "water only", "any, or none", "any, or none"],
                 ["Scope", "narrowest", "wider", "widest"],
                 ["Weakness", "no non-aqueous cases", "fails for BF₃, AlCl₃", "too wide; no strength order"]]
        tb2 = C.table(rows2, [2.2, 3.4, 3.4, 3.6], row_h=0.64, size=23, colors=[th.MUTED, th.AMBER, th.SKY, th.MINT]).move_to(DOWN * 0.1)
        nb = C.show_neby(self, "read", height=1.3)
        with self.say("Compare the three. Arrhenius is the narrowest, tied to water. Bronsted and Lowry is wider. Lewis is the widest, but it is so wide that it says nothing about the relative strengths of acids, and it even struggles to call hydrochloric acid an acid in the strict sense.") as v:
            for r in tb2:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 6 - 0.35)
        C.hide_neby(self, nb)
        self.play(FadeOut(tb2))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("A weak electrolyte: partly ionised", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["", "AB", "⇌", "A⁺", "+", "B⁻"], ["initial", "C", "", "0", "", "0"], ["equilibrium", "C(1 − α)", "", "Cα", "", "Cα"]]
        tb = C.table(rows, [2.6, 2.0, 0.7, 1.6, 0.6, 1.6], row_h=0.66, size=28, colors=[th.MUTED, th.INK, th.INK, th.SKY, th.INK, th.CORAL]).next_to(title, DOWN, buff=0.45)
        with self.say("Ostwald's dilution law. Take a weak electrolyte A B at concentration C. At equilibrium, a fraction alpha, the degree of ionisation, has split into ions. So the ions are C alpha each, and the molecules left are C times one minus alpha."):
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.6)
        der = VGroup(
            M(r"K = \frac{C\alpha \cdot C\alpha}{C(1-\alpha)} = \frac{C\alpha^{2}}{1-\alpha}", size=40),
            M(r"\alpha \ll 1 \;\Rightarrow\; K \approx C\alpha^{2}", size=40),
            M(r"\alpha = \sqrt{\frac{K}{C}} = \sqrt{K V}", size=52, color=th.AMBER),
        ).arrange(DOWN, buff=0.28).next_to(tb, DOWN, buff=0.3)
        with self.say("The law of mass action gives K equals C alpha squared over one minus alpha. For a weak electrolyte alpha is tiny, so one minus alpha is almost one, and K is C alpha squared."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
        with self.say("So alpha equals the square root of K over C. Since C is one over the volume V containing one mole, alpha is also the square root of K V."):
            self.sfx("impact", gain=-12)
            self.play(Write(der[2]))
            self.play(Circumscribe(der[2], color=th.AMBER))
        self.play(FadeOut(VGroup(title, tb, der[:2])), der[2].animate.scale(0.75).to_corner(UR, buff=0.8))
        Vt = ValueTracker(1.0)
        K = 1.8e-5
        bk = C.Beaker(center=[-3.6, -0.6, 0], w=3.0, h=3.6, level=0.5, color=C.WATER, opacity=0.2)
        bk.liq.add_updater(lambda m: m.stretch_to_fit_height(3.6 * (0.18 + 0.14 * np.log10(Vt.get_value()))).align_to(bk.outline, DOWN))
        rng = np.random.default_rng(4)
        N = 30
        home = [np.array([rng.uniform(-1.2, 1.2), rng.uniform(0.0, 1.0), 0]) for _ in range(N)]
        order = rng.permutation(N)

        def parts():
            frac = min(1.0, 5 * np.sqrt(K * Vt.get_value()))
            nion = int(round(frac * N))
            hmax = 3.6 * (0.18 + 0.14 * np.log10(Vt.get_value()))
            g = VGroup()
            for k, i in enumerate(order):
                p = bk.c + np.array([home[i][0], -1.65 + home[i][1] * (hmax - 0.3), 0])
                if k < nion:
                    g.add(Dot(p + LEFT * 0.09, radius=0.06, color=th.SKY), Dot(p + RIGHT * 0.09, radius=0.06, color=th.CORAL))
                else:
                    g.add(VGroup(Dot(p + LEFT * 0.06, radius=0.06, color=th.SKY), Dot(p + RIGHT * 0.06, radius=0.06, color=th.CORAL), Line(p + LEFT * 0.06, p + RIGHT * 0.06, color=WHITE, stroke_width=2)))
            return g
        pg = always_redraw(parts)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 14, 2], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": False}).move_to([2.6, -0.9, 0])
        xl = T("dilution: log V (1, 10, 100, 1000 L)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.2)
        x5 = T("ionised pairs drawn ×5", size=18, color=th.MUTED).next_to(bk.g, DOWN, buff=0.15)
        yl = T("α (%)", size=22, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        curve = ax.plot(lambda x: 100 * np.sqrt(K * 10 ** x), x_range=[0, 3, 0.02], color=th.AMBER, stroke_width=4)
        dot = always_redraw(lambda: Dot(ax.c2p(np.log10(Vt.get_value()), 100 * np.sqrt(K * Vt.get_value())), color=WHITE, radius=0.08))
        ro = DecimalNumber(0, num_decimal_places=2, font_size=36, color=th.AMBER, unit=r"\,\%")
        ro.add_updater(lambda m: m.set_value(100 * np.sqrt(K * Vt.get_value())).next_to(ax.c2p(0.3, 13), RIGHT, buff=0))
        with self.say("Watch it happen with acetic acid, one mole in V litres. At one litre only about zero point four percent is ionised. Now dilute: ten litres, a hundred, a thousand."):
            self.play(FadeIn(bk.g))
            self.add(bk.liq, pg)
            self.play(FadeIn(pg), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(x5))
            self.add(dot, ro)
            self.play(Create(curve), FadeIn(dot), FadeIn(ro))
            self.play(Vt.animate.set_value(1000), run_time=5, rate_func=lambda t: t)
        with self.say("The more you dilute, the more it ionises. A hundred times more dilute means ten times more ionised, because alpha goes as the square root of the dilution. The law holds for weak electrolytes only. Strong electrolytes like sodium chloride are fully ionised already, so there is no equilibrium to shift."):
            self.play(Indicate(ro, color=th.AMBER))
            self.wait(1)
        bk.liq.clear_updaters()
        ro.clear_updaters()
        self.play(FadeOut(VGroup(bk.g, ax, xl, yl, x5, curve, ro, der[2])), FadeOut(pg), FadeOut(dot))
        self.remove(pg, dot)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rng = np.random.default_rng(6)
        grid = VGroup()
        for i in range(9):
            for j in range(5):
                grid.add(C.water([-5.6 + i * 1.4, 2.0 - j * 1.0, 0], r=0.22))
        with self.say("Pure water conducts electricity, very slightly. So it must contain a few ions. Every now and then, one water molecule passes a proton to another."):
            self.play(LaggedStart(*[FadeIn(w, scale=0.6) for w in grid], lag_ratio=0.01), run_time=1.5)
            for _ in range(3):
                i = rng.integers(0, len(grid) - 1)
                a, b = grid[i], grid[i + 1]
                self.play(Indicate(a, color=th.CORAL, scale_factor=1.3), Indicate(b, color=th.SKY, scale_factor=1.3), run_time=0.6)
        note = T("only about 2 in every 10⁹ molecules are ionised", size=28, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("But it is rare. Only about two water molecules in every billion are ionised at any moment."):
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(grid, note)))
        eqs = VGroup(
            chem(r"H_2O + H_2O \rightleftharpoons H_3O^+ + OH^-", size=42),
            M(r"K = \frac{[\mathrm{H^+}][\mathrm{OH^-}]}{[\mathrm{H_2O}]}", size=44),
            M(r"K_w = K[\mathrm{H_2O}] = [\mathrm{H^+}][\mathrm{OH^-}]", size=48, color=th.AMBER),
            M(r"K_w = 1.0\times10^{-14}\ \text{at } 25^{\circ}\mathrm{C}", size=44, color=th.AMBER),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        with self.say("Write the equilibrium constant. The concentration of water itself, about fifty five point five moles per litre, hardly changes, so we fold it into the constant. The result is the ionic product of water, K w, equal to the concentration of hydrogen ions times the concentration of hydroxide ions."):
            for e in eqs[:3]:
                self.play(Write(e), run_time=1.0)
        with self.say("At twenty five degrees it is one times ten to the minus fourteen. In pure water the two are equal, ten to the minus seven moles per litre each. And this product holds in every aqueous solution, not just pure water."):
            self.play(Write(eqs[3]))
        pw = M(r"pK_w = pH + pOH = 14", size=50, color=th.MINT).next_to(eqs, DOWN, buff=0.4)
        with self.say("Take minus log of both sides, and you get p H plus p O H equals fourteen."):
            self.play(Write(pw))
        self.play(FadeOut(VGroup(eqs, pw)))
        temps = np.array([0, 25, 50, 100])
        pkw = np.array([14.94, 14.00, 13.26, 12.29])
        Tt = ValueTracker(0)

        def pkw_at(t):
            return float(np.interp(t, temps, pkw))
        ax = NumberLine(x_range=[5.5, 8, 0.5], length=9, include_numbers=True, color=th.MUTED, font_size=32).move_to([0, -1.6, 0])
        axl = T("pH of pure, neutral water", size=24, color=th.MUTED).next_to(ax, DOWN, buff=0.45)
        mark = always_redraw(lambda: Triangle(fill_color=th.MINT, fill_opacity=1, stroke_width=0).scale(0.18).rotate(PI).next_to(ax.n2p(pkw_at(Tt.get_value()) / 2), UP, buff=0.05))
        tv = DecimalNumber(0, num_decimal_places=0, font_size=56, color=th.CORAL, unit=r"^{\circ}\mathrm{C}")
        tv.add_updater(lambda m: m.set_value(Tt.get_value()).move_to([-3.2, 1.4, 0]))
        pv = DecimalNumber(7.47, num_decimal_places=2, font_size=56, color=th.MINT)
        pv.add_updater(lambda m: m.set_value(pkw_at(Tt.get_value()) / 2).move_to([3.2, 1.4, 0]))
        hdr = VGroup(T("temperature", size=24, color=th.MUTED).move_to([-3.2, 2.3, 0]), T("pH of pure water", size=24, color=th.MUTED).move_to([3.2, 2.3, 0]))
        with self.say("Ionisation of water absorbs heat, so K w grows with temperature. Watch the pH of perfectly pure water as we heat it from zero to a hundred degrees."):
            self.add(mark, tv, pv)
            self.play(Create(ax), FadeIn(axl), FadeIn(hdr), FadeIn(mark), FadeIn(tv), FadeIn(pv))
            self.play(Tt.animate.set_value(100), run_time=4.5, rate_func=linear)
        nb = C.show_neby(self, "surprised", height=1.3)
        care = T("At 100 °C, pH 6.14, and still neutral: [H⁺] = [OH⁻]", size=28, color=th.AMBER).to_edge(DOWN, buff=0.45)
        with self.say("At a hundred degrees, pure water has pH six point one four. Is boiling water acidic? No! It is still neutral, because hydrogen and hydroxide ions are still equal. Neutral means equal, not pH seven. Seven is only the neutral point at twenty five degrees."):
            self.play(FadeIn(care, shift=UP * 0.2))
        C.hide_neby(self, nb)
        tv.clear_updaters()
        pv.clear_updaters()
        self.play(FadeOut(VGroup(ax, axl, hdr, tv, pv, care)), FadeOut(mark))
        self.remove(mark)

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        defs = VGroup(
            VGroup(chem(r"HA \rightleftharpoons H^+ + A^-", size=38), M(r"K_a = \frac{[\mathrm{H^+}][\mathrm{A^-}]}{[\mathrm{HA}]}", size=44)).arrange(DOWN, buff=0.3),
            VGroup(chem(r"BOH \rightleftharpoons B^+ + OH^-", size=38), M(r"K_b = \frac{[\mathrm{B^+}][\mathrm{OH^-}]}{[\mathrm{BOH}]}", size=44)).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=1.4).move_to(UP * 1.2)
        with self.say("For a weak acid H A, the dissociation constant K a is the concentration of hydrogen ions times anions, over un-ionised acid. For a weak base B O H, K b is defined the same way with hydroxide. Both depend on temperature, but not on concentration. And combined with Ostwald's law, K a equals C alpha squared."):
            self.play(FadeIn(defs[0], shift=UP * 0.2))
            self.play(FadeIn(defs[1], shift=UP * 0.2))
        pk = VGroup(M(r"pK_a = -\log K_a", size=46, color=th.AMBER), M(r"pK_b = -\log K_b", size=46, color=th.AMBER)).arrange(RIGHT, buff=1.6).next_to(defs, DOWN, buff=0.6)
        ex = M(r"K_a(\mathrm{CH_3COOH}) = 1.8\times10^{-5} \;\Rightarrow\; pK_a = 5 - \log 1.8 = 4.74", size=38).next_to(pk, DOWN, buff=0.45)
        with self.say("Because these constants span many powers of ten, we use their negative logarithms. p K a is minus log K a. For acetic acid, K a is one point eight times ten to the minus five, so p K a is five minus log one point eight, four point seven four. Remember: small p K a, strong acid."):
            self.play(Write(pk))
            self.play(Write(ex))
        self.play(FadeOut(VGroup(defs, pk, ex)))
        title = T("Proof: Ka × Kb = Kw", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        a = M(r"K_a", r"=", r"{[\mathrm{H^+}]", r"[\mathrm{CH_3COO^-}]", r"\over", r"[\mathrm{CH_3COOH}]}", size=42)
        b = M(r"K_b", r"=", r"{[\mathrm{CH_3COOH}]", r"[\mathrm{OH^-}]", r"\over", r"[\mathrm{CH_3COO^-}]}", size=42)
        ea = chem(r"CH_3COOH \rightleftharpoons H^+ + CH_3COO^-", size=32, color=th.MUTED)
        eb = chem(r"CH_3COO^- + H_2O \rightleftharpoons CH_3COOH + OH^-", size=32, color=th.MUTED)
        grp = VGroup(VGroup(ea, a).arrange(DOWN, buff=0.2), VGroup(eb, b).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.5).next_to(title, DOWN, buff=0.4)
        with self.say("Here is the proof. Take acetic acid and its conjugate base, acetate. Write K a for the acid, and K b for acetate taking a proton from water."):
            self.play(FadeIn(title))
            self.play(FadeIn(grp[0]))
            self.play(FadeIn(grp[1]))
        prod = M(r"K_a \times K_b = [\mathrm{H^+}][\mathrm{OH^-}] = K_w", size=52, color=th.AMBER).to_edge(DOWN, buff=0.8)
        crosses = VGroup(*[Line(m.get_corner(DL), m.get_corner(UR), color=th.CORAL, stroke_width=5) for m in (a[3], a[5], b[2], b[5])])
        with self.say("Multiply them. Acetate on top of the first cancels acetate below in the second. Acetic acid below the first cancels acetic acid on top of the second. All that is left is hydrogen ion times hydroxide ion, which is K w."):
            self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.3), run_time=1.6)
            self.sfx("impact", gain=-12)
            self.play(Write(prod))
        pp = M(r"pK_a + pK_b = 14", size=44, color=th.MINT).next_to(prod, UP, buff=0.3)
        with self.say("Take logarithms, and p K a plus p K b equals fourteen. Acetic acid, four point seven four, so acetate has p K b nine point two six."):
            self.play(FadeIn(pp, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, grp, prod, crosses, pp)))

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        d = M(r"pH = -\log_{10}[\mathrm{H^+}], \qquad [\mathrm{H^+}] = 10^{-pH}", size=46).to_edge(UP, buff=0.8)
        with self.say("Hydrogen ion concentrations run from about ten moles per litre down to ten to the minus fifteen. In nineteen oh nine, Sorensen tamed that range with a logarithm. p H is minus the log, base ten, of the hydrogen ion concentration."):
            self.play(Write(d))
        nl = NumberLine(x_range=[0, 14, 1], length=12, include_numbers=True, font_size=24, color=th.MUTED).move_to([0, -0.4, 0])
        bands = VGroup(*[Rectangle(width=12 / 14, height=0.35, fill_color=C.universal(i + 0.5), fill_opacity=0.9, stroke_width=0).move_to(nl.n2p(i + 0.5) + UP * 0.35) for i in range(14)])
        p = ValueTracker(1.0)
        ptr = always_redraw(lambda: Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI).move_to(nl.n2p(p.get_value()) + UP * 0.8))
        hr = always_redraw(lambda: M(r"[\mathrm{H^+}] = 10^{-" + f"{p.get_value():.0f}" + r"}\ \mathrm{mol\,L^{-1}}", size=38, color=th.INK).move_to([0, 1.6, 0]))
        items = [(2, "lemon juice"), (3, "vinegar"), (7, "pure water"), (7.4, "blood"), (8.3, "baking soda"), (11.5, "household ammonia")]
        tags = VGroup()
        for i, (v, n) in enumerate(items):
            t = T(n, size=20, color=th.BODY).next_to(nl.n2p(v), DOWN, buff=[0.55, 1.0, 0.55, 1.0, 1.45, 0.55][i])
            tags.add(VGroup(Line(nl.n2p(v) + DOWN * 0.15, t.get_top(), color=th.FAINT, stroke_width=2), t))
        with self.say("Each step of one on the p H scale is a factor of ten in hydrogen ion concentration. Slide from p H one to p H thirteen, and the hydrogen ion concentration falls a million million times."):
            self.play(Create(nl), FadeIn(bands))
            self.add(ptr, hr)
            self.play(FadeIn(ptr), FadeIn(hr))
            self.play(p.animate.set_value(13), run_time=4, rate_func=lambda t: np.round(t * 12) / 12)
        with self.say("Lemon juice is around two, vinegar around three, pure water seven, blood seven point four, baking soda solution about eight, household ammonia about eleven or twelve. Below seven, acidic. Above, basic."):
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.25), run_time=2.5)
        self.play(FadeOut(VGroup(d, nl, bands, tags)), FadeOut(ptr), FadeOut(hr))
        self.remove(ptr, hr)
        title = T("Four formulas", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        f = VGroup(
            VGroup(T("strong acid", size=26, color=th.CORAL, weight="BOLD"), M(r"[\mathrm{H^+}] = C \times \text{basicity},\ \ pH = -\log[\mathrm{H^+}]", size=36)),
            VGroup(T("weak acid", size=26, color=th.CORAL, weight="BOLD"), M(r"[\mathrm{H^+}] = \sqrt{K_aC},\ \ pH = \tfrac12(pK_a - \log C)", size=36)),
            VGroup(T("strong base", size=26, color=th.SKY, weight="BOLD"), M(r"[\mathrm{OH^-}] = C \times \text{acidity},\ \ pH = 14 - pOH", size=36)),
            VGroup(T("weak base", size=26, color=th.SKY, weight="BOLD"), M(r"[\mathrm{OH^-}] = \sqrt{K_bC},\ \ pOH = \tfrac12(pK_b - \log C)", size=36)),
        )
        for r in f:
            r.arrange(RIGHT, buff=0.4)
        f.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.5)
        with self.say("Four formulas cover every case. A strong acid is fully ionised, so hydrogen ion equals concentration times basicity. A weak acid gives the square root of K a C, which in logs is half of p K a minus log C. Bases work the same way through hydroxide, then p H is fourteen minus p O H.") as v:
            self.play(FadeIn(title))
            for r in f:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.7)
        whyw = M(r"[\mathrm{H^+}] = C\alpha = C\sqrt{\tfrac{K_a}{C}} = \sqrt{K_aC}", size=38, color=th.AMBER).to_edge(DOWN, buff=0.6)
        with self.say("Where does the square root come from? From Ostwald: hydrogen ion is C alpha, and alpha is root K a over C. Multiply, and you get root K a C."):
            self.play(Write(whyw))
        self.play(FadeOut(VGroup(title, f, whyw)))
        self.example_21()
        self.example_22()
        self.example_23()
        care = self.callout("careful", "pH is not confined to 0–14: 2 M HCl has pH −0.30, 5 M NaOH has pH 14.7. And [H⁺] must be in mol L⁻¹, never g L⁻¹.", width=11, size=28)
        with self.say("Two traps. p H is not stuck between zero and fourteen. Two molar hydrochloric acid has p H minus zero point three. Five molar sodium hydroxide has p H fourteen point seven. And the concentration must be in moles per litre, so convert any grams per litre first."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))
        self.quiz("The pH of 0.005 M Ca(OH)₂ at 25 °C is",
                  ["2.3", "11.7", "12", "13"], 2,
                  "Your turn. What is the p H of zero point zero zero five molar calcium hydroxide? Pause and think.",
                  "C, twelve. Calcium hydroxide gives two hydroxide ions, so hydroxide is zero point zero one molar, p O H is two, and p H is fourteen minus two. Eleven point seven is what you get if you forget the two.")

    def example_21(self):
        head, prob = C.example_head(self, "Find the pH of (a) 0.005 M Ca(OH)₂, (b) 100 cm³ of 0.10 M HCl mixed with 100 cm³ of 0.05 M NaOH.")
        st = C.steps(r"(a)\ [\mathrm{OH^-}] = 2 \times 0.005 = 0.01,\ \ pOH = 2,\ \ pH = 12",
                     r"(b)\ \mathrm{H^+}: 0.10 \times 100 = 10.0\ \mathrm{mmol};\ \ \mathrm{OH^-}: 0.05 \times 100 = 5.0\ \mathrm{mmol}",
                     r"\text{excess } \mathrm{H^+} = 5.0\ \mathrm{mmol\ in\ } 200\ \mathrm{cm^3} \Rightarrow [\mathrm{H^+}] = 0.025",
                     r"pH = -\log(2.5\times10^{-2}) = 2 - 0.398 = 1.60", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example two point one. Calcium hydroxide is a strong base giving two hydroxide ions. So hydroxide is zero point zero one, p O H is two, and p H is twelve."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Part b is a mixture. Count millimoles. Ten millimoles of acid, five of base. Five millimoles of acid are left over, now spread through two hundred cubic centimetres: zero point zero two five molar. p H is two minus log two point five, one point six zero."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def example_22(self):
        head, prob = C.example_head(self, "Find the pH, the degree of ionisation and [CH₃COO⁻] in 0.10 M acetic acid (Ka = 1.8 × 10⁻⁵).")
        st = C.steps(r"[\mathrm{H^+}] = \sqrt{K_aC} = \sqrt{1.8\times10^{-6}} = 1.34\times10^{-3}",
                     r"pH = 3 - \log 1.34 = 3 - 0.127 = 2.87",
                     r"\alpha = \sqrt{K_a/C} = 1.34\times10^{-2} = 1.34\,\%",
                     r"[\mathrm{CH_3COO^-}] = [\mathrm{H^+}] = 1.34\times10^{-3}\ \mathrm{mol\,L^{-1}}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[1].set_color(th.AMBER)
        with self.say("Worked example two point two, decimolar acetic acid. Hydrogen ion is the square root of K a C, the square root of one point eight times ten to the minus six, which is one point three four times ten to the minus three. So p H is two point eight seven."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("The degree of ionisation is root K a over C: one point three four percent. Small, so our approximation was fair. And acetate equals hydrogen ion, since each ionised molecule gives one of each."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def example_23(self):
        head, prob = C.example_head(self, "Find α, [OH⁻] and the pH of 0.020 M NH₄OH (Kb = 1.8 × 10⁻⁵).")
        st = C.steps(r"\alpha = \sqrt{\frac{1.8\times10^{-5}}{0.020}} = \sqrt{9.0\times10^{-4}} = 0.030 = 3.0\,\%",
                     r"[\mathrm{OH^-}] = C\alpha = 0.020 \times 0.030 = 6.0\times10^{-4}",
                     r"pOH = 4 - \log 6 = 4 - 0.778 = 3.22",
                     r"pH = 14 - 3.22 = 10.78", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        nb = C.show_neby(self, "think", height=1.3)
        with self.say("Worked example two point three, a weak base. Zero point zero two molar ammonium hydroxide. Alpha is the square root of K b over C, which is the square root of nine times ten to the minus four: zero point zero three, three percent."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Hydroxide is C alpha, six times ten to the minus four. p O H is four minus log six, three point two two. And p H is fourteen minus that, ten point seven eight."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            self.play(Write(st[3]))
            nb.set_state("success", once=True)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 9
    def p9(self):
        self.section(8)
        bk = C.Beaker(center=[-3.4, -0.7, 0], w=3.4, h=3.4, level=0.75, color=C.WATER, opacity=0.18)
        lat = VGroup()
        for i in range(6):
            for j in range(2):
                s = "Ag" if (i + j) % 2 == 0 else "Cl"
                lat.add(C.atom(s, r=0.17 if s == "Ag" else 0.2).move_to(bk.c + np.array([-0.95 + 0.38 * i, -1.45 + 0.38 * j, 0])))
        rng = np.random.default_rng(8)
        free = VGroup()
        for k in range(6):
            s = "Ag" if k % 2 == 0 else "Cl"
            free.add(C.atom(s, r=0.17 if s == "Ag" else 0.2).move_to(bk.c + np.array([rng.uniform(-1.3, 1.3), rng.uniform(-0.6, 0.9), 0])))
        eq = chem(r"AgCl(s) \rightleftharpoons Ag^+(aq) + Cl^-(aq)", size=40).move_to([2.8, 2.2, 0])
        with self.say("Drop some silver chloride into water. A tiny amount dissolves. Ions leave the crystal and wander into the solution, and at the same time, ions crash back onto the crystal and stick."):
            self.play(FadeIn(bk.g), FadeIn(lat))
            self.play(FadeIn(free))
            self.play(Write(eq))
            for _ in range(2):
                i = int(rng.integers(0, 12))
                j = int(rng.integers(0, 6))
                a, b = lat[i].get_center(), free[j].get_center()
                self.play(lat[i].animate.move_to(b), free[j].animate.move_to(a), run_time=1.2)
        sat = T("saturated: dissolving rate = precipitating rate", size=24, color=th.AMBER).next_to(eq, DOWN, buff=0.3)
        ksp = M(r"K_{sp} = [\mathrm{Ag^+}][\mathrm{Cl^-}]", size=50, color=th.AMBER).next_to(sat, DOWN, buff=0.5)
        why = T("[solid] is constant, so it joins the constant", size=22, color=th.MUTED).next_to(ksp, DOWN, buff=0.25)
        with self.say("When the two rates are equal, the solution is saturated, and we have a dynamic equilibrium. The concentration of a pure solid is constant, so it is folded into the constant. What remains is the solubility product, K s p, equal to silver ion times chloride ion."):
            self.play(FadeIn(sat))
            self.play(Write(ksp), FadeIn(why))
        defs = VGroup(T("Solubility S: moles dissolved per litre of saturated solution", size=24, color=th.BODY),
                      T("Ksp: product of ion concentrations at saturation, each to the power of its coefficient", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.say("So, solubility is the number of moles that dissolve per litre to give a saturated solution. And K s p is the product of the ion concentrations in that saturated solution, each raised to the power of its coefficient."):
            self.play(FadeIn(defs))
        self.play(FadeOut(VGroup(bk.g, lat, free, eq, sat, ksp, why, defs)))
        gen = VGroup(chem(r"A_xB_y(s) \rightleftharpoons xA^{y+} + yB^{x-}", size=42),
                     M(r"[\mathrm{A}] = xS,\quad [\mathrm{B}] = yS", size=42),
                     M(r"K_{sp} = (xS)^{x}(yS)^{y} = x^{x}y^{y}S^{\,x+y}", size=50, color=th.AMBER)).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.8)
        with self.say("For any salt A x B y with solubility S, the ions are x S and y S. So K s p is x S to the x, times y S to the y."):
            for g in gen:
                self.play(Write(g))
        rows = [["Type", "Example", "Ksp", "S"], ["AB", "AgCl, BaSO₄", "S²", M(r"\sqrt{K_{sp}}", size=30, color=th.MINT)], ["AB₂ / A₂B", "PbI₂, Ag₂CrO₄", "4S³", M(r"\sqrt[3]{K_{sp}/4}", size=30, color=th.MINT)],
                ["AB₃", "Fe(OH)₃", "27S⁴", M(r"\sqrt[4]{K_{sp}/27}", size=30, color=th.MINT)], ["A₃B₂", "Ca₃(PO₄)₂", "108S⁵", M(r"\sqrt[5]{K_{sp}/108}", size=30, color=th.MINT)]]
        tb = C.table(rows, [2.4, 3.2, 2.0, 3.0], row_h=0.66, size=25, colors=[th.MUTED, th.INK, th.AMBER, th.MINT]).next_to(gen, DOWN, buff=0.45)
        with self.say("That gives a handy table. A B: S squared. A B two or A two B: four S cubed. A B three: twenty seven S to the fourth. A three B two: one hundred and eight S to the fifth. K s p depends only on temperature, but solubility depends on what else is dissolved.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(gen, tb)))
        head, prob = C.example_head(self, "(a) Solubility of AgCl is 1.93 × 10⁻³ g L⁻¹ (M = 143.5). Find Ksp. (b) Solubility of Ag₂CrO₄ is 6.5 × 10⁻⁵ mol L⁻¹. Find Ksp.")
        st = C.steps(r"(a)\ S = \frac{1.93\times10^{-3}}{143.5} = 1.345\times10^{-5}\ \mathrm{mol\,L^{-1}}",
                     r"K_{sp} = S^{2} = (1.345\times10^{-5})^{2} = 1.81\times10^{-10}",
                     r"(b)\ \mathrm{Ag_2CrO_4} \rightleftharpoons 2\mathrm{Ag^+} + \mathrm{CrO_4^{2-}}:\ K_{sp} = (2S)^2 S = 4S^3",
                     r"= 4(6.5\times10^{-5})^{3} = 4 \times 2.746\times10^{-13} = 1.10\times10^{-12}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example two point four. First convert grams per litre to moles per litre: one point nine three times ten to the minus three over one forty three point five, one point three four five times ten to the minus five. Silver chloride is type A B, so K s p is S squared: one point eight one times ten to the minus ten."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Silver chromate gives two silver ions per formula, so silver is two S, and K s p is four S cubed. Four times six point five times ten to the minus five, cubed: one point one zero times ten to the minus twelve."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 10
    def p10(self):
        self.section(9)
        d = self.callout("key", "Common ion effect: a strong electrolyte that supplies an ion common to a weak equilibrium suppresses that ionisation, or that solubility. It is Le Chatelier's principle for ions.", width=11.5, size=27).to_edge(UP, buff=0.8)
        with self.say("The common ion effect. If you add a strong electrolyte that supplies an ion already present in a weak equilibrium, that equilibrium is pushed back. It is simply Le Chatelier's principle, applied to ions."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        eq = M(r"\mathrm{CH_3COOH}", r"\rightleftharpoons", r"\mathrm{CH_3COO^-}", r"+", r"\mathrm{H^+}", size=48).move_to(DOWN * 0.6)
        add = T("+ CH₃COONa  (lots of CH₃COO⁻)", size=28, color=th.AMBER).next_to(eq[2], DOWN, buff=0.6)
        back = Arrow(eq[1].get_center() + RIGHT * 0.5 + UP * 0.65, eq[1].get_center() + LEFT * 0.9 + UP * 0.65, buff=0, color=th.CORAL, stroke_width=6)
        res = T("equilibrium shifts left: [H⁺] falls, pH rises", size=28, color=th.CORAL).to_edge(DOWN, buff=1.0)
        with self.say("Acetic acid ionises a little into acetate and hydrogen ions. Now add sodium acetate, a salt that floods the solution with acetate. The equilibrium shifts left. Hydrogen ion concentration falls, and the p H rises, even though we added more acetic material."):
            self.play(Write(eq))
            self.play(FadeIn(add, shift=UP * 0.2), eq[2].animate.scale(1.12).set_color(th.AMBER))
            self.play(GrowArrow(back), eq[4].animate.scale(0.7).set_opacity(0.5))
            self.play(FadeIn(res))
        self.play(FadeOut(VGroup(d, eq, add, back, res)))
        rows = [["System", "Common ion", "Effect"],
                ["CH₃COOH + CH₃COONa", "CH₃COO⁻", "acid ionisation suppressed, pH rises"],
                ["NH₄OH + NH₄Cl", "NH₄⁺", "base ionisation suppressed, [OH⁻] falls"],
                ["H₂S + HCl", "H⁺", "[S²⁻] falls sharply (Group II)"],
                ["AgCl + NaCl", "Cl⁻", "solubility of AgCl falls"],
                ["sat. NaCl + HCl gas", "Cl⁻", "pure NaCl crystallises"]]
        tb = C.table(rows, [4.2, 2.4, 5.6], row_h=0.66, size=24, colors=[th.INK, th.AMBER, th.BODY]).move_to(UP * 0.4)
        with self.say("The same idea appears all over the syllabus. Ammonium chloride suppresses ammonium hydroxide. Hydrochloric acid suppresses hydrogen sulphide. Sodium chloride lowers the solubility of silver chloride. And hydrogen chloride gas makes pure salt crystallise from brine.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))
        head, prob = C.example_head(self, "Ksp(AgCl) = 1.8 × 10⁻¹⁰. Find its solubility (a) in pure water, (b) in 0.010 M NaCl.")
        st = C.steps(r"(a)\ S = \sqrt{1.8\times10^{-10}} = 1.34\times10^{-5}\ \mathrm{mol\,L^{-1}}",
                     r"(b)\ [\mathrm{Cl^-}] = 0.010 + S' \approx 0.010",
                     r"S' = \frac{1.8\times10^{-10}}{0.010} = 1.8\times10^{-8}\ \mathrm{mol\,L^{-1}}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example two point five. In pure water, the solubility of silver chloride is the square root of K s p, one point three four times ten to the minus five moles per litre."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("In zero point zero one molar sodium chloride, the chloride comes almost entirely from the salt. So K s p equals S dash times zero point zero one, and S dash is one point eight times ten to the minus eight."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        b1 = Rectangle(width=4.5, height=0.5, fill_color=th.SKY, fill_opacity=0.85, stroke_width=0)
        b2 = Rectangle(width=4.5 / 745, height=0.5, fill_color=th.CORAL, fill_opacity=1, stroke_width=0)
        bg = VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(DOWN, buff=0.7).to_edge(LEFT, buff=1.2)
        l1 = T("pure water", size=22, color=th.SKY).next_to(b1, RIGHT, buff=0.2)
        l2 = T("in 0.010 M NaCl: 745 times less", size=22, color=th.CORAL).next_to(b2, RIGHT, buff=0.2)
        nb = C.show_neby(self, "surprised", height=1.3)
        with self.say("The solubility has dropped about seven hundred and forty five times. That is why a precipitate is always washed with a dilute solution containing a common ion, never with pure water, which would dissolve it away."):
            self.play(GrowFromEdge(b1, LEFT), FadeIn(l1))
            self.play(GrowFromEdge(b2, LEFT), FadeIn(l2))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st, b1, b2, l1, l2)))

    # ------------------------------------------------------------------ part 11
    def p11(self):
        self.section(10)
        q = ValueTracker(-12)
        nl = NumberLine(x_range=[-13, -5, 1], length=10, include_numbers=False, color=th.MUTED).move_to([0, -0.4, 0])
        nums = VGroup(*[M(r"10^{" + str(k) + "}", size=34, color=th.MUTED).next_to(nl.n2p(k), DOWN, buff=0.2) for k in range(-13, -4)])
        kx = np.log10(1.1e-10)
        kline = DashedLine(nl.n2p(kx) + DOWN * 0.4, nl.n2p(kx) + UP * 2.2, color=th.AMBER, stroke_width=4)
        kl = M(r"K_{sp}", size=36, color=th.AMBER).next_to(kline, UP, buff=0.1)
        zl = T("unsaturated: no precipitate", size=24, color=th.SKY).move_to(nl.n2p(-11.8) + UP * 1.3)
        zr = T("supersaturated: precipitate forms", size=24, color=th.CORAL).move_to(nl.n2p(-7.0) + UP * 1.3)
        ptr = always_redraw(lambda: VGroup(Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI).move_to(nl.n2p(q.get_value()) + UP * 0.35),
                                           M("Q", size=32, color=WHITE).move_to(nl.n2p(q.get_value()) + UP * 0.75)))
        title = T("Ionic product Q versus Ksp", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        with self.say("To predict precipitation, compute the ionic product, Q. It is calculated exactly like K s p, but with the concentrations you actually have, saturated or not. Then compare it with K s p."):
            self.play(FadeIn(title), Create(nl), FadeIn(nums), Create(kline), FadeIn(kl))
            self.add(ptr)
            self.play(FadeIn(ptr))
        with self.say("If Q is less than K s p, the solution is unsaturated, and more solid would dissolve. If Q equals K s p, it is exactly saturated. If Q is greater, it is supersaturated, and the salt precipitates until Q falls back down to K s p."):
            self.play(FadeIn(zl))
            self.play(q.animate.set_value(kx), run_time=1.5)
            self.play(Flash(nl.n2p(kx) + UP * 0.35, color=th.AMBER))
            self.play(q.animate.set_value(-6), FadeIn(zr), run_time=1.5)
            self.play(q.animate.set_value(kx), run_time=1.5, rate_func=rate_functions.ease_out_cubic)
        self.play(FadeOut(VGroup(title, nl, nums, kline, kl, zl, zr)), FadeOut(ptr))
        self.remove(ptr)
        head, prob = C.example_head(self, "Equal volumes of 0.0020 M BaCl₂ and 0.0020 M Na₂SO₄ are mixed. Will BaSO₄ precipitate? Ksp = 1.1 × 10⁻¹⁰.")
        st = C.steps(r"\text{after mixing: } [\mathrm{Ba^{2+}}] = [\mathrm{SO_4^{2-}}] = \frac{0.0020}{2} = 1.0\times10^{-3}",
                     r"Q = (1.0\times10^{-3})^{2} = 1.0\times10^{-6}",
                     r"Q = 1.0\times10^{-6} \gg K_{sp} = 1.1\times10^{-10} \;\Rightarrow\; \text{precipitate}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.CORAL)
        with self.say("Worked example two point six. Equal volumes of two millimolar barium chloride and sodium sulphate are mixed. The trap: mixing equal volumes halves each concentration. So each ion is one times ten to the minus three molar."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Q is the square of that, ten to the minus six. That is ten thousand times bigger than K s p. So yes, barium sulphate precipitates."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
            self.sfx("impact", gain=-12)
        self.play(FadeOut(VGroup(head, prob, st)))
        title = T("Precipitation in practice", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cards = VGroup(
            C.card(self, "Group II", "H₂S in dilute HCl. H⁺ pushes H₂S ⇌ 2H⁺ + S²⁻ left, so [S²⁻] stays tiny: only CuS, PbS, CdS (very low Ksp) precipitate.", w=4.1, h=3.3, color=th.AMBER, bsize=21),
            C.card(self, "Group III A", "NH₄OH with NH₄Cl. NH₄⁺ suppresses NH₄OH, keeping [OH⁻] low: Fe(OH)₃, Al(OH)₃, Cr(OH)₃ come down; Mg(OH)₂ stays.", w=4.1, h=3.3, color=th.SKY, bsize=21),
            C.card(self, "Salt and soap", "HCl gas into brine: pure NaCl crystallises. NaCl added to soap solution: the soap 'salts out' as a curd.", w=4.1, h=3.3, color=th.MINT, bsize=21),
        ).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.5)
        with self.say("Qualitative analysis is built on this. In Group two, hydrogen sulphide is passed in dilute hydrochloric acid. The common hydrogen ion keeps sulphide ion very low, so only the least soluble sulphides, copper, lead and cadmium, exceed their K s p. Zinc sulphide does not."):
            self.play(FadeIn(title))
            self.play(FadeIn(cards[0], shift=UP * 0.3))
        with self.say("In Group three A, ammonium chloride keeps hydroxide low, so iron, aluminium and chromium hydroxides precipitate while magnesium hydroxide stays dissolved. And adding hydrogen chloride gas to brine, or common salt to soap, throws out pure sodium chloride or soap by the same principle."):
            self.play(FadeIn(cards[1], shift=UP * 0.3))
            self.play(FadeIn(cards[2], shift=UP * 0.3))
        self.play(FadeOut(VGroup(title, cards)))

    # ------------------------------------------------------------------ part 12
    def p12(self):
        self.section(11)
        d = self.callout("key", "A buffer resists a change in pH when a small amount of strong acid or base is added, or when it is diluted.", width=11.5, size=28).to_edge(UP, buff=0.8)
        rows = [["Type", "Made from", "Example", "pH"],
                ["acidic buffer", "weak acid + its salt with a strong base", "CH₃COOH + CH₃COONa", "< 7"],
                ["basic buffer", "weak base + its salt with a strong acid", "NH₄OH + NH₄Cl", "> 7"],
                ["salt buffer", "salt of a weak acid and a weak base", "CH₃COONH₄", "≈ 7"]]
        tb = C.table(rows, [2.4, 5.0, 3.6, 1.2], row_h=0.66, size=23, colors=[th.AMBER, th.BODY, th.INK, th.MINT]).next_to(d, DOWN, buff=0.5)
        with self.say("Now the answer to our cold open. A buffer solution resists a change in p H when a little strong acid or base is added, or when it is diluted. The commonest kinds are a weak acid with its salt, like acetic acid and sodium acetate, or a weak base with its salt, like ammonium hydroxide and ammonium chloride.") as v:
            self.play(FadeIn(d, shift=DOWN * 0.2))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(VGroup(d, tb)))
        self.buffer_mechanism()
        self.henderson()
        self.example_27()
        self.buffer_uses()

    def buffer_mechanism(self):
        title = T("How a buffer works", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        bk = C.Beaker(center=[0, -0.9, 0], w=5.4, h=3.6, level=0.85, color=C.WATER, opacity=0.15)
        rng = np.random.default_rng(12)
        pts = bk.inside(rng, 24, level=0.85)
        acid = VGroup(*[VGroup(Circle(radius=0.2, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0), T("HA", size=14, color=WHITE, weight="BOLD")).move_to(p) for p in pts[:12]])
        base = VGroup(*[VGroup(Circle(radius=0.2, fill_color=th.SKY, fill_opacity=0.9, stroke_width=0), T("A⁻", size=14, color=WHITE, weight="BOLD")).move_to(p) for p in pts[12:]])
        la = T("reserve of acid, CH₃COOH", size=24, color=th.CORAL).move_to([-4.6, 1.4, 0])
        lb = T("reserve of base, CH₃COO⁻", size=24, color=th.SKY).move_to([4.6, 1.4, 0])
        with self.say("Look inside the acetate buffer. It holds two big reserves: plenty of un-ionised acetic acid, and plenty of acetate ions from the salt."):
            self.play(FadeIn(title), FadeIn(bk.g))
            self.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in acid], lag_ratio=0.05), FadeIn(la))
            self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in base], lag_ratio=0.05), FadeIn(lb))
        hs = VGroup(*[C.proton(0.14).move_to([-1.0 + 0.5 * k, 2.6, 0]) for k in range(4)])
        e1 = chem(r"CH_3COO^- + H^+ \rightarrow CH_3COOH", size=32, color=th.CORAL).to_edge(DOWN, buff=0.45)
        with self.say("Add some hydrogen ions. Acetate ions grab them and become acetic acid, a weak acid that barely ionises. The strong acid has been swapped for a weak one."):
            self.play(FadeIn(hs, shift=DOWN * 0.3))
            anims = []
            for h, b in zip(hs, base[:4]):
                anims.append(h.animate.move_to(b.get_center()).scale(0.3).set_opacity(0))
            self.play(*anims, run_time=1.0)
            self.play(*[Transform(b, VGroup(Circle(radius=0.2, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0), T("HA", size=14, color=WHITE, weight="BOLD")).move_to(b.get_center())) for b in base[:4]])
            self.play(Write(e1))
        ohs = VGroup(*[VGroup(Circle(radius=0.15, fill_color=th.MINT, fill_opacity=1, stroke_width=0), T("OH⁻", size=11, color=th.BG, weight="BOLD")).move_to([-1.0 + 0.5 * k, 2.6, 0]) for k in range(4)])
        e2 = chem(r"CH_3COOH + OH^- \rightarrow CH_3COO^- + H_2O", size=32, color=th.SKY).to_edge(DOWN, buff=0.45)
        with self.say("Add hydroxide instead. The acid reserve neutralises it, giving acetate and water. Either way, only the ratio of salt to acid changes a little, and the p H depends on the logarithm of that ratio. So the p H hardly moves."):
            self.play(FadeOut(e1), FadeIn(ohs, shift=DOWN * 0.3))
            self.play(*[o.animate.move_to(a.get_center()).scale(0.3).set_opacity(0) for o, a in zip(ohs, acid[:4])], run_time=1.0)
            self.play(*[Transform(a, VGroup(Circle(radius=0.2, fill_color=th.SKY, fill_opacity=0.9, stroke_width=0), T("A⁻", size=14, color=WHITE, weight="BOLD")).move_to(a.get_center())) for a in acid[:4]])
            self.play(Write(e2))
        self.play(FadeOut(VGroup(title, bk.g, acid, base, la, lb, e2, hs, ohs)))

    def henderson(self):
        title = T("Henderson–Hasselbalch equation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        st = VGroup(
            M(r"K_a = \frac{[\mathrm{H^+}][\mathrm{A^-}]}{[\mathrm{HA}]}", size=44),
            M(r"[\mathrm{HA}] \approx [\text{acid}],\quad [\mathrm{A^-}] \approx [\text{salt}]", size=40),
            M(r"[\mathrm{H^+}] = K_a\,\frac{[\text{acid}]}{[\text{salt}]}", size=44),
            M(r"pH = pK_a + \log\frac{[\text{salt}]}{[\text{acid}]}", size=54, color=th.AMBER),
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.3)
        with self.say("Now the formula. Start from K a. The common ion from the salt pushes the acid's ionisation so far back that the acid concentration is just the acid we put in, and the anion concentration is just the salt we put in."):
            self.play(FadeIn(title), Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Rearrange for hydrogen ion, take minus logs, and out comes the Henderson Hasselbalch equation. p H equals p K a plus log of salt over acid."):
            self.play(Write(st[2]))
            self.sfx("impact", gain=-12)
            self.play(Write(st[3]))
            self.play(Circumscribe(st[3], color=th.AMBER))
        bas = M(r"\text{basic buffer: } pOH = pK_b + \log\frac{[\text{salt}]}{[\text{base}]}", size=34, color=th.SKY).to_edge(DOWN, buff=0.35)
        with self.say("For a basic buffer, the same argument gives p O H equals p K b plus log salt over base."):
            self.play(Write(bas))
        self.play(FadeOut(VGroup(title, st[:3], bas)), st[3].animate.scale(0.7).to_corner(UR, buff=0.7))
        r = ValueTracker(0)
        ax = Axes(x_range=[-2, 2, 1], y_range=[2, 7, 1], x_length=7, y_length=4.2, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([-0.8, -0.6, 0])
        xl = T("log ([salt] / [acid])", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.4)
        yl = T("pH", size=22, color=th.MUTED).next_to(ax, LEFT, buff=0.2)
        line = ax.plot(lambda x: 4.74 + x, x_range=[-2, 2], color=th.AMBER, stroke_width=4)
        band = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(-1, 0)[0], height=4.2, fill_color=th.MINT, fill_opacity=0.12, stroke_width=0).move_to(ax.c2p(0, 4.75))
        bl = T("useful range: pKa ± 1", size=22, color=th.MINT).next_to(band, UP, buff=0.05)
        dot = always_redraw(lambda: Dot(ax.c2p(r.get_value(), 4.74 + r.get_value()), radius=0.09, color=WHITE))
        with self.say("Plot it. The p H is p K a when salt equals acid, and moves by just one unit when the ratio changes tenfold. A buffer is most useful within one unit of its p K a, so pick the weak acid whose p K a is closest to the p H you need."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(line))
            self.add(dot)
            self.play(r.animate.set_value(1), run_time=1.2)
            self.play(r.animate.set_value(-1), run_time=1.6)
            self.play(r.animate.set_value(0), run_time=0.8)
            self.play(FadeIn(band), FadeIn(bl))
        self.play(FadeOut(VGroup(ax, xl, yl, line, band, bl, st[3])), FadeOut(dot))
        self.remove(dot)

    def example_27(self):
        head, prob = C.example_head(self, "(a) What mass of sodium acetate (M = 82) in 1.00 L of 0.10 M acetic acid gives pH 5.00? (b) Find the pH change when 0.010 mol HCl is added to 1.00 L of buffer 0.10 M in both acid and salt. (Ka = 1.8 × 10⁻⁵)", size=25)
        st = C.steps(r"pK_a = 5 - \log 1.8 = 4.74",
                     r"5.00 = 4.74 + \log\frac{[\text{salt}]}{0.10} \Rightarrow \frac{[\text{salt}]}{0.10} = 10^{0.26} = 1.80",
                     r"[\text{salt}] = 0.180\ \mathrm{M} \Rightarrow w = 0.180 \times 82 = 14.8\ \mathrm{g}", size=38).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example two point seven. Part a: we want p H five with decimolar acetic acid. p K a is four point seven four. So log of salt over zero point one is zero point two six, and the ratio is ten to the zero point two six, one point eight zero."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Salt is zero point one eight molar. In one litre, that is zero point one eight times eighty two, about fourteen point eight grams of sodium acetate."):
            self.play(Write(st[2]))
        self.play(FadeOut(st))
        st2 = C.steps(r"\text{before: } pH = pK_a + \log\tfrac{0.10}{0.10} = 4.74",
                      r"\text{after: [salt]} = 0.090,\ \ [\text{acid}] = 0.110",
                      r"pH = 4.74 + \log\frac{0.090}{0.110} = 4.74 - 0.087 = 4.65",
                      r"\text{pure water: } 7 \rightarrow -\log 0.010 = 2", size=38).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        st2[2].set_color(th.MINT)
        st2[3].set_color(th.CORAL)
        with self.say("Part b is our cold open. Before, salt equals acid, so p H equals p K a, four point seven four. The zero point zero one mole of hydrochloric acid turns zero point zero one mole of acetate into acetic acid. Salt becomes zero point zero nine, acid zero point one one."):
            self.play(Write(st2[0]))
            self.play(Write(st2[1]))
        with self.say("So the new p H is four point seven four plus log of zero point zero nine over zero point one one, which is four point six five. A change of less than a tenth of a unit. The same acid in pure water took the p H from seven to two. Five whole units. Mystery solved."):
            nb = C.show_neby(self, "success", height=1.3, corner=DR)
            self.play(Write(st2[2]))
            self.play(Write(st2[3]))
            self.sfx("correct", gain=-10)
        C.hide_neby(self, nb)
        nb = C.show_neby(self, "celebrate", height=1.4)
        self.wait(1.0)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st2)))

    def buffer_uses(self):
        title = T("Buffers keep the world running", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cards = VGroup(
            C.card(self, "Blood", "H₂CO₃ / HCO₃⁻ (with phosphate and proteins) hold pH 7.4. A drift of 0.4 is fatal.", w=3.9, h=2.4, color=th.CORAL, bsize=21),
            C.card(self, "Cells", "H₂PO₄⁻ / HPO₄²⁻ buffers intracellular fluid near pH 7.2.", w=3.9, h=2.4, color=th.PINK, bsize=21),
            C.card(self, "Soil", "Acidic hill soils of Nepal are limed to raise and hold the pH near 6–7.", w=3.9, h=2.4, color=th.MINT, bsize=21),
            C.card(self, "Industry", "Electroplating, brewing, curd, dyeing, sugar refining and paper all need a fixed pH.", w=3.9, h=2.4, color=th.AMBER, bsize=21),
            C.card(self, "Medicine", "Eye drops and injections are buffered to the pH of body fluids.", w=3.9, h=2.4, color=th.SKY, bsize=21),
            C.card(self, "Analysis", "EDTA titrations run in NH₄Cl / NH₄OH buffer at pH 10.", w=3.9, h=2.4, color=th.LIME, bsize=21),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).next_to(title, DOWN, buff=0.4)
        with self.say("Buffers are everywhere. Blood is held at seven point four by carbonic acid and bicarbonate. Cell fluid uses phosphate. Acidic hill soils in Nepal are limed to hold their p H. Electroplating, brewing, curd making and dyeing all need a fixed p H. Eye drops and injections are buffered to match body fluids. And E D T A titrations run in an ammonia buffer at p H ten.") as v:
            self.play(FadeIn(title))
            for c in cards:
                self.sfx("pop", gain=-16)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)
                self.hold(v.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(title, cards)))

    # ------------------------------------------------------------------ part 13
    def p13(self):
        self.section(12)
        d = self.callout("key", "An acid-base indicator is a weak organic acid (or base) whose un-ionised and ionised forms have different colours.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("Now we can finally explain indicators. An acid base indicator is a weak organic acid or base, whose un-ionised form and ionised form have different colours."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        pH = ValueTracker(6.0)
        eq = M(r"\mathrm{HIn}", r"\rightleftharpoons", r"\mathrm{H^+}", r"+", r"\mathrm{In^-}", size=56).move_to(DOWN * 0.5)
        c1 = T("colourless", size=24, color=th.MUTED).next_to(eq[0], DOWN, buff=0.3)
        c2 = T("pink", size=24, color=C.PINK_END).next_to(eq[4], DOWN, buff=0.3)
        name = T("phenolphthalein", size=26, color=C.PINK_END).next_to(eq, UP, buff=0.4)
        fl = C.Flask(center=[4.6, -1.6, 0], scale=1.1, color="#DDE3F5", opacity=0.5)
        fl.liq.add_updater(lambda m: m.set_fill(C.phenolphthalein(pH.get_value())))
        pv = DecimalNumber(6.0, num_decimal_places=1, font_size=40, color=th.INK)
        pv.add_updater(lambda m: m.set_value(pH.get_value()).next_to(fl.g, UP, buff=0.3))
        pl = T("pH", size=24, color=th.MUTED)
        pl.add_updater(lambda m: m.next_to(pv, LEFT, buff=0.15))
        ost = M(r"pH = pK_{In} + \log\frac{[\mathrm{In^-}]}{[\mathrm{HIn}]}", size=40).move_to([-2.6, -2.5, 0])
        with self.say("Take phenolphthalein, H In. In acid, the high hydrogen ion concentration holds it in the colourless H In form. Add alkali, hydrogen ions are removed, the equilibrium shifts right, and pink In minus appears."):
            self.play(Write(eq), FadeIn(c1), FadeIn(c2), FadeIn(name))
            self.add(pv, pl)
            self.play(FadeIn(fl.g), FadeIn(pv), FadeIn(pl))
            self.play(pH.animate.set_value(11), eq[4].animate.scale(1.25), eq[0].animate.scale(0.8), run_time=3)
        with self.say("Treat it like a buffer, and Ostwald's theory gives p H equals p K of the indicator, plus log of In minus over H In. The eye sees one pure colour only when one form is about ten times the other. So the colour change happens over p K In plus or minus one."):
            self.play(Write(ost))
            self.play(pH.animate.set_value(8.0), run_time=2)
            self.play(pH.animate.set_value(10.2), run_time=2)
        fl.liq.clear_updaters()
        pv.clear_updaters()
        pl.clear_updaters()
        self.play(FadeOut(VGroup(d, eq, c1, c2, name, fl.g, pv, pl, ost)))
        inds = [("Methyl orange", 3.1, 4.4, C.MO_RED, C.MO_YEL), ("Methyl red", 4.2, 6.3, "#FF4B4B", "#FFE14A"), ("Litmus", 5.0, 8.0, "#E8433A", "#3A6FE0"),
                ("Bromothymol blue", 6.0, 7.6, "#F2D43C", "#3A6FE0"), ("Phenol red", 6.8, 8.4, "#F2D43C", "#E8433A"),
                ("Phenolphthalein", 8.3, 10.0, "#DDE3F5", "#FF4FB8"), ("Thymolphthalein", 9.3, 10.5, "#DDE3F5", "#3A6FE0")]
        nl = NumberLine(x_range=[0, 14, 1], length=9.0, include_numbers=True, font_size=22, color=th.MUTED).move_to([1.6, -2.8, 0])
        bars = VGroup()
        for i, (n, a, b, ca, cb) in enumerate(inds):
            y = 2.4 - i * 0.68
            x0, x1 = nl.n2p(a)[0], nl.n2p(b)[0]
            left = Rectangle(width=x0 - nl.n2p(0)[0], height=0.36, fill_color=ca, fill_opacity=0.55, stroke_width=0).move_to([(nl.n2p(0)[0] + x0) / 2, y, 0])
            mid = Rectangle(width=x1 - x0, height=0.36, stroke_width=0).set_fill(color=[ca, cb], opacity=0.95).move_to([(x0 + x1) / 2, y, 0])
            mid.set_sheen_direction(RIGHT)
            right = Rectangle(width=nl.n2p(14)[0] - x1, height=0.36, fill_color=cb, fill_opacity=0.55, stroke_width=0).move_to([(nl.n2p(14)[0] + x1) / 2, y, 0])
            lab = T(n, size=22, color=th.INK).next_to([nl.n2p(0)[0], y, 0], LEFT, buff=0.2)
            rng_l = T(f"{a:g} – {b:g}", size=18, color=th.INK, weight="BOLD").move_to(mid)
            bars.add(VGroup(left, mid, right, lab, rng_l))
        with self.say("Every indicator has its own range. Methyl orange changes between three point one and four point four, red to yellow. Methyl red, litmus, bromothymol blue and phenol red sit in the middle. Phenolphthalein changes between eight point three and ten, colourless to pink.") as v:
            self.play(Create(nl))
            for b in bars:
                self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur / 7 - 0.45)
        self.play(FadeOut(VGroup(nl, bars)))
        ax = Axes(x_range=[0, 50, 10], y_range=[0, 14, 2], x_length=6.4, y_length=4.4, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 20}).move_to([-2.4, -0.2, 0])
        xl = T("NaOH added (cm³)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35)
        weak = ax.plot(lambda v: C.ph_weak_acid(v), x_range=[0, 50, 0.1], color=th.AMBER, stroke_width=4, use_smoothing=False)
        b1 = Rectangle(width=6.4, height=ax.c2p(0, 4.4)[1] - ax.c2p(0, 3.1)[1], fill_color=C.MO_RED, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p(25, 3.75))
        b2 = Rectangle(width=6.4, height=ax.c2p(0, 10)[1] - ax.c2p(0, 8.3)[1], fill_color=C.PINK_END, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p(25, 9.15))
        t1 = T("methyl orange: changes too early", size=22, color=C.MO_RED).next_to(ax, RIGHT, buff=0.1).set_y(ax.c2p(0, 3.75)[1])
        t2 = T("phenolphthalein: inside the jump", size=22, color=C.PINK_END).next_to(ax, RIGHT, buff=0.1).set_y(ax.c2p(0, 9.15)[1])
        title = T("Weak acid vs strong base", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rule = T("Rule: the indicator's range must lie inside the steep jump.", size=26, color=th.AMBER).to_edge(DOWN, buff=0.3)
        with self.say("So how do we choose? Here is acetic acid titrated with sodium hydroxide. The vertical jump runs from about seven to about eleven. Methyl orange's range is far below it, so it would change colour too early, long before the equivalence point. Phenolphthalein's range sits right inside the jump."):
            self.play(FadeIn(title), Create(ax), FadeIn(xl))
            self.play(Create(weak), run_time=2)
            self.play(FadeIn(b1), FadeIn(t1))
            self.play(FadeIn(b2), FadeIn(t2))
        with self.say("That is the whole rule. Choose an indicator whose working range lies within the steep part of the titration curve, where one drop changes the p H by several units."):
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, ax, xl, weak, b1, b2, t1, t2, rule)))
        rows = [["Titration", "pH at equivalence", "Why", "Indicator"],
                ["strong acid vs strong base", "7", "no hydrolysis", "either"],
                ["weak acid vs strong base", "> 7 (≈ 8.7)", "anion hydrolysed", "phenolphthalein"],
                ["strong acid vs weak base", "< 7 (≈ 5.3)", "cation hydrolysed", "methyl orange"],
                ["weak acid vs weak base", "≈ 7", "both hydrolysed", "none: use a pH meter"]]
        tb = C.table(rows, [4.0, 2.6, 2.8, 3.2], row_h=0.66, size=23, colors=[th.INK, th.AMBER, th.BODY, th.MINT]).move_to(UP * 0.3)
        with self.say("Now the table from Unit 1 makes sense. The equivalence point is not always at seven, because the salt formed may hydrolyse. With a weak acid it is around eight point seven, so phenolphthalein. With a weak base, around five point three, so methyl orange.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(tb))
        self.tip("Weak acid + strong base → phenolphthalein. Strong acid + weak base → methyl orange. Weak + weak → no indicator works.",
                 "A memory hook for the exam. The indicator follows the strong partner. Strong base, phenolphthalein, which changes in the alkaline region. Strong acid, methyl orange, which changes in the acid region. Both weak, no sharp jump at all, so no indicator works.", state="wink")

    # ------------------------------------------------------------------ part 14
    def p14(self):
        self.section(13)
        title = T("Salts by composition", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Class", "Formed by", "Examples"],
                ["normal", "all replaceable H⁺ replaced", "NaCl, Na₂SO₄, K₃PO₄"],
                ["acid salt", "some H⁺ still replaceable", "NaHSO₄, NaHCO₃, NaH₂PO₄"],
                ["basic salt", "some OH⁻ of the base left", "Pb(OH)Cl, Zn(OH)Cl, Mg(OH)Cl"],
                ["double salt", "two salts crystallised together", "Mohr's salt, potash alum"],
                ["mixed salt", "one acid + two bases, or vice versa", "CaOCl₂, NaKSO₄"],
                ["complex salt", "contains a lasting complex ion", "K₄[Fe(CN)₆], [Cu(NH₃)₄]SO₄"]]
        tb = C.table(rows, [2.6, 5.0, 4.8], row_h=0.62, size=23, colors=[th.AMBER, th.BODY, th.INK]).next_to(title, DOWN, buff=0.4)
        with self.say("A salt forms when an acid reacts with a base. By composition there are six kinds. Normal salts, with every replaceable hydrogen replaced. Acid salts, like sodium bicarbonate, with some still left. Basic salts, with some hydroxide left. Double salts like Mohr's salt and potash alum. Mixed salts like bleaching powder. And complex salts like potassium ferrocyanide.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(VGroup(title, tb)))
        self.double_vs_complex()
        rows = [["Salt of", "Solution", "Examples"],
                ["strong acid + strong base", "neutral, pH 7", "NaCl, KNO₃, Na₂SO₄"],
                ["weak acid + strong base", "basic, pH > 7", "CH₃COONa, Na₂CO₃, KCN"],
                ["strong acid + weak base", "acidic, pH < 7", "NH₄Cl, CuSO₄, FeCl₃"],
                ["weak acid + weak base", "depends on Ka vs Kb", "CH₃COONH₄ (≈ 7)"]]
        tb = C.table(rows, [4.4, 3.6, 4.4], row_h=0.66, size=24, colors=[th.INK, th.AMBER, th.BODY]).move_to(UP * 0.4)
        note = T("NaHCO₃ is an acid salt, yet its solution is alkaline.", size=26, color=th.CORAL).next_to(tb, DOWN, buff=0.5)
        with self.say("Salts are also classed by the p H of their solution. Strong acid with strong base, neutral. Weak acid with strong base, basic. Strong acid with weak base, acidic. And a careful point: an acid salt is not the same as an acidic salt. Sodium bicarbonate is an acid salt by composition, but its solution is alkaline.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(tb, note)))

    def double_vs_complex(self):
        left = C.Beaker(center=[-3.4, -1.0, 0], w=2.8, h=2.6, level=0.7, color=C.WATER, opacity=0.18)
        right = C.Beaker(center=[3.4, -1.0, 0], w=2.8, h=2.6, level=0.7, color=C.WATER, opacity=0.18)
        hl = T("Mohr's salt (double)", size=26, color=th.AMBER, weight="SEMIBOLD").next_to(left.g, UP, buff=1.4)
        hr = T("K₄[Fe(CN)₆] (complex)", size=26, color=th.SKY, weight="SEMIBOLD").next_to(right.g, UP, buff=1.4)
        xtal_l = Square(side_length=0.7, fill_color=th.MINT, fill_opacity=0.8, stroke_width=0).move_to(left.c + UP * 1.75)
        xtal_r = Square(side_length=0.7, fill_color=th.AMBER, fill_opacity=0.8, stroke_width=0).move_to(right.c + UP * 1.75)
        rng = np.random.default_rng(14)
        ions_l = VGroup()
        for k, (t, col) in enumerate([("Fe²⁺", C.EL["Fe"]), ("NH₄⁺", th.SKY), ("NH₄⁺", th.SKY), ("SO₄²⁻", C.EL["S"]), ("SO₄²⁻", C.EL["S"])]):
            ions_l.add(T(t, size=20, color=col, weight="BOLD").move_to(left.c + np.array([-0.9 + 0.45 * k, -0.6 + 0.35 * (k % 2), 0])))
        ions_r = VGroup(*[T("K⁺", size=20, color=C.EL["K"], weight="BOLD").move_to(right.c + np.array([-1.0 + 0.65 * k, 0.1 if k % 2 else -0.9, 0])) for k in range(4)],
                        T("[Fe(CN)₆]⁴⁻", size=22, color=th.AMBER, weight="BOLD").move_to(right.c + DOWN * 0.4))
        with self.say("The difference between a double salt and a complex salt is a favourite question. Dissolve Mohr's salt. It falls apart completely into ferrous, ammonium and sulphate ions. The solution gives the tests of all three."):
            self.play(FadeIn(left.g), FadeIn(right.g), FadeIn(hl), FadeIn(hr), FadeIn(xtal_l), FadeIn(xtal_r))
            self.play(xtal_l.animate.move_to(left.c + DOWN * 0.3).scale(0.2).set_opacity(0), LaggedStart(*[FadeIn(i, scale=0.3) for i in ions_l], lag_ratio=0.15), run_time=1.6)
        with self.say("Dissolve potassium ferrocyanide. Only the potassium ions leave. The ferrocyanide complex ion stays in one piece, so the solution gives no test for ferrous ion or cyanide. A double salt exists only as a solid. A complex salt keeps its complex ion in solution."):
            self.play(xtal_r.animate.move_to(right.c + DOWN * 0.3).scale(0.2).set_opacity(0), LaggedStart(*[FadeIn(i, scale=0.3) for i in ions_r], lag_ratio=0.15), run_time=1.6)
            self.play(Indicate(ions_r[-1], color=th.AMBER))
        self.play(FadeOut(VGroup(left.g, right.g, hl, hr, xtal_l, xtal_r, ions_l, ions_r)))

    # ------------------------------------------------------------------ part 15
    def p15(self):
        self.section(14)
        d = self.callout("key", "Hydrolysis: the reaction of a salt's cation or anion with water, giving back the parent acid or base. It is the reverse of neutralisation.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("Why should a salt make water acidic or basic at all? Because of hydrolysis: the reaction of a salt's cation or anion with water to give back the parent acid or base. It is neutralisation running in reverse."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        y = -0.5
        ac = chem(r"CH_3COO^-", size=42).move_to([-4.6, y, 0])
        w = C.water([-1.7, y, 0], r=0.38)
        arr = M(r"\rightleftharpoons", size=56).move_to([0.2, y, 0])
        hac = chem(r"CH_3COOH", size=42).move_to([2.6, y, 0])
        oh = VGroup(Circle(radius=0.36, fill_color=th.MINT, fill_opacity=1, stroke_width=0), T("OH⁻", size=22, color=th.BG, weight="BOLD")).move_to([5.0, y, 0])
        p1 = M("+", size=44).move_to([-2.95, y, 0])
        p2 = M("+", size=44).move_to([4.05, y, 0])
        res = T("leftover OH⁻: the solution is alkaline", size=28, color=th.MINT).to_edge(DOWN, buff=0.9)
        with self.say("Sodium acetate. The sodium ion is a spectator. But acetate is the conjugate base of a weak acid, so it pulls a proton off a water molecule, forming acetic acid and leaving a hydroxide ion behind. The solution turns alkaline. This is anionic hydrolysis."):
            self.play(FadeIn(ac), FadeIn(p1), FadeIn(w))
            hp = w[2][0]
            self.play(hp.animate.move_to(ac.get_right() + RIGHT * 0.1), run_time=1.0)
            self.play(FadeIn(arr), TransformFromCopy(VGroup(ac, hp), hac), FadeOut(hp))
            self.play(FadeIn(p2), TransformFromCopy(w, oh))
            self.play(FadeIn(res))
        self.play(FadeOut(VGroup(d, ac, p1, w, arr, hac, p2, oh, res)))
        cases = VGroup(
            C.card(self, "SA + SB: NaCl", "Neither ion reacts with water. No hydrolysis. pH 7.", w=5.9, h=1.6, color=th.MUTED, bsize=22),
            C.card(self, "WA + SB: CH₃COONa", "Anion hydrolysed. Kh = Kw/Ka. Alkaline.", w=5.9, h=1.6, color=th.SKY, bsize=22),
            C.card(self, "SA + WB: NH₄Cl", "NH₄⁺ + H₂O ⇌ NH₄OH + H⁺. Kh = Kw/Kb. Acidic.", w=5.9, h=1.6, color=th.CORAL, bsize=22),
            C.card(self, "WA + WB: CH₃COONH₄", "Both hydrolysed. Kh = Kw/(KaKb). Depends on Ka vs Kb.", w=5.9, h=1.6, color=th.AMBER, bsize=22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to(UP * 0.2)
        with self.say("There are four cases. A salt of a strong acid and strong base, like sodium chloride, does not hydrolyse at all. Weak acid and strong base, the anion hydrolyses, alkaline. Strong acid and weak base, like ammonium chloride, the cation gives up a proton, acidic. Weak acid and weak base, both ions hydrolyse, and the result depends on which constant is bigger.") as v:
            for c in cases:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur / 4 - 0.6)
        self.play(FadeOut(cases))
        title = T("Anionic hydrolysis: the formulas", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        der = VGroup(
            M(r"K_h = \frac{[\mathrm{CH_3COOH}][\mathrm{OH^-}]}{[\mathrm{CH_3COO^-}]} \approx Ch^{2}", size=40),
            M(r"\times\frac{[\mathrm{H^+}]}{[\mathrm{H^+}]}:\quad K_h = \frac{K_w}{K_a}", size=44, color=th.AMBER),
            M(r"h = \sqrt{\frac{K_h}{C}} = \sqrt{\frac{K_w}{K_aC}}", size=42),
            M(r"pH = 7 + \tfrac12 pK_a + \tfrac12\log C", size=50, color=th.MINT),
        ).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.4)
        with self.say("For sodium acetate at concentration C, with degree of hydrolysis h, the hydrolysis constant K h is C h squared. Multiply top and bottom by hydrogen ion, and you recognise K w over K a."):
            self.play(FadeIn(title), Write(der[0]))
            self.play(Write(der[1]))
        with self.say("So h is the square root of K w over K a C. Hydroxide is C h, and taking logs gives p H equals seven plus half p K a plus half log C."):
            self.play(Write(der[2]))
            self.play(Write(der[3]))
        others = VGroup(M(r"\text{SA+WB: } pH = 7 - \tfrac12 pK_b - \tfrac12\log C", size=44, color=th.CORAL),
                        M(r"\text{WA+WB: } pH = 7 + \tfrac12 pK_a - \tfrac12 pK_b", size=44, color=th.AMBER)).arrange(DOWN, buff=0.45).move_to(DOWN * 0.6)
        with self.say("The other cases follow the same way. For a weak acid and weak base salt, look: no C at all. The p H of ammonium acetate does not change on dilution. A favourite one mark point."):
            self.play(FadeOut(der[:3]), der[3].animate.next_to(title, DOWN, buff=0.5))
            self.play(FadeIn(others, shift=UP * 0.2))
            self.play(Indicate(others[1], color=th.AMBER))
        self.play(FadeOut(VGroup(title, der[3], others)))
        head, prob = C.example_head(self, "Find Kh, the degree of hydrolysis h and the pH of 0.10 M sodium acetate at 25 °C. Ka = 1.8 × 10⁻⁵, Kw = 1.0 × 10⁻¹⁴.")
        st = C.steps(r"K_h = \frac{1.0\times10^{-14}}{1.8\times10^{-5}} = 5.56\times10^{-10}",
                     r"h = \sqrt{\frac{5.56\times10^{-10}}{0.10}} = 7.45\times10^{-5}",
                     r"[\mathrm{OH^-}] = Ch = 7.45\times10^{-6},\ \ pOH = 5.13",
                     r"pH = 14 - 5.13 = 8.87 \quad \left(= 7 + 2.37 - 0.50\right)", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example two point eight. K h is K w over K a, five point five six times ten to the minus ten. The degree of hydrolysis is root K h over C, seven point four five times ten to the minus five. Only about seven thousandths of a percent of the acetate reacts."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Hydroxide is C h, seven point four five times ten to the minus six. p O H is five point one three, so p H is eight point eight seven. The formula agrees: seven plus two point three seven minus zero point five zero, eight point eight seven."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("An aqueous solution of NH₄Cl is",
                  ["neutral", "acidic", "basic", "amphoteric"], 1,
                  "Last one. A solution of ammonium chloride. Neutral, acidic, basic, or amphoteric? Pause and think.",
                  "B, acidic. Ammonium chloride is the salt of a strong acid and a weak base. The ammonium ion gives a proton to water, producing hydrogen ions. The chloride ion, conjugate base of a strong acid, does nothing.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Arrhenius: H⁺ / OH⁻ in water. Bronsted: proton donor / acceptor. Lewis: e⁻-pair acceptor / donor.",
            "Conjugate pairs differ by one proton; the stronger the acid, the weaker its conjugate base.",
            M(r"\alpha = \sqrt{K/C},\quad K_w = [\mathrm{H^+}][\mathrm{OH^-}] = 10^{-14},\quad K_aK_b = K_w", size=40),
            M(r"pH = -\log[\mathrm{H^+}],\quad \text{weak acid: } [\mathrm{H^+}] = \sqrt{K_aC}", size=40),
            M(r"K_{sp} = x^{x}y^{y}S^{x+y};\quad Q > K_{sp} \Rightarrow \text{precipitate}", size=40),
            "Common ion suppresses ionisation and solubility (Le Chatelier).",
            M(r"\text{Buffer: } pH = pK_a + \log\frac{[\text{salt}]}{[\text{acid}]}", size=40),
            "Indicator range pKIn ± 1 must lie inside the jump.",
            M(r"\text{Hydrolysis: } K_h = \frac{K_w}{K_a},\ \frac{K_w}{K_b},\ \frac{K_w}{K_aK_b}", size=40),
        ], "Let us recap. Three definitions of acids and bases, each wider than the last. Conjugate pairs differ by one proton, and a strong acid has a weak conjugate base. Alpha is root K over C. K w is ten to the minus fourteen, and K a times K b equals K w. p H is minus log hydrogen ion, and for a weak acid hydrogen ion is root K a C. K s p links to solubility, and when Q exceeds it, a precipitate forms. A common ion suppresses ionisation. A buffer follows Henderson's equation. An indicator must change inside the jump. And salts hydrolyse according to which partner is weak.")
        self.outro("That is ionic equilibrium, the longest unit, done. Next, we ask not where a reaction ends up, but how fast it gets there, in chemical kinetics. See you in the next lesson on NEBians.")
