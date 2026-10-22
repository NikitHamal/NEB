import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def chunks(parts, colors, size=36, y=0.0, buff=0.3):
    g = VGroup(*[T(p_, size=size, color=c_) for p_, c_ in zip(parts, colors)]).arrange(RIGHT, buff=buff).move_to([0, y, 0])
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 29
    TITLE = "Passive Voice"
    SUBTITLE = "Grammar · be + past participle, in every tense"
    SECTIONS = ["Three moves", "Every tense", "Two objects, imperatives, make and let", "It is said that …; questions; prepositions", "Verbs with no passive; the errors", "Choosing the voice"]
    NEXT = "Unit 30 · Prepositions, Tenses and Relative Clauses"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        lines = VGroup(*[T(t_, size=36, color=th.INK) for t_ in ["My bicycle has been stolen.", "Rice is grown in the Terai.", "Applications must be submitted by Friday."]]).arrange(DOWN, buff=0.5).move_to([0, 0.8, 0])
        qs = VGroup(*[T(t_, size=24, color=th.AMBER).next_to(l_, RIGHT, buff=0.4) for t_, l_ in zip(["who? — unknown", "by farmers — obvious", "a rule for everyone"], lines)])
        with self.say("My bicycle has been stolen. Rice is grown in the Terai. Applications must be submitted by Friday. Who stole the bicycle? Nobody knows. Who grows the rice? Obviously, farmers. Who must submit? Everyone."):
            for l_ in lines:
                self.play(FadeIn(l_), run_time=0.6)
                self.hold(1.0)
            self.play(lines.animate.shift(LEFT * 1.7))
            for q_, l_ in zip(qs, lines):
                q_.next_to(l_, RIGHT, buff=0.4)
            self.play(LaggedStart(*[FadeIn(q_) for q_ in qs], lag_ratio=0.3))
        with self.say("That is the passive voice. It is not decoration. English uses it whenever the doer is unknown, obvious, unimportant or deliberately hidden, which is why notices, rules, reports and every formal letter you write need it."):
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(lines, qs)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 29: the passive voice."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. The three moves. The passive in every tense. Two objects, imperatives, make and let. It is said that, questions and prepositions. Verbs with no passive, and the errors. And choosing the voice.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Active → passive in three moves")
        act = chunks(["The gardener", "planted", "the roses."], [th.SKY, th.AMBER, th.MINT], y=1.4)
        labs = VGroup(*[T(t_, size=22, color=c_).next_to(m_, UP, buff=0.15) for t_, c_, m_ in zip(["subject (doer)", "verb", "object"], [th.SKY, th.AMBER, th.MINT], act)])
        pas = chunks(["The roses", "were planted", "by the gardener."], [th.MINT, th.AMBER, th.SKY], y=-0.4)
        steps = E.bullets(["1  the object becomes the subject", "2  the verb becomes be + past participle, be in the same tense", "3  the old subject becomes the agent with \"by\" — or is dropped"], width=11, size=26).move_to([0, -2.3, 0])
        with self.say("The active voice: the gardener planted the roses. The subject performs the action. To make it passive, three moves. One: the object becomes the new subject: the roses."):
            self.play(FadeIn(h), FadeIn(act), FadeIn(labs))
            self.play(TransformFromCopy(act[2], pas[0]), FadeIn(steps[0]))
        with self.say("Two: the verb becomes be plus the past participle, with be in the same tense as the active verb. Planted is simple past, so were planted. Three: the old subject becomes the agent, with by: by the gardener. The roses were planted by the gardener."):
            self.play(TransformFromCopy(act[1], pas[1]), FadeIn(steps[1]))
            self.play(TransformFromCopy(act[0], pas[2]), FadeIn(steps[2]))
        nt = para("Only a transitive verb — one with an object — can be made passive. Drop the agent when it is unknown, obvious or unimportant.", width=11, size=26, color=th.AMBER).move_to([0, -0.4, 0])
        with self.say("Only a verb that has an object, a transitive verb, can be made passive. And drop the agent whenever it is unknown, obvious or unimportant."):
            self.play(FadeOut(pas), FadeOut(steps), FadeIn(nt))
        self.play(FadeOut(VGroup(h, act, labs, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Be keeps the tense; the participle never changes")
        rows = [["tense", "active", "passive"], ["simple present", "He writes a letter.", "A letter is written."], ["present continuous", "He is writing a letter.", "A letter is being written."], ["present perfect", "He has written a letter.", "A letter has been written."], ["simple past", "He wrote a letter.", "A letter was written."],
                ["past continuous", "He was writing a letter.", "A letter was being written."], ["past perfect", "He had written a letter.", "A letter had been written."], ["future", "He will write a letter.", "A letter will be written."], ["modal", "He must write a letter.", "A letter must be written."], ["perfect modal", "He must have written it.", "It must have been written."]]
        tb = E.table(rows, [3.6, 4.4, 4.8], row_h=0.54, size=24, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, -0.2, 0])
        with self.say("The passive of every tense follows the same logic: be carries the tense, and the past participle never changes. He writes: a letter is written. He is writing: a letter is being written. He has written: has been written. He wrote: was written. He was writing: was being written. He had written: had been written. He will write: will be written. He must write: must be written. And he must have written: it must have been written.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        nt = VGroup(T("No ordinary passive for the perfect-continuous tenses or the future continuous:", size=26, color=th.INK), T("The mechanic has been repairing the car.  → leave it active", size=28, color=th.AMBER)).arrange(DOWN, buff=0.3).move_to([0, 0.4, 0])
        with self.say("Four tenses have no ordinary passive: the present perfect continuous, the past perfect continuous, the future continuous and the future perfect continuous. The mechanic has been repairing the car is simply left in the active."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Give, send, teach: two objects, two passives")
        rows = [["active", "person first (preferred)", "thing first"], ["They gave me a prize.", "I was given a prize.", "A prize was given to me."], ["He taught the boys English.", "The boys were taught English.", "English was taught to the boys."], ["She sent him a card.", "He was sent a card.", "A card was sent to him."]]
        tb = E.table(rows, [4.2, 4.2, 4.4], row_h=0.7, size=24, colors=[th.INK, th.MINT, th.SKY]).move_to([0, 0.7, 0])
        nt = T("buy, make, get, cook take \"for\": A watch was bought for his sister.", size=26, color=th.AMBER).move_to([0, -1.7, 0])
        with self.say("Verbs like give, send, offer, teach, tell, show and lend take two objects, a person and a thing, so they have two passives. They gave me a prize: I was given a prize, which English prefers, or a prize was given to me. He taught the boys English: the boys were taught English. And buy, make, get and cook take for: a watch was bought for his sister.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h2 = E.head(self, "Imperatives: let … be, or you are requested to")
        rows = [["active", "passive"], ["Open the door.", "Let the door be opened."], ["Do not touch the wires.", "Let not the wires be touched."], ["Please help the poor.", "You are requested to help the poor."], ["Work hard.", "You are advised to work hard."]]
        tb = E.table(rows, [4.0, 8.6], row_h=0.66, size=24, colors=[th.INK, th.MINT]).move_to([0, 0.6, 0])
        with self.say("Imperatives take let plus be: open the door becomes let the door be opened; and the negative, let not the wires be touched. Requests and advice become you are requested to, you are advised to: please help the poor, you are requested to help the poor.") as v:
            self.play(ReplacementTransform(h, h2))
            E.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(tb))
        h3 = E.head(self, "make, let, see, hear: the \"to\" comes back")
        rows = [["active", "passive"], ["They made him work overtime.", "He was made to work overtime."], ["They let him go.", "He was allowed to go."], ["I saw him enter the shop.", "He was seen to enter the shop."], ["We heard her sing.", "She was heard to sing."]]
        tb = E.table(rows, [6.2, 6.2], row_h=0.68, size=26, colors=[th.INK, th.MINT]).move_to([0, 0.5, 0])
        with self.say("Make, see, hear and help take a bare infinitive in the active, but in the passive the to comes back. They made him work overtime: he was made to work overtime. I saw him enter the shop: he was seen to enter the shop. And let becomes be allowed to: he was allowed to go.") as v:
            self.play(ReplacementTransform(h2, h3))
            E.reveal_table(self, tb, v.dur * 0.8)
        self.play(FadeOut(VGroup(h3, tb)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "It is said that … / She is said to …")
        tb = VGroup(E.card("People believe that she is innocent.", "It is believed that she is innocent.\nShe is believed to be innocent.", th.SKY, w=6.1, h=2.6, tsize=24, size=26),
                    E.card("They report that the bridge collapsed.", "It is reported that the bridge collapsed.\nThe bridge is reported to have collapsed.", th.MINT, w=6.1, h=2.6, tsize=24, size=26)).arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
        nt = T("past event → \"to have + past participle\": reported to have collapsed", size=26, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("Impersonal passives, the language of news and reports, have two routes. People believe that she is innocent: it is believed that she is innocent, or, she is believed to be innocent. They report that the bridge collapsed: it is reported that the bridge collapsed, or the bridge is reported to have collapsed. When the event is earlier, use to have plus the past participle.") as v:
            self.play(FadeIn(h), FadeIn(tb[0]))
            self.hold(v.dur * 0.3)
            self.play(FadeIn(tb[1]))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h2 = E.head(self, "Questions, and verbs that keep their preposition")
        q = VGroup(*[VGroup(T(a_, size=26, color=th.SKY), T("→", size=26, color=th.MUTED), T(b_, size=26, color=th.MINT)).arrange(RIGHT, buff=0.25) for a_, b_ in [("Did he write the letter?", "Was the letter written by him?"), ("Who broke the window?", "By whom was the window broken?"), ("Why did the police arrest him?", "Why was he arrested?")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.2, 0])
        p = VGroup(*[VGroup(T(a_, size=26, color=th.SKY), T("→", size=26, color=th.MUTED), T(b_, size=26, color=th.MINT)).arrange(RIGHT, buff=0.25) for a_, b_ in [("They laughed at him.", "He was laughed at."), ("Someone must look after the baby.", "The baby must be looked after."), ("They sent for the doctor.", "The doctor was sent for.")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.6, 0])
        for g_ in (q, p):
            g_.scale_to_fit_width(min(g_.width, 12.4))
        with self.say("Questions: convert first, then put the sentence back into question form. Did he write the letter: was the letter written by him? Who broke the window: by whom was the window broken? And prepositional verbs keep their preposition, even though its object has moved to the front. They laughed at him: he was laughed at. Someone must look after the baby: the baby must be looked after. They sent for the doctor: the doctor was sent for."):
            self.play(ReplacementTransform(h, h2))
            for r_ in q:
                self.play(FadeIn(r_), run_time=0.5)
                self.hold(1.4)
            for r_ in p:
                self.play(FadeIn(r_), run_time=0.5)
                self.hold(1.4)
        self.play(FadeOut(VGroup(h2, q, p)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Verbs that have no passive")
        cards = VGroup(
            E.card("intransitive", "come, go, die, sleep, arrive, happen, occur, rise, fall", th.SKY, w=3.95, h=2.6, size=24),
            E.card("stative", "have (= own), resemble, lack, suit, fit, cost, weigh", th.AMBER, w=3.95, h=2.6, size=24),
            E.card("reflexive objects", "He hurt himself. They know each other.", th.PINK, w=3.95, h=2.6, size=24),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.7, 0])
        nt = T("✗ The accident was happened at midnight.   ✗ This shirt is suited you.", size=26, color=th.CORAL).move_to([0, -1.6, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Some verbs have no passive at all. Intransitive verbs with no object: come, go, die, happen, occur. Stative verbs: have meaning own, resemble, lack, suit, cost. And reflexive objects: he hurt himself. So the accident was happened is wrong: the accident happened. And this shirt is suited you: this shirt suits you."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(cards, nt)))
        h2 = E.head(self, "Five passive errors")
        pairs = [("A letter has written by him.", "A letter has been written by him."), ("The window was broke.", "The window was broken."), ("He was died last year.", "He died last year."),
                 ("The matter was discussed about.", "The matter was discussed."), ("The letter was written by a pen.", "The letter was written with a pen.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("Five errors. A letter has written by him: be cannot be dropped, has been written. The window was broke: past participle, broken. He was died: die has no passive, he died. Discussed about: discuss takes no about. And by a pen: by names the doer, with names the instrument, so with a pen."):
            self.play(ReplacementTransform(h, h2))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.1)
        self.play(FadeOut(VGroup(h2, grid)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Active by default; passive for a reason")
        reasons = [("doer unknown", "My purse was stolen in the bus."), ("doer obvious", "The thief was arrested yesterday."), ("a process", "The leaves are plucked, dried and packed."), ("a rule or notice", "Phones must be switched off in the hall."),
                   ("the receiver is the topic", "The Dharahara was rebuilt after the earthquake."), ("impersonal, official", "It has been decided that the exam will be postponed.")]
        cards = VGroup(*[E.card(a_, b_, th.PALETTE[k % 8], w=4.0, h=2.0, tsize=26, size=22) for k, (a_, b_) in enumerate(reasons)]).arrange_in_grid(rows=2, cols=3, buff=(0.2, 0.25)).move_to([0, 0.3, 0])
        nt = para("Keep the agent only when it carries information: Hamlet was written by Shakespeare — but not \"the road was repaired by workers\".", width=11.4, size=24, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Changing voice is an exercise; choosing a voice is a skill, and your writing is marked on it. Use the active as your normal setting: it is shorter and clearer. Switch to the passive for a reason: the doer is unknown; obvious; unimportant, as in a process; a rule that applies to everyone; the receiver is the real topic; or the writer wants to be impersonal, as in official notices. And keep the agent only when it carries information: Hamlet was written by Shakespeare needs it; the road was repaired by workers does not."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=5)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, cards, nt)))
        h = E.head(self, "Worked item: a continuous tense, two objects")
        s = T("The principal was giving the students certificates.", size=32, color=th.INK).move_to([0, 1.8, 0])
        st = E.bullets(["verb: was giving — past continuous → was / were being + V3", "objects: the students (person), certificates (thing) — the person first", "the students is plural → were"], width=11, size=26).move_to([0, -0.1, 0])
        ans = T("The students were being given certificates by the principal.", size=30, color=th.MINT, weight="BOLD").move_to([0, -2.3, 0])
        ans.scale_to_fit_width(min(ans.width, 12.4))
        with self.say("A worked item. The principal was giving the students certificates. The verb was giving is past continuous, so the passive frame is was or were being plus the past participle. There are two objects; prefer the person, the students, as the new subject. Students is plural, so were. The students were being given certificates by the principal."):
            self.play(FadeIn(h), FadeIn(s))
            E.reveal_list(self, st, 8.0)
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(h, s, st, ans)))
        self.quiz("Passive of \"They are building a new bridge.\"",
                  ["A new bridge is built.", "A new bridge is being built.", "A new bridge has been built.", "A new bridge was being built."], 1,
                  "Pause and think.",
                  "Present continuous → is / are being + past participle.")
        self.quiz("Which sentence cannot be made passive?",
                  ["She wrote a poem.", "The accident happened at night.", "They sent for the doctor.", "He gave me a book."], 1,
                  "One more.",
                  "Happen is intransitive — no object, so no passive.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Object → subject; be (same tense) + V3; by + agent, or drop it.",
            "is being written, has been written, must have been written.",
            "Two objects: I was given a prize. Let the door be opened.",
            "He was made to work. It is said that … / She is said to …",
            "No passive: happen, die, resemble, suit. Passive for a reason.",
        ], "Quick recap. Three moves. Be carries the tense. Two objects, imperatives, and the to that comes back. Impersonal passives and prepositional verbs. And choosing the passive only for a reason.")
        self.outro("That was the passive voice. Next: prepositions, tenses and relative clauses. See you there.")
