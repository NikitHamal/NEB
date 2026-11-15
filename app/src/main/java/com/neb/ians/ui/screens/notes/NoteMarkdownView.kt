package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val inlineToken = Regex(
    "\\*\\*(.+?)\\*\\*|__(.+?)__|~~(.+?)~~|`([^`]+)`|\\*([^*\\n]+)\\*|(?<!\\w)_([^_\\n]+)_(?!\\w)|\\[([^\\]]+)]\\(([^)]*)\\)|(?<![\\w&])#(\\w+)|<u>(.+?)</u>"
)

/** Inline Markdown to styled text: bold, italic, strike, code, links and #tags. */
fun noteInline(text: String, accent: Color, codeBg: Color): AnnotatedString = buildAnnotatedString {
    var last = 0
    for (m in inlineToken.findAll(text)) {
        append(text.substring(last, m.range.first))
        val g = m.groupValues
        when {
            g[1].isNotEmpty() -> withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(g[1]) }
            g[2].isNotEmpty() -> withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(g[2]) }
            g[3].isNotEmpty() -> withStyle(SpanStyle(textDecoration = TextDecoration.LineThrough)) { append(g[3]) }
            g[4].isNotEmpty() -> withStyle(SpanStyle(fontFamily = FontFamily.Monospace, background = codeBg)) { append(g[4]) }
            g[5].isNotEmpty() -> withStyle(SpanStyle(fontStyle = FontStyle.Italic)) { append(g[5]) }
            g[6].isNotEmpty() -> withStyle(SpanStyle(fontStyle = FontStyle.Italic)) { append(g[6]) }
            g[7].isNotEmpty() -> withStyle(SpanStyle(color = accent, textDecoration = TextDecoration.Underline)) { append(g[7]) }
            g[10].isNotEmpty() -> withStyle(SpanStyle(textDecoration = TextDecoration.Underline)) { append(g[10]) }
            g[9].isNotEmpty() -> withStyle(SpanStyle(color = accent, fontWeight = FontWeight.Medium)) { append("#" + g[9]) }
        }
        last = m.range.last + 1
    }
    append(text.substring(last))
}

/** Rendered note body. Checkbox rows are interactive through [onToggleCheck] (source line index). */
@Composable
fun NoteMarkdownView(
    body: String,
    onToggleCheck: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    val scheme = MaterialTheme.colorScheme
    val accent = scheme.primary
    val codeBg = scheme.surfaceContainerHigh
    val lines = body.split('\n')
    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
        var i = 0
        while (i < lines.size) {
            val raw = lines[i]
            val index = i
            when {
                raw.trimStart().startsWith("```") -> {
                    val code = StringBuilder()
                    i++
                    while (i < lines.size && !lines[i].trimStart().startsWith("```")) {
                        if (code.isNotEmpty()) code.append('\n')
                        code.append(lines[i]); i++
                    }
                    Text(
                        code.toString(),
                        fontFamily = FontFamily.Monospace,
                        fontSize = 13.sp,
                        color = scheme.onSurface,
                        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(codeBg).padding(14.dp),
                    )
                }
                raw.isBlank() -> Box(Modifier.height(6.dp))
                Regex("^\\s*([-*_]\\s*){3,}$").matches(raw) -> Box(Modifier.fillMaxWidth().height(1.dp).background(scheme.outlineVariant))
                Regex("^\\s{0,3}#{1,6}\\s+.*").matches(raw) -> {
                    val level = raw.trimStart().takeWhile { it == '#' }.length
                    val style = when (level) {
                        1 -> MaterialTheme.typography.headlineSmall
                        2 -> MaterialTheme.typography.titleLarge
                        else -> MaterialTheme.typography.titleMedium
                    }
                    Text(
                        noteInline(raw.trimStart().drop(level).trim(), accent, codeBg),
                        style = style, fontWeight = FontWeight.SemiBold, color = scheme.onSurface,
                        modifier = Modifier.padding(top = 6.dp),
                    )
                }
                Regex("^\\s*[-*+]\\s\\[[ xX]](\\s.*)?$").matches(raw) -> {
                    val done = Regex("\\[[xX]]").containsMatchIn(raw.take(raw.indexOf(']') + 1))
                    val text = raw.substring(raw.indexOf(']') + 1).trim()
                    val indent = (raw.length - raw.trimStart().length).coerceAtMost(8) * 6
                    Row(
                        Modifier.fillMaxWidth().padding(start = indent.dp).clip(RoundedCornerShape(12.dp))
                            .clickable { onToggleCheck(index) }.padding(vertical = 4.dp),
                        verticalAlignment = Alignment.Top,
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Box(
                            Modifier.padding(top = 2.dp).size(22.dp).clip(RoundedCornerShape(7.dp))
                                .background(if (done) scheme.primary else scheme.surfaceContainerHighest),
                            contentAlignment = Alignment.Center,
                        ) {
                            if (done) Icon(Icons.Filled.Check, null, tint = scheme.onPrimary, modifier = Modifier.size(16.dp))
                        }
                        Text(
                            noteInline(text, accent, codeBg),
                            style = MaterialTheme.typography.bodyLarge,
                            color = if (done) scheme.onSurfaceVariant else scheme.onSurface,
                            textDecoration = if (done) TextDecoration.LineThrough else null,
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
                Regex("^\\s*([-*+]|\\d+[.)])\\s+.*").matches(raw) -> {
                    val marker = Regex("^\\s*([-*+]|\\d+[.)])\\s+").find(raw)!!
                    val ordered = marker.groupValues[1].first().isDigit()
                    val indent = (raw.length - raw.trimStart().length).coerceAtMost(8) * 6
                    Row(Modifier.fillMaxWidth().padding(start = indent.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(
                            if (ordered) marker.groupValues[1] else "\u2022",
                            style = MaterialTheme.typography.bodyLarge, color = scheme.primary, fontWeight = FontWeight.SemiBold,
                        )
                        Text(
                            noteInline(raw.substring(marker.value.length), accent, codeBg),
                            style = MaterialTheme.typography.bodyLarge, color = scheme.onSurface, modifier = Modifier.weight(1f),
                        )
                    }
                }
                raw.trimStart().startsWith(">") -> Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(Modifier.size(width = 4.dp, height = 22.dp).clip(RoundedCornerShape(2.dp)).background(scheme.primary))
                    Text(
                        noteInline(raw.trimStart().removePrefix(">").trim(), accent, codeBg),
                        style = MaterialTheme.typography.bodyLarge, color = scheme.onSurfaceVariant, fontStyle = FontStyle.Italic,
                        modifier = Modifier.weight(1f),
                    )
                }
                else -> Text(
                    noteInline(raw, accent, codeBg),
                    style = MaterialTheme.typography.bodyLarge, color = scheme.onSurface,
                )
            }
            i++
        }
    }
}
