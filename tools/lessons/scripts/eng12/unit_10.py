import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def walker(color=th.PINK, s=1.0):
    return VGroup(Circle(radius=0.2, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.6), Line(DOWN * 0.2, DOWN * 0.8, color=color, stroke_width=3),
                  Line(DOWN * 0.8, DOWN * 1.2 + LEFT * 0.2, color=color, stroke_width=3), Line(DOWN * 0.8, DOWN * 1.2 + RIGHT * 0.25, color=color, stroke_width=3)).scale(s)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 10
    TITLE = "I Was My Own Route"
    SUBTITLE = "Julia de Burgos · a poem in translation"
    SECTIONS = ["Julia de Burgos", "A poem in translation", "The walk, stanza by stanza", "The empty chair", "Themes", "Form and devices"]
    NEXT = "Unit 11 · The Awakening Age"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        road = Line([-6.4, -1.6, 0], [6.4, -1.6, 0], color=th.MUTED, stroke_width=4)
        w = walker().move_to([-5.0, -0.9, 0])
        stage = VGroup(Rectangle(width=2.6, height=0.3, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.6), *[Line(UP * 0, UP * 1.0, color=th.AMBER, stroke_width=3).shift(RIGHT * x) for x in (-1.1, 1.1)]).move_to([3.0, 0.4, 0])
        chair = VGroup(Line([0, 0, 0], [0, 0.6, 0], color=th.INK, stroke_width=4), Line([0, 0, 0], [0.5, 0, 0], color=th.INK, stroke_width=4), Line([0.5, 0, 0], [0.5, -0.5, 0], color=th.INK, stroke_width=4), Line([0, 0, 0], [0, -0.5, 0], color=th.INK, stroke_width=4)).move_to([3.0, 1.0, 0])
        lab = T("a ceremony in her honour …", size=26, color=th.AMBER).move_to([3.0, 2.3, 0])
        with self.say("A woman admits that she once tried to be what men wanted her to be. Then she starts walking. At the end of the poem, the old order prepares a grand ceremony to honour her, and she simply does not turn up."):
            self.play(Create(road), FadeIn(w), FadeIn(stage), FadeIn(chair), FadeIn(lab))
            self.play(w.animate.move_to([6.0, -0.9, 0]), run_time=3)
        q = T("… and the homage was left waiting for her.", size=28, color=th.CORAL).move_to([0, -2.5, 0])
        with self.say("Nothing is smashed. Nobody shouts. The rebellion is a walk and an empty chair, and that is what makes it frightening to the people it is aimed at."):
            self.play(FadeIn(q), Indicate(chair, color=th.CORAL))
            nb = E.neby_in(self, "cool", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(road, w, stage, chair, lab, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 10: I Was My Own Route, by the Puerto Rican poet Julia de Burgos."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Julia de Burgos. Reading a poem in translation. The walk, stanza by stanza. The empty chair. The themes. And the form and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Julia de Burgos (1914–1953)")
        facts = E.bullets(["born in Carolina, Puerto Rico: eldest of thirteen, a very poor family", "a teacher at twenty-one", "a nationalist: independence for the island, dignity for the poor, freedom for women — one cause", "this poem: from Poem in Twenty Furrows (1938)", "later New York and Cuba; died in poverty in Spanish Harlem, 1953"], width=8.2, size=24).move_to([-2.0, 0.2, 0])
        side = VGroup(T("legacy", size=26, color=th.AMBER, weight="BOLD"), para("a precursor of today's Latina and Latino writers; now a national figure in Puerto Rico", width=3.6, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.3, 0])
        with self.say("Julia de Burgos was born in nineteen fourteen in Puerto Rico, the eldest of thirteen children in a very poor family; six of her brothers and sisters died of malnutrition. She became a teacher at twenty one, and a nationalist: for her, independence for the island, dignity for the poor and freedom for women were one cause. This poem comes from her first book, from nineteen thirty eight. She later lived in New York and Cuba, and died in poverty in Spanish Harlem in nineteen fifty three. Today she is a national figure, and a forerunner of Latina writers."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 12.0)
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "\"Yo misma fui mi ruta\" — translated by Jack Agüeros")
        ok = E.card("safe to discuss", "images, structure, argument: the old guard, the branch, the whiplash, the soils, the parade are de Burgos's own", th.MINT, w=5.8, h=3.0, size=24).move_to([-3.2, 0.5, 0])
        care = E.card("be careful with", "sound and rhythm: any alliteration in English is the translator's. Spanish also marks the speaker as female in every adjective.", th.CORAL, w=5.8, h=3.0, size=24).move_to([3.2, 0.5, 0])
        tip = para("Exam sentence: \"Since the poem is a translation from Spanish, its sound effects are the translator's; its images and structure are de Burgos's own.\"", width=11.4, size=24, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("One thing most notes leave out. De Burgos wrote in Spanish; you read Jack Agüeros's English translation. Images, structure and argument survive translation, so discuss them with confidence. But sound and rhythm belong to the translator, so never say the poet uses alliteration without adding, in the English version. And something is lost: Spanish adjectives mark the speaker as a woman in every line; English cannot. The free verse shape, though, is hers. One sentence in the exam is enough."):
            self.play(FadeIn(h), FadeIn(ok))
            self.play(FadeIn(care))
            self.play(FadeIn(tip))
        self.play(FadeOut(VGroup(h, ok, care, tip)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Stanza 1: the confession")
        phrases = VGroup(*[VGroup(T(a_, size=30, color=c_, weight="BOLD"), para(b_, width=11, size=24, color=th.BODY)).arrange(DOWN, buff=0.12) for a_, b_, c_ in [
            ("\"an attempt at life\"", "not a life — a rough draft, a rehearsal of one", th.CORAL),
            ("\"a game of hide and seek with my being\"", "she hides from herself, as lightly as children play", th.AMBER),
            ("\"But I was made of nows\"", "a coined plural: built of present moments, nothing owed to the past", th.MINT),
            ("feet \"forward, forward\"", "they refuse to walk backwards, \"mocking the ashes\", towards \"the kiss / of new paths\"", th.SKY)]]).arrange(DOWN, buff=0.35).move_to([0, -0.3, 0])
        with self.say("Stanza one opens with a confession. She wanted to be what men wanted her to be, and that was only an attempt at life: a rough draft, not a life. A game of hide and seek with her own being, in which she both hides and seeks. Then, only four lines in, but: I was made of nows. A coined plural: she is built of present moments, owing nothing to the past. Her feet refuse to walk backwards and go forward, forward, mocking the ashes of what is burnt out, towards the kiss of new paths."):
            self.play(FadeIn(h))
            for p_ in phrases:
                self.play(FadeIn(p_, shift=UP * 0.15), run_time=0.6)
                self.hold(2.5)
        self.play(FadeOut(VGroup(h, phrases)))
        h = E.head(self, "Stanzas 2 and 3: the cost, and the release")
        w = walker(s=1.2).move_to([-1.0, -0.6, 0])
        birds = VGroup(*[VGroup(ArcBetweenPoints(LEFT * 0.35, ORIGIN, angle=-PI / 2, color=th.MUTED, stroke_width=4), ArcBetweenPoints(ORIGIN, RIGHT * 0.35, angle=-PI / 2, color=th.MUTED, stroke_width=4)).move_to([-3.2 + 0.6 * k, 0.6 - 0.4 * (k % 2), 0]) for k in range(4)])
        notes = VGroup(E.card("the old guard", "the conservative defenders of the old order — given \"desperate\" flapping wings. They tear her back: she has turned away and won't turn round. Desperate: they are afraid.", th.MUTED, w=5.6, h=2.7, size=22),
                       E.card("the unpinned branch", "pinned flat to a wall, now free \"forever\". Each whiplash drives her gaze further from \"distant familiar horizons\": punishment produces vision.", th.MINT, w=5.6, h=2.7, size=22)).arrange(DOWN, buff=0.2)
        notes.scale_to_fit_height(min(notes.height, 5.3)).move_to([3.4, -0.45, 0])
        with self.say("Stanza two, three short lines, is the cost. At every step the old guard, the defenders of the old order, beat their desperate wings and tear her back. Her back, because she has turned away and will not turn round. And desperate: they are not calm and powerful; they are frightened. Stanza three is release: she was unpinned forever, like a branch freed from a wall. And the paradox: every whiplash only drives her gaze further from the distant, familiar horizons she was taught to aim at. Punishment produces vision."):
            self.play(FadeIn(h), FadeIn(w), FadeIn(notes[0]))
            self.play(LaggedStart(*[b_.animate.shift(RIGHT * 1.2 + DOWN * 0.3) for b_ in birds], lag_ratio=0.1), FadeIn(birds), run_time=2)
            self.play(FadeIn(notes[1]))
        self.play(FadeOut(VGroup(h, w, birds, notes)))
        h = E.head(self, "Stanzas 4 and 5: belonging everywhere, whole")
        soils = VGroup(*[T(t_, size=28, color=c_) for t_, c_ in [("soil without history", th.SKY), ("soil without a future", th.AMBER), ("soil always soil, without edges", th.MINT)]]).arrange(DOWN, buff=0.35).move_to([0, 0.8, 0])
        one = T("All in me — as was life in me …", size=34, color=th.PINK, weight="BOLD").move_to([0, -1.6, 0])
        nt = para("No ancestors to obey, no destiny mapped, no borders. Then a single-line stanza: the climax, standing alone, needing nothing.", width=11, size=24, color=th.BODY).move_to([0, -2.7, 0])
        with self.say("Stanza four: having left her inherited ground, she claims all ground. She is a blossom of all the soils of the earth: soil without history, so no ancestors to obey; without a future, so no destiny mapped out; soil without edges, so no borders. Then stanza five is a single line, standing alone: the climax. All in me, as life was in me. The hide and seek is over; the self and life are the same size. And the trailing dots refuse to close."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(s_) for s_ in soils], lag_ratio=0.4))
            self.play(FadeIn(one, scale=1.1))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, soils, one, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Stanza 6: the same beginning, a different end")
        a = E.card("stanza 1", "\"I wanted to be like men wanted me to be …\" → her feet walk forward", th.SKY, w=5.6, h=2.4, size=24).move_to([-3.2, 1.0, 0])
        b = E.card("stanza 6", "the same four lines, word for word → a regal parade, heralds announce her … and the wish to follow men \"warped\"", th.PINK, w=5.6, h=2.4, size=24).move_to([3.2, 1.0, 0])
        arr = Arrow(a.get_right(), b.get_left(), buff=0.1, color=th.MUTED)
        nt = para("The repetition is a test: play the opening again and see what has changed. Everything after it has.", width=11, size=26, color=th.AMBER).move_to([0, -1.1, 0])
        q = T("\"and the homage was left waiting for me …\"", size=30, color=th.CORAL, weight="BOLD").move_to([0, -2.5, 0])
        with self.say("The last stanza repeats the first four lines word for word. It is not laziness; it is a test. Play the opening again, and see what has changed. Now the old guard hold a regal parade, and heralds announce her name: the establishment is opening its ranks to honour her. And at that very moment, the wish to follow men warped in her, twisted out of shape like damp wood. The final image is an absence: the homage was left waiting for me. No speech, no slammed door. She is simply elsewhere."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(GrowArrow(arr), FadeIn(b))
            self.play(FadeIn(nt))
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(h, a, b, arr, nt, q)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Identity found within", "not given by anyone's approval: she becomes herself by walking her own route", th.PINK, w=6.1, h=2.75, size=24),
            E.card("Women and patriarchy", "\"like men wanted me to be\": a life shaped by others is only \"an attempt at life\"", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("The present over the past", "\"made of nows\", \"mocking the ashes\": tradition has no claim on her", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Quiet rebellion", "no violence: walking forward and declining an invitation. The old guard's fear is the measure of her power.", th.AMBER, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Identity is found within, not handed out by anyone's approval. Women and patriarchy: a life shaped to what men want is only an attempt at life. The present over the past: made of nows, mocking the ashes. And quiet rebellion: no violence, just walking forward and declining an invitation, and the old guard's desperate fear measures her power. Remember too her politics: soil without edges, from a woman whose island was ruled by another country."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Free verse in six stanzas: 9 · 3 · 10 · 6 · 1 · 8")
        lens = [9, 3, 10, 6, 1, 8]
        bars = VGroup(*[Rectangle(width=0.8, height=0.32 * n, stroke_width=0, fill_color=th.PINK if n == 1 else th.SKY, fill_opacity=0.8) for n in lens]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([-3.2, -0.3, 0])
        bl = VGroup(*[T(str(n), size=24, color=th.INK).next_to(b_, UP, buff=0.1) for n, b_ in zip(lens, bars)])
        notes = E.bullets(["no rhyme, no metre — in either language", "line lengths mirror meaning: the bruise is short", "the climax is one line alone", "circular: stanza 6 repeats stanza 1, ends differently"], width=5.6, size=24).move_to([3.4, -0.2, 0])
        with self.say("The form is free verse, with no rhyme and no metre in either language, so the shape on the page is de Burgos's own. Six stanzas of nine, three, ten, six, one and eight lines. The short stanza two is the bruise; the single line of stanza five is the climax, standing alone. And the structure is circular: the last stanza repeats the first, and ends differently."):
            self.play(FadeIn(h), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.2), FadeIn(bl))
            E.reveal_list(self, notes, 5.0)
        self.play(FadeOut(VGroup(h, bars, bl, notes)))
        rows = [["metaphor", "\"an attempt at life\"", "a draft, not a life"], ["metaphor", "\"made of nows\"", "built of present moments"], ["symbol", "the old guard's wings", "frightened tradition"],
                ["paradox", "each whiplash → clearer sight", "punishment frees her"], ["repetition", "\"forward, forward\"", "the beat of footsteps"], ["ellipsis", "\"left waiting for me …\"", "an unwritten future"]]
        E.device_slide(self, rows, "Devices to quote. Metaphor: an attempt at life, and made of nows. The old guard and their desperate wings as a symbol of frightened tradition. Paradox: each whiplash makes her see more clearly. Repetition: forward, forward, the beat of footsteps. And the long closing ellipsis: the homage still waiting, the future unwritten.", widths=(2.8, 5.0, 4.6), size=22)
        self.quiz("What happens when the old guard prepare a parade in her honour?",
                  ["she accepts proudly", "she stays away", "she attacks them", "she joins the old guard"], 1,
                  "Pause and think.",
                  "Her wish to follow men \"warped\"; the homage was left waiting for her.")
        self.quiz("Why must you be careful discussing this poem's alliteration?",
                  ["it has none", "it is a translation from Spanish", "it rhymes", "it is a sonnet"], 1,
                  "One more.",
                  "The English sound effects are the translator's; images and structure are de Burgos's.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Julia de Burgos (1914–1953), Puerto Rico; Poem in Twenty Furrows (1938).",
            "Translated from Spanish: images are hers, sound is the translator's.",
            "\"an attempt at life\", \"made of nows\", the old guard's desperate wings.",
            "Unpinned branch, soils without edges, \"All in me\"; stanza 6 repeats stanza 1.",
            "Free verse 9·3·10·6·1·8; the homage left waiting; identity found within.",
        ], "Quick recap. De Burgos, and a poem read in translation. An attempt at life, a woman made of nows, an old guard with desperate wings. An unpinned branch and soils without edges. And a circular ending where the homage is left waiting.")
        self.outro("That was I Was My Own Route. Next poem: The Awakening Age. See you there.")
