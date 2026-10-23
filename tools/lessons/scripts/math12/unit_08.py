import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402

def conic_name(e):
    if e < 0.02:
        return "circle", th.SKY
    if e < 0.985:
        return "ellipse", th.MINT
    if e < 1.015:
        return "parabola", th.AMBER
    return "hyperbola", th.CORAL


def polar_conic(e, l, focus, scale=1.0, box=((-7, 7), (-3.6, 3.6)), color=th.MINT, width=4):
    """r = l / (1 + e cos θ) about `focus` (directrix to the right); drawn only inside `box`."""
    g, cur = VGroup(), []
    for t in np.linspace(0, TAU, 900):
        den = 1 + e * np.cos(t)
        ok = den > 1e-3
        if ok:
            r = l / den * scale
            p_ = np.array(focus) + np.array([r * np.cos(t), r * np.sin(t), 0])
            ok = box[0][0] <= p_[0] <= box[0][1] and box[1][0] <= p_[1] <= box[1][1]
        if ok:
            cur.append(p_)
        else:
            if len(cur) > 1:
                g.add(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(cur))
            cur = []
    if len(cur) > 1:
        g.add(VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(cur))
    return g


def axes_at(center, xr, yr, unit=1.0, nums=False):
    ax = Axes(x_range=xr, y_range=yr, x_length=(xr[1] - xr[0]) * unit, y_length=(yr[1] - yr[0]) * unit, tips=False,
              axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": nums, "font_size": 18}).move_to(center)
    ax.shift(np.array(center) - ax.c2p(0, 0))
    return ax


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 8
    TITLE = "Conic Sections"
    SUBTITLE = "One cone, one plane, four curves"
    SECTIONS = ["One definition, four curves", "Circle: condition of tangency", "Tangent and normal to a circle", "Parabola", "Ellipse", "Hyperbola"]
    NEXT = "Unit 9 · Product of Vectors"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        apex = np.array([-3.6, 0.2, 0])
        al = np.radians(30)
        L = 3.2
        cone = VGroup(*[Line(apex - L * np.array([np.sin(s * al), np.cos(s * al), 0]) * k, apex + L * np.array([np.sin(s * al), np.cos(s * al), 0]) * k, color=th.MUTED, stroke_width=3) for s in (1, -1) for k in (1,)])
        axis = DashedLine(apex + DOWN * 3.3, apex + UP * 3.3, color=th.FAINT)
        beta = ValueTracker(0.0)
        piv = apex + DOWN * 1.6
        cut = always_redraw(lambda: Line(piv - 2.6 * np.array([np.cos(np.radians(beta.get_value())), np.sin(np.radians(beta.get_value())), 0]),
                                         piv + 2.6 * np.array([np.cos(np.radians(beta.get_value())), np.sin(np.radians(beta.get_value())), 0]), color=th.AMBER, stroke_width=5))
        ecc = lambda: np.sin(np.radians(beta.get_value())) / np.cos(al)

        def curve():
            e = ecc()
            name, col = conic_name(e)
            return polar_conic(e, 1.1, (2.6 if e < 0.98 else 2.0, -0.4, 0), box=((-0.4, 6.8), (-3.2, 2.6)), color=col, width=5)

        def label():
            e = ecc()
            name, col = conic_name(e)
            return VGroup(T(name, size=38, color=col, weight="BOLD"), VGroup(M("e =", size=38), DecimalNumber(e, num_decimal_places=2, font_size=42, color=col)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.15).move_to([3.0, 2.7, 0])

        cv, lb = always_redraw(curve), always_redraw(label)
        with self.say("Take a double cone, seen here from the side, and slice it with a flat plane, the yellow line. A level cut gives a circle."):
            self.play(Create(cone), Create(axis))
            self.add(cut, cv, lb)
            self.wait(0.6)
        with self.say("Tilt the plane a little: an ellipse. Tilt it until it runs parallel to the side of the cone: the ellipse breaks open into a parabola. Tilt it further, so it cuts both halves of the cone: a hyperbola, in two branches."):
            self.play(beta.animate.set_value(35), run_time=2.0)
            self.wait(0.4)
            self.play(beta.animate.set_value(60), run_time=1.8)
            self.wait(0.4)
            self.play(beta.animate.set_value(75), run_time=1.6)
        with self.say("Four curves that look nothing alike, from one construction. They are the paths of planets and comets, the shape of a satellite dish and a cooling tower. And, as you will see, they all obey one single rule."):
            nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(cone, axis)), FadeOut(cut), FadeOut(cv), FadeOut(lb))
        self.remove(cut, cv, lb)
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 8: Conic Sections."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. One definition for all four curves. When a line touches a circle. Tangents and normals to a circle. Then the parabola, the ellipse and the hyperbola, each with its standard equation, its elements and its tangents.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "Focus–directrix: PS = e · PM")
        S = np.array([-1.7, -0.4, 0])
        d = 2.2
        e = 0.6
        dline = Line(S + np.array([d, -2.6, 0]), S + np.array([d, 2.7, 0]), color=th.CORAL, stroke_width=3)
        dl = T("directrix", size=22, color=th.CORAL).next_to(dline, DOWN, buff=0.08)
        Sd = Dot(S, radius=0.09, color=th.AMBER)
        Sl = M("S", size=28, color=th.AMBER).next_to(S, DL, buff=0.08)
        ell = polar_conic(e, e * d, S, color=th.MINT)
        th_ = ValueTracker(0.6)

        def Pt():
            t = th_.get_value()
            r = e * d / (1 + e * np.cos(t))
            return S + np.array([r * np.cos(t), r * np.sin(t), 0])

        geo = always_redraw(lambda: VGroup(Line(S, Pt(), color=th.AMBER, stroke_width=4), DashedLine(Pt(), np.array([S[0] + d, Pt()[1], 0]), color=th.CORAL, stroke_width=3),
                                           Dot(Pt(), radius=0.1, color=th.INK), M("P", size=28).next_to(Pt(), UL, buff=0.05), Dot(np.array([S[0] + d, Pt()[1], 0]), radius=0.06, color=th.CORAL)))

        def rd():
            p_ = Pt()
            ps = np.linalg.norm(p_ - S)
            pm = S[0] + d - p_[0]
            return VGroup(VGroup(T("PS =", size=26, color=th.AMBER), DecimalNumber(ps, num_decimal_places=2, font_size=32, color=th.AMBER)).arrange(RIGHT, buff=0.15),
                          VGroup(T("PM =", size=26, color=th.CORAL), DecimalNumber(pm, num_decimal_places=2, font_size=32, color=th.CORAL)).arrange(RIGHT, buff=0.15),
                          VGroup(T("PS ÷ PM =", size=26, color=th.INK), DecimalNumber(ps / pm, num_decimal_places=2, font_size=36, color=th.MINT)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, 1.4, 0])

        r_ = always_redraw(rd)
        with self.say("Here is the single rule. Fix a point S, the focus, and a line, the directrix. A conic is the path of a point P whose distance from the focus is always a fixed multiple e of its distance from the directrix. The number e is the eccentricity."):
            self.play(FadeIn(h), Create(dline), FadeIn(dl), FadeIn(Sd), FadeIn(Sl))
            self.add(geo, r_)
            self.play(Create(ell), th_.animate.set_value(0.6 + TAU), run_time=4.0, rate_func=rate_functions.linear)
        rows = [["eccentricity", "curve"], ["e = 0", "circle (limit)"], ["0 < e < 1", "ellipse"], ["e = 1", "parabola"], ["e > 1", "hyperbola"]]
        tb = P.table(rows, [2.4, 2.9], row_h=0.58, size=24, colors=[th.AMBER, th.INK]).move_to([4.1, -1.7, 0])
        with self.say("Watch P go round. Its two distances change, but their ratio stays at point six. That is an ellipse. Make e exactly one and you get a parabola; more than one, a hyperbola; and as e shrinks to zero, a circle.") as v:
            P.reveal_table(self, tb, v.dur * 0.7)
        self.play(FadeOut(VGroup(h, dline, dl, Sd, Sl, ell, tb)), FadeOut(geo), FadeOut(r_))
        self.remove(geo, r_)
        rows = [["in Ax² + By² + 2gx + 2fy + c = 0", "curve"], ["A = B ≠ 0", "circle"], ["one of A, B is zero", "parabola"], ["A ≠ B, same sign", "ellipse"], ["A, B opposite signs", "hyperbola"]]
        tb = P.table(rows, [6.4, 3.4], row_h=0.66, size=26, colors=[th.INK, th.MINT]).move_to([0, 1.0, 0])
        exs = VGroup(M(r"4x^2 + 9y^2 - 16x + 18y - 11 = 0:\ \text{ellipse}", size=32), M(r"9x^2 - 16y^2 = 144:\ \text{hyperbola}", size=32), M(r"y^2 - 8y - 4x + 20 = 0:\ \text{parabola}", size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.2, 0])
        with self.say("You can name a conic from its equation before doing any algebra. Look only at the squared terms. Equal coefficients: a circle. One square missing: a parabola. Unequal but the same sign: an ellipse. Opposite signs: a hyperbola.") as v:
            P.reveal_table(self, tb, v.dur * 0.8)
        with self.say("So four x squared plus nine y squared is an ellipse; nine x squared minus sixteen y squared, a hyperbola; and an equation with only y squared, a parabola. Name it first, then complete the square."):
            self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.2) for x_ in exs], lag_ratio=0.4))
        self.play(FadeOut(VGroup(tb, exs)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "The circle, in four forms")
        f = VGroup(M(r"(x - h)^2 + (y - k)^2 = r^2", size=40), M(r"x^2 + y^2 = r^2", size=36), M(r"x^2 + y^2 + 2gx + 2fy + c = 0:\ \ \text{centre } (-g, -f),\ r = \sqrt{g^2 + f^2 - c}", size=34, color=th.MINT),
                   M(r"(x - x_1)(x - x_2) + (y - y_1)(y - y_2) = 0\ \ (\text{diameter ends})", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.2, 0])
        says = ["A circle is every point at distance r from a centre h, k. The distance formula, squared, gives the standard form.", "With the centre at the origin, x squared plus y squared equals r squared.",
                "Expand, and every circle looks like x squared plus y squared plus two g x plus two f y plus c equals zero. The centre is minus g, minus f: half the coefficients, signs changed. The radius is root of g squared plus f squared minus c.",
                "And if you know the ends of a diameter, the angle in a semicircle is a right angle, which gives the diameter form."]
        self.play(FadeIn(h))
        for f_, sy in zip(f, says):
            with self.say(sy):
                self.play(Write(f_), run_time=1.1)
        c = self.callout("careful", "Divide by the coefficient of x² FIRST. 3x² + 3y² − 12x + 18y − 6 = 0 → x² + y² − 4x + 6y − 2 = 0: centre (2, −3), r = √15.", width=11, size=25)
        with self.say("A trap: if the squares carry a coefficient, divide it out first. Three x squared plus three y squared and so on: divide by three, and the centre is two, minus three."):
            self.play(FadeOut(f), FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(VGroup(h, c)))
        h = P.head(self, "When does a line touch a circle?")
        ax = axes_at((-3.2, -0.5, 0), [-3.2, 3.2, 1], [-3.2, 3.2, 1], unit=0.95)
        circ = Circle(radius=2 * ax.x_axis.unit_size, stroke_color=th.SKY, stroke_width=4).move_to(ax.c2p(0, 0))
        m_ = -0.5
        c_ = ValueTracker(0.5)

        def line_():
            cc = c_.get_value()
            g = VGroup(P.clipped(ax, lambda x: m_ * x + cc, -3.2, 3.2, -3.2, 3.2, th.AMBER))
            foot = np.array([-m_ * cc / (1 + m_ ** 2), cc / (1 + m_ ** 2)])
            g.add(DashedLine(ax.c2p(0, 0), ax.c2p(*foot), color=th.CORAL, stroke_width=3))
            return g

        def status():
            cc = c_.get_value()
            dd = abs(cc) / np.sqrt(1 + m_ ** 2)
            word, col = ("cuts in 2 points", th.MINT) if dd < 1.985 else (("touches: TANGENT", th.AMBER) if dd < 2.015 else ("misses", th.CORAL))
            return VGroup(VGroup(T("distance d =", size=26, color=th.CORAL), DecimalNumber(dd, num_decimal_places=2, font_size=34, color=th.CORAL), T("  radius = 2", size=26, color=th.SKY)).arrange(RIGHT, buff=0.12),
                          T(word, size=32, color=col, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.8, 0])

        ln, stt = always_redraw(line_), always_redraw(status)
        cond = VGroup(M(r"d = \frac{|c|}{\sqrt{1 + m^2}} = a", size=36), M(r"c^2 = a^2(1 + m^2)", size=46, color=th.AMBER), T("y = mx + c touches x² + y² = a²", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([3.4, -1.4, 0])
        with self.say("Slide a line of fixed slope across a circle of radius two. Watch the red distance from the centre to the line. Less than the radius: the line cuts the circle twice."):
            self.play(FadeIn(h), Create(ax), Create(circ))
            self.add(ln, stt)
            self.wait(0.6)
        with self.say("Equal to the radius: it just touches, a tangent. More than the radius: it misses altogether."):
            self.play(c_.animate.set_value(2 * np.sqrt(1 + m_ ** 2)), run_time=2.0)
            self.wait(0.8)
            self.play(c_.animate.set_value(3.0), run_time=1.0)
            self.play(c_.animate.set_value(2 * np.sqrt(1 + m_ ** 2)), run_time=1.0)
        with self.say("So y equals m x plus c touches x squared plus y squared equals a squared exactly when the distance, c over root of one plus m squared, equals a. That is, c squared equals a squared times one plus m squared."):
            self.play(Write(cond[0]))
            self.play(Write(cond[1]), FadeIn(cond[2]))
        self.play(FadeOut(VGroup(h, ax, circ, cond)), FadeOut(ln), FadeOut(stt))
        self.remove(ln, stt)
        P.worked(self, "Find the circle through (0, 0), (6, 0) and (0, 8). State its centre and radius.",
                 [r"(0,0):\ c = 0;\quad (6,0):\ 36 + 12g = 0 \Rightarrow g = -3;\quad (0,8):\ 64 + 16f = 0 \Rightarrow f = -4", r"x^2 + y^2 - 6x - 8y = 0", r"\text{centre } (3, 4),\quad r = \sqrt{9 + 16} = 5"],
                 ["Three points.", "Put each into the general form: c is zero, g is minus three, f is minus four.", "So the circle is x squared plus y squared minus six x minus eight y equals zero.", "Centre three, four; radius five."])
        P.worked(self, "Find the circle with centre (3, 4) that touches the line 4x − 3y + 10 = 0.",
                 [r"r = \frac{|4(3) - 3(4) + 10|}{\sqrt{16 + 9}} = \frac{10}{5} = 2", r"(x - 3)^2 + (y - 4)^2 = 4"],
                 ["Touching means distance equals radius.", "The perpendicular distance from three, four to the line is ten over five: two.", "So the circle is x minus three squared plus y minus four squared equals four."])
        P.worked(self, "For what c does y = 2x + c touch x² + y² = 20? Find the point of contact for c > 0.",
                 [r"c^2 = 20(1 + 4) = 100 \Rightarrow c = \pm10", r"\left(-\frac{a^2 m}{c},\ \frac{a^2}{c}\right) = \left(-\frac{40}{10},\ \frac{20}{10}\right) = (-4, 2)"],
                 ["Use the condition.", "c squared is twenty times five, a hundred: c is plus or minus ten.", "The point of contact is minus a squared m over c, a squared over c: minus four, two. It lies on both the line and the circle."])

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "The tangent is perpendicular to the radius")
        ax = axes_at((-3.2, -0.5, 0), [-3.3, 3.3, 1], [-3.3, 3.3, 1], unit=0.9)
        u = ax.x_axis.unit_size
        circ = Circle(radius=2.5 * u, stroke_color=th.SKY, stroke_width=4).move_to(ax.c2p(0, 0))
        t = ValueTracker(np.arctan2(4, 3))

        def tang():
            a = t.get_value()
            x1, y1 = 2.5 * np.cos(a), 2.5 * np.sin(a)
            P_ = ax.c2p(x1, y1)
            dirv = np.array([-np.sin(a), np.cos(a), 0])
            return VGroup(Line(ax.c2p(0, 0), P_, color=th.CORAL, stroke_width=4), Line(P_ - 2.2 * dirv, P_ + 2.2 * dirv, color=th.AMBER, stroke_width=4),
                          RightAngle(Line(P_, ax.c2p(0, 0)), Line(P_, P_ + dirv), length=0.22, color=th.MUTED), Dot(P_, color=th.INK))

        tg = always_redraw(tang)
        f = VGroup(M(r"\text{radius slope } \frac{y_1}{x_1} \Rightarrow \text{tangent slope } -\frac{x_1}{y_1}", size=32), M(r"xx_1 + yy_1 = a^2", size=46, color=th.AMBER),
                   M(r"xx_1 + yy_1 + g(x + x_1) + f(y + y_1) + c = 0", size=30), T("normal: the line through P and the centre", size=24, color=th.CORAL)).arrange(DOWN, buff=0.32).move_to([3.4, 0.2, 0])
        with self.say("At any point of a circle, the tangent is perpendicular to the radius. Move the point round and the right angle stays."):
            self.play(FadeIn(h), Create(ax), Create(circ))
            self.add(tg)
            self.play(t.animate.set_value(t.get_value() + 2.2), run_time=2.5)
            self.play(t.animate.set_value(np.arctan2(4, 3)), run_time=1.5)
        with self.say("The radius to x one, y one has slope y one over x one, so the tangent has slope minus x one over y one. Simplify, using the fact that the point is on the circle, and the tangent is x x one plus y y one equals a squared. For a general circle, replace x squared by x x one, y squared by y y one, two x by x plus x one, and two y by y plus y one. And the normal always passes through the centre."):
            for f_ in f:
                self.play(Write(f_), run_time=0.9)
        self.play(FadeOut(VGroup(h, ax, circ, f)), FadeOut(tg))
        self.remove(tg)
        P.worked(self, "Find the tangent and normal to x² + y² = 25 at (3, 4).",
                 [r"9 + 16 = 25\ \checkmark", r"\text{tangent: } 3x + 4y = 25", r"\text{normal: through } (0, 0) \text{ and } (3, 4):\ 4x - 3y = 0"],
                 ["Straight substitution.", "First check that the point is on the circle.", "Tangent: three x plus four y equals twenty five.", "Normal: the line through the centre and the point: four x minus three y equals zero. The slopes multiply to minus one."])
        h = P.head(self, "Tangents from (7, 1) to x² + y² = 25")
        ax = axes_at((-2.4, -0.9, 0), [-5.5, 8, 1], [-5.5, 4.5, 1], unit=0.42)
        u = ax.x_axis.unit_size
        circ = Circle(radius=5 * u, stroke_color=th.SKY, stroke_width=4).move_to(ax.c2p(0, 0))
        dc = DashedVMobject(Circle(radius=np.sqrt(50) * u, color=th.MUTED), num_dashes=60).move_to(ax.c2p(0, 0))
        Pp = Dot(ax.c2p(7, 1), color=th.AMBER)
        Pl = M("(7, 1)", size=26, color=th.AMBER).next_to(Pp, RIGHT, buff=0.1)
        t1 = Line(ax.c2p(7, 1), ax.c2p(4, -3), color=th.MINT, stroke_width=4).scale(1.6, about_point=ax.c2p(7, 1))
        t2 = Line(ax.c2p(7, 1), ax.c2p(3, 4), color=th.MINT, stroke_width=4).scale(1.6, about_point=ax.c2p(7, 1))
        ra = RightAngle(Line(ax.c2p(7, 1), ax.c2p(4, -3)), Line(ax.c2p(7, 1), ax.c2p(3, 4)), length=0.3, color=th.AMBER)
        st = VGroup(M(r"PT = \sqrt{S_1} = \sqrt{49 + 1 - 25} = 5", size=30), M(r"y - 1 = m(x - 7):\ (1 - 7m)^2 = 25(1 + m^2)", size=30), M(r"12m^2 - 7m - 12 = 0 \Rightarrow m = \tfrac43,\ -\tfrac34", size=30),
                    M(r"4x - 3y = 25,\quad 3x + 4y = 25:\ \perp", size=32, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        st.scale_to_fit_width(min(st.width, 6.0)).move_to([3.7, 1.0, 0])
        dl = para("director circle x² + y² = 2a²: tangents drawn from any point on it are perpendicular", width=5.0, size=22, color=th.MUTED).move_to([4.2, -1.4, 0])
        with self.say("From the outside point seven, one, draw the two tangents to the circle of radius five. The tangent length is root of S one: root of forty nine plus one minus twenty five, which is five."):
            self.play(FadeIn(h), Create(ax), Create(circ), FadeIn(Pp), FadeIn(Pl))
            self.play(Write(st[0]))
        with self.say("For the tangents themselves, take any line through seven, one with slope m and apply the tangency condition. The quadratic gives m equals four thirds or minus three quarters."):
            self.play(Write(st[1]), Write(st[2]))
            self.play(Create(t1), Create(t2))
        with self.say("Their slopes multiply to minus one: the tangents are perpendicular. That is no accident. Seven squared plus one squared is fifty, twice twenty five, so the point lies on the director circle, the circle from which every pair of tangents meets at a right angle."):
            self.play(Write(st[3]), Create(ra))
            self.play(Create(dc), FadeIn(dl))
        self.play(FadeOut(VGroup(h, ax, circ, dc, Pp, Pl, t1, t2, ra, st, dl)))
        self.tip("y = mx + c given? Use c² = a²(1 + m²). Line as lx + my + n = 0, or circle not at the origin? Use 'distance from centre = radius'.",
                 "Exam tip. If the line is in the form y equals m x plus c and the circle is centred at the origin, use c squared equals a squared, one plus m squared. Otherwise, use distance from the centre equals the radius.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Parabola: PS = PM  (e = 1)")
        ax = axes_at((-3.0, -0.6, 0), [-2.2, 4.0, 1], [-3.2, 3.2, 1], unit=0.86)
        a = 1.0
        par = ParametricFunction(lambda t: ax.c2p(t * t / (4 * a), t), t_range=[-3.2, 3.2], color=th.MINT, stroke_width=4)
        S = ax.c2p(a, 0)
        dline = Line(ax.c2p(-a, -3.2), ax.c2p(-a, 3.0), color=th.CORAL, stroke_width=3)
        lab = VGroup(Dot(S, color=th.AMBER), M("S(a, 0)", size=26, color=th.AMBER).next_to(S, DR, buff=0.06), T("x = −a", size=22, color=th.CORAL).next_to(dline, DOWN, buff=0.05))
        yv = ValueTracker(2.4)
        geo = always_redraw(lambda: VGroup(Line(S, ax.c2p(yv.get_value() ** 2 / 4, yv.get_value()), color=th.AMBER, stroke_width=4),
                                           Line(ax.c2p(yv.get_value() ** 2 / 4, yv.get_value()), ax.c2p(-a, yv.get_value()), color=th.CORAL, stroke_width=4),
                                           Dot(ax.c2p(yv.get_value() ** 2 / 4, yv.get_value()), color=th.INK)))
        rd = always_redraw(lambda: VGroup(T("PS = PM =", size=26), DecimalNumber(yv.get_value() ** 2 / 4 + a, num_decimal_places=2, font_size=34, color=th.MINT)).arrange(RIGHT, buff=0.15).move_to([3.6, 2.4, 0]))
        der = VGroup(M(r"\sqrt{(x - a)^2 + y^2} = x + a", size=34), M(r"x^2 - 2ax + a^2 + y^2 = x^2 + 2ax + a^2", size=30), M(r"y^2 = 4ax", size=50, color=th.MINT), M(r"\text{latus rectum } = 4a", size=32, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([3.4, -0.6, 0])
        with self.say("A parabola has eccentricity one: every point is exactly as far from the focus as from the directrix. Put the focus at a, zero and the directrix at x equals minus a. Move P along the curve: the yellow and red lengths are always equal."):
            self.play(FadeIn(h), Create(ax), Create(dline), FadeIn(lab))
            self.add(geo, rd)
            self.play(Create(par), yv.animate.set_value(-2.8), run_time=3.0)
            self.play(yv.animate.set_value(1.4), run_time=1.5)
        with self.say("Write PS equals PM with the distance formula, square both sides, and almost everything cancels: y squared equals four a x. The chord through the focus, the latus rectum, has length four a, which is why the four is there."):
            for d_ in der:
                self.play(Write(d_), run_time=0.9)
            lr = Line(ax.c2p(a, -2 * a), ax.c2p(a, 2 * a), color=th.AMBER, stroke_width=6)
            self.play(Create(lr))
        self.play(FadeOut(VGroup(h, ax, par, dline, lab, der, lr)), FadeOut(geo), FadeOut(rd))
        self.remove(geo, rd)
        quads = VGroup()
        specs = [(r"y^2 = 4ax", lambda t: (t * t / 4, t), "right"), (r"y^2 = -4ax", lambda t: (-t * t / 4, t), "left"), (r"x^2 = 4ay", lambda t: (t, t * t / 4), "up"), (r"x^2 = -4ay", lambda t: (t, -t * t / 4), "down")]
        for k, (eq, fn, dirn) in enumerate(specs):
            ax_ = axes_at((0, 0, 0), [-2, 2, 1], [-2, 2, 1], unit=0.62)
            cv = ParametricFunction(lambda t, fn=fn: ax_.c2p(*fn(t)), t_range=[-2.6, 2.6], color=th.MINT, stroke_width=4)
            foc = Dot(ax_.c2p(*[(1, 0), (-1, 0), (0, 1), (0, -1)][k]), radius=0.07, color=th.AMBER)
            g = VGroup(ax_, cv, foc, M(eq, size=30, color=th.INK).next_to(ax_, DOWN, buff=0.15), T(f"opens {dirn}", size=20, color=th.MUTED).next_to(ax_, DOWN, buff=0.6))
            quads.add(g)
        quads.arrange(RIGHT, buff=0.55).move_to([0, 0.5, 0])
        note = para("The squared variable decides the axis. Shifted vertex (h, k): (y − k)² = ±4a(x − h), (x − h)² = ±4a(y − k); focus a units from the vertex along the axis.", width=12, size=23, color=th.INK).move_to([0, -2.7, 0])
        with self.say("Swap or negate the variables and the parabola faces the other three ways. The variable that is squared tells you the axis: y squared opens sideways, x squared opens up or down. Move the vertex to h, k and everything moves with it; the focus is always a units from the vertex along the axis.") as v:
            self.play(LaggedStart(*[FadeIn(q_, shift=UP * 0.2) for q_ in quads], lag_ratio=0.25))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(quads, note)))
        P.worked(self, "Reduce y² − 8y − 4x + 20 = 0 to standard form; find vertex, focus, directrix and latus rectum.",
                 [r"y^2 - 8y + 16 = 4x - 20 + 16 \Rightarrow (y - 4)^2 = 4(x - 1)", r"h = 1,\ k = 4,\ 4a = 4 \Rightarrow a = 1", r"\text{vertex } (1, 4),\ \text{focus } (2, 4),\ \text{directrix } x = 0,\ \text{latus rectum } 4"],
                 ["Only y is squared, so the axis is horizontal.", "Complete the square in y: y minus four squared equals four times x minus one.", "Vertex one, four, and a equals one.", "The focus is one unit right of the vertex, the directrix one unit left: the y axis. Latus rectum four."])
        h = P.head(self, "A suspension bridge over the Karnali")
        road = Line([-6.0, -2.6, 0], [6.0, -2.6, 0], color=th.MUTED, stroke_width=5)
        s = 0.13
        towers = VGroup(*[Rectangle(width=0.25, height=20 * s, stroke_width=0, fill_color="#5C6080", fill_opacity=1).move_to([x, -2.6 + 10 * s, 0]) for x in (-40 * s, 40 * s)])
        cable = ParametricFunction(lambda x: np.array([x * s, -2.6 + (4 + x * x / 100) * s, 0]), t_range=[-40, 40], color=th.AMBER, stroke_width=5)
        hangers = VGroup(*[Line([x * s, -2.6, 0], [x * s, -2.6 + (4 + x * x / 100) * s, 0], color=th.FAINT, stroke_width=2) for x in range(-35, 36, 5)])
        mark = VGroup(DashedLine([20 * s, -2.6, 0], [20 * s, -2.6 + 8 * s, 0], color=th.MINT, stroke_width=4), T("8 m", size=24, color=th.MINT).move_to([20 * s + 0.45, -2.6 + 4 * s, 0]))
        dims = VGroup(T("span 80 m", size=22, color=th.MUTED).move_to([0, -3.0, 0]), T("towers 20 m", size=22, color=th.MUTED).next_to(towers[1], UP, buff=0.12), T("lowest point 4 m", size=22, color=th.MUTED).move_to([0, -2.6 + 4 * s + 0.3, 0]))
        st = VGroup(M(r"x^2 = 4ay \text{ through } (40, 16):\ 1600 = 64a \Rightarrow 4a = 100", size=30), M(r"x = 20:\ y = \tfrac{400}{100} = 4\ \Rightarrow\ 4 + 4 = 8\ \text{m}", size=32, color=th.MINT)).arrange(DOWN, buff=0.25).move_to([0, 2.0, 0])
        with self.say("A real parabola. A bridge cable spans eighty metres, the towers are twenty metres high, and the lowest point of the cable is four metres above the road. How high is the cable twenty metres from the middle?"):
            self.play(FadeIn(h), Create(road), FadeIn(towers), Create(cable), FadeIn(dims))
            self.play(LaggedStart(*[Create(x_) for x_ in hangers], lag_ratio=0.05))
        with self.say("Put the origin at the lowest point: x squared equals four a y. Each tower top is forty across and sixteen up, so four a is a hundred. At twenty metres, y is four: four above the lowest point, eight above the road."):
            self.play(Write(st[0]))
            self.play(Write(st[1]), Create(mark))
        self.play(FadeOut(VGroup(h, road, towers, cable, hangers, mark, dims, st)))
        P.worked(self, "Tangent and normal to y² = 12x at (3, 6); and show y = 2x + 2 touches y² = 16x.",
                 [r"a = 3:\ yy_1 = 2a(x + x_1) \Rightarrow 6y = 6(x + 3) \Rightarrow y = x + 3", r"\text{normal slope } -\frac{y_1}{2a} = -1:\ x + y = 9", r"y^2 = 16x:\ a = 4,\ c = \frac{a}{m} = \frac42 = 2\ \checkmark,\ \text{contact } \left(\frac{a}{m^2}, \frac{2a}{m}\right) = (1, 4)"],
                 ["Parabola tangents.", "The tangent at x one, y one is y y one equals two a times x plus x one: y equals x plus three.", "The normal has slope minus one: x plus y equals nine.", "For y equals m x plus c to touch y squared equals four a x, c must equal a over m. Here four over two is two: it touches, at one, four."])

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Ellipse: PS + PS′ = 2a  (string and two pins)")
        a, b = 3.0, 2.0
        c = np.sqrt(a * a - b * b)
        O = np.array([-2.6, -0.5, 0])
        u = 1.0
        ell = Ellipse(width=2 * a * u, height=2 * b * u, color=th.MINT, stroke_width=4).move_to(O)
        S1, S2 = O + np.array([c * u, 0, 0]), O + np.array([-c * u, 0, 0])
        t = ValueTracker(1.0)
        Pt = lambda: O + np.array([a * np.cos(t.get_value()), b * np.sin(t.get_value()), 0]) * u
        geo = always_redraw(lambda: VGroup(Line(S1, Pt(), color=th.AMBER, stroke_width=4), Line(S2, Pt(), color=th.SKY, stroke_width=4), Dot(Pt(), color=th.INK)))
        pins = VGroup(Dot(S1, color=th.AMBER), Dot(S2, color=th.SKY), M("S", size=26, color=th.AMBER).next_to(S1, DOWN, buff=0.1), M("S'", size=26, color=th.SKY).next_to(S2, DOWN, buff=0.1))
        rd = always_redraw(lambda: VGroup(VGroup(T("PS =", size=24, color=th.AMBER), DecimalNumber(np.linalg.norm(Pt() - S1), num_decimal_places=2, font_size=30, color=th.AMBER)).arrange(RIGHT, buff=0.12),
                                          VGroup(T("PS′ =", size=24, color=th.SKY), DecimalNumber(np.linalg.norm(Pt() - S2), num_decimal_places=2, font_size=30, color=th.SKY)).arrange(RIGHT, buff=0.12),
                                          VGroup(T("sum =", size=24), DecimalNumber(np.linalg.norm(Pt() - S1) + np.linalg.norm(Pt() - S2), num_decimal_places=2, font_size=34, color=th.MINT), T("= 2a", size=24, color=th.MINT)).arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.8, 1.5, 0]))
        with self.say("Tie a loop of string to two pins and pull it tight with a pencil: you draw an ellipse. The two pins are the foci. However the pencil moves, the two distances add up to the same length, two a, the major axis."):
            self.play(FadeIn(h), FadeIn(pins))
            self.add(geo, rd)
            self.play(Create(ell), t.animate.set_value(1.0 + TAU), run_time=4.0, rate_func=rate_functions.linear)
        der = VGroup(M(r"PS = e\,PM:\ x^2(1 - e^2) + y^2 = a^2(1 - e^2)", size=30), M(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1,\quad b^2 = a^2(1 - e^2)", size=36, color=th.MINT), M(r"e = \sqrt{1 - \frac{b^2}{a^2}},\quad \text{foci } (\pm ae, 0),\quad x = \pm\frac ae", size=32),
                     M(r"\text{latus rectum } \frac{2b^2}{a}", size=32, color=th.AMBER)).arrange(DOWN, buff=0.28).move_to([3.3, -1.3, 0])
        with self.say("From the focus directrix rule with e less than one, the algebra gives x squared over a squared plus y squared over b squared equals one, where b squared is a squared times one minus e squared. So e is root of one minus b squared over a squared. The foci are at plus or minus a e, the directrices at plus or minus a over e, and the latus rectum is two b squared over a."):
            self.play(FadeOut(rd))
            for d_ in der:
                self.play(Write(d_), run_time=0.9)
        self.play(FadeOut(VGroup(h, ell, pins, der)), FadeOut(geo))
        self.remove(geo, rd)
        c2 = self.callout("careful", "The foci and directrices go with the LARGER denominator. x²/9 + y²/25 = 1 has foci (0, ±4), not (±4, 0). Don't rename a and b to force a > b.", width=11, size=26)
        with self.say("A common slip. The foci always lie on the axis with the larger denominator. If the bigger number is under y squared, the ellipse is tall, and its foci are on the y axis."):
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.play(FadeOut(c2))
        P.worked(self, "For 9x² + 25y² = 225 find the axes, e, foci, directrices and latus rectum.",
                 [r"\frac{x^2}{25} + \frac{y^2}{9} = 1:\ a = 5,\ b = 3", r"e = \sqrt{1 - \tfrac{9}{25}} = \tfrac45,\quad \text{foci } (\pm4, 0),\quad x = \pm\tfrac{25}{4}", r"\text{axes } 10,\ 6;\quad \text{latus rectum } \frac{2 \cdot 9}{5} = 3.6"],
                 ["Read the ellipse.", "Divide by two twenty five: a is five, b is three.", "e is four fifths, so the foci are at plus or minus four and the directrices at plus or minus twenty five over four.", "Major axis ten, minor six, latus rectum three point six."])
        P.worked(self, "Reduce 4x² + 9y² − 16x + 18y − 11 = 0; find the centre, axes and eccentricity.",
                 [r"4(x^2 - 4x + 4) + 9(y^2 + 2y + 1) = 11 + 16 + 9", r"\frac{(x - 2)^2}{9} + \frac{(y + 1)^2}{4} = 1", r"\text{centre } (2, -1),\ \text{axes } 6, 4,\ e = \frac{\sqrt5}{3},\ \text{foci } (2 \pm \sqrt5, -1)"],
                 ["An untidy one.", "Complete both squares, adding sixteen and nine to the right.", "Divide by thirty six.", "Centre two, minus one; a three, b two; e root five over three; and the foci root five either side of the centre."])
        P.worked(self, "Tangent and normal to x²/25 + y²/16 = 1 at (3, 16/5).",
                 [r"\frac{3x}{25} + \frac{(16/5)y}{16} = 1 \Rightarrow 3x + 5y = 25", r"\frac{a^2x}{x_1} - \frac{b^2y}{y_1} = a^2 - b^2:\ \frac{25x}{3} - 5y = 9 \Rightarrow 25x - 15y = 27"],
                 ["The T equals zero rule again.", "Tangent: x x one over a squared plus y y one over b squared equals one: three x plus five y equals twenty five.", "Normal: twenty five x minus fifteen y equals twenty seven. Slopes minus three fifths and five thirds: perpendicular."])

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "Hyperbola: |PS′ − PS| = 2a,  asymptotes y = ±(b/a)x")
        ax = axes_at((-2.2, -0.4, 0), [-6, 6, 1], [-3.4, 3.4, 1], unit=0.62)
        a, b = 2.0, 1.5
        c = np.sqrt(a * a + b * b)
        br = VGroup(*[ParametricFunction(lambda t, s=s: ax.c2p(s * a * np.cosh(t), b * np.sinh(t)), t_range=[-1.75, 1.75], color=th.CORAL, stroke_width=4) for s in (1, -1)])
        asy = VGroup(*[DashedLine(ax.c2p(-6, -6 * k * b / a), ax.c2p(6, 6 * k * b / a), color=th.FAINT) for k in (1, -1)])
        box = DashedVMobject(Rectangle(width=2 * a * ax.x_axis.unit_size, height=2 * b * ax.y_axis.unit_size, color=th.MUTED).move_to(ax.c2p(0, 0)), num_dashes=40)
        S1, S2 = ax.c2p(c, 0), ax.c2p(-c, 0)
        foci = VGroup(Dot(S1, color=th.AMBER), Dot(S2, color=th.SKY))
        t = ValueTracker(-1.2)
        Pt = lambda: ax.c2p(a * np.cosh(t.get_value()), b * np.sinh(t.get_value()))
        geo = always_redraw(lambda: VGroup(Line(S1, Pt(), color=th.AMBER, stroke_width=4), Line(S2, Pt(), color=th.SKY, stroke_width=4), Dot(Pt(), color=th.INK)))
        rd = always_redraw(lambda: VGroup(T("PS′ − PS =", size=26), DecimalNumber(np.linalg.norm(Pt() - S2) / ax.x_axis.unit_size - np.linalg.norm(Pt() - S1) / ax.x_axis.unit_size, num_decimal_places=2, font_size=34, color=th.MINT), T("= 2a", size=26, color=th.MINT)).arrange(RIGHT, buff=0.12).move_to([4.2, 1.9, 0]))
        with self.say("A hyperbola has eccentricity bigger than one, and comes in two branches. For an ellipse the distances to the foci add to a constant. For a hyperbola, their difference is constant: two a."):
            self.play(FadeIn(h), Create(ax), Create(br), FadeIn(foci))
            self.add(geo, rd)
            self.play(t.animate.set_value(1.2), run_time=3.0)
        der = VGroup(M(r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1,\quad b^2 = a^2(e^2 - 1)", size=34, color=th.CORAL), M(r"e = \sqrt{1 + \frac{b^2}{a^2}} > 1,\quad a^2e^2 = a^2 + b^2", size=32), M(r"y = \pm\frac{b}{a}x", size=36, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([4.0, -1.0, 0])
        with self.say("The same algebra as the ellipse, but now one minus e squared is negative, and the plus sign becomes a minus: x squared over a squared minus y squared over b squared equals one, with b squared equal to a squared times e squared minus one. Far out, the branches hug two straight lines, the asymptotes, y equals plus or minus b over a x: the diagonals of the a by b box."):
            self.play(FadeOut(rd))
            self.play(Write(der[0]), Write(der[1]))
            self.play(Create(box), Create(asy), Write(der[2]))
        self.play(FadeOut(VGroup(h, ax, br, asy, box, foci, der)), FadeOut(geo))
        self.remove(geo, rd)
        c2 = self.callout("careful", "Ellipse: a²e² = a² − b².  Hyperbola: a²e² = a² + b². One sign flip changes e, the foci and the directrices together: name the conic BEFORE touching e.", width=11, size=26)
        with self.say("Keep the two relations apart. For the ellipse, a squared e squared is a squared minus b squared. For the hyperbola, it is plus. Name the curve before you compute e."):
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.play(FadeOut(c2))
        P.worked(self, "For 9x² − 16y² = 144 find the vertices, e, foci, directrices, latus rectum and asymptotes.",
                 [r"\frac{x^2}{16} - \frac{y^2}{9} = 1:\ a = 4,\ b = 3", r"e = \sqrt{1 + \tfrac{9}{16}} = \tfrac54,\quad \text{foci } (\pm5, 0),\quad x = \pm\tfrac{16}{5}", r"\text{vertices } (\pm4, 0),\ \text{latus rectum } \tfrac{18}{4} = 4.5,\ \text{asymptotes } 3x \pm 4y = 0"],
                 ["Read the hyperbola.", "Divide by one forty four: a four, b three.", "e is five quarters, foci at plus or minus five, directrices at plus or minus sixteen fifths.", "Vertices at plus or minus four, latus rectum four point five, and asymptotes three x plus or minus four y equals zero."])
        P.worked(self, "Tangent and normal to x²/16 − y²/9 = 1 at (5, 9/4).",
                 [r"\frac{5x}{16} - \frac{(9/4)y}{9} = 1 \Rightarrow 5x - 4y = 16", r"\frac{a^2x}{x_1} + \frac{b^2y}{y_1} = a^2 + b^2:\ \frac{16x}{5} + 4y = 25 \Rightarrow 16x + 20y = 125"],
                 ["The same rule, with a minus sign.", "Tangent: five x minus four y equals sixteen.", "Normal: sixteen x plus twenty y equals one two five. Slopes five quarters and minus four fifths: perpendicular."])
        rows = [["", "circle", "parabola", "ellipse", "hyperbola"], ["equation", "x² + y² = a²", "y² = 4ax", "x²/a² + y²/b² = 1", "x²/a² − y²/b² = 1"], ["e", "0", "1", "√(1 − b²/a²)", "√(1 + b²/a²)"],
                ["foci", "centre", "(a, 0)", "(±ae, 0)", "(±ae, 0)"], ["tangency", "c² = a²(1 + m²)", "c = a/m", "c² = a²m² + b²", "c² = a²m² − b²"], ["tangent at P", "xx₁ + yy₁ = a²", "yy₁ = 2a(x + x₁)", "xx₁/a² + yy₁/b² = 1", "xx₁/a² − yy₁/b² = 1"]]
        tb = P.table(rows, [2.0, 2.6, 2.6, 2.9, 2.9], row_h=0.78, size=26, colors=[th.AMBER, th.SKY, th.AMBER, th.MINT, th.CORAL]).move_to([0, 0.2, 0])
        with self.say("Here is the whole unit in one table: the standard equation, the eccentricity, the foci, the condition of tangency and the tangent at a point, for each of the four curves. Roughly a third of the marks in this unit are read straight off it.") as v:
            P.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        self.quiz("The eccentricity of a parabola is",
                  ["0", "between 0 and 1", "1", "greater than 1"], 2,
                  "Pause and think.",
                  "Exactly one: every point is as far from the focus as from the directrix.")
        self.quiz("The foci of x²/9 + y²/25 = 1 are",
                  ["(±4, 0)", "(0, ±4)", "(±3, 0)", "(0, ±5)"], 1,
                  "One more. Which denominator is larger?",
                  "Zero, plus or minus four. The larger denominator, twenty five, is under y squared, so the foci are on the y axis, root of twenty five minus nine away.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "A conic: PS = e·PM. e = 0 circle, e < 1 ellipse, e = 1 parabola, e > 1 hyperbola.",
            "Circle: centre (−g, −f), r = √(g² + f² − c); y = mx + c touches x² + y² = a² iff c² = a²(1 + m²).",
            "Parabola y² = 4ax: focus (a, 0), directrix x = −a, latus rectum 4a; tangent yy₁ = 2a(x + x₁).",
            "Ellipse: b² = a²(1 − e²), PS + PS′ = 2a. Hyperbola: b² = a²(e² − 1), |PS − PS′| = 2a, asymptotes y = ±bx/a.",
            "Tangent at (x₁, y₁): the T = 0 rule — replace x² by xx₁, y² by yy₁.",
        ], "Quick recap. One rule, PS equals e times PM, gives all four conics. The circle's centre and radius from the general form, and the tangency condition. The parabola, ellipse and hyperbola with their foci, directrices and latus recta. And the tangent at a point, by the T equals zero rule.")
        self.outro("That was conic sections. Next, product of vectors: the scalar and vector products and what they measure. See you there.")
