from manim import *

class PhysicalQuantities(Scene):
    def construct(self):
        # 1. Intro Title
        title = Text("Physical Quantities", font_size=56, weight=BOLD, color=BLUE)
        subtitle = Text("Physics 11 - Unit 1", font_size=36, color=LIGHT_GREY)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title_group))

        # 2. Definition
        def_text_1 = Text("A physical quantity is any property of matter", font_size=32)
        def_text_2 = Text("or of a phenomenon that can be measured.", font_size=32)
        def_group = VGroup(def_text_1, def_text_2).arrange(DOWN, buff=0.3)

        self.play(Write(def_group))
        self.wait(3)
        self.play(def_group.animate.shift(UP * 2.5).scale(0.8))

        # 3. Measurement Concept
        meas_title = Text("Measurement = Number × Unit", font_size=40, color=YELLOW)
        self.play(FadeIn(meas_title, shift=DOWN))
        self.wait(1)

        example_text = MathTex("L = 5 \\text{ meters}", font_size=48)
        example_text.next_to(meas_title, DOWN, buff=1)
        self.play(Write(example_text))

        # Annotations for Number and Unit
        arrow_num = Arrow(start=example_text.get_bottom() + DOWN*0.5 + LEFT*0.8, end=example_text.get_bottom() + LEFT*0.8, color=RED)
        label_num = Text("Number (Magnitude)", font_size=24, color=RED).next_to(arrow_num, DOWN)

        arrow_unit = Arrow(start=example_text.get_bottom() + DOWN*0.5 + RIGHT*0.8, end=example_text.get_bottom() + RIGHT*0.8, color=GREEN)
        label_unit = Text("Standard Unit", font_size=24, color=GREEN).next_to(arrow_unit, DOWN)

        self.play(GrowArrow(arrow_num), FadeIn(label_num))
        self.play(GrowArrow(arrow_unit), FadeIn(label_unit))
        self.wait(4)

        self.play(
            FadeOut(def_group), FadeOut(meas_title), FadeOut(example_text),
            FadeOut(arrow_num), FadeOut(label_num), FadeOut(arrow_unit), FadeOut(label_unit)
        )

        # 4. Outro / Transition
        outro_text = Text("Next: Significant Figures", font_size=40)
        self.play(Write(outro_text))
        self.wait(2)
        self.play(FadeOut(outro_text))
