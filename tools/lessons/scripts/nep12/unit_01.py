import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, T, para, th  # noqa: E402
import _common as C  # noqa: E402

GOLD, SKY, MINT, CORAL, PINK, LEAFC = th.AMBER, th.SKY, th.MINT, th.CORAL, th.PINK, C.LEAF


class Lesson(Lesson):
    SUBJECT = "nep"
    GRADE = 12
    UNIT = 1
    LANG = "ne"
    TITLE = "आमाको सपना"
    SUBTITLE = "गोपालप्रसाद रिमाल  ·  गद्य कविता"
    SECTIONS = ["कवि परिचय", "पाठको पृष्ठभूमि", "कवितासार", "खण्डगत व्याख्या", "प्रतीक र पात्र",
                "मूल भाव र समीक्षा", "गद्य कविता र भाषाशैली", "उत्तर लेख्ने ढाँचा"]
    NEXT = "एकाइ २  ·  विरहिणी दमयन्ती"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ helpers
    def ground(self, color="#151935"):
        return Rectangle(width=15, height=1.0, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0, -3.75, 0])

    def sym_icon(self, kind):
        if kind == "sun":
            return C.sun(0.35)
        if kind == "sword":
            blade = Polygon([-0.07, -0.2, 0], [0.07, -0.2, 0], [0.04, 0.75, 0], [0, 0.9, 0], [-0.04, 0.75, 0],
                            stroke_width=0, fill_color="#DDE6F5", fill_opacity=1)
            guard = Rectangle(width=0.45, height=0.08, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([0, -0.22, 0])
            hilt = Rectangle(width=0.08, height=0.3, stroke_width=0, fill_color="#8A6A4A", fill_opacity=1).move_to([0, -0.4, 0])
            dew = VGroup(*[Dot([x, y, 0], radius=0.04, color="#BFE3FF") for x, y in ((0.25, 0.5), (-0.22, 0.3), (0.2, 0.05))])
            return VGroup(blade, guard, hilt, dew).rotate(-0.5)
        if kind == "flute":
            return C.flute(1.6)
        if kind == "wind":
            return VGroup(*[ArcBetweenPoints([-0.7, y, 0], [0.7, y + 0.1, 0], angle=-0.5).set_stroke("#9FB4E8", 4) for y in (-0.25, 0.05, 0.35)])
        if kind == "leaf":
            return C.leaf(0.4).rotate(0.5)
        if kind == "moon":
            return C.moon(0.35)
        if kind == "jadata":
            rock = Polygon([-0.6, -0.3, 0], [-0.4, 0.2, 0], [0.1, 0.35, 0], [0.55, 0.1, 0], [0.6, -0.3, 0],
                           stroke_width=0, fill_color="#5A6080", fill_opacity=1)
            ch = VGroup(*[Circle(radius=0.09, stroke_color=th.MUTED, stroke_width=3).move_to([x, -0.42, 0]) for x in (-0.3, -0.1, 0.1, 0.3)])
            return VGroup(rock, ch)
        return Dot()

    def sym_card(self, kind, name, meaning, color, w=3.15, h=2.75):
        b = C.box(w, h, color=color)
        ic = self.sym_icon(kind)
        if ic.height > 0.9:
            ic.scale_to_fit_height(0.9)
        if ic.width > w - 0.6:
            ic.scale_to_fit_width(w - 0.6)
        nm = T(name, size=28, color=color, weight="BOLD")
        if nm.width > w - 0.3:
            nm.scale_to_fit_width(w - 0.3)
        mn = para(meaning, width=w - 0.4, size=23, color=th.BODY, align="center")
        g = VGroup(ic, nm, mn).arrange(DOWN, buff=0.14).move_to(b)
        return VGroup(b, g)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        sk = C.sky("#0A0E22", "#1D1A3C")
        st = C.stars(70, seed=11)
        sn = C.sun(0.75).move_to([3.6, -2.6, 0])
        hills = C.himalaya(seed=4)
        gr = self.ground()
        hut = C.hut(2.0).move_to([-4.7, -2.75, 0])
        ma = C.mother(2.5).move_to([-1.7, -3.25, 0], aligned_edge=DOWN)
        ch = C.child(1.45).move_to([-0.55, -3.25, 0], aligned_edge=DOWN)
        self.add(sk, st, sn, hills, gr)
        with self.say("साँझ ढलिसकेको छ। हिमालको काखमा एउटा सानो घर छ, र त्यसको झ्यालमा टुकीको मधुरो उज्यालो बलिरहेको छ।"):
            self.play(FadeIn(sk), FadeIn(st, lag_ratio=0.05), FadeIn(hills, shift=UP * 0.3), FadeIn(gr), run_time=2.0)
            self.play(FadeIn(hut, shift=UP * 0.2), run_time=0.8)
        b1 = C.bubble("आमा, त्यो आउँछ र ?", size=30, tail=DOWN + LEFT).move_to([1.4, 0.4, 0])
        with self.say("त्यही घरको आँगनमा एउटा सानो छोरो आमालाई सोध्छ, आमा, त्यो आउँछ र?"):
            self.play(FadeIn(ma, shift=UP * 0.2), FadeIn(ch, shift=UP * 0.2), run_time=0.8)
            self.sfx("pop", gain=-12)
            self.play(FadeIn(b1, scale=0.8), run_time=0.5)
        b2 = C.bubble("हो, बा, त्यो आउँछ।", size=30, tail=DOWN + RIGHT, fill="#3A2240").move_to([-3.1, 0.9, 0])
        with self.say("आमा एक क्षण पनि नहिचकिचाई, पूरा विश्वासका साथ भन्छिन्, हो, बा, त्यो आउँछ।"):
            self.sfx("pop", gain=-12)
            self.play(FadeIn(b2, scale=0.8), run_time=0.5)
            self.play(Circumscribe(b2[1], color=GOLD), run_time=1.0)
        big = T("त्यो", size=120, color=GOLD, weight="BOLD").move_to([3.6, 1.6, 0])
        qm = T("?", size=120, color=CORAL, weight="BOLD").next_to(big, RIGHT, buff=0.2)
        with self.say("तर पख्नुहोस्। त्यो भनेको को? कुनै पाहुना हो? बिहानको घाम हो? कि अरू नै केही? कविताभरि यसको नाम कतै लेखिएको छैन। छ त केवल एउटा शब्द, त्यो।"):
            self.play(FadeOut(b1), FadeOut(b2), run_time=0.4)
            self.sfx("impact", gain=-10)
            self.play(FadeIn(big, scale=1.5), run_time=0.7)
            self.play(FadeIn(qm, shift=LEFT * 0.3), run_time=0.4)
            self.play(Wiggle(qm), run_time=1.0)
        with self.say("कवि भन्छन्, त्यो बिहानको सूर्य झैँ उज्यालो छर्दै आउँछ। आज हामी यही रहस्य खोल्दैछौँ। पाठको अन्त्यसम्म पुग्दा त्यो को हो, र आमाको सपना के हो, तपाईँ आफैँ प्रस्ट भन्न सक्नुहुनेछ।"):
            self.play(FadeOut(VGroup(big, qm)), run_time=0.4)
            self.sfx("riser", gain=-14)
            self.play(sn.animate.move_to([3.6, 1.7, 0]), sk.animate.set_color("#3A3A78"), st.animate.set_opacity(0.15),
                      run_time=4.0, rate_func=rate_functions.ease_out_sine)
            self.play(Indicate(sn, color=WHITE, scale_factor=1.08), run_time=1.0)
        self.play(FadeOut(VGroup(sk, st, sn, hills, gr, hut, ma, ch)), run_time=0.8)
        g, nb = self.title_card()
        with self.say("नमस्ते! कक्षा बाह्रको अनिवार्य नेपालीमा स्वागत छ। आजको पाठ हो, एकाइ एक, आमाको सपना। यो गोपालप्रसाद रिमालको प्रसिद्ध गद्य कविता हो, जसमा आमा र छोराको सानो संवादभित्र एउटा सिङ्गो देशको सपना लुकेको छ।"):
            pass
        self.end_title(g, nb)
        self.roadmap("हाम्रो बाटो यस्तो छ। पहिले कविलाई चिनौँ, अनि कविताको पृष्ठभूमि बुझौँ। त्यसपछि कवितासार, खण्डगत व्याख्या, प्रतीक र पात्र, मूल भाव र समीक्षा, गद्य कविताको शैली, र अन्त्यमा परीक्षामा उत्तर लेख्ने ढाँचा।")

    # ------------------------------------------------------------------ part 1: poet
    def p1(self):
        self.section(0)
        name = C.kline("गोपालप्रसाद रिमाल", size=64, color=th.INK).move_to(UP * 1.4)
        under = Line(LEFT * 3.2, RIGHT * 3.2, color=self.color, stroke_width=5).next_to(name, DOWN, buff=0.25)
        pills = VGroup(C.pill("गद्य कविताका आरम्भकर्ता", GOLD, 28), C.pill("नाटककार", SKY, 28),
                       C.pill("प्रगतिवादी स्रष्टा", MINT, 28)).arrange(RIGHT, buff=0.35).next_to(under, DOWN, buff=0.6)
        with self.say("गोपालप्रसाद रिमाललाई नेपाली साहित्यमा गद्य कविताका आरम्भकर्ता भनेर चिनिन्छ। उनी कवि मात्र होइनन्, नाटककार र प्रगतिवादी स्रष्टा पनि हुन्।"):
            C.type_in(self, VGroup(name), run_time=1.2)
            self.play(Create(under), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pills], lag_ratio=0.3), run_time=1.5)
        self.play(FadeOut(VGroup(name, under, pills)), run_time=0.5)
        head = C.heading("जीवनरेखा", color=self.color)
        self.play(FadeIn(head), run_time=0.4)
        tl = C.timeline(self, [
            (1975, "जन्म · लगनटोल, काठमाडौँ", "उनको जन्म विक्रम संवत् उन्नाइस सय पचहत्तर, जेठ अठार गते काठमाडौँको लगनटोलमा भयो। उनका पिताको नाम उमाकान्त रिमाल हो।"),
            (1992, "पहिलो कविता 'प्रति' · शारदा पत्रिका", "उन्नाइस सय बयानब्बे सालमा शारदा पत्रिकामा छापिएको प्रति शीर्षकको कवितालाई उनको पहिलो प्रकाशित रचना मानिन्छ।"),
            (2002, "'यो प्रेम' नाटक लेखन", "दुई हजार दुई सालमा उनले यो प्रेम नाटक लेखे, जुन पछि दुई हजार पन्ध्र सालमा प्रकाशित भयो।"),
            (2019, "'आमाको सपना' सङ्ग्रह · मदन पुरस्कार", "दुई हजार उन्नाइस सालमा आमाको सपना कविता सङ्ग्रहले उनलाई मदन पुरस्कार दिलायो। हाम्रो पाठ यही सङ्ग्रहको शीर्षक कविता हो।"),
            (2030, "त्रिभुवन पुरस्कार · निधन", "दुई हजार तीस सालमा उनलाई त्रिभुवन पुरस्कार प्रदान गरियो, र सोही वर्ष कात्तिक आठ गते काठमाडौँमा उनको निधन भयो।"),
        ], y=-0.2, label_w=2.7, size=24)
        self.wait(0.5)
        self.play(FadeOut(VGroup(head, tl)), run_time=0.5)
        head = C.heading("प्रमुख कृति", color=self.color)
        cards = VGroup(
            C.card("आमाको सपना", "कविता सङ्ग्रह · मदन पुरस्कार", GOLD, w=3.15, h=2.7, hsize=34, bsize=26),
            C.card("मसान", "नाटक", SKY, w=3.15, h=2.7, hsize=34, bsize=26),
            C.card("यो प्रेम", "नाटक", PINK, w=3.15, h=2.7, hsize=34, bsize=26),
            C.card("रातो र चन्द्र सूर्य", "चर्चित राष्ट्रिय गीत", MINT, w=3.15, h=2.7, hsize=34, bsize=26),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.2)
        with self.say("उनका प्रमुख कृति हेरौँ। आमाको सपना, कविता सङ्ग्रह। मसान र यो प्रेम, दुई चर्चित नाटक। र रातो र चन्द्र सूर्य, जङ्गी निसान हाम्रो, उनले लेखेको चर्चित राष्ट्रिय गीत।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.3, scale=0.9), run_time=0.5)
                self.hold(v.dur / 4 - 0.9)
        with self.say("रिमालले थोरै लेखे, तर धेरै ख्याति कमाए। किन? किनभने उनले नेपाली कवितामा एउटा नयाँ बाटो खोलिदिए।"):
            self.play(Indicate(cards[0], color=GOLD, scale_factor=1.05), run_time=1.2)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        self.cage_break()
        with self.say("उनी सामाजिक कार्यकर्ता पनि थिए। समाज सुधार र राजनीतिक परिवर्तनका लागि सक्रिय उनको जीवन, र कवितामा देखिने विद्रोही स्वर, एकअर्कासँग मिल्छन्।"):
            ma = C.mother(2.4).move_to([-3.5, -2.6, 0], aligned_edge=DOWN)
            crowd = VGroup(*[C.person(1.3, color=c) for c in ("#6C7AA8", "#7F8DB8", "#5E6B98", "#8A97C2", "#6C7AA8")]).arrange(RIGHT, buff=0.25)
            crowd.move_to([2.4, -2.6, 0], aligned_edge=DOWN)
            fl = C.torch(1.2).move_to([0.0, -1.6, 0])
            self.play(FadeIn(crowd, lag_ratio=0.2), FadeIn(fl, shift=UP * 0.3), run_time=1.5)
            self.play(crowd.animate.set_color(GOLD).set_opacity(0.9), Indicate(fl), run_time=1.5)
        self.play(FadeOut(VGroup(crowd, fl)), run_time=0.4)
        self.tip(f"जन्म वि.सं. {self.num(1975)}, निधन {self.num(2030)}; 'आमाको सपना' सङ्ग्रहलाई मदन पुरस्कार {self.num(2019)} मा। वर्षमा शङ्का भए 'मदन पुरस्कार प्राप्त' मात्र लेख्नुहोस्।",
                 "एउटा परीक्षा सुझाव। रिमालको जन्म उन्नाइस सय पचहत्तर, निधन दुई हजार तीस, र मदन पुरस्कार दुई हजार उन्नाइसमा। केही स्रोतले वर्ष फरक लेखेका छन्। शङ्का लागे वर्ष नलेखी, मदन पुरस्कार प्राप्त, मात्र लेख्नु सुरक्षित हुन्छ।")

    def cage_break(self):
        word = T("कविता", size=72, color=th.INK, weight="BOLD").move_to(UP * 0.2)
        bars = VGroup(*[Line(UP * 1.3, DOWN * 1.3, color=th.MUTED, stroke_width=7).shift(RIGHT * x + UP * 0.2) for x in np.linspace(-2.2, 2.2, 8)])
        frame = VGroup(Line([-2.3, 1.5, 0], [2.3, 1.5, 0], color=th.MUTED, stroke_width=8),
                       Line([-2.3, -1.1, 0], [2.3, -1.1, 0], color=th.MUTED, stroke_width=8))
        tags = VGroup(C.pill("छन्द", CORAL, 26), C.pill("तुक", CORAL, 26), C.pill("अक्षरगणना", CORAL, 26))
        tags[0].move_to([-4.3, 1.0, 0])
        tags[1].move_to([4.0, 1.0, 0])
        tags[2].move_to([0, -1.9, 0])
        with self.say("उनीभन्दा पहिले कविता प्रायः शास्त्रीय छन्दको खोरभित्र बाँधिन्थ्यो। अक्षर गन्नुपर्ने, तुक मिलाउनुपर्ने, निश्चित लयमा हिँड्नुपर्ने।"):
            self.play(FadeIn(word), run_time=0.5)
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.1), Create(frame), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in tags], lag_ratio=0.4), run_time=1.5)
        new = T("गद्य कविता", size=72, color=GOLD, weight="BOLD").move_to(UP * 0.4)
        free = C.pill("मुक्त लय", MINT, 30).next_to(new, DOWN, buff=0.5)
        rng = np.random.default_rng(2)
        with self.say("रिमालले त्यो खोर तोडिदिए। छन्द र तुकको बन्धन नमानी, उनले भाव र चेतनालाई बोलीचालीको जस्तै सहज लयमा बगाए। यसैलाई गद्य कविता भनिन्छ।"):
            self.sfx("impact", gain=-10)
            self.play(*[b.animate.shift(np.array([rng.uniform(-5, 5), rng.choice([-4, 4]), 0])).rotate(rng.uniform(-2, 2)).set_opacity(0) for b in bars],
                      *[f.animate.shift(UP * 3 * (1 if i == 0 else -1)).set_opacity(0) for i, f in enumerate(frame)],
                      *[t.animate.shift((t.get_center() - ORIGIN) * 0.6).set_opacity(0) for t in tags], run_time=1.2)
            self.play(Transform(word, new), run_time=0.9)
            self.play(FadeIn(free, shift=UP * 0.2), run_time=0.5)
        self.remove(bars, frame, tags)
        self.play(FadeOut(VGroup(word, free)), run_time=0.4)

    # ------------------------------------------------------------------ part 2: background
    def p2(self):
        self.section(1)
        sk = C.sky("#0C0F22", "#191B33")
        hills = C.himalaya(seed=7, far="#1E2448", mid="#191E3C", near="#141831")
        crowd = VGroup(*[C.person(1.5, color="#4A5070") for _ in range(7)]).arrange(RIGHT, buff=0.45).move_to([0, -3.2, 0], aligned_edge=DOWN)
        for p in crowd:
            p[1].shift(DOWN * 0.07 + RIGHT * 0.1)
        with self.say("अब कविता जन्मिएको समयतिर फर्कौँ। त्यो बेला नेपालमा निरङ्कुश शासनको छायाँ थियो।"):
            self.play(FadeIn(sk), FadeIn(hills), run_time=1.0)
            self.bring_to_front(self.hud)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in crowd], lag_ratio=0.1), run_time=1.2)
        clouds = VGroup()
        for i, (w, x, y) in enumerate([("गरिबी", -4.4, 1.6), ("अशिक्षा", -1.5, 2.2), ("डर", 1.5, 1.5), ("जडता", 4.3, 2.1)]):
            puff = VGroup(*[Ellipse(width=1.4 + 0.3 * k, height=0.7, stroke_width=0, fill_color="#3A3F5E", fill_opacity=0.85).shift(RIGHT * (k - 1) * 0.55 + UP * (0.12 if k == 1 else 0))
                            for k in range(3)])
            lab = T(w, size=30, color=th.BODY, weight="SEMIBOLD").move_to(puff)
            clouds.add(VGroup(puff, lab).move_to([x, y, 0]))
        with self.say("जनजीवनमा गरिबी थियो, अशिक्षा थियो, डर थियो, र सबैभन्दा गहिरो कुरा, जडता थियो। मानिसहरू आफ्नो पीडा सुनाउन पनि डराउँथे।") as v:
            for c in clouds:
                self.play(FadeIn(c, shift=RIGHT * 0.5), run_time=0.6)
                self.hold(v.dur / 4 - 0.8)
            self.play(*[c.animate.shift(RIGHT * 0.3) for c in clouds], run_time=1.0)
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GOLD, fill_opacity=0.06).move_to([0, -3.4, 0]) for r in (1.5, 2.5, 3.5, 4.5)])
        with self.say("तर त्यही अँध्यारोभित्र पनि परिवर्तनको चाहना बिस्तारै बढ्दै थियो। कविले त्यही उठ्न खोजिरहेको आकाङ्क्षालाई आमा र छोराको सरल संवादमा राखेका छन्।"):
            self.play(FadeIn(glow, scale=0.5), *[c.animate.set_opacity(0.25) for c in clouds], run_time=1.8)
            self.play(*[p[1].animate.shift(UP * 0.07 + LEFT * 0.1) for p in crowd], crowd.animate.set_color("#C9A46A"), run_time=1.5)
        self.play(FadeOut(VGroup(sk, hills, crowd, clouds, glow)), run_time=0.6)
        w = C.kline("कवितामा 'क्रान्ति' शब्द सोझै आएको छैन", size=40, color=th.INK, hl={"क्रान्ति": CORAL}).move_to(UP * 2.0)
        with self.say("ध्यान दिनुहोस्, कवितामा क्रान्ति शब्द सोझै आएको छैन। तैपनि पाठ्यपुस्तकले क्रान्तिको आवश्यकता र स्वरूप सोधेको छ, अर्थात् यसलाई क्रान्तिको आह्वानका रूपमा पढ्न खोजेको छ।"):
            C.type_in(self, VGroup(w), run_time=1.5)
        gun = C.pill("बन्दुक र रगतको मात्र होइन", th.MUTED, 28).move_to(UP * 0.8)
        cross = Line(gun.get_left(), gun.get_right(), color=CORAL, stroke_width=5)
        three = VGroup(C.pill("अधर्मसित लड्ने", GOLD, 28), C.pill("जडता सगबगाउने", SKY, 28),
                       C.pill("सत्य आफैँ देख्ने, सहने र ग्रहण गर्ने", MINT, 28)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.3)
        lab = T("चेतनाको क्रान्ति", size=34, color=GOLD, weight="BOLD").next_to(three, LEFT, buff=0.6)
        with self.say("तर यो क्रान्ति बन्दुक र रगतको मात्र होइन। यो चेतनाको क्रान्ति हो। अधर्मसित लड्ने, जडता सगबगाउने, र सत्यलाई आफैँ देख्न, सहन र ग्रहण गर्न सक्ने चेतना।"):
            self.play(FadeIn(gun), run_time=0.5)
            self.play(Create(cross), run_time=0.5)
            self.play(FadeIn(lab, shift=RIGHT * 0.2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in three], lag_ratio=0.5), run_time=2.5)
        self.play(FadeOut(VGroup(w, gun, cross, three, lab)), run_time=0.5)
        self.triangle()

    def triangle(self):
        top = C.node("त्यो", GOLD, size=34, sub="क्रान्ति र परिवर्तन", w=3.6).move_to([0, 1.7, 0])
        lft = C.node("आमा", PINK, size=34, sub="मातृभूमि र जनचेतना", w=3.6).move_to([-4.0, -1.8, 0])
        rgt = C.node("छोरा", SKY, size=34, sub="आजको पुस्ता", w=3.6).move_to([4.0, -1.8, 0])
        l1 = C.link(lft, top, color=PINK, label="सपना र आशा", size=22)
        l2 = C.link(top, rgt, color=GOLD, label="पात भएर पछ्याउने", size=22)
        l3 = C.link(lft, rgt, color=th.MUTED, label="प्रश्न र आश्वासन", size=22, both=True)
        with self.say("कविताको संरचनालाई एउटा त्रिकोणमा हेरौँ। एकातिर आमा छिन्, जसले सपना र आशा बोकेकी छन्। अर्कोतिर छोरा छ, जसले प्रश्न सोध्छ, र आमा आश्वासन दिन्छिन्।"):
            self.play(FadeIn(lft, scale=0.8), run_time=0.5)
            self.play(FadeIn(rgt, scale=0.8), run_time=0.5)
            self.play(Create(l3[0]), FadeIn(l3[1:]), run_time=0.8)
        with self.say("र माथि छ, त्यो, अर्थात् क्रान्ति र परिवर्तन। आमाको आशा त्यसतर्फ फर्केको छ, र त्यो आएपछि छोराले पात भएर त्यसलाई पछ्याउनुपर्छ।"):
            self.sfx("shimmer", gain=-14)
            self.play(FadeIn(top, scale=0.8), run_time=0.6)
            self.play(GrowArrow(l1[0]), FadeIn(l1[1:]), run_time=0.8)
            self.play(GrowArrow(l2[0]), FadeIn(l2[1:]), run_time=0.8)
            self.play(Indicate(top, color=GOLD), run_time=1.0)
        self.play(FadeOut(VGroup(top, lft, rgt, l1, l2, l3)), run_time=0.5)

    # ------------------------------------------------------------------ part 3: summary
    def p3(self):
        self.section(2)
        pts = [[-6.2, -2.9, 0], [-3.5, -1.6, 0], [-0.5, -2.5, 0], [2.5, -1.2, 0], [6.2, -1.9, 0]]
        road = VMobject(stroke_color="#6B5A4A", stroke_width=26)
        road.set_points_smoothly(pts)
        dash = DashedVMobject(road.copy().set_stroke(GOLD, 3), num_dashes=40)
        stations = []
        heads = [("आदि", GOLD), ("मध्य", SKY), ("अन्त्य", MINT)]
        bodies = ["छोराको प्रश्न र आमाको आश्वासन: 'त्यो' आउँछ।",
                  "आमाको सपना, छोराबाट अपेक्षा र 'त्यो' आएपछिको परिवर्तन।",
                  "फेरि आशाको पुष्टि र सपनाको जिम्मा छोरालाई।"]
        cards = VGroup()
        for i, ((h, col), b) in enumerate(zip(heads, bodies)):
            p = road.point_from_proportion([0.14, 0.5, 0.86][i])
            dot = VGroup(Circle(radius=0.28, fill_color=col, fill_opacity=1, stroke_color=WHITE, stroke_width=3), ).move_to(p)
            stations.append(dot)
            cards.add(C.card(h, b, col, w=3.9, h=2.2, hsize=32, bsize=23).move_to([[-4.3, 0, 4.3][i], 1.25, 0]))
        lines = VGroup(*[DashedLine(stations[i].get_top(), cards[i].get_bottom(), color=heads[i][1], stroke_width=2) for i in range(3)])
        walker = Dot(road.get_start(), radius=0.14, color=WHITE)
        with self.say("कविता छोरा र आमाका बिचको प्रश्नोत्तरमा अघि बढ्छ। यसलाई आदि, मध्य र अन्त्य गरी तीन चरणमा बुझ्दा सजिलो हुन्छ।"):
            self.play(Create(road), Create(dash), run_time=1.5)
            self.play(LaggedStart(*[GrowFromCenter(s_) for s_ in stations], lag_ratio=0.3), FadeIn(walker), run_time=1.2)
        narrs = [
            "आदिमा छोरा सोध्छ, आमा, त्यो आउँछ र? आमा विश्वासका साथ भन्छिन्, हो, बा, त्यो आउँछ। त्यो बिहानको सूर्य झैँ उज्यालो छर्दै, कम्मरमा शीत जस्तै टल्कने हतियार झुन्ड्याएर, अधर्मसित लड्न आउँछ।",
            "मध्य भागमा आमा आफ्नो सपना सुनाउँछिन्। छोरा जन्मँदा उसको कलिलो अनुहार, हिस्सी परेको हाँसो र तोते बोलीमा उनले त्यही आउने कुराको छाया देखेकी थिइन्। त्यो आएपछि छोरा सत्यलाई कथा सुने झैँ सुन्ने छैन, आफैँ देख्ने, सहने र ग्रहण गर्ने हुनेछ। त्यो हुरी भएर आउनेछ, र छोरा पात भएर पछ्याउनेछ।",
            "अन्त्यमा छोराले फेरि सोध्छ, किनकि त्यो आउने आशाले उसको हृदयलाई कुत्कुत्याइसकेको छ। आमा फेरि पुष्टि गर्छिन्, हो, त्यो आउँछ। अनि भन्छिन्, अब म उठेँ, गएँ, तर त्यो तिमी नै हौला भन्ने मेरो यौवनभरिको सपना थियो।",
        ]
        props = [0.14, 0.5, 0.86]
        prev = 0.0
        for i in range(3):
            with self.say(narrs[i]):
                a0, a1 = prev, props[i]
                self.play(UpdateFromAlphaFunc(walker, lambda m, a, a0=a0, a1=a1: m.move_to(road.point_from_proportion(a0 + (a1 - a0) * a))), run_time=1.2)
                self.sfx("pop", gain=-12)
                self.play(Create(lines[i]), FadeIn(cards[i], shift=UP * 0.3), Flash(stations[i], color=heads[i][1]), run_time=0.8)
            prev = props[i]
        with self.say("यसरी कविताको अन्त्य निराशामा होइन, जिम्मेवारीको हस्तान्तरणमा हुन्छ। आमाको सपना अब छोराको काँधमा आइपुग्छ।"):
            self.play(UpdateFromAlphaFunc(walker, lambda m, a: m.move_to(road.point_from_proportion(0.86 + 0.14 * a))), run_time=1.2)
            self.play(Circumscribe(cards[2], color=MINT), run_time=1.2)
        self.play(FadeOut(VGroup(road, dash, *stations, cards, lines, walker)), run_time=0.6)

    # ------------------------------------------------------------------ part 4: section by section
    def p4(self):
        self.section(3)
        names = ["आगमनको आश्वासन", "आमाको सपना", "सिर्जनाशक्तिकी आमा", "भूमिकाको परिवर्तन", "हुरी र पात", "सपनाको उत्तराधिकार"]
        cols = [GOLD, PINK, CORAL, SKY, LEAFC, MINT]
        chips = VGroup()
        for i, (n, c) in enumerate(zip(names, cols)):
            chips.add(VGroup(C.badge(self, i + 1, c, r=0.3), T(n, size=28, color=th.INK)).arrange(RIGHT, buff=0.3))
        chips.arrange_in_grid(rows=3, cols=2, buff=(1.2, 0.55), flow_order="dr", col_alignments="ll").move_to(DOWN * 0.1)
        head = C.heading("छ खण्डमा कविता", color=self.color)
        with self.say("यो कविता श्लोकमा बाँधिएको छैन। त्यसैले भावका आधारमा यसलाई छ खण्डमा बाँडेर पढ्दा सजिलो हुन्छ। एक एक गरी हेरौँ।"):
            self.play(FadeIn(head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in chips], lag_ratio=0.2), run_time=2.4)
        self.play(FadeOut(VGroup(head, chips)), run_time=0.5)
        self.k1()
        self.k2()
        self.k3()
        self.k4()
        self.k5()
        self.k6()

    def ktag(self, i, name, color):
        t = VGroup(C.badge(self, i, color, r=0.24), T(name, size=24, color=color, weight="SEMIBOLD")).arrange(RIGHT, buff=0.2)
        return t.to_corner(UR, buff=0.45).shift(DOWN * 0.05)

    def k1(self):
        tag = self.ktag(1, "आगमनको आश्वासन", GOLD)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["हो, बा, त्यो आउँछ"], "पहिलो खण्ड। छोराको प्रश्नमा शङ्का होइन, आतुरता छ। र आमाको उत्तरमा कुनै हिचकिचाहट छैन। हो, बा, त्यो आउँछ।",
                         color=GOLD, size=52, where=UP * 1.9, keep=True, hl={"त्यो": GOLD})
        sn = C.sun(0.55).move_to([-4.6, -0.9, 0])
        sword = self.sym_icon("sword").scale(1.3).move_to([-0.2, -1.0, 0])
        shield = Star(n=8, outer_radius=0.6, inner_radius=0.3, stroke_width=0, fill_color=MINT, fill_opacity=1).move_to([4.0, -0.9, 0])
        trio = VGroup(
            VGroup(sn, T("उज्यालो", size=30, color=GOLD, weight="BOLD"), T("बिहानको सूर्य झैँ", size=22, color=th.BODY)),
            VGroup(sword, T("शक्ति", size=30, color=SKY, weight="BOLD"), T("शीत जस्तै टल्कने हतियार", size=22, color=th.BODY)),
            VGroup(shield, T("नैतिक उद्देश्य", size=30, color=MINT, weight="BOLD"), T("अधर्मसित लड्ने", size=22, color=th.BODY)),
        )
        for i, g in enumerate(trio):
            g[1].move_to([[-4.3, 0, 4.3][i], -2.2, 0])
            g[2].next_to(g[1], DOWN, buff=0.12)
            g[0].move_to([[-4.3, 0, 4.3][i], -0.8, 0])
        with self.say("आमाले त्यो लाई तीन रूपमा चिनाउँछिन्। बिहानको सूर्य झैँ उज्यालो, अर्थात् आशा। कम्मरमा शीत जस्तै टल्कने हतियार, अर्थात् शक्ति। र अधर्मसित लड्ने, अर्थात् नैतिक उद्देश्य।") as v:
            for g in trio:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(g[0], scale=0.6), FadeIn(g[1], shift=UP * 0.2), FadeIn(g[2]), run_time=0.7)
                self.hold(v.dur / 3 - 0.9)
        dew = VGroup(*[Star(n=4, outer_radius=0.12, inner_radius=0.04, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(sword.get_center() + np.array(o))
                       for o in ((0.4, 0.5, 0), (-0.3, 0.1, 0), (0.15, -0.3, 0))])
        with self.say("यहाँ हतियार रगत बगाउने वस्तु होइन। शीत झैँ चम्किलो र शुद्ध छ। अर्थात् यो क्रान्ति अधर्मविरुद्धको शुद्ध शक्ति हो।"):
            self.play(trio[0].animate.set_opacity(0.3), trio[2].animate.set_opacity(0.3), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in dew], lag_ratio=0.3), run_time=1.0)
            self.play(LaggedStart(*[Flash(d, color=WHITE, flash_radius=0.25, line_length=0.12) for d in dew], lag_ratio=0.3), run_time=1.2)
        self.play(FadeOut(VGroup(q, trio, dew)), run_time=0.5)
        q = C.show_quote(self, ["हिउँ र आगोभन्दा पनि बढ्ता छोइने भएर आउँछ"], "अर्को पङ्क्ति ध्यान दिएर हेर्नुहोस्। हिउँ र आगोभन्दा पनि बढ्ता छोइने भएर आउँछ।",
                         color=GOLD, size=40, where=UP * 1.9, keep=True, hl={"हिउँ": SKY, "आगोभन्दा": CORAL})
        sf = C.snowflake(0.7).move_to([-4.5, -1.0, 0])
        fl = C.flame(1.4).move_to([4.5, -1.0, 0])
        hrt = C.heart(0.6, color=PINK).move_to([0, -1.0, 0])
        a1 = Arrow(sf.get_right(), hrt.get_left(), buff=0.3, color=SKY, stroke_width=5)
        a2 = Arrow(fl.get_left(), hrt.get_right(), buff=0.3, color=CORAL, stroke_width=5)
        l1 = T("चिसोले छुन्छ", size=24, color=SKY).next_to(sf, DOWN, buff=0.3)
        l2 = T("तापले छुन्छ", size=24, color=CORAL).next_to(fl, DOWN, buff=0.3)
        l3 = T("त्यो: यी दुवैभन्दा गहिरो", size=26, color=GOLD, weight="BOLD").next_to(hrt, DOWN, buff=0.45)
        with self.say("हिउँले चिसोले छुन्छ, आगोले तापले छुन्छ। तर त्यो यी दुवैभन्दा बढी छोइने हुन्छ।"):
            self.play(FadeIn(sf, scale=0.5), FadeIn(fl, scale=0.5), FadeIn(l1), FadeIn(l2), run_time=0.8)
            self.play(Rotate(sf, PI / 3), Indicate(fl, color=GOLD), run_time=1.0)
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(hrt, scale=0.5), run_time=0.8)
        with self.say("अर्थात् त्यो सपनामा छामछुम गरेर बुझ्ने कुरा होइन। प्रत्यक्ष अनुभव हुने तीव्र यथार्थ हो, जसले चेतनालाई भित्रैसम्म झस्काउँछ।"):
            self.play(FadeIn(l3, shift=UP * 0.2), run_time=0.5)
            for _ in range(2):
                self.play(hrt.animate.scale(1.25), run_time=0.3)
                self.play(hrt.animate.scale(1 / 1.25), run_time=0.3)
        self.play(FadeOut(VGroup(q, sf, fl, hrt, a1, a2, l1, l2, l3, tag)), run_time=0.5)

    def k2(self):
        tag = self.ktag(2, "आमाको सपना", PINK)
        self.play(FadeIn(tag), run_time=0.3)
        ma = C.mother(2.6).move_to([-4.6, -3.1, 0], aligned_edge=DOWN)
        baby = C.child(1.0, topi=False).move_to([-3.4, -3.1, 0], aligned_edge=DOWN)
        mem = VGroup(C.pill("कलिलो अनुहार", PINK, 28), C.pill("हिस्सी परेको हाँसो", GOLD, 28), C.pill("तोते बोली", SKY, 28)).arrange(DOWN, buff=0.35)
        mem.move_to([1.8, -0.3, 0])
        cloud = Ellipse(width=6.4, height=3.6, stroke_color=th.PANEL_EDGE, stroke_width=3, fill_color=th.PANEL, fill_opacity=0.8).move_to(mem)
        dots = VGroup(*[Circle(radius=r, stroke_color=th.PANEL_EDGE, stroke_width=2, fill_color=th.PANEL, fill_opacity=0.8).move_to(p)
                        for r, p in ((0.12, [-2.6, 0.6, 0]), (0.2, [-2.0, 0.9, 0]))])
        with self.say("दोस्रो खण्डमा आमा पुरानो सम्झनामा डुब्छिन्। छोरा जन्मँदा उसको कलिलो अनुहार, हिस्सी परेको हाँसो र तोते बोलीमा उनले त्यो आउने कुराको छाया देखेकी थिइन्।") as v:
            self.play(FadeIn(ma, shift=UP * 0.2), FadeIn(baby, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(dots, lag_ratio=0.5), FadeIn(cloud, scale=0.8), run_time=0.8)
            for m in mem:
                self.play(FadeIn(m, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur / 3 - 1.1)
        self.play(FadeOut(VGroup(ma, baby, mem, cloud, dots)), run_time=0.5)
        q = C.show_quote(self, ["त्यो मिठो गीतले तिमीलाई", "आफ्नो बाँसुरी बनाएनछ"], "तर त्यसपछि एउटा पीडाले भरिएको पङ्क्ति आउँछ। त्यो मिठो गीतले तिमीलाई आफ्नो बाँसुरी बनाएनछ।",
                         color=PINK, size=42, where=UP * 1.8, keep=True, hl={"गीतले": GOLD, "बाँसुरी": PINK})
        fl = C.flute(4.0).move_to([1.6, -0.9, 0])
        notes = VGroup(*[C.note_glyph(GOLD, 0.32).move_to([-5.8 + 0.6 * k, -0.6 + 0.3 * np.sin(k), 0]) for k in range(4)])
        lg = T("गीत = क्रान्तिको सन्देश", size=26, color=GOLD).move_to([-3.8, -2.3, 0])
        lb = T("बाँसुरी = सन्देश बोक्ने वाहक", size=26, color=PINK).move_to([2.2, -2.3, 0])
        with self.say("बाँसुरी आफैँ गाउँदैन। गीत बाँसुरीबाट बग्छ। यहाँ गीत भनेको क्रान्तिको सन्देश हो, र बाँसुरी त्यो सन्देश बोक्ने वाहक।"):
            self.play(FadeIn(fl, shift=LEFT * 0.3), FadeIn(notes, lag_ratio=0.2), run_time=1.0)
            self.play(notes.animate.shift(RIGHT * 2.0), run_time=1.5)
            self.play(FadeIn(lg), FadeIn(lb), run_time=0.6)
        nb = self.neby("sad", height=1.4).move_to([5.6, -2.3, 0])
        with self.say("तर गीत बाँसुरीसम्म पुग्दै पुग्दैन। छोरा अझै त्यो वाहक बनेको छैन। यही आमाको गुनासो र पीडा हो।"):
            self.play(notes.animate.shift(RIGHT * 0.8).set_opacity(0), run_time=1.5)
            self.sfx("wrong", gain=-16)
            self.add(nb)
            self.play(FadeIn(nb), Indicate(fl, color=CORAL), run_time=0.8)
        self.play(FadeOut(VGroup(q, fl, lg, lb, tag)), FadeOut(nb), run_time=0.5)
        self.remove(nb, notes)

    def k3(self):
        tag = self.ktag(3, "सिर्जनाशक्तिकी आमा", CORAL)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["म आमा हुँ,", "सारा सिर्जनाशक्तिको मुख भएर"], "तेस्रो खण्डमा आमाको स्वर अचानक ठुलो हुन्छ। म आमा हुँ, सारा सिर्जनाशक्तिको मुख भएर।",
                         color=CORAL, size=44, where=UP * 1.8, keep=True, hl={"सिर्जनाशक्तिको": GOLD})
        ma = C.mother(2.4).move_to([-3.8, -3.1, 0], aligned_edge=DOWN)
        c = ma.get_center() + UP * 0.3
        rays = VGroup(*[Line(c + 1.4 * np.array([np.cos(a), np.sin(a), 0]), c + 2.0 * np.array([np.cos(a), np.sin(a), 0]), color=GOLD, stroke_width=4)
                        for a in np.linspace(0, TAU, 16, endpoint=False) if np.sin(a) > -0.6])
        sprouts = VGroup()
        for k, x in enumerate([0.6, 2.0, 3.4, 4.8]):
            stem = Line([x, -3.1, 0], [x, -2.4, 0], color=LEAFC, stroke_width=4)
            l1 = C.leaf(0.2).rotate(0.6).move_to([x + 0.18, -2.45, 0])
            l2 = C.leaf(0.2).rotate(-0.6 + PI).move_to([x - 0.18, -2.55, 0])
            sprouts.add(VGroup(stem, l1, l2))
        lab = T("नयाँ जीवन · नयाँ युग · मातृभूमि", size=28, color=GOLD, weight="SEMIBOLD").move_to([2.7, -1.0, 0])
        with self.say("यहाँ आमा एउटा घरकी आमा मात्र रहँदिनन्। उनी नयाँ जीवन र नयाँ युगलाई जन्म दिने सिर्जनाशक्ति बन्छिन्, मातृभूमि नै बन्छिन्।"):
            self.play(FadeIn(ma, shift=UP * 0.2), run_time=0.6)
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.08), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in sprouts], lag_ratio=0.25), FadeIn(lab, shift=UP * 0.2), run_time=1.5)
        self.play(FadeOut(VGroup(q, ma, rays, sprouts, lab)), run_time=0.5)
        q = C.show_quote(self, ["मैले यो कुनै अल्छी सपना देखेको होइन"], "उनी भन्छिन्, मैले यो कुनै अल्छी सपना देखेको होइन। अर्थात् यो आलस्यको कल्पना होइन, कर्मसँग जोडिएको दृढ विश्वास हो।",
                         color=CORAL, size=42, where=UP * 1.9, keep=True, hl={"अल्छी": CORAL})
        self.play(FadeOut(q), run_time=0.4)
        left = C.card("अहिले", "सत्य कुरालाई आमाको काखमा घोप्टिएर कथा सुने झैँ सुन्ने", th.MUTED, w=4.6, h=2.6, hsize=34, bsize=26).move_to([-3.4, 0.3, 0])
        lp = C.pill("निष्क्रिय", th.MUTED, 28).next_to(left, DOWN, buff=0.35)
        right_items = VGroup(C.pill("आफैँ देख्ने", MINT, 28), C.pill("सहने", MINT, 28), C.pill("ग्रहण गर्ने", MINT, 28)).arrange(DOWN, buff=0.22)
        rbox = C.box(4.6, 2.6, color=MINT)
        rhead = T("त्यो आएपछि", size=34, color=MINT, weight="BOLD")
        rin = VGroup(rhead, right_items).arrange(DOWN, buff=0.22).move_to(rbox)
        right = VGroup(rbox, rin).move_to([3.4, 0.3, 0])
        rp = C.pill("सक्रिय", MINT, 28).next_to(right, DOWN, buff=0.35)
        arr = Arrow(left.get_right(), right.get_left(), buff=0.2, color=GOLD, stroke_width=6)
        with self.say("र त्यसपछि आउँछ चेतनाको रूपान्तरण। अहिले छोरा सत्य कुरालाई आमाको काखमा घोप्टिएर, कथा सुने झैँ सुन्छ। त्यो निष्क्रिय सुनाइ हो।"):
            self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.7)
            self.play(FadeIn(lp), run_time=0.4)
        with self.say("तर त्यो आएपछि ऊ सत्यलाई आफैँ देख्न सक्ने, सहन सक्ने र ग्रहण गर्न सक्ने हुनेछ। सुन्नु र ग्रहण गर्नुमा यही भिन्नता छ। एउटा निष्क्रिय, अर्को सक्रिय।"):
            self.play(GrowArrow(arr), run_time=0.5)
            self.play(FadeIn(rbox), FadeIn(rhead), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in right_items], lag_ratio=0.4), run_time=1.5)
            self.play(FadeIn(rp), run_time=0.4)
        self.play(FadeOut(VGroup(left, lp, right, rp, arr, tag)), run_time=0.5)

    def k4(self):
        tag = self.ktag(4, "भूमिकाको परिवर्तन", SKY)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["मैले यसरी रोगीलाई झैँ", "तिम्रो कपाल मुसारिरहनुपर्ने छैन"], "चौथो खण्डमा आमा आफ्नै भूमिका बदलिने कल्पना गर्छिन्। मैले यसरी रोगीलाई झैँ तिम्रो कपाल मुसारिरहनुपर्ने छैन।",
                         color=SKY, size=42, where=UP * 1.8, keep=True, hl={"रोगीलाई": CORAL})
        self.play(q.animate.scale(0.75).to_edge(UP, buff=0.75), run_time=0.5)
        ma = C.mother(2.4).move_to([-4.2, -3.1, 0], aligned_edge=DOWN)
        ch = C.child(1.3).move_to([4.2, -3.1, 0], aligned_edge=DOWN)
        arr = Arrow([-2.6, -1.4, 0], [2.6, -1.4, 0], color=PINK, stroke_width=7)
        cares = VGroup(T("सम्झाउने", size=26, color=PINK), T("धैर्य दिने", size=26, color=PINK), T("कपाल मुसार्ने", size=26, color=PINK)).arrange(RIGHT, buff=0.5)
        cares.next_to(arr, UP, buff=0.25)
        st1 = C.pill("छोरा: असहाय र आश्रित", th.MUTED, 24).next_to(arr, DOWN, buff=0.35)
        with self.say("अहिले आमाले छोरालाई सम्झाउनुपर्छ, धैर्य दिनुपर्छ, बिरामीलाई झैँ कपाल सुम्सुम्याउनुपर्छ। छोरा असहाय र आश्रित छ।"):
            self.play(FadeIn(ma), FadeIn(ch), run_time=0.6)
            self.play(GrowArrow(arr), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cares], lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(st1), run_time=0.4)
        arr2 = Arrow([2.6, -1.4, 0], [-2.6, -1.4, 0], color=MINT, stroke_width=7)
        gives = VGroup(T("सान्त्वना दिने", size=26, color=MINT), T("सङ्ग्राममा जाने", size=26, color=MINT)).arrange(RIGHT, buff=0.6).next_to(arr2, UP, buff=0.25)
        st2 = C.pill("छोरा: सक्षम र नेतृत्वकारी", MINT, 24).next_to(arr2, DOWN, buff=0.35)
        big = C.child(2.3).move_to([4.2, -3.1, 0], aligned_edge=DOWN)
        with self.say("तर परिवर्तन आएपछि दृश्य उल्टिन्छ। छोरा आफैँ सङ्ग्राममा जान्छ, र लाख सम्झाए पनि नमान्ने आमाको मनलाई उल्टै उसैले सान्त्वना दिन्छ। पीडित र आश्रितबाट सक्षम र नेतृत्वकारी बन्ने यात्रा यहीँ देखिन्छ।"):
            self.sfx("whoosh", gain=-12)
            self.play(Transform(arr, arr2), FadeOut(cares), FadeOut(st1), Transform(ch, big), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 0.2) for g in gives], lag_ratio=0.3), run_time=1.0)
            self.play(FadeIn(st2), run_time=0.4)
        self.play(FadeOut(VGroup(q, ma, ch, arr, gives, st2, tag)), run_time=0.5)

    def k5(self):
        tag = self.ktag(5, "हुरी र पात", LEAFC)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["हेरौँला, त्यो हुरी भएर आउने छ", "तिमी पात भएर पछ्याउने छौ"], "अब कविताको सबैभन्दा चर्चित पङ्क्ति, जुन परीक्षामा बारम्बार सोधिन्छ। हेरौँला, त्यो हुरी भएर आउने छ, तिमी पात भएर पछ्याउने छौ।",
                         color=LEAFC, size=44, where=UP * 1.8, keep=True, hl={"हुरी": SKY, "पात": LEAFC})
        self.play(q.animate.scale(0.72).to_edge(UP, buff=0.7), run_time=0.5)
        rng = np.random.default_rng(9)
        leaves = VGroup(*[C.leaf(rng.uniform(0.16, 0.26), color=rng.choice([LEAFC, "#8BCB5A", "#D9A441", "#C8763A"])).rotate(rng.uniform(0, TAU)).move_to([rng.uniform(-6.0, -2.5), rng.uniform(-3.0, -2.4), 0])
                          for _ in range(14)])
        grd = Line([-7, -3.15, 0], [7, -3.15, 0], color="#4A5A3A", stroke_width=6)
        wl = C.wind_lines(8, seed=4)
        lh = C.pill("हुरी = परिवर्तनको प्रचण्ड वेग", SKY, 26).move_to([-3.3, 0.6, 0])
        lp = C.pill("पात = जनता, छोरा", LEAFC, 26).move_to([3.3, 0.6, 0])
        with self.say("हुरी भनेको परिवर्तनको प्रचण्ड, रोक्नै नसकिने वेग हो। पात भनेको जनता, अर्थात् छोरा। हुरी चलेपछि पात एक ठाउँमा थामिएर बस्न सक्दैन। हुरीसँगै उड्छ।"):
            self.play(Create(grd), FadeIn(leaves, lag_ratio=0.05), run_time=0.8)
            self.play(FadeIn(lh, shift=DOWN * 0.2), FadeIn(lp, shift=DOWN * 0.2), run_time=0.6)
            self.sfx("whoosh", gain=-8)
            self.play(LaggedStart(*[Create(w) for w in wl], lag_ratio=0.1), run_time=0.8)
            anims = []
            for l in leaves:
                end = np.array([rng.uniform(1.5, 6.3), rng.uniform(-2.6, -0.2), 0])
                anims.append(l.animate(path_arc=rng.uniform(-1.2, -0.4)).move_to(end).rotate(rng.uniform(2, 4)))
            self.play(*anims, wl.animate.shift(RIGHT * 2.5).set_opacity(0), run_time=2.5, rate_func=rate_functions.ease_in_out_sine)
        with self.say("त्यसै गरी परिवर्तनको लहर आएपछि जनता पनि निष्क्रिय बस्न सक्दैनन्। जनसहभागिताबिना क्रान्ति पूरा हुँदैन।"):
            self.play(*[l.animate.shift(RIGHT * 0.3 + UP * 0.15).rotate(0.6) for l in leaves], run_time=1.5)
            self.play(Indicate(lp, color=LEAFC), run_time=1.0)
        self.play(FadeOut(VGroup(q, leaves, grd, lh, lp)), run_time=0.5)
        self.remove(wl)
        q = C.show_quote(self, ["जीवनलोकबाट झरेर जून जस्तै पोखिँदा", "सारा जडता सगबगाएको थियो"], "यही खण्डमा अर्को सुन्दर बिम्ब छ। जीवनलोकबाट झरेर जून जस्तै पोखिँदा सारा जडता सगबगाएको थियो।",
                         color=LEAFC, size=42, where=UP * 1.9, keep=True, hl={"जून": "#F3EBC8", "जडता": th.MUTED})
        self.play(q.animate.scale(0.72).to_edge(UP, buff=0.7), run_time=0.5)
        mn = C.moon(0.5).move_to([4.8, 1.0, 0])
        beam = Polygon([4.6, 0.6, 0], [5.0, 0.6, 0], [3.5, -3.1, 0], [-4.8, -3.1, 0], stroke_width=0, fill_color="#F3EBC8", fill_opacity=0.0)
        sleepers = VGroup()
        pivots = []
        for x in np.linspace(-4.5, 1.5, 5):
            p = C.person(1.3, color="#4A5070")
            p.move_to([x, -3.1, 0], aligned_edge=DOWN)
            piv = p.get_bottom() + RIGHT * 0.26
            p.rotate(-PI / 2, about_point=piv)
            sleepers.add(p)
            pivots.append(piv)
        with self.say("जून शीतल र सुन्दर प्रकाश हो। त्यो जस्तै पोखिँदा सुतेको जडता सगबगाउन थाल्छ।"):
            self.play(FadeIn(mn, scale=0.6), FadeIn(sleepers), run_time=0.8)
            self.play(beam.animate.set_fill(opacity=0.12), run_time=1.5)
        rise = T("त्यो आउने छ, तिमी उठ्ने छौ", size=34, color=GOLD, weight="BOLD").move_to([0, 0.2, 0])
        with self.say("यहाँ परिवर्तनको सौन्दर्य पनि छ, र जडता तोड्ने शक्ति पनि। आमा भन्छिन्, त्यो आउने छ, तिमी उठ्ने छौ।"):
            self.play(LaggedStart(*[Rotate(p, PI / 2, about_point=pv) for p, pv in zip(sleepers, pivots)], lag_ratio=0.2), run_time=2.0)
            self.play(sleepers.animate.set_color("#C9A46A"), FadeIn(rise, shift=UP * 0.2), run_time=0.8)
        self.play(FadeOut(VGroup(q, mn, beam, sleepers, rise, tag)), run_time=0.5)
        self.quiz("'हेरौँला, त्यो हुरी भएर आउने छ, तिमी पात भएर पछ्याउने छौ' — यहाँ 'हुरी' र 'पात' ले क्रमशः के जनाउँछन् ?",
                  ["जनता र क्रान्ति", "क्रान्तिको वेग र जनता", "आमा र छोरा", "आँधी र रुखको पात"], 1,
                  "अब तपाईँको पालो। यस पङ्क्तिमा हुरी र पातले क्रमशः के जनाउँछन्? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ख हो। हुरी क्रान्ति वा परिवर्तनको प्रचण्ड वेग हो, र पात जनता हो, जसले त्यो वेगलाई पछ्याउँछ। क विकल्पमा क्रम उल्टो छ, ध्यान दिनुहोस्। र घ विकल्पले शाब्दिक अर्थ मात्र दिन्छ। कवितामा यी प्रतीक हुन्, साधारण आँधी र पात होइनन्।")

    def k6(self):
        tag = self.ktag(6, "सपनाको उत्तराधिकार", MINT)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["अब म उठेँ, गएँ, तर त्यो तिमी नै हौला", "भन्ने मेरो यौवनभरिको सपना थियो"], "अन्तिम खण्ड। अब म उठेँ, गएँ, तर त्यो तिमी नै हौला भन्ने मेरो यौवनभरिको सपना थियो।",
                         color=MINT, size=42, where=UP * 1.8, keep=True, hl={"तिमी": SKY, "सपना": GOLD})
        self.play(q.animate.scale(0.75).to_edge(UP, buff=0.7), run_time=0.5)
        ma = C.mother(2.5).move_to([-3.6, -3.1, 0], aligned_edge=DOWN)
        son = C.child(2.3).move_to([3.4, -3.1, 0], aligned_edge=DOWN)
        tc = C.torch(1.0).move_to(ma.get_center() + RIGHT * 0.75 + UP * 0.3)
        with self.say("अब म उठेँ, गएँ भन्दा आमा एउटा पुस्ताको प्रतिनिधिका रूपमा बिदा हुन्छिन्। तर जानुअघि आफ्नो जवानीभरिको सपनाको भार छोराको हातमा सुम्पिन्छिन्।"):
            self.play(FadeIn(ma), FadeIn(son), FadeIn(tc, shift=UP * 0.2), run_time=0.8)
            self.play(tc.animate(path_arc=-0.8).move_to(son.get_center() + LEFT * 0.55 + UP * 0.5), run_time=2.0)
            self.sfx("shimmer", gain=-12)
            self.play(Flash(tc[1], color=GOLD, flash_radius=0.5), ma.animate.set_opacity(0.45), run_time=0.8)
        lab = C.pill("निराशा होइन, जिम्मेवारीको हस्तान्तरण", GOLD, 30).move_to([0, 0.3, 0])
        with self.say("जसरी एउटा धावकले अर्को धावकलाई मसाल दिन्छ, त्यसरी नै सपना एक पुस्ताबाट अर्को पुस्तामा पुग्छ। यो निराशा होइन, जिम्मेवारीको हस्तान्तरण हो।"):
            self.play(FadeIn(lab, scale=0.8), run_time=0.6)
            self.play(son.animate.shift(UP * 0.15), tc.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.0)
        self.play(FadeOut(VGroup(q, ma, son, tc, lab, tag)), run_time=0.5)

    # ------------------------------------------------------------------ part 5: symbols & characters
    def p5(self):
        self.section(4)
        top = C.node("त्यो", GOLD, size=36, sub="क्रान्ति · परिवर्तनकारी शक्ति · मुक्तिको चेतना", w=6.4).move_to([0, 1.9, 0])
        lft = C.node("आमा", PINK, size=36, sub="मातृभूमि · जनचेतना · अघिल्लो पुस्ता", w=5.4).move_to([-3.6, -1.3, 0])
        rgt = C.node("छोरा  ('बा')", SKY, size=36, sub="युवा पुस्ता · जनता · उत्तराधिकारी", w=5.4).move_to([3.6, -1.3, 0])
        ma = C.mother(1.5).next_to(lft, DOWN, buff=0.2)
        ch = C.child(1.0).next_to(rgt, DOWN, buff=0.2)
        l1 = C.link(lft, top, color=PINK, label="सपना", size=22)
        l2 = C.link(top, rgt, color=GOLD, label="हुरी र पात", size=22)
        l3 = C.link(lft, rgt, color=th.MUTED, label="संवाद", size=22, both=True)
        with self.say("यो कवितामा पात्र थोरै छन्, तर हरेक पात्र एउटा प्रतीक हो। आमा, मातृभूमि र जनचेतनाको प्रतीक हुन्। उनी अघिल्लो पुस्ता र पीडित जनताको आवाज पनि हुन्।"):
            self.play(FadeIn(lft, scale=0.8), FadeIn(ma, shift=UP * 0.2), run_time=0.8)
        with self.say("छोरा, जसलाई आमाले माया गरेर बा भन्छिन्, नेपाली युवा पुस्ता र जनताको प्रतीक हो। ऊ क्रान्तिको उत्तराधिकारी हो।"):
            self.play(FadeIn(rgt, scale=0.8), FadeIn(ch, shift=UP * 0.2), run_time=0.8)
            self.play(Create(l3[0]), FadeIn(l3[1:]), run_time=0.6)
        with self.say("र त्यो, जसको नाम कविले कतै लिएका छैनन्, क्रान्ति हो। परिवर्तनकारी शक्ति, मुक्तिको चेतना। नाम नलिनुले नै यसको अर्थलाई व्यापक बनाएको छ।"):
            self.sfx("shimmer", gain=-14)
            self.play(FadeIn(top, scale=0.8), run_time=0.6)
            self.play(GrowArrow(l1[0]), FadeIn(l1[1:]), GrowArrow(l2[0]), FadeIn(l2[1:]), run_time=0.9)
        self.play(FadeOut(VGroup(top, lft, rgt, ma, ch, l1, l2, l3)), run_time=0.5)
        head = C.heading("प्रतीकको शब्दकोश", color=self.color)
        items = [("sun", "बिहानको सूर्य", "नयाँ युग, आशा", GOLD), ("sword", "शीत जस्तै हतियार", "शुद्ध र नैतिक शक्ति", SKY),
                 ("flute", "बाँसुरी", "क्रान्तिको स्वर बोक्ने माध्यम", PINK), ("wind", "हुरी", "परिवर्तनको प्रचण्ड वेग", "#9FB4E8"),
                 ("leaf", "पात", "जनता, अनुयायी शक्ति", LEAFC), ("moon", "जून", "शीतल, सुन्दर प्रकाश", "#F3EBC8"),
                 ("jadata", "जडता", "निष्क्रियता, अन्धविश्वास", th.MUTED)]
        cards = VGroup(*[self.sym_card(*it) for it in items])
        row1 = VGroup(*cards[:4]).arrange(RIGHT, buff=0.18)
        row2 = VGroup(*cards[4:]).arrange(RIGHT, buff=0.18)
        VGroup(row1, row2).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.25)
        with self.say("अब कवितामा आएका अरू प्रतीकहरूलाई एकै ठाउँमा राखौँ। बिहानको सूर्य, नयाँ युग र आशा। शीत जस्तै टल्कने हतियार, शुद्ध र नैतिक शक्ति। बाँसुरी, क्रान्तिको स्वर बोक्ने माध्यम। हुरी, परिवर्तनको प्रचण्ड वेग। पात, जनता। जून, शीतल र सुन्दर प्रकाश। र जडता, निष्क्रियता र पुरानो अन्धविश्वास।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for c in cards:
                self.sfx("pop", gain=-15)
                self.play(FadeIn(c, shift=UP * 0.2, scale=0.9), run_time=0.45)
                self.hold(v.dur / 7 - 0.6)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        self.quiz("'आमाको सपना' कवितामा 'त्यो' ले के जनाउँछ ?",
                  ["आमाको छोरो", "बिहानको घाम", "क्रान्ति वा परिवर्तनकारी शक्ति", "घर आउने पाहुना"], 2,
                  "एक अङ्कको प्रश्न, तर धेरैले गल्ती गर्छन्। कवितामा त्यो ले के जनाउँछ? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ग हो, क्रान्ति वा परिवर्तनकारी शक्ति। ख विकल्प आकर्षक लाग्छ, किनकि त्यो बिहानको सूर्य झैँ आउँछ भनिएको छ। तर झैँ ले तुलना मात्र गर्छ। त्यो सूर्य जस्तै उज्यालो छर्दै आउने कुरा हो, आफैँ सूर्य होइन। र छोरो त तिमी हो, त्यो होइन।")

    # ------------------------------------------------------------------ part 6: theme & critique
    def p6(self):
        self.section(5)
        block = C.kblock(["अन्याय र जडताको अन्धकार चिर्ने परिवर्तन अवश्य आउँछ;", "तर त्यसलाई पर्खेर बस्ने होइन,", "जनता आफैँ चेतनशील भएर त्यसको वाहक बन्नुपर्छ।"],
                         size=38, hl={"अवश्य": GOLD, "पर्खेर": CORAL, "वाहक": MINT}, buff=0.35)
        block.move_to(UP * 0.3)
        fr = C.quote_frame(block, GOLD)
        with self.say("अब कविताको केन्द्रीय आशय। अन्याय र जडताको अन्धकारलाई चिर्ने परिवर्तन अवश्य आउँछ। तर त्यसलाई पर्खेर बस्ने होइन। जनता आफैँ चेतनशील र सङ्घर्षशील भएर त्यसको वाहक बन्नुपर्छ।") as v:
            self.play(FadeIn(fr), run_time=0.5)
            C.type_in(self, block, run_time=min(v.dur * 0.7, 6))
        self.play(FadeOut(VGroup(fr, block)), run_time=0.5)
        head = C.heading("मूल भावका तीन खम्बा", color=self.color)
        data = [("आशा", "अँध्यारोमा पनि उज्यालो आउने विश्वास", GOLD),
                ("जिम्मेवारी", "सपना साकार पार्ने दायित्व छोराको", SKY),
                ("निरन्तरता", "एक पुस्ताको अधुरो सपना अर्कोले पूरा गर्छ", MINT)]
        base = Rectangle(width=11, height=0.25, stroke_width=0, fill_color=th.PANEL_EDGE, fill_opacity=1).move_to([0, -2.9, 0])
        roof = Polygon([-5.8, 1.55, 0], [5.8, 1.55, 0], [0, 2.45, 0], stroke_width=0, fill_color=th.PANEL_EDGE, fill_opacity=1)
        roof_t = T("आमाको सपना", size=26, color=th.INK, weight="BOLD").move_to([0, 1.85, 0])
        pillars = []
        narrs = ["यसलाई तीन खम्बामा राख्न सकिन्छ। पहिलो, आशा। अँध्यारोका बिचमा पनि उज्यालो आउने विश्वास।",
                 "दोस्रो, जिम्मेवारी। आमाको सपना सुन्ने मात्र होइन, त्यसलाई साकार पार्ने दायित्व छोराको हो।",
                 "तेस्रो, निरन्तरता। एउटा पुस्ताले अधुरो छाडेको सपना अर्को पुस्ताले पूरा गर्छ।"]
        self.play(FadeIn(head), FadeIn(base), run_time=0.5)
        for i, (n, b, c) in enumerate(data):
            x = [-3.8, 0, 3.8][i]
            col = Rectangle(width=2.9, height=4.2, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.15).move_to([x, -0.68, 0])
            nt = T(n, size=34, color=c, weight="BOLD").move_to([x, 0.6, 0])
            bt = para(b, width=2.5, size=23, color=th.BODY, align="center").move_to([x, -1.1, 0])
            with self.say(narrs[i]):
                self.play(GrowFromEdge(col, DOWN), run_time=0.7)
                self.play(FadeIn(nt, shift=DOWN * 0.2), FadeIn(bt), run_time=0.6)
            pillars.append(VGroup(col, nt, bt))
        self.play(FadeIn(roof, shift=DOWN * 0.3), FadeIn(roof_t), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(VGroup(head, base, roof, roof_t, *pillars)), run_time=0.5)
        self.balance()

    def balance(self):
        head = C.heading("समीक्षा: बलियो र कमजोर पक्ष", color=self.color)
        pivot = np.array([0, 1.4, 0])
        post = Line([0, -2.9, 0], pivot, color=th.MUTED, stroke_width=6)
        baseL = Line([-1.0, -2.9, 0], [1.0, -2.9, 0], color=th.MUTED, stroke_width=8)
        beam = Line(pivot + LEFT * 4.3, pivot + RIGHT * 4.3, color=th.MUTED, stroke_width=7)

        def pan(x, title, items, col):
            hang = VGroup(Line([x, 1.4, 0], [x - 1.3, 0.6, 0], color=th.FAINT, stroke_width=2),
                          Line([x, 1.4, 0], [x + 1.3, 0.6, 0], color=th.FAINT, stroke_width=2))
            dish = ArcBetweenPoints([x - 1.6, 0.6, 0], [x + 1.6, 0.6, 0], angle=PI / 3).set_stroke(col, 5)
            t = T(title, size=28, color=col, weight="BOLD").move_to([x, 0.95, 0])
            ps = VGroup(*[C.pill(s_, col, 21) for s_ in items]).arrange(DOWN, buff=0.15).next_to(dish, DOWN, buff=0.25)
            return VGroup(hang, dish, t), ps
        lp, lps = pan(-4.3, "बलियो पक्ष", ["सरलता र गहिराइको मेल", "सटीक प्रतीक", "गद्य कविताको नयाँ बाटो"], MINT)
        rp, rps = pan(4.3, "कमजोर पक्ष", ["'त्यो' अस्पष्ट", "क्रान्तिको योजना छुटेको", "पर्खाइको भाव बढी"], CORAL)
        lp.set_z_index(1)
        with self.say("समीक्षात्मक प्रश्नका लागि कविताका बलिया र कमजोर दुवै पक्ष जान्नुपर्छ। बलियो पक्ष हो, सरलता र गहिराइको मेल। घरेलु संवादमा राष्ट्रिय चेतना राखिएकाले कविता नारा बन्दैन, मानवीय बन्छ। प्रतीकहरू सटीक छन्, र गद्य कविताको नयाँ बाटो खोल्ने ऐतिहासिक महत्त्व पनि छ।"):
            self.play(FadeIn(head), Create(post), Create(baseL), Create(beam), FadeIn(lp), FadeIn(rp), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in lps], lag_ratio=0.5), run_time=2.0)
        with self.say("कमजोर पक्ष पनि छन्। त्यो के हो भनेर स्पष्ट नभनिएकाले अर्थ पाठकको व्याख्यामा निर्भर हुन्छ। क्रान्ति कसरी आउँछ भन्ने योजना छुटेको छ, र कतै कतै पर्खाइको भाव कर्मभन्दा बढी देखिन्छ।"):
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in rps], lag_ratio=0.5), run_time=2.0)
        with self.say("तैपनि समग्रमा बलियो पक्ष भारी पर्छ। यो कविताले पाठकलाई परिवर्तनको पर्खाइमा होइन, परिवर्तनको सहभागी बन्न प्रेरित गर्छ।"):
            self.play(Rotate(beam, 0.1, about_point=pivot), VGroup(lp, lps).animate.shift(DOWN * 0.42), VGroup(rp, rps).animate.shift(UP * 0.42), run_time=1.5)
        self.play(FadeOut(VGroup(head, post, baseL, beam, lp, lps, rp, rps)), run_time=0.5)

    # ------------------------------------------------------------------ part 7: genre & style
    def p7(self):
        self.section(6)
        d = self.callout("key", "जुन कवितामा छन्द, तुक र निश्चित अक्षरगणनाको बन्धन हुँदैन, तर गद्यको सहज लयभित्र भाव, बिम्ब र प्रतीकको काव्यात्मक घनत्व हुन्छ, त्यसलाई गद्य कविता भनिन्छ।", width=11, size=30).move_to(ORIGIN)
        with self.say("पहिले विधा। जुन कवितामा छन्द, तुक र निश्चित अक्षरगणनाको बन्धन हुँदैन, तर गद्यको सहज लयभित्र भाव, बिम्ब र प्रतीकको काव्यात्मक घनत्व हुन्छ, त्यसलाई गद्य कविता भनिन्छ।"):
            self.play(FadeIn(d, shift=UP * 0.3), run_time=0.7)
        self.play(FadeOut(d), run_time=0.4)
        head = C.heading("पद्य कविता र गद्य कविता", color=self.color)
        xs = [-4.4, -0.6, 3.6]
        hdr = VGroup(T("आधार", size=30, color=th.MUTED, weight="BOLD").move_to([xs[0], 1.9, 0]),
                     T("पद्य कविता", size=30, color=SKY, weight="BOLD").move_to([xs[1], 1.9, 0]),
                     T("गद्य कविता", size=30, color=GOLD, weight="BOLD").move_to([xs[2], 1.9, 0]))
        rule = Line([-6.2, 1.5, 0], [6.2, 1.5, 0], color=th.FAINT, stroke_width=2)
        rows = [("छन्द", "निश्चित छन्द हुन्छ", "निश्चित छन्द हुँदैन"), ("तुक", "प्रायः तुक मिलाइन्छ", "तुक अनिवार्य हुँदैन"),
                ("लय", "अक्षरगणना र गतियुक्त लय", "गद्यको सहज लय"), ("उदाहरण", "'धृतराष्ट्र'", "'आमाको सपना'")]
        rg = []
        for i, r in enumerate(rows):
            y = 0.9 - i * 0.95
            g = VGroup(*[T(t_, size=26, color=[th.INK, SKY, GOLD][k]).move_to([xs[k], y, 0]) for k, t_ in enumerate(r)])
            rg.append(g)
        with self.say("पद्य कविता र गद्य कविताबिचको भिन्नता तालिकामा हेरौँ। पद्यमा निश्चित छन्द हुन्छ, गद्य कवितामा हुँदैन। पद्यमा प्रायः तुक मिलाइन्छ, गद्य कवितामा तुक अनिवार्य छैन। पद्यको लय अक्षरगणनामा चल्छ, गद्य कविताको लय बोलीको सहज प्रवाहमा। पाठ्यपुस्तकको धृतराष्ट्र पद्य कविता हो, आमाको सपना गद्य कविता।") as v:
            self.play(FadeIn(head), FadeIn(hdr), Create(rule), run_time=0.6)
            for g in rg:
                self.play(FadeIn(g, shift=UP * 0.15), run_time=0.5)
                self.hold(v.dur / 4 - 0.8)
        self.play(FadeOut(VGroup(head, hdr, rule, *rg)), run_time=0.5)
        reps = VGroup(*[T("हो, त्यो आउँछ", size=s_, color=c, weight="BOLD") for s_, c in ((36, th.MUTED), (48, th.BODY), (62, GOLD))]).arrange(DOWN, buff=0.4)
        lab = C.pill("आवृत्ति = लय", MINT, 28).next_to(reps, DOWN, buff=0.5)
        with self.say("तब यस कवितामा लय कहाँबाट आउँछ? आवृत्तिबाट। हो, त्यो आउँछ, भन्ने पङ्क्ति पटक पटक दोहोरिएर विश्वासलाई दृढ बनाउँछ, र त्यही दोहोराइ यसको लय बन्छ।"):
            for r in reps:
                self.sfx("tick", gain=-10)
                self.play(FadeIn(r, scale=0.8), run_time=0.6)
            self.play(FadeIn(lab), run_time=0.4)
        self.play(FadeOut(VGroup(reps, lab)), run_time=0.4)
        styles = VGroup(C.pill("संवादात्मक शैली  (प्रमुख)", GOLD, 30), C.pill("आत्मकथनात्मक", SKY, 28), C.pill("प्रतीकात्मक", PINK, 28)).arrange(RIGHT, buff=0.35).move_to(UP * 1.5)
        with self.say("शैलीको कुरा गर्दा, यो कविता मुख्य रूपमा संवादात्मक शैलीमा छ। बिचबिचमा, म आमा हुँ भन्ने जस्ता आत्मकथनात्मक र प्रतीकात्मक शैली मिसिएको छ।"):
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in styles], lag_ratio=0.3), run_time=1.5)
        sims = C.kblock(["बिहानको सूर्य झैँ उज्यालो", "शीत जस्तै टल्कने हतियार", "जून जस्तै पोखिँदा", "रोगीलाई झैँ कपाल मुसार्नु"], size=34, hl={"झैँ": GOLD, "जस्तै": GOLD}, buff=0.3).move_to(DOWN * 1.0)
        ul = T("उपमा अलङ्कार", size=30, color=GOLD, weight="BOLD").next_to(sims, LEFT, buff=0.7)
        with self.say("कविले उपमा अलङ्कार धेरै प्रयोग गरेका छन्। झैँ र जस्तै जस्ता शब्दले दुई कुराबिच तुलना गरिन्छ। बिहानको सूर्य झैँ, शीत जस्तै, जून जस्तै, रोगीलाई झैँ।"):
            self.play(FadeIn(ul), run_time=0.4)
            C.type_in(self, sims, run_time=3.0)
        self.play(FadeOut(VGroup(styles, sims, ul)), run_time=0.5)
        q = C.show_quote(self, ["मधुर उषाले चराहरूको कण्ठलाई जस्तै", "… हृदयलाई कुत्कुत्याइसक्यो"], "र यो पङ्क्ति हेर्नुहोस्। मधुर उषाले चराहरूको कण्ठलाई जस्तै हृदयलाई कुत्कुत्याइसक्यो।",
                         color=PINK, size=40, where=UP * 1.6, keep=True, hl={"उषाले": GOLD, "कुत्कुत्याइसक्यो": PINK})
        birds = VGroup()
        for k in range(3):
            bd = VGroup(ArcBetweenPoints(LEFT * 0.35, ORIGIN, angle=-1.2), ArcBetweenPoints(ORIGIN, RIGHT * 0.35, angle=-1.2)).set_stroke(th.INK, 4)
            birds.add(bd.move_to([-2.5 + k * 1.2, -1.2 + 0.3 * (k % 2), 0]))
        dawn = C.sun(0.5, color="#F7A25E").move_to([3.6, -1.8, 0])
        lab = C.pill("मानवीकरण: निर्जीवलाई सजीव झैँ", MINT, 26).move_to([0, -2.7, 0])
        with self.say("यहाँ उषा, अर्थात् बिहानको पहिलो उज्यालोलाई, जीवित प्राणी झैँ कुत्कुत्याउने काम गर्ने बनाइएको छ। निर्जीवलाई सजीव झैँ देखाउनु मानवीकरण हो।"):
            self.play(FadeIn(dawn, shift=UP * 0.4), FadeIn(birds, lag_ratio=0.2), run_time=1.0)
            self.play(*[b.animate.shift(UP * 0.4) for b in birds], rate_func=there_and_back, run_time=1.0)
            self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(q, birds, dawn, lab)), run_time=0.5)
        self.word_order()
        self.word_sources()
        self.tip("'यो कुन विधाको रचना हो ?' भनी सोधिए 'गद्य कविता' लेख्नुहोस्। 'कविता' मात्र लेखे उत्तर अधुरो हुन्छ।",
                 "यहाँ एउटा सानो तर महँगो गल्ती हुन्छ। यो कुन विधाको रचना हो भनी सोधिए, गद्य कविता लेख्नुहोस्। कविता मात्र लेखे उत्तर अधुरो हुन्छ, र अङ्क कट्न सक्छ।")
        self.quiz("नेपाली भाषाको सामान्य (व्याकरणिक) पदक्रम कुन हो ?",
                  ["कर्ता + क्रिया + कर्म", "कर्ता + कर्म + क्रिया", "कर्म + कर्ता + क्रिया", "क्रिया + कर्ता + कर्म"], 1,
                  "पदक्रमबाट एउटा प्रश्न। नेपाली भाषाको सामान्य, अर्थात् व्याकरणिक पदक्रम कुन हो? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ख, कर्ता, कर्म, क्रिया। जस्तै, म भात खान्छु। क विकल्प, कर्ता, क्रिया, कर्म, अङ्ग्रेजीको क्रम हो। र ग विकल्प, कर्म पहिले आउने क्रम, कवितामा जोड दिन प्रयोग हुने आलङ्कारिक पदक्रम हो, सामान्य होइन।")

    def word_order(self):
        head = C.heading("पदक्रमको विचलन", color=self.color)

        def blk(word, role, col):
            t = T(word, size=34, color=th.INK, weight="BOLD")
            b = RoundedRectangle(corner_radius=0.15, width=t.width + 0.6, height=0.95, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.18)
            t.move_to(b)
            r = T(role, size=22, color=col).next_to(b, DOWN, buff=0.15)
            return VGroup(b, t, r)
        a = blk("तिमी", "कर्ता", SKY)
        b = blk("सत्य कुरालाई", "कर्म", GOLD)
        c = blk("सुन्ने छैनौ", "क्रिया", MINT)
        row = VGroup(a, b, c).arrange(RIGHT, buff=0.4).move_to(UP * 0.6)
        lab1 = C.pill("व्याकरणिक पदक्रम", SKY, 26).next_to(row, DOWN, buff=0.6)
        with self.say("अर्को विशेषता पदक्रमको विचलन हो। नेपालीको सामान्य पदक्रम हो, कर्ता, कर्म, क्रिया। जस्तै, तिमी सत्य कुरालाई सुन्ने छैनौ।"):
            self.play(FadeIn(head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in row], lag_ratio=0.3), run_time=1.2)
            self.play(FadeIn(lab1), run_time=0.4)
        pa, pb = a.get_center().copy(), b.get_center().copy()
        lab2 = C.pill("आलङ्कारिक पदक्रम: भावमा जोड", GOLD, 26).move_to(lab1)
        with self.say("तर कविले लेखे, सत्य कुरालाई तिमी सुन्ने छैनौ। कर्मलाई कर्ताभन्दा अगाडि सारेर सत्य कुरामाथि जोड दिइयो। साहित्यमा यसरी गरिने विचलनलाई आलङ्कारिक पदक्रम भनिन्छ।"):
            self.sfx("whoosh", gain=-12)
            w_a, w_b = a.width, b.width
            left_edge = row.get_left()[0]
            self.play(b.animate(path_arc=-PI / 2).move_to([left_edge + w_b / 2, pb[1], 0]),
                      a.animate(path_arc=-PI / 2).move_to([left_edge + w_b + 0.4 + w_a / 2, pa[1], 0]), run_time=1.2)
            self.play(Transform(lab1, lab2), Indicate(b, color=GOLD), run_time=0.9)
        self.play(FadeOut(VGroup(head, a, b, c, lab1)), run_time=0.5)

    def word_sources(self):
        head = C.heading("शब्दस्रोत", color=self.color)
        cols = [("तत्सम", ["सिर्जनाशक्ति", "अधर्म", "सङ्ग्राम", "यौवन", "सान्त्वना"], GOLD),
                ("तद्भव", ["आमा", "बिहान", "हिउँ", "आगो", "जून"], SKY),
                ("आगन्तुक", ["हतियार"], PINK)]
        groups = VGroup()
        for i, (h, ws, c) in enumerate(cols):
            hh = T(h, size=34, color=c, weight="BOLD")
            ps = VGroup(*[C.pill(w, c, 24) for w in ws]).arrange(DOWN, buff=0.18)
            g = VGroup(hh, ps).arrange(DOWN, buff=0.35).move_to([[-4.2, 0, 4.2][i], 0, 0]).align_to(UP * 2.2, UP)
            groups.add(g)
        with self.say("शब्दस्रोतको हिसाबले तत्सम, तद्भव र आगन्तुक शब्दको सुन्दर मेल छ। सिर्जनाशक्ति, अधर्म, सङ्ग्राम, यौवन, सान्त्वना तत्सम हुन्। आमा, बिहान, हिउँ, आगो, जून तद्भव हुन्। र हतियार आगन्तुक शब्द हो।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for g in groups:
                self.play(FadeIn(g[0]), LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in g[1]], lag_ratio=0.15), run_time=1.0)
                self.hold(v.dur / 3 - 1.2)
        self.play(FadeOut(VGroup(head, groups)), run_time=0.5)

    # ------------------------------------------------------------------ part 8: exam frames
    def p8(self):
        self.section(7)
        head = C.heading("परीक्षामा यो पाठ", color=self.color)
        base_y = -2.6
        u = 0.32
        b1 = Rectangle(width=1.6, height=8 * u, stroke_width=0, fill_color=SKY, fill_opacity=0.9).move_to([-1.5, base_y, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.6, height=8 * u, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([1.5, base_y, 0], aligned_edge=DOWN)
        l1 = VGroup(T("पाठगत बोध", size=26, color=SKY), T(self.num(8) + " अङ्क", size=30, color=th.INK, weight="BOLD")).arrange(DOWN, buff=0.1).next_to(b1, UP, buff=0.2)
        l2 = VGroup(T("समीक्षात्मक", size=26, color=GOLD), T(self.num(8) + " अङ्क", size=30, color=th.INK, weight="BOLD")).arrange(DOWN, buff=0.1).next_to(b2, UP, buff=0.2)
        tot = VGroup(T("जम्मा", size=26, color=th.MUTED), T(self.num(16) + " अङ्कसम्म", size=44, color=MINT, weight="BOLD")).arrange(DOWN, buff=0.1).move_to([4.9, -0.6, 0])
        with self.say("अब सबैभन्दा काम लाग्ने कुरा। यस्ता पाठबाट पाठगत बोधका आठ अङ्क र समीक्षात्मक प्रश्नका आठ अङ्क गरी जम्मा सोह्र अङ्कसम्म सोधिन सक्छ।"):
            self.play(FadeIn(head), run_time=0.4)
            self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.8)
            self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.8)
            self.sfx("impact", gain=-14)
            self.play(FadeIn(tot, scale=1.3), run_time=0.6)
        self.play(FadeOut(VGroup(b1, b2, l1, l2, tot)), run_time=0.5)
        kinds = VGroup(C.card("कवितांश व्याख्या", "उद्धरण दिएर सन्दर्भसहित अर्थ", SKY, w=3.9, h=2.4),
                       C.card("प्रतीकको प्रश्न", "'त्यो', 'तिमी', आमा र छोराले के जनाउँछन्", GOLD, w=3.9, h=2.4),
                       C.card("समीक्षात्मक प्रश्न", "आमाको सपना के हो, कसरी साकार हुन्छ", MINT, w=3.9, h=2.4)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        with self.say("परीक्षाले प्रायः तीन किसिमका कुरा खोज्छ। पहिलो, कवितांश दिएर व्याख्या। दोस्रो, त्यो, तिमी, आमा र छोराले के जनाउँछन् भन्ने प्रतीकको प्रश्न। तेस्रो, आमाको सपना के हो र कसरी साकार हुन्छ भन्ने समीक्षात्मक प्रश्न, जसमा सार दोहोर्‍याएर पुग्दैन, आफ्नै तर्क चाहिन्छ।") as v:
            for k in kinds:
                self.play(FadeIn(k, shift=UP * 0.3), run_time=0.5)
                self.hold(v.dur / 3 - 0.7)
        self.play(FadeOut(VGroup(head, kinds)), run_time=0.5)
        qq = para(f"प्रश्न: 'हेरौँला, त्यो हुरी भएर आउने छ, तिमी पात भएर पछ्याउने छौ' — सन्दर्भसहित व्याख्या गर्नुहोस्। [{self.num(4)}]", width=12, size=28, color=th.INK)
        qq.move_to(UP * 0.3)
        with self.say("पहिले चार अङ्कको कवितांश व्याख्या। हेरौँला, त्यो हुरी भएर आउने छ, तिमी पात भएर पछ्याउने छौ। यसको उत्तर तीन चरणमा लेख्नुहोस्।"):
            self.play(FadeIn(qq, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(qq), run_time=0.4)
        f1 = C.answer_frame(self, f"कवितांश व्याख्या: तीन चरण  [{self.num(4)}]", [
            ("सन्दर्भ", "यो अंश गोपालप्रसाद रिमालको गद्य कविता 'आमाको सपना' बाट लिइएको हो; आमाले छोरालाई क्रान्ति आउने विश्वास दिलाउँदा यी पङ्क्ति भनेकी हुन्।",
             "पहिलो चरण, सन्दर्भ। कुन कवि, कुन कविता, र कसले कसलाई कुन प्रसङ्गमा भनेको हो, एक दुई वाक्यमा लेख्नुहोस्।"),
            ("अर्थ विस्तार", "हुरी = क्रान्तिको तीव्र, प्रचण्ड वेग; पात = जनता वा छोरा। हुरी आएपछि पात थामिँदैन; परिवर्तनको लहरमा जनता पनि निष्क्रिय बस्दैनन्।",
             "दोस्रो चरण, अर्थ विस्तार। हरेक प्रतीक खोल्नुहोस्। हुरी भनेको क्रान्तिको प्रचण्ड वेग, पात भनेको जनता। अनि दुवैको सम्बन्ध देखाउनुहोस्।"),
            ("निचोड", "जनसहभागिताबिना क्रान्ति पूर्ण हुँदैन; क्रान्ति आएपछि जनता जागरुक भएर त्यसको साथ दिन्छन्।",
             "तेस्रो चरण, निचोड। पङ्क्तिले दिने सन्देश एक वाक्यमा टुङ्ग्याउनुहोस्। बस्, चार अङ्क पूरा।"),
        ], color=SKY, size=24, top=2.3)
        self.wait(0.8)
        self.play(FadeOut(f1), run_time=0.5)
        qq = para(f"प्रश्न: 'आमाको सपना' कविताले क्रान्तिको प्रतीक्षा मात्र होइन, जनताको उत्तरदायित्व पनि सम्झाउँछ। — तपाईँ कत्तिको सहमत हुनुहुन्छ ? [{self.num(8)}]", width=12, size=28, color=th.INK)
        qq.move_to(UP * 0.3)
        with self.say("अब आठ अङ्कको समीक्षात्मक प्रश्न। कविताले क्रान्तिको प्रतीक्षा मात्र होइन, जनताको उत्तरदायित्व पनि सम्झाउँछ। तपाईँ कत्तिको सहमत हुनुहुन्छ? यसको ढाँचा हेरौँ।"):
            self.play(FadeIn(qq, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(qq), run_time=0.4)
        f2 = C.answer_frame(self, f"समीक्षात्मक उत्तरको ढाँचा  [{self.num(8)}]", [
            ("भूमिका", "कवि, कविता र आफ्नो अडान: म यस भनाइसँग सहमत छु।",
             "भूमिकामा कवि र कविताको नाम लिएर आफ्नो अडान स्पष्ट भन्नुहोस्। म यस भनाइसँग सहमत छु।"),
            ("पहिलो आधार", "'त्यो आउने छ, तिमी उठ्ने छौ' — उठ्ने भार छोराकै; हुरीलाई पातले पछ्याउनुपर्छ।",
             "पहिलो आधार। त्यो आउने छ, तिमी उठ्ने छौ। क्रान्ति आएपछि पनि उठ्ने भार छोराकै हो।"),
            ("दोस्रो आधार", "कथा सुने झैँ होइन, आफैँ देख्ने, सहने र ग्रहण गर्ने — निष्क्रियताको अस्वीकार।",
             "दोस्रो आधार। आमा सत्यलाई कथा सुने झैँ सुन्ने छोरा चाहँदिनन्। आफैँ देख्ने, सहने र ग्रहण गर्ने छोरा चाहन्छिन्।"),
            ("तेस्रो आधार", "'अब म उठेँ, गएँ, तर त्यो तिमी नै हौला' — सपनाको हस्तान्तरण।",
             "तेस्रो आधार। अब म उठेँ, गएँ। आमाले सपनाको भार छोरालाई सुम्पिन्छिन्, अर्थात् उत्तरदायित्व अर्को पुस्तामा सर्छ।"),
            ("सीमा", "'त्यो' कसरी आउँछ भन्ने बाटो अस्पष्ट; कतै पर्खाइको भाव पनि बलियो।",
             "समीक्षा पूरा बनाउन एउटा सीमा पनि लेख्नुहोस्। त्यो कसरी आउँछ भन्ने बाटो अस्पष्ट छ।"),
            ("निष्कर्ष", "कविता प्रतीक्षाभन्दा बढी चेतना र जिम्मेवारीको आह्वान हो।",
             "र निष्कर्षमा भन्नुहोस्, यो कविता प्रतीक्षाभन्दा बढी चेतना र जिम्मेवारीको आह्वान हो।"),
        ], color=GOLD, size=22, top=2.4)
        self.wait(0.8)
        self.play(FadeOut(f2), run_time=0.5)
        self.tip("आठ अङ्कको उत्तरमा हरेक आधारसँग कविताको एउटा पङ्क्ति उद्धरण गर्नुहोस्, र अन्त्यमा 'सीमा' पनि लेख्नुहोस्।",
                 "अर्को सुझाव। आठ अङ्कको उत्तरमा हरेक आधारसँगै कविताको एउटा पङ्क्ति उद्धरण गर्नुहोस्। र अन्त्यतिर एउटा सीमा पनि लेख्नुहोस्। यसले उत्तरलाई साँच्चै समीक्षात्मक बनाउँछ, र परीक्षकले त्यही खोज्छन्।", state="success")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            f"'आमाको सपना' — गोपालप्रसाद रिमालको गद्य कविता; यही नामको सङ्ग्रहलाई मदन पुरस्कार ({self.num(2019)})",
            f"रिमाल: जन्म {self.num(1975)}, लगनटोल; निधन {self.num(2030)}; नेपाली गद्य कविताका आरम्भकर्ता",
            "छोरा सोध्छ 'त्यो आउँछ र ?', आमा भन्छिन् 'हो, बा, त्यो आउँछ'",
            "'त्यो' = क्रान्ति; छोरा = नयाँ पुस्ता, जनता; आमा = मातृभूमि, जनचेतना",
            "हुरी = परिवर्तनको वेग; पात = जनता; बाँसुरी = क्रान्तिको वाहक",
            "मूल भाव: परिवर्तन आउँछ, तर जनता आफैँ त्यसको वाहक बन्नुपर्छ",
            "व्याख्या: सन्दर्भ → अर्थ विस्तार → निचोड",
        ], "छोटो पुनरावलोकन गरौँ। आमाको सपना गोपालप्रसाद रिमालको गद्य कविता हो, र यही नामको सङ्ग्रहले मदन पुरस्कार पाएको छ। रिमाल नेपाली गद्य कविताका आरम्भकर्ता हुन्। कविता आमा र छोराको संवादमा अघि बढ्छ। त्यो भनेको क्रान्ति, छोरा भनेको नयाँ पुस्ता, र आमा भनेको मातृभूमि। हुरी परिवर्तनको वेग हो, पात जनता। मूल भाव, परिवर्तन आउँछ, तर जनता आफैँ त्यसको वाहक बन्नुपर्छ। र व्याख्या लेख्दा, सन्दर्भ, अर्थ विस्तार र निचोड।")
        self.outro("आजलाई यति नै। आमाको सपना अब तपाईँको पनि सपना बनोस्। अर्को पाठमा हामी मदनमणि दीक्षितको कथा, विरहिणी दमयन्ती पढ्नेछौँ। नेबियन्समा फेरि भेटौँला।")
