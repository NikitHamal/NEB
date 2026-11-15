package com.neb.ians.ui.screens.lab

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily

/** Cover patterns. All drawn flat in the accent colour, no gradient. */
internal enum class Pattern(val label: String) {
    None("None"), Dots("Dots"), Lines("Lines"), Grid("Grid"), Waves("Waves"),
    Rings("Rings"), Blobs("Blobs"), Stripes("Stripes"), Confetti("Confetti")
}

internal enum class Divider(val label: String) { Line("Line"), Dots("Dots"), Wave("Wave") }

/**
 * One look for a post: paper, ink, accent, type and a handful of decorations.
 * A post with no look (null on the server later) uses [defaultLook], so old posts never change.
 * Mirrors `web/static/web/js/pages/dynamic-posts-lab.js`; change both together.
 */
internal data class Look(
    val id: String,
    val name: String,
    val bg: Color,
    val ink: Color,
    val accent: Color,
    val soft: Color,
    val font: FontFamily,
    val pattern: Pattern,
    val dropCap: Boolean,
    val quoteBar: Boolean,
    val corner: Int,
    val tall: Boolean = false,
    val center: Boolean = false,
    val divider: Divider = Divider.Line,
    val mark: Boolean = true,
)

private val Serif = FontFamily.Serif
private val Sans = FontFamily.SansSerif
private val Mono = FontFamily.Monospace

internal val LOOKS = listOf(
    Look("paper", "Paper", Color(0xFFFBF8F1), Color(0xFF2B2620), Color(0xFFB4532A), Color(0xFFEFE7D6), Serif, Pattern.Lines, true, true, 28, divider = Divider.Dots),
    Look("ink", "Ink", Color(0xFF15171A), Color(0xFFEDEBE6), Color(0xFFE9B949), Color(0xFF24272C), Serif, Pattern.Rings, true, true, 28, tall = true),
    Look("garden", "Garden", Color(0xFFEAF3E4), Color(0xFF1F3322), Color(0xFF2F7D46), Color(0xFFD3E6C9), Sans, Pattern.Waves, false, true, 32, divider = Divider.Wave),
    Look("sunrise", "Sunrise", Color(0xFFFFF0E0), Color(0xFF3A2414), Color(0xFFE2622B), Color(0xFFFFDDBA), Sans, Pattern.Blobs, false, false, 36, tall = true, center = true),
    Look("blueprint", "Blueprint", Color(0xFFE6EEF7), Color(0xFF14283D), Color(0xFF1E5F9E), Color(0xFFCADBEC), Mono, Pattern.Grid, false, true, 16),
    Look("rose", "Rose", Color(0xFFFBEAEC), Color(0xFF3A1D22), Color(0xFFC03A52), Color(0xFFF5CFD5), Serif, Pattern.Dots, true, false, 32, center = true, divider = Divider.Dots),
    Look("chalk", "Chalk", Color(0xFF1E2B25), Color(0xFFE8EFE6), Color(0xFFF2D16B), Color(0xFF2C3D35), Mono, Pattern.Confetti, false, true, 20),
    Look("citrus", "Citrus", Color(0xFFFFF8D6), Color(0xFF33300E), Color(0xFF9A7B00), Color(0xFFF7EBA0), Sans, Pattern.Stripes, false, false, 24, tall = true),
    Look("ocean", "Ocean", Color(0xFFE3F3F2), Color(0xFF0E3231), Color(0xFF0F7B7B), Color(0xFFC3E4E2), Sans, Pattern.Waves, false, true, 32, divider = Divider.Wave),
    Look("mono", "Mono", Color(0xFFFFFFFF), Color(0xFF111111), Color(0xFF111111), Color(0xFFEDEDED), Serif, Pattern.None, true, true, 12, divider = Divider.Line),
)

internal val SWATCHES = listOf(
    Color(0xFFB4532A), Color(0xFFE9B949), Color(0xFF2F7D46), Color(0xFFE2622B),
    Color(0xFF1E5F9E), Color(0xFFC03A52), Color(0xFF6B4E9B), Color(0xFF0F7B7B),
)

internal enum class ListKind { Steps, Checks }

internal class Sample(
    val key: String, val label: String, val tag: String, val title: String, val lead: String,
    val mark: String, val callout: String, val quote: String, val kind: ListKind, val items: List<String>,
    val outro: String, val minutes: Int, val author: String,
)

internal val SAMPLES = listOf(
    Sample(
        "story", "Story", "Study tips", "How I stopped dreading Maths in Class 10",
        "Last year I could not finish a paper in time. Then I changed three small things, and the marks followed. Here is the plan I wish someone had handed me.",
        "changed three small things", "Time yourself from week one, not week ten.",
        "Do one chapter badly before you do one chapter perfectly.", ListKind.Steps,
        listOf("Solve the last five years of papers", "Keep a mistakes notebook", "Teach one friend each Sunday"),
        "None of this is clever. It is repetition with a little honesty, and it works because you can see progress every week.", 3, "Anita Gurung",
    ),
    Sample(
        "guide", "Guide", "Scholarships", "Your first month checklist for a scholarship form",
        "Most forms are rejected for missing papers, not weak marks. Keep one folder, tick as you go, and you will never panic on the last day.",
        "missing papers", "Scan every paper at 200 dpi or more.",
        "A complete form beats a perfect essay.", ListKind.Checks,
        listOf("Citizenship and birth certificate", "SEE and +2 mark sheets", "Recommendation letter", "Passport size photos", "Bank statement or income proof"),
        "Save the folder to your phone and your email. You will reuse it for every form that follows.", 4, "Bibek Thapa",
    ),
    Sample(
        "notice", "Notice", "Announcement", "Free model test this Saturday for Class 12",
        "Join us for a full length Physics and Chemistry model test, checked by teachers, with a solved paper shared the same evening.",
        "checked by teachers", "Bring a pen, a calculator and a bottle of water.",
        "Practice under exam rules, once, and the real day feels familiar.", ListKind.Steps,
        listOf("Register before Friday 6 pm", "Reach the hall by 9 am", "Collect your marked sheet on Monday"),
        "Seats are limited to the first 120 students.", 1, "NEBians Team",
    ),
)

/** The mixed feed demo: sample plus look, in order. A null look is the app default card. */
internal val FEED_MIX: List<Pair<Int, String?>> = listOf(
    0 to "paper", 2 to null, 1 to "chalk", 2 to "sunrise", 0 to "ocean", 1 to "citrus", 0 to "mono", 2 to "ink",
)
