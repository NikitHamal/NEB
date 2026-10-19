import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, T, para, th  # noqa: E402
import _common as C  # noqa: E402

GOLD, SKY, MINT, CORAL, PINK, TEAL = th.AMBER, th.SKY, th.MINT, th.CORAL, th.PINK, th.TEAL
SNOW = "#EEF3FF"
ROCK = "#3E4A3A"


class Lesson(Lesson):
    SUBJECT = "nep"
    GRADE = 12
    UNIT = 3
    LANG = "ne"
    TITLE = "घनघस्याको उकालो काट्ता"
    SUBTITLE = "तारानाथ शर्मा  ·  नियात्रा"
    SECTIONS = ["लेखक परिचय", "नियात्रा: विधाको पहिचान", "पाठको पृष्ठभूमि", "यात्राको सार", "खण्डगत व्याख्या",
                "पात्र र मूल भाव", "भाषाशैली र अलङ्कार", "उत्तर लेख्ने ढाँचा"]
    NEXT = "एकाइ ४  ·  व्यावसायिक पत्र"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ helpers
    def traveller(self, h=2.0):
        m = C.man(h, coat="#8A5A3A", shirt="#E8E0C8", topi=True)
        body = m[2]
        body.stretch(1.35, 0)
        return m

    def angry_mountain(self, w=9.0, h=5.2, base=-3.25):
        L, R, P = np.array([-w / 2, base, 0]), np.array([w / 2, base, 0]), np.array([0, base + h, 0])
        body = Polygon(L, [-w * 0.28, base + h * 0.62, 0], [-w * 0.12, base + h * 0.9, 0], P, [w * 0.14, base + h * 0.88, 0],
                       [w * 0.3, base + h * 0.6, 0], R, stroke_width=0, fill_color="#4A4038", fill_opacity=1)
        sn = []
        for t in np.linspace(0, 1, 11):
            x = -w * 0.2 + w * 0.4 * t
            y = base + h * (0.74 + 0.05 * np.sin(t * 9))
            sn.append([x, y, 0])
        snow = Polygon([-w * 0.12, base + h * 0.9, 0], P, [w * 0.14, base + h * 0.88, 0], *sn[::-1], stroke_width=0,
                       fill_color=SNOW, fill_opacity=1)
        rng = np.random.default_rng(5)
        bristles = VGroup()
        for _ in range(55):
            yy = rng.uniform(base + 0.2, base + h * 0.62)
            half = (w / 2) * (1 - (yy - base) / h) * 0.92
            xx = rng.uniform(-half, half)
            if abs(xx) < 1.6 and base + h * 0.3 < yy < base + h * 0.62:
                continue
            tr = Triangle(stroke_width=0, fill_color="#1E2A1E", fill_opacity=1).stretch_to_fit_width(0.22).stretch_to_fit_height(rng.uniform(0.35, 0.6))
            bristles.add(tr.move_to([xx, yy, 0]).rotate(rng.uniform(-0.3, 0.3)))
        cy = base + h * 0.5
        eyes = VGroup()
        for s_ in (-1, 1):
            e = Ellipse(width=0.85, height=0.5, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to([s_ * 0.85, cy, 0])
            p = Dot([s_ * 0.8, cy - 0.03, 0], radius=0.13, color=BLACK)
            eyes.add(VGroup(e, p))
        brows = VGroup(Line([-1.35, cy + 0.55, 0], [-0.35, cy + 0.25, 0], color="#1A1410", stroke_width=14),
                       Line([1.35, cy + 0.55, 0], [0.35, cy + 0.25, 0], color="#1A1410", stroke_width=14))
        mouth = ArcBetweenPoints([-0.6, cy - 0.85, 0], [0.6, cy - 0.85, 0], angle=-1.4).set_stroke("#1A1410", 10)
        g = VGroup(body, bristles, snow, eyes, brows, mouth)
        g.face = VGroup(eyes, brows, mouth)
        g.snow, g.bristles, g.brows = snow, bristles, brows
        return g

    def ktag(self, i, name, color):
        t = VGroup(C.badge(self, i, color, r=0.24), T(name, size=24, color=color, weight="SEMIBOLD")).arrange(RIGHT, buff=0.2)
        return t.to_corner(UR, buff=0.45).shift(DOWN * 0.05)

    def front(self):
        if self.hud is not None:
            self.bring_to_front(self.hud)

    def snowfall(self, n=40, seed=3, y0=3.4):
        rng = np.random.default_rng(seed)
        return VGroup(*[Dot([rng.uniform(-6.8, 6.8), rng.uniform(-3.0, y0), 0], radius=rng.uniform(0.02, 0.05), color=WHITE,
                            fill_opacity=rng.uniform(0.5, 0.95)) for _ in range(n)])

    def nepal(self):
        pts = [(-6.0, 1.3), (-5.2, 2.0), (-4.2, 1.9), (-3.0, 1.4), (-1.5, 1.0), (0.0, 0.7), (1.5, 0.4), (3.0, 0.3), (4.2, 0.1),
               (5.4, 0.3), (5.9, -0.1), (5.8, -0.9), (4.5, -1.1), (3.0, -1.2), (1.5, -1.0), (0.0, -0.8), (-1.5, -0.4),
               (-3.0, 0.0), (-4.5, 0.3), (-5.6, 0.5), (-6.2, 0.8)]
        return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=MINT, stroke_width=3, fill_color=MINT, fill_opacity=0.1)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        sk = C.sky("#121a3a", "#3a3a6a")
        mt = self.angry_mountain()
        tr = self.traveller(1.5).move_to([-5.6, -3.25, 0], aligned_edge=DOWN)
        self.add(sk)
        with self.say("सुदूरपश्चिमको एउटा पहाड। टाउकामा चिप्लो बरफको सेतो केश फुलाएको, अररो बुढो शरीरमा काला रुखका जिङ्ग्रिङे भुत्ला ठड्याएको।"):
            self.play(FadeIn(sk), run_time=0.6)
            self.play(FadeIn(mt[0], shift=UP * 0.4), run_time=1.0)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in mt.bristles], lag_ratio=0.02), run_time=1.5)
            self.play(FadeIn(mt.snow, shift=DOWN * 0.2), run_time=0.8)
        with self.say("र यो पहाड, मान्छेसित रिसाएको छ। गजधुम्म परेर बसेको छ। यसको नाम हो, घनघस्या।"):
            self.play(FadeIn(mt.face, scale=0.8), run_time=0.8)
            self.sfx("thud", gain=-8)
            self.play(mt.brows.animate.shift(DOWN * 0.15), run_time=0.4)
            self.play(Wiggle(mt.face, scale_value=1.05), run_time=1.0)
        q = C.kline("टोपी खस्ने उकालो", size=50, color=GOLD).move_to([-4.0, 2.75, 0])
        with self.say("यसको उकालो यति ठाडो छ, कि माथि हेर्दा टाउकाबाट टोपी नै खस्छ। अनि यही उकालो चढ्न आइपुगेका छन्, एक मोटा शरीरका लेखक, जसको उकालो देख्नेबित्तिकै सातोपुत्लो उड्छ।"):
            C.type_in(self, VGroup(q), run_time=1.2)
            self.play(FadeIn(tr, shift=RIGHT * 0.3), run_time=0.6)
            self.play(tr.animate.shift(RIGHT * 0.6), run_time=0.8)
            self.play(Rotate(tr[-1], 0.6, about_point=tr[-1].get_center()), tr[-1].animate.shift(LEFT * 0.4 + DOWN * 0.6), run_time=0.6)
        hook = C.kline("हाँस्दै हाँस्दै पहाड जित्ने कला", size=40, color=MINT).move_to([3.7, 2.75, 0])
        with self.say("उनी रुँदैनन्, गुनासो गर्दैनन्। हाँस्दै हाँस्दै पहाड जित्छन्। कसरी? चल्नुहोस्, आज हामी पनि उनीसँगै यो उकालो काट्छौँ।"):
            C.type_in(self, VGroup(hook), run_time=1.2)
        self.play(FadeOut(VGroup(sk, mt, tr, q, hook)), run_time=0.8)
        g, nb = self.title_card()
        with self.say("नमस्ते! कक्षा बाह्रको अनिवार्य नेपालीको एकाइ तीनमा स्वागत छ। आजको पाठ हो, तारानाथ शर्माको नियात्रा, घनघस्याको उकालो काट्ता।"):
            pass
        self.end_title(g, nb)
        self.roadmap("आजको बाटो। लेखक परिचय, नियात्रा विधा के हो, पाठको पृष्ठभूमि, यात्राको सार, खण्डगत व्याख्या, पात्र र मूल भाव, भाषाशैली र अलङ्कार, र अन्त्यमा परीक्षामा उत्तर लेख्ने ढाँचा।")

    # ------------------------------------------------------------------ part 1: author
    def p1(self):
        self.section(0)
        name = C.kline("तारानाथ शर्मा", size=64).move_to(UP * 1.5)
        orig = T("मूल थर: भण्डारी", size=26, color=th.MUTED).next_to(name, DOWN, buff=0.25)
        pills = VGroup(C.pill("नियात्रा विधाका स्थापक", GOLD, 28), C.pill("झर्रोवादी आन्दोलनका अगुवा", MINT, 28)).arrange(RIGHT, buff=0.35)
        pills2 = VGroup(*[C.pill(t, SKY, 24) for t in ("निबन्धकार", "समालोचक", "कथाकार", "पाठ्यपुस्तक लेखक")]).arrange(RIGHT, buff=0.3)
        VGroup(pills, pills2).arrange(DOWN, buff=0.3).next_to(orig, DOWN, buff=0.5)
        with self.say("तारानाथ शर्मा, जसको मूल थर भण्डारी हो, नेपाली साहित्यमा नियात्रा विधाका स्थापक र झर्रोवादी आन्दोलनका अगुवा हुन्। उनी निबन्धकार, समालोचक, कथाकार र पाठ्यपुस्तक लेखक पनि थिए।"):
            C.type_in(self, VGroup(name), run_time=1.0)
            self.play(FadeIn(orig), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pills], lag_ratio=0.3), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pills2], lag_ratio=0.2), run_time=1.2)
        self.play(FadeOut(VGroup(name, orig, pills, pills2)), run_time=0.5)
        steps = VGroup(*[C.card(a, b, c, w=3.6, h=1.7, hsize=30, bsize=24) for a, b, c in
                         (("स्नातक", "बनारस", SKY), ("स्नातकोत्तर", "पटना", MINT), ("विद्यावारिधि", "भाषाविज्ञान · विस्कन्सिन विश्वविद्यालय, अमेरिका", GOLD))])
        for i, s_ in enumerate(steps):
            s_.move_to([-4.2 + 4.2 * i, -1.2 + 1.1 * i, 0])
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.1, color=th.MUTED, stroke_width=4) for i in range(2)])
        with self.say("उनको शिक्षाको सिँढी हेरौँ। बनारसबाट स्नातक, पटनाबाट स्नातकोत्तर, र अमेरिकाको विस्कन्सिन विश्वविद्यालयबाट अङ्ग्रेजी भाषाविज्ञानमा विद्यावारिधि। जीवनको अन्तिम अवस्थासम्म उनी अध्यापनमै लागे।"):
            for i, s_ in enumerate(steps):
                self.play(FadeIn(s_, shift=UP * 0.3), run_time=0.5)
                if i < 2:
                    self.play(GrowArrow(arrows[i]), run_time=0.3)
        self.play(FadeOut(VGroup(steps, arrows)), run_time=0.5)
        head = C.heading("जीवनरेखा", color=self.color)
        self.play(FadeIn(head), run_time=0.4)
        tl = C.timeline(self, [
            (1991, "जन्म · बरबोटे, इलाम", "उनको जन्म विक्रम संवत् उन्नाइस सय एकानब्बे, असार नौ गते इलामको बरबोटेमा भयो।"),
            (2008, "पहिलो रचना 'इलाम' निबन्ध", "दुई हजार आठ सालमा दार्जिलिङको साथी साप्ताहिकमा छापिएको इलाम शीर्षकको निबन्ध उनको पहिलो रचना हो।"),
            (2013, "झर्रोवादी अभियान", "दुई हजार तेह्र सालतिर उनी झर्रोवादी अभियानका सहयोगी अगुवा बने।"),
            (2026, "'बेलाइततिर बरालिँदा' · मदन पुरस्कार", "दुई हजार छब्बीस सालमा बेलाइततिर बरालिँदा कृतिले मदन पुरस्कार पायो। निबन्ध सङ्ग्रहमा मदन पुरस्कार पाउने यो पहिलो कृति हो।"),
            (2029, "'सम र समका कृति' · साझा पुरस्कार", "दुई हजार उनन्तीसमा सम र समका कृति समालोचनाले साझा पुरस्कार पायो।"),
            (2039, "सर्वश्रेष्ठ पाठ्यपुस्तक लेखन पुरस्कार", "दुई हजार उनचालीसमा उनलाई सर्वश्रेष्ठ पाठ्यपुस्तक लेखन पुरस्कार मिल्यो।"),
            (2078, "निधन", "र दुई हजार अठहत्तर साल फागुन तीन गते उनको निधन भयो।"),
        ], y=-0.2, label_w=2.5, size=22)
        self.wait(0.4)
        self.play(FadeOut(VGroup(head, tl)), run_time=0.5)
        head = C.heading("प्रमुख कृति", color=self.color)
        works = [("बेलाइततिर बरालिँदा", "यात्रा निबन्ध · मदन पुरस्कार", GOLD), ("नमस्ते", "निबन्ध सङ्ग्रह", SKY),
                 ("घोत्ल्याइँहरू · सम र समका कृति", "समालोचना", MINT), ("नेपाली साहित्यको इतिहास", "साहित्यिक इतिहास", PINK),
                 ("पाताल प्रवास", "यात्रा निबन्ध", TEAL), ("मेरो कथा · ओझेल पर्दा · सुली", "उपन्यास", CORAL)]
        cards = VGroup(*[C.card(a, b, c, w=4.0, h=2.0, hsize=28, bsize=24) for a, b, c in works]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3))
        cards.next_to(head, DOWN, buff=0.45)
        with self.say("उनका प्रमुख कृति। बेलाइततिर बरालिँदा र पाताल प्रवास, यात्रा निबन्ध। नमस्ते, निबन्ध सङ्ग्रह। घोत्ल्याइँहरू र सम र समका कृति, समालोचना। नेपाली साहित्यको इतिहास। र मेरो कथा, ओझेल पर्दा र सुली जस्ता उपन्यास।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for c in cards:
                self.sfx("pop", gain=-15)
                self.play(FadeIn(c, shift=UP * 0.25, scale=0.9), run_time=0.45)
                self.hold(v.dur / 6 - 0.65)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        heavy = C.pill("कठिन, किताबी भाषा", th.MUTED, 30).move_to([-3.6, 0.6, 0])
        plain = C.pill("बोलीचालको सरल, ठेट नेपाली", MINT, 30).move_to([3.4, 0.6, 0])
        arr = Arrow(heavy.get_right(), plain.get_left(), buff=0.2, color=GOLD, stroke_width=6)
        lab = T("झर्रोवादी अभियान", size=30, color=GOLD, weight="BOLD").next_to(arr, UP, buff=0.3)
        note = para("यही असर 'घनघस्याको उकालो काट्ता' को भाषामा स्पष्ट देखिन्छ।", width=10, size=28, color=th.BODY, align="center").move_to([0, -1.4, 0])
        with self.say("झर्रोवादी अभियान के थियो? यसले नेपाली भाषालाई कठिन किताबी रूपबाट बोलीचालको सरल र ठेट स्वरूपमा ल्याउन खोज्यो। यही असर हाम्रो पाठको भाषामा स्पष्ट देखिन्छ।"):
            self.play(FadeIn(heavy), run_time=0.4)
            self.play(GrowArrow(arr), FadeIn(lab), run_time=0.7)
            self.play(FadeIn(plain, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(note), run_time=0.5)
        self.play(FadeOut(VGroup(heavy, plain, arr, lab, note)), run_time=0.5)

    # ------------------------------------------------------------------ part 2: genre
    def p2(self):
        self.section(1)
        bk = C.man(2.2, coat="#4A4A6A").move_to([-4.6, -3.1, 0], aligned_edge=DOWN)
        lb = T("बालकृष्ण पोखरेल", size=26, color=SKY, weight="BOLD").next_to(bk, UP, buff=0.25)
        book = VGroup(Rectangle(width=1.4, height=1.0, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                      Line(UP * 0.5, DOWN * 0.5, color=th.BG, stroke_width=3)).move_to([-2.6, -1.5, 0])
        bt = T("'मेनाइ साँघुको मेला'", size=24, color=GOLD).next_to(book, DOWN, buff=0.2)
        bub = C.bubble("तिमीले नियात्रा लेखेछौ !", size=34, tail=DOWN + LEFT).move_to([0.6, 1.4, 0])
        with self.say("नियात्रा भन्ने नाम कहाँबाट आयो? भाषाशास्त्री बालकृष्ण पोखरेलले तारानाथको मेनाइ साँघुको मेला पढेर भनेका थिए, तिमीले नियात्रा लेखेछौ।"):
            self.play(FadeIn(bk), FadeIn(lb), run_time=0.6)
            self.play(FadeIn(book, shift=UP * 0.2), FadeIn(bt), run_time=0.6)
            self.sfx("pop", gain=-12)
            self.play(FadeIn(bub, scale=0.8), run_time=0.5)
        why = para("किनभने त्यसमा यात्रा वर्णन मात्र होइन, लेखकका निजी कुरा पनि समेटिएका थिए।", width=5.5, size=26, color=th.INK).move_to([3.6, -1.2, 0])
        with self.say("किन? किनभने त्यसमा यात्राको वर्णन मात्र होइन, लेखकका निजी कुरा पनि समेटिएका थिए। र यही विधाको स्थापकका रूपमा तारानाथलाई मानिन्छ।"):
            self.play(FadeIn(why, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(bk, lb, book, bt, bub, why)), run_time=0.5)
        a = C.card("यात्रा वर्णन", "स्थान र घटना", SKY, w=3.4, h=1.8, hsize=32, bsize=26).move_to([-4.6, 0.6, 0])
        plus = T("+", size=72, color=th.INK, weight="BOLD").move_to([-2.4, 0.6, 0])
        b = VGroup(*[C.pill(t, GOLD, 24) for t in ("निजी अनुभूति", "विचार र कल्पना", "हास्यव्यङ्ग्य", "आत्मीयता")]).arrange(DOWN, buff=0.18).move_to([-0.2, 0.6, 0])
        eq = T("=", size=72, color=th.INK, weight="BOLD").move_to([2.0, 0.6, 0])
        c = VGroup(Circle(radius=1.25, fill_color=MINT, fill_opacity=0.2, stroke_color=MINT, stroke_width=4),
                   T("नियात्रा", size=40, color=MINT, weight="BOLD")).move_to([4.4, 0.6, 0])
        with self.say("नियात्रालाई एउटा जोडजस्तो सम्झनुहोस्। यात्राको वर्णन, अर्थात् स्थान र घटना। त्यसमा थपिन्छ, यात्रुको निजी अनुभूति, विचार र कल्पना, हास्यव्यङ्ग्य, र आत्मीयता। दुवै मिलेपछि बन्छ, नियात्रा।"):
            self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(plus), LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in b], lag_ratio=0.25), run_time=1.5)
            self.play(FadeIn(eq), GrowFromCenter(c), run_time=0.7)
        dfn = para("यात्राको वर्णनसँगै यात्रुको निजी अनुभूति, विचार, कल्पना, हास्यव्यङ्ग्य र आत्मीयता समेटिएको साहित्यिक गद्य रचनालाई नियात्रा भनिन्छ।",
                   width=11.5, size=26, color=th.BODY).move_to([0, -2.3, 0])
        with self.say("परिभाषा यस्तो लेख्नुहोस्। यात्राको वर्णनसँगै यात्रुको निजी अनुभूति, विचार, कल्पना, हास्यव्यङ्ग्य र आत्मीयता समेटिएको साहित्यिक गद्य रचनालाई नियात्रा भनिन्छ।"):
            self.play(FadeIn(dfn, shift=UP * 0.2), run_time=0.7)
        self.play(FadeOut(VGroup(a, plus, b, eq, c, dfn)), run_time=0.5)
        head = C.heading("कुन विधा, कस्तो पहिचान", color=self.color)
        rows = [("नियात्रा", "यात्रामा भोगिएको अनुभव र लेखकको मन", MINT), ("यात्रावृत्तान्त", "स्थान र घटना प्रधान", SKY),
                ("संस्मरण", "बितेको समयको स्मरण", PINK), ("निबन्ध", "विचार वा विषयको व्याख्या", GOLD)]
        grp = VGroup()
        for n_, d_, c_ in rows:
            grp.add(VGroup(C.pill(n_, c_, 30), T(d_, size=28, color=th.INK)).arrange(RIGHT, buff=0.5))
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.2)
        with self.say("यी चार विधा अलमल नगर्नुहोस्। नियात्रामा यात्रामा भोगिएको अनुभव र लेखकको मन प्रधान हुन्छ। यात्रावृत्तान्तमा स्थान र घटना प्रधान। संस्मरण बितेको समयको स्मरण हो, र निबन्ध कुनै विचार वा विषयको व्याख्या।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for g in grp:
                self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur / 4 - 0.7)
            self.play(Circumscribe(grp[0], color=MINT), run_time=1.0)
        self.play(FadeOut(VGroup(head, grp)), run_time=0.5)
        self.tip("'नियात्रा भनेको यात्रा वर्णन मात्र हो' भन्नु अधुरो हुन्छ। जुन लेखमा 'म' को मन यात्राभन्दा बढी बोल्छ, त्यो नियात्रा हो।",
                 "परीक्षा सुझाव। नियात्रा भनेको यात्रा वर्णन मात्र हो भनेर लेखे उत्तर अधुरो हुन्छ। सम्झनुहोस्, जुन लेखमा म को मन यात्राभन्दा बढी बोल्छ, त्यो नियात्रा हो।")
        self.quiz("नियात्राको मुख्य पहिचान कुन हो ?",
                  ["स्थान र घटनाको सूची मात्र", "यात्रासँगै लेखकको निजी अनुभूति र विचार", "काल्पनिक पात्र र कथानक", "छन्द र तुकको लय"], 1,
                  "अब एउटा प्रश्न। नियात्राको मुख्य पहिचान कुन हो? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ख। नियात्रामा यात्राको वर्णनसँगै लेखकको निजी अनुभूति, विचार र हास्य हुन्छ। क विकल्प यात्रावृत्तान्त जस्तो मात्र हो। ग कथा वा उपन्यासको गुण हो, र घ पद्य कविताको।")

    # ------------------------------------------------------------------ part 3: background
    def p3(self):
        self.section(2)
        np_ = self.nepal().shift(DOWN * 0.6)
        ilam = Dot([5.3, -1.1, 0], radius=0.12, color=GOLD)
        bait = Dot([-5.5, 0.4, 0], radius=0.12, color=CORAL)
        li = T("इलाम", size=26, color=GOLD, weight="BOLD").next_to(ilam, DOWN, buff=0.15)
        lbt = T("बैतडी", size=26, color=CORAL, weight="BOLD").next_to(bait, DOWN, buff=0.15)
        path = CurvedArrow(ilam.get_center() + UP * 0.2, bait.get_center() + RIGHT * 0.2, angle=0.5, color=th.INK, stroke_width=3)
        path = DashedVMobject(path, num_dashes=40)
        yr = C.pill(f"वि.सं. {self.num(2024)} पुसको अन्तिम हप्ता", SKY, 28).move_to([0, 2.7, 0])
        with self.say("यो यात्रा विक्रम संवत् दुई हजार चौबीस सालको पुसको अन्तिम हप्तामा भएको हो। लेखक मेची अञ्चलमा जन्मिएका इलामे हुन्, तर यसपटक नेपालको सुदूरपश्चिम भ्रमणमा निस्केका छन्।"):
            self.play(DrawBorderThenFill(np_), run_time=1.2)
            self.play(FadeIn(yr), FadeIn(ilam, scale=0.5), FadeIn(li), run_time=0.6)
            self.play(Create(path), run_time=1.5)
            self.play(FadeIn(bait, scale=0.5), FadeIn(lbt), Flash(bait, color=CORAL), run_time=0.6)
        with self.say("सुदूरपूर्वको इलामे शरीर बोकेर, उनी सुदूरपश्चिमको बैतडीबाट डँडेलधुरातर्फ हिँड्दैछन्। त्यो बेला यहाँ सडक थिएन। भरिया नै एकमात्र साधन थियो।"):
            self.play(Indicate(bait, color=CORAL, scale_factor=2), run_time=1.0)
        self.play(FadeOut(VGroup(np_, ilam, bait, li, lbt, path, yr)), run_time=0.5)
        hrt = C.heart(1.1, color=PINK).move_to([0, -0.2, 0])
        places = ["खप्तडमा वसन्त", "तुम्लिङमा हिउँ", "राजापुरको काँसे घारी", "तिल्केनीको उकालो", "घनघस्याको उकालो", "चन्दनीको उकालो"]
        ps = VGroup()
        for i, t_ in enumerate(places):
            a_ = PI / 2 + i * TAU / 6 + PI / 6
            ps.add(C.pill(t_, [GOLD, SKY, MINT, CORAL, PINK, TEAL][i], 26).move_to([np.cos(a_) * 4.4, -0.2 + np.sin(a_) * 2.2, 0]))
        q = C.kline("म नेपाललाई माया गर्ने राष्ट्रवादी मान्छे हुँ", size=36, color=th.INK, hl={"राष्ट्रवादी": GOLD}).to_edge(UP, buff=0.75)
        with self.say("लेखको सुरुमै लेखक आफ्नो राष्ट्रप्रेम जनाउँछन्। उनी खप्तडमा वसन्त बिताउन, तुम्लिङमा हिउँ खेल्न र राजापुरको काँसे घारीमा झ्याउरे गाउन चाहन्छन्। तिल्केनी, घनघस्या र चन्दनीका उकालालाई उत्तिकै माया गर्छन्।") as v:
            self.play(FadeIn(hrt, scale=0.5), run_time=0.5)
            for p in ps:
                self.play(FadeIn(p, scale=0.8), run_time=0.4)
                self.hold(v.dur / 6 - 0.55)
        with self.say("उनी भन्छन्, म नेपाललाई माया गर्ने राष्ट्रवादी मान्छे हुँ। नेपालको हरेक भाग उनको मुटुमा उत्तिकै छ।"):
            C.type_in(self, VGroup(q), run_time=1.5)
            for _ in range(2):
                self.play(hrt.animate.scale(1.15), run_time=0.3)
                self.play(hrt.animate.scale(1 / 1.15), run_time=0.3)
        self.play(FadeOut(VGroup(hrt, ps, q)), run_time=0.5)
        C.show_quote(self, ["प्रकृतिसित जुध्नु नै जीवनको रमाइलो हो"],
                     "र यो कठिन यात्रा किन? लेखक भन्छन्, प्रकृतिसित जुध्नु नै जीवनको रमाइलो हो, भन्ने भावलाई ह्याकुलाले छोपेर म सुदूरपश्चिमको भ्रमणमा निस्केको थिएँ। उनका लागि कठिनाइ नै यात्राको रमाइलो हो।",
                     color=GOLD, size=46, hl={"जुध्नु": CORAL, "रमाइलो": MINT})

    # ------------------------------------------------------------------ part 4: journey profile
    def p4(self):
        self.section(3)
        st = [("शाहीलेक, बैतडी", -5.9, 0.0), ("सतबाँझको लेक", -3.9, 1.6), ("पाटन", -1.9, -0.7), ("अघोरी गाड", 0.0, -2.0),
              ("घनघस्याको उकालो", 1.6, 0.2), ("धुरा", 3.4, 1.9), ("पोखरा", 5.6, 0.2)]
        pts = [np.array([x, y, 0]) for _, x, y in st]
        prof = VMobject(stroke_color="#B89A6A", stroke_width=6)
        prof.set_points_smoothly(pts)
        land = VMobject(stroke_width=0, fill_color="#2E3A2E", fill_opacity=1)
        samples = [prof.point_from_proportion(t) for t in np.linspace(0, 1, 120)]
        land.set_points_as_corners([np.array([-5.9, -3.25, 0])] + samples + [np.array([5.6, -3.25, 0]), np.array([-5.9, -3.25, 0])])
        caps = VGroup()
        for i in (1, 5):
            p = pts[i]
            caps.add(Polygon(p + LEFT * 0.75 + DOWN * 0.35, p + UP * 0.04, p + RIGHT * 0.75 + DOWN * 0.35, stroke_width=0, fill_color=SNOW, fill_opacity=0.95))
        props = []
        for p in pts:
            props.append(float(np.linspace(0, 1, 120)[int(np.argmin([np.linalg.norm(q - p) for q in samples]))]))
        dots, labs = VGroup(), VGroup()
        for i, (n_, x, y) in enumerate(st):
            d = Dot(pts[i], radius=0.11, color=WHITE)
            lab = para(n_, width=2.2, size=23, color=th.INK, align="center")
            lab.next_to(d, DOWN, buff=0.45)
            if i == 0:
                lab.shift(RIGHT * 0.5)
            if i == 6:
                lab.shift(LEFT * 0.4)
            dots.add(d)
            labs.add(lab)
        head = C.heading("उकाला-ओरालोको रेखाचित्र", color=self.color, size=34).shift(UP * 0.1)
        walker = self.traveller(0.7)
        walker.move_to(pts[0], aligned_edge=DOWN)
        with self.say("यात्रालाई एउटा उकाला ओरालोको रेखाचित्रमा हेरौँ। बैतडीको शाहीलेकबाट सुरु, सतबाँझको लेक, पाटन, अघोरी गाड, घनघस्याको उकालो, धुरा, र पोखरा।") as v:
            self.play(FadeIn(head), run_time=0.4)
            self.play(Create(prof), FadeIn(land), run_time=1.6)
            self.play(FadeIn(caps), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labs], lag_ratio=0.15), FadeIn(walker), run_time=1.5)
        self.front()
        legs = [
            (0, None, "बैतडीको शाहीलेकमा विद्यालय भवनमा दुई रात बसे, तर भरिया पाइएन। सहायक अञ्चलाधीश यमुनाराज पौड्यालले सत्र सत्र रुपियाँमा पाटनसम्म भारी बोक्ने दुई जना मिलाइदिए। दिउँसो एघार बजे, दशरथ चन्दको सालिकमा श्रद्धाका दुई थोपा आँसु चढाएर उनीहरू हिँडे।", f"दिउँसो {self.num(11)} बजे"),
            (1, 0, "सतबाँझको बाटोमा मन्दिर, फलामे साङ्लीको पिङ, पसल, भेडाका बथान, र विरहको गीत गाउने गोठाला भेटिए। धेरै माथि पुग्दा हिउँ भेटियो, र लेखकले साथी प्रेमबहादुर प्रधानसँग हिउँमा चिप्ली खेले।", None),
            (2, 1, "ओरालो झरेर पाटन पुगेपछि घरेलु विभाग र स्वास्थ्य केन्द्रका कर्मचारीले उनीहरूलाई डेरामा दालभात खुवाएर राखे। भोलिपल्ट भरिया डँडेलधुरा जान मानेनन्। प्रधानपञ्चको मद्दतले दुई जना पाइए, र दिउँसो बाह्र बजे हिँडे।", f"भोलिपल्ट दिउँसो {self.num(12)} बजे"),
            (3, 2, "दुई बजे अघोरी गाडको साँघु तरेपछि सुरु भयो, टोपी खस्ने उकालो।", f"दिउँसो {self.num(2)} बजे"),
            (4, 3, "घनघस्याको उकालो सबैभन्दा कठिन खण्ड हो। चुच्चे ढुङ्गा, पहरा, र पानी नपाइने बाटो। लेखक हास्यका साथ आफ्ना कष्ट सुनाउँछन्। निकै माथि दुई पानीको कुलो भेट्दा, उनलाई स्वर्ग पुगेजस्तो लाग्यो।", None),
            (5, 4, "भरिया रामसिंह र उसको भतिजो खाली खुट्टा हिउँमा उकालिए। लेखक चिप्लिँदै उनीहरूसँगै पाँच बजे धुरा पुगे। तीन माइलजति बाटो जमेको हिउँले ढाकिएको थियो, र साथीहरू कुइरो र भिरतिर बाटो हराए।", f"साँझ {self.num(5)} बजे"),
            (6, 5, "छिटो हिँड्ने तीन जना पोखरा पुगेर बास खोज्ने निर्णय भयो। बाटोमा खड्किनीले मकै भुटिदिइन्। राति बाह्र बजे पसल बन्द थियो, बुढाले बास दिएनन्। सुन्तला खाएर, दाउरा किनेर आगो ताप्दै उनीहरू साथी पर्खिरहे। राति दुई बजे भरिया र साथी आइपुगे, र सबै ढुङ्गाको सिरानी लगाएर सुते।", f"राति {self.num(12)} बजे  ·  {self.num(2)} बजे"),
        ]
        clock_m = None
        for i, prev, narr, ck in legs:
            with self.say(narr):
                if prev is not None:
                    a0, a1 = props[prev], props[i]
                    self.play(UpdateFromAlphaFunc(walker, lambda m, a, a0=a0, a1=a1: m.move_to(prof.point_from_proportion(a0 + (a1 - a0) * a), aligned_edge=DOWN)),
                              run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
                self.play(Flash(dots[i], color=GOLD, flash_radius=0.35), labs[i].animate.set_color(GOLD), run_time=0.5)
                if ck:
                    new = C.pill(ck, SKY, 26).to_corner(DL, buff=0.6).shift(UP * 0.1)
                    if clock_m is None:
                        self.play(FadeIn(new, shift=UP * 0.2), run_time=0.4)
                    else:
                        self.play(FadeOut(clock_m), FadeIn(new, shift=UP * 0.2), run_time=0.4)
                    clock_m = new
        self.play(FadeOut(VGroup(head, prof, land, caps, dots, labs, walker, *( [clock_m] if clock_m else []))), run_time=0.6)
        self.quiz("घनघस्याको उकालो कहाँबाट सुरु हुन्छ ?",
                  ["पाटनबाट", "सतबाँझको लेकबाट", "अघोरी गाडको साँघु तरेपछि", "पोखराबाट"], 2,
                  "एक अङ्कको प्रश्न। घनघस्याको उकालो कहाँबाट सुरु हुन्छ? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ग, अघोरी गाडको साँघु तरेपछि। पाटनबाट त उनीहरू हिँडेका मात्र हुन्, पाटनदेखि अघोरी गाडसम्म ओरालो र तेर्सो बाटो छ। सतबाँझ त अघिल्लो दिनको लेक हो, र पोखरा उकालो काटेपछिको बास।")

    # ------------------------------------------------------------------ part 5: sections
    def p5(self):
        self.section(4)
        self.k1()
        self.k2()
        self.k3()
        self.k4()

    def k1(self):
        tag = self.ktag(1, "घनघस्याको मानवीकरण", CORAL)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["टाउकामा चिप्लो न चिप्लो बरफको केश फुलाएर", "अररो वृद्ध शरीरमा काला रुखका जिङ्ग्रिङे भुत्ला ठड्याई", "यो घनघस्या गजधुम्म परेर बसेको छ"],
                         "पहिलो खण्डमा कविता जस्तै सुन्दर एउटा वाक्य छ। टाउकामा चिप्लो न चिप्लो बरफको केश फुलाएर, आफ्नो अररो वृद्ध शरीरमा काला रुखका जिङ्ग्रिङे भुत्ला ठड्याई, यो घनघस्या गजधुम्म परेर बसेको छ।",
                         color=CORAL, size=34, where=UP * 1.6, keep=True, hl={"बरफको": SKY, "केश": SKY, "रुखका": MINT, "भुत्ला": MINT, "गजधुम्म": CORAL})
        self.play(q.animate.scale(0.62).to_corner(UL, buff=0.6).shift(DOWN * 0.35), run_time=0.6)
        mt = self.angry_mountain(w=6.5, h=4.0).shift(RIGHT * 2.6)
        self.play(FadeIn(mt[0]), FadeIn(mt.bristles), FadeIn(mt.snow), run_time=0.8)
        rows = VGroup(
            VGroup(T("बरफ", size=30, color=SKY, weight="BOLD"), Arrow(LEFT * 0.4, RIGHT * 0.4, color=th.MUTED, buff=0), T("फुलेको केश", size=30, color=th.INK)).arrange(RIGHT, buff=0.25),
            VGroup(T("काला रुख", size=30, color=MINT, weight="BOLD"), Arrow(LEFT * 0.4, RIGHT * 0.4, color=th.MUTED, buff=0), T("जिङ्ग्रिङे भुत्ला", size=30, color=th.INK)).arrange(RIGHT, buff=0.25),
            VGroup(T("उकालो", size=30, color=CORAL, weight="BOLD"), Arrow(LEFT * 0.4, RIGHT * 0.4, color=th.MUTED, buff=0), T("रिसाएको वृद्ध", size=30, color=th.INK)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.7, -1.3, 0])
        with self.say("यहाँ निर्जीव उकालोलाई जीवित बुढो मान्छेको रूप दिइएको छ। बरफ बन्यो, फुलेको सेतो केश।"):
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), Indicate(mt.snow, color=SKY, scale_factor=1.05), run_time=1.0)
        with self.say("काला रुख बने, जिङ्ग्रिङे भुत्ला।"):
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), Indicate(mt.bristles, color=MINT, scale_factor=1.02), run_time=1.0)
        with self.say("र पूरै पहाड बन्यो, गजधुम्म परेर बसेको एक रिसाहा वृद्ध। यो मान्छेसित रिसाएको छ भन्दा त उसमा रिसको भावना नै आरोप गरिएको छ। यसैलाई मानवीकरण भनिन्छ।"):
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2), FadeIn(mt.face, scale=0.8), run_time=1.0)
            self.play(mt.brows.animate.shift(DOWN * 0.12), run_time=0.4)
        self.play(FadeOut(VGroup(q, mt, rows)), run_time=0.5)
        self.venn()
        self.quiz("घनघस्याको मानवीकरणमा 'बरफ' लाई के बनाइएको छ ?",
                  ["फुलेको केश", "जिङ्ग्रिङे भुत्ला", "रिसाएको आँखा", "सेतो लुगा"], 0,
                  "मानवीकरणको प्रश्न। घनघस्याको चित्रणमा बरफलाई के बनाइएको छ? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर क, फुलेको केश। टाउकामा बरफको केश फुलाएर भनिएको छ। ख विकल्प, जिङ्ग्रिङे भुत्ला त काला रुख हुन्। बुढो मान्छेको सेतो केश जस्तै, पहाडको टुप्पोको हिउँ।")
        self.play(FadeOut(tag), run_time=0.3)

    def venn(self):
        head = C.heading("सेती नदी र घनघस्या", color=self.color)
        a = Circle(radius=2.2, fill_color=SKY, fill_opacity=0.15, stroke_color=SKY, stroke_width=4).move_to([-1.5, -0.4, 0])
        b = Circle(radius=2.2, fill_color=CORAL, fill_opacity=0.15, stroke_color=CORAL, stroke_width=4).move_to([1.5, -0.4, 0])
        la = T("सेती", size=34, color=SKY, weight="BOLD").move_to([-2.4, 1.15, 0])
        lb = T("घनघस्या", size=34, color=CORAL, weight="BOLD").move_to([2.4, 1.15, 0])
        ta = para("पृथ्वीको पेटमा भासिँदै जान्छ", width=1.9, size=24, color=th.INK, align="center").move_to([-2.5, -0.5, 0])
        tb = para("ठडिएको ठडियै, झन् दृढ हुँदै", width=1.9, size=24, color=th.INK, align="center").move_to([2.5, -0.5, 0])
        tm = para("दुवै रिसाएका", width=1.2, size=26, color=GOLD, align="center").move_to([0, -0.4, 0])
        with self.say("पाठमा सेती नदी र घनघस्याको तुलना पनि छ, जुन परीक्षामा सोधिन्छ। समानता, दुवै रिसाएका छन्।"):
            self.play(FadeIn(head), run_time=0.3)
            self.play(Create(a), Create(b), FadeIn(la), FadeIn(lb), run_time=1.0)
            self.play(FadeIn(tm, scale=0.8), run_time=0.5)
        with self.say("तर भिन्नता के छ भने, सेती नदी पृथ्वीको पेटमा भासिँदै जान्छे, जबकि घनघस्या ठडिएको ठडियै छ, र झन् झन् दृढ हुँदै गइरहेको छ।"):
            self.play(FadeIn(ta, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(tb, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(tb, color=CORAL), run_time=0.8)
        self.play(FadeOut(VGroup(head, a, b, la, lb, ta, tb, tm)), run_time=0.5)

    def k2(self):
        tag = self.ktag(2, "सतबाँझको हिउँ", SKY)
        sk = C.sky("#1A2550", "#5A6A9A")
        hill = Polygon([-7.2, -3.3, 0], [-7.2, -1.0, 0], [-2.0, 0.4, 0], [3.0, -0.6, 0], [7.2, -1.6, 0], [7.2, -3.3, 0], stroke_width=0, fill_color=SNOW, fill_opacity=1)
        fall = self.snowfall(60, seed=4)
        a = self.traveller(1.3).move_to([-3.6, 0.1, 0], aligned_edge=DOWN)
        b = C.man(1.3, coat="#3E6A8A", topi=True).move_to([-2.6, 0.35, 0], aligned_edge=DOWN)
        self.add(sk)
        self.front()
        with self.say("दोस्रो खण्ड। सतबाँझको लेकमा धेरै माथि पुग्दा हिउँ भेटियो। लेखक र साथी प्रेमबहादुर प्रधान बच्चा जस्तै हिउँमा चिप्ली खेल्न थाले, र हिउँमा आकृति बनाए।"):
            self.play(FadeIn(sk), FadeIn(hill), FadeIn(tag), FadeIn(fall), run_time=0.8)
            self.front()
            self.play(FadeIn(a), FadeIn(b), run_time=0.5)
            self.play(a.animate.move_to([1.5, -0.9, 0], aligned_edge=DOWN).rotate(-0.3), b.animate.move_to([2.6, -1.3, 0], aligned_edge=DOWN).rotate(-0.3),
                      fall.animate.shift(DOWN * 0.6), run_time=2.0, rate_func=rate_functions.ease_in_quad)
        q = C.kblock(["यो हिउँ मेरो थियो, मेरो मुटुको थियो", "र हिमाली हार्दिकता बोकेको र चम्किलो थियो"], size=36, hl={"मेरो": GOLD, "मुटुको": PINK, "हार्दिकता": MINT}).move_to([0, 2.0, 0])
        bg = BackgroundRectangle(q, color=th.BG, fill_opacity=0.75, buff=0.25)
        with self.say("लेखकले बेलायतमा पनि हिउँ देखेका थिए। तर सतबाँझको हिउँबारे उनी भन्छन्, यो हिउँ मेरो थियो, मेरो मुटुको थियो, र हिमाली हार्दिकता बोकेको र चम्किलो थियो।"):
            self.play(FadeIn(bg), run_time=0.3)
            C.type_in(self, q, run_time=3.0)
        self.play(FadeOut(VGroup(sk, hill, fall, a, b, q, bg)), run_time=0.5)
        l = C.card("बेलायतको हिउँ", "बाहिरी अनुभव मात्र", th.MUTED, w=4.2, h=2.0, hsize=32, bsize=26).move_to([-3.4, 0.4, 0])
        r = C.card("सतबाँझको हिउँ", "मुटुसँग जोडिएको, आफ्नो", PINK, w=4.2, h=2.0, hsize=32, bsize=26).move_to([3.4, 0.4, 0])
        vs = T("तर", size=40, color=GOLD, weight="BOLD").move_to([0, 0.4, 0])
        res = C.pill("'मेरो' शब्द: स्वदेशप्रेमको स्वामित्वभाव", GOLD, 28).move_to([0, -1.6, 0])
        life = C.pill("बोध: जीवन एउटा नटुङ्गिने यात्रा रहेछ", MINT, 28).move_to([0, -2.5, 0])
        with self.say("विदेशी हिउँ बाहिरी अनुभव मात्र थियो। आफ्नै देशको हिमाली हिउँ भने मुटुसँग जोडिएको छ। मेरो भन्ने शब्दले स्वदेशप्रेमको स्वामित्वभाव देखाउँछ। र हिउँ खेलिसकेपछि लेखकले बोध गरे, जीवन एउटा नटुङ्गिने यात्रा रहेछ।"):
            self.play(FadeIn(l, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(vs), FadeIn(r, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(res, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(life, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(l, r, vs, res, life, tag)), run_time=0.5)

    def k3(self):
        tag = self.ktag(3, "उकालोमा हास्य", GOLD)
        self.play(FadeIn(tag), run_time=0.3)
        q = C.show_quote(self, ["मेरो शरीर अलिक मोटो भएकाले", "उकालो देख्नेबित्तिकै सातोपुत्लो उड्छ"],
                         "तेस्रो खण्ड हास्यले भरिएको छ। लेखक भन्छन्, मेरो शरीर अलिक मोटो भएकाले उकालो देख्नेबित्तिकै सातोपुत्लो उड्छ। उनलाई उकालो जेमराज, अर्थात् यमराज जत्तिकै डरलाग्दो लाग्छ।",
                         color=GOLD, size=40, where=UP * 0.3, hl={"मोटो": GOLD, "सातोपुत्लो": CORAL})
        head = C.heading("अलकत्रे बाटोलाई किन सराप्ने ?", color=self.color, size=36)
        road = VGroup(Rectangle(width=5.0, height=0.8, stroke_width=0, fill_color="#2A2A2E", fill_opacity=1),
                      DashedLine(LEFT * 2.3, RIGHT * 2.3, color=WHITE, stroke_width=3)).move_to([-3.4, 0.4, 0])
        rl = VGroup(T("कालोपत्रे बाटो", size=28, color=th.INK, weight="BOLD"), T("जोगबनी–धरान · भक्तपुर–बाह्रबिसे", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(road, DOWN, buff=0.3)
        rocks = VGroup(*[Polygon([x - 0.2, y, 0], [x, y + 0.3, 0], [x + 0.2, y, 0], stroke_width=0, fill_color="#7A7A6A", fill_opacity=1)
                         for x, y in zip(np.linspace(1.4, 5.4, 9), np.linspace(-0.9, 1.6, 9))])
        slope = Line([1.2, -1.0, 0], [5.6, 1.6, 0], color="#8A6A4A", stroke_width=10)
        sl = VGroup(T("घनघस्याको उकालो", size=28, color=CORAL, weight="BOLD"), T("चुच्चे ढुङ्गा · पहरा · पानी छैन", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([3.4, -1.9, 0])
        with self.say("अनि हेर्नुहोस्, उनी के गर्छन्। घनघस्याको चुच्चे ढुङ्गा र पानी नपाइने उकालोमा थाकेपछि, उनलाई जोगबनीदेखि धरान र भक्तपुरदेखि बाह्रबिसेसम्मका सजिला कालोपत्रे बाटा सम्झना आउँछन्।"):
            self.play(FadeIn(head), run_time=0.3)
            self.play(FadeIn(road), FadeIn(rl), run_time=0.6)
            self.play(Create(slope), LaggedStart(*[FadeIn(r_, scale=0.5) for r_ in rocks], lag_ratio=0.1), FadeIn(sl), run_time=1.5)
        joke = C.pill("सजिलो बाटोलाई धिक्कार्ने र सराप्ने: हास्यको उल्टो भाव", MINT, 28).move_to([0, 2.2, 0])
        with self.say("र ती सजिला बाटालाई धिक्कार्दै, सराप्दै कन्छन्। जुन बाटोले कुनै दुःख दिएन, त्यसैलाई सराप्नु! यो हास्यको मीठो उल्टो भाव हो।"):
            self.play(FadeIn(joke, scale=0.8), Wiggle(road), run_time=1.2)
        self.play(FadeOut(VGroup(head, road, rl, rocks, slope, sl, joke)), run_time=0.5)
        head = C.heading("निल आर्मस्ट्रङसँग तुलना", color=self.color, size=36)
        mn = C.moon(0.9).move_to([-3.6, 0.9, 0])
        helm = VGroup(Circle(radius=0.32, fill_color=WHITE, fill_opacity=1, stroke_width=0), Circle(radius=0.2, fill_color="#3A4A7A", fill_opacity=1, stroke_width=0).shift(RIGHT * 0.05))
        astro = VGroup(RoundedRectangle(corner_radius=0.15, width=0.7, height=0.9, fill_color=WHITE, fill_opacity=1, stroke_width=0), helm.shift(UP * 0.62)).move_to([-3.6, -1.0, 0])
        tools = VGroup(*[C.pill(t, SKY, 22) for t in ("अक्सिजन", "यन्त्र", "खाना र पानी")]).arrange(DOWN, buff=0.15).next_to(astro, RIGHT, buff=0.4)
        trv = self.traveller(1.6).move_to([3.0, -2.2, 0], aligned_edge=DOWN)
        drop = VGroup(C.flame(0.6, color=SKY, inner="#BFE3FF").move_to([4.6, -0.3, 0]))
        cross = Line([4.2, -0.7, 0], [5.0, 0.1, 0], color=CORAL, stroke_width=6)
        l1 = T("यथेष्ट वैज्ञानिक उपकरण", size=26, color=SKY).move_to([-3.4, -2.6, 0])
        l2 = T("पानीसमेत छैन, फिटफिटी", size=26, color=CORAL).move_to([3.6, -2.75, 0])
        with self.say("अर्को रमाइलो तुलना। लेखक भन्छन्, चन्द्रमामा पुग्दा निल आर्मस्ट्रङहरूलाई त्यति फिटफिटी परेन होला, किनभने उनीहरूसँग यथेष्ट वैज्ञानिक उपकरण थिए।"):
            self.play(FadeIn(head), FadeIn(mn), run_time=0.5)
            self.play(FadeIn(astro, shift=DOWN * 0.3), LaggedStart(*[FadeIn(t_) for t_ in tools], lag_ratio=0.3), FadeIn(l1), run_time=1.5)
        with self.say("तर घनघस्या चढ्ने यी यात्रीसँग न कुनै साधन, न पानी। चन्द्रयात्रा भन्दा घनघस्याको उकालो गाह्रो! यो अतिशयोक्तिपूर्ण हास्य हो।"):
            self.play(FadeIn(trv), FadeIn(drop), run_time=0.5)
            self.play(Create(cross), FadeIn(l2), run_time=0.6)
            self.play(Wiggle(trv), run_time=0.8)
        self.play(FadeOut(VGroup(head, mn, astro, tools, trv, drop, cross, l1, l2)), run_time=0.5)
        q = C.show_quote(self, ["मरुभूमिका यात्रीले एक्कासि मरुद्यान भेटे झैँ", "हामी फुलेल भयौँ"],
                         "अनि निकै माथि पुगेपछि, दुई पानीको कुलो भेटियो। लेखक लेख्छन्, मरुभूमिका यात्रीले एक्कासि मरुद्यान भेटे झैँ हामी फुलेल भयौँ। उनलाई स्वर्ग पुगेजस्तो लाग्यो।",
                         color=MINT, size=40, where=UP * 1.6, keep=True, hl={"मरुद्यान": MINT, "फुलेल": GOLD})
        sand = Rectangle(width=6.0, height=1.4, stroke_width=0, fill_color="#C9A46A", fill_opacity=1).move_to([-3.0, -2.4, 0])
        palm = VGroup(Line([-3.0, -1.7, 0], [-2.9, 0.0, 0], color="#8A6A4A", stroke_width=8),
                      *[C.leaf(0.45).rotate(a_).move_to([-2.9 + 0.45 * np.cos(a_), 0.05 + 0.25 * np.sin(a_), 0]) for a_ in (0.3, 1.2, 2.0, 2.9)])
        pool = Ellipse(width=1.8, height=0.4, stroke_width=0, fill_color=SKY, fill_opacity=1).move_to([-2.2, -1.85, 0])
        kulo = VGroup(*[Line([1.2, y, 0], [5.6, y - 0.4, 0], color=SKY, stroke_width=8) for y in (-1.2, -2.0)])
        lab = C.pill("उपमा: 'झैँ'", GOLD, 26).move_to([3.4, -0.3, 0])
        with self.say("मरुभूमिमा भेटिने हरियाली र पानी भएको ठाउँलाई मरुद्यान भनिन्छ। तिर्खाएका यात्रीलाई पानीको कुलो त्यस्तै लाग्यो। झैँ ले तुलना गरेकाले यो उपमा अलङ्कार हो।"):
            self.play(FadeIn(sand), FadeIn(palm), FadeIn(pool), run_time=0.8)
            self.play(LaggedStart(*[Create(k_) for k_ in kulo], lag_ratio=0.3), run_time=1.0)
            self.play(FadeIn(lab), run_time=0.4)
        self.play(FadeOut(VGroup(q, sand, palm, pool, kulo, lab, tag)), run_time=0.5)

    def k4(self):
        tag = self.ktag(4, "धुरा र पोखराको रात", SKY)
        nt = VGroup(C.sky("#070A1C", "#141834"), C.stars(60, seed=12))
        snowg = Polygon([-7.2, -3.3, 0], [-7.2, -1.6, 0], [0, -1.2, 0], [7.2, -1.8, 0], [7.2, -3.3, 0], stroke_width=0, fill_color=SNOW, fill_opacity=0.9)
        p1 = C.man(1.3, coat="#6A5A4A", shirt="#C8B89A").move_to([-4.5, -1.9, 0], aligned_edge=DOWN)
        p2 = C.man(1.1, coat="#5A4A3A", shirt="#C8B89A").move_to([-3.5, -1.85, 0], aligned_edge=DOWN)
        loads = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.55, stroke_width=0, fill_color="#8A6A3A", fill_opacity=1).next_to(p, LEFT, buff=-0.15).shift(UP * 0.35) for p in (p1, p2)])
        feet = C.pill("खाली खुट्टा हिउँमा", CORAL, 26).move_to([0, 0.8, 0])
        self.add(nt)
        with self.say("चौथो खण्डमा भरियाहरूको सहनशीलता देखिन्छ। रामसिंह र उसको भतिजो, भारी बोकेर, खाली खुट्टा हिउँमा उकालिए। लेखक चिप्लिँदै उनीहरूको पछि पछि।"):
            self.play(FadeIn(nt), FadeIn(snowg), FadeIn(tag), run_time=0.6)
            self.front()
            self.play(FadeIn(VGroup(p1, p2, loads)), run_time=0.5)
            self.play(VGroup(p1, p2, loads).animate.shift(RIGHT * 6.5 + UP * 0.25), run_time=3.0, rate_func=linear)
            self.play(FadeIn(feet), run_time=0.4)
        self.play(FadeOut(VGroup(snowg, p1, p2, loads, feet)), run_time=0.5)
        shop = VGroup(Rectangle(width=2.4, height=1.6, stroke_width=0, fill_color="#5A4A3A", fill_opacity=1),
                      Polygon([-1.4, 0.8, 0], [1.4, 0.8, 0], [0, 1.6, 0], stroke_width=0, fill_color="#3A2A1E", fill_opacity=1),
                      Rectangle(width=1.6, height=0.9, stroke_width=0, fill_color="#2A1E14", fill_opacity=1).shift(DOWN * 0.3)).move_to([-4.3, -2.2, 0])
        closed = C.pill("पसल बन्द", CORAL, 24).next_to(shop, UP, buff=0.3)
        fire = VGroup(*[C.flame(0.6 + 0.1 * k).move_to([0.6 + 0.25 * k, -2.75, 0]) for k in range(3)])
        logs = VGroup(*[Line([0.2, -3.05, 0], [1.6, -2.9, 0], color="#6B4A32", stroke_width=10), Line([0.2, -2.9, 0], [1.6, -3.05, 0], color="#6B4A32", stroke_width=10)])
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GOLD, fill_opacity=0.06).move_to([0.9, -2.6, 0]) for r in (0.9, 1.4, 2.0)])
        oranges = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color="#F28C28", fill_opacity=1).move_to([3.0 + 0.3 * k, -3.0, 0]) for k in range(3)])
        clk = C.pill(f"राति {self.num(12)} बजे", SKY, 26).to_corner(DL, buff=0.6).shift(UP * 0.1)
        with self.say("अन्तिम खण्डमा पोखराको रात। राति बाह्र बजे पुग्दा पसल बन्द थियो, र बुढाले बास दिएनन्। अनि उनीहरूले सुन्तला खाए, दाउरा किनेर आगो बाले, र आगो ताप्दै साथीहरूलाई पर्खिए।"):
            self.play(FadeIn(shop), FadeIn(clk), run_time=0.5)
            self.play(FadeIn(closed), run_time=0.4)
            self.play(FadeIn(logs), FadeIn(glow), LaggedStart(*[GrowFromEdge(f, DOWN) for f in fire], lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(oranges, lag_ratio=0.2), run_time=0.5)
            self.play(*[f.animate.scale(1.15) for f in fire], rate_func=there_and_back, run_time=0.8)
        clk2 = C.pill(f"राति {self.num(2)} बजे", SKY, 26).move_to(clk)
        stones = VGroup(*[Ellipse(width=0.7, height=0.35, stroke_width=0, fill_color="#7A7A8A", fill_opacity=1).move_to([2.4 + 1.3 * k, -2.2, 0]) for k in range(3)])
        dream = C.pill("भोलि डँडेलधुरा पुग्ने कल्पना", MINT, 26).move_to([3.4, -0.6, 0])
        with self.say("राति दुई बजे भरिया र साथी आइपुगे। सबै जना ढुङ्गाको सिरानी लगाएर, भोलि डँडेलधुरा पुग्ने कल्पना गर्दै सुते। नियात्रा यहीँ टुङ्गिन्छ।"):
            self.play(Transform(clk, clk2), run_time=0.4)
            self.play(FadeIn(stones, lag_ratio=0.2), run_time=0.6)
            self.play(FadeIn(dream, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(nt, shop, closed, fire, logs, glow, oranges, clk, stones, dream, tag)), run_time=0.6)

    # ------------------------------------------------------------------ part 6: characters & theme
    def p6(self):
        self.section(5)
        head = C.heading("यात्राका साथीहरू", color=self.color)
        people = [("लेखक ('म')", "मोटो शरीर, उकालोसित डराउने, तर हँसिलो र राष्ट्रप्रेमी", GOLD),
                  ("प्रेमबहादुर प्रधान", "लेखकका साथी; फुर्तिला, बास खोज्न अघि दौडिने", SKY),
                  ("रामसिंह र भतिजो", "भरिया; सहनशील, खाली खुट्टा हिउँमा हिँड्ने, बाटोका जानकार", MINT),
                  ("यमुनाराज पौड्याल", "सहायक अञ्चलाधीश; तत्काल भरिया मिलाइदिने सहयोगी", TEAL),
                  ("खड्किनी", "मकै भुटिदिने; पैसा पहिले लिने व्यवहारकुशल महिला", PINK),
                  ("पोखराका बुढा", "पसले; निठुरी जस्ता देखिने तर सीमित साधनका", CORAL)]
        cards = VGroup(*[C.card(a, b, c, w=4.0, h=2.2, hsize=28, bsize=22) for a, b, c in people]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3))
        cards.next_to(head, DOWN, buff=0.4)
        with self.say("नियात्रामा कथाका जस्ता विकसित पात्र हुँदैनन्, तर यात्राका साथीहरूले लेखकको स्वभावलाई उजागर गर्छन्।"):
            self.play(FadeIn(head), run_time=0.4)
        narrs = ["लेखक आफैँ, म। मोटो शरीर, उकालोसित डराउने, तर हँसिलो र राष्ट्रप्रेमी।",
                 "प्रेमबहादुर प्रधान, लेखकका फुर्तिला साथी, बास खोज्न अघि दौडिने।",
                 "रामसिंह र उसको भतिजो, भरिया। सहनशील, खाली खुट्टा हिउँमा हिँड्ने, बाटोका जानकार।",
                 "यमुनाराज पौड्याल, सहायक अञ्चलाधीश, जसले तत्कालै भरिया मिलाइदिए।",
                 "खड्किनी, जसको लोग्ने परदेश गएका छन्, पैसा पहिले लिएर मकै भुटिदिने व्यवहारकुशल महिला।",
                 "र पोखराका बुढा पसले, निठुरी जस्ता देखिने, तर परिवेशका सीमित साधन बोकेका।"]
        for c, n_ in zip(cards, narrs):
            with self.say(n_):
                self.play(FadeIn(c, shift=UP * 0.2, scale=0.9), run_time=0.5)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        block = C.kblock(["कठिन भूगोलको यात्रा शरीर थकाउँछ, तर जीवनलाई रमाइलो बनाउँछ;", "प्रकृतिसित जुध्नुमै जीवनको सौन्दर्य छ,", "र देशका सबै भूभागप्रतिको माया नै सच्चा राष्ट्रप्रेम हो।"],
                         size=34, hl={"रमाइलो": MINT, "जुध्नुमै": CORAL, "राष्ट्रप्रेम": GOLD}, buff=0.35).move_to(UP * 0.3)
        fr = C.quote_frame(block, GOLD)
        with self.say("अब मूल भाव। कठिन भूगोलमा गरिने यात्राले शरीर थकाउँछ, तर जीवनलाई रमाइलो र अर्थपूर्ण बनाउँछ। प्रकृतिसित जुध्नुमै जीवनको सौन्दर्य छ, र देशका सबै भूभागप्रतिको माया नै सच्चा राष्ट्रप्रेम हो।") as v:
            self.play(FadeIn(fr), run_time=0.5)
            C.type_in(self, block, run_time=min(v.dur * 0.7, 6))
        self.play(FadeOut(VGroup(fr, block)), run_time=0.5)
        head = C.heading("मूल भावका चार खम्बा", color=self.color)
        data = [("राष्ट्रप्रेम", "पूर्वदेखि पश्चिमसम्म सबै ठाउँ प्यारा", GOLD), ("सङ्घर्षको रमाइलो", "कठिनाइलाई हास्यले सामना", CORAL),
                ("मानवीय सहयोग", "अञ्चलाधीश, पाटनका साथी, प्रधानपञ्च", MINT), ("विकटताको यथार्थ", "सडक र सुविधाको अभाव", SKY)]
        base = Rectangle(width=12, height=0.25, stroke_width=0, fill_color=th.PANEL_EDGE, fill_opacity=1).move_to([0, -2.9, 0])
        narrs = ["पहिलो, राष्ट्रप्रेम। पूर्वदेखि पश्चिमसम्म नेपालका सबै ठाउँ लेखकलाई उत्तिकै प्यारा छन्।",
                 "दोस्रो, सङ्घर्षको रमाइलो। उकालोको कठिनाइलाई हास्यका साथ सामना गर्ने दृष्टि।",
                 "तेस्रो, मानवीय सहयोग। सहायक अञ्चलाधीश, पाटनका साथी र प्रधानपञ्चको सहयोग।",
                 "चौथो, विकटताको यथार्थ। सडक र सुविधाको अभावमा नेपालका गाउँले र यात्रुले भोग्ने कठिनाइ।"]
        self.play(FadeIn(head), FadeIn(base), run_time=0.4)
        cols = []
        for i, ((n_, b_, c_), nr) in enumerate(zip(data, narrs)):
            x = -4.5 + 3.0 * i
            col = Rectangle(width=2.7, height=4.4, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.15).move_to([x, -0.58, 0])
            nt_ = para(n_, width=2.4, size=28, color=c_, align="center", weight="BOLD").move_to([x, 0.8, 0])
            bt_ = para(b_, width=2.3, size=22, color=th.BODY, align="center").move_to([x, -0.9, 0])
            with self.say(nr):
                self.play(GrowFromEdge(col, DOWN), run_time=0.6)
                self.play(FadeIn(nt_), FadeIn(bt_), run_time=0.5)
            cols.append(VGroup(col, nt_, bt_))
        self.play(FadeOut(VGroup(head, base, *cols)), run_time=0.5)

    # ------------------------------------------------------------------ part 7: style
    def p7(self):
        self.section(6)
        head = C.heading("झर्रो शैली: बोलीचालका स्थानीय रूप", color=self.color, size=36)
        pairs = [("बाटामी गाड पडन्छ", "बाटोमा खोला पर्छ"), ("जेमराज", "यमराज"), ("पर्तिर", "परतिर, परपट्टि"), ("अलेलि", "अलि अलि")]
        rows = VGroup()
        for a_, b_ in pairs:
            l = C.pill(a_, GOLD, 30)
            arr = Arrow(LEFT * 0.6, RIGHT * 0.6, color=th.MUTED, buff=0)
            r = T(b_, size=30, color=th.INK)
            rows.add(VGroup(l, arr, r).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)
        with self.say("यस नियात्राको शैली सरल, बोलीचालको ठेट नेपाली, अर्थात् झर्रो शैली हो, र हास्यव्यङ्ग्यात्मक पनि। पाठमा स्थानीय बोलीका रूप पनि आएका छन्। परीक्षामा यिनको सही रूप सोधिन्छ।"):
            self.play(FadeIn(head), run_time=0.4)
        with self.say("बाटामी गाड पडन्छ, अर्थात् बाटोमा खोला पर्छ। जेमराज, अर्थात् यमराज। पर्तिर, परतिर। र अलेलि, अलि अलि।") as v:
            for r_ in rows:
                self.play(FadeIn(r_[0], shift=RIGHT * 0.2), run_time=0.4)
                self.play(GrowArrow(r_[1]), FadeIn(r_[2], shift=LEFT * 0.2), run_time=0.5)
                self.hold(v.dur / 4 - 1.0)
        self.play(FadeOut(VGroup(head, rows)), run_time=0.5)
        head = C.heading("शब्दस्रोत", color=self.color)
        a = VGroup(T("तद्भव र आगन्तुक: प्रचुर", size=30, color=MINT, weight="BOLD"),
                   VGroup(*[C.pill(w, MINT, 24) for w in ("उकालो", "ओरालो", "साँघु", "धारो", "कुला", "कटेरो", "लालटिन", "घडी")]).arrange_in_grid(rows=2, cols=4, buff=0.2)).arrange(DOWN, buff=0.35)
        b = VGroup(T("तत्सम: सीमित", size=30, color=GOLD, weight="BOLD"),
                   VGroup(*[C.pill(w, GOLD, 24) for w in ("सुदूर", "अद्वितीय", "विरह", "दृष्टिपात", "सहृदय")]).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.35)
        VGroup(a, b).arrange(DOWN, buff=0.6).move_to(DOWN * 0.3)
        with self.say("शब्दस्रोत हेर्दा, दमयन्तीको कथाभन्दा ठिक उल्टो। यहाँ तद्भव र आगन्तुक शब्द प्रचुर छन्, जस्तै उकालो, ओरालो, साँघु, धारो, कुला, कटेरो, लालटिन, घडी। तत्सम शब्द सीमित छन्, जस्तै सुदूर, अद्वितीय, विरह, दृष्टिपात, सहृदय।"):
            self.play(FadeIn(head), FadeIn(a[0]), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in a[1]], lag_ratio=0.1), run_time=1.5)
            self.play(FadeIn(b[0]), LaggedStart(*[FadeIn(p, scale=0.8) for p in b[1]], lag_ratio=0.1), run_time=1.5)
        self.play(FadeOut(VGroup(head, a, b)), run_time=0.5)
        head = C.heading("अलङ्कार र हास्य", color=self.color)
        al = [("मानवीकरण", "घनघस्या: रिसाएको वृद्ध", CORAL), ("उपमा", "मरुद्यान भेटे झैँ फुलेल", MINT),
              ("अतिशयोक्ति", "टोपी खस्ने उकालो; चन्द्रमा जस्तै टाढा डँडेलधुरा", GOLD), ("तुलना", "मधेस पुग्ने बेलाको झैँ ओरालो", SKY),
              ("व्यङ्ग्य र हास्य", "उकालो देख्नेबित्तिकै सातोपुत्लो उड्छ", PINK), ("उखान टुक्का", "सातोपुत्लो उड्नु, मन ढक्क फुल्नु", TEAL)]
        cards = VGroup(*[C.card(a_, b_, c_, w=4.0, h=2.0, hsize=30, bsize=23) for a_, b_, c_ in al]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).next_to(head, DOWN, buff=0.45)
        with self.say("अलङ्कारको छोटो सूची। मानवीकरण, घनघस्यालाई रिसाएको वृद्ध बनाउनु। उपमा, मरुद्यान भेटे झैँ फुलेल हुनु। अतिशयोक्ति, टोपी खस्ने उकालो, र चन्द्रमा जस्तै टाढा भएर बिलाएको डँडेलधुरा। तुलना, पहाडबाट मधेस पुग्ने बेलाको झैँ ओरालो। व्यङ्ग्य र हास्य, उकालो देख्नेबित्तिकै सातोपुत्लो उड्छ। र उखान टुक्का, सातोपुत्लो उड्नु, मन ढक्क फुल्नु।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for c in cards:
                self.sfx("pop", gain=-15)
                self.play(FadeIn(c, shift=UP * 0.2, scale=0.9), run_time=0.45)
                self.hold(v.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        head = C.heading("समीक्षा", color=self.color)
        good = VGroup(T("बलियो पक्ष", size=32, color=MINT, weight="BOLD"),
                      *[C.pill(t, MINT, 23) for t in ("कठिनाइलाई हाँसोमा बदल्ने हास्य", "मौलिक मानवीकरण र उपमा", "स्थानीय बोली र गाउँले जीवन")]).arrange(DOWN, buff=0.3).move_to([-3.4, -0.1, 0])
        bad = VGroup(T("कमजोर पक्ष", size=32, color=CORAL, weight="BOLD"),
                     *[C.pill(t, CORAL, 23) for t in ("गन्तव्यअघि नै अन्त्य: अपूर्ण", "भरियाको पीडा ओझेलमा", "स्थानीय शब्द बुझ्न अप्ठ्यारो")]).arrange(DOWN, buff=0.3).move_to([3.4, -0.1, 0])
        div = Line([0, 2.0, 0], [0, -2.4, 0], color=th.FAINT, stroke_width=2)
        with self.say("समीक्षामा, सबैभन्दा ठुलो बल हास्य र सरलता हो। कठिन यात्राको पीडालाई लेखकले हाँसोमा बदलेका छन्, त्यसैले पाठक थकित हुँदैन, यात्रामै सहभागी भएको महसुस गर्छ। मानवीकरण र उपमा मौलिक छन्, र स्थानीय बोली र गाउँले जीवनले पाठलाई सजीव बनाएका छन्।"):
            self.play(FadeIn(head), Create(div), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in good], lag_ratio=0.35), run_time=2.0)
        with self.say("कमजोर पक्ष, डँडेलधुरा पुग्नुअघि नै नियात्रा टुङ्गिएकाले अपूर्ण लाग्न सक्छ। म को हास्यबिच भरिया जस्ता सङ्घर्षशील पात्रको पीडा ओझेलमा परेको छ। र स्थानीय शब्द आजका विद्यार्थीलाई बुझ्न अप्ठ्यारो हुन सक्छन्।"):
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.2) for x in bad], lag_ratio=0.35), run_time=2.0)
        with self.say("तैपनि यो नियात्रा विधाको सफल नमुना हो। यसले सिकाउँछ, यात्रा भनेको गन्तव्यमा पुग्ने हतारो होइन, बाटोमा बटुलिने अनुभूति हो।"):
            self.play(Circumscribe(good, color=MINT), run_time=1.2)
        self.play(FadeOut(VGroup(head, good, bad, div)), run_time=0.5)

    # ------------------------------------------------------------------ part 8: exam frames
    def p8(self):
        self.section(7)
        head = C.heading("परीक्षाले खोज्ने तीन कुरा", color=self.color)
        kinds = VGroup(C.card("घटना र स्थानको क्रम", "बैतडी, सतबाँझ, पाटन, अघोरी गाड, घनघस्या, पोखरा", SKY, w=3.9, h=2.4),
                       C.card("भाव विस्तार", "मानवीकरण, हिउँ र कठिनाइसँग जोडिएका भनाइ", GOLD, w=3.9, h=2.4),
                       C.card("विधाका विशेषता", "यात्रा वर्णन र निजी भावनाको मिश्रण", MINT, w=3.9, h=2.4)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        with self.say("यस पाठबाट पनि पाठगत बोधका आठ र समीक्षात्मकका आठ अङ्कसम्म सोधिन सक्छ। प्रायः तीन कुरा खोजिन्छ। घटना र स्थानको क्रम, घनघस्या र हिउँसँग जोडिएका भनाइको भाव विस्तार, र नियात्रा विधाका विशेषता।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for k in kinds:
                self.play(FadeIn(k, shift=UP * 0.3), run_time=0.5)
                self.hold(v.dur / 3 - 0.7)
        self.play(FadeOut(VGroup(head, kinds)), run_time=0.5)
        qq = para(f"प्रश्न: 'प्रकृतिसित जुध्नु नै जीवनको रमाइलो हो भन्ने भावलाई ह्याकुलाले छोपेर नै म सुदूरपश्चिमको भ्रमणमा निक्लेको थिएँ।' — भाव विस्तार गर्नुहोस्। [{self.num(4)}]", width=12, size=28, color=th.INK).move_to(UP * 0.3)
        with self.say("पहिले चार अङ्कको भाव विस्तार। प्रकृतिसित जुध्नु नै जीवनको रमाइलो हो, भन्ने भावलाई ह्याकुलाले छोपेर नै म सुदूरपश्चिमको भ्रमणमा निक्लेको थिएँ।"):
            self.play(FadeIn(qq, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(qq), run_time=0.4)
        f = C.answer_frame(self, f"भाव विस्तार: तीन चरण  [{self.num(4)}]", [
            ("सन्दर्भ", "तारानाथ शर्माको नियात्रा 'घनघस्याको उकालो काट्ता' मा कठिन भूगोलको यात्राको प्रेरणा बताउँदा लेखिएको।",
             "पहिलो चरण, सन्दर्भ। लेखक, नियात्रा, र कुन प्रसङ्गमा भनिएको हो।"),
            ("अर्थ विस्तार", "प्रकृति = पहाड, उकालो, हिउँ, खोला; जुध्नु = हार नमानी सङ्घर्ष; ह्याकुला = काँधको थैलो, अर्थात् चाहनालाई भारी झैँ मनभरि बोक्नु।",
             "दोस्रो चरण, अर्थ विस्तार। प्रकृति भनेको पहाड, उकालो र हिउँ। जुध्नु भनेको हार नमानी सङ्घर्ष गर्नु। र ह्याकुला भनेको काँधमा झुन्ड्याउने थैलो, अर्थात् यो चाहना लेखकले भारी झैँ मनभरि बोकेका थिए।"),
            ("निचोड", "सजिलो बाटोको सन्तोषभन्दा कठिनाइ जितेपछिको आनन्द ठुलो; जीवनको रमाइलो सङ्घर्षमै छ।",
             "तेस्रो चरण, निचोड। कठिनाइ जितेपछि पाइने आनन्द सबैभन्दा ठुलो हुन्छ। जीवनको रमाइलो सङ्घर्षमै छ।"),
        ], color=SKY, size=24, top=2.3)
        self.wait(0.8)
        self.play(FadeOut(f), run_time=0.5)
        qq = para(f"प्रश्न: 'घनघस्याको उकालो काट्ता' मा लेखकले यात्राको कठिनाइलाई हास्यका साथ प्रस्तुत गरेका छन्। — समीक्षा गर्नुहोस्। [{self.num(8)}]", width=12, size=28, color=th.INK).move_to(UP * 0.3)
        with self.say("अब आठ अङ्कको समीक्षात्मक प्रश्न। लेखकले यात्राको कठिनाइलाई हास्यका साथ प्रस्तुत गरेका छन्, समीक्षा गर्नुहोस्।"):
            self.play(FadeIn(qq, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(qq), run_time=0.4)
        f = C.answer_frame(self, f"समीक्षात्मक उत्तरको ढाँचा  [{self.num(8)}]", [
            ("भूमिका", "यात्राको कठिनाइ वास्तविक, तर प्रस्तुति हास्यपूर्ण; म सहमत छु।",
             "भूमिकामा भन्नुहोस्, कठिनाइ वास्तविक छ, तर प्रस्तुति हास्यले भरिएको छ, र म सहमत छु।"),
            ("पहिलो आधार", "आफैँलाई हाँसोको पात्र: 'मोटो शरीर… सातोपुत्लो उड्छ', 'जेमराज जत्तिकै भयावह'।",
             "पहिलो आधार, लेखक आफैँलाई हाँसोको पात्र बनाउँछन्। मोटो शरीर र सातोपुत्लो उड्ने प्रसङ्ग।"),
            ("दोस्रो आधार", "अतिशयोक्तिपूर्ण तुलना: निल आर्मस्ट्रङ, अलकत्रे बाटोलाई सराप्नु, मरुद्यानको उपमा।",
             "दोस्रो, अतिशयोक्तिपूर्ण तुलना। निल आर्मस्ट्रङ, अलकत्रे बाटो र मरुद्यान।"),
            ("तेस्रो आधार", "मानवीकरण: घनघस्या रिसाएको वृद्ध; 'यो मान्छेसित रिसाएको छ'।",
             "तेस्रो, मानवीकरण। रिसाएको बुढो घनघस्याले डरलाग्दो उकालोलाई पनि रमाइलो पात्र बनाउँछ।"),
            ("सीमा", "हास्यको बिचमा भरियाको पीडा र गाउँले जीवन ओझेलमा।",
             "सीमा पनि लेख्नुहोस्। हास्यका बिचमा भरियाको पीडा ओझेलमा परेको छ।"),
            ("निष्कर्ष", "हास्यले नै नियात्राको सौन्दर्य र पठनीयता बढाएको छ।",
             "र निष्कर्ष, हास्यले नै यो नियात्राको सौन्दर्य र पठनीयता बढाएको छ।"),
        ], color=GOLD, size=22, top=2.4)
        self.wait(0.8)
        self.play(FadeOut(f), run_time=0.5)
        self.tip("'नियात्रा' नाम बालकृष्ण पोखरेलले दिएका हुन्; विधाका स्थापक तारानाथ शर्मा। दुवै नाम गडबड नगर्नुहोस्।",
                 "अन्तिम सुझाव। नियात्रा नाम दिने बालकृष्ण पोखरेल हुन्, तर यो विधाका स्थापक तारानाथ शर्मा। एक अङ्कको प्रश्नमा यी दुई नाम धेरैले साटासाट गर्छन्।", state="success")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            f"'घनघस्याको उकालो काट्ता' — तारानाथ शर्माको नियात्रा; यात्रा वि.सं. {self.num(2024)} पुसको अन्तिम हप्ता",
            f"तारानाथ: जन्म {self.num(1991)}, इलाम; निधन {self.num(2078)}; नियात्रा विधाका स्थापक; 'बेलाइततिर बरालिँदा' मदन पुरस्कार ({self.num(2026)})",
            "नियात्रा = यात्रा वर्णन + निजी अनुभूति, विचार, हास्य; नाम: बालकृष्ण पोखरेल",
            "क्रम: शाहीलेक → सतबाँझ → पाटन → अघोरी गाड → घनघस्या → धुरा → पोखरा",
            "घनघस्या: बरफ = फुलेको केश, काला रुख = भुत्ला; रिसाएको वृद्ध",
            "हास्य: निल आर्मस्ट्रङ, अलकत्रे बाटो सराप्नु, मरुद्यान झैँ",
            "मूल भाव: प्रकृतिसित जुध्नु नै जीवनको रमाइलो; सबै भूभागप्रति माया",
        ], "छोटो पुनरावलोकन। घनघस्याको उकालो काट्ता तारानाथ शर्माको नियात्रा हो, दुई हजार चौबीसको पुसमा गरिएको यात्रा। तारानाथ नियात्रा विधाका स्थापक हुन्। नियात्रा भनेको यात्रा वर्णन र निजी अनुभूतिको मिश्रण। यात्राको क्रम, शाहीलेक, सतबाँझ, पाटन, अघोरी गाड, घनघस्या, धुरा, पोखरा। घनघस्या रिसाएको बुढो, बरफ उसको केश। हास्यका प्रसङ्ग, निल आर्मस्ट्रङ, अलकत्रे बाटो र मरुद्यान। र मूल भाव, प्रकृतिसित जुध्नु नै जीवनको रमाइलो।")
        self.outro("आजलाई यति नै। जीवनमा उकालो आउँछ नै, तर तारानाथ जस्तै, हाँस्दै काट्नुहोस्। अर्को पाठमा हामी व्यावसायिक पत्र लेख्न सिक्नेछौँ। नेबियन्समा फेरि भेटौँला।")
