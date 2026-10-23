import os
import sys
from math import factorial

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

DOT_A = th.AMBER
DOT_B = th.CORAL


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 4
    TITLE = "Sequence and Series"
    SUBTITLE = "Sums you never have to add"
    SECTIONS = ["Sum of the first n natural numbers", "Sums of squares and cubes", "Mathematical induction", "Exponential and logarithmic series"]
    NEXT = "Unit 5 · Matrix Based System of Linear Equations"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        q = M(r"1 + 2 + 3 + \cdots + 100 = \ ?", size=48).move_to([0, 2.4, 0])
        top = VGroup(*[T(str(k), size=30, color=DOT_A, weight="BOLD") for k in range(1, 11)]).arrange(RIGHT, buff=0.55).move_to([0, 1.0, 0])
        bot = VGroup(*[T(str(k), size=30, color=th.SKY, weight="BOLD") for k in range(10, 0, -1)])
        for b, t in zip(bot, top):
            b.move_to(t.get_center() + DOWN * 0.8)
        sums = VGroup(*[T("11", size=30, color=th.MINT, weight="BOLD").move_to(t.get_center() + DOWN * 1.7) for t in top])
        bar = Line(top.get_left() + DOWN * 1.25 + LEFT * 0.2, top.get_right() + DOWN * 1.25 + RIGHT * 0.2, color=th.MUTED)
        res = M(r"2S = 10 \times 11 \ \Rightarrow\ S = 55", size=40, color=th.MINT).move_to([0, -1.8, 0])
        res2 = M(r"1 + 2 + \cdots + 100 = \frac{100 \times 101}{2} = 5050", size=44, color=th.AMBER).move_to([0, -2.8, 0])
        with self.say("A schoolteacher once set a class a long, dull task: add every number from one to a hundred. One boy, Carl Gauss, had the answer in seconds."):
            self.play(Write(q))
        with self.say("Here is his trick, with one to ten. Write the numbers forwards, then backwards underneath. Every column adds to eleven. Ten columns of eleven is a hundred and ten, but that is the sum twice. So the sum is fifty five."):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in top], lag_ratio=0.08))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bot], lag_ratio=0.08))
            self.play(Create(bar), LaggedStart(*[FadeIn(s_, scale=1.4) for s_ in sums], lag_ratio=0.08))
            self.play(Write(res))
        with self.say("For one to a hundred: a hundred columns of a hundred and one, halved. Five thousand and fifty. In this unit you will find formulas like this for sums of squares and cubes, prove them for every n at once, and meet two series that never end but still add up."):
            self.play(Write(res2))
            nb = P.neby_in(self, "laugh", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(q, top, bot, sums, bar, res, res2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 4: Sequence and Series."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four parts. The sum of the first n natural numbers and sigma notation. Sums of squares and cubes, and a method for any series with a polynomial term. Proof by mathematical induction. And the exponential and logarithmic series.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Sigma: shorthand for 'add up'")
        sg = M(r"\sum_{k=1}^{n} t_k = t_1 + t_2 + t_3 + \cdots + t_n", size=46).move_to([0, 1.7, 0])
        ex = M(r"\sum_{k=1}^{5} k^2", size=46, color=th.AMBER).move_to([-3.6, 0.0, 0])
        k = ValueTracker(1)
        terms = VGroup(*[M(f"{j}^2", size=40) for j in range(1, 6)])
        row = VGroup()
        for i, t_ in enumerate(terms):
            row.add(t_)
            if i < 4:
                row.add(M("+", size=40))
        row.arrange(RIGHT, buff=0.18).move_to([1.4, 0.0, 0])
        eq = M(r"= 1 + 4 + 9 + 16 + 25 = 55", size=40, color=th.MINT).move_to([1.4, -1.0, 0])
        dm = para("k is a dummy letter: Σ k² and Σ r² from 1 to 5 are the same number, 55.", width=11, size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("The capital Greek letter sigma means add up. Below it, where the counter k starts; on top, where it stops; on the right, the term to add each time."):
            self.play(FadeIn(h), Write(sg))
        with self.say("Sigma k squared, k from one to five: put k equal to one, two, three, four, five in turn and add. Fifty five. The letter k is only a counter, a dummy: use r instead and nothing changes.") as v:
            self.play(Write(ex))
            for i in range(5):
                self.play(FadeIn(row[2 * i], shift=DOWN * 0.2), *([FadeIn(row[2 * i - 1])] if i else []), run_time=0.45)
            self.play(Write(eq))
            self.play(FadeIn(dm))
        self.play(FadeOut(VGroup(sg, ex, row, eq, dm)))
        rules = VGroup(M(r"\sum (a_k \pm b_k) = \sum a_k \pm \sum b_k", size=40), M(r"\sum c\,a_k = c \sum a_k, \qquad \sum_{k=1}^{n} c = nc", size=40),
                       M(r"\sum a_k b_k \ne \left(\sum a_k\right)\left(\sum b_k\right)", size=40, color=th.CORAL)).arrange(DOWN, buff=0.5).move_to([0, 0.2, 0])
        says = ["Two rules, used in every question in this unit. Sigma splits over a sum or difference.", "A constant comes out in front. And a constant on its own, added n times, gives n times the constant.",
                "But there is no rule for a product. The sum of a k b k is not the product of the two sums."]
        for r_, sy in zip(rules, says):
            with self.say(sy):
                self.play(Write(r_), run_time=1.1)
        self.play(FadeOut(VGroup(h, rules)))
        self.p1_triangle()

    def p1_triangle(self):
        h = P.head(self, "Two triangles make a rectangle")
        n, s = 6, 0.55
        org = np.array([-5.2, -2.3, 0])
        A = VGroup(*[Dot(org + np.array([j * s, (n - i) * s, 0]), radius=0.11, color=DOT_A) for i in range(1, n + 1) for j in range(i)])
        B = VGroup(*[Dot(org + np.array([j * s, (n - i) * s, 0]), radius=0.11, color=DOT_B) for i in range(1, n + 1) for j in range(i, n + 1)])
        Bstart = B.copy().shift(RIGHT * 4.6)
        Bstart.rotate(PI)
        brace_h = Brace(VGroup(*[d for d in A] + [d for d in B]), LEFT, color=th.MUTED)
        lh = M("n", size=32, color=th.MUTED).next_to(brace_h, LEFT, buff=0.1)
        brace_w = Brace(VGroup(*[d for d in A] + [d for d in B]), UP, color=th.MUTED)
        lw = M("n+1", size=32, color=th.MUTED).next_to(brace_w, UP, buff=0.1)
        f = VGroup(M(r"1 + 2 + \cdots + 6 = 21", size=38, color=DOT_A), M(r"2S = n(n+1)", size=40), M(r"\sum_{k=1}^{n} k = \frac{n(n+1)}{2}", size=50, color=th.MINT)).arrange(DOWN, buff=0.45).move_to([3.4, 0.0, 0])
        with self.say("Here is the same trick as a picture. Stack one dot, two dots, three, up to six: a triangle of twenty one dots."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(d, scale=1.5) for d in A], lag_ratio=0.03))
            self.play(Write(f[0]))
        with self.say("Make a copy, turn it upside down, and slide it in. The two triangles lock together into a rectangle, n rows by n plus one columns."):
            self.play(FadeIn(Bstart))
            self.play(Transform(Bstart, B), run_time=1.8)
            self.play(GrowFromCenter(brace_h), FadeIn(lh), GrowFromCenter(brace_w), FadeIn(lw))
        with self.say("So twice the sum is n times n plus one, and the sum of the first n natural numbers is n into n plus one, over two. These are the triangular numbers: one, three, six, ten, and so on."):
            self.play(Write(f[1]))
            self.play(Write(f[2]))
        self.play(FadeOut(VGroup(h, A, Bstart, brace_h, lh, brace_w, lw, f)))
        P.worked(self, "Find (a) 51 + 52 + … + 100, and (b) the sum of the first n odd natural numbers.",
                 [r"\text{(a) } \sum_{51}^{100} k = \sum_{1}^{100} k - \sum_{1}^{50} k = 5050 - 1275 = 3775", r"\text{(b) } \sum_{k=1}^{n} (2k - 1) = 2\cdot\frac{n(n+1)}{2} - n = n^2"],
                 ["Two quick ones.", "For a sum that starts part way along, take the full sum to a hundred and subtract the sum to fifty: five thousand and fifty minus twelve seventy five, three thousand seven hundred and seventy five.",
                  "The k th odd number is two k minus one. Split with the sigma rules: twice the sum of k, minus n. That is n squared. One plus three plus five plus seven is sixteen, four squared. Check."])
        P.worked(self, "How many consecutive natural numbers, starting from 1, add up to 465?",
                 [r"\frac{n(n+1)}{2} = 465 \Rightarrow n^2 + n - 930 = 0", r"n = \frac{-1 \pm \sqrt{3721}}{2} = \frac{-1 \pm 61}{2} = 30 \ \text{or}\ -31", r"n = 30"],
                 ["Work backwards from a total.", "Set n into n plus one over two equal to four sixty five.", "Solve the quadratic: root of three seven two one is sixty one. So n is thirty or minus thirty one.",
                  "A count of terms cannot be negative: thirty. And if no positive whole-number root appears, the answer is that no such n exists. Never round."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Squares by telescoping")
        idt = M(r"(k+1)^3 - k^3 = 3k^2 + 3k + 1", size=42, color=th.AMBER).move_to([0, 2.2, 0])
        rows = []
        specs = [("2^3", "1^3", r"3(1)^2 + 3(1) + 1"), ("3^3", "2^3", r"3(2)^2 + 3(2) + 1"), ("4^3", "3^3", r"3(3)^2 + 3(3) + 1"), (None, None, None), ("(n+1)^3", "n^3", r"3n^2 + 3n + 1")]
        y = 1.45
        for a, b, c in specs:
            if a is None:
                r = M(r"\vdots", size=34).move_to([-2.4, y, 0])
                rows.append(r)
                y -= 0.45
                continue
            A_, mi, B_, eq, C_ = M(a, size=34), M("-", size=34), M(b, size=34), M("=", size=34), M(c, size=34)
            r = VGroup(A_, mi, B_, eq, C_).arrange(RIGHT, buff=0.16)
            r.shift(np.array([-2.4, y, 0]) - eq.get_center() + RIGHT * 0.0)
            r.shift(LEFT * (eq.get_center()[0] - 0.0))
            rows.append(r)
            y -= 0.55
        rows_g = VGroup(*rows)
        with self.say("For the sum of squares we use a beautiful trick called telescoping. Start from an identity: k plus one, cubed, minus k cubed, equals three k squared plus three k plus one."):
            self.play(FadeIn(h), Write(idt))
        with self.say("Write it out for k equal to one, two, three, all the way to n.") as v:
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.5)
        pairs = [(rows[0][0], rows[1][2]), (rows[1][0], rows[2][2])]
        strikes = VGroup(*[VGroup(Line(a.get_corner(DL), a.get_corner(UR), color=th.CORAL, stroke_width=4), Line(b.get_corner(DL), b.get_corner(UR), color=th.CORAL, stroke_width=4)) for a, b in pairs])
        keep = VGroup(SurroundingRectangle(rows[-1][0], color=th.MINT, buff=0.06), SurroundingRectangle(rows[0][2], color=th.MINT, buff=0.06))
        res = VGroup(M(r"(n+1)^3 - 1 = 3\sum k^2 + 3\sum k + n", size=34), M(r"\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}", size=42, color=th.MINT)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.45)
        with self.say("Now add all the lines. On the left, plus two cubed cancels minus two cubed, three cubed cancels three cubed, and so on down the column. Like a telescope folding shut, everything collapses except the last and the first: n plus one, cubed, minus one."):
            for st in strikes:
                self.play(Create(st), run_time=0.7)
            self.play(Create(keep))
        with self.say("On the right: three times the sum of squares, plus three times the sum of k, plus n. We already know the sum of k. Rearrange, and the sum of the first n squares is n, n plus one, two n plus one, over six."):
            self.play(Write(res[0]))
            self.play(Write(res[1]))
        self.play(FadeOut(VGroup(h, idt, rows_g, strikes, keep, res)))
        self.p2_cubes()

    def p2_cubes(self):
        h = P.head(self, "Cubes: the sum of cubes is a perfect square")
        u = 0.5
        org = np.array([-6.2, -3.0, 0])
        Tn = [0, 1, 3, 6, 10]
        cols = [th.SKY, th.CORAL, th.MINT, th.AMBER]

        def L(k):
            a, b = Tn[k - 1] * u, Tn[k] * u
            pts = [org + [a, 0, 0], org + [b, 0, 0], org + [b, b, 0], org + [0, b, 0], org + [0, a, 0], org + [a, a, 0]] if k > 1 else [org, org + [b, 0, 0], org + [b, b, 0], org + [0, b, 0]]
            return Polygon(*pts, stroke_color=th.INK, stroke_width=2, fill_color=cols[k - 1], fill_opacity=0.45)

        Ls = [L(k) for k in range(1, 5)]
        labs = [M(f"{k}^3 = {k ** 3}", size=26 if k > 1 else 20).move_to(org + np.array([(Tn[k] - 0.5 * (Tn[k] - Tn[k - 1])) * u, (Tn[k] - 0.5 * (Tn[k] - Tn[k - 1])) * u, 0])) for k in range(1, 5)]
        labs[0].next_to(Ls[0], RIGHT, buff=0.1)
        sides = VGroup(*[M(f"T_{k} = {Tn[k]}", size=24, color=th.MUTED).next_to(org + [Tn[k] * u, 0, 0], DOWN, buff=0.12) for k in (2, 3, 4)])
        f = VGroup(M(r"1^3 + 2^3 + 3^3 + 4^3 = 10^2 = 100", size=36, color=th.AMBER), M(r"\sum_{k=1}^{n} k^3 = \left[\frac{n(n+1)}{2}\right]^2", size=46, color=th.MINT),
                   M(r"= \frac{n^2(n+1)^2}{4}", size=40), para("The sum of the first n cubes is the square of the sum of the first n numbers.", width=6.2, size=24, color=th.INK)).arrange(DOWN, buff=0.4).move_to([3.4, -0.2, 0])
        with self.say("The cubes have a picture too. Take squares whose sides are the triangular numbers: one, three, six, ten. Each new square adds an L shaped strip."):
            self.play(FadeIn(h))
            for k in range(4):
                self.play(DrawBorderThenFill(Ls[k]), run_time=0.8)
            self.play(FadeIn(sides))
        with self.say("The strip added at stage two has area nine minus one, eight: two cubed. At stage three, thirty six minus nine, twenty seven: three cubed. At stage four, a hundred minus thirty six, sixty four: four cubed. So one plus eight plus twenty seven plus sixty four fills a ten by ten square."):
            for lb in labs:
                self.play(FadeIn(lb, scale=1.3), run_time=0.6)
            self.play(Write(f[0]))
        with self.say("In general the sum of the first n cubes is the square of n into n plus one over two: the square of the sum of the first n numbers. The same telescoping trick, with fourth powers, proves it algebraically."):
            for f_ in f[1:]:
                self.play(Write(f_), run_time=0.9)
        self.play(FadeOut(VGroup(h, *Ls, *labs, sides, f)))
        rows = [["sum", "formula", "denominator"], ["Σ k", "n(n + 1)/2", "2"], ["Σ k²", "n(n + 1)(2n + 1)/6", "6"], ["Σ k³", "n²(n + 1)²/4", "4"]]
        tb = P.table(rows, [2.2, 5.6, 2.8], row_h=0.72, size=28, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 1.2, 0])
        steps = P.bullets(["1. Write the k th term as a polynomial in k.", "2. Split with the sigma rules.", "3. Substitute the three standard sums.", "4. Factorise, then TEST on n = 1 or 2."], width=11, size=26).move_to([0, -1.8, 0])
        with self.say("The three standard sums. Memorise the denominators: two, six, four. They are the commonest slip under pressure.") as v:
            P.reveal_table(self, tb, v.dur * 0.8)
        with self.say("And the method for any series whose term is a polynomial: write the k th term, split it with sigma rules, substitute the three sums, factorise, and always test your answer on n equals one or two.") as v:
            P.reveal_list(self, steps, v.dur * 0.9)
        self.play(FadeOut(VGroup(tb, steps)))
        P.worked(self, "Find (a) 1² + 2² + … + 20² and (b) 1³ + 2³ + … + 15³.",
                 [r"\text{(a) } \frac{20 \cdot 21 \cdot 41}{6} = \frac{17220}{6} = 2870", r"\text{(b) } \left[\frac{15 \cdot 16}{2}\right]^2 = 120^2 = 14400"],
                 ["Direct substitution.", "Twenty, twenty one, forty one, over six: two thousand eight hundred and seventy.", "For the cubes, square the triangular number: fifteen times sixteen over two is a hundred and twenty; squared, fourteen thousand four hundred."])
        P.worked(self, "Find the sum to n terms of 1·2 + 2·3 + 3·4 + …, and the sum of the first 20 terms.",
                 [r"t_k = k(k+1) = k^2 + k", r"S_n = \frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2} = \frac{n(n+1)}{6}\left[(2n+1) + 3\right]", r"= \frac{n(n+1)(n+2)}{3}\qquad \text{test } n=2:\ \frac{2\cdot3\cdot4}{3} = 8 = 2 + 6\ \checkmark", r"S_{20} = \frac{20 \cdot 21 \cdot 22}{3} = 3080"],
                 ["The classic shape.", "The k th term is k times k plus one: k squared plus k.", "Sum each piece and take out the common factor n into n plus one over six.", "The bracket is two n plus four, so the sum is n, n plus one, n plus two, over three. Test with n equal to two: eight, and one times two plus two times three is eight.", "For twenty terms: three thousand and eighty."])
        P.worked(self, "Find 1² + 3² + 5² + … + (2n − 1)², and its value for n = 10.",
                 [r"t_k = (2k-1)^2 = 4k^2 - 4k + 1", r"S_n = \frac{4n(n+1)(2n+1)}{6} - \frac{4n(n+1)}{2} + n = \frac{n(4n^2 - 1)}{3}", r"= \frac{n(2n-1)(2n+1)}{3};\qquad S_{10} = \frac{10\cdot19\cdot21}{3} = 1330"],
                 ["Squares of odd numbers.", "The k th odd number is two k minus one; square it.", "Split, substitute and simplify: n times four n squared minus one, over three.", "Factorise the difference of squares. For n equal to ten: thirteen hundred and thirty."])
        P.worked(self, "Find 11³ + 12³ + … + 20³.",
                 [r"\sum_{11}^{20} k^3 = \sum_{1}^{20} k^3 - \sum_{1}^{10} k^3", r"= 210^2 - 55^2 = 44100 - 3025 = 41075"],
                 ["A sum that starts part way along.", "Subtract the sum up to ten from the sum up to twenty. Up to ten, not eleven: eleven cubed must stay in.", "Two hundred and ten squared minus fifty five squared: forty one thousand and seventy five."])
        self.tip("For Σ from m to n, use Σ(1 to n) − Σ(1 to m − 1). Subtract up to m − 1, not m, or you throw away the first term you wanted.",
                 "Exam tip. To sum from m to n, subtract the sum up to m minus one from the sum up to n. Subtract up to m itself and you throw away a term you were meant to keep.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Induction: the domino argument")
        n = 8
        ground = Line([-6.4, -1.2, 0], [6.4, -1.2, 0], color=th.MUTED, stroke_width=3)
        dom = VGroup(*[Rectangle(width=0.32, height=1.6, stroke_color=th.INK, stroke_width=2, fill_color=th.AMBER if i < 3 else th.MINT, fill_opacity=0.55).move_to([-5.2 + 1.25 * i, -0.4, 0]) for i in range(n)])
        names = ["P(1)", "P(2)", "P(3)", "…", "P(k)", "P(k+1)", "…", ""]
        nl = VGroup(*[T(nm, size=22, color=th.INK).next_to(d, DOWN, buff=0.15) for nm, d in zip(names, dom)])
        hand = Arrow(dom[0].get_left() + LEFT * 1.0 + UP * 0.5, dom[0].get_left() + UP * 0.5, buff=0.05, color=th.CORAL, stroke_width=6)
        steps = VGroup(T("1. Basis: P(1) is true  (push the first domino)", size=26, color=th.AMBER), T("2. Step: P(k) true ⇒ P(k+1) true  (each domino knocks the next)", size=26, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 2.0, 0])
        with self.say("Checking a formula for n equal to one, two and three proves nothing about n equal to forty. Induction proves it for every natural number at once. Think of an endless row of dominoes."):
            self.play(FadeIn(h), Create(ground), LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in dom], lag_ratio=0.08), FadeIn(nl))
        with self.say("Two things make them all fall. First, the basis: push the first one, so P of one is true. Second, the inductive step: the dominoes are close enough that whenever one falls, it knocks over the next. P of k true forces P of k plus one true."):
            self.play(FadeIn(steps[0]), GrowArrow(hand))
            self.play(FadeIn(steps[1]))
        tilt = -np.arcsin(1.25 / 1.6) * 0.98
        with self.say("Watch. Push the first, and each one topples the next, all the way along. Leave out either step and the row stays standing."):
            for i in range(n):
                pivot = dom[i].get_corner(DR)
                ang = tilt if i < n - 1 else -PI / 2 * 0.98
                self.play(Rotate(dom[i], ang, about_point=pivot), run_time=0.35, rate_func=rate_functions.ease_in_quad)
        self.play(FadeOut(VGroup(h, ground, dom, nl, hand, steps)))
        mem = P.bullets(["1. Let P(n) be the statement …", "2. Basis: for n = 1, LHS = … = RHS, so P(1) is true.", "3. Assume P(k) is true, i.e. …   (the inductive hypothesis)",
                         "4. Then … = the formula with k + 1, so P(k + 1) is true. Hence, by the principle of mathematical induction, P(n) holds for every natural number n."], width=11.5, size=26).move_to([0, 0.2, 0])
        hd = T("Four lines every induction proof must contain", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("Examiners give marks for the layout itself, so learn these four lines. Name the statement. Prove the basis. Assume it for k, and say the words inductive hypothesis. Then prove it for k plus one, and write the conclusion.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, mem, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, mem)))
        P.worked(self, "Prove by induction: 1³ + 2³ + … + n³ = n²(n + 1)²/4.",
                 [r"\textbf{Basis: } n=1:\ \text{LHS} = 1,\ \text{RHS} = \tfrac{1\cdot4}{4} = 1 \ \checkmark", r"\textbf{Assume } 1^3 + \cdots + k^3 = \tfrac{k^2(k+1)^2}{4}",
                  r"1^3 + \cdots + k^3 + (k+1)^3 = \tfrac{k^2(k+1)^2}{4} + (k+1)^3 = \tfrac{(k+1)^2\left[k^2 + 4k + 4\right]}{4}", r"= \tfrac{(k+1)^2(k+2)^2}{4}:\ \text{the formula for } k+1.\ \text{True for all } n."],
                 ["The cube formula, by induction.", "Basis: both sides are one.", "Assume it is true for k. That is the inductive hypothesis.", "Add the next term, k plus one cubed, to both sides, and replace the first k terms by the assumed formula. Take out k plus one squared over four: the bracket is k squared plus four k plus four.",
                  "That is k plus two, squared. Exactly the formula with k plus one in place of n. So by induction it holds for all n."])
        P.worked(self, "Prove by induction that 3²ⁿ − 1 is divisible by 8.",
                 [r"n = 1:\ 3^2 - 1 = 8 \ \checkmark", r"\text{Assume } 3^{2k} - 1 = 8m \Rightarrow 3^{2k} = 8m + 1", r"3^{2(k+1)} - 1 = 9 \cdot 3^{2k} - 1 = 9(8m + 1) - 1 = 72m + 8 = 8(9m + 1)"],
                 ["Induction also proves divisibility.", "Basis: three squared minus one is eight.", "Assume three to the two k, minus one, is eight m for some whole number m. So three to the two k is eight m plus one.", "Then three to the two k plus two, minus one, is nine times that, minus one: seventy two m plus eight, which is eight times nine m plus one. Divisible by eight."])
        P.worked(self, "Prove by induction: 1/(1·2) + 1/(2·3) + … + 1/(n(n + 1)) = n/(n + 1).",
                 [r"n=1:\ \tfrac12 = \tfrac12\ \checkmark", r"\frac{k}{k+1} + \frac{1}{(k+1)(k+2)} = \frac{k(k+2) + 1}{(k+1)(k+2)} = \frac{(k+1)^2}{(k+1)(k+2)}", r"= \frac{k+1}{k+2}\ \checkmark"],
                 ["One with fractions.", "Basis: a half equals a half.", "Assume the sum to k terms is k over k plus one, and add the next term. Over a common denominator the top is k squared plus two k plus one: k plus one, squared.", "Cancel, and you get k plus one over k plus two: the formula for k plus one."])
        c = self.callout("careful", "The inductive step is NOT 'put k + 1 into the formula'. You must USE the hypothesis: split off the last term and replace the first k terms by the assumed formula. No basis step: at most half marks.", width=11, size=26)
        with self.say("The classic mistake: rewriting the right hand side with k plus one and calling it done. That proves nothing. You must use the hypothesis. And a proof without the basis step loses half the marks."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("In a proof by induction, the step proved first is",
                  ["P(k + 1)", "P(k)", "P(1)", "P(n) for all n"], 2,
                  "Pause and think. Which step comes first?",
                  "P of one, the basis step. Without it there is no first domino, and nothing ever falls.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Partial sums of eˣ = 1 + x + x²/2! + …")
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-1, 8, 2], x_length=7.0, y_length=4.8, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-2.2, -0.6, 0])
        true = P.clipped(ax, np.exp, -2.5, 2.5, -1, 8, WHITE, width=5)
        k = ValueTracker(1)
        part = always_redraw(lambda: P.clipped(ax, lambda x: sum(x ** j / factorial(j) for j in range(int(k.get_value()))), -2.5, 2.5, -1, 8, th.AMBER))
        lab = always_redraw(lambda: T(f"{int(k.get_value())} term{'s' if int(k.get_value()) > 1 else ''}", size=28, color=th.AMBER).move_to([4.2, 1.8, 0]))
        f = VGroup(M(r"e^x = \sum_{r=0}^{\infty}\frac{x^r}{r!}", size=40, color=th.MINT), T("valid for EVERY real x", size=24, color=th.MINT), M(r"a^x = e^{x\log a}", size=36)).arrange(DOWN, buff=0.3).move_to([4.2, -0.6, 0])
        with self.say("Unit two built the exponential series from the limit for e. Here it is at work. The white curve is e to the x. One term of the series is a flat line; two terms a straight line; three a parabola. Each new term bends the yellow curve closer, and by six or seven terms it hugs e to the x across the whole picture."):
            self.play(FadeIn(h), Create(ax), Create(true))
            self.add(part, lab)
            for j in range(2, 8):
                self.play(k.animate.set_value(j), run_time=0.9)
            self.play(FadeIn(f))
        self.play(FadeOut(VGroup(h, ax, true, f)), FadeOut(part), FadeOut(lab))
        self.remove(part, lab)
        h = P.head(self, "log(1 + x) = x − x²/2 + x³/3 − …   (−1 < x ≤ 1)")
        ax1 = Axes(x_range=[0, 13, 2], y_range=[0, 1.1, 0.25], x_length=5.4, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([-3.3, -0.5, 0])
        ax2 = Axes(x_range=[0, 13, 2], y_range=[-8, 0, 2], x_length=5.4, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([3.3, -0.5, 0])
        S1, S2, a, b = [], [], 0.0, 0.0
        for r in range(1, 13):
            a += (-1) ** (r - 1) / r
            b += (-1) ** (r - 1) * (-1.2) ** r / r
            S1.append(a)
            S2.append(b)
        d1 = VGroup(*[Dot(ax1.c2p(r + 1, v), radius=0.07, color=th.AMBER) for r, v in enumerate(S1)])
        d2 = VGroup(*[Dot(ax2.c2p(r + 1, v), radius=0.07, color=th.CORAL) for r, v in enumerate(S2)])
        ln2 = DashedLine(ax1.c2p(0, np.log(2)), ax1.c2p(13, np.log(2)), color=th.MINT)
        t1 = VGroup(M(r"x = 1", size=30, color=th.AMBER), M(r"\to \log 2 = 0.6931", size=28, color=th.MINT)).arrange(RIGHT, buff=0.2).next_to(ax1, UP, buff=0.2)
        t2 = VGroup(M(r"x = -1.2", size=30, color=th.CORAL), T("terms grow: no sum", size=24, color=th.CORAL)).arrange(RIGHT, buff=0.2).next_to(ax2, UP, buff=0.2)
        xl = VGroup(T("terms used", size=20, color=th.MUTED).next_to(ax1, DOWN, buff=0.35), T("terms used", size=20, color=th.MUTED).next_to(ax2, DOWN, buff=0.35))
        with self.say("The logarithmic series behaves differently: it only works for x between minus one and one, including one. At x equal to one the partial sums zig zag, above and below, closing in on log two. At x equal to minus one point two the terms grow and the sums run away: no sum at all. That is why the condition must always be stated."):
            self.play(FadeIn(h), Create(ax1), Create(ax2), FadeIn(xl))
            self.play(Create(ln2), FadeIn(t1), FadeIn(t2))
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in d1], lag_ratio=0.15), LaggedStart(*[FadeIn(d, scale=1.5) for d in d2], lag_ratio=0.15), run_time=3.5)
        self.play(FadeOut(VGroup(h, ax1, ax2, d1, d2, ln2, t1, t2, xl)))
        P.worked(self, "Sum (a) 1 + 1/2! + 1/3! + 1/4! + … and (b) 1/1! + 1/3! + 1/5! + …",
                 [r"\text{(a) } e = 1 + \tfrac{1}{1!} + \tfrac{1}{2!} + \cdots \Rightarrow \text{sum} = e - 1 = 1.71828", r"\text{(b) } e - e^{-1} = 2\left(\tfrac{1}{1!} + \tfrac{1}{3!} + \tfrac{1}{5!} + \cdots\right)",
                  r"\text{sum} = \frac{e - e^{-1}}{2} = \frac{2.71828 - 0.36788}{2} = 1.17520"],
                 ["Recognise the series.", "The first is the series for e with its leading one removed: e minus one.", "For the second, write e and e to the minus one. Subtracting kills the even terms and doubles the odd ones.", "So the sum is e minus e to the minus one, over two: one point one seven five two."])
        P.worked(self, "Using log((1 + x)/(1 − x)) = 2(x + x³/3 + x⁵/5 + …), find log 1.2 to four decimal places.",
                 [r"\frac{1+x}{1-x} = \frac65 \Rightarrow 5 + 5x = 6 - 6x \Rightarrow x = \frac{1}{11}", r"\log 1.2 = 2\left(\tfrac{1}{11} + \tfrac{1}{3\cdot11^3} + \tfrac{1}{5\cdot11^5} + \cdots\right)", r"= 2(0.0909091 + 0.0002502 + 0.0000012) = 0.1823"],
                 ["A fast-converging series.", "Choose x so that one plus x over one minus x is one point two: x is one eleventh.", "Small x, so the terms shrink fast.", "Three terms give point one eight two three."])
        c = self.callout("careful", "In this unit log means the NATURAL logarithm, logₑ. Read it as base 10 and every series is wrong by a factor of 0.4343.", width=11, size=26)
        with self.say("And remember: here log means the natural logarithm, base e. Read it as base ten and every answer is off by a factor."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("The value of 1³ + 2³ + … + 10³ is",
                  ["385", "2025", "3025", "5050"], 2,
                  "Pause and think. The sum of the first ten cubes.",
                  "Three thousand and twenty five: the square of fifty five. Three eighty five is the sum of the squares, and five thousand and fifty belongs to Gauss.")
        self.quiz("1 + 1/1! + 1/2! + 1/3! + … equals",
                  ["e", "e − 1", "e + 1", "e⁻¹"], 2,
                  "One more. Careful with the first term.",
                  "e plus one. The series for e already starts one plus one over one factorial; this one has an extra one in front.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Σk = n(n + 1)/2,  Σk² = n(n + 1)(2n + 1)/6,  Σk³ = [n(n + 1)/2]²: denominators 2, 6, 4.",
            "Any polynomial term: write tₖ, split with the sigma rules, substitute, factorise, test on n = 1.",
            "From m to n: Σ(1…n) − Σ(1…m − 1).",
            "Induction: state P(n), prove P(1), ASSUME P(k), use it to prove P(k + 1), conclude.",
            "eˣ = Σ xʳ/r! for all x;  log(1 + x) = x − x²/2 + … for −1 < x ≤ 1 (log = logₑ).",
        ], "Quick recap. The three standard sums, with denominators two, six and four. Any polynomial term: split, substitute, factorise, test. For a part sum, subtract up to m minus one. Induction needs a basis and a step that uses the hypothesis. And the exponential series works for every x, while the log series needs x between minus one and one.")
        self.outro("That was sequence and series. Next, matrices: solving systems of linear equations with determinants and inverses. See you there.")
