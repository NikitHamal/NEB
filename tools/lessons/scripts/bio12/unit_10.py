import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402

HONEY = "#FFB547"
WATER = "#4CC9F0"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 10
    TITLE = "Applied Biology"
    SUBTITLE = "Animals and microbes that earn a living"
    SECTIONS = ["Application of zoology", "Microbial diseases and applied microbiology"]
    NEXT = "Class 12 Mathematics · Unit 1"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.ending)

    def worked(self, problem, lines, says, size=36):
        head, prob = B.example_head(self, problem, size=25)
        steps = VGroup(*[M(l_, size=size) for l_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        for s_ in steps:
            if s_.width > 12.4:
                s_.scale_to_fit_width(12.4).align_to(prob, LEFT)
        steps[-1].set_color(th.AMBER)
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.3)
        self.play(FadeOut(VGroup(head, prob, steps)))

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        cliff = Polygon([-6.8, 3.4, 0], [-3.2, 3.4, 0], [-2.6, 1.0, 0], [-3.4, -1.0, 0], [-2.8, -3.4, 0], [-6.8, -3.4, 0], stroke_width=0, fill_color="#4A4038", fill_opacity=1)
        comb = Ellipse(width=1.6, height=1.0, stroke_width=0, fill_color=HONEY, fill_opacity=0.9).move_to([-2.5, 1.6, 0])
        ladder = VGroup(Line([-1.3, 3.4, 0], [-1.6, -2.8, 0], color="#C9A27A", stroke_width=4), Line([-0.9, 3.4, 0], [-1.2, -2.8, 0], color="#C9A27A", stroke_width=4),
                        *[Line([-1.3 - 0.3 * t, 3.4 - 6.2 * t, 0], [-0.9 - 0.3 * t, 3.4 - 6.2 * t, 0], color="#C9A27A", stroke_width=3) for t in np.linspace(0.05, 0.95, 12)])
        t1 = para("Gurung honey hunters harvest the combs of the world's largest honey bee, Apis laboriosa, from Himalayan cliffs.", width=6.0, size=26, color=th.INK).move_to([3.2, 1.2, 0])
        t2 = para("In spring, from rhododendron nectar, that honey turns into 'mad honey' — and sells for five times the price.", width=6.0, size=26, color=th.AMBER).move_to([3.2, -0.9, 0])
        with self.say("On a cliff face in Gandaki Province, Gurung honey hunters climb rope ladders to cut combs from the world's largest honey bee, Apis laboriosa. In spring, when the bees feed on laliguras, our national flower, the honey carries a nerve toxin. People call it mad honey, and it sells for five times the normal price."):
            self.play(FadeIn(cliff), FadeIn(comb), Create(ladder))
            self.play(FadeIn(t1))
            self.play(FadeIn(t2))
        nb = B.neby_in(self, "surprised", height=1.3)
        with self.say("Biology, it turns out, earns a living. Bees, silkworms, fish, chickens, buffaloes and worms on one side; microbes that make us ill, and microbes that make our curd and our medicines, on the other."):
            pass
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(cliff, comb, ladder, t1, t2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 10: Applied Biology, the last unit of the year."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Two parts. Applied zoology: beekeeping, silk, fish farming, poultry, livestock and vermicomposting, with Nepal's own numbers. Then microbiology: the agents of disease, how they spread, tuberculosis, vaccines and antibiotics, and microbes at work.")

    # ------------------------------------------------------------------ part 1: applied zoology
    def p1(self):
        self.section(0)
        self.p1_bees()
        self.p1_silk()
        self.p1_fish()
        self.p1_livestock()
        self.p1_vermi()

    def p1_bees(self):
        head = T("Apiculture: beekeeping", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        rows = [["species", "name", "nest", "hiveable?"], ["Apis cerana", "mauri, Asian hive bee", "parallel combs in a cavity", "YES: the Nepali hive bee"], ["Apis mellifera", "European bee", "combs in a cavity", "yes: introduced 1992"],
                ["Apis dorsata", "rock bee", "one huge open comb", "no"], ["Apis laboriosa", "Himalayan cliff bee", "open comb under cliffs", "no: largest honey bee"], ["Apis florea", "little bee", "small open comb", "no"]]
        tb = B.table(rows, [2.8, 3.4, 3.8, 3.6], row_h=0.6, size=21, colors=[HONEY, th.INK, th.BODY, th.MINT]).move_to([0, 0.5, 0])
        nt = T("Write Apis cerana — 'Apis indica' is an obsolete name.", size=22, color=th.CORAL).move_to([0, -2.6, 0])
        with self.say("Apiculture is keeping honey bees in hives. Five species matter in Nepal. Apis cerana, the mauri, nests in dark cavities, so it can be coaxed into a box; it makes up about three quarters of Nepal's hives and survives up to three and a half thousand metres. Apis mellifera, the European bee, came in nineteen ninety two. The rock bee, the cliff bee and the little bee build single open combs and cannot be hived.") as v:
            self.play(FadeIn(head))
            B.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        castes = VGroup(*[VGroup(T(n_, size=28, color=c_, weight="BOLD"), para(d_, width=3.6, size=20, color=th.BODY, align="center"), T(t_, size=22, color=th.AMBER)).arrange(DOWN, buff=0.15) for n_, d_, t_, c_ in
                          [("queen", "the only fertile female; up to ~2000 eggs a day; stores sperm in a spermatheca", "egg to adult 16 days", th.PINK), ("worker", "sterile female: cleans, nurses, builds comb, guards, then forages", "21 days", HONEY),
                           ("drone", "male from an UNFERTILISED egg: haploid; only job is mating", "24 days", th.SKY)]]).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 0.5, 0])
        rj = para("Royal jelly is fed to EVERY larva for about 3 days; only the queen larva stays on it. Diet, not genes, makes a queen.", width=11.5, size=23, color=th.MINT).move_to([0, -2.3, 0])
        with self.say("The colony is a caste society. One queen, the only fertile female, laying up to two thousand eggs a day. Thousands of sterile female workers, who clean, nurse, build, guard and finally forage. And a few hundred drones, males that hatch from unfertilised eggs, so they are haploid. What makes a queen? Diet. Every larva gets royal jelly for about three days, but only the future queen is kept on it.") as v:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in castes], lag_ratio=0.3))
            self.play(FadeIn(rj))
        self.play(FadeOut(VGroup(castes, rj)))
        box = Rectangle(width=5.2, height=3.0, stroke_color="#C9A27A", stroke_width=5).move_to([-2.6, -0.5, 0])
        frames = VGroup(*[Rectangle(width=0.3, height=2.6, stroke_color=HONEY, stroke_width=3, fill_color=HONEY, fill_opacity=0.35).move_to([-4.6 + 0.62 * i, -0.5, 0]) for i in range(7)])
        gap = DoubleArrow(frames[2].get_right() + DOWN * 1.0, frames[3].get_left() + DOWN * 1.0, buff=0, color=th.CORAL, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        gl = T("bee space 6.4–9.5 mm", size=22, color=th.CORAL).next_to(box, DOWN, buff=0.15)
        lt = para("Langstroth, 1851–52: leave exactly the bee space and the bees build no comb or propolis there, so every frame lifts out without killing the colony. In Nepal, A. cerana also lives in the smaller Newton hive.", width=5.4, size=22, color=th.INK).move_to([3.6, -0.3, 0])
        with self.say("Before eighteen fifty one, harvesting honey usually meant destroying the colony. Then Langstroth noticed that bees always leave a gap of about six to nine millimetres, the bee space, which they never fill. Build a box with frames spaced exactly that far apart, and every frame lifts out undamaged. Every modern hive is his movable frame hive."):
            self.play(Create(box), LaggedStart(*[FadeIn(f_) for f_ in frames], lag_ratio=0.1))
            self.play(GrowArrow(gap), FadeIn(gl))
            self.play(frames[3].animate.shift(UP * 1.8), run_time=1.0)
            self.play(FadeIn(lt))
        self.play(FadeOut(VGroup(head, box, frames, gap, gl, lt)))
        prod = para("Products: honey (nectar ripened below ~20% water), beeswax, propolis, royal jelly. But the biggest value is POLLINATION: 87 of the leading food crops depend on animal pollinators.", width=11.5, size=24, color=th.INK).move_to([0, 1.4, 0])
        en = para("Enemies: the mite Varroa destructor (A. mellifera); Thai sacbrood virus and European foulbrood (A. cerana); wax moths; hornets.", width=11.5, size=22, color=th.CORAL).move_to([0, -0.1, 0])
        with self.say("Hives give honey, wax, propolis and royal jelly. But their greatest value is pollination: eighty seven of the world's leading food crops depend on animal pollinators. In Jumla, Apis cerana makes more than half of all visits to apple flowers. Their enemies are the Varroa mite, sacbrood virus and foulbrood disease, wax moths and hornets."):
            self.play(FadeIn(prod))
            self.play(FadeIn(en))
        self.play(FadeOut(VGroup(prod, en)))
        self.worked("Nepal produced 4,278 tonnes of honey from 276,000 hives in 2081/82. What is the average yield per hive? Compare with 16.45 kg per hive in 2019.",
                    [r"\frac{4\,278\,000 \text{ kg}}{276\,000 \text{ hives}} = 15.5 \text{ kg per hive}", r"15.5 < 16.45: \text{ yields are falling (forage loss, pesticides, brood disease)}"],
                    ["A worked example on Nepal's honey.", "Four point two seven eight million kilograms over two hundred and seventy six thousand hives: fifteen and a half kilograms per hive.",
                     "Slightly below twenty nineteen. Studies blame lost forage, pesticides and brood disease."])

    def p1_silk(self):
        head = T("Sericulture: the mulberry silkworm", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        stages = [("egg", "hatch in 10–14 days"), ("larva", "5 instars, 4 moults; eats only mulberry, ~30 days"), ("spinning", "2–3 days, figure-of-eight; 1000–1600 m of filament"), ("pupa in cocoon", ""), ("moth", "flightless; lays 300–500 eggs, dies")]
        C = np.array([-2.4, -0.4, 0])
        nodes = VGroup()
        for i, (n_, d_) in enumerate(stages):
            a = PI / 2 - TAU * i / 5
            p = C + polar(2.0, a)
            nodes.add(VGroup(Circle(radius=0.55, stroke_color=th.MINT, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), para(n_, width=1.0, size=18, color=th.INK, align="center")).move_to(p))
        arr = VGroup(*[CurvedArrow(nodes[i].get_center() + (nodes[(i + 1) % 5].get_center() - nodes[i].get_center()) * 0.3, nodes[(i + 1) % 5].get_center() - (nodes[(i + 1) % 5].get_center() - nodes[i].get_center()) * 0.3, angle=-0.3, color=th.MUTED, stroke_width=3) for i in range(5)])
        cap = B.Captions(self, at=(3.8, 0.0, 0), width=5.0, size=24)
        with self.say("Sericulture is rearing silkworms for silk. The mulberry silkworm, Bombyx mori, has been domesticated so long that the moth cannot fly and does not exist in the wild. It is monophagous: it eats mulberry leaves and nothing else, so growing mulberry is half the job."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.2), LaggedStart(*[Create(a_) for a_ in arr], lag_ratio=0.2))
        says = ["Eggs hatch in ten to fourteen days.", "The larva eats for about a month, through five instars separated by four moults.", "Then it stops eating and spins its cocoon for two or three days, swinging its head in a figure of eight and paying out a thousand metres or more of silk from its salivary glands.",
                "Inside the cocoon it becomes a pupa.", "Left alone, the moth would emerge, mate, lay eggs and die without ever eating."]
        for i, sy in enumerate(says):
            with self.say(sy):
                self.play(Indicate(nodes[i], color=th.MINT, scale_factor=1.15))
                cap(stages[i][0].capitalize(), color=th.MINT, sub=stages[i][1] or None)
        self.play(FadeOut(VGroup(nodes, arr)))
        cap.clear()
        steps = VGroup(*[VGroup(T(str(i + 1), size=24, color=th.AMBER, weight="BOLD"), T(s_, size=24, color=th.INK)).arrange(RIGHT, buff=0.3) for i, s_ in enumerate(
            ["harvest cocoons 5–7 days after spinning", "stifle: kill the pupa with steam or hot air", "deflossing: strip loose outer floss", "cook in hot water to soften the sericin gum", "reel several filaments together (filature)", "throw, degum, dye, weave"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.8, -0.2, 0])
        comp = para("Raw silk: 75–80% fibroin (the fibre) + 20–25% sericin (gum). Reelable thread per cocoon: 600–900 m.", width=4.4, size=21, color=th.MINT).move_to([4.4, -0.2, 0])
        with self.say("From cocoon to cloth, in order. Harvest the cocoons. Stifle them, killing the pupa before the moth can break the thread. Strip off the loose floss. Cook them to soften the gum. Reel the filaments together in a filature. Then degum, dye and weave. Raw silk is mostly the protein fibroin, held together by the gum sericin.") as v:
            for s_ in steps:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.08)
            self.play(FadeIn(comp))
        self.play(FadeOut(VGroup(steps, comp)))
        rows = [["silk", "insect", "food plant", "note"], ["mulberry", "Bombyx mori", "mulberry", "~90% of world silk; reeled"], ["tasar", "Antheraea paphia", "Terminalia, sal", "coarse, coppery"],
                ["eri", "Samia ricini", "castor", "open cocoon: SPUN, 'ahimsa' silk"], ["muga", "Antheraea assamensis", "som, soalu", "golden; Assam"]]
        tb = B.table(rows, [2.0, 3.6, 3.0, 4.4], row_h=0.62, size=22, colors=[th.AMBER, th.INK, th.BODY, th.MINT]).move_to([0, 0.6, 0])
        np_ = para("Nepal: Sericulture Development Centre, Khopasi (Kavre); ~39 tonnes a year from bivoltine B. mori; 38 mid-hill districts suitable.", width=12, size=22, color=th.BODY).move_to([0, -2.4, 0])
        with self.say("Mulberry silk is one of four. The three wild silks come from other moths: tasar on sal and Terminalia, eri on castor, and muga, the golden silk of Assam. The eri moth walks out of an open cocoon, so eri silk is made without killing the pupa, and it must be spun, not reeled. Nepal's centre is at Khopasi in Kavre, producing about thirty nine tonnes a year.") as v:
            B.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(np_))
        self.play(FadeOut(VGroup(head, tb, np_)))
        self.worked("A reeling centre needs 5,000 cocoons per kg of raw silk. A Kavre farmer brings 30,000 cocoons. If a sari needs 0.5 kg of raw silk, how many saris?",
                    [r"\text{raw silk} = \frac{30\,000}{5000} = 6.0 \text{ kg}", r"\text{saris} = \frac{6.0}{0.5} = 12"],
                    ["A quick sum.", "Thirty thousand cocoons at five thousand per kilogram: six kilograms of raw silk.", "At half a kilogram per sari: twelve saris, from thirty thousand caterpillars."])

    def p1_fish(self):
        head = T("Composite fish culture: one pond, six niches", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        pond = Rectangle(width=7.0, height=4.4, stroke_width=0, fill_color=WATER, fill_opacity=0.15).move_to([-2.4, -0.6, 0])
        zones = [(1.15, "surface"), (-0.6, "column"), (-2.35, "bottom")]
        zl = VGroup(*[T(z_, size=20, color=th.MUTED).move_to([-6.3, y, 0]) for y, z_ in zones])
        fish = [("silver carp", "phytoplankton", 1.15, -4.2, th.MINT), ("catla", "zooplankton", 1.15, -1.0, th.SKY), ("rohu", "column omnivore", -0.6, -3.0, th.AMBER),
                ("grass carp", "weeds at the margins", -0.6, 0.4, "#7BC043"), ("mrigal", "bottom detritus", -2.35, -4.0, th.PINK), ("common carp", "bottom omnivore", -2.35, -1.0, th.CORAL)]
        fs = VGroup()
        for n_, f_, y, x, c_ in fish:
            body = VGroup(Ellipse(width=1.0, height=0.4, stroke_width=0, fill_color=c_, fill_opacity=0.9), Polygon([0.5, 0, 0], [0.8, 0.2, 0], [0.8, -0.2, 0], stroke_width=0, fill_color=c_, fill_opacity=0.9))
            lab = VGroup(T(n_, size=18, color=c_, weight="BOLD"), T(f_, size=15, color=th.BODY)).arrange(DOWN, buff=0.03)
            fs.add(VGroup(body, lab.next_to(body, DOWN, buff=0.05)).move_to([x, y, 0]))
        cap = B.Captions(self, at=(4.2, 0.0, 0), width=4.4, size=23)
        with self.say("Nepal now gets eighty four percent of its fish from farms, almost all of it from the Terai. The key idea is composite culture. A pond is not one habitat but several: the plankton rich surface, the middle water, the weedy edges and the muddy bottom. Stock one species and most of the food is wasted."):
            self.play(FadeIn(head), FadeIn(pond), FadeIn(zl))
            cap("Different feeding niches, no competition", color=WATER, sub="Six carps (all Cyprinidae) share one pond.")
        with self.say("So stock six carps that feed in different places. Silver carp at the surface eats phytoplankton; catla, also near the surface, eats zooplankton. Rohu feeds in the column. Grass carp eats the weeds at the margins. Mrigal and common carp work the bottom. The same pond feeds them all, and the yield jumps.") as v:
            for f_ in fs:
                self.play(FadeIn(f_, shift=RIGHT * 0.3), run_time=0.4)
                self.hold(v.dur * 0.1)
        self.play(FadeOut(VGroup(pond, zl, fs)))
        cap.clear()
        w = self.callout("careful", "Silver carp eats PHYTOplankton; bighead carp eats ZOOplankton. Rohu is a COLUMN feeder; catla eats zooplankton. A favourite MCQ trap.", width=11, size=25).move_to([0, 1.3, 0])
        ib = para("Induced breeding: carps mature in ponds but do not SPAWN without river cues. Hiralal Chaudhuri (Cuttack, 10 July 1956) injected pituitary extract; today Ovaprim (a GnRH analogue + domperidone) is used.", width=11.5, size=23, color=th.INK).move_to([0, -1.3, 0])
        with self.say("Two traps. Silver carp eats plant plankton; its cousin the bighead eats animal plankton. And carps kept in ponds mature perfectly well, but they will not spawn, because they need river cues like rising, flowing monsoon water. Since nineteen fifty six, fish farmers inject hormones to make them spawn; today the drug Ovaprim is used."):
            self.play(FadeIn(w, shift=UP * 0.2))
            self.play(FadeIn(ib))
        self.play(FadeOut(VGroup(head, w, ib)))
        self.worked("A 0.6 ha pond in Bara is stocked at 5,000 fingerlings per hectare in the ratio surface 30% : column 30% : bottom 40%. How many of each? Expected harvest at 5.62 t/ha?",
                    [r"5000 \times 0.6 = 3000 \text{ fingerlings}", r"\text{surface } 900,\ \ \text{column } 900,\ \ \text{bottom } 1200", r"5.62 \times 0.6 = 3.37 \text{ t} \approx 3370 \text{ kg}"],
                    ["A stocking example.", "Five thousand per hectare on point six hectares: three thousand fingerlings.", "Thirty, thirty and forty percent: nine hundred, nine hundred and twelve hundred.", "At the national average yield, about three point four tonnes of fish."])
        tr = para("Cold water: rainbow trout (below ~21 °C) in Rasuwa and Nuwakot, 1,332 t a year. Native sahar (golden mahseer, Tor putitora) is Endangered.", width=11.5, size=23, color=th.SKY)
        with self.say("In the cold hill rivers, rainbow trout is farmed in Rasuwa and Nuwakot. And our native sahar, the golden mahseer, is now endangered and is being bred in hatcheries to restore it."):
            self.play(FadeIn(tr))
        self.play(FadeOut(tr))

    def p1_livestock(self):
        rows = [["", "broiler", "layer"], ["purpose", "meat", "eggs"], ["strains", "Cobb, Ross, Hubbard", "Hy-Line, Lohmann, White Leghorn"], ["growth", "slaughter weight in 4–6 weeks", "slow; matures to lay"], ["feed", "high-energy", "high-calcium layer mash"]]
        tb = B.table(rows, [2.4, 4.6, 5.4], row_h=0.6, size=22, colors=[th.MUTED, th.CORAL, th.AMBER]).move_to([0, 1.2, 0])
        ind = para("Nepal's three indigenous breeds: Sakini, Ghanti Khuile (naked neck), Pwankh Ulte (frizzle) — hardy, dual-purpose.", width=11.5, size=23, color=th.MINT).move_to([0, -1.2, 0])
        head = T("Poultry farming", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Poultry, from the red junglefowl. Broilers are bred for meat and reach slaughter weight in four to six weeks; layers are bred for eggs, and a modern layer approaches five hundred eggs. Nepal has three indigenous breeds: Sakini, the naked necked Ghanti Khuile, and the frizzled Pwankh Ulte, hardy birds for village scavenging.") as v:
            self.play(FadeIn(head))
            B.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(ind))
        self.play(FadeOut(VGroup(tb, ind)))
        rows = [["disease", "agent", "type", "control"], ["Newcastle (= Ranikhet)", "avian paramyxovirus 1", "virus", "vaccines, biosecurity"], ["Marek's disease", "gallid herpesvirus 2", "virus", "vaccine at hatch"],
                ["fowl pox", "Avipoxvirus", "virus", "wing-web vaccine"], ["coccidiosis", "Eimeria (E. tenella in caeca)", "protozoan", "coccidiostats, dry litter"], ["bird flu", "influenza A H5N1, H9", "virus", "culling, movement control"]]
        tb = B.table(rows, [3.4, 4.0, 1.8, 3.6], row_h=0.6, size=21, colors=[th.AMBER, th.INK, th.MUTED, th.MINT]).move_to([0, 0.3, 0])
        with self.say("Poultry diseases are a favourite short question. Newcastle disease and Ranikhet disease are the same thing, caused by a virus that can kill a whole flock. Marek's disease causes tumours. Coccidiosis is protozoan, not viral, and damages the caeca. And bird flu, H5N1, first hit Nepal in Jhapa in two thousand and nine.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(VGroup(head, tb)))
        head = T("Livestock: Nepal runs on the buffalo", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        bars = VGroup()
        for i, (n_, v_, c_) in enumerate([("buffalo", 52.1, th.SKY), ("cow", 47.9, th.AMBER)]):
            r = Rectangle(width=v_ / 52.1 * 6.0, height=0.55, stroke_width=0, fill_color=c_, fill_opacity=0.9)
            r.move_to([-2.6 + r.width / 2, 1.4 - 0.8 * i, 0])
            bars.add(VGroup(r, T(n_, size=24, color=th.INK).next_to([-2.6, 1.4 - 0.8 * i, 0], LEFT, buff=0.2), T(f"{v_}% of milk", size=22, color=c_).next_to(r, RIGHT, buff=0.15)))
        facts = VGroup(*[para(s_, width=11.5, size=22, color=c_) for s_, c_ in [("Buffalo: riverine type; indigenous Lime, Parkote, Gaddi; Murrah crosses. Rich milk → ghiu, khuwa.", th.SKY),
                                                                              ("Cattle: Lulu (Manang, Mustang, humpless) and Achhami ('nine fists' tall); Siri for draught.", th.AMBER),
                                                                              ("Yak × hill cattle = chauri: females fertile, F₁ males STERILE; more milk than yak but less fat. Yak milk → chhurpi.", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.4, 0])
        with self.say("Nepal's milk comes mostly from the buffalo: fifty two percent. Our buffaloes are the riverine type, with local breeds like Lime and Parkote, and their rich milk makes ghiu and khuwa. Among cattle, the humpless Lulu of Mustang and the tiny Achhami, nine fists tall. And up high, the yak, crossed with hill cattle to give the chauri. Female chauri are fertile, but the first generation males are sterile, a classic exam fact.") as v:
            self.play(FadeIn(head), LaggedStart(*[GrowFromEdge(b_[0], LEFT) for b_ in bars], lag_ratio=0.3), FadeIn(VGroup(*[b_[1:] for b_ in bars])))
            for f_ in facts:
                self.play(FadeIn(f_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.18)
        self.play(FadeOut(VGroup(head, bars, facts)))

    def p1_vermi(self):
        head = T("Vermicomposting", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        soil = Rectangle(width=12, height=4.0, stroke_width=0, fill_color="#3A2E1F", fill_opacity=0.9).move_to([0, -0.9, 0])
        litter = Rectangle(width=12, height=0.5, stroke_width=0, fill_color="#5E8C2E", fill_opacity=0.8).move_to([0, 1.35, 0])
        epi = VMobject(stroke_color=th.PINK, stroke_width=8).set_points_smoothly([[-4.8, 1.3, 0], [-4.3, 1.45, 0], [-3.8, 1.25, 0]])
        ane = VMobject(stroke_color=th.PINK, stroke_width=8).set_points_smoothly([[0, 1.1, 0], [0.1, -0.5, 0], [-0.1, -2.6, 0]])
        endo = VMobject(stroke_color=th.PINK, stroke_width=8).set_points_smoothly([[3.2, -1.0, 0], [4.0, -0.8, 0], [4.8, -1.1, 0]])
        labs = VGroup(VGroup(T("epigeic", size=24, color=th.MINT, weight="BOLD"), T("surface litter: YES", size=18, color=th.MINT)).arrange(DOWN, buff=0.05).move_to([-4.3, 2.3, 0]),
                      VGroup(T("anecic", size=24, color=th.CORAL, weight="BOLD"), T("deep burrows: no", size=18, color=th.CORAL)).arrange(DOWN, buff=0.05).move_to([1.6, 0.0, 0]),
                      VGroup(T("endogeic", size=24, color=th.CORAL, weight="BOLD"), T("eats soil: no", size=18, color=th.CORAL)).arrange(DOWN, buff=0.05).move_to([4.0, -1.8, 0]))
        with self.say("Vermicomposting turns organic waste into rich manure using earthworms. But only one kind of earthworm will do. Epigeic worms live in the surface litter and eat and breed fast: perfect. Anecic worms dig deep vertical burrows, and endogeic worms eat soil; neither suits a shallow bin. The standard species is Eisenia fetida, the red wiggler."):
            self.play(FadeIn(head), FadeIn(soil), FadeIn(litter))
            self.play(Create(epi), FadeIn(labs[0]))
            self.play(Create(ane), FadeIn(labs[1]))
            self.play(Create(endo), FadeIn(labs[2]))
        self.play(FadeOut(VGroup(soil, litter, epi, ane, endo, labs)))
        bed = VGroup(*[para(s_, width=11.5, size=23, color=th.INK) for s_ in ["bed 1 m × 1 m × 0.5 m, about 1 kg (~1000) worms", "waste pre-digested ~20 days, mixed with ~30% dung; ~60% moisture; shade",
                                                                                 "harvest after 60–140 days: dark, odourless, crumbly; C:N about 21", "vermicompost 0.5–1.5% N (FYM ~0.5%) + P, K, hormones, helpful microbes; vermiwash as a spray"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        with self.say("A bed about a metre square, stocked with a kilogram of worms. Waste is pre digested for about twenty days, mixed with dung, kept moist and shaded. After two to four months, not thirty days as often claimed, you harvest dark, odourless compost with about one percent nitrogen, twice that of farmyard manure, plus potassium, phosphorus, plant hormones and useful microbes.") as v:
            for b_ in bed:
                self.play(FadeIn(b_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.15)
        self.play(FadeOut(VGroup(head, bed)))
        self.worked("A farmer applies 5 t/ha of vermicompost at 1.0% N or 5 t/ha of farmyard manure at 0.5% N. How much nitrogen does each supply, and how much urea (46% N) would make up the difference?",
                    [r"\text{vermi: } 5000 \times 0.010 = 50 \text{ kg N/ha};\quad \text{FYM: } 5000 \times 0.005 = 25 \text{ kg N/ha}", r"\frac{25}{0.46} = 54.3 \text{ kg urea per hectare}"],
                    ["A worked example.", "Fifty kilograms of nitrogen from vermicompost, twenty five from farmyard manure.", "The gap of twenty five kilograms would need fifty four kilograms of urea. But urea brings no organic matter, no potassium, and no living microbes."])
        pl = para("Pearl culture (nacre secreted by a mantle pearl sac; Mikimoto) and lac culture (resin from female Kerria lacca on kusum, ber, palas) are NOT practised in Nepal.", width=11.5, size=23, color=th.MUTED)
        with self.say("Two more cultures appear in the syllabus, though neither is practised in Nepal. Pearls form when a pearl sac in an oyster's mantle secretes nacre around a graft; culture was pioneered by Mikimoto. And lac is a resin secreted by the female lac insect, Kerria lacca, on trees like kusum, ber and palas."):
            self.play(FadeIn(pl))
        self.play(FadeOut(pl))
        self.quiz("In composite fish culture, the surface PHYTOPLANKTON feeder is",
                  ["catla", "silver carp", "rohu", "mrigal"], 1,
                  "Pause and think. Which carp eats plant plankton at the surface?",
                  "Silver carp. Catla also lives near the surface, which makes it the trap, but it eats zooplankton. Rohu feeds in the column and mrigal at the bottom.")

    # ------------------------------------------------------------------ part 2: microbiology
    def p2(self):
        self.section(1)
        rows = [["group", "what it is", "size", "antibiotics work?"], ["bacteria", "prokaryote: no nucleus, 70S ribosomes, peptidoglycan wall", "0.5–5 µm", "YES"], ["viruses", "nucleic acid in a protein coat; only inside cells", "20–300 nm", "no: antivirals"],
                ["protozoa", "single-celled eukaryotes", "5–100 µm", "no: antiprotozoals"], ["fungi", "eukaryotes with chitin walls", "varies", "no: antifungals"]]
        tb = B.table(rows, [2.0, 6.4, 1.8, 2.8], row_h=0.66, size=21, colors=[th.AMBER, th.INK, th.MUTED, th.MINT]).move_to([0, 1.0, 0])
        gram = para("Bacteria: coccus, bacillus, spirillum, vibrio. Gram-positive: thick peptidoglycan keeps crystal violet (purple). Gram-negative: takes the pink safranin. Mycobacterium's waxy wall needs the acid-fast stain.", width=12, size=21, color=th.BODY).move_to([0, -2.2, 0])
        with self.say("Microbes come in four groups, and the group decides the treatment. Bacteria are prokaryotes with a peptidoglycan wall and small ribosomes, the only group antibiotics can touch. Viruses are not even cells: just nucleic acid in a coat, multiplying inside our cells. Then protozoa and fungi, both eukaryotes. Bacteria are named by shape and by the Gram stain.") as v:
            B.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(gram))
        self.play(FadeOut(VGroup(tb, gram)))
        head = T("Koch's postulates: proving a microbe causes a disease", size=28, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        steps = ["found in every case, absent from the healthy", "isolated and grown in pure culture", "the culture causes the same disease in a healthy host", "re-isolated, and shown to be the same organism"]
        rows = VGroup(*[VGroup(T(str(i + 1), size=28, color=self.color, weight="BOLD"), T(s_, size=25, color=th.INK)).arrange(RIGHT, buff=0.35) for i, s_ in enumerate(steps)]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.3, 0])
        lim = para("Limits: some pathogens cannot be cultured (M. leprae, most viruses); healthy carriers exist (Salmonella Typhi).", width=11, size=22, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("How do we know a microbe causes a disease? Robert Koch's four rules, used for anthrax and tuberculosis. Find it in every case. Grow it pure. Give it to a healthy host and get the same disease. And recover the same microbe again. They have limits: some microbes will not grow in culture, and some people carry a pathogen while staying healthy.") as v:
            self.play(FadeIn(head))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.14)
            self.play(FadeIn(lim))
        self.play(FadeOut(VGroup(head, rows, lim)))
        routes = [("airborne", "TB, influenza, COVID-19, measles", th.SKY), ("faecal–oral", "typhoid, cholera, hepatitis A and E", th.AMBER), ("vector", "malaria (Anopheles), dengue (Aedes), kala-azar (sandfly)", th.CORAL),
                  ("blood and body fluids", "hepatitis B and C, HIV", th.PINK), ("contact, fomites", "ringworm, scabies", th.MINT), ("environment", "tetanus spores in soil", th.MUTED)]
        cards = VGroup(*[VGroup(T(a, size=24, color=c_, weight="BOLD"), para(b, width=3.6, size=19, color=th.BODY, align="center")).arrange(DOWN, buff=0.12) for a, b, c_ in routes]).arrange_in_grid(2, 3, buff=(0.6, 0.6)).move_to([0, 0.2, 0])
        cw = T("Hepatitis B does NOT spread by food or water — A and E do. Dengue: day-biting Aedes, not Culex.", size=21, color=th.CORAL).move_to([0, -2.6, 0])
        with self.say("A disease answer must name the route precisely. Airborne droplets for tuberculosis and COVID. Faecal oral, through water and food, for typhoid, cholera and hepatitis A and E. Vectors for malaria, dengue and kala azar. Blood for hepatitis B and H I V. Two traps: hepatitis B does not spread through food or water, and dengue is carried by the day biting Aedes, not Culex."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.15))
            self.play(FadeIn(cw))
        self.play(FadeOut(VGroup(cards, cw)))
        self.p2_tb()
        self.p2_vaccine()
        self.p2_antibiotic()
        self.p2_useful()

    def p2_tb(self):
        head = T("Tuberculosis and the Ziehl–Neelsen stain", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        slide = RoundedRectangle(corner_radius=0.2, width=5.0, height=3.4, stroke_color=th.MUTED, stroke_width=3, fill_color="#F6F0E6", fill_opacity=0.1).move_to([-3.0, -0.4, 0])
        rng = np.random.default_rng(8)
        cells = VGroup(*[Ellipse(width=0.22, height=0.08, stroke_width=0, fill_color="#E05A8A", fill_opacity=1).rotate(rng.uniform(0, PI)).move_to([-3.0 + rng.uniform(-2.0, 2.0), -0.4 + rng.uniform(-1.3, 1.3), 0]) for _ in range(40)])
        tb_ = VGroup(*[cells[i] for i in range(0, 40, 5)])
        others = VGroup(*[cells[i] for i in range(40) if i % 5])
        steps = ["1. carbol fuchsin + heat: dye forced through the waxy wall", "2. acid–alcohol: every other cell loses the red", "3. methylene blue counterstain"]
        cap = B.Captions(self, at=(3.4, 0.0, 0), width=5.6, size=23)
        with self.say("Tuberculosis is Nepal's most important bacterial disease. Mycobacterium tuberculosis has a waxy wall full of mycolic acid, which makes it slow growing, tough, and impossible to stain the normal way. So we use the Ziehl Neelsen method. Flood the sputum smear with red carbol fuchsin and heat it, driving the dye through the wax."):
            self.play(FadeIn(head), FadeIn(slide), FadeIn(cells))
            cap(steps[0], color="#E05A8A")
        with self.say("Wash with acid alcohol. Every other cell loses the red dye; the mycobacteria hold it. They are acid fast."):
            self.play(*[o_.animate.set_fill(th.MUTED, opacity=0.4) for o_ in others], run_time=1.2)
            cap(steps[1], color=th.AMBER)
        with self.say("Counterstain with blue. Red rods on a blue background: a positive smear, and an infectious patient."):
            self.play(*[o_.animate.set_fill(th.SKY, opacity=0.9) for o_ in others], run_time=1.2)
            cap(steps[2] + " → red bacilli on blue", color=th.SKY)
        self.play(FadeOut(VGroup(slide, cells)))
        cap.clear()
        tx = VGroup(*[para(s_, width=11.5, size=23, color=c_) for s_, c_ in [("DOTS: Directly Observed Treatment, Short-course — a STRATEGY, not a drug.", th.MINT),
                                                                            ("Regimen: isoniazid, rifampicin, pyrazinamide, ethambutol for 2 months, then isoniazid + rifampicin for 4.", th.INK),
                                                                            ("MDR-TB: resistant to at least isoniazid AND rifampicin. Nepal: 2.2% of new patients.", th.CORAL),
                                                                            ("BCG: live attenuated Mycobacterium BOVIS; protects young children from severe TB.", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.0, 0])
        with self.say("Treatment follows DOTS, a strategy in which a health worker watches each dose being swallowed: four drugs for two months, then two for four more. Multi drug resistant TB resists at least isoniazid and rifampicin. And the B C G vaccine is a weakened strain of Mycobacterium bovis, not tuberculosis, protecting young children from the severe forms.") as v:
            for t_ in tx:
                self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.17)
        self.play(FadeOut(VGroup(head, tx)))

    def p2_vaccine(self):
        head = T("Why vaccines work: primary and secondary responses", size=28, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 100, 25], x_length=8.0, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-1.2, -0.3, 0])
        xl = T("days", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.1)
        yl = T("antibody", size=20, color=th.MUTED).next_to(ax, LEFT, buff=0.1)
        f1 = ax.plot(lambda t: 8 * np.exp(-((t - 14) / 5) ** 2) if t < 30 else 0.5, x_range=[0, 30, 0.2], color=th.SKY, stroke_width=4)
        f2 = ax.plot(lambda t: 90 * np.exp(-((t - 38) / 6) ** 2) + 3, x_range=[30, 60, 0.2], color=th.AMBER, stroke_width=5)
        m1 = DashedLine(ax.c2p(0, 0), ax.c2p(0, 100), color=th.SKY)
        m2 = DashedLine(ax.c2p(32, 0), ax.c2p(32, 100), color=th.AMBER)
        l1 = VGroup(T("1st contact", size=20, color=th.SKY), T("slow, small, IgM", size=18, color=th.BODY)).arrange(DOWN, buff=0.05).move_to(ax.c2p(14, 35))
        l2 = VGroup(T("2nd contact", size=20, color=th.AMBER), T("fast, huge, IgG: memory", size=18, color=th.BODY)).arrange(DOWN, buff=0.05).move_to(ax.c2p(50, 80))
        with self.say("On first meeting an antigen, the immune system takes five to ten days to respond, and the antibody level stays small. On a second meeting, memory cells are waiting: the response comes in one to three days and is a hundred to a thousand times stronger. A vaccine gives you that first meeting safely, so the real infection meets the second response."):
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(m1), Create(f1), FadeIn(l1), run_time=1.6)
            self.play(Create(m2), Create(f2), FadeIn(l2), run_time=1.6)
        self.play(FadeOut(VGroup(head, ax, xl, yl, f1, f2, m1, m2, l1, l2)))
        rows = [["type", "how it is made", "examples"], ["live attenuated", "weakened pathogen", "BCG, measles–rubella, oral polio"], ["killed", "whole pathogen, killed", "injectable polio, rabies"], ["subunit / conjugate", "only the protective antigen", "hepatitis B, HPV, typhoid conjugate"],
                ["toxoid", "inactivated toxin", "tetanus, diphtheria"], ["mRNA / vector", "genetic instructions for the antigen", "COVID-19 vaccines"]]
        tb = B.table(rows, [3.0, 4.6, 5.0], row_h=0.6, size=22, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.8, 0])
        hist = para("Jenner (1796): cowpox protects against smallpox. Pasteur coined 'vaccine'. Smallpox eradicated 1980; Nepal's last wild polio case 2010. A vaccine = ARTIFICIAL ACTIVE immunity.", width=12, size=22, color=th.BODY).move_to([0, -2.4, 0])
        with self.say("Vaccines come in several types: live but weakened, like B C G and measles; killed; just the key antigen, like hepatitis B; toxoids against tetanus; and now m R N A. It began with Jenner in seventeen ninety six, using cowpox against smallpox, which was eradicated in nineteen eighty. A vaccine gives artificial active immunity: your own body does the work, and remembers.") as v:
            B.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(hist))
        self.play(FadeOut(VGroup(tb, hist)))

    def p2_antibiotic(self):
        head = T("Antibiotics", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        plate = Circle(radius=1.8, stroke_color=th.MUTED, stroke_width=3, fill_color="#E8DCC4", fill_opacity=0.15).move_to([-3.2, -0.4, 0])
        rng = np.random.default_rng(1)
        col = VGroup(*[Dot(plate.get_center() + polar(rng.uniform(0.3, 1.6), rng.uniform(0, TAU)), radius=0.08, color=th.AMBER) for _ in range(60)])
        mould = Circle(radius=0.35, stroke_width=0, fill_color="#5FB04A", fill_opacity=0.9).move_to(plate.get_center() + RIGHT * 0.6 + UP * 0.4)
        halo = Circle(radius=0.95, stroke_color=th.MINT, stroke_width=2).move_to(mould)
        txt = para("Fleming, 1928: a Penicillium mould cleared the Staphylococcus around it. Florey and Chain purified penicillin (1940–41); Nobel 1945 to all three. Streptomycin (1943) from Streptomyces griseus — a BACTERIUM.", width=5.6, size=21, color=th.INK).move_to([3.2, 0.4, 0])
        with self.say("In nineteen twenty eight Alexander Fleming came back to a bacterial plate spoiled by a mould, and noticed the bacteria had dissolved around it. The mould was Penicillium. Florey and Chain later purified penicillin, and the three shared the Nobel Prize. Streptomycin, the first drug against tuberculosis, came from Streptomyces, which is a filamentous bacterium, not a fungus."):
            self.play(FadeIn(head), FadeIn(plate), FadeIn(col))
            self.play(FadeIn(mould))
            inside = [c_ for c_ in col if np.linalg.norm(c_.get_center() - mould.get_center()) < 0.95]
            self.play(*[FadeOut(c_) for c_ in inside], Create(halo), run_time=1.4)
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(plate, col, mould, halo, txt)))
        cl = VGroup(*[para(s_, width=11.5, size=23, color=c_) for s_, c_ in [("Broad-spectrum (tetracycline, ampicillin) vs narrow (penicillin G).", th.INK), ("Bactericidal (kills: penicillins, rifampicin) vs bacteriostatic (stops growth: tetracyclines, sulfonamides).", th.INK),
                                                                            ("Targets are all PROKARYOTIC (wall, 70S ribosome, gyrase): antibiotics do nothing against a cold or flu.", th.CORAL),
                                                                            ("Resistance: β-lactamases, efflux pumps, altered targets; genes spread on plasmids. Drivers: over-the-counter sales, unfinished courses, use in poultry.", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.0, 0])
        with self.say("Antibiotics are broad or narrow spectrum, and either kill bacteria or just stop them growing. Every one of them hits something only bacteria have: the cell wall, the bacterial ribosome, bacterial enzymes. That is why antibiotics are useless against a cold or flu. And resistance spreads between bacteria on plasmids, driven by antibiotics sold without prescription and courses left unfinished.") as v:
            for c_ in cl:
                self.play(FadeIn(c_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.17)
        self.play(FadeOut(VGroup(head, cl)))
        self.worked("E. coli divides every 20 minutes. Starting from one cell, how many cells after 6 hours? Compare with M. tuberculosis, generation time about 18 hours.",
                    [r"n = \frac{6 \times 60}{20} = 18;\quad N = 2^{18} = 262\,144", r"\text{TB: } n = \frac{6}{18} = 0.33 \text{ — not even one doubling}"],
                    ["A growth example.", "Six hours is eighteen generations of twenty minutes: two to the eighteen, over a quarter of a million cells from one.",
                     "Tuberculosis has not even doubled once. That is why cholera strikes in hours, while tuberculosis takes weeks to appear and six months to cure."])

    def p2_useful(self):
        rows = [["field", "organism", "what it does"], ["curd, yoghurt", "Lactobacillus + Streptococcus thermophilus", "lactose → lactic acid; casein curdles"], ["bread, raksi, beer", "Saccharomyces cerevisiae", "sugar → CO₂ + ethanol"],
                ["citric acid", "Aspergillus niger", "industrial fermentation"], ["clot-busting", "Streptococcus", "streptokinase after heart attacks"], ["nitrogen fixation", "Rhizobium, Azotobacter, Anabaena in Azolla", "biofertilisers"],
                ["biopesticide", "Bacillus thuringiensis", "Cry toxin for caterpillars"], ["biogas", "methanogenic ARCHAEA", "dung → 50–70% methane"]]
        tb = B.table(rows, [2.8, 5.2, 4.8], row_h=0.58, size=21, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.4, 0])
        cw = T("Spirulina is a cyanobacterium; methanogens are archaea, not bacteria.", size=22, color=th.CORAL).move_to([0, -2.6, 0])
        with self.say("And the microbes that work for us. Lactobacillus turns milk sugar into lactic acid: curd. Yeast makes bread rise and ferments raksi. Aspergillus makes citric acid; a Streptococcus makes streptokinase to dissolve heart attack clots. Rhizobium fixes nitrogen, Bacillus thuringiensis kills caterpillars, and methane making archaea run Nepal's biogas plants.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
            self.play(FadeIn(cw))
        self.play(FadeOut(VGroup(tb, cw)))
        self.tip("Antibiotics act on bacteria only. Vaccination = artificial ACTIVE immunity; antiserum = artificial PASSIVE. Write Salmonella Typhi, not 'Salmonella typhi'.",
                 "Exam tip. Antibiotics act only on bacteria. A vaccine gives artificial active immunity; a ready made antiserum gives artificial passive immunity. And names matter: Salmonella Typhi, Apis cerana, Eisenia fetida.", width=8.6)
        self.quiz("BCG vaccine contains a live attenuated strain of",
                  ["Mycobacterium tuberculosis", "Mycobacterium bovis", "Mycobacterium leprae", "Streptomyces griseus"], 1,
                  "Last one. B C G is made from which organism?",
                  "Mycobacterium bovis, the cattle tuberculosis bacillus, weakened over years of culture. Mycobacterium tuberculosis is the tempting answer, but the vaccine strain is bovine.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Apis cerana is Nepal's hive bee; bee space makes movable frames possible.",
            "Bombyx mori: 5 instars, 4 moults; stifle, cook, reel. Eri silk is spun.",
            "Composite carp culture: six species, six feeding niches; Ovaprim for spawning.",
            "Buffalo gives 52% of Nepal's milk; chauri males are sterile; Eisenia fetida for compost.",
            "Koch's postulates; Ziehl–Neelsen: red acid-fast bacilli; DOTS; BCG = M. bovis.",
            "Vaccines = active immunity; antibiotics act only on bacteria; microbes make curd, biogas.",
        ], "Quick recap. Apis cerana is Nepal's hive bee, and the bee space makes the movable frame hive work. Silkworms pass five instars and four moults. Composite fish culture puts six carps in six niches. The buffalo gives most of our milk. Koch's postulates prove a microbe causes a disease, and the Ziehl Neelsen stain shows tuberculosis as red rods. Vaccines give active immunity, antibiotics act only on bacteria, and microbes also make our curd and our biogas.")
        self.outro("That was applied biology, and the end of Class 12 Biology. Ten units, from a plant cell to a whole population. Revise with the recaps, work every example yourself, and you are ready for the board. See you in the next subject.")
