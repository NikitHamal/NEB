import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402


def titrate(s, bur, flask, to, drops=6, run_time=0.4, color_fn=None):
    """Drops fall while the burette level moves to `to` cm³; color_fn(v) recolours the flask."""
    v0 = bur.vol.get_value()
    step = (to - v0) / drops
    for i in range(drops):
        v = v0 + step * (i + 1)
        d = Circle(radius=0.055, fill_color=bur.color, fill_opacity=0.95, stroke_width=0).move_to(bur.tip_point)
        s.add(d)
        anims = [d.animate.move_to(flask.surface), bur.vol.animate.set_value(v)]
        if color_fn is not None:
            anims.append(flask.liq.animate.set_fill(color_fn(v)))
        s.play(*anims, run_time=run_time, rate_func=linear)
        s.remove(d)


def vol_readout(bur, size=40, color=th.INK, places=2):
    d = DecimalNumber(0, num_decimal_places=places, font_size=size, color=color)
    d.add_updater(lambda m: m.set_value(bur.vol.get_value()))
    return d


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 1
    TITLE = "Volumetric Analysis"
    SUBTITLE = "How much is in there? Ask a burette."
    SECTIONS = ["Gravimetric, volumetric, equivalent", "Equivalent weight and valency", "Equivalent weight of compounds",
                "Concentration units", "Primary and secondary standards", "Law of equivalence", "Titration: acid-base and redox"]
    NEXT = "Unit 2 · Ionic Equilibrium"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        bur = C.Burette(x=-1.6, top=3.3, bottom=0.25, color=th.SKY)
        fl = C.Flask(center=[-1.6, -2.1, 0], scale=1.15, color=C.MO_YEL, opacity=0.75)
        lab_b = T("0.1 N hydrochloric acid", size=24, color=th.SKY).next_to(bur.glass, LEFT, buff=0.35).shift(UP * 1.0)
        lab_f = T("washing soda solution", size=24, color=C.MO_YEL).next_to(fl.g, LEFT, buff=0.3)
        lab_f2 = T("+ methyl orange", size=20, color=th.MUTED).next_to(lab_f, DOWN, buff=0.1)
        rd = vol_readout(bur, size=64)
        unit = M(r"\mathrm{cm^3}", size=44, color=th.MUTED)
        rdg = VGroup(rd, unit)
        cap = T("burette reading", size=24, color=th.MUTED)
        rd.move_to([2.6, 1.2, 0])
        unit.add_updater(lambda m: m.next_to(rd, RIGHT, buff=0.18, aligned_edge=DOWN))
        cap.next_to(rd, UP, buff=0.3)
        with self.say("Here is a flask of washing soda, sodium carbonate, dissolved in water, with two drops of methyl orange. The solution is yellow. Above it sits a burette, full of hydrochloric acid of known strength."):
            self.play(FadeIn(fl.g, shift=UP * 0.3), FadeIn(lab_f), FadeIn(lab_f2))
            self.add(bur.liquid)
            self.play(Create(bur.glass), FadeIn(bur.liquid), FadeIn(lab_b), run_time=1.4)
            self.add(rd, unit)
            self.play(FadeIn(cap), FadeIn(rdg))
        with self.say("We open the tap, and the acid runs in, drop by drop. The colour does not change. Not yet."):
            titrate(self, bur, fl, 20.0, drops=10, run_time=0.38)
        with self.say("Slower now. Twenty one. Twenty two. Watch the flask."):
            titrate(self, bur, fl, 22.4, drops=6, run_time=0.5)
        self.sfx("impact", gain=-8)
        titrate(self, bur, fl, 22.5, drops=1, run_time=0.5, color_fn=lambda v: C.MO_RED if v > 22.45 else C.MO_YEL)
        self.play(Flash(fl.liq.get_center(), color=C.MO_RED, flash_radius=1.1, line_length=0.4), run_time=0.6)
        nb = C.show_neby(self, "surprised", height=1.6, corner=DR)
        q = para("From this one reading, how many grams of washing soda were in the flask?", width=5.6, size=28, color=th.INK)
        q.next_to(rd, DOWN, buff=0.7).shift(RIGHT * 0.2)
        with self.say("One single drop, and the whole flask turns red. The burette reads twenty two point five cubic centimetres. Now here is the challenge. From that one number, can you say exactly how many grams of washing soda were dissolved?"):
            self.play(Indicate(rd, color=th.AMBER, scale_factor=1.15))
            self.play(FadeIn(q, shift=UP * 0.2))
        with self.say("A chemist can, in about three lines. By the end of this lesson, so will you."):
            nb.set_state("wink", once=True)
            self.wait(1.0)
        rd.clear_updaters()
        unit.clear_updaters()
        self.play(FadeOut(VGroup(bur.glass, lab_b, lab_f, lab_f2, fl.g, rd, unit, cap, q)), FadeOut(bur.liquid), FadeOut(nb))
        self.remove(bur.liquid, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 1: Volumetric Analysis. This is the chapter that turns a burette reading into grams, molarity and percentage purity. It also gives you the n factor, the one idea that makes every titration numerical a one line problem."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is our path. Gravimetric and volumetric analysis, and the idea of an equivalent. Equivalent weight and valency. Equivalent weights of acids, bases, salts and redox agents. Concentration units. Primary and secondary standards. The law of equivalence. And finally, titration itself, acid base and redox.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        q1 = T("What is present?", size=44, color=th.SKY, weight="BOLD", display=True).move_to([-3.3, 1.6, 0])
        q2 = T("How much is present?", size=44, color=th.AMBER, weight="BOLD", display=True).move_to([3.1, 1.6, 0])
        l1 = T("qualitative analysis", size=28, color=th.BODY).next_to(q1, DOWN, buff=0.3)
        l2 = T("quantitative analysis", size=28, color=th.BODY).next_to(q2, DOWN, buff=0.3)
        with self.say("Analytical chemistry asks two different questions. What is present? That is qualitative analysis. And how much is present? That is quantitative analysis, and it is what this whole unit is about."):
            self.play(FadeIn(q1, shift=DOWN * 0.2), FadeIn(l1))
            self.play(FadeIn(q2, shift=DOWN * 0.2), FadeIn(l2))
            self.play(Indicate(q2, color=th.AMBER, scale_factor=1.08))
        r1 = T("weigh a precipitate", size=30, color=th.INK).move_to([0.2, -0.6, 0])
        r2 = T("measure a volume", size=30, color=th.INK).move_to([0.2, -2.0, 0])
        a1 = Arrow(l2.get_bottom(), r1.get_top() + RIGHT * 1.5, color=th.MINT, buff=0.15)
        a2 = Arrow(l2.get_bottom(), r2.get_right() + RIGHT * 0.1, color=th.SKY, buff=0.15)
        n1 = T("gravimetric", size=26, color=th.MINT, weight="SEMIBOLD").next_to(r1, LEFT, buff=0.4)
        n2 = T("volumetric", size=26, color=th.SKY, weight="SEMIBOLD").next_to(r2, LEFT, buff=0.4)
        with self.say("Classical quantitative analysis then splits again, by what you actually measure on the bench. Weigh a precipitate, and it is gravimetric analysis. Measure the volume of a solution, and it is volumetric analysis."):
            self.play(GrowArrow(a1), FadeIn(r1), FadeIn(n1))
            self.play(GrowArrow(a2), FadeIn(r2), FadeIn(n2))
        self.play(FadeOut(VGroup(q1, q2, l1, l2, r1, r2, a1, a2, n1, n2)))
        self.gravimetric()
        self.volumetric_intro()
        self.compare_table()
        self.equivalent_idea()

    def gravimetric(self):
        title = T("Gravimetric analysis: weigh it", size=36, color=th.MINT, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        bk = C.Beaker(center=[-4.0, -0.9, 0], w=2.2, h=2.4, level=0.62, color=th.SKY, opacity=0.25)
        bl = T("sulphate solution", size=22, color=th.MUTED).next_to(bk.g, DOWN, buff=0.2)
        eq = chem(r"BaCl_2 + Na_2SO_4 \rightarrow BaSO_4\downarrow + 2NaCl", size=40).move_to([1.6, 2.1, 0])
        with self.say("Here is the gravimetric route. To find how much sulphate is in a solution, we add barium chloride. Barium sulphate is almost completely insoluble, so it comes out as a white precipitate."):
            self.play(FadeIn(title), FadeIn(bk.g), FadeIn(bl))
            self.play(Write(eq))
            rng = np.random.default_rng(3)
            pts = bk.inside(rng, 60, level=0.62)
            ppt = VGroup(*[Dot(p, radius=0.045, color=WHITE) for p in pts])
            self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in ppt], lag_ratio=0.02), run_time=1.6)
            settled = [bk.c + np.array([rng.uniform(-0.95, 0.95), -1.1 + rng.uniform(0, 0.18), 0]) for _ in ppt]
            self.play(*[d.animate.move_to(p) for d, p in zip(ppt, settled)], run_time=1.6, rate_func=rate_functions.ease_in_quad)
        stepsg = VGroup(*[T(t, size=26, color=th.BODY) for t in ["1. filter", "2. wash", "3. ignite", "4. weigh"]]).arrange(RIGHT, buff=0.55).move_to([1.6, 1.15, 0])
        pan = Line([0.3, -1.3, 0], [2.9, -1.3, 0], color=th.INK, stroke_width=6)
        body = RoundedRectangle(corner_radius=0.15, width=3.4, height=1.0, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE).move_to([1.6, -2.0, 0])
        val = DecimalNumber(0, num_decimal_places=3, font_size=40, color=th.MINT).move_to(body).shift(LEFT * 0.3)
        gl = T("g", size=30, color=th.MINT).next_to(val, RIGHT, buff=0.15)
        with self.say("The precipitate is filtered, washed, ignited to drive off water, and weighed on an analytical balance."):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in stepsg], lag_ratio=0.4), run_time=1.8)
            self.play(FadeIn(body), Create(pan), FadeIn(val), FadeIn(gl))
            heap = VGroup(*[Dot([1.6 + rng.uniform(-0.5, 0.5), -1.2 + rng.uniform(0, 0.15), 0], radius=0.045, color=WHITE) for _ in range(len(ppt))])
            self.play(*[Transform(a, b) for a, b in zip(ppt, heap)], run_time=1.2)
            self.play(ChangeDecimalToValue(val, 0.233), run_time=1.5)
            self.sfx("click", gain=-8)
        prop = VGroup(
            M(r"233\ \mathrm{g\ BaSO_4} \;\text{contains}\; 96\ \mathrm{g\ SO_4^{2-}}", size=34),
            M(r"0.233\ \mathrm{g\ BaSO_4} \;\rightarrow\; 0.233 \times \tfrac{96}{233} = 0.096\ \mathrm{g\ SO_4^{2-}}", size=34, color=th.MINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.1, 0])
        with self.say("Suppose it weighs zero point two three three gram. A mole of barium sulphate, two hundred and thirty three grams, contains ninety six grams of sulphate. So simple proportion gives zero point zero nine six gram of sulphate. Chloride is weighed the same way as silver chloride, and iron as iron three oxide."):
            self.play(FadeOut(stepsg))
            self.play(Write(prop[0]))
            self.play(Write(prop[1]))
        self.play(FadeOut(VGroup(title, bk.g, bl, eq, ppt, pan, body, val, gl, prop)))

    def volumetric_intro(self):
        title = T("Volumetric analysis: measure a volume", size=36, color=th.SKY, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        bur = C.Burette(x=-3.6, top=2.6, bottom=-0.4, color=th.SKY)
        fl = C.Flask(center=[-3.6, -2.45, 0], scale=0.95, color=th.MUTED, opacity=0.4)
        lines = VGroup(
            T("a solution of known concentration", size=28, color=th.SKY),
            T("runs into the unknown", size=28, color=th.INK),
            T("until the reaction is exactly complete", size=28, color=th.INK),
            T("read the volume  →  calculate how much", size=28, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.2, 0.2, 0])
        with self.say("The volumetric route, also called titrimetric analysis, measures a volume instead. A solution of accurately known concentration runs from a burette into the unknown, until the reaction is exactly complete. The volume used tells you how much of the unknown was there."):
            self.play(FadeIn(title))
            self.add(bur.liquid)
            self.play(Create(bur.glass), FadeIn(bur.liquid), FadeIn(fl.g))
            for ln in lines:
                self.play(FadeIn(ln, shift=RIGHT * 0.2), run_time=0.5)
            titrate(self, bur, fl, 18, drops=5, run_time=0.35)
        self.play(FadeOut(VGroup(title, bur.glass, fl.g, lines)), FadeOut(bur.liquid))
        self.remove(bur.liquid)

    def compare_table(self):
        title = T("Gravimetric vs volumetric", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Feature", "Gravimetric", "Volumetric"],
                ["Measures", "mass of a precipitate", "volume of a standard solution"],
                ["Apparatus", "balance, crucible, furnace", "burette, pipette, volumetric flask"],
                ["Speed", "slow: hours to days", "fast: minutes"],
                ["Accuracy", "very high, to 0.01 mg", "high, about 0.1 %"],
                ["Indicator", "not needed", "usually needed"],
                ["Best for", "a few very accurate results", "routine, repeated analysis"]]
        tb = C.table(rows, [2.4, 4.6, 5.2], row_h=0.62, size=23, colors=[th.MUTED, th.MINT, th.SKY]).next_to(title, DOWN, buff=0.45)
        with self.say("Put the two side by side. Gravimetric work measures a mass, with a balance, a crucible and a furnace. It is slow, but extremely accurate. Volumetric work measures a volume, with a burette, a pipette and a volumetric flask. It is fast, accurate to about a tenth of a percent, and usually needs an indicator. That speed is why routine laboratories titrate.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.45)
                self.hold(v.dur / 8 - 0.45)
        self.play(FadeOut(VGroup(title, tb)))

    def equivalent_idea(self):
        title = T("The common currency: the equivalent", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        piv = np.array([0, 0.9, 0])
        Lb = 2.8
        tilt = ValueTracker(0)

        def ends():
            a = tilt.get_value()
            return piv + np.array([-Lb * np.cos(a), Lb * np.sin(a), 0]), piv + np.array([Lb * np.cos(a), -Lb * np.sin(a), 0])

        def beam():
            l, r = ends()
            g = VGroup(Line(l, r, color=th.INK, stroke_width=6))
            for e in (l, r):
                g.add(Line(e, e + DOWN * 1.1, color=th.MUTED, stroke_width=2),
                      Line(e + DOWN * 1.1 + LEFT * 0.9, e + DOWN * 1.1 + RIGHT * 0.9, color=th.INK, stroke_width=5))
            return g
        bm = always_redraw(beam)
        stand = VGroup(Polygon(piv + DOWN * 2.2 + LEFT * 0.5, piv + DOWN * 2.2 + RIGHT * 0.5, piv, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0))
        left = T("1.008 g  H", size=30, color=C.EL["H"], weight="BOLD")
        right = T("8 g  O", size=30, color=C.EL["O"], weight="BOLD")
        left.add_updater(lambda m: m.move_to(ends()[0] + DOWN * 0.8))
        right.add_updater(lambda m: m.move_to(ends()[1] + DOWN * 0.8))
        with self.say("To say that a reaction is exactly complete, we need a common currency, like an exchange rate between substances. Chemists chose hydrogen as the reference. One point zero zero eight grams of hydrogen is worth exactly eight grams of oxygen, because that is how much oxygen combines with it."):
            self.play(FadeIn(title), FadeIn(stand))
            self.add(bm, left, right)
            self.play(FadeIn(bm), FadeIn(left), FadeIn(right))
        for txt, col in [("35.5 g  Cl", C.EL["Cl"]), ("12 g  Mg", C.EL["Mg"]), ("9 g  Al", C.EL["Al"])]:
            new = T(txt, size=30, color=col, weight="BOLD").move_to(right)
            self.play(tilt.animate.set_value(0.18), run_time=0.35)
            right.clear_updaters()
            self.play(Transform(right, new), run_time=0.4)
            right.add_updater(lambda m: m.move_to(ends()[1] + DOWN * 0.8))
            self.sfx("tick", gain=-12)
            self.play(tilt.animate.set_value(0), run_time=0.5, rate_func=rate_functions.ease_out_back)
        defn = self.callout("key", "Equivalent weight: the parts by mass of a substance that combine with or displace 1.008 parts of hydrogen, 8 parts of oxygen or 35.5 parts of chlorine.", width=11.5, size=26)
        defn.to_edge(DOWN, buff=0.5)
        with self.say("Thirty five point five grams of chlorine, twelve of magnesium, nine of aluminium. Each balances the same one point zero zero eight grams of hydrogen. That balancing mass is the equivalent weight: the parts by mass of a substance that combine with or displace one point zero zero eight parts of hydrogen, eight of oxygen, or thirty five point five of chlorine."):
            self.play(FadeIn(defn, shift=UP * 0.3))
        left.clear_updaters()
        right.clear_updaters()
        self.play(FadeOut(VGroup(stand, left, right, defn)), FadeOut(bm))
        self.remove(bm)
        big = M(r"E", r"=", r"{\text{molar mass}", r"\over", r"n\text{-factor}}", size=72).move_to(UP * 0.6)
        big[0].set_color(th.AMBER)
        big[4].set_color(th.MINT)
        notes = VGroup(T("a pure number: no unit", size=26, color=th.BODY),
                       T("in grams, it is one gram equivalent", size=26, color=th.BODY)).arrange(DOWN, buff=0.2).next_to(big, DOWN, buff=0.6)
        with self.say("In modern language, the equivalent weight is the molar mass divided by the n factor, the number of reacting units each formula unit supplies. Equivalent weight is a relative number with no unit. Expressed in grams, it is called one gram equivalent."):
            self.play(Write(big))
            self.play(Circumscribe(big[4], color=th.MINT))
            self.play(FadeIn(notes, shift=UP * 0.2))
        nb = C.show_neby(self, "think", height=1.5)
        with self.say("Everything in this unit comes down to finding that n factor. So let us learn to find it, first for elements, then for compounds."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, big, notes)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        o = C.atom("O", r=0.55).move_to([-3.6, 0.6, 0])
        h1 = C.atom("H", r=0.32).move_to(o.get_center() + np.array([-0.85, -0.6, 0]))
        h2 = C.atom("H", r=0.32).move_to(o.get_center() + np.array([0.85, -0.6, 0]))
        bonds = VGroup(Line(o.get_center(), h1.get_center(), color=th.MUTED, stroke_width=6), Line(o.get_center(), h2.get_center(), color=th.MUTED, stroke_width=6))
        mol = VGroup(bonds, o, h1, h2)
        m1 = M(r"16\ \mathrm{g\ O} \;\leftrightarrow\; 2 \times 1.008\ \mathrm{g\ H}", size=40).move_to([2.6, 1.5, 0])
        m2 = M(r"\tfrac{16}{2} = 8\ \mathrm{g\ O} \;\leftrightarrow\; 1.008\ \mathrm{g\ H}", size=40, color=th.AMBER).next_to(m1, DOWN, buff=0.45)
        with self.say("Take water. One oxygen atom, valency two, holds two hydrogen atoms. So sixteen grams of oxygen combine with two times one point zero zero eight grams of hydrogen."):
            self.play(FadeIn(o, scale=0.5))
            self.play(Create(bonds), FadeIn(h1, shift=LEFT * 0.3), FadeIn(h2, shift=RIGHT * 0.3))
            self.play(Write(m1))
        with self.say("Divide both sides by two, the valency. Eight grams of oxygen go with one point zero zero eight grams of hydrogen. Eight is the equivalent weight of oxygen: its atomic weight divided by its valency."):
            self.play(Write(m2))
            self.play(Indicate(m2, color=th.AMBER))
        self.play(FadeOut(VGroup(m1, m2)), FadeOut(mol))
        der = VGroup(
            M(r"\text{1 atom of X (atomic weight } A,\ \text{valency } v) \text{ holds } v \text{ atoms of H}", size=32),
            M(r"A \text{ parts of X} \;\leftrightarrow\; 1.008\,v \text{ parts of H}", size=36),
            M(r"\frac{A}{v} \text{ parts of X} \;\leftrightarrow\; 1.008 \text{ parts of H}", size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0.6, 0.6, 0])
        final = M(r"\text{equivalent weight}", r"=", r"{\text{atomic weight}", r"\over", r"\text{valency}}", size=54).next_to(der, DOWN, buff=0.55)
        final[0].set_color(th.AMBER)
        with self.say("Now any element X, of atomic weight A and valency v. One atom of X combines with v atoms of hydrogen. So A parts of X combine with one point zero zero eight times v parts of hydrogen. Divide by v."):
            for d in der:
                self.play(Write(d), run_time=1.2)
        with self.say("The mass of X that combines with one point zero zero eight parts of hydrogen is A over v. Equivalent weight equals atomic weight divided by valency."):
            self.sfx("impact", gain=-12)
            self.play(Write(final))
            self.play(Circumscribe(final, color=th.AMBER))
        alt = VGroup(M(r"\text{atomic weight} = E \times \text{valency}", size=36), M(r"\text{valency} = \frac{\text{atomic weight}}{E}", size=36)).arrange(RIGHT, buff=1.0)
        self.play(FadeOut(der), FadeOut(mol), final.animate.to_edge(UP, buff=0.8))
        alt.next_to(final, DOWN, buff=0.45)
        with self.say("Rearrange it and you get the two other forms the board asks for: atomic weight equals equivalent weight times valency, and valency equals atomic weight over equivalent weight."):
            self.play(FadeIn(alt, shift=UP * 0.2))
        self.play(FadeOut(alt))
        data = [("H", 1.008, 1), ("O", 16, 2), ("Cl", 35.5, 1), ("Mg", 24, 2), ("Al", 27, 3), ("Ca", 40, 2), ("Fe", 56, 2), ("Fe", 56, 3)]
        bars = VGroup()
        x0 = -5.6
        base_y = -2.7
        for i, (s, A, v) in enumerate(data):
            E = A / v
            x = x0 + i * 1.6
            col = C.EL[s]
            bar = Rectangle(width=0.8, height=max(0.05, E * 0.105), fill_color=col, fill_opacity=0.85, stroke_width=0).move_to([x, base_y, 0], aligned_edge=DOWN)
            val = T(f"{E:.2f}".rstrip("0").rstrip("."), size=22, color=th.INK, weight="SEMIBOLD").next_to(bar, UP, buff=0.08)
            nm = T(s + ("²⁺" if (s == "Fe" and v == 2) else ("³⁺" if s == "Fe" else "")), size=24, color=col, weight="BOLD").next_to([x, base_y, 0], DOWN, buff=0.15)
            fr = T(f"{A:g}/{v}", size=18, color=th.MUTED).next_to(val, UP, buff=0.06)
            bars.add(VGroup(bar, val, nm, fr))
        with self.say("Here are the values you should know. Hydrogen one point zero zero eight. Oxygen eight. Chlorine thirty five point five. Magnesium, twenty four over two, twelve. Aluminium, twenty seven over three, nine. Calcium, twenty.") as v:
            for b in bars[:6]:
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1:]), run_time=0.5)
                self.hold(v.dur / 6 - 0.5)
        nb = C.show_neby(self, "surprised", height=1.4, at=[5.4, 1.3, 0])
        with self.say("And iron? Iron has two. As ferrous iron, valency two, its equivalent weight is twenty eight. As ferric iron, valency three, it is eighteen point six seven. Same atom, two different equivalent weights."):
            for b in bars[6:]:
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1:]), run_time=0.6)
            self.play(Indicate(VGroup(bars[6], bars[7]), color=th.AMBER))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(bars, final)))
        care = self.callout("careful", "Equivalent weight is not a fixed property. Atomic weight and molar mass are fixed; equivalent weight depends on the reaction. Always ask: in which reaction?", width=11, size=28)
        with self.say("So remember this. Atomic weight and molar mass are fixed numbers. Equivalent weight is not. It depends on the reaction. Before you quote an equivalent weight, always ask: in which reaction?"):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))
        head, prob = C.example_head(self, "A metal has equivalent weight 9 and valency 3. Find its atomic weight. Another element has atomic weight 40 and equivalent weight 20. Find its valency.")
        st = C.steps(r"A = E \times v = 9 \times 3 = 27 \quad (\text{aluminium})",
                     r"v = \frac{A}{E} = \frac{40}{20} = 2 \quad (\text{calcium})", size=42).next_to(prob, DOWN, buff=0.7).align_to(prob, LEFT)
        with self.say("Quick practice. A metal has equivalent weight nine and valency three. What is its atomic weight? And an element of atomic weight forty has equivalent weight twenty. What is its valency?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("Atomic weight is equivalent weight times valency: nine times three, twenty seven. That is aluminium. And valency is atomic weight over equivalent weight: forty over twenty, two. That is calcium."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        title = T("The n-factor depends on the class", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Class", "n-factor is", "E ="],
                ["Acid", "basicity: replaceable H⁺", "molar mass ÷ basicity"],
                ["Base", "acidity: replaceable OH⁻", "molar mass ÷ acidity"],
                ["Salt", "total + (or −) charge", "molar mass ÷ total charge"],
                ["Oxidising agent", "electrons gained", "molar mass ÷ e⁻ gained"],
                ["Reducing agent", "electrons lost", "molar mass ÷ e⁻ lost"]]
        tb = C.table(rows, [3.0, 4.6, 4.4], row_h=0.66, size=25, colors=[th.AMBER, th.INK, th.BODY]).next_to(title, DOWN, buff=0.45)
        with self.say("For a compound, valency is replaced by the n factor, the number of reacting units per formula unit. What counts as a unit depends on the class. For an acid, it is the basicity, the number of replaceable hydrogen ions. For a base, the acidity, the number of replaceable hydroxide ions. For a salt, the total positive charge. And for an oxidising or reducing agent, the number of electrons gained or lost.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.45)
                self.hold(v.dur / 6 - 0.5)
        self.play(FadeOut(VGroup(title, tb)))
        self.acids_bases()
        self.salts()
        self.redox_n()
        self.permanganate()
        self.example_11()
        self.quiz("The equivalent weight of KMnO₄ (molar mass 158) in acidic medium is",
                  ["158", "79", "52.67", "31.6"], 3,
                  "A one mark question that appears almost every year. Potassium permanganate, in acidic medium. What is its equivalent weight? Pause and think.",
                  "D, thirty one point six. In acid, manganese drops from plus seven to plus two, gaining five electrons, so we divide one fifty eight by five. Fifty two point six seven is the neutral medium value, and one fifty eight is the strongly alkaline one.")

    def acids_bases(self):
        def molecule(center, parts):
            g = VGroup()
            for sym, off, r in parts:
                g.add(C.atom(sym, r=r).move_to(np.array(center) + np.array([off[0], off[1], 0])))
            return g
        c1 = np.array([-3.4, 0.6, 0])
        core = VGroup(C.atom("S", r=0.42).move_to(c1))
        for ang in [45, 135, 225, 315]:
            a = np.radians(ang)
            core.add(C.atom("O", r=0.3).move_to(c1 + 0.85 * np.array([np.cos(a), np.sin(a), 0])))
        hs = VGroup(C.atom("H", r=0.24).move_to(c1 + 1.45 * np.array([np.cos(np.radians(135)), np.sin(np.radians(135)), 0])),
                    C.atom("H", r=0.24).move_to(c1 + 1.45 * np.array([np.cos(np.radians(-45)), np.sin(np.radians(-45)), 0])))
        name = chem(r"H_2SO_4", size=44).next_to(core, DOWN, buff=1.0)
        eqs = M(r"E = \frac{98}{2} = 49", size=48, color=th.AMBER).move_to([2.6, 0.6, 0])
        cnt = T("2 replaceable H⁺", size=28, color=th.SKY).next_to(eqs, UP, buff=0.5)
        with self.say("Watch an acid. Sulphuric acid, molar mass ninety eight, has two hydrogens it can hand over as hydrogen ions."):
            self.play(FadeIn(core, scale=0.6), FadeIn(hs), FadeIn(name))
        with self.say("Both of them leave. Basicity two, so the equivalent weight is ninety eight over two, forty nine."):
            self.play(hs[0].animate.shift(UL * 1.2).set_color(th.SKY), hs[1].animate.shift(DR * 1.2).set_color(th.SKY), run_time=1.0)
            self.sfx("pop")
            self.play(FadeIn(cnt), Write(eqs))
        self.play(FadeOut(VGroup(core, hs, name, eqs, cnt)))
        rows = VGroup(
            VGroup(chem("HCl"), M(r"n=1", size=36, color=th.SKY), M(r"E = 36.5", size=40, color=th.AMBER)),
            VGroup(chem(r"H_3PO_4"), M(r"n=3", size=36, color=th.SKY), M(r"E = \tfrac{98}{3} = 32.67", size=40, color=th.AMBER)),
            VGroup(chem("NaOH"), M(r"n=1", size=36, color=th.SKY), M(r"E = 40", size=40, color=th.AMBER)),
            VGroup(chem(r"Ca(OH)_2"), M(r"n=2", size=36, color=th.SKY), M(r"E = \tfrac{74}{2} = 37", size=40, color=th.AMBER)),
        )
        for r in rows:
            r[0].move_to([-4.0, 0, 0])
            r[1].move_to([-1.2, 0, 0])
            r[2].move_to([2.6, 0, 0])
        rows.arrange(DOWN, buff=0.55).move_to(ORIGIN)
        for r in rows:
            r[0].set_x(-4.0)
            r[1].set_x(-1.2)
            r[2].set_x(2.4)
        with self.say("The same rule everywhere. Hydrochloric acid gives one, so thirty six point five. Phosphoric acid, fully neutralised, gives three, so thirty two point six seven. For bases, count hydroxide ions. Sodium hydroxide, forty. Calcium hydroxide, seventy four over two, thirty seven.") as v:
            for r in rows:
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=RIGHT * 0.2), run_time=0.5)
                self.play(Write(r[2]), run_time=0.7)
                self.hold(v.dur / 4 - 1.2)
        self.play(FadeOut(rows))

    def salts(self):
        title = chem(r"Al_2(SO_4)_3", size=56).to_edge(UP, buff=0.9)
        al = VGroup(*[C.ion("Al", "3+", r=0.42) for _ in range(2)]).arrange(RIGHT, buff=0.6).move_to([-2.6, 0.2, 0])
        so = VGroup(*[VGroup(Circle(radius=0.48, fill_color=C.EL["S"], fill_opacity=1, stroke_color=WHITE, stroke_width=1.5), T("SO₄²⁻", size=20, color="#10131f", weight="BOLD")) for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to([2.6, 0.2, 0])
        lab = M(r"2 \times (+3) = +6", size=44, color=th.SKY).next_to(al, DOWN, buff=0.6)
        lab2 = M(r"3 \times (-2) = -6", size=44, color=th.MUTED).next_to(so, DOWN, buff=0.6)
        res = M(r"E = \frac{342}{6} = 57", size=52, color=th.AMBER).to_edge(DOWN, buff=0.8)
        with self.say("For a salt, count the total charge on one side. Aluminium sulphate splits into two aluminium ions, each plus three, and three sulphate ions, each minus two."):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in al], lag_ratio=0.3), LaggedStart(*[FadeIn(b, scale=0.5) for b in so], lag_ratio=0.3))
        with self.say("Total positive charge, two times three, is six. The negative side agrees, three times minus two. So the n factor is six, and the equivalent weight is three hundred forty two over six, fifty seven."):
            self.play(Write(lab), Write(lab2))
            self.play(Write(res))
        self.play(FadeOut(VGroup(title, al, so, lab, lab2, res)))

    def redox_n(self):
        title = T("Oxidising agent: count electrons gained", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"Cr_2O_7^{2-} + 14H^+ + 6e^- \rightarrow 2Cr^{3+} + 7H_2O", size=42).next_to(title, DOWN, buff=0.5)
        cr = VGroup(*[C.atom("Cr", r=0.42) for _ in range(2)]).arrange(RIGHT, buff=1.4).move_to([-1.5, -0.6, 0])
        ox = VGroup(*[T("+6", size=30, color=th.AMBER, weight="BOLD").next_to(c, UP, buff=0.15) for c in cr])
        es = VGroup(*[C.electron().move_to([4.2 + 0.35 * (k % 3), 0.4 - 0.4 * (k // 3), 0]) for k in range(6)])
        res = M(r"n = 6 \quad\Rightarrow\quad E = \frac{294}{6} = 49", size=46, color=th.AMBER).to_edge(DOWN, buff=0.7)
        with self.say("For a redox reagent, the n factor is the number of electrons transferred per formula unit. Potassium dichromate in acid: each of its two chromium atoms sits at plus six, and ends at plus three."):
            self.play(FadeIn(title), Write(eq))
            self.play(FadeIn(cr), FadeIn(ox))
        targets = [cr[k // 3].get_center() + 0.6 * np.array([np.cos(a), np.sin(a), 0]) for k, a in enumerate(np.linspace(0, TAU, 6, endpoint=False) + 0.4)]
        new = VGroup(*[T("+3", size=30, color=th.MINT, weight="BOLD").next_to(c, UP, buff=0.15) for c in cr])
        with self.say("Three electrons for each chromium, two chromiums: six electrons gained per formula unit. So the equivalent weight is two ninety four over six, forty nine."):
            self.play(FadeIn(es))
            self.play(*[e.animate.move_to(t) for e, t in zip(es, targets)], run_time=1.4)
            self.sfx("pop")
            self.play(*[Transform(a, b) for a, b in zip(ox, new)])
            self.play(Write(res))
        self.play(FadeOut(VGroup(title, eq, cr, ox, es, res)))

    def permanganate(self):
        title = T("Potassium permanganate: three equivalent weights", size=34, color=C.PURPLE, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax_x = -4.6
        ytop, ybot = 2.2, -2.6

        def y_of(o):
            return ybot + (o - 1) * (ytop - ybot) / 6.5
        ladder = VGroup(Line([ax_x, y_of(1.5), 0], [ax_x, y_of(7.4), 0], color=th.FAINT, stroke_width=4))
        for o in range(2, 8):
            ladder.add(Line([ax_x - 0.12, y_of(o), 0], [ax_x + 0.12, y_of(o), 0], color=th.MUTED, stroke_width=3),
                       T(f"+{o}", size=24, color=th.MUTED).next_to([ax_x - 0.12, y_of(o), 0], LEFT, buff=0.12))
        mn = C.atom("Mn", r=0.3).move_to([ax_x + 0.6, y_of(7), 0])
        cases = [(2, 5, "acidic", r"MnO_4^- + 8H^+ + 5e^- \rightarrow Mn^{2+} + 4H_2O", "158 ÷ 5 = 31.6", th.CORAL),
                 (4, 3, "neutral / faintly alkaline", r"MnO_4^- + 2H_2O + 3e^- \rightarrow MnO_2 + 4OH^-", "158 ÷ 3 = 52.67", th.AMBER),
                 (6, 1, "strongly alkaline", r"MnO_4^- + e^- \rightarrow MnO_4^{2-}", "158 ÷ 1 = 158", th.SKY)]
        with self.say("Now the star of every exam: potassium permanganate, molar mass one fifty eight. Manganese in it sits at plus seven. What it becomes depends on the medium, and so does its equivalent weight."):
            self.play(FadeIn(title), Create(ladder), FadeIn(mn, scale=0.5))
        rows = VGroup()
        narr = [
            "In acidic medium, dilute sulphuric acid, it falls all the way to manganese two plus. Five electrons gained. Equivalent weight one fifty eight over five, thirty one point six.",
            "In neutral or faintly alkaline medium, it stops at manganese dioxide, plus four. Three electrons. Fifty two point six seven.",
            "In strongly alkaline medium, it only reaches manganate, plus six. One electron. Equivalent weight one fifty eight.",
        ]
        for k, (o, n, med, tex, ev, col) in enumerate(cases):
            row = VGroup(T(med, size=24, color=col, weight="SEMIBOLD"), chem(tex, size=30), T(ev, size=28, color=col, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            row.move_to([1.6, 1.5 - 1.75 * k, 0]).align_to([-1.6, 0, 0], LEFT)
            rows.add(row)
            ghost = mn.copy().set_opacity(0.25)
            arr = Arrow([ax_x + 0.6 + 0.0, y_of(7) - 0.3, 0], [ax_x + 0.6 + 0.0, y_of(o) + 0.3, 0], buff=0, color=col, stroke_width=4)
            es = VGroup(*[C.electron(0.09) for _ in range(n)]).arrange(DOWN, buff=0.06).next_to(arr, RIGHT, buff=0.2)
            with self.say(narr[k]):
                self.add(ghost)
                self.play(mn.animate.move_to([ax_x + 0.6, y_of(o), 0]), GrowArrow(arr), FadeIn(es, shift=LEFT * 0.3), run_time=1.2)
                self.play(FadeIn(row, shift=LEFT * 0.2))
            self.play(FadeOut(VGroup(arr, es, ghost)), mn.animate.move_to([ax_x + 0.6, y_of(7), 0]), run_time=0.5)
        chk = M(r"\text{charge check: } (-1) + 8(+1) + 5(-1) = +2 \;=\; +2\ \checkmark", size=32, color=th.MINT).to_edge(DOWN, buff=0.45)
        with self.say("Every half equation balances in charge as well as mass. Check the acidic one: minus one, plus eight, minus five, gives plus two on the left. And plus two on the right."):
            self.play(Write(chk))
            self.play(Indicate(rows[0], color=th.CORAL, scale_factor=1.03))
        self.play(FadeOut(VGroup(title, ladder, mn, rows, chk)))

    def example_11(self):
        head, prob = C.example_head(self, "Find the equivalent weight of (a) H₃PO₄ reacting with NaOH to give Na₂HPO₄, (b) K₂Cr₂O₇ as an oxidant in acid, (c) Na₂CO₃ reacting with dilute HCl.")
        st = C.steps(r"(a)\ \ \mathrm{2NaOH + H_3PO_4 \rightarrow Na_2HPO_4 + 2H_2O}:\ \ n = 2,\ E = \tfrac{98}{2} = 49",
                     r"(b)\ \ \mathrm{Cr_2O_7^{2-} + 14H^+ + 6e^- \rightarrow 2Cr^{3+} + 7H_2O}:\ \ n = 6,\ E = \tfrac{294}{6} = 49",
                     r"(c)\ \ \mathrm{Na_2CO_3 + 2HCl \rightarrow 2NaCl + H_2O + CO_2}:\ \ n = 2,\ E = \tfrac{106}{2} = 53", size=34, buff=0.5)
        st.next_to(prob, DOWN, buff=0.6).align_to(prob, LEFT)
        with self.say("Worked example one point one. Find the equivalent weight of phosphoric acid when it reacts with sodium hydroxide to give disodium hydrogen phosphate, of potassium dichromate in acid, and of sodium carbonate with dilute hydrochloric acid."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        nb = C.show_neby(self, "think", height=1.3)
        with self.say("Part a has a trap. Only two of the three hydrogens are replaced in this reaction, so the effective basicity is two, not three. Ninety eight over two, forty nine."):
            self.play(Write(st[0]))
        with self.say("Part b, dichromate gains six electrons, as we just saw. Two ninety four over six, forty nine."):
            self.play(Write(st[1]))
        with self.say("Part c, one sodium carbonate neutralises two hydrogen ions, which also equals the total charge on its two sodium ions. One oh six over two, fifty three."):
            self.play(Write(st[2]))
            nb.set_state("success", once=True)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        bk = C.Beaker(center=[-4.2, -0.4, 0], w=2.4, h=2.8, level=0.65, color=C.WATER, opacity=0.25)
        rng = np.random.default_rng(5)
        sol = VGroup(*[Dot(p, radius=0.06, color=th.AMBER) for p in bk.inside(rng, 24, level=0.65)])
        lab = VGroup(T("solute", size=24, color=th.AMBER), T("solvent", size=24, color=C.WATER)).arrange(DOWN, buff=0.15).next_to(bk.g, DOWN, buff=0.25)
        defn = para("Concentration = amount of solute in a stated amount of solvent or solution", width=6.5, size=30, color=th.INK).move_to([2.4, 2.3, 0])
        with self.say("Concentration is the amount of solute in a stated amount of solvent, or of solution. The units differ only in how they measure each of those two amounts."):
            self.play(FadeIn(bk.g), LaggedStart(*[FadeIn(d, scale=0.3) for d in sol], lag_ratio=0.04), FadeIn(lab))
            self.play(FadeIn(defn, shift=UP * 0.2))
        fam1 = VGroup(T("per volume of solution", size=26, color=th.SKY, weight="BOLD"),
                      T("% w/v  ·  g/L  ·  molarity M", size=26, color=th.INK), T("normality N  ·  formality F", size=26, color=th.INK))
        fam2 = VGroup(T("per mass", size=26, color=th.MINT, weight="BOLD"),
                      T("% w/w  ·  molality m", size=26, color=th.INK), T("ppm  ·  ppb", size=26, color=th.INK))
        for f in (fam1, fam2):
            f.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fams = VGroup(fam1, fam2).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([2.4, -1.0, 0])
        with self.say("Sort them into two families. Percentage weight by volume, grams per litre, molarity, normality and formality all count per litre of solution. Percentage by mass and molality use only masses, and ppm and ppb are parts by mass too."):
            self.play(FadeIn(fam1, shift=RIGHT * 0.2))
            self.play(FadeIn(fam2, shift=RIGHT * 0.2))
        self.play(FadeOut(VGroup(defn, fams)))
        defs = VGroup(
            M(r"M = \frac{\text{moles of solute}}{\text{litres of solution}}", size=38),
            M(r"m = \frac{\text{moles of solute}}{\text{kg of solvent}}", size=38),
            M(r"N = \frac{\text{gram equivalents of solute}}{\text{litres of solution}}", size=38),
            M(r"S = \frac{\text{grams of solute}}{\text{litres of solution}}", size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.3, 0.3, 0])
        cols = [th.SKY, th.MINT, th.AMBER, th.BODY]
        for d, c in zip(defs, cols):
            d.set_color(c)
        with self.say("The four you will use most. Molarity, moles of solute per litre of solution. Molality, moles of solute per kilogram of solvent. Normality, gram equivalents per litre of solution. And strength, grams per litre.") as v:
            for d in defs:
                self.play(Write(d), run_time=0.9)
                self.hold(v.dur / 4 - 0.9)
        self.play(FadeOut(defs))
        self.temperature_demo(bk, sol, lab)
        self.formulas()
        self.formality_ppm()
        self.example_12()
        self.example_13()
        self.tip("Molarity, normality and formality change with temperature (volume expands). Molality, % by mass and mole fraction do not: they use masses only.",
                 "A favourite one mark question. Which concentration unit does not change with temperature? Any unit that uses the volume of solution changes, because liquids expand when heated. Molality, percentage by mass and mole fraction use only masses, so they stay fixed.", state="wink")
        self.quiz("A 0.1 M solution of H₂SO₄ is the same as",
                  ["0.05 N", "0.1 N", "0.2 N", "0.4 N"], 2,
                  "Now try this one. A zero point one molar solution of sulphuric acid has what normality? Pause and think.",
                  "C, zero point two normal. Normality is molarity times the n factor, and sulphuric acid has basicity two. Zero point zero five is the trap, from dividing instead of multiplying.")

    def temperature_demo(self, bk, sol, lab):
        Tt = ValueTracker(20)

        def V():
            return 1 + 0.00045 * (Tt.get_value() - 20)
        base_h = bk.liq.height
        bk.liq.add_updater(lambda m: m.stretch_to_fit_height(base_h * (1 + 8 * (V() - 1))).align_to(bk.outline, DOWN).shift(UP * 0.0))
        th_x = -2.3
        tube = RoundedRectangle(corner_radius=0.08, width=0.16, height=2.6, stroke_color=th.INK, stroke_width=2).move_to([th_x, -0.2, 0])
        bulb = Circle(radius=0.17, fill_color=th.CORAL, fill_opacity=1, stroke_color=th.INK, stroke_width=2).next_to(tube, DOWN, buff=-0.05)
        merc = always_redraw(lambda: Rectangle(width=0.08, height=0.2 + 2.2 * (Tt.get_value() - 10) / 80, fill_color=th.CORAL, fill_opacity=1, stroke_width=0)
                             .move_to(tube.get_bottom() + UP * (0.1 + 1.1 * (Tt.get_value() - 10) / 80)))
        tlab = DecimalNumber(20, num_decimal_places=0, font_size=32, color=th.CORAL, unit=r"^{\circ}\mathrm{C}")
        tlab.add_updater(lambda m: m.set_value(Tt.get_value()).next_to(tube, UP, buff=0.15))
        rows = VGroup()
        Mv = DecimalNumber(1.0, num_decimal_places=3, font_size=40, color=th.SKY)
        mv = DecimalNumber(1.0, num_decimal_places=3, font_size=40, color=th.MINT)
        Vv = DecimalNumber(1.0, num_decimal_places=3, font_size=40, color=th.INK)
        r1 = VGroup(T("volume of solution (L)", size=26, color=th.BODY), Vv)
        r2 = VGroup(T("molarity (mol/L)", size=26, color=th.SKY), Mv)
        r3 = VGroup(T("molality (mol/kg)", size=26, color=th.MINT), mv)
        for r in (r1, r2, r3):
            r.arrange(RIGHT, buff=0.4)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.45).move_to([2.6, 0.2, 0])
        Vv.add_updater(lambda m: m.set_value(V()))
        Mv.add_updater(lambda m: m.set_value(1 / V()))
        note = T("1 mol solute · 1 kg water · expansion drawn ×8", size=20, color=th.MUTED).next_to(rows, DOWN, buff=0.5)
        with self.say("Here is why the two families behave differently. One mole of solute in about one litre of solution. Molarity one, molality about one. Now we heat it, from twenty to eighty degrees Celsius."):
            self.add(merc)
            self.play(FadeIn(VGroup(tube, bulb)), FadeIn(merc), FadeIn(tlab), FadeIn(rows), FadeIn(note))
        self.add(bk.liq)
        with self.say("The liquid expands. The moles of solute stay the same, but they now share a bigger volume, so the molarity falls. The masses do not change at all, so the molality stays exactly where it was."):
            self.play(Tt.animate.set_value(80), sol.animate.shift(UP * 0.12), run_time=4.0, rate_func=smooth)
            self.play(Indicate(r2, color=th.SKY), Indicate(r3, color=th.MINT))
        nb = C.show_neby(self, "cool", height=1.4)
        with self.say("Molality, percentage by mass and mole fraction do not care about temperature. That is why physical chemists love molality."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        bk.liq.clear_updaters()
        for m in (Vv, Mv, tlab):
            m.clear_updaters()
        self.play(FadeOut(VGroup(bk.g, sol, lab, tube, bulb, tlab, rows, note)), FadeOut(merc))
        self.remove(merc)

    def formulas(self):
        title = T("Working formulas", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        f = VGroup(
            M(r"M = \frac{w \times 1000}{M_w \times V_{\mathrm{cm^3}}}", size=44),
            M(r"N = \frac{w \times 1000}{E \times V_{\mathrm{cm^3}}}", size=44),
            M(r"S = N \times E = M \times M_w", size=44),
            M(r"N = M \times n", size=52, color=th.AMBER),
        )
        VGroup(VGroup(f[0], f[1]).arrange(RIGHT, buff=1.0), f[2], f[3]).arrange(DOWN, buff=0.55).next_to(title, DOWN, buff=0.6)
        with self.say("The working formulas follow straight from the definitions. Molarity is the mass w, times a thousand, over molar mass times volume in cubic centimetres. Normality is the same with the equivalent weight in place of molar mass."):
            self.play(FadeIn(title), Write(f[0]))
            self.play(TransformFromCopy(f[0], f[1]))
        with self.say("Strength in grams per litre is normality times equivalent weight, or molarity times molar mass. And since E is molar mass over n, normality is simply molarity times the n factor."):
            self.play(Write(f[2]))
            self.play(Write(f[3]))
            self.play(Circumscribe(f[3], color=th.AMBER))
        self.play(FadeOut(VGroup(title, f)))

    def formality_ppm(self):
        lat = VGroup()
        for i in range(4):
            for j in range(4):
                s = "Na" if (i + j) % 2 == 0 else "Cl"
                lat.add(C.atom(s, r=0.22 if s == "Na" else 0.3, size=14).move_to([-4.2 + 0.62 * i, 0.9 - 0.62 * j, 0]))
        lt = T("NaCl: ions, no molecules", size=24, color=th.MUTED).next_to(lat, DOWN, buff=0.4)
        fdef = VGroup(T("Formality F", size=32, color=th.AMBER, weight="BOLD"),
                      para("formula masses of solute per litre of solution. 58.5 g NaCl made up to 1 L is 1 F.", width=5.6, size=26, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.5, 0.4, 0])
        with self.say("Formality is used for ionic solids like sodium chloride. A crystal of salt has no molecules, only ions. Dissolve it, and the ions drift apart. So instead of moles of molecules, we count formula masses: fifty eight point five grams made up to one litre is one formal."):
            self.play(LaggedStart(*[FadeIn(a, scale=0.4) for a in lat], lag_ratio=0.04), FadeIn(lt))
            rng = np.random.default_rng(2)
            self.play(*[a.animate.shift(np.array([rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6), 0])) for a in lat], run_time=1.5)
            self.play(FadeIn(fdef, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(lat, lt, fdef)))
        sq = Square(side_length=4.0, stroke_color=th.SKY, stroke_width=3, fill_color=C.WATER, fill_opacity=0.12).move_to([-3.4, -0.2, 0])
        grid = VGroup(*[Line(sq.get_corner(DL) + RIGHT * 0.4 * k, sq.get_corner(UL) + RIGHT * 0.4 * k, color=th.FAINT, stroke_width=1) for k in range(1, 10)],
                      *[Line(sq.get_corner(DL) + UP * 0.4 * k, sq.get_corner(DR) + UP * 0.4 * k, color=th.FAINT, stroke_width=1) for k in range(1, 10)])
        sl = T("1 kg of water = 1 000 000 mg", size=24, color=th.SKY).next_to(sq, UP, buff=0.2)
        speck = Dot(sq.get_center() + RIGHT * 0.7 + UP * 0.5, radius=0.03, color=th.CORAL)
        defs = VGroup(M(r"\text{ppm} = \frac{\text{mass of solute}}{\text{mass of solution}} \times 10^{6}", size=36),
                      T("1 ppm ≈ 1 mg per litre", size=28, color=th.AMBER),
                      T("1 ppb ≈ 1 μg per litre", size=28, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.9, 1.4, 0])
        with self.say("For very dilute solutions we use parts per million and parts per billion. A kilogram of water is a million milligrams. One milligram of solute in it, this tiny speck, is one part per million. For dilute water solutions, one ppm is one milligram per litre, and one ppb is one microgram per litre."):
            self.play(Create(sq), Create(grid), FadeIn(sl))
            self.play(FadeIn(speck, scale=4), Flash(speck, color=th.CORAL, flash_radius=0.3))
            self.play(Write(defs[0]))
            self.play(FadeIn(defs[1:], shift=UP * 0.2))
        ax0 = np.array([0.8, -2.6, 0])
        b1 = Rectangle(width=1.2, height=0.5, fill_color=th.MINT, fill_opacity=0.85, stroke_width=0).move_to(ax0 + RIGHT * 1.0, aligned_edge=DOWN)
        b2 = Rectangle(width=1.2, height=2.5, fill_color=th.CORAL, fill_opacity=0.85, stroke_width=0).move_to(ax0 + RIGHT * 3.6, aligned_edge=DOWN)
        l1 = T("WHO: 10 ppb", size=22, color=th.MINT).next_to(b1, UP, buff=0.1)
        l2 = T("Nepal: 50 ppb", size=22, color=th.CORAL).next_to(b2, UP, buff=0.1)
        cap = T("arsenic in drinking water", size=22, color=th.MUTED).next_to(VGroup(b1, b2), DOWN, buff=0.15)
        self.play(FadeOut(defs[0]), defs[1:].animate.move_to([2.9, 1.9, 0]))
        with self.say("Why does this matter in Nepal? Arsenic in Terai tube wells. The national standard is fifty parts per billion, just zero point zero five milligram per litre, and the World Health Organisation guideline is even lower, ten ppb. Tiny numbers, serious health limits."):
            self.play(GrowFromEdge(b1, DOWN), FadeIn(l1))
            self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(cap))
        self.play(FadeOut(VGroup(sq, grid, sl, speck, defs[1:], b1, b2, l1, l2, cap)))

    def example_12(self):
        head, prob = C.example_head(self, "What mass of anhydrous sodium carbonate is needed to prepare 250 cm³ of 0.1 N Na₂CO₃ solution?")
        st = C.steps(r"E(\mathrm{Na_2CO_3}) = \tfrac{106}{2} = 53",
                     r"\text{equivalents} = N \times V_{\mathrm{L}} = 0.1 \times 0.250 = 0.025",
                     r"w = 0.025 \times 53 = 1.325\ \mathrm{g}", size=40).next_to(prob, DOWN, buff=0.55).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example one point two. What mass of anhydrous sodium carbonate is needed to make two hundred and fifty cubic centimetres of a zero point one normal solution?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("The equivalent weight is one oh six over two, fifty three. The number of equivalents needed is normality times volume in litres: zero point one times zero point two five, zero point zero two five."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        body = RoundedRectangle(corner_radius=0.15, width=3.0, height=0.9, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE).move_to([4.4, -2.3, 0])
        pan = Line([3.3, -1.7, 0], [5.5, -1.7, 0], color=th.INK, stroke_width=6)
        val = DecimalNumber(0, num_decimal_places=3, font_size=38, color=th.AMBER).move_to(body).shift(LEFT * 0.25)
        gl = T("g", size=28, color=th.AMBER).next_to(val, RIGHT, buff=0.12)
        with self.say("Multiply by fifty three: one point three two five grams. Weigh exactly that, dissolve it, and make it up to the mark of a two hundred fifty cubic centimetre volumetric flask."):
            self.play(Write(st[2]))
            self.play(FadeIn(body), Create(pan), FadeIn(val), FadeIn(gl))
            self.play(ChangeDecimalToValue(val, 1.325), run_time=1.5)
            self.sfx("click", gain=-8)
        self.play(FadeOut(VGroup(head, prob, st, body, pan, val, gl)))

    def example_13(self):
        head, prob = C.example_head(self, "Concentrated sulphuric acid is 98 % by mass, density 1.84 g cm⁻³. Find its molarity, normality and molality.")
        bottle = VGroup(RoundedRectangle(corner_radius=0.2, width=1.6, height=2.2, fill_color="#2a2f4a", fill_opacity=1, stroke_color=th.INK, stroke_width=2),
                        Rectangle(width=0.6, height=0.4, fill_color="#2a2f4a", fill_opacity=1, stroke_color=th.INK, stroke_width=2))
        bottle[1].next_to(bottle[0], UP, buff=0)
        lbl = VGroup(chem(r"H_2SO_4", size=28), T("98 %", size=20, color=th.AMBER), T("d = 1.84", size=18, color=th.BODY)).arrange(DOWN, buff=0.08).move_to(bottle[0])
        bot = VGroup(bottle, lbl).move_to([-5.2, -1.2, 0])
        with self.say("Worked example one point three, straight from a reagent bottle label. Concentrated sulphuric acid, ninety eight percent by mass, density one point eight four grams per cubic centimetre. Find its molarity, normality and molality."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2), FadeIn(bot))
        bar = Rectangle(width=6.0, height=0.6, stroke_color=th.INK, stroke_width=2).move_to([0.6, 0.3, 0])
        acid = Rectangle(width=6.0 * 0.98, height=0.6, fill_color=th.AMBER, fill_opacity=0.8, stroke_width=0).align_to(bar, LEFT).set_y(0.3)
        wat = Rectangle(width=6.0 * 0.02, height=0.6, fill_color=C.WATER, fill_opacity=0.9, stroke_width=0).align_to(bar, RIGHT).set_y(0.3)
        bl = T("1 litre weighs 1000 × 1.84 = 1840 g", size=26, color=th.INK).next_to(bar, UP, buff=0.2)
        al = T("98 %: 1803.2 g of H₂SO₄", size=24, color=th.AMBER).next_to(bar, DOWN, buff=0.2).align_to(bar, LEFT)
        st = C.steps(r"M = \frac{1803.2}{98} = 18.4\ \mathrm{mol\,L^{-1}} \quad \left(= \frac{10\,p\,d}{M_w}\right)",
                     r"N = M \times n = 18.4 \times 2 = 36.8\ \mathrm{N}", size=36).next_to(al, DOWN, buff=0.4).align_to(bar, LEFT)
        with self.say("Take one litre. It weighs a thousand times one point eight four, one thousand eight hundred and forty grams. Ninety eight percent of that, one thousand eight hundred and three point two grams, is the acid."):
            self.play(FadeIn(bl), Create(bar))
            self.play(GrowFromEdge(acid, LEFT), GrowFromEdge(wat, RIGHT))
            self.play(FadeIn(al))
        with self.say("Divide by ninety eight: eighteen point four moles per litre. That is the shortcut, ten p d over molar mass. And normality is molarity times two: thirty six point eight."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        self.play(FadeOut(VGroup(bl, bar, acid, wat, al, st)))
        pc = np.array([-1.4, -0.4, 0])
        pie_a = Sector(radius=1.4, angle=TAU * 0.98, start_angle=PI / 2 + TAU * 0.02, arc_center=pc, fill_color=th.AMBER, fill_opacity=0.85, stroke_width=0)
        pie_w = Sector(radius=1.4, angle=TAU * 0.02, start_angle=PI / 2, arc_center=pc, fill_color=C.WATER, fill_opacity=1, stroke_width=0)
        pl = VGroup(T("100 g of acid:", size=26, color=th.INK), T("98 g H₂SO₄ = 1 mol", size=26, color=th.AMBER), T("2 g water = 0.002 kg", size=26, color=C.WATER)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 0.6, 0])
        mres = M(r"m = \frac{1\ \mathrm{mol}}{0.002\ \mathrm{kg}} = 500\ \mathrm{mol\,kg^{-1}}", size=44, color=th.MINT).next_to(pl, DOWN, buff=0.5)
        with self.say("For molality, take one hundred grams instead. Ninety eight grams is acid, exactly one mole. Only two grams is water, zero point zero zero two kilogram."):
            self.play(FadeIn(pie_a), FadeIn(pie_w))
            self.play(FadeIn(pl, shift=LEFT * 0.2))
        nb = C.show_neby(self, "surprised", height=1.3)
        with self.say("One mole over zero point zero zero two kilogram: five hundred moles per kilogram! Not a mistake. Concentrated sulphuric acid is nearly pure solute, so there is almost no solvent to divide by."):
            self.play(Write(mres))
            self.play(pie_w.animate.scale(1.6, about_point=pc), rate_func=there_and_back, run_time=1.0)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, bot, pie_a, pie_w, pl, mres)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        d1 = VGroup(T("Primary standard", size=34, color=th.MINT, weight="BOLD"),
                    para("so pure and stable that a standard solution is made simply by weighing it and dissolving it to a known volume", width=5.6, size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        d2 = VGroup(T("Secondary standard", size=34, color=th.CORAL, weight="BOLD"),
                    para("cannot be weighed reliably; its concentration is found by titrating it against a primary standard", width=5.6, size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(d1, d2).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.3)
        with self.say("A titration is only as good as the solution you claim to know. A primary standard is so pure and stable that you can make a standard solution just by weighing it accurately and dissolving it to a known volume. A secondary standard cannot be trusted on the balance. Its concentration must be found by titrating it against a primary standard."):
            self.play(FadeIn(d1, shift=RIGHT * 0.2))
            self.play(FadeIn(d2, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(d1, d2)))
        title = T("A primary standard must be", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        crit = ["very pure: 99.9 % or better",
                "stable in air: not hygroscopic, not efflorescent, no CO₂ uptake",
                "readily soluble, with a stable solution",
                "of high equivalent weight",
                "quick, complete and stoichiometric in reaction"]
        rows = VGroup()
        for i, c in enumerate(crit):
            box = Square(side_length=0.36, stroke_color=th.MINT, stroke_width=3)
            rows.add(VGroup(box, T(c, size=28, color=th.INK)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(title, DOWN, buff=0.5)
        with self.say("A primary standard must tick five boxes. Very pure, ninety nine point nine percent or better. Stable in air, so it neither absorbs moisture, nor loses its water of crystallisation, nor picks up carbon dioxide. Readily soluble, with a solution that keeps. A high equivalent weight. And a reaction that is fast, complete and stoichiometric.") as v:
            self.play(FadeIn(title))
            for r in rows:
                b = r[0]
                ck = VGroup(Line(b.get_center() + [-0.11, 0.0, 0], b.get_center() + [-0.03, -0.1, 0], color=th.MINT, stroke_width=5),
                            Line(b.get_center() + [-0.03, -0.1, 0], b.get_center() + [0.13, 0.12, 0], color=th.MINT, stroke_width=5))
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.4)
                self.sfx("tick", gain=-12)
                self.play(Create(ck), run_time=0.3)
                r.add(ck)
                self.hold(v.dur / 5 - 0.7)
        self.play(FadeOut(VGroup(title, rows)))
        self.naoh_drift()
        self.high_E()
        self.sorting()
        self.quiz("Which of these is a primary standard substance?",
                  ["NaOH", "HCl", "K₂Cr₂O₇", "KMnO₄"], 2,
                  "Which of these four can be weighed straight into a standard solution? Pause and think.",
                  "C, potassium dichromate. It is pure, not hygroscopic, stable, and has a high equivalent weight. Sodium hydroxide absorbs water and carbon dioxide, hydrochloric acid fumes, and permanganate contains manganese dioxide and slowly decomposes.")

    def naoh_drift(self):
        body = RoundedRectangle(corner_radius=0.15, width=3.4, height=1.0, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE).move_to([-3.0, -2.0, 0])
        pan = Line([-4.3, -1.3, 0], [-1.7, -1.3, 0], color=th.INK, stroke_width=6)
        pellets = VGroup(*[Ellipse(width=0.42, height=0.22, fill_color="#F2F4FA", fill_opacity=1, stroke_width=0).move_to([-3.6 + 0.45 * k, -1.15, 0]) for k in range(4)])
        val = DecimalNumber(4.000, num_decimal_places=3, font_size=40, color=th.CORAL).move_to(body).shift(LEFT * 0.3)
        gl = T("g", size=30, color=th.CORAL).next_to(val, RIGHT, buff=0.15)
        nl = chem("NaOH", size=40).next_to(pan, UP, buff=0.7)
        rng = np.random.default_rng(9)
        mols = VGroup()
        for k in range(10):
            if k % 2 == 0:
                o = C.atom("O", r=0.14).move_to([2.0 + rng.uniform(0, 3.5), rng.uniform(-1.5, 2.2), 0])
                h1 = C.atom("H", r=0.09).move_to(o.get_center() + [-0.15, -0.12, 0])
                h2 = C.atom("H", r=0.09).move_to(o.get_center() + [0.15, -0.12, 0])
                mols.add(VGroup(o, h1, h2))
            else:
                c = C.atom("C", r=0.13).move_to([2.0 + rng.uniform(0, 3.5), rng.uniform(-1.5, 2.2), 0])
                mols.add(VGroup(c, C.atom("O", r=0.11).move_to(c.get_center() + LEFT * 0.22), C.atom("O", r=0.11).move_to(c.get_center() + RIGHT * 0.22)))
        leg = VGroup(T("water vapour", size=22, color=C.EL["O"]), T("carbon dioxide", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 2.6, 0])
        with self.say("Why can sodium hydroxide never be a primary standard? Put four grams of pellets on the balance and watch the reading."):
            self.play(FadeIn(body), Create(pan), FadeIn(pellets), FadeIn(val), FadeIn(gl), FadeIn(nl))
            self.play(FadeIn(mols), FadeIn(leg))
        with self.say("It keeps creeping up. The pellets pull water vapour out of the air, they are deliquescent, and they react with carbon dioxide to form sodium carbonate. What you weigh is not pure sodium hydroxide."):
            self.play(*[m.animate.move_to(pellets[k % 4].get_center() + UP * 0.05).scale(0.3).set_opacity(0) for k, m in enumerate(mols)],
                      ChangeDecimalToValue(val, 4.087), pellets.animate.set_fill("#DCE6F0"), run_time=3.5, rate_func=smooth)
        nb = C.show_neby(self, "oops", height=1.4)
        others = para("Concentrated HCl fumes, so its strength drifts. KMnO₄ always contains some MnO₂ and is slowly reduced by organic matter, so it is standardised freshly against oxalic acid.", width=6.0, size=24, color=th.BODY).move_to([3.2, -0.4, 0])
        self.play(FadeOut(mols), FadeOut(leg))
        with self.say("The others fail too. Concentrated hydrochloric acid gives off fumes, so its strength drifts. Potassium permanganate always contains a little manganese dioxide and is slowly reduced by traces of organic matter, so we standardise it freshly against oxalic acid."):
            self.play(FadeIn(others, shift=LEFT * 0.2))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(body, pan, pellets, val, gl, nl, others)))

    def high_E(self):
        title = T("Why a high equivalent weight?", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        sub = T("to make 250 cm³ of 0.1 N, weigh:", size=26, color=th.MUTED).next_to(title, DOWN, buff=0.3)
        y1, y2 = 0.4, -1.4
        x0 = -5.6
        b1 = Rectangle(width=1.575 * 1.1, height=0.6, fill_color=th.SKY, fill_opacity=0.8, stroke_width=0).move_to([x0, y1, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=9.8 * 1.1, height=0.6, fill_color=th.MINT, fill_opacity=0.8, stroke_width=0).move_to([x0, y2, 0], aligned_edge=LEFT)
        e1 = Rectangle(width=0.06, height=0.8, fill_color=th.CORAL, fill_opacity=1, stroke_width=0).next_to(b1, RIGHT, buff=0)
        e2 = Rectangle(width=0.06, height=0.8, fill_color=th.CORAL, fill_opacity=1, stroke_width=0).next_to(b2, RIGHT, buff=0)
        l1 = T("oxalic acid, E = 63:  1.575 g", size=24, color=th.SKY).next_to(b1, UP, buff=0.15).align_to(b1, LEFT)
        l2 = T("Mohr's salt, E = 392:  9.8 g", size=24, color=th.MINT).next_to(b2, UP, buff=0.15).align_to(b2, LEFT)
        r1 = T("0.1 mg error = 0.0063 %", size=22, color=th.CORAL).next_to(e1, RIGHT, buff=0.2)
        r2 = T("0.1 mg error = 0.0010 %", size=22, color=th.CORAL).next_to(b2, DOWN, buff=0.15).align_to(b2, RIGHT)
        with self.say("And why a high equivalent weight? To make the same solution, a substance with a bigger equivalent weight must be weighed out in a bigger mass. Two hundred fifty cubic centimetres of decinormal oxalic acid needs one point five seven five grams. The same with Mohr's salt needs nine point eight grams."):
            self.play(FadeIn(title), FadeIn(sub))
            self.play(GrowFromEdge(b1, LEFT), FadeIn(l1))
            self.play(GrowFromEdge(b2, LEFT), FadeIn(l2))
        with self.say("The balance makes the same tiny error, say a tenth of a milligram, either way. On the bigger mass it is a much smaller fraction. A higher equivalent weight means a smaller relative weighing error."):
            self.play(FadeIn(e1), FadeIn(e2))
            self.play(FadeIn(r1), FadeIn(r2))
        self.play(FadeOut(VGroup(title, sub, b1, b2, e1, e2, l1, l2, r1, r2)))

    def sorting(self):
        h1 = T("Primary", size=34, color=th.MINT, weight="BOLD").move_to([-3.4, 2.5, 0])
        h2 = T("Secondary", size=34, color=th.CORAL, weight="BOLD").move_to([3.4, 2.5, 0])
        line = DashedLine([0, 2.8, 0], [0, -3.0, 0], color=th.FAINT)
        items = [("H_2C_2O_4\\cdot 2H_2O", 0), ("HCl", 1), ("Na_2CO_3", 0), ("NaOH", 1), ("K_2Cr_2O_7", 0), ("KMnO_4", 1),
                 ("KH\\ phthalate", 0), ("Na_2S_2O_3\\cdot 5H_2O", 1), ("AgNO_3,\\ NaCl", 0), ("I_2\\ solution", 1)]
        chips = VGroup()
        for tex, side in items:
            m = chem(tex, size=32, color=th.MINT if side == 0 else th.CORAL)
            box = SurroundingRectangle(m, color=th.PANEL_EDGE, buff=0.12, corner_radius=0.1, fill_color=th.PANEL, fill_opacity=0.9)
            chips.add(VGroup(box, m))
        cnt = [0, 0]
        with self.say("Now sort the usual suspects. Oxalic acid, anhydrous sodium carbonate, potassium dichromate, potassium hydrogen phthalate, silver nitrate and sodium chloride are primary standards. Hydrochloric acid, sodium hydroxide, potassium permanganate, sodium thiosulphate and iodine solution are secondary.") as v:
            self.play(FadeIn(h1), FadeIn(h2), Create(line))
            for ch, (tex, side) in zip(chips, items):
                ch.move_to([0, 3.2, 0])
                tgt = np.array([-3.4 if side == 0 else 3.4, 1.6 - 0.95 * cnt[side], 0])
                cnt[side] += 1
                self.play(FadeIn(ch, shift=DOWN * 0.3), run_time=0.25)
                self.play(ch.animate.move_to(tgt), run_time=0.45, rate_func=rate_functions.ease_out_cubic)
                self.sfx("pop_low", gain=-16)
                self.hold(v.dur / 10 - 0.75)
        self.play(FadeOut(VGroup(h1, h2, line, chips)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        law = self.callout("key", "Law of equivalence: substances always react in the ratio of their equivalents. One gram equivalent of an acid neutralises exactly one gram equivalent of a base, whatever the mole ratio.", width=11.5, size=27)
        law.to_edge(UP, buff=0.8)
        with self.say("Here is the law the whole unit rests on. Substances always react in the ratio of their equivalents. One gram equivalent of an acid exactly neutralises one gram equivalent of a base. One equivalent of an oxidising agent exactly oxidises one equivalent of a reducing agent. Whatever the mole ratio in the balanced equation."):
            self.play(FadeIn(law, shift=DOWN * 0.2))
        eq = chem(r"H_2SO_4 + 2NaOH \rightarrow Na_2SO_4 + 2H_2O", size=40).next_to(law, DOWN, buff=0.4)
        mol_l = T("1 mol", size=26, color=th.CORAL).move_to([-3.4, -1.0, 0])
        mol_r = T("2 mol", size=26, color=th.SKY).move_to([3.4, -1.0, 0])
        acid = VGroup(*[Circle(radius=0.32, fill_color=th.CORAL, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2) for _ in range(2)]).arrange(RIGHT, buff=0.25).move_to([-3.4, -1.8, 0])
        base = VGroup(*[Circle(radius=0.32, fill_color=th.SKY, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2) for _ in range(2)]).arrange(RIGHT, buff=0.25).move_to([3.4, -1.8, 0])
        for g, t in ((acid, "H⁺"), (base, "OH⁻")):
            for c in g:
                c.add(T(t, size=18, color=th.BG, weight="BOLD").move_to(c))
        el = T("2 equivalents", size=26, color=th.CORAL).next_to(acid, DOWN, buff=0.3)
        er = T("2 equivalents", size=26, color=th.SKY).next_to(base, DOWN, buff=0.3)
        with self.say("Look at sulphuric acid and sodium hydroxide. One mole of acid needs two moles of base, so the moles do not match. But one mole of sulphuric acid carries two equivalents, and two moles of sodium hydroxide carry two equivalents. The equivalents match exactly."):
            self.play(Write(eq))
            self.play(FadeIn(mol_l), FadeIn(mol_r))
            self.play(FadeIn(acid, scale=0.5), FadeIn(base, scale=0.5))
            self.play(FadeIn(el), FadeIn(er))
        with self.say("They pair off one to one, and nothing is left over."):
            for a, b in zip(acid, base):
                self.play(a.animate.move_to([-0.4, -1.8, 0]), b.animate.move_to([0.4, -1.8, 0]), run_time=0.6)
                self.sfx("pop")
                w = T("H₂O", size=26, color=C.WATER, weight="BOLD").move_to([0, -1.8, 0])
                self.play(FadeOut(VGroup(a, b), scale=0.3), FadeIn(w, scale=1.5), run_time=0.4)
                self.play(w.animate.shift(DOWN * 0.8 + (LEFT if a is acid[0] else RIGHT) * 0.6).set_opacity(0.6), run_time=0.3)
                acid.add(w)
        self.play(FadeOut(VGroup(law, eq, mol_l, mol_r, acid, base, el, er)))
        title = T("The normality equation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        d = VGroup(
            M(r"N = \frac{\text{equivalents}}{\text{litres}} \;\Rightarrow\; \text{milliequivalents} = N \times V_{\mathrm{cm^3}}", size=38),
            M(r"\text{at the end point: } \text{meq}_1 = \text{meq}_2", size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.5)
        big = M(r"N_1", r"V_1", r"=", r"N_2", r"V_2", size=96).next_to(d, DOWN, buff=0.6)
        big[0].set_color(th.CORAL)
        big[3].set_color(th.SKY)
        with self.say("Now turn the law into an equation. Normality is equivalents per litre, so in V cubic centimetres of a solution of normality N, there are N times V milliequivalents. At the end point, the milliequivalents of the two reactants are equal."):
            self.play(FadeIn(title), Write(d[0]))
            self.play(Write(d[1]))
        with self.say("And so: N one V one equals N two V two. The normality equation. It needs no balanced equation and no coefficients. That is its whole power."):
            self.sfx("impact", gain=-10)
            self.play(Write(big))
            self.play(Circumscribe(big, color=th.AMBER))
        self.play(FadeOut(d), big.animate.scale(0.6).next_to(title, DOWN, buff=0.4))
        more = VGroup(
            VGroup(M(r"n_1 M_1 V_1 = n_2 M_2 V_2", size=50, color=th.AMBER), T("in molarities, using N = M × n", size=24, color=th.MUTED)),
            VGroup(M(r"M_1 V_1 = M_2 V_2", size=50, color=th.MINT), T("dilution: same solute, before and after adding water", size=24, color=th.MUTED)),
        )
        for m in more:
            m.arrange(DOWN, buff=0.2)
        more.arrange(DOWN, buff=0.6).next_to(big, DOWN, buff=0.6)
        with self.say("Write N as M times n for each solution, and you get the molarity form: n one M one V one equals n two M two V two. And for diluting the same solute with water, the n factors cancel: M one V one equals M two V two."):
            self.play(FadeIn(more[0], shift=UP * 0.2))
            self.play(FadeIn(more[1], shift=UP * 0.2))
        self.play(FadeOut(VGroup(title, big, more)))
        self.example_14()
        self.tip("N₁V₁ = N₂V₂ only in normalities. With molarities you must write n₁M₁V₁ = n₂M₂V₂. Mixing the two is the commonest error in this unit.",
                 "Here is the single commonest error in this unit. N one V one equals N two V two works only with normalities. If you put molarities into it, you will be wrong whenever the n factors differ. With molarities, always carry the n factors: n one M one V one equals n two M two V two.", state="oops")

    def example_14(self):
        head, prob = C.example_head(self, "Commercial hydrochloric acid is 11.6 N. What volume of it is needed to prepare 500 cm³ of 0.1 N HCl?")
        st = C.steps(r"N_1V_1 = N_2V_2 \;\Rightarrow\; 11.6 \times V_1 = 0.1 \times 500",
                     r"V_1 = \frac{50}{11.6} = 4.31\ \mathrm{cm^3}", size=42).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[1].set_color(th.AMBER)
        with self.say("Worked example one point four. Commercial hydrochloric acid is eleven point six normal. What volume of it do we need to make five hundred cubic centimetres of decinormal acid?"):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("Equivalents do not change when you add water, so N one V one equals N two V two. Eleven point six times V one equals zero point one times five hundred, which is fifty. V one is fifty over eleven point six, four point three one cubic centimetres."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        bk = C.Beaker(center=[3.2, -1.9, 0], w=1.8, h=1.7, level=0.45, color=C.WATER, opacity=0.3)
        tube = VGroup(Rectangle(width=0.36, height=1.4, stroke_color=th.INK, stroke_width=2),
                      Rectangle(width=0.32, height=0.4, fill_color=th.AMBER, fill_opacity=0.8, stroke_width=0)).move_to([-2.0, -1.6, 0])
        tube[1].align_to(tube[0], DOWN)
        tl = T("4.31 cm³ acid", size=22, color=th.AMBER).next_to(tube, LEFT, buff=0.2)
        bl = T("~200 cm³ water", size=22, color=C.WATER).next_to(bk.g, RIGHT, buff=0.2)
        with self.say("And the practical rule: always add the acid to about two hundred cubic centimetres of water, never water to acid, then make it up to five hundred."):
            self.play(FadeIn(bk.g), FadeIn(tube), FadeIn(tl), FadeIn(bl))
            self.play(tube.animate.move_to(bk.c + UP * 1.6 + LEFT * 0.3).rotate(-0.9), tl.animate.next_to(bk.c + UP * 1.6 + LEFT * 0.3, LEFT, buff=0.6), run_time=1.0)
            drops = VGroup(*[Dot(bk.c + UP * (1.0 - 0.35 * k) + LEFT * 0.0, radius=0.05, color=th.AMBER) for k in range(4)])
            self.play(LaggedStart(*[d.animate.move_to(bk.c + DOWN * 0.3).set_opacity(0) for d in drops], lag_ratio=0.2), run_time=1.0)
            self.play(bk.liq.animate.set_fill(interpolate_color(ManimColor(C.WATER), ManimColor(th.AMBER), 0.15)))
        nb = C.show_neby(self, "oops", height=1.3, corner=DL)
        with self.say("Water poured into concentrated acid can boil on the spot and spit acid out of the vessel."):
            self.wait(0.4)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st, bk.g, tube, tl, bl, drops)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        bur = C.Burette(x=-3.8, top=3.0, bottom=0.0, color=th.SKY)
        fl = C.Flask(center=[-3.8, -2.2, 0], scale=1.0, color=th.MUTED, opacity=0.35)
        pip = VGroup(Rectangle(width=0.1, height=1.5, stroke_color=th.INK, stroke_width=2).move_to([-0.9, 1.8, 0]),
                     Ellipse(width=0.55, height=1.3, fill_color=th.AMBER, fill_opacity=0.25, stroke_color=th.INK, stroke_width=2).move_to([-0.9, 0.45, 0]),
                     Polygon([-0.95, -0.2, 0], [-0.85, -0.2, 0], [-0.88, -1.0, 0], [-0.92, -1.0, 0], stroke_color=th.INK, stroke_width=2, fill_opacity=0))
        defn = para("Titration: adding a standard solution from a burette to a measured volume of the unknown, just until the reaction is exactly complete.", width=6.2, size=26, color=th.INK).move_to([3.4, 2.2, 0])
        with self.say("Now we put it all together. Titration is adding a standard solution from a burette to a measured volume of the unknown, just until the reaction is exactly complete."):
            self.add(bur.liquid)
            self.play(Create(bur.glass), FadeIn(bur.liquid), FadeIn(fl.g))
            self.play(FadeIn(defn))
        vocab = [("titrant", "the standard solution, in the burette", bur.glass.get_right() + DOWN * 0.3),
                 ("analyte (titrate)", "the unknown, in the flask", fl.g.get_right()),
                 ("aliquot", "the measured portion delivered by the pipette", pip.get_right())]
        labs = VGroup()
        with self.say("Learn the vocabulary, because it is examined on its own. The titrant is the standard solution in the burette. The analyte, or titrate, is the unknown in the flask. And an aliquot is the measured portion of the unknown that the pipette delivers."):
            self.play(FadeIn(pip))
            for i, (a, b, p) in enumerate(vocab):
                t = VGroup(T(a, size=26, color=th.AMBER, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
                t.move_to([3.4, 0.9 - 1.0 * i, 0])
                ar = Arrow(t.get_left() + LEFT * 0.1, p + RIGHT * 0.1, buff=0.05, color=th.FAINT, stroke_width=3)
                self.play(FadeIn(t, shift=LEFT * 0.2), GrowArrow(ar), run_time=0.7)
                labs.add(t, ar)
        self.play(FadeOut(labs), FadeOut(defn), FadeOut(pip))
        ep = VGroup(
            VGroup(T("equivalence point", size=28, color=th.MINT, weight="BOLD"), T("chemically equivalent amounts have reacted", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(T("end point", size=28, color=th.CORAL, weight="BOLD"), T("the indicator changes colour: what we see", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(T("titration error", size=28, color=th.AMBER, weight="BOLD"), T("the small gap between the two", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.6, 0.6, 0])
        with self.say("Two points that students mix up. The equivalence point is where chemically equivalent amounts have reacted, a fact of chemistry. The end point is where the indicator changes colour, what we actually see. A good indicator puts them within a drop of each other. The small gap is the titration error."):
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in ep], lag_ratio=0.5), run_time=2.5)
            titrate(self, bur, fl, 15, drops=5, run_time=0.35)
        self.play(FadeOut(VGroup(bur.glass, fl.g, ep)), FadeOut(bur.liquid))
        self.remove(bur.liquid)
        self.parallax()
        self.concordant()
        self.types()
        self.acid_base_curve()
        self.carbonate_curve()
        self.example_15()
        self.redox()
        self.example_16()
        self.example_17()
        self.quiz("In the titration of oxalic acid against KMnO₄, the indicator used is",
                  ["phenolphthalein", "methyl orange", "starch", "none: KMnO₄ itself"], 3,
                  "Last question. In the permanganate and oxalic acid titration, which indicator do you add? Pause and think.",
                  "D, none. Permanganate is self indicating. Its purple colour vanishes as long as any oxalic acid remains, and the first permanent pale pink is the end point. Starch is for iodine titrations.")

    def parallax(self):
        title = T("Reading a burette", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        x0, w = -3.4, 1.4
        top, bot = 2.4, -2.6
        tube = Rectangle(width=w, height=top - bot, stroke_color=th.INK, stroke_width=3).move_to([x0, (top + bot) / 2, 0])

        def yv(v):
            return 1.9 - (v - 20.0) * 4.0
        ticks = VGroup()
        for k in range(11):
            v = 20.0 + 0.1 * k
            L = 0.6 if k % 5 == 0 else 0.3
            ticks.add(Line([x0 - w / 2, yv(v), 0], [x0 - w / 2 + L, yv(v), 0], color=th.INK if k % 5 == 0 else th.MUTED, stroke_width=2.5 if k % 5 == 0 else 1.5))
            if k % 5 == 0:
                ticks.add(T(f"{v:.1f}", size=22, color=th.INK).next_to([x0 - w / 2, yv(v), 0], LEFT, buff=0.12))
        ym = yv(20.5)
        men = ParametricFunction(lambda t: np.array([x0 + t * (w / 2 - 0.03), ym + 0.25 * t * t, 0]), t_range=[-1, 1], color=th.SKY, stroke_width=4)
        liq = Polygon(*[np.array([x0 + t * (w / 2 - 0.03), ym + 0.25 * t * t, 0]) for t in np.linspace(-1, 1, 30)],
                      [x0 + w / 2 - 0.03, bot + 0.02, 0], [x0 - w / 2 + 0.03, bot + 0.02, 0], fill_color=th.SKY, fill_opacity=0.25, stroke_width=0)
        eye_y = ValueTracker(ym)

        def eye():
            y = eye_y.get_value()
            e = VGroup(Ellipse(width=0.9, height=0.45, fill_color=WHITE, fill_opacity=1, stroke_color=th.INK, stroke_width=2),
                       Circle(radius=0.13, fill_color="#3a2a1a", fill_opacity=1, stroke_width=0).shift(LEFT * 0.15))
            return e.move_to([3.4, y, 0])

        def sight():
            y = eye_y.get_value()
            p_eye = np.array([2.9, y, 0])
            p_m = np.array([x0, ym, 0])
            d = p_m - p_eye
            p_far = p_m + d / np.linalg.norm(d) * 0.9
            return DashedLine(p_eye, p_far, color=th.AMBER, stroke_width=3)
        ey = always_redraw(eye)
        sl = always_redraw(sight)
        rd = DecimalNumber(20.5, num_decimal_places=2, font_size=44, color=th.AMBER)
        rd.add_updater(lambda m: m.set_value(20.5 - 0.06 * (eye_y.get_value() - ym)).move_to([3.4, -2.5, 0]))
        rl = T("you read", size=24, color=th.MUTED).next_to([3.4, -2.5, 0], UP, buff=0.4)
        with self.say("Reading the burette is a skill in itself. The liquid surface curves into a meniscus, and for a clear solution you always read the bottom of the curve. Here, twenty point five zero cubic centimetres."):
            self.play(FadeIn(title), Create(tube), FadeIn(ticks), FadeIn(liq), Create(men))
            self.add(ey, sl, rd)
            self.play(FadeIn(ey), FadeIn(sl), FadeIn(rd), FadeIn(rl))
        with self.say("But your eye must be level with it. Raise your eye, and you read too low. Lower it, and you read too high. That is parallax error, worth a few tenths of a cubic centimetre."):
            self.play(eye_y.animate.set_value(ym + 2.0), run_time=1.5)
            self.play(eye_y.animate.set_value(ym - 2.0), run_time=2.0)
            self.play(eye_y.animate.set_value(ym), run_time=1.2)
            self.sfx("correct", gain=-14)
        rd.clear_updaters()
        self.play(FadeOut(VGroup(title, tube, ticks, liq, men, rd, rl)), FadeOut(ey), FadeOut(sl))
        self.remove(ey, sl)

    def concordant(self):
        title = T("Concordant readings", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Titration", "Initial (cm³)", "Final (cm³)", "Volume used (cm³)"],
                ["rough", "0.00", "23.10", "23.10"],
                ["1", "0.00", "22.60", "22.60"],
                ["2", "0.50", "23.00", "22.50"],
                ["3", "1.00", "23.50", "22.50"]]
        tb = C.table(rows, [2.2, 2.8, 2.8, 3.4], row_h=0.62, size=24).next_to(title, DOWN, buff=0.45)
        with self.say("A titration is repeated until the results agree. The first one is a rough run, done quickly to find the neighbourhood, and it is discarded. Then careful runs, until two or more agree within zero point one cubic centimetre. Those are concordant readings, and their mean goes into the calculation.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        cross = Line(tb[1].get_left(), tb[1].get_right(), color=th.CORAL, stroke_width=4)
        hl = SurroundingRectangle(VGroup(tb[3], tb[4]), color=th.MINT, buff=0.04, corner_radius=0.08)
        mean = M(r"\text{mean of concordant readings} = 22.50\ \mathrm{cm^3}", size=40, color=th.MINT).next_to(tb, DOWN, buff=0.5)
        with self.say("Cross out the rough value. Twenty two point six and twenty two point five differ by exactly zero point one, which is just at the limit, but the two twenty two point fives agree perfectly. Use twenty two point five zero. Remember that number."):
            self.play(Create(cross))
            self.play(Create(hl))
            self.play(Write(mean))
        self.play(FadeOut(VGroup(title, tb, cross, hl, mean)))

    def types(self):
        title = T("Types of titration", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Type", "Reaction used", "Example", "Indicator"],
                ["Acid-base", "H⁺ + OH⁻ → H₂O", "NaOH vs HCl", "phenolphthalein, methyl orange"],
                ["Redox", "electron transfer", "KMnO₄ vs FeSO₄", "self-indicating"],
                ["Precipitation", "insoluble salt forms", "AgNO₃ vs NaCl", "K₂CrO₄ (Mohr)"],
                ["Complexometric", "a complex ion forms", "EDTA vs Ca²⁺, Mg²⁺", "Eriochrome black T"],
                ["Iodometric", "I₂ ⇌ 2I⁻", "Na₂S₂O₃ vs I₂", "starch"]]
        tb = C.table(rows, [2.6, 3.0, 3.0, 4.2], row_h=0.66, size=23, colors=[th.AMBER, th.INK, th.BODY, th.MINT]).next_to(title, DOWN, buff=0.45)
        with self.say("Titrations are named after the reaction they use. Acid base titrations use neutralisation. Redox titrations use electron transfer. Precipitation titrations, like silver nitrate against chloride, form an insoluble salt. Complexometric titrations use E D T A. And iodometric titrations use iodine and thiosulphate, with starch as the indicator. Our syllabus focuses on the first two.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
            self.play(Indicate(VGroup(tb[1], tb[2]), color=th.AMBER, scale_factor=1.02))
        self.play(FadeOut(VGroup(title, tb)))

    def acid_base_curve(self):
        bur = C.Burette(x=-5.6, top=3.0, bottom=0.0, color=th.SKY, labels=False)
        fl = C.Flask(center=[-5.6, -2.2, 0], scale=0.95, color="#DDE3F5", opacity=0.55)
        ax = Axes(x_range=[0, 50, 10], y_range=[0, 14, 2], x_length=8.0, y_length=5.2, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([1.6, -0.1, 0])
        xl = T("NaOH added (cm³)", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = T("pH", size=24, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.15)
        full = ax.plot(lambda v: C.ph_strong(v), x_range=[0, 50, 0.05], color=th.AMBER, stroke_width=4, use_smoothing=False)
        traced = full.copy()
        traced.add_updater(lambda m: m.pointwise_become_partial(full, 0, max(1e-3, bur.vol.get_value() / 50)))
        dot = always_redraw(lambda: Dot(ax.c2p(bur.vol.get_value(), C.ph_strong(bur.vol.get_value())), radius=0.08, color=WHITE))
        fl.liq.add_updater(lambda m: m.set_fill(C.phenolphthalein(C.ph_strong(bur.vol.get_value()))))
        cap = T("25 cm³ of 0.1 M HCl  +  phenolphthalein", size=22, color=th.BODY).next_to(ax, UP, buff=0.25)
        with self.say("Let us watch an acid base titration as a graph. Twenty five cubic centimetres of decimolar hydrochloric acid, with phenolphthalein, and decimolar sodium hydroxide in the burette. We plot the pH of the flask against the volume added."):
            self.add(bur.liquid)
            self.play(Create(bur.glass), FadeIn(bur.liquid), FadeIn(fl.g))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(cap))
            self.add(traced, dot)
        with self.say("At first the pH barely moves. Twenty cubic centimetres in, and it is still strongly acidic."):
            self.play(bur.vol.animate.set_value(22), run_time=4, rate_func=linear)
        with self.say("Then, near twenty five, one or two drops send the pH leaping from about four to about ten. The flask flushes pink. That vertical jump is the equivalence point."):
            self.play(bur.vol.animate.set_value(24.8), run_time=2.5, rate_func=linear)
            self.play(bur.vol.animate.set_value(25.2), run_time=2.0, rate_func=linear)
            self.sfx("impact", gain=-12)
            self.play(Flash(ax.c2p(25, 7), color=th.AMBER, flash_radius=0.5))
            self.play(bur.vol.animate.set_value(40), run_time=2.0, rate_func=linear)
        b1 = Rectangle(width=8.0, height=ax.c2p(0, 4.4)[1] - ax.c2p(0, 3.1)[1], fill_color=C.MO_RED, fill_opacity=0.18, stroke_width=0).move_to(ax.c2p(25, 3.75))
        b2 = Rectangle(width=8.0, height=ax.c2p(0, 10)[1] - ax.c2p(0, 8.3)[1], fill_color=C.PINK_END, fill_opacity=0.18, stroke_width=0).move_to(ax.c2p(25, 9.15))
        t1 = T("methyl orange 3.1–4.4", size=20, color=C.MO_RED).move_to(ax.c2p(40, 3.75))
        t2 = T("phenolphthalein 8.3–10", size=20, color=C.PINK_END).move_to(ax.c2p(40, 9.15))
        with self.say("Every indicator changes colour over its own pH range. Methyl orange, three point one to four point four. Phenolphthalein, eight point three to ten. For a strong acid and a strong base, the jump covers both ranges, so either indicator works."):
            self.play(FadeIn(b1), FadeIn(t1))
            self.play(FadeIn(b2), FadeIn(t2))
        weak = ax.plot(lambda v: C.ph_weak_acid(v), x_range=[0, 50, 0.1], color=th.SKY, stroke_width=4, use_smoothing=False)
        wl = T("weak acid (acetic)", size=20, color=th.SKY).move_to(ax.c2p(10, 6.6))
        with self.say("Now replace hydrochloric acid with a weak acid, like acetic acid. The curve starts higher, and the jump begins above pH seven. Methyl orange would change far too early. Phenolphthalein still sits inside the jump."):
            self.play(Create(weak), FadeIn(wl), run_time=2.0)
            self.play(Indicate(b2, color=C.PINK_END, scale_factor=1.0))
        rows = [["Acid vs base", "pH at equivalence", "Indicator"],
                ["strong vs strong", "7", "either"],
                ["weak acid vs strong base", "> 7", "phenolphthalein"],
                ["strong acid vs weak base", "< 7", "methyl orange"],
                ["weak vs weak", "≈ 7, no sharp jump", "none reliable"]]
        traced.clear_updaters()
        fl.liq.clear_updaters()
        self.play(FadeOut(VGroup(bur.glass, fl.g, ax, xl, yl, cap, b1, b2, t1, t2, weak, wl, full, traced)), FadeOut(bur.liquid), FadeOut(dot))
        self.remove(bur.liquid, dot, traced)
        tb = C.table(rows, [4.4, 3.8, 3.6], row_h=0.66, size=24, colors=[th.INK, th.AMBER, th.MINT]).move_to(UP * 0.4)
        with self.say("The rule of thumb, which you will prove properly in Unit 2. Strong with strong, either indicator. Weak acid with strong base, phenolphthalein. Strong acid with weak base, methyl orange. Weak with weak, there is no sharp jump, so no indicator is reliable.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(tb))

    def carbonate_curve(self):
        ax = Axes(x_range=[0, 40, 10], y_range=[2, 12, 2], x_length=8.4, y_length=4.8, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 22}).move_to([0.4, -0.4, 0])
        xl = T("0.1 M HCl added (cm³)", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = T("pH", size=24, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.15)
        cap = T("25 cm³ of 0.05 M Na₂CO₃", size=22, color=th.BODY).move_to(ax.c2p(30, 11))
        xs = np.arange(0, 40.01, 0.1)
        ys = [C.ph_carbonate(x) for x in xs]
        curve = VMobject(color=th.AMBER, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
        e1 = chem(r"Na_2CO_3 + HCl \rightarrow NaHCO_3 + NaCl", size=30, color=C.PINK_END).to_edge(UP, buff=0.75).shift(RIGHT * 0.5)
        e2 = chem(r"NaHCO_3 + HCl \rightarrow NaCl + H_2O + CO_2", size=30, color=C.MO_YEL).next_to(e1, DOWN, buff=0.15)
        p1 = Dot(ax.c2p(12.5, C.ph_carbonate(12.5)), color=C.PINK_END, radius=0.1)
        p2 = Dot(ax.c2p(25, C.ph_carbonate(25)), color=C.MO_YEL, radius=0.1)
        l1 = T("phenolphthalein end point: 12.5 cm³", size=20, color=C.PINK_END).next_to(p1, RIGHT, buff=0.2)
        l2 = T("methyl orange end point: 25.0 cm³", size=20, color=C.MO_YEL).next_to(p2, RIGHT, buff=0.2)
        self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(cap))
        with self.say("Sodium carbonate is a special case worth knowing. It is neutralised in two stages, so its curve has two steps. First, carbonate takes one proton and becomes bicarbonate, near pH eight point three. Phenolphthalein turns colourless here."):
            self.play(Create(curve), run_time=3.0, rate_func=linear)
            self.play(Write(e1), FadeIn(p1, scale=2), FadeIn(l1))
        with self.say("Then bicarbonate takes a second proton and releases carbon dioxide, near pH four. That is where methyl orange changes. So phenolphthalein measures half the carbonate, and methyl orange measures all of it. That is the double indicator method."):
            self.play(Write(e2), FadeIn(p2, scale=2), FadeIn(l2))
        self.play(FadeOut(VGroup(ax, xl, yl, cap, curve, e1, e2, p1, p2, l1, l2)))

    def example_15(self):
        nb = C.show_neby(self, "hop", height=1.4)
        head, prob = C.example_head(self, "25.0 cm³ of a sodium carbonate solution needed 22.5 cm³ of 0.1 N HCl, with methyl orange. Find the normality and strength of the Na₂CO₃ solution, and the mass of Na₂CO₃ in 250 cm³ of it.")
        with self.say("And now, the cold open. Worked example one point five. Twenty five cubic centimetres of the washing soda solution needed twenty two point five cubic centimetres of decinormal hydrochloric acid, with methyl orange. Find the normality and strength of the solution, and the mass of sodium carbonate in two hundred and fifty cubic centimetres of it."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        C.hide_neby(self, nb)
        st = C.steps(r"N_2 = \frac{N_1V_1}{V_2} = \frac{0.1 \times 22.5}{25.0} = 0.09\ \mathrm{N}",
                     r"S = N \times E = 0.09 \times 53 = 4.77\ \mathrm{g\,L^{-1}}",
                     r"\text{in } 250\ \mathrm{cm^3}:\ 4.77 \times 0.250 = 1.19\ \mathrm{g}", size=42).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Line one, the normality equation. N two equals zero point one times twenty two point five, over twenty five. Zero point zero nine normal."):
            self.play(Write(st[0]))
        with self.say("Line two. Methyl orange means all the carbonate reacted, so its n factor is two and E is fifty three. Strength is zero point zero nine times fifty three, four point seven seven grams per litre."):
            self.play(Write(st[1]))
        with self.say("Line three. Two hundred and fifty cubic centimetres is a quarter of a litre: one point one nine grams. Three lines, just as promised."):
            self.play(Write(st[2]))
            self.sfx("correct", gain=-10)
            self.play(Circumscribe(st[2], color=th.AMBER))
        nb = C.show_neby(self, "celebrate", height=1.5)
        self.wait(1.2)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))

    def redox(self):
        bur = C.Burette(x=-4.2, top=3.0, bottom=0.0, color=C.PURPLE)
        fl = C.Flask(center=[-4.2, -2.2, 0], scale=1.0, color="#E9ECF5", opacity=0.25)
        eq1 = chem(r"2KMnO_4 + 5H_2C_2O_4 + 3H_2SO_4 \rightarrow K_2SO_4 + 2MnSO_4 + 10CO_2 + 8H_2O", size=26).move_to([1.6, 2.6, 0])
        eq2 = chem(r"2KMnO_4 + 10FeSO_4 + 8H_2SO_4 \rightarrow K_2SO_4 + 2MnSO_4 + 5Fe_2(SO_4)_3 + 8H_2O", size=26).next_to(eq1, DOWN, buff=0.3)
        with self.say("Now redox titrations, where the n factor is the number of electrons transferred. The classic one is permanganometry: potassium permanganate, in dilute sulphuric acid, against oxalic acid or a ferrous salt."):
            self.add(bur.liquid)
            self.play(Create(bur.glass), FadeIn(bur.liquid), FadeIn(fl.g))
            self.play(Write(eq1))
            self.play(Write(eq2))
        with self.say("Watch the colour. Each purple drop is decolourised the instant it lands, as long as any reducing agent is left in the flask."):
            for k in range(5):
                d = Circle(radius=0.06, fill_color=C.PURPLE, fill_opacity=1, stroke_width=0).move_to(bur.tip_point)
                self.add(d)
                self.play(d.animate.move_to(fl.surface), bur.vol.animate.increment_value(3), run_time=0.35, rate_func=linear)
                self.remove(d)
                self.play(fl.liq.animate.set_fill(C.PURPLE, opacity=0.45), run_time=0.15)
                self.play(fl.liq.animate.set_fill("#E9ECF5", opacity=0.25), run_time=0.4)
        with self.say("Then one drop too many, and a pale pink colour stays. Permanganate is its own indicator. We call it self indicating."):
            d = Circle(radius=0.06, fill_color=C.PURPLE, fill_opacity=1, stroke_width=0).move_to(bur.tip_point)
            self.add(d)
            self.play(d.animate.move_to(fl.surface), run_time=0.35)
            self.remove(d)
            self.sfx("impact", gain=-12)
            self.play(fl.liq.animate.set_fill(C.PINK_END, opacity=0.6), run_time=0.6)
        dich = para("Potassium dichromate is a primary standard and keeps indefinitely, but it is not self-indicating: diphenylamine is used as indicator.", width=7.2, size=24, color=th.BODY).move_to([2.0, -0.6, 0])
        e3 = chem(r"K_2Cr_2O_7 + 6FeSO_4 + 7H_2SO_4 \rightarrow K_2SO_4 + Cr_2(SO_4)_3 + 3Fe_2(SO_4)_3 + 7H_2O", size=24).next_to(dich, DOWN, buff=0.35)
        with self.say("Its partner is dichrometry. Potassium dichromate is a primary standard and its solution keeps for ever, but its colour change is not sharp enough, so an indicator like diphenylamine is added."):
            self.play(FadeIn(dich), Write(e3))
        self.play(FadeOut(VGroup(bur.glass, fl.g, eq1, eq2, dich, e3)), FadeOut(bur.liquid))
        self.remove(bur.liquid)
        title = T("Only dilute H₂SO₄. And warm the oxalic acid.", size=34, color=th.CORAL, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        hcl = VGroup(T("Why not HCl?", size=28, color=th.AMBER, weight="BOLD"),
                     chem(r"2MnO_4^- + 16H^+ + 10Cl^- \rightarrow 2Mn^{2+} + 5Cl_2 + 8H_2O", size=32),
                     para("Chloride is itself oxidised, so extra permanganate is used up and the result comes out too high.", width=10, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        hno = VGroup(T("Why not HNO₃?", size=28, color=th.AMBER, weight="BOLD"),
                     para("Nitric acid is an oxidising agent: it would oxidise the Fe²⁺ or oxalic acid itself.", width=10, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        heat = VGroup(T("Why 60–70 °C?", size=28, color=th.AMBER, weight="BOLD"),
                      para("The oxalate reaction is very slow in the cold; it speeds up once the Mn²⁺ it makes catalyses it.", width=10, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(hcl, hno, heat).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.4)
        nb = C.show_neby(self, "think", height=1.4)
        with self.say("Three practical rules, all favourite five mark questions. Acidify only with dilute sulphuric acid. Hydrochloric acid is itself oxidised by permanganate to chlorine, which uses up extra permanganate and gives a high result."):
            self.play(FadeIn(title), FadeIn(hcl, shift=UP * 0.2))
        with self.say("Nitric acid is an oxidising agent, so it would oxidise the ferrous ions or oxalic acid by itself. And oxalic acid titrations are done hot, at sixty to seventy degrees, because the reaction is very slow in the cold, until the manganese two plus it produces starts to catalyse it."):
            self.play(FadeIn(hno, shift=UP * 0.2))
            self.play(FadeIn(heat, shift=UP * 0.2))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(title, hcl, hno, heat)))

    def example_16(self):
        head, prob = C.example_head(self, "20.0 cm³ of 0.1 N KMnO₄ oxidised 25.0 cm³ of oxalic acid (H₂C₂O₄·2H₂O) in hot dilute H₂SO₄. Find the normality, molarity and strength of the oxalic acid.")
        st = C.steps(r"N = \frac{0.1 \times 20.0}{25.0} = 0.08\ \mathrm{N}",
                     r"\mathrm{C_2O_4^{2-} \rightarrow 2CO_2 + 2e^-} \;\Rightarrow\; n = 2,\ E = \tfrac{126}{2} = 63",
                     r"M = \frac{N}{n} = \frac{0.08}{2} = 0.04\ \mathrm{mol\,L^{-1}}",
                     r"S = N \times E = 0.08 \times 63 = 5.04\ \mathrm{g\,L^{-1}}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example one point six. Twenty cubic centimetres of decinormal permanganate oxidised twenty five cubic centimetres of oxalic acid. Find the normality, molarity and strength of the oxalic acid."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("By the law of equivalence, normality is zero point one times twenty, over twenty five: zero point zero eight normal. No balanced equation needed."):
            self.play(Write(st[0]))
        with self.say("Each oxalate ion loses two electrons to become two carbon dioxide molecules. So n is two, and the equivalent weight of the dihydrate is one twenty six over two, sixty three."):
            self.play(Write(st[1]))
        with self.say("Molarity is normality over n, zero point zero four. Strength is normality times E, five point zero four grams per litre."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def example_17(self):
        head, prob = C.example_head(self, "3.92 g of pure Mohr's salt (molar mass 392) was made up to 250 cm³ in dilute H₂SO₄. 25.0 cm³ of it needed 20.0 cm³ of KMnO₄. Find the normality of the KMnO₄ and its mass per litre.")
        st = C.steps(r"n(\mathrm{Fe^{2+} \rightarrow Fe^{3+}}) = 1 \;\Rightarrow\; E = 392",
                     r"\text{eq} = \frac{3.92}{392} = 0.0100 \;\Rightarrow\; N = \frac{0.0100}{0.250} = 0.04\ \mathrm{N}",
                     r"\text{meq in aliquot} = 0.04 \times 25.0 = 1.00",
                     r"N(\mathrm{KMnO_4}) = \frac{1.00}{20.0} = 0.05\ \mathrm{N}",
                     r"S = 0.05 \times 31.6 = 1.58\ \mathrm{g\,L^{-1}}", size=36, buff=0.3).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        st[4].set_color(th.AMBER)
        with self.say("Worked example one point seven, standardising permanganate against Mohr's salt. Three point nine two grams of pure Mohr's salt, molar mass three ninety two, made up to two fifty cubic centimetres. Twenty five cubic centimetres of it needed twenty cubic centimetres of permanganate."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("Mohr's salt gives one ferrous ion, which loses one electron. So n is one and E is three ninety two. Three point nine two over three ninety two is zero point zero one equivalent, in a quarter litre: zero point zero four normal."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("The aliquot holds zero point zero four times twenty five, one milliequivalent. That reacted with twenty cubic centimetres of permanganate, so its normality is one over twenty, zero point zero five."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        with self.say("In acid, permanganate's equivalent weight is thirty one point six. So one litre contains zero point zero five times thirty one point six, one point five eight grams."):
            self.play(Write(st[4]))
            self.play(Circumscribe(st[4], color=th.AMBER))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Gravimetric weighs a precipitate; volumetric measures a volume of standard solution.",
            M(r"E = \frac{\text{molar mass}}{n},\qquad E_{\text{element}} = \frac{\text{atomic weight}}{\text{valency}}", size=34),
            "n = basicity, acidity, total charge, or electrons transferred.  KMnO₄: 31.6 (acid), 52.67 (neutral), 158 (strong alkali).",
            M(r"N = M \times n,\quad S = N \times E,\quad M = \frac{10\,p\,d}{M_w}", size=34),
            "Molality and % by mass do not change with temperature; molarity and normality do.",
            "Primary standards (oxalic acid, Na₂CO₃, K₂Cr₂O₇) can be weighed directly; secondary (NaOH, HCl, KMnO₄) cannot.",
            M(r"N_1V_1 = N_2V_2 \quad\text{or}\quad n_1M_1V_1 = n_2M_2V_2", size=34),
            "KMnO₄ is self-indicating; acidify with dilute H₂SO₄ only.",
        ], "Let us recap. Gravimetric analysis weighs, volumetric analysis measures a volume. Equivalent weight is molar mass over the n factor, and for an element, atomic weight over valency. The n factor is basicity, acidity, total charge, or electrons transferred, which gives permanganate three different values. Normality is molarity times n. Molality does not change with temperature. Primary standards can be weighed directly, secondary ones cannot. N one V one equals N two V two. And permanganate is its own indicator, in dilute sulphuric acid only.")
        self.outro("That is volumetric analysis. Next time, we look inside those acids and bases, with ionic equilibrium, and find out why indicators behave the way they do. Keep practising, and see you in the next lesson on NEBians.")
