package com.neb.ians.ui.components

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.em

/*
 * Write the way it will look.
 *
 * The text a composer holds is still Markdown, so posts, replies, drafts and the server are untouched. What changes is what
 * the writer sees: the markers (**, *, ~~, `, ## , > , [..](..)) are hidden and their effect is drawn, live, while they type.
 * Nobody has to know the syntax; the toolbar writes the markers for them.
 *
 * Caret rules: a marker inside a line sticks to the left, so typing at the end of a bold word keeps it bold; a marker that
 * opens a line (## , > ) sticks to the right, so the caret lands after it.
 */

/** Colours the live view needs; the rest comes from the text style of the field. */
class LiveColors(val code: Color, val codeText: Color, val link: Color, val quote: Color, val muted: Color)

/** A styled run, in raw offsets, for toolbar state ("is the caret in bold"). */
data class LiveKind(val kind: String, val start: Int, val end: Int)

class LiveText(
    val raw: String,
    val visible: String,
    val styled: AnnotatedString,
    val hidden: BooleanArray,
    val originalToVisible: IntArray,
    val visibleToOriginal: IntArray,
    /** Raw offset of every visible character (exact, not sticky). */
    val charOrigin: IntArray,
    val kinds: List<LiveKind>
) {
    val offsetMapping: OffsetMapping = object : OffsetMapping {
        override fun originalToTransformed(offset: Int): Int = originalToVisible[offset.coerceIn(0, raw.length)]
        override fun transformedToOriginal(offset: Int): Int = visibleToOriginal[offset.coerceIn(0, visible.length)]
    }
}

enum class LineKind { Heading, Quote, Bullet, Number, Check }

object LiveMarkdown {
    private const val ZWSP = "\u200B"
    private const val ESCAPABLE = "\\`*_~|[]()#>-+.!$"
    private val headingRe = Regex("^(#{1,3}) ")
    private val bulletRe = Regex("^(\\s*)([-*+]) (?!\\[[ xX]] )")
    private val todoRe = Regex("^(\\s*)[-*+] \\[([ xX])] ")
    private val hrRe = Regex("^(-{3,}|\\*{3,}|_{3,})$")
    private val prefixRe = Regex("^(#{1,3} |> |[-*+] \\[[ xX]] |[-*+] |\\d+[.)] )")

    private val plain = LiveColors(Color.Unspecified, Color.Unspecified, Color.Unspecified, Color.Unspecified, Color.Unspecified)

    @Composable
    fun rememberTransformation(): VisualTransformation {
        val s = MaterialTheme.colorScheme
        return remember(s.surfaceContainerHighest, s.primary, s.onSurface, s.onSurfaceVariant) {
            transformation(LiveColors(s.surfaceContainerHighest, s.onSurface, s.primary, s.onSurfaceVariant, s.onSurfaceVariant))
        }
    }

    fun transformation(colors: LiveColors): VisualTransformation = object : VisualTransformation {
        private var lastRaw: String? = null
        private var last: LiveText? = null
        override fun filter(text: AnnotatedString): TransformedText {
            val cached = last
            val lt = if (cached != null && lastRaw == text.text) cached else transform(text.text, colors).also { last = it; lastRaw = text.text }
            return TransformedText(lt.styled, lt.offsetMapping)
        }
    }

