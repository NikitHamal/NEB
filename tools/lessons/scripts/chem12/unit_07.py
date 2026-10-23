import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402

CU = "#D9824B"
ZN = "#9FB3C8"
HG = "#C8CDD8"
FE = "#8A8F9C"
AG = "#E3E7F0"
RUST = "#B5562B"
CUSO4 = "#3E8EDE"


def flow(stages, y=2.35, w=2.3, h=0.85, color=th.AMBER):
    """A row of process boxes joined by arrows. stages: list of short labels."""
    boxes = VGroup()
    for s in stages:
        b = RoundedRectangle(corner_radius=0.15, width=w, height=h, fill_color=th.PANEL, fill_opacity=1, stroke_color=th.PANEL_EDGE, stroke_width=2)
        t = para(s, width=w - 0.25, size=20, color=th.INK, align="center")
        t.move_to(b)
        boxes.add(VGroup(b, t))
    boxes.arrange(RIGHT, buff=0.42).move_to([0, y, 0])
    if boxes.width > 13.0:
        boxes.scale_to_fit_width(13.0)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for a, b in zip(boxes, boxes[1:])])
    return boxes, arrows


def light(s, boxes, k, color=th.AMBER):
    anims = []
    for i, b in enumerate(boxes):
        if i == k:
            anims.append(b[0].animate.set_stroke(color, width=4).set_fill(th.PANEL_EDGE, opacity=1))
        else:
            anims.append(b[0].animate.set_stroke(th.PANEL_EDGE, width=2).set_fill(th.PANEL, opacity=1))
    s.play(*anims, run_time=0.4)


def eqs(*tex, size=32, y=0.6, color=th.INK):
    g = VGroup(*[chem(t, size=size, color=color) for t in tex]).arrange(DOWN, buff=0.28)
    g.move_to([0, y, 0])
    if g.width > 12.6:
        g.scale_to_fit_width(12.6)
    return g


