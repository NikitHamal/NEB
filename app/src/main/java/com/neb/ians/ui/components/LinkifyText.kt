package com.neb.ians.ui.components

import androidx.compose.foundation.text.ClickableText
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.TextUnit.Companion.Unspecified

private val PLAIN_URL_RE = Regex("(https?://[^\\s]+|www\\.[^\\s]+)", RegexOption.IGNORE_CASE)

fun String.linkifyAnnotated(primary: Color): AnnotatedString = buildAnnotatedString {
    var cursor = 0
    val src = this@linkifyAnnotated
    PLAIN_URL_RE.findAll(src).forEach { match ->
        if (match.range.first > cursor) append(src.substring(cursor, match.range.first))
        val raw = match.value.trimEnd('.', ',', ';', ':', '!', '?', ')')
        if (raw.isNotEmpty()) {
            val href = if (raw.startsWith("http", ignoreCase = true)) raw else "http://$raw"
            pushStringAnnotation("url", href)
            pushStyle(SpanStyle(color = primary, textDecoration = TextDecoration.Underline))
            append(raw)
            pop()
            pop()
        } else {
            append(match.value)
        }
        cursor = match.range.last + 1
    }
    if (cursor < src.length) append(src.substring(cursor))
}

@Composable
fun LinkifyText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    fontSize: TextUnit = Unspecified,
    maxLines: Int = Int.MAX_VALUE,
    overflow: TextOverflow = TextOverflow.Clip,
    onTextLayout: (TextLayoutResult) -> Unit = {},
    onLinkClick: ((String) -> Unit)? = null
) {
    if (text.isEmpty()) return
    val uriHandler = LocalUriHandler.current
    val primary = MaterialTheme.colorScheme.primary
    val annotated = remember(text, primary) { text.linkifyAnnotated(primary) }
    ClickableText(
        text = annotated,
        modifier = modifier,
        style = style.copy(color = color, fontSize = fontSize),
        maxLines = maxLines,
        overflow = overflow,
        onTextLayout = onTextLayout,
        onClick = { offset ->
            annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let { ann ->
                val url = ann.item
                if (onLinkClick != null) onLinkClick(url) else runCatching { uriHandler.openUri(url) }
            }
        }
    )
}