    fun transform(raw: String, colors: LiveColors = plain): LiveText {
        val n = raw.length
        val hidden = BooleanArray(n)
        val replace = CharArray(n)
        val runs = ArrayList<Triple<Int, Int, SpanStyle>>()
        val kinds = ArrayList<LiveKind>()

        val codeStyle = SpanStyle(fontFamily = FontFamily.Monospace, background = colors.code, color = colors.codeText)
        val boldStyle = SpanStyle(fontWeight = FontWeight.Bold)
        val italicStyle = SpanStyle(fontStyle = FontStyle.Italic)
        val strikeStyle = SpanStyle(textDecoration = TextDecoration.LineThrough)
        val linkStyle = SpanStyle(color = colors.link, textDecoration = TextDecoration.Underline)

        fun hide(from: Int, to: Int) { for (i in from until to) if (i in 0 until n) hidden[i] = true }

        fun scanInline(from: Int, to: Int) {
            fun opens(i: Int, mark: Int): Boolean {
                if (i + mark >= to || raw[i + mark].isWhitespace()) return false
                if (i > from) { val p = raw[i - 1]; if (p.isLetterOrDigit() || p == raw[i]) return false }
                return true
            }
            fun closer(c: Char, mark: Int, start: Int): Int {
                var j = start + 1
                while (j + mark <= to) {
                    if (raw[j] == c && (mark == 1 || (j + 1 < to && raw[j + 1] == c)) && raw[j - 1] != '\\' && !hidden[j]) {
                        val before = raw[j - 1]
                        val after = if (j + mark < to) raw[j + mark] else ' '
                        val single = mark == 1 && (before == c || (j + 1 < to && raw[j + 1] == c))
                        if (!before.isWhitespace() && !after.isLetterOrDigit() && !single) return j
                    }
                    j++
                }
                return -1
            }
            var i = from
            while (i < to) {
                if (hidden[i]) { i++; continue }
                val c = raw[i]
                if (c == '\\' && i + 1 < to && ESCAPABLE.indexOf(raw[i + 1]) >= 0) { hidden[i] = true; i += 2; continue }
                if (c == '`') {
                    val j = raw.indexOf('`', i + 1)
                    if (j > i + 1 && j < to) {
                        hide(i, i + 1); hide(j, j + 1)
                        runs.add(Triple(i + 1, j, codeStyle)); kinds.add(LiveKind("code", i + 1, j))
                        i = j + 1; continue
                    }
                }
                if (c == '$') {
                    val j = raw.indexOf('$', i + 1)
                    if (j > i + 1 && j < to) { i = j + 1; continue }
                }
                if (c == '*' || c == '~' || c == '_') {
                    val dbl = i + 1 < to && raw[i + 1] == c
                    val mark = if (dbl) 2 else 1
                    if (c == '~' && !dbl) { i++; continue }
                    if (opens(i, mark)) {
                        val j = closer(c, mark, i + mark)
                        if (j > 0) {
                            hide(i, i + mark); hide(j, j + mark)
                            val kind = if (c == '~') "strike" else if (mark == 2) "bold" else "italic"
                            val style = if (c == '~') strikeStyle else if (mark == 2) boldStyle else italicStyle
                            runs.add(Triple(i + mark, j, style)); kinds.add(LiveKind(kind, i + mark, j))
                            i += mark; continue
                        }
                    }
                    i += mark; continue
                }
                if (c == '[') {
                    val mid = raw.indexOf("](", i + 1)
                    if (mid > i + 1 && mid < to) {
                        val text = raw.substring(i + 1, mid)
                        val close = raw.indexOf(')', mid + 2)
                        if (close in (mid + 2) until to && text.indexOf('[') < 0 && text.indexOf(']') < 0) {
                            hide(i, i + 1); hide(mid, close + 1)
                            runs.add(Triple(i + 1, mid, linkStyle)); kinds.add(LiveKind("link", i + 1, mid))
                            i = close + 1; continue
                        }
                    }
                }
                i++
            }
        }

        var inFence = false
        var ls = 0
        while (ls <= n) {
            var le = raw.indexOf('\n', ls)
            if (le < 0) le = n
            val line = raw.substring(ls, le)
            if (line.startsWith("```")) {
                inFence = !inFence
                hide(ls, le)
            } else if (inFence) {
                runs.add(Triple(ls, le, codeStyle))
            } else {
                var from = ls
                val heading = headingRe.find(line)
                val todo = todoRe.find(line)
                val bullet = bulletRe.find(line)
                when {
                    heading != null -> {
                        val level = heading.groupValues[1].length
                        hide(ls, ls + heading.value.length)
                        from = ls + heading.value.length
                        val size = if (level == 1) 1.4f else if (level == 2) 1.22f else 1.1f
                        runs.add(Triple(from, le, SpanStyle(fontSize = size.em, fontWeight = FontWeight.Bold)))
                        kinds.add(LiveKind("heading", from, le))
                    }
                    line.startsWith("> ") -> {
                        hide(ls, ls + 2); from = ls + 2
                        runs.add(Triple(from, le, SpanStyle(color = colors.quote, fontStyle = FontStyle.Italic)))
                        kinds.add(LiveKind("quote", from, le))
                    }
                    todo != null -> {
                        val ind = todo.groupValues[1].length
                        val done = todo.groupValues[2] != " "
                        hide(ls + ind, ls + ind + 3); hide(ls + ind + 4, ls + ind + 5)
                        replace[ls + ind + 3] = if (done) '\u2611' else '\u2610'
                        from = ls + ind + 6
                        if (done) runs.add(Triple(from, le, SpanStyle(textDecoration = TextDecoration.LineThrough, color = colors.muted)))
                        kinds.add(LiveKind("check", from, le))
                    }
                    bullet != null -> {
                        replace[ls + bullet.groupValues[1].length] = '\u2022'
                        from = ls + bullet.value.length
                        kinds.add(LiveKind("bullet", from, le))
                    }
                    hrRe.matches(line) -> {
                        for (i in ls until le) replace[i] = '\u2500'
                        from = le
                    }
                    Regex("^\\d+[.)] ").containsMatchIn(line) -> kinds.add(LiveKind("number", ls, le))
                }
                scanInline(from, le)
            }
            if (le >= n) break
            ls = le + 1
        }

        val o2t = IntArray(n + 1)
        val origin = IntArray(n)
        val sb = StringBuilder(n)
        var t = 0
        for (i in 0 until n) {
            o2t[i] = t
            if (!hidden[i]) {
                origin[t] = i
                sb.append(if (replace[i] != '\u0000') replace[i] else raw[i])
                t++
            }
        }
        o2t[n] = t
        val charOrigin = origin.copyOf(t)
        val t2o = IntArray(t + 1)
        for (k in 0..t) {
            val prevEnd = if (k == 0) 0 else charOrigin[k - 1] + 1
            val next = if (k < t) charOrigin[k] else n
            val atLineStart = prevEnd == 0 || raw[prevEnd - 1] == '\n'
            t2o[k] = if (next > prevEnd && atLineStart) next else prevEnd
        }
        val spans = ArrayList<AnnotatedString.Range<SpanStyle>>(runs.size)
        for ((s, e, style) in runs) {
            val a = o2t[s.coerceIn(0, n)]
            val b = o2t[e.coerceIn(0, n)]
            if (b > a) spans.add(AnnotatedString.Range(style, a, b))
        }
        val visible = sb.toString()
        return LiveText(raw, visible, AnnotatedString(visible, spans), hidden, o2t, t2o, charOrigin, kinds)
    }

