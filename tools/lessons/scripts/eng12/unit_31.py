import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

YRS = [2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081]
SCI = [42, 55, 68, 58, 90, 112, 130, 138]
MGT = [96, 92, 85, 70, 74, 76, 75, 72]
CATS = ["Food", "Housing", "Education", "Health", "Transport", "Other"]
VILL = [9, 2, 3, 2.5, 1.5, 2]
CITY = [14, 12, 8, 3, 5, 6]


def line_graph(x_len=8.4, y_len=4.0):
    ax = Axes(x_range=[2073.5, 2081.5, 1], y_range=[0, 150, 50], x_length=x_len, y_length=y_len, tips=False,
              axis_config={"color": th.MUTED, "stroke_width": 2, "include_ticks": True}, y_axis_config={"include_numbers": False})
    yl = VGroup(*[T(str(v), size=20, color=th.MUTED).next_to(ax.c2p(2073.5, v), LEFT, buff=0.12) for v in (0, 50, 100, 150)])
    xl = VGroup(*[T(str(y)[2:], size=20, color=th.MUTED).next_to(ax.c2p(y, 0), DOWN, buff=0.12) for y in YRS])
    sci = VMobject(stroke_color=th.SKY, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(YRS, SCI)])
    mgt = VMobject(stroke_color=th.AMBER, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(YRS, MGT)])
    key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=th.SKY, stroke_width=5), T("Science", size=22, color=th.SKY)).arrange(RIGHT, buff=0.15),
                 VGroup(Line(ORIGIN, RIGHT * 0.5, color=th.AMBER, stroke_width=5), T("Management", size=22, color=th.AMBER)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    key.next_to(ax.c2p(2074, 150), RIGHT, buff=0.1).shift(DOWN * 0.1)
    g = VGroup(ax, yl, xl, sci, mgt, key)
    g.ax, g.sci, g.mgt = ax, sci, mgt
    return g


def bar_chart(x_len=8.4, y_len=3.8):
    ax = Axes(x_range=[0, 6, 1], y_range=[0, 15, 5], x_length=x_len, y_length=y_len, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_ticks": False})
    bw = x_len / 6 * 0.32
    bars = VGroup()
    for k, (v, c) in enumerate(zip(VILL, CITY)):
        x0 = ax.c2p(k + 0.5, 0)
        bars.add(Rectangle(width=bw, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=th.MINT, fill_opacity=0.85).move_to(x0 + LEFT * bw * 0.55, aligned_edge=DOWN))
        bars.add(Rectangle(width=bw, height=ax.c2p(0, c)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=th.PINK, fill_opacity=0.85).move_to(x0 + RIGHT * bw * 0.55, aligned_edge=DOWN))
    xl = VGroup(*[T(c_, size=20, color=th.MUTED).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.12) for k, c_ in enumerate(CATS)])
    yl = VGroup(*[T(str(v), size=20, color=th.MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 5, 10, 15)])
    unit = T("Rs '000 a month", size=20, color=th.MUTED).next_to(ax.c2p(0, 15), UP, buff=0.3).align_to(yl, LEFT)
    key = VGroup(VGroup(Square(0.25, stroke_width=0, fill_color=th.MINT, fill_opacity=0.85), T("village", size=20, color=th.MINT)).arrange(RIGHT, buff=0.12),
                 VGroup(Square(0.25, stroke_width=0, fill_color=th.PINK, fill_opacity=0.85), T("city", size=20, color=th.PINK)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.4).next_to(ax.c2p(6, 15), DOWN, buff=0.1).align_to(ax.c2p(6, 15), RIGHT)
    g = VGroup(ax, bars, xl, yl, unit, key)
    g.ax, g.bars = ax, bars
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 31
    TITLE = "Guided Writing: Charts, Graphs and Outlines"
    SUBTITLE = "Writing · Question 4: describe, compare, and then stop"
    SECTIONS = ["What Question 4 wants", "Reading the visual", "The phrase bank", "A line graph with two lines", "A grouped bar chart and a process", "A story from an outline"]
    NEXT = "Unit 32 · Functional Writing"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        g = line_graph().move_to([0, 0.6, 0])
        nt = para("Turn a picture of information into English that a reader who has never seen the picture could follow.", width=11, size=28, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Two lines on one graph: students in the Science faculty of a school in Butwal, and students in Management, over eight years. Question four hands you this, and pays seven marks for the sentences you build out of it."):
            self.play(Create(g.ax), FadeIn(g[1]), FadeIn(g[2]), FadeIn(g[5]))
            self.play(Create(g.sci), Create(g.mgt), run_time=3)
        with self.say("Nothing has to be invented, and nothing may be. What is tested is whether you can turn a picture of information into English that a reader who has never seen the picture could follow."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(g, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 31: guided writing from charts, graphs and outlines."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. What question four wants. Reading the visual. The phrase bank. A line graph with two lines. A grouped bar chart, and a process. And a story from an outline.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Describe, compare — and then stop")
        three = VGroup(*[E.card(a_, b_, c_, w=3.95, h=2.4, size=24) for a_, b_, c_ in [("1  what it shows", "paraphrase the title: what, in what units, for whom, when", th.SKY), ("2  the pattern", "an overview sentence — no figures", th.MINT), ("3  the figures", "six to eight well-chosen numbers, with units", th.AMBER)]]).arrange(RIGHT, buff=0.25).move_to([0, 0.9, 0])
        no = T("No causes. No opinions. Every sentence of cause is a sentence of description you didn't write.", size=24, color=th.CORAL).move_to([0, -1.0, 0])
        no.scale_to_fit_width(min(no.width, 12.4))
        rows = [["credited", "marks", "means"], ["content", "3", "key figures, the pattern, nothing invented"], ["organisation", "2", "paraphrased opening, overview, grouped details, close"], ["language", "2", "trend and comparison words; grammar"]]
        tb = E.table(rows, [2.8, 1.4, 8.0], row_h=0.5, size=22, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, -2.35, 0])
        with self.say("A grade twelve data description does three things. It says what the visual shows, in your own words. It names the pattern, in an overview sentence. And it supports the pattern with figures. It does not explain why the pattern happened, and gives no opinion. The seven marks: three for content, two for organisation, two for language. Write a hundred and fifty to two hundred words, in about fifteen minutes; three hundred words buys no extra mark, only more chances of error.") as v:
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in three], lag_ratio=0.4))
            self.play(FadeIn(no))
            E.reveal_table(self, tb, v.dur * 0.3)
        self.play(FadeOut(VGroup(h, three, no, tb)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["visual", "shows", "first thing to find"], ["bar chart", "quantities side by side", "tallest and shortest bar"], ["grouped bar chart", "sets compared by category", "widest and narrowest gap"], ["line graph", "change over time", "direction, peaks, crossings"],
                ["pie chart", "parts of one whole (100 %)", "biggest slice; over half?"], ["table", "exact figures, two variables", "extremes of rows and columns"], ["flow chart", "stages in a fixed order", "how many stages; start, end"]]
        tb = E.table(rows, [3.1, 4.6, 5.1], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.6, 0])
        nt = T("Before writing: what is measured? in what units? for whom, over what period?", size=26, color=th.SKY).move_to([0, -2.3, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Six kinds of visual. A bar chart: find the tallest and the shortest bar. A grouped bar chart: the widest and narrowest gaps. A line graph: the overall direction, peaks, and crossing points. A pie chart: the biggest slice, and anything over half. A table: the extremes in each row and column. A flow chart: how many stages, and where it starts and ends. And before you write a word, answer three questions from the labels: what is measured, in what units, and for whom over what period.") as v:
            E.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = E.head(self, "Content marks lost before you begin")
        pairs = [("copying the title as your first sentence", "paraphrase it"), ("Rs '000: a bar of 12 = Rs 12", "Rs 12,000"), ("describing two lines one at a time", "compare them"), ("listing every figure", "six or seven good ones"), ("\"enrolment fell because of …\"", "no causes")]
        rows2 = VGroup(*[VGroup(T("✗ " + a_, size=26, color=th.CORAL), T("→ " + b_, size=26, color=th.MINT)).arrange(RIGHT, buff=0.4) for a_, b_ in pairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.2, 0])
        rows2.scale_to_fit_width(min(rows2.width, 12.4))
        with self.say("Most lost content marks begin here. Copying the title as your first sentence: paraphrase it. Misreading the unit: if the axis says thousands of rupees, a bar of twelve is twelve thousand rupees. Describing two lines one at a time and never comparing them: the comparison is the answer. Listing every figure: six or seven good ones score more. And giving a reason the chart does not show."):
            self.play(FadeIn(h))
            for r_ in rows2:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(1.4)
        self.play(FadeOut(VGroup(h, rows2)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Words for movement")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=6.0, y_length=3.6, tips=False, axis_config={"color": th.FAINT, "stroke_width": 2, "include_ticks": False}).move_to([-3.3, -0.4, 0])
        pts = [(0, 3), (1.5, 3.4), (3, 6.8), (4, 8.6), (5, 7.2), (6, 7.0), (7, 7.1), (8, 4.0), (9, 4.6), (10, 5.8)]
        cv = VMobject(stroke_color=th.AMBER, stroke_width=5).set_points_as_corners([ax.c2p(x, y) for x, y in pts])
        tags = VGroup(*[T(t_, size=22, color=c_).next_to(ax.c2p(x, y), d_, buff=b_) for t_, c_, x, y, d_, b_ in [("edged up", th.SKY, 1.4, 3.35, DOWN, 0.15), ("surged", th.MINT, 2.4, 5.45, LEFT, 0.3), ("peaked", th.AMBER, 4, 8.6, UP, 0.12), ("levelled off", th.MUTED, 6.4, 7.05, UP, 0.15), ("plunged", th.CORAL, 7.5, 5.55, LEFT, 0.2), ("recovered", th.PINK, 9.0, 4.6, DR, 0.1)]])
        bank = VGroup(*[VGroup(T(a_, size=24, color=c_, weight="BOLD"), T(b_, size=22, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.06) for a_, b_, c_ in [
            ("up a lot", "rose, climbed, surged, doubled", th.MINT), ("down a lot", "fell, declined, slumped, plunged, halved", th.CORAL), ("no change", "remained steady, levelled off, plateaued", th.MUTED), ("up and down", "fluctuated, varied", th.SKY), ("turning point", "peaked at, bottomed out at, recovered", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, -0.3, 0])
        with self.say("The two language marks are awarded for vocabulary, so learn it in groups. A small rise: it edged up. A big rise: it rose, climbed, surged, doubled. A big fall: it fell, declined, slumped, plunged. No change: it remained steady, levelled off, plateaued. Up and down: it fluctuated. And the turning points: it peaked at, bottomed out at, recovered."):
            self.play(FadeIn(h), Create(ax))
            self.play(Create(cv), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.3))
            E.reveal_list(self, bank, 5.0)
        self.play(FadeOut(VGroup(ax, cv, tags, bank)))
        h2 = E.head(self, "How much, compared with what")
        deg = VGroup(*[T(t_, size=26, color=c_) for t_, c_ in [("rose sharply · a sharp rise", th.MINT), ("fell steadily · a steady fall", th.SKY), ("increased slightly · a slight increase", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.2, 1.0, 0])
        cmp_ = VGroup(*[T(t_, size=26, color=th.INK) for t_ in ["twice as many as · half as many as", "accounts for a fifth of the total", "second only to · followed by", "whereas · by contrast · compared with"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, 1.0, 0])
        prep = VGroup(T("rose to 138 (where it ended)  ·  rose by 48 (how much it moved)", size=26, color=th.AMBER), T("a rise of 48  ·  an increase in the number of students  ·  stood at 42 in 2074", size=26, color=th.AMBER)).arrange(DOWN, buff=0.2).move_to([0, -1.7, 0])
        prep.scale_to_fit_width(min(prep.width, 12.4))
        tense = T("Tense: dated past data → past simple; a process or undated chart → present simple.", size=24, color=th.MUTED).move_to([0, -2.9, 0])
        tense.scale_to_fit_width(min(tense.width, 12.4))
        with self.say("Then degree: adverbs after the verb, adjectives before the noun: rose sharply, a sharp rise. Comparison and proportion, the half that grade twelve adds: twice as many as, accounts for a fifth of the total, second only to, whereas. The prepositions carry a mark of their own: rose to a hundred and thirty eight is where it ended; rose by forty eight is how much it moved; an increase in the number, never of. And tense is decided by the chart: dated past data takes the past simple; a process takes the present."):
            self.play(ReplacementTransform(h, h2), FadeIn(deg), FadeIn(cmp_))
            self.play(FadeIn(prep))
            self.play(FadeIn(tense))
        self.play(FadeOut(VGroup(h2, deg, cmp_, prep, tense)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        g = line_graph(x_len=6.4, y_len=3.6).move_to([-3.2, 0.2, 0])
        ax = g.ax
        cross = Circle(radius=0.32, color=th.CORAL, stroke_width=4).move_to(ax.c2p(2077.43, 71.7))
        para_s = [("opening", "The line graph compares Grade 11 enrolment in Science and Management at a Butwal school, 2074–2081 BS."),
                  ("overview", "The overall pattern is a reversal: Science began far smaller and ended far larger."),
                  ("details", "Science grew from 42 to 68 by 2076, dipped to 58, then rose sharply to 138 — over three times its start. Management fell to 70, then fluctuated between 72 and 76."),
                  ("close", "By 2081 Science students outnumbered Management by almost two to one.")]
        ans = VGroup(*[VGroup(T(a_, size=24, color=th.AMBER, weight="BOLD"), para(b_, width=5.6, size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for a_, b_ in para_s])
        top, bot = VGroup(*ans[:2]), VGroup(*ans[2:])
        for half in (top, bot):
            half.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.5, 0.3, 0])
            if half.height > 5.0:
                half.scale_to_fit_height(5.0).move_to([3.5, 0.3, 0])
        with self.say("A model answer for the two line graph. The opening paraphrases the title: the graph compares grade eleven enrolment in Science and Management at a Butwal school, from twenty seventy four to twenty eighty one. The overview names the pattern, with no figures: a reversal. Science began far smaller and ended far larger.") as v:
            self.play(FadeIn(g), FadeIn(top[0], shift=RIGHT * 0.2))
            self.hold(v.dur * 0.55)
            self.play(FadeIn(top[1], shift=RIGHT * 0.2), run_time=0.6)
        s2 = "Then the details, grouped by period, not year by year: Science grew from forty two to sixty eight, dipped to fifty eight, then rose sharply to a hundred and thirty eight, more than three times its start, while Management fell to seventy and then fluctuated between seventy two and seventy six. Name the crossing point. And close: by twenty eighty one Science outnumbered Management by almost two to one."
        with self.say(s2) as v:
            self.play(FadeOut(top, shift=UP * 0.2), FadeIn(bot[0], shift=RIGHT * 0.2), run_time=0.8)
            self.hold(max(0.5, v.dur * len(s2[:s2.index("Name the")].split()) / len(s2.split()) - 0.8))
            self.play(Create(cross))
            self.hold(0.8)
            self.play(FadeIn(bot[1], shift=RIGHT * 0.2), run_time=0.6)
        nt = T("grew · dipped · rose sharply · fell · fluctuated — not \"increased\" five times", size=24, color=th.MINT).move_to([0, -2.9, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Notice the verbs: grew, dipped, rose sharply, fell, fluctuated, instead of increased five times."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(g, cross, bot, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "A grouped bar chart: write about the gaps")
        g = bar_chart(x_len=7.6, y_len=3.4).move_to([-2.6, -0.4, 0])
        food = SurroundingRectangle(VGroup(g.bars[0], g.bars[1]), color=th.AMBER, buff=0.08)
        housing = SurroundingRectangle(VGroup(g.bars[2], g.bars[3]), color=th.CORAL, buff=0.08)
        health = SurroundingRectangle(VGroup(g.bars[6], g.bars[7]), color=th.SKY, buff=0.08)
        notes = VGroup(*[para(t_, width=4.6, size=22, color=c_) for t_, c_ in [("City spends more on every heading: about Rs 48,000 vs Rs 20,000 in total.", th.INK), ("Food is the biggest item for both — nearly half the village budget, under a third of the city's.", th.AMBER),
                                                                          ("Widest gap: housing, Rs 12,000 vs 2,000 — six times.", th.CORAL), ("Narrowest: health, Rs 3,000 vs 2,500.", th.SKY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, -0.2, 0])
        with self.say("With two sets of bars, write about the gaps, not the heights. Here, village and city household spending, in thousands of rupees a month. The city spends more on every heading, about forty eight thousand against twenty thousand in total. Food is the biggest item for both, but it is nearly half of the village budget and under a third of the city's: turning bars into a share of the whole is the comparison grade twelve wants. The widest gap is housing: six times as much. The narrowest is health."):
            self.play(FadeIn(h), FadeIn(g))
            self.play(FadeIn(notes[0]))
            self.play(Create(food), FadeIn(notes[1]))
            self.play(Create(housing), FadeIn(notes[2]))
            self.play(Create(health), FadeIn(notes[3]))
        self.play(FadeOut(VGroup(h, g, food, housing, health, notes)))
        h2 = E.head(self, "A process: present simple passive + sequencers")
        steps = ["separated at home", "collected by tractor", "weighed; plastic picked out", "piled into rows, turned weekly", "sieved after ten weeks", "bagged and sold"]
        boxes = VGroup(*[E.card(f"{k + 1}", s_, th.PALETTE[k % 8], w=3.8, h=1.55, tsize=24, size=22) for k, s_ in enumerate(steps)])
        boxes[0:3].arrange(RIGHT, buff=0.5).move_to([0, 1.2, 0])
        boxes[3:6].arrange(LEFT, buff=0.5).move_to([0, -0.95, 0])
        arrs = VGroup(*[Arrow(boxes[k].get_right() if k < 2 else boxes[k].get_bottom(), boxes[k + 1].get_left() if k < 2 else boxes[k + 1].get_top(), buff=0.06, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in range(3)])
        arrs.add(*[Arrow(boxes[k].get_left(), boxes[k + 1].get_right(), buff=0.06, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in (3, 4)])
        lang = T("The waste is weighed, … is then piled …, after which it is sieved. Finally it is bagged.", size=24, color=th.AMBER).move_to([0, -2.6, 0])
        lang.scale_to_fit_width(min(lang.width, 12.4))
        with self.say("A process diagram is not data: no figures, no trend, but stages in a fixed order. Count the stages in your opening: the chart shows how a municipality turns household waste into compost in six stages. Then use the present simple passive, because who does it does not matter, with a sequencer for every stage: the waste is collected, then weighed, after which it is piled into rows, and finally it is bagged and sold."):
            self.play(ReplacementTransform(h, h2))
            for k, b_ in enumerate(boxes):
                self.play(FadeIn(b_), *([GrowArrow(arrs[k - 1])] if k else []), run_time=0.5)
            self.play(FadeIn(lang))
        self.play(FadeOut(VGroup(h2, boxes, arrs, lang)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "A story from an outline")
        steps = E.bullets(["read every note first — you can't open without knowing the end", "fill what the notes leave out: a name, a place, a season — never contradicting a note", "past tense, third person; hold it", "weight the notes unequally: the turning point gets five sentences, the setting two", "show, don't tell: not \"he was frightened\" but \"he put the bag down twice before he could untie it\"", "one or two lines of direct speech; a title of three to six words that doesn't give away the ending"], width=11.4, size=24).move_to([0, -0.1, 0])
        with self.say("The other half of question four: a story from outline notes. Read every note first; you cannot choose an opening until you know the ending. Fill in what the notes leave out, a name, a place, a season, without contradicting any note. Choose past tense and third person, and hold them. Weight the notes unequally: the turning point gets four or five sentences, the setting two. Show rather than tell: not he was frightened, but he put the bag down twice before he could untie it. Add a line or two of direct speech. And a short title that does not give away the ending."):
            self.play(FadeIn(h))
            E.reveal_list(self, steps, 16.0)
        self.play(FadeOut(steps))
        pairs = [("Poor farmer goes market, finds bag.", "Note form left in: every note needs articles and a verb."), ("He opened the gate and sees a snake.", "Tense drift: choose the past and stay there."), ("The Honest Farmer Is Rewarded", "A title that tells the ending.")]
        rows = VGroup(*[VGroup(T("✗ " + a_, size=26, color=th.CORAL), T(b_, size=24, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for a_, b_ in pairs]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.3, 0])
        chk = para("Last two minutes: a paraphrased opening? an overview? units? a comparison? the passive for a process? no causes? 150–200 words?", width=11.6, size=24, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Faults that cost story marks: note form left in; tense drift, he opened the gate and sees a snake; and a title that tells the ending. And for every question four answer, a two minute check: a paraphrased opening, an overview, figures with units, a comparison, the passive for a process, no causes, and a hundred and fifty to two hundred words."):
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.5))
            self.play(FadeIn(chk))
        self.play(FadeOut(VGroup(h, rows, chk)))
        self.quiz("Which sentence belongs in a chart description?",
                  ["COVID caused the fall.", "Science rose to 138.", "I think Science is better.", "Science is the future."], 1,
                  "Pause and think.",
                  "Describe and compare with figures; no causes and no opinions.")
        self.quiz("\"The number of students rose ____ 90 ____ 138.\"",
                  ["by / to", "from / to", "of / in", "at / by"], 1,
                  "One more.",
                  "Rose from 90 to 138 — a rise of 48, or: it rose by 48.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Paraphrase the title; overview the pattern; support it with 6–8 figures + units.",
            "Describe and compare — never explain why, never give an opinion.",
            "Trend words: surged, plunged, plateaued, fluctuated, peaked; rose to / by.",
            "Two series: write about the gaps and the crossing point; shares of the whole.",
            "Process: present passive + sequencers. Story: weight the turning point; title last.",
        ], "Quick recap. Describe, compare, and stop. Read the labels first. Learn the phrase bank. Compare the lines and the gaps. Use the passive for a process. And shape a story around its turning point.")
        self.outro("That was guided writing. Next: functional writing — letters to the editor, emails, CVs and applications. See you there.")
