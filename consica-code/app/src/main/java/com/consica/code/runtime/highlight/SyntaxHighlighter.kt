package com.consica.code.runtime.highlight

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import com.consica.code.core.designsystem.EditorText
import com.consica.code.core.designsystem.SyntaxAttribute
import com.consica.code.core.designsystem.SyntaxComment
import com.consica.code.core.designsystem.SyntaxFunction
import com.consica.code.core.designsystem.SyntaxKeyword
import com.consica.code.core.designsystem.SyntaxNumber
import com.consica.code.core.designsystem.SyntaxString
import com.consica.code.core.designsystem.SyntaxTag
import com.consica.code.core.model.CodeLanguage

/**
 * Regex-based live syntax highlighting producing AnnotatedStrings for the
 * Compose editor. Fast enough for lesson-sized programs and fully offline.
 */
object SyntaxHighlighter {

    private val PY_KEYWORDS = setOf(
        "if", "elif", "else", "for", "while", "def", "return", "break", "continue",
        "pass", "in", "and", "or", "not", "True", "False", "None", "import", "from",
        "class", "try", "except", "finally", "with", "as", "lambda",
    )

    private val PY_BUILTINS = setOf(
        "print", "len", "range", "str", "int", "float", "abs", "min", "max", "sum",
        "sorted", "input", "bool", "list",
    )

    fun highlight(code: String, language: CodeLanguage): AnnotatedString = when (language) {
        CodeLanguage.PYTHON -> highlightPython(code)
        CodeLanguage.HTML -> highlightHtml(code)
    }

    private data class Span(val start: Int, val end: Int, val color: Color)

    private fun applySpans(code: String, spans: List<Span>): AnnotatedString {
        val sorted = spans.sortedBy { it.start }
        return buildAnnotatedString {
            append(code)
            addStyle(SpanStyle(color = EditorText), 0, code.length)
            var lastEnd = -1
            for (s in sorted) {
                if (s.start < lastEnd) continue // skip overlaps
                addStyle(SpanStyle(color = s.color), s.start, s.end)
                lastEnd = s.end
            }
        }
    }

    private fun highlightPython(code: String): AnnotatedString {
        val spans = mutableListOf<Span>()
        // strings
        for (m in Regex("(\"[^\"\\n]*\"?|'[^'\\n]*'?)").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxString)
        }
        // comments
        for (m in Regex("#[^\n]*").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxComment)
        }
        // numbers
        for (m in Regex("\\b\\d+(\\.\\d+)?\\b").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxNumber)
        }
        // keywords / builtins
        for (m in Regex("\\b[A-Za-z_][A-Za-z0-9_]*\\b").findAll(code)) {
            val word = m.value
            when {
                word in PY_KEYWORDS -> spans += Span(m.range.first, m.range.last + 1, SyntaxKeyword)
                word in PY_BUILTINS -> spans += Span(m.range.first, m.range.last + 1, SyntaxFunction)
            }
        }
        return applySpans(code, resolveOverlaps(spans))
    }

    private fun highlightHtml(code: String): AnnotatedString {
        val spans = mutableListOf<Span>()
        // comments
        for (m in Regex("<!--.*?-->", RegexOption.DOT_MATCHES_ALL).findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxComment)
        }
        // tags (names only)
        for (m in Regex("</?\\s*([a-zA-Z][a-zA-Z0-9]*)").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxTag)
        }
        // attribute names
        for (m in Regex("\\s([a-zA-Z-]+)=").findAll(code)) {
            val g = m.groups[1]!!
            spans += Span(g.range.first, g.range.last + 1, SyntaxAttribute)
        }
        // attribute values / strings
        for (m in Regex("\"[^\"\\n]*\"").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxString)
        }
        // angle brackets
        for (m in Regex("[<>]").findAll(code)) {
            spans += Span(m.range.first, m.range.last + 1, SyntaxKeyword)
        }
        return applySpans(code, resolveOverlaps(spans))
    }

    /** Strings and comments win over inner matches. */
    private fun resolveOverlaps(spans: List<Span>): List<Span> {
        val sorted = spans.sortedWith(compareBy({ it.start }, { -(it.end - it.start) }))
        val result = mutableListOf<Span>()
        var lastEnd = -1
        for (s in sorted) {
            if (s.start >= lastEnd) {
                result += s
                lastEnd = s.end
            }
        }
        return result
    }
}
