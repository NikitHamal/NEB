package com.neb.ians.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.text.ClickableText

/**
 * Lightweight markdown renderer matching the web's python-markdown output
 * (nl2br, bold, italic, inline code, strikethrough, headings, lists,
 * blockquotes, links and @mentions).
 *
 * Mentions (@username) and links are clickable.
 */
@Composable
fun MarkdownText(
    markdown: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {}
) {
    val blocks = remember(markdown) { parseMarkdownBlocks(markdown) }
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val onSurfaceVariant = MaterialTheme.colorScheme.onSurfaceVariant

    Column(modifier = modifier) {
        blocks.forEachIndexed { index, block ->
            if (index > 0) Spacer(modifier = Modifier.height(4.dp))
            when (block) {
                is MdBlock.Heading -> {
                    val headingStyle = when (block.level) {
                        1 -> MaterialTheme.typography.titleLarge
                        2 -> MaterialTheme.typography.titleMedium
                        else -> MaterialTheme.typography.titleSmall
                    }
                    InlineMdText(
                        text = block.text,
                        style = headingStyle.copy(fontWeight = FontWeight.Bold),
                        color = color,
                        primary = primary,
                        codeBg = codeBg,
                        onMentionClick = onMentionClick,
                        onLinkClick = onLinkClick
                    )
                }
                is MdBlock.Quote -> {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Spacer(
                            modifier = Modifier
                                .width(3.dp)
                                .height(20.dp)
                                .background(primary.copy(alpha = 0.5f), RoundedCornerShape(2.dp))
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        InlineMdText(
                            text = block.text,
                            style = style.copy(fontStyle = FontStyle.Italic),
                            color = onSurfaceVariant,
                            primary = primary,
                            codeBg = codeBg,
                            onMentionClick = onMentionClick,
                            onLinkClick = onLinkClick
                        )
                    }
                }
                is MdBlock.ListItem -> {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Text(
                            text = if (block.ordered) "${block.number}." else "\u2022",
                            style = style,
                            color = onSurfaceVariant,
                            modifier = Modifier.padding(end = 8.dp)
                        )
                        InlineMdText(
                            text = block.text,
                            style = style,
                            color = color,
                            primary = primary,
                            codeBg = codeBg,
                            onMentionClick = onMentionClick,
                            onLinkClick = onLinkClick
                        )
                    }
                }
                is MdBlock.Paragraph -> {
                    InlineMdText(
                        text = block.text,
                        style = style,
                        color = color,
                        primary = primary,
                        codeBg = codeBg,
                        onMentionClick = onMentionClick,
                        onLinkClick = onLinkClick
                    )
                }
            }
        }
    }
}

@Composable
private fun InlineMdText(
    text: String,
    style: TextStyle,
    color: Color,
    primary: Color,
    codeBg: Color,
    onMentionClick: (String) -> Unit,
    onLinkClick: (String) -> Unit
) {
    val errorBg = MaterialTheme.colorScheme.errorContainer
    val errorFg = MaterialTheme.colorScheme.onErrorContainer
    val annotated = remember(text, color, primary, codeBg, errorBg, errorFg) {
        buildInlineAnnotatedString(text, color, primary, codeBg, errorBg, errorFg)
    }
    ClickableText(
        text = annotated,
        style = style.copy(color = color),
        onClick = { offset ->
            annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                onMentionClick(it.item)
                return@ClickableText
            }
            annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                onLinkClick(it.item)
            }
        }
    )
}

sealed class MdBlock {
    data class Heading(val level: Int, val text: String) : MdBlock()
    data class Quote(val text: String) : MdBlock()
    data class ListItem(val text: String, val ordered: Boolean, val number: Int) : MdBlock()
    data class Paragraph(val text: String) : MdBlock()
}

