@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)

package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.combinedClickable
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
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.PushPin
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.local.entity.NoteEntity
import com.neb.ians.ui.components.InlineImageTokens
import com.neb.ians.ui.components.LiveColors
import com.neb.ians.ui.components.LiveMarkdown
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

private sealed interface PreviewLine {
    data class Plain(val text: AnnotatedString) : PreviewLine
    data class Check(val text: AnnotatedString, val done: Boolean) : PreviewLine
}

private val previewCheck = Regex("^\\s*[-*+]\\s\\[([ xX])]\\s?(.*)$")
private val previewSkip = setOf("[image]", "[audio recording]", "[drawing]")
private val previewRule = Regex("^\\s*(-{3,}|\\*{3,}|_{3,})\\s*$")

/** The first lines of a note as they will look: markers are hidden and their effect drawn, never shown as characters. */
private fun previewLines(body: String, max: Int, colors: LiveColors): List<PreviewLine> {
    val out = ArrayList<PreviewLine>()
    var inCode = false
    for (line in body.lineSequence()) {
        if (line.trimStart().startsWith("```")) { inCode = !inCode; continue }
        val raw = InlineImageTokens.plainText(line, "").replace(LiveMarkdown.ZWSP, "")
        if (inCode || raw.isBlank() || previewRule.matches(raw) || raw.trim() in previewSkip) continue
        val chk = previewCheck.find(raw)
        if (chk != null) {
            val text = LiveMarkdown.transform(chk.groupValues[2].trim(), colors).styled
            if (text.isNotEmpty()) out += PreviewLine.Check(text, chk.groupValues[1].lowercase() == "x")
        } else {
            val text = LiveMarkdown.transform(raw.trim(), colors).styled
            if (text.isNotEmpty()) out += PreviewLine.Plain(text)
        }
        if (out.size >= max) break
    }
    return out
}

private fun dateLabel(ms: Long): String {
    val now = Calendar.getInstance()
    val then = Calendar.getInstance().apply { timeInMillis = ms }
    val sameDay = now.get(Calendar.YEAR) == then.get(Calendar.YEAR) && now.get(Calendar.DAY_OF_YEAR) == then.get(Calendar.DAY_OF_YEAR)
    val days = (now.timeInMillis - ms) / 86_400_000L
    val pattern = when {
        sameDay -> "h:mm a"
        days < 7 -> "EEE"
        now.get(Calendar.YEAR) == then.get(Calendar.YEAR) -> "MMM d"
        else -> "MMM d, yyyy"
    }
    return SimpleDateFormat(pattern, Locale.getDefault()).format(ms)
}

/**
 * One note in the list. Short on purpose: a title, a few lines, one small preview of what the note holds (pictures,
 * recording, drawing, table, code) and one footer line, so the staggered columns stay dense and differ in height only
 * by what the notes really contain.
 */
