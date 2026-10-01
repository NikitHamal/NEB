"""Class 11 Physics, Unit 1: Physical Quantities.

An animated explainer built from ``notes/content/phy11/unit-01.md``.  Every
number, rule and figure on screen is that chapter's, in that chapter's order:
measurement and units, accuracy and precision, errors, significant figures,
combining uncertainties, and dimensional analysis.

The narration lives in ``NARRATION`` in ``tools/manim/make_narration.py``; the
durations it produces land in ``timings.json`` next to this file, and
``NebEpisode.beat`` holds each picture for exactly as long as its own line of
voice-over.  ``lead`` on a beat is a deliberate pause before the animation, used
so an accent lands in the middle of a long sentence rather than at its start.

    tools/manim/scripts/render.sh videos/phy11_unit01.py PhysicalQuantities -qh
"""

from __future__ import annotations

import os

from manim import (
    Arrow,
    DOWN,
    FadeIn,
    Line,
    FadeOut,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Circumscribe,
    Create,
    Indicate,
    TransformMatchingTex,
    VGroup,
    Write,
)

from neb import components as C
from neb.mathtext import NebMathTex
from neb.theme import (
    ACCENT,
    ACCENT_STRONG,
    BODY_SIZE,
    CONTENT_W,
    HIGHLIGHT_CYCLE,
    LEFT_EDGE,
    NebEpisode,
    SMALL_SIZE,
    SURFACE_RAISED,
    TEXT,
    TEXT_MUTED,
    TEXT_SECOND,
    T_BEAT,
    T_SLOW,
    VIOLET,
    WARN,
)

