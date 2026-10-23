import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

SLOTS = ["opinion", "size", "age", "shape", "colour", "origin", "material", "purpose"]


def ruler(y=0.6, w=12.4):
    n = len(SLOTS)
    cw = w / n
    boxes = VGroup(*[Rectangle(width=cw - 0.08, height=0.9, stroke_color=th.PALETTE[k % 8], stroke_width=3, fill_color=th.PALETTE[k % 8], fill_opacity=0.08).move_to([-w / 2 + cw * (k + 0.5), y, 0]) for k in range(n)])
    labs = VGroup(*[T(f"{k + 1} {s_}", size=20, color=th.PALETTE[k % 8]).next_to(b_, UP, buff=0.12) for k, (s_, b_) in enumerate(zip(SLOTS, boxes))])
    for l_, b_ in zip(labs, boxes):
        l_.scale_to_fit_width(min(l_.width, b_.width - 0.05))
    g = VGroup(boxes, labs)
    g.boxes = boxes
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 26
    TITLE = "Adjectives, Adverbs and Adjective Order"
    SUBTITLE = "Grammar · order, -ing/-ed, comparison, adverb position"
    SECTIONS = ["Where adjectives can stand", "The order of adjectives", "Bored or boring?", "Degrees of comparison", "Adverbs and their false friends", "Where an adverb stands"]
    NEXT = "Unit 27 · Reported Speech"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a = T("a woollen Nepali old beautiful shawl", size=38, color=th.CORAL).move_to([0, 1.0, 0])
        b = T("a beautiful old Nepali woollen shawl", size=38, color=th.MINT).move_to([0, -0.6, 0])
        with self.say("A woollen Nepali old beautiful shawl. Every word is right, and the phrase is wrong. Native speakers would never say it, though most could not tell you why."):
            self.play(FadeIn(a))
        nt = para("Grammar 12 is about the fussy details: the order of adjectives, bored vs boring, \"senior to\", and where an adverb may stand.", width=11, size=28, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("A beautiful old Nepali woollen shawl. English fixes the order of adjectives, and this unit gives you that order, along with the other fussy details the examiner actually tests: bored and boring, comparatives that take to, and where an adverb is allowed to stand."):
            self.play(TransformMatchingShapes(a.copy(), b), run_time=2)
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "cool", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 26: adjectives, adverbs and adjective order."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Where adjectives can stand. The order of adjectives. Bored or boring. Degrees of comparison. Adverbs and their false friends. And where an adverb is allowed to stand.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Before the noun, or after a linking verb")
        a = E.card("attributive", "before the noun: a tall boy", th.SKY, w=5.6, h=1.8, size=26).move_to([-3.2, 1.4, 0])
        b = E.card("predicative", "after a linking verb: the boy is tall", th.MINT, w=5.6, h=1.8, size=26).move_to([3.2, 1.4, 0])
        p_only = VGroup(T("predicative only", size=24, color=th.AMBER, weight="BOLD"), T("afraid, alive, asleep, alone, ashamed, aware, awake, alike, glad", size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([0, -0.4, 0])
        a_only = VGroup(T("attributive only", size=24, color=th.PINK, weight="BOLD"), T("main, only, mere, sheer, chief, former, latter, elder, eldest, inner, outer", size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(p_only, DOWN, buff=0.35).align_to(p_only, LEFT)
        ex = T("✗ the asleep child → ✓ the sleeping child   ·   ✗ He is elder than me → ✓ He is older than me", size=24, color=th.CORAL).move_to([0, -2.8, 0])
        ex.scale_to_fit_width(min(ex.width, 12.4))
        with self.say("Most adjectives can stand in two places: before the noun, a tall boy, or after a linking verb, the boy is tall. But a few are fixed. Afraid, alive, asleep, alone, aware and their family only come after the verb: the child was asleep, but never the asleep child; say the sleeping child. And main, only, mere, former, latter and elder only come before the noun: my elder brother, but never he is elder than me; say older."):
            self.play(FadeIn(h), FadeIn(a), FadeIn(b))
            self.play(FadeIn(p_only), FadeIn(a_only))
            self.play(FadeIn(ex))
        self.play(FadeOut(VGroup(h, a, b, p_only, a_only, ex)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Opinion · size · age · shape · colour · origin · material · purpose")
        r = ruler(y=0.9)
        words = [("woollen", 6), ("Nepali", 5), ("old", 2), ("beautiful", 0)]
        chips = VGroup(*[E.chip(w_, th.PALETTE[k % 8], size=26) for w_, k in words]).arrange(RIGHT, buff=0.4).move_to([0, -1.2, 0])
        result = T("a beautiful old Nepali woollen shawl", size=34, color=th.MINT, weight="BOLD").move_to([0, -2.6, 0])
        with self.say("Here is the order, in eight slots: opinion, size, age, shape, colour, origin, material, and purpose. Now sort the words: woollen is material, slot seven. Nepali is origin, slot six. Old is age, slot three. Beautiful is opinion, slot one. Read them in slot order, add the noun: a beautiful old Nepali woollen shawl."):
            self.play(FadeIn(h), FadeIn(r))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chips], lag_ratio=0.2))
            for (w_, k), c_ in zip(words, chips):
                self.play(c_.animate.move_to(r.boxes[k]).scale(0.85 if c_.width > r.boxes[k].width else 1.0), run_time=0.7)
            self.play(FadeIn(result))
        self.play(FadeOut(VGroup(chips, result)))
        ex = VGroup(*[T(t_, size=30, color=c_) for t_, c_ in [("a big red ball  — not a red big ball", th.INK), ("an old Italian leather jacket", th.INK), ("a small round wooden table", th.INK), ("a lovely long white cotton sari", th.INK)]]).arrange(DOWN, buff=0.3).move_to([0, -1.6, 0])
        nt = para("Commas only between adjectives of the same kind: a cold, wet, miserable morning. Numbers first: the first three chapters.", width=11.4, size=24, color=th.AMBER).move_to([0, -2.95, 0])
        ex.move_to([0, -0.95, 0])
        with self.say("More: a big red ball, size before colour, never a red big ball. An old Italian leather jacket. A small round wooden table. Two details. Adjectives of the same kind take commas: a cold, wet, miserable morning; adjectives of different kinds take none. And numbers come first: the first three chapters, not the three first."):
            for e_ in ex:
                self.play(FadeIn(e_, shift=UP * 0.1), run_time=0.5)
                self.hold(1.2)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, r, ex, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "-ing causes the feeling; -ed has it")
        pairs = [("The journey was tiring.", "The passengers were tired."), ("The film was boring.", "We were bored."), ("The result was disappointing.", "Her parents were disappointed."), ("an interesting lecture", "an interested listener"), ("a frightening noise", "a frightened child")]
        left = VGroup(*[T(a_, size=28, color=th.AMBER) for a_, _ in pairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, -0.1, 0])
        right = VGroup(*[T(b_, size=28, color=th.SKY) for _, b_ in pairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, -0.1, 0])
        for l_, r_ in zip(left, right):
            r_.set_y(l_.get_y())
        lh = T("-ing: the cause", size=28, color=th.AMBER, weight="BOLD").next_to(left, UP, buff=0.4)
        rh = T("-ed: the person who feels", size=28, color=th.SKY, weight="BOLD").next_to(right, UP, buff=0.4)
        with self.say("Participle adjectives. The ing form describes what causes the feeling; the ed form describes the person who has it. The journey was tiring; the passengers were tired. The film was boring; we were bored. The result was disappointing; her parents were disappointed. An interesting lecture; an interested listener. A frightening noise; a frightened child."):
            self.play(FadeIn(h), FadeIn(lh), FadeIn(rh))
            for l_, r_ in zip(left, right):
                self.play(FadeIn(l_), FadeIn(r_), run_time=0.5)
                self.hold(1.3)
        self.play(FadeOut(VGroup(left, right, lh, rh)))
        wr = VGroup(E.wrong_right("I am very interesting in music.", "I am very interested in music.", size=30), E.wrong_right("The students were boring with the lesson.", "The students were bored with the lesson.", size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.2, 0])
        with self.say("So: I am very interesting in music says that you make music interesting for others. You mean: I am very interested in music. And the students were bored with the lesson, not boring."):
            for w_ in wr:
                self.play(FadeIn(w_.wrong))
                self.play(Create(w_.cross), FadeIn(w_.right))
        self.play(FadeOut(VGroup(h, wr)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        rows = [["rule", "positive", "comparative", "superlative"], ["one syllable: + er, est", "tall", "taller", "tallest"], ["double the consonant", "big", "bigger", "biggest"], ["-y → -i", "happy", "happier", "happiest"], ["two syllables or more", "beautiful", "more beautiful", "most beautiful"],
                ["irregular", "good / well", "better", "best"], ["irregular", "bad", "worse", "worst"], ["irregular", "far", "farther / further", "farthest / furthest"], ["irregular", "old", "older / elder", "oldest / eldest"]]
        tb = E.table(rows, [4.0, 2.6, 3.2, 3.0], row_h=0.58, size=24, colors=[th.MUTED, th.INK, th.SKY, th.MINT]).move_to([0, 0.3, 0])
        with self.say("Degrees of comparison. One syllable takes er and est: tall, taller, tallest; double a final consonant: big, bigger. Y becomes i: happy, happier. Two syllables or more take more and most: more beautiful. And the irregulars: good, better, best; bad, worse, worst; far, farther or further; old, older or elder.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = E.head(self, "Comparatives that take \"to\", and patterns to memorise")
        lat = VGroup(T("superior · inferior · senior · junior · prior · preferable  + to", size=28, color=th.AMBER), T("He is senior to me.  Health is preferable to wealth.  I prefer tea to coffee.", size=26, color=th.INK)).arrange(DOWN, buff=0.2).move_to([0, 1.6, 0])
        pats = E.bullets(["taller than any other boy (not \"any boy\" — that includes him)", "one of the busiest cities (superlative + plural)", "The more you practise, the better you become.", "twice as heavy as  ·  not so / as tall as"], width=11.2, size=26).move_to([0, -0.9, 0])
        with self.say("Some comparatives come from Latin and take to, not than: superior, inferior, senior, junior, prior and preferable. He is senior to me; health is preferable to wealth; and with the verb, I prefer tea to coffee. Patterns to memorise: taller than any other boy, because any boy would include himself; one of the busiest cities, with a plural noun; the more you practise, the better you become; and twice as heavy as."):
            self.play(FadeIn(h), FadeIn(lat))
            E.reveal_list(self, pats, 8.0)
        self.play(FadeOut(VGroup(lat, pats)))
        pairs = [("more better", "better"), ("larger than any country in Asia", "larger than any other country"), ("better than Kathmandu", "better than that of Kathmandu"), ("the taller of the three", "the tallest of the three"), ("the most unique design", "a unique design"), ("sufficient enough", "sufficient")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.7, 0.4), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And the traps. Never combine more with er: not more better. Than any country must be than any other country. Compare like with like: the climate of Pokhara is better than that of Kathmandu. Among three, use the superlative: the tallest of the three. Unique, perfect, round and empty are absolute, so no degrees: a unique design. And say it once: sufficient, not sufficient enough."):
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.35)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.1)
        self.play(FadeOut(VGroup(h, grid)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Adverbs: false friends")
        rows = [["", "means", "example"], ["hard / hardly", "with effort / almost not", "He works hard.  He hardly works."], ["late / lately", "not on time / recently", "She came late.  I haven't seen him lately."], ["high / highly", "up / very much", "The bird flew high.  She is highly respected."], ["near / nearly", "close / almost", "Come near.  It's nearly ten."]]
        tb = E.table(rows, [2.8, 4.0, 6.0], row_h=0.62, size=24, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 1.0, 0])
        nt = para("-ly adjectives are never adverbs: friendly, lovely, lonely, silly, likely — so say \"in a friendly way\". And fast, hard, early have no -ly: not \"fastly\".", width=11.4, size=24, color=th.MINT).move_to([0, -1.9, 0])
        with self.say("Most adverbs of manner add l y, but watch the false friends. Hard means with effort; hardly means almost not: he works hard is praise, he hardly works is not. Late and lately: lately means recently. High and highly: highly means very much. Near and nearly: nearly means almost. Adjectives ending in l y, friendly, lovely, lonely, likely, are never adverbs, so say: he spoke in a friendly way. And fast, hard and early have no l y form at all: never fastly."):
            self.play(FadeIn(h))
            E.reveal_table(self, tb, 6.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        a = E.card("linking verbs take adjectives", "be, seem, look, feel, taste, sound, smell, become: The soup tastes good. I feel bad.", th.SKY, w=5.8, h=2.6, size=24).move_to([-3.2, 0.5, 0])
        b = E.card("action verbs take adverbs", "She sings nicely. He speaks English well. (good = adjective, well = adverb)", th.AMBER, w=5.8, h=2.6, size=24).move_to([3.2, 0.5, 0])
        nt = T("✗ The food tastes well.   ✗ She sings very nice.   ✗ I am feeling very badly.", size=26, color=th.CORAL).move_to([0, -2.0, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("A linking verb, be, seem, look, feel, taste, sound, smell, become, is followed by an adjective: the soup tastes good; I feel bad. An action verb takes an adverb: she sings nicely; he speaks English well. Good is the adjective, well is the adverb. So the food tastes well, she sings very nice and I am feeling very badly are all wrong."):
            self.play(FadeIn(a), FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Never between the verb and its object")
        wr = E.wrong_right("She speaks fluently English.", "She speaks English fluently.", size=32).move_to([0, 1.6, 0])
        freq = E.bullets(["frequency adverbs go before the main verb: He always arrives early.", "after \"be\": He is always late.", "after the first auxiliary: She has never seen the sea.", "enough follows: old enough, clearly enough"], width=11.2, size=26).move_to([0, -0.9, 0])
        with self.say("Where an adverb stands. It never comes between a verb and its object: she speaks fluently English is wrong; she speaks English fluently. Frequency adverbs like always and never go before the main verb, after the verb be, and after the first auxiliary: he always arrives early; he is always late; she has never seen the sea. And enough comes after: old enough."):
            self.play(FadeIn(h), FadeIn(wr.wrong))
            self.play(Create(wr.cross), FadeIn(wr.right))
            E.reveal_list(self, freq, 8.0)
        self.play(FadeOut(VGroup(wr, freq)))
        h2 = E.head(self, "Move \"only\", and the meaning moves")
        o = VGroup(*[VGroup(T(a_, size=32, color=th.INK), T(b_, size=24, color=c_)).arrange(RIGHT, buff=0.5) for a_, b_, c_ in [("Only I solved two sums.", "nobody else did", th.SKY), ("I only solved two sums.", "I did nothing more with them", th.AMBER), ("I solved only two sums.", "no more than two", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.8, 0])
        neg = T("A negative adverb in front → inversion:", size=26, color=th.PINK, weight="BOLD").move_to([0, -1.4, 0])
        neg2 = para("Never have I seen such a crowd. Rarely does he miss a class. Little did they know. Under no circumstances should you open this door.", width=11.4, size=26, color=th.PINK).next_to(neg, DOWN, buff=0.2)
        with self.say("Only attaches to whatever follows it, and moving it moves the meaning. Only I solved two sums: nobody else did. I only solved two sums: I did nothing more with them. I solved only two sums: no more than two. And a negative adverb at the front causes inversion, the auxiliary jumping before the subject: never have I seen such a crowd; rarely does he miss a class; little did they know."):
            self.play(ReplacementTransform(h, h2))
            for o_ in o:
                self.play(FadeIn(o_, shift=UP * 0.15), run_time=0.5)
                self.hold(1.5)
            self.play(FadeIn(neg), FadeIn(neg2))
        self.play(FadeOut(VGroup(h2, o, neg, neg2)))
        self.quiz("Choose the correct order.",
                  ["a red small cotton bag", "a small red cotton bag", "a cotton small red bag", "a small cotton red bag"], 1,
                  "Pause and think.",
                  "Size, then colour, then material: a small red cotton bag.")
        self.quiz("\"The lecture was so ____ that the students were ____.\"",
                  ["bored / boring", "boring / bored", "boring / boring", "bored / bored"], 1,
                  "One more.",
                  "The lecture causes the feeling (-ing); the students feel it (-ed).")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Order: opinion, size, age, shape, colour, origin, material, purpose.",
            "-ing causes the feeling; -ed has it: boring lecture, bored students.",
            "Senior to, superior to, preferable to; than any other; no \"more better\".",
            "Linking verb + adjective (tastes good); hard ≠ hardly, late ≠ lately.",
            "No adverb between verb and object; negative adverb first → inversion.",
        ], "Quick recap. The order of adjectives. Bored and boring. Comparatives with to, and the comparison traps. Linking verbs and false friend adverbs. And where an adverb may stand.")
        self.outro("That was adjectives, adverbs and adjective order. Next: reported speech. See you there.")
