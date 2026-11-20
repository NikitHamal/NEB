package com.neb.ians.ui.screens.notes

/** Pure Markdown counting helpers for the note body. */
object NoteFormatting {
    private val checkLine = Regex("^(\\s*[-*+]\\s)\\[([ xX])](\\s.*)?$")

    fun checkProgress(body: String): Pair<Int, Int> {
        var done = 0
        var total = 0
        for (line in body.lineSequence()) {
            val m = checkLine.find(line) ?: continue
            total++
            if (m.groupValues[2].lowercase() == "x") done++
        }
        return done to total
    }

    fun wordCount(body: String): Int = body.split(Regex("\\s+")).count { w -> w.any { it.isLetterOrDigit() } }
}
