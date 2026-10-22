import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

MUD = "#5B4A36"


def wing(color=th.MUTED, s=1.0, flip=False):
    pts = [[0, 0, 0], [0.9, 0.7, 0], [1.9, 0.9, 0], [2.6, 0.5, 0], [2.2, 0.15, 0], [2.5, -0.15, 0], [1.9, -0.25, 0], [2.1, -0.55, 0], [1.3, -0.45, 0], [0.6, -0.3, 0], [0, 0, 0]]
    w = VMobject(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25).set_points_as_corners(pts).scale(s)
    if flip:
        w.flip(UP)
    return w


def old_man(s=1.0):
    head = Circle(radius=0.3, stroke_color=th.INK, stroke_width=3)
    body = Line(DOWN * 0.3, DOWN * 1.2, color=th.INK, stroke_width=3)
    legs = VGroup(Line(DOWN * 1.2, DOWN * 1.8 + LEFT * 0.3, color=th.INK, stroke_width=3), Line(DOWN * 1.2, DOWN * 1.8 + RIGHT * 0.3, color=th.INK, stroke_width=3))
    wl = wing(s=0.8, flip=True).next_to(body, LEFT, buff=-0.05).shift(UP * 0.2)
    wr = wing(s=0.8).next_to(body, RIGHT, buff=-0.05).shift(UP * 0.2)
    return VGroup(wl, wr, head, body, legs).scale(s)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 7
    TITLE = "A Very Old Man with Enormous Wings"
    SUBTITLE = "Gabriel García Márquez · a short story"
    SECTIONS = ["Márquez and magical realism", "An angel in the mud", "From wonder to sideshow", "Decline and flight", "Characters and themes", "How the magic is told"]
    NEXT = "Unit 8 · A Day"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        mud = Rectangle(width=12.4, height=1.6, stroke_width=0, fill_color=MUD, fill_opacity=0.6).move_to([0, -2.2, 0])
        man = old_man(1.1).rotate(-PI / 2).move_to([0, -1.6, 0])
        rain = VGroup(*[Line([x, 3.3 - 0.6 * (k % 4), 0], [x - 0.15, 2.9 - 0.6 * (k % 4), 0], color=th.SKY, stroke_width=2) for k, x in enumerate(np.linspace(-6, 6, 30))])
        q = para("After three days of rain, a man finds a very old man face down in the mud of his courtyard — with enormous, dirty wings.", width=11, size=28, color=th.INK).move_to([0, 1.9, 0])
        with self.say("After three days of rain, a man throwing dead crabs into the sea finds something groaning at the back of his courtyard: a very old man, face down in the mud, who cannot get up because of his enormous, dirty wings."):
            self.play(FadeIn(rain), FadeIn(mud))
            self.play(FadeIn(man), FadeIn(q))
        q2 = T("an angel? — so the village charges five cents to stare", size=28, color=th.AMBER).move_to([0, 0.55, 0])
        with self.say("Is he an angel? The village is not sure. So it does the most human thing possible: it charges five cents to look at him."):
            self.play(FadeIn(q2))
            nb = E.neby_in(self, "surprised", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(mud, man, rain, q, q2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 7: A Very Old Man with Enormous Wings, by Gabriel García Márquez."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Márquez and magical realism. An angel in the mud. From wonder to sideshow. Decline and flight. The characters and themes. And how the magic is told.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Gabriel García Márquez (1927–2014)")
        facts = E.bullets(["born in Aracataca, Colombia; raised by his grandparents", "his grandmother told ghosts and omens in a flat, calm voice", "journalist, then novelist: One Hundred Years of Solitude (1967)", "Nobel Prize in Literature, 1982", "this story: 1968, subtitled \"A Tale for Children\"; trans. Gregory Rabassa"], width=8.2, size=24).move_to([-2.0, 0.2, 0])
        side = VGroup(T("\"Gabo\"", size=30, color=th.AMBER, weight="BOLD"), para("that calm telling of marvels became his own voice", width=3.6, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.4, 0])
        with self.say("Gabriel García Márquez, known as Gabo, was born in nineteen twenty seven in Aracataca, a small town in Colombia, and raised by his grandparents. His grandmother told stories of ghosts and omens in a flat, matter of fact voice, and that voice became his own. A journalist turned novelist, he wrote One Hundred Years of Solitude and won the Nobel Prize in nineteen eighty two. This story is from nineteen sixty eight."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))
        h = E.head(self, "Magical realism")
        df = E.card("Magical realism", "impossible events told in the same matter-of-fact tone as ordinary ones, so the magic seems part of everyday life. Nobody explains it; nobody marvels for long.", th.PINK, w=10.0, h=2.6).move_to([0, 0.9, 0])
        ex = VGroup(T("an angel arrives …", size=28, color=th.AMBER), T("… smelling of the outdoors, and is fed eggplant mush", size=28, color=th.INK)).arrange(DOWN, buff=0.2).move_to([0, -1.7, 0])
        with self.say("This is the classic example of magical realism: impossible events told in exactly the same calm tone as ordinary ones, so the magic feels like part of everyday life. The narrator never explains it, and the characters soon find it a nuisance rather than a marvel. An angel arrives, and he smells of the outdoors and is fed eggplant mush."):
            self.play(FadeIn(h), FadeIn(df))
            self.play(FadeIn(ex))
        self.play(FadeOut(VGroup(h, df, ex)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "Who is he? Everyone has an answer")
        man = old_man(1.0).move_to([0, 0.0, 0])
        verdicts = [("Pelayo and Elisenda", "a castaway from a wrecked ship", th.SKY, [-4.4, 1.4, 0]), ("the neighbour woman", "an angel, come for the sick child", th.MINT, [4.4, 1.4, 0]),
                    ("Father Gonzaga", "too human: he doesn't know Latin — an impostor?", th.AMBER, [-4.4, -1.6, 0]), ("the crowd", "make him mayor of the world, or a general!", th.CORAL, [4.4, -1.6, 0])]
        cs = VGroup(*[E.card(a_, b_, c_, w=4.2, h=2.0, tsize=26, size=24).move_to(p_) for a_, b_, c_, p_ in verdicts])
        with self.say("Pelayo fetches his wife Elisenda. The old man is nearly bald, nearly toothless, dressed like a ragpicker, his wings like a buzzard's, dirty and half plucked. He answers them in an unknown dialect with a sailor's voice, so they sensibly decide he is a castaway. The neighbour woman, who knows everything about life and death, needs one look: he is an angel, come for their sick child. Father Gonzaga, the priest, greets him in Latin; he does not understand, and up close he seems much too human. He writes to his bishop, who will write to Rome. And the crowd dreams of making him mayor of the world."):
            self.play(FadeIn(h), FadeIn(man))
            for c_ in cs:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.6)
                self.hold(3.0)
        self.play(FadeOut(VGroup(h, man, cs)))
        h = E.head(self, "Into the chicken coop")
        coop = VGroup(Rectangle(width=4.0, height=2.6, stroke_color=th.MUTED, stroke_width=3), *[Line([-2.0 + 0.4 * k, -1.3, 0], [-2.0 + 0.4 * k, 1.3, 0], color=th.FAINT, stroke_width=1.5) for k in range(1, 10)]).move_to([-3.0, -0.3, 0])
        man = old_man(0.7).move_to(coop)
        facts = E.bullets(["locked in with the hens", "that night the rain stops; the child's fever breaks", "they plan to set him adrift on a raft …", "… but at dawn the whole village is at the wire, throwing food \"as if he were a circus animal\""], width=6.0, size=24).move_to([3.3, -0.3, 0])
        with self.say("Pelayo locks him in the chicken coop with the hens. That night the rain stops and the baby's fever breaks. Feeling generous, the couple plan to put the angel on a raft with food and water and leave him to the sea. But at dawn the whole neighbourhood is at the wire, throwing in food as if he were a circus animal."):
            self.play(FadeIn(h), Create(coop), FadeIn(man))
            E.reveal_list(self, facts, 8.0)
        self.play(FadeOut(VGroup(h, coop, man, facts)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Five cents a look")
        coin = VGroup(Circle(radius=0.7, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.25), T("5¢", size=36, color=GOLD, weight="BOLD")).move_to([-4.6, 0.6, 0])
        crowd = VGroup(*[Dot([x, -2.2 + 0.25 * (k % 3), 0], radius=0.12, color=th.PALETTE[k % 8]) for k, x in enumerate(np.linspace(-6.2, 6.2, 40))])
        facts = E.bullets(["Elisenda's idea: fence the yard and charge admission", "pilgrims and invalids: a woman who counted her heartbeats, a man kept awake by the noise of the stars", "within a week the rooms are crammed with money"], width=8.0, size=24).move_to([1.6, 0.8, 0])
        with self.say("The courtyard becomes a marketplace, and soldiers have to break up the mob. Elisenda, aching from sweeping up the litter, has an idea: fence the yard and charge five cents to see the angel. Pilgrims come from far away: a woman who has counted her heartbeats since childhood and run out of numbers, a man kept awake by the noise of the stars. Within a week the house is crammed with money."):
            self.play(FadeIn(h), FadeIn(coin))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in crowd], lag_ratio=0.03))
            E.reveal_list(self, facts, 7.0)
        self.play(FadeOut(VGroup(h, coin, crowd, facts)))
        h = E.head(self, "His only virtue: patience")
        ab = E.bullets(["hens peck at his wings; cripples pull out his feathers", "even the kind throw stones to make him stand up", "he refuses mothballs (\"angels' food\") and eats only eggplant mush", "they burn his side with a branding iron to see if he is alive", "he wakes in tears, beats his wings in a storm of dung and dust"], width=11.0, size=26).move_to([0, -0.1, 0])
        nt = T("\"a cataclysm in repose\"", size=30, color=th.CORAL, weight="BOLD").move_to([0, -2.9, 0])
        with self.say("The angel takes no part in his own show. His only supernatural virtue seems to be patience. Hens peck at him, invalids tear out his feathers, even kind people throw stones to make him stand. He refuses mothballs, which the neighbour says angels eat, and lives on eggplant mush. Once, when he lies so still they think he is dead, they burn his side with a branding iron. He wakes in tears, shouting in his unknown language, and beats his wings in a storm of dust. After that they are careful: his calm was not that of a hero at rest, but of a cataclysm in repose."):
            self.play(FadeIn(h))
            E.reveal_list(self, ab, 14.0)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, ab, nt)))
        h = E.head(self, "Beaten by a spider woman")
        a = E.card("the angel", "aloof, silent, smelly; costs five cents; his \"miracles\" are absurd: a blind man grows three new teeth, a leper's sores sprout sunflowers", th.SKY, w=5.8, h=3.9, size=24).move_to([-3.1, 0.2, 0])
        b = E.card("the spider woman", "cheaper; you may question her; a sad girl's head on a ram-sized tarantula, changed for disobeying her parents. \"So much human truth\" and a clear moral.", th.CORAL, w=5.8, h=3.9, size=24).move_to([3.1, 0.2, 0])
        nt = para("The crowd leaves. The courtyard is as empty as when it rained.", width=10, size=28, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Meanwhile the Church investigates whether he has a navel and whether his dialect is Aramaic. Then a providential event: a travelling show brings a woman who was changed into a spider for disobeying her parents. She is cheaper, you may ask her questions, and her sad story has so much human truth and so clear a moral that she easily defeats the aloof angel, whose miracles are faintly ridiculous: a blind man who grows three new teeth instead of sight, a leper whose sores sprout sunflowers. The crowd leaves, and the courtyard is as empty as when it rained."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(a.animate.set_opacity(0.35), FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "A mansion with bars against angels")
        facts = E.bullets(["the money builds a two-storey mansion", "iron bars on the windows \"so that angels wouldn't get in\"", "Pelayo keeps rabbits; Elisenda buys satin shoes", "the child plays in the rotting coop; he and the angel catch chicken pox together", "the doctor finds the wings so natural he wonders why other men lack them"], width=11.0, size=26).move_to([0, 0.0, 0])
        with self.say("The couple have no complaints. With the money they build a two storey mansion, with iron bars on the windows so that angels can't get in. Pelayo gives up his job and keeps rabbits; Elisenda buys satin shoes. The child grows up and plays in the rotting coop, and he and the angel catch chicken pox together. The doctor who listens to the angel's chest finds so many noises he seems impossible alive, but the wings look so natural that the doctor wonders why other men don't have them."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 14.0)
        self.play(FadeOut(VGroup(h, facts)))
        h = E.head(self, "Decline — and flight")
        sea = Line([-6.4, -2.4, 0], [6.4, -2.4, 0], color=th.SKY, stroke_width=4)
        man = old_man(0.6).move_to([-4.6, -1.6, 0])
        path = VMobject().set_points_smoothly([[-4.6, -1.6, 0], [-2.4, -1.4, 0], [0, -0.2, 0], [3.0, 1.2, 0], [5.8, 2.2, 0]])
        q = para("Elisenda sighs with relief, \"for herself and for him\", until he is only \"an imaginary dot on the horizon of the sea\".", width=6.0, size=26, color=th.AMBER).move_to([-2.6, 1.3, 0])
        with self.say("The coop collapses. The angel drags himself about the house like a stray dying man; Elisenda chases him out with a broom and cries that it is awful living in a hell full of angels. One winter he has a fever, and they fear he will die. But he survives, and with the spring sun, stiff new feathers grow, which he hides. One morning, while Elisenda is cutting onions, a wind from the sea blows in. She watches his clumsy first attempts, nails ploughing the vegetable patch, and then he gains height. She sighs with relief, for herself and for him, until he is only an imaginary dot on the horizon of the sea."):
            self.play(FadeIn(h), Create(sea), FadeIn(man))
            self.hold(6.0)
            self.play(MoveAlongPath(man, path), run_time=3)
            self.play(man.animate.scale(0.12), run_time=1)
            self.play(FadeIn(q))
        self.play(FadeOut(VGroup(h, sea, man, q)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("The old man", "never understood, never identified: angel, castaway, \"a Norwegian with wings\"? Human in every detail — and endlessly patient. He leaves on his own terms.", th.SKY, w=6.1, h=3.0, size=24),
            E.card("Pelayo and Elisenda", "ordinary, neither hero nor villain: too kind to club him, scared enough to cage him, quick to profit. Elisenda is the business brain.", th.AMBER, w=6.1, h=3.0, size=24),
            E.card("Father Gonzaga", "the Church: cautious, sceptical, slow — writing to Rome while the crowd moves on", th.MINT, w=6.1, h=2.4, size=24),
            E.card("The crowd", "curiosity, greed, cruelty — and fickleness: a spider woman wins", th.CORAL, w=6.1, h=2.4, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("The characters. The old man is never identified: angel, castaway, or a Norwegian with wings. He is human in every detail, smelly, sick and old, and endlessly patient, and in the end he leaves on his own terms. Pelayo and Elisenda are neither heroes nor villains: too kind to kill him, scared enough to cage him, quick to make money. Father Gonzaga is the slow, sceptical Church. And the crowd is curious, greedy, cruel, and fickle."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))
        cards = VGroup(
            E.card("Wonder turned to spectacle", "a miracle met with entertainment and profit instead of awe", th.PINK, w=6.1, h=2.75, size=24),
            E.card("Greed and commercialism", "faith becomes a business; the profits build a house barred against angels", GOLD, w=6.1, h=2.75, size=24),
            E.card("Cruelty to the weak", "stones, a branding iron, a broom: the old and helpless treated as a curiosity", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("Appearance and reality", "an \"angel\" who is filthy, sick and old; comic miracles. What is an angel, really?", th.SKY, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Themes. Wonder turned into spectacle: the main irony is that a miracle is met with entertainment and profit rather than awe. Greed: faith becomes business, and the profits build a house with bars against angels. Cruelty to the weak and old. And appearance and reality: this angel is filthy, sick and old, so what is an angel, really? Behind them all, the old man's final flight is the story's one moment of freedom."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.6), run_time=6)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "The trick: the marvellous told like a rumour")
        a = VGroup(T("the extraordinary", size=28, color=th.PINK, weight="BOLD"), *[T(t_, size=24, color=th.INK) for t_ in ["a man with wings", "a woman turned into a spider", "sunflowers from a leper's sores"]]).arrange(DOWN, buff=0.3).move_to([-3.3, 0.6, 0])
        b = VGroup(T("the ordinary tone", size=28, color=th.MINT, weight="BOLD"), *[T(t_, size=24, color=th.INK) for t_ in ["he smells; he has lice", "admission is cheaper", "\"consolation miracles\""]]).arrange(DOWN, buff=0.3).move_to([3.3, 0.6, 0])
        nt = para("Because nobody marvels, the reader sees what the villagers do with a marvel — and that is the satire.", width=11, size=26, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("How is the magic told? Every impossible thing is described in the flattest everyday terms. A man with wings, and he has lice. A woman turned into a spider, and she is cheaper to see. Healing miracles, and they are consolation prizes. Because nobody in the story truly marvels, we see clearly what ordinary people do with a marvel, and that is the satire."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))
        rows = [["magical realism", "an angel fed eggplant mush", "magic made ordinary"], ["irony", "bars to keep angels out", "profit from the miracle"], ["satire", "does he have a navel?", "mocks authority"],
                ["imagery", "\"like powdered light\"", "beauty in squalor"], ["simile", "a dog with no illusions", "dignity in suffering"], ["open ending", "\"an imaginary dot\"", "the mystery stays"]]
        E.device_slide(self, rows, "Devices to quote. Magical realism itself. Irony: a mansion with bars to keep angels out, built with angel money. Satire on authority: the Church asks whether he has a navel. Imagery of beauty in squalor. Simile: the patience of a dog who had no illusions. And an open ending: he becomes an imaginary dot on the horizon, and we never learn what he was.", widths=(3.0, 5.4, 4.0), size=22)
        self.quiz("Why does the crowd abandon the angel?",
                  ["he flies away", "a spider woman with a moving story draws them", "the priest forbids visits", "he becomes violent"], 1,
                  "Pause and think.",
                  "The spider woman is cheaper, talks, and has \"so much human truth\": the fickle crowd moves on.")
        self.quiz("What makes this story magical realism?",
                  ["it is set in the future", "magic is told in a calm, everyday tone", "it has a happy ending", "the narrator is an angel"], 1,
                  "One more.",
                  "Impossible events are reported as matter-of-factly as ordinary ones.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "García Márquez (1927–2014), Nobel 1982; this tale 1968; magical realism.",
            "A winged old man in the mud: castaway, angel, or impostor?",
            "Caged, shown for five cents, tormented — then beaten by a spider woman.",
            "A mansion barred against angels; decline; new feathers; flight.",
            "Themes: wonder made spectacle, greed, cruelty, appearance vs reality.",
        ], "Quick recap. García Márquez and magical realism. A winged old man in the mud. A coop, five cents a look, and a spider woman who steals the show. A house barred against angels, and a final flight. Wonder turned into spectacle.")
        self.outro("That was A Very Old Man with Enormous Wings. Next we turn to poetry: A Day, by Emily Dickinson. See you there.")
