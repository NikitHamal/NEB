import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
import _emb as E  # noqa: E402
from _emb import EGG, SYN, ANT, POLAR, MALE, TUBE, EXINE, INTEG, polar  # noqa: E402

P3N = "#FFB547"
P2N = "#7BE495"
PN = "#C77DFF"


def ploidy_chip(txt, col):
    r = RoundedRectangle(corner_radius=0.12, width=0.8, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9)
    return VGroup(r, T(txt, size=22, color="#0B0E1A", weight="BOLD").move_to(r))


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 4
    TITLE = "Embryology"
    SUBTITLE = "From flower to seed"
    SECTIONS = ["Asexual and sexual reproduction", "Pollination", "Fertilization", "Male gametophyte",
                "Female gametophyte", "Dicot and monocot embryo", "Endosperm"]
    NEXT = "Unit 5 · Biotechnology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def grain(self, s=1.0):
        husk = Ellipse(width=2.2 * s, height=4.6 * s, stroke_color="#C9A27A", stroke_width=6, fill_color="#F3EBD6", fill_opacity=1)
        endo = Ellipse(width=1.9 * s, height=4.2 * s, stroke_width=0, fill_color="#F3EBD6", fill_opacity=1)
        emb = Ellipse(width=0.7 * s, height=1.0 * s, stroke_width=0, fill_color="#C5E8A0", fill_opacity=1).move_to([0.55 * s, -1.7 * s, 0])
        return VGroup(husk, endo, emb)

    def cold_open(self):
        bowl = VGroup(Arc(radius=2.4, start_angle=PI, angle=PI, stroke_color=th.BODY, stroke_width=6).move_to([0, -1.2, 0]),
                      *[Ellipse(width=0.22, height=0.5, stroke_width=0, fill_color="#F3EBD6", fill_opacity=1).rotate(a).move_to([x, y, 0])
                        for a, x, y in zip(np.random.default_rng(2).uniform(0, PI, 40), np.random.default_rng(3).uniform(-1.9, 1.9, 40), np.random.default_rng(4).uniform(-1.4, -0.3, 40))])
        with self.say("A plate of rice from the Terai. You eat it every day. But here is something strange about every single grain."):
            self.play(FadeIn(bowl, shift=UP * 0.3))
        self.play(FadeOut(bowl))
        g = self.grain(1.0).move_to([-2.6, 0, 0])
        chips = VGroup(VGroup(ploidy_chip("3n", P3N), T("endosperm: the white food", size=24, color=P3N)).arrange(RIGHT, buff=0.3),
                       VGroup(ploidy_chip("2n", P2N), T("embryo: the baby plant", size=24, color=P2N)).arrange(RIGHT, buff=0.3),
                       VGroup(ploidy_chip("2n", "#C9A27A"), T("seed coat: the mother's tissue", size=24, color="#C9A27A")).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([2.6, 0.2, 0])
        with self.say("Cut a grain open. The tiny embryo has two sets of chromosomes, like you. The skin is the mother plant's own tissue, also two sets. But the white part, the part you actually eat, has three sets. It is triploid."):
            self.play(FadeIn(g, scale=0.8))
            self.play(Indicate(g[2], color=P2N), FadeIn(chips[1]))
            self.play(Indicate(g[0], color="#C9A27A"), FadeIn(chips[2]))
            self.play(g[1].animate.set_fill(P3N, opacity=0.6), FadeIn(chips[0]))
        nb = B.neby_in(self, "surprised", height=1.4)
        with self.say("Three sets. No animal tissue is made like that. It comes from a double fertilization: one pollen grain, two sperm, two fusions at once. By the end of this lesson you will know exactly how."):
            pass
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(g, chips)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 4: Embryology. How a flower builds pollen and eggs, how they meet, and how one fertilised cell becomes a seed."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Our path. Asexual and sexual reproduction. Pollination. Fertilization, including double fertilization. Then the two gametophytes: the pollen grain, and the embryo sac. Then the embryo, in a dicot and a monocot. And finally the endosperm, the triploid food you eat.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        head = T("Asexual reproduction: clones", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        tub = Ellipse(width=2.4, height=1.6, stroke_width=0, fill_color="#C9A27A", fill_opacity=1).move_to([-4.2, -0.6, 0])
        eyes = [np.array([-4.9, -0.3, 0]), np.array([-3.8, -0.1, 0]), np.array([-3.4, -0.9, 0])]
        sprouts = VGroup(*[VGroup(Line(e, e + UP * 0.9 + RIGHT * 0.15, color="#5FB04A", stroke_width=5), Ellipse(width=0.35, height=0.18, stroke_width=0, fill_color="#5FB04A", fill_opacity=1).move_to(e + UP * 0.9 + RIGHT * 0.3)) for e in eyes])
        l1 = T("potato tuber: each eye is a bud", size=22, color=th.BODY).next_to(tub, DOWN, buff=0.35)
        leaf = Ellipse(width=3.0, height=1.5, stroke_color="#5FB04A", stroke_width=3, fill_color="#2E5E3A", fill_opacity=1).move_to([2.6, -0.4, 0])
        buds = VGroup(*[VGroup(Line(ORIGIN, UP * 0.35, color="#7BE495", stroke_width=3), Ellipse(width=0.22, height=0.12, stroke_width=0, fill_color="#7BE495", fill_opacity=1).shift(UP * 0.38))
                        .move_to(leaf.point_at_angle(a) + UP * 0.2) for a in np.linspace(0.3, PI - 0.3, 6)])
        l2 = T("Bryophyllum: buds on the leaf margin", size=22, color=th.BODY).next_to(leaf, DOWN, buff=0.35)
        with self.say("Plants can make new plants without any sex at all. A potato tuber is a swollen stem, and every eye is a bud. Plant it, and each bud grows into a new plant. The leaf of Bryophyllum sprouts little plantlets right along its edge."):
            self.play(FadeIn(head), FadeIn(tub), FadeIn(l1))
            self.play(LaggedStart(*[GrowFromPoint(s_, e) for s_, e in zip(sprouts, eyes)], lag_ratio=0.3))
            self.play(FadeIn(leaf), FadeIn(l2))
            self.play(LaggedStart(*[GrowFromCenter(b_) for b_ in buds], lag_ratio=0.15))
        clone = para("No gametes, no fertilization: every offspring is a genetically identical clone of its parent.", width=11, size=26, color=th.AMBER).move_to([0, -2.7, 0])
        with self.say("No gametes, no fertilization. So every offspring is a clone, genetically identical to the parent. This is vegetative propagation."):
            self.play(FadeIn(clone))
        self.play(FadeOut(VGroup(tub, sprouts, l1, leaf, buds, l2, clone, head)))
        rows = [["organ", "structure", "example"], ["underground stem", "rhizome · tuber · bulb · corm", "ginger · potato · onion · Colocasia"], ["sub-aerial stem", "runner · sucker · offset", "dubo grass · mint · water hyacinth"],
                ["leaf", "buds on the margin", "Bryophyllum"], ["root", "adventitious buds", "sweet potato, Dahlia"]]
        tb = B.table(rows, [2.8, 4.4, 4.8], row_h=0.66, size=23, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 0.3, 0])
        with self.say("The organs to know. Underground stems: the rhizome of ginger, the tuber of potato, the bulb of onion, the corm of Colocasia. Creeping stems: the runner of dubo grass, the sucker of mint, the offset of water hyacinth. Leaves, in Bryophyllum. And roots, in sweet potato and Dahlia.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        stock = Rectangle(width=0.6, height=2.4, stroke_width=0, fill_color="#7A5534", fill_opacity=1).move_to([-3.0, -1.1, 0])
        scion = Rectangle(width=0.5, height=1.6, stroke_width=0, fill_color="#5FB04A", fill_opacity=1).move_to([-3.0, 1.9, 0])
        cut = Polygon([-3.3, 0.1, 0], [-2.7, 0.1, 0], [-3.0, -0.3, 0], stroke_width=0, fill_color=th.BG, fill_opacity=1)
        ls = VGroup(T("scion: the variety you want", size=22, color="#5FB04A").move_to([-4.3, 2.9, 0]), T("stock: hardy roots", size=22, color="#C9A27A").move_to([-4.6, -2.75, 0]))
        art = VGroup(*[para(s_, width=5.6, size=24, color=th.INK) for s_ in ["cutting: sugarcane, rose", "layering: jasmine, litchi", "grafting and budding: mango, citrus, apple in Mustang and Jumla", "micropropagation: tissue culture"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.3, 0])
        with self.say("Growers copy plants on purpose. Cuttings of sugarcane and rose. Layering in jasmine and litchi. And grafting: a shoot of the variety you want, the scion, is joined onto a hardy rooted stock. The apple orchards of Mustang and Jumla are grafted."):
            self.play(FadeIn(stock), FadeIn(scion), FadeIn(ls))
            self.play(scion.animate.move_to([-3.0, 0.75, 0]), run_time=1.0)
            self.sfx("click", gain=-10)
            self.play(LaggedStart(*[FadeIn(a_, shift=LEFT * 0.2) for a_ in art], lag_ratio=0.3))
        self.play(FadeOut(VGroup(stock, scion, ls, art)))
        ap = self.callout("key", "Apomixis: a seed formed WITHOUT fertilization, so the embryo is a clone of the mother. In Citrus and mango, extra embryos grow from the nucellus: nucellar polyembryony. Breeders prize it because it fixes a hybrid's vigour.", width=11, size=26)
        with self.say("A special case: apomixis. A seed forms without any fertilization, so the embryo is a clone of its mother. In citrus and mango, extra embryos grow out of the nucellus beside the normal one: nucellar polyembryony. Breeders love apomixis, because it could fix a hybrid's vigour for ever."):
            self.play(FadeIn(ap, shift=UP * 0.2))
        self.play(FadeOut(ap))
        rows = [["", "asexual", "sexual"], ["speed", "quick", "slower"], ["offspring", "identical clones", "varied"], ["risk", "one disease can wipe out a whole crop", "variation helps some survive"], ["use", "keeps exact qualities; seedless banana", "raw material of breeding and evolution"]]
        tb = B.table(rows, [2.2, 5.0, 5.0], row_h=0.66, size=23, colors=[th.MUTED, th.SKY, th.PINK]).move_to([0, 0.3, 0])
        with self.say("The trade off. Asexual reproduction is quick and keeps a good variety exactly as it is, even a seedless banana. But with no variation, a single disease can wipe out the whole crop. Sexual reproduction is slower, but it creates variation, the raw material of breeding and of evolution.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        fl = E.flower(1.15).move_to([-3.2, -0.2, 0])
        P = fl.parts
        cap = B.Captions(self, at=(3.2, 0.2, 0), width=6.0, size=26)
        with self.say("Sexual reproduction happens in the flower. The stamens form the androecium: each is a filament carrying an anther. The anther is a microsporangium: it makes microspores, which become pollen."):
            self.play(FadeIn(fl))
            self.play(Indicate(P["stamens"], color=EXINE))
            cap("Androecium: stamens = filament + anther", color=EXINE, swatch=EXINE, sub="Anther = microsporangium → microspores (pollen).")
        with self.say("The carpels form the gynoecium: each pistil has an ovary, a style and a stigma. Inside the ovary are ovules, the megasporangia, which make megaspores. Two different kinds of spore: angiosperms are heterosporous."):
            self.play(Indicate(VGroup(P["ovary"], P["style"], P["stigma"]), color="#C5F05C"))
            cap("Gynoecium: pistil = ovary + style + stigma", color="#C5F05C", swatch="#C5F05C", sub="Ovule = megasporangium → megaspores. Two kinds of spore: heterosporous.")
        self.play(FadeOut(fl))
        cap.clear()
        nodes = [("sporophyte (2n): the plant", [0, 1.8, 0], P2N), ("spores (n)", [3.6, -0.6, 0], PN), ("gametophytes (n): pollen grain, embryo sac", [0, -2.4, 0], PN), ("zygote (2n)", [-3.6, -0.6, 0], P2N)]
        boxes = VGroup(*[self.panel(6.0 if i % 2 == 0 else 2.6, 0.75, color=c_).move_to(p_) for i, (_, p_, c_) in enumerate(nodes)])
        txt = VGroup(*[T(n_, size=22, color=th.INK).move_to(b_) for (n_, _, _), b_ in zip(nodes, boxes)])
        arrs = VGroup(*[CurvedArrow(boxes[i].get_center() + (boxes[(i + 1) % 4].get_center() - boxes[i].get_center()) * 0.35, boxes[(i + 1) % 4].get_center() - (boxes[(i + 1) % 4].get_center() - boxes[i].get_center()) * 0.35, angle=-0.5, color=th.MUTED, stroke_width=3) for i in range(4)])
        al = VGroup(T("meiosis", size=22, color=th.AMBER).move_to([3.0, 1.2, 0]), T("mitosis", size=22, color=th.AMBER).move_to([4.6, -1.7, 0]), T("fertilization", size=22, color=th.AMBER).move_to([-4.6, -1.7, 0]), T("growth", size=22, color=th.AMBER).move_to([-3.0, 1.2, 0]))
        with self.say("The plant you see is the diploid sporophyte. By meiosis it makes haploid spores. Those grow into tiny haploid gametophytes: the pollen grain is the male one, and the embryo sac is the female one. They make gametes, fertilization gives a diploid zygote, and the zygote grows into a new sporophyte. This is alternation of generations, squeezed almost out of sight inside the flower.") as v:
            for i in range(4):
                self.play(FadeIn(boxes[i]), FadeIn(txt[i]), run_time=0.4)
                self.play(Create(arrs[i]), FadeIn(al[i]), run_time=0.5)
                self.hold(v.dur * 0.18)
        self.play(FadeOut(VGroup(boxes, txt, arrs, al)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        d = self.callout("key", "Pollination: the transfer of pollen from an anther to a stigma of the same kind of flower. It must come first, because the male gametes cannot swim: they reach the egg only through a pollen tube.", width=11, size=27)
        with self.say("Pollination is the transfer of pollen from an anther to a stigma. It has to happen before fertilization, because flowering plant sperm cannot swim. They can only reach the egg through a pollen tube grown from a grain that has landed on a stigma."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        f1 = E.flower(0.75).move_to([-4.0, 0.0, 0])
        f2 = E.flower(0.75).move_to([-1.2, 0.0, 0])
        f3 = E.flower(0.75).move_to([3.8, 0.0, 0])
        brace = BraceBetweenPoints([-5.2, -2.7, 0], [0.0, -2.7, 0], direction=DOWN, color=th.MUTED)
        bl = T("one plant", size=22, color=th.MUTED).next_to(brace, DOWN, buff=0.08)
        b2 = T("another plant", size=22, color=th.MUTED).move_to([3.8, -3.05, 0])
        a1 = CurvedArrow(f1.parts["stamens"][1][1].get_center(), f1.parts["stigma"].get_center() + RIGHT * 0.05, angle=0.9, color=th.AMBER, stroke_width=4)
        a2 = CurvedArrow(f1.parts["stamens"][1][1].get_center(), f2.parts["stigma"].get_center(), angle=-0.8, color=th.SKY, stroke_width=4)
        a3 = CurvedArrow(f2.parts["stamens"][1][1].get_center(), f3.parts["stigma"].get_center(), angle=-0.5, color=th.MINT, stroke_width=4)
        cap = B.Captions(self, at=(0, 2.85, 0), width=12, size=25)
        with self.say("Three kinds. Pollen to the stigma of the same flower: autogamy, self pollination."):
            self.play(FadeIn(f1), FadeIn(f2), FadeIn(f3), GrowFromCenter(brace), FadeIn(bl), FadeIn(b2))
            self.play(Create(a1))
            cap("Autogamy: within the same flower", color=th.AMBER)
        with self.say("To another flower on the same plant: geitonogamy. It needs an agent to carry the pollen, but genetically it is still self pollination, because it is the same plant."):
            self.play(Create(a2))
            cap("Geitonogamy: another flower, same plant (genetically still selfing)", color=th.SKY)
        with self.say("And to a flower on a different plant of the same species: xenogamy, true cross pollination. Only this brings in new genes."):
            self.play(Create(a3))
            cap("Xenogamy: a different plant: the only one that brings new genes", color=th.MINT)
        self.play(FadeOut(VGroup(f1, f2, f3, brace, bl, b2, a1, a2, a3)))
        cap.clear()
        selfs = para("Self-pollination is made certain by homogamy (anther and stigma ripen together), cleistogamy (flowers that never open: Commelina, Viola, Oxalis) and bud pollination (pea, wheat).", width=11.5, size=26, color=th.INK).move_to([0, 0.3, 0])
        with self.say("Some plants make sure they self pollinate. In homogamy the anthers and stigma ripen together. In cleistogamy the flowers never open at all, as in Commelina, Viola and Oxalis. And pea and wheat pollinate themselves while still in bud."):
            self.play(FadeIn(selfs))
        self.play(FadeOut(selfs))
        rows = [["agent", "name", "flowers are", "examples"], ["wind", "anemophily", "small, dull, no nectar; masses of light dry pollen; feathery stigma", "maize, grasses, Pinus"],
                ["water", "hydrophily", "pollen and stigma unwettable; long thread-like pollen", "Vallisneria, Hydrilla"], ["insect", "entomophily", "large, bright, scented, nectar; sticky spiny pollen", "Salvia, mustard"],
                ["bird", "ornithophily", "large, red, tubular, lots of watery nectar, no scent", "simal (Bombax), Butea"], ["bat", "chiropterophily", "large, dull, strong smell, open at night, tough", "Kigelia, Adansonia"]]
        tb = B.table(rows, [1.4, 2.3, 6.2, 3.0], row_h=0.72, size=21, colors=[th.AMBER, th.SKY, th.INK, th.BODY]).move_to([0, 0.1, 0])
        with self.say("Cross pollination needs an agent, and each agent shapes the flower. Wind flowers are small and dull, with masses of light pollen and feathery stigmas, like maize. Water flowers, like Vallisneria, have pollen that will not get wet. Insect flowers are bright, scented and full of nectar. Bird flowers, like the red simal of the Terai, are large, red and tubular, with lots of nectar but no scent, because birds cannot smell well. And bat flowers open at night and smell strongly.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        head = T("Tricks that force cross-pollination", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        days = VGroup(*[T(f"day {k}", size=20, color=th.MUTED).move_to([-3.6 + 1.8 * k, -0.2, 0]) for k in range(1, 5)])
        an_bar = Rectangle(width=3.4, height=0.4, stroke_width=0, fill_color=EXINE, fill_opacity=0.85).move_to([-2.7 + 0.0, 0.8, 0])
        st_bar = Rectangle(width=3.4, height=0.4, stroke_width=0, fill_color="#C5F05C", fill_opacity=0.85).move_to([0.9, 0.3, 0])
        al_ = T("anthers shed pollen", size=20, color=EXINE).next_to(an_bar, UP, buff=0.08)
        sl_ = T("stigma receptive", size=20, color="#C5F05C").next_to(st_bar, UP, buff=0.08)
        prot = T("protandry: sunflower, Salvia", size=24, color=th.AMBER).move_to([3.9, 0.8, 0])
        with self.say("Plants have evolved tricks to avoid selfing. In dichogamy the two sexes ripen at different times. In protandry, as in sunflower, the anthers shed their pollen first, and the stigma of the same flower opens only after they are done. Protogyny is the reverse."):
            self.play(FadeIn(head), FadeIn(days))
            self.play(GrowFromEdge(an_bar, LEFT), FadeIn(al_))
            self.play(GrowFromEdge(st_bar, LEFT), FadeIn(sl_), FadeIn(prot))
        others = VGroup(*[T(s_, size=24, color=th.INK) for s_ in ["dicliny: separate male and female flowers (maize, papaya)", "herkogamy: a physical barrier (Calotropis pollinia)",
                                                                   "heterostyly: different style lengths (Primula)", "self-incompatibility: own pollen cannot grow (tobacco, crucifers)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -2.0, 0])
        with self.say("And four more. Dicliny: separate male and female flowers, as in maize and papaya. Herkogamy: a physical barrier. Heterostyly: different style lengths in different plants, as in Primula. And self incompatibility, a genetic lock that stops a plant's own pollen from growing on its stigma.") as v:
            self.play(FadeOut(VGroup(days, an_bar, st_bar, al_, sl_, prot)))
            others.move_to([0, 0.2, 0])
            for o_ in others:
                self.play(FadeIn(o_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.18)
        self.play(FadeOut(VGroup(head, others)))
        rows = [["", "self-pollination", "cross-pollination"], ["agent", "not needed", "always needed"], ["pollen wasted", "very little", "a great deal"], ["variation", "none", "plenty"],
                ["vigour", "falls: inbreeding depression", "hybrid vigour"], ["certainty", "almost certain", "depends on the agent"]]
        tb = B.table(rows, [2.6, 4.6, 4.6], row_h=0.66, size=23, colors=[th.MUTED, th.AMBER, th.MINT]).move_to([0, 0.3, 0])
        with self.say("Self versus cross, for the exam. Agent, wasted pollen, variation, vigour, and certainty.") as v:
            B.reveal_table(self, tb, max(2.5, v.dur * 0.9))
        self.wait(1.5)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        sty_top, sty_bot = np.array([0, 2.6, 0]), np.array([0, -0.6, 0])
        stigma = Ellipse(width=1.8, height=0.5, stroke_width=0, fill_color="#E9F99A", fill_opacity=1).move_to([0, 2.8, 0])
        style = Rectangle(width=0.7, height=3.4, stroke_width=0, fill_color="#3E5A2A", fill_opacity=1).move_to([0, 1.0, 0])
        ov = E.ovule(0.62).move_to([0, -2.0, 0])
        gr = E.pollen(0.32, cells=2).move_to([0, 3.15, 0])
        t = ValueTracker(0.0)
        path = [np.array([0, 2.95, 0]), np.array([0.08, 2.2, 0]), np.array([-0.08, 1.2, 0]), np.array([0.05, 0.2, 0]), np.array([0, -0.6, 0]),
                ov.parts["micropyle"].get_center() + DOWN * 0.1, ov.parts["embryo_sac"].parts["synergids"][0].get_center()]
        full = VMobject().set_points_smoothly(path)

        def tube():
            a = t.get_value()
            if a <= 0.001:
                return VGroup()
            seg = full.copy().pointwise_become_partial(full, 0, a)
            seg.set_stroke(TUBE, width=6)
            tip = seg.get_end()
            return VGroup(seg, Dot(tip, radius=0.07, color="#B6F5C4"), Dot(tip + UP * 0.22, radius=0.05, color=MALE), Dot(tip + UP * 0.38, radius=0.05, color=MALE))

        tb_ = always_redraw(tube)
        cap = B.Captions(self, at=(3.7, 0.4, 0), width=5.6, size=25)
        with self.say("A compatible pollen grain lands on a ripe stigma. It soaks up water and sugars and germinates. The inner wall, the intine, pushes out through a germ pore as a pollen tube."):
            self.play(FadeIn(stigma), FadeIn(style), FadeIn(ov))
            self.play(FadeIn(gr, shift=DOWN * 0.6))
            self.add(tb_)
            self.play(t.animate.set_value(0.12), run_time=1.0)
            cap("Germination: the intine grows out as a pollen tube", color=TUBE, swatch=TUBE)
        with self.say("The tube digests its way down through the style, steered chemically by substances from the synergids. The tube nucleus leads at the tip, and the generative cell, if it has not already, divides to give two male gametes, which follow behind.") as v:
            self.play(t.animate.set_value(0.8), run_time=v.dur * 0.85, rate_func=rate_functions.linear)
            cap("Tube nucleus at the tip; two male gametes behind", color=MALE, swatch=MALE)
        with self.say("Usually it enters the ovule through the micropyle: porogamy. Rarely through the chalaza, chalazogamy, as in Casuarina, or through the integument, mesogamy, as in Cucurbita."):
            self.play(t.animate.set_value(1.0), run_time=1.6)
            cap("Porogamy (micropyle) · chalazogamy (Casuarina) · mesogamy (Cucurbita)")
        self.play(FadeOut(VGroup(stigma, style, gr)), FadeOut(tb_), FadeOut(ov))
        self.remove(tb_)
        cap.clear()
        es = E.embryo_sac(2.6, 5.2).move_to([-2.6, -0.2, 0])
        S = es.parts
        lab = VGroup(B.label("antipodals (3)", [1.5, 2.0, 0], S["antipodals"].get_right(), color=ANT, size=22),
                     B.label("central cell, 2 polar nuclei", [1.5, 0.3, 0], S["polar"].get_right(), color=POLAR, size=22),
                     B.label("egg", [1.5, -1.25, 0], S["egg"].get_right(), color=EGG, size=22),
                     B.label("synergids (2), filiform apparatus", [1.5, -2.35, 0], S["synergids"][1].get_right(), color=SYN, size=22))
        for l_ in lab:
            l_[1].align_to(np.array([0.6, 0, 0]), LEFT)
            l_[0].put_start_and_end_on(l_[1].get_left() + LEFT * 0.08, l_[0].get_end())
        with self.say("Here is the inside of the ovule, the embryo sac. We will build it in part five. For now, meet the players. Egg and two synergids at the micropyle. Three antipodals at the far end. And a large central cell, holding two polar nuclei."):
            self.play(FadeIn(es))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lab], lag_ratio=0.3))
        tip = S["synergids"][0].get_center()
        m1 = Dot(tip + DOWN * 0.6, radius=0.11, color=MALE)
        m2 = Dot(tip + DOWN * 0.8, radius=0.11, color=MALE)
        tube2 = Line(tip + DOWN * 1.2, tip, color=TUBE, stroke_width=7)
        with self.say("The tube enters one synergid, guided by its filiform apparatus, and bursts, releasing both male gametes into the sac. What happens next is found only in flowering plants."):
            self.play(Create(tube2), FadeIn(m1), FadeIn(m2))
            self.play(m1.animate.move_to(tip), m2.animate.move_to(tip + RIGHT * 0.1), run_time=0.8)
            self.play(S["synergids"][0].animate.set_opacity(0.3))
        zyg = ploidy_chip("2n", P2N).next_to(S["egg"], LEFT, buff=0.3)
        pen = ploidy_chip("3n", P3N).next_to(S["polar"], LEFT, buff=0.3)
        with self.say("One male gamete fuses with the egg. That is syngamy, and it makes a diploid zygote, the future embryo."):
            self.play(m1.animate.move_to(S["egg"].get_center()), run_time=1.0)
            self.play(Flash(S["egg"], color=EGG), S["egg"][0].animate.set_fill(P2N, opacity=0.5), FadeOut(m1), FadeIn(zyg, scale=1.3))
            self.sfx("pop", gain=-10)
        with self.say("The second male gamete travels on to the centre and fuses with both polar nuclei at once. Three nuclei fuse, so it is called triple fusion, and the product is the triploid primary endosperm nucleus. That is where the three sets in your rice come from."):
            self.play(m2.animate.move_to(S["polar"].get_center()), run_time=1.2)
            self.play(Flash(S["polar"], color=POLAR), Transform(S["polar"], Dot(S["polar"].get_center(), radius=0.22, color=P3N)), FadeOut(m2), FadeIn(pen, scale=1.3))
            self.sfx("pop", gain=-10)
            nb = B.neby_in(self, "success", height=1.3)
        B.neby_out(self, nb)
        eq = VGroup(M(r"n + n \to 2n \ \ \text{zygote (syngamy)}", size=36, color=P2N), M(r"n + n + n \to 3n \ \ \text{PEN (triple fusion)}", size=36, color=P3N)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.4, 0])
        nw = para("double fertilization: Nawaschin, 1898 (Lilium, Fritillaria)", width=5.4, size=22, color=th.MUTED).next_to(eq, DOWN, buff=0.35).align_to(eq, LEFT)
        with self.say("Two fusions in one embryo sac: double fertilization, discovered by Nawaschin in eighteen ninety eight. And its point is economy. The food store is built only after the egg has really been fertilised, so the plant never wastes food on an ovule that will not become a seed."):
            self.play(FadeOut(lab), FadeIn(eq, shift=LEFT * 0.2))
            self.play(FadeIn(nw))
        self.play(FadeOut(VGroup(es, tube2, zyg, pen, eq, nw)))
        rows = [["before", "after"], ["ovule", "seed"], ["ovary", "fruit"], ["ovary wall", "pericarp"], ["integuments", "seed coat (testa, tegmen)"], ["zygote", "embryo"], ["primary endosperm nucleus", "endosperm"],
                ["nucellus", "used up, or perisperm"], ["synergids, antipodals", "degenerate"]]
        tb = B.table(rows, [5.0, 5.4], row_h=0.58, size=24, colors=[th.MUTED, th.MINT]).move_to([0, 0.1, 0])
        with self.say("After fertilization the whole flower is rebuilt. The ovule becomes the seed, the ovary the fruit, the ovary wall the pericarp. The integuments harden into the seed coat. The zygote becomes the embryo, the primary endosperm nucleus the endosperm. The nucellus is usually used up, and the synergids and antipodals die.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("The ploidy of the primary endosperm nucleus is",
                  ["n", "2n", "3n", "4n"], 2,
                  "Pause and think. One male gamete plus two polar nuclei. What ploidy?",
                  "Three n. One haploid male gamete plus two haploid polar nuclei gives three sets. Two n is the zygote, the tempting answer if you forget that there are two polar nuclei.")

    # ------------------------------------------------------------------ part 4: male gametophyte
    def p4(self):
        self.section(3)
        an = E.anther_ts(1.45).move_to([-3.0, -0.2, 0])
        P = an.parts
        cap = B.Captions(self, at=(3.6, 0.2, 0), width=5.6, size=25)
        with self.say("Cut a young anther across. It is butterfly shaped: two lobes joined by the connective, and each lobe holds two pollen sacs. Dithecous, and tetrasporangiate."):
            self.play(FadeIn(an))
            cap("Dithecous, tetrasporangiate", sub="Two lobes (thecae), four microsporangia; the connective carries a vascular bundle.")
        layers = [("epidermis", "epidermis", "#2EC4B6", "One layer: protection."),
                  ("endothecium", "endothecium", "#F4A261", "Fibrous thickenings: dries, curls, and tears the anther open at the stomium."),
                  ("middle", "middle layers", "#8189B0", "2 to 4 thin layers, crushed as pollen grows."),
                  ("tapetum", "tapetum", "#C77DFF", "Innermost, dense, often multinucleate: NOURISHES the microspores and supplies sporopollenin.")]
        says = ["Each sac has a wall of four layers. Outside, the epidermis, for protection.",
                "Then the endothecium, with bands of fibrous thickening. As it dries, it curls and tears the anther open: it does the dehiscence.",
                "Then two to four thin middle layers, which get crushed as the pollen grows.",
                "And innermost, the tapetum: big cells with dense cytoplasm, often with several nuclei. The tapetum feeds the developing pollen, and supplies sporopollenin for the pollen wall."]
        for (k_, n_, c_, d_), sy in zip(layers, says):
            with self.say(sy):
                self.play(Indicate(P[k_], color=c_, scale_factor=1.03))
                cap(n_.capitalize(), color=c_, swatch=c_, sub=d_)
        self.play(FadeOut(an))
        cap.clear()
        self.tip("Tapetum = NUTRITION (and sporopollenin). Epidermis = protection. Endothecium = dehiscence. If the tapetum fails, the pollen is sterile.",
                 "Exam tip. The tapetum is nutritive, not protective. Protection is the epidermis, opening is the endothecium, and feeding the pollen is the tapetum. If the tapetum fails, the pollen is sterile: which is exactly how male sterile lines are made for hybrid seed.")
        head = T("From mother cell to pollen grain", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        mmc = VGroup(Circle(radius=0.75, stroke_color=P2N, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1), E.nucleus(ORIGIN, 0.2, P2N)).move_to([-5.4, 0.2, 0])
        ml = VGroup(para("microspore mother cell", width=1.8, size=20, color=P2N, align="center"), ploidy_chip("2n", P2N)).arrange(DOWN, buff=0.1).next_to(mmc, DOWN, buff=0.2)
        tet = VGroup(*[VGroup(Circle(radius=0.36, stroke_color=PN, stroke_width=3, fill_color="#2E2650", fill_opacity=1), E.nucleus(ORIGIN, 0.1, PN)).move_to([-2.6 + dx, 0.2 + dy, 0]) for dx, dy in [(-0.37, 0.37), (0.37, 0.37), (-0.37, -0.37), (0.37, -0.37)]])
        tl = VGroup(para("tetrad of microspores", width=1.8, size=20, color=PN, align="center"), ploidy_chip("n", PN)).arrange(DOWN, buff=0.1).next_to(tet, DOWN, buff=0.2)
        ar1 = Arrow(mmc.get_right(), tet.get_left(), buff=0.15, color=th.MUTED, stroke_width=3)
        a1l = T("meiosis", size=20, color=th.AMBER).next_to(ar1, UP, buff=0.05)
        pg = E.pollen(0.85, cells=2).move_to([0.8, 0.2, 0])
        ar2 = Arrow(tet.get_right(), pg.get_left(), buff=0.15, color=th.MUTED, stroke_width=3)
        a2l = T("unequal mitosis", size=20, color=th.AMBER).next_to(ar2, UP, buff=0.05)
        pl = VGroup(T("2-celled pollen grain", size=20, color=EXINE)).next_to(pg, DOWN, buff=0.2)
        pg3 = E.pollen(0.85, cells=3).move_to([4.6, 0.2, 0])
        ar3 = Arrow(pg.get_right(), pg3.get_left(), buff=0.15, color=th.MUTED, stroke_width=3)
        a3l = para("generative cell divides", width=2.0, size=18, color=th.AMBER, align="center").next_to(ar3, UP, buff=0.05)
        p3l = para("3 cells: tube cell + 2 male gametes", width=3.0, size=20, color=MALE, align="center").next_to(pg3, DOWN, buff=0.2)
        with self.say("Inside each young sac, microspore mother cells, diploid, divide by meiosis into tetrads of four haploid microspores. That is microsporogenesis."):
            self.play(FadeIn(head), FadeIn(mmc), FadeIn(ml))
            self.play(GrowArrow(ar1), FadeIn(a1l), TransformFromCopy(mmc, tet), FadeIn(tl))
        with self.say("Each microspore then grows a two layered wall and divides by mitosis, very unequally. A big vegetative, or tube, cell, full of food, and a small spindle shaped generative cell floating inside it. That is microgametogenesis."):
            self.play(GrowArrow(ar2), FadeIn(a2l), TransformFromCopy(tet[1], pg), FadeIn(pl))
        with self.say("The generative cell divides once more to give two male gametes. In about sixty percent of families that happens later, inside the pollen tube; in grasses, mustards and sunflowers it happens before the pollen is shed, so the grain is shed three celled. Either way, the whole male gametophyte is just three cells."):
            self.play(GrowArrow(ar3), FadeIn(a3l), TransformFromCopy(pg, pg3), FadeIn(p3l))
        self.play(FadeOut(VGroup(mmc, ml, tet, tl, ar1, a1l, ar2, a2l, pl, ar3, a3l, pg3, p3l)), pg.animate.scale(2.3).move_to([-3.2, -0.3, 0]))
        G = pg.parts
        lab = VGroup(B.label("exine: sporopollenin", [1.0, 1.8, 0], G["exine"].get_top() + RIGHT * 0.6, color=EXINE, size=22),
                     B.label("germ pore", [1.0, 0.9, 0], G["pores"][0].get_center(), color=th.INK, size=22),
                     B.label("intine: cellulose and pectin", [1.0, 0.0, 0], G["intine"].point_at_angle(0.3), color="#F6E3A1", size=22),
                     B.label("vegetative (tube) nucleus", [1.0, -0.9, 0], G["veg"].get_center(), color="#B6F5C4", size=22),
                     B.label("generative cell", [1.0, -1.8, 0], G["gen"].get_center(), color=MALE, size=22))
        for l_ in lab:
            l_[1].align_to(np.array([0.5, 0, 0]), LEFT)
            l_[0].put_start_and_end_on(l_[1].get_left() + LEFT * 0.08, l_[0].get_end())
        with self.say("The wall. A hard, sculptured outer exine made of sporopollenin, the toughest organic material known. That is why pollen survives for millions of years as fossils. It has thin spots, the germ pores, where the tube will come out. Inside it, a thin intine of cellulose and pectin."):
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lab], lag_ratio=0.3), run_time=2.5)
        self.play(FadeOut(VGroup(pg, lab, head)))
        head, prob = B.example_head(self, "A mustard anther produced 1,200 pollen grains. (a) How many microspore mother cells? (b) How many meioses? (c) How many male gametes can they deliver? (d) How many nuclei in all in the 1,200 three-celled grains?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 1200 \div 4 = 300 \text{ mother cells}", size=38), M(r"\text{(b)}\ \ \text{one meiosis each} = 300", size=38),
                       M(r"\text{(c)}\ \ 1200 \times 2 = 2400 \text{ male gametes}", size=38), M(r"\text{(d)}\ \ 1200 \times 3 = 3600 \text{ nuclei}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["A counting example.", "Each mother cell makes four microspores, so twelve hundred grains needed three hundred mother cells.", "One meiosis per mother cell: three hundred meioses.",
                "Each grain makes two male gametes: two thousand four hundred.", "And a three celled grain has three nuclei, one tube nucleus and two gametes: three thousand six hundred in all."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.2)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("The layer of the anther wall that nourishes the developing microspores is the",
                  ["epidermis", "endothecium", "middle layer", "tapetum"], 3,
                  "Pause and think. Which anther wall layer feeds the pollen?",
                  "The tapetum. The endothecium is the trap: it is the layer with fibrous bands that splits the anther open. It does not feed anything.")

    # ------------------------------------------------------------------ part 5: female gametophyte
    def p5(self):
        self.section(4)
        ov = E.ovule(1.15).move_to([-3.0, 0.1, 0])
        P = ov.parts
        cap = B.Captions(self, at=(3.4, 0.3, 0), width=6.0, size=25)
        with self.say("Now the female side. This is an ovule, the megasporangium, cut lengthwise. It hangs from the placenta by a stalk, the funicle, which joins the body at the hilum."):
            self.play(FadeIn(ov))
            self.play(Indicate(P["funicle"], color="#C5F05C"))
            cap("Funicle and hilum", color="#C5F05C", swatch="#C5F05C")
        with self.say("Inside, a mass of nutritive tissue, the nucellus, wrapped in one or two integuments. They leave a narrow pore at one end, the micropyle. The opposite end, the base, is the chalaza. And deep in the nucellus sits the embryo sac."):
            self.play(Indicate(P["nucellus"], color=P2N))
            self.play(ShowPassingFlash(P["integuments"][0].copy().set_fill(opacity=0).set_stroke(INTEG, 9), time_width=0.6), run_time=1.0)
            self.play(Indicate(P["micropyle"], color=th.AMBER, scale_factor=1.6))
            cap("Nucellus · integuments · micropyle · chalaza · embryo sac", sub="Nucellus and integuments are the mother's own tissue: 2n.")
        with self.say("This ovule is turned completely upside down on its stalk, so the micropyle lies right beside the hilum, and the funicle is fused along one side as a ridge, the raphe. That is an anatropous ovule, the commonest type, found in about eighty percent of families."):
            cap("Anatropous: inverted, micropyle beside the hilum", color=INTEG, sub="About 80% of families. Also: orthotropous (straight), campylotropous (curved), amphitropous, circinotropous.")
        self.play(FadeOut(ov))
        cap.clear()
        head = T("Megasporogenesis", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        mmc = VGroup(Ellipse(width=0.9, height=1.3, stroke_color=P2N, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1), E.nucleus(ORIGIN, 0.18, P2N)).move_to([-4.2, 0.0, 0])
        ml = VGroup(T("megaspore mother cell", size=20, color=P2N), ploidy_chip("2n", P2N)).arrange(DOWN, buff=0.1).next_to(mmc, DOWN, buff=0.25)
        lin = VGroup(*[VGroup(Rectangle(width=0.8, height=0.55, stroke_color=PN, stroke_width=3, fill_color="#2E2650", fill_opacity=1), E.nucleus(ORIGIN, 0.09, PN)).move_to([-0.8, -0.85 + 0.6 * k, 0]) for k in range(4)])
        mic = T("micropyle ↓", size=20, color=th.MUTED).next_to(lin, DOWN, buff=0.2)
        cha = T("chalaza ↑", size=20, color=th.MUTED).next_to(lin, UP, buff=0.2)
        ar = Arrow(mmc.get_right(), lin.get_left(), buff=0.2, color=th.MUTED, stroke_width=3)
        al = T("meiosis", size=20, color=th.AMBER).next_to(ar, UP, buff=0.05)
        cap = B.Captions(self, at=(3.6, 0.0, 0), width=5.4, size=25)
        with self.say("Near the micropyle, one cell of the nucellus enlarges into the megaspore mother cell, diploid. It divides by meiosis into a row of four haploid megaspores: a linear tetrad. That is megasporogenesis."):
            self.play(FadeIn(head), FadeIn(mmc), FadeIn(ml))
            self.play(GrowArrow(ar), FadeIn(al), TransformFromCopy(mmc, lin), FadeIn(mic), FadeIn(cha))
            cap("Linear tetrad of megaspores (n)", color=PN, swatch=PN)
        with self.say("Then three of them die, usually the three nearest the micropyle. Only the chalazal one survives: the functional megaspore."):
            self.play(*[lin[k].animate.set_opacity(0.15) for k in range(3)], Indicate(lin[3], color=PN, scale_factor=1.15))
            cap("Three degenerate; the chalazal megaspore is functional", color=PN)
        self.play(FadeOut(VGroup(head, mmc, ml, lin, mic, cha, ar, al)))
        cap.clear()
        head = T("Megagametogenesis: 1 → 2 → 4 → 8", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-2.6, -0.3, 0])
        sac = Ellipse(width=1.2, height=1.8, stroke_color=th.INK, stroke_width=3, fill_color="#1A1F38", fill_opacity=1).move_to(C)
        n1 = VGroup(E.nucleus(C, 0.13, PN))
        cnt = VGroup(T("nuclei", size=22, color=th.MUTED), Integer(1, font_size=60, color=th.AMBER)).arrange(DOWN, buff=0.08).move_to([1.6, 1.4, 0])
        with self.say("The functional megaspore grows, and its nucleus divides by mitosis three times, with no walls at all in between. A free nuclear stage."):
            self.play(FadeIn(head), FadeIn(sac), FadeIn(n1), FadeIn(cnt))
        big = Ellipse(width=2.6, height=5.0, stroke_color=th.INK, stroke_width=3, fill_color="#1A1F38", fill_opacity=1).move_to(C)
        n2 = VGroup(E.nucleus(C + UP * 1.5, 0.13, PN), E.nucleus(C + DOWN * 1.5, 0.13, PN))
        n4 = VGroup(*[E.nucleus(C + [dx, dy, 0], 0.12, PN) for dx, dy in [(-0.35, 1.6), (0.35, 1.6), (-0.35, -1.6), (0.35, -1.6)]])
        n8pos = [(-0.45, 1.85), (0.45, 1.85), (0, 1.35), (0, 0.55), (0, -0.55), (-0.45, -1.85), (0.45, -1.85), (0, -1.35)]
        n8 = VGroup(*[E.nucleus(C + [dx, dy, 0], 0.11, PN) for dx, dy in n8pos])
        with self.say("One becomes two, one at each pole. Two become four. Four become eight: four at each end of the sac.") as v:
            self.play(Transform(sac, big), Transform(n1, n2), cnt[1].animate.set_value(2), run_time=1.2)
            self.hold(v.dur * 0.15)
            self.play(Transform(n1, n4), cnt[1].animate.set_value(4), run_time=1.0)
            self.hold(v.dur * 0.15)
            self.play(Transform(n1, n8), cnt[1].animate.set_value(8), run_time=1.0)
        es = E.embryo_sac(2.6, 5.0).move_to(C)
        S = es.parts
        with self.say("Then walls form. Three nuclei at the micropylar end become cells of the egg apparatus: the egg, flanked by two synergids. Three at the chalazal end become the antipodals. And one nucleus from each end moves to the middle. These are the two polar nuclei, sharing the big central cell."):
            self.play(FadeOut(n1), FadeOut(sac), FadeIn(es))
            self.play(Indicate(VGroup(S["egg"], S["synergids"]), color=EGG))
            self.play(Indicate(S["antipodals"], color=ANT))
            self.play(Indicate(S["polar"], color=POLAR, scale_factor=1.6))
        tally = VGroup(para("3 antipodals + 2 synergids + 1 egg + 1 central cell", width=5.6, size=24, color=th.INK, align="center"), T("= 7 cells, 8 nuclei", size=34, color=th.AMBER, weight="BOLD")).arrange(DOWN, buff=0.2).move_to([3.4, -0.6, 0])
        ty = para("Polygonum type · monosporic · in over 80% of flowering plants", width=5.6, size=22, color=th.MUTED, align="center").next_to(tally, DOWN, buff=0.4)
        with self.say("Count. Three antipodals, two synergids, one egg, and one central cell with two nuclei. Seven cells, eight nuclei. It is the Polygonum type embryo sac. Monosporic, because it grows from one megaspore. Over eighty percent of flowering plants have it."):
            self.play(FadeIn(tally[0]))
            self.play(Write(tally[1]))
            self.play(FadeIn(ty))
        self.play(FadeOut(VGroup(head, es, cnt, tally, ty)))
        head, prob = B.example_head(self, "A pea pod has 8 seeds and no ovule was wasted. (a) How many megaspore mother cells? (b) How many megaspores formed, and how many degenerated? (c) How many mitoses made the 8 embryo sacs? (d) The least number of pollen grains needed?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 1 \text{ ovule per seed} \Rightarrow 8", size=36), M(r"\text{(b)}\ \ 8\times4 = 32 \text{ formed},\ \ 8 \times 3 = 24 \text{ degenerate}", size=36),
                       M(r"\text{(c)}\ \ 1 + 2 + 4 = 7 \text{ per sac};\ \ 8 \times 7 = 56", size=36), M(r"\text{(d)}\ \ 1 \text{ grain per ovule} \Rightarrow 8", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        says = ["A counting example on the female side.", "One seed, one ovule, one megaspore mother cell: eight.", "Each meiosis makes four megaspores: thirty two, of which three per ovule die, twenty four.",
                "Making one embryo sac takes three rounds of division: one, then two, then four nuclei dividing. Seven mitoses per sac, fifty six in all.", "And each pollen grain fertilises one ovule, so at least eight pollen grains."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.2)
        self.play(FadeOut(VGroup(head, prob, steps)))
        rows = [["part", "ploidy", "why"], ["nucellus, integuments, seed coat", "2n", "mother sporophyte"], ["megaspore mother cell", "2n", "before meiosis"], ["egg, synergids, antipodals", "n", "gametophyte cells"],
                ["zygote, embryo", "2n", "n + n"], ["primary endosperm nucleus, endosperm", "3n", "n + n + n"], ["perisperm (black pepper)", "2n", "leftover nucellus"]]
        tb = B.table(rows, [5.4, 1.6, 4.4], row_h=0.62, size=23, colors=[th.INK, th.AMBER, th.BODY]).move_to([0, 0.2, 0])
        with self.say("Ploidy questions come every year, and one rule answers them all. Anything belonging to the mother plant is two n. Anything in the gametophyte is n. Only the two products of double fertilization differ: the embryo is two n, the endosperm three n. And the perisperm of black pepper, which is leftover nucellus, is two n.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("A typical angiosperm embryo sac is",
                  ["7-celled and 8-nucleate", "8-celled and 8-nucleate", "7-celled and 7-nucleate", "8-celled and 7-nucleate"], 0,
                  "Pause and think. How many cells, and how many nuclei?",
                  "Seven cells and eight nuclei. Eight celled is the trap: the two polar nuclei share one central cell, so eight nuclei sit in only seven cells.")

    # ------------------------------------------------------------------ part 6: embryo
    def p6(self):
        self.section(5)
        head = T("The dicot embryo: Capsella bursa-pastoris", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-3.0, -0.55, 0])
        stages = ["two", "octant", "globular", "heart", "torpedo", "mature"]
        cur = E.capsella("two", 1.7).move_to(C)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=6.0, size=25)
        says = [("The zygote rests for a while, letting the endosperm get ahead. Then it divides by a transverse wall into a small apical cell, towards the chalaza, and a large basal cell, towards the micropyle.", "2-celled: apical cell + basal cell", "Transverse division of the zygote."),
                ("The basal cell divides again and again into a row of six to ten cells, the suspensor, which pushes the embryo deep into the endosperm. Its lowest cell swells into a haustorium. The apical cell divides into eight cells: the octant.", "Suspensor + octant", "Suspensor from the basal cell; upper four cells → plumule and cotyledons; lower four → hypocotyl."),
                ("Divisions parallel to the surface now mark out three layers: dermatogen, the future epidermis; periblem, the cortex; and plerome, the stele. The embryo is globular.", "Globular stage", "Dermatogen → epidermis, periblem → cortex, plerome → stele."),
                ("Two cotyledons bulge out at the top: the heart shaped stage.", "Heart-shaped stage", "Two cotyledon primordia appear."),
                ("They lengthen: the torpedo stage.", "Torpedo stage", "Cotyledons elongate."),
                ("And finally the mature embryo, with two cotyledons, a plumule between them, and a radicle at the suspensor end. The top cell of the suspensor, the hypophysis, forms the root tip and root cap.", "Mature embryo", "Two cotyledons, plumule, hypocotyl, radicle; hypophysis → root tip and cap.")]
        self.play(FadeIn(head))
        for i, (sy, t_, sub) in enumerate(says):
            with self.say(sy):
                new = E.capsella(stages[i], 1.7).move_to(C)
                if i == 0:
                    self.play(FadeIn(new))
                else:
                    self.play(ReplacementTransform(cur, new), run_time=1.2)
                cur = new
                cap(t_, color=P2N, sub=sub)
        self.play(FadeOut(VGroup(head, cur)))
        cap.clear()
        head = T("The monocot embryo: a maize grain", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-3.0, -0.3, 0])
        grain = Ellipse(width=3.6, height=5.0, stroke_color="#C9A27A", stroke_width=5, fill_color="#F3EBD6", fill_opacity=0.9).move_to(C)
        aleu = Ellipse(width=3.35, height=4.75, stroke_color=th.AMBER, stroke_width=5).move_to(C)
        scut = Ellipse(width=0.8, height=2.4, stroke_color=P2N, stroke_width=3, fill_color="#C5E8A0", fill_opacity=1).move_to(C + [0.9, -0.9, 0])
        emb_ax = RoundedRectangle(corner_radius=0.15, width=0.4, height=1.9, stroke_width=0, fill_color="#7BE495", fill_opacity=1).move_to(C + [1.45, -0.9, 0])
        cole = Arc(radius=0.35, start_angle=0, angle=PI, stroke_color=th.SKY, stroke_width=5).move_to(C + [1.45, 0.05, 0])
        coler = Arc(radius=0.35, start_angle=PI, angle=PI, stroke_color=th.PINK, stroke_width=5).move_to(C + [1.45, -1.85, 0])
        epi = Ellipse(width=0.18, height=0.4, stroke_width=0, fill_color=th.MINT, fill_opacity=1).move_to(C + [1.72, -0.9, 0])
        lab = VGroup(B.label("endosperm (3n)", [1.2, 2.0, 0], C + [-0.6, 0.8, 0], color="#E9D8A6", size=22),
                     B.label("aleurone layer", [1.2, 1.3, 0], aleu.point_at_angle(0.8), color=th.AMBER, size=22),
                     B.label("coleoptile (over the plumule)", [1.2, 0.5, 0], cole.get_center(), color=th.SKY, size=22),
                     B.label("scutellum: the one cotyledon", [1.2, -0.4, 0], scut.get_center(), color=P2N, size=22),
                     B.label("epiblast", [1.2, -1.2, 0], epi.get_center(), color=th.MINT, size=22),
                     B.label("coleorhiza (over the radicle)", [1.2, -2.0, 0], coler.get_center(), color=th.PINK, size=22))
        for l_ in lab:
            l_[1].align_to(np.array([1.0, 0, 0]), LEFT)
            l_[0].put_start_and_end_on(l_[1].get_left() + LEFT * 0.08, l_[0].get_end())
        with self.say("A grass embryo starts the same way, but makes only one cotyledon, and it lies to one side of a huge endosperm. That single cotyledon is the shield shaped scutellum, pressed against the endosperm. Its surface layer secretes enzymes and absorbs the digested food."):
            self.play(FadeIn(head), FadeIn(grain), FadeIn(aleu))
            self.play(FadeIn(scut), FadeIn(emb_ax))
            self.play(FadeIn(lab[0]), FadeIn(lab[3]))
        with self.say("The young shoot is wrapped in a protective sheath, the coleoptile, which pushes up through the soil. The radicle is wrapped in a coleorhiza. A small flap opposite the scutellum, the epiblast, may be the remnant of a second cotyledon. And the outer layer of the endosperm is the protein rich aleurone layer."):
            self.play(Create(cole), FadeIn(lab[2]))
            self.play(Create(coler), FadeIn(lab[5]))
            self.play(FadeIn(epi), FadeIn(lab[4]))
            self.play(FadeIn(lab[1]))
        self.play(FadeOut(VGroup(head, grain, aleu, scut, emb_ax, cole, coler, epi, lab)))
        rows = [["", "dicot embryo", "monocot embryo"], ["cotyledons", "two, lateral", "one: the scutellum"], ["position", "central", "to one side of the endosperm"], ["plumule", "terminal, naked", "lateral, in a coleoptile"],
                ["radicle", "naked", "in a coleorhiza"], ["food store", "usually the cotyledons", "the endosperm"], ["examples", "Capsella, pea, gram", "maize, wheat, rice"]]
        tb = B.table(rows, [2.6, 4.4, 5.0], row_h=0.62, size=23, colors=[th.MUTED, P2N, th.SKY]).move_to([0, 0.2, 0])
        with self.say("The comparison: number and position of cotyledons, the plumule and radicle naked or sheathed, where the food is stored, and examples.") as v:
            B.reveal_table(self, tb, max(2.5, v.dur * 0.9))
        self.wait(1.5)
        self.play(FadeOut(tb))
        self.quiz("The scutellum of a maize grain is the",
                  ["coleoptile", "endosperm", "single cotyledon", "perisperm"], 2,
                  "Pause and think. What is the scutellum?",
                  "The single cotyledon of a grass embryo, shaped like a shield. The coleoptile is the sheath over the shoot, and the endosperm is the food the scutellum absorbs from.")

    # ------------------------------------------------------------------ part 7: endosperm
    def p7(self):
        self.section(6)
        d = self.callout("key", "Endosperm: the triploid (3n) nutritive tissue of the seed, grown from the primary endosperm nucleus after triple fusion. It feeds the embryo, and often the seedling too.", width=11, size=27)
        with self.say("The endosperm is the triploid food tissue of the seed, grown from the primary endosperm nucleus. It feeds the developing embryo, and in many seeds the seedling as well. It grows in one of three ways."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        head = T("Nuclear endosperm (the commonest)", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-2.8, -0.3, 0])
        sac = Ellipse(width=3.4, height=4.8, stroke_color=th.INK, stroke_width=3, fill_color="#1A1F38", fill_opacity=1).move_to(C)
        rng = np.random.default_rng(5)
        pts = [C + np.array([1.5 * np.cos(a) * 0.86, 2.2 * np.sin(a) * 0.86, 0]) for a in np.linspace(0, TAU, 28, endpoint=False)]
        nuc = VGroup(*[E.nucleus(p, 0.08, P3N) for p in pts])
        one = E.nucleus(C, 0.14, P3N)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.8, size=25)
        with self.say("In nuclear endosperm, the commonest kind, the primary endosperm nucleus divides again and again with no walls: a free nuclear stage. The nuclei spread round the edge of a big central vacuole."):
            self.play(FadeIn(head), FadeIn(sac), FadeIn(one))
            self.play(ReplacementTransform(one, nuc), run_time=2.0)
            cap("Free-nuclear divisions: no walls", color=P3N, sub="Maize, wheat, rice, Capsella, coconut.")
        walls = VGroup(*[Line(C + np.array([1.7 * np.cos(a) * 0.99, 2.4 * np.sin(a) * 0.99, 0]), C + np.array([1.7 * np.cos(a) * 0.68, 2.4 * np.sin(a) * 0.68, 0]), color=P3N, stroke_width=2) for a in np.linspace(0, TAU, 28, endpoint=False) + PI / 28])
        inner = Ellipse(width=3.4 * 0.68, height=4.8 * 0.68, stroke_color=P3N, stroke_width=2).move_to(C)
        water = Ellipse(width=3.4 * 0.64, height=4.8 * 0.64, stroke_width=0, fill_color=th.SKY, fill_opacity=0.25).move_to(C)
        with self.say("Later, walls form from the edge inwards. In a coconut you can see both stages at once. The white meat is cellular endosperm. The coconut water is endosperm still in its free nuclear, liquid stage. Both are triploid."):
            self.play(Create(walls), Create(inner))
            self.play(FadeIn(water))
            cap("Coconut: water = free-nuclear endosperm; meat = cellular endosperm", color=th.SKY, sub="Both 3n.")
        self.play(FadeOut(VGroup(head, sac, nuc, walls, inner, water)))
        cap.clear()
        rows = [["type", "how it develops", "examples"], ["nuclear", "free nuclei first; walls later or never", "maize, wheat, rice, coconut"], ["cellular", "a wall after every division from the start", "Datura, Petunia, balsam"],
                ["helobial", "first wall makes two unequal chambers; then free-nuclear", "Alisma, Eremurus (Helobiales)"]]
        tb = B.table(rows, [2.2, 6.0, 4.2], row_h=0.72, size=23, colors=[P3N, th.INK, th.BODY]).move_to([0, 0.6, 0])
        rum = para("Ruminate endosperm: the seed coat folds into it irregularly, as in betel nut and nutmeg.", width=11, size=24, color=th.MUTED).move_to([0, -2.2, 0])
        with self.say("Cellular endosperm puts a wall after every division right from the start, as in Datura and Petunia. Helobial endosperm is in between: the first division makes two unequal chambers, and then it goes free nuclear. And when the seed coat folds irregularly into the endosperm, as in betel nut and nutmeg, it is called ruminate.") as v:
            B.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(rum))
        self.play(FadeOut(VGroup(tb, rum)))
        head = T("Does the seed keep its endosperm?", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        s1 = VGroup(Ellipse(width=2.6, height=3.4, stroke_color="#C9A27A", stroke_width=5, fill_color="#F3EBD6", fill_opacity=1),
                    Ellipse(width=0.8, height=1.2, stroke_width=0, fill_color="#7BE495", fill_opacity=1).shift(DOWN * 1.0 + RIGHT * 0.6)).move_to([-3.4, -0.2, 0])
        s2 = VGroup(Circle(radius=1.5, stroke_color="#C9A27A", stroke_width=5, fill_color="#2E5E3A", fill_opacity=1),
                    Line(UP * 1.45, DOWN * 1.45, color="#C9A27A", stroke_width=3), Ellipse(width=0.4, height=0.6, stroke_width=0, fill_color="#7BE495", fill_opacity=1).move_to([0, -1.2, 0])).move_to([3.4, -0.2, 0])
        l1 = VGroup(T("endospermic (albuminous)", size=26, color=P3N, weight="BOLD"), T("maize, wheat, rice, castor, coconut", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(s1, DOWN, buff=0.3)
        l2 = VGroup(T("non-endospermic (exalbuminous)", size=26, color=P2N, weight="BOLD"), T("pea, gram, bean, groundnut, mustard", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(s2, DOWN, buff=0.3)
        with self.say("Seeds split two ways. In endospermic, or albuminous, seeds the endosperm stays in the mature seed as the food store, and the cotyledons stay thin: maize, wheat, rice, castor and coconut. In cereals, the aleurone layer secretes alpha amylase on germination to digest the starch."):
            self.play(FadeIn(head), FadeIn(s1), FadeIn(l1))
        with self.say("In non endospermic, or exalbuminous, seeds the developing embryo eats up the endosperm completely, and stores the food in its own fleshy cotyledons instead: pea, gram, bean and groundnut."):
            self.play(FadeIn(s2), FadeIn(l2))
        self.play(FadeOut(VGroup(head, s1, s2, l1, l2)))
        self.tip("Endosperm = 3n, from triple fusion. Cotyledon = 2n, part of the embryo. Perisperm = 2n, leftover nucellus (black pepper, beet).",
                 "Exam tip. Three food stores, three origins. Endosperm is three n, from triple fusion. A cotyledon is two n, part of the embryo. Perisperm is two n, leftover nucellus, as in black pepper and beet. A one mark difference that comes up every other year.")
        self.quiz("Coconut water is",
                  ["free-nuclear endosperm", "perisperm", "nucellus", "liquid mesocarp"], 0,
                  "Last check. What is coconut water?",
                  "Free nuclear endosperm: the liquid stage of nuclear endosperm, so it is triploid. The white meat around it is the same endosperm after walls have formed. It is not perisperm, which is nucellus.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Asexual reproduction gives clones; sexual reproduction gives variation.",
            "Pollination: autogamy, geitonogamy, xenogamy; wind, water, insect, bird, bat.",
            "Double fertilization: n + n = 2n zygote; n + n + n = 3n endosperm.",
            "Anther: epidermis, endothecium (opens), middle layers, tapetum (feeds).",
            "Embryo sac: Polygonum type, 7 cells and 8 nuclei.",
            "Capsella: octant → globular → heart → torpedo. Maize: scutellum. Endosperm: nuclear, cellular, helobial.",
        ], "Quick recap. Asexual reproduction makes clones, sexual reproduction makes variation. Pollination is autogamy, geitonogamy or xenogamy, carried by wind, water, insects, birds or bats. Double fertilization gives a two n zygote and a three n endosperm. The anther wall is epidermis, endothecium, middle layers and tapetum, which feeds the pollen. The embryo sac has seven cells and eight nuclei. The Capsella embryo goes octant, globular, heart, torpedo; the maize embryo has a scutellum. And endosperm is nuclear, cellular or helobial.")
        self.outro("That was embryology. Draw the embryo sac and the anther once from memory, and label every ploidy. Next, biotechnology: tissue culture, plant breeding, and genetically modified crops. See you there.")
