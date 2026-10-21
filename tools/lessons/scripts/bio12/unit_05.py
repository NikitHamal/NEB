import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
import _gen as G  # noqa: E402
from _gen import BASE  # noqa: E402

AUX = "#FFB547"
CYT = "#4CC9F0"
PLANT = "#5FB04A"


def flask(x, y, w=1.3, h=1.7, fill="#3E5A2A"):
    body = Polygon([x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + 0.18, y + h * 0.15, 0], [x + 0.18, y + h / 2, 0], [x - 0.18, y + h / 2, 0], [x - 0.18, y + h * 0.15, 0],
                   stroke_color=th.BODY, stroke_width=3, fill_opacity=0)
    med = Polygon([x - w / 2 + 0.05, y - h / 2 + 0.05, 0], [x + w / 2 - 0.05, y - h / 2 + 0.05, 0], [x + w * 0.3, y - h * 0.2, 0], [x - w * 0.3, y - h * 0.2, 0], stroke_width=0, fill_color=fill, fill_opacity=0.7)
    return VGroup(med, body)


def plantlet(scale=1.0, roots=True, shoots=True):
    g = VGroup()
    if shoots:
        g.add(Line(ORIGIN, UP * 0.6 * scale, color=PLANT, stroke_width=4), *[Ellipse(width=0.3 * scale, height=0.14 * scale, stroke_width=0, fill_color=PLANT, fill_opacity=1).rotate(s * 0.5).move_to([s * 0.14 * scale, (0.35 + 0.15 * k) * scale, 0]) for k, s in enumerate((1, -1))])
    if roots:
        g.add(*[Line(ORIGIN, [d * 0.25 * scale, -0.35 * scale, 0], color="#E9D8A6", stroke_width=2.5) for d in (-1, 0, 1)])
    return g


