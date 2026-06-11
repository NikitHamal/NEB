package com.consica.code.ui.playground

import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.VisualTransformation
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.theme.EditorText
import com.consica.code.ui.theme.SyntaxAttribute
import com.consica.code.ui.theme.SyntaxComment
import com.consica.code.ui.theme.SyntaxFunction
import com.consica.code.ui.theme.SyntaxKeyword
import com.consica.code.ui.theme.SyntaxNumber
import com.consica.code.ui.theme.SyntaxString
import com.consica.code.ui.theme.SyntaxTag

private val PythonKeywords = setOf(
    "def", "return", "if", "elif", "else", "while", "for", "in", "break", "continue",
    "and", "or", "not", "True", "False", "None", "pass", "import", "from", "class",
    "try", "except", "finally", "with", "as", "lambda", "global", "is",
)

private val PythonBuiltins = setOf(
    "print", "input", "len", "range", "str", "int", "float", "bool", "list",
    "abs", "min", "max", "sum", "round", "type", "sorted",
)

/**
 * Lightweight regex-free single-pass highlighter, fast enough to run on every
 * keystroke for lesson-sized programs.
 */
object SyntaxHighlighter {

    fun highlight(code: String, language: TrackLanguage): AnnotatedString = when (language) {
        TrackLanguage.PYTHON -> highlightPython(code)
        TrackLanguage.HTML -> highlightHtml(code)
        TrackLanguage.LOGIC -> AnnotatedString(code, SpanStyle(color = EditorText))
    }

    fun visualTransformation(language: TrackLanguage): VisualTransformation =
        VisualTransformation { text ->
            TransformedText(highlight(text.text, language), OffsetMapping.Identity)
        }

    private fun highlightPython(code: String): AnnotatedString = buildAnnotatedString {
        var i = 0
        val n = code.length
        while (i < n) {
            val c = code[i]
            when {
                c == '#' -> {
                    val end = code.indexOf('\n', i).let { if (it == -1) n else it }
                    withStyle(SyntaxComment) { append(code, i, end) }
                    i = end
                }
                c == '"' || c == '\'' -> {
                    val end = findStringEnd(code, i)
                    withStyle(SyntaxString) { append(code, i, end) }
                    i = end
                }
                c.isDigit() -> {
                    var end = i
                    while (end < n && (code[end].isDigit() || code[end] == '.')) end++
                    withStyle(SyntaxNumber) { append(code, i, end) }
                    i = end
                }
                c.isLetter() || c == '_' -> {
                    var end = i
                    while (end < n && (code[end].isLetterOrDigit() || code[end] == '_')) end++
                    val word = code.substring(i, end)
                    when {
                        word in PythonKeywords -> withStyle(SyntaxKeyword) { append(word) }
                        word in PythonBuiltins -> withStyle(SyntaxFunction) { append(word) }
                        else -> withStyle(SpanStyle(color = EditorText)) { append(word) }
                    }
                    i = end
                }
                else -> {
                    withStyle(SpanStyle(color = EditorText)) { append(c) }
                    i++
                }
            }
        }
    }

    private fun highlightHtml(code: String): AnnotatedString = buildAnnotatedString {
        var i = 0
        val n = code.length
        while (i < n) {
            val c = code[i]
            when {
                code.startsWith("<!--", i) -> {
                    val end = code.indexOf("-->", i).let { if (it == -1) n else it + 3 }
                    withStyle(SyntaxComment) { append(code, i, end) }
                    i = end
                }
                c == '<' -> {
                    val end = code.indexOf('>', i).let { if (it == -1) n else it + 1 }
                    appendTag(code.substring(i, end))
                    i = end
                }
                else -> {
                    val end = code.indexOf('<', i).let { if (it == -1) n else it }
                    withStyle(SpanStyle(color = EditorText)) { append(code, i, end) }
                    i = end
                }
            }
        }
    }

    private fun androidx.compose.ui.text.AnnotatedString.Builder.appendTag(tag: String) {
        var i = 0
        val n = tag.length
        var inQuotes = false
        var segmentStart = 0

        fun flush(end: Int, color: androidx.compose.ui.graphics.Color) {
            if (end > segmentStart) withStyle(color) { append(tag, segmentStart, end) }
            segmentStart = end
        }

        var seenName = false
        while (i < n) {
            val c = tag[i]
            when {
                c == '"' -> {
                    if (!inQuotes) {
                        flush(i, if (seenName) SyntaxAttribute else SyntaxTag)
                        inQuotes = true
                    } else {
                        inQuotes = false
                        flush(i + 1, SyntaxString)
                    }
                    i++
                }
                inQuotes -> i++
                c == ' ' && !seenName -> {
                    flush(i, SyntaxTag)
                    seenName = true
                    i++
                }
                else -> i++
            }
        }
        flush(n, if (inQuotes) SyntaxString else if (seenName) SyntaxAttribute else SyntaxTag)
    }

    private fun findStringEnd(code: String, start: Int): Int {
        val quote = code[start]
        var i = start + 1
        while (i < code.length) {
            when (code[i]) {
                '\\' -> i += 2
                quote -> return i + 1
                '\n' -> return i
                else -> i++
            }
        }
        return code.length
    }

    private fun androidx.compose.ui.text.AnnotatedString.Builder.withStyle(
        color: androidx.compose.ui.graphics.Color,
        block: androidx.compose.ui.text.AnnotatedString.Builder.() -> Unit,
    ) = withStyle(SpanStyle(color = color), block)

    private fun androidx.compose.ui.text.AnnotatedString.Builder.withStyle(
        style: SpanStyle,
        block: androidx.compose.ui.text.AnnotatedString.Builder.() -> Unit,
    ) {
        val index = pushStyle(style)
        block()
        pop(index)
    }
}
