import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def bull(color=th.INK, s=1.0, dead=False):
    body = Ellipse(width=2.6, height=1.2, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    head = Ellipse(width=0.9, height=0.7, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15).next_to(body, RIGHT, buff=-0.25).shift(UP * 0.35)
    horns = VGroup(Arc(radius=0.3, start_angle=PI / 2, angle=PI / 2, color=color, stroke_width=4).next_to(head, UP, buff=-0.05).shift(LEFT * 0.2), Arc(radius=0.3, start_angle=0, angle=PI / 2, color=color, stroke_width=4).next_to(head, UP, buff=-0.05).shift(RIGHT * 0.2))
    legs = VGroup(*[Line([x, -0.5, 0], [x, -1.2, 0], color=color, stroke_width=4) for x in (-0.9, -0.5, 0.5, 0.9)])
    g = VGroup(body, head, horns, legs).scale(s)
    if dead:
        g.rotate(PI)
    return g


def bowing(color=th.SKY, s=1.0):
    """A stick figure bowing low before the king."""
    hip = np.array([0, -0.6, 0])
    shoulder = hip + np.array([0.75, 0.55, 0])
    body = Line(hip, shoulder, color=color, stroke_width=4)
    head = Circle(radius=0.22, stroke_color=color, stroke_width=4).move_to(shoulder + np.array([0.28, -0.08, 0]))
    legs = VGroup(Line(hip, hip + np.array([-0.15, -0.9, 0]), color=color, stroke_width=4), Line(hip, hip + np.array([0.12, -0.9, 0]), color=color, stroke_width=4))
    arms = Line(shoulder, shoulder + np.array([0.15, -0.65, 0]), color=color, stroke_width=4)
    return VGroup(body, head, legs, arms).scale(s)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 20
    TITLE = "The Bull"
    SUBTITLE = "Bhimnidhi Tiwari · a one-act play"
    SECTIONS = ["Tiwari, the king and chakari", "The news", "The lie", "The show", "Characters", "Satire on feudalism"]
    NEXT = "Unit 21 · Question Tags and Questions"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        b = bull(th.AMBER).move_to([0, 0.4, 0])
        lab = T("Male — the king's bull", size=28, color=th.AMBER).next_to(b, DOWN, buff=0.5)
        q = para("The bull is dead. Nobody is sad. Everybody is terrified.", width=11, size=32, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("Kathmandu, seventeen ninety seven. The king's favourite bull, Male, has died in the night. Nobody is sad. Everybody is terrified, because the king is fond of the bull, and quick to punish."):
            self.play(FadeIn(b), FadeIn(lab))
            b.generate_target()
            b.target.rotate(PI).shift(DOWN * 0.4)
            self.play(MoveToTarget(b), run_time=1.5)
            self.play(FadeIn(q))
            nb = E.neby_in(self, "oops", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(b, lab, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 20: The Bull, a one act comedy by the Nepali writer Bhimnidhi Tiwari, the only play in your book about Nepal."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Tiwari, the king, and the word chakari. The news. The lie. The show. The characters. And the satire on feudalism.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Bhimnidhi Tiwari (1911–1973)")
        facts = E.bullets(["poet, dramatist and social reformer from Kathmandu", "founded the Nepali Sahitya Press and the Nepal Natak Sangh (drama society)", "Madan Puraskar (BS 2017) for Bisphot, on social injustice", "more than thirty-eight works; wrote against smoking, drinking, gambling"], width=8.0, size=24).move_to([-2.0, 0.4, 0])
        with self.say("Bhimnidhi Tiwari was a Nepali poet, dramatist and social reformer, born in Kathmandu in nineteen eleven. He founded a press and the Nepal Natak Sangh, a drama society that encouraged Nepali plays, and won the Madan Puraskar for Bisphot, a collection about social injustice."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 7.0)
        self.play(FadeOut(VGroup(h, facts)))
        h = E.head(self, "Background you need")
        cards = VGroup(
            E.card("the king", "Ranabahadur Shah, 23, grandson of Prithvi Narayan Shah: absolute, proud, sudden in anger", th.AMBER, w=3.95, h=3.2, size=24),
            E.card("chakari", "flattering and serving the powerful, or pleading your poverty, to win favour or protection", th.SKY, w=3.95, h=3.2, size=24),
            E.card("satire", "humour, irony and exaggeration that expose the faults of people or institutions — to correct them", th.MINT, w=3.95, h=3.2, size=24),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.1, 0])
        nt = para("Its target: the feudal system — a king and lords hold the power; common people owe service and have few rights.", width=11.4, size=24, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("Three things you need. The king is Ranabahadur Shah, twenty three, grandson of Prithvi Narayan Shah: absolute, proud, and sudden in anger. Chakari means flattering and serving the powerful, or pleading your poverty before them, to win favour; in this play everyone practises it. And satire uses humour, irony and exaggeration to expose faults, in order to correct them. The target here is the feudal system, in which a king and lords hold the power and common people have few rights."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, cards, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Dawn, Laxminarayan's yard")
        a = E.card("Laxminarayan", "the king's bull-doctor, a court officer with seven wives — and not one brings him his hookah", th.AMBER, w=5.6, h=2.6, size=24).move_to([-3.2, 1.0, 0])
        b = E.card("the news", "the cowherds Jitman and Gore run in: Male has died. The king has threatened to punish anyone who lets the bull die.", th.CORAL, w=5.6, h=2.6, size=24).move_to([3.2, 1.0, 0])
        with self.say("The play opens at dawn in the yard of Laxminarayan, the king's bull doctor, who is grumbling that not one of his seven wives has brought him his hookah. The cowherds Jitman and Gore run in with the news: Male is dead. All three are terrified; the king has threatened to punish anyone who lets the bull die."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
        rows = [["the bull", "the cowherds"], ["fine rice and lentil soup", "hungry"], ["a mattress, a quilt", "straw, in winter"], ["a mosquito net", "nothing"]]
        tb = E.table(rows, [5.0, 5.0], row_h=0.58, size=24, colors=[th.AMBER, th.SKY]).move_to([0, -1.9, 0])
        with self.say("The cowherds say it died of rich food: fine rice and lentil soup instead of grass. And they resent it. The bull had a mattress, a quilt and a mosquito net, while they sleep on straw in winter. Here is the satire's sharpest fact: an animal treated better than the men who serve it.") as v:
            E.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(VGroup(h, a, b, tb)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "The Basantapur palace")
        king = VGroup(Circle(radius=0.35, stroke_color=th.AMBER, stroke_width=3), Polygon([-0.3, 0.3, 0], [-0.15, 0.6, 0], [0, 0.35, 0], [0.15, 0.6, 0], [0.3, 0.3, 0], stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.6),
                      Line([0, -0.35, 0], [0, -1.4, 0], color=th.AMBER, stroke_width=4), Line([0, -1.4, 0], [-0.3, -2.2, 0], color=th.AMBER, stroke_width=4), Line([0, -1.4, 0], [0.3, -2.2, 0], color=th.AMBER, stroke_width=4)).move_to([4.4, 0.4, 0])
        kl = T("the king", size=24, color=th.AMBER).next_to(king, DOWN, buff=0.2)
        lx = VGroup(bowing(th.SKY), T("Laxminarayan", size=22, color=th.SKY).shift(DOWN * 1.9)).move_to([1.6, 0.0, 0])
        lie = E.bullets(["\"the bull is ill\": it won't get up, eat, move or speak; its eyes are fixed and still", "every symptom is true — of a dead bull", "praise: its beauty, its gait, its courage", "a cure: a change of climate in the hills — so it can \"die\" far away"], width=6.2, size=24).move_to([-3.2, -0.2, 0])
        with self.say("At the palace Laxminarayan bows low and tells a careful lie: the bull is ill. It will not get up, eat, move or speak, and its eyes are fixed and still. Every symptom is true, of a dead bull. He praises the bull's beauty and courage, a perfect piece of chakari, and suggests a change of climate in the hills, so that it can die conveniently far away."):
            self.play(FadeIn(h), FadeIn(king), FadeIn(kl), FadeIn(lx))
            E.reveal_list(self, lie, 9.0)
        nt = para("The king agrees — then changes his mind: he will go and see the bull himself, with his convoy.", width=11, size=26, color=th.CORAL).move_to([0, -2.7, 0])
        with self.say("The king agrees. Then he changes his mind. He will go and see the bull himself, at Thulo Gauchar, the royal pasture, with his whole convoy."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, king, kl, lx, lie, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Thulo Gauchar: nursing a corpse")
        b = bull(th.MUTED, s=0.9, dead=True).move_to([-3.2, -0.6, 0])
        ground = Line([-5.4, -1.25, 0], [-1.0, -1.25, 0], color=th.FAINT, stroke_width=3)
        b = VGroup(b, ground)
        acts = E.bullets(["the cowherds think of running — they'd be caught", "Laxminarayan runs ahead: massage its back feet! fan it!", "the king calls the bull by name; no breath, tail loose, ears dropped", "\"it is dead\""], width=6.0, size=24).move_to([3.2, -0.2, 0])
        with self.say("At the cowshed the cowherds think of running away, but they know they would be caught. Laxminarayan runs ahead of the convoy and orders them to massage the bull's back feet and fan it, as if it were alive. The king arrives and calls the bull by name. No breath. The tail has gone loose, the ears have dropped. It is dead, he says."):
            self.play(FadeIn(h), FadeIn(b))
            E.reveal_list(self, acts, 9.0)
        self.play(FadeOut(VGroup(b, acts)))
        rows = [["who", "performs", "reward"], ["Jitman", "\"I am an orphan now!\"", "Rs 400"], ["Gore", "\"dearer than my family — I'll hang myself!\"", "Rs 500"], ["Laxminarayan", "weeps too", "the last rites"]]
        tb = E.table(rows, [2.8, 7.0, 3.0], row_h=0.7, size=24, colors=[th.SKY, th.INK, th.AMBER]).move_to([0, 0.4, 0])
        nt = para("They escape death by performing grief for an animal they resented — and are paid for it. The three thank God they are alive.", width=11, size=26, color=th.CORAL).move_to([0, -2.1, 0])
        with self.say("Then the show. The cowherds burst into loud weeping. Jitman cries that he is an orphan now; the king gives him four hundred rupees. Gore says the bull was dearer to him than his parents, wife and children, and that he will hang himself; he gets five hundred. Laxminarayan weeps too. They escape death by performing grief for an animal they resented, and are paid for it. The ending is funny, and bitter.") as v:
            E.reveal_table(self, tb, v.dur * 0.5)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Laxminarayan", "a tyrant at home, a slave at court: clever, fast — brave only from fear", th.AMBER, w=4.0, h=3.3, size=26),
            E.card("Jitman and Gore", "the common people: they work, sleep on straw — and weep on cue", th.SKY, w=4.0, h=3.3, size=26),
            E.card("the king", "young, absolute, quick to anger — easily moved by a show of loyalty", th.CORAL, w=4.0, h=3.3, size=26),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.2, 0])
        nt = para("And Male, the bull: dead from the start, never speaks — the pivot of the whole plot.", width=11, size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("The characters. Laxminarayan is the central comic figure: a bully at home and a slave at court, clever and quick, but with the courage of the frightened; he lies because he dares not tell the truth. Jitman and Gore are the voice of the common people: they do the work and sleep on straw, and they turn out to be excellent weepers when their lives depend on it. The king is young, absolute and easily moved by a show of loyalty. And the bull itself is dead from the start, the silent pivot of the plot."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(cards, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        cards = VGroup(
            E.card("Satire on feudalism", "a king's pet is worth more than the people who serve it", th.CORAL, w=6.1, h=2.6, size=24),
            E.card("Fear and dehumanisation", "subjects live in fear; human feeling becomes a performance", th.SKY, w=6.1, h=2.6, size=24),
            E.card("Chakari", "flattery and pleading run the whole system — up and down", th.AMBER, w=6.1, h=2.6, size=24),
            E.card("Say vs feel", "they howl for a bull they resent; the doctor nurses a corpse", th.MINT, w=6.1, h=2.6, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("The themes: every answer should mention them. Satire on feudalism: a king's pet is worth more than human beings. Fear and dehumanisation: subjects live in fear, and feeling itself becomes a performance. Chakari: flattery and pleading run the whole system. And the gap between what people say and what they feel, which is where the comedy lives."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(cards))
        rows = [["satire", "a bull with a mosquito net", "exposes the system"], ["irony", "every \"symptom\" is true of a corpse", "the lie that tells the truth"], ["exaggeration", "\"dearer than my wife and children\"", "comic, and bitter"],
                ["dramatic irony", "we know it's dead; the king doesn't", "suspense and comedy"], ["contrast", "mattress vs straw", "who is valued"], ["comic reversal", "they're rewarded for their \"grief\"", "the system rewards pretence"]]
        E.device_slide(self, rows, "Devices to quote. Satire: a bull with a mosquito net. Irony: every symptom Laxminarayan reports is true of a corpse. Comic exaggeration: dearer than my wife and children. Dramatic irony: we know the bull is dead and the king does not. Contrast: a mattress against straw. And comic reversal: the system rewards pretence.", widths=(3.0, 5.4, 4.0), size=22)
        self.quiz("What is \"chakari\"?",
                  ["a royal pasture", "flattering and serving the powerful to win favour", "a kind of bull", "a punishment"], 1,
                  "Pause and think.",
                  "Pleasing or pleading before the powerful for favour or protection — practised by everyone in the play.")
        self.quiz("Why are the cowherds rewarded at the end?",
                  ["for saving the bull", "for their loud show of grief", "for telling the truth", "for running away"], 1,
                  "One more.",
                  "The king pays Rs 400 and Rs 500 for performances of grief for an animal they resented.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Bhimnidhi Tiwari (1911–1973); Kathmandu, 1797; King Ranabahadur Shah.",
            "The bull Male is dead: a mattress and mosquito net vs straw for the cowherds.",
            "The lie: \"ill\" — every symptom true of a corpse; the king comes to see.",
            "The show: nursing a corpse, then rewarded weeping — Rs 400 and Rs 500.",
            "Satire on feudalism: fear, chakari, an animal above people.",
        ], "Quick recap. Tiwari's satire. A dead royal bull and its terrified keepers. A lie built from true symptoms. A show of grief that pays. And a feudal system that values a pet above people.")
        self.outro("That completes the literature. Next, grammar: question tags and questions. See you there.")