def tube(center, color=C.WATER, opacity=0.35, h=2.2):
    c = np.array(center, dtype=float)
    w = 0.7
    outline = VMobject(stroke_color=th.INK, stroke_width=3).set_points_as_corners(
        [c + [-w / 2, h / 2, 0], c + [-w / 2, -h / 2 + w / 2, 0]])
    arc = Arc(radius=w / 2, start_angle=PI, angle=PI, arc_center=c + [0, -h / 2 + w / 2, 0], color=th.INK, stroke_width=3)
    right = Line(c + [w / 2, -h / 2 + w / 2, 0], c + [w / 2, h / 2, 0], color=th.INK, stroke_width=3)
    liq = VGroup(Rectangle(width=w - 0.06, height=h * 0.45, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(c + [0, -h / 2 + w / 2 + h * 0.225 - 0.05, 0]),
                 Sector(radius=w / 2 - 0.03, start_angle=PI, angle=PI, arc_center=c + [0, -h / 2 + w / 2, 0], fill_color=color, fill_opacity=opacity, stroke_width=0))
    return VGroup(liq, outline, arc, right)


def ppt_in(tb, color, n=22, seed=1):
    rng = np.random.default_rng(seed)
    c = tb[2].get_center()
    return VGroup(*[Dot(c + np.array([rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.35), 0]), radius=0.05, color=color) for _ in range(n)])


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 7
    TITLE = "Studies of Heavy Metals"
    SUBTITLE = "Copper, zinc, mercury, iron and silver"
    SECTIONS = ["Copper", "Zinc", "Mercury", "Iron", "Silver"]
    NEXT = "Unit 8 · Haloalkanes"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    def tests(self, title, items, narr_key=None):
        """items: list of (reagent label, precipitate colour or None, solution colour, result label). Builds test tubes."""
        head = T(title, size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        n = len(items)
        xs = np.linspace(-5.0, 5.0, n) if n > 1 else [0]
        tubes = VGroup()
        for x, (lab, pc, sc, res) in zip(xs, items):
            tb = tube([x, -0.4, 0], color=sc[0], opacity=sc[1])
            l1 = T(lab, size=20, color=th.AMBER, weight="BOLD").next_to(tb, UP, buff=0.2)
            l2 = para(res, width=2.3, size=18, color=th.BODY, align="center").next_to(tb, DOWN, buff=0.2)
            tubes.add(VGroup(tb, l1, l2))
        return head, tubes, xs

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        def sheet(x, coat, label):
            base = Rectangle(width=4.2, height=2.2, fill_color=FE, fill_opacity=1, stroke_width=0).move_to([x, -0.2, 0])
            c = Rectangle(width=4.2, height=0.25, fill_color=coat, fill_opacity=1, stroke_width=0).next_to(base, UP, buff=0)
            lab = T(label, size=28, color=coat, weight="BOLD").next_to(c, UP, buff=0.3)
            return VGroup(base, c, lab)
        g = sheet(-3.4, ZN, "galvanised iron (zinc coat)")
        t = sheet(3.4, "#D8DCE6", "tinned iron (tin coat)")
        with self.say("Two pieces of iron sheet. One is coated with zinc, galvanised, like the jasta roofing sheet on houses all over the hills. The other is coated with tin, like the inside of a food can. Both coatings keep air and water away from the iron."):
            self.play(FadeIn(g, shift=UP * 0.2))
            self.play(FadeIn(t, shift=UP * 0.2))
        sc1 = Line([-3.6, 0.95, 0], [-3.2, 0.62, 0], color=th.BG, stroke_width=10)
        sc2 = Line([3.2, 0.95, 0], [3.6, 0.62, 0], color=th.BG, stroke_width=10)
        with self.say("Now scratch both, right through to the iron, and leave them out in the rain for a few weeks."):
            self.sfx("click", gain=-6)
            self.play(Create(sc1), Create(sc2))
        rust = VGroup(*[Circle(radius=r, fill_color=RUST, fill_opacity=0.8, stroke_width=0).move_to([3.4 + dx, 0.3 + dy, 0]) for r, dx, dy in [(0.5, 0, 0), (0.35, 0.6, -0.4), (0.4, -0.6, -0.5), (0.3, 0.2, -0.8)]])
        zdot = VGroup(*[Dot([-3.4 + dx, 0.75 + dy, 0], radius=0.05, color=WHITE) for dx, dy in [(-0.3, 0.05), (0.2, -0.05), (0.4, 0.08), (-0.1, -0.1)]])
        with self.say("The galvanised sheet barely changes. A little of the zinc turns white, but the iron stays bright. The tinned sheet rusts around the scratch, and the rust spreads faster than it would on bare iron. Why would a coating make things worse?"):
            self.play(FadeIn(zdot), LaggedStart(*[GrowFromCenter(r) for r in rust], lag_ratio=0.3), run_time=3)
        nb = C.show_neby(self, "surprised", height=1.5, at=[0, -2.4, 0])
        with self.say("The answer lies in the chemistry of the five heavy metals in this unit. We will come back to it when we study iron."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(g, t, sc1, sc2, rust, zdot)))
        g_, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 7: Studies of Heavy Metals. Five metals, each with its ores, its extraction, its reactions and its important compounds: copper, zinc, mercury, iron and silver."):
            pass
        self.end_title(g_, nb)
        self.roadmap("Our five stops. Copper and blue vitriol. Zinc and white vitriol. Mercury, calomel and corrosive sublimate. Iron, steel and corrosion. And silver, with silver nitrate and silver chloride.")

    # ------------------------------------------------------------------ part 1: copper
    def p1(self):
        self.section(0)
        rows = [["Ore", "Formula", "Type"], ["copper pyrite (chief ore)", "CuFeS₂", "sulphide"], ["copper glance", "Cu₂S", "sulphide"],
                ["cuprite", "Cu₂O", "oxide, red"], ["malachite", "CuCO₃·Cu(OH)₂", "carbonate, green"], ["azurite", "2CuCO₃·Cu(OH)₂", "carbonate, blue"]]
        tb = C.table(rows, [4.6, 4.0, 3.4], row_h=0.62, size=26, colors=[th.INK, CU, th.BODY]).move_to(UP * 0.5)
        with self.say("Copper is the oldest worked metal: the repousse work of the Kathmandu valley and the gilded roofs of Pashupatinath. Its chief ore is copper pyrite, copper iron sulphide. Other ores are copper glance, cuprite, and the green and blue carbonates malachite and azurite.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        note = T("copper pyrite holds only 2–3 % copper: it must be concentrated first", size=26, color=th.AMBER).next_to(tb, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(0.6)
        self.play(FadeOut(VGroup(tb, note)))
        self.froth()
        self.cu_extraction()
        self.cu_refining()
        self.cu_properties()
        self.blue_vitriol()
        self.cu_oxides_examples()

    def froth(self):
        title = T("1. Froth flotation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        tank = C.Beaker(center=[-2.2, -0.8, 0], w=4.6, h=3.4, level=0.78, color="#7A8696", opacity=0.3)
        rng = np.random.default_rng(3)
        ore = VGroup(*[Dot(tank.c + np.array([rng.uniform(-2, 2), rng.uniform(-1.4, 0.8), 0]), radius=0.07, color=CU) for _ in range(26)])
        gang = VGroup(*[Square(side_length=0.13, fill_color="#B9A88A", fill_opacity=1, stroke_width=0).move_to(tank.c + np.array([rng.uniform(-2, 2), rng.uniform(-1.4, 0.8), 0])) for _ in range(26)])
        air = Arrow([-5.4, -2.3, 0], [-4.5, -2.3, 0], buff=0, color=th.SKY, stroke_width=5)
        al = T("air", size=22, color=th.SKY).next_to(air, UP, buff=0.05)
        txt = VGroup(T("pine oil wets the sulphide", size=24, color=CU), T("sulphide sticks to bubbles: rises in froth", size=24, color=CU),
                     T("water wets the gangue: it sinks", size=24, color="#B9A88A")).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.8, 0.0, 0])
        with self.say("Step one is concentration by froth flotation. Powdered ore is stirred in water with a little pine oil, and air is blown through. Sulphide particles are wetted by the oil, cling to the air bubbles and rise as a froth. The earthy gangue, wetted by water, sinks. It works because the ore is a sulphide."):
            self.play(FadeIn(title), FadeIn(tank.g), FadeIn(ore), FadeIn(gang))
            self.play(GrowArrow(air), FadeIn(al))
            bub = VGroup(*[Circle(radius=0.14, stroke_color=WHITE, stroke_width=2).move_to(tank.c + np.array([rng.uniform(-2, 2), -1.4, 0])) for _ in range(14)])
            self.play(FadeIn(bub))
            self.play(bub.animate.shift(UP * 2.4).set_opacity(0.4),
                      *[d.animate.move_to(tank.c + np.array([d.get_x() - tank.c[0], 1.15 + rng.uniform(0, 0.25), 0])) for d in ore],
                      *[q.animate.move_to(tank.c + np.array([q.get_x() - tank.c[0], -1.45 + rng.uniform(0, 0.15), 0])) for q in gang], run_time=2.5)
            self.play(LaggedStart(*[FadeIn(t_, shift=LEFT * 0.2) for t_ in txt], lag_ratio=0.4))
        self.play(FadeOut(VGroup(title, tank.g, ore, gang, air, al, txt, bub)))

    def cu_extraction(self):
        boxes, arrows = flow(["froth flotation", "roasting", "smelting", "Bessemer converter", "refining"])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in boxes], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.5)
        light(self, boxes, 1)
        e = eqs(r"2CuFeS_2 + O_2 \rightarrow Cu_2S + 2FeS + SO_2", r"2FeS + 3O_2 \rightarrow 2FeO + 2SO_2", r"2Cu_2S + 3O_2 \rightarrow 2Cu_2O + 2SO_2")
        n = T("deliberately incomplete: some Cu₂S must survive", size=24, color=th.AMBER).next_to(e, DOWN, buff=0.35)
        with self.say("Step two is roasting. The concentrate is heated in air in a reverberatory furnace at about ten seventy kelvin, below its melting point. Moisture goes, arsenic and antimony escape as volatile oxides, and the sulphides start to burn. Copper pyrite gives copper one sulphide and iron sulphide, and some of each is oxidised. Roasting is kept incomplete on purpose, because some copper sulphide is needed later."):
            self.play(FadeIn(e, shift=UP * 0.2))
            self.play(FadeIn(n))
        self.play(FadeOut(VGroup(e, n)))
        light(self, boxes, 2)
        e = eqs(r"FeO + SiO_2 \rightarrow FeSiO_3\ (\text{slag})", r"Cu_2O + FeS \rightarrow Cu_2S + FeO")
        n = T("product: copper matte, Cu₂S + FeS, about 45 % copper", size=24, color=th.AMBER).next_to(e, DOWN, buff=0.35)
        with self.say("Step three, smelting, in a water jacketed blast furnace with coke and sand. Silica is the flux. It carries the iron away as a fusible slag of iron silicate. Any copper oxide is turned back into sulphide by the iron sulphide. What collects below the slag is copper matte, a melt of copper and iron sulphides, about forty five percent copper."):
            self.play(FadeIn(e, shift=UP * 0.2))
            self.play(FadeIn(n))
        self.play(FadeOut(VGroup(e, n)))
        light(self, boxes, 3)
        e = eqs(r"2FeS + 3O_2 \rightarrow 2FeO + 2SO_2,\quad FeO + SiO_2 \rightarrow FeSiO_3", r"2Cu_2S + 3O_2 \rightarrow 2Cu_2O + 2SO_2")
        key = chem(r"2Cu_2O + Cu_2S \rightarrow 6Cu + SO_2\uparrow", size=48, color=th.AMBER).next_to(e, DOWN, buff=0.4)
        kl = T("auto-reduction: the ore reduces itself", size=26, color=th.AMBER).next_to(key, DOWN, buff=0.25)
        with self.say("Step four, the Bessemer converter, lined with silica. A hot air blast removes the last iron as slag and turns some copper sulphide into copper oxide. Then the oxide and sulphide react together: two copper one oxide plus copper one sulphide give six copper and sulphur dioxide. No outside reducing agent at all. This is auto reduction, or self reduction."):
            self.play(FadeIn(e, shift=UP * 0.2))
            self.sfx("impact", gain=-12)
            self.play(Write(key))
            self.play(FadeIn(kl))
        bl = T("blister copper, 98 % pure: escaping SO₂ blisters its surface", size=24, color=CU).to_edge(DOWN, buff=0.5)
        with self.say("The product is ninety eight percent pure, and is called blister copper, because escaping sulphur dioxide leaves blisters on its surface."):
            self.play(FadeIn(bl))
        self.play(FadeOut(VGroup(e, key, kl, bl)))
        light(self, boxes, 4)
        pole = T("poling: stirring with green wood poles reduces dissolved Cu₂O back to copper", size=24, color=th.BODY).move_to([0, 0.8, 0])
        with self.say("Step five, refining, in two stages. First, poling: the molten copper is stirred with poles of green wood, whose gases reduce any dissolved copper oxide. Then electrolytic refining."):
            self.play(FadeIn(pole))
        self.play(FadeOut(VGroup(boxes, arrows, pole)))

    def cu_refining(self):
        title = T("Electrolytic refining of copper", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        bk = C.Beaker(center=[-2.0, -1.0, 0], w=5.0, h=3.2, level=0.78, color=CUSO4, opacity=0.45)
        thin = ValueTracker(0)
        an = always_redraw(lambda: Rectangle(width=0.9 - 0.5 * thin.get_value(), height=3.0, fill_color="#B06A3A", fill_opacity=1, stroke_width=0).move_to([-3.6, -0.5, 0]))
        ca = always_redraw(lambda: Rectangle(width=0.15 + 0.5 * thin.get_value(), height=3.0, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([-0.4, -0.5, 0]))
        la = VGroup(T("anode (+)", size=22, color="#E0A070", weight="BOLD"), T("impure Cu", size=20, color="#E0A070")).arrange(DOWN, buff=0.05).move_to([-3.9, 1.65, 0])
        lc = VGroup(T("cathode (−)", size=22, color=CU, weight="BOLD"), T("pure Cu", size=20, color=CU)).arrange(DOWN, buff=0.05).move_to([-0.1, 1.65, 0])
        lab = T("15 % CuSO₄ + dilute H₂SO₄", size=20, color=CUSO4).next_to(bk.g, DOWN, buff=0.15)
        rows = VGroup(chem(r"\text{anode: } Cu \rightarrow Cu^{2+} + 2e^-", size=30), chem(r"\text{cathode: } Cu^{2+} + 2e^- \rightarrow Cu", size=30),
                      T("anode mud: Ag, Au, Pt (too noble to dissolve)", size=22, color=AG), T("left in solution: Zn²⁺, Fe²⁺ (too active to deposit)", size=22, color=th.BODY),
                      T("product: 99.95 % copper, for wiring", size=24, color=th.AMBER, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -0.3, 0])
        rows.scale_to_fit_width(min(rows.width, 6.6))
        rows.move_to([3.6, -0.3, 0])
        ph = ValueTracker(0)
        ions = always_redraw(lambda: VGroup(*[Dot([-3.1 + ((ph.get_value() + k / 6) % 1) * 2.2, -1.9 + 0.5 * k, 0], radius=0.07, color=CUSO4) for k in range(6)]))
        rng = np.random.default_rng(2)
        mud = VGroup(*[Dot([-3.6 + rng.uniform(-0.4, 0.4), -1.0 + rng.uniform(-0.4, 0.6), 0], radius=0.05, color=AG) for _ in range(12)])
        with self.say("The anode is a thick plate of impure blister copper. The cathode is a thin sheet of pure copper. The electrolyte is copper sulphate acidified with sulphuric acid. As current flows, the anode dissolves as copper ions, and pure copper deposits on the cathode."):
            self.play(FadeIn(title), FadeIn(bk.g), FadeIn(lab))
            self.add(an, ca, ions)
            self.play(FadeIn(an), FadeIn(ca), FadeIn(la), FadeIn(lc), FadeIn(ions))
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), thin.animate.set_value(0.5), ph.animate.set_value(2), run_time=3, rate_func=linear)
        with self.say("Noble metals like silver, gold and platinum do not dissolve. They fall below the anode as anode mud, a valuable by product. Active metals like zinc and iron dissolve but stay in solution. The cathode copper is ninety nine point nine five percent pure, good enough for electrical wiring."):
            self.play(FadeIn(mud), mud.animate.shift(DOWN * 0.9), thin.animate.set_value(1), ph.animate.set_value(4), run_time=3, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.4))
        self.play(FadeOut(VGroup(title, bk.g, la, lc, lab, rows, mud)), FadeOut(an), FadeOut(ca), FadeOut(ions))
        self.remove(an, ca, ions)

    def cu_properties(self):
        title = T("Reactions of copper", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rows = [["Reagent", "Reaction"],
                ["moist air + CO₂", "2Cu + O₂ + CO₂ + H₂O → CuCO₃·Cu(OH)₂ (green patina)"],
                ["air, red heat / above 1370 K", "2Cu + O₂ → 2CuO (black) / 4Cu + O₂ → 2Cu₂O (red)"],
                ["dilute HCl, dilute H₂SO₄", "no reaction: Cu is below hydrogen"],
                ["hot conc. H₂SO₄", "Cu + 2H₂SO₄ → CuSO₄ + SO₂ + 2H₂O"],
                ["dilute HNO₃", "3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O"],
                ["conc. HNO₃", "Cu + 4HNO₃ → Cu(NO₃)₂ + 2NO₂ + 2H₂O"]]
        tb = C.table(rows, [3.8, 8.6], row_h=0.62, size=23, colors=[th.AMBER, th.BODY]).next_to(title, DOWN, buff=0.35)
        with self.say("Copper is a soft, reddish metal, second only to silver as a conductor. In moist air it slowly grows a green patina of basic carbonate. Heated in air it forms black copper two oxide, and above thirteen seventy kelvin, red copper one oxide. Being below hydrogen, it does not react with dilute hydrochloric or sulphuric acid. But oxidising acids attack it: hot concentrated sulphuric acid gives sulphur dioxide, dilute nitric acid gives nitric oxide, and concentrated nitric acid gives brown nitrogen dioxide.") as v:
            self.play(FadeIn(title))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(VGroup(title, tb)))
        t1 = tube([-4.2, -0.4, 0], color="#E6E9F2", opacity=0.15)
        cu = Rectangle(width=0.18, height=1.6, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([-4.2, -0.3, 0])
        l1 = VGroup(T("Cu + NH₃(aq) + air", size=22, color=th.AMBER), T("deep blue: Schweitzer's reagent", size=20, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(t1, DOWN, buff=0.2)
        e1 = chem(r"2Cu + 8NH_3 + O_2 + 2H_2O \rightarrow 2[Cu(NH_3)_4](OH)_2", size=30).move_to([1.6, 2.4, 0])
        with self.say("Copper dissolves slowly in ammonia solution if air is present, giving the deep blue tetrammine copper ion. That solution is Schweitzer's reagent. It dissolves cellulose, and squirting the solution into acid regenerates the cellulose as fibre: the first artificial silk, rayon."):
            self.play(FadeIn(t1), FadeIn(cu), FadeIn(l1))
            self.play(t1[0].animate.set_fill(color="#2F4FE0", opacity=0.85), Write(e1), run_time=2)
        t2 = tube([0.0, -0.4, 0], color=AG, opacity=0.1)
        cu2 = Rectangle(width=0.18, height=1.6, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([0.0, -0.3, 0])
        tree = VGroup(*[Line([0.0, -0.6 + 0.25 * k, 0], [0.0 + (0.25 if k % 2 else -0.25), -0.45 + 0.25 * k, 0], color=AG, stroke_width=4) for k in range(5)])
        l2 = VGroup(T("Cu + AgNO₃", size=22, color=th.AMBER), T("silver tree; solution turns blue", size=20, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(t2, DOWN, buff=0.2)
        t3 = tube([4.2, -0.4, 0], color="#D9A03A", opacity=0.6)
        cu3 = Rectangle(width=0.18, height=1.6, fill_color=CU, fill_opacity=1, stroke_width=0).move_to([4.2, -0.3, 0])
        l3 = VGroup(T("Cu + FeCl₃", size=22, color=th.AMBER), T("copper dissolves! (PCB etching)", size=20, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(t3, DOWN, buff=0.2)
        e2 = VGroup(chem(r"Cu + 2AgNO_3 \rightarrow Cu(NO_3)_2 + 2Ag", size=30), chem(r"Cu + 2FeCl_3 \rightarrow CuCl_2 + 2FeCl_2", size=30)).arrange(DOWN, buff=0.2).move_to([1.6, 2.2, 0])
        with self.say("Copper displaces metals below it. In silver nitrate it grows a glittering silver tree, and the solution turns blue. And here is a trap. Copper dissolves in iron three chloride, even though iron is above copper. That is because the couple involved is iron three over iron two, at plus zero point seven seven volts, which sits above copper. This reaction etches printed circuit boards."):
            self.play(FadeOut(e1), FadeIn(t2), FadeIn(cu2), FadeIn(l2))
            self.play(Create(tree), t2[0].animate.set_fill(color=CUSO4, opacity=0.4), Write(e2[0]), run_time=1.6)
            self.play(FadeIn(t3), FadeIn(cu3), FadeIn(l3))
            self.play(cu3.animate.stretch(0.4, 0), t3[0].animate.set_fill(color="#5C9E7A", opacity=0.6), Write(e2[1]), run_time=1.6)
        self.play(FadeOut(VGroup(t1, cu, l1, t2, cu2, tree, l2, t3, cu3, l3, e2)))
        uses = VGroup(*[C.card(self, a, b, w=3.9, h=1.9, color=c, tsize=24, bsize=20) for a, b, c in [
            ("Electrical", "wiring, cables, motor windings", CU), ("Heat", "utensils, boilers, calorimeters", th.AMBER),
            ("Alloys", "brass Cu+Zn, bronze Cu+Sn, German silver Cu+Zn+Ni", th.SKY), ("Plating & craft", "electroplating, roofing, repoussé", th.MINT),
            ("Farming", "Bordeaux mixture fungicide", th.LIME), ("Coins", "coinage alloys", th.PINK)]]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25))
        with self.say("Its uses: electrical wiring, cooking vessels and boilers, the alloys brass, bronze, gun metal and German silver, electroplating and temple craft, and copper salts as fungicides.") as v:
            for c in uses:
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 6 - 0.45)
        self.play(FadeOut(uses))

    def blue_vitriol(self):
        title = T("Blue vitriol, CuSO₄·5H₂O", size=32, color=CUSO4, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        prep = VGroup(chem(r"CuO + H_2SO_4 \rightarrow CuSO_4 + H_2O", size=32), chem(r"2Cu + 2H_2SO_4 + O_2 \rightarrow 2CuSO_4 + 2H_2O\ (\text{industrial})", size=30)).arrange(DOWN, buff=0.25).next_to(title, DOWN, buff=0.4)
        st = VGroup(T("really:", size=24, color=th.MUTED), chem(r"[Cu(H_2O)_4]SO_4\cdot H_2O", size=40, color=th.AMBER)).arrange(RIGHT, buff=0.3).next_to(prep, DOWN, buff=0.45)
        sl = T("four waters bonded to Cu²⁺; the fifth hydrogen-bonded to sulphate", size=22, color=th.BODY).next_to(st, DOWN, buff=0.2)
        with self.say("Blue vitriol, nilathotha, is copper sulphate pentahydrate. It is made by dissolving copper oxide or carbonate in warm dilute sulphuric acid, or industrially by blowing air through scrap copper in the acid. Its structure is not five loose waters: four are bonded to the copper ion and the fifth is hydrogen bonded to the sulphate."):
            self.play(FadeIn(title), Write(prep))
            self.play(FadeIn(st))
            self.play(FadeIn(sl))
        self.play(FadeOut(VGroup(prep, st, sl)))
        temps = [(25, "#2F7BE0", "CuSO₄·5H₂O, blue"), (100, "#8EC9F0", "CuSO₄·H₂O, pale blue"), (230, "#F2F2F2", "CuSO₄, white"), (720, "#222222", "CuO, black")]
        heap = Polygon([-1.6, -1.6, 0], [1.6, -1.6, 0], [0.9, -0.5, 0], [-0.9, -0.5, 0], fill_color=temps[0][1], fill_opacity=1, stroke_color=th.INK, stroke_width=2).move_to([-2.6, -0.8, 0])
        tv = DecimalNumber(25, num_decimal_places=0, font_size=54, color=th.CORAL, unit=r"^{\circ}\mathrm{C}").move_to([-2.6, 1.2, 0])
        eqs_ = VGroup(chem(r"CuSO_4\cdot 5H_2O \xrightarrow{100^{\circ}C} CuSO_4\cdot H_2O + 4H_2O", size=30), chem(r"CuSO_4\cdot H_2O \xrightarrow{230^{\circ}C} CuSO_4 + H_2O", size=30),
                      chem(r"CuSO_4 \xrightarrow{720^{\circ}C} CuO + SO_3", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([2.8, -0.2, 0])
        with self.say("Heat it, and the water leaves in clear stages. At a hundred degrees, four waters go, and the blue fades to pale blue. At two hundred and thirty, the last one goes, leaving white anhydrous copper sulphate. At seven hundred and twenty, it decomposes to black copper oxide and sulphur trioxide."):
            self.play(FadeIn(heap), FadeIn(tv))
            for k in range(1, 4):
                self.play(ChangeDecimalToValue(tv, temps[k][0]), heap.animate.set_fill(temps[k][1]), FadeIn(eqs_[k - 1], shift=LEFT * 0.2), run_time=1.6)
        test = T("white anhydrous CuSO₄ turns blue with water: the test for water", size=24, color=th.AMBER).to_edge(DOWN, buff=0.5)
        with self.say("And that white powder turns blue again when water touches it, the standard laboratory test for water."):
            self.play(FadeIn(test))
            self.play(heap.animate.set_fill("#2F7BE0"), run_time=1.0)
        self.play(FadeOut(VGroup(title, heap, tv, eqs_, test)))
        head, tubes, xs = self.tests("Reactions of copper sulphate solution", [
            ("NaOH", None, (CUSO4, 0.45), "blue gelatinous Cu(OH)₂"),
            ("NH₃, excess", None, ("#2F4FE0", 0.85), "deep blue [Cu(NH₃)₄]²⁺"),
            ("H₂S", None, (CUSO4, 0.45), "black CuS"),
            ("KI", None, ("#8A5A2A", 0.55), "white Cu₂I₂ + brown I₂"),
            ("Fe or Zn", None, ("#B8D0A0", 0.35), "red-brown copper deposits")])
        pcols = ["#4A90E2", None, "#151515", "#EDEDED", CU]
        pp = VGroup()
        with self.say("The reactions of copper sulphate solution are examined every year. Sodium hydroxide gives a blue gelatinous precipitate of copper hydroxide. A little ammonia gives the same, but excess ammonia dissolves it to the deep blue tetrammine complex. Hydrogen sulphide gives black copper sulphide.") as v:
            self.play(FadeIn(head))
            for k in range(3):
                self.play(FadeIn(tubes[k]), run_time=0.5)
                if pcols[k]:
                    d_ = ppt_in(tubes[k][0], pcols[k], seed=k)
                    pp.add(d_)
                    self.play(FadeIn(d_), run_time=0.5)
        with self.say("Potassium iodide is special. It reduces copper two to copper one: a white precipitate of copper one iodide, coloured brown by the iodine released. Cyanide does the same. And iron or zinc displaces red brown copper metal."):
            for k in range(3, 5):
                self.play(FadeIn(tubes[k]), run_time=0.5)
                d_ = ppt_in(tubes[k][0], pcols[k], seed=k)
                pp.add(d_)
                self.play(FadeIn(d_), run_time=0.5)
        ki = chem(r"2CuSO_4 + 4KI \rightarrow Cu_2I_2\downarrow + 2K_2SO_4 + I_2", size=32, color=th.AMBER).to_edge(DOWN, buff=0.45)
        self.play(Write(ki))
        self.wait(0.6)
        self.play(FadeOut(VGroup(head, tubes, ki, pp)))
        uses = para("Uses of blue vitriol: Bordeaux mixture against blight on potato, tomato and grape; electroplating; Fehling's and Benedict's solutions; a mordant; an algicide in water tanks; the laboratory test for water.", width=11.5, size=28, color=th.BODY)
        with self.say("Blue vitriol is used in Bordeaux mixture against potato blight, in electroplating baths, in Fehling's and Benedict's solutions for sugars, as a mordant in calico printing, and as an algicide in water tanks."):
            self.play(FadeIn(uses))
        self.play(FadeOut(uses))

    def cu_oxides_examples(self):
        rows = [["", "Red oxide", "Black oxide"], ["name", "copper(I) oxide, cuprous", "copper(II) oxide, cupric"], ["formula", "Cu₂O", "CuO"],
                ["made by", "Fehling's + reducing sugar; 4Cu + O₂ above 1370 K", "2Cu + O₂ at red heat; heating Cu(NO₃)₂"],
                ["uses", "ruby glass, antifouling paint, rectifiers", "blue-green glass pigment, oxidant in C and H analysis"]]
        tb = C.table(rows, [2.0, 5.4, 5.4], row_h=0.75, size=23, colors=[th.MUTED, th.CORAL, th.INK]).move_to(UP * 0.4)
        sw = VGroup(Square(side_length=0.6, fill_color="#C0392B", fill_opacity=1, stroke_width=0), Square(side_length=0.6, fill_color="#1A1A1A", fill_opacity=1, stroke_color=th.MUTED, stroke_width=1)).arrange(RIGHT, buff=4.8).next_to(tb, UP, buff=0.2).shift(RIGHT * 1.0)
        with self.say("The two oxides of copper. Red oxide is copper one oxide, formed when Fehling's solution is reduced by a sugar, and used in ruby glass and antifouling paint for ships. Black oxide is copper two oxide, made by heating copper in air, used as a glass pigment and as the oxidant in organic analysis.") as v:
            self.play(FadeIn(sw))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(tb, sw)))
        head, prob = C.example_head(self, "An ore contains 20.0 % copper pyrite, CuFeS₂. How much copper can be recovered from 1.00 tonne at 90 % plant recovery? (Cu 63.5, Fe 56, S 32)")
        st = C.steps(r"M(\mathrm{CuFeS_2}) = 63.5 + 56 + 2(32) = 183.5",
                     r"\%\,\mathrm{Cu\ in\ mineral} = \tfrac{63.5}{183.5}\times100 = 34.60\,\%",
                     r"\mathrm{Cu\ in\ ore} = 0.200 \times 34.60\,\% = 6.92\,\% \Rightarrow 69.2\ \mathrm{kg\ per\ tonne}",
                     r"\text{at } 90\,\%:\ 0.90 \times 69.2 = 62.3\ \mathrm{kg}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example seven point one. Copper pyrite has molar mass one eighty three point five, so it is thirty four point six percent copper. The ore is only twenty percent pyrite, so it is six point nine two percent copper: sixty nine point two kilograms per tonne. At ninety percent recovery, sixty two point three kilograms."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        head, prob = C.example_head(self, "24.95 g of blue vitriol is heated to 100 °C, then 230 °C. Find the residue at each stage and the total water lost. (Cu 63.5, S 32, O 16, H 1)")
        st = C.steps(r"M = 63.5 + 32 + 64 + 90 = 249.5;\ \ n = \tfrac{24.95}{249.5} = 0.100\ \mathrm{mol}",
                     r"100^{\circ}\mathrm{C}:\ 0.100 \times 4 \times 18 = 7.2\ \mathrm{g\ lost} \Rightarrow 17.75\ \mathrm{g\ CuSO_4\cdot H_2O}",
                     r"230^{\circ}\mathrm{C}:\ 1.8\ \mathrm{g\ more} \Rightarrow 15.95\ \mathrm{g\ CuSO_4}\ \ (= 0.100 \times 159.5\ \checkmark)",
                     r"\text{total water} = 7.2 + 1.8 = 9.0\ \mathrm{g}", size=34).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example seven point two. Blue vitriol has molar mass two forty nine point five, so we have zero point one mole. At a hundred degrees, four waters per formula leave: seven point two grams, leaving seventeen point seven five grams. At two thirty the last water goes, one point eight grams more, leaving fifteen point nine five grams of white copper sulphate. Nine grams of water in total."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.quiz("Copper metal dissolves in a solution of",
                  ["dilute HCl", "dilute H₂SO₄", "FeCl₃", "ZnSO₄"], 2,
                  "Pause and think. Which of these solutions will dissolve copper metal?",
                  "C, iron three chloride. The iron three over iron two couple, plus zero point seven seven volts, lies above copper, so iron three ions oxidise copper. Dilute hydrochloric and sulphuric acids cannot, since copper is below hydrogen, and zinc ions are far too weak an oxidant.")

    # ------------------------------------------------------------------ part 2: zinc
    def p2(self):
        self.section(1)
        rows = [["Ore", "Formula"], ["zinc blende (chief ore)", "ZnS"], ["calamine", "ZnCO₃"], ["zincite", "ZnO"], ["willemite", "Zn₂SiO₄"]]
        tb = C.table(rows, [5.0, 3.0], row_h=0.66, size=28, colors=[th.INK, ZN]).move_to(UP * 0.6)
        with self.say("Zinc is the metal that protects other metals. The Ganesh Himal lead zinc deposit in Dhading is Nepal's best known metal prospect. The chief ore is zinc blende, zinc sulphide. Others are calamine, zincite and willemite.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.45)
                self.hold(v.dur / 5 - 0.45)
        self.play(FadeOut(tb))
        boxes, arrows = flow(["froth flotation", "roasting", "reduction with coke", "condense the vapour", "refining"])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in boxes], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.5)
        light(self, boxes, 1)
        e = eqs(r"2ZnS + 3O_2 \rightarrow 2ZnO + 2SO_2\uparrow", r"ZnCO_3 \rightarrow ZnO + CO_2\ \ (\text{calcination of calamine})")
        n = T("the SO₂ goes to a contact plant to make sulphuric acid", size=24, color=th.AMBER).next_to(e, DOWN, buff=0.35)
        with self.say("Blende is a sulphide, so it too is concentrated by froth flotation. It is then roasted in air at about twelve hundred kelvin to zinc oxide. Calamine is simply calcined. The sulphur dioxide is not wasted: it goes to make sulphuric acid."):
            self.play(FadeIn(e))
            self.play(FadeIn(n))
        self.play(FadeOut(VGroup(e, n)))
        light(self, boxes, 2)
        ret = RoundedRectangle(corner_radius=0.3, width=3.4, height=1.4, fill_color="#5A4A3A", fill_opacity=1, stroke_color=th.INK, stroke_width=3).move_to([-3.4, -0.6, 0])
        rl = T("fireclay retort, 1673 K", size=20, color=th.BODY).next_to(ret, DOWN, buff=0.15)
        charge = T("ZnO + C", size=26, color=WHITE, weight="BOLD").move_to(ret)
        pipe = Line(ret.get_right(), [1.2, -0.6, 0], color=th.INK, stroke_width=8)
        cond = RoundedRectangle(corner_radius=0.2, width=1.6, height=1.8, stroke_color=th.SKY, stroke_width=3).move_to([2.2, -1.0, 0])
        cl = T("condenser", size=20, color=th.SKY).next_to(cond, DOWN, buff=0.15)
        key = chem(r"ZnO + C \rightarrow Zn + CO\uparrow", size=44, color=th.AMBER).move_to([0, 1.0, 0])
        bt = ValueTracker(0)
        vap = always_redraw(lambda: VGroup(*[Dot([-1.6 + ((bt.get_value() + k / 6) % 1) * 3.4, -0.6 + 0.08 * np.sin(9 * k + 6 * bt.get_value()), 0], radius=0.07, color=ZN) for k in range(6)]))
        pool = Rectangle(width=1.5, height=0.01, fill_color=ZN, fill_opacity=1, stroke_width=0).move_to([2.2, -1.85, 0], aligned_edge=DOWN)
        with self.say("The oxide is reduced with coke in fireclay retorts at about sixteen seventy kelvin. At that temperature zinc, which boils at nine hundred and seven degrees, comes off as a vapour. It is led into condensers and collects as liquid zinc. This is why zinc was isolated so late in history: cool the vapour in air, and it simply burns back to oxide."):
            self.play(Write(key))
            self.play(FadeIn(ret), FadeIn(charge), FadeIn(rl), Create(pipe), Create(cond), FadeIn(cl))
            self.add(vap, pool)
            self.play(bt.animate.set_value(3), pool.animate.stretch_to_fit_height(0.7).align_to(cond, DOWN).shift(UP * 0.05), run_time=4, rate_func=linear)
        sp = T("crude metal: spelter, 97–98 %; first condensate: zinc dust", size=24, color=ZN).to_edge(DOWN, buff=0.45)
        with self.say("The crude metal is called spelter. The fine powder that condenses first is zinc dust. Spelter is refined by liquation, by fractional distillation, or electrolytically to ninety nine point nine five percent."):
            light(self, boxes, 4)
            self.play(FadeIn(sp))
        self.play(FadeOut(VGroup(boxes, arrows, ret, rl, charge, pipe, cond, cl, key, pool, sp)), FadeOut(vap))
        self.remove(vap)
        care = self.callout("careful", "Roast, then reduce. Carbon cannot reduce a sulphide: every sulphide ore is first roasted to the oxide. Copper is the only apparent exception, and there the reductant is its own sulphide (auto-reduction).", width=11, size=27)
        with self.say("A careful point. Carbon will not reduce a sulphide. Every sulphide ore is first roasted to the oxide, and then reduced. Copper only looks like an exception, because there the reducing agent is the ore's own sulphide."):
            self.play(FadeIn(care, shift=UP * 0.3))
        self.play(FadeOut(care))
        self.zn_properties()
        self.white_vitriol()

    def zn_properties(self):
        title = T("Zinc is amphoteric", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        t1 = tube([-3.2, -0.6, 0], color=th.CORAL, opacity=0.25)
        t2 = tube([3.2, -0.6, 0], color=th.SKY, opacity=0.25)
        z1 = Square(side_length=0.25, fill_color=ZN, fill_opacity=1, stroke_width=0).move_to([-3.2, -1.25, 0])
        z2 = Square(side_length=0.25, fill_color=ZN, fill_opacity=1, stroke_width=0).move_to([3.2, -1.25, 0])
        l1 = T("dilute HCl", size=24, color=th.CORAL, weight="BOLD").next_to(t1, UP, buff=0.2)
        l2 = T("hot NaOH(aq)", size=24, color=th.SKY, weight="BOLD").next_to(t2, UP, buff=0.2)
        e1 = chem(r"Zn + 2HCl \rightarrow ZnCl_2 + H_2\uparrow", size=36).next_to(t1, DOWN, buff=0.3)
        e2 = chem(r"Zn + 2NaOH + 2H_2O \rightarrow Na_2[Zn(OH)_4] + H_2\uparrow", size=32).next_to(t2, DOWN, buff=0.3)
        bt = ValueTracker(0)
        bub = always_redraw(lambda: VGroup(*[Circle(radius=0.05, stroke_color=WHITE, stroke_width=2).move_to([x + 0.1 * np.sin(5 * k), -1.1 + ((bt.get_value() + k / 5) % 1) * 1.0, 0]) for x in (-3.2, 3.2) for k in range(5)]))
        with self.say("Zinc is a bluish white metal, brittle when cold, malleable between one hundred and one hundred and fifty degrees, so zinc sheet is rolled hot. Its most asked property: it dissolves in acids and in alkalis, both with hydrogen. In hydrochloric acid it gives zinc chloride. In hot sodium hydroxide it gives sodium zincate. Zinc is amphoteric."):
            self.play(FadeIn(title), FadeIn(t1), FadeIn(t2), FadeIn(z1), FadeIn(z2), FadeIn(l1), FadeIn(l2))
            self.add(bub)
            self.play(bt.animate.set_value(3), Write(e1), Write(e2), run_time=4, rate_func=linear)
        self.play(FadeOut(VGroup(title, t1, t2, z1, z2, l1, l2, e1, e2)), FadeOut(bub))
        self.remove(bub)
        rows = [["Reagent", "Reaction"], ["air, strong heat", "2Zn + O₂ → 2ZnO (white 'philosopher's wool')"], ["dilute H₂SO₄", "Zn + H₂SO₄ → ZnSO₄ + H₂"],
                ["hot conc. H₂SO₄", "Zn + 2H₂SO₄ → ZnSO₄ + SO₂ + 2H₂O"], ["very dilute HNO₃", "4Zn + 10HNO₃ → 4Zn(NO₃)₂ + NH₄NO₃ + 3H₂O"],
                ["CuSO₄(aq)", "Zn + CuSO₄ → ZnSO₄ + Cu"], ["NaOH + NaNO₃", "4Zn + 7NaOH + NaNO₃ → 4Na₂ZnO₂ + NH₃ + 2H₂O"]]
        tb = C.table(rows, [3.4, 9.0], row_h=0.62, size=23, colors=[th.AMBER, th.BODY]).move_to(UP * 0.4)
        with self.say("More reactions. Burnt in air it gives white zinc oxide smoke, philosopher's wool. With dilute sulphuric acid, hydrogen. Hot concentrated sulphuric acid gives sulphur dioxide, and very dilute nitric acid is reduced all the way to ammonium nitrate. Zinc at minus zero point seven six volts displaces most metals. And in alkali it reduces nitrate to ammonia, a test for nitrate.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))
        uses = VGroup(*[C.card(self, a, b, w=3.9, h=1.9, color=c, tsize=24, bsize=20) for a, b, c in [
            ("Galvanising", "iron sheet, pipes, nails: the biggest use", ZN), ("Alloys", "brass, German silver, solders", th.AMBER), ("Dry cells", "the negative zinc can", th.SKY),
            ("Reducing agent", "zinc dust; Zn–Hg amalgam", th.MINT), ("Sacrificial anodes", "ships, pipelines, water heaters", th.CORAL), ("ZnO, ZnSO₄", "paint, rubber, calamine lotion, fertiliser", th.LIME)]]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25))
        with self.say("Uses: galvanising above all, alloys like brass, the can of the dry cell, zinc dust as a reducing agent, sacrificial anodes, and zinc compounds in paint, rubber, calamine lotion and fertiliser for zinc deficient paddy soils.") as v:
            for c in uses:
                self.play(FadeIn(c, shift=UP * 0.15), run_time=0.4)
                self.hold(v.dur / 6 - 0.45)
        self.play(FadeOut(uses))

    def white_vitriol(self):
        title = T("White vitriol, ZnSO₄·7H₂O", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        prep = VGroup(chem(r"Zn + H_2SO_4 \rightarrow ZnSO_4 + H_2\uparrow", size=32), chem(r"ZnO + H_2SO_4 \rightarrow ZnSO_4 + H_2O", size=32)).arrange(DOWN, buff=0.25).next_to(title, DOWN, buff=0.4)
        cr = T("crystallise below 30 °C (above it the hexahydrate forms)", size=24, color=th.AMBER).next_to(prep, DOWN, buff=0.3)
        heat = VGroup(chem(r"ZnSO_4\cdot 7H_2O \xrightarrow{100^{\circ}C} ZnSO_4\cdot H_2O + 6H_2O", size=30), chem(r"ZnSO_4\cdot H_2O \xrightarrow{450^{\circ}C} ZnSO_4 + H_2O", size=30),
                      chem(r"2ZnSO_4 \xrightarrow{\text{red heat}} 2ZnO + 2SO_2 + O_2", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cr, DOWN, buff=0.5)
        with self.say("White vitriol is zinc sulphate heptahydrate. Dissolve zinc, its oxide or carbonate in dilute sulphuric acid, and crystallise below thirty degrees, or a lower hydrate forms. On heating, six waters go at a hundred degrees, the last at four hundred and fifty, and at red heat it breaks down to zinc oxide, sulphur dioxide and oxygen."):
            self.play(FadeIn(title), Write(prep))
            self.play(FadeIn(cr))
            self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.2) for h in heat], lag_ratio=0.4))
        self.play(FadeOut(VGroup(prep, cr, heat)))
        t1 = tube([-3.2, -0.8, 0], color="#E6E9F2", opacity=0.15)
        t2 = tube([3.2, -0.8, 0], color="#E6E9F2", opacity=0.15)
        l1 = T("+ NaOH", size=24, color=th.AMBER, weight="BOLD").next_to(t1, UP, buff=0.2)
        l2 = T("+ NH₃(aq)", size=24, color=th.AMBER, weight="BOLD").next_to(t2, UP, buff=0.2)
        p1 = ppt_in(t1, WHITE, seed=4)
        p2 = ppt_in(t2, WHITE, seed=5)
        e1 = VGroup(chem(r"Zn(OH)_2\downarrow\ \text{white}", size=34), chem(r"\xrightarrow{\text{excess}} Na_2[Zn(OH)_4]", size=34)).arrange(DOWN, buff=0.12).next_to(t1, DOWN, buff=0.25)
        e2 = VGroup(chem(r"Zn(OH)_2\downarrow\ \text{white}", size=34), chem(r"\xrightarrow{\text{excess}} [Zn(NH_3)_4](OH)_2", size=34)).arrange(DOWN, buff=0.12).next_to(t2, DOWN, buff=0.25)
        with self.say("Its solution gives the classic test for zinc. Add sodium hydroxide: a white precipitate of zinc hydroxide. Add excess, and it dissolves as zincate. Ammonia does the same: white precipitate, then a colourless tetrammine complex in excess. Aluminium dissolves in excess sodium hydroxide but not in ammonia, and magnesium in neither. That is how you tell them apart."):
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(l1), FadeIn(l2))
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(e1[0]), FadeIn(e2[0]))
            self.play(FadeOut(p1, scale=0.3), FadeOut(p2, scale=0.3), FadeIn(e1[1]), FadeIn(e2[1]), run_time=1.5)
        self.play(FadeOut(VGroup(title, t1, t2, l1, l2, e1, e2)))
        more = VGroup(T("H₂S in alkaline solution: white ZnS", size=26, color=th.BODY), T("BaCl₂: white BaSO₄, insoluble in acid", size=26, color=th.BODY),
                      T("K₄[Fe(CN)₆]: white Zn₂[Fe(CN)₆]", size=26, color=th.BODY),
                      T("Uses: lithopone (ZnS + BaSO₄) white pigment, eye lotion, mordant, zinc fertiliser", size=24, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        with self.say("Hydrogen sulphide in alkaline solution gives white zinc sulphide, barium chloride gives white barium sulphate, and ferrocyanide a white precipitate. White vitriol is used to make lithopone, a white pigment that does not blacken in polluted air, as an eye lotion, a mordant and a zinc fertiliser."):
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in more], lag_ratio=0.4))
        self.play(FadeOut(more))
        head, prob = C.example_head(self, "194.8 g of pure zinc blende is roasted completely, and the ZnO is reduced by coke. Find (a) the volume of SO₂ at STP, (b) the mass of zinc. (Zn 65.4, S 32)")
        st = C.steps(r"n(\mathrm{ZnS}) = \tfrac{194.8}{97.4} = 2.00\ \mathrm{mol}",
                     r"2\mathrm{ZnS} \rightarrow 2\mathrm{SO_2}:\ V = 2.00 \times 22.4 = 44.8\ \mathrm{L}",
                     r"\mathrm{ZnO} \rightarrow \mathrm{Zn}:\ m = 2.00 \times 65.4 = 130.8\ \mathrm{g}", size=40).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example seven point three. Zinc sulphide has molar mass ninety seven point four, so we have two moles. Each zinc sulphide gives one sulphur dioxide: two moles, forty four point eight litres at S T P. And each gives one zinc: two times sixty five point four, one hundred and thirty point eight grams."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 3: mercury
    def p3(self):
        self.section(2)
        drop = VGroup(Circle(radius=0.9, fill_color=HG, fill_opacity=1, stroke_color=WHITE, stroke_width=2), Circle(radius=0.3, fill_color=WHITE, fill_opacity=0.6, stroke_width=0).shift(UL * 0.35)).move_to([-5.0, 0.2, 0])
        facts = VGroup(T("the only metal liquid at room temperature", size=26, color=th.INK), T("m.p. −38.9 °C, b.p. 356.6 °C, density 13.6 g cm⁻³", size=24, color=th.BODY),
                       para("a cumulative nerve poison: thermometers withdrawn under the Minamata Convention", width=8.0, size=26, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([1.4, 0.2, 0])
        with self.say("Mercury is the only metal that is liquid at room temperature, and the only one on our list that is a cumulative poison: its vapour damages the nervous system. That is why mercury thermometers are being withdrawn from Nepali hospitals under the Minamata Convention."):
            self.play(GrowFromCenter(drop))
            self.play(LaggedStart(*[FadeIn(f, shift=LEFT * 0.2) for f in facts], lag_ratio=0.4))
        self.play(FadeOut(VGroup(drop, facts)))
        title = T("Extraction from cinnabar, HgS", size=32, color="#E0453A", weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e = eqs(r"HgS + O_2 \rightarrow Hg + SO_2\uparrow", r"(2HgS + 3O_2 \rightarrow 2HgO + 2SO_2,\ \ 2HgO \rightarrow 2Hg + O_2)", y=1.4)
        e[0].set_color(th.AMBER).scale(1.3)
        why = T("no reducing agent needed: HgO falls apart on heating", size=26, color=th.AMBER).next_to(e, DOWN, buff=0.35)
        steps_ = VGroup(T("1. concentrate by froth flotation", size=24, color=th.BODY), T("2. roast in air at 700–800 K: that is the extraction", size=24, color=th.BODY),
                        T("3. condense the vapour in water-cooled condensers", size=24, color=th.BODY),
                        T("4. purify: spray down dilute HNO₃ (base metals dissolve), then vacuum distil", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(why, DOWN, buff=0.45)
        with self.say("Its ore is bright red cinnabar, mercury sulphide. Extraction is the easiest in the syllabus. Roast it in air at seven to eight hundred kelvin, and mercury comes straight off as vapour. Even if mercury oxide forms first, it decomposes on heating, which is exactly how Priestley discovered oxygen. So no reducing agent is needed."):
            self.play(FadeIn(title), Write(e[0]))
            self.play(FadeIn(e[1]), FadeIn(why))
        with self.say("The vapour is condensed in water cooled condensers. To purify it, the crude metal is sprayed down a tall column of dilute nitric acid, which dissolves base metals but not noble mercury, and then distilled under reduced pressure."):
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in steps_], lag_ratio=0.4))
        self.play(FadeOut(VGroup(title, e, why, steps_)))
        key = self.callout("key", "Excess mercury gives the mercurous Hg₂²⁺ salt; excess acid or halogen gives the mercuric Hg²⁺ salt. Hg₂²⁺ always contains an Hg–Hg bond, so never write Hg⁺.", width=11.5, size=27).to_edge(UP, buff=0.8)
        pairs = VGroup(
            VGroup(chem(r"2Hg + Cl_2 \rightarrow Hg_2Cl_2", size=36), T("limited Cl₂", size=20, color=th.MUTED)).arrange(DOWN, buff=0.1),
            VGroup(chem(r"Hg + Cl_2 \rightarrow HgCl_2", size=36), T("excess Cl₂", size=20, color=th.MUTED)).arrange(DOWN, buff=0.1),
            VGroup(chem(r"6Hg + 8HNO_3 \rightarrow 3Hg_2(NO_3)_2 + 2NO + 4H_2O", size=32), T("excess Hg, cold dilute acid", size=20, color=th.MUTED)).arrange(DOWN, buff=0.1),
            VGroup(chem(r"Hg + 4HNO_3 \rightarrow Hg(NO_3)_2 + 2NO_2 + 2H_2O", size=32), T("excess hot conc. acid", size=20, color=th.MUTED)).arrange(DOWN, buff=0.1),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.4)).next_to(key, DOWN, buff=0.45)
        with self.say("Mercury follows one rule. Excess mercury gives the mercurous salt, mercury one, which is really a pair of mercury atoms bonded together. Excess acid or halogen gives the mercuric salt, mercury two. So limited chlorine gives calomel, excess chlorine gives mercuric chloride. Cold dilute nitric acid with excess mercury gives mercurous nitrate, hot concentrated acid gives mercuric nitrate. Dilute hydrochloric and sulphuric acids do nothing."):
            self.play(FadeIn(key, shift=DOWN * 0.2))
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in pairs], lag_ratio=0.3), run_time=2)
        self.play(FadeOut(VGroup(key, pairs)))
        am = para("Amalgams: mercury dissolves most metals (sodium amalgam, zinc amalgam, dental Ag–Sn–Hg) but not iron or platinum, so it is shipped in iron bottles. Spilt mercury is dusted with sulphur: Hg + S → HgS, a non-volatile solid.", width=11.5, size=28, color=th.BODY)
        with self.say("Mercury dissolves most metals to form amalgams, like sodium amalgam and dental amalgam, but not iron or platinum, so it is transported in iron bottles. A spill is dusted with sulphur, which forms solid, non volatile mercury sulphide that can be swept up safely."):
            self.play(FadeIn(am))
        self.play(FadeOut(am))
        self.calomel_sublimate()

    def calomel_sublimate(self):
        h1 = VGroup(T("Calomel", size=34, color=th.SKY, weight="BOLD"), chem(r"Hg_2Cl_2", size=40, color=th.SKY), T("mercury(I) chloride", size=22, color=th.MUTED)).arrange(DOWN, buff=0.12).move_to([-3.4, 2.1, 0])
        h2 = VGroup(T("Corrosive sublimate", size=34, color=th.CORAL, weight="BOLD"), chem(r"HgCl_2", size=40, color=th.CORAL), T("mercury(II) chloride", size=22, color=th.MUTED)).arrange(DOWN, buff=0.12).move_to([3.4, 2.1, 0])
        p1 = VGroup(chem(r"Hg_2(NO_3)_2 + 2NaCl \rightarrow Hg_2Cl_2\downarrow + 2NaNO_3", size=30), chem(r"HgCl_2 + Hg \rightarrow Hg_2Cl_2", size=30),
                    para("white, insoluble, tasteless, non-poisonous", width=5.6, size=24, color=th.BODY, align="center")).arrange(DOWN, buff=0.18).move_to([-3.4, 0.2, 0])
        p2 = VGroup(chem(r"Hg + Cl_2 \rightarrow HgCl_2\ (\text{excess } Cl_2)", size=30), chem(r"HgSO_4 + 2NaCl \rightarrow HgCl_2\uparrow + Na_2SO_4", size=30),
                    para("white, soluble, covalent Cl–Hg–Cl, deadly poison", width=5.6, size=24, color=th.BODY, align="center")).arrange(DOWN, buff=0.18).move_to([3.4, 0.2, 0])
        for p_ in (p1, p2):
            p_.scale_to_fit_width(min(p_.width, 6.2))
        div = DashedLine([0, 2.8, 0], [0, -2.9, 0], color=th.FAINT)
        with self.say("Mercury's two chlorides are opposites in almost every way. Calomel, mercury one chloride, is made by precipitation from mercurous nitrate, or by grinding mercuric chloride with mercury. It is white, insoluble, tasteless and non poisonous. Corrosive sublimate, mercury two chloride, is made from mercury and excess chlorine, or by heating mercuric sulphate with salt. It is soluble, covalent, and a violent poison, as its name warns."):
            self.play(Create(div), FadeIn(h1), FadeIn(h2))
            self.play(FadeIn(p1, shift=UP * 0.2))
            self.play(FadeIn(p2, shift=UP * 0.2))
        self.play(FadeOut(VGroup(p1, p2)))
        t1 = tube([-3.4, -0.8, 0], color="#E6E9F2", opacity=0.1)
        w1 = ppt_in(t1, WHITE, seed=7)
        b1 = ppt_in(t1, "#202020", seed=8)
        l1 = VGroup(T("+ NH₃", size=26, color=th.AMBER, weight="BOLD"), chem(r"Hg_2Cl_2 + 2NH_3 \rightarrow Hg(NH_2)Cl + Hg + NH_4Cl", size=28), T("turns BLACK (free Hg): 'kalos melas'", size=24, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(t1, DOWN, buff=0.2)
        t2 = tube([3.4, -0.8, 0], color="#E6E9F2", opacity=0.1)
        w2 = ppt_in(t2, WHITE, seed=9)
        g2 = ppt_in(t2, "#6A6F7A", seed=10)
        l2 = VGroup(T("+ SnCl₂, then more", size=26, color=th.AMBER, weight="BOLD"), T("white Hg₂Cl₂ → grey mercury", size=24, color=th.BODY), T("proves a mercuric salt", size=24, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(t2, DOWN, buff=0.2)
        with self.say("Their key tests. Ammonia turns calomel black, because finely divided mercury forms. The name calomel comes from the Greek for beautiful black. With corrosive sublimate, tin two chloride first gives a white precipitate of calomel, and more tin chloride turns it grey as free mercury is formed. That two stage change proves a mercuric salt."):
            self.play(FadeIn(t1), FadeIn(w1))
            self.play(FadeIn(l1), FadeTransform(w1, b1), run_time=1.5)
            self.play(FadeIn(t2), FadeIn(w2))
            self.play(FadeIn(l2), FadeTransform(w2, g2), run_time=1.5)
        self.play(FadeOut(VGroup(t1, b1, l1, t2, g2, l2)))
        rows = [["HgCl₂ +", "Observation"], ["NaOH", "yellow HgO"], ["NH₃", "white Hg(NH₂)Cl ('infusible white ppt')"], ["KI, limited", "scarlet HgI₂"],
                ["KI, excess", "dissolves: K₂[HgI₄], Nessler's reagent (test for NH₄⁺)"]]
        tb = C.table(rows, [2.6, 8.2], row_h=0.6, size=23, colors=[th.AMBER, th.BODY]).move_to([0, -0.6, 0])
        uses = T("Uses: calomel electrode (pH meters); HgCl₂ as antiseptic, timber preservative, catalyst", size=22, color=th.MUTED).to_edge(DOWN, buff=0.4)
        with self.say("Corrosive sublimate also gives yellow mercury oxide with alkali, a white precipitate with ammonia, and scarlet mercury iodide with a little potassium iodide, which dissolves in excess to form Nessler's reagent, the test for ammonium ions in drinking water. Calomel is used in the calomel reference electrode, corrosive sublimate as an antiseptic and preservative.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
            self.play(FadeIn(uses))
        self.play(FadeOut(VGroup(h1, h2, div, tb, uses)))
        self.quiz("When ammonia is added to calomel, Hg₂Cl₂, the solid turns",
                  ["yellow", "scarlet", "black", "deep blue"], 2,
                  "Pause and think. What colour does calomel turn with ammonia?",
                  "C, black. Calomel disproportionates: one mercury becomes the white amido compound, the other becomes free, finely divided mercury, which looks black. Scarlet is mercury two iodide, and yellow is mercury two oxide.")

    # ------------------------------------------------------------------ part 4: iron
    def p4(self):
        self.section(3)
        rows = [["Ore", "Formula", "% Fe"], ["haematite (chief ore)", "Fe₂O₃", "70"], ["magnetite", "Fe₃O₄", "72"], ["siderite", "FeCO₃", "48"],
                ["limonite", "Fe₂O₃·3H₂O", "60"], ["iron pyrite (not used for iron)", "FeS₂", "47"]]
        tb = C.table(rows, [5.4, 3.4, 1.8], row_h=0.62, size=26, colors=[th.INK, RUST, th.AMBER]).move_to(UP * 0.5)
        with self.say("Iron is the working metal of the modern world. Nepal's Dhaubadi deposit in Nawalparasi is the basis of its first planned iron and steel plant. The chief ore is red haematite. Magnetite is the richest. Iron pyrite is never used for iron, because its sulphur makes the metal brittle when hot.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        n = T("concentrate (washing; magnetic separation) → calcine and roast → smelt in the blast furnace", size=22, color=th.AMBER).next_to(tb, DOWN, buff=0.4)
        self.play(FadeIn(n))
        self.wait(0.8)
        self.play(FadeOut(VGroup(tb, n)))
        self.blast_furnace()
        self.fe_properties()
        self.steel()
        self.corrosion()

    def blast_furnace(self):
        cx = -3.4
        shell = Polygon([cx - 1.0, 2.8, 0], [cx + 1.0, 2.8, 0], [cx + 1.8, 0.3, 0], [cx + 1.4, -2.4, 0], [cx - 1.4, -2.4, 0], [cx - 1.8, 0.3, 0],
                        fill_color="#2A2F45", fill_opacity=1, stroke_color=th.INK, stroke_width=3)
        zones = [(2.3, 1.1, "700–900 K", "reduction", th.SKY), (1.1, -0.3, "1200 K", "slag formation", th.AMBER), (-0.3, -1.3, "1500 K", "fusion", th.CORAL), (-1.3, -2.4, "1900 K", "combustion", "#FF5A3A")]
        bands = VGroup()
        for y1, y2, temp, name, col in zones:
            r = Rectangle(width=3.4, height=y1 - y2, fill_color=col, fill_opacity=0.18, stroke_width=0).move_to([cx, (y1 + y2) / 2, 0])
            bands.add(VGroup(r, T(temp, size=18, color=col).move_to([cx, (y1 + y2) / 2, 0])))
        bands.set_z_index(1)
        tuy = VGroup(Arrow([cx - 2.8, -1.8, 0], [cx - 1.5, -1.8, 0], buff=0, color=th.SKY, stroke_width=4), Arrow([cx + 2.8, -1.8, 0], [cx + 1.5, -1.8, 0], buff=0, color=th.SKY, stroke_width=4))
        tl = T("hot air blast (tuyères)", size=18, color=th.SKY).next_to(tuy[0], DOWN, buff=0.1).shift(RIGHT * 0.4)
        top = T("ore + coke + limestone (8 : 4 : 1)", size=20, color=th.BODY).next_to(shell, UP, buff=0.1)
        tt = ValueTracker(0)
        rng = np.random.default_rng(6)
        seeds = [(rng.uniform(-0.8, 0.8), rng.uniform(0, 1)) for _ in range(14)]

        def charge():
            g = VGroup()
            for dx, ph in seeds:
                f = (tt.get_value() * 0.25 + ph) % 1
                g.add(Dot([cx + dx * (1 + 0.6 * f), 2.6 - 4.7 * f, 0], radius=0.07, color=[RUST, "#333", "#DDD"][int(ph * 3) % 3]))
            return g
        ch = always_redraw(charge)
        iron = Rectangle(width=2.6, height=0.3, fill_color="#FF7A2A", fill_opacity=0.9, stroke_width=0).move_to([cx, -2.2, 0])
        slag = Rectangle(width=2.6, height=0.2, fill_color="#C9C2A8", fill_opacity=0.9, stroke_width=0).next_to(iron, UP, buff=0)
        with self.say("The blast furnace. Roasted ore, coke and limestone go in at the top, roughly eight to four to one. A blast of hot air enters near the bottom through the tuyeres. The charge sinks slowly through four zones, hottest at the bottom."):
            self.play(DrawBorderThenFill(shell), FadeIn(top))
            self.play(FadeIn(bands), GrowArrow(tuy[0]), GrowArrow(tuy[1]), FadeIn(tl))
            self.add(ch)
            self.play(tt.animate.set_value(4), run_time=4, rate_func=linear)
        eqs_ = [
            ("combustion, bottom, 1900 K", [r"C + O_2 \rightarrow CO_2", r"CO_2 + C \rightarrow 2CO"], "#FF5A3A",
             "At the bottom, coke burns in the blast to carbon dioxide, which meets more hot coke and becomes carbon monoxide, the real reducing agent."),
            ("reduction, top, 700–900 K", [r"3Fe_2O_3 + CO \rightarrow 2Fe_3O_4 + CO_2", r"Fe_3O_4 + CO \rightarrow 3FeO + CO_2", r"FeO + CO \rightarrow Fe + CO_2"], th.SKY,
             "Carbon monoxide rises. Near the top it reduces haematite step by step, to magnetite, to iron two oxide, and finally to spongy iron."),
            ("slag formation, 1200 K", [r"CaCO_3 \rightarrow CaO + CO_2", r"CaO + SiO_2 \rightarrow CaSiO_3\ (\text{slag})"], th.AMBER,
             "Lower down, limestone decomposes to quicklime, which combines with the sandy gangue to form a fusible slag of calcium silicate."),
            ("fusion, 1500 K", [r"FeO + C \rightarrow Fe + CO", r"\text{iron melts, dissolves carbon}"], th.CORAL,
             "In the fusion zone, any remaining oxide is reduced by carbon, and the iron melts and dissolves carbon. Molten iron collects at the hearth, with lighter slag floating on top."),
        ]
        panel = VGroup()
        for name, tex, col, narr in eqs_:
            g = VGroup(T(name, size=24, color=col, weight="BOLD"), *[chem(t_, size=30) for t_ in tex]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            panel.add(g)
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.9, 0.1, 0])
        if panel.height > 6.0:
            panel.scale_to_fit_height(6.0)
        with self.say("At the bottom, coke burns in the blast to carbon dioxide, which meets more hot coke and becomes carbon monoxide, the real reducing agent."):
            self.play(FadeIn(panel[0], shift=LEFT * 0.2), Indicate(bands[3], color="#FF5A3A", scale_factor=1.02), tt.animate.set_value(6), run_time=2.5, rate_func=linear)
        with self.say("Carbon monoxide rises. Near the top it reduces haematite step by step, to magnetite, to iron two oxide, and finally to spongy iron."):
            self.play(FadeIn(panel[1], shift=LEFT * 0.2), Indicate(bands[0], color=th.SKY, scale_factor=1.02), tt.animate.set_value(8), run_time=2.5, rate_func=linear)
        with self.say("Lower down, limestone decomposes to quicklime, which combines with the sandy gangue to form a fusible slag of calcium silicate."):
            self.play(FadeIn(panel[2], shift=LEFT * 0.2), Indicate(bands[1], color=th.AMBER, scale_factor=1.02), tt.animate.set_value(10), run_time=2.5, rate_func=linear)
        with self.say("In the fusion zone, any remaining oxide is reduced by carbon, and the iron melts and dissolves carbon. Molten iron collects at the hearth, with lighter slag floating on top."):
            self.play(FadeIn(panel[3], shift=LEFT * 0.2), FadeIn(iron), FadeIn(slag), tt.animate.set_value(12), run_time=2.5, rate_func=linear)
        pig = T("pig iron: about 4 % carbon, plus Si, Mn, P, S", size=24, color=th.AMBER).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.6)
        with self.say("The product, pig iron, holds about four percent carbon, with silicon, manganese, phosphorus and sulphur. Remelted with scrap, it becomes cast iron."):
            self.play(FadeIn(pig), tt.animate.set_value(14), run_time=2, rate_func=linear)
        self.play(FadeOut(VGroup(shell, top, bands, tuy, tl, panel, iron, slag, pig)), FadeOut(ch))
        self.remove(ch)

    def fe_properties(self):
        rows = [["Reagent", "Reaction"], ["moist air", "rusting: Fe₂O₃·xH₂O"], ["steam, red heat", "3Fe + 4H₂O ⇌ Fe₃O₄ + 4H₂"], ["dilute HCl / H₂SO₄", "Fe + 2HCl → FeCl₂ + H₂ (iron(II))"],
                ["hot conc. H₂SO₄", "2Fe + 6H₂SO₄ → Fe₂(SO₄)₃ + 3SO₂ + 6H₂O"], ["conc. HNO₃", "passivity: a thin oxide film stops attack"], ["Cl₂, heated", "2Fe + 3Cl₂ → 2FeCl₃ (iron(III))"],
                ["NaOH(aq)", "no action: iron is not amphoteric"]]
        tb = C.table(rows, [3.6, 8.4], row_h=0.6, size=23, colors=[th.AMBER, th.BODY]).move_to(UP * 0.5)
        with self.say("Pure iron is a soft, silvery, strongly magnetic metal. Dilute acids give iron two salts with hydrogen. Strong oxidisers, chlorine and hot concentrated sulphuric acid, give iron three. Concentrated nitric acid makes it passive: a thin oxide film stops all further attack. And unlike zinc, iron does not react with alkali.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 8 - 0.35)
        self.play(FadeOut(tb))
        rows = [["Variety", "Carbon", "Properties and uses"], ["cast / pig iron", "2.5–4.5 %", "hard, brittle; pipes, manhole covers, engine blocks"],
                ["wrought iron", "< 0.25 %", "purest, soft, weldable; chains, gates, magnet cores"], ["steel", "0.25–1.5 %", "hard AND tough; rods, rails, tools, vehicles"]]
        tb = C.table(rows, [3.2, 2.4, 7.0], row_h=0.72, size=24, colors=[th.INK, th.AMBER, th.BODY]).move_to(UP * 0.3)
        with self.say("Carbon content decides the variety. Cast iron, two and a half to four and a half percent, is hard but brittle. Wrought iron, below a quarter of a percent, is soft and weldable. In between, steel is both hard and tough."):
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.45)
        self.play(FadeOut(tb))

    def steel(self):
        title = T("Steel by the Basic Oxygen Process", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        cx = -3.6
        conv = Polygon([cx - 0.7, 1.3, 0], [cx + 0.7, 1.3, 0], [cx + 1.5, -0.1, 0], [cx + 1.5, -2.6, 0], [cx - 1.5, -2.6, 0], [cx - 1.5, -0.1, 0],
                       fill_color="#3A3F55", fill_opacity=1, stroke_color="#B9A88A", stroke_width=8)
        melt = Rectangle(width=2.8, height=1.3, fill_color="#FF7A2A", fill_opacity=0.9, stroke_width=0).move_to([cx, -1.9, 0])
        lance = Rectangle(width=0.16, height=2.6, fill_color=th.SKY, fill_opacity=1, stroke_width=0).move_to([cx, 1.2, 0])
        ll = T("O₂ lance, 10 atm", size=22, color=th.SKY).next_to(lance, RIGHT, buff=0.3).shift(UP * 0.6)
        lin = T("basic lining: dolomite CaO·MgO", size=20, color="#B9A88A").next_to(conv, DOWN, buff=0.15)
        bt = ValueTracker(0)
        flame = always_redraw(lambda: Polygon([cx - 0.5, 1.3, 0], [cx + 0.5, 1.3, 0], [cx + 0.1 * np.sin(8 * bt.get_value()), 2.2 + 0.2 * np.sin(5 * bt.get_value()), 0], fill_color=th.AMBER, fill_opacity=0.8, stroke_width=0))
        rows = [["Impurity", "Removed as"], ["C", "2C + O₂ → 2CO (burns at the mouth)"], ["Si", "SiO₂ + CaO → CaSiO₃ (slag)"], ["Mn", "MnO + SiO₂ → MnSiO₃ (slag)"],
                ["P", "P₂O₅ + 3CaO → Ca₃(PO₄)₂ (slag: fertiliser)"], ["S", "SO₂ gas"]]
        tb = C.table(rows, [1.8, 6.4], row_h=0.58, size=22, colors=[th.AMBER, th.BODY]).move_to([2.6, -0.2, 0])
        with self.say("Steel is iron with its carbon cut to between a quarter and one and a half percent, and the silicon, manganese, phosphorus and sulphur removed. Most of the world's steel is made by the basic oxygen process. Molten pig iron, scrap and quicklime go into a pear shaped converter with a basic lining of dolomite. A water cooled lance blows pure oxygen onto the melt."):
            self.play(FadeIn(title), DrawBorderThenFill(conv), FadeIn(melt), FadeIn(lin))
            self.play(FadeIn(lance), FadeIn(ll), lance.animate.shift(DOWN * 0.8))
            self.add(flame)
            self.play(FadeIn(flame), bt.animate.set_value(3), run_time=2.5, rate_func=linear)
        with self.say("The impurities burn. Carbon leaves as carbon monoxide, flaring at the mouth. Silicon, manganese and phosphorus form acidic oxides that the lime turns into slag, and that is why the lining must be basic. The phosphate slag is sold as fertiliser. No fuel is needed: the burning impurities supply all the heat. A charge takes about forty minutes.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), bt.animate.increment_value(1), run_time=0.5, rate_func=linear)
                self.hold(v.dur / 6 - 0.5)
        self.play(FadeOut(VGroup(title, conv, melt, lance, ll, lin, tb)), FadeOut(flame))
        self.remove(flame)
        rows = [["", "Basic Oxygen Process", "Open Hearth Process"], ["oxidant", "pure O₂ through a lance", "haematite (Fe₂O₃) in the charge"],
                ["fuel", "none", "producer gas + regenerators"], ["time", "20–40 min", "8–10 h"], ["control", "limited", "excellent: samples can be taken"],
                ["product", "bulk carbon steel", "alloy and tool steels"]]
        tb = C.table(rows, [2.2, 4.8, 5.4], row_h=0.66, size=23, colors=[th.MUTED, th.SKY, th.AMBER]).move_to(UP * 0.4)
        oh = chem(r"Fe_2O_3 + 3C \rightarrow 2Fe + 3CO,\quad 5Fe_2O_3 + 6P \rightarrow 10Fe + 3P_2O_5", size=28, color=th.AMBER).next_to(tb, DOWN, buff=0.4)
        with self.say("The older open hearth, or Siemens Martin process, uses a shallow hearth heated by producer gas, with brick regenerators that recycle the heat. The oxidising agent is haematite added to the charge, which burns out carbon, silicon, manganese and phosphorus. It is slow, eight to ten hours, but the operator can sample and adjust the melt, so alloy and tool steels are still made this way.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 7 - 0.4)
            self.play(Write(oh))
        self.play(FadeOut(VGroup(tb, oh)))
        heat = VGroup(T("annealing: heat, cool slowly → soft", size=24, color=th.BODY), T("quenching: heat, plunge into water → glass-hard, brittle", size=24, color=th.BODY),
                      T("tempering: reheat gently → tough again", size=24, color=th.BODY), T("case hardening: hard skin on a tough core", size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        with self.say("Heat treatment finishes the steel. Annealing softens it, quenching makes it glass hard but brittle, tempering restores toughness, and case hardening gives a hard skin over a tough core."):
            self.play(LaggedStart(*[FadeIn(h, shift=RIGHT * 0.2) for h in heat], lag_ratio=0.4))
        self.play(FadeOut(heat))
        head, prob = C.example_head(self, "A basic oxygen converter holds 100 t of pig iron with 4.0 % C, to be brought to 0.4 % C. Find the volume of O₂ at STP needed, if the carbon burns to CO. (C = 12)")
        st = C.steps(r"m(\mathrm{C}) = 100\ \mathrm{t} \times (0.040 - 0.004) = 3.6\ \mathrm{t} = 3.6\times10^{6}\ \mathrm{g}",
                     r"n(\mathrm{C}) = \tfrac{3.6\times10^{6}}{12} = 3.0\times10^{5}\ \mathrm{mol}",
                     r"2\mathrm{C} + \mathrm{O_2} \rightarrow 2\mathrm{CO}:\ n(\mathrm{O_2}) = 1.5\times10^{5}\ \mathrm{mol}",
                     r"V = 1.5\times10^{5}\times22.4 = 3.36\times10^{6}\ \mathrm{L} = 3360\ \mathrm{m^3}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[3].set_color(th.AMBER)
        with self.say("Worked example seven point four. The carbon to remove is three point six percent of a hundred tonnes: three point six tonnes, or three times ten to the five moles. Two carbons need one oxygen molecule, so one point five times ten to the five moles of oxygen, times twenty two point four litres: three thousand three hundred and sixty cubic metres."):
            self.play(FadeIn(head), FadeIn(prob))
            for s_ in st:
                self.play(Write(s_))
        self.play(FadeOut(VGroup(head, prob, st)))

    def corrosion(self):
        title = T("Rusting is electrochemical", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        plate = Rectangle(width=11, height=0.6, fill_color=FE, fill_opacity=1, stroke_width=0).move_to([0, -1.6, 0])
        drop = Ellipse(width=7.0, height=2.6, fill_color=C.WATER, fill_opacity=0.3, stroke_color=C.WATER, stroke_width=3).move_to([0, -1.3, 0])
        cut = Rectangle(width=11, height=1.6, fill_color=th.BG, fill_opacity=1, stroke_width=0).move_to([0, -2.7, 0])
        an = T("anode: O₂-poor centre", size=22, color=th.CORAL).move_to([0, -0.4, 0])
        cl = T("cathode: O₂-rich rim", size=22, color=th.MINT).move_to([3.0, 0.3, 0])
        cr = T("cathode", size=22, color=th.MINT).move_to([-3.0, 0.3, 0])
        ph = ValueTracker(0)
        es = always_redraw(lambda: VGroup(*[Dot([sgn * (0.3 + ((ph.get_value() + k / 4) % 1) * 2.6), -1.45, 0], radius=0.07, color=th.SKY) for sgn in (-1, 1) for k in range(4)]))
        o2 = VGroup(*[T("O₂", size=20, color=C.EL["O"], weight="BOLD").move_to([sgn * 3.1, -0.6, 0]) for sgn in (-1, 1)])
        fe2 = VGroup(*[T("Fe²⁺", size=18, color=RUST, weight="BOLD").move_to([dx, -1.1, 0]) for dx in (-0.3, 0.3)])
        eq = VGroup(chem(r"\text{anode: } 2Fe \rightarrow 2Fe^{2+} + 4e^-", size=36, color=th.CORAL), chem(r"\text{cathode: } O_2 + 4H^+ + 4e^- \rightarrow 2H_2O", size=36, color=th.MINT),
                    chem(r"4Fe^{2+} + O_2 + 4H_2O \rightarrow 2Fe_2O_3 + 8H^+ \rightarrow Fe_2O_3\cdot xH_2O", size=32, color=RUST)).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.3)
        with self.say("Now corrosion, and our cold open. Rusting needs both water and oxygen, and it is electrochemical. A drop of water on iron becomes a tiny galvanic cell. The centre of the drop, short of oxygen, is the anode: iron dissolves as iron two ions, leaving electrons behind."):
            self.play(FadeIn(title), FadeIn(plate), FadeIn(cut), FadeIn(drop), FadeIn(an))
            self.play(Write(eq[0]), FadeIn(fe2))
        with self.say("The electrons flow through the metal to the rim, where oxygen dissolves easily. There, oxygen is reduced with hydrogen ions from dissolved carbon dioxide. The iron two ions drift outwards and are oxidised further to hydrated iron three oxide, rust. Rust is flaky and porous, so it does not protect the iron beneath, and corrosion runs right through."):
            self.add(es)
            self.play(FadeIn(cl), FadeIn(cr), FadeIn(o2), Write(eq[1]), ph.animate.set_value(2), run_time=3, rate_func=linear)
            self.play(Write(eq[2]), fe2.animate.shift(UP * 0.1).set_color(RUST), ph.animate.set_value(3.5), run_time=2.5, rate_func=linear)
        fast = T("faster with: salt (sea air, road salt), acids, CO₂, scratches, contact with a less reactive metal", size=22, color=th.AMBER).to_edge(DOWN, buff=0.4)
        with self.say("Salt, acids and dissolved carbon dioxide speed it up, by making the water a better electrolyte. So do scratches, and contact with a less reactive metal."):
            self.play(FadeIn(fast))
        self.play(FadeOut(VGroup(title, plate, cut, drop, an, cl, cr, o2, fe2, eq, fast)), FadeOut(es))
        self.remove(es)
        self.scratch_compare()
        rows = [["Method", "How it works", "Example"], ["barrier coating", "keeps out air and water", "paint, grease, enamel"], ["galvanising", "Zn corrodes first, even when scratched", "roofing sheet, buckets"],
                ["tinning", "a barrier only", "food cans"], ["electroplating", "Cr, Ni or Cu deposited", "taps, cycle parts"], ["sacrificial anode", "Mg or Zn blocks corrode instead", "ships, pipelines, tanks"],
                ["alloying", "own passive film", "stainless steel: Fe + 18 % Cr + 8 % Ni"]]
        tb = C.table(rows, [3.2, 5.0, 4.6], row_h=0.6, size=22, colors=[th.AMBER, th.BODY, th.INK]).move_to(UP * 0.3)
        with self.say("So the ways to prevent rusting: a barrier of paint or grease, galvanising, tinning, electroplating, sacrificial anodes of magnesium or zinc wired to ships and pipelines, and alloying, as in stainless steel with chromium and nickel.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 7 - 0.4)
        self.play(FadeOut(tb))
        self.tip("Galvanised (Zn) iron is protected even when scratched; a scratched tinned (Sn) can rusts FASTER than bare iron. Compare positions in the electrochemical series.",
                 "A two mark favourite. Galvanising protects even when scratched, because zinc is more reactive than iron and corrodes first. A scratched tin can rusts faster than bare iron, because now iron is the more reactive metal and becomes the anode.", state="wink")

    def scratch_compare(self):
        def side(x, coat, coat_lab, flow_to_iron):
            iron = Rectangle(width=4.6, height=0.9, fill_color=FE, fill_opacity=1, stroke_width=0).move_to([x, -1.3, 0])
            cl = Rectangle(width=2.0, height=0.3, fill_color=coat, fill_opacity=1, stroke_width=0).next_to(iron, UP, buff=0).align_to(iron, LEFT)
            cr = Rectangle(width=2.0, height=0.3, fill_color=coat, fill_opacity=1, stroke_width=0).next_to(iron, UP, buff=0).align_to(iron, RIGHT)
            water = Rectangle(width=2.0, height=0.6, fill_color=C.WATER, fill_opacity=0.3, stroke_width=0).move_to([x, -0.55, 0])
            lab = T(coat_lab, size=26, color=coat, weight="BOLD").move_to([x, 2.1, 0])
            return VGroup(iron, cl, cr, water, lab)
        L = side(-3.4, ZN, "zinc coat (galvanised)", True)
        R = side(3.4, "#D8DCE6", "tin coat (tinned)", False)
        sl = VGroup(T("Zn  −0.76 V", size=22, color=ZN), T("Fe  −0.44 V", size=22, color=FE), T("Sn  −0.14 V", size=22, color="#D8DCE6")).arrange(DOWN, buff=0.15).move_to([0, 0.9, 0])
        aL = VGroup(T("Zn is the anode: it corrodes", size=22, color=ZN), T("iron is the cathode: safe", size=22, color=th.MINT)).arrange(DOWN, buff=0.08).next_to(L, DOWN, buff=0.3)
        aR = VGroup(T("Fe is the anode: it corrodes", size=22, color=th.CORAL), T("tin is the cathode", size=22, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(R, DOWN, buff=0.3)
        with self.say("Now solve the cold open. Scratch both sheets, and water bridges the coating and the exposed iron. A second galvanic cell forms, and the more reactive metal becomes the anode. Look at the electrochemical series: zinc minus zero point seven six, iron minus zero point four four, tin minus zero point one four."):
            self.play(FadeIn(L), FadeIn(R))
            self.play(FadeIn(sl))
        with self.say("On the galvanised sheet, zinc is more reactive than iron. Zinc is the anode and corrodes, slowly, while the iron is the cathode and stays safe. On the tinned sheet, iron is more reactive than tin. Now iron is the anode, and the large tin surface is the cathode, so the exposed iron rusts even faster than bare iron would."):
            self.play(FadeIn(aL), L[1].animate.set_fill(WHITE, opacity=0.6), L[2].animate.set_fill(WHITE, opacity=0.6))
            rust = Ellipse(width=1.8, height=0.5, fill_color=RUST, fill_opacity=0.9, stroke_width=0).move_to([3.4, -0.9, 0])
            self.play(FadeIn(aR), GrowFromCenter(rust))
            nb = C.show_neby(self, "success", height=1.3, at=[0, -2.4, 0])
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(L, R, sl, aL, aR, rust)))

    # ------------------------------------------------------------------ part 5: silver
    def p5(self):
        self.section(4)
        rows = [["Ore", "Formula"], ["native silver", "Ag"], ["argentite, silver glance (chief)", "Ag₂S"], ["horn silver", "AgCl"], ["ruby silver", "Ag₃SbS₃"], ["anode mud of Cu refining", "Ag, Au, Pt"]]
        tb = C.table(rows, [6.2, 3.0], row_h=0.62, size=26, colors=[th.INK, AG]).move_to(UP * 0.5)
        with self.say("Silver is the best conductor of heat and electricity of all metals, the metal of Nepali jewellery and the old mohar coins. Most silver today is a by product of lead, zinc and copper refining. Its chief ore is argentite, silver sulphide.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(tb))
        boxes, arrows = flow(["froth flotation", "leach with NaCN + air", "precipitate with Zn", "Moebius refining"], w=2.8)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in boxes], lag_ratio=0.15), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.4)
        light(self, boxes, 1)
        e1 = chem(r"Ag_2S + 4NaCN \rightleftharpoons 2Na[Ag(CN)_2] + Na_2S", size=40, color=th.AMBER).move_to([0, 0.9, 0])
        e2 = chem(r"2Na_2S + 2O_2 + H_2O \rightarrow Na_2S_2O_3 + 2NaOH", size=32).next_to(e1, DOWN, buff=0.45)
        lc = T("removing Na₂S pulls the equilibrium right: Le Chatelier at work", size=24, color=th.MINT).next_to(e2, DOWN, buff=0.3)
        arr = Arrow(e1.get_left() + DOWN * 0.15 + RIGHT * 6.6, e1.get_right() + DOWN * 0.15 + RIGHT * 0.2, buff=0, color=th.MINT, stroke_width=4).next_to(e1, DOWN, buff=0.05)
        with self.say("The cyanide process. The concentrated ore is stirred with dilute sodium cyanide while air is blown through. Silver sulphide dissolves as the soluble complex sodium dicyanoargentate. But the reaction is reversible, and would stop early. The air oxidises the sodium sulphide product as it forms, so the equilibrium is pulled to the right. Le Chatelier's principle doing real industrial work."):
            self.play(Write(e1))
            self.play(FadeIn(e2))
            self.play(GrowArrow(arr), FadeIn(lc))
        self.play(FadeOut(VGroup(e1, e2, lc, arr)))
        light(self, boxes, 2)
        e3 = chem(r"2Na[Ag(CN)_2] + Zn \rightarrow Na_2[Zn(CN)_4] + 2Ag\downarrow", size=40, color=th.AMBER).move_to([0, 0.9, 0])
        why = T("zinc is more electropositive than silver, so it displaces it", size=24, color=th.BODY).next_to(e3, DOWN, buff=0.35)
        with self.say("Zinc dust is added to the solution. Zinc is more electropositive, so it displaces the silver, which falls as a spongy precipitate."):
            self.play(Write(e3))
            self.play(FadeIn(why))
        self.play(FadeOut(VGroup(e3, why)))
        light(self, boxes, 3)
        mo = para("Moebius process: impure silver anode, pure silver cathode, AgNO₃ + 1 % HNO₃ electrolyte. Pure silver crystals fall into a bag; gold stays in the anode mud. 99.9 % silver.", width=11.5, size=26, color=th.BODY).move_to([0, 0.3, 0])
        key = T("Why cyanide? Ag⁺ forms a very stable complex with CN⁻, dragging even Ag₂S into solution.", size=22, color=th.AMBER).next_to(mo, DOWN, buff=0.4)
        with self.say("Finally the Moebius process refines it electrolytically, with silver nitrate as the electrolyte, to ninety nine point nine percent. Why cyanide at all? Silver ions form an extremely stable complex with cyanide, so stable that even the insoluble sulphide is forced into solution. The price is a lethal effluent."):
            self.play(FadeIn(mo))
            self.play(FadeIn(key))
        self.play(FadeOut(VGroup(boxes, arrows, mo, key)))
        tar = chem(r"4Ag + 2H_2S + O_2 \rightarrow 2Ag_2S + 2H_2O", size=36).move_to([0, 1.6, 0])
        tl = T("why silver ornaments tarnish black in polluted air", size=24, color=th.MUTED).next_to(tar, DOWN, buff=0.2)
        coin = Circle(radius=0.9, fill_color=AG, fill_opacity=1, stroke_color=WHITE, stroke_width=3).move_to([0, -1.2, 0])
        with self.say("Silver is unaffected by air and water, but hydrogen sulphide in polluted air tarnishes it black with silver sulphide. It dissolves in nitric acid and hot concentrated sulphuric acid, but not in dilute hydrochloric or sulphuric acid."):
            self.play(Write(tar), FadeIn(tl), FadeIn(coin))
            self.play(coin.animate.set_fill("#3A3A3A"), run_time=2.0)
        self.play(FadeOut(VGroup(tar, tl, coin)))
        self.silver_nitrate()
        self.silver_chloride()

    def silver_nitrate(self):
        title = T("Silver nitrate, AgNO₃: lunar caustic", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        prep = VGroup(chem(r"3Ag + 4HNO_3(\text{dil}) \rightarrow 3AgNO_3 + NO + 2H_2O", size=30), chem(r"Ag + 2HNO_3(\text{conc}) \rightarrow AgNO_3 + NO_2 + H_2O", size=30)).arrange(DOWN, buff=0.25).next_to(title, DOWN, buff=0.4)
        note = T("copper impurity: heat to 450 °C, Cu(NO₃)₂ → black CuO, then extract AgNO₃ with water", size=22, color=th.MUTED).next_to(prep, DOWN, buff=0.3)
        with self.say("Silver nitrate is called lunar caustic: luna was the alchemists' name for silver, and the solid burns skin. It is made by dissolving silver in nitric acid. If the silver contained copper, heating to four fifty degrees turns copper nitrate into insoluble black oxide, and the silver nitrate is extracted with water."):
            self.play(FadeIn(title), Write(prep))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(prep, note)))
        items = [("NaCl", "#F5F5F5", "white curdy AgCl"), ("KBr", "#F2EBB0", "pale yellow AgBr"), ("KI", "#F2D43C", "yellow AgI"), ("K₂CrO₄", "#B04020", "brick-red Ag₂CrO₄"), ("NaOH", "#5A3A2A", "brown Ag₂O")]
        xs = np.linspace(-5.0, 5.0, 5)
        tubes = VGroup()
        pps = VGroup()
        for x, (lab, col, res) in zip(xs, items):
            tb = tube([x, -0.5, 0], color="#E6E9F2", opacity=0.12)
            l1 = T("+ " + lab, size=22, color=th.AMBER, weight="BOLD").next_to(tb, UP, buff=0.2)
            l2 = para(res, width=2.2, size=19, color=th.BODY, align="center").next_to(tb, DOWN, buff=0.2)
            tubes.add(VGroup(tb, l1, l2))
            pps.add(ppt_in(tb, col, seed=int(x * 10) + 60))
        with self.say("Its precipitates are a colour chart. With chloride, white curdy silver chloride. With bromide, pale yellow. With iodide, yellow. With chromate, brick red silver chromate, the end point of Mohr's titration. And with alkali, brown silver oxide, not a hydroxide.") as v:
            for k in range(5):
                self.play(FadeIn(tubes[k]), run_time=0.4)
                self.play(FadeIn(pps[k]), run_time=0.4)
                self.hold(v.dur / 5 - 0.85)
        self.play(FadeOut(VGroup(tubes, pps)))
        tol = VGroup(chem(r"Ag_2O + 4NH_3 + H_2O \rightarrow 2[Ag(NH_3)_2]OH", size=34, color=th.AMBER), T("Tollens' reagent: the silver-mirror test for aldehydes", size=24, color=th.BODY),
                     chem(r"2AgNO_3 \xrightarrow{\text{heat}} 2Ag + 2NO_2 + O_2", size=32)).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        uses = para("Uses: photographic halides, indelible ink, Tollens' reagent, halide tests, argentometric titration, silver plating", width=11.5, size=24, color=th.MUTED).to_edge(DOWN, buff=0.45)
        with self.say("Silver oxide dissolves in excess ammonia to give Tollens' reagent, used in the silver mirror test for aldehydes. Heated strongly, silver nitrate decomposes to silver, nitrogen dioxide and oxygen. It is used for photographic film, indelible ink, Tollens' reagent, testing for halides, and argentometric titrations."):
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.2) for t_ in tol], lag_ratio=0.4))
            self.play(FadeIn(uses))
        self.play(FadeOut(VGroup(title, tol, uses)))

    def silver_chloride(self):
        title = T("Silver chloride, AgCl", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        prep = chem(r"AgNO_3 + NaCl \rightarrow AgCl\downarrow + NaNO_3", size=34).next_to(title, DOWN, buff=0.35)
        rows = [["Dissolves in", "Complex formed"], ["NH₃(aq)", "[Ag(NH₃)₂]Cl  (AgBr only partly, AgI not at all)"], ["Na₂S₂O₃, 'hypo'", "Na₃[Ag(S₂O₃)₂]: photographic fixing"], ["KCN", "K[Ag(CN)₂]"]]
        tb = C.table(rows, [3.2, 8.6], row_h=0.62, size=23, colors=[th.AMBER, th.BODY]).next_to(prep, DOWN, buff=0.4)
        with self.say("Silver chloride, horn silver, is made by adding a chloride to silver nitrate. It is white, curdy, and insoluble in water and dilute nitric acid. But it dissolves in three reagents, all by forming complexes: ammonia, sodium thiosulphate, which is how photographs are fixed, and potassium cyanide.") as v:
            self.play(FadeIn(title), Write(prep))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(prep, tb)))
        sq = Square(side_length=1.6, fill_color="#F5F5F5", fill_opacity=1, stroke_width=0).move_to([-2.4, -0.4, 0])
        sun = VGroup(Circle(radius=0.45, fill_color=th.AMBER, fill_opacity=1, stroke_width=0), *[Line(0.6 * np.array([np.cos(a), np.sin(a), 0]), 0.85 * np.array([np.cos(a), np.sin(a), 0]), color=th.AMBER, stroke_width=4) for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to([-5.2, 1.4, 0])
        eq = chem(r"2AgCl \xrightarrow{\text{light}} 2Ag + Cl_2", size=40, color=th.AMBER).move_to([2.6, 0.4, 0])
        use = para("the basis of film photography and photochromic lenses; also the Ag/AgCl reference electrode in pH probes and ECG pads", width=6.0, size=24, color=th.BODY).next_to(eq, DOWN, buff=0.4)
        with self.say("In light, silver chloride slowly turns violet, then grey, as it decomposes to silver and chlorine. That light sensitivity is the whole basis of film photography and of self darkening spectacle lenses. Silver chloride is also used in the silver silver chloride reference electrode inside pH probes and E C G pads."):
            self.play(FadeIn(sq), FadeIn(sun))
            self.play(sq.animate.set_fill("#6A6070"), Write(eq), run_time=2.5)
            self.play(FadeIn(use))
        self.play(FadeOut(VGroup(title, sq, sun, eq, use)))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Cu: flotation, roast, smelt to matte, Bessemer auto-reduction, electrolysis.",
            "Blue vitriol: blue → white at 230 °C; KI gives Cu₂I₂ + I₂.",
            "Zn: roast ZnS, reduce ZnO with C, condense vapour; amphoteric.",
            "White vitriol: Zn(OH)₂ dissolves in excess NaOH or NH₃.",
            "Hg: HgS + O₂ → Hg + SO₂; excess Hg gives Hg₂²⁺, excess acid Hg²⁺.",
            "Fe: blast furnace (CO reduces Fe₂O₃); steel by basic oxygen and open hearth.",
            "Rusting is electrochemical; galvanising beats tinning when scratched.",
            "Ag: cyanide process, then Zn; AgCl dissolves in NH₃, hypo, KCN.",
        ], "Let us recap. Copper comes from copper pyrite by flotation, roasting, smelting to matte, and auto reduction in the Bessemer converter, then electrolytic refining. Blue vitriol loses its water in stages and its solution gives a famous set of tests. Zinc is reduced as a vapour and is amphoteric. Mercury needs only roasting, and its two chlorides are opposites. Iron is made in the blast furnace and refined to steel, and it rusts electrochemically, which is why galvanising beats tinning. And silver is extracted by the cyanide process, with its nitrate and chloride as key compounds.")
        self.outro("That is the heavy metals, and the end of inorganic chemistry. Next we begin organic chemistry with the haloalkanes. See you in the next lesson on NEBians.")
