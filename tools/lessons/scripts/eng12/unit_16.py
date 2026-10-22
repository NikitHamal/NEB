import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def balloon(label, color, r=0.7):
    b = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
    s = Line(b.get_bottom(), b.get_bottom() + DOWN * 0.6, color=th.MUTED, stroke_width=2)
    t = T(label, size=22, color=color).move_to(b)
    t.scale_to_fit_width(min(t.width, 2 * r - 0.15))
    return VGroup(b, s, t)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 16
    TITLE = "Humility"
    SUBTITLE = "Yuval Noah Harari · an essay"
    SECTIONS = ["Harari and the claim", "Everyone thinks they are the centre", "\"All these claims are false\"", "My own people: the yoga story", "Themes", "How the essay works"]
    NEXT = "Unit 17 · Human Rights and the Age of Inequality"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        names = [("Greeks", th.SKY), ("China", th.CORAL), ("India", th.AMBER), ("Islam", th.MINT), ("Britain", th.PINK), ("Aztecs", th.LIME)]
        bs = VGroup(*[balloon(n_, c_) for n_, c_ in names]).arrange(RIGHT, buff=0.4).move_to([0, 0.4, 0])
        q = para("Every group likes to believe its story is the most important story ever told.", width=11, size=30, color=th.INK).move_to([0, -2.2, 0])
        with self.say("Every group of people likes to believe that its story is the most important story ever told. Greeks say history began in Athens. Chinese nationalists say it began with the Yellow Emperor. The Aztecs believed the sun would not rise without their sacrifices."):
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.3) for b_ in bs], lag_ratio=0.2))
            self.play(FadeIn(q))
        with self.say("Yuval Noah Harari collects these claims, and then turns the same lens on his own people. And at the end he hands you a pin, to puncture your own group's balloon."):
            self.play(bs[0].animate.scale(0.2).set_opacity(0), run_time=0.6)
            nb = E.neby_in(self, "laugh", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(bs, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 16: Humility, by Yuval Noah Harari."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Harari and his claim. Everyone thinks they are the centre. All these claims are false. My own people, and the yoga story. The themes. And how the essay works.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Yuval Noah Harari (born 1976)")
        facts = E.bullets(["Israeli historian; doctorate at Oxford", "professor at the Hebrew University of Jerusalem", "Sapiens (2014), Homo Deus (2016), 21 Lessons for the 21st Century (2018)", "this essay: from 21 Lessons, chapter 12, \"You are not the centre of the world\""], width=7.6, size=24).move_to([-2.4, 0.3, 0])
        warn = E.card("he reports, not endorses", "when he lists a group's boast, he is showing it is absurd. Write \"some nationalists claim…\", never \"Harari says…\"", th.CORAL, w=4.4, h=3.4, size=24).move_to([4.4, 0.2, 0])
        with self.say("Yuval Noah Harari is an Israeli historian, professor at the Hebrew University of Jerusalem, and author of Sapiens, a best selling history of humankind. This essay comes from his book 21 Lessons for the 21st Century, from a chapter titled You are not the centre of the world. One warning first: when he lists a group's boast, he is reporting it to show it is absurd, not endorsing it. In answers, write some nationalists claim, never Harari says."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 8.0)
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(h, facts, warn)))
        h = E.head(self, "The thesis")
        q = E.quote("Most people tend to believe they are the centre of the world, and their culture is the linchpin of human history.", "Harari", width=10, size=32).move_to([0, 0.8, 0])
        pin = para("A linchpin is the pin through an axle that keeps the wheel on. Each group thinks its culture is that pin.", width=10, size=26, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("His thesis: most people tend to believe they are the centre of the world, and their culture is the linchpin of human history. A linchpin is the small pin through an axle that keeps the wheel from falling off. Every group believes that its own culture is that pin."):
            self.play(FadeIn(h), FadeIn(q))
            self.play(FadeIn(pin))
        self.play(FadeOut(VGroup(h, q, pin)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "The catalogue of claims")
        claims = [("Greeks", "history began with Homer and Plato; every idea born in Athens", th.SKY),
                  ("Chinese nationalists", "it began with the Yellow Emperor; others are pale copies", th.CORAL),
                  ("Hindu nativists", "ancient sages invented aeroplanes, rockets, nuclear weapons", th.AMBER),
                  ("pious Muslims", "history before the Prophet is irrelevant; after, it revolves round the ummah", th.MINT),
                  ("Europeans and others", "without us, all would live in barbarous ignorance", th.PINK),
                  ("the Aztecs", "without our sacrifices the sun would not rise", th.LIME)]
        cards = VGroup(*[E.card(a_, b_, c_, w=4.0, h=2.3, tsize=26, size=22) for a_, b_, c_ in claims]).arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.25)).move_to([0, -0.1, 0])
        with self.say("Then the catalogue. Many Greeks believe history began with Homer and Plato. Chinese nationalists retort that it began with the Yellow Emperor, and that everyone else's achievements are pale copies. Some Hindu nativists claim that ancient sages invented aeroplanes and nuclear weapons. Pious Muslims see history before the Prophet as largely irrelevant; Turkish, Iranian and Egyptian nationalists add that their own nation was the fountainhead. British, French, Germans, Americans and Japanese are each convinced that without them humankind would live in barbarous ignorance. And the Aztecs believed the sun would not rise without their sacrifices."):
            self.play(FadeIn(h))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.6)
                self.hold(2.6)
        self.play(FadeOut(VGroup(h, cards)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "\"All these claims are false\"")
        v = T("wilful ignorance of history  +  \"more than a hint of racism\"", size=28, color=th.CORAL).move_to([0, 2.0, 0])
        v.scale_to_fit_width(min(v.width, 12.2))
        tl = E.timeline(["humans colonise the world", "plants and animals tamed", "first cities", "writing and money", "… today's nations and religions"], x0=-6.2, x1=6.2, y=-0.2, colors=[th.MINT, th.MINT, th.MINT, th.MINT, th.MUTED], size=22, wrap=2.3)
        nt = T("none of today's nations or religions existed for the first four", size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("The verdict is one short sentence: all these claims are false. They combine a wilful ignorance of history with more than a hint of racism. Why? None of today's religions or nations existed when humans colonised the world, tamed plants and animals, built the first cities, or invented writing and money. Those steps were taken long before any of them."):
            self.play(FadeIn(h), FadeIn(v))
            self.play(GrowArrow(tl.line), LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.4), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, v, tl, nt)))
        h = E.head(self, "What is truly universal")
        four = VGroup(*[E.chip(t_, c_, size=30) for t_, c_ in [("morality", th.SKY), ("art", th.PINK), ("spirituality", th.AMBER), ("creativity", th.MINT)]]).arrange(RIGHT, buff=0.35).move_to([0, 1.0, 0])
        src = T("born in Stone Age Africa — shared by all humans", size=28, color=th.INK).move_to([0, -0.4, 0])
        nt = para("To place them in the age of the Yellow Emperor, Plato or Muhammad is \"crass egotism\". (\"In our DNA\" is Harari's vivid way of saying: part of being human.)", width=11, size=24, color=th.AMBER).move_to([0, -2.1, 0])
        with self.say("Then the positive truth. Morality, art, spirituality and creativity are universal human abilities, embedded, he says, in our DNA: his vivid way of saying they are part of being human. They were born in Stone Age Africa, and they belong to everyone. To place their origin in China in the age of the Yellow Emperor, or Greece in the age of Plato, or Arabia in the age of Muhammad, is crass egotism."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(f_, scale=0.8) for f_ in four], lag_ratio=0.25))
            self.play(FadeIn(src))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, four, src, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "\"The Jews, my own people\"")
        q = E.quote("Name any human achievement or invention, and they will quickly claim credit for it.", "Harari, on his own people", width=10, size=30).move_to([0, 1.2, 0])
        nt = para("Now the essay turns personal: the same crass egotism, at home.", width=10, size=28, color=th.AMBER).move_to([0, -1.4, 0])
        with self.say("Now Harari makes it personal. He is all too familiar with such crass egotism, he says, because the Jews, his own people, also think they are the most important thing in the world. Name any human achievement, and they will quickly claim credit for it, and they are genuinely convinced."):
            self.play(FadeIn(h), FadeIn(q))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(q, nt)))
        steps = [("the claim", "a yoga teacher: Abraham invented yoga, from Hebrew letter shapes", th.SKY),
                 ("the route", "a concubine's son took it east to India", th.AMBER),
                 ("the \"evidence\"", "Genesis 25:6: Abraham gave them \"gifts\" and sent them east", th.MINT),
                 ("the punchline", "\"What do you think these gifts were?\"", th.CORAL)]
        cards = VGroup(*[E.card(a_, b_, c_, w=2.95, h=3.2, tsize=26, size=24) for a_, b_, c_ in steps]).arrange(RIGHT, buff=0.18).move_to([0, -0.1, 0])
        arr = VGroup(*[Arrow(cards[k].get_right(), cards[k + 1].get_left(), buff=0.0, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5) for k in range(3)])
        nt = T("a gift in a verse → yoga: evidence that proves nothing, taken with total seriousness", size=24, color=th.MUTED).move_to([0, -2.4, 0])
        nt.scale_to_fit_width(min(nt.width, 12.2))
        with self.say("Then the yoga story. A yoga teacher in Israel explained, in all seriousness, that yoga was invented by Abraham, and that the postures come from the shapes of the Hebrew letters. Abraham taught them to the son of one of his concubines, who went to India and taught the Indians. The evidence? A Bible verse: Abraham gave the sons of his concubines gifts and sent them east. What do you think these gifts were? The joke is the leap from a gift in a verse to yoga."):
            for k, c_ in enumerate(cards):
                self.play(FadeIn(c_, shift=UP * 0.2), *([GrowArrow(arr[k - 1])] if k else []), run_time=0.6)
                self.hold(2.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(cards, arr, nt)))
        a = E.card("the escalation", "Orthodox belief: the whole cosmos exists so rabbis can study scripture — stop, and galaxies end. Secular Jews too see their people as history's heroes.", th.PINK, w=5.8, h=3.0, size=24).move_to([-3.2, 0.3, 0])
        b = E.card("the method", "\"it is more polite to criticise one's own people than … foreigners\" — so readers can \"puncture the hot-air balloons inflated by their own tribes\"", th.AMBER, w=5.8, h=3.0, size=24).move_to([3.2, 0.3, 0])
        with self.say("He goes further. Mainstream Orthodox Judaism holds that the whole cosmos exists so that rabbis can study their scriptures, and that if they stopped, even distant galaxies would be annihilated. Secular Jews, too, see their people as the central heroes of history. Why choose his own people? Because it is more polite to criticise one's own people than foreigners. He leaves it to readers everywhere to puncture the hot air balloons inflated by their own tribes."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(h, a, b)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Egocentrism of nations", "every group thinks it is central: a natural habit, and a dangerous one", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Humility as honesty", "not shyness: checking proud claims against evidence — \"what is the proof?\"", th.SKY, w=6.1, h=2.75, size=24),
            E.card("A shared human heritage", "morality, art, spirituality, creativity belong to all — so others' achievements are ours too", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Criticise yourself first", "starting with his own people earns the right to ask everyone else", th.AMBER, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. The egocentrism of nations: a natural habit, and a dangerous one, because it justifies contempt for others. Humility as honesty about evidence: ask of any proud claim, what is the proof? A shared human heritage: if these abilities belong to all of us, then other people's achievements are, in a real sense, ours too. And criticise yourself first, which earns the right to ask everyone else to do the same."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        h = E.head(self, "Why is history a contested issue?")
        pts = E.bullets(["every group tells history with itself at the centre", "such stories feed national pride and identity — so they are defended fiercely", "evidence is ignored when it threatens the story", "Harari's answer: test claims against evidence, and remember what is shared"], width=11.2, size=26).move_to([0, 0.0, 0])
        with self.say("The favourite long question: why is history a contested issue? Because every group tells it with itself at the centre. Those stories feed national pride, so they are defended fiercely, and evidence is ignored when it threatens the story. Harari's answer is humility: test every claim against evidence, and remember what all humans share."):
            self.play(FadeIn(h))
            E.reveal_list(self, pts, 9.0)
        self.play(FadeOut(VGroup(h, pts)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["satire", "\"Did you know …?\"", "a boast made absurd"], ["catalogue", "Greeks, China, India, Islam, Europe, Aztecs", "a universal habit"], ["irony", "\"What do you think these gifts were?\"", "the proof proves nothing"],
                ["metaphor", "the linchpin of history", "\"we hold the wheel on\""], ["metaphor", "\"hot-air balloons\"", "inflated pride, easily punctured"], ["short verdict", "\"All these claims are false.\"", "the turn of the argument"]]
        E.device_slide(self, rows, "Devices to quote. Satire: mock surprise, did you know that rockets were invented by an ancient sage? A catalogue that shows a universal habit. Irony in the yoga punchline. Two metaphors: the linchpin, and hot air balloons waiting to be punctured. And a short, blunt verdict: all these claims are false.", widths=(2.6, 5.4, 4.4), size=24)
        self.quiz("Which abilities does Harari call universal, born in Stone Age Africa?",
                  ["writing and money", "morality, art, spirituality and creativity", "farming and cities", "science and rockets"], 1,
                  "Pause and think.",
                  "Morality, art, spirituality and creativity — shared by all humans, owned by no nation.")
        self.quiz("Why does Harari use his own people as the main example?",
                  ["they are the most important", "it is more polite to criticise one's own people", "he dislikes them", "they invented yoga"], 1,
                  "One more.",
                  "Criticising your own tribe first is fair — and invites readers to do the same.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Yuval Noah Harari (b. 1976); from 21 Lessons for the 21st Century (2018).",
            "Every group thinks its culture is the linchpin of history.",
            "\"All these claims are false\": ignorance of history and a hint of racism.",
            "Morality, art, spirituality, creativity: universal, born in Stone Age Africa.",
            "His own people first: the yoga story; puncture your own tribe's balloon.",
        ], "Quick recap. Harari and the linchpin of history. A catalogue of national boasts. All these claims are false. What is truly universal. And a historian who criticises his own people first.")
        self.outro("That was Humility. Next, the last essay: Human Rights and the Age of Inequality. See you there.")
