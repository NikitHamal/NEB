import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import arrow, clock, curve, example, neby_in, neby_out, readout  # noqa: E402

C_N, C_A, C_S, C_T, C_M = th.CORAL, th.MINT, th.SKY, th.AMBER, th.PINK


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 8
    TITLE = "Waves in Pipes and Strings"
    SUBTITLE = "Why a flute and a sarangi sing the notes they do"
    SECTIONS = ["Stationary waves in pipes", "Harmonics of organ pipes", "End correction", "Waves on a stretched string",
                "Harmonics of a string", "Laws of a vibrating string"]
    NEXT = "Unit 9 · Acoustic Phenomena"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ pipe drawing
    def pipe(self, x0, L, y, h=1.0, kind="closed", n=1, t=None, amp=0.22, nl=28, env=True, label=True):
        """A pipe from x0 to x0+L at height y. kind: 'closed' (closed at the left) or 'open'. Air layers move with the
        mode's displacement; a dashed envelope shows the standing wave."""
        walls = VGroup(Line([x0, y + h / 2, 0], [x0 + L, y + h / 2, 0]), Line([x0, y - h / 2, 0], [x0 + L, y - h / 2, 0])).set_stroke(th.BODY, 5)
        if kind == "closed":
            walls.add(Line([x0, y + h / 2, 0], [x0, y - h / 2, 0], stroke_width=9, color=th.BODY))
            k = (2 * n - 1) * PI / (2 * L)
            shape = lambda x: np.sin(k * (x - x0))
        else:
            k = n * PI / L
            shape = lambda x: np.cos(k * (x - x0))
        g = VGroup(walls)
        if env:
            e1 = DashedVMobject(curve(lambda x: y + 0.42 * h * shape(x), x0, x0 + L, n=120, color=C_T, width=3), num_dashes=40)
            e2 = DashedVMobject(curve(lambda x: y - 0.42 * h * shape(x), x0, x0 + L, n=120, color=C_T, width=3), num_dashes=40)
            g.add(e1, e2)
        layers = None
        if t is not None:
            xs = np.linspace(x0 + 0.06, x0 + L - 0.06, nl)
            layers = VGroup(*[Line([x, y - h / 2 + 0.06, 0], [x, y + h / 2 - 0.06, 0], color=C_S, stroke_width=2.5) for x in xs])
            w = 3.0 * (1 if kind == "closed" else 1) * (2 * n - 1 if kind == "closed" else n)

            def upd(m):
                c = np.cos(w * t.get_value())
                for ln, x in zip(m, xs):
                    ln.set_x(x + amp * shape(x) * c)
            layers.add_updater(upd)
            g.add(layers)
        return g, shape

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        t = clock(self, 1.0)
        L = 6.0
        x0 = -3.0
        g1, _ = self.pipe(x0, L, 0.6, 1.2, "open", 1, t, amp=0.3)
        tag = T("a bansuri: open at both ends", size=26, color=th.MUTED).to_edge(UP, buff=0.7)
        fr = readout("f =", lambda: 680, "Hz", size=40, color=C_T).move_to([0, -1.6, 0])
        with self.say("Blow across a bamboo bansuri, a pipe open at both ends, and it sings a clear note. For a pipe twenty five centimetres long, that note is six hundred and eighty hertz. The air inside is sloshing back and forth in a standing wave."):
            self.play(FadeIn(tag), FadeIn(g1), FadeIn(fr))
            self.wait(3)
        g2, _ = self.pipe(x0, L, 0.6, 1.2, "closed", 1, t, amp=0.3)
        tag2 = T("now close one end", size=26, color=C_N).to_edge(UP, buff=0.7)
        fr2 = readout("f =", lambda: 340, "Hz", size=40, color=C_N).move_to([0, -1.6, 0])
        with self.say("Now put your thumb over one end. Same pipe, same air, same length. Listen."):
            self.play(FadeOut(tag), FadeIn(tag2))
            self.play(FadeOut(g1), FadeIn(g2), FadeOut(fr), FadeIn(fr2))
            self.sfx("thud", gain=-12)
            self.wait(2)
        nb = neby_in(self, "surprised", corner=UR)
        q = T("One thumb, and the note drops a whole octave. Why?", size=32, color=th.AMBER, weight="BOLD").move_to([0, -2.6, 0])
        with self.say("The note drops to three hundred and forty hertz. Exactly half. A whole octave lower, just from closing one end. Why exactly half? By the end of this lesson you will be able to predict every note a pipe or a string can make."):
            self.play(FadeIn(q, shift=UP * 0.2))
            self.wait(1)
        self.play(FadeOut(VGroup(tag2, fr2, q)), FadeOut(g2))
        g1[-1].clear_updaters()
        g2[-1].clear_updaters()
        self.remove(g1, g2, t)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 8: Waves in Pipes and Strings. A flute, a sarangi, a bottle you blow across: all of them work the same way. A wave is trapped between two ends, and only the wavelengths that fit can survive."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the path. Stationary waves in pipes, the harmonics of closed and open organ pipes, the end correction and the resonance tube, the speed of a wave on a string, the harmonics of a string, and the three laws of a vibrating string.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        t = clock(self, 1.0)
        x0, L, y = -5.6, 7.0, 0.8
        walls = VGroup(Line([x0, y + 0.6, 0], [x0 + L, y + 0.6, 0]), Line([x0, y - 0.6, 0], [x0 + L, y - 0.6, 0]),
                       Line([x0 + L, y + 0.6, 0], [x0 + L, y - 0.6, 0], stroke_width=9)).set_stroke(th.BODY, 5)
        k = TAU / 3.2
        w = 2.4
        inc = always_redraw(lambda: curve(lambda x: y + 0.4 * np.sin(w * t.get_value() - k * (x - x0 - L)), x0, x0 + L, color=C_S, width=3))
        ref = always_redraw(lambda: curve(lambda x: y - 0.4 * np.sin(w * t.get_value() + k * (x - x0 - L)), x0, x0 + L, color=C_M, width=3))
        tot = always_redraw(lambda: curve(lambda x: y + 0.4 * (np.sin(w * t.get_value() - k * (x - x0 - L)) - np.sin(w * t.get_value() + k * (x - x0 - L))), x0, x0 + L, color=WHITE, width=5))
        with self.say("Send a sound wave down a pipe. When it reaches the end, it is reflected. The incident wave and the reflected wave have the same frequency and amplitude, but travel in opposite directions."):
            self.play(Create(walls))
            self.add(inc)
            self.play(FadeIn(inc))
            self.add(ref)
            self.play(FadeIn(ref))
        with self.say("Just as in the last unit, they superpose into a stationary wave, with fixed nodes and antinodes. Adjacent nodes are half a wavelength apart, and a node and the next antinode are a quarter wavelength apart."):
            self.add(tot)
            self.play(FadeIn(tot), inc.animate.set_stroke(opacity=0.3), ref.animate.set_stroke(opacity=0.3))
            self.wait(3)
        self.play(FadeOut(walls), FadeOut(inc), FadeOut(ref), FadeOut(tot))
        self.remove(inc, ref, tot)
        title = T("The ends decide everything", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        y1, y2 = 1.0, -1.6
        cl = VGroup(Line([-5.6, y1 + 0.5, 0], [-2.0, y1 + 0.5, 0]), Line([-5.6, y1 - 0.5, 0], [-2.0, y1 - 0.5, 0])).set_stroke(th.BODY, 5)
        cap = Line([-2.0, y1 + 0.5, 0], [-2.0, y1 - 0.5, 0], stroke_width=10, color=th.BODY)
        mol = always_redraw(lambda: VGroup(*[Dot([-2.0 - d - 0.25 * (d / 3.2) * np.cos(4 * t.get_value()) * 0 - 0.18 * np.sin(PI * d / 3.2 * 0.5) * np.cos(4 * t.get_value()), y1 + yy, 0], radius=0.06, color=C_S)
                                           for d in np.linspace(0.15, 3.3, 9) for yy in (-0.25, 0, 0.25)]))
        cll = VGroup(T("closed end: air cannot move", size=24, color=C_N), T("displacement NODE  ·  pressure antinode", size=24, color=C_N, weight="SEMIBOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, y1, 0])
        op = VGroup(Line([-5.6, y2 + 0.5, 0], [-2.0, y2 + 0.5, 0]), Line([-5.6, y2 - 0.5, 0], [-2.0, y2 - 0.5, 0])).set_stroke(th.BODY, 5)
        mol2 = always_redraw(lambda: VGroup(*[Dot([-2.0 - d - 0.3 * np.cos(PI * d / 3.2 * 0.5) * np.cos(4 * t.get_value()), y2 + yy, 0], radius=0.06, color=C_S)
                                            for d in np.linspace(-0.2, 3.3, 10) for yy in (-0.25, 0, 0.25)]))
        opl = VGroup(T("open end: air moves freely, pressure fixed by the atmosphere", size=24, color=C_A), T("displacement ANTINODE  ·  pressure node", size=24, color=C_A, weight="SEMIBOLD")).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, y2, 0])
        if opl.width > 7.4:
            opl.scale_to_fit_width(7.4).move_to([2.9, y2, 0])
        with self.say("Where the nodes sit is decided by the boundary condition at each end. At a closed end, the rigid wall stops the air from moving. Its displacement must be zero: a displacement node. But the air piles up and thins out against the wall, so the pressure swings the most there: a pressure antinode."):
            self.play(FadeIn(title), Create(cl), Create(cap))
            self.add(mol)
            self.play(FadeIn(mol), FadeIn(cll))
            self.wait(1.5)
        with self.say("At an open end, the air is free to move, but it touches the atmosphere, whose pressure it cannot change. The pressure variation is zero: a pressure node, which is the same place as a displacement antinode."):
            self.play(Create(op))
            self.add(mol2)
            self.play(FadeIn(mol2), FadeIn(opl))
            self.wait(1.5)
        self.play(FadeOut(VGroup(title, cl, cap, cll, op, opl)), FadeOut(mol), FadeOut(mol2))
        self.remove(mol, mol2, t)
        cau = self.callout("careful", "Displacement node = pressure antinode. The two pictures are always a quarter wavelength out of step. Decide which one you are drawing before you draw it.", width=11, size=28)
        with self.say("Keep this straight. A displacement node is a pressure antinode. The two descriptions are always a quarter wavelength out of step. If a question says pressure antinode at the closed end, it means exactly the same as displacement node. In this lesson we always draw displacement."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        defs = VGroup(T("Closed pipe: closed at one end, open at the other", size=28, color=C_N), T("e.g. a stopped organ pipe, a test tube", size=24, color=th.MUTED),
                      T("Open pipe: open at both ends", size=28, color=C_A), T("e.g. a flute or a bansuri", size=24, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        defs[1].shift(RIGHT * 0.4)
        defs[3].shift(RIGHT * 0.4)
        with self.say("Two kinds of pipe follow. A closed pipe, or closed organ pipe, is closed at one end and open at the other, like a test tube. An open pipe is open at both ends, like a flute or a bansuri."):
            self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in defs], lag_ratio=0.3), run_time=2)
        self.play(FadeOut(defs))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        t = clock(self, 1.0)
        title = T("Closed pipe: node at the closed end, antinode at the open end", size=28, color=C_N, weight="BOLD").to_edge(UP, buff=0.75)
        x0, L = -5.8, 5.4
        ys = [1.5, -0.2, -1.9]
        rows = VGroup()
        texts = [r"L = \frac{\lambda_1}{4}\ \Rightarrow\ f_1 = \frac{v}{4L}", r"L = \frac{3\lambda}{4}\ \Rightarrow\ f = 3f_1", r"L = \frac{5\lambda}{4}\ \Rightarrow\ f = 5f_1"]
        names = ["fundamental (1st harmonic)", "1st overtone = 3rd harmonic", "2nd overtone = 5th harmonic"]
        self.play(FadeIn(title))
        says = ["Start with the closed pipe. The closed end must be a node, and the open end an antinode. The simplest wave that fits goes from a node to the next antinode: a quarter of a wavelength. So L equals lambda by four, and the fundamental frequency is v over four L.",
                "The next one that fits has three quarters of a wavelength in the pipe. Its frequency is three times the fundamental.",
                "Then five quarters, at five times the fundamental. You can never fit two quarters, or four, with a node at one end and an antinode at the other. So a closed pipe makes only the odd harmonics."]
        for i in range(3):
            g, _ = self.pipe(x0, L, ys[i], 1.1, "closed", i + 1, t, amp=0.2)
            eq = M(texts[i], size=36).move_to([3.3, ys[i] + 0.15, 0])
            nm = T(names[i], size=20, color=th.MUTED).next_to(eq, DOWN, buff=0.1)
            rows.add(VGroup(g, eq, nm))
            with self.say(says[i]):
                self.play(FadeIn(g), Write(eq), FadeIn(nm))
                self.wait(1)
        gen = M(r"L = (2n-1)\frac{\lambda_n}{4}\ \Rightarrow\ f_n = (2n-1)\frac{v}{4L}", size=40, color=C_N).to_edge(DOWN, buff=0.55)
        with self.say("In general, L equals two n minus one, times lambda over four. So f n equals two n minus one, times v over four L. One, three, five, and so on. The even harmonics are missing."):
            self.play(Write(gen))
        self.play(FadeOut(VGroup(title, gen)), *[FadeOut(r) for r in rows])
        for r in rows:
            r[0][-1].clear_updaters()
        self.remove(*rows)
        title = T("Open pipe: antinodes at both ends", size=28, color=C_A, weight="BOLD").to_edge(UP, buff=0.75)
        rows = VGroup()
        texts = [r"L = \frac{\lambda_1}{2}\ \Rightarrow\ f_1 = \frac{v}{2L}", r"L = \lambda\ \Rightarrow\ f = 2f_1", r"L = \frac{3\lambda}{2}\ \Rightarrow\ f = 3f_1"]
        names = ["fundamental (1st harmonic)", "1st overtone = 2nd harmonic", "2nd overtone = 3rd harmonic"]
        self.play(FadeIn(title))
        says = ["Now the open pipe. Both ends are antinodes. The simplest wave has one node in the middle: half a wavelength. So L equals lambda by two, and the fundamental is v over two L.",
                "Next, a whole wavelength fits, at twice the fundamental.",
                "Then one and a half wavelengths, at three times. Every whole number fits, so an open pipe makes all the harmonics: f n equals n v over two L."]
        for i in range(3):
            g, _ = self.pipe(x0, L, ys[i], 1.1, "open", i + 1, t, amp=0.2)
            eq = M(texts[i], size=36).move_to([3.3, ys[i] + 0.15, 0])
            nm = T(names[i], size=20, color=th.MUTED).next_to(eq, DOWN, buff=0.1)
            rows.add(VGroup(g, eq, nm))
            with self.say(says[i]):
                self.play(FadeIn(g), Write(eq), FadeIn(nm))
                self.wait(1)
        self.play(FadeOut(title), *[FadeOut(r) for r in rows])
        for r in rows:
            r[0][-1].clear_updaters()
        self.remove(*rows, t)
        self.compare()
        example(self, "A closed organ pipe is 25 cm long and v = 340 m/s. Find its fundamental and its first two overtones. What would the fundamental be if the pipe were open at both ends?",
                [r"f_1 = \frac{v}{4L} = \frac{340}{4\times 0.25} = 340\ \text{Hz}",
                 r"\text{overtones: } 3f_1 = 1020\ \text{Hz},\quad 5f_1 = 1700\ \text{Hz}",
                 r"\text{open: } f_1' = \frac{v}{2L} = \frac{340}{0.50} = 680\ \text{Hz} = 2f_1"],
                ["Now the mystery from the start. A closed pipe twenty five centimetres long, with sound at three hundred and forty metres per second. Find its fundamental, its first two overtones, and the fundamental if it were open.",
                 "Closed: f one is v over four L, three forty over one, three hundred and forty hertz.",
                 "Only odd harmonics exist, so the first overtone is the third harmonic, one thousand and twenty hertz, and the second overtone is the fifth, seventeen hundred hertz.",
                 "Open at both ends, f one is v over two L: three forty over zero point five, six hundred and eighty hertz. Exactly double. Closing one end turns the half wavelength into a quarter wavelength, the wavelength doubles, and the note drops an octave. Mystery solved."], size=40)
        self.quiz("The first overtone of a closed organ pipe is its",
                  ["2nd harmonic", "3rd harmonic", "4th harmonic", "5th harmonic"], 1,
                  "Pause and think. The first overtone of a closed pipe is which harmonic?",
                  "B, the third harmonic. The second harmonic cannot exist in a closed pipe, so the first tone above the fundamental is three f one. Answer A is right for an open pipe, which is why it is such a popular wrong answer.")
        example(self, "The third harmonic of a closed pipe has the same frequency as the first overtone of an open pipe 50 cm long. Find the length of the closed pipe.",
                [r"\text{open, 1st overtone} = 2\times\frac{v}{2L_o} = \frac{v}{L_o}",
                 r"\text{closed, 3rd harmonic} = \frac{3v}{4L_c}",
                 r"\frac{3v}{4L_c} = \frac{v}{L_o}\ \Rightarrow\ L_c = \frac{3L_o}{4} = \frac{3\times 0.50}{4} = 37.5\ \text{cm}"],
                ["A favourite five mark question. The third harmonic of a closed pipe matches the first overtone of an open pipe fifty centimetres long. How long is the closed pipe?",
                 "The first overtone of an open pipe is its second harmonic: two times v over two L o, which is v over L o.",
                 "The third harmonic of a closed pipe is three v over four L c.",
                 "Set them equal. v cancels, and L c is three quarters of L o: thirty seven point five centimetres."], size=40)

    def compare(self):
        title = T("Closed vs open pipe", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        rows = [("", "Closed pipe", "Open pipe"), ("fundamental", "v / 4L", "v / 2L"), ("harmonics", "odd only: 1, 3, 5 …", "all: 1, 2, 3 …"),
                ("1st overtone", "3rd harmonic", "2nd harmonic"), ("quality", "poorer", "richer"), ("same length", "an octave lower", "an octave higher")]
        grid = VGroup()
        for i, r in enumerate(rows):
            row = VGroup(*[T(c if c else "·", size=26 if i else 30, color=(th.BG if not c else ([th.MUTED, C_N, C_A][j] if i == 0 or j == 0 else th.BODY)),
                             weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.4, -0.6, 3.4]):
                row[j].move_to([x, 2.0 - i * 0.72, 0])
            grid.add(row)
        bars = VGroup()
        for j, (col, fs) in enumerate([(C_N, [1, 3, 5, 7]), (C_A, [1, 2, 3, 4, 5, 6, 7])]):
            for f in range(1, 8):
                h = 0.9 / f if f in fs else 0.0
                if h > 0:
                    bars.add(Rectangle(width=0.22, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([-2.2 + j * 4.0 + f * 0.32, -2.85, 0], aligned_edge=DOWN))
        bl = VGroup(T("spectrum", size=20, color=th.MUTED).move_to([-1.0, -3.05, 0]), T("spectrum", size=20, color=th.MUTED).move_to([3.0, -3.05, 0]))
        with self.say("Here is the comparison. The closed pipe has fundamental v over four L and only odd harmonics. The open pipe has v over two L and all of them. So the first overtone of a closed pipe is the third harmonic, but for an open pipe it is the second. With more harmonics, the open pipe gives a richer note, and for the same length it sounds an octave higher.") as v_:
            self.play(FadeIn(title))
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 7 - 0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(bl))
        self.play(FadeOut(VGroup(title, grid, bars, bl)))
        self.tip("A harmonic is any whole-number multiple of f₁. An overtone is a tone actually produced above f₁, counted in order. In a closed pipe the 1st overtone is the 3rd harmonic.",
                 "Harmonic or overtone? A harmonic is any whole number multiple of the fundamental. An overtone is a tone that is actually produced above the fundamental, counted in order. In a closed pipe, the first overtone is the third harmonic, because the second does not exist. Mixing up these two words loses marks in almost every paper.", state="think")

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        t = clock(self, 1.0)
        x0, L, y = -5.0, 6.0, 0.6
        g, shape = self.pipe(x0, L, y, 1.4, "closed", 1, t, amp=0.25, env=False)
        e = 0.7
        k = PI / (2 * (L + e))
        env = VGroup(*[DashedVMobject(curve(lambda x, s=s: y + s * 0.6 * np.sin(k * (x - x0)), x0, x0 + L + e, n=120, color=C_T, width=3), num_dashes=40) for s in (1, -1)])
        A = Dot([x0 + L + e, y, 0], color=C_A, radius=0.1)
        Al = T("antinode", size=22, color=C_A).next_to(A, RIGHT, buff=0.2)
        br = BraceBetweenPoints([x0 + L, y - 0.9, 0], [x0 + L + e, y - 0.9, 0], DOWN, color=C_A)
        bl = M("e", size=34, color=C_A).next_to(br, DOWN, buff=0.08)
        with self.say("There is a small catch. The air just outside an open end still takes part in the vibration. So the antinode does not sit exactly at the rim. It sits a little way outside."):
            self.play(FadeIn(g))
            self.play(Create(env))
            self.play(FadeIn(A), FadeIn(Al))
        eqs = VGroup(M(r"e = 0.6\,r", size=48, color=C_A), M(r"\text{closed: } f_1 = \frac{v}{4(L + e)}", size=40), M(r"\text{open: } f_1 = \frac{v}{2(L + 2e)}", size=40)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -2.05, 0]).scale(0.9)
        with self.say("That extra distance is the end correction, e. Lord Rayleigh showed that for a pipe of internal radius r, e is about zero point six r. So the pipe behaves as if it were a little longer than it measures."):
            self.play(GrowFromCenter(br), FadeIn(bl))
            self.play(Write(eqs[0]))
        with self.say("For a closed pipe the effective length is L plus e. An open pipe has two open ends, so it gets two corrections: L plus two e. The correction matters most for short, wide pipes."):
            self.play(Write(eqs[1]))
            self.play(Write(eqs[2]))
        self.play(FadeOut(VGroup(env, A, Al, br, bl, eqs)), FadeOut(g))
        g[-1].clear_updaters()
        self.remove(g, t)
        example(self, "A closed pipe 20 cm long has an internal radius of 2.0 cm. Taking v = 340 m/s, find its fundamental frequency with and without the end correction.",
                [r"\text{without: } f_1 = \frac{340}{4\times 0.20} = 425\ \text{Hz}",
                 r"e = 0.6\times 0.020 = 0.012\ \text{m}",
                 r"\text{with: } f_1 = \frac{340}{4(0.200 + 0.012)} = \frac{340}{0.848} = 401\ \text{Hz}"],
                ["How big is the effect? A closed pipe twenty centimetres long has an internal radius of two centimetres. Find the fundamental with and without the end correction.",
                 "Without it: three forty over four times zero point two, four hundred and twenty five hertz.",
                 "The end correction is zero point six times zero point zero two, one point two centimetres.",
                 "With it: three forty over four times zero point two one two, about four hundred and one hertz. Twenty four hertz lower, about a semitone. You can easily hear that."], size=42)
        self.resonance_tube()

    def resonance_tube(self):
        title = T("The resonance tube", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        S = 4.6
        top = 2.3
        x = -4.0
        f, v, e = 480.0, 345.6, 0.010
        lam = v / f
        lev = ValueTracker(0.05)
        tube = VGroup(Line([x - 0.35, top, 0], [x - 0.35, top - 0.75 * S, 0]), Line([x + 0.35, top, 0], [x + 0.35, top - 0.75 * S, 0])).set_stroke(th.BODY, 4)
        water = always_redraw(lambda: Rectangle(width=0.66, height=max(0.01, S * (0.75 - lev.get_value())), stroke_width=0,
                                                fill_color="#1E5A8A", fill_opacity=0.85).move_to([x, top - 0.75 * S, 0], aligned_edge=DOWN))
        fork = VGroup(Line([x - 0.15, top + 0.9, 0], [x - 0.15, top + 0.35, 0]), Line([x + 0.15, top + 0.9, 0], [x + 0.15, top + 0.35, 0]),
                      Arc(radius=0.15, start_angle=PI, angle=PI, arc_center=[x, top + 0.35, 0]), Line([x, top + 0.2, 0], [x, top - 0.0, 0])).set_stroke(th.MUTED, 4)
        fl = T("480 Hz fork", size=20, color=th.MUTED).next_to(fork, LEFT, buff=0.2)

        def loud(l):
            Le = l + e
            return max(np.exp(-((Le - m * lam / 4) / 0.012) ** 2) for m in (1, 3, 5))
        meter_bg = Rectangle(width=0.5, height=3.0, stroke_color=th.FAINT, stroke_width=2).move_to([-1.0, 0.0, 0])
        meter = always_redraw(lambda: Rectangle(width=0.5, height=max(0.02, 3.0 * loud(lev.get_value())), stroke_width=0, fill_color=C_T, fill_opacity=0.9).align_to(meter_bg, DOWN).set_x(-1.0))
        ml = T("loudness", size=20, color=C_T).next_to(meter_bg, DOWN, buff=0.12)
        lr = readout("l =", lambda: 100 * lev.get_value(), "cm", decimals=1, size=26).move_to([-1.0, 2.0, 0])
        with self.say("The standard school experiment for the speed of sound uses a closed pipe whose length you can change: the resonance tube. Hold a sounding tuning fork over a tube of air above water. Lower the water, and the air column gets longer."):
            self.play(FadeIn(title), Create(tube), FadeIn(fork), FadeIn(fl))
            self.add(water, meter)
            self.play(FadeIn(water), FadeIn(meter_bg), FadeIn(meter), FadeIn(ml), FadeIn(lr))
        l1, l2 = lam / 4 - e, 3 * lam / 4 - e
        with self.say("At one particular length, the note suddenly booms out. That is the first resonance, at length l one. The air column now fits a quarter wavelength, plus the end correction."):
            self.play(lev.animate.set_value(l1), run_time=3.5, rate_func=linear)
            self.sfx("bell", gain=-14)
            m1 = VGroup(Line([x + 0.45, top - S * l1, 0], [x + 0.8, top - S * l1, 0], color=C_T, stroke_width=3), T("l₁ = 17.0 cm", size=20, color=C_T).next_to([x + 0.8, top - S * l1, 0], RIGHT, buff=0.1))
            self.play(FadeIn(m1))
        with self.say("Keep lowering. The sound fades, then booms again at a second length, l two, where three quarters of a wavelength fit."):
            self.play(lev.animate.set_value(l2), run_time=4.0, rate_func=linear)
            self.sfx("bell", gain=-14)
            m2 = VGroup(Line([x + 0.45, top - S * l2, 0], [x + 0.8, top - S * l2, 0], color=C_T, stroke_width=3), T("l₂ = 53.0 cm", size=20, color=C_T).next_to([x + 0.8, top - S * l2, 0], RIGHT, buff=0.1))
            self.play(FadeIn(m2))
        L = VGroup(M(r"l_1 + e = \frac{\lambda}{4},\qquad l_2 + e = \frac{3\lambda}{4}", size=36),
                   M(r"l_2 - l_1 = \frac{\lambda}{2}\ \Rightarrow\ v = f\lambda = 2f(l_2 - l_1)", size=36, color=C_S),
                   M(r"3l_1 + 3e = l_2 + e\ \Rightarrow\ e = \frac{l_2 - 3l_1}{2}", size=36, color=C_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.6, 0])
        with self.say("Write both conditions with the end correction: l one plus e is lambda by four, and l two plus e is three lambda by four."):
            self.play(Write(L[0]))
        with self.say("Subtract the first from the second, and e disappears completely. l two minus l one is half a wavelength. So v equals two f, times l two minus l one."):
            self.play(Write(L[1]))
        with self.say("Or multiply the first by three and subtract the second, and you find the end correction itself: l two minus three l one, over two. The awkward unknown cancels, which is why this experiment is so reliable."):
            self.play(Write(L[2]))
        steps = VGroup(M(r"\lambda = 2(0.530 - 0.170) = 0.720\ \text{m}", size=34), M(r"v = 480\times 0.720 = 345.6\ \text{m s}^{-1}", size=34, color=C_S),
                       M(r"e = \frac{0.530 - 0.510}{2} = 1.0\ \text{cm},\ \ r = \frac{e}{0.6} = 1.7\ \text{cm}", size=34, color=C_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, -2.0, 0])
        with self.say("With a four hundred and eighty hertz fork, l one is seventeen centimetres and l two fifty three. So lambda is two times thirty six centimetres, zero point seven two metres, and the speed of sound is four eighty times zero point seven two: three hundred and forty five point six metres per second. The end correction is fifty three minus fifty one, over two: one centimetre. So the tube's radius is about one point seven centimetres."):
            for s_ in steps:
                self.play(Write(s_), run_time=1.2)
        nb = neby_in(self, "success", corner=UR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, tube, fork, fl, meter_bg, ml, lr, m1, m2, L, steps)), FadeOut(water), FadeOut(meter))
        self.remove(water, meter)
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        t = ValueTracker(0)
        T0, mu = 1.0, 1.0
        pulse = always_redraw(lambda: curve(lambda x: 0.9 * np.exp(-((x - (-6.5 + 2.4 * t.get_value())) / 0.5) ** 2), -6.3, 6.3, n=240, color=C_S, width=5))
        ends = VGroup(Dot([-6.3, 0, 0], color=th.MUTED), Dot([6.3, 0, 0], color=th.MUTED))
        Tl = VGroup(Arrow([5.2, -0.8, 0], [6.6, -0.8, 0], buff=0, color=C_T, stroke_width=5), M("T", size=32, color=C_T).move_to([5.9, -1.2, 0]))
        with self.say("Now strings. A stretched string carries transverse waves. Two things control their speed: the tension, T, that pulls a displaced piece back, and the mass per unit length, mu, that resists being moved."):
            self.add(pulse)
            self.play(FadeIn(ends), FadeIn(Tl))
            self.play(t.animate.set_value(5.4), run_time=4, rate_func=linear)
        self.play(FadeOut(VGroup(ends, Tl)), FadeOut(pulse))
        self.remove(pulse)
        title = T("Deriving v = √(T/μ)", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        C = np.array([-3.2, -2.6, 0])
        R = 3.6
        dth = 0.7
        arc = Arc(radius=R, start_angle=PI / 2 - dth / 2, angle=dth, arc_center=C, color=C_S, stroke_width=8)
        rest = VGroup(Arc(radius=R, start_angle=PI / 2 + dth / 2, angle=0.5, arc_center=C, color=C_S, stroke_width=4).set_opacity(0.4),
                      Arc(radius=R, start_angle=PI / 2 - dth / 2 - 0.5, angle=0.5, arc_center=C, color=C_S, stroke_width=4).set_opacity(0.4))
        r1 = DashedLine(C, C + R * np.array([np.cos(PI / 2 + dth / 2), np.sin(PI / 2 + dth / 2), 0]), color=th.FAINT)
        r2 = DashedLine(C, C + R * np.array([np.cos(PI / 2 - dth / 2), np.sin(PI / 2 - dth / 2), 0]), color=th.FAINT)
        ang = Arc(radius=0.6, start_angle=PI / 2 - dth / 2, angle=dth, arc_center=C, color=th.MUTED)
        al = M(r"\Delta\theta", size=28).next_to(ang, UP, buff=0.05)
        Rl = M("R", size=30).move_to(C + 1.8 * np.array([np.cos(PI / 2 + dth / 2 + 0.12), np.sin(PI / 2 + dth / 2 + 0.12), 0]))
        pL = C + R * np.array([np.cos(PI / 2 + dth / 2), np.sin(PI / 2 + dth / 2), 0])
        pR = C + R * np.array([np.cos(PI / 2 - dth / 2), np.sin(PI / 2 - dth / 2), 0])
        tL = np.array([-np.sin(PI / 2 + dth / 2), np.cos(PI / 2 + dth / 2), 0]) * -1
        tR = np.array([-np.sin(PI / 2 - dth / 2), np.cos(PI / 2 - dth / 2), 0])
        TL = Arrow(pL, pL + 1.6 * np.array([-np.sin(PI / 2 + dth / 2), np.cos(PI / 2 + dth / 2), 0]), buff=0, color=C_T, stroke_width=6)
        TR = Arrow(pR, pR + 1.6 * np.array([np.sin(PI / 2 - dth / 2), -np.cos(PI / 2 - dth / 2), 0]), buff=0, color=C_T, stroke_width=6)
        TLl = M("T", size=32, color=C_T).next_to(TL.get_end(), LEFT, buff=0.1)
        TRl = M("T", size=32, color=C_T).next_to(TR.get_end(), RIGHT, buff=0.1)
        Fd = Arrow(C + UP * (R + 0.1), C + UP * (R - 1.3), buff=0, color=C_N, stroke_width=7)
        Fl = M(r"F = 2T\sin\tfrac{\Delta\theta}{2}", size=30, color=C_N).next_to(Fd, RIGHT, buff=0.15).shift(DOWN * 0.2)
        vel = Arrow(C + UP * (R + 0.35) + RIGHT * 0.9, C + UP * (R + 0.35) + LEFT * 0.9, buff=0, color=th.MINT, stroke_width=5)
        vl = M("v", size=30, color=th.MINT).next_to(vel, UP, buff=0.05)
        with self.say("Here is the derivation, a four mark favourite. Ride along with the pulse. In that frame, the pulse stands still, and the string streams backwards through it at speed v."):
            self.play(FadeIn(title), Create(arc), FadeIn(rest))
            self.play(GrowArrow(vel), FadeIn(vl))
        with self.say("Take the tiny piece of string right at the crest. It is nearly an arc of a circle of radius R, subtending a small angle delta theta. Its length is R delta theta, so its mass is mu R delta theta."):
            self.play(Create(r1), Create(r2), Create(ang), FadeIn(al), FadeIn(Rl))
        with self.say("The tension pulls along the string at each end. The sideways parts cancel, and the parts toward the centre add up: F equals two T sine delta theta by two, which for a small angle is T delta theta."):
            self.play(GrowArrow(TL), GrowArrow(TR), FadeIn(TLl), FadeIn(TRl))
            self.play(GrowArrow(Fd), FadeIn(Fl))
        L = VGroup(M(r"\Delta m = \mu R\,\Delta\theta", size=36), M(r"F = 2T\sin\frac{\Delta\theta}{2} \approx T\,\Delta\theta", size=36),
                   M(r"T\,\Delta\theta = \Delta m\frac{v^{2}}{R} = \mu R\,\Delta\theta\,\frac{v^{2}}{R}", size=36),
                   M(r"v = \sqrt{\frac{T}{\mu}}", size=60, color=C_S)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.6, 0.0, 0])
        with self.say("In this frame the piece moves round the arc at speed v, so F must be the centripetal force: mass times v squared over R. T delta theta equals mu R delta theta, times v squared over R."):
            self.play(Write(L[0]))
            self.play(Write(L[1]))
            self.play(Write(L[2]))
        with self.say("R cancels, delta theta cancels, and v squared equals T over mu. The speed of a transverse wave on a string is the square root of T over mu."):
            self.sfx("impact", gain=-12)
            self.play(Write(L[3]))
            self.play(Circumscribe(L[3], color=C_S))
        self.play(FadeOut(VGroup(title, arc, rest, r1, r2, ang, al, Rl, TL, TR, TLl, TRl, Fd, Fl, vel, vl, L[:3])), L[3].animate.to_edge(UP, buff=0.9))
        dims = M(r"\left[\frac{T}{\mu}\right] = \frac{\text{M L T}^{-2}}{\text{M L}^{-1}} = \text{L}^{2}\text{T}^{-2}\ \checkmark", size=40).move_to([0, 0.6, 0])
        thick = M(r"\mu = \pi r^{2}\rho:\ \text{a thicker or denser wire carries slower waves}", size=36).next_to(dims, DOWN, buff=0.5)
        with self.say("Check the dimensions. Tension over mass per length is length squared per time squared, and its square root is a speed. And since mu is pi r squared rho for a wire, a thicker or denser wire carries slower waves. That is why the low strings of a guitar are the fat ones."):
            self.play(Write(dims))
            self.play(Write(thick))
        self.play(FadeOut(VGroup(dims, thick, L[3])))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        t = clock(self, 1.0)
        x0, L = -5.6, 7.4
        ys = [1.9, 0.5, -0.9, -2.3]
        rows = VGroup()
        cl = VGroup()
        for i, y in enumerate(ys):
            n = i + 1
            cl.add(VGroup(Dot([x0, y, 0], color=th.MUTED, radius=0.09), Dot([x0 + L, y, 0], color=th.MUTED, radius=0.09)))
            s = always_redraw(lambda n=n, y=y: curve(lambda x: y + 0.45 * np.sin(n * PI * (x - x0) / L) * np.cos(2.2 * n * t.get_value()), x0, x0 + L, n=160, color=[C_S, C_A, C_T, C_M][n - 1], width=4))
            lab = M([r"n = 1:\ \ L = \frac{\lambda}{2},\ \ f_1", r"n = 2:\ \ L = \lambda,\ \ 2f_1", r"n = 3:\ \ L = \frac{3\lambda}{2},\ \ 3f_1", r"n = 4:\ \ L = 2\lambda,\ \ 4f_1"][n - 1], size=32).move_to([4.6, y, 0])
            rows.add(VGroup(s, lab))
        with self.say("A sonometer wire, or a sarangi string, is clamped at both ends. So both ends must be nodes. The string must hold a whole number of half wavelength loops."):
            self.play(FadeIn(cl))
            self.add(rows[0][0])
            self.play(FadeIn(rows[0][0]), FadeIn(rows[0][1]))
        with self.say("One loop, two loops, three loops, four. L equals n lambda by two. So lambda n is two L over n."):
            for r in rows[1:]:
                self.add(r[0])
                self.play(FadeIn(r[0]), FadeIn(r[1]), run_time=0.8)
            self.wait(1)
        eq = M(r"f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}},\qquad f_1 = \frac{1}{2L}\sqrt{\frac{T}{\mu}}", size=40, color=th.INK)
        box = BackgroundRectangle(eq, color=th.BG, fill_opacity=0.9, buff=0.2)
        eqg = VGroup(box, eq).to_edge(DOWN, buff=0.45)
        with self.say("Combine f equals v over lambda with v equals root T over mu. The n th mode has frequency n over two L, times root T over mu. Every whole number works, so unlike a closed pipe, a string gives every harmonic. That is why a plucked string sounds so rich."):
            self.play(FadeOut(rows[3]), FadeOut(cl[3]))
            self.play(FadeIn(eqg))
            self.wait(2)
        self.play(FadeOut(eqg), FadeOut(cl[:3]), *[FadeOut(r) for r in rows[:3]])
        self.remove(*[r[0] for r in rows], t)
        example(self, "A sonometer wire 50 cm long has mass per unit length 1.0 g/m and tension 160 N. Find the wave speed, the fundamental frequency and the second overtone.",
                [r"\mu = 1.0\times10^{-3}\ \text{kg m}^{-1}",
                 r"v = \sqrt{\frac{T}{\mu}} = \sqrt{\frac{160}{1.0\times10^{-3}}} = \sqrt{1.6\times10^{5}} = 400\ \text{m s}^{-1}",
                 r"f_1 = \frac{v}{2L} = \frac{400}{2\times 0.50} = 400\ \text{Hz}",
                 r"\text{2nd overtone} = 3f_1 = 1200\ \text{Hz}"],
                ["Worked example. A sonometer wire fifty centimetres long has a mass per unit length of one gram per metre, under a tension of one hundred and sixty newtons. Find the wave speed, the fundamental, and the second overtone.",
                 "Convert first: one gram per metre is one times ten to the minus three kilograms per metre.",
                 "v is root T over mu: root of one sixty over ten to the minus three, root of one point six times ten to the five, four hundred metres per second.",
                 "The fundamental is v over two L: four hundred over one, four hundred hertz.",
                 "A string has all harmonics, so the second overtone is the third harmonic: twelve hundred hertz."], size=40)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        Lt = ValueTracker(0.6)
        Tt = ValueTracker(100.0)
        mut = ValueTracker(1.0)
        f0 = 256.0
        fval = lambda: f0 * (0.6 / Lt.get_value()) * np.sqrt(Tt.get_value() / 100) / np.sqrt(mut.get_value())
        S = 12.0
        xa = -5.4
        box = RoundedRectangle(corner_radius=0.1, width=10.4, height=0.9, fill_color="#5a4632", fill_opacity=1, stroke_width=0).move_to([-0.2, -1.2, 0])
        fixed = Triangle(fill_color=th.MUTED, fill_opacity=1, stroke_width=0).scale(0.22).move_to([xa, -0.55, 0])
        bridge = always_redraw(lambda: Triangle(fill_color=th.INK, fill_opacity=1, stroke_width=0).scale(0.22).move_to([xa + S * Lt.get_value() * 0.6, -0.55, 0]))
        pul = Circle(radius=0.3, stroke_color=th.MUTED, stroke_width=4).move_to([4.9, -0.3, 0])
        t = clock(self, 1.0)
        wire = always_redraw(lambda: VGroup(
            curve(lambda x: -0.32 + 0.22 * np.sin(PI * (x - xa) / (S * Lt.get_value() * 0.6)) * np.cos(fval() / 60 * t.get_value()) / np.sqrt(mut.get_value()), xa, xa + S * Lt.get_value() * 0.6, n=120, color=C_S, width=2 + 2 * mut.get_value()),
            Line([xa + S * Lt.get_value() * 0.6, -0.32, 0], [4.9, -0.02, 0], color=C_S, stroke_width=2 + 2 * mut.get_value()).set_opacity(0.6)))
        weight = always_redraw(lambda: VGroup(Line([5.2, -0.3, 0], [5.2, -1.4, 0], color=th.MUTED, stroke_width=3),
                                              Rectangle(width=0.7, height=0.35 + 0.006 * Tt.get_value(), fill_color=th.MUTED, fill_opacity=1, stroke_width=0).move_to([5.2, -1.4, 0], aligned_edge=UP)))
        ro = VGroup(readout("L =", lambda: 100 * Lt.get_value(), "cm", decimals=0, size=28, color=th.INK),
                    readout("T =", lambda: Tt.get_value(), "N", decimals=1, size=28, color=C_T),
                    readout("μ =", lambda: mut.get_value(), "× μ₀", decimals=2, size=28, color=C_M),
                    readout("f =", fval, "Hz", decimals=0, size=34, color=C_S)).arrange(RIGHT, buff=0.55).move_to([0, 1.9, 0])
        with self.say("A sonometer lets us test this formula three ways. Here is a wire over a wooden box, stretched by a hanging weight, with a movable bridge to set the vibrating length."):
            self.add(wire, bridge, weight)
            self.play(FadeIn(box), FadeIn(fixed), FadeIn(bridge), FadeIn(wire), FadeIn(pul), FadeIn(weight), FadeIn(ro))
            self.wait(1)
        law1 = M(r"\text{Law of length: } f \propto \frac{1}{L}\quad (fL = \text{const})", size=36).move_to([0, 0.95, 0])
        with self.say("First, the law of length. Keep the tension and the wire the same, and slide the bridge. Halve the length, and the frequency doubles. f is proportional to one over L."):
            self.play(Write(law1))
            self.play(Lt.animate.set_value(0.3), run_time=2.5)
            self.play(Lt.animate.set_value(0.6), run_time=1.5)
        law2 = M(r"\text{Law of tension: } f \propto \sqrt{T}\quad (f/\sqrt{T} = \text{const})", size=36).move_to([0, 0.95, 0])
        with self.say("Second, the law of tension. Keep the length fixed, and add weight. Four times the tension only doubles the frequency. f is proportional to root T."):
            self.play(FadeOut(law1), FadeIn(law2))
            self.play(Tt.animate.set_value(400), run_time=2.5)
            self.play(Tt.animate.set_value(100), run_time=1.5)
        law3 = M(r"\text{Law of mass: } f \propto \frac{1}{\sqrt{\mu}}\quad (f\sqrt{\mu} = \text{const})", size=36).move_to([0, 0.95, 0])
        with self.say("Third, the law of mass. Swap in a heavier wire, with four times the mass per length, and the frequency halves. f is proportional to one over root mu."):
            self.play(FadeOut(law2), FadeIn(law3))
            self.play(mut.animate.set_value(4.0), run_time=2.5)
            self.play(mut.animate.set_value(1.0), run_time=1.5)
        self.play(FadeOut(VGroup(box, fixed, pul, ro, law3)), FadeOut(wire), FadeOut(bridge), FadeOut(weight))
        self.remove(wire, bridge, weight, t)
        sp = VGroup(M(r"\mu = \frac{\pi D^{2}\rho}{4}:\quad f \propto \frac{1}{D}\ \ (\text{law of diameter}),\quad f \propto \frac{1}{\sqrt{\rho}}\ \ (\text{law of density})", size=34),
                    M(r"f_1 = \frac{1}{LD}\sqrt{\frac{T}{\pi\rho}}", size=48, color=C_S)).arrange(DOWN, buff=0.45)
        with self.say("Because mu equals pi D squared rho over four, the law of mass is often split into two: a law of diameter, f proportional to one over D, and a law of density, f proportional to one over root rho. Put it all together, and f one equals one over L D, times root of T over pi rho."):
            self.play(Write(sp[0]))
            self.play(Write(sp[1]))
        self.play(FadeOut(sp))
        self.tip("Ratio method: f₂/f₁ = (L₁/L₂)·√(T₂/T₁)·√(μ₁/μ₂). Put in only what changed; you never need v or μ themselves.",
                 "Here is the fastest way through these numericals. Almost every one is a ratio question. Write f two over f one equals L one over L two, times root T two over T one, times root mu one over mu two, and put in only the quantities that changed. You never need the actual speed or mass per length.", state="wink")
        example(self, "A sonometer wire sounds 256 Hz under a tension of 100 N. (a) What tension gives 320 Hz at the same length? (b) Keeping 100 N, where should the bridge go on the 60 cm wire to give 320 Hz?",
                [r"(a)\ \ \frac{T_2}{T_1} = \left(\frac{320}{256}\right)^{2} = 1.25^{2} = 1.5625\ \Rightarrow\ T_2 = 156.25\ \text{N}",
                 r"(b)\ \ L_2 = L_1\frac{f_1}{f_2} = 60\times\frac{256}{320} = 60\times 0.8 = 48\ \text{cm}"],
                ["Worked example, using ratios. A wire sounds two hundred and fifty six hertz under one hundred newtons. What tension gives three hundred and twenty hertz at the same length? Or, keeping the tension, where should the bridge go on the sixty centimetre wire?",
                 "By the law of tension, T goes as f squared. Three twenty over two fifty six is one point two five, squared is one point five six two five. So the tension must rise to one hundred and fifty six point two five newtons.",
                 "By the law of length, L goes as one over f. Sixty times two fifty six over three twenty, sixty times zero point eight: forty eight centimetres. Shorten the vibrating length by twelve centimetres."], size=36)
        self.quiz("If the tension in a stretched string is made four times, its fundamental frequency becomes",
                  ["half", "twice", "four times", "unchanged"], 1,
                  "Pause and think. Make the tension in a string four times bigger. What happens to the fundamental frequency?",
                  "B, twice. f goes as root T, and root four is two. Four times is the trap: tension sits under a square root.")
        example(self, "A wire 1.0 m long, μ = 5.0 × 10⁻³ kg/m, under 200 N. Find v and f₁. What tension gives 150 Hz? With 200 N restored, where must a bridge go for 250 Hz?",
                [r"v = \sqrt{\frac{200}{5.0\times10^{-3}}} = \sqrt{4.0\times10^{4}} = 200\ \text{m s}^{-1},\quad f_1 = \frac{200}{2\times 1.0} = 100\ \text{Hz}",
                 r"T' = 200\times\left(\frac{150}{100}\right)^{2} = 200\times 2.25 = 450\ \text{N}",
                 r"L' = 1.0\times\frac{100}{250} = 0.40\ \text{m}"],
                ["A full eight mark question to finish. A wire one metre long, with mu equal to five times ten to the minus three kilograms per metre, is under two hundred newtons. Find v and f one, the tension for one hundred and fifty hertz, and the bridge position for two hundred and fifty hertz.",
                 "v is root of two hundred over five times ten to the minus three: root of four times ten to the four, two hundred metres per second. And f one is two hundred over two, one hundred hertz.",
                 "To reach one fifty hertz, multiply the tension by one point five squared, two point two five: four hundred and fifty newtons.",
                 "For two fifty hertz at the original tension, the length must fall by the same ratio: one hundred over two fifty of a metre, forty centimetres from one end."], size=34)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Closed end: displacement node (pressure antinode). Open end: displacement antinode (pressure node).",
            M(r"\text{closed pipe: } f_n = (2n-1)\frac{v}{4L}\ (\text{odd harmonics only})", size=34),
            M(r"\text{open pipe: } f_n = \frac{nv}{2L}\ (\text{all harmonics; an octave above closed})", size=34),
            M(r"e = 0.6r;\ \ v = 2f(l_2 - l_1),\ \ e = \frac{l_2 - 3l_1}{2}", size=34),
            M(r"\text{string: } v = \sqrt{T/\mu},\ \ f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}}\ (\text{all harmonics})", size=34),
            M(r"f \propto \frac{1}{L},\ \ f \propto \sqrt{T},\ \ f \propto \frac{1}{\sqrt{\mu}}", size=36),
        ], "Let us recap. A closed end is a displacement node, an open end an antinode. A closed pipe gives only odd harmonics of v over four L. An open pipe gives all harmonics of v over two L, an octave higher. The end correction is zero point six r, and the resonance tube cancels it: v equals two f, l two minus l one. On a string, v is root T over mu, every harmonic is allowed, and the frequency goes as one over L, root T, and one over root mu.")
        self.outro("That is how pipes and strings choose their notes. Next, we listen more closely: beats, the Doppler effect, loudness and the decibel, in Acoustic Phenomena. See you there, on NEBians.")