# ── The voice-over ─────────────────────────────────────────────────────────
# One entry per beat; the key matches the ``beat(key, ...)`` calls in
# ``construct``.  Written as spoken English, not as a transcript: contractions,
# spoken numbers ("zero point zero zero two five zero"), and the pauses a
# reader needs in order to follow a formula.
NARRATION = {
    "s0": "Every law of physics began as a number read off an instrument. "
    "And that number is never exact. This unit is about how much of a "
    "measured number you are entitled to believe — the language of "
    "precision, error and significant figures — and about the hidden "
    "structure every physical quantity carries with it: its dimensions.",
    "s1": "A physical quantity is any property of matter, or of a phenomenon, "
    "that can be measured. Measuring it means comparing it with a standard, "
    "so every measurement is a numerical value multiplied by a unit. "
    "Q equals n times u. For a given quantity, the product n u is fixed — "
    "so a smaller unit always gives a larger number. That one relation is "
    "the whole of unit conversion: n one u one equals n two u two.",
    "s2": "Accuracy is how close a measured value lies to the true or "
    "accepted value. Precision is how close repeated measurements lie to one "
    "another, and how finely the instrument can resolve a reading. The two "
    "are independent: a set of readings can be precise without being accurate "
    "— that is exactly what a zero error looks like — and accurate on "
    "average without being precise.",
    "s3": "Precision is capped by the least count of the instrument: the "
    "smallest change it can display. For a vernier calliper, ten vernier "
    "divisions span nine millimetres, so the least count is one tenth of a "
    "millimetre. Here the vernier zero lies past thirteen millimetres, and "
    "its fourth division coincides — so the reading is thirteen plus four "
    "times zero point one: thirteen point four millimetres.",
    "s4": "There are two kinds of error, and they need opposite remedies. "
    "A systematic error comes from a faulty instrument, a zero error, a wrong "
    "technique or personal bias; it always goes the same way, and it spoils "
    "accuracy. A random error comes from unpredictable fluctuations — "
    "judgement, draughts, supply ripple; it goes either way, and it spoils "
    "precision. Calibrate to remove the first; repeat and average to reduce "
    "the second.",
    "s5": "Measure a quantity n times, and the best estimate is the "
    "arithmetic mean. Then the mean absolute deviation is the average "
    "distance of each reading from that mean, and the result is quoted as "
    "a equals a-bar, plus or minus, delta a-mean. The relative error divides "
    "that uncertainty by the mean; the percentage error multiplies it by a "
    "hundred.",
    "s6": "The significant figures of a measured value are all the digits "
    "known with certainty, together with the first digit that is uncertain. "
    "They record the precision of the measurement, not its size. All "
    "non-zero digits count. Zeros between non-zero digits count. Leading "
    "zeros never count — they are only place-holders. Trailing zeros after "
    "a decimal point do count, because they were actually measured.",
    "s7": "Trailing zeros in a whole number are ambiguous, so write the number "
    "in standard form. Changing the unit never changes the count. And exact "
    "numbers — twelve eggs, or pi — have infinitely many. So in zero point "
    "zero zero two five zero, the two, the five and the final zero are the "
    "significant figures: three of them. Never drop a trailing zero: two "
    "point five centimetres and two point five zero centimetres are different "
    "claims about the instrument.",
    "s8": "Rounding off: if the digit to be dropped is less than five, leave "
    "the preceding digit alone; greater than five, raise it by one; exactly "
    "five with nothing after it, round so the preceding digit becomes even. "
    "Then arithmetic — and this is where marks are lost. Addition and "
    "subtraction keep as many decimal places as the term with the fewest. "
    "Multiplication and division keep as many significant figures as the "
    "factor with the fewest.",
    "s9": "So: three point one four metres, plus two point seven metres, plus "
    "zero point five eight six metres. The exact sum is six point four two "
    "six. How many decimal places does the answer keep? One — because two "
    "point seven has only one. The answer is six point four metres. Notice it "
    "is not rounded to two significant figures: the decimal-place rule "
    "governs addition.",
    "s10": "When you combine measurements, the errors combine too, and the "
    "rule depends on the operation. For a sum or a difference, absolute "
    "errors add. For a product or a quotient, relative errors add. And for a "
    "product of powers, each relative error is weighted by its power. Errors "
    "never cancel, because we do not know which way each one went: push both "
    "measurements to the worst possible end of their range, and the errors "
    "can only pile up.",
    "s11": "The power rule bites hardest. Measure the radius of a sphere to "
    "one percent, and since the volume goes as the radius cubed, the volume "
    "is only good to three percent. So in the laboratory, measure most "
    "carefully the quantity that carries the highest power. For a radius of "
    "seven point two zero, plus or minus zero point zero five centimetres, "
    "the volume is one point five six, plus or minus zero point zero three, "
    "times ten to the three cubic centimetres.",
    "s12": "Every physical quantity carries a hidden structure: its dimensions "
    "— the powers to which the base quantities must be raised in order to "
    "represent it. Force is mass times acceleration, so its dimensional "
    "formula is M L T to the minus two. And the principle of homogeneity says "
    "only quantities of the same dimensions may be added, subtracted or "
    "equated — so every term on both sides of a correct physical equation "
    "must have the same dimensional formula.",
    "s13": "That gives three tools. First, checking an equation. Test v "
    "squared equals u squared plus two a s: the left side is L squared T to "
    "the minus two, and so is every term on the right. The equation is "
    "dimensionally correct — although the pure number two is invisible to "
    "this test, so dimensional analysis can prove an equation wrong but never "
    "fully right.",
    "s14": "Second, converting between systems of units. A quantity of "
    "dimensions M to the a, L to the b, T to the c converts as n two equals "
    "n one, times the mass ratio to the a, the length ratio to the b, and the "
    "time ratio to the c. Energy is M L squared T to the minus two, so one "
    "joule is ten cubed times ten to the fourth — ten to the seven ergs. "
    "Bigger units give smaller numbers.",
    "s15": "Third, deriving a relation. The period of a simple pendulum may "
    "depend on its mass, its length and g. Assume a product of powers and "
    "match dimensions on both sides. The power of the mass comes out zero — "
    "the period does not depend on the mass of the bob. That is a real "
    "physical prediction from pure bookkeeping. Experiment, or a full "
    "derivation, supplies the constant two pi.",
    "s16": "The limits: it cannot supply dimensionless constants, like the "
    "two pi. It fails if the quantity depends on more than three base "
    "quantities. It cannot build an equation that is a sum of terms, only "
    "check one. And it cannot separate quantities with the same dimensions — "
    "work and torque are both M L squared T to the minus two. The worked "
    "examples and the practice questions are in the chapter notes.",
}


