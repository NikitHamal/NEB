package com.consica.code.domain.content

import androidx.annotation.StringRes
import com.consica.code.R
import com.consica.code.core.model.EcosystemItemType

/**
 * Lesson CONTENT layer — deliberately separate from any UI composable so it can be localized
 * (or shipped as offline language packs) later without touching UI code. Display titles route
 * through string resources; longer goal/intro copy is kept here in English for v1 and can be
 * promoted to resources or a downloadable content pack per language.
 */

enum class CodeLang(val id: String) { HTML("html"), PYTHON("python") }

enum class LessonKind { CODE, PUZZLE }

/** How we decide a code lesson was solved. Substring checks keep validation offline & simple. */
enum class ValidateOn { CODE, OUTPUT }

/** Optional per-age-tone intro lines (resource-backed for the showcase first lesson). */
data class AgeIntro(
    @StringRes val kid: Int,
    @StringRes val teen: Int,
    @StringRes val pro: Int,
)

/** A drag-and-drop ordering puzzle. [blocksInOrder] is the correct sequence; UI shuffles it. */
data class BlockPuzzle(
    val prompt: String,
    val blocksInOrder: List<String>,
)

data class Lesson(
    val id: String,
    val trackId: String,
    @StringRes val titleRes: Int,
    val kind: LessonKind,
    val lang: CodeLang? = null,
    val starterCode: String = "",
    val goal: String = "",
    val successNeedles: List<String> = emptyList(),
    val validateOn: ValidateOn = ValidateOn.CODE,
    val puzzle: BlockPuzzle? = null,
    val intro: AgeIntro? = null,
    @StringRes val goalRes: Int? = null,
    val xp: Int = 20,
    val sun: Int = 5,
    val water: Int = 3,
    val mastery: Int = 1,
    val grow: EcosystemItemType = EcosystemItemType.SPROUT,
    val badgeId: String? = null,
    val difficulty: Int = 1,
)

data class Track(
    val id: String,
    @StringRes val titleRes: Int,
    val lessonIds: List<String>,
)

object LessonCatalog {

    val seedLesson = Lesson(
        id = "seed_html_heading",
        trackId = "web_beginner",
        titleRes = R.string.lesson_seed_title,
        kind = LessonKind.CODE,
        lang = CodeLang.HTML,
        starterCode = "<!-- Write a heading that says Sprout -->\n",
        successNeedles = listOf("<h1", "sprout", "</h1>"),
        validateOn = ValidateOn.CODE,
        intro = AgeIntro(
            R.string.lesson_seed_intro_kid,
            R.string.lesson_seed_intro_teen,
            R.string.lesson_seed_intro_pro,
        ),
        goalRes = R.string.lesson_seed_goal,
        xp = 30, sun = 10, water = 5, mastery = 1,
        grow = EcosystemItemType.SPROUT,
        badgeId = "first_sprout",
        difficulty = 1,
    )

