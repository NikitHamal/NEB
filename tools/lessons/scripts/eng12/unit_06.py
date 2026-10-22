import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

SUN = "#F2994A"


def half_eye(w=1.6, color=th.AMBER, openness=0.35):
    """A Buddha-style half-closed eye: a lid arc over a half pupil."""
    lid = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=-PI * 0.55, color=color, stroke_width=5)
    lower = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=PI * 0.25 * openness / 0.35, color=color, stroke_width=3)
    pupil = Sector(radius=w * 0.17, start_angle=PI, angle=PI, color=color, fill_opacity=1).shift(DOWN * 0.02).rotate(PI)
    pupil.move_to(DOWN * w * 0.05)
    return VGroup(lid, lower, pupil)


def stupa_eyes(scale=1.0, color=th.AMBER):
    eyes = VGroup(half_eye(color=color), half_eye(color=color)).arrange(RIGHT, buff=0.8)
    brow = VGroup(*[Arc(radius=0.9, start_angle=PI * 0.25, angle=PI * 0.5, color=color, stroke_width=4).next_to(e_, UP, buff=0.05) for e_ in eyes])
    q = VMobject(stroke_color=color, stroke_width=4).set_points_smoothly([[-0.12, -0.2, 0], [0.12, -0.35, 0], [-0.05, -0.6, 0], [0.12, -0.8, 0]])
    return VGroup(eyes, brow, q).scale(scale)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 6
    TITLE = "The Half-closed Eyes of the Buddha and the Slowly Sinking Sun"
    SUBTITLE = "Shankar Lamichhane · a short story"
    SECTIONS = ["Shankar Lamichhane", "The tourist's evening", "The guide's day", "Two monologues, one picture", "Themes", "Irony and the eyes"]
    NEXT = "Unit 7 · A Very Old Man with Enormous Wings"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        se = stupa_eyes(1.3).move_to([0, 0.8, 0])
        sun = Circle(radius=0.5, stroke_width=0, fill_color=SUN, fill_opacity=0.9).move_to([3.6, 2.2, 0])
        q1 = T("\"Show me beautiful, full eyes.\"", size=30, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("A foreign tourist in Kathmandu, warmed by whisky, tells his Nepali guide how wonderful the country is: its peace, its gods, its carved windows, its smiles, and everywhere, eyes. Tomorrow, he says, show me beautiful eyes. Take me to a lonely stupa to watch the sunset reflected in the eyes of the Buddha."):
            self.play(FadeIn(se), FadeIn(sun))
            self.play(sun.animate.shift(DOWN * 1.6), FadeIn(q1), run_time=2)
        q2 = para("The next day the guide shows him a pair of eyes. Not the Buddha's.", width=11, size=30, color=th.CORAL).move_to([0, -2.5, 0])
        with self.say("The next day the guide does show him a pair of eyes. But they are not the Buddha's."):
            self.play(FadeIn(q2))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(se, sun, q1, q2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 6: The Half closed Eyes of the Buddha and the Slowly Sinking Sun, by Shankar Lamichhane."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Shankar Lamichhane. The tourist's evening. The guide's day. Two monologues making one picture. The themes. And the irony of the eyes.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Shankar Lamichhane (1928–1976)")
        facts = E.bullets(["born in Kathmandu; raised by his mother in Banaras", "studied science at Tri-Chandra College", "later managed a handicrafts store — and met many tourists", "a pioneer of the modern Nepali essay and story: lyrical, musical, plotless", "this story: 1962; translated by Michael Hutt"], width=7.8, size=24).move_to([-2.2, 0.2, 0])
        side = VGroup(T("his stories", size=26, color=th.AMBER, weight="BOLD"), para("\"heavy with symbolism\", with little conventional plot — closer to essays", width=3.9, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.4, 0])
        with self.say("Shankar Lamichhane was born in Kathmandu in nineteen twenty eight and raised by his mother in Banaras. He studied science, worked for government and cultural bodies, and later managed a handicrafts store, where he met many foreign visitors, exactly like the tourist in this story. He is one of Nepal's best loved essayists, and his stories are lyrical and full of symbols, with little conventional plot. This one appeared in nineteen sixty two, and you read it in Michael Hutt's English translation."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))
        h = E.head(self, "Two speeches, two silent listeners")
        a = E.card("Part One: the tourist", "the evening before, over whisky; the guide listens and never answers", th.AMBER, w=5.6, h=2.6).move_to([-3.2, 0.5, 0])
        b = E.card("Part Two: the guide", "the next day, sober, on a hill; the tourist listens and never answers", th.SKY, w=5.6, h=2.6).move_to([3.2, 0.5, 0])
        nt = para("No narrator, almost no action: two monologues, joined by the image of eyes.", width=11, size=26, color=th.MINT).move_to([0, -2.2, 0])
        with self.say("The story has an unusual shape. There is no narrator and almost no action. Part one is the tourist's speech, the evening before, over drinks; the guide never answers. Part two is the guide's speech the next day; now the tourist never answers. What joins them is the image of eyes."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Nepal through a glass of whisky")
        glass = VGroup(Polygon([-0.5, 0.8, 0], [0.5, 0.8, 0], [0.4, -0.8, 0], [-0.4, -0.8, 0], stroke_color=th.MUTED, stroke_width=3), Polygon([-0.46, 0.2, 0], [0.46, 0.2, 0], [0.4, -0.8, 0], [-0.4, -0.8, 0], stroke_width=0, fill_color=th.AMBER, fill_opacity=0.5)).move_to([5.0, -1.4, 0])
        items = [("the view from the plane", "a green valley, geometric fields, red, yellow and white houses, an age-old peace"), ("the East as giver", "religion, images, manuscripts, civilisation — given \"innocent of the notion of ownership\""),
                 ("history from books", "the valley as a lake, Manjushri's sword at Chobhar, monks with the \"samyak gaze\""), ("art and harmony", "carved houses like temples; Aryans and non-Aryans, Hindus and Buddhists side by side"),
                 ("momos and family", "an old man telling his grandson of Princess Bhrikuti; scenes \"not in libraries\""), ("the smile and the eyes", "a smile of welcome; carved windows, stupas, people: \"a land of eyes\"")]
        rows = VGroup(*[VGroup(T(a_, size=28, color=th.AMBER, weight="BOLD"), para(b_, width=8.6, size=26, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for a_, b_ in items])
        pages = [VGroup(*rows[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-1.3, -0.2, 0]), VGroup(*rows[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-1.3, -0.2, 0])]
        with self.say("Part one. The tourist praises everything. The view from the plane: neat fields, coloured houses, an age old peace. The East, he says, has only ever given to the West, religion, art, civilisation, without any idea of ownership. He knows the history from books: the valley as a lake, Manjushri's sword, the monks' pure samyak gaze."):
            self.play(FadeIn(h), FadeIn(glass))
            for r_ in pages[0]:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), glass[1].animate.stretch(0.9, 1, about_edge=DOWN), run_time=0.6)
                self.hold(2.5)
        self.play(FadeOut(pages[0]))
        with self.say("He admires the carved houses, the harmony of Hindus and Buddhists, the momos, an old man telling his grandson stories. And above all the smile, and the eyes: carved windows, stupas, people. Nepal, he says, is a land of eyes."):
            for r_ in pages[1]:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), glass[1].animate.stretch(0.9, 1, about_edge=DOWN), run_time=0.6)
                self.hold(2.0)
        nt = para("\"one more drink before dinner\"", width=3.0, size=26, color=th.CORAL).next_to(glass, UP, buff=0.3)
        with self.say("And notice how his speech is punctuated by drinks: one more drink before dinner, cheers once again. The warmer the whisky, the warmer the praise. He ends: show me beautiful, full eyes. Come, let's go to eat dinner."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, glass, pages[1], nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "\"Today I am to show you some eyes\"")
        stops = [("Chobhar hill", "the gorge cut by Manjushri's sword", th.SKY), ("a rock drawing", "birds and a temple of no named religion", th.MINT), ("Adinath temple", "Shiva, the Buddha, prayer wheels: real tolerance — but he won't stop here", th.AMBER), ("a farmer's house", "half the harvest to a city landlord; no momos, no stories", th.CORAL)]
        pts = [np.array([-5.0 + 3.3 * k, -0.2 + 0.5 * (k % 2), 0]) for k in range(4)]
        path = VMobject(stroke_color=th.FAINT, stroke_width=4).set_points_smoothly(pts)
        dots = VGroup(*[Dot(p_, radius=0.14, color=c_) for p_, (_, _, c_) in zip(pts, stops)])
        labs = VGroup(*[VGroup(T(a_, size=26, color=c_, weight="BOLD"), para(b_, width=2.9, size=22, color=th.BODY)).arrange(DOWN, buff=0.1).next_to(p_, UP if k % 2 == 0 else DOWN, buff=0.3) for k, (p_, (a_, b_, c_)) in enumerate(zip(pts, stops))])
        with self.say("Part two. Come, my guest, says the guide; today I am to show you some eyes. He takes the tourist up Chobhar hill, past the gorge of the Manjushri legend, past a village artist's drawing of birds and a temple of no named religion, to the Adinath temple, where Shiva and the Buddha stand together and children play. The tourist would call it living tolerance. The guide agrees, but will not stop there. He climbs on, to a farmer's family who pay half their harvest to a landlord in the city."):
            self.play(FadeIn(h), Create(path))
            for d_, l_ in zip(dots, labs):
                self.play(FadeIn(d_, scale=1.5), FadeIn(l_), run_time=0.6)
                self.hold(2.0)
        self.play(FadeOut(VGroup(h, path, dots, labs)))
        h = E.head(self, "The boy who can neither give nor take")
        eye_l = VGroup(Ellipse(width=1.6, height=0.7, stroke_color=th.INK, stroke_width=4), Circle(radius=0.22, color=th.INK, fill_opacity=0.9)).move_to([-1.1, 1.0, 0])
        eye_r = eye_l.copy().move_to([1.1, 1.0, 0])
        facts = E.bullets(["a boy with polio: he cannot speak, move his hands, chew or spit", "only his eyes are alive — a blank, listless look", "\"Here is a child who can neither give nor take anything at all\"", "the guide told the parents the tourist is a doctor: they smile with faith, \"as if he were their eldest son\""], width=11.4, size=24).move_to([0, -1.5, 0])
        with self.say("In the house is a child with polio. He cannot speak, move his hands, chew, or even spit. Only his eyes are alive. The tourist said the East is always giving to the West. Here, says the guide, is a child who can neither give nor take anything at all. And he confesses: he told the parents the tourist is a doctor. Now they smile at him with faith, as if he were their eldest son, home with a cure from across the seven seas. Every one of the tourist's phrases, turned inside out."):
            self.play(FadeIn(h), FadeIn(eye_l), FadeIn(eye_r))
            E.reveal_list(self, facts, 12.0)
        self.play(FadeOut(VGroup(h, eye_l, eye_r, facts)))
        h = E.head(self, "The sister, and a light in his eyes")
        txt = E.bullets(["his healthy little sister crawls, falls, knocks over the beer", "for a moment his eyes want to copy her — then indifference", "when she is scolded, a light gleams: how sweet to fall, to cry, to break something, to learn fire burns", "in her, words carry a culture forward; in him, \"the future ends\""], width=11.4, size=26).move_to([0, 0.0, 0])
        with self.say("The boy has a little sister who crawls about, falls, knocks things over. For a moment his eyes want to copy her, then sink back into indifference. When their mother scolds her, a light gleams in his eyes, and the guide imagines what he would say: how sweet it would be to fall and scrape a knee, to cry, to break something and feel guilty, to learn that fire burns. In the sister, words carry a whole culture forward. In him, the chain of human development ends."):
            self.play(FadeIn(h))
            E.reveal_list(self, txt, 12.0)
        self.play(FadeOut(VGroup(h, txt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "The same country, seen twice")
        L = ["evening, over drinks", "the East \"only gives\"", "peace, harmony, smiles", "history from books", "the Buddha's eyes, carved windows", "\"show me beautiful eyes\""]
        R = ["next day, sober", "a child who can \"neither give nor take\"", "poverty, helplessness", "the pulse of reality", "the eyes of a paralysed boy", "eyes \"in which hides the end of life\""]
        lh = T("the tourist", size=30, color=th.AMBER, weight="BOLD").move_to([-3.3, 2.1, 0])
        rh = T("the guide", size=30, color=th.SKY, weight="BOLD").move_to([3.3, 2.1, 0])
        lc = VGroup(*[T(t_, size=24, color=th.INK) for t_ in L]).arrange(DOWN, buff=0.33).next_to(lh, DOWN, buff=0.4)
        rc = VGroup(*[T(t_, size=24, color=th.INK) for t_ in R]).arrange(DOWN, buff=0.33).next_to(rh, DOWN, buff=0.4)
        mid = DashedLine([0, 2.3, 0], [0, -2.9, 0], color=th.FAINT)
        with self.say("Put the two speeches side by side. Evening, over drinks, against the next day, sober. The East that only gives, against a child who can neither give nor take. Peace and smiles, against poverty and helplessness. History from books, against the pulse of reality. The Buddha's eyes, against the eyes of a paralysed boy."):
            self.play(FadeIn(h), FadeIn(lh), FadeIn(rh), Create(mid))
            for a_, b_ in zip(lc, rc):
                self.play(FadeIn(a_), FadeIn(b_), run_time=0.5)
                self.hold(1.0)
        self.play(FadeOut(VGroup(h, lh, rh, lc, rc, mid)))
        cards = VGroup(
            E.card("The tourist", "not a villain: generous, eager to love the place. But he sees only what he expected, and turns people into a picture. His fault is sentimentality — a kind of blindness.", th.AMBER, w=6.1, h=3.9, size=24),
            E.card("The guide", "silent in Part One; ironic, sober, polite — and angry underneath. Morally complicated: he lies to the parents and uses the child, while insisting the boy is not a \"symbol\".", th.SKY, w=6.1, h=3.2, size=24),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.2, 0])
        with self.say("The two men. The tourist is not a villain; he is generous and wants to love the place. But he sees only what he came expecting, and turns living people into a postcard: his fault is sentimentality, which is a kind of blindness. The guide is ironic, patient and quietly angry. And he is morally complicated: he lies to the parents, and uses the boy to teach a lesson, while insisting the boy is not a symbol. That unease is part of the story's honesty."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=3)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Seeing and not seeing", "the samyak gaze means seeing things as they are; it belongs to whoever looks at the whole picture", th.SKY, w=6.1, h=2.75, size=24),
            E.card("East and West", "\"the East gives, the West takes\": flattering, but it turns people into a type — what critics call Orientalism", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Poverty behind the postcard", "no smoke, no momos, no stories: the rural poor that tourism leaves out", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Harmony — and its limits", "the Adinath temple's real tolerance, which the guide accepts but will not stop at", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Seeing and not seeing: the samyak gaze, the Buddhist ideal of seeing things as they are, belongs not to the tourist who claims it, but to whoever looks at the whole picture. East and West: the claim that the East only gives is flattering, but it turns real people into a type. Critics call this habit Orientalism. Poverty behind the postcard. And harmony: the guide accepts that Nepal's tolerance is real, but refuses to stop there."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        df = E.card("Orientalism (in outline)", "Edward Said's term (1978) for picturing Asia as exotic, spiritual, unchanging and passive. Lamichhane's story, from 1962, criticises the habit sixteen years earlier.", th.PINK, w=10.0, h=2.6).move_to([0, 0.3, 0])
        with self.say("Orientalism is the critic Edward Said's word, from nineteen seventy eight, for imagining Asia as exotic, spiritual, timeless and passive. Lamichhane's story criticises that habit sixteen years before the word existed."):
            self.play(FadeIn(df))
        self.play(FadeOut(df))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "The last sentence: beauty and suffering in one picture")
        se = stupa_eyes(0.9).move_to([-3.4, 1.0, 0])
        ce = VGroup(Ellipse(width=1.3, height=0.6, stroke_color=th.INK, stroke_width=4), Circle(radius=0.2, color=th.INK, fill_opacity=0.9)).move_to([2.6, 1.0, 0])
        ce2 = ce.copy().move_to([4.4, 1.0, 0])
        eq = T("=", size=60, color=th.AMBER).move_to([0.2, 1.0, 0])
        q = para("\"Look! They are just as beautiful as the setting sun's reflection in the eyes of the Buddha!\"", width=11, size=28, color=th.AMBER).move_to([0, -0.8, 0])
        with self.say("The guide ends by describing the boy's eyes in the tourist's own language: eyes surrounded by mountains, eyes that welcome, eyes in which hides the end of life. And then the final sentence: Look! They are just as beautiful as the setting sun's reflection in the eyes of the Buddha. Beauty and suffering, joined into one picture."):
            self.play(FadeIn(h), FadeIn(se))
            self.play(FadeIn(eq), FadeIn(ce), FadeIn(ce2))
            self.play(FadeIn(q))
        nt = para("Bitter irony — he means the opposite of \"beautiful\" — and, at the same time, a demand to look at the whole of Nepal. The sinking sun is that ending.", width=11, size=24, color=th.MINT).move_to([0, -2.4, 0])
        with self.say("It is bitter irony: he does not mean beautiful the way the tourist meant it. And at the same time it is a demand that the tourist look at the whole of Nepal, the Buddha and the boy together. The slowly sinking sun of the title is that ending of life."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, se, ce, ce2, eq, q, nt)))
        rows = [["irony", "endurance \"only in an Easterner\"", "praise turned to accusation"], ["symbol", "the Buddha's eyes; the sunset", "peace; an ending"], ["contrast", "drunk vs sober; books vs a hut", "the whole structure"],
                ["dramatic monologue", "two speakers, two silent listeners", "character revealed by voice"], ["motif", "eyes, again and again", "binds the two halves"], ["imagery", "fields like eyelashes", "the land becomes a face"]]
        E.device_slide(self, rows, "Devices to quote. Irony: the guide repeats the tourist's own praise, that only an Easterner could endure such a fate without complaint, and turns it into an accusation. Symbols: the Buddha's eyes, the boy's eyes, the setting sun. Contrast in every pairing. Two dramatic monologues. The motif of eyes. And imagery that turns the land into a face.", widths=(2.9, 5.6, 3.9), size=22)
        self.quiz("How is the story structured?",
                  ["one narrator tells all", "two monologues, no replies", "a diary", "a series of letters"], 1,
                  "Pause and think.",
                  "The tourist speaks in Part One, the guide in Part Two; neither listener answers.")
        self.quiz("What is the tourist's main weakness?",
                  ["cruelty", "sentimentality that blinds him", "greed", "rudeness"], 1,
                  "One more.",
                  "He is kind but sees only the romantic picture he expected — the poverty is invisible to him.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Shankar Lamichhane (1928–1976); this story 1962; trans. Michael Hutt.",
            "Part One: the tourist, over whisky, praises a peaceful, \"giving\" land of eyes.",
            "Part Two: the guide shows a paralysed boy who \"can neither give nor take\".",
            "Themes: seeing vs not seeing, Orientalism, poverty behind the postcard.",
            "Irony and the eyes: \"just as beautiful as the setting sun's reflection\".",
        ], "Quick recap. Lamichhane, and a story from nineteen sixty two. A tourist's whisky-warm praise. A guide's sober reply: a boy who can neither give nor take. Seeing against not seeing, East against West. And the bitter irony of the eyes.")
        self.outro("That was The Half closed Eyes of the Buddha and the Slowly Sinking Sun. Next, an old man with enormous wings falls into a muddy courtyard: Gabriel García Márquez. See you there.")
