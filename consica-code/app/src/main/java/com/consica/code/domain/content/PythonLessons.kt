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
 * Sunny Meadow — the beginner Python track. From the first print() all the
 * way to a tiny guessing game.
 */
internal object PythonLessons {

    val lessons: List<Lesson> = listOf(

        // ── 1. print() ──────────────────────────────────────────────────────
        Lesson(
            id = "py_print",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_print_title,
            descriptionRes = R.string.lesson_py_print_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 1,
            xpReward = 50,
            sunReward = 10,
            badgeId = "python_hatchling",
            ecosystemItemId = "sunflower",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_print_step1_kid,
                    teenTextRes = R.string.lesson_py_print_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_print_step2_kid,
                    teenTextRes = R.string.lesson_py_print_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "print(\"Hello, meadow!\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_print_step3_kid,
                    teenTextRes = R.string.lesson_py_print_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Say hello to the meadow\n",
                instructionRes = R.string.lesson_py_print_instruction,
                hintRes = R.string.lesson_py_print_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "print\\s*\\("),
                        ChallengeValidation.OutputContains(needles = listOf("Hello, meadow")),
                    ),
                ),
            ),
        ),

        // ── 2. Variables ────────────────────────────────────────────────────
        Lesson(
            id = "py_variables",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_variables_title,
            descriptionRes = R.string.lesson_py_variables_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 2,
            xpReward = 50,
            waterReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_variables_step1_kid,
                    teenTextRes = R.string.lesson_py_variables_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_variables_step2_kid,
                    teenTextRes = R.string.lesson_py_variables_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "plant_name = \"Sunflower\"\nplant_age = 3\nprint(f\"{plant_name} is {plant_age} years old\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_variables_step3_kid,
                    teenTextRes = R.string.lesson_py_variables_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Two labelled jars, ready to use\nplant_name = \"Sunflower\"\nplant_age = 3\n# Print a sentence using both variables\n",
                instructionRes = R.string.lesson_py_variables_instruction,
                hintRes = R.string.lesson_py_variables_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "plant_name"),
                        ChallengeValidation.OutputContains(needles = listOf("Sunflower", "3")),
                    ),
                ),
            ),
        ),

        // ── 3. Strings and numbers ──────────────────────────────────────────
        Lesson(
            id = "py_strings_numbers",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_strings_numbers_title,
            descriptionRes = R.string.lesson_py_strings_numbers_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 3,
            xpReward = 55,
            sunReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_strings_numbers_step1_kid,
                    teenTextRes = R.string.lesson_py_strings_numbers_step1_teen,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_strings_numbers_step2_kid,
                    teenTextRes = R.string.lesson_py_strings_numbers_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "seeds = 4 + 3\nword = \"meadow\"\nprint(seeds)\nprint(word.upper())",
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Seeds add up, words shout\nseeds = 4\nseeds = seeds + 3\nword = \"meadow\"\n# Print the seed total, then the word in UPPERCASE\n",
                instructionRes = R.string.lesson_py_strings_numbers_instruction,
                hintRes = R.string.lesson_py_strings_numbers_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.OutputContains(needles = listOf("7")),
                        ChallengeValidation.OutputContains(needles = listOf("MEADOW"), ignoreCase = false),
                    ),
                ),
            ),
        ),

        // ── 4. input() ──────────────────────────────────────────────────────
        Lesson(
            id = "py_input",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_input_title,
            descriptionRes = R.string.lesson_py_input_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 4,
            xpReward = 55,
            waterReward = 5,
            ecosystemItemId = "bee",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_input_step1_kid,
                    teenTextRes = R.string.lesson_py_input_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_input_step2_kid,
                    teenTextRes = R.string.lesson_py_input_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "name = input()\nprint(f\"Hello, {name}!\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_input_step3_kid,
                    teenTextRes = R.string.lesson_py_input_step3_teen,
                    expression = TerraExpression.HAPPY,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Ask for a name, then greet that friend\nname = input()\n# Now print a friendly greeting using the name\n",
                instructionRes = R.string.lesson_py_input_instruction,
                hintRes = R.string.lesson_py_input_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "input\\s*\\("),
                        ChallengeValidation.OutputContains(needles = listOf("Terra")),
                    ),
                ),
                stdin = listOf("Terra"),
            ),
        ),

        // ── 5. Conditionals ─────────────────────────────────────────────────
        Lesson(
            id = "py_conditionals",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_conditionals_title,
            descriptionRes = R.string.lesson_py_conditionals_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 5,
            xpReward = 60,
            sunReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_conditionals_step1_kid,
                    teenTextRes = R.string.lesson_py_conditionals_step1_teen,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_conditionals_step2_kid,
                    teenTextRes = R.string.lesson_py_conditionals_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "if sun_level > 5:\n    print(\"Sunny day!\")\nelse:\n    print(\"Cloudy day\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_conditionals_step3_kid,
                    teenTextRes = R.string.lesson_py_conditionals_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Weather check for the meadow\nsun_level = 8\n# If sun_level is more than 5, print Sunny day!\n# Otherwise print Cloudy day\n",
                instructionRes = R.string.lesson_py_conditionals_instruction,
                hintRes = R.string.lesson_py_conditionals_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "if\\s+"),
                        ChallengeValidation.OutputContains(needles = listOf("Sunny day")),
                    ),
                ),
            ),
        ),

        // ── 6. Loops ────────────────────────────────────────────────────────
        Lesson(
            id = "py_loops",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_loops_title,
            descriptionRes = R.string.lesson_py_loops_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 6,
            xpReward = 65,
            sunReward = 10,
            badgeId = "loop_ranger",
            ecosystemItemId = "butterfly",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_loops_step1_kid,
                    teenTextRes = R.string.lesson_py_loops_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_loops_step2_kid,
                    teenTextRes = R.string.lesson_py_loops_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "for i in range(5):\n    print(f\"Butterfly {i + 1}\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_loops_step3_kid,
                    teenTextRes = R.string.lesson_py_loops_step3_teen,
                    expression = TerraExpression.HAPPY,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Five butterflies are visiting the meadow\n# Use a for loop with range to greet each one\n",
                instructionRes = R.string.lesson_py_loops_instruction,
                hintRes = R.string.lesson_py_loops_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "for\\s+\\w+\\s+in\\s+range"),
                        ChallengeValidation.OutputContains(needles = listOf("Butterfly")),
                    ),
                ),
            ),
        ),

        // ── 7. Lists ────────────────────────────────────────────────────────
        Lesson(
            id = "py_lists",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_lists_title,
            descriptionRes = R.string.lesson_py_lists_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 7,
            xpReward = 65,
            waterReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_lists_step1_kid,
                    teenTextRes = R.string.lesson_py_lists_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_lists_step2_kid,
                    teenTextRes = R.string.lesson_py_lists_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "seeds = [\"sunflower\", \"fern\", \"pine\"]\nseeds.append(\"lotus\")\nprint(seeds)\nprint(len(seeds))",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_lists_step3_kid,
                    teenTextRes = R.string.lesson_py_lists_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Your seed pouch\nseeds = [\"sunflower\", \"fern\", \"pine\"]\n# Add the word lotus with append, then print the list and how many seeds you have\n",
                instructionRes = R.string.lesson_py_lists_instruction,
                hintRes = R.string.lesson_py_lists_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "\\.append\\s*\\("),
                        ChallengeValidation.OutputContains(needles = listOf("lotus", "4")),
                    ),
                ),
            ),
        ),

        // ── 8. Functions ────────────────────────────────────────────────────
        Lesson(
            id = "py_functions",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_functions_title,
            descriptionRes = R.string.lesson_py_functions_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 8,
            xpReward = 70,
            sunReward = 10,
            badgeId = "function_forester",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_functions_step1_kid,
                    teenTextRes = R.string.lesson_py_functions_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_functions_step2_kid,
                    teenTextRes = R.string.lesson_py_functions_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "def greet(name):\n    print(f\"Namaste, {name}!\")\n\ngreet(\"Terra\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_functions_step3_kid,
                    teenTextRes = R.string.lesson_py_functions_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# A reusable greeting machine\ndef greet(name):\n    print(\"change me\")\n\ngreet(\"Terra\")\ngreet(\"Asha\")\n",
                instructionRes = R.string.lesson_py_functions_instruction,
                hintRes = R.string.lesson_py_functions_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "def\\s+greet"),
                        ChallengeValidation.OutputContains(needles = listOf("Namaste, Terra", "Namaste, Asha")),
                    ),
                ),
            ),
        ),

        // ── 9. Debugging puzzle ─────────────────────────────────────────────
        Lesson(
            id = "py_debugging",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_debugging_title,
            descriptionRes = R.string.lesson_py_debugging_desc,
            type = LessonType.PUZZLE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 9,
            xpReward = 70,
            waterReward = 10,
            badgeId = "bug_squasher",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_debugging_step1_kid,
                    teenTextRes = R.string.lesson_py_debugging_step1_teen,
                    expression = TerraExpression.CONFUSED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_debugging_step2_kid,
                    teenTextRes = R.string.lesson_py_debugging_step2_teen,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_debugging_step3_kid,
                    teenTextRes = R.string.lesson_py_debugging_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            puzzle = BlockPuzzle(
                promptRes = R.string.lesson_py_debugging_instruction,
                hintRes = R.string.lesson_py_debugging_hint,
                language = TrackLanguage.PYTHON,
                blocks = listOf(
                    PuzzleBlock(code = "plants = [\"fern\", \"moss\", \"lily\"]"),
                    PuzzleBlock(code = "watered = 0"),
                    PuzzleBlock(code = "for plant in plants:"),
                    PuzzleBlock(code = "print(f\"Watering the {plant}\")", indent = 1),
                    PuzzleBlock(code = "watered = watered + 1", indent = 1),
                    PuzzleBlock(code = "print(f\"All done! {watered} plants are happy.\")"),
                ),
            ),
        ),

        // ── 10. Guess-the-number game ───────────────────────────────────────
        Lesson(
            id = "py_guess_game",
            biomeId = "sunny_meadow",
            titleRes = R.string.lesson_py_guess_game_title,
            descriptionRes = R.string.lesson_py_guess_game_desc,
            type = LessonType.CODE,
            language = TrackLanguage.PYTHON,
            path = LearningPath.BEGINNER_PYTHON,
            order = 10,
            xpReward = 80,
            sunReward = 15,
            waterReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_py_guess_game_step1_kid,
                    teenTextRes = R.string.lesson_py_guess_game_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_guess_game_step2_kid,
                    teenTextRes = R.string.lesson_py_guess_game_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "if guess < secret:\n    print(\"Too low!\")\nelif guess > secret:\n    print(\"Too high!\")\nelse:\n    print(\"Correct!\")",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_py_guess_game_step3_kid,
                    teenTextRes = R.string.lesson_py_guess_game_step3_teen,
                    expression = TerraExpression.PROUD,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.PYTHON,
                starterCode = "# Terra is thinking of a number...\nsecret = 7\nguess = int(input())\n# Tell the player: Too low!, Too high!, or Correct!\n",
                instructionRes = R.string.lesson_py_guess_game_instruction,
                hintRes = R.string.lesson_py_guess_game_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "if\\s+"),
                        ChallengeValidation.OutputContains(needles = listOf("Correct")),
                    ),
                ),
                stdin = listOf("7"),
            ),
        ),
    )
}