@Composable
internal fun NoteCard(
    note: NoteEntity,
    selected: Boolean,
    compact: Boolean,
    onClick: () -> Unit,
    onLongClick: () -> Unit,
) {
    val c = MaterialTheme.colorScheme
    val tone = noteTone(note.tone)
    val ink = tone.content
    val shape = RoundedCornerShape(22.dp)
    val live = remember(tone) { LiveColors(ink.copy(alpha = 0.12f), ink, ink, ink.copy(alpha = 0.75f), ink.copy(alpha = 0.6f)) }
    val key = remember(note.id, note.updatedAt) { NoteMediaCache.key(note) }
    val media by produceState(NoteMediaCache.peek(key), key) {
        value = NoteMediaCache.peek(key) ?: withContext(Dispatchers.Default) { NoteMediaCache.of(note) }
    }
    val m = media ?: NoteMedia.None
    val hasMedia = m.hasAny
    val maxEntries = if (hasMedia) 2 else if (compact) 4 else 3
    val lines = remember(note.body, maxEntries, live) { previewLines(note.body, maxEntries, live) }
    val (done, total) = remember(note.body) { NoteFormatting.checkProgress(note.body) }
    val nextDue = remember(note.doc) {
        if (!note.doc.contains("\"Todo\"") || !note.doc.contains("\"d\"")) 0L
        else NoteDoc.fromJson(note.doc).filter { it.type == BlockType.Todo && !it.checked && it.due > 0L }.minOfOrNull { it.due } ?: 0L
    }
    val date = remember(note.updatedAt) { dateLabel(note.updatedAt) }
    val border = when {
        selected -> BorderStroke(2.dp, c.primary)
        tone.hairline -> BorderStroke(1.dp, c.outlineVariant)
        else -> null
    }
    Column(
        Modifier.fillMaxWidth().clip(shape).background(tone.container)
            .then(if (border != null) Modifier.border(border, shape) else Modifier)
            .combinedClickable(onClick = onClick, onLongClick = onLongClick),
    ) {
        if (note.cover != 0) {
            val ctx = LocalContext.current
            val photo = if (note.cover < 0 && note.coverPhoto.isNotEmpty()) File(ctx.filesDir, "notes/${note.id}/${note.coverPhoto}") else null
            NoteCover(note.cover, photo, Modifier.fillMaxWidth().height(if (compact) 44.dp else 60.dp), animate = false, light = true)
        }
        val pad = if (compact) 11.dp else 14.dp
        Column(Modifier.fillMaxWidth().padding(horizontal = pad, vertical = if (compact) 9.dp else 11.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
            val hasTitle = note.title.isNotBlank()
            if (hasTitle || note.icon.isNotEmpty() || selected || note.pinned) Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                if (note.icon.isNotEmpty()) NoteIconTile(note.icon, if (compact) 22.dp else 26.dp, container = ink.copy(alpha = 0.12f), content = ink)
                if (hasTitle) Text(
                    note.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = ink,
                    maxLines = 2, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f),
                ) else Box(Modifier.weight(1f))
                if (selected) Icon(Icons.Outlined.Check, null, tint = readableOn(c.primary, tone.container, 3f), modifier = Modifier.size(18.dp))
                else if (note.pinned) Icon(Icons.Outlined.PushPin, "Pinned", tint = readableOn(ink, tone.container, 3f), modifier = Modifier.size(15.dp))
            }
            lines.forEachIndexed { i, line ->
                val cap = if (i == 0) (if (hasMedia) 2 else 3) else if (hasMedia) 1 else 2
                when (line) {
                    is PreviewLine.Plain -> Text(
                        line.text, style = MaterialTheme.typography.bodySmall.copy(lineHeight = 17.sp), color = ink.copy(alpha = 0.86f),
                        maxLines = cap, overflow = TextOverflow.Ellipsis,
                    )
                    is PreviewLine.Check -> Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                        Box(
                            Modifier.padding(top = 2.dp).size(13.dp).clip(RoundedCornerShape(4.dp))
                                .background(if (line.done) c.primary else ink.copy(alpha = 0.18f)),
                            contentAlignment = Alignment.Center,
                        ) { if (line.done) Icon(Icons.Outlined.Check, null, tint = c.onPrimary, modifier = Modifier.size(10.dp)) }
                        Text(
                            line.text, style = MaterialTheme.typography.bodySmall.copy(lineHeight = 17.sp),
                            color = ink.copy(alpha = if (line.done) 0.6f else 0.86f), maxLines = 1, overflow = TextOverflow.Ellipsis,
                        )
                    }
                }
            }
            if (hasMedia) NoteMediaPreview(m, compact, ink, tone.container)
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Text(date, style = MaterialTheme.typography.labelSmall, color = ink.copy(alpha = 0.6f), maxLines = 1, modifier = Modifier.weight(1f))
                if (nextDue > 0L) NoteChipLabel(NoteDue.label(nextDue), if (NoteDue.overdue(nextDue)) c.error else ink, ink)
                else if (note.tagList.isNotEmpty()) NoteChipLabel("#" + note.tagList.first(), ink, ink)
                if (total > 0) Text("$done/$total", style = MaterialTheme.typography.labelSmall, color = ink.copy(alpha = 0.6f))
            }
        }
    }
}

@Composable
private fun NoteChipLabel(text: String, color: androidx.compose.ui.graphics.Color, ink: androidx.compose.ui.graphics.Color) {
    Text(
        text, style = MaterialTheme.typography.labelSmall, color = color, maxLines = 1, overflow = TextOverflow.Ellipsis,
        modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(ink.copy(alpha = 0.10f)).padding(horizontal = 7.dp, vertical = 2.dp),
    )
}
