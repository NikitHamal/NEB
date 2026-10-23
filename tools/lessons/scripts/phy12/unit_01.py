from manim import *
import numpy as np

from kit import Lesson, M, T, para, th

C_TH, C_W, C_A, C_I, C_TAU, C_L, C_R = th.AMBER, th.SKY, th.CORAL, th.MINT, th.PINK, th.ACCENT, th.LIME


def wheel(R, kind, color):
    if kind == "ring":
        body = Annulus(inner_radius=R * 0.78, outer_radius=R, fill_color=color, fill_opacity=0.9, stroke_width=0)
        mark = Line(ORIGIN, RIGHT * R * 0.78, color=color, stroke_width=3, stroke_opacity=0.6)
    else:
        body = Circle(radius=R, fill_color=color, fill_opacity=0.85, stroke_color=WHITE, stroke_width=2)
        mark = Line(ORIGIN, RIGHT * R, color=th.BG, stroke_width=5)
    hub = Dot(radius=0.06, color=WHITE)
    return VGroup(body, mark, hub)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 1
    TITLE = "Rotational Dynamics"
    SUBTITLE = "Angle, inertia, torque and spin"
    SECTIONS = ["Angular kinematics", "Rotational kinetic energy", "Moment of inertia",
                "Inertia of a uniform rod", "Torque and τ = Iα", "Work and power", "Angular momentum"]
    NEXT = "Unit 2 · Periodic Motion"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        R = 0.45
        t = ValueTracker(0)
        lanes = []
        ramps = VGroup()
        for k, y0 in enumerate([2.0, -0.9]):
            A = np.array([-6.2, y0, 0])
            B = np.array([5.4, y0 - 2.3, 0])
            u = (B - A) / np.linalg.norm(B - A)
            nrm = np.array([-u[1], u[0], 0])
            slab = Polygon(A, B, B + DOWN * 0.25, A + DOWN * 0.25, stroke_width=0, fill_color=th.PANEL_EDGE, fill_opacity=1)
            fin = DashedLine(B + nrm * 1.3 - u * 0.9, B - u * 0.9, color=th.MINT, stroke_width=3)
            ramps.add(slab, fin)
            lanes.append((A, B, u, nrm))
        Lr = np.linalg.norm(lanes[0][1] - lanes[0][0]) - 0.9 - 0.6
        ad = 2 * Lr / 9.0
        ar = ad * 0.75

        def make(kind, color, acc, lane):
            A, B, u, nrm = lanes[lane]
            def f():
                s = min(Lr + 0.6, 0.5 * acc * t.get_value() ** 2 + 0.6)
                w = wheel(R, kind, color).rotate(-s / R)
                return w.move_to(A + u * s + nrm * (R + 0.02))
            return f

        ring = always_redraw(make("ring", th.AMBER, ar, 0))
        disc = always_redraw(make("disc", th.SKY, ad, 1))
        lab_r = T("Ring", size=26, color=th.AMBER, weight="SEMIBOLD")
        lab_d = T("Disc", size=26, color=th.SKY, weight="SEMIBOLD")
        q = T("Which one reaches the bottom first?", size=36, color=th.INK, weight="BOLD", display=True).to_edge(DOWN, buff=0.5)
        ring_side = wheel(1.0, "ring", th.AMBER).move_to([-2.2, 0.3, 0])
        disc_side = wheel(1.0, "disc", th.SKY).move_to([2.2, 0.3, 0])
        lab_r.next_to(ring_side, DOWN, buff=0.35)
        lab_d.next_to(disc_side, DOWN, buff=0.35)
        same = T("same mass  ·  same radius", size=28, color=th.MUTED).next_to(VGroup(lab_r, lab_d), DOWN, buff=0.5)
        with self.say("Here are two wheels. They have exactly the same mass, and exactly the same radius."):
            self.sfx("pop")
            self.play(FadeIn(ring_side, scale=0.6), FadeIn(lab_r), run_time=0.6)
            self.sfx("pop")
            self.play(FadeIn(disc_side, scale=0.6), FadeIn(lab_d), run_time=0.6)
            self.play(FadeIn(same, shift=UP * 0.2))
        with self.say("The only difference: in the ring, all the mass sits out at the rim. In the disc, the same mass is spread evenly, all the way to the centre."):
            self.play(Indicate(ring_side[0], color=WHITE, scale_factor=1.08), run_time=1.0)
            self.play(Indicate(disc_side[0], color=WHITE, scale_factor=1.08), run_time=1.0)
        self.play(FadeOut(VGroup(ring_side, disc_side, lab_r, lab_d, same)), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r_) for r_ in ramps], lag_ratio=0.2), run_time=1.0)
        self.add(ring, disc)
        tag_r = T("Ring", size=24, color=th.AMBER, weight="SEMIBOLD").move_to(lanes[0][0] + UP * 1.3 + RIGHT * 0.6)
        tag_d = T("Disc", size=24, color=th.SKY, weight="SEMIBOLD").move_to(lanes[1][0] + UP * 1.3 + RIGHT * 0.6)
        self.play(FadeIn(ring), FadeIn(disc), FadeIn(tag_r), FadeIn(tag_d), run_time=0.5)
        with self.say("We release both from rest, at the top of identical slopes. Which one reaches the bottom first? Make a guess before you watch."):
            self.play(FadeIn(q, shift=UP * 0.2))
        ring2 = ring
        self.sfx("whoosh", gain=-10)
        self.play(t.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        self.sfx("thud", gain=-8)
        self.sfx("correct", gain=-12)
        self.play(t.animate.set_value(3.47), Flash(lanes[1][1] - lanes[1][2] * 1.5 + lanes[1][3] * 0.47, color=th.SKY, flash_radius=0.75, line_length=0.35), run_time=0.47, rate_func=linear)
        self.sfx("thud", gain=-10)
        win = T("The disc wins. Every single time.", size=34, color=th.SKY, weight="SEMIBOLD").move_to(q)
        with self.say("The disc wins. Every single time. Not because it is heavier, and not because it is smaller. Same mass, same size. The secret is how the mass is arranged around the axis of spin. By the end of this lesson, you will be able to prove exactly why."):
            self.play(FadeOut(q), FadeIn(win, shift=UP * 0.2))
        self.play(FadeOut(VGroup(ramps, win, tag_r, tag_d)), FadeOut(ring2), FadeOut(disc), run_time=0.7)
        self.remove(ring2, disc)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 1: Rotational Dynamics. Everything you learned about straight line motion in Class 11 has a twin in the world of spin. Learn the translation, and this whole unit writes itself."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is our path. Angular kinematics, rotational kinetic energy, moment of inertia, the inertia of a rod, torque, work and power, and finally, angular momentum.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        O = LEFT * 3.4 + DOWN * 0.3
        R = 2.4
        body = Circle(radius=R, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3).move_to(O)
        axis = Dot(O, radius=0.08, color=WHITE)
        olab = T("O", size=24, color=th.MUTED).next_to(axis, DL, buff=0.08)
        th_ = ValueTracker(0)
        radii = [0.9, 1.6, 2.3]
        cols = [th.TEAL, th.AMBER, th.CORAL]
        ref = Line(O, O + RIGHT * R, color=th.FAINT, stroke_width=3)
        spoke = always_redraw(lambda: Line(O, O + R * np.array([np.cos(th_.get_value()), np.sin(th_.get_value()), 0]), color=WHITE, stroke_width=3))
        dots = VGroup(*[always_redraw(lambda r=r, c=c: Dot(O + r * np.array([np.cos(th_.get_value()), np.sin(th_.get_value()), 0]), radius=0.1, color=c)) for r, c in zip(radii, cols)])
        arcs = VGroup(*[always_redraw(lambda r=r, c=c: Arc(radius=r, start_angle=0, angle=max(th_.get_value(), 1e-3), arc_center=O, color=c, stroke_width=5)) for r, c in zip(radii, cols)])
        ang = always_redraw(lambda: Arc(radius=0.45, start_angle=0, angle=max(th_.get_value(), 1e-3), arc_center=O, color=C_TH, stroke_width=4))
        thl = always_redraw(lambda: M(r"\theta", color=C_TH, size=40).move_to(O + 0.75 * np.array([np.cos(th_.get_value() / 2), np.sin(th_.get_value() / 2), 0])))
        with self.say("Picture a rigid body spinning about a fixed axis through the point O. Every particle of the body moves in a circle around that axis."):
            self.play(DrawBorderThenFill(body), FadeIn(axis), FadeIn(olab), run_time=1.0)
            self.add(ref, arcs, spoke, dots)
            self.play(th_.animate.set_value(1.1), run_time=2.5, rate_func=smooth)
        self.add(ang, thl)
        with self.say("Look at three particles at different distances from the axis. The outer one travels a longer arc than the inner one. But every one of them turns through the same angle. That shared angle, theta, is why angle, not distance, is the natural language of rotation."):
            self.play(th_.animate.set_value(2.0), run_time=3.0, rate_func=smooth)
            self.play(*[Indicate(a) for a in arcs], run_time=1.2)
        d1 = M(r"\theta", r"=", r"{s", r"\over", r"r}", size=64).move_to(RIGHT * 3.3 + UP * 2.0)
        d1[0].set_color(C_TH)
        lab = T("arc length ÷ radius  (radians)", size=24, color=th.MUTED).next_to(d1, DOWN, buff=0.25)
        with self.say("We measure that angle in radians: the arc length s, divided by the radius r."):
            self.play(Write(d1), FadeIn(lab, shift=UP * 0.1))
        rad_r = 1.6
        C2 = RIGHT * 3.3 + DOWN * 1.4
        circ = Circle(radius=rad_r, color=th.FAINT, stroke_width=3).move_to(C2)
        rline = Line(C2, C2 + RIGHT * rad_r, color=th.SKY, stroke_width=6)
        with self.say("What is one radian? Take the radius itself, and bend it onto the circle. The angle it covers is exactly one radian, about fifty seven degrees."):
            self.play(Create(circ), Create(rline))
            bent = Arc(radius=rad_r, start_angle=0, angle=1.0, arc_center=C2, color=th.SKY, stroke_width=6)
            copy = rline.copy()
            self.play(Transform(copy, bent), run_time=1.5)
            wedge = Sector(radius=0.6, angle=1.0, arc_center=C2, fill_color=th.SKY, fill_opacity=0.35, stroke_width=0)
            one = M(r"1\,\text{rad}", size=30, color=th.SKY).move_to(C2 + 0.95 * np.array([np.cos(0.5), np.sin(0.5), 0]))
            self.play(FadeIn(wedge), FadeIn(one))
        lays = VGroup()
        for k in range(1, 6):
            lays.add(Arc(radius=rad_r, start_angle=k, angle=1.0, arc_center=C2, color=[th.TEAL, th.AMBER, th.CORAL, th.MINT, th.PINK][k - 1], stroke_width=6))
        last = Arc(radius=rad_r, start_angle=6, angle=2 * PI - 6, arc_center=C2, color=WHITE, stroke_width=6)
        full = M(r"2\pi \approx 6.28\ \text{radii fit}", size=30).next_to(circ, DOWN, buff=0.15)
        with self.say("Keep laying radii around the rim: two, three, four, five, six, and a little bit more. Exactly two pi radii fit around a full circle. So one revolution is two pi radians."):
            for a in lays:
                self.sfx("tick", gain=-12)
                self.play(Create(a), run_time=0.45)
            self.play(Create(last), run_time=0.4)
            self.play(FadeIn(full, shift=UP * 0.1))
        self.wait(0.3)
        self.play(FadeOut(VGroup(circ, rline, copy, wedge, one, lays, last, full, d1, lab)))
        defs = VGroup(
            VGroup(M(r"\omega", r"=", r"{d\theta", r"\over", r"dt}", size=56), T("angular velocity  ·  rad s⁻¹", size=22, color=th.MUTED)),
            VGroup(M(r"\alpha", r"=", r"{d\omega", r"\over", r"dt}", size=56), T("angular acceleration  ·  rad s⁻²", size=22, color=th.MUTED)),
        )
        for d in defs:
            d.arrange(DOWN, buff=0.2)
        defs[0][0][0].set_color(C_W)
        defs[1][0][0].set_color(C_A)
        defs.arrange(DOWN, buff=0.6).move_to(RIGHT * 3.3)
        with self.say("How fast the angle changes is the angular velocity, omega, equal to d theta by d t, in radians per second."):
            self.play(Write(defs[0]))
            self.play(th_.animate.set_value(2.0 + 2 * PI), run_time=3.0, rate_func=linear)
        with self.say("And how fast omega itself changes is the angular acceleration, alpha, equal to d omega by d t, in radians per second squared."):
            self.play(Write(defs[1]))
            self.play(th_.animate.set_value(2.0 + 6 * PI), run_time=3.0, rate_func=rate_functions.ease_in_quad)
        self.play(FadeOut(VGroup(body, axis, olab, ref, defs)), FadeOut(arcs), FadeOut(spoke), FadeOut(dots), FadeOut(ang), FadeOut(thl))
        self.remove(arcs, spoke, dots, ang, thl)
        self.dictionary()
        self.equations()
        self.linear_link()
        self.example_wheel()

    def dictionary(self):
        rows = [("s", r"\theta", "displacement"), ("v", r"\omega", "velocity"), ("a", r"\alpha", "acceleration"),
                ("m", "I", "mass  →  moment of inertia"), ("F", r"\tau", "force  →  torque"), ("p", "L", "momentum  →  angular momentum")]
        cols = [C_TH, C_W, C_A, C_I, C_TAU, C_L]
        hl = T("Linear", size=30, color=th.MUTED, weight="SEMIBOLD").move_to([-3.6, 2.35, 0])
        hr = T("Rotational", size=30, color=th.MUTED, weight="SEMIBOLD").move_to([0.4, 2.35, 0])
        title = T("The translation dictionary", size=40, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        g = VGroup()
        for i, ((a, b, name), c) in enumerate(zip(rows, cols)):
            y = 1.6 - i * 0.78
            la = M(a, size=50).move_to([-3.6, y, 0])
            ar = Arrow([-2.8, y, 0], [-0.4, y, 0], color=c, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.12)
            rb = M(b, size=50, color=c).move_to([0.4, y, 0])
            nm = T(name, size=22, color=th.BODY).move_to([4.2, y, 0])
            g.add(VGroup(la, ar, rb, nm))
        self.play(FadeIn(title, shift=DOWN * 0.2), FadeIn(hl), FadeIn(hr))
        with self.say("Here is the key that unlocks the whole chapter. Every linear quantity has a rotational partner. Displacement becomes angle. Velocity becomes angular velocity. Acceleration becomes angular acceleration. Mass becomes moment of inertia. Force becomes torque. And momentum becomes angular momentum.") as v:
            for r in g:
                self.play(FadeIn(r[0]), GrowArrow(r[1]), run_time=0.5)
                self.play(TransformFromCopy(r[0], r[2]), FadeIn(r[3], shift=LEFT * 0.2), run_time=0.7)
                self.hold(v.dur / 6 - 1.2)
        with self.say("Remember this table, and you can rebuild almost every formula in this unit, just by swapping the symbols."):
            self.play(Circumscribe(g, color=th.AMBER, buff=0.2), run_time=1.6)
        self.play(FadeOut(VGroup(title, hl, hr, g)))

    def equations(self):
        lin = VGroup(M(r"v = u + at"), M(r"s = ut + \tfrac{1}{2}at^{2}"), M(r"v^{2} = u^{2} + 2as")).arrange(DOWN, buff=0.55).move_to(LEFT * 3.4)
        rot = VGroup(M(r"\omega = \omega_0 + \alpha t"), M(r"\theta = \omega_0 t + \tfrac{1}{2}\alpha t^{2}"), M(r"\omega^{2} = \omega_0^{2} + 2\alpha\theta")).arrange(DOWN, buff=0.55).move_to(RIGHT * 3.4)
        hl = T("Class 11: constant a", size=26, color=th.MUTED).next_to(lin, UP, buff=0.6)
        hr = T("Class 12: constant α", size=26, color=C_A).next_to(rot, UP, buff=0.6)
        for e in rot:
            e.set_color_by_tex(r"\omega", C_W)
        with self.say("Watch it work. These are the three equations of motion you already know for constant acceleration."):
            self.play(FadeIn(hl), LaggedStart(*[Write(e) for e in lin], lag_ratio=0.3), run_time=2.0)
        with self.say("Swap u and v for omega nought and omega, a for alpha, and s for theta. Out come the three equations of angular motion, valid whenever alpha is constant."):
            self.play(FadeIn(hr))
            for a, b in zip(lin, rot):
                self.sfx("whoosh", gain=-16)
                self.play(TransformFromCopy(a, b), run_time=1.1)
        extra = M(r"\theta_n = \omega_0 + \frac{\alpha}{2}(2n-1)", size=40, color=th.BODY).to_edge(DOWN, buff=0.9)
        with self.say("Even the formula for the angle turned in the n-th second carries straight across."):
            self.play(FadeIn(extra, shift=UP * 0.2))
        self.play(FadeOut(VGroup(lin, rot, hl, hr, extra)))

    def linear_link(self):
        O = LEFT * 3.2 + DOWN * 0.2
        R = 2.5
        w = ValueTracker(0)
        disc = always_redraw(lambda: VGroup(
            Circle(radius=R, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3),
            *[Line(ORIGIN, R * np.array([np.cos(a), np.sin(a), 0]), color=th.FAINT, stroke_width=2) for a in np.arange(0, TAU, TAU / 8)],
        ).move_to(O).rotate(w.get_value(), about_point=O))
        self.add(disc)
        rs = [0.9, 1.7, 2.5]
        cols = [th.TEAL, th.AMBER, th.CORAL]

        def vecs():
            g = VGroup()
            a = w.get_value() + PI / 2
            for r, c in zip(rs, cols):
                p = O + r * np.array([np.cos(a), np.sin(a), 0])
                tdir = np.array([-np.sin(a), np.cos(a), 0])
                g.add(Dot(p, radius=0.09, color=c), Arrow(p, p + tdir * r * 0.75, buff=0, color=c, stroke_width=5, max_tip_length_to_length_ratio=0.2))
            return g
        vv = always_redraw(vecs)
        eq = M(r"v", r"=", r"r", r"\omega", size=72).move_to(RIGHT * 3.2 + UP * 2.2)
        eq[3].set_color(C_W)
        eq[2].set_color(C_R)
        with self.say("Now connect the two worlds. Since s equals r theta, and r is fixed for a particle, differentiating gives v equals r omega. Every particle shares the same omega, so its speed grows in proportion to its distance from the axis."):
            self.play(FadeIn(disc))
            self.add(vv)
            self.play(w.animate.set_value(PI * 1.2), run_time=4.0, rate_func=linear)
            self.play(Write(eq))
            self.play(w.animate.set_value(PI * 2.0), run_time=3.0, rate_func=linear)
        e2 = M(r"a_t", r"=", r"r", r"\alpha", size=56).next_to(eq, DOWN, buff=0.5)
        e3 = M(r"a_c", r"=", r"{v^{2}", r"\over", r"r}", r"=", r"r\omega^{2}", size=56).next_to(e2, DOWN, buff=0.45)
        e2[3].set_color(C_A)
        e2[0].set_color(th.TEAL)
        e3[0].set_color(th.PINK)
        self.play(FadeOut(vv))
        self.remove(vv)
        P = O + R * np.array([np.cos(w.get_value() + PI / 2), np.sin(w.get_value() + PI / 2), 0])
        tdir = np.array([-np.sin(w.get_value() + PI / 2), np.cos(w.get_value() + PI / 2), 0])
        cdir = (O - P) / np.linalg.norm(O - P)
        at = Arrow(P, P + tdir * 1.6, buff=0, color=th.TEAL, stroke_width=6)
        ac = Arrow(P, P + cdir * 1.8, buff=0, color=th.PINK, stroke_width=6)
        res = Arrow(P, P + tdir * 1.6 + cdir * 1.8, buff=0, color=WHITE, stroke_width=6)
        lt = M(r"a_t", color=th.TEAL, size=36).next_to(at.get_end(), UP, buff=0.1)
        lc = M(r"a_c", color=th.PINK, size=36).next_to(ac.get_end(), LEFT, buff=0.1)
        with self.say("If the spin is speeding up, a point on the rim has two accelerations. The tangential acceleration, r alpha, changes its speed."):
            self.play(Write(e2), GrowArrow(at), FadeIn(lt))
        with self.say("And the centripetal acceleration, v squared over r, or r omega squared, points to the centre and keeps turning its direction."):
            self.play(Write(e3), GrowArrow(ac), FadeIn(lc))
        e4 = M(r"a = \sqrt{a_t^{2} + a_c^{2}}", size=48).next_to(e3, DOWN, buff=0.45)
        with self.say("They are at right angles, so the total acceleration is the square root of a t squared plus a c squared."):
            self.play(GrowArrow(res), Write(e4))
        self.play(FadeOut(VGroup(at, ac, res, lt, lc, eq, e2, e3, e4)), FadeOut(disc))
        self.remove(disc)
        self.tip("Formulas like v = rω, s = rθ and τ = Iα work ONLY in radians. Convert first: 1 rev = 2π rad, and N rpm means ω = 2πN/60 rad/s.",
                 "Here is the trap that costs marks every year. v equals r omega, s equals r theta, and torque equals I alpha are true only when angles are in radians. If a question gives revolutions per minute, convert first. One revolution is two pi radians, so N revolutions per minute means omega equals two pi N over sixty radians per second.")

    def example_wheel(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A grinding wheel starts from rest and reaches 300 rev/min in 10 s with uniform angular acceleration. Find (a) α, (b) the number of revolutions, (c) the speed of a point 0.40 m from the axis.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        with self.say("Let us try a real problem. A grinding wheel starts from rest and reaches three hundred revolutions per minute in ten seconds, with uniform angular acceleration. Find the angular acceleration, the number of revolutions it makes, and the final speed of a point forty centimetres from the axis."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        self.play(prob.animate.scale(0.72).next_to(head, DOWN, aligned_edge=LEFT, buff=0.2), run_time=0.6)
        O = LEFT * 4.3 + DOWN * 0.55
        Rw = 1.35
        t = ValueTracker(0)
        alpha = PI
        wheelg = always_redraw(lambda: VGroup(
            Circle(radius=Rw, fill_color="#3a3f5c", fill_opacity=1, stroke_color=th.MUTED, stroke_width=4),
            Circle(radius=Rw * 0.82, stroke_color="#4c5275", stroke_width=2),
            *[Line(ORIGIN, Rw * 0.82 * np.array([np.cos(a), np.sin(a), 0]), color="#565d86", stroke_width=3) for a in np.arange(0, TAU, TAU / 6)],
            Dot(radius=0.12, color=WHITE),
        ).move_to(O).rotate(0.5 * alpha * t.get_value() ** 2, about_point=O))
        def readout():
            tv = t.get_value()
            g = VGroup(
                T(f"t = {tv:4.1f} s", size=22, color=th.BODY),
                T(f"ω = {alpha * tv:5.1f} rad/s", size=22, color=C_W),
                T(f"turns = {0.25 * alpha * tv ** 2 / PI:4.1f}", size=22, color=C_TH),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            return g.next_to(O + DOWN * Rw, DOWN, buff=0.25)
        ro = always_redraw(readout)
        self.add(wheelg, ro)
        self.play(FadeIn(wheelg), FadeIn(ro))
        self.play(t.animate.set_value(10), run_time=6, rate_func=linear)
        steps = VGroup(
            M(r"\omega = \frac{2\pi \times 300}{60} = 10\pi \approx 31.4\ \text{rad s}^{-1}", size=36),
            M(r"\alpha = \frac{\omega - \omega_0}{t} = \frac{10\pi}{10} = \pi \approx 3.14\ \text{rad s}^{-2}", size=36),
            M(r"\theta = \tfrac{1}{2}\alpha t^{2} = \tfrac{1}{2}(\pi)(10)^{2} = 50\pi\ \text{rad}", size=36),
            M(r"\text{turns} = \frac{50\pi}{2\pi} = 25", size=36),
            M(r"v = r\omega = 0.40 \times 31.4 \approx 12.6\ \text{m s}^{-1}", size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 2.6 + DOWN * 0.9)
        steps[1].set_color(C_A)
        steps[3].set_color(C_TH)
        steps[4].set_color(C_W)
        with self.say("First, convert. Three hundred revolutions per minute is two pi times three hundred, over sixty, which is ten pi, about thirty one point four radians per second."):
            self.play(Write(steps[0]))
        with self.say("Then alpha is the change in omega divided by time: ten pi over ten, which is pi, about three point one four radians per second squared."):
            self.play(Write(steps[1]))
        with self.say("Starting from rest, theta equals half alpha t squared: half times pi times one hundred, which is fifty pi radians. Divide by two pi for each turn, and you get exactly twenty five revolutions. Check the counter on the wheel. Twenty five."):
            self.play(Write(steps[2]))
            self.play(Write(steps[3]))
            self.play(Indicate(steps[3], color=th.AMBER))
        with self.say("Finally, v equals r omega: zero point four times thirty one point four, about twelve point six metres per second at that point."):
            self.play(Write(steps[4]))
            self.play(Circumscribe(steps[4], color=C_W))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps, ro)), FadeOut(wheelg))
        self.remove(wheelg, ro)

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        O = LEFT * 3.4 + DOWN * 0.2
        w = ValueTracker(0)
        pts = [(0.8, 0.3, "m_1"), (1.5, 2.2, "m_2"), (2.2, 4.1, "m_3"), (1.2, 5.3, "m_4")]
        body = Circle(radius=2.6, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3).move_to(O)
        cols = [th.TEAL, th.AMBER, th.CORAL, th.PINK]

        def particles():
            g = VGroup()
            for (r, a0, lab), c in zip(pts, cols):
                a = a0 + w.get_value()
                p = O + r * np.array([np.cos(a), np.sin(a), 0])
                tdir = np.array([-np.sin(a), np.cos(a), 0])
                g.add(DashedLine(O, p, color=th.FAINT, stroke_width=2), Dot(p, radius=0.11, color=c),
                      Arrow(p, p + tdir * r * 0.55, buff=0, color=c, stroke_width=4, max_tip_length_to_length_ratio=0.25))
            return g
        pg = always_redraw(particles)
        with self.say("A spinning body has energy, even though it is not going anywhere. Where is that energy? Think of the body as a crowd of tiny particles, masses m one, m two, m three, at distances r one, r two, r three from the axis."):
            self.play(DrawBorderThenFill(body))
            self.add(pg)
            self.play(w.animate.set_value(2.0), run_time=4, rate_func=linear)
        lines = VGroup(
            M(r"v_i = r_i\,\omega", size=46),
            M(r"E_k = \sum_i \tfrac{1}{2} m_i v_i^{2}", size=46),
            M(r"E_k = \sum_i \tfrac{1}{2} m_i (r_i\omega)^{2}", size=46),
            M(r"E_k = \tfrac{1}{2}\Big(\sum_i m_i r_i^{2}\Big)\,\omega^{2}", size=46),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.0 + UP * 0.4)
        with self.say("All the particles share the same omega, so particle i moves with speed r i omega."):
            self.play(Write(lines[0]))
            self.play(w.animate.set_value(3.5), run_time=2, rate_func=linear)
        with self.say("The total kinetic energy is just the sum of half m v squared for every particle."):
            self.play(Write(lines[1]))
        with self.say("Substitute r i omega for v i. Omega is the same for everyone, so pull it out of the sum."):
            self.play(TransformFromCopy(lines[1], lines[2]))
            self.play(TransformFromCopy(lines[2], lines[3]))
        brace = Brace(lines[3][0][6:15], DOWN, color=C_I)
        bl = T("moment of inertia, I", size=26, color=C_I).next_to(brace, DOWN, buff=0.1)
        with self.say("Look at the bracket. The sum of m r squared contains only masses and distances. It depends on the body and the axis, not on the motion at all. We give it a name: the moment of inertia, I."):
            self.play(GrowFromCenter(brace), FadeIn(bl))
            self.play(w.animate.set_value(5.0), run_time=3, rate_func=linear)
        final = M(r"E_k = \tfrac{1}{2} I \omega^{2}", size=80, color=th.INK)
        box = SurroundingRectangle(final, color=C_I, buff=0.3, corner_radius=0.15)
        comp = M(r"\text{compare: } \tfrac{1}{2} m v^{2}", size=40, color=th.MUTED)
        self.play(FadeOut(VGroup(lines, brace, bl, body)), FadeOut(pg))
        self.remove(pg)
        VGroup(final, comp).arrange(DOWN, buff=0.6)
        box.move_to(final)
        with self.say("So the rotational kinetic energy is one half I omega squared. Put it beside one half m v squared. Moment of inertia does for rotation exactly what mass does for straight line motion."):
            self.sfx("impact", gain=-12)
            self.play(Write(final), Create(box))
            self.play(FadeIn(comp, shift=UP * 0.2))
        roll = M(r"E_{\text{rolling}} = \tfrac{1}{2} M v^{2} + \tfrac{1}{2} I \omega^{2}", size=46).next_to(comp, DOWN, buff=0.6)
        with self.say("And a wheel that rolls has both kinds at once: translational energy for its forward motion, plus rotational energy for its spin. Hold on to that. It is the key to our race."):
            self.play(Write(roll))
        self.play(FadeOut(VGroup(final, box, comp, roll)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        defn = M(r"I", r"=", r"\sum m_i r_i^{2}", r"=", r"\int r^{2}\,dm", size=64).to_edge(UP, buff=1.1)
        defn[0].set_color(C_I)
        unit = T("SI unit kg m²   ·   dimensions [M L²]", size=24, color=th.MUTED).next_to(defn, DOWN, buff=0.25)
        with self.say("The moment of inertia of a body about an axis is the sum of each mass times the square of its perpendicular distance from that axis. For a continuous body, the sum becomes an integral of r squared d m. Its unit is kilogram metre squared."):
            self.play(Write(defn))
            self.play(FadeIn(unit))
        self.play(VGroup(defn, unit).animate.scale(0.7).to_edge(UP, buff=0.75))
        dumb = []
        for k, (x, d) in enumerate([(-3.4, 0.6), (3.4, 2.0)]):
            dumb.append((x, d))
        angs = [ValueTracker(0), ValueTracker(0)]

        def dumbbell(x, d, a):
            def f():
                c = np.array([x, -0.6, 0])
                rod = Line(c + LEFT * 2.3, c + RIGHT * 2.3, color=th.MUTED, stroke_width=6)
                b1 = Circle(radius=0.28, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to(c + LEFT * d)
                b2 = b1.copy().move_to(c + RIGHT * d)
                hub = Dot(c, radius=0.1, color=WHITE)
                return VGroup(rod, b1, b2, hub).rotate(a.get_value(), about_point=c)
            return f
        d1 = always_redraw(dumbbell(-3.4, 0.6, angs[0]))
        d2 = always_redraw(dumbbell(3.4, 2.0, angs[1]))
        l1 = T("masses near the axis", size=24, color=th.BODY).move_to([-3.4, -3.2, 0])
        l2 = T("same masses, far out", size=24, color=th.BODY).move_to([3.4, -3.2, 0])
        with self.say("Why does distance matter so much? Here are two identical rods with identical masses. On the left, the masses sit close to the axis. On the right, the same masses sit far out. We give both the same twist."):
            self.add(d1, d2)
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(l1), FadeIn(l2))
        ratio = (2.0 / 0.6) ** 2
        with self.say("The left one spins up quickly. The right one barely gets going. Its masses are about three times further out, and because the distance is squared, it has about eleven times the moment of inertia."):
            self.play(angs[0].animate.set_value(6 * PI), angs[1].animate.set_value(6 * PI / ratio), run_time=5, rate_func=rate_functions.ease_in_quad)
        f = VGroup(T("I depends on:", size=28, color=th.INK, weight="SEMIBOLD"),
                   T("1.  the total mass", size=26, color=th.BODY),
                   T("2.  how that mass is distributed", size=26, color=th.BODY),
                   T("3.  which axis you choose", size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(FadeOut(VGroup(l1, l2)), FadeOut(d1), FadeOut(d2))
        self.remove(d1, d2)
        f.move_to(ORIGIN)
        with self.say("So unlike mass, moment of inertia is not one fixed number for a body. It depends on three things: the total mass, how that mass is distributed, and which axis you choose to spin it about."):
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in f], lag_ratio=0.4), run_time=2.5)
        self.play(FadeOut(f), FadeOut(VGroup(defn, unit)))
        self.shapes_table()
        self.gyration()
        self.axis_theorems()
        self.race_solved()
        self.example_flywheel()

    def shapes_table(self):
        title = T("Moments of inertia to know", size=38, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        items = [
            ("Rod, centre", r"\tfrac{1}{12}ML^{2}", "rodc"), ("Rod, end", r"\tfrac{1}{3}ML^{2}", "rode"),
            ("Ring", r"MR^{2}", "ring"), ("Disc / cylinder", r"\tfrac{1}{2}MR^{2}", "disc"),
            ("Solid sphere", r"\tfrac{2}{5}MR^{2}", "sph"), ("Hollow sphere", r"\tfrac{2}{3}MR^{2}", "hsph"),
        ]
        cards = VGroup()
        for name, f, kind in items:
            box = self.panel(3.9, 2.35)
            if kind in ("rodc", "rode"):
                ic = VGroup(Line(LEFT * 1.0, RIGHT * 1.0, color=th.AMBER, stroke_width=10))
                ax = DashedLine(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=3).move_to(ORIGIN if kind == "rodc" else LEFT * 1.0)
                ic.add(ax)
            elif kind == "ring":
                ic = VGroup(Annulus(inner_radius=0.42, outer_radius=0.55, fill_color=th.AMBER, fill_opacity=1, stroke_width=0), Dot(color=WHITE, radius=0.06))
            elif kind == "disc":
                ic = VGroup(Circle(radius=0.55, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0), Dot(color=WHITE, radius=0.06))
            elif kind == "sph":
                ic = VGroup(Circle(radius=0.55, fill_color=th.AMBER, fill_opacity=1, stroke_width=0), Circle(radius=0.2, fill_color=WHITE, fill_opacity=0.35, stroke_width=0).shift(UL * 0.2), DashedLine(UP * 0.75, DOWN * 0.75, color=WHITE, stroke_width=3))
            else:
                ic = VGroup(Circle(radius=0.55, stroke_color=th.AMBER, stroke_width=6), Ellipse(width=1.1, height=0.3, stroke_color=th.AMBER, stroke_width=2, stroke_opacity=0.6), DashedLine(UP * 0.75, DOWN * 0.75, color=WHITE, stroke_width=3))
            fm = M(f, size=40, color=C_I)
            nm = T(name, size=22, color=th.BODY)
            inner = VGroup(ic, fm, nm).arrange(DOWN, buff=0.18).move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).next_to(title, DOWN, buff=0.4)
        with self.say("Here are the six results the syllabus expects you to know. A thin rod: one twelfth M L squared about its centre, one third M L squared about one end. A ring: M R squared. A disc or solid cylinder: one half M R squared. A solid sphere: two fifths M R squared. And a hollow sphere: two thirds M R squared.") as v:
            self.play(FadeIn(title))
            for cd in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(cd, shift=UP * 0.2, scale=0.9), run_time=0.5)
                self.hold(v.dur / 6 - 0.75)
        with self.say("Notice the pattern. The more of the mass that sits far from the axis, the bigger the number in front. The ring, with everything at the rim, has the largest of all."):
            self.play(Indicate(cards[2], color=th.AMBER, scale_factor=1.05), run_time=1.2)
        self.play(FadeOut(VGroup(title, cards)))

    def gyration(self):
        O = LEFT * 3.2 + DOWN * 0.3
        R = 2.4
        rng = np.random.default_rng(4)
        pts = []
        while len(pts) < 140:
            p = rng.uniform(-1, 1, 2)
            if np.hypot(*p) < 1:
                pts.append(p)
        dots = VGroup(*[Dot(O + R * np.array([p[0], p[1], 0]), radius=0.05, color=th.AMBER) for p in pts])
        outline = Circle(radius=R, stroke_color=th.PANEL_EDGE, stroke_width=3).move_to(O)
        k = R / np.sqrt(2)
        eq = M(r"I", r"=", r"M", r"k^{2}", size=64).move_to(RIGHT * 3.2 + UP * 1.8)
        eq[0].set_color(C_I)
        eq[3].set_color(th.SKY)
        eq2 = M(r"k = \sqrt{I / M}", size=52).next_to(eq, DOWN, buff=0.4)
        with self.say("Now a neat idea: the radius of gyration. A disc has its mass spread from the centre to the rim. Could we squeeze all of it into one thin ring, at just the right radius, without changing the moment of inertia?"):
            self.play(Create(outline), LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.01), run_time=2.0)
        targets = []
        for i, d in enumerate(dots):
            a = TAU * i / len(dots)
            targets.append(O + k * np.array([np.cos(a), np.sin(a), 0]))
        kr = Line(O, O + k * RIGHT, color=th.SKY, stroke_width=5)
        kl = M("k", color=th.SKY, size=40).next_to(kr, UP, buff=0.08)
        with self.say("Yes. That radius is called k, the radius of gyration. For a disc it comes out at R over root two, about seventy one percent of the way to the rim."):
            self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=2.5, rate_func=smooth)
            self.play(Create(kr), FadeIn(kl))
        with self.say("By definition, I equals M k squared, so k equals the square root of I over M. It is the distance at which the whole mass, concentrated, would give the same moment of inertia."):
            self.play(Write(eq))
            self.play(Write(eq2))
        disc_k = M(r"\text{disc: } k = \sqrt{\tfrac{\frac{1}{2}MR^{2}}{M}} = \frac{R}{\sqrt{2}}", size=40, color=th.BODY).next_to(eq2, DOWN, buff=0.5)
        self.play(Write(disc_k))
        self.wait(1)
        self.play(FadeOut(VGroup(dots, outline, kr, kl, eq, eq2, disc_k)))

    def axis_theorems(self):
        title = T("Two shortcuts", size=38, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cm = np.array([-3.2, -0.4, 0])
        disc = Circle(radius=1.6, fill_color=th.AMBER, fill_opacity=0.5, stroke_color=th.AMBER).move_to(cm)
        ax1 = DashedLine(cm + UP * 2.2, cm + DOWN * 2.2, color=WHITE, stroke_width=3)
        ax2 = DashedLine(cm + UP * 2.2 + RIGHT * 1.6, cm + DOWN * 2.2 + RIGHT * 1.6, color=th.SKY, stroke_width=3)
        dbr = BraceBetweenPoints(cm + DOWN * 1.9, cm + DOWN * 1.9 + RIGHT * 1.6, DOWN, color=th.SKY)
        dl = M("d", color=th.SKY, size=36).next_to(dbr, DOWN, buff=0.08)
        pa = M(r"I = I_{cm} + M d^{2}", size=54).move_to(RIGHT * 3.0 + UP * 1.2)
        pal = T("Parallel axis theorem", size=26, color=th.SKY, weight="SEMIBOLD").next_to(pa, UP, buff=0.25)
        with self.say("Two theorems save you a lot of integration. The parallel axis theorem: if you know I about an axis through the centre of mass, the moment of inertia about any parallel axis, a distance d away, is I c m plus M d squared."):
            self.play(FadeIn(title), FadeIn(disc), Create(ax1))
            self.play(TransformFromCopy(ax1, ax2), GrowFromCenter(dbr), FadeIn(dl))
            self.play(FadeIn(pal), Write(pa))
        pp = M(r"I_z = I_x + I_y", size=54).move_to(RIGHT * 3.0 + DOWN * 1.4)
        ppl = T("Perpendicular axis theorem (flat laminae)", size=24, color=th.MINT, weight="SEMIBOLD").next_to(pp, UP, buff=0.25)
        with self.say("And the perpendicular axis theorem, for flat sheets only: the moment of inertia about an axis perpendicular to the sheet equals the sum about two perpendicular axes lying in its plane."):
            self.play(FadeIn(ppl), Write(pp))
        self.wait(0.5)
        self.play(FadeOut(VGroup(title, disc, ax1, ax2, dbr, dl, pa, pal, pp, ppl)))

    def race_solved(self):
        head = T("Back to the race", size=40, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        with self.say("Now we can settle the race. Both wheels start at the same height, so both convert the same potential energy, M g h. But a rolling wheel must split that energy between moving forward and spinning."):
            self.play(FadeIn(head))
        def bars(x, name, col, rot_frac):
            base = np.array([x, -1.9, 0])
            H = 3.5
            tr = Rectangle(width=1.4, height=H * (1 - rot_frac), fill_color=th.TEAL, fill_opacity=0.9, stroke_width=0)
            ro = Rectangle(width=1.4, height=H * rot_frac, fill_color=col, fill_opacity=0.9, stroke_width=0)
            tr.move_to(base, aligned_edge=DOWN)
            ro.next_to(tr, UP, buff=0)
            nm = T(name, size=28, color=col, weight="SEMIBOLD").next_to(base, DOWN, buff=0.25)
            return tr, ro, nm
        trr, ror, nr = bars(-3.0, "Ring", th.AMBER, 0.5)
        trd, rod, nd = bars(0.4, "Disc", th.SKY, 1 / 3)
        lt = T("forward motion", size=24, color=th.TEAL).move_to([3.9, -1.0, 0])
        lr = T("spin", size=24, color=th.BODY).move_to([3.9, 1.0, 0])
        er = M(r"I = MR^{2}:\ \tfrac{1}{2}I\omega^{2} = \tfrac{1}{2}Mv^{2}", size=30, color=th.AMBER).next_to(VGroup(trr, ror), UP, buff=0.3).shift(LEFT * 0.4)
        ed = M(r"I = \tfrac{1}{2}MR^{2}:\ \tfrac{1}{2}I\omega^{2} = \tfrac{1}{4}Mv^{2}", size=30, color=th.SKY).next_to(VGroup(trd, rod), UP, buff=0.3).shift(RIGHT * 0.6)
        with self.say("For the ring, I is M R squared, and with omega equal to v over R, its spin energy equals its forward energy. Half of all the energy goes into spinning."):
            self.play(GrowFromEdge(trr, DOWN), FadeIn(nr))
            self.play(GrowFromEdge(ror, DOWN), Write(er))
        with self.say("For the disc, I is only half M R squared, so spin takes just one third of the energy, and two thirds is left for moving forward."):
            self.play(GrowFromEdge(trd, DOWN), FadeIn(nd))
            self.play(GrowFromEdge(rod, DOWN), Write(ed))
            self.play(FadeIn(lt), FadeIn(lr))
        concl = T("More energy into forward motion  →  faster  →  the disc wins.", size=30, color=th.INK, weight="SEMIBOLD").to_edge(DOWN, buff=0.35)
        with self.say("More energy for forward motion means more speed at every point on the slope. That is why the disc always wins. Mass far from the axis makes a body lazy to spin, and that laziness costs speed."):
            self.play(Indicate(trd, color=WHITE), FadeIn(concl, shift=UP * 0.2))
        self.wait(0.5)
        self.play(FadeOut(VGroup(head, trr, ror, nr, trd, rod, nd, lt, lr, er, ed, concl)))

    def example_flywheel(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A solid disc flywheel of mass 20 kg and radius 0.50 m spins at 120 rev/min. Find its moment of inertia, radius of gyration and kinetic energy.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"I = \tfrac{1}{2}MR^{2} = \tfrac{1}{2}(20)(0.50)^{2} = 2.5\ \text{kg m}^{2}", size=40),
            M(r"k = \sqrt{I/M} = \sqrt{2.5/20} \approx 0.354\ \text{m} \;\;(=R/\sqrt{2})", size=40),
            M(r"\omega = \frac{2\pi(120)}{60} = 4\pi \approx 12.57\ \text{rad s}^{-1}", size=40),
            M(r"E_k = \tfrac{1}{2}I\omega^{2} = \tfrac{1}{2}(2.5)(12.57)^{2} \approx 197\ \text{J}", size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.6).align_to(prob, LEFT)
        steps[0].set_color(C_I)
        steps[3].set_color(th.AMBER)
        with self.say("One more example. A solid disc flywheel of mass twenty kilograms and radius half a metre spins at one hundred and twenty revolutions per minute. Find I, k, and its kinetic energy."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        with self.say("For a disc, I is half M R squared: half times twenty times zero point two five, which is two point five kilogram metre squared."):
            self.play(Write(steps[0]))
        with self.say("The radius of gyration is the square root of two point five over twenty, about zero point three five four metres. That is R over root two, just as we found."):
            self.play(Write(steps[1]))
        with self.say("Convert the speed: one hundred and twenty r p m is four pi, about twelve point five seven radians per second."):
            self.play(Write(steps[2]))
        with self.say("And the energy is half I omega squared: about one hundred and ninety seven joules, stored in the spin."):
            self.play(Write(steps[3]))
            self.play(Circumscribe(steps[3], color=th.AMBER))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        L = 6.0
        y = 1.6
        rod = Rectangle(width=L, height=0.28, fill_color=th.AMBER, fill_opacity=0.85, stroke_width=0).move_to([0, y, 0])
        axis = DashedLine([0, y + 0.9, 0], [0, y - 0.9, 0], color=WHITE, stroke_width=3)
        ends = VGroup(M(r"-\tfrac{L}{2}", size=32).next_to(rod, LEFT, buff=0.2), M(r"+\tfrac{L}{2}", size=32).next_to(rod, RIGHT, buff=0.2))
        Cl = M("C", size=30, color=th.MUTED).next_to(axis, UP, buff=0.05)
        with self.say("Now let us derive the moment of inertia of a uniform rod ourselves. This derivation is a favourite long question. Take a thin rod of mass M and length L, with the axis through its centre C, perpendicular to the rod."):
            self.play(GrowFromCenter(rod), Create(axis), FadeIn(Cl))
            self.play(FadeIn(ends))
        xv = ValueTracker(1.6)
        el = always_redraw(lambda: Rectangle(width=0.22, height=0.34, fill_color=th.SKY, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to([xv.get_value(), y, 0]))
        xb = always_redraw(lambda: BraceBetweenPoints([0, y - 0.25, 0], [xv.get_value(), y - 0.25, 0], DOWN, color=th.SKY, buff=0.05))
        xl = always_redraw(lambda: M("x", size=30, color=th.SKY).next_to(xb, DOWN, buff=0.05))
        dxl = always_redraw(lambda: M("dx", size=28, color=WHITE).next_to(el, UP, buff=0.1))
        eqs = VGroup(M(r"\lambda = \frac{M}{L}", size=40), M(r"dm = \frac{M}{L}\,dx", size=40), M(r"dI = x^{2}\,dm", size=40)).arrange(RIGHT, buff=0.9).move_to([0, -0.1, 0])
        with self.say("The mass per unit length is M over L. Pick a tiny element of length d x, at a distance x from the centre. Its mass is d m equals M over L times d x, and since it is so small, its moment of inertia is simply x squared d m."):
            self.add(el, xb, xl, dxl)
            self.play(FadeIn(el), FadeIn(xb), FadeIn(xl), FadeIn(dxl))
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]))
            self.play(Write(eqs[2]))
        ax = Axes(x_range=[-3.2, 3.2, 1], y_range=[0, 9.5, 3], x_length=6.4 * (L / 6.0), y_length=2.6, tips=False,
                  axis_config={"color": th.FAINT, "include_ticks": False}).move_to([0, -2.3, 0])
        curve = ax.plot(lambda x: x ** 2, x_range=[-3, 3], color=th.SKY, stroke_width=4)
        cl = M(r"x^{2}", size=32, color=th.SKY).next_to(ax.c2p(3, 9), RIGHT, buff=0.1)
        self.play(eqs.animate.scale(0.75).move_to([0, 0.35, 0]))
        with self.say("Each element contributes in proportion to x squared. Let us plot that contribution along the rod. Elements near the centre add almost nothing. Elements near the ends add the most."):
            self.play(Create(ax), Create(curve), FadeIn(cl))
            self.play(xv.animate.set_value(-2.8), run_time=2.5, rate_func=smooth)
            self.play(xv.animate.set_value(2.8), run_time=2.5, rate_func=smooth)
        area = ax.get_area(curve, x_range=[-3, 3], color=th.SKY, opacity=0.35)
        integ = M(r"I_C", r"=", r"\int_{-L/2}^{+L/2} x^{2}\,\frac{M}{L}\,dx", size=46).to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        integ.move_to([0, 0.35, 0])
        with self.say("Adding up all the elements from minus L by two to plus L by two is exactly an integral. The moment of inertia is the shaded area under this curve, times M over L."):
            self.play(FadeOut(eqs))
            self.play(Write(integ), FadeIn(area))
        self.play(FadeOut(VGroup(xb, xl, dxl)), FadeOut(el))
        self.remove(el, xb, xl, dxl)
        grp = VGroup(rod, axis, Cl, ends, ax, curve, cl, area)
        self.play(grp.animate.scale(0.6).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3), integ.animate.to_edge(UP, buff=0.9).shift(RIGHT * 2.4))
        work = VGroup(
            M(r"= \frac{M}{L}\left[\frac{x^{3}}{3}\right]_{-L/2}^{+L/2}", size=42),
            M(r"= \frac{M}{3L}\left(\frac{L^{3}}{8} + \frac{L^{3}}{8}\right)", size=42),
            M(r"I_C = \frac{ML^{2}}{12}", size=58, color=C_I),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(integ, DOWN, buff=0.4).align_to(integ, LEFT).shift(RIGHT * 0.4)
        with self.say("Integrate x squared to get x cubed over three. Put in the limits: each end gives L cubed over eight, and the two halves add. Simplify, and the moment of inertia about the centre is M L squared over twelve."):
            self.play(Write(work[0]))
            self.play(Write(work[1]))
            self.sfx("impact", gain=-14)
            self.play(Write(work[2]))
            self.play(Circumscribe(work[2], color=C_I))
        self.play(FadeOut(VGroup(integ, work[0], work[1])), work[2].animate.to_edge(UP, buff=0.9).shift(RIGHT * 2.2))
        area2 = ax.get_area(curve, x_range=[0, 3], color=th.CORAL, opacity=0.0)
        with self.say("Now move the axis to one end. The same rod, but every element is now further from the axis, so the area must grow."):
            self.play(axis.animate.move_to(rod.get_left() + RIGHT * 0.0), Cl.animate.next_to(rod.get_left(), UP, buff=0.5))
            shifted = ax.plot(lambda x: (x + 3) ** 2 / 4.0, x_range=[-3, 3], color=th.CORAL, stroke_width=4)
            area3 = ax.get_area(shifted, x_range=[-3, 3], color=th.CORAL, opacity=0.35)
            self.play(Transform(curve, shifted), Transform(area, area3), FadeOut(cl))
        endw = VGroup(
            M(r"I_A = \int_{0}^{L} x^{2}\frac{M}{L}\,dx = \frac{ML^{2}}{3}", size=42, color=th.CORAL),
            M(r"\text{check: } I_C + M\left(\tfrac{L}{2}\right)^{2} = \frac{ML^{2}}{12} + \frac{ML^{2}}{4} = \frac{ML^{2}}{3}\ \checkmark", size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        endw.scale_to_fit_width(min(endw.width, 7.4)).next_to(work[2], DOWN, buff=0.5).to_edge(RIGHT, buff=0.45)
        with self.say("Integrating from zero to L gives M L squared over three, four times bigger. And we can check it with the parallel axis theorem: the end is L by two from the centre, so I c plus M times L by two, squared, is M L squared over twelve plus M L squared over four, which is M L squared over three. It matches."):
            self.play(Write(endw[0]))
            self.play(Write(endw[1]))
        self.wait(0.5)
        self.play(FadeOut(VGroup(grp, curve, area, work[2], endw)))
        self.quiz("The moment of inertia of a uniform rod (mass M, length L) about an axis through one end, perpendicular to it, is",
                  [M(r"ML^{2}/12", size=36), M(r"ML^{2}/3", size=36), M(r"ML^{2}/2", size=36), M(r"ML^{2}", size=36)], 1,
                  "Quick check, straight from past papers. A uniform rod, axis through one end. Which is it? Pause and think.",
                  "It is B, M L squared over three. One twelfth is about the centre. Moving the axis to the end adds M times L by two squared.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        hinge = np.array([-4.5, 0.6, 0])
        Ld = 5.0
        ang = ValueTracker(0)
        door = always_redraw(lambda: Rectangle(width=Ld, height=0.22, fill_color="#8B5E3C", fill_opacity=1, stroke_color="#C49A6C", stroke_width=2)
                             .move_to(hinge + RIGHT * Ld / 2).rotate(ang.get_value(), about_point=hinge))
        wall = VGroup(Line(hinge + DOWN * 0.3 + LEFT * 1.2, hinge + DOWN * 0.3 + LEFT * 0.05, color=th.MUTED, stroke_width=8))
        hd = Dot(hinge, radius=0.1, color=WHITE)
        hl = T("hinge (axis)", size=22, color=th.MUTED).next_to(hd, DOWN, buff=0.4)
        lab = T("A door, seen from above", size=26, color=th.MUTED).to_edge(UP, buff=0.9)
        with self.say("Why is a door handle always fixed at the edge, far from the hinge? Let us look at a door from above, and push it in different places with the same force."):
            self.play(FadeIn(lab), Create(wall), FadeIn(hd), FadeIn(hl))
            self.add(door)
            self.play(FadeIn(door))
        p_near = hinge + RIGHT * 1.0 + DOWN * 1.3
        f1 = Arrow(p_near, p_near + UP * 1.1, buff=0, color=C_TAU, stroke_width=6)
        with self.say("Push near the hinge, and the door barely turns."):
            self.play(GrowArrow(f1))
            self.play(ang.animate.set_value(0.12), run_time=2.0, rate_func=rate_functions.ease_out_quad)
        self.play(FadeOut(f1), ang.animate.set_value(0), run_time=0.6)
        p_far = hinge + RIGHT * 4.8 + DOWN * 1.3
        f2 = Arrow(p_far, p_far + UP * 1.1, buff=0, color=C_TAU, stroke_width=6)
        with self.say("Push at the edge with the same force, and it swings open easily. The turning effect of a force depends on where you apply it, not only on how hard you push."):
            self.play(GrowArrow(f2))
            self.play(ang.animate.set_value(0.9), FadeOut(f2), run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
        self.play(ang.animate.set_value(0), run_time=0.8)
        self.play(FadeOut(VGroup(lab, wall, hd, hl)), FadeOut(door))
        self.remove(door)
        O = np.array([-4.2, -1.2, 0])
        A = np.array([0.0, 0.2, 0])
        phi = ValueTracker(1.1)
        body = Polygon([-5.4, -2.6, 0], [-4.6, 0.4, 0], [-1.2, 1.4, 0], [1.0, 0.6, 0], [0.7, -0.9, 0], [-2.6, -2.5, 0],
                       fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3)
        od = Dot(O, color=WHITE, radius=0.09)
        ol = M("O", size=30, color=th.MUTED).next_to(od, DL, buff=0.05)
        rvec = Arrow(O, A, buff=0, color=C_R, stroke_width=5)
        rl = M(r"\vec r", size=36, color=C_R).next_to(rvec.get_center(), UP, buff=0.15)
        rdir = (A - O) / np.linalg.norm(A - O)
        pdir = np.array([-rdir[1], rdir[0], 0])

        def fdir():
            a = phi.get_value()
            return np.cos(a) * rdir + np.sin(a) * pdir
        F = always_redraw(lambda: Arrow(A, A + 2.3 * fdir(), buff=0, color=C_TAU, stroke_width=6))
        Fl = always_redraw(lambda: M(r"\vec F", size=36, color=C_TAU).next_to(A + 2.3 * fdir(), UR, buff=0.05))
        loa = always_redraw(lambda: DashedLine(A - 4.2 * fdir(), A + 3.4 * fdir(), color=th.FAINT, stroke_width=2))

        def foot():
            d = fdir()
            return A + np.dot(O - A, d) * d
        perp = always_redraw(lambda: Line(O, foot(), color=th.SKY, stroke_width=5))
        pl = always_redraw(lambda: M(r"d = r\sin\phi", size=32, color=th.SKY).next_to(Line(O, foot()).get_center(), DOWN, buff=0.3))
        arc = always_redraw(lambda: Arc(radius=0.55, start_angle=np.arctan2(rdir[1], rdir[0]), angle=phi.get_value(), arc_center=A, color=th.AMBER, stroke_width=4))
        phl = always_redraw(lambda: M(r"\phi", size=32, color=th.AMBER).move_to(A + 0.85 * np.array([np.cos(np.arctan2(rdir[1], rdir[0]) + phi.get_value() / 2), np.sin(np.arctan2(rdir[1], rdir[0]) + phi.get_value() / 2), 0])))
        with self.say("Now the general picture. A body can turn about an axis through O. A force F acts at a point whose position from the axis is the vector r. The angle between r and F is phi."):
            self.play(DrawBorderThenFill(body), FadeIn(od), FadeIn(ol))
            self.play(GrowArrow(rvec), FadeIn(rl))
            self.add(loa, F, Fl, arc, phl)
            self.play(FadeIn(F), FadeIn(Fl), FadeIn(arc), FadeIn(phl), FadeIn(loa))
        Fpar = always_redraw(lambda: DashedLine(A, A + 2.3 * np.cos(phi.get_value()) * rdir, color=th.MUTED, stroke_width=3))
        Fper = always_redraw(lambda: Arrow(A, A + 2.3 * np.sin(phi.get_value()) * pdir, buff=0, color=th.TEAL, stroke_width=5))
        Fperl = always_redraw(lambda: M(r"F\sin\phi", size=30, color=th.TEAL).next_to(A + 2.3 * np.sin(phi.get_value()) * pdir, LEFT, buff=0.1))
        with self.say("Split the force into two parts. The part along r just pulls on the axis, and does nothing to turn the body. Only the perpendicular part, F sine phi, turns it."):
            self.add(Fpar, Fper, Fperl)
            self.play(FadeIn(Fpar), FadeIn(Fper), FadeIn(Fperl))
        eq = M(r"\tau", r"=", r"r", r"F", r"\sin\phi", size=64).move_to([4.3, 2.2, 0])
        eq[0].set_color(C_TAU)
        with self.say("So the torque is r times F sine phi."):
            self.play(Write(eq))
        with self.say("Read it another way: F times r sine phi. And r sine phi is the perpendicular distance from the axis to the line of action of the force. We call it the moment arm."):
            self.add(perp, pl)
            self.play(Create(perp), FadeIn(pl))
        eq2 = M(r"\tau = F \times d", size=48).next_to(eq, DOWN, buff=0.4)
        with self.say("Watch what happens as the angle changes. At ninety degrees the moment arm is longest and the torque is greatest. Push straight along r, and the moment arm shrinks to zero. No torque at all."):
            self.play(Write(eq2))
            self.play(phi.animate.set_value(PI / 2), run_time=2.0)
            self.play(phi.animate.set_value(0.08), run_time=2.5)
            self.play(phi.animate.set_value(1.2), run_time=1.5)
        eq3 = M(r"\vec\tau = \vec r \times \vec F", size=44, color=th.BODY).next_to(eq2, DOWN, buff=0.4)
        u3 = T("unit: N m", size=24, color=th.MUTED).next_to(eq3, DOWN, buff=0.2)
        with self.say("As a vector, torque is r cross F, and its unit is the newton metre."):
            self.play(Write(eq3), FadeIn(u3))
        self.play(FadeOut(VGroup(body, od, ol, rvec, rl, eq, eq2, eq3, u3)), *[FadeOut(m) for m in (F, Fl, loa, perp, pl, arc, phl, Fpar, Fper, Fperl)])
        self.remove(F, Fl, loa, perp, pl, arc, phl, Fpar, Fper, Fperl)
        self.tau_ialpha()
        self.coin_rod()

    def tau_ialpha(self):
        lines = VGroup(
            M(r"F_i = m_i\,a_{t,i} = m_i r_i\,\alpha", size=44),
            M(r"\tau_i = F_i\,r_i = m_i r_i^{2}\,\alpha", size=44),
            M(r"\tau = \sum \tau_i = \Big(\sum m_i r_i^{2}\Big)\alpha", size=44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 0.6)
        with self.say("Now the most important result of the unit. Take one particle of the body, mass m i, at distance r i. Newton's second law says the tangential force on it is m i times its tangential acceleration, which is m i r i alpha. Every particle of a rigid body shares the same alpha."):
            self.play(Write(lines[0]))
        with self.say("The torque of that force is the force times r i, so m i r i squared alpha."):
            self.play(Write(lines[1]))
        with self.say("Add up the torques on all the particles. The internal forces cancel in pairs by Newton's third law, and alpha comes out of the sum."):
            self.play(Write(lines[2]))
        final = M(r"\tau", r"=", r"I", r"\alpha", size=96).next_to(lines, DOWN, buff=0.6)
        final[0].set_color(C_TAU)
        final[2].set_color(C_I)
        final[3].set_color(C_A)
        fma = M(r"\longleftrightarrow\ \ F = ma", size=48, color=th.MUTED).next_to(final, RIGHT, buff=0.6)
        with self.say("And there it is. Torque equals I alpha. The rotational form of F equals m a. Force becomes torque, mass becomes moment of inertia, acceleration becomes angular acceleration. Our dictionary, once again."):
            self.sfx("impact", gain=-10)
            self.play(Write(final))
            self.play(FadeIn(fma, shift=LEFT * 0.2))
            self.play(Circumscribe(final, color=C_TAU))
        self.play(FadeOut(VGroup(lines, final, fma)))

    def coin_rod(self):
        head = T("A surprising result", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        hinge = np.array([-3.6, 1.6, 0])
        Ls = 5.0
        g_scene = 4.0
        sim_t = np.linspace(0, 1.4, 1401)
        th_arr = np.zeros_like(sim_t)
        om = 0.0
        dt = sim_t[1] - sim_t[0]
        for i in range(1, len(sim_t)):
            a = 1.5 * g_scene / Ls * np.cos(th_arr[i - 1])
            om += a * dt
            th_arr[i] = min(PI / 2, th_arr[i - 1] + om * dt)
        T_ = ValueTracker(0)

        def theta():
            return float(np.interp(T_.get_value(), sim_t, th_arr))
        rod = always_redraw(lambda: Rectangle(width=Ls, height=0.16, fill_color=th.AMBER, fill_opacity=1, stroke_width=0)
                            .move_to(hinge + RIGHT * Ls / 2).rotate(-theta(), about_point=hinge))
        hd = Dot(hinge, radius=0.12, color=WHITE)
        stand = Line(hinge + DOWN * 0.1, hinge + DOWN * 4.0, color=th.MUTED, stroke_width=6)
        coin0 = hinge + RIGHT * (Ls - 0.15) + UP * 0.18
        coin = always_redraw(lambda: Circle(radius=0.15, fill_color="#E8C547", fill_opacity=1, stroke_color="#fff3b0", stroke_width=2)
                             .move_to(coin0 + DOWN * 0.5 * g_scene * T_.get_value() ** 2))
        with self.say("Here is a beautiful consequence. A uniform rod, mass two kilograms, length one metre, is hinged at one end and held horizontal. A coin rests on its free end. We let go. Does the coin stay on the rod as it swings down?"):
            self.play(FadeIn(head), Create(stand), FadeIn(hd))
            self.add(rod, coin)
            self.play(FadeIn(rod), FadeIn(coin))
        self.sfx("whoosh", gain=-12)
        self.play(T_.animate.set_value(0.75), run_time=3.0, rate_func=linear)
        gap = T("The rod falls away from the coin!", size=30, color=th.CORAL, weight="SEMIBOLD").to_edge(DOWN, buff=0.6)
        with self.say("Watch closely. The rod's free end drops faster than the coin, which is in free fall. The coin is left behind, floating above the rod. How can anything fall faster than free fall? Let us calculate."):
            self.play(FadeIn(gap))
        self.play(FadeOut(gap), FadeOut(head))
        self.remove(rod, coin)
        T_.set_value(0)
        rod2 = rod.copy()
        coin2 = coin.copy()
        self.play(FadeOut(rod2), FadeOut(coin2), FadeOut(stand), FadeOut(hd), run_time=0.3)
        hinge2 = np.array([-5.2, 1.8, 0])
        rod3 = Rectangle(width=3.6, height=0.14, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to(hinge2 + RIGHT * 1.8)
        hd3 = Dot(hinge2, radius=0.1, color=WHITE)
        wt = Arrow(hinge2 + RIGHT * 1.8, hinge2 + RIGHT * 1.8 + DOWN * 1.4, buff=0, color=th.CORAL, stroke_width=5)
        wl = M("Mg", size=32, color=th.CORAL).next_to(wt, RIGHT, buff=0.1)
        steps = VGroup(
            M(r"\tau = Mg\frac{L}{2} = 2 \times 9.8 \times 0.5 = 9.8\ \text{N m}", size=38),
            M(r"I = \frac{ML^{2}}{3} = \frac{2 \times 1^{2}}{3} = 0.667\ \text{kg m}^{2}", size=38),
            M(r"\alpha = \frac{\tau}{I} = \frac{9.8}{0.667} = 14.7\ \text{rad s}^{-2}", size=38),
            M(r"a_{\text{end}} = L\alpha = 14.7\ \text{m s}^{-2}\ >\ g", size=44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(RIGHT * 1.6 + DOWN * 0.3)
        steps[2].set_color(C_A)
        steps[3].set_color(th.CORAL)
        with self.say("The weight acts at the centre of the rod, half a metre from the hinge. So the torque is M g times L by two, which is nine point eight newton metres."):
            self.play(FadeIn(rod3), FadeIn(hd3), GrowArrow(wt), FadeIn(wl))
            self.play(Write(steps[0]))
        with self.say("About the end, the moment of inertia is M L squared over three, which is zero point six six seven."):
            self.play(Write(steps[1]))
        with self.say("Torque equals I alpha, so alpha is nine point eight divided by zero point six six seven: fourteen point seven radians per second squared."):
            self.play(Write(steps[2]))
        with self.say("The free end is one metre from the hinge, so its acceleration is L alpha: fourteen point seven metres per second squared. That is greater than g. The end of the rod really does accelerate faster than a freely falling coin, so the coin is left behind."):
            self.play(Write(steps[3]))
            self.sfx("impact", gain=-12)
            self.play(Circumscribe(steps[3], color=th.CORAL))
        self.wait(0.5)
        self.play(FadeOut(VGroup(rod3, hd3, wt, wl, steps)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        O = LEFT * 3.4
        R = 2.0
        ang = ValueTracker(0)
        disc = always_redraw(lambda: VGroup(Circle(radius=R, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=3),
                                            Line(ORIGIN, RIGHT * R, color=th.FAINT, stroke_width=3)).move_to(O).rotate(ang.get_value(), about_point=O))
        P = always_redraw(lambda: Dot(O + R * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]), color=th.AMBER, radius=0.1))
        Fv = always_redraw(lambda: Arrow(O + R * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]),
                                         O + R * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0]) + 1.3 * np.array([-np.sin(ang.get_value()), np.cos(ang.get_value()), 0]),
                                         buff=0, color=C_TAU, stroke_width=5))
        trail = always_redraw(lambda: Arc(radius=R, start_angle=0, angle=max(1e-3, ang.get_value()), arc_center=O, color=th.AMBER, stroke_width=6))
        lines = VGroup(
            M(r"dW = F\,ds", size=46),
            M(r"= \frac{\tau}{r}\,(r\,d\theta)", size=46),
            M(r"dW = \tau\,d\theta", size=52, color=C_TAU),
            M(r"W = \tau\,\theta \quad (\text{constant } \tau)", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(RIGHT * 3.0 + UP * 0.5)
        with self.say("When a torque turns a body, it does work. A tangential force F at the rim, distance r from the axis, pushes through a small arc d s equal to r d theta."):
            self.add(disc, trail, P, Fv)
            self.play(FadeIn(disc), FadeIn(P), FadeIn(Fv))
            self.play(ang.animate.set_value(1.2), run_time=2.5)
        with self.say("Work is force times distance. Write F as tau over r, and d s as r d theta. The r's cancel, leaving d W equals tau d theta. For a constant torque, W equals tau theta: torque times angle, just like force times distance."):
            self.play(Write(lines[0]))
            self.play(Write(lines[1]))
            self.play(Write(lines[2]))
            self.play(Write(lines[3]))
            self.play(ang.animate.set_value(2.4), run_time=2)
        pw = M(r"P = \frac{dW}{dt} = \tau\frac{d\theta}{dt} = \tau\,\omega", size=50).next_to(lines, DOWN, buff=0.5).align_to(lines, LEFT)
        pw2 = M(r"\longleftrightarrow\ P = Fv", size=40, color=th.MUTED).next_to(pw, DOWN, buff=0.25).align_to(pw, LEFT)
        with self.say("Power is the rate of doing work. Divide by d t: power equals tau omega, the exact twin of P equals F v."):
            self.play(Write(pw), FadeIn(pw2))
            self.play(ang.animate.set_value(5.0), run_time=2.5, rate_func=linear)
        self.play(FadeOut(VGroup(lines, pw, pw2)))
        wet = VGroup(
            M(r"W = \int \tau\,d\theta = \int_{\omega_1}^{\omega_2} I\omega\,d\omega", size=44),
            M(r"W = \tfrac{1}{2}I\omega_2^{2} - \tfrac{1}{2}I\omega_1^{2}", size=54, color=th.AMBER),
        ).arrange(DOWN, buff=0.5).move_to(RIGHT * 3.0)
        lab = T("work–energy theorem for rotation", size=26, color=th.AMBER).next_to(wet, UP, buff=0.4)
        with self.say("And because torque equals I alpha, the total work done equals the change in rotational kinetic energy: half I omega two squared minus half I omega one squared. This is the work energy theorem for rotation."):
            self.play(FadeIn(lab), Write(wet[0]))
            self.play(Write(wet[1]))
            self.play(ang.animate.set_value(8.0), run_time=2.0)
        self.play(FadeOut(VGroup(wet, lab)), FadeOut(disc), FadeOut(P), FadeOut(Fv), FadeOut(trail))
        self.remove(disc, P, Fv, trail)
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("An electric motor at a rice mill in Jhapa delivers a constant torque of 25 N m while running at 1500 rev/min. Find its power output and the work done in one minute.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"\omega = \frac{2\pi \times 1500}{60} = 50\pi \approx 157.1\ \text{rad s}^{-1}", size=42),
            M(r"P = \tau\omega = 25 \times 157.1 \approx 3927\ \text{W} \approx 3.93\ \text{kW}", size=42),
            M(r"W = Pt = 3927 \times 60 \approx 2.36 \times 10^{5}\ \text{J}", size=42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(prob, DOWN, buff=0.7).align_to(prob, LEFT)
        steps[1].set_color(th.AMBER)
        with self.say("Let us try it on a rice mill in Jhapa. Its motor delivers a constant torque of twenty five newton metres while running at fifteen hundred revolutions per minute. Find its power, and the work it does in one minute."):
            self.play(FadeIn(head), FadeIn(prob))
        with self.say("Radians first. Fifteen hundred r p m is fifty pi, about one hundred fifty seven radians per second."):
            self.play(Write(steps[0]))
        with self.say("Power equals tau omega: twenty five times one fifty seven point one, about three thousand nine hundred twenty seven watts, nearly four kilowatts."):
            self.play(Write(steps[1]))
        with self.say("In sixty seconds, the work done is power times time: about two point three six times ten to the five joules."):
            self.play(Write(steps[2]))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        d1 = M(r"L", r"=", r"I", r"\omega", size=80).move_to(UP * 1.6)
        d1[0].set_color(C_L)
        d1[2].set_color(C_I)
        d1[3].set_color(C_W)
        pl = M(r"\longleftrightarrow\ p = mv", size=44, color=th.MUTED).next_to(d1, RIGHT, buff=0.5)
        un = T("unit: kg m² s⁻¹  (or J s)", size=24, color=th.MUTED).next_to(d1, DOWN, buff=0.3)
        with self.say("The last piece of the dictionary: angular momentum. For a rigid body rotating about a fixed axis, L equals I omega, the twin of p equals m v. For a single particle, it is r times p times sine phi."):
            self.play(Write(d1), FadeIn(pl))
            self.play(FadeIn(un))
        d2 = M(r"\frac{dL}{dt} = I\frac{d\omega}{dt} = I\alpha = \tau", size=56).next_to(un, DOWN, buff=0.6)
        with self.say("Differentiate it. The rate of change of angular momentum is I alpha, which is the torque. So torque is the rate of change of angular momentum, just as force is the rate of change of momentum."):
            self.play(Write(d2))
        cons = self.callout("key", M(r"\tau_{\text{ext}} = 0 \;\Rightarrow\; L = I\omega = \text{constant} \;\Rightarrow\; I_1\omega_1 = I_2\omega_2", size=44, color=th.INK), width=11)
        cons.to_edge(DOWN, buff=0.7)
        with self.say("And here is one of the great conservation laws of physics. If no external torque acts, d L by d t is zero, so L stays constant. I one omega one equals I two omega two. If a body makes its moment of inertia smaller, it must spin faster."):
            self.play(FadeIn(cons, shift=UP * 0.3))
        self.play(FadeOut(VGroup(d1, pl, un, d2, cons)))
        self.skater()
        self.example_stool()
        self.applications()
        self.quiz("A disc (I = 2 kg m²) spinning at 10 rad/s is suddenly coupled to a stationary coaxial disc (I = 3 kg m²). What is the common angular velocity?",
                  [M(r"2\ \text{rad s}^{-1}", size=36), M(r"4\ \text{rad s}^{-1}", size=36), M(r"5\ \text{rad s}^{-1}", size=36), M(r"10\ \text{rad s}^{-1}", size=36)], 1,
                  "Try this one from the five mark questions. A spinning disc is suddenly coupled to a stationary one. What is the common angular velocity? Pause and think.",
                  "B, four radians per second. No external torque, so angular momentum is conserved: two times ten equals two plus three, times omega. Omega is twenty over five, which is four. And kinetic energy falls from one hundred joules to forty. The missing sixty joules become heat in the friction between the discs.")

    def skater(self):
        C = np.array([-3.0, -0.3, 0])
        arm = ValueTracker(2.3)
        ang = ValueTracker(0)
        I0 = 1.0 + 2 * 0.9 * 2.3 ** 2

        def Ival():
            return 1.0 + 2 * 0.9 * arm.get_value() ** 2

        def body():
            a = ang.get_value()
            r = arm.get_value()
            d = np.array([np.cos(a), np.sin(a), 0])
            torso = Circle(radius=0.65, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=th.BODY, stroke_width=3).move_to(C)
            head = Circle(radius=0.32, fill_color="#E9B48A", fill_opacity=1, stroke_width=0).move_to(C + 0.1 * d)
            arms = Line(C - d * r, C + d * r, color="#E9B48A", stroke_width=10)
            m1 = Circle(radius=0.25, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to(C + d * r)
            m2 = m1.copy().move_to(C - d * r)
            return VGroup(arms, torso, head, m1, m2)
        sk = always_redraw(body)
        lab = T("A skater, seen from above", size=26, color=th.MUTED).to_edge(UP, buff=0.9).shift(LEFT * 3.0)
        L0 = I0 * 1.0

        def meters():
            Iv = Ival()
            w = L0 / Iv
            KE = 0.5 * Iv * w * w
            items = [("I", Iv / I0, C_I), ("ω", w / (L0 / (1.0 + 2 * 0.9 * 0.55 ** 2)), C_W), ("L = Iω", 1.0, C_L), ("KE", KE / (0.5 * L0 * L0 / (1.0 + 2 * 0.9 * 0.55 ** 2)), th.AMBER)]
            g = VGroup()
            for i, (nm, frac, col) in enumerate(items):
                x = 1.6 + i * 1.45
                base = np.array([x, -2.6, 0])
                track = Rectangle(width=0.7, height=4.2, stroke_color=th.FAINT, stroke_width=2).move_to(base, aligned_edge=DOWN)
                bar = Rectangle(width=0.7, height=max(0.02, 4.2 * min(frac, 1.0)), fill_color=col, fill_opacity=0.9, stroke_width=0).move_to(base, aligned_edge=DOWN)
                t = T(nm, size=24, color=col, weight="SEMIBOLD").next_to(track, DOWN, buff=0.15)
                g.add(track, bar, t)
            return g
        mt = always_redraw(meters)

        def upd(m, dt):
            ang.increment_value(dt * 1.2 * (L0 / Ival()))
        ticker = Mobject()
        ticker.add_updater(upd)
        with self.say("Watch a skater, seen from above, spinning with arms stretched out and a weight in each hand. Out here, the moment of inertia is large, and the spin is slow."):
            self.add(ticker, sk, mt)
            self.play(FadeIn(lab), FadeIn(sk), FadeIn(mt))
            self.wait(2.5)
        with self.say("Now she pulls her arms in. No outside torque acts, so angular momentum must stay the same. Her moment of inertia drops, so her angular velocity shoots up. Look at the bars. I falls. Omega rises. L does not change at all."):
            self.play(arm.animate.set_value(0.55), run_time=3.0, rate_func=smooth)
            self.wait(3.0)
        with self.say("But look at the last bar. Her kinetic energy went up! Kinetic energy is L squared over two I, and I got smaller. Angular momentum is conserved, but kinetic energy is not. The extra energy comes from the work her muscles do, pulling the weights inward."):
            self.play(Indicate(mt, color=th.AMBER, scale_factor=1.0), run_time=1.5)
            self.wait(1.0)
        with self.say("Stretch the arms out again, and she slows right back down."):
            self.play(arm.animate.set_value(2.3), run_time=3.0, rate_func=smooth)
        self.play(FadeOut(lab), FadeOut(sk), FadeOut(mt))
        self.remove(sk, mt, ticker)

    def example_stool(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A student on a frictionless rotating stool holds weights at arm's length: I = 6 kg m², ω = 2 rad/s. Pulling the arms in makes I = 2 kg m². Find the new ω and the change in kinetic energy.", width=12.2, size=27, color=th.INK)
        prob.next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            M(r"I_1\omega_1 = I_2\omega_2 \;\Rightarrow\; 6 \times 2 = 2\,\omega_2 \;\Rightarrow\; \omega_2 = 6\ \text{rad s}^{-1}", size=40),
            M(r"E_1 = \tfrac{1}{2}(6)(2)^{2} = 12\ \text{J}", size=40),
            M(r"E_2 = \tfrac{1}{2}(2)(6)^{2} = 36\ \text{J}", size=40),
            M(r"\Delta E = +24\ \text{J}\ \ (\text{from the student's muscles})", size=40, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(prob, DOWN, buff=0.6).align_to(prob, LEFT)
        with self.say("Let us put numbers on it. A student sits on a frictionless stool, holding weights. The moment of inertia is six, and the stool turns at two radians per second. Pulling the arms in drops I to two. Find the new angular velocity and the change in kinetic energy."):
            self.play(FadeIn(head), FadeIn(prob))
        with self.say("Conserve angular momentum: six times two equals two times omega two, so omega two is six radians per second. Three times faster."):
            self.play(Write(steps[0]))
        with self.say("The energy before is half times six times two squared, twelve joules. After, half times two times six squared, thirty six joules."):
            self.play(Write(steps[1]))
            self.play(Write(steps[2]))
        with self.say("The kinetic energy rose by twenty four joules, all supplied by the student's own muscles."):
            self.play(Write(steps[3]))
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, prob, steps)))

    def applications(self):
        title = T("Conservation of L, everywhere", size=38, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        items = [
            ("Diver", "Tucks in to somersault fast, stretches out to slow down before the water."),
            ("Planets", "Gravity points at the Sun: zero torque. So a planet speeds up near the Sun (Kepler's second law)."),
            ("Spinning top", "Its L points along the axis. Tipping it would change L, so it resists."),
        ]
        cards = VGroup()
        for i, (h, b) in enumerate(items):
            box = self.panel(3.9, 3.6)
            hh = T(h, size=30, color=[th.SKY, th.AMBER, th.MINT][i], weight="BOLD")
            bb = para(b, width=3.3, size=22, color=th.BODY)
            VGroup(hh, bb).arrange(DOWN, buff=0.3).move_to(box)
            cards.add(VGroup(box, hh, bb))
        cards.arrange(RIGHT, buff=0.35).next_to(title, DOWN, buff=0.5)
        with self.say("You can see this law everywhere. A diver tucks in tight to somersault quickly, then stretches out to slow the spin before entering the water. A planet moves faster when it is closer to the Sun, because gravity pulls straight towards the Sun and exerts no torque. That is Kepler's second law. And a spinning top resists falling over, because tipping it would change the direction of its angular momentum.") as v:
            self.play(FadeIn(title))
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.3), run_time=0.6)
                self.hold(v.dur / 3 - 1.0)
        self.play(FadeOut(VGroup(title, cards)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"\omega = \omega_0 + \alpha t,\ \ \theta = \omega_0 t + \tfrac12\alpha t^{2},\ \ \omega^{2} = \omega_0^{2} + 2\alpha\theta", size=34),
            M(r"v = r\omega,\ \ a_t = r\alpha,\ \ a_c = r\omega^{2}\quad(\text{radians!})", size=34),
            M(r"E_k = \tfrac12 I\omega^{2},\ \ I = \sum m r^{2},\ \ I = Mk^{2}", size=34),
            M(r"\text{rod: } \tfrac{1}{12}ML^{2}\ (\text{centre}),\ \ \tfrac13 ML^{2}\ (\text{end});\ \ I = I_{cm} + Md^{2}", size=34),
            M(r"\tau = rF\sin\phi = I\alpha", size=34),
            M(r"W = \tau\theta,\ \ P = \tau\omega,\ \ W = \Delta(\tfrac12 I\omega^{2})", size=34),
            M(r"L = I\omega,\ \ \tau = \tfrac{dL}{dt};\ \ \tau = 0 \Rightarrow I_1\omega_1 = I_2\omega_2", size=34),
        ], "Let us recap. The equations of angular motion mirror the linear ones. v equals r omega links the two worlds, in radians only. Rotational energy is half I omega squared, where I is the sum of m r squared. A rod has M L squared over twelve about its centre and over three about its end. Torque is r F sine phi, and equals I alpha. Work is tau theta and power is tau omega. And angular momentum, I omega, is conserved when no external torque acts.")
        self.outro("That is rotational dynamics. Next time, we set things swinging, with periodic motion. Keep practising, and see you in the next lesson on NEBians.")
