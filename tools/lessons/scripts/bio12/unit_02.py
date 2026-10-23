# Content decisions where this lesson departs from notes/content/bio12/unit-02.md (for the reviewer):
# 1. Photoperiodism is not in the notes but belongs to "Plant growth and movement"; a short NCERT-level
#    beat was added (short-day / long-day / day-neutral, critical night length, night-break, phytochrome
#    in the leaf, florigen). The 12-hour critical night on screen is stated aloud as an illustration.
# 2. Mimosa: the notes say the lower (ventral) motor cells lose turgor for leaflets as well as the petiole.
#    That is right for the primary pulvinus (the petiole drops) but leaflets fold UPWARD, which needs the
#    upper motor cells of their small pulvini to lose turgor. The lesson states the lower-half rule only
#    for the primary pulvinus at the base of the leaf stalk.
# 3. The notes say cytochrome b6f pumps "four more" protons per two water molecules; with the Q-cycle it
#    is about eight per four electrons. The lesson only says the complex adds protons to the lumen.
# 4. RQ of protein: the notes give 0.82; the lesson says "about 0.8" (textbooks quote 0.8 to 0.9).
import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
from _bio import XYL, PHL, PAR, PARF, EPI, ENDO, CHL, WATER, FOOD  # noqa: E402
import _phys2 as P  # noqa: E402

