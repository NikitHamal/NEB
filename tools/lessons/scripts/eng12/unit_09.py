import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

SUNC = "#F5C451"
DUSK = "#8E6BD6"


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 9
    TITLE = "Every Morning I Wake"
    SUBTITLE = "Dylan Thomas · a poem from Under Milk Wood"
    SECTIONS = ["Dylan Thomas and Under Milk Wood", "Morning and evening", "\"Not wholly bad or good\"", "Good-bye — but just for now", "Themes", "Form and devices"]
    NEXT = "Unit 10 · I Was My Own Route"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        door = VGroup(Rectangle(width=1.6, height=2.6, stroke_color=th.AMBER, stroke_width=4, fill_color=th.PANEL, fill_opacity=1), Dot(radius=0.06, color=th.AMBER).shift(RIGHT * 0.5)).move_to([-4.0, -0.6, 0])
        man = VGroup(Circle(radius=0.25, stroke_color=th.INK, stroke_width=3), Line(DOWN * 0.25, DOWN * 1.2, color=th.INK, stroke_width=3)).move_to([-2.6, -0.8, 0])
        sun = Circle(radius=0.6, stroke_width=0, fill_color=SUNC, fill_opacity=0.9).move_to([4.0, 1.4, 0])
        hor = Line([-6.4, -1.9, 0], [6.4, -1.9, 0], color=th.MUTED, stroke_width=3)
        q = para("No money, no rain, no punishment for enemies. Just: look kindly on us, and give us one more day.", width=7.0, size=28, color=th.INK).move_to([1.8, -0.2, 0])
        with self.say("An old village minister steps out of his front door at sunset and says a short prayer aloud. He does not ask for money, or rain, or for his enemies to be punished. He asks God to look kindly on every creature that is born to die, and to give his town one more day. Then he says good night to the sun: good-bye, but just for now."):
            self.play(FadeIn(hor), FadeIn(door), FadeIn(man), FadeIn(sun))
            self.play(FadeIn(q))
            self.play(sun.animate.move_to([4.0, -1.9, 0]).set_color(DUSK), run_time=3)
            nb = E.neby_in(self, "listen", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(door, man, sun, hor, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 9: Every Morning I Wake, by Dylan Thomas. It is the gentlest poem in your course, and its gentleness is an argument."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Dylan Thomas and Under Milk Wood. Morning and evening. Not wholly bad or good. Good-bye, but just for now. The themes. And the form and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Dylan Thomas (1914–1953)")
        facts = E.bullets(["born in Swansea, south Wales", "18 Poems at twenty: famous almost at once", "a poet of sound: alliteration, rhyme, a deep reading voice", "a late Romantic: imagination, feeling, spontaneity", "joined the BBC in 1945; died in New York, aged 39"], width=7.6, size=24).move_to([-2.4, 0.2, 0])
        side = VGroup(T("also wrote", size=26, color=th.AMBER, weight="BOLD"), para("\"Do not go gentle into that good night\"", width=4.0, size=24, color=th.BODY), para("\"Fern Hill\"", width=4.0, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.5, 0.4, 0])
        with self.say("Dylan Thomas was born in Swansea, in south Wales, in nineteen fourteen, and published his first book of poems at twenty. He was a poet of sound before sense, building lines out of alliteration and rhyme, and reading them in a famous deep voice. He is often called a late Romantic. He worked for the BBC from nineteen forty five, and died in New York in nineteen fifty three, aged thirty nine."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))
        h = E.head(self, "Under Milk Wood: \"a play for voices\"")
        hill = Arc(radius=5.0, start_angle=PI * 0.3, angle=PI * 0.4, color="#3F7A55", stroke_width=6).move_to([0, 0.8, 0])
        wood = VGroup(*[Triangle(stroke_width=0, fill_color="#2E6A45", fill_opacity=1).scale(0.25).move_to(hill.point_from_proportion(t) + UP * 0.25) for t in np.linspace(0.1, 0.9, 12)])
        town = VGroup(*[Square(0.35, stroke_color=th.AMBER, stroke_width=2).move_to([-3.0 + 0.55 * k, -0.6 - 0.15 * (k % 2), 0]) for k in range(12)])
        labs = VGroup(T("Milk Wood", size=24, color=th.MINT).next_to(wood, UP, buff=0.1), T("Llareggub", size=26, color=th.AMBER, weight="BOLD").next_to(town, RIGHT, buff=0.3))
        facts = E.bullets(["a radio play (BBC, 1954): one spring day in a Welsh seaside town", "some sixty voices, dreams and kitchens; no plot", "Llareggub — read it backwards: a joke, he won't sentimentalise", "the Rev. Eli Jenkins recites this at his door, at sunset"], width=11.4, size=24).move_to([0, -2.3, 0])
        with self.say("The poem comes from Under Milk Wood, a radio play first broadcast in nineteen fifty four. It follows one spring day in an invented Welsh seaside town called Llareggub, a name which, read backwards, is a rude joke: Thomas loves the place but will not sentimentalise it. The speaker is the Reverend Eli Jenkins, a gentle, poetry writing minister, who recites these verses at his door as the sun goes down. The title is just the first line."):
            self.play(FadeIn(h), Create(hill), FadeIn(wood), FadeIn(town), FadeIn(labs))
            E.reveal_list(self, facts, 8.0)
        self.play(FadeOut(VGroup(h, hill, wood, town, labs, facts)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Stanza 1: a little prayer, every morning")
        q = E.quote("Every morning when I wake, / Dear Lord, a little prayer I make", "stanza 1", width=9.0, size=30).move_to([0, 1.4, 0])
        pts = E.bullets(["\"little\": modest — a daily habit, not an emergency", "\"Dear Lord\": how you begin a letter to someone you know", "he asks God only to look, lovingly, on \"all poor creatures born to die\"", "\"poor\" = pitiable; \"creatures\" = everything created, animals too"], width=11.2, size=26).move_to([0, -1.3, 0])
        with self.say("Stanza one. Every morning when I wake, dear Lord, a little prayer I make. Notice little: modest in length and ambition, said daily, not in a crisis. And Dear Lord, the way you start a letter to someone you know. The request is startlingly small: that God keep his loving eye on all poor creatures born to die. Not to do anything; just to look, with love. Poor means pitiable, and creatures means everything created, animals included. The only qualification is that we are mortal."):
            self.play(FadeIn(h), FadeIn(q))
            E.reveal_list(self, pts, 12.0)
        self.play(FadeOut(VGroup(h, q, pts)))
        h = E.head(self, "Stanza 2: a blessing on the town, every evening")
        sun = Circle(radius=0.45, stroke_width=0, fill_color=SUNC, fill_opacity=1).move_to([-3.2, 1.2, 0])
        moon = Circle(radius=0.45, stroke_width=0, fill_color=DUSK, fill_opacity=1).move_to([3.2, 1.2, 0])
        a = T("every morning → all creatures", size=26, color=SUNC).next_to(sun, DOWN, buff=0.3)
        b = T("every evening → one town", size=26, color=DUSK).next_to(moon, DOWN, buff=0.3)
        tg = para("Whether they last the night is always \"touch-and-go\": uncertain, could go either way. A minister promising no protection — only honesty.", width=11, size=26, color=th.CORAL).move_to([0, -2.0, 0])
        with self.say("Stanza two mirrors the first. Every morning becomes every evening, and the prayer for all creatures becomes a blessing on one small town. The poem has the shape of a day, and of the whole play. Then the frankest line: whether they last the night is always touch and go. It means highly uncertain. It is an astonishingly plain thing for a clergyman to say. He promises no protection; faith does not remove the risk."):
            self.play(FadeIn(h), FadeIn(sun), FadeIn(a))
            self.play(FadeIn(moon), FadeIn(b))
            self.play(FadeIn(tg))
        self.play(FadeOut(VGroup(h, sun, moon, a, b, tg)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        q = E.quote("We are not wholly bad or good, / Who live our lives under Milk Wood", "stanza 3", width=9.5, size=32).move_to([0, 1.6, 0])
        bar = Rectangle(width=8.0, height=0.5, stroke_width=0).set_fill(color=[th.MINT, th.CORAL], opacity=0.8).move_to([0, -0.4, 0])
        ends = VGroup(T("wholly bad", size=24, color=th.CORAL).next_to(bar, LEFT, buff=0.2), T("wholly good", size=24, color=th.MINT).next_to(bar, RIGHT, buff=0.2))
        dot = Triangle(color=th.INK, fill_opacity=1).scale(0.15).rotate(PI).next_to(bar, UP, buff=0.05)
        nt = para("Litotes — saying \"not wholly bad\" admits the badness first, and is warmer for it. The whole play stands behind this line.", width=11, size=26, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("Stanza three holds the poem's most famous line. We are not wholly bad or good, who live our lives under Milk Wood. The town in the play has a man who dreams of poisoning his wife, a woman who scrubs her house all day, a blind old sea captain in love with the drowned. None is a saint, none a villain. Thomas puts all of humanity in the middle. The figure is litotes, understatement by denying the opposite: saying not wholly bad admits the badness first, and is warmer for it."):
            self.play(FadeIn(q))
            self.play(FadeIn(bar), FadeIn(ends), FadeIn(dot))
            self.play(dot.animate.shift(LEFT * 1.6), run_time=0.8)
            self.play(dot.animate.shift(RIGHT * 2.4), run_time=0.9)
            self.play(dot.animate.shift(LEFT * 0.8), run_time=0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(q, bar, ends, dot, nt)))
        h = E.head(self, "\"Thou, I know, wilt be the first …\"")
        pts = VGroup(
            E.card("\"I know\"", "not \"I hope\": the one moment of total confidence — in God's generosity, not his own goodness", th.MINT, w=3.9, h=3.0, size=24),
            E.card("\"the first\"", "others see our worst first; God will be first to look for our best", th.AMBER, w=3.9, h=3.0, size=24),
            E.card("\"Thou … wilt\"", "the old intimate form from the chapel prayer book: affectionate, not grand", th.SKY, w=3.9, h=3.0, size=24),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.0, 0])
        with self.say("Then he tells God what God will do: You, I know, will be the first to see our best side, not our worst. Three points. I know, not I hope: the only moment of complete confidence, and it is confidence in God's generosity, not in his own goodness. The first: neighbours and gossips see the worst first; God will be first to look for the best. And Thou and wilt, the old intimate form of the chapel prayer book, affectionate rather than grand."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in pts], lag_ratio=0.6), run_time=4)
        self.play(FadeOut(VGroup(h, pts)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Stanza 4: one more day")
        hor = Line([-6.4, -1.2, 0], [6.4, -1.2, 0], color=th.MUTED, stroke_width=3)
        sun = Circle(radius=0.6, stroke_width=0, fill_color=SUNC, fill_opacity=1).move_to([0, 0.4, 0])
        q1 = T("\"O let us see another day!\"", size=32, color=th.AMBER, weight="BOLD").move_to([0, 2.2, 0])
        q2 = T("good-bye — but just for now!", size=34, color=SUNC, weight="BOLD").move_to([0, -2.2, 0])
        with self.say("The last stanza is the only one that asks for something concrete, and what it asks for is simply more time: O let us see another day! The exclamation mark is the loudest sound in the poem. Then the whole town, in his imagination, bows to the setting sun and says good-bye, but just for now."):
            self.play(FadeIn(h), Create(hor), FadeIn(sun), FadeIn(q1))
            self.play(sun.animate.move_to([0, -1.2, 0]), run_time=2.5)
            self.play(FadeIn(q2))
        nt = para("On the surface: the sun returns tomorrow. Underneath: the answer to \"born to die\" — perhaps dying, too, is only a short parting. The poem never says so.", width=11, size=26, color=th.MINT).move_to([0, 0.5, 0])
        with self.say("That phrase does two jobs. On the surface it is simple fact: the sun will be back in the morning. Underneath, it answers the first stanza's all poor creatures born to die. If good night to the sun is only a short parting, perhaps death is too. The poem never says so; it lets a cheerful, throwaway phrase carry a hope it is too modest to state."):
            self.play(FadeIn(nt), sun.animate.set_opacity(0.3))
        self.play(FadeOut(VGroup(h, hor, sun, q1, q2, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Prayer as habit", "every morning, every evening: said on ordinary days, so it can be trusted", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Human imperfection", "\"not wholly bad or good\": neither sentimental nor puritanical", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Mortality without terror", "death is in every stanza, yet the poem ends on an exclamation mark", DUSK, w=6.1, h=2.75, size=24),
            E.card("A merciful God, humbly imagined", "a loving eye, \"Dear Lord\", \"Thou\": no hell, no list of sins", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("The central idea: a minister's daily prayer asks not for protection or wealth but for mercy, that God look lovingly on mortal creatures, see that ordinary people are mixed rather than wicked, and grant them one more day. Themes: prayer as a habit of ordinary days. Human imperfection, neither sentimental nor puritanical. Mortality without terror. And a merciful God, imagined humbly."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        h = E.head(self, "The circle narrows, then opens")
        rings = VGroup(*[Circle(radius=r, stroke_color=c_, stroke_width=4).move_to([-3.2, -0.3, 0]) for r, c_ in [(2.4, th.SKY), (1.6, th.AMBER), (0.9, th.CORAL)]])
        rl = VGroup(*[T(t_, size=22, color=c_).move_to([-3.2, -0.3 + r - 0.3, 0]) for t_, c_, r in [("all creatures", th.SKY, 2.4), ("one town", th.AMBER, 1.6), ("one night", th.CORAL, 0.9)]])
        steps = E.bullets(["1 morning: a prayer for all creatures", "2 evening: a blessing on the town; \"touch-and-go\"", "3 a plea for fair judgement", "4 one more day — and the sun, for now"], width=5.6, size=24).move_to([3.3, -0.3, 0])
        with self.say("The structure is a narrowing circle: from all creation, to one town, to one night. Then the last line opens it out again to the sun. The whole poem is one turn of the earth."):
            self.play(FadeIn(h), LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.3), FadeIn(rl))
            E.reveal_list(self, steps, 5.0)
        self.play(FadeOut(VGroup(h, rings, rl, steps)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Rhyming couplets: aabb ccdd eeff gghh")
        pairs = [("wake", "make"), ("eye", "die"), ("sun-down", "town"), ("no", "touch-and-go"), ("good", "Wood"), ("first", "worst"), ("day", "pray"), ("bow", "now")]
        chips = VGroup(*[VGroup(E.chip(a_, th.SKY, size=24), E.chip(b_, th.SKY, size=24)).arrange(RIGHT, buff=0.15) for a_, b_ in pairs]).arrange_in_grid(rows=4, cols=2, buff=(1.2, 0.35)).move_to([0, 0.5, 0])
        nt = para("Eight perfect rhymes; nothing left hanging. In a poem about uncertainty and death, the sound keeps promising what the sense cannot. Metre: mostly iambic tetrameter, the beat of hymns and ballads.", width=11.4, size=24, color=th.INK).move_to([0, -2.4, 0])
        with self.say("The form. Sixteen lines in four quatrains, each built from two rhyming couplets: a a b b, c c d d, and so on. All eight rhymes are perfect, and a couplet is the most settled rhyme in English: the ear gets what it is waiting for at once. So in a poem about uncertainty and death, the sound keeps promising what the sense cannot. The metre is mostly iambic tetrameter, the beat of hymns and ballads.") as v:
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, scale=0.8) for c_ in chips], lag_ratio=0.2), run_time=3)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, chips, nt)))
        rows = [["apostrophe", "\"Dear Lord\", \"O please\", \"Thou\"", "spoken to God"], ["litotes", "\"not wholly bad or good\"", "warm understatement"], ["idiom", "\"touch-and-go\"", "plain honesty about risk"],
                ["parallelism", "every morning … every evening", "the shape of a day"], ["symbol", "the setting sun", "death, and return"], ["exclamation", "\"another day!\" \"just for now!\"", "cheer facing death"]]
        E.device_slide(self, rows, "Devices to quote. Apostrophe: the poem is spoken to God. Litotes: not wholly bad or good. The idiom touch and go. Parallelism: every morning, every evening. The setting sun as a symbol of death and return. And exclamations of cheer at the very edge of death.", widths=(2.8, 5.4, 4.2), size=22)
        self.quiz("Who speaks the poem in Under Milk Wood?",
                  ["First Voice", "the Reverend Eli Jenkins", "Captain Cat", "Dylan Thomas himself"], 1,
                  "Pause and think.",
                  "Eli Jenkins, the village minister, recites it at his door at sunset.")
        self.quiz("What is the rhyme scheme?",
                  ["abab", "abcb", "aabb ccdd …", "abba"], 2,
                  "One more.",
                  "Rhyming couplets, every rhyme perfect: settled sound for an unsettled subject.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Dylan Thomas (1914–1953); from the radio play Under Milk Wood (1954).",
            "Eli Jenkins's prayer: a loving eye on \"all poor creatures born to die\".",
            "Evening: a blessing on the town; survival is \"touch-and-go\".",
            "\"We are not wholly bad or good\"; God will see our best side first.",
            "\"Good-bye — but just for now!\"; couplets aabb, iambic tetrameter.",
        ], "Quick recap. Thomas and Under Milk Wood. A little prayer for all creatures born to die. A town whose every night is touch and go. People not wholly bad or good. And a cheerful good-bye to the sun, just for now.")
        self.outro("That was Every Morning I Wake. Next: I Was My Own Route, by Julia de Burgos. See you there.")
