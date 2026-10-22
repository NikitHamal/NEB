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


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 12
    TITLE = "Derivatives"
    SUBTITLE = "Slopes, rates and the best possible answer"
    SECTIONS = ["Hyperbolic functions", "L'Hospital's rule", "Differentials", "Tangent and normal", "Rates of change", "Increasing, decreasing, maxima and minima", "Concavity and inflection"]
    NEXT = "Unit 13 · Anti-derivatives"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        sheet = Square(side_length=3.6, stroke_color=th.INK, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to([-4.0, 0.2, 0])
        x = ValueTracker(0.6)
        u = 3.6 / 18

        def cut():
            c = x.get_value() * u
            g = VGroup()
            for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
                corner = sheet.get_center() + np.array([sx * 1.8, sy * 1.8, 0])
                g.add(Square(side_length=c, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.8).move_to(corner - np.array([sx * c / 2, sy * c / 2, 0])))
            return g

        ax = plot_axes([2.6, 0.0, 0], [0, 9, 1], [0, 450, 100], 5.6, 4.0)
        lab = VGroup(T("cut x (cm)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35), T("volume", size=20, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        V = ax.plot(lambda t: t * (18 - 2 * t) ** 2, x_range=[0, 9], color=th.AMBER, stroke_width=4)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), x.get_value() * (18 - 2 * x.get_value()) ** 2), color=th.AMBER, radius=0.1))
        c_ = always_redraw(cut)
        rd = always_redraw(lambda: VGroup(T("x =", size=26), DecimalNumber(x.get_value(), num_decimal_places=1, font_size=34, color=th.CORAL), T("  V =", size=26), DecimalNumber(x.get_value() * (18 - 2 * x.get_value()) ** 2, num_decimal_places=0, font_size=34, color=th.AMBER)).arrange(RIGHT, buff=0.12).move_to([-4.0, -2.4, 0]))
        with self.say("Take a square sheet of tin, eighteen centimetres a side. Cut a small square from each corner and fold up the flaps: an open box. Cut too little and the box is shallow. Cut too much and the base vanishes."):
            self.play(FadeIn(sheet), Create(ax), FadeIn(lab))
            self.add(c_, dot, rd)
            self.play(Create(V), x.animate.set_value(7.5), run_time=3.0)
        with self.say("Somewhere in between is the biggest possible box. At the top of the curve the slope is zero. Derivatives find it exactly: cut three centimetres, and the box holds four hundred and thirty two cubic centimetres. This unit is about using derivatives: for slopes, rates, approximations and the best possible answer."):
            self.play(x.animate.set_value(3.0), run_time=2.0)
            tl = Line(ax.c2p(1.2, 432), ax.c2p(4.8, 432), color=th.MINT, stroke_width=4)
            self.play(Create(tl))
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(sheet, ax, lab, V, tl)), FadeOut(c_), FadeOut(dot), FadeOut(rd))
        self.remove(c_, dot, rd)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 12: Derivatives."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Seven parts. Hyperbolic functions and their derivatives. L'Hospital's rule for awkward limits. Differentials and small errors. Tangents and normals. Rates of change. Increasing functions, maxima and minima. And concavity.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "cosh and sinh: the unit hyperbola")
        ax = plot_axes([-2.8, -0.5, 0], [-1, 4, 1], [-3, 3, 1], 4.6, 5.4)
        hyp = ax.plot_parametric_curve(lambda t: np.array([np.cosh(t), np.sinh(t)]), t_range=[-1.8, 1.8], color=th.CORAL, stroke_width=4)
        t = ValueTracker(0.3)
        pt = always_redraw(lambda: VGroup(Dot(ax.c2p(np.cosh(t.get_value()), np.sinh(t.get_value())), color=th.AMBER, radius=0.1),
                                          Line(ax.c2p(np.cosh(t.get_value()), 0), ax.c2p(np.cosh(t.get_value()), np.sinh(t.get_value()) + 1e-3), color=th.SKY, stroke_width=4),
                                          Line(ax.c2p(0, 0), ax.c2p(np.cosh(t.get_value()), 0), color=th.MINT, stroke_width=5)))
        rd = always_redraw(lambda: VGroup(VGroup(T("cosh t =", size=24, color=th.MINT), DecimalNumber(np.cosh(t.get_value()), num_decimal_places=2, font_size=30, color=th.MINT)).arrange(RIGHT, buff=0.12),
                                          VGroup(T("sinh t =", size=24, color=th.SKY), DecimalNumber(np.sinh(t.get_value()), num_decimal_places=2, font_size=30, color=th.SKY)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 2.2, 0]))
        f = VGroup(M(r"\cosh x = \frac{e^x + e^{-x}}{2},\quad \sinh x = \frac{e^x - e^{-x}}{2}", size=32), M(r"\cosh^2 x - \sinh^2 x = 1", size=36, color=th.CORAL),
                   M(r"\frac{d}{dx}\sinh x = \cosh x,\quad \frac{d}{dx}\cosh x = \sinh x", size=32, color=th.AMBER), M(r"\frac{d}{dx}\tanh x = \operatorname{sech}^2 x", size=32, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([3.4, -0.9, 0])
        with self.say("Cos and sin trace the unit circle. Their cousins, the hyperbolic cosine and sine, built from e to the x and e to the minus x, trace the unit hyperbola, x squared minus y squared equals one. So cosh squared minus sinh squared is always one."):
            self.play(FadeIn(h), Create(ax), Create(hyp))
            self.add(pt, rd)
            self.play(t.animate.set_value(1.4), run_time=1.8)
            self.play(t.animate.set_value(-1.2), run_time=1.8)
            self.play(Write(f[0]), Write(f[1]))
        with self.say("Differentiate straight from the exponential definitions: the derivative of sinh is cosh, and of cosh is sinh, with no minus sign at all, unlike cos. And tanh differentiates to sech squared."):
            self.play(Write(f[2]), Write(f[3]))
        self.play(FadeOut(VGroup(h, ax, hyp, f)), FadeOut(pt), FadeOut(rd))
        self.remove(pt, rd)
        rows = [["y", "dy/dx"], ["sinh⁻¹ x", "1 / √(x² + 1)"], ["cosh⁻¹ x", "1 / √(x² − 1),  x > 1"], ["tanh⁻¹ x", "1 / (1 − x²),  |x| < 1"]]
        tb = P.table(rows, [3.0, 5.4], row_h=0.72, size=28, colors=[th.SKY, th.AMBER]).move_to([0, 0.8, 0])
        nt = para("Compare sin⁻¹x → 1/√(1 − x²): the hyperbolic versions swap the signs inside the root.", width=11, size=24, color=th.MUTED).move_to([0, -1.8, 0])
        with self.say("And the inverse hyperbolic functions. Inverse sinh differentiates to one over root of x squared plus one; inverse cosh to one over root of x squared minus one; inverse tanh to one over one minus x squared. Compare them with the inverse trig derivatives: the signs inside swap.") as v:
            P.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        P.worked(self, "Differentiate (a) cosh(x² + 1), (b) ln(cosh x), (c) sinh x cosh x, (d) sinh⁻¹(x/3).",
                 [r"\text{(a) } 2x\sinh(x^2 + 1)\qquad \text{(b) } \frac{\sinh x}{\cosh x} = \tanh x", r"\text{(c) } \cosh^2 x + \sinh^2 x = \cosh 2x",
                  r"\text{(d) } \frac{1}{\sqrt{x^2/9 + 1}}\cdot\frac13 = \frac{1}{\sqrt{x^2 + 9}}"],
                 ["Four quick ones.", "Chain rule for the first: two x sinh of x squared plus one. The second is one over cosh times sinh: tanh x.", "Product rule: cosh squared plus sinh squared, which is cosh two x.", "And the inverse sinh of x over three tidies up to one over root of x squared plus nine."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "L'Hospital: near a, compare the slopes")
        ax = plot_axes([-2.6, -0.6, 0], [-1.2, 1.2, 0.5], [-1.2, 1.2, 0.5], 5.4, 5.0, nums=False)
        f = ax.plot(lambda x: np.sin(2 * x), x_range=[-1.2, 1.2], color=th.AMBER, stroke_width=4)
        g = ax.plot(lambda x: x + 0.3 * x * x, x_range=[-1.2, 1.2], color=th.SKY, stroke_width=4)
        lab = VGroup(M("f(x) = \\sin 2x", size=28, color=th.AMBER).next_to(ax.c2p(0.5, 0.95), UP, buff=0.05), M("g(x)", size=28, color=th.SKY).next_to(ax.c2p(1.1, 1.1), RIGHT, buff=0.05))
        tf = Line(ax.c2p(-0.5, -1.0), ax.c2p(0.5, 1.0), color=th.AMBER, stroke_width=2, stroke_opacity=0.6)
        tg = Line(ax.c2p(-1.0, -1.0), ax.c2p(1.0, 1.0), color=th.SKY, stroke_width=2, stroke_opacity=0.6)
        rule = VGroup(M(r"\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}", size=40, color=th.MINT), T("when the form is 0/0 or ∞/∞", size=26, color=th.MUTED),
                      M(r"\lim_{x\to0}\frac{\sin 2x}{x} = \lim_{x\to0}\frac{2\cos 2x}{1} = 2", size=34, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([3.4, 0.0, 0])
        with self.say("A limit like sin two x over x is nought over nought at zero: useless as it stands. But look at the graphs near zero. Both pass through the origin, and close in, each looks like its tangent line. So their ratio approaches the ratio of their slopes."):
            self.play(FadeIn(h), Create(ax), Create(f), Create(g), FadeIn(lab))
            self.play(Create(tf), Create(tg))
        with self.say("That is L'Hospital's rule. For a nought over nought, or infinity over infinity form, differentiate the top and the bottom separately, not as a quotient, and take the limit again. Sin two x over x becomes two cos two x over one: two."):
            for r_ in rule:
                self.play(Write(r_), run_time=0.9)
        self.play(FadeOut(VGroup(h, ax, f, g, lab, tf, tg, rule)))
        P.worked(self, "Evaluate lim (x→0) (eˣ − e⁻ˣ − 2x)/(x − sin x).",
                 [r"\frac{0}{0}:\ \lim \frac{e^x + e^{-x} - 2}{1 - \cos x}\quad \left(\tfrac00\right)", r"= \lim \frac{e^x - e^{-x}}{\sin x}\quad \left(\tfrac00\right)", r"= \lim \frac{e^x + e^{-x}}{\cos x} = \frac{2}{1} = 2"],
                 ["Sometimes once is not enough.", "Check the form: nought over nought. Differentiate top and bottom. Still nought over nought.", "Again: still nought over nought.", "A third time: e to the zero plus e to the zero, over cos zero. Two."])
        P.worked(self, "Evaluate (a) lim (x→∞) x²/eˣ, (b) lim (x→0⁺) x ln x, (c) lim (x→0⁺) xˣ.",
                 [r"\text{(a) } \frac{\infty}{\infty}:\ \lim\frac{2x}{e^x} = \lim\frac{2}{e^x} = 0", r"\text{(b) } 0\cdot\infty:\ \lim\frac{\ln x}{1/x} = \lim\frac{1/x}{-1/x^2} = \lim(-x) = 0", r"\text{(c) } y = x^x,\ \ln y = x\ln x \to 0 \Rightarrow y \to e^0 = 1"],
                 ["Other indeterminate forms.", "Infinity over infinity: twice, and the exponential wins. Zero.", "Nought times infinity is not a quotient, so rewrite it as log x over one over x. Then the rule gives minus x, which goes to zero.", "Nought to the nought: take logs. Log y is x log x, which we just found tends to zero, so y tends to one."])
        c = self.callout("careful", "Differentiate top and bottom SEPARATELY — not the quotient rule. And check the form every time: if it is not 0/0 or ∞/∞, the rule gives nonsense.", width=11, size=26)
        with self.say("Two warnings. It is not the quotient rule: differentiate top and bottom separately. And check the form before every step; once it stops being nought over nought, stop."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "dy along the tangent ≈ Δy along the curve")
        ax = plot_axes([-2.6, -0.6, 0], [0, 4, 1], [0, 3, 1], 5.6, 4.6, nums=False)
        fn = lambda x: np.sqrt(x) * 1.2
        cv = ax.plot(fn, x_range=[0.05, 4], color=th.AMBER, stroke_width=4)
        x0 = 1.2
        dx = ValueTracker(1.6)
        slope = 1.2 / (2 * np.sqrt(x0))

        def pic():
            d = dx.get_value()
            g = VGroup(Line(ax.c2p(0.2, fn(x0) + slope * (0.2 - x0)), ax.c2p(4, fn(x0) + slope * (4 - x0)), color=th.SKY, stroke_width=3),
                       Dot(ax.c2p(x0, fn(x0)), color=th.INK), Line(ax.c2p(x0, fn(x0)), ax.c2p(x0 + d, fn(x0)), color=th.MUTED, stroke_width=3),
                       Line(ax.c2p(x0 + d, fn(x0)), ax.c2p(x0 + d, fn(x0) + slope * d), color=th.SKY, stroke_width=7),
                       Line(ax.c2p(x0 + d, fn(x0) + slope * d), ax.c2p(x0 + d, fn(x0 + d)), color=th.CORAL, stroke_width=7))
            return g

        pc = always_redraw(pic)
        labs = VGroup(M(r"dx = \Delta x", size=28, color=th.MUTED), M(r"dy = f'(x)\,dx", size=30, color=th.SKY), M(r"\Delta y - dy \text{ (error)}", size=28, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.6, 0])
        f = VGroup(M(r"f(x + \Delta x) \approx f(x) + f'(x)\,\Delta x", size=36, color=th.MINT), T("the red gap shrinks much faster than Δx", size=24, color=th.MUTED)).arrange(DOWN, buff=0.25).move_to([3.4, -1.0, 0])
        with self.say("Near a point, a curve and its tangent almost agree. Step dx along the x axis. The true change in y, along the curve, is delta y. The change along the tangent, f dash of x times dx, is the differential dy. The red gap between them is the error."):
            self.play(FadeIn(h), Create(ax), Create(cv))
            self.add(pc)
            self.play(FadeIn(labs))
        with self.say("Shrink the step and the red gap vanishes much faster than the step itself. So for small changes, f of x plus delta x is approximately f of x plus f dash of x times delta x."):
            self.play(dx.animate.set_value(0.4), run_time=2.5)
            self.play(Write(f[0]), FadeIn(f[1]))
        self.play(FadeOut(VGroup(h, ax, cv, labs, f)), FadeOut(pc))
        self.remove(pc)
        P.worked(self, "Use differentials to approximate √49.5.",
                 [r"y = \sqrt x,\ x = 49,\ \Delta x = 0.5:\quad dy = \frac{1}{2\sqrt{49}}(0.5) = \frac{0.5}{14} = 0.0357", r"\sqrt{49.5} \approx 7 + 0.0357 = 7.0357\quad (\text{true } 7.03562)"],
                 ["Pick a nearby perfect square.", "Root forty nine is seven; the derivative there is one over fourteen; times a half: point zero three five seven.", "So root forty nine point five is about seven point zero three five seven: right to four places."])
        P.worked(self, "A sphere's radius is 7 cm with a possible error of 0.02 cm. Find the error in its volume, and the percentage error for a cube of side 10 ± 0.01 cm.",
                 [r"V = \tfrac43\pi r^3:\ dV = 4\pi r^2\,dr = 4\pi(49)(0.02) = 3.92\pi \approx 12.32\ \text{cm}^3", r"\frac{dV}{V} = 3\frac{dr}{r}:\ \text{relative errors are tripled by cubing}", r"\text{cube: } \tfrac{0.01}{10} = 0.1\% \Rightarrow \text{volume error } 3 \times 0.1\% = 0.3\%"],
                 ["Errors.", "The volume error is four pi r squared times d r: about twelve point three cubic centimetres.", "Divide by V: the relative error in a cube of anything is three times the relative error in the length.", "So a point one per cent error in a cube's side gives a point three per cent error in its volume."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Tangent and normal: slope m and −1/m")
        ax = plot_axes([-2.4, -0.7, 0], [-2.5, 3, 1], [-1, 6, 1], 5.4, 5.0, nums=True)
        fn = lambda x: x ** 3 - 3 * x + 2
        cv = P.clipped(ax, fn, -2.5, 3, -1, 6, th.AMBER)
        x = ValueTracker(-1.5)

        def lines_():
            a = x.get_value()
            m = 3 * a * a - 3
            p_ = np.array(ax.c2p(a, fn(a)))
            d = np.array(ax.c2p(1, m)) - np.array(ax.c2p(0, 0))
            d /= np.linalg.norm(d)
            nrm = np.array([-d[1], d[0], 0])
            return VGroup(Line(p_ - 1.8 * d, p_ + 1.8 * d, color=th.SKY, stroke_width=4), Line(p_ - 1.2 * nrm, p_ + 1.2 * nrm, color=th.PINK, stroke_width=3), Dot(p_, color=th.INK),
                          RightAngle(Line(p_, p_ + d), Line(p_, p_ + nrm), length=0.18, color=th.MUTED))

        def rd():
            a = x.get_value()
            return VGroup(T("tangent slope m =", size=24, color=th.SKY), DecimalNumber(3 * a * a - 3, num_decimal_places=2, font_size=32, color=th.SKY)).arrange(RIGHT, buff=0.15).move_to([3.6, 2.2, 0])

        ln, r_ = always_redraw(lines_), always_redraw(rd)
        f = VGroup(M(r"\text{tangent: } y - y_1 = m(x - x_1),\ \ m = \left.\tfrac{dy}{dx}\right|_{(x_1, y_1)}", size=30), M(r"\text{normal: } y - y_1 = -\tfrac1m(x - x_1)", size=30, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.8, 0])
        with self.say("The derivative at a point is the slope of the tangent there. The normal is perpendicular to the tangent, so its slope is minus one over m. Slide along y equals x cubed minus three x plus two and watch the slope change."):
            self.play(FadeIn(h), Create(ax), Create(cv))
            self.add(ln, r_)
            self.play(x.animate.set_value(1.9), run_time=3.5)
            self.play(Write(f[0]), Write(f[1]))
        self.play(FadeOut(VGroup(h, ax, cv, f)), FadeOut(ln), FadeOut(r_))
        self.remove(ln, r_)
        P.worked(self, "Find the tangent and normal to y = x³ − 3x + 2 at (2, 4).",
                 [r"\frac{dy}{dx} = 3x^2 - 3 \Rightarrow m = 9", r"\text{tangent: } y - 4 = 9(x - 2) \Rightarrow y = 9x - 14", r"\text{normal: } y - 4 = -\tfrac19(x - 2) \Rightarrow x + 9y - 38 = 0"],
                 ["Exactly the curve we just explored.", "At x equals two the slope is nine.", "Tangent: y equals nine x minus fourteen.", "Normal: slope minus a ninth, so x plus nine y minus thirty eight equals zero."])
        P.worked(self, "Find the angle between y = x² and y² = x at (1, 1).",
                 [r"y = x^2:\ m_1 = 2x = 2;\qquad y^2 = x:\ 2y\,y' = 1 \Rightarrow m_2 = \tfrac12", r"\tan\theta = \left|\frac{m_1 - m_2}{1 + m_1m_2}\right| = \frac{3/2}{2} = \frac34 \Rightarrow \theta = 36^\circ 52'"],
                 ["The angle between two curves is the angle between their tangents.", "Slopes at one, one: two, and, by implicit differentiation, a half.", "Tan theta is m one minus m two over one plus their product: three quarters. Thirty six degrees fifty two minutes."])

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "A 5 m ladder slides down a wall")
        wall = Line([-2.6, -2.8, 0], [-2.6, 2.2, 0], color=th.MUTED, stroke_width=5)
        ground = Line([-2.6, -2.8, 0], [3.0, -2.8, 0], color=th.MUTED, stroke_width=5)
        s = 0.9
        xt = ValueTracker(1.5)
        O = np.array([-2.6, -2.8, 0])

        def lad():
            xv = xt.get_value()
            yv = np.sqrt(25 - xv * xv)
            return VGroup(Line(O + RIGHT * xv * s, O + UP * yv * s, color=th.AMBER, stroke_width=8), M("x", size=28, color=th.SKY).move_to(O + RIGHT * xv * s / 2 + DOWN * 0.3), M("y", size=28, color=th.PINK).move_to(O + UP * yv * s / 2 + LEFT * 0.3))

        def rd():
            xv = xt.get_value()
            yv = np.sqrt(25 - xv * xv)
            return VGroup(VGroup(M("x =", size=30), DecimalNumber(xv, num_decimal_places=2, font_size=34, color=th.SKY)).arrange(RIGHT, buff=0.12),
                          VGroup(M("y =", size=30), DecimalNumber(yv, num_decimal_places=2, font_size=34, color=th.PINK)).arrange(RIGHT, buff=0.12),
                          VGroup(M(r"\tfrac{dy}{dt} =", size=30), DecimalNumber(-xv / yv * 2, num_decimal_places=2, font_size=34, color=th.CORAL), T("m/s", size=22)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 1.6, 0])

        ld, r_ = always_redraw(lad), always_redraw(rd)
        st = VGroup(M(r"x^2 + y^2 = 25", size=34), M(r"2x\frac{dx}{dt} + 2y\frac{dy}{dt} = 0", size=34), M(r"x = 4,\ y = 3:\ \frac{dy}{dt} = -\frac43(2) = -\frac83\ \text{m/s}", size=32, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -1.4, 0])
        with self.say("Rates of change are derivatives with respect to time. A five metre ladder leans on a wall, and its foot is pulled away at two metres per second. The foot moves steadily, but watch the top: it starts slowly, then plunges faster and faster."):
            self.play(FadeIn(h), Create(wall), Create(ground))
            self.add(ld, r_)
            self.play(xt.animate.set_value(4.0), run_time=3.5, rate_func=rate_functions.linear)
        with self.say("The link between x and y is Pythagoras: x squared plus y squared is twenty five. Differentiate with respect to time. When the foot is four metres out, the top is three metres up, and it is falling at eight thirds metres per second. The minus sign means y is decreasing."):
            for s_ in st:
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, wall, ground, st)), FadeOut(ld), FadeOut(r_))
        self.remove(ld, r_)
        h = P.head(self, "Water pouring into a cone")
        tip = np.array([-3.4, -2.6, 0])
        Hh, Rr = 4.6, 2.3
        cone = VGroup(Line(tip, tip + np.array([-Rr, Hh, 0]), color=th.INK, stroke_width=3), Line(tip, tip + np.array([Rr, Hh, 0]), color=th.INK, stroke_width=3),
                      DashedLine(tip + np.array([-Rr, Hh, 0]), tip + np.array([Rr, Hh, 0]), color=th.MUTED))
        hv = ValueTracker(0.3)
        water = always_redraw(lambda: Polygon(tip, tip + np.array([-hv.get_value() / 2, hv.get_value(), 0]), tip + np.array([hv.get_value() / 2, hv.get_value(), 0]), stroke_width=0, fill_color=th.SKY, fill_opacity=0.6))
        st = VGroup(M(r"\frac rh = \frac{5}{10} \Rightarrow r = \frac h2", size=32), M(r"V = \tfrac13\pi r^2h = \frac{\pi h^3}{12}", size=34), M(r"\frac{dV}{dt} = \frac{\pi h^2}{4}\frac{dh}{dt}", size=34),
                    M(r"3 = 4\pi\frac{dh}{dt} \Rightarrow \frac{dh}{dt} = \frac{3}{4\pi} \approx 0.239\ \text{m/min}", size=32, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.8, -0.2, 0])
        with self.say("Water pours at a steady three cubic metres a minute into a cone ten metres deep with a five metre radius. The level rises fast at first and slows as the cone widens."):
            self.play(FadeIn(h), Create(cone))
            self.add(water)
            self.play(hv.animate.set_value(4.2), run_time=3.0, rate_func=lambda t: t ** (1 / 3))
        with self.say("Similar triangles give r equals h over two, which removes r. So V is pi h cubed over twelve. Differentiate with respect to time, put in three and h equals four: the level is rising at three over four pi, about a quarter of a metre a minute."):
            for s_ in st:
                self.play(Write(s_), run_time=0.8)
        self.play(FadeOut(VGroup(h, cone, st)), FadeOut(water))
        self.remove(water)
        P.worked(self, "Air is pumped into a spherical balloon at 100 cm³/s. How fast is the radius growing when r = 15 cm?",
                 [r"\frac{dV}{dt} = 4\pi r^2\frac{dr}{dt}", r"100 = 4\pi(225)\frac{dr}{dt} \Rightarrow \frac{dr}{dt} = \frac{1}{9\pi} \approx 0.0354\ \text{cm/s}"],
                 ["One more rate.", "Differentiate the volume with respect to time.", "Substitute: one over nine pi, about point zero three five centimetres per second."])
        self.tip("Rates recipe: draw and label, write the equation linking the quantities (remove extra variables with a constraint), differentiate with respect to t, THEN substitute the numbers.",
                 "Exam tip. Draw it, link the quantities by one equation, differentiate with respect to time, and only then put in the numbers.")

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "The sign of f′ tells you the direction")
        ax = plot_axes([-2.4, 0.4, 0], [0, 3, 1], [3, 15, 3], 5.4, 3.2, nums=True)
        fn = lambda x: 2 * x ** 3 - 9 * x ** 2 + 12 * x + 5
        cv = ax.plot(fn, x_range=[0, 3], color=th.AMBER, stroke_width=4)
        ax2 = plot_axes([-2.4, -2.4, 0], [0, 3, 1], [-3, 7, 2], 5.4, 1.8, nums=False)
        dcv = ax2.plot(lambda x: 6 * (x - 1) * (x - 2), x_range=[0, 3], color=th.SKY, stroke_width=4)
        l2 = M("f'(x) = 6(x - 1)(x - 2)", size=26, color=th.SKY).next_to(ax2, LEFT, buff=0.1).shift(UP * 0.6 + RIGHT * 1.2)
        x = ValueTracker(0.2)
        pt = always_redraw(lambda: VGroup(Dot(ax.c2p(x.get_value(), fn(x.get_value())), color=th.INK), Dot(ax2.c2p(x.get_value(), 6 * (x.get_value() - 1) * (x.get_value() - 2)), color=th.INK),
                                          DashedLine(ax.c2p(x.get_value(), fn(x.get_value())), ax2.c2p(x.get_value(), 6 * (x.get_value() - 1) * (x.get_value() - 2)), color=th.FAINT)))
        word = always_redraw(lambda: T("rising: f′ > 0" if 6 * (x.get_value() - 1) * (x.get_value() - 2) > 0.05 else ("falling: f′ < 0" if 6 * (x.get_value() - 1) * (x.get_value() - 2) < -0.05 else "turning: f′ = 0"),
                                       size=30, color=th.MINT if 6 * (x.get_value() - 1) * (x.get_value() - 2) > 0.05 else (th.CORAL if 6 * (x.get_value() - 1) * (x.get_value() - 2) < -0.05 else th.AMBER), weight="BOLD").move_to([3.8, 2.2, 0]))
        with self.say("Where the derivative is positive the graph climbs; where it is negative the graph falls. Here is f of x equals two x cubed minus nine x squared plus twelve x plus five, and below it, its derivative, six times x minus one times x minus two."):
            self.play(FadeIn(h), Create(ax), Create(cv), Create(ax2), Create(dcv), FadeIn(l2))
            self.add(pt, word)
        with self.say("Walk along. Before x equals one, f dash is positive: rising. Between one and two, negative: falling. After two, positive again. At one and two the derivative is zero: the graph turns, at a local maximum and a local minimum."):
            self.play(x.animate.set_value(1.0), run_time=1.8)
            self.wait(0.4)
            self.play(x.animate.set_value(2.0), run_time=1.8)
            self.wait(0.4)
            self.play(x.animate.set_value(2.9), run_time=1.4)
        tests = VGroup(T("Second-derivative test at f′(c) = 0:", size=26, weight="BOLD"), M(r"f''(c) < 0:\ \text{maximum}\qquad f''(c) > 0:\ \text{minimum}", size=32, color=th.MINT), T("f″(c) = 0: test fails — check whether f′ changes sign", size=24, color=th.MUTED)).arrange(DOWN, buff=0.22).move_to([3.4, -0.6, 0])
        with self.say("To tell which is which: the second derivative. Negative means the curve bends down, so a maximum. Positive bends up: a minimum. Zero: the test fails, and you must check whether f dash changes sign."):
            self.play(FadeIn(tests))
        self.play(FadeOut(VGroup(h, ax, cv, ax2, dcv, l2, tests)), FadeOut(pt), FadeOut(word))
        self.remove(pt, word)
        P.worked(self, "Find the local maximum and minimum values of f(x) = x³ − 6x² + 9x + 15.",
                 [r"f'(x) = 3(x - 1)(x - 3) = 0 \Rightarrow x = 1, 3;\qquad f''(x) = 6x - 12", r"f''(1) = -6 < 0:\ \text{max } f(1) = 19", r"f''(3) = 6 > 0:\ \text{min } f(3) = 15"],
                 ["The standard routine.", "Stationary points at one and three; the second derivative is six x minus twelve.", "At one it is negative: a maximum, nineteen.", "At three positive: a minimum, fifteen."])
        P.worked(self, "From an 18 cm square sheet, squares of side x are cut from the corners to make an open box. Find x for maximum volume.",
                 [r"V = x(18 - 2x)^2,\quad 0 < x < 9", r"V' = (18 - 2x)(18 - 6x) = 12(9 - x)(3 - x) = 0 \Rightarrow x = 3\ (x = 9 \text{ gives } V = 0)", r"V'' = 24x - 144 = -72 < 0 \text{ at } x = 3:\ V_{\max} = 3(12)^2 = 432\ \text{cm}^3"],
                 ["The cold open's box.", "The base is eighteen minus two x, the height x.", "Differentiate and factorise: x is three or nine, and nine leaves no base at all.", "The second derivative is negative at three: a maximum of four hundred and thirty two cubic centimetres."])
        P.worked(self, "Find the absolute maximum and minimum of f(x) = 2x³ − 24x + 107 on [1, 3].",
                 [r"f'(x) = 6(x - 2)(x + 2) = 0 \Rightarrow x = 2\ (x = -2 \notin [1, 3])", r"f(1) = 85,\quad f(2) = 75,\quad f(3) = 89", r"\text{absolute max } 89 \text{ at } x = 3;\ \text{absolute min } 75 \text{ at } x = 2"],
                 ["On a closed interval.", "One stationary point inside: x equals two.", "Now evaluate at it and at both endpoints.", "The biggest is eighty nine, at an endpoint where the derivative is not zero. That is why endpoints must always be checked."])

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        h = P.head(self, "f″ tells you which way the curve bends")
        ax = plot_axes([-2.2, -0.6, 0], [-1, 3.6, 1], [-18, 14, 6], 5.8, 4.8, nums=True)
        fn = lambda x: x ** 4 - 4 * x ** 3 + 10
        cv = P.clipped(ax, fn, -1, 3.6, -18, 14, th.AMBER)
        x = ValueTracker(-0.6)

        def tang():
            a = x.get_value()
            m = 4 * a ** 3 - 12 * a ** 2
            p_ = np.array(ax.c2p(a, fn(a)))
            d = np.array(ax.c2p(1, m)) - np.array(ax.c2p(0, 0))
            d /= np.linalg.norm(d)
            f2 = 12 * a * (a - 2)
            col = th.MINT if f2 > 0.1 else (th.CORAL if f2 < -0.1 else th.AMBER)
            return VGroup(Line(p_ - 1.3 * d, p_ + 1.3 * d, color=col, stroke_width=4), Dot(p_, color=col))

        def rd():
            a = x.get_value()
            f2 = 12 * a * (a - 2)
            return T("concave up: f″ > 0" if f2 > 0.1 else ("concave down: f″ < 0" if f2 < -0.1 else "inflection: f″ changes sign"), size=28, color=th.MINT if f2 > 0.1 else (th.CORAL if f2 < -0.1 else th.AMBER), weight="BOLD").move_to([3.8, 2.2, 0])

        tg, r_ = always_redraw(tang), always_redraw(rd)
        infl = VGroup(Dot(ax.c2p(0, 10), color=th.AMBER, radius=0.11), Dot(ax.c2p(2, -6), color=th.AMBER, radius=0.11), M("(0, 10)", size=26, color=th.AMBER).next_to(ax.c2p(0, 10), UR, buff=0.05), M("(2, -6)", size=26, color=th.AMBER).next_to(ax.c2p(2, -6), DL, buff=0.05))
        f = VGroup(M(r"f(x) = x^4 - 4x^3 + 10", size=30), M(r"f''(x) = 12x(x - 2)", size=32, color=th.SKY), T("inflection points: (0, 10) and (2, −6)", size=24, color=th.AMBER), T("minimum at x = 3: f(3) = −17", size=24, color=th.MINT)).arrange(DOWN, buff=0.25).move_to([3.8, -0.4, 0])
        with self.say("The second derivative tells you how the slope is changing. Where it is positive, the tangent turns anticlockwise and the curve bends upward, like a cup: concave up. Where negative, it bends down, like a cap. Ride a tangent along x to the fourth minus four x cubed plus ten."):
            self.play(FadeIn(h), Create(ax), Create(cv), Write(f[0]))
            self.add(tg, r_)
            self.play(x.animate.set_value(3.4), run_time=5.0, rate_func=rate_functions.linear)
        with self.say("The second derivative, twelve x times x minus two, changes sign at zero and at two. Those are the points of inflection, where the bending switches. Notice x equals zero: the slope is zero there too, but it is not a maximum or minimum. The only extreme is the minimum at x equals three."):
            self.play(Write(f[1]), FadeIn(infl))
            self.play(FadeIn(f[2]), FadeIn(f[3]))
        self.play(FadeOut(VGroup(h, ax, cv, infl, f)), FadeOut(tg), FadeOut(r_))
        self.remove(tg, r_)
        self.quiz("lim (x→0) (sin 3x)/x equals",
                  ["0", "1", "3", "∞"], 2,
                  "Pause and think. Use L'Hospital.",
                  "Three: differentiate top and bottom to get three cos three x over one.")
        self.quiz("If f′(c) = 0 and f″(c) < 0, then at x = c, f has",
                  ["a local minimum", "a local maximum", "a point of inflection", "no conclusion"], 1,
                  "One more.",
                  "A local maximum: the curve is bending downward at a flat point.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "d(sinh x) = cosh x, d(cosh x) = sinh x, d(tanh x) = sech²x; sinh⁻¹x → 1/√(x² + 1).",
            "L'Hospital: for 0/0 or ∞/∞, differentiate top and bottom separately.",
            "Differentials: f(x + Δx) ≈ f(x) + f′(x)Δx; relative error of xⁿ is n times that of x.",
            "Tangent slope m = dy/dx, normal slope −1/m. Rates: link, differentiate in t, substitute.",
            "f′ > 0 rising; f′(c) = 0 and f″(c) < 0 max, > 0 min; f″ changes sign at an inflection.",
        ], "Quick recap. The hyperbolic derivatives. L'Hospital's rule for nought over nought. Differentials for small errors. Tangents, normals and related rates. And the first and second derivatives for rising, falling, maxima, minima and bending.")
        self.outro("That was derivatives. Next, anti-derivatives: running differentiation backwards to find integrals. See you there.")