SOL = th.AMBER          # solutes / solute potential
PRS = th.SKY            # pressure potential
ATPC = th.AMBER
NADH = th.MINT
FADC = th.PINK
CO2C = "#AAB2D6"
O2C = th.CORAL
HPC = "#FF9F6B"         # protons
CARB = "#9AA3D8"        # carbon beads
SHOOT, SHOOT_F, ROOT, ROOT_F, AUX = P.SHOOT, P.SHOOT_F, P.ROOT, P.ROOT_F, P.AUX


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 2
    TITLE = "Plant Physiology"
    SUBTITLE = "How a plant drinks, feeds, breathes and moves"
    SECTIONS = ["Water relation", "Photosynthesis", "Respiration", "Plant hormones", "Plant growth and movement"]
    NEXT = "Unit 3 · Genetics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ small helpers
    def head(self, text, color=None):
        return T(text, size=32, color=color or th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)

    def steps(self, items, size=36, buff=0.32):
        g = VGroup(*[M(s, size=size) if isinstance(s, str) else s for s in items])
        return g.arrange(DOWN, aligned_edge=LEFT, buff=buff)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        G, H, X = -2.8, 4.8, 1.4
        ground = Line([-6.8, G, 0], [6.8, G, 0], color=th.FAINT, stroke_width=3)
        trunk = Polygon([X - 0.32, G, 0], [X + 0.32, G, 0], [X + 0.11, G + H, 0], [X - 0.11, G + H, 0], stroke_width=0, fill_color="#7A5534", fill_opacity=1)
        crown = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=c, fill_opacity=0.97).move_to([X + dx, G + H + dy, 0])
                         for r, dx, dy, c in [(0.62, -0.8, -0.15, "#2E7D32"), (0.62, 0.8, -0.1, "#2E7D32"), (0.7, 0, 0.1, "#388E3C"), (0.45, -0.35, 0.5, "#43A047"), (0.45, 0.4, 0.48, "#43A047")]])
        sal = VGroup(trunk, crown)
        bar = Line([4.6, G, 0], [4.6, G + H, 0], color=th.MUTED, stroke_width=3)
        ticks = VGroup()
        for k in range(1, 4):
            y = G + H * k / 3
            ticks.add(Line([4.5, y, 0], [4.7, y, 0], color=th.MUTED, stroke_width=3), T(f"{10 * k} m", size=22, color=th.MUTED).move_to([5.3, y, 0]))
        sal_lab = T("sal tree, 30 m", size=24, color="#C9A27A").move_to([X, G - 0.3, 0])
        flow = B.Flow([X, G + 0.15, 0], [X, G + H - 0.1, 0], n=16, speed=0.9, width=0.22, r=0.055)
        with self.say("A sal tree near Hetauda, thirty metres tall. Every leaf at the top is full of water, and all of it came from the soil, thirty metres below."):
            self.play(Create(ground), FadeIn(sal, shift=UP * 0.3), Create(bar), FadeIn(ticks), FadeIn(sal_lab))
        with self.say("Something lifted it, ten storeys, every day. And the tree has no heart, no pump, no muscle."):
            self.add(flow)
            self.wait(1.0)
        PX = -3.6
        well = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.3, stroke_width=0, fill_color=WATER, fill_opacity=0.6).move_to([PX, G - 0.05, 0])
        pipe = VGroup(Line([PX - 0.12, G, 0], [PX - 0.12, G + H, 0], color=th.BODY, stroke_width=3), Line([PX + 0.12, G, 0], [PX + 0.12, G + H, 0], color=th.BODY, stroke_width=3))
        pump = RoundedRectangle(corner_radius=0.08, width=0.8, height=0.5, stroke_color=th.BODY, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to([PX, G + H + 0.2, 0])
        y10 = G + H / 3
        col = Rectangle(width=0.2, height=y10 - G, stroke_width=0, fill_color=WATER, fill_opacity=0.7).move_to([PX, (G + y10) / 2, 0])
        limit = DashedLine([PX - 0.9, y10, 0], [4.5, y10, 0], color=th.CORAL, stroke_width=2.5, dash_length=0.12)
        pl = T("suction pump: about 10 m at most", size=22, color=th.CORAL)
        pl.move_to([PX + 0.3 + pl.width / 2, y10 + 0.35, 0])
        cross = VGroup(Line([-0.25, -0.25, 0], [0.25, 0.25, 0]), Line([-0.25, 0.25, 0], [0.25, -0.25, 0])).set_stroke(th.CORAL, 6).move_to([PX, y10 + 1.0, 0])
        with self.say("Yet a suction pump on a well cannot lift water more than about ten metres. Pull harder and the water column breaks."):
            self.play(FadeIn(well), Create(pipe), FadeIn(pump))
            self.play(GrowFromEdge(col, DOWN), run_time=1.5)
            self.play(Create(limit), FadeIn(pl))
            self.sfx("wrong", gain=-12)
            self.play(Create(cross))
        nb = B.neby_in(self, "surprised", height=1.4, at=[-1.1, 1.4, 0])
        with self.say("The sal does three times that, silently. How? The surprising answer, by the end of this lesson: the water is not pushed up. It is pulled from above."):
            self.play(Indicate(crown, color=th.AMBER, scale_factor=1.05), run_time=1.2)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(ground, sal, bar, ticks, sal_lab, flow, well, pipe, pump, col, limit, pl, cross)))
        self.remove(flow)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 2: Plant Physiology. Unit 1 built the plumbing. Now we switch it on."):
            pass
        self.end_title(g, nb)
        self.roadmap("Five stops: water relations, photosynthesis, respiration, plant hormones, and growth and movement.")

    # ================================================================== PART 1: WATER RELATION
    def p1(self):
        self.section(0)
        self.p1_diffusion()
        self.p1_osmosis()
        self.p1_potential()
        self.p1_example()
        self.p1_plasmolysis()
        self.p1_root()
        self.p1_rootpressure()
        self.p1_ascent()
        self.p1_stomata()
        self.p1_guttation()

    def p1_diffusion(self):
        head = self.head("Diffusion and imbibition")
        box = Rectangle(width=5.0, height=3.4, stroke_color=th.MUTED, stroke_width=3, fill_color=WATER, fill_opacity=0.06).move_to([-3.4, -0.4, 0])
        rg = np.random.default_rng(3)
        c = box.get_center()
        start = [c + [-2.0 + rg.uniform(-0.3, 0.3), rg.uniform(-0.5, 0.5), 0] for _ in range(46)]
        end = [c + [rg.uniform(-2.3, 2.3), rg.uniform(-1.5, 1.5), 0] for _ in range(46)]
        dots = VGroup(*[Dot(p, radius=0.06, color=th.AMBER) for p in start])
        cap = B.Captions(self, at=(3.3, -0.3, 0), width=5.8, size=27)
        with self.say("Drop dye into still water. Its particles jiggle with heat energy and spread from crowded to scarce. That is diffusion.") as v:
            self.play(FadeIn(head), Create(box), FadeIn(dots))
            cap("Diffusion", color=th.AMBER, sub="Net movement from higher to lower concentration, driven by the particles' own kinetic energy.")
            self.play(*[d.animate.move_to(e) for d, e in zip(dots, end)], run_time=max(1.5, v.left - 0.3), rate_func=rate_functions.ease_out_sine)
        with self.say("No membrane, no energy, no living cell needed. It is fast over micrometres but hopeless over metres, which is why plants need xylem."):
            cap("No membrane, no energy, no life needed", color=th.AMBER, sub="Fast over micrometres, hopeless over metres: hence a transport system.")
        self.play(FadeOut(VGroup(box, dots)))
        pea = Circle(radius=0.42, stroke_color="#C5F05C", stroke_width=3, fill_color="#5E8C2E", fill_opacity=1).move_to([-4.8, -0.2, 0])
        wheat = Ellipse(width=0.55, height=0.95, stroke_color="#F6E3A1", stroke_width=3, fill_color="#B08A3E", fill_opacity=1).move_to([-2.0, -0.2, 0])
        groove = Line([-2.0, -0.55, 0], [-2.0, 0.15, 0], color="#6B5020", stroke_width=2)
        wheat = VGroup(wheat, groove)
        pool = RoundedRectangle(corner_radius=0.3, width=5.6, height=3.0, stroke_width=0, fill_color=WATER, fill_opacity=0.12).move_to([-3.4, -0.3, 0])
        lp = T("pea: protein-rich", size=22, color="#C5F05C").move_to([-4.8, -2.3, 0])
        lw = T("wheat: starch-rich", size=22, color="#F6E3A1").move_to([-2.0, -2.3, 0])
        with self.say("Soak a dry pea overnight and it swells to twice its size. That is imbibition: water adsorbed by hydrophilic colloids, the first step of germination.") as v:
            self.play(FadeIn(pool), FadeIn(pea), FadeIn(wheat), FadeIn(lp), FadeIn(lw))
            cap("Imbibition", color=WATER, sub="Water adsorbed by hydrophilic colloids, which swell. First step in germination.")
            self.play(pea.animate.scale(1.9), wheat.animate.scale(1.3), run_time=max(1.5, v.left - 0.5))
        with self.say("Protein imbibes most, then starch, then cellulose, so a pea swells more than a wheat grain."):
            cap("protein > starch > cellulose", color=WATER, sub="Imbibition pressure can reach a few megapascals.")
            self.play(Indicate(pea, color=th.AMBER, scale_factor=1.05))
        cap.clear()
        self.play(FadeOut(VGroup(head, pool, pea, wheat, lp, lw)))

    def p1_osmosis(self):
        head = self.head("Osmosis")
        BY, X0, X1, XM, TOP = -2.6, -6.0, -0.6, -3.3, 1.9
        h = ValueTracker(0.0)
        L0 = 0.0

        def fills():
            hl, hr = L0 - h.get_value(), L0 + h.get_value()
            a = Rectangle(width=XM - X0, height=hl - BY, stroke_width=0, fill_color=WATER, fill_opacity=0.25).move_to([(X0 + XM) / 2, (BY + hl) / 2, 0])
            b = Rectangle(width=X1 - XM, height=hr - BY, stroke_width=0, fill_color="#6C8FD0", fill_opacity=0.3).move_to([(XM + X1) / 2, (BY + hr) / 2, 0])
            return VGroup(a, b)

        fill = always_redraw(fills)
        tank = VMobject(stroke_color=th.MUTED, stroke_width=4).set_points_as_corners([[X0, TOP, 0], [X0, BY, 0], [X1, BY, 0], [X1, TOP, 0]])
        mem = DashedLine([XM, BY, 0], [XM, TOP, 0], color=th.AMBER, stroke_width=4, dash_length=0.12)
        rg = np.random.default_rng(5)
        wat = VGroup(*[Dot([rg.uniform(X0 + 0.2, X1 - 0.2), rg.uniform(BY + 0.15, -0.95), 0], radius=0.04, color=WATER) for _ in range(46)])
        sol = VGroup(*[Dot([rg.uniform(XM + 0.25, X1 - 0.25), rg.uniform(BY + 0.25, -0.9), 0], radius=0.12, color=FOOD) for _ in range(10)])
        la = T("pure water", size=22, color=WATER).move_to([(X0 + XM) / 2, 2.25, 0])
        lb = T("sugar solution", size=22, color=FOOD).move_to([(XM + X1) / 2, 2.25, 0])
        cap = B.Captions(self, at=(3.4, -0.2, 0), width=5.6, size=27)
        with self.say("Osmosis is diffusion through a selectively permeable membrane. Water passes through it; sugar does not."):
            self.play(FadeIn(head), Create(tank), FadeIn(fill), Create(mem), FadeIn(wat), FadeIn(sol), FadeIn(la), FadeIn(lb))
            cap("Selectively permeable membrane", color=th.AMBER, sub="Lets water through, holds the solute back.")
        f1 = B.Flow([XM - 1.0, -1.6, 0], [XM + 1.0, -1.6, 0], n=10, color=WATER, r=0.055, speed=0.8, width=1.1)
        f2 = B.Flow([XM + 1.0, -1.8, 0], [XM - 1.0, -1.8, 0], n=3, color=WATER, r=0.055, speed=0.8, width=0.9, seed=11)
        with self.say("More water crosses into the sugar side than comes back, so there is a net flow, and the solution column rises.") as v:
            self.add(f1, f2)
            cap("Net flow towards the solution", color=WATER, sub="Osmosis: net diffusion of water across a selectively permeable membrane.")
            self.play(h.animate.set_value(0.85), run_time=max(1.5, v.left - 0.5))
        piston = Rectangle(width=X1 - XM - 0.1, height=0.18, stroke_width=0, fill_color=th.BODY, fill_opacity=1).move_to([(XM + X1) / 2, 0.85 + 0.09, 0])
        arr = Arrow([(XM + X1) / 2, 1.9, 0], [(XM + X1) / 2, 1.05, 0], buff=0, color=th.CORAL, stroke_width=6)
        with self.say("The pressure needed to stop that flow is the osmotic pressure of the solution."):
            self.play(FadeIn(piston), GrowArrow(arr))
            cap("Osmotic pressure", color=th.CORAL, sub="The pressure that must be applied to a solution to stop water entering it through the membrane.")
            self.play(h.animate.set_value(0.0), piston.animate.shift(DOWN * 0.85), arr.animate.shift(DOWN * 0.85), FadeOut(f1), FadeOut(f2), run_time=2.0)
        self.remove(f1, f2)
        cap.clear()
        self.play(FadeOut(VGroup(head, tank, fill, mem, wat, sol, la, lb, piston, arr)))
        self.remove(fill)
        self.tip("Define osmosis with water potential: water moves from higher (less negative) Ψ to lower (more negative) Ψ. 'Dilute to concentrated' fails as soon as pressure acts, as in every turgid cell.",
                 "Exam tip. Don't define osmosis as dilute to concentrated; that fails once pressure acts. Say: water moves from higher to lower water potential.", width=8.6)

    def p1_potential(self):
        head = self.head("Water potential")
        nl = NumberLine(x_range=[-2.5, 0.5, 0.5], length=11, color=th.MUTED, include_numbers=True, font_size=26, decimal_number_config={"num_decimal_places": 1}).move_to([0, -2.1, 0])
        unit = T("MPa", size=22, color=th.MUTED).next_to(nl, RIGHT, buff=0.2)
        zero = VGroup(Triangle(fill_color=WATER, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(nl.n2p(0) + UP * 0.28),
                      T("pure water = 0", size=24, color=WATER).move_to(nl.n2p(0) + UP * 0.7))
        with self.say("Water potential, psi, measures the free energy of water. Pure water at atmospheric pressure is the reference: zero."):
            self.play(FadeIn(head), Create(nl), FadeIn(unit))
            self.play(FadeIn(zero, shift=DOWN * 0.2))
        s1 = VGroup(Triangle(fill_color=FOOD, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(nl.n2p(-2.48) + UP * 0.28),
                    T("1 M sucrose: −2.48", size=24, color=FOOD).move_to(nl.n2p(-2.48) + UP * 0.7 + RIGHT * 0.6))
        flow = Arrow(nl.n2p(-0.1) + UP * 1.3, nl.n2p(-2.3) + UP * 1.3, buff=0, color=WATER, stroke_width=5)
        fl = T("water flows this way: towards more negative Ψ", size=24, color=WATER).next_to(flow, UP, buff=0.15)
        with self.say("Solutes and surfaces lower it, so every solution and cell is negative. Water always moves from less negative to more negative."):
            self.play(FadeIn(s1, shift=DOWN * 0.2))
            self.play(GrowArrow(flow), FadeIn(fl))
        self.play(FadeOut(VGroup(flow, fl)))
        f = M(r"\Psi_w", "=", r"\Psi_s", "+", r"\Psi_p", size=60).move_to([0, 1.6, 0])
        f[2].set_color(SOL)
        f[4].set_color(PRS)
        d1 = VGroup(M(r"\Psi_s \le 0", size=36, color=SOL), T("solute potential: dissolved solutes lower it", size=24, color=th.BODY)).arrange(RIGHT, buff=0.3)
        d2 = VGroup(M(r"\Psi_p", size=36, color=PRS), T("pressure potential: + in a turgid cell, − in the xylem", size=24, color=th.BODY)).arrange(RIGHT, buff=0.3)
        d3 = T("(matric and gravity terms: negligible in a vacuolated cell)", size=22, color=th.MUTED)
        dd = VGroup(d1, d2, d3).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.0, 0])
        with self.say("For a cell, two terms matter. Psi s, the solute potential, is negative. Psi p, the pressure potential, is positive in a turgid cell, and negative in the xylem."):
            self.play(Write(f))
            self.play(FadeIn(d1, shift=RIGHT * 0.2))
            self.play(FadeIn(d2, shift=RIGHT * 0.2))
        with self.say("So the working equation is psi w equals psi s plus psi p."):
            self.play(FadeIn(d3))
            self.play(Circumscribe(f, color=th.AMBER), run_time=1.2)
        self.play(FadeOut(VGroup(d1, d2, d3, s1)), f.animate.scale(0.62).move_to([3.7, 2.25, 0]))
        # live cell
        C = np.array([-3.6, 0.15, 0])
        bath = RoundedRectangle(corner_radius=0.3, width=5.4, height=3.4, stroke_width=0, fill_color=WATER, fill_opacity=0.12).move_to(C)
        bl = T("bath: Ψw = −0.1 MPa", size=22, color=WATER).move_to(C + DOWN * 1.45)
        wall = Rectangle(width=3.2, height=2.0, stroke_color=PAR, stroke_width=6).move_to(C)
        pp = ValueTracker(0.0)

        def proto():
            d = 0.28 * (1 - pp.get_value() / 0.8) + 0.05
            pr = RoundedRectangle(corner_radius=0.2, width=3.2 - 2 * d, height=2.0 - 2 * d, stroke_color="#B6F5C4", stroke_width=2, fill_color="#1F4D33", fill_opacity=1).move_to(C)
            vac = RoundedRectangle(corner_radius=0.18, width=pr.width - 0.55, height=pr.height - 0.5, stroke_width=0, fill_color="#2B5F7F", fill_opacity=0.9).move_to(C + RIGHT * 0.12)
            nu = Dot(C + LEFT * (pr.width / 2 - 0.2), radius=0.1, color="#B6F5C4")
            return VGroup(pr, vac, nu)

        cell = always_redraw(proto)
        rows = VGroup()
        r1 = VGroup(M(r"\Psi_s =", size=40, color=SOL), DecimalNumber(-0.9, num_decimal_places=1, font_size=40, color=SOL))
        n2 = DecimalNumber(0.0, num_decimal_places=1, include_sign=True, font_size=40, color=PRS)
        r2 = VGroup(M(r"\Psi_p =", size=40, color=PRS), n2)
        n3 = DecimalNumber(-0.9, num_decimal_places=1, font_size=40, color=th.INK)
        r3 = VGroup(M(r"\Psi_w =", size=40), n3)
        for r in (r1, r2, r3):
            r.arrange(RIGHT, buff=0.2)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.4, 0])
        n2.add_updater(lambda m: m.set_value(pp.get_value()))
        n3.add_updater(lambda m: m.set_value(-0.9 + pp.get_value()))
        mk = always_redraw(lambda: VGroup(Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(nl.n2p(-0.9 + pp.get_value()) + UP * 0.28),
                                          T("cell", size=22, color=th.INK).move_to(nl.n2p(-0.9 + pp.get_value()) + UP * 0.65)))
        bm = VGroup(Triangle(fill_color=WATER, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI).move_to(nl.n2p(-0.1) + UP * 0.28),
                    T("bath", size=22, color=WATER).move_to(nl.n2p(-0.1) + UP * 1.0))
        with self.say("A cell with psi s of minus zero point nine sits in a bath at minus zero point one. Water flows in."):
            self.play(FadeOut(zero), FadeIn(bath), FadeIn(bl), Create(wall), FadeIn(cell), FadeIn(rows), FadeIn(mk), FadeIn(bm))
        fl1 = B.Flow(C + [-2.55, 0, 0], C + [-1.35, 0, 0], n=5, r=0.05, speed=0.6, width=1.2)
        fl2 = B.Flow(C + [2.55, 0, 0], C + [1.35, 0, 0], n=5, r=0.05, speed=0.6, width=1.2, seed=3)
        with self.say("The protoplast swells and the wall pushes back. Psi p climbs, and psi w climbs with it.") as v:
            self.add(fl1, fl2)
            self.play(pp.animate.set_value(0.8), run_time=max(2, v.left - 0.4), rate_func=rate_functions.ease_out_sine)
        n2.clear_updaters()
        n3.clear_updaters()
        with self.say("At psi p of plus zero point eight, psi w is minus zero point one, equal to the bath. Net flow stops: the cell is turgid."):
            self.play(FadeOut(fl1), FadeOut(fl2))
            self.play(Indicate(r3, color=th.MINT), run_time=1.0)
            nb = B.neby_in(self, "success", height=1.3)
        B.neby_out(self, nb)
        self.remove(fl1, fl2)
        self.play(FadeOut(VGroup(head, nl, unit, f, bath, bl, wall, cell, rows, mk, bm)))
        self.remove(cell, mk)

    def p1_example(self):
        head, prob = B.example_head(self, "Calculate the solute potential of a 1.0 M sucrose solution at 25 °C. A cell with Ψw = −1.2 MPa is placed in it. What happens to the cell?", size=26)
        lines = self.steps([r"\Psi_s = -\,i\,C\,R\,T",
                            r"i = 1 \quad (\text{sucrose does not ionise})",
                            r"T = 25 + 273 = 298\ \text{K}",
                            r"\Psi_s = -(1)(1.0)(0.00831)(298)",
                            r"\Psi_s = -2.48\ \text{MPa}"], size=36, buff=0.3)
        lines.next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        lines[-1].set_color(th.AMBER)
        says = ["Use psi s equals minus i C R T.",
                "Sucrose doesn't ionise, so i is one.",
                "T is twenty-five plus two seventy-three: two ninety-eight kelvin.",
                "R is zero point zero zero eight three one, in litre megapascal per mole per kelvin.",
                "Psi s is minus two point four eight megapascal."]
        with self.say("A worked example. One molar sucrose at twenty-five degrees. Find its solute potential, and the fate of a cell at minus one point two."):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        for ln, sy in zip(lines, says):
            with self.say(sy):
                self.play(Write(ln), run_time=1.0)
        nl = NumberLine(x_range=[-3, 0, 1], length=4.6, color=th.MUTED, include_numbers=True, font_size=24).move_to([3.6, -1.0, 0])
        mc = VGroup(Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI).move_to(nl.n2p(-1.2) + UP * 0.26), T("cell −1.2", size=22).move_to(nl.n2p(-1.2) + UP * 0.6))
        ms = VGroup(Triangle(fill_color=FOOD, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI).move_to(nl.n2p(-2.48) + UP * 0.26), T("solution −2.48", size=22, color=FOOD).move_to(nl.n2p(-2.48) + UP * 0.6 + LEFT * 0.1))
        ar = CurvedArrow(nl.n2p(-1.2) + UP * 0.95, nl.n2p(-2.48) + UP * 0.95, angle=0.8, color=WATER, stroke_width=4)
        ans = T("Water leaves the cell: it plasmolyses.", size=24, color=th.AMBER, weight="BOLD").move_to([3.3, -2.6, 0])
        with self.say("The solution is more negative than the cell, so water leaves the cell and it plasmolyses."):
            self.play(Create(nl), FadeIn(mc), FadeIn(ms))
            self.play(Create(ar))
            self.play(Write(ans))
        self.play(FadeOut(VGroup(head, prob, lines, nl, mc, ms, ar, ans)))

    def p1_plasmolysis(self):
        head = self.head("Plasmolysis")
        C = np.array([-3.2, -0.25, 0])
        W, Hh = 3.8, 2.6
        bath = RoundedRectangle(corner_radius=0.3, width=5.6, height=4.1, stroke_width=0, fill_color=WATER, fill_opacity=0.14).move_to(C)
        wall = Rectangle(width=W, height=Hh, stroke_color=PAR, stroke_width=7).move_to(C)
        s = ValueTracker(0.0)

        def proto():
            k = s.get_value()
            w = (W - 0.14) * (1 - 0.42 * k)
            h = (Hh - 0.14) * (1 - 0.34 * k)
            cr = min(h / 2 - 0.01, 0.06 + 1.1 * k)
            pr = RoundedRectangle(corner_radius=cr, width=w, height=h, stroke_color="#B6F5C4", stroke_width=2.5, fill_color="#1F4D33", fill_opacity=1).move_to(C)
            vac = RoundedRectangle(corner_radius=max(0.05, cr * 0.8), width=w * (0.78 - 0.25 * k), height=h * (0.72 - 0.25 * k), stroke_width=0, fill_color="#2B5F7F", fill_opacity=0.9).move_to(C + RIGHT * 0.15)
            nu = Dot(C + LEFT * (w / 2 - 0.22), radius=0.11, color="#B6F5C4")
            return VGroup(pr, vac, nu)

        cell = always_redraw(proto)
        npv = DecimalNumber(0.8, num_decimal_places=1, include_sign=True, font_size=42, color=PRS)
        rd = VGroup(M(r"\Psi_p =", size=42, color=PRS), npv).arrange(RIGHT, buff=0.2).move_to([3.4, 1.7, 0])
        npv.add_updater(lambda m: m.set_value(max(0.0, 0.8 * (1 - s.get_value() / 0.12))))
        cap = B.Captions(self, at=(3.4, -0.5, 0), width=5.6, size=27)
        with self.say("Now a turgid cell, psi p plus zero point eight."):
            self.play(FadeIn(head), FadeIn(bath), Create(wall), FadeIn(cell), FadeIn(rd))
            cap("Turgid", color=th.MINT, sub="Protoplast pressed against the wall; Ψp positive.")
        flows = [B.Flow(C + d * 0.6, C + d * 2.4, n=4, r=0.05, speed=0.7, width=0.8, seed=i) for i, d in enumerate([LEFT, RIGHT, UP * 0.55, DOWN * 0.55])]
        with self.say("Put it in that sucrose. Water leaves, pressure falls, and the protoplast just starts to leave the wall. Psi p is zero: incipient plasmolysis.") as v:
            self.play(bath.animate.set_fill(FOOD, opacity=0.16), run_time=0.8)
            self.add(*flows)
            self.play(s.animate.set_value(0.12), run_time=max(1.5, v.left * 0.45))
            cap("Incipient plasmolysis", color=th.AMBER, sub="Protoplast just begins to leave the wall. Ψp = 0, so Ψw = Ψs.")
        with self.say("More water leaves and the protoplast shrinks away: plasmolysed. The gap fills with sugar solution, because the wall is freely permeable.") as v:
            self.play(s.animate.set_value(1.0), run_time=max(2, v.left * 0.6))
            cap("Plasmolysed", color=th.CORAL, sub="The gap between wall and protoplast fills with the outside solution: the wall is freely permeable.")
        self.play(*[FadeOut(fw) for fw in flows], run_time=0.4)
        self.remove(*flows)
        back = [B.Flow(C + d * 2.4, C + d * 0.8, n=4, r=0.05, speed=0.7, width=0.8, seed=i + 9) for i, d in enumerate([LEFT, RIGHT, UP * 0.55, DOWN * 0.55])]
        with self.say("Back in water it recovers: deplasmolysis. Only a living cell can do this.") as v:
            self.play(bath.animate.set_fill(WATER, opacity=0.14), run_time=0.6)
            self.add(*back)
            cap("Deplasmolysis", color=WATER, sub="Back in water, the cell recovers: proof the protoplast is alive.")
            self.play(s.animate.set_value(0.0), run_time=max(2, v.left - 0.4))
        npv.clear_updaters()
        cap.clear()
        self.play(FadeOut(VGroup(head, bath, wall, cell, rd, *back)))
        self.remove(cell, *back)

    def p1_root(self):
        y0, hh, cw, gap = 0.1, 1.5, 1.25, 0.14
        xs = [-4.6, -3.2, -1.8, -0.4, 1.0, 2.4]
        names = ["root hair cell", "cortex", "cortex", "cortex", "endodermis", "pericycle"]
        cols = [th.TEAL, PAR, PAR, PAR, ENDO, B.PERI]
        row, up = VGroup(), VGroup()
        for x, c in zip(xs, cols):
            row.add(RoundedRectangle(corner_radius=0.15, width=cw, height=hh, stroke_color=c, stroke_width=2.5, fill_color=PARF, fill_opacity=1).move_to([x, y0, 0]))
            up.add(RoundedRectangle(corner_radius=0.15, width=cw, height=hh, stroke_color=c, stroke_width=2, fill_color=PARF, fill_opacity=0.6, stroke_opacity=0.5).move_to([x, y0 + hh + gap, 0]))
        hair = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.28, stroke_color=th.TEAL, stroke_width=2.5, fill_color=PARF, fill_opacity=1).move_to([-5.95, y0 + 0.25, 0])
        soil = VGroup(*[Circle(radius=r, stroke_width=0, fill_color="#5A4632", fill_opacity=1).move_to(p) for r, p in [(0.25, [-6.3, -0.5, 0]), (0.2, [-5.7, 0.8, 0]), (0.18, [-6.4, 0.95, 0]), (0.22, [-5.6, -0.6, 0])]])
        xv = B.vessel(h=3.2, w=0.75, center=[3.8, y0 + 0.75, 0], kind="pitted", segs=3)
        labs = VGroup(*[T(n, size=19, color=c).move_to([x, y0 - hh / 2 - 0.25, 0]) for x, n, c in zip(xs, names, cols)], T("xylem", size=19, color=XYL).move_to([3.8, y0 - hh / 2 - 0.25, 0]))
        wy = y0 + hh / 2 + gap / 2
        cs = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.5, height=0.16, stroke_width=0, fill_color="#FF9F43", fill_opacity=1).move_to([1.0, y, 0]) for y in (wy, y0 - hh / 2 - gap / 2)])
        apo = VMobject().set_points_as_corners([[-6.6, y0 + 0.25, 0], [-5.3, y0 + 0.25, 0], [-5.3, wy, 0], [0.55, wy, 0], [0.55, y0 + 0.3, 0], [1.0, y0 + 0.3, 0], [1.75, y0 + 0.3, 0], [1.75, wy, 0], [3.4, wy, 0]])
        sym = VMobject().set_points_as_corners([[-6.6, y0 + 0.2, 0], [-4.6, y0 - 0.25, 0], [2.4, y0 - 0.25, 0], [3.4, y0 - 0.25, 0]])
        apo_l = DashedVMobject(apo.copy().set_stroke(WATER, 3), num_dashes=60)
        sym_l = DashedVMobject(sym.copy().set_stroke(th.MINT, 3), num_dashes=50)
        pd = VGroup(*[Line([x + cw / 2 + gap / 2, y0 - 0.4, 0], [x + cw / 2 + gap / 2, y0 - 0.1, 0], stroke_width=3, color=th.MINT) for x in xs[:-1]])
        cap = B.Captions(self, at=(0, -2.35, 0), width=12, size=26)
        with self.say("Water enters a root through root hairs, whose sap is more negative than the soil water."):
            self.play(FadeIn(row), FadeIn(up), FadeIn(hair), FadeIn(soil), FadeIn(xv), FadeIn(labs))
            cap("Root hair: Ψw more negative than the soil water, so water enters.", color=th.TEAL)
        with self.say("It crosses the cortex through cell walls, the apoplast, or from cytoplasm to cytoplasm through plasmodesmata, the symplast."):
            self.play(Create(apo_l), run_time=1.5)
            cap("Apoplast: through walls and spaces. Symplast: cytoplasm to cytoplasm via plasmodesmata.", color=WATER)
            self.play(Create(sym_l), FadeIn(pd), run_time=1.5)
            dots = VGroup(*[Dot(radius=0.08, color=WATER) for _ in range(3)], *[Dot(radius=0.08, color=th.MINT) for _ in range(3)])
            self.add(dots)
            self.play(LaggedStart(*[MoveAlongPath(d, apo) for d in dots[:3]], *[MoveAlongPath(d, sym) for d in dots[3:]], lag_ratio=0.12), run_time=3.0)
            self.remove(dots, *dots)
        with self.say("At the endodermis, the Casparian strip of lignin and suberin blocks the wall route. Everything must cross a living membrane."):
            self.play(FadeIn(cs, scale=1.5))
            self.play(Flash(cs[0].get_center(), color=th.AMBER, flash_radius=0.4), Indicate(row[4], color=ENDO))
            cap("Casparian strip: blocks the wall route; everything crosses a membrane.", color="#FF9F43")
        self.play(FadeOut(VGroup(row, up, hair, soil, labs, cs, apo_l, sym_l, pd)), xv.animate.move_to([-3.5, -0.2, 0]))
        cap.clear()
        ions = VGroup(*[T("K⁺", size=20, color=P.KION).move_to([-5.3, -1.6 + 0.5 * i, 0]) for i in range(4)])
        pr = Arrow([-3.5, -1.0, 0], [-3.5, 1.4, 0], buff=0, color=th.AMBER, stroke_width=7)
        drops = VGroup(*[Dot([-3.5 + dx, 1.55, 0], radius=0.09, color=WATER) for dx in (-0.15, 0.0, 0.15)])
        cap2 = B.Captions(self, at=(2.6, -0.2, 0), width=6.6, size=27)
        with self.say("The endodermis also pumps ions into the xylem. Water follows by osmosis, creating root pressure."):
            self.play(LaggedStart(*[i_.animate.move_to([-3.5, -1.6 + 0.6 * k, 0]) for k, i_ in enumerate(ions)], lag_ratio=0.2), run_time=1.6)
            self.play(GrowArrow(pr), FadeIn(drops, shift=UP * 0.3))
            cap2("Root pressure", color=th.AMBER, sub="Ions pumped into the xylem; water follows osmotically. Typically 0.1 to 0.2 MPa.")
        cap2.clear()
        self.play(FadeOut(VGroup(xv, ions, pr, drops)))

    def p1_rootpressure(self):
        head = self.head("Can root pressure lift sap 30 m? No.")
        items = [("Too small", "0.1–0.2 MPa lifts water only about 10–20 m."),
                 ("Wrong time", "Highest at night; near zero at midday, when flow is greatest."),
                 ("Often absent", "Many conifers, such as pine, show none at all."),
                 ("Dead stems still work", "Sap keeps rising after the living cells are killed.")]
        cards = VGroup(*[B.card(self, a, b, w=5.6, h=1.55, color=th.CORAL, tsize=26, bsize=22) for a, b in items]).arrange_in_grid(2, 2, buff=(0.4, 0.3)).move_to([0, 0.3, 0])
        job = T("Its real job: refill air-blocked vessels overnight, and drive guttation.", size=26, color=th.MINT).move_to([0, -2.4, 0])
        with self.say("But root pressure cannot lift sap up a tree: it is far too small, it vanishes at midday, many conifers lack it, and sap still rises in killed stems.") as v:
            self.play(FadeIn(head))
            per = (v.dur - 1.0) / 4
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
                self.hold(per - 0.5)
        with self.say("Its real job is refilling air-blocked vessels at night, and guttation."):
            self.play(FadeIn(job, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, cards, job)))

    def p1_ascent(self):
        VX = -4.5
        ground = Line([-6.6, -2.8, 0], [-2.6, -2.8, 0], color=th.FAINT, stroke_width=3)
        ves = B.vessel(h=4.9, w=0.6, center=[VX, -0.3, 0], kind="pitted", segs=5)
        leaf = Ellipse(width=2.4, height=0.75, stroke_color=CHL, stroke_width=3, fill_color="#1F5E2A", fill_opacity=1).rotate(0.25).move_to([VX + 0.95, 2.45, 0])
        roots = VGroup(*[Line([VX, -2.75, 0], [VX + dx, -3.2, 0], color=ROOT, stroke_width=3) for dx in (-0.6, -0.2, 0.25, 0.6)])
        up = B.Flow([VX, -2.7, 0], [VX, 2.05, 0], n=16, speed=0.8, width=0.32, r=0.05)
        vap = B.Flow([VX + 1.5, 2.6, 0], [VX + 2.6, 3.0, 0], n=6, color="#C9D3E8", r=0.05, speed=0.6, width=0.4)
        cap = B.Captions(self, at=(3.3, 1.35, 0), width=6.0, size=27)
        with self.say("Back to the sal. Its xylem holds an unbroken thread of water. The cohesion tension theory of Dixon and Joly explains it with three pillars."):
            self.play(Create(ground), FadeIn(ves), FadeIn(leaf), FadeIn(roots))
            self.add(up)
            cap("Cohesion–tension theory", color=XYL, sub="Dixon and Joly, 1895: transpiration pull, cohesion, adhesion.")
        with self.say("One: transpiration pull. Water evaporates from leaf cell walls and escapes through stomata, tugging on the water behind it."):
            self.add(vap)
            cap("1. Transpiration pull", color=th.AMBER, sub="Evaporation from mesophyll cell walls pulls on the water column.")
        with self.say("So xylem water is under tension: its pressure potential is negative. The energy comes from the sun, not from metabolism."):
            cap("Xylem water is under tension", color=th.AMBER, sub="Ψp of xylem sap: about −0.5 to −3 MPa at midday. Energy: solar heat of evaporation.")
        mol = VGroup()
        xs = np.linspace(1.3, 5.5, 6)
        for k, x in enumerate(xs):
            o = Circle(radius=0.2, stroke_width=0, fill_color=WATER, fill_opacity=1).move_to([x, -1.6, 0])
            h1 = Dot(o.get_center() + polar(0.22, 0.6 + (k % 2) * 0.4), radius=0.08, color=WHITE)
            h2 = Dot(o.get_center() + polar(0.22, -0.6 - (k % 2) * 0.4), radius=0.08, color=WHITE)
            mol.add(VGroup(o, h1, h2))
        hb = VGroup(*[DashedLine(mol[k].get_center() + RIGHT * 0.3, mol[k + 1].get_center() + LEFT * 0.3, color=th.AMBER, stroke_width=3, dash_length=0.06) for k in range(5)])
        wallv = Line([1.0, -2.6, 0], [5.8, -2.6, 0], color=XYL, stroke_width=8)
        wl = T("vessel wall", size=20, color=XYL).move_to([3.4, -2.9, 0])
        ad = VGroup(*[DashedLine(m.get_center() + DOWN * 0.24, [m.get_center()[0], -2.55, 0], color=th.MINT, stroke_width=3, dash_length=0.06) for m in mol])
        with self.say("Two: cohesion. Hydrogen bonds hold water molecules together, so the column doesn't snap."):
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mol], lag_ratio=0.1))
            self.play(Create(hb))
            cap("2. Cohesion", color=th.AMBER, sub="Hydrogen bonds hold water molecules together: the column does not snap.")
            self.play(VGroup(mol, hb).animate.shift(UP * 0.25), rate_func=there_and_back, run_time=1.2)
        with self.say("Three: adhesion. Water clings to the vessel walls."):
            self.play(Create(wallv), FadeIn(wl))
            self.play(Create(ad))
            cap("3. Adhesion", color=th.MINT, sub="Water sticks to the lignocellulose vessel walls.")
        self.play(FadeOut(VGroup(mol, hb, wallv, wl, ad)))
        lad = [("soil", "−0.015", -2.55), ("root xylem", "−0.6", -1.5), ("trunk xylem", "−1.2", 0.0), ("leaf", "−2.0", 1.6), ("air, 50% humidity", "about −93", 3.0)]
        chips = VGroup()
        for name, val, y in lad:
            ch = P.chip(f"{name}: {val} MPa", color=th.INK if y < 2.9 else th.CORAL, size=20, edge=XYL if y < 2.9 else th.CORAL)
            ch.move_to([-1.5, min(y, 2.75), 0])
            chips.add(ch)
        chips[-1].move_to([0.2, 2.85, 0])
        with self.say("Water potential falls all the way: soil, root, trunk, leaf, and then minus ninety-three in dry air. That last huge step does the pulling.") as v:
            cap.clear()
            per = (v.dur - 0.6) / 5
            for ch in chips:
                self.play(FadeIn(ch, shift=RIGHT * 0.2), run_time=0.45)
                self.hold(per - 0.45)
        nb = B.neby_in(self, "success", height=1.3)
        with self.say("So the sal has no pump at the bottom. The sun pulls from the top, and the water column is the rope."):
            cap("The sun pulls; the water column is the rope.", color=th.AMBER)
        B.neby_out(self, nb)
        with self.say("Living-pump theories died when Strasburger poisoned oak trunks and sap still rose. Capillarity lifts water only about sixty centimetres."):
            cap("Why other theories fail", color=th.CORAL, sub="Strasburger: sap rises in poisoned trunks. Capillarity: only about 0.6 m.")
        cap.clear()
        self.play(FadeOut(VGroup(ground, ves, leaf, roots, up, vap, chips)))
        self.remove(up, vap)
        self.quiz("In the xylem of a rapidly transpiring tree, the pressure potential Ψp is",
                  ["positive and large", "negative", "always zero", "equal to Ψs"], 1,
                  "Pause and think. What is the sign of pressure potential in xylem at midday?",
                  "Negative: the column is under tension. Positive is the trap; that describes a turgid cell or root pressure at night.")

    def p1_stomata(self):
        C = np.array([-3.5, -0.2, 0])
        o = ValueTracker(0.0)
        gc = always_redraw(lambda: P.guard_pair(o.get_value(), c=C, H=1.55, w=0.72))
        epi = VGroup()
        for dx, dy, w_, h_ in [(-2.0, 1.1, 1.3, 1.3), (-2.1, -0.4, 1.3, 1.4), (-2.0, -1.8, 1.3, 1.1), (2.0, 1.1, 1.3, 1.3), (2.1, -0.4, 1.3, 1.4), (2.0, -1.8, 1.3, 1.1), (0, 2.25, 2.4, 0.7), (0, -2.65, 2.4, 0.6)]:
            epi.add(RoundedRectangle(corner_radius=0.25, width=w_, height=h_, stroke_color=EPI, stroke_width=2, stroke_opacity=0.6, fill_color="#163B38", fill_opacity=0.7).move_to(C + [dx, dy, 0]))
        cap = B.Captions(self, at=(3.2, -0.2, 0), width=6.2, size=27)
        with self.say("Most absorbed water is lost as vapour, mostly through stomata: transpiration, the price of letting carbon dioxide in. Each stoma is a pore between two kidney-shaped guard cells, which have chloroplasts and a thick inner wall."):
            self.play(FadeIn(epi), FadeIn(gc))
            cap("Guard cells", color=P.GC_STROKE, sub="Kidney-shaped, with chloroplasts; thick inner wall facing the pore.")
        mic = always_redraw(lambda: P.guard_pair(o.get_value(), c=C, H=1.55, w=0.72, micel=True, chl=False))
        with self.say("Cellulose microfibrils hoop around each guard cell: radial micellation. So swelling makes the cells longer, not fatter, and they bow apart."):
            self.play(FadeIn(mic))
            cap("Radial micellation", color=P.GC_STROKE, sub="Hoop-like microfibrils: turgor makes the cells longer, so they bow apart.")
        self.play(FadeOut(mic))
        self.remove(mic)
        hs = VGroup(*[T("H⁺", size=22, color=HPC, weight="BOLD").move_to(P.guard_inside(0.0, C, 1.55, 0.72, k, sgn)) for k, sgn in [(0, -1), (2, -1), (1, 1), (3, 1)]])
        ks = VGroup(*[T("K⁺", size=22, color=P.KION, weight="BOLD").move_to(C + [sgn * 2.0, y, 0]) for sgn, y in [(-1, 1.1), (-1, -0.4), (-1, -1.6), (1, 1.1), (1, -0.4), (1, -1.6)]])
        cl = VGroup(*[T("Cl⁻", size=20, color=th.SKY).move_to(C + [sgn * 2.05, y, 0]) for sgn, y in [(-1, 0.35), (1, 0.35)]])
        with self.say("Blue light switches on a proton pump. Protons leave the guard cells, and the inside turns negative."):
            self.play(FadeIn(hs))
            self.play(*[h_.animate.move_to(C + [(-1 if i < 2 else 1) * 2.0, 0.75 - i * 0.7 if i < 2 else 0.75 - (i - 2) * 0.7, 0]).set_opacity(0.5) for i, h_ in enumerate(hs)], run_time=1.5)
            cap("Blue light → proton pump", color=HPC, sub="H⁺ pumped out; the guard cell's inside turns strongly negative.")
        with self.say("Potassium ions flood in, with chloride and malate to balance the charge."):
            self.play(FadeIn(ks), FadeIn(cl))
            targets = [P.guard_inside(0.0, C, 1.55, 0.72, k, sgn) for sgn, k in [(-1, 0), (-1, 1), (-1, 2), (1, 0), (1, 1), (1, 2)]]
            self.play(*[k_.animate.move_to(t_) for k_, t_ in zip(ks, targets)], *[c_.animate.move_to(P.guard_inside(0.0, C, 1.55, 0.72, 3, s_)) for c_, s_ in zip(cl, (-1, 1))], run_time=1.6)
            cap("K⁺ floods in", color=P.KION, sub="With Cl⁻, and malate made from starch, to balance the charge.")
        ions = VGroup(ks, cl)
        with self.say("Psi s drops, water rushes in, the cells bow apart, and the pore opens.") as v:
            self.play(o.animate.set_value(1.0), *[k_.animate.shift(RIGHT * (-0.42 if i < 3 else 0.42)) for i, k_ in enumerate(ks)],
                      *[c_.animate.shift(RIGHT * (-0.4 if i == 0 else 0.4)) for i, c_ in enumerate(cl)], run_time=max(2, v.left - 0.6))
            cap("Ψs falls → water enters → pore opens", color=th.MINT)
        with self.say("Under water stress, A B A makes them lose potassium, and the pore closes.") as v:
            cap("ABA → K⁺ out → pore closes", color=th.CORAL, sub="The water-stress signal.")
            self.play(*[k_.animate.move_to(C + [(-1 if i < 3 else 1) * 2.0, 1.1 - (i % 3) * 1.35, 0]).set_opacity(0.4) for i, k_ in enumerate(ks)],
                      FadeOut(cl), o.animate.set_value(0.0), run_time=max(2, v.left - 0.6))
        cap.clear()
        self.play(FadeOut(VGroup(epi, gc, ks, hs)))
        self.remove(gc)
        w = self.callout("careful", "The starch–sugar theory is history. Onion guard cells contain no starch at all, yet open and close normally, using KCl. Write about K⁺ movement.", width=10.5)
        with self.say("Note: the old starch sugar theory is obsolete. Onion guard cells have no starch, yet work perfectly."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(w))

    def p1_guttation(self):
        head = self.head("Guttation")
        leaf = VMobject(stroke_color=CHL, stroke_width=3, fill_color="#1F5E2A", fill_opacity=1)
        pts = [[-3.4, -1.6, 0], [-5.4, -0.2, 0], [-4.8, 1.4, 0], [-3.4, 2.2, 0], [-2.0, 1.4, 0], [-1.4, -0.2, 0], [-3.4, -1.6, 0]]
        leaf.set_points_smoothly(pts)
        vein = VGroup(Line([-3.4, -2.4, 0], [-3.4, 2.0, 0], color="#8FD694", stroke_width=3), *[Line([-3.4, y, 0], [-3.4 + s * 1.5, y + 0.8, 0], color="#8FD694", stroke_width=2) for y in (-0.6, 0.3) for s in (-1, 1)])
        tips = [[-3.4, 2.25, 0], [-5.0, 0.4, 0], [-1.8, 0.4, 0], [-4.75, 1.3, 0], [-2.05, 1.3, 0]]
        drops = VGroup(*[Circle(radius=0.13, stroke_color=WHITE, stroke_width=1.5, fill_color=WATER, fill_opacity=0.85).move_to(p) for p in tips])
        cap = B.Captions(self, at=(3.2, -0.2, 0), width=6.0, size=27)
        with self.say("On humid mornings, drops form at leaf tips and margins. This is guttation: liquid sap pushed out through hydathodes by root pressure."):
            self.play(FadeIn(head), DrawBorderThenFill(leaf), Create(vein))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in drops], lag_ratio=0.25), run_time=1.5)
            cap("Guttation", color=WATER, sub="Liquid xylem sap exuded through hydathodes at leaf margins and tips.")
        with self.say("It happens when root pressure is high and transpiration low: at night, in moist soil and humid air."):
            cap("Root pressure high, transpiration low", color=WATER, sub="Night and dawn; moist soil, humid air. Water pore: a permanently open modified stoma.")
        cap.clear()
        self.play(FadeOut(VGroup(leaf, vein, drops)))
        rows = [["", "Guttation", "Dew"], ["source", "xylem sap, from inside", "water vapour of the air"], ["cause", "root pressure", "cooling below dew point"],
                ["where", "hydathodes, margins and tips", "any cold surface, even stone"], ["contents", "dilute salts and sugars: leaves a crust", "pure water: no residue"]]
        tb = B.table(rows, [2.2, 4.9, 4.9], row_h=0.66, size=24, colors=[th.MUTED, WATER, th.INK]).move_to([0, -0.4, 0])
        with self.say("Unlike dew, guttation water comes from inside the plant and leaves a salty crust; dew is pure, condensed from air.") as v:
            B.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(VGroup(head, tb)))

    # ================================================================== PART 2: PHOTOSYNTHESIS
    def p2(self):
        self.section(1)
        self.p2_equation()
        self.p2_chloroplast()
        self.p2_zscheme()
        self.p2_chemiosmosis()
        self.p2_calvin()
        self.p2_photoresp()
        self.p2_c4()
        self.p2_cam()
        self.p2_factors()

    def p2_equation(self):
        eq = M(r"6\,\mathrm{CO_2}", "+", r"12\,\mathrm{H_2O}", r"\xrightarrow[\text{chlorophyll}]{\text{light}}", r"\mathrm{C_6H_{12}O_6}", "+", r"6\,\mathrm{O_2}", "+", r"6\,\mathrm{H_2O}", size=50).move_to([0, 0.9, 0])
        with self.say("Photosynthesis: six carbon dioxide plus twelve water give glucose, six oxygen, and six water."):
            self.play(Write(eq), run_time=2.5)
        arc = CurvedArrow(eq[2].get_bottom() + DOWN * 0.15, eq[6].get_bottom() + DOWN * 0.15, angle=0.6, color=WATER, stroke_width=4)
        lab = para("Every O₂ released comes from water: 12 H₂O carry exactly the 12 O atoms of 6 O₂. Proved with heavy oxygen, ¹⁸O, in 1941.", width=11, size=26, color=th.BODY).move_to([0, -1.6, 0])
        with self.say("Why twelve water? Because all the oxygen released comes from water. Heavy-oxygen experiments in nineteen forty-one proved it."):
            self.play(eq[2].animate.set_color(WATER), eq[6].animate.set_color(WATER))
            self.play(Create(arc))
            self.play(FadeIn(lab, shift=UP * 0.2))
        self.play(FadeOut(VGroup(eq, arc, lab)))

    def p2_chloroplast(self):
        C = np.array([-2.6, -0.2, 0])
        outer = Ellipse(width=7.0, height=3.9, stroke_color=CHL, stroke_width=3.5, fill_color="#10261A", fill_opacity=1).move_to(C)
        inner = Ellipse(width=6.7, height=3.6, stroke_color=CHL, stroke_width=2, fill_color="#13301C", fill_opacity=1).move_to(C)
        grana = VGroup()
        gx = [-2.2, -0.9, 0.4, 1.7]
        gy = [0.35, -0.55, 0.45, -0.35]
        for x, y in zip(gx, gy):
            st = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.85, height=0.13, stroke_color="#B9F5C0", stroke_width=1.2, fill_color=CHL, fill_opacity=0.9).move_to(C + [x, y + (k - 3) * 0.17, 0]) for k in range(7)])
            grana.add(st)
        lam = VGroup(*[Line(C + [gx[i] + 0.42, gy[i] + 0.1, 0], C + [gx[i + 1] - 0.42, gy[i + 1] - 0.1, 0], color="#B9F5C0", stroke_width=2.5) for i in range(3)])
        starch = Ellipse(width=0.7, height=0.4, stroke_width=0, fill_color="#EDE6C8", fill_opacity=0.85).move_to(C + [-0.3, 1.05, 0])
        dna = Circle(radius=0.18, stroke_color=th.PINK, stroke_width=2).move_to(C + [2.4, 0.9, 0])
        ribo = VGroup(*[Dot(C + [x, y, 0], radius=0.035, color=th.AMBER) for x, y in [(-2.7, -0.9), (-1.6, 1.0), (0.9, -1.2), (2.7, -0.4), (1.2, 1.1), (-0.3, -1.3)]])
        chl = VGroup(outer, inner, lam, grana, starch, dna, ribo)
        cap = B.Captions(self, at=(4.0, -0.2, 0), width=4.9, size=26)
        with self.say("It happens in the chloroplast. Two membranes enclose the stroma, a fluid full of enzymes."):
            self.play(FadeIn(chl, scale=0.9), run_time=1.2)
            cap("Stroma", color=th.MINT, sub="Enzymes of carbon fixation, circular DNA, 70S ribosomes, starch.")
            self.play(Indicate(inner, color=th.MINT, scale_factor=1.02))
        with self.say("Inside are thylakoids, stacked into grana. Their inner space is the lumen."):
            self.play(LaggedStart(*[Indicate(g_, color=th.AMBER, scale_factor=1.1) for g_ in grana], lag_ratio=0.2))
            cap("Thylakoids → grana", color=CHL, sub="Stacks of membrane sacs, linked by stroma lamellae. Inside each sac: the lumen.")
        with self.say("Light reaction: thylakoids. Dark reaction: stroma."):
            cap("Light reaction: thylakoid. Dark reaction: stroma.", color=th.AMBER)
        cap.clear()
        self.play(FadeOut(chl))
        ax = Axes(x_range=[400, 700, 50], y_range=[0, 1.1, 0.5], x_length=8.5, y_length=3.0, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2},
                  x_axis_config={"numbers_to_include": [400, 500, 600, 700], "font_size": 22}).move_to([0, 0.2, 0])
        spec = VGroup()
        for k in range(60):
            lam_ = 400 + 300 * (k + 0.5) / 60
            hue = np.clip((lam_ - 400) / 300, 0, 1)
            col = interpolate_color(ManimColor("#6A3DFF"), ManimColor("#2EC4B6"), min(1, hue * 2.2)) if hue < 0.45 else interpolate_color(ManimColor("#57D163"), ManimColor("#FF4B4B"), (hue - 0.45) / 0.55)
            spec.add(Rectangle(width=8.5 / 60 + 0.01, height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(ax.c2p(lam_, 0) + DOWN * 0.75))
        ca = ax.plot(lambda x: 0.95 * np.exp(-((x - 430) / 18) ** 2) + 0.75 * np.exp(-((x - 662) / 14) ** 2) + 0.05, x_range=[400, 700], color=CHL, stroke_width=4)
        cb = ax.plot(lambda x: 1.0 * np.exp(-((x - 455) / 16) ** 2) + 0.45 * np.exp(-((x - 642) / 13) ** 2) + 0.04, x_range=[400, 700], color=th.TEAL, stroke_width=3)
        lab = VGroup(T("chlorophyll a", size=22, color=CHL), T("chlorophyll b", size=22, color=th.TEAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(560, 0.9))
        yl = T("absorption", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.2)
        xl = T("wavelength (nm)", size=22, color=th.MUTED).move_to(ax.c2p(550, 0) + DOWN * 1.15)
        note = T("blue and red absorbed; green reflected", size=24, color=th.BODY).move_to([0, -2.95, 0])
        with self.say("Chlorophyll a is the reaction-centre pigment. Chlorophyll b and carotenoids are accessory pigments that pass energy to it.") as v:
            self.play(Create(ax), FadeIn(spec), FadeIn(yl), FadeIn(xl))
            self.play(Create(ca), Create(cb), FadeIn(lab), run_time=2.0)
        with self.say("Chlorophyll absorbs blue and red light and reflects green."):
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(ax, spec, ca, cb, lab, yl, xl, note)))

    def p2_zscheme(self):
        pos = {"P680": (-5.0, -1.9), "P680*": (-5.0, 1.7), "Pheo": (-4.05, 1.2), "PQ": (-3.15, 0.55), "b6f": (-2.25, -0.05), "PC": (-1.35, -0.5),
               "P700": (-0.45, -0.85), "P700*": (-0.45, 2.35), "Fd": (0.55, 1.75), "FNR": (1.45, 1.2), "NADPH": (2.45, 0.75)}
        lab = {"P680": "P680", "P680*": "P680*", "Pheo": "pheophytin", "PQ": "PQ", "b6f": "cyt b₆f", "PC": "PC", "P700": "P700", "P700*": "P700*", "Fd": "Fd", "FNR": "FNR", "NADPH": "NADP⁺→NADPH"}
        colr = {"P680": th.SKY, "P680*": th.SKY, "P700": th.PINK, "P700*": th.PINK, "NADPH": th.MINT}
        nodes = {}
        for k, (x, y) in pos.items():
            nodes[k] = P.chip(lab[k], color=colr.get(k, th.INK), size=19 if k != "Pheo" else 17, edge=colr.get(k, th.PANEL_EDGE)).move_to([x, y, 0])
        order = ["P680", "P680*", "Pheo", "PQ", "b6f", "PC", "P700", "P700*", "Fd", "FNR", "NADPH"]
        arrows = VGroup()
        for a, b in zip(order[:-1], order[1:]):
            jump = (a, b) in (("P680", "P680*"), ("P700", "P700*"))
            arrows.add(Arrow(np.array([*pos[a], 0]), np.array([*pos[b], 0]), buff=0.3, color=th.AMBER if jump else th.MUTED, stroke_width=6 if jump else 3, max_tip_length_to_length_ratio=0.12 if jump else 0.25))
        yax = Arrow([-6.35, -2.9, 0], [-6.35, 2.6, 0], buff=0, color=th.FAINT, stroke_width=3)
        yl = T("energy of electron", size=19, color=th.MUTED).rotate(PI / 2).move_to([-6.62, 0, 0])
        l1 = T("light", size=20, color=th.AMBER, weight="BOLD").move_to([-4.45, -0.55, 0])
        l2 = T("light", size=20, color=th.AMBER, weight="BOLD").move_to([0.1, 0.4, 0])
        h2o = P.chip("H₂O", color=WATER, size=20).move_to([-5.95, -2.45, 0])
        wa = Arrow(h2o.get_right(), nodes["P680"].get_bottom() + DOWN * 0.02, buff=0.08, color=WATER, stroke_width=3)
        cap = B.Captions(self, at=(4.95, -1.0, 0), width=3.2, size=23)
        ps = VGroup(T("PS II", size=22, color=th.SKY, weight="BOLD").move_to([-4.05, -1.9, 0]), T("PS I", size=22, color=th.PINK, weight="BOLD").move_to([0.45, -0.9, 0]))
        with self.say("The light reaction is the Z-scheme. Height shows electron energy. Photosystem two, P680, and photosystem one, P700, work in series."):
            self.play(Create(yax), FadeIn(yl))
            self.play(FadeIn(nodes["P680"]), FadeIn(nodes["P700"]), FadeIn(ps))
            cap("Two photosystems", sub="PS II: P680. PS I: P700. Both chlorophyll a. PS II acts first.")
        e = Dot(nodes["P680"].get_center(), radius=0.11, color=th.AMBER)
        glow = always_redraw(lambda: Circle(radius=0.2, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.35).move_to(e))
        with self.say("Light excites P680, and an electron jumps to pheophytin."):
            self.add(glow, e)
            self.play(FadeIn(nodes["P680*"]), FadeIn(l1), GrowArrow(arrows[0]))
            self.sfx("pop", gain=-10)
            self.play(e.animate.move_to(nodes["P680*"]), run_time=0.6, rate_func=rate_functions.ease_out_expo)
            self.play(FadeIn(nodes["Pheo"]), GrowArrow(arrows[1]))
            self.play(e.animate.move_to(nodes["Pheo"]), run_time=0.5)
        with self.say("It runs downhill through plastoquinone, cytochrome b6 f, and plastocyanin, pumping protons into the lumen."):
            for k in ("PQ", "b6f", "PC"):
                i = order.index(k)
                self.play(FadeIn(nodes[k]), GrowArrow(arrows[i - 1]), run_time=0.45)
                self.play(e.animate.move_to(nodes[k]), run_time=0.45)
            self.play(GrowArrow(arrows[5]), run_time=0.4)
            self.play(e.animate.move_to(nodes["P700"]), run_time=0.45)
            cap("Downhill: PQ → cyt b₆f → PC", sub="Energy released pumps H⁺ into the lumen.")
        with self.say("Light excites P700. The electron jumps again, then through ferredoxin to F N R, which makes NADPH."):
            self.play(FadeIn(nodes["P700*"]), FadeIn(l2), GrowArrow(arrows[6]))
            self.sfx("pop", gain=-10)
            self.play(e.animate.move_to(nodes["P700*"]), run_time=0.6, rate_func=rate_functions.ease_out_expo)
            for k in ("Fd", "FNR", "NADPH"):
                i = order.index(k)
                self.play(FadeIn(nodes[k]), GrowArrow(arrows[i - 1]), run_time=0.45)
                self.play(e.animate.move_to(nodes[k]), run_time=0.45)
            cap("NADP⁺ → NADPH", color=th.MINT, sub="At the stroma side, by ferredoxin–NADP⁺ reductase.")
        phot = M(r"2\,\mathrm{H_2O} \rightarrow \mathrm{O_2} + 4\,\mathrm{H^+} + 4\,e^-", size=34, color=WATER).move_to([-2.2, -2.6, 0])
        with self.say("P680 replaces its lost electron by splitting water. Photolysis releases oxygen and protons into the lumen."):
            self.play(FadeIn(h2o), GrowArrow(wa))
            self.play(Write(phot))
            cap("Photolysis of water", color=WATER, sub="At the Mn₄CaO₅ cluster, lumen side: O₂ and H⁺ released into the lumen.")
        with self.say("This one-way flow, from water to NADP plus, is non-cyclic photophosphorylation. It makes ATP, NADPH and oxygen."):
            self.play(e.animate.move_to(nodes["P680"]), run_time=0.01)
            path = VMobject().set_points_as_corners([nodes[k].get_center() for k in order])
            self.play(MoveAlongPath(e, path), run_time=3.0, rate_func=rate_functions.linear)
            cap("Non-cyclic", color=th.MINT, sub="Water → NADP⁺. Products: ATP + NADPH + O₂.")
        cyc = CurvedArrow(nodes["Fd"].get_top() + UP * 0.05, nodes["PQ"].get_top() + UP * 0.05, angle=0.9, color=th.PINK, stroke_width=4)
        with self.say("In cyclic flow, photosystem one works alone. Electrons loop back, making only ATP. No NADPH, no oxygen."):
            self.play(Create(cyc), VGroup(*[nodes[k] for k in ("P680", "P680*", "Pheo", "FNR", "NADPH")], h2o, wa, phot, arrows[0], arrows[1], arrows[2], arrows[9], arrows[8], l1).animate.set_opacity(0.25))
            loop = VMobject().set_points_as_corners([nodes[k].get_center() for k in ("P700", "P700*", "Fd")])
            back = VMobject().set_points_smoothly([nodes["Fd"].get_center(), (nodes["Fd"].get_center() + nodes["PQ"].get_center()) / 2 + UP * 1.0, nodes["PQ"].get_center()])
            loop2 = VMobject().set_points_as_corners([nodes[k].get_center() for k in ("PQ", "b6f", "PC", "P700")])
            self.play(e.animate.move_to(nodes["P700"]), run_time=0.3)
            for _ in range(2):
                self.play(MoveAlongPath(e, loop), run_time=0.8, rate_func=rate_functions.linear)
                self.play(MoveAlongPath(e, back), run_time=0.7, rate_func=rate_functions.linear)
                self.play(MoveAlongPath(e, loop2), run_time=0.8, rate_func=rate_functions.linear)
            cap("Cyclic", color=th.PINK, sub="PS I only. ATP only: no NADPH, no O₂.")
        cap.clear()
        self.play(FadeOut(VGroup(*nodes.values(), arrows, yax, yl, l1, l2, h2o, wa, phot, cyc, ps, e, glow)))
        self.remove(glow)

    def p2_chemiosmosis(self):
        mem = Rectangle(width=13.0, height=0.7, stroke_width=0, fill_color="#2A4A2A", fill_opacity=1).move_to([0, 0.15, 0])
        edges = VGroup(Line([-6.5, 0.5, 0], [6.5, 0.5, 0], color=CHL, stroke_width=2), Line([-6.5, -0.2, 0], [6.5, -0.2, 0], color=CHL, stroke_width=2))
        st = T("stroma", size=24, color=th.MUTED).move_to([-5.7, 1.9, 0])
        lu = T("lumen", size=24, color=th.MUTED).move_to([-5.7, -1.4, 0])
        cpx = VGroup()
        for x, name, c, w in [(-3.9, "PS II", th.SKY, 1.1), (-1.7, "cyt b₆f", th.INK, 1.0), (0.5, "PS I", th.PINK, 1.1)]:
            b = RoundedRectangle(corner_radius=0.2, width=w, height=1.3, stroke_color=c, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1).move_to([x, 0.15, 0])
            cpx.add(VGroup(b, T(name, size=20, color=c).move_to(b)))
        stalk = Rectangle(width=0.45, height=1.0, stroke_color=th.AMBER, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1).move_to([3.4, 0.15, 0])
        knob = Circle(radius=0.55, stroke_color=th.AMBER, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to([3.4, 1.15, 0])
        spokes = VGroup(*[Line([3.4, 1.15, 0], [3.4, 1.15, 0] + polar(0.45, a), color=th.AMBER, stroke_width=3) for a in np.linspace(0, TAU, 6, endpoint=False)])
        syn = VGroup(stalk, knob, spokes)
        sl = T("ATP synthase", size=20, color=th.AMBER).move_to([3.4, 2.0, 0])
        rg = np.random.default_rng(2)
        hp = VGroup(*[T("H⁺", size=18, color=HPC).move_to([rg.uniform(-4.6, 2.4), rg.uniform(-1.85, -0.55), 0]) for _ in range(16)])
        o2 = P.chip("O₂", color=O2C, size=20).move_to([-4.9, -1.0, 0])
        cap = B.Captions(self, at=(0, -2.65, 0), width=12.4, size=24)
        with self.say("In the thylakoid, protons build up inside the lumen."):
            self.play(FadeIn(mem), Create(edges), FadeIn(st), FadeIn(lu), FadeIn(cpx), FadeIn(syn), FadeIn(sl))
            self.play(FadeIn(o2, shift=DOWN * 0.2))
            self.play(LaggedStart(*[FadeIn(h_, shift=DOWN * 0.3) for h_ in hp], lag_ratio=0.08), run_time=2.0)
            cap("H⁺ accumulate in the lumen: from photolysis and from cytochrome b₆f.", color=HPC)
        out = B.Flow([3.4, -1.2, 0], [3.4, 1.0, 0], n=7, color=HPC, r=0.06, speed=0.9, width=0.15)
        atps = VGroup(*[P.chip("ATP", color=ATPC, size=20).move_to([4.6 + 0.9 * (k % 2), 1.0 + 0.55 * (k // 2), 0]) for k in range(4)])
        with self.say("They flow back through ATP synthase, which spins and makes ATP. This is chemiosmosis.") as v:
            self.add(out)
            self.play(FadeOut(hp[8:]), Rotate(spokes, TAU, about_point=knob.get_center()), run_time=1.5, rate_func=rate_functions.linear)
            self.play(Rotate(spokes, TAU, about_point=knob.get_center()), LaggedStart(*[FadeIn(a_, scale=0.5) for a_ in atps], lag_ratio=0.3), run_time=2.0, rate_func=rate_functions.linear)
            cap("H⁺ flow back through ATP synthase → ATP in the stroma.", color=ATPC)
        nad = P.chip("NADPH", color=th.MINT, size=20).move_to([0.5, 1.35, 0])
        with self.say("Oxygen is released in the lumen; ATP and NADPH form in the stroma."):
            self.play(FadeIn(nad, shift=UP * 0.2))
            self.play(Indicate(o2), Indicate(nad), Indicate(atps))
            cap("O₂: lumen side.  ATP and NADPH: stroma side.", color=th.INK)
        cap.clear()
        self.play(FadeOut(VGroup(mem, edges, st, lu, cpx, syn, sl, hp[:8], o2, out, atps, nad)))
        self.remove(out)
        rows = [["", "Non-cyclic", "Cyclic"], ["photosystems", "PS II and PS I", "PS I only"], ["electron path", "open: water → NADP⁺", "closed loop"],
                ["photolysis", "yes", "no"], ["products", "ATP + NADPH + O₂", "ATP only"], ["main site", "grana thylakoids", "stroma lamellae"]]
        tb = B.table(rows, [2.8, 4.6, 4.2], row_h=0.62, size=24, colors=[th.MUTED, th.MINT, th.PINK]).move_to([0, 0.5, 0])
        why = para("Why both? The Calvin cycle needs ATP : NADPH = 3 : 2 = 1.5. Non-cyclic flow gives only about 1.28, so cyclic flow tops up the ATP.", width=11.5, size=25, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Non-cyclic uses both photosystems, splits water, and makes ATP, NADPH and oxygen. Cyclic uses photosystem one only and makes ATP alone.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
        with self.say("Why both? The Calvin cycle needs ATP to NADPH at three to two. Non-cyclic gives less ATP, so cyclic tops it up."):
            self.play(FadeIn(why, shift=UP * 0.2))
        self.play(FadeOut(VGroup(tb, why)))
        self.quiz("Cyclic photophosphorylation produces",
                  ["ATP, NADPH and O₂", "NADPH only", "ATP only", "ATP and O₂ only"], 2,
                  "Pause and think. What does cyclic photophosphorylation produce?",
                  "ATP only. No water is split, so no oxygen; no NADPH is made. ATP and oxygen is the trap.")

    def p2_calvin(self):
        C = np.array([-2.9, -0.35, 0])
        R = 1.75
        ring = Circle(radius=R, stroke_color=th.FAINT, stroke_width=10).move_to(C)
        tips = VGroup(*[Triangle(fill_color=th.MUTED, fill_opacity=1, stroke_width=0).scale(0.13).rotate(np.arctan2(-np.cos(a), np.sin(a)) - PI / 2).move_to(C + polar(R, a)) for a in (PI / 6, -PI / 2, 5 * PI / 6)])
        nodes = {"rubp": (PI / 2, "3 RuBP", "3 × 5C = 15 C", th.MINT), "pga": (-PI / 6, "6 3-PGA", "6 × 3C = 18 C", th.SKY), "g3p": (7 * PI / 6, "6 G3P", "6 × 3C = 18 C", th.AMBER)}
        nd = {}
        for k, (a, t1, t2, c) in nodes.items():
            g = VGroup(T(t1, size=24, color=c, weight="BOLD"), T(t2, size=19, color=th.BODY)).arrange(DOWN, buff=0.06)
            b = RoundedRectangle(corner_radius=0.14, width=g.width + 0.35, height=g.height + 0.25, stroke_color=c, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1)
            nd[k] = VGroup(b, g.move_to(b)).move_to(C + polar(R, a))
        co2 = P.chip("3 CO₂ (3 C)", color=CO2C, size=21).move_to(C + [2.3, 2.15, 0])
        co2a = Arrow(co2.get_bottom(), C + polar(R + 0.05, PI / 6) + UP * 0.05, buff=0.08, color=CO2C, stroke_width=4)
        rub = T("RuBisCO", size=20, color=CO2C).next_to(co2, UP, buff=0.12)
        red = P.chip("6 ATP + 6 NADPH", color=ATPC, size=20).move_to(C + [0, -R - 0.75, 0])
        reda = Arrow(red.get_top(), C + polar(R - 0.05, -PI / 2) + DOWN * 0.02, buff=0.05, color=ATPC, stroke_width=4)
        reg = P.chip("3 ATP", color=ATPC, size=20).move_to(C + [-2.75, 1.7, 0])
        rega = Arrow(reg.get_bottom(), C + polar(R + 0.05, 5 * PI / 6), buff=0.06, color=ATPC, stroke_width=4)
        tally = P.Tally([("carbons", th.INK), ("ATP", ATPC), ("NADPH", NADH)], title="for 3 turns", w=3.3, size=26).move_to([4.6, 0.9, 0])
        stage = B.Captions(self, at=(4.6, -1.7, 0), width=3.9, size=24)
        marker = Dot(C + polar(R, PI / 2), radius=0.12, color=WHITE)
        ang = ValueTracker(PI / 2)
        marker.add_updater(lambda m: m.move_to(C + polar(R, ang.get_value())))
        with self.say("The Calvin cycle runs in the stroma, powered by ATP and NADPH."):
            self.play(Create(ring), FadeIn(tips), FadeIn(nd["rubp"]), FadeIn(tally))
            self.play(ChangeDecimalToValue(tally.vals["carbons"], 15))
        self.add(marker)
        with self.say("Three RuBP, fifteen carbons, plus three carbon dioxide make six 3-PGA, eighteen carbons, via RuBisCO."):
            self.play(FadeIn(co2, shift=DOWN * 0.2), GrowArrow(co2a), FadeIn(rub))
            self.play(ChangeDecimalToValue(tally.vals["carbons"], 18), ang.animate.set_value(-PI / 6), run_time=2.0)
            self.play(FadeIn(nd["pga"], scale=0.8))
            stage("1. Carboxylation", color=th.SKY, sub="RuBP + CO₂ → 2 × 3-PGA, by RuBisCO.")
        with self.say("3-PGA is the first stable product: these are C3 plants."):
            self.play(Indicate(nd["pga"], color=th.SKY))
        with self.say("Six ATP and six NADPH reduce it to six G3P."):
            self.play(FadeIn(red, shift=UP * 0.2), GrowArrow(reda))
            self.play(ang.animate.set_value(-5 * PI / 6), tally.bump("ATP", 6), tally.bump("NADPH", 6), run_time=2.0)
            self.play(FadeIn(nd["g3p"], scale=0.8))
            stage("2. Reduction", color=th.AMBER, sub="3-PGA → G3P, using 1 ATP + 1 NADPH each.")
        out = P.chip("1 G3P → sugar", color=th.AMBER, size=21).move_to(C + [-2.6, -2.35, 0])
        outa = Arrow(nd["g3p"].get_bottom(), out.get_top(), buff=0.06, color=th.AMBER, stroke_width=4)
        with self.say("One G3P leaves the cycle to make sugar."):
            self.play(GrowArrow(outa), FadeIn(out, shift=DOWN * 0.2), ChangeDecimalToValue(tally.vals["carbons"], 15))
            self.sfx("pop", gain=-10)
        with self.say("Five G3P regenerate three RuBP, using three ATP."):
            self.play(FadeIn(reg, shift=DOWN * 0.2), GrowArrow(rega))
            self.play(ang.animate.set_value(-3 * PI / 2), tally.bump("ATP", 9), run_time=2.2)
            stage("3. Regeneration", color=th.MINT, sub="5 G3P → 3 RuBP, using 3 ATP.")
        with self.say("So one G3P costs nine ATP and six NADPH."):
            self.play(Circumscribe(tally, color=th.AMBER))
        marker.clear_updaters()
        stage.clear()
        self.play(FadeOut(VGroup(ring, tips, *nd.values(), co2, co2a, rub, red, reda, reg, rega, out, outa, marker)), tally.animate.move_to([-4.4, 0.6, 0]))
        lines = self.steps([r"\text{per CO}_2:\ 3\ \text{ATP} + 2\ \text{NADPH}",
                            r"\text{glucose} = 6\,\text{C}\ \Rightarrow\ 6\ \text{turns}",
                            r"6 \times 3 = 18\ \text{ATP}, \quad 6 \times 2 = 12\ \text{NADPH}",
                            r"\text{ATP} : \text{NADPH} = 18 : 12 = 3 : 2"], size=38, buff=0.4).move_to([2.0, 0.3, 0])
        lines[2].set_color(th.AMBER)
        hd = T("How many ATP and NADPH per glucose?", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        says = ["Per carbon dioxide: three ATP and two NADPH.",
                "Glucose needs six turns.",
                "Eighteen ATP and twelve NADPH.",
                "Ratio: three to two."]
        self.play(FadeIn(hd))
        for ln, sy in zip(lines, says):
            with self.say(sy):
                self.play(Write(ln), run_time=1.2)
        nb = B.neby_in(self, "success", height=1.3)
        self.wait(0.6)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(hd, lines, tally)))

    def p2_photoresp(self):
        head = self.head("Photorespiration")
        rub = VGroup(Circle(radius=1.0, stroke_color=th.MINT, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), T("RuBisCO", size=26, color=th.MINT, weight="BOLD")).move_to([-3.2, 0.2, 0])
        site = Arc(radius=0.35, start_angle=-PI / 2 + 0.6, angle=PI - 1.2, color=th.MINT, stroke_width=5).move_to(rub.get_top() + DOWN * 0.15)
        co2 = P.chip("CO₂", color=CO2C, size=22).move_to([-4.6, 2.4, 0])
        o2 = P.chip("O₂", color=O2C, size=22).move_to([-1.8, 2.4, 0])
        cap = B.Captions(self, at=(3.3, -0.2, 0), width=6.0, size=26)
        with self.say("RuBisCO can also grab oxygen, since air has far more oxygen than carbon dioxide."):
            self.play(FadeIn(head), FadeIn(rub), FadeIn(co2), FadeIn(o2))
            self.play(co2.animate.shift(RIGHT * 0.3 + DOWN * 0.2), o2.animate.shift(LEFT * 0.3 + DOWN * 0.2), rate_func=there_and_back, run_time=1.2)
            cap("RuBisCO: carboxylase and oxygenase", color=th.MINT)
        prods = VGroup(P.chip("3-PGA", color=th.SKY, size=21), P.chip("2-phosphoglycolate (2C)", color=th.CORAL, size=21)).arrange(DOWN, buff=0.3).move_to([-3.2, -2.1, 0])
        with self.say("Then it makes a useless two-carbon compound, salvaged at a loss of carbon: photorespiration."):
            self.play(o2.animate.move_to(rub.get_top() + DOWN * 0.1), FadeOut(co2), run_time=1.0)
            self.sfx("wrong", gain=-14)
            self.play(FadeIn(prods, shift=DOWN * 0.2))
            cap("Photorespiration", color=th.CORAL, sub="O₂ fixed instead of CO₂: carbon lost via chloroplast → peroxisome → mitochondrion.")
        with self.say("It worsens on hot, dry days when stomata close."):
            cap("Worse when hot and dry", color=th.CORAL, sub="Closed stomata: CO₂ falls, O₂ rises inside the leaf.")
        cap.clear()
        self.play(FadeOut(VGroup(head, rub, o2, prods)))

    def p2_c4(self):
        K = np.array([-3.3, -0.25, 0])
        vein = VGroup(*[Circle(radius=0.11, stroke_color=XYL, stroke_width=2, fill_color=XYL, fill_opacity=0.3).move_to(K + [dx, 0.15, 0]) for dx in (-0.22, 0, 0.22)],
                      *[Circle(radius=0.08, stroke_width=0, fill_color=PHL, fill_opacity=0.9).move_to(K + [dx, -0.2, 0]) for dx in (-0.15, 0.0, 0.15)])
        bs, bsc = VGroup(), []
        for k in range(8):
            a = TAU * k / 8 + PI / 8
            c = K + polar(0.95, a)
            bsc.append(c)
            bs.add(Circle(radius=0.36, stroke_color="#D8F5B0", stroke_width=2.5, fill_color="#20402A", fill_opacity=1).move_to(c))
            bs.add(*[Dot(c + polar(0.22, a + PI + d), radius=0.05, color=CHL) for d in (-0.6, -0.3, 0, 0.3, 0.6)])
        ms, msc = VGroup(), []
        for k in range(12):
            a = TAU * k / 12
            c = K + polar(1.85, a)
            msc.append(c)
            ms.add(Ellipse(width=0.62, height=0.78, stroke_color=PAR, stroke_width=2, fill_color=PARF, fill_opacity=1).rotate(a).move_to(c))
            ms.add(*[Dot(c + polar(0.17, a + d), radius=0.035, color=CHL) for d in (1.5, 3.1, 4.7)])
        lab_b = T("bundle sheath", size=20, color="#D8F5B0").move_to(K + [0, -2.75, 0])
        cap = B.Captions(self, at=(3.6, -0.2, 0), width=5.6, size=26)
        with self.say("C4 plants like maize and sugarcane avoid it with Kranz anatomy: bundle-sheath cells ring each vein, surrounded by mesophyll."):
            self.play(FadeIn(vein))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in bs], lag_ratio=0.01), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in ms], lag_ratio=0.01), run_time=1.0)
            cap("Kranz anatomy", color="#D8F5B0", sub="Vein → ring of bundle-sheath cells → ring of mesophyll cells.")
        a = PI / 3
        mc, bc = K + polar(1.85, a), K + polar(0.95, a + PI / 8 - PI / 8)
        bc = bsc[1]
        mc = msc[2]
        mol = P.chip("CO₂", color=CO2C, size=19).move_to(K + polar(3.0, PI / 3) + RIGHT * 0.3)
        with self.say("In the mesophyll, PEP carboxylase fixes carbon dioxide into oxaloacetate, a four-carbon acid."):
            self.play(FadeIn(mol, shift=DOWN * 0.2))
            self.play(mol.animate.move_to(mc), run_time=1.0)
            self.play(Transform(mol, P.chip("OAA (4C)", color=th.AMBER, size=19).move_to(mc)))
            cap("Mesophyll: PEP carboxylase", color=th.AMBER, sub="PEP (3C) + CO₂ → oxaloacetate (4C). No oxygenase activity at all.")
        with self.say("This becomes malate, which moves into the bundle sheath and releases carbon dioxide around RuBisCO."):
            self.play(Transform(mol, P.chip("malate (4C)", color=th.AMBER, size=19).move_to(mc)))
            self.play(mol.animate.move_to(bc), run_time=1.0)
            burst = VGroup(*[P.chip("CO₂", color=CO2C, size=16).move_to(K + polar(0.42, a_)) for a_ in np.linspace(0, TAU, 5, endpoint=False)])
            self.play(Transform(mol, P.chip("pyruvate (3C)", color=th.SKY, size=19).move_to(bc)), FadeIn(burst, scale=0.5))
            cap("Bundle sheath: CO₂ released", color=CO2C, sub="CO₂ 10–20 × air around RuBisCO → Calvin cycle runs, photorespiration suppressed.")
        with self.say("Pyruvate returns and is recycled to PEP, costing extra ATP: thirty per glucose instead of eighteen."):
            self.play(mol.animate.move_to(mc), run_time=1.0)
            self.play(Transform(mol, P.chip("PEP (3C)  −2 ATP", color=th.AMBER, size=19).move_to(mc)))
            cap("Cost: 5 ATP + 2 NADPH per CO₂", color=ATPC, sub="30 ATP per glucose, against 18 in a C3 plant.")
        with self.say("C4 separates the steps in space."):
            cap("Separation in SPACE", color=th.MINT, sub="Mesophyll: PEP carboxylase, no RuBisCO. Bundle sheath: RuBisCO and the Calvin cycle.")
        cap.clear()
        self.play(FadeOut(VGroup(vein, bs, ms, mol, burst)))
        self.quiz("The first stable product of the C4 pathway is",
                  ["3-phosphoglyceric acid", "phosphoenolpyruvate", "oxaloacetic acid", "malic acid"], 2,
                  "Pause and think. What is the first stable product of C4 photosynthesis?",
                  "Oxaloacetic acid, four carbons. Malic acid is the trap: it forms one step later. PEP is the acceptor, and 3-PGA is the C3 product.")

    def p2_cam(self):
        C = np.array([-3.2, -0.3, 0])
        night = ValueTracker(0.0)   # 0 day .. 1 night
        acid = ValueTracker(0.1)

        def scene_():
            n = night.get_value()
            bg = RoundedRectangle(corner_radius=0.3, width=5.6, height=4.6, stroke_width=0, fill_color=interpolate_color(ManimColor("#3A3410"), ManimColor("#101838"), n), fill_opacity=0.9).move_to(C)
            cell = RoundedRectangle(corner_radius=0.35, width=3.4, height=2.6, stroke_color=PAR, stroke_width=4, fill_color=PARF, fill_opacity=1).move_to(C + DOWN * 0.3)
            vac = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.8, stroke_color="#7FB8D8", stroke_width=2, fill_color="#1B3A50", fill_opacity=1).move_to(C + DOWN * 0.3)
            lev = acid.get_value()
            fillr = Rectangle(width=2.5, height=max(0.02, 1.7 * lev), stroke_width=0, fill_color=FOOD, fill_opacity=0.75)
            fillr.move_to(vac.get_bottom() + UP * (0.05 + fillr.height / 2))
            st = P.guard_pair(n, c=C + [0, 1.6, 0], H=0.45, w=0.22, chl=False)
            return VGroup(bg, cell, vac, fillr, st)

        sc = always_redraw(scene_)
        sun = Circle(radius=0.32, stroke_width=0, fill_color=th.AMBER, fill_opacity=1).move_to(C + [2.2, 1.85, 0])
        moon = VGroup(Circle(radius=0.3, stroke_width=0, fill_color="#E6ECFF", fill_opacity=1), Circle(radius=0.27, stroke_width=0, fill_color="#101838", fill_opacity=1).shift(RIGHT * 0.13 + UP * 0.08)).move_to(C + [2.2, 1.85, 0])
        al = T("malic acid in the vacuole", size=20, color=FOOD).move_to(C + [0, -2.25, 0])
        cap = B.Captions(self, at=(3.5, -0.2, 0), width=5.6, size=26)
        with self.say("CAM plants like pineapple and aloe separate the steps in time."):
            self.play(FadeIn(sc), FadeIn(sun), FadeIn(al))
            cap("CAM plants", color=FOOD, sub="Pineapple, Opuntia, Aloe vera (ghiukumari).")
        with self.say("At night, stomata open and carbon dioxide is stored as malic acid.") as v:
            self.play(FadeOut(sun), FadeIn(moon), night.animate.set_value(1.0), run_time=1.0)
            cap("Night: stomata open", color="#9FB4FF", sub="CO₂ → malic acid, stored in the vacuole.")
            self.play(acid.animate.set_value(0.95), run_time=max(1.5, v.left - 0.4))
        with self.say("By day, stomata close and the stored carbon dioxide enters the Calvin cycle.") as v:
            self.play(FadeOut(moon), FadeIn(sun), night.animate.set_value(0.0), run_time=1.0)
            cap("Day: stomata shut", color=th.AMBER, sub="Malic acid → CO₂ → Calvin cycle. Separation in TIME.")
            self.play(acid.animate.set_value(0.1), run_time=max(1.5, v.left - 0.4))
        cap.clear()
        self.play(FadeOut(VGroup(sc, sun, al)))
        self.remove(sc)
        rows = [["", "C3", "C4", "CAM"], ["first stable product", "3-PGA (3C)", "oxaloacetate (4C)", "oxaloacetate (4C)"], ["first CO₂ acceptor", "RuBP", "PEP", "PEP"],
                ["separation", "none", "space", "time"], ["Kranz anatomy", "absent", "present", "absent"], ["photorespiration", "high", "greatly suppressed", "greatly suppressed"],
                ["ATP per CO₂", "3", "5", "5–6"], ["stomata open", "day", "day", "night"], ["examples", "rice, wheat, potato", "maize, sugarcane, kodo", "pineapple, Aloe"]]
        tb = B.table(rows, [3.1, 3.0, 3.2, 3.0], row_h=0.56, size=22, colors=[th.MUTED, th.SKY, th.AMBER, FOOD]).move_to([0, 0.15, 0])
        hd = self.head("C3, C4 and CAM")
        with self.say("C3 plants make 3-PGA first. C4 and CAM make oxaloacetate first, separating the steps in space or time.") as v:
            self.play(FadeIn(hd))
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, tb)))

    def p2_factors(self):
        ax = Axes(x_range=[0, 1800, 600], y_range=[-8, 34, 10], x_length=7.0, y_length=4.4, tips=False,
                  axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-2.6, -0.1, 0])
        xl = T("light intensity", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.2)
        yl = T("net CO₂ uptake", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        lo_f = lambda I: (18.0 * 0.055 * I) / (18.0 + 0.055 * I) - 2.0
        hi_f = lambda I: (34.0 * 0.058 * I) / (34.0 + 0.058 * I) - 2.0
        lo = ax.plot(lo_f, x_range=[0, 1800], color=th.SKY, stroke_width=4)
        hi = ax.plot(hi_f, x_range=[0, 1800], color=th.AMBER, stroke_width=4)
        lcp_x = 2.0 * 18.0 / (0.055 * (18.0 - 2.0))
        lcp = Dot(ax.c2p(lcp_x, 0), radius=0.08, color=WHITE)
        ll = T("normal CO₂", size=20, color=th.SKY).move_to(ax.c2p(1500, lo_f(1500)) + DOWN * 0.35)
        hl = T("high CO₂", size=20, color=th.AMBER).move_to(ax.c2p(1500, hi_f(1500)) + UP * 0.3)
        zl = DashedLine(ax.c2p(0, 0), ax.c2p(1800, 0), color=th.FAINT, stroke_width=2)
        cap = B.Captions(self, at=(4.1, -0.1, 0), width=4.7, size=25)
        with self.say("Blackman's law says the slowest factor limits the rate."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(zl))
            cap("Law of limiting factors", color=th.AMBER, sub="Blackman, 1905: the factor in shortest supply sets the rate.")
        with self.say("In dim light, light limits photosynthesis. Where net gain is zero is the light compensation point."):
            self.play(Create(lo), run_time=2.5)
            self.play(FadeIn(lcp, scale=2), FadeIn(ll))
            cap("Light compensation point", color=th.SKY, sub="Photosynthesis = respiration: net gas exchange is zero.")
        with self.say("In bright light, carbon dioxide limits it. More carbon dioxide raises the plateau."):
            self.play(Create(hi), FadeIn(hl), run_time=2.0)
            cap("CO₂ now limits", color=th.AMBER, sub="Air today: about 427 ppm (0.043 %), not the old 0.03 %.")
        cap.clear()
        self.play(FadeOut(VGroup(ax, xl, yl, lo, hi, lcp, ll, hl, zl)))
        head, prob = B.example_head(self, "A rice plant at 20 °C in bright sun, CO₂ at 420 ppm. Doubling the light: no change. Raising CO₂ to 800 ppm: rate doubles. What is limiting? What if the plant is then warmed to 30 °C at 800 ppm?", size=25)
        steps = ["Doubling light changes nothing → light is NOT limiting (already saturated).",
                 "Raising CO₂ doubles the rate → CO₂ WAS the limiting factor.",
                 "At 800 ppm CO₂ is plentiful → the next factor takes over.",
                 "20 °C is below rice's optimum → temperature now limits: warming to 30 °C raises the rate further."]
        rows = VGroup(*[VGroup(T(str(i + 1), size=26, color=self.color, weight="BOLD"), para(s_, width=11.0, size=25, color=th.INK)).arrange(RIGHT, buff=0.3, aligned_edge=UP) for i, s_ in enumerate(steps)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["Example: rice at twenty degrees in bright light. Doubling light does nothing; doubling carbon dioxide doubles the rate. What limits it, and what if we warm it?",
                "Doubling the light changes nothing, so light is not limiting: the plant is already light-saturated.",
                "Raising carbon dioxide doubles the rate, so carbon dioxide was the limiting factor.",
                "At eight hundred parts per million carbon dioxide is plentiful, so the next factor in line takes over.",
                "Twenty degrees is below the optimum for rice's enzymes, so temperature now limits, and warming to thirty raises the rate further."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        for r_, sy in zip(rows, says[1:]):
            with self.say(sy):
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        nb = B.neby_in(self, "success", height=1.2)
        self.wait(0.5)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, prob, rows)))

    # ================================================================== PART 3: RESPIRATION
    def p3(self):
        self.section(2)
        self.p3_intro()
        self.tally = P.Tally([("ATP", ATPC), ("NADH", NADH), ("FADH₂", FADC), ("CO₂", CO2C)], title="running tally, per glucose", w=3.5, size=26).move_to([4.75, 0.2, 0])
        self.p3_glycolysis()
        self.p3_link()
        self.p3_krebs()
        self.p3_ets()
        self.p3_ferment()
        self.p3_rq()

    def p3_intro(self):
        eq = M(r"\mathrm{C_6H_{12}O_6} + 6\,\mathrm{O_2} \rightarrow 6\,\mathrm{CO_2} + 6\,\mathrm{H_2O} + \text{energy}", size=44).move_to([0, 2.0, 0])
        dg = T("about 2870 kJ per mole of glucose", size=24, color=th.MUTED).next_to(eq, DOWN, buff=0.25)
        flame = VGroup(Polygon([-4.4, -2.4, 0], [-3.4, -2.4, 0], [-3.9, -0.4, 0], stroke_width=0, fill_color=th.CORAL, fill_opacity=0.9),
                       Polygon([-4.15, -2.4, 0], [-3.65, -2.4, 0], [-3.9, -1.2, 0], stroke_width=0, fill_color=th.AMBER, fill_opacity=1))
        fl = T("burning: all at once, as heat", size=22, color=th.CORAL).move_to([-3.9, -2.8, 0])
        stairs = VGroup()
        for k in range(6):
            stairs.add(Line([0.4 + k * 0.85, 0.4 - k * 0.5, 0], [1.25 + k * 0.85, 0.4 - k * 0.5, 0], color=th.MUTED, stroke_width=4))
            if k < 5:
                stairs.add(Line([1.25 + k * 0.85, 0.4 - k * 0.5, 0], [1.25 + k * 0.85, 0.4 - (k + 1) * 0.5, 0], color=th.MUTED, stroke_width=4))
        ball = Dot([0.8, 0.6, 0], radius=0.16, color=th.AMBER)
        sl = T("cell: small steps, energy trapped in ATP", size=22, color=th.MINT).move_to([3.0, -2.8, 0])
        atps = VGroup()
        with self.say("Respiration is the stepwise oxidation of food to release usable energy. Burn glucose in a flame and about two thousand eight hundred and seventy kilojoules per mole comes out at once, as heat.") as v:
            self.play(Write(eq), FadeIn(dg))
            self.play(FadeIn(flame, scale=0.5), FadeIn(fl))
            self.play(flame.animate.scale(1.15, about_edge=DOWN), rate_func=there_and_back, run_time=0.8)
        with self.say("A cell releases it in small steps and traps much of it in ATP, in four stages. We keep a running tally.") as v:
            self.play(Create(stairs), FadeIn(ball), FadeIn(sl))
            for k in range(5):
                self.play(ball.animate.move_to([0.8 + (k + 1) * 0.85, 0.6 - (k + 1) * 0.5, 0]), run_time=0.45, rate_func=rate_functions.ease_in_quad)
                a_ = P.chip("ATP", color=ATPC, size=16).move_to([1.25 + k * 0.85, 0.85 - k * 0.5, 0])
                atps.add(a_)
                self.play(FadeIn(a_, shift=UP * 0.2), run_time=0.25)
        self.play(FadeOut(VGroup(eq, dg, flame, fl, stairs, ball, sl, atps)))

    def beads(self, n, at, r=0.2, color=CARB, gap=0.48):
        return VGroup(*[Circle(radius=r, stroke_color=WHITE, stroke_width=1.5, fill_color=color, fill_opacity=1) for _ in range(n)]).arrange(RIGHT, buff=gap - 2 * r).move_to(at)

    def p3_glycolysis(self):
        head = self.head("1 · Glycolysis")
        where = P.chip("cytoplasm · no O₂ needed", color=th.MUTED, size=20).move_to([-2.2, 2.25, 0])
        glu = self.beads(6, [-2.2, 1.2, 0])
        gl = T("glucose (6C)", size=22, color=CARB).next_to(glu, LEFT, buff=0.3)
        tl = self.tally
        with self.say("Stage one, glycolysis, in the cytoplasm. It needs no oxygen and runs in every living cell."):
            self.play(FadeIn(head), FadeIn(where), FadeIn(tl))
            self.play(LaggedStart(*[GrowFromCenter(b) for b in glu], lag_ratio=0.1), FadeIn(gl))
        inv = VGroup(P.chip("ATP", color=ATPC, size=20).move_to([-5.4, 0.2, 0]), P.chip("ATP", color=ATPC, size=20).move_to([1.0, 0.2, 0]))
        ph = VGroup(Dot(glu[0].get_center() + UP * 0.32, radius=0.1, color=ATPC), Dot(glu[-1].get_center() + UP * 0.32, radius=0.1, color=ATPC))
        with self.say("First two ATP are spent adding phosphates. The step at phosphofructokinase is the rate-limiting one."):
            self.play(inv[0].animate.move_to(glu[0].get_center() + UP * 0.8), inv[1].animate.move_to(glu[-1].get_center() + UP * 0.8), run_time=1.0)
            self.play(FadeOut(inv, shift=UP * 0.3), FadeIn(ph, scale=2))
            self.play(ChangeDecimalToValue(tl.vals["ATP"], -2))
        left = VGroup(*glu[:3], ph[0])
        right = VGroup(*glu[3:], ph[1])
        with self.say("The sugar splits into two three-carbon pieces. Each makes one NADH and two ATP directly, by substrate-level phosphorylation.") as v:
            self.play(left.animate.shift(LEFT * 1.6 + DOWN * 1.2), right.animate.shift(RIGHT * 1.6 + DOWN * 1.2), FadeOut(gl), run_time=1.2)
            gain, tags = VGroup(), []
            for grp in (left, right):
                c = grp[1].get_center()
                n_ = P.chip("NADH", color=NADH, size=18).move_to(c + DOWN * 0.75 + LEFT * 0.75)
                a1 = P.chip("2 ATP", color=ATPC, size=18).move_to(c + DOWN * 0.75 + RIGHT * 0.75)
                gain.add(n_, a1)
                tags += ["NADH", "ATP"]
            self.play(LaggedStart(*[FadeIn(g_, shift=DOWN * 0.2) for g_ in gain], lag_ratio=0.2), run_time=1.2)
            self.play(*[g_.animate.move_to(tl.vals[t_]).set_opacity(0) for g_, t_ in zip(gain, tags)],
                      ChangeDecimalToValue(tl.vals["ATP"], 2), ChangeDecimalToValue(tl.vals["NADH"], 2), run_time=1.2)
            self.remove(gain)
        pyr = VGroup(T("pyruvate (3C)", size=22, color=CARB).next_to(left, DOWN, buff=0.3), T("pyruvate (3C)", size=22, color=CARB).next_to(right, DOWN, buff=0.3))
        with self.say("Result: two pyruvate. Gross four ATP, minus two invested: net two ATP and two NADH."):
            self.play(FadeIn(pyr))
            self.play(Circumscribe(tl.vals["ATP"], color=th.AMBER))
        self.play(FadeOut(VGroup(head, where, left, right, pyr)))

    def p3_link(self):
        head = self.head("2 · Link reaction")
        where = P.chip("mitochondrial matrix", color=th.MUTED, size=20).move_to([-2.2, 2.25, 0])
        pyr = self.beads(3, [-2.2, 0.9, 0])
        pl = T("pyruvate (3C)", size=22, color=CARB).next_to(pyr, UP, buff=0.25)
        x2 = T("× 2 per glucose", size=24, color=th.MUTED).move_to([-2.2, -2.6, 0])
        tl = self.tally
        with self.say("Stage two, the link reaction, in the mitochondrial matrix."):
            self.play(FadeIn(head), FadeIn(where), FadeIn(pyr), FadeIn(pl), FadeIn(x2))
        co2 = P.chip("CO₂", color=CO2C, size=20).move_to(pyr[0].get_center() + UP * 0.9 + LEFT * 0.6)
        nadh = P.chip("NADH", color=NADH, size=20).move_to(pyr.get_center() + DOWN * 0.9 + RIGHT * 1.6)
        coa = P.chip("CoA", color=th.PINK, size=20)
        with self.say("Each pyruvate loses a carbon as carbon dioxide and makes NADH, leaving acetyl coenzyme A. Per glucose: two carbon dioxide, two NADH."):
            self.play(pyr[0].animate.move_to(co2.get_center()).set_opacity(0), FadeIn(co2), run_time=1.0)
            self.play(FadeIn(nadh, shift=DOWN * 0.2))
            coa.next_to(pyr[2], RIGHT, buff=0.15)
            al = T("acetyl-CoA (2C)", size=22, color=CARB).next_to(VGroup(pyr[1], pyr[2]), DOWN, buff=0.35)
            self.play(FadeIn(coa, shift=LEFT * 0.2), Transform(pl, T("acetyl-CoA (2C)", size=22, color=CARB).move_to(pl)))
            self.play(co2.animate.move_to(tl.vals["CO₂"]).set_opacity(0), nadh.animate.move_to(tl.vals["NADH"]).set_opacity(0),
                      ChangeDecimalToValue(tl.vals["CO₂"], 2), ChangeDecimalToValue(tl.vals["NADH"], 4), run_time=1.2)
            self.remove(co2, nadh)
        self.play(FadeOut(VGroup(head, where, pyr, pl, x2, coa)))

    def p3_krebs(self):
        tl = self.tally
        C = np.array([-2.5, -0.35, 0])
        R = 1.85
        names = [("citrate", 6), ("isocitrate", 6), ("α-ketoglutarate", 5), ("succinyl-CoA", 4), ("succinate", 4), ("fumarate", 4), ("malate", 4), ("oxaloacetate", 4)]
        angs = [PI / 2 - TAU * k / 8 for k in range(8)]
        ring = Circle(radius=R, stroke_color=th.FAINT, stroke_width=8).move_to(C)
        nodes = VGroup()
        for (n, c), a in zip(names, angs):
            g = VGroup(T(n, size=18, color=th.INK, weight="SEMIBOLD"), T(f"{c}C", size=17, color=CARB)).arrange(DOWN, buff=0.03)
            b = RoundedRectangle(corner_radius=0.1, width=g.width + 0.22, height=g.height + 0.16, stroke_color=th.PANEL_EDGE, stroke_width=2, fill_color=th.PANEL, fill_opacity=1)
            nodes.add(VGroup(b, g.move_to(b)).move_to(C + polar(R, a)))
        head = T("3 · Krebs cycle (matrix)", size=30, color=th.INK, weight="BOLD").move_to([-2.5, 2.85, 0])
        acet = P.chip("acetyl-CoA (2C)", color=CARB, size=19).move_to(C + polar(R + 0.2, 3 * PI / 4) + [-0.9, 0.55, 0])
        aa = Arrow(acet.get_bottom(), C + polar(R, 5 * PI / 8), buff=0.05, color=CARB, stroke_width=3)
        with self.say("Stage three, the Krebs cycle, in the matrix. Acetyl coenzyme A, two carbons, joins oxaloacetate, four, to make citrate, six."):
            self.play(FadeIn(head), Create(ring), FadeIn(nodes[7]), FadeIn(acet), GrowArrow(aa))
            self.play(FadeIn(nodes[0], scale=0.8))
        emis = {2: ["CO₂", "NADH"], 3: ["CO₂", "NADH"], 4: ["ATP"], 5: ["FADH₂"], 0: ["NADH"]}
        cols = {"CO₂": CO2C, "NADH": NADH, "ATP": ATPC, "FADH₂": FADC}
        counts = {"ATP": 2, "NADH": 4, "FADH₂": 0, "CO₂": 2}
        says = ["Isocitrate loses a carbon dioxide and makes NADH, giving alpha-ketoglutarate, five carbons. A second carbon dioxide and NADH give succinyl coenzyme A, four carbons.",
                "Then one ATP, one FADH two at the succinate step, and a third NADH as malate returns to oxaloacetate."]
        groups = [[1, 2, 3], [4, 5, 6, 7]]
        for grp, sy in zip(groups, says):
            with self.say(sy) as v:
                per = max(0.9, (v.dur - 0.5) / len(grp))
                for k in grp:
                    if k == 7:
                        self.play(Indicate(nodes[k], color=th.AMBER, scale_factor=1.08), run_time=0.45)
                    else:
                        self.play(FadeIn(nodes[k], scale=1.25), run_time=0.45)
                    em = emis.get(k if k != 7 else 0, [])
                    if em:
                        mid = C + polar(R + 0.95, (angs[k - 1] + angs[k]) / 2 if k != 7 else (angs[6] + angs[7]) / 2)
                        chs = VGroup(*[P.chip(e_, color=cols[e_], size=17) for e_ in em]).arrange(DOWN, buff=0.08).move_to(mid)
                        self.play(FadeIn(chs, scale=0.6), run_time=0.3)
                        anims = []
                        for e_, ch in zip(em, chs):
                            counts[e_] += 1
                            anims += [ch.animate.move_to(tl.vals[e_]).set_opacity(0), ChangeDecimalToValue(tl.vals[e_], counts[e_])]
                        self.play(*anims, run_time=0.5)
                        self.remove(chs)
                    self.hold(per - (1.25 if em else 0.45))
        sp = VGroup(T("× 2 turns", size=24, color=th.AMBER, weight="BOLD"), T("per glucose", size=20, color=th.AMBER)).arrange(DOWN, buff=0.08).move_to(C)
        with self.say("Per turn: three NADH, one FADH two, one ATP, two carbon dioxide. It turns twice per glucose."):
            self.play(FadeIn(sp, scale=1.3))
            spin = Dot(C + UP * R, radius=0.13, color=WHITE)
            self.add(spin)
            self.play(Rotate(spin, -TAU, about_point=C), tl.bump("ATP", 4), tl.bump("NADH", 10), tl.bump("FADH₂", 2), tl.bump("CO₂", 6), run_time=2.2)
        with self.say("Tally: six carbon dioxide, so every carbon is gone. Ten NADH, two FADH two, only four ATP, and no oxygen used yet."):
            self.play(Circumscribe(tl, color=th.AMBER), run_time=1.2)
            nb = B.neby_in(self, "surprised", height=1.2, corner=DR)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, ring, nodes, acet, aa, sp, spin)))

    def p3_ets(self):
        tl = self.tally
        self.play(tl.animate.scale(0.8).move_to([5.3, 1.6, 0]))
        mem = Rectangle(width=10.2, height=0.75, stroke_width=0, fill_color="#3B2F52", fill_opacity=1).move_to([-1.7, 0.2, 0])
        edges = VGroup(Line([-6.8, 0.575, 0], [3.4, 0.575, 0], color=B.PERI, stroke_width=2), Line([-6.8, -0.175, 0], [3.4, -0.175, 0], color=B.PERI, stroke_width=2))
        ims = T("intermembrane space", size=20, color=th.MUTED).move_to([-3.3, 2.75, 0])
        mat = T("matrix", size=20, color=th.MUTED).move_to([-6.2, -0.8, 0])
        cx = {}
        for name, x, w, h_ in [("I", -5.0, 1.0, 1.4), ("II", -3.6, 0.8, 0.9), ("III", -1.9, 1.0, 1.4), ("IV", -0.1, 1.0, 1.4)]:
            b = RoundedRectangle(corner_radius=0.18, width=w, height=h_, stroke_color=th.SKY, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1).move_to([x, 0.2 if name != "II" else -0.05, 0])
            cx[name] = VGroup(b, T(name, size=24, color=th.SKY, weight="BOLD").move_to(b))
        q = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=th.AMBER, fill_opacity=1), T("Q", size=18, color=th.BG, weight="BOLD")).move_to([-2.85, 0.2, 0])
        cc = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=th.PINK, fill_opacity=1), T("c", size=18, color=th.BG, weight="BOLD")).move_to([-1.0, 0.85, 0])
        syn = VGroup(Rectangle(width=0.45, height=1.0, stroke_color=th.AMBER, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1).move_to([2.2, 0.2, 0]),
                     Circle(radius=0.5, stroke_color=th.AMBER, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to([2.2, -0.75, 0]))
        sl = T("ATP synthase", size=20, color=th.AMBER).move_to([2.2, -1.5, 0])
        nadh = P.chip("NADH", color=NADH, size=20).move_to([-5.0, -1.2, 0])
        o2 = P.chip("½O₂ + 2H⁺ → H₂O", color=O2C, size=19).move_to([0.0, -1.35, 0])
        cap = B.Captions(self, at=(0, -2.6, 0), width=12.4, size=24)
        with self.say("Stage four, the electron transport system, on the inner mitochondrial membrane. Electrons from NADH pass through complex one, ubiquinone, complex three, cytochrome c and complex four to oxygen, the final acceptor, forming water."):
            self.play(FadeIn(mem), Create(edges), FadeIn(ims), FadeIn(mat), *[FadeIn(v_) for v_ in cx.values()], FadeIn(q), FadeIn(cc), FadeIn(syn), FadeIn(sl), FadeIn(nadh))
            e = Dot(nadh.get_center(), radius=0.1, color=th.AMBER)
            self.add(e)
            path = VMobject().set_points_as_corners([nadh.get_center(), cx["I"].get_center(), q.get_center(), cx["III"].get_center(), cc.get_center(), cx["IV"].get_center(), o2.get_center()])
            self.play(MoveAlongPath(e, path), run_time=3.0, rate_func=rate_functions.linear)
            self.play(FadeIn(o2, scale=0.7))
            self.remove(e)
            cap("NADH → I → Q → III → cyt c → IV → O₂ (the final electron acceptor)", color=th.INK)
        pumps = VGroup()
        for name, n in [("I", 4), ("III", 4), ("IV", 2)]:
            x = cx[name].get_center()[0]
            for k in range(n):
                pumps.add(T("H⁺", size=17, color=HPC).move_to([x - 0.3 + 0.3 * (k % 3), -0.75 - 0.3 * (k // 3), 0]))
        nums = VGroup(*[T(f"{n} H⁺", size=22, color=HPC, weight="BOLD").move_to([cx[name].get_center()[0], 2.35, 0]) for name, n in [("I", 4), ("III", 4), ("IV", 2)]])
        with self.say("Complexes one, three and four pump four, four and two protons: ten per NADH. FADH two enters at complex two, which pumps none, so it gives six."):
            self.play(FadeIn(pumps))
            self.play(*[p_.animate.shift(UP * (2.0 + 0.3 * (i % 2))) for i, p_ in enumerate(pumps)], run_time=1.5)
            self.play(FadeIn(nums))
            cap("10 H⁺ per NADH;  6 H⁺ per FADH₂ (enters at complex II)", color=HPC)
        back = B.Flow([2.2, 1.6, 0], [2.2, -0.6, 0], n=6, color=HPC, r=0.06, speed=0.9, width=0.15)
        frac = VGroup(M(r"\text{NADH}: \tfrac{10}{4} = 2.5\ \text{ATP}", size=30, color=NADH), M(r"\text{FADH}_2: \tfrac{6}{4} = 1.5\ \text{ATP}", size=30, color=FADC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.9, -1.15, 0])
        with self.say("About four protons through ATP synthase make one ATP. So NADH is worth two point five ATP, FADH two one point five. This is Mitchell's chemiosmosis."):
            self.add(back)
            self.play(FadeOut(pumps), FadeIn(frac[0]))
            self.play(FadeIn(frac[1]))
            cap("about 4 H⁺ per ATP: chemiosmosis (Mitchell)", color=th.AMBER)
        cap.clear()
        self.play(FadeOut(VGroup(mem, edges, ims, mat, *cx.values(), q, cc, syn, sl, nadh, o2, nums, back, frac, tl)))
        self.remove(back)
        rows = [["source", "number", "ATP each", "ATP"], ["glycolysis, direct", "", "", "2"], ["Krebs cycle, direct", "", "", "2"], ["NADH", "10", "2.5", "25"], ["FADH₂", "2", "1.5", "3"], ["total", "", "", "32"]]
        tb = B.table(rows, [4.2, 2.0, 2.4, 2.0], row_h=0.62, size=26, colors=[th.INK, th.BODY, th.BODY, th.AMBER]).move_to([0, 0.9, 0])
        hd = self.head("The modern ATP tally")
        with self.say("Add it up: two plus two, plus twenty-five from NADH, plus three from FADH two. Thirty-two.") as v:
            self.play(FadeIn(hd))
            B.reveal_table(self, tb, v.dur * 0.85)
        sh = VGroup(T("2 NADH from glycolysis are in the cytoplasm and must be shuttled in:", size=24, color=th.BODY),
                    T("malate–aspartate shuttle → complex I → 32 ATP", size=24, color=NADH),
                    T("glycerol-phosphate shuttle → ubiquinone → 30 ATP", size=24, color=FADC)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -1.9, 0])
        with self.say("But the two glycolysis NADH must be shuttled into the mitochondrion. The malate aspartate shuttle keeps them at two point five each: thirty-two. The glycerol phosphate shuttle drops them to one point five: thirty. So, thirty to thirty-two ATP."):
            self.play(FadeIn(sh[0]))
            self.play(FadeIn(sh[1]))
            self.play(FadeIn(sh[2]))
        self.play(FadeOut(VGroup(hd, tb, sh)))
        self.tip("Old books say 38 ATP: they assumed whole numbers, 3 per NADH and 2 per FADH₂. Write 30–32 and say why; quote 38 only as the classical figure.",
                 "Exam tip. Older books give thirty-eight, assuming exactly three ATP per NADH and two per FADH two. Chemiosmosis needs no whole numbers. Write thirty to thirty-two, and call thirty-eight the classical figure.", width=8.6)

    def p3_ferment(self):
        head = self.head("Without oxygen: fermentation")
        gly = P.chip("glucose → 2 pyruvate (glycolysis)", color=CARB, size=22).move_to([-3.0, 1.4, 0])
        nad = P.chip("NAD⁺", color=NADH, size=22).move_to([-5.2, -0.4, 0])
        nadh = P.chip("NADH", color=NADH, size=22).move_to([-0.8, -0.4, 0])
        a1 = CurvedArrow(nad.get_top() + UP * 0.05, nadh.get_top() + UP * 0.05, angle=-0.9, color=NADH, stroke_width=3)
        a2 = CurvedArrow(nadh.get_bottom() + DOWN * 0.05, nad.get_bottom() + DOWN * 0.05, angle=-0.9, color=th.AMBER, stroke_width=3)
        fl = T("fermentation", size=22, color=th.AMBER).move_to([-3.0, -1.75, 0])
        yeast = VGroup(T("yeast, waterlogged roots", size=22, color=th.INK), M(r"\text{pyruvate} \rightarrow \text{ethanol} + \mathrm{CO_2}", size=30, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 0.9, 0])
        lact = VGroup(T("muscle, Lactobacillus (dahi)", size=22, color=th.INK), M(r"\text{pyruvate} \rightarrow \text{lactic acid}", size=30, color=th.AMBER), T("no CO₂ released", size=20, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -1.0, 0])
        with self.say("Without oxygen, the chain stops and NAD plus runs out. Fermentation turns NADH back into NAD plus so glycolysis can continue."):
            self.play(FadeIn(head), FadeIn(gly), FadeIn(nad), FadeIn(nadh))
            self.play(Create(a1))
            self.play(Create(a2), FadeIn(fl))
        with self.say("Yeast and waterlogged roots make ethanol and carbon dioxide. Muscle and Lactobacillus in dahi make lactic acid, with no carbon dioxide."):
            self.play(FadeIn(yeast, shift=LEFT * 0.2))
            self.play(FadeIn(lact, shift=LEFT * 0.2))
        w = T("Fermentation itself makes no ATP: only the net 2 ATP of glycolysis.", size=26, color=th.CORAL, weight="BOLD").move_to([0, -2.65, 0])
        with self.say("Fermentation itself makes no ATP; the only gain is glycolysis's net two."):
            self.play(Write(w))
        self.play(FadeOut(VGroup(head, gly, nad, nadh, a1, a2, fl, yeast, lact, w)))

    def p3_rq(self):
        head = self.head("Respiratory quotient")
        f = M(r"\text{RQ} = \frac{\text{volume of CO}_2\ \text{evolved}}{\text{volume of O}_2\ \text{consumed}}", size=44).move_to([0, 1.5, 0])
        g = M(r"\mathrm{C_6H_{12}O_6} + 6\,\mathrm{O_2} \rightarrow 6\,\mathrm{CO_2} + 6\,\mathrm{H_2O} \qquad \text{RQ} = \tfrac{6}{6} = 1.0", size=36).move_to([0, -0.4, 0])
        with self.say("The respiratory quotient, R Q, is carbon dioxide given out divided by oxygen taken in. It reveals the fuel being burnt."):
            self.play(FadeIn(head), Write(f))
        with self.say("For glucose, six over six: R Q is one."):
            self.play(Write(g))
        self.play(FadeOut(VGroup(f, g, head)))
        head2, prob = B.example_head(self, "Show that the RQ of tripalmitin, C₅₁H₉₈O₆, is about 0.7.", size=27)
        lines = self.steps([r"2\,\mathrm{C_{51}H_{98}O_6} + 145\,\mathrm{O_2} \rightarrow 102\,\mathrm{CO_2} + 98\,\mathrm{H_2O}",
                            r"\text{C: } 2\times 51 = 102 \qquad \text{H: } 2\times 98 = 196 = 98\times 2",
                            r"\text{O: } 12 + 290 = 302 = 204 + 98",
                            r"\text{RQ} = \frac{102}{145} = 0.70"], size=36, buff=0.38)
        lines.next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        lines[-1].set_color(th.AMBER)
        says = ["Two tripalmitin molecules use one hundred and forty-five oxygen, giving one hundred and two carbon dioxide and ninety-eight water.",
                "Check: carbon one hundred and two each side; hydrogen one hundred and ninety-six each side.",
                "Oxygen: twelve plus two hundred and ninety, three hundred and two, equals two hundred and four plus ninety-eight. Balanced.",
                "R Q is one hundred and two over one hundred and forty-five: zero point seven zero."]
        with self.say("Worked example: show the R Q of the fat tripalmitin is about zero point seven."):
            self.play(FadeIn(head2), FadeIn(prob))
        for ln, sy in zip(lines, says):
            with self.say(sy):
                self.play(Write(ln), run_time=1.3)
        self.play(FadeOut(VGroup(head2, prob, lines)))
        nl = NumberLine(x_range=[0, 4.5, 0.5], length=11.5, color=th.MUTED, include_numbers=True, font_size=24, decimal_number_config={"num_decimal_places": 1}).move_to([0, -0.6, 0])
        hd = self.head("RQ tells you the fuel")
        marks = VGroup()
        for v_, n_, c_, up_, dx in [(0.7, "fat 0.7", th.AMBER, 1, -0.3), (0.8, "protein ≈ 0.8", th.PINK, -1, -0.6), (1.0, "carbohydrate 1.0", th.MINT, 1, 0.5), (1.33, "malic acid 1.33", th.SKY, -1, 0.7), (4.0, "oxalic acid 4.0", th.CORAL, 1, 0)]:
            tri = Triangle(fill_color=c_, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI if up_ > 0 else 0).move_to(nl.n2p(v_) + UP * 0.28 * up_)
            lb = T(n_, size=22, color=c_).move_to(nl.n2p(v_) + UP * ((0.7 if v_ != 1.0 else 1.1) if up_ > 0 else -1.15) + RIGHT * dx)
            marks.add(VGroup(tri, lb))
        mal = M(r"2\,\mathrm{C_4H_6O_5} + 6\,\mathrm{O_2} \rightarrow 8\,\mathrm{CO_2} + 6\,\mathrm{H_2O} \qquad \text{RQ} = \tfrac{8}{6} = 1.33", size=32, color=th.SKY).move_to([0, 1.6, 0])
        with self.say("Fat is oxygen-poor, so it needs much oxygen: R Q below one. Malic acid is oxygen-rich: two molecules need six oxygen and give eight carbon dioxide. R Q one point three three.") as v:
            self.play(FadeIn(hd), Create(nl))
            self.play(FadeIn(marks[0]), FadeIn(marks[2]))
            self.play(Write(mal))
            self.play(FadeIn(marks[3]))
        with self.say("So: fat zero point seven, protein about zero point eight, carbohydrate one, malic acid one point three three, oxalic acid four."):
            self.play(FadeIn(marks[1]), FadeIn(marks[4]))
        self.play(FadeOut(VGroup(hd, nl, marks, mal)))
        self.quiz("The respiratory quotient of a germinating castor seed, rich in fat, is closest to",
                  ["0.70", "1.00", "1.33", "4.00"], 0,
                  "Pause and think. A germinating castor seed burns stored oil. What R Q?",
                  "Zero point seven. Fats are oxygen-poor, so they use more oxygen than the carbon dioxide they release. One is the trap: that is for sugar, not oil.")

    # ================================================================== PART 4: HORMONES
    def p4(self):
        self.section(3)
        self.p4_intro()
        self.p4_auxin()
        self.p4_gibberellin()
        self.p4_cytokinin()
        self.p4_aba()
        self.p4_ethylene()

    def p4_intro(self):
        names = [("Auxin", th.AMBER), ("Gibberellin", th.MINT), ("Cytokinin", th.SKY), ("Abscisic acid", th.CORAL), ("Ethylene", th.PINK)]
        chips = VGroup(*[P.chip(n, color=c, size=28) for n, c in names]).arrange(RIGHT, buff=0.35).move_to([0, -0.6, 0])
        d = para("A plant hormone: an organic substance made in small amounts in one part of a plant, carried to another part, where it regulates a process.", width=11.5, size=28, color=th.INK).move_to([0, 1.5, 0])
        with self.say("A plant hormone is made in small amounts in one part of the plant and acts in another. There are five classical ones."):
            self.play(FadeIn(d, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in chips], lag_ratio=0.2))
        self.play(FadeOut(VGroup(d, chips)))

    def p4_auxin(self):
        head = self.head("Auxin: discovered by bending shoots", th.AMBER)
        X = [-4.9, -1.65, 1.65, 4.9]
        base_y, L = -2.0, 2.7
        labs = ["Darwin: tip covered", "Darwin: base covered", "Boysen-Jensen: gelatin", "Went: agar block, dark"]
        def panel(i, th_):
            b = np.array([X[i], base_y, 0])
            if i == 3:
                g = P.organ(b, L * 0.85, th_, w=0.17, tip=False)
                top, ph = g.top, g.phi
                d = np.array([np.sin(ph), np.cos(ph), 0])
                nv = np.array([-np.cos(ph), np.sin(ph), 0])
                blk = Polygon(top + nv * 0.17, top + nv * 0.0, top + nv * 0.0 + d * 0.22, top + nv * 0.17 + d * 0.22, stroke_width=0, fill_color=th.AMBER, fill_opacity=1)
                return VGroup(g, blk)
            g = P.organ(b, L, th_, w=0.17)
            top, ph = g.top, g.phi
            d = np.array([np.sin(ph), np.cos(ph), 0])
            nv = np.array([-np.cos(ph), np.sin(ph), 0])
            extra = VGroup()
            if i == 0:
                extra = Polygon(top - d * 0.45 + nv * 0.24, top - d * 0.45 - nv * 0.24, top + d * 0.25, stroke_width=0, fill_color="#C9CEE8", fill_opacity=1)
            if i == 1:
                p0 = b + UP * 0.05
                extra = Rectangle(width=0.5, height=1.3, stroke_width=0, fill_color="#C9CEE8", fill_opacity=1).move_to(p0 + UP * 0.65)
            if i == 2:
                extra = Line(top - d * 0.5 + nv * 0.2, top - d * 0.5 - nv * 0.2, color=th.AMBER, stroke_width=6)
            return VGroup(g, extra)

        pans = [panel(i, 0.0) for i in range(4)]
        ends = [panel(0, 0.0), panel(1, 0.6), panel(2, 0.6), panel(3, 0.55)]
        light = VGroup(*[VGroup(*[Arrow([X[i] + 1.4, base_y + 1.0 + 0.45 * k, 0], [X[i] + 0.55, base_y + 1.0 + 0.45 * k, 0], buff=0, color=th.AMBER, stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in range(3)]) for i in range(3)])
        dark = T("dark", size=20, color=th.MUTED).move_to([X[3] + 1.0, base_y + 2.4, 0])
        tl = VGroup(*[para(labs[i], width=2.9, size=20, color=th.BODY, align="center").move_to([X[i], base_y - 0.55, 0]) for i in range(4)])
        ground = VGroup(*[Line([x - 0.7, base_y, 0], [x + 0.7, base_y, 0], color=th.FAINT, stroke_width=3) for x in X])
        with self.say("Auxin's discovery is a favourite question. Darwin, in eighteen eighty: cover a coleoptile's tip and it no longer bends to light; cover the part below and it still bends."):
            self.play(FadeIn(head), FadeIn(ground), *[FadeIn(pans[i]) for i in range(2)], FadeIn(light[:2]), FadeIn(tl[:2]))
            self.play(Transform(pans[1], ends[1]), run_time=1.5)
        with self.say("So the tip senses light but bending happens lower down. Boysen-Jensen put a cut tip back on gelatin and it still bent: the signal is a diffusible chemical."):
            self.play(FadeIn(pans[2]), FadeIn(light[2]), FadeIn(tl[2]))
            self.play(Transform(pans[2], ends[2]), run_time=1.5)
        with self.say("Paál got bending in darkness from an off-centre tip. Went collected the chemical in agar blocks; a block on one side made a cut coleoptile bend away. He named it auxin."):
            self.play(FadeIn(pans[3]), FadeIn(dark), FadeIn(tl[3]))
            self.play(Transform(pans[3], ends[3]), run_time=1.5)
        self.play(FadeOut(VGroup(head, ground, *pans, light, dark, tl)))
        # mechanism
        bend = ValueTracker(0.0)
        shift_ = ValueTracker(0.0)
        b0 = np.array([-3.4, -2.6, 0])
        col = always_redraw(lambda: P.organ(b0, 4.3, bend.get_value(), w=0.36, aux=AUX, aux_shift=shift_.get_value(), aux_n=12, aux_side=1))
        gnd = Line([-5.4, -2.6, 0], [-1.4, -2.6, 0], color=th.FAINT, stroke_width=3)
        sun = Circle(radius=0.45, stroke_width=0, fill_color=th.AMBER, fill_opacity=1).move_to([0.4, 1.9, 0])
        rays = VGroup(*[Arrow([0.0, 1.6 - 0.6 * k, 0], [-1.3, 1.6 - 0.6 * k, 0], buff=0, color=th.AMBER, stroke_width=3, stroke_opacity=0.7, max_tip_length_to_length_ratio=0.08) for k in range(4)])
        cap = B.Captions(self, at=(3.9, -0.6, 0), width=4.8, size=26)
        with self.say("Auxin, made at the shoot tip from tryptophan, moves down. Light from one side drives it to the shaded side.") as v:
            self.play(Create(gnd), FadeIn(col), FadeIn(sun), FadeIn(rays))
            cap("Auxin moves to the shaded side", color=AUX, sub="IAA, from tryptophan, made at the shoot tip.")
            self.play(shift_.animate.set_value(1.0), run_time=max(1.5, v.left - 0.4))
        with self.say("The shaded side elongates more, so the shoot bends towards light: positive phototropism, the Cholodny Went hypothesis.") as v:
            self.play(bend.animate.set_value(0.75), run_time=max(2, v.left - 0.6))
            cap("Shaded side elongates more → bends to light", color=th.MINT, sub="Positive phototropism (Cholodny–Went).")
        nb = B.neby_in(self, "wink", height=1.2)
        self.wait(0.4)
        B.neby_out(self, nb)
        cap.clear()
        self.play(FadeOut(VGroup(col, gnd, sun, rays)))
        self.remove(col)
        # apical dominance
        stem = Line([-3.4, -2.6, 0], [-3.4, 1.6, 0], color=SHOOT, stroke_width=8)
        apex = Circle(radius=0.22, stroke_width=0, fill_color="#A6F5B0", fill_opacity=1).move_to([-3.4, 1.75, 0])
        nodes_y = [-1.5, -0.5, 0.5]
        leaves = VGroup(*[Ellipse(width=1.1, height=0.35, stroke_width=0, fill_color="#2E7D32", fill_opacity=1).rotate(s * 0.4).move_to([-3.4 + s * 0.65, y + 0.1, 0]) for y in nodes_y for s in (-1, 1)])
        buds = VGroup(*[Dot([-3.4 + s * 0.2, y + 0.35, 0], radius=0.09, color="#A6F5B0") for y in nodes_y for s in (-1, 1)])
        down = B.Flow([-3.4, 1.5, 0], [-3.4, -2.4, 0], n=10, color=AUX, r=0.05, speed=0.8, width=0.08)
        cap2 = B.Captions(self, at=(2.8, -0.4, 0), width=6.4, size=26)
        with self.say("Auxin from the apex also suppresses the buds below: apical dominance."):
            self.play(Create(stem), FadeIn(apex), FadeIn(leaves), FadeIn(buds))
            self.add(down)
            cap2("Apical dominance", color=AUX, sub="Auxin from the apex suppresses the axillary buds below.")
        branches = VGroup(*[Line(b.get_center(), b.get_center() + np.array([(-1 if i % 2 == 0 else 1) * 1.3, 0.9, 0]), color=SHOOT, stroke_width=5) for i, b in enumerate(buds)])
        with self.say("Pluck a tea bush tip and side buds grow, making the bush dense."):
            self.play(FadeOut(apex, shift=UP * 0.5), FadeOut(down))
            self.remove(down)
            self.play(LaggedStart(*[Create(b) for b in branches], lag_ratio=0.15), run_time=2.0)
            cap2("Remove the apex → laterals grow", color=th.MINT, sub="Basis of tea plucking, pruning and hedging.")
        with self.say("Synthetic auxins I B A and N A A root cuttings, and two four D kills broad-leaved weeds in rice and wheat. Careful: a dose that speeds a stem stops a root."):
            cap2("More auxin uses", color=AUX, sub="IBA, NAA: rooting. Parthenocarpy. 2,4-D kills dicot weeds. Roots need far lower doses than shoots.")
        cap2.clear()
        self.play(FadeOut(VGroup(stem, leaves, buds, branches)))

    def p4_gibberellin(self):
        head = self.head("Gibberellin", th.MINT)
        gnd = Line([-6.3, -2.4, 0], [-0.4, -2.4, 0], color=th.FAINT, stroke_width=3)
        norm = VGroup(*[Line([x, -2.4, 0], [x + 0.05, -1.2, 0], color="#5FB04A", stroke_width=5) for x in (-5.8, -5.4, -5.0)])
        sick = VGroup(*[Line([x, -2.4, 0], [x + 0.08, -2.39, 0], color="#C9E3A0", stroke_width=4) for x in (-2.8, -2.4, -2.0)])
        nl = T("healthy", size=20, color="#5FB04A").move_to([-5.4, -2.75, 0])
        sl = T("bakanae: tall, pale, weak", size=20, color="#C9E3A0").move_to([-2.4, -2.75, 0])
        cap = B.Captions(self, at=(3.3, -0.3, 0), width=6.0, size=26)
        with self.say("Gibberellin came from bakanae, the foolish seedling disease of rice, where infected seedlings grow tall and pale. Kurosawa showed a cell-free fungal extract did the same."):
            self.play(FadeIn(head), Create(gnd), Create(norm), FadeIn(nl), FadeIn(sl))
            self.add(sick)
            self.play(*[s_.animate.put_start_and_end_on(s_.get_start(), s_.get_start() + np.array([0.15, 3.6, 0])) for s_ in sick], run_time=2.0)
            cap("Bakanae disease of rice", color=th.MINT, sub="Gibberella fujikuroi; cell-free extract reproduces it (Kurosawa, 1926).")
        self.play(FadeOut(VGroup(norm, sick, nl, sl)))
        g = ValueTracker(0.0)
        B0 = np.array([-3.3, -2.4, 0])

        def cab():
            h = g.get_value() * 3.6
            ro = VGroup(*[Ellipse(width=1.5, height=0.45, stroke_color="#A7D36B", stroke_width=2, fill_color="#4E7F2A", fill_opacity=1).rotate(a).move_to(B0 + polar(0.65, a) + UP * 0.2)
                          for a in (0.15, PI - 0.15, 0.6, PI - 0.6)])
            st = Line(B0 + UP * 0.2, B0 + UP * (0.2 + h), color="#7BC043", stroke_width=6)
            g_ = VGroup(ro, st)
            if h > 0.6:
                for k in range(int(h / 0.7)):
                    y = 0.6 + k * 0.7
                    g_.add(Ellipse(width=0.55, height=0.2, stroke_width=0, fill_color="#5E8C2E", fill_opacity=1).rotate(0.4 * (-1) ** k).move_to(B0 + [0.3 * (-1) ** k, y, 0]))
            if h > 2.5:
                fl = VGroup(*[Dot(B0 + UP * (0.2 + h) + polar(0.18, a), radius=0.07, color="#FFE066") for a in np.linspace(0, TAU, 7)])
                g_.add(fl)
            return g_

        cb = always_redraw(cab)
        with self.say("Its signature effect is stem elongation. A rosette cabbage given gibberellin shoots up a stem and flowers: bolting.") as v:
            self.add(cb)
            cap("Bolting", color=th.MINT, sub="Rosette plants (cabbage, beet): sudden stem elongation before flowering.")
            self.play(g.animate.set_value(1.0), run_time=max(2, v.left - 0.3))
        with self.say("It also makes dwarf peas tall, breaks dormancy, triggers alpha-amylase in germinating barley, and enlarges Thompson Seedless grapes."):
            cap("More gibberellin effects", color=th.MINT, sub="Dwarf pea → tall. Breaks dormancy. α-amylase in barley aleurone. Bigger grapes.")
        cap.clear()
        self.play(FadeOut(VGroup(head, gnd, cb)))
        self.remove(cb)

    def p4_cytokinin(self):
        head = self.head("Cytokinin", th.SKY)
        c1 = Circle(radius=0.6, stroke_color=th.SKY, stroke_width=3, fill_color=PARF, fill_opacity=1).move_to([-3.4, 0.2, 0])
        two = VGroup(*[Circle(radius=0.45, stroke_color=th.SKY, stroke_width=3, fill_color=PARF, fill_opacity=1).move_to([-3.4 + d, 0.2, 0]) for d in (-0.46, 0.46)])
        four = VGroup(*[Circle(radius=0.35, stroke_color=th.SKY, stroke_width=3, fill_color=PARF, fill_opacity=1).move_to([-3.4 + dx, 0.2 + dy, 0]) for dx in (-0.36, 0.36) for dy in (-0.36, 0.36)])
        cap = B.Captions(self, at=(3.0, -0.2, 0), width=6.4, size=26)
        with self.say("Cytokinins promote cell division, with auxin present. Kinetin came from herring sperm DNA, zeatin from maize. They are made in root tips."):
            self.play(FadeIn(head), FadeIn(c1))
            self.play(ReplacementTransform(c1, two))
            self.play(ReplacementTransform(two, four))
            cap("Cytokinin: cell division", color=th.SKY, sub="Kinetin (from herring-sperm DNA), zeatin (maize). Made in root tips, moves up in xylem.")
        cap.clear()
        self.play(FadeOut(four))
        X = [-4.2, 0.0, 4.2]
        dishes = VGroup(*[Ellipse(width=3.2, height=1.1, stroke_color=th.MUTED, stroke_width=3, fill_color=th.PANEL, fill_opacity=0.8).move_to([x, -1.2, 0]) for x in X])
        calli = VGroup(*[B.blob([x, -1.0, 0], 0.42, n=9, jit=0.2, seed=k, stroke="#E6DCA0", fill="#8A7A3A") for k, x in enumerate(X)])
        ratios = VGroup(*[T(t, size=22, color=c).move_to([x, 2.0, 0]) for t, c, x in [("auxin > cytokinin", th.AMBER, X[0]), ("auxin ≈ cytokinin", th.INK, X[1]), ("cytokinin > auxin", th.SKY, X[2])]])
        roots = VGroup(*[Line([X[0] + d, -1.2, 0], [X[0] + d * 2.2, -2.5, 0], color=ROOT, stroke_width=4) for d in (-0.3, -0.1, 0.1, 0.3)])
        shoots = VGroup(*[VGroup(Line([X[2] + d, -0.7, 0], [X[2] + d * 1.5, 0.9, 0], color=SHOOT, stroke_width=5),
                                 Ellipse(width=0.5, height=0.2, stroke_width=0, fill_color="#2E7D32", fill_opacity=1).move_to([X[2] + d * 1.5 + 0.2, 0.75, 0])) for d in (-0.25, 0.0, 0.25)])
        outs = VGroup(*[T(t, size=24, color=c, weight="BOLD").move_to([x, 1.45, 0]) for t, c, x in [("roots", ROOT, X[0]), ("callus", "#E6DCA0", X[1]), ("shoots", SHOOT, X[2])]])
        with self.say("In tissue culture the ratio decides: more auxin gives roots, equal gives callus, more cytokinin gives shoots. This is the fact most often reversed."):
            self.play(FadeIn(dishes), FadeIn(calli), FadeIn(ratios))
            self.play(LaggedStart(*[Create(r_) for r_ in roots], lag_ratio=0.15), FadeIn(outs[0]), run_time=1.5)
            self.play(calli[1].animate.scale(1.6), FadeIn(outs[1]), run_time=1.2)
            self.play(LaggedStart(*[Create(s_) for s_ in shoots], lag_ratio=0.15), FadeIn(outs[2]), run_time=1.5)
        self.play(FadeOut(VGroup(dishes, calli, ratios, roots, shoots, outs)))
        leaf = Ellipse(width=3.8, height=2.0, stroke_color=CHL, stroke_width=3, fill_color="#2E7D32", fill_opacity=1).move_to([-3.4, 0.0, 0])
        spot = Circle(radius=0.45, stroke_width=0, fill_color="#2E7D32", fill_opacity=1).move_to([-3.0, 0.1, 0])
        sp_l = T("cytokinin drop", size=20, color=th.SKY).move_to([-3.0, -1.4, 0])
        with self.say("Cytokinin delays ageing: a treated spot on a detached leaf stays green while the rest yellows. That is the Richmond Lang effect."):
            self.play(FadeIn(leaf), FadeIn(spot), FadeIn(sp_l))
            self.play(leaf.animate.set_fill("#C9B23A"), run_time=2.5)
            cap("Richmond–Lang effect", color=th.SKY, sub="Cytokinin delays senescence; also releases lateral buds.")
        cap.clear()
        self.play(FadeOut(VGroup(head, leaf, spot, sp_l)))
        self.quiz("In tissue culture, a high cytokinin to auxin ratio makes the callus form",
                  ["roots", "shoots", "more callus", "somatic embryos only"], 1,
                  "Pause and think. Plenty of cytokinin, little auxin. What grows from the callus?",
                  "Shoots. High cytokinin gives shoots, high auxin roots, equal amounts callus. Roots is the trap: the exact reversal, and the commonest mistake here.")

    def p4_aba(self):
        head = self.head("Abscisic acid (ABA)", th.CORAL)
        C = np.array([-3.4, -0.3, 0])
        o = ValueTracker(1.0)
        gc = always_redraw(lambda: P.guard_pair(o.get_value(), c=C, H=1.4, w=0.65))
        abas = VGroup(*[P.chip("ABA", color=th.CORAL, size=18).move_to(C + polar(2.2, a)) for a in np.linspace(0.3, TAU + 0.3, 6, endpoint=False)])
        cap = B.Captions(self, at=(3.0, -0.3, 0), width=6.4, size=26)
        with self.say("Abscisic acid, A B A, is the stress hormone. In drought it closes stomata within minutes."):
            self.play(FadeIn(head), FadeIn(gc))
            self.play(LaggedStart(*[FadeIn(a_, scale=0.5) for a_ in abas], lag_ratio=0.1))
            self.play(o.animate.set_value(0.0), abas.animate.scale(0.9).set_opacity(0.6), run_time=2.0)
            cap("ABA closes stomata", color=th.CORAL, sub="Its single most important job, under water stress.")
        with self.say("It also induces seed and bud dormancy, opposing gibberellin."):
            cap("Dormancy and inhibition", color=th.CORAL, sub="Induces seed and bud dormancy; inhibits germination. Antagonist of gibberellin.")
        cap.clear()
        self.play(FadeOut(VGroup(gc, abas)))
        self.remove(gc)
        w = self.callout("careful", "Despite its name, ABA is not the main hormone of leaf fall. It was named after the cotton bolls it was extracted from. Abscission is mainly ethylene's job; auxin delays it.", width=10.5)
        with self.say("Trap: despite its name, A B A is not the main leaf-fall hormone. That is ethylene; auxin delays abscission."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, w)))

    def p4_ethylene(self):
        head = self.head("Ethylene", th.PINK)
        pos = [[-4.6, 0.6, 0], [-3.2, 1.0, 0], [-1.8, 0.6, 0], [-4.0, -0.7, 0], [-2.4, -0.7, 0]]
        GR, YE = "#6BAA3A", "#F2C94C"
        bns = VGroup(*[P.banana(p, ang=0.3 * ((-1) ** i), color=YE if i == 1 else GR) for i, p in enumerate(pos)])
        basket = VGroup(Line([-5.6, -1.5, 0], [-0.8, -1.5, 0], color="#B9875A", stroke_width=6), Line([-5.6, -1.5, 0], [-5.9, 1.8, 0], color="#B9875A", stroke_width=6), Line([-0.8, -1.5, 0], [-0.5, 1.8, 0], color="#B9875A", stroke_width=6))
        cap = B.Captions(self, at=(3.2, -0.2, 0), width=6.2, size=26)
        with self.say("Ethylene is the only gaseous hormone, made from methionine. Its signature job: ripening fruit."):
            self.play(FadeIn(head), Create(basket), FadeIn(bns))
            cap("Ethylene: a gas", color=th.PINK, sub="From methionine. Signature job: fruit ripening.")
        gas = [B.Flow(pos[1], pos[k], n=4, color="#D8D8E8", r=0.045, speed=0.7, width=0.2, seed=k) for k in (0, 2, 3, 4)]
        with self.say("Climacteric fruits like banana and mango release an autocatalytic burst of ethylene, so one ripe banana ripens its neighbours.") as v:
            self.add(*gas)
            cap("Climacteric fruits", color=YE, sub="Banana, mango, papaya, tomato: ethylene burst, autocatalytic. One ripe fruit ripens the rest.")
            self.play(LaggedStart(*[bns[k].animate.set_stroke(YE) for k in (0, 2, 3, 4)], lag_ratio=0.35), run_time=max(2, v.left - 0.4))
        self.play(*[FadeOut(g_) for g_ in gas], run_time=0.4)
        self.remove(*gas)
        with self.say("Orange, grape and litchi are non-climacteric and won't ripen after picking. Ethylene also causes leaf fall and epinasty, and is sprayed as ethephon."):
            cap("More ethylene effects", color=th.PINK, sub="Abscission, senescence, epinasty, flowering in pineapple. Applied as ethephon.")
        cap.clear()
        self.play(FadeOut(VGroup(bns, basket)))
        w = self.callout("careful", "Calcium carbide does not release ethylene: it gives acetylene, plus toxic impurities (phosphine, arsine). Carbide ripening is prohibited in Nepal.", width=10.5)
        with self.say("Warning: calcium carbide releases acetylene, not ethylene, plus toxic impurities. It is prohibited in Nepal."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, w)))
        rows = [["hormone", "made mainly in", "signature effects"], ["auxin (IAA)", "shoot apex", "elongation; apical dominance"],
                ["gibberellin (GA₃)", "young leaves, embryo", "internode elongation; bolting"], ["cytokinin (zeatin)", "root apex", "cell division; delays ageing"],
                ["abscisic acid", "leaves, seeds", "closes stomata; dormancy"], ["ethylene", "ripening fruit", "ripening; abscission"]]
        tb = B.table(rows, [3.4, 3.4, 5.8], row_h=0.66, size=24, colors=[th.AMBER, th.BODY, th.INK]).move_to([0, -0.2, 0])
        hd = self.head("Five hormones at a glance")
        with self.say("All five: auxin for elongation and apical dominance; gibberellin for bolting; cytokinin for division; A B A for stomatal closure and dormancy; ethylene for ripening and leaf fall.") as v:
            self.play(FadeIn(hd))
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(hd, tb)))

    # ================================================================== PART 5: GROWTH AND MOVEMENT
    def p5(self):
        self.section(4)
        self.p5_growth()
        self.p5_curve()
        self.p5_photoperiod()
        self.p5_tropic()
        self.p5_nastic()

    def p5_growth(self):
        head = self.head("Growth")
        d = para("Growth: a permanent, irreversible increase in size, volume or dry weight, with metabolic activity.", width=11.5, size=28, color=th.INK).move_to([0, 1.7, 0])
        with self.say("Growth is an irreversible increase in size or dry weight. A wilted leaf that recovers has not grown. Plant growth is localised in meristems and indeterminate."):
            self.play(FadeIn(head), FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        Y0 = 1.9
        e = ValueTracker(0.0)

        def root():
            ext = e.get_value()
            zc = [("cap", "#C9A27A", 0.35), ("division", "#9C8CFF", 0.7), ("elongation", th.AMBER, 0.9 + 1.4 * ext), ("maturation", PAR, 1.3)]
            g = VGroup()
            y = -2.6
            tops = []
            for name, c, h in zc:
                if name == "cap":
                    r = Polygon([-4.0 - 0.32, y + h, 0], [-4.0 + 0.32, y + h, 0], [-4.0, y, 0], stroke_width=0, fill_color=c, fill_opacity=1)
                    r.round_corners(0.1)
                else:
                    r = Rectangle(width=0.64, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([-4.0, y + h / 2, 0])
                g.add(r)
                tops.append((name, c, y, y + h))
                y += h
            return g, tops

        rr = always_redraw(lambda: root()[0])
        labs = always_redraw(lambda: VGroup(*[T(n, size=20, color=c).move_to([-2.9 + 0.35 * (n == "elongation"), (a + b) / 2, 0]).align_to([-3.5, 0, 0], LEFT) for n, c, a, b in root()[1]]))
        marks0 = np.linspace(0.0, 3.2, 9)

        def mk():
            ext = e.get_value()
            g = VGroup()
            for m in marks0:
                y = m
                if m > 1.05:
                    y = 1.05 + min(m - 1.05, 0.9) * (1 + 1.4 * ext / 0.9) + max(0, m - 1.95)
                g.add(Line([-4.32, -2.6 + y, 0], [-3.68, -2.6 + y, 0], color=WHITE, stroke_width=2.5))
            return g

        marks = always_redraw(mk)
        cap = B.Captions(self, at=(2.8, -0.3, 0), width=6.4, size=26)
        with self.say("In a root tip, cells divide behind the cap, then elongate, then mature."):
            self.play(FadeIn(rr), FadeIn(labs))
            cap("Three growing zones", sub="Division → elongation → maturation, running back from the tip.")
        with self.say("Ink marks spread most in the elongation zone: that is where the root lengthens.") as v:
            self.play(FadeIn(marks))
            self.play(e.animate.set_value(0.9), run_time=max(2, v.left - 0.5))
            cap("Most lengthening: zone of elongation", color=th.AMBER)
        cap.clear()
        self.play(FadeOut(VGroup(head, rr, labs, marks)))
        self.remove(rr, labs, marks)

    def p5_curve(self):
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 110, 20], x_length=8.6, y_length=4.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-0.6, -0.7, 0])
        xl = T("time", size=22, color=th.MUTED).next_to(ax, DOWN, buff=0.15)
        yl = T("size or dry mass", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        f = lambda t: 100 / (1 + np.exp(-(t - 6.0) * 0.85))
        curve = ax.plot(f, x_range=[0, 12], color=self.color, stroke_width=5)
        spans = [(0, 3.2, "lag"), (3.2, 6.0, "log"), (6.0, 8.8, "deceleration"), (8.8, 12, "stationary")]
        bands = VGroup()
        bl = VGroup()
        for i, (a, b, n) in enumerate(spans):
            r = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 110)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=[th.SKY, th.MINT, th.AMBER, th.PINK][i], fill_opacity=0.12)
            r.move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, 110)[1]) / 2, 0])
            bands.add(r)
            bl.add(T(n, size=22, color=[th.SKY, th.MINT, th.AMBER, th.PINK][i], weight="BOLD").move_to(ax.c2p((a + b) / 2, 104)))
        head = self.head("The grand period of growth: a sigmoid")
        inf = Dot(ax.c2p(6, 50), radius=0.1, color=WHITE)
        il = T("point of inflexion: fastest growth", size=22, color=th.INK).move_to(ax.c2p(9.0, 38))
        with self.say("Plot size against time and you get an S-shaped curve: the grand period of growth.") as v:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=max(2, v.left - 0.4), rate_func=rate_functions.linear)
        with self.say("Four phases: slow lag, exponential log, deceleration as resources run short, and stationary at maturity.") as v:
            per = (v.dur - 0.4) / 4
            for r_, l_ in zip(bands, bl):
                self.play(FadeIn(r_), FadeIn(l_), run_time=0.5)
                self.hold(per - 0.5)
        with self.say("The steepest point, the point of inflexion, is the fastest growth."):
            self.play(FadeIn(inf, scale=2), FadeIn(il))
        g1 = M(r"\text{geometric: } W_t = W_0\,e^{rt}", size=32, color=th.MINT)
        g2 = M(r"\text{arithmetic: } L_t = L_0 + rt", size=32, color=th.AMBER)
        gg = VGroup(g1, g2).arrange(RIGHT, buff=0.8).move_to([-0.4, 2.15, 0])
        with self.say("Early on both daughter cells divide: geometric, exponential growth. Later only one does: arithmetic growth. Then it stops, giving the S."):
            self.play(FadeIn(gg, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, ax, xl, yl, curve, bands, bl, inf, il, gg)))

    def p5_photoperiod(self):
        head = self.head("Photoperiodism")
        x0, W = -6.2, 6.6
        k = W / 24
        def bar(day, flash=False, y=0.0):
            d = Rectangle(width=day * k, height=0.55, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.9).move_to([x0 + day * k / 2, y, 0])
            n = Rectangle(width=(24 - day) * k, height=0.55, stroke_width=0, fill_color="#1E2A5A", fill_opacity=1).move_to([x0 + day * k + (24 - day) * k / 2, y, 0])
            g = VGroup(d, n)
            if flash:
                g.add(Rectangle(width=0.12, height=0.75, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to([x0 + day * k + (24 - day) * k / 2, y, 0]))
            return g
        ys = [0.8, -0.5, -1.8]
        bars = VGroup(bar(10, y=ys[0]), bar(16, y=ys[1]), bar(10, True, y=ys[2]))
        rl = VGroup(*[T(t, size=20, color=th.BODY).next_to([x0, y + 0.45, 0], RIGHT, buff=0) for t, y in zip(["10 h day, 14 h night", "16 h day, 8 h night", "14 h night, broken by a flash"], ys)])
        crit = DashedLine([x0 + 12 * k, 1.45, 0], [x0 + 12 * k, -2.15, 0], color=th.CORAL, stroke_width=2.5, dash_length=0.1)
        cl = VGroup(DoubleArrow([x0 + 12 * k, 1.45, 0], [x0 + 24 * k, 1.45, 0], buff=0, color=th.CORAL, stroke_width=3, tip_length=0.15),
                    T("critical night, 12 h (example)", size=18, color=th.CORAL).move_to([x0 + 18 * k, 1.75, 0]))
        hd = VGroup(VGroup(T("short-day plant", size=22, color=th.SKY, weight="BOLD"), para("chrysanthemum, soybean, Xanthium", width=2.3, size=16, color=th.MUTED, align="center")).arrange(DOWN, buff=0.06).move_to([2.3, 1.95, 0]),
                    VGroup(T("long-day plant", size=22, color=th.MINT, weight="BOLD"), para("wheat, radish, spinach", width=2.3, size=16, color=th.MUTED, align="center")).arrange(DOWN, buff=0.06).move_to([5.4, 1.95, 0]))
        res = [("flowers", "no"), ("no", "flowers"), ("no", "flowers")]
        outs = VGroup()
        for (a, b), y in zip(res, ys):
            outs.add(VGroup(T(a, size=24, color=th.MINT if a == "flowers" else th.CORAL, weight="BOLD").move_to([2.3, y, 0]),
                            T(b, size=24, color=th.MINT if b == "flowers" else th.CORAL, weight="BOLD").move_to([5.4, y, 0])))
        with self.say("Many plants time flowering by day and night length: photoperiodism, discovered by Garner and Allard in nineteen twenty."):
            self.play(FadeIn(head), FadeIn(hd))
        with self.say("Short-day plants, like chrysanthemum and soybean, need nights longer than a critical length; long-day plants, like wheat and radish, need shorter ones. Here, say twelve hours. Tomato is day-neutral."):
            self.play(FadeIn(bars[0]), FadeIn(rl[0]), Create(crit), FadeIn(cl))
            self.play(FadeIn(outs[0]))
            self.play(FadeIn(bars[1]), FadeIn(rl[1]))
            self.play(FadeIn(outs[1]))
        with self.say("Break a long night with a flash of light: the short-day plant stops flowering, the long-day plant flowers. So plants measure unbroken darkness."):
            self.play(FadeIn(bars[2]), FadeIn(rl[2]))
            self.play(Flash(bars[2][2].get_center(), color=WHITE, flash_radius=0.5))
            self.play(FadeIn(outs[2]))
        with self.say("The leaves sense it with phytochrome, and a signal, florigen, travels to the shoot tip."):
            self.play(Circumscribe(VGroup(bars, outs), color=th.AMBER), run_time=1.5)
        self.play(FadeOut(VGroup(head, bars, rl, crit, cl, hd, outs)))

    def p5_tropic(self):
        head = self.head("Tropic movements")
        tb_rows = [["tropism", "stimulus", "response"], ["phototropism", "light", "shoot +, root −"], ["gravitropism", "gravity", "root +, shoot −"],
                   ["hydrotropism", "water", "root +"], ["chemotropism", "chemical", "pollen tube to ovule"], ["thigmotropism", "touch", "tendril coils round support"]]
        with self.say("Tropic movements are growth movements whose direction follows the stimulus, like phototropism."):
            self.play(FadeIn(head))
            tb = B.table(tb_rows, [3.2, 2.6, 4.8], row_h=0.6, size=24, colors=[th.AMBER, th.BODY, th.INK]).move_to([0, -0.2, 0])
            B.reveal_table(self, tb, 4.0)
        self.play(FadeOut(tb))
        S0 = np.array([-0.6, 0.0, 0])
        bend = ValueTracker(0.0)
        sh = ValueTracker(0.0)
        seed = Ellipse(width=0.7, height=0.5, stroke_color="#E6DCA0", stroke_width=2.5, fill_color="#8A7A3A", fill_opacity=1).move_to(S0)
        shoot = always_redraw(lambda: P.organ(S0 + RIGHT * 0.25, 3.8, -bend.get_value(), w=0.22, rot=-PI / 2, aux=AUX, aux_shift=sh.get_value(), aux_n=10, aux_side=-1))
        root = always_redraw(lambda: P.organ(S0 + LEFT * 0.25, 3.6, -bend.get_value() * 1.1, w=0.18, rot=PI / 2, color=ROOT, fill=ROOT_F, aux=AUX, aux_shift=sh.get_value(), aux_n=10, aux_side=1))
        g_arrow = VGroup(Arrow([5.9, 1.4, 0], [5.9, -0.2, 0], buff=0, color=th.MUTED, stroke_width=4), T("gravity", size=20, color=th.MUTED).move_to([5.9, 1.7, 0]))
        cap = B.Captions(self, at=(0.0, -2.5, 0), width=12.4, size=25)
        with self.say("Lay a seedling sideways. Statoliths settle in the root cap, and auxin collects on the lower side of root and shoot.") as v:
            self.play(FadeIn(seed), FadeIn(shoot), FadeIn(root), FadeIn(g_arrow))
            self.play(sh.animate.set_value(1.0), run_time=max(1.5, v.left - 0.8))
            cap("Auxin collects on the LOWER side of both root and shoot.", color=AUX)
        with self.say("In the shoot that speeds lower-side growth, so it curves up. Roots are more sensitive, so the same auxin inhibits them, and the root curves down.") as v:
            self.play(bend.animate.set_value(1.0), run_time=max(2, v.left - 0.8))
            cap("Shoot: lower side grows faster → up.  Root: lower side inhibited → down.", color=th.MINT)
        nb = B.neby_in(self, "surprised", height=1.2, corner=UR, buff=0.9)
        self.wait(0.4)
        B.neby_out(self, nb)
        cap.clear()
        self.play(FadeOut(VGroup(head, seed, shoot, root, g_arrow)))
        self.remove(shoot, root)

    def p5_nastic(self):
        head = self.head("Nastic movements: Mimosa pudica")
        f = ValueTracker(0.0)
        dr = ValueTracker(0.0)
        Pv = np.array([-4.6, -1.8, 0])
        leaf = always_redraw(lambda: P.mimosa(f.get_value(), dr.get_value(), P=Pv, L=2.4, a0=0.95))
        stem = Line([-4.6, -3.1, 0], [-4.6, 1.4, 0], color=SHOOT, stroke_width=7)
        cap = B.Captions(self, at=(3.4, -0.3, 0), width=5.8, size=26)
        with self.say("Nastic movements have a direction fixed by the organ, not the stimulus. Some are growth movements, like Crocus flowers opening; others are turgor movements."):
            self.play(FadeIn(head), Create(stem), FadeIn(leaf))
            cap("Nastic movement", sub="Direction fixed by the organ, not by the stimulus. Growth or turgor.")
        finger = Dot([1.2, 2.0, 0], radius=0.14, color=th.CORAL)
        with self.say("Touch Mimosa pudica, lajjawati. An electrical signal spreads, the leaflets fold in pairs, and the leaf droops.") as v:
            self.play(FadeIn(finger))
            self.play(finger.animate.move_to(Pv + polar(2.4, 0.95) + polar(1.6, 0.95 + 0.35)), run_time=0.8)
            self.sfx("click", gain=-8)
            self.play(f.animate.set_value(1.0), run_time=1.2)
            self.play(dr.animate.set_value(0.85), FadeOut(finger), run_time=1.0, rate_func=rate_functions.ease_in_quad)
            cap("Seismonasty", color=th.CORAL, sub="Touch → electrical signal → leaflets fold, leaf droops, in 1 to 3 seconds.")
        Z = np.array([2.6, 1.0, 0])
        cells_u = VGroup(*[Circle(radius=0.28, stroke_color=SHOOT, stroke_width=2, fill_color="#2E5E3A", fill_opacity=1).move_to(Z + [-0.9 + 0.6 * i, 0.32, 0]) for i in range(4)])
        cells_l = VGroup(*[Circle(radius=0.28, stroke_color=SHOOT, stroke_width=2, fill_color="#2E5E3A", fill_opacity=1).move_to(Z + [-0.9 + 0.6 * i, -0.32, 0]) for i in range(4)])
        zl = VGroup(T("upper motor cells: stay turgid", size=19, color=th.MINT).move_to(Z + [0, 0.95, 0]), T("lower motor cells: lose K⁺ and water", size=19, color=th.CORAL).move_to(Z + [0, -0.95, 0]))
        zline = DashedLine(Pv + RIGHT * 0.25, Z + LEFT * 1.3, color=th.MUTED, stroke_width=2)
        with self.say("In the pulvinus at the leaf base, lower motor cells lose potassium and water and go limp, so the leaf drops."):
            cap.clear()
            self.play(Create(zline), FadeIn(cells_u), FadeIn(cells_l), FadeIn(zl))
            self.play(*[c_.animate.stretch(0.55, 1).set_fill("#4A3A2A") for c_ in cells_l], run_time=1.5)
        with self.say("Nothing grows; within ten to thirty minutes the cells refill and the leaf rises.") as v:
            self.play(*[c_.animate.stretch(1 / 0.55, 1).set_fill("#2E5E3A") for c_ in cells_l], dr.animate.set_value(0.0), f.animate.set_value(0.0), run_time=max(2, v.left - 0.4))
        self.play(FadeOut(VGroup(head, stem, leaf, cells_u, cells_l, zl, zline)))
        self.remove(leaf)
        rows = [["", "Tropic", "Nastic"], ["direction", "set by the stimulus", "set by the organ"], ["mechanism", "always growth", "growth or turgor"],
                ["permanence", "permanent", "turgor ones reversible"], ["examples", "phototropism, tendril coiling", "Crocus opening; Mimosa folding"]]
        tb = B.table(rows, [2.6, 4.6, 4.6], row_h=0.66, size=24, colors=[th.MUTED, th.AMBER, th.PINK]).move_to([0, 0.2, 0])
        hd = self.head("Tropic vs nastic")
        with self.say("So: tropic movements follow the stimulus, are always growth, and are permanent. Nastic movements follow the organ, may be growth or turgor, and turgor ones reverse.") as v:
            self.play(FadeIn(hd))
            B.reveal_table(self, tb, v.dur * 0.85)
        self.wait(2.0)
        self.play(FadeOut(VGroup(hd, tb)))
        self.quiz("The folding of Mimosa pudica leaflets on touch is an example of",
                  ["thigmotropism", "seismonasty", "photonasty", "hydrotropism"], 1,
                  "Last one. A lajjawati leaf folds when touched. Which movement is it?",
                  "Seismonasty: a nastic turgor movement. Thigmotropism is the trap: it is permanent directional growth, like a tendril coiling.")
        self.tip("Mimosa = seismonasty: nastic, turgor, reversible. Tendril = thigmotropism: tropic, growth, permanent.",
                 "Exam tip. Mimosa: seismonasty, nastic, turgor, reversible. Tendril: thigmotropism, tropic, growth, permanent.", state="wink", width=8.6)

    # ================================================================== ENDING
    def ending(self):
        self.recap([
            "Water moves to more negative Ψ; Ψw = Ψs + Ψp. Xylem sap is pulled: Ψp < 0.",
            "Stomata open as K⁺ floods guard cells; ABA closes them.",
            "Light reaction in thylakoids: ATP, NADPH, and O₂ from water.",
            "Calvin: 3 ATP + 2 NADPH per CO₂. C4 splits steps in space, CAM in time.",
            "Respiration: 30–32 ATP (old figure 38). RQ: fat 0.7, sugar 1, malic acid 1.33.",
            "Five hormones; tropisms are directional growth, Mimosa is turgor.",
        ], "Quick recap. Water moves to more negative potential, and xylem sap is pulled under tension. Potassium opens stomata; A B A closes them. The light reaction makes ATP, NADPH and oxygen from water. Calvin needs three ATP and two NADPH per carbon dioxide; C4 separates steps in space, CAM in time. Respiration gives thirty to thirty-two ATP; R Q is about zero point seven for fat. And five hormones; tropisms are growth, Mimosa is turgor.")
        self.outro("That was plant physiology. Remember the sal: the sun pulls a rope of water through it. Next, Unit 3, genetics. See you there.")
