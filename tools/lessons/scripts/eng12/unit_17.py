import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def floor_ceiling(ceiling=True, w=6.0, x=0.0, seed=1, top_rich=False):
    rng = np.random.default_rng(seed)
    n = 14
    hs = np.sort(rng.uniform(1.2, 3.0, n))
    if top_rich:
        hs[-1] = 3.4
    bars = VGroup(*[Rectangle(width=w / n * 0.8, height=h, stroke_width=0, fill_color=th.SKY, fill_opacity=0.7) for h in hs]).arrange(RIGHT, buff=w / n * 0.2, aligned_edge=DOWN)
    bars.move_to([x, -0.4, 0]).align_to(np.array([0, -2.6, 0]), DOWN)
    fl = Line([x - w / 2 - 0.2, -2.6 + 1.2, 0], [x + w / 2 + 0.2, -2.6 + 1.2, 0], color=th.MINT, stroke_width=5)
    g = VGroup(bars, fl)
    if ceiling:
        cl = DashedLine([x - w / 2 - 0.2, -2.6 + 3.2, 0], [x + w / 2 + 0.2, -2.6 + 3.2, 0], color=th.CORAL, stroke_width=5)
        g.add(cl)
    g.bars, g.floor = bars, fl
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 17
    TITLE = "Human Rights and the Age of Inequality"
    SUBTITLE = "Samuel Moyn · an essay"
    SECTIONS = ["Moyn and the question", "Floor and ceiling", "Croesus and the Declaration", "Welfare states, then markets", "Why not a new rights movement?", "Answering the exam"]
    NEXT = "Unit 18 · A Matter of Husbands"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = Axes(x_range=[1948, 2020, 10], y_range=[0, 10, 2], x_length=9.0, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-0.6, -0.2, 0])
        rights = ax.plot(lambda t: 1 + 7.5 / (1 + np.exp(-(t - 1985) / 8)), x_range=[1948, 2020], color=th.MINT, stroke_width=5)
        gap = ax.plot(lambda t: 3.2 - 1.0 / (1 + np.exp(-(t - 1960) / 5)) + 5.2 / (1 + np.exp(-(t - 1992) / 9)), x_range=[1948, 2020], color=th.CORAL, stroke_width=5)
        l1 = T("human rights spread", size=26, color=th.MINT).move_to(ax.c2p(1952, 9.4), aligned_edge=LEFT)
        l2 = T("gap between rich and poor", size=26, color=th.CORAL).move_to(ax.c2p(1952, 8.4), aligned_edge=LEFT)
        lab = VGroup(T("1948", size=22, color=th.MUTED).next_to(ax.c2p(1948, 0), DOWN, buff=0.15), T("today", size=22, color=th.MUTED).next_to(ax.c2p(2020, 0), DOWN, buff=0.15))
        with self.say("Since nineteen forty eight, human rights have spread round the world. Over the same years, especially since the nineteen seventies, the gap between the rich and the poor has grown wider. Both lines go up together. How can that be?"):
            self.play(Create(ax), FadeIn(lab))
            self.play(Create(rights), Create(gap), run_time=3)
            self.play(FadeIn(l1), FadeIn(l2))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, rights, gap, l1, l2, lab)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 17: Human Rights and the Age of Inequality, by Samuel Moyn."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Moyn and his question. Floor and ceiling. Croesus and the Universal Declaration. Welfare states, then markets. Why not a new rights movement? And how to answer the exam.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Samuel Moyn (born 1972)")
        facts = E.bullets(["American historian of law; professor at Yale", "The Last Utopia (2010): human rights as a movement are younger than we think", "Not Enough (2018): the book behind this essay", "the hardest essay in your book — it argues, it doesn't tell a story"], width=7.6, size=24).move_to([-2.3, 0.3, 0])
        key = E.card("the one sentence", "human rights are good at stopping state cruelty and setting a minimum — but they are not equipped to challenge inequality itself", th.AMBER, w=4.4, h=3.6, size=24).move_to([4.5, 0.2, 0])
        with self.say("Samuel Moyn is an American historian of law, a professor at Yale, known for re-telling the history of human rights with a sceptical eye. This essay comes from the argument of his book Not Enough. It is the hardest essay in your book, because it argues instead of telling a story. But every question comes back to one sentence: human rights are good at stopping state cruelty and guaranteeing a minimum, but they are not equipped to challenge inequality itself."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 8.0)
            self.play(FadeIn(key))
        self.play(FadeOut(VGroup(h, facts, key)))
        h = E.head(self, "What Moyn does NOT say")
        no = VGroup(*[T("✗  " + t_, size=28, color=th.CORAL) for t_ in ["human rights are bad", "human rights caused inequality"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 1.0, 0])
        yes = para("✓  human rights are the wrong tool for this job — they need a supplement, not a substitute", width=10, size=30, color=th.MINT).move_to([0, -1.1, 0])
        with self.say("Be careful. Moyn does not say human rights are bad, and he does not say they caused inequality. He says they are the wrong tool for this job, so the job needs a supplement, not a substitute."):
            self.play(FadeIn(h), FadeIn(no))
            self.play(FadeIn(yes))
        self.play(FadeOut(VGroup(h, no, yes)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Two kinds of equality")
        rows = [["", "status equality", "distributive equality"], ["means", "everyone counts as an equal person", "a fair share — a limit on the gap"], ["asks", "are you a full person in law?", "how much do you own, compared?"], ["in the UDHR?", "yes — Article 1", "no"], ["example", "ending slavery or caste discrimination", "taxes that narrow the gap"]]
        tb = E.table(rows, [2.6, 4.8, 4.8], row_h=0.68, size=24, colors=[th.AMBER, th.MINT, th.CORAL]).move_to([0, 0.4, 0])
        with self.say("Two phrases carry the whole essay. Status equality: everyone counts as an equal person, with the same dignity and legal rights, as in the Universal Declaration's first article; ending slavery or caste discrimination are examples. Distributive equality: everyone has a fair share, or at least there is a limit on how large the gap can grow, as when taxes narrow it. The Declaration has the first. It does not have the second.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h, tb)))
        h = E.head(self, "A floor, and a ceiling")
        a = floor_ceiling(ceiling=False, w=5.0, x=-3.3, seed=3, top_rich=True)
        b = floor_ceiling(ceiling=True, w=5.0, x=3.3, seed=3)
        la = VGroup(T("floor only", size=26, color=th.MINT, weight="BOLD"), T("everyone eats; a few own almost everything", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([-3.3, 1.95, 0])
        lb = VGroup(T("floor and ceiling", size=26, color=th.CORAL, weight="BOLD"), T("a minimum, and a limit on the top", size=22, color=th.BODY)).arrange(DOWN, buff=0.1).move_to([3.3, 1.95, 0])
        with self.say("Picture it as a floor and a ceiling. A floor of protection is the minimum everyone must be lifted to: food, basic health care, schooling. A ceiling on inequality is a limit on how far the top can pull away. A society can have a floor with no ceiling: everyone eats, but a few own almost everything. Moyn's point is that human rights give you the floor, and never mention the ceiling."):
            self.play(FadeIn(h), FadeIn(a), FadeIn(la))
            self.play(FadeIn(b), FadeIn(lb))
        self.play(FadeOut(VGroup(h, a, b, la, lb)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "We live in Croesus's world")
        c = E.card("Croesus", "king of Lydia, 6th century BC, so rich his name became a proverb: \"rich as Croesus\"", th.AMBER, w=5.0, h=2.6, size=24).move_to([-3.6, 0.8, 0])
        m = E.card("a modern Croesus", "fabulously rich, but kind: hates cruelty, lets nobody starve — a floor for all. Who could object?", th.SKY, w=6.4, h=2.6, size=24).move_to([2.9, 0.8, 0])
        nt = para("Moyn can: one man owning everything and treating everyone decently is still extreme inequality. Human rights fight repression and misery, but sit comfortably beside enormous wealth.", width=11.4, size=24, color=th.CORAL).move_to([0, -1.9, 0])
        with self.say("The essay opens with Croesus, the ancient king of Lydia, so rich that his name became a proverb. Imagine a modern Croesus: fabulously wealthy, but kind. He hates cruelty and insists that nobody in his kingdom starve. Who could object? Moyn can. A world where one man owns everything and treats everyone decently is still a world of extreme inequality. And that, he says, is our world: human rights fight repression and misery, but sit comfortably beside enormous wealth."):
            self.play(FadeIn(h), FadeIn(c))
            self.play(FadeIn(m))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(c, m, nt)))
        h2 = E.head(self, "The Universal Declaration, 10 December 1948")
        a = E.card("what it did", "Article 1: all are \"born free and equal in dignity and rights\". After racism and genocide, \"a revolutionary act\".", th.MINT, w=5.8, h=2.8, size=24).move_to([-3.2, 0.6, 0])
        b = E.card("what it left out", "any ceiling on the gap between rich and poor. Even the UN's poverty expert admits there is \"no explicitly stated right to equality\".", th.CORAL, w=5.8, h=2.8, size=24).move_to([3.2, 0.6, 0])
        q = para("\"one man owning everything — an absolute overlord — … would not violate the current scheme of human rights, so long as everyone had their basic rights fulfilled\"", width=11.4, size=24, color=th.AMBER).move_to([0, -2.0, 0])
        with self.say("Moyn is fair to the Universal Declaration of Human Rights, adopted on the tenth of December nineteen forty eight. Its first article announced status equality, everyone born free and equal in dignity and rights, and after racism and genocide that was revolutionary. But it implies nothing more. There is no ceiling on the wealth gap; even the UN's expert on poverty admits there is no explicitly stated right to equality. His thought experiment: one man could own everything, an absolute overlord, without violating human rights, so long as everyone's basic rights were met. Even perfectly realised human rights are compatible with radical inequality."):
            self.play(ReplacementTransform(h, h2), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(h2, a, b, q)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "How the ceiling was lost")
        tl = E.timeline(["1930s–40s: depression and war; the welfare state", "1944: Roosevelt — jobs, health, homes; end \"special privilege for the few\"", "1945 on: rights go global, but the ceiling stays national", "1970s: market fundamentalism (UK, US): welfare cut", "the floor goes global; the ceiling vanishes"], x0=-6.3, x1=6.3, y=0.2, colors=[th.SKY, th.MINT, th.AMBER, th.CORAL, th.PINK], size=22, wrap=2.5)
        with self.say("Then the history. After the depression of the nineteen thirties and the war, Western states built welfare states, protecting citizens from unemployment, sickness and old age. In nineteen forty four Franklin Roosevelt called for a second bill of rights: jobs, health, housing, education. People remember freedom from want, the floor. But Roosevelt's highest promise was to end special privilege for the few: a ceiling. That pairing worked only inside rich nations. When rights went global, the demand for equality at home was dropped. Then from the nineteen seventies, starting in Britain and America, governments turned to market fundamentalism and cut welfare. The floor went global; the ceiling vanished."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.8), run_time=12)
        self.play(FadeOut(VGroup(h, tl)))
        h = E.head(self, "1974: one Nobel Prize, two economists")
        a = E.card("Gunnar Myrdal", "believed the welfare idea could go worldwide — forgotten", th.SKY, w=5.4, h=2.4, size=26).move_to([-3.2, 0.6, 0])
        b = E.card("Friedrich Hayek", "the free-market thinker — \"saw his fondest wishes come true\"", th.CORAL, w=5.4, h=2.4, size=26).move_to([3.2, 0.6, 0])
        nt = para("The human rights movement adapted: it prized the individual's freedom from harm and a minimal state — and forgot the ceiling.", width=11, size=26, color=th.AMBER).move_to([0, -2.0, 0])
        with self.say("An irony Moyn enjoys: in nineteen seventy four the Nobel Prize in economics was shared by Gunnar Myrdal, who believed the welfare idea could go worldwide, and Friedrich Hayek, the champion of free markets. One was forgotten; the other saw his fondest wishes come true. The human rights movement adapted to the new climate, prizing freedom from harm and a minimal state, and the ceiling was forgotten."):
            self.play(FadeIn(h), FadeIn(a), FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "A new rights movement? \"I doubt it.\"")
        reasons = VGroup(*[E.card(a_, b_, c_, w=3.9, h=3.0, tsize=28, size=26) for a_, b_, c_ in [("1 · history", "inequality was curbed by strong states, taxes and movements — not individual rights", th.SKY), ("2 · the tools", "naming and shaming stops torture — not wealth", th.AMBER), ("3 · the agents", "the movement offers \"no serious threat\" to market fundamentalism", th.CORAL)]]).arrange(RIGHT, buff=0.3).move_to([0, 0.1, 0])
        with self.say("Could a new kind of human rights movement fix this? Moyn says: I doubt it, and gives three reasons. History: when inequality was contained, it was by strong states, taxes and organised political movements, not by individual rights. The tools: naming and shaming works against a government that tortures, but not against the rich for having too much. And the agents: the movement offers no serious threat to market fundamentalism."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in reasons], lag_ratio=0.5), run_time=4)
        self.play(FadeOut(reasons))
        hammer = VGroup(Rectangle(width=1.4, height=0.5, stroke_width=0, fill_color=th.MUTED, fill_opacity=1), Rectangle(width=0.2, height=1.8, stroke_width=0, fill_color="#8A5A33", fill_opacity=1).shift(DOWN * 1.1)).move_to([-4.0, 0.2, 0])
        q = E.quote("lacking anything but a hammer, … treats everything like a nail", "Moyn's closing image", width=6.8, size=30).move_to([1.8, 0.8, 0])
        nt = para("\"Neoliberalism, not human rights, is to blame for neoliberalism.\" Keep human rights for what they do well — and build other tools for inequality.", width=11, size=26, color=th.MINT).move_to([0, -2.1, 0])
        with self.say("He also heads off a misreading: it is foolish, he says, to blame human rights for the explosion of inequality. In his blunt formula, neoliberalism, not human rights, is to blame for neoliberalism. His closing image is the man who, having nothing but a hammer, treats everything like a nail. Human rights are so successful that people use them for every problem. Keep them for what they do well, and build other tools for inequality."):
            self.play(FadeIn(hammer), FadeIn(q))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, hammer, q, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "How to answer")
        rows = [["question", "answer in a sentence"], ["Who is Moyn?", "a Yale historian of law, critic of the history of human rights"], ["status vs distributive equality?", "equal persons vs a limit on the gap"], ["what does the UDHR lack?", "any ceiling on inequality"],
                ["Croesus?", "a kind, rich ruler: decency beside extreme inequality"], ["his conclusion?", "rights are the wrong tool; a supplement, not a substitute"]]
        tb = E.table(rows, [4.6, 7.6], row_h=0.66, size=24, colors=[th.AMBER, th.INK]).move_to([0, 0.4, 0])
        with self.say("For the exam. Who is Moyn: a Yale historian of law, critical of the history of human rights. Status against distributive equality: equal persons, against a limit on the gap. What the Declaration lacks: any ceiling on inequality. Croesus: decency beside extreme inequality. His conclusion: human rights are the wrong tool for inequality; they need a supplement, not a substitute.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h, tb)))
        self.quiz("In Moyn's terms, human rights mainly provide",
                  ["a ceiling on wealth", "a floor of protection", "equal incomes", "free markets"], 1,
                  "Pause and think.",
                  "A floor — a decent minimum — but no ceiling on how far the top can rise.")
        self.quiz("Does Moyn blame human rights for growing inequality?",
                  ["yes, entirely", "no — he blames neoliberalism; rights are just the wrong tool", "yes, partly", "he doesn't discuss it"], 1,
                  "One more.",
                  "\"Neoliberalism, not human rights, is to blame for neoliberalism.\"")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Samuel Moyn (b. 1972), Yale; rights spread while inequality grew — why?",
            "Status equality (in the UDHR) vs distributive equality (missing).",
            "A floor of protection, but no ceiling; we live in Croesus's world.",
            "Welfare states once had both; from the 1970s the ceiling vanished.",
            "Rights are the wrong tool for inequality: a supplement, not a substitute.",
        ], "Quick recap. Moyn's question. Status against distributive equality. A floor without a ceiling, and the world of Croesus. How the ceiling was lost. And why we need other tools, not fewer rights.")
        self.outro("That completes the essays. Next, the one act plays, starting with A Matter of Husbands. See you there.")
