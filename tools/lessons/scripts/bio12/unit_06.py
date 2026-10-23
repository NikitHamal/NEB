import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402

EPC = "#F4A6C6"
NUCC = "#7A3E8F"
COLL = "#F3EBD6"
ELAS = "#FFD166"
BM = "#FFB547"
ACT = "#4CC9F0"
MYO = "#FF6B6B"
AXON = "#C77DFF"
MYEL = "#FFE08A"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


def cell_row(kind, x0=-5.0, n=9, w=0.62, y=0.0, show_bm=True):
    g = VGroup()
    if kind == "squamous":
        h = 0.22
    elif kind == "cuboidal":
        h = w
    else:
        h = w * 2.4
    for i in range(n):
        x = x0 + i * w
        c = RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_color="#E06FA0", stroke_width=2, fill_color=EPC, fill_opacity=0.35).move_to([x, y + h / 2, 0])
        if kind == "squamous":
            nu = Ellipse(width=w * 0.45, height=0.13, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to([x, y + h / 2 + 0.03, 0])
        elif kind == "cuboidal":
            nu = Circle(radius=w * 0.18, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to(c)
        else:
            nu = Ellipse(width=w * 0.38, height=w * 0.55, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to([x, y + h * 0.25, 0])
        g.add(VGroup(c, nu))
    bm = Line([x0 - w / 2, y - 0.04, 0], [x0 + (n - 0.5) * w, y - 0.04, 0], color=BM, stroke_width=6) if show_bm else VGroup()
    return g, bm


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 6
    TITLE = "Animal Tissues"
    SUBTITLE = "Four tissues build every organ"
    SECTIONS = ["Epithelial tissue", "Connective tissue", "Muscular tissue", "Nervous tissue"]
    NEXT = "Unit 7 · Developmental Biology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        thorn = Polygon([-1.0, -2.6, 0], [-0.8, -2.6, 0], [-0.9, -2.0, 0], stroke_width=0, fill_color="#8A6A48", fill_opacity=1)
        foot = RoundedRectangle(corner_radius=0.3, width=2.0, height=0.6, stroke_width=0, fill_color="#E0B48C", fill_opacity=1).move_to([-0.6, -1.7, 0])
        timer = VGroup(T("reflex time", size=24, color=th.MUTED), DecimalNumber(0, num_decimal_places=3, font_size=60, color=th.AMBER), T("seconds", size=22, color=th.MUTED)).arrange(DOWN, buff=0.08).move_to([3.6, 1.0, 0])
        with self.say("Walking barefoot in a Chitwan forest, you step on a thorn. Before you even feel the pain, your foot has already jumped back. How fast was that?"):
            self.play(FadeIn(thorn), FadeIn(foot))
            self.play(foot.animate.shift(DOWN * 0.15), run_time=0.3)
            self.play(foot.animate.shift(UP * 1.2), run_time=0.25)
            self.play(FadeIn(timer))
            self.play(timer[1].animate.set_value(0.021), run_time=1.0)
        cmp_ = VGroup(T("with myelin:  0.021 s", size=32, color=th.MINT, weight="BOLD"), T("without myelin:  3.4 s", size=32, color=th.CORAL, weight="BOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -1.4, 0])
        with self.say("About twenty one thousandths of a second. Now take away one fatty wrapping around the nerve fibres, and the same reflex would take three and a half seconds. Long enough for the thorn to go deep. That wrapping is a tissue, and by the end of this lesson you will be able to calculate both numbers yourself."):
            self.play(FadeIn(cmp_[0]))
            self.play(FadeIn(cmp_[1]))
        nb = B.neby_in(self, "surprised", height=1.4, at=[-4.6, 1.4, 0])
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(thorn, foot, timer, cmp_)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 6: Animal Tissues, the first unit of zoology. The whole animal body is built from just four tissues. Learn them properly now, and every organ that follows becomes easy."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Four tissues, four parts. Epithelial tissue, the coverings and linings. Connective tissue, from fat to bone to blood. Muscular tissue, and how a sarcomere contracts. And nervous tissue: the neuron, the myelin sheath, and the synapse.")

    # ------------------------------------------------------------------ part 1: epithelium
    def p1(self):
        self.section(0)
        row, bm = cell_row("columnar", x0=-5.6, n=10, w=0.62, y=-0.4)
        below = Rectangle(width=6.6, height=1.4, stroke_width=0, fill_color="#3A2E40", fill_opacity=0.8).move_to([-2.8, -1.15, 0])
        cap_ = Line([-6.0, -1.0, 0], [0.0, -1.0, 0], color=th.CORAL, stroke_width=4)
        bl = VGroup(B.label("free (apical) surface", [3.4, 1.6, 0], row[6][0].get_top(), color=EPC, size=22),
                    B.label("basement membrane", [3.4, -0.2, 0], bm.point_from_proportion(0.85), color=BM, size=22),
                    B.label("connective tissue with capillaries", [3.4, -1.3, 0], cap_.point_from_proportion(0.9), color=th.CORAL, size=22))
        for l_ in bl:
            l_[1].align_to(np.array([1.4, 0, 0]), LEFT)
            l_[0].put_start_and_end_on(l_[1].get_left() + LEFT * 0.08, l_[0].get_end())
        with self.say("Epithelium is a sheet of tightly packed cells, with almost nothing between them, resting on a thin non cellular basement membrane. It covers the body's surfaces and lines its cavities and tubes."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in row], lag_ratio=0.06), Create(bm))
            self.play(FadeIn(below), Create(cap_))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in bl], lag_ratio=0.3))
        feats = VGroup(*[para(s_, width=5.0, size=22, color=th.INK) for s_ in ["cells packed, joined by junctions; matrix negligible", "polarity: a free surface and a basal surface",
                                                                  "avascular: fed by diffusion from below", "high power of regeneration", "the only tissue from all three germ layers"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.9, -2.4, 0]).scale(0.85)
        food = VGroup(*[Dot([x, -1.0, 0], radius=0.05, color=th.MINT) for x in np.linspace(-5.4, -0.6, 8)])
        with self.say("Its characters follow from its job as a boundary. The cells are joined by junctions, so the sheet is leak proof. It has a free surface and a basal surface. It has no blood vessels at all: food and oxygen diffuse up from the capillaries beneath. It regrows fast, because it is the layer that wears away. And it is the only tissue that arises from all three germ layers."):
            self.play(FadeOut(bl), feats.animate.scale(1 / 0.85).move_to([3.7, 0.3, 0]), run_time=0.6)
            self.play(*[d_.animate.shift(UP * 1.0) for d_ in food], FadeIn(food), run_time=1.6)
        self.play(FadeOut(VGroup(row, bm, below, cap_, feats, food)))
        self.p1_types()
        self.p1_strat()
        self.p1_glands()

    def p1_types(self):
        head = T("Simple epithelia: one layer", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.8, size=25)
        kinds = [("squamous", "Simple squamous", "Flat, tile-like cells. Alveoli, Bowman's capsule, lining of blood vessels: diffusion and filtration.", "Simple squamous. Flat, tile like cells, thin enough for gases to diffuse across. Lungs' alveoli, Bowman's capsule in the kidney, and the lining of every blood vessel."),
                 ("cuboidal", "Simple cuboidal", "Cube-shaped, round central nucleus. Kidney tubules, thyroid follicles, gland ducts: absorption and secretion.", "Simple cuboidal. Cube shaped cells with a round central nucleus. Kidney tubules, thyroid follicles and the ducts of glands, for absorbing and secreting."),
                 ("columnar", "Simple columnar", "Tall, nucleus near the base. Stomach, small intestine, gall bladder: secretion and absorption.", "Simple columnar. Tall cells with the nucleus near the base, lining the stomach and the small intestine, where a lot of secreting and absorbing happens.")]
        cur = None
        self.play(FadeIn(head))
        for k_, t_, sub, sy in kinds:
            row, bm = cell_row(k_, x0=-5.6, n=8, w=0.62, y=-0.8)
            new = VGroup(row, bm)
            with self.say(sy):
                if cur is None:
                    self.play(FadeIn(new, shift=UP * 0.2))
                else:
                    self.play(ReplacementTransform(cur, new), run_time=1.0)
                cap(t_, color=EPC, swatch=EPC, sub=sub)
            cur = new
        ph = ValueTracker(0.0)
        row = cur[0]
        cil = always_redraw(lambda: VGroup(*[Line(c_[0].get_top() + RIGHT * dx, c_[0].get_top() + RIGHT * dx + polar(0.35, PI / 2 - 0.5 * np.sin(ph.get_value() + i * 0.6)), color=th.MINT, stroke_width=2)
                                             for i, c_ in enumerate(row) for dx in (-0.2, -0.07, 0.07, 0.2)]))
        mucus = VGroup(*[Dot([x, row[0][0].get_top()[1] + 0.55, 0], radius=0.07, color=th.AMBER) for x in np.linspace(-5.6, -2.0, 6)])
        with self.say("Give columnar cells cilia, and the beating hairs sweep things along: mucus in the bronchioles, the egg along the oviduct, cerebrospinal fluid in the brain's ventricles. That is ciliated columnar epithelium."):
            self.add(cil)
            cap("Ciliated columnar", color=th.MINT, swatch=th.MINT, sub="Oviduct, bronchioles, brain ventricles: moves mucus, the ovum, CSF.")
            self.play(ph.animate.set_value(TAU * 4), *[d_.animate.shift(RIGHT * 1.6) for d_ in mucus], FadeIn(mucus), run_time=4.0, rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(cur, mucus)), FadeOut(cil))
        self.remove(cil)
        heights = [2.0, 1.1, 2.0, 1.3, 2.0, 1.0, 2.0, 1.2]
        ps = VGroup()
        for i, hh in enumerate(heights):
            x = -5.6 + i * 0.62
            c_ = RoundedRectangle(corner_radius=0.05, width=0.6, height=hh, stroke_color="#E06FA0", stroke_width=2, fill_color=EPC, fill_opacity=0.35).move_to([x, -0.8 + hh / 2, 0])
            nu = Ellipse(width=0.22, height=0.32, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to([x, -0.8 + (0.45 if hh < 1.5 else 1.2), 0])
            ps.add(VGroup(c_, nu))
        bm = Line([-5.95, -0.84, 0], [-0.8, -0.84, 0], color=BM, stroke_width=6)
        with self.say("Pseudostratified epithelium is a trick of the eye. The cells are of different heights, so their nuclei sit at two levels and the sheet looks layered. But every single cell stands on the basement membrane. It is one layer thick. It lines the trachea and the nose."):
            self.play(FadeIn(ps), Create(bm))
            cap("Pseudostratified", color=EPC, swatch=EPC, sub="ONE layer: every cell touches the basement membrane; nuclei at two levels. Trachea, nasal cavity.")
            self.play(Indicate(bm, color=BM, scale_factor=1.05))
        self.play(FadeOut(VGroup(ps, bm, head)))
        cap.clear()

    def p1_strat(self):
        head = T("Compound epithelia: many layers", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        y0 = -2.0
        bm = Line([-6.0, y0 - 0.05, 0], [-0.4, y0 - 0.05, 0], color=BM, stroke_width=6)
        layers = VGroup()
        for L in range(5):
            h = 0.5 - 0.08 * L
            w = 0.6 + 0.14 * L
            n = int(5.4 / w)
            for i in range(n):
                x = -5.7 + w / 2 + i * w + (0.1 * L)
                y = y0 + sum(0.5 - 0.08 * k for k in range(L)) + h / 2
                col = EPC if L < 3 else ("#E8DCC4" if L == 4 else "#E9B8C9")
                layers.add(RoundedRectangle(corner_radius=0.04, width=w * 0.96, height=h * 0.94, stroke_color="#E06FA0", stroke_width=1.5, fill_color=col, fill_opacity=0.5).move_to([x, y, 0]))
        germ = T("germinative layer: the only one that divides", size=22, color=BM).next_to(bm, DOWN, buff=0.15)
        top = T("dead, flat, keratinised cells flake off", size=22, color="#E8DCC4").move_to([-3.2, 1.0, 0])
        cap = B.Captions(self, at=(3.6, 0.2, 0), width=5.4, size=25)
        with self.say("Where wear is heavy, the epithelium is many cells thick. Only the deepest layer, the germinative layer, sits on the basement membrane and divides. Its daughters are pushed upward, flatten, die and are shed from the top."):
            self.play(FadeIn(head), Create(bm), FadeIn(germ))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in layers], lag_ratio=0.01), run_time=1.6)
            self.play(layers.animate.shift(UP * 0.12), run_time=0.8)
            self.play(FadeIn(top))
            cap("Stratified squamous", color=EPC, swatch=EPC, sub="Skin: keratinised, dry, waterproof. Mouth, oesophagus, vagina: non-keratinised, moist.")
        with self.say("In the skin, the dying cells fill with the tough protein keratin, giving a dry, waterproof keratinised surface. In the mouth, oesophagus and vagina the surface stays moist and is non keratinised."):
            pass
        self.play(FadeOut(VGroup(layers, top)))
        tr = VGroup(*[RoundedRectangle(corner_radius=0.18, width=0.75, height=0.55, stroke_color="#E06FA0", stroke_width=1.8, fill_color=EPC, fill_opacity=0.45).move_to([-5.4 + 0.78 * i + 0.3 * (L % 2), y0 + 0.3 + 0.5 * L, 0]) for L in range(5) for i in range(6)])
        with self.say("Transitional epithelium lines the ureter and the urinary bladder. Its cells can slide over one another. When the bladder is empty the lining is four or five cells thick with domed surface cells. As it fills, it stretches to just two or three thin layers."):
            self.play(FadeIn(tr))
            cap("Transitional", color=EPC, swatch=EPC, sub="Ureter and bladder: 4–5 layers relaxed, 2–3 thin layers stretched.")
            self.play(tr.animate.stretch(0.45, 1, about_edge=DOWN).stretch(1.15, 0, about_edge=LEFT), run_time=1.6)
            self.play(tr.animate.stretch(1 / 0.45, 1, about_edge=DOWN).stretch(1 / 1.15, 0, about_edge=LEFT), run_time=1.2)
        self.play(FadeOut(VGroup(head, tr, bm, germ)))
        cap.clear()
        self.tip("Pseudostratified is ONE layer: every cell touches the basement membrane. Stratified has real layers; only the deepest touches it.",
                 "Exam tip. Pseudostratified is not stratified. In pseudostratified epithelium every cell touches the basement membrane, so it is one layer. In a stratified epithelium only the deepest layer does.")

    def p1_glands(self):
        head = T("Glandular epithelium: how cells secrete", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        xs = [-4.2, 0.0, 4.2]
        cells = VGroup(*[RoundedRectangle(corner_radius=0.2, width=1.6, height=2.2, stroke_color="#E06FA0", stroke_width=3, fill_color=EPC, fill_opacity=0.3).move_to([x, -0.3, 0]) for x in xs])
        nuc = VGroup(*[Circle(radius=0.22, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to([x, -0.9, 0]) for x in xs])
        ves = VGroup(*[VGroup(*[Dot([x + dx, 0.3 + dy, 0], radius=0.09, color=th.AMBER) for dx, dy in [(-0.35, 0), (0.0, 0.25), (0.35, 0.05), (-0.15, 0.5), (0.25, 0.55)]]) for x in xs])
        names = VGroup(*[VGroup(T(n_, size=26, color=th.AMBER, weight="BOLD"), T(e_, size=20, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([x, -2.3, 0]) for x, n_, e_ in
                         zip(xs, ["merocrine", "apocrine", "holocrine"], ["salivary gland, pancreas", "mammary gland", "sebaceous gland"])])
        with self.say("Epithelial cells that specialise for secretion sink into the tissue below and form glands. A single goblet cell is a unicellular gland; many cells together make a multicellular gland. Exocrine glands release through a duct; endocrine glands have no duct and release hormones into the blood. And there are three ways a cell can let go of its secretion."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(nuc), FadeIn(ves))
        with self.say("Merocrine: the secretion leaves by exocytosis and the cell stays whole, as in the salivary glands. Apocrine: the tip of the cell pinches off with the secretion, as in the mammary gland. Holocrine: the whole cell breaks down and becomes the secretion, as in the sebaceous glands of the skin."):
            self.play(ves[0].animate.shift(UP * 1.6).set_opacity(0.7), FadeIn(names[0]), run_time=1.0)
            tip_ = Ellipse(width=1.4, height=0.7, stroke_color="#E06FA0", stroke_width=2, fill_color=EPC, fill_opacity=0.3).move_to([0, 0.75, 0])
            self.play(cells[1].animate.stretch(0.75, 1, about_edge=DOWN), FadeIn(tip_), run_time=0.6)
            self.play(VGroup(tip_, ves[1]).animate.shift(UP * 1.3), FadeIn(names[1]), run_time=1.0)
            self.play(FadeOut(cells[2], scale=1.3), FadeOut(nuc[2]), ves[2].animate.scale(1.5).shift(UP * 0.8), FadeIn(names[2]), run_time=1.2)
        self.play(FadeOut(VGroup(head, cells[:2], nuc[:2], ves, tip_, names)))
        head, prob = B.example_head(self, "In a ×1000 photomicrograph of the intestinal lining, a columnar cell measures 40 mm tall and 8 mm across. (a) Real height and width in µm? (b) How many such cells side by side along 1 mm of lining?", size=25)
        steps = VGroup(M(r"\text{actual} = \frac{\text{image}}{M}:\quad \frac{40\text{ mm}}{1000} = 0.040\text{ mm} = 40\ \mu\text{m},\quad \frac{8}{1000}\text{ mm} = 8\ \mu\text{m}", size=34),
                       M(r"n = \frac{1000\ \mu\text{m}}{8\ \mu\text{m}} = 125 \text{ cells}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["A quick calculation.", "Actual size is image size divided by magnification. Forty millimetres over a thousand is zero point zero four millimetres, which is forty micrometres. The width is eight micrometres.",
                "A millimetre is a thousand micrometres, so a thousand over eight: one hundred and twenty five cells. Forty tall and eight wide: five times taller than broad. That is what columnar means."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.4)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("Transitional epithelium is characteristic of the",
                  ["trachea", "small intestine", "urinary bladder", "oesophagus"], 2,
                  "Pause and think. Which organ needs a lining that can stretch?",
                  "The urinary bladder, and the ureter. Its cells slide over each other as it fills. The trachea has pseudostratified ciliated epithelium, the intestine simple columnar, and the oesophagus stratified squamous.")

    # ------------------------------------------------------------------ part 2: connective tissue
    def p2(self):
        self.section(1)
        rng = np.random.default_rng(6)
        box = RoundedRectangle(corner_radius=0.2, width=6.0, height=4.4, stroke_color=th.MUTED, stroke_width=2, fill_color="#20263F", fill_opacity=1).move_to([-3.0, -0.3, 0])
        coll = VGroup(*[VMobject(stroke_color=COLL, stroke_width=7, stroke_opacity=0.8).set_points_smoothly([[x, y, 0] for x, y in zip(np.linspace(-5.8, -0.2, 9), y0 + 0.12 * np.sin(np.linspace(0, 7, 9) + k))])
                        for k, y0 in enumerate(rng.uniform(-2.2, 1.6, 5))])
        elas = VGroup(*[VMobject(stroke_color=ELAS, stroke_width=2.5).set_points_as_corners([[rng.uniform(-5.8, -0.3), rng.uniform(-2.3, 1.7), 0] for _ in range(3)]) for _ in range(6)])
        fib = VGroup(*[VGroup(Ellipse(width=0.9, height=0.25, stroke_width=0, fill_color=th.SKY, fill_opacity=0.9), Dot(radius=0.06, color="#0B0E1A")).rotate(rng.uniform(0, PI)).move_to([x, y, 0]) for x, y in [(-4.8, 0.8), (-2.0, -1.4), (-1.0, 1.0)]])
        mac = VGroup(Circle(radius=0.35, stroke_width=0, fill_color=th.MINT, fill_opacity=0.8), Dot(radius=0.1, color="#0B0E1A")).move_to([-3.4, -0.4, 0])
        mast = VGroup(Circle(radius=0.3, stroke_width=0, fill_color=th.PINK, fill_opacity=0.8), *[Dot(polar(0.15, a), radius=0.04, color="#5A1A3A") for a in np.linspace(0, TAU, 7)]).move_to([-1.4, -0.2, 0])
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.8, size=25)
        with self.say("Connective tissue is the mirror image of epithelium. Here the cells are few and far apart, and the work is done by a large intercellular matrix of fibres and ground substance. It binds, supports, packs, transports and defends."):
            self.play(FadeIn(box))
            cap("Few cells, lots of matrix", sub="Mesodermal. Binds, supports, packs, transports, defends.")
        with self.say("Three kinds of fibre run through the matrix. White collagen fibres: thick, wavy bundles, very strong and inelastic; boil them and they become gelatin. Yellow elastic fibres: thin, branching, stretching to one and a half times their length and snapping back. And fine reticular fibres, the mesh of lymph nodes and the spleen."):
            self.play(LaggedStart(*[Create(c_) for c_ in coll], lag_ratio=0.15))
            cap("White collagen fibres", color=COLL, swatch=COLL, sub="Thick, wavy, unbranched, strong, inelastic.")
            self.play(LaggedStart(*[Create(e_) for e_ in elas], lag_ratio=0.1))
            cap("Yellow elastic fibres", color=ELAS, swatch=ELAS, sub="Thin, branching, stretch about 1.5× and recoil. Reticular fibres: a fine mesh.")
        bac = Dot([-2.6, 0.2, 0], radius=0.07, color=th.CORAL)
        with self.say("And the cells. Fibroblasts make the fibres and ground substance. Macrophages crawl about engulfing bacteria and debris. Mast cells release heparin, which stops blood clotting inside vessels, and histamine, which drives inflammation and allergy. Plasma cells make antibodies, and adipocytes store fat."):
            self.play(FadeIn(fib))
            cap("Fibroblasts make the fibres", color=th.SKY, swatch=th.SKY)
            self.play(FadeIn(mac), FadeIn(bac))
            self.play(mac.animate.move_to(bac.get_center()), run_time=0.8)
            self.play(FadeOut(bac), mac.animate.scale(1.15))
            self.play(FadeIn(mast))
            cap("Macrophage engulfs · mast cell: heparin + histamine", color=th.PINK, sub="Also plasma cells (antibodies) and adipocytes (fat).")
        self.play(FadeOut(VGroup(box, coll, elas, fib, mac, mast)))
        cap.clear()
        rows = [["group", "types", "chief job"], ["loose", "areolar, adipose, reticular", "packing, fat store, framework"], ["dense", "tendon, ligament; dermis", "transmits or resists pull"], ["skeletal", "cartilage, bone", "support, protection, movement"], ["fluid", "blood, lymph", "transport, defence"]]
        tb = B.table(rows, [2.4, 5.0, 5.0], row_h=0.66, size=23, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 1.2, 0])
        fat = VGroup()
        for i in range(4):
            for j in range(2):
                c_ = Circle(radius=0.5, stroke_color=ELAS, stroke_width=2, fill_color="#3D3820", fill_opacity=1).move_to([-3.6 + i * 1.05, -1.4 - j * 1.0 + 0.5 * (i % 2) * 0.0, 0])
                drop = Circle(radius=0.42, stroke_width=0, fill_color="#FFF0B3", fill_opacity=0.85).move_to(c_.get_center() + RIGHT * 0.03)
                nu = Ellipse(width=0.12, height=0.3, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to(c_.get_center() + LEFT * 0.42)
                fat.add(VGroup(c_, drop, nu))
        fl = para("Adipose: each cell is almost all fat droplet, with the nucleus squashed to one side — a signet ring. Stores energy, insulates, cushions the kidneys and eyeballs.", width=5.4, size=22, color=th.INK).move_to([3.4, -1.9, 0])
        with self.say("Connective tissue comes in four groups: loose, dense, skeletal and fluid. Loose areolar tissue is the body's packing material, under the skin and around every organ. Fill it with fat cells and it becomes adipose tissue. Each fat cell is almost entirely one big droplet, with the nucleus squeezed to one side like a signet ring.") as v:
            B.reveal_table(self, tb, v.dur * 0.5)
            self.play(LaggedStart(*[FadeIn(f_) for f_ in fat], lag_ratio=0.08), FadeIn(fl))
        self.play(FadeOut(VGroup(tb, fat, fl)))
        self.p2_tendon()
        self.p2_bone()
        self.p2_blood()

    def p2_tendon(self):
        head = T("Tendon vs ligament", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        tend = VGroup(*[Line([-6.0, y, 0], [-1.0, y, 0], color=COLL, stroke_width=6) for y in np.linspace(0.6, 1.6, 6)])
        lig = VGroup(*[VMobject(stroke_color=ELAS, stroke_width=3).set_points_smoothly([[x, 1.1 + 0.45 * np.sin(x * 2.4 + k), 0] for x in np.linspace(1.0, 6.0, 30)]) for k in range(5)])
        tl = T("tendon: white collagen, parallel", size=24, color=COLL).move_to([-3.5, 2.3, 0])
        ll = T("ligament: yellow elastic, branching", size=24, color=ELAS).move_to([3.5, 2.3, 0])
        pull = VGroup(Arrow([-1.0, 1.1, 0], [0.2, 1.1, 0], buff=0, color=th.CORAL, stroke_width=5), Arrow([6.0, 1.1, 0], [6.9, 1.1, 0], buff=0, color=th.CORAL, stroke_width=5))
        with self.say("Two dense tissues, always compared. A tendon is packed with parallel bundles of white collagen. Pull it, and it barely stretches. A ligament has branching yellow elastic fibres. Pull it, and it stretches, then springs back."):
            self.play(FadeIn(head), FadeIn(tend), FadeIn(lig), FadeIn(tl), FadeIn(ll))
            self.play(GrowArrow(pull[0]), GrowArrow(pull[1]))
            self.play(tend.animate.stretch(1.02, 0, about_edge=LEFT), lig.animate.stretch(1.18, 0, about_edge=LEFT), run_time=1.0)
            self.play(tend.animate.stretch(1 / 1.02, 0, about_edge=LEFT), lig.animate.stretch(1 / 1.18, 0, about_edge=LEFT), run_time=0.8)
        rows = [["", "tendon", "ligament"], ["fibre", "white collagen", "yellow elastic"], ["arrangement", "parallel bundles", "branching, interlacing"], ["elasticity", "inextensible", "elastic"], ["connects", "muscle to bone", "bone to bone"]]
        tb = B.table(rows, [2.8, 4.0, 4.0], row_h=0.6, size=23, colors=[th.MUTED, COLL, ELAS]).move_to([0, -1.5, 0])
        with self.say("The four marks: fibre, arrangement, elasticity, and what each connects. Tendon: muscle to bone. Ligament: bone to bone at a joint.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(VGroup(head, tend, lig, tl, ll, pull, tb)))

    def p2_bone(self):
        head = T("Cartilage and bone", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cart = RoundedRectangle(corner_radius=0.3, width=5.0, height=3.6, stroke_color="#B8C8FF", stroke_width=5, fill_color="#3A4A78", fill_opacity=0.7).move_to([-3.4, -0.4, 0])
        rng = np.random.default_rng(3)
        lac = VGroup()
        for x, y in zip(rng.uniform(-5.4, -1.4, 9), rng.uniform(-1.8, 0.9, 9)):
            n = rng.integers(1, 3)
            l_ = Ellipse(width=0.55 * n * 0.7 + 0.2, height=0.42, stroke_color="#DDE6FF", stroke_width=2, fill_color="#20263F", fill_opacity=1).move_to([x, y, 0])
            lac.add(VGroup(l_, *[Dot([x + (k - (n - 1) / 2) * 0.22, y, 0], radius=0.08, color=th.SKY) for k in range(n)]))
        cl = T("chondrocytes in lacunae, chondrin matrix", size=22, color=th.SKY).next_to(cart, DOWN, buff=0.2)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.6, size=24)
        with self.say("Cartilage is firm but flexible. Its cells, chondrocytes, sit alone or in twos in little spaces called lacunae, in a matrix of the protein chondrin. It is wrapped in a perichondrium, and it has no blood vessels at all: it is fed only by slow diffusion."):
            self.play(FadeIn(head), FadeIn(cart), LaggedStart(*[FadeIn(l_) for l_ in lac], lag_ratio=0.1), FadeIn(cl))
            cap("Cartilage: avascular", color="#B8C8FF", sub="Hyaline (trachea rings, nose, joint surfaces) · elastic (pinna, epiglottis) · fibrous (intervertebral discs) · calcified.")
        self.play(FadeOut(VGroup(cart, lac, cl)))
        C = np.array([-3.4, -0.4, 0])
        rings = VGroup(*[Circle(radius=0.45 + 0.32 * k, stroke_color="#E8DCC4", stroke_width=2.5).move_to(C) for k in range(6)])
        canal = Circle(radius=0.32, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.8).move_to(C)
        lacs = VGroup()
        cans = VGroup()
        for k in range(5):
            r = 0.61 + 0.32 * k
            n = 6 + 3 * k
            for i in range(n):
                a = TAU * i / n + 0.3 * k
                p = C + polar(r, a)
                lacs.add(Ellipse(width=0.2, height=0.1, stroke_width=0, fill_color="#5A4A30", fill_opacity=1).rotate(a + PI / 2).move_to(p))
                cans.add(Line(p + polar(0.06, a), p + polar(0.15, a), color="#8A7A5A", stroke_width=1.2), Line(p - polar(0.06, a), p - polar(0.15, a), color="#8A7A5A", stroke_width=1.2))
        with self.say("Bone is the hardest connective tissue. Its matrix is about one third protein, for toughness, and two thirds calcium salts, mainly calcium phosphate, for hardness. In mammalian compact bone it is built in cylinders called Haversian systems. A central Haversian canal carries a blood vessel and a nerve."):
            self.play(FadeIn(canal), FadeIn(head))
            cap("Haversian canal", color=th.CORAL, swatch=th.CORAL, sub="Blood vessel, lymph vessel, nerve. Matrix: ossein + calcium phosphate.")
        with self.say("Around it, four to twenty concentric rings of matrix, the lamellae. Between them, the osteocytes in their lacunae, each linked to its neighbours and to the canal by hair fine channels, the canaliculi. Volkmann's canals join neighbouring systems sideways, and the whole bone is wrapped in a periosteum."):
            self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.15))
            cap("Lamellae, lacunae, canaliculi", color="#E8DCC4", swatch="#E8DCC4", sub="Osteocytes talk through canaliculi; Volkmann's canals link systems; periosteum outside.")
            self.play(FadeIn(lacs), Create(cans), run_time=1.8)
        self.play(FadeOut(VGroup(rings, canal, lacs, cans)))
        cap.clear()
        rows = [["", "cartilage", "bone"], ["matrix", "chondrin: flexible", "ossein + Ca salts: rigid"], ["cells", "chondrocytes, 1–4 per lacuna", "osteocytes, 1 per lacuna"], ["canaliculi", "absent", "present"],
                ["blood supply", "none (avascular)", "rich, via Haversian canals"], ["covering", "perichondrium", "periosteum"]]
        tb = B.table(rows, [2.8, 4.6, 4.8], row_h=0.62, size=23, colors=[th.MUTED, "#B8C8FF", "#E8DCC4"]).move_to([0, 0.2, 0])
        with self.say("Cartilage versus bone: matrix, cells, canaliculi, blood supply and covering. That missing blood supply is why a torn knee cartilage heals so much more slowly than a broken bone. And one more favourite: frog bone has no Haversian systems. Those are a feature of mammals.") as v:
            B.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(VGroup(head, tb)))

    def p2_blood(self):
        head = T("Blood: a fluid connective tissue", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        tube = RoundedRectangle(corner_radius=0.3, width=1.1, height=4.0, stroke_color=th.BODY, stroke_width=3).move_to([-5.0, -0.5, 0])
        pl = Rectangle(width=1.0, height=2.15, stroke_width=0, fill_color="#F2D16B", fill_opacity=0.8).move_to([-5.0, 0.38, 0])
        fe = Rectangle(width=1.0, height=1.75, stroke_width=0, fill_color="#B3243A", fill_opacity=0.95).move_to([-5.0, -1.6, 0])
        tl = VGroup(T("plasma 55%", size=22, color="#F2D16B").next_to(pl, RIGHT, buff=0.2), T("formed elements 45%", size=22, color=th.CORAL).next_to(fe, RIGHT, buff=0.2))
        rbc = VGroup(Circle(radius=0.38, stroke_width=0, fill_color="#C0392B", fill_opacity=1), Circle(radius=0.18, stroke_width=0, fill_color="#8E2A1E", fill_opacity=1)).move_to([-1.6, 1.4, 0])
        neu = VGroup(Circle(radius=0.45, stroke_width=0, fill_color="#C9B8FF", fill_opacity=0.6), *[Circle(radius=0.12, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to(polar(0.16, a)) for a in (0, 2.1, 4.2)]).move_to([0.8, 1.4, 0])
        lym = VGroup(Circle(radius=0.36, stroke_width=0, fill_color="#C9B8FF", fill_opacity=0.6), Circle(radius=0.28, stroke_width=0, fill_color=NUCC, fill_opacity=1)).move_to([3.2, 1.4, 0])
        plt = VGroup(*[Dot([5.4 + dx, 1.4 + dy, 0], radius=0.07, color="#E8A0BF") for dx, dy in [(0, 0), (0.2, 0.15), (-0.15, 0.2)]])
        ll = VGroup(*[T(s_, size=20, color=th.BODY).next_to(m_, DOWN, buff=0.15) for s_, m_ in [("RBC: no nucleus", rbc), ("neutrophil: lobed", neu), ("lymphocyte", lym), ("platelets", plt)]])
        rows = [["element", "count per mm³", "job"], ["RBC", "4.5–5.5 million", "carry O₂ and CO₂"], ["WBC (all)", "4,000–11,000", "defence"], ["platelets", "150,000–400,000", "clotting"]]
        tb = B.table(rows, [2.0, 3.0, 3.0], row_h=0.6, size=22, colors=[th.AMBER, th.INK, th.BODY]).move_to([2.7, -1.5, 0])
        with self.say("Blood is a connective tissue whose matrix is a liquid. Spin it down: about fifty five percent is plasma, mostly water with proteins, sugar, salts and hormones, and forty five percent is formed elements. Red cells, biconcave discs with no nucleus in mammals, four and a half to five and a half million in each cubic millimetre. White cells, four to eleven thousand, for defence. And platelets, one hundred and fifty to four hundred thousand, for clotting.") as v:
            self.play(FadeIn(head), FadeIn(tube), FadeIn(pl), FadeIn(fe), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in [rbc, neu, lym, plt]], lag_ratio=0.2), FadeIn(ll))
            B.reveal_table(self, tb, v.dur * 0.4)
        self.play(FadeOut(VGroup(head, tube, pl, fe, tl, rbc, neu, lym, plt, ll, tb)))
        head, prob = B.example_head(self, "Blood is diluted 1 : 200 in a haemocytometer. Each small square is 1/400 mm² and the depth is 0.1 mm. 500 red cells are counted in 80 small squares. Find the RBC count per mm³. Is the person anaemic?", size=25)
        grid = VGroup(*[Square(side_length=0.16, stroke_color=th.MUTED, stroke_width=1) for _ in range(80)]).arrange_in_grid(8, 10, buff=0).move_to([5.6, -2.5, 0])
        rng = np.random.default_rng(2)
        cells = VGroup(*[Dot([5.6 + rng.uniform(-0.75, 0.75), -2.5 + rng.uniform(-0.6, 0.6), 0], radius=0.025, color=th.CORAL) for _ in range(160)])
        steps = VGroup(M(r"V = 80 \times \tfrac{1}{400}\,\text{mm}^2 \times 0.1\,\text{mm} = 0.02\ \text{mm}^3", size=36),
                       M(r"\frac{500}{0.02} = 25\,000 \text{ per mm}^3 \text{ (diluted)}", size=36),
                       M(r"25\,000 \times 200 = 5\times10^6 \text{ per mm}^3 \Rightarrow \text{normal}", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["A counting chamber example. Watch the units.", "The volume over eighty small squares is eighty times one four hundredth of a square millimetre, times zero point one millimetre deep: zero point zero two cubic millimetres.",
                "Five hundred cells in zero point zero two cubic millimetres is twenty five thousand per cubic millimetre of diluted blood.", "Undo the dilution, times two hundred: five million per cubic millimetre. Inside the normal range, so not anaemic."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob), FadeIn(grid), FadeIn(cells))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head, prob, steps, grid, cells)))
        self.quiz("Which is ABSENT in cartilage?",
                  ["lacunae", "chondrocytes", "blood vessels", "perichondrium"], 2,
                  "Pause and think. Which of these does cartilage lack?",
                  "Blood vessels. Cartilage is avascular, fed by diffusion from the perichondrium, which is why it heals slowly. It does have lacunae, chondrocytes, and a perichondrium.")

    # ------------------------------------------------------------------ part 3: muscle
    def p3(self):
        self.section(2)
        sk = VGroup(Rectangle(width=4.0, height=0.8, stroke_color=MYO, stroke_width=3, fill_color=MYO, fill_opacity=0.15),
                    *[Line([x, -0.4, 0], [x, 0.4, 0], color=MYO, stroke_width=2, stroke_opacity=0.7) for x in np.arange(-1.9, 2.0, 0.18)],
                    *[Ellipse(width=0.3, height=0.12, stroke_width=0, fill_color=NUCC, fill_opacity=1).move_to([x, y, 0]) for x, y in [(-1.4, 0.32), (-0.2, -0.32), (1.0, 0.32), (1.7, -0.32)]]).move_to([-3.6, 1.7, 0])
        cd = VGroup(*[Rectangle(width=1.4, height=0.6, stroke_color=MYO, stroke_width=3, fill_color=MYO, fill_opacity=0.15).move_to([x, y, 0]) for x, y in [(-1.0, 0), (0.4, 0), (1.6, 0.6), (1.6, -0.6)]],
                    *[Line([x, -0.3, 0], [x, 0.3, 0], color=MYO, stroke_width=1.6, stroke_opacity=0.6) for x in np.arange(-1.6, 1.0, 0.2)],
                    *[Line([x, -0.32, 0], [x, 0.32, 0], color=th.AMBER, stroke_width=6) for x in (-0.3, 1.1)],
                    *[Dot([x, 0, 0], radius=0.09, color=NUCC) for x in (-1.0, 0.4)]).move_to([-3.6, -0.1, 0])
        sm = VGroup(*[VGroup(Polygon([-1.1, 0, 0], [0, 0.22, 0], [1.1, 0, 0], [0, -0.22, 0], stroke_color=MYO, stroke_width=2.5, fill_color=MYO, fill_opacity=0.15).round_corners(0.08), Ellipse(width=0.35, height=0.1, stroke_width=0, fill_color=NUCC, fill_opacity=1)).move_to([dx, dy, 0])
                    for dx, dy in [(-0.6, 0.25), (0.6, 0.0), (-0.4, -0.25)]]).move_to([-3.6, -1.9, 0])
        names = VGroup(T("striated (skeletal)", size=24, color=MYO, weight="BOLD").next_to(sk, RIGHT, buff=0.3), T("cardiac: branched, intercalated discs", size=24, color=MYO, weight="BOLD").next_to(cd, RIGHT, buff=0.3),
                       T("smooth: spindle, no stripes", size=24, color=MYO, weight="BOLD").next_to(sm, RIGHT, buff=0.3))
        with self.say("Muscle cells, or fibres, are packed with two protein filaments, actin and myosin, that slide to make the cell shorten. There are three kinds. Striated, or skeletal, muscle: long unbranched cylinders, striped, with many nuclei at the edge. It is voluntary, fast, powerful, and it tires."):
            self.play(FadeIn(sk), FadeIn(names[0]))
        with self.say("Cardiac muscle, only in the heart: striped too, but its fibres branch, each has one central nucleus, and neighbouring cells are joined end to end by intercalated discs. It is involuntary, rhythmic, and it never tires."):
            self.play(FadeIn(cd), FadeIn(names[1]))
            self.play(*[Indicate(m_, color=th.AMBER) for m_ in cd[-4:-2]])
        with self.say("And smooth muscle: spindle shaped cells, one central nucleus, no stripes. It is involuntary, slow and steady, in the walls of the gut, the uterus, the blood vessels and the iris."):
            self.play(FadeIn(sm), FadeIn(names[2]))
        self.play(FadeOut(VGroup(sk, cd, sm, names)))
        rows = [["", "striated", "cardiac", "smooth"], ["fibre", "cylindrical, unbranched", "cylindrical, branched", "spindle"], ["striations", "prominent", "faint", "absent"], ["nuclei", "many, peripheral", "one, central", "one, central"],
                ["intercalated discs", "absent", "present", "absent"], ["control", "voluntary", "involuntary", "involuntary"], ["fatigue", "tires quickly", "never tires", "tires slowly"]]
        tb = B.table(rows, [3.0, 3.4, 3.2, 3.0], row_h=0.6, size=22, colors=[th.MUTED, th.INK, th.AMBER, th.INK]).move_to([0, 0.2, 0])
        with self.say("The three way table for the exam: fibre shape, striations, nuclei, intercalated discs, control, and fatigue.") as v:
            B.reveal_table(self, tb, max(2.5, v.dur * 0.9))
        self.wait(1.5)
        self.play(FadeOut(tb))
        self.p3_sarcomere()

    def p3_sarcomere(self):
        head = T("The sarcomere: Z line to Z line", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        s = ValueTracker(1.0)
        Y = 0.4

        def sarc():
            k = s.get_value()
            half = 2.6 * k
            g = VGroup()
            for x in (-half, half):
                g.add(Line([x, Y - 1.1, 0], [x, Y + 1.1, 0], color=WHITE, stroke_width=6))
            act_len = 1.9
            for sign in (-1, 1):
                for yy in (Y - 0.75, Y - 0.25, Y + 0.25, Y + 0.75):
                    x0 = sign * half
                    g.add(Line([x0, yy, 0], [x0 - sign * act_len, yy, 0], color=ACT, stroke_width=4))
            for yy in (Y - 0.5, Y, Y + 0.5):
                g.add(Line([-1.6, yy, 0], [1.6, yy, 0], color=MYO, stroke_width=11))
            g.add(Line([0, Y - 0.9, 0], [0, Y + 0.9, 0], color=MYO, stroke_width=2))
            Ab = BraceBetweenPoints([-1.6, Y - 1.25, 0], [1.6, Y - 1.25, 0], direction=DOWN, color=MYO)
            g.add(Ab, T("A band (constant)", size=20, color=MYO).next_to(Ab, DOWN, buff=0.05))
            il = -half
            ir = -1.6
            if ir - il > 0.15:
                Ib = BraceBetweenPoints([il, Y + 1.25, 0], [ir, Y + 1.25, 0], direction=UP, color=ACT)
                g.add(Ib, T("I band", size=20, color=ACT).next_to(Ib, UP, buff=0.05))
            hl = -half + act_len
            if hl < -0.05:
                Hb = BraceBetweenPoints([hl, Y + 1.25, 0], [-hl, Y + 1.25, 0], direction=UP, color=th.AMBER)
                g.add(Hb, T("H zone", size=20, color=th.AMBER).next_to(Hb, UP, buff=0.05))
            return g

        sg = always_redraw(sarc)
        ln = always_redraw(lambda: VGroup(T("sarcomere", size=22, color=th.MUTED), DecimalNumber(2.4 * s.get_value() * 1.0, num_decimal_places=1, font_size=36, color=th.INK), T("µm", size=22, color=th.MUTED)).arrange(RIGHT, buff=0.15).move_to([0, -2.7, 0]))
        with self.say("Under high power, striated muscle is a stack of repeating units. Between two Z lines lies one sarcomere, the unit of contraction, about two point four micrometres long at rest. Thick myosin filaments sit in the middle and make the dark A band. Thin actin filaments are anchored to the Z lines and make the light I band. The middle of the A band, with myosin only, is the H zone."):
            self.play(FadeIn(head))
            self.add(sg, ln)
            self.wait(2.0)
        with self.say("Now contract. The actin filaments slide in over the myosin, pulling the Z lines together. Watch the bands. The I band shrinks. The H zone shrinks and can vanish. But the A band does not change at all, because the myosin filaments themselves never shorten. They just slide.") as v:
            self.play(s.animate.set_value(0.75), run_time=v.dur * 0.6, rate_func=rate_functions.ease_in_out_sine)
            self.play(s.animate.set_value(1.0), run_time=v.dur * 0.25)
        self.play(FadeOut(VGroup(head)), FadeOut(sg), FadeOut(ln))
        self.remove(sg, ln)
        head, prob = B.example_head(self, "A myofibril is 2.4 cm long with sarcomeres of 2.4 µm at rest. (a) How many sarcomeres? (b) If each shortens to 1.8 µm, what is the new length and the percentage shortening?", size=25)
        steps = VGroup(M(r"2.4\text{ cm} = 24\,000\ \mu\text{m};\quad n = \frac{24\,000}{2.4} = 10\,000", size=38), M(r"10\,000 \times 1.8\ \mu\text{m} = 18\,000\ \mu\text{m} = 1.8 \text{ cm}", size=38),
                       M(r"\frac{2.4 - 1.8}{2.4} \times 100 = 25\%", size=40, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["A worked example.", "Put everything in micrometres. Two point four centimetres is twenty four thousand micrometres, so there are ten thousand sarcomeres in a row.",
                "Each shrinks to one point eight micrometres: eighteen thousand micrometres, one point eight centimetres.", "A shortening of twenty five percent. Each sarcomere moves only zero point six micrometres, but ten thousand in series add up to a movement you can see."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("During contraction of a sarcomere, the band whose length does NOT change is the",
                  ["I band", "H zone", "A band", "distance between Z lines"], 2,
                  "Pause and think. Which band stays the same length?",
                  "The A band, because it is exactly the length of the myosin filaments, and they never shorten. The I band and H zone both shrink as actin slides in, and the Z lines move closer together.")

    # ------------------------------------------------------------------ part 4: nervous tissue
    def p4(self):
        self.section(3)
        cy = Circle(radius=0.8, stroke_color=AXON, stroke_width=3, fill_color="#3A2A55", fill_opacity=1).move_to([-4.6, 0.2, 0])
        nuc = Circle(radius=0.28, stroke_width=0, fill_color="#9C7CCF", fill_opacity=1).move_to(cy)
        nis = VGroup(*[Dot(cy.get_center() + polar(0.55, a), radius=0.05, color=th.SKY) for a in np.linspace(0, TAU, 12, endpoint=False)])
        rng = np.random.default_rng(1)
        den = VGroup()
        for a in [1.6, 2.3, 3.0, 3.8, 4.5]:
            base = cy.get_center() + polar(0.8, a)
            tip = base + polar(1.0, a)
            den.add(Line(base, tip, color=AXON, stroke_width=4), *[Line(tip, tip + polar(0.45, a + d), color=AXON, stroke_width=2.5) for d in (-0.5, 0.5)])
        ax_y = 0.2
        axon = Line([-3.8, ax_y, 0], [4.4, ax_y, 0], color=AXON, stroke_width=5)
        myel = VGroup(*[RoundedRectangle(corner_radius=0.15, width=1.2, height=0.5, stroke_width=0, fill_color=MYEL, fill_opacity=0.55).move_to([-3.0 + 1.4 * k + 0.6, ax_y, 0]) for k in range(5)])
        nodes = [-3.0 + 1.4 * k + 1.3 for k in range(5)]
        tel = VGroup(*[VGroup(Line([4.4, ax_y, 0], [5.4, ax_y + d, 0], color=AXON, stroke_width=3), Dot([5.4, ax_y + d, 0], radius=0.12, color=th.AMBER)) for d in (-0.6, 0, 0.6)])
        cap = B.Captions(self, at=(0, -2.5, 0), width=12.4, size=24)
        with self.say("Nervous tissue is built from neurons, which carry messages, and the more numerous neuroglia, which support, insulate and protect them. A typical motor neuron has a cell body, the cyton, with its nucleus and dark patches of rough endoplasmic reticulum, the Nissl granules."):
            self.play(FadeIn(cy), FadeIn(nuc), FadeIn(nis))
            cap("Cyton (cell body): nucleus + Nissl granules (rough ER), no centriole", color=AXON)
        with self.say("Short branched dendrites carry impulses towards the cyton. One long axon carries them away, ending in fine branches, the telodendria, tipped with synaptic knobs."):
            self.play(LaggedStart(*[Create(d_) for d_ in den], lag_ratio=0.05))
            self.play(Create(axon), FadeIn(tel))
            cap("Dendrites carry TO the cyton · the axon carries AWAY · telodendria end in synaptic knobs", color=AXON)
        with self.say("In many neurons the axon is wrapped in a fatty myelin sheath, made by Schwann cells. The sheath is broken every millimetre or so, at the nodes of Ranvier."):
            self.play(LaggedStart(*[FadeIn(m_) for m_ in myel], lag_ratio=0.15))
            cap("Myelin sheath (Schwann cells) · gaps = nodes of Ranvier · neurilemma outside", color=MYEL)
        imp = Dot([-3.8, ax_y + 0.0, 0], radius=0.13, color=th.CORAL)
        with self.say("And here is why it matters. The impulse cannot travel under the insulating myelin. It jumps from node to node: saltatory conduction. That makes a myelinated fibre up to a hundred times faster."):
            self.add(imp)
            for x in nodes:
                self.play(imp.animate.move_to([x, ax_y + 0.0, 0]), run_time=0.25, rate_func=rate_functions.rush_into)
                self.play(Flash(imp, color=th.CORAL, line_length=0.15), run_time=0.25)
            self.play(imp.animate.move_to([4.4, ax_y, 0]), run_time=0.3)
            cap("Saltatory conduction: node to node, up to ~120 m/s", color=th.CORAL)
        self.play(FadeOut(VGroup(cy, nuc, nis, den, axon, myel, tel, imp)))
        cap.clear()
        race = VGroup(T("myelinated", size=24, color=th.MINT).move_to([-5.2, 1.0, 0]), T("non-myelinated", size=24, color=th.CORAL).move_to([-5.2, -0.6, 0]))
        l1 = Line([-4.0, 1.0, 0], [5.6, 1.0, 0], color=th.MUTED, stroke_width=3)
        l2 = Line([-4.0, -0.6, 0], [5.6, -0.6, 0], color=th.MUTED, stroke_width=3)
        d1 = Dot([-4.0, 1.0, 0], radius=0.14, color=th.MINT)
        d2 = Dot([-4.0, -0.6, 0], radius=0.14, color=th.CORAL)
        with self.say("Race them over the same distance. Myelinated, eighty five metres per second, is across in a flash. Non myelinated, half a metre per second, is still crawling."):
            self.play(FadeIn(race), Create(l1), Create(l2), FadeIn(d1), FadeIn(d2))
            self.play(d1.animate.move_to([5.6, 1.0, 0]), d2.animate.move_to([-3.95, -0.6, 0]), run_time=0.8, rate_func=rate_functions.linear)
            self.play(d2.animate.move_to([-3.5, -0.6, 0]), run_time=2.5, rate_func=rate_functions.linear)
        self.play(FadeOut(VGroup(race, l1, l2, d1, d2)))
        head, prob = B.example_head(self, "Stepping on a thorn: sensory path 0.90 m, motor path 0.80 m, both myelinated at 85 m/s, with 2 synapses of 0.5 ms each. (a) Total reflex time? (b) The same journey along a bare fibre at 0.5 m/s?", size=25)
        steps = VGroup(M(r"t = \frac{0.90 + 0.80}{85} = \frac{1.70}{85} = 0.020\text{ s} = 20\text{ ms}", size=38), M(r"+\ 2 \times 0.5\text{ ms} = 21\text{ ms} = 0.021\text{ s}", size=38),
                       M(r"\text{bare: } \frac{1.70}{0.5} = 3.4\text{ s} \ \ (\approx 160\times \text{ slower})", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["Now the cold open, solved.", "The nerve path is one point seven metres. At eighty five metres per second that takes zero point zero two seconds: twenty milliseconds.",
                "Add two synaptic delays of half a millisecond each: twenty one milliseconds.", "Along a bare fibre at half a metre per second: three point four seconds. About a hundred and sixty times slower. The myelin is the difference between a scratch and a deep wound."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        nb = B.neby_in(self, "success", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, prob, steps)))
        knob = Circle(radius=1.2, stroke_color=AXON, stroke_width=4, fill_color="#3A2A55", fill_opacity=1).move_to([-2.0, 0.3, 0])
        post = Rectangle(width=3.0, height=3.2, stroke_color="#9C8CFF", stroke_width=4, fill_color="#2A2A55", fill_opacity=1).move_to([1.9, 0.3, 0])
        ves = VGroup(*[Circle(radius=0.14, stroke_color=th.AMBER, stroke_width=2).move_to([-2.0 + dx, 0.3 + dy, 0]) for dx, dy in [(-0.4, 0.4), (0.2, 0.5), (0.5, 0.0), (-0.3, -0.3), (0.3, -0.5), (0.7, 0.4)]])
        rec = VGroup(*[Rectangle(width=0.12, height=0.3, stroke_width=0, fill_color=th.MINT, fill_opacity=1).move_to([0.42, 0.3 + y, 0]) for y in (-0.9, -0.3, 0.3, 0.9)])
        cl = T("cleft ~20 nm", size=22, color=th.MUTED).move_to([-0.4, 2.2, 0])
        cap = B.Captions(self, at=(0, -2.6, 0), width=12.4, size=24)
        with self.say("Where one neuron meets the next is a synapse. The membranes never touch: a gap of about twenty nanometres, the synaptic cleft, separates them. When an impulse reaches the knob, vesicles release a chemical, the neurotransmitter, such as acetylcholine."):
            self.play(FadeIn(knob), FadeIn(post), FadeIn(ves), FadeIn(rec), FadeIn(cl))
            cap("Synaptic knob · cleft · postsynaptic membrane with receptors")
        mol = VGroup(*[Dot([-0.9, 0.3 + y, 0], radius=0.05, color=th.AMBER) for y in np.linspace(-1.0, 1.0, 12)])
        with self.say("It diffuses across the cleft, binds receptors on the next cell, and starts a new impulse there. An enzyme, cholinesterase, then destroys it. Because the vesicles are only on one side and the receptors only on the other, a synapse works in one direction only."):
            self.play(*[v_.animate.move_to([-0.85, v_.get_center()[1], 0]) for v_ in ves], run_time=0.8)
            self.play(FadeIn(mol), FadeOut(ves))
            self.play(*[m_.animate.shift(RIGHT * 1.15) for m_ in mol], run_time=1.0)
            self.play(Flash(rec, color=th.MINT))
            cap("Chemical transmission: one-way, because vesicles are presynaptic and receptors postsynaptic", color=th.MINT)
        self.play(FadeOut(VGroup(knob, post, rec, cl, mol)))
        cap.clear()
        kinds = VGroup(*[para(s_, width=12.0, size=24, color=th.INK) for s_ in ["unipolar (one process) · bipolar (retina, olfactory) · multipolar (brain, cord: the commonest)", "sensory (afferent) · motor (efferent) · interneurons",
                                                                  "neuroglia: astrocytes (blood–brain barrier), oligodendrocytes (myelin in the CNS), microglia (phagocytes), ependymal cells (CSF)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for k_ in kinds:
            if k_.width > 12.6:
                k_.scale_to_fit_width(12.6)
        kinds.move_to([0, 0.3, 0])
        with self.say("Neurons are named by their processes: unipolar, bipolar as in the retina, and multipolar, the commonest. By job: sensory, motor and interneurons. And the neuroglia: astrocytes, which help form the blood brain barrier; oligodendrocytes, which make myelin inside the brain and spinal cord; microglia, the nervous system's phagocytes; and ependymal cells, which line the ventricles.") as v:
            for k_ in kinds:
                self.play(FadeIn(k_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.25)
        self.play(FadeOut(kinds))
        self.tip("Myelin sheath = fatty insulation made by the Schwann cell. Neurilemma = the Schwann cell's thin outer membrane, OUTSIDE the myelin. Non-myelinated fibres still have a neurilemma.",
                 "Exam tip. Do not mix up the two sheaths. The myelin sheath is the fatty insulation made by the Schwann cell. The neurilemma is the Schwann cell's own thin outer membrane, outside the myelin. Non myelinated fibres still have a neurilemma; they just have no myelin and no nodes.", width=8.6)
        self.quiz("Nissl granules are ABSENT from the",
                  ["cyton", "dendrite", "axon", "region round the nucleus"], 2,
                  "Pause and think. Where will you never find Nissl granules?",
                  "In the axon. Nissl granules are found in the cyton and the dendrites, and their absence from the axon is exactly how you tell an axon from a dendrite under the microscope.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Epithelium: packed cells on a basement membrane, avascular; simple, compound, glandular.",
            "Connective: few cells, much matrix; collagen and elastic fibres.",
            "Tendon (collagen, muscle→bone) vs ligament (elastic, bone→bone).",
            "Cartilage avascular; bone has Haversian systems (in mammals). Blood: 55% plasma.",
            "Muscle: striated, cardiac (intercalated discs), smooth. A band constant in contraction.",
            "Neuron: dendrites in, axon out; myelin → saltatory conduction; synapse one-way.",
        ], "Quick recap. Epithelium is packed cells on a basement membrane, with no blood vessels. Connective tissue is few cells in a lot of matrix. Tendons are collagen and join muscle to bone; ligaments are elastic and join bone to bone. Cartilage has no blood supply; mammalian bone has Haversian systems. Muscle is striated, cardiac or smooth, and in a contracting sarcomere the A band stays the same. And in a neuron, dendrites bring impulses in, the axon carries them out, myelin makes them jump, and the synapse is one way.")
        self.outro("That was animal tissues. Next, developmental biology: how sperm and eggs are made, and how a frog's egg becomes a tadpole. See you there.")
