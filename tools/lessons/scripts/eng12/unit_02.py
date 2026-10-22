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
    UNIT = 2
    TITLE = "A Respectable Woman"
    SUBTITLE = "Kate Chopin · a short story"
    SECTIONS = ["Kate Chopin and Louisiana", "The story", "The bench", "The characters", "Themes", "The ending and the craft"]
    NEXT = "Unit 3 · A Devoted Son"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        q = E.quote("Oh, I have overcome everything! You will see. This time I shall be very nice to him.", "Mrs. Baroda, the last line", width=9.5, size=32).move_to([0, 1.0, 0])
        r1 = T("she has conquered the temptation?", size=28, color=th.MINT).move_to([0, -1.4, 0])
        r2 = T("or she has conquered her scruples?", size=28, color=th.CORAL).move_to([0, -2.2, 0])
        with self.say("A married woman laughs, kisses her husband, and says: Oh, I have overcome everything! This time I shall be very nice to him. Readers have argued about that sentence for a hundred and thirty years."):
            self.play(FadeIn(q))
        with self.say("Has she overcome the temptation? Or has she overcome her resistance to it? By the end of this lesson, you will be able to argue both, and say why the writer chose not to tell us."):
            self.play(FadeIn(r1, shift=UP * 0.2))
            self.play(FadeIn(r2, shift=UP * 0.2))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(q, r1, r2)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 2: A Respectable Woman, by Kate Chopin."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Kate Chopin and her Louisiana. The story. The night on the bench. The characters. The themes. And the ending, with the craft that makes it work.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Kate Chopin (1850–1904)")
        tl = E.timeline(["1850: born in St. Louis; raised in a house of women", "1870: marries, moves to Louisiana", "1882: widowed; begins writing", "1894: this story, in Vogue", "1899: The Awakening — savaged", "1950s on: rediscovered"],
                        x0=-6.3, x1=6.3, y=0.2, colors=[th.SKY, th.MINT, th.MUTED, th.AMBER, th.CORAL, th.PINK], size=22, wrap=2.3)
        with self.say("Kate Chopin was born in eighteen fifty in St. Louis. Her father died when she was five, and she grew up in a house run by women: her mother, grandmother and great grandmother. She married and moved to Louisiana, was widowed in eighteen eighty two, and began writing in her late thirties. This story first appeared in Vogue magazine in eighteen ninety four. Her novel The Awakening, about a wife who leaves her husband, was attacked as indecent in eighteen ninety nine, and her career never recovered, until critics rediscovered her in the twentieth century."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.5), run_time=6)
        self.play(FadeOut(VGroup(h, tl)))
        h = E.head(self, "Local colour — and what lies under it")
        df = E.card("Local colour", "fiction devoted to one region's speech, dress, customs and landscape", th.AMBER, w=5.6, h=2.4).move_to([-3.3, 0.9, 0])
        ex = E.bullets(["a sugar plantation, a portico with Corinthian pillars", "the batture by the river, grosbec birds, live oaks", "French words: ma belle, chère amie, tête-à-tête"], width=5.6, size=24).move_to([3.3, 0.9, 0])
        under = para("But the region is only the surface. Underneath is her real subject: the inner life of women, and the roles society hands them.", width=11, size=28, color=th.MINT).move_to([0, -2.0, 0])
        with self.say("Chopin made her name as a local colour writer, recording one region's speech and customs: the Creole sugar country of Louisiana, with its pillared porches, river banks, and French phrases. But in her best stories the region is only the surface. Her real subject is the inner life of women, and the roles their society hands them."):
            self.play(FadeIn(h), FadeIn(df))
            E.reveal_list(self, ex, 4.0)
            self.play(FadeIn(under))
        self.play(FadeOut(VGroup(h, df, ex, under)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        steps = [
            ("The unwelcome guest", "Her husband Gaston invites his college friend Gouvernail, a journalist. She wanted rest and her husband to herself. She pictures the man — tall, cynical, eyeglasses — and dislikes the picture.", th.SKY,
             "Mrs. Baroda is a little provoked: her husband Gaston has invited an old college friend, Gouvernail, a journalist, to stay on their sugar plantation. She wanted rest, and her husband to herself. She has never met the man, but she imagines him, tall, cynical, in eyeglasses, and on that evidence, which is no evidence at all, she dislikes him."),
            ("The man who arrives", "He is nothing like her picture — and she rather likes him, without knowing why. He is quiet, courteous, and makes no effort at all to win her approval.", th.MINT,
             "The real Gouvernail is nothing like her picture, and to her surprise she rather likes him, without knowing why. He is quiet and perfectly polite, but he makes no effort at all to win her approval. He simply does not need it."),
            ("Piqued", "He wants nothing: he smokes on the portico, likes the dogs, won't fish or shoot. Ignored, her vanity is stung. She leaves him alone — he doesn't mind. So she forces her company on him.", th.AMBER,
             "He wants nothing. He sits on the portico, smoking, saying this is what I call living. He makes friends with the dogs and has no wish to fish or shoot. A hostess whose skill is supplying what guests want has nothing to do, and she is piqued: her vanity is stung. She leaves him alone; he does not mind. So she forces her company on him, trying to break through his reserve."),
            ("The quarrel", "\"He tires me frightfully.\" — \"But he gives you no trouble.\" — \"I should like him better if he did.\" She announces she will go to the city tomorrow.", th.CORAL,
             "She complains to Gaston that the friend tires her frightfully. Gaston is puzzled: the man gives her no trouble. I should like him better if he did, she answers, a reply that gives away more than she knows. She announces she will go to the city in the morning."),
            ("The bench", "That night, alone under a live oak, she is confused. A red cigar-point approaches: Gouvernail. He sits beside her and, at last, talks freely in the dark.", th.PINK,
             "That night she sits alone on a bench under a live oak, more confused than she has ever been. A red point of light approaches: a lighted cigar, so it must be Gouvernail, because her husband does not smoke. He sits beside her, and in the dark his reserve melts, and he talks."),
            ("Flight and return", "She tells no one, takes the early train, and stays away till he has gone. She refuses a summer visit. Then, before the year ends, she herself proposes he come again.", th.SKY,
             "She tells nobody, takes the early train to the city, and does not come back until he has left. When Gaston wants him back in summer, she strongly objects. Then, before the year is out, she herself proposes that Gouvernail visit again."),
        ]
        h = E.head(self, "Classical shape — all of it inside her head")
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 6, 1], x_length=11.4, y_length=4.0, tips=False, axis_config={"color": th.FAINT, "stroke_width": 2, "include_ticks": False}).move_to([0, -0.4, 0])
        xs, ys = [0.0, 2.6, 3.9, 5.2, 6.3, 7.4, 8.6, 10.0], [1.0, 2.0, 2.9, 3.9, 5.2, 3.4, 2.5, 3.0]
        cv = E.arc_curve(ax, xs, ys, color=th.AMBER)
        stages = VGroup(*[T(t_, size=22, color=c_).move_to(ax.c2p(x, -0.6)) for t_, x, c_ in [("exposition", 1.4, th.MUTED), ("rising action", 4.4, th.MUTED), ("climax", 6.3, th.CORAL), ("falling", 7.9, th.MUTED), ("resolution?", 9.5, th.AMBER)]])
        pk = T("the bench", size=24, color=th.CORAL, weight="BOLD").next_to(ax.c2p(6.3, 5.2), UP, buff=0.15)
        with self.say("The story follows the classic shape exactly: exposition, rising action, a climax on the bench, falling action, and a resolution. What is unusual is that every stage happens inside her mind, and the resolution resolves nothing. Let us walk along it."):
            self.play(FadeIn(h), Create(ax), FadeIn(stages))
            self.play(Create(cv), run_time=2.5)
            self.play(FadeIn(pk))
        g = VGroup(ax, cv, stages, pk)
        self.play(g.animate.scale(0.62).move_to([0, 1.1, 0]))
        marks = [0.0, 2.6, 3.9, 5.2, 6.3, 8.6]
        pts = [ax.c2p(x, float(np.interp(x, xs, ys))) for x in marks]
        dot = Dot(pts[0], radius=0.13, color=th.CORAL)
        self.play(FadeIn(dot, scale=1.5))

        for k, (t_, d_, c_, say) in enumerate(steps):
            tt = T(t_, size=32, color=c_, weight="BOLD").move_to([0, -0.85, 0])
            dd = para(d_, width=11.2, size=26, color=th.INK).next_to(tt, DOWN, buff=0.3)
            with self.say(say):
                self.play(dot.animate.move_to(pts[k]).set_color(c_), FadeIn(tt, shift=UP * 0.2))
                self.play(FadeIn(dd))
            self.play(FadeOut(VGroup(tt, dd)))
        self.play(FadeOut(VGroup(h, g, dot)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "In the dark: a voice, a quotation, a confession")
        cig = VGroup(Dot(color=th.CORAL, radius=0.08), Circle(radius=0.22, color=th.CORAL, stroke_width=2).set_stroke(opacity=0.5)).move_to([5.5, 1.6, 0])
        q1 = E.quote("Night of south winds — night of the large few stars! Still nodding night —", "Whitman, quoted by Gouvernail", width=7.0, size=28).move_to([-1.6, 1.0, 0])
        q2 = E.quote("a desire to be permitted to exist, with now and then a little whiff of genuine life", "Gouvernail", width=7.0, size=28).move_to([-1.6, -1.6, 0])
        with self.say("In the dark, a red cigar point comes up the gravel walk. Gouvernail sits down, and half to himself he quotes Walt Whitman: night of south winds, night of the large few stars. Whitman was America's great poet of the body and of open desire, so the quotation says what the characters cannot. Then he talks of his old ambitions, and of what is left: only a wish to exist, with now and then a little whiff of genuine life."):
            self.play(FadeIn(h), FadeIn(cig))
            self.play(cig.animate.move_to([4.2, 0.2, 0]), run_time=1.5)
            self.play(FadeIn(q1))
            self.play(FadeIn(q2))
        self.play(FadeOut(VGroup(q1, q2, cig)))
        her = Dot([-0.6, -0.2, 0], radius=0.22, color=th.PINK)
        him = Dot([1.6, -0.2, 0], radius=0.22, color=th.SKY)
        hl = VGroup(T("Mrs. Baroda", size=24, color=th.PINK).next_to(her, DOWN, buff=0.25), T("Gouvernail", size=24, color=th.SKY).next_to(him, DOWN, buff=0.25))
        bar = ValueTracker(0)
        meter = always_redraw(lambda: VGroup(Rectangle(width=0.5, height=0.05 + 3.0 * bar.get_value(), stroke_width=0, fill_color=th.CORAL, fill_opacity=0.85).move_to([-5.0, -1.6, 0], aligned_edge=DOWN)))
        ml = T("impulse", size=24, color=th.CORAL).move_to([-5.0, -2.0, 0])
        q3 = para("\"The stronger the impulse grew to bring herself near him, the further, in fact, did she draw away from him.\"", width=11.6, size=28, color=th.AMBER).move_to([0, 2.0, 0])
        with self.say("Her mind barely follows his words; she is drinking in his voice. She wants to touch his face in the dark, to whisper against his cheek, as she might have done, Chopin writes, if she had not been a respectable woman. Then the sentence on which the story turns: the stronger the impulse grew to bring herself near him, the further did she draw away."):
            self.play(FadeIn(her), FadeIn(him), FadeIn(hl), FadeIn(ml), FadeIn(meter))
            self.play(bar.animate.set_value(1.0), her.animate.shift(LEFT * 2.6), hl[0].animate.shift(LEFT * 2.6), run_time=3.5)
            self.play(FadeIn(q3))
        nt = para("Antithesis: one sentence holds the whole conflict — desire measured against restraint.", width=11, size=26, color=th.MINT).move_to([0, -3.0, 0])
        with self.say("That is antithesis: one sentence that holds the whole conflict, desire and restraint pulling in opposite directions. She gets up and leaves. Gouvernail, completely unaware, lights another cigar."):
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, her, him, hl, meter, ml, q3, nt)))
        q4 = E.quote("Besides being a respectable woman she was a very sensible one; and she knew there are some battles in life which a human being must fight alone.", width=10.0, size=30).move_to([0, 0.4, 0])
        with self.say("She thinks of telling her husband, who is also her friend, and decides not to. Besides being a respectable woman, she was a very sensible one, and she knew there are some battles in life which a human being must fight alone."):
            self.play(FadeIn(q4))
        self.play(FadeOut(q4))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        cards = VGroup(
            E.card("Mrs. Baroda", "not wicked, not weak: a woman meeting the first situation her social training can't handle. It begins in vanity, not love — she is \"piqued\" at being ignored.", th.PINK, w=4.1, h=4.0, size=24),
            E.card("Gouvernail", "the catalyst who does nothing. Quiet, tired, self-contained, wanting only a \"whiff of genuine life\". He never suspects what he stirs.", th.SKY, w=4.1, h=4.0, size=24),
            E.card("Gaston", "frank, affectionate, talkative, trusting. He stands for the safe, happy marriage — and its blindness: he never learns a thing.", th.AMBER, w=4.1, h=4.0, size=24),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.4, 0])
        nt = para("Symbols: the red cigar (his presence in the dark) · her white gown and the white scarf her husband sends (visible respectability)", width=11.6, size=24, color=th.MUTED).move_to([0, -2.5, 0])
        with self.say("Three characters. Mrs. Baroda is not wicked and not weak; she has simply never met a situation her training could not handle, and notice that it begins in vanity: she is piqued at being ignored. Gouvernail is the catalyst who does nothing at all, which is exactly the point. Gaston is warm, frank and trusting: the safe marriage, and its blindness, since he never learns a thing. Even objects speak: the red cigar in the dark, her white gown that gives her away, and the white scarf her husband sends out."):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.5), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(cards, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        cards = VGroup(
            E.card("Desire vs respectability", "\"respectable\" is a social word, about how a woman is seen. Her impulse is checked by an identity, not by conscience.", th.CORAL, w=6.1, h=2.75, size=24),
            E.card("The inner life is the real life", "outwardly: a guest comes, a wife shops, a guest leaves. The real events leave no trace.", th.SKY, w=6.1, h=2.75, size=24),
            E.card("Self-knowledge", "she learns she can want a man who doesn't try; that her body can overrule her mind; that some things can't be shared", th.MINT, w=6.1, h=2.75, size=24),
            E.card("Marriage and its limits", "a happy, loving marriage can still leave a woman entirely alone with what matters most", th.AMBER, w=6.1, h=2.75, size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.1, 0])
        with self.say("Four themes. Desire against respectability: respectable is a social word, about how a woman is seen, and what stops her is an identity, not her conscience. Chopin's quiet boldness is to show the impulse as natural and the restraint as coming from outside. Second, the inner life is the real life: outwardly, a guest comes and goes."):
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        with self.say("Third, self knowledge: she learns three things she never knew about herself. Fourth, marriage and its limits: a warm, loving marriage can still leave a woman completely alone with the thing that matters most. This awakening is what Chopin would expand, five years later, into a whole novel."):
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "\"I have overcome everything!\" — three readings")
        cards = VGroup(
            E.card("Virtue has won", "she has mastered the attraction, so the visit is safe. \"Overcome\" means conquered.", th.MINT, w=3.9, h=3.0, size=24),
            E.card("Scruple has gone", "what she has overcome is her resistance; she invites him because she means to act. \"Nice\" is a promise.", th.CORAL, w=3.9, h=3.0, size=24),
            E.card("Chopin won't say", "the words fit both. The reader must supply the moral — exactly the discomfort the story wants.", th.AMBER, w=3.9, h=3.0, size=24),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.2, 0])
        tip = para("In the exam: give both readings, the evidence for each, and why Chopin left it open. Don't pretend to certainty.", width=11.4, size=24, color=th.INK).move_to([0, -2.6, 0])
        with self.say("Now the ending. Reading one: virtue has won. She has mastered the feeling, so she can safely invite him back. Reading two: what she has overcome is her resistance, and being very nice to him is a promise. Reading three: Chopin arranged the words so that both fit, and handed the moral judgement to us. In the exam, give the readings, the evidence for each, and say why the ending is left open."):
            self.play(FadeIn(h))
            for c_ in cards:
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tip))
        self.play(FadeOut(VGroup(h, cards, tip)))
        rows = [["situational irony", "she dislikes him unseen; is drawn to him when ignored", "her judgement — and ours — overturned"], ["free indirect style", "\"he tires me frightfully\"", "we share her view before we question it"],
                ["antithesis", "the stronger the impulse … the further she drew away", "the whole conflict in one sentence"], ["allusion", "Whitman's night of south winds", "says what the characters cannot"],
                ["euphemism", "\"this folly that had seized her\"", "her own words refuse to name desire"], ["foreshadowing", "\"I should like him better if he did\"", "she confesses without knowing"], ["open ending", "\"I have overcome everything!\"", "the reader must judge"]]
        E.device_slide(self, rows, "The devices to quote. Situational irony: she dislikes the man she has never met and is drawn to the man who ignores her. Free indirect style. The antithesis on the bench. Allusion to Whitman. Euphemism: she calls her desire only a folly. Foreshadowing: I should like him better if he did give me trouble. And the open ending.", widths=(2.9, 5.3, 4.3), size=22, y=0.3)
        self.quiz("Why is Mrs. Baroda first annoyed by Gouvernail?",
                  ["he insults her", "he needs nothing from her", "he flirts with her", "he quarrels with Gaston"], 1,
                  "Pause and think.",
                  "He makes no appeal for her approval; her vanity is piqued long before anything like love.")
        self.quiz("\"The stronger the impulse grew … the further did she draw away.\" This is",
                  ["a simile", "antithesis", "onomatopoeia", "a rhetorical question"], 1,
                  "One more.",
                  "Antithesis: opposing ideas balanced in one sentence — desire against restraint.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Kate Chopin (1850–1904): Louisiana local colour; the inner life of women.",
            "Guest Gouvernail, disliked unseen, then unsettling because he needs nothing.",
            "The bench: Whitman, his voice, the impulse — and she draws away.",
            "Themes: desire vs respectability, self-knowledge, the limits of a happy marriage.",
            "Open ending: has she overcome the temptation, or her resistance?",
        ], "Quick recap. Chopin, and her Louisiana. A guest disliked before he arrives, and unsettling because he wants nothing. The night on the bench, where the stronger the impulse, the further she draws away. Desire against respectability. And an ending that can be read two ways.")
        self.outro("That was A Respectable Woman. Next: A Devoted Son, by Anita Desai, a story of a perfect son and a father who wants a sweet. See you there.")
