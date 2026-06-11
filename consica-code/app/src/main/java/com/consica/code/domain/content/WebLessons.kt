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
 * Forest Floor — the beginner web track. Learners plant their very first
 * HTML and CSS seeds with Terra the Owl.
 */
internal object WebLessons {

    val lessons: List<Lesson> = listOf(

        // ── 1. What is the web? ─────────────────────────────────────────────
        Lesson(
            id = "web_intro",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_intro_title,
            descriptionRes = R.string.lesson_web_intro_desc,
            type = LessonType.TUTORIAL,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 1,
            xpReward = 40,
            sunReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_intro_step1_kid,
                    teenTextRes = R.string.lesson_web_intro_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_intro_step2_kid,
                    teenTextRes = R.string.lesson_web_intro_step2_teen,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_intro_step3_kid,
                    teenTextRes = R.string.lesson_web_intro_step3_teen,
                    expression = TerraExpression.EXCITED,
                    codeSnippet = "<h1>Namaste, world!</h1>",
                ),
            ),
        ),

        // ── 2. Planting a Seed (first heading) ──────────────────────────────
        Lesson(
            id = "web_first_heading",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_first_heading_title,
            descriptionRes = R.string.lesson_web_first_heading_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 2,
            xpReward = 50,
            sunReward = 10,
            waterReward = 5,
            badgeId = "first_sprout",
            ecosystemItemId = "sprout",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_first_heading_step1_kid,
                    teenTextRes = R.string.lesson_web_first_heading_step1_teen,
                    adultTextRes = R.string.lesson_web_first_heading_step1_adult,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_first_heading_step2_kid,
                    teenTextRes = R.string.lesson_web_first_heading_step2_teen,
                    adultTextRes = R.string.lesson_web_first_heading_step2_adult,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_first_heading_step3_kid,
                    teenTextRes = R.string.lesson_web_first_heading_step3_teen,
                    adultTextRes = R.string.lesson_web_first_heading_step3_adult,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "<h1>Sprout</h1>",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_first_heading_step4_kid,
                    teenTextRes = R.string.lesson_web_first_heading_step4_teen,
                    adultTextRes = R.string.lesson_web_first_heading_step4_adult,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<!-- Plant your first word-seed below -->\n<h1></h1>",
                instructionRes = R.string.lesson_web_first_heading_instruction,
                hintRes = R.string.lesson_web_first_heading_hint,
                validation = ChallengeValidation.HtmlHasTag(tag = "h1", textContains = "Sprout"),
            ),
        ),

        // ── 3. Page skeleton puzzle ─────────────────────────────────────────
        Lesson(
            id = "web_structure",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_structure_title,
            descriptionRes = R.string.lesson_web_structure_desc,
            type = LessonType.PUZZLE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 3,
            xpReward = 45,
            waterReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_structure_step1_kid,
                    teenTextRes = R.string.lesson_web_structure_step1_teen,
                    expression = TerraExpression.THINKING,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_structure_step2_kid,
                    teenTextRes = R.string.lesson_web_structure_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "<!DOCTYPE html>\n<html>\n  <head>...</head>\n  <body>...</body>\n</html>",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_structure_step3_kid,
                    teenTextRes = R.string.lesson_web_structure_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            puzzle = BlockPuzzle(
                promptRes = R.string.lesson_web_structure_instruction,
                hintRes = R.string.lesson_web_structure_hint,
                language = TrackLanguage.HTML,
                blocks = listOf(
                    PuzzleBlock(code = "<!DOCTYPE html>"),
                    PuzzleBlock(code = "<html>"),
                    PuzzleBlock(code = "<head><title>My Forest Page</title></head>", indent = 1),
                    PuzzleBlock(code = "<body>", indent = 1),
                    PuzzleBlock(code = "<h1>Hello from the forest!</h1>", indent = 2),
                    PuzzleBlock(code = "</body>", indent = 1),
                    PuzzleBlock(code = "</html>"),
                ),
            ),
        ),

        // ── 4. Headings and paragraphs ──────────────────────────────────────
        Lesson(
            id = "web_headings_paragraphs",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_headings_paragraphs_title,
            descriptionRes = R.string.lesson_web_headings_paragraphs_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 4,
            xpReward = 50,
            sunReward = 5,
            ecosystemItemId = "fern",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_headings_paragraphs_step1_kid,
                    teenTextRes = R.string.lesson_web_headings_paragraphs_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_headings_paragraphs_step2_kid,
                    teenTextRes = R.string.lesson_web_headings_paragraphs_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "<h2>The Hills</h2>\n<p>I love walking there after school.</p>",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_headings_paragraphs_step3_kid,
                    teenTextRes = R.string.lesson_web_headings_paragraphs_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<!-- Write a heading with h2 and a paragraph with p -->\n",
                instructionRes = R.string.lesson_web_headings_paragraphs_instruction,
                hintRes = R.string.lesson_web_headings_paragraphs_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.HtmlHasTag(tag = "h2"),
                        ChallengeValidation.HtmlHasTag(tag = "p"),
                    ),
                ),
            ),
        ),

        // ── 5. Links and images ─────────────────────────────────────────────
        Lesson(
            id = "web_links_images",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_links_images_title,
            descriptionRes = R.string.lesson_web_links_images_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 5,
            xpReward = 55,
            waterReward = 5,
            badgeId = "web_wanderer",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_links_images_step1_kid,
                    teenTextRes = R.string.lesson_web_links_images_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_links_images_step2_kid,
                    teenTextRes = R.string.lesson_web_links_images_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "<a href=\"https://example.com\">Visit the forest</a>\n<img src=\"owl.png\" alt=\"A friendly owl\">",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_links_images_step3_kid,
                    teenTextRes = R.string.lesson_web_links_images_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<!-- Add one link and one image below -->\n<p>Places I want to explore:</p>\n",
                instructionRes = R.string.lesson_web_links_images_instruction,
                hintRes = R.string.lesson_web_links_images_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.HtmlHasTag(tag = "a"),
                        ChallengeValidation.HtmlHasTag(tag = "img"),
                    ),
                ),
            ),
        ),

        // ── 6. Lists ────────────────────────────────────────────────────────
        Lesson(
            id = "web_lists",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_lists_title,
            descriptionRes = R.string.lesson_web_lists_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 6,
            xpReward = 55,
            sunReward = 5,
            ecosystemItemId = "mushroom",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_lists_step1_kid,
                    teenTextRes = R.string.lesson_web_lists_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_lists_step2_kid,
                    teenTextRes = R.string.lesson_web_lists_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "<ul>\n  <li>Fern</li>\n  <li>Mushroom</li>\n</ul>",
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<!-- Make a list of three things you found in the forest -->\n<h2>My Forest Finds</h2>\n",
                instructionRes = R.string.lesson_web_lists_instruction,
                hintRes = R.string.lesson_web_lists_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.HtmlHasTag(tag = "ul"),
                        ChallengeValidation.HtmlHasTag(tag = "li"),
                    ),
                ),
            ),
        ),

        // ── 7. First CSS ────────────────────────────────────────────────────
        Lesson(
            id = "web_simple_css",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_simple_css_title,
            descriptionRes = R.string.lesson_web_simple_css_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 7,
            xpReward = 60,
            waterReward = 5,
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_simple_css_step1_kid,
                    teenTextRes = R.string.lesson_web_simple_css_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_simple_css_step2_kid,
                    teenTextRes = R.string.lesson_web_simple_css_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "h1 {\n  color: green;\n}",
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_simple_css_step3_kid,
                    teenTextRes = R.string.lesson_web_simple_css_step3_teen,
                    expression = TerraExpression.ENCOURAGING,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<style>\n  /* Paint your heading below */\n</style>\n<h1>Forest Floor</h1>",
                instructionRes = R.string.lesson_web_simple_css_instruction,
                hintRes = R.string.lesson_web_simple_css_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.HtmlHasTag(tag = "style"),
                        ChallengeValidation.CodeMatches(pattern = "color\\s*:\\s*\\w"),
                    ),
                ),
            ),
        ),

        // ── 8. Colors and layout ────────────────────────────────────────────
        Lesson(
            id = "web_colors_layout",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_colors_layout_title,
            descriptionRes = R.string.lesson_web_colors_layout_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 8,
            xpReward = 65,
            sunReward = 10,
            badgeId = "css_artist",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_colors_layout_step1_kid,
                    teenTextRes = R.string.lesson_web_colors_layout_step1_teen,
                    expression = TerraExpression.HAPPY,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_colors_layout_step2_kid,
                    teenTextRes = R.string.lesson_web_colors_layout_step2_teen,
                    expression = TerraExpression.FOCUSED,
                    codeSnippet = "body {\n  background-color: #e8f5e9;\n  text-align: center;\n}",
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<style>\n  body {\n    /* Give the page a background color and center the text */\n  }\n</style>\n<h1>My Garden Page</h1>\n<p>Everything grows here.</p>",
                instructionRes = R.string.lesson_web_colors_layout_instruction,
                hintRes = R.string.lesson_web_colors_layout_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.CodeMatches(pattern = "background(-color)?\\s*:"),
                        ChallengeValidation.CodeMatches(pattern = "text-align\\s*:\\s*center"),
                    ),
                ),
            ),
        ),

        // ── 9. Mini page project ────────────────────────────────────────────
        Lesson(
            id = "web_mini_page",
            biomeId = "forest_floor",
            titleRes = R.string.lesson_web_mini_page_title,
            descriptionRes = R.string.lesson_web_mini_page_desc,
            type = LessonType.CODE,
            language = TrackLanguage.HTML,
            path = LearningPath.BEGINNER_WEB,
            order = 9,
            xpReward = 80,
            sunReward = 15,
            waterReward = 10,
            badgeId = "html_hero",
            steps = listOf(
                LessonStep(
                    kidTextRes = R.string.lesson_web_mini_page_step1_kid,
                    teenTextRes = R.string.lesson_web_mini_page_step1_teen,
                    expression = TerraExpression.EXCITED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_mini_page_step2_kid,
                    teenTextRes = R.string.lesson_web_mini_page_step2_teen,
                    expression = TerraExpression.FOCUSED,
                ),
                LessonStep(
                    kidTextRes = R.string.lesson_web_mini_page_step3_kid,
                    teenTextRes = R.string.lesson_web_mini_page_step3_teen,
                    expression = TerraExpression.PROUD,
                ),
            ),
            challenge = CodeChallenge(
                language = TrackLanguage.HTML,
                starterCode = "<!DOCTYPE html>\n<html>\n<head>\n  <title>My First Page</title>\n</head>\n<body>\n  <!-- Build your page here: a big heading, a paragraph, and a list -->\n</body>\n</html>",
                instructionRes = R.string.lesson_web_mini_page_instruction,
                hintRes = R.string.lesson_web_mini_page_hint,
                validation = ChallengeValidation.All(
                    rules = listOf(
                        ChallengeValidation.HtmlHasTag(tag = "h1"),
                        ChallengeValidation.HtmlHasTag(tag = "p"),
                        ChallengeValidation.HtmlHasTag(tag = "ul"),
                        ChallengeValidation.HtmlHasTag(tag = "li"),
                    ),
                ),
            ),
        ),
    )
}
