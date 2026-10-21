import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402
from _bio import XYL, PHL, CAMB, CORK, SCL, COL, PAR, PARF, EPI, ENDO, PERI, PITH, CHL, WATER, FOOD  # noqa: E402

SGC = np.array([-2.75, 0.0, 0])
BUNDLES = [TAU * k / 8 + PI / 8 for k in range(8)]
HALF = 0.22
RP, RX0, STEP = 0.52, 0.8, 0.36
WOOD = "#2A6C8C"
LATE = "#123F57"
HEART = "#6B3E1F"
SAP = "#E3C58F"


def sg_geom(t):
    rx = RX0 + STEP * t
    rc = rx + 0.02
    tp = 0.07 * t
    ph_in = rc + tp + 0.03
    pth = 0.17 / (1 + 1.3 * t)
    ph_out = ph_in + pth
    rout = ph_out + 0.46 - 0.04 * min(t, 4)
    return dict(rx=rx, rc=rc, tp=tp, ph_in=ph_in, pth=pth, ph_out=ph_out, rout=rout)


def sg_frame(t, z=1.0, f=1.0, k=0.0, rays=0.0, center=SGC):
    """The dicot stem in transverse section after t years of secondary growth (t = 0: primary stem).
    z: zoom, f: how far the interfascicular cambium has grown (0..1), k: cork cambium activity (0..1),
    rays: highlight of the medullary-ray parenchyma between the bundles."""
    G = sg_geom(t)
    S = lambda r: r * z
    g = VGroup()
    ck = 0.2 * k
    rk = G["rout"] - 0.13
    outer = G["rout"] + ck
    g.add(Circle(radius=S(outer), stroke_width=0, fill_color=PARF, fill_opacity=1))
    g.add(Circle(radius=S(RP), stroke_width=0, fill_color="#22284A", fill_opacity=1))
    if rays > 0:
        for a in BUNDLES:
            g.add(AnnularSector(inner_radius=S(RP), outer_radius=S(G["ph_out"] + 0.04), angle=TAU / 8 - 2 * HALF, start_angle=a + HALF,
                                stroke_width=0, fill_color=PAR, fill_opacity=0.45 * rays))
    if t > 0:
        g.add(Annulus(inner_radius=S(RX0), outer_radius=S(G["rx"]), stroke_width=0, fill_color=WOOD, fill_opacity=0.9))
        for kk in range(1, int(t + 1e-6) + 1):
            r = RX0 + STEP * kk
            g.add(Annulus(inner_radius=S(r - 0.075), outer_radius=S(r), stroke_width=0, fill_color=LATE, fill_opacity=1))
        if t > 0.25:
            for j in range(16):
                a = TAU * j / 16 + PI / 16
                g.add(Line(polar(S(RX0 + 0.02), a), polar(S(G["rx"] - 0.02), a), stroke_width=1.6, color=PAR, stroke_opacity=min(1, t)))
        g.add(Annulus(inner_radius=S(G["rc"]), outer_radius=S(G["rc"] + G["tp"]), stroke_width=0, fill_color=PHL, fill_opacity=0.55))
    for a in BUNDLES:
        g.add(AnnularSector(inner_radius=S(RP + 0.02), outer_radius=S(RX0), angle=2 * HALF, start_angle=a - HALF, stroke_width=0, fill_color=XYL, fill_opacity=0.95))
        op = max(0.25, 1 - 0.18 * t)
        g.add(AnnularSector(inner_radius=S(G["ph_in"]), outer_radius=S(G["ph_out"]), angle=2 * HALF * (1 + 0.08 * t), start_angle=a - HALF * (1 + 0.08 * t),
                            stroke_width=0, fill_color=PHL, fill_opacity=op))
    if f >= 0.999:
        g.add(Circle(radius=S(G["rc"]), stroke_color=CAMB, stroke_width=5))
    else:
        gap = TAU / 8 - 2 * HALF
        for a in BUNDLES:
            g.add(Arc(radius=S(G["rc"]), start_angle=a - HALF, angle=2 * HALF, stroke_color=CAMB, stroke_width=5))
            if f > 0.01:
                g.add(Arc(radius=S(G["rc"]), start_angle=a + HALF, angle=gap * f / 2, stroke_color="#FFD99A", stroke_width=5))
                g.add(Arc(radius=S(G["rc"]), start_angle=a + TAU / 8 - HALF, angle=-gap * f / 2, stroke_color="#FFD99A", stroke_width=5))
    if k > 0:
        g.add(Annulus(inner_radius=S(rk - 0.05 * k), outer_radius=S(rk), stroke_width=0, fill_color="#3E7A4A", fill_opacity=1))
        g.add(Annulus(inner_radius=S(rk), outer_radius=S(rk + ck), stroke_width=0, fill_color=CORK, fill_opacity=1))
        for j in range(1, int(ck / 0.04) + 1):
            g.add(Circle(radius=S(rk + 0.04 * j), stroke_color="#7A5534", stroke_width=1.2))
        g.add(Circle(radius=S(rk), stroke_color="#FFE2B8", stroke_width=3))
    epi_r = outer
    fade = 1 - 0.75 * k
    if t > 2.3 or k > 0:
        n = 9
        gapa = min(0.32, 0.1 * (t - 2.3) + 0.3 * k)
        for j in range(n):
            a0 = TAU * j / n + 0.2
            g.add(Arc(radius=S(epi_r), start_angle=a0 + gapa / 2, angle=TAU / n - gapa, stroke_color=EPI, stroke_width=6, stroke_opacity=fade))
    else:
        g.add(Circle(radius=S(epi_r), stroke_color=EPI, stroke_width=6))
    return g.shift(center)


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 1
    TITLE = "Plant Anatomy"
    SUBTITLE = "What a plant looks like from the inside"
    SECTIONS = ["Concept of tissues", "Meristems and permanent tissues", "Dicot and monocot root",
                "Dicot and monocot stem", "Dicot and monocot leaf", "Secondary growth of dicot stem"]
    NEXT = "Unit 2 · Plant Physiology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ground = Line([-6.8, -2.8, 0], [6.8, -2.8, 0], color=th.FAINT, stroke_width=3)
        yrs = ValueTracker(0.0)

        def sal():
            y = yrs.get_value()
            w = 0.16 + 0.036 * y
            h = 0.6 + min(y, 25) * 0.13
            x = 2.6
            trunk = Polygon([x - w, -2.8, 0], [x + w, -2.8, 0], [x + w * 0.45, -2.8 + h, 0], [x - w * 0.45, -2.8 + h, 0], stroke_width=0, fill_color="#7A5534", fill_opacity=1)
            cr = 0.3 + 0.025 * min(y, 30)
            crown = VGroup(*[Circle(radius=cr * s_, fill_color="#2E7D32", fill_opacity=0.95, stroke_width=0).move_to([x + dx * cr, -2.8 + h + dy * cr, 0])
                             for s_, dx, dy in [(1.0, 0, 0.6), (0.75, -0.9, 0.2), (0.8, 0.9, 0.25)]])
            return VGroup(trunk, crown)

        def bamboo():
            y = yrs.get_value()
            n = int(min(9, 1 + y * 8))
            g = VGroup()
            for i in range(n):
                g.add(Rectangle(width=0.36, height=0.62, stroke_color="#A7D36B", stroke_width=2.5, fill_color="#5E8C2E", fill_opacity=1).move_to([-2.6, -2.49 + 0.64 * i, 0]))
            return g

        S, Bm = always_redraw(sal), always_redraw(bamboo)
        lab_s = T("sal (Shorea robusta)", size=24, color="#C9A27A").move_to([2.6, -3.2, 0])
        lab_b = T("bamboo (bans)", size=24, color="#A7D36B").move_to([-2.6, -3.2, 0])
        cnt = VGroup(T("years", size=22, color=th.MUTED), Integer(0, font_size=54, color=th.INK)).arrange(DOWN, buff=0.05).move_to([0, 2.6, 0])
        cnt[1].add_updater(lambda m: m.set_value(int(yrs.get_value())))
        with self.say("A forest in Chitwan. Two plants side by side: a bamboo, and a young sal tree. In a single season the bamboo shoots up to its full height. The sal is slow."):
            self.play(Create(ground), FadeIn(lab_s), FadeIn(lab_b))
            self.add(S, Bm)
            self.play(FadeIn(cnt))
            self.play(yrs.animate.set_value(1.0), run_time=2.5)
        with self.say("Now let forty years go by. Watch the sal trunk. Every year it gets thicker, until it is wider than your arms can reach around. And the bamboo? It came out of the ground as wide as it would ever be, and it never gets any thicker.") as v:
            self.play(yrs.animate.set_value(40.0), run_time=v.dur * 0.85, rate_func=rate_functions.ease_in_out_sine)
        cnt[1].clear_updaters()
        nb = B.neby_in(self, "think", height=1.4, at=[0, 0.4, 0])
        with self.say("Both are green. Both stand in the same sun and drink from the same soil. So why can only one of them make wood?"):
            pass
        B.neby_out(self, nb)
        S.clear_updaters()
        Bm.clear_updaters()
        knife = Line([1.2, -1.9, 0], [4.0, -1.9, 0], color=WHITE, stroke_width=5)
        disc = sg_frame(4.0, 0.62, 1.0, k=1.0, center=np.array([-2.6, 0.4, 0]))
        with self.say("The answer is hidden inside, and you only see it if you cut the plant open and look at a thin slice under a microscope. That is plant anatomy."):
            self.play(ShowPassingFlash(knife, time_width=0.6), run_time=0.8)
            self.sfx("impact", gain=-10)
            self.play(FadeOut(Bm), FadeOut(lab_b), FadeIn(disc, scale=0.3), run_time=1.0)
        self.play(FadeOut(VGroup(ground, S, lab_s, disc, cnt)))
        self.remove(S, Bm)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 1: Plant Anatomy. By the end you will be able to look at a slide and say, in seconds, dicot root, or monocot stem, and prove it from what is on the slide."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. What a tissue is. Meristems, and the permanent tissues they become. Then we cut across a root, a stem and a leaf, of both a dicot and a monocot. And finally, secondary growth, where we come back to the sal and the bamboo.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        C = np.array([-3.2, 0.1, 0])
        body = Ellipse(width=2.2, height=3.0, stroke_color=PAR, stroke_width=3, fill_color=PARF, fill_opacity=1).move_to(C)
        chl = AnnularSector(inner_radius=0.7, outer_radius=1.0, angle=PI * 1.3, start_angle=PI * 1.35, fill_color=CHL, fill_opacity=0.85, stroke_width=0).stretch(1.0, 0).move_to(C + DOWN * 0.35)
        nuc = Circle(radius=0.28, stroke_color="#B6F5C4", stroke_width=2, fill_color="#2F5E3E", fill_opacity=1).move_to(C + UP * 0.25)
        eye = Dot(C + [0.62, 0.7, 0], radius=0.09, color=th.CORAL)
        fl = VGroup(*[VMobject(stroke_color=PAR, stroke_width=3).set_points_smoothly([C + [0, 1.5, 0], C + [s_ * 0.4, 2.2, 0], C + [s_ * 0.2, 2.8, 0], C + [s_ * 0.6, 3.3, 0]]) for s_ in (-1, 1)])
        cell = VGroup(body, chl, nuc, eye, fl)
        name = T("Chlamydomonas: one cell", size=26, color=PAR).move_to(C + DOWN * 2.1)
        jobs = ["photosynthesis", "absorption", "movement", "reproduction"]
        chips = VGroup()
        for i, j in enumerate(jobs):
            ch = VGroup(RoundedRectangle(corner_radius=0.15, width=2.9, height=0.55, stroke_color=th.PANEL_EDGE, fill_color=th.PANEL, fill_opacity=1, stroke_width=2), T(j, size=22, color=th.INK))
            ch[1].move_to(ch[0])
            ch.move_to([0.9, 1.5 - i * 0.95, 0])
            chips.add(ch)
        links = VGroup(*[Line(C + RIGHT * 1.1, ch.get_left(), stroke_width=2, color=th.FAINT) for ch in chips])
        with self.say("Start with the simplest green life there is: Chlamydomonas, a single cell swimming in a pond. That one cell does everything. It photosynthesises, it absorbs, it moves, and it reproduces."):
            self.play(FadeIn(cell, scale=0.8), FadeIn(name))
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(c_, shift=RIGHT * 0.2)) for l_, c_ in zip(links, chips)], lag_ratio=0.3), run_time=2.4)
            self.play(Rotate(fl, 0.15, about_point=C + UP * 1.5), rate_func=there_and_back, run_time=0.8)
        self.play(FadeOut(VGroup(cell, name, chips, links)))
        cols, rows = 13, 8
        s = 0.42
        grid = VGroup(*[Square(side_length=s * 0.92, stroke_color=th.MUTED, stroke_width=1.5, fill_color=th.PANEL, fill_opacity=1).move_to([(i - (cols - 1) / 2) * s - 2.0, (j - (rows - 1) / 2) * s, 0])
                        for j in range(rows) for i in range(cols)])
        with self.say("A fig tree cannot work like that. It is far too big for every cell to do every job. Its answer is division of labour."):
            self.play(LaggedStart(*[FadeIn(q) for q in grid], lag_ratio=0.004), run_time=1.5)

        def role(i, j):
            if i in (0, cols - 1) or j in (0, rows - 1):
                return 0
            if i in (3, 9):
                return 2
            if i in (4, 8):
                return 3
            if 5 <= i <= 7:
                return 4
            return 1

        rc = [(EPI, "protection"), (CHL, "photosynthesis"), (SCL, "support"), (XYL, "transport"), (PITH, "storage")]
        anims = []
        for idx, q in enumerate(grid):
            i, j = idx % cols, idx // cols
            anims.append(q.animate.set_fill(rc[role(i, j)][0], opacity=0.75).set_stroke(rc[role(i, j)][0]))
        leg = B.legend([(n_, c_) for c_, n_ in rc], size=24).move_to([4.4, 0, 0])
        with self.say("Groups of cells specialise. Some only protect, some only photosynthesise, some only support, some only carry water and food, some only store. Each group does one job, and does it well."):
            self.play(LaggedStart(*anims, lag_ratio=0.004), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in leg], lag_ratio=0.2))
        self.play(FadeOut(VGroup(grid, leg)))
        d = self.callout("key", "A tissue is a group of cells of common origin that are structurally similar and work together to perform a particular function.", width=11)
        d.move_to([0, 1.0, 0])
        hist = VGroup(T("histology: the study of tissues", size=26, color=th.BODY), T("plant anatomy: the internal structure of plants", size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.0, 0])
        grew = VGroup(T("1670s", size=30, color=th.AMBER, weight="BOLD"), para("Nehemiah Grew and Marcello Malpighi found the subject; Grew is the father of plant anatomy", width=9.5, size=22, color=th.INK)).arrange(RIGHT, buff=0.35).move_to([0, -2.4, 0])
        with self.say("Each such group is a tissue: a group of cells of common origin, similar in structure, working together for one function. The study of tissues is histology. The study of the inside of plants is plant anatomy, founded in the sixteen seventies by Nehemiah Grew and Marcello Malpighi. Grew is called the father of plant anatomy."):
            self.play(FadeIn(d, shift=UP * 0.2))
            self.play(FadeIn(hist))
            self.play(FadeIn(grew, shift=UP * 0.2))
        self.play(FadeOut(VGroup(d, hist, grew)))
        self.p1_tree()
        self.p1_systems()

    def box(self, text, pos, color, w=2.6, h=0.62, size=22):
        t = para(text, width=w - 0.25, size=size, color=th.INK, align="center")
        b = RoundedRectangle(corner_radius=0.12, width=w, height=max(h, t.height + 0.28), stroke_color=color, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1)
        return VGroup(b, t.move_to(b)).move_to(pos)

    def elbow(self, a, b, color=th.MUTED):
        a, b = np.array(a, dtype=float), np.array(b, dtype=float)
        m = (a[1] + b[1]) / 2
        return VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners([a, [a[0], m, 0], [b[0], m, 0], b])

    def p1_tree(self):
        MER, PERM = "#9C8CFF", PAR
        root = self.box("plant tissue", [0, 2.6, 0], th.INK, w=2.8)
        m = self.box("meristematic: cells still divide", [-3.5, 1.3, 0], MER, w=3.8)
        p = self.box("permanent: division lost", [3.5, 1.3, 0], PERM, w=3.8)
        mk = [self.box(t_, [x, -0.1, 0], MER, w=1.9, size=20) for t_, x in [("apical", -5.4), ("intercalary", -3.5), ("lateral", -1.6)]]
        sp = self.box("simple: one cell type", [1.75, -0.1, 0], PERM, w=3.0, size=20)
        cp = self.box("complex: many cell types", [5.2, -0.1, 0], PERM, w=3.0, size=20)
        sk = [self.box(t_, [1.75, y, 0], PERM, w=2.4, size=20) for t_, y in [("parenchyma", -1.15), ("collenchyma", -1.95), ("sclerenchyma", -2.75)]]
        ck = [self.box(t_, [5.2, y, 0], PERM, w=2.0, size=20) for t_, y in [("xylem", -1.15), ("phloem", -1.95)]]
        l1 = [self.elbow(root.get_bottom(), m.get_top()), self.elbow(root.get_bottom(), p.get_top())]
        l2 = [self.elbow(m.get_bottom(), q.get_top()) for q in mk]
        l3 = [self.elbow(p.get_bottom(), sp.get_top()), self.elbow(p.get_bottom(), cp.get_top())]
        l4 = [Line(a_.get_bottom(), b_.get_top(), color=th.MUTED, stroke_width=2.5) for a_, b_ in zip([sp] + sk[:-1], sk)] + [Line(a_.get_bottom(), b_.get_top(), color=th.MUTED, stroke_width=2.5) for a_, b_ in zip([cp] + ck[:-1], ck)]
        b1 = T("basis 1: can the cells divide?", size=22, color=th.AMBER).move_to([0, 1.95, 0])
        b2 = T("basis 2: how many kinds of cell?", size=22, color=th.AMBER).move_to([3.5, 0.6, 0])
        with self.say("Tissues are classified on two quite different bases, and students lose marks by mixing them up. The first basis: can the cells still divide? If yes, the tissue is meristematic. If they have lost that power, it is permanent."):
            self.play(FadeIn(root))
            self.play(*[Create(l_) for l_ in l1], FadeIn(m, shift=DOWN * 0.2), FadeIn(p, shift=DOWN * 0.2), FadeIn(b1))
        with self.say("Meristems are apical, intercalary or lateral, depending on where they sit."):
            self.play(*[Create(l_) for l_ in l2], LaggedStart(*[FadeIn(q, shift=DOWN * 0.2) for q in mk], lag_ratio=0.2))
        with self.say("The second basis applies to permanent tissue: how many kinds of cell does it contain? A simple tissue has only one kind: parenchyma, collenchyma or sclerenchyma. A complex tissue has several kinds working as a unit: xylem and phloem."):
            self.play(*[Create(l_) for l_ in l3], FadeIn(sp), FadeIn(cp), FadeIn(b2))
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(q)) for l_, q in zip(l4, sk + ck)], lag_ratio=0.25), run_time=2.2)
        self.play(FadeOut(VGroup(root, m, p, *mk, sp, cp, *sk, *ck, *l1, *l2, *l3, *l4, b1, b2)))

    def p1_systems(self):
        st = B.DicotStemTS(R=2.75).move_to([-3.3, -0.15, 0])
        P = st.parts
        cap = B.Captions(self, at=(3.7, 0.0, 0), width=5.4, size=27)
        with self.say("There is a third way to organise tissues, and it is the fastest way to read any section. Cut any organ across, and its tissues fall into three systems. This is Sachs' classification."):
            self.play(FadeIn(st, scale=0.9), run_time=1.2)
            cap("Three tissue systems", sub="Sachs' classification: epidermal, ground and vascular.")
        groups = [("Epidermal (dermal) system", EPI, [P["epi"]], "Epidermis, cuticle, stomata, hairs: protection and control of water loss."),
                  ("Ground (fundamental) system", PAR, [P["hyp"], P["cortex"], P["endo"], P["pith"]], "Cortex, endodermis, pericycle, pith, medullary rays: photosynthesis, storage, support."),
                  ("Vascular (conducting) system", XYL, [P["bundles"]], "Xylem, phloem and cambium, in bundles or a ring: long-distance transport.")]
        says = ["The epidermal system: the outermost layer, with its cuticle, stomata and hairs. It protects, and it controls water loss and gas exchange.",
                "The ground system: everything between the skin and the plumbing. Cortex, endodermis, pericycle, pith and the medullary rays. It photosynthesises, stores and supports.",
                "And the vascular system: xylem, phloem and cambium, here in a ring of bundles. It carries water and food over long distances."]
        everything = [P["epi"], P["hyp"], P["cortex"], P["endo"], P["pith"], P["bundles"]]
        for m_ in everything:
            m_.save_state()
        for (title, col, parts, sub), sy in zip(groups, says):
            with self.say(sy):
                cap(title, color=col, swatch=col, sub=sub)
                self.play(*[Restore(m_) if m_ in parts else m_.animate.fade(0.85) for m_ in everything], run_time=0.8)
        self.play(*[Restore(m_) for m_ in everything], run_time=0.5)
        cap.clear()
        self.play(st.animate.scale(0.6).move_to([-4.6, 0.3, 0]))
        self.tip("Asked to 'describe the internal structure' of any organ? Walk inwards: epidermis → ground tissue → vascular tissue → centre. You will never leave a layer out.",
                 "Exam tip. When a question says describe the internal structure of an organ, walk inwards in exactly this order: epidermis, then the ground tissue, then the vascular tissue, then the centre. You will never miss a layer, and your answer will read like a real section.", width=7.4)
        self.play(FadeOut(st))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        self.p2_meristem()
        self.p2_position()
        self.p2_function()
        self.p2_simple()
        self.p2_complex()

    def p2_meristem(self):
        mer = B.meristem(3.4, 3.4, s=0.38, center=[-4.2, 0.0, 0])
        tl = T("meristem", size=28, color="#C9B8FF", weight="BOLD").next_to(mer, UP, buff=0.25)
        feats = ["small, isodiametric, tightly packed", "no intercellular spaces", "thin cellulose wall", "dense cytoplasm, large nucleus",
                 "vacuoles absent or tiny", "high rate of metabolism"]
        rows = VGroup(*[VGroup(Dot(radius=0.06, color="#C9B8FF"), T(f_, size=25, color=th.INK)).arrange(RIGHT, buff=0.2) for f_ in feats]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, 0.0, 0])
        with self.say("A meristem, from the Greek meristos, divisible, is a tissue of young cells that keep the power to divide. Every permanent tissue in a plant was once meristematic. Look at the cells.") as v:
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(c_) for c_ in mer], lag_ratio=0.003), run_time=1.6)
        with self.say("They are small and box-like, packed with no spaces between them. Thin cellulose walls, dense cytoplasm, a large nucleus, and almost no vacuole. These are cells built to divide, with a high rate of metabolism.") as v:
            per = (v.dur - 0.5) / len(rows)
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.4)
                self.hold(per - 0.4)
        with self.say("And because a plant keeps its meristems all its life, it can keep growing for as long as it lives. That is open, or indeterminate, growth. Animals do not have it."):
            self.play(Indicate(tl, color=th.AMBER))
        self.play(FadeOut(VGroup(mer, tl, rows)))
        cards = VGroup(B.card(self, "Promeristem", "the few cells at the very tip from which all other meristems arise", w=3.7, h=3.0, color="#C9B8FF", bsize=21),
                       B.card(self, "Primary meristem", "from the promeristem; present since the embryo; builds the primary body", w=3.7, h=3.0, color="#9C8CFF", bsize=21),
                       B.card(self, "Secondary meristem", "arises later from permanent tissue that regains division: interfascicular cambium, cork cambium, wound cambium", w=3.7, h=3.0, color=CAMB, bsize=21)).arrange(RIGHT, buff=0.55).move_to([0, -0.2, 0])
        arr = VGroup(*[Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.06, color=th.MUTED, stroke_width=3) for i in range(2)])
        head = T("Classified by origin: where did the meristem come from?", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("Meristems are classified three ways, and each answers a different question. By origin: where did it come from? The promeristem is the handful of cells at the very tip. Primary meristems come from it and build the primary body. Secondary meristems appear later, from permanent cells that have regained the power to divide, like the cork cambium."):
            self.play(FadeIn(head))
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(GrowArrow(arr[0]), FadeIn(cards[1], shift=UP * 0.2))
            self.play(GrowArrow(arr[1]), FadeIn(cards[2], shift=UP * 0.2))
        self.play(FadeOut(VGroup(head, cards, arr)))

    def p2_position(self):
        head = T("Classified by position", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        stem = Rectangle(width=0.5, height=3.6, stroke_color=PAR, stroke_width=3, fill_color=PARF, fill_opacity=1).move_to([-3.6, 0.3, 0])
        root = Polygon([-3.8, -1.5, 0], [-3.4, -1.5, 0], [-3.6, -2.9, 0], stroke_color="#C9A27A", stroke_width=3, fill_color="#3A2E1F", fill_opacity=1)
        leaves = VGroup(*[Ellipse(width=1.5, height=0.45, stroke_color=PAR, stroke_width=2, fill_color="#2E7D32", fill_opacity=1).rotate(s_ * 0.3).move_to([-3.6 + s_ * 0.95, y, 0]) for y, s_ in [(1.2, 1), (1.2, -1), (0.0, 1), (0.0, -1)]])
        soil = Line([-5.5, -1.5, 0], [-1.7, -1.5, 0], color=th.FAINT, stroke_width=2)
        ap = VGroup(Dot([-3.6, 2.1, 0], radius=0.16, color="#9C8CFF"), Dot([-3.6, -2.85, 0], radius=0.13, color="#9C8CFF"))
        ic = VGroup(*[Rectangle(width=0.5, height=0.14, stroke_width=0, fill_color=th.CORAL, fill_opacity=1).move_to([-3.6, y, 0]) for y in (-0.25, 0.95)])
        lat = VGroup(*[Rectangle(width=0.07, height=3.3, stroke_width=0, fill_color=CAMB, fill_opacity=1).move_to([-3.6 + d, 0.3, 0]) for d in (-0.15, 0.15)])
        cap = B.Captions(self, at=(2.6, 0.2, 0), width=6.4, size=27)
        plant = VGroup(soil, root, stem, leaves)
        with self.say("By position: where does the meristem sit? Apical meristems sit at the tips of the shoot and the root. They make the plant longer. That is primary growth."):
            self.play(FadeIn(head), FadeIn(plant))
            self.play(FadeIn(ap, scale=2))
            cap("Apical meristem", color="#9C8CFF", swatch="#9C8CFF", sub="At the root and shoot tips. Adds length: primary growth, the primary body.")
            self.play(stem.animate.stretch(1.08, 1, about_edge=DOWN), ap[0].animate.shift(UP * 0.29), run_time=1.2)
        with self.say("Intercalary meristems are pieces of apical meristem left behind between permanent tissues, at the base of an internode or a leaf sheath. They are found in grasses, in Equisetum, and in mint."):
            self.play(FadeIn(ic))
            cap("Intercalary meristem", color=th.CORAL, swatch=th.CORAL, sub="Left behind at the base of internodes and leaf sheaths: grasses, Equisetum, mint.")
        with self.say("Lateral meristems run as cylinders along the length of the axis: the vascular cambium and the cork cambium. They make the plant thicker. That is secondary growth."):
            self.play(FadeIn(lat))
            cap("Lateral meristem", color=CAMB, swatch=CAMB, sub="Vascular cambium and cork cambium (phellogen). Adds girth: secondary growth.")
            self.play(stem.animate.stretch(1.4, 0), lat[0].animate.shift(LEFT * 0.08), lat[1].animate.shift(RIGHT * 0.08), run_time=1.2)
        self.play(FadeOut(VGroup(plant, ap, ic, lat, head)))
        cap.clear()
        blades = VGroup()
        for i in range(16):
            x = -4.5 + i * 0.6
            blades.add(VGroup(Rectangle(width=0.16, height=2.2, stroke_width=0, fill_color="#5FB04A", fill_opacity=1).move_to([x, -1.4, 0]),
                              Rectangle(width=0.16, height=0.16, stroke_width=0, fill_color=th.CORAL, fill_opacity=1).move_to([x, -2.42, 0])))
        soil = Line([-5.2, -2.5, 0], [5.2, -2.5, 0], color=th.FAINT, stroke_width=3)
        blade_line = Line([-5.4, -1.5, 0], [5.4, -1.5, 0], color=WHITE, stroke_width=4)
        lab = T("intercalary meristem at the base of each blade", size=24, color=th.CORAL).move_to([0, -3.0, 0])
        with self.say("This is why a lawn grows back after it is mown. The mower takes the tips, and the apical meristems with them. But the intercalary meristems at the base of each leaf are untouched, and they push the blade back up. It is also why a bamboo culm can elongate so fast."):
            self.play(Create(soil), FadeIn(blades), FadeIn(lab))
            self.play(ShowPassingFlash(blade_line, time_width=0.5), *[b[0].animate.stretch(0.45, 1, about_edge=DOWN) for b in blades], run_time=1.2)
            self.sfx("whoosh", gain=-12)
            self.play(*[b[0].animate.stretch(2.0, 1, about_edge=DOWN) for b in blades], run_time=2.5)
        self.play(FadeOut(VGroup(blades, soil, lab)))

    def p2_function(self):
        head = T("Classified by function (Haberlandt)", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        C = np.array([-3.4, -1.9, 0])
        gm = Sector(radius=3.0, angle=PI, start_angle=0, stroke_width=0, fill_color="#3B2F6B", fill_opacity=1).move_to(C, aligned_edge=DOWN)
        gm.shift(C - gm.get_bottom())
        pd = Arc(radius=3.0, start_angle=0, angle=PI, stroke_color=EPI, stroke_width=12).move_arc_center_to(C)
        pc = VGroup(*[Rectangle(width=0.22, height=2.0, stroke_width=0, fill_color=CAMB, fill_opacity=0.95).move_to(C + [d, 1.0, 0]) for d in (-0.9, 0.9)])
        items = [("protoderm", EPI, pd, "epidermis"), ("procambium", CAMB, pc, "primary xylem, primary phloem, vascular cambium"), ("ground meristem", "#C9B8FF", gm, "cortex, endodermis, pericycle, pith, medullary rays")]
        rows = VGroup()
        for n_, c_, _, prod in items:
            rows.add(VGroup(T(n_, size=26, color=c_, weight="BOLD"), T("→", size=28, color=th.MUTED), para(prod, width=3.6, size=22, color=th.INK)).arrange(RIGHT, buff=0.25, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([2.9, 0.0, 0])
        with self.say("By function. Haberlandt showed that the apical meristem is already sorted into three zones, and each zone is destined for one tissue system."):
            self.play(FadeIn(head), FadeIn(gm), Create(pd), FadeIn(pc))
        says = ["The outermost layer, the protoderm, becomes the epidermis.",
                "Strands of procambium become the primary xylem and phloem, and the vascular cambium.",
                "And the rest, the ground meristem, becomes the cortex, endodermis, pericycle, pith and medullary rays."]
        for (n_, c_, m_, _), r_, sy in zip(items, rows, says):
            with self.say(sy):
                self.play(Indicate(m_, color=c_, scale_factor=1.03), FadeIn(r_, shift=RIGHT * 0.2), run_time=1.0)
        self.play(FadeOut(VGroup(head, gm, pd, pc, rows)))
        pos = [np.array([0, 1.4, 0]), np.array([3.3, -1.6, 0]), np.array([-3.3, -1.6, 0])]
        nodes = VGroup(self.box("meristematic cell", pos[0], "#9C8CFF", w=3.2), self.box("permanent cell", pos[1], PAR, w=3.2), self.box("meristem again (secondary)", pos[2], CAMB, w=3.6))
        arcs = VGroup(CurvedArrow(pos[0] + [1.7, -0.2, 0], pos[1] + [0, 0.4, 0], angle=-0.7, color=th.MUTED, stroke_width=3),
                      CurvedArrow(pos[1] + [-1.7, -0.2, 0], pos[2] + [1.85, -0.2, 0], angle=-0.7, color=th.MUTED, stroke_width=3),
                      CurvedArrow(pos[2] + [0, 0.4, 0], pos[0] + [-1.7, -0.2, 0], angle=-0.7, color=th.MUTED, stroke_width=3))
        al = VGroup(T("differentiation", size=24, color=PAR).move_to([2.9, 0.5, 0]), T("dedifferentiation", size=24, color=CAMB).move_to([0, -2.75, 0]),
                    T("redifferentiation", size=24, color="#9C8CFF").move_to([-2.9, 0.5, 0]))
        with self.say("Three words that make all of this precise. Differentiation: a meristematic cell matures into a permanent cell, and stops dividing. Dedifferentiation: a permanent cell regains the power to divide. That is how the interfascicular cambium and the cork cambium form. Redifferentiation: the products of that new meristem mature again into permanent tissue."):
            self.play(FadeIn(nodes[0]))
            self.play(Create(arcs[0]), FadeIn(al[0]), FadeIn(nodes[1]))
            self.play(Create(arcs[1]), FadeIn(al[1]), FadeIn(nodes[2]))
            self.play(Create(arcs[2]), FadeIn(al[2]))
        self.play(FadeOut(VGroup(nodes, arcs, al)))
        w = self.callout("careful", "Monocots have apical and intercalary meristems but, except Dracaena and Yucca, no normal vascular cambium. That is exactly why a maize stem never thickens into a trunk.", width=11)
        with self.say("One caution. Monocots have apical and intercalary meristems, but, apart from a few such as Dracaena and Yucca, no normal vascular cambium. Keep that in mind; it is the answer to our cold open."):
            self.play(FadeIn(w, shift=UP * 0.2))
        self.play(FadeOut(w))

    def p2_simple(self):
        head = T("Simple permanent tissues", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cap = B.Captions(self, at=(3.3, -0.1, 0), width=6.2, size=27)
        L = np.array([-3.6, -0.3, 0])
        pa = B.parenchyma(4.4, 3.6, r=0.3, center=L)
        with self.say("Permanent cells have differentiated: they have taken a fixed shape, wall and job, and lost the power to divide. The simple ones first. Parenchyma is the least specialised and most common tissue: the packing of the plant."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c_) for c_ in pa], lag_ratio=0.004), run_time=1.6)
            cap("Parenchyma", color=PAR, swatch=PAR, sub="Living, thin-walled, isodiametric cells with intercellular spaces.")
        with self.say("Its cells are living and thin walled, with conspicuous spaces between them. It fills the cortex, pith, medullary rays and mesophyll. It stores food and water, it is where most of the plant's metabolism happens, and it can still divide, which is why a cutting can regrow a whole plant."):
            cap("Storage, metabolism, regeneration", color=PAR, sub="Cortex, pith, medullary rays, mesophyll. Can dedifferentiate: cuttings regrow.")
        ch = B.parenchyma(4.4, 3.6, r=0.3, center=L, chloro=True)
        with self.say("Give parenchyma chloroplasts and it becomes chlorenchyma, the photosynthetic tissue of the leaf mesophyll."):
            self.play(FadeOut(pa), FadeIn(ch), run_time=1.0)
            cap("Chlorenchyma", color=CHL, swatch=CHL, sub="Parenchyma with chloroplasts: photosynthesis. Leaf mesophyll.")
        ae = B.parenchyma(4.4, 3.6, r=0.3, center=L, air=True)
        with self.say("Give it huge air spaces and it becomes aerenchyma, which floats water plants like Hydrilla and the water lily, and carries oxygen down to the roots of rice. Elongated, pointed parenchyma is prosenchyma, and isolated cells storing oil, tannin or crystals are idioblasts."):
            self.play(FadeOut(ch), FadeIn(ae), run_time=1.0)
            cap("Aerenchyma", color=WATER, swatch=WATER, sub="Large air cavities: buoyancy and oxygen. Hydrilla, Nymphaea, rice roots. Also: prosenchyma, idioblasts.")
        self.play(FadeOut(ae))
        co = B.collenchyma(4.4, 3.6, r=0.3, center=L)
        with self.say("Collenchyma is living mechanical tissue. Its walls are thickened unevenly, here at the corners, with cellulose, hemicellulose and a lot of pectin. Pectin is what makes it flexible rather than brittle."):
            self.play(LaggedStart(*[FadeIn(c_) for c_ in co], lag_ratio=0.01), run_time=1.4)
            cap("Collenchyma", color=COL, swatch=COL, sub="Living. Unevenly thickened walls: cellulose, hemicellulose, much pectin. Flexible.")
        self.play(FadeOut(co))
        sh = Line([-3.6, -2.6, 0], [-3.6, 1.6, 0], color=COL, stroke_width=10)
        bent = ArcBetweenPoints([-3.6, -2.6, 0], [-2.3, 1.3, 0], angle=-0.6, color=COL, stroke_width=10)
        with self.say("Because the walls are not lignified, the cells can still stretch. So collenchyma supports an organ that is still growing: it bends in the wind and springs back. It sits just under the epidermis of young dicot stems, in petioles, and in the ridges of a sunflower or pumpkin stem. Never in monocots, and rarely in roots."):
            self.play(Create(sh))
            self.play(Transform(sh, bent), run_time=0.9, rate_func=there_and_back)
            self.play(Transform(sh, bent), run_time=0.9, rate_func=there_and_back)
            cap("Supports a growing organ", color=COL, sub="Hypodermis of young dicot stems, petioles, ridges of Cucurbita and Helianthus. Not in monocots.")
        self.play(FadeOut(sh))
        kinds = VGroup()
        for i, (kd, nm, ex) in enumerate([("angular", "angular", "corners: Datura, Solanum"), ("lamellar", "lamellar (plate)", "tangential walls: Helianthus"), ("lacunar", "lacunar (tubular)", "round air spaces: Cucurbita")]):
            p_ = B.collenchyma(1.9, 1.6, r=0.22, kind=kd)
            kinds.add(VGroup(p_, T(nm, size=22, color=COL, weight="BOLD"), T(ex, size=18, color=th.BODY)).arrange(DOWN, buff=0.15))
        kinds.arrange(RIGHT, buff=0.35).scale(0.8).move_to([-3.55, -0.4, 0])
        with self.say("By the pattern of thickening there are three kinds. Angular, thickened at the corners, as in Datura. Lamellar, thickened on the tangential walls, as in the sunflower stem. And lacunar, thickened round the air spaces, as in Cucurbita."):
            self.play(LaggedStart(*[FadeIn(k_, shift=UP * 0.2) for k_ in kinds], lag_ratio=0.35), run_time=2.4)
            cap("Angular · lamellar · lacunar", color=COL, sub="Named by where the wall is thickened.")
        self.play(FadeOut(kinds))
        sc = B.sclerenchyma(4.4, 3.6, r=0.3, center=L)
        with self.say("Sclerenchyma is dead mechanical tissue. The wall is thick, evenly lignified and pierced by simple pits. The lumen inside is tiny, and the living contents disappear at maturity. It gives rigidity, hardness and strength."):
            self.play(LaggedStart(*[FadeIn(c_) for c_ in sc], lag_ratio=0.004), run_time=1.4)
            cap("Sclerenchyma", color=SCL, swatch=SCL, sub="Dead at maturity. Thick, uniformly lignified walls; simple pits; narrow lumen. Rigid.")
        self.play(FadeOut(sc))
        fibres = VGroup(*[B.fibre(3.6, 0.2, center=[-3.6 + 0.05 * ((-1) ** i), 1.0 - i * 0.18, 0]) for i in range(9)])
        allo = T("allo (Girardinia diversifolia)", size=22, color=th.AMBER).next_to(fibres, DOWN, buff=0.25)
        with self.say("It comes in two forms. Fibres are very long, narrow cells with pointed ends, in bundles. Jute, flax and hemp are fibres from the phloem, and so is allo, the Himalayan nettle, whose fibres are woven into cloth in Sankhuwasabha and Bajhang."):
            self.play(LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.3) for f_ in fibres], lag_ratio=0.1), FadeIn(allo))
            cap("Fibres", color=SCL, swatch=SCL, sub="Long, narrow, pointed, in bundles. Bast fibres: jute, flax, hemp, allo.")
        self.play(FadeOut(VGroup(fibres, allo)))
        sclereids = VGroup(*[B.sclereid(0.55, seed=s_) for s_ in range(5)]).arrange_in_grid(2, 3, buff=0.25).move_to([-3.6, -0.3, 0])
        with self.say("Sclereids, or stone cells, are short, irregular and extremely thick walled. They are the grit in a guava or a pear, the shell of a walnut, the hard coat of a pulse seed."):
            self.play(LaggedStart(*[GrowFromCenter(s_) for s_ in sclereids], lag_ratio=0.2), run_time=1.6)
            cap("Sclereids (stone cells)", color=SCL, swatch=SCL, sub="Short, very thick layered walls: grit of guava and pear, walnut shell, seed coats.")
        self.play(FadeOut(sclereids))
        cap.clear()
        rows = [["", "Collenchyma", "Sclerenchyma"], ["cells", "living", "dead at maturity"], ["wall", "cellulose, hemicellulose, pectin", "lignin"],
                ["thickening", "uneven: corners or certain walls", "uniform and heavy; narrow lumen"], ["role", "flexible support, growing organ", "rigid support, mature organ"]]
        tb = B.table(rows, [2.2, 4.8, 4.8], row_h=0.72, size=24, colors=[th.MUTED, COL, SCL]).move_to([0, -0.6, 0])
        with self.say("A four mark question, Group B, number one: distinguish collenchyma from sclerenchyma under four headings. Cells: living versus dead. Wall: cellulose and pectin versus lignin. Thickening: uneven versus uniform and heavy. Role: flexible support in a growing organ versus rigid support in a mature one.") as v:
            B.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(head, tb)))
        self.quiz("Which tissue gives flexible support to a young, still-growing dicot stem?",
                  ["sclerenchyma", "collenchyma", "parenchyma", "xylem fibres"], 1,
                  "Pause and think. A young sunflower stem bends in the wind and springs back. Which tissue lets it do that?",
                  "Collenchyma. It is alive, and its walls are rich in pectin and not lignified, so it can stretch as the organ grows. Sclerenchyma is the tempting answer, but its lignified walls are rigid and its cells are dead: it supports organs that have finished growing.")

    def p2_complex(self):
        head = T("Complex tissue: xylem", size=32, color=XYL, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        tr = B.tracheid(3.4, 0.5, center=[-5.7, -0.3, 0])
        ve = B.vessel(3.4, 0.75, center=[-4.25, -0.3, 0], kind="pitted")
        fb = B.fibre(3.4, 0.22, center=[-2.75, -0.3, 0]).rotate(PI / 2)
        xp = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=0.6, height=0.62, stroke_color=PAR, stroke_width=2, fill_color=PARF, fill_opacity=1), Dot(radius=0.07, color="#B6F5C4")).move_to([-1.2, -1.6 + 0.68 * j, 0]) for j in range(5)])
        names = ["tracheid", "vessel", "fibre", "parenchyma"]
        state = ["dead", "dead", "dead", "living"]
        objs = [tr, ve, fb, xp]
        labs = VGroup(*[VGroup(T(n_, size=21, color=th.INK), T(s_, size=18, color=th.CORAL if s_ == "dead" else PAR)).arrange(DOWN, buff=0.06).next_to(o_, DOWN, buff=0.22) for n_, s_, o_ in zip(names, state, objs)])
        cap = B.Captions(self, at=(3.6, -0.1, 0), width=5.6, size=26)
        with self.say("Now the complex tissues, made of several kinds of cell. Xylem carries water and dissolved minerals upwards, from root to leaf, and it also gives strength. It has four elements, and three of them are dead."):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(o_, shift=UP * 0.2) for o_ in objs], lag_ratio=0.25), LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.25), run_time=2.0)
        with self.say("Tracheids: long, tapering, lignified cells with bordered pits, and closed ends. Water seeps from one to the next through the pits. They are found in all vascular plants, and in gymnosperms like pine they are the only conducting element."):
            cap("Tracheids", color=XYL, swatch=XYL, sub="Dead, tapering, bordered pits, end walls not perforated. The only conducting element in gymnosperms.")
            self.play(Indicate(tr, color=XYL, scale_factor=1.05))
        flow = B.Flow([-4.25, -1.9, 0], [-4.25, 1.3, 0], n=10, color=WATER, speed=1.0, width=0.4)
        with self.say("Vessels are short, wide tubes stacked end to end, with their end walls perforated or dissolved away. Together they make one continuous open pipe, the most efficient water conductor there is. They are characteristic of flowering plants."):
            cap("Vessels (tracheae)", color=XYL, swatch=XYL, sub="Dead, wide, perforated end walls: a continuous pipe. Characteristic of angiosperms.")
            self.add(flow)
            self.wait(2.0)
        with self.say("Xylem fibres are dead and thick walled, purely for support. And xylem parenchyma is the one living element: it stores starch and tannin, and moves water sideways."):
            cap("Fibres and xylem parenchyma", color=PAR, swatch=PAR, sub="Fibres: dead, support. Parenchyma: living, storage and radial conduction.")
        self.play(FadeOut(VGroup(head, *objs, labs, flow)))
        self.remove(flow)
        cap.clear()
        head = T("Complex tissue: phloem", size=32, color=PHL, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        st, comp = B.sieve_tube(4.2, 0.8, center=[-4.4, -0.3, 0])
        food = B.Flow([-4.5, -2.2, 0], [-4.5, 1.6, 0], n=10, color=FOOD, speed=0.6, width=0.45, twoway=True)
        pf = B.fibre(3.6, 0.22, center=[-2.3, -0.3, 0]).rotate(PI / 2)
        pp = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=0.6, height=0.62, stroke_color=PAR, stroke_width=2, fill_color=PARF, fill_opacity=1), Dot(radius=0.07, color="#B6F5C4")).move_to([-1.2, -1.6 + 0.68 * j, 0]) for j in range(5)])
        with self.say("Phloem carries food, mostly sucrose, from where it is made to where it is used. And unlike xylem, it can carry it in either direction, up or down. Its main cells are sieve tube elements, joined end to end through perforated cross walls called sieve plates."):
            self.play(FadeIn(head), FadeIn(st), FadeIn(pf), FadeIn(pp))
            self.add(food)
            cap("Sieve tube elements", color=PHL, swatch=PHL, sub="Living but without a nucleus. End to end through sieve plates. Food flows both ways.")
        with self.say("A sieve tube is alive, but it has lost its nucleus. So beside each one runs a narrow companion cell, with dense cytoplasm and a big nucleus. It controls the sieve tube through plasmodesmata, and loads sugar into it."):
            cap("Companion cells", color="#FFB3D9", swatch="#FFB3D9", sub="Living, nucleated. Control the enucleate sieve tube; load sugar.")
            self.play(Indicate(comp, color="#FFB3D9", scale_factor=1.06))
        with self.say("Then phloem fibres, or bast fibres, the only dead element of phloem. And phloem parenchyma, which stores food, resin and latex."):
            cap("Phloem fibres and parenchyma", color=PAR, sub="Bast fibres: dead, support. Phloem parenchyma: living storage.")
        self.play(FadeOut(VGroup(head, st, pf, pp, food)))
        self.remove(food)
        cap.clear()
        self.p2_proto()

    def p2_proto(self):
        head = T("Protoxylem and metaxylem", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        an = B.vessel(2.6, 0.45, center=[-5.3, -0.2, 0], kind="annular")
        sp = B.vessel(2.6, 0.45, center=[-4.3, -0.2, 0], kind="spiral")
        sc = B.vessel(2.6, 0.75, center=[-3.0, -0.2, 0], kind="scalariform")
        rt = B.vessel(2.6, 0.75, center=[-1.65, -0.2, 0], kind="reticulate")
        pt = B.vessel(2.6, 0.75, center=[-0.3, -0.2, 0], kind="pitted")
        l1 = VGroup(T("protoxylem", size=22, color=XYL, weight="BOLD"), T("formed first", size=18, color=th.BODY)).arrange(DOWN, buff=0.06).move_to([-4.8, 1.8, 0])
        l2 = VGroup(T("metaxylem", size=22, color=XYL, weight="BOLD"), T("formed later", size=18, color=th.BODY)).arrange(DOWN, buff=0.06).move_to([-1.65, 1.8, 0])
        n1 = VGroup(*[T(s_, size=16, color=th.BODY).next_to(v_, DOWN, buff=0.2) for s_, v_ in zip(["annular", "spiral", "scalariform", "reticulate", "pitted"], [an, sp, sc, rt, pt])])
        cap = B.Captions(self, at=(3.9, -0.1, 0), width=5.0, size=26)
        with self.say("The first xylem to form, while the organ is still lengthening, is protoxylem. Its vessels are narrow, with lignin only in rings or a spiral. Watch what that allows."):
            self.play(FadeIn(head), FadeIn(VGroup(an, sp)), FadeIn(l1))
            cap("Protoxylem", color=XYL, sub="Narrow vessels; annular or spiral thickening.")
            self.play(VGroup(an, sp).animate.stretch(1.25, 1), run_time=1.2)
            self.play(VGroup(an, sp).animate.stretch(0.8, 1), run_time=0.8)
        with self.say("It stretches, like a spring, as the organ grows. Xylem formed later is metaxylem: wider vessels with scalariform, reticulate or pitted walls. Strong, but no longer stretchable."):
            self.play(FadeIn(VGroup(sc, rt, pt)), FadeIn(l2), FadeIn(n1))
            cap("Metaxylem", color=XYL, sub="Wider vessels; scalariform, reticulate or pitted. Formed after elongation.")
        self.play(FadeOut(VGroup(an, sp, sc, rt, pt, l1, l2, n1)))
        cap.clear()

        def org(c, exarch):
            g = VGroup(Circle(radius=1.7, stroke_color=th.MUTED, stroke_width=3).move_to(c))
            for k in range(4):
                a = TAU * k / 4 + PI / 4
                rs = [(1.45, 0.07), (1.1, 0.11), (0.7, 0.15)] if exarch else [(0.45, 0.07), (0.8, 0.11), (1.2, 0.15)]
                for j, (rr, sz) in enumerate(rs):
                    col = th.AMBER if j == 0 else XYL
                    g.add(Circle(radius=sz, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.35).move_to(c + polar(rr, a)))
                p0, p1 = (1.4, 0.75) if exarch else (0.5, 1.2)
                g.add(Arrow(c + polar(p0, a + 0.33), c + polar(p1, a + 0.33), buff=0, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3))
            return g

        rt_ = org(np.array([-3.3, -0.3, 0]), True)
        st_ = org(np.array([3.0, -0.3, 0]), False)
        t1 = VGroup(T("root: exarch", size=28, color=th.INK, weight="BOLD"), T("protoxylem outside, towards the periphery", size=19, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(rt_, DOWN, buff=0.15)
        t2 = VGroup(T("stem: endarch", size=28, color=th.INK, weight="BOLD"), T("protoxylem inside, towards the centre", size=19, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(st_, DOWN, buff=0.15)
        pl = VGroup(Dot(radius=0.09, color=th.AMBER), T("protoxylem", size=22, color=th.AMBER)).arrange(RIGHT, buff=0.15).move_to([0, 2.1, 0])
        with self.say("Where the protoxylem sits is a diagnostic feature. In a root, protoxylem is on the outside, towards the periphery, and metaxylem towards the centre: that is exarch. The xylem develops inwards."):
            self.play(FadeIn(pl), FadeIn(rt_), FadeIn(t1))
        with self.say("In a stem it is the other way round. Protoxylem towards the centre, metaxylem outside: endarch. The xylem develops outwards."):
            self.play(FadeIn(st_), FadeIn(t2))
        self.play(FadeOut(VGroup(head, rt_, st_, t1, t2, pl)))
        self.tip("Roots are EXtroverts, stems are ENDoverts: exarch xylem in the root, endarch in the stem.",
                 "A memory trick. Roots are extroverts, stems are endoverts. Exarch in the root, endarch in the stem. One word that most students forget in a root answer.", state="wink")
        sec = self.callout("remember", "Special (secretory) tissues: laticiferous tissue (latex of Euphorbia, Calotropis, Ficus, rubber) and glandular tissue (nectaries, Citrus oil glands, resin canals of Pinus, digestive glands of Drosera).", width=11, size=26)
        with self.say("Some books add a third group, the secretory tissues. Laticiferous tissue carries latex, in Euphorbia, Calotropis, Ficus and the rubber tree. Glandular tissue includes nectaries, the oil glands of a lemon peel, the resin canals of pine and the digestive glands of the sundew."):
            self.play(FadeIn(sec, shift=UP * 0.2))
        self.play(FadeOut(sec))
        self.quiz("The only water-conducting element in the xylem of a gymnosperm such as Pinus is the",
                  ["vessel", "tracheid", "sieve tube", "xylem parenchyma"], 1,
                  "Pause and think. Pine has no vessels. So what carries its water?",
                  "Tracheids. Vessels, with their open perforated ends, are characteristic of flowering plants; gymnosperms rely on tracheids alone, passing water through bordered pits. Sieve tubes carry food, and xylem parenchyma only moves water sideways.")

    # ------------------------------------------------------------------ part 3: root
    def p3(self):
        self.section(2)
        C = np.array([-3.1, -0.15, 0])
        rt = B.RootTS(R=2.75).move_to(C)
        P = rt.parts
        cap = B.Captions(self, at=(3.75, 0.1, 0), width=5.3, size=27)
        order = [("epi", "hairs"), ("cortex",), ("endo", "casp"), ("peri",), ("phloem", "xylem")]
        says = [("Cut a young root across, a few centimetres behind the tip, and walk inwards. The outermost layer is the epiblema, or rhizodermis: one row of thin walled cells, with no cuticle and no stomata. A root must absorb water, so it cannot waterproof itself. Some cells grow out into root hairs, so it is also called the piliferous layer.",
                 "Epiblema (piliferous layer)", EPI, "One cell thick. No cuticle, no stomata. Bears unicellular root hairs."),
                ("Inside it, a broad cortex of thin walled parenchyma with plenty of air spaces, storing starch. No chlorenchyma, and normally no collenchyma.",
                 "Cortex", PAR, "Wide zone of parenchyma with intercellular spaces; stores starch."),
                ("The innermost layer of the cortex is the endodermis: one ring of barrel shaped cells fitted tightly together. Their radial and tangential walls carry a band of suberin and lignin, the Casparian strip.",
                 "Endodermis", ENDO, "Barrel-shaped cells, no spaces. Casparian strips on radial and tangential walls."),
                ("Just inside it, the pericycle, usually a single layer. It is the layer most worth naming, as you will see in a moment.",
                 "Pericycle", PERI, "One layer of parenchyma inside the endodermis."),
                ("And the vascular tissue. Xylem and phloem lie in separate strips, on alternate radii: xylem arms, with phloem patches between them. That is a radial arrangement. And the xylem is exarch, with the small protoxylem at the tips of the arms, on the outside.",
                 "Radial bundles, exarch xylem", XYL, "Xylem and phloem on alternate radii. Protoxylem at the outer tips.")]
        shown = []
        for keys, (sy, title, col, sub) in zip(order, says):
            with self.say(sy):
                for k_ in keys:
                    self.play(FadeIn(P[k_]), run_time=0.9)
                    shown.append(P[k_])
                cap(title, color=col, swatch=col, sub=sub)
                if keys[0] == "epi":
                    w = B.Flow(C + polar(3.6, PI * 0.78), C + polar(2.75, PI * 0.78), n=5, color=WATER, speed=0.6)
                    self.add(w)
                    self.wait(1.5)
                    self.remove(w)
        self.play(FadeOut(rt))
        cap.clear()
        self.p3_casparian()
        self.p3_lateral()
        self.p3_compare()

    def p3_casparian(self):
        head = T("Why the Casparian strip matters", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cells = VGroup(*[RoundedRectangle(corner_radius=0.25, width=2.0, height=1.5, stroke_color=ENDO, stroke_width=4, fill_color="#3D3820", fill_opacity=1).move_to([0, y, 0]) for y in (1.0, -0.6, -2.2)])
        strips = VGroup(*[Rectangle(width=0.5, height=0.16, stroke_width=0, fill_color="#FF9F43", fill_opacity=1).move_to([0, y, 0]) for y in (0.2, -1.4)])
        lc = T("cortex side", size=24, color=PAR).move_to([-4.6, 2.2, 0])
        rc = T("stele side", size=24, color=XYL).move_to([4.6, 2.2, 0])
        apo = VMobject(stroke_color=th.CORAL, stroke_width=4).set_points_as_corners([[-5.5, 0.2, 0], [-0.3, 0.2, 0]])
        x_ = VGroup(Line([-0.5, 0.45, 0], [-0.05, -0.05, 0], color=th.CORAL, stroke_width=7), Line([-0.5, -0.05, 0], [-0.05, 0.45, 0], color=th.CORAL, stroke_width=7))
        sym = VMobject(stroke_color=th.MINT, stroke_width=4).set_points_smoothly([[-5.5, -1.4, 0], [-1.4, -1.4, 0], [-0.7, -1.0, 0], [0, -0.75, 0], [0.7, -1.0, 0], [1.4, -1.4, 0], [5.5, -1.4, 0]])
        dot1 = Dot(radius=0.11, color=WATER).move_to([-5.5, 0.2, 0])
        dot2 = Dot(radius=0.11, color=WATER).move_to([-5.5, -1.4, 0])
        l1 = T("through the walls: blocked", size=24, color=th.CORAL).move_to([-3.2, 0.6, 0])
        l2 = T("through the living cell: controlled", size=24, color=th.MINT).move_to([3.0, -2.0, 0])
        cap = B.Captions(self, at=(-3.4, -2.55, 0), width=5.6, size=23)
        with self.say("Here are three endodermal cells, cortex on the left, the stele on the right. Water from the soil can travel two ways: along the cell walls, or through the living cells."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(lc), FadeIn(rc))
        with self.say("The Casparian strip is a waterproof band in the walls between the cells. Water creeping along the walls runs straight into it, and stops."):
            self.play(FadeIn(strips, scale=1.4))
            self.play(Create(apo), MoveAlongPath(dot1, Line([-5.5, 0.2, 0], [-0.4, 0.2, 0])), run_time=1.6)
            self.sfx("wrong", gain=-12)
            self.play(Create(x_), FadeIn(l1))
        with self.say("So the water is forced through the living protoplast of an endodermal cell, across its membrane. The root gains control over exactly what enters the stele."):
            self.play(Create(sym), MoveAlongPath(dot2, sym), run_time=2.4)
            self.sfx("correct", gain=-12)
            self.play(FadeIn(l2))
            cap("The endodermis is a checkpoint: nothing reaches the xylem without crossing a living membrane.", color=ENDO)
        with self.say("Opposite the protoxylem points, a few endodermal cells stay thin walled. They are the passage cells, and water crosses easily there."):
            cap("Passage cells: thin-walled endodermal cells opposite the protoxylem.", color=ENDO)
        self.play(FadeOut(VGroup(head, cells, strips, lc, rc, apo, x_, sym, dot1, dot2, l1, l2)))
        cap.clear()

    def p3_lateral(self):
        C = np.array([-3.1, -0.15, 0])
        rt = B.RootTS(R=2.4, hairs=False).move_to(C)
        a = 0.0
        grow = ValueTracker(0.0)

        def bud():
            L = grow.get_value()
            r0 = 0.72
            r1 = r0 + L
            w = 0.38
            pts = [C + polar(r0, a) + polar(w, a + PI / 2), C + polar(r1, a) + polar(w, a + PI / 2), C + polar(r1 + 0.3, a), C + polar(r1, a) - polar(w, a + PI / 2), C + polar(r0, a) - polar(w, a + PI / 2)]
            p = Polygon(*pts, stroke_color=PERI, stroke_width=3, fill_color="#4A3D80", fill_opacity=0.95)
            p.round_corners(0.12)
            return p

        bd = always_redraw(bud)
        cap = B.Captions(self, at=(3.75, 0.1, 0), width=5.3, size=27)
        with self.say("Why is the pericycle the layer to name? Because lateral roots grow from it. Watch. Pericycle cells opposite a protoxylem point start dividing, and a new root pushes outwards, right through the endodermis, the cortex and the epiblema."):
            self.play(FadeIn(rt))
            self.add(bd)
            cap("Lateral roots arise from the pericycle", color=PERI, swatch=PERI)
            self.play(grow.animate.set_value(2.4), run_time=4.0, rate_func=rate_functions.ease_in_out_sine)
        with self.say("A branch that starts deep inside like this is endogenous. A stem's branches are the opposite: they arise exogenously, from buds at the surface. In a dicot the pericycle also gives rise to part of the vascular cambium, and to the cork cambium."):
            cap("Endogenous origin", color=PERI, sub="Root branches arise deep inside, from the pericycle; stem branches arise exogenously, at the surface.")
        self.play(FadeOut(rt), FadeOut(bd))
        self.remove(bd)
        cap.clear()
        k = self.callout("key", "Xylem and phloem on the SAME radius with cambium between them: stem. On ALTERNATE radii: root. Decide that first, then count the xylem groups to decide dicot or monocot.", width=11)
        with self.say("Here is the one line test that decides most slides. Xylem and phloem on the same radius, with cambium between them, means stem. On alternate radii means root. Decide that first. Then count the xylem groups to decide dicot or monocot."):
            self.play(FadeIn(k, shift=UP * 0.2))
        self.play(FadeOut(k))

    def p3_compare(self):
        C = np.array([-3.1, -0.15, 0])
        d = B.RootTS(R=2.75, arms=4).move_to(C)
        m = B.RootTS(R=2.75, arms=18, monocot=True).move_to(C)
        cap = B.Captions(self, at=(3.75, 0.1, 0), width=5.3, size=27)
        cnt = VGroup(T("xylem groups", size=22, color=th.MUTED), T("4 · tetrarch", size=34, color=XYL, weight="BOLD")).arrange(DOWN, buff=0.1).move_to([3.75, 2.3, 0])
        with self.say("Now dicot versus monocot. A dicot root has few xylem groups, usually two to six: diarch, triarch, up to hexarch. Ranunculus is commonly tetrarch. Xylem fills the centre, so the pith is absent or tiny."):
            self.play(FadeIn(d), FadeIn(cnt))
            cap("Dicot root", sub="2 to 6 xylem groups. Pith absent or very small. Cambium forms later: secondary growth.")
        n2 = T("many · polyarch", size=34, color=XYL, weight="BOLD").move_to(cnt[1])
        with self.say("A monocot root, like maize, keeps the same ground plan, but the numbers change. Many xylem groups, more than six and often twenty or more: polyarch. They are pushed out into a ring, and the centre is filled with a large pith."):
            self.play(FadeOut(d), FadeIn(m), Transform(cnt[1], n2), run_time=1.6)
            cap("Monocot root", sub="Polyarch: more than 6 groups. Large pith. Conjunctive tissue often sclerenchymatous.")
        with self.say("And crucially, a monocot root has no cambium, so it shows no secondary growth. A dicot root has a cambium in waiting, formed later from the conjunctive tissue and the pericycle."):
            cap("No cambium in the monocot root", color=th.CORAL, sub="So no secondary growth. In the dicot, cambium forms from conjunctive tissue and pericycle.")
        self.play(FadeOut(m), FadeOut(cnt))
        cap.clear()
        rows = [["", "Dicot root", "Monocot root"], ["xylem groups", "2–6 (diarch to hexarch)", "more than 6 (polyarch)"], ["pith", "absent or very small", "large, well developed"],
                ["conjunctive tissue", "parenchymatous", "usually sclerenchymatous"], ["cambium", "forms later", "absent"], ["secondary growth", "present", "absent"],
                ["examples", "Helianthus, Cicer, Ranunculus", "Zea mays, Oryza, Allium"]]
        tb = B.table(rows, [3.0, 4.6, 4.6], row_h=0.66, size=24, colors=[th.MUTED, th.INK, th.INK]).move_to([0, 0.2, 0])
        same = para("Shared by both: epiblema with root hairs, endodermis with Casparian strips and passage cells, pericycle, radial bundles, exarch xylem.", width=12, size=22, color=th.MUTED).move_to([0, -3.0, 0])
        with self.say("Here is the comparison to learn as a table. Xylem groups, pith, conjunctive tissue, cambium, secondary growth, and examples. And everything else is shared: both have root hairs, an endodermis with Casparian strips, a pericycle, radial bundles and exarch xylem.") as v:
            B.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(same))
        self.play(FadeOut(VGroup(tb, same)))
        self.quiz("The Casparian strip is found in the",
                  ["epiblema", "pericycle", "endodermis", "conjunctive tissue"], 2,
                  "Pause and think. Where is the Casparian strip?",
                  "The endodermis: a band of suberin and lignin on its radial and tangential walls, forcing water through the living cells. The pericycle is the tempting wrong answer, because it lies right next to it, but the pericycle has no such band.")

    # ------------------------------------------------------------------ part 4: stem
    def p4(self):
        self.section(3)
        C = np.array([-3.1, -0.15, 0])
        st = B.DicotStemTS(R=2.75).move_to(C)
        P = st.parts
        cap = B.Captions(self, at=(3.75, 0.1, 0), width=5.3, size=27)
        steps_ = [(["epi"], "Now a sunflower stem, Helianthus. The epidermis is one layer, but unlike the root it has a cuticle, a few stomata and often multicellular hairs. The stem is above ground and must limit water loss.",
                   "Epidermis", EPI, "Cuticle, a few stomata, multicellular trichomes."),
                  (["hyp"], "Below it, the hypodermis: several layers of collenchyma, thickest under the ridges. That is what makes a young sunflower stem ridged and flexible.",
                   "Hypodermis: collenchyma", COL, "A few layers of collenchyma: flexible support."),
                  (["cortex"], "Then the general cortex: chlorenchyma outside, ordinary parenchyma inside.",
                   "General cortex", PAR, "Chlorenchyma outside, parenchyma inside."),
                  (["endo"], "The innermost cortical layer is the endodermis, loaded with starch grains. So in a stem it is called the starch sheath. A Casparian strip is not usually visible.",
                   "Endodermis: the starch sheath", ENDO, "Full of starch grains; Casparian strip not usually seen."),
                  (["caps"], "The pericycle shows as patches of sclerenchyma sitting like caps on the outer face of each bundle. These bundle caps are a strong clue that you are looking at a dicot stem.",
                   "Pericycle: bundle caps", SCL, "Semilunar patches of sclerenchyma over each bundle."),
                  (["phloem", "cambium", "xylem"], "And the bundles: a single ring of them, few, all the same size, wedge shaped.",
                   "A single ring of bundles", XYL, "Few, equal in size, wedge-shaped: a eustele."),
                  (["pith"], "In the centre a large pith of parenchyma, with strips running out between the bundles. Those strips are the medullary rays, and that is exactly where the interfascicular cambium will appear in part six.",
                   "Pith and medullary rays", PITH, "Large central parenchyma; rays run between the bundles.")]
        for keys, sy, title, col, sub in steps_:
            with self.say(sy):
                if keys[0] == "phloem":
                    self.play(FadeIn(VGroup(*[b[0] for b in P["bundles"]])), run_time=0.4)
                self.play(*[FadeIn(P[k_]) for k_ in keys], run_time=0.9)
                cap(title, color=col, swatch=col, sub=sub)
        self.play(st.animate.scale(0.55).move_to([-5.3, 1.3, 0]), FadeOut(cap.cur))
        cap.cur = None
        self.p4_bundle()
        self.play(FadeOut(st))
        self.p4_monocot()
        self.p4_types()
        self.p4_example()

    def p4_bundle(self):
        O = np.array([-0.6, -0.4, 0])
        back = Polygon(O + [-1.0, -1.8, 0], O + [1.0, -1.8, 0], O + [1.9, 1.9, 0], O + [-1.9, 1.9, 0], stroke_color=th.FAINT, stroke_width=2, fill_color="#171329", fill_opacity=1)
        back.round_corners(0.15)
        capm = Polygon(O + [-1.7, 2.0, 0], O + [1.7, 2.0, 0], O + [1.1, 2.6, 0], O + [-1.1, 2.6, 0], stroke_width=0, fill_color=SCL, fill_opacity=0.9)
        capm.round_corners(0.15)
        ph = VGroup(*[Circle(radius=0.17, stroke_color="#FFC1DE", stroke_width=1.5, fill_color=PHL, fill_opacity=0.75).move_to(O + [x, y, 0]) for y in (1.6, 1.22) for x in np.linspace(-1.35, 1.35, 7)])
        cb = VGroup(*[Rectangle(width=0.34, height=0.2, stroke_color=CAMB, stroke_width=2, fill_color=CAMB, fill_opacity=0.5).move_to(O + [x, 0.85, 0]) for x in np.linspace(-1.2, 1.2, 8)])
        xy = VGroup()
        for y, sz, xs in [(0.3, 0.28, [-0.9, 0.0, 0.9]), (-0.5, 0.2, [-0.5, 0.5]), (-1.15, 0.12, [-0.25, 0.25]), (-1.55, 0.08, [0.0])]:
            for x in xs:
                xy.add(Circle(radius=sz, stroke_color=XYL, stroke_width=3, fill_color=XYL, fill_opacity=0.25).move_to(O + [x, y, 0]))
        L = [("bundle cap (pericycle)", capm, SCL), ("phloem", ph, PHL), ("cambium", cb, CAMB), ("metaxylem", VGroup(*xy[:3]), XYL), ("protoxylem", VGroup(*xy[-3:]), XYL)]
        labs = VGroup()
        for i, (n_, m_, c_) in enumerate(L):
            labs.add(B.label(n_, [4.4, m_.get_center()[1], 0], m_.get_right() + RIGHT * 0.05, color=c_, size=22))
        for l_ in labs:
            l_[1].align_to(np.array([3.0, 0, 0]), LEFT)
            l_[0].put_start_and_end_on(l_[1].get_left() + LEFT * 0.08, l_[0].get_end())
        pith = T("towards the pith", size=20, color=th.MUTED).move_to(O + [0, -2.15, 0])
        with self.say("Zoom into one bundle. From the outside in: the sclerenchyma cap, the phloem, a strip of cambium, then the xylem. The big metaxylem vessels lie near the cambium, and the small protoxylem points towards the pith. That is endarch xylem."):
            self.play(FadeIn(back), FadeIn(capm), FadeIn(ph), FadeIn(cb), FadeIn(xy), FadeIn(pith))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.25), run_time=2.0)
        words = VGroup(*[T(w_, size=26, color=c_, weight="BOLD") for w_, c_ in [("conjoint", th.INK), ("collateral", PHL), ("open", CAMB), ("endarch", XYL)]]).arrange(RIGHT, buff=0.5).move_to([0.6, -3.0, 0])
        with self.say("Name it in four words. Conjoint: xylem and phloem in one bundle. Collateral: on the same radius, phloem outside. Open: there is cambium between them. And endarch."):
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.2) for w_ in words], lag_ratio=0.4), run_time=2.4)
        self.play(FadeOut(VGroup(back, capm, ph, cb, xy, labs, pith, words)))

    def p4_monocot(self):
        C = np.array([-3.1, -0.15, 0])
        st = B.MonocotStemTS(R=2.75).move_to(C)
        P = st.parts
        cap = B.Captions(self, at=(3.75, 0.1, 0), width=5.3, size=27)
        with self.say("Now a maize stem, Zea mays. The differences are so large that you will never confuse the two once you know them. One layer of epidermis, with a thick cuticle."):
            self.play(FadeIn(P["epi"]))
            cap("Epidermis, thick cuticle", color=EPI, swatch=EPI)
        with self.say("The hypodermis is sclerenchyma, not collenchyma, two or three layers thick. A maize stem is stiff, not flexible."):
            self.play(FadeIn(P["hyp"]))
            cap("Hypodermis: sclerenchyma", color=SCL, swatch=SCL, sub="Stiff, not flexible.")
        with self.say("Inside, there is no cortex, no endodermis, no pericycle and no pith. The whole mass is one continuous ground tissue of parenchyma."):
            self.play(FadeIn(P["ground"]))
            cap("Undifferentiated ground tissue", color=PAR, swatch=PAR, sub="No cortex, endodermis, pericycle or pith.")
        with self.say("And the bundles are scattered all through it. Many of them, and unequal: small and crowded near the edge, large and widely spaced towards the centre. This scattered arrangement is called an atactostele."):
            self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in P["bundles"]], lag_ratio=0.03), run_time=2.4)
            cap("Scattered bundles (atactostele)", color=XYL, swatch=XYL, sub="Numerous; small near the periphery, large towards the centre.")
        self.play(st.animate.scale(0.55).move_to([-5.3, 1.3, 0]), FadeOut(cap.cur))
        cap.cur = None
        mb = B.mono_bundle(5.2).move_to([-0.4, -0.5, 0])
        Q = mb.parts
        L = [("sclerenchyma sheath", Q["sheath"], SCL, 1.9), ("phloem: no phloem parenchyma", Q["phloem"], PHL, 1.0), ("metaxylem vessels", Q["meta"], XYL, 0.1),
             ("protoxylem", Q["proto"], XYL, -0.8), ("lysigenous cavity", Q["cavity"], "#9AA3D8", -1.6)]
        labs = VGroup()
        for n_, m_, c_, y in L:
            g = B.label(n_, [0, y, 0], m_.get_right() + RIGHT * 0.02 if n_ != "sclerenchyma sheath" else m_.get_right(), color=c_, size=22)
            g[1].align_to(np.array([2.2, 0, 0]), LEFT)
            g[0].put_start_and_end_on(g[1].get_left() + LEFT * 0.08, g[0].get_end())
            labs.add(g)
        with self.say("Zoom into one maize bundle. It looks like a little skull. A sheath of sclerenchyma all round. Two big metaxylem vessels for eyes, protoxylem below them, in a Y or V shape."):
            self.play(FadeIn(mb, scale=0.8))
            self.play(FadeIn(labs[0]), FadeIn(labs[2]), FadeIn(labs[3]))
        with self.say("The lowest protoxylem breaks down, leaving a water filled hole: the lysigenous cavity. Above, the phloem has only sieve tubes and companion cells. Phloem parenchyma is absent."):
            self.play(FadeIn(labs[4]), Indicate(Q["cavity"], color=th.AMBER))
            self.play(FadeIn(labs[1]))
        words = VGroup(*[T(w_, size=26, color=c_, weight="BOLD") for w_, c_ in [("conjoint", th.INK), ("collateral", PHL), ("closed", th.CORAL), ("endarch", XYL)]]).arrange(RIGHT, buff=0.5).move_to([0.6, -3.0, 0])
        with self.say("And there is no cambium at all. Conjoint, collateral, endarch, but closed. That single word is why a maize stem can never grow thick in the ordinary way."):
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.2) for w_ in words], lag_ratio=0.3), run_time=1.8)
            self.play(Indicate(words[2], scale_factor=1.25, color=th.CORAL))
        self.play(FadeOut(VGroup(mb, labs, words, st)))
        rows = [["", "Dicot stem", "Monocot stem"], ["hypodermis", "collenchyma", "sclerenchyma"], ["ground tissue", "cortex, endodermis, pericycle, pith", "undifferentiated"],
                ["bundles", "one ring, few, equal", "scattered, many, unequal"], ["bundle type", "conjoint, collateral, open", "conjoint, collateral, closed"],
                ["bundle sheath", "absent (bundle caps instead)", "sclerenchymatous"], ["phloem parenchyma", "present", "absent"], ["lysigenous cavity", "absent", "present"],
                ["medullary rays", "present", "absent"], ["secondary growth", "present", "absent"]]
        tb = B.table(rows, [3.0, 4.7, 4.7], row_h=0.56, size=23, colors=[th.MUTED, th.INK, th.INK]).move_to([0, 0.15, 0])
        with self.say("The comparison table, the long answer every year. Hypodermis, ground tissue, arrangement and number of bundles, bundle type, sheath, phloem parenchyma, the cavity, medullary rays, and secondary growth. Learn it row by row.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))

    def p4_types(self):
        head = T("Types of vascular bundle", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)

        def blobs(pts, col, r=0.13):
            return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(p) for p in pts])

        def ring(n, rr, col, r=0.11):
            return blobs([polar(rr, TAU * k / n) for k in range(n)], col, r)

        icons = [
            ("radial", "roots", VGroup(blobs([[-0.35, 0.35, 0], [0.35, -0.35, 0]], XYL, 0.2), blobs([[0.35, 0.35, 0], [-0.35, -0.35, 0]], PHL, 0.2))),
            ("collateral", "most stems", VGroup(blobs([[x, 0.35, 0] for x in (-0.3, 0, 0.3)], PHL), blobs([[x, -0.3, 0] for x in (-0.3, 0, 0.3)], XYL))),
            ("bicollateral", "Cucurbita, Luffa, Solanum", VGroup(blobs([[x, 0.5, 0] for x in (-0.3, 0, 0.3)], PHL), blobs([[x, 0, 0] for x in (-0.3, 0, 0.3)], XYL), blobs([[x, -0.5, 0] for x in (-0.3, 0, 0.3)], PHL))),
            ("amphivasal", "xylem outside: Dracaena, Yucca", VGroup(ring(10, 0.48, XYL), blobs([[0, 0, 0], [0.18, 0.1, 0], [-0.18, -0.1, 0]], PHL))),
            ("amphicribral", "phloem outside: ferns", VGroup(ring(10, 0.48, PHL), blobs([[0, 0, 0], [0.18, 0.1, 0], [-0.18, -0.1, 0]], XYL))),
        ]
        cards = VGroup()
        for n_, ex, ic in icons:
            box = self.panel(2.4, 2.8)
            g = VGroup(ic, T(n_, size=24, color=th.INK, weight="BOLD"), para(ex, width=2.1, size=18, color=th.BODY, align="center")).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange(RIGHT, buff=0.25).move_to([0, -0.1, 0])
        leg = VGroup(VGroup(Dot(color=XYL), T("xylem", size=20, color=XYL)).arrange(RIGHT, buff=0.1), VGroup(Dot(color=PHL), T("phloem", size=20, color=PHL)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.5).move_to([0, -2.1, 0])
        oc = T("open = cambium present (can thicken)     closed = no cambium", size=24, color=CAMB).move_to([0, -2.8, 0])
        with self.say("You will be asked to name a bundle, not just describe it. Radial: xylem and phloem on different radii, in roots. Conjoint and collateral: phloem only on the outside, as in most stems. Bicollateral: phloem on both sides of the xylem, in the pumpkin family, Cucurbitaceae, and in Solanum.") as v:
            self.play(FadeIn(head), FadeIn(leg))
            for c_ in cards[:3]:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur * 0.25 - 0.5)
        with self.say("And concentric, where one tissue surrounds the other. Amphivasal: xylem surrounds phloem, as in Dracaena and Yucca. Amphicribral: phloem surrounds xylem, as in ferns. Finally, open means a cambium is present, closed means none."):
            self.play(FadeIn(cards[3], shift=UP * 0.2))
            self.play(FadeIn(cards[4], shift=UP * 0.2))
            self.play(FadeIn(oc))
        self.play(FadeOut(VGroup(head, cards, leg, oc)))
        self.tip("Amphi-VAS-al: VAScular tissue (xylem) outside. Amphi-CRIB-ral: cribrum = sieve, so sieve tubes (phloem) outside.",
                 "Two marks that hinge on one syllable. Amphi vas al: vas, vascular, the xylem, is on the outside. Amphi crib ral: cribrum is Latin for a sieve, so the sieve tubes, the phloem, are on the outside.", state="wink")

    def p4_example(self):
        head, prob = B.example_head(self, "A stained TS shows: a one-layered epidermis with a thick cuticle; a hypodermis of cells thickened at their corners; a ring of eight wedge-shaped bundles, each with a strip of thin cells between xylem and phloem; a wide central parenchyma. Identify the organ and class, with reasons.", size=24)
        steps = ["Xylem and phloem in the same bundle, same radius → stem, not root.",
                 "Cuticle → aerial organ. Corner-thickened hypodermis = angular collenchyma → dicot.",
                 "One ring of similar bundles (not scattered) → dicot.",
                 "Thin strip between xylem and phloem = cambium → open bundle.",
                 "Wide central parenchyma = pith → present in dicot stem."]
        rows = VGroup(*[VGroup(T(str(i + 1), size=24, color=self.color, weight="BOLD"), para(s_, width=11.4, size=23, color=th.INK)).arrange(RIGHT, buff=0.3, aligned_edge=UP) for i, s_ in enumerate(steps)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(prob, DOWN, buff=0.4).align_to(prob, LEFT)
        ans = para("Answer: TS of a young dicot stem, with conjoint, collateral, open bundles in one ring.", width=12, size=25, color=th.AMBER, weight="BOLD").next_to(rows, DOWN, buff=0.3).align_to(prob, LEFT)
        blk = VGroup(prob, rows, ans)
        if blk.get_bottom()[1] < -3.25:
            top = prob.get_top()
            blk.scale((top[1] + 3.25) / blk.height).move_to(top, aligned_edge=UP).align_to(head, LEFT)
        says = ["A worked example: reading an unknown slide. Read the clues, then reason one at a time.",
                "First, root or stem? Xylem and phloem lie in the same bundle, on the same radius. So it is a stem.",
                "The cuticle confirms an aerial organ. Thickening at the corners is angular collenchyma, which occurs in dicot stems and never in monocots.",
                "One ring of similar bundles, not scattered ones: a dicot again.",
                "The thin strip between xylem and phloem is the cambium, so the bundles are open.",
                "And the wide central parenchyma is the pith, present in a dicot stem."]
        with self.say(says[0]):
            self.play(FadeIn(head), FadeIn(prob, shift=UP * 0.2))
        for r_, sy in zip(rows, says[1:]):
            with self.say(sy):
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        with self.say("Answer: a transverse section of a young dicot stem, with conjoint, collateral, open bundles in a single ring."):
            self.play(Write(ans))
        self.play(FadeOut(VGroup(head, prob, rows, ans)))
        self.quiz("A vascular bundle in which the phloem completely surrounds the xylem is called",
                  ["amphivasal", "amphicribral", "bicollateral", "radial"], 1,
                  "Pause and think. Phloem all the way round the xylem. What is it called?",
                  "Amphicribral. Cribrum means sieve: the sieve tubes are outside. Amphivasal is the exact reverse, xylem outside, and that is the trap. Bicollateral has phloem on two sides only, not all round.")

    # ------------------------------------------------------------------ part 5: leaf
    def p5(self):
        self.section(4)
        leaf = Line([-3.0, 0.0, 0], [3.0, 0.0, 0], color=CHL, stroke_width=14)
        rays = VGroup(*[Arrow([x, 2.8, 0], [x, 0.35, 0], buff=0, color=th.AMBER, stroke_width=4) for x in np.linspace(-2.6, 2.6, 6)])
        top = T("upper side: full sun", size=24, color=th.AMBER).move_to([0, 3.15, 0])
        bot = T("lower side: shade", size=24, color=th.MUTED).move_to([0, -0.7, 0])
        dv = T("dorsiventral", size=36, color=th.INK, weight="BOLD").move_to([0, -2.0, 0])
        with self.say("A typical dicot leaf is held flat, so its upper surface gets far more light than its lower. Its anatomy is two faced to match, and we call it dorsiventral."):
            self.play(Create(leaf), LaggedStart(*[GrowArrow(r_) for r_ in rays], lag_ratio=0.1), FadeIn(top))
            self.play(FadeIn(bot), Write(dv))
        self.play(FadeOut(VGroup(leaf, rays, top, bot, dv)))
        lf = B.DicotLeafTS(w=11.0).move_to([0, 0.7, 0])
        P = lf.parts
        cap = B.Captions(self, at=(0, -2.45, 0), width=12, size=26)
        seq = [(["cuticle", "ue"], "Upper epidermis: one layer with a thick cuticle, and very few stomata or none.", "Upper epidermis + thick cuticle", EPI),
               (["palisade"], "Below it, the palisade parenchyma: one to three layers of tall, closely packed cells standing on end, crammed with chloroplasts. Most photosynthesis happens here.", "Palisade parenchyma: most photosynthesis", CHL),
               (["spongy"], "Then the spongy parenchyma: loose, irregular cells with big air spaces between them, and fewer chloroplasts. This is the tissue built for gas exchange.", "Spongy parenchyma: air spaces for gas exchange", PAR),
               (["le", "stomata"], "The lower epidermis has a thinner cuticle and many stomata, each opening into an air chamber, the substomatal cavity. Stomata mainly on the lower side make the leaf hypostomatic, which saves water, because the lower side is cooler.", "Lower epidermis: many stomata (hypostomatic)", EPI),
               (["vein"], "And the veins. Each bundle is conjoint, collateral and closed, with xylem towards the upper side and phloem towards the lower side, exactly as you would expect if the leaf were a flattened piece of stem. A sheath of parenchyma surrounds it, and the venation is reticulate.", "Vein: xylem up, phloem down; parenchyma sheath", XYL)]
        for keys, sy, title, col in seq:
            with self.say(sy):
                self.play(*[FadeIn(P[k_]) for k_ in keys], run_time=1.0)
                cap(title, color=col, swatch=col)
        st0 = P["stomata"][1].get_center()
        co2 = VGroup(*[Dot(radius=0.07, color=th.SKY) for _ in range(5)])
        paths = [VMobject().set_points_smoothly([st0 + DOWN * 0.6, st0 + UP * 0.25, st0 + UP * 0.9 + RIGHT * (0.3 * i - 0.6), st0 + UP * 1.6 + RIGHT * (0.35 * i - 0.7)]) for i in range(5)]
        for d_, p_ in zip(co2, paths):
            d_.move_to(p_.get_start())
        with self.say("Follow a molecule of carbon dioxide. In through a stoma, into the cavity, through the spongy air spaces, and up to a palisade cell. The whole leaf is a gas exchange machine."):
            cap("CO₂: stoma → substomatal cavity → spongy air spaces → palisade", color=th.SKY)
            self.play(LaggedStart(*[MoveAlongPath(d_, p_) for d_, p_ in zip(co2, paths)], lag_ratio=0.2), run_time=3.0)
        self.play(FadeOut(VGroup(lf, co2)))
        cap.clear()
        self.p5_mono()

    def p5_mono(self):
        leaf = Line([0, -2.6, 0], [0, 2.4, 0], color=CHL, stroke_width=14)
        r1 = VGroup(*[Arrow([-3.0, y, 0], [-0.35, y, 0], buff=0, color=th.AMBER, stroke_width=4) for y in np.linspace(-2, 1.8, 5)])
        r2 = VGroup(*[Arrow([3.0, y, 0], [0.35, y, 0], buff=0, color=th.AMBER, stroke_width=4) for y in np.linspace(-2, 1.8, 5)])
        ib = T("isobilateral", size=36, color=th.INK, weight="BOLD").move_to([4.4, -2.6, 0])
        with self.say("A grass or maize leaf stands more or less upright, so both its surfaces get about the same light. Its anatomy is the same on both sides: isobilateral."):
            self.play(Create(leaf), LaggedStart(*[GrowArrow(a_) for a_ in [*r1, *r2]], lag_ratio=0.05), run_time=1.6)
            self.play(Write(ib))
        self.play(FadeOut(VGroup(leaf, r1, r2, ib)))
        lf = B.MonocotLeafTS(w=11.0).move_to([0, 0.75, 0])
        P = lf.parts
        cap = B.Captions(self, at=(0, -2.3, 0), width=12, size=26)
        seq = [(["cuticle", "ue", "le", "stomata"], "Both epidermes are cuticularised, and both carry stomata in roughly equal numbers. The leaf is amphistomatic. The guard cells are dumb-bell shaped, not kidney shaped as in a dicot.", "Stomata on both surfaces (amphistomatic); dumb-bell guard cells", EPI),
               (["mesophyll"], "The mesophyll is not differentiated. No palisade, no spongy layer: just uniform chlorenchyma with small air spaces.", "Mesophyll undifferentiated", CHL),
               (["bundles", "girders"], "The bundles run in a parallel row, large alternating with small, each inside a sheath of sclerenchyma that often extends as a girder to both surfaces. The venation is parallel.", "Parallel bundles; sclerenchyma sheaths and girders", SCL),
               (["bulliform"], "And in the upper epidermis of grasses, groups of large, thin walled, water filled cells: the bulliform, or motor, cells.", "Bulliform (motor) cells in the upper epidermis", "#A8F0FF")]
        for keys, sy, title, col in seq:
            with self.say(sy):
                self.play(*[FadeIn(P[k_]) for k_ in keys], run_time=1.0)
                cap(title, color=col, swatch=col)
        self.play(FadeOut(lf))
        cap.clear()
        flat = ArcBetweenPoints([-3.6, 0.2, 0], [3.6, 0.2, 0], angle=-0.15, color=CHL, stroke_width=16)
        rolled = VMobject(stroke_color=CHL, stroke_width=16).set_points_smoothly([polar(0.9 + 0.25 * t, PI * 0.5 + t * 1.15 * PI) + np.array([-0.0, 0.2, 0]) for t in np.linspace(-1, 1, 60)])
        bl = VGroup(*[Ellipse(width=0.42, height=0.6, stroke_color="#A8F0FF", stroke_width=3, fill_color="#1D3F52", fill_opacity=1).move_to([x, 0.62, 0]) for x in (-1.2, 0, 1.2)])
        sun = T("a hot afternoon in the Terai", size=26, color=th.AMBER).move_to([0, 2.6, 0])
        with self.say("Here is what the bulliform cells do. On a hot afternoon in a Terai maize field, the plant loses water. The bulliform cells lose turgor and shrink, and the leaf rolls inwards, upper side in. A rolled leaf exposes fewer stomata to the dry air, and transpiration falls."):
            self.play(Create(flat), FadeIn(bl))
            self.play(FadeIn(sun))
            self.play(bl.animate.scale(0.45), run_time=1.0)
            self.play(Transform(flat, rolled), FadeOut(bl), run_time=2.0)
            nb = B.neby_in(self, "surprised", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(flat, sun)))
        rows = [["", "Dorsiventral (dicot)", "Isobilateral (monocot)"], ["orientation", "horizontal", "more or less vertical"], ["stomata", "mostly lower (hypostomatic)", "both surfaces (amphistomatic)"],
                ["guard cells", "kidney-shaped", "dumb-bell shaped"], ["mesophyll", "palisade + spongy", "undifferentiated"], ["bulliform cells", "absent", "present (upper epidermis)"],
                ["bundle sheath", "parenchymatous", "sclerenchymatous, girders"], ["venation", "reticulate", "parallel"], ["examples", "Mangifera, Helianthus, Ficus", "Zea mays, Oryza, Cynodon"]]
        tb = B.table(rows, [2.8, 4.8, 4.8], row_h=0.6, size=23, colors=[th.MUTED, th.INK, th.INK]).move_to([0, 0.25, 0])
        with self.say("Four of these differences make a full four mark answer. Orientation, stomata, guard cells, mesophyll, bulliform cells, bundle sheath, venation, and examples.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("Bulliform cells occur in the",
                  ["upper epidermis of a grass leaf", "lower epidermis of a dicot leaf", "mesophyll of a maize leaf", "hypodermis of a dicot stem"], 0,
                  "Pause and think. Where are bulliform cells found?",
                  "The upper epidermis of a grass leaf: large, thin walled motor cells that lose turgor and roll the leaf. A dicot leaf has none, and they are epidermal cells, not mesophyll.")

    # ------------------------------------------------------------------ part 6: secondary growth
    def p6(self):
        self.section(5)
        self.p6_why()
        self.p6_ring()
        self.p6_file()
        self.p6_years()
        self.p6_annual()
        self.p6_heart()
        self.p6_cork()
        self.p6_order()
        self.p6_monocot()
        self.p6_root()

    def p6_why(self):
        ground = Line([-6.5, -2.6, 0], [6.5, -2.6, 0], color=th.FAINT, stroke_width=3)
        sun = VGroup(*[Line([-0.2, 2.3, 0], [0.4, 1.7, 0], color=th.AMBER, stroke_width=3).rotate(TAU * k / 10, about_point=[-0.2, 2.6, 0]) for k in range(10)],
                     Circle(radius=0.25, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to([-0.2, 2.6, 0]))
        sun.set_opacity(0)
        sunflower = VGroup(Line([-3.5, -2.6, 0], [-3.5, -0.2, 0], color=PAR, stroke_width=7),
                           Circle(radius=0.38, fill_color="#FFD23F", fill_opacity=1, stroke_color="#E9A800", stroke_width=3).move_to([-3.5, 0.05, 0]),
                           Dot([-3.5, 0.05, 0], radius=0.17, color="#6B3E1F"))
        sal = VGroup(Polygon([2.8, -2.6, 0], [3.7, -2.6, 0], [3.4, 1.4, 0], [3.1, 1.4, 0], stroke_width=0, fill_color="#7A5534", fill_opacity=1),
                     *[Circle(radius=r, fill_color="#2E7D32", fill_opacity=0.95, stroke_width=0).move_to(p) for r, p in
                       [(0.9, [3.25, 2.1, 0]), (0.7, [2.4, 1.6, 0]), (0.75, [4.1, 1.7, 0])]])
        l1 = T("sunflower · 1 m · stands on primary tissue", size=22, color=th.BODY).move_to([-3.5, -3.0, 0])
        l2 = T("sal · 30 m · needs wood", size=22, color=th.BODY).move_to([3.25, -3.0, 0])
        with self.say("A sunflower a metre tall can stand on its primary tissues alone. A sal tree thirty metres tall cannot. As a woody plant adds height and leaves, its young body can neither carry the load nor pipe enough water to the crown. So it adds girth."):
            self.play(Create(ground), FadeIn(sunflower, shift=UP * 0.3), FadeIn(l1))
            self.play(FadeIn(sal, shift=UP * 0.3), FadeIn(l2))
            self.play(sal[0].animate.stretch(1.6, 0), run_time=1.6)
        self.play(FadeOut(VGroup(ground, sunflower, sal, l1, l2, sun)))
        d = self.callout("key", "Secondary growth is the increase in thickness, or girth, of a plant axis, brought about by the lateral meristems: the vascular cambium and the cork cambium. It happens in the stems and roots of dicots and gymnosperms; normally not in monocots, and never in leaves.", width=11)
        d.move_to([0, 0.2, 0])
        with self.say("That is secondary growth: the increase in thickness of a stem or root, made by two lateral meristems, the vascular cambium and the cork cambium. It happens in dicots and gymnosperms. Monocots normally do not have it, and leaves never do."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))

    def p6_ring(self):
        z = ValueTracker(1.95)
        f = ValueTracker(0.0)
        hi = ValueTracker(0.0)
        stem = always_redraw(lambda: sg_frame(0.0, z.get_value(), f.get_value(), rays=hi.get_value()))
        cap = B.Captions(self, at=(3.75, 0.2, 0), width=5.2, size=27)
        self.cap = cap
        head = T("Step 1 · the cambial ring", size=30, color=CAMB, weight="BOLD").move_to([3.75, 2.7, 0])
        with self.say("Step one. Start from the young dicot stem you met in part four, simplified. A ring of eight bundles, each with phloem outside and xylem inside."):
            self.play(FadeIn(stem), FadeIn(head))
            cap("A young dicot stem: a ring of open bundles", sub="Phloem (pink) outside, xylem (blue) inside, pith at the centre.")
        cells = VGroup(*[Arc(radius=1.95 * (RX0 + 0.02), start_angle=a - HALF, angle=2 * HALF, stroke_color=CAMB, stroke_width=10).shift(SGC) for a in BUNDLES])
        with self.say("Inside each bundle, between the xylem and the phloem, there is already a strip of cambium. It is called the fascicular, or intrafascicular, cambium, because it lies inside the bundle, the fascicle."):
            cap("Fascicular cambium", color=CAMB, swatch=CAMB, sub="A strip of cambium already present inside each bundle, between xylem and phloem.")
            self.play(LaggedStart(*[ShowPassingFlash(c.copy(), time_width=0.6) for c in cells], lag_ratio=0.1), run_time=1.6)
        with self.say("Between the bundles there is only parenchyma, the medullary rays. Watch the ray cells that lie exactly in line with the cambium strips."):
            cap("Medullary rays", color=PAR, swatch=PAR, sub="Parenchyma between the bundles, joining pith to cortex.")
            self.play(hi.animate.set_value(1.0), run_time=1.0)
        with self.say("They dedifferentiate. They regain the power to divide, and become a new meristem: the interfascicular cambium, the cambium between the bundles. It grows across each gap from both sides."):
            cap("Interfascicular cambium", color="#FFD99A", swatch="#FFD99A", sub="Ray cells in line with the strips dedifferentiate and become meristematic.")
            self.play(f.animate.set_value(0.97), hi.animate.set_value(0.4), run_time=3.2, rate_func=rate_functions.ease_in_out_sine)
        self.play(f.animate.set_value(1.0), run_time=0.2)
        self.sfx("shimmer", gain=-10)
        glow = Circle(radius=1.95 * (RX0 + 0.02), stroke_color=CAMB, stroke_width=14).shift(SGC)
        with self.say("The two kinds join end to end, and the result is one continuous cambial ring, one cell thick, running right round the stem. This ring is the vascular cambium."):
            cap("A complete cambial ring", color=CAMB, swatch=CAMB, sub="Fascicular plus interfascicular cambium: the vascular cambium, one cell thick.")
            self.play(ShowPassingFlash(glow, time_width=0.5), run_time=1.4)
            self.play(hi.animate.set_value(0.0), run_time=0.6)
        self.stem_z, self.stem_f = z, f
        self.play(FadeOut(head), FadeOut(stem))
        self.remove(stem)
        cap.clear()

    def p6_file(self):
        cap = self.cap
        head = T("Step 2 · the ring divides", size=30, color=CAMB, weight="BOLD").move_to([3.75, 2.7, 0])
        h, w, x = 0.4, 1.4, -3.0
        y0 = -2.95

        def cell(kind):
            col = {"x": XYL, "c": CAMB, "p": PHL, "o": PAR, "px": XYL, "pp": PHL}[kind]
            sw = {"x": 6, "px": 6, "c": 3, "p": 2.5, "pp": 2.5, "o": 2}[kind]
            fo = {"x": 0.12, "px": 0.3, "c": 0.45, "p": 0.3, "pp": 0.18, "o": 0.2}[kind]
            r = RoundedRectangle(corner_radius=0.07, width=w, height=h * 0.9, stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fo)
            return r

        kinds = ["px", "c", "pp", "o", "o"]
        stack = [cell(k_).move_to([x, y0 + h * (i + 0.5), 0]) for i, k_ in enumerate(kinds)]
        ci = 1
        inner = Arrow([x - 1.5, -1.9, 0], [x - 1.5, -3.0, 0], buff=0, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        outer = Arrow([x - 1.5, 1.4, 0], [x - 1.5, 2.5, 0], buff=0, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        li = T("towards the pith", size=20, color=th.MUTED).next_to(inner, LEFT, buff=0.15)
        lo = T("towards the bark", size=20, color=th.MUTED).next_to(outer, LEFT, buff=0.15)
        nx, npl = [0], [0]
        cx = VGroup(T("secondary xylem", size=22, color=XYL), T("0", size=34, color=XYL, weight="BOLD")).arrange(DOWN, buff=0.1).move_to([0.25, -1.3, 0])
        cp = VGroup(T("secondary phloem", size=22, color=PHL), T("0", size=34, color=PHL, weight="BOLD")).arrange(DOWN, buff=0.1).move_to([0.25, 1.3, 0])
        with self.say("Step two. Zoom into one radial file of cells, a single row running from the pith outwards. In the middle sits one cambium cell."):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in stack], lag_ratio=0.12), GrowArrow(inner), GrowArrow(outer), FadeIn(li), FadeIn(lo))
            cap("One radial file of cells", sub="Primary xylem at the bottom, then the cambium cell, then primary phloem and cortex.")
            self.play(Indicate(stack[1], color=CAMB, scale_factor=1.12))
        self.play(FadeIn(cx), FadeIn(cp), run_time=0.4)

        def divide(side, rt=0.7):
            nonlocal ci
            c = stack[ci]
            wall = Line(c.get_left() + RIGHT * 0.1, c.get_right() + LEFT * 0.1, color=WHITE, stroke_width=4).move_to(c)
            self.sfx("pop", gain=-14)
            self.play(Create(wall), run_time=rt * 0.35)
            if side == "in":
                new = cell("x").move_to(c)
                self.play(*[m.animate.shift(UP * h) for m in stack[ci:]], FadeIn(new, scale=0.6), FadeOut(wall), run_time=rt * 0.65)
                stack.insert(ci, new)
                ci += 1
                nx[0] += 1
                self.remove(cx[1])
                cx[1] = T(str(nx[0]), size=34, color=XYL, weight="BOLD").move_to(cx[1])
                self.add(cx[1])
            else:
                new = cell("p").move_to(c.get_center() + UP * h)
                self.play(*[m.animate.shift(UP * h) for m in stack[ci + 1:]], FadeIn(new, scale=0.6), FadeOut(wall), run_time=rt * 0.65)
                stack.insert(ci + 1, new)
                npl[0] += 1
                self.remove(cp[1])
                cp[1] = T(str(npl[0]), size=34, color=PHL, weight="BOLD").move_to(cp[1])
                self.add(cp[1])

        with self.say("The cambium cell divides tangentially, with the new wall parallel to the surface. One daughter stays a cambium cell. The other, cut off on the inner face, matures into secondary xylem: wood."):
            cap("Cut off inwards: secondary xylem", color=XYL, swatch=XYL, sub="Tangential (periclinal) division. The inner daughter becomes wood.")
            divide("in", 1.4)
        with self.say("Next time the cell divides, the daughter cut off on the outer face becomes secondary phloem, the bast."):
            cap("Cut off outwards: secondary phloem", color=PHL, swatch=PHL, sub="The outer daughter becomes bast. The cambium cell itself always remains.")
            divide("out", 1.4)
        with self.say("Keep it going. Inwards, inwards, outwards, inwards, inwards, inwards. The cambium makes far more xylem than phloem, often several times more. That is why a tree trunk is almost all wood."):
            cap("Far more xylem than phloem", sub="That is why a trunk is overwhelmingly wood, with a thin skin of phloem outside it.")
            for s_ in ["in", "in", "out", "in", "in", "in"]:
                divide(s_, 0.6)
        arr = Arrow([x + 1.0, stack[ci].get_center()[1] - 2.0, 0], [x + 1.0, stack[ci].get_center()[1], 0], buff=0, color=CAMB, stroke_width=5)
        with self.say("And look where the cambium cell has gone. Each new xylem cell is added behind it, so the cambium itself is pushed steadily outwards, and everything outside it, the primary phloem and the cortex, is shoved outwards too."):
            cap("The cambium is pushed outwards", color=CAMB, sub="New wood is laid down inside it, so the ring keeps moving out.")
            self.play(GrowArrow(arr), Indicate(stack[ci], color=CAMB, scale_factor=1.12), run_time=1.4)
        self.play(FadeOut(VGroup(head, *stack, inner, outer, li, lo, cx, cp, arr)))
        cap.clear()

    def p6_years(self):
        cap = self.cap
        t = ValueTracker(0.0)
        z = ValueTracker(1.95)
        stem = always_redraw(lambda: sg_frame(t.get_value(), z.get_value(), 1.0))
        yr = VGroup(T("year", size=24, color=th.MUTED), Integer(0, font_size=56, color=th.INK)).arrange(DOWN, buff=0.05).move_to([0.6, 2.7, 0])
        yr[1].add_updater(lambda m: m.set_value(int(t.get_value() + 1e-6)))
        self.add(stem)
        with self.say("Now step back and let the years run. First zoom out, so there is room to grow."):
            self.play(FadeIn(stem), run_time=0.5)
            self.play(z.animate.set_value(1.0), run_time=1.6)
            cap("The same stem, zoomed out", sub="Cambium ring in amber. Now watch it work.")
        self.play(FadeIn(yr))
        with self.say("Year one. A band of new wood builds up inside the ring. A thin band of new phloem forms outside it. The ring and everything outside it move outwards.") as v:
            cap("Secondary xylem inside, secondary phloem outside", sub="The wood (blue) thickens from the inside; the bast (pink) is a thin band.")
            self.play(t.animate.set_value(1.0), run_time=v.dur * 0.85, rate_func=rate_functions.linear)
        with self.say("The primary phloem, which lies outside the ring, is squeezed between the growing wood and the cortex. Year after year it is crushed flat, until it is obliterated.") as v:
            cap("Primary phloem: crushed", color=PHL, swatch=PHL, sub="Pressed between the expanding wood and the cortex, then obliterated.")
            self.play(t.animate.set_value(2.0), run_time=v.dur * 0.85, rate_func=rate_functions.linear)
        pxh = VGroup(*[AnnularSector(inner_radius=RP + 0.02, outer_radius=RX0, angle=2 * HALF, start_angle=a - HALF, stroke_color=WHITE, stroke_width=3, fill_opacity=0).shift(SGC) for a in BUNDLES])
        with self.say("The primary xylem, on the other hand, survives. It stays where it was, squeezed against the pith at the very centre, wrapped in all the new wood."):
            cap("Primary xylem: survives at the centre", color=XYL, swatch=XYL, sub="Pressed against the pith, inside all the secondary wood.")
            self.play(LaggedStart(*[ShowPassingFlash(p_.copy(), time_width=0.7) for p_ in pxh], lag_ratio=0.08), run_time=1.6)
        rays = VGroup(*[Line(polar(RX0 + 0.05, TAU * j / 16 + PI / 16), polar(sg_geom(2.0)["rx"] - 0.05, TAU * j / 16 + PI / 16), color=COL, stroke_width=4).shift(SGC) for j in range(16)])
        with self.say("Some cambium cells stay parenchymatous. They lay down radial ribbons of living cells running through the wood: the secondary medullary rays. They carry water and food sideways, across the stem, and store starch."):
            cap("Secondary medullary rays", color=COL, swatch=COL, sub="Radial files of living parenchyma through the wood: sideways transport and storage.")
            self.play(LaggedStart(*[ShowPassingFlash(r_.copy(), time_width=0.8) for r_ in rays], lag_ratio=0.05), run_time=2.0)
        with self.say("Two more years. Each year's wood is a ring of its own, with a sharp edge where one season stops and the next begins. Hold that thought.") as v:
            cap("Each year leaves a ring", sub="A sharp boundary every year: we will read these in a moment.")
            self.play(t.animate.set_value(4.0), run_time=v.dur * 0.85, rate_func=rate_functions.linear)
        with self.say("But the epidermis and cortex outside are not dividing. They cannot stretch for ever. As the stem widens, they split. The plant needs a new skin, and that is step three, coming up."):
            cap("The outer skin tears", color=EPI, swatch=EPI, sub="The epidermis and cortex cannot keep up with the widening stem.")
            nb = B.neby_in(self, "surprised", height=1.3)
        B.neby_out(self, nb)
        yr[1].clear_updaters()
        self.play(FadeOut(stem), FadeOut(yr))
        self.remove(stem)
        cap.clear()

    def p6_annual(self):
        head = T("Annual rings", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cols = VGroup()
        x = -4.75
        years = []
        for y in range(3):
            yg = VGroup()
            for c in range(7):
                s = 0.6 - 0.054 * c
                sw = 1.5 + c * 1.1
                colm = VGroup()
                n = int(2.3 / s)
                for j in range(n):
                    colm.add(Square(side_length=s * 0.92, stroke_color=XYL, stroke_width=sw, fill_color=XYL, fill_opacity=0.06 + 0.04 * c)
                             .move_to([x + s / 2, 0.75 - (n * s) / 2 + s * (j + 0.5), 0]))
                x += s
                yg.add(colm)
            years.append(yg)
            cols.add(yg)
        bounds = VGroup(*[DashedLine([years[y][-1].get_right()[0], -0.5, 0], [years[y][-1].get_right()[0], 2.0, 0], color=th.AMBER, stroke_width=3) for y in range(2)])
        cap = B.Captions(self, at=(0, -2.15, 0), width=11.5, size=27)
        dirn = Arrow([-4.7, -0.75, 0], [4.7, -0.75, 0], buff=0, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.03)
        dl = T("pith side  →  bark side", size=20, color=th.MUTED).next_to(dirn, DOWN, buff=0.08)
        with self.say("Here is that sharp edge, cell by cell. In spring, water is plentiful and growth is fast. The cambium cuts off wide vessels with thin walls. That is spring wood, or early wood: light in colour and low in density."):
            self.play(FadeIn(head), GrowArrow(dirn), FadeIn(dl))
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.1) for c_ in years[0][:3]], lag_ratio=0.3), run_time=1.6)
            cap("Spring wood (early wood)", color=XYL, sub="Wide vessels, thin walls: light and low in density.")
        with self.say("As autumn comes, and the dry cold season, activity slows. The vessels get narrow and their walls thick. That is autumn wood, or late wood: dark and dense."):
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.1) for c_ in years[0][3:]], lag_ratio=0.3), run_time=1.6)
            cap("Autumn wood (late wood)", color="#9FDDF5", sub="Narrow vessels, thick walls: dark and dense.")
        br = BraceBetweenPoints(years[0][0].get_corner(UL) + UP * 0.08, years[0][-1].get_corner(UR) + UP * 0.08, direction=UP, color=th.AMBER)
        bl = T("one annual ring = one year", size=24, color=th.AMBER, weight="BOLD").next_to(br, UP, buff=0.08)
        with self.say("Next spring, wide cells again, right next to the narrow ones. That sudden jump is the edge you see on a cut log. One band of spring wood plus the band of autumn wood after it makes one annual ring, or growth ring: one year's growth."):
            self.play(FadeIn(years[1][:3], shift=RIGHT * 0.1), run_time=0.8)
            self.play(Create(bounds[0]))
            self.play(GrowFromCenter(br), FadeIn(bl))
            cap("Spring + autumn wood = one annual ring", color=th.AMBER)
            self.play(FadeIn(years[1][3:]), FadeIn(years[2]), Create(bounds[1]), run_time=1.4)
        self.play(FadeOut(VGroup(cols, bounds, br, bl, dirn, dl)))
        cap.clear()
        widths = [0.3, 0.29, 0.27, 0.11, 0.28, 0.26, 0.25, 0.09, 0.24, 0.22]
        C = np.array([-3.0, -0.45, 0])
        rings = VGroup()
        r = 0.15
        disc = VGroup(Circle(radius=0.15, fill_color=SAP, fill_opacity=1, stroke_width=0).move_to(C))
        for wv in widths:
            r += wv
            disc.add(Annulus(inner_radius=r - wv, outer_radius=r, fill_color=SAP, fill_opacity=1, stroke_width=0).move_to(C))
            rings.add(Circle(radius=r, stroke_color="#8A5A2B", stroke_width=4).move_to(C))
        bark = Annulus(inner_radius=r, outer_radius=r + 0.14, fill_color="#5A3A22", fill_opacity=1, stroke_width=0).move_to(C)
        cnt = VGroup(T("rings counted", size=24, color=th.MUTED), Integer(0, font_size=80, color=th.AMBER)).arrange(DOWN, buff=0.1).move_to([2.6, 1.0, 0])
        with self.say("So a cut stump is a calendar. Count the rings from the centre outwards, and you have the age of the tree. This is dendrochronology.") as v:
            self.play(FadeIn(disc), FadeIn(bark), FadeIn(cnt))
            per = (v.dur - 1.5) / len(rings)
            for i, rr in enumerate(rings):
                self.sfx("tick", gain=-14)
                self.play(Create(rr), cnt[1].animate.set_value(i + 1), run_time=max(0.2, per))
        thin = VGroup(rings[3].copy(), rings[7].copy()).set_stroke(th.CORAL, width=7)
        tl = para("Narrow rings: dry or cold years. The widths are a record of past climate.", width=5.2, size=24, color=th.CORAL).move_to([2.9, -1.0, 0])
        with self.say("Ten rings, ten years. And the widths are a diary. These two narrow rings are bad years, a drought or a cold summer. That is how tree rings are used to reconstruct past climate."):
            self.play(Create(thin), FadeIn(tl))
        self.play(FadeOut(VGroup(thin, tl)))
        warn = self.callout("careful", "Rings give the age only where the seasons are sharply different. In the hot, wet Terai the cambium may work almost all year, and a mid-season drought can lay down a false ring.", width=5.6, size=24)
        warn.move_to([3.0, -0.4, 0])
        with self.say("One qualification is worth a mark. Annual rings are reliable only where the growing season is sharply defined. In the hot, wet Terai, and in the tropics, the cambium may work almost all year, so the rings are faint. A drought in mid season can even lay down a false ring. So write: counting rings gives the age of a tree in regions with a distinct growing season."):
            self.play(FadeOut(cnt), FadeIn(warn, shift=UP * 0.2))
        self.play(FadeOut(warn))
        self.stump = VGroup(disc, rings, bark)
        self.stump_r = [0.15 + sum(widths[:i + 1]) for i in range(len(widths))]
        self.play(FadeOut(head))

    def p6_heart(self):
        disc, rings, bark = self.stump
        C = np.array([-3.0, -0.45, 0])
        rr = self.stump_r
        heart = Circle(radius=rr[5], fill_color=HEART, fill_opacity=1, stroke_width=0).move_to(C)
        hl = B.label("heartwood (duramen)", [1.9, 1.6, 0], C + polar(rr[3], 0.6), color="#E0A877", size=24)
        sl = B.label("sapwood (alburnum)", [1.9, -2.4, 0], C + polar((rr[6] + rr[9]) / 2, -0.5), color=SAP, size=24)
        h_txt = para("dead, dark, hard; tannins, resins and gums; vessels plugged; only mechanical support", width=4.4, size=21, color=th.BODY).next_to(hl[1], DOWN, aligned_edge=LEFT, buff=0.12)
        s_txt = para("outer, lighter, living parenchyma; the only wood that carries water", width=4.4, size=21, color=th.BODY).next_to(sl[1], UP, aligned_edge=LEFT, buff=0.12)
        self.add(heart)
        self.bring_to_front(rings, bark)
        heart.set_opacity(0)
        with self.say("As a trunk ages, the oldest wood at the centre stops conducting. Its parenchyma dies, and tannins, resins, gums and oils are deposited in its cells. It turns dark. This is heartwood, or duramen: hard, durable, resistant to insects and decay, and purely mechanical."):
            self.play(heart.animate.set_opacity(1), run_time=1.6)
            self.play(FadeIn(hl), FadeIn(h_txt))
        with self.say("The outer, lighter zone is sapwood, or alburnum. It still has living parenchyma and working vessels, and it is the only part of the wood that actually carries the transpiration stream."):
            self.play(FadeIn(sl), FadeIn(s_txt))
        self.play(FadeOut(VGroup(hl, h_txt, sl, s_txt)))
        V = np.array([3.0, -0.2, 0])
        wall_l = Line(V + [-0.55, -2.2, 0], V + [-0.55, 2.2, 0], color=XYL, stroke_width=6)
        wall_r = Line(V + [0.55, -2.2, 0], V + [0.55, 2.2, 0], color=XYL, stroke_width=6)
        pits = VGroup(*[Line(V + [sx * 0.55, y, 0], V + [sx * 0.55, y + 0.22, 0], color=th.BG, stroke_width=8) for sx, y in [(-1, -1.3), (1, -0.4), (-1, 0.5), (1, 1.3)]])
        par = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.8, height=0.75, stroke_color=PAR, stroke_width=2, fill_color=PARF, fill_opacity=1).move_to(V + [sx * 1.0, y + 0.11, 0])
                       for sx, y in [(-1, -1.3), (1, -0.4), (-1, 0.5), (1, 1.3)]])
        flow = B.Flow(V + [0, -2.1, 0], V + [0, 2.1, 0], n=9, color=WATER, speed=0.8, width=0.6)
        vl = T("vessel", size=24, color=XYL).next_to(wall_r, UP, buff=0.12).shift(LEFT * 0.55)
        with self.say("Zoom into one vessel of the young sapwood. Water streams up it. Living parenchyma cells sit against its wall, connected through pits."):
            self.play(Create(wall_l), Create(wall_r), FadeIn(pits), FadeIn(par), FadeIn(vl))
            self.add(flow)
            self.wait(1.5)
        tyl = VGroup()
        for sx, y in [(-1, -1.3), (1, -0.4), (-1, 0.5), (1, 1.3)]:
            b = Ellipse(width=1.05, height=0.62, stroke_color=PAR, stroke_width=2.5, fill_color="#2E5A3C", fill_opacity=1).move_to(V + [sx * 0.03, y + 0.11, 0])
            tyl.add(b)
        tl = T("tyloses", size=28, color=PAR, weight="BOLD").next_to(wall_l, LEFT, buff=0.3).shift(UP * 1.6)
        with self.say("In heartwood, these parenchyma cells balloon out through the pits into the vessel. The balloons are called tyloses, and they plug the vessel shut. The water stops."):
            self.play(LaggedStart(*[GrowFromPoint(b, V + [-sx * 0.55, b.get_center()[1] - V[1], 0]) for b, (sx, _) in zip(tyl, [(-1, 0), (1, 0), (-1, 0), (1, 0)])], lag_ratio=0.3), FadeIn(tl), run_time=2.4)
            self.play(FadeOut(flow), run_time=0.6)
        self.remove(flow)
        val = para("Sal, sisau and teak are prized for their heartwood.", width=5.5, size=26, color=th.AMBER).move_to([2.6, -3.0, 0])
        with self.say("That dead, plugged, chemically protected heartwood is the valuable timber. Sal, sisau and teak are prized for it."):
            self.play(FadeIn(val))
        self.play(FadeOut(VGroup(wall_l, wall_r, pits, par, tyl, tl, vl, val, disc, rings, bark, heart)))

    def p6_cork(self):
        cap = self.cap
        k = ValueTracker(0.0)
        stem = always_redraw(lambda: sg_frame(4.0, 1.0, 1.0, k=k.get_value()))
        head = T("Step 3 · cork cambium and bark", size=30, color=CORK, weight="BOLD").move_to([3.75, 2.7, 0])
        with self.say("Step three. Back to our stem, four years old, its skin torn. A second lateral meristem now appears in the outer cortex, or the hypodermis. Cells there dedifferentiate into the cork cambium, the phellogen."):
            self.play(FadeIn(stem), FadeIn(head))
            cap("Cork cambium (phellogen)", color="#FFE2B8", swatch="#FFE2B8", sub="Arises by dedifferentiation in the hypodermis or outer cortex. In a root: from the pericycle.")
            self.play(k.animate.set_value(0.15), run_time=1.2)
        with self.say("It too divides tangentially. Outwards it cuts off cork, the phellem. Its walls are soaked with suberin, the cells die, and the layer becomes waterproof and gas proof. Inwards it cuts off phelloderm, a thin layer of living cells sometimes called secondary cortex.") as v:
            cap("Cork cambium → cork + phelloderm", color=CORK, swatch=CORK, sub="Outwards: phellem (cork), suberised and dead. Inwards: phelloderm, living.")
            self.play(k.animate.set_value(1.0), run_time=v.dur * 0.8)
        G = sg_geom(4.0)
        rk = G["rout"] - 0.13
        peri = VGroup(Annulus(inner_radius=rk - 0.05, outer_radius=rk + 0.2, stroke_color=WHITE, stroke_width=3, fill_opacity=0).shift(SGC))
        with self.say("Phellogen, phellem and phelloderm, taken together, are called the periderm."):
            cap("Periderm = phellogen + phellem + phelloderm", color="#FFE2B8")
            self.play(ShowPassingFlash(peri[0].copy().set_stroke(WHITE, 6), time_width=0.6), run_time=1.4)
        bark = Annulus(inner_radius=G["rc"], outer_radius=G["rout"] + 0.22, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.28).shift(SGC)
        edge = Circle(radius=G["rc"], stroke_color=CAMB, stroke_width=6).shift(SGC)
        with self.say("And now the word every student gets wrong. Bark is not just the cork. Bark is everything outside the vascular cambium: the secondary phloem, the periderm, and whatever is left of the cortex and epidermis."):
            cap("Bark = everything outside the vascular cambium", color=th.AMBER, sub="Secondary phloem + periderm + remains of cortex and epidermis.")
            self.play(FadeIn(bark), Create(edge), run_time=1.2)
        with self.say("Bark formed early in the season, containing living phloem, is soft bark. The dead, flaking outer bark of an old trunk is called rhytidome. If it peels off as a whole hollow cylinder, as in birch, it is ring bark. If it comes off in irregular flakes, as in guava, it is scale bark."):
            cap("Soft bark · rhytidome · ring bark · scale bark", sub="Ring bark: Betula (birch), peels as a cylinder. Scale bark: Psidium (guava), flakes.")
        self.play(FadeOut(bark), FadeOut(edge), FadeOut(stem), FadeOut(head))
        self.remove(stem)
        cap.clear()
        self.p6_lenticel()
        tip_ = "Bark is everything outside the vascular cambium, not just the cork. Periderm = phellogen + phellem + phelloderm."
        self.tip(tip_, "Exam tip. Two definitions examiners love. Periderm is phellogen plus phellem plus phelloderm. Bark is everything outside the vascular cambium. Write them in exactly those words, and never call the cork alone the bark.")

    def p6_lenticel(self):
        head = T("Lenticels: how a corked stem breathes", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        cork = VGroup()
        for row in range(4):
            for c in range(24):
                x = -5.75 + c * 0.5
                if abs(x) < 1.0:
                    continue
                cork.add(Rectangle(width=0.48, height=0.28, stroke_color="#7A5534", stroke_width=2, fill_color=CORK, fill_opacity=1).move_to([x, 0.2 + row * 0.3, 0]))
        phel = Line([-6, -0.15, 0], [6, -0.15, 0], color="#FFE2B8", stroke_width=5)
        inside = Rectangle(width=12, height=1.6, stroke_width=0, fill_color=PARF, fill_opacity=1).move_to([0, -1.0, 0])
        comp = VGroup(*[Circle(radius=0.17, stroke_color="#E8C9A0", stroke_width=2, fill_color="#8A6A48", fill_opacity=1).move_to([x, y, 0])
                        for x, y in [(-0.7, 0.2), (-0.25, 0.25), (0.25, 0.22), (0.7, 0.2), (-0.5, 0.6), (0.0, 0.62), (0.5, 0.6), (-0.3, 1.0), (0.25, 1.02), (0.0, 1.4), (-0.55, 1.05), (0.6, 1.05)]])
        epi = VGroup(Line([-6, 1.4, 0], [-1.1, 1.4, 0], color=EPI, stroke_width=6), Line([1.1, 1.4, 0], [6, 1.4, 0], color=EPI, stroke_width=6))
        l1 = T("cork (phellem)", size=24, color=CORK).move_to([-3.6, 1.95, 0])
        l2 = T("phellogen", size=22, color="#FFE2B8").move_to([4.6, -0.42, 0])
        l3 = T("complementary cells", size=24, color="#E8C9A0").move_to([3.2, 2.1, 0])
        ar = Arrow(l3.get_left() + LEFT * 0.05, [0.45, 1.25, 0], buff=0.05, color="#E8C9A0", stroke_width=3)
        with self.say("Unbroken cork would suffocate the living tissue inside. So at certain points the phellogen makes something else: loose, rounded, thin walled cells with big spaces between them, called complementary cells. They push up and burst through the surface as a raised, lens shaped pore."):
            self.play(FadeIn(head), FadeIn(inside), FadeIn(cork), Create(phel), FadeIn(l1), FadeIn(l2), Create(epi))
            self.play(LaggedStart(*[GrowFromCenter(c_) for c_ in comp], lag_ratio=0.12), run_time=2.2)
            self.play(FadeIn(l3), GrowArrow(ar))
        o2 = B.Flow([0.0, 2.7, 0], [0.0, -1.2, 0], n=6, color=th.SKY, speed=0.8, width=0.6, seed=3)
        co2 = B.Flow([0.25, -1.2, 0], [0.25, 2.7, 0], n=6, color=th.CORAL, speed=0.8, width=0.6, seed=4)
        gl = VGroup(T("O₂ in", size=24, color=th.SKY), T("CO₂ out", size=24, color=th.CORAL)).arrange(DOWN, buff=0.1).move_to([-3.4, -1.2, 0])
        nm = T("lenticel", size=34, color=th.AMBER, weight="BOLD").move_to([-3.4, -2.6, 0])
        with self.say("That pore is a lenticel, and it is how a woody stem exchanges gases: oxygen in, carbon dioxide out. Look at the trunk of a sisau or a mango and you can see them with the naked eye, as little raised lines."):
            self.add(o2, co2)
            self.play(FadeIn(gl), FadeIn(nm, scale=1.2))
            self.wait(1.0)
        self.play(FadeOut(VGroup(head, inside, cork, phel, comp, epi, l1, l2, l3, ar, gl, nm, o2, co2)))
        self.remove(o2, co2)
        bottle = VGroup(RoundedRectangle(corner_radius=0.25, width=1.2, height=2.6, stroke_color=th.SKY, stroke_width=4).move_to([0, -0.6, 0]),
                        Rectangle(width=0.5, height=0.6, stroke_width=0, fill_color=CORK, fill_opacity=1).move_to([0, 1.1, 0]))
        q = para("Bottle cork is the phellem of Quercus suber, the cork oak: light, compressible, waterproof and chemically inert.", width=6, size=26, color=th.INK).move_to([3.4, -0.3, 0])
        with self.say("Those same properties, light, springy, waterproof and inert, are why cork seals a bottle. Bottle cork is the phellem of the cork oak, Quercus suber."):
            self.play(FadeIn(bottle, shift=UP * 0.2), FadeIn(q))
            nb = B.neby_in(self, "cool", height=1.4, at=[-3.4, -0.4, 0])
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(bottle, q)))

    def p6_order(self):
        head, prob = B.example_head(self, "Arrange in the order they occur in a dicot stem, and name the meristem responsible: formation of lenticels; crushing of primary phloem; dedifferentiation of medullary ray cells; deposition of tyloses; formation of secondary xylem.", size=25)
        names = ["lenticels form", "primary phloem crushed", "ray cells dedifferentiate", "tyloses deposited", "secondary xylem forms"]
        cols = [CORK, PHL, "#FFD99A", PAR, XYL]
        cards = VGroup()
        for i, (n_, c_) in enumerate(zip(names, cols)):
            box = self.panel(2.3, 1.25, color=c_)
            tt = para(n_, width=2.0, size=22, color=th.INK, align="center")
            num = T(str(i + 1), size=20, color=th.MUTED).move_to(box.get_corner(UL) + [0.2, -0.18, 0])
            cards.add(VGroup(box, tt.move_to(box), num))
        cards.arrange(RIGHT, buff=0.22).move_to([0, -0.4, 0])
        with self.say("A worked example, straight from the exam. Five events, listed out of order. Put them in the order they happen, and name the meristem responsible for each."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.15))
        order = [2, 4, 1, 0, 3]
        slots = [cards[i].get_center() for i in range(5)]
        tags = ["creates the cambium", "vascular cambium", "vascular cambium", "cork cambium", "no meristem: old wood"]
        with self.say("Think it through. Nothing can happen until there is a cambial ring, so first the ray cells dedifferentiate. That event creates the meristem. Then the new cambium makes secondary xylem. As the wood builds up, the primary phloem is crushed. Only once the cortex is stretched does the cork cambium form and make lenticels. And tyloses come last of all, in old wood turning into heartwood.") as v:
            self.play(*[cards[j].animate.move_to(slots[i]) for i, j in enumerate(order)], run_time=2.0, path_arc=0.6)
            self.sfx("whoosh", gain=-12)
            arrows = VGroup(*[Arrow(slots[i] + RIGHT * 1.15, slots[i + 1] + LEFT * 1.15, buff=0.02, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5) for i in range(4)])
            self.play(FadeIn(arrows))
            per = (v.dur - 3.0) / 5
            tg = VGroup()
            for i, j in enumerate(order):
                t_ = para(tags[i], width=2.2, size=19, color=cols[j], align="center").next_to(cards[j], DOWN, buff=0.2)
                tg.add(t_)
                self.play(FadeIn(t_, shift=UP * 0.1), Indicate(cards[j][0], color=cols[j], scale_factor=1.05), run_time=0.5)
                self.hold(per - 0.5)
        ans = T("Answer: 3 → 5 → 2 → 1 → 4", size=34, color=th.AMBER, weight="BOLD").move_to([0, -2.75, 0])
        with self.say("In the numbers of the question, the answer is three, five, two, one, four."):
            self.play(Write(ans))
            nb = B.neby_in(self, "success", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(head, prob, cards, arrows, tg, ans)))

    def p6_monocot(self):
        ground = Line([-6.5, -2.7, 0], [1.0, -2.7, 0], color=th.FAINT, stroke_width=3)
        culm = VGroup()
        for i in range(7):
            culm.add(Rectangle(width=0.62, height=0.72, stroke_color="#A7D36B", stroke_width=3, fill_color="#5E8C2E", fill_opacity=1).move_to([-4.5, -2.34 + 0.75 * i, 0]))
        nodes = VGroup(*[Line([-4.86, -1.97 + 0.75 * i, 0], [-4.14, -1.97 + 0.75 * i, 0], color="#E4F5B8", stroke_width=5) for i in range(6)])
        sal = VGroup(Polygon([-2.6, -2.7, 0], [-1.2, -2.7, 0], [-1.65, 2.4, 0], [-2.15, 2.4, 0], stroke_width=0, fill_color="#7A5534", fill_opacity=1))
        l1 = T("bamboo", size=24, color="#A7D36B").move_to([-4.5, -3.1, 0])
        l2 = T("sal", size=24, color="#C9A27A").move_to([-1.9, -3.1, 0])
        mb = B.mono_bundle(3.6).move_to([3.8, 0.4, 0])
        ml = para("closed bundle: no cambium between xylem and phloem", width=4.8, size=24, color=th.INK, align="center").next_to(mb, DOWN, buff=0.3)
        with self.say("Now we can answer the question from the very start. Why does the sal trunk thicken while the bamboo never does? Look at a monocot bundle. It is closed. There is no cambium between its xylem and phloem."):
            self.play(Create(ground), FadeIn(culm), FadeIn(nodes), FadeIn(sal), FadeIn(l1), FadeIn(l2))
            self.play(FadeIn(mb, scale=0.8), FadeIn(ml))
        with self.say("And the bundles are scattered, not in a ring, so there is no line of ray cells where an interfascicular cambium could form. No vascular cambium means no secondary xylem, so no wood, and no annual rings."):
            self.play(Indicate(mb.parts["meta"], color=th.CORAL))
        with self.say("A bamboo or a palm gets its width another way, by primary thickening. A meristem just below the shoot tip builds each segment at its full width before it elongates. Then the segment is simply pushed up. That is why a bamboo shoot comes out of the ground as wide as it will ever be."):
            self.play(VGroup(culm, nodes).animate.stretch(1.12, 1, about_edge=DOWN), run_time=1.6)
            self.play(sal[0].animate.stretch(1.25, 0), run_time=1.4)
        note = para("Exceptions: Dracaena, Yucca and Agave have anomalous secondary growth from a cambium outside the bundles.", width=5.0, size=22, color=th.MUTED).move_to([3.8, -2.6, 0])
        with self.say("A few monocots, such as Dracaena, Yucca and Agave, do thicken, but abnormally: a cambium forms outside the bundles and makes whole new bundles, not ordinary wood."):
            self.play(FadeOut(ml), FadeIn(note))
        self.play(FadeOut(VGroup(ground, culm, nodes, sal, l1, l2, mb, note)))

    def p6_root(self):
        head = T("Secondary growth in a dicot root", size=32, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        C = np.array([-2.9, -0.35, 0])
        sc = 2.3
        core = VGroup(Circle(radius=1.05 * sc, stroke_color=PERI, stroke_width=3, fill_color="#1A1F38", fill_opacity=1).move_to(C))
        for k in range(4):
            a = TAU * k / 4
            for rr, sz in [(0.1, 0.1), (0.3, 0.09), (0.5, 0.07), (0.72, 0.05)]:
                core.add(Circle(radius=sz * sc, stroke_color=XYL, stroke_width=2.5, fill_color=XYL, fill_opacity=0.3).move_to(C + polar(rr * sc, a)))
            core.add(Circle(radius=0.12 * sc, stroke_width=0, fill_color=PHL, fill_opacity=0.85).move_to(C + polar(0.72 * sc, a + PI / 4)))

        def wavy(amp):
            pts = [C + polar(sc * (0.72 + amp * np.cos(4 * th_)), th_) for th_ in np.linspace(0, TAU, 240)]
            return VMobject(stroke_color=CAMB, stroke_width=6).set_points_smoothly(pts)

        arcs = VGroup(*[Arc(radius=0.52 * sc, start_angle=PI / 4 + TAU * k / 4 - 0.35, angle=0.7, stroke_color=CAMB, stroke_width=6).move_arc_center_to(C) for k in range(4)])
        cap = B.Captions(self, at=(3.6, 0.0, 0), width=5.4, size=26)
        with self.say("A dicot root thickens too, but its ring has to be assembled differently, because here xylem and phloem lie on alternate radii. This is a tetrarch root: four xylem arms, four phloem patches between them."):
            self.play(FadeIn(head), FadeIn(core))
            cap("A tetrarch dicot root", sub="Xylem arms (blue) and phloem patches (pink) on alternate radii.")
        with self.say("First, conjunctive parenchyma just inside each phloem patch becomes meristematic. Those are the first arcs of cambium."):
            cap("Arcs inside each phloem patch", color=CAMB, swatch=CAMB, sub="Conjunctive parenchyma dedifferentiates.")
            self.play(Create(arcs), run_time=1.4)
        w0 = wavy(0.22)
        with self.say("Then pericycle cells lying outside each protoxylem point join in. The arcs link up into a ring that is wavy: tucked in under the phloem, bulging out round the xylem tips."):
            cap("Pericycle joins: a wavy ring", color=CAMB, swatch=CAMB, sub="Inside the phloem, outside the protoxylem.")
            self.play(ReplacementTransform(arcs, w0), run_time=1.8)
        circ = wavy(0.0)
        with self.say("The parts under the phloem work faster and push outwards, so the ring soon becomes a circle. From then on it behaves exactly like the stem's cambium: secondary xylem inside, secondary phloem outside. Here the cork cambium arises from the pericycle, and the epiblema and cortex are shed."):
            cap("The ring becomes circular", sub="Then: wood inside, bast outside; cork cambium from the pericycle.")
            self.play(Transform(w0, circ), run_time=2.2)
        self.play(FadeOut(VGroup(head, core, w0)))
        cap.clear()
        self.quiz("Interfascicular cambium is formed by the dedifferentiation of",
                  ["pericycle cells", "medullary ray cells", "endodermal cells", "phloem parenchyma"], 1,
                  "Quick check. The interfascicular cambium of a dicot stem forms from which cells?",
                  "Medullary ray cells: the ray parenchyma lying in line with the fascicular strips. Pericycle is the tempting wrong answer: it does make cambium, but in the root, outside the protoxylem, not in the stem.")
        self.quiz("Cork is impermeable to water because its walls are impregnated with",
                  ["lignin", "cutin", "suberin", "pectin"], 2,
                  "One more. What makes cork waterproof?",
                  "Suberin. Lignin stiffens sclerenchyma and xylem, cutin forms the cuticle on the epidermis, and pectin is what makes collenchyma flexible.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Tissue: cells of common origin doing one job. Meristematic or permanent; simple or complex.",
            "Collenchyma alive and flexible; sclerenchyma dead and lignified. Xylem up; phloem both ways.",
            "Root: radial bundles, exarch xylem, endodermis with Casparian strips.",
            "Stem: conjoint collateral, endarch. Dicot one ring, open; monocot scattered, closed.",
            "Leaf: dicot dorsiventral (palisade + spongy); monocot isobilateral (bulliform cells).",
            "Cambial ring → wood inside, bast outside; annual rings; cork cambium → periderm; bark.",
        ], "Quick recap. Tissues: meristematic or permanent, simple or complex. Collenchyma is alive and flexible, sclerenchyma dead and lignified; xylem carries water up, phloem carries food both ways. Roots have radial bundles and exarch xylem. Stems have conjoint, collateral, endarch bundles, in one open ring in a dicot, scattered and closed in a monocot. Dicot leaves are dorsiventral, monocot leaves isobilateral. And in secondary growth, the cambial ring makes wood inside and bast outside, laying down annual rings, while the cork cambium makes the periderm, and everything outside the cambium is bark.")
        self.outro("That was plant anatomy. Draw each section once from memory, then check it against the video. Next, we take this plumbing and make it work: plant physiology, how water climbs a tree and how a leaf turns light into sugar. See you there.")
