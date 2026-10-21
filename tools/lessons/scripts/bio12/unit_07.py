import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402

P2 = "#7BE495"
P1 = "#C77DFF"
ECTO = "#4CC9F0"
MESO = "#FF6B6B"
ENDO = "#FFD166"
YOLK = "#F3E3B0"
DARK = "#3A3550"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


def chip(txt, col):
    r = RoundedRectangle(corner_radius=0.1, width=0.75, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.9)
    return VGroup(r, T(txt, size=20, color="#0B0E1A", weight="BOLD").move_to(r))


def gcell(r, col, label=None):
    g = VGroup(Circle(radius=r, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.22), Dot(radius=max(0.05, r * 0.25), color=col))
    return g


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 7
    TITLE = "Developmental Biology"
    SUBTITLE = "From one cell to a frog"
    SECTIONS = ["Gametogenesis", "Frog: fertilisation and cleavage", "Frog: gastrulation to metamorphosis"]
    NEXT = "Unit 8 · Human Biology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        rng = np.random.default_rng(3)
        eggs = VGroup(*[VGroup(Circle(radius=0.32, stroke_color=WHITE, stroke_width=1.5, fill_color=WHITE, fill_opacity=0.12),
                               Circle(radius=0.14, stroke_width=0, fill_color=DARK, fill_opacity=1)).move_to([x, y, 0])
                        for x, y in zip(rng.uniform(-5.5, 5.5, 26), rng.uniform(-2.4, 2.4, 26))])
        cnt = VGroup(T("eggs laid", size=24, color=th.MUTED), Integer(2800, font_size=60, color=th.AMBER)).arrange(DOWN, buff=0.08).move_to([0, 2.6, 0])
        with self.say("A monsoon night in a paddy field. A single female frog lays about two thousand eight hundred eggs in a floating mass of jelly. Each one is a single cell, about two millimetres across."):
            self.play(LaggedStart(*[FadeIn(e_, scale=0.5) for e_ in eggs], lag_ratio=0.04), FadeIn(cnt))
        stages = [("fertilised", 2380), ("tadpoles", 1428), ("adult frogs", 43)]
        with self.say("Most will never make it. About eighty five percent are fertilised. Sixty percent of those hatch. And of the tadpoles, only three in a hundred survive to become frogs. Forty three adults, from two thousand eight hundred eggs.") as v:
            for (n_, k_) in stages:
                keep = max(1, int(len(eggs) * k_ / 2800))
                self.play(cnt[1].animate.set_value(k_), Transform(cnt[0], T(n_, size=24, color=th.MUTED).move_to(cnt[0])), *[e_.animate.set_opacity(0.08) for e_ in eggs[keep:]], run_time=max(0.8, v.dur * 0.28))
        with self.say("Yet every survivor turned one cell into a whole animal, with a brain, a heart and legs. How? That is developmental biology."):
            nb = B.neby_in(self, "think", height=1.4)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(eggs, cnt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 7: Developmental Biology. How sperm and eggs are made, and how a frog's egg becomes a frog."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Three parts. Gametogenesis: how sperm and eggs are made, with the chromosome number at every step. Then the frog: fertilisation and cleavage. And finally gastrulation, the three germ layers, and the tadpole's metamorphosis.")

    # ------------------------------------------------------------------ part 1: gametogenesis
    def p1(self):
        self.section(0)
        d = self.callout("key", "Gametogenesis: diploid germ cells in the gonad become haploid gametes. Spermatogenesis in the testis, oogenesis in the ovary. Three phases: multiplication (mitosis) → growth → maturation (meiosis I and II).", width=11, size=27)
        with self.say("Gametogenesis turns diploid germ cells into haploid gametes: spermatogenesis in the testis, oogenesis in the ovary. Both run through three phases. Multiplication, by mitosis. Growth. And maturation, two meiotic divisions that halve the chromosome number."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        head = T("One primary cell, two very different outcomes", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        Lx, Rx = -2.1, 2.1
        ys = [1.55, 0.45, -0.65, -1.75]
        sp = [VGroup(gcell(0.3, P2)).move_to([Lx, ys[0], 0]), VGroup(gcell(0.36, P2)).move_to([Lx, ys[1], 0]),
              VGroup(*[gcell(0.28, P1).move_to([Lx + d, ys[2], 0]) for d in (-0.45, 0.45)]), VGroup(*[gcell(0.2, P1).move_to([Lx + d, ys[3], 0]) for d in (-0.9, -0.3, 0.3, 0.9)])]
        oo = [VGroup(gcell(0.3, P2)).move_to([Rx, ys[0], 0]), VGroup(gcell(0.5, P2)).move_to([Rx, ys[1], 0]),
              VGroup(gcell(0.42, P1).move_to([Rx - 0.2, ys[2], 0]), gcell(0.1, P1).move_to([Rx + 0.5, ys[2] + 0.2, 0])),
              VGroup(gcell(0.4, P1).move_to([Rx - 0.4, ys[3], 0]), *[gcell(0.09, P1).move_to([Rx + d, ys[3] + 0.15, 0]) for d in (0.3, 0.6, 0.9)])]
        names_l = ["spermatogonium", "primary spermatocyte", "2 secondary spermatocytes", "4 spermatids → 4 sperms"]
        names_r = ["oogonium", "primary oocyte (huge: yolk)", "secondary oocyte + 1st polar body", "1 ovum + 3 polar bodies"]
        ploid = ["2n", "2n", "n", "n"]
        lab_l = VGroup(*[para(n_, width=2.5, size=19, color=th.BODY, align="center").next_to(sp[i], LEFT, buff=0.25) for i, n_ in enumerate(names_l)])
        lab_r = VGroup(*[para(n_, width=2.5, size=19, color=th.BODY, align="center").next_to(oo[i], RIGHT, buff=0.25) for i, n_ in enumerate(names_r)])
        chips = VGroup(*[chip(p_, P2 if p_ == "2n" else P1).move_to([0, ys[i], 0]) for i, p_ in enumerate(ploid)])
        steps_ = ["mitosis, then growth", "meiosis I (reductional)", "meiosis II (equational)"]
        st = VGroup(*[T(s_, size=18, color=th.AMBER).move_to([0, (ys[i] + ys[i + 1]) / 2, 0]) for i, s_ in enumerate(steps_)])
        hl = VGroup(T("testis", size=26, color=th.SKY, weight="BOLD").move_to([Lx, 2.25, 0]), T("ovary", size=26, color=th.PINK, weight="BOLD").move_to([Rx, 2.25, 0]))
        with self.say("Side by side. A diploid spermatogonium and a diploid oogonium multiply by mitosis. One grows into a primary spermatocyte, or a primary oocyte, still diploid. In the female the growth is enormous, because the oocyte stocks up yolk and machinery for the embryo."):
            self.play(FadeIn(head), FadeIn(hl))
            self.play(FadeIn(sp[0]), FadeIn(oo[0]), FadeIn(lab_l[0]), FadeIn(lab_r[0]), FadeIn(chips[0]))
            self.play(FadeIn(st[0]), TransformFromCopy(sp[0], sp[1]), TransformFromCopy(oo[0], oo[1]), FadeIn(lab_l[1]), FadeIn(lab_r[1]), FadeIn(chips[1]))
        with self.say("Meiosis one is the reduction division: two n to n. In the male it gives two equal secondary spermatocytes. In the female the split is wildly unequal: one big secondary oocyte, and one tiny first polar body."):
            self.play(FadeIn(st[1]), TransformFromCopy(sp[1], sp[2]), TransformFromCopy(oo[1], oo[2]), FadeIn(lab_l[2]), FadeIn(lab_r[2]), FadeIn(chips[2]))
        with self.say("Meiosis two. The male makes four spermatids, which are remodelled into four sperms by spermiogenesis. The female makes one ovum and another polar body, and the first polar body may divide too: one ovum and three polar bodies, which soon die."):
            self.play(FadeIn(st[2]), TransformFromCopy(sp[2], sp[3]), TransformFromCopy(oo[2], oo[3]), FadeIn(lab_l[3]), FadeIn(lab_r[3]), FadeIn(chips[3]))
            self.sfx("pop", gain=-12)
        self.play(FadeOut(VGroup(head, hl, *sp, *oo, lab_l, lab_r, chips, st)))
        w = self.callout("careful", "Both sexes do exactly two meiotic divisions and make four haploid nuclei. The difference is the cytoplasm: in the female it all goes to ONE cell; the other three nuclei leave as polar bodies.", width=11)
        with self.say("Careful: the maths is the same in both sexes. Two meiotic divisions, four haploid nuclei. The difference is the cytoplasm. In the female nearly all of it goes into one cell, so the egg can feed the early embryo."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(w))
        rows = [["", "spermatogenesis", "oogenesis"], ["site", "seminiferous tubules", "ovary"], ["begins", "puberty, continues for life", "in the foetus; arrested, resumed at puberty"], ["growth phase", "slight", "enormous: yolk"],
                ["meiotic division", "equal", "unequal: polar bodies"], ["from one primary cell", "4 sperms", "1 ovum + 3 polar bodies"], ["extra phase", "spermiogenesis", "none"]]
        tb = B.table(rows, [3.2, 4.4, 5.2], row_h=0.6, size=22, colors=[th.MUTED, th.SKY, th.PINK]).move_to([0, 0.2, 0])
        with self.say("The comparison table: site, when it begins, the growth phase, how the cytoplasm is divided, the products, and the extra phase in males.") as v:
            B.reveal_table(self, tb, max(2.5, v.dur * 0.9))
        self.wait(1.5)
        self.play(FadeOut(tb))
        head, prob = B.example_head(self, "Rana tigrina has 2n = 26. Give the chromosomes and chromatids in (a) a primary spermatocyte at prophase I, (b) a secondary spermatocyte, (c) a spermatid. (d) A G₁ spermatogonium has 6.0 pg of DNA: how much in a sperm?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 26 \text{ chromosomes},\ 26\times2 = 52 \text{ chromatids (DNA already copied)}", size=34),
                       M(r"\text{(b)}\ \ 13 \text{ chromosomes},\ 26 \text{ chromatids}", size=34), M(r"\text{(c)}\ \ 13 \text{ chromosomes},\ 13 \text{ chromatids}", size=34),
                       M(r"\text{(d)}\ \ 6.0 \div 2 = 3.0 \text{ pg; the zygote is back to } 6.0 \text{ pg and } 2n = 26", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        for s_ in steps:
            if s_.width > 12.4:
                s_.scale_to_fit_width(12.4).align_to(prob, LEFT)
        says = ["A worked example that catches many students.", "At prophase one the DNA has already been copied. Still twenty six chromosomes, but each has two chromatids: fifty two.",
                "Meiosis one separates the pairs: thirteen chromosomes, each still with two chromatids, twenty six chromatids.", "Meiosis two separates the sister chromatids: thirteen chromosomes of one chromatid each.",
                "And a sperm carries half the G one amount of DNA: three picograms. Add the egg's three, and the zygote is back to six, and to twenty six chromosomes."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head, prob, steps)))
        head, prob = B.example_head(self, "A frog has 500 primary spermatocytes and 600 primary oocytes, all completing gametogenesis. (a) Sperms and ova formed? (b) Polar bodies? (c) What percentage of the haploid nuclei made in the ovary can be fertilised?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 500\times4 = 2000 \text{ sperms},\quad 600\times1 = 600 \text{ ova}", size=36), M(r"\text{(b)}\ \ 600\times3 = 1800 \text{ polar bodies}", size=36),
                       M(r"\text{(c)}\ \ \tfrac14 \times 100 = 25\%", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["One more.", "Four sperms per spermatocyte: two thousand. One ovum per oocyte: six hundred.", "Three polar bodies per oocyte: one thousand eight hundred.", "And only one in four of the female's haploid nuclei is usable: twenty five percent, against a hundred percent in the male. But each egg is stocked for the first days of life."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.2)
        self.play(FadeOut(VGroup(head, prob, steps)))
        egg = VGroup(Circle(radius=1.5, stroke_color=WHITE, stroke_width=2, fill_color=YOLK, fill_opacity=0.9),
                     AnnularSector(inner_radius=0, outer_radius=1.5, angle=PI, start_angle=0, stroke_width=0, fill_color=DARK, fill_opacity=1),
                     Dot([0, 0.7, 0], radius=0.15, color=WHITE)).move_to([-3.4, 0.0, 0])
        el = VGroup(T("animal pole: pigment, nucleus", size=22, color=th.INK).next_to(egg, UP, buff=0.15), T("vegetal pole: yolk", size=22, color=YOLK).next_to(egg, DOWN, buff=0.15))
        rows = [["type", "yolk", "example"], ["alecithal", "none", "human"], ["microlecithal", "little, even", "Amphioxus"], ["mesolecithal", "moderate, at one pole", "FROG"], ["macrolecithal", "huge, at one pole", "hen"], ["centrolecithal", "in the centre", "insects"]]
        tb = B.table(rows, [2.6, 3.0, 2.0], row_h=0.56, size=21, colors=[th.AMBER, th.INK, th.BODY]).move_to([2.8, -0.1, 0])
        with self.say("The frog's egg is mesolecithal, with a moderate amount of yolk, and telolecithal, with that yolk pushed to one end. The dark animal pole holds the nucleus and most of the cytoplasm; the pale vegetal pole holds the yolk. Eggs are classified on exactly these two features: how much yolk, and where.") as v:
            self.play(FadeIn(egg), FadeIn(el))
            B.reveal_table(self, tb, v.dur * 0.6)
        self.play(FadeOut(VGroup(egg, el, tb)))
        self.quiz("The number of functional gametes formed from one primary oocyte is",
                  ["one", "two", "three", "four"], 0,
                  "Pause and think. One primary oocyte. How many usable eggs?",
                  "One. The two meiotic divisions do make four haploid nuclei, which is the trap, but three of them leave as polar bodies with almost no cytoplasm, and they cannot be fertilised.")

    # ------------------------------------------------------------------ part 2: fertilisation and cleavage
    def p2(self):
        self.section(1)
        C = np.array([-2.8, -0.2, 0])
        rot = ValueTracker(0.0)
        mem = ValueTracker(1.8)

        def egg():
            a = rot.get_value()
            g = VGroup(Circle(radius=1.8, stroke_width=0, fill_color=YOLK, fill_opacity=0.95).move_to(C),
                       AnnularSector(inner_radius=0, outer_radius=1.8, angle=PI, start_angle=a, stroke_width=0, fill_color=DARK, fill_opacity=1, arc_center=C))
            g.add(Circle(radius=mem.get_value(), stroke_color=WHITE, stroke_width=2).move_to(C))
            return g

        eg = always_redraw(egg)
        sperm = VGroup(Ellipse(width=0.3, height=0.16, stroke_width=0, fill_color=th.SKY, fill_opacity=1), VMobject(stroke_color=th.SKY, stroke_width=2).set_points_smoothly([[0.15, 0, 0], [0.5, 0.1, 0], [0.8, -0.08, 0], [1.1, 0.05, 0]]))
        sperm.rotate(PI * 0.15).move_to(C + polar(3.2, PI * 0.15))
        cap = B.Captions(self, at=(3.6, 0.2, 0), width=5.4, size=25)
        with self.say("Frogs mate in amplexus: the male clasps the female, she sheds her eggs into the water, and he sheds sperm over them at once. Fertilisation is external."):
            self.add(eg)
            self.play(FadeIn(sperm))
            cap("External fertilisation in amplexus", sub="2,500 to 3,000 eggs in a mass of jelly.")
        with self.say("The moment a sperm touches the egg, the egg reacts. The vitelline membrane lifts away from the surface as a fertilisation membrane, which no second sperm can cross. So fertilisation is monospermic."):
            self.play(sperm.animate.move_to(C + polar(1.85, PI * 0.15)), run_time=1.0)
            self.play(mem.animate.set_value(2.05), run_time=1.0)
            cap("Fertilisation membrane lifts", color=WHITE, sub="Blocks other sperms: monospermic.")
        gc_ = always_redraw(lambda: AnnularSector(inner_radius=1.3, outer_radius=1.8, angle=0.9, start_angle=PI + rot.get_value() - 0.9 + 0.0, stroke_width=0, fill_color="#9A97A8", fill_opacity=0.95).move_arc_center_to(C) if rot.get_value() > 0.05 else VGroup())
        with self.say("Then the pigmented outer layer of the egg rotates, about thirty degrees, towards the point where the sperm entered. On the opposite side it uncovers a pale crescent of cytoplasm: the grey crescent."):
            self.add(gc_)
            self.play(rot.animate.set_value(PI / 6), FadeOut(sperm), run_time=2.0)
            cap("The grey crescent, opposite the sperm's entry", color="#C9C6D6", swatch="#9A97A8", sub="It will become the dorsal lip of the blastopore and fixes the body axis.")
        with self.say("Remember that grey crescent. It marks the future back of the frog, and fixes its whole body axis. Finally the sperm's pronucleus, with thirteen chromosomes, fuses with the egg's, also thirteen: a diploid zygote of twenty six."):
            self.play(Indicate(gc_, color=WHITE))
        self.play(FadeOut(eg), FadeOut(gc_))
        self.remove(eg, gc_)
        cap.clear()
        d = self.callout("key", "Cleavage: rapid mitotic divisions of the zygote with NO growth in between. The blastomeres get smaller each time; the embryo stays the same size.", width=11, size=27)
        with self.say("Then comes cleavage: rapid mitotic divisions with no growth in between. The cells, called blastomeres, get smaller each time, while the embryo as a whole stays the same size."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        C = np.array([-3.0, -0.2, 0])
        R = 1.7
        base = VGroup(Circle(radius=R, stroke_width=0, fill_color=YOLK, fill_opacity=0.95).move_to(C), AnnularSector(inner_radius=0, outer_radius=R, angle=PI, start_angle=0, stroke_width=0, fill_color=DARK, fill_opacity=1).move_arc_center_to(C))
        out = Circle(radius=R, stroke_color=WHITE, stroke_width=3).move_to(C)
        f1 = Line(C + UP * R, C + DOWN * R, color=WHITE, stroke_width=4)
        f2 = Ellipse(width=0.9, height=2 * R, stroke_color=WHITE, stroke_width=3).move_to(C)
        f3 = Line(C + polar(R, np.arcsin(0.35)) + LEFT * 0.0, C + polar(R, PI - np.arcsin(0.35)), color=WHITE, stroke_width=4)
        cnt = VGroup(T("blastomeres", size=22, color=th.MUTED), Integer(1, font_size=56, color=th.AMBER)).arrange(DOWN, buff=0.08).move_to([1.0, 2.0, 0])
        cap = B.Captions(self, at=(3.6, -0.2, 0), width=5.4, size=24)
        with self.say("The first furrow is vertical, running through both poles and cutting the grey crescent in half: two equal cells. About an hour after fertilisation."):
            self.play(FadeIn(base), Create(out), FadeIn(cnt))
            self.play(Create(f1), cnt[1].animate.set_value(2))
            cap("1st: vertical, through both poles", sub="Bisects the grey crescent: 2 equal blastomeres.")
        with self.say("The second is also vertical, at right angles to the first: four equal cells."):
            self.play(Create(f2), cnt[1].animate.set_value(4))
            cap("2nd: vertical, at right angles", sub="4 equal blastomeres.")
        with self.say("The third is horizontal, but above the equator, because the yolk below resists the furrow. So the four cells on top are small micromeres, and the four below are big yolky macromeres. The cleavage cuts right through the egg, so it is holoblastic, but the cells are unequal."):
            self.play(Create(f3), cnt[1].animate.set_value(8))
            cap("3rd: horizontal, ABOVE the equator", color=th.AMBER, sub="4 micromeres + 4 macromeres: holoblastic but unequal.")
        with self.say("Then sixteen cells, thirty two, and a solid ball called the morula. The number of cells doubles every time: after n divisions, two to the n.") as v:
            cap("Then 16, 32 … a solid morula", color=th.AMBER, sub="After n cleavages: 2ⁿ blastomeres, and no growth.")
            for k in range(4, 8):
                self.play(cnt[1].animate.set_value(2 ** k), run_time=max(0.4, v.dur * 0.15))
        self.play(FadeOut(VGroup(base, out, f1, f2, f3, cnt)))
        cap.clear()
        head, prob = B.example_head(self, "A frog's egg is 1.8 mm across. After 7 synchronous cleavages with no change in total volume, (a) how many blastomeres? (b) the diameter of one? (c) What does this show?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 2^7 = 128", size=38), M(r"\text{(b)}\ \ V \propto d^3:\ \ \frac{d_{cell}}{d_{egg}} = \left(\tfrac{1}{128}\right)^{1/3} = \frac{1}{5.04};\ \ d = \frac{1.8}{5.04} \approx 0.36\text{ mm}", size=36),
                       M(r"\text{(c)}\ \ 128\times \text{ the cells, same } 1.8\text{ mm: division without growth}", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["A worked example on cleavage.", "Seven doublings: two to the seven, one hundred and twenty eight cells.",
                "Each has one one hundred and twenty eighth of the volume. Diameter goes as the cube root of volume, so the cell is five point zero four times smaller across: about zero point three six millimetres.",
                "A hundred and twenty eight times the cells, but the embryo is still one point eight millimetres across. Nothing new has been made: the same cytoplasm has been cut into smaller boxes."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head, prob, steps)))
        C = np.array([-3.0, -0.3, 0])
        roof = VGroup(*[Circle(radius=0.18, stroke_color=WHITE, stroke_width=1.5, fill_color=DARK, fill_opacity=1).move_to(C + polar(rr, a)) for rr in (1.55, 1.2) for a in np.linspace(0.15, PI - 0.15, 12 if rr > 1.4 else 9)])
        floor = VGroup(*[Circle(radius=0.32, stroke_color=WHITE, stroke_width=1.5, fill_color=YOLK, fill_opacity=0.95).move_to(C + [x, y, 0]) for x in np.linspace(-1.2, 1.2, 5) for y in (-0.5, -1.1) if x * x + y * y < 2.2])
        cav = Ellipse(width=2.0, height=1.1, stroke_color=th.SKY, stroke_width=2, fill_color=th.SKY, fill_opacity=0.15).move_to(C + UP * 0.4)
        cl = T("blastocoel: pushed up by the yolk", size=22, color=th.SKY).move_to([2.6, 1.2, 0])
        bl = para("Coeloblastula: a roof of small micromeres, a thick floor of yolky macromeres, an ECCENTRIC cavity.", width=5.4, size=22, color=th.INK).move_to([2.8, -0.6, 0])
        with self.say("By about thirty two cells, a fluid filled cavity appears inside: the blastocoel. The embryo is now a hollow ball, a blastula. The heavy yolky macromeres crowd the bottom, so the cavity is pushed up into the animal half. It is eccentric."):
            self.play(FadeIn(floor), FadeIn(roof))
            self.play(FadeIn(cav), FadeIn(cl))
            self.play(FadeIn(bl))
        self.play(FadeOut(VGroup(roof, floor, cav, cl, bl)))
        self.quiz("The grey crescent of the frog's egg appears",
                  ["at the point of sperm entry", "opposite the point of sperm entry", "at the vegetal pole", "all round the equator"], 1,
                  "Pause and think. Where does the grey crescent appear?",
                  "Opposite the point of sperm entry. The pigmented layer rotates towards the entry point, uncovering pale cytoplasm on the far side. Writing 'at the point of entry' is the classic mistake.")

    # ------------------------------------------------------------------ part 3: gastrulation to metamorphosis
    def p3(self):
        self.section(2)
        C = np.array([-3.0, -0.3, 0])
        g = ValueTracker(0.0)

        def gastrula():
            k = g.get_value()
            out = VGroup(Circle(radius=2.0, stroke_width=0, fill_color=MESO, fill_opacity=0.35).move_to(C))
            out.add(Annulus(inner_radius=1.75 - 0.1 * k, outer_radius=2.0, stroke_width=0, fill_color=ECTO, fill_opacity=0.85).move_to(C))
            yolk = Circle(radius=1.0 * (1 - 0.35 * k), stroke_width=0, fill_color=ENDO, fill_opacity=0.9).move_to(C + DOWN * (0.6 + 0.2 * k))
            out.add(yolk)
            bc = Ellipse(width=2.2 * (1 - 0.9 * k) + 0.01, height=1.1 * (1 - 0.9 * k) + 0.01, stroke_width=0, fill_color=th.BG, fill_opacity=1).move_to(C + UP * (0.55 + 0.3 * k) + LEFT * 0.4 * k)
            out.add(bc)
            if k > 0.05:
                arch = Ellipse(width=0.4 + 2.2 * k, height=0.25 + 0.9 * k, stroke_color=ENDO, stroke_width=6, fill_color=th.BG, fill_opacity=1).move_to(C + RIGHT * (1.5 - 1.3 * k) + DOWN * (0.6 - 0.5 * k))
                out.add(arch)
            lip = Dot(C + polar(2.0, -0.35), radius=0.12, color=WHITE)
            out.add(lip)
            return out

        gg = always_redraw(gastrula)
        cap = B.Captions(self, at=(3.6, 0.2, 0), width=5.4, size=24)
        with self.say("Gastrulation turns the one layered blastula into a gastrula with three germ layers. Nothing new is made. Cells simply move to where they will be needed. It begins with a groove just below the grey crescent. Its upper edge, the white dot, is the dorsal lip of the blastopore."):
            self.add(gg)
            cap("Dorsal lip of the blastopore", color=WHITE, sub="Forms just below the grey crescent.")
        with self.say("Two movements do the work. In epiboly, the small animal cells divide fast and spread down over the yolky cells, like a sock being pulled on. They become ectoderm. In emboly, cells roll inwards over the lip of the blastopore and move forward inside. They become mesoderm and endoderm.") as v:
            cap("Epiboly (spread over) + emboly (roll in)", color=ECTO, sub="Ectoderm outside; mesoderm and endoderm move inside.")
            self.play(g.animate.set_value(0.6), run_time=v.dur * 0.8)
        with self.say("Inside, a new cavity grows: the archenteron, the primitive gut. It pushes the old blastocoel aside until it disappears. The blastopore becomes a ring, with a plug of pale yolky cells sticking out: the yolk plug. Now there are three layers: ectoderm outside, endoderm lining the gut, mesoderm in between.") as v:
            self.play(g.animate.set_value(1.0), run_time=v.dur * 0.6)
            cap("Archenteron replaces the blastocoel", color=ENDO, swatch=ENDO, sub="Ectoderm (blue), mesoderm (red), endoderm (yellow); yolk plug in the blastopore.")
        self.play(FadeOut(gg))
        self.remove(gg)
        cap.clear()
        sp = self.callout("key", "Spemann and Mangold (1924): a dorsal lip grafted onto another embryo's belly makes a whole second embryo. The dorsal lip is the PRIMARY ORGANISER, and it comes from the grey crescent.", width=5.6, size=24).move_to([-3.2, 0.3, 0])
        cw = self.callout("careful", "The frog is a deuterostome: its blastopore becomes the ANUS; the mouth forms later at the other end.", width=5.4, size=24).move_to([3.4, 0.3, 0])
        with self.say("In nineteen twenty four, Spemann and Mangold grafted a dorsal lip from one newt embryo onto the belly of another. The host grew a complete second embryo. The dorsal lip is the primary organiser. And one fact students get backwards: in the frog, the blastopore becomes the anus, not the mouth. Frogs, like us, are deuterostomes."):
            self.play(FadeIn(sp, shift=UP * 0.2))
            self.play(FadeIn(cw, shift=UP * 0.2))
        self.play(FadeOut(VGroup(sp, cw)))
        n = ValueTracker(0.0)

        def neural():
            k = n.get_value()
            gg = VGroup()
            noto = Circle(radius=0.35, stroke_width=0, fill_color=MESO, fill_opacity=0.9).move_to([-3.0, -1.4, 0])
            xs = np.linspace(-6.0, 0.0, 60)
            gap = 1.6 * (1 - k)
            pts_l, pts_r = [], []
            for x in xs:
                d = x + 3.0
                y = 0.0 + 0.9 * k * np.exp(-((abs(d) - 0.6) ** 2) / 0.3) - 0.5 * np.exp(-(d ** 2) / 0.4) * (1 - k)
                pts_l.append([x, y, 0])
            ecto = VMobject(stroke_color=ECTO, stroke_width=10).set_points_smoothly(pts_l)
            gg.add(ecto, noto)
            if k > 0.95:
                tube = Annulus(inner_radius=0.2, outer_radius=0.45, stroke_width=0, fill_color=ECTO, fill_opacity=0.95).move_to([-3.0, -0.4, 0])
                gg.add(tube)
            return gg

        ng = always_redraw(neural)
        labs = VGroup(T("notochord (mesoderm)", size=22, color=MESO).move_to([-3.0, -2.2, 0]))
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.6, size=24)
        with self.say("Next, the nervous system. The roof of the gut rolls off as a rod, the notochord. It signals to the ectoderm above it, which thickens into a neural plate."):
            self.add(ng)
            self.play(FadeIn(labs))
            cap("Neural plate over the notochord", color=ECTO, swatch=ECTO)
        with self.say("The edges rise as neural folds, the middle sinks as a groove, and the folds meet and fuse into a hollow neural tube: the future brain and spinal cord. Cells left over at the seam form the neural crest."):
            self.play(n.animate.set_value(0.9), run_time=2.4)
            self.play(n.animate.set_value(1.0), run_time=0.4)
            cap("Neural folds → neural tube", color=ECTO, sub="Brain and spinal cord; the neural crest from the seam.")
        self.play(FadeOut(ng), FadeOut(labs))
        self.remove(ng)
        cap.clear()
        txt = ["epidermis and glands; brain, spinal cord, nerves; retina and lens; enamel; adrenal medulla", "all muscle; bone, cartilage, dermis; notochord; blood, heart, vessels; kidneys; gonads",
               "lining of the gut (not mouth, anus); liver, pancreas; lining of trachea and lungs; thyroid, thymus; bladder lining"]
        rows = [["germ layer", "becomes"]] + [[n_, para(t_, width=9.4, size=23, color=c_)] for n_, t_, c_ in zip(["ectoderm", "mesoderm", "endoderm"], txt, [ECTO, MESO, ENDO])]
        tb = B.table(rows, [2.6, 10.0], row_h=1.05, size=24, colors=[th.INK, th.BODY]).move_to([0, 0.9, 0])
        with self.say("The germ layer table, the most asked table in this unit. Ectoderm makes the skin and the entire nervous system, including the retina and lens. Mesoderm makes muscle, bone, blood, the heart, the kidneys and the gonads. Endoderm lines the gut and makes the liver, pancreas, the lining of the lungs, and the thyroid.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.tip("Outside or made of nerve → ECTODERM. Lining a tube that opens into the gut → ENDODERM. Everything in between (muscle, bone, blood, kidney) → MESODERM.",
                 "A memory trick: outside, inside, in between. Anything on the outside, or made of nerve, is ectoderm. Anything lining a tube that opens into the gut is endoderm. Everything in between, muscle, bone, blood, kidney, is mesoderm.", width=8.6)
        self.p3_meta()

    def tadpole(self, stage, s=1.0):
        body = Ellipse(width=1.2 * s, height=0.8 * s, stroke_width=0, fill_color="#5E6B3A", fill_opacity=1)
        tail_len = [1.6, 1.6, 1.6, 1.2, 0.4, 0.0][stage]
        tail = Polygon([0.5 * s, 0.15 * s, 0], [0.5 * s + tail_len * s, 0, 0], [0.5 * s, -0.15 * s, 0], stroke_width=0, fill_color="#5E6B3A", fill_opacity=1) if tail_len > 0 else VGroup()
        g = VGroup(tail, body, Dot([-0.35 * s, 0.12 * s, 0], radius=0.06 * s, color=WHITE))
        if stage == 0:
            g.add(*[Line([-0.1 * s, 0.3 * s, 0], [-0.1 * s + dx * s, 0.65 * s, 0], color=th.CORAL, stroke_width=3) for dx in (-0.2, 0, 0.2)])
        if stage >= 2:
            g.add(Line([0.4 * s, -0.3 * s, 0], [0.7 * s, -0.75 * s, 0], color="#5E6B3A", stroke_width=6))
        if stage >= 3:
            g.add(Line([-0.3 * s, -0.3 * s, 0], [-0.55 * s, -0.65 * s, 0], color="#5E6B3A", stroke_width=6))
        return g

    def p3_meta(self):
        head = T("Hatching and metamorphosis", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        labs = ["external gills, no mouth", "operculum, internal gills; herbivore", "hind limbs", "forelimbs; lungs", "tail absorbed", "froglet: carnivore"]
        stages = VGroup(*[self.tadpole(i, 0.8).move_to([-5.2 + 2.1 * i, 0.6, 0]) for i in range(6)])
        ll = VGroup(*[para(l_, width=1.9, size=17, color=th.BODY, align="center").next_to(stages[i], DOWN, buff=0.45) for i, l_ in enumerate(labs)])
        with self.say("About six days after fertilisation a tadpole hatches. At first it has external gills and no mouth, living on its yolk. Then a mouth opens and it becomes a plant eater, and a fold of skin covers internal gills. Hind legs appear, then front legs; lungs replace the gills; the tail is digested away; and the gut shortens as it turns carnivore. Two to three months, egg to froglet.") as v:
            self.play(FadeIn(head))
            for s_, l_ in zip(stages, ll):
                self.play(FadeIn(s_, shift=RIGHT * 0.2), FadeIn(l_), run_time=0.5)
                self.hold(v.dur * 0.13)
        self.play(FadeOut(VGroup(stages, ll)))
        chain = VGroup(*[T(s_, size=26, color=c_, weight="BOLD") for s_, c_ in [("pituitary", th.SKY), ("TSH", th.SKY), ("thyroid + iodine", th.AMBER), ("thyroxine", th.AMBER), ("metamorphosis", th.MINT)]]).arrange(RIGHT, buff=0.55).move_to([0, 1.3, 0])
        arr = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.08, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        exp = VGroup(VGroup(self.tadpole(1, 0.7), T("+ thyroxine →", size=22, color=th.AMBER), self.tadpole(5, 0.45), T("tiny frog, early", size=20, color=th.BODY)).arrange(RIGHT, buff=0.3),
                     VGroup(self.tadpole(1, 0.7), T("no iodine / no thyroid →", size=22, color=th.CORAL), self.tadpole(1, 1.3), T("giant tadpole, never changes", size=20, color=th.BODY)).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -1.3, 0])
        with self.say("What drives it? Thyroxine. The pituitary releases TSH, which makes the thyroid produce thyroxine, and the thyroid needs iodine to do it. Feed thyroxine to a young tadpole and it becomes a tiny frog far too early. Remove its thyroid, or keep it in iodine free water, and it grows into a giant tadpole that never changes."):
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chain], lag_ratio=0.2), LaggedStart(*[GrowArrow(a_) for a_ in arr], lag_ratio=0.2))
            self.play(FadeIn(exp[0], shift=UP * 0.2))
            self.play(FadeIn(exp[1], shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, chain, arr, exp)))
        head, prob = B.example_head(self, "A frog lays 2,800 eggs. 85% are fertilised, 60% of those hatch, and 3% of tadpoles become adults. (a) How many adults? (b) What percentage of eggs? (c) What does this say about population size?", size=25)
        bars = VGroup()
        for i, (n_, v_) in enumerate([("eggs", 2800), ("fertilised", 2380), ("tadpoles", 1428), ("adults", 42.84)]):
            r = Rectangle(width=max(0.05, v_ / 2800 * 6.0), height=0.38, stroke_width=0, fill_color=[th.SKY, th.MINT, th.AMBER, th.CORAL][i], fill_opacity=0.9)
            r.move_to([-3.2 + r.width / 2, 0.55 - 0.5 * i, 0])
            bars.add(VGroup(r, T(n_, size=20, color=th.INK).next_to([-3.2, 0.55 - 0.5 * i, 0], LEFT, buff=0.15), T(f"{v_:g}", size=20, color=th.BODY).next_to(r, RIGHT, buff=0.12)))
        steps = VGroup(M(r"2800 \times 0.85 \times 0.60 \times 0.03 = 42.84 \approx 43", size=36), M(r"\frac{42.84}{2800}\times100 = 1.53\%", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -2.3, 0])
        with self.say("And the cold open as an exam question. Two thousand eight hundred eggs, times nought point eight five, times nought point six, times nought point nought three: about forty three adults. That is one point five three percent of the eggs."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.3))
            self.play(Write(steps[0]))
            self.play(Write(steps[1]))
        with self.say("Only two adults are needed to replace the parents. In nature, predators, drying ponds and disease cut the forty three down to about two. External fertilisation with no parental care only works if the number of eggs is enormous, the opposite of the mammal strategy of a few, well protected young."):
            nb = B.neby_in(self, "think", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, prob, bars, steps)))
        self.quiz("Which of the following is NOT a derivative of mesoderm?",
                  ["kidney", "heart", "liver", "skeletal muscle"], 2,
                  "Pause and think. Which one is not mesodermal?",
                  "The liver. It grows out of the gut lining, so it is endodermal. Kidney, heart and muscle are all mesoderm, the in between layer.")
        self.quiz("A tadpole kept in iodine-free water will",
                  ["metamorphose early", "remain a tadpole and keep growing", "die within a week", "develop lungs but no limbs"], 1,
                  "Last one. A tadpole with no iodine. What happens?",
                  "It stays a tadpole and keeps growing. Without iodine the thyroid cannot make thyroxine, and without thyroxine there is no metamorphosis. Early metamorphosis is what extra thyroxine causes, the opposite case.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Gametogenesis: multiplication → growth → two meiotic divisions.",
            "One primary spermatocyte → 4 sperms; one primary oocyte → 1 ovum + 3 polar bodies.",
            "Frog egg: mesolecithal, telolecithal; the grey crescent fixes the dorsal side.",
            "Cleavage: holoblastic, unequal; 2ⁿ cells, no growth; eccentric blastocoel.",
            "Gastrulation: epiboly + emboly → 3 germ layers; dorsal lip = organiser; blastopore → anus.",
            "Thyroxine (needs iodine, driven by TSH) controls metamorphosis.",
        ], "Quick recap. Gametogenesis is multiplication, growth, and two meiotic divisions. One spermatocyte gives four sperms, one oocyte gives one ovum and three polar bodies. The frog's egg is mesolecithal and telolecithal, and the grey crescent marks the dorsal side. Cleavage is holoblastic but unequal, doubling the cells with no growth. Gastrulation moves cells into three germ layers, the dorsal lip is Spemann's organiser, and the blastopore becomes the anus. And metamorphosis is driven by thyroxine, which needs iodine.")
        self.outro("That was developmental biology. Next, the biggest unit of zoology: human biology, from digestion to hormones. See you there.")
