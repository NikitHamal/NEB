import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

CROCUS = "#B784E0"


def scene_card(title, text, color, w=5.8, h=2.6):
    return E.card(title, text, color, w=w, h=h, tsize=28, size=24)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 12
    TITLE = "Soft Storm"
    SUBTITLE = "Abhi Subedi · a poem"
    SECTIONS = ["Abhi Subedi and his Kathmandu", "How the softness began", "Four scenes from a violent decade", "Crocuses over stone", "Themes", "Form and devices"]
    NEXT = "Unit 13 · On Libraries"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a = T("storm", size=60, color=th.CORAL, weight="BOLD").move_to([1.4, 0.6, 0])
        b = T("soft", size=60, color=th.SKY, weight="BOLD").next_to(a, LEFT, buff=0.35)
        nt = para("A storm that is soft is not a storm at all — and that contradiction is the whole poem.", width=10, size=28, color=th.INK).move_to([0, -1.4, 0])
        with self.say("A storm is violent. Soft is gentle. Put them together, soft storm, and you get a contradiction, an oxymoron. That contradiction, in the title and repeated through the poem, is the whole argument."):
            self.play(FadeIn(a, scale=1.3))
            self.play(FadeIn(b, shift=RIGHT * 0.3))
            self.play(FadeIn(nt))
        nt2 = para("Hungry children, a lost child with a radio, a man beaten for no reason, a blood-stained shirt. The poet does not grow angry. He grows soft.", width=10, size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Abhi Subedi watches Kathmandu in a violent decade: hungry children, a lost child with a radio, a man beaten for no reason, a blood stained shirt. He does not become angry. He becomes soft. What does that mean?"):
            self.play(FadeIn(nt2))
            nb = E.neby_in(self, "sad", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b, nt, nt2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 12: Soft Storm, by the Nepali poet Abhi Subedi."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Abhi Subedi and his Kathmandu. How the softness began. Four scenes from a violent decade. Crocuses over stone. The themes. And the form and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Abhi Subedi (born 1945)")
        facts = E.bullets(["born in Sabla, Terhathum: a hill boy writing about the capital", "taught English at Tribhuvan University for about forty years", "poet, playwright, critic, translator, columnist", "writes in both Nepali and English — two instruments, one mind", "plays: Dreams of Peach Blossoms, Fire in the Monastery"], width=8.0, size=24).move_to([-2.0, 0.2, 0])
        nt = para("Date: the poem's \"violent history\" and \"war memories\" point to Nepal's conflict years (1996–2006). Don't assert a publication you can't verify.", width=4.0, size=22, color=th.AMBER).move_to([4.7, 0.2, 0])
        with self.say("Abhi Subedi was born in nineteen forty five in Terhathum, in the eastern hills, and taught English at Tribhuvan University for about forty years; many of Nepal's English teachers were his students. He is a poet, playwright, critic and translator, and he writes in both Nepali and English. The textbook gives no date for this poem, but its violent history and war memories point clearly to Nepal's conflict years. Say that, rather than naming a book you cannot verify."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, facts, nt)))
        h = E.head(self, "Two place names, a few hundred metres apart")
        a = scene_card("Thamel", "the tourist quarter: trekking shops, bars, neon — the richest, brightest street in Nepal", th.AMBER).move_to([-3.2, 0.6, 0])
        b = scene_card("Kesharmahal", "a Rana palace: the Kaiser Library and the Garden of Dreams; old trees where fruit bats really roost", th.MINT).move_to([3.2, 0.6, 0])
        nt = para("\"homeless children in Thamel / cried with hunger under the bat-bearing / trees of Kesharmahal\" — hunger beside a palace of books and a pleasure garden. He doesn't point it out; he lets you do the arithmetic.", width=11.4, size=24, color=th.INK).move_to([0, -2.1, 0])
        with self.say("Only two place names appear, a few hundred metres apart. Thamel is the tourist quarter, Kathmandu's brightest and richest street. Kesharmahal is a Rana palace with the Kaiser Library and the Garden of Dreams, and old trees where fruit bats really roost. So homeless children cry with hunger under the bat bearing trees of a palace full of books and a garden built for pleasure. Subedi does not point it out. He puts the two things in one sentence and lets you do the arithmetic."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "\"I became soft / I became soft\"")
        pts = VGroup(*[VGroup(T(a_, size=28, color=c_, weight="BOLD"), para(b_, width=11, size=24, color=th.BODY)).arrange(DOWN, buff=0.1) for a_, b_, c_ in [
            ("\"crashed on the eerie stillness\"", "after the tumult, not peace but a frightening quiet; he crashes on it like a boat on rock", th.SKY),
            ("\"I inherited the soft\"", "softness handed down by the times, not chosen", CROCUS),
            ("\"the sky grew like crocuses / over stones\"", "small spring flowers pushing through stone: life insisting in a hard place", CROCUS),
            ("\"softness rose like a gale / tearing my roofs\"", "the paradox: softness behaves like a storm", th.CORAL)]]).arrange(DOWN, buff=0.3).move_to([0, -0.3, 0])
        with self.say("Stanza one begins by saying it twice: I became soft, I became soft, as if discovering it while speaking. Why? After the tumult he crashed on the eerie stillness, the frightening quiet after something terrible. He inherited the soft, handed down by the times, when the sky grew like crocuses over stones: crocuses are small spring flowers that push up through stony ground, and they will come back. Then the governing paradox: softness rose like a gale, tearing my roofs. Softness behaves like a storm. And the night speaks only the public language of posters and politics, rituals and reasons."):
            self.play(FadeIn(h))
            for p_ in pts:
                self.play(FadeIn(p_, shift=UP * 0.15), run_time=0.6)
                self.hold(2.8)
        self.play(FadeOut(VGroup(h, pts)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Four scenes from a violent decade")
        cards = VGroup(
            scene_card("1 · the hungry children", "in Thamel, under the trees of Kesharmahal; no names, no faces — only hunger and a place", th.AMBER, w=6.1, h=2.75),
            scene_card("2 · the child with a radio", "a forlorn child, a transistor round his neck, running and wailing for his mother \"in the corridors of violent history\"", th.SKY, w=6.1, h=2.75),
            scene_card("3 · the beating", "a man beaten before his family \"by nobody for no reason / in no sensible times\"", th.CORAL, w=6.1, h=2.75),
            scene_card("4 · the shirt", "a blood-stained shirt in a far corner, whispering \"in the earth's ears\" with \"bruised human lips\"", th.PINK, w=6.1, h=2.75),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.45, 0])
        with self.say("Then four scenes. The hungry children in Thamel. A forlorn child with a transistor radio round his neck, running and wailing to find his mother in the corridors of violent history. A man beaten before his family by nobody, for no reason, in no sensible times. And a blood stained shirt."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        a = scene_card("the radio", "his only possession, maybe his livelihood — broadcasting the news of the very violence that lost him his mother. He carries history's noise while running through it.", th.SKY, w=5.9, h=3.4).move_to([-3.1, 0.2, 0])
        b = scene_card("\"by nobody\"", "four negatives in five lines: no reason, nobody, no reason, no sensible times. In a collapsed time, violence has no authors. It just happens.", th.CORAL, w=5.9, h=3.4).move_to([3.1, 0.2, 0])
        with self.say("Look closer at two. The radio is the child's only possession, maybe his living, and it is broadcasting the news of the violence that has lost him his mother: he carries the noise of history while running through it. And the beating: count the negatives. No reason, nobody, no reason again, no sensible times. Four in five lines. The repetition is the sound of a mind that cannot find an explanation. By nobody: in a collapsed time, violence stops having authors. It just happens."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(h, a, b)))
        h = E.head(self, "The shirt, and the reproach")
        a = scene_card("the shirt", "no body is mentioned — as the dead of a conflict are often met: a garment, a sandal, a photograph. It can only whisper to the earth: no one human is listening.", th.PINK, w=5.9, h=3.4).move_to([-3.1, 0.2, 0])
        b = scene_card("\"its Leela\"", "Leela: divine play. \"You\" gave words but didn't listen, gave storms but didn't stay. You = a person, the country's leaders, or God?", th.AMBER, w=5.9, h=3.4).move_to([3.1, 0.2, 0])
        with self.say("The shirt has no body; the person who wore it is never mentioned, which is how the dead of a conflict are often met, as a garment or a photograph. It can only whisper to the earth, because no human authority is listening. Then the poem's only complaint: you gave words but did not listen to them, gave storms but did not wait to see their Leela, the divine play, over the silent stone. Who is you? A person, the country's leaders, or God. The poem does not say, and probably means all three."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(h, a, b)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "\"Crocuses have grown / over the stone\"")
        stone = Polygon([-6, -2.4, 0], [-3.5, -1.2, 0], [-1.0, -1.6, 0], [1.5, -1.0, 0], [4.0, -1.5, 0], [6, -2.4, 0], stroke_color=th.MUTED, stroke_width=3, fill_color="#3A3A46", fill_opacity=0.9)
        crocs = VGroup(*[VGroup(Line(ORIGIN, UP * 0.5, color=th.MINT, stroke_width=3), Ellipse(width=0.22, height=0.38, stroke_width=0, fill_color=CROCUS, fill_opacity=1).shift(UP * 0.6)).move_to([x, y, 0], aligned_edge=DOWN) for x, y in [(-4.2, -1.45), (-2.6, -1.4), (-0.4, -1.5), (1.4, -1.1), (3.3, -1.35)]])
        silent = VGroup(*[T(t_, size=26, color=th.INK) for t_ in ["silent pages", "silent stones", "silent shirts", "silent dilapidations of gods' abodes"]]).arrange(DOWN, buff=0.18).move_to([0, 1.3, 0])
        with self.say("Stanza seven turns from witnessing to reflecting, and opens with the poem's one plainly hopeful image: crocuses have grown over the stone, I saw last moonlit night. The flowers really have come up through the rock, placed right after the worst stanzas. Then storms loiter in the narrow lanes, hanging about with no purpose, like the violence did. And the crescendo: the storm rages over silent pages, silent stones, silent shirts, and the silent ruins of the gods' temples. An enormous grief, and total silence."):
            self.play(FadeIn(h), FadeIn(stone))
            self.play(LaggedStart(*[GrowFromEdge(c_, DOWN) for c_ in crocs], lag_ratio=0.25), run_time=2)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in silent], lag_ratio=0.5), run_time=3)
        self.play(FadeOut(VGroup(h, stone, crocs, silent)))
        h = E.head(self, "\"The mad time spools\"")
        wrong = E.bullets(["\"stone growing in flower\" — the right things, reversed", "history rushing \"over deforested land\"", "birds singing of \"bizarre journeys / over the warming earth\"", "\"rhododendron blooming in winter\" — Nepal's spring flower, out of season"], width=11.2, size=26).move_to([0, 0.2, 0])
        nt = para("Environmental collapse set beside political violence as one disorder: \"All in unison have created / this soft gale.\" Then it ends small: \"My soft storm / dances in ripples / of your uneasy lake.\"", width=11.4, size=24, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Stanza eight: the mad time spools, winding up everything onto its reel, and everything is slightly wrong. Stone growing in flower. Deforested land. Birds on bizarre journeys over the warming earth. And rhododendron, laligurans, Nepal's national flower, blooming in winter instead of spring: a symptom, not a pretty picture. Subedi puts environmental collapse beside political violence as one disorder. All in unison created this soft gale. And the ending shrinks the public storm to something private: my soft storm dances in ripples of your uneasy lake."):
            self.play(FadeIn(h))
            E.reveal_list(self, wrong, 10.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, wrong, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Softness as a response", "not anger, not despair: a decent person in indecent times sees clearly and writes it down", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Violence without meaning", "\"by nobody for no reason\": cruelty with no author and no cause", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Silence and witness", "silent pages, stones, shirts: only the poem speaks", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Nature in disorder — and hope", "warming earth, winter rhododendron; yet crocuses over stone", CROCUS, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Softness as a response: when the times are cruel and nothing can be done, a decent person sees clearly and writes it down. Violence without meaning, by nobody for no reason. Silence and witness: everything the storm passes over is silent; only the poem speaks. And nature in disorder, the warming earth and winter rhododendron, beside a stubborn hope: crocuses over stone."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Free verse, nine stanzas — held together by a refrain")
        refr = VGroup(*[T("I became soft", size=26, color=th.SKY).set_opacity(1 - 0.08 * k) for k in range(8)]).arrange(DOWN, buff=0.12).move_to([-3.6, -0.3, 0])
        notes = E.bullets(["106 lines, no rhyme, no metre", "anaphora: \"I became soft\" opens stanza after stanza — eight times", "the oxymoron \"soft storm\", \"soft gale\"", "one slipped rhyme: storm \"rages / over silent pages\"", "two addresses to \"you\"; ends in a private lake"], width=6.4, size=24).move_to([3.0, -0.3, 0])
        with self.say("The form is free verse: nine stanzas, a hundred and six lines, no rhyme, no metre. What holds it together is anaphora: the phrase I became soft opens stanza after stanza, eight times. The oxymoron, soft storm, soft gale, is the poem's key figure: a contradiction that names a feeling both gentle and devastating. And notice the one rhyme that slips in, rages over silent pages, landing exactly on the idea of writing."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(r_) for r_ in refr], lag_ratio=0.15))
            E.reveal_list(self, notes, 7.0)
        self.play(FadeOut(VGroup(h, refr, notes)))
        rows = [["oxymoron", "\"soft storm\", \"soft gale\"", "gentle and devastating at once"], ["anaphora", "\"I became soft\"", "binds a free-verse poem"], ["symbol", "crocuses over stone", "life in a hard place"],
                ["personification", "the shirt whispers to the earth", "the dead speak; no one listens"], ["repetition", "\"for no reason … for no reason\"", "a mind circling the senseless"], ["allusion", "Leela, divine play", "a reproach to \"you\""]]
        E.device_slide(self, rows, "Devices to quote. Oxymoron: soft storm. Anaphora: I became soft. The crocuses as a symbol of life in a hard place. Personification: the shirt whispering to the earth. Repetition: for no reason, for no reason. And the allusion to Leela, divine play.", widths=(2.9, 5.0, 4.5), size=22)
        self.quiz("\"Soft storm\" is an example of",
                  ["simile", "oxymoron", "onomatopoeia", "alliteration"], 1,
                  "Pause and think.",
                  "Two contradictory words joined: an oxymoron — a feeling both gentle and devastating.")
        self.quiz("Why is \"rhododendron blooming in winter\" disturbing?",
                  ["it is too cold", "Nepal's spring flower out of season: a sign of disorder", "rhododendrons are rare", "it is a dream"], 1,
                  "One more.",
                  "With the warming earth and deforested land, it joins environmental disorder to the political one.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Abhi Subedi (b. 1945); Nepal's conflict years; Thamel and Kesharmahal.",
            "\"I became soft\": inherited, like crocuses over stones; softness like a gale.",
            "Four scenes: hungry children, a child with a radio, a man beaten \"by nobody\", a shirt.",
            "Crocuses over stone; silent pages; winter rhododendron; the mad time spools.",
            "Oxymoron and anaphora in free verse; ends in ripples of \"your uneasy lake\".",
        ], "Quick recap. Subedi's Kathmandu in a violent decade. A softness inherited from the times. Four scenes of suffering. Crocuses over stone and a world out of season. And an oxymoron at the heart of it all: a soft storm.")
        self.outro("That completes the poems. Next we move to essays, starting with On Libraries. See you there.")
