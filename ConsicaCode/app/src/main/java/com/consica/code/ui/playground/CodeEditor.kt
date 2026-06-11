package com.consica.code.ui.playground

import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.PillShape
import com.consica.code.core.design.codeTextStyle
import com.consica.code.domain.content.CodeLang
import com.consica.code.domain.runner.RunResult

private val CodeBg = Color(0xFF14201A)
private val CodeFg = Color(0xFFD7F0D5)
private val CodeLineNo = Color(0xFF6E8C6A)

/** Monospace code editor with optional line numbers. Dark "terminal" surface for focus. */
@Composable
fun CodeEditor(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    modifier: Modifier = Modifier,
    showLineNumbers: Boolean = false,
) {
    Surface(shape = CardShape, color = CodeBg, modifier = modifier) {
        Row(Modifier.padding(Dimens.md)) {
            if (showLineNumbers) {
                val lineCount = value.text.count { it == '\n' } + 1
                Column(Modifier.padding(end = Dimens.sm)) {
                    for (i in 1..lineCount) {
                        Text(
                            i.toString(),
                            style = codeTextStyle().copy(color = CodeLineNo),
                        )
                    }
                }
            }
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                textStyle = codeTextStyle().copy(color = CodeFg),
                cursorBrush = SolidColor(CodeFg),
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 160.dp),
            )
        }
    }
}

private data class Snippet(val label: String, val insert: String, val caretBack: Int = 0)

/**
 * "Custom keyboard" of language snippets/symbols. Inserts at the cursor so young learners don't
 * have to hunt for symbols on the system keyboard. [caretBack] places the cursor inside a pair.
 */
@Composable
fun SymbolBar(
    lang: CodeLang?,
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    modifier: Modifier = Modifier,
) {
    val snippets = when (lang) {
        CodeLang.HTML -> listOf(
            Snippet("<h1>", "<h1></h1>", 5),
            Snippet("<p>", "<p></p>", 4),
            Snippet("<a>", "<a href=\"\"></a>", 6),
            Snippet("<ul>", "<ul>\n  <li></li>\n</ul>", 11),
            Snippet("</>", "</>", 1),
            Snippet("\"", "\"\"", 1),
            Snippet("<", "<"),
            Snippet(">", ">"),
        )
        CodeLang.PYTHON -> listOf(
            Snippet("print", "print()", 1),
            Snippet("if", "if :", 1),
            Snippet("for", "for i in range():", 2),
            Snippet("def", "def name():", 3),
            Snippet("( )", "()", 1),
            Snippet("[ ]", "[]", 1),
            Snippet("\"", "\"\"", 1),
            Snippet(":", ":"),
        )
        else -> emptyList()
    }
    if (snippets.isEmpty()) return

    Row(
        modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(vertical = Dimens.xs),
        horizontalArrangement = Arrangement.spacedBy(Dimens.sm),
    ) {
        snippets.forEach { s ->
            Surface(
                onClick = { onValueChange(insertSnippet(value, s)) },
                shape = PillShape,
                color = MaterialTheme.colorScheme.secondaryContainer,
            ) {
                Text(
                    s.label,
                    style = codeTextStyle().copy(color = MaterialTheme.colorScheme.onSecondaryContainer),
                    modifier = Modifier.padding(horizontal = Dimens.md, vertical = Dimens.sm),
                )
            }
        }
    }
}

private fun insertSnippet(value: TextFieldValue, snippet: Snippet): TextFieldValue {
    val start = value.selection.start.coerceIn(0, value.text.length)
    val end = value.selection.end.coerceIn(0, value.text.length)
    val newText = value.text.substring(0, start) + snippet.insert + value.text.substring(end)
    val caret = (start + snippet.insert.length - snippet.caretBack).coerceIn(0, newText.length)
    return TextFieldValue(newText, TextRange(caret))
}

/** Console / output panel. Shows run output and any friendly errors. */
@Composable
fun ConsolePanel(
    result: RunResult?,
    placeholder: String,
    modifier: Modifier = Modifier,
    showErrors: Boolean = true,
) {
    Surface(shape = CardShape, color = CodeBg, modifier = modifier) {
        Column(Modifier.padding(Dimens.md)) {
            if (result == null) {
                Text(placeholder, style = codeTextStyle().copy(color = CodeLineNo))
                return@Column
            }
            if (result.output.isNotBlank()) {
                Text(result.output, style = codeTextStyle().copy(color = CodeFg))
            }
            if (showErrors && result.hasErrors) {
                result.errors.forEach { err ->
                    val prefix = err.line?.let { "line $it: " } ?: ""
                    Box(Modifier.fillMaxWidth().padding(top = Dimens.xs)) {
                        Text(
                            "$prefix${err.message}",
                            style = codeTextStyle().copy(color = MaterialTheme.colorScheme.error),
                        )
                    }
                }
            }
        }
    }
}
