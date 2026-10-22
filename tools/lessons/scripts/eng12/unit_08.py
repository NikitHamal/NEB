import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

AMETHYST = "#9B6BD6"
SUNC = "#F5C451"

STANZAS = [["I'll tell you how the sun rose, —", "A ribbon at a time.", "The steeples swam in amethyst,", "The news like squirrels ran."],
           ["The hills untied their bonnets,", "The bobolinks begun.", "Then I said softly to myself,", "\"That must have been the sun!\""],
           ["But how he set, I know not.", "There seemed a purple stile", "Which little yellow boys and girls", "Were climbing all the while"],
           ["Till when they reached the other side,", "A dominie in gray", "Put gently up the evening bars,", "And led the flock away."]]


def stanza(k, size=30, color=th.INK):
    return VGroup(*[T(l_, size=size, color=color) for l_ in STANZAS[k]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)


def sky(color_top, color_bottom, w=6.0, h=4.2):
    bands = VGroup(*[Rectangle(width=w, height=h / 8, stroke_width=0, fill_color=interpolate_color(ManimColor(color_top), ManimColor(color_bottom), k / 7), fill_opacity=1) for k in range(8)]).arrange(DOWN, buff=0)
    return bands


def steeple(x, h=1.4, color="#2B2140"):
    base = Rectangle(width=0.35, height=h * 0.55, stroke_width=0, fill_color=color, fill_opacity=1)
    spire = Triangle(stroke_width=0, fill_color=color, fill_opacity=1).stretch_to_fit_width(0.35).stretch_to_fit_height(h * 0.45).next_to(base, UP, buff=0)
    return VGroup(base, spire).move_to([x, 0, 0], aligned_edge=DOWN)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 8
    TITLE = "A Day"
    SUBTITLE = "Emily Dickinson · a poem"
    SECTIONS = ["Emily Dickinson", "The sunrise, told", "The sunset, not known", "Themes", "Form, metre and rhyme", "Devices"]
    NEXT = "Unit 9 · Every Morning I Wake"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a = T("I'll tell you how the sun rose …", size=36, color=SUNC, weight="BOLD").move_to([0, 1.2, 0])
        b = T("But how he set, I know not.", size=36, color=AMETHYST, weight="BOLD").move_to([0, -0.6, 0])
        with self.say("A child runs in with news: I'll tell you how the sun rose! And out it comes, in a rush of pictures."):
            self.play(FadeIn(a, shift=UP * 0.2))
        with self.say("Then, halfway through, the voice drops. But how he set, I know not. Sixteen short lines, and one of the quietest, strangest poems in your course. What happened at sunset that the speaker cannot describe?"):
            self.play(FadeIn(b, shift=UP * 0.2))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 8: A Day, by Emily Dickinson."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Emily Dickinson. The sunrise, told. The sunset, not known. The themes. Form, metre and rhyme. And the devices you should quote.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Emily Dickinson (1830–1886)")
        facts = E.bullets(["lived almost her whole life in one house in Amherst, Massachusetts", "in later life rarely went out; wore white", "wrote about 1,800 poems; published perhaps ten", "sewed the rest into little booklets; her sister found them", "first selection printed in 1890, four years after her death"], width=7.8, size=24).move_to([-2.2, 0.2, 0])
        side = VGroup(T("influences", size=26, color=th.AMBER, weight="BOLD"), *[para(t_, width=3.9, size=24, color=th.BODY) for t_ in ["the Metaphysical poets", "the Book of Revelation", "Puritan New England religion", "the hymn book"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.7, 0.2, 0])
        with self.say("Emily Dickinson lived almost her entire life in one house in Amherst, Massachusetts. In later years she rarely went out, wore white, and spoke to some visitors from behind a door. She wrote about eighteen hundred poems and published perhaps ten. The rest she sewed into little booklets, which her sister found after her death. The first selection was printed in eighteen ninety."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
        with self.say("Her mind was shaped by the Metaphysical poets, who yoked huge ideas to homely objects; by the Bible's Book of Revelation; by the Puritan religion of New England; and by the hymns she sang every Sunday. You will find all four in this poem."):
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, facts, side)))
        h = E.head(self, "Three facts about the text")
        cards = VGroup(
            E.card("Not her title", "Dickinson left it untitled. \"A Day\" was added by her editors in 1890.", th.CORAL, w=3.9, h=2.8),
            E.card("Written c. 1860", "printed 1890; public domain — so we can read it whole", th.SKY, w=3.9, h=2.8),
            E.card("The dash", "the mark after line 1 is her famous dash: a held breath, not a stop", th.AMBER, w=3.9, h=2.8),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.1, 0])
        with self.say("Three examinable facts. The title, A Day, is not hers: her editors added it in eighteen ninety. The poem was written around eighteen sixty. And the mark at the end of the first line is her famous dash, a held breath rather than a stop."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
        self.play(FadeOut(VGroup(h, cards)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        sk = sky("#2A1F4F", "#F2A65A").move_to([3.3, 0.2, 0])
        ground = Rectangle(width=6.0, height=0.5, stroke_width=0, fill_color="#1E2A20", fill_opacity=1).next_to(sk, DOWN, buff=0)
        st = VGroup(*[steeple(x) for x in (2.0, 3.3, 4.5)]).align_to(ground, UP).shift(UP * 0.0)
        for s_, x in zip(st, (2.0, 3.3, 4.5)):
            s_.next_to(ground, UP, buff=0).set_x(x)
        ribbons = VGroup(*[Line([0.4, -1.0 + 0.45 * k, 0], [6.2, -1.0 + 0.45 * k, 0], color=c_, stroke_width=10) for k, c_ in enumerate([SUNC, "#F2994A", "#E56B6F", AMETHYST])])
        s1 = stanza(0).move_to([-3.3, 0.3, 0])
        with self.say("Stanza one. I'll tell you how the sun rose: the voice of a child who has seen something and cannot keep it. A ribbon at a time: dawn is not sudden, it is unrolled in narrow bands, like ribbon off a bolt in a draper's shop."):
            self.play(FadeIn(s1[0]), FadeIn(sk), FadeIn(ground))
            self.play(FadeIn(s1[1]), LaggedStart(*[Create(r_) for r_ in ribbons], lag_ratio=0.4), run_time=2.5)
        with self.say("The steeples swam in amethyst. Church spires are the tallest things in town, so they catch the light first. Amethyst is a violet jewel, and in the Book of Revelation it is one of the stones in the wall of heaven, so for a moment the town is built into heaven. And swam turns the air into water. Then the only simile in the poem: the news like squirrels ran. The light runs down into the streets in bursts, like a squirrel."):
            self.play(FadeIn(s1[2]), FadeIn(st), *[s_.animate.set_color(AMETHYST) for s_ in st])
            self.play(st.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.2)
            self.play(FadeIn(s1[3]))
            sq = Dot([2.0, -1.4, 0], radius=0.1, color=SUNC)
            self.play(MoveAlongPath(sq, VMobject().set_points_smoothly([[1.0, -1.4, 0], [2.0, -0.9, 0], [3.0, -1.5, 0], [4.2, -0.9, 0], [5.6, -1.4, 0]])), run_time=1.6)
            self.play(FadeOut(sq))
        self.play(FadeOut(VGroup(sk, ground, st, ribbons, s1)))
        s2 = stanza(1).move_to([-3.1, 0.3, 0])
        hills = VGroup(*[Arc(radius=1.4 + 0.3 * k, start_angle=0, angle=PI, color="#3F7A55", stroke_width=4, fill_color="#2A4A36", fill_opacity=0.8).move_to([2.2 + 2.0 * k, -1.0, 0]) for k in range(2)])
        mist = VGroup(*[Ellipse(width=1.8, height=0.5, stroke_width=0, fill_color=WHITE, fill_opacity=0.45).move_to(h_.get_top() + DOWN * 0.1) for h_ in hills])
        bird = VGroup(*[ArcBetweenPoints(LEFT * 0.25, ORIGIN, angle=-PI / 2, color=th.INK), ArcBetweenPoints(ORIGIN, RIGHT * 0.25, angle=-PI / 2, color=th.INK)]).move_to([3.0, 1.6, 0])
        with self.say("Stanza two. The hills untied their bonnets: before dawn the hilltops are wrapped in mist, and as the light comes the mist loosens and lifts, like women untying their bonnets when they come indoors. The bobolinks begun: bobolinks are songbirds, and begun instead of began is a child's grammar, kept on purpose. Begun what? Singing; the speaker is too excited to say."):
            self.play(FadeIn(s2[0]), FadeIn(hills), FadeIn(mist))
            self.play(LaggedStart(*[m_.animate.shift(UP * 0.8).set_opacity(0) for m_ in mist], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(s2[1]), FadeIn(bird))
            self.play(bird.animate.shift(RIGHT * 1.5 + UP * 0.3), run_time=1.2)
        with self.say("Then the voice drops. Then I said softly to myself: That must have been the sun! She has watched the whole performance, and only worked out afterwards, by deduction, what caused it. It is charming, and it is the first sign that this speaker understands less than she describes."):
            self.play(FadeIn(s2[2]))
            self.play(FadeIn(s2[3]), Circumscribe(s2[3], color=SUNC))
        self.play(FadeOut(VGroup(s2, hills, mist, bird)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        s3 = stanza(2).move_to([-3.2, 0.3, 0])
        sk = sky("#3B1F5E", "#1A1430").move_to([3.3, 0.3, 0])
        fence = VGroup(Line([0.4, -0.8, 0], [6.2, -0.8, 0], color=th.MUTED, stroke_width=4), Line([0.4, -0.4, 0], [6.2, -0.4, 0], color=th.MUTED, stroke_width=4))
        stile = VGroup(*[Line([2.9 + 0.25 * k, -1.2 + 0.25 * k, 0], [3.5 + 0.25 * k, -1.2 + 0.25 * k, 0], color=AMETHYST, stroke_width=5) for k in range(4)])
        kids = VGroup(*[Dot([1.4 + 0.35 * k, -1.2, 0], radius=0.09, color=SUNC) for k in range(6)])
        with self.say("Stanza three is the turn. But how he set, I know not. Eight lines of confident telling, and now, I know not. Notice the sun has become he: a person, with a will, gone somewhere she cannot follow. And everything is hedged: there seemed a purple stile. A stile is a set of steps built over a field wall, so people can cross where animals cannot. The horizon at evening becomes a boundary, with a way over it."):
            self.play(FadeIn(sk), FadeIn(s3[0]))
            self.play(FadeIn(s3[1]), Create(fence), FadeIn(stile))
        with self.say("Which little yellow boys and girls were climbing all the while: the last golden rays, or small gold lit clouds, seen as children going home over the wall, one at a time."):
            self.play(FadeIn(s3[2]), FadeIn(s3[3]), FadeIn(kids))
            for k_ in kids:
                self.play(MoveAlongPath(k_, VMobject().set_points_smoothly([k_.get_center(), [3.2, -0.6, 0], [4.0, -0.2, 0], [5.0, -1.2, 0]])), run_time=0.45)
        self.play(FadeOut(s3))
        s4 = stanza(3).move_to([-3.2, 0.3, 0])
        dom = VGroup(Circle(radius=0.22, stroke_color=th.MUTED, stroke_width=3, fill_color=th.MUTED, fill_opacity=0.6), Polygon([-0.35, -0.25, 0], [0.35, -0.25, 0], [0.45, -1.3, 0], [-0.45, -1.3, 0], stroke_width=0, fill_color=th.MUTED, fill_opacity=0.8)).arrange(DOWN, buff=0.02).move_to([5.6, -0.2, 0])
        bars = VGroup(*[Line([4.6, -1.3 + 0.3 * k, 0], [4.6, -1.3 + 0.3 * k, 0] + RIGHT * 0.01, color=th.INK, stroke_width=5) for k in range(3)])
        with self.say("Stanza four. Till when they reached the other side, a dominie in gray: a dominie is a schoolmaster, and in America also a minister. In grey: the colour of dusk, and of a Puritan minister's coat. He has no face. He put gently up the evening bars: the bars are the poles that close a gap in a farm fence once the animals are in for the night. It is done gently; the poem insists on that. And led the flock away. The children have become sheep, the schoolmaster a shepherd: the oldest Christian image for God gathering the dead."):
            self.play(FadeIn(s4[0]), FadeIn(dom))
            self.play(FadeIn(s4[1]))
            self.play(FadeIn(s4[2]), LaggedStart(*[l_.animate.put_start_and_end_on(l_.get_start(), l_.get_start() + RIGHT * 1.6) for l_ in bars], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(s4[3]), FadeOut(kids), dom.animate.shift(RIGHT * 1.2).set_opacity(0.2), run_time=2)
        self.play(FadeOut(VGroup(s4, sk, fence, stile, dom, bars)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "A day is a life")
        tl = E.timeline(["sunrise: birth, childhood — easy to tell", "noon", "sunset: death — can only be imagined"], x0=-6.0, x1=6.0, y=0.6, colors=[SUNC, th.MUTED, AMETHYST], size=26, wrap=3.6, up_down=False)
        nt = para("The word \"death\" never appears. Instead: a boundary, a crossing, the other side, a figure in grey, a gate shut gently, a flock led home.", width=11.4, size=26, color=th.INK).move_to([0, -1.8, 0])
        with self.say("The central idea. Behind the day lies a life. Morning, birth and childhood, can be told perfectly. Evening, death, can only be imagined. The word death never appears. Instead we get a boundary, a crossing, the other side, a figure in grey, a gate shut gently, and a flock led home."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.5))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tl, nt)))
        cards = VGroup(
            E.card("Innocence to experience", "a child with a story becomes someone who has watched what she cannot narrate — the turn at \"I know not\"", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Nature as theatre", "she shows what the sun does — steeples, squirrels, hills, birds — never the sun itself", SUNC, w=6.1, h=2.75, size=24),
            E.card("Death, handled gently", "one of the few Dickinson death poems that is not frightened: the bars go up \"gently\"", AMETHYST, w=6.1, h=2.75, size=24),
            E.card("Faith and doubt", "church and shepherd are all there — but \"there seemed\": a comforting picture, an honest verb", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Four themes. Innocence to experience: the confident child of the first half becomes someone who has seen what she cannot explain, and it happens exactly at I know not. Nature as theatre: she never looks at the sun itself, only at what it does. Death, handled gently: Dickinson wrote dozens of poems about dying, and this is one of the few that is not afraid. And faith and doubt: the church and the shepherd are all there, but only as what seemed. A comforting picture, and an honest verb."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Four quatrains, rhyme abcb")
        s = stanza(1, size=30).move_to([-2.0, 0.4, 0])
        tags = VGroup(*[T(t_, size=28, color=c_, weight="BOLD").next_to(s[k], RIGHT, buff=0.5).set_x(2.6) for k, (t_, c_) in enumerate([("a", th.MUTED), ("b", SUNC), ("c", th.MUTED), ("b", SUNC)])])
        nt = para("Only lines 2 and 4 rhyme. Stanza 1's time / ran is a slant rhyme — breathless, slightly out of control.", width=11, size=26, color=th.INK).move_to([0, -2.3, 0])
        with self.say("The form. Four quatrains, sixteen lines. In each stanza only the second and fourth lines rhyme: a b c b. Begun, sun. Stile, while. Gray, away. Only the first stanza's time and ran is a slant rhyme, a near miss, which suits that breathless, excited opening."):
            self.play(FadeIn(h), FadeIn(s))
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.3))
            self.play(Indicate(VGroup(s[1], s[3]), color=SUNC))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, s, tags, nt)))
        h = E.head(self, "Hymn metre: 8 · 6 · 8 · 6")
        rows = [["stanza", "line 1", "line 2", "line 3", "line 4"], ["1", "7", "6", "8", "6"], ["2", "7", "6", "8", "6"], ["3", "7", "6", "8", "6"], ["4", "8", "6", "8", "6"]]
        tb = E.table(rows, [2.2, 1.8, 1.8, 1.8, 1.8], row_h=0.6, size=26, colors=[th.AMBER, th.CORAL, th.INK, th.INK, th.INK]).move_to([0, 0.6, 0])
        nt = para("Common metre, as in \"Amazing Grace\": iambic tetrameter and trimeter. Lines 1 of stanzas 1–3 are \"headless\" — they start on a stress. Only the last stanza settles into perfect hymn metre, just as the poem turns religious.", width=11.4, size=24, color=th.INK).move_to([0, -2.2, 0])
        with self.say("The metre is the common metre of the hymn book, the metre of Amazing Grace: lines of eight and six syllables, iambic tetrameter and trimeter. Dickinson sang it every Sunday. But count: in the first three stanzas the opening line is one syllable short. It is headless, starting on a stress, a little push forward. Only the last stanza fills out to perfect hymn metre, exactly as the poem becomes religious. That is not an accident.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.4)
            self.play(Circumscribe(VGroup(*[tb[i][2] for i in range(1, 5)]), color=th.CORAL))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["metaphor", "\"A ribbon at a time\"", "dawn unrolled slowly"], ["simile", "\"The news like squirrels ran\"", "darting, restless light"], ["personification", "\"The hills untied their bonnets\"", "mist lifting; the world at ease"],
                ["antithesis", "rose / \"how he set, I know not\"", "the poem's whole structure"], ["allegory", "yellow children → the flock", "sunset as the end of a life"], ["allusion", "\"led the flock away\"", "the Good Shepherd, unnamed"], ["enjambment", "\"all the while / Till when …\"", "the sentence crosses the stanza like a stile"]]
        E.device_slide(self, rows, "Devices to quote. Metaphor: a ribbon at a time. The poem's only simile: the news like squirrels ran. Personification: the hills untied their bonnets. Antithesis between how the sun rose and how he set. The allegory of the yellow children who become a flock. A biblical allusion to the Good Shepherd, never named. And enjambment: the sentence steps over the stanza break, just as the children step over the stile.", widths=(2.8, 5.4, 4.2), size=22, y=0.2)
        self.quiz("Who is the \"dominie in gray\"?",
                  ["a farmer", "a schoolmaster or minister — perhaps God or Death", "the sun", "the speaker's father"], 1,
                  "Pause and think.",
                  "Dominie means schoolmaster or minister; as the shepherd who leads the flock away, he suggests God or Death.")
        self.quiz("What is the rhyme scheme of each stanza?",
                  ["aabb", "abab", "abcb", "abba"], 2,
                  "One more.",
                  "abcb: only lines 2 and 4 rhyme, and stanza 1's time / ran is a slant rhyme.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Emily Dickinson (1830–1886); c. 1860; title \"A Day\" added by editors.",
            "Sunrise told: ribbon, amethyst steeples, squirrels, hills untying bonnets.",
            "Sunset not known: a purple stile, yellow children, a dominie in gray, a flock.",
            "A day as a life; innocence to experience; death handled gently; faith and doubt.",
            "Four quatrains, abcb, hymn metre; headless first lines; antithesis and allegory.",
        ], "Quick recap. Dickinson, and a poem from about eighteen sixty. The sunrise told in four pictures. The sunset only imagined: a stile, children, a grey shepherd. A day as a life, and death handled gently. And the hymn metre underneath.")
        self.outro("That was A Day. Next poem: Every Morning I Wake, by Dylan Thomas. See you there.")
