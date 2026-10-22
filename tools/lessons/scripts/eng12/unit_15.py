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
    UNIT = 15
    TITLE = "Knowledge and Wisdom"
    SUBTITLE = "Bertrand Russell · an essay"
    SECTIONS = ["Russell and the problem", "A sense of proportion", "Ends, feeling and private life", "The tyranny of the here and now", "Can wisdom be taught?", "Why it is urgent"]
    NEXT = "Unit 16 · Humility"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 2], x_length=8, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_ticks": False}).move_to([-1.0, -0.2, 0])
        k = ax.plot(lambda x: 0.6 + 0.08 * x * x, x_range=[0, 10], color=th.SKY, stroke_width=5)
        w = ax.plot(lambda x: 0.6 + 0.12 * x, x_range=[0, 10], color=th.AMBER, stroke_width=5)
        lk = T("knowledge", size=26, color=th.SKY).next_to(ax.c2p(10, 8.6), RIGHT, buff=0.2)
        lw = T("wisdom", size=26, color=th.AMBER).next_to(ax.c2p(10, 1.8), RIGHT, buff=0.2)
        xl = T("1954 →", size=22, color=th.MUTED).next_to(ax.c2p(10, 0), DOWN, buff=0.2)
        with self.say("A student can know every treaty in the history book and still quarrel with a classmate for a year over a borrowed pen. A scientist can understand the atom perfectly and still build something that frightens the world. In nineteen fifty four, Bertrand Russell asked why our knowledge has grown so fast while our wisdom has not."):
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(k), Create(w), run_time=2.5)
            self.play(FadeIn(lk), FadeIn(lw))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, k, w, lk, lw, xl)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 15: Knowledge and Wisdom, by Bertrand Russell."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Russell and the problem. A sense of proportion. Ends, feeling and private life. The tyranny of the here and now. Can wisdom be taught? And why it is urgent.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Bertrand Russell (1872–1970)")
        facts = E.bullets(["mathematician and philosopher; with Whitehead, Principia Mathematica", "A History of Western Philosophy made philosophy readable for millions", "a pacifist, jailed in 1918; later a leading anti-nuclear campaigner", "Russell–Einstein Manifesto, 1955", "Nobel Prize in Literature, 1950"], width=7.8, size=24).move_to([-2.2, 0.2, 0])
        ctx = E.card("written in 1954", "nine years after Hiroshima and Nagasaki; the year of the US hydrogen-bomb test at Bikini Atoll", th.CORAL, w=4.2, h=3.0, size=24).move_to([4.5, 0.2, 0])
        with self.say("Bertrand Russell was a mathematician and philosopher, one of the founders of analytic philosophy, who wrote with Whitehead an attempt to build mathematics on pure logic. He was also a public figure who acted on his beliefs: a pacifist jailed in nineteen eighteen, and later a leader of the campaign against nuclear weapons. He won the Nobel Prize in Literature in nineteen fifty. He wrote this essay in nineteen fifty four, nine years after Hiroshima, in the year of a hydrogen bomb test. The atom was the perfect example of knowledge running ahead of wisdom."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(ctx))
        self.play(FadeOut(VGroup(h, facts, ctx)))
        h = E.head(self, "Knowledge vs wisdom")
        rows = [["", "knowledge", "wisdom (Russell)"], ["what", "information, skill, a specialist's grasp", "a comprehensive view of life"], ["where", "in the mind", "in mind and feeling"], ["risk", "can be misused", "guards against harm"], ["taught by", "instruction", "widening moral instruction"]]
        tb = E.table(rows, [2.2, 5.0, 5.0], row_h=0.66, size=24, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 0.6, 0])
        nt = para("Textbook shorthand: knowledge = acquiring information; wisdom = applying it well, learned through experience. Learn it — but use Russell's richer account in long answers.", width=11.2, size=24, color=th.MUTED).move_to([0, -2.3, 0])
        with self.say("Russell's problem: our age far surpasses all others in knowledge, with no matching increase in wisdom. But what is wisdom? Knowledge is information and skill. Wisdom, for Russell, is a comprehensive view of life, living in feeling as well as mind, and guarding against the harm knowledge can do. Your textbook's shorthand, wisdom as the practical application of knowledge, is worth learning, but in long answers use Russell's own account.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tb, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Factor 1: a sense of proportion")
        df = para("\"the capacity to take account of all the important factors in a problem and to attach to each its due weight\"", width=11, size=28, color=th.AMBER).move_to([0, 1.8, 0])
        a = E.card("the medical researcher", "lowers infant deaths across the world — and, unforeseen, food supplies fall short in the most populous regions", th.SKY, w=5.8, h=2.6, size=24).move_to([-3.2, -0.6, 0])
        b = E.card("the atom", "studied out of pure curiosity — and puts into \"powerful lunatics'\" hands the means of destroying the human race", th.CORAL, w=5.8, h=2.6, size=24).move_to([3.2, -0.6, 0])
        nt = T("not against science — against narrow vision", size=26, color=th.MINT).move_to([0, -2.6, 0])
        with self.say("The first factor of wisdom is a sense of proportion: the capacity to take account of all the important factors in a problem and give each its due weight. Specialisation makes this hard. A medical researcher, absorbed in his work, succeeds in lowering the infant death rate around the world, and the unforeseen result is that food supplies fall short in the most crowded regions. More striking still: a scientist studies the atom out of pure curiosity, and puts into the hands of powerful lunatics the means of destroying the human race. Russell is not against science. He is against narrow vision."):
            self.play(FadeIn(h), FadeIn(df))
            self.play(FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, df, a, b, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Factor 2: awareness of the ends of human life")
        hegel = E.card("Hegel", "a comprehensive philosophy of history — whose chief lesson was that Germany had led the world since 400 AD. A wide mind bent by national pride.", th.AMBER, w=6.0, h=3.0, size=24).move_to([-3.1, 0.4, 0])
        q = E.quote("men whose knowledge is wide but whose feelings are narrow … lack what I call wisdom", "Russell", width=5.2, size=28).move_to([3.4, 0.4, 0])
        with self.say("But comprehensiveness is not enough. Wisdom also needs awareness of the ends of human life: what life is for. Many historians did harm because they saw facts through their own passions. Hegel's philosophy of history was certainly comprehensive, yet its chief lesson was that Germany had been the leading nation since four hundred A D. So wisdom includes feeling: men whose knowledge is wide but whose feelings are narrow lack what Russell calls wisdom."):
            self.play(FadeIn(h), FadeIn(hegel))
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(hegel, q)))
        h2 = E.head(self, "Factor 3: freedom from personal prejudice — in private life too")
        stone = E.card("noble but impossible ends", "seekers of the philosopher's stone and the elixir of life: had they succeeded, a gift to mankind — \"their lives were wasted\"", th.PINK, w=5.8, h=3.0, size=24).move_to([-3.2, 0.3, 0])
        a = Dot([2.0, 0.6, 0], radius=0.25, color=th.SKY)
        b = Dot([4.6, 0.6, 0], radius=0.25, color=th.CORAL)
        la = VGroup(T("Mr A", size=24, color=th.SKY).next_to(a, UP, buff=0.15), T("Mr B", size=24, color=th.CORAL).next_to(b, UP, buff=0.15))
        lists = VGroup(T("an \"appalling list\" of B's vices", size=22, color=th.SKY).move_to([3.3, -0.4, 0]), T("an \"exactly similar list\" of A's", size=22, color=th.CORAL).move_to([3.3, -0.9, 0]))
        nt = para("Patiently show each that the other has \"only the normal share of human wickedness\" — and you have \"instilled some fragment of wisdom\".", width=5.8, size=22, color=th.MINT).move_to([3.3, -2.2, 0])
        with self.say("Wisdom is needed in private life too: in choosing ends, and in freedom from personal prejudice. Even a noble end can be unwise if it is impossible: those who spent their lives seeking the philosopher's stone and the elixir of life wasted them. Then a humble case: Mr A and Mr B hate each other. Ask A, and you get an appalling list of B's vices; ask B, an exactly similar list about A. Tell each what the other says, and at first the hatred grows. But with patience you may persuade each that the other has only the normal share of human wickedness, and then you have instilled some fragment of wisdom."):
            self.play(ReplacementTransform(h, h2), FadeIn(stone))
            self.play(FadeIn(a), FadeIn(b), FadeIn(la))
            self.play(FadeIn(lists))
            self.play(a.animate.shift(RIGHT * 0.6), b.animate.shift(LEFT * 0.6), FadeIn(nt))
        self.play(FadeOut(VGroup(h2, stone, a, b, la, lists, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "The essence: freedom from the here and now")
        c0 = np.array([-2.6, -0.4, 0])
        rings = VGroup(*[Circle(radius=r, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.08).move_to(c0) for r, c_ in [(2.8, th.MINT), (2.1, th.SKY), (1.45, th.AMBER), (0.8, th.PINK)]])
        labs = VGroup(*[T(t_, size=22, color=c_).move_to(c0 + UP * (r - 0.3)) for t_, c_, r in [("all humanity, all time", th.MINT, 2.8), ("nation", th.SKY, 2.1), ("family, friends", th.AMBER, 1.45), ("me", th.PINK, 0.8)]])
        labs[3].move_to(c0)
        txt = E.bullets(["our senses are egoistic: they start from our own bodies", "a baby feels only its own hunger", "growing up widens the circle", "complete impartiality is impossible — but \"a continual approach towards impartiality\" is wisdom growing", "two ways: know what is remote in time and space, and let it count in your feelings"], width=5.0, size=22).move_to([3.7, -0.4, 0])
        with self.say("Then the essence of wisdom: emancipation, as far as possible, from the tyranny of the here and now. Our senses are egoistic; sight and touch start from our own bodies, and our emotions start from ourselves. A baby feels only its own hunger. As we grow, the circle widens: family, nation, all humanity, all time. Nobody can be completely impartial, but a continual approach towards impartiality is growth in wisdom: by knowing things remote in time and space, and by giving them their due weight in our feelings."):
            self.play(FadeIn(h))
            for r_, l_ in zip(reversed(rings), reversed(labs)):
                self.play(GrowFromCenter(r_), FadeIn(l_), run_time=0.7)
            E.reveal_list(self, txt, 9.0)
        self.play(FadeOut(VGroup(h, rings, labs, txt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Can wisdom be taught? Yes")
        q = para("\"We are told on Sundays that we should love our neighbour as ourselves. On the other six days of the week, we are exhorted to hate.\"", width=11, size=28, color=th.AMBER).move_to([0, 1.6, 0])
        sam = E.card("the Good Samaritan", "made a foreigner the neighbour. We no longer hate Samaritans, so we miss the point: in 1954, read \"Communist\" or \"anti-Communist\" instead.", th.SKY, w=10.0, h=2.4, size=24).move_to([0, -1.0, 0])
        with self.say("Can wisdom be taught? Russell says yes, and that it should be an aim of education. We are told on Sundays to love our neighbour; on the other six days we are urged to hate. The parable of the Good Samaritan made a despised foreigner the neighbour, but nobody hates Samaritans any more, so we miss the point. To get it, Russell says, substitute Communist or anti Communist, the great hatred of the Cold War in nineteen fifty four."):
            self.play(FadeIn(h), FadeIn(q))
            self.play(FadeIn(sam))
        self.play(FadeOut(VGroup(q, sam)))
        q = T("\"Hatred of evil is itself a kind of bondage to evil.\"", size=32, color=th.CORAL, weight="BOLD").move_to([0, 1.8, 0])
        a = E.card("not hate …", "if you hate wrongdoers you become as harmful, and you won't change them. \"The way out is through understanding, not through hate.\"", th.MINT, w=5.8, h=2.8, size=24).move_to([-3.2, -0.3, 0])
        b = E.card("… but not non-resistance", "resist — with \"the greatest degree of understanding and the smallest degree of force\" that keeps the good safe", th.AMBER, w=5.8, h=2.8, size=24).move_to([3.2, -0.3, 0])
        with self.say("But surely it is right to hate those who do harm? Russell says no. Hatred of evil is itself a kind of bondage to evil: hate them, and you will probably become as harmful as they are, and you will not persuade them to change. The way out is through understanding, not hate. And he adds a precaution: this is not non resistance. Resist, but with the greatest understanding and the smallest force needed to protect what is good."):
            self.play(FadeIn(q))
            self.play(FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(q, a, b)))
        leaders = VGroup(*[E.card(n_, d_, c_, w=3.9, h=2.6, size=24) for n_, d_, c_ in [("Elizabeth I", "free from the religious fanaticism of her age — and effective", th.PINK), ("Henry IV of France", "the same, in a world of Protestant–Catholic fury", th.SKY), ("Abraham Lincoln", "\"conducted a great war without ever departing from … wisdom\"", th.AMBER)]]).arrange(RIGHT, buff=0.3).move_to([0, 0.0, 0])
        nt = T("Wisdom is not weakness.", size=30, color=th.MINT, weight="BOLD").move_to([0, -2.3, 0])
        with self.say("Is wisdom weak, then? History says not. Queen Elizabeth the First and Henry the Fourth of France lived among fanatics on both sides of a religious war, stayed free of the errors of their time, and were both beneficial and effective. Abraham Lincoln conducted a great war without ever departing from wisdom. Wisdom is not weakness."):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.2) for l_ in leaders], lag_ratio=0.4))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, leaders, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "How to teach it, and why now")
        pts = E.bullets(["give moral instruction a larger intellectual element", "point out the cost of hatred and narrow-mindedness while teaching knowledge", "set every specialism inside a wider survey of human activity", "even the best technicians should be good citizens — \"citizens of the world\""], width=11.2, size=26).move_to([0, 0.7, 0])
        q = para("\"With every increase of knowledge and skill, wisdom becomes more necessary\" — more power to realise our purposes means more capacity for evil, if the purposes are unwise.", width=11.2, size=26, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("How should it be taught? Give moral instruction a larger intellectual element. Point out the disastrous results of hatred and narrow mindedness in the course of teaching knowledge. Set every specialist skill inside a wider survey of human life. Even the best technicians should be good citizens, citizens of the world, not of a sect or nation. And the final argument: with every increase of knowledge and skill, wisdom becomes more necessary, because more power to realise our purposes means more capacity for evil, if our purposes are unwise. The world needs wisdom as it has never needed it before."):
            self.play(FadeIn(h))
            E.reveal_list(self, pts, 9.0)
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(h, pts, q)))
        self.quiz("What does Russell call the essence of wisdom?",
                  ["memorising facts", "emancipation from the tyranny of the here and now", "obedience to authority", "specialisation"], 1,
                  "Pause and think.",
                  "Freeing ourselves, as far as possible, from seeing everything from our own small place and moment.")
        self.quiz("Why does Russell mention Hegel?",
                  ["as a wise historian", "wide knowledge, narrow feeling", "to praise Germany", "as a scientist"], 1,
                  "One more.",
                  "Wide knowledge with narrow feeling is not wisdom.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Bertrand Russell (1872–1970), Nobel 1950; essay written 1954, the nuclear age.",
            "Knowledge has grown; wisdom has not. Wisdom = comprehensive vision, with feeling.",
            "Factors: proportion, awareness of ends, freedom from prejudice (Mr A and Mr B).",
            "Essence: emancipation from the tyranny of the here and now.",
            "It can be taught; hatred of evil is bondage to evil; more knowledge needs more wisdom.",
        ], "Quick recap. Russell in the nuclear age. Knowledge outrunning wisdom. Proportion, awareness of ends, and freedom from prejudice. The essence: escaping the here and now. And why, the more we know, the more wisdom we need.")
        self.outro("That was Knowledge and Wisdom. Next essay: Humility. See you there.")
