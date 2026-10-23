import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import clock, curve, example, neby_in, neby_out, readout  # noqa: E402

C_W, C_R, C_L, C_G = th.SKY, th.AMBER, th.MINT, "#2a3a6a"
GLASS = "#22406e"


def U(a):
    return np.array([np.cos(a), np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 10
    TITLE = "Nature and Propagation of Light"
    SUBTITLE = "Wavefronts, Huygens and why light bends"
    SECTIONS = ["Wavefronts and rays", "Huygens' principle", "Reflection by wave theory", "Refraction: Snell's law",
                "Frequency, wavelength, optical path", "Waves versus corpuscles"]
    NEXT = "Unit 11 · Interference"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ Huygens construction at a plane surface
    def construction(self, i_deg=50, n=None, ym=-1.4, xA=-3.6, W=3.4, k=7, show_wavelets=True):
        """Returns (u tracker, mobjects dict) animating a plane wavefront AB meeting a surface y = ym.
        n=None: mirror (reflection). Otherwise a denser medium of index n below the surface (refraction)."""
        i = np.radians(i_deg)
        A = np.array([xA, ym, 0])
        d = np.array([np.sin(i), -np.cos(i), 0])
        w = np.array([np.cos(i), np.sin(i), 0])
        B = A + W * w
        BC = W * np.tan(i)
        AC = W / np.cos(i)
        C = A + RIGHT * AC
        u = ValueTracker(0)
        if n is None:
            dr = np.array([np.sin(i), np.cos(i), 0])
            R = BC
        else:
            r = np.arcsin(np.sin(i) / n)
            dr = np.array([np.sin(r), -np.cos(r), 0])
            R = BC / n
        P = lambda: A + RIGHT * AC * u.get_value()
        inc = always_redraw(lambda: Line(P(), B + d * BC * u.get_value(), color=C_W, stroke_width=6))
        out = always_redraw(lambda: Line(P(), A + dr * R * u.get_value(), color=C_R if n is None else C_L, stroke_width=6) if u.get_value() > 0.01 else VGroup())
        fk = np.linspace(0, 1, k)

        def wl():
            g = VGroup()
            uu = u.get_value()
            for f in fk:
                rad = R * (uu - f)
                if rad <= 0.01:
                    continue
                start = 0 if n is None else PI
                g.add(Arc(radius=rad, start_angle=start, angle=PI, arc_center=A + RIGHT * AC * f, color=th.MUTED, stroke_width=2))
            return g
        wavelets = always_redraw(wl) if show_wavelets else VGroup()
        return u, dict(A=A, B=B, C=C, D=A + dr * R, d=d, dr=dr, inc=inc, out=out, wavelets=wavelets, BC=BC, AC=AC, R=R, i=i)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        bound = 0.0
        field = Rectangle(width=13.6, height=3.6, stroke_width=0, fill_color="#2f5a2a", fill_opacity=0.5).move_to([0, 1.8, 0])
        mud = Rectangle(width=13.6, height=3.6, stroke_width=0, fill_color="#5a4632", fill_opacity=0.6).move_to([0, -1.8, 0])
        lab = VGroup(T("grass: march fast", size=24, color=th.LIME).move_to([-4.6, 3.1, 0]), T("mud: march slowly", size=24, color=th.AMBER).move_to([-4.6, -3.1, 0]))
        a = np.radians(40)
        d = np.array([np.sin(a), -np.cos(a), 0])
        w = np.array([np.cos(a), np.sin(a), 0])
        v1, v2 = 1.6, 0.8
        n = 9
        starts = [np.array([-5.0, 2.6, 0]) + w * (j * 0.45) for j in range(n)]
        r = np.arcsin(np.sin(a) * v2 / v1)
        d2 = np.array([np.sin(r), -np.cos(r), 0])
        t = ValueTracker(0)

        def pos(s0):
            tb = (s0[1] - bound) / (v1 * np.cos(a))
            tt = t.get_value()
            if tt <= tb:
                return s0 + d * v1 * tt
            return s0 + d * v1 * tb + d2 * v2 * (tt - tb)
        row = always_redraw(lambda: VGroup(*[Dot(pos(s), radius=0.12, color=WHITE) for s in starts],
                                           VMobject(stroke_color=th.SKY, stroke_width=3).set_points_as_corners([pos(s) for s in starts])))
        with self.say("A line of students marches across a field in step, arm in arm. Their path crosses from firm grass into soft mud, at an angle."):
            self.play(FadeIn(field), FadeIn(mud), FadeIn(lab))
            self.add(row)
            self.play(FadeIn(row))
            self.play(t.animate.set_value(2.4), run_time=3.0, rate_func=linear)
        with self.say("The ones who reach the mud first slow down, while the others are still striding on the grass. So the whole line swings round, and marches off in a new direction, bent towards the boundary's normal."):
            self.play(t.animate.set_value(6.0), run_time=5.0, rate_func=linear)
        nb = neby_in(self, "think", corner=UR)
        q = para("Light bends at a glass surface too. Ray diagrams just say it does. But why? And which way?", width=8, size=30, color=th.AMBER).move_to([2.6, 0.9, 0])
        bg = BackgroundRectangle(q, color=th.BG, fill_opacity=0.85, buff=0.2)
        with self.say("Light does exactly this at the surface of glass or water. Ray diagrams tell you that it bends. Wave optics tells you why. And it rebuilds every law of reflection and refraction from one simple idea."):
            self.play(FadeIn(bg), FadeIn(q))
        self.play(FadeOut(VGroup(field, mud, lab, q, bg)), FadeOut(row))
        self.remove(row)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 10: the Nature and Propagation of Light. In this unit we replace the ray by the wavefront, meet Huygens' principle, and use it to prove the laws of reflection and refraction from scratch. Interference, diffraction and polarization in the next three units all stand on this geometry."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. Wavefronts and rays, Huygens' principle, reflection by wave theory, refraction and Snell's law, what happens to frequency and wavelength, the optical path, and finally the great contest between waves and corpuscles.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        t = clock(self, 1.0)
        S = np.array([-4.2, 0, 0])
        v, per = 1.2, 0.8

        def fronts():
            tt = t.get_value()
            g = VGroup()
            for k_ in range(12):
                r = v * ((tt % per) + k_ * per)
                if r > 0.05 and r < 9:
                    g.add(Circle(radius=r, stroke_color=C_W, stroke_width=3, stroke_opacity=max(0.15, 1 - r / 9)).move_to(S))
            return g
        fr = always_redraw(fronts)
        src = Dot(S, color=th.AMBER, radius=0.12)
        rays = VGroup(*[Arrow(S + 0.6 * U(a), S + 3.6 * U(a), buff=0, color=C_R, stroke_width=4, max_tip_length_to_length_ratio=0.1) for a in np.linspace(0, TAU, 8, endpoint=False)])
        defn = self.callout("key", "A wavefront is the locus of all points vibrating in the same phase. A ray is the normal to the wavefront, pointing the way the wave advances.", width=5.4, size=24)
        defn.move_to([3.6, 1.4, 0])
        with self.say("A point source of light sends out disturbances in all directions. At any instant, all the points the disturbance has just reached started vibrating at the same moment. So they vibrate in step."):
            self.add(fr)
            self.play(FadeIn(src), FadeIn(fr))
            self.wait(2)
        with self.say("The surface through all those points is a wavefront: the locus of points vibrating in the same phase. The perpendicular to a wavefront, in the direction the wave moves, is a ray. And the wavefront moves at the speed of the wave in that medium."):
            self.play(FadeIn(defn, shift=LEFT * 0.2))
            self.play(LaggedStart(*[GrowArrow(r) for r in rays], lag_ratio=0.1))
        self.play(FadeOut(VGroup(defn, rays, src)), FadeOut(fr))
        self.remove(fr, t)
        title = T("Three shapes of wavefront", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        cards = VGroup()
        specs = [("spherical", "point source", "amplitude ∝ 1/r"), ("cylindrical", "a long thin slit", "amplitude ∝ 1/√r"), ("plane", "a very distant source", "amplitude constant")]
        for k_, (nm, s_, a_) in enumerate(specs):
            box = self.panel(3.9, 3.9)
            c = box.get_center() + UP * 0.45
            if k_ == 0:
                pic = VGroup(Dot(c + LEFT * 1.1, color=th.AMBER), *[Arc(radius=r, start_angle=-0.9, angle=1.8, arc_center=c + LEFT * 1.1, color=C_W, stroke_width=3) for r in (0.5, 0.95, 1.4, 1.85)])
            elif k_ == 1:
                pic = VGroup(Line(c + LEFT * 1.1 + UP * 0.8, c + LEFT * 1.1 + DOWN * 0.8, color=th.AMBER, stroke_width=6),
                             *[RoundedRectangle(corner_radius=0.3 + 0.0, width=2 * r, height=1.6 + 2 * r * 0.2, color=C_W, stroke_width=3).move_to(c + LEFT * 1.1).set_opacity(0.8)
                               for r in (0.45, 0.9, 1.35)])
                pic[1:].set_fill(opacity=0)
            else:
                pic = VGroup(*[Line(c + RIGHT * x + UP * 0.9, c + RIGHT * x + DOWN * 0.9, color=C_W, stroke_width=3) for x in (-1.2, -0.6, 0, 0.6, 1.2)],
                             Arrow(c + LEFT * 1.4, c + RIGHT * 1.5, buff=0, color=C_R, stroke_width=3))
            txt = VGroup(T(nm, size=28, color=th.INK, weight="BOLD"), T(s_, size=22, color=th.BODY), T(a_, size=20, color=th.MUTED)).arrange(DOWN, buff=0.1).move_to(box.get_bottom() + UP * 0.8)
            cards.add(VGroup(box, pic, txt))
        cards.arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.35)
        with self.say("Near a point source, wavefronts are spheres. Near a long thin slit, they are cylinders. And very far from any source, a small patch of a huge sphere is indistinguishable from a flat plane. That is why sunlight reaches the Earth as plane wavefronts.") as v_:
            self.play(FadeIn(title))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.6)
                self.hold(v_.dur / 3 - 0.7)
        self.play(FadeOut(VGroup(title, cards)))
        lens = VGroup(Arc(radius=3.0, start_angle=-0.42, angle=0.84, arc_center=[-2.75, 0, 0], color=th.SKY, stroke_width=4),
                      Arc(radius=3.0, start_angle=PI - 0.42, angle=0.84, arc_center=[2.75, 0, 0], color=th.SKY, stroke_width=4))
        lens.add(Polygon(*[lens[0].point_from_proportion(a) for a in np.linspace(0, 1, 20)], *[lens[1].point_from_proportion(a) for a in np.linspace(0, 1, 20)],
                         stroke_width=0, fill_color=th.SKY, fill_opacity=0.15))
        F = np.array([3.4, 0, 0])
        tt = ValueTracker(0)

        def fronts2():
            g = VGroup()
            for k_ in range(5):
                x = -6.0 + ((tt.get_value() + k_ * 1.3) % 6.5)
                if x < 0:
                    g.add(Line([x, 1.3, 0], [x, -1.3, 0], color=C_W, stroke_width=3))
                else:
                    rr = F[0] - x
                    if rr > 0.08:
                        g.add(Arc(radius=rr, start_angle=PI - min(1.0, 1.3 / rr), angle=2 * min(1.0, 1.3 / rr), arc_center=F, color=C_W, stroke_width=3))
            return g
        f2 = always_redraw(fronts2)
        fd = VGroup(Dot(F, color=th.AMBER), T("focus", size=22, color=th.AMBER).next_to(F, DOWN, buff=0.15))
        with self.say("A converging lens reshapes wavefronts. Flat plane waves go in. The middle of each front is held back most by the thick glass, so the front comes out curved, as a sphere shrinking down onto the focus."):
            self.play(FadeIn(lens), FadeIn(fd))
            self.add(f2)
            self.play(tt.animate.set_value(13), run_time=7, rate_func=linear)
        self.play(FadeOut(VGroup(lens, fd)), FadeOut(f2))
        self.remove(f2)
        self.quiz("A wavefront is a surface on which all points have the same",
                  ["amplitude", "phase", "wavelength", "intensity"], 1,
                  "Quick check. A wavefront is a surface on which every point has the same what? Pause and think.",
                  "B, the same phase. That is the definition. The amplitude can differ along a wavefront, for example near the edge of a beam, but all the points on it are vibrating in step.")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        title = T("Huygens' principle (1678)", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        st = VGroup(T("1.  Every point on a wavefront is a source of secondary wavelets,", size=24, color=th.BODY),
                    T("     spreading forward at the wave speed v of that medium.", size=24, color=th.BODY),
                    T("2.  The new wavefront, after time t, is the forward envelope", size=24, color=th.BODY),
                    T("     (common tangent) of all those wavelets, each of radius vt.", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(title, DOWN, buff=0.3)
        with self.say("In sixteen seventy eight, Christiaan Huygens gave a rule for moving a wavefront forward. It has two parts. First, every point on a wavefront acts as a fresh source of secondary wavelets, which spread forward at the speed of the wave in that medium. Second, the new wavefront, a time t later, is the surface that touches all those wavelets: their forward envelope."):
            self.play(FadeIn(title))
            self.play(FadeIn(st[:2]))
            self.play(FadeIn(st[2:]))
        self.play(FadeOut(st))
        x0 = -4.6
        ys = np.linspace(-2.2, 1.6, 9)
        old = Line([x0, ys[0] - 0.2, 0], [x0, ys[-1] + 0.2, 0], color=C_W, stroke_width=6)
        pts = VGroup(*[Dot([x0, y, 0], radius=0.07, color=th.AMBER) for y in ys])
        rr = ValueTracker(0.01)
        arcs = always_redraw(lambda: VGroup(*[Arc(radius=rr.get_value(), start_angle=-PI / 2, angle=PI, arc_center=[x0, y, 0], color=th.MUTED, stroke_width=2) for y in ys]))
        new = always_redraw(lambda: Line([x0 + rr.get_value(), ys[0] - 0.2, 0], [x0 + rr.get_value(), ys[-1] + 0.2, 0], color=C_W, stroke_width=6))
        vt = always_redraw(lambda: VGroup(Line([x0, -2.75, 0], [x0 + rr.get_value(), -2.75, 0], color=th.AMBER, stroke_width=3), M("vt", size=28, color=th.AMBER).move_to([x0 + rr.get_value() / 2, -3.05, 0])))
        with self.say("Watch it work on a plane wavefront. Pick a row of points on it. Set your compass to v t, and strike an arc from each point."):
            self.play(Create(old), FadeIn(pts))
            self.add(arcs, vt)
            self.play(rr.animate.set_value(2.0), run_time=2.5)
        with self.say("The common tangent of all those arcs is the new wavefront: another plane, moved forward by v t."):
            self.add(new)
            self.play(Create(new))
        self.play(FadeOut(VGroup(old, pts)), FadeOut(arcs), FadeOut(new), FadeOut(vt))
        self.remove(arcs, new, vt)
        S = np.array([-3.0, -0.4, 0])
        R0 = 1.2
        angs = np.linspace(-1.1, 1.1, 9)
        oldc = Arc(radius=R0, start_angle=-1.25, angle=2.5, arc_center=S, color=C_W, stroke_width=6)
        pts = VGroup(*[Dot(S + R0 * U(a), radius=0.07, color=th.AMBER) for a in angs])
        rr.set_value(0.01)
        arcs = always_redraw(lambda: VGroup(*[Arc(radius=rr.get_value(), start_angle=a - PI / 2, angle=PI, arc_center=S + R0 * U(a), color=th.MUTED, stroke_width=2) for a in angs]))
        newc = always_redraw(lambda: Arc(radius=R0 + rr.get_value(), start_angle=-1.25, angle=2.5, arc_center=S, color=C_W, stroke_width=6))
        with self.say("A spherical wavefront works the same way. Wavelets of radius v t from every point, and their envelope is a bigger sphere, centred on the same source."):
            self.play(Create(oldc), FadeIn(pts), FadeIn(Dot(S, color=th.AMBER)))
            self.add(arcs)
            self.play(rr.animate.set_value(1.8), run_time=2.5)
            self.add(newc)
            self.play(Create(newc))
        self.clear_stage()
        self.remove(arcs, newc)
        self.obliquity()

    def obliquity(self):
        title = T("Why is there no backward wave?", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        C = np.array([-3.0, -0.4, 0])
        full = Circle(radius=1.8, stroke_color=th.MUTED, stroke_width=2).move_to(C)
        back = DashedLine(C + LEFT * 2.6 + UP * 2.0, C + LEFT * 2.6 + DOWN * 2.2, color=th.CORAL, stroke_width=3)
        bl = T("backward envelope?", size=22, color=th.CORAL).next_to(back, UP, buff=0.1)
        with self.say("There is a puzzle. Drawn honestly, each secondary wavelet is a complete sphere. So there should also be a backward envelope, a wave travelling back towards the source. We never see one."):
            self.play(FadeIn(title), Create(full), FadeIn(Dot(C, color=th.AMBER)))
            self.play(Create(back), FadeIn(bl))
        card = VGroup(*[]) if False else None
        cardioid = ParametricFunction(lambda s: C + 1.8 * 0.5 * (1 + np.cos(s)) * U(s), t_range=[0, TAU], color=th.AMBER, stroke_width=5)
        eq = M(r"K = \tfrac12(1 + \cos\theta)", size=46, color=th.AMBER).move_to([3.2, 1.0, 0])
        notes = VGroup(M(r"\theta = 0:\ K = 1\ \ (\text{straight ahead})", size=32), M(r"\theta = 180^{\circ}:\ K = 0\ \ (\text{straight back})", size=32)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq, DOWN, buff=0.4)
        with self.say("Huygens simply declared that the wavelets have no strength backwards. Later, Fresnel and Kirchhoff showed why. The amplitude of a wavelet depends on the angle theta from the forward direction, through the obliquity factor, K equals a half, one plus cos theta."):
            self.play(Create(cardioid), Write(eq))
        with self.say("Straight ahead, K is one. Straight backwards, it is zero. So only the forward envelope survives. In the exam, it is enough to say: secondary wavelets are effective only in the forward direction."):
            self.play(FadeIn(notes))
            self.play(FadeOut(back), FadeOut(bl))
        self.play(FadeOut(VGroup(title, full, cardioid, eq, notes)), *[FadeOut(m) for m in self.mobjects[3:] if isinstance(m, Dot)])
        self.tip("Wavelets are arcs, not arrows. Draw arcs of radius vt from points on the old wavefront and their common tangent; straight arrows from the wavefront earn no marks.",
                 "One drawing tip that saves marks. A secondary wavelet is a tiny spherical wave, not a ray. Draw arcs of radius v t from points on the old wavefront, and then their common tangent. Students who draw straight arrows instead lose the whole proof.", state="think")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        u, m = self.construction(i_deg=48, n=None)
        mirror = VGroup(Line([-6.0, -1.4, 0], [3.0, -1.4, 0], color=th.BODY, stroke_width=5),
                        *[Line([x, -1.4, 0], [x - 0.2, -1.65, 0], color=th.MUTED, stroke_width=2) for x in np.arange(-5.8, 3.0, 0.35)])
        A, B, C, D = m["A"], m["B"], m["C"], m["D"]
        la = VGroup(M("A", size=32).next_to(A, DL, buff=0.08), M("B", size=32).next_to(B, LEFT, buff=0.12))
        rays = VGroup(*[Arrow(p - m["d"] * 1.6, p, buff=0, color=C_W, stroke_width=3, max_tip_length_to_length_ratio=0.15) for p in (A, B)])
        with self.say("Now let us prove the laws of reflection. A plane wavefront A B travels towards a mirror, in a medium where light moves at speed c. Take the instant when end A has just touched the mirror. End B still has some way to go."):
            self.play(Create(mirror))
            self.play(GrowArrow(rays[0]), GrowArrow(rays[1]))
            self.add(m["inc"])
            self.play(FadeIn(m["inc"]), FadeIn(la))
        self.add(m["wavelets"], m["out"])
        with self.say("As the wavefront sweeps along the mirror, each point it touches starts a secondary wavelet. The wavelet from A starts first, so it grows biggest. The ones further along start later and are smaller."):
            self.play(u.animate.set_value(0.6), run_time=4.0, rate_func=linear)
        with self.say("When B finally reaches the mirror at C, after time t, the wavelet from A has radius c t. The tangent from C to that wavelet is the reflected wavefront, C D."):
            self.play(u.animate.set_value(1.0), run_time=2.5, rate_func=linear)
            lc = VGroup(M("C", size=32).next_to(C, DR, buff=0.08), M("D", size=32).next_to(D, RIGHT, buff=0.12))
            self.play(FadeIn(lc))
        self.remove(m["inc"], m["out"], m["wavelets"])
        AB = Line(A, B, color=C_W, stroke_width=5)
        CD = Line(C, D, color=C_R, stroke_width=5)
        wv = VGroup(*[Arc(radius=m["BC"] * (1 - f), start_angle=0, angle=PI, arc_center=A + RIGHT * m["AC"] * f, color=th.MUTED, stroke_width=2) for f in np.linspace(0, 1, 7)[:-1]])
        self.add(AB, CD, wv)
        BCl = DashedLine(B, C, color=C_W, stroke_width=3)
        ADl = DashedLine(A, D, color=C_R, stroke_width=3)
        lab = VGroup(M(r"BC = ct", size=30, color=C_W).next_to(Line(B, C).get_center(), RIGHT, buff=0.15), M(r"AD = ct", size=30, color=C_R).next_to(Line(A, D).get_center(), LEFT, buff=0.15))
        with self.say("Now compare two right angled triangles. In triangle A B C, B C is the distance B travelled: c t. In triangle A D C, A D is the radius of A's wavelet: also c t. They share the side A C, and both have a right angle, at B and at D, because a wavefront is always perpendicular to its ray."):
            self.play(Create(BCl), Create(ADl), FadeIn(lab))
            tri1 = Polygon(A, B, C, stroke_width=0, fill_color=C_W, fill_opacity=0.18)
            tri2 = Polygon(A, D, C, stroke_width=0, fill_color=C_R, fill_opacity=0.18)
            self.play(FadeIn(tri1))
            self.play(FadeIn(tri2))
        grp = VGroup(mirror, rays, la, lc, AB, CD, wv, BCl, ADl, lab, tri1, tri2)
        self.play(grp.animate.scale(0.62).to_edge(LEFT, buff=0.3).shift(UP * 0.4))
        L = VGroup(M(r"\sin i = \frac{BC}{AC},\qquad \sin r = \frac{AD}{AC}", size=38), M(r"\frac{\sin i}{\sin r} = \frac{BC}{AD} = \frac{ct}{ct} = 1", size=38),
                   M(r"i = r", size=60, color=C_R)).arrange(DOWN, buff=0.4).move_to([3.5, 0.6, 0])
        with self.say("The angle between the wavefront and the mirror equals the angle between the ray and the normal. So sine i is B C over A C, and sine r is A D over A C."):
            self.play(Write(L[0]))
        with self.say("Divide them. Sine i over sine r equals B C over A D, which is c t over c t, one. So the angle of incidence equals the angle of reflection."):
            self.play(Write(L[1]))
            self.sfx("impact", gain=-12)
            self.play(Write(L[2]))
        first = para("And the incident wavefront, the mirror and the reflected wavefront all lie in the plane of the diagram, so the incident ray, the reflected ray and the normal are coplanar: the first law.", width=6.0, size=24, color=th.BODY).next_to(L, DOWN, buff=0.4)
        with self.say("And because the incident wavefront, the mirror and the reflected wavefront are all built in the same plane, the incident ray, the reflected ray and the normal are coplanar. That is the first law. Both laws, from one construction."):
            self.play(FadeIn(first))
        nb = neby_in(self, "success", corner=DR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(grp, L, first)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        nidx = 1.6
        u, m = self.construction(i_deg=52, n=nidx, ym=0.2, xA=-4.2, W=3.0)
        glass = Rectangle(width=10.0, height=3.4, stroke_width=0, fill_color=GLASS, fill_opacity=0.8).move_to([-1.8, 0.2 - 1.7, 0])
        surf = Line([-6.8, 0.2, 0], [3.2, 0.2, 0], color=th.BODY, stroke_width=3)
        lbl = VGroup(M(r"\text{medium 1: speed } v_1", size=28, color=C_W).move_to([4.6, 1.2, 0]), M(r"\text{medium 2 (denser): } v_2 < v_1", size=28, color=C_L).move_to([4.6, -1.0, 0]))
        A, B, C, D = m["A"], m["B"], m["C"], m["D"]
        la = VGroup(M("A", size=32).next_to(A, UL, buff=0.08), M("B", size=32).next_to(B, UP, buff=0.1))
        with self.say("Now refraction. The same plane wavefront A B meets the flat surface of a denser medium, where light is slower: v two is less than v one. End A touches the surface first."):
            self.play(FadeIn(glass), Create(surf), FadeIn(lbl))
            self.add(m["inc"])
            self.play(FadeIn(m["inc"]), FadeIn(la))
        self.add(m["wavelets"], m["out"])
        with self.say("While B travels the distance B C at speed v one, the wavelet from A spreads into the glass, but only at the slower speed v two. It grows to a radius of just v two t."):
            self.play(u.animate.set_value(0.65), run_time=4.0, rate_func=linear)
        with self.say("The tangent from C to that smaller wavelet is the refracted wavefront, C D. Because the wavelet is small, the new front is tilted, and the ray bends towards the normal. Just like the marching students."):
            self.play(u.animate.set_value(1.0), run_time=2.5, rate_func=linear)
            lc = VGroup(M("C", size=32).next_to(C, UR, buff=0.08), M("D", size=32).next_to(D, DL, buff=0.08))
            self.play(FadeIn(lc))
        self.remove(m["inc"], m["out"], m["wavelets"])
        AB = Line(A, B, color=C_W, stroke_width=5)
        CD = Line(C, D, color=C_L, stroke_width=5)
        wv = Arc(radius=m["R"], start_angle=PI, angle=PI, arc_center=A, color=th.MUTED, stroke_width=2)
        BCl = DashedLine(B, C, color=C_W, stroke_width=3)
        ADl = DashedLine(A, D, color=C_L, stroke_width=3)
        lab = VGroup(M(r"BC = v_1t", size=30, color=C_W).next_to(Line(B, C).get_center(), RIGHT, buff=0.15), M(r"AD = v_2t", size=30, color=C_L).next_to(Line(A, D).get_center(), LEFT, buff=0.15))
        self.add(AB, CD, wv)
        with self.say("Mark the two distances. B C equals v one t. A D equals v two t."):
            self.play(Create(BCl), Create(ADl), FadeIn(lab))
        grp = VGroup(glass, surf, la, lc, AB, CD, wv, BCl, ADl, lab)
        self.play(FadeOut(lbl), grp.animate.scale(0.62).to_edge(LEFT, buff=0.2).shift(UP * 0.2))
        L = VGroup(M(r"\sin i = \frac{BC}{AC} = \frac{v_1t}{AC}", size=36), M(r"\sin r = \frac{AD}{AC} = \frac{v_2t}{AC}", size=36),
                   M(r"\frac{\sin i}{\sin r} = \frac{v_1}{v_2} = {}_1n_2 = \text{constant}", size=38, color=C_L),
                   M(r"n = \frac{c}{v}\ \Rightarrow\ \frac{\sin i}{\sin r} = \frac{n_2}{n_1}", size=36), M(r"n_1\sin i = n_2\sin r", size=52, color=th.AMBER)).arrange(DOWN, buff=0.28).move_to([3.4, 0.0, 0])
        says = ["From triangle A B C, sine i is B C over A C, which is v one t over A C.",
                "From triangle A D C, sine r is A D over A C, which is v two t over A C.",
                "Divide. A C and t cancel, and sine i over sine r equals v one over v two. That depends only on the two media, not on the angle. It is a constant: Snell's law, with the constant being the refractive index of medium two relative to medium one.",
                "Define the absolute refractive index of a medium as n equals c over v. Then v one is c over n one, and v two is c over n two.",
                "And Snell's law takes its most useful form: n one sine i equals n two sine r."]
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(FadeOut(VGroup(grp, L)))
        example(self, "Light strikes a glass block (n = 1.5) at 60°. With c = 3 × 10⁸ m/s and vacuum wavelength 600 nm, find the angle of refraction, the speed of light in the glass and the wavelength in the glass.",
                [r"\sin r = \frac{\sin 60^{\circ}}{1.5} = \frac{0.8660}{1.5} = 0.5774\ \Rightarrow\ r = 35.3^{\circ}",
                 r"v = \frac{c}{n} = \frac{3\times10^{8}}{1.5} = 2.0\times10^{8}\ \text{m s}^{-1}",
                 r"\lambda_g = \frac{\lambda_0}{n} = \frac{600}{1.5} = 400\ \text{nm}\quad(f = 5.0\times10^{14}\ \text{Hz in both})"],
                ["Worked example. Light strikes a glass block of refractive index one point five, at sixty degrees. Find the angle of refraction, the speed in the glass, and the wavelength in the glass.",
                 "Snell: sine r is sine sixty over one point five, zero point eight six six over one point five, zero point five seven seven four. So r is thirty five point three degrees.",
                 "Speed is c over n: two times ten to the eight metres per second.",
                 "And the wavelength is six hundred over one point five, four hundred nanometres. The frequency, five times ten to the fourteen hertz, is the same in both. More on that next."], size=38)
        self.quiz("Secondary wavelets in Huygens' construction travel with",
                  ["the speed of the source", "the speed of light in that medium", "infinite speed", "half the wave speed"], 1,
                  "Pause and think. In Huygens' construction, how fast do the secondary wavelets spread?",
                  "B, at the speed of light in that medium, c over n. That is the whole secret of refraction: in the glass, the wavelets grow more slowly, so the front tilts.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        t = clock(self, 1.0)
        nidx = 1.6
        k1 = TAU / 1.6
        k2 = k1 * nidx
        w = 3.0
        xb = 0.0

        def yv(x):
            if x < xb:
                return 0.7 * np.sin(w * t.get_value() - k1 * (x + 6))
            return 0.7 * np.sin(w * t.get_value() - k1 * (xb + 6) - k2 * (x - xb))
        glass = Rectangle(width=6.6, height=3.0, stroke_width=0, fill_color=GLASS, fill_opacity=0.8).move_to([3.3, 0.6, 0])
        wave = always_redraw(lambda: curve(lambda x: 0.6 + yv(x), -6.3, 6.3, n=400, color=C_W, width=4))
        lb = VGroup(T("air", size=26).move_to([-3.2, 2.5, 0]), T("glass, n = 1.6", size=26, color=C_L).move_to([3.3, 2.5, 0]))
        pA = always_redraw(lambda: Dot([-2.0, 0.6 + yv(-2.0), 0], color=th.AMBER, radius=0.12))
        pB = always_redraw(lambda: Dot([2.6, 0.6 + yv(2.6), 0], color=th.AMBER, radius=0.12))
        with self.say("What actually changes when light enters glass? Look at the wave. The vibrations inside the glass are driven by the vibrations arriving from the air, so they must keep exactly the same rhythm. Watch the two marked points: they bob up and down at the same rate."):
            self.play(FadeIn(glass), FadeIn(lb))
            self.add(wave, pA, pB)
            self.play(FadeIn(wave), FadeIn(pA), FadeIn(pB))
            self.wait(3)
        eqs = VGroup(M(r"f \text{ unchanged (set by the source)}", size=34), M(r"v = \frac{c}{n},\qquad \lambda_m = \frac{\lambda_0}{n}", size=40, color=C_L),
                     M(r"\frac{\lambda_1}{\lambda_2} = \frac{v_1}{v_2} = \frac{n_2}{n_1}", size=40)).arrange(DOWN, buff=0.3).move_to([0, -2.1, 0])
        with self.say("So the frequency does not change on refraction. It is fixed by the source. But the speed falls to c over n, and since v equals f lambda, the wavelength shrinks by the same factor: lambda in the medium is lambda in vacuum over n. The waves bunch up. The colour, which is set by frequency, stays the same."):
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]))
        self.play(FadeOut(VGroup(glass, lb, eqs)), FadeOut(wave), FadeOut(pA), FadeOut(pB))
        self.remove(wave, pA, pB, t)
        title = T("Optical path", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        x0, xg = -5.0, 2.4
        nn = 1.5
        lam0 = 0.5
        slab = Rectangle(width=xg, height=1.2, stroke_width=0, fill_color=GLASS, fill_opacity=0.9).move_to([x0 + xg / 2, 1.2, 0])
        w1 = curve(lambda x: 1.2 + 0.4 * np.sin(TAU * (x - x0) * nn / lam0), x0, x0 + xg, n=400, color=C_L, width=3)
        vac = curve(lambda x: -1.0 + 0.4 * np.sin(TAU * (x - x0) / lam0), x0, x0 + xg * nn, n=400, color=C_W, width=3)
        b1 = BraceBetweenPoints([x0, 0.45, 0], [x0 + xg, 0.45, 0], DOWN, color=C_L)
        b1l = M(r"x\ \text{in glass}", size=28, color=C_L).next_to(b1, DOWN, buff=0.05)
        b2 = BraceBetweenPoints([x0, -1.75, 0], [x0 + xg * nn, -1.75, 0], DOWN, color=C_W)
        b2l = M(r"nx\ \text{in vacuum}", size=28, color=C_W).next_to(b2, DOWN, buff=0.05)
        eq = M(r"\text{optical path} = n\,x", size=48, color=th.AMBER).move_to([3.6, 1.2, 0])
        with self.say("This gives a very useful idea. A length x of glass holds n times as many waves as the same length of vacuum. It holds the same number of waves as a length n x of vacuum."):
            self.play(FadeIn(title), FadeIn(slab), Create(w1), GrowFromCenter(b1), FadeIn(b1l))
            self.play(Create(vac), GrowFromCenter(b2), FadeIn(b2l))
        with self.say("So we define the optical path as n times x. Whenever light passes through glass or water in the next two units, replace the real distance by the optical path."):
            self.play(Write(eq))
        self.play(FadeOut(VGroup(title, slab, w1, vac, b1, b1l, b2, b2l, eq)))
        self.quiz("When light travels from air into glass, the quantity that does NOT change is",
                  ["speed", "wavelength", "frequency", "direction"], 2,
                  "Pause and think. Light goes from air into glass. Which quantity stays the same?",
                  "C, the frequency. It is set by the source. The speed falls to c over n, the wavelength shrinks by the same factor, and the direction changes unless the light hits the surface straight on.")
        example(self, "A beam of frequency 5.0 × 10¹⁴ Hz passes from air into a liquid where its wavelength is 375 nm. Find the refractive index and the speed of light in the liquid.",
                [r"v = f\lambda_m = (5.0\times10^{14})(375\times10^{-9}) = 1.875\times10^{8}\ \text{m s}^{-1}",
                 r"n = \frac{c}{v} = \frac{3\times10^{8}}{1.875\times10^{8}} = 1.6",
                 r"\text{check: } \lambda_0 = \frac{c}{f} = 600\ \text{nm},\quad \frac{600}{375} = 1.6\ \checkmark"],
                ["Worked example. Light of frequency five times ten to the fourteen hertz enters a liquid, where its wavelength is three hundred and seventy five nanometres. Find the refractive index and the speed.",
                 "The frequency is unchanged, so the speed in the liquid is f times lambda: one point eight seven five times ten to the eight metres per second.",
                 "The refractive index is c over v: three over one point eight seven five, one point six.",
                 "Check another way. In vacuum the wavelength would be c over f, six hundred nanometres. Six hundred over three seventy five is also one point six. The two routes agree."], size=38)
        example(self, "A glass plate 2.0 mm thick (n = 1.5) is placed in light of vacuum wavelength 500 nm. Find the optical path, the number of waves in the plate, and the extra time compared with 2.0 mm of vacuum.",
                [r"nx = 1.5\times 2.0\times10^{-3} = 3.0\times10^{-3}\ \text{m}",
                 r"N = \frac{nx}{\lambda_0} = \frac{3.0\times10^{-3}}{500\times10^{-9}} = 6000",
                 r"\Delta t = \frac{(n - 1)x}{c} = \frac{0.5\times 2.0\times10^{-3}}{3\times10^{8}} = 3.3\times10^{-12}\ \text{s}"],
                ["Worked example. A glass plate two millimetres thick, of index one point five, sits in light of vacuum wavelength five hundred nanometres. Find the optical path, the number of waves in the plate, and the extra time it takes.",
                 "The optical path is n x: one point five times two millimetres, three millimetres.",
                 "The number of waves is the optical path over the vacuum wavelength: three millimetres over five hundred nanometres, six thousand waves.",
                 "Time in glass is n x over c, in vacuum x over c. The delay is n minus one, times x, over c: about three point three picoseconds. Tiny, but in the next unit, delays like this shift whole interference patterns."], size=38)
        self.quiz("The optical path of a ray covering 4 cm in a medium of refractive index 1.5 is",
                  ["2.67 cm", "4 cm", "6 cm", "9 cm"], 2,
                  "Pause and think. A ray covers four centimetres in a medium of index one point five. What is its optical path?",
                  "C, six centimetres: n times x. Two point six seven is what you get if you divide instead of multiplying. The optical path is always longer than the real path in glass.")
        example(self, "Light of wavelength 600 nm in vacuum enters a medium of refractive index 1.25. Find its speed, frequency and wavelength in the medium.",
                [r"v = \frac{c}{n} = \frac{3\times10^{8}}{1.25} = 2.4\times10^{8}\ \text{m s}^{-1}",
                 r"f = \frac{c}{\lambda_0} = \frac{3\times10^{8}}{600\times10^{-9}} = 5.0\times10^{14}\ \text{Hz}\ (\text{unchanged})",
                 r"\lambda_m = \frac{v}{f} = \frac{2.4\times10^{8}}{5.0\times10^{14}} = 480\ \text{nm} = \frac{600}{1.25}"],
                ["One more from the five mark questions. Light of vacuum wavelength six hundred nanometres enters a medium of index one point two five. Find its speed, frequency and wavelength there.",
                 "Speed is c over n: three times ten to the eight over one point two five, two point four times ten to the eight metres per second.",
                 "The frequency is the same as in vacuum: c over six hundred nanometres, five times ten to the fourteen hertz.",
                 "And the wavelength is v over f, four hundred and eighty nanometres, which is just six hundred divided by one point two five."], size=40)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Newton's corpuscles vs Huygens' waves", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        surf = Line([-6.6, -0.6, 0], [6.6, -0.6, 0], color=th.BODY, stroke_width=3)
        water = Rectangle(width=13.2, height=2.6, stroke_width=0, fill_color="#1E5A8A", fill_opacity=0.6).move_to([0, -1.9, 0])
        div = DashedLine([0, 2.4, 0], [0, -3.2, 0], color=th.FAINT)
        t = ValueTracker(0)
        a = np.radians(45)
        s1 = np.array([-5.4, 2.0, 0])
        d1 = np.array([np.sin(a), -np.cos(a), 0])
        tb = (s1[1] + 0.6) / (np.cos(a) * 1.2)
        rN = np.arcsin(np.sin(a) / 1.33)
        dN = np.array([np.sin(rN), -np.cos(rN), 0])

        def corp():
            tt = t.get_value()
            p = s1 + d1 * 1.2 * min(tt, tb) + (dN * 1.2 * 1.33 * (tt - tb) if tt > tb else 0)
            return Dot(p, radius=0.12, color=th.CORAL)

        def wavep():
            tt = t.get_value()
            s2 = s1 + RIGHT * 6.4
            p = s2 + d1 * 1.2 * min(tt, tb) + (dN * 1.2 / 1.33 * (tt - tb) if tt > tb else 0)
            return Dot(p, radius=0.12, color=C_W)
        cd = always_redraw(corp)
        wd = always_redraw(wavep)
        tr1 = TracedPath(cd.get_center, stroke_color=th.CORAL, stroke_width=3)
        tr2 = TracedPath(wd.get_center, stroke_color=C_W, stroke_width=3)
        labs = VGroup(para("Newton: water attracts the corpuscles, which speed up as they bend", width=5.6, size=22, color=th.CORAL).move_to([-3.3, -2.7, 0]),
                      para("Huygens: the wave slows down in water, so it bends", width=5.6, size=22, color=C_W).move_to([3.3, -2.7, 0]))
        with self.say("For over a century two pictures of light competed. Newton said light is a stream of tiny particles, corpuscles. To explain bending towards the normal, he needed water to pull the particles in, so they would speed up in water. Huygens said light is a wave, and it bends towards the normal because it slows down in water."):
            self.play(FadeIn(title), FadeIn(water), Create(surf), Create(div), FadeIn(labs))
            self.add(cd, wd, tr1, tr2)
            self.play(t.animate.set_value(tb + 1.4), run_time=5, rate_func=linear)
        with self.say("Both pictures bend the light the same way. But they make opposite predictions about its speed in water. Newton says faster. Huygens says slower. Someone just had to measure it."):
            self.play(Indicate(cd, color=WHITE), Indicate(wd, color=WHITE))
        self.play(FadeOut(VGroup(title, water, surf, div, labs, tr1, tr2)), FadeOut(cd), FadeOut(wd))
        self.remove(cd, wd, tr1, tr2)
        rows = [("", "Corpuscles (Newton)", "Waves (Huygens)"), ("light is", "a stream of particles", "spreading wavefronts"), ("speed in water", "greater than in air", "less than in air"),
                ("reflection, refraction", "explained", "explained"), ("interference, diffraction", "not explained", "explained"), ("verdict", "disproved, 1850", "confirmed")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=25 if i else 28, color=(th.BG if not c else ([th.MUTED, th.CORAL, C_W][j] if i == 0 or j == 0 else th.BODY)),
                             weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.5, -0.6, 3.6]):
                row[j].move_to([x, 2.4 - i * 0.68, 0])
            grid.add(row)
        fou = para("1850: Foucault's rotating-mirror experiment shows light is SLOWER in water than in air.", width=10, size=26, color=th.AMBER, align="center").to_edge(DOWN, buff=0.55)
        with self.say("In eighteen fifty, Léon Foucault did it, with a rapidly rotating mirror. Light travels more slowly in water than in air. That single result ended the corpuscular theory. And the wave picture also explains interference, diffraction and polarization, which particles never could. Those are our next three units.") as v_:
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 8 - 0.6)
            self.play(FadeIn(fou, shift=UP * 0.2))
        nb = neby_in(self, "cool", corner=DR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(grid, fou)))
        neby_out(self, nb)
        self.quiz("According to the wave theory of light, the speed of light in water is",
                  ["greater than in air", "less than in air", "equal to that in air", "zero"], 1,
                  "Pause and think. What does the wave theory predict for the speed of light in water?",
                  "B, less than in air. The wave theory needs light to slow down in water to bend towards the normal, and Foucault confirmed it. Greater is the corpuscular prediction, the one that failed.")
        self.slab()

    def slab(self):
        head = T(self.S["example"], size=26, color=self.color, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A ray is incident at 45° on a glass slab (n = 1.5) 6.0 cm thick. Find the angle of refraction, the speed in the slab, the time to cross it and the lateral displacement.", width=12.2, size=26, color=th.INK).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
        with self.say("To finish, a full long question. A ray hits a parallel glass slab of index one point five, six centimetres thick, at forty five degrees. Find the angle of refraction, the speed inside, the time to cross, and the lateral displacement of the emergent ray."):
            self.play(FadeIn(head), FadeIn(prob))
        s = 0.45
        top, bot = 0.6, 0.6 - 6.0 * s
        slab = Rectangle(width=3.4, height=6.0 * s, stroke_color=th.SKY, stroke_width=3, fill_color=GLASS, fill_opacity=0.85).move_to([-4.8, (top + bot) / 2, 0])
        i, r = np.radians(45), np.arcsin(np.sin(np.radians(45)) / 1.5)
        P = np.array([-6.0, top, 0])
        Q = P + np.array([np.tan(r) * 6.0 * s, -6.0 * s, 0])
        inc = Line(P + np.array([-np.sin(i), np.cos(i), 0]) * 1.4, P, color=th.AMBER, stroke_width=5)
        ins = Line(P, Q, color=th.AMBER, stroke_width=5)
        em = Line(Q, Q + np.array([np.sin(i), -np.cos(i), 0]) * 1.2, color=th.AMBER, stroke_width=5)
        ext = DashedLine(P, P + np.array([np.sin(i), -np.cos(i), 0]) * 4.2, color=th.MUTED, stroke_width=2)
        dd = np.array([np.sin(i), -np.cos(i), 0])
        foot = P + dd * np.dot(Q - P, dd)
        dl = Line(Q, foot, color=th.CORAL, stroke_width=4)
        dlab = M("d", size=30, color=th.CORAL).next_to(dl, DOWN, buff=0.05)
        steps = VGroup(M(r"\sin r = \frac{0.7071}{1.5} = 0.4714\ \Rightarrow\ r = 28.1^{\circ}", size=32),
                       M(r"v = \frac{c}{n} = 2.0\times10^{8}\ \text{m s}^{-1}", size=32),
                       M(r"\text{path} = \frac{6.0}{\cos r} = \frac{6.0}{0.8819} = 6.80\ \text{cm},\ \ t = \frac{6.80\times10^{-2}}{2.0\times10^{8}} = 3.4\times10^{-10}\ \text{s}", size=30),
                       M(r"d = \frac{t\sin(i - r)}{\cos r} = \frac{6.0\times\sin 16.9^{\circ}}{0.8819} = \frac{6.0\times 0.2902}{0.8819} = 1.97\ \text{cm}", size=30, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.scale_to_fit_width(min(steps.width, 8.4)).move_to([2.1, -1.2, 0])
        self.play(prob.animate.scale(0.8).next_to(head, DOWN, aligned_edge=LEFT, buff=0.2), FadeIn(slab), Create(inc))
        with self.say("Snell's law: sine r is sine forty five over one point five, zero point four seven one four, so r is twenty eight point one degrees."):
            self.play(Create(ins))
            self.play(Write(steps[0]))
        with self.say("The speed inside is c over n, two times ten to the eight metres per second."):
            self.play(Write(steps[1]))
        with self.say("The ray crosses on a slant, so its path is the thickness over cos r: six over zero point eight eight one nine, six point eight centimetres. At two times ten to the eight, that takes three point four times ten to the minus ten seconds."):
            self.play(Write(steps[2]))
        with self.say("It leaves parallel to the incoming ray, but shifted sideways. The lateral displacement is t sine of i minus r, over cos r: six times sine sixteen point nine degrees, over zero point eight eight one nine. About one point nine seven centimetres."):
            self.play(Create(em), Create(ext))
            self.play(Create(dl), FadeIn(dlab))
            self.play(Write(steps[3]))
        self.wait(0.5)
        self.play(FadeOut(VGroup(head, prob, slab, inc, ins, em, ext, dl, dlab, steps)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "A wavefront is a surface of constant phase; a ray is its normal. Spherical, cylindrical or plane.",
            "Huygens: every point is a source of forward wavelets of radius vt; the new wavefront is their envelope (K = ½(1 + cos θ)).",
            M(r"\text{reflection: } BC = AD = ct\ \Rightarrow\ i = r", size=34),
            M(r"\text{refraction: } \frac{\sin i}{\sin r} = \frac{v_1}{v_2} = \frac{n_2}{n_1},\quad n_1\sin i = n_2\sin r", size=34),
            M(r"f \text{ unchanged};\ \ v = \frac{c}{n},\ \ \lambda_m = \frac{\lambda_0}{n};\ \ \text{optical path} = nx", size=34),
            "Foucault (1850): light is slower in water, so the wave theory wins over corpuscles.",
        ], "Let us recap. A wavefront is a surface of constant phase, and a ray is its normal. Huygens' principle: every point on a wavefront sends out forward wavelets, and the new wavefront is their envelope. Applied to a mirror, equal wavelets give i equals r. Applied to a denser medium, slower wavelets give sine i over sine r equals v one over v two, Snell's law. The frequency never changes on refraction; the speed and wavelength fall by n, and the optical path is n x. And Foucault's experiment settled it: light is a wave.")
        self.outro("That is the nature of light. Next, we let two light waves meet, and see bright and dark fringes appear from nowhere, in Interference. See you there, on NEBians.")
