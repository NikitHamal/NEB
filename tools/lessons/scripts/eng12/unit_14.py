import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _en as E  # noqa: E402


def person(color, label, x, y=0.0):
    return VGroup(Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35), T(label, size=22, color=color).shift(DOWN * 0.55)).move_to([x, y, 0])


class Lesson(Lesson):
    SUBJECT = "eng"
    GRADE = 12
    UNIT = 14
    TITLE = "Marriage as a Social Institution"
    SUBTITLE = "Steven L. Nock · an essay"
    SECTIONS = ["Nock and the essay's argument", "An institution with soft boundaries", "Durkheim: limits on desire", "Marriage vs cohabitation", "Marriage as social capital", "Normative marriage: six dimensions"]
    NEXT = "Unit 15 · Knowledge and Wisdom"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        a, b = person(th.SKY, "", -0.9, 0.2), person(th.PINK, "", 0.9, 0.2)
        ring = Circle(radius=2.6, stroke_color=th.AMBER, stroke_width=3).move_to([0, 0.2, 0])
        helpers = VGroup(*[T(t_, size=24, color=th.AMBER).move_to([3.4 * np.cos(a_), 0.2 + 2.9 * np.sin(a_), 0]) for t_, a_ in [("law", PI / 2), ("religion", PI / 6), ("custom", -PI / 6), ("relatives", -PI / 2), ("expectations", 5 * PI / 6), ("society", 7 * PI / 6)]])
        with self.say("Ask a class why people marry, and you will hear about love, family and happiness. A sociologist asks a different question: what is a marriage? Two people, yes."):
            self.play(FadeIn(a), FadeIn(b))
        with self.say("But Steven Nock's answer is that a marriage is never just two people. It comes with rules, expectations and helpers already attached: law, religion, custom, relatives. They existed before the couple met, and they limit the couple, but they also protect and guide them."):
            self.play(Create(ring), LaggedStart(*[FadeIn(h_) for h_ in helpers], lag_ratio=0.25))
            nb = E.neby_in(self, "think", height=1.3)
        E.neby_out(self, nb)
        self.play(FadeOut(VGroup(a, b, ring, helpers)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 English, Unit 14: Marriage as a Social Institution, by the American sociologist Steven Nock."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Nock and the essay's argument. An institution with soft boundaries. Durkheim and the limits on desire. Marriage against cohabitation. Marriage as social capital. And normative marriage, in six dimensions.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = E.head(self, "Steven L. Nock (1950–2008)")
        facts = E.bullets(["Professor of Sociology, University of Virginia", "studied marriage, cohabitation, divorce, fatherhood", "Marriage in Men's Lives (1998): why married men behave differently", "this passage: Chapter 2 of that book", "the most academic essay in your book — but only five ideas"], width=7.6, size=24).move_to([-2.4, 0.2, 0])
        warn = E.card("read the headnote with care", "the passage is theory about what marriage is — not a \"debate\", and not \"a private matter\"", th.CORAL, w=4.4, h=3.6, tsize=26, size=24).move_to([4.4, 0.2, 0])
        with self.say("Steven Nock was a professor of sociology at the University of Virginia who studied marriage, cohabitation and divorce. His book Marriage in Men's Lives asks why married men behave differently from unmarried men. This passage is from its second chapter. It is the most academic essay in your book, but it contains only five ideas. One warning: the textbook's headnote talks of a national marriage debate and programmes; none of that is in the passage. Use the passage itself."):
            self.play(FadeIn(h))
            E.reveal_list(self, facts, 8.0)
            self.play(FadeIn(warn))
        self.play(FadeOut(VGroup(h, facts, warn)))
        h = E.head(self, "Five steps")
        steps = VGroup(*[E.card(f"{k + 1}", t_, c_, w=2.35, h=2.6, tsize=34, size=22) for k, (t_, c_) in enumerate([("an institution", th.SKY), ("limits on desire (Durkheim)", th.AMBER), ("vs cohabitation: a template", th.MINT), ("social capital", th.PINK), ("six dimensions", th.CORAL)])]).arrange(RIGHT, buff=0.18).move_to([0, 0.2, 0])
        with self.say("Here is the argument in five steps. One: marriage is an institution. Two: it benefits men by setting limits on desire. Three: unlike cohabitation, it supplies a template. Four: it is a form of social capital. Five: normative marriage has six dimensions. Learn these five and you can answer any question on the essay."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in steps], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, steps)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = E.head(self, "\"Much more than the sum of two spouses\"")
        df = E.card("Institution (sociology)", "an established, lasting pattern of rules and roles that meets a basic need and passes between generations: family, education, religion, the economy, the state", th.SKY, w=6.0, h=3.0, size=24).move_to([-3.2, 0.6, 0])
        pts = E.bullets(["defined by legal, moral and conventional assumptions", "\"culturally patterned\", tied to education, the economy, politics", "its rules come from outside any one couple", "couples are \"heirs\" to a vast system of understood principles"], width=5.6, size=24).move_to([3.4, 0.3, 0])
        with self.say("Nock's first sentence is his thesis: a marriage is much more than the sum of two spouses. It is a relationship defined by legal, moral and conventional assumptions. It is an institution, in the sociologist's sense: an established pattern of rules and roles, like the family, education or the economy, culturally patterned and tied to those other institutions. Its rules come from outside any particular couple, and couples inherit them, as heirs to a vast system of understood principles."):
            self.play(FadeIn(h), FadeIn(df))
            E.reveal_list(self, pts, 8.0)
        self.play(FadeOut(VGroup(df, pts)))
        a, b = person(th.SKY, "", -0.7, -0.2), person(th.PINK, "", 0.7, -0.2)
        soft = DashedVMobject(Circle(radius=2.0, color=th.AMBER, stroke_width=4).move_to([0, -0.2, 0]), num_dashes=30)
        lab = para("soft boundaries: the commonly understood limits that distinguish marriage from every other relationship. Soft, because no one is arrested for crossing them — opinion, custom and law enforce them together, and they bend.", width=5.0, size=24, color=th.AMBER).move_to([4.0, -0.2, 0])
        with self.say("Those rules set what Nock calls soft boundaries round the couple: the commonly understood limits of behaviour that separate marriage from every other kind of relationship. Soft, because nobody is arrested for crossing them. Opinion, custom and law enforce them together, and they bend."):
            VGroup(a, b).shift(LEFT * 2.6)
            soft.shift(LEFT * 2.6)
            self.play(FadeIn(a), FadeIn(b), Create(soft))
            self.play(FadeIn(lab))
        self.play(FadeOut(VGroup(h, a, b, soft, lab)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = E.head(self, "Émile Durkheim: marriage limits desire")
        stairs = VGroup(*[E.chip(t_, c_, size=24) for t_, c_ in [("necessities: food, housing", th.MUTED), ("well-being, comfort", th.SKY), ("luxury", th.AMBER), ("prestige", th.PINK), ("… always more", th.CORAL)]])
        for k, s_ in enumerate(stairs):
            s_.move_to([-4.2 + 1.6 * k, -2.6 + 0.7 * k, 0])
        nt = para("Desire has no natural limit. Durkheim (1897): marriage is \"an organ of society\" that restrains it — giving love \"a strictly definite object\", closing the horizon, producing \"moral equilibrium\".", width=11.4, size=24, color=th.INK).move_to([0, 2.0, 0])
        with self.say("Why does marriage matter to men? Nock borrows an old argument from the French sociologist Émile Durkheim. In modern societies basic needs are mostly met, so desire moves on: to comfort, luxury, prestige. And those wants have no natural limit; satisfied, they demand more. So the central problem is setting legitimate limits on desire, and Durkheim says marriage does it. It is an organ of society that ties a man to one partner, gives his need for love a strictly definite object, closes the horizon, and so gives him moral equilibrium."):
            self.play(FadeIn(h))
            for s_ in stairs:
                self.play(FadeIn(s_, shift=UP * 0.2), run_time=0.5)
                self.hold(0.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, stairs, nt)))
        h = E.head(self, "\"Moral equilibrium\"")
        beam = Line([-3, 0, 0], [3, 0, 0], color=th.INK, stroke_width=6)
        pivot = Triangle(color=th.AMBER, fill_opacity=1).scale(0.3).next_to(beam, DOWN, buff=0)
        g = VGroup(beam, pivot).move_to([0, 0.3, 0])
        nt = para("Equilibrium = balance. Someone who wants everything is always off balance; limits give a fixed centre to live from. In plain words: a man who knows what is expected of him, and what is closed to him, is calmer than one free to want anything.", width=11, size=26, color=th.BODY).move_to([0, -1.9, 0])
        with self.say("Equilibrium means balance. A person who wants everything is always off balance, because there is always something more to want. Limits give a fixed centre to live from. In plain words: a man who knows what is expected of him, and what is closed to him, is calmer than a man who is free to want anything."):
            self.play(FadeIn(h), FadeIn(g))
            self.play(Rotate(beam, 0.25, about_point=pivot.get_top()), run_time=0.6)
            self.play(Rotate(beam, -0.25, about_point=pivot.get_top()), run_time=0.8)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, g, nt)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = E.head(self, "Freedom, or a template?")
        a = E.card("cohabiting couple", "\"tremendous freedom\": parents, holidays, money — all to invent. Their parents get \"little guidance\" too. Freedom = no help.", th.SKY, w=5.8, h=3.0, size=24).move_to([-3.2, 0.6, 0])
        b = E.card("married couple", "\"a pattern to follow\": marriage \"supplies a template\" for most of domestic life — backed by law, religion and custom", th.AMBER, w=5.8, h=3.0, size=24).move_to([3.2, 0.6, 0])
        nt = para("The double edge: the cohabiting couple's freedom is exactly the absence of the help the married couple has.", width=11, size=26, color=th.MINT).move_to([0, -2.1, 0])
        with self.say("Then an objection: surely two people can live happily together without marrying? Cohabiting couples, Nock agrees, have tremendous freedom: how to deal with each other's parents, whether to holiday together, whether to pool money. Everything is theirs to invent, and their parents get little guidance too. Married couples face many of the same decisions, but they have a pattern to follow: marriage supplies a template. Notice the double edge: the cohabiting couple's freedom is exactly the absence of help."):
            self.play(FadeIn(h), FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(a, b, nt)))
        q1 = T("\"I would like you to meet my wife.\"", size=34, color=th.AMBER).move_to([0, 1.4, 0])
        q2 = T("\"I would like you to meet my ___ .\"", size=34, color=th.SKY).move_to([0, -0.2, 0])
        nt = para("Married pledges are enforceable: others expect them, and law, religion and custom back them. For the unmarried partner there isn't even a word — proof of how little convention governs it. \"It is not an institution.\"", width=11.2, size=24, color=th.INK).move_to([0, -2.2, 0])
        with self.say("One sentence shows the difference. I would like you to meet my wife says a great deal: pledges of faithfulness, duties to children and relatives, and these are not just personal promises but enforceable, because others expect them and law, religion and custom back them up. Now finish this one: I would like you to meet my, what? There is not even a word. That missing word, Nock says, shows how little such relationships are governed by convention. It is not an institution."):
            self.play(FadeIn(q1))
            self.play(FadeIn(q2))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, q1, q2, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = E.head(self, "Three kinds of capital (James Coleman)")
        rows = [["capital", "where it is", "how tangible"], ["physical", "tools, buildings, machines, money", "wholly tangible"], ["human", "skills and knowledge in a person", "less tangible"], ["social", "in the relations among persons", "less tangible yet"]]
        tb = E.table(rows, [2.6, 5.6, 3.6], row_h=0.7, size=26, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.8, 0])
        nt = para("Social capital: networks of people bound by trust that obligations will be incurred and repaid. All three make productive activity possible.", width=11, size=24, color=th.INK).move_to([0, -2.0, 0])
        with self.say("Step four: marriage is a form of capital, as surely as any other resource. Nock borrows three kinds from the sociologist James Coleman. Physical capital: tools, buildings, money, wholly tangible. Human capital: the skills and knowledge in a person, less tangible. And social capital: found in the relations among persons, less tangible yet. It is a network of people linked by trust that obligations will be incurred and repaid.") as v:
            self.play(FadeIn(h))
            E.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        a, b = person(th.SKY, "husband", -1.0, 0.6), person(th.PINK, "wife", 1.0, 0.6)
        kin = VGroup(*[person(c_, l_, x, y) for c_, l_, x, y in [(th.MUTED, "his parents", -4.6, 1.9), (th.MUTED, "his siblings", -4.6, -0.7), (th.MUTED, "her parents", 4.6, 1.9), (th.MUTED, "her siblings", 4.6, -0.7)]])
        links = VGroup(*[Line(k_[0].get_center(), (a if k_.get_x() < 0 else b)[0].get_center(), color=th.AMBER, stroke_width=2) for k_ in kin], *[Line(k_[0].get_center(), (b if k_.get_x() < 0 else a)[0].get_center(), color=th.AMBER, stroke_width=2).set_opacity(0.5) for k_ in kin])
        nt = para("Marriage connects each spouse to new kin, \"woven with threads of obligations\" that persist — help in need, information, honour. \"An individual asset\": intangible, and harder to keep because it exists only in relationships.", width=11.4, size=24, color=th.INK).move_to([0, -2.7, 0])
        with self.say("How does marriage create social capital? Through marriage, husband and wife become connected to new kin, and their friends. Those ties are woven with threads of obligations: in need you can call on relatives and expect help, and the debts persist. So the institution of marriage is an individual asset: intangible, but no less important than money, and harder to keep, because it exists only in relationships with others."):
            self.play(FadeIn(a), FadeIn(b), LaggedStart(*[FadeIn(k_) for k_ in kin], lag_ratio=0.2))
            self.play(LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.1))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, kin, links, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = E.head(self, "Normative marriage in America: six dimensions")
        dims = [("voluntary", "both choose freely"), ("mature", "between adults"), ("heterosexual", "a man and a woman"), ("husband as main earner", "the expected provider"), ("faithful", "fidelity from both"), ("parenthood", "expected to have children")]
        cards = VGroup(*[E.card(f"{k + 1} · {a_}", b_, th.PALETTE[k % 8], w=3.9, h=1.9, tsize=26, size=24) for k, (a_, b_) in enumerate(dims)]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.25)).move_to([0, 0.2, 0])
        with self.say("Finally, the six dimensions that define normative marriage in America, as Nock describes it. Entered voluntarily. By mature adults. Heterosexual. With the husband as the principal earner. Sexually faithful on both sides. And leading to parenthood."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4), run_time=5)
        self.play(FadeOut(cards))
        a = E.card("normative ≠ normal", "normative = how things should be, by society's standard. Many real marriages depart from it — Nock says so.", th.AMBER, w=5.8, h=2.8, size=24).move_to([-3.2, 0.5, 0])
        b = E.card("social control", "yet the ideal still shapes everyone's expectations: \"a force greater than the individuals\", channelling behaviour and hopes", th.CORAL, w=5.8, h=2.8, size=24).move_to([3.2, 0.5, 0])
        nt = para("Context: written about 1990s America. The law has since changed (same-sex marriage, US Supreme Court, 2015), and Nepal's law and customs differ again.", width=11.4, size=24, color=th.MUTED).move_to([0, -2.3, 0])
        with self.say("Two cautions. Normative does not mean normal: it means how marriage should be, by a society's standard, and Nock admits many real marriages depart from it. Yet the ideal is still a form of social control, a force greater than the individuals, channelling their behaviour and hopes. And remember the context: this describes America in the nineteen nineties. The law has since changed, and Nepal's law and customs are different again."):
            self.play(FadeIn(a))
            self.play(FadeIn(b))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, a, b, nt)))
        self.quiz("Why does Nock say cohabitation \"is not an institution\"?",
                  ["it is illegal", "it has no widely accepted rules — not even a word for the partner", "it never lasts", "it has too many rules"], 1,
                  "Pause and think.",
                  "No template and no convention: there isn't even a word to finish \"meet my ___\".")
        self.quiz("Social capital is found",
                  ["in banks", "in tools and machines", "in the relations among persons", "in a person's skills"], 2,
                  "One more.",
                  "In relationships bound by trust — which is why marriage, linking new kin, creates it.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Steven L. Nock (1950–2008); from Marriage in Men's Lives (1998).",
            "Marriage is an institution: rules from outside the couple, soft boundaries.",
            "Durkheim: marriage limits endless desire, giving \"moral equilibrium\".",
            "Cohabitation has freedom but no template — not even a word for the partner.",
            "Marriage is social capital; normative marriage has six dimensions.",
        ], "Quick recap. Nock's five steps. Marriage as an institution with soft boundaries. Durkheim's limits on desire. Cohabitation's freedom without a template. Social capital. And the six dimensions of normative marriage.")
        self.outro("That was Marriage as a Social Institution. Next essay: Knowledge and Wisdom, by Bertrand Russell. See you there.")
