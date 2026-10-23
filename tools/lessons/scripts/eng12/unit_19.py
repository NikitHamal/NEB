import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def candle(lit=False, h=1.0):
    body = Rectangle(width=0.22, height=h, stroke_color=th.INK, stroke_width=2, fill_color="#F0E6C8", fill_opacity=0.9)
    g = VGroup(body)
    if lit:
        g.add(Ellipse(width=0.14, height=0.3, stroke_width=0, fill_color=th.AMBER, fill_opacity=1).next_to(body, UP, buff=0.02))
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 19
    TITLE = "Facing Death"
    SUBTITLE = "August Strindberg · a one-act play"
    SECTIONS = ["Strindberg and modern tragedy", "A ruined boarding house", "The quarrel", "The daughters' cruelty", "The plan, told in code", "Characters, themes, devices"]
    NEXT = "Unit 20 · The Bull"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        basket = VGroup(Arc(radius=0.8, start_angle=PI, angle=PI, color="#8A5A33", stroke_width=5), Line([-0.8, 0, 0], [0.8, 0, 0], color="#8A5A33", stroke_width=5), T("empty", size=22, color=th.MUTED).shift(DOWN * 0.35)).move_to([-5.4, 0.5, 0])
        bills = VGroup(*[VGroup(Rectangle(width=1.3, height=1.3, stroke_color=th.INK, stroke_width=2, fill_color=th.PANEL, fill_opacity=1), T(t_, size=22, color=th.CORAL).shift(UP * 0.35)) for t_ in ("baker", "butcher", "grocer")]).arrange(RIGHT, buff=0.35).move_to([-2.3, 0.7, 0])
        lab = T("no bread — three unpaid bills", size=26, color=th.CORAL).move_to([-3.6, -1.2, 0])
        cs = VGroup(*[candle() for _ in range(6)]).arrange(RIGHT, buff=0.2).move_to([3.0, 0.2, 0])
        cl = T("six candles in the package", size=26, color=th.AMBER).move_to([3.0, -1.2, 0])
        with self.say("A widowed innkeeper sits in the dining room of his failing Swiss boarding house. His errand boy comes back with no bread, only three unpaid bills: the baker, the butcher, the grocer. On the table there is a package of candles."):
            self.play(FadeIn(basket), FadeIn(bills), FadeIn(lab))
            self.play(FadeIn(cs), FadeIn(cl))
        nt = para("By the end of the morning he will have saved his daughters — and only one of them will understand how.", width=11, size=28, color=th.INK).move_to([0, -2.6, 0])
        with self.say("By the end of the morning he will have saved his three daughters from poverty, so quietly that only one of them understands how. Count those candles. One of them matters."):
            self.play(FadeIn(nt), cs[5].animate.set_color(th.AMBER))
            nb = E.neby_in(self, "sad", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(basket, bills, lab, cs, cl, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 19: Facing Death, a one act play by the Swedish dramatist August Strindberg."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Strindberg and modern tragedy. A ruined boarding house. The quarrel. The daughters' cruelty. The plan, told in code. And the characters, themes and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "August Strindberg (1849–1912)")
        facts = E.bullets(["Swedish; more than sixty plays", "Miss Julie, The Father: naturalism — people speak and act as in real life", "later dream-like plays (A Dream Play): a forerunner of expressionism", "lived near Lake Geneva in the 1880s — the setting of this play"], width=7.8, size=24).move_to([-2.2, 0.3, 0])
        with self.say("August Strindberg was Sweden's great dramatist, author of more than sixty plays. In Miss Julie and The Father he brought naturalism to the stage: characters who speak and behave as in real life, driven by psychology and circumstance, not melodrama. Later he wrote dream like plays that led towards expressionism. He lived by Lake Geneva in the eighteen eighties, and that is where this play is set."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 8.0)
        self.play(FadeOut(VGroup(h, facts)))
        rows = [["", "classical tragedy", "modern tragedy"], ["hero", "a king or general", "an ordinary person: an innkeeper"], ["cause", "fate, gods, a flaw of pride", "money, family, society"], ["language", "poetic", "everyday speech"], ["setting", "a palace, a battlefield", "a dining-room"], ["ending", "death, then order restored", "a private death; life goes on"]]
        tb = E.table(rows, [2.2, 4.6, 5.6], row_h=0.64, size=24, colors=[th.AMBER, th.MUTED, th.MINT]).move_to([0, 0.4, 0])
        with self.say("Your textbook calls this a modern tragedy. Compare it with the classical kind. The hero is not a king but an innkeeper. He is destroyed not by fate or the gods but by debt and his family. The language is everyday speech; the setting is a dining room; and the ending is a private death, after which life goes on.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "French Switzerland, the 1880s")
        lake = VGroup(Rectangle(width=6.0, height=1.2, stroke_width=0, fill_color="#2D5C8A", fill_opacity=0.6), *[Triangle(stroke_width=0, fill_color="#1E3D2A", fill_opacity=1).scale(0.35).stretch(2.2, 1).move_to([-2.4 + 0.5 * k, 0.9, 0]) for k in range(4)]).move_to([-3.2, 0.9, 0])
        ll = T("Lake Léman, seen over churchyard cypresses", size=22, color=th.MUTED).next_to(lake, DOWN, buff=0.2)
        facts = E.bullets(["Durand keeps a pension: a boarding house for tourists", "one tourist in two months; the railway went east instead", "debts everywhere — but he has paid the fire insurance (or no last mortgage)", "every object is a weapon: bread, bills, a rat-trap, milk, matches"], width=5.8, size=24).move_to([3.4, 0.2, 0])
        nt = para("Death is in the view from the start; money is the real plot.", width=6.0, size=24, color=th.AMBER).move_to([-3.2, -1.6, 0])
        with self.say("The setting: a dining room in French Switzerland in the eighteen eighties, with a view of Lake Léman over the cypress trees of a churchyard, so death is in the view from the start. Monsieur Durand keeps a boarding house for tourists, and it is failing: one tourist in two months, since the railway went east instead. Debts are everywhere. But, he tells his eldest daughter Adèle, he has paid the fire insurance. Remember that."):
            self.play(FadeIn(h), FadeIn(lake), FadeIn(ll))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, lake, ll, facts, nt)))
        h = E.head(self, "Movement 2: the lodger's offer")
        a = E.card("Antonio offers", "\"Allow me to stay a month longer and I will pay my bill in advance.\"", th.SKY, w=5.6, h=2.6, size=26).move_to([-3.2, 0.5, 0])
        b = E.card("Durand refuses", "\"Privation must come and teach my children to lead a different life.\"", th.AMBER, w=5.6, h=2.6, size=26).move_to([3.2, 0.5, 0])
        nt = para("Antonio's odd question — was he born in Switzerland? \"Uncertainly.\" A secret is coming.", width=11, size=26, color=th.MUTED).move_to([0, -2.0, 0])
        with self.say("Antonio, a young Italian lieutenant lodging in the house, offers to help: let me stay a month longer and pay in advance. Durand refuses: privation must come and teach my children to lead a different life. Then Antonio asks a strange question: were you born in Switzerland? Yes, says Durand, uncertainly. A secret is coming."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Movement 3: a kiss, and a dead mother's words")
        steps = E.bullets(["Antonio kisses Thérèse; Durand sees it from the doorway", "Thérèse denies it — then repeats what her dead mother told her:", "    he lies about being Swiss; he is a Frenchman — and a deserter", "Durand raises his stick; Antonio leaves: \"Keep my contempt — and my ten francs\"", "Durand flings a gold coin after him and breaks his stick in two"], width=11.4, size=26).move_to([0, 0.2, 0])
        with self.say("Then the quarrel. Antonio kisses the daughter Thérèse, and Durand sees it from the doorway. Thérèse denies it, and then throws at her father what her dead mother told her: that he lies about being Swiss, that he is really a Frenchman, and a deserter. Durand raises his stick at Antonio, who leaves with contempt. Durand flings a gold coin after him and breaks his stick in two."):
            self.play(FadeIn(h))
            E.reveal_list(self, steps, 11.0)
        self.play(FadeOut(VGroup(h, steps)))
        a = E.card("the dead mother", "never on stage, but the ghost of the play: a spendthrift and a storyteller who taught her children to despise their father", th.PINK, w=10.0, h=2.6, size=26).move_to([0, 0.5, 0])
        nt = para("Durand will not defend himself by speaking ill of her — even at the end.", width=10, size=26, color=th.AMBER).move_to([0, -1.8, 0])
        with self.say("The dead mother is never seen, but she is the ghost of the play: a spendthrift and a storyteller who taught her children to despise their father. And Durand refuses to defend himself by speaking ill of her, even at the end."):
            self.play(FadeIn(a))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Movement 4: milk for the cat, none for the father")
        items = VGroup(*[E.card(t_, d_, c_, w=3.9, h=2.4, size=24) for t_, d_, c_ in [("the milk", "Adèle brings him a glass; Thérèse snatches it away", th.SKY), ("the matches", "\"you sha'n't waste the matches\" — taken from him", th.AMBER), ("the mockery", "cream for the cat, none for the father; he eats the rats' bait", th.CORAL)]]).arrange(RIGHT, buff=0.25).move_to([0, 0.6, 0])
        q = para("\"a lone brakeman on an express train\" — he sees it heading for the abyss and cannot reach the brakes", width=11, size=26, color=th.MINT).move_to([0, -2.0, 0])
        with self.say("The cruelty grows small and sharp. Adèle brings him a glass of milk; Thérèse snatches it away. She takes his matches too: you shan't waste the matches. They mock him: there is cream for the cat but no milk for their father; he eats the rats' bait. Durand describes himself as a lone brakeman on an express train, watching it race towards an abyss, unable to reach the brakes. Outside, the wind begins to rise."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(i_, shift=UP * 0.2) for i_ in items], lag_ratio=0.4))
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(h, items, q)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Movement 5: farewells, and the truth in code")
        rows = [["he says", "it means"], ["\"Put out the fire in the stove.\"", "no fire of ours will be blamed"], ["\"Shut the windows upstairs.\"", "the house must burn well; send them away"], ["\"the sixth candle is placed very high up\"", "a fuse, burning down"], ["\"Hide the insurance papers.\"", "the money will rescue you"], ["\"I am going away to get money for you.\"", "literally true"]]
        tb = E.table(rows, [6.4, 5.8], row_h=0.64, size=24, colors=[th.AMBER, th.MINT]).move_to([0, 0.5, 0])
        with self.say("The last movement is a double story. On the surface, Durand sends his daughters upstairs to shut the windows. He is tender to Thérèse: if she loves Antonio, she must marry him; you gave me so much joy as a child that you owe me nothing. To Adèle alone he speaks in code. Put out the stove: no fire of ours will be blamed. Count the candles: five of six; the sixth is placed very high up, a fuse. Hide the insurance papers. I am going away to get money for you, which is literally true.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        cs = VGroup(*[candle(lit=(k == 5)) for k in range(6)]).arrange(RIGHT, buff=0.25).move_to([-3.6, 0.4, 0])
        cs[5].shift(UP * 1.2)
        smoke = VGroup(*[Circle(radius=0.3 + 0.1 * k, stroke_width=0, fill_color=th.MUTED, fill_opacity=0.25).move_to([2.6 + 0.4 * k, 2.4 - 0.1 * k, 0]) for k in range(5)])
        q = VGroup(T("\"You have — taken — poison!\"", size=30, color=th.CORAL, weight="BOLD"), T("\"Tell Thérèse — and Annette —\"", size=28, color=th.INK)).arrange(DOWN, buff=0.4).move_to([2.6, -0.4, 0])
        nt = para("Only Adèle understands. She becomes the keeper of the secret.", width=6, size=26, color=th.AMBER).move_to([2.6, -2.4, 0])
        with self.say("He tells Adèle the truth about his past, asks her to care for her sisters, forbids her to speak ill of their mother, and drinks from a glass. Smoke forces its way through the ceiling; bells ring in the distance. You have taken poison, Adèle cries. He nods, asks if she has the insurance papers, begins: tell Thérèse, and Annette, and his head falls. Curtain."):
            self.play(FadeIn(cs))
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.3) for s_ in smoke], lag_ratio=0.3), run_time=2)
            self.play(FadeIn(q))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, cs, smoke, q, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        cards = VGroup(
            E.card("Durand", "a modern tragic hero: gentle, proud, passive — and capable of total sacrifice. Silent about his wife's faults to the end.", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Adèle (27)", "works \"like Cinderella\"; bitter, practical — the only one who understands", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Thérèse and Annette (24)", "spoiled, mocking, loyal to their mother's lies; Thérèse capable of sudden tenderness", th.PINK, w=6.1, h=2.75, size=24),
            E.card("Antonio", "the kindly lodger whose kiss sets off the quarrel; leaves in contempt", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("The characters. Durand: gentle, proud, passive, and capable of total sacrifice, silent about his wife's faults to the end. Adèle, the eldest, who works in the kitchen like Cinderella, bitter and practical, and the only one who understands. Thérèse and Annette, spoiled and mocking, loyal to their mother's lies. And Antonio, the lodger whose kiss sets off the quarrel."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(cards))
        th3 = VGroup(*[E.card(t_, d_, c_, w=3.9, h=2.6, tsize=24, size=24) for t_, d_, c_ in [("love without thanks", "he gives everything; they give mockery", th.AMBER), ("a dead mother's lies", "they poison a family from the grave", th.PINK), ("death as an act of care", "his suicide is a gift, hidden", th.CORAL)]]).arrange(RIGHT, buff=0.25).move_to([0, 1.0, 0])
        dev = E.bullets(["naturalism: small real objects — bread, bills, milk, matches, a rat-trap", "symbols: the candles (a fuse), the broken stick (lost authority), the lake and churchyard", "dramatic irony: his coded words mean one thing to them, another to us", "foreshadowing: the fire insurance, the stove, \"everything crash at once\""], width=11.4, size=24).move_to([0, -1.7, 0])
        with self.say("Three themes: love without thanks; a dead mother's lies poisoning a family; and death as a deliberate act of care. And the devices: naturalism, built from small real objects; symbols, the candles as a fuse and the broken stick as lost authority; dramatic irony in his coded words; and foreshadowing from the very first scene, when he mentions the fire insurance and longs for everything to crash at once."):
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.2) for t_ in th3], lag_ratio=0.4))
            E.reveal_list(self, dev, 9.0)
        self.play(FadeOut(VGroup(th3, dev)))
        self.quiz("Why does Durand burn the house and take poison?",
                  ["out of anger at Antonio", "for the insurance money", "because he is a deserter", "to punish his daughters"], 1,
                  "Pause and think.",
                  "His death and the fire turn the insurance into his daughters' rescue: sacrifice, not revenge.")
        self.quiz("Why is \"Facing Death\" called a modern tragedy?",
                  ["it is set in the future", "an ordinary man is ruined", "it has five acts", "it ends happily"], 1,
                  "One more.",
                  "Ordinary hero, social and economic causes, plain language, a private death.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "August Strindberg (1849–1912): naturalism; a modern one-act tragedy.",
            "A failing boarding house: no bread, three bills — but the fire insurance is paid.",
            "A kiss, a quarrel, the dead mother's lies; milk and matches snatched away.",
            "The plan in code: the stove, the windows, the sixth candle, the papers.",
            "Poison and smoke: love without thanks; death as an act of care.",
        ], "Quick recap. Strindberg's modern tragedy. A ruined boarding house and a paid insurance policy. A family turned against its father. A plan told in code. And a death that is a hidden gift.")
        self.outro("That was Facing Death. Next, the last play: The Bull. See you there.")