    // ---------------------------------------------------------------- toolbar state

    /** Whether the caret (or the whole selection) sits inside a run of [kind]. */
    fun isActive(v: TextFieldValue, kind: String): Boolean {
        val lt = transform(v.text)
        val s = v.selection.min
        val e = v.selection.max
        return lt.kinds.any { it.kind == kind && it.start <= s && it.end >= e }
    }

    // ---------------------------------------------------------------- formatting

    private fun kindFor(mark: String) = when (mark) {
        "**" -> "bold"; "*" -> "italic"; "~~" -> "strike"; else -> "code"
    }

    /** Bold, italic, strike, code. Selection: wrap or unwrap. Caret in a word: that word. Caret elsewhere: starts the style. */
    fun toggleInline(v: TextFieldValue, mark: String): TextFieldValue {
        val t = v.text
        val lt = transform(t)
        val m = mark.length
        val kind = kindFor(mark)
        var s = v.selection.min.coerceIn(0, t.length)
        var e = v.selection.max.coerceIn(0, t.length)
        while (s < e && s < t.length && lt.hidden[s]) s++
        while (e > s && lt.hidden[e - 1]) e--
        var caretOnly = s == e
        var shift = 0
        if (caretOnly) {
            val exit = lt.kinds.firstOrNull { it.kind == kind && it.end == s && t.startsWith(mark, s) }
            if (exit != null) return TextFieldValue(t, TextRange(s + m))
            if (s > 0 && s < t.length && t[s - 1].isLetterOrDigit() && t[s].isLetterOrDigit()) {
                var a = s
                var b = s
                while (a > 0 && t[a - 1].isLetterOrDigit() && !lt.hidden[a - 1]) a--
                while (b < t.length && t[b].isLetterOrDigit() && !lt.hidden[b]) b++
                shift = s - a
                s = a; e = b; caretOnly = false
            } else {
                val out = t.substring(0, s) + mark + ZWSP + mark + t.substring(s)
                return TextFieldValue(out, TextRange(s + m + 1))
            }
        }
        val run = lt.kinds.firstOrNull { it.kind == kind && it.start <= s && it.end >= e }
        val sb = StringBuilder(t)
        if (run != null) {
            // right side first so earlier offsets stay valid
            if (e == run.end) sb.delete(e, e + m) else sb.insert(e, mark)
            if (s == run.start) sb.delete(s - m, s) else sb.insert(s, mark)
            val ns = if (s == run.start) s - m else s + m
            val ne = ns + (e - s)
            return if (shift > 0) TextFieldValue(sb.toString(), TextRange(ns + shift)) else TextFieldValue(sb.toString(), TextRange(ns, ne))
        }
        sb.insert(e, mark)
        sb.insert(s, mark)
        return if (shift > 0) TextFieldValue(sb.toString(), TextRange(s + m + shift)) else TextFieldValue(sb.toString(), TextRange(s + m, e + m))
    }

