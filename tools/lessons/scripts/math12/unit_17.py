import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402


def plot_axes(center, xr, yr, w, h, nums=True, size=18):
    return Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, tips=False,
                axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": nums, "font_size": size}).move_to(center)


def cayley(heads, op, size=30, cell=0.62, hl=None):
    """Composition table: header row and column, entries op(a, b). Returns group with .cells[i][j] (0-based over elements)."""
    n = len(heads)
    g = VGroup()
    cells = []
    sym = M(r"\ast", size=size, color=th.MUTED).move_to([0, 0, 0])
    g.add(sym)
    for j, hj in enumerate(heads):
        g.add(M(str(hj), size=size, color=th.AMBER).move_to([(j + 1) * cell * 1.3, 0, 0]))
    for i, hi in enumerate(heads):
        g.add(M(str(hi), size=size, color=th.AMBER).move_to([0, -(i + 1) * cell, 0]))
        row = []
        for j, hj in enumerate(heads):
            e = M(str(op(hi, hj)), size=size, color=th.INK).move_to([(j + 1) * cell * 1.3, -(i + 1) * cell, 0])
            g.add(e)
            row.append(e)
        cells.append(row)
    w = (n + 0.5) * cell * 1.3
    g.add(Line([cell * 0.65, cell * 0.45, 0], [cell * 0.65, -(n + 0.5) * cell, 0], color=th.MUTED, stroke_width=2),
          Line([-cell * 0.5, -cell * 0.5, 0], [w + 0.1, -cell * 0.5, 0], color=th.MUTED, stroke_width=2))
    g.cells = cells
    return g


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 17
    TITLE = "Appendix: Retained Topics"
    SUBTITLE = "Groups, Rolle and the Mean Value Theorem, numerical integration"
    SECTIONS = ["Binary operations and groups", "Cayley tables", "Rolle's theorem", "The Mean Value Theorem", "Numerical integration (revision)"]
    NEXT = "Class 12 English"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        clock = Circle(radius=1.8, stroke_color=th.INK, stroke_width=4).move_to([-3.4, -0.2, 0])
        marks = VGroup(*[VGroup(Dot(clock.get_center() + 1.8 * np.array([np.sin(TAU * k / 4), np.cos(TAU * k / 4), 0]), color=th.AMBER), M(str(k), size=36, color=th.AMBER).move_to(clock.get_center() + 2.25 * np.array([np.sin(TAU * k / 4), np.cos(TAU * k / 4), 0]))) for k in range(4)])
        ang = ValueTracker(0)
        hand = always_redraw(lambda: Arrow(clock.get_center(), clock.get_center() + 1.5 * np.array([np.sin(ang.get_value()), np.cos(ang.get_value()), 0]), buff=0, color=th.MINT, stroke_width=6))
        eqs = VGroup(M(r"2 + 3 = 5 \equiv 1", size=40), M(r"3 + 1 = 4 \equiv 0", size=40), T("arithmetic that wraps round: Z₄", size=26, color=th.MUTED)).arrange(DOWN, buff=0.4).move_to([3.0, 0.6, 0])
        with self.say("A clock with only four hours: nought, one, two, three. Start at two and move on three: you land on one. Start at three, move on one: back to nought. Arithmetic that wraps round."):
            self.play(Create(clock), FadeIn(marks))
            self.add(hand)
            self.play(ang.animate.set_value(TAU / 2), run_time=0.8)
            self.play(ang.animate.set_value(TAU / 2 + 3 * TAU / 4), Write(eqs[0]), run_time=1.6)
            self.play(Write(eqs[1]), FadeIn(eqs[2]))
        with self.say("This little system obeys exactly the same rules as ordinary addition, and as rotations, and as multiplying by i. That shared pattern is called a group. It is one of three topics dropped from the timetable but still set in NEB papers, so this appendix covers them all."):
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(clock, marks, eqs)), FadeOut(hand))
        self.remove(hand)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 17: the appendix of retained topics."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Five parts. Binary operations and the group axioms. Building and reading Cayley tables. Rolle's theorem. The Mean Value Theorem. And a revision of numerical integration, as you would set it out in the exam.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Binary operation: closed on the set")
        ex = VGroup(VGroup(M(r"a + b \text{ on } \mathbb{N}", size=36), T("yes", size=28, color=th.MINT)).arrange(RIGHT, buff=0.5), VGroup(M(r"a - b \text{ on } \mathbb{N}", size=36), T("no: 3 − 5 = −2", size=28, color=th.CORAL)).arrange(RIGHT, buff=0.5),
                    VGroup(M(r"ab \text{ on } \mathbb{Z}", size=36), T("yes", size=28, color=th.MINT)).arrange(RIGHT, buff=0.5), VGroup(M(r"a / b \text{ on } \mathbb{Z}", size=36), T("no: 1 ÷ 2 = 0.5", size=28, color=th.CORAL)).arrange(RIGHT, buff=0.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.0, 0])
        with self.say("A binary operation combines two elements of a set and must give an answer inside the same set. Addition on the natural numbers: yes. Subtraction: no, three minus five escapes. Multiplication on the integers: yes. Division: no, one over two is not an integer. One counter example is enough."):
            self.play(FadeIn(h))
            for e_ in ex:
                self.play(FadeIn(e_, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeOut(VGroup(h, ex)))
        hd = T("The group axioms for (G, *)", size=30, weight="BOLD").to_edge(UP, buff=0.75)
        ax = P.bullets(["1. Closure: a * b is in G for all a, b in G.", "2. Associativity: (a * b) * c = a * (b * c).", "3. Identity: some e has a * e = e * a = a for every a.", "4. Inverse: every a has a⁻¹ with a * a⁻¹ = a⁻¹ * a = e.",
                        "Abelian if also a * b = b * a.  Finite or infinite by the number of elements (its order)."], width=11.5, size=27).move_to([0, -0.1, 0])
        with self.say("A group is a set with an operation satisfying four axioms. Closure. Associativity. An identity element that changes nothing. And an inverse for every element that brings it back to the identity. If the order of combining never matters, the group is abelian. Its order is the number of elements.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, ax, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, ax)))
        P.worked(self, "Show that (Z, +) is an infinite abelian group, but (N, +) is not a group.",
                 [r"\mathbb{Z}:\ \text{closed},\ \text{associative},\ e = 0,\ a^{-1} = -a,\ a + b = b + a", r"\mathbb{N}:\ 3 \text{ would need } -3 \notin \mathbb{N}:\ \text{the inverse axiom fails}"],
                 ["Integers and naturals.", "For the integers, all four axioms hold, it commutes, and it has infinitely many elements.", "For the natural numbers there is no negative to undo three. The inverse axiom fails, so it is not a group."])
        P.worked(self, "Prove that a group's identity is unique, and each element has exactly one inverse.",
                 [r"e, e' \text{ identities}:\ e' = e \ast e' = e", r"b, c \text{ inverses of } a:\ b = b \ast e = b \ast (a \ast c) = (b \ast a) \ast c = e \ast c = c"],
                 ["Two short proofs.", "If e and e dash are both identities, combine them: the result equals each, so they are equal.", "If b and c both undo a, use the identity, associativity, and the identity again: b equals c."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Cayley table of Z₄ under +₄")
        tb = cayley([0, 1, 2, 3], lambda a, b: (a + b) % 4, size=44, cell=0.85).move_to([-3.4, -0.4, 0])
        with self.say("A finite group is best shown in a Cayley table, like a multiplication table. Here is Z four, addition modulo four: the clock from the start."):
            self.play(FadeIn(h), FadeIn(tb))
        checks = VGroup(T("closure: every entry is in {0, 1, 2, 3}", size=24, color=th.INK), T("identity: the 0 row repeats the header", size=24, color=th.MINT), T("inverses: find the 0 in each row", size=24, color=th.AMBER),
                        T("abelian: symmetric about the diagonal", size=24, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.0, 0])
        cells = tb.cells
        with self.say("Read the axioms straight off the table. Every entry is in the set: closed. The row for nought simply repeats the header: nought is the identity."):
            self.play(FadeIn(checks[0]))
            self.play(*[c.animate.set_color(th.MINT) for c in cells[0]], FadeIn(checks[1]))
        with self.say("Find the identity in each row: one plus three, two plus two, three plus one. So the inverse of one is three, two is its own inverse. And the table is a mirror image across its diagonal: the group is abelian, of order four."):
            boxes = VGroup(*[SurroundingRectangle(cells[i][j], color=th.AMBER, buff=0.08) for i in range(4) for j in range(4) if (i + j) % 4 == 0])
            self.play(Create(boxes), FadeIn(checks[2]))
            diag = DashedLine(cells[0][0].get_center() + UL * 0.3, cells[3][3].get_center() + DR * 0.3, color=th.SKY)
            self.play(Create(diag), FadeIn(checks[3]))
        self.play(FadeOut(VGroup(h, tb, checks, boxes, diag)))
        h = P.head(self, "{1, −1, i, −i} under multiplication")
        names = ["1", "-1", "i", "-i"]
        vals = [1, -1, 1j, -1j]
        tostr = {1: "1", -1: "-1", 1j: "i", -1j: "-i"}
        tb = cayley(names, lambda a, b: tostr[vals[names.index(a)] * vals[names.index(b)]], size=40, cell=0.85).move_to([-3.4, -0.4, 0])
        f = VGroup(T("identity 1;  inverses: i ↔ −i,  1 and −1 self-inverse", size=24, color=th.AMBER), T("an abelian group of order 4, with the same shape as Z₄", size=24, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, 0.0, 0])
        with self.say("The four fourth roots of unity, one, minus one, i and minus i, under multiplication. Every product stays in the set; one is the identity; i and minus i are inverses. Another abelian group of order four. Remember the cold open: multiplying by i is a quarter turn, just like the four hour clock."):
            self.play(FadeIn(h), FadeIn(tb))
            self.play(FadeIn(f))
        self.play(FadeOut(VGroup(h, tb, f)))
        P.worked(self, "Show {1, 2, 3, 4} is a group under multiplication modulo 5; find each inverse.",
                 [r"2 \times_5 3 = 6 \equiv 1,\quad 4 \times_5 4 = 16 \equiv 1,\ \ldots\ \text{no entry is } 0", r"e = 1;\quad 1^{-1} = 1,\ 2^{-1} = 3,\ 3^{-1} = 2,\ 4^{-1} = 4", r"\text{(mod 6 fails: } 2 \times_6 3 = 0 \notin G)"],
                 ["Multiplication modulo five.", "Fill the table: every entry is one of one to four, never zero, because five is prime.", "One is the identity; find the ones in each row for the inverses: two and three undo each other, four undoes itself.", "With six instead of five, two times three gives nought, which escapes the set."])

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Rolle: equal heights ⇒ a flat tangent somewhere")
        ax = plot_axes([-2.4, -0.6, 0], [0.5, 3.5, 0.5], [-1.5, 1.0, 0.5], 6.0, 4.0)
        f = lambda x: x * x - 4 * x + 3
        cv = ax.plot(f, x_range=[0.6, 3.4], color=th.AMBER, stroke_width=4)
        ends = VGroup(Dot(ax.c2p(1, 0), color=th.SKY), Dot(ax.c2p(3, 0), color=th.SKY), M("f(1) = f(3) = 0", size=28, color=th.SKY).next_to(ax.c2p(2, 0), UP, buff=0.4))
        tl = Line(ax.c2p(1.4, -1), ax.c2p(2.6, -1), color=th.MINT, stroke_width=5)
        cond = P.bullets(["(i) f continuous on [a, b]", "(ii) f differentiable on (a, b)", "(iii) f(a) = f(b)", "⇒ some c in (a, b) has f′(c) = 0"], width=5, size=26).move_to([4.0, 0.6, 0])
        cond[3].set_color(th.MINT)
        with self.say("Rolle's theorem. If a smooth curve starts and ends at the same height, then somewhere in between its tangent is flat. Three conditions: continuous on the closed interval, differentiable inside it, and equal values at the ends. Then f dash of c is zero for some c strictly between."):
            self.play(FadeIn(h), Create(ax), Create(cv), FadeIn(ends))
            self.play(FadeIn(cond))
            self.play(Create(tl))
        ex = M(r"f(x) = x^2 - 4x + 3:\ f'(c) = 2c - 4 = 0 \Rightarrow c = 2 \in (1, 3)", size=30, color=th.MINT).to_edge(DOWN, buff=0.5)
        with self.say("For x squared minus four x plus three on one to three: both ends are zero, the polynomial is smooth, and f dash of c is zero at c equals two, inside the interval. Verified."):
            self.play(Write(ex))
        self.play(FadeOut(VGroup(h, ax, cv, ends, tl, cond, ex)))
        P.worked(self, "Verify Rolle's theorem for f(x) = x³ − 4x on [−2, 2].",
                 [r"f(-2) = -8 + 8 = 0 = f(2);\ \text{polynomial, so continuous and differentiable}", r"f'(c) = 3c^2 - 4 = 0 \Rightarrow c = \pm\frac{2}{\sqrt3} = \pm1.1547 \in (-2, 2)"],
                 ["Two flat points.", "Equal end values and a polynomial: the conditions hold.", "f dash is zero at plus or minus two over root three, both inside: Rolle promises at least one, not only one."])
        P.worked(self, "Why does Rolle's theorem fail for |x| on [−1, 1], and for 1/x on [−1, 1]?",
                 [r"|x|:\ \text{a corner at } 0,\ \text{not differentiable};\ f' = \pm1 \ne 0", r"1/x:\ \text{not defined, so not continuous, at } x = 0"],
                 ["When the conditions fail.", "The absolute value has a sharp corner at nought: no derivative there, and the slope is never zero.", "One over x is not even defined at nought, so it is not continuous."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Mean Value Theorem: some tangent is parallel to the chord")
        ax = plot_axes([-2.4, -0.6, 0], [0.5, 3.5, 0.5], [0, 10, 2], 6.0, 4.2)
        f = lambda x: x * x
        cv = ax.plot(f, x_range=[0.6, 3.2], color=th.AMBER, stroke_width=4)
        chord = Line(ax.c2p(1, 1), ax.c2p(3, 9), color=th.SKY, stroke_width=4)
        c = ValueTracker(1.1)
        tg = always_redraw(lambda: Line(ax.c2p(c.get_value() - 0.6, f(c.get_value()) - 1.2 * c.get_value()), ax.c2p(c.get_value() + 0.6, f(c.get_value()) + 1.2 * c.get_value()), color=th.MINT if abs(c.get_value() - 2) < 0.03 else th.FAINT, stroke_width=5))
        dt = always_redraw(lambda: Dot(ax.c2p(c.get_value(), f(c.get_value())), color=th.MINT, radius=0.09))
        f_ = VGroup(M(r"f'(c) = \frac{f(b) - f(a)}{b - a}", size=40, color=th.MINT), T("some tangent has the chord's slope", size=24, color=th.MUTED), M(r"x^2 \text{ on } [1, 3]:\ \frac{9 - 1}{2} = 4 = 2c \Rightarrow c = 2", size=30)).arrange(DOWN, buff=0.35).move_to([3.6, 0.2, 0])
        with self.say("Tilt Rolle's picture and you get the Mean Value Theorem. Join the ends of the curve with a chord. Somewhere in between, a tangent runs exactly parallel to that chord: f dash of c equals the chord's slope. If you drive sixty kilometres in an hour, at some instant your speedometer read exactly sixty."):
            self.play(FadeIn(h), Create(ax), Create(cv), Create(chord))
            self.add(tg, dt)
            self.play(c.animate.set_value(2.9), run_time=2.0)
            self.play(c.animate.set_value(2.0), run_time=1.5)
            self.play(Write(f_[0]), FadeIn(f_[1]))
        with self.say("For x squared on one to three, the chord's slope is eight over two, four. And two c equals four at c equals two."):
            self.play(Write(f_[2]))
        self.play(FadeOut(VGroup(h, ax, cv, chord, f_)), FadeOut(tg), FadeOut(dt))
        self.remove(tg, dt)
        self.tip("Write all three (or two) conditions in words, compute c, and STATE that c lies in the open interval. Rolle is the special case f(a) = f(b) of the MVT.",
                 "Exam tip. Write out the conditions, find c, and say that c lies inside the open interval. That last sentence is a mark.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "∫₁² dx/x with n = 4: the ordinate table")
        rows = [["i", "xᵢ", "yᵢ = 1/xᵢ", "weight T", "weight S"], ["0", "1.00", "1.000000", "1", "1"], ["1", "1.25", "0.800000", "2", "4"], ["2", "1.50", "0.666667", "2", "2"], ["3", "1.75", "0.571429", "2", "4"], ["4", "2.00", "0.500000", "1", "1"]]
        tb = P.table(rows, [0.8, 1.3, 2.2, 1.5, 1.5], row_h=0.6, size=26, colors=[th.MUTED, th.INK, th.MINT, th.SKY, th.AMBER]).move_to([-2.9, 0.2, 0])
        res = VGroup(M(r"T = \frac{h}{2}[\ldots] = 0.697024", size=34, color=th.SKY), M(r"S = \frac{h}{3}[\ldots] = 0.693254", size=34, color=th.AMBER), M(r"\ln 2 = 0.693147", size=36, color=th.MINT),
                     para("errors: 0.0039 (trapezium), 0.0001 (Simpson)", width=4.6, size=24, color=th.MUTED)).arrange(DOWN, buff=0.35)
        res.move_to([4.0, 0.2, 0])
        with self.say("Finally, numerical integration as you set it out in the exam. Integral one to two of one over x, with four strips, so h is a quarter. Make the ordinate table first. The trapezium rule weights the ends once and the rest twice. Simpson's rule weights them one, four, two, four, one.") as v:
            self.play(FadeIn(h))
            P.reveal_table(self, tb, v.dur * 0.8)
        with self.say("The trapezium rule gives point six nine seven; Simpson gives point six nine three two five. The true value, log two, is point six nine three one five. Simpson's error is about a fortieth of the trapezium's."):
            for r_ in res:
                self.play(Write(r_), run_time=0.7)
        self.play(FadeOut(VGroup(h, tb, res)))
        self.quiz("In a group, the element e with a * e = e * a = a for all a is",
                  ["the inverse", "the identity", "the order", "the generator"], 1,
                  "Pause and think.",
                  "The identity: it changes nothing. In Z four it is nought.")
        self.quiz("For f(x) = x² on [1, 3], the Mean Value Theorem gives c =",
                  ["1.5", "2", "2.5", "4"], 1,
                  "One more.",
                  "Two: the chord slope is four, and f dash of c equals two c.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Binary operation: closed. Group: closure, associativity, identity, inverses; abelian if commutative.",
            "Cayley table: identity row repeats the header; find e in each row for inverses; symmetric ⇒ abelian.",
            "Rolle: continuous, differentiable, f(a) = f(b) ⇒ f′(c) = 0 for some c in (a, b).",
            "MVT: f′(c) = (f(b) − f(a))/(b − a) — a tangent parallel to the chord.",
            "Trapezium weights 1, 2, …, 2, 1 (× h/2); Simpson 1, 4, 2, …, 4, 1 (× h/3), n even.",
        ], "Quick recap. The four group axioms and how to read them from a Cayley table. Rolle's theorem and the Mean Value Theorem, with their conditions. And the trapezium and Simpson weights for numerical integration. That completes Class 12 Mathematics.")
        self.outro("That was the appendix, and the end of Class 12 Mathematics. Well done for working through all of it. See you in the next subject.")
