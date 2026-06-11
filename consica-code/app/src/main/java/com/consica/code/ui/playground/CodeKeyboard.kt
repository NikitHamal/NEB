package com.consica.code.ui.playground

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import com.consica.code.domain.model.TrackLanguage

/**
 * A code key: [label] is what the learner sees, [insert] is what lands in the
 * editor, and [cursorOffset] places the caret inside the inserted text
 * (e.g. between quotes). -1 means "end of insert".
 */
data class CodeKey(
    val label: String,
    val insert: String,
    val cursorOffset: Int = -1,
)

private val PythonKeys = listOf(
    CodeKey("print", "print(\"\")", 7),
    CodeKey("\" \"", "\"\"", 1),
    CodeKey("( )", "()", 1),
    CodeKey("=", " = "),
    CodeKey("+", " + "),
    CodeKey(":", ":"),
    CodeKey("if", "if :", 3),
    CodeKey("for", "for i in range():", 16),
    CodeKey("def", "def ():", 4),
    CodeKey("⇥", "    "),
    CodeKey("#", "# "),
    CodeKey(",", ", "),
)

private val HtmlKeys = listOf(
    CodeKey("< >", "<>", 1),
    CodeKey("</ >", "</>", 2),
    CodeKey("h1", "<h1></h1>", 4),
    CodeKey("p", "<p></p>", 3),
    CodeKey("=\" \"", "=\"\"", 2),
    CodeKey("/", "/"),
    CodeKey("img", "<img src=\"\">", 10),
    CodeKey("div", "<div></div>", 5),
    CodeKey("br", "<br>"),
    CodeKey("!", "!"),
    CodeKey("-", "-"),
    CodeKey("⇥", "  "),
)

/**
 * Horizontal strip of big friendly snippet keys shown above the system
 * keyboard so young learners don't hunt for symbols.
 */
@Composable
fun CodeKeyboard(
    language: TrackLanguage,
    onKey: (CodeKey) -> Unit,
    modifier: Modifier = Modifier,
) {
    val keys = when (language) {
        TrackLanguage.PYTHON, TrackLanguage.LOGIC -> PythonKeys
        TrackLanguage.HTML -> HtmlKeys
    }
    Column(modifier.fillMaxWidth().testTag("code_keyboard")) {
        Row(
            Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState())
                .padding(horizontal = 8.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            for (key in keys) {
                KeyChip(key = key, onClick = { onKey(key) })
            }
        }
    }
}

@Composable
private fun KeyChip(key: CodeKey, onClick: () -> Unit) {
    Text(
        text = key.label,
        style = MaterialTheme.typography.labelLarge.copy(fontFamily = FontFamily.Monospace),
        color = MaterialTheme.colorScheme.onSecondaryContainer,
        modifier = Modifier
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.secondaryContainer)
            .clickable(onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 10.dp),
    )
}

/** Applies a [CodeKey] press to the editor text and returns the new value. */
fun applyCodeKey(
    text: String,
    selectionStart: Int,
    key: CodeKey,
): Pair<String, Int> {
    val start = selectionStart.coerceIn(0, text.length)
    val newText = text.substring(0, start) + key.insert + text.substring(start)
    val cursor = if (key.cursorOffset >= 0) start + key.cursorOffset else start + key.insert.length
    return newText to cursor
}