class PhysicalQuantities(NebEpisode):
    subject_line = "Class 11 Physics · Unit 1"
    episode_title = "Physical Quantities"
    total_sections = 10

    # ── helpers ────────────────────────────────────────────────────────────
    def top(self, mobject, buff: float = 0.15):
        """Park a mobject just under the section header."""
        return mobject.next_to(self._header, DOWN, buff=buff)

    def build_header(self, title: str, section_kicker: str):
        self._header = self.open_section(title, section_kicker)

    def centre_stage(self, *mobjects):
        group = VGroup(*mobjects).arrange(DOWN, buff=0.5)
        group.move_to([0, -0.15, 0])
        return group

    # ── the episode ────────────────────────────────────────────────────────
    def construct(self):
        # 0 ── cold open ────────────────────────────────────────────────────
        title = C.title_card(
            "CLASS 11 PHYSICS · UNIT 1",
            "Physical Quantities",
            "Significant figures, error and dimensions",
        )
        hook = C.prose(
            "Every law of physics began as a number read off an instrument.",
            size=30,
            color=TEXT_SECOND,
            width=9.5,
        )
        opening = VGroup(title, hook).arrange(DOWN, buff=0.7)
        opening.move_to([0, -0.1, 0])
        self.beat("s0", [FadeIn(opening, shift=UP * 0.3)], run_time=T_SLOW)

        # 1 ── measurement and units ────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])
        self.build_header("Measurement and units", "§ 1.1")
        nu = C.equation_card(r"Q = n \times u", label="measurement = number × unit", width=6.2)
        conversion = C.equation_card(
            r"n_1 u_1 = n_2 u_2",
            label="the whole of unit conversion",
            width=6.2,
            accent=VIOLET,
        )
        pair = VGroup(nu, conversion).arrange(RIGHT, buff=0.8)
        pair.move_to([0, 1.15, 0])
        self.beat("s1a", [FadeIn(pair, shift=UP * 0.25)], run_time=T_BEAT)

        si = C.table(
            [
                ["Base quantity", "SI unit", "Dimension"],
                ["Length", "metre", "[L]"],
                ["Mass", "kilogram", "[M]"],
                ["Time", "second", "[T]"],
                ["Electric current", "ampere", "[I]"],
                ["Temperature", "kelvin", "[K]"],
                ["Amount of substance", "mole", "[N]"],
                ["Luminous intensity", "candela", "[J]"],
            ],
            font_size=22,
            header_size=22,
            h_buff=0.6,
            v_buff=0.26,
        )
        si.move_to([0, -1.35, 0])
        entries = list(si.get_entries())
        self.play(Create(si.get_horizontal_lines()), run_time=0.5)
        self.beat(
            "s1b",
            [
                AnimationGroup(
                    *[FadeIn(e, shift=RIGHT * 0.12) for e in entries],
                    lag_ratio=0.05,
                )
            ],
            run_time=1.4,
        )
        self.beat("s1c", [], run_time=0.0)
        self.beat(
            "s1c2",
            [Circumscribe(si, color=ACCENT, buff=0.16)],
            run_time=T_SLOW,
            lead=5.9,
        )
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 2 ── accuracy and precision ───────────────────────────────────────
        self.build_header("Accuracy, precision and least count", "§ 1.1")
        target = C.target_diagram(panel_size=1.62)
        target.move_to([0, 0.05, 0])
        self.beat("s2a", [FadeIn(target, shift=UP * 0.25)], run_time=T_SLOW)
        definition = C.callout(
            "ACCURACY vs PRECISION",
            "Accuracy is closeness to the true value. Precision is closeness of "
            "repeated readings, set by the least count. They are independent.",
            width=9.0,
        )
        definition.move_to([0, 0.35, 0])
        self.beat(
            "s2b",
            [FadeOut(target, shift=UP * 0.2), FadeIn(definition, shift=UP * 0.2)],
            run_time=T_BEAT,
        )

        # 3 ── the vernier ──────────────────────────────────────────────────
        self.beat(
            "s2c",
            [FadeOut(definition, shift=UP * 0.2)],
            run_time=T_BEAT,
        )
        vernier = C.vernier(13.4, width=11.0)
        vernier.move_to([0, -0.3, 0])
        reading = NebMathTex(
            r"13 + 4(0.1) = 13.4\ \text{mm}",
            color=TEXT,
            font_size=40,
        )
        reading.move_to([0, 1.6, 0])
        self.beat("s3a", [FadeIn(vernier, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat("s3b", [Write(reading)], run_time=T_BEAT)
        self.beat(
            "s3c",
            [Indicate(vernier.coincidence, color=VIOLET, scale_factor=1.15)],
            run_time=T_BEAT,
        )
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 4 ── errors ───────────────────────────────────────────────────────
        self.build_header("Errors in measurement", "§ 1.1")
        errors = C.table(
            [
                ["", "Systematic", "Random"],
                ["Cause", "faulty instrument, zero error, bias", "judgement, draughts, ripple"],
                ["Sign", "always the same direction", "equally likely either way"],
                ["Effect", "spoils accuracy", "spoils precision"],
                ["Remedy", "calibrate, correct, change method", "repeat and take the mean"],
            ],
            font_size=20,
            header_size=21,
            h_buff=0.6,
            v_buff=0.26,
        )
        errors.move_to([0, 0.6, 0])
        mean = NebMathTex(
            r"\Delta a_{mean} = \frac{1}{n}\sum_{i=1}^{n} \Delta a_i",
            color=TEXT,
            font_size=38,
        )
        quote = NebMathTex(r"a = \bar{a} \pm \Delta a_{mean}", color=ACCENT, font_size=38)
        formulas = VGroup(mean, quote).arrange(DOWN, buff=0.4)
        formulas.move_to([0, -1.5, 0])
        self.beat("s4a", [FadeIn(errors, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat("s4b", [FadeIn(formulas, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat("s5a", [Indicate(quote, color=ACCENT)], run_time=T_BEAT)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 5 ── significant figures: the rules ───────────────────────────────
        self.build_header("Significant figures", "§ 1.1")
        definition = VGroup(
            C.kicker("DEFINITION"),
            C.prose(
                "The digits known with certainty, plus the first uncertain digit.",
                size=28,
                color=TEXT,
                width=10.4,
            ),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        definition.move_to([0, 1.55, 0])
        rules = C.table(
            [
                ["Rule", "Example", "Count"],
                ["All non-zero digits count", "2345", "4"],
                ["Zeros between non-zero digits count", "2.005", "4"],
                ["Leading zeros never count", "0.0025", "2"],
                ["Trailing zeros after a point count", "2.500", "4"],
                ["Trailing zeros in a whole number", "4700 to 4.70e3", "3"],
                ["Changing the unit never changes it", "2.50 cm = 25.0 mm", "3"],
                ["Exact and pure numbers", "12 eggs, 2π", "∞"],
            ],
            font_size=20,
            header_size=20,
            h_buff=0.55,
            v_buff=0.24,
        )
        rules.move_to([0, -0.5, 0])
        self.beat("s6a", [FadeIn(definition, shift=UP * 0.2)], run_time=T_BEAT)
        self.play(Create(rules.get_horizontal_lines()), run_time=0.5)
        self.beat(
            "s6b",
            [
                AnimationGroup(
                    *[FadeIn(e, shift=RIGHT * 0.1) for e in rules.get_entries()],
                    lag_ratio=0.045,
                )
            ],
            run_time=1.5,
        )

        # 6 ── the zeros trap ───────────────────────────────────────────────
        self.beat(
            "s7a",
            [
                FadeOut(definition, shift=UP * 0.2),
                FadeOut(rules, shift=UP * 0.2),
            ],
            run_time=T_BEAT,
        )
        number = C.digits("0.00250", 4, size=72)
        number.move_to([0, 1.2, 0])
        badge = C.chip("3 significant figures")
        badge.move_to([0, -0.35, 0])
        trap = C.callout(
            "ZEROS ARE THE TRAP",
            "Leading zeros are place-holders. The zero in 2.50 was measured, so it "
            "counts. Never drop a trailing zero: 2.5 cm and 2.50 cm are different "
            "claims.",
            width=9.6,
            accent=WARN,
        )
        trap.move_to([0, -1.85, 0])
        self.beat("s7b", [FadeIn(number, shift=UP * 0.2)], run_time=T_BEAT)
        self.beat("s7c", [FadeIn(badge, shift=UP * 0.15)], run_time=T_QUICK if False else T_BEAT)
        self.beat("s7d", [FadeIn(trap, shift=UP * 0.2)], run_time=T_BEAT)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 7 ── rounding and arithmetic ──────────────────────────────────────
        self.build_header("Rounding and arithmetic", "§ 1.1")
        rounding = C.bullets(
            [
                "less than 5: leave the digit alone",
                "greater than 5: raise it by one",
                "exactly 5, nothing after: make it even",
            ],
            size=25,
            buff=0.3,
        )
        rounding_block = VGroup(C.kicker("ROUNDING OFF"), rounding).arrange(
            DOWN, buff=0.26, aligned_edge=LEFT
        )
        arithmetic = C.table(
            [
                ["Operation", "The answer keeps"],
                ["addition, subtraction", "the fewest decimal places"],
                ["multiplication, division", "the fewest significant figures"],
            ],
            font_size=22,
            header_size=22,
            h_buff=0.5,
            v_buff=0.3,
        )
        arithmetic_title = C.kicker("ARITHMETIC")
        arithmetic_block = VGroup(arithmetic_title, arithmetic).arrange(
            DOWN, buff=0.26, aligned_edge=LEFT
        )
        stack = VGroup(rounding_block, arithmetic_block).arrange(DOWN, buff=0.42)
        stack.move_to([0, 0.2, 0])
        self.beat("s8a", [FadeIn(stack, shift=UP * 0.2)], run_time=T_SLOW)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])
        quiz = C.quiz(
            "3.14 m + 2.7 m + 0.586 m = ?",
            ["6.426 m", "6.43 m", "6.4 m", "6 m"],
            2,
            width=9.4,
        )
        quiz.move_to([0, -0.75, 0])
        self.beat("s8b", [FadeIn(quiz, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat("s9a", C.reveal_quiz(quiz), run_time=T_SLOW)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 8 ── combining uncertainties ──────────────────────────────────────
        self.build_header("Combining uncertainties", "§ 1.1")
        sum_rule = C.equation_card(
            r"\Delta Z = \Delta A + \Delta B", width=3.9, font_size=32
        )
        product_rule = C.equation_card(
            r"\frac{\Delta Z}{Z} = \frac{\Delta A}{A} + \frac{\Delta B}{B}",
            width=3.9,
            font_size=32,
            accent=VIOLET,
        )
        power_rule = C.equation_card(
            r"\frac{\Delta Z}{Z} = p\frac{\Delta A}{A} + q\frac{\Delta B}{B}",
            width=3.9,
            font_size=32,
            accent=ACCENT_STRONG,
        )
        rules_row = VGroup(sum_rule, product_rule, power_rule).arrange(RIGHT, buff=0.32)
        rules_row.move_to([0, 1.5, 0])
        self.beat("s10a", [FadeIn(rules_row, shift=UP * 0.25)], run_time=T_SLOW)
        note = C.prose(
            "absolute errors add for sums and differences; relative errors add "
            "for products and quotients, each weighted by its power",
            size=SMALL_SIZE,
            color=TEXT_MUTED,
            width=11.0,
        )
        note.move_to([0, 0.35, 0])
        self.beat("s10a2", [FadeIn(note, shift=UP * 0.15)], run_time=T_BEAT)

        derivation = NebMathTex(
            r"Z_{\max} = (A + \Delta A) + (B + \Delta B) = Z + (\Delta A + \Delta B)",
            color=TEXT,
            font_size=25,
        )
        derivation.move_to([0, -0.55, 0])
        self.beat("s10b", [Write(derivation)], run_time=T_BEAT)
        self.beat(
            "s10b2",
            [Circumscribe(derivation, color=ACCENT, buff=0.22)],
            run_time=T_SLOW,
            lead=2.7,
        )

        radius = C.prose("radius measured to 1 %", size=26, color=TEXT_SECOND)
        volume = C.prose("volume good to 3 %", size=26, color=TEXT)
        arrow = Arrow(LEFT, RIGHT, color=ACCENT, stroke_width=C.stroke(3), buff=0.25)
        chain = VGroup(radius, arrow, volume).arrange(RIGHT, buff=0.55)
        chain.move_to([0, -1.75, 0])
        self.beat("s11a", [FadeIn(chain, shift=UP * 0.2)], run_time=T_BEAT)
        self.beat(
            "s11a2",
            [Indicate(arrow, color=ACCENT, scale_factor=1.35)],
            run_time=T_BEAT,
            lead=2.0,
        )
        self.beat(
            "s11b",
            [Indicate(volume, color=ACCENT, scale_factor=1.12)],
            run_time=T_BEAT,
        )
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 9 ── dimensions ───────────────────────────────────────────────────
        self.build_header("Dimensions and dimensional analysis", "§ 1.2")
        force = NebMathTex(r"[F] = [M][LT^{-2}] = [MLT^{-2}]", color=TEXT, font_size=40)
        force.move_to([0, 1.95, 0])
        homogeneity = C.callout(
            "PRINCIPLE OF HOMOGENEITY",
            "Only quantities of the same dimensions may be added, subtracted or "
            "equated — so every term on both sides of a correct physical equation "
            "must have the same dimensional formula.",
            width=10.6,
        )
        homogeneity.move_to([0, 0.45, 0])
        self.beat("s12a", [FadeIn(force, shift=UP * 0.2)], run_time=T_BEAT)
        self.beat(
            "s12a2",
            [Indicate(force, color=ACCENT, scale_factor=1.06)],
            run_time=T_BEAT,
            lead=2.2,
        )
        self.beat("s12b", [FadeIn(homogeneity, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat(
            "s12b2",
            [Circumscribe(homogeneity, color=ACCENT, buff=0.18)],
            run_time=T_SLOW,
            lead=4.0,
        )
        self.beat("s12c", [FadeOut(homogeneity, shift=UP * 0.2)], run_time=T_BEAT)

        check = NebMathTex(
            r"v^2 = u^2 + 2as",
            color=TEXT,
            font_size=46,
            substrings_to_isolate=["v^2", "u^2", "2as"],
        )
        check.move_to([0, 1.4, 0])
        tags = [
            NebMathTex(r"[L^2T^{-2}]", color=ACCENT, font_size=30),
            NebMathTex(r"[L^2T^{-2}]", color=ACCENT, font_size=30),
            NebMathTex(r"[L^2T^{-2}]", color=ACCENT, font_size=30),
        ]
        # One tag under each term, hanging from a short rule so the eye can
        # match term to dimension.
        stems = []
        for tag, piece in zip(tags, check.isolate_mobs):
            tag.move_to([piece.get_center()[0], check.get_bottom()[1] - 0.55, 0])
            tag.set_opacity(0)
            stems.append(
                Line(
                    [piece.get_center()[0], check.get_bottom()[1] - 0.14, 0],
                    [piece.get_center()[0], tag.get_top()[1] + 0.06, 0],
                    stroke_color=ACCENT,
                    stroke_width=C.stroke(2),
                ).set_opacity(0)
            )
        self.beat("s13a", [FadeIn(check, shift=UP * 0.2)], run_time=T_BEAT)
        self.beat(
            "s13b",
            [
                AnimationGroup(
                    *[
                        anim
                        for pair in zip(stems, tags)
                        for anim in (
                            pair[0].animate.set_opacity(1),
                            pair[1].animate.set_opacity(1),
                        )
                    ],
                    lag_ratio=0.18,
                )
            ],
            run_time=T_SLOW,
        )
        self.beat(
            "s13c",
            [Circumscribe(VGroup(*tags), color=ACCENT, buff=0.22)],
            run_time=T_SLOW,
        )
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 10 ── converting and deriving ─────────────────────────────────────
        self.build_header("Converting units and deriving relations", "§ 1.2")
        convert = NebMathTex(
            r"n_2 = n_1 \left(\frac{M_1}{M_2}\right)^{a}"
            r"\left(\frac{L_1}{L_2}\right)^{b}"
            r"\left(\frac{T_1}{T_2}\right)^{c}",
            color=TEXT,
            font_size=30,
        )
        convert.move_to([0, 1.95, 0])
        self.beat("s14a", [Write(convert)], run_time=T_BEAT)
        self.beat(
            "s14a2",
            [Indicate(convert, color=ACCENT, scale_factor=1.05)],
            run_time=T_BEAT,
            lead=2.7,
        )
        joule = NebMathTex(
            r"1\ \text{J} = (10^3)^1 (10^2)^2 (1)^{-2} = 10^7\ \text{erg}",
            color=ACCENT,
            font_size=28,
        )
        joule.move_to([0, 1.05, 0])
        self.beat("s14b", [Write(joule)], run_time=T_BEAT)
        self.beat(
            "s14b2",
            [Indicate(joule, color=ACCENT, scale_factor=1.1)],
            run_time=T_BEAT,
            lead=2.2,
        )

        pendulum = NebMathTex(
            r"T = k\,m^{a}l^{b}g^{c}",
            color=TEXT,
            font_size=34,
        )
        matched = NebMathTex(
            r"[T] = [M^{a}L^{b+c}T^{-2c}] \Rightarrow a = 0,\ b = c = \tfrac{1}{2}",
            color=TEXT_SECOND,
            font_size=30,
        )
        result = NebMathTex(r"T = 2\pi\sqrt{\frac{l}{g}}", color=ACCENT, font_size=40)
        note = C.prose("the mass of the bob drops out", size=26, color=TEXT_SECOND)
        chain = VGroup(pendulum, matched, result, note).arrange(DOWN, buff=0.34)
        chain.move_to([0, -0.75, 0])
        self.beat("s15a", [FadeIn(chain, shift=UP * 0.2)], run_time=T_SLOW)
        self.beat(
            "s15a2",
            [Indicate(matched, color=ACCENT, scale_factor=1.05)],
            run_time=T_BEAT,
            lead=2.7,
        )
        self.beat(
            "s15b",
            [Indicate(result, color=ACCENT, scale_factor=1.08)],
            run_time=T_BEAT,
            lead=2.2,
        )
        self.beat(
            "s15b2",
            [Indicate(note, color=ACCENT, scale_factor=1.12)],
            run_time=T_BEAT,
            lead=2.7,
        )
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._chrome])

        # 11 ── limits and summary ──────────────────────────────────────────
        self.build_header("What it cannot do", "§ 1.2")
        limits = C.bullets(
            [
                "supply dimensionless constants — the 2π must come from theory",
                "handle more than three base quantities",
                "build an equation that is a sum of terms",
                VGroup(
                    C.prose("separate work from torque — both are ", size=27, color=TEXT),
                    NebMathTex(r"[ML^2T^{-2}]", color=ACCENT, font_size=27),
                ).arrange(RIGHT, buff=0.12),
            ],
            size=27,
            buff=0.36,
        )
        limits.move_to([0, 1.0, 0])
        self.beat(
            "s16a",
            [AnimationGroup(*[FadeIn(m, shift=UP * 0.2) for m in limits], lag_ratio=0.35)],
            run_time=T_SLOW,
        )
        self.beat(
            "s16a2",
            [Indicate(limits[-1], color=ACCENT, scale_factor=1.1)],
            run_time=T_BEAT,
            lead=4.5,
        )
        self.beat("s16b", [FadeOut(limits, shift=UP * 0.2)], run_time=T_BEAT)
        self.close_section()
        self.build_header("Chapter summary", "Wrap-up")

        summary = VGroup(
            C.prose("A measurement is a number times a unit.", size=28, color=TEXT),
            C.prose(
                "Accuracy is closeness to the truth; precision is closeness of readings.",
                size=26,
                color=TEXT_SECOND,
            ),
            C.prose(
                "Significant figures record how much of your number you can defend.",
                size=26,
                color=TEXT_SECOND,
            ),
            C.prose(
                "Errors add absolutely for sums, relatively for products — a power multiplies.",
                size=26,
                color=TEXT_SECOND,
            ),
            C.prose(
                "Dimensions let you check, convert and derive.",
                size=26,
                color=TEXT_SECOND,
            ),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary.move_to([0, 0.15, 0])
        self.beat(
            "s16c",
            [AnimationGroup(*[FadeIn(m, shift=UP * 0.2) for m in summary], lag_ratio=0.5)],
            run_time=T_SLOW,
        )

        end = C.prose(
            "Worked examples and practice questions are in the chapter notes.",
            size=26,
            color=TEXT_MUTED,
        )
        end.move_to([0, -2.45, 0])
        self.beat("s16d", [FadeIn(end, shift=UP * 0.2)], run_time=T_BEAT)
        self.hold(1.2)
