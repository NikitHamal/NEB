package com.consica.code.data.content

import com.consica.code.R
import com.consica.code.core.model.AgeAdaptiveText
import com.consica.code.core.model.Biome
import com.consica.code.core.model.BlockPuzzle
import com.consica.code.core.model.ChallengeCheck
import com.consica.code.core.model.CodeChallenge
import com.consica.code.core.model.CodeLanguage
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.LessonStep
import com.consica.code.core.model.LessonType
import com.consica.code.core.model.TerraExpression

/**
 * The full offline lesson catalog. Lesson copy lives in string resources so
 * content can be localized (Nepali next) without touching this structure.
 */
object LessonCatalog {

    // ------------------------------------------------------------------
    // Forest Floor — Beginner Web
    // ------------------------------------------------------------------

    private val webIntro = Lesson(
        id = "web_intro",
        biome = Biome.FOREST_FLOOR,
        order = 0,
        type = LessonType.TUTORIAL,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_intro_title,
        descriptionRes = R.string.lesson_web_intro_desc,
        xpReward = 20, sunReward = 5, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_intro_1_kids, R.string.step_web_intro_1_teens, R.string.step_web_intro_1_pro),
                TerraExpression.EXCITED,
            ),
            LessonStep(
                AgeAdaptiveText(R.string.step_web_intro_2_kids, R.string.step_web_intro_2_teens, R.string.step_web_intro_2_pro),
                TerraExpression.THINKING,
                codeSnippet = "<h1>Hello!</h1>",
            ),
            LessonStep(
                AgeAdaptiveText(R.string.step_web_intro_3_kids, R.string.step_web_intro_3_teens, R.string.step_web_intro_3_pro),
                TerraExpression.ENCOURAGING,
            ),
        ),
    )

    private val webHeading = Lesson(
        id = "web_heading",
        biome = Biome.FOREST_FLOOR,
        order = 1,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_heading_title,
        descriptionRes = R.string.lesson_web_heading_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        badgeId = BadgeCatalog.FIRST_SPROUT,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_heading_1_kids, R.string.step_web_heading_1_teens, R.string.step_web_heading_1_pro),
                TerraExpression.HAPPY,
                codeSnippet = "<h1>…</h1>",
            ),
            LessonStep(
                AgeAdaptiveText(R.string.step_web_heading_2_kids, R.string.step_web_heading_2_teens, R.string.step_web_heading_2_pro),
                TerraExpression.EXCITED,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<!-- Write your heading below -->\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_heading_kids, R.string.challenge_web_heading_teens, R.string.challenge_web_heading_pro),
            hint = AgeAdaptiveText(R.string.hint_web_heading_kids, R.string.hint_web_heading_teens, R.string.hint_web_heading_pro),
            checks = listOf(ChallengeCheck.HtmlHasTag("h1", content = "Sprout")),
            successLabel = "Sprout",
        ),
    )

    private val webParagraphs = Lesson(
        id = "web_paragraphs",
        biome = Biome.FOREST_FLOOR,
        order = 2,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_paragraphs_title,
        descriptionRes = R.string.lesson_web_paragraphs_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_paragraphs_1_kids, R.string.step_web_paragraphs_1_teens, R.string.step_web_paragraphs_1_pro),
                TerraExpression.HAPPY,
                codeSnippet = "<p>Plants grow here!</p>",
            ),
            LessonStep(
                AgeAdaptiveText(R.string.step_web_paragraphs_2_kids, R.string.step_web_paragraphs_2_teens, R.string.step_web_paragraphs_2_pro),
                TerraExpression.ENCOURAGING,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<h1>My Garden</h1>\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_paragraphs_kids, R.string.challenge_web_paragraphs_teens, R.string.challenge_web_paragraphs_pro),
            hint = AgeAdaptiveText(R.string.hint_web_paragraphs_kids, R.string.hint_web_paragraphs_teens, R.string.hint_web_paragraphs_pro),
            checks = listOf(ChallengeCheck.HtmlHasTag("h1"), ChallengeCheck.HtmlHasTag("p")),
        ),
    )

    private val webStructure = Lesson(
        id = "web_structure",
        biome = Biome.FOREST_FLOOR,
        order = 3,
        type = LessonType.PUZZLE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_structure_title,
        descriptionRes = R.string.lesson_web_structure_desc,
        xpReward = 35, sunReward = 10, waterReward = 10,
        badgeId = BadgeCatalog.BLOCK_WIZARD,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_structure_1_kids, R.string.step_web_structure_1_teens, R.string.step_web_structure_1_pro),
                TerraExpression.THINKING,
            ),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_web_structure_kids, R.string.puzzle_web_structure_teens, R.string.puzzle_web_structure_pro),
            language = CodeLanguage.HTML,
            solution = listOf(
                "<!DOCTYPE html>",
                "<html>",
                "<head>",
                "<title>My Page</title>",
                "</head>",
                "<body>",
                "<h1>Hello Forest</h1>",
                "</body>",
                "</html>",
            ),
        ),
    )

    private val webLinks = Lesson(
        id = "web_links",
        biome = Biome.FOREST_FLOOR,
        order = 4,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_links_title,
        descriptionRes = R.string.lesson_web_links_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_links_1_kids, R.string.step_web_links_1_teens, R.string.step_web_links_1_pro),
                TerraExpression.EXCITED,
                codeSnippet = "<a href=\"#\">Visit</a>",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<h1>Doorways</h1>\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_links_kids, R.string.challenge_web_links_teens, R.string.challenge_web_links_pro),
            hint = AgeAdaptiveText(R.string.hint_web_links_kids, R.string.hint_web_links_teens, R.string.hint_web_links_pro),
            checks = listOf(ChallengeCheck.HtmlHasTag("a"), ChallengeCheck.CodeContains("href")),
        ),
    )

    private val webImages = Lesson(
        id = "web_images",
        biome = Biome.FOREST_FLOOR,
        order = 5,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_images_title,
        descriptionRes = R.string.lesson_web_images_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_images_1_kids, R.string.step_web_images_1_teens, R.string.step_web_images_1_pro),
                TerraExpression.HAPPY,
                codeSnippet = "<img src=\"tree.png\" alt=\"a tree\">",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<h1>My Photos</h1>\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_images_kids, R.string.challenge_web_images_teens, R.string.challenge_web_images_pro),
            hint = AgeAdaptiveText(R.string.hint_web_images_kids, R.string.hint_web_images_teens, R.string.hint_web_images_pro),
            checks = listOf(ChallengeCheck.CodeContains("<img"), ChallengeCheck.CodeContains("src"), ChallengeCheck.CodeContains("alt")),
        ),
    )

    private val webLists = Lesson(
        id = "web_lists",
        biome = Biome.FOREST_FLOOR,
        order = 6,
        type = LessonType.PUZZLE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_lists_title,
        descriptionRes = R.string.lesson_web_lists_desc,
        xpReward = 35, sunReward = 10, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_lists_1_kids, R.string.step_web_lists_1_teens, R.string.step_web_lists_1_pro),
                TerraExpression.THINKING,
                codeSnippet = "<ul>\n  <li>fern</li>\n</ul>",
            ),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_web_lists_kids, R.string.puzzle_web_lists_teens, R.string.puzzle_web_lists_pro),
            language = CodeLanguage.HTML,
            solution = listOf(
                "<ul>",
                "<li>fern</li>",
                "<li>moss</li>",
                "<li>vine</li>",
                "</ul>",
            ),
            distractors = listOf("</li>fern<li>"),
        ),
    )

    private val webCss = Lesson(
        id = "web_css_colors",
        biome = Biome.FOREST_FLOOR,
        order = 7,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_css_title,
        descriptionRes = R.string.lesson_web_css_desc,
        xpReward = 35, sunReward = 15, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_css_1_kids, R.string.step_web_css_1_teens, R.string.step_web_css_1_pro),
                TerraExpression.EXCITED,
                codeSnippet = "<style>\n  h1 { color: green; }\n</style>",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<h1>Colorful Garden</h1>\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_css_kids, R.string.challenge_web_css_teens, R.string.challenge_web_css_pro),
            hint = AgeAdaptiveText(R.string.hint_web_css_kids, R.string.hint_web_css_teens, R.string.hint_web_css_pro),
            checks = listOf(ChallengeCheck.HtmlHasTag("style"), ChallengeCheck.CodeContains("color")),
        ),
    )

    private val webProject = Lesson(
        id = "web_mini_page",
        biome = Biome.FOREST_FLOOR,
        order = 8,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_web_project_title,
        descriptionRes = R.string.lesson_web_project_desc,
        xpReward = 60, sunReward = 25, waterReward = 15,
        masteryReward = 3,
        badgeId = BadgeCatalog.WEB_GARDENER,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_web_project_1_kids, R.string.step_web_project_1_teens, R.string.step_web_project_1_pro),
                TerraExpression.PROUD,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<!-- Your mini page: heading + paragraph + list -->\n",
            instruction = AgeAdaptiveText(R.string.challenge_web_project_kids, R.string.challenge_web_project_teens, R.string.challenge_web_project_pro),
            hint = AgeAdaptiveText(R.string.hint_web_project_kids, R.string.hint_web_project_teens, R.string.hint_web_project_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("h1"),
                ChallengeCheck.HtmlHasTag("p"),
                ChallengeCheck.HtmlHasTag("li"),
            ),
        ),
    )

    // ------------------------------------------------------------------
    // Sunny Meadow — Beginner Python
    // ------------------------------------------------------------------

    private val pyPrint = Lesson(
        id = "py_print",
        biome = Biome.SUNNY_MEADOW,
        order = 0,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_print_title,
        descriptionRes = R.string.lesson_py_print_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        badgeId = BadgeCatalog.FIRST_PRINT,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_print_1_kids, R.string.step_py_print_1_teens, R.string.step_py_print_1_pro),
                TerraExpression.EXCITED,
                codeSnippet = "print(\"Hello!\")",
            ),
            LessonStep(
                AgeAdaptiveText(R.string.step_py_print_2_kids, R.string.step_py_print_2_teens, R.string.step_py_print_2_pro),
                TerraExpression.ENCOURAGING,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Make the console speak!\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_print_kids, R.string.challenge_py_print_teens, R.string.challenge_py_print_pro),
            hint = AgeAdaptiveText(R.string.hint_py_print_kids, R.string.hint_py_print_teens, R.string.hint_py_print_pro),
            checks = listOf(ChallengeCheck.RunsCleanly, ChallengeCheck.OutputContains("Hello, Meadow!")),
            successLabel = "Hello, Meadow!",
        ),
    )

    private val pyVariables = Lesson(
        id = "py_variables",
        biome = Biome.SUNNY_MEADOW,
        order = 1,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_variables_title,
        descriptionRes = R.string.lesson_py_variables_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_variables_1_kids, R.string.step_py_variables_1_teens, R.string.step_py_variables_1_pro),
                TerraExpression.HAPPY,
                codeSnippet = "plant = \"fern\"\nprint(plant)",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Create your seed box\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_variables_kids, R.string.challenge_py_variables_teens, R.string.challenge_py_variables_pro),
            hint = AgeAdaptiveText(R.string.hint_py_variables_kids, R.string.hint_py_variables_teens, R.string.hint_py_variables_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("plant"),
                ChallengeCheck.CodeContains("print(plant)", ignoreCase = false),
            ),
        ),
    )

    private val pyStrNum = Lesson(
        id = "py_strings_numbers",
        biome = Biome.SUNNY_MEADOW,
        order = 2,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_strnum_title,
        descriptionRes = R.string.lesson_py_strnum_desc,
        xpReward = 30, sunReward = 10, waterReward = 5,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_strnum_1_kids, R.string.step_py_strnum_1_teens, R.string.step_py_strnum_1_pro),
                TerraExpression.THINKING,
                codeSnippet = "print(3 + 4)\nprint(\"sun\" + \"flower\")",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Python is a calculator too\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_strnum_kids, R.string.challenge_py_strnum_teens, R.string.challenge_py_strnum_pro),
            hint = AgeAdaptiveText(R.string.hint_py_strnum_kids, R.string.hint_py_strnum_teens, R.string.hint_py_strnum_pro),
            checks = listOf(ChallengeCheck.RunsCleanly, ChallengeCheck.OutputContains("42")),
            successLabel = "42",
        ),
    )

    private val pyOrder = Lesson(
        id = "py_order",
        biome = Biome.SUNNY_MEADOW,
        order = 3,
        type = LessonType.PUZZLE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_order_title,
        descriptionRes = R.string.lesson_py_order_desc,
        xpReward = 35, sunReward = 10, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_order_1_kids, R.string.step_py_order_1_teens, R.string.step_py_order_1_pro),
                TerraExpression.THINKING,
            ),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_py_order_kids, R.string.puzzle_py_order_teens, R.string.puzzle_py_order_pro),
            language = CodeLanguage.PYTHON,
            solution = listOf(
                "plant = \"fern\"",
                "water = 3",
                "print(plant)",
                "print(water)",
            ),
        ),
    )

    private val pyCond = Lesson(
        id = "py_conditionals",
        biome = Biome.SUNNY_MEADOW,
        order = 4,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_cond_title,
        descriptionRes = R.string.lesson_py_cond_desc,
        xpReward = 40, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_cond_1_kids, R.string.step_py_cond_1_teens, R.string.step_py_cond_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "if sun > 5:\n    print(\"grow!\")\nelse:\n    print(\"rest\")",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "sun = 8\n# Add your if/else below\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_cond_kids, R.string.challenge_py_cond_teens, R.string.challenge_py_cond_pro),
            hint = AgeAdaptiveText(R.string.hint_py_cond_kids, R.string.hint_py_cond_teens, R.string.hint_py_cond_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("if"),
                ChallengeCheck.OutputContains("grow!"),
            ),
            successLabel = "grow!",
        ),
    )

    private val pyLoops = Lesson(
        id = "py_loops",
        biome = Biome.SUNNY_MEADOW,
        order = 5,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_loops_title,
        descriptionRes = R.string.lesson_py_loops_desc,
        xpReward = 40, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_loops_1_kids, R.string.step_py_loops_1_teens, R.string.step_py_loops_1_pro),
                TerraExpression.EXCITED,
                codeSnippet = "for i in range(3):\n    print(\"drip\")",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Make it rain three times\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_loops_kids, R.string.challenge_py_loops_teens, R.string.challenge_py_loops_pro),
            hint = AgeAdaptiveText(R.string.hint_py_loops_kids, R.string.hint_py_loops_teens, R.string.hint_py_loops_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("for"),
                ChallengeCheck.OutputContains("drip\ndrip\ndrip"),
            ),
            successLabel = "drip ×3",
        ),
    )

    private val pyLoopPuzzle = Lesson(
        id = "py_loop_puzzle",
        biome = Biome.SUNNY_MEADOW,
        order = 6,
        type = LessonType.PUZZLE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_loop_puzzle_title,
        descriptionRes = R.string.lesson_py_loop_puzzle_desc,
        xpReward = 40, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_loop_puzzle_1_kids, R.string.step_py_loop_puzzle_1_teens, R.string.step_py_loop_puzzle_1_pro),
                TerraExpression.THINKING,
            ),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_py_loop_kids, R.string.puzzle_py_loop_teens, R.string.puzzle_py_loop_pro),
            language = CodeLanguage.PYTHON,
            solution = listOf(
                "count = 0",
                "for i in range(3):",
                "    count = count + 1",
                "    print(count)",
            ),
            distractors = listOf("count = \"three\""),
        ),
    )

    private val pyLists = Lesson(
        id = "py_lists",
        biome = Biome.SUNNY_MEADOW,
        order = 7,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_lists_title,
        descriptionRes = R.string.lesson_py_lists_desc,
        xpReward = 40, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_lists_1_kids, R.string.step_py_lists_1_teens, R.string.step_py_lists_1_pro),
                TerraExpression.HAPPY,
                codeSnippet = "seeds = [\"fern\", \"moss\", \"vine\"]\nfor s in seeds:\n    print(s)",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Fill your basket\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_lists_kids, R.string.challenge_py_lists_teens, R.string.challenge_py_lists_pro),
            hint = AgeAdaptiveText(R.string.hint_py_lists_kids, R.string.hint_py_lists_teens, R.string.hint_py_lists_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("["),
                ChallengeCheck.CodeContains("for"),
            ),
        ),
    )

    private val pyFunctions = Lesson(
        id = "py_functions",
        biome = Biome.SUNNY_MEADOW,
        order = 8,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_functions_title,
        descriptionRes = R.string.lesson_py_functions_desc,
        xpReward = 45, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_functions_1_kids, R.string.step_py_functions_1_teens, R.string.step_py_functions_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "def greet():\n    print(\"namaste\")\n\ngreet()",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Write your recipe\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_functions_kids, R.string.challenge_py_functions_teens, R.string.challenge_py_functions_pro),
            hint = AgeAdaptiveText(R.string.hint_py_functions_kids, R.string.hint_py_functions_teens, R.string.hint_py_functions_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("def"),
                ChallengeCheck.OutputContains("namaste"),
            ),
            successLabel = "namaste",
        ),
    )

    private val pyDebug = Lesson(
        id = "py_debug",
        biome = Biome.SUNNY_MEADOW,
        order = 9,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_debug_title,
        descriptionRes = R.string.lesson_py_debug_desc,
        xpReward = 50, sunReward = 20, waterReward = 15,
        masteryReward = 3,
        badgeId = BadgeCatalog.BUG_CATCHER,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_debug_1_kids, R.string.step_py_debug_1_teens, R.string.step_py_debug_1_pro),
                TerraExpression.CONFUSED,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "season = \"autumn\"\nprnt(\"harvest time\")\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_debug_kids, R.string.challenge_py_debug_teens, R.string.challenge_py_debug_pro),
            hint = AgeAdaptiveText(R.string.hint_py_debug_kids, R.string.hint_py_debug_teens, R.string.hint_py_debug_pro),
            checks = listOf(ChallengeCheck.RunsCleanly, ChallengeCheck.OutputContains("harvest time")),
            successLabel = "harvest time",
        ),
    )

    // ------------------------------------------------------------------
    // Riverbank — Intermediate
    // ------------------------------------------------------------------

    private val cssLayout = Lesson(
        id = "css_layout",
        biome = Biome.RIVERBANK,
        order = 0,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_css_layout_title,
        descriptionRes = R.string.lesson_css_layout_desc,
        xpReward = 45, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_css_layout_1_teens, R.string.step_css_layout_1_teens, R.string.step_css_layout_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "div {\n  background-color: lightgreen;\n  padding: 16px;\n}",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<div>\n  <h1>River Card</h1>\n</div>\n",
            instruction = AgeAdaptiveText(R.string.challenge_css_layout_teens, R.string.challenge_css_layout_teens, R.string.challenge_css_layout_pro),
            hint = AgeAdaptiveText(R.string.hint_css_layout_teens, R.string.hint_css_layout_teens, R.string.hint_css_layout_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("style"),
                ChallengeCheck.CodeContains("background"),
                ChallengeCheck.CodeContains("padding"),
            ),
        ),
    )

    private val htmlForm = Lesson(
        id = "html_form",
        biome = Biome.RIVERBANK,
        order = 1,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_html_form_title,
        descriptionRes = R.string.lesson_html_form_desc,
        xpReward = 45, sunReward = 15, waterReward = 10,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_html_form_1_teens, R.string.step_html_form_1_teens, R.string.step_html_form_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "<form>\n  <input>\n  <button>Send</button>\n</form>",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<h1>Visitor Book</h1>\n",
            instruction = AgeAdaptiveText(R.string.challenge_html_form_teens, R.string.challenge_html_form_teens, R.string.challenge_html_form_pro),
            hint = AgeAdaptiveText(R.string.hint_html_form_teens, R.string.hint_html_form_teens, R.string.hint_html_form_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("form"),
                ChallengeCheck.CodeContains("<input"),
                ChallengeCheck.HtmlHasTag("button"),
            ),
        ),
    )

    private val pyLogic = Lesson(
        id = "py_logic_puzzle",
        biome = Biome.RIVERBANK,
        order = 2,
        type = LessonType.PUZZLE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_logic_title,
        descriptionRes = R.string.lesson_py_logic_desc,
        xpReward = 50, sunReward = 15, waterReward = 15,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_logic_1_teens, R.string.step_py_logic_1_teens, R.string.step_py_logic_1_pro),
                TerraExpression.THINKING,
            ),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_py_logic_teens, R.string.puzzle_py_logic_teens, R.string.puzzle_py_logic_pro),
            language = CodeLanguage.PYTHON,
            solution = listOf(
                "rain = 7",
                "if rain > 5:",
                "    if rain > 10:",
                "        print(\"flood watch\")",
                "    else:",
                "        print(\"good rain\")",
                "else:",
                "    print(\"dry day\")",
            ),
            distractors = listOf("print(\"snow day\")"),
        ),
    )

    private val pyData = Lesson(
        id = "py_data",
        biome = Biome.RIVERBANK,
        order = 3,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_data_title,
        descriptionRes = R.string.lesson_py_data_desc,
        xpReward = 50, sunReward = 15, waterReward = 15,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_data_1_teens, R.string.step_py_data_1_teens, R.string.step_py_data_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "seeds = [\"fern\", \"moss\", \"vine\"]\nprint(seeds[0])\nprint(len(seeds))",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "seeds = [\"fern\", \"moss\", \"vine\"]\n# Print the first item, then the length\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_data_teens, R.string.challenge_py_data_teens, R.string.challenge_py_data_pro),
            hint = AgeAdaptiveText(R.string.hint_py_data_teens, R.string.hint_py_data_teens, R.string.hint_py_data_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.OutputContains("fern"),
                ChallengeCheck.OutputContains("3"),
            ),
        ),
    )

    private val pyModules = Lesson(
        id = "py_modules",
        biome = Biome.RIVERBANK,
        order = 4,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_py_modules_title,
        descriptionRes = R.string.lesson_py_modules_desc,
        xpReward = 55, sunReward = 20, waterReward = 15,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_py_modules_1_teens, R.string.step_py_modules_1_teens, R.string.step_py_modules_1_pro),
                TerraExpression.FOCUSED,
                codeSnippet = "def double(n):\n    return n * 2\n\nprint(double(4))",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "# Build double(n) and use it\n",
            instruction = AgeAdaptiveText(R.string.challenge_py_modules_teens, R.string.challenge_py_modules_teens, R.string.challenge_py_modules_pro),
            hint = AgeAdaptiveText(R.string.hint_py_modules_teens, R.string.hint_py_modules_teens, R.string.hint_py_modules_pro),
            checks = listOf(
                ChallengeCheck.RunsCleanly,
                ChallengeCheck.CodeContains("def"),
                ChallengeCheck.CodeContains("return"),
                ChallengeCheck.OutputContains("8"),
            ),
            successLabel = "8",
        ),
    )

    private val projectCard = Lesson(
        id = "project_card",
        biome = Biome.RIVERBANK,
        order = 5,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_project_card_title,
        descriptionRes = R.string.lesson_project_card_desc,
        xpReward = 70, sunReward = 30, waterReward = 20,
        masteryReward = 4,
        badgeId = BadgeCatalog.RIVER_BUILDER,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_project_card_1_teens, R.string.step_project_card_1_teens, R.string.step_project_card_1_pro),
                TerraExpression.PROUD,
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<!-- Your profile card -->\n",
            instruction = AgeAdaptiveText(R.string.challenge_project_card_teens, R.string.challenge_project_card_teens, R.string.challenge_project_card_pro),
            hint = AgeAdaptiveText(R.string.hint_project_card_teens, R.string.hint_project_card_teens, R.string.hint_project_card_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("h1"),
                ChallengeCheck.HtmlHasTag("p"),
                ChallengeCheck.HtmlHasTag("style"),
            ),
        ),
    )

    // ------------------------------------------------------------------
    // Canopy — Advanced / 16+
    // ------------------------------------------------------------------

    private val advTools = Lesson(
        id = "adv_workspace",
        biome = Biome.CANOPY,
        order = 0,
        type = LessonType.TUTORIAL,
        language = null,
        titleRes = R.string.lesson_adv_tools_title,
        descriptionRes = R.string.lesson_adv_tools_desc,
        xpReward = 40, sunReward = 15, waterReward = 10,
        masteryReward = 2,
        advanced = true,
        steps = listOf(
            LessonStep(AgeAdaptiveText(R.string.step_adv_tools_1_pro), TerraExpression.PROFESSIONAL),
            LessonStep(AgeAdaptiveText(R.string.step_adv_tools_2_pro), TerraExpression.FOCUSED),
            LessonStep(AgeAdaptiveText(R.string.step_adv_tools_3_pro), TerraExpression.THINKING),
        ),
    )

    private val advWeb = Lesson(
        id = "adv_web_project",
        biome = Biome.CANOPY,
        order = 1,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_adv_web_title,
        descriptionRes = R.string.lesson_adv_web_desc,
        xpReward = 60, sunReward = 20, waterReward = 15,
        advanced = true,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_adv_web_1_pro),
                TerraExpression.PROFESSIONAL,
                codeSnippet = "<header>…</header>\n<main>…</main>\n<footer>…</footer>",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<!-- Compose header / main / footer -->\n",
            instruction = AgeAdaptiveText(R.string.challenge_adv_web_pro),
            hint = AgeAdaptiveText(R.string.hint_adv_web_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("header"),
                ChallengeCheck.HtmlHasTag("main"),
                ChallengeCheck.HtmlHasTag("footer"),
            ),
        ),
    )

    private val advPy = Lesson(
        id = "adv_py_script",
        biome = Biome.CANOPY,
        order = 2,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_adv_py_title,
        descriptionRes = R.string.lesson_adv_py_desc,
        xpReward = 65, sunReward = 20, waterReward = 20,
        advanced = true,
        steps = listOf(
            LessonStep(
                AgeAdaptiveText(R.string.step_adv_py_1_pro),
                TerraExpression.PROFESSIONAL,
                codeSnippet = "total = 0\nfor r in rain:\n    if r > 10:\n        total = total + r",
            ),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "rain = [4, 12, 8, 20, 15, 3]\n# Sum values greater than 10\n",
            instruction = AgeAdaptiveText(R.string.challenge_adv_py_pro),
            hint = AgeAdaptiveText(R.string.hint_adv_py_pro),
            checks = listOf(ChallengeCheck.RunsCleanly, ChallengeCheck.OutputContains("47")),
            successLabel = "47",
        ),
    )

    private val advAlgo = Lesson(
        id = "adv_algorithm",
        biome = Biome.CANOPY,
        order = 3,
        type = LessonType.PUZZLE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_adv_algo_title,
        descriptionRes = R.string.lesson_adv_algo_desc,
        xpReward = 65, sunReward = 20, waterReward = 20,
        advanced = true,
        steps = listOf(
            LessonStep(AgeAdaptiveText(R.string.step_adv_algo_1_pro), TerraExpression.FOCUSED),
        ),
        puzzle = BlockPuzzle(
            prompt = AgeAdaptiveText(R.string.puzzle_adv_algo_pro),
            language = CodeLanguage.PYTHON,
            solution = listOf(
                "seeds = [\"fern\", \"moss\", \"vine\"]",
                "target = \"moss\"",
                "found = False",
                "for s in seeds:",
                "    if s == target:",
                "        found = True",
                "print(found)",
            ),
            distractors = listOf("found = \"maybe\"", "while True:"),
        ),
    )

    private val advDebug = Lesson(
        id = "adv_debug",
        biome = Biome.CANOPY,
        order = 4,
        type = LessonType.CODE,
        language = CodeLanguage.PYTHON,
        titleRes = R.string.lesson_adv_debug_title,
        descriptionRes = R.string.lesson_adv_debug_desc,
        xpReward = 70, sunReward = 25, waterReward = 20,
        advanced = true,
        steps = listOf(
            LessonStep(AgeAdaptiveText(R.string.step_adv_debug_1_pro), TerraExpression.CONFUSED),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.PYTHON,
            starterCode = "values = [10, 20, 30]\ntotal = 0\nfor v in values:\n    total = total - v\naverage = totl / 3\nprint(\"average:\", average)\n",
            instruction = AgeAdaptiveText(R.string.challenge_adv_debug_pro),
            hint = AgeAdaptiveText(R.string.hint_adv_debug_pro),
            checks = listOf(ChallengeCheck.RunsCleanly, ChallengeCheck.OutputContains("average: 20")),
            successLabel = "average: 20",
        ),
    )

    private val advCapstone = Lesson(
        id = "adv_capstone",
        biome = Biome.CANOPY,
        order = 5,
        type = LessonType.CODE,
        language = CodeLanguage.HTML,
        titleRes = R.string.lesson_adv_capstone_title,
        descriptionRes = R.string.lesson_adv_capstone_desc,
        xpReward = 100, sunReward = 50, waterReward = 30,
        masteryReward = 5,
        badgeId = BadgeCatalog.CANOPY_MASTER,
        advanced = true,
        steps = listOf(
            LessonStep(AgeAdaptiveText(R.string.step_adv_capstone_1_pro), TerraExpression.PROUD),
        ),
        challenge = CodeChallenge(
            language = CodeLanguage.HTML,
            starterCode = "<!-- Capstone: your Digital Garden -->\n",
            instruction = AgeAdaptiveText(R.string.challenge_adv_capstone_pro),
            hint = AgeAdaptiveText(R.string.hint_adv_capstone_pro),
            checks = listOf(
                ChallengeCheck.HtmlHasTag("h1"),
                ChallengeCheck.HtmlHasTag("p"),
                ChallengeCheck.HtmlHasTag("li"),
                ChallengeCheck.HtmlHasTag("style"),
            ),
        ),
    )

    /** All lessons, in canonical path order. */
    val all: List<Lesson> = listOf(
        webIntro, webHeading, webParagraphs, webStructure, webLinks, webImages, webLists, webCss, webProject,
        pyPrint, pyVariables, pyStrNum, pyOrder, pyCond, pyLoops, pyLoopPuzzle, pyLists, pyFunctions, pyDebug,
        cssLayout, htmlForm, pyLogic, pyData, pyModules, projectCard,
        advTools, advWeb, advPy, advAlgo, advDebug, advCapstone,
    )

    val byId: Map<String, Lesson> = all.associateBy { it.id }

    fun lessonsFor(biome: Biome): List<Lesson> =
        all.filter { it.biome == biome }.sortedBy { it.order }

    fun indexOf(lesson: Lesson): Int = all.indexOfFirst { it.id == lesson.id }

    fun nextAfter(lessonId: String): Lesson? {
        val idx = all.indexOfFirst { it.id == lessonId }
        return if (idx >= 0 && idx < all.lastIndex) all[idx + 1] else null
    }
}
