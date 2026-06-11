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
 * Advanced biomes:
 *  - Mountain Peaks — multi-step projects, clean code and algorithmic thinking
 *  - Sky Canopy — concepts, creative coding and the capstone challenge
 * Every lesson here is flagged [Lesson.advanced].
 */
internal object AdvancedLessons {

    val lessons: List<Lesson> = mountainPeaksLessons + skyCanopyLessons

    // ═══════════════════════ MOUNTAIN PEAKS ════════════════════════════════

    private val mountainPeaksLessons: List<Lesson>
        get() = listOf(

            // ── 1. Multi-step web project ───────────────────────────────────
            Lesson(
                id = "adv_web_project",
                biomeId = "mountain_peaks",
                titleRes = R.string.lesson_adv_web_project_title,
                descriptionRes = R.string.lesson_adv_web_project_desc,
                type = LessonType.PROJECT,
                language = TrackLanguage.HTML,
                path = LearningPath.ADVANCED,
                order = 1,
                xpReward = 160,
                sunReward = 20,
                waterReward = 15,
                masteryReward = 3,
                badgeId = "project_pioneer",
                ecosystemItemId = "waterfall",
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_web_project_step1_kid,
                        teenTextRes = R.string.lesson_adv_web_project_step1_teen,
                        adultTextRes = R.string.lesson_adv_web_project_step1_adult,
                        expression = TerraExpression.PROFESSIONAL,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_web_project_step2_kid,
                        teenTextRes = R.string.lesson_adv_web_project_step2_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_web_project_step3_kid,
                        teenTextRes = R.string.lesson_adv_web_project_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.HTML,
                    starterCode = "<!DOCTYPE html>\n<html>\n<head>\n  <title>Mountain Lodge</title>\n  <style>\n    /* Step 3: style the page — background color and a font-family */\n  </style>\n</head>\n<body>\n  <header>\n    <!-- Step 1: lodge name in an h1 and a tagline paragraph -->\n  </header>\n  <main>\n    <!-- Step 2: a section with an h2 and a ul listing three trails -->\n  </main>\n  <footer>\n    <p>Built at 4000 metres</p>\n  </footer>\n</body>\n</html>",
                    instructionRes = R.string.lesson_adv_web_project_instruction,
                    hintRes = R.string.lesson_adv_web_project_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.HtmlHasTag(tag = "h1"),
                            ChallengeValidation.HtmlHasTag(tag = "h2"),
                            ChallengeValidation.HtmlHasTag(tag = "ul"),
                            ChallengeValidation.HtmlHasTag(tag = "li"),
                            ChallengeValidation.CodeMatches(pattern = "background(-color)?\\s*:"),
                            ChallengeValidation.CodeMatches(pattern = "font-family\\s*:"),
                        ),
                    ),
                ),
            ),

            // ── 2. Python scripts & clean code ──────────────────────────────
            Lesson(
                id = "adv_python_project",
                biomeId = "mountain_peaks",
                titleRes = R.string.lesson_adv_python_project_title,
                descriptionRes = R.string.lesson_adv_python_project_desc,
                type = LessonType.PROJECT,
                language = TrackLanguage.PYTHON,
                path = LearningPath.ADVANCED,
                order = 2,
                xpReward = 160,
                sunReward = 20,
                waterReward = 10,
                masteryReward = 3,
                badgeId = "clean_coder",
                ecosystemItemId = "snow_lotus",
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_python_project_step1_kid,
                        teenTextRes = R.string.lesson_adv_python_project_step1_teen,
                        adultTextRes = R.string.lesson_adv_python_project_step1_adult,
                        expression = TerraExpression.PROFESSIONAL,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_python_project_step2_kid,
                        teenTextRes = R.string.lesson_adv_python_project_step2_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "def describe_trail(name, km):\n    print(f\"{name}: {km} km\")",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_python_project_step3_kid,
                        teenTextRes = R.string.lesson_adv_python_project_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# Trail report generator\n# Step 1: write a function describe_trail(name, km) that prints one clean line\n# Step 2: loop through the trails below and describe each one\n# Step 3: print the total distance of all trails\n\ntrail_names = [\"Lakeside Loop\", \"Pine Ridge\", \"Summit Path\"]\ntrail_kms = [4, 9, 13]\n\n# Your code below\n",
                    instructionRes = R.string.lesson_adv_python_project_instruction,
                    hintRes = R.string.lesson_adv_python_project_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "def\\s+\\w+"),
                            ChallengeValidation.CodeMatches(pattern = "for\\s+"),
                            ChallengeValidation.OutputContains(needles = listOf("Lakeside Loop", "26")),
                        ),
                    ),
                ),
            ),

            // ── 3. Debugging workflows puzzle ───────────────────────────────
            Lesson(
                id = "adv_debugging",
                biomeId = "mountain_peaks",
                titleRes = R.string.lesson_adv_debugging_title,
                descriptionRes = R.string.lesson_adv_debugging_desc,
                type = LessonType.PUZZLE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.ADVANCED,
                order = 3,
                xpReward = 130,
                waterReward = 10,
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_debugging_step1_kid,
                        teenTextRes = R.string.lesson_adv_debugging_step1_teen,
                        expression = TerraExpression.CONFUSED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_debugging_step2_kid,
                        teenTextRes = R.string.lesson_adv_debugging_step2_teen,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_debugging_step3_kid,
                        teenTextRes = R.string.lesson_adv_debugging_step3_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                ),
                puzzle = BlockPuzzle(
                    promptRes = R.string.lesson_adv_debugging_instruction,
                    hintRes = R.string.lesson_adv_debugging_hint,
                    language = TrackLanguage.PYTHON,
                    blocks = listOf(
                        PuzzleBlock(code = "fuel = 5"),
                        PuzzleBlock(code = "while fuel > 0:"),
                        PuzzleBlock(code = "print(f\"Fuel left: {fuel}\")", indent = 1),
                        PuzzleBlock(code = "fuel = fuel - 1", indent = 1),
                        PuzzleBlock(code = "print(\"Lander touched down safely!\")"),
                    ),
                    distractors = listOf(
                        PuzzleBlock(code = "fuel = fuel + 1", indent = 1),
                        PuzzleBlock(code = "while fuel < 0:"),
                    ),
                ),
            ),

            // ── 4. Algorithmic thinking ─────────────────────────────────────
            Lesson(
                id = "adv_algorithms",
                biomeId = "mountain_peaks",
                titleRes = R.string.lesson_adv_algorithms_title,
                descriptionRes = R.string.lesson_adv_algorithms_desc,
                type = LessonType.CODE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.ADVANCED,
                order = 4,
                xpReward = 150,
                sunReward = 15,
                badgeId = "algorithm_ace",
                ecosystemItemId = "eagle",
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_algorithms_step1_kid,
                        teenTextRes = R.string.lesson_adv_algorithms_step1_teen,
                        adultTextRes = R.string.lesson_adv_algorithms_step1_adult,
                        expression = TerraExpression.PROFESSIONAL,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_algorithms_step2_kid,
                        teenTextRes = R.string.lesson_adv_algorithms_step2_teen,
                        expression = TerraExpression.THINKING,
                        codeSnippet = "tallest = peaks[0]\nfor p in peaks:\n    if p > tallest:\n        tallest = p",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_adv_algorithms_step3_kid,
                        teenTextRes = R.string.lesson_adv_algorithms_step3_teen,
                        expression = TerraExpression.ENCOURAGING,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# Find the tallest peak WITHOUT using max()\npeaks = [8848, 8167, 8586, 8091]\ntallest = peaks[0]\n# Loop through peaks, update tallest, then print it\n",
                    instructionRes = R.string.lesson_adv_algorithms_instruction,
                    hintRes = R.string.lesson_adv_algorithms_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "for\\s+"),
                            ChallengeValidation.CodeMatches(pattern = "if\\s+"),
                            ChallengeValidation.OutputContains(needles = listOf("8848")),
                        ),
                    ),
                ),
            ),
        )

    // ═══════════════════════ SKY CANOPY ════════════════════════════════════

    private val skyCanopyLessons: List<Lesson>
        get() = listOf(

            // ── 1. What is an API? (offline concept lesson) ─────────────────
            Lesson(
                id = "sky_apis",
                biomeId = "sky_canopy",
                titleRes = R.string.lesson_sky_apis_title,
                descriptionRes = R.string.lesson_sky_apis_desc,
                type = LessonType.TUTORIAL,
                language = TrackLanguage.LOGIC,
                path = LearningPath.ADVANCED,
                order = 1,
                xpReward = 120,
                sunReward = 10,
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_apis_step1_kid,
                        teenTextRes = R.string.lesson_sky_apis_step1_teen,
                        adultTextRes = R.string.lesson_sky_apis_step1_adult,
                        expression = TerraExpression.HAPPY,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_apis_step2_kid,
                        teenTextRes = R.string.lesson_sky_apis_step2_teen,
                        adultTextRes = R.string.lesson_sky_apis_step2_adult,
                        expression = TerraExpression.THINKING,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_apis_step3_kid,
                        teenTextRes = R.string.lesson_sky_apis_step3_teen,
                        expression = TerraExpression.FOCUSED,
                        codeSnippet = "REQUEST:  GET /weather?city=Pokhara\nRESPONSE: { \"sky\": \"clear\", \"temp\": 21 }",
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_apis_step4_kid,
                        teenTextRes = R.string.lesson_sky_apis_step4_teen,
                        expression = TerraExpression.EXCITED,
                    ),
                ),
            ),

            // ── 2. Creative coding project ──────────────────────────────────
            Lesson(
                id = "sky_creative",
                biomeId = "sky_canopy",
                titleRes = R.string.lesson_sky_creative_title,
                descriptionRes = R.string.lesson_sky_creative_desc,
                type = LessonType.PROJECT,
                language = TrackLanguage.HTML,
                path = LearningPath.ADVANCED,
                order = 2,
                xpReward = 170,
                sunReward = 20,
                waterReward = 15,
                ecosystemItemId = "cloud_lantern",
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_creative_step1_kid,
                        teenTextRes = R.string.lesson_sky_creative_step1_teen,
                        expression = TerraExpression.EXCITED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_creative_step2_kid,
                        teenTextRes = R.string.lesson_sky_creative_step2_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_creative_step3_kid,
                        teenTextRes = R.string.lesson_sky_creative_step3_teen,
                        expression = TerraExpression.PROUD,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.HTML,
                    starterCode = "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    .sky {\n      /* Paint the whole sky with a background color */\n    }\n    .cloud {\n      /* Shape a soft cloud: background color + border-radius */\n    }\n  </style>\n</head>\n<body>\n  <div class=\"sky\">\n    <!-- Add an h1 title and at least two cloud divs -->\n  </div>\n</body>\n</html>",
                    instructionRes = R.string.lesson_sky_creative_instruction,
                    hintRes = R.string.lesson_sky_creative_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.HtmlHasTag(tag = "div"),
                            ChallengeValidation.HtmlHasTag(tag = "h1"),
                            ChallengeValidation.CodeMatches(pattern = "background(-color)?\\s*:"),
                            ChallengeValidation.CodeMatches(pattern = "border-radius\\s*:"),
                        ),
                    ),
                ),
            ),

            // ── 3. Capstone challenge ───────────────────────────────────────
            Lesson(
                id = "sky_capstone",
                biomeId = "sky_canopy",
                titleRes = R.string.lesson_sky_capstone_title,
                descriptionRes = R.string.lesson_sky_capstone_desc,
                type = LessonType.CODE,
                language = TrackLanguage.PYTHON,
                path = LearningPath.ADVANCED,
                order = 3,
                xpReward = 200,
                sunReward = 20,
                waterReward = 15,
                masteryReward = 3,
                badgeId = "capstone",
                ecosystemItemId = "rainbow",
                advanced = true,
                steps = listOf(
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_capstone_step1_kid,
                        teenTextRes = R.string.lesson_sky_capstone_step1_teen,
                        adultTextRes = R.string.lesson_sky_capstone_step1_adult,
                        expression = TerraExpression.PROFESSIONAL,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_capstone_step2_kid,
                        teenTextRes = R.string.lesson_sky_capstone_step2_teen,
                        expression = TerraExpression.FOCUSED,
                    ),
                    LessonStep(
                        kidTextRes = R.string.lesson_sky_capstone_step3_kid,
                        teenTextRes = R.string.lesson_sky_capstone_step3_teen,
                        expression = TerraExpression.PROUD,
                    ),
                ),
                challenge = CodeChallenge(
                    language = TrackLanguage.PYTHON,
                    starterCode = "# Capstone: Ecosystem health report\nspecies = [\"owl\", \"fern\", \"river fish\", \"snow lotus\"]\ncounts = [4, 12, 7, 2]\n\n# 1) Write a function health(count) that prints thriving (8 or more),\n#    stable (4 to 7) or needs care (under 4)\n# 2) Loop through species and report each one with its health\n# 3) Print the total count of all living things\n",
                    instructionRes = R.string.lesson_sky_capstone_instruction,
                    hintRes = R.string.lesson_sky_capstone_hint,
                    validation = ChallengeValidation.All(
                        rules = listOf(
                            ChallengeValidation.CodeMatches(pattern = "def\\s+\\w+"),
                            ChallengeValidation.CodeMatches(pattern = "for\\s+"),
                            ChallengeValidation.CodeMatches(pattern = "if\\s+"),
                            ChallengeValidation.OutputContains(
                                needles = listOf("thriving", "stable", "needs care", "25"),
                            ),
                        ),
                    ),
                ),
            ),
        )
}
