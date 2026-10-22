import os
import sys
from math import comb

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402


def tree2(origin, first, second, dx=2.4, dy1=1.3, dy2=0.65, size=26):
    """Two-stage probability tree. first = [(label, prob_tex, color)], second = [[(label, prob_tex, color), ...] per first branch].
    Returns (group, leaves) where leaves[i][j] is the end point."""
    o = np.array(origin, dtype=float)
    g = VGroup(Dot(o, radius=0.06, color=th.MUTED))
    leaves = []
    n1 = len(first)
    for i, (lab, pr, col) in enumerate(first):
        p1 = o + np.array([dx, ((n1 - 1) / 2 - i) * 2 * dy1, 0])
        ln = Line(o, p1, color=col, stroke_width=3)
        g.add(ln, M(pr, size=size, color=col).next_to(ln.get_center(), UP if p1[1] >= o[1] else DOWN, buff=0.08), M(lab, size=size + 2, color=col).next_to(p1, RIGHT, buff=0.08))
        row = []
        n2 = len(second[i])
        for j, (lab2, pr2, col2) in enumerate(second[i]):
            st = p1 + RIGHT * 0.55
            p2 = st + np.array([dx, ((n2 - 1) / 2 - j) * 2 * dy2, 0])
            ln2 = Line(st, p2, color=col2, stroke_width=3)
            g.add(ln2, M(pr2, size=size - 2, color=col2).next_to(ln2.get_center(), UP if p2[1] >= st[1] else DOWN, buff=0.05), M(lab2, size=size, color=col2).next_to(p2, RIGHT, buff=0.08))
            row.append(p2)
        leaves.append(row)
    return g, leaves


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 11
    TITLE = "Probability"
    SUBTITLE = "Updating chances with new information"
    SECTIONS = ["Dependent events", "Conditional probability and independence", "Bayes' theorem", "The binomial distribution"]
    NEXT = "Unit 12 · Derivatives"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    def people(self, n_cols=40, n_rows=25, at=(-2.3, -0.4, 0), sp=0.19):
        g = VGroup()
        for k in range(n_cols * n_rows):
            r, c = divmod(k, n_cols)
            g.add(Square(side_length=sp * 0.78, stroke_width=0, fill_color=th.FAINT, fill_opacity=1).move_to(np.array(at) + np.array([(c - (n_cols - 1) / 2) * sp, ((n_rows - 1) / 2 - r) * sp, 0])))
        return g

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        grid = self.people()
        rng = np.random.default_rng(3)
        order = rng.permutation(1000)
        sick = order[:10]
        healthy_pos = order[10:30]
        cap = P.Captions(self, at=(4.9, 1.6, 0), width=3.6, size=24)
        with self.say("A disease affects one person in a hundred. Here are a thousand people. Ten of them are ill."):
            self.play(LaggedStart(*[FadeIn(sq) for sq in grid], lag_ratio=0.0008, run_time=1.5))
            self.play(*[grid[k].animate.set_fill(th.CORAL) for k in sick])
            cap("10 ill, 990 well", color=th.CORAL)
        with self.say("A test catches ninety nine per cent of the ill: all ten, near enough, test positive. But it also wrongly flags two per cent of the healthy people: about twenty of the nine hundred and ninety."):
            self.play(*[grid[k].animate.set_stroke(th.AMBER, width=3) for k in sick])
            self.play(*[grid[k].animate.set_fill(th.SKY).set_stroke(th.AMBER, width=3) for k in healthy_pos])
            cap("positives: 10 ill + 20 well", color=th.AMBER)
        with self.say("You test positive. What is the chance you are ill? Not ninety nine per cent. Of the thirty positives, only ten are ill: one in three. Turning probabilities round like this is Bayes' theorem, and this unit builds up to it."):
            self.play(*[grid[k].animate.set_fill_opacity(0.15) for k in range(1000) if k not in set(sick) | set(healthy_pos)])
            cap("P(ill | positive) = 10/30 = 1/3", color=th.MINT)
            nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(grid))
        cap.clear()
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 11: Probability."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four parts. Dependent events and tree diagrams. Conditional probability and independence. Bayes' theorem, for reasoning backwards. And repeated trials: the binomial distribution.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "A bag of 5 red and 3 black: draw two, without replacement")
        bag = VGroup(*[Circle(radius=0.2, fill_color=th.CORAL if i < 5 else "#2A2D3A", fill_opacity=1, stroke_color=th.INK, stroke_width=2) for i in range(8)]).arrange_in_grid(rows=2, cols=4, buff=0.12).move_to([-1.0, 2.3, 0])
        tg, leaves = tree2((-6.2, -0.7, 0), [("R", r"\frac58", th.CORAL), ("B", r"\frac38", th.INK)], [[("R", r"\frac47", th.CORAL), ("B", r"\frac37", th.INK)], [("R", r"\frac57", th.CORAL), ("B", r"\frac27", th.INK)]], dx=2.6, dy1=1.25, dy2=0.6, size=34)
        res = VGroup(M(r"RR:\ \tfrac58\cdot\tfrac47 = \tfrac{20}{56}", size=30, color=th.CORAL), M(r"RB:\ \tfrac58\cdot\tfrac37 = \tfrac{15}{56}", size=30), M(r"BR:\ \tfrac38\cdot\tfrac57 = \tfrac{15}{56}", size=30), M(r"BB:\ \tfrac38\cdot\tfrac27 = \tfrac{6}{56}", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r_, row in zip(res, [leaves[0][0], leaves[0][1], leaves[1][0], leaves[1][1]]):
            r_.move_to(row).set_x(4.4)
        rule = M(r"P(A \cap B) = P(A)\,P(B \mid A)", size=38, color=th.MINT).move_to([3.4, 2.4, 0])
        with self.say("Draw one ball, keep it out, then draw another. The second draw depends on the first: if the first was red, only four reds remain among seven. These are dependent events, and a tree diagram keeps track of them."):
            self.play(FadeIn(h), FadeIn(bag))
            self.play(Create(tg), run_time=2.5)
        with self.say("Multiply along each path. Both red: five eighths times four sevenths, twenty fifty sixths. That is the multiplication theorem: the probability of A and B is the probability of A, times the probability of B given A. The four paths add up to one."):
            self.play(Write(rule))
            for r_ in res:
                self.play(Write(r_), run_time=0.6)
        sm = M(r"\text{one of each} = \tfrac{15 + 15}{56} = \tfrac{15}{28},\qquad \text{at least one black} = 1 - \tfrac{20}{56} = \tfrac{9}{14}", size=30, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("One of each colour: add the two middle paths, fifteen twenty eighths. At least one black: one minus both red, nine fourteenths."):
            self.play(Write(sm))
        self.play(FadeOut(VGroup(h, bag, tg, res, rule, sm)))
        P.worked(self, "Two cards are drawn without replacement from a pack of 52. Find P(both kings) and P(king then queen). Three cards: P(all aces)?",
                 [r"P(K_1 K_2) = \frac{4}{52}\times\frac{3}{51} = \frac{1}{221}", r"P(K\,Q) = \frac{4}{52}\times\frac{4}{51} = \frac{4}{663}", r"P(AAA) = \frac{4}{52}\times\frac{3}{51}\times\frac{2}{50} = \frac{1}{5525}"],
                 ["Cards, without replacement.", "Four kings in fifty two; then three kings in the fifty one left: one in two twenty one.", "A king then a queen: all four queens are still there among fifty one.", "Three aces: chain the multiplication three times."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Given B: the sample space shrinks to B")
        S = RoundedRectangle(corner_radius=0.2, width=5.6, height=4.2, stroke_color=th.MUTED, stroke_width=3).move_to([-3.6, -0.5, 0])
        A = Circle(radius=1.3, stroke_color=th.SKY, stroke_width=4, fill_color=th.SKY, fill_opacity=0.15).move_to([-4.3, -0.4, 0])
        B = Circle(radius=1.3, stroke_color=th.AMBER, stroke_width=4, fill_color=th.AMBER, fill_opacity=0.15).move_to([-2.8, -0.6, 0])
        labs = VGroup(M("S", size=32, color=th.MUTED).next_to(S, UL, buff=-0.45), M("A", size=34, color=th.SKY).move_to([-5.1, 0.6, 0]), M("B", size=34, color=th.AMBER).move_to([-2.0, 0.5, 0]))
        inter = Intersection(A, B, stroke_width=0, fill_color=th.MINT, fill_opacity=0.7)
        f = VGroup(M(r"P(A \mid B) = \frac{P(A \cap B)}{P(B)}", size=46, color=th.MINT), T("'the probability of A, given that B has happened'", size=24, color=th.MUTED),
                   M(r"\text{independent} \iff P(A \mid B) = P(A) \iff P(A \cap B) = P(A)P(B)", size=30, color=th.AMBER)).arrange(DOWN, buff=0.35)
        f[2].scale_to_fit_width(6.4)
        f.arrange(DOWN, buff=0.35).move_to([3.4, -0.2, 0])
        with self.say("Conditional probability. Suppose you are told that B has happened. Everything outside B is now impossible: B becomes the whole sample space. The chance of A is now the part of A inside B, as a fraction of B."):
            self.play(FadeIn(h), Create(S), FadeIn(A), FadeIn(B), FadeIn(labs))
            self.play(S.animate.set_stroke(opacity=0.2), A.animate.set_fill(opacity=0.04).set_stroke(opacity=0.35), B.animate.set_stroke(width=7))
            self.play(FadeIn(inter))
            self.play(Write(f[0]), FadeIn(f[1]))
        with self.say("If knowing B changes nothing, so the probability of A given B is just the probability of A, the events are independent. Equivalently, the probability of both is the product of the two."):
            self.play(Write(f[2]))
        self.play(FadeOut(VGroup(h, S, A, B, labs, inter, f)))
        h = P.head(self, "100 students: always draw the two-way table")
        rows = [["", "passed", "failed", "total"], ["boys", "45", "15", "60"], ["girls", "35", "5", "40"], ["total", "80", "20", "100"]]
        tb = P.table(rows, [2.0, 1.8, 1.8, 1.8], row_h=0.72, size=30, colors=[th.INK, th.MINT, th.CORAL, th.AMBER]).move_to([-3.2, 0.3, 0])
        q = VGroup(M(r"P(\text{pass}) = \frac{80}{100} = \frac45", size=40), M(r"P(\text{pass} \mid \text{girl}) = \frac{35}{40} = \frac78", size=40, color=th.PINK), M(r"P(\text{girl} \mid \text{pass}) = \frac{35}{80} = \frac{7}{16}", size=40, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.6, 0.2, 0])
        with self.say("A Kathmandu college: a hundred students, sixty boys. Forty five boys and thirty five girls passed. Put it in a two way table first, always. The chance a random student passed is eighty out of a hundred."):
            self.play(FadeIn(h), FadeIn(tb))
            self.play(Write(q[0]))
        with self.say("Given a girl: work inside the girls' row only. Thirty five of forty passed: seven eighths. Given a pass: now the pass column is the whole world. Thirty five of the eighty: seven sixteenths. Same thirty five, different denominators, different questions."):
            self.play(Write(q[1]))
            self.play(Write(q[2]))
        self.play(FadeOut(VGroup(h, tb, q)))
        h = P.head(self, "Two dice: 'given' names the sample space")
        grid = VGroup()
        for i in range(1, 7):
            for j in range(1, 7):
                grid.add(VGroup(Square(side_length=0.74, stroke_color=th.FAINT, stroke_width=1.5), T(f"{i},{j}", size=20, color=th.MUTED)).move_to([-5.6 + (j - 1) * 0.8, 1.6 - (i - 1) * 0.8, 0]))
        sum6 = [k for k in range(36) if (k // 6 + 1) + (k % 6 + 1) == 6]
        odd = [k for k in range(36) if (k // 6 + 1) % 2 == 1 and (k % 6 + 1) % 2 == 1]
        both = [k for k in sum6 if k in odd]
        q = VGroup(M(r"P(\text{both odd} \mid \text{sum } 6) = \frac35", size=40, color=th.AMBER), M(r"P(\text{sum } 6 \mid \text{both odd}) = \frac39 = \frac13", size=40, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.4, 0.2, 0])
        with self.say("Two dice, thirty six outcomes. Given that the sum is six: only five squares remain. Three of them are both odd: three fifths."):
            self.play(FadeIn(h), FadeIn(grid))
            self.play(*[grid[k][0].animate.set_fill(th.AMBER, opacity=0.35) for k in sum6])
            self.play(*[grid[k][0].animate.set_stroke(th.MINT, width=5) for k in both])
            self.play(Write(q[0]))
        with self.say("Turn it round. Given both odd: nine squares. The same three have sum six: one third. Same favourable outcomes, different conditions, different answers."):
            self.play(*[grid[k][0].animate.set_fill(th.SKY, opacity=0.3) for k in odd if k not in sum6], *[grid[k][0].animate.set_fill(th.FAINT, opacity=0) for k in sum6 if k not in odd])
            self.play(Write(q[1]))
        self.play(FadeOut(VGroup(h, grid, q)))
        P.worked(self, "Three students solve a problem independently with chances 1/2, 1/3 and 1/4. Find P(solved) and P(exactly one solves it).",
                 [r"P(\text{all fail}) = \tfrac12\cdot\tfrac23\cdot\tfrac34 = \tfrac14 \Rightarrow P(\text{solved}) = \tfrac34", r"P(\text{exactly one}) = \tfrac12\cdot\tfrac23\cdot\tfrac34 + \tfrac12\cdot\tfrac13\cdot\tfrac34 + \tfrac12\cdot\tfrac23\cdot\tfrac14 = \tfrac{6 + 3 + 2}{24} = \tfrac{11}{24}"],
                 ["Independent events.", "'At least one solves it' is one minus 'all three fail'. Multiply the failure chances: a quarter. So three quarters.", "Exactly one: three separate cases, one solver and two failures each. Add them: eleven twenty fourths."])
        c = self.callout("careful", "P(A | B) ≠ P(B | A). Independent (P(A and B) = P(A)P(B)) is NOT the same as mutually exclusive (P(A and B) = 0).", width=11, size=26)
        with self.say("Two classic confusions. A given B is not B given A. And independent is not the same as mutually exclusive: exclusive events cannot both happen, so they are about as dependent as events can be."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Bayes: from effect back to cause")
        tg, leaves = tree2((-5.8, -0.5, 0), [(r"E_1", r"P(E_1)", th.SKY), (r"E_2", r"P(E_2)", th.PINK)], [[("W", r"P(W|E_1)", th.AMBER), (r"W'", "", th.MUTED)], [("W", r"P(W|E_2)", th.AMBER), (r"W'", "", th.MUTED)]], dx=2.6, dy1=1.3, dy2=0.65, size=30)
        f = VGroup(M(r"P(W) = \sum P(E_i)\,P(W \mid E_i)", size=34), T("(total probability: add the paths that end in W)", size=22, color=th.MUTED),
                   M(r"P(E_1 \mid W) = \frac{P(E_1)\,P(W \mid E_1)}{\sum P(E_i)\,P(W \mid E_i)}", size=38, color=th.MINT), T("(the share of W that came through E₁)", size=22, color=th.MUTED)).arrange(DOWN, buff=0.25)
        f.scale_to_fit_width(min(f.width, 5.6)).move_to([3.9, 0.0, 0])
        with self.say("Bayes' theorem reasons backwards. Several causes, E one and E two, each can produce an effect W. Going forwards along the tree, multiply along the paths. The total probability of W is the sum of the paths that end in W."):
            self.play(FadeIn(h), Create(tg), run_time=2.0)
            self.play(Write(f[0]), FadeIn(f[1]))
        with self.say("Now W has happened. Which cause was it? The probability of E one given W is the E one path's share of all the W paths. That is Bayes' theorem."):
            self.play(Write(f[2]), FadeIn(f[3]))
        self.play(FadeOut(VGroup(h, tg, f)))
        P.worked(self, "Bag A: 3 white, 2 red. Bag B: 2 white, 4 red. A bag is chosen at random and a ball drawn. Find P(white), and P(bag A | white).",
                 [r"P(W) = \tfrac12\cdot\tfrac35 + \tfrac12\cdot\tfrac13 = \tfrac{3}{10} + \tfrac16 = \tfrac{7}{15}", r"P(A \mid W) = \frac{3/10}{7/15} = \frac{9}{14} \approx 64\%"],
                 ["Two bags.", "Total probability: half times three fifths, plus half times a third: seven fifteenths.", "Bayes: the bag A path, three tenths, as a share of seven fifteenths: nine fourteenths. Sensible: bag A is the whiter bag."])
        P.worked(self, "Machine A makes 60% of the bulbs, B the rest; 2% of A's and 3% of B's are defective. A defective bulb is found. P(made by A)?",
                 [r"P(D) = 0.6(0.02) + 0.4(0.03) = 0.012 + 0.012 = 0.024", r"P(A \mid D) = \frac{0.012}{0.024} = \frac12"],
                 ["A factory.", "Total probability of a defective bulb: point zero two four.", "The A path is point zero one two of it: exactly a half. A makes more bulbs, but makes them better, and the two effects cancel."])
        h = P.head(self, "The screening test, by Bayes")
        st = VGroup(M(r"P(D) = 0.01,\ \ P(+ \mid D) = 0.99,\ \ P(+ \mid D') = 0.02", size=32), M(r"P(+) = 0.01(0.99) + 0.99(0.02) = 0.0099 + 0.0198 = 0.0297", size=32),
                    M(r"P(D \mid +) = \frac{0.0099}{0.0297} = \frac13", size=44, color=th.MINT), T("false positives from the huge healthy group outnumber the true positives two to one", size=24, color=th.MUTED)).arrange(DOWN, buff=0.35).move_to([0, 0.0, 0])
        with self.say("Now the cold open, done properly. One per cent ill, a ninety nine per cent catch rate, a two per cent false alarm rate. Total probability of a positive: point zero two nine seven. The share from the ill: exactly one third. That is why a positive screening result is always checked with a second test."):
            self.play(FadeIn(h))
            for s_ in st:
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Repeated independent trials")
        f = VGroup(M(r"P(X = r) = {}^nC_r\,p^r q^{n-r},\quad q = 1 - p", size=42, color=th.MINT), T("n independent trials, each a success with probability p", size=24, color=th.MUTED),
                   M(r"\text{mean} = np,\qquad \text{variance} = npq", size=36, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([0, 1.7, 0])
        with self.say("Toss a coin, roll a die, again and again, the same chance of success each time. The probability of exactly r successes in n trials: choose which r trials succeed, n C r ways, each with probability p to the r times q to the n minus r. The mean number of successes is n p, and the variance n p q."):
            self.play(FadeIn(h))
            for f_ in f:
                self.play(Write(f_), run_time=0.9)
        ax = Axes(x_range=[-0.5, 5.5, 1], y_range=[0, 0.5, 0.1], x_length=7.4, y_length=3.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([-1.8, -1.6, 0])
        pt = ValueTracker(0.5)

        def bars():
            p = pt.get_value()
            g = VGroup()
            for r in range(6):
                pr = comb(5, r) * p ** r * (1 - p) ** (5 - r)
                g.add(Rectangle(width=0.8, height=max(ax.c2p(0, pr)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0, fill_color=th.SKY, fill_opacity=0.85).move_to(ax.c2p(r, 0), aligned_edge=DOWN))
            return g

        def lab():
            p = pt.get_value()
            return VGroup(VGroup(M(r"n = 5,\ p =", size=40), DecimalNumber(p, num_decimal_places=2, font_size=42, color=th.SKY)).arrange(RIGHT, buff=0.12),
                          VGroup(M(r"\text{mean } np =", size=38), DecimalNumber(5 * p, num_decimal_places=2, font_size=40, color=th.AMBER)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, -1.6, 0])

        b_, l_ = always_redraw(bars), always_redraw(lab)
        with self.say("Here are the probabilities for five trials. With a fair coin, p a half, the bars are symmetric about the mean, two and a half. Make success rarer, like rolling a six, and the bars pile up near zero; make it likely, and they slide right."):
            self.play(Create(ax))
            self.add(b_, l_)
            self.wait(0.6)
            self.play(pt.animate.set_value(1 / 6), run_time=1.8)
            self.play(pt.animate.set_value(0.8), run_time=1.8)
            self.play(pt.animate.set_value(0.5), run_time=1.0)
        self.play(FadeOut(VGroup(h, f, ax)), FadeOut(b_), FadeOut(l_))
        self.remove(b_, l_)
        P.worked(self, "A fair coin is tossed 5 times. Find P(exactly 3 heads), P(at least 3 heads), and the mean.",
                 [r"P(3) = {}^5C_3\left(\tfrac12\right)^5 = \tfrac{10}{32} = \tfrac{5}{16}", r"P(X \ge 3) = \tfrac{10 + 5 + 1}{32} = \tfrac12", r"\text{mean} = np = 2.5"],
                 ["Coins.", "Exactly three: five C three is ten, times a half to the fifth: five sixteenths.", "At least three: ten plus five plus one, over thirty two: a half, as symmetry demands.", "Mean: two and a half heads."])
        P.worked(self, "A die is thrown 4 times. Find P(exactly two sixes), P(at least one six), and the mean and variance of the number of sixes.",
                 [r"P(2) = {}^4C_2\left(\tfrac16\right)^2\left(\tfrac56\right)^2 = \tfrac{150}{1296} = \tfrac{25}{216}", r"P(X \ge 1) = 1 - \left(\tfrac56\right)^4 = \tfrac{671}{1296} \approx 0.518", r"\text{mean} = \tfrac46 = \tfrac23,\qquad \text{variance} = 4\cdot\tfrac16\cdot\tfrac56 = \tfrac59"],
                 ["A die.", "Exactly two sixes: six ways, times one thirty sixth, times twenty five thirty sixths: twenty five over two sixteen.", "At least one: one minus no sixes at all: just over a half.", "Mean two thirds; variance five ninths."])
        self.tip("'At least one' = 1 − P(none). Name the success, write n, p, q first, and check that the probabilities of every case add to 1.",
                 "Exam tip. At least one is one minus none. Write down n, p and q before anything else.")
        self.quiz("A test is 99% accurate for the ill, but 2% of the healthy also test positive, and 1% of people are ill. P(ill | positive) is about",
                  ["99%", "50%", "33%", "2%"], 2,
                  "Pause and think about the thousand people.",
                  "About a third: ten true positives against about twenty false ones.")
        self.quiz("If A and B are independent with P(A) = 0.5 and P(B) = 0.4, then P(A and B) is",
                  ["0.9", "0.2", "0.1", "0"], 1,
                  "One more.",
                  "Point two: for independent events, multiply. Zero would mean mutually exclusive.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Dependent events: P(A and B) = P(A) P(B | A); multiply along tree paths.",
            "P(A | B) = P(A and B)/P(B): B becomes the whole sample space.",
            "Independent ⇔ P(A and B) = P(A)P(B) — not the same as mutually exclusive.",
            "Bayes: P(E₁ | W) = P(E₁)P(W | E₁) / Σ P(Eᵢ)P(W | Eᵢ).",
            "Binomial: P(X = r) = ⁿCᵣ pʳ qⁿ⁻ʳ; mean np, variance npq; at least one = 1 − P(none).",
        ], "Quick recap. Multiply along a tree for dependent events. Conditioning shrinks the sample space. Independent events multiply. Bayes' theorem finds the cause from the effect. And the binomial formula counts successes in repeated trials, with mean n p and variance n p q.")
        self.outro("That was probability. Next, derivatives: limits, rates of change and how to differentiate anything. See you there.")
