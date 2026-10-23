import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

SC = 0.2                       # 1 cm in the ambiguous-case figure
A0 = np.array([-6.0, -2.2, 0])
CPT = A0 + 30 * SC * np.array([np.cos(np.radians(30)), np.sin(np.radians(30)), 0])


def feet(a_cm):
    """x-positions where the arc of radius a (cm) from C meets the base line."""
    r, hh = a_cm * SC, CPT[1] - A0[1]
    if r < hh - 1e-6:
        return []
    d = np.sqrt(max(r * r - hh * hh, 0))
    return [CPT[0] - d, CPT[0] + d] if d > 1e-3 else [CPT[0]]


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 7
    TITLE = "Solution of Triangles"
    SUBTITLE = "Three parts in, six parts out"
    SECTIONS = ["The four cases", "The ambiguous case (SSA)", "Heights and distances"]
    NEXT = "Unit 8 · Conic Sections"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        base = Line(A0 + LEFT * 0.6, A0 + RIGHT * 12.4, color=th.MUTED)
        f1, f2 = feet(20)
        B1, B2 = np.array([f1, A0[1], 0]), np.array([f2, A0[1], 0])
        t1 = Polygon(A0, B1, CPT, stroke_color=th.AMBER, stroke_width=5, fill_color=th.AMBER, fill_opacity=0.15)
        t2 = Polygon(A0, B2, CPT, stroke_color=th.SKY, stroke_width=5, fill_color=th.SKY, fill_opacity=0.12)
        labs = VGroup(M("A", size=30).next_to(A0, DL, buff=0.08), M("C", size=30).next_to(CPT, UP, buff=0.1), M("B_1", size=28, color=th.AMBER).next_to(B1, DOWN, buff=0.12), M("B_2", size=28, color=th.SKY).next_to(B2, DOWN, buff=0.12))
        data = VGroup(M(r"a = BC = 20", size=34), M(r"b = AC = 30", size=34), M(r"A = 30^\circ", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 1.9, 0])
        q = T("Same three facts. Two different triangles.", size=30, color=th.CORAL).move_to([0, 3.0, 0])
        with self.say("Here are three facts about a triangle: side a is twenty, side b is thirty, and angle A is thirty degrees. Draw it. Here it is."):
            self.play(Create(base), FadeIn(data))
            self.play(Create(t1), FadeIn(labs[:3]))
        with self.say("And here it is again. A second triangle, completely different, that fits the very same three facts. Both are correct. So when a question gives you two sides and an angle that is not between them, the answer may be two triangles, or one, or none. This unit shows you how to tell, and how to solve any triangle from any three parts."):
            self.play(Create(t2), FadeIn(labs[3]), FadeIn(q))
            nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(base, t1, t2, labs, data, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 7: Solution of Triangles."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Three parts. The four kinds of data and the law that matches each. The ambiguous case, with two sides and a non included angle. And heights and distances: towers, rivers and fields.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        rows = [["given", "name", "first step", "answers"], ["three sides", "SSS", "cosine law or half angles", "one"], ["two sides + angle BETWEEN", "SAS", "cosine law or tangent law", "one"],
                ["one side + two angles", "ASA / AAS", "third angle, then sine law", "one"], ["two sides + angle NOT between", "SSA", "sine law", "0, 1 or 2"]]
        tb = P.table(rows, [4.6, 1.9, 4.4, 1.8], row_h=0.72, size=24, colors=[th.INK, th.AMBER, th.MUTED, th.MINT]).move_to([0, 0.5, 0])
        aaa = para("Three angles (AAA) are NOT enough: they fix the shape, never the size. Every similar triangle has the same angles.", width=11.5, size=24, color=th.CORAL).move_to([0, -2.6, 0])
        with self.say("To solve a triangle is to find all six parts, three sides and three angles, from the three you are given. There are only four patterns of data. Three sides. Two sides and the angle between them. One side and two angles. And two sides with an angle that is not between them. The first three always give exactly one triangle. The last is the troublemaker.") as v:
            P.reveal_table(self, tb, v.dur * 0.85)
        with self.say("And three angles alone will never do: they fix the shape but not the size."):
            self.play(FadeIn(aaa))
        self.play(FadeOut(VGroup(tb, aaa)))
        P.worked(self, "SSS: solve the triangle a = 5, b = 7, c = 8 cm, and find its area.",
                 [r"\cos A = \frac{49 + 64 - 25}{2 \cdot 7 \cdot 8} = \frac{88}{112} = 0.7857 \Rightarrow A = 38^\circ 13'", r"\cos B = \frac{64 + 25 - 49}{2 \cdot 8 \cdot 5} = \frac{40}{80} = \frac12 \Rightarrow B = 60^\circ",
                  r"C = 180^\circ - 38^\circ 13' - 60^\circ = 81^\circ 47'", r"s = 10:\ \Delta = \sqrt{10 \cdot 5 \cdot 3 \cdot 2} = 10\sqrt3 = 17.32\ \text{cm}^2"],
                 ["Three sides.", "The cosine law for A: thirty eight degrees thirteen minutes.", "Again for B: cos B is exactly a half, so B is sixty.", "Subtract for C: eighty one forty seven. The largest angle faces the largest side, eight. Good.", "And the area by Heron: s is ten, so the area is ten root three, seventeen point three two square centimetres."])
        P.worked(self, "SAS: solve a = 3, c = 2 cm, B = 60°.",
                 [r"b^2 = 9 + 4 - 2(3)(2)\tfrac12 = 7 \Rightarrow b = \sqrt7 = 2.646", r"\frac{A + C}{2} = 90^\circ - 30^\circ = 60^\circ;\quad \tan\frac{A-C}{2} = \frac{3-2}{3+2}\cot30^\circ = 0.3464 \Rightarrow \frac{A-C}{2} = 19^\circ 6'",
                  r"A = 79^\circ 6',\qquad C = 40^\circ 54'"],
                 ["Two sides and the angle between them.", "The cosine law gives the third side at once: root seven.", "For the angles, Napier's tangent law gives both together: half the sum is sixty, half the difference nineteen degrees six minutes.", "Add and subtract: A seventy nine six, C forty fifty four."])
        P.worked(self, "ASA: solve A = 60°, C = 75°, b = 10 cm.",
                 [r"B = 180^\circ - 60^\circ - 75^\circ = 45^\circ", r"a = \frac{10\sin60^\circ}{\sin45^\circ} = 12.25,\qquad c = \frac{10\sin75^\circ}{\sin45^\circ} = 13.66", r"45^\circ < 60^\circ < 75^\circ \leftrightarrow 10 < 12.25 < 13.66\ \checkmark"],
                 ["One side and two angles.", "The third angle first: forty five.", "Then the sine law twice: twelve point two five and thirteen point six six.", "Check: the sides increase in the same order as their opposite angles."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Swing side a from C: how often does it hit the base?")
        base = Line(A0 + LEFT * 0.7, A0 + RIGHT * 12.6, color=th.MUTED, stroke_width=3)
        AC = Line(A0, CPT, color=th.INK, stroke_width=4)
        alt = DashedLine(CPT, np.array([CPT[0], A0[1], 0]), color=th.CORAL)
        hl = M(r"h = b\sin A", size=28, color=th.CORAL).next_to(alt, RIGHT, buff=0.1).shift(DOWN * 0.3)
        lab = VGroup(M("A", size=30).next_to(A0, DL, buff=0.08), M("C", size=30).next_to(CPT, UP, buff=0.1), M("b = 30", size=28, color=th.MUTED).move_to((A0 + CPT) / 2 + np.array([-0.4, 0.35, 0])), M(r"30^\circ", size=26, color=th.SKY).move_to(A0 + np.array([1.0, 0.25, 0])))
        a = ValueTracker(10.0)

        def figure():
            av = a.get_value()
            g = VGroup(Arc(radius=av * SC, start_angle=PI * 1.02, angle=PI * 0.96, arc_center=CPT, stroke_color=th.AMBER, stroke_width=3, stroke_opacity=0.7))
            for x in feet(av):
                ok = x > A0[0] + 1e-3
                B = np.array([x, A0[1], 0])
                if ok:
                    g.add(Polygon(A0, B, CPT, stroke_color=th.MINT, stroke_width=4, fill_color=th.MINT, fill_opacity=0.12), Dot(B, radius=0.09, color=th.MINT))
                else:
                    g.add(Dot(B, radius=0.09, color=th.CORAL), Cross(Dot(B, radius=0.15), stroke_color=th.CORAL, stroke_width=4))
            return g

        def readout():
            av = a.get_value()
            n = len([x for x in feet(av) if x > A0[0] + 1e-3])
            col = [th.CORAL, th.SKY, th.MINT][n]
            word = ["no triangle", "one triangle", "two triangles"][n]
            return VGroup(VGroup(M("a =", size=34), DecimalNumber(av, num_decimal_places=0, font_size=38, color=th.AMBER)).arrange(RIGHT, buff=0.15),
                          T("h = 15", size=26, color=th.CORAL), T(word, size=32, color=col, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 1.6, 0])

        fig, rd = always_redraw(figure), always_redraw(readout)
        with self.say("Given a, b and A. Draw angle A and side b, which fixes the point C. Side a must reach from C to the base line, so swing a compass of radius a about C. The shortest distance from C to the base is the altitude h, which is b sin A: fifteen here."):
            self.play(FadeIn(h), Create(base), Create(AC), FadeIn(lab))
            self.play(Create(alt), FadeIn(hl))
            self.add(fig, rd)
        with self.say("If a is ten, shorter than h, the arc never reaches the base. No triangle."):
            self.wait(0.5)
        with self.say("At a equals fifteen, exactly h, the arc just touches: one triangle, right angled."):
            self.play(a.animate.set_value(15), run_time=1.5)
        with self.say("Between h and b, say twenty, the arc cuts the base twice, both in front of A: two triangles. This is the ambiguous case."):
            self.play(a.animate.set_value(20), run_time=1.5)
        with self.say("And once a is at least b, the second crossing falls behind A, which is not allowed. Only one triangle again."):
            self.play(a.animate.set_value(32), run_time=1.8)
        self.play(FadeOut(VGroup(h, base, AC, alt, hl, lab)), FadeOut(fig), FadeOut(rd))
        self.remove(fig, rd)
        key = P.bullets(["a < h:  NO triangle  (sin B > 1)", "a = h:  ONE, right-angled at B", "h < a < b:  TWO triangles, B and 180° − B", "a ≥ b:  ONE (the obtuse B is rejected)"], width=10, size=30).move_to([0, 0.3, 0])
        hd = T("The SSA test (A acute), with h = b sin A", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        ob = T("If A is obtuse: one triangle when a > b, none otherwise.", size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("So the test: compute h equals b sin A. Less than h: none. Equal to h: one, right angled. Between h and b: two. At least b: one. And if the given angle is obtuse, there is one triangle when a is longer than b, and none otherwise.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, key, v.dur * 0.7)
            self.play(FadeIn(ob))
        self.play(FadeOut(VGroup(hd, key, ob)))
        P.worked(self, "Solve the triangle a = 20 cm, b = 30 cm, A = 30°.",
                 [r"h = 30 \sin30^\circ = 15 < 20 < 30:\ \text{two triangles}", r"\sin B = \frac{30 \times 0.5}{20} = 0.75 \Rightarrow B_1 = 48^\circ 35'\ \text{or}\ B_2 = 131^\circ 25'",
                  r"C_1 = 101^\circ 25',\ c_1 = \frac{20\sin C_1}{\sin30^\circ} = 39.21;\qquad C_2 = 18^\circ 35',\ c_2 = 12.75"],
                 ["The cold open's triangle.", "h is fifteen, and twenty lies between fifteen and thirty: two triangles.", "The sine law gives sin B equals point seven five. B is forty eight degrees thirty five minutes, or its supplement, one thirty one twenty five. Both work, since A plus B stays below one eighty.",
                  "Solve each: c is thirty nine point two one in the first triangle, and twelve point seven five in the second."])
        P.worked(self, "Can a triangle have a = 10, b = 30, A = 30°? Solve a = 40, b = 30, A = 30°.",
                 [r"\sin B = \frac{30 \times 0.5}{10} = 1.5 > 1:\ \text{no triangle}", r"a = 40 > b:\ \sin B = \frac{15}{40} = 0.375 \Rightarrow B = 22^\circ 1'\ (157^\circ 59'\ \text{rejected: } A + B > 180^\circ)",
                  r"C = 127^\circ 59',\qquad c = \frac{40 \sin C}{\sin30^\circ} = 63.06"],
                 ["Two more.", "With a equal to ten, sin B would be one point five. No angle has that sine. No triangle.", "With a equal to forty, longer than b, only one triangle: B is twenty two degrees one minute. The obtuse option would push A plus B past one eighty.", "Then C and c follow: sixty three point zero six."])
        c = self.callout("careful", "When the sine law gives sin B = k, write BOTH B and 180° − B, then test each with A + B < 180°. Don't silently take the calculator's answer.", width=11, size=26)
        with self.say("The mark-losing habit: taking only the calculator's angle. Always write both B and one eighty minus B, then test each one."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("If a = 20, b = 30 and A = 30°, the number of possible triangles is",
                  ["0", "1", "2", "infinitely many"], 2,
                  "Pause and think. Compare a with h equals b sin A.",
                  "Two. h is fifteen, and twenty lies between fifteen and thirty.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Height of a tower")
        s = 0.09
        gy = -2.4
        Tx = 4.2
        ht = 20 * np.sqrt(3)
        ground = Line([-6.8, gy, 0], [6.6, gy, 0], color=th.MUTED, stroke_width=3)
        tower = Rectangle(width=0.35, height=ht * s, stroke_width=2, stroke_color=th.INK, fill_color="#3A3F5C", fill_opacity=1).move_to([Tx, gy + ht * s / 2, 0])
        S = np.array([Tx, gy + ht * s, 0])
        Pp, Qp = np.array([Tx - 60 * s, gy, 0]), np.array([Tx - 20 * s, gy, 0])
        walker = Dot(Pp, radius=0.1, color=th.SKY)
        ls1 = DashedLine(Pp, S, color=th.AMBER)
        ls2 = DashedLine(Qp, S, color=th.MINT)
        a1 = Arc(radius=0.7, start_angle=0, angle=np.radians(30), arc_center=Pp, color=th.AMBER, stroke_width=4)
        a2 = Arc(radius=0.55, start_angle=0, angle=np.radians(60), arc_center=Qp, color=th.MINT, stroke_width=4)
        lab = VGroup(M("P", size=28).next_to(Pp, DOWN, buff=0.12), M("Q", size=28).next_to(Qp, DOWN, buff=0.12), M("S", size=28).next_to(S, UP, buff=0.1), M("T", size=28).next_to([Tx, gy, 0], DR, buff=0.1),
                     M(r"30^\circ", size=24, color=th.AMBER).move_to(Pp + np.array([1.05, 0.25, 0])), M(r"60^\circ", size=24, color=th.MINT).move_to(Qp + np.array([0.75, 0.42, 0])))
        d40 = VGroup(DoubleArrow(Pp + DOWN * 0.55, Qp + DOWN * 0.55, buff=0, color=th.SKY, stroke_width=3, tip_length=0.15), T("40 m", size=24, color=th.SKY).move_to((Pp + Qp) / 2 + DOWN * 0.85))
        steps = VGroup(M(r"\angle PQS = 180^\circ - 60^\circ = 120^\circ", size=30), M(r"\angle PSQ = 180^\circ - 30^\circ - 120^\circ = 30^\circ", size=30), M(r"\Rightarrow QS = PQ = 40\ \text{m}", size=30),
                       M(r"h = 40\sin60^\circ = 20\sqrt3 = 34.64\ \text{m}", size=34, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-3.6, 1.5, 0])
        with self.say("From a point P the top of a tower is at an elevation of thirty degrees. Walk forty metres towards it, to Q, and the elevation becomes sixty. How tall is the tower?"):
            self.play(FadeIn(h), Create(ground), FadeIn(tower))
            self.play(FadeIn(walker), Create(ls1), Create(a1), FadeIn(lab[0]), FadeIn(lab[2:5]))
            self.play(walker.animate.move_to(Qp), run_time=1.5)
            self.play(Create(ls2), Create(a2), FadeIn(lab[1]), FadeIn(lab[5]), FadeIn(d40))
        with self.say("Look at triangle P Q S. The sixty degrees at Q is an exterior angle, so the angle inside at Q is one twenty. That leaves thirty at S. Two equal angles: the triangle is isosceles, and Q S equals P Q, forty metres. In the right triangle at the foot, the height is forty sin sixty: twenty root three, about thirty four point six metres."):
            for st in steps:
                self.play(Write(st), run_time=0.9)
        self.play(FadeOut(VGroup(h, ground, tower, walker, ls1, ls2, a1, a2, lab, d40, steps)))
        P.worked(self, "A and B are 100 m apart on one bank of a river; a tree C is on the far bank. angle CAB = 60°, angle CBA = 45°. Find AC, BC and the width.",
                 [r"C = 180^\circ - 60^\circ - 45^\circ = 75^\circ\quad (\text{ASA})", r"AC = \frac{100\sin45^\circ}{\sin75^\circ} = 73.21\ \text{m},\qquad BC = \frac{100\sin60^\circ}{\sin75^\circ} = 89.66\ \text{m}", r"\text{width} = AC\sin60^\circ = 63.40\ \text{m}\ \ (= BC\sin45^\circ\ \checkmark)"],
                 ["The surveyor's river.", "A baseline and two angles: the third angle is seventy five.", "The sine law gives both sloping distances.", "The width is the perpendicular from the tree: sixty three point four metres, and the other triangle agrees."])
        P.worked(self, "A field in Chitwan has sides 120 m, 170 m and 250 m. Find its area in m² and in ropani (1 ropani = 508.72 m²).",
                 [r"s = 270:\ \ s - a = 150,\ s - b = 100,\ s - c = 20", r"\Delta = \sqrt{270 \cdot 150 \cdot 100 \cdot 20} = \sqrt{81\,000\,000} = 9000\ \text{m}^2", r"9000 \div 508.72 = 17.69\ \text{ropani}"],
                 ["A real field.", "s is two seventy.", "Heron: nine thousand square metres.", "That is seventeen point seven ropani. Small for such long sides, because the field is long and thin."])
        self.tip("Name the case (SSS, SAS, ASA, SSA) in words before you calculate. Keep five figures, round at the end, and give angles in degrees and minutes: 0.5° is 30′, not 50′.",
                 "Exam tip. Name the case before you calculate. Keep five figures until the end. And remember: half a degree is thirty minutes, not fifty.")
        self.quiz("A triangle can NOT be solved from",
                  ["SSS", "SAS", "AAA", "ASA"], 2,
                  "Pause and think. Which data never fixes a triangle?",
                  "Three angles. They fix the shape, but every similar triangle, of any size, has the same angles.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "SSS: cosine law or half angles.  SAS: cosine law, or the tangent law.",
            "ASA / AAS: third angle first, then the sine law. AAA: shape only.",
            "SSA: h = b sin A. a < h none; a = h one; h < a < b two; a ≥ b one.",
            "Always test both B and 180° − B with A + B < 180°.",
            "Heights and distances: draw it, use the exterior angle, solve the triangle on the baseline.",
        ], "Quick recap. Three sides: cosine law. Two sides and the included angle: cosine or tangent law. One side and two angles: the sine law. Two sides and a non included angle: compare a with b sin A, and test both possible angles. And for heights and distances, draw the figure and solve the triangle on the baseline.")
        self.outro("That was solution of triangles. Next, conic sections: the parabola, ellipse and hyperbola. See you there.")
