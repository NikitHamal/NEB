import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import clock, curve, example, neby_in, neby_out, readout  # noqa: E402

C_E, C_P, C_R = th.AMBER, th.SKY, th.MINT


def U(a):
    return np.array([np.cos(a), np.sin(a), 0])


def polaroid(center, ang, r=1.0, color=th.SKY):
    """End-on Polaroid disc with its transmission axis at angle ang (radians from vertical)."""
    c = np.array(center, dtype=float)
    disc = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.12).move_to(c)
    lines = VGroup()
    d = U(PI / 2 + ang)
    n = U(ang)
    for k in np.linspace(-0.8, 0.8, 7):
        half = np.sqrt(max(0, 1 - k * k)) * r
        p = c + n * k * r
        lines.add(Line(p - d * half, p + d * half, color=color, stroke_width=2, stroke_opacity=0.7))
    axis = DoubleArrow(c - d * (r + 0.25), c + d * (r + 0.25), buff=0, color=color, stroke_width=3, tip_length=0.15)
    return VGroup(disc, lines, axis)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 13
    TITLE = "Polarization"
    SUBTITLE = "Proof that light is a transverse wave"
    SECTIONS = ["Polarized light", "Producing polarized light", "Brewster's law", "Transverse nature of light",
                "Polaroids and Malus's law", "Uses of polarization"]
    NEXT = "Unit 14 · Electrical Circuits"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        lake = Rectangle(width=13.6, height=3.4, stroke_width=0, fill_color="#1E5A8A", fill_opacity=0.75).move_to([0, -1.9, 0])
        hills = VMobject(fill_color="#2f5a2a", fill_opacity=1, stroke_width=0).set_points_as_corners([[-6.8, -0.2, 0], [-4.5, 1.6, 0], [-2.0, 0.4, 0], [0.6, 2.2, 0], [3.4, 0.6, 0], [6.8, 1.8, 0], [6.8, -0.2, 0], [-6.8, -0.2, 0]])
        sun = Circle(radius=0.45, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to([4.6, 2.6, 0])
        ang = ValueTracker(PI / 2)
        glare = always_redraw(lambda: VGroup(*[Ellipse(width=w, height=0.18, fill_color=WHITE, stroke_width=0, fill_opacity=0.15 + 0.8 * np.sin(ang.get_value()) ** 2).move_to([x, y, 0])
                                               for x, y, w in ((2.0, -1.0, 2.6), (3.4, -1.6, 1.8), (1.0, -2.0, 2.2), (2.8, -2.6, 1.4))]))
        lens = always_redraw(lambda: polaroid([-3.6, -1.6, 0], ang.get_value(), r=1.0, color=th.SKY))
        tag = T("Phewa Lake, midday", size=24, color=th.MUTED).to_edge(UP, buff=0.6)
        with self.say("Midday on Phewa Lake. The sunlight bouncing off the water is a blinding glare."):
            self.play(FadeIn(lake), FadeIn(hills), FadeIn(sun), FadeIn(tag))
            self.add(glare)
            self.play(FadeIn(glare))
        with self.say("Now look through one lens of a pair of polarizing sunglasses, and slowly turn it."):
            self.add(lens)
            self.play(FadeIn(lens))
            self.play(ang.animate.set_value(PI / 4), run_time=3)
        with self.say("At one angle the glare simply vanishes. Turn it a quarter turn further, and the glare is back at full strength. A plain piece of tinted plastic, and it can tell one direction of light from another."):
            self.play(ang.animate.set_value(0), run_time=2)
            self.play(ang.animate.set_value(-PI / 2), run_time=3)
            self.play(ang.animate.set_value(0), run_time=2)
        nb = neby_in(self, "surprised", corner=DL)
        q = T("How can light have a direction across its path?", size=32, color=th.AMBER, weight="BOLD").move_to([0, 2.9, 0])
        with self.say("How can a beam of light have a sideways direction that a filter can pick out? The answer proves something deep: light is a transverse wave."):
            self.play(FadeOut(tag), FadeIn(q))
        self.play(FadeOut(VGroup(lake, hills, sun, q)), FadeOut(glare), FadeOut(lens))
        self.remove(glare, lens)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 13: Polarization. Interference and diffraction showed us that light is a wave. Polarization tells us what kind of wave. We will see how polarized light is produced, and learn the two laws the exam always asks for: Brewster's law and Malus's law."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. What polarized light is, the ways of producing it, Brewster's law, the proof that light is transverse, Polaroids and Malus's law, and the uses of polarization all around you.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        rng = np.random.default_rng(3)
        t = ValueTracker(0)
        C1 = np.array([-3.4, 0.2, 0])
        C2 = np.array([3.4, 0.2, 0])
        angs = rng.uniform(0, PI, 400)

        def unpol():
            k = int(t.get_value() * 12) % 400
            g = VGroup(Circle(radius=1.6, stroke_color=th.FAINT, stroke_width=2).move_to(C1))
            for j in range(6):
                a = angs[(k + j * 37) % 400]
                g.add(DoubleArrow(C1 - 1.4 * U(a), C1 + 1.4 * U(a), buff=0, color=C_E, stroke_width=3, tip_length=0.15, stroke_opacity=1 - j * 0.13))
            return g
        un = always_redraw(unpol)
        pol = always_redraw(lambda: VGroup(Circle(radius=1.6, stroke_color=th.FAINT, stroke_width=2).move_to(C2),
                                           DoubleArrow(C2 + DOWN * 1.4 * abs(np.sin(6 * t.get_value())) - DOWN * 0.001, C2 + UP * 1.4 * abs(np.sin(6 * t.get_value())) + UP * 0.001, buff=0, color=C_E, stroke_width=4, tip_length=0.15)))
        labs = VGroup(T("unpolarized", size=28, color=th.INK, weight="BOLD").next_to(C1 + DOWN * 1.6, DOWN, buff=0.3), T("plane polarized", size=28, color=th.INK, weight="BOLD").next_to(C2 + DOWN * 1.6, DOWN, buff=0.3))
        sub = T("looking along the beam, towards the source", size=22, color=th.MUTED).to_edge(UP, buff=0.8)
        with self.say("Look at a beam of light end on, as if it were coming straight at you. The electric field of the wave vibrates across the beam, at right angles to the direction of travel. In light from a lamp or the Sun, that direction changes at random millions of times a second, as one atom after another emits its short wave train. That is unpolarized light."):
            self.play(FadeIn(sub))
            self.add(un)
            self.play(FadeIn(un), FadeIn(labs[0]))
            self.play(t.animate.set_value(8), run_time=8, rate_func=linear)
        with self.say("If the vibrations are confined to just one plane, the light is plane polarized, or linearly polarized. Polarization is the process of confining the vibrations of the electric vector to a single plane."):
            self.add(pol)
            self.play(FadeIn(pol), FadeIn(labs[1]))
            self.play(t.animate.set_value(13), run_time=5, rate_func=linear)
        self.play(FadeOut(VGroup(sub, labs)), FadeOut(un), FadeOut(pol))
        self.remove(un, pol)
        title = T("Two planes, always at 90°", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        o = np.array([-3.4, -0.4, 0])
        sk = np.array([0.9, 0.45, 0])
        vib = Polygon(o + LEFT * 2.6 + UP * 1.4, o + RIGHT * 2.6 + UP * 1.4, o + RIGHT * 2.6 + DOWN * 1.4, o + LEFT * 2.6 + DOWN * 1.4, stroke_color=C_E, stroke_width=2, fill_color=C_E, fill_opacity=0.12)
        polp = Polygon(o + LEFT * 2.6 - sk, o + RIGHT * 2.6 - sk, o + RIGHT * 2.6 + sk, o + LEFT * 2.6 + sk, stroke_color=C_P, stroke_width=2, fill_color=C_P, fill_opacity=0.12)
        ray = Arrow(o + LEFT * 2.8, o + RIGHT * 3.0, buff=0, color=WHITE, stroke_width=4)
        wav = curve(lambda x: o[1] + 1.1 * np.sin(2.4 * (x - o[0])), o[0] - 2.5, o[0] + 2.5, color=C_E, width=4)
        tl = VGroup(T("plane of vibration", size=22, color=C_E).next_to(vib, UP, buff=0.1), T("plane of polarization", size=22, color=C_P).next_to(polp, DOWN, buff=0.5))
        defs = VGroup(para("Plane of vibration: contains the direction of vibration and the direction of travel.", width=5.6, size=24, color=C_E),
                      para("Plane of polarization: through the direction of travel, perpendicular to the plane of vibration. No vibration happens in it.", width=5.6, size=24, color=C_P)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.5, 0.0, 0])
        with self.say("Two planes get named, and students mix them up every year. The plane of vibration contains the direction of the vibrations and the direction of travel."):
            self.play(FadeIn(title), FadeIn(vib), GrowArrow(ray), Create(wav), FadeIn(tl[0]))
            self.play(FadeIn(defs[0]))
        with self.say("The plane of polarization also contains the direction of travel, but it is perpendicular to the plane of vibration. No vibration happens in it at all. The two planes are always at ninety degrees."):
            self.play(FadeIn(polp), FadeIn(tl[1]))
            self.play(FadeIn(defs[1]))
        self.play(FadeOut(VGroup(title, vib, polp, ray, wav, tl, defs)))
        title = T("Drawing it side-on", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        rows = VGroup()
        for k, (nm, kinds) in enumerate([("unpolarized", "ad"), ("vibrations in the page", "a"), ("vibrations out of the page", "d")]):
            y = 1.4 - k * 1.5
            ray = Arrow([-2.0, y, 0], [5.6, y, 0], buff=0, color=WHITE, stroke_width=3)
            marks = VGroup()
            for i, x in enumerate(np.linspace(-1.4, 4.6, 7)):
                kind = kinds[i % len(kinds)]
                if kind == "a":
                    marks.add(DoubleArrow([x, y - 0.4, 0], [x, y + 0.4, 0], buff=0, color=C_E, stroke_width=3, tip_length=0.12))
                else:
                    marks.add(Dot([x, y, 0], radius=0.09, color=C_P))
            rows.add(VGroup(T(nm, size=24, color=th.BODY).move_to([-4.3, y, 0]), ray, marks))
        with self.say("In side views, vibrations in the plane of the page are drawn as short double headed arrows, and vibrations straight out of the page as dots. Unpolarized light gets both. Plane polarized light gets only one kind.") as v_:
            self.play(FadeIn(title))
            for r in rows:
                self.play(FadeIn(r[0]), GrowArrow(r[1]), LaggedStart(*[FadeIn(m) for m in r[2]], lag_ratio=0.1), run_time=1.0)
                self.hold(v_.dur / 3 - 1.0)
        self.play(FadeOut(VGroup(title, rows)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Five ways to polarize light", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        items = [("Reflection", "at one special angle the reflected light is fully polarized: glare off a wet road or a lake", th.AMBER),
                 ("Refraction", "a pile of glass plates polarizes the transmitted beam more with every plate", th.SKY),
                 ("Selective absorption", "a Polaroid absorbs one vibration direction and passes the other", th.MINT),
                 ("Double refraction", "a calcite crystal splits a beam into two oppositely polarized rays: the Nicol prism", th.PINK),
                 ("Scattering", "sky light at 90° to the Sun, scattered by air molecules, is polarized", th.LIME)]
        cards = VGroup()
        for h, b, c in items:
            box = self.panel(3.9, 2.3)
            g = VGroup(T(h, size=26, color=c, weight="BOLD"), para(b, width=3.4, size=19, color=th.BODY)).arrange(DOWN, buff=0.15).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).next_to(title, DOWN, buff=0.35)
        with self.say("Polarized light can be made in five ways. By reflection: the glare from a wet road or a lake is largely polarized. By refraction, through a pile of glass plates. By selective absorption, in a Polaroid sheet. By double refraction, in a calcite crystal. And by scattering: look at the blue sky at right angles to the Sun through a Polaroid, and turn it.") as v_:
            self.play(FadeIn(title))
            for c_ in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
                self.hold(v_.dur / 5 - 0.6)
        self.play(FadeOut(VGroup(title, cards)))
        rh = Polygon([-2.4, -1.6, 0], [1.0, -1.6, 0], [2.4, 1.4, 0], [-1.0, 1.4, 0], stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.12)
        lab = T("calcite (Iceland spar)", size=22, color=th.SKY).next_to(rh, DOWN, buff=0.15)
        inc = Line([-6.4, -0.1, 0], [-1.7, -0.1, 0], color=WHITE, stroke_width=4)
        o_r = Line([-1.7, -0.1, 0], [1.75, -0.1, 0], color=th.AMBER, stroke_width=4)
        e_r = Line([-1.7, -0.1, 0], [1.75, 0.6, 0], color=th.PINK, stroke_width=4)
        o_out = Line([1.75, -0.1, 0], [6.4, -0.1, 0], color=th.AMBER, stroke_width=4)
        e_out = Line([1.75, 0.6, 0], [6.4, 0.6, 0], color=th.PINK, stroke_width=4)
        inc_m = VGroup(*[VGroup(DoubleArrow([x, -0.45, 0], [x, 0.25, 0], buff=0, color=th.BODY, stroke_width=2, tip_length=0.1), Dot([x + 0.3, -0.1, 0], radius=0.07, color=th.BODY)) for x in (-5.6, -4.4, -3.2)])
        o_m = VGroup(*[Dot([x, -0.1, 0], radius=0.08, color=th.AMBER) for x in (3.0, 4.2, 5.4)])
        e_m = VGroup(*[DoubleArrow([x, 0.3, 0], [x, 0.9, 0], buff=0, color=th.PINK, stroke_width=3, tip_length=0.1) for x in (3.0, 4.2, 5.4)])
        ol = VGroup(T("ordinary ray (obeys Snell)", size=22, color=th.AMBER).move_to([4.2, -0.65, 0]), T("extraordinary ray (does not)", size=22, color=th.PINK).move_to([4.2, 1.25, 0]))
        with self.say("Double refraction is the strangest. Send unpolarized light into a calcite crystal, and it splits into two refracted rays. The ordinary ray obeys Snell's law. The extraordinary ray does not."):
            self.play(FadeIn(rh), FadeIn(lab), Create(inc), FadeIn(inc_m))
            self.play(Create(o_r), Create(e_r))
            self.play(Create(o_out), Create(e_out), FadeIn(ol))
        nic = para("The two rays are plane polarized at right angles. A Nicol prism is calcite cut and cemented with Canada balsam so that the ordinary ray is totally reflected away, leaving one polarized beam.", width=11, size=24, color=th.BODY).to_edge(DOWN, buff=0.45)
        with self.say("And the two rays are plane polarized, in planes at right angles to each other: one shown with dots, one with arrows. A Nicol prism is a calcite crystal cut in two and cemented with Canada balsam, so that the ordinary ray is totally internally reflected away. Only the polarized extraordinary ray comes out."):
            self.play(FadeIn(o_m), FadeIn(e_m))
            self.play(FadeIn(nic))
        self.play(FadeOut(VGroup(rh, lab, inc, o_r, e_r, o_out, e_out, inc_m, o_m, e_m, ol, nic)))
        eq = M(r"P = \frac{I_{\max} - I_{\min}}{I_{\max} + I_{\min}}", size=56).move_to([-2.6, 1.0, 0])
        notes = VGroup(T("P = 1: fully plane polarized", size=26, color=C_R), T("P = 0: unpolarized", size=26, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eq, DOWN, buff=0.5)
        a = ValueTracker(0)
        Imax, Imin = 1.0, 0.25
        an = always_redraw(lambda: polaroid([3.6, 0.4, 0], a.get_value(), r=1.2, color=th.SKY))
        bar_bg = Rectangle(width=0.5, height=2.4, stroke_color=th.FAINT).move_to([5.8, 0.4, 0])
        bar = always_redraw(lambda: Rectangle(width=0.5, height=max(0.02, 2.4 * (Imin + (Imax - Imin) * np.cos(a.get_value()) ** 2)), stroke_width=0, fill_color=C_E, fill_opacity=0.9).align_to(bar_bg, DOWN).set_x(5.8))
        ro = readout("P =", lambda: (Imax - Imin) / (Imax + Imin), "", decimals=2, size=30, color=C_E).move_to([3.6, -1.8, 0])
        with self.say("Most of these methods give a mixture: partially polarized light. To measure how polarized it is, look through an analyser and rotate it a full turn. The brightness swings between a maximum and a minimum. The degree of polarization is I max minus I min, over I max plus I min. It is one for fully polarized light, and zero for unpolarized light."):
            self.add(an, bar)
            self.play(FadeIn(an), FadeIn(bar_bg), FadeIn(bar), Write(eq))
            self.play(a.animate.set_value(PI), run_time=4)
            self.play(FadeIn(notes), FadeIn(ro))
        self.play(FadeOut(VGroup(eq, notes, bar_bg, ro)), FadeOut(an), FadeOut(bar))
        self.remove(an, bar)

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        n = 1.5
        O = np.array([-1.2, -0.6, 0])
        th_i = ValueTracker(np.radians(30))
        glass = Rectangle(width=9, height=2.6, stroke_width=0, fill_color="#22406e", fill_opacity=0.85).move_to([-2.2, -1.9, 0])
        surf = Line([-6.7, -0.6, 0], [2.3, -0.6, 0], color=th.BODY, stroke_width=3)
        normal = DashedLine(O + UP * 2.8, O + DOWN * 2.2, color=th.FAINT)

        def rays():
            i = th_i.get_value()
            r = np.arcsin(np.sin(i) / n)
            din = np.array([np.sin(i), -np.cos(i), 0])
            S = O - din * 3.6
            R = O + np.array([np.sin(i), np.cos(i), 0]) * 3.6
            Tt = O + np.array([np.sin(r), -np.cos(r), 0]) * 2.2
            par = abs(np.cos(i + r))
            g = VGroup(Line(S, O, color=WHITE, stroke_width=4), Line(O, R, color=th.AMBER, stroke_width=4), Line(O, Tt, color=th.SKY, stroke_width=4))
            for f in (0.35, 0.65):
                p = S + (O - S) * f
                perp = np.array([din[1], -din[0], 0])
                g.add(DoubleArrow(p - perp * 0.28, p + perp * 0.28, buff=0, color=WHITE, stroke_width=2, tip_length=0.08), Dot(p + din * 0.32, radius=0.06, color=WHITE))
                q = O + (R - O) * f
                dr = (R - O) / np.linalg.norm(R - O)
                pr = np.array([dr[1], -dr[0], 0])
                g.add(Dot(q + dr * 0.32, radius=0.07, color=th.AMBER))
                if par > 0.04:
                    g.add(DoubleArrow(q - pr * 0.3 * par, q + pr * 0.3 * par, buff=0, color=th.AMBER, stroke_width=2, tip_length=0.08 * min(1, par * 3)))
            return g
        rg = always_redraw(rays)
        ro = VGroup(readout("angle of incidence:", lambda: np.degrees(th_i.get_value()), "°", decimals=1, size=24),
                    readout("angle between reflected and refracted:", lambda: 180 - np.degrees(th_i.get_value()) - np.degrees(np.arcsin(np.sin(th_i.get_value()) / n)), "°", decimals=1, size=24, color=C_R)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.8, 2.6, 0])
        with self.say("When unpolarized light strikes glass or water, both the reflected and the refracted beams come out partly polarized. Watch the reflected beam. Its arrow component, vibrating in the plane of incidence, shrinks as we change the angle."):
            self.play(FadeIn(glass), Create(surf), Create(normal))
            self.add(rg)
            self.play(FadeIn(rg), FadeIn(ro))
            self.play(th_i.animate.set_value(np.radians(48)), run_time=3)
        with self.say("In eighteen eleven, David Brewster found that at one particular angle, the reflected beam is completely plane polarized: only dots are left, vibrating perpendicular to the plane of incidence. For glass, that happens at about fifty six degrees. And look at the readout: at that angle, the reflected and refracted rays are exactly at right angles."):
            self.play(th_i.animate.set_value(np.arctan(n)), run_time=3)
            self.wait(1.5)
        self.play(FadeOut(ro))
        self.play(VGroup(glass, surf, normal).animate.shift(LEFT * 1.6), rg.animate.shift(LEFT * 1.6))
        self.remove(rg)
        O2 = O + LEFT * 1.6
        i = np.arctan(n)
        r = np.arcsin(np.sin(i) / n)
        S = O2 - np.array([np.sin(i), -np.cos(i), 0]) * 3.6
        R = O2 + np.array([np.sin(i), np.cos(i), 0]) * 3.6
        Tt = O2 + np.array([np.sin(r), -np.cos(r), 0]) * 2.2
        fixed = VGroup(Line(S, O2, color=WHITE, stroke_width=4), Line(O2, R, color=th.AMBER, stroke_width=4), Line(O2, Tt, color=th.SKY, stroke_width=4))
        ra = RightAngle(Line(O2, R), Line(O2, Tt), length=0.35, color=C_R)
        angs = VGroup(Arc(radius=0.8, start_angle=PI / 2, angle=i, arc_center=O2, color=WHITE), M(r"\theta_p", size=30).move_to(O2 + 1.15 * U(PI / 2 + i / 2)),
                      Arc(radius=0.8, start_angle=-PI / 2, angle=r, arc_center=O2, color=th.SKY), M("r", size=30, color=th.SKY).move_to(O2 + 1.1 * U(-PI / 2 + r / 2)))
        self.add(fixed)
        L = VGroup(M(r"\theta_p + 90^{\circ} + r = 180^{\circ}\ \Rightarrow\ r = 90^{\circ} - \theta_p", size=34),
                   M(r"n = \frac{\sin\theta_p}{\sin r} = \frac{\sin\theta_p}{\sin(90^{\circ} - \theta_p)} = \frac{\sin\theta_p}{\cos\theta_p}", size=34),
                   M(r"n = \tan\theta_p", size=60, color=C_E)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.8, 0.6, 0])
        if L.width > 6.0:
            L.scale_to_fit_width(6.0).move_to([3.8, 0.6, 0])
        with self.say("Now the proof. At the polarizing angle, the reflected and refracted rays are at ninety degrees. On the top of the surface, the angles round O make a straight line: theta p, plus ninety, plus r, is one eighty. So r is ninety minus theta p."):
            self.play(Create(ra), FadeIn(angs))
            self.play(Write(L[0]))
        with self.say("Snell's law says n is sine theta p over sine r. But sine of ninety minus theta p is cos theta p."):
            self.play(Write(L[1]))
        with self.say("So n equals tan theta p. That is Brewster's law: the tangent of the polarizing angle equals the refractive index."):
            self.sfx("impact", gain=-12)
            self.play(Write(L[2]))
            self.play(Circumscribe(L[2], color=C_E))
        self.play(FadeOut(VGroup(glass, surf, normal, fixed, ra, angs, L)))
        why = para("Why? The refracted wave makes the electrons in the glass vibrate across the refracted ray. A vibrating charge sends out nothing along its own line of vibration. At θp the reflected direction lies exactly along that line for the in-plane component, so only the perpendicular component can be reflected.", width=11.5, size=26, color=th.BODY)
        with self.say("There is a neat physical reason. The refracted wave sets the electrons in the glass vibrating, across the refracted ray. A vibrating charge radiates nothing along its own line of vibration. At Brewster's angle, the reflected direction lies exactly along that line for the vibrations in the plane of incidence. So that component cannot be reflected, and only the perpendicular one survives."):
            self.play(FadeIn(why))
        self.play(FadeOut(why))
        cau = self.callout("careful", "Brewster's angle θp = tan⁻¹ n: rarer to denser, the reflected light is polarized. Critical angle C = sin⁻¹(1/n): denser to rarer, total internal reflection. For n = 1.5: θp = 56.3°, C = 41.8°.", width=11, size=26)
        with self.say("Do not confuse Brewster's angle with the critical angle. Brewster's angle, tan inverse n, is for light going from a rarer to a denser medium, and it is about polarization. The critical angle, sine inverse one over n, is for denser to rarer, and it is about total internal reflection. For n equal to one point five, they are fifty six point three and forty one point eight degrees: quite different."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        example(self, "Find the polarizing angle for glass of refractive index 1.5, and the corresponding angle of refraction. Verify that the reflected and refracted rays are perpendicular.",
                [r"\tan\theta_p = 1.5\ \Rightarrow\ \theta_p = 56.3^{\circ}",
                 r"r = 90^{\circ} - 56.3^{\circ} = 33.7^{\circ}",
                 r"\frac{\sin 56.3^{\circ}}{\sin 33.7^{\circ}} = \frac{0.832}{0.555} = 1.50\ \checkmark,\quad 180^{\circ} - 56.3^{\circ} - 33.7^{\circ} = 90^{\circ}"],
                ["Worked example. Find the polarizing angle for glass of index one point five, and the angle of refraction. Check that the rays are perpendicular.",
                 "Tan theta p is one point five, so theta p is fifty six point three degrees.",
                 "The angle of refraction is ninety minus that: thirty three point seven degrees.",
                 "Check with Snell: sine fifty six point three over sine thirty three point seven is zero point eight three two over zero point five five five, one point five zero. And the angle between the two rays is one eighty minus both, exactly ninety degrees."], size=38)
        example(self, "The polarizing angle of a medium is 60°. Find its refractive index, the speed of light in it, and its critical angle (c = 3 × 10⁸ m/s).",
                [r"n = \tan 60^{\circ} = \sqrt{3} = 1.732",
                 r"v = \frac{c}{n} = \frac{3\times10^{8}}{1.732} = 1.73\times10^{8}\ \text{m s}^{-1}",
                 r"\sin C = \frac{1}{1.732} = 0.5774\ \Rightarrow\ C = 35.3^{\circ}"],
                ["Another one, mixing ideas. A medium has a polarizing angle of sixty degrees. Find its index, the speed of light in it, and its critical angle.",
                 "n is tan sixty, root three, one point seven three two.",
                 "The speed is c over n: one point seven three times ten to the eight metres per second.",
                 "The critical angle has sine one over n, zero point five seven seven four, so C is thirty five point three degrees. Different from the Brewster angle, as we said."], size=40)
        self.quiz("At the polarizing angle, the angle between the reflected and the refracted ray is",
                  ["0°", "45°", "90°", "180°"], 2,
                  "Pause and think. At the polarizing angle, what is the angle between the reflected and refracted rays?",
                  "C, ninety degrees. That right angle is exactly what turns Snell's law into Brewster's law, n equals tan theta p.")

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        a = ValueTracker(0.0)
        P = polaroid([-3.6, 0.6, 0], 0.0, r=1.3, color=th.SKY)
        A = always_redraw(lambda: polaroid([0.6, 0.6, 0], a.get_value(), r=1.3, color=th.PINK))
        lp = VGroup(T("polarizer P", size=24, color=th.SKY).next_to(P, DOWN, buff=0.25), T("analyser A", size=24, color=th.PINK).move_to([0.6, -1.25, 0]))
        bar_bg = Rectangle(width=0.6, height=3.0, stroke_color=th.FAINT).move_to([4.2, 0.6, 0])
        bar = always_redraw(lambda: Rectangle(width=0.6, height=max(0.02, 3.0 * np.cos(a.get_value()) ** 2), stroke_width=0, fill_color=C_E, fill_opacity=0.9).align_to(bar_bg, DOWN).set_x(4.2))
        bl = T("light through", size=22, color=C_E).next_to(bar_bg, DOWN, buff=0.15)
        ra = readout("angle =", lambda: np.degrees(a.get_value()), "°", decimals=0, size=26).move_to([0.6, 2.6, 0])
        with self.say("Here is the experiment that proves light is a transverse wave. Send ordinary light through one Polaroid sheet, P. What comes out looks just a little dimmer. Now put a second sheet, A, behind it, and rotate it about the beam."):
            self.play(FadeIn(P), FadeIn(lp))
            self.add(A, bar)
            self.play(FadeIn(A), FadeIn(bar_bg), FadeIn(bar), FadeIn(bl), FadeIn(ra))
        with self.say("The light coming through rises and falls. Twice in every full turn, when the two sheets are crossed, it drops to zero."):
            self.play(a.animate.set_value(TAU), run_time=7, rate_func=linear)
        self.play(FadeOut(VGroup(P, lp, bar_bg, bl, ra)), FadeOut(A), FadeOut(bar))
        self.remove(A, bar)
        t = clock(self, 1.0)
        y1, y2 = 1.4, -1.4
        sl = ValueTracker(0)
        tw = always_redraw(lambda: curve(lambda x: y1 + (0.6 * np.sin(3 * x - 5 * t.get_value()) if x < 0 or np.cos(sl.get_value()) > 0.5 else 0.6 * np.sin(3 * x - 5 * t.get_value()) * max(0, np.cos(sl.get_value()))), -6.0, 5.0, color=C_E, width=4))
        slot = always_redraw(lambda: VGroup(Rectangle(width=0.3, height=1.8, stroke_color=th.BODY, stroke_width=3).move_to([0, y1, 0]).stretch(max(0.12, abs(np.cos(sl.get_value()))), 1)))
        xs = np.linspace(-6.0, 5.0, 40)
        lw = VGroup(*[Line([x, y2 - 0.4, 0], [x, y2 + 0.4, 0], color=th.MINT, stroke_width=2.5) for x in xs])
        lw.add_updater(lambda m: [ln.set_x(x + 0.12 * np.sin(3 * x - 5 * t.get_value())) for ln, x in zip(m, xs)])
        slot2 = always_redraw(lambda: Rectangle(width=0.3, height=1.4, stroke_color=th.BODY, stroke_width=3).move_to([0, y2, 0]).stretch(max(0.12, abs(np.cos(sl.get_value()))), 1))
        labs = VGroup(T("transverse (rope through a slot)", size=22, color=C_E).move_to([-3.5, y1 + 1.0, 0]), T("longitudinal (sound, a pushed spring)", size=22, color=th.MINT).move_to([-3.5, y2 + 0.9, 0]))
        with self.say("Why does that prove anything? Think of a rope wave passing through a slot. If the rope shakes along the slot, the wave goes through. Turn the slot across, and the wave is blocked. A longitudinal wave, like sound, vibrates along its direction of travel, so turning the slot makes no difference at all."):
            self.add(tw, slot, lw, slot2)
            self.play(FadeIn(tw), FadeIn(slot), FadeIn(lw), FadeIn(slot2), FadeIn(labs))
            self.play(sl.animate.set_value(PI / 2), run_time=3)
            self.wait(1)
        concl = para("Rotating the analyser can cut light off completely, so light's vibrations must lie ACROSS the beam: light is a transverse wave. Sound cannot be polarized.", width=11, size=26, color=th.AMBER).to_edge(DOWN, buff=0.35)
        with self.say("Light behaves like the rope, never like the spring. The fact that turning the analyser can cut the light off completely means its vibrations lie across the beam. Polarization is the one optical effect that proves light is a transverse wave. Sound, being longitudinal, can never be polarized."):
            self.play(FadeOut(labs), FadeIn(concl))
            self.wait(1)
        self.play(FadeOut(concl), FadeOut(tw), FadeOut(slot), FadeOut(lw), FadeOut(slot2))
        lw.clear_updaters()
        self.remove(tw, slot, lw, slot2, t)
        self.quiz("Polarization of light establishes that light waves are",
                  ["longitudinal", "transverse", "stationary", "mechanical"], 1,
                  "Pause and think. What does polarization tell us about light waves?",
                  "B, transverse. Interference and diffraction only show that light is a wave. Polarization shows which kind: one with a vibration direction across the beam that a filter can select.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        title = T("The Polaroid", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        chains = VGroup(*[Line([-5.6, y, 0], [-1.6, y, 0], color=th.MUTED, stroke_width=5) for y in np.linspace(-1.6, 1.6, 9)])
        Ev = DoubleArrow([-3.6, -1.1, 0], [-3.6, 1.1, 0], buff=0, color=C_E, stroke_width=5, tip_length=0.18)
        Eh = DoubleArrow([-4.8, 0, 0], [-2.4, 0, 0], buff=0, color=th.CORAL, stroke_width=5, tip_length=0.18)
        txt = VGroup(para("1928: Edwin Land, tiny aligned needle crystals of herapathite in a plastic film.", width=5.6, size=22, color=th.BODY),
                     para("Today: a polyvinyl alcohol sheet, stretched so its long molecules line up, then soaked in iodine.", width=5.6, size=22, color=th.BODY),
                     para("The chains conduct along their length: they absorb the field component along them and pass the one across them: the transmission axis.", width=5.6, size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.0, 0])
        with self.say("A Polaroid is a thin sheet that passes light vibrating in one direction only. Edwin Land made the first in nineteen twenty eight, from tiny aligned needle crystals of herapathite. Modern sheets are polyvinyl alcohol, stretched so that its long molecules all lie parallel, then soaked in iodine."):
            self.play(FadeIn(title), LaggedStart(*[Create(c) for c in chains], lag_ratio=0.08))
            self.play(FadeIn(txt[0]), FadeIn(txt[1]))
        with self.say("The iodine soaked chains conduct electricity along their length. So they soak up the part of the electric field that vibrates along them, and let through the part vibrating across them. That direction is the transmission axis. Two sheets are used together: the first is the polarizer, the second the analyser."):
            self.play(GrowFromCenter(Eh))
            self.play(Eh.animate.set_opacity(0.15), GrowFromCenter(Ev))
            self.play(FadeIn(txt[2]))
        self.play(FadeOut(VGroup(title, chains, Ev, Eh, txt)))
        th_ = ValueTracker(0.5)
        O = np.array([-3.4, 0.0, 0])
        Aamp = 2.2

        def vec():
            a = th_.get_value()
            ax_d = U(PI / 2 - a)
            g = VGroup(DashedLine(O - ax_d * 2.8, O + ax_d * 2.8, color=th.PINK, stroke_width=3),
                       Arrow(O, O + UP * Aamp, buff=0, color=WHITE, stroke_width=6))
            comp = Aamp * np.cos(a)
            g.add(Arrow(O, O + ax_d * comp, buff=0, color=C_E, stroke_width=6) if comp > 0.15 else VGroup())
            perp = U(-a) * Aamp * np.sin(a)
            g.add(DashedLine(O + ax_d * comp, O + UP * Aamp, color=th.CORAL, stroke_width=3) if np.sin(a) > 0.05 else VGroup())
            return g
        vv = always_redraw(vec)
        labs = always_redraw(lambda: VGroup(M("A", size=32).next_to(O + UP * Aamp, UP, buff=0.1),
                                            M(r"A\cos\theta", size=30, color=C_E).next_to(O + U(PI / 2 - th_.get_value()) * Aamp * np.cos(th_.get_value()), RIGHT, buff=0.15)))
        axl = T("analyser axis", size=22, color=th.PINK).move_to([-1.2, -2.6, 0])
        L = VGroup(M(r"\text{along the axis: } A\cos\theta\ \text{(passes)}", size=34, color=C_E), M(r"\text{across it: } A\sin\theta\ \text{(absorbed)}", size=34, color=th.CORAL),
                   M(r"I = k(A\cos\theta)^{2}", size=40), M(r"I = I_0\cos^{2}\theta", size=60, color=C_E)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.4, 0])
        with self.say("Now Malus's law. Plane polarized light of amplitude A meets an analyser whose axis is at an angle theta to the vibrations. Split A into two parts. A cos theta, along the axis, gets through. A sine theta, across the axis, is absorbed."):
            self.add(vv, labs)
            self.play(FadeIn(vv), FadeIn(labs), FadeIn(axl))
            self.play(Write(L[0]), Write(L[1]))
            self.play(th_.animate.set_value(1.1), run_time=2)
        with self.say("Intensity goes as amplitude squared. So the transmitted intensity is k, A cos theta, squared, which is I nought cos squared theta. That is Malus's law. Parallel axes let all of it through. Crossed axes, at ninety degrees, let nothing through."):
            self.play(Write(L[2]))
            self.sfx("impact", gain=-12)
            self.play(Write(L[3]))
            self.play(th_.animate.set_value(PI / 2 - 0.02), run_time=2)
            self.play(th_.animate.set_value(0.02), run_time=2)
        self.play(FadeOut(VGroup(axl, L)), FadeOut(vv), FadeOut(labs))
        self.remove(vv, labs)
        cau = self.callout("careful", "Malus's law is for light that is ALREADY polarized. Unpolarized light through the first Polaroid: the average of cos²θ over all directions is ½, so I = I₀/2 whatever its orientation.", width=11, size=26)
        with self.say("A trap that costs marks. Malus's law only applies to light that is already polarized. When unpolarized light meets the first Polaroid, its vibrations point in every direction at random, and the average of cos squared over all directions is a half. So the first sheet always lets through exactly half, whichever way it is turned. Only after that does cos squared theta apply."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        self.three_polaroids()
        example(self, "Unpolarized light of intensity I₀ falls on a polarizer. An analyser behind it has its axis at 60° to the polarizer's. Find the emergent intensity.",
                [r"I_1 = \frac{I_0}{2}",
                 r"I_2 = I_1\cos^{2}60^{\circ} = \frac{I_0}{2}\left(\frac12\right)^{2} = \frac{I_0}{8} = 0.125\,I_0"],
                ["Worked example. Unpolarized light of intensity I nought, a polarizer, then an analyser at sixty degrees. What comes out?",
                 "After the polarizer, half: I nought over two.",
                 "Then Malus: times cos squared sixty, a quarter. I nought over eight, twelve and a half percent."], size=44)
        example(self, "Three Polaroids: the first and third are crossed, the middle one is at θ to the first. Show that the emergent intensity is (I₀/8) sin² 2θ, and find θ for the maximum. Evaluate for θ = 30°.",
                [r"I_1 = \frac{I_0}{2},\quad I_2 = \frac{I_0}{2}\cos^{2}\theta",
                 r"I_3 = \frac{I_0}{2}\cos^{2}\theta\cos^{2}(90^{\circ} - \theta) = \frac{I_0}{2}\cos^{2}\theta\sin^{2}\theta",
                 r"= \frac{I_0}{8}(2\sin\theta\cos\theta)^{2} = \frac{I_0}{8}\sin^{2}2\theta\quad(\max\ \tfrac{I_0}{8} \text{ at } \theta = 45^{\circ})",
                 r"\theta = 30^{\circ}:\ \frac{I_0}{8}\sin^{2}60^{\circ} = \frac{I_0}{8}\times 0.75 = \frac{3I_0}{32} = 0.09375\,I_0"],
                ["Now the long question on the three sheets. The first and third are crossed, the middle one at angle theta. Show that I nought over eight sine squared two theta comes out.",
                 "After the first, I nought over two. After the second, times cos squared theta.",
                 "The third is at ninety minus theta to the second, so multiply by cos squared of ninety minus theta, which is sine squared theta.",
                 "Two sine theta cos theta is sine two theta, so the product is I nought over eight, sine squared two theta. It is largest, I nought over eight, when theta is forty five degrees.",
                 "At thirty degrees: sine squared sixty is three quarters, so three I nought over thirty two, about nine percent. Adding a third sheet lets light through two crossed ones."], size=36)
        self.quiz("Unpolarized light of intensity I₀ passes through a single Polaroid. The emergent intensity is",
                  [M("I_0", size=40), M("I_0/2", size=40), M("I_0/4", size=40), M("0", size=40)], 1,
                  "Pause and think. Unpolarized light through one Polaroid. How much gets through?",
                  "B, half. The average of cos squared over all directions is a half. It does not matter how the single sheet is turned. Zero only happens with two crossed sheets.")

    def three_polaroids(self):
        title = T("A surprise with three Polaroids", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        m = ValueTracker(0.0)
        P1 = polaroid([-4.4, 0.4, 0], 0.0, r=1.0, color=th.SKY)
        P3 = polaroid([3.0, 0.4, 0], PI / 2, r=1.0, color=th.SKY)
        self._mid = False
        P2 = always_redraw(lambda: polaroid([-0.7, 0.4, 0], m.get_value(), r=1.0, color=th.PINK) if self._mid else VGroup())
        I3 = lambda: (0.5 * np.cos(m.get_value()) ** 2 * np.sin(m.get_value()) ** 2) if self._mid else 0.0
        bar_bg = Rectangle(width=0.6, height=2.6, stroke_color=th.FAINT).move_to([5.6, 0.4, 0])
        bar = always_redraw(lambda: Rectangle(width=0.6, height=max(0.02, 2.6 * I3() / 0.125), stroke_width=0, fill_color=C_E, fill_opacity=0.9).align_to(bar_bg, DOWN).set_x(5.6))
        ro = readout("out:", lambda: I3(), "× I₀", decimals=3, size=26, color=C_E).next_to(bar_bg, DOWN, buff=0.2)
        lbs = VGroup(T("1st", size=22).next_to(P1, DOWN, buff=0.3), T("3rd (crossed)", size=22).next_to(P3, DOWN, buff=0.3))
        with self.say("Here is a beautiful puzzle. Two crossed Polaroids: nothing gets through. Now slip a third sheet between them, at an angle. Surely a third filter can only block more light?"):
            self.play(FadeIn(title), FadeIn(P1), FadeIn(P3), FadeIn(lbs), FadeIn(bar_bg), FadeIn(ro))
            self.add(P2, bar)
            self.wait(1.5)
        self._mid = True
        with self.say("But light comes through! The middle sheet turns the vibrations part way round, and the last sheet passes some of them. Turn the middle sheet, and the output is biggest at forty five degrees."):
            self.play(m.animate.set_value(PI / 6), run_time=1.5)
            self.play(m.animate.set_value(PI / 4), run_time=1.5)
            self.play(m.animate.set_value(PI / 2), run_time=2)
            self.play(m.animate.set_value(PI / 6), run_time=2)
        self.play(FadeOut(VGroup(title, P1, P3, lbs, bar_bg, ro)), FadeOut(P2), FadeOut(bar))
        self.remove(P2, bar)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Polarization at work", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        items = [("Sunglasses", "glare off water is mostly horizontally polarized; vertical axes block it", th.SKY),
                 ("Photography", "a rotating filter darkens the blue sky and kills reflections", th.AMBER),
                 ("LCD screens", "calculators, watches and phones rotate polarized light between crossed sheets", th.MINT),
                 ("3-D cinema", "each eye gets an image polarized at right angles to the other", th.PINK),
                 ("Stress analysis", "a plastic model between crossed Polaroids shows coloured strain fringes", th.CORAL),
                 ("Light control", "two Polaroids in series give a smooth dimmer", th.LIME)]
        cards = VGroup()
        for h, b, c in items:
            box = self.panel(3.9, 2.2)
            g = VGroup(T(h, size=26, color=c, weight="BOLD"), para(b, width=3.4, size=19, color=th.BODY)).arrange(DOWN, buff=0.15).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).next_to(title, DOWN, buff=0.35)
        with self.say("Polarization is all around you. Polarizing sunglasses: glare from water and roads is mostly horizontally polarized, so the lenses pass only vertical vibrations. Camera filters that darken the sky and remove reflections. The LCD screen of every calculator and phone, which works by twisting polarized light between crossed sheets. 3 D films, where each eye gets light polarized at right angles. Engineers' stress analysis, where a plastic model of a bridge glows with coloured fringes between crossed Polaroids. And simple, smooth light dimmers.") as v_:
            self.play(FadeIn(title))
            for c_ in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        nb = neby_in(self, "cool", corner=DR)
        self.wait(0.3)
        self.play(FadeOut(VGroup(title, cards)))
        neby_out(self, nb)
        self.tip("Unpolarized → first Polaroid: always I₀/2. Then multiply by cos² of the angle between each sheet and the one before it. Crossed pair: zero.",
                 "Here is the recipe for every Polaroid numerical. Unpolarized light through the first sheet: always half. Then, for each further sheet, multiply by cos squared of the angle between it and the sheet just before it. Not the angle to the first sheet. And a crossed pair gives zero.", state="wink")
        example(self, "The polarizing angle of a medium is 58°. Calculate its refractive index and the speed of light in it.",
                [r"n = \tan 58^{\circ} = 1.60",
                 r"v = \frac{c}{n} = \frac{3\times10^{8}}{1.60} = 1.87\times10^{8}\ \text{m s}^{-1}"],
                ["One last quick one. A polarizing angle of fifty eight degrees. Find n and the speed of light.",
                 "n is tan fifty eight, one point six zero.",
                 "And v is c over n: one point eight seven times ten to the eight metres per second."], size=44)
        self.quiz("Two Polaroids are crossed. The intensity of the light coming out is",
                  [M("I_0", size=40), M("I_0/2", size=40), M("I_0/4", size=40), M("0", size=40)], 3,
                  "Last check. Two crossed Polaroids. How much light comes out?",
                  "D, zero. The first passes half, and the second, at ninety degrees, passes cos squared ninety of that, which is nothing. Unless, of course, you slip a third sheet in between.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Unpolarized light vibrates in all directions across the ray; plane polarized light in one plane. The plane of polarization is ⟂ to the plane of vibration.",
            "Produced by reflection, a pile of plates, Polaroid (absorption), double refraction (Nicol) and scattering.",
            M(r"P = \frac{I_{\max} - I_{\min}}{I_{\max} + I_{\min}}", size=36),
            M(r"\text{Brewster: } n = \tan\theta_p,\ \ \theta_p + r = 90^{\circ}\quad(\text{not the critical angle})", size=34),
            M(r"\text{Malus: } I = I_0\cos^{2}\theta;\ \ \text{unpolarized} \to I_0/2;\ \ \text{crossed} \to 0", size=34),
            "Polarization proves light is transverse; sound cannot be polarized.",
        ], "Let us recap. Unpolarized light vibrates in every direction across the beam; plane polarized light in just one plane. It can be produced by reflection, refraction, absorption in a Polaroid, double refraction and scattering. Brewster's law says n equals tan theta p, where the reflected and refracted rays are perpendicular. Malus's law says I equals I nought cos squared theta, after a first sheet that always halves unpolarized light. And because light can be polarized, it must be a transverse wave.")
        self.outro("That completes wave optics. Next, we switch to electricity, and analyse real circuits with Kirchhoff's laws, in Electrical Circuits. See you there, on NEBians.")
