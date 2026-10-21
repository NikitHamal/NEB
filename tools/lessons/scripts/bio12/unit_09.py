import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _bio as B  # noqa: E402

MALE = "#4CC9F0"
FEM = "#F472B6"
RBC = "#E04848"
PARA = "#C77DFF"


def polar(r, a):
    return np.array([r * np.cos(a), r * np.sin(a), 0])


class Lesson(Lesson):
    SUBJECT = "bio"
    GRADE = 12
    UNIT = 9
    TITLE = "Human Population and Health Disorders"
    SUBTITLE = "How many of us, and what makes us ill"
    SECTIONS = ["Human population", "Health disorders"]
    NEXT = "Unit 10 · Applied Biology"

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
        ax = Axes(x_range=[1911, 2021, 20], y_range=[0, 32, 8], x_length=8.5, y_length=4.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-0.8, -0.3, 0])
        yl = T("population (millions)", size=20, color=th.MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        data = [(1911, 5.64), (1920, 5.57), (1930, 5.53), (1941, 6.28), (1952, 8.26), (1961, 9.41), (1971, 11.56), (1981, 15.02), (1991, 18.49), (2001, 23.15), (2011, 26.49), (2021, 29.16)]
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=th.AMBER) for x, y in data])
        line = VMobject(stroke_color=th.AMBER, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in data])
        with self.say("In nineteen eleven, Nepal's first census counted about five and a half million people. For forty years, almost nothing changed. Then something happened: the line turned sharply upward."):
            self.play(Create(ax), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts[:5]], lag_ratio=0.2), Create(line.copy().pointwise_become_partial(line, 0, 0.36)))
        g = T("1970s: 2.62% a year", size=26, color=th.CORAL, weight="BOLD").move_to(ax.c2p(1955, 22))
        n = T("2021: 29.2 million, growing only 0.92%", size=26, color=th.MINT, weight="BOLD").move_to(ax.c2p(1975, 30))
        with self.say("Malaria control, vaccines and clean water stopped people dying young, while families stayed large. Growth peaked at two point six percent a year. And now, the 2021 census: twenty nine million, but growing at just zero point nine two percent, the slowest in a hundred and ten years. Why the slowdown? And what makes the people who are here fall ill?"):
            self.play(Create(line), LaggedStart(*[FadeIn(p_) for p_ in pts[5:]], lag_ratio=0.2), run_time=2.4)
            self.play(FadeIn(g))
            self.play(FadeIn(n))
        nb = B.neby_in(self, "think", height=1.3)
        B.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, yl, pts, line, g, n)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Biology, Unit 9: Human Population and Health Disorders."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Two parts. Human population: the rates, growth and doubling time, pyramids, dependency, and the demographic transition, all with Nepal's real census numbers. Then health disorders: infections, malaria and HIV, immunity, non communicable and deficiency diseases.")

    # ------------------------------------------------------------------ part 1: population
    def p1(self):
        self.section(0)
        rates = VGroup(M(r"\text{CBR} = \frac{\text{live births}}{\text{mid-year population}}\times1000", size=36), M(r"\text{CDR} = \frac{\text{deaths}}{\text{mid-year population}}\times1000", size=36),
                       M(r"\text{RNI} = \text{CBR} - \text{CDR}", size=36), M(r"\text{IMR} = \frac{\text{infant deaths}}{\text{live births}}\times1000", size=36, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-1.2, 0.3, 0])
        note = para("TFR: children per woman over a lifetime. MMR: maternal deaths per 100,000 live births.", width=4.4, size=22, color=th.BODY).move_to([4.4, 0.6, 0])
        warn = para("IMR is per 1000 LIVE BIRTHS, not per 1000 people.", width=4.4, size=22, color=th.CORAL).move_to([4.4, -1.2, 0])
        with self.say("Demography is the counting of people. Births add them, deaths remove them, migration moves them. The crude birth rate is live births per thousand people a year; the crude death rate, deaths per thousand. Their difference is the rate of natural increase. And the infant mortality rate is infant deaths per thousand live births, not per thousand people. That denominator is the classic trap.") as v:
            for r_ in rates:
                self.play(Write(r_), run_time=0.8)
                self.hold(v.dur * 0.1)
            self.play(FadeIn(note))
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(rates, note, warn)))
        self.worked("A municipality of 250,000 registered 4500 live births and 1300 deaths in a year, 90 of them infants. Find CBR, CDR, RNI (%), IMR and the doubling time.",
                    [r"\text{CBR} = \tfrac{4500}{250\,000}\times1000 = 18.0;\quad \text{CDR} = \tfrac{1300}{250\,000}\times1000 = 5.2", r"\text{RNI} = 18.0 - 5.2 = 12.8 \text{ per } 1000 = 1.28\%",
                     r"\text{IMR} = \tfrac{90}{4500}\times1000 = 20", r"T_d \approx \tfrac{70}{1.28} \approx 55 \text{ years}"],
                    ["A worked example.", "Births per thousand: eighteen. Deaths per thousand: five point two.", "Natural increase: twelve point eight per thousand, which is one point two eight percent.",
                     "Infant mortality uses live births: ninety over four thousand five hundred, times a thousand: twenty.", "And by the rule of seventy, seventy over one point two eight: the population doubles in about fifty five years."])
        self.p1_growth()
        self.p1_pyramid()
        self.p1_dtm()

    def p1_growth(self):
        head = T("Exponential growth and the rule of 70", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 100, 25], y_range=[0, 14, 2], x_length=6.0, y_length=3.8, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-3.0, -0.6, 0])
        r = ValueTracker(2.0)
        cur = always_redraw(lambda: ax.plot(lambda t: min(14, np.exp(r.get_value() / 100 * t)), x_range=[0, 100, 0.5], color=th.AMBER, stroke_width=4))
        lin = ax.plot(lambda t: 1 + t * 0.02, x_range=[0, 100], color=th.MUTED, stroke_width=3)
        rd = always_redraw(lambda: VGroup(T("growth rate", size=22, color=th.MUTED), DecimalNumber(r.get_value(), num_decimal_places=2, font_size=40, color=th.AMBER), T("% per year", size=22, color=th.MUTED),
                                          T("doubling time", size=22, color=th.MUTED), DecimalNumber(69.3 / r.get_value(), num_decimal_places=0, font_size=40, color=th.MINT), T("years", size=22, color=th.MUTED)).arrange(DOWN, buff=0.08).move_to([3.4, 0.2, 0]))
        eq = M(r"P_t = P_0 e^{rt} \Rightarrow T_d = \frac{\ln 2}{r} = \frac{69.3}{R\%} \approx \frac{70}{R}", size=36).move_to([0.6, 2.3, 0])
        with self.say("Populations do not grow by a fixed number each year, which would be a straight line. They grow by a fixed proportion, so the increase itself keeps getting bigger: exponential growth, a J curve. Set P t equal to twice P nought, and the doubling time comes out as the natural log of two over r. With r as a percentage, that is about seventy divided by the rate: the rule of seventy."):
            self.play(FadeIn(head), Create(ax), Create(lin), Write(eq))
            self.add(cur, rd)
            self.wait(1.0)
        with self.say("Watch it change. At two point six percent, Nepal's peak in the nineteen seventies, the population doubles in about twenty seven years. At today's zero point nine two percent, it takes about seventy five years."):
            self.play(r.animate.set_value(2.62), run_time=1.6)
            self.wait(0.6)
            self.play(r.animate.set_value(0.92), run_time=2.0)
        self.play(FadeOut(VGroup(head, ax, lin, eq)), FadeOut(cur), FadeOut(rd))
        self.remove(cur, rd)
        self.worked("Census 2011: 26,494,504. Census 2021: 29,164,578. The reference dates are 10.43 years apart. Find the annual exponential growth rate and the doubling time.",
                    [r"\frac{P_t}{P_0} = \frac{29\,164\,578}{26\,494\,504} = 1.1008", r"r = \frac{\ln 1.1008}{10.43} = \frac{0.0960}{10.43} = 0.0092 = 0.92\%", r"T_d = \frac{0.693}{0.0092} \approx 75 \text{ years}"],
                    ["Now Nepal's own numbers.", "The 2021 count divided by the 2011 count: one point one zero zero eight.",
                     "Take the natural log, zero point zero nine six, and divide by ten point four three years, not ten, because the 2021 census was delayed by COVID. Zero point nine two percent, exactly the official figure.",
                     "Doubling time: zero point six nine three over zero point zero zero nine two, about seventy five years."])

    def p1_pyramid(self):
        head = T("Population pyramids", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)

        def pyr(widths, x):
            g = VGroup()
            for i, w in enumerate(widths):
                y = -2.0 + 0.32 * i
                g.add(Rectangle(width=w, height=0.28, stroke_width=0, fill_color=MALE, fill_opacity=0.85).move_to([x - w / 2 - 0.03, y, 0]),
                      Rectangle(width=w, height=0.28, stroke_width=0, fill_color=FEM, fill_opacity=0.85).move_to([x + w / 2 + 0.03, y, 0]))
            return g

        exp = pyr([1.5 - 0.13 * i for i in range(11)], -4.2)
        sta = pyr([0.95, 1.0, 1.0, 0.97, 0.93, 0.9, 0.85, 0.78, 0.65, 0.5, 0.3], 0)
        dec = pyr([0.6, 0.7, 0.8, 0.9, 0.95, 1.0, 1.0, 0.95, 0.9, 0.75, 0.55], 4.2)
        lab = VGroup(*[VGroup(T(a, size=24, color=th.INK, weight="BOLD"), T(b, size=19, color=th.BODY)).arrange(DOWN, buff=0.08).move_to([x, -2.75, 0]) for a, b, x in
                       [("expanding", "high births and deaths: Niger", -4.2), ("stable", "Nepal and India today", 0), ("declining", "low births: Japan, Italy", 4.2)]])
        leg = VGroup(VGroup(Square(0.2, fill_color=MALE, fill_opacity=1, stroke_width=0), T("males", size=20, color=MALE)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, fill_color=FEM, fill_opacity=1, stroke_width=0), T("females", size=20, color=FEM)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.4).move_to([0, 2.2, 0])
        with self.say("A population pyramid stacks age groups from young at the bottom to old at the top, males on the left, females on the right. A broad base and a narrow top means many births and many deaths: rapid growth. Near vertical sides mean slow growth. And a base narrower than the middle means a population starting to shrink."):
            self.play(FadeIn(head), FadeIn(leg))
            for p_, l_ in zip([exp, sta, dec], lab):
                self.play(LaggedStart(*[GrowFromCenter(b_) for b_ in p_], lag_ratio=0.02), FadeIn(l_), run_time=1.2)
        nep = para("Nepal 2021: the 0–9 group (5.21 million) is now SMALLER than the 10–19 group (5.88 million): the signature of falling fertility.", width=11.5, size=23, color=th.AMBER).move_to([0, 2.2, 0])
        with self.say("Nepal's pyramid has just begun to pinch at the bottom. In 2021 there were fewer children under ten than ten to nineteen year olds. That is falling fertility, written in the shape."):
            self.play(FadeOut(leg), FadeIn(nep), Indicate(sta[:4], color=th.AMBER))
        self.play(FadeOut(VGroup(head, exp, sta, dec, lab, nep)))
        self.worked("Census 2021: 8,115,575 aged 0–14, 19,027,289 aged 15–64, 2,021,714 aged 65+. Find the child, old-age and total dependency ratios.",
                    [r"\text{child} = \tfrac{8\,115\,575}{19\,027\,289}\times100 = 42.7", r"\text{old-age} = \tfrac{2\,021\,714}{19\,027\,289}\times100 = 10.6", r"\text{total} = \tfrac{10\,137\,289}{19\,027\,289}\times100 = 53.3"],
                    ["The dependency ratio: people too young or too old to work, per hundred people of working age.", "Children: forty two point seven per hundred workers.", "The elderly: ten point six.",
                     "Total: fifty three. Low and falling, which means Nepal is inside its demographic dividend, a few decades with an unusually large working share. It pays only if those workers find jobs."])

    def p1_dtm(self):
        head = T("The demographic transition", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 45, 10], x_length=9.0, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-0.6, -0.2, 0])
        br = ax.plot(lambda s: 40 if s < 1.5 else (40 - 28 * (s - 1.5) / 1.5 if s < 3 else 12), x_range=[0, 4, 0.02], color=th.MINT, stroke_width=5)
        dr = ax.plot(lambda s: 40 if s < 0.8 else (40 - 30 * (s - 0.8) / 1.2 if s < 2 else 10), x_range=[0, 4, 0.02], color=th.CORAL, stroke_width=5)
        gap = ax.get_area(br, x_range=[0.8, 3.0], bounded_graph=dr, color=th.AMBER, opacity=0.3)
        stages = VGroup(*[para(s_, width=1.9, size=18, color=th.MUTED, align="center").move_to(ax.c2p(i + 0.5, 46)) for i, s_ in enumerate(["1 high stationary", "2 early expanding", "3 late expanding", "4 low stationary"])])
        leg = VGroup(T("birth rate", size=22, color=th.MINT), T("death rate", size=22, color=th.CORAL), T("natural increase", size=22, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.5, 0.6, 0])
        nep = para("Nepal: through stage 2 from about 1950 to 1990; TFR fell from 4.6 (1996) to 2.1 (2022), replacement level.", width=11.5, size=22, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Every industrialising country has followed the same path, the demographic transition. Stage one: high births, high deaths, little growth. Stage two: death rates fall with clean water and vaccines, but births stay high, and the population explodes. Stage three: births fall too, with contraception and girls' education. Stage four: both low, growth near zero."):
            self.play(FadeIn(head), Create(ax), FadeIn(stages), FadeIn(leg))
            self.play(Create(dr), Create(br), run_time=2.2)
            self.play(FadeIn(gap))
        with self.say("Nepal passed through stage two between about nineteen fifty and nineteen ninety, which is why growth peaked. Since then births have fallen fast: four point six children per woman in nineteen ninety six, two point one in twenty twenty two. That is replacement level, and the reason for the slowdown in our cold open. Education of girls is the single most effective control."):
            self.play(FadeIn(nep))
        self.play(FadeOut(VGroup(head, ax, br, dr, gap, stages, leg, nep)))
        rows = [["indicator", "value", "source"], ["population", "29,164,578", "Census 2021"], ["sex ratio", "95.6 males per 100 females", "Census 2021"], ["growth rate", "0.92% a year", "2011–2021"],
                ["absent abroad", "2.19 million (82% male)", "Census 2021"], ["life expectancy", "71.3 years", "NSO"], ["TFR · IMR", "2.1 · 28 per 1000 live births", "NDHS 2022"], ["MMR", "151 per 100,000 (539 in 1996)", "NMMS 2021"]]
        tb = B.table(rows, [3.2, 5.6, 3.0], row_h=0.58, size=22, colors=[th.MUTED, th.INK, th.BODY]).move_to([0, 0.3, 0])
        with self.say("Nepal today, in numbers. Twenty nine million people. More women than men, because over two million Nepalis, four fifths of them men, were abroad on census day. Life expectancy seventy one. Two children per woman. And maternal deaths down from five hundred and thirty nine to one hundred and fifty one per hundred thousand births, one of the fastest falls ever recorded.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("A population pyramid with a broad base and a narrow apex indicates",
                  ["a declining population", "a stationary population", "a rapidly growing population", "zero growth"], 2,
                  "Pause and think. Broad base, narrow top. What does it mean?",
                  "Rapid growth: many children being born, and many dying before old age. A declining population has the reverse, a base narrower than the middle.")

    # ------------------------------------------------------------------ part 2: health disorders
    def p2(self):
        self.section(1)
        d = self.callout("key", "Health (WHO, 1948): a state of complete physical, mental and social well-being, and not merely the absence of disease or infirmity.", width=11, size=27).move_to([0, 1.3, 0])
        cls = VGroup(*[VGroup(T(a, size=26, color=c_, weight="BOLD"), para(b, width=3.6, size=20, color=th.BODY, align="center")).arrange(DOWN, buff=0.12) for a, b, c_ in
                       [("communicable", "a pathogen, passed from host to host: bacteria, viruses, protozoa, worms, fungi", th.CORAL), ("non-communicable", "not transmissible: heart disease, diabetes, cancer, allergy", th.SKY),
                        ("deficiency", "something missing from the diet", th.AMBER)]]).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, -1.2, 0])
        with self.say("The World Health Organization defines health as complete physical, mental and social well being, not merely the absence of disease. Diseases fall into three groups: communicable, caused by a pathogen that passes between people; non communicable, which are not transmitted; and deficiency diseases."):
            self.play(FadeIn(d, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cls], lag_ratio=0.3))
        self.play(FadeOut(VGroup(d, cls)))
        rows = [["disease", "pathogen", "spread", "prevention"], ["tuberculosis", "Mycobacterium tuberculosis", "droplets", "BCG, DOTS"], ["typhoid", "Salmonella Typhi", "faecal food, water", "safe water, vaccine"],
                ["cholera", "Vibrio cholerae", "contaminated water", "chlorination, ORS"], ["hepatitis B", "hepatitis B virus", "blood, sex, mother → child", "vaccine"], ["rabies", "Lyssavirus", "bite of infected animal", "dog vaccination"],
                ["dengue", "dengue virus", "Aedes mosquito", "remove clean-water breeding sites"], ["kala-azar", "Leishmania donovani", "sandfly", "indoor spraying"], ["ascariasis", "Ascaris lumbricoides", "eggs in soil, food", "latrines, deworming"]]
        tb = B.table(rows, [2.4, 3.6, 3.4, 3.4], row_h=0.56, size=20, colors=[th.AMBER, th.INK, th.BODY, th.MINT]).move_to([0, 0.3, 0])
        with self.say("The communicable diseases to know, as pathogen, route and prevention. Tuberculosis, by droplets, prevented by B C G and DOTS treatment. Typhoid and cholera, from contaminated water. Hepatitis B, by blood. Rabies, by an animal bite. Dengue, carried by the Aedes mosquito, now spreading in Nepal's cities. Kala azar by the sandfly. And roundworm, from soil on unwashed food.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.tip("Four marks = four facts: pathogen, transmission, 2–3 symptoms, one control measure. Write names properly: Plasmodium vivax, not plasmodium Vivax.",
                 "Exam tip. A four mark disease question wants four facts: the pathogen, how it spreads, two or three symptoms, and one control measure. And write the scientific name correctly: capital genus, small species, Plasmodium vivax.")
        self.p2_malaria()
        self.p2_hiv()
        self.p2_ncd()

    def p2_malaria(self):
        head = T("Malaria: Plasmodium and its two hosts", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        man = RoundedRectangle(corner_radius=0.4, width=5.6, height=4.0, stroke_color=th.SKY, stroke_width=2).move_to([-3.4, -0.25, 0])
        mos = RoundedRectangle(corner_radius=0.4, width=5.6, height=4.0, stroke_color=th.AMBER, stroke_width=2).move_to([3.4, -0.25, 0])
        hl = VGroup(T("human: intermediate host (asexual)", size=22, color=th.SKY).next_to(man, UP, buff=0.1), T("female Anopheles: definitive host (sexual)", size=22, color=th.AMBER).next_to(mos, UP, buff=0.1))
        liver = RoundedRectangle(corner_radius=0.3, width=1.8, height=1.0, stroke_width=0, fill_color="#7A3B2E", fill_opacity=0.9).move_to([-4.8, 0.6, 0])
        ll = T("liver", size=20, color=th.INK).move_to(liver)
        rbcs = VGroup(*[Circle(radius=0.32, stroke_width=0, fill_color=RBC, fill_opacity=0.85).move_to([-2.0 + 0.8 * (i % 3), 0.6 - 0.9 * (i // 3), 0]) for i in range(6)])
        spz = VGroup(*[Line(ORIGIN, RIGHT * 0.25, color=PARA, stroke_width=4).move_to([-1.4 + 0.12 * k, 1.2, 0]) for k in range(3)])
        cap = B.Captions(self, at=(0, -2.85, 0), width=12.6, size=20)
        with self.say("Malaria is caused by Plasmodium, carried by the female Anopheles mosquito. In Nepal, Plasmodium vivax is by far the commonest. When an infected mosquito bites, thread like sporozoites enter the blood with its saliva."):
            self.play(FadeIn(head), Create(man), Create(mos), FadeIn(hl))
            self.play(FadeIn(spz))
            cap("Bite: sporozoites enter the blood", color=PARA)
        with self.say("They go straight to the liver and multiply there, asexually, into thousands of merozoites. That is the pre erythrocytic stage."):
            self.play(FadeIn(liver), FadeIn(ll))
            self.play(spz.animate.move_to(liver.get_center()), run_time=1.0)
            cap("Liver: schizogony → merozoites", color=PARA)
        mer = VGroup(*[Dot(radius=0.06, color=PARA).move_to(liver.get_center() + polar(0.3, a)) for a in np.linspace(0, TAU, 8, endpoint=False)])
        with self.say("Merozoites burst out and invade red blood cells. Inside each cell the parasite grows, divides, and every forty eight hours the red cells burst together, releasing new merozoites and toxins. That synchronised bursting is the fever: a cold stage with shivering, a hot stage, then sweating. Every third day: tertian malaria."):
            self.play(FadeOut(spz), FadeIn(mer))
            self.play(FadeIn(rbcs), *[m_.animate.move_to(rbcs[i % 6].get_center()) for i, m_ in enumerate(mer)], run_time=1.2)
            self.play(*[r_.animate.scale(1.25) for r_ in rbcs], run_time=0.6)
            self.play(*[FadeOut(r_, scale=1.6) for r_ in rbcs], run_time=0.5)
            self.sfx("impact", gain=-14)
            cap("Red cells: schizogony every 48 h → cells burst together → fever (cold, hot, sweating)", color=RBC)
        gam = VGroup(Ellipse(width=0.5, height=0.3, stroke_width=0, fill_color=MALE, fill_opacity=1).move_to([-1.2, -1.4, 0]), Ellipse(width=0.5, height=0.3, stroke_width=0, fill_color=FEM, fill_opacity=1).move_to([-0.6, -1.4, 0]))
        stomach = Circle(radius=0.6, stroke_color=th.AMBER, stroke_width=3).move_to([2.2, 0.0, 0])
        cyst = VGroup(Circle(radius=0.35, stroke_width=0, fill_color=PARA, fill_opacity=0.5), *[Line(ORIGIN, RIGHT * 0.18, color=PARA, stroke_width=3).rotate(a).move_to(polar(0.12, a)) for a in np.linspace(0, TAU, 6, endpoint=False)]).move_to([3.5, -1.2, 0])
        gland = Ellipse(width=0.9, height=0.5, stroke_color=th.AMBER, stroke_width=3).move_to([4.8, 0.8, 0])
        lab2 = VGroup(T("gut: gametes fuse → zygote", size=18, color=th.AMBER).next_to(stomach, UP, buff=0.1), T("oocyst on stomach wall", size=18, color=PARA).next_to(cyst, DOWN, buff=0.1), T("salivary glands", size=18, color=th.AMBER).next_to(gland, UP, buff=0.1))
        with self.say("Some merozoites become male and female gametocytes instead. A mosquito sucks them up with blood. In its gut they become gametes and fuse: fertilisation happens in the mosquito. The zygote burrows into the stomach wall as an oocyst, which bursts to release sporozoites. They migrate to the salivary glands, ready for the next bite."):
            self.play(FadeIn(gam))
            self.play(gam.animate.move_to(stomach.get_center()), Create(stomach), run_time=1.2)
            self.play(FadeIn(lab2[0]))
            self.play(FadeIn(cyst), FadeIn(lab2[1]))
            self.play(Create(gland), FadeIn(lab2[2]))
            cap("Mosquito: gametes → zygote → oocyst → sporozoites → salivary glands", color=th.AMBER)
        self.play(FadeOut(VGroup(head, man, mos, hl, liver, ll, mer, gam, stomach, cyst, gland, lab2)))
        cap.clear()
        k = self.callout("key", "The DEFINITIVE host is the one where sexual reproduction (fertilisation) happens: the female Anopheles. Humans are the INTERMEDIATE host: only asexual schizogony occurs in us.", width=11, size=26).move_to([0, 0.8, 0])
        np_ = para("Nepal 2024: 37 indigenous and 1006 imported cases; elimination target now 2030. Control: bed nets, indoor spraying, prompt diagnosis and treatment.", width=11.5, size=22, color=th.BODY).move_to([0, -1.6, 0])
        with self.say("The host names trip students up every year. The definitive host is where sexual reproduction happens: the mosquito. We are only the intermediate host, where the parasite multiplies asexually. Nepal has nearly eliminated malaria: just thirty seven local cases in twenty twenty four."):
            self.play(FadeIn(k, shift=UP * 0.2))
            self.play(FadeIn(np_))
        self.play(FadeOut(VGroup(k, np_)))

    def p2_hiv(self):
        head = T("HIV and AIDS", size=30, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        vir = VGroup(Circle(radius=0.8, stroke_color=th.CORAL, stroke_width=4, fill_color=th.CORAL, fill_opacity=0.12),
                     *[Line(polar(0.8, a), polar(1.05, a), color=th.CORAL, stroke_width=4) for a in np.linspace(0, TAU, 12, endpoint=False)],
                     Polygon(*[polar(0.4, a) for a in np.linspace(0, TAU, 6, endpoint=False)], stroke_color=th.AMBER, stroke_width=3),
                     *[VMobject(stroke_color=th.MINT, stroke_width=3).set_points_smoothly([[-0.2 + 0.1 * k, -0.25, 0], [0.0 + 0.1 * k, 0.0, 0], [-0.1 + 0.1 * k, 0.25, 0]]) for k in range(2)]).move_to([-4.2, 0.2, 0])
        vl = para("retrovirus: 2 RNA strands + reverse transcriptase, integrase, protease; envelope with gp120", width=3.4, size=19, color=th.BODY, align="center").next_to(vir, DOWN, buff=0.25)
        steps = ["binds CD4 on a helper T cell", "reverse transcriptase: RNA → DNA", "integrase: DNA into our chromosome (provirus)", "the cell makes new viruses until it dies"]
        rows = VGroup(*[VGroup(T(str(i + 1), size=24, color=th.CORAL, weight="BOLD"), T(s_, size=24, color=th.INK)).arrange(RIGHT, buff=0.3) for i, s_ in enumerate(steps)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.2, 0.6, 0])
        with self.say("HIV is a retrovirus: two strands of RNA and its own enzymes inside an envelope. It targets the helper T lymphocyte, the cell that coordinates the whole immune response. It binds the C D four receptor, copies its RNA into DNA with reverse transcriptase, splices that DNA into our own chromosome with integrase, and turns the cell into a virus factory until it dies.") as v:
            self.play(FadeIn(head), FadeIn(vir), FadeIn(vl))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur * 0.12)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1200, 400], x_length=6.0, y_length=2.2, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([1.8, -2.1, 0])
        cd4 = ax.plot(lambda t: 1000 * np.exp(-0.17 * t) if t > 0.3 else 1000 - 600 * t, x_range=[0, 10, 0.05], color=th.SKY, stroke_width=4)
        line200 = DashedLine(ax.c2p(0, 200), ax.c2p(10, 200), color=th.CORAL)
        l200 = T("below 200: AIDS", size=18, color=th.CORAL).next_to(ax.c2p(10, 200), RIGHT, buff=0.1)
        cl = T("CD4 count over ~10 years untreated", size=18, color=th.SKY).next_to(ax, UP, buff=0.05)
        with self.say("Over years, the helper T cell count falls. Below two hundred per cubic millimetre, the person has AIDS, and dies of ordinary infections like tuberculosis and pneumonia, because both arms of immunity have lost their coordinator. HIV spreads by unprotected sex, infected blood and needles, and from mother to child. Not by touching, sharing food, or mosquitoes. There is no cure, but antiretroviral therapy holds it down for decades."):
            self.play(FadeOut(rows), Create(ax), FadeIn(cl))
            self.play(Create(cd4), run_time=2.0)
            self.play(Create(line200), FadeIn(l200))
        self.play(FadeOut(VGroup(head, vir, vl, ax, cd4, line200, l200, cl)))
        rows = [["", "active", "passive"], ["antibodies", "made by your own body", "given ready-made"], ["natural", "after an infection", "across the placenta (IgG), in colostrum (IgA)"], ["artificial", "vaccine: BCG, DPT, measles", "antiserum: anti-tetanus, anti-rabies"],
                ["memory", "yes, long-lasting", "no, short-lived"]]
        tb = B.table(rows, [2.4, 4.6, 5.6], row_h=0.66, size=22, colors=[th.MUTED, th.MINT, th.SKY]).move_to([0, 0.6, 0])
        ig = para("Antibody classes: IgG (most, crosses the placenta) · IgM (first made) · IgA (mucus, colostrum) · IgE (allergy) · IgD (on B cells).", width=12, size=22, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Immunity. Innate immunity is with you from birth: skin, mucus, stomach acid, phagocytes. Acquired immunity is specific. It is active when your own body makes the antibodies, after an infection or a vaccine, with memory that lasts. It is passive when antibodies are handed over ready made: across the placenta, in colostrum, or as an antiserum. Quick, but short lived.") as v:
            B.reveal_table(self, tb, v.dur * 0.8)
            self.play(FadeIn(ig))
        self.play(FadeOut(VGroup(tb, ig)))
        self.quiz("The definitive host of the malarial parasite is",
                  ["man", "female Anopheles", "male Anopheles", "Culex"], 1,
                  "Pause and think. Which is the definitive host of Plasmodium?",
                  "The female Anopheles, because fertilisation and the sexual phase happen inside her. Man is the trap: we suffer the disease, but only the asexual phase occurs in us. Male mosquitoes do not bite.")

    def p2_ncd(self):
        rows = [["disease", "cause or risk", "prevention"], ["hypertension", "salt, obesity, alcohol, stress", "less salt, exercise"], ["coronary heart disease", "smoking, high LDL, diabetes", "no tobacco, diet, exercise"],
                ["COPD", "tobacco and indoor biomass smoke", "clean cooking fuel"], ["diabetes", "type 1: no insulin; type 2: resistance", "weight control, exercise"], ["cancer", "tobacco, HPV, aflatoxin, radiation", "screening, vaccination"]]
        tb = B.table(rows, [3.4, 5.0, 4.0], row_h=0.62, size=22, colors=[th.SKY, th.BODY, th.MINT]).move_to([0, 0.9, 0])
        nep = para("Nepal's epidemiological transition: NCDs now cause about two-thirds of deaths. Leading causes: COPD, heart disease, stroke; leading risk: air pollution. STEPS 2019: 24.5% raised BP, 28.9% use tobacco.", width=12, size=22, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("Nepal is going through an epidemiological transition: infections are retreating, and non communicable diseases now cause about two thirds of deaths. Chronic lung disease from smoke, heart disease and stroke lead the list. One adult in four has high blood pressure, and nearly three in ten use tobacco.") as v:
            B.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nep))
        self.play(FadeOut(VGroup(tb, nep)))
        rows = [["missing", "disease", "signs"], ["protein + energy", "kwashiorkor / marasmus", "oedema, moon face / extreme wasting"], ["vitamin A", "night blindness", "Bitot's spots, xerophthalmia"], ["vitamin B₁", "beriberi", "oedema, nerve damage"],
                ["vitamin B₃", "pellagra", "dermatitis, diarrhoea, dementia"], ["vitamin C", "scurvy", "bleeding gums"], ["vitamin D", "rickets / osteomalacia", "bow legs / soft bones"], ["iron", "anaemia", "pallor, tiredness"], ["iodine", "goitre, cretinism", "neck swelling"]]
        tb = B.table(rows, [3.0, 4.2, 5.4], row_h=0.56, size=21, colors=[th.AMBER, th.INK, th.BODY]).move_to([0, 0.5, 0])
        with self.say("Finally, deficiency diseases. Too little protein and energy: kwashiorkor, which swells with oedema, and marasmus, which shrinks to skin and bone. Vitamin A: night blindness. B one: beriberi. B three: pellagra, the three Ds, dermatitis, diarrhoea, dementia. C: scurvy. D: rickets. Iron: anaemia. And iodine: goitre, now rare in Nepal thanks to iodised salt.") as v:
            B.reveal_table(self, tb, v.dur * 0.9)
        st = para("NDHS 2022: 25% of under-fives stunted (57% in 1996); 43% of young children anaemic.", width=11, size=22, color=th.CORAL).move_to([0, -2.85, 0])
        with self.say("Progress is real but incomplete: stunting has fallen from fifty seven to twenty five percent, but forty three percent of young children are still anaemic."):
            self.play(FadeIn(st))
        self.play(FadeOut(VGroup(tb, st)))
        self.quiz("The 'three Ds' — dermatitis, diarrhoea and dementia — are signs of",
                  ["scurvy", "beriberi", "pellagra", "rickets"], 2,
                  "Last one. Dermatitis, diarrhoea, dementia. Which deficiency?",
                  "Pellagra, from lack of vitamin B three, niacin. Beriberi is B one, thiamine, and causes oedema and nerve damage; scurvy is vitamin C.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "CBR, CDR per 1000 people; IMR per 1000 live births; RNI = CBR − CDR.",
            "Doubling time ≈ 70 ÷ growth %. Nepal 2021: 0.92%, about 75 years.",
            "Pyramids show growth; dependency ratio 53; Nepal late in the demographic transition.",
            "Malaria: human = intermediate host, female Anopheles = definitive host; 48 h fever cycle.",
            "HIV destroys helper T cells; below 200 CD4 per mm³ = AIDS.",
            "Active vs passive immunity; NCDs now dominate; know your deficiency diseases.",
        ], "Quick recap. Birth and death rates are per thousand people, but infant mortality is per thousand live births. Doubling time is about seventy over the growth rate: seventy five years for Nepal today. Pyramids show growth, and Nepal is late in the demographic transition. In malaria, the mosquito is the definitive host. H I V destroys helper T cells. And non communicable diseases now cause most deaths.")
        self.outro("That was human population and health. Next, the last unit of biology: applied biology, from fisheries and beekeeping to the microbes that make us ill and the ones that feed us. See you there.")
