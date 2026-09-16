package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.MarkdownInlineText
import kotlinx.serialization.json.JsonObject

internal val CANVAS_WIDGET_WIDTH = 280.dp

@Composable
fun CanvasWidgetCard(
    obj: JsonObject,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    val kind = obj.str("kind").ifBlank { "quiz" }
    val topic = obj.str("topic")
    val state = obj.obj("state")

    Surface(
        shape = RoundedCornerShape(14.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        shadowElevation = 6.dp,
        modifier = modifier
            .width(CANVAS_WIDGET_WIDTH)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(14.dp))
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.primaryContainer)
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = (topic.ifBlank { kind.replaceFirstChar { it.uppercase() } }),
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                    modifier = Modifier.weight(1f),
                    maxLines = 1
                )
                IconButton(onClick = onDelete, modifier = Modifier.size(28.dp)) {
                    Icon(Icons.Filled.Close, contentDescription = "Delete", modifier = Modifier.size(16.dp))
                }
            }
            Box(modifier = Modifier.padding(12.dp)) {
                when (kind) {
                    "quiz" -> QuizBody(state)
                    "flash" -> FlashBody(state)
                    "flow" -> FlowBody(state)
                    "timeline" -> TimelineBody(state)
                    "poll" -> PollBody(state)
                    else -> Text(
                        topic.ifBlank { "Widget" },
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                }
            }
        }
    }
}

@Composable
private fun QuizBody(state: JsonObject?) {
    if (state == null) return
    var picked by remember(state) { mutableIntStateOf(-1) }
    val options = state.arr("options").map { it.asStr() }
    val answer = state.str("answer")
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        MarkdownInlineText(
            markdown = state.str("q").ifBlank { state.str("question") },
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface
        )
        options.forEachIndexed { index, option ->
            val isAnswer = option == answer || option == (answer.toIntOrNull()?.let { options.getOrNull(it) })
            val bg = when {
                picked == -1 -> MaterialTheme.colorScheme.surfaceContainerHigh
                isAnswer -> Color(0xFF16A34A).copy(alpha = 0.18f)
                index == picked -> Color(0xFFE11D48).copy(alpha = 0.18f)
                else -> MaterialTheme.colorScheme.surfaceContainerHigh
            }
            val fg = when {
                picked != -1 && isAnswer -> Color(0xFF16A34A)
                picked == index -> Color(0xFFE11D48)
                else -> MaterialTheme.colorScheme.onSurface
            }
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(10.dp))
                    .background(bg)
                    .clickable(enabled = picked == -1) { picked = index }
                    .padding(10.dp)
            ) {
                Text(option, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Medium, color = fg)
            }
        }
    }
}

@Composable
private fun FlashBody(state: JsonObject?) {
    if (state == null) return
    val cards = state.arr("cards").mapNotNull { it as? JsonObject }
    if (cards.isEmpty()) return
    var index by remember(state) { mutableIntStateOf(0) }
    var flipped by remember(state, index) { mutableStateOf(false) }
    val card = cards[index.coerceIn(cards.indices)]
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.surfaceContainerHigh, RoundedCornerShape(10.dp))
                .clickable { flipped = !flipped }
                .padding(14.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                if (flipped) card.str("a") else card.str("q"),
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = if (flipped) FontWeight.Normal else FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurface
            )
        }
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
            IconButton(onClick = { index = (index - 1 + cards.size) % cards.size }, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.ArrowBack, contentDescription = "Previous", modifier = Modifier.size(18.dp))
            }
            Text("${index + 1} / ${cards.size}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            IconButton(onClick = { index = (index + 1) % cards.size }, modifier = Modifier.size(32.dp)) {
                Icon(Icons.Filled.ArrowForward, contentDescription = "Next", modifier = Modifier.size(18.dp))
            }
        }
    }
}

@Composable
private fun FlowBody(state: JsonObject?) {
    if (state == null) return
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        val start = state.obj("start")
        if (start != null) {
            FlowStep(label = start.str("label"), desc = start.str("desc"), highlight = true)
        }
        state.arr("steps").forEach { item ->
            val o = item as? JsonObject ?: return@forEach
            FlowStep(label = o.str("label"), desc = o.str("desc"), highlight = false)
        }
        val decision = state.obj("decision")
        if (decision != null && (decision.str("cond").isNotBlank() || decision.str("yes").isNotBlank())) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFFD97706).copy(alpha = 0.12f), RoundedCornerShape(10.dp))
                    .padding(10.dp)
            ) {
                Text(decision.str("cond"), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = Color(0xFFD97706))
                Text("Yes → ${decision.str("yes")} · No → ${decision.str("no")}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}

@Composable
private fun FlowStep(label: String, desc: String, highlight: Boolean) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                if (highlight) MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)
                else MaterialTheme.colorScheme.surfaceContainerHigh,
                RoundedCornerShape(10.dp)
            )
            .padding(10.dp)
    ) {
        Text(label, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
        if (desc.isNotBlank()) {
            Spacer(Modifier.width(6.dp))
            Text(desc, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun TimelineBody(state: JsonObject?) {
    if (state == null) return
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        state.arr("events").forEach { item ->
            val o = item as? JsonObject ?: return@forEach
            Row(verticalAlignment = Alignment.Top) {
                Box(Modifier.padding(top = 6.dp).size(8.dp).background(MaterialTheme.colorScheme.primary, CircleShape))
                Spacer(Modifier.width(8.dp))
                Column {
                    Text(o.str("t"), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    Text(o.str("d"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurface)
                }
            }
        }
    }
}

@Composable
private fun PollBody(state: JsonObject?) {
    if (state == null) return
    val options = state.arr("options").map { it.asStr() }
        .ifEmpty { state.arr("choices").map { it.asStr() } }
    var votes by remember(state) { mutableStateOf(List(options.size) { 0 }) }
    var voted by remember(state) { mutableIntStateOf(-1) }
    val total = votes.sum().coerceAtLeast(1)
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        val question = state.str("question").ifBlank { state.str("q") }
        if (question.isNotBlank()) {
            Text(question, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
        }
        options.forEachIndexed { index, option ->
            val pct = votes[index].toFloat() / total
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(10.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                    .clickable {
                        if (voted == -1) {
                            voted = index
                            votes = votes.mapIndexed { i, v -> if (i == index) v + 1 else v }
                        }
                    }
                    .padding(10.dp)
            ) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(option, style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Medium, color = MaterialTheme.colorScheme.onSurface, modifier = Modifier.weight(1f))
                    if (voted != -1) {
                        Text("${(pct * 100).toInt()}%", style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    }
                }
                if (voted != -1) {
                    Spacer(Modifier.height(6.dp))
                    LinearProgressIndicator(progress = { pct }, modifier = Modifier.fillMaxWidth())
                }
            }
        }
    }
}
