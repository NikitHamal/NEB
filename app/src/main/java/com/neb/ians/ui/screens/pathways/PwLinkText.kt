package com.neb.ians.ui.screens.pathways

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.LinkAnnotation
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextLinkStyles
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withLink
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.sp

/** Web addresses, bare domains (.np and common ones), e-mail and Nepali phone numbers, built once. */
private val LINK = Regex(
    """(https?://[^\s<,]+[^\s<,.)]|\bwww\.[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:/[^\s<,]*[^\s<,.)])?|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:gov|edu|org|com|net)\.np\b""" +
        """|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|org|edu|gov|net|io|int)\b(?:/[^\s<,]*[^\s<,.)])?|\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b|\b0\d{1,2}-\d{6,7}\b|\b1660-\d{2}-\d{5}\b)""",
    RegexOption.IGNORE_CASE,
)
private val SCHEME = Regex("^https?://(www\\.)?", RegexOption.IGNORE_CASE)

/** [text] with every address turned into a tappable link (browser, mail or dialer). Plain text comes back untouched and cheap. */
internal fun pwLinkify(text: String, style: TextLinkStyles): AnnotatedString {
    if (text.length < 5 || LINK.find(text) == null) return AnnotatedString(text)
    return buildAnnotatedString {
        var last = 0
        LINK.findAll(text).forEach { m ->
            append(text, last, m.range.first)
            val v = m.value
            val url = when {
                v.startsWith("http", true) -> v
                '@' in v -> "mailto:$v"
                v.all { it.isDigit() || it == '-' } -> "tel:" + v.replace("-", "")
                else -> "https://$v"
            }
            withLink(LinkAnnotation.Url(url, style)) { append(v.replace(SCHEME, "")) }
            last = m.range.last + 1
        }
        append(text, last, text.length)
    }
}

/** Body text where web addresses, e-mail and phone numbers open on tap. */
@Composable
internal fun PwLinkText(
    text: String, modifier: Modifier = Modifier, fontSize: TextUnit = 14.sp, lineHeight: TextUnit = 21.sp,
    color: Color = MaterialTheme.colorScheme.onSurface, weight: FontWeight = FontWeight.Normal, maxLines: Int = Int.MAX_VALUE,
) {
    val styles = remember(color) { TextLinkStyles(SpanStyle(color = color, fontWeight = FontWeight.SemiBold, textDecoration = TextDecoration.Underline)) }
    val a = remember(text, styles) { pwLinkify(text, styles) }
    Text(a, modifier, color = color, fontSize = fontSize, lineHeight = lineHeight, fontWeight = weight, maxLines = maxLines, overflow = TextOverflow.Ellipsis)
}
