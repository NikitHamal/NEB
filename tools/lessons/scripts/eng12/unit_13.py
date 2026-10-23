import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

OAK = "#8A5A33"


def shelf(w=4.0, rows=4, color=OAK, seed=1, density=1.0):
    rng = np.random.default_rng(seed)
    frame = Rectangle(width=w, height=rows * 0.62 + 0.1, stroke_color=color, stroke_width=4)
    books = VGroup()
    for r in range(rows):
        y = frame.get_top()[1] - 0.06 - 0.62 * (r + 1)
        x = frame.get_left()[0] + 0.1
        while x < frame.get_right()[0] - 0.2:
            bw = rng.uniform(0.09, 0.2)
            if rng.uniform() < density:
                bh = rng.uniform(0.38, 0.56)
                books.add(Rectangle(width=bw, height=bh, stroke_width=0, fill_color=th.PALETTE[int(rng.integers(0, 8))], fill_opacity=0.8).move_to([x + bw / 2, y + bh / 2, 0]))
            x += bw + 0.02
        books.add(Line([frame.get_left()[0], y, 0], [frame.get_right()[0], y, 0], color=color, stroke_width=3))
    return VGroup(frame, books)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 13
    TITLE = "On Libraries"
    SUBTITLE = "Oliver Sacks · an essay"
    SECTIONS = ["Oliver Sacks", "The library at home", "Willesden: a good learner", "Science, Oxford and the vaults", "New York: space and strangers", "The empty shelves"]
    NEXT = "Unit 14 · Marriage as a Social Institution"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        full = shelf(5.0, 4, seed=3).move_to([-3.2, 0.2, 0])
        empty = shelf(5.0, 4, seed=3, density=0.12).move_to([3.2, 0.2, 0])
        la = T("where he became himself", size=26, color=th.MINT).next_to(full, DOWN, buff=0.3)
        lb = T("decades later: thrown out", size=26, color=th.CORAL).next_to(empty, DOWN, buff=0.3)
        with self.say("For most people a library is a place where you must be quiet. For Oliver Sacks, it was the place where he became himself."):
            self.play(FadeIn(full), FadeIn(la))
        with self.say("His essay is a warm memory of every library he loved, and then, in its last two paragraphs, a shock: the shelves are being emptied, because students now find everything on a screen."):
            self.play(FadeIn(empty), FadeIn(lb))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(full, empty, la, lb)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 13: On Libraries, an essay by Oliver Sacks."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Oliver Sacks. The library at home. Willesden, where he was a good learner. Science, Oxford and the vaults. New York: space and strangers. And the empty shelves.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Oliver Sacks (1933–2015)")
        facts = E.bullets(["born in London to two doctors; studied medicine at Oxford", "from 1965 a neurologist in New York for nearly fifty years", "wrote about patients as human beings, not cases", "Awakenings (1973), The Man Who Mistook His Wife for a Hat (1985)", "\"the poet laureate of medicine\""], width=7.6, size=24).move_to([-2.4, 0.2, 0])
        side = E.card("a personal essay", "first person, memories moving towards an opinion — praise of intellectual freedom, community and serendipity", th.AMBER, w=4.4, h=3.4, size=24).move_to([4.4, 0.2, 0])
        with self.say("Oliver Sacks was born in London in nineteen thirty three, the son of two doctors. He studied medicine at Oxford and from nineteen sixty five worked as a neurologist in New York for nearly fifty years. He became famous for writing about his patients as human beings rather than cases, in books like Awakenings. The New York Times called him the poet laureate of medicine. This is a personal essay: first person, memories that move towards an opinion. The textbook calls it a praise of intellectual freedom, community, and the joy of lucky discovery."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 9.0)
            self.play(FadeIn(side))
        self.play(FadeOut(VGroup(h, facts, side)))
        h = E.head(self, "Thirteen paragraphs, three movements")
        bar = VGroup(Rectangle(width=8.4, height=0.7, stroke_width=0, fill_color=th.MINT, fill_opacity=0.6), Rectangle(width=1.9, height=0.7, stroke_width=0, fill_color=th.SKY, fill_opacity=0.6), Rectangle(width=1.9, height=0.7, stroke_width=0, fill_color=th.CORAL, fill_opacity=0.7)).arrange(RIGHT, buff=0).move_to([0, 0.6, 0])
        labs = VGroup(T("1–9 childhood and youth", size=24, color=th.MINT).next_to(bar[0], DOWN, buff=0.25), T("10–11 New York", size=22, color=th.SKY).next_to(bar[1], UP, buff=0.25), T("12–13 the turn", size=24, color=th.CORAL).next_to(bar[2], DOWN, buff=0.25))
        nt = para("Eleven paragraphs of gratitude, then two of loss — and nothing warns you the turn is coming.", width=10.5, size=26, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("The essay has thirteen short paragraphs in three movements: childhood and youth, adult life in New York, and then the turn. Eleven paragraphs of gratitude, then two of loss, and nothing warns you that the turn is coming. That is why it hits so hard."):
            self.play(FadeIn(h), LaggedStart(*[GrowFromEdge(b_, LEFT) for b_ in bar], lag_ratio=0.5), FadeIn(labs))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, bar, labs, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "An oak-panelled room")
        sh = shelf(4.6, 4, seed=7).move_to([-3.6, -0.2, 0])
        items = E.bullets(["his father's Hebrew books, all of Ibsen", "young poets of the Great War, \"many killed\"", "on the low shelves: his brothers' adventure books — Kipling's The Jungle Book; he became Mowgli", "his mother's Dickens, Trollope, Shaw, Shakespeare", "medical books in a locked cabinet — the key left in the door", "he read at three or four; late for meals, they knew where to look"], width=6.6, size=22).move_to([3.0, -0.2, 0])
        with self.say("His favourite room as a child was the family library: oak panelled, every wall lined with books. His father's Hebrew scholarship and all of Ibsen's plays. The young poets of the Great War, many of them killed. On the lowest shelves, where a small boy could reach, his older brothers' adventure books, including Kipling's Jungle Book: he identified with the wolf boy Mowgli. His mother's Dickens and Shaw. Medical books in a locked cabinet, with the key left in the door. He learned to read at three or four, and when he was late for a meal, the family knew where to look."):
            self.play(FadeIn(h), FadeIn(sh))
            E.reveal_list(self, items, 14.0)
        self.play(FadeOut(VGroup(h, sh, items)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Willesden Public Library: the \"Ur-library\"")
        ur = E.card("Ur-", "German: original, archetypal. The first library, against which every later one was measured.", th.AMBER, w=4.8, h=3.0, size=24).move_to([-3.7, 0.9, 0])
        q = E.quote("not a good pupil, but … a good learner", "Sacks", width=6.2, size=32).move_to([2.8, 0.9, 0])
        nt = E.bullets(["at school, information went \"in one ear and out by the other\"", "he had to learn actively: what he wanted, in his own way", "at the library he felt free — to roam, to choose, \"to become myself\"", "and enjoyed \"the quiet companionship of other readers\""], width=11.4, size=24).move_to([0, -2.1, 0])
        with self.say("The library that mattered most was not at home but Willesden Public Library, five minutes' walk away. He calls it his Ur library: Ur is a German prefix meaning the original, the first of all libraries. There, he says, he received his real education. He disliked school; in class, information went in one ear and out the other. He could not learn passively. He was not a good pupil, but a good learner. In the library he roamed the shelves freely, followed what fascinated him, became himself, and enjoyed the quiet companionship of other readers on quests of their own."):
            self.play(FadeIn(h), FadeIn(ur))
            self.play(FadeIn(q))
            E.reveal_list(self, nt, 9.0)
        self.play(FadeOut(VGroup(h, ur, q, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Hunting for the books that weren't there")
        tl = E.timeline(["St Paul's Walker Library: strong in history, weak in chemistry", "a testimonial gets him into the Science Museum library: Mellor, Gmelin", "Oxford: the Radcliffe and the Bodleian (1602)", "the Bodleian: Theodore Hook, who improvised 500 operas"], x0=-6.2, x1=6.2, y=0.1, colors=[th.MUTED, th.SKY, th.AMBER, th.PINK], size=22, wrap=2.8)
        with self.say("As he grew, his reading leaned to astronomy and chemistry. His school's Walker Library was excellent in history but weak in science, so a teacher wrote him a testimonial that got him into the Science Museum library, where he devoured huge chemistry treatises. At Oxford he had the Radcliffe Science Library and the Bodleian, which goes back to sixteen oh two. There he stumbled on Theodore Hook, a forgotten nineteenth century wit said to have improvised more than five hundred operas, and decided to write his life. The lesson: one library cannot hold everything; a hungry reader goes looking."):
            self.play(FadeIn(h), GrowArrow(tl.line))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), FadeIn(l_)) for d_, l_ in zip(tl.dots, tl.labels)], lag_ratio=0.6), run_time=8)
        self.play(FadeOut(VGroup(h, tl)))
        h = E.head(self, "The Queen's College vaults: the catacombs")
        building = VGroup(Rectangle(width=5.0, height=1.4, stroke_color=th.INK, stroke_width=3), T("Wren's library", size=24, color=th.INK)).move_to([-3.2, 1.6, 0])
        building[1].move_to(building[0])
        ground = Line([-6.2, 0.8, 0], [-0.2, 0.8, 0], color=th.MUTED, stroke_width=3)
        vault = VGroup(shelf(4.6, 3, color=th.MUTED, seed=11)).move_to([-3.4, -0.9, 0])
        finds = E.bullets(["incunabula: books printed before 1501", "Gesner (1551), with Dürer's rhinoceros", "Darwin, all in first editions", "Sir Thomas Browne: \"how magnificent the language!\"", "Johnson, Hume, Pope, Swift — \"just sitting on the shelves\""], width=5.4, size=22).move_to([3.7, 0.0, 0])
        with self.say("But the Oxford library he loved most was his own college's, the Queen's College. Above ground, a building by Christopher Wren. Beneath it, in an underground maze of heating pipes and shelves, the catacombs. There he held incunabula, books printed before fifteen oh one, a sixteenth century book of animals with Dürer's rhinoceros, and all of Darwin's works in first editions. He fell in love with the magnificent language of Sir Thomas Browne, and met Johnson, Hume, Pope and Swift. And they were not locked away; they were just sitting on the shelves. There, he says, he gained a sense of history and of his own language."):
            self.play(FadeIn(h), FadeIn(building), Create(ground))
            self.play(FadeIn(vault))
            E.reveal_list(self, finds, 10.0)
        self.play(FadeOut(VGroup(h, building, ground, vault, finds)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "New York, 1965: from a fridge-top to the stacks")
        fridge = VGroup(RoundedRectangle(corner_radius=0.1, width=1.4, height=2.6, stroke_color=th.MUTED, stroke_width=3), Line([-0.7, 0.3, 0], [0.7, 0.3, 0], color=th.MUTED, stroke_width=2)).move_to([-4.8, -0.2, 0])
        pad = Rectangle(width=0.9, height=0.12, stroke_width=0, fill_color=th.INK, fill_opacity=0.9).next_to(fridge, UP, buff=0)
        fl = para("a \"horrid, pokey little apartment\": he wrote part of Migraine on top of the refrigerator", width=3.6, size=22, color=th.MUTED).next_to(fridge, DOWN, buff=0.25)
        table = VGroup(Rectangle(width=4.0, height=0.15, stroke_width=0, fill_color=OAK, fill_opacity=1), *[Line([x, 0, 0], [x, -1.0, 0], color=OAK, stroke_width=4) for x in (-1.8, 1.8)]).move_to([1.4, -0.6, 0])
        tl = para("the Albert Einstein College of Medicine library: a large table, and stacks to wander — \"unexpected treasures, lucky finds\"", width=6.2, size=24, color=th.MINT).move_to([2.2, 1.6, 0])
        with self.say("In nineteen sixty five Sacks arrived in New York, in a horrid, pokey little apartment with nowhere to write. He wrote part of his first book balanced on top of the refrigerator. He longed for space, and found it in the library of the Albert Einstein College of Medicine, where he worked: a large table to write at, and stacks to wander with no idea what his eye might fall on. Unexpected treasures, lucky finds. That is serendipity: the joy of finding something valuable by accident."):
            self.play(FadeIn(h), FadeIn(fridge), FadeIn(pad), FadeIn(fl))
            self.play(FadeIn(table), FadeIn(tl))
        self.play(FadeOut(VGroup(fridge, pad, fl, table, tl)))
        a = Dot([-1.2, 0.2, 0], radius=0.18, color=th.SKY)
        b = Dot([1.2, 0.2, 0], radius=0.18, color=th.AMBER)
        bk = Rectangle(width=0.5, height=0.7, stroke_width=0, fill_color=th.PINK, fill_opacity=0.9).move_to([0, 1.2, 0])
        bl = T("Brain, 1890", size=22, color=th.PINK).next_to(bk, UP, buff=0.15)
        nt = E.bullets(["two strangers hunting the same old volume: a whispered conversation, then a friendship", "\"a sense of community, even intimacy\"", "built on the physical book: handled, shared, the names of earlier borrowers inside"], width=11.0, size=24).move_to([0, -1.9, 0])
        with self.say("And there were people. The library was quiet, yet whispered conversations might start in the stacks, two readers hunting the same bound volume of the journal Brain from eighteen ninety, and those conversations could become friendships. Everyone was absorbed in a private world, and yet there was a sense of community, even intimacy. Part of it came from the physical book itself: handled, passed between readers, carrying the names and dates of earlier borrowers."):
            self.play(FadeIn(a), FadeIn(b), FadeIn(bk), FadeIn(bl))
            self.play(a.animate.shift(RIGHT * 0.7), b.animate.shift(LEFT * 0.7))
            E.reveal_list(self, nt, 8.0)
        self.play(FadeOut(VGroup(h, a, b, bk, bl, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "\"But a shift was occurring by the 1990s\"")
        full = shelf(4.6, 4, seed=5).move_to([-3.4, 0.4, 0])
        empty = shelf(4.6, 4, seed=5, density=0.12).move_to([3.4, 0.4, 0])
        screen = VGroup(RoundedRectangle(corner_radius=0.08, width=1.6, height=1.1, stroke_color=th.SKY, stroke_width=3, fill_color=th.SKY, fill_opacity=0.15)).move_to([0, 0.4, 0])
        ar = VGroup(Arrow(full.get_right(), screen.get_left(), buff=0.15, color=th.MUTED), Arrow(screen.get_right(), empty.get_left(), buff=0.15, color=th.MUTED))
        nt = para("Students ignore the shelves and use computers, so the books are thrown out \"with remarkably little objection\". He is horrified: \"a murder, a crime … the destruction of centuries of knowledge\".", width=11.4, size=24, color=th.CORAL).move_to([0, -2.2, 0])
        with self.say("Then the turn. But a shift was occurring by the nineteen nineties. Students ignored the shelves and found what they needed on computers, so the college decided to get rid of the books. Visiting a couple of months ago, he was horrified: the once overflowing shelves were nearly empty, the books thrown out with remarkably little objection. It felt like a murder, a crime, the destruction of centuries of knowledge."):
            self.play(FadeIn(h), FadeIn(full))
            self.play(GrowArrow(ar[0]), FadeIn(screen), GrowArrow(ar[1]), FadeIn(empty))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(full, empty, screen, ar, nt)))
        a = E.card("the librarian", "\"everything of worth\" has been digitised", th.SKY, w=5.6, h=3.0, size=26).move_to([-3.2, 0.9, 0])
        b = E.card("Sacks", "he doesn't use a computer — and \"there is something irreplaceable about a physical book: its look, its smell, its heft\"", th.AMBER, w=5.8, h=3.0, size=24).move_to([3.2, 0.9, 0])
        last = para("In 1967, rummaging in the stacks, he found an 1873 book, Liveing's Megrim — and it inspired his own first book. Digitise the shelf and you keep the text; you lose the accident.", width=11.2, size=24, color=th.MINT).move_to([0, -1.7, 0])
        with self.say("A librarian reassures him that everything of worth has been digitised. He is not reassured. He does not use a computer, and there is something irreplaceable about a physical book: its look, its smell, its heft. Then the last memory closes the circle: in nineteen sixty seven, rummaging in the stacks, he found an eighteen seventy three book on migraine, which inspired his own first book. Digitise the shelf, and you may keep the text. But you lose the lucky accident."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(last))
        self.play(FadeOut(VGroup(h, a, b, last)))
        rows = [["", "traditional library", "digital library"], ["finding", "browsing, serendipity", "search: you find what you ask for"], ["the book", "look, smell, heft", "text on a screen"], ["people", "strangers in the stacks", "each alone at a screen"], ["Sacks", "mourns its loss", "sorrow, not anger"]]
        tb = E.table(rows, [2.2, 4.8, 5.4], row_h=0.66, size=24, colors=[th.AMBER, th.MINT, th.SKY]).move_to([0, 0.2, 0])
        with self.say("For the long question, traditional against digital: browsing and lucky finds against searching for what you already know you want; the physical book against text on a screen; a community of strangers against each reader alone. Notice Sacks's tone: not anger at technology, but sorrow for what is lost.") as v:
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        self.quiz("Why does Sacks call Willesden his \"Ur-library\"?",
                  ["it was the biggest", "it was his first, original library", "it was in Germany", "it was the oldest in London"], 1,
                  "Pause and think.",
                  "Ur- means original: the first library, where he got his \"real education\".")
        self.quiz("What does Sacks say he was at school?",
                  ["a good pupil", "a good listener", "not a good pupil, but a good learner", "a lazy reader"], 2,
                  "One more.",
                  "He could not learn passively in class, but learned actively among the shelves.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Oliver Sacks (1933–2015): neurologist, \"poet laureate of medicine\"; a personal essay.",
            "Home library; Willesden, the \"Ur-library\": \"not a good pupil, but a good learner\".",
            "Science Museum, the Bodleian, the Queen's College vaults: history and language.",
            "New York: space, \"lucky finds\", whispered friendships in the stacks.",
            "The 1990s: shelves emptied; \"its look, its smell, its heft\"; serendipity lost.",
        ], "Quick recap. Sacks, and a personal essay. The library at home and the Ur library at Willesden. The vaults under Oxford. Space and strangers in New York. And the shock of the empty shelves.")
        self.outro("That was On Libraries. Next essay: Marriage as a Social Institution. See you there.")
