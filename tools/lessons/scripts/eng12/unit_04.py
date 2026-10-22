import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

PAPER = "#E9D9A6"
INKD = "#4A3B22"


def treasure_map(w=7.0, h=4.6):
    """Chang-hi's map: reef with a gap, the river, the dotted line from the gap to the palms, the star — and the little dashes."""
    paper = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color="#B89B5E", stroke_width=3, fill_color=PAPER, fill_opacity=0.95)
    o = paper.get_center()
    sx, sy = w / 7.0, h / 4.6
    P = lambda x, y: o + np.array([x * sx, y * sy, 0])
    reef_l = VMobject(stroke_color=INKD, stroke_width=3).set_points_smoothly([P(-3.2, -1.6), P(-2.2, -1.9), P(-1.0, -2.0), P(-0.45, -1.95)])
    reef_r = VMobject(stroke_color=INKD, stroke_width=3).set_points_smoothly([P(0.45, -1.95), P(1.4, -1.9), P(2.6, -1.7), P(3.2, -1.4)])
    river = VMobject(stroke_color="#2F6C8F", stroke_width=4).set_points_smoothly([P(-2.9, 1.9), P(-2.0, 1.0), P(-0.6, 0.9), P(0.6, 0.4), P(1.7, 0.9), P(2.9, 1.5)])
    palms = VGroup(*[VGroup(Line(P(x, -1.2), P(x, -0.75), color=INKD, stroke_width=3), *[Line(P(x, -0.75), P(x + dx, -0.6 + dy), color="#3E7A3A", stroke_width=3) for dx, dy in [(-0.2, -0.1), (0.2, -0.1), (0, 0.12)]]) for x in (-0.35, 0.0, 0.35)])
    dotted = DashedLine(P(0, -1.95), P(0.25, 0.55), color=INKD, stroke_width=3, dash_length=0.08)
    star = Star(5, outer_radius=0.22, color=th.CORAL, fill_opacity=1).move_to(P(0.27, 0.6))
    dash_pos = [(-0.9, 0.3, 0.6), (-0.6, 1.3, -0.4), (1.1, 1.3, 0.9), (1.2, 0.0, -0.8), (-0.3, -0.2, 0.2), (0.8, -0.4, 1.3), (-1.3, 0.95, -1.1), (0.4, 1.45, 0.3)]
    dashes = VGroup(*[Line(ORIGIN, RIGHT * 0.28, color=INKD, stroke_width=4).rotate(a).move_to(P(x, y)) for x, y, a in dash_pos])
    g = VGroup(paper, reef_l, reef_r, river, palms, dotted, star, dashes)
    g.parts = dict(paper=paper, reef=VGroup(reef_l, reef_r), river=river, palms=palms, dotted=dotted, star=star, dashes=dashes)
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 4
    TITLE = "The Treasure in the Forest"
    SUBTITLE = "H. G. Wells · a short story"
    SECTIONS = ["H. G. Wells", "The map and the dream", "Into the forest", "The trap explained", "Characters and themes", "How Wells builds suspense"]
    NEXT = "Unit 5 · My Old Home"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        mp = treasure_map().move_to([0, -0.2, 0])
        d = mp.parts
        with self.say("Two men in a canoe, dying of thirst, study a stolen map. Here is the reef, with a gap. Here is the river. A dotted line runs from the gap to a clump of palms, and a star marks the place."):
            self.play(FadeIn(d["paper"]), Create(d["reef"]), Create(d["river"]), run_time=2)
            self.play(FadeIn(d["palms"]), Create(d["dotted"]), FadeIn(d["star"], scale=1.5))
        q = T("what are these little dashes?", size=30, color=th.AMBER, weight="BOLD").move_to([0, 2.9, 0])
        with self.say("And scattered round the star, some little dashes, pointing this way and that. Neither man can explain them. They will find out what they mean, one minute too late."):
            self.play(LaggedStart(*[Create(x_) for x_ in d["dashes"]], lag_ratio=0.15))
            self.play(FadeIn(q), d["dashes"].animate.set_color(th.CORAL))
            nb = E.neby_in(self, "surprised", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(mp, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 4: The Treasure in the Forest, by H. G. Wells."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. H. G. Wells. The map and the dream. Into the forest. The trap explained. The characters and themes. And how Wells builds suspense, clue by clue.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "H. G. Wells (1866–1946)")
        tl = E.timeline(["1866: born in Bromley, Kent; a poor shopkeeper's son", "studies biology under T. H. Huxley", "1894: this story, in Pall Mall Budget", "1895–98: The Time Machine, The Invisible Man, The War of the Worlds", "1946: dies in London"],
                        x0=-6.3, x1=6.3, y=0.3, colors=[th.SKY, th.MINT, th.AMBER, th.PINK, th.MUTED], size=22, wrap=2.6)
        nt = para("Not science fiction: an adventure-mystery with a sting in the tail. Collected in The Stolen Bacillus (1895).", width=11.4, size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Herbert George Wells was born in eighteen sixty six to a poor family in Kent. Apprenticed as a draper at thirteen, he hated it, won a scholarship, and studied biology under Thomas Huxley, Darwin's great defender. This story appeared in a London magazine in eighteen ninety four, when he was twenty seven. Within four years he had written The Time Machine, The Invisible Man and The War of the Worlds, and became a father of science fiction."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.5), run_time=6)
        with self.say("But this story is not science fiction. It is a tight adventure and mystery with a sting in the tail: a lesson in how to plant a secret in plain sight."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tl, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Evans's dream: how they got the map")
        steps = VGroup(*[E.card(t_, d_, c_, w=3.0, h=3.4, size=22) for t_, d_, c_ in [
            ("A galleon", "a Spanish treasure ship runs aground; the gold is buried; the crew never return", th.SKY),
            ("Chang-hi", "200 years later he finds the ingots, reburies them alone — \"very safe\"", th.AMBER),
            ("Overheard", "by a fire, Evans and Hooker hear three Chinese men talk of it", th.MINT),
            ("Seized", "they take the map by force: Chang-hi's pigtail in Evans's hand", th.CORAL)]]).arrange(RIGHT, buff=0.2).move_to([0, 0.3, 0])
        ar = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.0, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.5) for k in range(3)])
        with self.say("Evans dozes in the canoe, and his dream tells us the back story. Long ago a Spanish galleon ran aground and its gold was buried. Two hundred years later a Chinese man, Chang-hi, found the gold and reburied it single handed, laying great stress on how safe it was. Evans and Hooker overheard him by a campfire. Then the dream jumps to Chang-hi's pigtail in Evans's hand: they took the map by force."):
            self.play(FadeIn(h))
            for k, s_ in enumerate(steps):
                self.play(FadeIn(s_, shift=UP * 0.2), *([GrowArrow(ar[k - 1])] if k else []), run_time=0.7)
                self.hold(1.5)
        nt = para("The story never says they killed him. It implies it — and that is the point.", width=11, size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Notice: the story never says they killed Chang-hi. It only implies it. And in the dream Chang-hi gives a startling, incomprehensible grin, and the gold becomes a furnace, with a devil who looks like him feeding Evans burning coals. Two warnings, already."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, steps, ar, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "From glare to gloom")
        bands = VGroup(Rectangle(width=6.2, height=4.4, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.12).move_to([-3.2, -0.3, 0]), Rectangle(width=6.2, height=4.4, stroke_width=0, fill_color="#0E3B2C", fill_opacity=0.6).move_to([3.2, -0.3, 0]))
        left = VGroup(T("the beach", size=30, color=th.AMBER, weight="BOLD"), *[T(t_, size=24, color=th.INK) for t_ in ["\"the sky blazed\"", "lips hard and dry", "thirst; they drink greedily", "hope, and hurry"]]).arrange(DOWN, buff=0.3).move_to(bands[0])
        right = VGroup(T("the forest", size=30, color=th.MINT, weight="BOLD"), *[T(t_, size=24, color=th.INK) for t_ in ["trees like \"vast pillars\"", "cool, silent shadow", "\"It seems almost cold here\"", "danger, waiting"]]).arrange(DOWN, buff=0.3).move_to(bands[1])
        with self.say("They land, drink from the river, and walk into the jungle. Wells builds the setting as a contrast. The beach is blazing glare, dry lips, thirst and hurry. The forest is cool shadow under trees like vast pillars, so silent that Evans shivers: it seems almost cold here. From bright and open to dark and enclosed: from hope to danger."):
            self.play(FadeIn(h), FadeIn(bands[0]), FadeIn(left))
            self.play(FadeIn(bands[1]), FadeIn(right))
        self.play(FadeOut(VGroup(h, bands, left, right)))
        h = E.head(self, "Someone has been here before")
        body = VGroup(Ellipse(width=2.4, height=0.7, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.35), Circle(radius=0.3, stroke_color=th.SKY, stroke_width=3).shift(LEFT * 1.4)).scale(1.5).move_to([-3.2, 0.1, 0])
        hole = Ellipse(width=3.0, height=1.2, stroke_color=th.MUTED, stroke_width=3, fill_color="#1A140C", fill_opacity=1).move_to([2.8, -0.1, 0])
        bars = VGroup(*[Rectangle(width=0.7, height=0.3, stroke_width=0, fill_color=GOLD, fill_opacity=0.9) for _ in range(4)]).arrange(RIGHT, buff=0.06).move_to(hole)
        clues = VGroup(T("a Chinese man, face down, in blue", size=24, color=th.SKY).next_to(body, DOWN, buff=0.35), T("neck \"puffed and purple\", hands swollen", size=24, color=th.CORAL).next_to(body, DOWN, buff=0.85),
                       T("a spade, stones, a fresh hole", size=24, color=th.MUTED).next_to(hole, DOWN, buff=0.35), T("\"It's here still\": dull yellow bars", size=24, color=GOLD).next_to(hole, DOWN, buff=0.85))
        with self.say("By the stream they find a dead Chinese man, face down, in blue, beside a spade, a heap of stones and a freshly dug hole. Somebody has been here before. Evans swears and stamps; Hooker turns white and notices the dead man's neck is puffed and purple, his hands swollen. Then Hooker looks into the hole: You fool, it's all right. It's here still. Dull yellow bars of gold."):
            self.play(FadeIn(h), FadeIn(body), FadeIn(clues[0]))
            self.play(FadeIn(clues[1]))
            self.play(FadeIn(hole), FadeIn(clues[2]))
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.2), FadeIn(clues[3]))
        self.play(FadeOut(VGroup(h, body, hole, bars, clues)))
        h = E.head(self, "Three little pricks")
        ev = [("1", "Evans heaves out a bar: \"a little thorn pricked his hand\". He pulls it out and keeps working.", th.AMBER),
              ("2", "\"another little thorn\" — he grows irritable, short of breath, unreasonably angry", th.CORAL),
              ("3", "he collapses, clutching his throat. Lifting the gold, Hooker feels \"a little prick\" on his thumb.", th.PINK)]
        rows = VGroup(*[VGroup(Circle(radius=0.38, stroke_color=c_, stroke_width=4).add(T(n_, size=30, color=c_, weight="BOLD")), para(d_, width=9.8, size=26, color=th.INK)).arrange(RIGHT, buff=0.4) for n_, d_, c_ in ev]).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, -0.1, 0])
        with self.say("Now watch the thorns. Evans climbs into the hole and heaves out a heavy bar; a little thorn pricks his hand. He pulls it out and carries on, piling ingots on his jacket. Another little thorn. He grows irritable, his arms ache, the forest feels stuffy, he snaps at Hooker. Then he stumbles, clutches his throat, and slides down a tree. And as Hooker gathers up the gold, he feels a little prick on the ball of his thumb."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
                self.hold(2.5)
        self.play(FadeOut(VGroup(h, rows)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Hooker understands — one minute too late")
        mp = treasure_map(w=6.0, h=4.0).move_to([-3.5, -0.3, 0])
        d = mp.parts
        thorns = VGroup(*[VGroup(Line(ORIGIN, UP * 0.35, color=th.CORAL, stroke_width=4), Triangle(color=th.CORAL, fill_opacity=1).scale(0.07).shift(UP * 0.4)).move_to(x_.get_center()) for x_ in d["dashes"]])
        keys = VGroup(*[VGroup(T(a_, size=28, color=c_, weight="BOLD"), T("→ " + b_, size=26, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for a_, b_, c_ in [("the little dashes", "poisoned thorns, set round the gold", th.CORAL), ("\"very safe\"", "the treasure was booby-trapped", th.AMBER), ("the grin", "Chang-hi knew", th.PINK), ("the dead man", "not a snake: the thorns", th.SKY)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        keys.scale_to_fit_width(min(keys.width, 6.0)).move_to([3.5, -0.3, 0])
        with self.say("At that moment Hooker puts it all together. He looks at Evans twitching on the ground, at the blue clad body through the trees, and he thinks of the little dashes on the map. In a moment he understands. The dashes marked poisoned thorns, like those the Dyaks of Borneo use in blowpipes, planted all round the treasure. That is what Chang-hi meant by very safe. And he understands that grin now."):
            self.play(FadeIn(h), FadeIn(mp))
            self.play(LaggedStart(*[ReplacementTransform(x_, t_) for x_, t_ in zip(d["dashes"], thorns)], lag_ratio=0.1), run_time=2)
            for k_ in keys:
                self.play(FadeIn(k_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(1.2)
        self.play(FadeOut(VGroup(h, mp, thorns, keys)))
        q = E.quote("the white petals of some unknown flower came floating down through the gloom", "the last line", width=9.0, size=32).move_to([0, 0.8, 0])
        petals = VGroup(*[Ellipse(width=0.18, height=0.1, color=WHITE, fill_opacity=0.9).move_to([x, 3.2, 0]) for x in np.linspace(-5.5, 5.5, 9)])
        nt = para("He sucks the wound; the pain spreads. The story stops — no word about what happens next. None is needed.", width=11, size=26, color=th.MUTED).move_to([0, -2.0, 0])
        with self.say("Hooker sucks the wound for dear life, but the ache creeps into his arms and throat, and he knows it is no good. He sits by the pile of gold and watches his companion's body quiver. A breeze stirs high above, and the white petals of some unknown flower come floating down through the gloom. Wells stops there. He does not tell us Hooker dies. He does not need to."):
            self.play(FadeIn(q))
            self.play(LaggedStart(*[p_.animate.shift(DOWN * (7.2 + 0.3 * (k % 3))).rotate(PI * (k % 2 + 1)) for k, p_ in enumerate(petals)], lag_ratio=0.1), run_time=5)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(q, petals, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Evans", "hot-tempered and openly greedy; stamps and swears at the corpse; keeps digging after two pricks. The first to die.", th.CORAL, w=4.0, h=3.5, size=24),
            E.card("Hooker", "careful, watchful, the story's eyes. He notices the purple neck and wants to bury the body — and understands too late.", th.SKY, w=4.0, h=3.5, size=24),
            E.card("Chang-hi", "never on stage, yet he wins: a shrewd, secretive man who out-thinks his robbers from beyond the grave", th.AMBER, w=4.0, h=3.5, size=24),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.2, 0])
        with self.say("Three characters. Evans: hot tempered and greedy, swearing at the corpse and digging on after two pricks. Hooker: careful and watchful, the story's eyes, the one who understands, too late. And Chang-hi, who never appears on stage, yet wins: the shrewd man the robbers looked down on out-thinks them from beyond death."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=4)
        self.play(FadeOut(cards))
        cards = VGroup(
            E.card("Greed and its punishment", "a voyage without water, a stolen map, a corpse ignored, bar after bar after a prick: each step of greed leads deeper into the trap", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Appearance and reality", "the corpse looks snake-bitten, the forest peaceful, the gold a prize, the thorns ordinary. Each false look costs a life.", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Racism and its blindness", "they call a Chinese life \"scarcely sacred\". Contempt stops them imagining Chang-hi might be cleverer — and he is.", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Crime and rough justice", "the man they wronged defeats them; knowledge arrives at the moment of no return", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Greed and its punishment: every stage of greed leads them deeper into the trap, and the moral is acted out, never stated. Appearance and reality: nothing is what it seems, and each false appearance costs a life. Racism and its blindness: they think a Chinese life is scarcely sacred, and that contempt stops them imagining Chang-hi could be cleverer than they are. And rough justice: the man they wronged defeats them."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Every clue was planted early")
        clues = [("the little dashes on the map", "the poisoned thorns", th.CORAL), ("Chang-hi stressing \"the safety\"", "a booby-trap", th.AMBER), ("his startling grin", "he knew what awaited them", th.PINK), ("the nightmare of burning coals", "pain and punishment", th.SKY), ("the forest \"almost cold\"", "danger", th.MINT)]
        rows = VGroup(*[VGroup(T(a_, size=24, color=c_), Arrow(LEFT * 0.4, RIGHT * 0.4, color=th.MUTED, stroke_width=3), T(b_, size=24, color=th.INK)).arrange(RIGHT, buff=0.3) for a_, b_, c_ in clues]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        with self.say("The story is a lesson in foreshadowing. Every detail is a clue planted early. The little dashes on the map: the thorns. Chang-hi's stress on safety: a booby trap. His grin: he knew. The nightmare of burning coals: punishment. Even the forest feeling almost cold: danger. Read it twice and every line points to the ending."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(1.0)
        self.play(FadeOut(VGroup(h, rows)))
        rows = [["dramatic irony", "we suspect the thorns before Evans does", "each greedy act feels tragic"], ["situational irony", "they die of what protects the treasure", "the prize is the trap"], ["suspense", "the unexplained corpse", "what killed him?"],
                ["pathetic fallacy", "the silent forest, the falling petals", "nature seems to watch"], ["understatement", "\"Somebody has been here before.\"", "plain words, real alarm"], ["open ending", "no word on Hooker's death", "the reader completes it"]]
        E.device_slide(self, rows, "Other devices to quote. Dramatic irony: we guess about the thorns before Evans does. Situational irony: they die of the very thing that protects the treasure. Suspense around the corpse. Pathetic fallacy: the silent forest seems to watch. Understatement: somebody has been here before. And an open ending that the reader completes.", widths=(2.9, 5.3, 4.2), size=22)
        self.quiz("What did the little dashes on Chang-hi's map mark?",
                  ["the way to the river", "poisoned thorns", "other graves", "palm trees"], 1,
                  "Pause and think.",
                  "Poisoned thorns set round the gold: that is why Chang-hi said it was \"very safe\".")
        self.quiz("Why does Hooker understand Chang-hi's grin at the end?",
                  ["Chang-hi knew the gold was a trap", "Chang-hi was happy to share", "Chang-hi was mad", "it was a dream"], 0,
                  "One more.",
                  "Chang-hi knew the robbers would walk into his poisoned thorns.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "H. G. Wells (1866–1946); this tale from 1894, in The Stolen Bacillus.",
            "A stolen map; Evans's dream tells how they seized it from Chang-hi.",
            "Glare to gloom: the corpse, the gold, three little pricks.",
            "The dashes were poisoned thorns; \"very safe\" and the grin explained.",
            "Themes: greed punished, appearance vs reality, racism's blindness; foreshadowing everywhere.",
        ], "Quick recap. Wells, and a tale from eighteen ninety four. A stolen map and a guilty dream. From the blazing beach to the silent forest, a corpse, gold, and three little pricks. The dashes were poisoned thorns. Greed punished, appearances that lie, and contempt that blinds.")
        self.outro("That was The Treasure in the Forest. Next, a homecoming in China, and a childhood friend who now calls the narrator master: My Old Home, by Lu Xun. See you there.")
