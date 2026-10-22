import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402
from _m import polar  # noqa: E402

ZC = th.AMBER
WC = th.SKY


def argand(center=(-3.2, -0.4, 0), r=2.6, unit=1.0, nums=False):
    pl = NumberPlane(x_range=[-r, r, 1], y_range=[-r, r, 1], x_length=2 * r * unit, y_length=2 * r * unit,
                     background_line_style={"stroke_color": th.FAINT, "stroke_width": 1, "stroke_opacity": 0.5},
                     axis_config={"stroke_color": th.MUTED, "stroke_width": 2}).move_to(center)
    lab = VGroup(T("Re", size=20, color=th.MUTED).next_to(pl.c2p(r, 0), DOWN, buff=0.1), T("Im", size=20, color=th.MUTED).next_to(pl.c2p(0, r), LEFT, buff=0.1))
    return pl, lab


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 3
    TITLE = "Complex Numbers"
    SUBTITLE = "Length and angle"
    SECTIONS = ["Polar form", "De Moivre's theorem and roots", "Cube roots of unity", "Euler's formula"]
    NEXT = "Unit 4 · Sequence and Series"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        pl, lab = argand(center=(-1.0, -0.3, 0), r=1.8, unit=1.5)
        O = pl.c2p(0, 0)
        u = pl.x_axis.unit_size
        z = Dot(pl.c2p(1, 0), radius=0.1, color=ZC)
        names = [r"1", r"i", r"-1", r"-i"]
        offs = [DR, UR, DL, DR]
        labs = VGroup(*[M(n_, size=34, color=ZC).next_to(pl.c2p(np.cos(k * PI / 2), np.sin(k * PI / 2)), offs[k], buff=0.1) for k, n_ in enumerate(names)])
        cnt = VGroup(T("multiply by i:", size=24, color=th.MUTED), M(r"1 \to i \to -1 \to -i \to 1", size=36, color=ZC)).arrange(DOWN, buff=0.1).move_to([4.4, 1.8, 0])
        turn = T("each × i = a quarter turn", size=26, color=th.MINT).move_to([4.4, 0.6, 0])
        with self.say("Multiply one by i. You get i. Multiply by i again: minus one. Again: minus i. Again: back to one. Plot those four points and something beautiful appears: multiplying by i is simply a quarter turn."):
            self.play(Create(pl), FadeIn(lab), FadeIn(z), FadeIn(labs[0]), FadeIn(cnt))
            tr = VGroup()
            for k in range(4):
                arc = Arc(radius=u, start_angle=k * PI / 2, angle=PI / 2, arc_center=O, color=ZC, stroke_width=4)
                self.play(Create(arc), MoveAlongPath(z, arc), run_time=0.9)
                tr.add(arc)
                self.add(arc)
                if k < 3:
                    self.play(FadeIn(labs[k + 1], scale=1.4), run_time=0.3)
            self.play(FadeIn(turn))
        with self.say("Complex numbers are really about lengths and turns. See them that way, and powers and roots that look impossible become easy."):
            nb = P.neby_in(self, "surprised", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(pl, lab, z, tr, cnt, labs, turn)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 3: Complex Numbers."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four parts. The polar form, length and angle. De Moivre's theorem, for powers and for roots. The cube roots of unity. And Euler's formula, which ties it all to the number e.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        pl, lab = argand()
        O = pl.c2p(0, 0)
        x, y = ValueTracker(1.0), ValueTracker(1.7320508)
        Pt = always_redraw(lambda: Dot(pl.c2p(x.get_value(), y.get_value()), radius=0.1, color=ZC))
        rad = always_redraw(lambda: Line(O, pl.c2p(x.get_value(), y.get_value()), color=ZC, stroke_width=4))
        proj = always_redraw(lambda: VGroup(DashedLine(pl.c2p(x.get_value(), 0), pl.c2p(x.get_value(), y.get_value()), color=th.MUTED), DashedLine(pl.c2p(0, y.get_value()), pl.c2p(x.get_value(), y.get_value()), color=th.MUTED)))
        ang = always_redraw(lambda: Arc(radius=0.55, start_angle=0, angle=np.arctan2(y.get_value(), x.get_value()), arc_center=O, color=WC, stroke_width=4))

        def readout():
            xv, yv = x.get_value(), y.get_value()
            r = np.hypot(xv, yv)
            t = np.degrees(np.arctan2(yv, xv))
            return VGroup(VGroup(T("z = x + iy:", size=24, color=th.MUTED), T(f"{xv:+.2f} {yv:+.2f} i", size=28, color=th.INK)).arrange(RIGHT, buff=0.2),
                          VGroup(T("r = |z| =", size=24, color=th.MUTED), DecimalNumber(r, num_decimal_places=2, font_size=36, color=ZC)).arrange(RIGHT, buff=0.2),
                          VGroup(T("θ = arg z =", size=24, color=th.MUTED), DecimalNumber(t, num_decimal_places=0, font_size=36, color=WC), T("°", size=28, color=WC)).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.2, 0])

        rd = always_redraw(readout)
        f = M(r"z = r(\cos\theta + i\sin\theta)", size=42, color=th.MINT).move_to([3.6, -1.1, 0])
        f2 = M(r"r = \sqrt{x^2 + y^2},\ \ x = r\cos\theta,\ y = r\sin\theta", size=30).move_to([3.6, -2.0, 0])
        with self.say("Plot z equals x plus i y as the point x, y on the Argand diagram: real axis across, imaginary axis up. Now describe it differently. Its distance from the origin is the modulus, r, root of x squared plus y squared. Its angle from the positive real axis is the argument, theta."):
            self.play(Create(pl), FadeIn(lab))
            self.add(proj, rad, ang, Pt, rd)
            self.wait(1.0)
        with self.say("Since x is r cos theta and y is r sin theta, z equals r times cos theta plus i sin theta. The polar form. Length and angle."):
            self.play(Write(f), Write(f2))
        with self.say("Move the point and watch. The principal argument always lies between minus one eighty and plus one eighty degrees: anticlockwise positive, clockwise negative."):
            for (a_, b_) in [(-1, 1), (-1.732, -1), (1, -1), (1, 1.732)]:
                self.play(x.animate.set_value(a_), y.animate.set_value(b_), run_time=1.3)
        self.play(FadeOut(VGroup(pl, lab, f, f2)), FadeOut(VGroup(Pt, rad, proj, ang, rd)))
        self.remove(Pt, rad, proj, ang, rd)
        rows = [["point", "quadrant", "principal argument"], ["x > 0, y > 0", "I", "α"], ["x < 0, y > 0", "II", "π − α"], ["x < 0, y < 0", "III", "−(π − α)"], ["x > 0, y < 0", "IV", "−α"]]
        tb = P.table(rows, [3.2, 2.2, 4.0], row_h=0.66, size=26, colors=[th.INK, th.MUTED, th.AMBER]).move_to([0, 0.6, 0])
        nt = para("α = tan⁻¹|y/x|, an acute angle. A calculator cannot tell −1 − i from 1 + i: ALWAYS plot the point first.", width=11, size=24, color=th.CORAL).move_to([0, -2.3, 0])
        with self.say("The calculator trap. Inverse tan of y over x cannot tell minus one minus i from one plus i: it gives the same angle. So find the acute angle alpha first, then fix the quadrant from the picture. Second quadrant: pi minus alpha. Third: minus, pi minus alpha. Fourth: minus alpha.") as v:
            P.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        P.worked(self, "Polar form, principal arguments: (a) 1 + i√3, (b) −1 + i, (c) −√3 − i, (d) 1 − i.",
                 [r"\text{(a) } r = 2,\ \alpha = 60^\circ,\ \text{Q I}: \ 2(\cos60^\circ + i\sin60^\circ)", r"\text{(b) } r = \sqrt2,\ \alpha = 45^\circ,\ \text{Q II}: \ \sqrt2(\cos135^\circ + i\sin135^\circ)",
                  r"\text{(c) } r = 2,\ \alpha = 30^\circ,\ \text{Q III}: \ 2[\cos(-150^\circ) + i\sin(-150^\circ)]", r"\text{(d) } r = \sqrt2,\ \alpha = 45^\circ,\ \text{Q IV}: \ \sqrt2[\cos(-45^\circ) + i\sin(-45^\circ)]"],
                 ["Four conversions. Each time: find r, find the acute angle, then fix the quadrant.", "One plus i root three: r two, alpha sixty, first quadrant. Theta is sixty degrees.",
                  "Minus one plus i: second quadrant, so one eighty minus forty five, one thirty five.", "Minus root three minus i: third quadrant, so minus, one eighty minus thirty: minus one fifty.", "And one minus i: fourth quadrant, minus forty five degrees."], colors=[None, None, None, th.AMBER])
        self.p1_mult()

    def p1_mult(self):
        h = P.head(self, "Multiply: lengths multiply, angles add")
        pl, lab = argand(center=(-3.6, -0.4, 0), r=2.0, unit=1.4)
        O = pl.c2p(0, 0)
        z1 = np.array([1.3, 0.4])
        z2 = np.array([1.0, 0.8])
        pr = np.array([z1[0] * z2[0] - z1[1] * z2[1], z1[0] * z2[1] + z1[1] * z2[0]])
        a1, a2 = Arrow(O, pl.c2p(*z1), buff=0, color=ZC, stroke_width=5), Arrow(O, pl.c2p(*z2), buff=0, color=WC, stroke_width=5)
        ap = Arrow(O, pl.c2p(*pr), buff=0, color=th.MINT, stroke_width=6)
        l = VGroup(M(r"z_1", size=34, color=ZC).next_to(a1.get_end(), RIGHT, buff=0.1), M(r"z_2", size=34, color=WC).next_to(a2.get_end(), UP, buff=0.1), M(r"z_1z_2", size=34, color=th.MINT).next_to(ap.get_end(), LEFT, buff=0.1))
        rot = a1.copy()
        t1, t2 = np.arctan2(z1[1], z1[0]), np.arctan2(z2[1], z2[0])
        arcs = VGroup(Arc(radius=0.6, start_angle=0, angle=t1, arc_center=O, color=ZC, stroke_width=4), Arc(radius=0.9, start_angle=0, angle=t2, arc_center=O, color=WC, stroke_width=4),
                      Arc(radius=1.25, start_angle=t1, angle=t2, arc_center=O, color=th.MINT, stroke_width=4))
        f = VGroup(M(r"z_1z_2 = r_1r_2[\cos(\theta_1+\theta_2) + i\sin(\theta_1+\theta_2)]", size=34, color=th.MINT), M(r"\frac{z_1}{z_2} = \frac{r_1}{r_2}[\cos(\theta_1-\theta_2) + i\sin(\theta_1-\theta_2)]", size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, -0.4, 0])
        with self.say("Here is why polar form matters. Multiply two complex numbers. Expand, and the brackets turn out to be exactly the compound angle formulas. So the product has length r one times r two, and angle theta one plus theta two. Multiplying stretches and rotates."):
            self.play(FadeIn(h), Create(pl), FadeIn(lab))
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(l[:2]), Create(arcs[:2]))
            self.play(Transform(rot, ap), Create(arcs[2]), run_time=1.6)
            self.play(FadeIn(l[2]))
            self.play(Write(f[0]))
        with self.say("And dividing does the opposite: divide the lengths, subtract the angles."):
            self.play(Write(f[1]))
        self.play(FadeOut(VGroup(h, pl, lab, a1, a2, rot, l, f, arcs)))
        P.worked(self, "Find the modulus and principal argument of z = (1 + i)/(1 − i√3).",
                 [r"|1+i| = \sqrt2,\ \arg = 45^\circ;\quad |1 - i\sqrt3| = 2,\ \arg = -60^\circ", r"|z| = \frac{\sqrt2}{2} = \frac{1}{\sqrt2},\quad \arg z = 45^\circ - (-60^\circ) = 105^\circ"],
                 ["Use the division rule, with no rationalising.", "The top has modulus root two and argument forty five; the bottom has modulus two and argument minus sixty.", "Divide the moduli and subtract the arguments: modulus one over root two, argument one hundred and five degrees."])

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "De Moivre's theorem")
        f = M(r"(\cos\theta + i\sin\theta)^n = \cos n\theta + i\sin n\theta", size=48, color=th.MINT).move_to([0, 1.6, 0])
        g = M(r"[r(\cos\theta + i\sin\theta)]^n = r^n(\cos n\theta + i\sin n\theta)", size=40).move_to([0, 0.5, 0])
        pf = para("Proof for positive integers by induction: multiplying cos kθ + i sin kθ by cos θ + i sin θ adds the angles, giving cos(k + 1)θ + i sin(k + 1)θ. It extends to negative integers by taking reciprocals, and to fractions with several values.", width=11.5, size=23, color=th.BODY).move_to([0, -1.2, 0])
        with self.say("If multiplying adds angles, then raising to the n th power multiplies the angle by n. That is De Moivre's theorem: cos theta plus i sin theta, to the n, equals cos n theta plus i sin n theta. With a modulus, r becomes r to the n."):
            self.play(FadeIn(h), Write(f))
            self.play(Write(g))
        with self.say("The proof for whole numbers is by induction: each extra factor adds another theta to the angle. It also holds for negative integers, and for fractional powers, where it gives several values."):
            self.play(FadeIn(pf))
        self.play(FadeOut(VGroup(f, g, pf)))
        pl, lab = argand(center=(-2.6, -0.6, 0), r=2.6, unit=1.0)
        O = pl.c2p(0, 0)
        pts, spokes = [], VGroup()
        for k in range(11):
            z = 0.4 * 1.2 ** k * np.exp(1j * np.radians(30 * k))
            pts.append(Dot(pl.c2p(z.real, z.imag), radius=0.08, color=th.AMBER))
            spokes.add(Line(O, pts[-1].get_center(), color=th.AMBER, stroke_width=1.5, stroke_opacity=0.35))
        sp = VMobject(stroke_color=th.AMBER, stroke_width=3).set_points_smoothly([pl.c2p(*(0.4 * 1.2 ** t * np.array([np.cos(np.radians(30 * t)), np.sin(np.radians(30 * t))]))) for t in np.linspace(0, 10, 120)])
        sl = VGroup(M(r"z = r\,\mathrm{cis}\,\theta:\ r = 1.2,\ \theta = 30^\circ", size=30), M(r"z^k:\ \text{length } r^k,\ \text{angle } k\theta", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.6, 0])
        with self.say("Picture it. Each power turns by the same angle and scales by the same factor, so successive powers trace a spiral."):
            self.play(Create(pl), FadeIn(lab), FadeIn(sl))
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(d, scale=1.5)) for l_, d in zip(spokes, pts)], lag_ratio=0.25), Create(sp), run_time=3.0)
        self.play(FadeOut(VGroup(h, pl, lab, *pts, sp, spokes, sl)))
        P.worked(self, "Evaluate (1 + i)¹⁰.",
                 [r"1 + i = \sqrt2(\cos45^\circ + i\sin45^\circ)", r"(1+i)^{10} = (\sqrt2)^{10}(\cos450^\circ + i\sin450^\circ)", r"= 32(\cos90^\circ + i\sin90^\circ) = 32i"],
                 ["Expanding one plus i to the tenth would take eleven terms. Use polar form instead.", "Root two, forty five degrees.", "Raise the modulus to the tenth and multiply the angle by ten: four fifty degrees.", "Four fifty is three sixty plus ninety: thirty two i."])
        P.worked(self, "Show that (√3 + i)⁷ = −64(√3 + i).",
                 [r"\sqrt3 + i = 2(\cos30^\circ + i\sin30^\circ)", r"(\sqrt3+i)^7 = 128(\cos210^\circ + i\sin210^\circ) = 128\left(-\tfrac{\sqrt3}{2} - \tfrac i2\right)", r"= -64\sqrt3 - 64i = -64(\sqrt3 + i)"],
                 ["Another power.", "Modulus two, argument thirty.", "Two to the seven is one two eight; seven times thirty is two ten degrees, in the third quadrant, where cosine and sine are both negative.", "So minus sixty four, root three plus i. Watch those signs: that is where marks go."])
        P.worked(self, "Use De Moivre to prove cos 3θ = 4cos³θ − 3cos θ and sin 3θ = 3 sin θ − 4 sin³θ.",
                 [r"\cos3\theta + i\sin3\theta = (c + is)^3 = c^3 + 3ic^2s - 3cs^2 - is^3", r"\cos3\theta = c^3 - 3c(1 - c^2) = 4c^3 - 3c", r"\sin3\theta = 3(1-s^2)s - s^3 = 3s - 4s^3"],
                 ["A favourite proof.", "De Moivre on one side, the binomial theorem on the other.", "Match real parts, and replace s squared by one minus c squared.", "Match imaginary parts, and replace c squared by one minus s squared."])
        self.p2_roots()

    def p2_roots(self):
        h = P.head(self, "n roots, evenly spaced on a circle")
        pl, lab = argand(center=(-3.0, -0.6, 0), r=2.6)
        O = pl.c2p(0, 0)
        f = M(r"z^{1/n} = r^{1/n}\left[\cos\frac{\theta + 2k\pi}{n} + i\sin\frac{\theta + 2k\pi}{n}\right]", size=36, color=th.MINT).move_to([3.4, 1.4, 0])
        kk = T("k = 0, 1, …, n − 1", size=26, color=th.AMBER).next_to(f, DOWN, buff=0.3)
        with self.say("Roots are where De Moivre really shines. A complex number has infinitely many arguments, theta plus any multiple of two pi, and they all describe the same point. Take the n th root: divide each argument by n. Now they are different! The roots all have modulus r to the one over n, and are spaced two pi over n apart. Exactly n of them, k from zero to n minus one."):
            self.play(FadeIn(h), Create(pl), FadeIn(lab))
            self.play(Write(f), FadeIn(kk))
        circ = Circle(radius=2 * pl.x_axis.unit_size, stroke_color=th.FAINT, stroke_width=2).move_to(O)
        z8 = Dot(pl.c2p(0, 2.6 * 0.95), radius=0.1, color=th.CORAL)
        zl = M(r"8i", size=32, color=th.CORAL).next_to(z8, RIGHT, buff=0.1)
        roots = [2 * np.exp(1j * np.radians(a)) for a in (30, 150, 270)]
        rd = VGroup(*[Dot(pl.c2p(z.real, z.imag), radius=0.12, color=th.AMBER) for z in roots])
        tri = Polygon(*[d.get_center() for d in rd], stroke_color=th.AMBER, stroke_width=3)
        lbl = VGroup(M(r"\sqrt3 + i", size=30, color=th.AMBER).next_to(rd[0], RIGHT, buff=0.1), M(r"-\sqrt3 + i", size=30, color=th.AMBER).next_to(rd[1], LEFT, buff=0.1), M(r"-2i", size=30, color=th.AMBER).next_to(rd[2], DR, buff=0.05))
        steps = VGroup(M(r"8i = 8[\cos(90^\circ + 360^\circ k) + i\sin(90^\circ + 360^\circ k)]", size=30), M(r"(8i)^{1/3} = 2\left[\cos\tfrac{90^\circ + 360^\circ k}{3} + i\sin\tfrac{90^\circ+360^\circ k}{3}\right]", size=30),
                       M(r"30^\circ,\ 150^\circ,\ 270^\circ:\ \ \sqrt3+i,\ -\sqrt3+i,\ -2i", size=30, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, -1.4, 0])
        with self.say("Find the cube roots of eight i. Eight i has modulus eight and argument ninety degrees, plus any multiple of three sixty. Take the cube root: modulus two, and arguments ninety over three, four fifty over three and eight ten over three: thirty, one fifty and two seventy degrees. Root three plus i, minus root three plus i, and minus two i. A perfect equilateral triangle."):
            self.play(FadeIn(z8), FadeIn(zl), Create(circ))
            for s_ in steps:
                self.play(Write(s_), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in rd], lag_ratio=0.3), FadeIn(lbl))
            self.play(Create(tri))
        self.play(FadeOut(VGroup(steps, rd, tri, lbl, z8, zl, f, kk)))
        sq = [2 * np.exp(1j * np.radians(a)) for a in (45, 135, 225, 315)]
        sd = VGroup(*[Dot(pl.c2p(z.real, z.imag), radius=0.12, color=th.MINT) for z in sq])
        sqp = Polygon(*[d.get_center() for d in sd], stroke_color=th.MINT, stroke_width=3)
        t2 = VGroup(M(r"z^4 = -16 = 16(\cos180^\circ + i\sin180^\circ)", size=32), M(r"z = 2\,\mathrm{cis}(45^\circ, 135^\circ, 225^\circ, 315^\circ)", size=32), M(r"= \pm\sqrt2 \pm i\sqrt2", size=36, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.3, 0])
        with self.say("Solve z to the four plus sixteen equals zero. Minus sixteen has modulus sixteen and argument one eighty. Fourth roots: modulus two, angles forty five, one thirty five, two twenty five and three fifteen. Plus or minus root two, plus or minus i root two: the corners of a square."):
            for s_ in t2:
                self.play(Write(s_), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in sd], lag_ratio=0.2))
            self.play(Create(sqp))
        self.play(FadeOut(VGroup(t2, sd, sqp, circ)))
        n = ValueTracker(5)

        def poly():
            k = int(n.get_value())
            pts = [pl.c2p(1.6 * np.cos(TAU * j / k), 1.6 * np.sin(TAU * j / k)) for j in range(k)]
            return VGroup(Polygon(*pts, stroke_color=th.SKY, stroke_width=3), *[Dot(p_, radius=0.09, color=th.SKY) for p_ in pts])

        pg = always_redraw(poly)
        uc = Circle(radius=1.6 * pl.x_axis.unit_size, stroke_color=th.FAINT).move_to(O)
        lab2 = always_redraw(lambda: T(f"n = {int(n.get_value())}", size=30, color=th.SKY).move_to([3.4, 1.8, 0]))
        props = VGroup(VGroup(T("nth roots of unity:", size=24, color=th.INK), M(r"1,\ \omega,\ \omega^2,\ \dots,\ \omega^{n-1}", size=30)).arrange(RIGHT, buff=0.2), T("vertices of a regular n-gon, one at 1", size=24, color=th.INK),
                       T("sum = 0;  product = (−1)ⁿ⁺¹", size=26, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.0, 0])
        with self.say("Put z equal to one: the n th roots of unity. They sit on the unit circle at the corners of a regular n sided polygon, with one corner at one. Their sum is always zero, because they balance perfectly around the centre. Their product is minus one to the n plus one."):
            self.play(Create(uc))
            self.add(pg, lab2)
            self.play(FadeIn(props))
            for k in (6, 7, 8, 3):
                self.play(n.animate.set_value(k), run_time=0.8)
        self.play(FadeOut(VGroup(h, pl, lab, uc, props)), FadeOut(pg), FadeOut(lab2))
        self.remove(pg, lab2)
        self.tip("Write the general argument θ + 2kπ BEFORE dividing by n, and take k = 0, 1, …, n − 1. Then check: the roots should sum to zero (for zⁿ = c).",
                 "Exam tip. Always write theta plus two k pi before you divide by n, and list k from zero to n minus one. Then check: the n roots of z to the n equals a constant always add up to zero.")
        self.quiz("The principal argument of −1 − i is",
                  ["45°", "135°", "−135°", "225°"], 2,
                  "Pause and think. Minus one minus i. What is its principal argument?",
                  "Minus one thirty five degrees. It is in the third quadrant, and the principal value must lie between minus one eighty and one eighty. Forty five is what a calculator gives, and two twenty five is outside the principal range.")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "The cube roots of unity")
        st = VGroup(M(r"z^3 - 1 = (z - 1)(z^2 + z + 1) = 0", size=40), M(r"z = 1,\quad \omega = \frac{-1 + i\sqrt3}{2},\quad \omega^2 = \frac{-1 - i\sqrt3}{2}", size=40, color=th.MINT)).arrange(DOWN, buff=0.45).move_to([2.0, 1.0, 0])
        pl, lab = argand(center=(-4.4, -1.1, 0), r=1.5, unit=1.35)
        O = pl.c2p(0, 0)
        pts = [pl.c2p(np.cos(a), np.sin(a)) for a in (0, TAU / 3, -TAU / 3)]
        dd = VGroup(*[Dot(p_, radius=0.1, color=th.AMBER) for p_ in pts])
        tri = Polygon(*pts, stroke_color=th.AMBER, stroke_width=3)
        ll = VGroup(M("1", size=30, color=th.AMBER).next_to(dd[0], UR, buff=0.05), M(r"\omega", size=30, color=th.AMBER).next_to(dd[1], UP, buff=0.08), M(r"\omega^2", size=30, color=th.AMBER).next_to(dd[2], DOWN, buff=0.08))
        with self.say("Put n equal to three. Factorise z cubed minus one: z minus one, times z squared plus z plus one. So one root is one, and the quadratic gives the other two: minus one plus or minus i root three, over two. Call the first omega. The other is omega squared. On the diagram, they are an equilateral triangle on the unit circle."):
            self.play(FadeIn(h), Write(st[0]))
            self.play(Write(st[1]))
            self.play(Create(pl), FadeIn(lab), LaggedStart(*[FadeIn(d, scale=1.5) for d in dd], lag_ratio=0.2), FadeIn(ll))
            self.play(Create(tri))
        props = VGroup(M(r"\omega^3 = 1 \ \Rightarrow\ \text{reduce powers mod 3}", size=34), M(r"1 + \omega + \omega^2 = 0", size=40, color=th.AMBER), M(r"\omega^2 = \bar\omega = \tfrac{1}{\omega}", size=34),
                       M(r"a^3+b^3+c^3-3abc = (a+b+c)(a+b\omega+c\omega^2)(a+b\omega^2+c\omega)", size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, -1.5, 0])
        with self.say("The properties you will use. Omega cubed is one, so reduce any power modulo three. One plus omega plus omega squared is zero, the most useful line in the unit: so one plus omega is minus omega squared, and so on. Omega squared is the conjugate of omega and also its reciprocal. And they factorise a cubed plus b cubed plus c cubed minus three a b c."):
            self.play(FadeOut(st))
            for p_ in props:
                self.play(Write(p_), run_time=0.9)
        self.play(FadeOut(VGroup(h, pl, lab, dd, tri, ll, props)))
        P.worked(self, "Find ω¹⁰⁰ + ω²⁰⁰ + ω³⁰⁰.",
                 [r"100 = 3(33) + 1 \Rightarrow \omega^{100} = \omega", r"200 = 3(66) + 2 \Rightarrow \omega^{200} = \omega^2;\quad \omega^{300} = 1", r"\omega + \omega^2 + 1 = 0"],
                 ["Reduce the powers.", "A hundred is three thirty three plus one: omega.", "Two hundred leaves remainder two: omega squared. Three hundred: one.", "And omega plus omega squared plus one is zero."])
        P.worked(self, "Prove (1 + ω − ω²)³ + (1 − ω + ω²)³ = −16.",
                 [r"1 + \omega - \omega^2 = -\omega^2 - \omega^2 = -2\omega^2", r"1 - \omega + \omega^2 = -\omega - \omega = -2\omega", r"(-2\omega^2)^3 + (-2\omega)^3 = -8 - 8 = -16"],
                 ["Never expand the cubes. Simplify each bracket first, using one plus omega plus omega squared equals zero.", "One plus omega is minus omega squared, so the first bracket is minus two omega squared.", "Similarly the second is minus two omega.", "Cube them: minus eight omega to the six, which is minus eight, plus minus eight. Minus sixteen."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Euler's formula")
        s = VGroup(M(r"e^{i\theta} = 1 + i\theta + \frac{(i\theta)^2}{2!} + \frac{(i\theta)^3}{3!} + \cdots", size=38),
                   M(r"= \left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots\right) + i\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots\right)", size=36),
                   M(r"e^{i\theta} = \cos\theta + i\sin\theta", size=52, color=th.MINT)).arrange(DOWN, buff=0.45).move_to([0, 0.2, 0])
        says = ["Remember the exponential series from unit two. Put x equal to i theta.", "The powers of i cycle: i, minus one, minus i, one. Separate the terms with i from those without. The first bracket is the series for cos theta, the second for sin theta.",
                "So e to the i theta equals cos theta plus i sin theta. Euler's formula."]
        self.play(FadeIn(h))
        for s_, sy in zip(s, says):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(s))
        pl, lab = argand(center=(-3.0, -0.6, 0), r=1.8, unit=1.25)
        O = pl.c2p(0, 0)
        t = ValueTracker(0.0)
        uc = Circle(radius=pl.x_axis.unit_size, stroke_color=th.FAINT, stroke_width=2).move_to(O)
        pt = always_redraw(lambda: Dot(pl.c2p(np.cos(t.get_value()), np.sin(t.get_value())), radius=0.11, color=th.AMBER))
        rd = always_redraw(lambda: VGroup(Line(O, pl.c2p(np.cos(t.get_value()), np.sin(t.get_value())), color=th.AMBER, stroke_width=3),
                                          Line(O, pl.c2p(np.cos(t.get_value()), 0), color=th.SKY, stroke_width=5), Line(pl.c2p(np.cos(t.get_value()), 0), pl.c2p(np.cos(t.get_value()), np.sin(t.get_value()) + 1e-4), color=th.PINK, stroke_width=4),
                                          M(r"e^{i\theta}", size=30, color=th.AMBER).move_to(pl.c2p(1.32 * np.cos(t.get_value()), 1.32 * np.sin(t.get_value())))))
        cs = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=th.SKY, stroke_width=5), M(r"\cos\theta\ (\text{real part})", size=32)).arrange(RIGHT, buff=0.15),
                    VGroup(Line(ORIGIN, RIGHT * 0.5, color=th.PINK, stroke_width=4), M(r"\sin\theta\ (\text{imaginary part})", size=32)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.1, 0])
        lbl = always_redraw(lambda: VGroup(T("θ =", size=26, color=th.MUTED), DecimalNumber(t.get_value() / PI, num_decimal_places=2, font_size=34, color=th.AMBER), T("π", size=26, color=th.AMBER)).arrange(RIGHT, buff=0.1).move_to([3.4, 2.0, 0]))
        eid = M(r"e^{i\pi} + 1 = 0", size=58, color=th.MINT).move_to([3.4, -0.2, 0])
        form = VGroup(M(r"z = re^{i\theta}", size=38), M(r"\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2},\ \ \sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}", size=30)).arrange(DOWN, buff=0.3).move_to([3.4, -1.8, 0])
        with self.say("As theta grows, e to the i theta walks round the unit circle. At theta equal to pi it reaches minus one. So e to the i pi plus one equals zero: Euler's identity, linking e, i, pi, one and zero in a single line."):
            self.play(Create(pl), FadeIn(lab), Create(uc))
            self.add(rd, pt, lbl)
            self.play(FadeIn(cs))
            self.play(t.animate.set_value(PI), run_time=3.0, rate_func=rate_functions.linear)
            self.play(Write(eid))
        with self.say("Every complex number is then r e to the i theta, and De Moivre is just the law of indices. Adding and subtracting e to the plus and minus i theta gives cos and sin as exponentials."):
            self.play(t.animate.set_value(TAU), run_time=2.0, rate_func=rate_functions.linear)
            self.play(Write(form))
        self.play(FadeOut(VGroup(h, pl, lab, uc, eid, form, cs)), FadeOut(pt), FadeOut(rd), FadeOut(lbl))
        self.remove(pt, rd, lbl)
        P.worked(self, "Prove cos³θ = (3 cos θ + cos 3θ)/4 using Euler's formula.",
                 [r"8\cos^3\theta = (e^{i\theta} + e^{-i\theta})^3", r"= (e^{3i\theta} + e^{-3i\theta}) + 3(e^{i\theta} + e^{-i\theta}) = 2\cos3\theta + 6\cos\theta", r"\cos^3\theta = \frac{3\cos\theta + \cos3\theta}{4}"],
                 ["Euler makes this short.", "Two cos theta is e to the i theta plus e to the minus i theta. Cube both sides.", "Expand by the binomial theorem; the products like e to the i theta times e to the minus i theta are one. Each pair is twice a cosine.", "Divide by eight."])
        P.worked(self, "If x + 1/x = 2 cos θ, prove xⁿ + 1/xⁿ = 2 cos nθ.",
                 [r"x^2 - 2x\cos\theta + 1 = 0 \Rightarrow x = \cos\theta \pm i\sin\theta = e^{\pm i\theta}", r"x^n + x^{-n} = e^{in\theta} + e^{-in\theta} = 2\cos n\theta"],
                 ["A classic.", "Multiply by x and solve the quadratic: x is cos theta plus or minus i sin theta, that is, e to the plus or minus i theta.", "Then x to the n plus its reciprocal is e to the i n theta plus e to the minus i n theta: two cos n theta."])
        self.quiz("If ω is a complex cube root of unity, then 1 + ω + ω² equals",
                  ["1", "0", "−1", "3"], 1,
                  "Pause and think. One plus omega plus omega squared.",
                  "Zero. They are the three roots of z cubed minus one, whose z squared coefficient is zero; geometrically, they balance round the origin. Three would be the answer only if omega were one.")
        self.quiz("The value of (1 + i)⁸ is",
                  ["16", "16i", "−16", "8"], 0,
                  "One more. One plus i to the eighth.",
                  "Sixteen. Root two to the eighth is sixteen, and eight times forty five is three sixty degrees, which points along the positive real axis.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "z = r(cos θ + i sin θ): r = √(x² + y²), θ from the PLOTTED quadrant, −π < θ ≤ π.",
            "Multiply: moduli multiply, arguments add. Divide: divide, subtract.",
            "De Moivre: [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ).",
            "nth roots: r^(1/n) cis((θ + 2kπ)/n), k = 0 … n−1: a regular n-gon; they sum to 0.",
            "1, ω, ω²: ω³ = 1, 1 + ω + ω² = 0. Euler: e^(iθ) = cos θ + i sin θ; e^(iπ) + 1 = 0.",
        ], "Quick recap. Polar form is length and angle, with the angle taken from the plotted quadrant. Multiplying multiplies lengths and adds angles. De Moivre raises both to the n. The n th roots sit on a regular polygon and add to zero. One plus omega plus omega squared is zero. And Euler's formula says e to the i theta is cos theta plus i sin theta.")
        self.outro("That was complex numbers. Next, sequence and series: sums of squares and cubes, and proof by mathematical induction. See you there.")
