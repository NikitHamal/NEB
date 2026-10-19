"""Class 8 Science and Technology · Unit 1 · Scientific Learning."""
from manim import *
import numpy as np

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kit import Lesson, M, T, para, th  # noqa: E402
from kit.live import Counter  # noqa: E402
import _common as C  # noqa: E402

SC = th.SKY
ICE = "#CFE9FF"
GLASS = "#93A8CC"


# ---------------------------------------------------------------- little shapes
def teardrop(h=0.9, w=0.5, color="#14161F"):
    """A flame / drop shape, pointed at the top."""
    n = 30
    pts = []
    for i in range(n):
        u = i / (n - 1)
        half = w / 2 * np.sin(PI * u ** 0.7) * (1 - 0.78 * u) + 0.01
        pts.append([half, -h / 2 + h * u, 0])
    for i in range(n - 1, -1, -1):
        u = i / (n - 1)
        half = w / 2 * np.sin(PI * u ** 0.7) * (1 - 0.78 * u) + 0.01
        pts.append([-half, -h / 2 + h * u, 0])
    return Polygon(*pts, fill_color=color, fill_opacity=1, stroke_width=0)


def star(points=8, r1=0.3, r2=0.14, color="#14161F"):
    pts = []
    for i in range(points * 2):
        r = r1 if i % 2 == 0 else r2
        a = PI / 2 + i * PI / points
        pts.append([r * np.cos(a), r * np.sin(a), 0])
    return Polygon(*pts, fill_color=color, fill_opacity=1, stroke_width=0)


def skull(s=0.26, color="#14161F"):
    head = Circle(radius=s, fill_color=color, fill_opacity=1, stroke_width=0)
    jaw = RoundedRectangle(corner_radius=0.04, width=s * 1.1, height=s * 0.75,
                           fill_color=color, fill_opacity=1, stroke_width=0).next_to(head, DOWN, buff=-s * 0.45)
    eyes = VGroup(*[Circle(radius=s * 0.26, fill_color=th.BG, fill_opacity=1, stroke_width=0)
                    .move_to(head.get_center() + RIGHT * dx * s * 0.45 + UP * s * 0.15)
                    for dx in (-1, 1)])
    bones = VGroup(
        Line(head.get_center() + DL * s * 1.9, head.get_center() + UR * s * 1.9, color=color, stroke_width=7),
        Line(head.get_center() + DR * s * 1.9, head.get_center() + UL * s * 1.9, color=color, stroke_width=7),
    )
    bones.set_z_index(-1)
    return VGroup(bones, head, jaw, eyes)


def sign(color, sym, size=1.25):
    d = Square(side_length=size).rotate(PI / 4)
    d.set_fill(color, 0.94).set_stroke("#0A0D18", 6)
    sym.move_to(d.get_center())
    return VGroup(d, sym)


def hazard(kind):
    if kind == "flammable":
        s = VGroup(teardrop(0.62, 0.34), Circle(radius=0.13, fill_color=th.AMBER, fill_opacity=1,
                                                stroke_width=0).move_to(DOWN * 0.17))
        return sign("#E8622A", s)
    if kind == "corrosive":
        tube = VGroup(RoundedRectangle(corner_radius=0.05, width=0.2, height=0.5, stroke_color="#14161F",
                                       stroke_width=5, fill_opacity=0).rotate(PI),
                      Line(LEFT * 0.1, RIGHT * 0.1, color="#14161F", stroke_width=5))
        tube[0].move_to(UP * 0.18)
        tube[1].move_to(tube[0].get_top())
        hand = Line(DL * 0.3 + DOWN * 0.2, RIGHT * 0.05 + DOWN * 0.34, color="#14161F", stroke_width=7)
        drip = teardrop(0.16, 0.1, "#14161F").move_to(DOWN * 0.05 + LEFT * 0.16)
        return sign("#F2C230", VGroup(tube, hand, drip))
    if kind == "toxic":
        return sign("#F2F2F2", skull(0.2))
    if kind == "harmful":
        x = VGroup(Line(DL * 0.28, UR * 0.28, color="#14161F", stroke_width=11),
                   Line(DR * 0.28, UL * 0.28, color="#14161F", stroke_width=11))
        return sign("#F2C230", x)
    if kind == "oxidising":
        s = VGroup(Circle(radius=0.2, fill_color="#14161F", fill_opacity=1, stroke_width=0).move_to(DOWN * 0.12),
                   teardrop(0.46, 0.3).move_to(UP * 0.24))
        return sign("#E8622A", s)
    s = VGroup(star(9, 0.34, 0.15))
    return sign("#E8622A", s)


def beaker(w=1.15, h=1.55):
    body = RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=GLASS,
                            stroke_width=3, fill_color="#0D1330", fill_opacity=0.6)
    rim = Line(LEFT * (w / 2 + 0.05), RIGHT * (w / 2 + 0.05), color=GLASS, stroke_width=5)
    rim.move_to(body.get_top() + UP * 0.02)
    ticks = VGroup(*[Line(RIGHT * (w / 2 - 0.02), RIGHT * (w / 2 - 0.2), color=GLASS, stroke_width=2)
                     .shift(body.get_bottom() + RIGHT * 0 + UP * (0.25 + 0.35 * k)) for k in range(4)])
    return VGroup(body, rim, ticks)


def check_mark(color=th.MINT, s=1.0):
    return VGroup(Line([-0.1 * s, 0.02 * s, 0], [-0.02 * s, -0.09 * s, 0], color=color, stroke_width=6),
                  Line([-0.02 * s, -0.09 * s, 0], [0.13 * s, 0.1 * s, 0], color=color, stroke_width=6))


def cross_mark(color=th.CORAL, s=1.0):
    return VGroup(Line([-0.1 * s, 0.1 * s, 0], [0.1 * s, -0.1 * s, 0], color=color, stroke_width=6),
                  Line([-0.1 * s, -0.1 * s, 0], [0.1 * s, 0.1 * s, 0], color=color, stroke_width=6))


