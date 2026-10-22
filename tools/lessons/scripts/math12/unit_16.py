import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

G = 10.0


def plot_axes(center, xr, yr, w, h, nums=True, size=18):
    return Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, tips=False,
                axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": nums, "font_size": size}).move_to(center)


def force(o, v, color, w=6):
    return Arrow(o, o + v, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.15)


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 16
    TITLE = "Mechanics"
    SUBTITLE = "Forces at rest and in motion"
    SECTIONS = ["Resultant, equilibrium and Lami's theorem", "Moments and the inclined plane", "Newton's laws", "Connected bodies, lifts and momentum", "Projectiles"]
    NEXT = "Unit 17 · Appendix: Retained Topics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = plot_axes([0, -0.6, 0], [0, 42, 10], [0, 22, 5], 11.0, 4.6)
        u = 20.0
        cols = [th.SKY, th.MINT, th.AMBER, th.PINK, th.CORAL]
        angs = [15, 30, 45, 60, 75]
        paths = VGroup()
        for a, c in zip(angs, cols):
            t = np.radians(a)
            Tf = 2 * u * np.sin(t) / G
            paths.add(ax.plot_parametric_curve(lambda s, t=t: np.array([u * np.cos(t) * s, u * np.sin(t) * s - G * s * s / 2]), t_range=[0, Tf], color=c, stroke_width=4))
        labs = VGroup(*[T(f"{a}°", size=22, color=c).next_to(p_.get_end(), UP, buff=0.08) for a, c, p_ in zip(angs, cols, paths)])
        with self.say("Throw a ball at twenty metres per second. At fifteen degrees it skims low; at seventy five it climbs high and drops close by. In between, forty five degrees sends it furthest of all, forty metres."):
            self.play(Create(ax))
            for p_, l_ in zip(paths, labs):
                self.play(Create(p_), FadeIn(l_), run_time=0.9)
        with self.say("And notice: fifteen and seventy five degrees land at exactly the same spot, and so do thirty and sixty. Mechanics explains why. This unit is about forces: when they balance, and how they move things."):
            self.play(Indicate(VGroup(paths[0], paths[4]), color=WHITE), Indicate(VGroup(labs[0], labs[4])))
            nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, paths, labs)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 16: Mechanics, the alternative to Unit 15."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Five parts. The resultant of forces, equilibrium and Lami's theorem. Moments and the inclined plane. Newton's laws of motion. Connected bodies, lifts and momentum. And projectiles.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "The resultant: parallelogram law")
        O = np.array([-4.2, -1.6, 0])
        s = 0.42
        P_, Q_ = 5.0, 3.0
        th_ = ValueTracker(60)

        def pic():
            t = np.radians(th_.get_value())
            a = P_ * s * RIGHT
            b = Q_ * s * np.array([np.cos(t), np.sin(t), 0])
            return VGroup(DashedLine(O + a, O + a + b, color=th.FAINT), DashedLine(O + b, O + a + b, color=th.FAINT), force(O, a, th.SKY), force(O, b, th.PINK), force(O, a + b, th.MINT, w=7))

        def rd():
            t = np.radians(th_.get_value())
            R = np.sqrt(P_ ** 2 + Q_ ** 2 + 2 * P_ * Q_ * np.cos(t))
            return VGroup(VGroup(T("θ =", size=26), DecimalNumber(th_.get_value(), num_decimal_places=0, font_size=34), T("°", size=26)).arrange(RIGHT, buff=0.1),
                          VGroup(T("R =", size=26, color=th.MINT), DecimalNumber(R, num_decimal_places=2, font_size=36, color=th.MINT), T("N", size=24)).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 2.2, 0])

        pc, r_ = always_redraw(pic), always_redraw(rd)
        f = VGroup(M(r"R^2 = P^2 + Q^2 + 2PQ\cos\theta", size=36, color=th.MINT), M(r"\tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta}", size=34), T("forces of 5 N and 3 N at 60°: R = √49 = 7 N", size=24, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([3.6, 0.0, 0])
        with self.say("Two forces pulling on one point have a single equivalent force, the resultant: the diagonal of the parallelogram they make. Five newtons and three newtons at sixty degrees combine into exactly seven. Close the angle and the resultant grows to eight; open it to one eighty and it shrinks to two."):
            self.play(FadeIn(h))
            self.add(pc, r_)
            self.play(Write(f[0]), Write(f[1]))
            self.play(FadeIn(f[2]))
            self.play(th_.animate.set_value(0), run_time=1.5)
            self.play(th_.animate.set_value(180), run_time=2.0)
            self.play(th_.animate.set_value(60), run_time=1.2)
        self.play(FadeOut(VGroup(h, f)), FadeOut(pc), FadeOut(r_))
        self.remove(pc, r_)
        h = P.head(self, "Three forces in equilibrium: Lami's theorem")
        ceil = Line([-6.4, 2.4, 0], [-0.8, 2.4, 0], color=th.MUTED, stroke_width=6)
        A_ = np.array([-6.0, 2.4, 0])
        Opt = A_ + 3.0 * np.array([np.cos(np.radians(-30)), np.sin(np.radians(-30)), 0])
        B_ = Opt + (2.4 - Opt[1]) / np.sin(np.radians(60)) * np.array([np.cos(np.radians(60)), np.sin(np.radians(60)), 0])
        strings = VGroup(Line(Opt, A_, color=th.SKY, stroke_width=5), Line(Opt, B_, color=th.PINK, stroke_width=5), Line(Opt, Opt + DOWN * 1.6, color=th.INK, stroke_width=5))
        wt = Square(side_length=0.9, stroke_color=th.INK, fill_color="#5C6080", fill_opacity=1).move_to(Opt + DOWN * 2.05)
        lab = VGroup(M("T_1", size=30, color=th.SKY).move_to((Opt + A_) / 2 + np.array([-0.2, -0.3, 0])), M("T_2", size=30, color=th.PINK).move_to((Opt + B_) / 2 + np.array([0.35, -0.1, 0])), T("100 N", size=22).move_to(wt),
                     T("30°", size=22, color=th.MUTED).move_to(A_ + np.array([0.7, -0.2, 0])), T("60°", size=22, color=th.MUTED).move_to(B_ + np.array([-0.35, -0.3, 0])))
        f = VGroup(M(r"\frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{R}{\sin\gamma}", size=40, color=th.MINT), para("each force ÷ sine of the angle between the OTHER two", width=5.2, size=24, color=th.MUTED),
                   M(r"\frac{T_1}{\sin150^\circ} = \frac{T_2}{\sin120^\circ} = \frac{100}{\sin90^\circ}", size=32), M(r"T_1 = 50\ \text{N},\quad T_2 = 86.6\ \text{N}", size=36, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([3.6, -0.2, 0])
        with self.say("When three forces hold a point still, Lami's theorem links them: each force divided by the sine of the angle between the other two gives the same number. A hundred newton weight hangs from two strings at thirty and sixty degrees to the ceiling."):
            self.play(FadeIn(h), Create(ceil), Create(strings), FadeIn(wt), FadeIn(lab))
            self.play(Write(f[0]), FadeIn(f[1]))
        with self.say("The strings are at right angles to each other, so the weight sits opposite ninety degrees; the tensions sit opposite one fifty and one twenty. Lami gives fifty newtons in the shallow string and eighty six point six in the steep one. The steeper string carries more."):
            self.play(Write(f[2]))
            self.play(Write(f[3]))
        self.play(FadeOut(VGroup(h, ceil, strings, wt, lab, f)))
        P.worked(self, "Forces of 3 N, 4 N and 5 N keep a point in equilibrium. Find the angle between the 3 N and 4 N forces.",
                 [r"\text{resultant of 3 and 4 must be 5:}\quad 25 = 9 + 16 + 24\cos\theta", r"\cos\theta = 0 \Rightarrow \theta = 90^\circ"],
                 ["Equilibrium of three forces.", "The third force balances the other two, so the resultant of three and four is five.", "So cos theta is zero: the forces are at right angles. A three four five triangle."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Moments: a beam on two supports")
        s = 2.0
        A_ = np.array([-5.4, -0.6, 0])
        beam = Rectangle(width=4 * s, height=0.25, stroke_color=th.INK, fill_color="#8B5A2B", fill_opacity=1).move_to(A_ + RIGHT * 2 * s)
        sup = VGroup(*[Triangle(stroke_color=th.MUTED, fill_color=th.MUTED, fill_opacity=1).scale(0.25).move_to(A_ + RIGHT * x * s + DOWN * 0.35) for x in (0, 4)])
        fs = VGroup(force(A_ + RIGHT * 2 * s + DOWN * 0.15, DOWN * 1.3, th.INK), force(A_ + RIGHT * 1 * s + DOWN * 0.15, DOWN * 1.6, th.CORAL), force(A_ + DOWN * 0.55, UP * 2.2, th.MINT), force(A_ + RIGHT * 4 * s + DOWN * 0.55, UP * 1.6, th.MINT))
        fl = VGroup(T("200 N", size=22).next_to(fs[0].get_end(), DOWN, buff=0.05), T("300 N", size=22, color=th.CORAL).next_to(fs[1].get_end(), DOWN, buff=0.05), M("R_A", size=28, color=th.MINT).next_to(fs[2].get_end(), UP, buff=0.05), M("R_B", size=28, color=th.MINT).next_to(fs[3].get_end(), UP, buff=0.05))
        dims = VGroup(T("1 m", size=20, color=th.MUTED).move_to(A_ + RIGHT * 0.5 * s + UP * 0.35), T("4 m", size=20, color=th.MUTED).move_to(A_ + RIGHT * 3 * s + UP * 0.35))
        st = VGroup(M(r"\text{moments about } A:\ 4R_B = 200(2) + 300(1) = 700", size=30), M(r"R_B = 175\ \text{N},\quad R_A = 500 - 175 = 325\ \text{N}", size=34, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([1.6, 2.2, 0])
        with self.say("A force also turns things. Its moment about a point is the force times its perpendicular distance from the point. A four metre beam weighing two hundred newtons rests on two supports, with a three hundred newton load one metre from A."):
            self.play(FadeIn(h), FadeIn(beam), FadeIn(sup), FadeIn(dims))
            self.play(LaggedStart(*[GrowArrow(f_) for f_ in fs], lag_ratio=0.2), FadeIn(fl))
        with self.say("Take moments about A, so the unknown R A has no turning effect. Four R B equals two hundred times two plus three hundred times one. R B is a hundred and seventy five newtons. The vertical forces balance, so R A is three twenty five. The support nearer the load carries more."):
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        self.play(FadeOut(VGroup(h, beam, sup, fs, fl, dims, st)))
        h = P.head(self, "A block on a smooth plane at 30°")
        O = np.array([-5.8, -2.4, 0])
        L = 6.0
        a = np.radians(30)
        top = O + L * np.array([np.cos(a), np.sin(a), 0])
        plane = Polygon(O, O + RIGHT * L * np.cos(a), top, stroke_color=th.MUTED, fill_color=th.PANEL, fill_opacity=1)
        c = O + 0.55 * L * np.array([np.cos(a), np.sin(a), 0]) + 0.32 * np.array([-np.sin(a), np.cos(a), 0])
        blk = Square(side_length=0.6, stroke_color=th.INK, fill_color="#5C6080", fill_opacity=1).rotate(a).move_to(c)
        up = np.array([np.cos(a), np.sin(a), 0])
        nrm = np.array([-np.sin(a), np.cos(a), 0])
        fs = VGroup(force(c, DOWN * 2.0, th.INK), force(c, nrm * 1.73, th.MINT), force(c, up * 1.0, th.AMBER), DashedLine(c, c - up * 1.0, color=th.SKY), DashedLine(c, c - nrm * 1.73, color=th.SKY))
        fl = VGroup(M("mg", size=28).next_to(fs[0].get_end(), DOWN, buff=0.05), M("N", size=28, color=th.MINT).next_to(fs[1].get_end(), UP, buff=0.05), M("P", size=28, color=th.AMBER).next_to(fs[2].get_end(), UR, buff=0.05),
                    M(r"mg\sin\alpha", size=24, color=th.SKY).next_to(c - up * 1.0, DOWN, buff=0.1), M(r"mg\cos\alpha", size=24, color=th.SKY).next_to(c - nrm * 1.73, RIGHT, buff=0.1))
        st = VGroup(M(r"\text{along: } P = mg\sin30^\circ = 200 \cdot \tfrac12 = 100\ \text{N}", size=32), M(r"\text{across: } N = mg\cos30^\circ = 100\sqrt3 \approx 173.2\ \text{N}", size=32, color=th.MINT), T("resolve along and perpendicular to the plane", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([3.5, 0.6, 0])
        with self.say("On a slope, resolve along the plane and perpendicular to it. A twenty kilogram block on a smooth thirty degree slope: its weight, two hundred newtons, splits into mg sin alpha down the slope and mg cos alpha into it. So holding it needs a hundred newtons up the slope, and the plane pushes back with a hundred root three."):
            self.play(FadeIn(h), FadeIn(plane), FadeIn(blk))
            self.play(GrowArrow(fs[0]), FadeIn(fl[0]))
            self.play(Create(fs[3]), Create(fs[4]), FadeIn(fl[3:]))
            self.play(GrowArrow(fs[1]), GrowArrow(fs[2]), FadeIn(fl[1:3]))
            for s_ in st:
                self.play(Write(s_), run_time=0.8)
        self.play(FadeOut(VGroup(h, plane, blk, fs, fl, st)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "F = ma, and the equations of motion")
        laws = P.bullets(["1. A body keeps its state of rest or uniform motion unless a net force acts.", "2. F = ma: the net force equals mass × acceleration.", "3. Action and reaction are equal and opposite, on DIFFERENT bodies."], width=11.5, size=26).move_to([0, 1.4, 0])
        eqs = VGroup(M(r"v = u + at", size=36), M(r"s = ut + \tfrac12at^2", size=36), M(r"v^2 = u^2 + 2as", size=36)).arrange(RIGHT, buff=0.8).move_to([0, -1.2, 0])
        el = T("for constant acceleration", size=24, color=th.MUTED).next_to(eqs, DOWN, buff=0.3)
        with self.say("Newton's three laws. Without a net force, nothing changes. With one, the acceleration is the force divided by the mass. And forces come in equal and opposite pairs, acting on different bodies. For constant acceleration, three equations connect velocity, distance and time.") as v:
            self.play(FadeIn(h))
            P.reveal_list(self, laws, v.dur * 0.6)
            self.play(Write(eqs), FadeIn(el))
        self.play(FadeOut(VGroup(h, laws, eqs, el)))
        h = P.head(self, "A block on a rough floor")
        floor = Line([-6.2, -1.6, 0], [6.2, -1.6, 0], color=th.MUTED, stroke_width=5)
        tex = VGroup(*[Line([x, -1.6, 0], [x - 0.2, -1.8, 0], color=th.FAINT) for x in np.arange(-6, 6.2, 0.4)])
        xb = ValueTracker(-5.0)
        blk = always_redraw(lambda: VGroup(Square(side_length=1.0, stroke_color=th.INK, fill_color="#5C6080", fill_opacity=1).move_to([xb.get_value(), -1.1, 0]), T("10 kg", size=20).move_to([xb.get_value(), -1.1, 0]),
                                           force(np.array([xb.get_value() + 0.5, -1.1, 0]), RIGHT * 1.6, th.AMBER), force(np.array([xb.get_value() - 0.5, -1.5, 0]), LEFT * 1.0, th.CORAL),
                                           T("40 N", size=20, color=th.AMBER).move_to([xb.get_value() + 1.4, -0.75, 0]), T("f = μN = 25 N", size=20, color=th.CORAL).move_to([xb.get_value() - 1.4, -1.95, 0])))
        st = VGroup(M(r"N = mg = 100\ \text{N},\quad f = \mu N = 0.25(100) = 25\ \text{N}", size=32), M(r"a = \frac{40 - 25}{10} = 1.5\ \text{m/s}^2", size=38, color=th.MINT)).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        with self.say("A ten kilogram block is pulled across a rough floor with forty newtons. Friction opposes the motion: the coefficient of friction times the normal reaction, a quarter of a hundred, twenty five newtons. The net force is fifteen newtons, so the acceleration is one and a half metres per second squared."):
            self.play(FadeIn(h), Create(floor), FadeIn(tex))
            self.add(blk)
            self.play(Write(st[0]))
            self.play(xb.animate.set_value(3.5), Write(st[1]), run_time=3.0, rate_func=rate_functions.ease_in_quad)
        self.play(FadeOut(VGroup(h, floor, tex, st)), FadeOut(blk))
        self.remove(blk)
        P.worked(self, "A force of 12 N acts on a 3 kg body at rest on a smooth floor. Find a, v after 5 s, the distance, and the work done.",
                 [r"a = \frac{12}{3} = 4\ \text{m/s}^2;\quad v = 0 + 4(5) = 20\ \text{m/s}", r"s = \tfrac12(4)(25) = 50\ \text{m};\quad W = Fs = 600\ \text{J}", r"\tfrac12mv^2 = \tfrac12(3)(400) = 600\ \text{J}\ \checkmark"],
                 ["Newton's second law at work.", "Acceleration four; after five seconds, twenty metres per second.", "It has gone fifty metres, and the work done is six hundred joules.", "Which equals the kinetic energy gained. Work turns into kinetic energy."])
        P.worked(self, "A stone is thrown straight up at 20 m/s. Find its greatest height and its time in the air.",
                 [r"v^2 = u^2 + 2as:\ 0 = 400 - 20s \Rightarrow s = 20\ \text{m}", r"v = u + at:\ 0 = 20 - 10t \Rightarrow t = 2\ \text{s};\quad \text{total } 4\ \text{s}"],
                 ["Vertical motion.", "At the top the velocity is zero: twenty metres up.", "It takes two seconds to rise, and by symmetry two to fall: four in all."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Two masses over a pulley")
        pul = Circle(radius=0.45, stroke_color=th.INK, stroke_width=4).move_to([-3.0, 2.0, 0])
        hang = Line([-3.0, 2.0, 0], [-3.0, 2.8, 0], color=th.MUTED)
        y1 = ValueTracker(0.0)

        def sys_():
            d = y1.get_value()
            yA, yB = -0.4 - d, -0.4 + d
            return VGroup(Line([-3.45, 2.0, 0], [-3.45, yA + 0.4, 0], color=th.INK, stroke_width=3), Line([-2.55, 2.0, 0], [-2.55, yB + 0.3, 0], color=th.INK, stroke_width=3),
                          VGroup(Square(side_length=0.8, stroke_color=th.INK, fill_color=th.CORAL, fill_opacity=0.8).move_to([-3.45, yA, 0]), T("5 kg", size=20).move_to([-3.45, yA, 0])),
                          VGroup(Square(side_length=0.6, stroke_color=th.INK, fill_color=th.SKY, fill_opacity=0.8).move_to([-2.55, yB, 0]), T("3 kg", size=18).move_to([-2.55, yB, 0])))

        sy = always_redraw(sys_)
        st = VGroup(M(r"5g - T = 5a", size=34, color=th.CORAL), M(r"T - 3g = 3a", size=34, color=th.SKY), M(r"\text{add: } 20 = 8a \Rightarrow a = 2.5\ \text{m/s}^2", size=34), M(r"T = 30 + 3(2.5) = 37.5\ \text{N}", size=36, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.2, 0])
        with self.say("Five kilograms and three kilograms hang over a smooth pulley. The heavier side falls, the lighter rises, with the same acceleration and the same tension in the string. Write F equals m a for each mass, positive in its own direction of motion."):
            self.play(FadeIn(h), Create(pul), Create(hang))
            self.add(sy)
            self.play(Write(st[0]), Write(st[1]))
        with self.say("Add the equations and the tension cancels: twenty equals eight a, so a is two and a half. Then the tension is thirty seven and a half newtons: between the two weights, as it must be."):
            self.play(y1.animate.set_value(1.6), Write(st[2]), run_time=2.0, rate_func=rate_functions.ease_in_quad)
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(h, pul, hang, st)), FadeOut(sy))
        self.remove(sy)
        P.worked(self, "A 60 kg person stands in a lift. Find the floor's reaction when the lift accelerates (a) up at 2 m/s², (b) down at 2 m/s², (c) falls freely.",
                 [r"\text{(a) } R - mg = ma \Rightarrow R = 60(10 + 2) = 720\ \text{N}", r"\text{(b) } R = 60(10 - 2) = 480\ \text{N}", r"\text{(c) } a = g \Rightarrow R = 0:\ \text{weightless}"],
                 ["The lift.", "Going up faster, the floor must push harder: seven hundred and twenty newtons.", "Accelerating down, less: four hundred and eighty.", "In free fall the floor pushes not at all: you feel weightless."])
        P.worked(self, "A 3 kg trolley at 4 m/s hits a stationary 5 kg trolley and they move together. Find the common velocity and the kinetic energy lost.",
                 [r"3(4) + 5(0) = 8v \Rightarrow v = 1.5\ \text{m/s}", r"\text{KE: } \tfrac12(3)(16) = 24\ \text{J} \to \tfrac12(8)(2.25) = 9\ \text{J}", r"\text{lost } 15\ \text{J (inelastic collision)}"],
                 ["Momentum.", "Momentum is conserved: twelve before, eight v after. One and a half metres per second.", "Kinetic energy: twenty four joules before, nine after.", "Fifteen joules became heat and sound."])
        P.worked(self, "A 0.15 kg ball hits a wall at 20 m/s and rebounds at 15 m/s. Find the impulse, and the average force over 0.05 s.",
                 [r"\text{impulse} = m(v - u) = 0.15(-15 - 20) = -5.25\ \text{N s}", r"F = \frac{5.25}{0.05} = 105\ \text{N, away from the wall}"],
                 ["Impulse.", "Take towards the wall as positive, so the rebound is minus fifteen. Impulse: minus five point two five newton seconds.", "Spread over a twentieth of a second, the average force is a hundred and five newtons."])

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Projectiles: two independent motions")
        ax = plot_axes([-2.6, -0.6, 0], [0, 40, 10], [0, 12, 4], 7.2, 3.8)
        u, ang = 20.0, ValueTracker(30)

        def path():
            t = np.radians(ang.get_value())
            Tf = 2 * u * np.sin(t) / G
            return ax.plot_parametric_curve(lambda s: np.array([u * np.cos(t) * s, u * np.sin(t) * s - G * s * s / 2]), t_range=[0, Tf], color=th.AMBER, stroke_width=4)

        tt = ValueTracker(0)

        def ball():
            t = np.radians(ang.get_value())
            s = tt.get_value()
            x, y = u * np.cos(t) * s, u * np.sin(t) * s - G * s * s / 2
            p_ = ax.c2p(x, y)
            return VGroup(Dot(p_, color=th.INK, radius=0.11), force(p_, RIGHT * u * np.cos(t) * 0.06, th.SKY, w=4), force(p_, UP * (u * np.sin(t) - G * s) * 0.06 + UP * 1e-3, th.PINK, w=4))

        pa, bl = always_redraw(path), always_redraw(ball)
        st = VGroup(T("horizontal: constant u cos θ", size=24, color=th.SKY), T("vertical: u sin θ, slowed by g", size=24, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 1.9, 0])
        with self.say("A projectile does two things at once. Across, nothing pushes it, so its horizontal velocity stays fixed at u cos theta: the blue arrow never changes. Up and down, gravity slows it, stops it at the top, and brings it back: the pink arrow shrinks, vanishes and grows downward."):
            self.play(FadeIn(h), Create(ax))
            self.add(pa, bl)
            self.play(FadeIn(st))
            self.play(tt.animate.set_value(2.0), run_time=3.0, rate_func=rate_functions.linear)
        f = VGroup(M(r"T = \frac{2u\sin\theta}{g},\quad H = \frac{u^2\sin^2\theta}{2g}", size=32), M(r"R = \frac{u^2\sin 2\theta}{g}", size=40, color=th.MINT), para("sin 2θ is largest at θ = 45°; θ and 90° − θ give the same range", width=5.0, size=22, color=th.MUTED)).arrange(DOWN, buff=0.3)
        f.scale_to_fit_width(min(f.width, 4.8)).move_to([4.3, -0.8, 0])
        with self.say("From these come the formulas: time of flight two u sin theta over g, greatest height u squared sin squared theta over two g, and range u squared sin two theta over g. Sin two theta is largest at forty five degrees. And theta and ninety minus theta have the same sin two theta: that is why fifteen and seventy five degrees landed together."):
            self.play(Write(f[0]))
            self.play(Write(f[1]), FadeIn(f[2]))
            self.play(tt.animate.set_value(0), run_time=0.3)
            self.play(ang.animate.set_value(60), run_time=1.5)
        self.play(FadeOut(VGroup(h, ax, st, f)), FadeOut(pa), FadeOut(bl))
        self.remove(pa, bl)
        P.worked(self, "A ball is projected at 20 m/s at 30°. Find T, H, R, and its speed after 1 s.",
                 [r"u\cos\theta = 17.32,\quad u\sin\theta = 10", r"T = \frac{2(10)}{10} = 2\ \text{s},\quad H = \frac{100}{20} = 5\ \text{m},\quad R = \frac{400\sin60^\circ}{10} = 34.6\ \text{m}", r"t = 1:\ v_y = 10 - 10 = 0 \Rightarrow \text{speed } 17.32\ \text{m/s (at the top)}"],
                 ["The standard projectile.", "Split the velocity: seventeen point three two across, ten up.", "Time of flight two seconds, height five metres, range thirty four point six metres.", "After one second the vertical velocity is zero: it is at the top, moving at seventeen point three two."])
        P.worked(self, "A stone is thrown horizontally at 20 m/s from a 45 m cliff. Find the time, distance and landing speed.",
                 [r"45 = \tfrac12(10)t^2 \Rightarrow t = 3\ \text{s};\quad x = 20(3) = 60\ \text{m}", r"v_y = 30:\ v = \sqrt{20^2 + 30^2} = 36.1\ \text{m/s at } 56.3^\circ \text{ below horizontal}"],
                 ["Horizontal launch.", "Falling forty five metres from rest takes three seconds; meanwhile it travels sixty metres across.", "It lands with thirty downward and twenty across: thirty six point one metres per second."])
        P.worked(self, "With u = 20 m/s, find the two angles giving a range of 20 m, and the maximum range.",
                 [r"20 = \frac{400\sin2\theta}{10} \Rightarrow \sin2\theta = \tfrac12", r"2\theta = 30^\circ \text{ or } 150^\circ \Rightarrow \theta = 15^\circ \text{ or } 75^\circ", r"R_{\max} = \frac{u^2}{g} = 40\ \text{m at } 45^\circ"],
                 ["The cold open, explained.", "Sin two theta must be a half.", "So two theta is thirty or one fifty: fifteen or seventy five degrees, complementary angles.", "And the maximum, at forty five, is forty metres."])
        self.quiz("Masses 5 kg and 3 kg hang over a smooth pulley (g = 10). The acceleration is",
                  ["10 m/s²", "2.5 m/s²", "5 m/s²", "1.25 m/s²"], 1,
                  "Pause and think.",
                  "Two point five: the difference in weight, twenty newtons, divided by the total mass, eight kilograms.")
        self.quiz("A projectile's horizontal range is greatest when the angle of projection is",
                  ["30°", "45°", "60°", "90°"], 1,
                  "One more.",
                  "Forty five degrees, where sin two theta reaches one.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Resultant: R² = P² + Q² + 2PQ cos θ. Lami: each force ÷ sin(angle between the other two) is equal.",
            "Moments: take moments about an unknown force; then balance the vertical forces.",
            "Inclined plane: resolve mg into mg sin α along and mg cos α across. Friction f = μN.",
            "F = ma; v = u + at, s = ut + ½at², v² = u² + 2as; momentum is conserved in collisions.",
            "Projectile: T = 2u sin θ/g, H = u² sin²θ/2g, R = u² sin 2θ/g, maximum at 45°.",
        ], "Quick recap. The parallelogram law and Lami's theorem for forces at a point. Moments for beams. Resolving on an inclined plane, and friction. Newton's laws, the equations of motion and momentum. And projectiles, with the greatest range at forty five degrees.")
        self.outro("That was mechanics. Next, the appendix: the retained topics you still need for the examination. See you there.")