    val all: List<Lesson> = listOf(
        seedLesson,
        // ---- Beginner Web ----
        Lesson(
            "web_tags", "web_beginner", R.string.lesson_html_tags, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<p>Write a paragraph about your favourite tree.</p>\n",
            goal = "Use a <p> paragraph tag.",
            successNeedles = listOf("<p", "</p>"),
            grow = EcosystemItemType.FLOWER, badgeId = null, difficulty = 1,
        ),
        Lesson(
            "web_structure", "web_beginner", R.string.lesson_html_structure, LessonKind.PUZZLE,
            puzzle = BlockPuzzle(
                "Order a basic HTML document.",
                listOf("<html>", "<head>", "<title>My Page</title>", "</head>", "<body>", "<h1>Hi</h1>", "</body>", "</html>"),
            ),
            goal = "Arrange the document from outside in.",
            grow = EcosystemItemType.TREE, difficulty = 2,
        ),
        Lesson(
            "web_headings", "web_beginner", R.string.lesson_headings_paragraphs, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<h1>Title</h1>\n<p>...</p>\n",
            goal = "Add a heading and a paragraph.",
            successNeedles = listOf("<h1", "<p"),
            grow = EcosystemItemType.FLOWER, difficulty = 1,
        ),
        Lesson(
            "web_links_images", "web_beginner", R.string.lesson_links_images, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<a href=\"https://example.com\">A link</a>\n",
            goal = "Create a link with an <a> tag.",
            successNeedles = listOf("<a", "href", "</a>"),
            grow = EcosystemItemType.BUTTERFLY, difficulty = 2,
        ),
        Lesson(
            "web_lists", "web_beginner", R.string.lesson_lists, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<ul>\n  <li>Seed</li>\n</ul>\n",
            goal = "Make a list with <ul> and <li>.",
            successNeedles = listOf("<ul", "<li", "</ul>"),
            grow = EcosystemItemType.MUSHROOM, difficulty = 2,
        ),
        Lesson(
            "web_css", "web_beginner", R.string.lesson_simple_css, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<h1 style=\"color:green\">Leafy</h1>\n",
            goal = "Colour a heading green with style.",
            successNeedles = listOf("style", "color", "green"),
            grow = EcosystemItemType.TREE, badgeId = "web_explorer", difficulty = 2,
        ),
        // ---- Beginner Python ----
        Lesson(
            "py_print", "py_beginner", R.string.lesson_py_print, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "print(\"Hello, garden!\")\n",
            goal = "Print a friendly message.",
            successNeedles = listOf("hello"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.SPROUT, badgeId = "first_print", difficulty = 1,
        ),
        Lesson(
            "py_variables", "py_beginner", R.string.lesson_py_variables, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "tree = \"oak\"\nprint(tree)\n",
            goal = "Store a value in a variable and print it.",
            successNeedles = listOf("oak"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.FLOWER, difficulty = 1,
        ),
        Lesson(
            "py_strings_numbers", "py_beginner", R.string.lesson_py_strings_numbers, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "seeds = 3 + 4\nprint(seeds)\n",
            goal = "Add two numbers and print the result.",
            successNeedles = listOf("7"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.WATER, difficulty = 1,
        ),
        Lesson(
            "py_input", "py_beginner", R.string.lesson_py_input, LessonKind.PUZZLE,
            puzzle = BlockPuzzle(
                "Order code that greets a user by name.",
                listOf("name = input(\"Name? \")", "greeting = \"Hi \" + name", "print(greeting)"),
            ),
            goal = "Read input, build a message, print it.",
            grow = EcosystemItemType.BIRD, difficulty = 2,
        ),
        Lesson(
            "py_conditionals", "py_beginner", R.string.lesson_py_conditionals, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "rain = 5\nif rain > 3:\n    print(\"plants are happy\")\n",
            goal = "Print only when rain is greater than 3.",
            successNeedles = listOf("happy"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.FLOWER, difficulty = 2,
        ),
        Lesson(
            "py_loops", "py_beginner", R.string.lesson_py_loops, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "for i in range(3):\n    print(\"leaf\")\n",
            goal = "Print 'leaf' three times with a loop.",
            successNeedles = listOf("leaf"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.TREE, difficulty = 2,
        ),
        Lesson(
            "py_lists", "py_beginner", R.string.lesson_py_lists, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "garden = [\"rose\", \"fern\"]\nprint(garden[0])\n",
            goal = "Print the first item of a list.",
            successNeedles = listOf("rose"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.MUSHROOM, difficulty = 2,
        ),
        Lesson(
            "py_functions", "py_beginner", R.string.lesson_py_functions, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "def grow():\n    print(\"growing\")\n\ngrow()\n",
            goal = "Define a function and call it.",
            successNeedles = listOf("growing"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.BIRD, badgeId = "python_explorer", difficulty = 3,
        ),
        // ---- Intermediate ----
        Lesson(
            "inter_css_layout", "intermediate", R.string.lesson_inter_css_layout, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<div style=\"display:flex;gap:8px\">\n  <span>A</span><span>B</span>\n</div>\n",
            goal = "Lay out boxes in a row with flex.",
            successNeedles = listOf("flex"),
            grow = EcosystemItemType.TREE, difficulty = 2,
        ),
        Lesson(
            "inter_forms", "intermediate", R.string.lesson_inter_forms, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<form>\n  <input placeholder=\"Your name\">\n</form>\n",
            goal = "Build a form with an input.",
            successNeedles = listOf("<form", "<input"),
            grow = EcosystemItemType.BUTTERFLY, difficulty = 2,
        ),
        Lesson(
            "inter_logic", "intermediate", R.string.lesson_inter_logic, LessonKind.PUZZLE,
            puzzle = BlockPuzzle(
                "Order a loop that counts down from 3.",
                listOf("n = 3", "while n > 0:", "    print(n)", "    n = n - 1", "print(\"liftoff\")"),
            ),
            goal = "Sequence a countdown loop.",
            grow = EcosystemItemType.BIRD, difficulty = 3,
        ),
        Lesson(
            "inter_data", "intermediate", R.string.lesson_inter_data, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "scores = {\"a\": 1, \"b\": 2}\nprint(scores[\"b\"])\n",
            goal = "Read a value from a dictionary.",
            successNeedles = listOf("2"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.MUSHROOM, badgeId = "logician", difficulty = 3,
        ),
        // ---- Advanced (16+) ----
        Lesson(
            "adv_workspace", "advanced", R.string.lesson_adv_workspace, LessonKind.CODE, CodeLang.HTML,
            starterCode = "<!DOCTYPE html>\n<html>\n<body>\n  <h1>Portfolio</h1>\n</body>\n</html>\n",
            goal = "Start a multi-section page in a workspace.",
            successNeedles = listOf("<!doctype", "<body"),
            grow = EcosystemItemType.TREE, difficulty = 3,
        ),
        Lesson(
            "adv_algorithms", "advanced", R.string.lesson_adv_algorithms, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "nums = [5, 2, 9]\nprint(max(nums))\n",
            goal = "Find the largest number.",
            successNeedles = listOf("9"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.BIRD, difficulty = 3,
        ),
        Lesson(
            "adv_capstone", "advanced", R.string.lesson_adv_capstone, LessonKind.CODE, CodeLang.PYTHON,
            starterCode = "def total(items):\n    return sum(items)\n\nprint(total([1,2,3,4]))\n",
            goal = "Write a function that sums a list.",
            successNeedles = listOf("10"), validateOn = ValidateOn.OUTPUT,
            grow = EcosystemItemType.TREE, badgeId = "capstone", difficulty = 3,
        ),
    )

    val tracks: List<Track> = listOf(
        Track("web_beginner", R.string.path_track_web_beginner,
            listOf("seed_html_heading", "web_tags", "web_structure", "web_headings", "web_links_images", "web_lists", "web_css")),
        Track("py_beginner", R.string.path_track_python_beginner,
            listOf("py_print", "py_variables", "py_strings_numbers", "py_input", "py_conditionals", "py_loops", "py_lists", "py_functions")),
        Track("intermediate", R.string.path_track_intermediate,
            listOf("inter_css_layout", "inter_forms", "inter_logic", "inter_data")),
        Track("advanced", R.string.path_track_advanced,
            listOf("adv_workspace", "adv_algorithms", "adv_capstone")),
    )

    private val byId = all.associateBy { it.id }
    fun byId(id: String): Lesson? = byId[id]

    fun track(id: String): Track? = tracks.firstOrNull { it.id == id }

    /** Ordered flat list across all tracks (used for the vertical biome map). */
    val ordered: List<Lesson> = tracks.flatMap { t -> t.lessonIds.mapNotNull { byId[it] } }

    /** The lesson immediately after [lessonId] in the ordered path, if any. */
    fun next(lessonId: String): Lesson? {
        val idx = ordered.indexOfFirst { it.id == lessonId }
        return if (idx >= 0 && idx + 1 < ordered.size) ordered[idx + 1] else null
    }
}
