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
    UNIT = 1
    TITLE = "Neighbours"
    SUBTITLE = "Tim Winton · a short story"
    SECTIONS = ["The writer and his Australia", "The story, season by season", "What crosses the fence", "The characters", "Themes", "How it is told"]
    NEXT = "Unit 2 · A Respectable Woman"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    def street(self):
        left = E.house(th.CORAL, label="Macedonian family").move_to([-4.6, -0.6, 0])
        mid = E.house(th.SKY, label="the young couple").move_to([0, -0.6, 0])
        right = E.house(th.AMBER, label="Polish widower").move_to([4.6, -0.6, 0])
        f1, f2 = E.fence(-2.3, -1.4, 0.2), E.fence(2.3, -1.4, 0.2)
        return VGroup(left, mid, right), VGroup(f1, f2)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        houses, fences = self.street()
        VGroup(houses, fences).scale(1.15).move_to([0, -0.5, 0])
        noise = VGroup(*[Arc(radius=0.35 + 0.25 * k, start_angle=-PI / 4, angle=PI / 2, color=th.CORAL, stroke_width=4).move_arc_center_to(houses[0][0].get_right() + RIGHT * 0.1) for k in range(3)])
        q1 = T("murder?", size=30, color=th.CORAL, weight="BOLD").move_to([0, 2.4, 0])
        q2 = T("no — just talking", size=30, color=th.MINT, weight="BOLD").move_to([0, 2.4, 0])
        with self.say("A young couple move into a crowded street. On one side, a Macedonian family who shout so loudly that for six months the newcomers think they are murdering each other. They are not. They are just talking."):
            self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.2) for h_ in houses], lag_ratio=0.25), FadeIn(fences))
            self.play(LaggedStart(*[Create(n_) for n_ in noise], lag_ratio=0.2), FadeIn(q1))
            self.play(ReplacementTransform(q1, q2))
        q3 = T("Can strangers become family without sharing a single word?", size=30, color=th.AMBER).move_to([0, 2.4, 0])
        q3.scale_to_fit_width(min(q3.width, 12.4))
        with self.say("Nobody in this street shares a language with the couple. Yet within one year, these strangers will be cheering at dawn for a baby that is not theirs. How?"):
            self.play(FadeOut(noise), ReplacementTransform(q2, q3))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(houses, fences, q3)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 1: Neighbours, a very short story by the Australian writer Tim Winton."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. The writer and his Australia. The story, season by season. What crosses the fence. The characters. The themes. And how the story is told: point of view, structure and devices.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Tim Winton (born 1960)")
        facts = E.bullets(["born in Perth, grew up in Perth and Albany, Western Australia", "first novel An Open Swimmer published at 22 (1982)", "Miles Franklin Award four times: Shallows, Cloudstreet, Dirt Music, Breath", "twice shortlisted for the Booker Prize", "\"Neighbours\" is in his first story collection, Scission (1985)"], width=7.4, size=24).move_to([-2.4, 0.2, 0])
        style = VGroup(T("his style", size=26, color=th.AMBER, weight="BOLD"), *[para(t_, width=4.0, size=24, color=th.BODY) for t_ in ["ordinary, unliterary people", "plain, short, physical prose", "place as a character"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.2, 0])
        with self.say("Tim Winton was born in nineteen sixty in Perth and grew up in Western Australia. He published his first novel at twenty two, and has since won Australia's top fiction prize, the Miles Franklin Award, four times. Neighbours comes from his first collection of stories, Scission, from nineteen eighty five."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 6.0)
        with self.say("Three things about his writing matter here. He writes about ordinary people. His prose is plain and physical: smells, sounds, actions, almost never a stated feeling. And place does the emotional work, like a character."):
            self.play(LaggedStart(*[FadeIn(s_) for s_ in style], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, facts, style)))
        h = E.head(self, "1980s Australia: a multicultural street")
        df = E.card("Multiculturalism", "several cultures living side by side in one society, publicly accepted, instead of minorities being expected to disappear into the majority", th.MINT, w=6.2, h=3.0).move_to([-3.2, 0.2, 0])
        ctx = E.bullets(["official Australian policy from the 1970s", "post-war migrants from southern and eastern Europe settled in the inner suburbs", "Winton's street: Macedonian, Polish, Italian and Greek families"], width=5.2, size=24).move_to([3.6, 0.2, 0])
        with self.say("The story is set in the nineteen eighties, when Australia had officially adopted multiculturalism: many cultures accepted side by side, rather than migrants being expected to melt into the majority. Families from southern and eastern Europe had long settled in the cheaper inner suburbs. Winton's street, with Macedonian, Polish, Italian and Greek neighbours, is what that policy looked like on the ground."):
            self.play(FadeIn(h), FadeIn(df))
            E.reveal_list(self, ctx, 4.5)
        self.play(FadeOut(VGroup(h, df, ctx)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "A year in one street: closeness rises season by season")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 7, 1], x_length=11.6, y_length=4.4, tips=False, axis_config={"color": th.FAINT, "stroke_width": 2, "include_ticks": False}).move_to([0, -0.3, 0])
        xs = [0.0, 1.4, 2.9, 4.2, 5.4, 6.6, 7.5, 8.5, 9.3, 10.0]
        ys = [0.6, 0.8, 1.9, 2.7, 3.3, 4.4, 3.7, 4.7, 5.3, 6.1]
        curve = E.arc_curve(ax, xs, ys, color=th.AMBER)
        yl = T("closeness", size=22, color=th.MUTED).rotate(PI / 2).next_to(ax, LEFT, buff=0.1)
        seasons = VGroup(*[T(t_, size=22, color=th.MUTED).move_to(ax.c2p(x, -0.55)) for t_, x in [("arrival", 0.9), ("autumn", 3.4), ("winter", 5.4), ("spring", 6.6), ("summer", 8.0), ("birth", 9.7)]])
        with self.say("Almost nothing dramatic happens in Neighbours. There is no villain and no crisis. What changes is a relationship, and Winton measures it in seasons. Let us walk through the year."):
            self.play(FadeIn(h), Create(ax), FadeIn(yl), FadeIn(seasons))
            self.play(Create(curve), run_time=2.5)
        graph = VGroup(ax, curve, yl, seasons)
        self.play(graph.animate.scale(0.62).move_to([0, 1.15, 0]))
        marks = [0.0, 2.9, 4.2, 5.4, 6.6, 7.5, 10.0]
        pts = [ax.c2p(x, float(np.interp(x, xs, ys))) for x in marks]
        dot = Dot(pts[0], radius=0.13, color=th.CORAL)
        self.play(FadeIn(dot, scale=1.5))
        steps = [
            ("Arrival", "They feel \"like sojourners in a foreign land\": spitting, shouting, watering at dawn. The Pole hammers nails in and pulls them out. The neighbours judge them back: a wife who works, a husband who stays home.", th.SKY,
             "They arrive wary. Raised in quiet outer suburbs, they feel like visitors in a foreign land. The Macedonians shout, the old Polish widower hammers nails into wood and pulls them out again, and a little boy urinates in the street. The disapproval runs both ways: the neighbours frown at a wife who goes out to work while the husband stays home writing a thesis."),
            ("Autumn: the garden", "They dig a vegetable patch under the neighbours' watching eyes. Advice comes over the fence. He resents it — but takes careful note. She strokes the boy's shaved head and is given garlic to plant.", th.MINT,
             "In autumn they dig a vegetable garden, and the garden brings the neighbours to the fence with advice. The young man resents it, but, tellingly, he takes careful note of what is said. His wife is bolder: she runs a hand over the little boy's shaved head, and the big woman next door gives her garlic to plant."),
            ("The henhouse", "Their henhouse falls down. The Polish widower slides through the fence uninvited and rebuilds it. They cannot understand a word he says.", th.AMBER,
             "They build a henhouse, and the neighbours watch it fall down. Then the old Polish widower slips through the fence, uninvited, and rebuilds it for them. Winton adds one flat sentence: they could not understand a word he said. That is the heart of the story."),
            ("Winter: exchange", "Cabbages go over the fence; grappa and firewood come back. They stop walking with lowered eyes, and feel \"superior and proud\" when their own parents look shocked.", th.PINK,
             "In winter, gifts start crossing. The couple give away cabbages and receive grappa and firewood. They no longer walk with their eyes lowered. And when their own parents visit and look shocked at the neighbours, the couple feel superior and proud, which shows how far they have come, and that a little pride is still there."),
            ("Spring: the ducks", "The Macedonians teach them to kill and pluck their ducks. On buckets, in down and steam and half-understood stories, the couple end up shouting too.", th.CORAL,
             "In spring the Macedonian family teach them to slaughter and pluck their ducks. Everyone sits on buckets telling barely understood stories, and the couple feel almost drunk with it. By the end they are shouting too, behaving exactly like the neighbours whose noise once appalled them."),
            ("The pregnancy", "An unplanned baby. The street takes over: chocolates from the deli man, names from Italian women, a knitted suit. Just as he means to complain about the Pole's noisy garage, the old man brings a barrow of firewood.", th.SKY,
             "Then an unplanned pregnancy, and the street takes it over. The deli man presses chocolates on her, Italian women offer names, Greek women feel her belly, and the woman next door knits a baby suit. The Pole finally builds with his wood: a two car garage, though he has no car. Just as the young man is about to complain about the noise, the old man arrives with a barrowful of firewood for them."),
            ("The birth", "A home birth through the night. Twelve faces at the fences. At dawn, a queue of neighbours cheering. He weeps: the novels he studies \"had not prepared him for this\".", th.AMBER,
             "The baby comes at home, through the night. Fetching wood at dusk, the young man counts twelve faces at the fences. A boy is born at dawn, and on the Macedonian side a queue of sleepy faces looks up and cheers. He begins to weep. The twentieth century novel, he realises, had not prepared him for this."),
        ]
        for k, (t_, d_, c_, say) in enumerate(steps):
            tt = T(t_, size=32, color=c_, weight="BOLD").move_to([0, -0.85, 0])
            dd = para(d_, width=11.2, size=26, color=th.INK).next_to(tt, DOWN, buff=0.3)
            with self.say(say):
                self.play(dot.animate.move_to(pts[k]).set_color(c_), FadeIn(tt, shift=UP * 0.2))
                self.play(FadeIn(dd))
            self.play(FadeOut(VGroup(tt, dd)))
        self.play(FadeOut(VGroup(h, graph, dot)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "The plot is what crosses the fence")
        houses, fences = self.street()
        sc = VGroup(houses, fences).scale(0.8).move_to([0, -0.9, 0])
        items = [("advice", th.MINT, 0, 1), ("garlic", th.MINT, 0, 1), ("a rebuilt henhouse", th.AMBER, 2, 1), ("cabbages", th.SKY, 1, 0), ("grappa, firewood", th.PINK, 0, 1), ("duck-killing lessons", th.CORAL, 0, 1),
                 ("a knitted suit", th.CORAL, 0, 1), ("a barrow of firewood", th.AMBER, 2, 1), ("a cheer at dawn", th.MINT, 0, 1)]
        shown = VGroup()
        with self.say("Here is the best way to answer the exam question, what happens in this story. Do not say nothing. Say the plot is a change of relationship, and prove it with the things that cross the fences. Advice. Garlic. A rebuilt henhouse. Cabbages going one way, grappa and firewood coming back. Lessons in killing ducks. A knitted suit. A barrow of wood. And finally, a cheer."):
            self.play(FadeIn(h), FadeIn(sc))
            for k, (t_, c_, a, b) in enumerate(items):
                ch = E.chip(t_, c_, size=22).move_to(houses[a][0].get_top() + UP * 0.6)
                self.play(FadeIn(ch, scale=0.7), run_time=0.25)
                self.play(ch.animate.move_to(houses[b][0].get_center()), run_time=0.45)
                tgt = E.chip(t_, c_, size=22).move_to([-5.0 + 3.35 * (k % 4), 2.0 - 0.6 * (k // 4), 0])
                self.play(Transform(ch, tgt), run_time=0.3)
                shown.add(ch)
        nt = para("Not one line of dialogue crosses the fences. Everything that matters is a thing or an action.", width=11, size=26, color=th.AMBER).move_to([0, -3.0, 0])
        with self.say("Notice: not a single line of dialogue crosses those fences in the whole story. Everything that matters is an object or an action."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, sc, shown, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "The characters — and nobody has a name")
        cards = VGroup(
            E.card("The young man", "a thesis-writer on the modern novel; well-meaning but quietly snobbish. He senses, resents, assumes, suspects — until he weeps.", th.SKY, w=4.1, h=4.1, size=24),
            E.card("The young woman", "works at a hospital; braver and quicker. Makes the first touch of friendship; does the hardest, most heroic work: the birth.", th.PINK, w=4.1, h=4.1, size=24),
            E.card("The Polish widower", "old, alone, building nothing — until a garage for a man with no car. Gives most, receives least, never in words.", th.AMBER, w=4.1, h=4.1, size=24),
        ).arrange(RIGHT, buff=0.2).move_to([0, 0.35, 0])
        mac = para("The Macedonian family: they begin as noise and end as a choir. The loudness and frankness the couple hated turn out to be the same quality as their generosity.", width=11.6, size=24, color=th.CORAL).move_to([0, -2.65, 0])
        with self.say("The characters. Watch the young man's verbs in the first half: he senses disapproval, resents advice, assumes why the boy's head is shaved, suspects the old man of annoying him on purpose. He reads the street like a text, from a distance. His wife has fewer lines but more courage: she makes the first friendly touch, and at the birth Winton gives her all the heroic words."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards[:2]], lag_ratio=0.3))
        with self.say("The Polish widower is the most moving figure and the one we know least. He rebuilds their henhouse and brings them firewood, and they never understand a word he says. And the Macedonian family begin as noise and end as a choir, cheering at the fence."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(FadeIn(mac))
        self.play(FadeOut(VGroup(cards, mac)))
        why = E.bullets(["names are learned by talking — across these fences no one can tell theirs", "so the narrator honestly withholds them", "it makes the story representative: any couple, any migrant street", "and makes the ending stronger: strangers act like family without ever being introduced"], width=11.4, size=26).move_to([0, 0.0, 0])
        with self.say("Notice that nobody in the story has a name. A name is something someone tells you, and across these fences nobody can. So the narrator withholds them. This makes the story representative, any couple in any migrant street, and it makes the ending stronger: these people behave like family without ever having been introduced."):
            E.reveal_list(self, why, 8.0)
        self.play(FadeOut(VGroup(h, why)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Community across language", "people can belong to each other without a shared language: garlic, labour and a cheer do what words cannot", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Prejudice, slowly corrected", "not hatred but the mild, educated, superior kind — corrected by time and closeness, not argument. And it runs both ways.", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Books against life", "he studies the modern novel of loneliness and irony; the street teaches him what books could not", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Birth as a shared event", "the great events are of the body and cannot be private: one baby, a whole street awake", th.AMBER, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Four themes. First, community across language: people can belong to each other without sharing words. Second, prejudice and its slow correction. The couple's prejudice is not hatred; it is the mild, educated, superior kind, the hardest kind to see in yourself, and Winton corrects it with time and closeness, not with an argument. He is fair, too: the neighbours judge the couple as well."):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        with self.say("Third, book learning against lived experience. The young man studies the modern novel, famous for loneliness and irony, while the real lesson happens outside his window. Fourth, birth as a shared, physical event: one baby keeps a whole street awake."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.play(FadeOut(cards))
        q = E.quote("The twentieth century novel had not prepared him for this.", "the last line", width=9.5, size=34).move_to([0, 0.6, 0])
        nt = para("Irony: the man who studies literature is educated by a street he once looked down on.", width=10.5, size=26, color=th.AMBER).move_to([0, -1.8, 0])
        with self.say("And the last line settles the contest between books and life. The twentieth century novel had not prepared him for this. The man who studies literature is educated by a street he once looked down on. That is irony, and it is the story's whole argument in a sentence."):
            self.play(FadeIn(q))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(q, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Point of view: free indirect style")
        q = E.quote("The child's head was shaved regularly, he assumed, in order to make his hair grow thick.", width=9.5, size=28).move_to([0, 1.2, 0])
        ex = E.bullets(["third person, past tense, but limited to the young man's mind", "the narrator's words take on HIS attitudes, without quotation marks", "\"he assumed\" quietly warns us: he invents explanations for people he does not know", "so the reader's prejudice is corrected at the same speed as his"], width=11.4, size=24).move_to([0, -1.5, 0])
        with self.say("How is it told? In the third person, but limited almost entirely to the young man: a technique called free indirect style, where the narrator's words take on a character's attitudes without quotation marks. Read this sentence. The guess about the shaved head is his, not the narrator's, and the little words he assumed warn us that he is inventing reasons for people he does not know. Because we see through his eyes, our own prejudice is corrected at the same speed as his."):
            self.play(FadeIn(h), FadeIn(q))
            E.reveal_list(self, ex, 8.0)
        self.play(FadeOut(VGroup(h, q, ex)))
        h = E.head(self, "Structure: two harvests at once")
        tl = E.timeline(["autumn: garden planted, baby conceived", "winter: gifts", "spring: ducks, pregnancy", "summer: the street's celebration", "the birth: garden and child both ripe"], x0=-6.2, x1=6.2, y=0.2, colors=[th.MINT, th.SKY, th.CORAL, th.PINK, th.AMBER], size=22, wrap=2.5)
        nt = para("No chapters, no scene breaks: the seasons are the structure. The vegetable cycle and the human cycle run in parallel.", width=11, size=26, color=th.INK).move_to([0, -2.6, 0])
        with self.say("The structure. There are no chapters or scene breaks; the seasons are the structure. The garden is planted in autumn, and the child is conceived in autumn too; both come to harvest at the end. That parallel is why such a plotless story feels complete."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.3))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, tl, nt)))
        rows = [["understatement", "\"They could not understand a word he said.\"", "flatness makes kindness huge"], ["irony", "the novel \"had not prepared him for this\"", "the scholar is taught by the street"],
                ["sensory imagery", "vermilion sunsets, wood smoke", "feeling built from things"], ["list", "\"flattered, claustrophobic, grateful, peeved\"", "honest, mixed emotion"],
                ["symbol", "the fence; the lumber; the garden", "barrier; waste; growth"], ["sound motif", "shouting → crooning → cheering", "the noise they hate, they finally join"]]
        E.device_slide(self, rows, "The devices to quote. Understatement: they could not understand a word he said, so flat that the kindness feels enormous. Irony in the last line. Sensory imagery, sunsets and wood smoke, instead of named feelings. Lists, including a list of mixed feelings. Symbols: the fence, the lumber, the garden. And a motif of sound that runs from shouting to a cheer.", widths=(2.8, 5.2, 4.4), size=22)
        self.quiz("Why does nobody in \"Neighbours\" have a name?",
                  ["Winton forgot to name them", "no one can tell their names", "the story is a true account", "to hide the setting"], 1,
                  "Pause and think.",
                  "Names are learned by talking, and nobody can talk across these fences; it also makes the story stand for any migrant street.")
        self.quiz("Which act first breaks the barrier completely, without a word?",
                  ["the duck killing", "the deli man's chocolates", "the rebuilt henhouse", "the parents' visit"], 2,
                  "One more.",
                  "The Polish widower rebuilds their henhouse, and they cannot understand a word he says.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Tim Winton (b. 1960); \"Neighbours\" from Scission (1985); 1980s multicultural Australia.",
            "A year in one street: garden, henhouse, gifts, ducks, pregnancy, birth.",
            "The plot is what crosses the fence: advice, garlic, labour, firewood, a cheer.",
            "Themes: community without language, mild prejudice corrected, books vs life, shared birth.",
            "Free indirect style through the young man; seasons as structure; no names; ironic last line.",
        ], "Quick recap. Winton and the multicultural Australia of the eighties. One year in one street, season by season. The plot as the things that cross the fence. Themes of community, prejudice, books and life. And the telling: free indirect style, the seasons, no names, and an ironic last line.")
        self.outro("That was Neighbours. Next, a story about a woman, her husband's guest, and a feeling she will not name: A Respectable Woman. See you there.")