class Lesson(Lesson):
    SUBJECT = "sci"
    GRADE = 8
    UNIT = 1
    TITLE = "Scientific Learning"
    SUBTITLE = "How we find out what is true"
    SECTIONS = ["Science and the scientific method", "Variables in an experiment",
                "Safety in the laboratory", "Doing the experiment", "Research work",
                "Running a survey", "Measurement and units"]
    NEXT = "Unit 2 · Information and Communication Technology"
    MOOD = "bright"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7,
                   self.ending)

    # ------------------------------------------------------------ cold open
    def cold_open(self):
        masses = [50, 100, 150]
        times = [240.0, 480.0, 720.0]
        xs = [-4.3, 0.0, 4.3]
        base_y = -1.5
        tr = ValueTracker(0.0)

        beakers = VGroup()
        labels = VGroup()
        dyn = VGroup()
        clocks = VGroup()
        for m, T_, x in zip(masses, times, xs):
            b = beaker(1.35, 1.6).move_to([x, base_y + 0.8, 0])
            beakers.add(b)
            labels.add(T(f"{m} g of ice", size=24, color=ICE, weight="SEMIBOLD").move_to([x, base_y - 0.32, 0]))
            s0 = 0.54 * (m / 50) ** (1 / 3)

            def make(T_=T_, s0=s0, b=b):
                def f():
                    t = tr.get_value()
                    frac = max(0.0, 1 - t / T_)
                    h = 0.1 + 1.0 * (1 - frac)
                    water = Rectangle(width=b[0].width - 0.12, height=h, stroke_width=0,
                                      fill_color="#2F7BC0", fill_opacity=0.62)
                    water.move_to(b[0].get_bottom() + UP * (h / 2 + 0.04))
                    g = VGroup(water)
                    side = s0 * frac ** (1 / 3)
                    if side > 0.04:
                        cube = RoundedRectangle(corner_radius=0.05, width=side, height=side,
                                                stroke_color="#B7E2FF", stroke_width=2.5,
                                                fill_color=ICE, fill_opacity=0.92)
                        cube.move_to(b[0].get_bottom() + UP * (h + side / 2 + 0.05))
                        shine = Line(cube.get_corner(UL) + RIGHT * 0.06 + DOWN * 0.06,
                                     cube.get_corner(UR) + LEFT * 0.06 + DOWN * 0.06,
                                     color=WHITE, stroke_width=2, stroke_opacity=0.7)
                        g.add(cube, shine)
                    return g
                return f
            dyn.add(always_redraw(make()))
            c = Counter(0, digits=3, size=32, color=th.MUTED, suffix="s").move_to([x, base_y + 2.05, 0])
            c.add_updater(lambda mm, T_=T_: mm.set_value(min(tr.get_value(), T_)))
            clocks.add(c)

        q = T("Which one melts first?", size=40, color=th.INK, weight="BOLD", display=True)
        q.to_edge(UP, buff=0.85)

        self.add(beakers, labels, dyn, clocks)
        with self.say("Three beakers, on the same bench, in the same room. Fifty grams of crushed ice, one hundred grams, and one hundred and fifty grams."):
            self.sfx("pop")
            self.play(FadeIn(beakers, shift=UP * 0.2), FadeIn(labels), FadeIn(dyn), FadeIn(clocks), run_time=1.2)
        with self.say("The ice is crushed the same way. The beakers are identical. The room does not change. Only one thing is different: how much ice there is."):
            self.play(Indicate(labels, color=th.INK, scale_factor=1.06), run_time=1.4)
        with self.say("Now we start the clock and let them melt. Which one finishes first? And be careful, that is not the real question. The real question is: how much longer will the big one take?"):
            self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.sfx("whoosh", gain=-14)
        self.play(tr.animate.set_value(720), run_time=10.0, rate_func=linear)
        self.sfx("correct", gain=-14)
        self.play(*[Indicate(c, color=th.MINT, scale_factor=1.15) for c in clocks], run_time=1.0)

        # the bar chart of the three times
        ax = Axes(x_range=[0, 160, 50], y_range=[0, 800, 200], x_length=5.2, y_length=2.5,
                  axis_config={"color": th.FAINT, "stroke_width": 2, "include_tip": False,
                               "font_size": 20, "tick_size": 0.05}, tips=False).move_to([-2.2, 0.55, 0])
        xl = T("mass of ice (g)", size=19, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.28)
        yl = T("time to melt (s)", size=19, color=th.MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.18)
        bars = VGroup()
        for m, t in zip(masses, times):
            p0 = ax.coords_to_point(m, 0)
            p1 = ax.coords_to_point(m, t)
            bars.add(Rectangle(width=0.52, height=p1[1] - p0[1], stroke_width=0, fill_color=SC,
                               fill_opacity=0.8).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        with self.say("Fifty grams: four minutes. One hundred grams: eight minutes. One hundred and fifty grams: twelve minutes. Exactly in step."):
            self.play(FadeOut(VGroup(beakers, labels, dyn, clocks)), FadeOut(q), run_time=0.8)
            self.remove(dyn)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
            for b in bars:
                self.sfx("tick", gain=-12)
                self.play(GrowFromEdge(b, DOWN), run_time=0.35)
        prop = M(r"t \propto m", size=66, color=th.AMBER).move_to([3.7, 1.35, 0])
        pl = para("Double the mass, double the time. Triple the mass, triple the time.",
                  width=4.2, size=23, color=th.BODY).next_to(prop, DOWN, buff=0.55)
        with self.say("Look at that. Double the mass, double the time. Triple the mass, triple the time. The time is proportional to the mass."):
            self.play(Write(prop), FadeIn(pl, shift=UP * 0.2))
        with self.say("And notice what made that conclusion possible. We changed one thing only, and kept everything else the same. That single habit is the whole of this unit. Today you learn the method, the safety, the experiment, the survey, and the measurement that go with it."):
            self.play(Indicate(prop, color=th.AMBER, scale_factor=1.08), run_time=1.2)
        self.play(FadeOut(VGroup(ax, xl, yl, bars, prop, pl)), run_time=0.7)

        g, nb = self.title_card()
        with self.say("This is Class Eight Science and Technology, Unit One: Scientific Learning."):
            pass
        self.end_title(g, nb)
        self.roadmap("Seven stops on the way. The scientific method. Variables. Laboratory safety. "
                     "Doing the experiment. Research work. Running a survey. And measurement and units.")

    # ------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        head = T("What makes a statement scientific?", size=36, color=th.INK, weight="BOLD",
                 display=True).to_edge(UP, buff=0.8)
        with self.say("Let us begin with the hardest idea in this chapter. Science is not a pile of facts in a book. It is a way of finding out what is true."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        defn = self.callout("key", "Science is the organised study of the natural world, based on observation and experiment. Every claim it makes must be testable.",
                            width=6.8, size=24).move_to([-3.35, 0.8, 0])
        with self.say("And here is the test that every scientific claim has to pass. Can it be checked by an observation or a measurement? If it cannot be tested at all, it is not science, however beautiful it sounds."):
            self.sfx("pop")
            self.play(FadeIn(defn, shift=UP * 0.3), run_time=0.7)
        g = C.card(self, "Testable", "A bigger glass of water takes longer to freeze in the same freezer.",
                   color=th.MINT, width=4.4, size=21, title_size=23)
        g.next_to([3.6, 1.5, 0], ORIGIN).shift(DOWN * 0.0)
        b = C.card(self, "Not testable", "Water that is spoken to kindly freezes into prettier ice.",
                   color=th.CORAL, width=4.4, size=21, title_size=23)
        b.next_to(g, DOWN, buff=0.35)
        g.move_to([3.9, 1.55, 0])
        b.next_to(g, DOWN, buff=0.35)
        g.add(check_mark(th.MINT, 1.3).next_to(g[0], LEFT, buff=0.18))
        b.add(cross_mark(th.CORAL, 1.3).next_to(b[0], LEFT, buff=0.18))
        with self.say("Take the first claim: a bigger glass of water takes longer to freeze in the same freezer. Testable. We can weigh the water and time it."):
            self.play(FadeIn(g, shift=RIGHT * 0.3), run_time=0.6)
        with self.say("Now the second: water that is spoken to kindly freezes into prettier ice. How would you measure prettier? Who decides? There is no observation that could settle it, so it is not a scientific statement."):
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeOut(VGroup(head, defn, g, b)), run_time=0.6)

        # the method, as a ring
        names = ["Observe", "Question", "Hypothesis", "Predict", "Experiment", "Analyse", "Conclude"]
        gloss = ["Notice something and describe it exactly.",
                 "Turn it into a question a measurement can answer.",
                 "Give a testable answer before you start.",
                 "Say what you will see if you are right.",
                 "Change one thing, keep the rest the same, and measure.",
                 "Put the readings in a table, then a graph, and look for a pattern.",
                 "Was the hypothesis supported? Then repeat it."]
        C0 = np.array([0.0, 0.1, 0])
        R = 1.5
        nodes, tags, ring = C.ring(7, C0, R, SC, names, label_gap=0, label_size=21)
        for i, tg in enumerate(tags):
            a = PI / 2 - i * TAU / 7
            tg.move_to(C0 + np.array([2.85 * np.cos(a), 2.0 * np.sin(a), 0]))
        strip = T(gloss[0], size=23, color=th.BODY).move_to([0, -2.85, 0])
        marker = Dot(C.at(C0, R, 0, 7), radius=0.1, color=th.AMBER)
        with self.say("Now the working order that scientists follow. Seven steps, and then round again."):
            self.play(FadeIn(ring), LaggedStart(*[FadeIn(n, scale=0.5) for n in nodes], lag_ratio=0.12), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.1), run_time=0.9)
            self.play(FadeIn(marker))
        self.add(strip)
        with self.say("One: observe. Notice something, and describe it exactly. Not that the ice melts fast, but that the ice melted in fifteen minutes in the sun."):
            self.play(FadeIn(strip, shift=UP * 0.15), Indicate(nodes[0], color=SC, scale_factor=1.2), run_time=0.7)
        for i in range(1, 7):
            with self.say(f"{'Two three four five six seven'.split()[i - 1].capitalize()}: {gloss[i][0].lower() + gloss[i][1:]}"):
                p = C.at(C0, R, i, 7)
                nxt = T(gloss[i], size=23, color=th.BODY).move_to([0, -2.85, 0])
                self.sfx("tick", gain=-16)
                self.play(marker.animate.move_to(p), Indicate(nodes[i], color=SC, scale_factor=1.2),
                          FadeOut(strip), FadeIn(nxt), run_time=0.6)
                strip = nxt
        back = CurvedArrow(C0 + R * DOWN + RIGHT * 0.35, C0 + R * UP + RIGHT * 0.35, angle=1.15,
                           color=th.AMBER, stroke_width=3, tip_length=0.16)
        bl = para("repeat, or ask a better question", width=2.3, size=19, color=th.AMBER).move_to([4.5, 0.3, 0])
        with self.say("And then the arrow that matters most. If the result does not support the hypothesis, you do not throw the experiment away. You go back, and you ask a better question."):
            self.play(Create(back), FadeIn(bl), run_time=1.0)
        with self.say("A failed hypothesis is still a result. It is often the most useful one you will get."):
            self.play(Indicate(back, color=th.AMBER, scale_factor=1.05), run_time=1.0)
        self.play(FadeOut(VGroup(ring, nodes, tags, marker, strip, back, bl)), run_time=0.7)

    # ------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        head = T("Three kinds of quantity in every experiment", size=36, color=th.INK,
                 weight="BOLD", display=True).to_edge(UP, buff=0.8)
        with self.say("Every experiment has exactly three kinds of quantity in it, and mixing them up is the most common mistake in school science."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        cols = [("Independent", "the one you change on purpose", "mass of ice: 50 g, 100 g, 150 g", th.AMBER),
                ("Dependent", "the one you measure", "time taken to melt", SC),
                ("Controlled", "the ones you keep the same", "room temperature, beaker, grain size", th.MINT)]
        cards = VGroup()
        for nm, mean, ex, col in cols:
            body = VGroup(para(mean, width=3.4, size=20, color=th.BODY),
                          para(ex, width=3.4, size=19, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            cards.add(C.card(self, nm, body, color=col, width=4.2, title_size=27))
        cards.arrange(RIGHT, buff=0.4).move_to([0, 0.7, 0])
        with self.say("The independent variable is the one you choose and change. In our ice race, that was the mass of the ice: fifty, one hundred, one hundred and fifty grams."):
            self.play(FadeIn(cards[0], shift=UP * 0.3), run_time=0.6)
        with self.say("The dependent variable is the one you measure. It depends on the first one. Here, the time taken to melt."):
            self.play(FadeIn(cards[1], shift=UP * 0.3), run_time=0.6)
        with self.say("And the controlled variables are everything else you deliberately keep the same, so that the result can only be caused by the thing you changed."):
            self.play(FadeIn(cards[2], shift=UP * 0.3), run_time=0.6)
        link = CurvedArrow(cards[0].get_bottom() + DOWN * 0.05, cards[1].get_bottom() + DOWN * 0.05,
                           angle=-0.7, color=th.FAINT, stroke_width=2, tip_length=0.14)
        ll = T("change  →  measure", size=20, color=th.MUTED).next_to(link, DOWN, buff=0.05)
        with self.say("So the independent variable causes the dependent variable, and the controlled variables are held still so that nothing else can sneak in."):
            self.play(Create(link), FadeIn(ll), run_time=0.8)
        self.play(FadeOut(VGroup(head, cards, link, ll)), run_time=0.6)

        # a controlled experiment, and the two-thing trap
        head2 = T("A controlled experiment", size=34, color=th.MINT, weight="BOLD",
                  display=True).to_edge(UP, buff=0.8)
        ok = self.panel(6.1, 2.5, color=th.MINT)
        okt = para("Same beaker, same room, same crushed ice. Only the mass changes.",
                   width=5.4, size=23, color=th.INK).move_to(ok).shift(UP * 0.35)
        okh = T("One change", size=24, color=th.MINT, weight="BOLD").move_to(ok).shift(DOWN * 0.6)
        bad = self.panel(6.1, 2.5, color=th.CORAL)
        bt = para("A bigger piece of ice in a warmer room melts faster. What did you learn? Nothing.",
                  width=5.4, size=23, color=th.INK).move_to(bad).shift(UP * 0.35)
        bh = T("Two changes", size=24, color=th.CORAL, weight="BOLD").move_to(bad).shift(DOWN * 0.6)
        G1 = VGroup(ok, okt, okh).move_to([-3.3, 0.6, 0])
        G2 = VGroup(bad, bt, bh).move_to([3.3, 0.6, 0])
        with self.say("A controlled experiment changes one thing and keeps every other factor the same. That is the only way to know which change caused the result."):
            self.play(FadeIn(head2, shift=DOWN * 0.2), FadeIn(G1, shift=UP * 0.3), run_time=0.8)
        with self.say("Change two things at once, and the experiment tells you nothing. If you use a bigger piece of ice and also move it to a warmer room, and it melts faster, which change did it?"):
            self.play(FadeIn(G2, shift=UP * 0.3), run_time=0.8)
        with self.say("You cannot say. And in an exam, an answer that names the variables but never says which one is controlled loses marks."):
            self.play(Indicate(G2, color=th.CORAL, scale_factor=1.02), run_time=1.2)
        self.play(FadeOut(VGroup(head2, G1, G2)), run_time=0.6)

        self.quiz("In the melting ice experiment, which quantity is the independent variable?",
                  ["The time taken to melt", "The mass of the ice", "The room temperature", "The size of the beaker"], 1,
                  "A question from the exercise at the end of this chapter. Read the four options carefully, and pause to think.",
                  "B, the mass of the ice. You decide it, so you change it on purpose: fifty, one hundred, one hundred and fifty grams. The time is what you measure, so that is the dependent variable. The room temperature and the beaker are held the same, so they are controlled variables.")

    # ------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        head = T("Know the danger before you touch anything", size=34, color=th.INK,
                 weight="BOLD", display=True).to_edge(UP, buff=0.8)
        kinds = [("flammable", "Flammable", "spirit, kerosene, LPG"),
                 ("corrosive", "Corrosive", "strong acids and alkalis"),
                 ("toxic", "Toxic", "mercury, pesticides"),
                 ("harmful", "Harmful", "dilute acids, lime"),
                 ("oxidising", "Oxidising", "permanganate, peroxide"),
                 ("explosive", "Explosive", "sodium in water, dry ice")]
        grid = VGroup()
        for k, nm, ex in kinds:
            s = hazard(k)
            h = T(nm, size=22, color=th.INK, weight="SEMIBOLD")
            e = T(ex, size=17, color=th.MUTED)
            grid.add(VGroup(s, h, e).arrange(DOWN, buff=0.14))
        grid.arrange_in_grid(rows=2, cols=3, buff=(0.55, 0.35)).move_to([0, 0.5, 0])
        with self.say("A laboratory is a room built for experiments, and everything in it carries its own danger. That is why every bottle and every cupboard carries a sign."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        with self.say("Flammable: it catches fire easily. Spirit, kerosene, an L P G cylinder."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[0], scale=0.7), run_time=0.5)
        with self.say("Corrosive: it attacks skin and cloth. Strong acids and strong alkalis."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[1], scale=0.7), run_time=0.5)
        with self.say("Toxic, or poisonous: mercury, and many pesticides."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[2], scale=0.7), run_time=0.5)
        with self.say("Harmful or irritant: dilute acids, lime, bleaching powder."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[3], scale=0.7), run_time=0.5)
        with self.say("Oxidising: potassium permanganate, hydrogen peroxide. These give up oxygen readily and make a fire far worse."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[4], scale=0.7), run_time=0.5)
        with self.say("And explosive: sodium metal dropped in water, or dry ice sealed in a bottle."):
            self.sfx("pop", gain=-14)
            self.play(FadeIn(grid[5], scale=0.7), run_time=0.5)
        self.play(FadeOut(VGroup(head, grid)), run_time=0.6)

        # wafting, the safe way to smell
        head2 = T("Never put your nose over the bottle", size=32, color=th.CORAL, weight="BOLD",
                  display=True).to_edge(UP, buff=0.8)
        bottle = VGroup(RoundedRectangle(corner_radius=0.14, width=1.1, height=1.55, stroke_color=GLASS,
                                         stroke_width=3, fill_color="#12203C", fill_opacity=0.95),
                        RoundedRectangle(corner_radius=0.06, width=0.44, height=0.42, stroke_color=GLASS,
                                         stroke_width=3, fill_color="#12203C", fill_opacity=0.95)
                        .move_to(UP * 0.95),
                        Line(LEFT * 0.26, RIGHT * 0.26, color=GLASS, stroke_width=4).move_to(UP * 1.18))
        bottle.move_to([-3.3, -1.1, 0])
        liq = Rectangle(width=0.92, height=0.6, stroke_width=0, fill_color=th.LIME, fill_opacity=0.3)
        liq.move_to(bottle[0].get_bottom() + UP * 0.36)
        face = VGroup(Circle(radius=0.62, stroke_color=th.BODY, stroke_width=3, fill_color="#1A2140",
                             fill_opacity=1).move_to([3.0, 0.35, 0]),
                      Triangle(stroke_color=th.BODY, stroke_width=3, fill_color="#1A2140", fill_opacity=1)
                      .scale(0.28).rotate(-PI / 2).move_to([2.36, 0.3, 0]),
                      Dot([2.85, 0.55, 0], radius=0.05, color=th.BODY),
                      Dot([3.35, 0.55, 0], radius=0.05, color=th.BODY))
        nose_lab = T("your nose", size=20, color=th.CORAL).next_to(face[0], UP, buff=0.18)
        hand = VGroup(Arc(radius=0.85, start_angle=-PI / 0.9, angle=PI * 0.72, color=th.AMBER, stroke_width=4)
                      .move_to([-0.9, -0.5, 0]),
                      T("fan with your hand", size=19, color=th.AMBER).move_to([-0.75, -1.65, 0]))
        waft = VGroup(*[Dot(bottle[2].get_center() + RIGHT * (0.5 + 0.42 * i) + UP * (0.06 * i),
                            radius=0.05, color=th.LIME) for i in range(7)])
        with self.say("Here is the mistake almost every student makes once. Never put your nose over the mouth of the bottle, and never taste a chemical."):
            self.play(FadeIn(head2, shift=DOWN * 0.2), FadeIn(bottle), FadeIn(liq), run_time=0.8)
            self.play(FadeIn(face), FadeIn(nose_lab))
        with self.say("To smell a gas safely, hold the bottle away from you and fan the vapour towards your nose with your open hand. A little reaches you, and no more."):
            self.play(FadeIn(hand), run_time=0.5)
            for k in range(3):
                self.play(hand.animate(rate_func=there_and_back).shift(RIGHT * 0.45 + UP * 0.25), run_time=0.5)
            self.play(FadeIn(waft), run_time=0.3)
            self.play(waft.animate.shift(RIGHT * 2.6 + UP * 0.55).set_opacity(0.2), run_time=1.6)
        self.play(FadeOut(VGroup(head2, bottle, liq, face, nose_lab, waft, hand)), run_time=0.6)

        # the rules
        rules = ["Read the whole instruction before you start, and follow it in order.",
                 "Wear an apron, and goggles when acids or alkalis are out.",
                 "Never taste a chemical. Fan a gas towards your nose.",
                 "Never point the open end of a test tube at anyone.",
                 "Keep the bench clear of bags and water bottles.",
                 "Turn the gas off at the burner and at the cylinder."]
        head3 = T("Six habits that keep you safe", size=32, color=th.MINT, weight="BOLD",
                  display=True).to_edge(UP, buff=0.8)
        rows = VGroup()
        for i, r in enumerate(rules):
            n = T(str(i + 1), size=22, color=th.MINT, weight="BOLD")
            t = para(r, width=9.4, size=24, color=th.INK)
            rows.add(VGroup(n, t).arrange(RIGHT, buff=0.35, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        rows.next_to(head3, DOWN, buff=0.45).align_to(head3, LEFT).shift(RIGHT * 0.6)
        with self.say("Now the habits. Read the whole instruction before you begin, and follow it in order."):
            self.play(FadeIn(head3, shift=DOWN * 0.2))
            self.sfx("tick", gain=-14)
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.5)
        for i in range(1, 6):
            self.sfx("tick", gain=-14)
            self.play(FadeIn(rows[i], shift=RIGHT * 0.2), run_time=0.45)
        with self.say("Apron on, goggles on. Never taste anything. Never point a test tube at yourself or at a classmate. Keep the bench clear. And when you finish, turn the gas off at the burner and at the cylinder, and wash your hands."):
            self.play(LaggedStart(*[Indicate(r, color=th.MINT, scale_factor=1.02) for r in rows], lag_ratio=0.15), run_time=2.0)
        self.play(FadeOut(VGroup(head3, rows)), run_time=0.5)
        self.tip("Before any experiment, answer three questions. What am I trying to find out? What is the danger here? And what will I do if something goes wrong?",
                 "Before you touch a single thing, answer three questions. What am I trying to find out? What is the danger in this apparatus or this chemical? And what will I do if something goes wrong, a spill, a burn, or broken glass? A student who can answer all three works safely, and writes a better report too.",
                 state="think")

    # ------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        head = T("The report writes itself, if you follow the order", size=32, color=th.INK,
                 weight="BOLD", display=True).to_edge(UP, buff=0.8)
        parts = [("Aim", "one sentence: what you are finding out"),
                 ("Apparatus", "the list, with quantities and sizes"),
                 ("Procedure", "the steps, in order"),
                 ("Observation", "the readings in a table, with units"),
                 ("Result", "the working, formula first"),
                 ("Conclusion", "what the readings show")]
        rows = VGroup()
        for i, (nm, d) in enumerate(parts):
            n = T(str(i + 1), size=24, color=SC, weight="BOLD")
            h = T(nm, size=25, color=th.INK, weight="SEMIBOLD")
            dd = T(d, size=21, color=th.MUTED)
            rows.add(VGroup(n, VGroup(h, dd).arrange(RIGHT, buff=0.28)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rows.next_to(head, DOWN, buff=0.5).align_to(head, LEFT).shift(RIGHT * 0.5)
        with self.say("An experiment is a controlled test of an idea, and its report has six parts. They always come in this order, so a reader can repeat exactly what you did."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.2), run_time=1.6)
        with self.say("Aim, apparatus, procedure, observation, result, conclusion. Six parts, in that order, every single time."):
            self.play(LaggedStart(*[Indicate(r, color=SC, scale_factor=1.03) for r in rows], lag_ratio=0.12), run_time=1.4)
        self.play(FadeOut(VGroup(head, rows)), run_time=0.5)

        # worked experiment
        h2 = T(self.S["example"], size=24, color=SC, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("Does the time an ice cube takes to melt depend on its mass? Three beakers, 50 g, 100 g and 150 g of crushed ice, one balance, one stopwatch.", width=12.0, size=24, color=th.INK)
        prob.next_to(h2, DOWN, aligned_edge=LEFT, buff=0.2)
        with self.say("Let us run the whole experiment on paper. Our aim: to find out how the time taken by ice to melt depends on its mass."):
            self.play(FadeIn(h2), FadeIn(prob, shift=UP * 0.2))
        with self.say("Apparatus: three identical beakers, ice crushed to the same grain size, a balance, a stopwatch, and a thermometer. Procedure: weigh the ice, note the room temperature, start the watch, stir gently, and stop it when no ice is left."):
            self.play(Indicate(prob, color=SC, scale_factor=1.02), run_time=1.4)

        # the observation table
        data = [(50, 240), (100, 480), (150, 720)]
        tbl = C.table(["mass of ice (g)", "time to melt (s)"], data, [2.5, 2.5], size=25, row_h=0.52)
        box = self.panel(tbl.width + 0.9, tbl.height + 0.75, color=th.PANEL_EDGE)
        tbl.move_to(box)
        tblg = VGroup(box, tbl).move_to([-4.0, 0.35, 0])
        cells = [r for r in tbl[2:]]
        with self.say("Now the observations. Fifty grams: two hundred and forty seconds. One hundred grams: four hundred and eighty. One hundred and fifty grams: seven hundred and twenty."):
            self.play(FadeIn(tblg, shift=UP * 0.3), run_time=0.6)
            for c in cells:
                self.sfx("tick", gain=-14)
                self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.35)

        ax = Axes(x_range=[0, 160, 50], y_range=[0, 800, 200], x_length=4.6, y_length=3.0,
                  axis_config={"color": th.FAINT, "stroke_width": 2, "include_tip": False,
                               "font_size": 20, "tick_size": 0.05}, tips=False).move_to([2.9, -0.6, 0])
        xl = T("mass (g)", size=19, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = T("time (s)", size=19, color=th.MUTED).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.2)
        line = ax.plot_line_graph([50, 100, 150], [240, 480, 720], add_vertex_dots=True,
                                  line_color=SC, vertex_dot_radius=0.055,
                                  vertex_dot_style={"fill_color": SC, "stroke_width": 0})
        with self.say("Put those readings on a graph. Mass across, time up."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
            self.play(Create(line["line_graph"]), run_time=1.2)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in line["vertex_dots"]], lag_ratio=0.15), run_time=0.6)
        thru = ax.plot(lambda x: 4.8 * x, x_range=[0, 160], color=th.AMBER, stroke_width=3)
        tl = T("a straight line through zero", size=20, color=th.AMBER).move_to([2.9, 1.05, 0])
        with self.say("And look what happens. The three points fall on a straight line, and that line goes through zero. That shape has a name: directly proportional."):
            self.play(Create(thru), FadeIn(tl), run_time=1.2)
        res = M(r"\frac{480}{240}=2,\quad \frac{720}{240}=3", size=38, color=th.INK).move_to([-4.0, -1.85, 0])
        res2 = M(r"t \propto m", size=52, color=th.AMBER).move_to([-4.0, -2.6, 0])
        with self.say("Check it with the numbers. Four eighty over two forty is two. Seven twenty over two forty is three. So the time is proportional to the mass, and the hypothesis was supported."):
            self.play(Write(res), Write(res2), run_time=1.2)
        with self.say("One precaution belongs in every report. Ice of a different grain size melts at a different speed, so all three samples must be crushed the same way, and stirred equally gently, because stirring warms the mixture."):
            self.play(Indicate(tblg, color=th.MINT, scale_factor=1.02), run_time=1.2)
        self.play(FadeOut(VGroup(h2, prob, tblg, ax, xl, yl, line, thru, tl, res, res2)), run_time=0.7)

    # ------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        head = T("A school research project, done properly", size=32, color=th.INK,
                 weight="BOLD", display=True).to_edge(UP, buff=0.8)
        steps = ["Choose a narrow question", "Read what is already known", "Plan how to collect evidence",
                 "Collect it honestly", "Organise it in tables and graphs", "Write the report"]
        rows = VGroup()
        for i, s in enumerate(steps):
            c = Circle(radius=0.22, fill_color=th.PANEL, fill_opacity=1, stroke_color=SC, stroke_width=2)
            n = T(str(i + 1), size=20, color=SC, weight="BOLD").move_to(c)
            t = T(s, size=24, color=th.INK)
            rows.add(VGroup(VGroup(c, n), t).arrange(RIGHT, buff=0.32))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to(head, DOWN, buff=0.5).align_to(head, LEFT).shift(RIGHT * 0.8)
        with self.say("Research is a careful search for an answer to a question that is not yet settled. A school project is small, but it follows the same steps."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        with self.say("First, choose a narrow question. How much water does a household in my ward use in a day? That can be studied in a week."):
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.5)
        with self.say("How can Nepal solve its water problem? That cannot. A question that is too big cannot be answered with the evidence you can actually collect."):
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.5)
        with self.say("Then read what is already known, and write down where each fact came from. Plan how you will collect evidence: measure, count, interview, or survey."):
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2), run_time=0.5)
        with self.say("Collect it honestly. Never change a reading to make the story neater. Then organise it into tables and simple graphs."):
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2), run_time=0.5)
        with self.say("And finally, write the report: title, aim, method, findings, conclusion, and a list of sources."):
            self.play(FadeIn(rows[4], shift=RIGHT * 0.2), FadeIn(rows[5], shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(head, rows)), run_time=0.5)

        copy = self.callout("careful", "Copying three paragraphs from a website and changing a few words is not research. It teaches nothing, and it is not yours.",
                            width=9.6, size=26).move_to([0, 1.4, 0])
        mine = self.callout("remember", "Your own reading from the meter, or your own count of the households, is the part that is yours.",
                            width=9.6, size=26).move_to([0, -0.5, 0])
        with self.say("One warning. Copying three paragraphs from a website and changing a few words is not research. It is copying, and it teaches you nothing."):
            self.sfx("thud", gain=-16)
            self.play(FadeIn(copy, shift=UP * 0.3), run_time=0.7)
        with self.say("When you use someone else's finding, say where it came from. Your own reading, your own count, your own measurement, that is the part that is really yours."):
            self.sfx("pop", gain=-12)
            self.play(FadeIn(mine, shift=UP * 0.3), run_time=0.7)
        self.play(FadeOut(VGroup(copy, mine)), run_time=0.6)

    # ------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        head = T("A survey asks the same question of everyone", size=32, color=th.INK,
                 weight="BOLD", display=True).to_edge(UP, buff=0.8)
        with self.say("A survey collects information from many people or places by asking the same questions of each. We use it when measuring directly is impossible."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        # the ward
        ward = RoundedRectangle(corner_radius=0.14, width=8.6, height=4.4, stroke_color=th.PANEL_EDGE,
                                stroke_width=3, fill_color="#101733", fill_opacity=1).move_to([-2.5, -0.5, 0])
        wl = T("Ward 5  ·  2000 households", size=22, color=th.MUTED).next_to(ward, UP, buff=0.15)
        houses = VGroup()
        sample = VGroup()
        lanes = VGroup()
        for r in range(4):
            y = ward.get_center()[1] + 1.35 - r * 0.95
            lanes.add(Line([ward.get_left()[0] + 0.3, y, 0], [ward.get_right()[0] - 0.3, y, 0],
                           color=th.FAINT, stroke_width=1.5))
            for c in range(9):
                x = ward.get_left()[0] + 0.75 + c * 0.9
                h = RoundedRectangle(corner_radius=0.03, width=0.3, height=0.3, stroke_width=0,
                                     fill_color=th.PANEL_EDGE, fill_opacity=1).move_to([x, y, 0])
                houses.add(h)
                if c % 4 == 1:
                    sample.add(h.copy().set_fill(SC, 0.95))
        with self.say("Here is our ward: two thousand households, along eight lanes. We cannot visit them all in a week."):
            self.play(DrawBorderThenFill(ward), FadeIn(wl), LaggedStart(*[FadeIn(h) for h in houses], lag_ratio=0.02), run_time=1.4)
        with self.say("So we take a sample. One household in every few, all the way down every lane. That is a fair sample, because every part of the ward is represented."):
            self.play(LaggedStart(*[GrowFromCenter(s) for s in sample], lag_ratio=0.08), run_time=1.4)
            self.sfx("shimmer", gain=-14)
        with self.say("A sample made of your own friends, all from one lane, is not fair. The way you choose the sample matters more than how big it is."):
            self.play(Indicate(sample, color=SC, scale_factor=1.1), run_time=1.2)
        self.play(FadeOut(VGroup(head, ward, wl, houses, sample, lanes)), run_time=0.6)

        # worked survey with tally table and bar chart
        h2 = T(self.S["example"], size=24, color=SC, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A sample of 40 households. One question: does your household separate degradable waste from non-degradable waste?",
                    width=7.4, size=23, color=th.INK)
        prob.next_to(h2, DOWN, aligned_edge=LEFT, buff=0.2)
        with self.say("Let us work one out. A sample of forty households, taken every fifth house on four lanes, and one question asked of an adult in each home."):
            self.play(FadeIn(h2), FadeIn(prob, shift=UP * 0.2))
        rows_data = [("Yes, always", "22", th.MINT), ("Sometimes", "12", th.AMBER), ("No", "6", th.CORAL)]
        tbl = C.table(["Answer", "Number"],
                      [(nm, n) for nm, n, _ in rows_data] + [("Total", "40")],
                      [3.0, 1.9], size=24, row_h=0.5)
        box = self.panel(tbl.width + 0.8, tbl.height + 0.7, color=th.PANEL_EDGE)
        tbl.move_to(box)
        tblg = VGroup(box, tbl).move_to([-3.9, -1.0, 0])
        body = tbl[2:]
        with self.say("The tally gives twenty two who always separate, twelve who sometimes do, and six who never. Forty in total."):
            self.play(FadeIn(tblg, shift=UP * 0.3), run_time=0.6)
            for r in body:
                self.sfx("tick", gain=-14)
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.35)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 25, 5], x_length=3.6, y_length=2.6,
                  axis_config={"color": th.FAINT, "stroke_width": 2, "include_tip": False,
                               "font_size": 18, "tick_size": 0.05}, tips=False).move_to([3.2, -1.0, 0])
        labs = VGroup(*[T(s, size=17, color=th.MUTED).next_to(ax.coords_to_point(i + 0.5, 0), DOWN, buff=0.25)
                        for i, s in enumerate(["always", "somet", "never"])])
        bars = VGroup()
        for i, (nm, n, col) in enumerate(rows_data):
            p0 = ax.coords_to_point(i + 0.5, 0)
            p1 = ax.coords_to_point(i + 0.5, int(n))
            bars.add(Rectangle(width=0.5, height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                               fill_opacity=0.8).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
        with self.say("A bar chart shows the same thing at a glance. The always bar is the tallest, but it is not a majority on its own."):
            self.play(Create(ax), FadeIn(labs), run_time=0.7)
            for b in bars:
                self.sfx("tick", gain=-16)
                self.play(GrowFromEdge(b, DOWN), run_time=0.3)
        frac = M(r"\frac{22}{40}=0.55=55\%", size=44, color=th.AMBER).move_to([3.2, 1.5, 0])
        with self.say("Twenty two out of forty is zero point five five, so fifty five per cent of the sample always separate their waste."):
            self.play(Write(frac), run_time=1.0)
        lim = self.callout("careful", "The survey shows what people said. It does not prove that they do it, and 40 households cannot stand for all 2000. Both limits belong in the report.",
                           width=8.4, size=22).move_to([0, 1.6, 0])
        with self.say("And now the honest part, which belongs in every survey report. It shows what people said, not what they do. And forty households cannot stand for two thousand."):
            self.play(FadeOut(VGroup(h2, prob, frac)), run_time=0.5)
            self.play(FadeIn(lim, shift=UP * 0.3), run_time=0.7)
        self.play(FadeOut(VGroup(tblg, ax, labs, bars, lim)), run_time=0.7)

        self.quiz("A student wants to know how many families in a ward of 2000 separate their waste. Which sample is the fairest?",
                  ["Forty of the student's own classmates", "Every fifth house along every lane", "The first forty houses at the ward entrance", "Twenty houses from the richest lane"], 1,
                  "Think about the ward we just drew, with eight lanes. Which sample would really stand for the whole ward?",
                  "B, every fifth house along every lane. Every lane is represented, so the sample looks like the ward. Classmates are all from one school, the first forty houses are all from one corner, and the richest lane is one lane only. A fair sample must cover every part of the population, or the answer describes the sample and not the ward.")

    # ------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        head = T("A number without a unit means nothing", size=32, color=th.INK, weight="BOLD",
                 display=True).to_edge(UP, buff=0.8)
        with self.say("Every measurement has two parts: a number and a unit. A length of five means nothing at all. Five metres means something."):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        five = T("5", size=120, color=th.MUTED, weight="BOLD", display=True).move_to([-3.6, 0.4, 0])
        with self.say("Five. Five what? Five grains of rice? Five kilometres?"):
            self.play(FadeIn(five, scale=1.3), run_time=0.8)
        m5 = T("5 m", size=120, color=SC, weight="BOLD", display=True).move_to([-3.6, 0.4, 0])
        mlab = T("now it is a measurement", size=24, color=th.MUTED).next_to(m5, DOWN, buff=0.3)
        with self.say("Add the unit, and it becomes a measurement."):
            self.sfx("pop")
            self.play(ReplacementTransform(five, m5), FadeIn(mlab, shift=UP * 0.1), run_time=0.9)

        rows_data = [("Length", "metre", "m", "ruler, tape"),
                     ("Mass", "kilogram", "kg", "beam balance"),
                     ("Time", "second", "s", "stopwatch"),
                     ("Temperature", "kelvin", "K", "thermometer"),
                     ("Current", "ampere", "A", "ammeter")]
        tab = VGroup()
        hdrs = ["Quantity", "SI unit", "Symbol", "Instrument"]
        widths = [2.3, 2.6, 1.3, 3.0]
        x = -5.6
        hp = []
        for w, h in zip(widths, hdrs):
            hp.append(T(h, size=20, color=th.MUTED).move_to([x + w / 2, 1.55, 0]))
            x += w
        tab.add(VGroup(*hp))
        for i, r in enumerate(rows_data):
            y = 1.05 - i * 0.52
            x = -5.6
            cells = VGroup()
            for j, (w, v) in enumerate(zip(widths, r)):
                col = th.INK if j < 3 else th.MUTED
                sz = 22 if j < 3 else 20
                cells.add(T(v, size=sz, color=col).move_to([x + w / 2, y, 0]))
                x += w
            tab.add(cells)
        sep = Line([-5.7, 1.35, 0], [5.5, 1.35, 0], color=th.PANEL_EDGE, stroke_width=2)
        tab.add(sep)
        with self.say("These are the units you will use all year. Length in metres, mass in kilograms, time in seconds, temperature in kelvin, and electric current in amperes."):
            self.play(FadeOut(VGroup(m5, mlab)), run_time=0.4)
            self.play(FadeIn(tab[0]), Create(sep), run_time=0.5)
            for r in tab[1:6]:
                self.sfx("tick", gain=-16)
                self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.3)
        with self.say("Notice the instrument beside each one. A measurement is only as good as the instrument that made it."):
            self.play(LaggedStart(*[Indicate(r[-1], color=SC, scale_factor=1.15) for r in tab[1:6]], lag_ratio=0.12), run_time=1.4)
        pre = VGroup(T("1 km = 1000 m", size=26, color=th.INK), T("1 m = 100 cm", size=26, color=th.INK),
                     T("1 cm = 10 mm", size=26, color=th.INK), T("1 kg = 1000 g", size=26, color=th.INK))
        pre.arrange(RIGHT, buff=0.75).move_to([0, -2.55, 0])
        with self.say("Bigger and smaller units are built with prefixes. A thousand metres is a kilometre. A hundred centimetres is a metre. A thousand grams is a kilogram."):
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pre], lag_ratio=0.2), run_time=1.2)
        self.play(FadeOut(VGroup(head, tab, sep, pre)), run_time=0.6)

        # the density worked example, with a real measuring cylinder
        h2 = T(self.S["example"], size=24, color=SC, weight="BOLD").to_corner(UL, buff=0.75)
        prob = para("A stone of mass 84 g is lowered into a measuring cylinder holding 40 ml of water. The level rises to 72 ml. Find its volume and density, and say whether it floats.",
                    width=7.2, size=22, color=th.INK)
        prob.next_to(h2, DOWN, aligned_edge=LEFT, buff=0.2)
        with self.say("Here is a measurement question of the kind the exam loves. A stone of mass eighty four grams is lowered into a measuring cylinder holding forty millilitres of water, and the level rises to seventy two."):
            self.play(FadeIn(h2), FadeIn(prob, shift=UP * 0.2))
        cyl = RoundedRectangle(corner_radius=0.07, width=1.9, height=3.5, stroke_color=GLASS, stroke_width=3,
                               fill_color="#0D1330", fill_opacity=0.65).move_to([3.1, -0.55, 0])
        marks = VGroup()
        for k in range(6):
            y = cyl.get_bottom()[1] + 0.4 + k * 0.55
            marks.add(Line([cyl.get_left()[0] + 0.1, y, 0], [cyl.get_left()[0] + 0.45, y, 0],
                           color=GLASS, stroke_width=2))
            marks.add(T(str(20 * k), size=16, color=th.MUTED).move_to([cyl.get_left()[0] - 0.28, y, 0]))
        lvl = ValueTracker(40.0)
        water = always_redraw(lambda: Rectangle(width=1.72, height=0.02 + (lvl.get_value() / 120) * 3.1,
                                                stroke_width=0, fill_color="#2E6FA8", fill_opacity=0.62)
                              .move_to(cyl.get_bottom() + UP * (0.02 + (lvl.get_value() / 120) * 3.1) / 2 + UP * 0.04))
        stone = VGroup(Circle(radius=0.3, fill_color="#8C7A6B", fill_opacity=1, stroke_width=0),
                       Circle(radius=0.3, fill_color="#A89684", fill_opacity=1, stroke_width=0).scale(0.7)
                       .shift(RIGHT * 0.1 + UP * 0.08))
        stone.move_to([3.1, 2.2, 0])
        with self.say("Watch the water. The stone displaces its own volume, so the rise tells us the volume of the stone."):
            self.play(FadeIn(cyl), FadeIn(marks), run_time=0.8)
            self.add(water)
            self.play(FadeIn(stone), stone.animate.move_to([3.1, -0.9, 0]), run_time=1.0)
            self.sfx("thud", gain=-18)
            self.play(lvl.animate.set_value(72), run_time=1.2)
        v72 = T("72 ml", size=21, color=th.AMBER).next_to([3.1, -0.05, 0], RIGHT, buff=0.2)
        self.play(FadeIn(v72))
        steps = VGroup(
            M(r"V = 72 - 40 = 32\ \text{cm}^{3}", size=40),
            M(r"\rho = \frac{m}{V} = \frac{84}{32} = 2.625\ \text{g cm}^{-3}", size=40),
            M(r"\rho_{\text{water}} = 1\ \text{g cm}^{-3} \;\Rightarrow\; \text{sinks}", size=40, color=th.CORAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.4, -0.5, 0])
        with self.say("Volume equals seventy two minus forty, thirty two cubic centimetres. That is the volume of the stone."):
            self.play(Write(steps[0]), run_time=0.9)
        with self.say("Density is mass over volume: eighty four over thirty two, which is two point six two five grams per cubic centimetre."):
            self.play(Write(steps[1]), run_time=0.9)
        with self.say("Water has a density of one gram per cubic centimetre. The stone is denser than water, so it sinks."):
            self.play(Write(steps[2]), run_time=0.9)
        self.play(FadeOut(VGroup(h2, prob, cyl, marks, water, stone, v72, steps)), run_time=0.7)
        self.remove(water)

        self.tip("Write the unit in the column head of your table, never beside every number. And before you record a reading, ask whether it is sensible: a classroom is about 8 m long, not 8 cm.",
                 "Two habits protect every reading you take. Write the unit once, in the head of the column, never beside every number. And before you write a reading down, ask whether it is sensible. A classroom is about eight metres long, not eight centimetres, and a school bag weighs a few kilograms, not a few grams. If the number looks impossible, the unit or the instrument is wrong.",
                 state="think")

    # ------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Science is organised knowledge, tested by observation and experiment.",
            "The method: observe, question, hypothesise, predict, experiment, analyse, conclude, and repeat.",
            "Change the independent variable, measure the dependent one, keep the controlled ones the same.",
            "Read first, wear goggles and apron, never taste, never point a tube at anyone.",
            "A report has aim, apparatus, procedure, observation, result, conclusion.",
            "A survey needs a fair sample, the same questions, a tally table, and honest limits.",
            "Every measurement needs a unit, and every reading must be sensible.",
        ], "Let us gather it together. Science is organised knowledge, tested by observation and experiment. The method is a loop: observe, question, hypothesise, predict, experiment, analyse, conclude, and then repeat. In a controlled experiment you change the independent variable, measure the dependent one, and hold everything else the same. In the laboratory: read first, wear your goggles and apron, never taste, never point a tube at anyone. A report has six parts in a fixed order. A survey needs a fair sample and an honest statement of its limits. And every measurement needs a unit.")
        self.outro("That is scientific learning, the toolkit for the rest of the year. Next time, we look at the tools themselves: information and communication technology. Keep asking good questions, and see you in the next lesson on NEBians.")
