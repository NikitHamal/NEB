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
    UNIT = 13
    TITLE = "Anti-derivatives"
    SUBTITLE = "Running differentiation backwards"
    SECTIONS = ["Standard integrals", "Substitution and parts", "Standard forms with a² ± x²", "Partial fractions", "The definite integral", "Limit of a sum", "Area under and between curves"]
    NEXT = "Unit 14 · Differential Equations"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = plot_axes([-2.2, -0.4, 0], [0, 6, 1], [0, 30, 10], 6.4, 4.4, nums=True).shift(DOWN * 0.2)
        lab = VGroup(T("time (s)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35), T("speed (m/s)", size=20, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        v = lambda t: 5 * t
        cv = ax.plot(v, x_range=[0, 6], color=th.SKY, stroke_width=4)
        tt = ValueTracker(0.01)
        area = always_redraw(lambda: ax.get_area(cv, x_range=[0, tt.get_value()], color=th.AMBER, opacity=0.45))
        rd = always_redraw(lambda: VGroup(VGroup(T("t =", size=26), DecimalNumber(tt.get_value(), num_decimal_places=1, font_size=34)).arrange(RIGHT, buff=0.12),
                                          VGroup(T("distance =", size=26, color=th.AMBER), DecimalNumber(2.5 * tt.get_value() ** 2, num_decimal_places=1, font_size=36, color=th.AMBER), T("m", size=24)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 1.4, 0]))
        f = VGroup(M(r"v = 5t", size=36, color=th.SKY), M(r"s = \tfrac52 t^2", size=40, color=th.AMBER), M(r"\frac{ds}{dt} = 5t = v", size=34, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([4.4, -1.4, 0])
        with self.say("A bus pulls away from a stop, its speed rising steadily: five metres per second every second. How far has it gone? The distance is the area under the speed graph."):
            self.play(Create(ax), FadeIn(lab), Create(cv))
            self.add(area, rd)
            self.play(tt.animate.set_value(6), run_time=3.5, rate_func=rate_functions.linear)
        with self.say("The area so far is five halves t squared. And differentiate that: five t, the speed. So the area function is the thing whose derivative is the speed. Finding it means running differentiation backwards: anti-differentiation, or integration."):
            for f_ in f:
                self.play(Write(f_), run_time=0.8)
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, lab, cv, f)), FadeOut(area), FadeOut(rd))
        self.remove(area, rd)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 13: Anti-derivatives."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Seven parts. The standard integrals. Substitution and integration by parts. The standard forms with a squared plus or minus x squared. Partial fractions. The definite integral and its properties. The integral as the limit of a sum. And areas under and between curves.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Every derivative, read backwards")
        ax = plot_axes([-3.0, -0.6, 0], [-2, 2, 1], [-1.5, 6.5, 1], 4.4, 5.0, nums=False)
        fam = VGroup(*[ax.plot(lambda x, c=c: x * x + c, x_range=[-2, 2], color=th.AMBER, stroke_width=3, stroke_opacity=0.35 + 0.15 * (c == 0)) for c in (-1, 0, 1, 2)])
        slopes = VGroup(*[Line(ax.c2p(1 - 0.4, 2 * (-0.4) + 1 + c), ax.c2p(1 + 0.4, 2 * 0.4 + 1 + c), color=th.SKY, stroke_width=4) for c in (-1, 0, 1, 2)])
        lab = M(r"\int 2x\,dx = x^2 + C", size=40, color=th.MINT).move_to([3.4, 2.2, 0])
        nt = para("Every curve x² + C has the same slope 2x at each x: that is why the constant C must always be written.", width=6.0, size=24, color=th.MUTED).move_to([3.4, 1.0, 0])
        with self.say("If the derivative of x squared is two x, then the anti-derivative of two x is x squared. But so is x squared plus one, or plus anything: they are all the same curve shifted up, with identical slopes. So every indefinite integral carries a plus C."):
            self.play(FadeIn(h), Create(ax), LaggedStart(*[Create(c_) for c_ in fam], lag_ratio=0.2))
            self.play(LaggedStart(*[Create(s_) for s_ in slopes], lag_ratio=0.2))
            self.play(Write(lab), FadeIn(nt))
        self.play(FadeOut(VGroup(ax, fam, slopes, lab, nt)))
        rows = [["f(x)", "∫ f(x) dx"], ["xⁿ  (n ≠ −1)", "xⁿ⁺¹/(n + 1)"], ["1/x", "ln|x|"], ["eˣ,  aˣ", "eˣ,  aˣ/ln a"], ["sin x,  cos x", "−cos x,  sin x"], ["sec²x,  cosec²x", "tan x,  −cot x"], ["1/√(1 − x²),  1/(1 + x²)", "sin⁻¹x,  tan⁻¹x"]]
        tb = P.table(rows, [5.0, 5.0], row_h=0.62, size=26, colors=[th.SKY, th.AMBER]).move_to([0, -0.2, 0])
        with self.say("Read your table of derivatives backwards and you have a table of integrals. Raise the power by one and divide by the new power, except for one over x, which gives log x. e to the x is its own integral. Sine integrates to minus cosine, cosine to sine. And the inverse trig derivatives give inverse trig integrals.") as v:
            P.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h, tb)))
        P.worked(self, "Evaluate ∫ (3x² − 4/x + 5√x + eˣ) dx.",
                 [r"\int 3x^2\,dx = x^3,\qquad \int \frac4x\,dx = 4\ln|x|", r"\int 5x^{1/2}\,dx = 5\cdot\frac{x^{3/2}}{3/2} = \frac{10}{3}x^{3/2}", r"= x^3 - 4\ln|x| + \frac{10}{3}x^{3/2} + e^x + C"],
                 ["Term by term.", "Three x squared gives x cubed; four over x gives four log x.", "Write root x as x to the half: raise to three halves and divide by three halves.", "Collect, with one constant. Check by differentiating: you get back the integrand."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Substitution: spot a function and its derivative")
        st = VGroup(M(r"\int x\sqrt{x^2 + 1}\,dx", size=40), M(r"u = x^2 + 1,\quad du = 2x\,dx \Rightarrow x\,dx = \tfrac{du}{2}", size=34, color=th.SKY),
                    M(r"= \int \sqrt u\,\frac{du}{2} = \frac{u^{3/2}}{3}", size=36), M(r"= \tfrac13\left(x^2 + 1\right)^{3/2} + C", size=40, color=th.MINT)).arrange(DOWN, buff=0.35).move_to([0, 0.1, 0])
        hl = VGroup(Underline(st[0], color=th.AMBER).set_width(st[0].width * 0.8))
        with self.say("Substitution is the chain rule run backwards. Look for a function together with its derivative. In x root of x squared plus one, the inside, x squared plus one, has derivative two x, and an x is sitting outside."):
            self.play(FadeIn(h), Write(st[0]))
            self.play(Create(hl))
        with self.say("So let u be x squared plus one. Then x d x is d u over two, and the integral becomes root u over two: easy. Put x back at the end: a third of x squared plus one, to the three halves."):
            self.play(FadeOut(hl))
            for s_ in st[1:]:
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))
        P.worked(self, "Prove ∫ sec x dx = ln|sec x + tan x| + C.",
                 [r"\int \sec x\cdot\frac{\sec x + \tan x}{\sec x + \tan x}\,dx = \int\frac{\sec^2 x + \sec x\tan x}{\sec x + \tan x}\,dx", r"u = \sec x + \tan x:\ du = (\sec x\tan x + \sec^2 x)\,dx", r"= \int\frac{du}{u} = \ln|\sec x + \tan x| + C"],
                 ["A clever substitution.", "Multiply top and bottom by sec x plus tan x.", "Now the top is exactly the derivative of the bottom.", "And derivative over function integrates to log of the function."])
        h = P.head(self, "Integration by parts")
        st = VGroup(M(r"\int u\,dv = uv - \int v\,du", size=48, color=th.MINT), T("from the product rule, read backwards", size=24, color=th.MUTED),
                    T("choose u by ILATE: Inverse trig, Log, Algebraic, Trig, Exponential", size=26, color=th.AMBER)).arrange(DOWN, buff=0.35).move_to([0, 1.2, 0])
        ex = VGroup(M(r"\int x e^x\,dx:\quad u = x,\ dv = e^x dx", size=34), M(r"= xe^x - \int e^x\,dx = xe^x - e^x + C", size=36, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.6, 0])
        with self.say("For a product of two different kinds of function, use integration by parts: the product rule backwards. The integral of u d v is u v minus the integral of v d u. Choose u as the factor that gets simpler when differentiated; the rule ILATE gives the order: inverse trig, log, algebraic, trig, exponential."):
            self.play(FadeIn(h))
            for s_ in st:
                self.play(FadeIn(s_), run_time=0.8)
        with self.say("For x e to the x: x is algebraic, so it is u. Then the new integral is just e to the x, and the answer is x e to the x minus e to the x."):
            self.play(Write(ex[0]))
            self.play(Write(ex[1]))
        self.play(FadeOut(VGroup(h, st, ex)))
        P.worked(self, "Evaluate I = ∫ eˣ sin x dx.",
                 [r"I = e^x\sin x - \int e^x\cos x\,dx", r"\int e^x\cos x\,dx = e^x\cos x + \int e^x\sin x\,dx = e^x\cos x + I", r"I = e^x\sin x - e^x\cos x - I \Rightarrow I = \frac{e^x}{2}(\sin x - \cos x) + C"],
                 ["The cyclic case: neither factor simplifies.", "Parts once, with u equal to sin x.", "Parts again on the new integral. The original integral I reappears.", "So I appears on both sides: move it across and divide by two."])

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        rows = [["integral", "result"], ["∫ dx/(x² + a²)", "(1/a) tan⁻¹(x/a)"], ["∫ dx/(x² − a²)", "(1/2a) ln|(x − a)/(x + a)|"], ["∫ dx/√(a² − x²)", "sin⁻¹(x/a)"], ["∫ dx/√(x² ± a²)", "ln|x + √(x² ± a²)|"], ["∫ √(a² − x²) dx", "(x/2)√(a² − x²) + (a²/2) sin⁻¹(x/a)"]]
        tb = P.table(rows, [4.0, 7.0], row_h=0.68, size=26, colors=[th.SKY, th.AMBER]).move_to([0, 0.6, 0])
        nt = para("Make the coefficient of x² equal to 1 first, then read off a. Complete the square for ax² + bx + c.", width=11, size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("A family of standard forms is built around a squared plus or minus x squared. One over x squared plus a squared gives inverse tan. One over root of a squared minus x squared gives inverse sine. And others give logarithms. To use them, first make the coefficient of x squared equal to one, and complete the square if there is an x term.") as v:
            P.reveal_table(self, tb, v.dur * 0.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        P.worked(self, "Evaluate (a) ∫ dx/(4x² + 9), (b) ∫ dx/(x² − 16), (c) ∫ dx/√(9 − 4x²).",
                 [r"\text{(a) } \frac14\int\frac{dx}{x^2 + (3/2)^2} = \frac14\cdot\frac23\tan^{-1}\frac{2x}{3} = \frac16\tan^{-1}\frac{2x}{3} + C", r"\text{(b) } a = 4:\ \frac18\ln\left|\frac{x - 4}{x + 4}\right| + C",
                  r"\text{(c) } \frac12\int\frac{dx}{\sqrt{(3/2)^2 - x^2}} = \frac12\sin^{-1}\frac{2x}{3} + C"],
                 ["Matching the forms.", "Take the four out: a is three halves, giving a sixth of inverse tan two x over three.", "Here a is four directly: an eighth of log of x minus four over x plus four.", "Take two out of the root: a half inverse sine two x over three."])
        h = P.head(self, "Where ∫√(a² − x²) dx comes from")
        R = 2.2
        O = np.array([-3.6, -1.2, 0])
        arc = Arc(radius=R, start_angle=0, angle=PI / 2, arc_center=O, color=th.SKY, stroke_width=4)
        ax_ = VGroup(Line(O, O + RIGHT * (R + 0.3), color=th.MUTED), Line(O, O + UP * (R + 0.3), color=th.MUTED))
        xv = 1.4
        yv = np.sqrt(R * R - xv * xv)
        P_ = O + np.array([xv, yv, 0])
        tri = Polygon(O, O + RIGHT * xv, P_, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.45)
        sec = Sector(radius=R, start_angle=np.arctan2(yv, xv), angle=PI / 2 - np.arctan2(yv, xv), arc_center=O, stroke_width=0, fill_color=th.MINT, fill_opacity=0.45)
        sl = VGroup(Line(O + RIGHT * xv, P_, color=th.INK, stroke_width=3), Line(O, P_, color=th.INK, stroke_width=3), M("x", size=28).next_to(O + RIGHT * xv / 2, DOWN, buff=0.1), M("a", size=28).move_to(O + (P_ - O) * 0.5 + np.array([-0.2, 0.25, 0])))
        f = VGroup(M(r"\int_0^x \sqrt{a^2 - t^2}\,dt", size=36), M(r"= \underbrace{\tfrac12 x\sqrt{a^2 - x^2}}_{\text{triangle}} + \underbrace{\tfrac{a^2}{2}\sin^{-1}\tfrac xa}_{\text{sector}}", size=34)).arrange(DOWN, buff=0.4).move_to([2.6, 0.2, 0])
        f[1][0][0:13].set_color(th.AMBER)
        nt = T("(proof: x = a sin θ, then cos²θ = (1 + cos 2θ)/2)", size=22, color=th.MUTED).move_to([2.6, -2.2, 0])
        with self.say("The last form has a lovely picture. The area under the quarter circle from nought to x splits into a triangle and a sector. The triangle has area half x times root of a squared minus x squared. The sector's angle is inverse sine of x over a, so its area is a squared over two times that angle. That is exactly the formula. Algebraically, substitute x equals a sin theta."):
            self.play(FadeIn(h), Create(ax_), Create(arc))
            self.play(FadeIn(tri), FadeIn(sec), Create(sl))
            self.play(Write(f[0]), Write(f[1]))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, arc, ax_, tri, sec, sl, f, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Partial fractions: split, then integrate")
        st = VGroup(M(r"\frac{1}{(x - 1)(x + 2)} = \frac{A}{x - 1} + \frac{B}{x + 2}", size=48), M(r"1 = A(x + 2) + B(x - 1)", size=44),
                    M(r"x = 1:\ A = \frac13;\qquad x = -2:\ B = -\frac13", size=42, color=th.SKY), M(r"\int\frac{dx}{(x - 1)(x + 2)} = \frac13\ln\left|\frac{x - 1}{x + 2}\right| + C", size=46, color=th.MINT)).arrange(DOWN, buff=0.38).move_to([0, 0.1, 0])
        says = ["A fraction with a factorised denominator can be split into simpler fractions, each easy to integrate. One over x minus one times x plus two is A over x minus one, plus B over x plus two.", "Multiply through by the denominator.",
                "Choose clever values of x. Put x equal to one and the B term vanishes: A is a third. Put x equal to minus two: B is minus a third.", "Each piece integrates to a log, and the logs combine."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))
        rows = [["factor in the denominator", "partial fractions"], ["(x − a)", "A/(x − a)"], ["(x − a)²", "A/(x − a) + B/(x − a)²"], ["x² + bx + c (no real roots)", "(Bx + C)/(x² + bx + c)"]]
        tb = P.table(rows, [5.4, 5.8], row_h=0.72, size=26, colors=[th.INK, th.AMBER]).move_to([0, 0.6, 0])
        nt = para("If the top's degree is not less than the bottom's, divide first.", width=11, size=24, color=th.CORAL).move_to([0, -1.9, 0])
        with self.say("The form depends on the factors. A linear factor gets a constant on top. A repeated factor gets one fraction for each power. An irreducible quadratic gets a linear numerator. And if the top is not of lower degree than the bottom, divide first.") as v:
            P.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        P.worked(self, "Evaluate ∫ dx / ((x − 1)(x² + 1)).",
                 [r"\frac{1}{(x - 1)(x^2 + 1)} = \frac{A}{x - 1} + \frac{Bx + D}{x^2 + 1}", r"1 = A(x^2 + 1) + (Bx + D)(x - 1):\ A = \tfrac12,\ B = -\tfrac12,\ D = -\tfrac12", r"= \tfrac12\ln|x - 1| - \tfrac14\ln(x^2 + 1) - \tfrac12\tan^{-1}x + C"],
                 ["An irreducible quadratic.", "x squared plus one needs a linear numerator.", "x equal to one gives A; compare the x squared terms and the constants for B and D.", "The last fraction splits into a log and an inverse tan."])

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "The definite integral: F(b) − F(a), a signed area")
        ax = plot_axes([-2.2, -0.6, 0], [0, 7, 1], [-1.3, 1.3, 1], 6.4, 3.6, nums=False)
        sn = ax.plot(np.sin, x_range=[0, 7], color=th.SKY, stroke_width=4)
        b = ValueTracker(PI)
        pos = always_redraw(lambda: ax.get_area(sn, x_range=[0, min(b.get_value(), PI)], color=th.MINT, opacity=0.5))
        neg = always_redraw(lambda: ax.get_area(sn, x_range=[PI, max(b.get_value(), PI + 0.001)], color=th.CORAL, opacity=0.5))
        rd = always_redraw(lambda: VGroup(M(r"\int_0^b \sin x\,dx =", size=42), DecimalNumber(1 - np.cos(b.get_value()), num_decimal_places=2, font_size=46, color=th.AMBER)).arrange(RIGHT, buff=0.15).move_to([3.6, 2.0, 0]))
        f = VGroup(M(r"= [-\cos x]_0^b = 1 - \cos b", size=38), T("area below the axis counts as negative", size=24, color=th.CORAL)).arrange(DOWN, buff=0.25).move_to([3.6, 1.0, 0])
        with self.say("The definite integral from a to b is F of b minus F of a, where F is any anti-derivative; the constant cancels. It measures signed area. Integrate sine from nought to pi: the green hump has area exactly two."):
            self.play(FadeIn(h), Create(ax), Create(sn))
            self.add(pos, neg, rd)
            self.play(Write(f[0]))
        with self.say("Carry on past pi, and the curve dips below the axis. That area counts as negative, so the integral falls: to one at three pi over two, and to zero at two pi, where the two humps cancel exactly."):
            self.play(b.animate.set_value(1.5 * PI), run_time=1.8)
            self.play(FadeIn(f[1]))
            self.play(b.animate.set_value(2 * PI), run_time=1.5)
        self.play(FadeOut(VGroup(h, ax, sn, f)), FadeOut(pos), FadeOut(neg), FadeOut(rd))
        self.remove(pos, neg, rd)
        props = VGroup(M(r"\int_a^b f = -\int_b^a f,\qquad \int_a^b f = \int_a^c f + \int_c^b f", size=44), M(r"\int_0^a f(x)\,dx = \int_0^a f(a - x)\,dx\quad (\text{the reflection trick})", size=44, color=th.AMBER),
                       M(r"\int_{-a}^a f = 2\int_0^a f\ (f \text{ even}),\qquad \int_{-a}^a f = 0\ (f \text{ odd})", size=44)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.2, 0])
        hd = T("Properties of the definite integral", size=30, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("Three properties do most of the work. Swapping the limits changes the sign, and you can split at any point. Replacing x by a minus x does not change the integral from nought to a: the reflection trick. And over a symmetric interval, an odd function integrates to zero, an even one to twice the half.") as v:
            self.play(FadeIn(hd))
            P.reveal_list(self, props, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, props)))
        P.worked(self, "Evaluate I = ∫₀^(π/2) √(sin x) / (√(sin x) + √(cos x)) dx.",
                 [r"x \to \tfrac\pi2 - x:\quad I = \int_0^{\pi/2}\frac{\sqrt{\cos x}}{\sqrt{\cos x} + \sqrt{\sin x}}\,dx", r"2I = \int_0^{\pi/2} 1\,dx = \frac\pi2", r"I = \frac\pi4"],
                 ["No anti-derivative exists here. Use the reflection trick.", "Replace x by pi over two minus x: sine and cosine swap.", "Add the two forms: the fractions add to one, and the integral of one is pi over two.", "So I is pi over four."])
        P.worked(self, "Evaluate ∫₀^π x sin x dx.",
                 [r"I = \int_0^\pi (\pi - x)\sin x\,dx = \pi\int_0^\pi \sin x\,dx - I", r"2I = \pi \cdot 2 \Rightarrow I = \pi"],
                 ["The trick again.", "Replace x by pi minus x: the integral equals pi times the integral of sin x, minus I.", "The integral of sin x from nought to pi is two, so I is pi. Integration by parts agrees."])

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "∫₀¹ x² dx as the limit of a sum")
        ax = plot_axes([-2.4, -0.6, 0], [0, 1, 0.25], [0, 1, 0.25], 5.4, 4.6, nums=True)
        cv = ax.plot(lambda x: x * x, x_range=[0, 1], color=th.AMBER, stroke_width=4)
        n = ValueTracker(4)

        def rects():
            k = int(n.get_value())
            w = 1 / k
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, ((r + 1) * w) ** 2)[1] - ax.c2p(0, 0)[1], 0.001), stroke_color=th.SKY, stroke_width=1.5, fill_color=th.SKY, fill_opacity=0.35).move_to(ax.c2p(r * w, 0), aligned_edge=DL) for r in range(k)])

        def rd():
            k = int(n.get_value())
            S = (k + 1) * (2 * k + 1) / (6 * k * k)
            return VGroup(VGroup(T("n =", size=28), Integer(k, font_size=36, color=th.SKY)).arrange(RIGHT, buff=0.15), VGroup(M(r"S_n =", size=34), DecimalNumber(S, num_decimal_places=4, font_size=38, color=th.SKY)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 2.0, 0])

        rc, r_ = always_redraw(rects), always_redraw(rd)
        st = VGroup(M(r"S_n = \frac1n\sum_{r=1}^n \frac{r^2}{n^2} = \frac{n(n+1)(2n+1)}{6n^3}", size=32), M(r"= \frac16\left(2 + \frac3n + \frac{1}{n^2}\right) \to \frac13", size=34, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([3.4, -0.6, 0])
        with self.say("Why is an integral an area? Fill the region under x squared from nought to one with n thin rectangles. Their total area overshoots a little. Now take more and thinner rectangles."):
            self.play(FadeIn(h), Create(ax), Create(cv))
            self.add(rc, r_)
            self.wait(0.8)
            for k in (10, 20, 40):
                self.play(n.animate.set_value(k), run_time=1.0)
        with self.say("The sum uses the sum of squares from unit four: n, n plus one, two n plus one, over six n cubed. As n grows, the extra terms vanish and the sum tends to one third: exactly the integral, x cubed over three from nought to one."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        self.play(FadeOut(VGroup(h, ax, cv, st)), FadeOut(rc), FadeOut(r_))
        self.remove(rc, r_)

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        h = P.head(self, "Area between y = 2x and y = x²")
        ax = plot_axes([-2.4, -0.6, 0], [0, 2.4, 0.5], [0, 4.5, 1], 5.4, 4.8, nums=True)
        top = ax.plot(lambda x: 2 * x, x_range=[0, 2.25], color=th.SKY, stroke_width=4)
        bot = ax.plot(lambda x: x * x, x_range=[0, 2.1], color=th.AMBER, stroke_width=4)
        reg = ax.get_area(top, x_range=[0, 2], bounded_graph=bot, color=th.MINT, opacity=0.5)
        strip = Rectangle(width=0.12, height=ax.c2p(0, 2 * 1.2)[1] - ax.c2p(0, 1.44)[1], stroke_color=th.INK, stroke_width=2, fill_color=th.INK, fill_opacity=0.5).move_to(ax.c2p(1.2, (2.4 + 1.44) / 2))
        st = VGroup(T("1. intersections: x² = 2x → x = 0, 2", size=26), T("2. top curve: the line (test x = 1)", size=26), M(r"3.\ A = \int_0^2 (2x - x^2)\,dx = \left[x^2 - \frac{x^3}{3}\right]_0^2 = \frac43", size=34, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.4, 0])
        with self.say("To find the area between two curves, find where they meet: x squared equals two x at nought and two. Decide which is on top: at x equals one the line is higher."):
            self.play(FadeIn(h), Create(ax), Create(top), Create(bot))
            self.play(FadeIn(st[0]), FadeIn(st[1]))
        with self.say("Each thin strip has height top minus bottom. Add the strips: integrate two x minus x squared from nought to two. Four thirds square units."):
            self.play(FadeIn(strip))
            self.play(strip.animate.move_to(ax.c2p(0.5, (1 + 0.25) / 2)).stretch_to_fit_height(ax.c2p(0, 1)[1] - ax.c2p(0, 0.25)[1]), run_time=1.2)
            self.play(FadeIn(reg), FadeOut(strip))
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(h, ax, top, bot, reg, st)))
        P.worked(self, "Find the area of the circle x² + y² = a², and of the ellipse x²/a² + y²/b² = 1.",
                 [r"A = 4\int_0^a \sqrt{a^2 - x^2}\,dx = 4\left[\frac x2\sqrt{a^2 - x^2} + \frac{a^2}{2}\sin^{-1}\frac xa\right]_0^a", r"= 4\cdot\frac{a^2}{2}\cdot\frac\pi2 = \pi a^2", r"\text{ellipse: } y = \frac ba\sqrt{a^2 - x^2} \Rightarrow A = \frac ba\cdot\pi a^2 = \pi ab"],
                 ["The circle, proved.", "Four times the quarter circle, using the standard form.", "At x equals a: inverse sine of one is pi over two. Pi a squared.", "The ellipse is the circle squashed by b over a: pi a b."])
        P.worked(self, "Find the area under y = x² from x = 0 to 3, and under y = 1/x from 1 to e.",
                 [r"\int_0^3 x^2\,dx = \left[\frac{x^3}{3}\right]_0^3 = 9", r"\int_1^e \frac{dx}{x} = [\ln x]_1^e = 1"],
                 ["Two quick areas.", "Under x squared: nine square units.", "Under one over x from one to e: exactly one. That is what makes e the natural base."])
        c = self.callout("careful", "Area is always positive: if part of the region lies below the x-axis, integrate that part separately and take its absolute value. Always find the intersections first.", width=11, size=26)
        with self.say("A warning. An integral counts area below the axis as negative, but an area cannot be negative. Split the region where the curve crosses the axis and add the sizes."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("∫ from 0 to 2π of sin x dx equals",
                  ["2", "4", "0", "−2"], 2,
                  "Pause and think about the two humps.",
                  "Zero: the hump above and the hump below cancel. The total area, though, is four.")
        self.quiz("For ∫ x eˣ dx by parts, u should be",
                  ["eˣ", "x", "x eˣ", "either"], 1,
                  "One more. Use ILATE.",
                  "x, the algebraic factor: it becomes one when differentiated, and the integral that is left is easy.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "∫ f dx = F + C where F′ = f; read the derivative table backwards.",
            "Substitution: spot g(x) and g′(x). Parts: ∫u dv = uv − ∫v du, choose u by ILATE.",
            "Standard forms in x² ± a² and a² − x²; partial fractions by factor type.",
            "Definite integral = F(b) − F(a), a signed area; reflection trick: replace x by a − x on [0, a].",
            "Area between curves: intersections, top minus bottom, integrate.",
        ], "Quick recap. Integration runs differentiation backwards, with a plus C. Substitution undoes the chain rule, parts undoes the product rule. The standard forms and partial fractions handle the rest. The definite integral is a signed area, and the area between curves is the integral of top minus bottom.")
        self.outro("That was anti-derivatives. Next, differential equations: equations that involve derivatives, and how to solve them. See you there.")
