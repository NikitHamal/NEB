import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
import _hum as H  # noqa: E402
from _hum import OXY, DEOXY, GUT, BILE, LYMPH, polar  # noqa: E402


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 8
    TITLE = "Human Biology"
    SUBTITLE = "Eight systems, one body"
    SECTIONS = ["Digestive system", "Respiratory system", "Circulatory system", "Excretory system",
                "Nervous system", "Sense organs", "Endocrinology", "Reproductive system"]
    NEXT = "Unit 9 · Human Population and Health Disorders"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    def worked(self, problem, lines, says, size=36):
        head, prob = B.example_head(self, problem, size=25)
        steps = VGroup(*[M(l_, size=size) if isinstance(l_, str) else l_ for l_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
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
        clock = VGroup(Circle(radius=0.9, stroke_color=th.MUTED, stroke_width=4), Dot(radius=0.06, color=WHITE))
        hand = Line(ORIGIN, UP * 0.75, color=th.AMBER, stroke_width=5)
        clk = VGroup(clock, hand).move_to([-4.6, 1.2, 0])
        lab = T("one ordinary day", size=26, color=th.MUTED).next_to(clk, DOWN, buff=0.2)
        facts = [("your heart pumps", 7200, "litres of blood", OXY), ("your lungs move", 10800, "litres of air", th.SKY), ("your kidneys filter", 180, "litres of plasma", th.AMBER)]
        rows = VGroup()
        for i, (a, n, b, c_) in enumerate(facts):
            r = VGroup(T(a, size=28, color=th.BODY), Integer(0, font_size=56, color=c_), T(b, size=28, color=th.BODY)).arrange(RIGHT, buff=0.3).move_to([1.4, 1.5 - 1.3 * i, 0])
            rows.add(r)
        with self.say("Think about one ordinary day. You went to class, ate dal bhat, maybe played football. Meanwhile, without asking you, your heart pumped about seven thousand two hundred litres of blood. Your lungs moved over ten thousand litres of air. And your kidneys filtered one hundred and eighty litres of plasma, then quietly took back almost all of it.") as v:
            self.play(FadeIn(clk), FadeIn(lab))
            self.play(Rotate(hand, -TAU * 2, about_point=clk[0][1].get_center()), run_time=v.dur * 0.3, rate_func=rate_functions.linear)
            for r, (_, n, _, _) in zip(rows, facts):
                self.play(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1]), run_time=0.4)
                self.play(r[1].animate.set_value(n), run_time=1.2)
        nb = B.neby_in(self, "surprised", height=1.4)
        with self.say("Eight organ systems, working together every second, all controlled by nerves and hormones. Today we take the whole machine apart, system by system."):
            pass
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(clk, lab, rows)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 8: Human Biology, the biggest unit of zoology. Eight systems, every one with a diagram and a calculation the board loves to ask."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Eight parts. Digestion. Breathing and gas transport. The heart and circulation. The kidney. Nerves and the brain. The eye and ear. The hormones. And the reproductive system.")

    # ------------------------------------------------------------------ part 1: digestion
    def p1(self):
        self.section(0)
        path = H.gut_path().scale(0.95).move_to([-2.8, -0.15, 0])
        tube = path.copy().set_stroke(GUT, width=14)
        bolus = Dot(path.get_start(), radius=0.16, color=th.AMBER)
        stops = [(0.0, "mouth and buccal cavity", "teeth chew; saliva starts starch digestion; tongue rolls a bolus"), (0.12, "oesophagus", "25 cm; no enzyme; peristalsis"),
                 (0.25, "stomach", "1–1.5 L; HCl, pepsin; churns food into chyme"), (0.45, "small intestine", "about 6 m: duodenum, jejunum, ileum; most digestion, all absorption"),
                 (0.82, "large intestine", "about 1.5 m: caecum, colon, rectum; water reabsorbed, faeces formed"), (1.0, "anus", "egestion")]
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.8, size=25)
        with self.say("Food arrives as polymers, starch, protein and fat, far too big to cross a cell membrane. Digestion breaks them into small monomers that can. It happens in a tube about nine metres long, from mouth to anus, helped by glands outside it: the salivary glands, the liver and the pancreas."):
            self.play(Create(tube), run_time=2.0)
            self.play(FadeIn(bolus))
        with self.say("Follow a mouthful. Chewed and mixed with saliva in the mouth. Pushed down the oesophagus by peristalsis. Churned in the acid stomach into chyme. Digested and absorbed along six metres of small intestine. And in the large intestine, water is taken back and faeces are formed.") as v:
            per = v.dur / len(stops)
            prev = 0
            for f, n_, d_ in stops:
                self.play(MoveAlongPath(bolus, path.copy().pointwise_become_partial(path, prev, max(f, prev + 0.001))), run_time=max(0.3, per * 0.45))
                cap(n_.capitalize(), color=GUT, swatch=GUT, sub=d_)
                self.hold(per * 0.35)
                prev = f
        self.play(FadeOut(VGroup(tube, bolus)))
        cap.clear()
        mem = self.callout("remember", "Mouth → pharynx → oesophagus → stomach → duodenum → jejunum → ileum → caecum → colon → rectum → anus. Three sphincters: cardiac, pyloric, anal.", width=11, size=26)
        with self.say("Learn the order once and you will never lose it: mouth, pharynx, oesophagus, stomach, duodenum, jejunum, ileum, caecum, colon, rectum, anus. Guarded by three sphincters: cardiac, pyloric and anal."):
            self.play(FadeIn(mem, shift=UP * 0.2))
        self.play(FadeOut(mem))
        perm = M(r"2\left(\frac{I\,2\ \ C\,1\ \ PM\,2\ \ M\,3}{I\,2\ \ C\,1\ \ PM\,2\ \ M\,3}\right) = 32", size=48).move_to([0, 1.2, 0])
        milk = M(r"2\left(\frac{I\,2\ \ C\,1\ \ M\,2}{I\,2\ \ C\,1\ \ M\,2}\right) = 20", size=48, color=th.MINT).move_to([0, -0.8, 0])
        l1 = T("permanent teeth", size=24, color=th.MUTED).next_to(perm, UP, buff=0.2)
        l2 = T("milk teeth: no premolars", size=24, color=th.MINT).next_to(milk, UP, buff=0.2)
        th_ = T("thecodont · dicyphodont · heterodont", size=26, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Our teeth sit in bony sockets, come in two sets, and are of four kinds: incisors cut, canines tear, premolars and molars grind. The dental formula counts one half of each jaw, so it is doubled. Two incisors, one canine, two premolars, three molars, above and below: thirty two. Milk teeth have no premolars: twenty."):
            self.play(FadeIn(l1), Write(perm))
            self.play(FadeIn(l2), Write(milk))
            self.play(FadeIn(th_))
        self.play(FadeOut(VGroup(perm, milk, l1, l2, th_)))
        self.p1_enzymes()
        self.p1_villus()

    def p1_enzymes(self):
        head = T("Where each food is digested", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cols = ["mouth (pH 6.8)", "stomach (pH 2)", "small intestine (pH 8)"]
        xs = [-4.0, 0.0, 4.0]
        hdr = VGroup(*[T(c_, size=24, color=th.AMBER, weight="BOLD").move_to([x, 2.0, 0]) for c_, x in zip(cols, xs)])
        foods = [("starch", th.SKY, [("salivary amylase → maltose", 0), ("pancreatic amylase → maltose; maltase → glucose", 2)]),
                 ("protein", th.CORAL, [("pepsin → peptones", 1), ("trypsin, chymotrypsin → peptides; peptidases → amino acids", 2)]),
                 ("fat", th.AMBER, [("bile emulsifies; lipase → fatty acids + glycerol", 2)])]
        rows = VGroup()
        with self.say("Now the chemistry, food by food. Starch is started by salivary amylase in the mouth, paused in the acid stomach, and finished in the small intestine by pancreatic amylase and then maltase, down to glucose.") as v:
            self.play(FadeIn(head), FadeIn(hdr))
            y = 0.9
            n_, c_, steps = foods[0]
            lab = T(n_, size=26, color=c_, weight="BOLD").move_to([-6.1, y, 0])
            self.play(FadeIn(lab))
            for txt, col in steps:
                t_ = para(txt, width=3.6, size=20, color=c_, align="center").move_to([xs[col], y, 0])
                self.play(FadeIn(t_, shift=RIGHT * 0.2))
                rows.add(t_)
            rows.add(lab)
        with self.say("Protein begins in the stomach, where pepsin, activated by hydrochloric acid, cuts it into peptones. In the intestine, trypsin and chymotrypsin carry on, and peptidases on the brush border finish the job: amino acids."):
            y = -0.4
            n_, c_, steps = foods[1]
            lab = T(n_, size=26, color=c_, weight="BOLD").move_to([-6.1, y, 0])
            self.play(FadeIn(lab))
            for txt, col in steps:
                t_ = para(txt, width=3.6, size=20, color=c_, align="center").move_to([xs[col], y, 0])
                self.play(FadeIn(t_, shift=RIGHT * 0.2))
                rows.add(t_)
            rows.add(lab)
        with self.say("Fat is handled almost entirely in the intestine. Bile from the liver has no enzyme at all: its salts emulsify the fat into tiny droplets, giving lipase far more surface to work on. The products: fatty acids and glycerol."):
            y = -1.7
            n_, c_, steps = foods[2]
            lab = T(n_, size=26, color=c_, weight="BOLD").move_to([-6.1, y, 0])
            self.play(FadeIn(lab))
            big = Circle(radius=0.45, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.8).move_to([2.2, -2.7, 0])
            small = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.8).move_to([2.2 + dx, -2.7 + dy, 0]) for dx in (-0.4, -0.15, 0.15, 0.4) for dy in (-0.2, 0.2)])
            self.play(FadeIn(big))
            self.play(ReplacementTransform(big, small))
            for txt, col in steps:
                t_ = para(txt, width=3.6, size=20, color=c_, align="center").move_to([xs[col], y, 0])
                self.play(FadeIn(t_, shift=RIGHT * 0.2))
                rows.add(t_)
            rows.add(lab, small)
        self.play(FadeOut(VGroup(head, hdr, rows)))
        self.tip("Protein-digesting enzymes are secreted INACTIVE (pepsinogen, trypsinogen) so they cannot digest the gland. HCl activates pepsinogen; enterokinase activates trypsinogen. Bile has NO enzyme.",
                 "Exam tip. Protein digesting enzymes are made in an inactive form, pepsinogen and trypsinogen, so they cannot digest the gland that makes them. Acid activates pepsinogen; enterokinase activates trypsinogen. And bile contains no enzyme at all.", width=8.6)

    def p1_villus(self):
        head = T("Absorption: the villus", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        v = H.villus(3.6, 1.4).move_to([-3.0, -0.4, 0])
        P = v.parts
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.8, size=25)
        with self.say("Absorption happens almost entirely in the small intestine, and its surface is multiplied three times over: by circular folds, by finger like villi, and by microvilli on every cell, the brush border. The total area is about two hundred square metres, a badminton court folded inside you."):
            self.play(FadeIn(head), FadeIn(P["wall"]))
            self.play(Create(P["brush"]))
            cap("Folds × villi × microvilli ≈ 200 m²", color=GUT, swatch=GUT)
        glu = VGroup(*[Dot(radius=0.07, color=th.SKY).move_to(P["wall"].point_from_proportion(t) + LEFT * 0.4 + UP * 0.1) for t in (0.15, 0.3)])
        fat = VGroup(*[Dot(radius=0.07, color=th.AMBER).move_to(P["wall"].point_from_proportion(t) + RIGHT * 0.4 + UP * 0.1) for t in (0.7, 0.85)])
        with self.say("Inside each villus runs a net of blood capillaries and a central lymph vessel, the lacteal. Glucose and amino acids are absorbed by active transport into the blood, and travel by the hepatic portal vein to the liver first."):
            self.play(Create(P["capillary"]), Create(P["lacteal"]))
            self.play(FadeIn(glu))
            self.play(*[d_.animate.move_to(P["capillary"].point_from_proportion(0.25 + 0.4 * i)) for i, d_ in enumerate(glu)], run_time=1.2)
            cap("Sugars, amino acids → blood capillary → hepatic portal vein → liver", color=OXY, swatch=OXY)
        with self.say("Fatty acids and glycerol are rebuilt into fat inside the cell, packed into chylomicrons, and enter the lacteal. They travel in the lymph to the neck veins, bypassing the liver."):
            self.play(FadeIn(fat))
            self.play(*[d_.animate.move_to(P["lacteal"].point_from_proportion(0.4 + 0.3 * i)) for i, d_ in enumerate(fat)], run_time=1.2)
            cap("Fats → chylomicrons → lacteal → lymph (bypass the liver)", color=LYMPH, swatch=LYMPH)
        self.play(FadeOut(VGroup(head, v, glu, fat)))
        cap.clear()
        self.quiz("Which digestive juice contains NO digestive enzyme?",
                  ["saliva", "gastric juice", "bile", "pancreatic juice"], 2,
                  "Pause and think. Which juice has no enzyme at all?",
                  "Bile. It only emulsifies fat and neutralises acid; its salts are not enzymes. Pancreatic juice is the trap in the other direction: it is the most complete digestive juice, with enzymes for every kind of food.")

    # ------------------------------------------------------------------ part 2: respiration
    def p2(self):
        self.section(1)
        path = ["nostrils", "nasal chambers", "pharynx", "larynx", "trachea", "bronchi", "bronchioles", "alveoli"]
        chips = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=1.45, height=0.6, stroke_color=th.SKY if i < 7 else th.MINT, stroke_width=2, fill_color=th.PANEL, fill_opacity=1),
                                para(p_, width=1.35, size=18, color=th.INK, align="center")) for i, p_ in enumerate(path)])
        for c_ in chips:
            c_[1].move_to(c_[0])
        chips.arrange(RIGHT, buff=0.18).move_to([0, 1.6, 0])
        br = VGroup(Brace(chips[:7], DOWN, color=th.SKY), Brace(chips[7:], DOWN, color=th.MINT))
        bl = VGroup(T("conducting: warms, moistens, filters", size=22, color=th.SKY).next_to(br[0], DOWN, buff=0.1), T("exchange", size=22, color=th.MINT).next_to(br[1], DOWN, buff=0.1))
        fick = M(r"\text{rate of diffusion} \propto \frac{\text{area} \times \Delta p}{\text{thickness}}", size=40).move_to([0, -1.3, 0])
        nums = T("300 million alveoli · 70 m² · membrane under 1 µm", size=26, color=th.MINT).move_to([0, -2.5, 0])
        with self.say("Air travels a conducting path that warms, moistens and filters it, but exchanges nothing: nostrils, nasal chambers, pharynx, larynx, trachea held open by C shaped rings of cartilage, bronchi and bronchioles. Exchange happens only in the alveoli."):
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in chips], lag_ratio=0.12))
            self.play(GrowFromCenter(br[0]), FadeIn(bl[0]), GrowFromCenter(br[1]), FadeIn(bl[1]))
        with self.say("Fick's law says diffusion is fastest with a large area, a steep pressure difference, and a thin barrier. The lung maximises all three: three hundred million alveoli, seventy square metres, and a membrane less than a micrometre thick."):
            self.play(Write(fick))
            self.play(FadeIn(nums))
        self.play(FadeOut(VGroup(chips, br, bl, fick, nums)))
        self.p2_breathing()
        self.p2_volumes()
        self.p2_transport()

    def p2_breathing(self):
        head = T("Breathing is Boyle's law", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        d = ValueTracker(0.0)
        C = np.array([-3.2, -0.2, 0])

        def chest():
            k = d.get_value()
            g = VGroup()
            w = 3.0 + 0.5 * k
            jar = RoundedRectangle(corner_radius=0.5, width=w, height=3.4, stroke_color=th.BODY, stroke_width=3).move_to(C + UP * 0.1)
            dia = VMobject(stroke_color=th.CORAL, stroke_width=7).set_points_smoothly([C + [-w / 2, -1.6, 0], C + [0, -1.6 + 0.5 * (1 - k), 0], C + [w / 2, -1.6, 0]])
            tr = Line(C + UP * 1.9, C + UP * 0.8, color=th.SKY, stroke_width=6)
            lungs = VGroup(*[Ellipse(width=0.9 + 0.4 * k, height=1.6 + 0.5 * k, stroke_color=th.PINK, stroke_width=3, fill_color=th.PINK, fill_opacity=0.25).move_to(C + [s * (0.65 + 0.15 * k), 0.0 - 0.1 * k, 0]) for s in (-1, 1)])
            g.add(jar, dia, tr, lungs)
            return g

        ch = always_redraw(chest)
        cap = B.Captions(self, at=(3.4, 0.2, 0), width=5.6, size=25)
        flow_in = VGroup(*[Arrow(C + UP * 2.9 + RIGHT * dx, C + UP * 2.0 + RIGHT * dx, buff=0, color=th.SKY, stroke_width=4) for dx in (-0.25, 0.25)])
        with self.say("Breathing is pure physics. Enlarge the chest, and the pressure inside falls below the air outside, so air rushes in. In inspiration the diaphragm contracts and flattens, and the external intercostal muscles lift the ribs up and out. The lungs expand and about half a litre of air enters."):
            self.play(FadeIn(head))
            self.add(ch)
            cap("Inspiration: active", color=th.SKY, sub="Diaphragm contracts and flattens; external intercostals lift the ribs. Volume up, pressure down, air in.")
            self.play(d.animate.set_value(1.0), GrowArrow(flow_in[0]), GrowArrow(flow_in[1]), run_time=2.0)
        with self.say("Expiration is normally passive. The muscles relax, the elastic lungs and chest wall recoil, the volume falls, the pressure rises, and air is pushed out. Only forced breathing uses the internal intercostals and the abdominal muscles."):
            self.play(FadeOut(flow_in))
            cap("Expiration: normally passive", color=th.PINK, sub="Muscles relax; elastic recoil; volume down, pressure up, air out.")
            self.play(d.animate.set_value(0.0), run_time=2.0)
            self.play(d.animate.set_value(1.0), run_time=1.2)
            self.play(d.animate.set_value(0.0), run_time=1.2)
        with self.say("The rhythm is set by the respiratory centre in the medulla, adjusted by the pons, and driven mostly by a rise in carbon dioxide and acidity in the blood, not by a fall in oxygen."):
            cap("Control: medulla (rhythm) + pons", sub="Chemoreceptors respond mainly to rising CO₂ and H⁺.")
        self.play(FadeOut(head), FadeOut(ch))
        self.remove(ch)
        cap.clear()

    def p2_volumes(self):
        head = T("Lung volumes on a spirogram", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 12, 1], y_range=[0, 6000, 1000], x_length=7.4, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-2.2, -0.5, 0])
        base = 2300

        def vol(t):
            if t < 3:
                return base + 250 + 250 * np.sin(t * TAU / 1.5)
            if t < 4.5:
                return base + 250 + 250 * np.sin(3 * TAU / 1.5) + (t - 3) / 1.5 * 3000
            if t < 6.5:
                return 5800 - 500 - (t - 4.5) / 2.0 * (5800 - 500 - 1200)
            if t < 8:
                return 1200 + (t - 6.5) / 1.5 * (base - 1200 + 250)
            return base + 250 + 250 * np.sin((t - 8) * TAU / 1.5)

        tr = ax.plot(vol, x_range=[0, 11.5, 0.02], color=th.SKY, stroke_width=4)
        rv = Rectangle(width=ax.c2p(11.5, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1200)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=th.CORAL, fill_opacity=0.2).move_to(ax.c2p(5.75, 600))
        x0 = ax.c2p(9.2, 0)[0]

        def brace(y0, y1, txt, col, x):
            a, b = np.array([x, ax.c2p(0, y0)[1], 0]), np.array([x, ax.c2p(0, y1)[1], 0])
            return VGroup(DoubleArrow(a, b, buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.08), T(txt, size=18, color=col).next_to((a + b) / 2, RIGHT, buff=0.08))

        tv = brace(2300, 2800, "TV 500", th.MINT, ax.c2p(1.2, 0)[0])
        irv = brace(2800, 5800, "IRV 3000", th.SKY, ax.c2p(5.0, 0)[0])
        erv = brace(1200, 2300, "ERV 1100", th.AMBER, ax.c2p(7.0, 0)[0])
        rvb = brace(0, 1200, "RV 1200", th.CORAL, ax.c2p(10.6, 0)[0])
        caps = VGroup(*[T(s_, size=24, color=c_) for s_, c_ in [("VC = TV + IRV + ERV = 4600 ml", th.INK), ("TLC = VC + RV = 5800 ml", th.INK), ("IC = 3500 · FRC = 2300 ml", th.BODY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.4, 1.0, 0])
        warn = para("A spirometer cannot measure RV, so it cannot measure TLC or FRC either.", width=4.6, size=22, color=th.CORAL).move_to([4.4, -1.3, 0])
        yl = T("ml", size=20, color=th.MUTED).next_to(ax.c2p(0, 6000), LEFT, buff=0.1)
        with self.say("A spirometer records each breath. Quiet breathing moves the tidal volume, about five hundred millilitres. Take the deepest breath you can: the extra is the inspiratory reserve, about three thousand. Breathe out as hard as you can: the expiratory reserve, about eleven hundred. And about twelve hundred millilitres can never be breathed out at all: the residual volume.") as v:
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            self.play(Create(tr), run_time=v.dur * 0.35, rate_func=rate_functions.linear)
            self.play(FadeIn(tv))
            self.play(FadeIn(irv))
            self.play(FadeIn(erv))
            self.play(FadeIn(rv), FadeIn(rvb))
        with self.say("Capacities are sums of volumes. The vital capacity, the most you can breathe out after the deepest breath, is tidal plus both reserves: four thousand six hundred. Add the residual volume for the total lung capacity: five thousand eight hundred. One trap: a spirometer can never see the residual volume, so it cannot measure total lung capacity either."):
            self.play(LaggedStart(*[FadeIn(c_, shift=LEFT * 0.2) for c_ in caps], lag_ratio=0.4))
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(head, ax, tr, rv, tv, irv, erv, rvb, caps, warn, yl)))
        self.worked("Breathing 15 times a minute, tidal volume 500 ml, dead space 150 ml. Find (a) pulmonary ventilation, (b) alveolar ventilation. (c) What if she takes shallow 250 ml breaths at 30 a minute?",
                    [r"\text{(a)}\ \ 500 \times 15 = 7500 \text{ ml/min}", r"\text{(b)}\ \ (500 - 150) \times 15 = 5250 \text{ ml/min}",
                     r"\text{(c)}\ \ 250\times30 = 7500 \text{ (same)},\ \ (250-150)\times30 = 3000 \text{ ml/min: } 43\% \text{ less}"],
                    ["A worked example on dead space.", "Pulmonary ventilation is tidal volume times rate: seven and a half litres a minute.",
                     "But the first hundred and fifty millilitres of each breath only fills the airways. Alveolar ventilation is three hundred and fifty times fifteen: five thousand two hundred and fifty.",
                     "Now shallow, fast breathing. The total is the same, seven and a half litres, but only a hundred millilitres per breath reaches the alveoli: three thousand. Panting is a poor way to get oxygen."])

    def p2_transport(self):
        head = T("How oxygen is carried", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 100, 20], y_range=[0, 100, 25], x_length=6.0, y_length=3.8, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-2.4, -0.5, 0])
        xl = T("pO₂ (mmHg)", size=20, color=th.MUTED).next_to(ax, DOWN, buff=0.35)
        yl = T("% saturation", size=20, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.35)
        sh = ValueTracker(0.0)
        sig = lambda p, p50: 100 * p ** 2.7 / (p ** 2.7 + p50 ** 2.7)
        curve = always_redraw(lambda: ax.plot(lambda p: sig(p, 26 + sh.get_value()), x_range=[0.5, 100, 0.5], color=OXY, stroke_width=5))
        base = ax.plot(lambda p: sig(p, 26), x_range=[0.5, 100, 0.5], color=OXY, stroke_width=2, stroke_opacity=0.35)
        lung = DashedLine(ax.c2p(100, 0), ax.c2p(100, 100), color=th.SKY)
        tis = DashedLine(ax.c2p(40, 0), ax.c2p(40, 100), color=th.AMBER)
        ll = VGroup(T("lungs", size=20, color=th.SKY).next_to(ax.c2p(100, 100), UP, buff=0.05), T("tissues", size=20, color=th.AMBER).next_to(ax.c2p(40, 100), UP, buff=0.05))
        cap = B.Captions(self, at=(4.0, 0.0, 0), width=4.8, size=24)
        with self.say("Gases move only by diffusion, down partial pressure gradients. Ninety seven percent of oxygen rides on haemoglobin, each molecule carrying four oxygens. The curve of saturation against oxygen pressure is S shaped: nearly full in the lungs, and giving oxygen up steeply around the tissues."):
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.add(curve)
            self.play(Create(lung), Create(tis), FadeIn(ll))
            cap("Sigmoid dissociation curve", color=OXY, swatch=OXY, sub="97% of O₂ as oxyhaemoglobin, 3% dissolved.")
        with self.say("In working muscle, carbon dioxide and acid rise and the temperature goes up. All of these shift the curve to the right: the Bohr effect. At the same pressure, haemoglobin lets go of more oxygen exactly where it is needed most."):
            self.add(base)
            self.play(sh.animate.set_value(10), run_time=2.0)
            cap("Bohr effect: shift to the right", color=th.AMBER, sub="More CO₂, more H⁺, higher temperature → more O₂ unloaded in active tissue.")
        self.play(FadeOut(VGroup(head, ax, xl, yl, base, lung, tis, ll)), FadeOut(curve))
        self.remove(curve)
        cap.clear()
        bars = VGroup()
        for i, (n_, v_, c_) in enumerate([("bicarbonate in plasma", 70, th.SKY), ("carbaminohaemoglobin", 23, th.PINK), ("dissolved", 7, th.MUTED)]):
            r = Rectangle(width=v_ / 70 * 5.0, height=0.5, stroke_width=0, fill_color=c_, fill_opacity=0.9)
            r.move_to([-1.0 + r.width / 2, 0.8 - 0.8 * i, 0])
            bars.add(VGroup(r, T(n_, size=22, color=th.INK).next_to([-1.0, 0.8 - 0.8 * i, 0], LEFT, buff=0.2), T(f"{v_}%", size=22, color=c_).next_to(r, RIGHT, buff=0.15)))
        eq = M(r"CO_2 + H_2O \underset{\text{carbonic anhydrase}}{\rightleftharpoons} H_2CO_3 \rightleftharpoons H^+ + HCO_3^-", size=38).move_to([0, -1.9, 0])
        h2 = T("How carbon dioxide is carried", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        with self.say("Carbon dioxide travels three ways. About seventy percent as bicarbonate, made inside red cells by the enzyme carbonic anhydrase. About a quarter bound to haemoglobin as carbaminohaemoglobin. And about seven percent simply dissolved."):
            self.play(FadeIn(h2), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars], lag_ratio=0.3))
            self.play(Write(eq))
        self.play(FadeOut(VGroup(h2, bars, eq)))
        self.worked("Haemoglobin 15 g per 100 ml; 1 g binds 1.34 ml O₂; blood volume 5 L. Find (a) O₂ capacity of 100 ml blood, (b) total O₂ on haemoglobin, (c) O₂ delivered per minute if 5 ml leaves each 100 ml and cardiac output is 5 L/min.",
                    [r"\text{(a)}\ \ 1.34 \times 15 = 20.1 \text{ ml per 100 ml}", r"\text{(b)}\ \ 50 \times 20.1 = 1005 \text{ ml} \approx 1.0 \text{ L}", r"\text{(c)}\ \ 5000 \times \tfrac{5}{100} = 250 \text{ ml/min}"],
                    ["A worked example on oxygen capacity.", "Fifteen grams times one point three four: twenty point one millilitres of oxygen per hundred millilitres of blood.",
                     "Five litres is fifty lots of a hundred millilitres: about one litre of oxygen on haemoglobin in the whole body.", "And five litres a minute, each hundred millilitres giving up five: two hundred and fifty millilitres a minute, exactly an adult's resting oxygen use."])
        self.quiz("The volume of air that remains in the lungs even after the most forceful expiration is the",
                  ["tidal volume", "vital capacity", "residual volume", "expiratory reserve volume"], 2,
                  "Pause and think. What is left after you blow out as hard as you can?",
                  "The residual volume, about twelve hundred millilitres, which keeps the alveoli from collapsing. The expiratory reserve is the trap: that is the extra air you CAN force out.")

    # ------------------------------------------------------------------ part 3: circulation
    def p3(self):
        self.section(2)
        chain = VGroup(*[T(s_, size=26, color=c_, weight="BOLD") for s_, c_ in [("injury", th.CORAL), ("thromboplastin + Ca²⁺", th.AMBER), ("prothrombin → thrombin", th.SKY), ("fibrinogen → fibrin", th.MINT)]]).arrange(RIGHT, buff=0.6).move_to([0, 2.0, 0])
        if chain.width > 12.6:
            chain.scale_to_fit_width(12.6)
        arr = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.08, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        rng = np.random.default_rng(5)
        mesh = VGroup(*[Line([rng.uniform(-3, 3), rng.uniform(-2.5, 0.6), 0], [rng.uniform(-3, 3), rng.uniform(-2.5, 0.6), 0], color=th.MINT, stroke_width=2) for _ in range(18)])
        rbc = VGroup(*[Circle(radius=0.18, stroke_width=0, fill_color=OXY, fill_opacity=0.9).move_to([rng.uniform(-2.6, 2.6), rng.uniform(-2.2, 0.3), 0]) for _ in range(14)])
        with self.say("Blood was covered in the tissues unit, so here is what is new. When a vessel is cut, platelets and damaged tissue release thromboplastin. With calcium ions it turns prothrombin into thrombin, and thrombin turns soluble fibrinogen into threads of fibrin. The threads trap blood cells: a clot. The liver needs vitamin K to make prothrombin."):
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chain], lag_ratio=0.4), LaggedStart(*[GrowArrow(a_) for a_ in arr], lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(rbc))
            self.play(LaggedStart(*[Create(m_) for m_ in mesh], lag_ratio=0.05))
        self.play(FadeOut(VGroup(chain, arr, mesh, rbc)))
        rows = [["group", "antigen on RBC", "antibody in plasma", "donates to", "receives from"], ["A", "A", "anti-B", "A, AB", "A, O"], ["B", "B", "anti-A", "B, AB", "B, O"],
                ["AB", "A and B", "none", "AB", "all: universal recipient"], ["O", "none", "anti-A and anti-B", "all: universal donor", "O"]]
        tb = B.table(rows, [1.4, 2.4, 2.8, 2.8, 3.4], row_h=0.66, size=22, colors=[th.AMBER, th.INK, th.INK, th.MINT, th.SKY]).move_to([0, 0.9, 0])
        rh = para("Rh: an Rh⁻ mother with an Rh⁺ baby can make anti-D after the first birth; it can destroy a later Rh⁺ baby's red cells (erythroblastosis foetalis). Prevented with anti-D within 72 hours.", width=12, size=22, color=th.CORAL).move_to([0, -2.3, 0])
        with self.say("Blood groups. Group A cells carry antigen A, and the plasma carries anti B. Group O cells carry no antigen, so O can be given to anyone: the universal donor. Group A B plasma has no antibodies, so A B can receive from anyone: the universal recipient. Separately, an Rh negative mother carrying an Rh positive baby can become sensitised, and her antibodies can attack a later Rh positive baby. An anti D injection within seventy two hours of delivery prevents it.") as v:
            B.reveal_table(self, tb, v.dur * 0.55)
            self.play(FadeIn(rh))
        self.play(FadeOut(VGroup(tb, rh)))
        self.p3_heart()
        self.p3_cycle()

    def p3_heart(self):
        hh = H.heart(1.1).move_to([-3.0, -0.2, 0])
        P = hh.parts
        lab = VGroup(T("right atrium", size=20, color=DEOXY).next_to(P["RA"], LEFT, buff=0.15), T("left atrium", size=20, color=OXY).next_to(P["LA"], RIGHT, buff=0.15),
                     T("right ventricle", size=20, color=DEOXY).next_to(P["RV"], LEFT, buff=0.15), T("left ventricle: wall ~3× thicker", size=20, color=OXY).next_to(P["LV"], RIGHT, buff=0.15))
        cap = B.Captions(self, at=(4.2, 2.5, 0), width=4.8, size=24)
        with self.say("The heart: a fist sized muscular pump in a double walled pericardium. Four chambers. Two thin walled atria receive blood; two thick walled ventricles pump it out. The right side carries deoxygenated blood, the left side oxygenated, and a septum keeps them apart. The left ventricle's wall is about three times thicker, because it pumps blood round the whole body."):
            self.play(FadeIn(hh))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lab], lag_ratio=0.25))
        with self.say("Four valves keep the flow one way. The tricuspid between the right atrium and ventricle; the bicuspid, or mitral, on the left; and two semilunar valves at the exits to the pulmonary artery and the aorta. Tendon cords anchor the atrioventricular valves, like the strings of a parachute."):
            self.play(Indicate(P["tricuspid"], color=WHITE, scale_factor=1.6), Indicate(P["bicuspid"], color=WHITE, scale_factor=1.6))
            cap("Tricuspid (R) · bicuspid/mitral (L) · 2 semilunar", sub="Chordae tendineae stop the cusps turning inside out.")
        self.play(FadeOut(lab), hh.animate.scale(0.7).move_to([0, -0.4, 0]))
        cap.clear()
        lungs = RoundedRectangle(corner_radius=0.4, width=3.0, height=0.9, stroke_color=th.PINK, stroke_width=3).move_to([0, 2.5, 0])
        body = RoundedRectangle(corner_radius=0.4, width=3.0, height=0.9, stroke_color=th.MUTED, stroke_width=3).move_to([0, -3.0, 0])
        ll = VGroup(T("lungs", size=24, color=th.PINK).move_to(lungs), T("body", size=24, color=th.MUTED).move_to(body))
        pul = VMobject(stroke_color=DEOXY, stroke_width=6).set_points_smoothly([[-0.75, -0.9, 0], [-1.6, -0.2, 0], [-1.9, 1.5, 0], [-1.2, 2.5, 0]])
        pul2 = VMobject(stroke_color=OXY, stroke_width=6).set_points_smoothly([[1.2, 2.5, 0], [2.6, 0.9, 0], [0.7, 0.4, 0]])
        sys1 = VMobject(stroke_color=OXY, stroke_width=6).set_points_smoothly([[0.7, -1.2, 0], [3.4, -1.6, 0], [1.2, -3.0, 0]])
        sys2 = VMobject(stroke_color=DEOXY, stroke_width=6).set_points_smoothly([[-1.2, -3.0, 0], [-3.4, -1.4, 0], [-3.0, 0.5, 0], [-1.3, 0.3, 0], [-0.75, 0.25, 0]])
        loop = VGroup(sys2, pul, pul2, sys1)
        dot = Dot(radius=0.13, color=WHITE)
        with self.say("Follow one red cell. From the body it returns deoxygenated to the right side, is pumped to the lungs, comes back oxygenated to the left side, and is pumped out to the body. Twice through the heart in one circuit: double circulation. Closed, and complete, because the two kinds of blood never mix.") as v:
            self.play(FadeIn(lungs), FadeIn(body), FadeIn(ll))
            for seg in loop:
                self.play(Create(seg), MoveAlongPath(dot, seg), run_time=max(0.6, v.dur * 0.18))
        cl = para("Also: coronary arteries feed the heart muscle itself; the hepatic portal vein takes gut blood to the liver first.", width=4.2, size=21, color=th.BODY).move_to([4.6, 0.2, 0])
        with self.say("Two special routes. The coronary arteries feed the heart muscle itself; block them, and that is a heart attack. And the hepatic portal vein carries blood from the gut to the liver before it reaches the rest of the body."):
            self.play(FadeIn(cl))
        self.play(FadeOut(VGroup(hh, lungs, body, ll, loop, dot, cl)))

    def p3_cycle(self):
        head = T("One heartbeat: 0.8 seconds", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        x0, W = -5.6, 11.2
        segs = [("atrial 0.1 s", 0.1, th.SKY), ("ventricular systole 0.3 s", 0.3, OXY), ("joint diastole 0.4 s", 0.4, th.MUTED)]
        bar = VGroup()
        x = x0
        for n_, d_, c_ in segs:
            r = Rectangle(width=W * d_ / 0.8, height=0.6, stroke_width=0, fill_color=c_, fill_opacity=0.75).move_to([x + W * d_ / 0.8 / 2, 1.4, 0])
            bar.add(VGroup(r, T(n_, size=19, color=c_ if c_ != th.MUTED else th.BODY).next_to(r, UP, buff=0.12)))
            x += W * d_ / 0.8
        lubb = VGroup(T("lubb", size=28, color=th.AMBER, weight="BOLD"), T("AV valves shut", size=18, color=th.BODY)).arrange(DOWN, buff=0.05).move_to([x0 + W * 0.125, 0.35, 0])
        dupp = VGroup(T("dupp", size=28, color=th.AMBER, weight="BOLD"), T("semilunar valves shut", size=18, color=th.BODY)).arrange(DOWN, buff=0.05).move_to([x0 + W * 0.5, 0.35, 0])
        ecg = VMobject(stroke_color=th.MINT, stroke_width=4).set_points_as_corners(H.ecg_points(beats=1, x0=x0 - W * 0.1, width=W, y0=-1.6, amp=1.0))
        lab = VGroup(T("P", size=24, color=th.MINT).move_to([x0 + W * 0.05, -1.15, 0]), T("QRS", size=24, color=th.MINT).move_to([x0 + W * 0.24, -0.45, 0]), T("T", size=24, color=th.MINT).move_to([x0 + W * 0.52, -1.0, 0]))
        with self.say("Cardiac muscle beats by itself: it is myogenic. The pacemaker is the sino atrial node in the wall of the right atrium, firing about seventy two times a minute. The wave spreads over the atria, pauses about a tenth of a second at the atrioventricular node, then races down the bundle of His and the Purkinje fibres into the ventricles."):
            self.play(FadeIn(head))
        with self.say("At seventy two beats a minute, one cycle takes zero point eight seconds. Atrial systole, a tenth of a second. Ventricular systole, three tenths: the atrioventricular valves slam shut, lubb, and about seventy millilitres is ejected. Then joint diastole, four tenths: the semilunar valves shut, dupp, and the heart refills.") as v:
            for b_ in bar:
                self.play(GrowFromEdge(b_, LEFT), run_time=0.6)
            self.play(FadeIn(lubb, scale=1.3))
            self.sfx("thud", gain=-10)
            self.play(FadeIn(dupp, scale=1.3))
            self.sfx("thud", gain=-12)
        with self.say("The electrical wave can be recorded from the skin: the E C G. The P wave is the atria depolarising. The Q R S complex is the ventricles depolarising, just before they contract. The T wave is the ventricles repolarising. Heart rate is sixty divided by the R to R interval in seconds."):
            self.play(Create(ecg), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lab], lag_ratio=0.3))
        self.play(FadeOut(VGroup(head, bar, lubb, dupp, ecg, lab)))
        self.worked("Heart rate 72 /min, end-diastolic volume 130 ml, end-systolic volume 60 ml. Find (a) stroke volume, (b) cardiac output, (c) ejection fraction, (d) cardiac output in exercise at 150 /min with SV 110 ml.",
                    [r"\text{(a)}\ \ SV = 130 - 60 = 70 \text{ ml}", r"\text{(b)}\ \ CO = 70 \times 72 = 5040 \text{ ml/min} \approx 5.0 \text{ L/min}",
                     r"\text{(c)}\ \ EF = \tfrac{70}{130}\times100 = 53.8\%", r"\text{(d)}\ \ 110 \times 150 = 16\,500 \text{ ml/min} = 16.5 \text{ L/min}"],
                    ["A cardiac output example from the Shahid Gangalal Heart Centre.", "Stroke volume is what the ventricle fills to, minus what is left: seventy millilitres.",
                     "Cardiac output is stroke volume times heart rate: about five litres a minute.", "Ejection fraction is seventy over one hundred and thirty: fifty three point eight percent, just under the normal fifty five to seventy.",
                     "In exercise, one hundred and ten times one hundred and fifty: sixteen and a half litres a minute, more than three times the resting value."])
        self.tip("Cardiac output = stroke volume × heart rate, in litres per minute — not beats per minute. Normal BP 120/80 mmHg; above 140/90 is hypertension.",
                 "Exam tip. Cardiac output is stroke volume times heart rate, measured in litres per minute, not in beats. An athlete has a slow pulse but a normal cardiac output, because each beat pumps more. And normal blood pressure is one twenty over eighty.")

    # ------------------------------------------------------------------ part 4: excretion
    def p4(self):
        self.section(3)
        nh = VGroup(*[VGroup(T(a, size=28, color=c_, weight="BOLD"), T(b, size=22, color=th.BODY), T(e, size=20, color=th.MUTED)).arrange(DOWN, buff=0.12) for a, b, e, c_ in
                      [("ammonotelic", "ammonia: toxic, very soluble", "bony fish (lots of water)", th.SKY), ("ureotelic", "urea: much less toxic", "humans, mammals", th.AMBER), ("uricotelic", "uric acid: nearly insoluble", "birds, reptiles, insects (save water)", th.MINT)]]).arrange(RIGHT, buff=0.9).move_to([0, 0.4, 0])
        with self.say("Deaminating surplus amino acids makes ammonia, which is very toxic. Fish, surrounded by water, simply wash it out: they are ammonotelic. Our liver converts it at once into much less toxic urea, through the ornithine cycle: we are ureotelic. Birds and reptiles, which must save water, make nearly insoluble uric acid: uricotelic."):
            self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.2) for n_ in nh], lag_ratio=0.35))
        self.play(FadeOut(nh))
        ne = H.nephron(1.0).move_to([-1.4, -0.2, 0])
        P = ne.parts
        cap = B.Captions(self, at=(4.6, 0.6, 0), width=3.8, size=23)
        with self.say("Each kidney holds about a million nephrons, its working units. A nephron starts with a knot of about fifty capillaries, the glomerulus, cupped in a double walled Bowman's capsule. Then a long tubule: the proximal convoluted tubule, the loop of Henle diving into the medulla, the distal convoluted tubule, and a collecting duct."):
            self.play(FadeIn(P["medulla"]), Create(P["capsule"]), FadeIn(P["glomerulus"]), Create(P["afferent"]), Create(P["efferent"]))
            self.play(Create(P["tubule"]), run_time=2.0)
            self.play(Create(P["duct"]))
            cap("Nephron", color=th.MINT, sub="Glomerulus + Bowman's capsule, PCT, loop of Henle, DCT, collecting duct.")
        with self.say("Look at the blood vessels. The afferent arteriole bringing blood in is wider than the efferent arteriole taking it out. So blood backs up in the glomerulus, and its pressure stays high. That pressure is what drives filtration."):
            self.play(Indicate(P["afferent"], color=OXY, scale_factor=1.2), Indicate(P["efferent"], color=OXY, scale_factor=1.2))
            cap("Wide in, narrow out", color=OXY, swatch=OXY, sub="Afferent wider than efferent: high glomerular pressure.")
        flow = B.Flow(P["capsule"].get_center() + RIGHT * 0.4 + UP * 0.25, P["tubule"].point_from_proportion(0.3), n=6, color=th.SKY, speed=0.7, seed=3)
        nfp = M(r"\text{NFP} = 55 - 15 - 30 = 10 \text{ mmHg}", size=32).move_to([0.3, 3.0, 0])
        with self.say("Step one: ultrafiltration. Glomerular blood pressure, about fifty five millimetres of mercury, pushes against the fifteen of fluid already in the capsule and the thirty pulling back from plasma proteins. Net filtration pressure: ten. Water and small solutes are squeezed out; cells and proteins stay in the blood."):
            self.add(flow)
            self.play(Write(nfp))
            cap("1. Ultrafiltration", color=th.SKY, swatch=th.SKY, sub="GFR 125 ml/min = 180 litres a day; cells and proteins stay behind.")
            self.wait(1.0)
        with self.say("That is a hundred and twenty five millilitres a minute, a hundred and eighty litres a day. But we pass only about one and a half litres of urine. So about ninety nine percent must be taken back."):
            pass
        reab = VGroup(*[T(s_, size=20, color=c_).move_to(p_) for s_, c_, p_ in [("PCT: all glucose, amino acids; ~70% Na⁺ and water", th.MINT, [-1.9, 2.75, 0]),
                                                                                  ("descending limb: water out", th.SKY, [-3.5, -1.0, 0]), ("ascending limb: Na⁺, Cl⁻ out, NOT water", th.AMBER, [1.0, -3.15, 0]),
                                                                                  ("DCT, duct: water (ADH), Na⁺ (aldosterone)", th.PINK, [3.9, -0.4, 0])]])
        with self.say("Step two: selective reabsorption. The proximal tubule takes back all the glucose and amino acids and most of the salt and water. The descending limb lets water out; the ascending limb pumps salt out but will not let water follow. The distal tubule and collecting duct fine tune, under the control of hormones. Step three, secretion: the tubule adds hydrogen ions, potassium, creatinine and drugs, which is how the kidney controls blood pH."):
            self.play(FadeOut(nfp))
            cap.clear()
            self.play(LaggedStart(*[FadeIn(r_) for r_ in reab], lag_ratio=0.5), run_time=3.0)
        self.play(FadeOut(VGroup(ne, reab, flow)))
        self.remove(flow)
        self.p4_counter()

    def p4_counter(self):
        head = T("The counter-current multiplier", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        grad = VGroup()
        for i in range(10):
            y = 1.6 - 0.42 * i
            grad.add(Rectangle(width=4.6, height=0.42, stroke_width=0, fill_color=interpolate_color(ManimColor("#2A2E55"), ManimColor(th.AMBER), i / 9), fill_opacity=0.55).move_to([-2.2, y, 0]))
        osm = VGroup(T("300", size=22, color=th.INK).next_to(grad[0], LEFT, buff=0.15), T("1200 mOsm/L", size=22, color=th.AMBER).next_to(grad[-1], LEFT, buff=0.15))
        down = Line([-3.0, 1.9, 0], [-3.0, -2.3, 0], color=th.SKY, stroke_width=8)
        up = Line([-1.8, -2.3, 0], [-1.8, 1.9, 0], color=th.AMBER, stroke_width=8)
        bend = ArcBetweenPoints([-3.0, -2.3, 0], [-1.8, -2.3, 0], angle=PI, color=th.MINT, stroke_width=8)
        duct = Line([0.3, 1.9, 0], [0.3, -2.3, 0], color=th.PINK, stroke_width=8)
        w = VGroup(*[Arrow([-3.0, y, 0], [-3.7, y, 0], buff=0, color=th.SKY, stroke_width=3, max_tip_length_to_length_ratio=0.3) for y in (1.0, 0.0, -1.0)])
        s = VGroup(*[Arrow([-1.8, y, 0], [-1.1, y, 0], buff=0, color=th.AMBER, stroke_width=3, max_tip_length_to_length_ratio=0.3) for y in (1.0, 0.0, -1.0)])
        wd = VGroup(*[Arrow([0.3, y, 0], [-0.4, y, 0], buff=0, color=th.PINK, stroke_width=3, max_tip_length_to_length_ratio=0.3) for y in (0.5, -0.5, -1.5)])
        cap = B.Captions(self, at=(3.8, 0.2, 0), width=5.0, size=23)
        with self.say("How does the kidney make urine four times more concentrated than blood? The loop of Henle. The ascending limb pumps salt out into the medulla, but it is waterproof. The descending limb, running the other way right beside it, lets water out into that salty fluid."):
            self.play(FadeIn(head), Create(down), Create(bend), Create(up))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in s], lag_ratio=0.2))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in w], lag_ratio=0.2))
            cap("Ascending: salt out, no water", color=th.AMBER, sub="Descending: water out into the salty medulla.")
        with self.say("Because the two limbs run in opposite directions, a small difference at each level is multiplied down the loop. The medulla builds a gradient from three hundred at the cortex to twelve hundred milliosmoles at the tip. The vasa recta run counter current too, so the blood does not wash the salt away."):
            self.play(LaggedStart(*[FadeIn(g_) for g_ in grad], lag_ratio=0.08), FadeIn(osm), run_time=2.0)
            self.bring_to_front(down, bend, up, w, s)
            cap("Gradient: 300 → 1200 mOsm/L", color=th.AMBER)
        with self.say("Finally the collecting duct runs down through that gradient. When the hormone A D H makes its wall permeable, water leaves by osmosis at every level, and the urine comes out concentrated."):
            self.play(Create(duct), LaggedStart(*[GrowArrow(a_) for a_ in wd], lag_ratio=0.2))
            cap("Collecting duct + ADH → concentrated urine", color=th.PINK, swatch=th.PINK)
        self.play(FadeOut(VGroup(head, grad, osm, down, up, bend, duct, w, s, wd)))
        cap.clear()
        self.worked("Renal blood flow 1200 ml/min, haematocrit 45%, GFR 125 ml/min. Find (i) renal plasma flow, (ii) filtration fraction, (iii) volume filtered in 24 hours.",
                    [r"\text{(i)}\ \ RPF = 1200 \times 0.55 = 660 \text{ ml/min}", r"\text{(ii)}\ \ FF = \tfrac{125}{660} = 0.189 \approx 19\%", r"\text{(iii)}\ \ 125 \times 60 \times 24 = 180\,000 \text{ ml} = 180 \text{ L}"],
                    ["A worked example on filtration.", "Plasma is the part that is not cells: fifty five percent of twelve hundred, six hundred and sixty millilitres a minute.",
                     "Filtration fraction is the share of that plasma which filters: one twenty five over six sixty, about nineteen percent.", "And over a day, one twenty five times sixty times twenty four: one hundred and eighty litres. Of which about one and a half leave as urine."])
        ctl = VGroup(*[para(s_, width=11.5, size=23, color=c_) for s_, c_ in [("ADH: dehydration → more ADH → collecting duct permeable → less, concentrated urine. No ADH: diabetes insipidus.", th.PINK),
                                                                             ("Low BP → JGA releases renin → angiotensin II → aldosterone → Na⁺ and water kept → BP restored. ANF from the atria does the opposite.", th.AMBER),
                                                                             ("Kidney failure: haemodialysis against fluid with NO urea, so urea diffuses out while glucose and salts stay.", th.SKY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.2, 0])
        with self.say("Hormones fine tune it. A D H, from the posterior pituitary, saves water; without it you get diabetes insipidus, litres of dilute urine. When blood pressure falls, the juxtaglomerular apparatus releases renin, leading to angiotensin and aldosterone, which save salt and water and restore the pressure. And when the kidneys fail, dialysis pumps blood past a membrane bathed in fluid that has no urea, so urea diffuses out.") as v:
            for c_ in ctl:
                self.play(FadeIn(c_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.25)
        self.play(FadeOut(ctl))
        self.quiz("The glomerular filtrate formed in a day is about 180 L, but urine is about 1.5 L. This is mainly because of",
                  ["tubular secretion", "selective reabsorption", "ultrafiltration", "the counter-current in the vasa recta"], 1,
                  "Pause and think. Where do the other hundred and seventy eight litres go?",
                  "Selective reabsorption, mostly in the proximal tubule, takes back about ninety nine percent of the filtrate. Secretion adds things to the urine, so it cannot explain the drop.")

    # ------------------------------------------------------------------ part 5: nervous system
    def p5(self):
        self.section(4)
        tree = VGroup(T("nervous system", size=28, color=th.INK, weight="BOLD").move_to([0, 2.3, 0]),
                      T("CNS: brain + spinal cord", size=24, color=th.SKY).move_to([-3.2, 1.2, 0]), T("PNS: 12 cranial + 31 spinal nerve pairs", size=24, color=th.MINT).move_to([3.0, 1.2, 0]),
                      T("somatic: voluntary", size=22, color=th.MINT).move_to([1.4, 0.0, 0]), T("autonomic: involuntary", size=22, color=th.MINT).move_to([4.6, 0.0, 0]),
                      T("sympathetic: fight or flight", size=21, color=th.CORAL).move_to([2.6, -1.3, 0]), T("parasympathetic: rest and digest", size=21, color=th.AMBER).move_to([5.0, -2.1, 0]))
        lines = VGroup(Line([0, 2.05, 0], [-3.2, 1.45, 0], color=th.MUTED), Line([0, 2.05, 0], [3.0, 1.45, 0], color=th.MUTED), Line([3.0, 0.95, 0], [1.4, 0.25, 0], color=th.MUTED),
                       Line([3.0, 0.95, 0], [4.6, 0.25, 0], color=th.MUTED), Line([4.6, -0.25, 0], [2.6, -1.05, 0], color=th.MUTED), Line([4.6, -0.25, 0], [5.0, -1.85, 0], color=th.MUTED))
        with self.say("The nervous system is the fast control system, working in milliseconds along fixed wires. The central nervous system is the brain and spinal cord. The peripheral system is twelve pairs of cranial nerves and thirty one pairs of spinal nerves: somatic for voluntary muscle, and autonomic for the organs, split into sympathetic, fight or flight, and parasympathetic, rest and digest."):
            self.play(FadeIn(tree[0]))
            self.play(Create(lines[:2]), FadeIn(tree[1:3]))
            self.play(Create(lines[2:4]), FadeIn(tree[3:5]))
            self.play(Create(lines[4:]), FadeIn(tree[5:]))
        self.play(FadeOut(VGroup(tree, lines)))
        head = T("The nerve impulse", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 5, 1], y_range=[-90, 50, 30], x_length=7.0, y_length=4.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-2.0, -0.5, 0])
        yl = VGroup(*[T(f"{v} mV", size=18, color=th.MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (-70, -55, 35)])
        thr = DashedLine(ax.c2p(0, -55), ax.c2p(5, -55), color=th.CORAL, stroke_width=2)
        ap = H.action_potential(ax)
        cap = B.Captions(self, at=(4.2, 0.2, 0), width=4.6, size=23)
        with self.say("At rest, the sodium potassium pump throws out three sodium ions for every two potassium it brings in, and the membrane leaks potassium. The inside sits at minus seventy millivolts: polarised."):
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            rest = ap.copy().pointwise_become_partial(ap, 0, 0.2)
            self.play(Create(rest))
            cap("Resting potential −70 mV", sub="Na⁺/K⁺ pump: 3 Na⁺ out, 2 K⁺ in; K⁺ leaks out.")
        with self.say("A stimulus pushes it to the threshold, minus fifty five. Sodium gates fly open, sodium floods in, and the inside shoots to plus thirty five: depolarisation. Then sodium gates close, potassium gates open, potassium rushes out, and the inside goes negative again, overshooting to minus eighty before settling."):
            self.play(Create(thr))
            self.play(Create(ap), run_time=2.4)
            cap("Depolarisation → repolarisation → hyperpolarisation", color=th.AMBER, sub="Na⁺ in to +35 mV; K⁺ out, down to −80 mV; ~1 ms refractory period.")
        with self.say("The all or none law. Below threshold, nothing. At or above it, an impulse of exactly the same size every time. A stronger stimulus does not make a bigger impulse; it makes more impulses per second."):
            cap("All-or-none", color=th.CORAL, sub="Strength is coded by frequency, not by size.")
        self.play(FadeOut(VGroup(head, ax, yl, thr, ap, rest)))
        cap.clear()
        self.worked("A nerve is stimulated at the elbow and the wrist, 33 cm apart. The muscle responds 9.5 ms and 4.0 ms after the two stimuli. Find the conduction velocity. Is the fibre myelinated?",
                    [r"\Delta t = 9.5 - 4.0 = 5.5 \text{ ms}", r"v = \frac{0.33 \text{ m}}{5.5 \times 10^{-3} \text{ s}} = 60 \text{ m/s} \Rightarrow \text{myelinated}"],
                    ["A conduction velocity example from Bharatpur.", "The delay at the muscle is the same for both, so subtracting removes it: five point five milliseconds for thirty three centimetres.",
                     "Zero point three three metres over five point five thousandths of a second: sixty metres per second. Far faster than a bare fibre's one or two: it is myelinated."])
        rows = [["part", "main job"], ["cerebrum", "thought, memory, speech, voluntary action, sensation"], ["thalamus", "relay for all senses except smell"], ["hypothalamus", "temperature, hunger, thirst; controls the pituitary"],
                ["cerebellum", "balance, posture, coordination"], ["pons", "bridge; helps control breathing"], ["medulla oblongata", "vital centres: heartbeat, breathing, BP, swallowing, vomiting"]]
        tb = B.table(rows, [3.4, 8.6], row_h=0.6, size=22, colors=[th.AMBER, th.INK]).move_to([0, 0.3, 0])
        with self.say("The brain, about one point three five kilograms, floating in cerebrospinal fluid inside three meninges. The cerebrum thinks, remembers and moves you. The thalamus relays the senses. The hypothalamus controls temperature, hunger and thirst, and the pituitary. The cerebellum keeps balance. And the medulla runs the vital centres: heartbeat, breathing and blood pressure.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.p5_reflex()

    def p5_reflex(self):
        head = T("The reflex arc", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cord = VGroup(Circle(radius=1.3, stroke_color=th.MUTED, stroke_width=3, fill_color=th.PANEL, fill_opacity=1),
                      VMobject(stroke_width=0, fill_color="#5A4A7A", fill_opacity=1).set_points_smoothly([[0, 0.9, 0], [0.7, 0.6, 0], [0.4, 0, 0], [0.75, -0.7, 0], [0, -0.5, 0], [-0.75, -0.7, 0], [-0.4, 0, 0], [-0.7, 0.6, 0], [0, 0.9, 0]])).move_to([2.6, 0.0, 0])
        skin = Dot([-5.2, 1.6, 0], radius=0.15, color=th.CORAL)
        musc = Ellipse(width=1.0, height=0.5, stroke_width=0, fill_color=OXY, fill_opacity=0.8).move_to([-5.0, -1.8, 0])
        sens = VMobject(stroke_color=th.SKY, stroke_width=5).set_points_smoothly([skin.get_center(), [-2.0, 1.8, 0], [0.8, 1.4, 0], [2.4, 0.5, 0]])
        gang = Dot([0.8, 1.4, 0], radius=0.15, color=th.SKY)
        relay = Line([2.4, 0.5, 0], [2.4, -0.4, 0], color=th.AMBER, stroke_width=5)
        mot = VMobject(stroke_color=th.MINT, stroke_width=5).set_points_smoothly([[2.4, -0.4, 0], [0.8, -1.2, 0], [-2.0, -1.8, 0], musc.get_center() + RIGHT * 0.5])
        labs = VGroup(T("receptor", size=20, color=th.CORAL).next_to(skin, UP, buff=0.1), T("sensory neuron (dorsal root ganglion)", size=20, color=th.SKY).move_to([-1.6, 2.25, 0]),
                      T("relay neuron", size=20, color=th.AMBER).next_to(cord, RIGHT, buff=0.15), T("motor neuron", size=20, color=th.MINT).move_to([-1.6, -2.3, 0]), T("effector", size=20, color=OXY).next_to(musc, DOWN, buff=0.1))
        imp = Dot(radius=0.12, color=WHITE)
        with self.say("Touch a hot tawa and your hand jerks away before you feel the pain. That is a reflex: rapid, automatic, involuntary. Its path, the reflex arc, has five parts: a receptor, a sensory neuron into the spinal cord, a relay neuron, a motor neuron, and an effector muscle."):
            self.play(FadeIn(head), FadeIn(cord), FadeIn(skin), FadeIn(musc))
            self.play(Create(sens), FadeIn(gang), Create(relay), Create(mot), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.2))
        with self.say("Watch the impulse. Skin, into the dorsal horn, across the relay neuron, out through the ventral root, to the muscle. About twenty milliseconds. A branch also climbs to the brain, which is why you feel the pain only after your hand has moved. The brain is informed, but not consulted."):
            self.add(imp.move_to(skin))
            self.play(MoveAlongPath(imp, sens), run_time=1.0, rate_func=rate_functions.linear)
            self.play(MoveAlongPath(imp, relay), run_time=0.4, rate_func=rate_functions.linear)
            self.play(MoveAlongPath(imp, mot), run_time=1.0, rate_func=rate_functions.linear)
            self.play(musc.animate.stretch(0.7, 0), run_time=0.3)
        self.play(FadeOut(VGroup(head, cord, skin, musc, sens, gang, relay, mot, labs, imp)))
        self.tip("A spinal reflex is decided in the SPINAL CORD — the impulse does not 'go to the brain and come back'. The knee jerk is monosynaptic: no relay neuron.",
                 "Exam tip. In a spinal reflex the decision is made in the spinal cord. Never write that the impulse goes to the brain and comes back. And the knee jerk is monosynaptic: the sensory neuron connects straight to the motor neuron, with no relay neuron.")

    # ------------------------------------------------------------------ part 6: sense organs
    def p6(self):
        self.section(5)
        e = H.eye(3.6, 1.0).move_to([-3.0, 0.2, 0])
        lab = VGroup(T("cornea, lens: focus", size=20, color=th.SKY).move_to([-5.6, 1.7, 0]), T("retina: rods + cones", size=20, color=th.CORAL).move_to([-0.6, 1.7, 0]))
        rods = VGroup(T("rods ~120 million", size=24, color=th.MUTED, weight="BOLD"), T("rhodopsin · dim light · black and white", size=20, color=th.BODY),
                      T("cones ~6–7 million", size=24, color=th.AMBER, weight="BOLD"), T("iodopsin · bright light · colour · packed in the fovea", size=20, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 0.6, 0])
        va = para("No vitamin A → no rhodopsin → night blindness. Blind spot: where the optic nerve leaves, no receptors.", width=5.4, size=21, color=th.CORAL).move_to([3.6, -1.4, 0])
        with self.say("The eye. A tough sclera, clear in front as the cornea; a dark choroid; and the light sensitive retina. The retina has about a hundred and twenty million rods, with the pigment rhodopsin, for dim light in black and white, and six or seven million cones, with iodopsin, for bright light and colour, crowded in the yellow spot. Where the optic nerve leaves there are no receptors: the blind spot. And without vitamin A, rhodopsin cannot be made: night blindness, still a real problem in the Terai."):
            self.play(FadeIn(e), FadeIn(lab))
            self.play(FadeIn(rods, shift=LEFT * 0.2))
            self.play(FadeIn(va))
        self.play(FadeOut(VGroup(e, lab, rods, va)))
        self.p6_defects()
        self.p6_ear()

    def p6_defects(self):
        head = T("Defects of the eye", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)

        def case(y, L, focus_x, lens=None, fix_col=th.MINT):
            e = H.eye(L, 0.9).move_to([0.5, y, 0])
            lx = e[1].get_center()[0]
            rays = VGroup(*[VMobject(stroke_color=th.AMBER, stroke_width=3).set_points_as_corners([[-5.0, y + d, 0], [lx, y + d, 0], [focus_x, y, 0]]) for d in (-0.45, 0.45)])
            g = VGroup(e, rays)
            if lens == "concave":
                g.add(VGroup(ArcBetweenPoints([-2.2, y + 0.7, 0], [-2.2, y - 0.7, 0], angle=0.5, color=fix_col, stroke_width=5), ArcBetweenPoints([-1.95, y - 0.7, 0], [-1.95, y + 0.7, 0], angle=0.5, color=fix_col, stroke_width=5)))
            elif lens == "convex":
                g.add(Ellipse(width=0.35, height=1.4, stroke_color=fix_col, stroke_width=5).move_to([-2.1, y, 0]))
            return g

        my = case(1.1, 4.2, 0.5 + 4.2 * 0.9 / 2 - 0.6)
        hy = case(-1.6, 2.8, 0.5 + 2.8 * 0.9 / 2 + 0.6)
        l1 = VGroup(T("myopia (short sight)", size=24, color=th.CORAL, weight="BOLD"), T("eyeball too long; image in front of retina", size=19, color=th.BODY), T("fix: concave lens", size=20, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 1.1, 0])
        l2 = VGroup(T("hypermetropia (long sight)", size=24, color=th.CORAL, weight="BOLD"), T("eyeball too short; image behind retina", size=19, color=th.BODY), T("fix: convex lens", size=20, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, -1.6, 0])
        with self.say("Two defects follow straight from geometry. In myopia, short sight, the eyeball is too long, so distant objects focus in front of the retina; a concave, diverging lens fixes it. In hypermetropia, long sight, the eyeball is too short and the image would fall behind the retina; a convex, converging lens fixes it."):
            self.play(FadeIn(head), FadeIn(my), FadeIn(l1))
            self.play(FadeIn(hy), FadeIn(l2))
        oth = para("Also: presbyopia (stiff lens with age), astigmatism (unevenly curved cornea), cataract (opaque lens, replaced). Accommodation: ciliary muscle contracts → lens rounder → near focus.", width=12, size=21, color=th.MUTED).move_to([0, -3.0, 0])
        with self.say("Add presbyopia, the stiffening lens of age; astigmatism, an unevenly curved cornea; and cataract, a lens gone cloudy. Focusing on near objects, accommodation, happens when the ciliary muscle contracts, the ligaments slacken, and the elastic lens rounds up."):
            self.play(FadeIn(oth))
        self.play(FadeOut(VGroup(head, my, hy, l1, l2, oth)))

    def p6_ear(self):
        head = T("The ear: hearing and balance", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        parts = [("pinna", th.BODY), ("ear drum", th.PINK), ("malleus", th.AMBER), ("incus", th.AMBER), ("stapes", th.AMBER), ("oval window", th.SKY), ("cochlea: organ of Corti", th.MINT), ("auditory nerve", th.CORAL)]
        chain = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.1, width=1.4, height=0.75, stroke_color=c_, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1), para(n_, width=1.3, size=17, color=c_, align="center")) for n_, c_ in parts])
        for c_ in chain:
            c_[1].move_to(c_[0])
        chain.arrange(RIGHT, buff=0.18).move_to([0, 1.2, 0])
        wave = Dot(radius=0.12, color=WHITE).move_to(chain[0].get_center())
        amp = T("the ossicles amplify about 20×", size=22, color=th.AMBER).next_to(chain[2:5], DOWN, buff=0.25)
        with self.say("Sound collected by the pinna vibrates the ear drum. Three tiny bones, the malleus, incus and stapes, the smallest in the body, act as levers and amplify the vibration about twenty times. The stapes pushes on the oval window, sending waves through the fluid of the cochlea, where hair cells in the organ of Corti turn them into nerve impulses. We hear from twenty to twenty thousand hertz."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in chain], lag_ratio=0.1))
            self.add(wave)
            for c_ in chain[1:]:
                self.play(wave.animate.move_to(c_.get_center()), run_time=0.3)
            self.play(FadeIn(amp))
        bal = VGroup(T("Eustachian tube: equalises pressure on the drum (ears pop on the way to Muktinath)", size=22, color=th.SKY),
                     T("semicircular canals (3 planes): rotation — dynamic balance", size=22, color=th.MINT), T("utriculus and sacculus with otoliths: head position — static balance", size=22, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.5, 0])
        for b_ in bal:
            if b_.width > 12.4:
                b_.scale_to_fit_width(12.4)
        with self.say("The Eustachian tube links the middle ear to the throat and equalises pressure, which is why your ears pop on the drive up to Muktinath. And the inner ear also balances you: three semicircular canals at right angles sense rotation, while the utriculus and sacculus, with their tiny stones, sense which way is up."):
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in bal], lag_ratio=0.3))
        self.play(FadeOut(VGroup(head, chain, wave, amp, bal)))
        self.quiz("Myopia (short sight) is corrected using a",
                  ["convex lens", "concave lens", "cylindrical lens", "bifocal lens"], 1,
                  "Pause and think. A short sighted eye focuses too early. Which lens?",
                  "A concave, diverging lens: it spreads the rays slightly so the image moves back onto the retina. A convex lens is for hypermetropia, and a cylindrical lens corrects astigmatism.")

    # ------------------------------------------------------------------ part 7: endocrinology
    def p7(self):
        self.section(6)
        rows = [["", "nervous", "endocrine"], ["message", "electrical impulse", "chemical hormone in blood"], ["route", "fixed wire to one target", "whole bloodstream"], ["speed", "milliseconds", "seconds to hours"], ["effect lasts", "very briefly", "long, even lifelong"]]
        tb = B.table(rows, [2.6, 4.2, 4.8], row_h=0.62, size=23, colors=[th.MUTED, th.SKY, th.AMBER]).move_to([0, 1.2, 0])
        chem = para("Hormones: peptides (insulin, GH, ADH) bind surface receptors and act via a second messenger (cAMP); steroids (cortisol, testosterone) pass through the membrane and act on genes; amine derivatives (thyroxine, adrenaline).", width=11.8, size=22, color=th.BODY).move_to([0, -2.0, 0])
        with self.say("The endocrine system is the slow but far reaching control system. Ductless glands pour hormones into the blood, which carries them to any cell with the right receptor. Slower than nerves, but the effects last much longer. Peptide hormones like insulin bind a receptor on the surface and work through a second messenger such as cyclic A M P; steroid hormones pass straight through the membrane and act on the genes.") as v:
            B.reveal_table(self, tb, v.dur * 0.55)
            self.play(FadeIn(chem))
        self.play(FadeOut(VGroup(tb, chem)))
        self.p7_pituitary()
        self.p7_glands()
        self.p7_glucose()

    def p7_pituitary(self):
        head = T("The pituitary: the master gland, under the hypothalamus", size=28, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        hyp = RoundedRectangle(corner_radius=0.3, width=2.6, height=0.8, stroke_color=th.PINK, stroke_width=3, fill_color=th.PINK, fill_opacity=0.15).move_to([-2.6, 1.9, 0])
        stalk = Line([-2.6, 1.5, 0], [-2.6, 0.9, 0], color=th.PINK, stroke_width=6)
        ant = Ellipse(width=1.7, height=1.1, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.2).move_to([-3.45, 0.4, 0])
        post = Ellipse(width=1.5, height=1.0, stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.2).move_to([-1.85, 0.4, 0])
        l0 = VGroup(T("hypothalamus", size=22, color=th.PINK).move_to(hyp), T("anterior", size=18, color=th.SKY).move_to(ant), T("posterior", size=18, color=th.AMBER).move_to(post))
        ah = VGroup(*[T(s_, size=21, color=th.SKY) for s_ in ["GH: growth (dwarfism / gigantism, acromegaly)", "TSH → thyroid", "ACTH → adrenal cortex", "FSH: follicles; sperm", "LH (ICSH): ovulation; testosterone", "prolactin: milk secretion"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, 0.9, 0])
        ph = VGroup(*[para(s_, width=5.6, size=21, color=th.AMBER) for s_ in ["ADH: water reabsorption (diabetes insipidus)", "oxytocin: labour, milk ejection (positive feedback)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -1.6, 0])
        nt = para("The posterior lobe makes nothing: it stores and releases two hormones made in the hypothalamus.", width=3.6, size=20, color=th.MUTED).move_to([-4.4, -1.7, 0])
        with self.say("The pituitary is pea sized, hanging from the hypothalamus. Its anterior lobe is true glandular tissue, controlled by releasing hormones from the hypothalamus through a private portal blood supply. It makes six hormones, and the board expects all six: growth hormone, T S H for the thyroid, A C T H for the adrenal cortex, F S H and L H for the gonads, and prolactin for milk.") as v:
            self.play(FadeIn(head), FadeIn(hyp), Create(stalk), FadeIn(ant), FadeIn(post), FadeIn(l0))
            for a_ in ah:
                self.play(FadeIn(a_, shift=LEFT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.06)
        with self.say("The posterior lobe makes nothing at all. It only stores and releases two hormones made in the hypothalamus: A D H, which saves water in the kidney, and oxytocin, which drives labour and milk ejection, the classic example of positive feedback."):
            self.play(FadeIn(ph, shift=LEFT * 0.2), FadeIn(nt))
        self.play(FadeOut(VGroup(head, hyp, stalk, ant, post, l0, ah, ph, nt)))
        head = T("Negative feedback: the thyroid thermostat", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        nodes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.2, width=3.3, height=0.8, stroke_color=c_, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), T(n_, size=22, color=c_)).move_to(p_)
                         for n_, c_, p_ in [("hypothalamus: TRH", th.PINK, [0, 1.9, 0]), ("pituitary: TSH", th.SKY, [4.2, 0, 0]), ("thyroid: T₄", th.AMBER, [0, -1.9, 0]), ("body cells: BMR ↑", th.MINT, [-4.2, 0, 0])]])
        for n_ in nodes:
            n_[1].move_to(n_[0])
        arr = VGroup(*[CurvedArrow(nodes[i].get_center() + (nodes[(i + 1) % 4].get_center() - nodes[i].get_center()) * 0.38, nodes[(i + 1) % 4].get_center() - (nodes[(i + 1) % 4].get_center() - nodes[i].get_center()) * 0.38, angle=-0.4, color=th.MUTED, stroke_width=3) for i in range(3)])
        neg = DashedVMobject(CurvedArrow([-0.4, -1.45, 0], [-0.4, 1.45, 0], angle=-0.5, color=th.CORAL, stroke_width=4), num_dashes=14)
        nl = para("high T₄ switches TRH and TSH off", width=2.4, size=21, color=th.CORAL).move_to([0.9, 0, 0])
        with self.say("Most hormones are held steady by negative feedback. The hypothalamus releases T R H, the pituitary releases T S H, the thyroid makes thyroxine, which raises the metabolic rate. And when thyroxine is high, it switches off the hypothalamus and pituitary. Like a thermostat."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.3))
            self.play(LaggedStart(*[Create(a_) for a_ in arr], lag_ratio=0.3))
            self.play(Create(neg), FadeIn(nl))
        gt = para("Iodine lack → no T₄ → TSH never switched off → thyroid swells: simple goitre. Hypo in infancy: cretinism; in adults: myxoedema. Hyper: Graves' disease.", width=12.6, size=20, color=th.AMBER).move_to([0, -2.95, 0])
        with self.say("Break the loop and you see the diseases. With no iodine, thyroxine cannot be made, so T S H is never switched off and keeps whipping the thyroid, which swells: simple goitre. Too little thyroxine in a baby causes cretinism; in an adult, myxoedema. Too much causes Graves' disease, with bulging eyes."):
            self.play(FadeIn(gt))
        self.play(FadeOut(VGroup(head, nodes, arr, neg, nl, gt)))

    def p7_glands(self):
        rows = [["gland", "hormone", "effect", "disorder"], ["parathyroid", "parathormone", "raises blood Ca²⁺", "low: tetany"], ["thyroid C cells", "calcitonin", "lowers blood Ca²⁺", ""],
                ["adrenal cortex", "aldosterone", "keeps Na⁺ and water", "excess: Conn's"], ["adrenal cortex", "cortisol", "raises glucose; anti-inflammatory", "excess: Cushing's"], ["adrenal cortex", "(all low)", "", "Addison's: bronzed skin"],
                ["adrenal medulla", "adrenaline", "fight or flight: heart, glucose, BP up", ""], ["pineal", "melatonin", "sleep–wake rhythm", ""], ["thymus", "thymosin", "T-cells mature", ""]]
        tb = B.table(rows, [2.8, 2.6, 4.4, 3.0], row_h=0.56, size=21, colors=[th.AMBER, th.INK, th.BODY, th.CORAL]).move_to([0, 0.2, 0])
        with self.say("The other glands, in one table. Parathormone raises blood calcium, calcitonin lowers it. The adrenal cortex makes aldosterone, which keeps salt and water, and cortisol, which raises blood sugar and calms inflammation. Too much cortisol is Cushing's syndrome; too little of everything is Addison's disease. The adrenal medulla makes adrenaline for fight or flight. The pineal makes melatonin for sleep, and the thymus matures T cells.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))

    def p7_glucose(self):
        head = T("Keeping blood glucose at 70–110 mg per 100 ml", size=28, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        g = ValueTracker(90)
        ax = NumberLine(x_range=[40, 220, 20], length=10, color=th.MUTED, include_numbers=True, font_size=22).move_to([0, 0.5, 0])
        band = Rectangle(width=ax.n2p(110)[0] - ax.n2p(70)[0], height=0.5, stroke_width=0, fill_color=th.MINT, fill_opacity=0.25).move_to((ax.n2p(70) + ax.n2p(110)) / 2)
        thr = VGroup(DashedLine(ax.n2p(180) + DOWN * 0.4, ax.n2p(180) + UP * 0.8, color=th.CORAL), T("renal threshold 180", size=20, color=th.CORAL).next_to(ax.n2p(180) + UP * 0.8, UP, buff=0.05))
        mk = always_redraw(lambda: Triangle(fill_color=th.AMBER, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI).next_to(ax.n2p(g.get_value()), UP, buff=0.05))
        ins = VGroup(T("β cells: INSULIN", size=26, color=th.SKY, weight="BOLD"), T("glucose into cells; glycogen made", size=20, color=th.BODY)).arrange(DOWN, buff=0.08).move_to([-3.2, -1.6, 0])
        glu = VGroup(T("α cells: GLUCAGON", size=26, color=th.AMBER, weight="BOLD"), T("glycogen broken down; glucose released", size=20, color=th.BODY)).arrange(DOWN, buff=0.08).move_to([3.2, -1.6, 0])
        with self.say("The islets of Langerhans in the pancreas hold blood glucose steady. After a meal glucose rises, and beta cells release insulin, which lets glucose into cells and stores it as glycogen. It falls back."):
            self.play(FadeIn(head), Create(ax), FadeIn(band), FadeIn(thr))
            self.add(mk)
            self.play(g.animate.set_value(150), run_time=1.2)
            self.play(FadeIn(ins))
            self.play(g.animate.set_value(95), run_time=1.4)
        with self.say("When you fast, glucose falls, and alpha cells release glucagon, which breaks glycogen down and puts glucose back. Glucagon, adrenaline, cortisol and growth hormone can all raise blood sugar. Only insulin lowers it."):
            self.play(g.animate.set_value(65), run_time=1.0)
            self.play(FadeIn(glu))
            self.play(g.animate.set_value(90), run_time=1.2)
        dm = para("No insulin (or tissues ignoring it): diabetes mellitus. Glucose climbs past 180, spills into urine (glycosuria), drags water with it: thirst, much urine, weight loss.", width=11.5, size=22, color=th.CORAL).move_to([0, -3.0, 0])
        with self.say("Without insulin, or when the body ignores it, that is diabetes mellitus. Glucose climbs past the kidney's threshold of one hundred and eighty, spills into the urine, and drags water with it."):
            self.play(g.animate.set_value(210), run_time=1.6)
            self.play(FadeIn(dm))
        self.play(FadeOut(VGroup(head, ax, band, thr, ins, glu, dm)), FadeOut(mk))
        self.remove(mk)
        self.quiz("Which hormone LOWERS blood glucose?",
                  ["glucagon", "adrenaline", "insulin", "cortisol"], 2,
                  "Pause and think. Only one of these lowers blood sugar. Which?",
                  "Insulin, from the beta cells. Glucagon, adrenaline and cortisol all raise blood glucose, which is exactly why losing the one lowering hormone causes a disease as serious as diabetes.")

    # ------------------------------------------------------------------ part 8: reproduction
    def p8(self):
        self.section(7)
        male = VGroup(*[T(s_, size=21, color=c_) for s_, c_ in [("testes in the scrotum: 2–2.5 °C below body temperature", th.SKY), ("seminiferous tubules: sperm; Leydig cells: testosterone", th.SKY),
                                                                 ("epididymis (stores, matures) → vas deferens → urethra", th.BODY), ("seminal vesicles (fructose) · prostate · Cowper's glands", th.BODY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        female = VGroup(*[T(s_, size=21, color=c_) for s_, c_ in [("ovaries: oocytes + oestrogen, progesterone", th.PINK), ("Fallopian tube: fimbriae catch the egg; fertilisation in the ampulla", th.PINK),
                                                                   ("uterus: endometrium for implantation", th.BODY), ("cervix → vagina", th.BODY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        hm = T("male", size=28, color=th.SKY, weight="BOLD")
        hf = T("female", size=28, color=th.PINK, weight="BOLD")
        cm = VGroup(hm, male).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cf = VGroup(hf, female).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        both = VGroup(cm, cf).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.2, 0])
        if both.height > 5.3:
            both.scale_to_fit_height(5.3).move_to([0, -0.2, 0])
        for t_ in [*male, *female]:
            if t_.width > 12.4:
                t_.scale_to_fit_width(12.4)
        with self.say("The male system. The testes hang in the scrotum, two degrees cooler than the body, because sperm cannot be made at body temperature. Seminiferous tubules make sperm; the Leydig cells between them make testosterone. Sperm mature in the epididymis and travel through the vas deferens, joined by fluid from the seminal vesicles, rich in fructose for energy, and from the prostate.") as v:
            self.play(FadeIn(hm))
            for m_ in male:
                self.play(FadeIn(m_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.15)
        with self.say("The female system. The ovaries make oocytes and the hormones oestrogen and progesterone. Finger like fimbriae of the Fallopian tube sweep the released egg in, and fertilisation happens in its widest part, the ampulla. The uterus, with its lining the endometrium, receives the embryo."):
            self.play(FadeIn(hf))
            for f_ in female:
                self.play(FadeIn(f_, shift=RIGHT * 0.2), run_time=0.4)
        self.play(FadeOut(both))
        self.p8_cycle()

    def p8_cycle(self):
        head = T("The menstrual cycle: four hormones, 28 days", size=28, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 28, 7], y_range=[0, 1.1, 0.5], x_length=9.0, y_length=3.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-1.0, 0.0, 0])
        days = VGroup(*[T(str(d), size=18, color=th.MUTED).next_to(ax.c2p(d, 0), DOWN, buff=0.1) for d in (1, 7, 14, 21, 28)])
        cur = H.hormone_curves(ax)
        leg = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c_, stroke_width=5), T(n_, size=20, color=c_)).arrange(RIGHT, buff=0.12) for n_, c_ in [("FSH", th.SKY), ("LH", th.AMBER), ("oestrogen", th.PINK), ("progesterone", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.0, 0.6, 0])
        phases = [(0, 5, "menstrual", th.CORAL), (5, 13, "proliferative", th.SKY), (13, 15, "ovulation", th.AMBER), (15, 28, "secretory", th.MINT)]
        pb = VGroup()
        for a, b, n_, c_ in phases:
            r = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=0.35, stroke_width=0, fill_color=c_, fill_opacity=0.5).move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, -2.4, 0])
            pb.add(VGroup(r, T(n_, size=16, color=th.INK).move_to(r)))
        with self.say("From menarche, at about twelve, to menopause, around fifty, a twenty eight day cycle repeats. Days one to five, menstruation: the lining from the last cycle is shed, because progesterone has collapsed."):
            self.play(FadeIn(head), Create(ax), FadeIn(days), FadeIn(leg))
            self.play(FadeIn(pb[0]))
        with self.say("Days six to thirteen, the proliferative phase. F S H ripens a Graafian follicle, which pours out oestrogen, and oestrogen rebuilds the lining."):
            self.play(Create(cur[0]), Create(cur[2]), FadeIn(pb[1]), run_time=2.0)
        with self.say("Around day fourteen, high oestrogen triggers a sudden surge of L H. The follicle bursts and releases the secondary oocyte: ovulation."):
            self.play(Create(cur[1]), FadeIn(pb[2]), run_time=1.6)
            self.play(Flash(ax.c2p(13.8, 0.97), color=th.AMBER))
        with self.say("Days fifteen to twenty eight, the secretory phase. The empty follicle becomes the yellow corpus luteum, whose progesterone makes the lining thick and ready. If no embryo arrives, the corpus luteum dies, progesterone falls, and the cycle starts again."):
            self.play(Create(cur[3]), FadeIn(pb[3]), run_time=2.0)
        self.play(FadeOut(VGroup(head, ax, days, cur, leg, pb)))
        fl = self.callout("careful", "The egg lives about 24 hours after ovulation, but sperm survive 3–5 days, so the fertile window is roughly days 10–17 of a 28-day cycle — not day 14 alone.", width=11, size=25)
        with self.say("A careful point. The egg survives only about a day after ovulation, but sperm can survive three to five days. So the fertile window is roughly days ten to seventeen, not day fourteen alone."):
            self.play(FadeIn(fl, shift=UP * 0.2))
        self.play(FadeOut(fl))
        steps = VGroup(*[T(s_, size=24, color=th.INK) for s_ in ["fertilisation in the ampulla, within 24 hours of ovulation", "zygote → morula → blastocyst while moving down the tube",
                                                                  "implantation 6–7 days after fertilisation", "gestation about 280 days (40 weeks) from the last period"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.3, 0])
        with self.say("If a sperm meets the egg, fertilisation happens in the ampulla. The zygote divides as it drifts down the tube, becoming a morula, then a hollow blastocyst, which implants in the endometrium six or seven days later. Pregnancy lasts about two hundred and eighty days, counted from the last period.") as v:
            for s_ in steps:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(v.dur * 0.18)
        self.play(FadeOut(steps))
        self.worked("Menarche at 13, menopause at 49, one ovulation every 28 days, two pregnancies each removing 10 months of cycling. Estimate the ova released, and what fraction of about 1 million oocytes that is.",
                    [r"(49-13)\times365 = 13\,140 \text{ days}", r"13\,140 - 2\times10\times30 = 12\,540 \text{ days}", r"\frac{12\,540}{28} \approx 448 \text{ ova};\quad \frac{448}{10^6} \approx 0.045\%"],
                    ["A worked example.", "Thirty six reproductive years is thirteen thousand one hundred and forty days.", "Take away twenty months of pregnancy, about six hundred days: twelve thousand five hundred and forty.",
                     "Divide by twenty eight: about four hundred and forty eight eggs. Less than one in two thousand of the oocytes she was born with. The rest simply degenerate."])
        self.quiz("Ovulation is triggered by a sudden surge of",
                  ["FSH", "LH", "progesterone", "prolactin"], 1,
                  "Last one. Which hormone surges to trigger ovulation?",
                  "L H. High oestrogen from the ripening follicle triggers the L H surge, and the follicle bursts. F S H is the trap: it ripens the follicle, but the surge that releases the egg is L H.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Digestion: enzymes per food; bile emulsifies; villi absorb (sugars to blood, fats to lacteal).",
            "Breathing is Boyle's law; VC = TV + IRV + ERV; Bohr effect unloads O₂ in active tissue.",
            "Double, closed circulation; SA node pacemaker; CO = SV × HR; P–QRS–T.",
            "Nephron: filter 180 L/day, reabsorb 99%; loop of Henle concentrates; ADH saves water.",
            "Impulse: −70 → +35 mV, all-or-none; myelin speeds it; reflex arc has five parts.",
            "Pituitary's six + two hormones; negative feedback; only insulin lowers glucose; LH surge → ovulation.",
        ], "Quick recap. Each food has its enzymes, bile only emulsifies, and villi absorb, sugars into blood and fats into the lacteals. Breathing is Boyle's law, and the Bohr effect unloads oxygen where it is needed. The circulation is double and closed, paced by the S A node, with cardiac output equal to stroke volume times rate. Nephrons filter one hundred and eighty litres a day and take back ninety nine percent. The impulse jumps from minus seventy to plus thirty five, all or none. And hormones work by feedback: only insulin lowers blood sugar, and an L H surge triggers ovulation.")
        self.outro("That was human biology, the heart of zoology. Next: human population and the disorders that threaten our health. See you there.")