def polar_(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 5
    TITLE = "Biotechnology"
    SUBTITLE = "Putting living things to work"
    SECTIONS = ["Tissue culture", "Plant breeding", "Disease-resistant plants", "Green manure, bio-fertilizer, bio-pesticide",
                "Genetic engineering and GMOs", "Bio-engineering", "Food safety and food security"]
    NEXT = "Unit 6 · Animal Tissues"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        bud = plantlet(1.4).move_to([0, 0.2, 0])
        cnt = VGroup(T("plants", size=24, color=th.MUTED), Integer(1, font_size=64, color=th.AMBER)).arrange(DOWN, buff=0.05).move_to([4.6, 2.0, 0])
        wk = VGroup(T("week", size=24, color=th.MUTED), Integer(0, font_size=48, color=th.INK)).arrange(DOWN, buff=0.05).move_to([-4.6, 2.0, 0])
        with self.say("A banana plant cannot make useful seeds. It is a sterile triploid. So how do you get thousands of identical, disease free banana plants for a new orchard? You start with one tiny bud."):
            self.play(FadeIn(bud, scale=0.5), FadeIn(cnt), FadeIn(wk))
        grid = VGroup()
        with self.say("Every four weeks, in a glass jar of jelly, each shoot is split into four. Four. Sixteen. Sixty four. After twenty four weeks, six rounds: four thousand and ninety six plants, from one bud.") as v:
            n = 1
            cur = VGroup(bud)
            for k in range(1, 7):
                n *= 4
                side = int(np.ceil(np.sqrt(min(n, 256))))
                s = 3.6 / side
                new = VGroup(*[plantlet(max(0.12, s * 0.9)).move_to([(i % side - (side - 1) / 2) * s, ((side - 1) / 2 - i // side) * s * 0.95 - 0.2, 0]) for i in range(min(n, 256))])
                self.play(ReplacementTransform(cur, new), cnt[1].animate.set_value(n), wk[1].animate.set_value(4 * k), run_time=max(0.5, v.dur * 0.13))
                cur = new
            self.sfx("impact", gain=-12)
        nb = B.neby_in(self, "surprised", height=1.4)
        with self.say("Every one of them is a perfect copy of the parent. That is biotechnology: using living cells to make what people need. And it is older than you think. Curd, gundruk, jaand and chhurpi are all biotechnology."):
            pass
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(cur, cnt, wk)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 5: Biotechnology. Growing whole plants from a few cells, breeding better crops, moving genes between species, and keeping our food both sufficient and safe."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Our path. Tissue culture. Plant breeding. Disease resistant plants, including Bt crops. Green manure, bio fertilizers and bio pesticides. Genetic engineering, PCR, gels and GMOs. Bio engineering. And food safety and food security.")

    # ------------------------------------------------------------------ part 1: tissue culture
    def p1(self):
        self.section(0)
        d = self.callout("key", "Plant tissue culture: growing cells, tissues or organs on a sterile, defined nutrient medium under controlled conditions (in vitro). It rests on TOTIPOTENCY: one living plant cell can regenerate a whole plant.", width=11, size=27)
        with self.say("Plant tissue culture is growing plant cells, tissues or organs on a sterile nutrient medium, in glass, under controlled light and temperature. It works because of totipotency: a single living plant cell carries all the instructions to rebuild a whole plant."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        head = T("Steward, 1957: one carrot cell → one carrot plant", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        c1 = Circle(radius=0.3, stroke_color=PLANT, stroke_width=3, fill_color="#1E4A2C", fill_opacity=1).move_to([-4.6, -0.3, 0])
        callus = VGroup(*[Circle(radius=0.16, stroke_color=PLANT, stroke_width=2, fill_color="#1E4A2C", fill_opacity=1).move_to([-1.6 + 0.28 * np.cos(a) * r, -0.3 + 0.28 * np.sin(a) * r, 0])
                          for r, n in [(0, 1), (1, 6), (2, 12)] for a in np.linspace(0, TAU, n, endpoint=False)])
        pl = VGroup(plantlet(2.4).move_to([1.6, -0.1, 0]))
        carrot = VGroup(Polygon([4.6, -0.6, 0], [4.9, -0.6, 0], [4.75, -2.4, 0], stroke_width=0, fill_color="#F08A24", fill_opacity=1),
                        *[Line([4.75, -0.6, 0], [4.75 + d, 0.6, 0], color=PLANT, stroke_width=4) for d in (-0.4, 0, 0.4)])
        labs = VGroup(*[T(s_, size=22, color=th.BODY).move_to([x, -2.7, 0]) for s_, x in [("one phloem cell", -4.6), ("callus", -1.6), ("plantlet", 1.6), ("whole carrot", 4.75)]])
        arr = VGroup(*[Arrow([a, -0.3, 0], [b, -0.3, 0], buff=0, color=th.MUTED, stroke_width=3) for a, b in [(-4.1, -2.5), (-0.7, 0.8), (2.4, 4.0)]])
        with self.say("Haberlandt predicted it in nineteen oh two. Steward proved it in nineteen fifty seven. He took single cells from carrot phloem, floated them in coconut water, and watched each one divide into a lump, then a plantlet, then a whole carrot."):
            self.play(FadeIn(head), FadeIn(c1), FadeIn(labs[0]))
            self.play(GrowArrow(arr[0]), TransformFromCopy(c1, callus), FadeIn(labs[1]))
            self.play(GrowArrow(arr[1]), FadeIn(pl), FadeIn(labs[2]))
            self.play(GrowArrow(arr[2]), FadeIn(carrot), FadeIn(labs[3]))
        self.play(FadeOut(VGroup(head, c1, callus, pl, carrot, labs, arr)))
        rows = [["component", "examples", "role"], ["macronutrients", "N, P, K, Ca, Mg, S salts", "bulk nutrition"], ["micronutrients", "Fe, Mn, Zn, B, Cu, Mo", "enzyme cofactors"],
                ["carbon source", "sucrose, 2–3%", "energy: cultures do not photosynthesise"], ["vitamins, glycine", "thiamine, nicotinic acid, inositol", "growth factors"],
                ["growth regulators", "auxin (IAA, NAA, 2,4-D) + cytokinin (kinetin, BAP)", "decide what forms"], ["agar, 0.8%", "", "gel support"]]
        tb = B.table(rows, [3.0, 5.6, 4.4], row_h=0.6, size=22, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 0.3, 0])
        h2 = T("MS medium (Murashige and Skoog, 1962)", size=28, color=th.INK, weight="BOLD").next_to(tb, UP, buff=0.25)
        with self.say("The standard jelly is M S medium, from Murashige and Skoog. Mineral salts, big and small. Sucrose for energy, because the cultures cannot feed themselves by photosynthesis. Vitamins. Agar to set it. And, most important, plant hormones: an auxin and a cytokinin.") as v:
            self.play(FadeIn(h2))
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(tb, h2)))
        self.p1_ratio()
        self.p1_steps()

    def p1_ratio(self):
        head = T("The auxin : cytokinin ratio decides", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        r = ValueTracker(0.0)
        fl = flask(0, -0.6, w=2.6, h=3.0)

        def growth():
            v = r.get_value()
            g = VGroup()
            base = np.array([0, -1.45, 0])
            cal = VGroup(*[Circle(radius=0.13, stroke_color=PLANT, stroke_width=1.5, fill_color="#1E4A2C", fill_opacity=1).move_to(base + [0.24 * np.cos(a) * k, 0.12 + 0.18 * np.sin(a) * k * 0.5, 0])
                           for k, n in [(0, 1), (1, 5), (2, 9)] for a in np.linspace(0, TAU, n, endpoint=False)])
            g.add(cal)
            if v < -0.2:
                s = min(1, (-v - 0.2) / 0.8)
                g.add(*[Line(base + [d * 0.3, 0, 0], base + [d * 0.6 * s, -0.35 * s, 0], color="#E9D8A6", stroke_width=3) for d in (-1, -0.4, 0.4, 1)])
            if v > 0.2:
                s = min(1, (v - 0.2) / 0.8)
                for d in (-0.35, 0, 0.35):
                    g.add(Line(base + [d, 0.3, 0], base + [d * 1.4, 0.3 + 0.9 * s, 0], color=PLANT, stroke_width=4),
                          Ellipse(width=0.32 * s + 0.01, height=0.14 * s + 0.01, stroke_width=0, fill_color=PLANT, fill_opacity=1).move_to(base + [d * 1.4 + 0.1, 0.3 + 0.9 * s, 0]))
            return g

        gr = always_redraw(growth)
        bar = always_redraw(lambda: VGroup(Rectangle(width=0.5, height=1.5 + 1.2 * max(-r.get_value(), 0) - 0.6 * max(r.get_value(), 0), stroke_width=0, fill_color=AUX, fill_opacity=0.9).move_to([-5.2, -1.4, 0], aligned_edge=DOWN),
                                           Rectangle(width=0.5, height=1.5 + 1.2 * max(r.get_value(), 0) - 0.6 * max(-r.get_value(), 0), stroke_width=0, fill_color=CYT, fill_opacity=0.9).move_to([-3.7, -1.4, 0], aligned_edge=DOWN)))
        bl = VGroup(T("auxin", size=22, color=AUX).move_to([-5.2, -1.75, 0]), T("cytokinin", size=22, color=CYT).move_to([-3.7, -1.75, 0]))
        cap = B.Captions(self, at=(4.0, 0.0, 0), width=4.8, size=26)
        self.add(gr, bar)
        with self.say("Skoog and Miller found that the ratio of the two hormones decides what the tissue becomes. With both roughly equal, the cells just keep dividing into an unorganised lump, the callus."):
            self.play(FadeIn(head), FadeIn(fl), FadeIn(bl))
            cap("Equal: callus", color=PLANT, sub="An unorganised mass of dividing cells.")
        with self.say("Raise the auxin, lower the cytokinin, and roots grow."):
            self.play(r.animate.set_value(-1.0), run_time=2.0)
            cap("High auxin : low cytokinin → ROOTS", color=AUX)
        with self.say("Turn it the other way, high cytokinin, low auxin, and shoots grow instead. Grow shoots first, then move them onto a root medium, and you have plantlets."):
            self.play(r.animate.set_value(1.0), run_time=2.4)
            cap("Low auxin : high cytokinin → SHOOTS", color=CYT)
        self.play(FadeOut(VGroup(head, fl, gr, bar, bl)))
        self.remove(gr, bar)
        cap.clear()

    def p1_steps(self):
        head = T("The steps", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        steps = [("explant", "a shoot tip, node, leaf disc or embryo from a healthy plant"), ("sterilise", "70% ethanol, then 0.1% HgCl₂ or 1% NaOCl, then rinses"), ("inoculate", "onto medium, in a laminar air-flow cabinet"),
                 ("callus", "25 °C, 16 h light; subculture every 3–4 weeks"), ("shoots, then roots", "high-cytokinin medium, then high-auxin medium"), ("hardening", "greenhouse, high humidity, then slowly to normal air"), ("field", "")]
        chips = VGroup()
        for i, (a, b) in enumerate(steps):
            c_ = VGroup(RoundedRectangle(corner_radius=0.15, width=1.65, height=0.8, stroke_color=self.color, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1), para(a, width=1.5, size=20, color=th.INK, align="center"))
            c_[1].move_to(c_[0])
            chips.add(c_)
        chips.arrange(RIGHT, buff=0.22).move_to([0, 1.0, 0])
        arr = VGroup(*[Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.02, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.4) for i in range(6)])
        cap = B.Captions(self, at=(0, -1.2, 0), width=11.5, size=26)
        says = ["Step one, the explant: a small piece from a healthy, disease free mother plant.", "Step two, surface sterilisation, because a single fungal spore would overrun the jar. Ethanol, then mercuric chloride or bleach, then sterile water.",
                "Step three, inoculation onto the medium, inside a laminar air flow cabinet.", "Step four, incubation: the explant grows a callus, which is cut up and moved to fresh medium every three or four weeks.",
                "Step five: high cytokinin for shoots, then high auxin for roots.", "Step six, hardening. The tender plantlets have lived in a humid jar, so they are moved slowly, through a humid greenhouse, to normal air.", "And step seven, the field."]
        self.play(FadeIn(head))
        for i, sy in enumerate(says):
            with self.say(sy):
                self.play(FadeIn(chips[i], shift=UP * 0.2), *([GrowArrow(arr[i - 1])] if i else []), run_time=0.5)
                cap(steps[i][0].capitalize(), color=self.color, sub=steps[i][1] or None)
        self.play(FadeOut(VGroup(head, chips, arr)))
        cap.clear()
        rows = [["culture", "what grows", "chief use"], ["callus", "unorganised mass", "regeneration; somaclonal variation"], ["suspension", "free cells in shaken liquid", "secondary metabolites, industrially"],
                ["meristem / shoot tip", "0.2–0.5 mm apical dome", "VIRUS-FREE plants"], ["anther / pollen", "microspores", "HAPLOIDS → instant pure lines"], ["embryo rescue", "a young hybrid embryo", "saves wide crosses"],
                ["protoplast", "wall-less cells", "somatic hybrids: 'pomato'"]]
        tb = B.table(rows, [3.2, 4.2, 5.2], row_h=0.6, size=22, colors=[th.AMBER, th.BODY, th.INK]).move_to([0, 0.3, 0])
        with self.say("There are several kinds of culture, each with its use. Meristem culture gives virus free plants, because viruses do not reach the growing tip; that is how virus free seed potato is made. Anther culture gives haploid plants, and doubling them with colchicine gives perfectly pure lines in one step. Embryo rescue saves hybrids that would otherwise die in the seed. And fusing the naked protoplasts of two species gives somatic hybrids, like the pomato, potato plus tomato.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        head, prob = B.example_head(self, "A banana shoot-tip explant is subcultured every 4 weeks, and each subculture multiplies the shoots by 4. (a) How many shoots after 24 weeks? (b) If 5% are lost during hardening, how many plants reach the field?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 24 \div 4 = 6 \text{ subcultures};\ \ N = 1 \times 4^6 = 4096", size=38), M(r"\text{(b)}\ \ 4096 \times 0.95 = 3891.2 \approx 3891 \text{ plants}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["Here is the cold open as an exam question.", "Twenty four weeks is six subcultures of four weeks, and each multiplies by four: four to the power six, four thousand and ninety six shoots.", "Lose five percent in hardening, and ninety five percent survive: about three thousand eight hundred and ninety one plants."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.4)
        self.play(FadeOut(VGroup(head, prob, steps)))
        uses = VGroup(*[para(s_, width=11.5, size=24, color=th.INK) for s_ in ["micropropagation: banana, orchid, potato, sugarcane, strawberry (labs in Kathmandu and Chitwan)", "virus-free seed potato from meristems",
                                                                 "germplasm stored in liquid nitrogen at −196 °C", "the last step of every plant genetic-engineering project"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.6, 0])
        lim = para("Limits: expensive, needs skilled staff and strict asepsis; one contamination ruins a batch; unwanted somaclonal variation.", width=11.5, size=24, color=th.CORAL).move_to([0, -2.2, 0])
        with self.say("Its uses: mass propagation of banana, orchids, potato and sugarcane, in commercial labs right here in Kathmandu and Chitwan. Virus free seed potato. Storing germplasm frozen in liquid nitrogen. And every genetically engineered plant must pass through tissue culture, to turn one changed cell into a whole plant. Its limits: cost, skill, contamination, and unwanted somaclonal variation.") as v:
            for u_ in uses:
                self.play(FadeIn(u_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.13)
            self.play(FadeIn(lim))
        self.play(FadeOut(VGroup(uses, lim)))

    # ------------------------------------------------------------------ part 2: plant breeding
    def p2(self):
        self.section(1)
        d = self.callout("key", "Plant breeding: the deliberate improvement of the heredity of crop plants — yield, quality, resistance — by selecting and recombining the variation in a species and its relatives.", width=11, size=27).move_to([0, 1.4, 0])
        obj = VGroup(*[T(s_, size=24, color=th.INK) for s_ in ["higher yield · better quality (protein, oil, vitamins)", "resistance to disease and pests · tolerance of drought, cold, salt",
                                                                "early maturity: two or three crops a year", "dwarf, stiff straw that does not lodge"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.3, 0])
        with self.say("Plant breeding is the deliberate improvement of crops: more yield, better quality, resistance to disease and pests, tolerance of drought and cold, early maturity so two or three crops fit in a year, and short stiff straw that does not fall over under heavy grain.") as v:
            self.play(FadeIn(d, shift=UP * 0.2))
            for o_ in obj:
                self.play(FadeIn(o_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.1)
        self.play(FadeOut(VGroup(d, obj)))
        head = T("Hybridisation: making the cross by hand", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        import _emb as E
        fl = E.flower(1.1).move_to([-3.0, -0.3, 0])
        P = fl.parts
        bag = RoundedRectangle(corner_radius=0.3, width=3.6, height=4.2, stroke_color=th.MUTED, stroke_width=3, fill_color=th.MUTED, fill_opacity=0.12).move_to([-3.0, 0.0, 0])
        tag = VGroup(Rectangle(width=0.9, height=0.5, stroke_color=th.AMBER, stroke_width=2), T("tagged", size=18, color=th.AMBER)).move_to([-0.8, -2.0, 0])
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.6, size=25)
        with self.say("The heart of a breeding programme is the cross. First, collect germplasm, the landraces and wild relatives, into a gene bank, and choose two parents. Then, on the female parent, remove the anthers before they shed pollen. That is emasculation."):
            self.play(FadeIn(head), FadeIn(fl))
            self.play(P["stamens"].animate.shift(UP * 2.5 + RIGHT * 1.5).set_opacity(0), run_time=1.2)
            cap("Emasculation", color=th.CORAL, sub="Anthers removed before they dehisce, so the flower cannot pollinate itself.")
        with self.say("Cover the flower with a bag, so no stray pollen arrives. When the stigma is ready, dust it with pollen from the chosen male parent, bag it again, and tag it."):
            self.play(FadeIn(bag))
            cap("Bagging, then pollination, then tagging", color=th.AMBER)
            self.play(Flash(P["stigma"], color=th.AMBER), FadeIn(tag))
        with self.say("Then years of work. Self the F one, select the best plants from the F two onwards, generation after generation, test them at many sites, and release the best through the National Seed Board."):
            cap("Select from F₂ on → multi-site trials → release", sub="Released by the National Seed Board, then certified seed is multiplied.")
        self.play(FadeOut(VGroup(head, fl, bag, tag)))
        cap.clear()
        meth = VGroup(*[T(s_, size=24, color=th.INK) for s_ in ["introduction of a variety from elsewhere", "selection: mass, pure-line, clonal", "hybridisation: intervarietal, interspecific, intergeneric",
                                                                 "mutation breeding: gamma rays, EMS", "polyploidy breeding: colchicine", "marker-assisted selection: pick the right seedling by its DNA"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.3, 0])
        h2 = T("Methods of breeding", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("The methods. Introduction, selection, hybridisation, mutation breeding, polyploidy breeding, and the newest, marker assisted selection, where a DNA test on a seedling tells the breeder which plant carries the gene, without waiting for it to grow up.") as v:
            self.play(FadeIn(h2))
            for m_ in meth:
                self.play(FadeIn(m_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.1)
        self.play(FadeOut(VGroup(h2, meth)))
        ax = VGroup(*[VGroup(Rectangle(width=1.0, height=h_, stroke_width=0, fill_color=c_, fill_opacity=0.9).move_to([x, -2.0 + h_ / 2, 0]), T(n_, size=22, color=th.INK).move_to([x, -2.35, 0]))
                      for x, h_, c_, n_ in [(-4.8, 1.6, th.SKY, "wheat 1960"), (-3.4, 3.4, th.AMBER, "Green Revolution")]])
        gr = para("Borlaug's semi-dwarf, rust-resistant wheats and IRRI's IR8 rice (1966) roughly doubled cereal yields in South Asia. NARC in Nepal released wheat Bhrikuti and Gautam, rice Sabitri, Radha-4 and Khumal-4, maize Rampur Composite and Manakamana-3.", width=7.0, size=23, color=th.INK).move_to([2.6, 0.0, 0])
        with self.say("Breeding on a national scale was the Green Revolution of the nineteen sixties. Norman Borlaug's short, rust resistant wheats and the rice I R eight roughly doubled cereal yields across South Asia. Here, the Nepal Agricultural Research Council has released wheats like Bhrikuti and Gautam, rices like Sabitri and Khumal four, and maize like Rampur Composite."):
            self.play(LaggedStart(*[GrowFromEdge(a_[0], DOWN) for a_ in ax], lag_ratio=0.4), FadeIn(VGroup(*[a_[1] for a_ in ax])))
            self.play(FadeIn(gr))
        self.play(FadeOut(VGroup(ax, gr)))
        hb = VGroup(*[VGroup(Rectangle(width=1.1, height=h_, stroke_width=0, fill_color=c_, fill_opacity=0.9).move_to([x, -2.0 + h_ / 2, 0]), T(n_, size=22, color=th.INK).move_to([x, -2.35, 0]))
                      for x, h_, c_, n_ in [(-4.6, 2.0, th.SKY, "inbred A"), (-3.2, 1.8, th.PINK, "inbred B"), (-1.8, 3.6, th.AMBER, "F₁ hybrid"), (-0.4, 2.4, th.MUTED, "F₂")]])
        txt = para("Heterosis: an F₁ beats both parents. Inbreeding depression: vigour falls when a cross-pollinated crop like maize is selfed. The F₂ segregates and loses the vigour, so hybrid seed must be bought fresh every season.", width=5.6, size=23, color=th.INK).move_to([3.6, 0.3, 0])
        with self.say("Two ideas behind hybrid seed. Heterosis, or hybrid vigour: the F one of two inbred lines outgrows both parents. And inbreeding depression: maize selfed again and again gets weaker. Save seed from a hybrid, and the F two segregates and loses its vigour. That is why farmers must buy hybrid seed fresh every season. And the newest goal is biofortification: crops richer in iron, zinc or vitamins."):
            self.play(LaggedStart(*[GrowFromEdge(h_[0], DOWN) for h_ in hb[:3]], lag_ratio=0.3), FadeIn(VGroup(*[h_[1] for h_ in hb[:3]])))
            self.play(GrowFromEdge(hb[3][0], DOWN), FadeIn(hb[3][1]))
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(hb, txt)))

    # ------------------------------------------------------------------ part 3: disease resistance
    def p3(self):
        self.section(2)
        rows = [["", "vertical (race-specific)", "horizontal (field)"], ["genes", "one or a few major genes", "many genes, each small"], ["effect", "complete, against SOME races", "partial, against ALL races"],
                ["durability", "breaks down when a new race appears", "durable"], ["breeding", "simple", "difficult"]]
        tb = B.table(rows, [2.4, 5.2, 4.6], row_h=0.66, size=23, colors=[th.MUTED, th.CORAL, th.MINT]).move_to([0, 0.6, 0])
        with self.say("A plant is resistant when it can stop or limit infection. Vertical resistance comes from one or a few major genes. It gives complete protection, but only against some races of the pathogen, and it breaks down when a new race appears. Horizontal resistance comes from many small genes: only partial, but against every race, and it lasts.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        head = T("Flor's gene-for-gene hypothesis (1956)", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        grid, sq, tx = G.punnett(["R", "r"], ["Avr", "avr"], [["resists", "disease"], ["disease", "disease"]], cell=1.7, size=24)
        grid.move_to([-1.5, -0.4, 0])
        ll = VGroup(T("plant gene", size=22, color=th.AMBER).next_to(grid, LEFT, buff=0.2), T("pathogen gene", size=22, color=th.AMBER).next_to(grid, UP, buff=0.1))
        with self.say("Flor explained vertical resistance. For every resistance gene, R, in the host, there is a matching avirulence gene, Avr, in the pathogen. The plant resists only when both are present, like a lock that only works with its key. In every other combination, the disease wins."):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(ll))
            self.play(sq[(0, 0)].animate.set_fill(th.MINT, opacity=0.5), *[sq[k].animate.set_fill(th.CORAL, opacity=0.35) for k in [(0, 1), (1, 0), (1, 1)]])
        self.play(FadeOut(VGroup(head, grid, ll)))
        meth = VGroup(*[para(s_, width=11.5, size=24, color=th.INK) for s_ in ["sources: wild relatives and old landraces, kept in gene banks", "backcross method: cross the gene in, backcross to the good variety again and again",
                                                                 "mutation breeding: mildew-resistant barley (mlo)", "genetic engineering: a gene from any organism at all"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        with self.say("Where do resistance genes come from? Wild relatives and old landraces, which is why gene banks matter. Nepal's mid hill terraces still hold rice and barley landraces with genes modern varieties have lost. They are moved by the backcross method, by mutation breeding, or by genetic engineering, which can bring in a gene from any organism at all.") as v:
            for m_ in meth:
                self.play(FadeIn(m_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.17)
        self.play(FadeOut(meth))
        self.p3_bt()

    def p3_bt(self):
        head = T("How the Bt toxin kills a caterpillar", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        crys = Square(side_length=0.7, stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.5).rotate(PI / 4).move_to([-5.0, 1.0, 0])
        cl = T("inactive crystal protoxin", size=22, color=th.AMBER).next_to(crys, DOWN, buff=0.2)
        gut = RoundedRectangle(corner_radius=0.5, width=8.0, height=2.2, stroke_color=th.MINT, stroke_width=3, fill_color="#173A1E", fill_opacity=0.6).move_to([1.6, -0.4, 0])
        gl = T("insect midgut: pH about 10", size=22, color=th.MINT).next_to(gut, UP, buff=0.15)
        cells = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.85, height=0.6, stroke_color="#B6F5C4", stroke_width=2, fill_color="#2E5E3A", fill_opacity=1).move_to([-2.0 + 0.95 * k, -1.85, 0]) for k in range(8)])
        cap = B.Captions(self, at=(0, -2.85, 0), width=12, size=24)
        with self.say("The best known resistance gene comes from a soil bacterium, Bacillus thuringiensis. It makes its toxin as an inactive crystal, a protoxin, so it harms neither itself nor us."):
            self.play(FadeIn(head), FadeIn(crys), FadeIn(cl))
        with self.say("A caterpillar eats it. Its midgut is strongly alkaline, and that dissolves the crystal. Gut enzymes then cut the protoxin into the active toxin."):
            self.play(FadeIn(gut), FadeIn(gl), FadeIn(cells))
            self.play(crys.animate.move_to([-1.5, -0.3, 0]), FadeOut(cl), run_time=1.0)
            bits = VGroup(*[Dot([-1.5, -0.3, 0], radius=0.09, color=th.AMBER) for _ in range(8)])
            self.play(FadeOut(crys), FadeIn(bits))
            self.play(*[b_.animate.move_to(cells[k].get_top() + UP * 0.12) for k, b_ in enumerate(bits)], run_time=1.2)
            cap("Alkaline gut dissolves the crystal → proteases cut it → active toxin", color=th.AMBER)
        holes = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=th.BG, fill_opacity=1).move_to(c_.get_top() + DOWN * 0.12) for c_ in cells])
        with self.say("The toxin binds to receptors on the gut lining and punches pores in the cells. They swell and burst. The larva stops feeding and dies."):
            self.play(FadeIn(holes))
            self.play(*[c_.animate.scale(1.25).set_fill(th.CORAL, opacity=0.4) for c_ in cells], run_time=1.0)
            self.play(*[FadeOut(c_, scale=1.4) for c_ in cells], FadeOut(holes), FadeOut(bits))
            cap("Binds receptors → pores → gut cells burst → larva stops feeding and dies", color=th.CORAL)
        safe = para("Our stomach is acidic and has no such receptors: the crystal passes through us unchanged.", width=11, size=26, color=th.MINT).move_to([0, 1.8, 0])
        with self.say("Our stomachs are acidic, not alkaline, and our gut has no such receptors. So the toxin passes through us unchanged. That is why it is so specific."):
            self.play(FadeIn(safe))
        self.play(FadeOut(VGroup(head, gut, gl, safe)))
        cap.clear()
        rows = [["transgene", "source", "protects against", "crop"], ["cry1Ac, cry2Ab", "B. thuringiensis", "bollworm", "Bt cotton (India 2002)"], ["cry1Ab", "B. thuringiensis", "stem borer", "Bt maize"],
                ["cry1Ac", "B. thuringiensis", "fruit-and-shoot borer", "Bt brinjal (Bangladesh 2013)"], ["coat protein gene", "papaya ringspot virus", "the virus itself", "papaya"],
                ["RNAi construct", "the nematode's own gene", "root-knot nematode", "tobacco"]]
        tb = B.table(rows, [2.8, 3.3, 3.2, 3.8], row_h=0.62, size=22, colors=[th.AMBER, th.BODY, th.INK, th.MINT]).move_to([0, 0.2, 0])
        with self.say("Bt cotton was approved in India in two thousand and two and now covers about ninety percent of the cotton area there. Bt brinjal was approved in Bangladesh in two thousand and thirteen, the first genetically engineered food crop in South Asia. Other crops carry a virus coat protein gene against that virus, or an R N A interference construct that silences a nematode's own gene.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 4: manures and bio-inputs
    def p4(self):
        self.section(3)
        field = Line([-5, -2.0, 0], [5, -2.0, 0], color="#8A6A48", stroke_width=6)
        crop = VGroup(*[VGroup(Line([x, -2.0, 0], [x, -0.6, 0], color=PLANT, stroke_width=4), *[Ellipse(width=0.5, height=0.18, stroke_width=0, fill_color=PLANT, fill_opacity=1).rotate(s * 0.4).move_to([x + s * 0.22, y, 0]) for s, y in [(1, -1.0), (-1, -0.75)]]) for x in np.linspace(-4.5, 4.5, 12)])
        l1 = T("dhaincha (Sesbania), sunn hemp (Crotalaria), cowpea, guar", size=24, color=PLANT).move_to([0, 1.6, 0])
        nn = T("+ 60–90 kg nitrogen per hectare", size=28, color=th.AMBER, weight="BOLD").move_to([0, 0.8, 0])
        with self.say("Green manure is a quick growing crop, usually a legume like dhaincha or sunn hemp, grown in the field and then ploughed back into the same soil while still green. A good dhaincha crop adds sixty to ninety kilograms of nitrogen per hectare, plus organic matter that improves the soil's structure and water holding."):
            self.play(Create(field), LaggedStart(*[GrowFromEdge(c_, DOWN) for c_ in crop], lag_ratio=0.05), FadeIn(l1))
            self.play(*[c_.animate.rotate(-PI / 2, about_point=c_[0].get_start()).set_opacity(0.5) for c_ in crop], run_time=1.2)
            self.play(FadeIn(nn, scale=1.2))
        gl = para("Green-leaf manure: leaves of neem, Gliricidia or Artocarpus cut and carried to the field.", width=11, size=24, color=th.MUTED).move_to([0, -2.8, 0])
        with self.say("When tree leaves are cut and carried to the field instead, it is green leaf manure: neem, Gliricidia and Artocarpus are used this way in Nepal."):
            self.play(FadeIn(gl))
        self.play(FadeOut(VGroup(field, crop, l1, nn, gl)))
        rows = [["group", "organism", "what it does"], ["symbiotic N-fixer", "Rhizobium (legume nodules)", "fixes N₂"], ["symbiotic N-fixer", "Frankia in utis (Alnus nepalensis)", "N₂ in a non-legume tree"],
                ["symbiotic N-fixer", "Anabaena azollae in Azolla", "the paddy-field classic"], ["free-living", "Azotobacter, Clostridium", "fix N₂ in soil"], ["associative", "Azospirillum", "around cereal roots"],
                ["blue-green algae", "Nostoc, Anabaena, Aulosira", "N₂ in flooded rice"], ["phosphate solubilisers", "Bacillus megaterium, Pseudomonas", "free bound phosphate"], ["mycorrhiza", "Glomus (VAM)", "extends roots: P and water"]]
        tb = B.table(rows, [3.2, 5.2, 4.0], row_h=0.56, size=22, colors=[th.MUTED, th.AMBER, th.INK]).move_to([0, 0.15, 0])
        with self.say("A bio fertilizer is different. It is a culture of living microbes that make nutrients available to the plant. Rhizobium in legume nodules, and Frankia in the roots of our own utis tree, fix nitrogen from the air. Azolla, a tiny water fern carrying the cyanobacterium Anabaena, is the classic bio fertilizer of rice fields. Azotobacter fixes nitrogen free in the soil. Some bacteria dissolve locked up phosphate. And mycorrhizal fungi extend the root system for phosphorus and water.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        root = Line([-1.0, 1.5, 0], [-1.0, -2.0, 0], color="#E9D8A6", stroke_width=12)
        rng = np.random.default_rng(9)
        hy = VGroup(*[VMobject(stroke_color=th.PINK, stroke_width=2).set_points_smoothly([[-1.0, y, 0], [-1.0 + s * 1.0, y + rng.uniform(-0.4, 0.4), 0], [-1.0 + s * 2.4, y + rng.uniform(-0.8, 0.8), 0], [-1.0 + s * 3.6, y + rng.uniform(-1.0, 1.0), 0]])
                      for y in np.linspace(1.2, -1.7, 7) for s in (-1, 1)])
        pd = VGroup(*[Dot([x, y, 0], radius=0.06, color=th.AMBER) for x, y in zip(rng.uniform(-5, 3, 30), rng.uniform(-2.5, 2.2, 30))])
        ml = T("mycorrhizal hyphae reach phosphate the root never could", size=24, color=th.PINK).move_to([0, -2.8, 0])
        with self.say("Here is mycorrhiza at work. Fungal threads spread from the root far into the soil, reaching phosphate the root alone could never touch."):
            self.play(Create(root), FadeIn(pd))
            self.play(LaggedStart(*[Create(h_) for h_ in hy], lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(ml))
        self.play(FadeOut(VGroup(root, hy, pd, ml)))
        self.tip("A bio-fertilizer is a LIVING ORGANISM (Rhizobium, Azolla, Glomus) that makes nutrients available — not manure or compost, which supply nutrients themselves.",
                 "Exam tip. If a question asks for a bio fertilizer, the answer must be an organism: Rhizobium, Azolla, Glomus. Manure and compost supply nutrients themselves; a bio fertilizer supplies living microbes that unlock them.", width=8.6)
        rows = [["type", "agent", "target"], ["bacterial", "Bacillus thuringiensis", "caterpillars"], ["fungal", "Trichoderma", "soil-borne fungal disease"], ["fungal", "Beauveria, Metarhizium", "many insects"],
                ["viral", "nuclear polyhedrosis virus", "Helicoverpa, Spodoptera"], ["botanical", "neem (azadirachtin), pyrethrum", "broad-spectrum"], ["predator", "Trichogramma wasp, ladybird", "borer eggs, aphids"]]
        tb = B.table(rows, [2.4, 5.0, 4.4], row_h=0.6, size=22, colors=[th.MUTED, th.MINT, th.INK]).move_to([0, 0.5, 0])
        pc = para("For: specific, spare bees and birds, biodegradable, no residue. Against: slow, sensitive to sunlight, short shelf life.", width=11.5, size=23, color=th.BODY).move_to([0, -2.6, 0])
        with self.say("Bio pesticides are living things, or substances from them, used against pests. Bt against caterpillars. The fungus Trichoderma against soil borne diseases. A virus against Helicoverpa. Neem. And tiny Trichogramma wasps that parasitise the eggs of borers. They are specific, spare bees and birds, and leave no residue, though they act slowly and do not keep long.") as v:
            B.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(pc))
        self.play(FadeOut(VGroup(tb, pc)))

    # ------------------------------------------------------------------ part 5: genetic engineering
    def p5(self):
        self.section(4)
        d = self.callout("key", "Genetic engineering: isolating a gene, joining it to a carrier DNA in vitro, and putting it into a living cell, so the cell gains a trait breeding could never give. The joined DNA is recombinant DNA (rDNA).", width=11, size=27)
        with self.say("Genetic engineering means taking a gene out of one organism, joining it in a test tube to a carrier DNA, and putting it into a living cell, which then gains a trait that no amount of breeding could give it. Because the joined DNA combines two sources, it is called recombinant DNA."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        self.p5_ecori()
        self.p5_plasmid()
        self.p5_pcr()
        self.p5_gel()
        self.p5_gmo()

    def p5_ecori(self):
        head = T("Molecular scissors: EcoRI", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        top = "CTGAATTCAG"
        bot = "".join({"A": "T", "T": "A", "G": "C", "C": "G"}[b] for b in top)
        w = 0.52
        r1 = G.seq_row(top, w=w, gap=0.04).move_to([0, 0.9, 0])
        r2 = G.seq_row(bot, w=w, gap=0.04).move_to([0, 0.3, 0])
        l5 = VGroup(T("5′", size=22, color=th.MUTED).next_to(r1, LEFT, buff=0.2), T("3′", size=22, color=th.MUTED).next_to(r1, RIGHT, buff=0.2),
                    T("3′", size=22, color=th.MUTED).next_to(r2, LEFT, buff=0.2), T("5′", size=22, color=th.MUTED).next_to(r2, RIGHT, buff=0.2))
        site = SurroundingRectangle(VGroup(r1[2:8], r2[2:8]), color=th.AMBER, buff=0.08)
        sl = T("GAATTC reads the same 5′→3′ on both strands: a palindrome", size=24, color=th.AMBER).move_to([0, -0.6, 0])
        with self.say("The first tool is a restriction enzyme, the molecular scissors. Bacteria make them to chop up invading viruses. Each one recognises a short palindrome: a sequence that reads the same five prime to three prime on both strands. E co R one looks for G A A T T C."):
            self.play(FadeIn(head), FadeIn(r1), FadeIn(r2), FadeIn(l5))
            self.play(Create(site), FadeIn(sl))
        cut1 = Line(r1[2].get_right() + UP * 0.32 + RIGHT * 0.02, r1[2].get_right() + DOWN * 0.32 + RIGHT * 0.02, color=th.CORAL, stroke_width=6)
        cut2 = Line(r2[7].get_left() + UP * 0.32 + LEFT * 0.02, r2[7].get_left() + DOWN * 0.32 + LEFT * 0.02, color=th.CORAL, stroke_width=6)
        with self.say("It cuts between G and A on each strand. Because the two cuts are offset, the pieces come apart with four unpaired bases hanging off each end: A A T T. These are sticky ends."):
            self.play(Create(cut1), Create(cut2))
            self.sfx("click", gain=-10)
            left = VGroup(r1[:3], r2[:7])
            right = VGroup(r1[3:], r2[7:])
            self.play(FadeOut(VGroup(cut1, cut2, site, l5)), left.animate.shift(LEFT * 1.4), right.animate.shift(RIGHT * 1.4), run_time=1.2)
            sticky = VGroup(SurroundingRectangle(r1[3:7], color=th.MINT, buff=0.05), SurroundingRectangle(r2[3:7], color=th.MINT, buff=0.05))
            self.play(Create(sticky), Transform(sl, T("sticky (cohesive) ends: single-stranded AATT tails", size=24, color=th.MINT).move_to(sl)))
        with self.say("Any two pieces cut with the same enzyme have matching sticky ends, so they can pair up. Then the second tool, DNA ligase, the molecular glue, seals the backbone. Some enzymes, like Sma one, cut straight across and leave blunt ends. Arber, Nathans and Smith won the nineteen seventy eight Nobel Prize for discovering them."):
            self.play(left.animate.shift(RIGHT * 1.4), right.animate.shift(LEFT * 1.4), FadeOut(sticky), run_time=1.2)
            self.play(Flash(r1[3], color=th.MINT), Flash(r2[6], color=th.MINT))
        self.play(FadeOut(VGroup(head, r1, r2, sl)))

    def p5_plasmid(self):
        head = T("Vectors: a plasmid carries the gene", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-2.8, -0.4, 0])
        ring = Circle(radius=1.7, stroke_color=th.SKY, stroke_width=10).move_to(C)
        amp = Arc(radius=1.7, start_angle=PI * 0.65, angle=PI * 0.5, stroke_color=th.AMBER, stroke_width=14).move_arc_center_to(C)
        tet = Arc(radius=1.7, start_angle=-PI * 0.15, angle=PI * 0.5, stroke_color=th.MINT, stroke_width=14).move_arc_center_to(C)
        ori = Dot(C + polar_(1.7, -PI * 0.55), radius=0.16, color=th.PINK)
        labs = VGroup(M(r"amp^R", size=36, color=th.AMBER).move_to(C + polar_(2.3, PI * 0.9)), M(r"tet^R", size=36, color=th.MINT).move_to(C + polar_(2.3, PI * 0.1)),
                      T("ori", size=26, color=th.PINK, weight="BOLD").move_to(C + polar_(2.2, -PI * 0.55)))
        cap = B.Captions(self, at=(3.4, 0.0, 0), width=5.8, size=25)
        with self.say("The third tool is a vector, a carrier that will multiply inside the host. The classic one is the plasmid p B R three two two: a small ring of bacterial DNA. It has an origin of replication, so it copies itself, and two antibiotic resistance genes, for ampicillin and tetracycline, that act as markers."):
            self.play(FadeIn(head), Create(ring), Create(amp), Create(tet), FadeIn(ori), FadeIn(labs))
            cap("pBR322", color=th.SKY, sub="ori to replicate · amp-R and tet-R marker genes · unique restriction sites.")
        gene = Arc(radius=1.7, start_angle=PI * 0.02, angle=PI * 0.22, stroke_color=th.CORAL, stroke_width=20).move_arc_center_to(C)
        gl = T("your gene", size=24, color=th.CORAL, weight="BOLD").move_to(C + polar_(2.45, PI * 0.13))
        with self.say("Cut the plasmid and your gene with the same enzyme, mix, and ligate. If the cut site lies inside the tetracycline gene, your gene lands right in the middle of it, and breaks it."):
            self.play(Create(gene), FadeOut(labs[1]), FadeIn(gl))
            cap("Insert into tet-R: insertional inactivation", color=th.CORAL, sub="The recombinant plasmid still has amp-R, but tet-R no longer works.")
        p1 = VGroup(Circle(radius=1.0, stroke_color=th.BODY, stroke_width=3, fill_color="#2A2A1A", fill_opacity=1), T("ampicillin", size=20, color=th.AMBER)).move_to([2.2, -1.6, 0])
        p2 = VGroup(Circle(radius=1.0, stroke_color=th.BODY, stroke_width=3, fill_color="#1A2A22", fill_opacity=1), T("tetracycline", size=20, color=th.MINT)).move_to([4.8, -1.6, 0])
        p1[1].next_to(p1[0], DOWN, buff=0.1)
        p2[1].next_to(p2[0], DOWN, buff=0.1)
        cols1 = VGroup(*[Dot(p1[0].get_center() + polar_(r, a), radius=0.09, color=WHITE) for r, a in [(0.4, 0.3), (0.5, 2.0), (0.3, 4.0), (0.6, 5.0), (0.0, 0)]])
        cols2 = VGroup(*[Dot(p2[0].get_center() + polar_(r, a), radius=0.09, color=WHITE) for r, a in [(0.4, 0.3), (0.3, 4.0)]])
        miss = VGroup(*[Circle(radius=0.11, stroke_color=th.CORAL, stroke_width=2).move_to(p2[0].get_center() + polar_(r, a)) for r, a in [(0.5, 2.0), (0.6, 5.0), (0.0, 0)]])
        with self.say("Now push the plasmids into bacteria and pick out the right ones. Only colonies with a plasmid survive on ampicillin. Copy them onto tetracycline: those with a broken tetracycline gene die. Those are the ones carrying your gene. Modern vectors use the lac Z gene instead: recombinant colonies stay white on X gal, the others turn blue."):
            cap.clear()
            self.play(FadeIn(p1), FadeIn(cols1))
            self.play(FadeIn(p2), FadeIn(cols2), Create(miss))
            cap2 = para("Grow on ampicillin, die on tetracycline = recombinant. Or blue–white screening with lacZ.", width=5.4, size=22, color=th.CORAL).move_to([3.5, 0.9, 0])
            self.play(FadeIn(cap2))
        self.play(FadeOut(VGroup(head, ring, amp, tet, ori, labs[0], labs[2], gene, gl, p1, p2, cols1, cols2, miss, cap2)))
        rows = [["method", "how", "used for"], ["CaCl₂ + heat shock", "Ca²⁺ makes the wall porous; 42 °C pulse", "E. coli"], ["electroporation", "a high-voltage pulse opens pores", "bacteria, protoplasts"],
                ["microinjection", "a fine glass needle into the nucleus", "animal cells, eggs"], ["gene gun", "DNA-coated gold fired into cells", "monocots, chloroplasts"], ["Agrobacterium", "Ti plasmid T-DNA enters the plant genome", "dicots"]]
        tb = B.table(rows, [3.0, 5.8, 3.6], row_h=0.62, size=22, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 0.5, 0])
        steps = T("isolate DNA → cut → ligate → transform → select → multiply", size=26, color=th.MINT, weight="BOLD").move_to([0, -2.6, 0])
        with self.say("How do you get DNA into a cell? Calcium chloride and a heat shock for bacteria. An electric pulse. A glass needle. A gene gun firing DNA coated gold particles, used for cereals. And for broad leaved plants, nature's own genetic engineer: Agrobacterium tumefaciens, whose Ti plasmid normally slips its own DNA into plant cells. So the six steps are: isolate the DNA, cut, ligate, transform, select, and multiply.") as v:
            B.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(steps))
        self.play(FadeOut(VGroup(tb, steps)))

    def p5_pcr(self):
        head = T("PCR: a photocopier for DNA", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 3, 1], y_range=[40, 100, 20], x_length=6.0, y_length=2.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-2.6, 0.3, 0])
        temps = [(0, 0.33, 95, "denature 94–95 °C", th.CORAL), (0.33, 0.66, 55, "anneal 50–65 °C", th.SKY), (0.66, 1.0, 72, "extend 72 °C", th.MINT)]
        prof = VGroup()
        for k in range(3):
            for a, b, t_, n_, c_ in temps:
                prof.add(Line(ax.c2p(k + a, t_), ax.c2p(k + b, t_), color=c_, stroke_width=5))
        tl = VGroup(*[T(n_, size=20, color=c_).move_to(ax.c2p((a + b) / 2, t_ + 9)) for a, b, t_, n_, c_ in temps])
        yl = T("°C", size=20, color=th.MUTED).next_to(ax, LEFT, buff=0.1).shift(UP * 1.0)
        cyc = VGroup(T("cycles", size=22, color=th.MUTED), Integer(0, font_size=50, color=th.INK)).arrange(DOWN, buff=0.08).move_to([3.0, 2.0, 0])
        cop = VGroup(T("copies", size=22, color=th.MUTED), Integer(1, font_size=50, color=th.AMBER)).arrange(DOWN, buff=0.08).move_to([5.1, 2.0, 0])
        with self.say("The polymerase chain reaction, invented by Kary Mullis in nineteen eighty three, copies one chosen stretch of DNA millions of times, in a tube, with no cell at all. The tube holds the DNA, two short primers that flank the target, the four nucleotides, and a heat proof polymerase, Taq, from a hot spring bacterium."):
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            self.play(Create(prof[:3]), FadeIn(tl), run_time=1.6)
        with self.say("Each cycle has three steps. Heat to ninety five degrees: the strands separate. Cool to about fifty five: the primers stick. Warm to seventy two: Taq builds new strands from the primers. And every cycle doubles the number of copies.") as v:
            self.play(FadeIn(cyc), FadeIn(cop))
            for k in range(1, 4):
                self.play(cyc[1].animate.set_value(k), cop[1].animate.set_value(2 ** k), *([Create(prof[3 * (k - 1):3 * k])] if k > 1 else []), run_time=max(0.6, v.dur * 0.2))
        with self.say("Keep going. Ten cycles, a thousand copies. Twenty, a million. Thirty, over a billion, in about two hours.") as v:
            for k in [10, 20, 30]:
                self.play(cyc[1].animate.set_value(k), cop[1].animate.set_value(2 ** k), run_time=max(0.6, v.dur * 0.25))
            self.sfx("impact", gain=-12)
        self.play(FadeOut(VGroup(ax, prof, tl, yl, cyc, cop)))
        head2, prob = B.example_head(self, "A PCR starts with 5 copies of a target and runs 30 cycles at 100% efficiency. How many copies at the end? Roughly how many after 35 cycles?", size=25)
        steps = VGroup(M(r"N = N_0 \times 2^n", size=40), M(r"N_{30} = 5 \times 2^{30} = 5 \times 1.07\times10^{9} \approx 5.37\times10^{9}", size=38),
                       M(r"N_{35} = 5 \times 2^{35} \approx 1.72\times10^{11}\ \ (\times 2^5 = 32)", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["A worked example.", "Copies after n cycles are the starting number times two to the n.", "Thirty cycles: five times two to the thirty, about five point three seven times ten to the nine.",
                "Five more cycles multiply by two to the five, thirty two: about one point seven times ten to the eleven. In practice the enzyme and nucleotides run out and the curve flattens after thirty to thirty five cycles."]
        with self.say(says[0]):
            self.play(FadeOut(head), FadeIn(head2), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head2, prob, steps)))

    def p5_gel(self):
        head = T("Gel electrophoresis", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        gel = RoundedRectangle(corner_radius=0.15, width=5.4, height=4.8, stroke_color=th.MUTED, stroke_width=2, fill_color="#1A2238", fill_opacity=1).move_to([-2.6, -0.5, 0])
        wells = VGroup(*[Rectangle(width=0.7, height=0.15, stroke_width=0, fill_color=th.BG, fill_opacity=1).move_to([-4.3 + 1.7 * k, 1.6, 0]) for k in range(3)])
        neg = T("− cathode", size=22, color=th.SKY).move_to([-2.6, 2.25, 0])
        pos = T("+ anode", size=22, color=th.CORAL).move_to([-2.6, -3.15, 0])
        ladder = [(10, 1.2), (5, 0.4), (4, 0.15), (2, -0.6), (1, -1.6)]
        lane1 = [5, 4, 2, 1]
        lane2 = [6, 4, 2]
        y_of = lambda kb: -2.3 + 0.95 * np.log2(kb * 1.0)

        def bands(x, sizes, col):
            return VGroup(*[Rectangle(width=0.7, height=0.1, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to([x, 1.6, 0]) for _ in sizes])

        b0, b1, b2 = bands(-4.3, [l[0] for l in ladder], "#FFB547"), bands(-2.6, lane1, "#FF9F43"), bands(-0.9, lane2, "#FF9F43")
        ll = VGroup(*[T(f"{k} kb", size=18, color=th.MUTED).move_to([-5.7, y_of(k), 0]) for k, _ in ladder])
        cap = B.Captions(self, at=(3.6, 0.2, 0), width=5.4, size=24)
        with self.say("To check the right piece has been cut or copied, run it on an agarose gel. Load the samples in wells at the negative end. DNA's phosphate groups make it negative at any pH, so every fragment moves towards the positive anode. The gel is a sieve: short fragments slip through quickly and go far, long ones lag behind.") as v:
            self.play(FadeIn(head), FadeIn(gel), FadeIn(wells), FadeIn(neg), FadeIn(pos))
            self.add(b0, b1, b2)
            self.play(*[b_.animate.move_to([-4.3, y_of(k), 0]) for b_, (k, _) in zip(b0, ladder)],
                      *[b_.animate.move_to([-2.6, y_of(k), 0]) for b_, k in zip(b1, lane1)],
                      *[b_.animate.move_to([-0.9, y_of(k), 0]) for b_, k in zip(b2, lane2)], run_time=max(2.5, v.dur * 0.6), rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(ll))
            cap("Short fragments run furthest", sub="Stained with ethidium bromide, seen orange under UV. A ladder of known sizes gives each band's size.")
        lin = VGroup(T("linear, 3 sites → 4 pieces", size=22, color=th.INK), T("lane 2: 5 + 4 + 2 + 1 = 12 kb", size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cir = VGroup(T("circular, 3 sites → 3 pieces", size=22, color=th.INK), T("lane 3: 6 + 4 + 2 = 12 kb", size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        both = VGroup(lin, cir).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, -1.9, 0])
        with self.say("A favourite question. A linear molecule cut at three sites gives four pieces; a circular plasmid cut at three sites gives only three, because a ring has no ends. Either way, the fragment sizes must add back up to the whole molecule, twelve kilobases here. And two fragments of the same size run together as one brighter band."):
            self.play(FadeIn(lin))
            self.play(FadeIn(cir))
        self.play(FadeOut(VGroup(head, gel, wells, neg, pos, b0, b1, b2, ll, both)))
        cap.clear()

    def p5_gmo(self):
        rows = [["GMO", "gene", "result"], ["E. coli → humulin (1982)", "human insulin A and B chains", "cheap human insulin"], ["Bt cotton", "cry1Ac", "resists bollworm"], ["Golden Rice", "psy + crtI", "β-carotene (vitamin A precursor) in the grain"],
                ["Flavr Savr tomato (1994)", "antisense polygalacturonase", "softens slowly, keeps longer"], ["Roundup Ready soybean", "bacterial EPSPS", "tolerates glyphosate"]]
        tb = B.table(rows, [4.2, 4.4, 4.6], row_h=0.62, size=22, colors=[th.AMBER, th.BODY, th.INK]).move_to([0, 0.8, 0])
        with self.say("An organism changed this way is a G M O; if it carries a gene from another species, it is transgenic. Bacteria making human insulin since nineteen eighty two. Bt cotton. Golden Rice, whose grain makes beta carotene, the raw material of vitamin A. A slow softening tomato. A soybean that survives a weed killer.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        pc = VGroup(para("Benefits: more yield with less pesticide; drought and salt tolerance; biofortified food; cheap medicines.", width=5.6, size=22, color=th.MINT),
                    para("Concerns: allergens; marker genes; gene flow to wild relatives ('superweeds'); harm to non-target insects; seed dependence; patents.", width=5.6, size=22, color=th.CORAL)).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, -2.3, 0])
        with self.say("The benefits are real: higher yields with less spraying, stress tolerance, healthier food, cheap medicines. So are the concerns: possible allergens, gene flow to wild relatives, harm to insects we did not target, and farmers depending on bought, patented seed. That is why countries regulate them under the Cartagena Protocol on Biosafety."):
            self.play(FadeIn(pc))
        self.play(FadeOut(VGroup(tb, pc)))
        nep = self.callout("remember", "Nepal: ratified the Cartagena Protocol (2001); National Biosafety Framework (2006). A Supreme Court interim order (2014) stopped GM seed imports. No GM crop is registered for cultivation in Nepal; border samples are tested by PCR.", width=11, size=25)
        with self.say("And in Nepal? We ratified the Cartagena Protocol in two thousand and one and adopted a biosafety framework in two thousand and six. In two thousand and fourteen the Supreme Court stopped the import of G M seed. No G M crop is registered for growing in Nepal, and border samples are checked by P C R."):
            self.play(FadeIn(nep, shift=UP * 0.2))
        self.play(FadeOut(nep))
        self.tip("Transgenic ≠ hybrid. A hybrid comes from ordinary crossing; a transgenic plant carries a gene inserted in the lab, often from another kingdom. A maize hybrid is NOT a GMO.",
                 "Exam tip. A hybrid is made by ordinary crossing between related plants. A transgenic plant carries a gene put in by a laboratory, often from a bacterium or an animal. A hybrid maize is not a G M O. Do not call every improved variety a G M O.", width=8.6)
        self.quiz("A circular plasmid has three EcoRI sites. After complete digestion it gives",
                  ["2 fragments", "3 fragments", "4 fragments", "6 fragments"], 1,
                  "Pause and think. A ring, cut in three places. How many pieces?",
                  "Three. A ring has no free ends, so n cuts give n pieces. Four is the trap: that is a linear molecule with three cuts, which gives n plus one.")

    # ------------------------------------------------------------------ part 6: bio-engineering
    def p6(self):
        self.section(5)
        head = T("The bioreactor", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        tank = RoundedRectangle(corner_radius=0.5, width=2.8, height=4.2, stroke_color=th.BODY, stroke_width=4, fill_color="#1A2238", fill_opacity=1).move_to([-3.0, -0.4, 0])
        brew = RoundedRectangle(corner_radius=0.4, width=2.6, height=3.0, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.25).move_to([-3.0, -0.95, 0])
        shaft = Line([-3.0, 2.0, 0], [-3.0, -1.8, 0], color=th.BODY, stroke_width=4)
        blades = VGroup(*[Line([-3.5, y, 0], [-2.5, y, 0], color=th.BODY, stroke_width=6) for y in (-0.6, -1.6)])
        motor = Rectangle(width=0.8, height=0.5, stroke_width=0, fill_color=th.MUTED, fill_opacity=1).move_to([-3.0, 2.1, 0])
        probes = VGroup(*[Line([x, 1.6, 0], [x, -0.2, 0], color=c_, stroke_width=4) for x, c_ in [(-3.9, th.CORAL), (-2.1, th.SKY)]])
        rng = np.random.default_rng(4)
        bub = VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=1.5).move_to([-3.0 + rng.uniform(-1.1, 1.1), -2.2 + rng.uniform(0, 2.6), 0]) for _ in range(18)])
        cap = B.Captions(self, at=(3.0, 0.2, 0), width=6.4, size=25)
        with self.say("Bio engineering scales living reactions up to industry. Its central machine is the bioreactor, or fermenter: a sterile stirred steel tank. Probes watch the temperature, the p H and the dissolved oxygen; air bubbles in; the stirrer keeps everything mixed; and microbes or cultured cells make the product."):
            self.play(FadeIn(head), FadeIn(tank), FadeIn(brew), FadeIn(shaft), FadeIn(blades), FadeIn(motor), FadeIn(probes))
            self.play(Rotate(blades, PI, axis=UP, about_point=[-3.0, -1.1, 0]), LaggedStart(*[b_.animate.shift(UP * 0.8) for b_ in bub], lag_ratio=0.05), FadeIn(bub), run_time=2.0)
            cap("Bioreactor (fermenter)", color=th.AMBER, sub="Sterile, stirred; temperature, pH, O₂ and feed controlled automatically.")
        self.play(FadeOut(VGroup(head, tank, brew, shaft, blades, motor, probes, bub)))
        cap.clear()
        rows = [["area", "example"], ["fermentation", "penicillin (Penicillium), citric acid (Aspergillus niger)"], ["enzyme technology", "immobilised glucose isomerase → high-fructose syrup"], ["biofuel", "ethanol from sugarcane; biodiesel from Jatropha"],
                ["biogas", "methanogens digest dung: ~450,000 plants in Nepal"], ["bioremediation", "Pseudomonas putida degrades oil"], ["phytoremediation", "Brassica juncea takes up lead"], ["biosensor", "the glucometer"],
                ["bioleaching", "Thiobacillus releases copper from ore"], ["single-cell protein", "Spirulina"]]
        tb = B.table(rows, [3.6, 8.6], row_h=0.54, size=22, colors=[th.AMBER, th.INK]).move_to([0, 0.15, 0])
        with self.say("Its uses run far and wide. Penicillin and citric acid from fermenters. Immobilised enzymes. Ethanol and biodiesel. Microbes that eat oil spills, plants that pull lead out of soil, the glucose meter, bacteria that leach copper from ore, and Spirulina as protein. And one Nepal knows well: biogas.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        dome = Arc(radius=1.8, start_angle=0, angle=PI, stroke_color=th.BODY, stroke_width=6).move_to([0, -0.6, 0])
        base = Line([-1.8, -1.5, 0], [1.8, -1.5, 0], color=th.BODY, stroke_width=6)
        slurry = Rectangle(width=3.5, height=0.8, stroke_width=0, fill_color="#6B4E2E", fill_opacity=0.9).move_to([0, -1.1, 0])
        inlet = Line([-2.8, 0.4, 0], [-1.5, -1.2, 0], color=th.BODY, stroke_width=5)
        gas = VGroup(*[Dot([x, y, 0], radius=0.06, color=th.MINT) for x, y in zip(np.linspace(-1.2, 1.2, 9), [-0.4, 0.1, -0.2, 0.3, 0.0, 0.2, -0.3, 0.1, -0.1])])
        pipe = Line([0, 0.3, 0], [0, 1.6, 0], color=th.MINT, stroke_width=6)
        fl = VGroup(*[Line([d * 0.12, 1.6, 0], [d * 0.12, 1.95, 0], color=th.AMBER, stroke_width=5) for d in (-1, 0, 1)])
        gl = T("about 60% methane: cooking and light", size=24, color=th.MINT).move_to([3.2, 1.6, 0])
        sl = T("spent slurry → back to the field as manure", size=24, color="#C9A27A").move_to([3.2, -2.2, 0])
        with self.say("Nepal's biogas programme began in nineteen ninety two. Cattle dung and water go into a fixed dome digester, where methanogenic bacteria, working without oxygen, make a gas that is about sixty percent methane, for cooking and light. The spent slurry goes back to the fields as manure. It saves firewood, cuts kitchen smoke, and spares the forests."):
            self.play(Create(dome), Create(base), FadeIn(slurry), Create(inlet))
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.3) for g_ in gas], lag_ratio=0.1), Create(pipe))
            self.play(FadeIn(fl), FadeIn(gl), FadeIn(sl))
        self.play(FadeOut(VGroup(dome, base, slurry, inlet, gas, pipe, fl, gl, sl)))

    # ------------------------------------------------------------------ part 7: food safety and security
    def p7(self):
        self.section(6)
        a = self.callout("key", "Food SAFETY is about quality: food free from anything that could harm the eater.", width=5.4, size=26)
        b = self.callout("remember", "Food SECURITY is about access: everyone, always, has enough safe, nutritious food (FAO, 1996).", width=5.4, size=26)
        VGroup(a, b).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to([0, 1.3, 0])
        pillars = VGroup(*[VGroup(Rectangle(width=1.4, height=1.6, stroke_width=0, fill_color=c_, fill_opacity=0.8), T(n_, size=22, color=th.INK, weight="BOLD")).arrange(DOWN, buff=0.15) for n_, c_ in
                           [("availability", th.SKY), ("access", th.AMBER), ("utilisation", th.MINT), ("stability", th.PINK)]]).arrange(RIGHT, buff=0.5).move_to([0, -1.7, 0])
        roof = Polygon([-4.4, -0.75, 0], [4.4, -0.75, 0], [0, -0.1, 0], stroke_width=0, fill_color=th.PANEL_EDGE, fill_opacity=1)
        with self.say("Two terms students mix up. Food safety is about quality: the food must not harm the person eating it. Food security is about access: all people, at all times, have enough safe and nutritious food for an active, healthy life. Security stands on four pillars: availability, access, utilisation, and stability."):
            self.play(FadeIn(a, shift=UP * 0.2))
            self.play(FadeIn(b, shift=UP * 0.2))
            self.play(LaggedStart(*[GrowFromEdge(p_, DOWN) for p_ in pillars], lag_ratio=0.2), FadeIn(roof))
        self.play(FadeOut(VGroup(a, b, pillars, roof)))
        rows = [["hazard", "examples"], ["biological", "Salmonella, E. coli O157:H7, cholera, hepatitis A, aflatoxin from Aspergillus flavus on damp maize"], ["chemical", "pesticide residue, heavy metals, excess colour, melamine, ripening chemicals"], ["physical", "glass, metal, stones, hair, insect parts"]]
        tb = B.table(rows, [2.6, 9.8], row_h=0.7, size=22, colors=[th.CORAL, th.INK]).move_to([0, 1.1, 0])
        how = para("Ensured by: good farm hygiene; dry storage below the mould moisture level; pasteurisation, canning, refrigeration; HACCP at every critical point; Codex labelling. In Nepal: the Food Act 2023 BS, the DFTQC, and the Right to Food and Food Sovereignty Act 2075 (Article 36 of the Constitution).", width=11.8, size=23, color=th.BODY).move_to([0, -1.7, 0])
        with self.say("Hazards come in three kinds. Biological: germs like Salmonella and cholera, and aflatoxin, a poison made by a mould on damp maize and groundnut. Chemical: pesticide residues, heavy metals, adulterants. Physical: glass, stones, hair. Safety is protected by hygiene, dry storage, pasteurisation and refrigeration, the HACCP system of watching every critical step, and the law: in Nepal, the Food Act, the Department of Food Technology and Quality Control, and the Right to Food Act of twenty seventy five.") as v:
            B.reveal_table(self, tb, v.dur * 0.5)
            self.play(FadeIn(how))
        self.play(FadeOut(VGroup(tb, how)))
        helps = VGroup(*[T(s_, size=25, color=th.INK) for s_ in ["higher-yielding, stress-tolerant varieties → availability", "biofortified crops (Golden Rice, iron beans, zinc wheat) → utilisation",
                                                                  "tissue culture → disease-free planting material", "bio-pesticides and bio-fertilizers → fewer chemical residues", "PCR and biosensors → fast detection of contamination"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        h2 = T("Where biotechnology helps", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("And this is where the whole unit comes together. Better varieties raise availability. Biofortified crops improve nutrition. Tissue culture gives clean planting material. Bio pesticides and bio fertilizers cut chemical residues. And PCR and biosensors catch contamination fast.") as v:
            self.play(FadeIn(h2))
            for h_ in helps:
                self.play(FadeIn(h_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.12)
        self.play(FadeOut(VGroup(h2, helps)))
        self.quiz("Aflatoxin in stored maize is an example of a",
                  ["physical hazard", "chemical hazard made by a machine", "biological hazard", "food security problem"], 2,
                  "Last check. Aflatoxin on damp, badly stored maize. What kind of hazard?",
                  "A biological hazard: it is made by a living mould, Aspergillus flavus, growing on damp grain. It is a safety problem, not a security one: the food is there, but it can harm the eater.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Tissue culture rests on totipotency; auxin : cytokinin decides roots, callus or shoots.",
            "Breeding: emasculate, bag, cross, select; heterosis; Green Revolution.",
            "Bt: an alkaline gut activates the crystal; gene-for-gene resistance.",
            "Bio-fertilizers are living organisms: Rhizobium, Azolla, Glomus.",
            "rDNA: EcoRI + ligase + plasmid; PCR doubles each cycle; gels sort by size.",
            "Food safety = quality; food security = access, on four pillars.",
        ], "Quick recap. Tissue culture works because plant cells are totipotent, and the auxin to cytokinin ratio decides roots, callus or shoots. Breeders emasculate, bag, cross and select, and hybrids show heterosis. The Bt toxin is activated only in an insect's alkaline gut. Bio fertilizers are living organisms. Recombinant DNA uses restriction enzymes, ligase and a plasmid; PCR doubles DNA every cycle; gels sort fragments by size. And food safety is about quality, food security about access.")
        self.outro("That was biotechnology, and the end of botany. Next we move to zoology, starting with the tissues of the animal body. See you there.")
