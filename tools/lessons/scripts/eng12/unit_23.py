import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def bin_box(title, color, w=5.4, h=2.5):
    b = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.06)
    t = T(title, size=28, color=color, weight="BOLD").next_to(b, UP, buff=0.15)
    return VGroup(b, t)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 23
    TITLE = "Determiners and Quantifiers"
    SUBTITLE = "Grammar · a, an, the, some, much, many, few, little, each, every"
    SECTIONS = ["Two questions first", "A or an: decided by sound", "The, and no article at all", "Which determiner with which noun", "Uncountable nouns", "Common errors and worked items"]
    NEXT = "Unit 24 · Subject-Verb Agreement"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        s = E.sentence("Nepal is beautiful country.", size=42).move_to([0, 1.0, 0])
        gap = T("a", size=42, color=th.MINT, weight="BOLD")
        with self.say("Nepal is beautiful country. Can you hear what is missing? Nepali has no articles at all, no a, an or the, so these little words are the marks most often lost in the grammar question and in your writing."):
            self.play(FadeIn(s))
            self.play(Indicate(VGroup(s.words[1], s.words[2]), color=th.CORAL))
        s2 = E.sentence("Nepal is a beautiful country.", size=42, color=th.INK).move_to([0, 1.0, 0])
        nt = para("A determiner opens a noun phrase and tells you which, or how many: a pen, the pen, this pen, my pen, every pen, few pens, much ink.", width=11, size=28, color=th.AMBER).move_to([0, -1.4, 0])
        with self.say("Nepal is a beautiful country. Words like a, the, this, my, every, few and much are determiners: they open a noun phrase and tell you which, or how many. And choosing them is a matter of matching the determiner to the kind of noun that follows."):
            self.play(TransformMatchingShapes(s, s2))
            self.play(s2.words[2].animate.set_color(th.MINT))
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(s2, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 23: determiners and quantifiers."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Two questions to ask first. A or an, decided by sound. The, and no article at all. Which determiner goes with which noun. Uncountable nouns. And the common errors, with worked items.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Is the noun countable? Singular or plural?")
        cb = bin_box("countable: how many?", th.SKY).move_to([-3.2, -0.15, 0])
        ub = bin_box("uncountable: how much?", th.AMBER).move_to([3.2, -0.15, 0])
        words = [("books", 0), ("bread", 1), ("information", 1), ("chair", 0), ("advice", 1), ("students", 0), ("furniture", 1), ("village", 0), ("news", 1)]
        chips = VGroup(*[E.chip(w_, th.MUTED, size=26) for w_, _ in words]).arrange(RIGHT, buff=0.2).move_to([0, 2.1, 0])
        chips.scale_to_fit_width(min(chips.width, 12.6))
        with self.say("Before choosing any determiner, ask two questions. First: is the noun countable or uncountable? Books, chairs, students and villages can be counted. Bread, information, advice, furniture and news cannot, even though their Nepali equivalents often can."):
            self.play(FadeIn(h), FadeIn(cb), FadeIn(ub), LaggedStart(*[FadeIn(c_) for c_ in chips], lag_ratio=0.1))
            placed = [0, 0]
            for (w_, k), c_ in zip(words, chips):
                tgt = (cb if k == 0 else ub)[0].get_corner(UL) + np.array([1.3 + 2.6 * (placed[k] % 2), -0.5 - 0.7 * (placed[k] // 2), 0])
                placed[k] += 1
                col = th.SKY if k == 0 else th.AMBER
                c_.generate_target()
                c_.target.move_to(tgt)
                c_.target[0].set_fill(col)
                self.play(MoveToTarget(c_), run_time=0.45)
        nt = para("Second: singular or plural? \"Much\" only with uncountables, \"many\" only with plural countables, \"a / an\" only with singular countables. Get these two right and half the item is answered.", width=11.4, size=24, color=th.INK).move_to([0, -2.85, 0])
        with self.say("Second: singular or plural? Much goes only with uncountables, many only with plural countables, and a or an only with a singular countable. Get these two questions right, and half the item is already answered."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, cb, ub, chips, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "A or an? Listen to the first sound, not the letter")
        a_col = VGroup(T("a  — consonant sound", size=28, color=th.SKY, weight="BOLD"), *[T(t_, size=26, color=th.INK) for t_ in ["a university, a uniform   /ju:/", "a European country   /ju:/", "a one-rupee coin   /w/", "a horse, a hotel   (h is sounded)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.2, 0.0, 0])
        an_col = VGroup(T("an  — vowel sound", size=28, color=th.MINT, weight="BOLD"), *[T(t_, size=26, color=th.INK) for t_ in ["an umbrella, an uncle", "an hour, an honest man   (silent h)", "an MA, an MP   (em, em)", "an X-ray, an NGO   (eks, en)"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.0, 0])
        mid = DashedLine([0.1, 2.0, 0], [0.1, -2.0, 0], color=th.FAINT)
        nt = T("He is an university student.  ✗   →   He is a university student.  ✓", size=26, color=th.CORAL).move_to([0, -2.7, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("A or an is decided by sound, not spelling. A before a consonant sound: a university and a uniform begin with a you sound; a European country; a one rupee coin begins with a w sound; and a horse, where the h is sounded. An before a vowel sound: an umbrella; an hour and an honest man, where the h is silent; an M A and an M P, because the letter M is read em; an X ray and an N G O. So he is an university student is wrong: a university student."):
            self.play(FadeIn(h), Create(mid), FadeIn(a_col[0]), FadeIn(an_col[0]))
            for a_, b_ in zip(a_col[1:], an_col[1:]):
                self.play(FadeIn(a_), FadeIn(b_), run_time=0.5)
                self.hold(2.2)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a_col, an_col, mid, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "\"The\": the listener knows exactly which one")
        uses = [("mentioned before", "a shawl … the shawl"), ("unique things", "the sun, the moon, the earth"), ("superlatives, ordinals", "the best answer, the first bench"),
                ("rivers, ranges, seas", "the Koshi, the Himalayas"), ("plural countries, groups", "the Netherlands, the UN"), ("papers, holy books", "the Kathmandu Post, the Gita"),
                ("instruments", "play the madal"), ("adjective as a noun", "the poor, the Nepalese"), ("only, same, whole", "the only son")]
        cards = VGroup(*[E.card(a_, b_, th.PALETTE[k % 8], w=4.0, h=1.6, tsize=26, size=24) for k, (a_, b_) in enumerate(uses)]).arrange_in_grid(rows=3, cols=3, buff=(0.2, 0.2)).move_to([0, -0.25, 0])
        with self.say("The is used when the listener can tell exactly which one you mean. Something mentioned before: I bought a shawl; the shawl was pashmina. Unique things: the sun, the moon. Superlatives and ordinals: the best answer, the first bench. Rivers, mountain ranges and seas: the Koshi, the Himalayas. Plural country names and organisations: the Netherlands, the U N. Newspapers, holy books and historical periods. Musical instruments: play the madal. An adjective used as a noun: the poor. And with only, same and whole."):
            self.play(FadeIn(h))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.45)
                self.hold(1.4)
        self.play(FadeOut(cards))
        h2 = E.head(self, "No article at all")
        zero = E.bullets(["general plurals and uncountables: Books are cheap in Bhotahity. Honesty pays.", "names of people, cities, single mountains, lakes, countries: Sita, Birgunj, Everest, Phewa Lake, Nepal", "languages, subjects, games, meals, festivals: He teaches Nepali. We had lunch. during Tihar", "institutions used for their purpose: go to school, in hospital, go to bed", "transport after \"by\": by bus, by air — but on foot"], width=11.4, size=25).move_to([0, 0.1, 0])
        nt = T("✗ The Everest is in Nepal.   ✓ Everest is in Nepal.   ·   ✗ goes to the school by bus (to study)", size=24, color=th.CORAL).move_to([0, -2.7, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("And no article at all. With plurals and uncountables used in general: books are cheap in Bhotahity; honesty pays. With names of people, cities, single mountains, lakes and countries: Everest, not the Everest. With languages, subjects, games, meals and festivals. With institutions used for their purpose: she goes to school, meaning to study; but she goes to the school to meet the principal, meaning the building. And with transport after by: by bus, by air."):
            self.play(ReplacementTransform(h, h2))
            E.reveal_list(self, zero, 12.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h2, zero, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Which determiner with which noun?")
        rows = [["", "a book", "books", "information"], ["a / an", "✓", "✗", "✗"], ["much", "✗", "✗", "✓ much time"], ["many", "✗", "✓ many books", "✗"], ["(a) few, several", "✗", "✓", "✗"], ["(a) little", "✗", "✗", "✓ a little milk"],
                ["each, every", "✓ each boy", "✗", "✗"], ["both", "✗", "✓ both hands", "✗"], ["some, any, a lot of, enough", "✗", "✓", "✓"]]
        tb = E.table(rows, [4.4, 2.6, 2.8, 3.2], row_h=0.56, size=24, colors=[th.AMBER, th.SKY, th.MINT, th.PINK]).move_to([0, -0.35, 0])
        with self.say("This grid is the heart of the unit. A or an: only a singular countable, a book. Much: only uncountables, much time. Many: only plural countables, many books. A few and several: plural countables. A little: uncountables, a little milk. Each and every: a singular countable, each boy. Both: two of something, both hands. And some, any, a lot of and enough go with both plural countables and uncountables.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h2 = E.head(self, "The tricky pairs")
        cards = VGroup(
            E.card("some / any", "some in positives and offers (Would you like some tea?); any in negatives and questions — or \"it doesn't matter which\": Take any seat.", th.SKY, w=6.1, h=2.6, size=22),
            E.card("each / every", "both + singular noun and verb. Each: one by one, even of two. Every: the whole group, three or more. Each of the students was present.", th.AMBER, w=6.1, h=2.6, size=22),
            E.card("either / neither, both / all", "either, neither, both: for two. All: for more than two. All of them — \"of\" before a pronoun.", th.MINT, w=6.1, h=2.6, size=22),
            E.card("fewer / less", "fewer counts (fewer students); less measures (less sugar). \"10 items or less\" is wrong.", th.PINK, w=6.1, h=2.6, size=22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("The tricky pairs. Some in positive sentences and in offers: would you like some tea? Any in negatives and questions, or meaning it doesn't matter which: take any seat. Each and every both take a singular noun and verb; each looks at members one by one, every at the whole group. Either, neither and both are for two; all for more than two. And fewer counts while less measures: fewer students, less sugar."):
            self.play(ReplacementTransform(h, h2), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(VGroup(h2, cards)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Uncountable in English, countable in Nepali")
        words = ["information", "advice", "news", "furniture", "luggage", "equipment", "stationery", "scenery", "knowledge", "homework", "research", "progress", "evidence", "traffic", "money", "bread", "hair", "jewellery", "permission", "damage"]
        chips = VGroup(*[E.chip(w_, th.AMBER, size=24) for w_ in words]).arrange_in_grid(rows=4, buff=(0.18, 0.22)).move_to([0, 0.9, 0])
        chips.scale_to_fit_width(min(chips.width, 12.4))
        rule = T("no -s  ·  no a/an  ·  singular verb  ·  much / a little", size=28, color=th.MINT).move_to([0, -1.3, 0])
        with self.say("These nouns are uncountable in English, even though in Nepali they can be counted: information, advice, news, furniture, luggage, equipment, stationery, scenery, knowledge, homework, research, progress, evidence, traffic, money, bread, hair, jewellery, permission and damage. So: no s, no a or an, a singular verb, and much or a little rather than many or a few."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, scale=0.8) for c_ in chips], lag_ratio=0.06), run_time=4)
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(chips, rule)))
        rows = [["instead of", "say"], ["two informations", "two pieces of information"], ["many advices", "much advice / several pieces of advice"], ["a good news", "good news / a piece of good news"], ["three luggages", "three pieces of luggage"], ["a bread", "a loaf of bread / a slice of bread"], ["thunders", "a clap of thunder"]]
        tb = E.table(rows, [4.6, 7.4], row_h=0.6, size=24, colors=[th.CORAL, th.MINT]).move_to([0, 0.5, 0])
        nt = para("Plural only: scissors, trousers, spectacles, clothes, goods, cattle, police, people — two pairs of trousers. And \"news\" is singular: The news is encouraging.", width=11.4, size=24, color=th.INK).move_to([0, -2.3, 0])
        with self.say("To count them, use a measure phrase: two pieces of information, several pieces of advice, a piece of good news, three pieces of luggage, a loaf of bread, a clap of thunder. Some nouns are plural only and take a plural verb: scissors, trousers, spectacles, clothes, cattle, police, people; count them with a pair of. And news is singular despite its s: the news is encouraging.") as v:
            E.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Errors in every script")
        pairs = [("He gave me many advices.", "He gave me much advice."), ("She has a long hair.", "She has long hair."), ("Less students came today.", "Fewer students came today."),
                 ("Every students must attend.", "Every student must attend."), ("One of my friend lives here.", "One of my friends lives here."), ("My this pen is new.", "This pen of mine is new.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.7, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("The errors that appear in every script. Many advices: much advice. A long hair: long hair, uncountable. Less students: fewer students. Every students: every student, singular. One of my friend: one of my friends, plural after one of. And my this pen: only one central determiner is allowed, so this pen of mine."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.6)
                self.hold(1.3)
        self.play(FadeOut(VGroup(h, grid)))
        h = E.head(self, "Worked item: few, a few, little, a little")
        rows = [["sentence", "noun", "sense", "answer"], ["Very ___ sugar is left: no sugar today.", "uncountable", "almost none", "little"], ["___ students came: there was a strike.", "plural", "almost none", "Few"], ["He has ___ friends, so he's never lonely.", "plural", "positive", "a few"]]
        tb = E.table(rows, [6.4, 2.4, 2.4, 1.6], row_h=0.8, size=24, colors=[th.INK, th.SKY, th.AMBER, th.MINT]).move_to([0, 0.6, 0])
        nt = para("\"Few\" and \"little\" are negative: hardly any. \"A few\" and \"a little\" are positive: some.", width=11, size=26, color=th.AMBER).move_to([0, -1.9, 0])
        with self.say("A worked item. There is very blank sugar left, so make the tea without it. Sugar is uncountable, and the amount is almost none: little. Blank students attended, because there was a strike: plural countable, almost none: few. He has blank friends there, so he is never lonely: plural countable, and positive: a few. Remember: few and little are negative, meaning hardly any; a few and a little are positive, meaning some.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))
        h = E.head(self, "Worked item: supply the articles")
        s = para("Yesterday I met ___ old friend of my father at ___ bus park. He is ___ engineer and works for ___ government.", width=11, size=30, color=th.INK).move_to([0, 1.4, 0])
        st = E.bullets(["old friend: singular, first mention, vowel sound → an", "bus park: we both know which → the", "engineer: a job after \"be\", vowel sound → an", "government: only one here → the"], width=11, size=26).move_to([0, -1.2, 0])
        with self.say("And articles. Yesterday I met blank old friend of my father at blank bus park. He is blank engineer and works for blank government. Old friend: singular, first mention, and old begins with a vowel sound: an. Bus park: we both know which one: the. Engineer: a job title after be, with a vowel sound: an. Government: there is only one here: the."):
            self.play(FadeIn(h), FadeIn(s))
            E.reveal_list(self, st, 9.0)
        self.play(FadeOut(VGroup(h, s, st)))
        self.quiz("He gave me ____ .",
                  ["many useful informations", "much useful information", "an useful information", "a useful informations"], 1,
                  "Pause and think.",
                  "Information is uncountable: no -s, no a/an, and \"much\" rather than \"many\".")
        self.quiz("\"___ honest man never lies.\"",
                  ["A", "An", "The", "no article"], 1,
                  "One more.",
                  "\"Honest\" begins with a vowel sound — the h is silent — so \"an\".")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Ask first: countable or uncountable? singular or plural?",
            "A / an by sound: a university, an hour, an MA.",
            "The for the known one; no article for names, general plurals, by bus.",
            "Much + uncountable, many + plural; few/little negative, a few/a little positive.",
            "Information, advice, news, furniture: no -s, no a/an; use \"a piece of\".",
        ], "Quick recap. Two questions first. A or an by sound. The, and no article. The determiner grid. And the uncountable nouns that trip up every script.")
        self.outro("That was determiners and quantifiers. Next: subject verb agreement. See you there.")
