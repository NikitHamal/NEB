import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

JADE = "#3FB98A"
MOON = "#F5C451"


def memory_scene(w=8.0, h=4.4):
    """The golden moon over a seashore of jade-green watermelons, and a boy with a pitchfork."""
    sky = Rectangle(width=w, height=h, stroke_width=0, fill_color="#14246B", fill_opacity=1)
    moon = Circle(radius=0.55, stroke_width=0, fill_color=MOON, fill_opacity=1).move_to(sky.get_corner(UR) + np.array([-1.3, -0.9, 0]))
    glow = Circle(radius=0.9, stroke_width=0, fill_color=MOON, fill_opacity=0.15).move_to(moon)
    sand = Rectangle(width=w, height=h * 0.38, stroke_width=0, fill_color="#C8B06A", fill_opacity=0.55).align_to(sky, DOWN)
    melons = VGroup(*[Ellipse(width=0.42, height=0.28, stroke_color="#1F6E4A", stroke_width=2, fill_color=JADE, fill_opacity=1).move_to(sky.get_corner(DL) + np.array([0.5 + 0.62 * i + 0.3 * (j % 2), 0.3 + 0.32 * j, 0])) for j in range(4) for i in range(int(w / 0.62) - 1)])
    boy = VGroup(Circle(radius=0.17, stroke_color=WHITE, stroke_width=3), Line(DOWN * 0.17, DOWN * 0.75, color=WHITE, stroke_width=3), Line(DOWN * 0.75, DOWN * 1.1 + LEFT * 0.2, color=WHITE, stroke_width=3), Line(DOWN * 0.75, DOWN * 1.1 + RIGHT * 0.2, color=WHITE, stroke_width=3),
                 Arc(radius=0.18, start_angle=PI * 1.15, angle=PI * 0.7, color="#D8D8E8", stroke_width=4).shift(DOWN * 0.12), Line(DOWN * 0.35 + LEFT * 0.35, UP * 0.35 + RIGHT * 0.6, color="#BFC6D0", stroke_width=3))
    boy.move_to(sky.get_center() + np.array([-1.2, -0.55, 0]))
    zha = Ellipse(width=0.45, height=0.2, stroke_width=0, fill_color="#6B4F3A", fill_opacity=1).next_to(boy, DOWN, buff=-0.15).shift(RIGHT * 0.05)
    g = VGroup(sky, glow, moon, sand, melons, boy, zha)
    g.parts = dict(sky=sky, moon=VGroup(glow, moon), sand=sand, melons=melons, boy=boy, zha=zha)
    return g


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 5
    TITLE = "My Old Home"
    SUBTITLE = "Lu Xun · a short story"
    SECTIONS = ["Lu Xun and his China", "Homecoming and memory", "Runtu: the boy and the man", "The other people", "Themes", "The wall and the road"]
    NEXT = "Unit 6 · The Half-closed Eyes of the Buddha and the Slowly Sinking Sun"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        sc = memory_scene().move_to([0, -0.2, 0])
        d = sc.parts
        with self.say("A golden moon in a deep blue sky. Below it, a seashore planted as far as the eye can see with jade green watermelons. And in the middle, a boy of eleven in a silver necklet, stabbing with a pitchfork at a small wild animal that slips between his legs."):
            self.play(FadeIn(d["sky"]), FadeIn(d["moon"], scale=0.6))
            self.play(FadeIn(d["sand"]), LaggedStart(*[FadeIn(m_, scale=0.5) for m_ in d["melons"]], lag_ratio=0.01), run_time=2)
            self.play(FadeIn(d["boy"]), FadeIn(d["zha"]))
            self.play(d["zha"].animate.shift(RIGHT * 1.6), run_time=1.2)
        master = T("\"Master!\"", size=48, color=th.CORAL, weight="BOLD").move_to([0, 0.2, 0])
        with self.say("Thirty years later, the same boy, now a worn out farmer, stands in front of his old friend, and says only one word. Master."):
            self.play(sc.animate.set_opacity(0.15))
            self.play(FadeIn(master, scale=1.3))
            nb = E.neby_in(self, "sad", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(sc, master)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 5: My Old Home, by the Chinese writer Lu Xun."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Lu Xun and his China. The homecoming, and a memory. Runtu, the boy and the man. The other people. The themes. And the story's two great images: the wall, and the road.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Lu Xun (1881–1936)")
        facts = E.bullets(["pen-name of Zhou Shuren, born in Shaoxing, south-east China", "his family's fortunes collapsed: years between pawnshops and pharmacies", "studied medicine in Japan — then gave it up: China needed healthy minds", "1918: A Madman's Diary, the first modern short story in spoken Chinese", "\"My Old Home\" (1921), collected in Call to Arms (1923)"], width=8.0, size=24)
        facts.scale_to_fit_height(min(facts.height, 5.0)).move_to([-2.0, -0.35, 0])
        side = VGroup(T("based on life", size=26, color=th.AMBER, weight="BOLD"), para("In 1919 he went home to sell the family house and take his mother north. But the story is fiction: the narrator is \"I\", not Lu Xun.", width=3.8, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.7, 0.2, 0])
        with self.say("Lu Xun is the pen name of Zhou Shuren, the founder of modern Chinese literature. Born in eighteen eighty one into a once wealthy family, he spent his boyhood between pawnshops and pharmacies after its collapse. He went to Japan to study medicine, then gave it up, deciding that his people needed healthy minds more than healthy bodies, and that literature could help. His story A Madman's Diary was the first modern story written in everyday spoken Chinese."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
        with self.say("My Old Home was written in nineteen twenty one. Like its narrator, Lu Xun went home in nineteen nineteen to sell the family house. But it is fiction based on experience: in the exam, call the speaker the narrator, not Lu Xun."):
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Home again — and not the home he remembered")
        grey = Rectangle(width=12.4, height=4.2, stroke_width=0, fill_color="#2A3140", fill_opacity=0.6).move_to([0, -0.3, 0])
        lines = VGroup(*[para(t_, width=11.4, size=26, color=c_) for t_, c_ in [("more than seven hundred miles by boat, in the depth of winter", th.INK), ("a grey sky, a cold wind, a few lifeless villages", th.MUTED), ("dry grass trembling on the roof of the old clan house — sold, to be handed over before New Year", th.INK), ("he decides: perhaps home was always like this; it is my mood that has changed", th.AMBER)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(grey)
        with self.say("The narrator travels more than seven hundred miles by boat, in the depth of winter, to the home he left twenty years before. A grey sky, a cold wind, a few lifeless villages. Is this the place he remembered? Perhaps it was always like this, he decides; only his mood has changed. He has come to say goodbye: the old house has been sold, and he is taking his mother and his little nephew Hongr to live where he now works."):
            self.play(FadeIn(h), FadeIn(grey))
            E.reveal_list(self, lines, 9.0)
        self.play(FadeOut(VGroup(h, grey, lines)))
        h = E.head(self, "One name, and a picture flashes back")
        sc = memory_scene(w=6.4, h=3.8).move_to([-3.0, -0.4, 0])
        facts = E.bullets(["thirty years ago, both about ten", "Runtu, a labourer's son, came to guard the vessels at a great sacrifice", "silver necklet: his father had pledged him to the gods", "he knew bird traps, coloured shells, two-legged fish, the zha", "the town boys saw only the sky above a high courtyard wall"], width=5.6, size=22).move_to([3.6, -0.3, 0])
        with self.say("Then his mother mentions Runtu, who always asks after him. At that name a picture flashes into his mind: the golden moon, the watermelons, the boy with the pitchfork. Thirty years ago, when the family was still rich, Runtu, the son of a part time labourer, came to help guard the ritual vessels at a great sacrifice. He wore a silver necklet, because his father had pledged him to the gods. Within hours the two boys were fast friends. Runtu knew wonders: how to trap birds in the snow, where to find shells of every colour, fish that jumped on two legs. The town boys, by contrast, only ever saw the four corners of sky above their courtyard wall."):
            self.play(FadeIn(h), FadeIn(sc))
            E.reveal_list(self, facts, 14.0)
        nt = para("Notice the colours: gold and jade in memory, grey in the present. Lu Xun lets the gap do the work.", width=11, size=24, color=th.AMBER).move_to([0, -3.0, 0])
        with self.say("Notice the colours: gold and jade in the memory, grey in the present. Lu Xun sets a warm memory beside a cold fact, and lets the gap speak."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, sc, facts, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "The boy and the man")
        left = ["about eleven", "round, crimson face", "silver necklet, felt cap", "steel pitchfork by moonlight", "knows birds, shells, the zha", "\"fast friends\""]
        right = ["about forty", "sallow, deeply lined face", "eyes swollen and red", "one thin padded jacket", "hands like the bark of a pine tree", "says \"Master!\""]
        lh = T("Runtu then", size=30, color=MOON, weight="BOLD").move_to([-3.3, 2.1, 0])
        rh = T("Runtu now", size=30, color=th.MUTED, weight="BOLD").move_to([3.3, 2.1, 0])
        lc = VGroup(*[T(t_, size=26, color=th.INK) for t_ in left]).arrange(DOWN, buff=0.32).next_to(lh, DOWN, buff=0.4)
        rc = VGroup(*[T(t_, size=26, color=th.CORAL if k == 5 else th.INK) for k, t_ in enumerate(right)]).arrange(DOWN, buff=0.32).next_to(rh, DOWN, buff=0.4)
        mid = DashedLine([0, 2.3, 0], [0, -2.9, 0], color=th.FAINT)
        with self.say("One cold afternoon Runtu arrives, and the narrator knows him at once, and yet this is not the Runtu he remembered. The boy was about eleven, round faced and crimson cheeked, in a silver necklet, brave with a pitchfork. The man is about forty: his face sallow and lined, his eyes swollen and red from the sea wind, one thin padded jacket against the cold, his hands cracked like the bark of a pine tree."):
            self.play(FadeIn(h), FadeIn(lh), FadeIn(rh), Create(mid))
            for a_, b_ in zip(lc[:5], rc[:5]):
                self.play(FadeIn(a_), FadeIn(b_), run_time=0.5)
                self.hold(1.2)
        wall = Rectangle(width=0.5, height=5.0, stroke_color=th.CORAL, stroke_width=3, fill_color=th.CORAL, fill_opacity=0.35).move_to([0, -0.3, 0])
        with self.say("The narrator is overjoyed and tongue tied; all the old talk of shells and birds sticks in his throat. Runtu's lips move without a sound. Then, respectfully, he says: Master. And the narrator shudders, because he knows at once what a lamentably thick wall has grown up between them."):
            self.play(FadeIn(lc[5]))
            self.play(FadeIn(rc[5], scale=1.3))
            self.play(ReplacementTransform(mid, wall))
        self.play(FadeOut(VGroup(h, lh, rh, lc, rc, wall)))
        h = E.head(self, "What has squeezed him dry")
        cs = ["many children", "famines", "taxes", "soldiers", "bandits", "officials", "landed gentry"]
        man = Circle(radius=0.7, stroke_color=th.AMBER, stroke_width=4).move_to([0, -0.45, 0])
        ml = T("Runtu", size=26, color=th.AMBER).move_to(man)
        chips = VGroup(*[E.chip(t_, th.CORAL, size=24).move_to(np.array([0, -0.45, 0]) + 2.25 * np.array([1.7 * np.cos(TAU * k / 7 + PI / 2), np.sin(TAU * k / 7 + PI / 2), 0])) for k, t_ in enumerate(cs)])
        with self.say("Asked about his life, Runtu shakes his head. Too many children, bad harvests, taxes, and everyone wanting money. His face does not move, like a stone statue. After he goes, the narrator and his mother count what has crushed him: many children, famines, taxes, soldiers, bandits, officials and gentry, squeezing him as dry as a mummy. There is no single villain. The pressure comes from the whole system."):
            self.play(FadeIn(h), Create(man), FadeIn(ml))
            for c_ in chips:
                self.play(FadeIn(c_, scale=0.7), run_time=0.45)
                self.hold(0.6)
            self.play(man.animate.scale(0.6), ml.animate.scale(0.75), *[c_.animate.shift((np.array([0, -0.45, 0]) - c_.get_center()) * 0.25) for c_ in chips], run_time=1.5)
        self.play(FadeOut(VGroup(h, man, ml, chips)))
        h = E.head(self, "What Runtu asks for")
        items = VGroup(*[E.card(t_, d_, c_, w=3.05, h=3.0, tsize=26, size=24) for t_, d_, c_ in [("tables, chairs", "two tables and four chairs: plain needs", th.SKY), ("a balance", "to weigh and sell", th.MINT), ("candlesticks", "and an incense burner: for worship", th.AMBER), ("stove ashes", "fertiliser for his fields", th.MUTED)]]).arrange(RIGHT, buff=0.2).move_to([0, 0.2, 0])
        with self.say("Offered whatever the family will not take, Runtu chooses two tables, four chairs, a balance, the ashes from the stove for his fields, and an incense burner with candlesticks. Remember those candlesticks. The narrator smiles at them now, and will turn the joke on himself at the end."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(i_, shift=UP * 0.2) for i_ in items], lag_ratio=0.4), run_time=3)
        self.play(FadeOut(VGroup(h, items)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        cards = VGroup(
            E.card("Mrs Yang, \"the Compass\"", "once the Beancurd Beauty; now all cheekbones, hands on hips, legs apart like a compass. Calls him rich, pockets his mother's gloves, accuses Runtu of hiding bowls in the ashes.", th.PINK, w=6.1, h=3.0, size=22),
            E.card("The narrator", "educated, gentle, honest about his own failings: silent before Mrs Yang, tongue-tied with Runtu, and finally doubting his own hope", th.SKY, w=6.1, h=3.0, size=22),
            E.card("Hongr and Shuisheng", "the narrator's nephew and Runtu's son make friends at once, with no master or servant between them", th.MINT, w=6.1, h=2.4, size=22),
            E.card("Mother", "practical and kind; she asks Runtu to call her son \"brother\" — and he refuses", th.AMBER, w=6.1, h=2.4, size=22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("The other people. Mrs Yang, once the Beancurd Beauty of the shop opposite, now stands with legs apart like the compass in a geometry box. She insists the narrator is rich, and walks off with his mother's gloves. She is comic, but Lu Xun does not condemn her: she too lives by picking up what others leave. The narrator himself is gentle and honest about his own failings."):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        with self.say("And two boys: Hongr, the narrator's nephew, and Shuisheng, Runtu's son, the image of young Runtu without the necklet. They become friends at once, exactly as their elders once did. When the mother asks Runtu to call her son brother, as he used to, Runtu refuses: he was a child then and did not understand."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("The barrier of class", "the \"thick wall\": built of habit, money and deference; invisible but high. Neither man built it; society did.", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Memory and reality", "gold and jade in memory, grey and bare in fact. Was the past ever as good as we remember?", MOON, w=6.1, h=2.75, size=24),
            E.card("Rural poverty", "children, famine, taxes, soldiers, bandits, officials: the peasant squeezed by a whole system", th.AMBER, w=6.1, h=2.75, size=24),
            E.card("Hope and the next generation", "the boys' friendship shows the wall is not natural — and could come down", th.MINT, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. The barrier of class is the centre: a thick wall made of money, habit and deference, invisible but high, and built by society, not by either man. Memory and reality: the golden memory against the grey present. Rural poverty: a peasant squeezed by a whole system. And hope in the next generation: the boys' friendship shows that the wall is not natural, and might come down."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        h = E.head(self, "Is the narrator's hope just another idol?")
        a = E.card("Runtu's idols", "incense burner and candlesticks: a hope in the gods, which the narrator smiles at", th.AMBER, w=5.4, h=2.6, size=24).move_to([-3.2, 0.5, 0])
        b = E.card("the narrator's idol", "his hope for a new life — \"an idol I had created myself\", only more remote", th.SKY, w=5.4, h=2.6, size=24).move_to([3.2, 0.5, 0])
        nt = para("Irony turned on himself: Lu Xun's honesty about the limits of the educated man's hope.", width=11, size=26, color=th.MINT).move_to([0, -2.2, 0])
        with self.say("Then the narrator catches himself. He had smiled at Runtu for wanting an incense burner and candlesticks, still worshipping idols. But what is his own hope for a new life, except an idol he has made himself, only further away? It is irony turned on himself, and it is what makes the ending honest."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Hope is like a road")
        ground = Rectangle(width=12.4, height=3.6, stroke_width=0, fill_color="#3A4A2A", fill_opacity=0.35).move_to([0, -0.9, 0])
        steps = VGroup()
        rng = np.random.default_rng(3)
        for k in range(46):
            t = k / 45
            x = -5.8 + 11.6 * t
            y = -0.9 + 0.9 * np.sin(t * PI * 1.2) + rng.uniform(-0.25, 0.25)
            steps.add(Ellipse(width=0.22, height=0.12, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.7).move_to([x, y, 0]).rotate(0.3))
        road = VMobject(stroke_color=th.AMBER, stroke_width=26, stroke_opacity=0.45).set_points_smoothly([[-5.8 + 11.6 * t, -0.9 + 0.9 * np.sin(t * PI * 1.2), 0] for t in np.linspace(0, 1, 30)])
        q = E.quote("when many men pass one way, a road is made", "the last line", width=8.0, size=32).move_to([0, 2.0, 0])
        with self.say("As the boat pulls away, the narrator feels no regret, only that invisible high wall. The picture of the boy among the watermelons blurs. He hopes Hongr and Shuisheng will never be parted, and that they will have a new life, unlike his and unlike Runtu's. Half asleep, he sees the jade green shore and the golden moon once more, and thinks: hope is like a road across the earth. To begin with there was no road. But when many people pass one way, a road is made."):
            self.play(FadeIn(h), FadeIn(ground))
            self.play(LaggedStart(*[FadeIn(s_, scale=0.5) for s_ in steps], lag_ratio=0.06), run_time=6)
            self.play(Create(road), run_time=2)
            self.play(FadeIn(q))
        nt = para("Not a promise but a call to action: hope exists only if people walk it into being.", width=11, size=26, color=th.MINT).move_to([0, -3.0, 0])
        with self.say("It is not a promise. It is a call to action: hope exists only if enough people walk it into being. And notice the frame: the same golden moon that opened the memory now closes the story, the past turned into a dream of the future."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, ground, steps, road, q, nt)))
        rows = [["frame", "the golden moon, start and end", "memory becomes hope"], ["contrast", "the boy and the man; gold and grey", "the story's main method"], ["simile", "hands \"like the bark of a pine tree\"", "harsh, exact pictures"],
                ["symbol", "the wall; the necklet; the road", "small things, big meanings"], ["irony", "he smiles at idols, then finds his own", "honesty about himself"], ["metaphor", "the \"thick wall\"; hope as a road", "abstractions given shape"]]
        E.device_slide(self, rows, "Devices to quote. A frame: the golden moon at the start of the memory and again at the end. Contrast, the story's main method. Similes that are harsh and exact: hands like pine bark, a woman like a compass. Symbols: the wall, the necklet, the idols, the road. Irony turned on the narrator. And metaphor: the thick wall, and hope as a road.", widths=(2.9, 5.6, 3.9), size=22)
        self.quiz("What does Runtu's word \"Master!\" reveal to the narrator?",
                  ["Runtu is joking", "a wall of class divides them", "Runtu has forgotten him", "Runtu wants a job"], 1,
                  "Pause and think.",
                  "The habit of deference shows the invisible but high wall that poverty and class have built.")
        self.quiz("In the last line, hope is compared to",
                  ["a golden moon", "a road made by walking", "a high wall", "a silver necklet"], 1,
                  "One more.",
                  "There were no roads at first; when many people pass one way, a road is made.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Lu Xun (1881–1936), pen-name of Zhou Shuren; \"My Old Home\" (1921), in Call to Arms.",
            "A winter homecoming; a golden memory of the boy Runtu among the watermelons.",
            "Runtu now: worn out, silent, and calling him \"Master\" — the thick wall.",
            "Themes: class, memory vs reality, rural poverty, hope in the children.",
            "His own hope may be an idol; yet a road is made when many walk one way.",
        ], "Quick recap. Lu Xun, and a story from nineteen twenty one. A grey homecoming and a golden memory. A friend who now says Master, and the thick wall of class. And a hope that is honest about itself: a road made by walking.")
        self.outro("That was My Old Home. Next, a story from Nepal: The Half-closed Eyes of the Buddha and the Slowly Sinking Sun. See you there.")
