import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def stage(w=11.0, h=4.4):
    floor = Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], color=th.MUTED, stroke_width=4)
    curtL = Polygon([-w / 2, h / 2, 0], [-w / 2 + 0.9, h / 2, 0], [-w / 2 + 0.5, -h / 2, 0], [-w / 2, -h / 2, 0], stroke_width=0, fill_color="#7A1F2B", fill_opacity=0.9)
    curtR = curtL.copy().flip(UP).move_to([w / 2 - 0.35, 0, 0])
    door = VGroup(Rectangle(width=1.4, height=2.6, stroke_color=th.PINK, stroke_width=3), *[Line([-0.7 + 0.2 * k, 1.3, 0], [-0.7 + 0.2 * k, -1.3, 0], color=th.PINK, stroke_width=2).set_opacity(0.5) for k in range(1, 7)]).move_to([w / 2 - 1.9, -h / 2 + 1.3, 0])
    dl = T("boudoir", size=22, color=th.PINK).next_to(door, UP, buff=0.15)
    return VGroup(floor, curtL, curtR, door, dl)


def woman(color, x, label=None):
    g = VGroup(Circle(radius=0.28, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4), Polygon([-0.35, -0.3, 0], [0.35, -0.3, 0], [0.55, -1.6, 0], [-0.55, -1.6, 0], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25))
    g.arrange(DOWN, buff=0.02).move_to([x, -0.9, 0])
    if label:
        g.add(T(label, size=22, color=color).next_to(g, DOWN, buff=0.15))
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 18
    TITLE = "A Matter of Husbands"
    SUBTITLE = "Ferenc Molnár · a one-act play"
    SECTIONS = ["Molnár and the one-act play", "The plea", "The actress's \"theory\"", "The twist", "Characters", "Themes and devices"]
    NEXT = "Unit 19 · Facing Death"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        st = stage().move_to([0, -0.2, 0])
        wife = woman(th.SKY, -3.2)
        act = woman(th.AMBER, 0.4)
        q = T("\"Give me back my husband!\"", size=34, color=th.SKY, weight="BOLD").move_to([0, 2.6, 0])
        with self.say("A young wife sits on the edge of a gilt chair in a famous actress's drawing room, still in her hat and furs, as if ready to run. The actress enters, and the wife says: give me back my husband!"):
            self.play(FadeIn(st), FadeIn(wife))
            self.play(FadeIn(act), FadeIn(q))
        with self.say("A few minutes later the wife leaves happy, grateful, and kissing the actress goodbye. Then the actress turns to that curtained door. Keep your eye on it."):
            self.play(Indicate(st[3], color=th.PINK), run_time=1.5)
            nb = E.neby_in(self, "wink", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(st, wife, act, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 18: A Matter of Husbands, a one act comedy by the Hungarian playwright Ferenc Molnár."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Molnár and the one act play. The plea. The actress's theory. The twist. The characters. And the themes and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Ferenc Molnár (1878–1952)")
        facts = E.bullets(["Hungary's most celebrated playwright; born in Budapest", "law student, then journalist", "The Paul Street Boys (1906); plays: The Devil, Liliom (later the musical Carousel), The Swan", "left Europe in 1940; died in New York", "witty drawing-room comedies — often compared with Wilde and Shaw"], width=7.8, size=24).move_to([-2.2, 0.2, 0])
        with self.say("Ferenc Molnár was Hungary's most celebrated playwright, born in Budapest in eighteen seventy eight. He studied law, became a journalist, and made his name with the novel The Paul Street Boys and plays like Liliom, later the musical Carousel. Jewish, he left Europe in nineteen forty and died in New York. He wrote witty, sophisticated drawing room comedies, and is often compared with Oscar Wilde and Bernard Shaw."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
        self.play(FadeOut(VGroup(h, facts)))
        rows = [["term", "meaning", "here"], ["one-act play", "no act breaks, one setting, continuous time", "one drawing room, one afternoon"], ["duologue", "only two speaking parts", "the two women"], ["stage directions", "notes on tone and gesture", "\"regards her appraisingly\""],
                ["twist ending", "a final surprise that changes everything", "the last line"], ["play within a play", "a character stages a performance", "the actress's \"comedy\" story"]]
        tb = E.table(rows, [2.9, 5.0, 4.6], row_h=0.64, size=22, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.2, 0])
        with self.say("Five terms to use. It is a one act play: one room, one continuous afternoon. A duologue: only two speaking parts. Its stage directions carry tone and gesture. It ends with a twist. And it contains a play within a play: the actress's own performance.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Beats 1–4: plea, denial, evidence, outburst")
        beats = [("the plea", "\"Give me back my husband!\" — Alfred, a blond, bespectacled lawyer", th.SKY), ("the denial", "she knows him only as the lawyer who drew up her contract; \"He never sent me a flower in all his life\"", th.AMBER),
                 ("the evidence", "flowers twice a week, charged to his account; a letter; a lock of hair", th.CORAL), ("the outburst", "sobbing: the actress has cosmetics, bright lights, \"Mr. Shakespeare\"'s lines — she has nothing", th.PINK)]
        cards = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.6, tsize=28, size=24) for a_, b_, c_ in beats]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        with self.say("The play has no scenes, so we follow its beats. The plea: give me back my husband, Alfred, a blond, bespectacled lawyer. The denial: the actress knows him only as the lawyer who drew up her contract; he never sent her a flower in his life. The evidence: the wife learned at the florist that Alfred sends flowers twice a week, charged to his account; there is a letter, and a lock of hair. Then the outburst: sobbing, the wife says the actress has cosmetics, bright lights and an author's lines to make her beautiful, while she has nothing."):
            self.play(FadeIn(h))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.6)
                self.hold(3.0)
        self.play(FadeOut(VGroup(h, cards)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "\"This is a very interesting case\"")
        q = E.quote("He is playing a little comedy to make you jealous.", "the Famous Actress", width=9.0, size=34).move_to([0, 1.4, 0])
        pts = E.bullets(["she studies the wife \"appraisingly\" — looking for an opening", "asks: were you affectionate once? getting on badly lately?", "then the theory: husbands do this to actresses \"endless times\"", "every clue becomes a trick: the flowers ordered and cancelled, the letter, the hair from a bribed hairdresser"], width=11.2, size=24).move_to([0, -1.2, 0])
        with self.say("Then the turn. The actress stops acting outraged and studies the wife appraisingly, like a practical person looking for an opening. This is a very interesting case, she says. Were you affectionate once? Getting on badly lately? Then her theory: your husband is playing a little comedy to make you jealous. It happens, she says, endless times to actresses. And every clue becomes part of the trick: the flowers were ordered and cancelled, the letter was planted, the lock of hair came from a bribed hairdresser."):
            self.play(FadeIn(h), FadeIn(q))
            E.reveal_list(self, pts, 11.0)
        self.play(FadeOut(VGroup(h, q, pts)))
        h = E.head(self, "Flattery mixed with pity")
        lines = VGroup(*[T(t_, size=28, color=c_) for t_, c_ in [("\"you foolish little woman\"", th.SKY), ("\"a cunning lawyer\" who adores you", th.AMBER), ("\"no man deserves to be adored as much as that\"", th.PINK), ("\"don't let him fool you like this again\"", th.MINT)]]).arrange(DOWN, buff=0.4).move_to([0, 0.4, 0])
        nt = para("She never tells a plain lie about the affair — she simply tells a better story. The wife leaves \"a perfect fool\", kissing her.", width=11, size=26, color=th.CORAL).move_to([0, -2.3, 0])
        with self.say("Her weapon is flattery mixed with pity. You foolish little woman. Your husband is a cunning lawyer who adores you. No man deserves to be adored as much as that. Don't let him fool you like this again. Notice that she never tells a plain lie about the affair; she simply tells a better story. The wife leaves happy, a perfect fool, kissing the actress goodbye."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.5))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, lines, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        st = stage().move_to([0, -0.2, 0])
        act = woman(th.AMBER, 1.6)
        q = T("\"All right, Alfred. You can come in now. She has gone.\"", size=30, color=th.PINK, weight="BOLD").move_to([0, 2.6, 0])
        q.scale_to_fit_width(min(q.width, 12.2))
        man = woman(th.MUTED, 3.6).set_opacity(0.6)
        with self.say("Alone, the actress walks to the curtained door of her boudoir and calls: All right, Alfred. You can come in now. She has gone. Curtain."):
            self.play(FadeIn(st), FadeIn(act))
            self.play(act.animate.move_to([2.6, -0.9, 0]))
            self.play(FadeIn(q))
            self.play(FadeIn(man, shift=LEFT * 0.3))
        self.play(FadeOut(VGroup(st, act, q, man)))
        h = E.head(self, "What the last line tells us")
        four = VGroup(*[E.card(f"{k + 1}", t_, c_, w=2.95, h=2.6, tsize=34, size=26) for k, (t_, c_) in enumerate([("the wife's fears were right", th.SKY), ("the actress knew he was listening", th.AMBER), ("the clues were real", th.CORAL), ("her \"comedy\" was her own", th.PINK)])]).arrange(RIGHT, buff=0.18).move_to([0, 0.3, 0])
        nt = para("Read it again: the clues were there — her calm, her careful questions, the curtained door.", width=11, size=26, color=th.MINT).move_to([0, -2.2, 0])
        with self.say("One line turns everything upside down. The wife's fears were right. The actress knew all along that Alfred was listening. The letter, the flowers and the lock of hair were exactly what they seemed. And the comedy she described so well was the comedy she had just performed. Read it again and the clues were there: her calm, her careful questions, and that curtained door."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(f_, shift=UP * 0.2) for f_ in four], lag_ratio=0.4))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, four, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Famous Actress", "poised, persuasive, amoral: she listens, denies, then improvises a better story", th.AMBER, w=4.0, h=3.4, tsize=26, size=26),
            E.card("Earnest Young Woman", "serious, sincere, truly grieving — and too trusting", th.SKY, w=4.0, h=3.4, tsize=24, size=26),
            E.card("Alfred", "never seen: sly, unfaithful, hiding in the next room", th.MUTED, w=4.0, h=3.4, tsize=26, size=26),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.2, 0])
        nt = para("No names for the women: they are types — a woman of the stage and a woman of ordinary life.", width=11, size=24, color=th.MUTED).move_to([0, -2.6, 0])
        with self.say("The characters. The Famous Actress is poised, quick witted and persuasive, and amoral: she feels no guilt. The play's humour depends on our admiring her skill while disapproving of how she uses it. The Earnest Young Woman is serious and sincere, rehearsed, plainly dressed, truly grieving, and too trusting. And Alfred is never seen: a sly, cowardly husband hiding in the next room. Notice that the women have no names. They are types: a woman of the stage and a woman of ordinary life."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(cards, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        cards = VGroup(
            E.card("Appearance and reality", "the truth is behind a curtain the whole time", th.SKY, w=6.1, h=2.4, size=24),
            E.card("Persuasion over proof", "the wife has real evidence; a good story beats it", th.AMBER, w=6.1, h=2.4, size=24),
            E.card("Acting off the stage", "she performs when no curtain has risen", th.PINK, w=6.1, h=2.4, size=24),
            E.card("Dramatic irony", "she leaves happier than she came — and more deceived", th.CORAL, w=6.1, h=2.4, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Appearance and reality: the truth sits behind a curtain the whole time. Persuasion over proof: the wife has real evidence, and a good story beats it. Acting off the stage: the actress performs even when no curtain has risen. And irony: the wronged wife leaves happier than she arrived, and more deceived."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(cards))
        rows = [["twist ending", "\"You can come in now.\"", "reverses the whole play"], ["dramatic irony", "the wife thanks the woman deceiving her", "we see more than she does"], ["play within a play", "the \"little comedy\" story", "acting inside acting"],
                ["stage directions", "\"regards her appraisingly\"", "reveal the actress thinking"], ["flattery", "\"no man deserves to be adored …\"", "persuasion's weapon"], ["symbol", "the curtained door", "the hidden truth"]]
        E.device_slide(self, rows, "Devices to quote. The twist ending. Dramatic irony, on a second reading. A play within a play. Stage directions that show the actress thinking. Flattery as a weapon. And the curtained door, a symbol of the hidden truth.", widths=(3.0, 5.4, 4.0), size=22)
        self.quiz("Where is Alfred during the conversation?",
                  ["at his office", "in the actress's boudoir, listening", "at home", "at the florist"], 1,
                  "Pause and think.",
                  "Behind the curtained door: \"All right, Alfred. You can come in now.\"")
        self.quiz("Why does the wife leave happy?",
                  ["Alfred apologised", "she believes it was a trick", "she found proof he was faithful", "she decided to divorce"], 1,
                  "One more.",
                  "The actress's \"little comedy\" theory turned every clue into a sign of love.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Ferenc Molnár (1878–1952), Hungarian; a one-act drawing-room comedy, a duologue.",
            "The plea, the denial, the evidence: flowers, a letter, a lock of hair.",
            "\"A little comedy to make you jealous\": flattery and pity turn every clue.",
            "Twist: \"All right, Alfred. You can come in now. She has gone.\"",
            "Themes: appearance vs reality, persuasion over proof, acting off the stage.",
        ], "Quick recap. Molnár's one act comedy. A wife's plea and her evidence. The actress's brilliant theory. And a last line that turns the whole play upside down.")
        self.outro("That was A Matter of Husbands. Next play: Facing Death. See you there.")
