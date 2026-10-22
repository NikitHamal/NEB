import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _m as P  # noqa: E402
from _m import polar  # noqa: E402

VOW = th.AMBER
CON = th.SKY


class Lesson(Lesson):
    SUBJECT = "math"
    GRADE = 12
    UNIT = 1
    TITLE = "Permutation and Combination"
    SUBTITLE = "Counting without listing"
    SECTIONS = ["Basic principle of counting", "Permutations of distinct objects", "Objects not all different",
                "Circular permutations and repetition", "Combinations", "Properties of combination"]
    NEXT = "Unit 2 · Binomial Theorem"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        plate = RoundedRectangle(corner_radius=0.2, width=6.4, height=1.6, stroke_color=WHITE, stroke_width=4, fill_color="#B3243A", fill_opacity=1).move_to([0, 1.2, 0])
        txt = T("BA 1 PA 2345", size=56, color=WHITE, weight="BOLD").move_to(plate)
        with self.say("Every motorbike in Bagmati carries a number plate. Thirty players in your class want a five member committee. Eleven cricketers need a batting order. How many possibilities are there in each case? Far too many to list."):
            self.play(FadeIn(plate), Write(txt))
        q = VGroup(T("Does order matter?", size=44, color=th.AMBER, weight="BOLD"),
                   VGroup(T("yes → permutation (arrangement)", size=30, color=CON), T("no → combination (selection)", size=30, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)).arrange(DOWN, buff=0.5).move_to([0, -1.4, 0])
        with self.say("This whole chapter turns on one question. Does the order matter? If it does, you are counting arrangements: permutations. If it does not, you are counting selections: combinations. Get that decision right, and every exam question becomes a short calculation."):
            self.play(FadeIn(q[0], scale=1.2))
            self.play(FadeIn(q[1], shift=UP * 0.2))
        nb = P.neby_in(self, "think", height=1.3)
        P.neby_out(self, nb)
        self.play(FadeOut(VGroup(plate, txt, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Mathematics, Unit 1: Permutation and Combination. Counting, without ever writing out the list."):
            pass
        self.end_title(tc, nb)
        self.roadmap("The plan. The two basic counting principles and factorials. Permutations of different objects. Objects that repeat. Arrangements round a circle, and with repetition. Combinations. And finally the properties of combinations, including Pascal's rule.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = P.head(self, "AND multiplies, OR adds")
        K = np.array([-5.0, -0.5, 0])
        Pk = np.array([0.0, -0.5, 0])
        J = np.array([5.0, -0.5, 0])
        cities = VGroup(*[VGroup(Dot(p_, radius=0.15, color=WHITE), T(n_, size=24, color=th.INK).next_to(p_, DOWN, buff=0.25)) for p_, n_ in [(K, "Kathmandu"), (Pk, "Pokhara"), (J, "Jomsom")]])
        bus = VGroup(*[ArcBetweenPoints(K, Pk, angle=a, color=th.SKY, stroke_width=4) for a in (-0.6, -0.35, -0.12)])
        fly = VGroup(*[ArcBetweenPoints(K, Pk, angle=a, color=th.PINK, stroke_width=4) for a in (0.35, 0.65)])
        jeep = VGroup(*[ArcBetweenPoints(Pk, J, angle=a, color=th.MINT, stroke_width=4) for a in (-0.5, -0.17, 0.17, 0.5)])
        l1 = T("3 buses OR 2 flights: 3 + 2 = 5", size=26, color=th.INK).move_to([0, 2.0, 0])
        l2 = T("then AND 4 jeeps: 5 × 4 = 20", size=26, color=th.AMBER, weight="BOLD").move_to([0, 1.4, 0])
        with self.say("Two rules do almost everything. From Kathmandu to Pokhara you can take one of three buses, or one of two flights. These are alternatives: you do one or the other. So the choices add: three plus two, five."):
            self.play(FadeIn(h), FadeIn(cities))
            self.play(LaggedStart(*[Create(b_) for b_ in bus], lag_ratio=0.2), LaggedStart(*[Create(f_) for f_ in fly], lag_ratio=0.2))
            self.play(FadeIn(l1))
        with self.say("Then from Pokhara to Jomsom there are four jeeps. You do the first leg, and then the second. For each of the five first legs there are four second legs, so the choices multiply: twenty journeys. The connecting word tells you the rule: OR adds, AND multiplies."):
            self.play(LaggedStart(*[Create(j_) for j_ in jeep], lag_ratio=0.2))
            self.play(FadeIn(l2))
            path = VMobject().set_points_as_corners([K, Pk])
            d = Dot(K, radius=0.12, color=th.AMBER)
            self.add(d)
            for b_ in [bus[0], fly[1]]:
                for j_ in [jeep[0], jeep[3]]:
                    self.play(MoveAlongPath(d, b_), run_time=0.35)
                    self.play(MoveAlongPath(d, j_), run_time=0.35)
                    d.move_to(K)
            self.remove(d)
        self.play(FadeOut(VGroup(h, cities, bus, fly, jeep, l1, l2)))
        h = P.head(self, "Factorial")
        f = M(r"n! = n(n-1)(n-2)\cdots 3\cdot2\cdot1", size=48).move_to([0, 1.6, 0])
        f2 = M(r"n! = n\,(n-1)!", size=44, color=th.SKY).move_to([0, 0.5, 0])
        vals = VGroup(*[M(rf"{k}! = {v}", size=36) for k, v in [(3, 6), (4, 24), (5, 120), (6, 720)]]).arrange(RIGHT, buff=0.7).move_to([0, -0.6, 0])
        z = M(r"n = 1:\ \ 1! = 1\cdot 0! \ \Rightarrow\ 0! = 1", size=40, color=th.AMBER).move_to([0, -1.9, 0])
        with self.say("A shorthand we will need constantly. n factorial is the product of all whole numbers from n down to one. Five factorial is one hundred and twenty, six factorial seven hundred and twenty. And notice: n factorial equals n times n minus one factorial."):
            self.play(FadeIn(h), Write(f))
            self.play(Write(f2))
            self.play(LaggedStart(*[FadeIn(v_) for v_ in vals], lag_ratio=0.2))
        with self.say("Put n equal to one in that rule. One factorial is one times zero factorial, so zero factorial must equal one. It is not an accident; the formula forces it."):
            self.play(Write(z))
        self.play(FadeOut(VGroup(h, f, f2, vals, z)))
        self.p1_boxes()

    def p1_boxes(self):
        h = P.head(self, "Fill the boxes: three-digit numbers from 1–6")
        lab = VGroup(*[T(s_, size=22, color=th.MUTED) for s_ in ["hundreds", "tens", "units"]])
        rows = []
        cases = [("repetition allowed", [6, 6, 6], "216", [0, 1, 2]), ("no repetition", [6, 5, 4], "120", [0, 1, 2]), ("no repetition, even", [5, 4, 3], "60", [2, 0, 1])]
        y = 1.4
        allg = VGroup()
        says = ["Three boxes: hundreds, tens and units, to be filled from the digits one to six. If digits may repeat, every box has six choices: six times six times six, two hundred and sixteen.",
                "If they may not repeat, each digit used is gone: six, then five, then four. One hundred and twenty.",
                "And if the number must also be even, fill the restricted box first. The units digit must be two, four or six: three choices. That leaves five for the hundreds and four for the tens. Sixty."]
        self.play(FadeIn(h))
        for (name, vals, tot, order), sy in zip(cases, says):
            bx = P.slots(3, w=1.0, h=0.8, buff=0.55).move_to([-0.6, y, 0])
            nm = T(name, size=22, color=th.BODY).next_to(bx, LEFT, buff=0.4)
            if y == 1.4:
                for l_, b_ in zip(lab, bx):
                    l_.next_to(b_, UP, buff=0.12)
                allg.add(lab)
            nums = [P.num_in(bx[i], vals[i]) for i in range(3)]
            res = M(r"= " + tot, size=40, color=th.MINT).next_to(bx, RIGHT, buff=0.4)
            times = VGroup(*[T("×", size=30, color=th.MUTED).move_to((bx[i].get_right() + bx[i + 1].get_left()) / 2) for i in range(2)])
            with self.say(sy):
                self.play(FadeIn(bx), FadeIn(nm), *( [FadeIn(lab)] if y == 1.4 else []))
                for i in order:
                    if i == 2 and order[0] == 2:
                        self.play(Indicate(bx[2], color=th.CORAL, scale_factor=1.15), run_time=0.5)
                    self.play(FadeIn(nums[i], scale=1.4), run_time=0.4)
                self.play(FadeIn(times), Write(res))
            allg.add(bx, nm, *nums, times, res)
            y -= 1.4
        self.play(FadeOut(VGroup(h, allg)))
        self.tip("Fill the RESTRICTED place first (must be even, must start with a vowel, a given person at the head). Then the free places.",
                 "Exam tip. Whenever a question has a restriction, must be even, must start with a vowel, a certain person at the head, fill that place first. Otherwise you will not know how many choices are left for it.", state="wink")

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = P.head(self, "Arranging r of n distinct objects")
        bx = P.slots(5, w=1.7, h=1.0, buff=0.25).move_to([0, 1.0, 0])
        labs = ["n", "n-1", "n-2", r"\cdots", "n-r+1"]
        ms = VGroup(*[M(l_, size=38, color=th.AMBER).move_to(b_) for l_, b_ in zip(labs, bx)])
        br = Brace(bx, DOWN, color=th.MUTED)
        bl = T("r boxes", size=24, color=th.MUTED).next_to(br, DOWN, buff=0.1)
        f1 = M(r"{}^nP_r = n(n-1)(n-2)\cdots(n-r+1)", size=44).move_to([0, -1.2, 0])
        f2 = M(r"= \frac{n(n-1)\cdots(n-r+1)\,(n-r)!}{(n-r)!} = \frac{n!}{(n-r)!}", size=44, color=th.MINT).move_to([0, -2.4, 0])
        with self.say("Now the general case. Arrange r objects, chosen from n different objects, in a row. The first box can take any of the n. The second, n minus one, because one is used. The third, n minus two. And the r th box takes n minus r plus one."):
            self.play(FadeIn(h), FadeIn(bx))
            for m_ in ms:
                self.play(FadeIn(m_, scale=1.3), run_time=0.4)
            self.play(GrowFromCenter(br), FadeIn(bl))
        with self.say("Multiply them, by the AND rule. That product is written n P r. Multiply top and bottom by n minus r factorial, and it closes up neatly: n factorial over n minus r factorial."):
            self.play(Write(f1))
            self.play(Write(f2))
        self.play(FadeOut(VGroup(bx, ms, br, bl, f1, f2)))
        fs = VGroup(M(r"{}^nP_r = \frac{n!}{(n-r)!}", size=46, color=th.MINT), M(r"{}^nP_n = n!", size=42), M(r"{}^nP_0 = 1,\quad {}^nP_1 = n", size=42)).arrange(DOWN, buff=0.45).move_to([0, 0.2, 0])
        with self.say("Put r equal to n: n different objects can be arranged among themselves in n factorial ways. And n P zero is one, n P one is n."):
            self.play(LaggedStart(*[Write(f_) for f_ in fs], lag_ratio=0.4))
        self.play(FadeOut(VGroup(h, fs)))
        P.worked(self, "(a) Find n if ⁿP₄ = 20 · ⁿP₂.  (b) Find r if ¹⁰Pᵣ = 720.",
                 [r"n(n-1)(n-2)(n-3) = 20\,n(n-1)", r"(n-2)(n-3) = 20 \Rightarrow n^2 - 5n - 14 = 0", r"(n-7)(n+2) = 0 \Rightarrow n = 7", r"\text{(b) } 10\times9\times8 = 720 \Rightarrow r = 3"],
                 ["A worked example. Write both sides as products, not factorials.", "n P four is four falling factors; n P two is two.", "Cancel n times n minus one, which is not zero, and expand.",
                  "So n is seven or minus two, and a count cannot be negative: n is seven. Check: seven P four is eight forty, and twenty times seven P two is twenty times forty two, also eight forty.", "And ten P r equal to seven twenty: ten times nine times eight already gives seven twenty, so r is three."],
                 colors=[None, None, th.AMBER, th.AMBER])
        self.p2_triangle()

    def p2_triangle(self):
        h = P.head(self, "TRIANGLE: blocks and gaps")
        w = P.word("TRIANGLE", w=0.7, size=34).move_to([0, 1.6, 0])
        a = M(r"8! = 40\,320", size=40).move_to([0, 0.5, 0])
        with self.say("Arrange the letters of TRIANGLE. Eight different letters: five consonants and three vowels. With no restriction, eight factorial: forty thousand three hundred and twenty."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(t_, shift=DOWN * 0.2) for t_ in w], lag_ratio=0.08))
            self.play(Write(a))
        vi = [2, 3, 7]
        ci = [0, 1, 4, 5, 6]
        cons = VGroup(*[w[i] for i in ci])
        vows = VGroup(*[w[i] for i in vi])
        self.play(FadeOut(a))
        tgt = VGroup(*[w[i].copy() for i in ci + vi]).arrange(RIGHT, buff=0.08).move_to([0, 1.6, 0])
        self.play(*[w[i].animate.move_to(tgt[k]) for k, i in enumerate(ci + vi)], run_time=1.0)
        blk = SurroundingRectangle(VGroup(*[w[i] for i in vi]), color=VOW, buff=0.08, corner_radius=0.1)
        b1 = M(r"\text{6 units: } 6! \times 3! = 720 \times 6 = 4320", size=38).move_to([0, 0.3, 0])
        with self.say("Now all the vowels together. Tie the three vowels into one block. The block and the five consonants make six units: six factorial ways. Inside the block, the vowels can be shuffled in three factorial ways. Four thousand three hundred and twenty."):
            self.play(Create(blk))
            self.play(Write(b1))
            self.play(Swap(w[vi[0]], w[vi[2]]), run_time=0.8)
        self.play(FadeOut(VGroup(blk, b1)))
        cons_t = VGroup(*[w[i].copy() for i in ci]).arrange(RIGHT, buff=1.3).move_to([0, 1.6, 0])
        self.play(*[w[i].animate.move_to(cons_t[k]) for k, i in enumerate(ci)], *[w[i].animate.move_to([-2 + 2 * k, -0.3, 0]) for k, i in enumerate(vi)], run_time=1.0)
        gaps = VGroup(*[T("_", size=40, color=th.MINT).move_to(p_) for p_ in [cons_t[0].get_left() + LEFT * 0.65] + [(cons_t[k].get_right() + cons_t[k + 1].get_left()) / 2 for k in range(4)] + [cons_t[4].get_right() + RIGHT * 0.65]])
        gl = T("6 gaps", size=24, color=th.MINT).next_to(cons_t, UP, buff=0.3)
        b2 = M(r"5! \times {}^6P_3 = 120 \times 120 = 14\,400", size=40, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("And no two vowels together. Use the gap method. Arrange the five consonants first: five factorial ways. They leave six gaps: before, between and after them. Drop the three vowels into three different gaps: six P three ways. One hundred and twenty times one hundred and twenty: fourteen thousand four hundred."):
            self.play(FadeIn(gaps), FadeIn(gl))
            for k, i in enumerate(vi):
                gi = [0, 2, 5][k]
                self.play(w[i].animate.move_to([gaps[gi].get_center()[0], 1.6, 0]), FadeOut(gaps[gi]), run_time=0.5)
            self.play(Write(b2))
        self.play(FadeOut(VGroup(h, w, gaps, gl, b2)))
        c = self.callout("careful", "'No two vowels together' (gap method) is NOT the same as 'vowels not all together' (total minus block): for TRIANGLE, 14,400 versus 40,320 − 4320 = 36,000.", width=11, size=26)
        with self.say("Careful with the wording. Vowels not all together is the total minus the block case: thirty six thousand. No two vowels together needs the gap method: fourteen thousand four hundred. They are different questions."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = P.head(self, "When some objects are identical")
        w = VGroup(P.tile("A", VOW), P.tile("A", VOW), P.tile("B", CON)).arrange(RIGHT, buff=0.1).move_to([-3.5, 1.6, 0])
        lab = VGroup(P.tile("A₁", VOW, size=24), P.tile("A₂", VOW, size=24), P.tile("B", CON)).arrange(RIGHT, buff=0.1)
        perms = ["A₁A₂B", "A₂A₁B", "A₁BA₂", "A₂BA₁", "BA₁A₂", "BA₂A₁"]
        lst = VGroup(*[T(p_, size=26, color=th.INK) for p_ in perms]).arrange_in_grid(3, 2, buff=(0.8, 0.3)).move_to([-3.2, -0.6, 0])
        pairs = VGroup(*[SurroundingRectangle(VGroup(lst[2 * k], lst[2 * k + 1]), color=th.MINT, buff=0.1) for k in range(3)])
        res = VGroup(T("AAB", size=28, color=th.MINT), T("ABA", size=28, color=th.MINT), T("BAA", size=28, color=th.MINT)).arrange(DOWN, buff=0.5).move_to([0.6, -0.6, 0])
        f = M(r"x \times 2! = 3! \Rightarrow x = \frac{3!}{2!} = 3", size=40, color=th.AMBER).move_to([3.8, 0.8, 0])
        with self.say("Arrange A, A, B. If we label the two A's to make them different, there are three factorial, six arrangements. But swapping the labels changes nothing that you can see. So the six fall into pairs, and there are really only three: six over two factorial."):
            self.play(FadeIn(h), FadeIn(w))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lst], lag_ratio=0.12))
            self.play(LaggedStart(*[Create(p_) for p_ in pairs], lag_ratio=0.2))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in res], lag_ratio=0.2))
            self.play(Write(f))
        g = M(r"\text{arrangements} = \frac{n!}{p!\,q!\,s!}", size=48, color=th.MINT).move_to([3.0, -2.3, 0])
        with self.say("In general: if n objects contain p alike of one kind, q of another and s of a third, each real arrangement hides p factorial times q factorial times s factorial labelled ones. So the count is n factorial over p factorial q factorial s factorial."):
            self.play(Write(g))
        self.play(FadeOut(VGroup(h, w, lst, pairs, res, f, g)))
        P.worked(self, "How many arrangements of KATHMANDU? In how many are the three vowels together?",
                 [r"9 \text{ letters, A twice: } \frac{9!}{2!} = 181\,440", r"\text{block (A,A,U) + 6 consonants} = 7 \text{ units: } 7!", r"7! \times \frac{3!}{2!} = 5040 \times 3 = 15\,120"],
                 ["KATHMANDU.", "Nine letters, and only A repeats, twice. Nine factorial over two factorial: one hundred and eighty one thousand four hundred and forty.",
                  "Vowels together: A, A and U make one block, plus six different consonants: seven units, seven factorial.", "Inside the block, A A U can be ordered in three factorial over two factorial, three ways. Fifteen thousand one hundred and twenty."])
        P.worked(self, "Arrangements of MISSISSIPPI? In how many do no two I's come together?",
                 [r"M\,1,\ I\,4,\ S\,4,\ P\,2:\quad \frac{11!}{4!\,4!\,2!} = 34\,650", r"\text{others } (M,S^4,P^2): \frac{7!}{4!\,2!} = 105 \text{, leaving 8 gaps}", r"105 \times {}^8C_4 = 105 \times 70 = 7350"],
                 ["The classic: MISSISSIPPI.", "Eleven letters: one M, four I's, four S's, two P's. Eleven factorial over four factorial four factorial two factorial: thirty four thousand six hundred and fifty.",
                  "For no two I's together, arrange the other seven letters first: one hundred and five ways, leaving eight gaps.", "The four I's are identical, so we only choose which four gaps: eight C four, seventy. Seven thousand three hundred and fifty."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = P.head(self, "Round a table there is no 'first seat'")
        C = np.array([-3.0, -0.4, 0])
        tab, seats = P.round_table(4, R=1.6, center=C, labels=list("ABCD"))
        rot = ValueTracker(0.0)
        cap = P.Captions(self, at=(3.4, 0.0, 0), width=5.4, size=25)
        with self.say("Seat four friends, A, B, C, D, round a table. In a row, there would be four factorial, twenty four orders. But round a table, rotate everyone one seat, and nothing has really changed: each person has the same neighbours."):
            self.play(FadeIn(h), FadeIn(tab), FadeIn(seats))
            for _ in range(3):
                pos = [s_.get_center() for s_ in seats]
                self.play(*[seats[i].animate.move_to(pos[(i + 1) % 4]) for i in range(4)], path_arc=-PI / 2, run_time=0.8)
            cap("4 rotations look the same", sub="So the 4! linear orders come in groups of 4.")
        f = VGroup(M(r"\frac{n!}{n} = (n-1)!", size=48, color=th.MINT), T("fix one person; arrange the rest", size=24, color=th.BODY)).arrange(DOWN, buff=0.3).move_to([3.4, -1.6, 0])
        with self.say("So the linear arrangements come in groups of four that are rotations of each other: four factorial over four, which is three factorial. In general, n objects in a circle: n minus one factorial. Another way to see it: fix one person's seat, then arrange the other n minus one."):
            self.play(Indicate(seats[0], scale_factor=1.3))
            self.play(Write(f))
        self.play(FadeOut(VGroup(tab, seats, f)))
        cap.clear()
        beads = VGroup(*[Circle(radius=0.25, stroke_width=0, fill_color=c_, fill_opacity=1).move_to(C + polar(1.4, PI / 2 - TAU * i / 5)) for i, c_ in enumerate(th.PALETTE[:5])])
        ring = Circle(radius=1.4, stroke_color=th.MUTED, stroke_width=2).move_to(C)
        g = VGroup(M(r"\text{garland, necklace: } \frac{(n-1)!}{2}", size=40, color=th.AMBER), T("turning it over gives the same object", size=22, color=th.BODY)).arrange(DOWN, buff=0.3).move_to([3.4, -1.0, 0])
        with self.say("A garland or a necklace is different again. You can pick it up and turn it over. Clockwise and anticlockwise become the same object, so the count halves: n minus one factorial over two."):
            self.play(Create(ring), LaggedStart(*[FadeIn(b_) for b_ in beads], lag_ratio=0.1))
            self.play(Rotate(VGroup(ring, beads), PI, axis=UP, about_point=C), run_time=1.5)
            self.play(Write(g))
        self.play(FadeOut(VGroup(h, ring, beads, g)))
        P.worked(self, "Eight friends sit at a round table. (a) No restriction. (b) Two particular friends together. (c) Those two never together. (d) Eight different flowers in a garland.",
                 [r"\text{(a) } 7! = 5040", r"\text{(b) block: } 6! \times 2! = 1440", r"\text{(c) } 5040 - 1440 = 3600", r"\text{(d) } \frac{7!}{2} = 2520"],
                 ["A round table worked example.", "Eight in a circle: seven factorial, five thousand and forty.", "Tie the two friends together: seven units round the circle, six factorial, times two for their swap. One thousand four hundred and forty.",
                  "Never together is everything else: three thousand six hundred.", "And a garland of eight flowers: seven factorial over two, two thousand five hundred and twenty."])
        h = P.head(self, "Repetition allowed: n to the r")
        lt = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=0.8, height=0.55, stroke_color=th.SKY, stroke_width=2.5), T(str(i + 1), size=22, color=th.SKY)).move_to([-5.0 + 1.0 * i, 0.6, 0]) for i in range(5)])
        for l_ in lt:
            l_[1].move_to(l_[0])
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.15, width=1.6, height=1.3, stroke_color=th.AMBER, stroke_width=3).move_to([2.0 + 1.9 * i, 0.6, 0]) for i in range(3)])
        bl = VGroup(*[T(f"box {i + 1}", size=20, color=th.AMBER).next_to(boxes[i], UP, buff=0.1) for i in range(3)])
        res = M(r"3 \times 3 \times 3 \times 3 \times 3 = 3^5 = 243", size=42, color=th.MINT).move_to([0, -1.6, 0])
        warn = T("not 5³: each LETTER chooses a box", size=24, color=th.CORAL).move_to([0, -2.6, 0])
        with self.say("If objects can be reused, the choices never shrink: r places, n choices each, n to the power r. Post five letters into three boxes. Do not let the boxes choose; a box can take many letters. Let each letter choose its box: three choices, five times over. Three to the five, two hundred and forty three. Not five cubed."):
            self.play(FadeIn(h), FadeIn(lt), FadeIn(boxes), FadeIn(bl))
            rng = np.random.default_rng(2)
            for l_ in lt:
                b_ = boxes[rng.integers(0, 3)]
                self.play(l_.animate.scale(0.6).move_to(b_.get_center() + np.array([rng.uniform(-0.45, 0.45), rng.uniform(-0.35, 0.35), 0])), run_time=0.4)
            self.play(Write(res))
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(h, lt, boxes, bl, res, warn)))
        rows = [["situation", "count"], ["r of n, order matters, no repeats", "ⁿPᵣ = n!/(n−r)!"], ["r of n, order matters, repeats allowed", "nʳ"], ["all n, with p, q alike", "n!/(p! q!)"],
                ["all n round a circle", "(n−1)!"], ["garland or necklace", "(n−1)!/2"], ["r of n, order does NOT matter", "ⁿCᵣ = n!/(r!(n−r)!)"]]
        tb = P.table(rows, [6.6, 4.4], row_h=0.62, size=24, colors=[th.INK, th.AMBER]).move_to([0, 0.2, 0])
        with self.say("Here is the whole map so far, plus the one we meet next. Order matters with no repeats: n P r. With repeats: n to the r. Identical objects: divide by their factorials. A circle: n minus one factorial, halved for a garland. And when order does not matter at all: n C r.") as v:
            P.reveal_table(self, tb, v.dur * 0.9)
        self.play(FadeOut(tb))
        self.quiz("The number of ways in which 6 people can sit at a round table is",
                  ["720", "360", "120", "60"], 2,
                  "Pause and think. Six people, round table.",
                  "One hundred and twenty: six minus one, factorial. Seven twenty is the row answer, and sixty is the garland answer, which only applies if the arrangement can be flipped over.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = P.head(self, "Selection first, then arrangement")
        letters = P.word("ABCD", vowels="", cc=th.MINT, w=0.7).move_to([-4.6, 1.8, 0])
        sel = [("ABC", 0.6), ("ABD", -0.2), ("ACD", -1.0), ("BCD", -1.8)]
        cols = VGroup()
        for s_, y in sel:
            grp = P.word(s_, vowels="", cc=th.MINT, w=0.5, size=24).move_to([-4.6, y, 0])
            from itertools import permutations
            arr = VGroup(*[T("".join(p_), size=20, color=th.SKY) for p_ in permutations(s_)]).arrange(RIGHT, buff=0.25).move_to([0.9, y, 0])
            cols.add(VGroup(grp, Arrow(grp.get_right(), arr.get_left(), buff=0.15, color=th.MUTED, stroke_width=3), arr))
        lab = VGroup(T("⁴C₃ = 4 selections", size=24, color=th.MINT).move_to([-4.6, 1.5, 0]), T("each in 3! orders", size=24, color=th.SKY).move_to([0.9, 1.5, 0]))
        tot = M(r"{}^4C_3 \times 3! = 4 \times 6 = 24 = {}^4P_3", size=40, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Now selections, where order does not matter. Choose three letters from A, B, C, D. There are just four choices of trio. But each trio can be arranged in three factorial, six orders. Four times six is twenty four, which is exactly four P three."):
            self.play(FadeIn(h), FadeIn(lab[0]))
            self.play(LaggedStart(*[FadeIn(c_[0]) for c_ in cols], lag_ratio=0.2))
            self.play(FadeIn(lab[1]), LaggedStart(*[AnimationGroup(GrowArrow(c_[1]), FadeIn(c_[2])) for c_ in cols], lag_ratio=0.2))
            self.play(Write(tot))
        self.play(FadeOut(VGroup(h, cols, lab, tot)))
        f = VGroup(M(r"{}^nC_r \times r! = {}^nP_r", size=46), M(r"{}^nC_r = \frac{n!}{r!\,(n-r)!} = \frac{n(n-1)\cdots(n-r+1)}{r!}", size=46, color=th.MINT)).arrange(DOWN, buff=0.6).move_to([0, 0.3, 0])
        note = T("compute with the last form: r factors on top, r! below", size=24, color=th.AMBER).move_to([0, -2.0, 0])
        with self.say("That works in general. Every arrangement is one selection followed by one ordering, so n C r times r factorial equals n P r. Divide, and n C r is n factorial over r factorial and n minus r factorial. To compute it, use the last form: r falling factors on top, r factorial below."):
            self.play(Write(f[0]))
            self.play(Write(f[1]))
            self.play(FadeIn(note))
        self.play(FadeOut(VGroup(f, note)))
        P.worked(self, "A committee of 5 from 7 men and 4 women must contain (a) exactly 2 women, (b) at least 2 women, (c) at most 1 woman.",
                 [r"\text{(a) } {}^4C_2 \times {}^7C_3 = 6 \times 35 = 210", r"\text{(b) } 210 + {}^4C_3{}^7C_2 + {}^4C_4{}^7C_1 = 210 + 84 + 7 = 301", r"\text{(c) } {}^{11}C_5 - 301 = 462 - 301 = 161"],
                 ["A committee example.", "Exactly two women: choose two of four women, AND three of seven men. Six times thirty five: two hundred and ten.",
                  "At least two women means two OR three OR four: separate cases, so add. Three hundred and one.", "At most one woman is everything else: four sixty two minus three oh one, one hundred and sixty one."])
        h = P.head(self, "12 points, 5 of them collinear")
        rng = np.random.default_rng(4)
        col = [np.array([-5.0 + 1.0 * k, -1.8 + 0.25 * k, 0]) for k in range(5)]
        oth = [np.array([x, y, 0]) for x, y in [(-4.4, 1.2), (-2.8, 0.6), (-1.4, 1.6), (-0.4, 0.2), (-3.6, -0.4), (-1.8, -0.6), (0.3, 1.1)]]
        dots = VGroup(*[Dot(p_, radius=0.08, color=th.AMBER) for p_ in col], *[Dot(p_, radius=0.08, color=th.SKY) for p_ in oth])
        col = [c_ + LEFT * 0.8 for c_ in col]
        dots.shift(LEFT * 0.8)
        ln = Line(col[0] + (col[0] - col[4]) * 0.15, col[4] + (col[4] - col[0]) * 0.15, color=th.AMBER, stroke_width=3)
        txt = VGroup(M(r"\text{lines: } {}^{12}C_2 - {}^5C_2 + 1 = 66 - 10 + 1 = 57", size=34), M(r"\text{triangles: } {}^{12}C_3 - {}^5C_3 = 220 - 10 = 210", size=34),
                     M(r"\text{diagonals of a 12-gon: } {}^{12}C_2 - 12 = 54", size=34, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, -0.3, 0])
        with self.say("A geometry favourite. Twelve points, five of them on one line. Any two points make a line: twelve C two, sixty six. But the five collinear points were counted as ten lines when they make just one. Subtract ten, add back one: fifty seven. Any three points make a triangle unless they are collinear: two hundred and twenty minus ten. And a twelve sided polygon: sixty six segments, minus twelve sides, leaves fifty four diagonals."):
            self.play(FadeIn(h), FadeIn(dots))
            self.play(Create(ln))
            for t_ in txt:
                self.play(Write(t_), run_time=1.0)
        self.play(FadeOut(VGroup(h, dots, ln, txt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = P.head(self, "Five properties of ⁿCᵣ")
        props = VGroup(M(r"\text{(i) } {}^nC_0 = {}^nC_n = 1", size=38), M(r"\text{(ii) } {}^nC_r = {}^nC_{n-r}", size=38), M(r"\text{(iii) } {}^nC_r = {}^nC_s \Rightarrow r = s \text{ or } r + s = n", size=38),
                       M(r"\text{(iv) } {}^nC_r + {}^nC_{r-1} = {}^{n+1}C_r", size=38, color=th.MINT), M(r"\text{(v) } r\,{}^nC_r = n\,{}^{n-1}C_{r-1}", size=38)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        why = [("one way to choose nothing, one to choose everything", 0), ("choosing r to take = choosing n−r to leave", 1), ("each value is taken at most twice", 2), ("leave out a marked object, or include it", 3), ("choose a committee, then its chair", 4)]
        cap = P.Captions(self, at=(4.6, -0.1, 0), width=3.8, size=22)
        says = ["The properties. There is one way to choose nothing, and one way to choose everything.", "Choosing r things to take is the same act as choosing the n minus r things to leave behind. So n C r equals n C n minus r.",
                "So if n C r equals n C s, either r equals s, or r plus s equals n.", "Pascal's rule, the important one. To choose r from n plus one objects, mark one object. Either you leave it out, n C r ways, or you include it and choose r minus one more, n C r minus one ways.",
                "And r times n C r equals n times n minus one C r minus one: both count choosing a committee of r and then its chairperson."]
        self.play(FadeIn(h))
        for (w_, i), sy in zip(why, says):
            with self.say(sy):
                self.play(Write(props[i]), run_time=0.9)
                cap(w_, color=th.AMBER)
        self.play(FadeOut(VGroup(h, props)))
        cap.clear()
        h = P.head(self, "Pascal's triangle: each entry is the sum of the two above")
        tri = P.pascal(8, top=(0, 2.2, 0))
        with self.say("Pascal's rule builds a famous triangle. Each row lists n C zero up to n C n, and every entry is the sum of the two above it."):
            self.play(FadeIn(h))
            for row in tri:
                self.play(LaggedStart(*[FadeIn(x_, scale=1.3) for x_ in row], lag_ratio=0.1), run_time=0.5)
        a, b, c = tri[5][2], tri[5][3], tri[6][3]
        with self.say("Look: ten plus ten makes twenty. Five C two plus five C three equals six C three. The rows also add up to powers of two, one, two, four, eight, sixteen: the total number of subsets, which we will prove in the next unit."):
            self.play(Indicate(a, color=th.AMBER), Indicate(b, color=th.AMBER))
            self.play(Indicate(c, color=th.MINT, scale_factor=1.5))
            sums = VGroup(*[T(f"= {2 ** n}", size=22, color=th.MINT).next_to(tri[n], RIGHT, buff=0.4) for n in range(8)])
            self.play(LaggedStart(*[FadeIn(s_) for s_ in sums], lag_ratio=0.1))
        self.play(FadeOut(VGroup(h, tri, sums)))
        P.worked(self, "If ⁿCᵣ₋₁ = 36, ⁿCᵣ = 84, ⁿCᵣ₊₁ = 126, find n and r.",
                 [r"\frac{ {}^nC_r}{ {}^nC_{r-1}} = \frac{n-r+1}{r} = \frac{84}{36} = \frac{7}{3} \Rightarrow 3n - 10r + 3 = 0", r"\frac{ {}^nC_{r+1}}{ {}^nC_r} = \frac{n-r}{r+1} = \frac{126}{84} = \frac32 \Rightarrow 2n - 5r - 3 = 0",
                  r"\Rightarrow n = 9,\ r = 3 \quad (36, 84, 126 = {}^9C_2, {}^9C_3, {}^9C_4)"],
                 ["Three consecutive combinations. Take ratios: consecutive ones have a very simple ratio.", "n C r over n C r minus one is n minus r plus one over r. Set it equal to eighty four over thirty six, seven thirds.",
                  "The next ratio is n minus r over r plus one, equal to three halves.", "Solve the pair: n is nine and r is three. Check: nine C two, three and four are thirty six, eighty four and one twenty six."])
        P.worked(self, "(a) ²ⁿC₃ : ⁿC₂ = 44 : 3, find n.  (b) If ⁿC₈ = ⁿC₁₂, find ⁿC₁₇.",
                 [r"\frac{2n(2n-1)(2n-2)/6}{n(n-1)/2} = \frac{4(2n-1)}{3} = \frac{44}{3} \Rightarrow n = 6", r"\text{(b) } 8 \ne 12 \Rightarrow n = 20", r"{}^{20}C_{17} = {}^{20}C_3 = \frac{20\cdot19\cdot18}{6} = 1140"],
                 ["Two more.", "Write each as falling factors over a factorial, cancel, and you get four times two n minus one over three. Equal to forty four thirds: n is six.",
                  "If n C eight equals n C twelve, and eight is not twelve, then n is twenty.", "And never compute twenty C seventeen directly. Use twenty C three: twenty times nineteen times eighteen over six, one thousand one hundred and forty."])
        self.tip("Never compute big factorials. Cancel first, and use the smaller of r and n − r: ⁵⁰C₄₈ = ⁵⁰C₂ = 1225.",
                 "Exam tip. Never multiply out big factorials. Cancel first, and always use the smaller of r and n minus r. Fifty C forty eight is just fifty C two, twelve twenty five.")
        self.quiz("If ⁿC₉ = ⁿC₇, then n is",
                  ["2", "9", "16", "63"], 2,
                  "Pause and think. n C nine equals n C seven. What is n?",
                  "Sixteen. Since nine is not seven, the property says nine plus seven must equal n. Two is the trap from subtracting.")
        self.quiz("The number of distinct arrangements of the letters of LEVEL is",
                  ["120", "60", "30", "20"], 2,
                  "One more. LEVEL.",
                  "Thirty. Five letters, with L twice and E twice: one twenty over two times two. One twenty is the trap: it ignores the repeated letters.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "OR adds, AND multiplies; n! = n(n−1)!, and 0! = 1.",
            "ⁿPᵣ = n!/(n−r)!; fill restricted places first; blocks for 'together', gaps for 'no two together'.",
            "Identical objects: n!/(p! q! …). Circle: (n−1)!; garland: (n−1)!/2. Repeats: nʳ.",
            "ⁿCᵣ = n!/(r!(n−r)!) = ⁿPᵣ/r!; use complements for 'at least' and 'never'.",
            "ⁿCᵣ = ⁿCₙ₋ᵣ; ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ (Pascal); rows of Pascal's triangle sum to 2ⁿ.",
        ], "Quick recap. OR adds and AND multiplies. Permutations, where order matters, are n factorial over n minus r factorial. Fill restricted places first, tie blocks for together, and use gaps for no two together. Repeated objects divide by their factorials; circles give n minus one factorial, halved for a garland. Combinations are permutations divided by r factorial. And Pascal's rule builds the triangle whose rows add up to powers of two.")
        self.outro("That was permutation and combination. Next, the binomial theorem, where those same n C r numbers turn up as the coefficients of every expansion. See you there.")
