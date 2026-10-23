import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def globe(r=1.8):
    c = Circle(radius=r, stroke_color=th.SKY, stroke_width=3, fill_color="#123055", fill_opacity=0.8)
    lat = VGroup(*[Ellipse(width=2 * r * np.cos(a), height=0.25 * r * np.cos(a), stroke_color=th.FAINT, stroke_width=1.5).shift(UP * r * np.sin(a)) for a in (-0.9, -0.45, 0, 0.45, 0.9)])
    mer = Line(UP * r, DOWN * r, color=th.AMBER, stroke_width=5)
    return VGroup(c, lat, mer)


def rope(x0, x1, y=0.0, color=th.AMBER):
    xs = np.linspace(x0, x1, 120)
    a = VMobject(stroke_color=color, stroke_width=5).set_points_smoothly([[x, y + 0.12 * np.sin(6 * x), 0] for x in xs])
    b = VMobject(stroke_color=th.MINT, stroke_width=5).set_points_smoothly([[x, y - 0.12 * np.sin(6 * x), 0] for x in xs])
    return VGroup(a, b)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 11
    TITLE = "The Awakening Age"
    SUBTITLE = "Ben Okri · a poem"
    SECTIONS = ["Ben Okri and the poem's occasion", "Couplets 1–2: the summons", "Couplets 3–4: the rope", "Couplets 5–7: perception and harvest", "Themes", "Form and devices"]
    NEXT = "Unit 12 · Soft Storm"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        poster = VGroup(Rectangle(width=4.2, height=3.0, stroke_color=th.MUTED, stroke_width=3), T("POVERTY", size=40, color=th.MUTED, weight="BOLD")).move_to([-3.2, 0.3, 0])
        full = VGroup(Rectangle(width=4.2, height=3.0, stroke_color=th.AMBER, stroke_width=3), VGroup(*[T(t_, size=30, color=c_, weight="BOLD") for t_, c_ in [("work", th.SKY), ("wisdom", th.MINT), ("creativity", th.PINK), ("and poverty", th.MUTED)]]).arrange(DOWN, buff=0.15)).move_to([3.2, 0.3, 0])
        full[1].move_to(full[0])
        with self.say("A charity poster shows a country in one word: poverty. Hunger, disaster, need. Ben Okri's poem argues that this picture is not just incomplete. It is part of the problem."):
            self.play(FadeIn(poster))
        q = T("\"There's more to a people than their poverty\"", size=30, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("There's more to a people than their poverty, he writes: there is their work, their wisdom, their creativity. Change how people are seen, and you change what is possible."):
            self.play(FadeIn(full))
            self.play(FadeIn(q))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(poster, full, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 11: The Awakening Age, by Ben Okri."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Ben Okri and the poem's occasion. The summons. The rope. Perception and harvest. The themes. And the form and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Sir Ben Okri (born 1959)")
        facts = E.bullets(["born in Minna, Nigeria — 1959 (your textbook's 1949 is a misprint)", "childhood in London, then Nigeria during the civil war", "The Famished Road won the Booker Prize in 1991, when he was 32", "often called magical realist — he says Africa simply has \"more dimensions to reality\"", "knighted in 2023"], width=8.2, size=24).move_to([-2.0, 0.2, 0])
        with self.say("Ben Okri was born in Nigeria in nineteen fifty nine; your textbook's nineteen forty nine is a misprint. He spent his early childhood in London, then returned to Nigeria during its civil war. His novel The Famished Road won the Booker Prize when he was only thirty two. Critics call him a magical realist; he replies that in his tradition there are simply more dimensions to reality: myths, ancestors, spirits. He was knighted in twenty twenty three."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 11.0)
        self.play(FadeOut(VGroup(h, facts)))
        h = E.head(self, "1999: Oxfam's \"On The Line\"")
        g = globe(2.0).move_to([-3.4, -0.4, 0])
        stops = VGroup(*[T(t_, size=22, color=th.AMBER).move_to(g.get_center() + np.array([0.9, 1.6 - 0.45 * k, 0]), aligned_edge=LEFT) for k, t_ in enumerate(["Britain", "France", "Spain", "Algeria", "Mali", "Burkina Faso", "Togo", "Ghana"])])
        info = para("Commissioned for the millennium: a project linking schools and communities along the Greenwich Meridian — the line of zero longitude. Hence: \"O ye who travel the meridian line\".", width=5.4, size=24, color=th.INK).move_to([3.6, 0.6, 0])
        nt = para("Not a war poem, and not really about migration: its subject is rich and poor countries at the end of the 20th century.", width=5.4, size=22, color=th.MUTED).move_to([3.6, -1.9, 0])
        with self.say("Here is context almost no guide gives you. The poem was commissioned in nineteen ninety nine by Oxfam for a millennium project called On The Line, which linked schools and communities along the Greenwich Meridian, the line of zero longitude, from Britain down through France, Spain, and West Africa. That explains the first line: O ye who travel the meridian line. So it is not a war poem, and not really about labour migration: its subject is rich and poor countries at the end of the century. Give that fact in one sentence, then answer the question asked."):
            self.play(FadeIn(h), FadeIn(g))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stops], lag_ratio=0.2))
            self.play(FadeIn(info))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, g, stops, info, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Couplet 1: a blessing")
        q = T("\"O ye who travel the meridian line …\"", size=32, color=th.AMBER).move_to([0, 1.6, 0])
        pts = E.bullets(["\"O ye\": the language of the old Bible and public prayer — ceremony, not chat", "\"May …\": the optative, the grammar of wishing. Okri never gives an order.", "the vision of a new world shines \"within you\": change begins inside", "\"shine\" starts a chain of light: glory, clearest light, flowering"], width=11.2, size=26).move_to([0, -0.7, 0])
        with self.say("Couplet one opens like a blessing. O ye who travel the meridian line: O ye is the old language of the Bible and public prayer, lifting the poem into ceremony. Then may: the grammar of wishing. Six of the seven couplets are wishes or statements; not one is an order. The vision of a new world is to shine within you, so change begins inside. And shine starts a chain of light running through the whole poem."):
            self.play(FadeIn(h), FadeIn(q))
            E.reveal_list(self, pts, 9.0)
        self.play(FadeOut(VGroup(h, q, pts)))
        h = E.head(self, "Couplet 2: \"poverty's rage\"")
        fog = Rectangle(width=5.0, height=3.0, stroke_width=0, fill_color=th.MUTED, fill_opacity=0.5).move_to([1.0, -0.2, 0])
        fogl = T("poverty's rage", size=30, color=th.CORAL, weight="BOLD").move_to(fog)
        eye = VGroup(Ellipse(width=1.4, height=0.6, stroke_color=th.INK, stroke_width=4), Dot(radius=0.15, color=th.INK)).move_to([-4.6, -0.2, 0])
        glory = T("the glory of the awakening age", size=28, color=th.AMBER, weight="BOLD").move_to([4.0, -2.3, 0])
        notes = E.bullets(["rage = violent anger: poverty is furious, not a quiet misfortune", "\"see through to\": poverty is a fog the eyes must pierce", "\"awakening\": the light was always there; the eyes were shut"], width=11.4, size=24).move_to([0, 2.0, 0])
        with self.say("Couplet two. Eyes that have lived with poverty's rage: not sadness, rage, violent anger. Okri will not soften it. And they are to see through to the glory of the awakening age. See through: poverty is like a fog the vision must pierce. And awakening, not new: the light was always there, and the eyes were shut."):
            self.play(FadeIn(h), FadeIn(eye), FadeIn(fog), FadeIn(fogl))
            E.reveal_list(self, notes, 6.0)
            self.play(fog.animate.set_opacity(0.08), fogl.animate.set_opacity(0.3), FadeIn(glory), run_time=2)
        self.play(FadeOut(VGroup(h, fog, fogl, eye, glory, notes)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "\"Woven in history, like a mountain rope\"")
        r = rope(-6.0, 6.0, y=1.0)
        props = VGroup(*[E.card(t_, d_, c_, w=2.9, h=2.4, size=22) for t_, d_, c_ in [("many strands", "twisted into one: weak alone, strong together", th.AMBER), ("tied at both ends", "useless unless both sides hold", th.MINT), ("one fate", "if one climber falls, the others hold", th.SKY), ("going up", "a rope exists to ascend", th.PINK)]]).arrange(RIGHT, buff=0.2).move_to([0, -1.3, 0])
        with self.say("Couplet three gives the reason, beginning with for, the only logical connective in the poem. We are richly linked in hope: richly, just after poverty, relocates wealth into connection. Woven in history, like a mountain rope. Think about a climbing rope, as a Nepali reader can. It is many strands twisted into one. It is useless unless tied at both ends. The climbers share one fate. And it exists for one purpose: going up."):
            self.play(FadeIn(h), Create(r), run_time=2)
            for p_ in props:
                self.play(FadeIn(p_, shift=UP * 0.2), run_time=0.6)
                self.hold(1.4)
        self.play(FadeOut(VGroup(h, r, props)))
        h = E.head(self, "Couplet 4: together, ascend")
        mtn = Polygon([-6.2, -2.8, 0], [-2.4, 1.8, 0], [0.6, -2.8, 0], stroke_color=th.MUTED, stroke_width=3, fill_color="#26304A", fill_opacity=0.8)
        climbers = VGroup(*[Dot([-5.0 + 0.35 * k, -2.2 + 0.42 * k, 0], radius=0.11, color=th.PALETTE[k]) for k in range(5)])
        line = VMobject(stroke_color=th.AMBER, stroke_width=3).set_points_as_corners([c_.get_center() for c_ in climbers])
        txt = E.bullets(["\"Together\": the first word, and the whole poem's condition", "\"ascend\": a formal, aspiring verb — mountains, thrones, heaven", "guided by \"our heart's clearest light\": one heart, many owners"], width=6.0, size=24).move_to([3.4, 2.0, 0])
        txt.move_to([3.6, -0.4, 0])
        with self.say("Couplet four uses the rope. Together, the first word, is the poem's whole condition. Ascend is a formal, aspiring verb: you ascend a mountain, a throne, a stair to heaven. And the guide is our heart's clearest light, not policy or economics. Notice our heart: one heart, many owners. The many have become one climber."):
            self.play(FadeIn(h), FadeIn(mtn), FadeIn(climbers), Create(line))
            self.play(VGroup(climbers, line).animate.shift(UP * 1.6 + RIGHT * 1.35), run_time=2)
            E.reveal_list(self, txt, 4.0)
        self.play(FadeOut(VGroup(h, mtn, climbers, line, txt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Couplet 5: the hinge")
        a = E.card("not", "when aid arrives · when the economy grows", th.MUTED, w=5.4, h=2.2, size=26).move_to([-3.2, 0.9, 0])
        b = E.card("but", "\"when perceptions are changed\"", th.AMBER, w=5.4, h=2.2, size=28).move_to([3.2, 0.9, 0])
        nt = para("Then \"a flowering of truth instead of pain\": much of the pain was the pain of being misdescribed. The passive voice leaves open who must change — the poor, seeing themselves through others' eyes; the rich, seeing only a problem to pity.", width=11.4, size=24, color=th.INK).move_to([0, -1.6, 0])
        with self.say("Couplet five is the intellectual centre, the lines to quote if you must defend this as a serious poem. What must change first is not aid, not the economy, but perception: how people are seen. The passive, perceptions are changed, leaves open who changes them: the poor, who see themselves through others' eyes, and the rich, who see only a problem to pity. Then a flowering of truth instead of pain: much of the pain, it suggests, was the pain of being misdescribed."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))
        h = E.head(self, "Couplet 6: the definition")
        q = T("\"There's more to a people than their poverty\"", size=32, color=th.AMBER, weight="BOLD").move_to([0, 1.6, 0])
        three = VGroup(*[E.card(t_, d_, c_, w=3.6, h=2.0, tsize=30, size=24) for t_, d_, c_ in [("work", "what people do — first!", th.SKY), ("wisdom", "what they know", th.MINT), ("creativity", "what they make", th.PINK)]]).arrange(RIGHT, buff=0.3).move_to([0, -0.5, 0])
        nt = para("poverty / creativity: the poem's only long rhyme chains the two words together.", width=11, size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("Couplet six is the one to memorise: there's more to a people than their poverty; there is their work, their wisdom, their creativity. Work comes first: this is not sentimental noble poverty, but an economy the poster never photographs. And the rhyme, poverty with creativity, the poem's only long rhyme, chains together exactly the two words the couplet is arguing about."):
            self.play(FadeIn(h), FadeIn(q))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.2) for t_ in three], lag_ratio=0.3))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, q, three, nt)))
        h = E.head(self, "Couplet 7: \"may our lives rhyme\"")
        w1 = E.chip("poverty", th.MUTED, size=30).move_to([-2.4, 1.2, 0])
        w2 = E.chip("creativity", th.PINK, size=30).move_to([2.4, 1.2, 0])
        arc = ArcBetweenPoints(w1.get_top(), w2.get_top(), angle=-PI / 3, color=th.AMBER)
        nt = E.bullets(["rhyme: two different things that answer each other — Okri's model of a relationship", "\"along the line\": back to the meridian of line 1, a circle", "\"a loving harvest of space and time\": sown long ago, patient, enough for everyone"], width=11.4, size=26).move_to([0, -1.3, 0])
        with self.say("The last couplet turns the poem's technique into its meaning: may our lives rhyme. A rhyme is two different words that answer each other, not identical, but in harmony: that is Okri's model of how people should relate, and he has spent thirteen lines demonstrating it in couplets. Along the line returns to the meridian, closing the circle. And a loving harvest of space and time: something sown long ago, patient, and enough for everyone, the answer to poverty."):
            self.play(FadeIn(h), FadeIn(w1), FadeIn(w2), Create(arc))
            E.reveal_list(self, nt, 9.0)
        self.play(FadeOut(VGroup(h, w1, w2, arc, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Perception, not charity", "the poor described only by lack — that description keeps them poor", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Solidarity", "\"richly linked in hope\": a rope of many strands, one fate", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Hope and awakening", "light, glory, flowering: the change begins within", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Dignity of the poor", "work, wisdom, creativity — not pity", th.PINK, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Perception, not charity: describing people only by what they lack is itself part of what keeps them poor. Solidarity: richly linked in hope, one rope, one fate. Hope and awakening, beginning within. And the dignity of the poor: their work, wisdom and creativity, not our pity. You may apply the poem to Nepali workers abroad, but say honestly that you are applying it."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Fourteen lines, seven couplets: aa bb cc dd ee ff gg")
        pairs = VGroup(*[VGroup(Square(0.5, stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.3), Square(0.5, stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.3)).arrange(DOWN, buff=0.1) for _ in range(7)]).arrange(RIGHT, buff=0.35).move_to([0, 0.8, 0])
        letters = VGroup(*[T(c_ * 2, size=26, color=th.INK).next_to(p_, DOWN, buff=0.2) for c_, p_ in zip("abcdefg", pairs)])
        nt = para("Fourteen lines, so the exercises call it a sonnet — but it has no regular metre and no sonnet rhyme scheme. The couplets themselves are the argument: things that answer one another. \"May our lives rhyme.\"", width=11.4, size=24, color=th.INK).move_to([0, -2.0, 0])
        with self.say("The form. Fourteen lines, which is why your exercises call it a sonnet, but there is no regular metre and no sonnet rhyme scheme. Instead, seven rhyming couplets: a a, b b, c c, and so on. The couplets are the argument: pairs of lines that answer one another, until the last couplet names the idea: may our lives rhyme."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(p_) for p_ in pairs], lag_ratio=0.15), FadeIn(letters))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, pairs, letters, nt)))
        rows = [["apostrophe", "\"O ye who travel …\"", "a ceremonial address"], ["simile", "\"like a mountain rope\"", "strands, one fate, ascent"], ["metaphor", "\"a flowering of truth\"", "slow, natural change"],
                ["imagery of light", "shine, glory, clearest light", "hope and vision"], ["antithesis", "truth \"instead of pain\"", "the turn of the poem"], ["harvest metaphor", "\"a loving harvest of space and time\"", "enough for everyone"]]
        E.device_slide(self, rows, "Devices to quote. Apostrophe: O ye who travel. The simile of the mountain rope. Metaphor: a flowering of truth. A chain of light imagery. Antithesis: truth instead of pain. And the closing harvest metaphor.", widths=(3.0, 5.2, 4.2), size=22)
        self.quiz("What is the rhyme scheme of \"The Awakening Age\"?",
                  ["abab cdcd efef gg", "seven rhyming couplets", "abcb", "no rhyme"], 1,
                  "Pause and think.",
                  "aa bb cc dd ee ff gg: seven couplets, fourteen lines.")
        self.quiz("According to the poem, what must change first?",
                  ["the economy", "the weather", "how people are perceived", "the government"], 2,
                  "One more.",
                  "\"When perceptions are changed\", truth flowers instead of pain.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Ben Okri (born 1959, not 1949); Booker 1991; poem for Oxfam's \"On The Line\", 1999.",
            "\"O ye who travel the meridian line\": a blessing, all wishes, no orders.",
            "\"poverty's rage\"; \"richly linked in hope … like a mountain rope\".",
            "\"When perceptions are changed\"; \"more to a people than their poverty\".",
            "Seven couplets, 14 lines; \"may our lives rhyme\"; a loving harvest.",
        ], "Quick recap. Okri, and a poem written for a line round the earth. A blessing in wishes. Poverty's rage seen through. A mountain rope of hope. Perception before charity. And seven couplets that ask our lives to rhyme.")
        self.outro("That was The Awakening Age. Next, the last poem: Soft Storm. See you there.")
