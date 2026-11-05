package com.neb.ians.ui.screens.notes

import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue

/** Pure Markdown editing helpers for the note body. */
object NoteFormatting {
    private val listLine = Regex("^(\\s*)(?:(\\d+)[.)]|[-*+])\\s(\\[[ xX]]\\s)?")
    private val checkLine = Regex("^(\\s*[-*+]\\s)\\[([ xX])](\\s.*)?$")

    /** Wraps the selection in [mark] (or unwraps it when it is already wrapped). */
    fun wrap(v: TextFieldValue, mark: String): TextFieldValue {
        val s = v.selection.min
        val e = v.selection.max
        val t = v.text
        if (s >= mark.length && e + mark.length <= t.length &&
            t.substring(s - mark.length, s) == mark && t.substring(e, e + mark.length) == mark
        ) {
            val out = t.removeRange(e, e + mark.length).removeRange(s - mark.length, s)
            return TextFieldValue(out, TextRange(s - mark.length, e - mark.length))
        }
        val out = t.substring(0, s) + mark + t.substring(s, e) + mark + t.substring(e)
        return if (s == e) TextFieldValue(out, TextRange(s + mark.length))
        else TextFieldValue(out, TextRange(s + mark.length, e + mark.length))
    }

    /** Toggles [prefix] on every line the selection touches. */
    fun prefixLines(v: TextFieldValue, prefix: String, strip: Regex? = null): TextFieldValue {
        val t = v.text
        val start = t.lastIndexOf('\n', (v.selection.min - 1).coerceAtLeast(-1)) + 1
        var end = t.indexOf('\n', v.selection.max)
        if (end < 0) end = t.length
        val lines = t.substring(start, end).split('\n')
        val allHave = lines.all { it.startsWith(prefix) }
        val changed = lines.map { line ->
            val bare = strip?.replaceFirst(line, "") ?: line
            if (allHave) line.removePrefix(prefix) else prefix + (if (line.startsWith(prefix)) line.removePrefix(prefix) else bare)
        }
        val block = changed.joinToString("\n")
        val out = t.substring(0, start) + block + t.substring(end)
        val delta = block.length - (end - start)
        return TextFieldValue(out, TextRange((v.selection.min + if (lines.size == 1) delta else 0).coerceAtLeast(start), start + block.length))
    }

    fun heading(v: TextFieldValue) = prefixLines(v, "## ", Regex("^#{1,6}\\s+"))
    fun bullet(v: TextFieldValue) = prefixLines(v, "- ", Regex("^(\\s*([-*+]|\\d+[.)])\\s+(\\[[ xX]]\\s)?)"))
    fun numbered(v: TextFieldValue) = prefixLines(v, "1. ", Regex("^(\\s*([-*+]|\\d+[.)])\\s+(\\[[ xX]]\\s)?)"))
    fun checklist(v: TextFieldValue) = prefixLines(v, "- [ ] ", Regex("^(\\s*([-*+]|\\d+[.)])\\s+(\\[[ xX]]\\s)?)"))
    fun quote(v: TextFieldValue) = prefixLines(v, "> ", Regex("^>\\s?"))

    fun code(v: TextFieldValue): TextFieldValue {
        val sel = v.text.substring(v.selection.min, v.selection.max)
        if (!sel.contains('\n')) return wrap(v, "`")
        val s = v.selection.min
        val e = v.selection.max
        val out = v.text.substring(0, s) + "```\n" + sel + "\n```" + v.text.substring(e)
        return TextFieldValue(out, TextRange(s + 4, s + 4 + sel.length))
    }

    fun divider(v: TextFieldValue): TextFieldValue {
        val s = v.selection.max
        val lead = if (s > 0 && v.text[s - 1] != '\n') "\n" else ""
        val ins = "$lead---\n"
        return TextFieldValue(v.text.substring(0, s) + ins + v.text.substring(s), TextRange(s + ins.length))
    }

    /**
     * After Enter on a list line, continues the list; Enter on an empty item ends it.
     * Returns null when the edit was not such an Enter.
     */
    fun continueList(old: TextFieldValue, new: TextFieldValue): TextFieldValue? {
        if (new.text.length != old.text.length + 1 || !new.selection.collapsed) return null
        val caret = new.selection.start
        if (caret == 0 || new.text[caret - 1] != '\n') return null
        val lineStart = new.text.lastIndexOf('\n', caret - 2) + 1
        val prev = new.text.substring(lineStart, caret - 1)
        val m = listLine.find(prev) ?: return null
        val rest = prev.substring(m.value.length)
        if (rest.isBlank()) {
            val out = new.text.substring(0, lineStart) + "\n" + new.text.substring(caret)
            return TextFieldValue(out, TextRange(lineStart + 1))
        }
        val indent = m.groupValues[1]
        val marker = when {
            m.groupValues[2].isNotEmpty() -> "${m.groupValues[2].toInt() + 1}. "
            else -> prev.substring(indent.length, prev.indexOf(' ', indent.length) + 1)
        }
        val box = if (m.groupValues[3].isNotEmpty()) "[ ] " else ""
        val ins = indent + marker + box
        val out = new.text.substring(0, caret) + ins + new.text.substring(caret)
        return TextFieldValue(out, TextRange(caret + ins.length))
    }

    /** Flips the checkbox on [lineIndex]; returns the new body or null if that line is not one. */
    fun toggleCheck(body: String, lineIndex: Int): String? {
        val lines = body.split('\n').toMutableList()
        val line = lines.getOrNull(lineIndex) ?: return null
        val m = checkLine.find(line) ?: return null
        val on = m.groupValues[2].lowercase() == "x"
        lines[lineIndex] = m.groupValues[1] + (if (on) "[ ]" else "[x]") + m.groupValues[3]
        return lines.joinToString("\n")
    }

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
