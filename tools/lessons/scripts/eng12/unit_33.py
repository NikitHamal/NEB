import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def hourglass(cx=-2.6):
    top = Polygon([cx - 3.0, 2.6, 0], [cx + 3.0, 2.6, 0], [cx + 1.7, 1.15, 0], [cx - 1.7, 1.15, 0], stroke_color=th.AMBER, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    body = Rectangle(width=3.4, height=2.6, stroke_color=th.SKY, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to([cx, -0.25, 0])
    bot = Polygon([cx - 1.7, -1.65, 0], [cx + 1.7, -1.65, 0], [cx + 3.0, -3.1, 0], [cx - 3.0, -3.1, 0], stroke_color=th.MINT, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    tt = VGroup(T("a general opening", size=22, color=th.INK).move_to([cx, 2.3, 0]), T("narrow to the issue", size=22, color=th.MUTED).move_to([cx, 1.85, 0]), T("THESIS", size=24, color=th.AMBER, weight="BOLD").move_to([cx, 1.4, 0]))
    bt = VGroup(*[T(s_, size=22, color=c_).move_to([cx, y, 0]) for s_, c_, y in [("reason 1", th.INK, 0.65), ("reason 2", th.INK, 0.05), ("reason 3", th.INK, -0.55), ("other side, answered", th.CORAL, -1.15)]])
    seps = VGroup(*[Line([cx - 1.4, y, 0], [cx + 1.4, y, 0], color=th.FAINT, stroke_width=1.5) for y in (0.35, -0.25, -0.85)])
    ct = VGroup(T("restated in new words", size=22, color=th.MINT).move_to([cx, -1.95, 0]), T("what follows from it", size=22, color=th.MUTED).move_to([cx, -2.4, 0]), T("a last line worth remembering", size=22, color=th.INK).move_to([cx, -2.85, 0]))
    g = VGroup(top, tt, body, seps, bt, bot, ct)
    g.top, g.tt, g.body, g.bt, g.bot, g.ct = VGroup(top, tt), body, VGroup(body, seps), bt, VGroup(bot, ct), ct
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 33
    TITLE = "Free Writing: Essays and Memoirs"
    SUBTITLE = "Writing · Question 6: a position, or a remembered scene"
    SECTIONS = ["What Question 6 wants", "Five kinds, and the thesis", "The hourglass and the paragraph", "Openings, endings and links", "Inside a model essay", "The memoir"]
    NEXT = "Unit 34 · Unseen Reading"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        cards = VGroup(*[E.card(a_, b_, c_, w=6.0, h=2.2, tsize=28, size=28) for a_, b_, c_ in [("a question", "Examinations do more harm than good. Do you agree?", th.SKY), ("a memory", "An unforgettable morning.", th.PINK)]]).arrange(RIGHT, buff=0.6).move_to([0, 1.2, 0])
        owe = VGroup(*[T(t_, size=26, color=c_) for t_, c_ in [("owed: a position, with reasons", th.SKY), ("owed: a scene, and what it means now", th.PINK)]])
        for o_, c_ in zip(owe, cards):
            o_.scale_to_fit_width(min(o_.width, c_.width)).next_to(c_, DOWN, buff=0.4)
        nt = para("Ten marks and a free choice: the question most often wasted.", width=11, size=28, color=th.AMBER).move_to([0, -2.4, 0])
        s1 = "Two topics on the same paper. Examinations do more harm than good: do you agree? And: an unforgettable morning. The first is a question, and it is owed a position, with reasons. The second is a memory, and it is owed a scene, and what you understand about it now. Deciding which one you have been given is the first minute's work."
        with self.say(s1) as v:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            v.until("And: an")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            v.until("The first is")
            self.play(FadeIn(owe[0]))
            v.until("The second is")
            self.play(FadeIn(owe[1]))
        with self.say("Question six leaves you alone with ten marks and a free choice, which is exactly why it is the question most often wasted."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(cards, owe, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 33: free writing, essays and memoirs."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. What question six wants. The five kinds of essay, and the thesis. The hourglass, and the four moves of a paragraph. Openings, endings and links. Inside a model essay. And the memoir.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Ten marks, thirty minutes")
        rows = [["credited", "marks", "means"], ["content", "4", "a clear position or centre; ideas developed; detail"], ["organisation", "3", "an intro, 3–4 one-idea paragraphs, a conclusion"], ["language", "3", "a range of sentences and words; accurate grammar"]]
        tb = E.table(rows, [2.8, 1.4, 8.4], row_h=0.6, size=24, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, 1.25, 0])
        segs = [(4, "plan 4", th.AMBER), (22, "write 22 minutes", th.SKY), (4, "check 4", th.MINT)]
        bar, x = VGroup(), -6.0
        for m_, lab, c_ in segs:
            w = 12.0 * m_ / 30
            r_ = Rectangle(width=w - 0.04, height=0.55, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to([x + w / 2, -1.55, 0])
            bar.add(VGroup(r_, T(lab, size=24, color=c_).next_to(r_, UP, buff=0.15)))
            x += w
        words = T("300–400 words, with a title", size=26, color=th.INK).move_to([0, -2.6, 0])
        with self.say("Ten marks. Four for content: a clear position or a clear centre, with ideas developed rather than listed. Three for organisation: an introduction, three or four body paragraphs and a conclusion, each paragraph on one idea. And three for language: range, and accuracy.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
        with self.say("Write three hundred to four hundred words in about thirty minutes: four minutes to plan, twenty two to write, and four to check.") as v:
            for b_, q_ in zip(bar, ["four minutes", "twenty two", "and four"]):
                v.until(q_)
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[1]), run_time=0.5)
            self.play(FadeIn(words))
        self.play(FadeOut(VGroup(tb, bar, words)))
        h2 = E.head(self, "Four minutes of planning is the essay")
        same = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.25, height=0.75, stroke_color=th.CORAL, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1) for _ in range(4)]).arrange(RIGHT, buff=0.18).move_to([-3.4, 0.6, 0])
        same_t = VGroup(*[T("point A", size=22, color=th.CORAL).move_to(b_) for b_ in same])
        steps = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.25, height=0.75, stroke_color=th.MINT, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1).move_to([1.4 + 1.43 * k, -0.4 + 0.55 * k, 0]) for k in range(4)])
        steps_t = VGroup(*[T(f"step {k + 1}", size=22, color=th.MINT).move_to(b_) for k, b_ in enumerate(steps)])
        cap1 = para("Writing at once: the same point, four times", width=5.6, size=24, color=th.CORAL).next_to(same, DOWN, buff=0.5)
        cap2 = para("Planning first: each paragraph moves one step", width=5.6, size=24, color=th.MINT).move_to([3.55, -1.5, 0])
        nt = para("400 careful words beat 600 careless ones: the language mark is for accuracy, not quantity.", width=11.4, size=26, color=th.AMBER).move_to([0, -2.75, 0])
        with self.say("A candidate who starts writing the moment the topic is chosen produces four paragraphs that say the same thing four times. A candidate who spends four minutes on a plan produces four paragraphs that each move the argument one step further. And four hundred careful words beat six hundred careless ones, because the language mark is a mark for accuracy, not for quantity.") as v:
            self.play(ReplacementTransform(h, h2), LaggedStart(*[FadeIn(VGroup(b_, t_)) for b_, t_ in zip(same, same_t)], lag_ratio=0.3), FadeIn(cap1))
            v.until("A candidate who spends")
            self.play(LaggedStart(*[FadeIn(VGroup(b_, t_), shift=UP * 0.2) for b_, t_ in zip(steps, steps_t)], lag_ratio=0.3), FadeIn(cap2))
            v.until("And four hundred")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h2, same, same_t, steps, steps_t, cap1, cap2, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["kind", "the topic sounds like", "the examiner wants", "tense"], ["argumentative", "Do you agree?", "position + reasons + other side", "present"], ["expository", "Explain why …", "causes or stages; no opinion", "present"],
                ["descriptive", "A monsoon morning", "one place, one hour, five senses", "past or present"], ["narrative", "An incident that …", "one event, a turning point", "past"], ["reflective", "What failure taught me", "the experience + the thought", "past → present"]]
        tb = E.table(rows, [2.3, 3.45, 5.0, 2.45], row_h=0.66, size=22, colors=[th.AMBER, th.SKY, th.INK, th.MINT]).move_to([0, 0.75, 0])
        nt = para("A memoir is a narrative with the reflection built in: it gets its own part.", width=11.4, size=26, color=th.PINK).move_to([0, -2.6, 0])
        with self.say("Five kinds of essay, and the topic tells you which. Do you agree, or should Nepal: argumentative, a position, reasons, and one honest counter argument, answered. Explain why, or discuss the causes: expository, causes or stages in order, and no opinion. A monsoon morning in my village: descriptive, one place, one hour, five senses. An incident that changed me: narrative, one event told in scenes, with a turning point. What failure taught me: reflective, the experience plus the thought it produced. A memoir is a narrative with the reflection built in, and it gets its own part.") as v:
            self.play(FadeIn(tb[0]))
            for r_, q_ in zip(tb[1:], ["Do you agree", "Explain why", "A monsoon", "An incident", "What failure"]):
                v.until(q_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("A memoir is")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = E.head(self, "The thesis: one sentence, a position, the reasons")
        nots = VGroup(*[VGroup(T("✗ " + a_, size=26, color=th.CORAL), T(b_, size=22, color=th.MUTED)).arrange(RIGHT, buff=0.35) for a_, b_ in [("In this essay I will discuss examinations.", "an announcement"), ("Examinations are a very important topic.", "no position"), ("Examinations are good and bad.", "no position")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.3, 0])
        thesis = E.card("✓ a thesis", "Examinations measure memory rather than understanding, and the fear they create does more damage to learning than the discipline they impose is worth.", th.MINT, w=11.6, h=2.0, tsize=26, size=26).move_to([0, -1.6, 0])
        with self.say("An essay that argues needs a thesis: one sentence, usually the last of the introduction, that states your position and signposts the reasons. In this essay I will discuss examinations is an announcement, not a thesis. Examinations are a very important topic takes no position. Examinations are good and bad takes no position either. Here is a thesis: examinations measure memory rather than understanding, and the fear they create does more damage to learning than the discipline they impose is worth.") as v:
            self.play(FadeIn(h))
            for n_, q_ in zip(nots, ["In this essay", "a very important", "good and bad"]):
                v.until(q_)
                self.play(FadeIn(n_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("Here is a thesis")
            self.play(FadeIn(thesis, shift=UP * 0.2))
        self.play(FadeOut(VGroup(nots, thesis)))
        h2 = E.head(self, "Test it: could a reasonable person disagree?")
        test = E.wrong_right("Water is necessary for life.", "Bottled water should be taxed.", size=30, rule="a fact can't be argued with; a thesis can").move_to([0, 1.5, 0])
        temps = VGroup(*[E.card(a_, b_, c_, w=5.9, h=2.4, tsize=26, size=24) for a_, b_, c_ in [("position + because", "Nepal should make cycle lanes compulsory, because the cost is small and the health gain large.", th.SKY), ("although + main clause", "Although foreign employment has fed many families, it has emptied our villages.", th.AMBER)]]).arrange(RIGHT, buff=0.4).move_to([0, -1.6, 0])
        with self.say("Test it in one move: can a reasonable person disagree? Water is necessary for life cannot be argued with; it is a fact. Bottled water should be taxed can, so it is a thesis. Two templates help until you no longer need them: a position plus because, or although plus a main clause.") as v:
            self.play(ReplacementTransform(h, h2))
            v.until("Water is")
            self.play(FadeIn(test.wrong))
            v.until("Bottled water")
            self.play(Create(test.cross), FadeIn(test.right), FadeIn(test[2]))
            v.until("Two templates")
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.2) for t_ in temps], lag_ratio=0.5))
        self.play(FadeOut(VGroup(h2, test, temps)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "The shape of the whole essay: an hourglass")
        hg = hourglass()
        side = VGroup(*[VGroup(T(a_, size=26, color=c_, weight="BOLD"), T(b_, size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([1.0, y, 0], aligned_edge=LEFT) for a_, b_, c_, y in [
            ("Introduction · 50–60 words", "narrows from the world to your thesis", th.AMBER, 1.9), ("Body · 200–260 words", "one idea a paragraph; the longest part", th.SKY, -0.25), ("Conclusion · 50–60 words", "widens out: new words, no new idea", th.MINT, -2.4)]])
        ticks = VGroup(*[Line([0.5, y, 0], [0.85, y, 0], color=th.FAINT, stroke_width=2) for y in (1.9, -0.25, -2.4)])
        with self.say("The whole essay has the shape of an hourglass. The introduction narrows: a general opening, then the issue, then the thesis, in fifty or sixty words. The body is the straight part and the longest, two hundred to two hundred and sixty words: a paragraph for each reason, and one for the other side, answered. The conclusion widens back out: the position restated in new words, what follows from it, and a last line worth remembering.") as v:
            self.play(FadeIn(h))
            v.until("The introduction")
            self.play(FadeIn(hg.top), FadeIn(side[0]), Create(ticks[0]))
            v.until("The body")
            self.play(FadeIn(hg.body), FadeIn(side[1]), Create(ticks[1]))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in hg.bt], lag_ratio=0.4))
            v.until("The conclusion")
            self.play(FadeIn(hg.bot), FadeIn(side[2]), Create(ticks[2]))
        self.play(FadeOut(VGroup(hg, side, ticks)))
        h2 = E.head(self, "Every body paragraph: four moves")
        moves = [("Point", "the topic sentence: one idea, stated flatly", "Examinations reward memory, not understanding.", th.SKY), ("Evidence", "an example, a fact, a case", "A student can score full marks on a definition they cannot use.", th.AMBER),
                 ("Explain", "why the evidence proves the point", "What is tested, then, is recall under pressure.", th.MINT), ("Link", "a bridge to the next paragraph", "The cost of that pressure is the next question.", th.PINK)]
        bars = VGroup()
        for k, (a_, b_, ex, c_) in enumerate(moves):
            box = RoundedRectangle(corner_radius=0.1, width=9.6, height=1.1, stroke_color=th.FAINT, stroke_width=1.5, fill_color=th.PANEL, fill_opacity=1).move_to([-1.6, 2.0 - 1.35 * k, 0])
            strip = Rectangle(width=0.14, height=1.1, stroke_width=0, fill_color=c_, fill_opacity=1).align_to(box, LEFT).align_to(box, DOWN)
            l1 = VGroup(T(a_, size=26, color=c_, weight="BOLD"), T("— " + b_, size=24, color=th.INK)).arrange(RIGHT, buff=0.2)
            txt = VGroup(l1, T(ex, size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.4)
            bars.add(VGroup(box, strip, txt))
        tags = VGroup(*[E.chip(t_, c_, size=22).next_to(bars[k], RIGHT, buff=0.25) for k, t_, c_ in [(2, "content marks", th.MINT), (3, "organisation marks", th.PINK)]])
        with self.say("Every body paragraph is built with the same four moves. Point: the topic sentence, one idea stated flatly. Evidence: an example, a fact, a case. Explain: why the evidence proves the point. Link: a bridge to the next paragraph. Most candidates write the first two and stop. The third is where the content marks are, and the fourth is where the organisation marks are.") as v:
            self.play(ReplacementTransform(h, h2))
            for b_, q_ in zip(bars, ["Point:", "Evidence:", "Explain:", "Link:"]):
                v.until(q_)
                self.play(FadeIn(b_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("Most candidates")
            self.play(bars[2:].animate.set_opacity(0.35))
            v.until("The third")
            self.play(bars[2:].animate.set_opacity(1), FadeIn(tags[0]))
            v.until("and the fourth")
            self.play(FadeIn(tags[1]))
        self.play(FadeOut(VGroup(bars, tags)))
        h3 = E.head(self, "Links that turn paragraphs into an essay")
        rows = [["job", "choose from"], ["adding", "furthermore · what is more · in addition"], ["contrasting", "however · by contrast · on the other hand · and yet"], ["cause", "consequently · as a result · which is why · hence"],
                ["example", "for instance · take the case of · consider"], ["conceding", "granted that … · it is true that … but"], ["concluding", "in short · on balance · the upshot is"]]
        tb = E.table(rows, [3.0, 9.4], row_h=0.62, size=24, colors=[th.AMBER, th.INK]).move_to([0, 0.15, 0])
        nt = T("The same \"moreover\" three times is itself an error of style.", size=26, color=th.CORAL).move_to([0, -2.75, 0])
        with self.say("Cohesion turns four paragraphs into one essay, so vary the links. Furthermore and what is more, for adding. However, by contrast, and yet, for contrast. Consequently, which is why, for cause. For instance, take the case of. Granted that, or it is true that, to concede. And in short, on balance, to conclude. The same moreover three times is itself an error.") as v:
            self.play(ReplacementTransform(h2, h3))
            E.reveal_table(self, tb, v.dur * 0.75)
            v.until("The same moreover")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h3, tb, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Six openings the examiner has read a thousand times")
        cl = ["Since time immemorial …", "Man is a social animal …", "In today's modern world of science and technology …", "The dictionary defines education as …", "Every coin has two sides.", "In this essay I am going to discuss …"]
        lines_ = VGroup(*[T(s_, size=26, color=th.INK) for s_ in cl]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.55, 0])
        strikes = VGroup(*[E.strike(l_) for l_ in lines_])
        nt = para("Each wastes the first sentence: the only one read with full attention.", width=11.4, size=26, color=th.AMBER).move_to([0, -2.6, 0])
        s1 = "Six openings every examiner has read a thousand times. Since time immemorial. Man is a social animal. In today's modern world of science and technology. The dictionary defines education as. Every coin has two sides. In this essay I am going to discuss. Each one wastes the first sentence, the only sentence certain to be read with full attention."
        with self.say(s1) as v:
            self.play(FadeIn(h))
            for l_, s_, q_ in zip(lines_, strikes, ["Since time", "Man is", "In today's", "The dictionary", "Every coin", "In this essay"]):
                v.until(q_)
                self.play(FadeIn(l_), run_time=0.3)
                self.play(Create(s_), l_.animate.set_color(th.MUTED), run_time=0.4)
            v.until("Each one")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(lines_, strikes, nt)))
        h2 = E.head(self, "Open with one of these instead")
        cards = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.25, tsize=26, size=24) for a_, b_, c_ in [("a concrete scene", "At six in the morning the corridor outside the exam hall smells of fear and hair oil.", th.SKY), ("a number or a fact", "A Grade 12 student sits roughly thirty formal tests in two years.", th.AMBER),
                                                                                              ("a contradiction", "We say we value understanding, and then we measure it with a stopwatch.", th.MINT), ("a question you will answer", "What exactly is an examination for?", th.PINK)]]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to([0, -0.25, 0])
        with self.say("Use one of four instead. A concrete scene: at six in the morning the corridor outside the examination hall smells of fear and hair oil. A number: a grade twelve student sits roughly thirty formal tests in two years. A contradiction: we say we value understanding, and then we measure it with a stopwatch. Or a question you will answer: what exactly is an examination for?") as v:
            self.play(ReplacementTransform(h, h2))
            for c_, q_ in zip(cards, ["A concrete", "A number", "A contradiction", "Or a question"]):
                v.until(q_)
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(cards))
        h3 = E.head(self, "A conclusion does three small things")
        three = VGroup(*[E.chip(t_, c_, size=28) for t_, c_ in [("1  restate the position in different words", th.MINT), ("2  say what should follow from it", th.SKY), ("3  end on a short sentence", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.9, 0])
        never = VGroup(*[T("✗ " + s_, size=28, color=th.CORAL) for s_ in ["Last but not the least, …", "So, this is my essay."]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.75, 0])
        with self.say("Conclusions fail the opposite way: they repeat the introduction word for word, or bring in a brand new idea. A good one does three small things: it restates the position in different words, says what should follow, and ends on a short sentence. Never begin with last but not the least, and never end with so, this is my essay.") as v:
            self.play(ReplacementTransform(h2, h3))
            for t_, q_ in zip(three, ["it restates", "says what", "and ends"]):
                v.until(q_)
                self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("Never begin")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in never], lag_ratio=0.6))
        self.play(FadeOut(VGroup(h3, three, never)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "A model essay: \"Thirty Tests and One Question\"")
        rows_ = [("intro", "We say we value understanding, then measure it with a stopwatch.", "a contradiction to open; the thesis concedes, then argues", th.SKY),
                 ("charge one", "The first charge against them is that they test recall, not thought.", "photosynthesis: full marks, yet no idea why the plant turns yellow", th.AMBER),
                 ("charge two", "The second charge is heavier. Fear is a poor teacher.", "six months of guess papers: curiosity is postponed", th.AMBER),
                 ("the other side", "It must be granted that examinations do some good.", "a deadline, and a blind examiner: that fairness is real", th.MINT),
                 ("the answer", "Fairness is an argument for examinations of some kind, not for these.", "a remedy, not a repeat of paragraph one", th.PINK)]
        blocks = VGroup()
        for k, (tag, line, note, c_) in enumerate(rows_):
            y = 2.0 - 1.1 * k
            tg = VGroup(RoundedRectangle(corner_radius=0.08, width=2.5, height=0.62, stroke_color=c_, stroke_width=2.5, fill_color=th.PANEL, fill_opacity=1), T(tag, size=22, color=c_, weight="BOLD"))
            tg[1].move_to(tg[0])
            tg.move_to([-5.2, y, 0])
            txt = VGroup(T(line, size=22, color=th.INK), T(note, size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.7, y, 0], aligned_edge=LEFT)
            txt.scale_to_fit_width(min(txt.width, 10.2))
            blocks.add(VGroup(tg, txt))
        s1 = "Here is a model answer to: examinations do more harm than good; do you agree? Its title is Thirty Tests and One Question. It opens with the contradiction: we say we value understanding, and then we measure it with a stopwatch. Its thesis, at the end of paragraph one, concedes before it argues: examinations are not useless, but as they are set they measure memory rather than understanding, and the fear they produce costs more than their discipline is worth."
        s2 = "Each body paragraph opens with a flat topic sentence and then earns it. They test recall, not thought: a student can score full marks on the definition of photosynthesis and still not explain why a plant on a dark window sill turns yellow. Fear is a poor teacher: in the six months before the board exam, learning stops and revision begins. Then the other side, given properly: examinations impose a deadline, and they are blind; the examiner does not know whose child is writing. And the answer: fairness is an argument for examinations of some kind, not for these."
        with self.say(s1) as v:
            self.play(FadeIn(h))
            v.until("It opens")
            self.play(FadeIn(blocks[0], shift=RIGHT * 0.2))
        with self.say(s2) as v:
            for b_, q_ in zip(blocks[1:], ["They test", "Fear is", "Then the other", "And the answer"]):
                v.until(q_)
                self.play(FadeIn(b_, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeOut(blocks))
        h2 = E.head(self, "Why it scores")
        why = E.bullets(["✓  the thesis concedes something before it argues", "✓  every paragraph earns its topic sentence with a concrete case", "✓  the other side is given properly, then answered", "✓  the conclusion offers a remedy instead of a repeat", "✓  sentences vary from three words to thirty"], width=11.4, size=26).move_to([0, -0.1, 0])
        with self.say("Why it scores: the thesis concedes something before it argues. Every paragraph earns its topic sentence with a concrete case. The other side is given properly, then answered. The conclusion proposes a remedy instead of repeating paragraph one. And the sentences vary from three words to thirty.") as v:
            self.play(ReplacementTransform(h, h2))
            for w_, q_ in zip(why, ["the thesis concedes", "Every paragraph", "The other side", "The conclusion", "And the sentences"]):
                v.until(q_)
                self.play(FadeIn(w_, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(h2, why)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "A memoir: one remembered episode")
        top = para("An autobiography covers a life; a memoir takes one episode, and shows why it is still remembered.", width=11.4, size=26, color=th.AMBER).move_to([0, 2.05, 0])
        feats = E.bullets(["1  first person, past tense", "2  a single, narrow slice of time: a morning, one journey", "3  sensory detail: what was seen, heard, smelt, touched", "4  the double voice: then, and the older you telling it", "5  a turning point, and what you now understand"], width=11.4, size=26).move_to([0, -0.8, 0])
        with self.say("A memoir is not an autobiography. An autobiography covers a life; a memoir takes one remembered episode and tells it so the reader understands why it is still remembered. Five features. First person, past tense. A single, narrow slice of time: a morning, one journey. Sensory detail: what could be seen, heard, smelt and touched, which is where the content marks are. The double voice: the person it happened to, and the older person telling it. And a turning point, with a reflection.") as v:
            self.play(FadeIn(h), FadeIn(top))
            for f_, q_ in zip(feats, ["First person", "A single", "Sensory", "The double", "And a turning"]):
                v.until(q_)
                self.play(FadeIn(f_, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(top, feats)))
        h2 = E.head(self, "The double voice")
        now_l = Line([-6.2, 0.75, 0], [6.2, 0.75, 0], color=th.AMBER, stroke_width=4)
        then_l = Line([-6.2, -1.55, 0], [6.2, -1.55, 0], color=th.MUTED, stroke_width=4)
        now_t = T("NOW: the writer looking back, present tense", size=24, color=th.AMBER, weight="BOLD").move_to([-6.2, 2.4, 0], aligned_edge=LEFT)
        then_t = T("THEN: the episode, past tense", size=24, color=th.MUTED, weight="BOLD").move_to([-6.2, -3.1, 0], aligned_edge=LEFT)
        nows = VGroup()
        for x, q_ in [(-2.0, "\"… which surprises me now.\""), (3.4, "\"What I think about now …\"")]:
            nows.add(VGroup(Dot([x, 0.75, 0], radius=0.09, color=th.AMBER), T(q_, size=24, color=th.INK).move_to([x, 1.35, 0]), DashedLine([x, 0.65, 0], [x, -1.45, 0], color=th.FAINT, stroke_width=2)))
        thens = VGroup(*[VGroup(Dot([x, -1.55, 0], radius=0.09, color=th.MUTED), para(t_, width=2.6, size=22, color=th.INK).move_to([x, -2.2, 0])) for x, t_ in [(-5.0, "the bus never came"), (-1.75, "the walk begins"), (1.5, "a lift on a milk truck"), (4.75, "the hall, 25 minutes late")]])
        s2 = "The double voice is what makes it a memoir and not a story. Below, the episode as it happened, in the past: the bus that never came, the walk, the lift from a milk truck, the hall, twenty five minutes late. Above, the writer years later, understanding it: which surprises me now; what I think about now. A memoir keeps crossing between the two."
        with self.say(s2) as v:
            self.play(ReplacementTransform(h, h2))
            v.until("Below")
            self.play(Create(then_l), FadeIn(then_t))
            for t_, q_ in zip(thens, ["the bus that", "the walk", "the lift", "the hall"]):
                v.until(q_)
                self.play(FadeIn(t_, shift=UP * 0.15), run_time=0.4)
            v.until("Above")
            self.play(Create(now_l), FadeIn(now_t))
            for n_, q_ in zip(nows, ["which surprises", "what I think"]):
                v.until(q_)
                self.play(FadeIn(n_[0]), FadeIn(n_[1]), Create(n_[2]), run_time=0.5)
        self.play(FadeOut(VGroup(now_l, then_l, now_t, then_t, nows, thens)))
        h3 = E.head(self, "Detail that is physical, and a last line to use")
        dets = VGroup(*[E.chip(t_, th.SKY, size=24) for t_ in ["a polythene bag", "four steel milk cans", "rain coming sideways"]]).arrange(RIGHT, buff=0.3).move_to([0, 1.6, 0])
        dets.scale_to_fit_width(min(dets.width, 12.6))
        q = E.quote("I have been trying, ever since, to be somebody's milk truck.", who="the last line of the model memoir", width=10.0, size=32).move_to([0, -0.9, 0])
        with self.say("Its details are physical, not emotional: an admit card in a polythene bag, four steel milk cans, the rain coming sideways. And it ends not on the walk, and not on the mark, but on the driver who made room for three boys and asked for nothing. The last line turns a private memory into something a reader can use: I have been trying, ever since, to be somebody's milk truck.") as v:
            self.play(ReplacementTransform(h2, h3), LaggedStart(*[FadeIn(d_, shift=UP * 0.15) for d_ in dets], lag_ratio=0.4))
            v.until("The last line")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.play(FadeOut(VGroup(h3, dets, q)))
        self.quiz("Which sentence is a thesis?",
                  ["I will discuss exams.", "Exams are good and bad.", "Exams harm learning.", "Exams are a big topic."], 2,
                  "Pause and think.",
                  "Only C takes a position that a reasonable person could dispute.")
        self.quiz("What makes a memoir more than a story?",
                  ["a happy ending", "the older voice", "many different events", "a moral in the title"], 1,
                  "One more.",
                  "The double voice: the person it happened to, and the older person telling it.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "A question wants a position; a memory wants a scene. Decide in the first minute.",
            "The thesis: one sentence a reasonable person could dispute, ending paragraph one.",
            "The hourglass; every body paragraph: point, evidence, explain, link.",
            "No cliché openings; conclude in new words, with no new idea.",
            "Memoir: one episode, past tense, sensory detail, the older voice.",
        ], "Quick recap. A position or a scene, decided in the first minute. A thesis that can be disputed. The hourglass, and the four moves. Openings without clichés, conclusions without repeats. And the memoir's double voice.")
        self.outro("That was free writing. Next: unseen reading comprehension. See you there.")
