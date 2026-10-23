import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _common as C  # noqa: E402
from _common import chem  # noqa: E402


def profile(ax, r=1.0, ts=3.4, p=0.2, w=1.0):
    """A smooth energy-profile curve on axes ax: reactant level r, barrier top ts, product level p."""
    def f(x):
        if x < 0:
            return r
        if x > 10:
            return p
        s = x / 10
        base = r + (p - r) * (3 * s * s - 2 * s ** 3)
        bump = (ts - (r + p) / 2) * np.exp(-((s - 0.5) ** 2) / (2 * (0.13 * w) ** 2))
        return base + bump
    return f


def mb(E, kT):
    return 2 / np.sqrt(np.pi) * kT ** -1.5 * np.sqrt(max(E, 0)) * np.exp(-E / kT)


class Lesson(Lesson):
    SUBJECT = "chem"
    GRADE = 12
    UNIT = 3
    TITLE = "Chemical Kinetics"
    SUBTITLE = "How fast, and why"
    SECTIONS = ["Introduction", "Average and instantaneous rate", "Rate law", "Rate constant and its unit",
                "Order and molecularity", "Integrated rate equations", "Half-life", "Collision theory",
                "Factors affecting rate", "Catalysis"]
    NEXT = "Unit 4 · Thermodynamics"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.p9, self.p10, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        gem = Polygon([-1.2, 0.6, 0], [1.2, 0.6, 0], [1.8, 0, 0], [0, -1.9, 0], [-1.8, 0, 0], fill_color="#BFE9FF", fill_opacity=0.9, stroke_color=WHITE, stroke_width=3)
        facets = VGroup(*[Line(a, b, color=WHITE, stroke_width=1.5, stroke_opacity=0.7) for a, b in [
            ([-1.2, 0.6, 0], [-0.6, 0, 0]), ([1.2, 0.6, 0], [0.6, 0, 0]), ([-1.8, 0, 0], [1.8, 0, 0]), ([-0.6, 0, 0], [0, -1.9, 0]), ([0.6, 0, 0], [0, -1.9, 0]), ([0, 0.6, 0], [-0.6, 0, 0]), ([0, 0.6, 0], [0.6, 0, 0])]])
        d = VGroup(gem, facets).move_to([-3.2, 0.2, 0])
        gr = VGroup(*[Line([-1.3, 0.3 * k, 0], [1.3, 0.3 * k, 0], color="#4A4F60", stroke_width=10) for k in range(-3, 4)]).move_to([3.4, 0.2, 0])
        dl = T("diamond", size=30, color="#BFE9FF", weight="SEMIBOLD").next_to(d, DOWN, buff=0.4)
        gl = T("graphite", size=30, color=th.MUTED, weight="SEMIBOLD").next_to(gr, DOWN, buff=0.4)
        arr = Arrow(d.get_right(), gr.get_left(), buff=0.3, color=th.AMBER, stroke_width=6)
        al = T("releases energy: spontaneous", size=24, color=th.AMBER).next_to(arr, DOWN, buff=0.15)
        with self.say("Here is a fact that sounds like a joke. Diamond is unstable. Turning diamond into graphite, pencil lead, releases energy. Thermodynamics says it is spontaneous. Every diamond in the world is supposed to be turning into graphite."):
            self.play(DrawBorderThenFill(d), FadeIn(dl))
            self.play(GrowArrow(arr), FadeIn(al))
            self.play(FadeIn(gr), FadeIn(gl))
        ring = Circle(radius=0.55, stroke_color="#E8C547", stroke_width=10).move_to(d.get_bottom() + DOWN * 0.15)
        yrs = T("after 100 years: still a diamond", size=30, color=th.INK, weight="BOLD").to_edge(DOWN, buff=0.6)
        with self.say("And yet your grandmother's diamond ring looks exactly the same after a hundred years. Not a speck of graphite. If the reaction is spontaneous, why does nothing happen?"):
            self.play(d.animate.scale(0.6).shift(UP * 0.3), FadeOut(dl), run_time=0.6)
            self.play(Create(ring))
            self.play(FadeIn(yrs, shift=UP * 0.2))
        nb = C.show_neby(self, "think", height=1.5, at=[0, -1.2, 0])
        with self.say("Thermodynamics tells you whether a reaction can happen. It says nothing about how long it takes. That missing half of the story is chemical kinetics. By the end of this lesson, you will see the barrier that guards every diamond."):
            self.wait(0.5)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(d, gr, gl, arr, al, ring, yrs)))
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Chemistry, Unit 3: Chemical Kinetics. How fast reactions go, what controls their speed, and the energy barrier every collision must clear."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. What kinetics is. Average and instantaneous rates. The rate law, the rate constant and its units. Order and molecularity. Integrated rate equations, and half life. Collision theory and activation energy. The factors that change the rate, including the Arrhenius equation. And finally, catalysis.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        d = self.callout("key", "Chemical kinetics: the study of the rate of a reaction, the factors affecting it, and its mechanism, the sequence of elementary steps.", width=11.5, size=28).to_edge(UP, buff=0.8)
        with self.say("Chemical kinetics studies three things: the rate of a reaction, the factors that change that rate, and the mechanism, the sequence of simple steps by which reactants become products."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        nl = NumberLine(x_range=[-12, 15, 3], length=12.4, include_numbers=False, color=th.MUTED).move_to([0, -2.0, 0])
        labs = VGroup(*[M(r"10^{" + str(k) + r"}\,\mathrm{s}", size=30, color=th.MUTED).next_to(nl.n2p(k), DOWN, buff=0.2) for k in range(-12, 16, 3)])
        items = [(-9, "ionic: AgNO₃ + NaCl,\nH⁺ + OH⁻", th.SKY), (3, "H₂O₂ decomposing,\nester hydrolysis", th.MINT),
                 (8, "rusting of iron", th.AMBER), (13.5, "formation\nof coal", th.CORAL)]
        tags = VGroup()
        for i, (x, s, c) in enumerate(items):
            t = T(s, size=22, color=c, line_spacing=0.8)
            y = -0.6 + (i % 2) * 1.3
            t.move_to([nl.n2p(x)[0], y, 0])
            tags.add(VGroup(Line(nl.n2p(x), t.get_bottom() + DOWN * 0.05, color=c, stroke_width=2), Dot(nl.n2p(x), color=c), t))
        band = Rectangle(width=nl.n2p(5)[0] - nl.n2p(0)[0], height=0.3, fill_color=th.MINT, fill_opacity=0.3, stroke_width=0).move_to((nl.n2p(0) + nl.n2p(5)) / 2)
        bl = T("measurable in the lab", size=20, color=th.MINT).next_to(band, DOWN, buff=0.55)
        with self.say("Reactions span an astonishing range of speeds. Ionic reactions, like silver nitrate with salt, or acid with alkali, finish in a millionth of a second. Rusting takes years. Coal takes millions of years to form. In between, in minutes to hours, sit reactions like the decomposition of hydrogen peroxide, the ones we can actually follow in a laboratory.") as v:
            self.play(FadeOut(d), Create(nl), FadeIn(labs))
            for t in tags:
                self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
                self.hold(v.dur / 5 - 0.6)
            self.play(FadeIn(band), FadeIn(bl))
        self.play(FadeOut(VGroup(nl, labs, tags, band, bl)))
        cards = VGroup(
            C.card(self, "Cement", "residence time in the Hetauda kiln", w=3.0, h=2.0, color=th.AMBER, bsize=21),
            C.card(self, "Medicine", "the expiry date on a paracetamol strip", w=3.0, h=2.0, color=th.SKY, bsize=21),
            C.card(self, "Food", "how fast food spoils in Terai heat", w=3.0, h=2.0, color=th.CORAL, bsize=21),
            C.card(self, "Water", "how long chlorine protects a tank", w=3.0, h=2.0, color=th.MINT, bsize=21),
        ).arrange(RIGHT, buff=0.25)
        with self.say("Why should you care? Kinetics fixes how long cement stays in the kiln at Hetauda, the expiry date on your paracetamol, how quickly food spoils in the Terai summer, and how long chlorine keeps a Kathmandu water tank safe.") as v:
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)
                self.hold(v.dur / 4 - 0.5)
        self.play(FadeOut(cards))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1.0, 0.2], x_length=7.2, y_length=4.6, tips=False,
                  axis_config={"color": th.MUTED, "include_numbers": True, "font_size": 26}).move_to([-2.4, -0.4, 0])
        xl = T("time", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = T("[R]", size=24, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.15)
        f = lambda t: np.exp(-0.25 * t)
        curve = ax.plot(f, x_range=[0, 10], color=th.SKY, stroke_width=4)
        d = M(r"\text{average rate} = -\frac{\Delta[\mathrm{R}]}{\Delta t} = +\frac{\Delta[\mathrm{P}]}{\Delta t}", size=36).move_to([3.6, 2.4, 0])
        unit = T("unit: mol L⁻¹ s⁻¹", size=22, color=th.MUTED).next_to(d, DOWN, buff=0.2)
        with self.say("The rate of a reaction is the change in concentration per unit time. As a reactant R is used up, its concentration falls along a curve like this. The average rate over an interval is minus delta R over delta t, or plus delta P over delta t for a product. The minus sign just keeps the rate positive. The unit is moles per litre per second."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=1.5)
            self.play(Write(d), FadeIn(unit))
        t1 = 2.0
        dt = ValueTracker(6.0)

        def chord():
            a, b = t1, t1 + dt.get_value()
            p, q = ax.c2p(a, f(a)), ax.c2p(b, f(b))
            u = (q - p) / np.linalg.norm(q - p)
            return VGroup(Line(p - u * 1.2, q + u * 1.2, color=th.AMBER, stroke_width=4), Dot(p, color=th.AMBER), Dot(q, color=th.AMBER))
        ch = always_redraw(chord)
        lab = T("chord: average rate", size=24, color=th.AMBER).move_to([3.6, 0.6, 0])
        with self.say("On the graph, the average rate is the slope of a chord joining two points. But the curve is steep at first and flat later, so an average over a long interval describes neither."):
            self.add(ch)
            self.play(FadeIn(ch), FadeIn(lab))
        lab2 = T("tangent: instantaneous rate", size=24, color=th.CORAL).move_to([3.6, 0.6, 0])
        rinst = M(r"r_{\text{inst}} = -\frac{d[\mathrm{R}]}{dt}", size=44, color=th.CORAL).move_to([3.6, -0.6, 0])
        with self.say("Now shrink the interval. The second point slides towards the first, and the chord turns into the tangent. Its slope is the instantaneous rate, minus d R by d t. The instantaneous rate at time zero is the initial rate, the one we use to find rate laws."):
            nb = C.show_neby(self, "cool", height=1.3, corner=DR)
            self.play(dt.animate.set_value(0.02), run_time=3.5, rate_func=smooth)
            self.play(FadeTransform(lab, lab2), Write(rinst))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(ax, xl, yl, curve, d, unit, lab2, rinst)), FadeOut(ch))
        self.remove(ch)
        eq = chem(r"2N_2O_5 \rightarrow 4NO_2 + O_2", size=48).to_edge(UP, buff=0.8)
        rr = M(r"r = -\frac{1}{2}\frac{d[\mathrm{N_2O_5}]}{dt} = +\frac{1}{4}\frac{d[\mathrm{NO_2}]}{dt} = +\frac{d[\mathrm{O_2}]}{dt}", size=40).next_to(eq, DOWN, buff=0.35)
        k = ValueTracker(0)
        base = -2.9
        cols = [(r"\mathrm{N_2O_5}", th.CORAL, -2), (r"\mathrm{NO_2}", th.AMBER, 4), (r"\mathrm{O_2}", th.SKY, 1)]
        bars = VGroup()
        for i, (n, c, s) in enumerate(cols):
            x = -3.2 + i * 3.2
            def mk(x=x, c=c, s=s):
                h0 = 2.0 if s < 0 else 0.0
                h = max(0.02, h0 + s * 0.25 * k.get_value())
                return Rectangle(width=1.1, height=h, fill_color=c, fill_opacity=0.85, stroke_width=0).move_to([x, base, 0], aligned_edge=DOWN)
            bars.add(always_redraw(mk))
        names = VGroup(*[M(n, size=32, color=c).move_to([-3.2 + i * 3.2, base - 0.3, 0]) for i, (n, c, s) in enumerate(cols)])
        names.next_to([0, base, 0], DOWN, buff=0.15)
        for i, nm in enumerate(names):
            nm.set_x(-3.2 + i * 3.2)
        rates = VGroup(T("−2 units", size=22, color=th.CORAL), T("+4 units", size=22, color=th.AMBER), T("+1 unit", size=22, color=th.SKY))
        for i, r in enumerate(rates):
            r.move_to([-3.2 + i * 3.2, 0.2, 0])
        with self.say("With unequal coefficients, each species changes at its own speed. In two N two O five giving four N O two plus O two, for every two molecules of N two O five lost, four N O two and one O two appear. So we define one rate of reaction by dividing each rate by its coefficient."):
            self.play(Write(eq))
            self.add(bars)
            self.play(FadeIn(names), FadeIn(bars))
            self.play(k.animate.set_value(1), run_time=2.0, rate_func=linear)
            self.play(FadeIn(rates))
            self.play(Write(rr))
        self.play(FadeOut(VGroup(eq, rr, names, rates)), FadeOut(bars))
        self.remove(bars)
        head, prob = C.example_head(self, "In 2N₂O₅ → 4NO₂ + O₂, [N₂O₅] falls from 0.50 to 0.40 mol L⁻¹ in 100 s. Find the rate of disappearance of N₂O₅, the rate of reaction, and the rates of formation of NO₂ and O₂.")
        st = C.steps(r"-\frac{\Delta[\mathrm{N_2O_5}]}{\Delta t} = \frac{0.50 - 0.40}{100} = 1.0\times10^{-3}\ \mathrm{mol\,L^{-1}s^{-1}}",
                     r"r = \tfrac{1}{2} \times 1.0\times10^{-3} = 5.0\times10^{-4}",
                     r"\frac{\Delta[\mathrm{NO_2}]}{\Delta t} = 4r = 2.0\times10^{-3},\qquad \frac{\Delta[\mathrm{O_2}]}{\Delta t} = r = 5.0\times10^{-4}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example three point one. N two O five falls by zero point one zero in a hundred seconds: one times ten to the minus three moles per litre per second. Divide by its coefficient two: the rate of reaction is five times ten to the minus four."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("Then N O two forms at four times that, two times ten to the minus three, and oxygen at one times, five times ten to the minus four. Check: N O two appears four times as fast as oxygen. It does."):
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st)))
        self.tip("For N₂ + 3H₂ → 2NH₃: −d[N₂]/dt = −⅓ d[H₂]/dt = +½ d[NH₃]/dt. Divide by the coefficient before you equate anything.",
                 "A very common slip. In the Haber reaction, hydrogen disappears three times as fast as nitrogen, and ammonia appears twice as fast. Always divide each rate by its coefficient before you set them equal.", state="oops")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        d = M(r"r = k[\mathrm{A}]^{x}[\mathrm{B}]^{y}", size=72).move_to(UP * 1.6)
        n = T("x and y are found by experiment", size=30, color=th.AMBER).next_to(d, DOWN, buff=0.4)
        with self.say("The rate law relates the rate to concentrations: r equals k times A to the x, times B to the y. Here is the crucial point. The powers x and y are found by experiment. They cannot be read off the balanced equation."):
            self.play(Write(d))
            self.play(FadeIn(n, shift=UP * 0.2))
        self.play(FadeOut(n), d.animate.scale(0.6).to_edge(UP, buff=0.7))
        rows = [["Reaction", "Equation suggests", "Observed rate law", "Order"],
                ["2N₂O₅ → 4NO₂ + O₂", "[N₂O₅]²", "k[N₂O₅]", "1"],
                ["H₂ + I₂ → 2HI", "[H₂][I₂]", "k[H₂][I₂]", "2"],
                ["2NO₂ + F₂ → 2NO₂F", "[NO₂]²[F₂]", "k[NO₂][F₂]", "2"],
                ["CHCl₃ + Cl₂ → CCl₄ + HCl", "[CHCl₃][Cl₂]", M(r"k[\mathrm{CHCl_3}][\mathrm{Cl_2}]^{1/2}", size=30, color=th.AMBER), "1.5"],
                ["2H₂O₂ → 2H₂O + O₂", "[H₂O₂]²", "k[H₂O₂]", "1"]]
        tb = C.table(rows, [4.6, 2.8, 3.4, 1.4], row_h=0.64, size=23, colors=[th.INK, th.MUTED, th.AMBER, th.MINT]).next_to(d, DOWN, buff=0.4)
        with self.say("Look how often the equation lies. Two N two O five should give a squared term, but the observed law is first order. Chloroform and chlorine give an order of one and a half. Only hydrogen and iodine happen to match. The reason is mechanism: the rate is set by the slowest step, and only species in that step appear in the rate law.") as v:
            nb = C.show_neby(self, "surprised", height=1.3, corner=DR)
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(tb, d)))
        title = T("The initial-rate method", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        rules = VGroup(*[VGroup(M(a, size=40), T(b, size=26, color=c)).arrange(RIGHT, buff=0.5) for a, b, c in [
            (r"[\mathrm{A}] \times 2 \Rightarrow r \times 2", "order 1   (2¹ = 2)", th.SKY),
            (r"[\mathrm{A}] \times 2 \Rightarrow r \times 4", "order 2   (2² = 4)", th.AMBER),
            (r"[\mathrm{A}] \times 2 \Rightarrow r \times 1", "order 0   (2⁰ = 1)", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.6)
        with self.say("To find the orders, run the reaction several times, changing one concentration at a time, and measure the initial rate. If doubling A doubles the rate, the order in A is one. If it quadruples the rate, two. If nothing changes, zero."):
            self.play(FadeIn(title))
            for r in rules:
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.play(FadeOut(VGroup(title, rules)))
        head, prob = C.example_head(self, "For A + 2B → C at 298 K, find the orders, the rate law and k.")
        rows = [["Exp.", "[A]", "[B]", "initial rate"], ["1", "0.10", "0.10", "2.0 × 10⁻³"], ["2", "0.20", "0.10", "4.0 × 10⁻³"], ["3", "0.10", "0.20", "8.0 × 10⁻³"]]
        tb = C.table(rows, [1.0, 1.3, 1.3, 2.3], row_h=0.6, size=24, colors=[th.MUTED, th.SKY, th.AMBER, th.INK]).next_to(prob, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        st = C.steps(r"1 \to 2:\ [\mathrm{A}]\times2,\ r\times2 \Rightarrow x = 1",
                     r"1 \to 3:\ [\mathrm{B}]\times2,\ r\times4 \Rightarrow y = 2",
                     r"r = k[\mathrm{A}][\mathrm{B}]^{2},\ \text{order } 3",
                     r"k = \frac{2.0\times10^{-3}}{(0.10)(0.10)^{2}} = 2.0\ \mathrm{L^2\,mol^{-2}\,s^{-1}}", size=32).next_to(tb, RIGHT, buff=0.4).align_to(tb, UP)
        with self.say("Worked example three point two. Three experiments. From one to two, A doubles while B is fixed, and the rate doubles. First order in A."):
            self.play(FadeIn(head), FadeIn(prob), FadeIn(tb))
            self.play(Indicate(VGroup(tb[1], tb[2]), color=th.SKY, scale_factor=1.02))
            self.play(Write(st[0]))
        with self.say("From one to three, B doubles and the rate goes up four times. Second order in B. So the rate law is k A B squared, third order overall."):
            self.play(Indicate(VGroup(tb[1], tb[3]), color=th.AMBER, scale_factor=1.02))
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        with self.say("Put experiment one in to find k: two times ten to the minus three, divided by zero point one times zero point one squared. k is two, in litres squared per mole squared per second."):
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, tb, st)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        d = self.callout("key", "Rate constant k: the rate when every reactant concentration is unity. Also called the specific reaction rate.", width=11, size=28).to_edge(UP, buff=0.8)
        with self.say("The rate constant k is the rate of the reaction when every concentration is one mole per litre. That is why it is also called the specific reaction rate."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        u = M(r"[k] = \frac{\mathrm{mol\,L^{-1}\,s^{-1}}}{(\mathrm{mol\,L^{-1}})^{n}} = (\mathrm{mol\,L^{-1}})^{1-n}\,\mathrm{s^{-1}}", size=44).to_edge(UP, buff=0.9)
        rows = [["Order n", "Units of k"], ["0", "mol L⁻¹ s⁻¹"], ["1", "s⁻¹"], ["2", "L mol⁻¹ s⁻¹"], ["3", "L² mol⁻² s⁻¹"]]
        tb = C.table(rows, [2.4, 4.2], row_h=0.62, size=28, colors=[th.AMBER, th.INK]).next_to(u, DOWN, buff=0.5)
        self.play(FadeOut(d))
        with self.say("Its units depend on the order. Rate divided by concentration to the n gives moles per litre to the power one minus n, per second. Zero order: moles per litre per second. First order: just per second. Second: litres per mole per second. Third: litres squared per mole squared per second.") as v:
            self.play(Write(u))
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 6 - 0.4)
        nb = C.show_neby(self, "wink", height=1.3)
        with self.say("A shortcut: count the power of mole in the unit, and subtract it from one. Litres per mole per second has mole to the minus one, so the order is one minus minus one, two. And a first order k has no concentration in it at all, so it can be quoted per second, per minute or per year."):
            self.play(Indicate(tb[3], color=th.AMBER, scale_factor=1.03))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(u, tb)))
        title = T("What k tells you", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        pts = VGroup(*[T(s, size=27, color=th.BODY) for s in [
            "1.  the intrinsic speed of a reaction, free of concentration",
            "2.  independent of concentration, but rises with temperature",
            "3.  larger k, faster reaction (for the same order)",
            "4.  its units reveal the overall order",
            "5.  fixed for a given reaction at a given temperature"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(title, DOWN, buff=0.5)
        with self.say("Why does k matter? It measures the intrinsic speed of a reaction, independent of how concentrated the solution happens to be. Reactions should be compared by their rate constants, never by their rates. It changes with temperature and with a catalyst, roughly doubling for every ten degree rise. And its units reveal the order.") as v:
            self.play(FadeIn(title))
            for p in pts:
                self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.45)
                self.hold(v.dur / 5 - 0.5)
        self.play(FadeOut(VGroup(title, pts)))
        head, prob = C.example_head(self, "k = 3.0 × 10⁻² L mol⁻¹ s⁻¹. (a) Order? (b) Rate law? (c) Rate at [A] = 0.20 mol L⁻¹? (d) Effect of trebling [A]?")
        st = C.steps(r"(a)\ \mathrm{mol^{-1}}:\ 1 - n = -1 \Rightarrow n = 2",
                     r"(b)\ r = k[\mathrm{A}]^{2}",
                     r"(c)\ r = 3.0\times10^{-2} \times (0.20)^{2} = 1.2\times10^{-3}\ \mathrm{mol\,L^{-1}s^{-1}}",
                     r"(d)\ r \times 3^{2} = 9 \times 1.2\times10^{-3} = 1.08\times10^{-2}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example three point three. The unit has mole to the minus one, so the reaction is second order, and the rate law is k A squared. At zero point two molar, the rate is three times ten to the minus two times zero point zero four: one point two times ten to the minus three."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        with self.say("Treble the concentration, and a second order rate goes up three squared, nine times: one point zero eight times ten to the minus two. The rate constant itself does not change at all."):
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        rows = [["", "Order", "Molecularity"],
                ["obtained", "by experiment, from the rate law", "in theory, by counting species in one step"],
                ["values", "0, 1, 2, 3, or fractional", "1, 2 or 3 only"],
                ["zero?", "yes", "never"],
                ["applies to", "overall reaction or a step", "an elementary step only"],
                ["conditions", "can change (pseudo-order)", "fixed"]]
        tb = C.table(rows, [2.4, 5.0, 5.4], row_h=0.66, size=24, colors=[th.MUTED, th.AMBER, th.SKY]).move_to(UP * 0.6)
        with self.say("Order and molecularity sound alike, but they are different ideas. Order is the sum of the powers in the experimental rate law. It can be zero, or even a fraction. Molecularity is the number of species colliding in a single elementary step: one, two or three, always a whole number, never zero.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 6 - 0.4)
        n = T("For an elementary (one-step) reaction, order = molecularity.", size=28, color=th.MINT).next_to(tb, DOWN, buff=0.5)
        with self.say("For an elementary reaction, one that happens in a single step, the two are equal. They differ for complex reactions with several steps."):
            self.play(FadeIn(n, shift=UP * 0.2))
        self.play(FadeOut(VGroup(tb, n)))
        # zero order: saturated surface
        title = T("Zero order: a saturated surface", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        surf = Rectangle(width=9, height=0.5, fill_color="#8C93A8", fill_opacity=1, stroke_width=0).move_to([0, -2.2, 0])
        sl = T("hot tungsten surface", size=22, color=th.BG, weight="BOLD").move_to(surf)
        sites = VGroup(*[Dot([-4.0 + 0.8 * i, -1.85, 0], radius=0.18, color=th.SKY) for i in range(11)])
        rng = np.random.default_rng(3)
        gas = VGroup(*[Dot([rng.uniform(-4.4, 4.4), rng.uniform(-1.2, 2.2), 0], radius=0.1, color=th.SKY, fill_opacity=0.6) for _ in range(30)])
        eq = chem(r"2NH_3 \xrightarrow{W} N_2 + 3H_2\qquad r = k", size=38).next_to(title, DOWN, buff=0.3)
        with self.say("Zero order. Ammonia decomposes on a hot tungsten wire. Every active spot on the metal surface is already covered by an ammonia molecule. Adding more ammonia gas does nothing: the queue just gets longer. The rate is simply k."):
            self.play(FadeIn(title), FadeIn(surf), FadeIn(sl), Write(eq))
            self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in sites], lag_ratio=0.05), FadeIn(gas))
            more = VGroup(*[Dot([rng.uniform(-4.4, 4.4), rng.uniform(-1.2, 2.2), 0], radius=0.1, color=th.SKY, fill_opacity=0.6) for _ in range(30)])
            self.play(FadeIn(more, shift=DOWN * 0.3))
            self.play(Indicate(sites, color=th.AMBER, scale_factor=1.15))
        hl = T("The light-driven H₂ + Cl₂ → 2HCl is zero order too: the light intensity sets the rate.", size=22, color=th.BODY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(hl))
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, surf, sl, sites, gas, more, eq, hl)))
        # pseudo first order
        title = T("Pseudo-first-order reactions", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        eq = chem(r"C_{12}H_{22}O_{11} + H_2O \xrightarrow{H^+} C_6H_{12}O_6 + C_6H_{12}O_6", size=36).next_to(title, DOWN, buff=0.3)
        waters = VGroup(*[Dot([rng.uniform(-6, 6), rng.uniform(-1.5, 1.3), 0], radius=0.05, color=C.WATER, fill_opacity=0.7) for _ in range(260)])
        sug = VGroup(*[Square(side_length=0.3, fill_color=th.AMBER, fill_opacity=1, stroke_width=0).move_to([rng.uniform(-5, 5), rng.uniform(-1.3, 1.1), 0]) for _ in range(6)])
        laws = VGroup(M(r"r = k'[\text{sucrose}][\mathrm{H_2O}]", size=38), M(r"[\mathrm{H_2O}] \approx \text{constant} \Rightarrow r = k[\text{sucrose}]", size=38, color=th.AMBER)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.say("Pseudo first order. When cane sugar is hydrolysed, one sugar molecule reacts with one water molecule. Truly, that is second order. But water is the solvent, a vast ocean of it. Using up a few molecules changes its concentration by almost nothing."):
            self.play(FadeIn(title), Write(eq))
            self.play(FadeIn(waters), FadeIn(sug))
            self.play(Write(laws[0]))
        with self.say("So the water term is absorbed into the constant, and the reaction behaves as first order. Second order in reality, first order in behaviour. The acid hydrolysis of an ester is the other standard example."):
            self.play(Write(laws[1]))
        self.play(FadeOut(VGroup(title, eq, waters, sug, laws)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("Zero order: integrate the rate law", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        z = VGroup(M(r"-\frac{d[\mathrm{A}]}{dt} = k \;\Rightarrow\; -\int_{[\mathrm{A}]_0}^{[\mathrm{A}]} d[\mathrm{A}] = k\int_0^t dt", size=38),
                   M(r"[\mathrm{A}]_0 - [\mathrm{A}] = kt", size=42),
                   M(r"[\mathrm{A}] = [\mathrm{A}]_0 - kt", size=52, color=th.MINT)).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.35).to_edge(LEFT, buff=0.7)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 1, 0.25], x_length=4.8, y_length=3.2, tips=False, axis_config={"color": th.MUTED}).move_to([3.8, -1.2, 0])
        zl = ax.plot(lambda t: max(0, 1 - 0.1 * t), x_range=[0, 10], color=th.MINT, stroke_width=4)
        lb = VGroup(T("[A]", size=20, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1), T("t", size=20, color=th.MUTED).next_to(ax.x_axis, RIGHT, buff=0.1))
        sl = T("straight line, slope −k", size=22, color=th.MINT).next_to(ax, UP, buff=0.2)
        with self.say("The rate law is a differential equation. Integrate it, and you get concentration as a function of time. For zero order, minus d A by d t equals k. Integrate from A nought at time zero to A at time t: A nought minus A equals k t."):
            self.play(FadeIn(title))
            self.play(Write(z[0]))
            self.play(Write(z[1]))
        with self.say("So A equals A nought minus k t. A plot of concentration against time is a straight line of slope minus k. The reactant is used at a steady rate, and is gone completely at time A nought over k."):
            self.play(Write(z[2]))
            self.play(Create(ax), FadeIn(lb), Create(zl), FadeIn(sl))
        self.play(FadeOut(VGroup(title, z, ax, zl, lb, sl)))
        title = T("First order: integrate the rate law", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        f = VGroup(M(r"-\frac{d[\mathrm{A}]}{dt} = k[\mathrm{A}] \;\Rightarrow\; -\int \frac{d[\mathrm{A}]}{[\mathrm{A}]} = k\int dt", size=38),
                   M(r"\ln\frac{[\mathrm{A}]_0}{[\mathrm{A}]} = kt", size=44),
                   M(r"k = \frac{2.303}{t}\log\frac{[\mathrm{A}]_0}{[\mathrm{A}]}", size=56, color=th.AMBER),
                   M(r"[\mathrm{A}] = [\mathrm{A}]_0\,e^{-kt}", size=42, color=th.SKY)).arrange(DOWN, buff=0.32).next_to(title, DOWN, buff=0.3)
        with self.say("First order. Minus d A by d t equals k A. Separate the variables: d A over A equals minus k d t. Integrating one over A gives a natural log. So ln of A nought over A equals k t."):
            self.play(FadeIn(title))
            self.play(Write(f[0]))
            self.play(Write(f[1]))
        with self.say("Convert to base ten logs, and you get the equation to know by heart: k equals two point three zero three over t, times log of A nought over A. Or, written the other way, A equals A nought e to the minus k t: exponential decay."):
            self.sfx("impact", gain=-12)
            self.play(Write(f[2]))
            self.play(Circumscribe(f[2], color=th.AMBER))
            self.play(Write(f[3]))
        self.play(FadeOut(VGroup(title, f[0], f[1], f[3])), f[2].animate.scale(0.7).to_corner(UR, buff=0.7))
        kk = ValueTracker(0.3)
        ax1 = Axes(x_range=[0, 10, 2], y_range=[0, 1, 0.25], x_length=5.2, y_length=3.6, tips=False, axis_config={"color": th.MUTED}).move_to([-3.4, -0.9, 0])
        ax2 = Axes(x_range=[0, 10, 2], y_range=[-6.2, 0, 1], x_length=5.2, y_length=3.6, tips=False, axis_config={"color": th.MUTED}).move_to([3.2, -0.9, 0])
        c1 = always_redraw(lambda: ax1.plot(lambda t: np.exp(-kk.get_value() * t), x_range=[0, 10], color=th.SKY, stroke_width=4))
        c2 = always_redraw(lambda: ax2.plot(lambda t: max(-6.2, -kk.get_value() * t), x_range=[0, 10], color=th.AMBER, stroke_width=4))
        l1 = VGroup(T("[A] against t: a curve", size=22, color=th.SKY).next_to(ax1, UP, buff=0.2), T("t", size=20, color=th.MUTED).next_to(ax1.x_axis, RIGHT, buff=0.1))
        l2 = VGroup(T("ln[A] against t: straight, slope −k", size=22, color=th.AMBER).next_to(ax2, UP, buff=0.2), T("t", size=20, color=th.MUTED).next_to(ax2.x_axis, RIGHT, buff=0.1))
        kl = DecimalNumber(0.3, num_decimal_places=2, font_size=34, color=th.INK)
        kl.add_updater(lambda m: m.set_value(kk.get_value()).move_to([0, 2.2, 0]))
        kt = M("k =", size=34).next_to([0, 2.2, 0], LEFT, buff=0.5)
        with self.say("Plot concentration against time and you get a curve that falls ever more slowly, and never quite reaches zero. But plot the log of concentration against time, and it is a straight line with slope minus k. That straight line is the test for first order. Change k, and only the steepness changes."):
            self.add(c1, c2, kl)
            self.play(Create(ax1), Create(ax2), FadeIn(l1), FadeIn(l2), FadeIn(c1), FadeIn(c2), FadeIn(kl), FadeIn(kt))
            self.play(kk.animate.set_value(0.6), run_time=1.6)
            self.play(kk.animate.set_value(0.15), run_time=1.6)
            self.play(kk.animate.set_value(0.3), run_time=1.0)
        kl.clear_updaters()
        self.play(FadeOut(VGroup(ax1, ax2, l1, l2, kl, kt, f[2])), FadeOut(c1), FadeOut(c2))
        self.remove(c1, c2)
        self.tip("Only the ratio [A]₀/[A] appears, so use anything proportional to the amount left: titre volume, gas pressure, optical rotation, mass of a radioactive sample.",
                 "A useful trick. The first order equation only needs the ratio of initial to remaining amount. So any quantity proportional to the amount left will do: a titration volume, a gas pressure, an angle of optical rotation. The units cancel.", state="cool")
        self.example_34()
        self.example_35()

    def example_34(self):
        head, prob = C.example_head(self, "A first-order reaction is 25 % complete in 40 min. Find (a) k, (b) the time for 75 % completion.")
        st = C.steps(r"[\mathrm{A}]_0 = 100,\ [\mathrm{A}] = 75:\ \ k = \frac{2.303}{40}\log\frac{100}{75} = 0.057575 \times 0.1249",
                     r"k = 7.19\times10^{-3}\ \mathrm{min^{-1}}",
                     r"t_{75\%} = \frac{2.303}{7.19\times10^{-3}}\log\frac{100}{25} = 320.3 \times 0.6021 = 193\ \mathrm{min}",
                     r"\text{check: } t_{1/2} = \frac{0.693}{k} = 96.4\ \mathrm{min},\ \ 2t_{1/2} = 193\ \checkmark", size=34).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[1].set_color(th.AMBER)
        st[3].set_color(th.MINT)
        with self.say("Worked example three point four. Twenty five percent complete in forty minutes. Take a hundred to start, so seventy five is left. k is two point three zero three over forty, times log of one hundred over seventy five. That is seven point one nine times ten to the minus three per minute."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            self.play(Write(st[1]))
        with self.say("For seventy five percent completion, twenty five is left. The time is two point three zero three over k, times log four: one hundred and ninety three minutes. And a check: seventy five percent done means one quarter left, which is two half lives. The half life is ninety six point four minutes. Twice that is one ninety three. It matches."):
            self.play(Write(st[2]))
            self.play(Write(st[3]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def example_35(self):
        head, prob = C.example_head(self, "NH₃ on hot tungsten is zero order, k = 2.0 × 10⁻² mol L⁻¹ s⁻¹, [A]₀ = 0.50 mol L⁻¹. Find [A] after 10 s, the half-life, and the time to finish.")
        st = C.steps(r"[\mathrm{A}] = 0.50 - (2.0\times10^{-2})(10) = 0.30\ \mathrm{mol\,L^{-1}}",
                     r"t_{1/2} = \frac{[\mathrm{A}]_0}{2k} = \frac{0.50}{0.040} = 12.5\ \mathrm{s}",
                     r"t_{\text{end}} = \frac{[\mathrm{A}]_0}{k} = \frac{0.50}{0.020} = 25\ \mathrm{s} = 2t_{1/2}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        with self.say("Worked example three point five, zero order. After ten seconds, A is zero point five minus zero point two, zero point three molar. The half life is A nought over two k, twelve point five seconds. And it finishes completely at A nought over k, twenty five seconds, exactly two half lives. A zero order reaction really does end. A first order one never quite does."):
            nb = C.show_neby(self, "think", height=1.3, corner=DR)
            self.play(FadeIn(head), FadeIn(prob))
            for s in st:
                self.play(Write(s))
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(head, prob, st)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        d = M(r"t_{1/2}:\ [\mathrm{A}] = \tfrac12[\mathrm{A}]_0", size=44).to_edge(UP, buff=0.8)
        z = VGroup(T("zero order", size=26, color=th.MINT, weight="BOLD"), M(r"\tfrac{[\mathrm{A}]_0}{2} = [\mathrm{A}]_0 - kt_{1/2} \Rightarrow t_{1/2} = \frac{[\mathrm{A}]_0}{2k}", size=36)).arrange(DOWN, buff=0.2)
        f = VGroup(T("first order", size=26, color=th.AMBER, weight="BOLD"), M(r"k = \frac{2.303}{t_{1/2}}\log 2 \Rightarrow t_{1/2} = \frac{0.693}{k}", size=36)).arrange(DOWN, buff=0.2)
        VGroup(z, f).arrange(RIGHT, buff=0.9).next_to(d, DOWN, buff=0.5)
        with self.say("The half life is the time for the concentration to fall to half its starting value. Put A equals half A nought into each equation. Zero order gives A nought over two k. First order gives point six nine three over k."):
            self.play(Write(d))
            self.play(FadeIn(z, shift=UP * 0.2))
            self.play(FadeIn(f, shift=UP * 0.2))
        k1 = T("depends on [A]₀", size=24, color=th.MINT).next_to(z, DOWN, buff=0.3)
        k2 = T("independent of [A]₀ !", size=24, color=th.AMBER, weight="BOLD").next_to(f, DOWN, buff=0.3)
        with self.say("Look closely. The zero order half life depends on how much you start with. The first order half life does not. That is the single most useful fact in this chapter."):
            self.play(FadeIn(k1), FadeIn(k2))
            self.play(Circumscribe(VGroup(f, k2), color=th.AMBER))
        self.play(FadeOut(VGroup(d, z, f, k1, k2)))
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.2, tips=False,
                  axis_config={"color": th.MUTED}).move_to([0.2, -0.4, 0])
        xl = T("time, in half-lives", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.4)
        xn = VGroup(*[T(str(i), size=20, color=th.MUTED).next_to(ax.c2p(i, 0), DOWN, buff=0.12) for i in range(6)])
        tt = ValueTracker(0)
        curve = always_redraw(lambda: ax.plot(lambda t: 0.5 ** t, x_range=[0, max(0.01, tt.get_value())], color=th.AMBER, stroke_width=4))
        fr = ["1", "1/2", "1/4", "1/8", "1/16", "1/32"]
        pc = ["0 %", "50 %", "75 %", "87.5 %", "93.75 %", "96.9 %"]
        marks = VGroup()
        for i in range(1, 6):
            p = ax.c2p(i, 0.5 ** i)
            marks.add(VGroup(DashedLine(ax.c2p(i, 0), p, color=th.FAINT, stroke_width=2), Dot(p, color=th.AMBER),
                             T(fr[i], size=22, color=th.INK, weight="BOLD").next_to(p, UR, buff=0.08), T(pc[i] + " done", size=16, color=th.MUTED).next_to(p, UR, buff=0.08).shift(UP * 0.3)))
        with self.say("For first order, every half life removes half of whatever is left. One half, then a quarter, an eighth, a sixteenth, a thirty second. After n half lives, one half to the power n remains.") as v:
            self.play(Create(ax), FadeIn(xl), FadeIn(xn))
            self.add(curve)
            for i in range(1, 6):
                self.play(tt.animate.set_value(i), run_time=0.7, rate_func=linear)
                self.sfx("tick", gain=-12)
                self.play(FadeIn(marks[i - 1]), run_time=0.3)
                self.hold(v.dur / 5 - 1.1)
        mem = M(r"t_{99\%} = 6.64\,t_{1/2},\qquad t_{99.9\%} \approx 10\,t_{1/2}", size=38, color=th.MINT).to_edge(UP, buff=0.75)
        with self.say("Two shortcuts worth memorising. Ninety nine percent completion takes six point six four half lives, and ninety nine point nine percent takes about ten."):
            self.play(Write(mem))
        self.play(FadeOut(VGroup(ax, xl, xn, marks, mem)), FadeOut(curve))
        self.remove(curve)
        head, prob = C.example_head(self, "The half-life of first-order N₂O₅ decomposition is 20 min. (a) What fraction remains after 1 hour? (b) If 4.0 g was taken, what mass decomposes in 1 hour? (c) Find k.")
        st = C.steps(r"60\ \mathrm{min} = 3\,t_{1/2} \Rightarrow \left(\tfrac12\right)^{3} = \tfrac18 = 12.5\,\%",
                     r"\text{left} = 4.0 \times \tfrac18 = 0.50\ \mathrm{g};\ \ \text{decomposed} = 3.5\ \mathrm{g}",
                     r"k = \frac{0.693}{20} = 3.47\times10^{-2}\ \mathrm{min^{-1}} = 5.78\times10^{-4}\ \mathrm{s^{-1}}", size=34).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        bars = VGroup(*[Rectangle(width=2.4 * 0.5 ** i, height=0.45, fill_color=th.AMBER, fill_opacity=0.85, stroke_width=0) for i in range(4)])
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45).to_edge(RIGHT, buff=0.6)
        bl = VGroup(*[T(s, size=18, color=th.MUTED).next_to(b, LEFT, buff=0.15) for s, b in zip(["4.0 g", "2.0 g", "1.0 g", "0.5 g"], bars)])
        with self.say("Worked example three point six. One hour is sixty over twenty, three half lives. So one eighth is left: twelve point five percent. Four grams halves to two, then one, then half a gram. So three point five grams has decomposed."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
            for b, l in zip(bars, bl):
                self.play(GrowFromEdge(b, LEFT), FadeIn(l), run_time=0.4)
            self.play(Write(st[1]))
        with self.say("And k is point six nine three over twenty: three point four seven times ten to the minus two per minute."):
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st, bars, bl)))
        self.quiz("For a first-order reaction, the half-life is",
                  ["proportional to [A]₀", "inversely proportional to [A]₀", "independent of [A]₀", "proportional to [A]₀²"], 2,
                  "Pause and think. How does the half life of a first order reaction depend on the starting concentration?",
                  "C, independent. t half equals point six nine three over k, with no concentration in it. Option A describes a zero order reaction.")

    # ------------------------------------------------------------------ part 8
    def p8(self):
        self.section(7)
        box = Rectangle(width=7.0, height=4.6, stroke_color=th.PANEL_EDGE, stroke_width=3).move_to([-2.6, -0.5, 0])
        rng = np.random.default_rng(21)
        n = 14
        pos = [np.array([rng.uniform(-3.2, 3.2), rng.uniform(-2.0, 2.0), 0]) for _ in range(n)]
        vel = [np.array([*rng.normal(0, 1.6, 2), 0]) for _ in range(n)]
        cols = [th.SKY if i % 2 == 0 else th.CORAL for i in range(n)]
        balls = VGroup(*[Dot(box.get_center() + p, radius=0.16, color=c) for p, c in zip(pos, cols)])
        flashes = VGroup()

        def step(g, dt):
            c0 = box.get_center()
            for i, b in enumerate(g):
                p = b.get_center() - c0 + vel[i] * dt
                for k, lim in ((0, 3.3), (1, 2.1)):
                    if abs(p[k]) > lim:
                        vel[i][k] *= -1
                        p[k] = np.sign(p[k]) * lim
                b.move_to(c0 + p)
            for i in range(n):
                for j in range(i + 1, n):
                    d = g[i].get_center() - g[j].get_center()
                    if np.linalg.norm(d) < 0.32:
                        u = d / (np.linalg.norm(d) + 1e-9)
                        vi, vj = np.dot(vel[i], u), np.dot(vel[j], u)
                        if vi - vj < 0:
                            vel[i] += (vj - vi) * u
                            vel[j] += (vi - vj) * u
        balls.add_updater(step)
        pts = VGroup(*[T(s, size=24, color=c) for s, c in [("1. Molecules must collide.", th.INK), ("2. With at least the minimum energy, Ea.", th.AMBER), ("3. And with the right orientation.", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.95, 0.4, 0])
        with self.say("Collision theory pictures a reaction as the result of collisions. First, molecules must collide. In a gas at room temperature there are about ten to the thirty collisions per litre every second. If every one worked, every gas reaction would be over in a microsecond."):
            self.play(Create(box))
            self.add(balls)
            self.play(FadeIn(balls), FadeIn(pts[0]))
            self.wait(2.0)
        with self.say("So only a tiny fraction of collisions are effective. The molecules must carry at least a certain minimum energy, the activation energy. And they must meet with the correct orientation, the right atoms facing each other."):
            self.play(FadeIn(pts[1]))
            self.play(FadeIn(pts[2]))
            self.wait(1.5)
        eq = M(r"r = Z \times P \times e^{-E_a/RT}", size=44, color=th.AMBER).next_to(pts, DOWN, buff=0.5)
        with self.say("So the rate is the collision frequency Z, times the steric factor P for orientation, times e to the minus E a over R T, the fraction of collisions with enough energy."):
            self.play(Write(eq))
            self.wait(1.0)
        balls.clear_updaters()
        self.play(FadeOut(VGroup(box, balls, pts, eq)))
        # energy profile
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 4.2, 1], x_length=8.0, y_length=4.8, tips=True,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-1.6, -0.5, 0])
        xl = T("reaction coordinate", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = T("energy", size=22, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1)
        f = profile(ax, r=1.4, ts=3.5, p=0.6)
        curve = ax.plot(f, x_range=[0, 10, 0.05], color=th.INK, stroke_width=4)
        s = ValueTracker(0.3)
        ball = always_redraw(lambda: Dot(ax.c2p(s.get_value(), f(s.get_value())) + UP * 0.17, radius=0.17, color=th.AMBER))
        r_lab = T("reactants", size=22, color=th.SKY).next_to(ax.c2p(1.0, 1.4), UP, buff=0.35)
        p_lab = T("products", size=22, color=th.MINT).next_to(ax.c2p(9.2, 0.6), DOWN, buff=0.2)
        with self.say("Now the energy picture. As reactants turn into products, the energy does not go straight down. It first climbs a hill. The top of that hill is the activated complex, or transition state: old bonds half broken, new bonds half formed. It cannot be isolated."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), FadeIn(r_lab), FadeIn(p_lab))
            self.add(ball)
            self.play(s.animate.set_value(3.5), run_time=1.5)
            self.play(s.animate.set_value(0.6), run_time=1.0)
            self.play(s.animate.set_value(5.0), run_time=1.2)
        ea = DoubleArrow(ax.c2p(2.0, 1.4), ax.c2p(2.0, 3.5), buff=0, color=th.AMBER, stroke_width=4, tip_length=0.2)
        eal = M("E_a", size=36, color=th.AMBER).next_to(ea, LEFT, buff=0.1)
        dh = DoubleArrow(ax.c2p(8.0, 1.4), ax.c2p(8.0, 0.6), buff=0, color=th.CORAL, stroke_width=4, tip_length=0.15)
        dhl = M(r"\Delta H", size=32, color=th.CORAL).next_to(dh, RIGHT, buff=0.1)
        lv = DashedLine(ax.c2p(0, 1.4), ax.c2p(8.2, 1.4), color=th.FAINT)
        top = DashedLine(ax.c2p(1.5, 3.5), ax.c2p(5.2, 3.5), color=th.FAINT)
        ac = T("activated complex ‡", size=22, color=th.INK).next_to(ax.c2p(5, 3.5), UP, buff=0.35)
        key = VGroup(M(r"E_{\text{threshold}} = E_{\text{reactants}} + E_a", size=34), T("small Ea: fast  ·  large Ea: slow", size=24, color=th.AMBER)).arrange(DOWN, buff=0.25).move_to([4.6, 2.3, 0])
        with self.say("The height of the hill above the reactants is the activation energy, E a: the extra energy a collision must bring. The absolute height it must reach is the threshold energy. A small activation energy means a fast reaction. A large one means a slow one. The difference between reactants and products is delta H, which has nothing to do with the hill."):
            self.play(Create(lv), Create(top), FadeIn(ac))
            self.play(GrowFromCenter(ea), FadeIn(eal))
            self.play(GrowFromCenter(dh), FadeIn(dhl))
            self.play(FadeIn(key))
        nb = C.show_neby(self, "success", height=1.4, corner=DR)
        dia = T("diamond → graphite: Ea is huge", size=24, color="#BFE9FF", weight="BOLD").move_to([4.3, 0.6, 0])
        with self.say("And that is the answer to our cold open. Diamond turning into graphite is downhill overall, but the hill in between is enormous, because every carbon carbon bond in the diamond's network must be broken. At room temperature, almost no atoms ever get over it. Your diamond is safe for billions of years."):
            self.play(FadeIn(dia, shift=UP * 0.2))
            self.play(s.animate.set_value(2.6), run_time=1.0)
            self.play(s.animate.set_value(0.4), run_time=1.0)
        C.hide_neby(self, nb)
        self.play(FadeOut(VGroup(ax, xl, yl, curve, r_lab, p_lab, ea, eal, dh, dhl, lv, top, ac, key, dia)), FadeOut(ball))
        self.remove(ball)
        hi = chem(r"H_2 + I_2 \rightarrow [H\cdots H\cdots I\cdots I]^{\ddagger} \rightarrow 2HI", size=40).to_edge(UP, buff=0.9)
        hpos = [np.array([-1.0, 0.6, 0]), np.array([-1.0, -0.6, 0])]
        ipos = [np.array([1.0, 0.6, 0]), np.array([1.0, -0.6, 0])]
        H = VGroup(*[C.atom("H", r=0.28).move_to(p + LEFT * 2.5) for p in hpos])
        I = VGroup(*[C.atom("I", r=0.45).move_to(p + RIGHT * 2.5) for p in ipos])
        with self.say("For hydrogen and iodine, the activated complex is a square of four atoms. The H H bond and the I I bond stretch, while two new H I bonds start to form. Then it falls apart into two molecules of hydrogen iodide."):
            self.play(Write(hi))
            self.play(FadeIn(H), FadeIn(I))
            self.play(H.animate.shift(RIGHT * 2.1), I.animate.shift(LEFT * 2.1), run_time=1.2)
            sq = VGroup(DashedLine(H[0].get_center(), H[1].get_center(), color=th.FAINT), DashedLine(I[0].get_center(), I[1].get_center(), color=th.FAINT),
                        DashedLine(H[0].get_center(), I[0].get_center(), color=th.AMBER), DashedLine(H[1].get_center(), I[1].get_center(), color=th.AMBER))
            self.play(Create(sq))
            self.play(FadeOut(sq), VGroup(H[0], I[0]).animate.shift(UP * 1.0), VGroup(H[1], I[1]).animate.shift(DOWN * 1.0), run_time=1.2)
            bonds = VGroup(Line(H[0].get_center(), I[0].get_center(), color=th.MUTED, stroke_width=6), Line(H[1].get_center(), I[1].get_center(), color=th.MUTED, stroke_width=6))
            self.play(Create(bonds))
        self.play(FadeOut(VGroup(hi, H, I, bonds)))

    # ------------------------------------------------------------------ part 9
    def p9(self):
        self.section(8)
        title = T("Nature and surface area", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        lump = Square(side_length=1.4, fill_color="#E9E4D8", fill_opacity=1, stroke_width=0).move_to([-3.4, -0.6, 0])
        rng = np.random.default_rng(31)
        powder = VGroup(*[Square(side_length=0.18, fill_color="#E9E4D8", fill_opacity=1, stroke_width=0).move_to([3.4 + rng.uniform(-1.2, 1.2), -0.6 + rng.uniform(-0.7, 0.7), 0]) for _ in range(49)])
        l1 = T("marble chip", size=24, color=th.BODY).next_to(lump, DOWN, buff=0.9)
        l2 = T("same mass, powdered", size=24, color=th.BODY).next_to(powder, DOWN, buff=0.5).set_y(l1.get_y())
        bub1 = VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=2).move_to(lump.get_top() + RIGHT * rng.uniform(-0.6, 0.6)) for _ in range(4)])
        bub2 = VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=2).move_to([3.4 + rng.uniform(-1.2, 1.2), 0.1, 0]) for _ in range(30)])
        with self.say("What changes the rate? First, the nature of the reactants. Ionic reactions are instant because no covalent bond must break. And surface area. A marble chip in dilute hydrochloric acid fizzes slowly. The same mass, powdered, fizzes furiously, because far more surface is exposed. That is why limestone is crushed before it goes into a lime kiln."):
            self.play(FadeIn(title), FadeIn(lump), FadeIn(powder), FadeIn(l1), FadeIn(l2))
            self.play(bub1.animate.shift(UP * 1.6).set_opacity(0), bub2.animate.shift(UP * 1.6).set_opacity(0), run_time=2.0)
        self.play(FadeOut(VGroup(title, lump, powder, l1, l2, bub1, bub2)))
        cc = VGroup(T("Concentration (and pressure)", size=34, color=th.INK, weight="BOLD", display=True),
                    para("More molecules per litre means more collisions per second. How much faster depends on the order: for r = k[A]², doubling [A] quadruples the rate; for zero order, nothing changes. For gases, raising the pressure raises the concentration.", width=11, size=28, color=th.BODY)).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        with self.say("Second, concentration. More molecules per litre means more collisions per second. How much faster depends on the order: double the concentration in a second order reaction, and the rate goes up four times. For gases, higher pressure does the same job."):
            self.play(FadeIn(cc, shift=UP * 0.2))
        self.play(FadeOut(cc))
        self.temperature()
        self.arrhenius()
        self.example_37()
        self.example_38()
        self.catalyst_profile()

    def temperature(self):
        title = T("Temperature: why 10 K doubles the rate", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 0.6, 0.1], x_length=9.0, y_length=4.4, tips=False,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-0.6, -0.6, 0])
        xl = T("kinetic energy of molecules", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.25)
        yl = T("fraction of molecules", size=22, color=th.MUTED).next_to(ax.y_axis, UP, buff=0.1)
        kT = ValueTracker(1.0)
        Ea = 4.0
        c1 = ax.plot(lambda E: mb(E, 1.0), x_range=[0, 10, 0.05], color=th.SKY, stroke_width=4)
        c2 = always_redraw(lambda: ax.plot(lambda E: mb(E, kT.get_value()), x_range=[0, 10, 0.05], color=th.CORAL, stroke_width=4))
        tail1 = ax.get_area(c1, x_range=[Ea, 10], color=th.SKY, opacity=0.5)
        tail2 = always_redraw(lambda: ax.get_area(ax.plot(lambda E: mb(E, kT.get_value()), x_range=[Ea, 10, 0.05]), x_range=[Ea, 10], color=th.CORAL, opacity=0.45))
        eline = DashedLine(ax.c2p(Ea, 0), ax.c2p(Ea, 0.55), color=th.AMBER, stroke_width=3)
        el = M("E_a", size=34, color=th.AMBER).next_to(eline, UP, buff=0.05)
        l1 = T("T", size=26, color=th.SKY, weight="BOLD").move_to(ax.c2p(1.2, 0.5))
        l2 = T("T + 10 K", size=26, color=th.CORAL, weight="BOLD").move_to(ax.c2p(3.2, 0.42))
        with self.say("Third, temperature. A ten degree rise near room temperature usually doubles or even trebles the rate. Why so much? It is not the extra collisions. Collision frequency rises only with the square root of T, under two percent for ten degrees."):
            self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl))
        with self.say("The secret is in this curve, the Maxwell Boltzmann distribution of molecular energies. Only molecules in the tail beyond E a can react. That shaded tail is tiny."):
            self.play(Create(c1), FadeIn(l1))
            self.play(Create(eline), FadeIn(el))
            self.play(FadeIn(tail1))
        with self.say("Raise the temperature. The curve flattens and spreads to the right. The peak hardly moves, but the tail beyond E a grows dramatically, roughly doubling. Twice as many molecules can climb the hill, so the rate doubles."):
            nb = C.show_neby(self, "surprised", height=1.3, corner=DR)
            self.add(c2, tail2)
            self.play(FadeIn(c2), FadeIn(tail2), FadeIn(l2))
            self.play(kT.animate.set_value(1.25), run_time=3.0)
        C.hide_neby(self, nb)
        tc = M(r"\text{temperature coefficient} = \frac{k_{T+10}}{k_T} \approx 2 \text{ to } 3", size=34, color=th.AMBER).to_edge(DOWN, buff=0.45)
        self.play(Write(tc))
        self.wait(0.5)
        self.play(FadeOut(VGroup(title, ax, xl, yl, c1, tail1, eline, el, l1, l2, tc)), FadeOut(c2), FadeOut(tail2))
        self.remove(c2, tail2)

    def arrhenius(self):
        title = T("The Arrhenius equation", size=36, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        e1 = M(r"k", r"=", r"A", r"\,e^{-E_a/RT}", size=72).next_to(title, DOWN, buff=0.4)
        e1[2].set_color(th.SKY)
        e1[3].set_color(th.AMBER)
        notes = VGroup(T("A: frequency factor (units of k)", size=24, color=th.SKY), T("e^(−Ea/RT): fraction energetic enough", size=24, color=th.AMBER),
                       T("R = 8.314 J K⁻¹ mol⁻¹, T in kelvin", size=24, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(e1, DOWN, buff=0.35)
        with self.say("Arrhenius put this into one equation in eighteen eighty nine. k equals A, the frequency factor, times e to the minus E a over R T, the fraction of collisions energetic enough."):
            self.play(FadeIn(title), Write(e1))
            self.play(FadeIn(notes))
        ln = M(r"\ln k = \ln A - \frac{E_a}{R}\cdot\frac{1}{T}", size=44).next_to(notes, DOWN, buff=0.4)
        with self.say("Take logs: ln k equals ln A minus E a over R, times one over T. That is a straight line. Plot ln k against one over T, and the slope gives you minus E a over R. That is how activation energies are measured."):
            self.play(Write(ln))
        self.play(FadeOut(VGroup(e1, notes)), ln.animate.next_to(title, DOWN, buff=0.4))
        two = VGroup(M(r"\log k_2 - \log k_1 = -\frac{E_a}{2.303R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)", size=38),
                     M(r"\log\frac{k_2}{k_1} = \frac{E_a}{2.303\,R}\left(\frac{T_2 - T_1}{T_1T_2}\right)", size=50, color=th.AMBER)).arrange(DOWN, buff=0.45).next_to(ln, DOWN, buff=0.5)
        with self.say("Write it at two temperatures and subtract. A cancels, and you get the form you must know by heart: log k two over k one equals E a over two point three zero three R, times T two minus T one, over T one T two."):
            self.play(Write(two[0]))
            self.sfx("impact", gain=-12)
            self.play(Write(two[1]))
            self.play(Circumscribe(two[1], color=th.AMBER))
        self.play(FadeOut(VGroup(title, ln, two)))

    def example_37(self):
        head, prob = C.example_head(self, "A rate constant doubles from 300 K to 310 K. Find the activation energy. (R = 8.314 J K⁻¹ mol⁻¹, log 2 = 0.3010)")
        st = C.steps(r"0.3010 = \frac{E_a}{2.303 \times 8.314}\times\frac{10}{300 \times 310} = \frac{E_a \times 10}{19.147 \times 93000}",
                     r"E_a = \frac{0.3010 \times 19.147 \times 93000}{10} = 53\,604\ \mathrm{J\,mol^{-1}}",
                     r"E_a \approx 53.6\ \mathrm{kJ\,mol^{-1}}", size=38).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example three point seven. The rate constant doubles between three hundred and three hundred and ten kelvin. So log two, zero point three zero one, equals E a over two point three zero three times eight point three one four, times ten over three hundred times three ten."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("Rearrange: E a is about fifty three thousand six hundred joules per mole, fifty three point six kilojoules. Remember this: an activation energy of about fifty kilojoules is what makes a rate double for every ten degrees near room temperature."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def example_38(self):
        head, prob = C.example_head(self, "k = 2.0 × 10⁻⁵ s⁻¹ at 300 K and 8.0 × 10⁻⁵ s⁻¹ at 320 K. Find Ea and the frequency factor A. (log 4 = 0.6021)")
        st = C.steps(r"0.6021 = \frac{E_a \times 20}{19.147 \times 96000} \Rightarrow E_a = 55\,336\ \mathrm{J\,mol^{-1}} \approx 55.3\ \mathrm{kJ\,mol^{-1}}",
                     r"\log A = \log k + \frac{E_a}{2.303RT} = -4.699 + \frac{55\,336}{5744}",
                     r"\log A = -4.699 + 9.633 = 4.934 \Rightarrow A = 8.6\times10^{4}\ \mathrm{s^{-1}}", size=36).next_to(prob, DOWN, buff=0.45).align_to(prob, LEFT)
        st[2].set_color(th.AMBER)
        with self.say("Worked example three point eight. The rate constant quadruples from three hundred to three hundred and twenty kelvin. The same equation with log four gives E a about fifty five point three kilojoules per mole."):
            self.play(FadeIn(head), FadeIn(prob))
            self.play(Write(st[0]))
        with self.say("For A, use log k equals log A minus E a over two point three zero three R T at three hundred kelvin. Log A is minus four point six nine nine plus nine point six three three, which is four point nine three four. So A is eight point six times ten to the four per second, with the same units as k."):
            self.play(Write(st[1]))
            self.play(Write(st[2]))
        self.play(FadeOut(VGroup(head, prob, st)))

    def catalyst_profile(self):
        title = T("Catalyst: a lower path", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 4.2, 1], x_length=7.0, y_length=4.6, tips=True,
                  axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-2.9, -0.6, 0])
        xl = T("reaction coordinate", size=22, color=th.MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
        f1 = profile(ax, r=1.4, ts=3.6, p=0.6)
        f2 = profile(ax, r=1.4, ts=2.3, p=0.6)
        c1 = ax.plot(f1, x_range=[0, 10, 0.05], color=th.INK, stroke_width=4)
        c2 = ax.plot(f2, x_range=[0, 10, 0.05], color=th.MINT, stroke_width=4)
        l1 = T("uncatalysed", size=22, color=th.INK).next_to(ax.c2p(5, 3.6), UP, buff=0.1)
        l2 = T("catalysed", size=22, color=th.MINT).next_to(ax.c2p(5, 2.35), DOWN, buff=0.15)
        ea1 = DoubleArrow(ax.c2p(2.2, 1.4), ax.c2p(2.2, 3.6), buff=0, color=th.INK, stroke_width=3, tip_length=0.15)
        ea2 = DoubleArrow(ax.c2p(3.0, 1.4), ax.c2p(3.0, 2.3), buff=0, color=th.MINT, stroke_width=3, tip_length=0.15)
        lv = DashedLine(ax.c2p(0, 1.4), ax.c2p(3.2, 1.4), color=th.FAINT)
        t1 = DashedLine(ax.c2p(2.0, 3.6), ax.c2p(5, 3.6), color=th.FAINT)
        t2 = DashedLine(ax.c2p(2.8, 2.3), ax.c2p(5, 2.3), color=th.FAINT)
        rules = VGroup(T("lowers Ea forwards and backwards equally", size=22, color=th.BODY), T("so the equilibrium position does not change", size=22, color=th.BODY),
                       T("ΔH is unchanged", size=22, color=th.BODY), T("cannot make an impossible reaction go", size=22, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.75, 0.6, 0])
        with self.say("Fourth, a catalyst. It changes the rate without being used up, by opening an alternative path with a lower activation energy. Usually it forms an unstable intermediate with a reactant, which then breaks down to give the product and returns the catalyst."):
            self.play(FadeIn(title), Create(ax), FadeIn(xl))
            self.play(Create(c1), FadeIn(l1), Create(lv), Create(t1), GrowFromCenter(ea1))
            self.play(TransformFromCopy(c1, c2), FadeIn(l2), Create(t2), GrowFromCenter(ea2))
        with self.say("Three things the board always asks. It lowers the barrier by the same amount in both directions, so forward and backward reactions speed up equally, and the position of equilibrium does not change. Only the time to reach it does. Delta H is unchanged, because the start and finish levels are the same. And a catalyst cannot make an impossible reaction happen."):
            for r in rules:
                self.play(FadeIn(r, shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(VGroup(rules[0], rules[1]), color=th.AMBER, scale_factor=1.03))
        other = T("Also: light intensity (H₂ + Cl₂, photosynthesis) and the solvent.", size=24, color=th.MUTED).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(other))
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, ax, xl, c1, c2, l1, l2, ea1, ea2, lv, t1, t2, rules, other)))

    # ------------------------------------------------------------------ part 10
    def p10(self):
        self.section(9)
        defs = VGroup(T("positive catalyst: speeds a reaction up", size=26, color=th.MINT),
                      T("negative catalyst (inhibitor): slows it, e.g. glycerol on H₂O₂", size=26, color=th.CORAL),
                      T("promoter: boosts a catalyst, e.g. Mo with Fe in the Haber process", size=26, color=th.AMBER),
                      T("poison: kills a catalyst, e.g. As₂O₃ on V₂O₅ in the contact process", size=26, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.3)
        with self.say("Catalysis is the change of rate caused by a catalyst. A positive catalyst speeds a reaction up. A negative catalyst, or inhibitor, slows it down, as glycerol does for hydrogen peroxide. A promoter has no power of its own but boosts a catalyst, like molybdenum with iron. And a poison destroys a catalyst, like arsenic oxide on vanadium pentoxide.") as v:
            for d in defs:
                self.play(FadeIn(d, shift=RIGHT * 0.2), run_time=0.5)
                self.hold(v.dur / 4 - 0.6)
        self.play(FadeOut(defs))
        title = T("Homogeneous: same phase", size=34, color=th.SKY, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        c = np.array([0, -0.5, 0])
        nodes = [c + np.array([-2.6, 0.9, 0]), c + np.array([2.6, 0.9, 0]), c + np.array([0, -1.6, 0])]
        labs = VGroup(chem("2NO", size=40, color=th.SKY).move_to(nodes[0]), chem(r"2NO_2", size=40, color=th.AMBER).move_to(nodes[1]))
        a1 = CurvedArrow(nodes[0] + RIGHT * 0.7 + UP * 0.2, nodes[1] + LEFT * 0.8 + UP * 0.2, angle=-TAU / 6, color=th.MUTED)
        a2 = CurvedArrow(nodes[1] + LEFT * 0.4 + DOWN * 0.4, nodes[0] + RIGHT * 0.4 + DOWN * 0.4, angle=-TAU / 4, color=th.MUTED)
        t1 = chem(r"+\,O_2", size=32, color=C.EL["O"]).next_to(a1, UP, buff=0.1)
        t2 = chem(r"+\,2SO_2 \rightarrow 2SO_3", size=32, color=C.EL["S"]).next_to(a2, DOWN, buff=0.1)
        net = chem(r"\text{net: } 2SO_2 + O_2 \xrightarrow{NO} 2SO_3", size=36, color=th.INK).to_edge(DOWN, buff=0.5)
        with self.say("In homogeneous catalysis, catalyst and reactants are in the same phase. In the lead chamber process, nitric oxide gas takes up oxygen to become nitrogen dioxide, which hands the oxygen to sulphur dioxide and turns back into nitric oxide. It goes round and round, and never appears in the overall equation. Acid catalysed ester and sugar hydrolysis are homogeneous too."):
            self.play(FadeIn(title), FadeIn(labs[0]))
            self.play(Create(a1), FadeIn(t1), FadeIn(labs[1]))
            self.play(Create(a2), FadeIn(t2))
            self.play(Write(net))
        self.play(FadeOut(VGroup(title, labs, a1, a2, t1, t2, net)))
        title = T("Heterogeneous: a surface does the work", size=34, color=th.AMBER, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        surf = Rectangle(width=10, height=0.5, fill_color="#8C93A8", fill_opacity=1, stroke_width=0).move_to([0, -2.4, 0])
        sl = T("Ni surface", size=22, color=th.BG, weight="BOLD").move_to(surf)
        h2 = VGroup(*[VGroup(C.atom("H", r=0.18), C.atom("H", r=0.18).shift(RIGHT * 0.34)).move_to([-3 + 2.0 * k, 1.6, 0]) for k in range(3)])
        oil = VGroup(*[VGroup(Line(LEFT * 0.6, RIGHT * 0.6, color=th.AMBER, stroke_width=8), Line(LEFT * 0.15 + UP * 0.08, RIGHT * 0.15 + UP * 0.08, color=th.AMBER, stroke_width=8)).move_to([-2 + 2.0 * k, 0.6, 0]) for k in range(2)])
        steps = T("adsorb  →  bonds weaken  →  react  →  desorb", size=26, color=th.INK).next_to(title, DOWN, buff=0.3)
        with self.say("In heterogeneous catalysis the catalyst is in a different phase, usually a solid surface. Making vanaspati ghee: hydrogen and vegetable oil are adsorbed on nickel. Adsorption weakens the hydrogen bond and holds the molecules in the right orientation. They react, and the solid fat desorbs, freeing the surface."):
            self.play(FadeIn(title), FadeIn(surf), FadeIn(sl), FadeIn(steps))
            self.play(FadeIn(h2), FadeIn(oil))
            self.play(*[h.animate.move_to([-3 + 2.0 * k, -1.95, 0]).set_opacity(0.9) for k, h in enumerate(h2)], *[o.animate.move_to([-2 + 2.0 * k, -1.95, 0]) for k, o in enumerate(oil)], run_time=1.5)
            self.play(*[h[1].animate.shift(RIGHT * 0.3) for h in h2], run_time=0.6)
            self.play(VGroup(h2, oil).animate.shift(UP * 2.2).set_opacity(0.4), run_time=1.2)
        rows = [["Reaction", "Catalyst", "Process"], ["N₂ + 3H₂ ⇌ 2NH₃", "Fe + Mo promoter", "Haber"], ["2SO₂ + O₂ ⇌ 2SO₃", "V₂O₅", "contact"],
                ["4NH₃ + 5O₂ → 4NO + 6H₂O", "Pt gauze", "Ostwald"], ["oil + H₂ → vanaspati", "Ni", "hydrogenation"]]
        self.play(FadeOut(VGroup(surf, sl, h2, oil, steps)))
        tb = C.table(rows, [4.8, 3.4, 2.8], row_h=0.62, size=24, colors=[th.INK, th.AMBER, th.MUTED]).move_to(DOWN * 0.3)
        with self.say("The big industrial processes are all heterogeneous. Iron with a molybdenum promoter for ammonia. Vanadium pentoxide for sulphuric acid. Platinum gauze for nitric acid. And nickel for ghee.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.4)
                self.hold(v.dur / 5 - 0.4)
        self.play(FadeOut(VGroup(title, tb)))
        self.enzyme()
        self.quiz("A catalyst increases the rate of a reversible reaction because it",
                  ["raises ΔH", "shifts the equilibrium right", "lowers Ea of both directions", "raises the temperature"], 2,
                  "Pause and think. How exactly does a catalyst speed up a reversible reaction?",
                  "C. It provides a path of lower activation energy, lowering the barrier equally for the forward and backward reactions. So it does not change delta H, and it does not shift the equilibrium. It only gets there sooner.")

    def enzyme(self):
        title = T("Enzymes: lock and key", size=34, color=th.MINT, weight="BOLD", display=True).to_edge(UP, buff=0.7)
        body = Polygon([-2.4, -2.2, 0], [2.4, -2.2, 0], [2.4, -0.2, 0], [0.6, -0.2, 0], [0.6, -0.9, 0], [-0.6, -0.9, 0], [-0.6, -0.2, 0], [-2.4, -0.2, 0],
                       fill_color=th.MINT, fill_opacity=0.5, stroke_color=th.MINT, stroke_width=3).move_to([-3.5, -1.0, 0])
        el = T("enzyme", size=24, color=th.MINT).next_to(body, DOWN, buff=0.2)
        sub = Rectangle(width=1.15, height=1.4, fill_color=th.AMBER, fill_opacity=0.9, stroke_width=0).move_to([-3.5, 2.0, 0])
        wrong = Circle(radius=0.65, fill_color=th.CORAL, fill_opacity=0.9, stroke_width=0).move_to([-1.6, 2.0, 0])
        sl = T("substrate", size=22, color=th.AMBER).next_to(sub, LEFT, buff=0.2)
        with self.say("Enzymes are protein biocatalysts made by living cells. Each has an active site, a pocket of a definite shape. Only a substrate of the matching shape fits, like a key in a lock. A wrong shape simply does not fit."):
            self.play(FadeIn(title), FadeIn(body), FadeIn(el))
            self.play(FadeIn(sub), FadeIn(sl), FadeIn(wrong))
            self.play(wrong.animate.move_to(body.get_center() + UP * 0.6), run_time=0.8)
            self.play(wrong.animate.shift(UP * 0.6 + LEFT * 1.5).set_opacity(0.3), run_time=0.6)
            self.play(sub.animate.move_to(body.get_center() + UP * 0.25), FadeOut(sl), run_time=1.0)
            self.sfx("click", gain=-8)
            halves = VGroup(sub.copy().stretch(0.5, 0).set_fill(th.SKY), sub.copy().stretch(0.5, 0).set_fill(th.PINK))
            halves[0].move_to(sub.get_center() + LEFT * 0.3)
            halves[1].move_to(sub.get_center() + RIGHT * 0.3)
            self.remove(sub)
            self.add(halves)
            self.play(halves[0].animate.shift(UP * 2.4 + LEFT * 1.2), halves[1].animate.shift(UP * 2.4 + RIGHT * 1.2), run_time=1.0)
        rows = [["Enzyme", "Reaction", "Source"], ["invertase", "sucrose → glucose + fructose", "yeast"], ["zymase", "glucose → ethanol + CO₂", "yeast"],
                ["diastase", "starch → maltose", "malt"], ["urease", "urea → NH₃ + CO₂", "soyabean"], ["pepsin", "proteins → peptides", "gastric juice"]]
        tb = C.table(rows, [2.2, 4.6, 2.2], row_h=0.56, size=22, colors=[th.MINT, th.INK, th.MUTED])
        tb.scale_to_fit_width(7.2).move_to([3.15, -0.4, 0])
        with self.say("Enzymes are astonishingly efficient, and astonishingly specific: urease attacks urea and nothing else. They work only in a narrow range of temperature, around body temperature, and of p H, because heat denatures the protein. Yeast enzymes ferment rice for jaand and raksi, and Lactobacillus turns milk into dahi.") as v:
            for r in tb:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=0.35)
                self.hold(v.dur / 6 - 0.4)
        self.play(FadeOut(VGroup(title, body, el, wrong, halves, tb)))
        care = self.callout("remember", "Autocatalysis: a product catalyses its own reaction. In the KMnO₄–oxalic acid titration, the Mn²⁺ formed speeds up the reaction, so the first drops decolourise slowly and the rest instantly.", width=11, size=27)
        nb = C.show_neby(self, "surprised", height=1.3)
        with self.say("Remember the permanganate titration from Unit 1? The first drops lose their colour slowly, the rest almost instantly. The manganese two plus ions produced catalyse the reaction itself. That is autocatalysis, and it is why we warm the flask to get started."):
            self.play(FadeIn(care, shift=UP * 0.3))
        C.hide_neby(self, nb)
        self.play(FadeOut(care))

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Rate = change in concentration per unit time: chord gives average, tangent gives instantaneous.",
            M(r"r = -\tfrac{1}{a}\tfrac{d[\mathrm{A}]}{dt} = \tfrac{1}{c}\tfrac{d[\mathrm{C}]}{dt};\quad r = k[\mathrm{A}]^{x}[\mathrm{B}]^{y}\ (\text{experimental})", size=38),
            M(r"[k] = (\mathrm{mol\,L^{-1}})^{1-n}\,\mathrm{s^{-1}}", size=38),
            "Order: experimental, may be 0 or fractional. Molecularity: 1, 2 or 3 per elementary step.",
            M(r"\text{zero: } [\mathrm{A}] = [\mathrm{A}]_0 - kt,\ t_{1/2} = \tfrac{[\mathrm{A}]_0}{2k};\quad \text{first: } k = \tfrac{2.303}{t}\log\tfrac{[\mathrm{A}]_0}{[\mathrm{A}]},\ t_{1/2} = \tfrac{0.693}{k}", size=36),
            "Collisions need energy ≥ Ea and the right orientation; the activated complex sits on the barrier.",
            M(r"k = Ae^{-E_a/RT},\quad \log\tfrac{k_2}{k_1} = \tfrac{E_a}{2.303R}\left(\tfrac{T_2 - T_1}{T_1T_2}\right)", size=38),
            "A catalyst lowers Ea both ways; ΔH and equilibrium unchanged. Homogeneous, heterogeneous, enzyme.",
        ], "Let us recap. The rate is the slope of the concentration time curve, divided by the coefficient. The rate law is found by experiment, and the units of k reveal the order. Order can be zero or fractional, molecularity cannot. Zero order runs in a straight line, first order decays exponentially with a constant half life of point six nine three over k. Only collisions with enough energy and the right orientation succeed, which Arrhenius captured in one equation. And a catalyst lowers the barrier both ways, changing neither delta H nor the equilibrium.")
        self.outro("That is chemical kinetics. Next, we follow the energy itself, with thermodynamics: enthalpy, entropy, and the free energy that decides whether a reaction can go at all. See you in the next lesson on NEBians.")
