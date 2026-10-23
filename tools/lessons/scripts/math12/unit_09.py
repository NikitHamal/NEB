import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

AC, BC = th.AMBER, th.SKY


def vec(o, v, color, w=5):
    return Arrow(o, o + v, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.18)


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 9
    TITLE = "Product of Vectors"
    SUBTITLE = "Two ways to multiply arrows"
    SECTIONS = ["Scalar (dot) product", "Projection and properties", "Dot product in geometry and trigonometry", "Vector (cross) product", "Cross product: areas, moments, sine rules"]
    NEXT = "Unit 10 · Correlation and Regression"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ground = Line([-6.5, -1.6, 0], [6.5, -1.6, 0], color=th.MUTED, stroke_width=3)
        cart = VGroup(RoundedRectangle(corner_radius=0.1, width=1.6, height=0.8, stroke_color=th.INK, fill_color="#5C4033", fill_opacity=1), Circle(radius=0.22, color=th.INK, fill_color=th.BG, fill_opacity=1).shift(DL * 0.45 + LEFT * 0.05), Circle(radius=0.22, color=th.INK, fill_color=th.BG, fill_opacity=1).shift(DR * 0.45 + RIGHT * 0.05))
        cart.move_to([-4.0, -0.95, 0])
        ang = ValueTracker(35)

        def rope():
            a = np.radians(ang.get_value())
            o = cart.get_right() + UP * 0.15
            F = 2.4 * np.array([np.cos(a), np.sin(a), 0])
            return VGroup(vec(o, F, th.AMBER), DashedLine(o + F, o + np.array([F[0], 0, 0]), color=th.FAINT), vec(o, np.array([F[0], 0, 0]), th.MINT, w=7),
                          M(r"F", size=30, color=th.AMBER).move_to(o + F + 0.3 * UP), M(r"F\cos\theta", size=28, color=th.MINT).next_to(o + np.array([F[0] / 2, 0, 0]), DOWN, buff=0.15))

        rp = always_redraw(rope)
        q = VGroup(M(r"W = F\,d\cos\theta = \vec F \cdot \vec d", size=44, color=th.MINT), T("only the part of the pull along the road does work", size=26, color=th.MUTED)).arrange(DOWN, buff=0.25).move_to([2.6, 2.3, 0])
        with self.say("Pull a loaded cart along a road with a rope that slopes upward. Only part of your pull moves the cart forward: the green part, along the road. The rest just lifts."):
            self.play(Create(ground), FadeIn(cart))
            self.add(rp)
            self.play(cart.animate.shift(RIGHT * 2.2), run_time=2.0)
        with self.say("Make the rope steeper and the useful part shrinks; pull straight up and it is zero. The work done is F times d times cos theta. That way of multiplying two arrows to get a number is the dot product. There is a second way, which gives an arrow, and this unit is about both."):
            self.play(ang.animate.set_value(70), run_time=1.5)
            self.play(ang.animate.set_value(15), run_time=1.5)
            self.play(Write(q))
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ground, cart, q)), FadeOut(rp))
        self.remove(rp)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 9: Product of Vectors."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Five parts. The scalar, or dot, product and the angle between vectors. Projections and the rules of the dot product. The dot product in geometry and trigonometry. The vector, or cross, product. And what the cross product measures: areas, moments and the sine rules.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "a · b = |a| |b| cos θ")
        O = np.array([-5.0, -1.4, 0])
        a = 3.8 * RIGHT
        th_ = ValueTracker(50)
        bl = 3.0

        def pic():
            t = np.radians(th_.get_value())
            b = bl * np.array([np.cos(t), np.sin(t), 0])
            return VGroup(vec(O, a, AC), vec(O, b, BC), Arc(radius=0.55, start_angle=0, angle=t, arc_center=O, color=th.INK, stroke_width=3),
                          M(r"\vec a", size=32, color=AC).next_to(O + a, DOWN, buff=0.12), M(r"\vec b", size=32, color=BC).move_to(O + b * 1.15), M(r"\theta", size=28).move_to(O + 0.8 * np.array([np.cos(t / 2), np.sin(t / 2), 0])))

        def rd():
            t = np.radians(th_.get_value())
            dv = 2.6 * 2.0 * np.cos(t)
            col = th.MINT if dv > 0.05 else (th.CORAL if dv < -0.05 else th.AMBER)
            word = "positive: acute" if dv > 0.05 else ("negative: obtuse" if dv < -0.05 else "ZERO: perpendicular")
            return VGroup(VGroup(T("θ =", size=32, color=th.MUTED), DecimalNumber(th_.get_value(), num_decimal_places=0, font_size=42), T("degrees", size=28, color=th.MUTED)).arrange(RIGHT, buff=0.15),
                          VGroup(M(r"\vec a\cdot\vec b =", size=40), DecimalNumber(dv, num_decimal_places=2, font_size=44, color=col)).arrange(RIGHT, buff=0.15), T(word, size=34, color=col, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 1.0, 0])

        p_, r_ = always_redraw(pic), always_redraw(rd)
        with self.say("The scalar, or dot, product of a and b is the length of a, times the length of b, times the cosine of the angle between them. The answer is a number, not a vector. Swing b round and watch its sign."):
            self.play(FadeIn(h))
            self.add(p_, r_)
            self.wait(0.5)
        with self.say("Acute angle: positive. At exactly ninety degrees the cosine is zero, and so is the dot product. Obtuse: negative. So a zero dot product is the test for perpendicular vectors."):
            self.play(th_.animate.set_value(90), run_time=1.6)
            self.wait(0.8)
            self.play(th_.animate.set_value(140), run_time=1.4)
            self.play(th_.animate.set_value(50), run_time=1.2)
        comp = VGroup(M(r"\hat i\cdot\hat i = \hat j\cdot\hat j = \hat k\cdot\hat k = 1,\qquad \hat i\cdot\hat j = \hat j\cdot\hat k = \hat k\cdot\hat i = 0", size=30),
                      M(r"\vec a\cdot\vec b = a_1b_1 + a_2b_2 + a_3b_3", size=40, color=th.MINT), M(r"\cos\theta = \frac{\vec a\cdot\vec b}{|\vec a||\vec b|}", size=40, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([0, -2.0, 0])
        with self.say("In components it is even easier. Each unit vector dotted with itself is one, and with a different one is zero. So the dot product is a one b one plus a two b two plus a three b three, and the cosine of the angle is the dot product over the two lengths."):
            self.play(FadeOut(r_), FadeOut(p_))
            self.remove(p_, r_)
            for c_ in comp:
                self.play(Write(c_), run_time=0.9)
        self.play(FadeOut(VGroup(h, comp)))
        P.worked(self, "Find the angle between a = 2i + 2j − k and b = 6i − 3j + 2k.",
                 [r"\vec a\cdot\vec b = 12 - 6 - 2 = 4", r"|\vec a| = \sqrt{9} = 3,\qquad |\vec b| = \sqrt{49} = 7", r"\cos\theta = \frac{4}{21} = 0.1905 \Rightarrow \theta = 79.02^\circ"],
                 ["The standard question.", "Multiply matching components and add: four.", "The lengths: three and seven.", "Cos theta is four over twenty one, so theta is seventy nine degrees."])
        P.worked(self, "Show that A(2, 1, 1), B(2, 2, 3), C(4, 4, 2) form a right-angled triangle.",
                 [r"\vec{BA} = -\hat j - 2\hat k,\qquad \vec{BC} = 2\hat i + 2\hat j - \hat k", r"\vec{BA}\cdot\vec{BC} = 0 - 2 + 2 = 0 \Rightarrow \angle B = 90^\circ"],
                 ["Test each corner.", "For the angle at B, both vectors must start at B: B A and B C.", "Their dot product is zero, so the angle at B is a right angle."])
        c = self.callout("careful", "The angle at a vertex needs BOTH vectors starting at that vertex: for the angle B use BA and BC, not AB and BC (that gives 180° − B).", width=11, size=26)
        with self.say("A careful point: for the angle at B, both arrows must start at B. Using A B instead of B A gives you one eighty minus the angle."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Projection: the shadow of a on b")
        O = np.array([-5.2, -2.6, 0])
        b = np.array([7.0, 1.0, 0])
        bu = b / np.linalg.norm(b)
        a = np.array([2.2, 2.8, 0])
        pr = np.dot(a, bu) * bu
        A_, Bv = vec(O, a, AC), vec(O, b, BC)
        shadow = Line(O, O + pr, color=th.MINT, stroke_width=9)
        drop = DashedLine(O + a, O + pr, color=th.FAINT)
        ra = RightAngle(Line(O + pr, O), Line(O + pr, O + a), length=0.2, color=th.MUTED)
        labs = VGroup(M(r"\vec a", size=34, color=AC).next_to(O + a, UP, buff=0.1), M(r"\vec b", size=34, color=BC).next_to(O + b, RIGHT, buff=0.1), M(r"|\vec a|\cos\theta", size=30, color=th.MINT).next_to(O + pr / 2, DOWN, buff=0.25))
        f = VGroup(M(r"\text{scalar projection of } \vec a \text{ on } \vec b = |\vec a|\cos\theta = \frac{\vec a\cdot\vec b}{|\vec b|}", size=32, color=th.MINT),
                   M(r"\text{vector projection} = \left(\frac{\vec a\cdot\vec b}{|\vec b|^2}\right)\vec b", size=32)).arrange(DOWN, buff=0.3).move_to([1.6, 1.6, 0])
        with self.say("Shine a light straight down onto b. The shadow that a casts on b is the projection of a on b. Its length is a cos theta, which is the dot product divided by the length of b, the vector you project onto. Multiply by the unit vector along b and you get the vector projection."):
            self.play(FadeIn(h), GrowArrow(Bv), GrowArrow(A_), FadeIn(labs[:2]))
            self.play(Create(drop), Create(ra))
            self.play(Create(shadow), FadeIn(labs[2]))
            self.play(Write(f[0]))
            self.play(Write(f[1]))
        self.play(FadeOut(VGroup(h, A_, Bv, shadow, drop, ra, labs, f)))
        P.worked(self, "a = i + 3j + 2k, b = 3i + 2j + 6k: find the projection of a on b, the vector projection, and the angle.",
                 [r"\vec a\cdot\vec b = 3 + 6 + 12 = 21,\quad |\vec a| = \sqrt{14},\quad |\vec b| = 7", r"\text{projection} = \frac{21}{7} = 3,\qquad \text{vector projection} = \frac{21}{49}\vec b = \tfrac37(3\hat i + 2\hat j + 6\hat k)", r"\cos\theta = \frac{21}{7\sqrt{14}} = 0.8018 \Rightarrow \theta = 36.7^\circ"],
                 ["One dot product serves three answers.", "Dot product twenty one; lengths root fourteen and seven.", "Divide by the length of b, the one you project onto: three. For the vector, multiply b by twenty one over forty nine.", "And the angle: thirty six point seven degrees."])
        props = P.bullets(["a · b = b · a   (commutative)", "a · (b + c) = a · b + a · c   (distributive)", "a · a = |a|²", "|a ± b|² = |a|² ± 2 a · b + |b|²", "a · b = 0  ⇔  a and b are perpendicular (both non-zero)"], width=11, size=28).move_to([0, 0, 0])
        hd = T("Properties of the dot product", size=30, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("The rules. Order does not matter. It distributes over addition. A vector dotted with itself is its length squared. So the length of a plus or minus b, squared, expands just like algebra. And a zero dot product means perpendicular.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, props, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, props)))
        P.worked(self, "|a| = 3, |b| = 4, |a + b| = 5. Find a · b, the angle, and |a − b|.",
                 [r"25 = 9 + 2\,\vec a\cdot\vec b + 16 \Rightarrow \vec a\cdot\vec b = 0 \Rightarrow \theta = 90^\circ", r"|\vec a - \vec b|^2 = 9 - 0 + 16 = 25 \Rightarrow |\vec a - \vec b| = 5"],
                 ["No components needed.", "Square the sum and expand: twenty five equals nine plus sixteen plus twice the dot product. So the dot product is zero: perpendicular. A three-four-five right angle.", "The difference has the same length, five."])
        P.worked(self, "F = 4i + j − 3k N moves a particle from A(1, −2, 3) to B(5, −1, 2) m. Find the work done.",
                 [r"\vec d = \vec{AB} = 4\hat i + \hat j - \hat k", r"W = \vec F\cdot\vec d = 16 + 1 + 3 = 20\ \text{J}", r"\cos\theta = \frac{20}{\sqrt{26}\sqrt{18}} = 0.9245 \Rightarrow \theta = 22.4^\circ"],
                 ["Back to work.", "Displacement: head minus tail.", "Work is the dot product: twenty joules.", "And the force is twenty two degrees off the direction of motion."])
        c = self.callout("careful", "You cannot cancel a vector: a · b = a · c does NOT give b = c. It only says a is perpendicular to b − c.", width=11, size=26)
        with self.say("And one trap. You cannot divide by a vector: a dot b equals a dot c does not mean b equals c. It only says a is perpendicular to b minus c."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Parallelogram diagonals: when are they perpendicular?")
        O = np.array([-5.6, -2.4, 0])
        ang = ValueTracker(60)
        blen = ValueTracker(2.2)
        al = 3.4

        def para_():
            t = np.radians(ang.get_value())
            a = al * RIGHT
            b = blen.get_value() * np.array([np.cos(t), np.sin(t), 0])
            d1, d2 = a + b, a - b
            g = VGroup(Polygon(O, O + a, O + a + b, O + b, stroke_color=th.MUTED, stroke_width=3, fill_color=th.PANEL, fill_opacity=0.6), vec(O, a, AC), vec(O, b, BC),
                       Line(O, O + a + b, color=th.MINT, stroke_width=4), Line(O + b, O + a, color=th.PINK, stroke_width=4))
            return g

        def rd():
            t = np.radians(ang.get_value())
            a = al * RIGHT
            b = blen.get_value() * np.array([np.cos(t), np.sin(t), 0])
            dd = np.dot(a + b, a - b)
            return VGroup(VGroup(M(r"|\vec a|^2 - |\vec b|^2 =", size=32), DecimalNumber(dd, num_decimal_places=2, font_size=34, color=th.MINT if abs(dd) < 0.05 else th.INK)).arrange(RIGHT, buff=0.15),
                          T("rhombus: diagonals perpendicular" if abs(dd) < 0.05 else "diagonals not perpendicular", size=26, color=th.MINT if abs(dd) < 0.05 else th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, 1.6, 0])

        pg, r_ = always_redraw(para_), always_redraw(rd)
        der = VGroup(M(r"(\vec a + \vec b)\cdot(\vec a - \vec b) = |\vec a|^2 - |\vec b|^2", size=34), M(r"= 0 \iff |\vec a| = |\vec b|", size=34, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([3.0, -1.0, 0])
        with self.say("The dot product proves geometry with almost no effort. In a parallelogram on a and b, the diagonals are a plus b and a minus b. Their dot product expands to length a squared minus length b squared. That is zero exactly when the sides are equal: the diagonals of a parallelogram are perpendicular only in a rhombus."):
            self.play(FadeIn(h))
            self.add(pg, r_)
            self.play(Write(der[0]))
            self.play(blen.animate.set_value(3.4), run_time=2.0)
            self.play(Write(der[1]))
            self.play(ang.animate.set_value(100), run_time=1.5)
        self.play(FadeOut(VGroup(h, der)), FadeOut(pg), FadeOut(r_))
        self.remove(pg, r_)
        h = P.head(self, "The cosine law in one line")
        O = np.array([-5.4, -2.4, 0])
        a, b = np.array([5.2, 0, 0]), np.array([1.8, 3.8, 0])
        tri = VGroup(vec(O, a, AC), vec(O, b, BC), vec(O + b, a - b, th.MINT), M(r"\vec a", size=32, color=AC).next_to(O + a / 2, DOWN, buff=0.1), M(r"\vec b", size=32, color=BC).next_to(O + b / 2, LEFT, buff=0.1),
                     M(r"\vec c = \vec a - \vec b", size=30, color=th.MINT).next_to(O + b + (a - b) / 2, UR, buff=0.05))
        st = VGroup(M(r"c^2 = (\vec a - \vec b)\cdot(\vec a - \vec b)", size=34), M(r"= a^2 + b^2 - 2\,\vec a\cdot\vec b", size=34), M(r"= a^2 + b^2 - 2ab\cos C", size=40, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.5, 0])
        with self.say("And the cosine law of unit six falls out in one line. The third side is a minus b. Dot it with itself: a squared plus b squared minus two a dot b, which is minus two a b cos C."):
            self.play(FadeIn(h), FadeIn(tri))
            for s_ in st:
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, tri, st)))
        P.worked(self, "Use the dot product of two unit vectors to find cos 15° exactly.",
                 [r"\vec{OP} = \tfrac{1}{\sqrt2}\hat i + \tfrac{1}{\sqrt2}\hat j\ (45^\circ),\qquad \vec{OQ} = \tfrac{\sqrt3}{2}\hat i + \tfrac12\hat j\ (30^\circ)", r"\cos15^\circ = \vec{OP}\cdot\vec{OQ} = \frac{\sqrt3 + 1}{2\sqrt2} = \frac{\sqrt6 + \sqrt2}{4} = 0.9659"],
                 ["Trigonometry from vectors.", "Take unit vectors at forty five and thirty degrees. The angle between them is fifteen, and both have length one.", "So their dot product is cos fifteen: root six plus root two, over four. The same trick proves cos A minus B in general."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "a × b: a vector, perpendicular to both")
        O = np.array([-3.4, -1.6, 0])
        a = np.array([2.8, -0.5, 0])
        b = np.array([1.2, 1.1, 0])
        par = Polygon(O, O + a, O + a + b, O + b, stroke_color=th.MUTED, stroke_width=2, fill_color=th.MINT, fill_opacity=0.25)
        n = vec(O, UP * 2.6, th.CORAL, w=6)
        labs = VGroup(M(r"\vec a", size=32, color=AC).next_to(O + a, DOWN, buff=0.1), M(r"\vec b", size=32, color=BC).next_to(O + b, UP, buff=0.05), M(r"\vec a\times\vec b", size=32, color=th.CORAL).next_to(O + UP * 2.6, LEFT, buff=0.1),
                     T("area = |a × b|", size=24, color=th.MINT).move_to(O + (a + b) / 2 + DOWN * 0.05))
        f = VGroup(M(r"\vec a\times\vec b = |\vec a||\vec b|\sin\theta\ \hat n", size=40, color=th.CORAL), T("length = area of the parallelogram on a and b", size=24, color=th.MINT), para("direction: right-hand rule (curl the fingers from a to b; the thumb points along a × b)", width=6.0, size=22, color=th.MUTED),
                   M(r"\vec b\times\vec a = -\,\vec a\times\vec b", size=36, color=th.AMBER), M(r"\vec a\times\vec b = \vec 0 \iff \vec a \parallel \vec b", size=34)).arrange(DOWN, buff=0.28).move_to([3.3, 0.2, 0])
        with self.say("The second product, the vector or cross product, gives a vector. Its length is a b sin theta, which is exactly the area of the parallelogram on a and b. Its direction is perpendicular to both, chosen by the right hand rule: curl your fingers from a to b, and your thumb points along a cross b."):
            va, vb = vec(O, a, AC), vec(O, b, BC)
            self.play(FadeIn(h), GrowArrow(va), GrowArrow(vb), FadeIn(labs[:2]))
            self.play(FadeIn(par), FadeIn(labs[3]))
            self.play(GrowArrow(n), FadeIn(labs[2]))
            self.play(Write(f[0]), FadeIn(f[1]), FadeIn(f[2]))
        with self.say("Swap the order and the thumb flips: b cross a is minus a cross b. And parallel vectors span no area, so their cross product is the zero vector."):
            self.play(Write(f[3]), Write(f[4]))
        self.play(FadeOut(VGroup(h, par, n, labs, f, va, vb)))
        h = P.head(self, "In components: a 3 × 3 determinant")
        det = M(r"\vec a\times\vec b = \begin{vmatrix} \hat i & \hat j & \hat k \\ a_1 & a_2 & a_3 \\ b_1 & b_2 & b_3 \end{vmatrix}", size=44).move_to([-2.4, 0.8, 0])
        ex = M(r"\vec a = 2\hat i + \hat j + 3\hat k,\quad \vec b = 3\hat i + 5\hat j - 2\hat k", size=32).move_to([0, 2.2, 0])
        G = P.grid([[r"\hat i", r"\hat j", r"\hat k"], [2, 1, 3], [3, 5, -2]], size=40, dx=1.1, dy=0.75).move_to([-4.0, -1.7, 0])
        parts = VGroup(M(r"\hat i:\ (1)(-2) - (3)(5) = -17", size=32), M(r"\hat j:\ -[(2)(-2) - (3)(3)] = +13", size=32), M(r"\hat k:\ (2)(5) - (1)(3) = 7", size=32),
                       M(r"\vec a\times\vec b = -17\hat i + 13\hat j + 7\hat k", size=36, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.8, -1.3, 0])
        with self.say("To compute it, write a determinant: the unit vectors on top, a in the second row, b in the third. Take a equal to two i plus j plus three k, and b equal to three i plus five j minus two k."):
            self.play(FadeIn(h), Write(det), Write(ex))
            self.play(FadeIn(G))
        for k, sy in enumerate(["For the i part, cover the i column and cross-multiply what is left: one times minus two, minus three times five. Minus seventeen.",
                                "For j, cover the j column, cross-multiply, and change the sign. That middle minus sign is where most marks are lost. Plus thirteen.", "For k, cover the k column: two times five minus one times three. Seven."]):
            cover = SurroundingRectangle(VGroup(*[G.cells[i][k] for i in range(3)]), color=th.CORAL, buff=0.08, fill_color=th.BG, fill_opacity=0.85)
            with self.say(sy):
                self.play(FadeIn(cover))
                self.play(Write(parts[k]))
                self.play(FadeOut(cover))
        with self.say("So a cross b is minus seventeen i plus thirteen j plus seven k. Check: dot it with a and you get minus thirty four plus thirteen plus twenty one, zero. Perpendicular, as it must be."):
            self.play(Write(parts[3]))
        self.play(FadeOut(VGroup(h, det, ex, G, parts)))
        P.worked(self, "Find a unit vector perpendicular to both a = i + 2j + 2k and b = 2i + j − 2k.",
                 [r"\vec a\times\vec b = (-4 - 2)\hat i - (-2 - 4)\hat j + (1 - 4)\hat k = -6\hat i + 6\hat j - 3\hat k", r"|\vec a\times\vec b| = \sqrt{81} = 9", r"\hat n = \pm\tfrac13(-2\hat i + 2\hat j - \hat k)"],
                 ["The classic use.", "Anything perpendicular to both is parallel to a cross b: minus six, six, minus three.", "Its length is nine.", "Divide, and remember both directions: plus or minus a third of minus two, two, minus one."])
        P.worked(self, "|a| = 5, |b| = 13, |a × b| = 25. Find a · b.",
                 [r"(\vec a\cdot\vec b)^2 + |\vec a\times\vec b|^2 = |\vec a|^2|\vec b|^2\quad (\cos^2 + \sin^2 = 1)", r"(\vec a\cdot\vec b)^2 = 4225 - 625 = 3600 \Rightarrow \vec a\cdot\vec b = \pm60"],
                 ["Linking the two products.", "Since cos squared plus sin squared is one, the dot product squared plus the cross product's length squared equals the product of the lengths squared: Lagrange's identity.", "So the dot product is plus or minus sixty: the data fixes sin theta, but not whether theta is acute or obtuse."])
        c = self.callout("careful", "a · b is a NUMBER, a × b is a VECTOR. a · b = b · a, but b × a = −a × b. Never write a · b · c or divide by a vector.", width=11, size=26)
        with self.say("Keep the two products apart. The dot product is a number and does not care about order. The cross product is a vector, and order flips its sign."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Areas from the cross product")
        f = VGroup(M(r"\text{parallelogram on } \vec a, \vec b:\ |\vec a\times\vec b|", size=36), M(r"\text{triangle } ABC:\ \tfrac12|\vec{AB}\times\vec{AC}|", size=36, color=th.MINT),
                   M(r"\text{parallelogram from its diagonals:}\ \tfrac12|\vec d_1\times\vec d_2|", size=36), M(r"A, B, C \text{ collinear} \iff \vec{AB}\times\vec{AC} = \vec 0", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.1, 0])
        says = ["The length of the cross product is the area of the parallelogram on the two vectors.", "A triangle is half of that parallelogram: half the cross product of two sides from the same vertex.",
                "If you only know the diagonals of a parallelogram, its area is half their cross product.", "And three points are on one line exactly when the triangle they form has no area: the cross product is zero."]
        self.play(FadeIn(h))
        for f_, sy in zip(f, says):
            with self.say(sy):
                self.play(Write(f_), run_time=0.9)
        self.play(FadeOut(VGroup(h, f)))
        P.worked(self, "Find the area of the triangle A(1, 1, 1), B(1, 2, 3), C(2, 3, 1).",
                 [r"\vec{AB} = (0, 1, 2),\qquad \vec{AC} = (1, 2, 0)", r"\vec{AB}\times\vec{AC} = (0 - 4)\hat i - (0 - 2)\hat j + (0 - 1)\hat k = -4\hat i + 2\hat j - \hat k", r"\text{area} = \tfrac12\sqrt{16 + 4 + 1} = \tfrac{\sqrt{21}}{2} = 2.29\ \text{sq. units}"],
                 ["A triangle in space.", "Two sides from the same vertex A.", "Cross them: minus four, two, minus one.", "Half its length: root twenty one over two, about two point two nine."])
        P.worked(self, "Show A(3, −2, 4), B(1, 1, 1), C(−1, 4, −2) are collinear.",
                 [r"\vec{AB} = (-2, 3, -3),\qquad \vec{AC} = (-4, 6, -6) = 2\,\vec{AB}", r"\vec{AB}\times\vec{AC} = (-18 + 18)\hat i - (12 - 12)\hat j + (-12 + 12)\hat k = \vec 0"],
                 ["Zero area.", "A C is exactly twice A B: the same direction.", "So the cross product is the zero vector, and the three points lie on one line."])
        h = P.head(self, "Moment of a force: M = r × F")
        O = np.array([-5.4, -1.8, 0])
        r = np.array([3.4, 1.0, 0])
        F = np.array([0.5, 2.0, 0])
        pivot = VGroup(Dot(O, radius=0.12, color=th.INK), M("O", size=28).next_to(O, DL, buff=0.08))
        rv, fv = vec(O, r, BC), vec(O + r, F, th.AMBER)
        lineF = DashedLine(O + r - 1.4 * F, O + r + 1.6 * F, color=th.FAINT)
        Fu = F / np.linalg.norm(F)
        foot = O + r - np.dot(r, Fu) * Fu
        perp = DashedLine(O, foot, color=th.MINT, stroke_width=4)
        labs = VGroup(M(r"\vec r", size=32, color=BC).next_to(O + r / 2, DOWN, buff=0.15), M(r"\vec F", size=32, color=th.AMBER).next_to(O + r + F, RIGHT, buff=0.1), M("d", size=30, color=th.MINT).next_to(perp.get_center(), UL, buff=0.05))
        st = VGroup(M(r"\vec M = \vec r\times\vec F", size=40, color=th.CORAL), M(r"|\vec M| = |\vec r||\vec F|\sin\theta = |\vec F|\,d", size=34), para("d = |M| / |F|: the distance from O to the line of action", width=5.4, size=24, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([3.6, 1.0, 0])
        with self.say("Physics uses the cross product for turning. A force F acts at a point with position r from a pivot O. Its moment, or torque, is r cross F. Its size is the force times the perpendicular distance d from O to the line of the force."):
            self.play(FadeIn(h), FadeIn(pivot), GrowArrow(rv), FadeIn(labs[0]))
            self.play(GrowArrow(fv), FadeIn(labs[1]), Create(lineF))
            self.play(Create(perp), FadeIn(labs[2]))
            for s_ in st:
                self.play(Write(s_), run_time=0.8)
        self.play(FadeOut(VGroup(h, pivot, rv, fv, lineF, perp, labs, st)))
        P.worked(self, "F = i + 2j − 2k N acts at P(3, 2, 2). Find its moment about O and the distance from O to its line of action.",
                 [r"\vec M = \vec r\times\vec F = (-4 - 4)\hat i - (-6 - 2)\hat j + (6 - 2)\hat k = -8\hat i + 8\hat j + 4\hat k", r"|\vec M| = \sqrt{144} = 12\ \text{N m},\qquad |\vec F| = 3\ \text{N}", r"d = \frac{12}{3} = 4\ \text{m}"],
                 ["A moment in three dimensions.", "r is three, two, two. Cross with F: minus eight, eight, four.", "Its size is twelve newton metres; the force is three newtons.", "So the line of action passes four metres from O."])
        P.worked(self, "Use the cross product of unit vectors to show sin 75° = (√6 + √2)/4.",
                 [r"\vec{OP} = \cos B\,\hat i - \sin B\,\hat j,\ \ \vec{OQ} = \cos A\,\hat i + \sin A\,\hat j\ \Rightarrow\ \vec{OP}\times\vec{OQ} = \sin(A + B)\,\hat k", r"\sin(A + B) = \sin A\cos B + \cos A\sin B", r"\sin75^\circ = \tfrac{1}{\sqrt2}\cdot\tfrac{\sqrt3}{2} + \tfrac{1}{\sqrt2}\cdot\tfrac12 = \frac{\sqrt6 + \sqrt2}{4} = 0.9659"],
                 ["Trigonometry again, with the other product.", "Take unit vectors at minus B and at A. The angle between them is A plus B, so their cross product has length sin A plus B.", "In components, that cross product is sin A cos B plus cos A sin B.", "With A forty five and B thirty: root six plus root two over four. The same as cos fifteen, as it must be."])
        self.quiz("If a · b = 0 for non-zero vectors a and b, then",
                  ["a is parallel to b", "a is perpendicular to b", "a = b", "a × b = 0"], 1,
                  "Pause and think.",
                  "a is perpendicular to b: cos theta is zero. A zero cross product would mean parallel.")
        self.quiz("The area of the parallelogram with diagonals d₁ and d₂ is",
                  ["|d₁ × d₂|", "½|d₁ × d₂|", "|d₁ · d₂|", "2|d₁ × d₂|"], 1,
                  "One more.",
                  "Half the cross product of the diagonals. The full cross product is for the sides.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "a · b = |a||b| cos θ = a₁b₁ + a₂b₂ + a₃b₃: a NUMBER; zero ⇔ perpendicular.",
            "Projection of a on b = a · b / |b|;  work W = F · d.",
            "a × b = |a||b| sin θ × (unit normal): a VECTOR perpendicular to both; |a × b| = parallelogram area; b × a = −a × b.",
            "Triangle area ½|AB × AC|; collinear ⇔ AB × AC = 0; moment M = r × F.",
            "(a · b)² + |a × b|² = |a|²|b|²;  both products prove cos(A − B), sin(A + B), the cosine law.",
        ], "Quick recap. The dot product is a number, a b cos theta, zero for perpendicular vectors, and gives projections and work. The cross product is a vector perpendicular to both, whose length is an area, and whose order matters. It gives triangle areas, collinearity and moments. And together they prove the compound angle formulas.")
        self.outro("That was product of vectors. Next, correlation and regression: measuring how two quantities move together. See you there.")