internal fun parseMarkdownBlocks(markdown: String): List<MdBlock> {
    val blocks = mutableListOf<MdBlock>()
    var orderedIndex = 1
    markdown.replace("\r\n", "\n").split("\n").forEach { rawLine ->
        val line = rawLine.trimEnd()
        when {
            line.isBlank() -> {
                orderedIndex = 1
                blocks.add(MdBlock.Paragraph(""))
            }
            line.startsWith("### ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(3, line.removePrefix("### "))) }
            line.startsWith("## ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(2, line.removePrefix("## "))) }
            line.startsWith("# ") -> { orderedIndex = 1; blocks.add(MdBlock.Heading(1, line.removePrefix("# "))) }
            line.startsWith("> ") -> { orderedIndex = 1; blocks.add(MdBlock.Quote(line.removePrefix("> "))) }
            line.startsWith("- ") || line.startsWith("* ") -> {
                blocks.add(MdBlock.ListItem(line.substring(2), ordered = false, number = 0))
            }
            Regex("^\\d+\\.\\s").containsMatchIn(line) -> {
                val text = line.replaceFirst(Regex("^\\d+\\.\\s"), "")
                blocks.add(MdBlock.ListItem(text, ordered = true, number = orderedIndex))
                orderedIndex++
            }
            else -> { orderedIndex = 1; blocks.add(MdBlock.Paragraph(line)) }
        }
    }
    // Collapse consecutive blank paragraphs
    val result = mutableListOf<MdBlock>()
    var lastBlank = false
    blocks.forEach { b ->
        val isBlank = b is MdBlock.Paragraph && b.text.isBlank()
        if (!(isBlank && lastBlank)) result.add(b)
        lastBlank = isBlank
    }
    while (result.isNotEmpty() && result.last() is MdBlock.Paragraph && (result.last() as MdBlock.Paragraph).text.isBlank()) {
        result.removeAt(result.lastIndex)
    }
    return result
}

private val inlinePattern = Regex(
    "(\\*\\*([^*]+)\\*\\*)" +          // 1,2 bold
        "|(\\*([^*]+)\\*)" +            // 3,4 italic
        "|(`([^`]+)`)" +                // 5,6 code
        "|(~~([^~]+)~~)" +              // 7,8 strikethrough
        "|(\\[([^\\]]+)\\]\\(([^)]+)\\))" + // 9,10,11 link
        "|(@([A-Za-z0-9_]+))"           // 12,13 mention
)

internal fun buildInlineAnnotatedString(
    text: String,
    baseColor: Color,
    primary: Color,
    codeBg: Color,
    errorBg: Color = Color(0xFFFFD8E4),
    errorFg: Color = Color(0xFF31111D)
): AnnotatedString = buildAnnotatedString {
    var cursor = 0
    inlinePattern.findAll(text).forEach { match ->
        if (match.range.first > cursor) {
            append(text.substring(cursor, match.range.first))
        }
        val g = match.groups
        when {
            g[2] != null -> withStyleAppend(SpanStyle(fontWeight = FontWeight.Bold), g[2]!!.value)
            g[4] != null -> withStyleAppend(SpanStyle(fontStyle = FontStyle.Italic), g[4]!!.value)
            g[6] != null -> withStyleAppend(
                SpanStyle(fontFamily = FontFamily.Monospace, background = codeBg, fontSize = 13.sp),
                g[6]!!.value
            )
            g[8] != null -> withStyleAppend(SpanStyle(textDecoration = TextDecoration.LineThrough), g[8]!!.value)
            g[10] != null && g[11] != null -> {
                pushStringAnnotation("url", g[11]!!.value)
                withStyleAppend(SpanStyle(color = primary, textDecoration = TextDecoration.Underline), g[10]!!.value)
                pop()
            }
            g[13] != null -> {
                val isAll = g[13]!!.value.equals("all", ignoreCase = true)
                if (isAll) {
                    withStyleAppend(
                        SpanStyle(background = errorBg, color = errorFg, fontWeight = FontWeight.Bold),
                        "@all"
                    )
                } else {
                    pushStringAnnotation("mention", g[13]!!.value)
                    withStyleAppend(SpanStyle(color = primary, fontWeight = FontWeight.Medium), "@${g[13]!!.value}")
                    pop()
                }
            }
        }
        cursor = match.range.last + 1
    }
    if (cursor < text.length) append(text.substring(cursor))
}

private fun androidx.compose.ui.text.AnnotatedString.Builder.withStyleAppend(style: SpanStyle, text: String) {
    pushStyle(style)
    append(text)
    pop()
}

/** Strip markdown markers for inline previews (post cards). Mirrors web render_content_inline. */
fun markdownToPlainPreview(markdown: String): String {
    return markdown
        .replace(Regex("!\\[[^\\]]*\\]\\([^)]*\\)"), "")
        .replace(Regex("\\[([^\\]]+)\\]\\([^)]*\\)"), "$1")
        .replace(Regex("[*_~`#>]+"), "")
        .replace(Regex("\\n{2,}"), "\n")
        .trim()
}

@Composable
fun ExpandableMarkdownText(
    markdown: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyMedium,
    color: Color = MaterialTheme.colorScheme.onSurface,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {},
    minimizedMaxLines: Int = 3
) {
    var isExpanded by remember { mutableStateOf(false) }
    var hasOverflow by remember { mutableStateOf(false) }

    Column(modifier = modifier) {
        if (isExpanded) {
            MarkdownText(
                markdown = markdown,
                style = style,
                color = color,
                onMentionClick = onMentionClick,
                onLinkClick = onLinkClick
            )
        } else {
            // Collapsed preview stays fully formatted: block structure is
            // flattened but inline markdown (bold, italic, code, strike,
            // colored/links and highlighted @mentions) keeps rendering, so
            // the preview never looks like raw unprocessed text.
            val flatText = remember(markdown) { markdownToInlinePreview(markdown) }
            val primary = MaterialTheme.colorScheme.primary
            val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
            val errorBg = MaterialTheme.colorScheme.errorContainer
            val errorFg = MaterialTheme.colorScheme.onErrorContainer
            val annotated = remember(flatText, color, primary, codeBg, errorBg, errorFg) {
                buildInlineAnnotatedString(flatText, color, primary, codeBg, errorBg, errorFg)
            }
            ClickableText(
                text = annotated,
                style = style.copy(color = color),
                maxLines = minimizedMaxLines,
                overflow = TextOverflow.Ellipsis,
                onTextLayout = { textLayoutResult ->
                    hasOverflow = textLayoutResult.hasVisualOverflow
                },
                onClick = { offset ->
                    annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                        onMentionClick(it.item)
                        return@ClickableText
                    }
                    annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                        onLinkClick(it.item)
                    }
                }
            )
        }
        if (hasOverflow || isExpanded) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = if (isExpanded) "See less" else "See more",
                style = style.copy(fontWeight = FontWeight.SemiBold),
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = { isExpanded = !isExpanded }
                )
            )
        }
    }
}

