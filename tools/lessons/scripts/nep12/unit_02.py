import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, T, para, th  # noqa: E402
import _common as C  # noqa: E402

GOLD, SKY, MINT, CORAL, PINK, TEAL = th.AMBER, th.SKY, th.MINT, th.CORAL, th.PINK, th.TEAL
DAMA = "#1F8A8A"


class Lesson(Lesson):
    SUBJECT = "nep"
    GRADE = 12
    UNIT = 2
    LANG = "ne"
    TITLE = "विरहिणी दमयन्ती"
    SUBTITLE = "मदनमणि दीक्षित  ·  पौराणिक कथा"
    SECTIONS = ["लेखक परिचय", "पाठको पृष्ठभूमि", "कथासार: यात्राको नक्सा", "खण्डगत व्याख्या", "पात्र र चरित्र",
                "मूल भाव र समीक्षा", "कथाका तत्त्व र भाषाशैली", "उत्तर लेख्ने ढाँचा"]
    NEXT = "एकाइ ३  ·  घनघस्याको उकालो काट्ता"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.ending)

    # ------------------------------------------------------------------ helpers
    def dama(self, h=2.4):
        return C.woman(h, sari=DAMA)

    def night(self):
        return VGroup(C.sky("#070A1C", "#141834"), C.stars(70, seed=21))

    def forest_bg(self, seed=3, color="#2E6B3A"):
        back = C.forest(11, y=-3.0, seed=seed, hmin=1.8, hmax=2.8, color="#1F4A2A")
        front = C.forest(7, y=-3.2, seed=seed + 4, hmin=2.2, hmax=3.2, color=color)
        return VGroup(back, front)

    def ktag(self, i, name, color):
        t = VGroup(C.badge(self, i, color, r=0.24), T(name, size=24, color=color, weight="SEMIBOLD")).arrange(RIGHT, buff=0.2)
        return t.to_corner(UR, buff=0.45).shift(DOWN * 0.05)

    def fire(self, at, n=5, h=0.7):
        g = VGroup()
        for k in range(n):
            f = C.flame(h * (0.7 + 0.3 * ((k * 7) % 3) / 2)).move_to(at + RIGHT * (k - (n - 1) / 2) * h * 0.45)
            g.add(f)
        return g

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        nt = self.night()
        mn = C.moon(0.45).move_to([4.8, 2.5, 0])
        fr = self.forest_bg()
        hut = C.hut(1.8, wall="#5A4A3A", roof="#3A2A1E", lamp=False).move_to([-3.0, -2.6, 0])
        d = self.dama(2.1).move_to([-1.0, -3.2, 0], aligned_edge=DOWN)
        n = C.man(2.2, crown=True).move_to([0.2, -3.2, 0], aligned_edge=DOWN)
        self.add(nt, mn)
        with self.say("मध्यरात। घना जङ्गल। रूखहरूको बिचमा एउटा सानो छाप्रो।"):
            self.play(FadeIn(nt), FadeIn(mn), run_time=1.0)
            if self.hud is not None:
                self.bring_to_front(self.hud)
            self.play(FadeIn(fr, shift=UP * 0.3, lag_ratio=0.05), FadeIn(hut), run_time=1.5)
        with self.say("छाप्रोमा एउटी रानी थकित भएर निदाएकी छिन्। छेउमै उनका पति, एक राजा।"):
            self.play(FadeIn(d), FadeIn(n), run_time=0.8)
            piv = d.get_bottom() + RIGHT * 0.5
            self.play(Rotate(d, -PI / 2, about_point=piv), run_time=1.2)
        with self.say("तर जब रानी ब्युँझिन्छिन्, छेउमा कोही छैन। राजा केही नभनी, अँध्यारोमा कतै हिँडिसकेका छन्।"):
            self.play(n.animate.shift(RIGHT * 7).set_opacity(0), run_time=2.5, rate_func=rate_functions.ease_in_sine)
            self.play(Rotate(d, PI / 2, about_point=piv), run_time=1.0)
        self.remove(n)
        qs = VGroup(T("एक्ली", size=44, color=th.INK, weight="BOLD"), T("भोकी", size=44, color=th.INK, weight="BOLD"),
                    T("डरलाग्दो जङ्गल", size=44, color=CORAL, weight="BOLD")).arrange(RIGHT, buff=0.6).move_to([1.4, 1.2, 0])
        with self.say("एक्ली। भोकी। चारैतिर डरलाग्दो जङ्गल। अब उनी के गर्लिन्? रुँदै बस्लिन्? हार मान्लिन्?"):
            for q in qs:
                self.sfx("thud", gain=-14)
                self.play(FadeIn(q, scale=1.3), run_time=0.5)
        big = C.kline("बल होइन, बुद्धि र धैर्य", size=56, color=GOLD).move_to([1.2, 0.0, 0])
        with self.say("होइन। यो कथा त्यस्ती नारीको हो, जसले बलले होइन, बुद्धि र धैर्यले हरेक सङ्कट जितिन्। उनको नाम हो, दमयन्ती।"):
            self.play(qs.animate.shift(UP * 1.0).set_opacity(0.4), run_time=0.5)
            C.type_in(self, VGroup(big), run_time=1.5)
            self.play(Indicate(d, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.play(FadeOut(VGroup(nt, mn, fr, hut, d, qs, big)), run_time=0.8)
        g, nb = self.title_card()
        with self.say("नमस्ते! कक्षा बाह्रको अनिवार्य नेपालीको एकाइ दुईमा स्वागत छ। आजको पाठ हो, मदनमणि दीक्षितको पौराणिक कथा, विरहिणी दमयन्ती। विरहिणी भनेको पतिको वियोगमा परेकी नारी।"):
            pass
        self.end_title(g, nb)
        self.roadmap("आजको बाटो। पहिले लेखकलाई चिनौँ र कथाको पृष्ठभूमि बुझौँ। त्यसपछि दमयन्तीको यात्रालाई नक्सामा हेरौँ, खण्डखण्ड गरी व्याख्या गरौँ, पात्र र चरित्र, मूल भाव र समीक्षा, कथाका तत्त्व र भाषाशैली, र अन्त्यमा परीक्षामा उत्तर लेख्ने ढाँचा।")

    # ------------------------------------------------------------------ part 1: author
    def p1(self):
        self.section(0)
        name = C.kline("मदनमणि दीक्षित", size=64).move_to(UP * 1.4)
        under = Line(LEFT * 3, RIGHT * 3, color=self.color, stroke_width=5).next_to(name, DOWN, buff=0.25)
        pills = VGroup(C.pill("आख्यानकार", GOLD, 28), C.pill("पत्रकार", SKY, 28), C.pill("पौराणिक विषयका स्रष्टा", MINT, 28)).arrange(RIGHT, buff=0.35)
        pills.next_to(under, DOWN, buff=0.6)
        with self.say("मदनमणि दीक्षित नेपाली आख्यान साहित्यका वरिष्ठ स्रष्टा र पत्रकार हुन्। वैदिक र पौराणिक साहित्यका पात्र र कथावस्तु टिपेर लेख्नु उनको विशेषता हो।"):
            C.type_in(self, VGroup(name), run_time=1.2)
            self.play(Create(under), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pills], lag_ratio=0.3), run_time=1.5)
        self.play(FadeOut(VGroup(name, under, pills)), run_time=0.5)
        head = C.heading("जीवनरेखा", color=self.color)
        self.play(FadeIn(head), run_time=0.4)
        tl = C.timeline(self, [
            (1979, "जन्म · गैरीधारा, काठमाडौँ", "उनको जन्म विक्रम संवत् उन्नाइस सय उनासी, फागुन छ गते काठमाडौँको गैरीधारामा भयो। पिता लक्ष्मणमणि आचार्य दीक्षित, र माता विष्णुकुमारी।"),
            (2039, "'माधवी' उपन्यास · मदन पुरस्कार", "दुई हजार उनचालीस सालमा उनको उपन्यास माधवी प्रकाशित भयो, र त्यसले मदन पुरस्कार पायो। उनले साझा पुरस्कार पनि पाएका छन्।"),
            (2068, "पद्मश्री साधना सम्मान", "दुई हजार अठसट्ठी सालमा उनलाई पद्मश्री साधना सम्मान प्रदान गरियो।"),
            (2076, "निधन · जनैपूर्णिमा, काठमाडौँ", "र दुई हजार छयहत्तर साल साउन तीस गते, जनैपूर्णिमाका दिन काठमाडौँमा उनको निधन भयो।"),
        ], y=-0.2, label_w=3.0, size=24)
        with self.say("साहित्यसँगै उनी पत्रकार पनि थिए। लामो समय उनले समीक्षा साप्ताहिकको सम्पादन गरे।"):
            pass
        self.play(FadeOut(VGroup(head, tl)), run_time=0.5)
        head = C.heading("प्रमुख कृति", color=self.color)
        works = [("माधवी", "उपन्यास · मदन पुरस्कार", GOLD), ("कसले जित्यो कसले हार्‍यो ?", "कथा सङ्ग्रह", SKY),
                 ("चरैवेति · त्यो युग · हाम्रा ती दिन", "निबन्ध सङ्ग्रह", MINT), ("म रुँदै बिर्सन्छु", "संस्मरण", PINK),
                 ("बर्लिन डायरीका पाना", "यात्रावर्णन", TEAL), ("ऋग्वेद: केही प्रमुख सूक्त", "वैदिक सूक्तको प्रस्तुति", CORAL)]
        cards = VGroup(*[C.card(a, b, c, w=4.0, h=2.0, hsize=28, bsize=24) for a, b, c in works]).arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3))
        cards.next_to(head, DOWN, buff=0.45)
        with self.say("उनका प्रमुख कृति। माधवी उपन्यास, जसलाई नेपाली आख्यानको गहन र बृहत् कृति मानिन्छ। कसले जित्यो कसले हार्‍यो, कथा सङ्ग्रह। चरैवेति, त्यो युग र हाम्रा ती दिन, निबन्ध सङ्ग्रह। म रुँदै बिर्सन्छु, संस्मरण। बर्लिन डायरीका पाना, यात्रावर्णन। र ऋग्वेदका केही प्रमुख सूक्तको प्रस्तुति।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for c in cards:
                self.sfx("pop", gain=-15)
                self.play(FadeIn(c, shift=UP * 0.25, scale=0.9), run_time=0.45)
                self.hold(v.dur / 6 - 0.65)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        books = VGroup(*[C.pill(t, c, 28) for t, c in (("चार वेद", GOLD), ("अठार महापुराण", SKY), ("महाभारत", MINT))]).arrange(DOWN, buff=0.35).move_to([-4.2, 0.4, 0])
        arr = Arrow([-2.4, 0.4, 0], [-0.4, 0.4, 0], color=GOLD, stroke_width=6)
        reader = C.card("आधुनिक पाठक", "सरल र मानवीय भाषामा", PINK, w=3.6, h=1.8).move_to([1.6, 0.4, 0])
        with self.say("उनको ठुलो योगदान के हो भने, चार वेद, अठार महापुराण र महाभारत जस्ता पूर्वीय ग्रन्थको सारलाई उनले आधुनिक पाठकसामु सरल र मानवीय भाषामा ल्याइदिए।"):
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in books], lag_ratio=0.3), run_time=1.2)
            self.play(GrowArrow(arr), FadeIn(reader, shift=LEFT * 0.2), run_time=0.8)
        self.play(FadeOut(VGroup(books, arr, reader)), run_time=0.4)
        halo = VGroup(Circle(radius=0.75, stroke_color=GOLD, stroke_width=6).move_to([-3.5, 1.0, 0]),
                      T("देवी", size=40, color=GOLD, weight="BOLD").move_to([-3.5, 1.0, 0]))
        cross = VGroup(Line([-4.3, 0.2, 0], [-2.7, 1.8, 0], color=CORAL, stroke_width=7), Line([-4.3, 1.8, 0], [-2.7, 0.2, 0], color=CORAL, stroke_width=7))
        hum = VGroup(C.heart(0.55, color=PINK).move_to([2.6, 1.0, 0]), T("मानिस", size=40, color=th.INK, weight="BOLD").move_to([3.9, 1.0, 0]))
        feels = VGroup(*[C.pill(t, c, 26) for t, c in (("दुःख", SKY), ("प्रेम", PINK), ("क्रोध", CORAL), ("आशा", GOLD))]).arrange(RIGHT, buff=0.3).move_to([3.3, -0.6, 0])
        arr = Arrow([-2.2, 1.0, 0], [1.8, 1.0, 0], color=th.MUTED, stroke_width=5)
        dm = C.pill("दमयन्ती: बुद्धि र धैर्यको बलमा सङ्कटसँग जुध्ने नारी", MINT, 28).move_to([0, -2.2, 0])
        with self.say("अझ महत्त्वपूर्ण कुरा, उनले पौराणिक पात्रलाई देवता वा चमत्कारका रूपमा मात्र हेरेनन्। दुःख, प्रेम, क्रोध र आशा भएका मानिसका रूपमा हेरे।"):
            self.play(FadeIn(halo), run_time=0.5)
            self.play(Create(cross), run_time=0.5)
            self.play(GrowArrow(arr), FadeIn(hum, scale=0.7), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in feels], lag_ratio=0.3), run_time=1.2)
        with self.say("त्यसैले यस कथामा पनि दमयन्ती कुनै अलौकिक शक्तिकी देवी होइनन्। उनी बुद्धि र धैर्यको बलमा सङ्कटसँग जुध्ने एक साहसी नारी हुन्।"):
            self.play(FadeIn(dm, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(halo, cross, hum, feels, arr, dm)), run_time=0.5)

    # ------------------------------------------------------------------ part 2: background
    def p2(self):
        self.section(1)
        outer = C.box(11.5, 5.4, color=GOLD).move_to(DOWN * 0.2)
        o_t = T("महाभारत", size=36, color=GOLD, weight="BOLD").move_to(outer.get_top() + DOWN * 0.45)
        mid = C.box(8.6, 3.6, color=MINT).move_to(DOWN * 0.5)
        m_t = T("वनपर्व", size=32, color=MINT, weight="BOLD").move_to(mid.get_top() + DOWN * 0.4)
        inner = C.box(5.6, 1.9, color=PINK).move_to(DOWN * 0.8)
        i_t = T("नलोपाख्यान", size=36, color=PINK, weight="BOLD").move_to(inner)
        with self.say("नल र दमयन्तीको कथा कहाँबाट आएको हो? महाभारतभित्र, वनपर्व छ। र त्यही वनपर्वभित्र आउँछ, नलोपाख्यान, अर्थात् नलको कथा।"):
            self.play(FadeIn(outer), FadeIn(o_t), run_time=0.7)
            self.play(FadeIn(mid, scale=0.9), FadeIn(m_t), run_time=0.7)
            self.play(FadeIn(inner, scale=0.9), FadeIn(i_t), run_time=0.7)
            self.play(Indicate(i_t, color=PINK), run_time=0.8)
        self.play(FadeOut(VGroup(outer, o_t, mid, m_t, inner, i_t)), run_time=0.5)
        n = C.man(2.3, crown=True).move_to([-4.2, -2.6, 0], aligned_edge=DOWN)
        d = self.dama(2.3).move_to([4.2, -2.6, 0], aligned_edge=DOWN)
        ln = VGroup(T("नल", size=34, color=GOLD, weight="BOLD"), T("निषध देशका राजा", size=24, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(n, UP, buff=0.25)
        ld = VGroup(T("दमयन्ती", size=34, color=TEAL, weight="BOLD"), T("विदर्भकी राजकुमारी", size=24, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(d, UP, buff=0.25)
        hrt = C.heart(0.6, color=PINK).move_to([0, -1.2, 0])
        with self.say("निषध देशका राजा नल, र विदर्भकी राजकुमारी दमयन्ती। यिनको प्रेम, वियोग र पुनर्मिलनको कथा भारतीय र नेपाली परम्परामा निकै चर्चित छ।"):
            self.play(FadeIn(n, shift=RIGHT * 0.3), FadeIn(ln), run_time=0.7)
            self.play(FadeIn(d, shift=LEFT * 0.3), FadeIn(ld), run_time=0.7)
            self.play(FadeIn(hrt, scale=0.4), run_time=0.5)
            self.play(hrt.animate.scale(1.2), rate_func=there_and_back, run_time=0.6)
        dice = VGroup(C.dice(0.7, 5).rotate(0.3), C.dice(0.7, 2).rotate(-0.4)).arrange(RIGHT, buff=0.3).move_to([0, 0.9, 0])
        lost = C.pill("जुवामा राज्य गुमाए", CORAL, 28).move_to([0, 2.0, 0])
        with self.say("तर नलले जुवामा आफ्नो राज्य गुमाए, र दुवै जङ्गल पसे। अनि एक रात, नलले दमयन्तीलाई जङ्गलमै एक्ली छाडेर हिँडे।"):
            self.play(FadeIn(dice, shift=DOWN * 0.3), run_time=0.5)
            self.play(Rotate(dice[0], PI), Rotate(dice[1], -PI), run_time=0.8)
            self.play(FadeIn(lost), hrt.animate.set_color(th.MUTED), run_time=0.6)
            self.play(n.animate.shift(LEFT * 3).set_opacity(0), ln.animate.shift(LEFT * 3).set_opacity(0), run_time=1.5)
        start = C.pill("हाम्रो पाठ यहाँबाट सुरु हुन्छ", GOLD, 32).move_to([-1.5, -0.2, 0])
        arr = Arrow(start.get_right(), d.get_left() + UP * 0.6, color=GOLD, stroke_width=5)
        with self.say("हाम्रो पाठ ठिक यही परित्यागपछि सुरु हुन्छ। यो पूरा महाभारतको कथा होइन, लेखकले पुनः सिर्जना गरेको एउटा अंश हो।"):
            self.play(FadeOut(VGroup(dice, lost, hrt)), run_time=0.4)
            self.play(FadeIn(start, scale=0.8), GrowArrow(arr), run_time=0.8)
        self.remove(n, ln)
        self.play(FadeOut(VGroup(d, ld, start, arr)), run_time=0.5)
        self.tip("पाठको कथा लेखकको पुनःसिर्जना हो; मूल पौराणिक कथासँग सबै घटना नमिल्न सक्छन्। परीक्षामा पाठमा भएकै घटना लेख्नुहोस्।",
                 "एउटा परीक्षा सुझाव। टेलिभिजन वा अरू किताबमा तपाईँले नल दमयन्तीको अलि फरक कथा पढ्नुभएको होला। तर परीक्षामा मूल कथा होइन, पाठमा भएकै घटना लेख्नुहोस्।")

    # ------------------------------------------------------------------ part 3: journey map
    def p3(self):
        self.section(2)
        P = [np.array(p_) for p_ in ([-5.6, -1.5, 0], [-3.75, 0.5, 0], [-1.85, -1.5, 0], [0.0, 0.5, 0], [1.85, -1.5, 0], [3.75, 0.5, 0], [5.6, -1.5, 0])]
        road = C.stick_path([P[0] + LEFT * 0.7 + UP * 0.5] + P + [P[-1] + RIGHT * 0.7 + UP * 0.5], color="#5A4A3A", width=22)
        dash = DashedVMobject(road.copy().set_stroke(GOLD, 3), num_dashes=50)
        stops = [("जङ्गलमा नलको खोजी", GOLD), ("कर्कोटकको छाप्रो", CORAL), ("तीन दिनको यात्रा", MINT), ("ताराको रात र सपना", SKY),
                 ("शुचिभद्रको सार्थ", GOLD), ("तलाउमा हात्ती", CORAL), ("चेदी: सैरन्ध्री", MINT)]
        samples = [road.point_from_proportion(t) for t in np.linspace(0, 1, 400)]
        props = [float(np.linspace(0, 1, 400)[int(np.argmin([np.linalg.norm(q - p_) for q in samples]))]) for p_ in P]
        dots, labs = VGroup(), VGroup()
        for i, (t, c) in enumerate(stops):
            dt = VGroup(Circle(radius=0.28, fill_color=c, fill_opacity=1, stroke_color=WHITE, stroke_width=2),
                        T(self.num(i + 1), size=24, color=th.BG, weight="BOLD")).move_to(P[i])
            dots.add(dt)
            lab = para(t, width=2.6, size=25, color=c, align="center")
            lab.next_to(dt, UP if i % 2 == 1 else DOWN, buff=0.22)
            labs.add(lab)
        walker = self.dama(0.8).move_to(road.get_start() + LEFT * 0.5, aligned_edge=DOWN)
        head = C.heading("दमयन्तीको यात्रा", color=self.color)
        with self.say("पूरा कथालाई एउटा यात्राका रूपमा हेरौँ। दमयन्ती सात ठाउँ हुँदै अघि बढ्छिन्। यो नक्सा सम्झनुभयो भने घटनाक्रमको प्रश्न सजिलै आउँछ।"):
            self.play(FadeIn(head), Create(road), Create(dash), run_time=1.6)
            self.play(FadeIn(walker), run_time=0.4)
        narrs = [
            "पहिलो, मध्यरातमा कर्कोटक नागहरूको वनको छाप्रामा नलले छाडेर गएपछि, विदीर्ण हृदयले दमयन्ती उनलाई खोज्दै जङ्गलको गोरेटोमा हिँड्छिन्। वनका फूल, पात, चराचुरुङ्गीमा समेत उनी नलकै रूप देख्छिन्।",
            "दोस्रो, पिपलको फेदमा निदाएकी उनलाई एक कर्कोटक नागयुवकले समातेर काँधमा बोकी आफ्नो छाप्रोमा पुर्‍याउँछ। तर उनी बुद्धिले उसलाई जाँड खुवाएर, छाप्रोमा आगो लगाई पूर्वतिर भाग्छिन्, र शिंशपाको रुखमा रात काट्छिन्।",
            "तेस्रो, तीन दिनसम्म कन्दमूल खाँदै एक्लै हिँड्छिन्। लट्ठी बोक्छिन्, कपाल धुलोले जगल्टा बनाउँछिन्, र अनुहारमा हिलो दल्छिन्, ताकि कसैले आक्रमण नगरोस्।",
            "चौथो, तेस्रो रात खेतको ढुङ्गामा सुत्दा ध्रुवतारा, सप्तर्षि र आकाशगङ्गाले उनलाई मोहित पार्छन्। सपनामा ऋषिको आश्रमबाट आवाज आउँछ, अझै उत्तरतिर हिँड, तिम्रो नल भेटिनेछन्।",
            "पाँचौँ, उत्तरतिर हिँड्दा घन्टी बजाउँदै आएको व्यापारीहरूको लस्कर भेटिन्छ। सार्थवाह शुचिभद्रले भोजन र नयाँ वस्त्र दिन्छन्, र चेदीतिर नल भेटिन सक्ने बताउँछन्।",
            "छैटौँ, पद्मसौगन्धिक तलाउको किनारमा रात बिताउँदा जङ्गली हात्तीको बथान आउँछ, र सार्थ कुल्चिएर नष्ट हुन्छ। दमयन्ती अग्लो रुखमा चढेर बाँच्छिन्, अर्की नारीलाई पनि बचाउँछिन्।",
            "र सातौँ, चेदी पुगेर उनी आफ्नी ठुलीआमा, रानी सुनन्दाकहाँ पहिचान लुकाएर, तीन सर्तसहित सैरन्ध्रीको काम स्वीकार्छिन्।",
        ]
        prev = 0.0
        for i in range(7):
            with self.say(narrs[i]):
                a0, a1 = prev, props[i]
                if a1 > a0:
                    self.play(UpdateFromAlphaFunc(walker, lambda m, a, a0=a0, a1=a1: m.move_to(road.point_from_proportion(a0 + (a1 - a0) * a) + LEFT * 0.6 + DOWN * 0.15, aligned_edge=DOWN)), run_time=1.0)
                self.sfx("pop", gain=-13)
                self.play(GrowFromCenter(dots[i]), FadeIn(labs[i], shift=UP * 0.1), run_time=0.6)
            prev = props[i]
        groups = [("आदि", [0], GOLD), ("मध्य", [1, 2, 3, 4, 5], SKY), ("अन्त्य", [6], MINT)]
        tags = VGroup()
        for nm, idx, c in groups:
            xs = [dots[j].get_center()[0] for j in idx]
            t = C.pill(nm, c, 28).move_to([np.mean(xs), 2.35, 0])
            tags.add(t)
        with self.say("यसलाई आदि, मध्य र अन्त्यमा बाँड्दा, आदिमा नलको खोजी। मध्यमा कर्कोटक, तीन दिनको यात्रा, सार्थ र हात्तीको आक्रमण। र अन्त्यमा चेदीमा सैरन्ध्री बन्नु।"):
            self.play(FadeOut(head), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tags], lag_ratio=0.4), run_time=1.5)
        self.play(FadeOut(VGroup(road, dash, dots, labs, walker, tags)), run_time=0.6)

    # ------------------------------------------------------------------ part 4: sections
    def p4(self):
        self.section(3)
        self.k1()
        self.k2()
        self.k3()
        self.k4()
        self.k5()
        self.k6()
        self.k7()

    def k1(self):
        tag = self.ktag(1, "नलको भ्रम", GOLD)
        nt = self.night()
        fr = self.forest_bg(seed=8)
        d = self.dama(2.0).move_to([-5.0, -3.2, 0], aligned_edge=DOWN)
        self.add(nt, fr)
        self.play(FadeIn(nt), FadeIn(fr), FadeIn(tag), run_time=0.8)
        if self.hud is not None:
            self.bring_to_front(self.hud)
        ghosts = VGroup(*[C.man(1.8, crown=True).set_opacity(0.0).move_to([x, -3.0, 0], aligned_edge=DOWN) for x in (-2.0, 1.0, 4.0)])
        with self.say("पहिलो खण्डमा वियोगको उत्कट अनुभूति छ। नलसँग आनन्दको जीवन बिताएकी दमयन्ती, अब जताततै नल देख्न थाल्छिन्। रुखको छायाँमा, फूलमा, चराचुरुङ्गी र पशुमा समेत।"):
            self.play(FadeIn(d, shift=RIGHT * 0.3), run_time=0.6)
            self.play(d.animate.shift(RIGHT * 2.5), run_time=2.0)
            for g in ghosts:
                self.play(g.animate.set_opacity(0.35), run_time=0.5)
                self.play(g.animate.set_opacity(0.0), run_time=0.5)
        self.remove(ghosts)
        sh = C.kline("बौलाही झैँ प्रियतम नल !", size=46, color=GOLD).move_to([1.2, 1.6, 0])
        with self.say("उनी बौलाही झैँ पुकार्छिन्, प्रियतम नल! तर जङ्गल चुप छ।"):
            C.type_in(self, VGroup(sh), run_time=1.5)
            self.play(Wiggle(sh), run_time=1.0)
        self.play(FadeOut(sh), run_time=0.3)
        pip = C.tree(3.0, color="#3B7A47").move_to([3.8, -3.2, 0], aligned_edge=DOWN)
        cl = C.cloud(3.0, color="#2A2F4E").move_to([0.8, 1.5, 0])
        pus = VGroup(C.man(1.3, coat="#7A3A3A").move_to([0.2, 0.8, 0]), C.dice(0.4, 6).move_to([1.3, 1.6, 0]))
        lab = C.pill("सपनामा: जुवाडी पुष्कर", CORAL, 26).move_to([0.8, 2.75, 0])
        with self.say("भोकी, अर्धनग्न र शिथिल भएकी उनी एउटा पिपलको फेदमा सुत्छिन्। र सपनामा देख्छिन्, नलको भाइ, जुवाडी पुष्कर, जसका कारण यो सबै सङ्कट आएको थियो।"):
            self.play(FadeIn(pip), d.animate.move_to([2.6, -3.2, 0], aligned_edge=DOWN), run_time=1.2)
            self.play(Rotate(d, -PI / 2, about_point=d.get_bottom() + RIGHT * 0.5), run_time=0.8)
            self.play(FadeIn(cl, scale=0.6), FadeIn(pus), FadeIn(lab), run_time=0.8)
        self.play(FadeOut(VGroup(nt, fr, d, pip, cl, pus, lab, tag)), run_time=0.6)

    def k2(self):
        tag = self.ktag(2, "कर्कोटकको छाप्रो", CORAL)
        self.play(FadeIn(tag), run_time=0.3)
        hut = C.hut(2.4, wall="#5A4A3A", roof="#3A2A1E", lamp=True).move_to([-3.8, -2.3, 0])
        k = C.man(2.3, coat="#2F5A3A", shirt="#6B7A4A").move_to([-1.2, -3.2, 0], aligned_edge=DOWN)
        d = self.dama(2.2).move_to([0.2, -3.2, 0], aligned_edge=DOWN)
        lk = T("कर्कोटक नागयुवक", size=26, color=CORAL, weight="BOLD").next_to(k, UP, buff=0.2)
        with self.say("दोस्रो खण्ड कथाको सबैभन्दा रोमाञ्चक भाग हो। ब्युँझँदा एक कर्कोटक नागयुवक कामुक दृष्टिले हेर्दै उनको कपाल सुम्सुम्याइरहेको थियो। उनी दौडिन्, तर उसले समात्यो, र काँधमा बोकेर आफ्नो छाप्रोमा पुर्‍यायो।"):
            self.play(FadeIn(hut), FadeIn(k), FadeIn(d), FadeIn(lk), run_time=0.8)
            self.play(d.animate.shift(RIGHT * 2.0), run_time=0.6)
            self.play(k.animate.shift(RIGHT * 2.2), lk.animate.shift(RIGHT * 2.2), run_time=0.5)
            self.sfx("thud", gain=-12)
            self.play(VGroup(k, lk).animate.shift(LEFT * 2.4), d.animate.shift(LEFT * 2.4), run_time=1.2)
        self.play(FadeOut(VGroup(hut, k, d, lk)), run_time=0.4)
        steps = [("शान्त रहिन्", "छटपटाएपछि रक्षाको उपाय सोचिन्", SKY),
                 ("विश्वासमा लिइन्", "मुसुक्क हाँसेर नमस्कार, 'भोक लाग्यो'", GOLD),
                 ("कमजोरी प्रयोग गरिन्", "जाँड खुवाइन्, आगो लगाइन्, भागिन्", CORAL)]
        cards = VGroup(*[C.card(a, b, c, w=3.8, h=2.1, hsize=30, bsize=23) for a, b, c in steps]).arrange(RIGHT, buff=0.55).move_to(UP * 0.9)
        arrows = VGroup(*[Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.08, color=th.MUTED, stroke_width=5) for i in range(2)])
        nums = VGroup(*[C.badge(self, i + 1, steps[i][2], r=0.26).next_to(cards[i], UP, buff=0.15) for i in range(3)])
        narrs = ["तर यहाँ दमयन्तीले तीनओटा काम क्रमैसँग गरिन्। पहिले, शान्त रहिन्। छटपटाएर केही हुँदैन भनेर बुझेपछि उनले रक्षाको उपाय सोचिन्।",
                 "दोस्रो, नागलाई विश्वासमा लिइन्। मुसुक्क हाँसेर नमस्कार गरिन्, र भोक लागेको बताइन्। उसको दुष्ट नियत बुझेर पनि, पति हराएको कुरा मात्र सुनाइन्।",
                 "तेस्रो, उसकै कमजोरीको प्रयोग गरिन्। नागले खाना पकाउँदै जौको जाँड खायो। दमयन्तीले मायालु हातले अझ धेरै खुवाइन्। ऊ उङ्न थालेपछि, अगुल्टो लिएर बाहिर निस्किइन्।"]
        for i in range(3):
            with self.say(narrs[i]):
                self.play(GrowFromCenter(nums[i]), FadeIn(cards[i], shift=UP * 0.2), run_time=0.6)
                if i > 0:
                    self.play(GrowArrow(arrows[i - 1]), run_time=0.4)
        hut2 = C.hut(1.8, wall="#5A4A3A", roof="#3A2A1E", lamp=False).move_to([-3.8, -2.4, 0])
        flames = self.fire(hut2.get_top() + DOWN * 0.3, n=5, h=0.8)
        runner = self.dama(1.3).move_to([-2.2, -3.25, 0], aligned_edge=DOWN)
        east = T("पूर्वतिर", size=26, color=GOLD).move_to([3.5, -1.6, 0])
        tree = C.tree(2.2, color="#3B7A47").move_to([5.3, -3.25, 0], aligned_edge=DOWN)
        with self.say("ढोका र पिँढीमा जाँड पोखेर आगो लगाइदिइन्, र पूर्वतिर भागिन्। एक कोस पर शिंशपाको रुखमा बसेर रात कटाइन्।"):
            self.play(cards.animate.scale(0.7).to_edge(UP, buff=0.9), FadeOut(arrows), FadeOut(nums), run_time=0.6)
            self.play(FadeIn(hut2), FadeIn(runner), run_time=0.4)
            self.sfx("whoosh", gain=-10)
            self.play(LaggedStart(*[GrowFromEdge(f, DOWN) for f in flames], lag_ratio=0.15), run_time=1.0)
            self.play(runner.animate.move_to([4.6, -3.25, 0], aligned_edge=DOWN), FadeIn(east), FadeIn(tree),
                      *[f.animate.scale(1.3) for f in flames], run_time=2.0)
        key = C.pill("बल होइन, बुद्धि र संयमले खतरा जितिन्", MINT, 30).move_to([0, 0.15, 0])
        with self.say("यहाँ बल होइन, बुद्धि र संयमले खतरा जितिएको छ। यही प्रसङ्गले दमयन्तीलाई प्रत्युत्पन्नमति, अर्थात् तत्काल उपाय सोच्न सक्ने बुद्धिमती नारी बनाउँछ।"):
            self.play(FadeIn(key, scale=0.8), run_time=0.6)
        self.play(FadeOut(VGroup(cards, hut2, flames, runner, east, tree, key, tag)), run_time=0.5)
        self.quiz("कर्कोटक नागयुवकको छाप्रोबाट दमयन्ती कसरी उम्किइन् ?",
                  ["उससँग लडेर", "जाँड खुवाई आगो लगाएर", "शुचिभद्रको सहायताले", "नल आएर बचाएपछि"], 1,
                  "अब एउटा प्रश्न। कर्कोटक नागयुवकको छाप्रोबाट दमयन्ती कसरी उम्किइन्? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ख। उनले नागलाई धेरै जाँड खुवाएर अचेत बनाइन्, र ढोकामा आगो लगाएर भागिन्। लडेर होइन, बुद्धिले। शुचिभद्र त धेरै पछि भेटिन्छन्, र नल कथाभरि आउँदै आउँदैनन्।")

    def k3(self):
        tag = self.ktag(3, "रूप बिगार्नुको अर्थ", MINT)
        self.play(FadeIn(tag), run_time=0.3)
        d = self.dama(2.8).move_to([-4.0, -3.2, 0], aligned_edge=DOWN)
        stick = Line(d.get_center() + RIGHT * 0.7 + DOWN * 1.4, d.get_center() + RIGHT * 0.85 + UP * 1.2, color="#8A6A4A", stroke_width=7)
        dust = VGroup(*[Dot(d.head.get_center() + np.array([np.cos(a), np.sin(a), 0]) * 0.33, radius=0.05, color="#8A7A5A") for a in np.linspace(0.2, PI - 0.2, 9)])
        lab = VGroup(C.pill("धुलोले जगल्टा", "#C9A46A", 24), C.pill("अनुहारमा हिलो", "#C9A46A", 24), C.pill("हातमा लट्ठी", "#C9A46A", 24)).arrange(DOWN, buff=0.25).move_to([-0.6, -0.8, 0])
        with self.say("तेस्रो खण्डमा तीन दिनको एकान्त यात्रा छ। दमयन्ती अत्यन्त सुन्दरी हुन्। तर जङ्गलमा त्यही रूप उनका लागि खतरा बनिसकेको थियो।"):
            self.play(FadeIn(d, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(d, color=GOLD, scale_factor=1.04), run_time=1.0)
        with self.say("त्यसैले उनले केशलाई धुलोले मुसारेर जगल्टा बनाइन्, मुहारमा हिलो दलिन्, र हातमा लट्ठी लिइन्, ताकि अजिङ्गर, कर्कोटक वा निषादयुवकले उनलाई कुरूप र बौलाही ठानून्, आक्रमण नगरून्।"):
            self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in dust], lag_ratio=0.1), run_time=0.8)
            self.play(d.head.animate.set_color("#7A5A3A"), run_time=0.6)
            self.play(Create(stick), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(l, shift=LEFT * 0.2) for l in lab], lag_ratio=0.3), run_time=1.2)
        st = C.pill("आत्महीनता होइन, आत्मरक्षाको रणनीति", MINT, 28).move_to([2.6, 1.0, 0])
        with self.say("ध्यान दिनुहोस्, यो आत्महीनता होइन। यो आत्मरक्षाको रणनीति हो।"):
            self.play(FadeIn(st, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(lab, st)), run_time=0.4)
        q = C.show_quote(self, ["मानिसको परिचय उसको शरीरले भन्दा पनि", "उसको मस्तिष्क र हृदयले दिन्छ"],
                         "र यही बेला उनी एउटा गहिरो कुरा बुझ्छिन्। मानिसको परिचय उसको शरीरले भन्दा पनि उसको मस्तिष्क र हृदयले दिन्छ।",
                         color=MINT, size=38, where=[2.3, 1.5, 0], keep=True, hl={"शरीरले": th.MUTED, "मस्तिष्क": SKY, "हृदयले": PINK})
        lamp = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=SKY, fill_opacity=0.12).move_to(d.head) for r in (0.45, 0.65, 0.9)])
        hrt = C.heart(0.35, color=PINK).move_to(d.get_center() + UP * 0.35)
        hglow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=PINK, fill_opacity=0.12).move_to(hrt) for r in (0.4, 0.6, 0.85)])
        mean = para("बाहिरी रूप बिग्रे पनि भित्री प्रेम र बुद्धि झन् उज्यालो हुन्छ। साँचो परिचय सोच, विवेक, चरित्र र भावनाले दिन्छ।", width=6.6, size=26, color=th.INK).move_to([2.6, -1.4, 0])
        with self.say("अर्थात्, मानिस सुन्दर देखिनु वा नदेखिनुले उसको वास्तविक परिचय दिँदैन। उसको सोच, विवेक, चरित्र र भावना नै साँचो परिचय हो। दमयन्तीको शरीर क्षतविक्षत भयो, तर नलप्रतिको प्रेम र बुद्धि झन् कोमल र दृढ भयो।"):
            self.play(d.animate.set_opacity(0.45), run_time=0.6)
            self.play(FadeIn(lamp, scale=0.5), FadeIn(hglow, scale=0.5), FadeIn(hrt, scale=0.5), run_time=1.0)
            self.play(FadeIn(mean, shift=UP * 0.2), run_time=0.8)
        self.play(FadeOut(VGroup(q, d, stick, dust, lamp, hglow, hrt, mean, tag)), run_time=0.5)

    def k4(self):
        tag = self.ktag(4, "आकाश र हृदय", SKY)
        nt = self.night()
        mw = C.milky_way(180, seed=3, a=(-7.0, -2.0), b=(3.0, 3.4))
        dh = VGroup(Star(n=5, outer_radius=0.16, inner_radius=0.07, stroke_width=0, fill_color=WHITE, fill_opacity=1),
                    *[Circle(radius=r, stroke_width=0, fill_color=WHITE, fill_opacity=0.1) for r in (0.25, 0.4)]).move_to([-4.2, 2.6, 0])
        sp = C.saptarishi(0.9).move_to([-2.0, 1.4, 0])
        l1 = T("ध्रुवतारा", size=22, color=th.BODY).next_to(dh, DOWN, buff=0.1)
        l2 = T("सप्तर्षि", size=22, color=th.BODY).next_to(sp, DOWN, buff=0.15)
        l3 = T("आकाशगङ्गा", size=22, color=th.BODY).move_to([0.6, 2.2, 0])
        rock = Polygon([-6.4, -3.25, 0], [-6.0, -2.6, 0], [-3.4, -2.5, 0], [-3.0, -3.25, 0], stroke_width=0, fill_color="#3A3A4A", fill_opacity=1)
        d = self.dama(1.8).rotate(-PI / 2).move_to([-4.7, -2.3, 0])
        with self.say("चौथो खण्ड कथाको सबैभन्दा काव्यात्मक क्षण हो। तेस्रो रात, खेतको ढुङ्गामा सुत्दा, दमयन्ती माथि आकाश हेर्छिन्।"):
            self.play(FadeIn(nt), FadeIn(tag), FadeIn(rock), FadeIn(d), run_time=0.8)
            if self.hud is not None:
                self.bring_to_front(self.hud)
        with self.say("ध्रुवतारा, सप्तर्षि, पाँचतारे मण्डल, र आकाशगङ्गा। लेखक भन्छन्, आकाशगङ्गा दमयन्तीका दृष्टिमा सङ्गीतमय हुन थाल्यो। उनी वियोगको गीत गाउन थाल्छिन्।"):
            self.play(FadeIn(dh, scale=0.5), FadeIn(l1), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, scale=0.3) for x in sp[1]], lag_ratio=0.15), Create(sp[0]), FadeIn(l2), run_time=1.2)
            self.play(FadeIn(mw, lag_ratio=0.01), FadeIn(l3), run_time=1.5)
            notes = VGroup(*[C.note_glyph(GOLD, 0.25).move_to(d.get_center() + RIGHT * (0.4 + 0.5 * k) + UP * (0.5 + 0.35 * k)) for k in range(3)])
            self.play(LaggedStart(*[FadeIn(nn, shift=UP * 0.3) for nn in notes], lag_ratio=0.3), run_time=1.0)
        hbox = C.box(4.0, 3.2, color=PINK).move_to([4.3, 0.2, 0])
        hrt = C.heart(0.9, color=PINK).move_to([4.3, 0.5, 0])
        hl = T("दमयन्तीको हृदय", size=24, color=PINK).move_to([4.3, -1.0, 0])
        c1 = C.cloud(2.4, color="#4A5070", opacity=0.75).move_to([-6.5, 1.8, 0])
        c2 = C.cloud(1.6, color="#6A6F8E", opacity=0.75).move_to([2.5, 1.0, 0])
        with self.say("तर बिस्तारै पातला बादलले त्यो उज्यालो आकाशलाई धमिलो पार्छन्। त्यसै गरी, आशाले भरिएको दमयन्तीको हृदयलाई पनि वियोगको पीडाले बेला बेला धमिलो पारिरहेको छ।"):
            self.play(FadeIn(hbox), FadeIn(hrt), FadeIn(hl), run_time=0.6)
            self.play(c1.animate.move_to([-2.5, 1.9, 0]), c2.animate.move_to([4.3, 0.6, 0]), mw.animate.set_opacity(0.3), hrt.animate.set_opacity(0.45), run_time=3.0)
        same = C.pill("बाहिरी प्रकृति र भित्री मनको मेल", GOLD, 28).move_to([1.0, -1.9, 0])
        with self.say("आकाशमा उज्यालो र धमिलोपनको आवतजावत, र हृदयमा आशा र निराशाको आवतजावत। बाहिरी प्रकृति र भित्री मनको यही समानता परीक्षामा सोधिन्छ।"):
            self.play(FadeIn(same, scale=0.8), run_time=0.6)
            self.play(c2.animate.shift(RIGHT * 2).set_opacity(0.2), hrt.animate.set_opacity(1), run_time=1.5)
        self.play(FadeOut(VGroup(same, hbox, hrt, hl, c1, c2, notes)), run_time=0.4)
        voice = C.kblock(["अझै उत्तरतिर हिँड,", "तिम्रो नल भेटिनेछन्"], size=44, hl={"उत्तरतिर": GOLD, "नल": TEAL}).move_to([2.6, -0.4, 0])
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=GOLD, fill_opacity=0.05).move_to(voice) for r in (1.5, 2.2, 3.0)])
        with self.say("त्यसपछि उनी ऋषिका आश्रमको सुखद सपना देख्छिन्, जहाँ एउटा आवाज सुन्छिन्, अझै उत्तरतिर हिँड, तिम्रो नल भेटिनेछन्। निराशाको बिचमा यो आशाको सन्देश हो।"):
            self.play(FadeIn(glow, scale=0.5), run_time=0.6)
            C.type_in(self, voice, run_time=2.0)
        self.play(FadeOut(VGroup(nt, mw, dh, sp, l1, l2, l3, rock, d, voice, glow, tag)), run_time=0.6)

    def k5(self):
        tag = self.ktag(5, "शुचिभद्रको सार्थ", GOLD)
        self.play(FadeIn(tag), run_time=0.3)
        sun = C.sun(0.5).move_to([5.0, 2.2, 0])
        grd = Line([-7, -3.2, 0], [7, -3.2, 0], color="#4A5A3A", stroke_width=6)
        d = self.dama(1.8).move_to([4.0, -3.2, 0], aligned_edge=DOWN)
        caravan = VGroup()
        for k in range(4):
            caravan.add(C.man(1.6, coat=[th.PANEL_EDGE, "#7A5A3A", "#3E6A8A", "#6A4A6A"][k], topi=True).move_to([-6.5 - 1.1 * k, -3.2, 0], aligned_edge=DOWN))
        bl = C.bell(0.35).move_to([-6.0, -0.9, 0])
        with self.say("पाँचौँ खण्डमा नयाँ आशा जाग्छ। बिहान स्नान गरी, केरा खाएर, उनी उत्तरतिर हिँड्छिन्। अनि टाढैबाट घन्टी बजेको सुनिन्छ। व्यापारीहरूको लस्कर, जसलाई सार्थ भनिन्छ।"):
            self.play(FadeIn(sun), Create(grd), FadeIn(d), run_time=0.7)
            self.add(caravan, bl)
            self.play(caravan.animate.shift(RIGHT * 7.0), bl.animate.shift(RIGHT * 4.0), run_time=3.0, rate_func=rate_functions.ease_out_sine)
            self.play(Wiggle(bl), run_time=0.8)
        lead = T("सार्थवाह शुचिभद्र", size=28, color=GOLD, weight="BOLD").next_to(caravan[0], UP, buff=0.25)
        gifts = VGroup(C.pill("भोजन", MINT, 26), C.pill("नयाँ वस्त्र", SKY, 26), C.pill("चेदीतिर नल भेटिन सक्छन्", GOLD, 26)).arrange(RIGHT, buff=0.3).move_to([0.5, 1.2, 0])
        with self.say("लस्करका मुखिया, अर्थात् सार्थवाह, शुचिभद्रले उनको परिचय सोध्छन्। भोजन र नयाँ वस्त्र दिन्छन्, र भन्छन्, चेदीतिर नल भेटिन सक्छन्। कठिन बेलामा मानवीय सहयोगको यो उज्यालो पक्ष हो।"):
            self.play(FadeIn(lead), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in gifts], lag_ratio=0.35), run_time=1.5)
        self.play(FadeOut(VGroup(sun, grd, d, caravan, bl, lead, gifts, tag)), run_time=0.5)

    def k6(self):
        tag = self.ktag(6, "हात्तीको आक्रमण", CORAL)
        nt = self.night()
        lake = Ellipse(width=6.0, height=1.2, stroke_width=0, fill_color="#1E4A7A", fill_opacity=1).move_to([1.5, -2.7, 0])
        lot = VGroup(*[C.lotus(0.35).move_to([x, -2.6, 0]) for x in (0.0, 1.4, 2.8)])
        tree = C.tree(4.2, color="#2E6B3A").move_to([-4.6, -3.25, 0], aligned_edge=DOWN)
        tents = VGroup(*[Triangle(stroke_width=0, fill_color="#8A7A5A", fill_opacity=1).stretch_to_fit_width(0.9).stretch_to_fit_height(0.7).move_to([x, -2.0, 0]) for x in (-2.4, -1.3)])
        lab = T("पद्मसौगन्धिक तलाउ", size=26, color=SKY).move_to([1.5, -1.65, 0])
        with self.say("छैटौँ खण्डमा कथाको चरम बिन्दु आउँछ। सार्थ पद्मसौगन्धिक तलाउको किनारमा रात बिताउँछ।"):
            self.play(FadeIn(nt), FadeIn(tag), FadeIn(lake), FadeIn(lot), FadeIn(tree), FadeIn(tents), FadeIn(lab), run_time=1.0)
            if self.hud is not None:
                self.bring_to_front(self.hud)
        d = self.dama(0.9).move_to(tree.get_center() + UP * 0.6 + LEFT * 0.1)
        other = C.woman(0.85, sari="#8A4A8A").move_to(tree.get_center() + UP * 0.1 + RIGHT * 0.35)
        with self.say("तर दमयन्ती निदाउनुअघि नै सतर्क भइसकेकी थिइन्। उनले आफूलाई पहिल्यै एउटा अग्लो रुखमा जोगाइन्, र अर्की नारीलाई पनि रुखको अर्को हाँगामा चढ्न सघाइन्।"):
            self.play(FadeIn(d, shift=UP * 0.6), run_time=0.8)
            self.play(FadeIn(other, shift=UP * 0.6), run_time=0.8)
        herd = VGroup(*[C.elephant(1.4 - 0.1 * (k % 2)).move_to([8.0 + 2.2 * k, -3.25, 0], aligned_edge=DOWN).flip() for k in range(3)])
        with self.say("मध्यरातमा जङ्गली हात्तीको बथान पानी खान आउँछ। र सुतिरहेको सार्थ कुल्चिएर नष्ट हुन्छ।"):
            self.add(herd)
            self.sfx("thud", gain=-6)
            self.play(herd.animate.shift(LEFT * 9.5), run_time=3.0, rate_func=linear)
            self.sfx("impact", gain=-8)
            self.play(tents.animate.stretch(0.2, 1, about_edge=DOWN).set_opacity(0.4), Wiggle(tree, scale_value=1.03), run_time=0.8)
        surv = C.pill(f"दश-बाह्र जना मात्र बाँचे", CORAL, 28).move_to([1.5, 1.4, 0])
        sm = C.pill("प्रत्युत्पन्नमति: तत्काल सही निर्णय", MINT, 28).move_to([1.5, 0.4, 0])
        with self.say("सार्थका दश बाह्र जना मात्र बाँचे, र दमयन्ती तीमध्ये एक थिइन्। उनको सतर्कता र तत्काल सही निर्णय गर्ने बुद्धि, अर्थात् प्रत्युत्पन्नमतिले उनलाई बचायो। जीवन र मृत्यु कति क्षणभङ्गुर छन्, यो खण्डले देखाउँछ।"):
            self.play(FadeIn(surv, scale=0.8), run_time=0.5)
            self.play(FadeIn(sm, scale=0.8), run_time=0.5)
        self.play(FadeOut(VGroup(nt, lake, lot, tree, tents, lab, d, other, herd, surv, sm, tag)), run_time=0.6)

    def k7(self):
        tag = self.ktag(7, "चेदी र सैरन्ध्री", MINT)
        self.play(FadeIn(tag), run_time=0.3)
        pal = C.palace(4.6).move_to([3.4, -3.2, 0], aligned_edge=DOWN)
        su = C.woman(1.0, sari="#8A3A5A", border=GOLD).move_to(pal.balcony.get_top() + UP * 0.02, aligned_edge=DOWN)
        lsu = T("रानी सुनन्दा", size=24, color=PINK).next_to(su, UP, buff=0.12)
        d = self.dama(1.8).move_to([-4.8, -3.2, 0], aligned_edge=DOWN)
        d.head.set_color("#7A5A3A")
        kids = VGroup(*[C.child(0.9, shirt=c).move_to([x, -3.2, 0], aligned_edge=DOWN) for x, c in ((-2.6, SKY), (-1.9, GOLD))])
        with self.say("अन्तिम खण्ड। चेदी नजिक पुग्दा दमयन्ती आमाबाट सुनेको कुरा सम्झिन्छिन्। उनकी ठुलीआमा सुनन्दा, चेदीका राजा सुबाहुकी रानी हुन्।"):
            self.play(FadeIn(pal, shift=UP * 0.3), FadeIn(d), run_time=0.8)
            self.play(FadeIn(su), FadeIn(lsu), run_time=0.5)
        with self.say("पहिचान खुल्ने डर थियो, तैपनि नल भेटिने आशामा उनी चेदी पस्छिन्। बौलाही जस्ती देखिएकी उनलाई केटाकेटीले गिज्याउँछन्। बार्दलीबाट रानी सुनन्दाले देख्छिन्, बोलाउँछिन्, र परिचय सोध्छिन्।"):
            self.play(d.animate.shift(RIGHT * 2.6), FadeIn(kids), run_time=1.2)
            self.play(*[k.animate.shift(UP * 0.25) for k in kids], rate_func=there_and_back, run_time=0.6)
            self.play(Indicate(su, color=GOLD), run_time=0.8)
        self.play(FadeOut(VGroup(pal, su, lsu, d, kids)), run_time=0.5)
        head = C.heading("दमयन्तीका तीन सर्त", color=self.color)
        conds = [("कसैको जुठो नखाने", GOLD), ("कसैको पाउ नदाब्ने", SKY), ("परपुरुषसित नबोल्ने", PINK)]
        seals = VGroup()
        for i, (t, c) in enumerate(conds):
            ring = Circle(radius=1.15, stroke_color=c, stroke_width=5, fill_color=c, fill_opacity=0.12)
            inner = Circle(radius=0.98, stroke_color=c, stroke_width=1.5)
            nb = T(self.num(i + 1), size=40, color=c, weight="BOLD").move_to(UP * 0.4)
            tx = para(t, width=1.8, size=24, color=th.INK, align="center").move_to(DOWN * 0.25)
            seals.add(VGroup(ring, inner, nb, tx).move_to([[-4.0, 0, 4.0][i], 0.3, 0]))
        with self.say("दमयन्तीले आफूलाई एक सेठकी पत्नीको सिँगारपटार गर्ने सुसारे भनेर चिनाइन्। र काम स्वीकार्नुअघि तीन सर्त राखिन्। पहिलो, कसैको जुठो नखाने। दोस्रो, कसैको पाउ नदाब्ने। तेस्रो, परपुरुषसित नबोल्ने।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for s_ in seals:
                self.sfx("impact", gain=-14)
                self.play(FadeIn(s_, scale=1.4), run_time=0.5)
                self.hold(v.dur / 4 - 0.6)
        mean = C.pill("स्वाभिमान · मर्यादा · पतिव्रता धर्मको दृढता", GOLD, 28).move_to([0, -2.2, 0])
        sair = T("सैरन्ध्री = रूपसज्जाको काममा खटिएकी सेविका", size=26, color=th.BODY).move_to([0, -2.95, 0])
        with self.say("यी सर्तले दमयन्तीको स्वाभिमान, मर्यादा र पतिव्रता धर्मको दृढता देखाउँछन्। सेविका बने पनि उनले आफ्नो आत्मसम्मान बेचिनन्। सुनन्दाले सर्त स्वीकारिन्, र दमयन्ती राजकुमारीकी सैरन्ध्री, अर्थात् रूपसज्जा गर्ने सेविका बनिन्।"):
            self.play(FadeIn(mean, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(sair), run_time=0.5)
        self.play(FadeOut(VGroup(head, seals, mean, sair, tag)), run_time=0.5)
        self.quiz("दमयन्तीले सुनन्दासामु राखेका सर्तमा कुन पर्दैन ?",
                  ["कसैको जुठो नखाने", "कसैको पाउ नदाब्ने", "परपुरुषसित नबोल्ने", "राजमहलबाहिर नजाने"], 3,
                  "एक अङ्कको प्रश्न, उल्टो तरिकाले। दमयन्तीले राखेका सर्तमा कुन पर्दैन? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर घ। राजमहलबाहिर नजाने भन्ने सर्त पाठमा छैन। तीन सर्त हुन्, जुठो नखाने, पाउ नदाब्ने, र परपुरुषसित नबोल्ने। यी तीनै उनको आत्मसम्मान र मर्यादासँग जोडिएका छन्।")

    # ------------------------------------------------------------------ part 5: characters
    def p5(self):
        self.section(4)
        center = C.node("दमयन्ती", TEAL, size=38, sub="नायिका · विदर्भकी कन्या", w=3.6).move_to([0, -0.3, 0])
        others = [
            ("नल", "पति · निषधराज · अनुपस्थित", GOLD, [-4.6, 1.9, 0], "खोजीको लक्ष्य"),
            ("पुष्कर", "नलको भाइ · जुवाडी", CORAL, [-4.9, -0.3, 0], "सपनामा"),
            ("कर्कोटक", "नागयुवक · कामुक, मदिराप्रेमी", CORAL, [-3.6, -2.55, 0], "खतरा"),
            ("शुचिभद्र", "सार्थवाह · दयालु, सहयोगी", MINT, [4.6, 1.9, 0], "सहारा"),
            ("सुनन्दा", "चेदीकी रानी · ठुलीआमा", MINT, [4.9, -0.3, 0], "आश्रय"),
            ("इन्द्रसेना र इन्द्रसेन", "छोरी र छोरा", SKY, [3.6, -2.55, 0], "मातृत्वको सम्झना"),
        ]
        nodes, links = [], []
        for nm, sub, c, pos, rel in others:
            nd = C.node(nm, c, size=28, sub=sub, w=4.1, h=1.0).move_to(pos)
            nodes.append(nd)
            lk = C.link(nd, center, color=c, label=rel, size=20)
            if nm == "नल":
                lk[0].set_stroke(opacity=0.5)
            links.append(lk)
        with self.say("अब पात्रहरू। कथाको केन्द्रमा दमयन्ती छिन्, कथाकी नायिका। बाँकी सबै पात्र उनकै वरिपरि घुम्छन्।"):
            self.play(FadeIn(center, scale=0.7), run_time=0.6)
        narr = ["नल, निषधका राजा र दमयन्तीका पति। उनी पाठमा प्रत्यक्ष आउँदैनन्, तर पूरा कथा उनकै खोजीमा अघि बढ्छ। उनी केन्द्रीय तर अनुपस्थित पात्र हुन्।",
                "पुष्कर, नलको जुवाडी भाइ, जो सपनामा मात्र आउँछ।",
                "कर्कोटक नागयुवक, कामुक, बलजफ्ती गर्ने, तर मूर्ख र मदिराप्रेमी। उसैको कमजोरीले दमयन्ती उम्किन्छिन्।",
                "शुचिभद्र, व्यापारी लस्करका मुखिया, दयालु र व्यवहारकुशल। उनी कुबेरका मित्र मणिभद्रको कुलमा जन्मेका हुन्।",
                "सुनन्दा, चेदीराज सुबाहुकी रानी र दमयन्तीकी ठुलीआमा। हेर्नेबित्तिकै मानिसको ओज ठम्याउने दयालु वृद्धा।",
                "र इन्द्रसेना र इन्द्रसेन, नल दमयन्तीका छोरी र छोरा, जसको सम्झनाले दमयन्तीको मातृत्व झल्काउँछ।"]
        for nd, lk, n_ in zip(nodes, links, narr):
            with self.say(n_):
                self.play(FadeIn(nd, scale=0.8), run_time=0.5)
                self.play(GrowArrow(lk[0]), FadeIn(lk[1:]), run_time=0.5)
        key = VGroup(C.pill("सहयोगी", MINT, 22), C.pill("खतरा / बाधा", CORAL, 22), C.pill("परिवार", SKY, 22)).arrange(RIGHT, buff=0.3).move_to([0, 2.95, 0])
        with self.say("रङ हेर्नुहोस्। हरियो सहयोगी, रातो खतरा वा बाधा, र निलो परिवार।"):
            self.play(FadeIn(key), run_time=0.5)
        self.play(FadeOut(VGroup(center, *nodes, *links, key)), run_time=0.5)
        self.traits()

    def traits(self):
        head = C.heading("दमयन्तीको चरित्र: पाँच बुँदा", color=self.color)
        d = self.dama(2.3).move_to([0, -3.1, 0], aligned_edge=DOWN)
        glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=TEAL, fill_opacity=0.06).move_to(d) for r in (1.4, 2.0)])
        tr = [("अटुट प्रेम", "जताततै नलको रूप देख्ने", PINK, [-4.4, 1.25, 0]),
              ("बुद्धि र धैर्य", "कर्कोटकलाई बुद्धिले जित्ने", GOLD, [4.4, 1.25, 0]),
              ("आत्मनियन्त्रण", "भोक, डर र निद्रामा पनि संयम", SKY, [-4.4, -1.4, 0]),
              ("स्वाभिमान", "तीन सर्त", MINT, [4.4, -1.4, 0]),
              ("आशा र सङ्कल्प", "जसरी भए पनि नल भेटिने विश्वास", CORAL, [0, 1.25, 0])]
        cards = [C.card(a, b, c, w=3.7, h=1.7, hsize=30, bsize=23).move_to(p) for a, b, c, p in tr]
        with self.say("परीक्षामा सबैभन्दा धेरै सोधिने प्रश्न, दमयन्तीको चरित्र चित्रण। यसलाई पाँच बुँदामा सम्झनुहोस्।"):
            self.play(FadeIn(head), FadeIn(glow), FadeIn(d, shift=UP * 0.2), run_time=0.8)
        narrs = ["एक, अटुट प्रेम। पतिले छाडे पनि उनी नललाई घृणा गर्दिनन्, बरु जताततै नलकै रूप देख्छिन्।",
                 "दुई, बुद्धि र धैर्य। कर्कोटकलाई बलले होइन, बुद्धिले जित्छिन्, र हात्तीको आक्रमणमा समयमै रुख चढ्छिन्।",
                 "तीन, आत्मनियन्त्रण। भोक, डर र थकानमा पनि उनी संयम गुमाउँदिनन्।",
                 "चार, स्वाभिमान। सेविका बन्दा पनि तीन सर्त राखेर आत्मसम्मान जोगाउँछिन्।",
                 "र पाँच, आशा र सङ्कल्प। जसरी भए पनि नल भेटिन्छन् भन्ने विश्वास उनी कहिल्यै छाड्दिनन्।"]
        for c, n_ in zip(cards, narrs):
            with self.say(n_):
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=(ORIGIN - c.get_center()) * -0.05, scale=0.85), run_time=0.6)
        with self.say("यी पाँचै गुणको प्रमाण कथाबाटै दिनुहोस्, अनि उत्तर पूर्ण हुन्छ।"):
            self.play(Indicate(d, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.play(FadeOut(VGroup(head, glow, d, *cards)), run_time=0.5)

    # ------------------------------------------------------------------ part 6: theme & critique
    def p6(self):
        self.section(5)
        block = C.kblock(["नारी प्रेम र सङ्घर्षकी प्रतिमूर्ति हुन्;", "दृढ सङ्कल्प, बुद्धि र धैर्य भएको मानिस", "जतिसुकै कठिन परिस्थितिमा पनि हार मान्दैन।"],
                         size=38, hl={"प्रेम": PINK, "सङ्घर्षकी": GOLD, "सङ्कल्प,": MINT}, buff=0.35).move_to(UP * 0.3)
        fr = C.quote_frame(block, GOLD)
        with self.say("कथाको मूल भाव। नारी प्रेम र सङ्घर्षकी प्रतिमूर्ति हुन्। दृढ सङ्कल्प, बुद्धि र धैर्य भएको मानिस जतिसुकै कठिन परिस्थितिमा पनि हार मान्दैन।") as v:
            self.play(FadeIn(fr), run_time=0.5)
            C.type_in(self, block, run_time=min(v.dur * 0.7, 6))
        self.play(FadeOut(VGroup(fr, block)), run_time=0.5)
        head = C.heading("मूल भावका तीन आयाम", color=self.color)
        dims = [("वियोगको पीडा र प्रेमको गहिराइ", "जताततै नल देख्नु, वियोगको गीत", PINK),
                ("नारी सङ्घर्ष", "शरीरभन्दा बुद्धि र सङ्कल्पले आत्मरक्षा", GOLD),
                ("मानवीयता", "शुचिभद्र र सुनन्दाको सहारा", MINT)]
        cards = VGroup(*[C.card(a, b, c, w=3.9, h=2.6, hsize=28, bsize=24) for a, b, c in dims]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        narrs = ["यसका तीन आयाम छन्। पहिलो, वियोगको पीडा र प्रेमको गहिराइ। दमयन्ती जताततै नल देख्छिन्।",
                 "दोस्रो, नारी सङ्घर्ष। असुरक्षित जङ्गलमा एक्ली नारीले शरीरभन्दा बुद्धि र सङ्कल्पबाट आफूलाई जोगाउँछिन्।",
                 "तेस्रो, मानवीयता। शुचिभद्र र सुनन्दा जस्ता पात्रले कठिन बेलामा सहारा दिन्छन्।"]
        self.play(FadeIn(head), run_time=0.4)
        for c, n_ in zip(cards, narrs):
            with self.say(n_):
                self.play(FadeIn(c, shift=UP * 0.3), run_time=0.6)
        self.play(FadeOut(VGroup(head, cards)), run_time=0.5)
        head = C.heading("समीक्षा", color=self.color)
        good = VGroup(T("बलियो पक्ष", size=32, color=MINT, weight="BOLD"),
                      *[C.pill(t, MINT, 23) for t in ("देवी होइन, मानवीय र यथार्थ नायिका", "प्रकृति र मनको समानान्तर चित्रण", "बलको सट्टा बुद्धि: नारी सशक्तिकरण")]).arrange(DOWN, buff=0.3)
        bad = VGroup(T("कमजोर पक्ष", size=32, color=CORAL, weight="BOLD"),
                     *[C.pill(t, CORAL, 23) for t in ("तत्सम शब्दले भारी भाषा", "बिचबाट सुरु र अन्त्य: अपूर्ण", "कर्कोटक सरल खलनायक")]).arrange(DOWN, buff=0.3)
        good.move_to([-3.4, -0.1, 0])
        bad.move_to([3.4, -0.1, 0])
        div = Line([0, 2.0, 0], [0, -2.4, 0], color=th.FAINT, stroke_width=2)
        with self.say("समीक्षाका लागि दुवै पक्ष। बलियो पक्ष, लेखकले पौराणिक नायिकालाई देवी नबनाई भोक, डर र निद्रा भएकी एक्ली नारीका रूपमा देखाएका छन्, त्यसैले पाठक उनीसँग जोडिन्छ। प्रकृति र भित्री भावको समानान्तर चित्रण सुन्दर छ। र बलको सट्टा बुद्धिले जित्ने प्रसङ्गले नारी सशक्तिकरणको सन्देश दिन्छ।"):
            self.play(FadeIn(head), Create(div), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in good], lag_ratio=0.35), run_time=2.0)
        with self.say("कमजोर पक्ष, भाषा तत्सम शब्दले भारी छ, सामान्य पाठकलाई अलि कठिन हुन्छ। कथा प्रसङ्गको बिचबाट सुरु भई बिचमै टुङ्गिन्छ, त्यसैले अपूर्ण लाग्न सक्छ। र कर्कोटकलाई पूर्ण खलनायकका रूपमा सरल ढङ्गले देखाइएको छ।"):
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.2) for x in bad], lag_ratio=0.35), run_time=2.0)
        with self.say("तैपनि समग्रमा यो दृढ सङ्कल्प, नारी साहस र वियोगी प्रेमको सुन्दर कथा हो, जसले सङ्कटमा हार नमान्न प्रेरणा दिन्छ।"):
            self.play(Circumscribe(good, color=MINT), run_time=1.2)
        self.play(FadeOut(VGroup(head, good, bad, div)), run_time=0.5)

    # ------------------------------------------------------------------ part 7: elements & style
    def p7(self):
        self.section(6)
        d = self.callout("key", "कुनै एउटा घटना वा जीवनको एउटा पक्षलाई सङ्क्षेपमा, रोचक ढङ्गले, पात्र, परिवेश र संवादसहित प्रस्तुत गर्ने गद्य रचनालाई कथा भनिन्छ।", width=11, size=30).move_to(ORIGIN)
        with self.say("पहिले, कथा भनेको के हो? कुनै एउटा घटना वा जीवनको एउटा पक्षलाई सङ्क्षेपमा, रोचक ढङ्गले, पात्र, परिवेश र संवादसहित प्रस्तुत गर्ने गद्य रचनालाई कथा भनिन्छ।"):
            self.play(FadeIn(d, shift=UP * 0.3), run_time=0.6)
        self.play(FadeOut(d), run_time=0.4)
        hub = VGroup(Circle(radius=1.0, fill_color=self.color, fill_opacity=0.2, stroke_color=self.color, stroke_width=4),
                     T("कथा", size=44, color=th.INK, weight="BOLD")).move_to([0, -0.2, 0])
        els = [("कथावस्तु", "नलको खोजीदेखि सैरन्ध्रीसम्म"), ("पात्र", "दमयन्ती मुख्य; अरू सहायक"), ("परिवेश", "जङ्गल, छाप्रो, तलाउ, चेदी"),
               ("संवाद", "कर्कोटक, शुचिभद्र, सुनन्दासँग"), ("द्वन्द्व", "बाह्य र आन्तरिक"), ("उद्देश्य", "सङ्कल्प र नारी सङ्घर्षको महिमा"),
               ("शैली", "वर्णनात्मक, चित्रात्मक"), ("चरम बिन्दु", "हात्तीको आक्रमण")]
        cols = [GOLD, TEAL, MINT, SKY, CORAL, PINK, "#C5F05C", GOLD]
        spokes, cards = VGroup(), VGroup()
        for i, ((a, b), c) in enumerate(zip(els, cols)):
            ang = PI / 2 - i * TAU / 8
            pos = hub.get_center() + np.array([np.cos(ang) * 4.6, np.sin(ang) * 2.45, 0])
            cd = VGroup(T(a, size=26, color=c, weight="BOLD"), T(b, size=20, color=th.BODY)).arrange(DOWN, buff=0.08)
            bx = C.box(cd.width + 0.4, cd.height + 0.25, color=c).move_to(pos)
            cd.move_to(bx)
            cards.add(VGroup(bx, cd))
            spokes.add(Line(hub.get_center() + np.array([np.cos(ang), np.sin(ang), 0]) * 1.0, bx.get_center(), color=c, stroke_width=2, stroke_opacity=0.6))
        cards.set_z_index(1)
        with self.say("कथाका तत्त्वलाई यो पाङ्ग्रामा हेरौँ। कथावस्तु, नलको खोजीदेखि सैरन्ध्री बन्नुसम्मको घटनाक्रम। पात्र, दमयन्ती मुख्य, र कर्कोटक, शुचिभद्र, सुनन्दा सहायक। परिवेश, जङ्गल, छाप्रो, खेतको ढुङ्गा, तलाउ र चेदी नगर। संवाद, कर्कोटक, शुचिभद्र र सुनन्दासँग।") as v:
            self.play(GrowFromCenter(hub), run_time=0.5)
            for i in range(4):
                self.play(Create(spokes[i]), FadeIn(cards[i], scale=0.8), run_time=0.5)
                self.hold(v.dur / 4 - 0.7)
        with self.say("द्वन्द्व, बाह्य र आन्तरिक दुवै। उद्देश्य, दृढ सङ्कल्प र नारी सङ्घर्षको महिमा देखाउनु। शैली, वर्णनात्मक र चित्रात्मक। र चरम बिन्दु, हात्तीको आक्रमणमा सार्थको विनाश र दमयन्तीको बाँच्नु।") as v:
            for i in range(4, 8):
                self.play(Create(spokes[i]), FadeIn(cards[i], scale=0.8), run_time=0.5)
                self.hold(v.dur / 4 - 0.7)
        self.play(FadeOut(VGroup(hub, spokes, cards)), run_time=0.5)
        head = C.heading("द्वन्द्व", color=self.color)
        ext = VGroup(T("बाह्य द्वन्द्व", size=32, color=CORAL, weight="BOLD"), *[C.pill(t, CORAL, 24) for t in ("कर्कोटक", "जङ्गली हात्ती", "जङ्गलको भय")]).arrange(DOWN, buff=0.3).move_to([-3.4, -0.2, 0])
        inn = VGroup(T("आन्तरिक द्वन्द्व", size=32, color=SKY, weight="BOLD"), *[C.pill(t, SKY, 24) for t in ("वियोगको पीडा", "आशा र निराशा", "पहिचान खुल्ने डर")]).arrange(DOWN, buff=0.3).move_to([3.4, -0.2, 0])
        with self.say("द्वन्द्व दुई किसिमको छ। बाहिरबाट आउने, कर्कोटक, हात्ती र जङ्गलको भय। र मनभित्रको, वियोगको पीडा, आशा र निराशाको उतारचढाव, र पहिचान खुल्ने डर।"):
            self.play(FadeIn(head), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in ext], lag_ratio=0.3), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in inn], lag_ratio=0.3), run_time=1.5)
        self.play(FadeOut(VGroup(head, ext, inn)), run_time=0.5)
        self.quiz("'विरहिणी दमयन्ती' लाई पौराणिक कथा किन भनिन्छ ?",
                  ["वास्तविक इतिहासका व्यक्ति भएकाले", "पात्र र घटना पुराण वा महाभारतबाट आएकाले", "पुरानो भाषामा लेखिएकाले", "लेखक पुराना भएकाले"], 1,
                  "विधासम्बन्धी प्रश्न। यो कथालाई पौराणिक कथा किन भनिन्छ? रोकिनुहोस् र सोच्नुहोस्।",
                  "सही उत्तर ख। नल, दमयन्ती, कर्कोटक र कुबेर जस्ता पात्र र घटना पुराण र महाभारतबाट आएका छन्। क विकल्पले ऐतिहासिक कथाको परिभाषा दिन्छ, पौराणिक होइन। पौराणिक भए पनि यसको सन्देश आजको समाजसँग जोडिन्छ।")
        self.style()

    def style(self):
        head = C.heading("भाषाशैली", color=self.color)
        sty = VGroup(C.pill("वर्णनात्मक", GOLD, 28), C.pill("चित्रात्मक", SKY, 28), C.pill("मनोवैज्ञानिक", PINK, 28)).arrange(RIGHT, buff=0.35).move_to(UP * 1.9)
        with self.say("शैली वर्णनात्मक, चित्रात्मक र मनोवैज्ञानिक छ। लेखक घटना मात्र भन्दैनन्, दमयन्तीको भित्री मनको उतारचढाव पनि देखाउँछन्।"):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in sty], lag_ratio=0.3), run_time=1.5)
        words = ["विदीर्ण", "भस्मीभूत", "विक्षिप्त", "शिथिल", "किंकर्तव्यविमूढ", "धूमिल", "संयत"]
        rng = np.random.default_rng(4)
        wg = VGroup(*[C.pill(w, GOLD, 26) for w in words])
        targets = [[-4.8, 0.6, 0], [-1.6, 0.6, 0], [1.6, 0.6, 0], [4.8, 0.6, 0], [-3.2, -0.5, 0], [0.4, -0.5, 0], [3.6, -0.5, 0]]
        for w, t in zip(wg, targets):
            w.move_to(np.array(t) + UP * 4)
        tad = T("तद्भव: आगो, आँखा, हात्ती, रुख", size=26, color=SKY).move_to([0, -1.6, 0])
        note = C.pill("तत्सम शब्द प्रधान", GOLD, 28).move_to([0, -2.5, 0])
        with self.say("शब्दस्रोत हेर्दा, तत्सम शब्द प्रधान छन्। विदीर्ण, भस्मीभूत, विक्षिप्त, शिथिल, किंकर्तव्यविमूढ, धूमिल, संयत। साथै आगो, आँखा, हात्ती, रुख जस्ता तद्भव शब्द पनि छन्।"):
            self.play(LaggedStart(*[w.animate.move_to(t) for w, t in zip(wg, targets)], lag_ratio=0.12), run_time=2.0, rate_func=rate_functions.ease_out_bounce)
            self.play(FadeIn(tad), FadeIn(note), run_time=0.6)
        self.play(FadeOut(VGroup(sty, wg, tad, note)), run_time=0.5)
        rows = [("उपमा", "बौलाही झैँ प्रियतम नल !", {"झैँ": GOLD}, GOLD),
                ("रूपक", "वियोगको उत्कट ज्वाला", {"ज्वाला": CORAL}, CORAL),
                ("मानवीकरण", "आकाशगङ्गा दमयन्तीका दृष्टिमा सङ्गीतमय हुन थाल्यो", {"सङ्गीतमय": SKY}, SKY),
                ("विरोधाभास", "भोकी र अर्धनग्न, तर सधैँ अपराजिता", {"अपराजिता": MINT}, MINT)]
        grp = VGroup()
        for a, b, hl, c in rows:
            lab = T(a, size=28, color=c, weight="BOLD")
            ln = C.kline(b, size=32, color=th.INK, hl=hl, weight="NORMAL")
            grp.add(VGroup(lab, ln))
        for g in grp:
            g[1].next_to(g[0], RIGHT, buff=0.5)
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.3)
        for g in grp:
            g[1].align_to(grp, LEFT).shift(RIGHT * 2.3)
        narrs = ["अलङ्कार हेरौँ। उपमा, बौलाही झैँ प्रियतम नल। झैँ ले वियोगको चरम अवस्थालाई बौलाहीसँग तुलना गर्छ।",
                 "रूपक, वियोगको उत्कट ज्वाला। यहाँ वियोगलाई सिधै आगो नै भनिएको छ।",
                 "मानवीकरण, आकाशगङ्गा दमयन्तीका दृष्टिमा सङ्गीतमय हुन थाल्यो। निर्जीव आकाशगङ्गामा सङ्गीतको गुण।",
                 "र विरोधाभास। भोकी र अर्धनग्न, आफूलाई पराजित अनुभव गर्दा पनि, सधैँ अपराजिता।"]
        for g, n_ in zip(grp, narrs):
            with self.say(n_):
                self.play(FadeIn(g[0], shift=RIGHT * 0.2), run_time=0.4)
                C.type_in(self, VGroup(g[1]), run_time=1.2)
        self.play(FadeOut(VGroup(head, grp)), run_time=0.5)
        self.tip("उपमामा 'झैँ, जस्तै' ले तुलना गर्छ; रूपकमा तुलना नगरी सिधै उही भनिन्छ: 'वियोगको ज्वाला'।",
                 "उपमा र रूपकमा धेरैले अलमल गर्छन्। उपमामा झैँ, जस्तै जस्ता शब्दले तुलना गरिन्छ। रूपकमा तुलना होइन, सिधै उही भनिन्छ, जस्तै वियोगको ज्वाला।")

    # ------------------------------------------------------------------ part 8: exam frames
    def p8(self):
        self.section(7)
        head = C.heading("परीक्षाले खोज्ने तीन कुरा", color=self.color)
        kinds = VGroup(C.card("घटनाक्रम", "कर्कोटकदेखि सैरन्ध्रीसम्म क्रम मिलाउने", SKY, w=3.9, h=2.4),
                       C.card("चरित्र र सङ्कल्प", "दमयन्तीको चरित्र, दृढ सङ्कल्प र सङ्घर्ष", GOLD, w=3.9, h=2.4),
                       C.card("कथांशको बोध", "'मानिसको परिचय…' जस्ता अंशको तात्पर्य", MINT, w=3.9, h=2.4)).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        with self.say("यस पाठबाट पाठगत बोधका आठ र समीक्षात्मक प्रश्नका आठ अङ्कसम्म सोधिन सक्छ। प्रायः तीन किसिमका प्रश्न आउँछन्। घटनाक्रम, चरित्र र सङ्कल्पको समीक्षा, र कथांशको तात्पर्य। तेस्रो प्रकारमा अनुच्छेदको वाक्य सोझै नसार्नुहोस्, आफ्नै भाषामा लेख्नुहोस्।") as v:
            self.play(FadeIn(head), run_time=0.4)
            for k in kinds:
                self.play(FadeIn(k, shift=UP * 0.3), run_time=0.5)
                self.hold(v.dur / 3 - 0.7)
        self.play(FadeOut(VGroup(head, kinds)), run_time=0.5)
        self.sequence()
        f = C.answer_frame(self, f"चरित्र चित्रणको ढाँचा  [{self.num(8)}]", [
            ("भूमिका", "मदनमणि दीक्षितको 'विरहिणी दमयन्ती' कथाकी नायिका, नलकी पत्नी, विदर्भकी कन्या, केन्द्रीय पात्र।",
             "अब आठ अङ्कको चरित्र चित्रण। भूमिकामा लेखक, कथा र दमयन्तीको परिचय दिनुहोस्। उनी नायिका, नलकी पत्नी र विदर्भकी कन्या हुन्।"),
            ("अटुट प्रेमिका", "छाडिए पनि घृणा होइन; वनका फूल, पात, पशुमा नलको रूप।",
             "पहिलो बुँदा, अटुट प्रेमिका। छाडिए पनि घृणा गरिनन्, जताततै नल देखिन्।"),
            ("बुद्धिमती", "कर्कोटकलाई जाँड खुवाई आगो लगाएर उम्किनु; हात्तीबाट रुख चढेर बच्नु।",
             "दोस्रो, बुद्धिमती र प्रत्युत्पन्नमति। कर्कोटक र हात्तीका प्रसङ्ग उदाहरण दिनुहोस्।"),
            ("साहसी, संयमी", "तीन दिन एक्लै जङ्गल पार; भोक र थकानमा पनि आत्मनियन्त्रण।",
             "तेस्रो, साहसी र आत्मनियन्त्रित। तीन दिनको एकान्त यात्रा।"),
            ("स्वाभिमानी", "सैरन्ध्री बन्दा पनि तीन सर्त।",
             "चौथो, स्वाभिमानी। तीन सर्त।"),
            ("संवेदनशील", "ताराले मोहित हुनु, वियोगको गीत गाउनु।",
             "पाँचौँ, संवेदनशील र काव्यात्मक हृदयकी। ताराको रात र वियोगको गीत।"),
            ("निष्कर्ष", "प्रेम, बुद्धि, साहस र स्वाभिमानको संयोग; विवेक र सङ्कल्प नछाड्ने सन्देश।",
             "र निष्कर्षमा भन्नुहोस्, दमयन्ती प्रेम, बुद्धि, साहस र स्वाभिमानको सुन्दर संयोग हुन्।"),
        ], color=GOLD, size=22, top=2.45)
        self.wait(0.8)
        self.play(FadeOut(f), run_time=0.5)
        f = C.answer_frame(self, f"कथांशको तात्पर्य: 'मानिसको परिचय…'  [{self.num(3)}]", [
            ("सन्दर्भ", "आक्रमणकारीबाट जोगिन दमयन्तीले रूप बिगारेको प्रसङ्ग।",
             "अन्तमा तीन अङ्कको कथांश प्रश्न, मानिसको परिचय शरीरले भन्दा मस्तिष्क र हृदयले दिन्छ। पहिले सन्दर्भ, दमयन्तीले रूप बिगारेको प्रसङ्ग।"),
            ("अर्थ", "बाहिरी रूपले होइन; सोच, विवेक, चरित्र र भावनाले साँचो परिचय दिन्छ।",
             "त्यसपछि अर्थ। बाहिरी रूपले होइन, सोच, विवेक, चरित्र र भावनाले मानिसको साँचो परिचय दिन्छ।"),
            ("निचोड", "शरीर क्षतविक्षत भए पनि दमयन्तीको बुद्धि र प्रेम झन् दृढ भए।",
             "र निचोड। शरीर क्षतविक्षत भए पनि दमयन्तीको बुद्धि र प्रेम झन् दृढ भए।"),
        ], color=MINT, size=24, top=2.3)
        self.wait(0.8)
        self.play(FadeOut(f), run_time=0.5)

    def sequence(self):
        head = C.heading(f"घटनाको क्रम मिलाउनुहोस्  [{self.num(4)}]", color=SKY, size=36)
        ev = [("ग", "नलको खोजीमा एक्लै हिँड्नु"), ("ङ", "कर्कोटकले जबर्जस्ती बोकेर लैजानु"), ("च", "मदिरा खुवाई आगो लगाई भाग्नु"),
              ("ख", "शुचिभद्रसित भेट हुनु"), ("घ", "पद्मसौगन्धिक तलाउमा वास बस्नु"), ("क", "हात्तीको कुल्चाइबाट धेरैको ज्यान जानु"),
              ("झ", "दश-बाह्र जना मात्र बाँच्नु"), ("छ", "चेदी पुग्नु"), ("ज", "सैरन्ध्रीका रूपमा रहनु")]
        mk = []
        for lt, t in ev:
            b = C.box(5.6, 0.56, color=th.PANEL_EDGE)
            l = T(f"({lt})", size=22, color=SKY, weight="BOLD")
            tx = T(t, size=22, color=th.INK)
            VGroup(l, tx).arrange(RIGHT, buff=0.2).move_to(b).align_to(b, LEFT).shift(RIGHT * 0.2)
            mk.append(VGroup(b, l, tx))
        order_shuffled = [5, 3, 0, 8, 1, 6, 4, 7, 2]
        shuffled = [mk[i] for i in order_shuffled]
        col_pos = lambda k: np.array([-3.2 if k < 5 else 3.2, 1.75 - (k % 5) * 0.68, 0])
        for k, m in enumerate(shuffled):
            m.move_to(col_pos(k))
        with self.say("घटनाक्रमको प्रश्न यस्तो आउँछ। नौओटा घटना उल्टापाल्टा दिइन्छन्, र तपाईँले सही क्रम मिलाउनुपर्छ। हाम्रो यात्राको नक्सा सम्झनुहोस्।"):
            self.play(FadeIn(head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in shuffled], lag_ratio=0.08), run_time=1.6)
        nums = VGroup()
        anims = []
        for i, m in enumerate(mk):
            tgt = col_pos(i)
            anims.append(m.animate.move_to(tgt))
            nums.add(C.badge(self, i + 1, SKY, r=0.2).move_to(tgt + LEFT * 3.1))
        with self.say("सही क्रम हो, ग, ङ, च, ख, घ, क, झ, छ, ज। अर्थात्, नलको खोजी, कर्कोटकले बोक्नु, आगो लगाई भाग्नु, शुचिभद्रसँग भेट, तलाउमा वास, हात्तीको आक्रमण, दश बाह्र जना मात्र बाँच्नु, चेदी पुग्नु, र सैरन्ध्री बन्नु।"):
            self.sfx("whoosh", gain=-12)
            self.play(*anims, run_time=1.8, rate_func=rate_functions.ease_in_out_cubic)
            self.play(LaggedStart(*[GrowFromCenter(n_) for n_ in nums], lag_ratio=0.1), run_time=1.2)
            for m in mk:
                m[0].set_stroke(SKY)
        self.wait(0.6)
        self.play(FadeOut(VGroup(head, *mk, nums)), run_time=0.5)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            f"'विरहिणी दमयन्ती' — मदनमणि दीक्षितको पौराणिक कथा; दीक्षित: जन्म {self.num(1979)}, निधन {self.num(2076)}, 'माधवी' मदन पुरस्कार ({self.num(2039)})",
            "स्रोत: महाभारतको वनपर्व, नलोपाख्यान",
            "यात्रा: नलको खोजी → कर्कोटक → तीन दिन → सार्थ → हात्ती → चेदी",
            "तीन सर्त: जुठो नखाने, पाउ नदाब्ने, परपुरुषसित नबोल्ने",
            "दमयन्ती: प्रेम, बुद्धि, संयम, स्वाभिमान, सङ्कल्प",
            "मूल भाव: नारी प्रेम र सङ्घर्षकी प्रतिमूर्ति; सङ्कल्पले सङ्कट जितिन्छ",
            "'मानिसको परिचय शरीरले भन्दा मस्तिष्क र हृदयले दिन्छ'",
        ], "छोटो पुनरावलोकन। विरहिणी दमयन्ती मदनमणि दीक्षितको पौराणिक कथा हो, जसको स्रोत महाभारतको नलोपाख्यान हो। दमयन्तीको यात्रा, नलको खोजी, कर्कोटक, तीन दिनको यात्रा, सार्थ, हात्ती र चेदी। तीन सर्त, जुठो नखाने, पाउ नदाब्ने, परपुरुषसित नबोल्ने। दमयन्तीका गुण, प्रेम, बुद्धि, संयम, स्वाभिमान र सङ्कल्प। र सबैभन्दा ठुलो पाठ, मानिसको परिचय शरीरले होइन, मस्तिष्क र हृदयले दिन्छ।")
        self.outro("आजलाई यति नै। दमयन्ती जस्तै, सङ्कटमा पनि बुद्धि र धैर्य नछाड्नुहोस्। अर्को पाठमा हामी तारानाथ शर्माको नियात्रा, घनघस्याको उकालो काट्ता, सँगै चढ्नेछौँ। नेबियन्समा फेरि भेटौँला।")
