import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402

PAPER = "#F3EEE2"
INKP = "#2B2B33"


def page(w=4.6, h=6.0):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color="#C9C1AE", stroke_width=2, fill_color=PAPER, fill_opacity=1)


def lines(n, w, color="#9C9483", gap=0.16, width=2):
    return VGroup(*[Line(ORIGIN, RIGHT * (w if k < n - 1 else w * 0.6), color=color, stroke_width=width) for k in range(n)]).arrange(DOWN, aligned_edge=LEFT, buff=gap)


def letter_zones(pg):
    """A letter page, top to bottom: sender and date, receiver, salutation, subject, three paragraphs, close."""
    l, r, t = pg.get_left()[0] + 0.3, pg.get_right()[0] - 0.3, pg.get_top()[1]
    z = {}
    z["sender"] = lines(3, 1.3).move_to([r, t - 0.5, 0], aligned_edge=RIGHT)
    z["date"] = Line(ORIGIN, RIGHT * 0.9, color=th.AMBER, stroke_width=3).next_to(z["sender"], DOWN, buff=0.15).align_to(z["sender"], RIGHT)
    z["to"] = lines(4, 1.4).move_to([l, t - 1.75, 0], aligned_edge=LEFT)
    z["salute"] = Line(ORIGIN, RIGHT * 1.1, color=th.SKY, stroke_width=4).move_to([l, t - 2.45, 0], aligned_edge=LEFT)
    z["subject"] = Line(ORIGIN, RIGHT * 2.6, color=th.PINK, stroke_width=5).move_to([l, t - 2.85, 0], aligned_edge=LEFT)
    z["body"] = VGroup(*[lines(3, r - l, color="#7E776A") for _ in range(3)]).arrange(DOWN, buff=0.22).move_to([l, t - 3.25, 0], aligned_edge=UL)
    z["close"] = lines(2, 1.1, color=th.MINT, width=3).move_to([l, t - 5.35, 0], aligned_edge=LEFT)
    return z


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 32
    TITLE = "Functional Writing"
    SUBTITLE = "Writing · Question 5: letters, emails, applications and CVs"
    SECTIONS = ["Format first", "Register", "The letter to the editor", "The formal email", "The application and the CV", "The complaint, and the checklist"]
    NEXT = "Unit 33 · Free Writing"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        pg = page().move_to([-3.4, -0.3, 0])
        z = letter_zones(pg)
        q = para("Where does the date go? How do you greet a stranger? How does a letter end when you don't know the reader's name?", width=6.0, size=28, color=th.INK).move_to([3.0, 0.6, 0])
        nt = para("These conventions are fixed, can be learnt in an evening — and carry half the marks.", width=6.0, size=28, color=th.AMBER).move_to([3.0, -1.6, 0])
        with self.say("Question five is worth eight marks, and it is the most predictable question on the paper. The examiner is not asking for something interesting to say. He is asking whether you know the shape of a document real people send to real offices. Where does the date go? How do you greet a stranger? How does a letter end when you do not know the reader's name?"):
            self.play(FadeIn(pg))
            self.play(LaggedStart(*[FadeIn(v_) for v_ in z.values()], lag_ratio=0.25), run_time=3)
            self.play(FadeIn(q))
        with self.say("Those conventions are fixed. They can be learnt in an evening, and they carry half the marks."):
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(pg, *z.values(), q, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 32: functional writing: letters to the editor, emails, C Vs and applications."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Format first. Register. The letter to the editor. The formal email. The application and the C V. And the letter of complaint, with a final checklist.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Decide the form before you write a word")
        forms = VGroup(*[E.card(a_, b_, c_, w=3.1, h=2.0, tsize=22, size=22) for a_, b_, c_ in [("letter to the editor", "a public issue, for thousands of readers", th.SKY), ("email", "a letter with the envelope printed on top", th.MINT), ("application + CV", "a covering letter and a one-page record", th.AMBER), ("complaint / request", "facts, proof, and one clear remedy", th.PINK)]]).arrange(RIGHT, buff=0.17).move_to([0, 1.3, 0])
        rows = [["credited", "marks", "means"], ["format", "2", "addresses, date, salutation, subject, close, signature"], ["content", "3", "every point asked, and what the reader needs to act"], ["organisation", "1", "one idea to a paragraph"], ["language", "2", "formal register, held throughout"]]
        tb = E.table(rows, [2.8, 1.4, 8.0], row_h=0.52, size=22, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, -1.3, 0])
        ln = T("150–200 words of body · about 18 minutes, two of them laying out the page", size=24, color=th.SKY).move_to([0, -3.05, 0])
        with self.say("Format first, then content. A brilliant argument in the wrong layout loses the format marks and cannot get them back. So decide which of four forms is asked for: a letter to the editor, an email, an application with a C V, or a letter of complaint or request. The eight marks: two for format, three for content, one for organisation, two for language. Write a hundred and fifty to two hundred words of body, in about eighteen minutes, two of them spent laying out the page.") as v:
            self.play(FadeIn(h), LaggedStart(*[FadeIn(f_, shift=UP * 0.2) for f_ in forms], lag_ratio=0.3))
            v.until("The eight marks")
            E.reveal_table(self, tb, v.dur * 0.25)
            v.until("Write a hundred")
            self.play(FadeIn(ln))
        self.play(FadeOut(VGroup(h, forms, tb, ln)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        rows = [["friendly", "formal — use this"], ["I'm writing about", "I am writing to draw your attention to"], ["Can you fix it?", "I should be grateful if the matter could be looked into"], ["get in touch", "I may be contacted on the number given above"], ["a big problem", "a matter of considerable concern to residents"], ["ASAP", "at your earliest convenience"]]
        tb = E.table(rows, [4.0, 8.4], row_h=0.66, size=24, colors=[th.CORAL, th.MINT]).move_to([0, 0.8, 0])
        nt = para("The commonest Grade 12 fault: a body that slides from formal into friendly halfway through.", width=11, size=26, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Register is the level of formality, and question five is almost always formal. Not I'm writing about, but I am writing to draw your attention to. Not can you fix it, but I should be grateful if the matter could be looked into. Not get in touch, but I may be contacted on the number given above. And not A S A P, but at your earliest convenience. The commonest fault is a letter that slides from formal into friendly halfway through.") as v:
            E.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = E.head(self, "Strike these out of your English")
        pairs = [("Myself Ramesh Thapa.", "I am Ramesh Thapa."), ("Kindly do the needful.", "say what the needful is"), ("Your's faithfully", "Yours faithfully"), ("Respected Sir,", "Dear Sir,"), ("I beg to state that …", "(a hundred years out of date)"), ("Please reply back.", "Please reply.")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=26) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(0.8, 0.45), col_alignments="ll").move_to([0, -0.2, 0])
        grid.scale_to_fit_width(min(grid.width, 12.6))
        with self.say("And strike these phrases out of your English. Myself Ramesh Thapa: say I am Ramesh Thapa, or better, open with the issue. Kindly do the needful: say what the needful is. Your's faithfully, with an apostrophe: there is no apostrophe in yours. Respected sir: dear sir. I beg to state: a hundred years out of date. And reply back: reply already means back."):
            self.play(FadeIn(h))
            for g_ in grid:
                self.play(FadeIn(g_.wrong), run_time=0.35)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
                self.hold(1.0)
        self.play(FadeOut(VGroup(h, grid)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "The letter to the editor, zone by zone")
        pg = page(w=4.4, h=5.9).move_to([-3.8, -0.35, 0])
        z = letter_zones(pg)
        tg = [VGroup(z["sender"], z["date"]), z["to"], z["salute"], z["subject"], z["body"][0], z["body"][1], z["body"][2], z["close"]]
        labs = [("your address, then the date", th.AMBER, 2.05), ("the editor's address", th.BODY, 0.9), ("Dear Sir/Madam — never a name", th.SKY, 0.3), ("Subject: one line only", th.PINK, -0.25),
                ("para 1: the issue", th.BODY, -0.85), ("para 2: the evidence", th.BODY, -1.4), ("para 3: what you want done", th.BODY, -1.95), ("Yours faithfully, then your full name", th.MINT, -2.75)]
        cues = ["Top right", "On the left", "The salutation", "A subject line", "the issue", "the evidence", "what you want done", "And the close"]
        callouts = VGroup()
        for tgt, (t_, c_, y) in zip(tg, labs):
            lab = T(t_, size=24, color=c_).move_to([-0.7, y, 0], aligned_edge=LEFT)
            box = SurroundingRectangle(tgt, color=c_, buff=0.07, stroke_width=2.5, corner_radius=0.04)
            ln = Line([pg.get_right()[0] + 0.06, tgt.get_center()[1], 0], lab.get_left() + LEFT * 0.12, color=c_, stroke_width=1.5, stroke_opacity=0.7)
            callouts.add(VGroup(box, ln, lab))
        with self.say("The letter to the editor, the form asked for most often. Remember what it is: a letter to one person, the editor, written to be read by thousands. Top right, your address, then the date, written out. On the left, the editor's address. The salutation, dear sir or madam, never a name. A subject line, one line only. Then three short paragraphs: the issue, the evidence, and what you want done. And the close, yours faithfully or yours sincerely, with your full name.") as v:
            self.play(FadeIn(h), FadeIn(pg), FadeIn(VGroup(*z.values())))
            for c_, q_ in zip(callouts, cues):
                v.until(q_)
                self.play(Create(c_[0]), Create(c_[1]), FadeIn(c_[2]), run_time=0.5)
        self.play(FadeOut(VGroup(pg, *z.values(), callouts)))
        rules = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.2, size=24) for a_, b_, c_ in [("1  one issue only", "roads AND load-shedding AND exams: the sub-editor cuts it", th.SKY), ("2  say when and where", "\"dark since Baisakh on the Milanchowk stretch\" — not \"many problems\"", th.AMBER),
                                                                                      ("3  name who can act", "the ward office, the municipality — and exactly what to do", th.MINT), ("4  sign with full name and place", "unsigned letters are not printed — or marked", th.PINK)]]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).move_to([0, -0.2, 0])
        h2 = E.head(self, "Four rules for a printed letter")
        with self.say("Four rules separate a printed letter from a rejected one. One issue only: a letter about roads, load shedding and exams at once gets cut. Say when and where: the lights on the Milanchowk stretch have been dark since Baisakh is evidence; there are many problems is not. Name who can act, and exactly what they should do. And sign with your full name and place."):
            self.play(ReplacementTransform(h, h2), LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in rules], lag_ratio=0.6), run_time=5)
        self.play(FadeOut(VGroup(h2, rules)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "An email is a letter with the envelope on top")
        win = RoundedRectangle(corner_radius=0.12, width=12.6, height=3.2, stroke_color=th.MUTED, stroke_width=2, fill_color=th.PANEL, fill_opacity=1).move_to([0, 0.9, 0])
        fields = [("To:", "principal@school.edu.np", th.SKY), ("Cc:", "club advisor", th.MUTED), ("Subject:", "Request to hold a blood donation camp on 15 Magh", th.PINK), ("Attachment:", "camp_plan.pdf", th.AMBER)]
        rows = VGroup()
        for k, (a_, b_, c_) in enumerate(fields):
            y = win.get_top()[1] - 0.42 - 0.5 * k
            rows.add(VGroup(T(a_, size=24, color=c_, weight="BOLD").move_to([win.get_left()[0] + 0.3, y, 0], aligned_edge=LEFT), T(b_, size=24, color=th.INK).move_to([win.get_left()[0] + 2.5, y, 0], aligned_edge=LEFT)))
        ysep = win.get_top()[1] - 2.35
        sep = Line([win.get_left()[0] + 0.2, ysep, 0], [win.get_right()[0] - 0.2, ysep, 0], color=th.FAINT)
        body = lines(2, 11.6, color=th.FAINT).next_to(sep, DOWN, buff=0.3).align_to(sep, LEFT).shift(RIGHT * 0.1)
        notes = VGroup(*[VGroup(T(a_, size=24, color=c_, weight="BOLD"), T(b_, size=24, color=th.BODY)).arrange(RIGHT, buff=0.2) for a_, b_, c_ in [("To", "the one person who can decide", th.SKY), ("Cc", "people who need to know, not act", th.MUTED), ("Subject", "6–10 words naming the action, never \"Hello sir\"", th.PINK), ("Attachment", "mention it in the body too", th.AMBER), ("Below the header", "as formal as a letter", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, -2.2, 0])
        with self.say("A formal email is a letter with the envelope printed on top. The header does the work of the addresses, so you don't repeat them. To: one reader, the person who can actually decide. Cc: people who need to know but need not act. The subject: six to ten words naming the action, request to hold a blood donation camp on the fifteenth of Magh, never just hello sir. Mention any attachment in the body. And below the header, stay as formal as a letter.") as v:
            self.play(FadeIn(h), FadeIn(win))
            for r_, n_, q_ in zip(rows, notes, ["To: one reader", "Cc:", "The subject", "Mention any"]):
                v.until(q_)
                self.play(FadeIn(r_), FadeIn(n_), run_time=0.5)
            v.until("And below")
            self.play(Create(sep), FadeIn(body), FadeIn(notes[4]))
        self.play(FadeOut(VGroup(h, win, rows, sep, body, notes)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "The covering letter: four paragraphs")
        steps = E.bullets(["1  the post, and where and when you saw it advertised", "2  your single most relevant qualification, with year and board", "3  what you have actually done: an internship, tuition you taught, software you can use", "4  offer yourself for interview, and name the enclosures"], width=11.2, size=26).move_to([0, 0.6, 0])
        nt = para("It does not repeat the CV: it points to the two facts in it that matter for this post.", width=11, size=26, color=th.AMBER).move_to([0, -2.3, 0])
        with self.say("An application is a covering letter, in four paragraphs. The post, and where and when you saw it advertised. Your single most relevant qualification, with the year and the board. What you have actually done: an internship, tuition you taught, software you can use. And a close offering yourself for interview and naming the enclosures. It does not repeat the C V; it points to the two facts in it that matter for this post.") as v:
            self.play(FadeIn(h))
            for st_, q_ in zip(steps, ["The post", "Your single", "What you have", "And a close"]):
                v.until(q_)
                self.play(FadeIn(st_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("It does not")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(steps, nt)))
        h2 = E.head(self, "The CV: seven headings, never paragraphs")
        cv = page(w=4.4, h=6.0).move_to([-3.8, -0.35, 0])
        heads = ["Personal details", "Career objective", "Academic qualifications", "Work experience", "Skills", "Extra-curricular activities", "References"]
        hv = VGroup()
        for k, t_ in enumerate(heads):
            y = cv.get_top()[1] - 0.45 - 0.78 * k
            hv.add(VGroup(T(t_, size=22, color=INKP, weight="BOLD").move_to([cv.get_left()[0] + 0.3, y, 0], aligned_edge=LEFT), lines(2, 3.6, gap=0.1).move_to([cv.get_left()[0] + 0.3, y - 0.32, 0], aligned_edge=LEFT)))
        notes = VGroup(*[T(t_, size=24, color=c_) for t_, c_ in [("a plain email: sabin.gurung@gmail.com", th.INK), ("one sentence, aimed at this post", th.INK), ("a small table — newest first", th.AMBER), ("post, organisation, dates, one line", th.INK), ("only what you can prove", th.INK), ("posts held, prizes, volunteering", th.INK), ("two people who have agreed", th.INK)]])
        leads = VGroup()
        for a_, b_ in zip(hv, notes):
            y = a_[0].get_center()[1]
            b_.move_to([-0.7, y, 0], aligned_edge=LEFT)
            leads.add(Line([cv.get_right()[0] + 0.06, y, 0], [-0.82, y, 0], color=th.FAINT, stroke_width=1.5))
        with self.say("The C V comes in seven headings, never paragraphs, because it is read in thirty seconds. Personal details, with a plain email address. A career objective: one sentence aimed at this post. Academic qualifications in a small table, newest first. Work experience. Skills, only what you can prove. Extra curricular activities. And two references who have agreed.") as v:
            self.play(ReplacementTransform(h, h2), FadeIn(cv))
            for a_, l_, b_, q_ in zip(hv, leads, notes, ["Personal details", "A career", "Academic", "Work experience", "Skills", "Extra curricular", "And two references"]):
                v.until(q_)
                self.play(FadeIn(a_), Create(l_), FadeIn(b_), run_time=0.5)
        self.play(FadeOut(VGroup(cv, hv, leads, notes)))
        h3 = E.head(self, "Match the close to the greeting")
        pairs = VGroup(*[E.card(a_, b_, c_, w=5.6, h=2.3, tsize=32, size=28) for a_, b_, c_ in [("Dear Sir/Madam,", "Yours faithfully,\nyou don't know the name", th.SKY), ("Dear Mr Sharma,", "Yours sincerely,\nyou know the name", th.MINT)]]).arrange(RIGHT, buff=0.5).move_to([0, 0.7, 0])
        wr = E.wrong_right("Your's faithfully", "Yours faithfully — no apostrophe", size=28).move_to([0, -2.0, 0])
        with self.say("And remember the close. Dear sir or madam takes yours faithfully. A named person, dear Mr Sharma, takes yours sincerely. And there is no apostrophe in yours.") as v:
            self.play(ReplacementTransform(h2, h3), FadeIn(pairs[0], shift=UP * 0.2))
            v.until("A named")
            self.play(FadeIn(pairs[1], shift=UP * 0.2))
            v.until("And there is")
            self.play(FadeIn(wr.wrong))
            self.play(Create(wr.cross), FadeIn(wr.right))
        self.play(FadeOut(VGroup(h3, pairs, wr)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "A complaint that gets acted on")
        facts = VGroup(*[E.chip(t_, c_, size=26) for t_, c_ in [("what you bought or used", th.SKY), ("when and where", th.SKY), ("proof: bill, order, ticket number", th.AMBER), ("what went wrong", th.CORAL), ("the remedy: repair, replacement, refund or apology", th.MINT)]]).arrange(DOWN, buff=0.2).move_to([0, 0.75, 0])
        nt = para("An angry complaint gets a polite reply and no action. One that reads like a file note gets fixed — name ONE remedy, and put the order number in the subject line.", width=11.4, size=24, color=th.AMBER).move_to([0, -2.5, 0])
        with self.say("A complaint that sounds angry gets a polite reply and no action. A complaint that reads like a file note gets acted on, because the reader can see exactly what to put right. It needs five facts: what you bought or used; when and where; the proof, a bill or order number; what went wrong; and the remedy you want: repair, replacement, refund or apology. Name one of them, and put the order number in the subject line, where a clerk will look for it."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(f_, shift=UP * 0.15) for f_ in facts], lag_ratio=0.4), run_time=4)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(facts, nt)))
        h2 = E.head(self, "Two minutes at the end: the checklist")
        chk = E.bullets(["the form the question asked for?", "your address top right, theirs left, the date written out?", "a one-line subject?", "a close that matches the salutation, with your full name below?", "every point answered, with dates and numbers?", "no myself, do the needful, respected sir, reply back?"], width=11.2, size=26).move_to([0, -0.2, 0])
        with self.say("And a two minute check at the end, because each line is a real mark. Is it the form the question asked for? Your address top right, the receiver's on the left, and the date written out? A one line subject? Does the close match the salutation, with your full name below? Is every point answered, with dates and numbers rather than adjectives? And no myself, no do the needful, no respected sir, no reply back?"):
            self.play(ReplacementTransform(h, h2))
            E.reveal_list(self, chk, 12.0)
        self.play(FadeOut(VGroup(h2, chk)))
        self.quiz("A letter begins \"Dear Sir/Madam\". How should it end?",
                  ["Yours sincerely", "Yours faithfully", "Your's faithfully", "Thanking you"], 1,
                  "Pause and think.",
                  "You don't know the name, so: Yours faithfully — with no apostrophe.")
        self.quiz("Which is the best email subject line?",
                  ["Hello sir", "Leave", para("Request for two days' leave, 5–6 Falgun", width=4.4, size=26, color=th.INK), "Urgent!!!"], 2,
                  "One more.",
                  "Six to ten words that name the action — and here, the dates.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Format first: two marks for layout that a good argument can't win back.",
            "Formal register throughout; strike myself, do the needful, respected sir.",
            "Editor: one issue, when and where, who should act, full name and place.",
            "Email: To, Cc, a 6–10 word subject; application: four paragraphs; CV: seven headings.",
            "Complaint: five facts and one remedy; Sir → faithfully, a name → sincerely.",
        ], "Quick recap. Format first. A formal register held to the end. The letter to the editor, zone by zone. The email header. The covering letter and the C V. And the complaint that gets acted on.")
        self.outro("That was functional writing. Next: free writing — essays and memoirs. See you there.")
