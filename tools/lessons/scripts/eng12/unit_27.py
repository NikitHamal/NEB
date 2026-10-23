import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def stair(labels, x0=-5.6, y0=1.6, dx=1.9, dy=-0.62, colors=None, size=26):
    """A staircase of tenses: each step one move back in time."""
    g = VGroup()
    for k, l_ in enumerate(labels):
        c_ = colors[k] if colors else th.PALETTE[k % 8]
        g.add(E.chip(l_, c_, size=size).move_to([x0 + dx * k, y0 + dy * k, 0]))
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 27
    TITLE = "Reported Speech"
    SUBTITLE = "Grammar · direct to indirect, step by step"
    SECTIONS = ["The five steps", "One step back in time", "Pronouns, time and place", "Questions, commands, exclamations", "When the tense stays", "Say, tell, and worked items"]
    NEXT = "Unit 28 · Conditional Sentences"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        d = T("Sita said, \"I am busy today.\"", size=40, color=th.INK).move_to([0, 1.0, 0])
        r = T("Sita said that she was busy that day.", size=40, color=th.MINT).move_to([0, -0.6, 0])
        with self.say("Sita said, I am busy today. Those are her exact words, in direct speech. Now report them, as a reporter would."):
            self.play(FadeIn(d))
        nt = para("Four things change — the link word, the pronoun, the tense, the time words — and the transformation becomes mechanical.", width=11, size=28, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("Sita said that she was busy that day. Count the changes: a link word, that; the pronoun, I to she; the tense, am to was; and the time word, today to that day. Do them in the same order every time, and reported speech becomes almost automatic."):
            self.play(TransformMatchingShapes(d.copy(), r), run_time=2)
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "talk", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(d, r, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 27: reported speech."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. The five steps. One step back in time. Pronouns, time and place. Questions, commands and exclamations. When the tense stays. And say, tell, with worked items.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Five steps, in this order, every time")
        steps = VGroup(*[VGroup(T(f"{k + 1}", size=34, color=c_, weight="BOLD"), T(t_, size=28, color=th.INK)).arrange(RIGHT, buff=0.4) for k, (t_, c_) in enumerate([
            ("remove the inverted commas, the comma and the ? or !", th.MUTED), ("choose the reporting verb and link word: that, if, whether, a wh-word, to + verb", th.SKY),
            ("change the pronouns to fit the new speaker and listener", th.MINT), ("move the tense one step back (with exceptions)", th.AMBER), ("change words of time and place: now → then, here → there", th.PINK)])]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.2, 0])
        steps.scale_to_fit_width(min(steps.width, 12.4))
        with self.say("The standard procedure has five steps. One: remove the inverted commas, the comma after the reporting verb, and any question or exclamation mark. Two: choose the reporting verb and the link word: that for a statement, if or whether for a yes no question, a wh word, or to plus a verb for a command. Three: change the pronouns to fit the new speaker and listener. Four: move the tense one step back, with a few exceptions. Five: change the words of time and place."):
            self.play(FadeIn(h))
            for s_ in steps:
                self.play(FadeIn(s_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(2.0)
        self.play(FadeOut(VGroup(h, steps)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "One step back in time")
        pairs = [("write", "wrote"), ("am writing", "was writing"), ("have written", "had written"), ("wrote", "had written"), ("was writing", "had been writing"), ("will write", "would write")]
        rows = VGroup(*[VGroup(T(f"\"I {a_}\"", size=30, color=th.SKY), Arrow(LEFT * 0.5, RIGHT * 0.5, color=th.MUTED, buff=0), T(f"he said he {b_}", size=30, color=th.MINT)).arrange(RIGHT, buff=0.4) for a_, b_ in pairs]).arrange(DOWN, buff=0.28).move_to([0, -0.1, 0])
        for r_ in rows:
            r_[0].align_to(np.array([-5.6, 0, 0]), LEFT)
            r_[1].move_to([-0.6, r_.get_y(), 0])
            r_[2].align_to(np.array([0.2, 0, 0]), LEFT)
        nt = T("past perfect stays past perfect — there is no further step back", size=24, color=th.AMBER).move_to([0, -2.9, 0])
        with self.say("After a past reporting verb, every tense moves one step back. I write becomes he said he wrote. I am writing: he was writing. I have written: he had written. I wrote: he had written. I was writing: he had been writing. I will write: he would write. And the past perfect stays as it is, because there is no further step back."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_[0]), GrowArrow(r_[1]), FadeIn(r_[2]), run_time=0.5)
                self.hold(1.2)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(rows, nt)))
        rows = [["direct", "reported", "example"], ["can", "could", "\"I can swim.\" → She said she could swim."], ["may", "might", "\"You may go.\" → He said I might go."], ["must (obligation)", "had to", "\"You must leave.\" → He said I had to leave."], ["will / shall", "would", "\"We shall win.\" → They said they would win."], ["shall (offer)", "should", "\"Shall I carry it?\" → He asked whether he should."], ["would, could, might, should, ought to", "no change", "\"You should rest.\" → She said I should rest."]]
        tb = E.table(rows, [4.2, 2.2, 6.6], row_h=0.62, size=22, colors=[th.SKY, th.MINT, th.INK]).move_to([0, 0.0, 0])
        with self.say("Modals shift too. Can becomes could; may becomes might; must, meaning obligation, becomes had to; will and shall become would; and shall in an offer becomes should. But would, could, might, should and ought to have no further past, so they never change.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h, tb)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Pronouns follow the people")
        d = T("He said to me, \"I have finished your work.\"", size=34, color=th.INK).move_to([0, 1.5, 0])
        r = T("He told me that he had finished my work.", size=34, color=th.MINT).move_to([0, 0.1, 0])
        rule = E.bullets(["first person (I, we, my) → follows the subject of the reporting verb", "second person (you, your) → follows its object", "third person (he, she, they) → no change"], width=11, size=26).move_to([0, -1.9, 0])
        with self.say("Pronouns follow the people. He said to me, I have finished your work. I is the speaker, the subject of said, so I becomes he. Your means the listener, the object, me, so your becomes my. He told me that he had finished my work. The rule: first person follows the subject of the reporting verb, second person follows its object, and third person does not change."):
            self.play(FadeIn(h), FadeIn(d))
            self.play(TransformMatchingShapes(d.copy(), r), run_time=2)
            E.reveal_list(self, rule, 6.0)
        self.play(FadeOut(VGroup(d, r, rule)))
        h2 = E.head(self, "Time and place move away")
        pairs = [("now", "then"), ("today", "that day"), ("tonight", "that night"), ("yesterday", "the previous day"), ("tomorrow", "the next day"), ("last week", "the previous week"), ("next week", "the following week"), ("ago", "before"), ("here", "there"), ("this / these", "that / those")]
        chips = VGroup(*[VGroup(T(a_, size=26, color=th.SKY), T("→", size=26, color=th.MUTED), T(b_, size=26, color=th.MINT)).arrange(RIGHT, buff=0.2) for a_, b_ in pairs]).arrange_in_grid(rows=5, cols=2, buff=(1.2, 0.3), col_alignments="ll").move_to([0, 0.2, 0])
        ex = T("\"I met him here yesterday,\" she said. → She said that she had met him there the previous day.", size=24, color=th.AMBER).move_to([0, -2.6, 0])
        ex.scale_to_fit_width(min(ex.width, 12.4))
        with self.say("Words of time and place move away from the speaker's moment. Now becomes then; today, that day; tonight, that night; yesterday, the previous day; tomorrow, the next day; last week, the previous week; ago, before; here, there; this and these, that and those. I met him here yesterday, she said, becomes: she said that she had met him there the previous day."):
            self.play(ReplacementTransform(h, h2), LaggedStart(*[FadeIn(c_) for c_ in chips], lag_ratio=0.15), run_time=3)
            self.play(FadeIn(ex))
        self.play(FadeOut(VGroup(h2, chips, ex)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Questions: ask + statement order, no do")
        rows = [["direct", "reported"], ["He said, \"Are you coming?\"", "He asked whether / if I was coming."], ["He said, \"Do you like tea?\"", "He asked whether I liked tea."], ["He said, \"Where did you go?\"", "He asked where I had gone."], ["She said, \"What is your name?\"", "She asked what my name was."], ["\"Who broke the glass?\" he asked.", "He asked who had broken the glass."]]
        tb = E.table(rows, [5.6, 7.0], row_h=0.66, size=24, colors=[th.SKY, th.MINT]).move_to([0, 0.4, 0])
        nt = T("no question mark at the end — and never \"that\" before if or a wh-word", size=24, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Questions. Three things happen: the reporting verb becomes ask; the question goes back to statement order; and do, does and did disappear. Are you coming becomes he asked whether I was coming. Do you like tea: he asked whether I liked tea. Where did you go: he asked where I had gone. What is your name: she asked what my name was. A reported question has no question mark, and never put that before if or a wh word.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h2 = E.head(self, "Commands, requests, advice: verb + object + to")
        rows = [["direct", "verb", "reported"], ["\"Stand up,\" the teacher said to us.", "ordered", "The teacher ordered us to stand up."], ["\"Please lend me your pen.\"", "requested", "He requested me to lend him my pen."], ["\"You should see a doctor.\"", "advised", "She advised me to see a doctor."],
                ["\"Don't touch the wires.\"", "warned", "He warned me not to touch the wires."], ["\"Let's go for a walk.\"", "suggested", "She suggested going for a walk."]]
        tb = E.table(rows, [4.8, 2.2, 5.8], row_h=0.64, size=22, colors=[th.SKY, th.AMBER, th.MINT]).move_to([0, 0.3, 0])
        with self.say("Commands, requests and advice turn the imperative into an infinitive: reporting verb, object, to, base verb. Stand up: the teacher ordered us to stand up. Please lend me your pen: he requested me to lend him my pen. You should see a doctor: she advised me to see a doctor. A negative takes not to: he warned me not to touch the wires. And let's becomes suggested: she suggested going for a walk.") as v:
            self.play(ReplacementTransform(h, h2))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h3 = E.head(self, "Exclamations, wishes and fixed expressions")
        rows = [["direct", "reported"], ["\"What a beautiful garden!\"", "He exclaimed that it was a very beautiful garden."], ["\"Alas! I have lost my purse.\"", "She exclaimed with sorrow that she had lost her purse."], ["\"May you live long!\"", "He prayed that I might live long."], ["\"Good morning,\" she said to him.", "She greeted him."], ["\"Thank you.\"  ·  \"Yes.\"", "He thanked her.  ·  He replied in the affirmative."]]
        tb = E.table(rows, [5.0, 7.6], row_h=0.66, size=22, colors=[th.SKY, th.MINT]).move_to([0, 0.3, 0])
        with self.say("Exclamations become exclaimed that, with the feeling named: she exclaimed with sorrow that she had lost her purse. A wish, may you live long, becomes he prayed that I might live long. And fixed expressions simply become verbs: good morning, she greeted him; thank you, he thanked her; yes, he replied in the affirmative.") as v:
            self.play(ReplacementTransform(h2, h3))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h3, tb)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "When the tense does not shift")
        cards = VGroup(
            E.card("reporting verb in present / future", "He says that he is busy. She has told me that she will come.", th.SKY, w=6.1, h=2.2, size=24),
            E.card("universal truths, permanent facts", "The teacher said that the earth revolves round the sun.", th.MINT, w=6.1, h=2.2, size=24),
            E.card("unreal: 2nd/3rd conditionals, wish", "He said that if he were rich, he would travel.", th.AMBER, w=6.1, h=2.2, size=24),
            E.card("a past fixed to a stated time", "He said that he was born in 2005.", th.PINK, w=6.1, h=2.2, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("Sometimes the tense does not shift. When the reporting verb is in the present or future: he says that he is busy. With universal truths and permanent facts: the teacher said that the earth revolves round the sun. With unreal clauses, second and third conditionals and wishes, which are already unreal: he said that if he were rich, he would travel. And with a past tied to a stated past time: he said he was born in two thousand and five."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(VGroup(h, cards)))
        h = E.head(self, "Six mistakes that cost marks")
        pairs = [("He said me that he was ill.", "He told me that he was ill."), ("He told to me the truth.", "He told me the truth."), ("He asked me that where I was going.", "He asked me where I was going."), ("He asked where was I going.", "He asked where I was going."),
                 ("He asked if I am free?", "He asked if I was free."), ("He said he will come the next day.", "He said he would come the next day.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("Six mistakes that cost marks. He said me: say needs to, so said to me, or told me. He told to me: tell takes no to. He asked me that where: never that before a wh word. He asked where was I going: statement order, where I was going. He asked if I am free, with a question mark: was, and a full stop. And he said he will come: after a past reporting verb, would."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.2)
        self.play(FadeOut(VGroup(h, grid)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["verb", "pattern", "example"], ["say", "say (to somebody) that …", "He said to me that he was late."], ["tell", "tell somebody that … (no \"to\")", "He told me that he was late."], ["speak", "speak to somebody; a language", "I spoke to the principal."], ["ask", "ask somebody about / for …", "She asked for water."]]
        tb = E.table(rows, [2.0, 5.0, 5.6], row_h=0.7, size=24, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 1.0, 0])
        with self.say("Say, tell, speak and ask. Say takes to before a listener: he said to me. Tell takes the listener directly, with no to: he told me. Speak to somebody, or speak a language. And ask somebody about or for something.") as v:
            E.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(tb))
        h = E.head(self, "Worked item: five changes in one sentence")
        d = para("Ramesh said to me, \"I bought this book here yesterday and I am reading it now.\"", width=11.4, size=28, color=th.INK).move_to([0, 1.9, 0])
        st = E.bullets(["said to me → told me … that", "I → he", "bought → had bought; am reading → was reading", "this → that; here → there; yesterday → the previous day; now → then"], width=11.2, size=26).move_to([0, -0.2, 0])
        r = para("Ramesh told me that he had bought that book there the previous day and that he was reading it then.", width=11.4, size=28, color=th.MINT).move_to([0, -2.5, 0])
        with self.say("A worked item. Ramesh said to me, I bought this book here yesterday and I am reading it now. There is a listener, so told me, that. I refers to Ramesh: he. Bought becomes had bought; am reading becomes was reading. This becomes that, here becomes there, yesterday the previous day, and now then. Ramesh told me that he had bought that book there the previous day, and that he was reading it then."):
            self.play(FadeIn(h), FadeIn(d))
            E.reveal_list(self, st, 9.0)
            self.play(FadeIn(r))
        self.play(FadeOut(VGroup(h, d, st, r)))
        self.quiz("\"Where are you going?\" she said to me. → She asked me ____ .",
                  ["where was I going", "where I was going", "that where I was going", "where am I going?"], 1,
                  "Pause and think.",
                  "Ask + wh-word + statement order + backshift, and no question mark.")
        self.quiz("\"Don't touch the wires,\" he said. → He warned me ____ the wires.",
                  ["don't touch", "not to touch", "to not touched", "not touch"], 1,
                  "One more.",
                  "A negative command: verb + object + not to + base verb.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Five steps: marks off, verb + link word, pronouns, tense back, time and place.",
            "Tense: present → past, past → past perfect, will → would, can → could.",
            "Questions: ask + if/whether or wh-word + statement order, no do, no ?",
            "Commands: told / ordered / advised + object + (not) to + verb.",
            "No backshift: present reporting verb, universal truths, unreal clauses.",
        ], "Quick recap. The five steps. One step back in time. Pronouns that follow the people, and time words that move away. Questions, commands and exclamations. And when the tense stays.")
        self.outro("That was reported speech. Next: conditional sentences. See you there.")
