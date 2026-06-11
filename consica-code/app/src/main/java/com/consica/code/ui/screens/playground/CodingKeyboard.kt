package com.consica.code.ui.screens.playground

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.consica.code.core.designsystem.CodeTextStyle
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.CodeLanguage

/** A snippet key: label shown, text inserted, optional cursor pull-back. */
data class SnippetKey(val label: String, val insert: String, val cursorBack: Int = 0)

private val PY_KEYS_KIDS = listOf(
    SnippetKey("print", "print(\"\")", 2),
    SnippetKey("\" \"", "\"\"", 1),
    SnippetKey("=", " = "),
    SnippetKey("if", "if :", 1),
    SnippetKey("else", "else:\n    "),
    SnippetKey("loop", "for i in range(3):\n    "),
    SnippetKey("def", "def my_function():\n    "),
    SnippetKey("[ ]", "[]", 1),
    SnippetKey("( )", "()", 1),
    SnippetKey(":", ":"),
    SnippetKey("⇥", "    "),
    SnippetKey(",", ", "),
)

private val PY_KEYS_PRO = listOf(
    SnippetKey("print", "print()", 1),
    SnippetKey("\"", "\""),
    SnippetKey("'", "'"),
    SnippetKey("=", "="),
    SnippetKey("==", "=="),
    SnippetKey(":", ":"),
    SnippetKey("⇥", "    "),
    SnippetKey("if", "if "),
    SnippetKey("elif", "elif "),
    SnippetKey("else", "else:"),
    SnippetKey("for", "for  in :", 4),
    SnippetKey("while", "while :", 1),
    SnippetKey("def", "def ():", 3),
    SnippetKey("return", "return "),
    SnippetKey("[", "["),
    SnippetKey("]", "]"),
    SnippetKey("(", "("),
    SnippetKey(")", ")"),
    SnippetKey("#", "# "),
)

private val HTML_KEYS_KIDS = listOf(
    SnippetKey("<h1>", "<h1></h1>", 5),
    SnippetKey("<p>", "<p></p>", 4),
    SnippetKey("<a>", "<a href=\"\"></a>", 6),
    SnippetKey("<img>", "<img src=\"\" alt=\"\">", 10),
    SnippetKey("<ul>", "<ul>\n  <li></li>\n</ul>", 12),
    SnippetKey("<li>", "<li></li>", 5),
    SnippetKey("style", "<style>\n  h1 { color: green; }\n</style>"),
    SnippetKey("<", "<"),
    SnippetKey(">", ">"),
    SnippetKey("/", "/"),
    SnippetKey("\" \"", "\"\"", 1),
    SnippetKey("=", "="),
)

private val HTML_KEYS_PRO = listOf(
    SnippetKey("<", "<"),
    SnippetKey(">", ">"),
    SnippetKey("/", "/"),
    SnippetKey("\"", "\""),
    SnippetKey("=", "="),
    SnippetKey("h1", "<h1></h1>", 5),
    SnippetKey("p", "<p></p>", 4),
    SnippetKey("div", "<div></div>", 6),
    SnippetKey("a", "<a href=\"\"></a>", 6),
    SnippetKey("img", "<img src=\"\" alt=\"\">", 10),
    SnippetKey("ul", "<ul>\n  <li></li>\n</ul>", 12),
    SnippetKey("form", "<form>\n  \n</form>", 8),
    SnippetKey("style", "<style>\n  \n</style>", 9),
    SnippetKey("header", "<header></header>", 9),
    SnippetKey("main", "<main></main>", 7),
    SnippetKey("footer", "<footer></footer>", 9),
)

/**
 * The custom coding keyboard helper bar — kid-friendly large snippet keys for
 * young learners, denser professional keys for older users.
 */
@Composable
fun CodingKeyboard(
    language: CodeLanguage,
    ageGroup: AgeGroup,
    professional: Boolean,
    onKey: (SnippetKey) -> Unit,
    modifier: Modifier = Modifier,
) {
    val keys = when {
        language == CodeLanguage.PYTHON && (professional || ageGroup != AgeGroup.KIDS) -> PY_KEYS_PRO
        language == CodeLanguage.PYTHON -> PY_KEYS_KIDS
        professional || ageGroup != AgeGroup.KIDS -> HTML_KEYS_PRO
        else -> HTML_KEYS_KIDS
    }

    Column(modifier = modifier.fillMaxWidth()) {
        val rows = if (ageGroup == AgeGroup.KIDS && !professional) keys.chunked(6) else listOf(keys)
        rows.forEach { rowKeys ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                rowKeys.forEach { key ->
                    Surface(
                        onClick = { onKey(key) },
                        shape = MaterialTheme.shapes.small,
                        color = MaterialTheme.colorScheme.surfaceVariant,
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                    ) {
                        Text(
                            text = key.label,
                            style = CodeTextStyle,
                            color = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.padding(
                                horizontal = if (ageGroup == AgeGroup.KIDS && !professional) 14.dp else 10.dp,
                                vertical = if (ageGroup == AgeGroup.KIDS && !professional) 10.dp else 6.dp,
                            ),
                        )
                    }
                }
            }
        }
    }
}
