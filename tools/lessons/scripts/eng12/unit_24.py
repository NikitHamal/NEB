import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def link(a, b, color=th.AMBER):
    """An arc over the sentence from the subject word a to the verb word b."""
    d = abs(b.get_x() - a.get_x())
    return ArcBetweenPoints(a.get_top() + UP * 0.12, b.get_top() + UP * 0.12, angle=-PI / 3 if d < 3 else -PI / 7, color=color, stroke_width=4)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 24
    TITLE = "Subject-Verb Agreement"
    SUBTITLE = "Grammar · concord, and the miscellaneous agreements"
    SECTIONS = ["Find the subject first", "Two subjects joined", "Pronouns, distributives, numbers", "Nouns that deceive", "Word order that hides the subject", "Other agreements and worked items"]
    NEXT = "Unit 25 · Connectives and Discourse Markers"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        s = E.sentence("The list of the students who passed have been published.", size=34).move_to([0, 0.8, 0])
        verb = s.words[7]
        with self.say("The list of the students who passed have been published. It sounds right, because students is the noun standing next to the verb. And it is wrong."):
            self.play(FadeIn(s))
            self.play(Indicate(VGroup(s.words[4], verb), color=th.CORAL))
        nt = para("The verb agrees with the head of the subject — never with the noun that happens to stand nearest.", width=11, size=30, color=th.AMBER).move_to([0, -1.4, 0])
        with self.say("The verb agrees with the head of the subject, the list, never with whatever noun happens to stand nearest. The board never tests he goes and they go. It tests exactly this kind of sentence."):
            arc = link(s.words[1], verb)
            self.play(Create(arc), s.words[1].animate.set_color(th.MINT), verb.animate.set_color(th.CORAL))
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(s, arc, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 24: subject verb agreement."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Find the subject first. Two subjects joined together. Pronouns, distributives and number phrases. Nouns that deceive. Word order that hides the subject. And the other agreements, with worked items.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Cross out the modifiers; what's left is the subject")
        s = E.sentence("The quality of the mangoes sold in the market was excellent.", size=32).move_to([0, 1.4, 0])
        mods = VGroup(*s.words[2:9])
        cross = E.strike(mods)
        rule = para("Cross out every phrase beginning with of, with, along with, as well as, including, besides — and every relative clause.", width=11, size=26, color=th.INK).move_to([0, -0.4, 0])
        with self.say("The method: cross out the modifiers. Take: the quality of the mangoes sold in the market was excellent. Cross out the phrase beginning with of, and everything describing the mangoes. What is left? The quality. Singular, so was."):
            self.play(FadeIn(h), FadeIn(s))
            self.play(mods.animate.set_opacity(0.35), Create(cross))
            arc = link(s.words[1], s.words[9])
            self.play(Create(arc), s.words[1].animate.set_color(th.MINT), s.words[9].animate.set_color(th.MINT))
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(s, cross, arc, rule)))
        ex = VGroup(*[T(t_, size=30, color=th.INK) for t_ in ["The list of candidates has been published.", "The causes of this accident are still unknown.", "One of my friends lives in Dhangadhi.", "The boy who won the prizes is from Surkhet."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-0.6, 0.0, 0])
        notes = VGroup(*[T(t_, size=24, color=th.MINT) for t_ in ["list → has", "causes → are", "one → lives", "boy → is"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(ex, RIGHT, buff=0.5)
        with self.say("More. The list of candidates has been published: the list. The causes of this accident are still unknown: the causes, plural. One of my friends lives in Dhangadhi: the subject is one. The boy who won the prizes is from Surkhet: the relative clause describes the boy, and the boy is."):
            for e_, n_ in zip(ex, notes):
                self.play(FadeIn(e_), FadeIn(n_), run_time=0.6)
                self.hold(1.6)
        self.play(FadeOut(VGroup(h, ex, notes)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["pattern", "verb", "example"], ["A and B", "plural", "Sita and Gita are cousins."], ["A and B = one thing", "singular", "Bread and butter is a cheap breakfast."], ["each / every A and B", "singular", "Every boy and every girl was given a badge."],
                ["A as well as / along with B", "agrees with A", "The captain, as well as the players, was praised."], ["either … or, neither … nor", "the nearer one", "Neither the teacher nor the students were present."], ["not only … but also; A or B", "the nearer one", "Not only the boys but also the girl was late."]]
        tb = E.table(rows, [4.2, 2.2, 6.4], row_h=0.66, size=22, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, 0.5, 0])
        with self.say("Two subjects joined together. With and, the subject is plural: Sita and Gita are cousins. But if the two words name one thing, the verb is singular: bread and butter is a cheap breakfast. Each and every keep it singular: every boy and every girl was given a badge. As well as, along with and together with only add information, so the verb agrees with the first subject: the captain, as well as the players, was praised. And with either or, neither nor, not only but also, and plain or, the verb agrees with the nearer subject.") as v:
            E.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        h = E.head(self, "Neither … nor: the nearer subject decides")
        a = E.sentence("Neither the principal nor the teachers are willing.", size=32).move_to([0, 1.3, 0])
        b = E.sentence("Neither the teachers nor the principal is willing.", size=32).move_to([0, -0.5, 0])
        nt = para("Same meaning, different verbs — exactly why the examiner sets them. And as well as is not and: Hari as well as his friends was absent.", width=11, size=26, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("See the proximity rule work both ways. Neither the principal nor the teachers are willing: the nearer subject, teachers, is plural. Turn it round: neither the teachers nor the principal is willing: the nearer subject is singular. Same meaning, different verbs. And remember, as well as is not and: Hari as well as his friends was absent."):
            self.play(FadeIn(h), FadeIn(a))
            arc = link(a.words[5], a.words[6], th.MINT)
            self.play(Create(arc), a.words[5].animate.set_color(th.MINT), a.words[6].animate.set_color(th.MINT))
            self.play(FadeIn(b))
            arc2 = link(b.words[5], b.words[6], th.SKY)
            self.play(Create(arc2), b.words[5].animate.set_color(th.SKY), b.words[6].animate.set_color(th.SKY))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, arc, arc2, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Singular, plural, or it depends")
        sing = VGroup(*[E.chip(w_, th.SKY, size=24) for w_ in ["each", "every", "either", "neither", "one", "everyone", "someone", "anybody", "nobody", "nothing", "many a", "more than one"]]).arrange_in_grid(rows=2, buff=(0.18, 0.22))
        plur = VGroup(*[E.chip(w_, th.MINT, size=24) for w_ in ["both", "few", "a few", "many", "several", "others"]]).arrange(RIGHT, buff=0.2)
        dep = VGroup(*[E.chip(w_, th.AMBER, size=24) for w_ in ["some", "all", "most", "half", "none", "a lot", "the rest", "fractions", "per cent"]]).arrange(RIGHT, buff=0.18)
        lab = [T("always singular", size=26, color=th.SKY, weight="BOLD"), T("always plural", size=26, color=th.MINT, weight="BOLD"), T("depends on the noun after \"of\"", size=26, color=th.AMBER, weight="BOLD")]
        g = VGroup(VGroup(lab[0], sing).arrange(DOWN, buff=0.2), VGroup(lab[1], plur).arrange(DOWN, buff=0.2), VGroup(lab[2], dep).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.45).move_to([0, -0.2, 0])
        g.scale_to_fit_width(min(g.width, 12.6))
        with self.say("Pronouns and distributives. Always singular: each, every, either, neither, one, everyone, someone, anybody, nobody, nothing, many a, and more than one, even though its meaning is plural: more than one house was damaged. Always plural: both, few, a few, many, several, others. And some words depend on the noun after of: some, all, most, half, none, a lot, the rest, fractions and percentages."):
            self.play(FadeIn(h))
            for part in g:
                self.play(FadeIn(part[0]), LaggedStart(*[FadeIn(c_, scale=0.8) for c_ in part[1]], lag_ratio=0.06))
                self.hold(2.0)
        self.play(FadeOut(g))
        ex = VGroup(T("Half of the apple is rotten.", size=30, color=th.SKY), T("Half of the apples are rotten.", size=30, color=th.MINT), T("Most of the water has dried up.", size=30, color=th.SKY), T("Most of the students have paid.", size=30, color=th.MINT)).arrange_in_grid(rows=2, buff=(0.8, 0.35)).move_to([0, 1.0, 0])
        num = VGroup(E.card("A number of", "+ plural verb: A number of tourists are waiting.", th.MINT, w=5.8, h=2.0, size=26), E.card("The number of", "+ singular verb: The number of tourists is rising.", th.SKY, w=5.8, h=2.0, size=26)).arrange(RIGHT, buff=0.3).move_to([0, -1.6, 0])
        with self.say("So: half of the apple is rotten, but half of the apples are rotten; most of the water has dried up, but most of the students have paid. And one pair to memorise. A number of means many, so it takes a plural verb: a number of tourists are waiting. The number of is a single figure, so it takes a singular verb: the number of tourists is rising."):
            self.play(LaggedStart(*[FadeIn(e_) for e_ in ex], lag_ratio=0.4))
            self.play(FadeIn(num))
        self.play(FadeOut(VGroup(h, ex, num)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        rows = [["group", "verb", "example"], ["subjects and diseases in -s", "singular", "Mathematics is easy. Measles is serious."], ["two-part tools and clothes", "plural", "The scissors are blunt."], ["a pair of + those", "singular", "A pair of scissors is missing."],
                ["plural meaning, no -s", "plural", "The police are investigating. Cattle are grazing."], ["titles, countries, bodies", "singular", "Gulliver's Travels is a satire."], ["one amount: money, time", "singular", "Twenty rupees is not much. Five years is long."],
                ["collective noun as one body", "singular", "The committee has taken a decision."], ["the + adjective (people)", "plural", "The rich are not always happy."], ["gerund, infinitive, clause", "singular", "Swimming is good exercise. To err is human."]]
        tb = E.table(rows, [4.2, 1.6, 7.0], row_h=0.58, size=22, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, 0.1, 0])
        with self.say("Nouns whose number is not what it looks. Subjects and diseases ending in s are singular: mathematics is easy; measles is serious. Two part tools and clothes are plural: the scissors are blunt; but a pair of scissors is missing. Police, cattle and people are plural without an s. Titles, countries and organisations are singular: the United States is a federal republic. An amount of money, time or distance is one amount: twenty rupees is not much; five years is a long time. A committee acting as one body is singular. The plus an adjective, the rich, is plural. And a gerund or infinitive subject is singular: swimming is good exercise; to err is human.") as v:
            E.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "When the subject comes after the verb")
        cards = VGroup(
            E.card("There is / There are", "the noun after it decides: There is a temple. There are two temples. A list: the nearer noun.", th.SKY, w=6.1, h=2.55, size=24),
            E.card("Here comes / Here come", "the same rule: Here comes the bus. Here come the buses.", th.MINT, w=6.1, h=2.55, size=24),
            E.card("inverted sentences", "the subject follows the verb: On the wall hang three old photographs.", th.AMBER, w=6.1, h=2.55, size=24),
            E.card("relative clauses", "one of the boys who have passed — but the only one who has passed", th.PINK, w=6.1, h=2.55, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("Word order can hide the subject. After there is and there are, the verb agrees with the noun that follows: there is a temple on the hill, there are two temples; with a mixed list, the nearer noun: there is a pen and two erasers. Here comes the bus; here come the buses. In an inverted sentence the subject follows the verb: on the wall hang three old photographs. And in relative clauses: he is one of the boys who have passed, because the boys passed; but he is the only one of the boys who has passed, because only he did."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.7), run_time=7)
        self.play(FadeOut(VGroup(h, cards)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Other agreements")
        cards = VGroup(
            E.card("pronoun and antecedent", "Every student must bring his or her admit card. The committee announced its decision.", th.SKY, w=6.1, h=2.4, size=24),
            E.card("this kind / these kinds", "This kind of book is useful. These kinds of books are useful. Never \"these kind of\".", th.AMBER, w=6.1, h=2.4, size=24),
            E.card("number compounds", "a five-year-old boy, a ten-rupee note, a two-hour journey — but the boy is five years old", th.MINT, w=6.1, h=2.4, size=24),
            E.card("sequence of tenses", "He said that he was busy. Except a universal truth: … that the earth moves round the sun.", th.PINK, w=6.1, h=2.4, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("Agreement is not only subject and verb. A pronoun matches its antecedent: every student must bring his or her admit card; the committee announced its decision. This kind of book is useful; these kinds of books are useful, never these kind of. Number compounds used as adjectives stay singular: a five year old boy, a ten rupee note, but the boy is five years old. And a past main verb pulls the next clause into the past, except a universal truth: the teacher told us that the earth moves round the sun."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.7), run_time=7)
        self.play(FadeOut(cards))
        h2 = E.head(self, "Worked item: five faults in one sentence")
        s = para("Each of the boy in these kind of classes have their own tablet, and the number of such classes are growing.", width=11.4, size=28, color=th.CORAL).move_to([0, 1.8, 0])
        fixes = E.bullets(["each of the boy → each of the boys (plural after \"each of\")", "these kind → these kinds", "have → has (the subject is \"each\")", "their → his or her (formal writing)", "the number … are → is"], width=11.2, size=25).move_to([0, -0.6, 0])
        ans = T("Each of the boys in these kinds of classes has his or her own tablet, and the number … is growing.", size=24, color=th.MINT).move_to([0, -2.9, 0])
        ans.scale_to_fit_width(min(ans.width, 12.4))
        with self.say("A worked item with five faults. Each of the boy in these kind of classes have their own tablet, and the number of such classes are growing. Each of must be followed by a plural noun: the boys. These must take kinds. The subject is each, which is singular: has. In formal writing, his or her. And the number of always takes a singular verb: is growing."):
            self.play(ReplacementTransform(h, h2), FadeIn(s))
            E.reveal_list(self, fixes, 10.0)
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(h2, s, fixes, ans)))
        self.quiz("\"The captain, along with his players, ____ arrived.\"",
                  ["have", "has", "are", "were"], 1,
                  "Pause and think.",
                  "Along with only adds information: the verb agrees with the captain — has.")
        self.quiz("\"Neither the students nor the teacher ____ present.\"",
                  ["were", "was", "are", "have"], 1,
                  "One more.",
                  "Neither … nor: the nearer subject, the teacher, is singular — was.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Cross out of-phrases and relative clauses; the head noun decides.",
            "And = plural; as well as / along with = the first subject.",
            "Either/neither … or/nor, not only … but also: the nearer subject.",
            "Each, every, one, many a: singular. A number of: plural; the number of: singular.",
            "Mathematics is, scissors are, the police are, five years is, these kinds of.",
        ], "Quick recap. Find the subject first. And against as well as. The nearer subject rule. Words that are always singular or plural. And the nouns that deceive.")
        self.outro("That was subject verb agreement. Next: connectives and discourse markers. See you there.")
