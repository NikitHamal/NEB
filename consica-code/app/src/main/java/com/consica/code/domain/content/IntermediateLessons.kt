package com.consica.code.domain.content

import com.consica.code.R
import com.consica.code.domain.model.BlockPuzzle
import com.consica.code.domain.model.ChallengeValidation
import com.consica.code.domain.model.CodeChallenge
import com.consica.code.domain.model.LearningPath
import com.consica.code.domain.model.Lesson
import com.consica.code.domain.model.LessonStep
import com.consica.code.domain.model.LessonType
import com.consica.code.domain.model.PuzzleBlock
import com.consica.code.domain.model.TerraExpression
import com.consica.code.domain.model.TrackLanguage

/**
 * Intermediate biomes:
 *  - River Delta — intermediate web (layouts, forms, page structure, mini project)
 *  - Deep Grove — intermediate Python (logic, data, reusable functions, challenges)
 */
internal object IntermediateLessons {

    val lessons: List<Lesson> = riverDeltaLessons + deepGroveLessons

    // ════════════════════════ RIVER DELTA (web) ════════════════════════════

    private val riverDeltaLessons: List<Lesson>
        get() = listOf(

            // ── 1. CSS layouts ──────────────────────────────────────────────
            Lesson(
                id = "int_web_layouts",
                biomeId = "river_delta",
                titleRes = R.string.lesson_int_web_layouts_title,
                descriptionRes = R.string.lesson_int_web_layouts_desc,
                type = LessonType.CODE,
                language = TrackLanguage.HTML,
                path = LearningPath.INTERMEDIATE,
                order = 1,
                xpReward = 90,
                sunReward = 10,
                ecosystemItemId = "river_stone",
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_layouts_step1_kid,
                        teenTextRes = R.string.lesson_int_web_layouts_step1_teen,
                        expression = TerraExpression.HAPPY,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_layouts_step2_kid,
                        teenTextRes = R.string.lesson_int_web_layouts_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = ".card {\n  padding: 16px;\n  border-radius: 12px;\n  background-color: #e3f2fd;\n}",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_layouts_step3_kid,
                        teenTextRes = R.string.lesson_int_web_layouts_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.HTML,
                    starterCode = "<style>\n  .card {\n    /* Shape your card here */\n  }\n</style>\n<div class=\"card\">\n  <h2>River Delta</h2>\n  <p>Where the water spreads wide and calm.</p>\n</div>",
                    instructionRes = R.string.lesson_int_web_layouts_instruction,
                    hintRes = R.string.lesson_int_web_layouts_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "padding\\s*:"),
                            ChallengeValidation.CodeMatches(pattern = "border-radius\\s*:"),
                            ChallengeValidation.CodeMatches(pattern = "background(-color)?\\s*:"),
                        ),
                    ),
                ),
            ),

            // ── 2. Forms ────────────────────────────────────────────────────
            Lesson(
                id = "int_web_forms",
                biomeId = "river_delta",
                titleRes = R.string.lesson_int_web_forms_title,
                descriptionRes = R.string.lesson_int_web_forms_desc,
                type = LessonType.CODE,
                language = TrackLanguage.HTML,
                path = LearningPath.INTERMEDIATE,
                order = 2,
                xpReward = 95,
                waterReward = 10,
                ecosystemItemId = "fish",
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_forms_step1_kid,
                        teenTextRes = R.string.lesson_int_web_forms_step1_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_forms_step2_kid,
                        teenTextRes = R.string.lesson_int_web_forms_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "<form>\n  <label>Your name</label>\n  <input type=\"text\">\n  <button>Send</button>\n</form>",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_forms_step3_kid,
                        teenTextRes = R.string.lesson_int_web_forms_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.HTML,
                    starterCode = "<h2>River Survey</h2>\n<form>\n  <!-- Add a label, a text input, and a button -->\n</form>",
                    instructionRes = R.string.lesson_int_web_forms_instruction,
                    hintRes = R.string.lesson_int_web_forms_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.HtmlHasTag(tag = "form"),
                            ChallengeValidation.HtmlHasTag(tag = "label"),
                            ChallengeValidation.HtmlHasTag(tag = "input"),
                            ChallengeValidation.HtmlHasTag(tag = "button"),
                        ),
                    ),
                ),
            ),

            // ── 3. Page sections puzzle ─────────────────────────────────────
            Lesson(
                id = "int_web_sections",
                biomeId = "river_delta",
                titleRes = R.string.lesson_int_web_sections_title,
                descriptionRes = R.string.lesson_int_web_sections_desc,
                type = LessonType.PUZZLE,
                language = TrackLanguage.HTML,
                path = LearningPath.INTERMEDIATE,
                order = 3,
                xpReward = 90,
                sunReward = 5,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_sections_step1_kid,
                        teenTextRes = R.string.lesson_int_web_sections_step1_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_sections_step2_kid,
                        teenTextRes = R.string.lesson_int_web_sections_step2_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                ),
                puzzle = BlockPuzzle(
                    promptRes = R.string.lesson_int_web_sections_instruction,
                    hintRes = R.string.lesson_int_web_sections_hint,
                    language = TrackLanguage.HTML,
                    blocks = listOf(
                        PuzzleBlock(code = "<header><h1>Delta Diary</h1></header>"),
                        PuzzleBlock(code = "<nav><a href=\"#posts\">Posts</a></nav>"),
                        PuzzleBlock(code = "<main>"),
                        PuzzleBlock(code = "<section id=\"posts\"><p>Today the river was calm.</p></section>", indent = 1),
                        PuzzleBlock(code = "</main>"),
                        PuzzleBlock(code = "<footer><p>Written beside the river</p></footer>"),
                    ),
                ),
            ),

            // ── 4. Profile card mini project ────────────────────────────────
            Lesson(
                id = "int_web_profile_card",
                biomeId = "river_delta",
                titleRes = R.string.lesson_int_web_profile_card_title,
                descriptionRes = R.string.lesson_int_web_profile_card_desc,
                type = LessonType.CODE,
                language = TrackLanguage.HTML,
                path = LearningPath.INTERMEDIATE,
                order = 4,
                xpReward = 110,
                sunReward = 15,
                waterReward = 10,
                badgeId = "river_builder",
                ecosystemItemId = "lily",
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_profile_card_step1_kid,
                        teenTextRes = R.string.lesson_int_web_profile_card_step1_teen,
                        expression = TerraExpression.EXCITED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_profile_card_step2_kid,
                        teenTextRes = R.string.lesson_int_web_profile_card_step2_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_web_profile_card_step3_kid,
                        teenTextRes = R.string.lesson_int_web_profile_card_step3_teen,
                        expression = TerraExpression.PROUD,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.HTML,
                    starterCode = "<style>\n  .profile {\n    /* Round the corners and add some padding */\n  }\n</style>\n<div class=\"profile\">\n  <!-- Add an image, your name in an h2, and a short bio paragraph -->\n</div>",
                    instructionRes = R.string.lesson_int_web_profile_card_instruction,
                    hintRes = R.string.lesson_int_web_profile_card_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.HtmlHasTag(tag = "img"),
                            ChallengeValidation.HtmlHasTag(tag = "h2"),
                            ChallengeValidation.HtmlHasTag(tag = "p"),
                            ChallengeValidation.CodeMatches(pattern = "border-radius\\s*:"),
                        ),
                    ),
                ),
            ),
        )

    // ════════════════════════ DEEP GROVE (Python) ══════════════════════════

    private val deepGroveLessons: List<Lesson>
        get() = listOf(

            // ── 1. Logic puzzle ─────────────────────────────────────────────
            Lesson(
                id = "int_py_logic",
                biomeId = "deep_grove",
                titleRes = R.string.lesson_int_py_logic_title,
                descriptionRes = R.string.lesson_int_py_logic_desc,
                type = LessonType.PUZZLE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.INTERMEDIATE,
                order = 1,
                xpReward = 90,
                waterReward = 5,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_logic_step1_kid,
                        teenTextRes = R.string.lesson_int_py_logic_step1_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_logic_step2_kid,
                        teenTextRes = R.string.lesson_int_py_logic_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "if n % 2 == 0:\n    print(\"even\")",
                    ),
                ),
                puzzle = BlockPuzzle(
                    promptRes = R.string.lesson_int_py_logic_instruction,
                    hintRes = R.string.lesson_int_py_logic_hint,
                    language = TrackLanguage.PYTHON,
                    blocks = listOf(
                        PuzzleBlock(code = "numbers = [3, 10, 7, 16]"),
                        PuzzleBlock(code = "for n in numbers:"),
                        PuzzleBlock(code = "if n % 2 == 0:", indent = 1),
                        PuzzleBlock(code = "print(f\"{n} is even\")", indent = 2),
                        PuzzleBlock(code = "else:", indent = 1),
                        PuzzleBlock(code = "print(f\"{n} is odd\")", indent = 2),
                    ),
                ),
            ),

            // ── 2. Working with data ────────────────────────────────────────
            Lesson(
                id = "int_py_data",
                biomeId = "deep_grove",
                titleRes = R.string.lesson_int_py_data_title,
                descriptionRes = R.string.lesson_int_py_data_desc,
                type = LessonType.CODE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.INTERMEDIATE,
                order = 2,
                xpReward = 95,
                sunReward = 10,
                ecosystemItemId = "pine",
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_data_step1_kid,
                        teenTextRes = R.string.lesson_int_py_data_step1_teen,
                        expression = TerraExpression.HAPPY,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_data_step2_kid,
                        teenTextRes = R.string.lesson_int_py_data_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "prices = [50, 120, 80, 30]\nprices.sort()\nprint(prices[0])\nprint(sum(prices))",
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# The trail snack stand\nprices = [50, 120, 80, 30]\n# 1) Sort the prices\n# 2) Print the cheapest price and the total of all prices\n",
                    instructionRes = R.string.lesson_int_py_data_instruction,
                    hintRes = R.string.lesson_int_py_data_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "prices"),
                            ChallengeValidation.OutputContains(needles = listOf("30", "280")),
                        ),
                    ),
                ),
            ),

            // ── 3. Functions and reuse ──────────────────────────────────────
            Lesson(
                id = "int_py_functions",
                biomeId = "deep_grove",
                titleRes = R.string.lesson_int_py_functions_title,
                descriptionRes = R.string.lesson_int_py_functions_desc,
                type = LessonType.CODE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.INTERMEDIATE,
                order = 3,
                xpReward = 100,
                waterReward = 10,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_functions_step1_kid,
                        teenTextRes = R.string.lesson_int_py_functions_step1_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_functions_step2_kid,
                        teenTextRes = R.string.lesson_int_py_functions_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "def rectangle_area(width, height):\n    print(f\"Area: {width * height}\")",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_functions_step3_kid,
                        teenTextRes = R.string.lesson_int_py_functions_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# A reusable area calculator for garden beds\ndef rectangle_area(width, height):\n    print(\"change me\")\n\n# Call it for a 4 x 5 bed and a 3 x 3 bed\n",
                    instructionRes = R.string.lesson_int_py_functions_instruction,
                    hintRes = R.string.lesson_int_py_functions_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "def\\s+rectangle_area"),
                            ChallengeValidation.OutputContains(needles = listOf("20", "9")),
                        ),
                    ),
                ),
            ),

            // ── 4. Problem solving challenge ────────────────────────────────
            Lesson(
                id = "int_py_challenge",
                biomeId = "deep_grove",
                titleRes = R.string.lesson_int_py_challenge_title,
                descriptionRes = R.string.lesson_int_py_challenge_desc,
                type = LessonType.CODE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.INTERMEDIATE,
                order = 4,
                xpReward = 120,
                sunReward = 15,
                waterReward = 10,
                badgeId = "grove_thinker",
                ecosystemItemId = "owl_friend",
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_challenge_step1_kid,
                        teenTextRes = R.string.lesson_int_py_challenge_step1_teen,
                        expression = TerraExpression.EXCITED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_challenge_step2_kid,
                        teenTextRes = R.string.lesson_int_py_challenge_step2_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_int_py_challenge_step3_kid,
                        teenTextRes = R.string.lesson_int_py_challenge_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# Vowel counter\nword = \"himalaya\"\n# Count how many a, e, i, o, u letters appear in word\n# and print the total\n",
                    instructionRes = R.string.lesson_int_py_challenge_instruction,
                    hintRes = R.string.lesson_int_py_challenge_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "for\\s+"),
                            ChallengeValidation.OutputContains(needles = listOf("4")),
                        ),
                    ),
                ),
            ),
        )
}
