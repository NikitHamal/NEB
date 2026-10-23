import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def feet_scene(label, color, tucked=False):
    """A seated father (circle head, bed) and two feet; tucked=True pulls the feet up under him."""
    bed = Rectangle(width=3.0, height=0.25, stroke_color=th.MUTED, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    body = RoundedRectangle(corner_radius=0.3, width=0.9, height=1.3, stroke_color=th.AMBER, stroke_width=3).next_to(bed, UP, buff=0).shift(LEFT * 0.6)
    headc = Circle(radius=0.32, stroke_color=th.AMBER, stroke_width=3).next_to(body, UP, buff=0.05)
    feet = VGroup(*[Ellipse(width=0.5, height=0.22, stroke_color=th.AMBER, stroke_width=3, fill_color=th.AMBER, fill_opacity=0.3) for _ in range(2)]).arrange(RIGHT, buff=0.05)
    if tucked:
        feet.next_to(body, RIGHT, buff=-0.25).align_to(bed, UP).shift(UP * 0.15)
    else:
        feet.next_to(bed, RIGHT, buff=0.15).shift(DOWN * 0.3)
    hand = VGroup(Line(ORIGIN, LEFT * 0.9, color=color, stroke_width=6), Dot(color=color, radius=0.1)).next_to(feet, RIGHT, buff=0.15 if not tucked else 0.9)
    lab = T(label, size=24, color=color).next_to(bed, DOWN, buff=0.7)
    return VGroup(bed, body, headc, feet, hand, lab)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 3
    TITLE = "A Devoted Son"
    SUBTITLE = "Anita Desai · a short story"
    SECTIONS = ["Anita Desai", "The rise", "The turn", "The characters", "Themes", "How it is built"]
    NEXT = "Unit 4 · The Treasure in the Forest"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a = feet_scene("the first morning: he touches his father's feet", th.MINT).move_to([-3.4, 0.0, 0])
        b = feet_scene("the last evening: the feet are tucked away", th.CORAL, tucked=True).move_to([3.4, 0.0, 0])
        with self.say("A young man comes first in the whole country in his medical exams. The first thing he does is touch his father's feet, and the whole neighbourhood praises him for it."):
            self.play(FadeIn(a))
        with self.say("Forty years later, the same son, now the richest doctor in town, reaches out to press his old father's feet. And the father tucks them away, out of reach. What happened in between?"):
            self.play(FadeIn(b))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 3: A Devoted Son, by the Indian writer Anita Desai."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Anita Desai. The son's rise. The turn, and the father's decline. The characters. The themes. And how the story is built: two halves, a shifting viewpoint, and irony.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Anita Desai (born 1937)")
        facts = E.bullets(["born in Mussoorie; German mother, Bengali father; grew up in Delhi", "German at home, Hindi outside — English became her \"literary language\"", "novels: Clear Light of Day, In Custody, Fasting, Feasting (all Booker-shortlisted)", "this story: from Games at Twilight (1978)", "her daughter Kiran Desai won the Booker in 2006"], width=7.6, size=24).move_to([-2.3, 0.2, 0])
        sub = VGroup(T("she writes about", size=26, color=th.AMBER, weight="BOLD"), *[para(t_, width=4.0, size=24, color=th.BODY) for t_ in ["the inner lives of families", "the quiet pressure of duty", "the gap between what people say and feel"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.2, 0])
        with self.say("Anita Desai, born in nineteen thirty seven, is one of India's leading writers in English. Her mother was German and her father Bengali; she grew up in Delhi speaking German at home and Hindi outside, and English became her literary language. Three of her novels were shortlisted for the Booker Prize. This story comes from her collection Games at Twilight, from nineteen seventy eight."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 7.0)
        with self.say("Her subject is the inner life of families: the quiet pressure of duty, and the gap between what people say and what they feel. This story is also funny, and then, halfway through, very bitter."):
            self.play(LaggedStart(*[FadeIn(s_) for s_ in sub], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, facts, sub)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "The great ascent")
        rungs = ["grandfather: sold vegetables", "Varma: 40 years at a kerosene depot", "Rakesh: first in the country", "an M.D. and a scholarship to \"the USA\"", "comes home; marries the girl his mother chose", "hospital director, then his own clinic", "the best, richest doctor in town"]
        cols = [th.MUTED, th.MUTED, th.MINT, th.SKY, th.AMBER, th.PINK, th.CORAL]
        steps = VGroup(*[E.chip(t_, c_, size=22) for t_, c_ in zip(rungs, cols)])
        for k, s_ in enumerate(steps):
            s_.move_to([-4.6 + 1.55 * k, -2.6 + 0.78 * k, 0])
            if s_.get_right()[0] > 6.7:
                s_.shift(LEFT * (s_.get_right()[0] - 6.7))
            if s_.get_left()[0] < -6.7:
                s_.shift(RIGHT * (-6.7 - s_.get_left()[0]))
        with self.say("The first half is a success story. Rakesh's grandfather sold vegetables; his father Varma worked forty years at a kerosene depot. Rakesh, the first in the family ever educated, comes first in the country in his exams. Neighbours crowd in with garlands and sweets, admiring, and a little envious. He wins a scholarship to the USA, which Varma proudly insists everyone call it, not America. Then, surprisingly, he comes home, touches his father's feet again, and marries the plump, placid village girl his mother chose, Veena. He becomes a hospital director, then opens his own clinic, and drives his parents there in a new sky blue Ambassador."):
            self.play(FadeIn(h))
            for s_ in steps:
                self.play(FadeIn(s_, shift=UP * 0.2), run_time=0.5)
                self.hold(0.9)
        sat = para("Satire: \"the USA\" — not America, which only ignorant neighbours say.", width=6.0, size=24, color=th.AMBER).move_to([-3.4, 2.0, 0])
        with self.say("Notice the narrator's tone here. It echoes the neighbours' own over the top praise, and it gently mocks the family's new snobberies, like the USA joke. It is warm, and it is satire."):
            self.play(FadeIn(sat))
        self.play(FadeOut(VGroup(h, steps, sat)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        q = E.quote("talent and skill, if displayed too long, cease to dazzle", "the hinge of the story", width=9.0, size=32).move_to([0, 0.6, 0])
        with self.say("Then comes the hinge. Talent and skill, Desai writes, if displayed too long, cease to dazzle. The tone cools. Varma has retired, his wife has died, and the old man goes to pieces."):
            self.play(FadeIn(q))
        self.play(FadeOut(q))
        h = E.head(self, "Everything he enjoys is crossed off")
        foods = VGroup(*[T(t_, size=30, color=th.AMBER) for t_ in ["soojie halwa and cream", "anything fried", "sweets", "jalebis from the crossroads", "fried fish he can smell"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, 0.0, 0])
        crosses = VGroup(*[Line(f_.get_left() + LEFT * 0.1, f_.get_right() + RIGHT * 0.1, color=th.CORAL, stroke_width=5) for f_ in foods])
        left = VGroup(T("what is left", size=26, color=th.MUTED, weight="BOLD"), *[T(t_, size=26, color=th.INK) for t_ in ["dry bread", "boiled lentils", "boiled vegetables", "cereal weighed on scales"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.0, 0])
        with self.say("Rakesh takes charge of his father's diet. After a bout of illness from halwa and cream, the famous doctor forbids anything rich. Fried food goes, then sweets, then everything the old man enjoys. Varma bribes his grandsons to buy him jalebis, and is caught; Rakesh warns of cholera and typhoid. What is left: dry bread, boiled lentils, boiled vegetables, and cereal weighed on scales."):
            self.play(FadeIn(h), FadeIn(foods))
            for c_ in crosses:
                self.play(Create(c_), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in left], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, foods, crosses, left)))
        h = E.head(self, "Food is replaced by tonics")
        pills = ["for the bowels", "for blood pressure", "for arthritis", "to keep his heart beating"]
        bottles = VGroup()
        for k, t_ in enumerate(pills):
            b_ = VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=1.5, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.15), Rectangle(width=0.45, height=0.3, stroke_color=th.SKY, stroke_width=3))
            b_[1].next_to(b_[0], UP, buff=0)
            bottles.add(VGroup(b_, para(t_, width=2.4, size=22, color=th.SKY).next_to(b_, DOWN, buff=0.2)))
        bottles.arrange(RIGHT, buff=0.7).move_to([0, 0.6, 0])
        q2 = para("\"Let me die.\" — Rakesh answers that he has his duty.", width=10, size=28, color=th.CORAL).move_to([0, -2.3, 0])
        with self.say("On that thin diet Varma weakens, and pills and tonics take the place of food: for his bowels, his blood pressure, his arthritis, and finally to keep his heart beating. There are rushes to hospital and the humiliation of the stomach pump. When the old man begs, let me die, his son replies that he has his duty."):
            self.play(FadeIn(h))
            for b_ in bottles:
                self.play(FadeIn(b_, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(q2))
        self.play(FadeOut(VGroup(h, bottles, q2)))
        h = E.head(self, "The last evening")
        gate = VGroup(Rectangle(width=4.6, height=1.2, stroke_color=th.MINT, stroke_width=3), T("Dr. Rakesh, M.D. …", size=28, color=th.CORAL, weight="BOLD")).move_to([3.6, 1.4, 0])
        gate[1].move_to(gate[0])
        gl = para("the gate: his son's name and degrees; his own name long gone", width=4.6, size=22, color=th.MUTED).next_to(gate, DOWN, buff=0.2)
        ev = E.bullets(["propped up on pillows; \"Rakesh says you can sit if you try\"", "the son arrives in white, with a new tonic, and reaches for his feet", "Varma tucks his feet away, sweeps the bottle from his hand: it smashes", "brown syrup on white trousers — and for once, noise and attention around him", "flat on his back, like \"some dire prophet\": God is calling — let me go"], width=7.0, size=24).move_to([-2.8, -0.5, 0])
        with self.say("The last scene. On the veranda, Veena props him up on pillows that make his head swim: Rakesh says you can sit if you try. He stares at the gate, which carries his son's name and degrees; his own name vanished long ago. The doctor arrives in white with a new tonic and reaches out, ever devoted, to press his father's feet. The old man tucks them away, and with one grand sweep knocks the bottle from his son's hand. It smashes. Brown syrup stains the white trousers. For once there is noise and attention around him, and he lies back like a prophet and groans that God is calling him: now let him go."):
            self.play(FadeIn(h), FadeIn(gate), FadeIn(gl))
            E.reveal_list(self, ev, 12.0)
        self.play(FadeOut(VGroup(h, gate, gl, ev)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        cards = VGroup(
            E.card("Rakesh", "Desai is scrupulously fair: hard-working, modest, loyal, faithful. He never neglects a duty. But he turns every wish into a medical fact, laughs at complaints, and cannot hear a plain \"no\".", th.SKY, w=6.2, h=3.4, size=22),
            E.card("Varma", "not simply a victim: vain, greedy for sweets, theatrical, ready to bribe a child. Yet he gets the strongest lines and the last word; we move from smiling at him to pitying him.", th.AMBER, w=6.2, h=3.4, size=22),
            E.card("Veena", "seen only through Varma's eyes, so we can't tell if she is unkind or just obedient. Everyone repeats the doctor.", th.PINK, w=6.2, h=2.3, size=22),
            E.card("Bhatia", "the neighbour over the hedge: Varma's audience, and the voice of plain moral common sense", th.MINT, w=6.2, h=2.3, size=22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to([0, 0.0, 0])
        with self.say("Desai is fair to Rakesh. He is hard working, modest and loyal; he came home when he need not have; nothing shows him neglecting a duty. But he turns every wish into a medical fact, laughs outside the door at his father's complaints, and cannot hear a plain no, perhaps because everyone has always agreed with him. Varma is no saint either: vain, greedy for sweets, given to fake deaths, willing to bribe a grandchild. Yet Desai gives him the last word."):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        with self.say("Veena we only see through the old man's resentful eyes, so we cannot tell if she is unkind or simply obedient. And Bhatia, the neighbour over the hedge, is the voice of common sense: shocked that a son could refuse his father food."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Two ideas of what a son owes")
        a = E.card("the community's idea", "ritual and visible: touch the feet, obey, marry as mother says, provide a car ride and a comfortable bed", th.SKY, w=5.6, h=2.6, size=24).move_to([-3.2, 0.6, 0])
        b = E.card("Varma's idea", "personal: be listened to, be fed what he loves, choose how his life ends", th.AMBER, w=5.6, h=2.6, size=24).move_to([3.2, 0.6, 0])
        nt = para("Rakesh fulfils the first completely — and never notices the second.", width=10, size=28, color=th.CORAL).move_to([0, -2.1, 0])
        with self.say("The central theme is duty and its limits. The community's idea of a good son is ritual and visible: touch the feet, obey, provide. Varma's idea is personal: listen to me, feed me what I love, let me choose how my life ends. Rakesh fulfils the first completely, and never notices the second."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))
        cards = VGroup(
            E.card("Care vs control", "everything is for his health; almost everything takes his choices away. What is a long life worth if lived only to take medicine?", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Appearance and reality", "the same efficiency is first admired, then called heartless: \"the interpretation had altered\"", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Ambition and its cost", "from the vegetable market to a clinic — and no room left for the old man's tastes, or his name", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Old age and the wish to die", "he wants respect for his exhaustion, not more life; the ending grants only noise", th.AMBER, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Around it, more themes. Care against control: the story never says Rakesh is medically wrong, but asks what a life is worth if it is lived only to eat medicines. Appearance and reality: the same behaviour is admired in the first half and called tyranny in the second; as the narrator admits, only the interpretation has altered. Ambition and its cost: in the new prosperity there is no room for the old man's tastes, or even his name. And old age: Varma does not want more life; he wants his exhaustion respected."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Two halves, and a narrator who changes sides")
        ax = Axes(x_range=[0, 10, 1], y_range=[-3, 3, 1], x_length=11.0, y_length=3.8, tips=False, axis_config={"color": th.FAINT, "stroke_width": 2, "include_ticks": False}).move_to([0, -0.2, 0])
        cv = E.arc_curve(ax, [0, 2, 4, 5, 6, 8, 10], [2.5, 2.6, 2.2, 0.2, -1.4, -2.3, -2.7], color=th.AMBER)
        top = T("narrator admires Rakesh (the neighbours' voice)", size=22, color=th.SKY).move_to(ax.c2p(2.6, 3.3))
        bot = T("narrator close to Varma (his words)", size=22, color=th.CORAL).move_to(ax.c2p(7.6, -3.5))
        hinge = VGroup(DashedLine(ax.c2p(5, -3), ax.c2p(5, 3), color=th.MUTED), T("\"cease to dazzle\"", size=22, color=th.MUTED).move_to(ax.c2p(5.0, -3.6)).shift(LEFT * 2.6))
        nt = para("We are never taken inside Rakesh — so the ending feels like an accusation.", width=11, size=26, color=th.MINT).move_to([0, -3.0, 0])
        with self.say("The story has two halves of opposite mood. In the first, festive and comic, the narrator echoes the neighbours' admiration. After the hinge, the narrator moves close to Varma and even borrows his words, calling Veena a smiling, hypocritical pudding. And we are never once taken inside Rakesh's mind. That is why the ending lands like an accusation: we know what the father feels, and can only guess at the son."):
            self.play(FadeIn(h), Create(ax), FadeIn(top))
            self.play(Create(cv), FadeIn(hinge), run_time=2.5)
            self.play(FadeIn(bot))
        self.play(FadeOut(VGroup(ax, cv, top, bot, hinge)))
        tri = VGroup(
            E.card("verbal irony", "\"such a son as few women had borne\" — praise with a faint mocking edge", th.SKY, w=3.9, h=2.6, size=22),
            E.card("situational irony", "every kindness of the son increases the father's misery", th.AMBER, w=3.9, h=2.6, size=22),
            E.card("dramatic irony", "we know Varma is serious when he says he is dying; his family thinks he is acting", th.CORAL, w=3.9, h=2.6, size=22),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        ti = para("And the title itself: \"devoted\" means one thing in the first half, another in the second.", width=11, size=26, color=th.INK).move_to([0, -2.2, 0])
        with self.say("The main tool is irony, in all three kinds. Verbal irony: such a son as few women had borne, praise with a mocking edge. Situational irony: each kindness of the son increases the father's misery. Dramatic irony: we know the old man means it when he says he is dying; his family thinks he is acting. And above all, the title, which means one thing in the first half and the opposite in the second."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in tri], lag_ratio=0.4))
            self.play(FadeIn(ti))
        self.play(FadeOut(VGroup(h, tri, ti)))
        rows = [["motif: feet", "touched, then tucked away", "respect becomes refusal"], ["symbol: the signboard", "his son's name on the gate", "the father erased"], ["symbol: the tonic", "smashed at the climax", "his last, only refusal"],
                ["simile", "\"like some dire prophet\"", "the weak old man made grand"], ["satire", "\"the USA\", not America", "mocks new snobberies"], ["contrast", "halwa vs scales and pills", "old world vs cold modern care"]]
        E.device_slide(self, rows, "Devices to quote. The motif of feet: touched in respect at the start, tucked away in refusal at the end; Desai never comments, the reversal does it. Symbols: the signboard with the son's name, and the tonic bottle. Similes that make the old man grand, like some dire prophet. Satire on snobbery. And the contrast between the old world of halwa and betel and the new world of scales and pills.", widths=(3.0, 5.0, 4.4), size=22)
        self.quiz("Why is the title \"A Devoted Son\" ironic?",
                  ["Rakesh neglects his father", "he ignores his father's will", "Rakesh is not really the son", "the father is devoted, not the son"], 1,
                  "Pause and think.",
                  "Rakesh does every duty, yet the care takes away his father's choices, food and dignity.")
        self.quiz("How does the narrator's viewpoint change at the hinge?",
                  ["from Varma to Rakesh", "from admiring to siding with Varma", "from first to second person", "it never changes"], 1,
                  "One more.",
                  "It moves from echoing the community's praise of Rakesh to sharing Varma's feelings and words.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Anita Desai (b. 1937); from Games at Twilight (1978).",
            "First half: the rise — exams, the USA, a clinic; feet touched in respect.",
            "The hinge: skill displayed too long ceases to dazzle; food replaced by tonics.",
            "Themes: duty vs the father's will, care vs control, appearance vs reality.",
            "Irony of the title; the narrator changes sides; the feet are tucked away.",
        ], "Quick recap. Desai, and Games at Twilight. The son's great ascent. The hinge, and a diet that becomes a cell. Duty against will, care against control. And the irony of a devoted son whose father finally tucks his feet away.")
        self.outro("That was A Devoted Son. Next, a tale of greed and gold on a tropical island: The Treasure in the Forest, by H. G. Wells. See you there.")
