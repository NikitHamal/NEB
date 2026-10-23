import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
from _phys import arrow, clock, curve, example, neby_in, neby_out, readout  # noqa: E402

C_Y, C_P, C_I, C_B, C_F = th.SKY, th.CORAL, th.AMBER, th.MINT, th.PINK


def wavefronts(t, src, period, v, color=th.SKY, maxr=9.0, width=3):
    """Circular wave crests emitted every `period` from the moving source position src(time)."""
    def mk():
        tt = t.get_value()
        g = VGroup()
        k = int(tt / period)
        for i in range(k, -1, -1):
            te = i * period
            r = v * (tt - te)
            if r > maxr:
                break
            if r < 0.02:
                continue
            g.add(Circle(radius=r, stroke_color=color, stroke_width=width, stroke_opacity=max(0.15, 1 - r / maxr)).move_to(src(te)))
        return g
    return always_redraw(mk)


class Lesson(Lesson):
    SUBJECT = "phy"
    GRADE = 12
    UNIT = 9
    TITLE = "Acoustic Phenomena"
    SUBTITLE = "Loudness, pitch, quality and the Doppler effect"
    SECTIONS = ["Pressure amplitude", "Intensity", "Intensity level: the decibel", "Loudness, pitch and quality",
                "The Doppler effect", "Doppler: cases and uses"]
    NEXT = "Unit 10 · Nature and Propagation of Light"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        t = ValueTracker(0)
        v, vs, per = 2.0, 0.9, 0.45
        y0 = 0.4
        src = lambda tt: np.array([-6.5 + vs * tt, y0, 0])
        wf = wavefronts(t, src, per, v, color=th.SKY, maxr=7)
        amb = always_redraw(lambda: VGroup(RoundedRectangle(corner_radius=0.1, width=0.9, height=0.5, fill_color=WHITE, fill_opacity=1, stroke_width=0),
                                           Rectangle(width=0.5, height=0.08, fill_color=th.CORAL, fill_opacity=1, stroke_width=0)).move_to(src(t.get_value())))
        O = np.array([1.0, -1.6, 0])
        you = VGroup(Circle(radius=0.22, fill_color="#E9B48A", fill_opacity=1, stroke_width=0), T("you", size=22).shift(DOWN * 0.45)).move_to(O)
        f0 = 700.0
        vsnd = 340.0

        def fobs():
            s = src(t.get_value())
            d = O - s
            c = d[0] / np.linalg.norm(d)
            return f0 * vsnd / (vsnd - 25.0 * c)
        ro = readout("you hear", fobs, "Hz", size=34, color=th.AMBER).move_to([3.6, 2.4, 0])
        tag = T("an ambulance on the Ring Road; its siren always plays 700 Hz", size=24, color=th.MUTED).to_edge(DOWN, buff=0.4)
        with self.say("An ambulance races along the Ring Road with its siren on. The siren itself always plays exactly the same note. Watch the sound waves it sends out."):
            self.play(FadeIn(tag), FadeIn(you))
            self.add(wf, amb)
            self.play(FadeIn(ro))
            self.play(t.animate.set_value(6.0), run_time=6.0, rate_func=linear)
        with self.say("Ahead of it, the waves are squeezed together. Behind it, they are stretched apart. As it comes towards you the note is high, and the moment it passes, the pitch drops."):
            self.play(t.animate.set_value(11.5), run_time=6.0, rate_func=linear)
        nb = neby_in(self, "surprised", corner=UL)
        q = T("Same siren. Why does the pitch change?", size=32, color=th.AMBER, weight="BOLD").move_to([2.5, 1.5, 0])
        with self.say("Same siren, different note. Why? By the end of this lesson, you will calculate exactly what you hear. On the way, we will also turn everyday words like loud, shrill and sweet into physics you can measure."):
            self.play(FadeIn(q))
            self.play(t.animate.set_value(14.0), run_time=3.0, rate_func=linear)
        self.play(FadeOut(VGroup(tag, you, ro, q)), FadeOut(wf), FadeOut(amb))
        self.remove(wf, amb)
        neby_out(self, nb)
        g, nb = self.title_card()
        with self.say("Welcome to Class 12 Physics, Unit 9: Acoustic Phenomena. Everything you hear, the pitch of a temple bell, the roar of a bus, the whine of a passing ambulance, is a pressure wave arriving at your eardrum."):
            pass
        self.end_title(g, nb)
        self.roadmap("Here is the plan. The pressure amplitude of a sound wave, intensity and the inverse square law, intensity level in decibels, loudness, pitch and quality, and finally the Doppler effect, its cases and its uses.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        t = clock(self, 1.0)
        lam, A = 4.0, 0.35
        k, w = TAU / lam, 1.8
        xs = np.linspace(-6.2, 6.2, 52)
        yl = 2.0
        layers = VGroup(*[Line([x, yl - 0.6, 0], [x, yl + 0.6, 0], color=th.BODY, stroke_width=2.5) for x in xs])

        def upd(m):
            for ln, x in zip(m, xs):
                ln.set_x(x + A * np.sin(w * t.get_value() - k * x))
        layers.add_updater(upd)
        y1, y2 = 0.0, -2.0
        ax1 = Line([-6.3, y1, 0], [6.3, y1, 0], color=th.FAINT, stroke_width=2)
        ax2 = Line([-6.3, y2, 0], [6.3, y2, 0], color=th.FAINT, stroke_width=2)
        disp = always_redraw(lambda: curve(lambda x: y1 + 0.7 * np.sin(w * t.get_value() - k * x), -6.3, 6.3, color=C_Y, width=4))
        pres = always_redraw(lambda: curve(lambda x: y2 + 0.7 * np.cos(w * t.get_value() - k * x), -6.3, 6.3, color=C_P, width=4))
        l1 = T("displacement y", size=22, color=C_Y).move_to([-5.3, y1 + 0.95, 0])
        l2 = T("excess pressure ΔP", size=22, color=C_P).move_to([-5.1, y2 + 0.95, 0])
        with self.say("A sound wave can be described in two ways. By how far the air layers are displaced from their resting places. Or by the excess pressure: how much the pressure rises above, or falls below, the steady atmospheric value."):
            self.add(layers)
            self.play(FadeIn(layers))
            self.add(disp)
            self.play(Create(ax1), FadeIn(disp), FadeIn(l1))
            self.add(pres)
            self.play(Create(ax2), FadeIn(pres), FadeIn(l2))
            self.wait(1)
        t.rate = 0
        guides = VGroup(*[DashedLine([x, yl + 0.8, 0], [x, y2 - 0.9, 0], color=th.MUTED, stroke_width=2) for x in [(w * t.get_value() - PI / 2) / k % lam - 6.0 + lam * j for j in range(3)] if -6.3 < x < 6.3])
        with self.say("Freeze it and compare. Where the layers are crowded together, the displacement is passing through zero, but the pressure is at its peak. The pressure wave is a quarter of a wavelength out of step with the displacement wave."):
            self.play(Create(guides))
            self.wait(2)
        self.play(FadeOut(VGroup(layers, ax1, ax2, l1, l2, guides)), FadeOut(disp), FadeOut(pres))
        layers.clear_updaters()
        self.remove(layers, disp, pres, t)
        title = T("Pressure amplitude", size=34, color=th.INK, weight="BOLD", display=True).to_edge(UP, buff=0.75)
        L = VGroup(M(r"y = a\sin(\omega t - kx)", size=40), M(r"\Delta P = -B\frac{\partial y}{\partial x}", size=40),
                   M(r"\Delta P = Bak\cos(\omega t - kx)", size=40), M(r"P_0 = Bak,\quad B = \rho v^{2},\ k = \frac{\omega}{v}", size=40),
                   M(r"P_0 = \rho v\omega a = 2\pi\rho v f a", size=56, color=C_P)).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.35)
        says = ["Now the derivation. Take a plane wave with displacement y equals a sine, omega t minus k x.",
                "A thin layer of air is stretched or squeezed by the wave. Its volume strain is d y by d x, so by the definition of bulk modulus, the excess pressure is minus B d y by d x.",
                "Differentiate: d y by d x is minus k a cos, omega t minus k x. So delta P is B a k cos, omega t minus k x. Cosine where y has sine: that is the quarter wave shift.",
                "The pressure amplitude is the largest value, B a k. For sound, B equals rho v squared, and k equals omega over v.",
                "Substitute, and P nought equals rho v omega a, or two pi rho v f a. For the same displacement, a higher frequency means a bigger pressure swing."]
        self.play(FadeIn(title))
        for e, sy in zip(L, says):
            with self.say(sy):
                self.play(Write(e), run_time=1.2)
        self.play(FadeOut(VGroup(title, L)))
        ear = VGroup(T("the faintest sound you can hear at 1 kHz:", size=28, color=th.INK),
                     M(r"\Delta P_{\text{rms}} \approx 2\times10^{-5}\ \text{Pa}\quad(\text{one five-thousand-millionth of an atmosphere})", size=34, color=C_P),
                     M(r"a \approx 10^{-11}\ \text{m}\quad(\text{smaller than an atom})", size=38, color=C_Y)).arrange(DOWN, buff=0.4)
        with self.say("And your ear is astonishingly sensitive. At one kilohertz, the faintest sound you can hear has a pressure swing of only about two times ten to the minus five pascals, one five thousand millionth of atmospheric pressure. The air layers move about ten to the minus eleven metres. That is smaller than an atom."):
            self.play(FadeIn(ear[0]))
            self.play(Write(ear[1]))
            self.play(Write(ear[2]))
        nb = neby_in(self, "surprised", corner=DR)
        self.wait(0.5)
        self.play(FadeOut(ear))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        d = self.callout("key", "Intensity: the energy carried per second through unit area held perpendicular to the direction of the wave. Unit: W m⁻².", width=11, size=28)
        d.to_edge(UP, buff=0.8)
        eq = M(r"I = \tfrac12\rho v\omega^{2}a^{2} = 2\pi^{2}\rho v f^{2}a^{2} = \frac{P_0^{2}}{2\rho v}", size=46).next_to(d, DOWN, buff=0.5)
        b1 = Brace(eq[0][7:11], DOWN, color=C_I)
        with self.say("The intensity of sound at a point is the energy the wave carries per second, through one square metre held perpendicular to its direction. Its unit is the watt per square metre."):
            self.play(FadeIn(d, shift=DOWN * 0.2))
        with self.say("For a plane wave, it works out to half rho v omega squared a squared, which is also P nought squared over two rho v. So intensity depends on the square of the amplitude, and the square of the frequency. Double the amplitude, and you get four times the intensity."):
            self.play(Write(eq))
        self.play(FadeOut(VGroup(d, eq)))
        O = np.array([-4.6, -0.3, 0])
        rays = VGroup(*[Line(O, O + 9.5 * np.array([np.cos(a), np.sin(a), 0]), color=th.FAINT, stroke_width=2) for a in np.linspace(-0.32, 0.32, 5)])
        src = Dot(O, color=C_I, radius=0.14)
        rr = ValueTracker(1.0)
        unit = 2.6
        sq = VGroup()
        for n, c in zip((1, 2, 3), (C_I, C_P, C_F)):
            h = 2 * n * unit * np.sin(0.16)
            sq.add(Rectangle(width=0.18, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.3).move_to(O + RIGHT * n * unit))
        lbl = VGroup(*[T(f"{n * n} ×  area", size=20, color=c).next_to(sq[n - 1], DOWN, buff=0.12) for n, c in zip((1, 2, 3), (C_I, C_P, C_F))])
        rl = VGroup(*[M(s, size=28, color=th.MUTED).next_to(sq[i], UP, buff=0.12) for i, s in enumerate(("r", "2r", "3r"))])
        with self.say("Now think of a small source sending sound out equally in all directions. The same energy every second flows out through bigger and bigger spheres."):
            self.play(FadeIn(src), Create(rays))
            self.play(FadeIn(sq[0]), FadeIn(rl[0]), FadeIn(lbl[0]))
        with self.say("At twice the distance, the same energy is spread over four times the area. At three times the distance, nine times the area."):
            self.play(TransformFromCopy(sq[0], sq[1]), FadeIn(rl[1]), FadeIn(lbl[1]))
            self.play(TransformFromCopy(sq[1], sq[2]), FadeIn(rl[2]), FadeIn(lbl[2]))
        law = M(r"I = \frac{P}{4\pi r^{2}}\ \ \Rightarrow\ \ I \propto \frac{1}{r^{2}}", size=48, color=C_I).move_to([3.4, 2.4, 0])
        with self.say("The sphere's area is four pi r squared, so I equals P over four pi r squared. Intensity falls as one over r squared. That is the inverse square law, and it is why you have to stand close to hear someone speaking softly."):
            self.play(Write(law))
        self.play(FadeOut(VGroup(rays, src, sq, lbl, rl, law)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        e = ValueTracker(-12.0)
        ladder = [(-12, "threshold of hearing", 0), (-10, "rustling leaves, whisper", 20), (-8, "quiet room at night", 40), (-6, "normal conversation", 60),
                  (-4, "busy Kathmandu street", 80), (-1, "motorcycle horn at 1 m", 110), (0, "threshold of pain", 120)]
        y_of = lambda ex: -2.7 + (ex + 12) * 0.42
        bar = Line([-1.0, y_of(-12), 0], [-1.0, y_of(0), 0], color=th.FAINT, stroke_width=8)
        rows = VGroup()
        for ex, nm, db in ladder:
            y = y_of(ex)
            rows.add(VGroup(Line([-1.2, y, 0], [-0.8, y, 0], color=th.BODY, stroke_width=3),
                            M(rf"10^{{{ex}}}" if ex != 0 else "1", size=26, color=C_I).next_to([-1.3, y, 0], LEFT, buff=0.1),
                            T(f"{db} dB", size=22, color=C_B).next_to([-0.7, y, 0], RIGHT, buff=0.1),
                            T(nm, size=22, color=th.BODY).next_to([0.6, y, 0], RIGHT, buff=0.15)))
        mark = always_redraw(lambda: Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.12).rotate(-PI / 2).move_to([-1.55 - 1.2, y_of(e.get_value()), 0]))
        hdr = VGroup(T("I (W/m²)", size=22, color=C_I).move_to([-2.2, 3.0, 0]), T("level", size=22, color=C_B).move_to([-0.2, 3.0, 0]))
        eq = M(r"\beta = 10\log_{10}\frac{I}{I_0}\ \text{dB},\quad I_0 = 10^{-12}\ \text{W m}^{-2}", size=34).move_to([-0.0, 3.0, 0])
        with self.say("The ear can cope with intensities from ten to the minus twelve, the faintest whisper of sound, up to about one watt per square metre, where it starts to hurt. That is a range of a million million. A straight scale is hopeless, so we use a logarithmic one."):
            self.play(Create(bar), LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.1), LaggedStart(*[FadeIn(r[1]) for r in rows], lag_ratio=0.1))
            self.add(mark)
            self.play(e.animate.set_value(0), run_time=3)
        with self.say("Taking the threshold of hearing, I nought equal to ten to the minus twelve, as the reference, the intensity level beta is ten log base ten of I over I nought, measured in decibels."):
            self.play(Write(eq))
            self.play(e.animate.set_value(-12), run_time=1.5)
        with self.say("Each factor of ten in intensity adds ten decibels. A whisper is twenty, a conversation sixty, a busy Kathmandu street eighty, a motorcycle horn one hundred and ten, and the threshold of pain one hundred and twenty.") as v_:
            per = (v_.dur - 0.5) / len(rows)
            for (ex, nm, db), r in zip(ladder, rows):
                self.play(e.animate.set_value(ex), FadeIn(r[2]), FadeIn(r[3]), run_time=min(0.8, per))
                self.hold(per - 0.8)
        self.play(FadeOut(VGroup(bar, rows, eq)), FadeOut(mark))
        self.remove(mark)
        self.tip("Doubling I adds 3 dB. Multiplying I by 10 adds 10 dB. Doubling the distance from a point source quarters I, so the level falls by 6 dB.",
                 "Three numbers answer most decibel questions without a calculator. Doubling the intensity adds three decibels, because ten log two is three. Multiplying it by ten adds exactly ten decibels. And doubling your distance from a point source quarters the intensity, so the level falls by six decibels.", state="wink")
        self.quiz("If the intensity of a sound is doubled, its intensity level increases by about",
                  ["2 dB", "3 dB", "6 dB", "10 dB"], 1,
                  "Pause and think. Double the intensity of a sound. By how many decibels does the level go up?",
                  "B, three decibels. Ten log two is about three. Six decibels is the tempting wrong answer: that is what you get for four times the intensity, which is what happens when you halve your distance.")
        example(self, "A sound wave of 1000 Hz in air has displacement amplitude 1.0 × 10⁻⁸ m. With ρ = 1.29 kg/m³ and v = 340 m/s, find the pressure amplitude, the intensity and the intensity level.",
                [r"\rho v = 1.29\times 340 = 438.6,\quad \omega = 2\pi\times 1000 = 6.283\times10^{3}\ \text{rad s}^{-1}",
                 r"P_0 = \rho v\omega a = 438.6\times 6.283\times10^{3}\times 1.0\times10^{-8} = 2.76\times10^{-2}\ \text{Pa}",
                 r"I = \frac{P_0^{2}}{2\rho v} = \frac{7.60\times10^{-4}}{877.2} = 8.66\times10^{-7}\ \text{W m}^{-2}",
                 r"\beta = 10\log_{10}(8.66\times10^{5}) = 10\times 5.94 = 59.4\ \text{dB}"],
                ["Worked example. A one kilohertz sound wave in air has a displacement amplitude of one times ten to the minus eight metres. Find its pressure amplitude, intensity, and intensity level.",
                 "First the pieces. Rho v is one point two nine times three forty, four hundred and thirty eight point six. Omega is two pi times a thousand, six point two eight three times ten to the three.",
                 "Pressure amplitude is rho v omega a: about two point seven six times ten to the minus two pascals.",
                 "Intensity is P nought squared over two rho v: seven point six times ten to the minus four over eight seven seven point two, about eight point six six times ten to the minus seven watts per square metre.",
                 "And the level is ten log of that over ten to the minus twelve: ten log of eight point six six times ten to the five, fifty nine point four decibels. About conversation level, from air layers moving one hundredth of a micrometre."], size=34)
        example(self, "A small loudspeaker radiates 2.0 W uniformly in all directions. Find the intensity and intensity level at 10 m, and the level at 20 m.",
                [r"I = \frac{P}{4\pi r^{2}} = \frac{2.0}{4\pi(10)^{2}} = \frac{2.0}{1256.6} = 1.59\times10^{-3}\ \text{W m}^{-2}",
                 r"\beta = 10\log_{10}(1.59\times10^{9}) = 92.0\ \text{dB}",
                 r"\text{at 20 m: } I \div 4\ \Rightarrow\ \beta' = 92.0 - 6.0 = 86.0\ \text{dB}"],
                ["Now the inverse square law at work. A loudspeaker radiates two watts equally in all directions. Find the intensity and level at ten metres, and the level at twenty metres.",
                 "Intensity is P over four pi r squared: two over twelve fifty six point six, one point five nine times ten to the minus three watts per square metre.",
                 "The level is ten log of one point five nine times ten to the nine: ninety two decibels.",
                 "At twenty metres, double the distance, the intensity is a quarter, so the level drops by six decibels: eighty six. No logarithms needed."], size=38)
        example(self, "The intensity level of a sound is 70 dB. Find its intensity, and the new level if the intensity is increased 100 times.",
                [r"10\log_{10}\frac{I}{I_0} = 70\ \Rightarrow\ \frac{I}{I_0} = 10^{7}\ \Rightarrow\ I = 1.0\times10^{-5}\ \text{W m}^{-2}",
                 r"\times 100 = \times 10^{2}\ \Rightarrow\ +20\ \text{dB}\ \Rightarrow\ \beta' = 90\ \text{dB}"],
                ["And backwards. A sound has an intensity level of seventy decibels. What is its intensity? And what happens if the intensity is made a hundred times bigger?",
                 "Seventy decibels means I over I nought is ten to the seven. So I is ten to the seven times ten to the minus twelve: ten to the minus five watts per square metre.",
                 "A hundred is ten squared, so it adds twenty decibels: ninety decibels. A hundred times the intensity, but only twenty more decibels."], size=40)
        example(self, "A point source emits 0.50 W uniformly. Find the intensity and intensity level at 5.0 m. At what distance does the level fall to 60 dB?",
                [r"I = \frac{0.50}{4\pi(5.0)^{2}} = \frac{0.50}{314.16} = 1.59\times10^{-3}\ \text{W m}^{-2},\quad \beta = 92.0\ \text{dB}",
                 r"60\ \text{dB}:\ I' = 10^{6}I_0 = 1.0\times10^{-6}\ \text{W m}^{-2}",
                 r"r'^{2} = \frac{P}{4\pi I'} = \frac{0.50}{4\pi\times10^{-6}} = 3.979\times10^{4}\ \text{m}^{2}\ \Rightarrow\ r' = 199\ \text{m}"],
                ["A full long question. A point source emits half a watt in all directions. Find the intensity and level at five metres, and the distance at which the level falls to sixty decibels.",
                 "At five metres: zero point five over four pi times twenty five, one point five nine times ten to the minus three watts per square metre. That is ninety two decibels again.",
                 "Sixty decibels means ten to the six times I nought: ten to the minus six watts per square metre.",
                 "So r squared is P over four pi I dash: about three point nine eight times ten to the four, and r is about one hundred and ninety nine metres. From ninety two decibels to sixty, a factor of about sixteen hundred in intensity, between five metres and two hundred. That is the inverse square law at work."], size=36)

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=5.4, y_length=3.6, tips=False, axis_config={"color": th.MUTED, "include_ticks": False}).move_to([-3.2, 0.0, 0])
        xl = T("intensity I", size=22, color=C_I).next_to(ax.x_axis, DOWN, buff=0.2)
        yl = T("loudness felt", size=22, color=C_B).next_to(ax.y_axis, UP, buff=0.1)
        lc = ax.plot(lambda x: 4.2 * np.log10(1 + 6 * x), x_range=[0, 10], color=C_B, stroke_width=5)
        lin = DashedVMobject(ax.plot(lambda x: x, x_range=[0, 10], color=th.MUTED, stroke_width=2), num_dashes=30)
        eq = M(r"L = k\log_{10} I", size=48, color=C_B).move_to([3.2, 1.6, 0])
        nm = T("Weber–Fechner law", size=24, color=th.MUTED).next_to(eq, DOWN, buff=0.2)
        with self.say("Loudness is something different. It is the sensation in your ear. It grows with intensity, but not in proportion. By the Weber Fechner law, the sensation goes as the logarithm of the stimulus: L equals k log I. Ten times the intensity does not sound ten times as loud."):
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(lin))
            self.play(Create(lc))
            self.play(Write(eq), FadeIn(nm))
        more = para("Loudness also depends on frequency: the ear is most sensitive between about 1 kHz and 5 kHz, so a 100 Hz note and a 3 kHz note of equal intensity do not sound equally loud.", width=5.6, size=24, color=th.BODY).move_to([3.4, -1.0, 0])
        with self.say("It also depends on frequency. Your ear is most sensitive between about one and five kilohertz. So a deep hundred hertz hum and a three kilohertz whistle with the same intensity do not sound equally loud."):
            self.play(FadeIn(more))
        self.play(FadeOut(VGroup(ax, xl, yl, lc, lin, eq, nm, more)))
        cau = self.callout("careful", "Intensity is physical (W m⁻²). Intensity level is β = 10 log(I/I₀) in dB. Loudness is a sensation, measured in phon or sone. Never write loudness = 10 log(I/I₀).", width=11, size=28)
        with self.say("So keep three things apart. Intensity is physical, in watts per square metre. Intensity level is ten log I over I nought, in decibels. Loudness is a sensation, measured in phon or sone. A sound can be perfectly measurable and yet completely inaudible, like an ultrasonic whistle."):
            self.play(FadeIn(cau, shift=UP * 0.2))
        self.play(FadeOut(cau))
        t = clock(self, 1.0)
        lo = always_redraw(lambda: curve(lambda x: 1.6 + 0.6 * np.sin(2.0 * x - 3 * t.get_value()), -6.3, 0.2, color=C_Y, width=4))
        hi = always_redraw(lambda: curve(lambda x: 1.6 + 0.6 * np.sin(6.0 * x - 9 * t.get_value()), 0.6, 6.3, color=C_F, width=4))
        ll = VGroup(T("low frequency: low pitch", size=22, color=C_Y).move_to([-3.0, 2.6, 0]), T("high frequency: high pitch", size=22, color=C_F).move_to([3.4, 2.6, 0]))
        band = VGroup()
        bx = lambda f: -5.6 + 11.2 * (np.log10(f) - 0) / 6
        for a, b, c, nm in [(1, 20, th.FAINT, "infrasonic"), (20, 20000, C_B, "audible 20 Hz – 20 kHz"), (20000, 1e6, th.FAINT, "ultrasonic")]:
            r = Rectangle(width=bx(b) - bx(a), height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.6).move_to([(bx(a) + bx(b)) / 2, -1.0, 0])
            band.add(VGroup(r, T(nm, size=20, color=th.INK).move_to(r)))
        ex = VGroup(T("earthquakes, elephants", size=18, color=th.MUTED).next_to(band[0], DOWN, buff=0.15), T("bats, dolphins, medical scans", size=18, color=th.MUTED).next_to(band[2], DOWN, buff=0.15))
        ticks = VGroup(*[T(s, size=18, color=th.MUTED).move_to([bx(f), -1.55 if False else -0.55, 0]) for f, s in ((20, "20 Hz"), (20000, "20 kHz"))])
        with self.say("Pitch is how high or low a note sounds, and it is set by frequency. The higher the frequency, the higher the pitch. A normal ear hears from about twenty hertz to twenty thousand hertz. Below that is infrasonic, like earthquake rumbles and elephant calls. Above it is ultrasonic, used by bats and dolphins, and in medical scanning."):
            self.add(lo, hi)
            self.play(FadeIn(lo), FadeIn(hi), FadeIn(ll))
            self.play(LaggedStart(*[FadeIn(b) for b in band], lag_ratio=0.3), FadeIn(ticks))
            self.play(FadeIn(ex))
        self.play(FadeOut(VGroup(ll, band, ex, ticks)), FadeOut(lo), FadeOut(hi))
        self.remove(lo, hi, t)
        self.quality()

    def quality(self):
        title = T("Quality: same note, different instruments", size=30, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        amps = {"bansuri": [1.0, 0.12, 0.05, 0.0, 0.0, 0.0], "sarangi": [1.0, 0.7, 0.55, 0.45, 0.3, 0.2]}
        t = clock(self, 0.6)
        rows = VGroup()
        for i, (nm, a) in enumerate(amps.items()):
            y = 1.1 - i * 2.6
            wav = always_redraw(lambda a=a, y=y, i=i: curve(lambda x: y + 0.32 * sum(ai * np.sin((n + 1) * (2.4 * x - 4 * t.get_value()) + n) for n, ai in enumerate(a)), -6.0, 1.4, n=300, color=[C_Y, C_I][i], width=4))
            bars = VGroup(*[Rectangle(width=0.3, height=max(0.02, 1.4 * ai), stroke_width=0, fill_color=[C_Y, C_I][i], fill_opacity=0.9).move_to([2.6 + n * 0.55, y - 0.7, 0], aligned_edge=DOWN) for n, ai in enumerate(a)])
            lab = T(nm, size=26, color=[C_Y, C_I][i], weight="BOLD").move_to([-5.2, y + 1.0, 0])
            hl = T("1  2  3  4  5  6", size=18, color=th.MUTED).next_to(bars, DOWN, buff=0.1)
            rows.add(VGroup(wav, bars, lab, hl))
        sl = T("harmonics present", size=20, color=th.MUTED).move_to([4.0, 2.4, 0])
        with self.say("Play the same note, at the same loudness, on a bansuri and a sarangi. You can still tell them apart instantly. Why? A real instrument makes the fundamental plus a set of overtones. The flute's note is almost pure fundamental, a smooth wave."):
            self.play(FadeIn(title), FadeIn(sl))
            self.add(rows[0][0])
            self.play(FadeIn(rows[0][0]), FadeIn(rows[0][2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[0][1]], lag_ratio=0.1), FadeIn(rows[0][3]))
        with self.say("The bowed string adds strong overtones, and the waveform becomes jagged and complex. The number of overtones and their relative intensities fix the shape of the wave, and that shape is the quality, or timbre, of the note."):
            self.add(rows[1][0])
            self.play(FadeIn(rows[1][0]), FadeIn(rows[1][2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[1][1]], lag_ratio=0.1), FadeIn(rows[1][3]))
            self.wait(1.5)
        self.play(FadeOut(VGroup(title, sl)), *[FadeOut(r) for r in rows])
        self.remove(*[r[0] for r in rows], t)
        tbl = [("Characteristic", "Physical quantity", "Depends on"), ("loudness", "intensity", "amplitude², 1/r², the ear"), ("pitch", "frequency", "the fundamental frequency"),
               ("quality", "waveform", "number and strength of overtones")]
        grid = VGroup()
        for i, r in enumerate(tbl):
            row = VGroup(*[T(c, size=26 if i else 26, color=(th.MUTED if i == 0 else [C_B, C_I, th.BODY][j]), weight="BOLD" if i == 0 else "NORMAL") for j, c in enumerate(r)])
            for j, x in enumerate([-4.4, -1.0, 3.2]):
                row[j].move_to([x, 1.6 - i * 0.9, 0])
            grid.add(row)
        with self.say("So the three characteristics you can hear each match one physical quantity. Loudness goes with intensity. Pitch goes with frequency. And quality goes with the waveform, that is, with the overtones present.") as v_:
            for r in grid:
                self.play(FadeIn(r, shift=UP * 0.15), run_time=0.5)
                self.hold(v_.dur / 4 - 0.6)
        self.play(FadeOut(grid))
        self.quiz("The quality of a musical note depends on",
                  ["frequency", "amplitude", "its overtones", "speed of sound"], 2,
                  "Pause and think. What decides the quality of a musical note?",
                  "C, the number and intensity of its overtones, because they fix the shape of the waveform. Frequency decides the pitch, and amplitude decides the loudness. Those are the other two characteristics, not quality.")

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        d = self.callout("key", "Doppler effect: the apparent change in frequency when the source, the observer, or both move relative to the medium. The source's own frequency never changes; only the frequency received does.", width=11.5, size=26)
        with self.say("The Doppler effect is the apparent change in frequency when the source, the observer, or both, move relative to the medium. The source never changes its own frequency. Only the frequency received changes."):
            self.play(FadeIn(d, shift=UP * 0.2))
        self.play(FadeOut(d))
        t = ValueTracker(0)
        v, vs, per = 2.0, 0.8, 0.9
        y0 = 0.6
        S0 = np.array([-4.0, y0, 0])
        src = lambda tt: S0 + RIGHT * vs * tt
        wf = wavefronts(t, src, per, v, color=th.SKY, maxr=8)
        sdot = always_redraw(lambda: Dot(src(t.get_value()), color=C_I, radius=0.14))
        obs = VGroup(Circle(radius=0.2, fill_color="#E9B48A", fill_opacity=1, stroke_width=0), T("observer", size=20).shift(DOWN * 0.42)).move_to([5.6, y0, 0])
        with self.say("Case one: the source moves towards an observer who stands still. The source sends out a crest once every period, T. In that time the crest travels v T, but the source itself moves v s T forward, chasing its own wave."):
            self.add(wf, sdot)
            self.play(FadeIn(obs))
            self.play(t.animate.set_value(4.5 * per), run_time=5.5, rate_func=linear)
        tt = t.get_value()
        k = int(tt / per)
        ahead = [src(i * per)[0] + v * (tt - i * per) for i in (k, k - 1)]
        behind = [src(i * per)[0] - v * (tt - i * per) for i in (k, k - 1)]
        b1 = BraceBetweenPoints([min(ahead), y0 - 0.1, 0], [max(ahead), y0 - 0.1, 0], DOWN, color=C_P)
        b1l = M(r"\lambda' = \frac{v - v_s}{f}", size=32, color=C_P).next_to(b1, DOWN, buff=0.08)
        b2 = BraceBetweenPoints([min(behind), y0 - 0.1, 0], [max(behind), y0 - 0.1, 0], DOWN, color=C_Y)
        b2l = M(r"\frac{v + v_s}{f}", size=32, color=C_Y).next_to(b2, DOWN, buff=0.08)
        with self.say("So in front of the source, the crests are packed closer: the wavelength becomes v T minus v s T, which is v minus v s, over f. Behind it, they are spread out."):
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        self.play(FadeOut(VGroup(b1, b1l, b2, b2l, obs)), FadeOut(wf), FadeOut(sdot))
        self.remove(wf, sdot)
        title = T("Deriving the Doppler formula", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        L = VGroup(M(r"\text{source approaches: } \lambda' = \frac{v - v_s}{f}\ \Rightarrow\ f' = \frac{v}{\lambda'} = \frac{v}{v - v_s}f", size=38),
                   M(r"\text{observer approaches: } f' = \frac{v + v_o}{\lambda} = \frac{v + v_o}{v}f", size=38),
                   M(r"f' = \left(\frac{v + v_o}{v - v_s}\right)f", size=64, color=C_I)).arrange(DOWN, buff=0.55).next_to(title, DOWN, buff=0.5)
        with self.say("The observer is at rest, so the waves still reach her at speed v. Frequency is speed over wavelength: f dash equals v over v minus v s, times f. The note is raised."):
            self.play(FadeIn(title), Write(L[0]))
        with self.say("Case two: the source is still, and the observer runs towards it at v o. The wavelength is unchanged, but she runs into the crests, meeting them at speed v plus v o. So f dash equals v plus v o, over v, times f."):
            self.play(Write(L[1]))
        with self.say("Combine the two, and you get the general Doppler formula: f dash equals v plus v o, over v minus v s, times f."):
            self.sfx("impact", gain=-12)
            self.play(Write(L[2]))
            self.play(Circumscribe(L[2], color=C_I))
        self.play(FadeOut(VGroup(L[0], L[1])), L[2].animate.next_to(title, DOWN, buff=0.5))
        rule = VGroup(T("One question fixes every sign: does this motion bring them closer?", size=26, color=th.INK, weight="SEMIBOLD"),
                      T("observer moving towards the source: v₀ positive; away: negative", size=24, color=th.BODY),
                      T("source moving towards the observer: vₛ positive; away: negative", size=24, color=th.BODY),
                      T("check: any approach must raise the frequency", size=24, color=C_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(L[2], DOWN, buff=0.6)
        with self.say("Use this one formula always, and fix the signs with one question: does this motion bring them closer? An observer moving towards the source has positive v o; moving away, negative. A source moving towards the observer has positive v s; moving away, negative. And check: any approach must raise the frequency. If your answer says otherwise, a sign is wrong.") as v_:
            for r in rule:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v_.dur / 4 - 0.7)
        nb = neby_in(self, "think", corner=DR)
        self.wait(0.4)
        self.play(FadeOut(VGroup(title, L[2], rule)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        title = T("The six cases", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        cases = [("source approaches", r"\frac{v}{v - v_s}f"), ("source recedes", r"\frac{v}{v + v_s}f"), ("observer approaches", r"\frac{v + v_o}{v}f"),
                 ("observer recedes", r"\frac{v - v_o}{v}f"), ("both approach", r"\frac{v + v_o}{v - v_s}f"), ("both recede", r"\frac{v - v_o}{v + v_s}f")]
        cards = VGroup()
        for i, (nm, f) in enumerate(cases):
            box = self.panel(3.9, 1.7)
            g = VGroup(T(nm, size=22, color=[C_P, C_Y][i % 2]), M(f, size=40)).arrange(DOWN, buff=0.15).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.3, 0.3)).next_to(title, DOWN, buff=0.4)
        with self.say("Here are all six cases, each just the general formula with the right signs. Source approaching or receding, observer approaching or receding, and both together. Approaching raises the pitch; receding lowers it.") as v_:
            self.play(FadeIn(title))
            for c in cards:
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
                self.hold(v_.dur / 6 - 0.6)
        self.play(FadeOut(VGroup(title, cards)))
        self.no_shift()
        self.uses()
        example(self, "A train approaching a station sounds a 640 Hz whistle while moving at 20 m/s (v = 340 m/s). Find the frequency heard on the platform as it approaches and after it passes.",
                [r"\text{approaching: } f' = \frac{340}{340 - 20}\times 640 = \frac{340}{320}\times 640 = 680\ \text{Hz}",
                 r"\text{receding: } f'' = \frac{340}{340 + 20}\times 640 = \frac{340}{360}\times 640 = 604.4\ \text{Hz}",
                 r"\text{drop} = 680 - 604.4 = 75.6\ \text{Hz}"],
                ["Worked example. A train approaching a station sounds a six hundred and forty hertz whistle, moving at twenty metres per second. What does a passenger on the platform hear, as it approaches and after it passes?",
                 "Approaching: three forty over three forty minus twenty, three forty over three twenty, times six forty. Six hundred and eighty hertz.",
                 "After it passes, the source recedes: three forty over three sixty, times six forty. About six hundred and four point four hertz.",
                 "The pitch drops by seventy five point six hertz as the train goes by. More than a whole musical tone, exactly what you hear at the station. And the same physics as our ambulance."], size=38)
        example(self, "A jeep sounding a 400 Hz horn travels at 20 m/s on the Prithvi Highway; a motorcycle comes towards it at 15 m/s (v = 340 m/s). Find the frequency the motorcyclist hears.",
                [r"v_o = +15,\quad v_s = +20\quad(\text{both approach})",
                 r"f' = \frac{340 + 15}{340 - 20}\times 400 = \frac{355}{320}\times 400 = 443.8\ \text{Hz}"],
                ["Both moving. A jeep with a four hundred hertz horn drives at twenty metres per second along the Prithvi Highway, and a motorcycle comes towards it at fifteen. What does the rider hear?",
                 "Both motions bring them closer, so both signs are positive: v o is plus fifteen, v s is plus twenty.",
                 "f dash is three fifty five over three twenty, times four hundred: about four hundred and forty four hertz. The horn sounds forty four hertz sharper than it really is."], size=40)
        example(self, "A whistle of frequency 500 Hz is sounded on a car moving away from a stationary listener at 25 m/s (v = 340 m/s). Find the frequency heard.",
                [r"v_s = -25\ (\text{recedes}):\quad f' = \frac{340}{340 + 25}\times 500 = \frac{340}{365}\times 500 = 465.8\ \text{Hz}"],
                ["One more, moving away. A car with a five hundred hertz whistle drives away from a listener at twenty five metres per second.",
                 "The source recedes, so v s is minus twenty five. f dash equals three forty over three sixty five, times five hundred: about four hundred and sixty six hertz. Lower, as it must be for a receding source."], size=42)
        self.quiz("A source and an observer move with the same velocity in the same direction. The apparent frequency is",
                  ["greater than f", "less than f", "equal to f", "zero"], 2,
                  "Last check. A source and an observer move with the same velocity, in the same direction. What frequency is heard? Pause and think.",
                  "C, equal to f. Their separation never changes, so no crests are gained or lost on the way. The Doppler effect needs a change in separation along the line joining them.")

    def no_shift(self):
        title = T("When there is no Doppler shift", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        items = VGroup(
            T("1.  same velocity, same direction: the separation never changes", size=26, color=th.BODY),
            T("2.  motion perpendicular to the line joining them, at that instant", size=26, color=th.BODY),
            T("3.  a steady wind, with source and observer at rest: v and λ change in the same ratio", size=26, color=th.BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        if items.width > 12.4:
            items.scale_to_fit_width(12.4)
        items.next_to(title, DOWN, buff=0.6)
        with self.say("Relative motion does not always mean a shift. If the source and observer move with the same velocity in the same direction, their separation stays constant, and f dash equals f. At the instant a train passes you broadside, moving at right angles to the line joining you, there is no shift either. And a steady wind changes nothing for a source and observer at rest, because it changes the speed of sound and the wavelength in exactly the same proportion.") as v_:
            self.play(FadeIn(title))
            for it in items:
                self.play(FadeIn(it, shift=RIGHT * 0.2), run_time=0.6)
                self.hold(v_.dur / 3 - 0.7)
        self.play(FadeOut(VGroup(title, items)))

    def uses(self):
        title = T("The Doppler effect at work", size=32, color=th.INK, weight="BOLD").to_edge(UP, buff=0.75)
        items = [("Speed guns", "traffic police bounce waves off a car and measure the shift", th.CORAL),
                 ("SONAR", "the speed of a submarine or a shoal of fish", th.SKY),
                 ("Doppler ultrasound", "the speed of blood in an artery (echocardiography)", th.MINT),
                 ("Red shift", "light from distant galaxies is shifted: the universe is expanding", th.PINK)]
        cards = VGroup()
        for h, b, c in items:
            box = self.panel(5.7, 1.9)
            g = VGroup(T(h, size=28, color=c, weight="BOLD"), para(b, width=5.0, size=22, color=th.BODY)).arrange(DOWN, buff=0.15).move_to(box)
            cards.add(VGroup(box, g))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).next_to(title, DOWN, buff=0.45)
        with self.say("And it is everywhere. Traffic police speed guns, and weather radar. SONAR, to find the speed of a submarine or a shoal of fish. Doppler ultrasound, to measure the speed of blood in an artery. And in astronomy, the red shift of light from distant galaxies, which is our evidence that the universe is expanding.") as v_:
            self.play(FadeIn(title))
            for c in cards:
                self.sfx("pop", gain=-14)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
                self.hold(v_.dur / 4 - 0.6)
        nb = neby_in(self, "cool", corner=DR)
        self.wait(0.3)
        self.play(FadeOut(VGroup(title, cards)))
        neby_out(self, nb)

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            M(r"\Delta P = -B\frac{\partial y}{\partial x},\ \ P_0 = Bak = \rho v\omega a;\ \text{pressure is } \tfrac{\lambda}{4} \text{ out of step}", size=32),
            M(r"I = \tfrac12\rho v\omega^{2}a^{2} = \frac{P_0^{2}}{2\rho v};\quad I = \frac{P}{4\pi r^{2}} \propto \frac{1}{r^{2}}", size=34),
            M(r"\beta = 10\log_{10}\frac{I}{I_0},\ I_0 = 10^{-12};\ \ \times 2 \to +3\ \text{dB},\ \times 10 \to +10\ \text{dB}", size=32),
            "Loudness is a sensation (L = k log I); pitch is set by frequency; quality by the overtones.",
            M(r"f' = \frac{v + v_o}{v - v_s}f\quad(\text{signs positive when approaching})", size=36),
            "No shift for equal velocities, perpendicular motion, or a steady wind.",
        ], "Let us recap. The pressure amplitude is rho v omega a, and the pressure wave is a quarter wavelength out of step with displacement. Intensity goes as amplitude squared and frequency squared, and falls as one over r squared. Intensity level is ten log I over I nought: double the intensity for three more decibels. Loudness is a sensation, pitch is frequency, and quality is set by the overtones. And the Doppler formula is f dash equals v plus v o, over v minus v s, times f, with approach counted positive.")
        self.outro("That completes our study of sound. Next, we turn to light: what it is, and how it travels, in Nature and Propagation of Light. See you there, on NEBians.")
