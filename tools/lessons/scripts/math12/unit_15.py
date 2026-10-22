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


def gs_iter(n):
    x = y = z = 0.0
    out = []
    for _ in range(n):
        x = (17 - y + 2 * z) / 20
        y = (-18 - 3 * x + z) / 20
        z = (25 - 2 * x + 3 * y) / 20
        out.append((x, y, z))
    return out


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 15
    TITLE = "Computational Methods"
    SUBTITLE = "When a computer does the algebra"
    SECTIONS = ["Gauss elimination", "Gauss–Seidel iteration", "Linear programming: the simplex method", "How accurate is the answer?"]
    NEXT = "Unit 16 · Mechanics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = plot_axes([-2.4, -0.4, 0], [1.8, 3.1, 0.2], [-4, 18, 4], 6.4, 4.6)
        f = lambda x: x ** 3 - 2 * x - 5
        cv = ax.plot(f, x_range=[1.8, 3.05], color=th.AMBER, stroke_width=4)
        xs = [3.0]
        for _ in range(3):
            x = xs[-1]
            xs.append(x - f(x) / (3 * x * x - 2))
        steps = VGroup()
        for a, b in zip(xs, xs[1:]):
            steps.add(VGroup(DashedLine(ax.c2p(a, 0), ax.c2p(a, f(a)), color=th.FAINT), Line(ax.c2p(a, f(a)), ax.c2p(b, 0), color=th.SKY, stroke_width=3), Dot(ax.c2p(b, 0), color=th.MINT, radius=0.08)))
        tab = VGroup(*[VGroup(T(f"x{i} =", size=26, color=th.MUTED), T(f"{v:.6f}", size=28, color=th.MINT)).arrange(RIGHT, buff=0.15) for i, v in enumerate(xs)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 0.8, 0])
        q = M(r"x^3 - 2x - 5 = 0", size=40).move_to([4.4, 2.6, 0])
        with self.say("Solve x cubed minus two x minus five equals zero. There is no neat formula to factorise it. But a computer can home in on the root: guess three, follow the tangent down to the axis, and use where it lands as the next guess."):
            self.play(Create(ax), Create(cv), Write(q))
            self.play(FadeIn(tab[0]))
            for s_, t_ in zip(steps, tab[1:]):
                self.play(Create(s_), FadeIn(t_), run_time=1.0)
        with self.say("Two point three six, then two point one two seven, then two point zero nine five, and the digits soon stop changing: the root is two point zero nine four six. Numerical methods like this solve problems that algebra cannot, and the art is knowing how accurate the answer is."):
            nb = P.neby_in(self, "cool", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, cv, steps, tab, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 15: Computational Methods."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four parts. Gauss elimination for systems of equations. The Gauss Seidel iteration. Linear programming by the simplex method. And how accurate a computed answer is: Newton Raphson and the integration rules.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Gauss elimination: x + y + z = 6, 2x + 3y + z = 11, 3x + y + 4z = 17")
        G = P.grid([[1, 1, 1, 6], [2, 3, 1, 11], [3, 1, 4, 17]], bar=3, size=40, dx=1.1, dy=0.8).move_to([-2.0, 0.6, 0])
        with self.say("Gauss elimination is the systematic version of eliminating by hand, which is why computers use it. Write the augmented matrix. Use the first pivot to clear the first column: subtract twice row one from row two, and three times row one from row three."):
            self.play(FadeIn(h), FadeIn(G))
            P.set_row(self, G, 1, [0, 1, -1, -1], r"R_2 - 2R_1")
            P.set_row(self, G, 2, [0, -2, 1, -1], r"R_3 - 3R_1")
        with self.say("Then the second pivot clears the second column: add twice row two to row three. The matrix is now triangular."):
            P.set_row(self, G, 2, [0, 0, -1, -3], r"R_3 + 2R_2")
        back = VGroup(M(r"-z = -3 \Rightarrow z = 3", size=36), M(r"y - z = -1 \Rightarrow y = 2", size=36), M(r"x + y + z = 6 \Rightarrow x = 1", size=36, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.6, 0])
        with self.say("Back substitute from the bottom: z is three, y is two, x is one."):
            for b_ in back:
                self.play(Write(b_), run_time=0.8)
        nt = para("If a pivot is 0, swap with a lower row (partial pivoting). Computers always choose the largest available pivot, to keep rounding errors small.", width=11.5, size=24, color=th.MUTED).move_to([0, -2.9, 0])
        with self.say("If a pivot turns out to be zero, swap in a lower row. In practice, computers always swap in the largest available pivot, to keep rounding errors small."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, G, back, nt)))
        P.worked(self, "A Pokhara shop: 1 pen + 1 notebook + 1 eraser = Rs 60; 2 + 3 + 1 = Rs 110; 3 + 1 + 4 = Rs 170. Find each price.",
                 [r"x + y + z = 60,\quad 2x + 3y + z = 110,\quad 3x + y + 4z = 170", r"\text{same coefficients as before, right sides} \times 10", r"x = 10,\quad y = 20,\quad z = 30"],
                 ["Recognise the system.", "These are the equations we just solved, with every right side multiplied by ten.", "So every unknown is ten times bigger: pens ten rupees, notebooks twenty, erasers thirty."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Gauss–Seidel: guess, improve, repeat")
        eq = VGroup(M(r"20x + y - 2z = 17", size=40), M(r"3x + 20y - z = -18", size=40), M(r"2x - 3y + 20z = 25", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.8, 1.6, 0])
        re_ = VGroup(M(r"x = (17 - y + 2z)/20", size=38, color=th.SKY), M(r"y = (-18 - 3x + z)/20", size=38, color=th.SKY), M(r"z = (25 - 2x + 3y)/20", size=38, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.6, 1.6, 0])
        dom = T("diagonally dominant: 20 > 1 + 2,  20 > 3 + 1,  20 > 2 + 3", size=28, color=th.AMBER).move_to([0, 0.15, 0])
        with self.say("Gauss Seidel takes another route: iteration. Solve each equation for its own unknown. Start from a guess, nought, nought, nought, and keep improving. It is guaranteed to converge when each diagonal coefficient beats the others in its row. Here twenty beats one plus two, and so on."):
            self.play(FadeIn(h), Write(eq))
            self.play(Write(re_))
            self.play(FadeIn(dom))
        its = gs_iter(5)
        rows = [["n", "x", "y", "z"], ["0", "0", "0", "0"]] + [[str(i + 1), f"{a:.6f}", f"{b:.6f}", f"{c:.6f}"] for i, (a, b, c) in enumerate(its)]
        tb = P.table(rows, [0.9, 2.8, 2.8, 2.8], row_h=0.44, size=24, colors=[th.MUTED, th.MINT, th.MINT, th.MINT]).move_to([0, -1.9, 0])
        with self.say("Each new value is used immediately: the new y uses the x just found, and the new z uses both. That is what makes it Gauss Seidel. Watch the digits settle: by the fourth or fifth round they no longer change. x is one, y is minus one, z is one.") as v:
            P.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h, eq, re_, dom, tb)))
        P.worked(self, "Why is Gauss–Seidel unsafe on x + 4y − z = 6, 5x − y + z = 7, x + y + 6z = 12? Fix it.",
                 [r"\text{row 1: } |1| < 4 + 1;\quad \text{row 2: } |-1| < 5 + 1:\ \text{not dominant}", r"\text{reorder: } 5x - y + z = 7,\ \ x + 4y - z = 6,\ \ x + y + 6z = 12", r"5 > 2,\quad 4 > 2,\quad 6 > 2:\ \text{now safe}"],
                 ["Check dominance first.", "The first two rows fail the test.", "Reorder so each big coefficient sits on the diagonal.", "Now every row is dominant, and the iteration will converge."])

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Maximise Z = 3x + 5y:  x + y ≤ 4,  x + 3y ≤ 6")
        ax = plot_axes([-3.0, -0.6, 0], [0, 6.5, 1], [0, 4.5, 1], 6.8, 4.8)
        l1 = ax.plot(lambda x: 4 - x, x_range=[0, 4.5], color=th.SKY, stroke_width=3)
        l2 = ax.plot(lambda x: (6 - x) / 3, x_range=[0, 6.2], color=th.PINK, stroke_width=3)
        V = [(0, 0), (4, 0), (3, 1), (0, 2)]
        reg = Polygon(*[ax.c2p(*v) for v in V], stroke_width=0, fill_color=th.MINT, fill_opacity=0.3)
        lab = VGroup(*[M(f"({a}, {b})", size=24, color=th.INK).next_to(ax.c2p(a, b), UR if (a, b) != (0, 0) else DL, buff=0.06) for a, b in V])
        zc = ValueTracker(0)
        zl = always_redraw(lambda: P.clipped(ax, lambda x: (zc.get_value() - 3 * x) / 5, 0, 6.5, 0, 4.5, th.AMBER, width=3))
        zr = always_redraw(lambda: VGroup(M("Z =", size=42, color=th.AMBER), DecimalNumber(zc.get_value(), num_decimal_places=1, font_size=44, color=th.AMBER)).arrange(RIGHT, buff=0.12).move_to([3.6, 2.4, 0]))
        with self.say("Linear programming. Make as much profit Z equals three x plus five y as you can, under two limits. The limits cut out a region, the feasible region, a polygon. Slide the profit line outward: the last point it touches is a corner. The best answer is always at a corner."):
            self.play(FadeIn(h), Create(ax), Create(l1), Create(l2))
            self.play(FadeIn(reg), FadeIn(lab))
            self.add(zl, zr)
            self.play(zc.animate.set_value(14), run_time=3.0)
        path = VGroup(Arrow(ax.c2p(0, 0), ax.c2p(0, 2), buff=0.1, color=th.CORAL, stroke_width=5), Arrow(ax.c2p(0, 2), ax.c2p(3, 1), buff=0.1, color=th.CORAL, stroke_width=5))
        txt = VGroup(T("simplex: walk corner to corner,", size=26, color=th.CORAL), T("always improving Z", size=26, color=th.CORAL), M(r"(0,0) \to (0,2) \to (3,1),\ Z = 14", size=32, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.8, 0.4, 0])
        with self.say("The simplex method finds that corner without drawing anything, which matters when there are many variables. It starts at the origin and walks along edges from corner to corner, improving Z each time, until no step helps. Here: nought nought, then nought two, then three one, where Z is fourteen."):
            self.play(GrowArrow(path[0]), FadeIn(txt[0]))
            self.play(GrowArrow(path[1]), FadeIn(txt[1]))
            self.play(Write(txt[2]))
        self.play(FadeOut(VGroup(h, ax, l1, l2, reg, lab, path, txt)), FadeOut(zl), FadeOut(zr))
        self.remove(zl, zr)
        rules = P.bullets(["1. Add slack variables: x + y + s₁ = 4, x + 3y + s₂ = 6;  write Z − 3x − 5y = 0.",
                           "2. Pivot column: the MOST NEGATIVE entry in the Z row (none left → optimal).", "3. Pivot row: the SMALLEST ratio RHS ÷ (positive) column entry.",
                           "4. Make the pivot 1, clear the rest of its column (Z row included). Repeat."], width=12, size=26).move_to([0, 0.2, 0])
        hd = T("The simplex rules", size=30, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("The rules. Turn each inequality into an equation with a slack variable, the unused capacity. Choose the pivot column with the most negative number in the Z row. Choose the pivot row with the smallest ratio of right side to column entry. Pivot, as in Gauss Jordan. Repeat until the Z row has no negatives.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, rules, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, rules)))
        h = P.head(self, "The tableaux for Z = 3x + 5y")
        t1 = P.table([["basic", "x", "y", "s₁", "s₂", "RHS", "ratio"], ["s₁", "1", "1", "1", "0", "4", "4"], ["s₂", "1", "3", "0", "1", "6", "2 ←"], ["Z", "−3", "−5", "0", "0", "0", ""]], [1.2, 0.9, 0.9, 0.9, 0.9, 1.0, 1.0], row_h=0.5, size=24, colors=[th.MUTED] + [th.INK] * 6).move_to([-3.3, 0.9, 0])
        t3 = P.table([["basic", "x", "y", "s₁", "s₂", "RHS"], ["x", "1", "0", "3/2", "−1/2", "3"], ["y", "0", "1", "−1/2", "1/2", "1"], ["Z", "0", "0", "2", "1", "14"]], [1.2, 0.8, 0.8, 1.1, 1.1, 1.0], row_h=0.5, size=24, colors=[th.MUTED] + [th.INK] * 5).move_to([3.3, 0.9, 0])
        cap = VGroup(T("tableau 1: y enters (−5), s₂ leaves (ratio 2)", size=22, color=th.AMBER).next_to(t1, DOWN, buff=0.3), T("tableau 3: no negatives → x = 3, y = 1, Z = 14", size=22, color=th.MINT).next_to(t3, DOWN, buff=0.3))
        with self.say("In the first tableau, minus five is the most negative, so y enters; the smallest ratio is two, so s two leaves. One more pivot brings in x. In the final tableau the Z row has no negatives: x is three, y is one, and the maximum Z is fourteen, the same corner we found by sliding the line.") as v:
            self.play(FadeIn(h))
            P.reveal_table(self, t1, v.dur * 0.35)
            self.play(FadeIn(cap[0]))
            P.reveal_table(self, t3, v.dur * 0.35)
            self.play(FadeIn(cap[1]))
        self.play(FadeOut(VGroup(h, t1, t3, cap)))
        P.worked(self, "A Butwal workshop: a chair needs 4 h carpentry + 2 h finishing (profit Rs 800); a table 2 h + 4 h (Rs 600). Only 60 h and 48 h are available. Maximise profit.",
                 [r"Z = 8x + 6y\ (\text{hundreds});\quad 4x + 2y \le 60,\quad 2x + 4y \le 48", r"\text{tableau 1: } x \text{ enters, ratio } 15;\quad \text{tableau 2: } y \text{ enters, ratio } 6", r"x = 12,\ y = 6,\ Z = 132:\ \text{Rs } 13\,200"],
                 ["A real problem.", "Set up: profit in hundreds of rupees, and the two hour limits.", "Two pivots: first x enters, then y.", "Twelve chairs and six tables, for thirteen thousand two hundred rupees. Both workshops are fully booked."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Newton–Raphson: correct digits double each step")
        f = VGroup(M(r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}", size=44, color=th.MINT), T("the tangent at xₙ meets the x-axis at xₙ₊₁", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([0, 1.8, 0])
        xs = [2.0]
        for _ in range(4):
            x = xs[-1]
            xs.append(x - (x ** 3 - 2 * x - 5) / (3 * x * x - 2))
        rows = [["n", "xₙ", "error"]] + [[str(i), f"{v:.9f}", f"{abs(v - xs[-1]):.0e}" if i < 4 else "—"] for i, v in enumerate(xs[:5])]
        tb = P.table(rows, [1.0, 4.0, 2.4], row_h=0.5, size=26, colors=[th.MUTED, th.MINT, th.CORAL]).move_to([0, -1.2, 0])
        with self.say("Newton Raphson, from the cold open: x n plus one is x n minus f over f dash. Near a root, the error is squared at every step. Watch the error column: about a tenth, then five thousandths, then two hundred thousandths, then two ten-billionths. The number of correct digits roughly doubles each time.") as v:
            self.play(FadeIn(h), Write(f[0]), FadeIn(f[1]))
            P.reveal_table(self, tb, v.dur * 0.6)
        self.play(FadeOut(VGroup(h, f, tb)))
        P.worked(self, "Use Newton–Raphson to find √5 to five decimal places.",
                 [r"f(x) = x^2 - 5:\quad x_{n+1} = \frac12\left(x_n + \frac{5}{x_n}\right)", r"x_0 = 2 \to 2.25 \to 2.236111 \to 2.236068 \to 2.236068", r"\sqrt5 = 2.23607"],
                 ["Square roots, the ancient way.", "The formula becomes: average x and five over x.", "From two: two point two five, then two point two three six one one one, then the digits freeze.", "Root five is two point two three six oh seven."])
        h = P.head(self, "Trapezium vs Simpson on ∫₀¹ dx/(1 + x²) = π/4")
        ax = plot_axes([-3.2, -0.6, 0], [0, 1, 0.25], [0, 1.1, 0.25], 4.8, 4.0)
        fn = lambda x: 1 / (1 + x * x)
        cv = ax.plot(fn, x_range=[0, 1], color=th.AMBER, stroke_width=4)
        xs4 = np.linspace(0, 1, 5)
        traps = VGroup(*[Polygon(ax.c2p(a, 0), ax.c2p(a, fn(a)), ax.c2p(b, fn(b)), ax.c2p(b, 0), stroke_color=th.SKY, stroke_width=2, fill_color=th.SKY, fill_opacity=0.3) for a, b in zip(xs4, xs4[1:])])
        f2 = VGroup(M(r"T = \frac h2\left[y_0 + y_n + 2(\text{rest})\right] = 0.782794", size=30, color=th.SKY), M(r"S = \frac h3\left[y_0 + y_n + 4(\text{odd}) + 2(\text{even})\right] = 0.785392", size=30, color=th.MINT),
                    M(r"\tfrac\pi4 = 0.785398", size=34, color=th.AMBER), T("error: trapezium shrinks like h², Simpson like h⁴", size=24, color=th.MUTED), T("actual errors: 0.0026 vs 0.000006 (about 400 times smaller)", size=22, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([2.8, -0.3, 0])
        with self.say("Numerical integration. Split the area into four strips. The trapezium rule replaces the curve by straight chords: point seven eight two eight. Simpson's rule fits parabolas through three points at a time: point seven eight five three nine. The true value is pi over four."):
            self.play(FadeIn(h), Create(ax), Create(cv))
            self.play(FadeIn(traps))
            self.play(Write(f2[0]), Write(f2[1]), Write(f2[2]))
        with self.say("The trapezium error shrinks like h squared; Simpson's like h to the fourth. Here, with the same five values, Simpson is about four hundred times more accurate. Halve h, and the trapezium error falls by four, Simpson's by sixteen."):
            self.play(FadeIn(f2[3]), FadeIn(f2[4]))
        self.play(FadeOut(VGroup(h, ax, cv, traps, f2)))
        self.quiz("Gauss–Seidel is guaranteed to converge when the system is",
                  ["symmetric", "diagonally dominant", "homogeneous", "triangular"], 1,
                  "Pause and think.",
                  "Diagonally dominant: each diagonal coefficient is bigger than the sum of the others in its row.")
        self.quiz("In the simplex method, the pivot column is chosen by",
                  ["the smallest ratio", "the most negative entry in the Z row", "the largest RHS", "the first column"], 1,
                  "One more.",
                  "The most negative entry in the Z row. The smallest ratio then picks the pivot row.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Gauss elimination: clear below each pivot, back-substitute; swap rows if a pivot is 0.",
            "Gauss–Seidel: rearrange, iterate using the newest values; needs diagonal dominance.",
            "LPP: the optimum is at a corner; simplex walks corners using slack variables.",
            "Simplex: most negative Z entry → column; smallest ratio → row; pivot; repeat.",
            "Newton–Raphson doubles correct digits; trapezium error ~ h², Simpson ~ h⁴.",
        ], "Quick recap. Gauss elimination and back substitution. Gauss Seidel iteration for diagonally dominant systems. The simplex method walking from corner to corner. And the accuracy of Newton Raphson and the integration rules.")
        self.outro("That was computational methods. Next, the alternative unit, mechanics: forces, equilibrium and motion. See you there.")
