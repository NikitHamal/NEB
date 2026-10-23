import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

TYPE_COL = [th.MINT, th.SKY, th.AMBER, th.CORAL]


def reality_scale(y=1.6, w=11.6):
    bar = Rectangle(width=w, height=0.36, stroke_width=0).set_fill(color=[th.CORAL, th.AMBER, th.SKY, th.MINT], opacity=0.85).move_to([0, y, 0])  # gradients render right-to-left
    xs = np.linspace(-w / 2 + 0.9, w / 2 - 0.9, 4)
    labs = VGroup(*[VGroup(T(f"type {k}", size=26, color=TYPE_COL[k], weight="BOLD"), T(t_, size=22, color=th.MUTED)).arrange(DOWN, buff=0.08).move_to([x, y + 0.85, 0]) for k, (x, t_) in enumerate(zip(xs, ["always true", "real, likely", "unreal now", "impossible past"]))])
    ticks = VGroup(*[Line([x, y - 0.25, 0], [x, y + 0.25, 0], color=th.INK, stroke_width=3) for x in xs])
    g = VGroup(bar, ticks, labs)
    g.xs = xs
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 28
    TITLE = "Conditional Sentences"
    SUBTITLE = "Grammar · four types, mixed, wish and if only"
    SECTIONS = ["How real is the condition?", "The four types", "Mixed conditionals", "Conditionals without \"if\"", "When will can follow if; the errors", "Wish, if only, and worked items"]
    NEXT = "Unit 29 · Passive Voice"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        sc = reality_scale(y=1.9)
        ex = [("If it rains, the match will be cancelled.", 1), ("If I were you, I would apologise.", 2), ("If she had revised, she would have passed.", 3)]
        lines = VGroup(*[T(t_, size=30, color=TYPE_COL[k]) for t_, k in ex]).arrange(DOWN, buff=0.45).move_to([0, -1.1, 0])
        with self.say("Three sentences with if. If it rains, the match will be cancelled: that may well happen. If I were you, I would apologise: I am not you, so it is unreal. If she had revised, she would have passed: it is over, and it did not happen."):
            self.play(FadeIn(sc))
            dots = []
            for l_, (_, k) in zip(lines, ex):
                dot = Dot(sc.xs[k] * RIGHT + UP * 1.9, radius=0.14, color=WHITE)
                dots.append(dot)
                self.play(FadeIn(l_, shift=UP * 0.15), FadeIn(dot, scale=1.5), run_time=0.7)
                self.hold(2.0)
        nt = para("English shows how real a condition is by its choice of tense — often not the tense of the time you mean.", width=11, size=28, color=th.INK).move_to([0, -3.0, 0])
        with self.say("The whole grammar of conditionals lies in one question: how real is the condition? English answers by choosing a tense, and it is often not the tense of the time being talked about. So learn four fixed patterns, instead of reasoning them out every time."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(sc, lines, nt, *dots)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 28: conditional sentences."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. How real is the condition. The four types. Mixed conditionals. Conditionals without if. When will can follow if, and the errors. And wish, if only, with worked items.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Four fixed patterns")
        rows = [["type", "if-clause", "main clause"], ["0  general truth", "if + present simple", "present simple"], ["1  real, likely", "if + present simple", "will / can / may + base verb"], ["2  unreal now", "if + past simple (were)", "would / could + base verb"], ["3  impossible past", "if + past perfect", "would / could + have + V3"]]
        tb = E.table(rows, [4.2, 3.9, 4.8], row_h=0.74, size=24, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 0.6, 0])
        rules = VGroup(T("never \"will\" or \"would\" in the if-clause", size=28, color=th.CORAL, weight="BOLD"), T("comma only when the if-clause comes first", size=26, color=th.MUTED)).arrange(DOWN, buff=0.2).move_to([0, -2.3, 0])
        with self.say("The four patterns. Type zero, a general truth: if plus present simple, and present simple. Type one, real or likely: if plus present simple, and will, can or may plus the base verb. Type two, unreal now: if plus past simple, with were for every person, and would, could or might. Type three, the impossible past: if plus past perfect, and would have plus the past participle. Two rules hold for all four: never will or would in the if clause; and a comma only when the if clause comes first.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(rules))
        self.play(FadeOut(VGroup(h, tb, rules)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "The four types in detail")
        sc = reality_scale(y=1.25)
        blocks = [
            (0, ["If you mix blue and yellow, you get green.", "If water falls below zero, it freezes."], "a fact; \"if\" = \"when\""),
            (1, ["If you work hard, you will pass.", "If she calls, tell her I'm out."], "a real possibility"),
            (2, ["If I knew his number, I would ring him.", "If I were you, I would apologise."], "past form, no past meaning: a signal of unreality"),
            (3, ["If she had revised, she would have scored better.", "If I had known you were ill, I would have visited you."], "it's over; nothing can change it")]
        def block(t_, exs, note):
            g = VGroup(*[T(e_, size=30, color=TYPE_COL[t_]) for e_ in exs], T(note, size=24, color=th.MUTED)).arrange(DOWN, buff=0.35).move_to([0, -1.3, 0])
            for m_ in g:
                if m_.width > 12.4:
                    m_.scale_to_fit_width(12.4)
            return g

        dot = Dot([sc.xs[0], 1.25, 0], radius=0.14, color=WHITE)
        cur = block(*blocks[0])
        with self.say("In detail. Type zero states a fact that is always true, and if can be replaced by when: if you mix blue and yellow, you get green."):
            self.play(FadeIn(h), FadeIn(sc), FadeIn(dot))
            self.play(FadeIn(cur))
        says = ["Type one is a real possibility in the present or future: if you work hard, you will pass. The main clause can even be an order: if she calls, tell her I'm out.",
                "Type two is untrue now, or very unlikely. The past tense here has no past meaning at all: it is a signal of unreality. If I knew his number, I would ring him, because I don't know it. If I were you, I would apologise: the fixed formula for advice.",
                "Type three is the impossible past: the condition was not met, and the time is finished. If she had revised, she would have scored better. If I had known you were ill, I would have visited you."]
        for (t_, exs, note), say in zip(blocks[1:], says):
            g = block(t_, exs, note)
            with self.say(say):
                self.play(FadeOut(cur), dot.animate.move_to([sc.xs[t_], 1.25, 0]), FadeIn(g))
            cur = g
        self.play(FadeOut(VGroup(h, sc, dot, cur)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Mixed conditionals: two different times")
        tl = Arrow([-6.0, 0.6, 0], [6.0, 0.6, 0], buff=0, color=th.MUTED, stroke_width=4)
        past = T("past", size=26, color=th.MUTED).move_to([-4.7, 0.25, 0])
        now = T("now", size=26, color=th.MUTED).move_to([4.7, 0.25, 0])
        a1 = CurvedArrow([-3.5, 0.9, 0], [3.5, 0.9, 0], angle=-PI / 4, color=th.AMBER)
        s1 = T("If I had studied medicine, I would be a doctor now.", size=30, color=th.AMBER).move_to([0, 2.4, 0])
        l1 = T("type 3 if-clause (past cause) + type 2 main clause (present result)", size=22, color=th.MUTED).next_to(s1, DOWN, buff=0.12)
        a2 = CurvedArrow([3.5, 0.3, 0], [-3.5, 0.3, 0], angle=-PI / 4, color=th.SKY)
        s2 = T("If he were honest, he would not have cheated in the test.", size=30, color=th.SKY).move_to([0, -1.6, 0])
        l2 = T("type 2 if-clause (present state) + type 3 main clause (past result)", size=22, color=th.MUTED).next_to(s2, DOWN, buff=0.12)
        with self.say("Real life does not always keep both clauses in one time. A mixed conditional takes each clause from a different type. If I had studied medicine, I would be a doctor now: a past cause, with the past perfect, and a present result, with would plus the base verb. And the other way round: if he were honest, he would not have cheated in the test: a present state, and a past result."):
            self.play(FadeIn(h), GrowArrow(tl), FadeIn(past), FadeIn(now))
            self.play(Create(a1), FadeIn(s1), FadeIn(l1))
            self.play(Create(a2), FadeIn(s2), FadeIn(l2))
        self.play(FadeOut(VGroup(h, tl, past, now, a1, s1, l1, a2, s2, l2)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Drop \"if\" and invert — three patterns only")
        rows = [["with if", "inverted"], ["If I were you …", "Were I you …"], ["If he had told me …", "Had he told me …"], ["If you should need help …", "Should you need help …"]]
        tb = E.table(rows, [5.2, 5.2], row_h=0.7, size=28, colors=[th.SKY, th.MINT]).move_to([0, 1.0, 0])
        nt = T("✗ If had I known …  — once \"if\" goes, it must not come back", size=26, color=th.CORAL).move_to([0, -1.2, 0])
        with self.say("In formal English you can drop if and move the auxiliary in front of the subject, in three patterns only. If I were you: were I you. If he had told me: had he told me. If you should need help: should you need help. And once if is gone, it must not come back: never if had I known."):
            self.play(FadeIn(h))
            E.reveal_table(self, tb, 5.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h2 = E.head(self, "Other conditional connectives")
        rows = [["connective", "means", "example"], ["unless", "if … not", "unless you work hard"], ["provided / as long as", "on one condition", "provided you return it"], ["in case", "a precaution — not \"if\"", "in case it rains"],
                ["even if", "the result holds anyway", "even if it rains"], ["but for", "if it hadn't been for", "But for your help, …"], ["otherwise", "if that doesn't happen", "Hurry, otherwise …"]]
        tb = E.table(rows, [3.8, 4.4, 4.6], row_h=0.64, size=24, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.1, 0])
        with self.say("Other conditional connectives. Unless means if not: you will fail unless you work hard. Provided that, and as long as, set one condition. In case is a precaution, not the same as if: take an umbrella in case it rains. Even if: the result holds anyway. But for, plus a noun, means if it had not been for: but for your help, I would have failed. And otherwise: hurry, otherwise you will be late.") as v:
            self.play(ReplacementTransform(h, h2))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h2, tb)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Four cases where will / would / should may follow if")
        cards = VGroup(
            E.card("willingness", "If you will wait here, I'll call the manager. (= be kind enough to)", th.SKY, w=6.1, h=2.2, size=24),
            E.card("insistence", "If you will eat so much sugar, expect toothache.", th.AMBER, w=6.1, h=2.2, size=24),
            E.card("remote chance: should / were to", "If you should meet him, give him my regards.", th.MINT, w=6.1, h=2.2, size=24),
            E.card("not a condition: if = whether", "I wonder if he will come. Ask her if she will join us.", th.PINK, w=6.1, h=2.2, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("The rule no will after if applies to conditions, and there are four recognised exceptions, so don't over correct. Willingness: if you will wait here, I'll call the manager. Insistence: if you will eat so much sugar, expect toothache. A remote chance, with should: if you should meet him, give him my regards. And when if means whether, after wonder or ask, it is not a condition at all: I wonder if he will come."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(VGroup(h, cards)))
        h = E.head(self, "The six errors examiners look for")
        pairs = [("If it will rain, we'll stay in.", "If it rains, we'll stay in."), ("If I would have known, I'd have come.", "If I had known, I'd have come."), ("If I was you, I'd accept.", "If I were you, I'd accept."),
                 ("Unless you don't hurry, you'll miss it.", "Unless you hurry, you'll miss it."), ("Take a coat in case it will be cold.", "Take a coat in case it is cold."), ("If he would be here, he'd help.", "If he were here, he'd help.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And the six errors. If it will rain: no will in the if clause, if it rains. If I would have known: had known. If I was you: were. Unless you don't hurry: unless already contains not. In case it will be cold: in case it is cold. And if he would be here: if he were here."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.1)
        self.play(FadeOut(VGroup(h, grid)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["pattern", "meaning", "example"], ["wish + past simple / were", "regret about now", "I wish I knew the answer. I wish I were taller."], ["wish + past perfect", "regret about the past", "I wish I had listened to you."], ["wish + would", "annoyance; wish for change", "I wish you would stop shouting."],
                ["if only", "the same, stronger", "If only I had known earlier!"], ["It is (high) time + past", "something overdue", "It is high time we left."], ["as if + past", "an untrue comparison", "He talks as if he knew everything."]]
        tb = E.table(rows, [4.4, 3.6, 4.8], row_h=0.64, size=22, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.4, 0])
        nt = T("✗ I wish I would have gone. → ✓ I wish I had gone.   ✗ It is time we go. → ✓ It is time we went.", size=24, color=th.CORAL).move_to([0, -2.5, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Wish and if only behave like a type two or type three if clause: the tense goes one step back to show the thing is not so. I wish I knew the answer: I don't. I wish I had listened to you: I didn't. I wish you would stop shouting: annoyance. If only I had known earlier. It is high time we left: something overdue, with the past. And he talks as if he knew everything. So never I wish I would have gone, but I wish I had gone; and it is time we went, not go.") as v:
            E.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = E.head(self, "Worked item: choose the type")
        rows = [["sentence", "type", "answer"], ["If you (boil) water, it (turn) into steam.", "0", "boil … turns"], ["If she (come) tomorrow, I (meet) her.", "1", "comes … will meet"], ["If I (be) the mayor, I (ban) plastic bags.", "2", "were … would ban"], ["If they (start) earlier, they (reach) the summit. (it failed)", "3", "had started … would have reached"]]
        tb = E.table(rows, [6.4, 1.2, 4.6], row_h=0.8, size=22, colors=[th.INK, th.AMBER, th.MINT]).move_to([0, 0.4, 0])
        nt = T("Ask how real each condition is — the type follows.", size=26, color=th.SKY).move_to([0, -2.3, 0])
        with self.say("A worked item. If you boil water, it turns into steam: a scientific fact, type zero. If she comes tomorrow, I will meet her: a real future, type one. If I were the mayor, I would ban plastic bags: I am not, type two. If they had started earlier, they would have reached the summit: the climb failed yesterday, type three. Ask how real each condition is, and the type follows.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))
        self.quiz("\"If I ____ you, I would accept the offer.\"",
                  ["was", "were", "am", "would be"], 1,
                  "Pause and think.",
                  "Type 2, the fixed advice formula: If I were you …")
        self.quiz("\"He missed the train, so he isn't here now.\" → If he hadn't missed the train, he ____ here now.",
                  ["would have been", "would be", "will be", "had been"], 1,
                  "One more.",
                  "A mixed conditional: past cause (had not missed), present result (would be … now).")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Type 0: present + present. Type 1: present + will.",
            "Type 2: past (were) + would. Type 3: had + V3 + would have + V3.",
            "Never will / would in the if-clause (except willingness, insistence, if = whether).",
            "Mixed: had studied … would be now. Inversion: Were I / Had he / Should you.",
            "Wish + past (now), wish + past perfect (past); it's time we went.",
        ], "Quick recap. How real is the condition. The four types. Mixed conditionals and inversion. Unless, in case and but for. And wish, if only, and it's high time.")
        self.outro("That was conditional sentences. Next: the passive voice. See you there.")
