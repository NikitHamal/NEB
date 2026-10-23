import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def door(label, color, sign, w=2.4, h=3.4):
    d = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.08)
    knob = Dot(radius=0.08, color=color).move_to(d.get_right() + LEFT * 0.35)
    s = T(sign, size=40, color=color, weight="BOLD").move_to(d.get_center() + UP * 0.4)
    l = T(label, size=28, color=color, weight="BOLD").next_to(d, DOWN, buff=0.25)
    return VGroup(d, knob, s, l)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 22
    TITLE = "Modal Verbs"
    SUBTITLE = "Grammar · can, could, may, might, will, would, shall, should, must"
    SECTIONS = ["Five rules that never change", "Nine modals, many meanings", "Ability, permission, obligation", "Advice and deduction", "Perfect modals: did it happen?", "Semi-modals and common mistakes"]
    NEXT = "Unit 23 · Determiners and Quantifiers"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a = E.wrong_right("He can able to speak Chinese.", "He can speak Chinese.", size=34).move_to([0, 1.2, 0])
        b = E.wrong_right("I must have to go now.", "I must go now.", size=34).move_to([0, -1.2, 0])
        with self.say("Two sentences you will hear every day in Nepal, and the examiner marks both wrong. He can able to speak Chinese. I must have to go now."):
            self.play(FadeIn(a.wrong), FadeIn(b.wrong))
        with self.say("Each one uses two helpers where English allows one. He can speak Chinese. I must go now. Modal verbs follow a few strict rules, and once you know them, the modal item in your exam is easy marks."):
            self.play(Create(a.cross), Create(b.cross))
            self.play(FadeIn(a.right, shift=UP * 0.15), FadeIn(b.right, shift=UP * 0.15))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 22: modal verbs."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Five rules that never change. Nine modals and their meanings. Ability, permission and obligation. Advice and deduction. Perfect modals, and whether the action happened. And semi modals with the common mistakes.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Modals comment on an action — and obey five rules")
        rules = [("1  no -s", "He cans swim.", "He can swim."), ("2  bare infinitive, no \"to\"", "She must to go.", "She must go."), ("3  no \"do\" in questions", "Does he can drive?", "Can he drive?"),
                 ("4  never two modals", "I will can help.", "I will be able to help."), ("5  no \"to can\", no \"canning\"", "I hope to can come.", "I hope to be able to come.")]
        rows = VGroup()
        for k, (t_, w_, r_) in enumerate(rules):
            y = 1.9 - 0.95 * k
            rows.add(VGroup(T(t_, size=24, color=th.AMBER, weight="BOLD").move_to([0, y, 0]).align_to(np.array([-6.5, 0, 0]), LEFT),
                            T("✗ " + w_, size=24, color=th.CORAL).move_to([0, y, 0]).align_to(np.array([-1.5, 0, 0]), LEFT),
                            T("✓ " + r_, size=24, color=th.MINT).move_to([0, y, 0]).align_to(np.array([2.3, 0, 0]), LEFT)))
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        rows.move_to([0, -0.1, 0])
        nt = T("only \"ought\" keeps \"to\": you ought to thank her", size=24, color=th.MUTED).move_to([0, -2.8, 0])
        with self.say("Can, could, may, might, will, would, shall, should and must do not describe an action; they comment on it: how possible, how necessary, how polite. And they obey five rules. One: no s in the third person: he can swim, not he cans. Two: a bare infinitive, without to: she must go. Only ought keeps to. Three: no do in questions or negatives: can he drive? Four: never two modals together: not will can, but will be able to. Five: no ing form and no participle; for those, use a semi modal like be able to."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=UP * 0.15), run_time=0.6)
                self.hold(2.2)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, rows, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["modal", "meanings", "example"], ["can", "ability, informal permission, possibility", "She can speak Maithili."], ["could", "past ability, polite request, possibility", "Could you lend me your notes?"], ["may", "formal permission, possibility (about 50 %)", "You may leave after the bell."],
                ["might", "weaker possibility, very polite request", "It might rain this evening."], ["will", "future, willingness, promise, habit", "I will carry your bag."], ["would", "polite offer, past habit, unreal situations", "Would you like some tea?"],
                ["shall", "offers and suggestions with I / we", "Shall I open the window?"], ["should", "advice, expectation, weaker duty", "You should see a doctor."], ["must", "strong obligation, deduction", "He must be over sixty."]]
        tb = E.table(rows, [1.9, 5.6, 5.0], row_h=0.56, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.2, 0])
        nt = T("Read the whole sentence, name the meaning you need, then choose the modal.", size=26, color=th.SKY).move_to([0, -3.0, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Each modal carries several meanings. Can: ability, informal permission, general possibility. Could: past ability and polite requests. May: formal permission, or about fifty per cent possibility. Might: a weaker possibility. Will: future, willingness, promise. Would: polite offers, past habits and unreal situations. Shall: offers and suggestions with I and we. Should: advice. Must: strong obligation, or a confident deduction. So the safe method in the exam: read the whole sentence, name the meaning you need, and only then choose the word.") as v:
            E.reveal_table(self, tb, v.dur * 0.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Ability: can, could, was able to")
        ex = VGroup(*[VGroup(T(a_, size=28, color=th.INK), T(b_, size=24, color=c_)).arrange(RIGHT, buff=0.4) for a_, b_, c_ in [
            ("Bishal can solve any sum in his head.", "present ability", th.SKY), ("At fourteen I could cycle to Bhairahawa.", "general past ability", th.SKY),
            ("After three attempts they were able to reach the summit.", "one particular success", th.MINT), ("Next year she will be able to drive.", "no two modals", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        ex.scale_to_fit_width(min(ex.width, 12.4))
        nt = T("✗ He can able to …   ✗ We could not able to …   — one or the other, never both", size=24, color=th.CORAL).move_to([0, -2.4, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Ability. Can for the present: Bishal can solve any sum in his head. Could for a general ability in the past: at fourteen I could cycle to Bhairahawa. But for one particular success on one occasion, use was able to: after three attempts they were able to reach the summit. And where a modal cannot go, after will for instance, use be able to. Never write can able to, or could not able to: use one or the other."):
            self.play(FadeIn(h))
            for e_ in ex:
                self.play(FadeIn(e_, shift=UP * 0.15), run_time=0.6)
                self.hold(1.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(ex, nt)))
        h2 = E.head(self, "Mustn't and needn't are opposites")
        a = door("mustn't", th.CORAL, "✗").move_to([-3.0, 0.4, 0])
        b = door("needn't", th.MINT, "free").move_to([3.0, 0.4, 0])
        la = para("You mustn't park here. — forbidden", width=4.8, size=26, color=th.CORAL).next_to(a, DOWN, buff=0.3)
        lb = para("You needn't come on Saturday. — no need", width=4.8, size=26, color=th.MINT).next_to(b, DOWN, buff=0.3)
        la.set_x(a.get_x())
        lb.set_x(b.get_x())
        with self.say("Permission: may I come in is formal; can I is informal; could I is polite. But learn this pair above all. Mustn't means it is forbidden: you mustn't park here. Needn't means there is no need; you are free: you needn't come on Saturday. Every year candidates write needn't where the sentence means forbidden."):
            self.play(ReplacementTransform(h, h2), FadeIn(a), FadeIn(b))
            self.play(FadeIn(la), FadeIn(lb))
        self.play(FadeOut(VGroup(a, b, la, lb)))
        h3 = E.head(self, "Obligation: must, have to, had to, should")
        cards = VGroup(
            E.card("must", "from inside, from the speaker: I must stop wasting time.", th.CORAL, w=3.9, h=2.6, size=24),
            E.card("have to", "from outside — rules, timetable: We have to wear the uniform.", th.SKY, w=3.9, h=2.6, size=24),
            E.card("had to", "the past of both. Must has no past: Yesterday I had to work late.", th.AMBER, w=3.9, h=2.6, size=24),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        nt = T("should / ought to: a weaker duty — A citizen ought to pay tax.", size=26, color=th.MINT).move_to([0, -2.0, 0])
        with self.say("Obligation. Must is felt from inside, or comes from the speaker: I must stop wasting time. Have to comes from outside, from rules or other people: we have to wear the college uniform. Had to is the past of both, because must has no past: yesterday I had to work late, never I must worked. And should, or ought to, is a weaker duty: a citizen ought to pay tax."):
            self.play(ReplacementTransform(h2, h3), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h3, cards, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Advice, from gentle to urgent")
        lad = VGroup(*[VGroup(E.chip(a_, c_, size=28), T(b_, size=26, color=th.INK)).arrange(RIGHT, buff=0.4) for a_, b_, c_ in [
            ("could / might", "You could try the evening class.", th.MUTED), ("should / ought to", "You should revise the whole unit.", th.SKY), ("had better", "You'd better leave now, or you'll miss the bus.", th.CORAL)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-0.4, 0.5, 0])
        arr = Arrow([-6.2, 1.6, 0], [-6.2, -0.8, 0], color=th.AMBER, buff=0)
        al = T("stronger", size=22, color=th.AMBER).next_to(arr, DOWN, buff=0.1)
        nt = para("\"Had better\" is for one occasion and hints at a bad result; negative: had better not. Preference: I'd rather walk than wait.", width=11, size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("Advice comes in strengths. Gentle: could, or might: you could try the evening class. Normal: should, or ought to: you should revise the whole unit. Urgent, about now: had better: you'd better leave now, or you'll miss the bus. Had better is about one occasion and hints at a bad result; its negative is had better not. And for preference, would rather: I'd rather walk than wait."):
            self.play(FadeIn(h), GrowArrow(arr), FadeIn(al))
            for l_ in lad:
                self.play(FadeIn(l_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(1.5)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, lad, arr, al, nt)))
        h = E.head(self, "Deduction: how sure are you?")
        bar = Rectangle(width=10.0, height=0.4, stroke_width=0).set_fill(color=[th.MINT, th.AMBER, th.CORAL], opacity=0.85).move_to([0, 0.9, 0])
        ticks = VGroup(*[VGroup(Line([x, 0.6, 0], [x, 1.2, 0], color=th.INK, stroke_width=3), T(t_, size=26, color=c_, weight="BOLD").move_to([x, 1.65, 0]), T(p_, size=22, color=th.MUTED).move_to([x, 0.2, 0])) for x, t_, c_, p_ in [(-4.8, "can't", th.CORAL, "0 %: impossible"), (0, "may / might / could", th.AMBER, "possible"), (4.8, "must", th.MINT, "certain")]])
        ex = VGroup(T("The lights are off; they must have gone out.", size=26, color=th.MINT), T("She may be in the library.", size=26, color=th.AMBER), T("He can't be in Jumla — I saw him in Kathmandu an hour ago.", size=26, color=th.CORAL)).arrange(DOWN, buff=0.25).move_to([0, -1.6, 0])
        ex.scale_to_fit_width(min(ex.width, 12.4))
        nt = T("The opposite of deductive \"must\" is \"can't\" — not \"mustn't\".", size=26, color=th.SKY).move_to([0, -3.0, 0])
        with self.say("Deduction is where the exam separates candidates, so picture a scale of certainty. Must: the only possible explanation. The lights are off; they must have gone out. May, might or could: one of several possibilities: she may be in the library. And can't: impossible. He can't be in Jumla; I saw him in Kathmandu an hour ago. Notice: the opposite of deductive must is can't, not mustn't."):
            self.play(FadeIn(h), FadeIn(bar), LaggedStart(*[FadeIn(t_) for t_ in ticks], lag_ratio=0.3))
            self.play(LaggedStart(*[FadeIn(e_) for e_ in ex], lag_ratio=0.5))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, bar, ticks, ex, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Modal + have + V3 talks about the past")
        rows = [["perfect modal", "meaning", "did it happen?"], ["must have + V3", "I am sure it happened", "yes"], ["can't / couldn't have + V3", "I am sure it did not", "no"], ["may / might have + V3", "possibly it happened", "unknown"],
                ["could have + V3", "it was possible, but didn't happen", "usually no"], ["should have + V3", "the right thing — not done", "no, a mistake"], ["shouldn't have + V3", "it was done, and wrong", "yes"], ["needn't have + V3", "done, but unnecessary", "yes"]]
        tb = E.table(rows, [4.6, 5.0, 2.8], row_h=0.6, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.4, 0])
        with self.say("A modal followed by have and the past participle talks about the past, and each one tells you whether the action happened. Must have: I'm sure it happened. Can't have: I'm sure it didn't. May or might have: possibly. Could have: it was possible, but it didn't happen. Should have: it was the right thing, and it wasn't done. Shouldn't have: it was done, and it was wrong. And needn't have: it was done, but it was unnecessary.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        a = E.card("needn't have taken", "I needn't have taken an umbrella — it didn't rain. (I took it: a waste.)", th.SKY, w=5.8, h=2.8, size=26).move_to([-3.2, 0.4, 0])
        b = E.card("didn't need to take", "I didn't need to take an umbrella, so I left it at home. (I didn't take it.)", th.AMBER, w=5.8, h=2.8, size=26).move_to([3.2, 0.4, 0])
        with self.say("The pair the board loves. I needn't have taken an umbrella: it didn't rain. I took it, and it was a waste. Compare: I didn't need to take an umbrella, so I left it at home. There was no need, so I didn't take it."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
        self.play(FadeOut(VGroup(h, a, b)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        rows = [["semi-modal", "meaning", "example"], ["have to / had to", "outside obligation", "I had to renew my licence."], ["be able to", "ability, all forms", "He has been able to walk since March."], ["be allowed to", "permission", "We were allowed to leave early."], ["used to", "a past habit, now stopped", "He used to smoke."],
                ["be supposed to", "what is expected", "You are supposed to wear a helmet."], ["need / dare", "necessity / courage", "You needn't shout. He dare not complain."]]
        tb = E.table(rows, [3.4, 3.8, 5.2], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.4, 0])
        nt = T("Not the same: I used to go (a past habit)  ·  I am used to going (accustomed)", size=24, color=th.SKY).move_to([0, -2.4, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Semi modals supply the forms the nine modals lack. Have to and had to for outside obligation. Be able to, in every tense. Be allowed to for permission. Used to for a past habit that has stopped: he used to smoke. Be supposed to, for what is expected. And need and dare. Careful with one pair: I used to go means a past habit; I am used to going means I am accustomed to it.") as v:
            E.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = E.head(self, "The mistakes the examiner looks for")
        pairs = [("I must have to go now.", "I must go now."), ("We should to respect our teachers.", "We should respect our teachers."), ("You had better to consult a doctor.", "You had better consult a doctor."),
                 ("Yesterday I must submit the form.", "Yesterday I had to submit the form."), ("May be he is at home.", "Maybe he is at home."), ("He mustn't worry; there's no hurry.", "He needn't worry; there's no hurry.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=24) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("The mistakes the examiner looks for. I must have to go: one obligation word only. We should to respect: no to after should. You had better to consult: had better takes the bare infinitive. Yesterday I must submit: must has no past, so had to. May be he is at home: the adverb is maybe, one word. And he mustn't worry, there's no hurry: that means forbidden; you need needn't."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.4)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.6)
                self.hold(1.4)
        self.play(FadeOut(VGroup(h, grid)))
        h = E.head(self, "Worked item: could or was able to?")
        s = para("The house was burning fiercely, but the fire brigade ____ rescue everyone inside.", width=11, size=30, color=th.INK).move_to([0, 1.6, 0])
        st = E.bullets(["meaning: ability in the past", "general ability, or one particular success? — one difficult occasion, and it succeeded", "so not \"could\" (general past ability) but \"was able to\" (or \"managed to\")"], width=11, size=26).move_to([0, -0.4, 0])
        ans = T("… the fire brigade was able to rescue everyone inside.", size=30, color=th.MINT, weight="BOLD").move_to([0, -2.5, 0])
        ans.scale_to_fit_width(min(ans.width, 12.4))
        with self.say("Exam style. The house was burning fiercely, but the fire brigade blank rescue everyone inside. The meaning is ability in the past. Is it a general ability, or one particular success? One difficult occasion, and it succeeded. So not could, but was able to: the fire brigade was able to rescue everyone inside."):
            self.play(FadeIn(h), FadeIn(s))
            E.reveal_list(self, st, 8.0)
            self.play(FadeIn(ans))
        self.play(FadeOut(VGroup(h, s, st, ans)))
        self.quiz("\"You ____ park here; it's a hospital gate.\" (forbidden)",
                  ["needn't", "mustn't", "don't have to", "may not have"], 1,
                  "Pause and think.",
                  "Mustn't forbids. Needn't and don't have to mean there is no need.")
        self.quiz("\"The ground is wet. It ____ last night.\" (I'm sure)",
                  ["must rain", "must have rained", "should have rained", "can't have rained"], 1,
                  "One more.",
                  "A confident deduction about the past: must have + past participle.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Modals: no -s, bare infinitive, no do, never two together.",
            "Name the meaning first: ability, permission, obligation, advice, deduction.",
            "Could = general past ability; was able to = one success.",
            "Mustn't = forbidden; needn't = no need; can't = the opposite of deductive must.",
            "Modal + have + V3 tells you whether a past action happened.",
        ], "Quick recap. The five rules. Name the meaning, then choose the modal. Could against was able to. Mustn't, needn't and can't. And perfect modals that tell you what really happened.")
        self.outro("That was modal verbs. Next: determiners and quantifiers. See you there.")
