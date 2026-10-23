import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 25
    TITLE = "Connectives and Discourse Markers"
    SUBTITLE = "Grammar · because, although, however, therefore, in spite of"
    SECTIONS = ["Check what must follow", "Connectives by meaning", "Paired connectives", "Punctuation and doubled connectives", "Look-alikes", "Joining sentences"]
    NEXT = "Unit 26 · Adjectives, Adverbs and Adjective Order"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        s = E.sentence("Although he was ill, but he attended the class.", size=38).move_to([0, 1.0, 0])
        but = s.words[4]
        cross = E.strike(but)
        fix = T("Although he was ill, he attended the class.", size=38, color=th.MINT).move_to([0, -0.4, 0])
        with self.say("Although he was ill, but he attended the class. In Nepali, two connectives in one sentence are natural. In English, one is enough."):
            self.play(FadeIn(s))
            self.play(but.animate.set_color(th.CORAL), Create(cross))
            self.play(FadeIn(fix, shift=UP * 0.15))
        nt = para("Connectives of the same meaning need different grammar: because + a clause, because of + a noun, therefore after a full stop.", width=11, size=28, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("And here is the deeper trick of this unit: connectives with the same meaning need different grammar. Because takes a clause; because of takes a noun; therefore needs a full stop or a semicolon in front of it. Meaning is not enough. Always check what must follow."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(s, cross, fix, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 25: connectives and discourse markers."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Check what must follow. Connectives grouped by meaning. Paired connectives. Punctuation and doubled connectives. Look alikes. And joining sentences, the NEB way.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "One idea, four grammars")
        rows = VGroup(*[E.card(k_, ex_ + "\n" + n_, c_, w=6.1, h=2.6, tsize=26, size=24) for k_, ex_, n_, c_ in [
            ("subordinating conjunction", "We returned because the road was blocked.", "+ a clause: because, although, when, if", th.SKY),
            ("coordinating conjunction", "The road was blocked, so we returned.", "comma before: and, but, so, or, yet", th.MINT),
            ("discourse marker", "The road was blocked; therefore, we returned.", ". or ; before, comma after: however, therefore", th.AMBER),
            ("preposition", "We returned because of the blocked road.", "+ a noun or -ing: because of, in spite of", th.PINK)]]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("One idea, a blocked road and our return, in four grammars. A subordinating conjunction like because, although, when or if is followed by a clause: we returned because the road was blocked. A coordinating conjunction like and, but, so, or, yet joins two clauses, with a comma before it: the road was blocked, so we returned. A discourse marker like however, therefore or moreover cannot join clauses by itself: it needs a full stop or a semicolon before it, and a comma after it. And a preposition like because of, in spite of or despite is followed by a noun or an ing form: because of the blocked road."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=UP * 0.15), run_time=0.6)
                self.hold(3.2)
        self.play(FadeOut(VGroup(h, rows)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["relation", "+ clause", "marker", "+ noun / -ing"], ["addition", "—", "moreover, besides", "in addition to"], ["contrast", "although, whereas", "however", "in spite of, despite"], ["cause", "because, since, as", "—", "because of, due to"],
                ["result", "so … that", "therefore, hence", "—"], ["purpose", "so that, lest", "—", "in order to"], ["condition", "if, unless", "otherwise", "without, but for"], ["time", "when, until, as soon as", "then, meanwhile", "during"]]
        tb = E.table(rows, [2.2, 3.8, 3.2, 3.6], row_h=0.6, size=24, colors=[th.AMBER, th.SKY, th.MINT, th.PINK]).move_to([0, 0.5, 0])
        nt = T("plus: for example, such as (example) · similarly, likewise (comparison) · in short, in conclusion (summary)", size=22, color=th.MUTED).move_to([0, -2.4, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Grouped by meaning. Addition: moreover, furthermore, besides; in addition to before a noun. Contrast: although with a clause, however as a marker, in spite of or despite with a noun. Cause: because, since, as with a clause; because of, owing to, due to with a noun. Result: so that and such that; therefore, consequently, hence. Purpose: so that with a clause, in order to with a verb. Condition: if, unless, provided that; otherwise as a marker. Time: when, while, until, as soon as; then, meanwhile, finally.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        rows = [["pair", "example", "watch"], ["both … and", "She is both clever and hard-working.", "plural verb"], ["neither … nor", "Neither the pen nor the book is mine.", "never \"or\"; nearer subject"], ["not only … but also", "He not only sings but also plays.", "same shape both sides"],
                ["whether … or", "I don't know whether he'll come or not.", "not \"if … or not\""], ["so / such … that", "so tired that … / such a cold night that …", "so + adj; such + noun"], ["too … to", "The box is too heavy to lift.", "already negative"], ["lest … should", "Work hard lest you should fail.", "already negative"]]
        tb = E.table(rows, [3.2, 5.6, 3.6], row_h=0.6, size=22, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.5, 0])
        with self.say("Paired connectives come in two halves, and both must be present. Both and, with a plural verb. Neither nor, never neither or, and the verb follows the nearer subject. Not only but also, with the same grammatical shape on both sides. Whether or not. So with an adjective, such with a noun: so tired that, such a cold night that. And two pairs that are already negative, so never add not: the box is too heavy to lift; work hard lest you should fail.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = E.head(self, "No sooner … than   ·   Hardly … when")
        a = E.sentence("The teacher entered the class. The students stood up.", size=30).move_to([0, 1.6, 0])
        b = E.sentence("No sooner had the teacher entered the class than the students stood up.", size=30, color=th.MINT).move_to([0, 0.2, 0])
        b.scale_to_fit_width(min(b.width, 12.6))
        c = E.sentence("Hardly had the teacher entered the class when the students stood up.", size=30, color=th.SKY).move_to([0, -1.0, 0])
        c.scale_to_fit_width(min(c.width, 12.6))
        nt = para("Earlier event after \"no sooner\", in the past perfect, with inversion: had + subject. Then \"than\" — never \"then\". With hardly / scarcely, use \"when\".", width=11.4, size=24, color=th.AMBER).move_to([0, -2.5, 0])
        with self.say("The pair the board loves most. The teacher entered the class; the students stood up. Put the earlier event after no sooner, in the past perfect, and invert: no sooner had the teacher entered the class. Then join with than, never then: than the students stood up. With hardly or scarcely, the second half takes when: hardly had the teacher entered the class when the students stood up."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b, shift=DOWN * 0.15))
            m1 = E.mark(VGroup(*b.words[0:3]), th.AMBER)
            m2 = E.mark(b.words[8], th.CORAL)
            self.play(Create(m1), Create(m2))
            self.play(FadeIn(c, shift=DOWN * 0.15))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, c, m1, m2, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "A discourse marker can't join two clauses alone")
        wr = E.wrong_right("It was late, however we continued.", "It was late. However, we continued.", size=30).move_to([0, 1.2, 0])
        alt = T("✓ It was late; however, we continued.", size=30, color=th.MINT).next_to(wr, DOWN, buff=0.2).align_to(wr, LEFT)
        rules = E.bullets(["comma before a coordinating conjunction joining two clauses: The power went off, and the fans stopped.", "comma after a fronted clause: When the bell rang, the children rushed out.", "no comma the other way round: The children rushed out when the bell rang."], width=11.4, size=24).move_to([0, -1.6, 0])
        with self.say("Punctuation the examiner checks. A discourse marker cannot join two clauses by itself: it was late, however we continued, is wrong. Use a full stop, or a semicolon, before it and a comma after it. Also: a comma before a coordinating conjunction that joins two full clauses; a comma after a subordinate clause at the front; and no comma when the subordinate clause comes second."):
            self.play(FadeIn(h), FadeIn(wr.wrong))
            self.play(Create(wr.cross), FadeIn(wr.right), FadeIn(alt))
            E.reveal_list(self, rules, 7.0)
        self.play(FadeOut(VGroup(h, wr, alt, rules)))
        h = E.head(self, "Never double the connective")
        pairs = [("Although he was ill, but he came.", "Although he was ill, he came."), ("Because it rained, so we stayed in.", "It rained, so we stayed in."), ("No sooner had he left then it rained.", "No sooner had he left than it rained."),
                 ("Unless you don't work hard, you'll fail.", "Unless you work hard, you'll fail."), ("Work hard lest you should not fail.", "Work hard lest you should fail."), ("Despite of the rain, the match went on.", "Despite the rain, the match went on.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And never double the connective, the commonest Nepali influenced error. Although with but: keep one. Because with so: keep one. No sooner with then: it must be than. Unless already means if not, so never unless you don't. Lest is already negative, so never lest you should not. And despite never takes of."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.6)
                self.hold(1.2)
        self.play(FadeOut(VGroup(h, grid)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        rows = [["pair", "difference", "example"], ["because / because of", "clause / noun", "because of his illness"], ["although / in spite of", "clause / noun", "in spite of his poverty"], ["beside / besides", "next to / as well as", "Besides Nepali, he speaks Maithili."],
                ["so / such", "adjective / noun", "so cold / such a cold night"], ["too / very", "too much / a lot", "too hot to drink"], ["since / for", "point / length of time", "since Monday / for three days"]]
        tb = E.table(rows, [4.0, 3.4, 5.4], row_h=0.66, size=24, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.3, 0])
        with self.say("Look alikes. Because with a clause, because of with a noun. Although with a clause, in spite of with a noun. Beside means next to; besides means in addition to. So with an adjective, such with a noun. Too means more than is acceptable: too hot to drink. And since marks a point of time, for a length of time.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["use", "join: The tea was very hot. I could not drink it."], ["so … that", "The tea was so hot that I could not drink it."], ["too … to", "The tea was too hot to drink."], ["although", "He was tired. He finished. → Although he was tired, he finished."],
                ["unless", "Work hard. Otherwise you'll fail. → Unless you work hard, you'll fail."], ["in spite of", "He was ill. He came. → In spite of his illness, he came."], ["so that", "She got up early. She wanted the first bus. → … so that she could catch the first bus."]]
        tb = E.table(rows, [2.6, 10.2], row_h=0.62, size=22, colors=[th.AMBER, th.INK]).move_to([0, 0.5, 0])
        with self.say("Joining sentences, the patterns NEB sets. The tea was very hot; I could not drink it. With so that: the tea was so hot that I could not drink it. With too to: the tea was too hot to drink. With although: although he was tired, he finished. With unless: unless you work hard, you will fail. With in spite of, turn the clause into a noun: in spite of his illness. And with so that for purpose: she got up early so that she could catch the first bus.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = E.head(self, "Worked item: the right form for the gap")
        items = VGroup(*[VGroup(T(a_, size=28, color=th.INK), T(b_, size=24, color=c_)).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for a_, b_, c_ in [
            ("(a) The flight was cancelled ____ the bad weather.", "a noun phrase follows → a preposition: because of", th.PINK),
            ("(b) ____ the weather was bad, the flight was cancelled.", "a clause, at the front → a conjunction: Because", th.SKY),
            ("(c) The weather was bad; ____, the flight was cancelled.", "a semicolon before, a comma after → a marker: therefore", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        items.scale_to_fit_width(min(items.width, 12.4))
        with self.say("A worked item. The flight was cancelled blank the bad weather: a noun phrase follows, so a preposition: because of. Blank the weather was bad, the flight was cancelled: a full clause at the front, so a conjunction: because. The weather was bad, semicolon, blank, comma, the flight was cancelled: a semicolon before and a comma after means a discourse marker: therefore."):
            self.play(FadeIn(h))
            for i_ in items:
                self.play(FadeIn(i_, shift=UP * 0.15))
                self.hold(3.5)
        self.play(FadeOut(VGroup(h, items)))
        self.quiz("\"____ the heavy rain, the match went on.\"",
                  ["Although", "In spite of", "Despite of", "However"], 1,
                  "Pause and think.",
                  "A noun phrase follows, so a preposition: in spite of (or despite, without of).")
        self.quiz("\"No sooner had he reached the stop ____ the bus left.\"",
                  ["then", "when", "than", "that"], 2,
                  "One more.",
                  "No sooner … than. (Hardly … when.)")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Check what follows: clause, comma + clause, a sentence break, or a noun.",
            "because / because of; although / in spite of; despite (never \"of\").",
            "However, therefore: a full stop or semicolon before, a comma after.",
            "Pairs: neither … nor, not only … but also, no sooner … than, hardly … when.",
            "Never double: although … but, because … so, unless … don't.",
        ], "Quick recap. Check what must follow. The four grammars of connectives. Pairs that come in halves. Punctuation round discourse markers. And never doubling the connective.")
        self.outro("That was connectives and discourse markers. Next: adjectives, adverbs and adjective order. See you there.")