    private fun prefixFor(kind: LineKind, number: Int) = when (kind) {
        LineKind.Heading -> "## "; LineKind.Quote -> "> "; LineKind.Bullet -> "- "; LineKind.Number -> "$number. "; LineKind.Check -> "- [ ] "
    }

    private fun hasKind(line: String, kind: LineKind) = when (kind) {
        LineKind.Heading -> headingRe.containsMatchIn(line)
        LineKind.Quote -> line.startsWith("> ")
        LineKind.Bullet -> bulletRe.containsMatchIn(line)
        LineKind.Number -> Regex("^\\d+[.)] ").containsMatchIn(line)
        LineKind.Check -> todoRe.containsMatchIn(line)
    }

    /** Turns every touched line into a heading, quote, bullet, number or to-do; again removes it. */
    fun toggleLine(v: TextFieldValue, kind: LineKind): TextFieldValue {
        val t = v.text
        val sel = v.selection
        val start = t.lastIndexOf('\n', (sel.min - 1).coerceAtLeast(-1)) + 1
        var end = t.indexOf('\n', sel.max)
        if (end < 0) end = t.length
        val lines = t.substring(start, end).split('\n')
        val remove = lines.all { hasKind(it, kind) }
        var number = 1
        var firstDelta = 0
        val out = lines.mapIndexed { idx, line ->
            val old = prefixRe.find(line)?.value.orEmpty()
            val bare = line.removePrefix(old)
            val next = if (remove) bare else prefixFor(kind, number++) + bare
            if (idx == 0) firstDelta = next.length - line.length
            next
        }
        val block = out.joinToString("\n")
        val text = t.substring(0, start) + block + t.substring(end)
        return if (sel.collapsed) {
            val firstPrefix = if (remove) 0 else prefixFor(kind, 1).length
            TextFieldValue(text, TextRange(maxOf(start + firstPrefix, sel.min + firstDelta).coerceIn(0, text.length)))
        } else TextFieldValue(text, TextRange(start, start + block.length))
    }

    fun insertDivider(v: TextFieldValue): TextFieldValue {
        val t = v.text
        val at = v.selection.max.coerceIn(0, t.length)
        val lead = if (at > 0 && t[at - 1] != '\n') "\n" else ""
        val ins = "$lead---\n"
        return TextFieldValue(t.substring(0, at) + ins + t.substring(at), TextRange(at + ins.length))
    }

    fun insertCodeBlock(v: TextFieldValue): TextFieldValue {
        val t = v.text
        val s = v.selection.min.coerceIn(0, t.length)
        val e = v.selection.max.coerceIn(0, t.length)
        val lead = if (s > 0 && t[s - 1] != '\n') "\n" else ""
        val body = t.substring(s, e)
        val ins = "$lead```\n$body\n```\n"
        return TextFieldValue(t.substring(0, s) + ins + t.substring(e), TextRange(s + lead.length + 4 + body.length))
    }

    /** Adds a link: the selection (or the address itself) becomes the clickable text. */
    fun insertLink(v: TextFieldValue, url: String): TextFieldValue {
        val clean = url.trim().let { if (it.isNotEmpty() && !it.contains("://") && !it.startsWith("mailto:")) "https://$it" else it }
        if (clean.isEmpty()) return v
        val t = v.text
        val s = v.selection.min.coerceIn(0, t.length)
        val e = v.selection.max.coerceIn(0, t.length)
        val label = if (s == e) clean.removePrefix("https://").removePrefix("http://") else t.substring(s, e)
        val ins = "[$label]($clean)"
        return TextFieldValue(t.substring(0, s) + ins + t.substring(e), TextRange(s + ins.length))
    }

    /** Plain characters (maths symbols, Greek letters) at the caret. */
    fun insertSymbol(v: TextFieldValue, symbol: String): TextFieldValue {
        val t = v.text
        val s = v.selection.min.coerceIn(0, t.length)
        val e = v.selection.max.coerceIn(0, t.length)
        return TextFieldValue(t.substring(0, s) + symbol + t.substring(e), TextRange(s + symbol.length))
    }

    /** Without the invisible helper character used to start a style on an empty caret. */
    fun cleaned(text: String): String = text.replace(Regex("(\\*\\*|\\*|~~|`)\u200B\\1"), "").replace(ZWSP, "")
}
