import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 5
    TITLE = "Matrix Based System of Linear Equations"
    SUBTITLE = "One equation, AX = B, three ways to solve it"
    SECTIONS = ["Cramer's rule", "Row-equivalent (Gauss) method", "Inverse matrix method", "Consistency: one, many or no solution"]
    NEXT = "Unit 6 · Properties of a Triangle"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = Axes(x_range=[-1, 6, 1], y_range=[-1, 6, 1], x_length=5.6, y_length=5.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-3.0, -0.4, 0])
        l1 = ax.plot(lambda x: (13 - 2 * x) / 3, x_range=[-1, 6], color=th.AMBER, stroke_width=4)
        m = ValueTracker(3.0)
        c = ValueTracker(-3.0)
        l2 = always_redraw(lambda: P.clipped(ax, lambda x: m.get_value() * x + c.get_value(), -1, 6, -1, 6, th.SKY, step=0.02))
        eqs = VGroup(M(r"2x + 3y = 13", size=36, color=th.AMBER), M(r"3x - y = 3", size=36, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 2.0, 0])
        pt = Dot(ax.c2p(2, 3), radius=0.11, color=th.MINT)
        ptl = M(r"(2, 3)", size=30, color=th.MINT).next_to(pt, UR, buff=0.08)
        cap = P.Captions(self, at=(3.4, -0.6, 0), width=6.0, size=26)
        with self.say("Two equations, two unknowns. Each equation is a straight line, and the solution is where the lines cross: here, the single point two, three."):
            self.play(Create(ax), Create(l1), FadeIn(eqs))
            self.add(l2)
            self.play(FadeIn(pt, scale=2), FadeIn(ptl))
            cap("crossing lines: exactly ONE solution", color=th.MINT)
        with self.say("But turn the second line until it runs parallel to the first. Now they never meet: no solution at all."):
            self.play(FadeOut(pt), FadeOut(ptl))
            e2 = M(r"2x + 3y = 6", size=36, color=th.SKY).move_to(eqs[1], aligned_edge=LEFT)
            self.play(m.animate.set_value(-2 / 3), c.animate.set_value(2.0), Transform(eqs[1], e2), run_time=2.0)
            cap("parallel lines: NO solution", color=th.CORAL)
        with self.say("Slide it onto the first, and every point of the line is a solution: infinitely many. With three unknowns the lines become planes, and guessing by eye is hopeless. This unit gives you machines that decide, and solve, every time."):
            e3 = M(r"4x + 6y = 26", size=36, color=th.SKY).move_to(eqs[1], aligned_edge=LEFT)
            self.play(c.animate.set_value(13 / 3), Transform(eqs[1], e3), run_time=1.6)
            cap("the same line: INFINITELY many solutions", color=th.AMBER)
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, l1, eqs)), FadeOut(l2))
        cap.clear()
        self.remove(l2)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 5: Matrix Based System of Linear Equations."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four parts. Cramer's rule, using determinants. The row equivalent, or Gauss, method. The inverse matrix method. And consistency: how to tell one solution from infinitely many from none.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Write the system as AX = B")
        sysm = VGroup(M(r"x + 2y + z = 8", size=34), M(r"2x + 3y - z = 5", size=34), M(r"3x - y + 2z = 7", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-4.2, 0.6, 0])
        A = P.grid([[1, 2, 1], [2, 3, -1], [3, -1, 2]], size=34).move_to([-0.3, 0.6, 0])
        X = P.grid([["x"], ["y"], ["z"]], size=34).next_to(A, RIGHT, buff=0.25)
        eq = M("=", size=40).next_to(X, RIGHT, buff=0.25)
        B = P.grid([[8], [5], [7]], size=34).next_to(eq, RIGHT, buff=0.25)
        labs = VGroup(M("A", size=36, color=th.AMBER).next_to(A, DOWN, buff=0.25), M("X", size=36, color=th.SKY).next_to(X, DOWN, buff=0.25), M("B", size=36, color=th.MINT).next_to(B, DOWN, buff=0.25))
        hl = SurroundingRectangle(VGroup(A.cells[0]), color=th.AMBER, buff=0.08)
        rd = M(r"(1)x + (2)y + (1)z = x + 2y + z", size=30, color=th.AMBER).move_to([0, -1.9, 0])
        key = para("Same order of unknowns in every equation; a missing unknown gets coefficient 0.", width=11, size=24, color=th.MUTED).move_to([0, -2.8, 0])
        with self.say("First, every method starts the same way. Line up the unknowns in the same order and read off three objects: the coefficient matrix A, the column of unknowns X, and the column of constants B."):
            self.play(FadeIn(h), Write(sysm))
            self.play(FadeIn(A), FadeIn(X), FadeIn(eq), FadeIn(B))
            self.play(FadeIn(labs))
        with self.say("Why does A X equal B say the same thing? Multiply the first row of A into the column X: x plus two y plus z. That is the left side of the first equation. A missing unknown simply gets a zero."):
            self.play(Create(hl), Write(rd))
            self.play(FadeIn(key))
        self.play(FadeOut(VGroup(h, sysm, A, X, eq, B, labs, hl, rd, key)))
        h = P.head(self, "Cramer's rule: replace a column")
        d2 = VGroup(M(r"a_1x + b_1y = c_1", size=34), M(r"a_2x + b_2y = c_2", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-4.0, 1.6, 0])
        el = VGroup(M(r"(a_1b_2 - a_2b_1)\,x = c_1b_2 - c_2b_1", size=34), M(r"x = \frac{\begin{vmatrix} c_1 & b_1 \\ c_2 & b_2 \end{vmatrix}}{\begin{vmatrix} a_1 & b_1 \\ a_2 & b_2 \end{vmatrix}} = \frac{D_x}{D},\qquad y = \frac{D_y}{D}", size=36, color=th.MINT)).arrange(DOWN, buff=0.45).move_to([1.2, 0.2, 0])
        rule = para("D: the coefficients.  Dx: D with the x-COLUMN replaced by the constants.  D ≠ 0.", width=11.5, size=25, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Cramer's rule comes from plain elimination. Multiply to kill y, subtract, and x times a determinant equals another determinant. The bottom one is D, made of the coefficients. The top one is D with the x column replaced by the constants. So x is D x over D, and y is D y over D, as long as D is not zero."):
            self.play(FadeIn(h), Write(d2))
            self.play(Write(el[0]))
            self.play(Write(el[1]))
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(h, d2, el, rule)))
        P.worked(self, "Solve by Cramer's rule: 2x + 3y = 13, 3x − y = 3.",
                 [r"D = \begin{vmatrix} 2 & 3 \\ 3 & -1 \end{vmatrix} = -2 - 9 = -11 \ne 0", r"D_x = \begin{vmatrix} 13 & 3 \\ 3 & -1 \end{vmatrix} = -22,\qquad D_y = \begin{vmatrix} 2 & 13 \\ 3 & 3 \end{vmatrix} = -33",
                  r"x = \frac{-22}{-11} = 2,\qquad y = \frac{-33}{-11} = 3"],
                 ["The cold open's system.", "D is minus two minus nine: minus eleven. Not zero, so there is exactly one solution.", "Put thirteen and three in the x column: minus twenty two. In the y column: minus thirty three.", "Divide: x is two and y is three. The crossing point we saw."], size=34)
        self.p1_three()

    def p1_three(self):
        h = P.head(self, "Three unknowns: x + y + z = 4,  x − y + z = 6,  2x + y − z = 0")
        A = [[1, 1, 1], [1, -1, 1], [2, 1, -1]]
        Bc = [4, 6, 0]
        D = P.grid(A, size=32, dx=0.85).move_to([-4.6, 1.0, 0])
        Dl = M("D =", size=34).next_to(D, LEFT, buff=0.2)
        Bg = P.grid([[b] for b in Bc], size=32, color=th.MINT).move_to([-1.8, 1.0, 0])
        Bl = M("B", size=30, color=th.MINT).next_to(Bg, DOWN, buff=0.2)
        Dv = M("= 6", size=34, color=th.AMBER).next_to(D, RIGHT, buff=0.2)
        with self.say("With three unknowns the rule is the same, with three by three determinants. Expand D along its first row: six. Not zero, so go on."):
            self.play(FadeIn(h), FadeIn(D), FadeIn(Dl))
            self.play(FadeIn(Bg), FadeIn(Bl))
            self.play(Write(Dv))
        res = VGroup()
        vals = [12, -6, 18]
        names = ["D_x", "D_y", "D_z"]
        pos = [[2.4, 1.0, 0], [-3.4, -1.5, 0], [2.4, -1.5, 0]]
        says = ["For D x, copy D and slide the constants into the first column, the x column. Expand: twelve.", "For D y, the constants go into the second column: minus six.", "And for D z, the third column: eighteen. Replace a column, never a row."]
        for k in range(3):
            cols = [[(Bc[i] if j == k else A[i][j]) for j in range(3)] for i in range(3)]
            G = P.grid(cols, size=32, dx=0.85).move_to(pos[k])
            for i in range(3):
                G.cells[i][k].set_color(th.MINT)
            lab = M(names[k] + " =", size=32).next_to(G, LEFT, buff=0.15)
            v = M(f"= {vals[k]}", size=32, color=th.AMBER).next_to(G, RIGHT, buff=0.15)
            fly = Bg.cells.copy()
            with self.say(says[k]):
                base = D.copy()
                self.play(base.animate.move_to(pos[k]), FadeIn(lab))
                self.play(*[fly[i].animate.move_to(G.cells[i][k]) for i in range(3)], *[base.cells[i][k].animate.set_opacity(0) for i in range(3)], run_time=1.0)
                self.remove(base, fly, *fly, *[c_ for r_ in fly for c_ in r_])
                self.add(G)
                self.play(Write(v))
            res.add(VGroup(G, lab, v))
        ans = M(r"x = \tfrac{12}{6} = 2,\quad y = \tfrac{-6}{6} = -1,\quad z = \tfrac{18}{6} = 3", size=38, color=th.MINT).move_to([0, -3.0, 0])
        with self.say("Divide each by D: x is two, y is minus one, z is three. Check in the third equation: four minus one minus three is zero. Correct."):
            self.play(Write(ans))
        self.play(FadeOut(VGroup(h, D, Dl, Dv, Bg, Bl, res, ans)))
        self.remove(*[r_[0] for r_ in res])
        P.worked(self, "In Bhaktapur, 2 kg apples + 3 kg oranges cost Rs 640, and 3 kg apples + 2 kg oranges cost Rs 610. Find each price per kg.",
                 [r"2x + 3y = 640,\qquad 3x + 2y = 610", r"D = 4 - 9 = -5,\quad D_x = 1280 - 1830 = -550,\quad D_y = 1220 - 1920 = -700", r"x = 110,\quad y = 140:\ \text{apples Rs 110, oranges Rs 140 per kg}"],
                 ["A word problem.", "Let apples cost x rupees a kilo and oranges y.", "D is minus five, D x minus five fifty, D y minus seven hundred.", "So apples cost a hundred and ten rupees a kilo, and oranges a hundred and forty. Check: two twenty plus four twenty is six forty."])
        c = self.callout("careful", "Cramer's rule dies when D = 0: you may not divide. The system then has no solution or infinitely many (Part 4). Writing x = 0/0 earns nothing.", width=11, size=26)
        with self.say("One warning. If D is zero, Cramer's rule says nothing at all. The system has either no solution or infinitely many, and part four shows how to tell."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["operation", "symbol", "on the equations"], ["swap two rows", "Rᵢ ↔ Rⱼ", "reorder the equations"], ["multiply a row by c ≠ 0", "Rᵢ → cRᵢ", "scale an equation"], ["add a multiple of another row", "Rᵢ → Rᵢ + cRⱼ", "add c × one equation to another"]]
        tb = P.table(rows, [4.4, 2.8, 4.8], row_h=0.7, size=25, colors=[th.INK, th.AMBER, th.MUTED]).move_to([0, 0.9, 0])
        nt = para("These are exactly the moves you make when you eliminate by hand, so they never change the solution. Apply them to the AUGMENTED matrix [A | B].", width=11.5, size=24, color=th.INK).move_to([0, -1.9, 0])
        with self.say("The second method uses three elementary row operations: swap two rows, multiply a row by a non zero number, and add a multiple of one row to another. They are exactly what you do when you eliminate by hand, so they never change the answer. We apply them to the augmented matrix: A with the constants attached.") as v:
            P.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = P.head(self, "Gauss elimination: zeros below the diagonal")
        sysm = M(r"x + 2y + z = 8,\quad 2x + 3y - z = 5,\quad 3x - y + 2z = 7", size=32).move_to([0, 2.1, 0])
        G = P.grid([[1, 2, 1, 8], [2, 3, -1, 5], [3, -1, 2, 7]], bar=3, size=38, dx=1.05, dy=0.75).move_to([-1.6, 0.2, 0])
        with self.say("Solve x plus two y plus z equals eight, two x plus three y minus z equals five, three x minus y plus two z equals seven. Write the augmented matrix."):
            self.play(FadeIn(h), Write(sysm))
            self.play(FadeIn(G))
        with self.say("Clear the first column below the leading one. Row two minus two times row one. Row three minus three times row one."):
            P.set_row(self, G, 1, [0, -1, -3, -11], r"R_2 \to R_2 - 2R_1")
            P.set_row(self, G, 2, [0, -7, -1, -17], r"R_3 \to R_3 - 3R_1")
        with self.say("Now clear the second column below its pivot, minus one. Row three minus seven times row two. The coefficient part is now triangular: echelon form."):
            P.set_row(self, G, 2, [0, 0, 20, 60], r"R_3 \to R_3 - 7R_2")
            zs = VGroup(G.cells[1][0], G.cells[2][0], G.cells[2][1])
            self.play(zs.animate.set_color(th.MINT), Indicate(zs, color=th.MINT, scale_factor=1.3))
        back = VGroup(M(r"20z = 60 \Rightarrow z = 3", size=34), M(r"-y - 3(3) = -11 \Rightarrow y = 2", size=34), M(r"x + 2(2) + 3 = 8 \Rightarrow x = 1", size=34, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.4, 0])
        with self.say("Back substitution, from the bottom up. Twenty z is sixty, so z is three. Then minus y minus nine is minus eleven, so y is two. Then x plus four plus three is eight, so x is one."):
            for b_ in back:
                self.play(Write(b_), run_time=0.9)
        self.play(FadeOut(VGroup(sysm, back)), zs.animate.set_color(th.INK))
        h2 = P.head(self, "Gauss–Jordan: keep going until [ I | X ]")
        with self.say("Gauss Jordan goes further. Make every pivot one, then clear above the pivots too."):
            self.play(Transform(h, h2))
            P.set_row(self, G, 1, [0, 1, 3, 11], r"R_2 \to -R_2")
            P.set_row(self, G, 2, [0, 0, 1, 3], r"R_3 \to \tfrac{1}{20}R_3")
        with self.say("Clear above the third pivot, then above the second. The left block becomes the identity, and the answer, one, two, three, sits in the last column. No back substitution at all."):
            P.set_row(self, G, 0, [1, 2, 0, 5], r"R_1 \to R_1 - R_3")
            P.set_row(self, G, 1, [0, 1, 0, 2], r"R_2 \to R_2 - 3R_3")
            P.set_row(self, G, 0, [1, 0, 0, 1], r"R_1 \to R_1 - 2R_2")
            lastc = SurroundingRectangle(VGroup(*[G.cells[i][3] for i in range(3)]), color=th.MINT, buff=0.1)
            ans = M(r"x = 1,\ y = 2,\ z = 3", size=38, color=th.MINT).move_to([3.8, -2.2, 0])
            self.play(Create(lastc), Write(ans))
        self.play(FadeOut(VGroup(h, G, lastc, ans)))
        P.worked(self, "Solve by Gauss elimination: y + z = 5, x + y − z = 0, 2x − y + z = 3.",
                 [r"R_1 \leftrightarrow R_2:\ (1, 1, -1 \mid 0),\ (0, 1, 1 \mid 5),\ (2, -1, 1 \mid 3)", r"R_3 \to R_3 - 2R_1:\ (0, -3, 3 \mid 3);\qquad R_3 \to R_3 + 3R_2:\ (0, 0, 6 \mid 18)",
                  r"z = 3,\quad y = 5 - 3 = 2,\quad x = 0 - 2 + 3 = 1"],
                 ["A zero where the first pivot should be.", "No problem: swap the first two rows.", "Clear the first column, then the second.", "Six z is eighteen, so z is three; then y is two and x is one."])
        self.tip("A zero in the pivot place is not an error: swap with a lower row that has a non-zero entry there. Only a WHOLE zero column below means |A| = 0 (Part 4).",
                 "Exam tip. A zero in the pivot place is not a mistake. Swap with a lower row and carry on. Only if the whole column below is zero is something special happening.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Undo A: X = A⁻¹B")
        st = VGroup(M(r"AX = B", size=42), M(r"A^{-1}(AX) = A^{-1}B", size=42), M(r"(A^{-1}A)X = IX = X", size=42), M(r"X = A^{-1}B = \frac{1}{|A|}(\mathrm{adj}\,A)\,B", size=46, color=th.MINT)).arrange(DOWN, buff=0.35).move_to([0, -0.1, 0])
        says = ["The third method undoes A. Start from A X equals B.", "Multiply both sides on the left by A inverse, which exists exactly when the determinant of A is not zero.", "A inverse times A is the identity, and the identity times X is X.",
                "So X is A inverse B. And since A inverse is the adjoint over the determinant, X is one over the determinant of A, times adjoint A, times B."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.0)
        self.play(FadeOut(VGroup(h, st)))
        h = P.head(self, "2 × 2 inverse: swap, negate, divide")
        G = P.grid([["a", "b"], ["c", "d"]], size=44, dx=1.1, dy=0.8).move_to([-3.6, 0.6, 0])
        Gl = M("A =", size=40).next_to(G, LEFT, buff=0.2)
        adj = P.grid([["a", "b"], ["c", "d"]], size=44, dx=1.1, dy=0.8).move_to([1.4, 0.6, 0])
        al = M(r"\mathrm{adj}\,A =", size=36).next_to(adj, LEFT, buff=0.2)
        res = M(r"A^{-1} = \frac{1}{ad - bc}\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}", size=42, color=th.MINT).move_to([0, -2.0, 0])
        with self.say("For a two by two matrix there is a quick recipe. Swap the two diagonal entries, a and d. Change the signs of the other two. That is the adjoint. Then divide by the determinant, a d minus b c."):
            self.play(FadeIn(h), FadeIn(G), FadeIn(Gl))
            self.play(TransformFromCopy(G, adj), FadeIn(al))
            a_, d_ = adj.cells[0][0], adj.cells[1][1]
            self.play(a_.animate.move_to(adj.cells[1][1].get_center()), d_.animate.move_to(adj.cells[0][0].get_center()), path_arc=PI / 2, run_time=1.0)
            nb_ = M("-b", size=44, color=th.CORAL).move_to(adj.cells[0][1])
            nc_ = M("-c", size=44, color=th.CORAL).move_to(adj.cells[1][0])
            self.play(Transform(adj.cells[0][1], nb_), Transform(adj.cells[1][0], nc_))
            self.play(Write(res))
        self.play(FadeOut(VGroup(h, G, Gl, adj, al, res)))
        P.worked(self, "Solve 2x + 3y = 13, 3x − y = 3 by the inverse matrix method.",
                 [r"|A| = -11,\qquad A^{-1} = \frac{1}{-11}\begin{bmatrix} -1 & -3 \\ -3 & 2 \end{bmatrix} = \frac{1}{11}\begin{bmatrix} 1 & 3 \\ 3 & -2 \end{bmatrix}",
                  r"X = \frac{1}{11}\begin{bmatrix} 1 & 3 \\ 3 & -2 \end{bmatrix}\begin{bmatrix} 13 \\ 3 \end{bmatrix} = \frac{1}{11}\begin{bmatrix} 22 \\ 33 \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}"],
                 ["The same system, a third way.", "Determinant minus eleven. Swap and negate, then divide by minus eleven.", "Multiply into the constants: twenty two and thirty three, over eleven. Two and three, as before."], size=34)
        P.worked(self, "Three numbers: their sum is 6; the first plus twice the third is 7; three times the first plus the other two is 12. Find them.",
                 [r"A = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 0 & 2 \\ 3 & 1 & 1 \end{bmatrix},\ B = \begin{bmatrix} 6 \\ 7 \\ 12 \end{bmatrix},\quad |A| = -2 + 5 + 1 = 4",
                  r"\mathrm{adj}\,A = \begin{bmatrix} -2 & 0 & 2 \\ 5 & -2 & -1 \\ 1 & 2 & -1 \end{bmatrix}\ (\text{cofactors, transposed})",
                  r"X = \frac14\begin{bmatrix} -12 + 0 + 24 \\ 30 - 14 - 12 \\ 6 + 14 - 12 \end{bmatrix} = \frac14\begin{bmatrix} 12 \\ 4 \\ 8 \end{bmatrix} = \begin{bmatrix} 3 \\ 1 \\ 2 \end{bmatrix}"],
                 ["A three by three.", "Note the zero for the missing y in the second equation. Determinant four.", "Find all nine cofactors and transpose them: that is the adjoint.", "Multiply by B and divide by four. The numbers are three, one and two. Check: three plus four is seven."], size=32)
        P.worked(self, "A Pokhara hotel: 2 singles + 1 double + 1 deluxe = Rs 9000; 1 + 2 + 1 = Rs 10 000; 1 + 1 + 2 = Rs 12 000. Find the tariffs.",
                 [r"2x + y + z = 9000,\quad x + 2y + z = 10\,000,\quad x + y + 2z = 12\,000;\quad |A| = 4", r"\text{add all three: } 4(x + y + z) = 31\,000 \Rightarrow x + y + z = 7750", r"x = 1250,\quad y = 2250,\quad z = 4250"],
                 ["A real-world system.", "Determinant four, so one solution exists. The inverse method works, but look first for a shortcut.", "Adding all three equations gives four times x plus y plus z: thirty one thousand. So x plus y plus z is seven thousand seven hundred and fifty.",
                  "Subtract it from each equation: single twelve fifty, double twenty two fifty, deluxe forty two fifty."])
        c = self.callout("careful", "X = A⁻¹B: multiply on the LEFT. BA⁻¹ is not even defined (3×1 times 3×3). And compute |A| first: if |A| = 0 there is no inverse.", width=11, size=26)
        with self.say("Two warnings. Multiply on the left: B times A inverse is not even defined. And find the determinant first: if it is zero, there is no inverse."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        rows = [["method", "needs", "best when"], ["Cramer", "|A| ≠ 0", "2–3 unknowns, small numbers"], ["inverse", "|A| ≠ 0", "many systems, same A"], ["Gauss", "nothing", "always: the only one if |A| = 0"]]
        tb = P.table(rows, [2.6, 2.6, 6.8], row_h=0.72, size=26, colors=[th.AMBER, th.INK, th.MUTED]).move_to([0, 0.2, 0])
        with self.say("Which method? Cramer needs a non zero determinant and is quickest for small systems. The inverse also needs a non zero determinant, and pays off when many systems share the same A. Row reduction needs nothing, and it is the only one that still works when the determinant is zero.") as v:
            P.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Read the last row")
        cases = [([[1, 2, 1, 8], [0, -1, -3, -11], [0, 0, 20, 60]], "|A| ≠ 0: exactly ONE solution", th.MINT, "consistent, unique"),
                 ([[1, 1, 1, 6], [0, 1, 2, 8], [0, 0, 0, 0]], "0 = 0: INFINITELY many", th.AMBER, "consistent, dependent"),
                 ([[1, 1, 1, 6], [0, 1, 2, 8], [0, 0, 0, 1]], "0 = 1: NO solution", th.CORAL, "inconsistent")]
        gs = VGroup()
        for k, (rows, lab, col, sub) in enumerate(cases):
            g = P.grid(rows, bar=3, size=32, dx=0.8, dy=0.58)
            for c_ in g.cells[2]:
                c_.set_color(col)
            gs.add(VGroup(g, T(lab, size=22, color=col, weight="BOLD").next_to(g, DOWN, buff=0.3), T(sub, size=20, color=th.MUTED).next_to(g, DOWN, buff=0.75)))
        gs.arrange(RIGHT, buff=0.7).move_to([0, 0.5, 0])
        says = ["Row reduce the augmented matrix, and look at the last row. It can only look one of three ways. A non zero pivot: one unique solution.",
                "A whole row of zeros, zero equals zero: true but empty. Only two real equations remain for three unknowns, so there are infinitely many solutions.",
                "Zeros on the left but not on the right: zero equals one. Impossible. The equations contradict each other, and there is no solution."]
        self.play(FadeIn(h))
        for g, sy in zip(gs, says):
            with self.say(sy):
                self.play(FadeIn(g, shift=UP * 0.2))
        key = para("Determinant test: |A| ≠ 0 → one solution.  |A| = 0 → no unique solution: row reduce to decide between many and none. A homogeneous system (B = 0) always has x = y = z = 0.", width=12, size=23, color=th.INK).move_to([0, -2.6, 0])
        with self.say("The determinant gives the first split. Not zero: one solution. Zero: then row reduce to tell many from none. A homogeneous system, with B all zeros, is never inconsistent, because zero, zero, zero always works.") as v:
            self.play(FadeIn(key))
        self.play(FadeOut(VGroup(h, gs, key)))
        P.worked(self, "Show that x + y + z = 6, 2x + 3y + 4z = 20, x + 2y + 3z = 14 has infinitely many solutions, and find them.",
                 [r"|A| = 1(9-8) - 1(6-4) + 1(4-3) = 0", r"R_2 - 2R_1,\ R_3 - R_1:\ (0, 1, 2 \mid 8),\ (0, 1, 2 \mid 8);\quad R_3 - R_2:\ (0, 0, 0 \mid 0)", r"z = t:\quad y = 8 - 2t,\quad x = 6 - y - z = t - 2", r"(x, y, z) = (t - 2,\ 8 - 2t,\ t),\ \ t \in \mathbb{R}"],
                 ["Many solutions.", "The determinant is zero, so no unique solution.", "Row reduce: the second and third rows become identical, and the last row vanishes. Zero equals zero.", "Two equations, three unknowns. Let z be any number t. Then y is eight minus two t, and x is t minus two.",
                  "A whole line of solutions, one for every real t. Put t equal to two: zero, four, two. Check: six, twenty, fourteen."])
        P.worked(self, "Show that x + y + z = 6, 2x + 3y + 4z = 20, x + 2y + 3z = 15 is inconsistent.",
                 [r"|A| = 0\ \text{(same A)}", r"R_2 - 2R_1:\ (0, 1, 2 \mid 8);\quad R_3 - R_1:\ (0, 1, 2 \mid 9)", r"R_3 - R_2:\ (0, 0, 0 \mid 1),\ \text{i.e. } 0 = 1:\ \text{no solution}"],
                 ["Change one number.", "Same coefficients, so the determinant is still zero.", "This time the two reduced rows differ in the constant: eight and nine.", "Subtract: zero equals one. Impossible. Changing fourteen to fifteen turned infinitely many solutions into none."])
        P.worked(self, "For x + y + z = 6, x + 2y + 3z = 10, x + 2y + λz = μ, find when there is (i) a unique solution, (ii) none, (iii) infinitely many.",
                 [r"|A| = 1(2\lambda - 6) - 1(\lambda - 3) + 0 = \lambda - 3", r"\text{(i) } \lambda \ne 3:\ \text{unique, for every } \mu", r"\lambda = 3:\ \text{last row becomes } (0, 0, 0 \mid \mu - 10)", r"\text{(ii) } \lambda = 3,\ \mu \ne 10:\ \text{none};\qquad \text{(iii) } \lambda = 3,\ \mu = 10:\ \text{infinitely many}"],
                 ["The board's favourite.", "The determinant is lambda minus three.", "If lambda is not three, the determinant is not zero: a unique solution, whatever mu is.", "If lambda is three, row reduce: the last row becomes zero, zero, zero, mu minus ten.",
                  "So if mu is not ten, zero equals something non zero: no solution. If mu is ten, zero equals zero: infinitely many."])
        self.quiz("If |A| = 0 for a system AX = B, then the system",
                  ["has exactly one solution", "has no solution", "has no unique solution", "is always inconsistent"], 2,
                  "Pause and think. The determinant of A is zero. What can you say for certain?",
                  "It has no unique solution. It may have none, or infinitely many: only row reduction decides. Always inconsistent is wrong: a homogeneous system with a zero determinant has infinitely many.")
        self.quiz("In Cramer's rule, Dy is D with",
                  ["row 1 replaced by B", "column 2 replaced by B", "row 2 replaced by B", "B added to each column"], 1,
                  "One more. How is D y built?",
                  "The second column, the y column, replaced by the constants. Replace a column, never a row.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Write AX = B: unknowns in the same order, 0 for a missing one.",
            "Cramer: x = Dx/D, y = Dy/D, z = Dz/D, replacing a COLUMN by B; needs D ≠ 0.",
            "Gauss: row-reduce [A | B] to echelon form, back-substitute. Gauss–Jordan: on to [I | X].",
            "Inverse: X = A⁻¹B = (adj A)B/|A|, multiplying on the LEFT; needs |A| ≠ 0.",
            "Last row: pivot → one solution; 0 = 0 → infinitely many; 0 = 1 → none.",
        ], "Quick recap. Write A X equals B. Cramer replaces a column by the constants and divides by D. Gauss row reduces the augmented matrix; Gauss Jordan goes on to the identity. The inverse method left multiplies by A inverse. And the last row tells you: one solution, infinitely many, or none.")
        self.outro("That was systems of linear equations. Next, properties of a triangle: the sine, cosine and projection laws. See you there.")
