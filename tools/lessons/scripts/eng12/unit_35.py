import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def parts_word(parts, root, size=30, gap=0.08):
    """A word as chips, the root filled amber and the affixes outlined."""
    g = VGroup()
    for p_ in parts:
        on = p_ == root
        t = T(p_, size=size, color=th.BG if on else th.INK, weight="BOLD" if on else "NORMAL")
        b = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=0.62, stroke_color=th.AMBER if on else th.FAINT, stroke_width=2, fill_color=th.AMBER if on else th.PANEL, fill_opacity=1)
        g.add(VGroup(b, t.move_to(b)))
    return g.arrange(RIGHT, buff=gap)


def stressed(sylls, k, size=30, color=th.AMBER):
    """Syllables side by side; the stressed one is capitalised, larger and coloured."""
    return VGroup(*[T(s_.upper() if i == k else s_, size=size + 8 if i == k else size, color=color if i == k else th.INK, weight="BOLD" if i == k else "NORMAL") for i, s_ in enumerate(sylls)]).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 35
    TITLE = "Vocabulary, Sounds, Spelling and Idioms"
    SUBTITLE = "Question 8 · five one-mark items you can learn in advance"
    SECTIONS = ["What Question 8 asks", "How words are built", "Collocations and phrasal verbs", "Confusables and spelling", "Sounds and stress", "Idioms and proverbs"]
    NEXT = "Class 12 English, complete"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        one = T("beautiful", size=56, color=th.INK, weight="BOLD").move_to([0, 0.6, 0])
        fam = [("beaut", "y", "noun", th.SKY), ("beaut", "ify", "verb", th.MINT), ("beaut", "iful", "adjective", th.AMBER), ("beaut", "ifully", "adverb", th.PINK), ("beaut", "ician", "person", th.CORAL)]
        words = VGroup()
        for a_, b_, lab, c_ in fam:
            w = VGroup(T(a_, size=40, color=th.INK, weight="BOLD"), T(b_, size=40, color=c_, weight="BOLD")).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
            words.add(VGroup(w, T(lab, size=24, color=c_).next_to(w, DOWN, buff=0.12)))
        words.arrange(RIGHT, buff=0.4).move_to([0, 0.6, 0])
        words.scale_to_fit_width(min(words.width, 12.8))
        rule = T("y → i before a suffix: beauty → beautiful", size=26, color=th.MUTED).move_to([0, -1.0, 0])
        nt = para("Question 8: five marks, the cheapest on the paper. Every item can be learnt in advance.", width=11.4, size=28, color=th.AMBER).move_to([0, -2.4, 0])
        with self.say("Beautiful, memorised alone, is one word. Beauty, beautify, beautiful, beautifully and beautician, learnt together, are five words, four suffixes and a spelling rule, and they cost no more effort.") as v:
            self.play(FadeIn(one, scale=1.1))
            v.until("Beauty, beautify")
            self.play(ReplacementTransform(one, words[2]), LaggedStart(*[FadeIn(w_, shift=UP * 0.2) for j, w_ in enumerate(words) if j != 2], lag_ratio=0.25))
            v.until("and a spelling rule")
            self.play(FadeIn(rule))
        with self.say("Question eight carries only five marks, and they are the cheapest on the paper: every item in it can be learnt in advance, and none of it can be reasoned out on the day.") as v:
            self.play(FadeIn(nt))
            nb = E.neby_in(self, "read", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(words, rule, nt)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 35, the last unit: vocabulary, sounds, spelling and idioms."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. What question eight asks. How words are built. Collocations and phrasal verbs. Confusables and spelling. Sounds and stress. And idioms and proverbs.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Five one-mark items, drawn from this pool")
        pool = [("word formation", "decide → decision", th.SKY), ("prefix or suffix", "legal → illegal", th.SKY), ("phrasal verb", "tolerate → put up with", th.MINT), ("collocation", "make a decision", th.MINT), ("confusable", "affect / effect", th.AMBER),
                ("spelling", "recieve → receive", th.AMBER), ("stress", "inCREASE (verb)", th.PINK), ("sound", "bird, word, board?", th.PINK), ("idiom", "burn the midnight oil", th.CORAL)]
        cards = VGroup(*[E.card(a_, b_, c_, w=4.0, h=1.5, tsize=24, size=24) for a_, b_, c_ in pool]).arrange_in_grid(rows=3, cols=3, buff=(0.25, 0.25)).move_to([0, -0.15, 0])
        with self.say("Question eight is five one mark items, drawn from a pool of nine kinds: word formation, a prefix or suffix, a phrasal verb, a collocation, a confusable pair, a spelling, a stressed syllable, a sound, and an idiom or proverb. A candidate who has spent twenty evenings on this unit answers the whole question in four minutes, and walks into the reading passage with time in hand.") as v:
            self.play(FadeIn(h))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cards], lag_ratio=0.25), run_time=v.dur * 0.5)
        self.play(FadeOut(cards))
        h2 = E.head(self, "A word-formation item: part of speech first")
        s1 = VGroup(T("The committee's", size=30, color=th.INK), T("(decide)", size=30, color=th.SKY, weight="BOLD"), T("was announced on Friday,", size=30, color=th.INK)).arrange(RIGHT, buff=0.18)
        s2 = VGroup(T("and nobody was", size=30, color=th.INK), T("(satisfy)", size=30, color=th.PINK, weight="BOLD"), T("with it.", size=30, color=th.INK)).arrange(RIGHT, buff=0.18)
        sent = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.6, 0])
        a1 = VGroup(T("noun: after committee's, before a verb", size=24, color=th.SKY), T("decide + ion → decision", size=28, color=th.INK, weight="BOLD"), T("not decidation", size=22, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.2, -0.9, 0])
        a2 = VGroup(T("adjective: after was, describing people", size=24, color=th.PINK), T("satisfy → satisfied", size=28, color=th.INK, weight="BOLD"), T("a thing is satisfying; a person is satisfied", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.2, -0.9, 0])
        nt = T("Decide the part of speech before choosing the suffix: that is the whole method.", size=26, color=th.AMBER).move_to([0, -2.85, 0])
        nt.scale_to_fit_width(min(nt.width, 12.6))
        with self.say("A typical item: the committee's, decide, was announced on Friday, and nobody was, satisfy, with it. The first gap follows committee's and comes before a verb, so it must be a noun: decide takes ion, and gives decision, not decidation. The second follows was and describes people, so it is an adjective: satisfied, not satisfying, because a thing is satisfying and a person is satisfied. Decide the part of speech before choosing the suffix: that is the whole method.") as v:
            self.play(ReplacementTransform(h, h2), FadeIn(sent))
            v.until("The first gap")
            self.play(FadeIn(a1, shift=UP * 0.2))
            v.until("The second follows")
            self.play(FadeIn(a2, shift=UP * 0.2))
            v.until("Decide the part")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h2, sent, a1, a2, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "One root, six words: PORT means \"carry\"")
        rows = [(["im", "port"], "carry in: bring goods into a country"), (["ex", "port"], "carry out: send goods abroad"), (["trans", "port"], "carry across: move from place to place"),
                (["sup", "port"], "carry from under: hold up, help"), (["port", "able"], "able to be carried"), (["re", "port", "er"], "one who carries back: a news writer")]
        lines_ = VGroup()
        for k, (ps, gl) in enumerate(rows):
            w = parts_word(ps, "port", size=28).move_to([-6.0, 2.0 - 0.82 * k, 0], aligned_edge=LEFT)
            g = T(gl, size=24, color=th.BODY).move_to([-1.6, 2.0 - 0.82 * k, 0], aligned_edge=LEFT)
            lines_.add(VGroup(w, T("→", size=26, color=th.MUTED).move_to([-2.0, 2.0 - 0.82 * k, 0]), g))
        nt = T("Prefixes change the meaning; suffixes change the part of speech.", size=26, color=th.AMBER).move_to([0, -2.95, 0])
        with self.say("Almost every long English word is a root with something attached at each end. Port means carry. Import: carry in. Export: carry out. Transport: carry across. Support: carry from under. Portable: able to be carried. And a reporter is one who carries back the news. Take the word apart and the meaning falls out. Prefixes change the meaning; suffixes change the part of speech.") as v:
            self.play(FadeIn(h))
            for l_, q_ in zip(lines_, ["Import", "Export", "Transport", "Support", "Portable", "And a reporter"]):
                v.until(q_)
                self.play(FadeIn(l_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("Prefixes change")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(lines_, nt)))
        h2 = E.head(self, "Which negative prefix?")
        rules = [("im-", "before m and p", "immature, impatient", th.SKY), ("il-", "before l", "illegal, illiterate", th.MINT), ("ir-", "before r", "irregular, irresponsible", th.AMBER), ("in-", "before most others", "inactive, invisible", th.PINK), ("un-", "with plain English words", "unhappy, unknown", th.CORAL)]
        rr = VGroup(*[VGroup(T(a_, size=34, color=c_, weight="BOLD"), T(b_, size=24, color=th.MUTED), T(e_, size=28, color=th.INK)) for a_, b_, e_, c_ in rules])
        for k, r_ in enumerate(rr):
            y = 1.85 - 0.85 * k
            r_[0].move_to([-5.6, y, 0], aligned_edge=LEFT)
            r_[1].move_to([-4.0, y, 0], aligned_edge=LEFT)
            r_[2].move_to([0.6, y, 0], aligned_edge=LEFT)
        nt = T("When in doubt, un- is the safest guess.", size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Which negative prefix? Im before m and p: immature, impatient. Il before l: illegal, illiterate. Ir before r: irregular, irresponsible. In before most others: inactive, invisible. And un with most plain English words: unhappy, unknown. When in doubt, un is the safest guess.") as v:
            self.play(ReplacementTransform(h, h2))
            for r_, q_ in zip(rr, ["Im before", "Il before", "Ir before", "In before", "And un"]):
                v.until(q_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.5)
            v.until("When in doubt")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(rr, nt)))
        h3 = E.head(self, "Suffixes decide the part of speech")
        rows = [["makes a", "suffixes", "examples"], ["noun", "-ment -ion -ity -ness -ance -ship", "judgement, decision, kindness"], ["person", "-er -or -ist -ian", "teacher, novelist, musician"], ["verb", "-ise -fy -en", "modernise, simplify, strengthen"], ["adjective", "-ful -less -ous -al -ive -able", "careless, famous, readable"], ["adverb", "-ly", "quickly, carefully"]]
        tb = E.table(rows, [2.4, 5.4, 4.8], row_h=0.68, size=24, colors=[th.AMBER, th.MINT, th.INK]).move_to([0, -0.1, 0])
        with self.say("Suffixes decide the part of speech. Ment, ion, ity, ness, ance and ship make nouns. Er, or, ist and ian make a person. Ise, fy and en make verbs. Ful, less, ous, al, ive and able make adjectives. And ly makes an adverb.") as v:
            self.play(ReplacementTransform(h2, h3))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(VGroup(h3, tb)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Collocations: words that travel together")
        rows = [["verb", "goes with"], ["make", "a decision, a mistake, progress, an effort, friends"], ["do", "homework, a favour, business, research, your best"], ["take", "an examination, a photograph, a risk, part, care"], ["have", "breakfast, a look, an argument, fun"], ["give", "a speech, permission, advice, an example"], ["pay", "attention, a visit, a compliment, respect"]]
        tb = E.table(rows, [2.2, 10.2], row_h=0.62, size=24, colors=[th.AMBER, th.INK]).move_to([0, 0.15, 0])
        with self.say("A collocation is a pair of words that travel together, and the verb is not free. You make a decision, a mistake, progress, friends. You do homework, a favour, research, your best. You take an examination, a photograph, a risk. You have breakfast and an argument; you give a speech and advice; you pay attention and a visit.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h2 = E.head(self, "Six collocations that get reversed")
        pairs = [("do a mistake", "make a mistake"), ("give an exam", "take an exam"), ("do a decision", "make a decision"), ("say a lie", "tell a lie"), ("open the light", "turn on the light"), ("strong rain", "heavy rain")]
        grid = VGroup(*[E.wrong_right(w_, r_, size=28) for w_, r_ in pairs]).arrange_in_grid(rows=3, cols=2, buff=(1.4, 0.45), col_alignments="ll").move_to([0, -0.15, 0])
        with self.say("Six that Nepali candidates often reverse. Not do a mistake, but make a mistake. Not give an exam, but take an exam. Not do a decision, but make one. Not say a lie, but tell a lie. Not open the light, but turn on the light. And not strong rain, but heavy rain.") as v:
            self.play(ReplacementTransform(h, h2))
            for g_, q_ in zip(grid, ["Not do a mistake", "Not give", "Not do a decision", "Not say", "Not open", "And not strong"]):
                v.until(q_)
                self.play(FadeIn(g_.wrong), run_time=0.3)
                self.play(Create(g_.cross), FadeIn(g_.right), run_time=0.5)
        self.play(FadeOut(grid))
        h3 = E.head(self, "Phrasal verbs: learn them with a meaning")
        pv = [("put up with", "tolerate"), ("put off", "postpone"), ("call off", "cancel"), ("look into", "investigate"), ("bring up", "raise"), ("turn down", "reject"), ("carry out", "perform"), ("run out of", "have none left")]
        cells = VGroup(*[VGroup(T(a_, size=28, color=th.MINT, weight="BOLD"), T("= " + b_, size=26, color=th.INK)).arrange(RIGHT, buff=0.25) for a_, b_ in pv]).arrange_in_grid(rows=4, cols=2, buff=(1.2, 0.36), col_alignments="ll").move_to([0, 0.75, 0])
        sep = VGroup(T("turn the offer down  ·  turn down the offer  ·  turn it down", size=26, color=th.MINT), T("✗ turn down it    ✗ put up the noise with", size=26, color=th.CORAL)).arrange(DOWN, buff=0.2).move_to([0, -2.35, 0])
        with self.say("Phrasal verbs are learnt with their meaning. Put up with: tolerate. Put off: postpone. Call off: cancel. Look into: investigate. Bring up: raise. Turn down: reject. Carry out: perform. Run out of: have none left. Most can be split: turn the offer down, or turn down the offer. With a pronoun the split is compulsory: turn it down, never turn down it. And verbs with two particles, like put up with, are never split.") as v:
            self.play(ReplacementTransform(h2, h3))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cells], lag_ratio=0.3), run_time=v.dur * 0.45)
            v.until("Most can be split")
            self.play(FadeIn(sep[0]))
            v.until("never turn down it")
            self.play(FadeIn(sep[1]))
        self.play(FadeOut(VGroup(h3, cells, sep)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Words that are easy to confuse")
        conf = [("affect / effect", "the rain affected the crop; the effect was severe"), ("advice / advise", "noun with c, verb with s"), ("practice / practise", "daily practice (noun); to practise (verb)"), ("principal / principle", "a person, or the chief thing / a rule"),
                ("stationary / stationery", "not moving / paper and pens"), ("lose / loose", "lose a match / a loose knot"), ("its / it's", "belonging to it / it is"), ("accept / except", "receive / leave out")]
        rows = VGroup(*[VGroup(T(a_, size=26, color=th.AMBER, weight="BOLD"), T(b_, size=24, color=th.INK)) for a_, b_ in conf])
        for k, r_ in enumerate(rows):
            y = 2.15 - 0.66 * k
            r_[0].move_to([-6.2, y, 0], aligned_edge=LEFT)
            r_[1].move_to([-1.6, y, 0], aligned_edge=LEFT)
        with self.say("Confusable pairs are learnt by their difference. Affect is the verb and effect the noun: the rain affected the crop, and the effect was severe. Advice is the noun with a c, advise the verb with an s, and practice and practise follow the same rule. The principal is a person or the chief thing; a principle is a rule. Stationary means not moving; stationery is paper and pens. Lose a match; a loose knot. Its, belonging to it; it's, it is. Accept, receive; except, leave out.") as v:
            self.play(FadeIn(h))
            for r_, q_ in zip(rows, ["Affect is", "Advice is", "and practice", "The principal", "Stationary", "Lose a", "Its, belonging", "Accept"]):
                v.until(q_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.4)
        self.play(FadeOut(rows))
        h2 = E.head(self, "Spelling rules that actually pay")
        rules = [("i before e, except after c", "believe, field · receive, ceiling · but: seize, weird", th.SKY), ("double for a stressed last syllable", "stop → stopping · beGIN → beginning · but ENter → entering", th.MINT),
                 ("drop a silent e before a vowel", "hope → hoping, but hopeful · notice → noticeable keeps it", th.AMBER), ("y → i after a consonant", "happy → happiness · carry → carried · but play → played", th.PINK)]
        rc = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.0, tsize=26, size=24) for a_, b_, c_ in rules]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to([0, 0.35, 0])
        sm = T("-ful has one l: careful, useful  ·  all-, well-, till- drop one: always, welcome, until", size=24, color=th.MUTED).move_to([0, -2.6, 0])
        sm.scale_to_fit_width(min(sm.width, 12.6))
        with self.say("Four spelling rules that actually pay. I before e, except after c, when the sound is ee: believe and field, but receive and ceiling, with exceptions like seize and weird. Double the final consonant when the last syllable is stressed: stop, stopping; begin, beginning; but enter, entering. Drop a silent e before a vowel suffix: hope, hoping, but hopeful; and notice keeps its e in noticeable, to protect the soft c. And y becomes i after a consonant: happy, happiness; but play, played. Two small ones: the suffix ful has one l, and all, well and till drop a letter in always, welcome and until.") as v:
            self.play(ReplacementTransform(h, h2))
            for c_, q_ in zip(rc, ["I before e", "Double the", "Drop a silent", "And y becomes"]):
                v.until(q_)
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
            v.until("Two small ones")
            self.play(FadeIn(sm))
        self.play(FadeOut(VGroup(rc, sm)))
        h3 = E.head(self, "The most misspelt words: watch the doubles")
        ws = ["accommodation", "necessary", "occurred", "separate", "definitely", "received", "beginning", "committee", "embarrass", "immediately", "recommend", "questionnaire"]
        dbl = {"accommodation": [(1, 3), (4, 6)], "necessary": [(4, 6)], "occurred": [(1, 3), (4, 6)], "beginning": [(4, 6)], "committee": [(2, 4), (5, 7), (7, 9)], "embarrass": [(4, 6), (7, 9)], "immediately": [(1, 3)], "recommend": [(4, 6)], "questionnaire": [(7, 9)]}
        trap = {"separate": [(3, 4)], "definitely": [(5, 6)], "received": [(3, 5)]}
        cells = VGroup()
        for w_ in ws:
            t = T(w_, size=30, color=th.INK)
            for a_, b_ in dbl.get(w_, []):
                t[a_:b_].set_color(th.AMBER)
            for a_, b_ in trap.get(w_, []):
                t[a_:b_].set_color(th.MINT)
            cells.add(t)
        cells.arrange_in_grid(rows=4, cols=3, buff=(0.9, 0.42), col_alignments="lll").move_to([0, 0.2, 0])
        key = VGroup(T("doubled letters", size=24, color=th.AMBER), T("the letter people get wrong", size=24, color=th.MINT)).arrange(RIGHT, buff=0.8).move_to([0, -2.6, 0])
        with self.say("And the words most often misspelt in board answer books. Accommodation, with two c's and two m's. Necessary, one c and two s's. Occurred, committee, embarrass, recommend, questionnaire: count the doubles. And three that hide a single letter: sep a rate, defin i tely, rec e i ved.") as v:
            self.play(ReplacementTransform(h2, h3))
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.2), run_time=v.dur * 0.6)
            self.play(FadeIn(key))
        self.play(FadeOut(VGroup(h3, cells, key)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Sounds Nepali speakers often swap")
        rows = [["symbol", "as in", "often heard instead"], ["/θ/", "think, bath", "an aspirated t: \"tink\""], ["/ð/", "this, mother", "a hard d: \"dis\""], ["/v/", "very, have", "a w: \"wery\""], ["/z/", "zoo, rose", "a j: \"joo\""],
                ["/æ/", "bad, cat", "an e: bad sounds like bed"], ["/ɜː/", "bird, word", "a full r: \"burd\""], ["/ə/", "about, teacher", "a full vowel: the schwa vanishes"]]
        tb = E.table(rows, [2.0, 3.8, 6.6], row_h=0.6, size=24, colors=[th.AMBER, th.INK, th.MUTED]).move_to([0, 0.2, 0])
        with self.say("English spelling is unreliable, so dictionaries describe sounds with phonetic symbols. You are not asked to transcribe, only to recognise the common symbols and hear the contrasts Nepali does not make. Theta, in think, often becomes an aspirated t: tink. Eth, in this, becomes a hard d: dis. V becomes w: wery. Z becomes j: joo. The vowel of bad drifts to bed. Bird gets a full r: burd. And the schwa, the weak vowel in about and teacher, disappears into a full vowel.") as v:
            self.play(FadeIn(h), FadeIn(tb[0]))
            for r_, q_ in zip(tb[1:], ["Theta", "Eth", "V becomes", "Z becomes", "The vowel of bad", "Bird gets", "And the schwa"]):
                v.until(q_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.4)
        self.play(FadeOut(tb))
        h2 = E.head(self, "One spelling, three sounds: -ed")
        eds = VGroup(*[VGroup(T(w_, size=40, color=th.INK, weight="BOLD"), E.chip(s_, c_, size=30)).arrange(DOWN, buff=0.3) for w_, s_, c_ in [("walked", "/t/", th.SKY), ("played", "/d/", th.MINT), ("wanted", "/ɪd/", th.AMBER)]]).arrange(RIGHT, buff=1.4).move_to([0, 0.7, 0])
        rule = para("/ɪd/ only after t or d; /t/ after voiceless sounds like k, p, s; /d/ after the rest.", width=11.4, size=26, color=th.MUTED).move_to([0, -1.6, 0])
        with self.say("English endings matter too. The ed of walked is a t sound; of played, a d; and of wanted, a whole extra syllable, id. It is id only after t or d; t after voiceless sounds like k, p and s; and d after the rest.") as v:
            self.play(ReplacementTransform(h, h2))
            for e_, q_ in zip(eds, ["walked", "of played", "and of wanted"]):
                v.until(q_)
                self.play(FadeIn(e_, shift=UP * 0.2), run_time=0.5)
            v.until("It is id")
            self.play(FadeIn(rule))
        self.play(FadeOut(VGroup(eds, rule)))
        h3 = E.head(self, "Stress: the noun–verb shift")
        pairs = [("record", ["re", "cord"]), ("present", ["pre", "sent"]), ("export", ["ex", "port"]), ("conduct", ["con", "duct"])]
        colh = VGroup(T("noun", size=26, color=th.SKY, weight="BOLD"), T("verb", size=26, color=th.MINT, weight="BOLD"))
        colh[0].move_to([-2.2, 2.05, 0])
        colh[1].move_to([2.2, 2.05, 0])
        prs = VGroup()
        for k, (w_, sy) in enumerate(pairs):
            y = 1.25 - 0.8 * k
            prs.add(VGroup(stressed(sy, 0, color=th.SKY).move_to([-2.2, y, 0]), stressed(sy, 1, color=th.MINT).move_to([2.2, y, 0])))
        ex = VGroup(T("They gave him a PREsent.", size=28, color=th.SKY), T("The head will preSENT the prizes.", size=28, color=th.MINT)).arrange(RIGHT, buff=1.0).move_to([0, -2.3, 0])
        ex.scale_to_fit_width(min(ex.width, 12.6))
        with self.say("Every word of more than one syllable has one syllable said louder, longer and higher. Some words shift it by job. As nouns, record, present, export and conduct stress the first syllable. As verbs, the stress moves to the second. They gave him a present: a noun, so present. The head will present the prizes: after will, a verb, so present. The test is never the spelling; it is the job the word does in the sentence.") as v:
            self.play(ReplacementTransform(h2, h3), FadeIn(colh))
            v.until("As nouns")
            self.play(LaggedStart(*[FadeIn(p_[0]) for p_ in prs], lag_ratio=0.3))
            v.until("As verbs")
            self.play(LaggedStart(*[FadeIn(p_[1]) for p_ in prs], lag_ratio=0.3))
            v.until("They gave him")
            self.play(FadeIn(ex[0]))
            v.until("The head will")
            self.play(FadeIn(ex[1]))
        self.play(FadeOut(VGroup(colh, prs, ex)))
        h4 = E.head(self, "Suffixes that pull the stress")
        pull = VGroup(*[VGroup(stressed(sy, k_, size=30, color=th.AMBER), T(s_, size=22, color=th.MUTED)).arrange(DOWN, buff=0.15) for sy, k_, s_ in [(["e", "du", "ca", "tion"], 2, "-ion"), (["a", "bi", "li", "ty"], 1, "-ity"), (["pho", "to", "gra", "phy"], 1, "-graphy"), (["bi", "o", "lo", "gy"], 1, "-logy")]]).arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        stay = VGroup(*[VGroup(stressed(sy, 0, size=30, color=th.MINT), T(s_, size=22, color=th.MUTED)).arrange(DOWN, buff=0.15) for sy, s_ in [(["hap", "pi", "ness"], "-ness"), (["gov", "ern", "ment"], "-ment")]]).arrange(RIGHT, buff=1.2).move_to([0, -1.6, 0])
        tags = VGroup(T("pull it to the syllable before:", size=24, color=th.AMBER).next_to(pull, UP, buff=0.3), T("leave it where it was:", size=24, color=th.MINT).next_to(stay, UP, buff=0.3))
        with self.say("Some suffixes pull the stress onto the syllable just before them: education, ability, photography, biology. Others leave it where it was: happiness, government.") as v:
            self.play(ReplacementTransform(h3, h4), FadeIn(tags[0]), LaggedStart(*[FadeIn(p_) for p_ in pull], lag_ratio=0.3))
            v.until("Others leave")
            self.play(FadeIn(tags[1]), LaggedStart(*[FadeIn(p_) for p_ in stay], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h4, pull, stay, tags)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "An idiom item: meaning in a clause, then a sentence")
        q = T("Explain \"a blessing in disguise\" and use it in a sentence.", size=28, color=th.SKY).move_to([0, 2.2, 0])
        m = E.card("the meaning", "something that seems unfortunate at first but turns out to be lucky", th.MINT, w=11.6, h=1.6, tsize=24, size=26).move_to([0, 0.75, 0])
        s = E.card("the sentence", "Missing the early bus was a blessing in disguise, because it skidded off the road above Mugling.", th.AMBER, w=11.6, h=1.6, tsize=24, size=26).move_to([0, -1.05, 0])
        nt = T("A clause, not a one-word synonym; and the idiom in its fixed form.", size=24, color=th.MUTED).move_to([0, -2.55, 0])
        with self.say("An idiom item asks for the meaning and a sentence. A blessing in disguise: something that seems unfortunate at first but turns out to be lucky. Then a sentence that makes the meaning visible: missing the early bus was a blessing in disguise, because it skidded off the road above Mugling. Give the meaning as a clause, not a one word synonym, and keep the idiom in its fixed form.") as v:
            self.play(FadeIn(h), FadeIn(q))
            v.until("A blessing in disguise:")
            self.play(FadeIn(m, shift=UP * 0.2))
            v.until("Then a sentence")
            self.play(FadeIn(s, shift=UP * 0.2))
            v.until("Give the meaning")
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(q, m, s, nt)))
        h2 = E.head(self, "Idioms worth knowing")
        ids = [("burn the midnight oil", "study late into the night"), ("break the ice", "start talk in an awkward moment"), ("cut corners", "do a job cheaply and badly"), ("the ball is in your court", "it is now your turn to act"),
               ("sit on the fence", "refuse to take a side"), ("beat about the bush", "avoid coming to the point"), ("at the eleventh hour", "at the very last moment"), ("a drop in the ocean", "far too little to matter")]
        cells = VGroup(*[VGroup(T(a_, size=26, color=th.AMBER, weight="BOLD"), T(b_, size=24, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.08) for a_, b_ in ids]).arrange_in_grid(rows=4, cols=2, buff=(0.9, 0.38), col_alignments="ll").move_to([0, -0.15, 0])
        with self.say("Idioms worth knowing. Burn the midnight oil: study late into the night. Break the ice: start a conversation in an awkward moment. Cut corners: do a job cheaply and badly. The ball is in your court: it is now your turn to act. Sit on the fence: refuse to take a side. Beat about the bush: avoid coming to the point. At the eleventh hour: at the very last moment. And a drop in the ocean: far too little to matter.") as v:
            self.play(ReplacementTransform(h, h2))
            for c_, q_ in zip(cells, ["Burn the", "Break the", "Cut corners", "The ball", "Sit on", "Beat about", "At the eleventh", "And a drop"]):
                v.until(q_)
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.4)
        self.play(FadeOut(cells))
        h3 = E.head(self, "Proverbs: say what each teaches")
        pv = [("A stitch in time saves nine.", "repair a small fault now and avoid a large one later"), ("Too many cooks spoil the broth.", "too many people managing one job ruin it"), ("Empty vessels make the most noise.", "those who know least talk loudest"), ("Rome was not built in a day.", "anything worth building takes time")]
        pc = VGroup(*[E.card(a_, b_, c_, w=6.1, h=2.0, tsize=26, size=24) for (a_, b_), c_ in zip(pv, [th.SKY, th.MINT, th.AMBER, th.PINK])]).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to([0, -0.2, 0])
        with self.say("And a proverb is explained by what it teaches. A stitch in time saves nine: repair a small fault now and you avoid a large one later. Too many cooks spoil the broth: too many people managing one job ruin it. Empty vessels make the most noise: those who know least talk loudest. Rome was not built in a day: anything worth building takes time.") as v:
            self.play(ReplacementTransform(h2, h3))
            for c_, q_ in zip(pc, ["A stitch", "Too many", "Empty vessels", "Rome was"]):
                v.until(q_)
                self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
        self.play(FadeOut(VGroup(h3, pc)))
        self.quiz("Which negative prefix goes with \"legal\"?",
                  ["un-", "in-", "il-", "dis-"], 2,
                  "Pause and think.",
                  "il- before l: illegal, as in illiterate.")
        self.quiz("\"The head will present the prizes.\" Where is the stress?",
                  ["PREsent", "preSENT", "on both", "on neither"], 1,
                  "One more.",
                  "After will it is a verb, so the stress moves to the second syllable: preSENT.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Five learnable marks: learn words in families, not in lists.",
            "Part of speech first, then the suffix: decision, satisfied.",
            "Make a mistake, take an exam, tell a lie; turn it down.",
            "i before e except after c; double for a stressed last syllable.",
            "PREsent the noun, preSENT the verb; idioms in their fixed form.",
        ], "Quick recap. Learn words in families. Fix the part of speech before the suffix. Collocations and phrasal verbs, learnt with their meaning. The spelling rules that pay. And stress that shifts with the job a word does.")
        self.outro("That completes Class 12 English, thirty five units. Well done for coming all this way.")
