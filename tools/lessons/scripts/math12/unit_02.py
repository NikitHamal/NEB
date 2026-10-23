import os
import sys
from math import comb

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

AC = th.SKY
BC = th.PINK


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 2
    TITLE = "Binomial Theorem"
    SUBTITLE = "Every term of (a + b)ⁿ, without multiplying"
    SECTIONS = ["Binomial theorem, positive integral index", "General term and coefficients", "Any index", "Approximation", "Euler's number e", "Series for eˣ, aˣ and log(1 + x)"]
    NEXT = "Unit 3 · Complex Numbers"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        q = M(r"\sqrt[3]{127} = \ ?", size=80).move_to([0, 1.2, 0])
        a = M(r"5.0265", size=80, color=th.AMBER).move_to([0, -0.6, 0])
        with self.say("No calculator. Find the cube root of one hundred and twenty seven, correct to four decimal places. It sounds impossible by hand."):
            self.play(Write(q))
        with self.say("By the end of this lesson you will do it in three lines: five point zero two six five. And the tool that does it will also expand a to the power twenty in one go, and give you the number e."):
            self.play(FadeIn(a, scale=1.3))
        nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(q, a)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 2: the Binomial Theorem."):
            pass
        self.end_title(tc, nb)
        self.roadmap("The theorem for whole number powers, and its proof. The general term, the middle term and the coefficients. The theorem for any index, as an infinite series. Approximations. Euler's number e. And the series for e to the x, a to the x, and log of one plus x.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Watch the pattern")
        rows = VGroup(M(r"(a+b)^1 = a + b", size=36), M(r"(a+b)^2 = a^2 + 2ab + b^2", size=36), M(r"(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3", size=36),
                      M(r"(a+b)^4 = a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + b^4", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-1.4, 0.4, 0])
        tri = P.pascal(5, dx=0.6, dy=0.5, size=24, top=(4.6, 1.6, 0))
        with self.say("Multiply out the first few powers of a plus b, and watch. The power of a falls from n to zero. The power of b rises from zero to n. They always add to n. And the coefficients, one two one, one three three one, one four six four one, are the rows of Pascal's triangle."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(Write(r_), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tri], lag_ratio=0.2))
        self.play(FadeOut(VGroup(rows, tri)))
        thm = M(r"(a+b)^n = \sum_{r=0}^{n} {}^nC_r\, a^{n-r} b^r", size=54, color=th.MINT).move_to([0, 1.2, 0])
        exp = M(r"= {}^nC_0a^n + {}^nC_1a^{n-1}b + {}^nC_2a^{n-2}b^2 + \cdots + {}^nC_nb^n", size=38).move_to([0, -0.1, 0])
        nt = T("n + 1 terms", size=26, color=th.AMBER).move_to([0, -1.2, 0])
        with self.say("So the binomial theorem says: a plus b to the n is the sum, from r equals zero to n, of n C r times a to the n minus r times b to the r. Exactly n plus one terms."):
            self.play(Write(thm))
            self.play(Write(exp))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(thm, exp, nt)))
        brs = VGroup(*[M(r"(a+b)", size=40, color=th.INK) for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0, 1.4, 0])
        picks = [1, 0, 1, 0, 0]
        hl = VGroup(*[SurroundingRectangle(brs[i][0][3 if picks[i] else 1], color=BC if picks[i] else AC, buff=0.05) for i in range(5)])
        res = M(r"a^3b^2 \text{ appears } {}^5C_2 = 10 \text{ times}", size=40, color=th.AMBER).move_to([0, -0.2, 0])
        with self.say("Why combinations? Because a plus b to the fifth is five brackets multiplied together. To make a term a cubed b squared, you take b from two of the brackets and a from the other three. The number of ways to choose those two brackets is five C two, ten. So a cubed b squared appears ten times."):
            self.play(FadeIn(brs))
            self.play(LaggedStart(*[Create(h_) for h_ in hl], lag_ratio=0.2))
            self.play(Write(res))
        self.play(FadeOut(VGroup(h, brs, hl, res)))
        h = P.head(self, "Proof by induction")
        steps = VGroup(T("Base: n = 1:  ¹C₀a + ¹C₁b = a + b  ✓", size=26, color=th.INK),
                       T("Assume true for n = k, multiply both sides by (a + b):", size=26, color=th.INK),
                       M(r"(a+b)^{k+1} = a^{k+1} + \sum_{r=1}^{k}\left[{}^kC_r + {}^kC_{r-1}\right]a^{k+1-r}b^r + b^{k+1}", size=36),
                       M(r"\text{Pascal: } {}^kC_r + {}^kC_{r-1} = {}^{k+1}C_r \Rightarrow (a+b)^{k+1} = \sum_{r=0}^{k+1}{}^{k+1}C_r\,a^{k+1-r}b^r", size=36, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.1, 0])
        for s_ in steps:
            if s_.width > 12.6:
                s_.scale_to_fit_width(12.6)
        says = ["The formal proof is by induction. For n equal to one it reads a plus b. True.", "Now assume it is true for some k, and multiply both sides by a plus b.",
                "Shift the index in the second sum so both sums have the same shape. The middle terms pair up as k C r plus k C r minus one.", "By Pascal's rule from unit one, that is k plus one C r. So the formula holds for k plus one, and by induction for every positive integer n."]
        self.play(FadeIn(h))
        for s_, sy in zip(steps, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.2)
        self.play(FadeOut(VGroup(h, steps)))
        c = self.callout("careful", "For (a − b)ⁿ the signs alternate. For (2x − 3y)⁹ the whole of −3y is the second term: (−3y)ʳ — cube the 3 too.", width=11, size=26)
        with self.say("Keep the minus sign inside the bracket. For a minus b, the signs alternate. And for two x minus three y, the whole of minus three y is the second quantity, so raise the three to the power as well."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        P.worked(self, "Expand (2x + 3/x)⁵.",
                 [r"(2x)^5 + 5(2x)^4\tfrac{3}{x} + 10(2x)^3\tfrac{9}{x^2} + 10(2x)^2\tfrac{27}{x^3} + 5(2x)\tfrac{81}{x^4} + \tfrac{243}{x^5}",
                  r"= 32x^5 + 240x^3 + 720x + \frac{1080}{x} + \frac{810}{x^3} + \frac{243}{x^5}"],
                 ["A first expansion. a is two x, b is three over x, and the coefficients are one five ten ten five one.", "Write every term with its powers.", "Then simplify each one."])
        P.worked(self, "Evaluate (√3 + 1)⁵ − (√3 − 1)⁵ without a calculator.",
                 [r"(a+b)^5 - (a-b)^5 = 2\left[{}^5C_1a^4b + {}^5C_3a^2b^3 + {}^5C_5b^5\right]", r"= 2\left[5\cdot9 + 10\cdot3 + 1\right] = 2(76) = 152"],
                 ["A neat trick.", "Subtract the two expansions: terms with even powers of b cancel, odd ones double.", "With a squared three and a to the four nine: two times seventy six, one hundred and fifty two. The surds vanish."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "The general term")
        g = M(r"T_{r+1} = {}^nC_r\, a^{n-r}\, b^r", size=60, color=th.MINT).move_to([0, 1.3, 0])
        wn = T("r = 0 gives the FIRST term — so the term with r is the (r + 1)th", size=26, color=th.AMBER).move_to([0, 0.1, 0])
        mid = VGroup(T("middle term:", size=26, color=th.INK, weight="BOLD"), M(r"n \text{ even: } T_{\frac n2 + 1}", size=38), M(r"n \text{ odd: } T_{\frac{n+1}{2}},\ T_{\frac{n+3}{2}}", size=38)).arrange(RIGHT, buff=0.5).move_to([0, -1.4, 0])
        with self.say("Any single term can be written directly. The general term, T r plus one, is n C r, a to the n minus r, b to the r. Notice the plus one: r equal to zero gives the first term, so the term carrying r is the r plus one th. Write the plus one down every time, or you will be one term out."):
            self.play(FadeIn(h), Write(g))
            self.play(FadeIn(wn))
        with self.say("There are n plus one terms. If n is even that is an odd number, and there is one middle term, number n over two plus one. If n is odd, there are two middle terms."):
            self.play(FadeIn(mid))
        self.play(FadeOut(VGroup(h, g, wn, mid)))
        P.worked(self, "Find the term independent of x in (x² − 2/x)⁹.",
                 [r"T_{r+1} = {}^9C_r (x^2)^{9-r}\left(-\tfrac{2}{x}\right)^r = {}^9C_r(-2)^r x^{18-3r}", r"18 - 3r = 0 \Rightarrow r = 6 \ (\text{7th term})", r"{}^9C_6(-2)^6 = 84 \times 64 = 5376"],
                 ["The most common question: the term independent of x.", "Write the general term, and collect all the powers of x into one: x to the eighteen minus three r.", "Independent of x means that power is zero: r is six, the seventh term.", "Its value: eighty four times sixty four, five thousand three hundred and seventy six."])
        P.worked(self, "Find the coefficient of x³² in (x⁴ − 1/x³)¹⁵.",
                 [r"T_{r+1} = (-1)^r\,{}^{15}C_r\,x^{60-7r}", r"60 - 7r = 32 \Rightarrow r = 4", r"(-1)^4\,{}^{15}C_4 = 1365"],
                 ["A coefficient.", "General term: x to the sixty minus seven r.", "Set that equal to thirty two: r is four, a whole number, so the term exists.", "The coefficient is fifteen C four: one thousand three hundred and sixty five."])
        P.worked(self, "Middle term(s) of (a) (x/2 + 2/x)⁸ and (b) (2x − y)⁷.",
                 [r"\text{(a) } T_5 = {}^8C_4\left(\tfrac x2\right)^4\left(\tfrac 2x\right)^4 = 70", r"\text{(b) } T_4 = {}^7C_3(2x)^4(-y)^3 = -560x^4y^3", r"T_5 = {}^7C_4(2x)^3(-y)^4 = 280x^3y^4"],
                 ["Middle terms.", "Eight is even: one middle term, the fifth. The x's cancel completely: seventy.", "Seven is odd: two middle terms, the fourth and fifth. The fourth is minus five sixty x to the four y cubed.", "The fifth is two eighty x cubed y to the four."])
        h = P.head(self, "Sums of binomial coefficients")
        a = M(r"x = 1:\quad {}^nC_0 + {}^nC_1 + \cdots + {}^nC_n = 2^n", size=40).move_to([0, 1.2, 0])
        b = M(r"x = -1:\quad {}^nC_0 - {}^nC_1 + {}^nC_2 - \cdots = 0", size=40).move_to([0, 0.0, 0])
        c = T("sum of coefficients of any expansion: put every variable = 1", size=26, color=th.AMBER).move_to([0, -1.2, 0])
        d = M(r"(2x - 3y)^{12}:\ (2-3)^{12} = 1", size=40, color=th.MINT).move_to([0, -2.2, 0])
        with self.say("Put x equal to one in one plus x to the n: the coefficients add up to two to the n. Put x equal to minus one: the alternating sum is zero. And in general, the sum of the coefficients of any expansion is found by putting every variable equal to one. For two x minus three y to the twelve: minus one to the twelve, which is one."):
            self.play(FadeIn(h), Write(a))
            self.play(Write(b))
            self.play(FadeIn(c))
            self.play(Write(d))
        self.play(FadeOut(VGroup(h, a, b, c, d)))
        P.worked(self, "Three consecutive coefficients of (1 + x)ⁿ are 45, 120 and 210. Find n and the positions.",
                 [r"\frac{n-r+1}{r} = \frac{120}{45} = \frac83 \Rightarrow 3n - 11r + 3 = 0", r"\frac{n-r}{r+1} = \frac{210}{120} = \frac74 \Rightarrow 4n - 11r - 7 = 0", r"n = 10,\ r = 3: \text{ the 3rd, 4th and 5th terms}"],
                 ["The ratio method again.", "The ratio of consecutive coefficients is n minus r plus one over r. Equal to eight thirds.", "The next ratio, equal to seven quarters.", "Subtract: n is ten and r is three. The terms are the third, fourth and fifth."])
        self.tip("Write Tᵣ₊₁ first, collect ALL powers of x into one exponent, then set it equal to what you want. If r is not a whole number, that term does not exist.",
                 "Exam tip. For any particular term, write T r plus one, collect every power of x into a single exponent, and set it equal to the power you want. If r does not come out a whole number, the term simply does not exist.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "When n is not a positive integer")
        s = M(r"(1+x)^n = 1 + nx + \frac{n(n-1)}{2!}x^2 + \frac{n(n-1)(n-2)}{3!}x^3 + \cdots", size=40, color=th.MINT).move_to([0, 1.4, 0])
        cond = M(r"|x| < 1", size=56, color=th.AMBER).move_to([0, 0.1, 0])
        note = para("For a whole-number n the factor (n − n) eventually appears and every later term is zero, so the series stops. Otherwise it never stops: an infinite series, which only makes sense if it converges.", width=11.5, size=24, color=th.BODY).move_to([0, -1.6, 0])
        with self.say("For a negative or fractional power, the same formula still works, but the coefficients never become zero, so the series never stops. One plus x to the n equals one plus n x plus n times n minus one over two factorial x squared, and so on forever. An infinite series is only useful if it converges, and this one does only when the absolute value of x is less than one. That condition is part of the answer: always state it."):
            self.play(FadeIn(h), Write(s))
            self.play(FadeIn(cond, scale=1.3))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(h, s, cond, note)))
        h = P.head(self, "Partial sums of (1 − x)⁻¹ = 1 + x + x² + …")
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1, 6, 1], x_length=8, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-1.0, -0.6, 0])
        true = ax.plot(lambda x: 1 / (1 - x), x_range=[-1.5, 0.83], color=WHITE, stroke_width=4)
        k = ValueTracker(1)

        def partial():
            n = int(k.get_value())
            g, cur = VGroup(), []
            for x in np.arange(-1.5, 1.5001, 0.01):
                y = sum(x ** j for j in range(n))
                if -1 <= y <= 6:
                    cur.append(ax.c2p(x, y))
                else:
                    if len(cur) > 1:
                        g.add(VMobject(stroke_color=th.AMBER, stroke_width=4).set_points_as_corners(cur))
                    cur = []
            if len(cur) > 1:
                g.add(VMobject(stroke_color=th.AMBER, stroke_width=4).set_points_as_corners(cur))
            return g

        part = always_redraw(partial)
        band = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(-1, 0)[0], height=4.4, stroke_width=0, fill_color=th.MINT, fill_opacity=0.08).move_to(ax.c2p(0, 2.5))
        lab = always_redraw(lambda: T(f"{int(k.get_value())} terms", size=26, color=th.AMBER).move_to([4.6, 1.4, 0]))
        with self.say("Watch why. The white curve is one over one minus x. The yellow curve adds up the series term by term. Inside the green band, where x is between minus one and one, the partial sums close in on the true curve. Outside it, they fly away, no matter how many terms you take."):
            self.play(FadeIn(h), Create(ax), FadeIn(band), Create(true))
            self.add(part, lab)
            self.play(k.animate.set_value(12), run_time=5, rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(h, ax, band, true)), FadeOut(part), FadeOut(lab))
        self.remove(part, lab)
        rows = [["expansion", "series (|x| < 1)"], ["(1 − x)⁻¹", "1 + x + x² + x³ + …"], ["(1 + x)⁻¹", "1 − x + x² − x³ + …"], ["(1 − x)⁻²", "1 + 2x + 3x² + 4x³ + …"], ["√(1 + x)", "1 + x/2 − x²/8 + x³/16 − …"]]
        tb = P.table(rows, [3.0, 6.6], row_h=0.66, size=26, colors=[th.AMBER, th.INK]).move_to([0, 0.2, 0])
        with self.say("Four expansions worth knowing by sight. Notice the signs: with minus x inside a negative power, every term is positive; with plus x, the signs alternate.") as v:
            P.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(tb))
        P.worked(self, "Expand to the term in x³ and state the validity: (a) √(1 − 2x), (b) 1/√(4 + x).",
                 [r"\text{(a) } 1 + \tfrac12(-2x) + \frac{\frac12(-\frac12)}{2}(4x^2) + \frac{\frac12(-\frac12)(-\frac32)}{6}(-8x^3)", r"= 1 - x - \tfrac12x^2 - \tfrac12x^3,\quad |x| < \tfrac12",
                  r"\text{(b) } (4+x)^{-1/2} = \tfrac12\left(1+\tfrac x4\right)^{-1/2}", r"= \tfrac12 - \tfrac{x}{16} + \tfrac{3x^2}{256} - \tfrac{5x^3}{2048},\quad |x| < 4"],
                 ["Two expansions.", "For one minus two x to the half, replace x by minus two x everywhere, powers included.", "Simplifying: one minus x minus half x squared minus half x cubed, valid when two x is less than one in size: x less than a half.",
                  "For four plus x, first make the bracket start with one: take the four out as four to the minus half, which is a half.", "Expand with x over four, and multiply by a half. Valid when x over four is less than one: x less than four in size, not one."])
        c = self.callout("careful", "Always factor out the constant so the bracket is (1 + small). The validity condition applies to that small quantity: 1/√(4 + x) needs |x| < 4.", width=11, size=26)
        with self.say("That is the classic mistake: never expand four plus x directly. Make it one plus something small first, and apply the condition to the something small."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Small x: a few terms are enough")
        tm = VGroup(*[VGroup(T(n_, size=24, color=th.MUTED), DecimalNumber(v_, num_decimal_places=7, font_size=34, color=c_)).arrange(RIGHT, buff=0.4) for n_, v_, c_ in
                      [("1", 1.0, th.INK), ("x/3", 0.0066667, th.INK), ("−x²/9", -0.0000444, th.INK), ("next ~x³", 0.000001, th.MUTED)]]).arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to([-2.0, -0.2, 0])
        q = M(r"(1.02)^{1/3} = (1 + 0.02)^{1/3}", size=42).move_to([0, 2.0, 0])
        tot = M(r"\approx 1.00662 \ (\text{true } 1.0066227)", size=40, color=th.MINT).move_to([3.0, -1.6, 0])
        with self.say("When x is small, x squared is tiny and x cubed tinier still, so the first two or three terms already give an excellent value. One point zero two to the power one third: one, plus point zero two over three, minus point zero zero zero four over nine. The next term is about a millionth and cannot touch the fifth decimal place. One point zero zero six six two."):
            self.play(FadeIn(h), Write(q))
            self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.2) for t_ in tm], lag_ratio=0.3))
            self.play(Write(tot))
        self.play(FadeOut(VGroup(h, tm, q, tot)))
        P.worked(self, "Using the binomial theorem, find the cube root of 127 correct to four decimal places.",
                 [r"127^{1/3} = \left[125\left(1 + \tfrac{2}{125}\right)\right]^{1/3} = 5(1 + 0.016)^{1/3}", r"= 5\left[1 + \tfrac{0.016}{3} - \tfrac{0.016^2}{9}\right] = 5[1 + 0.0053333 - 0.0000284]", r"= 5 \times 1.0053049 = 5.0265"],
                 ["The cold open, solved. Pick the nearest perfect cube, one twenty five, and factor it out so the bracket is close to one.", "Five, times one plus point zero one six, to the third.",
                  "Expand: one, plus point zero one six over three, minus its square over nine.", "Five times one point zero zero five three: five point zero two six five. The true value is five point zero two six five two six."])
        P.worked(self, "Find √102 to four decimal places, and (1.02)¹⁰ to four significant figures.",
                 [r"\sqrt{102} = 10(1 + 0.02)^{1/2} = 10[1 + 0.01 - 0.00005 + \cdots] = 10.0995", r"(1.02)^{10} = 1 + 10(0.02) + 45(0.02)^2 + 120(0.02)^3 + \cdots", r"= 1 + 0.2 + 0.018 + 0.00096 \approx 1.219"],
                 ["Two more.", "Root one hundred and two: factor out a hundred, expand: ten point zero nine nine five.",
                  "One point zero two to the tenth: ten is a whole number, so the series is finite and exact; we just stop when terms become negligible.", "One point two one nine."])
        self.tip("To approximate a root: split N into (nearest perfect kth power) + (small remainder) and factor the power out. √102 → 100, the cube root of 127 → 125, fourth root of 17 → 16.",
                 "Exam tip. To approximate a root, split the number into the nearest perfect power plus a small remainder, and factor out the power. Root one oh two: use a hundred. Cube root of one twenty seven: use one twenty five.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "e = lim (1 + 1/n)ⁿ")
        n = ValueTracker(1)
        rd = always_redraw(lambda: VGroup(T("n =", size=30, color=th.MUTED), Integer(int(n.get_value()), font_size=46, color=th.INK),
                                          T("(1 + 1/n)ⁿ =", size=30, color=th.MUTED), DecimalNumber((1 + 1 / max(1, int(n.get_value()))) ** max(1, int(n.get_value())), num_decimal_places=6, font_size=46, color=th.AMBER)).arrange(RIGHT, buff=0.3).move_to([0, 1.2, 0]))
        story = para("A bank pays 100% interest a year. Compound it twice, monthly, daily, every second… the money does not grow without limit. It approaches e times what you started with.", width=11, size=26, color=th.BODY).move_to([0, -0.4, 0])
        ev = M(r"e = 2.718281828\ldots", size=52, color=th.MINT).move_to([0, -2.0, 0])
        with self.say("Imagine a bank that pays one hundred percent interest a year. Compound it twice a year and you get one point five squared, two point two five. Monthly, more. Daily, more still. Yet however often you compound, it never runs away. It approaches a fixed number: e."):
            self.play(FadeIn(h))
            self.add(rd)
            self.play(FadeIn(story))
            self.play(n.animate.set_value(2), run_time=0.8)
            self.play(n.animate.set_value(12), run_time=1.0)
            self.play(n.animate.set_value(365), run_time=1.2)
            self.play(n.animate.set_value(100000), run_time=1.5, rate_func=rate_functions.ease_in_quad)
            self.play(Write(ev))
        self.play(FadeOut(VGroup(h, story, ev)), FadeOut(rd))
        self.remove(rd)
        h = P.head(self, "The series for e, and 2 < e < 3")
        st = VGroup(M(r"\left(1+\tfrac1n\right)^n = 1 + 1 + \frac{1}{2!}\left(1-\tfrac1n\right) + \frac{1}{3!}\left(1-\tfrac1n\right)\left(1-\tfrac2n\right) + \cdots", size=36),
                    M(r"n \to \infty:\quad e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots = \sum_{r=0}^{\infty}\frac{1}{r!}", size=40, color=th.MINT),
                    M(r"e > 1 + 1 = 2;\quad r! > 2^{r-1}\ (r \ge 3) \Rightarrow e < 1 + \left(1 + \tfrac12 + \tfrac14 + \cdots\right) = 3", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.6, 0])
        for s_ in st:
            if s_.width > 12.6:
                s_.scale_to_fit_width(12.6)
        says = ["Expand one plus one over n to the n with the binomial theorem, and divide each factor of n in the numerators by an n from the denominator.", "As n grows, every bracket one minus k over n tends to one. So e is one plus one over one factorial plus one over two factorial, and so on: the sum of one over r factorial.",
                "Every term is positive, and the first two make two, so e is more than two. And from three on, r factorial is bigger than two to the r minus one, so the series is less than one plus a geometric series that sums to two: e is less than three."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        nl = NumberLine(x_range=[0, 3, 0.5], length=11, color=th.MUTED, include_numbers=True, font_size=24, decimal_number_config={"num_decimal_places": 1}).move_to([0, -2.4, 0])
        em = VGroup(DashedLine(nl.n2p(np.e) + UP * 0.75, nl.n2p(np.e) + DOWN * 0.15, color=th.MINT), M("e", size=32, color=th.MINT).next_to(nl.n2p(np.e) + UP * 0.75, UP, buff=0.05))
        from math import factorial
        bars, x0 = VGroup(), 0.0
        for r in range(8):
            w = 1 / factorial(r)
            bars.add(Rectangle(width=nl.n2p(x0 + w)[0] - nl.n2p(x0)[0], height=0.32, stroke_width=1, stroke_color=th.BG, fill_color=[th.AMBER, th.SKY][r % 2], fill_opacity=0.9).move_to(nl.n2p(x0 + w / 2) + UP * 0.3))
            x0 += w
        tot = ValueTracker(0)
        rd = always_redraw(lambda: VGroup(T("sum so far:", size=24, color=th.MUTED), DecimalNumber(tot.get_value(), num_decimal_places=5, font_size=34, color=th.AMBER)).arrange(RIGHT, buff=0.2).move_to([-3.8, -1.5, 0]))
        with self.say("Watch the terms pile up on a number line: one, then one more, a half, a sixth, a twenty fourth. Each is much smaller than the last, and after eight terms the total already agrees with e to four decimal places: two point seven one eight three.") as v:
            self.play(Create(nl), FadeIn(em))
            self.add(rd)
            acc = 0.0
            for r, b in enumerate(bars):
                acc += 1 / factorial(r)
                self.play(GrowFromEdge(b, LEFT), tot.animate.set_value(acc), run_time=max(0.35, 0.9 - 0.08 * r))
        self.play(FadeOut(VGroup(h, st, nl, em, bars)), FadeOut(rd))
        self.remove(rd)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "Three standard series")
        s = VGroup(M(r"e^x = 1 + \frac{x}{1!} + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots \quad (\text{all } x)", size=38),
                   M(r"a^x = e^{x\log a} = 1 + \frac{x\log a}{1!} + \frac{(x\log a)^2}{2!} + \cdots", size=38),
                   M(r"\log(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \quad (-1 < x \le 1)", size=38),
                   M(r"\log\frac{1+x}{1-x} = 2\left(x + \frac{x^3}{3} + \frac{x^5}{5} + \cdots\right) \quad (|x| < 1)", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.1, 0])
        says = ["The exponential series: e to the x is the sum of x to the r over r factorial, and it works for every x.", "Any a to the x becomes an exponential, because a is e to the log a.",
                "The logarithmic series, log of one plus x, alternates, and only works from minus one up to one.", "Replace x by minus x and subtract, and you get a much faster series for log of one plus x over one minus x."]
        self.play(FadeIn(h))
        for s_, sy in zip(s, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.2)
        nt = T("In NEB work, log with no base means logₑ (also written ln).", size=24, color=th.MUTED).move_to([0, -3.0, 0])
        self.play(FadeIn(nt))
        self.wait(1)
        self.play(FadeOut(VGroup(h, s, nt)))
        P.worked(self, "Find the sum of 1/1! + 2/2! + 3/3! + 4/4! + …",
                 [r"\frac{n}{n!} = \frac{n}{n\,(n-1)!} = \frac{1}{(n-1)!}", r"\Rightarrow \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!} + \cdots = e"],
                 ["Summing a series.", "Cancel one n: the general term n over n factorial is one over n minus one factorial.", "So the series is one over zero factorial, plus one over one factorial, and so on: exactly e."])
        P.worked(self, "Show 1 + 1/2! + 1/4! + 1/6! + … = (e + e⁻¹)/2 and evaluate it.",
                 [r"e + e^{-1} = 2\left(1 + \frac{1}{2!} + \frac{1}{4!} + \cdots\right)", r"\frac{e + e^{-1}}{2} = \frac{2.718282 + 0.367879}{2} = 1.5431"],
                 ["Even factorials.", "Add the series for e and e to the minus one: odd terms cancel, even ones double.", "Halve it: one point five four three one."])
        P.worked(self, "Compute logₑ 2 correct to four decimal places.",
                 [r"\frac{1+x}{1-x} = 2 \Rightarrow x = \tfrac13", r"\log 2 = 2\left(\tfrac13 + \tfrac{1}{3\cdot3^3} + \tfrac{1}{5\cdot3^5} + \tfrac{1}{7\cdot3^7}\right)", r"= 2(0.346567) = 0.6931"],
                 ["Log two. Putting x equal to one in the first log series crawls; you would need thousands of terms. Use the fast one instead.", "Choose x so that one plus x over one minus x is two: x is a third.", "Four terms.", "Zero point six nine three one. The true value is zero point six nine three one four seven."])
        self.quiz("The validity condition for 1/√(1 + 3x) is",
                  ["|x| < 1", "|x| < 3", "|x| < 1/3", "all x"], 2,
                  "Pause and think. One plus three x to the minus half. When is it valid?",
                  "x less than a third in size, because the quantity in the bracket is three x, and that must be less than one. Absolute x less than one is the trap: it ignores the three.")
        self.quiz("The number of terms in the expansion of (a + b)¹⁰ is",
                  ["10", "11", "9", "20"], 1,
                  "One more. How many terms in a plus b to the ten?",
                  "Eleven. r runs from zero to ten. Ten is the trap: it forgets the r equals zero term.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "(a + b)ⁿ = Σ ⁿCᵣ aⁿ⁻ʳ bʳ: n + 1 terms; proved by induction with Pascal's rule.",
            "Tᵣ₊₁ = ⁿCᵣ aⁿ⁻ʳ bʳ; collect powers of x and equate for any particular term.",
            "Σ ⁿCᵣ = 2ⁿ; alternating sum = 0; sum of coefficients: put variables = 1.",
            "Any index: (1 + x)ⁿ = 1 + nx + n(n−1)x²/2! + …, valid for |x| < 1. Factor out constants first.",
            "e = Σ 1/r! = 2.71828…; eˣ = Σ xʳ/r!; log(1 + x) = x − x²/2 + x³/3 − …",
        ], "Quick recap. The binomial theorem gives n plus one terms with coefficients n C r. The general term is T r plus one. The coefficients sum to two to the n. For any index the series is infinite and needs x less than one in size. Approximate roots by splitting off the nearest perfect power. And e is the sum of one over r factorial.")
        self.outro("That was the binomial theorem. Next, complex numbers: polar form, De Moivre's theorem, and the cube roots of unity. See you there.")
