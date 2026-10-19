import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import Flow, arrow, block, example, hatch, nothing, pipe_walls, sdash  # noqa: E402

WATER = "#1E5A8A"
C_P, C_U, C_W, C_T, C_V = th.SKY, th.MINT, th.CORAL, th.AMBER, th.PINK


def tank(center, w, h, level, color=WATER):
    c = np.array(center, dtype=float)
    walls = VGroup(Line(c + [-w / 2, h / 2, 0], c + [-w / 2, -h / 2, 0]), Line(c + [-w / 2, -h / 2, 0], c + [w / 2, -h / 2, 0]),
                   Line(c + [w / 2, -h / 2, 0], c + [w / 2, h / 2, 0])).set_stroke(th.BODY, 4)
    liq = Rectangle(width=w - 0.06, height=level, stroke_width=0, fill_color=color, fill_opacity=0.75)
    liq.move_to(c + [0, -h / 2 + level / 2 + 0.02, 0])
    return VGroup(liq, walls)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 3
    TITLE = "Fluid Statics"
    SUBTITLE = "Pressure, surfaces and flow"
    SECTIONS = ["Pressure and buoyancy", "Surface tension and surface energy", "Angle of contact and capillarity",
                "Viscosity", "Poiseuille's formula", "Stokes' law", "Equation of continuity", "Bernoulli's equation"]
    NEXT = "Unit 4 · First Law of Thermodynamics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        surf = 0.4
        water = Rectangle(width=12.4, height=3.4, stroke_width=0, fill_color=WATER, fill_opacity=0.7).move_to([0, surf - 1.7, 0])
        line = Line([-6.2, surf, 0], [6.2, surf, 0], color=th.SKY, stroke_width=3)
        nail = VGroup(Rectangle(width=0.12, height=1.0, fill_color="#9AA3B5", fill_opacity=1, stroke_width=0),
                      Rectangle(width=0.36, height=0.08, fill_color="#9AA3B5", fill_opacity=1, stroke_width=0).shift(UP * 0.5)).move_to([-4.2, 1.8, 0])
        hull = Polygon([-1.3, 0, 0], [1.3, 0, 0], [0.9, -0.75, 0], [-0.9, -0.75, 0], fill_color="#9AA3B5", fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        cabin = Rectangle(width=0.9, height=0.45, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=WHITE, stroke_width=2).next_to(hull, UP, buff=0)
        ship = VGroup(hull, cabin).move_to([0, 1.9, 0])
        needle = Line([3.0, 0, 0], [5.0, 0, 0], color="#C8CFDD", stroke_width=5).move_to([4.0, 1.8, 0])
        labs = VGroup(T("steel nail", size=26, color=th.MUTED).move_to([-4.2, 3.0, 0]), T("steel ship", size=26, color=th.MUTED).move_to([0, 3.0, 0]),
                      T("steel needle", size=26, color=th.MUTED).move_to([4.0, 3.0, 0]))
        with self.say("Three pieces of steel, and a tank of water. A nail, a ship, and a sewing needle. Steel is almost eight times denser than water. So all three should sink. Right?"):
            self.play(FadeIn(water), Create(line))
            self.play(LaggedStart(FadeIn(nail, shift=DOWN * 0.3), FadeIn(ship, shift=DOWN * 0.3), FadeIn(needle, shift=DOWN * 0.3), lag_ratio=0.3), FadeIn(labs))
        dimple = always_redraw(lambda: VMobject(stroke_color=th.SKY, stroke_width=3).set_points_smoothly(
            [[x, surf - (0.12 * np.exp(-((x - 4.0) / 0.9) ** 4) if needle.get_center()[1] < surf + 0.05 else 0), 0] for x in np.linspace(2.4, 5.6, 40)]))
        with self.say("Drop the nail. It sinks straight to the bottom, as expected."):
            self.sfx("whoosh_down", gain=-10)
            self.play(nail.animate.move_to([-4.2, -2.4, 0]), run_time=1.6, rate_func=rate_functions.ease_in_quad)
            self.sfx("thud", gain=-10)
        with self.say("Lower the ship. Thousands of tonnes of steel, and it floats."):
            self.play(ship.animate.move_to([0, surf + 0.05, 0]), run_time=1.6, rate_func=rate_functions.ease_out_back)
        self.add(dimple)
        with self.say("Now lay the needle gently on the surface. It floats too, resting in a tiny dent in the water, as if the surface were a stretched skin."):
            self.play(needle.animate.move_to([4.0, surf + 0.01, 0]), run_time=1.6, rate_func=smooth)
            self.play(Indicate(needle, color=th.AMBER), run_time=1.0)
        nb = self.neby("surprised", height=1.4).to_corner(DL, buff=0.5).shift(UP * 0.3)
        q = T("Same steel. Two different reasons.", size=34, color=th.AMBER, weight="BOLD", display=True).to_edge(DOWN, buff=0.5)
        with self.say("The ship and the needle both float, but for two completely different reasons. One is about pressure. The other is about the surface itself. By the end of this lesson, you will be able to explain both, and a lot more besides."):
            self.add(nb)
            self.play(FadeIn(nb, scale=0.5), FadeIn(q, shift=UP * 0.2))
        self.play(FadeOut(VGroup(water, line, nail, ship, needle, labs, q)), FadeOut(dimple), FadeOut(nb))
        self.remove(dimple, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 3: Fluid Statics. Anything that flows is a fluid: water, air, blood, honey. Today we follow fluids at rest, at their surfaces, and on the move."):
            pass
        self.end_title(g, nb)
        self.roadmap("Eight stops. Pressure and buoyancy. Surface tension and surface energy. Angle of contact and capillarity. Viscosity. Poiseuille's formula. Stokes' law. The equation of continuity. And finally, Bernoulli's equation.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        defs = VGroup(M(r"P = \frac{F}{A}", size=60), T("unit: pascal,  1 Pa = 1 N m⁻²  ·  a scalar", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).move_to([3.2, 2.0, 0])
        pin = VGroup(Polygon([-0.4, 0.5, 0], [0.4, 0.5, 0], [0.04, -0.6, 0], [-0.04, -0.6, 0], fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0),
                     Circle(radius=0.45, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).shift(UP * 0.7)).move_to([-4.6, 0.6, 0])
        thumb = RoundedRectangle(corner_radius=0.3, width=1.2, height=0.6, fill_color="#E9B48A", fill_opacity=1, stroke_width=0).next_to(pin, UP, buff=0)
        board = Rectangle(width=4.5, height=0.4, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0).next_to(pin, DOWN, buff=0).shift(RIGHT * 1.2)
        with self.say("Fluids cannot hold a shape, so we describe them with pressure: the normal force per unit area, P equals F over A, measured in pascals. A drawing pin shows why area matters: the same push from your thumb is gentle on the wide head, but enormous at the tiny point."):
            self.play(Write(defs[0]), FadeIn(defs[1]))
            self.play(FadeIn(board), FadeIn(pin), FadeIn(thumb))
            self.play(Indicate(pin[0], color=th.CORAL, scale_factor=1.1), run_time=1.2)
        self.play(FadeOut(VGroup(pin, thumb, board, defs)))
        self.column()
        self.vessels()
        self.hydraulic()
        self.archimedes()
        self.floating()
        example(self, "(a) Find the absolute pressure 10 m below the surface of Phewa Lake. (b) A block weighs 4.9 N in air and 3.92 N in water. Find its volume, density and relative density. (P₀ = 1.013 × 10⁵ Pa)",
                [r"P = P_0 + h\rho g = 1.013\times10^{5} + (10)(1000)(9.8) = 1.99\times10^{5}\ \text{Pa}",
                 r"U = 4.9 - 3.92 = 0.98\ \text{N} = V\rho_w g \;\Rightarrow\; V = \frac{0.98}{1000\times9.8} = 1.0\times10^{-4}\ \text{m}^{3}",
                 r"m = \frac{4.9}{9.8} = 0.5\ \text{kg},\quad \rho = \frac{0.5}{10^{-4}} = 5000\ \text{kg m}^{-3},\quad \text{R.D.} = 5"],
                ["Let us try two exam questions together. First, the absolute pressure ten metres below the surface of Phewa Lake. Second, a block that weighs four point nine newtons in air, and three point nine two newtons in water. Find its volume, density and relative density.",
                 "Absolute pressure is atmospheric plus h rho g. One point zero one three times ten to the five, plus ten times a thousand times nine point eight. That is about one point nine nine times ten to the five pascals. Ten metres of water adds almost one whole atmosphere.",
                 "The block seems lighter in water by zero point nine eight newtons. That loss is the upthrust, V rho g. So the volume is zero point nine eight over nine thousand eight hundred: one times ten to the minus four cubic metres.",
                 "Its mass is four point nine over nine point eight, half a kilogram. Density is mass over volume, five thousand kilograms per cubic metre, so its relative density is five."], size=34)
        self.quiz("A body floats in water with three-quarters of its volume submerged. Its relative density is…",
                  ["0.25", "0.50", "0.75", "1.33"], 2,
                  "Pause and think. A body floats with three quarters of its volume under water. What is its relative density?",
                  "C, zero point seven five. For a floating body, the fraction submerged equals the ratio of densities. Three quarters under means the body is three quarters as dense as water. Option A is the fraction above the water, a classic mix up.")

    def column(self):
        c = np.array([-3.4, -0.5, 0])
        w, H = 4.2, 4.4
        surf_y = c[1] + H / 2 - 0.3
        tk = tank(c, w, H, H - 0.3)
        h = ValueTracker(1.0)

        def col():
            y = surf_y - h.get_value()
            r = Rectangle(width=1.0, height=max(0.01, h.get_value()), stroke_color=th.AMBER, stroke_width=2, fill_color=th.AMBER, fill_opacity=0.25)
            r.move_to([c[0], (surf_y + y) / 2, 0])
            area = Rectangle(width=1.0, height=0.06, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to([c[0], y, 0])
            br = DoubleArrow([c[0] + 0.85, surf_y, 0], [c[0] + 0.85, y, 0], buff=0, color=th.INK, stroke_width=3, tip_length=0.15) if h.get_value() > 0.3 else nothing([c[0], y, 0])
            return VGroup(r, area, br, M("h", size=32).next_to(br, RIGHT, buff=0.1), M("A", size=28, color=th.AMBER).next_to(area, LEFT, buff=0.15))
        cg = always_redraw(col)
        der = VGroup(
            M(r"\text{weight of column} = (\rho A h)\,g", size=40),
            M(r"P = \frac{\rho A h g}{A}", size=44),
            M(r"P = h\rho g", size=64, color=C_P),
        ).arrange(DOWN, buff=0.4).move_to([3.2, 1.3, 0])
        with self.say("How does pressure grow as you go deeper? Take a small flat area A at depth h inside still water. It carries the whole column of water standing on top of it."):
            self.play(FadeIn(tk))
            self.add(cg)
            self.play(FadeIn(cg))
            self.play(h.animate.set_value(2.6), run_time=2.5)
        with self.say("The column has volume A h, mass rho A h, and weight rho A h g. Divide that weight by the area, and the area cancels. The pressure is h rho g."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
            self.play(Write(der[2]))
            self.sfx("impact", gain=-14)
        tags = VGroup(T("gauge pressure:  hρg", size=26, color=C_P), T("absolute pressure:  P₀ + hρg", size=26, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, -1.5, 0])
        with self.say("So pressure depends only on the depth, the density of the liquid and g. Go twice as deep, and the pressure doubles. h rho g alone is called the gauge pressure. Add the atmosphere pressing on the surface, P nought, and you get the absolute pressure."):
            self.play(h.animate.set_value(1.3), run_time=1.5)
            self.play(h.animate.set_value(3.8), run_time=2.0)
            self.play(FadeIn(tags, shift=UP * 0.2))
        self.play(FadeOut(VGroup(tk, der, tags)), FadeOut(cg))
        self.remove(cg)

    def vessels(self):
        base_y = -2.2
        H = 3.0
        shapes = [
            Polygon([-5.6, base_y, 0], [-4.2, base_y, 0], [-3.4, base_y + H + 0.4, 0], [-6.4, base_y + H + 0.4, 0]),
            Polygon([-1.4, base_y, 0], [0.2, base_y, 0], [0.2, base_y + 1.0, 0], [-0.4, base_y + 1.6, 0], [-0.4, base_y + H + 0.4, 0], [-0.8, base_y + H + 0.4, 0], [-0.8, base_y + 1.6, 0], [-1.4, base_y + 1.0, 0]),
            Polygon([3.2, base_y, 0], [5.2, base_y, 0], [4.6, base_y + H + 0.4, 0], [3.8, base_y + H + 0.4, 0]),
        ]
        fills = VGroup()
        for s in shapes:
            inter = Intersection(s, Rectangle(width=20, height=H, ).move_to([0, base_y + H / 2, 0]), fill_color=WATER, fill_opacity=0.75, stroke_width=0)
            fills.add(inter)
        outs = VGroup(*[s.copy().set_fill(opacity=0).set_stroke(th.BODY, 4) for s in shapes])
        lvl = DashedLine([-6.6, base_y + H, 0], [6.4, base_y + H, 0], color=th.SKY, stroke_width=2)
        gauges = VGroup()
        for x in [-4.9, -0.6, 4.2]:
            gauges.add(VGroup(Dot([x, base_y + 0.25, 0], radius=0.09, color=th.AMBER), T("same P", size=22, color=th.AMBER).move_to([x, base_y - 0.45, 0])))
        with self.say("This has a surprising consequence. Here are three vessels of very different shapes: a wide one, a strange narrow one, and a tapering one. Fill all three to the same depth."):
            self.play(Create(outs))
            self.play(FadeIn(fills), Create(lvl))
        with self.say("The pressure at the bottom is exactly the same in all three. It depends on depth, not on the shape of the vessel, nor on how much water it holds. Physicists call this the hydrostatic paradox."):
            self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in gauges], lag_ratio=0.3))
            self.sfx("tick", gain=-12)
        self.play(FadeOut(VGroup(outs, fills, lvl, gauges)))

    def hydraulic(self):
        y = -1.6
        small_x, big_x = -3.6, 2.4
        a, A = 0.5, 2.8
        d = ValueTracker(0)
        body = VGroup(
            Rectangle(width=a, height=2.4, stroke_color=th.BODY, stroke_width=4).move_to([small_x, y + 0.6, 0]),
            Rectangle(width=A, height=1.8, stroke_color=th.BODY, stroke_width=4).move_to([big_x, y + 0.3, 0]),
            Rectangle(width=big_x - small_x, height=0.5, stroke_color=th.BODY, stroke_width=4).move_to([(small_x + big_x) / 2, y - 0.85, 0]),
        )

        def liquid():
            ds = d.get_value()
            db = ds * a / A
            g = VGroup(Rectangle(width=a - 0.05, height=1.3 - ds, fill_color=WATER, fill_opacity=0.8, stroke_width=0).move_to([small_x, y - 0.6 + (1.3 - ds) / 2, 0]),
                       Rectangle(width=A - 0.05, height=1.0 + db, fill_color=WATER, fill_opacity=0.8, stroke_width=0).move_to([big_x, y - 0.6 + (1.0 + db) / 2, 0]),
                       Rectangle(width=big_x - small_x, height=0.45, fill_color=WATER, fill_opacity=0.8, stroke_width=0).move_to([(small_x + big_x) / 2, y - 0.85, 0]))
            ps = Rectangle(width=a - 0.02, height=0.15, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([small_x, y + 0.7 - ds + 0.07, 0])
            pb = Rectangle(width=A - 0.02, height=0.15, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([big_x, y + 0.4 + db + 0.07, 0])
            car = VGroup(RoundedRectangle(corner_radius=0.15, width=2.2, height=0.6, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0),
                         Circle(radius=0.18, fill_color=th.BG, fill_opacity=1, stroke_color=th.MUTED).shift(LEFT * 0.6 + DOWN * 0.32),
                         Circle(radius=0.18, fill_color=th.BG, fill_opacity=1, stroke_color=th.MUTED).shift(RIGHT * 0.6 + DOWN * 0.32)).next_to(pb, UP, buff=0.18)
            push = arrow([small_x, y + 1.9 - ds + 0.3, 0], [small_x, y + 0.9 - ds + 0.3, 0], th.AMBER, 6)
            return VGroup(g, ps, pb, car, push)
        lq = always_redraw(liquid)
        eq = VGroup(M(r"\frac{f}{a} = \frac{F}{A}", size=50), M(r"F = f\,\frac{A}{a}", size=50, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([-0.5, 1.2, 0])
        lab = T("Pascal's law: pressure applied to an enclosed fluid is transmitted undiminished", size=24, color=th.MUTED).to_edge(UP, buff=0.7)
        with self.say("Pascal's law says that pressure applied to an enclosed fluid is passed on, undiminished, to every part of it. Push down gently on a narrow piston of area a, and the same pressure acts on a wide piston of area A."):
            self.play(FadeIn(lab), Create(body))
            self.add(lq)
            self.play(FadeIn(lq))
            self.play(d.animate.set_value(0.9), run_time=2.5)
        with self.say("Same pressure on a bigger area means a bigger force. f over a equals F over A, so F is f times A over a. A small push lifts a whole car. That is the hydraulic lift, the hydraulic press, and the brakes in every vehicle on the road."):
            self.play(Write(eq))
            self.play(d.animate.set_value(0.2), run_time=1.0)
            self.play(d.animate.set_value(1.1), run_time=2.0)
        self.play(FadeOut(VGroup(body, eq, lab)), FadeOut(lq))
        self.remove(lq)

    def archimedes(self):
        c = np.array([-3.2, -0.6, 0])
        tk = tank(c, 4.6, 4.8, 4.4)
        surf_y = c[1] - 2.4 + 4.4
        depth = ValueTracker(0.6)
        Hc = 1.4

        def cyl():
            top = surf_y - depth.get_value()
            bot = top - Hc
            body = Rectangle(width=1.4, height=Hc, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=th.INK, stroke_width=2).move_to([c[0], (top + bot) / 2, 0])
            k = 0.55
            f1 = arrow([c[0], top + k * depth.get_value() + 0.02, 0], [c[0], top + 0.02, 0], th.CORAL, 6)
            f2 = arrow([c[0], bot - k * (depth.get_value() + Hc) - 0.02, 0], [c[0], bot - 0.02, 0], th.MINT, 6)
            sides = VGroup(*[arrow([c[0] + s * (0.7 + 0.55 * (depth.get_value() + Hc / 2) * 0.6), (top + bot) / 2, 0], [c[0] + s * 0.72, (top + bot) / 2, 0], th.MUTED, 4) for s in (-1, 1)])
            return VGroup(body, f1, f2, sides)
        cg = always_redraw(cyl)
        der = VGroup(
            M(r"F_1 = h_1\rho g A \ \ (\text{down})", size=36, color=th.CORAL),
            M(r"F_2 = h_2\rho g A \ \ (\text{up})", size=36, color=th.MINT),
            M(r"U = F_2 - F_1 = (h_2 - h_1)A\rho g = V\rho g", size=38),
            T("Upthrust = weight of fluid displaced", size=28, color=th.AMBER, weight="SEMIBOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.6, 0])
        if der.width > 6.4:
            der.scale_to_fit_width(6.4).move_to([3.3, 0.6, 0])
        with self.say("Now immerse a solid cylinder. The water pushes on every face. The sideways pushes cancel in pairs. On top, the water presses down. Underneath, it presses up."):
            self.play(FadeIn(tk))
            self.add(cg)
            self.play(FadeIn(cg))
        with self.say("The bottom face is deeper, so the upward push is bigger than the downward one. Push the cylinder deeper and both grow, but their difference stays the same."):
            self.play(depth.animate.set_value(2.2), run_time=3.0)
            self.play(depth.animate.set_value(1.0), run_time=2.0)
        with self.say("F one is h one rho g A, downwards. F two is h two rho g A, upwards. Their difference is h two minus h one, times A rho g, which is V rho g. And V rho is just the mass of water the body pushes aside."):
            self.play(Write(der[0]), Write(der[1]))
            self.play(Write(der[2]))
        with self.say("That is Archimedes' principle: the upthrust equals the weight of the fluid displaced."):
            self.play(FadeIn(der[3], shift=UP * 0.2))
            self.sfx("correct", gain=-14)
        self.play(FadeOut(VGroup(tk, der)), FadeOut(cg))
        self.remove(cg)

    def floating(self):
        surf = 0.2
        water = Rectangle(width=7.0, height=3.4, stroke_width=0, fill_color=WATER, fill_opacity=0.7).move_to([-2.9, surf - 1.7, 0])
        wl = Line([-6.4, surf, 0], [0.6, surf, 0], color=th.SKY, stroke_width=3)
        rho = ValueTracker(0.5)
        H = 2.2

        def blk():
            f = rho.get_value()
            bot = surf - f * H
            b = Rectangle(width=2.0, height=H, fill_color=th.AMBER, fill_opacity=0.85, stroke_color=WHITE, stroke_width=2).move_to([-2.9, bot + H / 2, 0])
            sub = Rectangle(width=2.0, height=max(0.01, f * H), fill_color=th.BG, fill_opacity=0.35, stroke_width=0).move_to([-2.9, bot + f * H / 2, 0])
            return VGroup(b, sub)
        bg = always_redraw(blk)
        n1 = DecimalNumber(0.5, num_decimal_places=2, font_size=44, color=th.AMBER)
        n2 = DecimalNumber(0.5, num_decimal_places=2, font_size=44, color=th.SKY)
        rd = VGroup(T("density of body ÷ density of water", size=22, color=th.MUTED), n1,
                    T("fraction under water", size=22, color=th.MUTED), n2).arrange(DOWN, buff=0.15).move_to([3.8, -0.9, 0])
        n1.add_updater(lambda m: m.set_value(rho.get_value()))
        n2.add_updater(lambda m: m.set_value(rho.get_value()))
        eq = M(r"V\rho_b g = V_s\rho_l g \;\Rightarrow\; \frac{V_s}{V} = \frac{\rho_b}{\rho_l}", size=42).move_to([3.0, 2.3, 0])
        with self.say("A body floats when the upthrust equals its weight. If it floats with volume V s under the liquid, then V rho b g equals V s rho l g. So the fraction submerged equals the ratio of the densities."):
            self.play(FadeIn(water), Create(wl))
            self.add(bg)
            self.play(FadeIn(bg), Write(eq))
            self.add(rd)
            self.play(FadeIn(rd))
        with self.say("Make the body denser, and it sinks lower. Lighter, and it rides higher. Ice in sea water has a density ratio of about zero point eight nine, so almost nine tenths of an iceberg hides below the surface."):
            self.play(rho.animate.set_value(0.25), run_time=1.8)
            self.play(rho.animate.set_value(0.89), run_time=2.5)
            self.wait(1)
        with self.say("And the steel ship? Its hull is a hollow shell full of air. Its average density, steel plus all that air, is less than water's, so it displaces its own weight of water long before it is full. A solid nail cannot do that."):
            self.play(rho.animate.set_value(0.4), run_time=2)
            nb = self.neby("success", height=1.3).to_corner(DR, buff=0.45)
            self.add(nb)
            self.play(FadeIn(nb, scale=0.5))
        self.play(FadeOut(VGroup(water, wl, eq)), FadeOut(bg), FadeOut(rd), FadeOut(nb))
        self.remove(bg, nb)

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows, cols = 6, 11
        x0, y0 = -6.0, -2.6
        dx, dy = 0.5, 0.5
        mols = VGroup()
        for r in range(rows):
            for k in range(cols):
                mols.add(Circle(radius=0.17, fill_color=th.SKY, fill_opacity=0.55, stroke_width=0).move_to([x0 + k * dx, y0 + r * dy, 0]))
        surf_y = y0 + (rows - 1) * dy
        line = Line([x0 - 0.3, surf_y + 0.22, 0], [x0 + (cols - 1) * dx + 0.3, surf_y + 0.22, 0], color=th.SKY, stroke_width=3)
        A = np.array([x0 + 5 * dx, y0 + 2 * dy, 0])
        B = np.array([x0 + 5 * dx, surf_y, 0])
        inner = VGroup(*[Arrow(A, A + 0.7 * np.array([np.cos(a), np.sin(a), 0]), buff=0.15, color=th.MINT, stroke_width=4) for a in np.arange(0, TAU, TAU / 8)])
        outer = VGroup(*[Arrow(B, B + 0.7 * np.array([np.cos(a), np.sin(a), 0]), buff=0.15, color=th.CORAL, stroke_width=4) for a in np.arange(PI, TAU + 0.01, PI / 4)])
        net = Arrow(B, B + DOWN * 1.1, buff=0.15, color=th.AMBER, stroke_width=7)
        sph_a = DashedVMobject(Circle(radius=0.8, color=th.MINT).move_to(A), num_dashes=24)
        sph_b = DashedVMobject(Circle(radius=0.8, color=th.CORAL).move_to(B), num_dashes=24)
        with self.say("Why can a needle rest on water? Zoom in to the molecules. They attract each other. That attraction between like molecules is called cohesion, and it acts only over a tiny range, about one nanometre, the sphere of molecular influence."):
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mols], lag_ratio=0.01), run_time=1.5)
            self.play(Create(line))
        with self.say("A molecule deep inside is surrounded on all sides. It is pulled equally in every direction, so the net force on it is zero."):
            self.play(Create(sph_a), Indicate(mols[2 * cols + 5], color=th.MINT))
            self.play(LaggedStart(*[GrowArrow(a) for a in inner], lag_ratio=0.05))
        with self.say("But a molecule at the surface has neighbours only below and beside it. Nothing pulls it upward. So it feels a net pull inward, into the liquid."):
            self.play(Create(sph_b), Indicate(mols[(rows - 1) * cols + 5], color=th.CORAL))
            self.play(LaggedStart(*[GrowArrow(a) for a in outer], lag_ratio=0.05))
            self.play(GrowArrow(net))
        txt = para("Every surface molecule is pulled inward, so the liquid keeps its surface as small as it can: free drops are spheres, and the surface acts like a stretched skin.", width=5.6, size=24, color=th.BODY).move_to([3.6, 1.2, 0])
        drop = Circle(radius=0.7, fill_color=th.SKY, fill_opacity=0.6, stroke_color=WHITE, stroke_width=2).move_to([3.6, -1.6, 0])
        blob = Square(side_length=1.3, fill_color=th.SKY, fill_opacity=0.6, stroke_color=WHITE, stroke_width=2).move_to([3.6, -1.6, 0]).rotate(0.3)
        with self.say("To bring a molecule up to the surface, work must be done against that inward pull. So a liquid keeps its surface area as small as it possibly can. That is why a free drop of rain pulls itself into a sphere, the shape with the least surface for its volume."):
            self.play(FadeIn(txt))
            self.play(FadeIn(blob))
            self.play(Transform(blob, drop), run_time=1.5, rate_func=rate_functions.ease_out_elastic)
        self.play(FadeOut(VGroup(mols, line, inner, outer, net, sph_a, sph_b, txt, blob)))
        defn = VGroup(M(r"T = \frac{F}{L}", size=60, color=C_T), T("force per unit length on a line drawn in the surface  ·  N m⁻¹  ·  [M T⁻²]", size=24, color=th.MUTED)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.8)
        with self.say("We measure that skin with surface tension, T: the force per unit length acting on an imaginary line drawn in the surface, at right angles to the line. Its unit is newton per metre."):
            self.play(Write(defn[0]), FadeIn(defn[1]))
        self.film(defn)
        self.bubble()
        self.needle_resolve()

    def film(self, defn):
        L = 2.0
        x0 = -5.6
        top, bot = 0.9, -1.1
        xw = ValueTracker(-2.6)
        frame = VGroup(Line([x0, top, 0], [-0.4, top, 0]), Line([x0, bot, 0], [-0.4, bot, 0]), Line([x0, top, 0], [x0, bot, 0])).set_stroke(th.BODY, 5)

        def film_():
            x = xw.get_value()
            return VGroup(Rectangle(width=x - x0, height=top - bot, stroke_width=0, fill_color=th.PINK, fill_opacity=0.25).move_to([(x + x0) / 2, (top + bot) / 2, 0]),
                          Line([x, top + 0.15, 0], [x, bot - 0.15, 0], color=th.AMBER, stroke_width=6),
                          arrow([x, (top + bot) / 2, 0], [x - 0.9, (top + bot) / 2, 0], C_T, 5))
        fg = always_redraw(film_)
        lbl = M(r"l", size=34).move_to([x0 - 0.35, (top + bot) / 2, 0])
        F = M(r"F = 2Tl", size=40, color=C_T).move_to([-3.2, -1.9, 0])
        der = VGroup(
            M(r"W = F x = 2Tl\,x", size=42),
            M(r"\Delta A = 2\,l\,x\ \ (\text{two surfaces})", size=38),
            M(r"W = T\,\Delta A \;\Rightarrow\; T = \frac{W}{\Delta A}", size=46, color=C_T),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.5, 0])
        with self.say("Here is a soap film stretched on a wire frame, with one side a light sliding wire of length l. The film pulls the wire inward. A film has two surfaces, front and back, so the force is two T l."):
            self.play(Create(frame), FadeIn(lbl))
            self.add(fg)
            self.play(FadeIn(fg), FadeIn(F))
        with self.say("Now pull the wire out slowly through a distance x. The work done is force times distance, two T l x. But two l x is exactly the new surface area created, front and back."):
            self.play(xw.animate.set_value(-0.9), run_time=2.5)
            self.play(Write(der[0]))
            self.play(Write(der[1]))
        with self.say("So W equals T times delta A. Surface tension is also the work done per unit increase in area: the surface energy, in joules per square metre. And since a joule per square metre is the same as a newton per metre, surface tension and surface energy are numerically equal."):
            self.play(Write(der[2]))
            self.play(xw.animate.set_value(-2.0), run_time=1.5)
            self.play(xw.animate.set_value(-0.9), run_time=1.5)
        self.play(FadeOut(VGroup(frame, lbl, F, der, defn)), FadeOut(fg))
        self.remove(fg)

    def bubble(self):
        r = ValueTracker(0.6)
        c1 = np.array([-3.6, 0.0, 0])
        c2 = np.array([1.2, 0.0, 0])
        drop = always_redraw(lambda: Circle(radius=r.get_value(), fill_color=th.SKY, fill_opacity=0.55, stroke_color=WHITE, stroke_width=2).move_to(c1))
        soap = always_redraw(lambda: VGroup(Circle(radius=r.get_value(), stroke_color=th.PINK, stroke_width=3, fill_color=th.PINK, fill_opacity=0.08),
                                            Circle(radius=r.get_value() + 0.08, stroke_color=th.PINK, stroke_width=3)).move_to(c2))
        l1 = VGroup(T("drop or air bubble in liquid", size=22, color=th.MUTED), M(r"\Delta P = \frac{2T}{r}", size=46, color=th.SKY)).arrange(DOWN, buff=0.2).move_to([-3.6, -2.4, 0])
        l2 = VGroup(T("soap bubble (two surfaces)", size=22, color=th.MUTED), M(r"\Delta P = \frac{4T}{r}", size=46, color=th.PINK)).arrange(DOWN, buff=0.2).move_to([1.2, -2.4, 0])
        note = para("Smaller bubble, larger excess pressure. Surface tension falls as temperature rises, and detergents lower it.", width=3.6, size=22, color=th.BODY).move_to([5.0, 0.4, 0])
        with self.say("Because the surface pulls inward, the pressure inside a curved surface is higher than outside. For a drop, or an air bubble inside a liquid, the excess pressure is two T over r. A soap bubble has two surfaces, so it is four T over r."):
            self.add(drop, soap)
            self.play(FadeIn(drop), FadeIn(soap))
            self.play(FadeIn(l1), FadeIn(l2))
        with self.say("Notice the r on the bottom. The smaller the bubble, the bigger the pressure inside. Surface tension also falls as temperature rises, and soap or detergent lowers it, which is why hot soapy water cleans so well."):
            self.play(r.animate.set_value(1.3), run_time=1.5)
            self.play(r.animate.set_value(0.35), run_time=1.5)
            self.play(FadeIn(note))
            self.play(r.animate.set_value(0.8), run_time=1.0)
        self.play(FadeOut(VGroup(l1, l2, note)), FadeOut(drop), FadeOut(soap))
        self.remove(drop, soap)
        example(self, "Find the work done in blowing a soap bubble of radius 3 cm, and the excess pressure inside it. (T = 0.03 N/m)",
                [r"\Delta A = 2 \times 4\pi r^{2} = 8\pi(0.03)^{2} = 2.26\times10^{-2}\ \text{m}^{2}",
                 r"W = T\,\Delta A = 0.03 \times 2.26\times10^{-2} = 6.79\times10^{-4}\ \text{J}",
                 r"\Delta P = \frac{4T}{r} = \frac{4\times0.03}{0.03} = 4\ \text{Pa}"],
                ["A worked example. Find the work done in blowing a soap bubble of radius three centimetres, and the excess pressure inside it. The surface tension is zero point zero three newtons per metre.",
                 "The bubble has two surfaces, each four pi r squared. So the area created is eight pi times zero point zero three squared, about two point two six times ten to the minus two square metres. Do not forget that factor of two. It is the most common mistake in this question.",
                 "Work equals T times the area: zero point zero three times two point two six times ten to the minus two, which is six point seven nine times ten to the minus four joules.",
                 "Excess pressure is four T over r: four times zero point zero three, over zero point zero three. Exactly four pascals."], size=38)

    def needle_resolve(self):
        surf = 0.0
        pts = lambda: [[x, surf - 0.45 * np.exp(-(x / 1.1) ** 2), 0] for x in np.linspace(-5, 5, 80)]
        water = Rectangle(width=10.4, height=2.6, stroke_width=0, fill_color=WATER, fill_opacity=0.6).move_to([0, -1.35, 0])
        skin = VMobject(stroke_color=th.SKY, stroke_width=4).set_points_smoothly(pts())
        needle = Circle(radius=0.17, fill_color="#C8CFDD", fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to([0, surf - 0.45 + 0.17, 0])
        ang = 0.55
        tl = Arrow([-0.05, -0.25, 0], [-0.05 - 1.6 * np.cos(ang), -0.25 + 1.6 * np.sin(ang), 0], buff=0, color=C_T, stroke_width=6)
        tr = Arrow([0.05, -0.25, 0], [0.05 + 1.6 * np.cos(ang), -0.25 + 1.6 * np.sin(ang), 0], buff=0, color=C_T, stroke_width=6)
        w = Arrow([0, -0.28, 0], [0, -1.6, 0], buff=0, color=th.CORAL, stroke_width=6)
        labs = VGroup(M("T", size=34, color=C_T).next_to(tl.get_end(), LEFT, buff=0.1), M("T", size=34, color=C_T).next_to(tr.get_end(), RIGHT, buff=0.1),
                      M("mg", size=34, color=th.CORAL).next_to(w.get_end(), RIGHT, buff=0.1))
        cap = para("The dent tilts the surface. Its pull along both sides has an upward part that holds the needle's small weight.", width=10, size=26, color=th.INK).to_edge(UP, buff=0.8)
        with self.say("Now the needle. Seen end on, it sits in a little dent in the surface. The surface pulls along itself on both sides, and because the dent is tilted, each pull has an upward part. Together they hold up the needle's small weight. The ship floats by upthrust. The needle floats by surface tension."):
            self.play(FadeIn(water), Create(skin))
            self.play(FadeIn(needle, shift=DOWN * 0.3))
            self.play(GrowArrow(tl), GrowArrow(tr), GrowArrow(w), FadeIn(labs))
            self.play(FadeIn(cap))
        self.play(FadeOut(VGroup(water, skin, needle, tl, tr, w, labs, cap)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        self.contact()
        self.capillary()
        example(self, "Find the rise of water in a capillary tube of internal diameter 0.4 mm. (T = 0.072 N/m, θ = 0°, ρ = 1000 kg/m³, g = 9.8 m/s²)",
                [r"r = 0.2\ \text{mm} = 2\times10^{-4}\ \text{m},\quad \cos 0^\circ = 1",
                 r"h = \frac{2T\cos\theta}{r\rho g} = \frac{2\times0.072\times1}{(2\times10^{-4})(1000)(9.8)}",
                 r"h = \frac{0.144}{1.96} = 0.0735\ \text{m} = 7.35\ \text{cm}"],
                ["Let us calculate one. Water rises in a capillary tube of internal diameter zero point four millimetres. Surface tension zero point zero seven two, angle of contact zero. How high does it rise?",
                 "Careful: the question gives the diameter. The radius is half of it, zero point two millimetres, two times ten to the minus four metres. And cosine of zero is one.",
                 "Substitute: two times zero point zero seven two, over two times ten to the minus four, times a thousand, times nine point eight.",
                 "That is zero point one four four over one point nine six: zero point zero seven three five metres. The water climbs seven point three five centimetres up a tube thinner than a pencil lead."], size=40)
        self.tip("In h = 2T cos θ / rρg, r is the INTERNAL RADIUS (halve a given diameter). For mercury, θ ≈ 140°, so cos θ is negative and h is a fall, not a rise.",
                 "Two traps in capillary questions. First, r is the internal radius. If the question gives a diameter, halve it. Second, watch the sign of cosine theta. For mercury the angle of contact is about one hundred forty degrees, cosine is negative, and the liquid falls instead of rising.", state="think")
        self.quiz("Water rises to height h in a capillary tube of radius r. In a tube of radius r/2 it rises to…",
                  ["h/2", "h", "2h", "4h"], 2,
                  "Pause and think. Water rises to height h in a tube of radius r. What happens in a tube of half the radius?",
                  "C, two h. The rise is inversely proportional to the radius: h equals two T cos theta over r rho g. Halve r and h doubles. Four h would be right if the rise went as one over r squared, which it does not.")

    def contact(self):
        y = -0.2
        tubes = []
        for cx, col, concave, name in [(-3.4, WATER, True, "water on glass"), (2.4, "#9AA3B5", False, "mercury on glass")]:
            w = 1.6
            walls = VGroup(Line([cx - w / 2, y + 1.6, 0], [cx - w / 2, y - 1.8, 0]), Line([cx + w / 2, y + 1.6, 0], [cx + w / 2, y - 1.8, 0])).set_stroke(th.BODY, 5)
            k = 0.45 if concave else -0.45
            xs = np.linspace(cx - w / 2 + 0.04, cx + w / 2 - 0.04, 40)
            top = [[x, y + k * ((x - cx) / (w / 2)) ** 2, 0] for x in xs]
            body = Polygon(*top, [cx + w / 2 - 0.04, y - 1.8, 0], [cx - w / 2 + 0.04, y - 1.8, 0], stroke_width=0, fill_color=col, fill_opacity=0.8)
            edge = VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly(top)
            lab = T(name, size=26, color=th.INK, weight="SEMIBOLD").move_to([cx, y - 2.3, 0])
            tubes.append((walls, body, edge, lab, cx, w, k))
        with self.say("When a liquid meets a solid, two attractions compete. Cohesion pulls liquid molecules to each other. Adhesion pulls them to the solid. Water is attracted to glass more than to itself, so it climbs the wall and makes a concave meniscus. Mercury prefers itself, so it pulls away and bulges up, convex."):
            for walls, body, edge, lab, *_ in tubes:
                self.play(Create(walls), FadeIn(body), Create(edge), FadeIn(lab), run_time=1.2)
        angs = VGroup()
        for (walls, body, edge, lab, cx, w, k), deg, col in zip(tubes, [20, 140], [th.MINT, th.CORAL]):
            P = np.array([cx - w / 2 + 0.04, y + k, 0])
            tang_dir = np.array([np.sin(np.radians(deg)), -np.cos(np.radians(deg)), 0])
            tline = Line(P, P + tang_dir * 1.0, color=col, stroke_width=4)
            arc = Arc(radius=0.45, start_angle=-PI / 2, angle=np.radians(deg), arc_center=P, color=col, stroke_width=3)
            angs.add(VGroup(tline, arc, M(r"\theta", size=30, color=col).move_to(P + 0.75 * np.array([np.sin(np.radians(deg / 2)), -np.cos(np.radians(deg / 2)), 0]))))
        tags = VGroup(T("θ acute (≈ 0°): wets, rises", size=24, color=th.MINT).move_to([-3.4, 2.4, 0]), T("θ obtuse (≈ 140°): does not wet, falls", size=24, color=th.CORAL).move_to([2.4, 2.4, 0]))
        with self.say("The angle of contact, theta, is the angle between the solid surface and the tangent to the liquid at the point of contact, measured through the liquid. For water on clean glass it is nearly zero. For mercury on glass it is about one hundred forty degrees."):
            self.play(LaggedStart(*[Create(a) for a in angs], lag_ratio=0.4), FadeIn(tags))
        self.play(FadeOut(VGroup(*[VGroup(*t[:4]) for t in tubes], angs, tags)))

    def capillary(self):
        base_y = -2.6
        surf_y = -1.6
        dish = VGroup(Rectangle(width=8.2, height=1.0, stroke_width=0, fill_color=WATER, fill_opacity=0.75).move_to([-2.4, base_y + 0.5, 0]),
                      Line([-6.5, base_y + 1.3, 0], [-6.5, base_y, 0]), Line([-6.5, base_y, 0], [1.7, base_y, 0]), Line([1.7, base_y, 0], [1.7, base_y + 1.3, 0])).set_stroke(th.BODY, 4)
        dish[0].set_stroke(width=0)
        radii = [0.45, 0.25, 0.13]
        xs = [-5.0, -2.4, 0.2]
        k = 0.42
        fill = ValueTracker(0)
        tubes = VGroup()
        for x, r in zip(xs, radii):
            tubes.add(VGroup(Line([x - r, surf_y - 0.6, 0], [x - r, 3.0, 0]), Line([x + r, surf_y - 0.6, 0], [x + r, 3.0, 0])).set_stroke(th.BODY, 3))

        def cols():
            g = VGroup()
            for x, r in zip(xs, radii):
                h = k / r * fill.get_value()
                g.add(Rectangle(width=2 * r - 0.04, height=h + 0.6, stroke_width=0, fill_color=WATER, fill_opacity=0.85).move_to([x, surf_y - 0.6 + (h + 0.6) / 2, 0]))
            return g
        cg = always_redraw(cols)
        with self.say("Dip three glass tubes of fine bore, narrower and narrower, into water. The water climbs up each one on its own. And the thinner the tube, the higher it climbs. This rise or fall of liquid in a narrow tube is capillarity."):
            self.play(FadeIn(dish), Create(tubes))
            self.add(cg)
            self.play(fill.animate.set_value(1.0), run_time=3.5, rate_func=rate_functions.ease_out_cubic)
        zx, zr = 4.4, 0.9
        zt = VGroup(Line([zx - zr, -2.6, 0], [zx - zr, 2.4, 0]), Line([zx + zr, -2.6, 0], [zx + zr, 2.4, 0])).set_stroke(th.BODY, 4)
        top = 1.0
        colz = Rectangle(width=2 * zr - 0.05, height=top + 2.6, stroke_width=0, fill_color=WATER, fill_opacity=0.8).move_to([zx, (top - 2.6) / 2, 0])
        ang = np.radians(15)
        tL = Arrow([zx - zr, top, 0], [zx - zr + 0.9 * np.sin(ang), top + 0.9 * np.cos(ang), 0], buff=0, color=C_T, stroke_width=5)
        tR = Arrow([zx + zr, top, 0], [zx + zr - 0.9 * np.sin(ang), top + 0.9 * np.cos(ang), 0], buff=0, color=C_T, stroke_width=5)
        W = Arrow([zx, -0.6, 0], [zx, -2.0, 0], buff=0, color=th.CORAL, stroke_width=6)
        hl = DoubleArrow([zx + zr + 0.25, -1.6, 0], [zx + zr + 0.25, top, 0], buff=0, color=th.INK, stroke_width=3, tip_length=0.15)
        labs = VGroup(M(r"T", size=30, color=C_T).next_to(tL.get_end(), LEFT, buff=0.05), M(r"W", size=30, color=th.CORAL).next_to(W, LEFT, buff=0.1),
                      M("h", size=30).next_to(hl, RIGHT, buff=0.08))
        self.play(FadeOut(VGroup(dish, tubes)), FadeOut(cg))
        self.remove(cg)
        self.play(Create(zt), FadeIn(colz))
        der = VGroup(
            M(r"F_{\uparrow} = (2\pi r)\,T\cos\theta", size=40, color=C_T),
            M(r"W = (\pi r^{2}h)\rho g", size=40, color=th.CORAL),
            M(r"2\pi r T\cos\theta = \pi r^{2}h\rho g", size=40),
            M(r"h = \frac{2T\cos\theta}{r\rho g}", size=60, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-2.4, 0.2, 0])
        with self.say("Why? Look at one tube. The liquid touches the glass all the way round a circle of length two pi r. Along that line, surface tension pulls along the liquid surface, at the angle of contact theta to the wall. Its vertical part, T cos theta per unit length, lifts the liquid. The upward force is two pi r T cos theta."):
            self.play(GrowArrow(tL), GrowArrow(tR), FadeIn(labs[0]))
            self.play(Write(der[0]))
        with self.say("It holds up the weight of the raised column: volume pi r squared h, times rho g."):
            self.play(GrowArrow(W), FadeIn(labs[1]), GrowFromCenter(hl), FadeIn(labs[2]))
            self.play(Write(der[1]))
        with self.say("Set them equal, cancel pi r, and the height is h equals two T cos theta, over r rho g. The r on the bottom says it all: the rise is inversely proportional to the radius. That is Jurin's law."):
            self.play(Write(der[2]))
            self.play(Write(der[3]))
            self.sfx("impact", gain=-14)
            self.play(Circumscribe(der[3], color=th.AMBER))
        self.play(FadeOut(VGroup(zt, colz, tL, tR, W, hl, labs, der)))
        apps = [("Lamp wick", "Oil climbs the fine threads of the wick to the flame."), ("Trees", "Water and sap rise through narrow vessels towards the leaves."),
                ("Blotting paper", "Ink soaks into the tiny gaps between fibres."), ("Ploughing", "Breaking soil capillaries stops water rising and evaporating.")]
        cards = VGroup()
        for i, (h, b) in enumerate(apps):
            box = self.panel(5.9, 1.4)
            g = VGroup(T(h, size=26, color=[th.AMBER, th.MINT, th.SKY, th.LIME][i], weight="BOLD"), para(b, width=5.3, size=21, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35))
        with self.say("Capillarity is all around you. Oil climbs a lamp wick. Water rises through the narrow vessels of a tree. Ink soaks into blotting paper. And farmers in the Terai plough their fields after rain to break the fine capillaries in the soil, so the water is not drawn up to the surface and lost.") as v:
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.6)
                self.hold(v.dur / 4 - 0.7)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        n = 8
        x0, x1 = -6.2, 0.6
        yb, yt = -2.2, 1.4
        dy = (yt - yb) / n
        shift = ValueTracker(0)
        table = Rectangle(width=x1 - x0 + 0.4, height=0.3, fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_width=0).move_to([(x0 + x1) / 2, yb - 0.15, 0])

        def layers():
            g = VGroup()
            for i in range(n):
                v = (i + 0.5) / n
                y = yb + dy * (i + 0.5)
                col = interpolate_color(ManimColor(th.SKY), ManimColor(th.PINK), v)
                g.add(Rectangle(width=x1 - x0, height=dy - 0.04, stroke_width=0, fill_color=col, fill_opacity=0.25).move_to([(x0 + x1) / 2, y, 0]))
                for k in range(4):
                    xx = x0 + ((k * 2.0 + shift.get_value() * v) % (x1 - x0))
                    g.add(Dot([xx, y, 0], radius=0.05, color=col))
                g.add(arrow([x0 + 0.3, y, 0], [x0 + 0.3 + 2.6 * v, y, 0], col, 4))
            plate = Rectangle(width=2.0, height=0.25, fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([x0 + 3.5 + (shift.get_value() * 1.0) % 2.0, yt + 0.13, 0])
            g.add(plate)
            return g
        lg = always_redraw(layers)

        def ticker(m, dt):
            shift.increment_value(dt * 1.5)
        clk = Mobject()
        clk.add_updater(ticker)
        with self.say("Pour honey and pour water. Both flow, but honey drags. That internal friction in a fluid is viscosity. Picture a liquid between a fixed table and a plate dragged along the top. The liquid moves in thin layers. The layer touching the table stays still. The layer touching the plate moves with it. Each layer slides over the next, dragging on its neighbours."):
            self.play(FadeIn(table))
            self.add(lg, clk)
            self.play(FadeIn(lg))
            self.wait(6)
        der = VGroup(
            M(r"\text{velocity gradient} = \frac{dv}{dx}", size=38),
            M(r"F = -\eta A\frac{dv}{dx}", size=54, color=th.AMBER),
            M(r"\eta:\ \text{N s m}^{-2} = \text{Pa s},\ \ [ML^{-1}T^{-1}]", size=34),
            M(r"1\ \text{Pa s} = 10\ \text{poise}", size=34, color=th.MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, 0.3, 0])
        if der.width > 5.4:
            der.scale_to_fit_width(5.4).move_to([3.9, 0.3, 0])
        with self.say("The speed changes steadily from layer to layer. The rate of change of velocity with distance, d v by d x, is the velocity gradient. Newton found that the viscous force between layers is proportional to the contact area and to the velocity gradient: F equals minus eta A d v by d x."):
            self.play(Write(der[0]))
            self.play(Write(der[1]))
        with self.say("Eta is the coefficient of viscosity, the force per unit area per unit velocity gradient. Its unit is newton second per metre squared, or pascal second. One pascal second is ten poise. The minus sign shows that the force opposes the sliding."):
            self.play(Write(der[2]), Write(der[3]))
            self.wait(1)
        heat = VGroup(T("heat a liquid  →  η falls  (warm honey pours)", size=24, color=th.MINT),
                      T("heat a gas  →  η rises", size=24, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(der, DOWN, buff=0.45).align_to(der, LEFT)
        with self.say("Viscosity is like friction, but it grows with speed. And heat changes it in opposite ways: warm honey pours easily, because heating makes a liquid less viscous. But a hot gas is more viscous."):
            self.play(FadeIn(heat[0], shift=UP * 0.2))
            self.play(FadeIn(heat[1], shift=UP * 0.2))
        self.play(FadeOut(VGroup(table, der, heat)), FadeOut(lg))
        self.remove(lg, clk)
        example(self, "A plate of area 0.1 m² is dragged at 0.5 m/s over a 1 mm layer of oil (η = 0.8 Pa s) on a fixed table. What force is needed?",
                [r"\frac{dv}{dx} = \frac{0.5}{10^{-3}} = 500\ \text{s}^{-1}", r"F = \eta A\frac{dv}{dx} = 0.8\times0.1\times500 = 40\ \text{N}"],
                ["Quick example. A plate of area zero point one square metres is dragged at half a metre per second over a one millimetre layer of oil, of viscosity zero point eight pascal seconds. What force is needed?",
                 "The velocity falls from half a metre per second to zero across one millimetre, so the gradient is zero point five over ten to the minus three: five hundred per second.",
                 "F equals eta A d v by d x: zero point eight times zero point one times five hundred. Forty newtons."], size=44)

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        R = 1.6
        x0, x1 = -6.4, 1.4
        mid = lambda x: -0.3
        half = lambda x: R
        walls = pipe_walls(x0, x1, half, mid)
        flow = Flow(x0, x1, half, mid, q=1.4, lanes=9, per_lane=8, color=th.SKY, profile=lambda f: 1.6 * (1 - f * f) + 0.05)
        prof = VGroup(*[Arrow([x0 + 0.6, -0.3 + f * R, 0], [x0 + 0.6 + 2.6 * (1 - f * f), -0.3 + f * R, 0], buff=0, color=th.AMBER, stroke_width=4,
                               max_tip_length_to_length_ratio=0.15) for f in np.linspace(-0.85, 0.85, 7)])
        env = VMobject(stroke_color=th.AMBER, stroke_width=3).set_points_smoothly([[x0 + 0.6 + 2.6 * (1 - f * f), -0.3 + f * R, 0] for f in np.linspace(-1, 1, 20)])
        q = M(r"Q = \frac{\pi P r^{4}}{8\eta l}", size=64, color=th.AMBER).move_to([4.3, 0.6, 0])
        qd = para("volume per second through a tube of radius r and length l, under a pressure difference P", width=4.4, size=20, color=th.MUTED).next_to(q, DOWN, buff=0.3)
        with self.say("Now let a viscous liquid flow steadily through a narrow horizontal tube. Because of viscosity, the liquid at the wall is at rest, and the liquid in the centre moves fastest. The velocity profile is a parabola."):
            self.play(Create(walls))
            self.add(flow)
            self.play(FadeIn(flow))
            self.play(LaggedStart(*[GrowArrow(a) for a in prof], lag_ratio=0.08), Create(env))
            self.wait(1)
        with self.say("Poiseuille found that the volume flowing per second is Q equals pi P r to the four, over eight eta l, where P is the pressure difference across the tube of length l."):
            self.play(Write(q), FadeIn(qd))
        self.play(FadeOut(VGroup(prof, env)))
        dim = VGroup(
            M(r"Q = K\left(\frac{P}{l}\right)^{a} r^{b}\,\eta^{c}", size=50),
            M(r"L^{3}T^{-1} = (ML^{-2}T^{-2})^{a}\,L^{b}\,(ML^{-1}T^{-1})^{c}", size=44),
            M(r"M:\ a + c = 0", size=44), M(r"T:\ -2a - c = -1", size=44), M(r"L:\ -2a + b - c = 3", size=44),
            M(r"a = 1,\ \ c = -1,\ \ b = 4", size=50, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -0.2, 0])
        self.play(FadeOut(walls), FadeOut(flow), q.animate.scale(0.7).to_corner(UR, buff=0.7), FadeOut(qd))
        self.remove(flow)
        with self.say("You can derive its form by dimensions, a favourite exam question. Suppose Q depends on the pressure gradient P over l, the radius r, and the viscosity eta, each to some power."):
            self.play(Write(dim[0]))
        with self.say("Write the dimensions of each side. Volume per second is L cubed T to the minus one. The pressure gradient is M L to the minus two T to the minus two. Viscosity is M L to the minus one T to the minus one."):
            self.play(Write(dim[1]))
        with self.say("Match the powers. For M: a plus c equals zero. For T: minus two a minus c equals minus one. For L: minus two a plus b minus c equals three."):
            self.play(Write(dim[2]), Write(dim[3]), Write(dim[4]))
        with self.say("Solve: a is one, c is minus one, and b is four. So Q is proportional to P r to the four over eta l. The constant, pi over eight, comes from the full theory."):
            self.play(Write(dim[5]))
            self.play(Circumscribe(dim[5], color=th.AMBER))
        self.play(FadeOut(dim))
        big = VGroup(*[Square(side_length=0.5, fill_color=th.SKY, fill_opacity=0.85, stroke_width=0) for _ in range(16)]).arrange_in_grid(4, 4, buff=0.08).move_to([-3.0, -0.4, 0])
        small = Square(side_length=0.5, fill_color=th.SKY, fill_opacity=0.85, stroke_width=0).move_to([3.0, -0.4, 0])
        lb = VGroup(T("radius r", size=26, color=th.INK).next_to(big, UP, buff=0.4), T("radius r / 2", size=26, color=th.INK).next_to(small, UP, buff=0.4).align_to(big.get_top() + UP * 0.4, DOWN))
        lb[1].move_to([3.0, lb[0].get_center()[1], 0])
        res = T("16 : 1", size=60, color=th.AMBER, weight="BOLD", display=True).move_to([0, -0.4, 0])
        with self.say("That fourth power is dramatic. Halve the radius, and the flow drops to one sixteenth. Sixteen cups of blood through a healthy artery, one cup through an artery narrowed to half. That is why even a slight narrowing of an artery makes the heart work so hard."):
            self.play(FadeIn(lb))
            self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in big], lag_ratio=0.05), FadeIn(small, scale=0.5))
            self.play(FadeIn(res, scale=0.6))
            nb = self.neby("surprised", height=1.4).to_corner(DR, buff=0.45)
            self.add(nb)
            self.play(FadeIn(nb, scale=0.5))
        self.play(FadeOut(VGroup(big, small, lb, res, q)), FadeOut(nb))
        self.remove(nb)
        example(self, "Water (η = 1.0 × 10⁻³ Pa s) flows through a horizontal tube of length 0.5 m and radius 1 mm under a pressure difference of 1000 Pa. Find Q, and Q if r is halved.",
                [r"Q = \frac{\pi P r^{4}}{8\eta l} = \frac{\pi(1000)(10^{-3})^{4}}{8(10^{-3})(0.5)}",
                 r"Q = \frac{\pi\times10^{-9}}{4\times10^{-3}} = 7.85\times10^{-7}\ \text{m}^{3}\,\text{s}^{-1}",
                 r"r \to r/2:\ \ Q' = \frac{Q}{16} = 4.91\times10^{-8}\ \text{m}^{3}\,\text{s}^{-1}"],
                ["Let us compute one. Water flows through a tube half a metre long, of radius one millimetre, under a pressure difference of a thousand pascals. Find the flow rate, and the flow if the radius is halved.",
                 "Substitute: pi times a thousand times ten to the minus three, to the power four, over eight times ten to the minus three times zero point five.",
                 "The top is pi times ten to the minus nine, the bottom is four times ten to the minus three. Q is seven point eight five times ten to the minus seven cubic metres per second, about zero point seven eight five cubic centimetres every second.",
                 "Halve the radius, and divide by sixteen: four point nine one times ten to the minus eight cubic metres per second."], size=38)
        self.quiz("In Poiseuille's formula, the rate of flow Q is proportional to…",
                  [M(r"r", size=40), M(r"r^{2}", size=40), M(r"r^{3}", size=40), M(r"r^{4}", size=40)], 3,
                  "Pause and think. In Poiseuille's formula, the rate of flow is proportional to which power of the radius?",
                  "D, r to the power four. Many students choose r squared, thinking of the cross sectional area. But a wider tube also lets the centre move faster, which adds two more powers of r.")

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        cx = -4.3
        top, bot = 2.6, -2.8
        jar = VGroup(Rectangle(width=2.4, height=top - bot, stroke_width=0, fill_color="#5A4A1E", fill_opacity=0.55).move_to([cx, (top + bot) / 2, 0]),
                     Line([cx - 1.2, top + 0.3, 0], [cx - 1.2, bot, 0]), Line([cx - 1.2, bot, 0], [cx + 1.2, bot, 0]), Line([cx + 1.2, bot, 0], [cx + 1.2, top + 0.3, 0])).set_stroke(th.BODY, 4)
        jar[0].set_stroke(width=0)
        t = ValueTracker(0)
        tau = 1.2
        vt = 1.0

        def v(tt):
            return vt * (1 - np.exp(-tt / tau))

        def y(tt):
            return top - 0.2 - 0.8 * vt * (tt - tau * (1 - np.exp(-tt / tau)))

        def ball():
            tt = t.get_value()
            p = np.array([cx, y(tt), 0])
            W = 1.3
            drag = (W - 0.35) * v(tt) / vt
            g = VGroup(Circle(radius=0.22, fill_color="#C8CFDD", fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to(p),
                       arrow(p + RIGHT * 0.35, p + RIGHT * 0.35 + DOWN * W, th.CORAL, 5),
                       arrow(p + LEFT * 0.35, p + LEFT * 0.35 + UP * 0.35, th.MINT, 5),
                       arrow(p + LEFT * 0.7, p + LEFT * 0.7 + UP * max(0.01, drag), th.AMBER, 5))
            return g
        bg = always_redraw(ball)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1.2, 0.5], x_length=5.2, y_length=2.6,
                  axis_config={"color": th.MUTED, "stroke_width": 2, "include_tip": False}).move_to([3.0, -1.6, 0])
        axl = VGroup(T("time", size=20, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT),
                     T("speed", size=20, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1))
        vline = DashedLine(ax.c2p(0, 1), ax.c2p(6, 1), color=th.AMBER, stroke_width=2)
        vlab = M(r"v_t", size=30, color=th.AMBER).next_to(vline, RIGHT, buff=0.1)
        curve = always_redraw(lambda: ax.plot(v, x_range=[0, max(0.06, t.get_value()), 0.03], color=th.SKY, stroke_width=4))
        stokes = M(r"F = 6\pi\eta r v", size=56, color=th.AMBER).move_to([3.0, 2.2, 0])
        legend = VGroup(M(r"mg", size=38, color=th.CORAL), M(r"U", size=38, color=th.MINT), M(r"6\pi\eta r v", size=38, color=th.AMBER)).arrange(RIGHT, buff=0.6).move_to([3.0, 1.0, 0])
        with self.say("Drop a small steel ball into a tall jar of oil. A sphere moving slowly through a fluid feels a drag that grows with its speed. Stokes showed that the drag is six pi eta r v."):
            self.play(FadeIn(jar))
            self.play(Write(stokes))
        with self.say("Watch the forces. The weight pulls down, and the upthrust pushes up. As the ball speeds up, the drag grows, until weight is exactly balanced by upthrust plus drag. From then on, the ball falls at a constant speed: the terminal velocity."):
            self.add(bg)
            self.play(FadeIn(bg), FadeIn(legend), Create(ax), FadeIn(axl))
            self.add(curve)
            self.play(Create(vline), FadeIn(vlab))
            self.play(t.animate.set_value(6), run_time=7, rate_func=linear)
        self.play(FadeOut(VGroup(ax, axl, vline, vlab, legend)), FadeOut(curve), stokes.animate.scale(0.7).move_to([3.0, 2.8, 0]))
        self.remove(curve)
        der = VGroup(
            M(r"\tfrac43\pi r^{3}\rho g = \tfrac43\pi r^{3}\sigma g + 6\pi\eta r v_t", size=38),
            M(r"6\pi\eta r v_t = \tfrac43\pi r^{3}(\rho - \sigma)g", size=38),
            M(r"v_t = \frac{2r^{2}(\rho - \sigma)g}{9\eta}", size=56, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.6, 0.2, 0])
        with self.say("At terminal velocity, the forces balance. Weight, four thirds pi r cubed rho g, equals upthrust, four thirds pi r cubed sigma g, plus the drag."):
            self.play(Write(der[0]))
        with self.say("Rearrange, and the terminal velocity is two r squared, times rho minus sigma, times g, over nine eta."):
            self.play(Write(der[1]))
            self.play(Write(der[2]))
            self.sfx("impact", gain=-14)
        apps = para("Terminal velocity grows as r²: tiny cloud droplets drift, big raindrops fall fast. Millikan used it to size his oil drops, and timing a falling ball measures η.", width=6.2, size=22, color=th.BODY).next_to(der, DOWN, buff=0.4)
        with self.say("The r squared explains why clouds float. Their droplets are so tiny that their terminal velocity is almost zero, while big raindrops fall fast. Millikan used this law to find the size of his oil drops, and so the charge of the electron. And timing a ball bearing falling through a liquid is how we measure its viscosity."):
            self.play(FadeIn(apps))
        self.play(FadeOut(VGroup(jar, stokes, der, apps)), FadeOut(bg))
        self.remove(bg)
        example(self, "A steel ball of radius 1 mm and density 7800 kg/m³ falls through oil of density 900 kg/m³ and viscosity 1.0 Pa s. Find its terminal velocity.",
                [r"v_t = \frac{2r^{2}(\rho-\sigma)g}{9\eta} = \frac{2(10^{-3})^{2}(7800-900)(9.8)}{9\times1.0}",
                 r"v_t = 1.50\times10^{-2}\ \text{m s}^{-1} \approx 1.5\ \text{cm s}^{-1}"],
                ["A steel ball of radius one millimetre and density seven thousand eight hundred falls through oil of density nine hundred and viscosity one pascal second. Find its terminal velocity.",
                 "Two times ten to the minus three squared, times seven eight hundred minus nine hundred, which is six thousand nine hundred, times nine point eight, all over nine.",
                 "That is one point five times ten to the minus two metres per second. About one and a half centimetres every second. Slow and steady."], size=40)

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        x0, x1 = -6.4, 6.4
        mid = lambda x: -0.2
        half = lambda x: 1.3 - 0.75 / (1 + np.exp(-(x - 0.0) * 2.2))
        walls = pipe_walls(x0, x1, half, mid)
        flow = Flow(x0, x1, half, mid, q=0.55, lanes=7, per_lane=12, color=th.SKY)
        s1 = VGroup(Line([-4.2, -0.2 - 1.3, 0], [-4.2, -0.2 + 1.3, 0], color=th.AMBER, stroke_width=4), M(r"A_1,\ v_1", size=34, color=th.AMBER).move_to([-4.2, 1.6, 0]))
        s2 = VGroup(Line([4.2, -0.2 - half(4.2), 0], [4.2, -0.2 + half(4.2), 0], color=th.MINT, stroke_width=4), M(r"A_2,\ v_2", size=34, color=th.MINT).move_to([4.2, 1.6, 0]))
        with self.say("Now fluids on the move. Take a steady flow of an incompressible liquid through a pipe that narrows. Watch the tracer particles. In the wide part they stroll. In the narrow part, they race."):
            self.play(Create(walls))
            self.add(flow)
            self.play(FadeIn(flow))
            self.wait(4)
        slab1 = Rectangle(width=0.55 * 1.3 / half(-4.2) * 1.2, height=2 * half(-4.2), stroke_width=0, fill_color=th.AMBER, fill_opacity=0.35).move_to([-4.2, -0.2, 0], aligned_edge=LEFT)
        slab2 = Rectangle(width=0.55 / half(4.2) * 1.2, height=2 * half(4.2), stroke_width=0, fill_color=th.MINT, fill_opacity=0.35).move_to([4.2, -0.2, 0], aligned_edge=LEFT)
        der = VGroup(M(r"\rho A_1 v_1\,\Delta t = \rho A_2 v_2\,\Delta t", size=42), M(r"A_1 v_1 = A_2 v_2 = \text{constant}", size=52, color=th.AMBER)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.55)
        with self.say("Why? In a short time delta t, the liquid entering the wide end fills a slab of length v one delta t, with mass rho A one v one delta t. The liquid leaving the narrow end fills a longer, thinner slab, rho A two v two delta t."):
            self.play(FadeIn(s1), FadeIn(s2))
            self.play(FadeIn(slab1), FadeIn(slab2))
            self.play(Write(der[0]))
        with self.say("No liquid is created or lost in between, so the two masses are equal. A one v one equals A two v two. That is the equation of continuity, conservation of mass for a flowing fluid. Where the pipe narrows, the fluid must speed up."):
            self.play(Write(der[1]))
            self.sfx("correct", gain=-14)
            self.wait(2)
        self.play(FadeOut(VGroup(walls, s1, s2, slab1, slab2, der)), FadeOut(flow))
        self.remove(flow)
        hose = para("Put your thumb over a hosepipe and the water shoots further. A river runs fast through a gorge and slowly across the plains.", width=10.0, size=28, color=th.INK)
        nb = self.neby("cool", height=1.5)
        g = Group(hose, nb).arrange(RIGHT, buff=0.5)
        with self.say("You have felt this. Press your thumb over the end of a hosepipe, and the water shoots further. The Trishuli races through its narrow gorges, and slows to a crawl when it spreads across the plains."):
            self.add(nb)
            self.play(FadeIn(hose), FadeIn(nb, scale=0.5))
        self.play(FadeOut(hose), FadeOut(nb))
        self.remove(nb)
        example(self, "Water flows at 2 m/s through a pipe of internal diameter 6 cm that narrows to 3 cm. Find the speed in the narrow part and the volume flow rate.",
                [r"v_2 = v_1\left(\frac{d_1}{d_2}\right)^{2} = 2\left(\frac{6}{3}\right)^{2} = 8\ \text{m s}^{-1}",
                 r"Q = A_1 v_1 = \pi(0.03)^{2}(2) = 5.65\times10^{-3}\ \text{m}^{3}\text{s}^{-1} = 5.65\ \text{L s}^{-1}"],
                ["A pipe of internal diameter six centimetres carries water at two metres per second, and narrows to three centimetres. Find the speed in the narrow part, and the flow rate.",
                 "Area goes as diameter squared. Halving the diameter quarters the area, so the speed is multiplied by four: eight metres per second.",
                 "The flow rate is A one v one: pi times zero point zero three squared, times two. That is five point six five times ten to the minus three cubic metres per second, about five and a half litres every second."], size=42)

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        defn = self.callout("key", M(r"P + \tfrac12\rho v^{2} + \rho g h = \text{constant}", size=50, color=th.INK), width=9)
        defn.to_edge(UP, buff=0.8)
        cond = T("steady  ·  streamline  ·  non-viscous  ·  incompressible  ·  along one streamline", size=22, color=th.MUTED).next_to(defn, DOWN, buff=0.25)
        with self.say("Continuity is conservation of mass. Bernoulli's equation is conservation of energy. For the steady, streamline flow of an ideal fluid, pressure, plus kinetic energy per unit volume, plus potential energy per unit volume, stays constant along a streamline."):
            self.play(FadeIn(defn, shift=DOWN * 0.2))
            self.play(FadeIn(cond))
        self.play(FadeOut(VGroup(defn, cond)))
        self.derive()
        self.venturi()
        self.torricelli()
        self.wing()
        self.tip("Bernoulli's equation needs steady, streamline, non-viscous, incompressible flow, and applies along ONE streamline. Not for turbulent flow, nor for a viscous liquid in a long pipe.",
                 "Exam tip. When you state Bernoulli's principle, write the conditions: steady, streamline flow of a non viscous, incompressible fluid, along a single streamline. Examiners look for them. And never apply it to turbulent flow, or to a real viscous liquid in a long pipe, where energy is lost as heat.")
        self.quiz("Bernoulli's equation expresses the conservation of…",
                  ["mass", "momentum", "energy", "angular momentum"], 2,
                  "Last check. Bernoulli's equation expresses the conservation of what? Pause and think.",
                  "C, energy. It is the work energy theorem written per unit volume of fluid. Mass is the trap: that is conservation of mass, the equation of continuity, A one v one equals A two v two.")

    def derive(self):
        x0, x1 = -6.4, 6.4
        mid = lambda x: -1.2 + 1.4 / (1 + np.exp(-x * 1.6))
        half = lambda x: 0.9 - 0.45 / (1 + np.exp(-x * 1.6))
        walls = pipe_walls(x0, x1, half, mid)
        flow = Flow(x0, x1, half, mid, q=0.4, lanes=5, per_lane=12, color=th.SKY)
        xa, xb = -4.0, 4.0
        la = VGroup(M(r"P_1,\ v_1,\ h_1", size=30, color=th.AMBER).move_to([xa, mid(xa) + 1.3, 0]))
        lb = VGroup(M(r"P_2,\ v_2,\ h_2", size=30, color=th.MINT).move_to([xb, mid(xb) + 1.0, 0]))
        pa = Arrow([xa - 1.2, mid(xa), 0], [xa - 0.2, mid(xa), 0], buff=0, color=th.AMBER, stroke_width=6)
        pb = Arrow([xb + 1.2, mid(xb), 0], [xb + 0.2, mid(xb), 0], buff=0, color=th.MINT, stroke_width=6)
        with self.say("Here is the derivation. A tube of flow rises and narrows. At the lower end, the pressure is P one, the speed v one and the height h one. At the upper end, P two, v two and h two."):
            self.play(Create(walls))
            self.add(flow)
            self.play(FadeIn(flow), FadeIn(la), FadeIn(lb))
            self.play(GrowArrow(pa), GrowArrow(pb))
        self.play(VGroup(walls, la, lb, pa, pb).animate.scale(0.8).shift(UP * 2.0), FadeOut(flow), run_time=0.8)
        self.remove(flow)
        der = VGroup(
            M(r"W = P_1 V - P_2 V = (P_1 - P_2)V", size=38),
            M(r"(P_1 - P_2)V = \tfrac12 m(v_2^{2} - v_1^{2}) + mg(h_2 - h_1)", size=38),
            M(r"m = \rho V:\quad P_1 - P_2 = \tfrac12\rho(v_2^{2} - v_1^{2}) + \rho g(h_2 - h_1)", size=38),
            M(r"P_1 + \tfrac12\rho v_1^{2} + \rho g h_1 = P_2 + \tfrac12\rho v_2^{2} + \rho g h_2", size=42, color=th.AMBER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.9, 0])
        if der.width > 12.6:
            der.scale_to_fit_width(12.6).move_to([0, -1.9, 0])
        with self.say("In a short time, a volume V of fluid is pushed in at the lower end, and an equal volume leaves at the top. The pressure behind does work P one V on it. Work P two V is done against the pressure ahead. The net work is P one minus P two, times V."):
            self.play(Write(der[0]))
        with self.say("By the work energy theorem, this net work equals the gain in kinetic energy, plus the gain in potential energy, of that mass m."):
            self.play(Write(der[1]))
        with self.say("Put m equals rho V, and divide everything by V."):
            self.play(Write(der[2]))
        with self.say("Now collect the ones on each side. P one plus half rho v one squared plus rho g h one, equals P two plus half rho v two squared plus rho g h two. That is Bernoulli's equation."):
            self.play(Write(der[3]))
            self.sfx("impact", gain=-12)
            self.play(Circumscribe(der[3], color=th.AMBER))
        self.play(FadeOut(VGroup(walls, la, lb, pa, pb, der)))

    def venturi(self):
        x0, x1 = -6.4, 2.2
        mid = lambda x: -1.0
        half = lambda x: 0.9 - 0.5 * np.exp(-((x + 2.1) / 1.0) ** 2)
        walls = pipe_walls(x0, x1, half, mid)
        flow = Flow(x0, x1, half, mid, q=0.4, lanes=5, per_lane=10, color=th.SKY)
        speed = ValueTracker(1.0)

        def gauges():
            g = VGroup()
            for x, k in [(-4.6, 1.0), (-2.1, 0.0)]:
                v = 0.4 / half(x)
                P = 3.0 - 1.5 * speed.get_value() * v * v
                top = mid(x) + half(x)
                g.add(Rectangle(width=0.3, height=max(0.05, P), stroke_width=0, fill_color=WATER, fill_opacity=0.9).move_to([x, top + max(0.05, P) / 2, 0]))
                g.add(Line([x - 0.17, top, 0], [x - 0.17, top + 3.2, 0], color=th.BODY, stroke_width=2), Line([x + 0.17, top, 0], [x + 0.17, top + 3.2, 0], color=th.BODY, stroke_width=2))
            return g
        gg = always_redraw(gauges)
        tags = VGroup(T("wide: slow, high P", size=22, color=th.AMBER).move_to([-4.9, -2.3, 0]), T("narrow: fast, low P", size=22, color=th.MINT).move_to([-0.6, -2.3, 0]))
        eq = VGroup(M(r"h_1 = h_2:", size=36), M(r"P_1 - P_2 = \tfrac12\rho(v_2^{2} - v_1^{2})", size=38, color=th.AMBER), M(r"A_1 v_1 = A_2 v_2", size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.4, 0])
        if eq.width > 4.4:
            eq.scale_to_fit_width(4.4).move_to([4.6, 0.4, 0])
        title = T("Venturi meter", size=32, color=th.INK, weight="BOLD").move_to([4.6, 2.4, 0])
        with self.say("Now the applications. First, the Venturi meter: a horizontal pipe with a narrow throat, and a vertical tube at the wide part and at the throat to show the pressure."):
            self.play(Create(walls), FadeIn(title))
            self.add(flow, gg)
            self.play(FadeIn(flow), FadeIn(gg))
        with self.say("In the throat the water moves faster, so by Bernoulli, its pressure must be lower. The water column above the throat is shorter. Faster flow, lower pressure. That is the heart of Bernoulli."):
            self.play(FadeIn(tags))
            self.wait(3)
        with self.say("The heights are equal, so P one minus P two equals half rho, times v two squared minus v one squared. Together with continuity, the measured pressure difference tells you the rate of flow."):
            self.play(Write(eq))
            self.wait(1.5)
        self.play(FadeOut(VGroup(walls, tags, eq, title)), FadeOut(flow), FadeOut(gg))
        self.remove(flow, gg)

    def torricelli(self):
        sc = 1.0
        ground = -2.9
        tx = -4.6
        H = 3.0
        hole_y = ground + 1.8
        surf = ground + H
        tk = VGroup(Rectangle(width=2.4, height=H, stroke_width=0, fill_color=WATER, fill_opacity=0.75).move_to([tx, ground + H / 2, 0]),
                    Line([tx - 1.2, ground + H + 0.4, 0], [tx - 1.2, ground, 0]), Line([tx - 1.2, ground, 0], [tx + 1.2, ground, 0]), Line([tx + 1.2, ground, 0], [tx + 1.2, ground + H + 0.4, 0])).set_stroke(th.BODY, 4)
        tk[0].set_stroke(width=0)
        gl = Line([-6.8, ground, 0], [6.8, ground, 0], color=th.FAINT, stroke_width=3)
        v = np.sqrt(2 * 9.8 * 1.2)
        tt = np.sqrt(2 * 1.8 / 9.8)
        x_land = v * tt
        k = 1.6
        jet = ParametricFunction(lambda s: np.array([tx + 1.2 + k * v * s, hole_y - 4.9 * s * s, 0]), t_range=[0, tt], color=th.SKY, stroke_width=5)
        hl = DoubleArrow([tx + 1.45, surf, 0], [tx + 1.45, hole_y, 0], buff=0, color=th.AMBER, stroke_width=3, tip_length=0.15)
        hlab = M(r"1.2\ \text{m}", size=28, color=th.AMBER).next_to(hl, RIGHT, buff=0.1)
        yl = DoubleArrow([tx + 1.45, hole_y, 0], [tx + 1.45, ground, 0], buff=0, color=th.MUTED, stroke_width=3, tip_length=0.15)
        ylab = M(r"1.8\ \text{m}", size=28, color=th.MUTED).next_to(yl, RIGHT, buff=0.1)
        land = Dot([tx + 1.2 + k * x_land, ground, 0], radius=0.1, color=th.CORAL)
        xd = DoubleArrow([tx + 1.2, ground - 0.25, 0], [tx + 1.2 + k * x_land, ground - 0.25, 0], buff=0, color=th.CORAL, stroke_width=3, tip_length=0.15)
        xl = M(r"x", size=30, color=th.CORAL).next_to(xd, DOWN, buff=0.05)
        der = VGroup(M(r"\tfrac12\rho v^{2} = \rho g h \;\Rightarrow\; v = \sqrt{2gh}", size=40, color=th.AMBER),
                     M(r"v = \sqrt{2(9.8)(1.2)} = 4.85\ \text{m s}^{-1}", size=36),
                     M(r"t = \sqrt{\tfrac{2(1.8)}{9.8}} = 0.606\ \text{s}", size=36),
                     M(r"x = vt = 4.85\times0.606 = 2.94\ \text{m}", size=38, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.6, 0])
        if der.width > 6.4:
            der.scale_to_fit_width(6.4).move_to([3.4, 1.6, 0])
        title = T("Torricelli's theorem", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.7).shift(LEFT * 3.4)
        with self.say("Second, Torricelli's theorem. A tank on the ground holds water three metres deep. A small hole is made in its side, one point two metres below the surface."):
            self.play(FadeIn(title), FadeIn(tk), Create(gl))
            self.play(GrowFromCenter(hl), FadeIn(hlab), GrowFromCenter(yl), FadeIn(ylab))
        with self.say("At the surface and at the hole, the pressure is atmospheric, and the surface barely moves. So Bernoulli leaves just half rho v squared equals rho g h. The water leaves at root two g h, the same speed as a stone falling through that height."):
            self.play(Write(der[0]))
            self.sfx("whoosh", gain=-14)
            self.play(Create(jet), run_time=1.2)
        with self.say("Here that is root of two times nine point eight times one point two: four point eight five metres per second. The hole is one point eight metres above the ground, and the jet leaves horizontally, so it falls for root of two times one point eight over nine point eight, zero point six zero six seconds."):
            self.play(Write(der[1]))
            self.play(Write(der[2]))
        with self.say("In that time it travels four point eight five times zero point six zero six: two point nine four metres from the foot of the tank. A long answer question, done in four lines."):
            self.play(Write(der[3]))
            self.play(FadeIn(land, scale=2), GrowFromCenter(xd), FadeIn(xl))
            self.sfx("correct", gain=-12)
        self.play(FadeOut(VGroup(title, tk, gl, hl, hlab, yl, ylab, jet, der, land, xd, xl)))

    def wing(self):
        wing = VMobject(fill_color=th.PANEL_EDGE, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        xs = np.linspace(-2.2, 2.2, 60)
        topc = [[x, -0.3 + 1.15 * np.sqrt(max(0, 1 - ((x + 0.6) / 2.8) ** 2)) * (1 - (x + 2.2) / 4.4 * 0.7), 0] for x in xs]
        botc = [[x, -0.3 - 0.12 * np.sin(np.pi * (x + 2.2) / 4.4), 0] for x in xs[::-1]]
        wing.set_points_as_corners(topc + botc + [topc[0]])
        wing.make_smooth()
        x0, x1 = -6.6, 6.6

        def ysh(x, y0):
            bump = (0.85 if y0 > 0 else -0.25) * np.exp(-(x / 2.2) ** 2) * np.exp(-abs(y0) * 0.5)
            return y0 + bump

        lines = VGroup(*[VMobject(stroke_color=th.SKY, stroke_width=2, stroke_opacity=0.5).set_points_smoothly([[x, ysh(x, y0), 0] for x in np.linspace(x0, x1, 60)]) for y0 in [-2.4, -1.7, -1.1, 0.75, 1.3, 1.9, 2.6]])
        t = ValueTracker(0)

        def parts():
            g = VGroup()
            for y0, v in [(0.75, 1.9), (1.3, 1.6), (-1.1, 1.0), (-1.7, 1.0)]:
                for k in range(6):
                    x = x0 + ((k * 2.2 + t.get_value() * v * 2.0) % (x1 - x0))
                    g.add(Dot([x, ysh(x, y0), 0], radius=0.06, color=th.AMBER if y0 > 0 else th.SKY))
            return g
        pg = always_redraw(parts)
        lift = Arrow([0, 0.2, 0], [0, 2.2, 0], buff=0, color=th.MINT, stroke_width=8)
        labs = VGroup(T("faster air above: lower pressure", size=24, color=th.AMBER).move_to([0, 3.0, 0]), T("slower air below: higher pressure", size=24, color=th.SKY).move_to([0, -3.0, 0]))
        with self.say("Third, the aeroplane wing. Its curved upper surface makes the air above it flow faster than the air below. Faster air, lower pressure. So the pressure underneath is greater, and the difference pushes the wing up. That is lift."):
            self.play(FadeIn(wing), Create(lines))
            self.add(pg)
            self.play(t.animate.set_value(3), run_time=3, rate_func=linear)
            self.play(FadeIn(labs), GrowArrow(lift), t.animate.set_value(5), run_time=2, rate_func=linear)
        with self.say("The same effect tears tin roofs off houses in a storm: fast wind over the roof, still air inside. And it works your atomiser, and the air hole of a Bunsen burner: a fast stream across the top of a tube lowers the pressure there, and the atmosphere pushes liquid or air in."):
            self.play(t.animate.set_value(10), run_time=6, rate_func=linear)
        self.play(FadeOut(VGroup(wing, lines, lift, labs)), FadeOut(pg))
        self.remove(pg)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"P = h\rho g\ (\text{gauge}),\ \ P = P_0 + h\rho g;\ \ \text{Pascal: } F = f\,A/a", size=32),
            M(r"\text{Upthrust } U = V\rho g;\ \ \text{floating: } V_s/V = \rho_b/\rho_l", size=32),
            M(r"T = F/L = W/\Delta A;\ \ \Delta P = 2T/r\ (\text{drop}),\ 4T/r\ (\text{soap bubble})", size=32),
            M(r"h = \frac{2T\cos\theta}{r\rho g}\quad(h \propto 1/r)", size=32),
            M(r"F = \eta A\,\frac{dv}{dx};\ \ Q = \frac{\pi P r^{4}}{8\eta l}", size=32),
            M(r"F = 6\pi\eta r v;\ \ v_t = \frac{2r^{2}(\rho - \sigma)g}{9\eta}", size=32),
            M(r"A_1v_1 = A_2v_2;\ \ P + \tfrac12\rho v^{2} + \rho g h = \text{const};\ \ v = \sqrt{2gh}", size=32),
        ], "Let us recap. Pressure in a liquid is h rho g and depends only on depth, and Pascal's law passes it on undiminished. Upthrust equals the weight of fluid displaced. Surface tension is force per unit length, equal to surface energy, with excess pressure two T over r, or four T over r for a soap bubble. Capillary rise is two T cos theta over r rho g. Viscous force is eta A d v by d x, and Poiseuille's flow goes as r to the four. Stokes' drag is six pi eta r v, giving the terminal velocity. Continuity conserves mass, and Bernoulli conserves energy, giving root two g h for a jet.")
        self.outro("That is fluid statics, from floating ships to flying planes. Next time, we turn up the heat, with the first law of thermodynamics. Keep practising, and see you in the next lesson on NEBians.")
