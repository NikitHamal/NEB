import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def person(color, s=1.0):
    return VGroup(Circle(radius=0.22, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4), Line(DOWN * 0.22, DOWN * 0.85, color=color, stroke_width=3),
                  Line(DOWN * 0.85, DOWN * 1.25 + LEFT * 0.2, color=color, stroke_width=3), Line(DOWN * 0.85, DOWN * 1.25 + RIGHT * 0.2, color=color, stroke_width=3)).scale(s)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 30
    TITLE = "Prepositions, Tenses and Relative Clauses"
    SUBTITLE = "Grammar · in/on/at, fixed prepositions, tenses, who/which/that"
    SECTIONS = ["In, on, at", "Fixed prepositions", "Twelve tenses", "Sequence of tenses", "Relative clauses: the comma test", "Relative-clause details and worked items"]
    NEXT = "Unit 31 · Guided Writing"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        chips = VGroup(*[E.chip(t_, c_, size=34) for t_, c_ in [("good at English", th.SKY), ("married to someone", th.PINK), ("angry with someone", th.CORAL)]]).arrange(DOWN, buff=0.4).move_to([0, 0.8, 0])
        with self.say("Good at English. Married to someone. Angry with someone. Nothing in logic explains why these prepositions are the right ones. They are simply fixed, and the examiner marks them."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in chips], lag_ratio=0.4))
        nt = para("This last grammar unit gathers the three areas that cost the most marks: prepositions, the sequence of tenses, and relative clauses — where one comma changes the meaning.", width=11, size=28, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("This last grammar unit gathers the three areas that appear most often and do the most damage: prepositions, the sequence of tenses, and relative clauses, where a single comma can change the meaning of a sentence."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(chips, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 30: prepositions, tenses and relative clauses."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. In, on and at. Fixed prepositions. The twelve tenses. The sequence of tenses. Relative clauses and the comma test. And relative clause details, with worked items.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "In, on, at: narrowing down")
        boxes = VGroup()
        specs = [("in", "in May · in 2026 · in winter · in the morning · in Nepal", 12.4, 4.8, th.SKY), ("on", "on Sunday · on 5 June · on my birthday · on the table", 9.8, 3.0, th.MINT), ("at", "at 6 o'clock · at night · at the bus stop", 7.2, 1.2, th.AMBER)]
        for w_, ex_, bw, bh, c_ in specs:
            r = RoundedRectangle(corner_radius=0.15, width=bw, height=bh, stroke_color=c_, stroke_width=4, fill_color=c_, fill_opacity=0.05).move_to([0, -0.55, 0])
            lab = T(w_, size=34, color=c_, weight="BOLD")
            ex = T(ex_, size=24, color=th.INK)
            if w_ == "at":
                lab.move_to(r.get_left() + RIGHT * 0.5)
                ex.next_to(lab, RIGHT, buff=0.4)
            else:
                lab.move_to(r.get_corner(UL) + np.array([0.45, -0.38, 0]))
                ex.next_to(lab, RIGHT, buff=0.4)
            if ex.get_right()[0] > r.get_right()[0] - 0.2:
                ex.scale_to_fit_width(r.get_right()[0] - 0.2 - ex.get_left()[0]).next_to(lab, RIGHT, buff=0.4)
            boxes.add(VGroup(r, lab, ex))
        with self.say("Prepositions of time and place narrow down. In is for the largest area: in May, in twenty twenty six, in winter, in the morning, in Nepal. On is for a day or a surface: on Sunday, on the fifth of June, on my birthday, on the table. At is for a single point: at six o'clock, at night, at the bus stop."):
            self.play(FadeIn(h))
            for b_ in boxes:
                self.play(FadeIn(b_), run_time=0.8)
                self.hold(3.5)
        self.play(FadeOut(VGroup(h, boxes)))
        rows = [["pair", "difference", "example"], ["since / for", "a point / a length of time", "since 2019 · for three years"], ["during / for", "+ a noun / + a period", "during the holidays · for a week"], ["by / until", "not later than / up to", "Finish it by Friday. Wait until Friday."], ["in time / on time", "early enough / punctually", "We arrived in time for the bus."],
                ["between / among", "two / more than two", "between the two · among the students"], ["beside / besides", "next to / in addition to", "Sit beside me. Besides English, …"]]
        tb = E.table(rows, [3.2, 4.2, 5.4], row_h=0.64, size=24, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.3, 0])
        with self.say("Pairs that are regularly confused. Since marks a point of time, for a length: since twenty nineteen, for three years. During takes a noun, for a period. By means not later than: finish it by Friday; until means up to that moment: wait until Friday. In time means early enough; on time means punctually. Between two, among more than two. And beside means next to, besides means in addition to.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Fixed prepositions: learn them as one word")
        pairs = ["good at", "afraid of", "married to", "angry with (a person)", "interested in", "famous for", "proud of", "different from", "similar to", "responsible for", "depend on", "consist of", "apologise to … for", "belong to", "congratulate on", "insist on", "accuse of", "prevent from", "succeed in", "object to"]
        chips = VGroup(*[E.chip(p_, th.PALETTE[k % 8], size=24) for k, p_ in enumerate(pairs)]).arrange_in_grid(rows=5, buff=(0.2, 0.25)).move_to([0, 0.1, 0])
        chips.scale_to_fit_width(min(chips.width, 12.4))
        with self.say("Fixed prepositions: learn each pair as if it were one word. Good at, afraid of, married to, angry with a person, interested in, famous for, proud of, different from, similar to, responsible for. And verbs: depend on, consist of, apologise to someone for something, belong to, congratulate on, insist on, accuse of, prevent from, succeed in, object to."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, scale=0.8) for c_ in chips], lag_ratio=0.12), run_time=6)
        self.play(FadeOut(chips))
        h2 = E.head(self, "Verbs that take no preposition at all")
        pairs = [("discuss about the problem", "discuss the problem"), ("enter into the hall", "enter the hall"), ("marry with her", "marry her"), ("reach at the station", "reach the station"), ("return back home", "return home"), ("resemble to his father", "resemble his father"), ("emphasise on the point", "emphasise the point"), ("comprise of five members", "comprise five members")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=4, cols=2, buff=(0.8, 0.35), col_alignments="ll").move_to([0, -0.25, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And the verbs that take no preposition, the ones Nepali speakers add one to. Discuss the problem, never discuss about. Enter the hall. Marry her, or be married to her. Reach the station, although you arrive at it. Return home, not return back. Resemble his father. Emphasise the point. And comprise five members, although it consists of five."):
            self.play(ReplacementTransform(h, h2))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.3)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.45)
                self.hold(0.9)
        self.play(FadeOut(grid))
        pairs = [("She is good in Mathematics.", "She is good at Mathematics."), ("He is married with a teacher.", "He is married to a teacher."), ("different than that one", "different from that one"), ("I am waiting your reply.", "I am waiting for your reply."), ("He replied my letter.", "He replied to my letter."), ("She listened the news.", "She listened to the news.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.8, 0.45), col_alignments="ll").move_to([0, -0.25, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        h3 = E.head(self, "…and the ones that need one")
        with self.say("The opposite errors are just as common: missing or wrong prepositions. Good at Mathematics, not good in. Married to a teacher. Different from. Waiting for your reply. Replied to my letter. Listened to the news."):
            self.play(ReplacementTransform(h2, h3))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.3)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.45)
                self.hold(0.8)
        self.play(FadeOut(VGroup(h3, grid)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Twelve tenses: three times × four aspects")
        cols = ["simple", "continuous", "perfect", "perfect continuous"]
        rows_ = [("past", ["wrote", "was writing", "had written", "had been writing"]), ("present", ["writes", "is writing", "has written", "has been writing"]), ("future", ["will write", "will be writing", "will have written", "will have been writing"])]
        rows = [["", *cols]] + [[r_, *cells] for r_, cells in rows_]
        tb = E.table(rows, [2.0, 2.4, 3.0, 2.9, 3.6], row_h=0.8, size=26, colors=[th.AMBER, th.SKY, th.MINT, th.PINK, th.CORAL]).move_to([0, 0.7, 0])
        sig = E.bullets(["present perfect: just, already, yet, ever, never, so far", "perfect continuous: for, since, all day, how long", "past perfect: before, after, by the time — the earlier of two past events"], width=11.2, size=24).move_to([0, -2.1, 0])
        with self.say("All twelve tenses fit one grid: three times, past, present and future, by four aspects: simple, continuous, perfect and perfect continuous. He wrote, was writing, had written, had been writing. He writes, is writing, has written, has been writing. He will write, will be writing, will have written, will have been writing. Learn the signal words too: just, already and yet call for the present perfect; for and since for the perfect continuous; before and by the time for the past perfect.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.55)
            E.reveal_list(self, sig, v.dur * 0.3)
        self.play(FadeOut(VGroup(h, tb, sig)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "A past main verb pulls the next clause into the past")
        ex = VGroup(*[T(t_, size=30, color=th.INK) for t_ in ["He said that he was unwell.", "She asked what I wanted.", "They left before the guests arrived."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.3, 0])
        exc = E.bullets(["universal truth: He said that honesty is the best policy.", "comparison after than: He worked harder than I do.", "habitual present fact: She told me that she goes to the gym every morning."], width=11.2, size=24).move_to([0, -1.2, 0])
        with self.say("The sequence of tenses. When the main verb is in the past, the verb in the subordinate clause is normally past too. He said that he was unwell. She asked what I wanted. They left before the guests arrived. Three exceptions: a universal truth stays present, he said that honesty is the best policy; a comparison after than may keep its own tense; and a present habit may be kept: she told me that she goes to the gym every morning."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(e_) for e_ in ex], lag_ratio=0.4))
            E.reveal_list(self, exc, 8.0)
        self.play(FadeOut(VGroup(ex, exc)))
        h2 = E.head(self, "Two past events: the earlier one is past perfect")
        tl = Arrow([-6.0, 0.2, 0], [6.0, 0.2, 0], buff=0, color=th.MUTED, stroke_width=4)
        e1 = VGroup(Dot([-2.4, 0.2, 0], radius=0.14, color=th.CORAL), T("the train left", size=26, color=th.CORAL).move_to([-2.4, 0.75, 0]), T("had left", size=26, color=th.CORAL, weight="BOLD").move_to([-2.4, -0.35, 0]))
        e2 = VGroup(Dot([2.4, 0.2, 0], radius=0.14, color=th.SKY), T("I reached the station", size=26, color=th.SKY).move_to([2.4, 0.75, 0]), T("reached", size=26, color=th.SKY, weight="BOLD").move_to([2.4, -0.35, 0]))
        s = T("When I reached the station, the train had left.", size=32, color=th.MINT).move_to([0, -1.6, 0])
        w = T("✗ When I reached the station, the train left.  (= it left as I arrived)", size=24, color=th.CORAL).move_to([0, -2.5, 0])
        w.scale_to_fit_width(min(w.width, 12.4))
        with self.say("When two past events are told together, the earlier one takes the past perfect. The train left first; then I reached the station. When I reached the station, the train had left. If you write the train left, you say it left at the moment you arrived."):
            self.play(ReplacementTransform(h, h2), GrowArrow(tl))
            self.play(FadeIn(e1))
            self.play(FadeIn(e2))
            self.play(FadeIn(s))
            self.play(FadeIn(w))
        self.play(FadeOut(VGroup(tl, e1, e2, s, w)))
        h3 = E.head(self, "Tense errors in exam scripts")
        pairs = [("I am knowing the answer.", "I know the answer."), ("He has gone to Pokhara last week.", "He went to Pokhara last week."), ("I am working here since 2020.", "I have been working here since 2020."), ("If he will come, I'll meet him.", "If he comes, I'll meet him.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.5), col_alignments="ll").move_to([0, 0.3, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        nt = para("Stative verbs — know, believe, like, want, own — take no -ing. The present perfect never takes a finished time like \"last week\".", width=11.2, size=24, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("The tense errors examiners see most. I am knowing: stative verbs like know, believe, want and own are not used in the continuous, so I know. He has gone to Pokhara last week: the present perfect never takes a finished past time, so he went. I am working here since twenty twenty: with since, the present perfect continuous, I have been working. And if he will come: if he comes."):
            self.play(ReplacementTransform(h2, h3))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.35)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h3, grid, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        rows = [["pronoun", "used for", "example"], ["who", "a person, as subject", "the girl who won the prize"], ["whom", "a person, as object (formal)", "the man whom we met"], ["whose", "possession", "the boy whose bag was lost"], ["which", "a thing or animal", "the house which stands on the hill"],
                ["that", "person or thing — defining only", "the bus that goes to Bhaktapur"], ["where / when / why", "a place / a time / a reason", "the village where I was born"]]
        tb = E.table(rows, [3.0, 4.6, 5.2], row_h=0.64, size=24, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.3, 0])
        with self.say("A relative clause describes a noun, and begins with a relative pronoun. Who for a person as subject: the girl who won the prize. Whom for a person as object, in formal English. Whose for possession. Which for a thing or an animal. That for a person or thing, but only in defining clauses. And where, when and why for a place, a time and a reason.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = E.head(self, "The comma test")
        a = T("My brother who lives in Pokhara is a doctor.", size=30, color=th.SKY).move_to([0, 2.0, 0])
        bros = VGroup(*[person(c_) for c_ in [th.MUTED, th.SKY, th.MUTED]]).arrange(RIGHT, buff=0.6).move_to([-3.2, 0.4, 0])
        la = para("no commas = defining: it tells you WHICH brother — so I have more than one", width=5.6, size=24, color=th.SKY).move_to([2.8, 0.4, 0])
        b = T("My brother, who lives in Pokhara, is a doctor.", size=30, color=th.MINT).move_to([0, -1.3, 0])
        one = person(th.MINT).move_to([-3.2, -2.6, 0])
        lb = para("commas = non-defining: just extra information — I have one brother; \"that\" is forbidden", width=5.6, size=24, color=th.MINT).move_to([2.8, -2.6, 0])
        with self.say("Commas decide what a relative clause means. My brother who lives in Pokhara is a doctor, with no commas, is a defining clause: it tells you which brother, so I must have more than one. My brother, comma, who lives in Pokhara, comma, is a doctor: a non defining clause, just extra information about a brother already identified, so I have only one. And in a non defining clause, that is forbidden."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in bros], lag_ratio=0.2), FadeIn(la))
            self.play(Indicate(bros[1], color=th.SKY))
            self.play(FadeIn(b))
            self.play(FadeIn(one), FadeIn(lb))
        self.play(FadeOut(VGroup(h, a, bros, la, b, one, lb)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Details that win marks")
        cards = VGroup(
            E.card("drop the object pronoun", "This is the book (that) I told you about. Never drop the subject: the man who lives next door.", th.SKY, w=6.1, h=2.6, size=24),
            E.card("\"that\" after superlatives", "the best film that I have ever seen; all, only, nothing that …", th.AMBER, w=6.1, h=2.6, size=24),
            E.card("prepositions", "the officer to whom I spoke = the officer I spoke to. Never \"to that\".", th.MINT, w=6.1, h=2.6, size=24),
            E.card("reduced clauses", "the boy standing at the gate; the letter written by him", th.PINK, w=6.1, h=2.6, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("Details that win marks. In a defining clause you may drop the pronoun when it is the object: this is the book I told you about; but never when it is the subject. That is preferred after superlatives and after all, only and nothing. A preposition may go before whom or which, or at the end, but never before that. And a relative clause can often shrink to a participle: the boy standing at the gate; the letter written by him."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(cards))
        h2 = E.head(self, "Relative-clause errors")
        pairs = [("The boy who he came yesterday …", "The boy who came yesterday …"), ("the pen which I bought it", "the pen which I bought"), ("My father, that is a teacher, …", "My father, who is a teacher, …"), ("The house where I bought is small.", "The house which I bought is small.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.5), col_alignments="ll").move_to([0, 0.0, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And the errors. The boy who he came: the pronoun is already the subject, don't repeat it. The pen which I bought it: drop it. My father, that is a teacher: non defining, so who. And the house where I bought: where is not used when the noun is the object of the verb, so which."):
            self.play(ReplacementTransform(h, h2))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.35)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.0)
        self.play(FadeOut(grid))
        h3 = E.head(self, "Worked item: fill the prepositions")
        s = para("We arrived ___ the airport ___ 6 o'clock ___ the morning ___ 5 June, and waited ___ two hours ___ our flight.", width=11.4, size=28, color=th.INK).move_to([0, 1.6, 0])
        ans = VGroup(*[E.chip(t_, c_, size=28) for t_, c_ in [("at (place)", th.SKY), ("at (a point)", th.AMBER), ("in (part of a day)", th.SKY), ("on (a date)", th.MINT), ("for (a length)", th.PINK), ("for (wait for)", th.PINK)]]).arrange_in_grid(rows=2, buff=(0.3, 0.3)).move_to([0, -0.6, 0])
        nt = T("Careful: \"reach\" takes no preposition — \"arrive at\" does.", size=26, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("A worked item. We arrived blank the airport, blank six o'clock, blank the morning, blank the fifth of June, and waited blank two hours, blank our flight. Arrived at the airport. At six o'clock, a point. In the morning, part of a day. On the fifth of June, a date. For two hours, a length. And wait always takes for. Careful: if the verb were reach, there would be no preposition at all."):
            self.play(ReplacementTransform(h2, h3), FadeIn(s))
            self.play(LaggedStart(*[FadeIn(a_, scale=0.8) for a_ in ans], lag_ratio=0.35), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h3, s, ans, nt)))
        self.quiz("\"I have been living here ____ 2019.\"",
                  ["for", "since", "from", "at"], 1,
                  "Pause and think.",
                  "Since + a point of time; for + a length of time.")
        self.quiz("\"My mother, ____ is a nurse, works at night.\"",
                  ["that", "who", "which", "whom"], 1,
                  "One more.",
                  "Commas make it non-defining, so \"that\" is forbidden: who.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "In (big) → on (day, surface) → at (point); since a point, for a length.",
            "Fixed: good at, married to, different from; discuss / reach / marry — no preposition.",
            "Twelve tenses = 3 times × 4 aspects; past main verb → past clause.",
            "Two past events: the earlier is past perfect (the train had left).",
            "No commas = defining (which one); commas = extra, and never \"that\".",
        ], "Quick recap. In, on and at. Fixed prepositions and the verbs that take none. Twelve tenses in one grid, and their sequence. And relative clauses, where one comma changes the meaning.")
        self.outro("That completes the grammar. Next, writing: guided writing from charts, graphs and outlines. See you there.")
