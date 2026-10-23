import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

# the running triangle a = 13, b = 14, c = 15 (B at origin, C on the x-axis)
RA, RB, RC = np.array([7.6154, 12.9231, 0]), np.array([0.0, 0, 0]), np.array([13.0, 0, 0])


def tri(A, B, C, color=th.INK, labels=True, sides=None, size=30):
    poly = Polygon(A, B, C, stroke_color=color, stroke_width=4)
    g = VGroup(poly)
    cen = (A + B + C) / 3
    if labels:
        for p_, n_ in ((A, "A"), (B, "B"), (C, "C")):
            d = p_ - cen
            g.add(M(n_, size=size, color=th.INK).move_to(p_ + 0.32 * d / np.linalg.norm(d)))
    if sides:
        for (p_, q_), s_ in zip(((B, C), (C, A), (A, B)), sides):
            mid = (p_ + q_) / 2
            d = mid - cen
            g.add(M(s_, size=size - 2, color=th.AMBER).move_to(mid + 0.62 * d / np.linalg.norm(d)))
    return g


def place(P_, s=0.32, at=(-4.2, -2.4, 0)):
    return np.array(at) + s * P_


def angle_arc(V, P1, P2, r=0.45, color=th.SKY):
    a1 = np.arctan2(*(P1 - V)[:2][::-1])
    a2 = np.arctan2(*(P2 - V)[:2][::-1])
    d = (a2 - a1 + PI) % TAU - PI
    return Arc(radius=r, start_angle=a1, angle=d, arc_center=V, color=color, stroke_width=4)


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 6
    TITLE = "Properties of a Triangle"
    SUBTITLE = "Translating sides into angles"
    SECTIONS = ["Sine law", "Cosine law", "Tangent law", "Projection laws", "Half angle laws", "Area and the radii"]
    NEXT = "Unit 7 · Solution of Triangles"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        river = Rectangle(width=14.5, height=1.6, stroke_width=0, fill_color="#1E4A7A", fill_opacity=0.7).move_to([0, 0.4, 0])
        waves = VGroup(*[FunctionGraph(lambda x, k=k: 0.06 * np.sin(3 * x + k) + 0.4 + (k - 1) * 0.4, x_range=[-7, 7], color="#4D86C6", stroke_width=2) for k in range(3)])
        Pp, Qp = np.array([-2.0, -1.9, 0]), np.array([1.6, -1.9, 0])
        hh = 3.6 / (1 / np.tan(np.radians(70)) + 1 / np.tan(np.radians(60)))
        Tp = Pp + np.array([hh / np.tan(np.radians(70)), hh, 0])
        tree = VGroup(Rectangle(width=0.12, height=0.5, stroke_width=0, fill_color="#8B5A2B", fill_opacity=1).move_to(Tp + DOWN * 0.15), Triangle(stroke_width=0, fill_color=th.MINT, fill_opacity=1).scale(0.35).move_to(Tp + UP * 0.25))
        base = Line(Pp, Qp, color=th.AMBER, stroke_width=5)
        bl = T("50 m", size=26, color=th.AMBER).next_to(base, DOWN, buff=0.15)
        s1, s2 = DashedLine(Pp, Tp, color=th.INK), DashedLine(Qp, Tp, color=th.INK)
        a1, a2 = angle_arc(Pp, Qp, Tp, r=0.6), angle_arc(Qp, Tp, Pp, r=0.6)
        l1 = T("70°", size=24, color=th.SKY).move_to(Pp + np.array([1.0, 0.3, 0]))
        l2 = T("60°", size=24, color=th.SKY).move_to(Qp + np.array([-1.05, 0.3, 0]))
        q = T("How far is the tree?  (no boat, no rope)", size=28, color=th.INK).to_edge(UP, buff=0.4)
        with self.say("A surveyor on the bank of the Narayani wants the distance to a tree on the far side. No boat, no rope across the water."):
            self.play(FadeIn(river), Create(waves), FadeIn(tree), FadeIn(q))
        with self.say("Instead she walks fifty metres along her bank and measures two angles: seventy degrees at one end, sixty at the other. One side and two angles: the triangle is now completely decided."):
            self.play(Create(base), FadeIn(bl))
            self.play(Create(s1), Create(s2), Create(a1), Create(a2), FadeIn(l1), FadeIn(l2))
        ans = T("sine law: 50·sin 60° / sin 50° ≈ 56.5 m", size=28, color=th.MINT).move_to([0, -2.6, 0])
        with self.say("The third angle is fifty degrees, and the sine law turns those angles into the missing sides: about fifty six and a half metres. This unit is the dictionary that translates between sides and angles."):
            self.play(Write(ans))
            nb = P.neby_in(self, "cool", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(river, waves, tree, base, bl, s1, s2, a1, a2, l1, l2, q, ans)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 6: Properties of a Triangle."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. The sine law, the cosine law, the tangent law, the projection laws, the half angle laws, and finally the area of a triangle with its circumcircle, incircle and excircles. One triangle, thirteen, fourteen, fifteen, will run through all of them.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Standard notation, and the sine law")
        A, B, C = place(RA), place(RB), place(RC)
        t = tri(A, B, C, sides=["a = 13", "b = 14", "c = 15"])
        note = P.bullets(["side a faces angle A, b faces B, c faces C", "A + B + C = 180°", "s = (a + b + c)/2,  area Δ"], width=6.2, size=24).move_to([3.4, 0.9, 0])
        with self.say("Standard notation. Side a faces angle A, b faces B, c faces C. The angles add to one eighty, s is the semi perimeter, and delta is the area. Our running triangle has sides thirteen, fourteen and fifteen: its numbers come out unusually clean."):
            self.play(FadeIn(h), Create(t[0]), FadeIn(t[1:]))
            self.play(FadeIn(note))
        D = np.array([A[0], B[1], 0])
        alt = DashedLine(A, D, color=th.CORAL, stroke_width=4)
        hl = M("h", size=30, color=th.CORAL).next_to(alt, RIGHT, buff=0.08)
        der = VGroup(M(r"h = c\sin B", size=36), M(r"h = b\sin C", size=36), M(r"c\sin B = b\sin C \Rightarrow \frac{b}{\sin B} = \frac{c}{\sin C}", size=36),
                     M(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}", size=46, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.3, -1.0, 0])
        with self.say("Drop the altitude from A, length h. In the left right-angled triangle, h is c sin B. In the right one, h is b sin C. They are the same length, so b over sin B equals c over sin C. Do the same from another vertex and all three ratios are equal: the sine law.") as v:
            self.play(FadeOut(note), Create(alt), FadeIn(hl))
            arcs = VGroup(angle_arc(B, C, A), angle_arc(C, A, B))
            self.play(Create(arcs[0]), Write(der[0]))
            self.play(Create(arcs[1]), Write(der[1]))
            self.play(Write(der[2]))
            self.play(Write(der[3]))
        self.play(FadeOut(VGroup(h, t, alt, hl, der, arcs)))
        self.p1_circle()

    def p1_circle(self):
        h = P.head(self, "The common ratio is the diameter: 2R")
        O, R = np.array([-3.4, -0.5, 0]), 2.4
        circ = Circle(radius=R, stroke_color=th.FAINT, stroke_width=3).move_to(O)
        th_ = ValueTracker(1.75)
        Bq, Cq = O + R * np.array([np.cos(np.radians(215)), np.sin(np.radians(215)), 0]), O + R * np.array([np.cos(np.radians(325)), np.sin(np.radians(325)), 0])
        Ap = lambda: O + R * np.array([np.cos(th_.get_value()), np.sin(th_.get_value()), 0])
        trg = always_redraw(lambda: VGroup(Polygon(Ap(), Bq, Cq, stroke_color=th.INK, stroke_width=4), Dot(Ap(), color=th.AMBER), angle_arc(Ap(), Bq, Cq, r=0.5, color=th.AMBER),
                                           M("A", size=30).move_to(Ap() + 0.35 * (Ap() - O) / R)))
        bc = VGroup(M("B", size=30).move_to(Bq + 0.35 * (Bq - O) / R), M("C", size=30).move_to(Cq + 0.35 * (Cq - O) / R))
        a = np.linalg.norm(Cq - Bq)

        def readout():
            A_ = Ap()
            u, v = Bq - A_, Cq - A_
            ang = np.arccos(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v))
            return VGroup(VGroup(T("angle A =", size=24, color=th.MUTED), DecimalNumber(np.degrees(ang), num_decimal_places=1, font_size=34, color=th.AMBER), T("°", size=26, color=th.AMBER)).arrange(RIGHT, buff=0.12),
                          VGroup(M(r"\frac{a}{\sin A} =", size=34), DecimalNumber(a / np.sin(ang), num_decimal_places=2, font_size=36, color=th.MINT)).arrange(RIGHT, buff=0.15),
                          VGroup(T("diameter 2R =", size=24, color=th.MUTED), DecimalNumber(2 * R, num_decimal_places=2, font_size=36, color=th.MINT)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.9, 0])

        rd = always_redraw(readout)
        why = para("Angles in the same segment are equal, so A matches the angle at A′ where BA′ is a diameter; that triangle has a right angle at C, so sin A = a/2R.", width=6.4, size=22, color=th.BODY).move_to([3.4, -1.9, 0])
        with self.say("Why are the three ratios equal? Draw the circle through A, B and C, the circumcircle, with radius R. Keep B and C fixed and slide A round the circle. The angle at A does not change, and neither does a over sin A. It always equals the diameter, two R."):
            self.play(FadeIn(h), Create(circ), FadeIn(bc))
            self.add(trg, rd)
            self.play(th_.animate.set_value(2.6), run_time=2.0)
            self.play(th_.animate.set_value(1.0), run_time=2.0)
        Ad = 2 * O - Bq
        dia = VGroup(Line(Bq, Ad, color=th.CORAL, stroke_width=4), Line(Ad, Cq, color=th.CORAL, stroke_width=3), M(r"A'", size=30, color=th.CORAL).move_to(Ad + 0.35 * (Ad - O) / R))
        res = M(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R", size=42, color=th.MINT).move_to([0, -3.0, 0])
        with self.say("The proof: take A prime at the end of the diameter through B. The angle at A prime equals the angle at A, standing on the same chord, and the angle at C is a right angle, in a semicircle. So sin A is a over two R."):
            self.play(Create(dia), FadeIn(why))
        with self.say("So a over sin A, b over sin B and c over sin C all equal two R. Written as a equals two R sin A, it is the switch that turns any side into a sine."):
            self.play(FadeOut(why), Write(res))
        self.play(FadeOut(VGroup(h, circ, bc, dia, res)), FadeOut(trg), FadeOut(rd))
        self.remove(trg, rd)
        P.worked(self, "In triangle ABC, A = 30°, B = 45°, a = 10 cm. Find b and c.",
                 [r"C = 180^\circ - 30^\circ - 45^\circ = 105^\circ", r"b = \frac{a\sin B}{\sin A} = \frac{10 \cdot \frac{1}{\sqrt2}}{\frac12} = 10\sqrt2 = 14.14\ \text{cm}", r"c = \frac{a\sin C}{\sin A} = \frac{10 \times 0.9659}{0.5} = 19.32\ \text{cm}"],
                 ["Two angles and a side: the sine law's home ground.", "First the third angle: a hundred and five degrees.", "Then b over sin B equals a over sin A: ten root two, fourteen point one four.", "And c, using sin one oh five, point nine six five nine: nineteen point three two. The largest side faces the largest angle. Check."])
        P.worked(self, "Prove that a(sin B − sin C) + b(sin C − sin A) + c(sin A − sin B) = 0.",
                 [r"a = 2R\sin A,\ b = 2R\sin B,\ c = 2R\sin C", r"\text{LHS} = 2R\left[\sin A\sin B - \sin A\sin C + \sin B\sin C - \sin B\sin A + \sin C\sin A - \sin C\sin B\right]", r"= 2R \cdot 0 = 0"],
                 ["An identity. Turn every side into a sine.", "Use a equals two R sin A, and the same for b and c.", "Expand the bracket. Every product appears twice, with opposite signs.", "So it is zero."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Cosine law: Pythagoras with a correction")
        Aang = ValueTracker(55.0)
        b_, c_ = 3.0, 5.0
        # use the textbook layout: A at the left, AB along the base
        Ab = np.array([-6.2, -2.3, 0])
        Bb = Ab + np.array([c_, 0, 0])

        def C_of():
            t = np.radians(Aang.get_value())
            return Ab + b_ * np.array([np.cos(t), np.sin(t), 0])

        def scene_():
            Cq = C_of()
            D = np.array([Cq[0], Ab[1], 0])
            g = VGroup(Polygon(Ab, Bb, Cq, stroke_color=th.INK, stroke_width=4),
                       DashedLine(Cq, D, color=th.CORAL, stroke_width=3), Line(Ab, D, color=th.SKY, stroke_width=7), angle_arc(Ab, Bb, Cq, r=0.5, color=th.AMBER),
                       M("A", size=30).next_to(Ab, DL, buff=0.08), M("B", size=30).next_to(Bb, DR, buff=0.08), M("C", size=30).next_to(Cq, UP, buff=0.1), M("D", size=26, color=th.CORAL).next_to(D, DOWN, buff=0.12),
                       M("b", size=30, color=th.AMBER).move_to((Ab + Cq) / 2 + np.array([-0.25, 0.2, 0])), M("c", size=30, color=th.AMBER).move_to((Ab + Bb) / 2 + np.array([0.6, -0.3, 0])),
                       M("a", size=30, color=th.AMBER).move_to((Bb + Cq) / 2 + np.array([0.25, 0.2, 0])))
            return g

        sc = always_redraw(scene_)
        der = VGroup(M(r"AD = b\cos A,\quad CD = b\sin A,\quad DB = c - b\cos A", size=32), M(r"a^2 = (b\sin A)^2 + (c - b\cos A)^2", size=34), M(r"a^2 = b^2 + c^2 - 2bc\cos A", size=46, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.0, 1.3, 0])

        def live():
            t = np.radians(Aang.get_value())
            a = np.linalg.norm(C_of() - Bb)
            bb, cc = b_, c_
            return VGroup(VGroup(T("A =", size=28, color=th.MUTED), DecimalNumber(Aang.get_value(), num_decimal_places=0, font_size=38, color=th.AMBER), T("°   cos A =", size=28, color=th.MUTED), DecimalNumber(np.cos(t), num_decimal_places=2, font_size=38, color=th.SKY)).arrange(RIGHT, buff=0.12),
                          VGroup(T("a² =", size=28, color=th.MUTED), DecimalNumber(a ** 2, num_decimal_places=2, font_size=38, color=th.MINT), T("   b² + c² =", size=28, color=th.MUTED), DecimalNumber(bb ** 2 + cc ** 2, num_decimal_places=2, font_size=38, color=th.INK)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, -1.6, 0])

        lv = always_redraw(live)
        with self.say("The sine law cannot help when you know all three sides, or two sides and the angle between them. For that we need the cosine law. Drop the altitude from C onto A B. The blue piece A D is b cos A, the altitude is b sin A, and the rest of the base, D B, is c minus b cos A."):
            self.play(FadeIn(h))
            self.add(sc)
            self.play(Write(der[0]))
        with self.say("Pythagoras in the right triangle on the right: a squared equals b sin A squared, plus c minus b cos A squared. Expand. The sin squared and cos squared combine into one, and a squared equals b squared plus c squared, minus two b c cos A."):
            self.play(Write(der[1]))
            self.play(Write(der[2]))
        with self.say("Think of it as Pythagoras with a correction. At ninety degrees cos A is zero, and it is exactly Pythagoras. Make A acute and a squared is less than b squared plus c squared. Make A obtuse: cos A turns negative, the foot D slides outside the base, and a squared becomes bigger. The same formula covers every case."):
            self.add(lv)
            self.play(Aang.animate.set_value(90), run_time=2.0)
            self.wait(0.5)
            self.play(Aang.animate.set_value(125), run_time=2.0)
            self.wait(0.5)
            self.play(Aang.animate.set_value(55), run_time=1.5)
        self.play(FadeOut(VGroup(h, der)), FadeOut(sc), FadeOut(lv))
        self.remove(sc, lv)
        f = VGroup(M(r"\cos A = \frac{b^2 + c^2 - a^2}{2bc}", size=42), M(r"\cos B = \frac{c^2 + a^2 - b^2}{2ca}", size=42), M(r"\cos C = \frac{a^2 + b^2 - c^2}{2ab}", size=42)).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        with self.say("Rearranged, the cosine law gives any angle from the three sides. Notice the pattern: the side opposite the angle is the one subtracted."):
            self.play(LaggedStart(*[Write(f_) for f_ in f], lag_ratio=0.4))
        self.play(FadeOut(f))
        P.worked(self, "In a triangle a = 13, b = 14, c = 15 cm. Find A and sin C.",
                 [r"\cos A = \frac{196 + 225 - 169}{2 \cdot 14 \cdot 15} = \frac{252}{420} = \frac35 \Rightarrow A = 53^\circ 8'", r"\cos C = \frac{169 + 196 - 225}{2 \cdot 13 \cdot 14} = \frac{140}{364} = \frac{5}{13}", r"\sin C = \sqrt{1 - \tfrac{25}{169}} = \frac{12}{13}\quad (C = 67^\circ 23')"],
                 ["The running triangle.", "Cos A is two fifty two over four twenty: three fifths. A is fifty three degrees eight minutes.", "Cos C is five thirteenths.", "Sin C is positive in a triangle, so it is twelve thirteenths."])
        P.worked(self, "In triangle ABC, b = 7, c = 8 and A = 60°. Find a.",
                 [r"a^2 = 49 + 64 - 2(7)(8)\cdot\tfrac12 = 113 - 56 = 57", r"a = \sqrt{57} = 7.55\ \text{cm}"],
                 ["Two sides and the angle between them.", "The cosine law: forty nine plus sixty four minus fifty six: fifty seven.", "a is root fifty seven, seven point five five centimetres."])
        c = self.callout("careful", "cos A < 0 exactly when a² > b² + c²: A is obtuse. cos A = −0.5 gives A = 120°, not 60°. Only one angle can be obtuse: the one facing the longest side.", width=11, size=26)
        with self.say("Keep the sign. A negative cosine means an obtuse angle: minus a half is one hundred and twenty degrees, not sixty."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Tangent law (Napier's analogy)")
        st = VGroup(M(r"\frac{a-b}{a+b} = \frac{\sin A - \sin B}{\sin A + \sin B}", size=38), M(r"= \frac{2\cos\frac{A+B}{2}\sin\frac{A-B}{2}}{2\sin\frac{A+B}{2}\cos\frac{A-B}{2}} = \cot\frac{A+B}{2}\tan\frac{A-B}{2}", size=36),
                    M(r"\frac{A+B}{2} = 90^\circ - \frac C2 \Rightarrow \cot\frac{A+B}{2} = \tan\frac C2", size=36), M(r"\tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}", size=46, color=th.MINT)).arrange(DOWN, buff=0.35).move_to([0, -0.1, 0])
        says = ["Given two sides and the angle between them, the tangent law finds both other angles at once. Start from the sine law: a minus b over a plus b is sin A minus sin B over sin A plus sin B; the two R cancels.",
                "Turn the sum and difference of sines into products. The twos cancel, leaving cot of half A plus B, times tan of half A minus B.",
                "Half of A plus B is ninety minus half C, so that cotangent is tan of half C.", "Therefore tan of half A minus B equals a minus b over a plus b, times cot of half C."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.1)
        self.play(FadeOut(VGroup(h, st)))
        P.worked(self, "In triangle ABC, a = 9, b = 7, C = 60°. Find A, B and c.",
                 [r"\frac{A+B}{2} = 90^\circ - 30^\circ = 60^\circ", r"\tan\frac{A-B}{2} = \frac{9-7}{9+7}\cot30^\circ = \frac{2}{16}(1.7321) = 0.2165 \Rightarrow \frac{A-B}{2} = 12^\circ 13'",
                  r"A = 60^\circ + 12^\circ 13' = 72^\circ 13',\qquad B = 60^\circ - 12^\circ 13' = 47^\circ 47'", r"c^2 = 81 + 49 - 63 = 67 \Rightarrow c = 8.19"],
                 ["The tangent law at work.", "Half the sum of A and B is ninety minus thirty: sixty degrees.", "Half the difference: two sixteenths times root three, point two one six five, so twelve degrees thirteen minutes.",
                  "Add and subtract: A is seventy two thirteen, B is forty seven forty seven.", "And c from the cosine law: root sixty seven, eight point one nine."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Projection laws: a = b cos C + c cos B")
        A, B, C = place(RA, s=0.33, at=(-5.6, -2.9, 0)), place(RB, s=0.33, at=(-5.6, -2.9, 0)), place(RC, s=0.33, at=(-5.6, -2.9, 0))
        t = tri(A, B, C, sides=["a", "b", "c"])
        D = np.array([A[0], B[1], 0])
        alt = DashedLine(A, D, color=th.MUTED)
        bd = Line(B, D, color=th.SKY, stroke_width=9)
        dc = Line(D, C, color=th.PINK, stroke_width=9)
        cs = VGroup(M(r"BD = c\cos B", size=34, color=th.SKY), M(r"DC = b\cos C", size=34, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 1.5, 0])
        res = VGroup(M(r"a = b\cos C + c\cos B", size=44, color=th.MINT), M(r"b = c\cos A + a\cos C", size=38), M(r"c = a\cos B + b\cos A", size=38)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, -1.2, 0])
        with self.say("Look again at the altitude. It cuts the base into two pieces. The blue piece is the shadow of side c on the base, its projection: c cos B. The pink piece is the projection of b: b cos C."):
            self.play(FadeIn(h), Create(t[0]), FadeIn(t[1:]), Create(alt))
            self.play(Create(bd), Write(cs[0]))
            self.play(Create(dc), Write(cs[1]))
        with self.say("Together they make the whole base. So a equals b cos C plus c cos B. Each side is the sum of the other two, each times the cosine of the angle next to it. If an angle is obtuse, its cosine is negative and the formula still holds."):
            self.play(Write(res[0]))
            self.play(Write(res[1]), Write(res[2]))
        self.play(FadeOut(VGroup(h, t, alt, bd, dc, cs, res)))
        P.worked(self, "Prove that a(b cos C − c cos B) = b² − c².",
                 [r"b\cos C = \frac{a^2 + b^2 - c^2}{2a},\qquad c\cos B = \frac{a^2 + c^2 - b^2}{2a}", r"b\cos C - c\cos B = \frac{2b^2 - 2c^2}{2a} = \frac{b^2 - c^2}{a}", r"a(b\cos C - c\cos B) = b^2 - c^2"],
                 ["Turn everything into sides.", "Replace both cosines by the cosine law. The b and the c cancel neatly.", "Subtract: two b squared minus two c squared over two a.", "Multiply by a. Done. With thirteen, fourteen, fifteen, both sides are minus twenty nine."])
        P.worked(self, "Prove that b cos B + c cos C = a cos(B − C).",
                 [r"b\cos B + c\cos C = 2R(\sin B\cos B + \sin C\cos C) = R(\sin2B + \sin2C)", r"= 2R\sin(B + C)\cos(B - C) = 2R\sin A\cos(B - C)", r"= a\cos(B - C)"],
                 ["This time, turn everything into sines.", "Two sin cos is sin of the double angle.", "Sum to product; and B plus C is one eighty minus A, so its sine is sin A.", "Two R sin A is a."])
        self.tip("In an identity, convert EVERYTHING to sides (cosine/projection laws) or EVERYTHING to sines (a = 2R sin A). Never a mixture.",
                 "Exam tip. In an identity, turn everything into sides, or everything into sines. Never leave a mixture.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Half angle laws")
        st = VGroup(M(r"2\sin^2\frac A2 = 1 - \cos A = \frac{a^2 - (b-c)^2}{2bc} = \frac{2(s-b)\cdot2(s-c)}{2bc}", size=34), M(r"\sin\frac A2 = \sqrt{\frac{(s-b)(s-c)}{bc}}", size=40, color=th.MINT),
                    M(r"\cos\frac A2 = \sqrt{\frac{s(s-a)}{bc}}", size=40, color=th.MINT), M(r"\tan\frac A2 = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}", size=40, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([0, -0.2, 0])
        says = ["Areas and radii need the half angles. Start from one minus cos A, which is two sin squared of half A, and put in the cosine law. The top is a difference of two squares: a plus b minus c, times a minus b plus c. Each is twice s minus something.",
                "So sin of half A is the square root of s minus b, times s minus c, over b c. Positive, because half A is less than ninety degrees.", "One plus cos A gives the cosine: root of s times s minus a, over b c.", "And dividing, the b c cancels: tan of half A is root of s minus b, s minus c, over s, s minus a."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.1)
        self.play(FadeOut(VGroup(h, st)))
        c = self.callout("careful", "s is HALF the perimeter. s − a, s − b, s − c are all positive and add up to s. Writing s = a + b + c wrecks every number that follows.", width=11, size=26)
        with self.say("The commonest slip in this unit: s is half the perimeter. Check every time that s minus a, s minus b and s minus c add up to s."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        P.worked(self, "For a = 13, b = 14, c = 15, find sin(A/2), cos(A/2) and tan(A/2).",
                 [r"s = 21:\ s-a = 8,\ s-b = 7,\ s-c = 6\quad (8 + 7 + 6 = 21\ \checkmark)", r"\sin\frac A2 = \sqrt{\frac{7\cdot6}{14\cdot15}} = \sqrt{\tfrac15},\qquad \cos\frac A2 = \sqrt{\frac{21\cdot8}{210}} = \sqrt{\tfrac45}", r"\tan\frac A2 = \sqrt{\frac{42}{168}} = \frac12 \Rightarrow A = 2(26^\circ 34') = 53^\circ 8'\ \checkmark"],
                 ["The running triangle again.", "s is twenty one, and the three differences are eight, seven and six. They add to twenty one. Good.", "Sin of half A is root a fifth; cos of half A is root four fifths.", "Tan of half A is exactly a half. So A is fifty three degrees eight minutes, as the cosine law found."])
        P.worked(self, "Find the angles of the triangle with sides 3, 5 and 7 cm.",
                 [r"s = 7.5:\ s-a = 4.5,\ s-b = 2.5,\ s-c = 0.5", r"\tan\frac A2 = \sqrt{\frac{2.5 \times 0.5}{7.5 \times 4.5}} = 0.1925 \Rightarrow A = 21^\circ 47'", r"\tan\frac C2 = \sqrt{\frac{4.5 \times 2.5}{7.5 \times 0.5}} = \sqrt3 \Rightarrow C = 120^\circ", r"B = 180^\circ - 21^\circ 47' - 120^\circ = 38^\circ 13'"],
                 ["Three sides, three angles.", "s is seven and a half.", "Tan of half A is point one nine two five: A is twenty one degrees forty seven minutes.", "Tan of half C is root three, so half C is sixty and C is one hundred and twenty. Obtuse, facing the longest side.", "B is what is left: thirty eight thirteen."])
        rows = [["you are given", "use"], ["two angles + a side", "sine law"], ["two sides + an opposite angle", "sine law (watch for two answers)"], ["two sides + the included angle", "cosine law, or tangent law"], ["three sides", "cosine law, or half angle laws"]]
        tb = P.table(rows, [5.4, 6.2], row_h=0.7, size=26, colors=[th.INK, th.AMBER]).move_to([0, 0.2, 0])
        with self.say("Which law for which data? Two angles and a side: the sine law. Two sides and an opposite angle: also the sine law, but watch for two possible triangles, which is the next unit. Two sides and the included angle: cosine or tangent law. Three sides: cosine or half angle laws.") as v:
            P.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "Area: Δ = ½ab sin C = √(s(s − a)(s − b)(s − c))")
        st = VGroup(M(r"\Delta = \tfrac12 \cdot a \cdot (b\sin C) = \tfrac12 ab\sin C", size=38), M(r"\sin A = 2\sin\tfrac A2\cos\tfrac A2 = \frac{2}{bc}\sqrt{s(s-a)(s-b)(s-c)}", size=36),
                    M(r"\Delta = \tfrac12 bc\sin A = \sqrt{s(s-a)(s-b)(s-c)}", size=44, color=th.MINT), M(r"13, 14, 15:\ \ \Delta = \sqrt{21\cdot8\cdot7\cdot6} = \sqrt{7056} = 84", size=38, color=th.AMBER)).arrange(DOWN, buff=0.4).move_to([0, -0.2, 0])
        says = ["The area is half base times height, and the height from A is b sin C. So the area is half a b sin C.", "Write sin A as two sin half A cos half A, and use the half angle laws.",
                "The b c cancels, and the area is the square root of s, s minus a, s minus b, s minus c: Heron's formula. Area from the three sides alone.", "For our triangle: root of twenty one times eight times seven times six. Exactly eighty four."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.1)
        self.play(FadeOut(VGroup(h, st)))
        h = P.head(self, "Three kinds of circle")
        s_ = 0.27
        at = np.array([-5.0, -1.2, 0])
        A, B, C = at + s_ * RA, at + s_ * RB, at + s_ * RC
        t = tri(A, B, C)
        O, R = at + s_ * np.array([6.5, 4.875, 0]), 8.125 * s_
        I, r = at + s_ * np.array([7.0, 4.0, 0]), 4.0 * s_
        s2, at2 = 0.155, np.array([-5.4, 0.1, 0])
        A2, B2, C2 = at2 + s2 * RA, at2 + s2 * RB, at2 + s2 * RC
        t2 = tri(A2, B2, C2, size=26)
        E1, r1 = at2 + s2 * np.array([6.0, -10.5, 0]), 10.5 * s2
        cc = Circle(radius=R, stroke_color=th.SKY, stroke_width=3).move_to(O)
        ic = Circle(radius=r, stroke_color=th.MINT, stroke_width=3).move_to(I)
        ec = Circle(radius=r1, stroke_color=th.AMBER, stroke_width=3).move_to(E1)
        ext = VGroup(DashedLine(B2, A2 + 2.1 * (B2 - A2), color=th.MUTED, stroke_width=2), DashedLine(C2, A2 + 2.1 * (C2 - A2), color=th.MUTED, stroke_width=2))
        f = VGroup(VGroup(M(r"R = \frac{abc}{4\Delta}", size=36, color=th.SKY), T("circumradius: through A, B, C", size=22, color=th.SKY)).arrange(DOWN, buff=0.12),
                   VGroup(M(r"r = \frac{\Delta}{s}", size=36, color=th.MINT), T("inradius: touches all three sides", size=22, color=th.MINT)).arrange(DOWN, buff=0.12),
                   VGroup(M(r"r_1 = \frac{\Delta}{s-a}", size=36, color=th.AMBER), T("exradius: touches a, and b, c produced", size=22, color=th.AMBER)).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.4).move_to([3.9, 0.2, 0])
        vals = M(r"13, 14, 15:\ R = 8.125,\ r = 4,\ r_1 = 10.5", size=32, color=th.INK).move_to([3.9, -2.6, 0])
        with self.say("Every triangle has three kinds of special circle. The circumcircle passes through the three vertices; its radius R is a b c over four delta."):
            self.play(FadeIn(h), Create(t[0]), FadeIn(t[1:]))
            self.play(Create(cc), FadeIn(f[0]))
        with self.say("The incircle sits inside, touching all three sides. Its radius r is delta over s."):
            self.play(Create(ic), FadeIn(f[1]))
        with self.say("And an excircle sits outside, touching side a and the other two sides extended. Its radius r one is delta over s minus a. There are three of these, one opposite each vertex."):
            self.play(FadeOut(VGroup(cc, ic)), ReplacementTransform(t, t2))
            self.play(Create(ext), Create(ec), FadeIn(f[2]))
        with self.say("For our triangle: R is eight point one two five, r is exactly four, and r one is ten and a half."):
            self.play(Write(vals))
        self.play(FadeOut(VGroup(h, t2, ec, ext, f, vals)))
        P.worked(self, "For a = 13, b = 14, c = 15, find R, r, r₁, r₂, r₃.",
                 [r"\Delta = 84,\ s = 21,\ s-a = 8,\ s-b = 7,\ s-c = 6", r"R = \frac{13\cdot14\cdot15}{4\cdot84} = \frac{2730}{336} = 8.125,\qquad r = \frac{84}{21} = 4", r"r_1 = \frac{84}{8} = 10.5,\quad r_2 = \frac{84}{7} = 12,\quad r_3 = \frac{84}{6} = 14"],
                 ["All five radii.", "Collect the numbers: area eighty four, s twenty one, and eight, seven, six.", "R is twenty seven thirty over three thirty six: eight point one two five. r is eighty four over twenty one: four.", "The exradii: ten and a half, twelve and fourteen."])
        P.worked(self, "Prove that r₁ + r₂ + r₃ − r = 4R.",
                 [r"= \Delta\left[\frac{1}{s-a} + \frac{1}{s-b} + \frac{1}{s-c} - \frac1s\right]", r"\frac{1}{s-a} + \frac{1}{s-b} = \frac{c}{(s-a)(s-b)},\qquad \frac{1}{s-c} - \frac1s = \frac{c}{s(s-c)}",
                  r"\text{sum} = c\,\frac{s(s-c) + (s-a)(s-b)}{\Delta^2} = \frac{c \cdot ab}{\Delta^2}", r"r_1 + r_2 + r_3 - r = \frac{abc}{\Delta} = 4R\qquad (10.5 + 12 + 14 - 4 = 32.5 = 4 \times 8.125\ \checkmark)"],
                 ["A favourite proof.", "Write every radius as delta over something.", "Pair them cleverly: s minus a plus s minus b is c, and s minus s minus c is also c.", "Add, and the top simplifies to a b. The bottom is delta squared, by Heron.", "So the total is a b c over delta, which is four R. And our numbers agree: thirty two and a half."])
        self.quiz("In any triangle, a / sin A equals",
                  ["R", "2R", "R/2", "4R"], 1,
                  "Pause and think. The sine law ratio.",
                  "Two R, the diameter of the circumcircle.")
        self.quiz("For the triangle 13, 14, 15, the inradius r is",
                  ["4", "8.125", "84", "21"], 0,
                  "One more. Area eighty four, semi perimeter twenty one.",
                  "Four: delta over s, eighty four over twenty one. Eight point one two five is the circumradius.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Sine law: a/sin A = b/sin B = c/sin C = 2R, so a = 2R sin A.",
            "Cosine law: a² = b² + c² − 2bc cos A; cos A < 0 means A is obtuse.",
            "Tangent law: tan((A − B)/2) = ((a − b)/(a + b)) cot(C/2). Projection: a = b cos C + c cos B.",
            "Half angles: tan(A/2) = √((s − b)(s − c)/(s(s − a))), with s the HALF perimeter.",
            "Δ = ½ab sin C = √(s(s − a)(s − b)(s − c));  R = abc/4Δ,  r = Δ/s,  r₁ = Δ/(s − a).",
        ], "Quick recap. The sine law, with its common ratio two R. The cosine law, Pythagoras with a correction. The tangent and projection laws. The half angle laws in terms of the semi perimeter. And the area, by Heron, with the circumradius, inradius and exradii.")
        self.outro("That was the properties of a triangle. Next, solution of triangles: using these laws to find every missing side and angle, including the ambiguous case. See you there.")
