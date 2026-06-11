package com.consica.code.ui.screens.playground

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.consica.code.core.designsystem.CodeTextStyle
import com.consica.code.core.designsystem.EditorBackground
import com.consica.code.core.designsystem.EditorLineNumber
import com.consica.code.core.designsystem.EditorText
import com.consica.code.core.designsystem.SunYellow
import com.consica.code.core.model.CodeLanguage
import com.consica.code.runtime.highlight.SyntaxHighlighter

/** Live syntax highlighting via VisualTransformation (identity offsets). */
private class SyntaxTransformation(private val language: CodeLanguage) : VisualTransformation {
    override fun filter(text: androidx.compose.ui.text.AnnotatedString): TransformedText {
        val highlighted = SyntaxHighlighter.highlight(text.text, language)
        return TransformedText(highlighted, OffsetMapping.Identity)
    }
}

/**
 * The Green-Code editor surface: dark, high contrast, monospace, with optional
 * line numbers for the professional mode.
 */
@Composable
fun CodeEditor(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    language: CodeLanguage,
    showLineNumbers: Boolean,
    modifier: Modifier = Modifier,
    errorLine: Int? = null,
) {
    val transformation = remember(language) { SyntaxTransformation(language) }
    val scrollState = rememberScrollState()

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .background(EditorBackground),
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState)
                .padding(vertical = 12.dp),
        ) {
            if (showLineNumbers) {
                val lineCount = value.text.count { it == '\n' } + 1
                Column(
                    modifier = Modifier
                        .width(40.dp)
                        .padding(end = 4.dp),
                ) {
                    for (i in 1..lineCount) {
                        Text(
                            text = i.toString(),
                            style = CodeTextStyle,
                            color = if (i == errorLine) SunYellow else EditorLineNumber,
                            textAlign = TextAlign.End,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                textStyle = CodeTextStyle.copy(color = EditorText),
                cursorBrush = SolidColor(SunYellow),
                visualTransformation = transformation,
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 12.dp),
            )
        }
    }
}

/** Inserts [snippet] at the cursor, optionally placing the cursor [cursorBack] chars earlier. */
fun TextFieldValue.insertSnippet(snippet: String, cursorBack: Int = 0): TextFieldValue {
    val start = selection.min
    val end = selection.max
    val newText = text.substring(0, start) + snippet + text.substring(end)
    val cursor = start + snippet.length - cursorBack
    return TextFieldValue(newText, TextRange(cursor))
}
