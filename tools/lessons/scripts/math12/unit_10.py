import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

RNG = np.random.default_rng(7)
BASE_X = np.linspace(-1.6, 1.6, 26)
NOISE = RNG.normal(0, 1, 26)


def pearson(x, y):
    dx, dy = x - x.mean(), y - y.mean()
    return float((dx * dy).sum() / np.sqrt((dx * dx).sum() * (dy * dy).sum()))


def cloud(rho):
    """Points with correlation close to rho (same noise every time, so the cloud morphs smoothly)."""
    y = rho * BASE_X + np.sqrt(max(1 - rho * rho, 0)) * NOISE * 0.92
    return BASE_X, y


def scatter_axes(center, w=5.0, h=3.6, xr=(-2, 2, 1), yr=(-2.6, 2.6, 1), nums=False):
    ax = Axes(x_range=list(xr), y_range=list(yr), x_length=w, y_length=h, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": nums, "font_size": 18}).move_to(center)
    return ax


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 10
    TITLE = "Correlation and Regression"
    SUBTITLE = "How two quantities move together"
    SECTIONS = ["Correlation and the scatter diagram", "Karl Pearson's coefficient", "Properties of r", "Rank correlation", "Regression lines"]
    NEXT = "Unit 11 · Probability"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = scatter_axes((-2.4, -0.3, 0), w=7.0, h=5.4)
        xl = T("study hours", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.15)
        yl = T("marks", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        rho = ValueTracker(0.92)

        def dots():
            x, y = cloud(rho.get_value())
            return VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=th.AMBER) for a, b in zip(x, y) if -2.6 <= b <= 2.6])

        def rd():
            x, y = cloud(rho.get_value())
            r = pearson(x, y)
            word = "strong positive" if r > 0.75 else ("weak positive" if r > 0.25 else ("no correlation" if r > -0.25 else ("weak negative" if r > -0.75 else "strong negative")))
            col = th.MINT if r > 0.25 else (th.MUTED if r > -0.25 else th.CORAL)
            return VGroup(VGroup(M("r =", size=44), DecimalNumber(r, num_decimal_places=2, font_size=52, color=col)).arrange(RIGHT, buff=0.2), T(word, size=30, color=col, weight="BOLD")).arrange(DOWN, buff=0.3).move_to([4.0, 0.8, 0])

        d, r_ = always_redraw(dots), always_redraw(rd)
        with self.say("Each dot is one student: hours of study across, marks up. The dots climb from lower left to upper right, in a tight band. Study more, score more, on the whole. One number, r, measures how tightly two quantities move together."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.add(d, r_)
            self.wait(1.0)
        with self.say("Loosen the band and r falls. A shapeless blob: r near zero, no relationship. Tilt it the other way, like price against quantity sold, and r turns negative, down to minus one for a perfect falling line."):
            self.play(rho.animate.set_value(0.45), run_time=1.6)
            self.play(rho.animate.set_value(0.0), run_time=1.6)
            self.play(rho.animate.set_value(-0.85), run_time=1.8)
        with self.say("Correlation tells you how strongly two things move together. Regression goes one step further and gives you a line, so you can predict one from the other."):
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, xl, yl)), FadeOut(d), FadeOut(r_))
        self.remove(d, r_)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 10: Correlation and Regression."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Five parts. Correlation and the scatter diagram. Karl Pearson's coefficient, r. The properties of r. Spearman's rank correlation. And the two regression lines, with predictions.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Reading a scatter diagram")
        specs = [(1.0, "perfect positive, r = +1", th.MINT), (-1.0, "perfect negative, r = −1", th.CORAL), (0.85, "strong positive", th.MINT), (-0.45, "weak negative", th.CORAL), (0.0, "no correlation", th.MUTED), (None, "curved: r misleads", th.AMBER)]
        panels = VGroup()
        for rho, lab, col in specs:
            ax = scatter_axes((0, 0, 0), w=3.9, h=2.2, yr=(-2.8, 2.8, 1))
            if rho is None:
                x = BASE_X
                y = 2.2 - 1.6 * x * x + 0.2 * NOISE
            else:
                x, y = cloud(rho)
            dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.055, color=col) for a, b in zip(x, y) if -2.8 <= b <= 2.8])
            panels.add(VGroup(ax, dts, T(lab, size=24, color=col).next_to(ax, DOWN, buff=0.1)))
        panels.arrange_in_grid(rows=2, cols=3, buff=(0.4, 0.35)).move_to([0, -0.45, 0])
        with self.say("Plot every pair as a dot and the scatter diagram tells you the story before any arithmetic. Dots on one rising line: perfect positive correlation. On a falling line: perfect negative. A tight rising band: strong positive. A loose falling cloud: weak negative. A shapeless blob: none.") as v:
            self.play(FadeIn(h))
            for p_ in panels[:5]:
                self.play(FadeIn(p_, shift=UP * 0.15), run_time=0.5)
                self.hold(max(0.0, v.dur / 6 - 0.5))
        with self.say("And a warning: this last cloud clearly follows a curve, yet r comes out near zero. Karl Pearson's r measures only straight line relationships."):
            self.play(FadeIn(panels[5], shift=UP * 0.15))
        self.play(FadeOut(VGroup(h, panels)))
        h = P.head(self, "Tomato price and quantity sold at Kalimati")
        rows = [["price x (Rs/kg)", "120", "140", "160", "180", "200"], ["quantity y (quintal)", "11", "8", "9", "7", "5"]]
        tb = P.table(rows, [3.6, 1.3, 1.3, 1.3, 1.3, 1.3], row_h=0.6, size=24, colors=[th.INK] + [th.AMBER] * 5).move_to([0, 2.1, 0])
        ax = Axes(x_range=[100, 220, 20], y_range=[0, 12, 2], x_length=6.0, y_length=3.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([-1.4, -1.3, 0])
        pts = [(120, 11), (140, 8), (160, 9), (180, 7), (200, 5)]
        dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=th.CORAL) for a, b in pts])
        verdict = VGroup(T("falls to the right", size=26, color=th.CORAL), T("close to a line", size=26, color=th.CORAL), T("strong, negative, linear", size=28, color=th.CORAL, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, -1.2, 0])
        with self.say("A real example. The price of tomatoes on five days, and the quantity sold. Plot the five points: as the price goes up, the quantity comes down, almost along a straight line. Strong, negative, linear correlation. We will calculate it exactly in a moment."):
            self.play(FadeIn(h), FadeIn(tb))
            self.play(Create(ax))
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in dts], lag_ratio=0.2))
            self.play(FadeIn(verdict))
        self.play(FadeOut(VGroup(h, tb, ax, dts, verdict)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Why Σ dx dy measures correlation")
        ax = scatter_axes((-2.4, -0.5, 0), w=6.0, h=4.6)
        x, y = cloud(0.8)
        mx, my = x.mean(), y.mean()
        vx = DashedLine(ax.c2p(mx, -2.6), ax.c2p(mx, 2.6), color=th.FAINT)
        vy = DashedLine(ax.c2p(-2, my), ax.c2p(2, my), color=th.FAINT)
        ml = M(r"(\bar x, \bar y)", size=26, color=th.MUTED).next_to(ax.c2p(mx, my), DR, buff=0.05)
        dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=th.INK) for a, b in zip(x, y)])
        signs = VGroup(*[T(s_, size=34, color=c_, weight="BOLD").move_to(ax.c2p(*p_)) for s_, c_, p_ in [("+", th.MINT, (1.5, 2.1)), ("+", th.MINT, (-1.5, -2.1)), ("−", th.CORAL, (-1.5, 2.1)), ("−", th.CORAL, (1.5, -2.1))]])
        f = VGroup(M(r"d_x = x - \bar x,\quad d_y = y - \bar y", size=32), M(r"r = \frac{\sum d_x d_y}{\sqrt{\sum d_x^2 \sum d_y^2}}", size=44, color=th.MINT), T("−1 ≤ r ≤ +1, no units", size=26, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([3.8, 0.0, 0])
        with self.say("Where does the formula come from? Draw lines through the mean point, x bar, y bar. They cut the plane into four quarters."):
            self.play(FadeIn(h), Create(ax), FadeIn(dts))
            self.play(Create(vx), Create(vy), FadeIn(ml))
        with self.say("For each point, measure its deviations from the means, d x and d y. In the top right and bottom left quarters, both deviations have the same sign, so their product is positive. In the other two, it is negative. Add up all the products: mostly positive points give a big positive total."):
            self.play(FadeIn(signs))
            self.play(*[d_.animate.set_color(th.MINT if (a - mx) * (b - my) > 0 else th.CORAL) for d_, a, b in zip(dts, x, y)], run_time=1.2)
        with self.say("Divide by the square root of sum d x squared times sum d y squared, and the answer is pinned between minus one and plus one, with no units. That is Karl Pearson's coefficient of correlation."):
            self.play(Write(f[0]))
            self.play(Write(f[1]))
            self.play(FadeIn(f[2]))
        self.play(FadeOut(VGroup(h, ax, vx, vy, ml, dts, signs, f)))
        rows = [["|r|", "interpretation"], ["1", "perfect"], ["0.75 – 1", "high, strong"], ["0.5 – 0.75", "moderate"], ["0.25 – 0.5", "low"], ["0 – 0.25", "very weak, practically none"]]
        tb = P.table(rows, [3.0, 5.6], row_h=0.6, size=26, colors=[th.AMBER, th.INK]).move_to([0, 0.7, 0])
        det = para("The sign gives the direction, the size the strength. r² is the coefficient of determination: r = 0.8 means 64% of the variation in y is explained by x.", width=11.5, size=24, color=th.INK).move_to([0, -2.4, 0])
        with self.say("Reading the value: the sign gives the direction, the size gives the strength. Above three quarters is high, a half to three quarters moderate, below a quarter practically nothing. And r squared tells you the fraction of the variation in y that x explains.") as v:
            P.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(det))
        self.play(FadeOut(VGroup(tb, det)))
        rows = [["x", "y", "dx", "dy", "dx·dy", "dx²", "dy²"], ["120", "11", "−40", "3", "−120", "1600", "9"], ["140", "8", "−20", "0", "0", "400", "0"], ["160", "9", "0", "1", "0", "0", "1"],
                ["180", "7", "20", "−1", "−20", "400", "1"], ["200", "5", "40", "−3", "−120", "1600", "9"], ["800", "40", "0", "0", "−260", "4000", "20"]]
        tb = P.table(rows, [1.2, 1.0, 1.2, 1.0, 1.5, 1.3, 1.1], row_h=0.5, size=24, colors=[th.INK, th.INK, th.SKY, th.SKY, th.AMBER, th.MUTED, th.MUTED]).move_to([-2.6, 0.0, 0])
        hd = T("Kalimati: x̄ = 160, ȳ = 8", size=28, weight="BOLD").to_edge(UP, buff=0.75)
        res = VGroup(M(r"r = \frac{-260}{\sqrt{4000 \times 20}}", size=40), M(r"= \frac{-260}{282.8} = -0.92", size=40, color=th.CORAL), T("strong negative", size=28, color=th.CORAL, weight="BOLD"),
                     T("check: Σdx = Σdy = 0", size=22, color=th.MUTED)).arrange(DOWN, buff=0.35).move_to([4.2, 0.0, 0])
        with self.say("Now the tomatoes. The means are a hundred and sixty and eight, whole numbers, so use deviations from the actual means. Build the table: d x, d y, their product, and their squares. The two deviation columns must add to zero, which is your check.") as v:
            self.play(FadeIn(hd))
            P.reveal_table(self, tb, v.dur * 0.85)
        with self.say("Then r is minus two sixty over root of four thousand times twenty: minus point nine two. A strong negative correlation, just as the picture said."):
            for r_ in res:
                self.play(Write(r_), run_time=0.8)
        self.play(FadeOut(VGroup(hd, tb, res)))
        P.worked(self, "Study hours x = 1, …, 9 and marks y = 9, 8, 10, 12, 11, 13, 14, 16, 15. Find r.",
                 [r"n = 9,\ \sum x = 45,\ \sum y = 108,\ \sum xy = 597,\ \sum x^2 = 285,\ \sum y^2 = 1356", r"r = \frac{n\sum xy - \sum x\sum y}{\sqrt{[n\sum x^2 - (\sum x)^2][n\sum y^2 - (\sum y)^2]}}",
                  r"= \frac{5373 - 4860}{\sqrt{(2565 - 2025)(12204 - 11664)}} = \frac{513}{540} = 0.95"],
                 ["When the numbers are small, use the raw-score form.", "Total the five columns: x, y, x y, x squared, y squared.", "Put them into the raw-score formula.", "Five thirteen over five forty: point nine five. Very high positive, and r squared says ninety per cent of the variation in marks goes with study hours."])
        self.tip("Pick the form: whole-number means → deviations from the means; small numbers → raw scores; awkward means → deviations from an ASSUMED mean. Set the table out neatly: the marks are in the columns.",
                 "Exam tip. Whole-number means: use deviations. Small raw numbers: use the raw-score form. Awkward means: deviations from an assumed mean. And set out the table neatly, because the marks are in the columns.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "r ignores a change of origin and scale")
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=5.4, y_length=4.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([-2.8, -0.6, 0])
        x, y = cloud(0.75)
        sx, sy = ValueTracker(1.0), ValueTracker(0.0)
        dts = always_redraw(lambda: VGroup(*[Dot(ax.c2p(5 + 1.5 * a * sx.get_value() + sy.get_value(), 5 + 1.5 * b), radius=0.07, color=th.AMBER) for a, b in zip(x, y) if 0 <= 5 + 1.5 * a * sx.get_value() + sy.get_value() <= 10 and 0 <= 5 + 1.5 * b <= 10]))
        r0 = pearson(x, y)
        rd = VGroup(M(r"r =", size=40), DecimalNumber(r0, num_decimal_places=3, font_size=44, color=th.MINT)).arrange(RIGHT, buff=0.15).move_to([3.6, 2.0, 0])
        rule = VGroup(M(r"u = \frac{x - a}{h},\quad v = \frac{y - b}{k}\ \ (h, k > 0)", size=32), M(r"r_{uv} = r_{xy}", size=44, color=th.MINT), T("so code awkward data before you calculate", size=24, color=th.MUTED),
                      T("also: r(xy) = r(yx), and r² = b(yx) · b(xy)", size=22, color=th.INK)).arrange(DOWN, buff=0.3).move_to([3.6, -0.6, 0])
        with self.say("A powerful property. Slide all the x values along, or stretch them, and the shape of the cloud does not change. Neither does r."):
            self.play(FadeIn(h), Create(ax), FadeIn(rd))
            self.add(dts)
            self.play(sy.animate.set_value(1.5), run_time=1.5)
            self.play(sx.animate.set_value(0.6), run_time=1.5)
            self.play(sx.animate.set_value(1.0), sy.animate.set_value(0.0), run_time=1.0)
        with self.say("So you may subtract a convenient number from every x and divide by a common factor, and do the same to y, as long as the factors are positive. r stays exactly the same. That is why we can code awkward data before calculating."):
            for r_ in rule:
                self.play(Write(r_), run_time=0.8)
        self.play(FadeOut(VGroup(h, ax, rd, rule)), FadeOut(dts))
        self.remove(dts)
        c = self.callout("careful", "r = 0 means no LINEAR relation, not no relation. And correlation is not causation: ice-cream sales and drownings both rise in summer.", width=11, size=26)
        with self.say("Two cautions. Zero correlation only means no straight line relationship. And correlation is not causation: two things can rise together because a third thing drives them both."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Spearman's rank correlation")
        f = VGroup(M(r"r_s = 1 - \frac{6\sum D^2}{n^3 - n}", size=50, color=th.MINT), T("D = difference between the two ranks of each item", size=26, color=th.INK),
                   T("ties: give the average rank, and add (m³ − m)/12 to ΣD² for each tied group of m", size=24, color=th.MUTED)).arrange(DOWN, buff=0.4).move_to([0, 0.6, 0])
        with self.say("Some things can only be ranked, not measured: dancers placed by judges, students in order of merit. Spearman's coefficient works with ranks. Find D, the difference in ranks for each item, and r s is one minus six sum D squared, over n cubed minus n. For ties, give each the average rank, and add a small correction for each tied group."):
            self.play(FadeIn(h))
            for f_ in f:
                self.play(Write(f_), run_time=0.9)
        self.play(FadeOut(VGroup(h, f)))
        rows = [["performer", "A", "B", "C", "D", "E", "F", "G", "H"], ["judge X", "4", "1", "7", "2", "8", "5", "3", "6"], ["judge Y", "7", "1", "6", "4", "5", "8", "2", "3"], ["D", "−3", "0", "1", "−2", "3", "−3", "1", "3"], ["D²", "9", "0", "1", "4", "9", "9", "1", "9"]]
        tb = P.table(rows, [2.4] + [1.05] * 8, row_h=0.6, size=26, colors=[th.INK] + [th.AMBER] * 8).move_to([0, 1.0, 0])
        hd = T("Two judges, a folk-dance competition", size=28, weight="BOLD").to_edge(UP, buff=0.75)
        res = VGroup(M(r"\sum D^2 = 42,\quad n = 8:\ \ r_s = 1 - \frac{6(42)}{512 - 8} = 1 - 0.5 = 0.5", size=36, color=th.MINT), T("moderate agreement: both put B first, but they split over E and F", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([0, -2.2, 0])
        with self.say("Two judges rank eight dancers. Subtract the ranks for each dancer, square, and add: forty two. With n equal to eight, r s is one minus two fifty two over five oh four: exactly a half. Moderate agreement: both judges put B first, but they disagree sharply about E and F.") as v:
            self.play(FadeIn(hd))
            P.reveal_table(self, tb, v.dur * 0.55)
            self.play(Write(res[0]), FadeIn(res[1]))
        self.play(FadeOut(VGroup(hd, tb, res)))
        P.worked(self, "Ten students' Maths and Statistics marks give ΣD² = 44 (no ties). Another set has three tied pairs and ΣD² = 39. Find rs in each case.",
                 [r"r_s = 1 - \frac{6(44)}{1000 - 10} = 1 - \frac{264}{990} = 0.733", r"\text{ties: each group of 2 adds } \tfrac{8 - 2}{12} = 0.5;\ \text{three groups add } 1.5", r"r_s = 1 - \frac{6(39 + 1.5)}{990} = 1 - \frac{243}{990} = 0.755"],
                 ["Two more.", "With no ties: one minus two sixty four over nine ninety: point seven three three.", "With ties, each group of two tied values adds half to the sum of D squared. Three such groups add one and a half.", "So r s is one minus two forty three over nine ninety: point seven five five."])
        c = self.callout("careful", "Decide 'rank 1 = highest' and use it for BOTH variables. Ranking one column upward and the other downward reverses the sign of rs.", width=11, size=26)
        with self.say("Rank both columns the same way round, highest first. Mix the directions and the sign of your answer flips."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "The line of best fit: least squares")
        ax = Axes(x_range=[20, 30, 2], y_range=[34, 46, 2], x_length=7.0, y_length=5.0, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 18}).move_to([-2.6, -0.6, 0])
        X = np.array([21, 22, 25, 25, 28, 29.0])
        Y = np.array([37, 39, 38, 40, 43, 43.0])
        bt = ValueTracker(0.0)

        def fit():
            b = bt.get_value()
            g = VGroup(Line(ax.c2p(20, 40 + b * (20 - 25)), ax.c2p(30, 40 + b * (30 - 25)), color=th.SKY, stroke_width=4))
            for a, c in zip(X, Y):
                yh = 40 + b * (a - 25)
                side = abs(ax.c2p(0, c)[1] - ax.c2p(0, yh)[1])
                if side > 0.01:
                    sq = Square(side_length=side, stroke_width=1.5, stroke_color=th.CORAL, fill_color=th.CORAL, fill_opacity=0.25)
                    sq.move_to(np.array([ax.c2p(a, 0)[0] + side / 2, (ax.c2p(0, c)[1] + ax.c2p(0, yh)[1]) / 2, 0]))
                    g.add(sq)
            return g

        def rd():
            b = bt.get_value()
            sse = float(((Y - (40 + b * (X - 25))) ** 2).sum())
            return VGroup(VGroup(T("slope b =", size=26, color=th.SKY), DecimalNumber(b, num_decimal_places=2, font_size=34, color=th.SKY)).arrange(RIGHT, buff=0.15),
                          VGroup(T("sum of squares =", size=26, color=th.CORAL), DecimalNumber(sse, num_decimal_places=2, font_size=34, color=th.CORAL)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 2.0, 0])

        dts = VGroup(*[Dot(ax.c2p(a, c), radius=0.09, color=th.AMBER) for a, c in zip(X, Y)])
        mean = VGroup(Dot(ax.c2p(25, 40), radius=0.1, color=th.MINT), M(r"(\bar x, \bar y)", size=26, color=th.MINT).next_to(ax.c2p(25, 40), UL, buff=0.05))
        lab = VGroup(T("rainfall x (cm)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.4), T("wheat yield y", size=20, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.35))
        fr, r_ = always_redraw(fit), always_redraw(rd)
        with self.say("Rainfall and wheat yield on six plots. Which straight line fits best? Pivot a line about the mean point and look at the vertical misses. Square each miss: the red squares. The best line is the one that makes their total area as small as possible. The method of least squares."):
            self.play(FadeIn(h), Create(ax), FadeIn(lab), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dts], lag_ratio=0.15), FadeIn(mean))
            self.add(fr, r_)
            self.play(bt.animate.set_value(1.6), run_time=2.2)
            self.play(bt.animate.set_value(0.72), run_time=2.0)
        res = VGroup(M(r"b_{yx} = \frac{\sum d_x d_y}{\sum d_x^2} = \frac{36}{50} = 0.72", size=32), M(r"y - \bar y = b_{yx}(x - \bar x)", size=34, color=th.SKY), T("the best line always passes through (x̄, ȳ)", size=22, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([3.6, -0.9, 0])
        with self.say("The minimum comes at slope point seven two. Calculus gives the formula: b y x is sum d x d y over sum d x squared. And the best line always passes through the mean point. This is the regression line of y on x."):
            for r__ in res:
                self.play(Write(r__), run_time=0.8)
        self.play(FadeOut(VGroup(h, ax, lab, dts, mean, res)), FadeOut(fr), FadeOut(r_))
        self.remove(fr, r_)
        h = P.head(self, "Two regression lines")
        f = VGroup(VGroup(T("y on x (predict y):", size=26, color=th.SKY), M(r"y - \bar y = b_{yx}(x - \bar x),\ \ b_{yx} = \frac{\sum d_xd_y}{\sum d_x^2} = r\frac{\sigma_y}{\sigma_x}", size=32, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
                   VGroup(T("x on y (predict x):", size=26, color=th.PINK), M(r"x - \bar x = b_{xy}(y - \bar y),\ \ b_{xy} = \frac{\sum d_xd_y}{\sum d_y^2} = r\frac{\sigma_x}{\sigma_y}", size=32, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
                   M(r"r^2 = b_{yx}\,b_{xy},\quad r = \pm\sqrt{b_{yx}b_{xy}}\ (\text{same sign as the } b\text{'s})", size=32, color=th.MINT), T("both lines pass through (x̄, ȳ); r = ±1 → they coincide; r = 0 → they are perpendicular", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.1, 0])
        with self.say("There are two regression lines. Y on x, for predicting y, minimises the vertical misses. X on y, for predicting x, minimises the horizontal misses. Their slopes are the two regression coefficients, and their product is r squared. Both lines cross at the mean point."):
            self.play(FadeIn(h))
            for f_ in f:
                self.play(FadeIn(f_, shift=RIGHT * 0.2), run_time=0.8)
        self.play(FadeOut(VGroup(h, f)))
        P.worked(self, "Rainfall x: 21, 22, 25, 25, 28, 29; yield y: 37, 39, 38, 40, 43, 43. Find both regression lines, the yield at x = 27, and r.",
                 [r"\bar x = 25,\ \bar y = 40;\ \sum d_xd_y = 36,\ \sum d_x^2 = 50,\ \sum d_y^2 = 32", r"b_{yx} = 0.72:\ y = 0.72x + 22;\qquad b_{xy} = 1.125:\ x = 1.125y - 20", r"x = 27:\ y = 0.72(27) + 22 = 41.44", r"r = +\sqrt{0.72 \times 1.125} = \sqrt{0.81} = 0.9"],
                 ["The whole job.", "Means twenty five and forty; the table gives thirty six, fifty and thirty two.", "So y on x is y equals point seven two x plus twenty two, and x on y is x equals one point one two five y minus twenty.", "To predict yield from rainfall, use y on x: forty one point four four.", "And r is the square root of the product of the b's: point nine, positive like both b's."])
        P.worked(self, "The regression lines are 4x − 5y + 33 = 0 and 20x − 9y − 107 = 0. Find x̄, ȳ and r. If var(x) = 9, find σ of y.",
                 [r"\text{solve together: } \bar x = 13,\ \bar y = 17", r"y = \tfrac{4x + 33}{5} \Rightarrow b_{yx} = 0.8;\quad x = \tfrac{9y + 107}{20} \Rightarrow b_{xy} = 0.45", r"r^2 = 0.36 \le 1\ \checkmark \Rightarrow r = 0.6", r"0.8 = 0.6 \cdot \frac{\sigma_y}{3} \Rightarrow \sigma_y = 4"],
                 ["Working backwards.", "Both lines pass through the means, so solve them: thirteen and seventeen.", "Guess which line is which: the first as y on x gives point eight; the second as x on y gives point four five.", "Their product, point three six, is at most one, so the guess was right: r is point six. A product above one would mean swap them.", "Finally b y x equals r sigma y over sigma x gives sigma y equals four."])
        c = self.callout("careful", "To estimate y from x use y on x; to estimate x from y use x on y. Rearranging the wrong line scores zero. And don't extrapolate far outside the data.", width=11, size=26)
        with self.say("The classic trap: to estimate y, use the line of y on x; to estimate x, use x on y. Rearranging the wrong one gets no marks. And a line fitted on twenty to thirty centimetres of rain says nothing reliable about sixty."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("If b(yx) = 0.8 and b(xy) = 0.45, then r equals",
                  ["0.36", "0.6", "1.25", "−0.6"], 1,
                  "Pause and think.",
                  "Point six: the square root of point eight times point four five, positive like the b's.")
        self.quiz("For r = −0.92, the correlation is",
                  ["weak positive", "strong negative", "moderate negative", "none"], 1,
                  "One more.",
                  "Strong negative: the size, point nine two, is above three quarters, and the sign is negative.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Scatter diagram first: direction, form, strength. r measures LINEAR correlation only.",
            "r = Σdx·dy / √(Σdx² Σdy²), −1 ≤ r ≤ 1; unchanged by change of origin and scale.",
            "Spearman: rs = 1 − 6ΣD²/(n³ − n); average ranks for ties, plus (m³ − m)/12.",
            "y on x: y − ȳ = b(yx)(x − x̄), b(yx) = Σdx·dy/Σdx²; x on y with b(xy) = Σdx·dy/Σdy².",
            "r² = b(yx)·b(xy); both lines meet at (x̄, ȳ); predict y with y on x.",
        ], "Quick recap. Look at the scatter diagram first. Karl Pearson's r, between minus one and one, measures straight line correlation and ignores changes of origin and scale. Spearman's formula works with ranks. The two regression lines meet at the means, their slopes multiply to r squared, and you predict y with the line of y on x.")
        self.outro("That was correlation and regression. Next, probability: conditional probability, independence and Bayes' theorem. See you there.")
