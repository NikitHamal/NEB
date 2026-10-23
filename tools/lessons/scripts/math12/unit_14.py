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


def slope_field(ax, f, xs, ys, L=0.32, color=th.FAINT):
    g = VGroup()
    for x in xs:
        for y in ys:
            try:
                m = f(x, y)
            except ZeroDivisionError:
                continue
            if not np.isfinite(m):
                d = np.array([0, 1.0, 0])
            else:
                d = np.array(ax.c2p(1, m)) - np.array(ax.c2p(0, 0))
                d /= np.linalg.norm(d)
            p_ = np.array(ax.c2p(x, y))
            g.add(Line(p_ - d * L / 2, p_ + d * L / 2, color=color, stroke_width=2.5))
    return g


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 14
    TITLE = "Differential Equations"
    SUBTITLE = "Equations about rates of change"
    SECTIONS = ["Order, degree and forming equations", "Separable variables", "Homogeneous equations", "Linear equations", "Exact equations", "Growth, decay and cooling"]
    NEXT = "Unit 15 · Computational Methods"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = plot_axes([-2.2, -0.4, 0], [0, 40, 10], [0, 85, 20], 6.4, 4.6)
        lab = VGroup(T("minutes", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35), T("°C", size=20, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        k = np.log(2) / 10
        room = DashedLine(ax.c2p(0, 20), ax.c2p(40, 20), color=th.SKY)
        rl = T("room 20 °C", size=20, color=th.SKY).next_to(ax.c2p(40, 20), UP, buff=0.08).shift(LEFT * 0.6)
        cv = ax.plot(lambda t: 20 + 60 * np.exp(-k * t), x_range=[0, 40], color=th.CORAL, stroke_width=5)
        tt = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), 20 + 60 * np.exp(-k * tt.get_value())), color=th.CORAL, radius=0.1))
        rd = always_redraw(lambda: VGroup(T("tea:", size=26), DecimalNumber(20 + 60 * np.exp(-k * tt.get_value()), num_decimal_places=1, font_size=36, color=th.CORAL), T("°C", size=26)).arrange(RIGHT, buff=0.12).move_to([4.4, 2.0, 0]))
        law = VGroup(M(r"\frac{d\theta}{dt} = -k(\theta - 20)", size=40, color=th.AMBER), T("cools faster when it is hotter", size=24, color=th.MUTED)).arrange(DOWN, buff=0.25).move_to([4.4, 0.4, 0])
        with self.say("A glass of tea at eighty degrees, in a room at twenty. It cools quickly at first, then more and more slowly, creeping towards room temperature but never quite reaching it."):
            self.play(Create(ax), FadeIn(lab), Create(room), FadeIn(rl))
            self.add(dot, rd)
            self.play(Create(cv), tt.animate.set_value(40), run_time=4.0, rate_func=rate_functions.linear)
        with self.say("Newton's law says why: the rate of cooling is proportional to how much hotter the tea is than the room. That is an equation about a rate of change, a differential equation. Solving it gives the whole curve. This unit shows you how."):
            self.play(Write(law[0]), FadeIn(law[1]))
            nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, lab, room, rl, cv, law)), FadeOut(dot), FadeOut(rd))
        self.remove(dot, rd)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 14: Differential Equations."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Order, degree and forming a differential equation. Separable equations. Homogeneous equations. Linear equations with an integrating factor. Exact equations. And applications: growth, decay and cooling.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Order and degree")
        ex = M(r"\Bigg(", r"\frac{d^3y}{dx^3}", r"\Bigg)", r"^2", r" + \frac{dy}{dx} = \sin x", size=46).move_to([0, 1.6, 0])
        o = SurroundingRectangle(ex[1], color=th.SKY, buff=0.06)
        d = SurroundingRectangle(ex[3], color=th.AMBER, buff=0.05)
        lab = VGroup(T("order = the highest derivative = 3", size=28, color=th.SKY), T("degree = its power (after clearing roots and fractions) = 2", size=28, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        nt = para("Clear radicals first: y″ = √(1 + y′²) becomes y″² = 1 + y′², order 2, degree 2.", width=11, size=24, color=th.MUTED).move_to([0, -2.2, 0])
        with self.say("A differential equation contains derivatives. Its order is the highest derivative that appears: here, the third. Its degree is the power of that highest derivative, once roots and fractions in the derivatives are cleared: here, two."):
            self.play(FadeIn(h), Write(ex))
            self.play(Create(o), FadeIn(lab[0]))
            self.play(Create(d), FadeIn(lab[1]))
        with self.say("Watch for square roots. The second derivative equals the root of one plus the first derivative squared: square both sides, and it has order two, degree two."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, ex, o, d, lab, nt)))
        h = P.head(self, "A family of curves → one differential equation")
        ax = plot_axes([-3.0, -0.6, 0], [-3, 3, 1], [-3, 3, 1], 4.8, 4.8, nums=False)
        circles = VGroup(*[Circle(radius=r * ax.x_axis.unit_size, stroke_color=th.AMBER, stroke_width=3, stroke_opacity=0.8).move_to(ax.c2p(0, 0)) for r in (0.8, 1.6, 2.4)])
        st = VGroup(M(r"x^2 + y^2 = a^2", size=38), M(r"2x + 2y\frac{dy}{dx} = 0", size=36), M(r"\frac{dy}{dx} = -\frac xy", size=44, color=th.MINT), T("one arbitrary constant → differentiate once", size=24, color=th.MUTED)).arrange(DOWN, buff=0.35).move_to([3.4, 0.0, 0])
        with self.say("Going the other way, every family of curves has a differential equation. The circles x squared plus y squared equals a squared, for every radius a. Differentiate once, because there is one constant, and a disappears: d y by d x equals minus x over y. One equation describes every circle in the family."):
            self.play(FadeIn(h), Create(ax), LaggedStart(*[Create(c_) for c_ in circles], lag_ratio=0.2))
            for s_ in st:
                self.play(Write(s_), run_time=0.8)
        self.play(FadeOut(VGroup(h, ax, circles, st)))
        P.worked(self, "Form the differential equation of (a) y = mx, (b) y = Ae²ˣ.",
                 [r"\text{(a) } \frac{dy}{dx} = m = \frac yx \Rightarrow \frac{dy}{dx} = \frac yx", r"\text{(b) } \frac{dy}{dx} = 2Ae^{2x} = 2y \Rightarrow \frac{dy}{dx} - 2y = 0"],
                 ["Eliminate the constant.", "Lines through the origin: the slope m is y over x.", "And for A e to the two x, the derivative is twice y itself."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Slope field of dy/dx = −x/y")
        ax = plot_axes([-2.6, -0.6, 0], [-3, 3, 1], [-3, 3, 1], 5.2, 5.2, nums=False)
        field = slope_field(ax, lambda x, y: -x / y, np.arange(-2.75, 2.8, 0.5), np.arange(-2.75, 2.8, 0.5), L=0.3)
        tr = ValueTracker(0)
        path = always_redraw(lambda: Arc(radius=2.0 * ax.x_axis.unit_size, start_angle=PI / 2, angle=max(tr.get_value(), 1e-3), arc_center=ax.c2p(0, 0), color=th.AMBER, stroke_width=5))
        txt = VGroup(para("at every point, a short line shows the slope the equation demands", width=5.4, size=24, color=th.MUTED), para("a solution curve follows the slopes everywhere", width=5.4, size=24, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.8, 0])
        with self.say("What does a solution look like? At every point, the equation tells you a slope. Draw a little line there: this is the slope field. A solution is a curve that follows those little lines everywhere. Start at the top and follow them: you go round a circle. Every starting point gives a different circle."):
            self.play(FadeIn(h), Create(ax), LaggedStart(*[Create(l_) for l_ in field], lag_ratio=0.004, run_time=2.0))
            self.play(FadeIn(txt[0]))
            self.add(path)
            self.play(tr.animate.set_value(TAU), FadeIn(txt[1]), run_time=3.0, rate_func=rate_functions.linear)
        sep = VGroup(M(r"y\,dy = -x\,dx", size=36), M(r"\int y\,dy = -\int x\,dx", size=36), M(r"x^2 + y^2 = C", size=44, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([3.4, -1.3, 0])
        with self.say("Algebraically: put all the y's with d y on one side and all the x's with d x on the other. That separates the variables. Integrate each side, and the circles appear: x squared plus y squared equals C."):
            for s_ in sep:
                self.play(Write(s_), run_time=0.8)
        self.play(FadeOut(VGroup(h, ax, field, txt, sep)), FadeOut(path))
        self.remove(path)
        P.worked(self, "Solve (1 + x²) dy/dx = 1 + y².",
                 [r"\frac{dy}{1 + y^2} = \frac{dx}{1 + x^2}", r"\tan^{-1}y = \tan^{-1}x + C"],
                 ["Separate.", "y with d y on the left, x with d x on the right.", "Both are standard forms: inverse tan of y equals inverse tan of x plus C."])
        P.worked(self, "Solve sec²x tan y dx + sec²y tan x dy = 0.",
                 [r"\frac{\sec^2 x}{\tan x}\,dx + \frac{\sec^2 y}{\tan y}\,dy = 0", r"\ln|\tan x| + \ln|\tan y| = \ln|c| \Rightarrow \tan x\tan y = c"],
                 ["Divide by tan x tan y to separate.", "Each term is a derivative over its function.", "So the logs add. Writing the constant as log c lets the answer collapse to tan x tan y equals c."])
        P.worked(self, "Solve x dy/dx = y(x − 1).",
                 [r"\frac{dy}{y} = \left(1 - \frac1x\right)dx", r"\ln|y| = x - \ln|x| + \ln|C| \Rightarrow xy = Ce^x"],
                 ["One more.", "Separate: d y over y equals one minus one over x, d x.", "Integrate and collect the logs: x y equals C e to the x."])

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "Homogeneous: dy/dx = F(y/x) → put y = vx")
        st = VGroup(M(r"\frac{dy}{dx} = \frac{x^2 + y^2}{2xy}\quad (\text{both degree } 2)", size=36), M(r"y = vx,\quad \frac{dy}{dx} = v + x\frac{dv}{dx}", size=36, color=th.SKY),
                    M(r"v + x\frac{dv}{dx} = \frac{1 + v^2}{2v} \Rightarrow x\frac{dv}{dx} = \frac{1 - v^2}{2v}", size=34), M(r"\frac{2v\,dv}{1 - v^2} = \frac{dx}{x} \Rightarrow x(1 - v^2) = C", size=34),
                    M(r"x^2 - y^2 = Cx", size=44, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([0, -0.2, 0])
        says = ["When every term on the right has the same total degree, the right side depends only on y over x. That is a homogeneous equation.", "The trick: put y equal to v x. Then d y by d x is v plus x d v by d x, by the product rule.",
                "Substitute, and every x cancels from the right. Move v across.", "Now the variables separate: v with d v, x with d x. Integrate.", "Finally put v back as y over x: x squared minus y squared equals C x."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))
        P.worked(self, "Solve x dy/dx = y + x tan(y/x).",
                 [r"\frac{dy}{dx} = \frac yx + \tan\frac yx;\quad y = vx:\ v + x\frac{dv}{dx} = v + \tan v", r"\cot v\,dv = \frac{dx}{x} \Rightarrow \ln|\sin v| = \ln|Cx|", r"\sin\frac yx = Cx"],
                 ["Another homogeneous one.", "Divide by x; it is a function of y over x. Put y equal to v x: the v's cancel.", "Separate, and cot v integrates to log sin v.", "So sin of y over x equals C x."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Linear: dy/dx + Py = Q, integrating factor e^(∫P dx)")
        st = VGroup(M(r"\frac{dy}{dx} + Py = Q", size=44, color=th.SKY), M(r"I = e^{\int P\,dx}", size=44, color=th.AMBER), M(r"\frac{d}{dx}(Iy) = IQ \Rightarrow Iy = \int IQ\,dx + C", size=40, color=th.MINT),
                    para("Multiplying by I turns the left side into the derivative of the product I·y: the product rule run backwards.", width=10, size=24, color=th.MUTED)).arrange(DOWN, buff=0.4).move_to([0, -0.1, 0])
        says = ["A linear equation has y and its derivative to the first power only. Write it as d y by d x plus P y equals Q, where P and Q are functions of x.", "Multiply through by the integrating factor, e to the integral of P.",
                "Then the left side is exactly the derivative of I times y. Integrate both sides, and divide by I.", "Why does it work? The derivative of I is P times I, so the product rule gives back I times the left side."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(FadeIn(s_, shift=UP * 0.15), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))
        P.worked(self, "Solve x dy/dx + 2y = x³.",
                 [r"\frac{dy}{dx} + \frac2x y = x^2:\quad P = \frac2x,\ Q = x^2", r"I = e^{2\ln x} = x^2", r"\frac{d}{dx}(x^2y) = x^4 \Rightarrow x^2y = \frac{x^5}{5} + C", r"y = \frac{x^3}{5} + \frac{C}{x^2}"],
                 ["The three steps.", "Divide by x to get the standard form.", "The integrating factor is e to the two log x: x squared.", "Now the left side is the derivative of x squared y. Integrate: x to the fifth over five plus C.", "Divide by x squared."])
        P.worked(self, "Solve (1 + x²) dy/dx + 2xy = 4x².",
                 [r"I = e^{\int \frac{2x}{1 + x^2}dx} = 1 + x^2", r"\frac{d}{dx}\left[(1 + x^2)y\right] = 4x^2 \Rightarrow (1 + x^2)y = \frac{4x^3}{3} + C"],
                 ["Spot the shortcut.", "The integrating factor is one plus x squared: the very thing we would divide by.", "So the left side was already the derivative of one plus x squared, times y. Integrate directly."])
        c = self.callout("careful", "Divide to make the coefficient of dy/dx exactly 1 BEFORE reading off P. And never forget the + C before you divide by I.", width=11, size=26)
        with self.say("Two slips to avoid. Make the coefficient of d y by d x one before you read off P. And add the constant before dividing by I, or you lose part of the answer."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Exact: M dx + N dy = 0 with ∂M/∂y = ∂N/∂x")
        st = VGroup(M(r"(3x^2 + 2y)\,dx + (2x + 3y^2)\,dy = 0", size=38), M(r"\frac{\partial M}{\partial y} = 2 = \frac{\partial N}{\partial x}\ \checkmark\ \text{exact}", size=36, color=th.SKY),
                    M(r"u = \int (3x^2 + 2y)\,dx = x^3 + 2xy + g(y)", size=36), M(r"\frac{\partial u}{\partial y} = 2x + g'(y) = 2x + 3y^2 \Rightarrow g = y^3", size=34), M(r"x^3 + 2xy + y^3 = C", size=44, color=th.MINT)).arrange(DOWN, buff=0.32).move_to([0, -0.2, 0])
        says = ["Some equations are the total differential of a single function u: d u equals M d x plus N d y. Then the solution is just u equals C.", "The test: the partial derivative of M with respect to y must equal the partial of N with respect to x. Here both are two.",
                "To find u, integrate M with respect to x, holding y fixed, and add an unknown function of y.", "Differentiate with respect to y and match it to N: g dash is three y squared, so g is y cubed.", "The solution: x cubed plus two x y plus y cubed equals C."]
        self.play(FadeIn(h))
        for s_, sy in zip(st, says):
            with self.say(sy):
                self.play(Write(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, st)))
        P.worked(self, "Solve (2xy + y²) dx + (x² + 2xy) dy = 0.",
                 [r"\frac{\partial M}{\partial y} = 2x + 2y = \frac{\partial N}{\partial x}", r"u = x^2y + xy^2 + g(y);\quad \frac{\partial u}{\partial y} = x^2 + 2xy + g' \Rightarrow g' = 0", r"xy(x + y) = C"],
                 ["Another exact one.", "Test: both partials are two x plus two y.", "Integrate M in x; matching N leaves nothing for g.", "So x y times x plus y equals C."])

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "dP/dt = kP: exponential growth and decay")
        ax = plot_axes([-2.4, -0.6, 0], [0, 30, 10], [0, 120, 20], 6.0, 4.4)
        lab = VGroup(T("years after 2068 BS", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35), T("thousands", size=20, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT))
        k = np.log(1.25) / 10
        cv = ax.plot(lambda t: 40 * np.exp(k * t), x_range=[0, 30], color=th.MINT, stroke_width=4)
        pts = VGroup(*[Dot(ax.c2p(t, 40 * 1.25 ** (t / 10)), color=th.AMBER, radius=0.1) for t in (0, 10, 20)])
        pl = VGroup(*[T(s_, size=22, color=th.AMBER).next_to(p_, UP, buff=0.15) for s_, p_ in zip(["40 000", "50 000", "62 500"], pts)])
        st = VGroup(M(r"\frac{dP}{dt} = kP \Rightarrow \frac{dP}{P} = k\,dt \Rightarrow P = P_0e^{kt}", size=32), M(r"e^{10k} = \frac{50000}{40000} = \frac54", size=34),
                    M(r"P(20) = 40000\left(\tfrac54\right)^2 = 62\,500", size=36, color=th.MINT), T("equal time steps multiply by the same factor", size=22, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.say("A population that grows at a rate proportional to its size obeys d P by d t equals k P. Separate and integrate: P equals P nought e to the k t. A municipality had forty thousand people in twenty sixty eight and fifty thousand ten years later."):
            self.play(FadeIn(h), Create(ax), FadeIn(lab), Create(cv))
            self.play(Write(st[0]), FadeIn(pts[:2]), FadeIn(pl[:2]))
        with self.say("So ten years multiplies the population by five quarters. Another ten years multiplies by five quarters again: sixty two thousand five hundred. No need to work out k at all."):
            self.play(Write(st[1]))
            self.play(Write(st[2]), FadeIn(pts[2]), FadeIn(pl[2]), FadeIn(st[3]))
        self.play(FadeOut(VGroup(h, ax, lab, cv, pts, pl, st)))
        P.worked(self, "A bacterial culture doubles in 3 hours. By what factor does it grow in 12 hours?",
                 [r"N = N_0e^{kt},\quad e^{3k} = 2", r"\frac{N}{N_0} = e^{12k} = \left(e^{3k}\right)^4 = 2^4 = 16"],
                 ["Doubling time.", "Doubling in three hours means e to the three k is two.", "Twelve hours is four doublings: sixteen times."])
        P.worked(self, "Tea at 80 °C cools in a 20 °C room to 50 °C in 10 minutes. Find its temperature after 20 minutes, and when it reaches 30 °C.",
                 [r"\theta = 20 + 60e^{-kt};\quad t = 10:\ 30 = 60e^{-10k} \Rightarrow e^{-10k} = \tfrac12", r"t = 20:\ \text{excess } 60\cdot\tfrac14 = 15 \Rightarrow \theta = 35\,^\circ\text{C}", r"10 = 60e^{-kt} \Rightarrow t = \frac{10\ln 6}{\ln 2} \approx 25.8\ \text{min}"],
                 ["Back to the tea.", "Newton's law: the excess over the room decays exponentially. It halves in ten minutes.", "After twenty minutes, it has halved twice: fifteen degrees above the room, thirty five.", "For thirty degrees, the excess must fall to ten: about twenty five point eight minutes."])
        self.quiz("The order and degree of (d²y/dx²)³ + (dy/dx)⁴ = x are",
                  ["2 and 3", "2 and 4", "3 and 2", "4 and 2"], 0,
                  "Pause and think.",
                  "Order two, the second derivative; degree three, its power. The fourth power belongs to a lower derivative.")
        self.quiz("The integrating factor of dy/dx + (1/x) y = x² is",
                  ["eˣ", "x", "ln x", "1/x"], 1,
                  "One more.",
                  "x: e to the integral of one over x is e to the log x, which is x.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Order: highest derivative; degree: its power after clearing roots. n constants → differentiate n times.",
            "Separable: f(y) dy = g(x) dx, integrate both sides.",
            "Homogeneous dy/dx = F(y/x): put y = vx, then separate.",
            "Linear dy/dx + Py = Q: I = e^(∫P dx), Iy = ∫IQ dx + C. Exact: ∂M/∂y = ∂N/∂x, find u.",
            "Growth/decay P = P₀eᵏᵗ; cooling θ = θₛ + (θ₀ − θₛ)e⁻ᵏᵗ.",
        ], "Quick recap. Order and degree, and forming an equation by eliminating constants. Separate the variables when you can. Homogeneous equations: put y equal to v x. Linear equations: multiply by the integrating factor. Exact equations: find u. And the exponential laws of growth, decay and cooling.")
        self.outro("That was differential equations. Next, computational methods: solving equations numerically. See you there.")
