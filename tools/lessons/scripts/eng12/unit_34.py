import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def mock_page(paras=(3, 4, 3, 4, 2), w=4.6, gap=0.16, pgap=0.34):
    """A page of grey text lines, paragraph by paragraph; .first holds each paragraph's first line."""
    ps = VGroup()
    for n in paras:
        ps.add(VGroup(*[Line(ORIGIN, RIGHT * (w if k < n - 1 else w * 0.55), color=th.FAINT, stroke_width=4) for k in range(n)]).arrange(DOWN, aligned_edge=LEFT, buff=gap))
    ps.arrange(DOWN, aligned_edge=LEFT, buff=pgap)
    title = Line(ORIGIN, RIGHT * w * 0.45, color=th.MUTED, stroke_width=7).next_to(ps, UP, buff=0.35).align_to(ps, LEFT)
    box = RoundedRectangle(corner_radius=0.1, width=w + 0.6, height=ps.height + 1.1, stroke_color=th.FAINT, stroke_width=1.5, fill_color=th.PANEL, fill_opacity=1).move_to(VGroup(title, ps))
    g = VGroup(box, title, ps)
    g.ps, g.title, g.first = ps, title, VGroup(*[p_[0] for p_ in ps])
    return g


def node(text, color, w=3.6, h=0.9, size=24):
    b = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1)
    t = para(text, width=w - 0.3, size=size, color=th.INK)
    return VGroup(b, t.move_to(b))


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 34
    TITLE = "Unseen Reading Comprehension"
    SUBTITLE = "Reading · Question 1: the passage is the authority, not you"
    SECTIONS = ["What Question 1 asks", "Five steps, in this order", "Skimming and scanning", "True, False or Not Given", "Words in context, and inference", "A worked passage"]
    NEXT = "Unit 35 · Vocabulary, Sounds and Idioms"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        panel = RoundedRectangle(corner_radius=0.12, width=6.6, height=4.6, stroke_color=th.FAINT, stroke_width=1.5, fill_color=th.PANEL, fill_opacity=1).move_to([-3.2, 0.3, 0])
        body = para("A fog net does nothing clever. It is a rectangle of fine plastic mesh, stretched between two poles at right angles to the wind. Droplets that strike a thread stick, run together and slide down into a gutter.", width=5.9, size=24, color=th.BODY)
        last = para("There are no moving parts and nothing to switch on.", width=5.9, size=24, color=th.BODY)
        txt = VGroup(body, last).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(panel)
        st = E.card("True, False or Not Given?", "A fog net has to be turned on before it will collect water.", th.SKY, w=5.8, h=2.3, tsize=26, size=26).move_to([3.5, 1.2, 0])
        opts = VGroup(*[E.chip(t_, th.MUTED, size=24) for t_ in ["TRUE", "FALSE", "NOT GIVEN"]]).arrange(RIGHT, buff=0.3).next_to(st, DOWN, buff=0.4)
        hit = E.mark(last, color=th.AMBER)
        right = E.chip("FALSE", th.CORAL, size=24).move_to(opts[1])
        key = para("Every answer must be defensible by pointing at a line.", width=11.4, size=28, color=th.AMBER).move_to([0, -2.8, 0])
        s1 = "Question one prints the answers in front of you. Here is a paragraph about fog nets, and a statement: a fog net has to be turned on before it will collect water. True, false, or not given? You may know nothing about fog nets. You don't need to. You need the line: there are no moving parts and nothing to switch on. The passage says the opposite, so the answer is false."
        with self.say(s1) as v:
            self.play(FadeIn(panel), FadeIn(txt))
            v.until("and a statement")
            self.play(FadeIn(st, shift=UP * 0.2))
            v.until("True, false")
            self.play(FadeIn(opts))
            v.until("You need the line")
            self.play(Create(hit))
            v.until("so the answer")
            self.play(FadeIn(right), opts[1].animate.set_opacity(0))
        with self.say("That is the whole skill. The passage is the authority, not you, and every answer must be defensible by pointing at a line."):
            self.play(FadeIn(key))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(panel, txt, st, opts, hit, right, key)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 34: unseen reading comprehension."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. What question one asks. Five steps, in this order. Skimming and scanning. True, false or not given. Words in context, and inference. And a worked passage.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Fifteen marks, twenty-five minutes")
        rows = [["set", "task", "marks"], ["A", "True / False / Not Given, or fill the gaps", "5"], ["B", "short answers in your own words", "5"], ["C", "vocabulary in context", "5"]]
        tb = E.table(rows, [1.4, 8.2, 1.6], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 1.3, 0])
        segs = [(3, "skim", th.SKY), (3, "read the questions", th.SKY), (5, "re-read and mark", th.AMBER), (11, "write", th.AMBER), (3, "check", th.MINT)]
        bar, x = VGroup(), -6.0
        for m_, lab, c_ in segs:
            w = 12.0 * m_ / 25
            r_ = Rectangle(width=w - 0.05, height=0.6, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to([x + w / 2, -1.2, 0])
            n_ = T(str(m_), size=24, color=th.BG, weight="BOLD").move_to(r_)
            l_ = para(lab, width=max(1.3, w - 0.1), size=22, color=c_)
            l_.next_to(r_, DOWN, buff=0.15)
            bar.add(VGroup(r_, n_, l_))
            x += w
        mins = T("minutes", size=22, color=th.MUTED).next_to(bar, UP, buff=0.2).align_to(bar, LEFT)
        with self.say("An unseen passage of three hundred and fifty to four hundred and fifty words, and three sets of questions, five marks each. Set A: true, false or not given, or filling gaps from the text. Set B: short answers in your own words. Set C: vocabulary in context. Fifteen marks, a fifth of the written paper.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
        with self.say("You have about twenty five minutes, and they should be spent unequally: three to skim, three to read the questions, five to re-read and mark the passage, eleven to write, and three to check.") as v:
            self.play(FadeIn(mins))
            for b_, q_ in zip(bar, ["three to skim", "three to read", "five to re-read", "eleven", "and three to check"]):
                v.until(q_)
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[1]), FadeIn(b_[2]), run_time=0.5)
        self.play(FadeOut(VGroup(h, tb, bar, mins)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Five steps, in this order")
        steps = [("1  skim", "ninety seconds: the title, the first sentence of every paragraph, the last sentence", th.SKY), ("2  read the questions", "all of them, before the passage: underline the key word in each", th.PINK),
                 ("3  scan and mark", "hunt each key word; write the question number in the margin", th.AMBER), ("4  write", "question by question, from the marked lines, passage open", th.MINT), ("5  check", "against the checklist", th.MUTED)]
        rows = VGroup()
        for k, (a_, b_, c_) in enumerate(steps):
            chip = E.chip(a_, c_, size=24)
            d = para(b_, width=7.6, size=24, color=th.INK)
            rows.add(VGroup(chip, d))
        for k, r_ in enumerate(rows):
            r_[0].move_to([-6.2, 2.0 - 1.0 * k, 0], aligned_edge=LEFT)
            r_[1].move_to([-2.2, 2.0 - 1.0 * k, 0], aligned_edge=LEFT)
        with self.say("Five steps, in this order. Skim: ninety seconds for the title, the first sentence of every paragraph and the last sentence of the passage. Read the questions, all of them, before you read the passage properly, and underline the key word in each. Scan and mark: hunt each key word in the passage, and write the question number in the margin. Write, question by question, from the marked lines, with the passage open. And check.") as v:
            self.play(FadeIn(h))
            for r_, q_ in zip(rows, ["Skim:", "Read the questions", "Scan and mark", "Write,", "And check"]):
                v.until(q_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeOut(rows))
        h2 = E.head(self, "Why the questions come before the careful reading")
        cards = VGroup(*[E.card(a_, b_, c_, w=5.8, h=2.5, tsize=28, size=26) for a_, b_, c_ in [("passage first", "Read without questions, it has to be remembered in full.", th.CORAL), ("questions first", "Read with five key words in your head, it is a search.", th.MINT)]]).arrange(RIGHT, buff=0.5).move_to([0, 0.6, 0])
        nt = para("Searching is about four times faster than remembering: this one change of order is worth two or three marks.", width=11.4, size=26, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("Why the questions first? A passage read without questions has to be remembered in full. A passage read with five key words in your head is a search, and searching is about four times faster than remembering. This one change of order is worth two or three marks.") as v:
            self.play(ReplacementTransform(h, h2), FadeIn(cards[0], shift=UP * 0.2))
            v.until("A passage read with")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            v.until("and searching")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h2, cards, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Skimming and scanning are different skills")
        a = mock_page().scale(0.95).move_to([-3.4, 0.05, 0])
        b = mock_page().scale(0.95).move_to([3.4, 0.05, 0])
        target = b.ps[3][2]
        num = E.chip("1,240", th.AMBER, size=22).move_to(target.get_left() + RIGHT * 1.7)
        ca = VGroup(T("skimming", size=28, color=th.SKY, weight="BOLD"), T("the gist: title, first lines, last line", size=22, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(a, DOWN, buff=0.2)
        cb = VGroup(T("scanning", size=28, color=th.AMBER, weight="BOLD"), T("one fact: hunt its shape", size=22, color=th.BODY)).arrange(DOWN, buff=0.08).next_to(b, DOWN, buff=0.2)
        eye_a = Dot(radius=0.13, color=th.SKY)
        pts = [a.title.get_left()] + [p_ for f_ in a.first for p_ in (f_.get_left(), f_.get_right())] + [a.ps[-1][-1].get_left(), a.ps[-1][-1].get_right()]
        path_a = VMobject().set_points_as_corners(pts)
        zz = []
        for k in range(4):
            for ln in b.ps[k]:
                zz += [ln.get_left(), ln.get_right()] if len(zz) % 4 == 0 else [ln.get_right(), ln.get_left()]
        stop = next((i for i, p_ in enumerate(zz) if np.allclose(p_, target.get_left()) or np.allclose(p_, target.get_right())), len(zz) - 1)
        path_b = VMobject().set_points_as_corners(zz[:stop + 1] + [num.get_left() + LEFT * 0.2])
        eye_b = Dot(radius=0.13, color=th.AMBER)
        with self.say("Skimming and scanning are different skills. Skimming looks for the gist: the eye runs down the left edge, reading the title, the first line of each paragraph, and the last line. Scanning hunts one particular fact: you already know exactly what you want, and the eye zig-zags until it sees its shape.") as v:
            self.play(FadeIn(h), FadeIn(a), FadeIn(b), FadeIn(num))
            v.until("Skimming looks")
            self.play(FadeIn(ca), FadeIn(eye_a.move_to(pts[0])))
            self.play(MoveAlongPath(eye_a, path_a), run_time=4, rate_func=linear)
            v.until("Scanning hunts")
            self.play(FadeIn(cb), FadeIn(eye_b.move_to(zz[0])))
            self.play(MoveAlongPath(eye_b, path_b), run_time=4, rate_func=linear)
            self.play(Indicate(num, color=th.AMBER, scale_factor=1.3))
        self.play(FadeOut(VGroup(a, b, num, ca, cb, eye_a, eye_b)))
        h2 = E.head(self, "What to scan for, and in which order")
        tiers = VGroup(*[E.card(a_, b_, c_, w=11.6, h=1.35, tsize=26, size=24) for a_, b_, c_ in [("first: numbers, dates and Capital Letters", "the easiest shapes to find, so answer those questions first", th.MINT), ("next: technical words", "words the passage can't paraphrase: mesh, condensation, homestay", th.AMBER), ("last: questions built of common words", "the hardest to find: leave them till the end", th.CORAL)]]).arrange(DOWN, buff=0.3).move_to([0, -0.2, 0])
        with self.say("So what do you scan for first? Numbers, dates and capital letters: they are the easiest shapes to find, so the questions that contain them are the ones to answer first. Next, technical words the passage cannot paraphrase, like mesh, condensation, homestay. Hardest are questions built entirely of common words: leave those until last.") as v:
            self.play(ReplacementTransform(h, h2))
            for t_, q_ in zip(tiers, ["Numbers", "Next,", "Hardest"]):
                v.until(q_)
                self.play(FadeIn(t_, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(h2, tiers)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "True, False, Not Given: three different claims")
        defs = VGroup(*[E.card(a_, b_, c_, w=3.9, h=2.7, tsize=30, size=24) for a_, b_, c_ in [("TRUE", "The passage says it, in these words or in others.", th.MINT), ("FALSE", "The passage says the opposite: a line contradicts it.", th.CORAL), ("NOT GIVEN", "The passage is silent, however true it is in real life.", th.AMBER)]]).arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        nt = para("Only one of the three is about the world, and it is the wrong one to use.", width=11.4, size=26, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("This set separates a twelve from a fifteen, because the three answers are three different claims. True: the passage says it, in these words or in others. False: the passage says the opposite; there is a line you could point at that contradicts it. Not given: the passage neither says it nor contradicts it. It may well be true in real life. That is irrelevant.") as v:
            self.play(FadeIn(h))
            for d_, q_ in zip(defs, ["True:", "False:", "Not given:"]):
                v.until(q_)
                self.play(FadeIn(d_, shift=UP * 0.2), run_time=0.5)
            v.until("It may well be")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(defs, nt)))
        h2 = E.head(self, "The decision the question really asks")
        n0 = node("Find the line the statement is about", th.SKY, w=6.6).move_to([0, 2.0, 0])
        n1 = node("there is such a line", th.INK, w=3.6).move_to([-3.4, 0.45, 0])
        n2 = node("there is no such line anywhere", th.INK, w=4.6, h=1.1).move_to([3.4, 0.45, 0])
        n3 = node("it agrees", th.INK, w=2.4).move_to([-5.0, -1.05, 0])
        n4 = node("it says the opposite", th.INK, w=3.5).move_to([-1.75, -1.05, 0])
        r1 = E.chip("TRUE", th.MINT, size=26).move_to([-5.0, -2.55, 0])
        r2 = E.chip("FALSE", th.CORAL, size=26).move_to([-1.75, -2.55, 0])
        r3 = E.chip("NOT GIVEN", th.AMBER, size=26).move_to([3.4, -2.55, 0])
        ar = lambda a_, b_: Arrow(a_.get_bottom(), b_.get_top(), buff=0.08, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        a01, a02, a13, a14, a3r, a4r, a2r = ar(n0, n1), ar(n0, n2), ar(n1, n3), ar(n1, n4), ar(n3, r1), ar(n4, r2), ar(n2, r3)
        tree = VGroup(n0, n1, n2, n3, n4, r1, r2, r3, a01, a02, a13, a14, a3r, a4r, a2r)
        with self.say("The decision is always the same. Find the line in the passage that the statement is about. If there is such a line, ask whether it agrees, which is true, or says the opposite, which is false. If there is no such line anywhere, the answer is not given, however sure you are about the world. Most wrong answers come from knowing the statement is true in real life, and forgetting that the question is about the passage.") as v:
            self.play(ReplacementTransform(h, h2), FadeIn(n0))
            v.until("If there is such")
            self.play(GrowArrow(a01), FadeIn(n1))
            v.until("whether it agrees")
            self.play(GrowArrow(a13), FadeIn(n3), GrowArrow(a3r), FadeIn(r1))
            v.until("or says the opposite")
            self.play(GrowArrow(a14), FadeIn(n4), GrowArrow(a4r), FadeIn(r2))
            v.until("If there is no")
            self.play(GrowArrow(a02), FadeIn(n2), GrowArrow(a2r), FadeIn(r3))
        self.play(FadeOut(tree))
        h3 = E.head(self, "Four traps")
        traps = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.2, tsize=26, size=24) for a_, b_, c_ in [("all, every, never, only", "\"most cliff bees nest on north rock\" ≠ \"all cliff bees do\": FALSE", th.CORAL), ("a comparison never made", "nets praised, wells never mentioned: \"nets are cheaper than wells\" is NOT GIVEN", th.AMBER),
                                                                                              ("a cause smuggled in", "two things happened; unless the passage links them, \"one caused the other\" is NOT GIVEN", th.AMBER), ("your own knowledge", "true in the world, silent in the passage: still NOT GIVEN", th.AMBER)]]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to([0, -0.25, 0])
        with self.say("And four traps. All, every, never and only: a passage that says most cliff bees nest on north facing rock does not support all cliff bees do; that is false. A comparison you were never given: if the passage praises fog nets and never mentions wells, fog nets are cheaper than wells is not given. A cause smuggled in: two things happened, but unless the passage says one caused the other, the causal statement is not given. And your own knowledge: true in the world, silent in the passage, still not given.") as v:
            self.play(ReplacementTransform(h2, h3))
            for t_, q_ in zip(traps, ["All, every", "A comparison", "A cause", "And your own"]):
                v.until(q_)
                self.play(FadeIn(t_, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(h3, traps)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "A word in context: four moves")
        l1 = E.sentence("The committee was wary of large groups, and for two seasons", size=30)
        l2 = E.sentence("it capped the number of guests in any one house at four.", size=30)
        sent = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 1.9, 0])
        q = T("Find a word which means \"set an upper limit on\".", size=26, color=th.SKY).move_to([0, 0.7, 0])
        m_all = SurroundingRectangle(sent, color=th.FAINT, buff=0.12, corner_radius=0.08, stroke_width=2)
        m_cap = E.mark(l2.words[1], color=th.AMBER)
        pos = T("verb, past tense", size=22, color=th.AMBER).next_to(m_cap, DOWN, buff=0.12)
        m_sig = VGroup(E.mark(VGroup(*l1.words[3:7]), color=th.MINT), E.mark(VGroup(*l2.words[10:12]), color=th.MINT))
        steps = VGroup(*[T(t_, size=24, color=c_) for t_, c_ in [("1  read the whole sentence", th.INK), ("2  fix the part of speech", th.AMBER), ("3  look for a signal", th.MINT), ("4  replace and test", th.PINK)]]).arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.25), col_alignments="ll").move_to([0, -0.4, 0])
        test = T("… it set an upper limit on the number of guests … at four  ✓", size=26, color=th.PINK).move_to([0, -1.6, 0])
        ans = T("answer: capped   (not the cap you wear: that meaning is irrelevant)", size=24, color=th.MUTED).move_to([0, -2.6, 0])
        s1 = "Vocabulary in context is never answered from memory. Take this sentence, and the question: find a word which means set an upper limit on. First, read the whole sentence, not the phrase. Second, fix the part of speech: capped sits between it and the number, so it is a verb in the past tense, and the answer must be a verb. Third, look for a signal: at four says something was fixed at a maximum, and wary of large groups says why. Fourth, replace and test: it set an upper limit on the number of guests at four. It makes sense, so the answer is capped. The cap you wear on your head is irrelevant."
        with self.say(s1) as v:
            self.play(FadeIn(h), FadeIn(sent))
            v.until("and the question")
            self.play(FadeIn(q))
            v.until("First, read")
            self.play(Create(m_all), FadeIn(steps[0]))
            v.until("Second, fix")
            self.play(Create(m_cap), FadeIn(pos), FadeIn(steps[1]))
            v.until("Third, look")
            self.play(Create(m_sig), FadeIn(steps[2]))
            v.until("Fourth, replace")
            self.play(FadeIn(steps[3]), FadeIn(test, shift=UP * 0.15))
            v.until("so the answer")
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(sent, q, m_all, m_cap, pos, m_sig, steps, test, ans)))
        h2 = E.head(self, "An inference has a line behind it")
        facts = VGroup(*[E.card("the passage says", t_, th.SKY, w=5.4, h=1.6, tsize=22, size=26) for t_ in ["The school now has eleven pupils.", "The youngest teacher is fifty-four."]]).arrange(RIGHT, buff=0.6).move_to([0, 1.5, 0])
        good = E.card("✓ a fair inference", "The village is losing its young families.", th.MINT, w=5.4, h=1.6, tsize=24, size=26).move_to([-3.0, -1.5, 0])
        bad = E.card("✗ a guess", "The teachers are badly paid.", th.CORAL, w=5.4, h=1.6, tsize=24, size=26).move_to([3.0, -1.5, 0])
        arrs = VGroup(*[Arrow(f_.get_bottom(), good.get_top(), buff=0.1, color=th.MINT, stroke_width=3) for f_ in facts])
        why = T("nothing in the text points at it", size=22, color=th.CORAL).next_to(bad, DOWN, buff=0.15)
        with self.say("An inference is not a guess; it is a conclusion with a line behind it. If the passage says the school now has eleven pupils, and the youngest teacher is fifty four, then the village is losing its young families is a fair inference: two facts point at it. The teachers are badly paid is not, because nothing in the text points at it.") as v:
            self.play(ReplacementTransform(h, h2))
            v.until("If the passage")
            self.play(LaggedStart(*[FadeIn(f_, shift=DOWN * 0.2) for f_ in facts], lag_ratio=0.5))
            v.until("then the village")
            self.play(*[GrowArrow(a_) for a_ in arrs], FadeIn(good))
            v.until("The teachers")
            self.play(FadeIn(bad), FadeIn(why))
        self.play(FadeOut(VGroup(h2, facts, good, bad, arrs, why)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "A worked passage: \"Water Out of the Air\"")
        panel = RoundedRectangle(corner_radius=0.12, width=7.0, height=3.6, stroke_color=th.FAINT, stroke_width=1.5, fill_color=th.PANEL, fill_opacity=1).move_to([-2.9, 0.75, 0])
        tx = para("[4] The attraction of the method is not its output, which is modest, but its cost. A village that installs a row of nets needs no fuel, no electricity and no technician; a broken panel is a sewing job.", width=6.4, size=24, color=th.BODY).move_to(panel)
        stmt = E.card("statement 4", "Fog nets cost less to install than a deep tube well.", th.SKY, w=5.2, h=2.0, tsize=24, size=26).move_to([3.8, 1.4, 0])
        verdict = E.chip("NOT GIVEN", th.AMBER, size=28).move_to([3.8, -0.15, 0])
        why = para("cheap, yes — but a tube well is never mentioned: the comparison isn't in the passage, even if it is true.", width=11.4, size=24, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Here is part of a practice passage about fog nets. Paragraph four says the attraction of the method is not its output, which is modest, but its cost: no fuel, no electricity, no technician. Statement four: fog nets cost less to install than a deep tube well. Cheap, yes. But a tube well is never mentioned. The comparison is not in the passage, even though it may well be true, so the answer is not given.") as v:
            self.play(FadeIn(h), FadeIn(panel), FadeIn(tx))
            v.until("Statement four")
            self.play(FadeIn(stmt, shift=UP * 0.2))
            v.until("so the answer")
            self.play(FadeIn(verdict, scale=1.2), FadeIn(why))
        self.play(FadeOut(VGroup(panel, tx, stmt, verdict, why)))
        h2 = E.head(self, "In your own words: change the words, keep the meaning")
        orig = para("the passage: some droplets strike a thread and stick … and slide down the mesh into a gutter", width=11.4, size=26, color=th.BODY).move_to([0, 1.9, 0])
        pairs = VGroup(*[VGroup(T(a_, size=30, color=th.CORAL), T("→", size=30, color=th.MUTED), T(b_, size=30, color=th.MINT)).arrange(RIGHT, buff=0.35) for a_, b_ in [("strike", "hit"), ("stick", "cling"), ("slide down", "run down")]]).arrange(DOWN, buff=0.35).move_to([0, 0.1, 0])
        ans = para("your answer: some droplets hit the threads and cling to them … then run down into a gutter.", width=11.4, size=26, color=th.MINT).move_to([0, -1.85, 0])
        nt = T("Copying the sentence unchanged scores zero.", size=26, color=th.CORAL).move_to([0, -2.9, 0])
        with self.say("Set B asks: in your own words, explain how a droplet of fog becomes water in the tank. The passage says droplets strike a thread and stick, then slide down the mesh. Change the words and keep the meaning: strike becomes hit, stick becomes cling, slide down becomes run down. Copying the sentence unchanged would score zero.") as v:
            self.play(ReplacementTransform(h, h2))
            v.until("The passage says")
            self.play(FadeIn(orig))
            v.until("strike becomes")
            self.play(LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.2) for p_ in pairs], lag_ratio=0.5), FadeIn(ans))
            v.until("Copying")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(orig, pairs, ans, nt)))
        h3 = E.head(self, "Before you hand it in")
        chk = E.bullets(["could I point at the line behind every answer?", "own words: did the wording really change?", "a gap-fill: the passage's word, unchanged, and only one?", "anything marked False that is merely Not Given?", "vocabulary: the right part of speech, and does it fit back?", "a title that covers the whole passage, not paragraph one?"], width=11.2, size=26).move_to([0, -0.2, 0])
        with self.say("And before you hand it in: could you point at the line behind every answer? For own words, did the wording really change? For a gap fill, is it the passage's word, unchanged, and only one? Did you mark anything false that is merely not given? Is each vocabulary answer the right part of speech, and does it fit back into the sentence? And does your title cover the whole passage, not just paragraph one?") as v:
            self.play(ReplacementTransform(h2, h3))
            E.reveal_list(self, chk, v.dur * 0.8)
        self.play(FadeOut(VGroup(h3, chk)))
        self.quiz("Passage: \"Most students walk to school.\" Statement: \"All students walk to school.\"",
                  ["True", "False", "Not Given", "Can't tell"], 1,
                  "Pause and think.",
                  "Most contradicts all, so the passage says the opposite: False.")
        self.quiz("The passage praises solar lamps and never mentions kerosene. \"Solar lamps are cheaper than kerosene.\"",
                  ["True", "False", "Not Given", "True, in real life"], 2,
                  "One more.",
                  "A comparison the passage never makes: Not Given.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "The passage is the authority: point at the line behind every answer.",
            "Skim, read the questions, scan and mark, write, check.",
            "Scan for numbers, dates and capitals first; common words last.",
            "True: it says so. False: it says the opposite. Not Given: it is silent.",
            "Context words: whole sentence, part of speech, signal, replace and test.",
        ], "Quick recap. The passage is the authority. Five steps, with the questions read before the careful reading. Scan for the easy shapes first. True, false and not given are three different claims. And words in context are reasoned, not remembered.")
        self.outro("That was unseen reading. Next, the last unit of Class 12 English: vocabulary, sounds, spelling and idioms. See you there.")
