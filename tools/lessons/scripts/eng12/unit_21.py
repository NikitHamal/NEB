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
    UNIT = 21
    TITLE = "Question Tags and Questions"
    SUBTITLE = "Grammar · tags, inversion, embedded questions"
    SECTIONS = ["Three decisions make every tag", "The irregular tags", "The traps", "Yes/no and wh-questions", "Indirect questions", "Worked items"]
    NEXT = "Unit 22 · Modal Verbs"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        s = E.sentence("He is a teacher, isn't it?", size=40).move_to([0, 0.8, 0])
        tag = VGroup(*s.words[4:])
        cross = E.strike(tag)
        fix = T("isn't he?", size=40, color=th.MINT, weight="BOLD").next_to(tag, DOWN, buff=0.45)
        with self.say("Here is the most common mistake in Nepali English. He is a teacher, isn't it? The examiner marks it wrong every single time."):
            self.play(FadeIn(s))
            self.play(tag.animate.set_color(th.CORAL), Create(cross))
        nt = para("A question tag is not written from feeling. It is calculated — in three steps.", width=11, size=30, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("The right tag is isn't he. And the good news is that a tag is never a matter of feeling. It is calculated, in three steps, every time. Learn the steps and the question tag item in your exam becomes a free mark."):
            self.play(FadeIn(fix, shift=UP * 0.2))
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "wink", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(s, cross, fix, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 21: question tags and questions."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. The three decisions behind every tag. The irregular tags. The traps. Yes no and wh questions. Indirect questions. And worked items in exam style.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Operator + polarity + pronoun")
        s = E.sentence("She has finished the work,", size=38).move_to([-2.2, 1.6, 0])
        slot = T("_____ ?", size=38, color=th.MUTED).next_to(s, RIGHT, buff=0.3)
        steps = VGroup(*[VGroup(T(n_, size=30, color=c_, weight="BOLD"), T(d_, size=24, color=th.BODY)).arrange(RIGHT, buff=0.3) for n_, d_, c_ in [
            ("1  operator", "repeat the auxiliary or modal; if none, use do / does / did", th.SKY),
            ("2  polarity", "positive statement → negative tag, and back", th.CORAL),
            ("3  pronoun", "replace the subject with its pronoun", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -1.2, 0])
        with self.say("Every tag needs three decisions. Take: she has finished the work. Decision one, the operator. Find the auxiliary or the modal in the statement and repeat it. Here it is has."):
            self.play(FadeIn(h), FadeIn(s), FadeIn(slot))
            m1 = E.mark(s.words[1], th.SKY)
            self.play(FadeIn(steps[0]), Create(m1))
        op = T("has", size=38, color=th.SKY, weight="BOLD").move_to(slot).align_to(slot, LEFT)
        with self.say("Decision two, the polarity. The statement is positive, so the tag must be negative: has becomes hasn't. A negative statement takes a positive tag."):
            self.play(ReplacementTransform(slot, op))
            self.play(FadeIn(steps[1]))
            neg = T("hasn't", size=38, color=th.CORAL, weight="BOLD").move_to(op).align_to(op, LEFT)
            self.play(Transform(op, neg))
        pr = T("she?", size=38, color=th.MINT, weight="BOLD").next_to(op, RIGHT, buff=0.2)
        with self.say("Decision three, the pronoun. Replace the subject with its personal pronoun: she. Operator, polarity, pronoun. She has finished the work, hasn't she?"):
            m2 = E.mark(s.words[0], th.MINT)
            self.play(FadeIn(steps[2]), Create(m2))
            self.play(FadeIn(pr, shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(s, op, pr, steps, m1, m2)))
        rows = [["statement", "operator", "tag"], ["She is waiting outside.", "is", "isn't she?"], ["They were not invited.", "were (negative)", "were they?"], ["We can meet on Friday.", "can", "can't we?"],
                ["The bus left early.", "none → did", "didn't it?"], ["Sita teaches at Amar Campus.", "none → does", "doesn't she?"], ["She didn't come.", "did (negative)", "did she?"]]
        tb = E.table(rows, [5.4, 3.6, 3.0], row_h=0.6, size=26, colors=[th.INK, th.SKY, th.MINT]).move_to([0, 0.15, 0])
        nt = para("A negative tag is always contracted: isn't he? — never \"is not he?\". (Formal: \"am I not?\")", width=11, size=24, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("More examples. She is waiting outside: isn't she? They were not invited: the statement is negative, so were they? The bus left early has no auxiliary at all, so we supply did: didn't it? Sita teaches at Amar Campus: doesn't she? And a negative tag is always contracted: isn't he, never is not he.") as v:
            E.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Irregular tags: special subjects and words")
        rows = [["statement", "tag", "why"], ["I am your monitor,", "aren't I?", "\"amn't\" doesn't exist"], ["Let's plant a tree,", "shall we?", "a suggestion"], ["Open the window,", "will you?", "a command made polite"], ["Don't be late,", "will you?", "negative imperative"],
                ["There is a mistake,", "isn't there?", "\"there\" is the subject"], ["Nobody phoned,", "did they?", "nobody = negative; they"], ["Nothing is impossible,", "is it?", "nothing = negative; it"], ["Everyone has left,", "haven't they?", "everyone → they"]]
        tb = E.table(rows, [4.8, 3.0, 4.6], row_h=0.56, size=24, colors=[th.INK, th.MINT, th.MUTED]).move_to([0, -0.3, 0])
        with self.say("Now the irregular tags: learn this table and nothing can surprise you. I am your monitor: aren't I, because amn't does not exist. Let's plant a tree: shall we. An order, open the window: will you, which turns the command into a polite request; and don't be late also takes will you. There is a mistake: isn't there, because there is the grammatical subject. Nobody phoned: nobody is already negative, so the tag is positive, did they. Nothing is impossible: is it. And everyone has left: haven't they.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h2 = E.head(self, "Irregular tags: special verbs and clauses")
        rows = [["statement", "tag"], ["Those are his books,", "aren't they?"], ["We have to pay today,", "don't we?"], ["You'd better rest,", "hadn't you?   ('d = had)"], ["You'd rather walk,", "wouldn't you?   ('d = would)"], ["He used to smoke,", "didn't he?"],
                ["He must be ill,", "isn't he?   (deduction: the verb is be)"], ["She hardly ever complains,", "does she?"], ["I think he is honest,", "isn't he?   (the inside clause)"], ["I don't think she will come,", "will she?"]]
        tb = E.table(rows, [5.6, 6.8], row_h=0.52, size=24, colors=[th.INK, th.MINT]).move_to([0, -0.35, 0])
        with self.say("And the verbs. Those are his books: aren't they. We have to pay today: have to behaves like a full verb, so don't we. You had better rest: hadn't you; you would rather walk: wouldn't you. He used to smoke: didn't he. He must be ill is a deduction whose real verb is be, so isn't he. She hardly ever complains: hardly makes it negative, so does she. With I think, the tag follows the inside clause: I think he is honest, isn't he. And I don't think she will come takes a positive tag, will she.") as v:
            self.play(ReplacementTransform(h, h2))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        neg = VGroup(*[E.chip(w_, th.CORAL, size=26) for w_ in ["never", "hardly", "scarcely", "barely", "seldom", "rarely", "few", "little", "no", "none", "nobody", "nothing", "neither", "nowhere"]]).arrange_in_grid(rows=2, buff=(0.2, 0.25)).move_to([0, 0.6, 0])
        pos = para("These make a statement negative, so the tag is positive. But \"a few\" and \"a little\" are positive: He has a little money, hasn't he?", width=11, size=26, color=th.INK).move_to([0, -1.9, 0])
        with self.say("Memorise the words that make a statement negative without any not: never, hardly, scarcely, barely, seldom, rarely, few, little, no, none, nobody, nothing, neither, nowhere. They take a positive tag. But careful: a few and a little are positive. He has a little money, hasn't he?"):
            self.play(LaggedStart(*[FadeIn(n_, scale=0.8) for n_ in neg], lag_ratio=0.08))
            self.play(FadeIn(pos))
        self.play(FadeOut(VGroup(h2, neg, pos)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Four traps that cost the mark")
        traps = VGroup(
            E.wrong_right("He is coming tomorrow, isn't it?", "He is coming tomorrow, isn't he?", size=28, rule="never use \"isn't it\" for everything"),
            E.wrong_right("She can't swim, can't she?", "She can't swim, can she?", size=28, rule="never two negatives"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 0.3, 0])
        with self.say("The traps. First, isn't it as an all purpose tag: he is coming tomorrow, isn't it, is wrong. The pronoun must match the subject: isn't he. Second, two negatives: she can't swim, can't she, is wrong. A negative statement takes a positive tag: can she."):
            self.play(FadeIn(h))
            for t_ in traps:
                self.play(FadeIn(t_.wrong))
                self.play(Create(t_.cross), FadeIn(t_.right, shift=UP * 0.15), FadeIn(t_[2]))
        self.play(FadeOut(traps))
        a = E.card("'s = is or has", "He's gone, hasn't he?  ·  He's a pilot, isn't he?", th.SKY, w=5.8, h=2.2, size=26).move_to([-3.2, 1.0, 0])
        b = E.card("'d = had or would", "You'd better go, hadn't you?  ·  You'd like tea, wouldn't you?", th.AMBER, w=5.8, h=2.2, size=26).move_to([3.2, 1.0, 0])
        c = E.card("tag the subject", "Sita's brother works in Qatar, doesn't he? — the subject is \"brother\", not Sita", th.PINK, w=11.8, h=1.8, size=26).move_to([0, -1.4, 0])
        with self.say("Third, the contractions. Apostrophe s can be is or has: he's gone, hasn't he; but he's a pilot, isn't he. Apostrophe d can be had or would: you'd better go, hadn't you; you'd like tea, wouldn't you. Fourth, tag the subject, not the nearest noun: Sita's brother works in Qatar, doesn't he, because the subject is the brother."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(c))
        self.play(FadeOut(VGroup(a, b, c)))
        f = VGroup(T("It's hot today, isn't it?", size=32, color=th.INK), Arrow(LEFT * 0.6 + UP * 0.3, RIGHT * 0.6 + DOWN * 0.3, color=th.MINT, buff=0), T("falling: asking you to agree", size=24, color=th.MINT)).arrange(RIGHT, buff=0.35).move_to([0, 1.0, 0])
        r = VGroup(T("You locked the gate, didn't you?", size=32, color=th.INK), Arrow(LEFT * 0.6 + DOWN * 0.3, RIGHT * 0.6 + UP * 0.3, color=th.AMBER, buff=0), T("rising: a real question", size=24, color=th.AMBER)).arrange(RIGHT, buff=0.35).move_to([0, -0.8, 0])
        VGroup(f, r).scale_to_fit_width(min(VGroup(f, r).width, 12.4))
        with self.say("Finally, tone of voice carries meaning that print cannot. Said with a falling tone, a tag asks you to agree: it's hot today, isn't it. Said with a rising tone, it is a genuine question: you locked the gate, didn't you?"):
            self.play(FadeIn(f))
            self.play(FadeIn(r))
        self.play(FadeOut(VGroup(h, f, r)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Yes/no questions: the operator jumps to the front")
        a = E.sentence("She is in Grade 12.", size=40).move_to([0, 1.4, 0])
        a2 = E.sentence("Is she in Grade 12?", size=40, color=th.MINT).move_to([0, 1.4, 0])
        b = E.sentence("He works in Doha.", size=40).move_to([0, -0.6, 0])
        b2 = E.sentence("Does he work in Doha?", size=40, color=th.MINT).move_to([0, -0.6, 0])
        nt = para("No auxiliary? Supply do / does / did — and the main verb goes back to its base form.", width=11, size=26, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("A yes no question puts the operator in front of the subject. She is in Grade twelve becomes: is she in Grade twelve? If there is no auxiliary, supply do, does or did, and the main verb goes back to its base form: he works in Doha becomes does he work in Doha, not does he works."):
            self.play(FadeIn(h), FadeIn(a))
            ma = E.mark(a.words[1], th.SKY)
            self.play(Create(ma))
            self.play(TransformMatchingShapes(a, a2), FadeOut(ma), run_time=1.5)
            self.play(FadeIn(b))
            self.play(TransformMatchingShapes(b, b2), run_time=1.5)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(a2, b2, nt)))
        h2 = E.head(self, "Wh-questions: wh-word + operator + subject + verb")
        form = VGroup(*[E.chip(t_, c_, size=28) for t_, c_ in [("wh-word", th.AMBER), ("operator", th.SKY), ("subject", th.MINT), ("main verb", th.PINK), ("rest ?", th.MUTED)]]).arrange(RIGHT, buff=0.2).move_to([0, 1.6, 0])
        ex = VGroup(*[T(t_, size=30, color=th.INK) for t_ in ["Where are you going?", "Why didn't you inform me?", "How long have you waited?"]]).arrange(DOWN, buff=0.3).move_to([0, -0.2, 0])
        qw = T("who · whom · whose · what · which · when · where · why · how · how many · how much · how long · how often", size=24, color=th.MUTED).move_to([0, -2.4, 0])
        qw.scale_to_fit_width(min(qw.width, 12.4))
        with self.say("A wh question puts the question word first, then inverts exactly as before: wh word, operator, subject, main verb, the rest. Where are you going? Why didn't you inform me? How long have you waited?"):
            self.play(ReplacementTransform(h, h2), LaggedStart(*[FadeIn(f_) for f_ in form], lag_ratio=0.2))
            self.play(LaggedStart(*[FadeIn(e_) for e_ in ex], lag_ratio=0.4))
            self.play(FadeIn(qw))
        self.play(FadeOut(VGroup(form, ex, qw)))
        a = E.card("subject question: no do", "Someone broke the window. → Who broke the window?   (not \"Who did break\")", th.MINT, w=11.8, h=2.0, size=26).move_to([0, 1.2, 0])
        b = E.card("object question: invert", "You met someone. → Whom did you meet? / Who did you meet?", th.SKY, w=11.8, h=2.0, size=26).move_to([0, -1.2, 0])
        with self.say("One important exception. When the question word is itself the subject, there is no inversion and no do: someone broke the window becomes who broke the window, not who did break. But when it replaces the object, you invert: you met someone becomes whom did you meet, or less formally, who did you meet?"):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(h2, a, b)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Inside another sentence, the inversion is undone")
        d = E.sentence("Where is the bus park?", size=38, color=th.INK).move_to([0, 1.4, 0])
        e = E.sentence("Could you tell me where the bus park is?", size=38, color=th.MINT).move_to([0, -0.2, 0])
        with self.say("When a question is put inside another sentence, after could you tell me, do you know, or I wonder, the inversion is undone: the embedded part goes back to statement order. Where is the bus park? becomes: could you tell me where the bus park is?"):
            self.play(FadeIn(h), FadeIn(d))
            self.play(TransformMatchingShapes(d.copy(), e), run_time=2)
            me = E.mark(e.words[-1], th.AMBER)
            self.play(Create(me))
        self.play(FadeOut(VGroup(d, e, me)))
        rows = [["direct question", "embedded"], ["What time does the bank open?", "Do you know what time the bank opens?"], ["Why did she resign?", "I wonder why she resigned."], ["Has the result come out?", "Do you know if the result has come out?"], ["Is this seat free?", "May I ask if this seat is free?"]]
        tb = E.table(rows, [5.2, 7.2], row_h=0.7, size=24, colors=[th.INK, th.MINT]).move_to([0, 0.5, 0])
        nt = para("do / does / did disappear and the verb takes back its tense. A yes/no question needs \"if\" or \"whether\".", width=11.4, size=24, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("Notice that do, does and did disappear, and the verb takes back its tense: what time does the bank open becomes what time the bank opens; why did she resign becomes why she resigned. A yes no question needs if or whether as the link: do you know whether the result has come out?") as v:
            E.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Worked item 1: a hidden negative")
        s = T("Your brother seldom writes to you, ____ ?", size=34, color=th.INK).move_to([0, 1.8, 0])
        steps = E.bullets(["operator: \"writes\" has no auxiliary; he → does", "polarity: \"seldom\" means almost never — the statement is negative, so the tag is positive", "pronoun: your brother → he"], width=11.2, size=26).move_to([0, -0.1, 0])
        ans = T("Your brother seldom writes to you, does he?", size=34, color=th.MINT, weight="BOLD").move_to([0, -2.3, 0])
        with self.say("Exam style. Your brother seldom writes to you, blank. The operator: writes has no auxiliary, and the subject is third person singular, so does. The polarity: there is no not, but seldom means almost never, so the statement is negative and the tag is positive. The pronoun: he. Does he. The student who ignores seldom writes doesn't he, and loses the mark."):
            self.play(FadeIn(h), FadeIn(s))
            E.reveal_list(self, steps, 9.0)
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(s, steps, ans)))
        h2 = E.head(self, "Worked item 2: one statement, three questions")
        s = T("Bishnu bought a second-hand laptop in Bhotahity last week.", size=28, color=th.INK).move_to([0, 2.0, 0])
        qs = VGroup(*[VGroup(T(a_, size=24, color=th.MUTED), T(b_, size=28, color=c_)).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for a_, b_, c_ in [
            ("(a) ask about the buyer — a subject question: no did", "Who bought a second-hand laptop in Bhotahity last week?", th.MINT),
            ("(b) ask about the thing — an object question: invert, did + base form", "What did Bishnu buy in Bhotahity last week?", th.SKY),
            ("(c) embed (b) after \"Could you tell me\" — no inversion, past tense back", "Could you tell me what Bishnu bought in Bhotahity last week?", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.5, 0])
        qs.scale_to_fit_width(min(qs.width, 12.4))
        with self.say("Last item. Bishnu bought a second hand laptop in Bhotahity last week. Ask about the person who bought it: the question word replaces the subject, so no inversion and no did: who bought a second hand laptop? Ask about the thing he bought: an object question, so invert: what did Bishnu buy? Now embed that after could you tell me: the inversion and the did disappear, and the past tense comes back: could you tell me what Bishnu bought?"):
            self.play(ReplacementTransform(h, h2), FadeIn(s))
            for q_ in qs:
                self.play(FadeIn(q_, shift=UP * 0.15))
                self.hold(3.0)
        self.play(FadeOut(VGroup(h2, s, qs)))
        self.quiz("Choose the correct tag: Nobody helped him, ____?",
                  ["didn't they", "did they", "did he", "didn't he"], 1,
                  "Pause and think.",
                  "Nobody is negative, so the tag is positive; nobody takes \"they\": did they?")
        self.quiz("Which embedded question is correct?",
                  ["Tell me where is the library.", "Tell me where the library is.", "Tell me where does the library is.", "Tell me is where the library."], 1,
                  "One more.",
                  "Inside another sentence the question goes back to statement order: where the library is.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Tag = operator + opposite polarity + pronoun; no auxiliary → do / does / did.",
            "Irregulars: aren't I, shall we, will you, isn't there, did they, is it.",
            "Hidden negatives (never, hardly, seldom, nobody…) take a positive tag.",
            "Questions invert; subject questions take no do; base form after do.",
            "Embedded questions undo the inversion: where the bus park is.",
        ], "Quick recap. Operator, polarity, pronoun. The irregular tags. Hidden negatives. Inversion, and subject questions without do. And embedded questions in statement order.")
        self.outro("That was question tags and questions. Next: modal verbs. See you there.")
