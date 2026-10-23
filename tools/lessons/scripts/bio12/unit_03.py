import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
import _gen as G  # noqa: E402
from _gen import BASE, PAIR, RNA_PAIR, OLD, NEW, SUGAR, PHOS  # noqa: E402

TALL = "#7BE495"
DWARF = "#FFB547"
XC = "#F472B6"
YC = "#4CC9F0"


def polar_(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 3
    TITLE = "Genetics"
    SUBTITLE = "From the DNA molecule to Mendel's peas"
    SECTIONS = ["Genetic materials", "Mendelian genetics: the laws", "Mendelian genetics: beyond Mendel",
                "Linkage and crossing over", "Mutation and polyploidy"]
    NEXT = "Unit 4 · Embryology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        fam = VGroup(*[G.person(False, s=0.55) for _ in range(3)]).arrange(RIGHT, buff=0.7).move_to([0, -1.4, 0])
        mom = G.person(False, s=0.75).move_to([-1.2, 1.2, 0])
        dad = G.person(True, s=0.75).move_to([1.2, 1.2, 0])
        bar = Line(mom.get_right(), dad.get_left(), color=th.MUTED, stroke_width=3)
        drop = Line(bar.get_center(), bar.get_center() + DOWN * 1.3, color=th.MUTED, stroke_width=3)
        sib = Line([fam[0].get_center()[0], -0.6, 0], [fam[-1].get_center()[0], -0.6, 0], color=th.MUTED, stroke_width=3)
        ticks = VGroup(*[Line([f.get_center()[0], -0.6, 0], f.get_top(), color=th.MUTED, stroke_width=3) for f in fam])
        l1 = T("a third daughter", size=28, color=th.PINK).move_to([0, -2.4, 0])
        blame = T("\"It's the mother's fault.\"", size=34, color=th.CORAL, weight="BOLD").move_to([0, 2.6, 0])
        with self.say("In a village in Nepal, a third daughter is born. And, as so often happens, someone says it: the mother has failed again. She could not give a son."):
            self.play(FadeIn(mom), FadeIn(dad), Create(bar))
            self.play(Create(drop), Create(sib), Create(ticks), LaggedStart(*[FadeIn(f, scale=0.5) for f in fam], lag_ratio=0.4))
            self.play(FadeIn(l1))
            self.play(Write(blame))
        cross = Line(blame.get_left(), blame.get_right(), color=th.CORAL, stroke_width=6)
        with self.say("Biology says the opposite. Whether a baby is a girl or a boy is decided entirely by the father. Today you will be able to prove that, with a four box square, and a lot more besides."):
            self.play(Create(cross))
            self.play(Indicate(dad, color=th.SKY, scale_factor=1.3))
        nb = B.neby_in(self, "surprised", height=1.4)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(fam, mom, dad, bar, drop, sib, ticks, l1, blame, cross)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 3: Genetics, the biggest unit of botany. We start with the molecule that carries heredity, follow Mendel's peas, and end with what happens when the message gets damaged."):
            pass
        self.end_title(g, nb)
        self.roadmap("Our path. What the genetic material is, how it copies itself and how it makes a protein. Mendel's laws, worked through with Punnett squares and the chi square test. Then everything beyond Mendel: blood groups, sex determination, sex linkage and pedigrees. Linkage and crossing over, with gene maps. And mutation and polyploidy.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        self.p1_griffith()
        self.p1_hershey()
        self.p1_structure()
        self.p1_helix()
        self.p1_rna()
        self.p1_replication()
        self.p1_dogma()

    def p1_griffith(self):
        head = T("Griffith, 1928: transformation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        xs = [-4.8, -1.6, 1.6, 4.8]
        inj = ["live S", "live R", "heat-killed S", "heat-killed S + live R"]
        cols = [th.CORAL, th.SKY, "#8A6A6A", th.AMBER]
        res = [False, True, True, False]
        cards = VGroup()
        for x, i_, c_ in zip(xs, inj, cols):
            box = self.panel(2.9, 3.6).move_to([x, -0.4, 0])
            lab = para(i_, width=2.6, size=22, color=c_, align="center").move_to([x, 1.0, 0])
            cards.add(VGroup(box, lab))
        mice = [G.mouse(True).move_to([x, -0.5, 0]) for x in xs]
        outs = [G.mouse(r).move_to([x, -0.5, 0]) for x, r in zip(xs, res)]
        tags = VGroup(*[T("dies" if not r else "lives", size=24, color=th.CORAL if not r else th.MINT, weight="BOLD").move_to([x, -1.6, 0]) for x, r in zip(xs, res)])
        cap = B.Captions(self, at=(0, -2.75, 0), width=12.5, size=24)
        with self.say("Was heredity carried by protein or by DNA? Chromosomes contain both, and in nineteen twenty eight protein looked the better bet. Frederick Griffith worked with pneumonia bacteria. The S strain has a smooth capsule and kills. The R strain is rough, with no capsule, and is harmless."):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(c) for c in cards[:2]], lag_ratio=0.3), FadeIn(mice[0]), FadeIn(mice[1]))
            self.play(Transform(mice[0], outs[0]), FadeIn(tags[0]))
            self.play(Transform(mice[1], outs[1]), FadeIn(tags[1]))
        with self.say("Heat killed S bacteria alone: the mouse lives. But mix heat killed S with live harmless R, and the mouse dies. And from its blood, Griffith recovered living S bacteria."):
            self.play(FadeIn(cards[2]), FadeIn(mice[2]))
            self.play(Transform(mice[2], outs[2]), FadeIn(tags[2]))
            self.play(FadeIn(cards[3]), FadeIn(mice[3]))
            self.play(Transform(mice[3], outs[3]), FadeIn(tags[3]))
            self.sfx("impact", gain=-12)
            cap("Something from the dead S cells changed the living R cells permanently: the transforming principle.", color=th.AMBER)
        self.play(FadeOut(VGroup(cards, *mice, tags)))
        cap.clear()
        tubes = VGroup()
        for i, (enz, ok) in enumerate([("protease", True), ("RNase", True), ("DNase", False)]):
            tube = VGroup(RoundedRectangle(corner_radius=0.3, width=0.9, height=2.4, stroke_color=th.BODY, stroke_width=3),
                          Rectangle(width=0.86, height=1.2, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.35).shift(DOWN * 0.55))
            tube.move_to([-3.5 + 3.5 * i, -0.2, 0])
            lab = T("+ " + enz, size=26, color=th.INK, weight="BOLD").next_to(tube, UP, buff=0.25)
            out = T("transforms" if ok else "no transformation", size=24, color=th.MINT if ok else th.CORAL, weight="BOLD").next_to(tube, DOWN, buff=0.3)
            tubes.add(VGroup(tube, lab, out))
        h2 = T("Avery, MacLeod and McCarty, 1944", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Sixteen years later, Avery, MacLeod and McCarty repeated it in test tubes and destroyed one kind of molecule at a time. Destroy the protein: transformation still happens. Destroy the RNA: it still happens. Destroy the DNA, with DNase, and it stops. The transforming principle was DNA."):
            self.play(FadeOut(head), FadeIn(h2))
            for t_ in tubes:
                self.play(FadeIn(t_[0]), FadeIn(t_[1]), run_time=0.5)
                self.play(FadeIn(t_[2], shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(tubes[2], color=th.CORAL))
        self.play(FadeOut(VGroup(h2, tubes)))

    def phage(self, inner, coat):
        head = RegularPolygon(6, radius=0.45, stroke_color=coat, stroke_width=5, fill_color=th.BG, fill_opacity=1).rotate(PI / 6)
        dna = VMobject(stroke_color=inner, stroke_width=4).set_points_smoothly([[-0.2, 0.15, 0], [0.15, 0.2, 0], [-0.1, -0.05, 0], [0.2, -0.15, 0], [-0.15, -0.2, 0]])
        tail = Rectangle(width=0.14, height=0.6, stroke_color=coat, stroke_width=4).next_to(head, DOWN, buff=0)
        legs = VGroup(*[Line(tail.get_bottom(), tail.get_bottom() + [d, -0.3, 0], color=coat, stroke_width=3) for d in (-0.3, -0.12, 0.12, 0.3)])
        return VGroup(head, dna, tail, legs)

    def p1_hershey(self):
        head = T("Hershey and Chase, 1952", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        p1 = self.phage(th.AMBER, th.MUTED).move_to([-4.2, 1.2, 0])
        p2 = self.phage(th.MUTED, th.SKY).move_to([2.2, 1.2, 0])
        l1 = T("³²P labels DNA", size=24, color=th.AMBER).next_to(p1, RIGHT, buff=0.3)
        l2 = T("³⁵S labels protein coat", size=24, color=th.SKY).next_to(p2, RIGHT, buff=0.3)
        bac = VGroup(*[RoundedRectangle(corner_radius=0.3, width=1.8, height=0.8, stroke_color=th.MINT, stroke_width=3, fill_color="#173A1E", fill_opacity=1).move_to([x, -0.6, 0]) for x in (-4.2, 2.2)])
        with self.say("The clinching experiment used a virus that infects bacteria, phage T two. It is just DNA wrapped in a protein coat. Only DNA contains phosphorus, and only protein contains sulphur. So one batch of phages was labelled with radioactive phosphorus thirty two, in the DNA, and another with sulphur thirty five, in the coat."):
            self.play(FadeIn(head), FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2))
            self.play(FadeIn(bac))
            self.play(p1.animate.next_to(bac[0], UP, buff=0), p2.animate.next_to(bac[1], UP, buff=0))
        dna_in = VMobject(stroke_color=th.AMBER, stroke_width=4).set_points_smoothly([[-4.6, -0.6, 0], [-4.3, -0.45, 0], [-4.0, -0.75, 0], [-3.7, -0.55, 0]])
        dna2 = VMobject(stroke_color=th.MUTED, stroke_width=4).set_points_smoothly([[1.8, -0.6, 0], [2.1, -0.45, 0], [2.4, -0.75, 0], [2.7, -0.55, 0]])
        tubes = VGroup()
        for x, pel, sup in [(-4.2, th.AMBER, th.MUTED), (2.2, th.MUTED, th.SKY)]:
            t_ = RoundedRectangle(corner_radius=0.3, width=1.0, height=1.8, stroke_color=th.BODY, stroke_width=3).move_to([x, -2.25, 0])
            tubes.add(VGroup(t_, Rectangle(width=0.9, height=0.9, stroke_width=0, fill_color=sup, fill_opacity=0.35).move_to([x, -1.9, 0]),
                             Ellipse(width=0.8, height=0.35, stroke_width=0, fill_color=pel, fill_opacity=0.9).move_to([x, -2.9, 0])))
        r1 = para("radioactivity in the pellet, inside the bacteria", width=3.6, size=21, color=th.AMBER).next_to(tubes[0], RIGHT, buff=0.3)
        r2 = para("radioactivity in the liquid, with the empty coats", width=3.6, size=21, color=th.SKY).next_to(tubes[1], RIGHT, buff=0.3)
        with self.say("The phages infected the bacteria. Then a kitchen blender shook the empty coats off, and a centrifuge spun the heavy bacteria into a pellet. The phosphorus was inside the bacteria, and in the next generation of phages. The sulphur stayed outside, in the liquid. Only DNA had entered the cell. DNA is the genetic material."):
            self.play(Create(dna_in), Create(dna2))
            self.play(p1.animate.shift(UP * 0.9).set_opacity(0.4), p2.animate.shift(UP * 0.9).set_opacity(0.4), run_time=0.8)
            self.play(FadeIn(tubes), FadeOut(bac), FadeOut(dna_in), FadeOut(dna2))
            self.play(FadeIn(r1), FadeIn(r2))
        tmv = self.callout("remember", "In tobacco mosaic virus there is no DNA: Fraenkel-Conrat and Singer (1957) showed new viruses always match the RNA donor. In some viruses, RNA is the genetic material.", width=11, size=26)
        self.play(FadeOut(VGroup(p1, p2, l1, l2, tubes, r1, r2)))
        with self.say("One footnote. Tobacco mosaic virus has no DNA at all. When Fraenkel Conrat and Singer swapped the RNA and the protein coat between two strains, the new viruses always matched the RNA donor. So in some viruses, RNA is the genetic material."):
            self.play(FadeIn(tmv, shift=UP * 0.2))
        self.play(FadeOut(VGroup(tmv, head)))

    def p1_structure(self):
        head = T("The nucleotide", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        nt = G.nucleotide("A", s=1.6).move_to([-3.0, 0.3, 0])
        P = nt.parts
        cap = B.Captions(self, at=(3.4, 0.3, 0), width=5.8, size=26)
        with self.say("DNA is a polymer of nucleotides. Each nucleotide has three parts. A phosphate group. A five carbon sugar, deoxyribose. And a nitrogenous base. Base plus sugar alone is a nucleoside; add the phosphate and it becomes a nucleotide."):
            self.play(FadeIn(head))
            self.play(FadeIn(P["phosphate"], scale=1.3))
            cap("Phosphate", color=PHOS, swatch=PHOS)
            self.play(FadeIn(nt[0]), FadeIn(P["sugar"]))
            cap("Deoxyribose sugar", color=SUGAR, swatch=SUGAR, sub="A pentose; in RNA it is ribose, with an extra hydroxyl at carbon two.")
            self.play(FadeIn(nt[1]), FadeIn(P["base"]), FadeIn(P["label"]))
            cap("Nitrogenous base", color=BASE["A"], swatch=BASE["A"], sub="Base + sugar = nucleoside. + phosphate = nucleotide.")
        self.play(FadeOut(nt), FadeOut(head))
        cap.clear()
        pur = VGroup(*[VGroup(G.purine(BASE[b], 0.42), T(n_, size=24, color=BASE[b])).arrange(DOWN, buff=0.25) for b, n_ in [("A", "adenine"), ("G", "guanine")]]).arrange(RIGHT, buff=0.8)
        pyr = VGroup(*[VGroup(G.pyrimidine(BASE[b], 0.42), T(n_, size=24, color=BASE[b])).arrange(DOWN, buff=0.25) for b, n_ in [("C", "cytosine"), ("T", "thymine"), ("U", "uracil (RNA)")]]).arrange(RIGHT, buff=0.7)
        h1 = T("purines: double ring", size=28, color=th.INK, weight="BOLD")
        h2 = T("pyrimidines: single ring", size=28, color=th.INK, weight="BOLD")
        c1 = VGroup(h1, pur).arrange(DOWN, buff=0.4).move_to([-3.6, 0.2, 0])
        c2 = VGroup(h2, pyr).arrange(DOWN, buff=0.4).move_to([3.0, 0.2, 0])
        with self.say("The bases come in two shapes. Purines, adenine and guanine, have a double ring. Pyrimidines, cytosine, thymine, and in RNA uracil, have a single ring."):
            self.play(FadeIn(c1, shift=UP * 0.2))
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.play(FadeOut(VGroup(c1, c2)))
        chain = VGroup(*[G.nucleotide(b, s=0.9) for b in "ATGC"]).arrange(DOWN, buff=0.12).move_to([-3.0, 0.0, 0])
        bonds = VGroup(*[Line(chain[i].parts["sugar"].get_bottom(), chain[i + 1].parts["phosphate"].get_top(), color=PHOS, stroke_width=4) for i in range(3)])
        e5 = T("5′ end (free phosphate)", size=24, color=PHOS).next_to(chain, UP, buff=0.2)
        e3 = T("3′ end (free OH)", size=24, color=SUGAR).next_to(chain, DOWN, buff=0.2)
        cap = B.Captions(self, at=(3.4, 0.0, 0), width=5.8, size=26)
        with self.say("Nucleotides join through phosphodiester bonds, linking carbon three of one sugar to carbon five of the next through a phosphate. So a strand has a free phosphate at one end, the five prime end, and a free hydroxyl at the other, the three prime end. A strand has a direction."):
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.2) for c_ in chain], lag_ratio=0.2))
            self.play(Create(bonds))
            cap("Phosphodiester bonds", color=PHOS, swatch=PHOS, sub="3′ carbon of one sugar → phosphate → 5′ carbon of the next.")
            self.play(FadeIn(e5), FadeIn(e3))
        self.play(FadeOut(VGroup(chain, bonds, e5, e3)))
        cap.clear()
        bars = VGroup()
        vals = [("A", 30), ("T", 30), ("G", 20), ("C", 20)]
        for i, (b, v) in enumerate(vals):
            r = Rectangle(width=0.8, height=v * 0.1, stroke_width=0, fill_color=BASE[b], fill_opacity=0.9).move_to([-4.6 + i * 1.1, -2.0 + v * 0.05, 0])
            bars.add(VGroup(r, T(b, size=26, color=BASE[b], weight="BOLD").next_to(r, DOWN, buff=0.12), T(f"{v}%", size=22, color=th.INK).next_to(r, UP, buff=0.1)))
        rule = M(r"A = T,\quad G = C,\quad \frac{A+G}{T+C} = 1", size=46).move_to([3.0, 0.6, 0])
        note = para("purines = pyrimidines; but (A+T)/(G+C) differs between species", width=5.4, size=22, color=th.BODY).next_to(rule, DOWN, buff=0.35)
        h3 = T("Chargaff's rules, 1950", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("In nineteen fifty, Erwin Chargaff analysed DNA from many species and found a strange regularity. Adenine always equals thymine, and guanine always equals cytosine. So purines equal pyrimidines. Only the ratio of A plus T to G plus C changes from species to species."):
            self.play(FadeIn(h3), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.2))
            self.play(Write(rule), FadeIn(note))
        self.play(FadeOut(VGroup(h3, bars, rule, note)))

    def p1_helix(self):
        ph = ValueTracker(0.0)
        hx = G.Helix("ATGCGTACGATCCGTA", x0=-5.6, x1=5.6, amp=1.15, turns=1.6, phase=ph, center_y=0.5)
        head = T("Watson and Crick, 1953", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cap = B.Captions(self, at=(0, -2.4, 0), width=12, size=25)
        self.add(hx)
        with self.say("Then Rosalind Franklin's X ray photographs showed a helix. In nineteen fifty three James Watson and Francis Crick put it all together: the double helix.") as v:
            self.play(FadeIn(head), FadeIn(hx))
            self.play(ph.animate.set_value(PI), run_time=v.dur * 0.6, rate_func=rate_functions.linear)
        facts = [("Two antiparallel chains coiled into a right-handed helix: one runs 5′→3′, the other 3′→5′.", "Two chains, coiled round one axis into a right handed helix, and antiparallel: one runs five prime to three prime, the other the opposite way."),
                 ("Sugar–phosphate backbones outside; bases inside, paired across.", "The sugar phosphate backbones are on the outside. The bases point inwards and pair across the middle."),
                 ("A pairs with T, G pairs with C: always a purine with a pyrimidine, so the width never changes.", "A always pairs with T, and G with C. That is a purine with a pyrimidine every time, so the helix has a constant width. And it explains Chargaff's rules.")]
        for c_, sy in facts:
            with self.say(sy) as v:
                cap(c_)
                self.play(ph.animate.increment_value(PI * 0.6), run_time=v.dur * 0.7, rate_func=rate_functions.linear)
        self.play(FadeOut(hx), FadeOut(head))
        self.remove(hx)
        cap.clear()
        at = VGroup(G.base_chip("A", 0.8, 0.6, 30), G.base_chip("T", 0.8, 0.6, 30)).arrange(RIGHT, buff=1.4).move_to([-3.2, 0.9, 0])
        gc = VGroup(G.base_chip("G", 0.8, 0.6, 30), G.base_chip("C", 0.8, 0.6, 30)).arrange(RIGHT, buff=1.4).move_to([-3.2, -1.1, 0])
        hb1 = VGroup(*[DashedLine(at[0].get_right() + [0.05, dy, 0], at[1].get_left() + [-0.05, dy, 0], color=WHITE, stroke_width=3) for dy in (0.12, -0.12)])
        hb2 = VGroup(*[DashedLine(gc[0].get_right() + [0.05, dy, 0], gc[1].get_left() + [-0.05, dy, 0], color=WHITE, stroke_width=3) for dy in (0.18, 0, -0.18)])
        n1 = T("2 hydrogen bonds", size=26, color=th.INK).next_to(at, DOWN, buff=0.15)
        n2 = T("3 hydrogen bonds", size=26, color=th.INK).next_to(gc, DOWN, buff=0.15)
        dims = VGroup(*[VGroup(T(a, size=36, color=th.AMBER, weight="BOLD"), T(b, size=24, color=th.BODY)).arrange(RIGHT, buff=0.3)
                        for a, b in [("2 nm", "diameter"), ("3.4 nm", "one full turn (pitch)"), ("10 bp", "per turn"), ("0.34 nm", "between base pairs")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.0, 0])
        with self.say("Look closely at the pairs. A and T are held by two hydrogen bonds. G and C by three. That is why DNA rich in G and C needs a higher temperature to come apart."):
            self.play(FadeIn(at), FadeIn(gc))
            self.play(Create(hb1), FadeIn(n1))
            self.play(Create(hb2), FadeIn(n2))
        with self.say("And the numbers, which are asked every year. Diameter two nanometres. One full turn, the pitch, three point four nanometres, containing ten base pairs, so neighbouring base pairs are zero point three four nanometres apart. The coiling also leaves a wide major groove and a narrow minor groove.") as v:
            for d_ in dims:
                self.play(FadeIn(d_, shift=LEFT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.17)
        self.play(FadeOut(VGroup(at, gc, hb1, hb2, n1, n2, dims)))
        self.quiz("In the Watson–Crick model, one complete turn of the DNA helix measures",
                  ["0.34 nm", "2 nm", "3.4 nm", "20 nm"], 2,
                  "Pause and think. How long is one complete turn of the helix?",
                  "Three point four nanometres. Zero point three four is the gap between neighbouring base pairs, ten of which make a turn, and two nanometres is the width. Those three numbers are always offered together to catch you.")

    def p1_rna(self):
        rows = [["", "DNA", "RNA"], ["sugar", "deoxyribose", "ribose (2′-OH)"], ["bases", "A, G, C, T", "A, G, C, U"], ["strands", "double helix", "mostly single"],
                ["stability", "very stable", "short-lived"], ["Chargaff's rule", "obeyed", "not obeyed"], ["job", "stores information", "expresses it"]]
        tb = B.table(rows, [3.0, 4.2, 4.2], row_h=0.62, size=24, colors=[th.MUTED, th.SKY, th.PINK]).move_to([0, 0.6, 0])
        with self.say("RNA differs from DNA in three ways that matter. Its sugar is ribose, it has uracil instead of thymine, and it is usually single stranded. That extra hydroxyl on ribose makes it reactive and short lived: perfect for a temporary message, poor for permanent storage.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        mr = G.seq_row("AUGGCUUGG", w=0.5).move_to([-3.4, 1.8, 0])
        brs = VGroup(*[Brace(mr[3 * i:3 * i + 3], DOWN, color=th.MUTED) for i in range(3)])
        cods = VGroup(*[T("codon", size=20, color=th.MUTED).next_to(b_, DOWN, buff=0.05) for b_ in brs])
        trna = VMobject(stroke_color=th.PINK, stroke_width=6).set_points_smoothly([[2.0, 2.2, 0], [2.0, 1.2, 0], [1.2, 0.8, 0], [1.4, 0.2, 0], [2.1, 0.5, 0], [2.4, -0.4, 0], [2.0, -1.0, 0], [2.7, -1.0, 0], [2.6, -0.4, 0], [2.9, 0.5, 0], [3.6, 0.2, 0], [3.8, 0.8, 0], [3.0, 1.2, 0], [3.0, 2.2, 0]])
        acl = T("anticodon", size=22, color=th.PINK).next_to(trna, DOWN, buff=0.2)
        cca = T("CCA end: amino acid attaches", size=22, color=th.PINK).next_to(trna, UP, buff=0.15)
        ribo = VGroup(Ellipse(width=2.2, height=1.0, stroke_width=0, fill_color="#5C6BC0", fill_opacity=0.8).move_to([-3.4, -1.0, 0]),
                      Ellipse(width=1.8, height=0.7, stroke_width=0, fill_color="#7986CB", fill_opacity=0.8).move_to([-3.4, -1.85, 0]))
        cap = B.Captions(self, at=(0, -2.85, 0), width=12, size=24)
        with self.say("Three kinds of RNA build proteins. Messenger RNA, only three to five percent of the cell's RNA, carries the copy of a gene to the ribosome. It is read three bases at a time, in codons."):
            self.play(FadeIn(mr), Create(brs), FadeIn(cods))
            cap("mRNA (~3–5%): the message, read in codons", color=th.AMBER)
        with self.say("Transfer RNA is the adapter. It is the smallest RNA, folded into a clover leaf, with an anticodon loop at one end and the amino acid carried at its C C A end. About fifteen percent."):
            self.play(Create(trna), FadeIn(acl), FadeIn(cca))
            cap("tRNA (~15%): clover-leaf adapter; anticodon + amino acid", color=th.PINK)
        with self.say("And ribosomal RNA, about eighty percent, builds the ribosome with proteins. Remarkably, it is the R N A that actually forms each peptide bond: it is a ribozyme."):
            self.play(FadeIn(ribo))
            cap("rRNA (~80%): builds the ribosome; makes the peptide bond (ribozyme)", color="#7986CB")
        self.play(FadeOut(VGroup(mr, brs, cods, trna, acl, cca, ribo)))
        cap.clear()

    def p1_replication(self):
        head = T("Replication is semi-conservative", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        models = VGroup()
        for i, (nm, kids) in enumerate([("conservative", [(OLD, OLD), (NEW, NEW)]), ("semi-conservative", [(OLD, NEW), (NEW, OLD)]), ("dispersive", [("mix", "mix"), ("mix", "mix")])]):
            g = VGroup(T(nm, size=24, color=th.INK, weight="BOLD"))
            par = VGroup(Line(UP * 0.7, DOWN * 0.7, color=OLD, stroke_width=8), Line(UP * 0.7, DOWN * 0.7, color=OLD, stroke_width=8).shift(RIGHT * 0.25))
            ch = VGroup()
            for k, (a, b) in enumerate(kids):
                def strand(c):
                    if c == "mix":
                        return VGroup(*[Line(UP * (0.7 - 0.35 * j), UP * (0.35 - 0.35 * j), color=OLD if j % 2 == 0 else NEW, stroke_width=8) for j in range(4)])
                    return Line(UP * 0.7, DOWN * 0.7, color=c, stroke_width=8)
                pr = VGroup(strand(a), strand(b).shift(RIGHT * 0.25)).shift(RIGHT * (k * 0.9 - 0.45))
                ch.add(pr)
            ar = Arrow(UP * 0.2, DOWN * 0.4, buff=0, color=th.MUTED, stroke_width=3)
            g.add(par, ar, ch)
            g.arrange(DOWN, buff=0.22)
            models.add(g)
        models.arrange(RIGHT, buff=1.5).move_to([0, 0.0, 0])
        with self.say("When DNA copies itself, what happens to the old strands? There were three ideas. Conservative: the old molecule stays whole and a brand new one is made. Semi conservative: the strands separate, and each daughter keeps one old strand. Dispersive: old and new pieces scattered through both."):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(m_, shift=UP * 0.2) for m_ in models], lag_ratio=0.4), run_time=2.4)
        self.play(FadeOut(models))

        def tube(x, bands):
            t_ = RoundedRectangle(corner_radius=0.35, width=1.0, height=3.4, stroke_color=th.BODY, stroke_width=3).move_to([x, -0.3, 0])
            g = VGroup(t_)
            for y, w in bands:
                g.add(Rectangle(width=0.85, height=0.12, stroke_width=0, fill_color=th.AMBER, fill_opacity=w).move_to([x, y, 0]))
            return g

        yH, yM, yL = -1.3, -0.3, 0.7
        tubes = VGroup(tube(-3.6, [(yH, 1)]), tube(0, [(yM, 1)]), tube(3.6, [(yM, 0.9), (yL, 0.9)]))
        labs = VGroup(*[T(s_, size=22, color=th.BODY).next_to(t_, DOWN, buff=0.2) for s_, t_ in zip(["grown in ¹⁵N", "1 generation in ¹⁴N", "2 generations in ¹⁴N"], tubes)])
        dl = VGroup(T("light", size=20, color=th.MUTED).move_to([5.3, yL, 0]), T("hybrid", size=20, color=th.MUTED).move_to([5.3, yM, 0]), T("heavy", size=20, color=th.MUTED).move_to([5.3, yH, 0]))
        with self.say("Meselson and Stahl settled it in nineteen fifty eight. They grew E coli on heavy nitrogen fifteen, then moved it to ordinary nitrogen fourteen, and spun the DNA in a density gradient. At the start: one heavy band. After one generation: one band, of intermediate, hybrid density. That alone kills the conservative model, which predicts a heavy and a light band."):
            self.play(FadeIn(tubes[0]), FadeIn(labs[0]), FadeIn(dl))
            self.play(FadeIn(tubes[1]), FadeIn(labs[1]))
        with self.say("After two generations: half hybrid, half light. The dispersive model predicts a single band drifting lighter, so that is out too. Only semi conservative replication fits."):
            self.play(FadeIn(tubes[2]), FadeIn(labs[2]))
            self.sfx("correct", gain=-12)
        self.play(FadeOut(VGroup(head, tubes, labs, dl)))
        self.p1_fork()

    def p1_fork(self):
        head = T("The replication fork", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        open_ = ValueTracker(0.0)
        y0 = 0.3
        XL = -5.6
        xf = lambda: -4.6 + 9.0 * open_.get_value()

        def strands():
            x = xf()
            g = VGroup(Line([x, y0 + 0.12, 0], [6.4, y0 + 0.12, 0], color=OLD, stroke_width=7), Line([x, y0 - 0.12, 0], [6.4, y0 - 0.12, 0], color=OLD, stroke_width=7))
            if x > XL + 0.8:
                g.add(VMobject(stroke_color=OLD, stroke_width=7).set_points_as_corners([[XL, y0 + 1.1, 0], [x - 0.7, y0 + 1.1, 0], [x, y0 + 0.12, 0]]))
                g.add(VMobject(stroke_color=OLD, stroke_width=7).set_points_as_corners([[XL, y0 - 1.1, 0], [x - 0.7, y0 - 1.1, 0], [x, y0 - 0.12, 0]]))
            return g

        st = always_redraw(strands)
        heli = always_redraw(lambda: VGroup(Circle(radius=0.28, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.9).move_to([xf() + 0.05, y0, 0])))
        t5 = VGroup(T("3′", size=22, color=OLD).move_to([XL - 0.35, y0 + 1.1, 0]), T("5′", size=22, color=OLD).move_to([XL - 0.35, y0 - 1.1, 0]))
        fork_dir = Arrow([3.6, 2.2, 0], [5.4, 2.2, 0], buff=0, color=th.MUTED, stroke_width=3)
        fd = T("fork moves", size=20, color=th.MUTED).next_to(fork_dir, UP, buff=0.05)
        cap = B.Captions(self, at=(0, -2.55, 0), width=12, size=24)
        with self.say("Now watch a fork. Replication starts at a fixed spot, the origin. Helicase, the red bead, unzips the helix by breaking the hydrogen bonds. Topoisomerase relieves the twisting ahead of it, and single strand binding proteins hold the opened strands apart."):
            self.play(FadeIn(head))
            self.add(st, heli)
            self.play(open_.animate.set_value(0.3), run_time=2.0)
            self.play(FadeIn(t5), GrowArrow(fork_dir), FadeIn(fd))
            cap("Helicase unwinds · topoisomerase relieves supercoiling · SSB proteins hold strands apart")
        lead = always_redraw(lambda: Arrow([XL + 0.1, y0 + 0.75, 0], [xf() - 0.75, y0 + 0.75, 0], buff=0, color=NEW, stroke_width=7, max_tip_length_to_length_ratio=0.06))
        with self.say("DNA polymerase three can only add nucleotides to a free three prime end, so every new strand is built five prime to three prime. On the top template, that direction points into the fork. So this new strand grows smoothly, chasing the helicase. That is the leading strand."):
            self.add(lead)
            self.play(open_.animate.set_value(0.52), run_time=2.6)
            cap("Leading strand: made continuously, 5′→3′, towards the fork", color=NEW)
        frags = VGroup()
        for a_, b_ in [(-5.45, -4.15), (-4.05, -2.75)]:
            frags.add(VGroup(Line([b_, y0 - 0.75, 0], [b_ - 0.2, y0 - 0.75, 0], color=th.AMBER, stroke_width=8),
                             Arrow([b_ - 0.2, y0 - 0.75, 0], [a_, y0 - 0.75, 0], buff=0, color=th.AMBER, stroke_width=6, max_tip_length_to_length_ratio=0.15)))
        with self.say("The bottom template runs the other way. So here the polymerase must work away from the fork, in short backward pieces. Each piece is started by a little RNA primer, laid down by primase. These pieces are Okazaki fragments, a thousand to two thousand nucleotides long. This is the lagging strand."):
            cap("Lagging strand: Okazaki fragments, each made 5′→3′, away from the fork", color=th.AMBER)
            self.play(FadeIn(frags))
            last = -2.75
            for k in range(3):
                x_end = xf() - 0.55
                if x_end - last < 1.0:
                    self.play(open_.animate.increment_value(0.12), run_time=0.5)
                    x_end = xf() - 0.55
                prim = Line([x_end, y0 - 0.75, 0], [x_end - 0.25, y0 - 0.75, 0], color=th.CORAL, stroke_width=8)
                fr = Arrow([x_end - 0.25, y0 - 0.75, 0], [last + 0.08, y0 - 0.75, 0], buff=0, color=th.AMBER, stroke_width=6, max_tip_length_to_length_ratio=0.15)
                self.play(Create(prim), run_time=0.3)
                self.play(GrowArrow(fr), run_time=0.6)
                frags.add(VGroup(prim, fr))
                last = x_end
                if xf() < 5.0:
                    self.play(open_.animate.increment_value(0.13), run_time=0.6)
        with self.say("Finally DNA polymerase one replaces the RNA primers with DNA, and DNA ligase seals the nicks between the fragments. One strand continuous, the other in pieces: replication is semi discontinuous."):
            self.play(*[f_[0].animate.set_color(th.AMBER) for f_ in frags])
            cap("Pol I replaces primers · ligase seals nicks · semi-discontinuous replication", color=th.MINT)
        self.play(FadeOut(VGroup(head, st, heli, lead, frags, t5, fork_dir, fd)))
        self.remove(st, lead, heli)
        cap.clear()
        rows = [["enzyme", "job"], ["helicase", "unwinds, breaking hydrogen bonds"], ["topoisomerase (gyrase)", "relieves supercoiling ahead of the fork"], ["SSB proteins", "keep the strands apart"],
                ["primase", "lays a short RNA primer (free 3′-OH)"], ["DNA polymerase III", "adds nucleotides 5′→3′: main builder"], ["DNA polymerase I", "removes primers, fills gaps"], ["DNA ligase", "seals nicks (phosphodiester bonds)"]]
        tb = B.table(rows, [4.2, 7.2], row_h=0.6, size=24, colors=[th.AMBER, th.INK]).move_to([0, 0.3, 0])
        with self.say("Here are the seven enzymes in one table, the way the examiner wants them: helicase, topoisomerase, single strand binding proteins, primase, polymerase three, polymerase one, and ligase.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.tip("New DNA is ALWAYS made 5′→3′; the template is read 3′→5′. Each Okazaki fragment is itself made 5′→3′.",
                 "Exam tip. Never write that the lagging strand is made three prime to five prime. Every piece of new DNA, including every Okazaki fragment, is made five prime to three prime. Only the overall growth of the lagging strand runs away from the fork.")

    def p1_dogma(self):
        steps = VGroup(*[T(s_, size=40, color=c_, weight="BOLD") for s_, c_ in [("DNA", OLD), ("RNA", th.PINK), ("protein", th.AMBER)]]).arrange(RIGHT, buff=2.2).move_to([0, 2.2, 0])
        arr = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.2, color=th.MUTED, stroke_width=4) for i in range(2)])
        lab = VGroup(T("transcription", size=22, color=th.MUTED).next_to(arr[0], UP, buff=0.1), T("translation", size=22, color=th.MUTED).next_to(arr[1], UP, buff=0.1))
        loop = CurvedArrow(steps[0].get_left() + LEFT * 0.1 + DOWN * 0.1, steps[0].get_left() + LEFT * 0.1 + UP * 0.25, angle=-PI * 1.4, color=th.MUTED, stroke_width=3)
        with self.say("Crick summed up what DNA is for in his central dogma. DNA copies itself by replication. It is transcribed into RNA. And RNA is translated into protein. In retroviruses like H I V, reverse transcriptase even copies RNA back into DNA."):
            self.play(FadeIn(steps[0]), Create(loop))
            self.play(GrowArrow(arr[0]), FadeIn(lab[0]), FadeIn(steps[1]))
            self.play(GrowArrow(arr[1]), FadeIn(lab[1]), FadeIn(steps[2]))
        tmpl = "TACCGAACCATT"
        tr = G.seq_row(tmpl, w=0.5).move_to([0, 0.6, 0])
        tl = T("template strand 3′", size=22, color=OLD).next_to(tr, LEFT, buff=0.25)
        mr = VGroup(*[G.base_chip(RNA_PAIR[b], 0.5, 0.5) for b in tmpl]).arrange(RIGHT, buff=0.06).next_to(tr, DOWN, buff=0.25)
        ml = T("mRNA 5′", size=22, color=th.PINK).next_to(mr, LEFT, buff=0.25)
        cap = B.Captions(self, at=(0, -2.6, 0), width=12, size=24)
        with self.say("Transcription. RNA polymerase binds a promoter, opens a short stretch of DNA, and copies just one strand, the template strand, adding ribonucleotides five prime to three prime. Opposite every A it puts U, not T.") as v:
            self.play(FadeIn(tr), FadeIn(tl))
            self.play(FadeIn(ml))
            per = (v.dur - 2.0) / len(mr)
            for c_ in mr:
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=max(0.12, per))
            cap("Only the template (antisense) strand is copied; the mRNA matches the coding strand, with U for T.", color=th.PINK)
        with self.say("In eukaryotes this first transcript is then processed: a cap at the five prime end, a poly A tail at the three prime end, and the introns, the non coding pieces, are cut out while the exons are spliced together."):
            cap("Processing: 5′ cap + poly-A tail + splicing (introns out, exons joined)")
        self.play(FadeOut(VGroup(tr, tl, steps, arr, lab, loop)), mr.animate.move_to([0, 1.9, 0]), ml.animate.next_to(mr.copy().move_to([0, 1.9, 0]), LEFT, buff=0.25))
        cap.clear()
        grid = VGroup(*[Square(side_length=0.22, stroke_width=1, stroke_color=th.FAINT, fill_color=th.AMBER if k < 61 else th.CORAL, fill_opacity=0.7) for k in range(64)]).arrange_in_grid(8, 8, buff=0.04).move_to([-3.8, -0.6, 0])
        gl = M(r"4^3 = 64 \text{ codons}", size=40).next_to(grid, UP, buff=0.25)
        props = VGroup(*[T(s_, size=24, color=th.INK) for s_ in ["61 sense codons · 3 stop: UAA, UAG, UGA", "AUG = start, and methionine", "triplet, non-overlapping, comma-less",
                                                                    "degenerate: most amino acids have several codons", "unambiguous, and nearly universal"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -0.6, 0])
        with self.say("The code. Four bases read in threes give four cubed, sixty four codons. Sixty one code for amino acids, and three, U A A, U A G and U G A, mean stop. A U G means start, and methionine. The code is triplet, non overlapping and comma less. It is degenerate: most amino acids have several codons. It is unambiguous, and almost universal, the same in bacteria, in rice and in you.") as v:
            self.play(FadeOut(mr), FadeOut(ml))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in grid], lag_ratio=0.01), Write(gl), run_time=1.6)
            for p_ in props:
                self.play(FadeIn(p_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.12)
        self.play(FadeOut(VGroup(grid, gl, props)))
        self.p1_translate()

    def tr_step(self, i, seq, cods, names, cols, chain, ribo):
        aa = VGroup(Circle(radius=0.32, stroke_width=0, fill_color=cols[i], fill_opacity=1), T(names[i], size=20, color="#0B0E1A", weight="BOLD"))
        anti = VGroup(*[G.base_chip({"A": "U", "U": "A", "G": "C", "C": "G"}[b], 0.5, 0.4, 20) for b in seq[3 * i:3 * i + 3]]).arrange(RIGHT, buff=0.04)
        stem = Line(UP * 0, UP * 0.6, color=th.PINK, stroke_width=5)
        t_ = VGroup(anti, stem.next_to(anti, UP, buff=0), aa.next_to(anti, UP, buff=0.6))
        t_.move_to(cods[i].get_center() + UP * 1.25).shift(UP * 2)
        self.play(t_.animate.shift(DOWN * 2), run_time=0.6)
        if len(chain):
            self.play(chain.animate.next_to(aa, LEFT, buff=0.05), run_time=0.4)
            self.sfx("pop", gain=-14)
        chain.add(aa.copy())
        self.remove(aa)
        self.add(chain)
        self.play(FadeOut(VGroup(anti, stem)), run_time=0.3)
        if i < 2:
            self.play(ribo.animate.shift(RIGHT * 3 * 0.66), chain.animate.shift(RIGHT * 3 * 0.66), run_time=0.5)

    def p1_translate(self):
        seq = "AUGGCUUGGUAA"
        mr = G.seq_row(seq, w=0.62, gap=0.04).move_to([0, -0.9, 0])
        cods = [mr[3 * i:3 * i + 3] for i in range(4)]
        names = ["Met", "Ala", "Trp", "stop"]
        cols = [th.AMBER, th.MINT, th.SKY, th.CORAL]
        ribo = VGroup(Ellipse(width=2.4, height=1.5, stroke_width=0, fill_color="#5C6BC0", fill_opacity=0.55).move_to(cods[0].get_center() + UP * 0.75 + RIGHT * 0.95),
                      Ellipse(width=2.2, height=0.8, stroke_width=0, fill_color="#7986CB", fill_opacity=0.55).move_to(cods[0].get_center() + DOWN * 0.15 + RIGHT * 0.95))
        chain = VGroup()
        cap = B.Captions(self, at=(0, -2.6, 0), width=12, size=24)
        head = T("Translation on the ribosome", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Translation. Each amino acid is first loaded onto its own transfer RNA, using ATP. Then the small ribosomal subunit grips the messenger and finds the start codon, A U G. The first transfer RNA, carrying methionine, pairs with it."):
            self.play(FadeIn(head), FadeIn(mr), FadeIn(ribo))
            cap("Activation · initiation at AUG (P site)")
            self.tr_step(0, seq, cods, names, cols, chain, ribo)
        with self.say("Elongation, over and over. The next transfer RNA enters the A site, its anticodon pairing with the codon. The ribosomal RNA joins the growing chain to the new amino acid with a peptide bond, and the ribosome moves on one codon. The empty transfer RNA leaves from the E site."):
            cap("Elongation: tRNA into A site · peptide bond (peptidyl transferase) · translocate one codon")
            self.tr_step(1, seq, cods, names, cols, chain, ribo)
            self.tr_step(2, seq, cods, names, cols, chain, ribo)
        with self.say("When a stop codon arrives, U A A here, no transfer RNA fits it. A release factor binds, the finished chain is set free, and the ribosome falls apart. Several ribosomes usually read one messenger at once, a polysome."):
            self.play(ribo.animate.shift(RIGHT * 3 * 0.66), chain.animate.shift(RIGHT * 3 * 0.66), run_time=0.5)
            self.play(Indicate(cods[3], color=th.CORAL))
            self.play(chain.animate.shift(UP * 1.5 + RIGHT * 0.5), FadeOut(ribo), run_time=0.8)
            cap("Termination at a stop codon: release factor · polypeptide freed", color=th.CORAL)
        self.play(FadeOut(VGroup(head, mr, chain)))
        cap.clear()
        gene = VGroup()
        parts_ = [("exon", 1.6, th.MINT), ("intron", 1.0, th.FAINT), ("exon", 1.4, th.MINT), ("intron", 1.2, th.FAINT), ("exon", 1.3, th.MINT)]
        x = -3.25
        for n_, w_, c_ in parts_:
            r = Rectangle(width=w_, height=0.6, stroke_width=0, fill_color=c_, fill_opacity=0.9).move_to([x + w_ / 2, 0.6, 0])
            gene.add(VGroup(r, T(n_, size=20, color="#0B0E1A" if c_ == th.MINT else th.INK).move_to(r)))
            x += w_
        defs = VGroup(*[T(s_, size=25, color=th.INK) for s_ in ["gene: a DNA segment coding one polypeptide or functional RNA", "locus: its fixed place on a chromosome; alleles: its alternative forms",
                                                                   "cistron (function) · muton (mutation) · recon (recombination)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.5, 0])
        with self.say("So what is a gene? A segment of DNA that carries the information for one polypeptide or one functional RNA. In a eukaryote it is usually a split gene: coding exons interrupted by non coding introns. Its fixed place on a chromosome is its locus, and its alternative forms are alleles. In molecular terms, the unit of function is the cistron, of mutation the muton, and of recombination the recon."):
            self.play(LaggedStart(*[FadeIn(g_) for g_ in gene], lag_ratio=0.2))
            self.play(LaggedStart(*[FadeIn(d_, shift=UP * 0.15) for d_ in defs], lag_ratio=0.4), run_time=2.0)
        self.play(FadeOut(VGroup(gene, defs)))

    # ------------------------------------------------------------------ part 2: Mendel's laws
    def p2(self):
        self.section(1)
        self.p2_mendel()
        self.p2_mono()
        self.p2_test()
        self.p2_di()
        self.p2_chi()

    def p2_mendel(self):
        head = T("Gregor Mendel, 1856–1863", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        why = VGroup(*[VGroup(T(str(i + 1), size=28, color=self.color, weight="BOLD"), T(s_, size=26, color=th.INK)).arrange(RIGHT, buff=0.3)
                       for i, s_ in enumerate(["one pair of contrasting characters at a time", "pure, true-breeding lines first", "he counted, and did the arithmetic", "he followed F₁, F₂ and F₃"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-2.4, 0.2, 0])
        pea = VGroup(G.pea(True), G.pea(False).shift(RIGHT * 1.0)).move_to([4.2, -0.3, 0])
        pl = T("Pisum sativum", size=24, color=TALL).next_to(pea, DOWN, buff=0.2)
        with self.say("Gregor Mendel, a monk in Brno, worked on the garden pea from eighteen fifty six to eighteen sixty three, and published in eighteen sixty six. Nobody understood him until nineteen hundred, when de Vries, Correns and Tschermak rediscovered his work. He succeeded because of four decisions.") as v:
            self.play(FadeIn(head), FadeIn(pea), FadeIn(pl))
            for w_ in why:
                self.play(FadeIn(w_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.12)
        with self.say("And the pea was a lucky choice. It pollinates itself, because the keel petals wrap the stamens and stigma, so pure lines are easy to keep. Yet it can be crossed by hand after removing the anthers. It grows fast, gives many seeds, and shows seven clear pairs of characters."):
            self.play(Indicate(pea, color=TALL))
        self.play(FadeOut(VGroup(why, pea, pl)))
        rows = [["character", "dominant", "recessive"], ["stem height", "tall", "dwarf"], ["flower position", "axial", "terminal"], ["flower colour", "violet", "white"],
                ["pod shape", "inflated", "constricted"], ["pod colour", "green", "yellow"], ["seed shape", "round", "wrinkled"], ["cotyledon colour", "yellow", "green"]]
        tb = B.table(rows, [3.6, 3.2, 3.2], row_h=0.58, size=24, colors=[th.MUTED, TALL, DWARF]).move_to([0, 0.0, 0])
        with self.say("His seven pairs. Tall over dwarf, axial flowers over terminal, violet over white, inflated pods over constricted, green pods over yellow, round seeds over wrinkled, and yellow cotyledons over green.") as v:
            self.play(FadeOut(head))
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        words = [("gene, locus", "a unit of inheritance at a fixed place on a chromosome"), ("allele", "one form of a gene: T or t"), ("dominant / recessive", "expressed / masked in the heterozygote"),
                 ("homozygous / heterozygous", "TT or tt / Tt"), ("genotype / phenotype", "genetic make-up / appearance"), ("test cross", "F₁ × the homozygous recessive")]
        rows = VGroup(*[VGroup(T(a, size=25, color=th.AMBER, weight="BOLD"), T(b, size=24, color=th.INK)).arrange(RIGHT, buff=0.4) for a, b in words]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0, 0])
        with self.say("The words you must use exactly. A gene sits at a locus. Its forms are alleles. Dominant is expressed in the heterozygote, recessive is masked. Homozygous means both alleles alike, heterozygous means different. Genotype is the genetic make up, phenotype the appearance.") as v:
            for r_ in rows[:5]:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.45)
                self.hold(v.dur * 0.14)
        self.play(FadeOut(rows[:5]))
        self.remove(rows)

    def tall_dwarf(self, gt):
        tall = "T" in gt
        p = G.pea(tall, color=TALL if tall else DWARF, h=0.62 if tall else 0.3)
        return p

    def p2_mono(self):
        head = T("A monohybrid cross", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        P1 = VGroup(G.pea(True, TALL), T("TT", size=30, color=TALL, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-4.6, 1.2, 0])
        P2 = VGroup(G.pea(False, DWARF), T("tt", size=30, color=DWARF, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-2.4, 1.2, 0])
        x = T("×", size=40, color=th.MUTED).move_to([-3.5, 1.4, 0])
        g1 = VGroup(T("gametes:", size=22, color=th.MUTED), T("T", size=30, color=TALL, weight="BOLD"), T("t", size=30, color=DWARF, weight="BOLD")).arrange(RIGHT, buff=0.5).move_to([-3.5, -0.3, 0])
        F1 = VGroup(G.pea(True, TALL), T("F₁: all Tt, all tall", size=26, color=TALL, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-3.5, -2.0, 0])
        with self.say("Mendel crossed a pure tall plant, T T, with a pure dwarf, t t. Each parent makes only one kind of gamete: T, or t. So every F one plant is T t. And every one of them is tall. The dwarf character seems to have vanished."):
            self.play(FadeIn(head), FadeIn(P1), FadeIn(x), FadeIn(P2))
            self.play(FadeIn(g1, shift=DOWN * 0.2))
            self.play(FadeIn(F1, shift=DOWN * 0.2))
        grid, sq, tx = G.punnett(["T", "t"], ["T", "t"], [["TT", "Tt"], ["Tt", "tt"]], cell=1.25, size=30)
        grid.move_to([2.6, 0.2, 0])
        sel = T("F₁ selfed: Tt × Tt", size=26, color=th.INK, weight="BOLD").next_to(grid, UP, buff=0.3)
        with self.say("Now let the F one plants pollinate themselves. Each makes two kinds of gamete, T and t, in equal numbers. Put them on the sides of a Punnett square and fill it in.") as v:
            self.play(FadeIn(sel), FadeIn(VGroup(*[m for m in grid if m not in tx.values()])))
            for k in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                self.play(FadeIn(tx[k], scale=1.3), run_time=0.4)
        r1 = T("3 tall : 1 dwarf", size=34, color=th.INK, weight="BOLD").next_to(grid, DOWN, buff=0.35)
        r2 = T("1 TT : 2 Tt : 1 tt", size=28, color=th.AMBER).next_to(r1, DOWN, buff=0.15)
        with self.say("Three boxes contain a T, so three tall. One box, t t, is dwarf. Phenotypes three to one. Genotypes one T T, two T t, one t t. Mendel actually counted seven hundred and eighty seven tall and two hundred and seventy seven dwarf: two point eight four to one. The dwarf was never destroyed. It was hiding."):
            self.play(*[sq[k].animate.set_fill(TALL, opacity=0.35) for k in [(0, 0), (0, 1), (1, 0)]], sq[(1, 1)].animate.set_fill(DWARF, opacity=0.5))
            self.play(Write(r1))
            self.play(FadeIn(r2))
            nb = B.neby_in(self, "surprised", height=1.2)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, P1, P2, x, g1, F1, grid, sel, r1, r2)))
        l1 = self.callout("key", "Law of dominance: in a hybrid only the dominant allele is expressed; the recessive stays unexpressed but unchanged.", width=11, size=27)
        l2 = self.callout("key", "Law of segregation (purity of gametes): the two alleles separate at gamete formation, so each gamete carries only one. A gamete is never hybrid.", width=11, size=27)
        VGroup(l1, l2).arrange(DOWN, buff=0.35).move_to([0, 0.5, 0])
        basis = T("cytological basis: homologous chromosomes separate at anaphase I of meiosis", size=24, color=th.MUTED).move_to([0, -2.6, 0])
        with self.say("Two laws follow. The law of dominance: in a hybrid only the dominant allele shows, while the recessive stays hidden but unchanged. And the law of segregation, or purity of gametes: the two alleles separate when gametes form, so each gamete gets only one. A gamete is never hybrid. The physical reason is anaphase one of meiosis, when the two homologous chromosomes go to opposite poles."):
            self.play(FadeIn(l1, shift=UP * 0.2))
            self.play(FadeIn(l2, shift=UP * 0.2))
            self.play(FadeIn(basis))
        self.play(FadeOut(VGroup(l1, l2, basis)))
        head, prob = B.example_head(self, "A pure tall pea is crossed with a dwarf. The F₁ are selfed and give 1,200 F₂ plants. (a) How many tall and how many dwarf? (b) How many tall plants breed true? (c) A tall F₂ plant is picked at random: what is the chance it is heterozygous?", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ \tfrac34 \times 1200 = 900 \text{ tall},\quad \tfrac14\times1200 = 300 \text{ dwarf}", size=36),
                       M(r"\text{(b)}\ \ TT = \tfrac14 \times 1200 = 300", size=36),
                       M(r"\text{(c)}\ \ P(Tt \mid \text{tall}) = \frac{600}{900} = \frac{2}{3}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["A worked example. Twelve hundred F two plants.",
                "Part a. Three quarters are tall: nine hundred. One quarter dwarf: three hundred.",
                "Part b. Only T T plants breed true, and they are one quarter of the total: three hundred.",
                "Part c is the trap. Among the nine hundred tall plants, three hundred are T T and six hundred are T t. So the chance a tall plant is heterozygous is six hundred out of nine hundred: two thirds, not one half."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.4)
        self.play(FadeOut(VGroup(head, prob, steps)))

    def p2_test(self):
        head = T("The test cross: making a hidden genotype visible", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        q = VGroup(G.pea(True, TALL), T("TT or Tt?", size=28, color=TALL, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([0, 1.2, 0])
        a = VGroup(T("if TT × tt", size=28, color=th.INK, weight="BOLD"), VGroup(*[G.pea(True, TALL) for _ in range(4)]).arrange(RIGHT, buff=0.35), T("all tall", size=26, color=TALL)).arrange(DOWN, buff=0.2).move_to([-3.3, -1.2, 0])
        b = VGroup(T("if Tt × tt", size=28, color=th.INK, weight="BOLD"), VGroup(G.pea(True, TALL), G.pea(False, DWARF), G.pea(True, TALL), G.pea(False, DWARF)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN), T("1 tall : 1 dwarf", size=26, color=DWARF)).arrange(DOWN, buff=0.2).move_to([3.3, -1.2, 0])
        with self.say("A tall plant could be T T or T t. They look identical. To find out, cross it with the homozygous recessive, a dwarf. That is a test cross. If the plant was T T, every offspring is tall. If it was T t, you get one tall to one dwarf. The offspring ratio is a direct copy of the unknown parent's gametes."):
            self.play(FadeIn(head), FadeIn(q))
            self.play(FadeIn(a, shift=UP * 0.2))
            self.play(FadeIn(b, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, q, a, b)))
        w = self.callout("careful", "Every test cross is a back cross, but not every back cross is a test cross. A back cross uses either parent; a test cross uses only the homozygous recessive.", width=11)
        with self.say("Careful with the words. A back cross is F one crossed with either parent. A test cross must use the homozygous recessive. So every test cross is a back cross, but not the other way round."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(w))

    def p2_di(self):
        head = T("A dihybrid cross", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        p1 = VGroup(G.seed(True, True, 0.32), T("RRYY", size=28, color=th.AMBER, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-4.8, 1.5, 0])
        p2 = VGroup(G.seed(False, False, 0.32), T("rryy", size=28, color=th.MINT, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-2.4, 1.5, 0])
        f1 = VGroup(G.seed(True, True, 0.32), T("F₁: RrYy, round yellow", size=24, color=th.INK, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-3.6, -0.1, 0])
        gam = VGroup(T("F₁ gametes:", size=22, color=th.MUTED), *[T(g_, size=28, color=th.AMBER, weight="BOLD") for g_ in ["RY", "Ry", "rY", "ry"]]).arrange(RIGHT, buff=0.3).move_to([-3.6, -1.5, 0])
        nt = T("4 kinds, equal numbers", size=22, color=th.MUTED).next_to(gam, DOWN, buff=0.15)
        with self.say("Now two characters at once. Round yellow seeds, R R Y Y, crossed with wrinkled green, r r y y. Every F one seed is round and yellow, R r Y y. Here is the key step. Because the R pair separates independently of the Y pair, the F one makes four kinds of gamete, R Y, R y, r Y and r y, in equal numbers."):
            self.play(FadeIn(head), FadeIn(p1), FadeIn(p2))
            self.play(FadeIn(f1, shift=DOWN * 0.2))
            self.play(FadeIn(gam), FadeIn(nt))
        gs = ["RY", "Ry", "rY", "ry"]
        cells = [[a + b for b in gs] for a in gs]
        grid, sq, tx = G.punnett(gs, gs, [["" for _ in gs] for _ in gs], cell=0.78, size=22)
        grid.move_to([2.6, -0.2, 0])
        seeds = {}
        for i, a in enumerate(gs):
            for j, b in enumerate(gs):
                rnd = "R" in (a[0] + b[0])
                yel = "Y" in (a[1] + b[1])
                seeds[(i, j)] = G.seed(rnd, yel, 0.24).move_to(sq[(i, j)])
        with self.say("Four kinds of male gamete meet four kinds of female gamete: sixteen boxes. Fill them in, and draw each seed: round if it has at least one R, yellow if it has at least one Y.") as v:
            self.play(FadeIn(VGroup(*[m for m in grid if m not in tx.values()])))
            per = (v.dur - 1.0) / 16
            for k in sorted(seeds):
                self.play(GrowFromCenter(seeds[k]), run_time=max(0.15, per))
        cls = {"RY": [], "Ry": [], "rY": [], "ry": []}
        for (i, j), s_ in seeds.items():
            a, b = gs[i], gs[j]
            key = ("R" if "R" in a[0] + b[0] else "r") + ("Y" if "Y" in a[1] + b[1] else "y")
            cls[key].append((i, j))
        lab = [("RY", "9 round yellow", th.AMBER), ("Ry", "3 round green", th.MINT), ("rY", "3 wrinkled yellow", "#FFD23F"), ("ry", "1 wrinkled green", "#7BC043")]
        out = VGroup()
        with self.say("Now count. Nine round yellow. Three round green. Three wrinkled yellow. One wrinkled green. Nine to three to three to one, and two brand new combinations, round green and wrinkled yellow, that neither grandparent had.") as v:
            for key, txt, col in lab:
                self.play(*[sq[k].animate.set_fill(col, opacity=0.35) for k in cls[key]], run_time=0.5)
                o = T(txt, size=26, color=col, weight="BOLD")
                out.add(o)
                o.move_to([-3.6, -2.4 - 0.0, 0])
                self.play(FadeIn(o), run_time=0.3)
                self.hold(v.dur * 0.18 - 0.8)
                self.play(FadeOut(o), run_time=0.2)
        res = T("9 : 3 : 3 : 1", size=48, color=th.INK, weight="BOLD").move_to([-3.6, -2.4, 0])
        self.play(FadeOut(VGroup(p1, p2, f1, gam, nt)), Write(res))
        law = self.callout("key", "Law of independent assortment: the members of one allele pair go into gametes independently of another pair, so all combinations appear equally.", width=6.2, size=24)
        law.move_to([-3.4, 0.6, 0])
        with self.say("That is Mendel's third law, independent assortment. And notice: each character alone still gives three to one, twelve round to four wrinkled, twelve yellow to four green. Nine three three one is just three to one, times three to one: the product rule."):
            self.play(FadeIn(law, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, grid, *seeds.values(), res, law)))
        rows = [["heterozygous pairs, n", "gamete kinds", "F₂ phenotypes", "F₂ genotypes", "Punnett boxes"], ["1", "2", "2", "3", "4"], ["2", "4", "4", "9", "16"], ["3", "8", "8", "27", "64"], ["n", "2ⁿ", "2ⁿ", "3ⁿ", "4ⁿ"]]
        tb = B.table(rows, [3.4, 2.2, 2.4, 2.4, 2.4], row_h=0.66, size=24, colors=[th.AMBER, th.INK, th.INK, th.INK, th.INK]).move_to([0, 0.4, 0])
        with self.say("And the pattern generalises. With n heterozygous pairs there are two to the n kinds of gamete, two to the n phenotypes, three to the n genotypes, and four to the n boxes in the square. A trihybrid needs sixty four boxes.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        head, prob = B.example_head(self, "RrYy is selfed and gives 1,600 seeds. Find (a) the number in each phenotypic class, (b) the number of RrYy seeds, (c) the chance that a round yellow seed is RRYY.", size=25)
        steps = VGroup(M(r"\text{(a)}\ \ 900 : 300 : 300 : 100", size=38),
                       M(r"\text{(b)}\ \ P(Rr)\times P(Yy) = \tfrac12\times\tfrac12 = \tfrac14;\ \ \tfrac14\times1600 = 400", size=36),
                       M(r"\text{(c)}\ \ P(RRYY \mid \text{round yellow}) = \frac{1}{9}", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.5).align_to(prob, LEFT)
        says = ["Worked example. Sixteen hundred seeds from a selfed R r Y y plant.",
                "Part a. Sixteen hundred times nine sixteenths, three sixteenths, three sixteenths and one sixteenth: nine hundred, three hundred, three hundred and one hundred.",
                "Part b. Use the product rule. Each gene gives the heterozygote with probability one half, so R r Y y is one quarter: four hundred seeds.",
                "Part c. Round yellow seeds fill nine of the sixteen boxes, and only one of those nine is R R Y Y. So one ninth."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for s_, sy in zip(steps, says[1:]):
            with self.say(sy):
                self.play(Write(s_), run_time=1.4)
        self.play(FadeOut(VGroup(head, prob, steps)))
        self.quiz("The phenotypic ratio of a dihybrid TEST cross (RrYy × rryy) is",
                  ["9 : 3 : 3 : 1", "1 : 1 : 1 : 1", "3 : 1", "1 : 2 : 1"], 1,
                  "Pause and think. A dihybrid crossed with the double recessive. What ratio?",
                  "One to one to one to one. The F one makes four kinds of gamete in equal numbers, and the tester adds only recessive alleles, so each gamete shows itself directly. Nine three three one is the selfed F two, the tempting answer.")

    def p2_chi(self):
        head = T("Is the deviation just chance? The chi-square test", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        f = M(r"\chi^2 = \sum \frac{(O-E)^2}{E}", size=56).move_to([0, 1.6, 0])
        defs = VGroup(T("O = observed count,  E = expected count,  df = classes − 1", size=26, color=th.BODY),
                      T("χ² below the critical value at p = 0.05 → deviation is chance → ratio accepted", size=26, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([0, 0.0, 0])
        crit = B.table([["df", "1", "2", "3", "4", "5"], ["critical χ² (p = 0.05)", "3.841", "5.991", "7.815", "9.488", "11.070"]], [3.8, 1.4, 1.4, 1.4, 1.4, 1.4], row_h=0.6, size=24).move_to([0, -1.7, 0])
        with self.say("Real counts never match a ratio exactly. Is the gap small enough to be chance? The chi square test decides. For each class take observed minus expected, square it, divide by expected, and add them up. Compare with the critical value for your degrees of freedom, the number of classes minus one. If your chi square is less than the critical value, the deviation is just chance and the ratio is accepted."):
            self.play(FadeIn(head), Write(f))
            self.play(FadeIn(defs[0]))
            self.play(FadeIn(defs[1]))
            self.play(FadeIn(crit))
        self.play(FadeOut(VGroup(f, defs, crit)))
        rows = [["class", "O", "E", "O − E", "(O−E)²/E"], ["round yellow", "315", "312.75", "+2.25", "0.016"], ["round green", "108", "104.25", "+3.75", "0.135"],
                ["wrinkled yellow", "101", "104.25", "−3.25", "0.101"], ["wrinkled green", "32", "34.75", "−2.75", "0.218"], ["total", "556", "556", "0", "0.470"]]
        tb = B.table(rows, [3.6, 1.6, 2.0, 1.8, 2.4], row_h=0.58, size=24, colors=[th.MUTED, th.INK, th.SKY, th.INK, th.AMBER]).move_to([0, 0.6, 0])
        with self.say("Mendel's own dihybrid count: three hundred and fifteen, one hundred and eight, one hundred and one, and thirty two, out of five hundred and fifty six. Expected numbers are nine, three, three and one sixteenths of five hundred and fifty six: three hundred and twelve point seven five, one hundred and four point two five twice, and thirty four point seven five. Work each row, and the total chi square is zero point four seven.") as v:
            self.play(FadeOut(head))
            B.reveal_table(self, tb, v.dur * 0.9)
        nl = NumberLine(x_range=[0, 9, 1], length=10, color=th.MUTED, include_numbers=True, font_size=24).move_to([0, -2.4, 0])
        cv = VGroup(Line(nl.n2p(7.815) + DOWN * 0.3, nl.n2p(7.815) + UP * 0.5, color=th.CORAL, stroke_width=5), T("7.815 (df = 3)", size=22, color=th.CORAL).next_to(nl.n2p(7.815) + UP * 0.5, UP, buff=0.05))
        me = VGroup(Dot(nl.n2p(0.47), radius=0.12, color=th.AMBER), T("0.470", size=22, color=th.AMBER).next_to(nl.n2p(0.47) + UP * 0.15, UP, buff=0.05))
        with self.say("Four classes, so three degrees of freedom, and a critical value of seven point eight one five. Zero point four seven is far below it. The deviation is chance, and the data agree with nine three three one."):
            self.play(Create(nl))
            self.play(FadeIn(cv))
            self.play(FadeIn(me, scale=1.5))
            self.sfx("correct", gain=-12)
        self.play(FadeOut(VGroup(tb, nl, cv, me)))
        self.tip("Chi-square uses actual counts, never percentages. E comes from the same total as O.",
                 "Exam tip. Chi square only works with actual counts of individuals, never percentages or fractions. And the expected column must add up to the same total as the observed column.")

    # ------------------------------------------------------------------ part 3: beyond Mendel
    def p3(self):
        self.section(2)
        self.p3_dominance()
        self.p3_abo()
        self.p3_lethal()
        self.p3_sex()
        self.p3_linked()
        self.p3_pedigree()

    def flower(self, col, r=0.45):
        pet = VGroup(*[Ellipse(width=r * 1.1, height=r * 0.6, stroke_width=0, fill_color=col, fill_opacity=1).move_to(polar_(r * 0.5, TAU * k / 5)).rotate(TAU * k / 5) for k in range(5)])
        return VGroup(pet, Dot(radius=r * 0.18, color="#FFE08A"))

    def p3_dominance(self):
        head = T("Incomplete dominance: Mirabilis jalapa", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        RED, PINKC, WHITE_ = "#E63946", "#FF8FB1", "#F1F1F1"
        r = VGroup(self.flower(RED), T("RR", size=26, color=RED, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-4.6, 1.3, 0])
        w = VGroup(self.flower(WHITE_), T("rr", size=26, color=WHITE_, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-2.2, 1.3, 0])
        f1 = VGroup(self.flower(PINKC), T("F₁: Rr, pink", size=26, color=PINKC, weight="BOLD")).arrange(DOWN, buff=0.15).move_to([-3.4, -0.6, 0])
        f2 = VGroup(*[VGroup(self.flower(c_, 0.38), T(t_, size=22, color=c_)).arrange(DOWN, buff=0.1) for c_, t_ in [(RED, "1 RR red"), (PINKC, "2 Rr pink"), (WHITE_, "1 rr white")]]).arrange(RIGHT, buff=0.6).move_to([3.0, 0.4, 0])
        f2h = T("F₂", size=28, color=th.INK, weight="BOLD").next_to(f2, UP, buff=0.3)
        note = para("1 : 2 : 1 — the phenotypic ratio equals the genotypic ratio", width=5.6, size=24, color=th.AMBER).next_to(f2, DOWN, buff=0.4)
        with self.say("Now the cases Mendel never met. In the four o'clock plant, Mirabilis jalapa, red crossed with white gives pink. Neither allele is fully dominant, so the heterozygote is in between. That is incomplete dominance."):
            self.play(FadeIn(head), FadeIn(r), FadeIn(w))
            self.play(FadeIn(f1, shift=DOWN * 0.2))
        with self.say("Self the pinks, and you get one red, two pink, one white. Here the phenotypic ratio is the same as the genotypic ratio, one to two to one, because you can see the heterozygotes."):
            self.play(FadeIn(f2h), LaggedStart(*[FadeIn(f_, shift=UP * 0.2) for f_ in f2], lag_ratio=0.3))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(head, r, w, f1, f2, f2h, note)))
        head = T("Codominance: both alleles show, side by side", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        rng = np.random.default_rng(3)

        def coat(cols, x):
            box = RoundedRectangle(corner_radius=0.3, width=3.0, height=2.0, stroke_color=th.MUTED, stroke_width=2).move_to([x, 0.3, 0])
            hairs = VGroup(*[Line([0, 0, 0], [0.05, 0.28, 0], color=cols[k % len(cols)], stroke_width=3).move_to([x + rng.uniform(-1.3, 1.3), 0.3 + rng.uniform(-0.8, 0.8), 0]) for k in range(140)])
            return VGroup(box, hairs)

        c1, c2, c3 = coat(["#C0392B"], -4.2), coat(["#F1F1F1"], -0.6), coat(["#C0392B", "#F1F1F1"], 3.4)
        l = VGroup(*[T(t_, size=24, color=th.INK).next_to(c_, DOWN, buff=0.2) for t_, c_ in [("red", c1), ("white", c2), ("roan: red AND white hairs", c3)]])
        with self.say("Codominance is different. Both alleles are fully expressed, side by side, with no blending. Cross a red bull with a white cow, and the calf is roan: its coat has red hairs and white hairs mixed together. Not a single pink hair."):
            self.play(FadeIn(head), FadeIn(c1), FadeIn(c2), FadeIn(l[0]), FadeIn(l[1]))
            self.play(FadeIn(c3), FadeIn(l[2]))
        ab = M(r"\text{In people, } I^AI^B \text{ gives blood group AB: both A and B antigens on every red cell.}", size=30, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("The human example is blood group A B. A person with alleles I A and I B carries both the A antigen and the B antigen on every red cell."):
            self.play(FadeIn(ab))
        self.play(FadeOut(VGroup(head, c1, c2, c3, l, ab)))

    def p3_abo(self):
        head = T("Multiple alleles: the ABO blood groups", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        gm = lambda t_: M(t_, size=34, color=th.AMBER)
        rows = [["genotype", "blood group", "antigens on red cells"], [gm(r"I^AI^A \text{ or } I^Ai"), "A", "A"], [gm(r"I^BI^B \text{ or } I^Bi"), "B", "B"], [gm(r"I^AI^B"), "AB", "A and B"], [gm("ii"), "O", "none"]]
        tb = B.table(rows, [3.6, 2.8, 4.2], row_h=0.64, size=26, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 0.2, 0])
        note = M(r"\text{Three alleles; each person carries two. } I^A, I^B \text{ codominant; both dominant over } i", size=30, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("A gene can have more than two alleles in a population, although each person carries only two. The ABO blood group gene has three: I A, I B and little i. I A and I B are codominant with each other, and both are dominant over i. That gives six genotypes and four blood groups.") as v:
            self.play(FadeIn(head))
            B.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(head, tb, note)))
        head, prob = B.example_head(self, "A group O woman has a group B child. She names a group AB man as the father; he points to a group O man. (a) Could the AB man be the father? (b) Could the O man? (c) A heterozygous group A man marries a heterozygous group B woman: chance their first child is group O?", size=25)
        lines = VGroup(M(r"\text{(a) Mother } ii \text{ gives only } i \Rightarrow \text{child } I^Bi;\ I^B \text{ came from the father. } I^AI^B \text{ can give it: \textbf{could be}.}", size=30),
                       M(r"\text{(b) An O man is } ii:\ ii \times ii \to \text{all O} \Rightarrow \text{\textbf{cannot be}.}", size=30),
                       M(r"\text{(c) } I^Ai \times I^Bi \to I^AI^B,\ I^Ai,\ I^Bi,\ ii \Rightarrow P(\text{O}) = \tfrac14 = 25\%", size=30, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        for l_ in lines:
            if l_.width > 12.4:
                l_.scale_to_fit_width(12.4).align_to(prob, LEFT)
        says = ["A worked example on parentage.",
                "Part a. A group O mother is little i little i, and can give only little i. So the group B child must be I B little i, and the I B came from the father. An A B man can give I B. So yes, he could be the father.",
                "Part b. A group O man can give only little i, and two group O parents can only have a group O child. So no, he cannot be the father.",
                "Part c. I A little i times I B little i gives four equally likely children: A B, A, B and O. The chance of group O is one quarter."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob))
        for l_, sy in zip(lines, says[1:]):
            with self.say(sy):
                self.play(FadeIn(l_, shift=RIGHT * 0.2))
        self.play(FadeOut(VGroup(head, prob, lines)))
        self.tip("Blood groups can prove a man CANNOT be the father. They can never prove that he IS: millions share his group.",
                 "Exam tip. A blood group test can exclude a man: it can show he cannot be the father. It can never prove that he is, because millions of other men share his group. Write could be, and cannot be. Never is.")
        self.quiz("A man of blood group AB marries a woman of group O. Which group can NEVER appear among their children?",
                  ["A", "B", "AB", "A and B both"], 2,
                  "Pause and think. Father A B, mother O. Which child's group is impossible?",
                  "A B. The mother can give only little i, so every child gets an i: either I A little i, group A, or I B little i, group B. An A B child would need both I A and I B, and the mother can supply neither. A and B both is the trap: those are exactly the groups that can appear.")

    def p3_lethal(self):
        head = T("Lethal genes", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        grid, sq, tx = G.punnett(["G", "g"], ["G", "g"], [["GG", "Gg"], ["Gg", "gg"]], cell=1.2, size=28)
        grid.move_to([-3.2, 0.0, 0])
        lab = T("Gg × Gg (green, carrying albino)", size=24, color=th.INK).next_to(grid, UP, buff=0.3)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.6, size=26)
        cross = VGroup(Line(sq[(1, 1)].get_corner(UL), sq[(1, 1)].get_corner(DR), color=th.CORAL, stroke_width=6), Line(sq[(1, 1)].get_corner(UR), sq[(1, 1)].get_corner(DL), color=th.CORAL, stroke_width=6))
        with self.say("Some alleles kill. In maize, a recessive allele blocks chlorophyll. Cross two green plants that both carry it, and seedlings come up three green to one white. But the white seedlings cannot photosynthesise. They die as soon as the food in the seed runs out."):
            self.play(FadeIn(head), FadeIn(grid), FadeIn(lab))
            self.play(*[sq[k].animate.set_fill("#5FB04A", opacity=0.45) for k in [(0, 0), (0, 1), (1, 0)]], sq[(1, 1)].animate.set_fill("#F1F1F1", opacity=0.6))
            cap("Seedlings: 3 green : 1 white", sub="The white (gg) seedlings starve once the seed's food is gone.")
            self.play(Create(cross))
        with self.say("So the survivors are one G G to two G g. All green, but two thirds of them are carriers. When the lethal allele is dominant for colour, as in yellow mice, the survivors show a visible two to one ratio: two yellow to one non yellow."):
            cap("Survivors: 1 GG : 2 Gg", color=th.AMBER, sub="All green; 2/3 are carriers. A dominant-colour lethal (yellow mice) gives a visible 2 : 1.")
        self.play(FadeOut(VGroup(head, grid, lab, cross)))
        cap.clear()

    def p3_sex(self):
        head = T("Sex determination", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        kt = VGroup(T("44 + XX", size=34, color=th.PINK, weight="BOLD"), T("44 + XY", size=34, color=th.SKY, weight="BOLD")).arrange(RIGHT, buff=4.2).move_to([0, 1.9, 0])
        kl = VGroup(T("woman: 22 autosome pairs + XX", size=20, color=th.BODY).next_to(kt[0], DOWN, buff=0.15), T("man: 22 autosome pairs + XY", size=20, color=th.BODY).next_to(kt[1], DOWN, buff=0.15))
        with self.say("Sex is decided by one special pair of chromosomes, the sex chromosomes, or allosomes. The rest are autosomes. A woman has forty four autosomes plus X X. A man has forty four plus X Y."):
            self.play(FadeIn(head), FadeIn(kt), FadeIn(kl))
        grid, sq, tx = G.punnett(["X", "X"], ["X", "Y"], [["XX", "XY"], ["XX", "XY"]], cell=1.2, size=30)
        grid.move_to([0.5, -1.0, 0])
        el = T("mother's eggs", size=22, color=th.PINK).next_to(grid, LEFT, buff=0.2)
        sl = T("father's sperm", size=22, color=th.SKY).next_to(grid, UP, buff=0.1)
        with self.say("Now the square. Every egg the mother makes carries an X. She has nothing else to give. The father's sperm are of two kinds: half carry X, half carry Y."):
            self.play(FadeIn(VGroup(*[m for m in grid if m not in tx.values()])), FadeIn(el), FadeIn(sl))
            self.play(*[FadeIn(t_) for t_ in tx.values()])
        with self.say("An X sperm makes a daughter. A Y sperm makes a son. Fifty fifty, and the deciding chromosome comes only from the father. So the mother of three daughters failed at nothing. Blaming her has no biological basis at all."):
            self.play(*[sq[(i, 0)].animate.set_fill(th.PINK, opacity=0.35) for i in range(2)], *[sq[(i, 1)].animate.set_fill(th.SKY, opacity=0.35) for i in range(2)])
            self.play(Indicate(sl, color=th.SKY, scale_factor=1.3))
            nb = B.neby_in(self, "cool", height=1.4)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(kt, kl, grid, el, sl)))
        rows = [["type", "female", "male", "examples"], ["XX–XY", "XX", "XY", "humans, Drosophila, Melandrium"], ["XX–XO", "XX", "XO", "grasshopper, cockroach, Dioscorea"],
                ["ZZ–ZW", "ZW", "ZZ", "birds, butterflies"], ["haplo-diploid", "diploid", "haploid", "honey bee, ant, wasp"]]
        tb = B.table(rows, [2.8, 1.8, 1.8, 5.4], row_h=0.66, size=24, colors=[th.AMBER, th.PINK, th.SKY, th.BODY]).move_to([0, 0.0, 0])
        with self.say("Other animals use other systems. Grasshoppers are X X and X O: the male has a single X and no Y. In birds and butterflies it is reversed: the female is Z W and decides the sex. And in honey bees, fertilised eggs become females and unfertilised eggs become males.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(VGroup(head, tb)))

    def p3_linked(self):
        head = T("Sex-linked inheritance", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        X = RoundedRectangle(corner_radius=0.2, width=0.42, height=2.6, stroke_width=0, fill_color=th.PINK, fill_opacity=0.85).move_to([-4.2, 0.2, 0])
        Y = RoundedRectangle(corner_radius=0.2, width=0.42, height=1.1, stroke_width=0, fill_color=th.SKY, fill_opacity=0.85).move_to([-3.4, 0.95, 0])
        gene = Rectangle(width=0.42, height=0.14, stroke_width=0, fill_color=th.AMBER, fill_opacity=1).move_to([-4.2, -0.4, 0])
        gl = T("c", size=26, color=th.AMBER, weight="BOLD").next_to(gene, LEFT, buff=0.15)
        nothing = T("no partner here", size=22, color=th.MUTED).move_to([-2.3, -0.4, 0])
        cap = B.Captions(self, at=(2.7, 0.3, 0), width=6.4, size=26)
        with self.say("Most genes on the X chromosome have no partner on the much smaller Y. So a man has only one copy of each X linked gene: he is hemizygous. A single recessive allele on his one X is enough to show. That is why red green colour blindness and haemophilia are far commoner in men."):
            self.play(FadeIn(head), FadeIn(X), FadeIn(Y))
            self.play(FadeIn(gene), FadeIn(gl), FadeIn(nothing))
            cap("Hemizygous male", color=th.AMBER, sub="One X, so one recessive allele is enough: colour blindness, haemophilia.")
        with self.say("The pattern is called criss cross inheritance. An affected father passes the allele to all his daughters, who become carriers, and to none of his sons. A carrier mother passes it to half her sons, who are affected."):
            cap("Criss-cross inheritance", sub="Affected father → all daughters carriers, no sons. Carrier mother → half her sons affected.")
        self.play(FadeOut(VGroup(head, X, Y, gene, gl, nothing)))
        cap.clear()
        head, prob = B.example_head(self, "A woman with normal vision, whose father was colour blind, marries a man with normal vision. Find her genotype, the chance that a child is colour blind, and the chance that a son is.", size=25)
        grid, sq, tx = G.punnett(["$X^C$", "$X^c$"], ["$X^C$", "$Y$"], [["$X^CX^C$", "$X^CY$"], ["$X^CX^c$", "$X^cY$"]], cell=1.25, size=24)
        grid.scale(0.95).move_to([-3.2, -1.25, 0])
        key = M(r"X^C = \text{normal allele},\quad X^c = \text{colour-blind allele}", size=30, color=th.MUTED).move_to([2.6, -0.1, 0])
        res = VGroup(T("normal girl · normal boy", size=24, color=th.MINT), T("carrier girl · colour-blind boy", size=24, color=th.CORAL),
                     M(r"P(\text{child}) = \tfrac14,\qquad P(\text{son}) = \tfrac12", size=38, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -1.6, 0])
        with self.say("A worked example. Her father was colour blind, so he was X small c Y. A father gives his only X to every daughter, so she got the colour blind X from him and a normal X from her mother. She is a carrier. Her husband is a normal X Y."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(FadeIn(key))
            self.play(FadeIn(grid))
        with self.say("Fill in the square. A normal girl, a normal boy, a carrier girl, and a colour blind boy. So one child in four is colour blind. But among sons only, it is one in two. Every daughter sees normally, though half are carriers."):
            self.play(sq[(1, 1)].animate.set_fill(th.CORAL, opacity=0.45), sq[(1, 0)].animate.set_fill(th.AMBER, opacity=0.3))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in res], lag_ratio=0.4))
        self.play(FadeOut(VGroup(head, prob, grid, key, res)))

    def p3_pedigree(self):
        head = T("Reading a pedigree", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        I1, I2 = G.person(True).move_to([-4.6, 1.6, 0]), G.person(False).move_to([-3.0, 1.6, 0])
        II1, II2, II3, II4 = G.person(True).move_to([-5.0, 0.0, 0]), G.person(False, affected=True).move_to([-3.8, 0.0, 0]), G.person(True).move_to([-2.6, 0.0, 0]), G.person(False).move_to([-1.2, 0.0, 0])
        III1 = G.person(True, affected=True).move_to([-1.9, -1.6, 0])

        def couple(a, b, kids):
            bar = Line(a.get_right(), b.get_left(), color=th.MUTED, stroke_width=3)
            mid = bar.get_center()
            y = (mid[1] + kids[0].get_top()[1]) / 2
            g = VGroup(bar, Line(mid, [mid[0], y, 0], color=th.MUTED, stroke_width=3))
            xs = [k.get_center()[0] for k in kids]
            g.add(Line([min(xs + [mid[0]]), y, 0], [max(xs + [mid[0]]), y, 0], color=th.MUTED, stroke_width=3))
            for k in kids:
                g.add(Line([k.get_center()[0], y, 0], k.get_top(), color=th.MUTED, stroke_width=3))
            return g

        lines = VGroup(couple(I1, I2, [II1, II2, II3]), couple(II3, II4, [III1]))
        gens = VGroup(*[T(s_, size=24, color=th.MUTED).move_to([-6.3, y, 0]) for s_, y in [("I", 1.6), ("II", 0.0), ("III", -1.6)]])
        leg = VGroup(VGroup(G.person(True, s=0.35), T("male", size=20, color=th.BODY)).arrange(RIGHT, buff=0.15), VGroup(G.person(False, s=0.35), T("female", size=20, color=th.BODY)).arrange(RIGHT, buff=0.15),
                     VGroup(G.person(True, affected=True, s=0.35), T("affected", size=20, color=th.BODY)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.5).move_to([-3.2, -2.75, 0])
        rules = VGroup(*[para(s_, width=5.6, size=22, color=th.INK) for s_ in ["1. In every generation → suspect dominant; skips one → suspect recessive.", "2. Two unaffected parents with an affected child → certainly recessive.",
                                                                               "3. Both sexes equally → autosomal; mostly males → suspect X-linked.", "4. Affected father → every daughter, no son → X-linked."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 0.1, 0])
        with self.say("In people we cannot arrange crosses, so we read family trees. A pedigree uses squares for males, circles for females, and shades the affected. Read it with four questions, in order.") as v:
            self.play(FadeIn(head), FadeIn(leg))
            self.play(FadeIn(VGroup(I1, I2, II1, II2, II3, II4, III1, lines, gens)))
            for r_ in rules:
                self.play(FadeIn(r_, shift=LEFT * 0.2), run_time=0.4)
        sol = VGroup(para("Unaffected I-1 × I-2 have an affected daughter → recessive.", width=5.6, size=22, color=th.AMBER),
                     para("An X-linked recessive daughter needs an affected father; hers is normal → autosomal recessive.", width=5.6, size=22, color=th.AMBER),
                     para("So I-1 and I-2 are both Aa. II-3 gave 'a' to III-1, so he is Aa; II-4 must be Aa too.", width=5.6, size=22, color=th.AMBER),
                     M(r"Aa \times Aa:\ P(\text{affected}) = \tfrac14", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.2, 0])
        with self.say("Try this family. An unaffected couple in generation one has an affected daughter. A trait missing in both parents but present in the child must be recessive. Could it be X linked? No: an X linked recessive daughter needs an affected father, and hers is normal. So it is autosomal recessive."):
            self.play(FadeOut(rules), Indicate(II2, color=th.CORAL))
            self.play(FadeIn(sol[0]))
            self.play(FadeIn(sol[1]))
        with self.say("Both grandparents must be A a. Their son in generation two had an affected son, so he passed on a small a: he is A a, and so is his unaffected wife. Another child of theirs is affected with a probability of one quarter."):
            self.play(FadeIn(sol[2]))
            self.play(Write(sol[3]))
        self.play(FadeOut(VGroup(head, leg, I1, I2, II1, II2, II3, II4, III1, lines, gens, sol)))

    # ------------------------------------------------------------------ part 4: linkage
    def p4(self):
        self.section(3)
        self.p4_bateson()
        self.p4_cross()
        self.p4_map()

    def p4_bateson(self):
        head = T("Bateson and Punnett, 1906: sweet pea", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cls = [("purple long", 284, 214.3), ("purple round", 21, 71.4), ("red long", 21, 71.4), ("red round", 55, 23.8)]
        ax = VGroup()
        base = -2.2
        for i, (n_, o, e) in enumerate(cls):
            x = -4.5 + i * 2.6
            eb = Rectangle(width=0.7, height=e * 0.016, stroke_color=th.MUTED, stroke_width=2, fill_opacity=0).move_to([x - 0.4, base + e * 0.008, 0])
            ob = Rectangle(width=0.7, height=o * 0.016, stroke_width=0, fill_color=th.AMBER if i in (0, 3) else th.SKY, fill_opacity=0.9).move_to([x + 0.4, base + o * 0.008, 0])
            ax.add(VGroup(eb, ob, T(n_, size=22, color=th.INK).move_to([x, base - 0.35, 0]), T(str(o), size=22, color=th.AMBER if i in (0, 3) else th.SKY).next_to(ob, UP, buff=0.08)))
        leg = VGroup(VGroup(Rectangle(width=0.4, height=0.25, stroke_color=th.MUTED, stroke_width=2), T("expected from 9:3:3:1", size=22, color=th.MUTED)).arrange(RIGHT, buff=0.15),
                     VGroup(Rectangle(width=0.4, height=0.25, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.9), T("observed", size=22, color=th.INK)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).move_to([0, 2.4, 0])
        with self.say("Independent assortment has a catch. In nineteen oh six Bateson and Punnett crossed sweet peas, purple with long pollen against red with round pollen. The F two should have been nine three three one. It was not. The two parental combinations were far too common, and the two new combinations far too rare."):
            self.play(FadeIn(head), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(a_[0]) for a_ in ax], lag_ratio=0.1), LaggedStart(*[FadeIn(a_[2]) for a_ in ax], lag_ratio=0.1))
            self.play(LaggedStart(*[GrowFromEdge(a_[1], DOWN) for a_ in ax], lag_ratio=0.15), LaggedStart(*[FadeIn(a_[3]) for a_ in ax], lag_ratio=0.15))
        with self.say("They called it coupling and repulsion. Alleles that entered the cross together tended to stay together. In nineteen ten Thomas Hunt Morgan, working with fruit flies, gave the real explanation: those genes sit on the same chromosome. He called it linkage."):
            self.play(Indicate(VGroup(ax[0], ax[3]), color=th.AMBER))
        self.play(FadeOut(VGroup(head, ax, leg)))
        d = self.callout("key", "Linkage: the tendency of genes on the same chromosome to be inherited together. All the genes on one chromosome form a linkage group; the number of linkage groups = the haploid chromosome number.", width=11, size=27)
        d.move_to([0, 1.3, 0])
        rows = [["organism", "2n", "linkage groups"], ["Pisum sativum", "14", "7"], ["Zea mays", "20", "10"], ["Drosophila", "8", "4"], ["Homo sapiens", "46", "23"]]
        tb = B.table(rows, [3.6, 1.6, 2.8], row_h=0.5, size=23, colors=[th.INK, th.MUTED, th.AMBER]).move_to([0, -1.6, 0])
        with self.say("Linkage is the tendency of genes on the same chromosome to travel together. All the genes on one chromosome make a linkage group, so a species has as many linkage groups as its haploid chromosome number. Pea, seven. Maize, ten. Fruit fly, four. Humans, twenty three."):
            self.play(FadeIn(d, shift=UP * 0.2))
            self.play(FadeIn(tb))
        self.play(FadeOut(VGroup(d, tb)))
        cm = self.callout("remember", "Complete linkage (no new combinations) is rare: male Drosophila and female silkworm, where crossing over does not happen. Most linkage is incomplete: crossing over separates the genes now and then.", width=11, size=26)
        with self.say("Linkage is rarely complete. Only in male fruit flies and female silkworms does crossing over never happen. Everywhere else linkage is incomplete: now and then, the genes are separated. By what? Crossing over."):
            self.play(FadeIn(cm, shift=UP * 0.2))
        self.play(FadeOut(cm))

    def p4_cross(self):
        head = T("Crossing over at pachytene", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        A1, A2 = "#4CC9F0", "#3AA8D0"
        B1, B2 = "#FF8FB1", "#E46F94"
        xs = [-1.2, -0.6, 0.6, 1.2]
        cols = [A1, A2, B1, B2]
        labs = [("A", "B"), ("A", "B"), ("a", "b"), ("a", "b")]
        chs = VGroup()
        for x, c_, (g1, g2) in zip(xs, cols, labs):
            body = RoundedRectangle(corner_radius=0.17, width=0.34, height=3.6, stroke_width=0, fill_color=c_, fill_opacity=0.9).move_to([x, 0.0, 0])
            m1 = T(g1, size=26, color=th.INK, weight="BOLD").move_to([x, 1.2, 0])
            m2 = T(g2, size=26, color=th.INK, weight="BOLD").move_to([x, -1.2, 0])
            chs.add(VGroup(body, m1, m2))
        cen = VGroup(Dot([-0.9, 0.4, 0], radius=0.1, color=th.INK), Dot([0.9, 0.4, 0], radius=0.1, color=th.INK))
        ll = VGroup(T("homologue 1", size=22, color=A1).move_to([-2.9, 1.8, 0]), T("homologue 2", size=22, color=B1).move_to([2.9, 1.8, 0]))
        cap = B.Captions(self, at=(0, -2.75, 0), width=12, size=24)
        with self.say("Here is a pair of homologous chromosomes in meiosis, paired up as a bivalent. Each has already copied itself, so there are four chromatids: a tetrad. One homologue carries A and B, the other a and b."):
            self.play(FadeIn(head), FadeIn(chs), FadeIn(cen), FadeIn(ll))
            cap("Synapsis (zygotene) → bivalent of four chromatids (a tetrad)")
        cut_y = -0.4
        ch2, ch3 = chs[1], chs[2]
        lo2 = VGroup(Rectangle(width=0.34, height=1.4, stroke_width=0, fill_color=A2, fill_opacity=0.9).move_to([-0.6, cut_y - 0.7 - 0.0, 0]), T("B", size=26, color=th.INK, weight="BOLD").move_to([-0.6, -1.2, 0]))
        lo3 = VGroup(Rectangle(width=0.34, height=1.4, stroke_width=0, fill_color=B1, fill_opacity=0.9).move_to([0.6, cut_y - 0.7, 0]), T("b", size=26, color=th.INK, weight="BOLD").move_to([0.6, -1.2, 0]))
        x_ = VGroup(Line([-0.75, cut_y + 0.25, 0], [0.75, cut_y - 0.25, 0], color=WHITE, stroke_width=5), Line([-0.75, cut_y - 0.25, 0], [0.75, cut_y + 0.25, 0], color=WHITE, stroke_width=5))
        with self.say("At pachytene, two non sister chromatids, one from each homologue, break at exactly corresponding points. The crossing point is a chiasma."):
            self.play(Create(x_))
            self.sfx("click", gain=-10)
            cap("Two NON-SISTER chromatids break at the same point: a chiasma (pachytene)", color=th.AMBER)
        with self.say("The broken ends rejoin the other way round, sealed by endonuclease and ligase. Now one chromatid carries A with small b, and another carries small a with B. Brand new combinations."):
            self.remove(ch2[2], ch3[2])
            self.add(lo2, lo3)
            self.play(lo2.animate.shift(RIGHT * 1.2), lo3.animate.shift(LEFT * 1.2), run_time=1.4, path_arc=0.8)
            self.play(FadeOut(x_))
            cap("Reunion: segments exchanged → recombinant chromatids Ab and aB", color=th.MINT)
        gam = VGroup(*[VGroup(T(g_, size=30, color=c_, weight="BOLD"), T(k_, size=20, color=th.MUTED)).arrange(DOWN, buff=0.08) for g_, c_, k_ in
                       [("AB", A1, "parental"), ("Ab", th.MINT, "recombinant"), ("aB", th.MINT, "recombinant"), ("ab", B1, "parental")]]).arrange(RIGHT, buff=0.8).move_to([0, -2.0, 0])
        with self.say("Meiosis then hands one chromatid to each of four gametes: two parental types, A B and a b, and two recombinants, A small b and small a B. The chiasma itself is the visible mark of a crossover that has already happened: Janssens' chiasmatype theory. The chiasmata then slide to the ends in diplotene and diakinesis: terminalisation."):
            cap.clear()
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in gam], lag_ratio=0.25))
        self.play(FadeOut(VGroup(head, chs, cen, ll, lo2, lo3, gam)))
        f = VGroup(*[T(s_, size=25, color=th.INK) for s_ in ["distance between the genes: the main factor", "sex: none in male Drosophila; usually higher in females", "age: falls in older organisms",
                                                             "temperature: raised by very high or low", "X-rays and some chemicals: raise it", "next to the centromere: rare"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -0.1, 0])
        h2 = T("What changes the crossover frequency?", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("What controls how often crossing over happens? Above all, distance: the farther apart two genes are, the more likely a chiasma falls between them. Also sex, age, temperature, radiation and chemicals, and nearness to the centromere, where it is rare.") as v:
            self.play(FadeIn(h2))
            for r_ in f:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.12)
        self.play(FadeOut(VGroup(h2, f)))

    def p4_map(self):
        head = T("Gene mapping", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        f = M(r"\text{RF} = \frac{\text{recombinants}}{\text{total offspring}} \times 100\%", size=46).move_to([0, 1.8, 0])
        unit = T("1% recombination = 1 map unit = 1 centiMorgan (cM)   ·   Sturtevant, 1913", size=24, color=th.AMBER).next_to(f, DOWN, buff=0.35)
        line = Line([-5, -1.0, 0], [5, -1.0, 0], color=th.SKY, stroke_width=10)
        genes = [("y", -4.0), ("w", -3.4), ("v", 1.2), ("m", 3.0)]
        gm = VGroup(*[VGroup(Line([x, -1.25, 0], [x, -0.75, 0], color=th.INK, stroke_width=4), T(g_, size=28, color=th.INK, weight="BOLD").move_to([x, -0.45, 0])) for g_, x in genes])
        dist = VGroup(*[VGroup(DoubleArrow([a, -1.6, 0], [b, -1.6, 0], buff=0, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.1), T(t_, size=20, color=th.MUTED).move_to([(a + b) / 2, -1.95, 0]))
                        for a, b, t_ in [(-4.0, -3.4, "close: rarely separated"), (1.2, 3.0, "farther: separated more often")]])
        with self.say("Because a crossover is more likely between genes that are far apart, the recombination frequency measures distance. It is the recombinant offspring divided by the total, times a hundred. Sturtevant, in nineteen thirteen, made one percent recombination equal one map unit, one centimorgan, and drew the first genetic map, showing that genes lie in a line."):
            self.play(FadeIn(head), Write(f))
            self.play(FadeIn(unit))
            self.play(Create(line), LaggedStart(*[FadeIn(g_) for g_ in gm], lag_ratio=0.2))
            self.play(FadeIn(dist))
        cap = para("The largest recombination frequency you can observe is 50%: the same as independent assortment. Genes more than 50 cM apart look unlinked.", width=11.5, size=24, color=th.BODY).move_to([0, -2.8, 0])
        with self.say("One limit. The highest recombination frequency you can ever observe is fifty percent, which is exactly what unlinked genes give. So genes more than fifty map units apart on the same chromosome look as if they were unlinked."):
            self.play(FadeIn(cap))
        self.play(FadeOut(VGroup(head, f, unit, line, gm, dist, cap)))
        head, prob = B.example_head(self, "Maize: coloured (C) over colourless (c), full (Sh) over shrunken (sh). A double heterozygote test-crossed with c sh / c sh gave: coloured full 4032, coloured shrunken 149, colourless full 152, colourless shrunken 4035. Linked? RF? Parent's arrangement?", size=24)
        bars = VGroup()
        data = [("coloured full", 4032, th.AMBER), ("coloured shrunken", 149, th.MINT), ("colourless full", 152, th.MINT), ("colourless shrunken", 4035, th.AMBER)]
        for i, (n_, v, c_) in enumerate(data):
            r = Rectangle(width=v / 4035 * 4.6, height=0.38, stroke_width=0, fill_color=c_, fill_opacity=0.9)
            r.height = 0.3
            r.move_to([-5.9 + r.width / 2 + 3.0, 0.55 - i * 0.4, 0])
            bars.add(VGroup(r, T(n_, size=20, color=th.INK).next_to([-2.9, 0.55 - i * 0.4, 0], LEFT, buff=0.15), T(str(v), size=20, color=c_).next_to(r, RIGHT, buff=0.12)))
        steps = VGroup(T("Unlinked would be 1:1:1:1. Two huge + two tiny classes → linked.", size=23, color=th.INK),
                       M(r"\text{RF} = \frac{149+152}{4032+149+152+4035}\times100 = \frac{301}{8368}\times 100 = 3.6\%", size=34, color=th.AMBER),
                       M(r"\Rightarrow 3.6 \text{ cM apart;\ \ parent in coupling: } C\,Sh / c\,sh", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(bars, DOWN, buff=0.3).align_to(prob, LEFT)
        if steps.get_bottom()[1] < -3.25:
            steps.scale((steps.get_top()[1] + 3.25) / steps.height, about_edge=UP)
        with self.say("A worked example from maize. A double heterozygote is test crossed, and gives four classes: four thousand and thirty two, one hundred and forty nine, one hundred and fifty two, and four thousand and thirty five."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.2))
        with self.say("If the genes were unlinked, a test cross would give one to one to one to one. Two huge classes and two tiny ones mean the genes are linked."):
            self.play(FadeIn(steps[0]))
        with self.say("The tiny classes are the recombinants: one hundred and forty nine plus one hundred and fifty two, three hundred and one, out of eight thousand three hundred and sixty eight. That is three point six percent. So the genes are three point six map units apart."):
            self.play(Write(steps[1]))
        with self.say("And the big classes show which alleles travelled together: C with full, and small c with shrunken. The parent was in coupling, C S h over small c small s h."):
            self.play(Write(steps[2]))
        self.play(FadeOut(VGroup(head, prob, bars, steps)))
        self.tip("Recombinants are the RARE classes, whatever they look like — not the recessive ones.",
                 "Exam tip. In a linkage test cross, find the recombinants by their numbers, not their appearance. The two smallest classes are always the recombinants.")
        self.quiz("In a test cross of a double heterozygote, 96 of 1600 offspring were recombinants. The map distance between the genes is",
                  ["0.6 cM", "6 cM", "9.6 cM", "60 cM"], 1,
                  "Pause and think. Ninety six recombinants out of sixteen hundred. How far apart are the genes?",
                  "Six centimorgans. Ninety six divided by sixteen hundred is zero point zero six, times a hundred is six percent, and one percent recombination is one map unit. Zero point six comes from forgetting a factor of ten.")
        rows = [["", "linkage", "crossing over"], ["effect", "keeps linked genes together", "separates linked genes"], ["result", "parental combinations", "recombinants"],
                ["with distance", "weaker", "more frequent"], ["value", "keeps good combinations", "creates variation"]]
        tb = B.table(rows, [2.8, 4.6, 4.6], row_h=0.66, size=24, colors=[th.MUTED, th.SKY, th.MINT]).move_to([0, 0.2, 0])
        with self.say("The comparison to learn. Linkage keeps genes together and gives parental combinations; it weakens with distance; it keeps good combinations intact. Crossing over separates them and gives recombinants; it becomes more frequent with distance; and it creates variation.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("Crossing over takes place during",
                  ["leptotene", "zygotene", "pachytene", "diplotene"], 2,
                  "One more. In which stage of prophase one does crossing over happen?",
                  "Pachytene. Zygotene is when the homologues pair, which is the tempting answer, and diplotene is when the chiasmata become visible as the homologues start to separate.")

    # ------------------------------------------------------------------ part 5: mutation and polyploidy
    def p5(self):
        self.section(4)
        self.p5_point()
        self.p5_chromo()
        self.p5_poly()

    def codon_row(self, seq, y, x0=-5.0):
        cods = [seq[i:i + 3] for i in range(0, len(seq) - len(seq) % 3, 3)]
        g = VGroup()
        for k, c_ in enumerate(cods):
            box = VGroup(*[G.base_chip(b, 0.42, 0.42, 20) for b in c_]).arrange(RIGHT, buff=0.03)
            aa = G.CODON.get(c_, "?")
            t_ = T(aa, size=22, color=th.CORAL if aa == "stop" else th.INK, weight="BOLD").next_to(box, DOWN, buff=0.1)
            g.add(VGroup(box, t_))
        g.arrange(RIGHT, buff=0.3).move_to([0, y, 0])
        return g

    def p5_point(self):
        head = T("Mutation", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        d = self.callout("key", "A mutation is a sudden, random, heritable change in the genetic material, not caused by segregation or recombination. Hugo de Vries (1901), from Oenothera lamarckiana.", width=11, size=27).move_to([0, 1.1, 0])
        props = para("sudden · random · heritable (in germ cells) · recurrent · usually recessive and harmful · rare: 1 in 10⁵–10⁶ gametes", width=11.5, size=22, color=th.BODY, align="center").move_to([0, -0.9, 0])
        cls = T("somatic or germinal · spontaneous or induced · gene (point) or chromosomal", size=24, color=th.AMBER).move_to([0, -1.9, 0])
        with self.say("Finally, what happens when the message itself changes. A mutation is a sudden, random, heritable change in the genetic material, not caused by segregation or recombination. Hugo de Vries coined the word in nineteen oh one, from the evening primrose. Mutations are usually recessive and usually harmful, because a random change to a finely tuned system is more likely to break it than to improve it. And they are rare."):
            self.play(FadeIn(head), FadeIn(d, shift=UP * 0.2))
            self.play(FadeIn(props))
            self.play(FadeIn(cls))
        self.play(FadeOut(VGroup(d, props, cls)))
        orig = "AUGGAGUGGAAAUAA"
        r0 = self.codon_row(orig, 1.6)
        l0 = T("original", size=22, color=th.MUTED).next_to(r0, LEFT, buff=0.3)
        cap = B.Captions(self, at=(0, -2.75, 0), width=12, size=24)
        with self.say("Point mutations change one or a few bases. Here is a stretch of messenger RNA, read as codons: methionine, glutamic acid, tryptophan, lysine, stop."):
            self.play(FadeIn(r0), FadeIn(l0))
        rows = [("AUGGAAUGGAAAUAA", "silent: GAG → GAA, still Glu (the code is degenerate)", th.MINT),
                ("AUGGUGUGGAAAUAA", "missense: GAG → GUG, Glu → Val (sickle-cell anaemia)", th.AMBER),
                ("AUGGAGUGAAAAUAA", "nonsense: UGG → UGA, a stop codon: the chain is cut short", th.CORAL)]
        says = ["A substitution swaps one base. If the new codon still means the same amino acid, the mutation is silent. G A G to G A A is still glutamic acid, because the code is degenerate.",
                "If it means a different amino acid, it is missense. G A G to G U G puts valine in place of glutamic acid. This exact change, at the sixth amino acid of the beta chain of haemoglobin, causes sickle cell anaemia.",
                "And if it creates a stop codon, it is nonsense: the protein is cut short. A purine for a purine, or pyrimidine for pyrimidine, is a transition; a purine for a pyrimidine is a transversion."]
        shown = VGroup()
        for (sq_, cap_, col), sy in zip(rows, says):
            r_ = self.codon_row(sq_, 0.0)
            with self.say(sy):
                self.play(FadeOut(shown), FadeIn(r_))
                diffs = [i for i, (a, b) in enumerate(zip(orig, sq_)) if a != b]
                for i in diffs:
                    k, j = divmod(i, 3)
                    self.play(Indicate(r_[k][0][j], color=col, scale_factor=1.4))
                cap(cap_, color=col)
            shown = r_
        self.play(FadeOut(shown))
        ins = "AUGGAGCUGGAAAUAA"
        r1 = self.codon_row(ins[:15], 0.0)
        with self.say("Now insert a single base. Every codon after it is read in the wrong frame. Glutamic acid, then leucine, glutamic acid, isoleucine: garbage, all the way to the end. That is a frameshift, from inserting or deleting bases in any number that is not a multiple of three, and it is far more damaging than a substitution."):
            self.play(FadeIn(r1))
            self.play(Indicate(r1[2][0][0], color=th.CORAL, scale_factor=1.5))
            self.play(*[Indicate(r1[k], color=th.CORAL, scale_factor=1.05) for k in range(2, 5)])
            cap("frameshift: insertion or deletion of a number of bases that is not a multiple of 3", color=th.CORAL)
        self.play(FadeOut(VGroup(head, r0, l0, r1)))
        cap.clear()

    def p5_chromo(self):
        head = T("Chromosomal mutations", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = list("ABCDEFG")
        cols = [th.SKY] * 7
        base = G.chrom_bar(L, -5.2, 2.0, colors=cols)
        lab0 = T("normal", size=22, color=th.MUTED).next_to(base, RIGHT, buff=0.3)
        rows = [("deletion", list("ABEFG"), "a segment lost (C D)", th.CORAL), ("duplication", list("ABCDCDEFG"), "a segment repeated", th.MINT),
                ("inversion", list("ABEDCFG"), "a segment turned round (C D E)", th.AMBER), ("translocation", list("ABCDEXY"), "a segment moved to a non-homologous chromosome", th.PINK)]
        shown = VGroup()
        with self.say("Larger changes alter the structure of whole chromosomes. Take a chromosome with segments A to G. A deletion loses a piece. A duplication repeats a piece. An inversion turns a piece end to end. And a translocation moves a piece onto a different, non homologous chromosome.") as v:
            self.play(FadeIn(head), FadeIn(base), FadeIn(lab0))
            for i, (n_, segs, d_, c_) in enumerate(rows):
                bar = G.chrom_bar(segs, -5.2, 1.0 - i * 0.95, colors=[c_ if s_ in "XY" else th.SKY for s_ in segs])
                lt = VGroup(T(n_, size=24, color=c_, weight="BOLD"), T(d_, size=20, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.6, 1.0 - i * 0.95, 0])
                self.play(FadeIn(bar, shift=RIGHT * 0.2), FadeIn(lt), run_time=0.6)
                shown.add(bar, lt)
                self.hold(v.dur * 0.2 - 0.6)
        self.play(FadeOut(VGroup(base, lab0, shown)))
        hh = VGroup(*[RoundedRectangle(corner_radius=0.12, width=0.24, height=1.2, stroke_width=0, fill_color=c_, fill_opacity=0.9) for c_ in (th.SKY, th.PINK)]).arrange(RIGHT, buff=0.2).move_to([-3.0, 0.6, 0])
        cell = Circle(radius=1.3, stroke_color=th.MUTED, stroke_width=3).move_to([-3.0, 0.6, 0])
        g1 = Circle(radius=0.7, stroke_color=th.MUTED, stroke_width=3).move_to([-4.6, -1.7, 0])
        g2 = Circle(radius=0.7, stroke_color=th.MUTED, stroke_width=3).move_to([-1.4, -1.7, 0])
        l1 = T("n + 1", size=26, color=th.CORAL, weight="BOLD").next_to(g1, DOWN, buff=0.1)
        l2 = T("n − 1", size=26, color=th.CORAL, weight="BOLD").next_to(g2, DOWN, buff=0.1)
        rows = [["aneuploid", "formula", "human example"], ["monosomy", "2n − 1", "Turner's syndrome, 45, XO"], ["trisomy", "2n + 1", "Down's (47, +21); Klinefelter's (47, XXY)"], ["nullisomy", "2n − 2", "lethal in humans"]]
        tb = B.table(rows, [2.0, 1.4, 4.4], row_h=0.62, size=21, colors=[th.AMBER, th.INK, th.BODY]).move_to([2.8, 0.0, 0])
        with self.say("Changes in number come in two kinds. Euploidy changes whole sets. Aneuploidy changes one or a few chromosomes, and it starts with non disjunction: a pair fails to separate at anaphase, so one gamete gets an extra chromosome and the other gets none."):
            self.play(Create(cell), FadeIn(hh))
            self.play(hh.animate.move_to(g1), Create(g1), Create(g2), run_time=1.2)
            self.play(FadeIn(l1), FadeIn(l2))
        with self.say("Fertilise them, and you get monosomy, two n minus one, as in Turner's syndrome, or trisomy, two n plus one, as in Down's syndrome, trisomy twenty one, or Klinefelter's, X X Y.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(head, cell, hh, g1, g2, l1, l2, tb)))
        mut = VGroup(VGroup(T("physical", size=26, color=th.SKY, weight="BOLD"), para("X-rays, gamma rays, UV (thymine dimers), heat", width=3.6, size=21, color=th.BODY)).arrange(DOWN, buff=0.15),
                     VGroup(T("chemical", size=26, color=th.AMBER, weight="BOLD"), para("mustard gas, nitrous acid, EMS, 5-bromouracil, acridines, colchicine", width=3.6, size=21, color=th.BODY)).arrange(DOWN, buff=0.15),
                     VGroup(T("biological", size=26, color=th.MINT, weight="BOLD"), para("transposons, some viruses", width=3.6, size=21, color=th.BODY)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 0.6, 0])
        why = para("Mutation is the only original source of new alleles. Recombination only reshuffles them. Mutation breeding with gamma rays or EMS has given short-strawed, early and disease-resistant rice, wheat and barley.", width=11.5, size=24, color=th.AMBER).move_to([0, -1.9, 0])
        h2 = T("Mutagens, and why mutation matters", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Agents that raise the mutation rate are mutagens: physical ones like X rays and ultraviolet, chemical ones like mustard gas, nitrous acid and E M S, and biological ones like transposons. And here is why mutation matters: it is the only original source of new alleles. Crossing over only reshuffles what already exists. Without mutation there is nothing for natural selection to work on, and no evolution."):
            self.play(FadeIn(h2), LaggedStart(*[FadeIn(m_, shift=UP * 0.2) for m_ in mut], lag_ratio=0.3))
            self.play(FadeIn(why))
        self.play(FadeOut(VGroup(h2, mut, why)))

    def p5_poly(self):
        head = T("Polyploidy", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)

        def sets(cols, x, y):
            g = VGroup()
            for k, c_ in enumerate(cols):
                g.add(VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.13, height=h_, stroke_width=0, fill_color=c_, fill_opacity=0.9) for h_ in (0.8, 0.6, 0.45)]).arrange(RIGHT, buff=0.06))
            g.arrange(RIGHT, buff=0.22).move_to([x, y, 0])
            return g

        c2 = sets([th.SKY, th.SKY], -4.0, 1.4)
        c4 = sets([th.SKY] * 4, -4.0, 0.0)
        a2 = sets([th.SKY, th.PINK], 2.6, 1.4)
        a4 = sets([th.SKY, th.SKY, th.PINK, th.PINK], 2.6, 0.0)
        la = VGroup(T("autopolyploid: AA → AAAA", size=26, color=th.SKY, weight="BOLD").next_to(c4, DOWN, buff=0.3), T("allopolyploid: AB → AABB", size=26, color=th.PINK, weight="BOLD").next_to(a4, DOWN, buff=0.3))
        ex = VGroup(para("potato (4x = 48), triploid banana and seedless watermelon", width=4.6, size=22, color=th.BODY).next_to(la[0], DOWN, buff=0.15),
                    para("bread wheat (6x = 42), cotton, tobacco, Triticale, Raphanobrassica", width=4.6, size=22, color=th.BODY).next_to(la[1], DOWN, buff=0.15))
        with self.say("Polyploidy means more than two complete sets of chromosomes: triploid, tetraploid, hexaploid. About half of all flowering plant species are polyploid. In autopolyploidy the sets come from one species: A A becomes A A A A, as in the potato, and triploid banana and seedless watermelon."):
            self.play(FadeIn(head), FadeIn(c2))
            self.play(TransformFromCopy(c2, c4), FadeIn(la[0]), FadeIn(ex[0]))
        with self.say("In allopolyploidy the sets come from two different species: A B becomes A A B B. Bread wheat is a hexaploid of this kind, and so are cotton, tobacco and Triticale, the first man made cereal."):
            self.play(FadeIn(a2))
            self.play(TransformFromCopy(a2, a4), FadeIn(la[1]), FadeIn(ex[1]))
        self.play(FadeOut(VGroup(c2, c4, a2, a4, la, ex)))
        rad = sets([th.SKY], -4.6, 1.0)
        cab = sets([th.AMBER], -1.6, 1.0)
        hyb = sets([th.SKY, th.AMBER], -3.1, -0.4)
        dbl = sets([th.SKY, th.SKY, th.AMBER, th.AMBER], -3.1, -1.8)
        rl = T("radish (n = 9)", size=22, color=th.SKY).next_to(rad, UP, buff=0.15)
        cl = T("cabbage (n = 9)", size=22, color=th.AMBER).next_to(cab, UP, buff=0.15)
        hl = T("hybrid: 18, but sterile — nothing pairs", size=22, color=th.CORAL).next_to(hyb, RIGHT, buff=0.3)
        dl = T("doubled: 36 — every set has a partner → fertile", size=22, color=th.MINT).next_to(dbl, RIGHT, buff=0.3)
        with self.say("Here is the classic story. In nineteen twenty eight Karpechenko crossed radish with cabbage, nine chromosomes each per gamete. The hybrid had eighteen chromosomes, but nine radish and nine cabbage, so none could pair at meiosis. It was sterile."):
            self.play(FadeIn(rad), FadeIn(cab), FadeIn(rl), FadeIn(cl))
            self.play(TransformFromCopy(VGroup(rad, cab), hyb), FadeIn(hl))
        with self.say("Then, now and then, the chromosome number doubled. With thirty six, every chromosome had a partner again, and the plant was fertile: Raphanobrassica, a new allopolyploid. Sadly, it had the root of a cabbage and the leaves of a radish."):
            self.play(TransformFromCopy(hyb, dbl), FadeIn(dl))
            nb = B.neby_in(self, "laugh", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(rad, cab, rl, cl, hyb, hl, dbl, dl)))
        col = para("Colchicine, from Colchicum autumnale, stops the spindle forming, so doubled chromosomes stay in one nucleus. Effects: the gigas effect (bigger cells, leaves, flowers, fruits) and, in odd polyploids like 3n, sterility — which is why bananas are seedless.", width=11.5, size=25, color=th.INK).move_to([0, 0.6, 0])
        warn = self.callout("careful", "Polyploidy changes whole sets (3n, 4n). Aneuploidy changes single chromosomes (2n ± 1). Down's syndrome is aneuploidy; bread wheat is polyploidy.", width=11, size=25).move_to([0, -1.8, 0])
        with self.say("Breeders make polyploids with colchicine, from the autumn crocus. It stops the spindle forming, so the doubled chromosomes stay in one nucleus. Polyploids show the gigas effect: bigger cells, leaves, flowers and fruits. And odd polyploids, like triploids, are sterile, because three sets cannot pair evenly. That is exactly why a banana has no seeds."):
            self.play(FadeIn(col))
        with self.say("And one distinction to keep straight. Polyploidy changes whole sets. Aneuploidy changes single chromosomes. Down's syndrome is aneuploidy; bread wheat is polyploidy."):
            self.play(FadeIn(warn, shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, col, warn)))
        rows = [["", "autopolyploidy", "allopolyploidy"], ["sets from", "one species", "two different species"], ["make-up", "AAAA", "AABB"], ["pairing", "multivalents", "normal bivalents"],
                ["fertility", "often low", "usually fertile"], ["examples", "potato, banana, watermelon", "wheat, Raphanobrassica, Triticale"]]
        tb = B.table(rows, [2.6, 4.6, 4.8], row_h=0.66, size=24, colors=[th.MUTED, th.SKY, th.PINK]).move_to([0, 0.2, 0])
        with self.say("The table for the exam: source of the sets, make up, pairing at meiosis, fertility, and examples.") as v:
            B.reveal_table(self, tb, max(2.5, v.dur * 0.9))
        self.wait(1.5)
        self.play(FadeOut(tb))
        self.quiz("Raphanobrassica is an example of",
                  ["autopolyploidy", "allopolyploidy", "monosomy", "trisomy"], 1,
                  "Last check. Radish crossed with cabbage, then doubled. What is Raphanobrassica?",
                  "Allopolyploidy: its sets come from two different species, Raphanus sativus and Brassica oleracea. Autopolyploidy is the trap, but that multiplies the sets of a single species. Monosomy and trisomy change single chromosomes, not sets.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "DNA is the genetic material (Griffith, Avery, Hershey–Chase); RNA in some viruses.",
            "Double helix: antiparallel, A=T (2 H-bonds), G≡C (3); 2 nm, 3.4 nm per turn, 10 bp.",
            "Replication semi-conservative and 5′→3′: leading strand + Okazaki fragments.",
            "Mendel: 3:1, 9:3:3:1, test cross 1:1:1:1; chi-square checks the fit.",
            "Beyond Mendel: 1:2:1, codominance, ABO, sex by the father's sperm, X-linked in males.",
            "Linkage + crossing over → RF = map distance. Mutation and polyploidy make new variation.",
        ], "Quick recap. DNA is the genetic material, as Griffith, Avery and Hershey and Chase showed, though some viruses use RNA. It is an antiparallel double helix, A with T by two bonds, G with C by three, two nanometres wide, three point four per turn. It replicates semi conservatively, always five prime to three prime, so one strand is leading and one is made in Okazaki fragments. Mendel gives three to one, nine three three one, and one one one one in a test cross, and chi square tells you if the data fit. Beyond Mendel: incomplete dominance, codominance, the ABO alleles, a baby's sex set by the father, and X linked traits in men. Linkage and crossing over give recombination frequencies, which are map distances. And mutation and polyploidy create the new variation that evolution needs.")
        self.outro("That was genetics, the biggest unit of botany. Work every Punnett square in this video yourself with pen and paper; it is the only way the ratios stick. Next, embryology: how a flower makes a seed, and how one pollen grain ends up with two sperm. See you there.")
