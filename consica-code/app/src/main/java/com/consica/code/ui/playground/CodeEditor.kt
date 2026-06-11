package com.consica.code.ui.playground

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.ui.theme.CodeTextStyle
import com.consica.code.ui.theme.EditorBackground
import com.consica.code.ui.theme.EditorLineNumber
import com.consica.code.ui.theme.SproutGreen

/**
 * Syntax-highlighted code editor. Line numbers appear in pro mode so younger
 * learners see a simpler, friendlier surface.
 */
@Composable
fun CodeEditor(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    language: TrackLanguage,
    modifier: Modifier = Modifier,
    showLineNumbers: Boolean = false,
    readOnly: Boolean = false,
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(EditorBackground),
    ) {
        Row(Modifier.fillMaxSize()) {
            if (showLineNumbers) {
                val lineCount = value.text.count { it == '\n' } + 1
                Column(
                    Modifier
                        .padding(start = 12.dp, top = 12.dp, bottom = 12.dp)
                        .testTag("line_numbers"),
                ) {
                    for (line in 1..lineCount) {
                        Text(
                            text = line.toString().padStart(2),
                            style = CodeTextStyle,
                            color = EditorLineNumber,
                        )
                    }
                }
            }
            BasicTextField(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier
                    .fillMaxSize()
                    .padding(12.dp)
                    .testTag("code_editor"),
                textStyle = CodeTextStyle,
                cursorBrush = SolidColor(SproutGreen),
                visualTransformation = SyntaxHighlighter.visualTransformation(language),
                readOnly = readOnly,
            )
        }
    }
}

/** Read-only highlighted snippet used inside lesson dialogue and hints. */
@Composable
fun CodeSnippet(
    code: String,
    language: TrackLanguage,
    modifier: Modifier = Modifier,
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(EditorBackground)
            .padding(12.dp),
    ) {
        Text(
            text = SyntaxHighlighter.highlight(code, language),
            style = CodeTextStyle,
        )
    }
}