/**
 * Flatten markdown blocks into a single flow of text for collapsed previews,
 * keeping inline markers so [buildInlineAnnotatedString] can still style
 * bold/italic/code/links/mentions. Block markers become readable bullets.
 */
fun markdownToInlinePreview(markdown: String): String {
    if (markdown.isBlank()) return ""
    return parseMarkdownBlocks(markdown).joinToString("\n") { block ->
        when (block) {
            is MdBlock.Heading -> block.text
            is MdBlock.Quote -> block.text
            is MdBlock.ListItem -> (if (block.ordered) "${block.number}. " else "• ") + block.text
            is MdBlock.Paragraph -> block.text
        }
    }.replace(Regex("!\\[[^]]*]\\([^)]*\\)"), "").trim()
}

/**
 * Compact single-flow inline markdown for cards (suggested feed, lists):
 * bold/italic/inline-code/strikethrough/links/@mentions rendered inline like
 * the full [MarkdownText], but collapsed to one ellipsizable Text with
 * newlines folded — perfect for 2-line excerpts.
 */
@Composable
fun MarkdownInlineText(
    markdown: String,
    style: TextStyle,
    color: Color,
    modifier: Modifier = Modifier,
    maxLines: Int = Int.MAX_VALUE,
    onMentionClick: (String) -> Unit = {},
    onLinkClick: (String) -> Unit = {}
) {
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val errorBg = MaterialTheme.colorScheme.errorContainer
    val errorFg = MaterialTheme.colorScheme.onErrorContainer
    val flattened = remember(markdown) {
        markdown.replace(Regex("\\s*\n+\\s*"), " ").trim()
    }
    if (flattened.isEmpty()) return
    val annotated = remember(flattened, color, primary, codeBg, errorBg, errorFg) {
        buildInlineAnnotatedString(flattened, color, primary, codeBg, errorBg, errorFg)
    }
    ClickableText(
        text = annotated,
        modifier = modifier,
        style = style.copy(color = color),
        overflow = TextOverflow.Ellipsis,
        maxLines = maxLines,
        onClick = { offset ->
            annotated.getStringAnnotations("mention", offset, offset).firstOrNull()?.let {
                onMentionClick(it.item)
                return@ClickableText
            }
            annotated.getStringAnnotations("url", offset, offset).firstOrNull()?.let {
                onLinkClick(it.item)
            }
        }
    )
}
