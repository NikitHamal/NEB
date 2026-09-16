package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
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
import androidx.compose.material.icons.filled.CenterFocusStrong
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.CanvasNode
import com.neb.ians.ui.components.MarkdownInlineText
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject

internal val CANVAS_CARD_WIDTH: Dp = 340.dp

@Composable
fun CanvasCard(
    node: CanvasNode,
    onDrag: (dxDp: Float, dyDp: Float) -> Unit,
    onDragEnd: () -> Unit,
    onOpenInspector: () -> Unit,
    onFocus: () -> Unit,
    onDelete: () -> Unit,
    onRetry: () -> Unit,
    onFollowup: (String) -> Unit,
    onReportHeight: (Float) -> Unit
) {
    val primary = MaterialTheme.colorScheme.primary
    val kindColor = canvasKindColor(node.kind, primary)
    val metaColor = canvasMetaColor(node.meta, primary)
    val stripe = if (metaColor != Color.Unspecified) metaColor else kindColor
    val content = node.content
    val title = content?.str("title")?.takeIf { it.isNotBlank() } ?: node.title.ifBlank { "Untitled" }
    val summary = content?.str("summary") ?: ""
    val generating = node.status == "generating"
    val failed = node.status == "failed"

    val density = LocalDensity.current
    Box(
        modifier = Modifier
            .width(CANVAS_CARD_WIDTH)
            .onGloballyPositioned { coords ->
                onReportHeight(with(density) { coords.size.height.toDp().value })
            }
    ) {
        Surface(
            shape = RoundedCornerShape(16.dp),
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            shadowElevation = 6.dp,
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
        ) {
            Row(modifier = Modifier.fillMaxWidth()) {
                Box(
                    modifier = Modifier
                        .width(4.dp)
                        .height(64.dp)
                        .background(stripe, RoundedCornerShape(topStart = 16.dp, bottomStart = 16.dp))
                )
                Column(modifier = Modifier.weight(1f)) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .pointerInput(node.id) {
                                detectTapGestures(
                                    onTap = { onOpenInspector() },
                                    onDoubleTap = { onOpenInspector() }
                                )
                            }
                            .pointerInput(node.id) {
                                detectDragGestures(
                                    onDragEnd = { onDragEnd() }
                                ) { change, dragAmount ->
                                    change.consume()
                                    onDrag(dragAmount.x, dragAmount.y)
                                }
                            }
                            .padding(start = 14.dp, top = 12.dp, end = 6.dp, bottom = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = title,
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            modifier = Modifier.weight(1f),
                            maxLines = 2
                        )
                        IconButton(onClick = onFocus, modifier = Modifier.size(32.dp)) {
                            Icon(Icons.Filled.CenterFocusStrong, contentDescription = "Focus", modifier = Modifier.size(18.dp))
                        }
                        IconButton(onClick = onOpenInspector, modifier = Modifier.size(32.dp)) {
                            Icon(Icons.Filled.Tune, contentDescription = "Edit", modifier = Modifier.size(18.dp))
                        }
                        IconButton(onClick = onDelete, modifier = Modifier.size(32.dp)) {
                            Icon(Icons.Filled.Close, contentDescription = "Delete", modifier = Modifier.size(18.dp))
                        }
                    }
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(start = 14.dp, end = 14.dp, bottom = 12.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        when {
                            generating -> GeneratingRow()
                            failed -> {
                                Text(
                                    node.error ?: "Generation failed",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.error
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Filled.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                                    Spacer(Modifier.width(6.dp))
                                    Text(
                                        "Retry",
                                        style = MaterialTheme.typography.labelLarge,
                                        color = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.clickable(onClick = onRetry)
                                    )
                                }
                            }
                            else -> {
                                if (summary.isNotBlank()) {
                                    MarkdownInlineText(
                                        markdown = summary,
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                }
                                content?.arr("sections")?.forEach { section ->
                                    (section as? JsonObject)?.let { CanvasSection(it) }
                                }
                                NodeFollowupRow(onSend = onFollowup)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun GeneratingRow() {
    val pulse by rememberInfiniteTransition(label = "cv_gen").animateFloat(
        initialValue = 0.35f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(700, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "pulse"
    )
    Row(verticalAlignment = Alignment.CenterVertically) {
        repeat(3) {
            Box(
                modifier = Modifier
                    .padding(end = 6.dp)
                    .size(8.dp)
                    .alpha(pulse)
                    .background(MaterialTheme.colorScheme.primary, CircleShape)
            )
        }
        Text(
            "Generating…",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun NodeFollowupRow(onSend: (String) -> Unit) {
    var draft by remember { mutableStateOf("") }
    Row(verticalAlignment = Alignment.CenterVertically) {
        OutlinedTextField(
            value = draft,
            onValueChange = { draft = it },
            placeholder = { Text("Ask a follow-up…") },
            singleLine = true,
            textStyle = MaterialTheme.typography.bodySmall,
            modifier = Modifier.weight(1f),
            shape = RoundedCornerShape(20.dp)
        )
        Spacer(Modifier.width(6.dp))
        IconButton(
            onClick = {
                if (draft.isNotBlank()) {
                    onSend(draft.trim())
                    draft = ""
                }
            },
            modifier = Modifier.size(36.dp)
        ) {
            Icon(Icons.Filled.Send, contentDescription = "Send", tint = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
private fun CanvasSection(section: JsonObject) {
    when (section.str("type")) {
        "text" -> MarkdownInlineText(
            markdown = section.str("content"),
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface
        )
        "bullets" -> CanvasSectionTitle(section.str("title")) {
            section.arr("items").forEach { item ->
                BulletLine(item.asStr())
            }
        }
        "stats" -> {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                section.arr("items").forEach { item ->
                    val o = item as? JsonObject ?: return@forEach
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(o.str("k"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Text(o.str("v"), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
        }
        "timeline" -> CanvasSectionTitle(section.str("title")) {
            section.arr("steps").forEach { item ->
                val o = item as? JsonObject ?: return@forEach
                Row(verticalAlignment = Alignment.Top) {
                    Box(Modifier.padding(top = 6.dp).size(8.dp).background(MaterialTheme.colorScheme.primary, CircleShape))
                    Spacer(Modifier.width(8.dp))
                    Column {
                        Text(o.str("title"), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
                        if (o.str("sub").isNotBlank()) {
                            Text(o.str("sub"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
        "flow" -> CanvasSectionTitle(section.str("title")) {
            section.arr("nodes").forEach { item ->
                val o = item as? JsonObject ?: return@forEach
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(canvasToneColor(o.str("tone")).copy(alpha = 0.12f), RoundedCornerShape(10.dp))
                        .padding(10.dp)
                ) {
                    Text(o.str("label"), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = canvasToneColor(o.str("tone")))
                    if (o.str("desc").isNotBlank()) {
                        Spacer(Modifier.width(6.dp))
                        Text(o.str("desc"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
            val links = section.arr("links")
            if (links.isNotEmpty()) {
                Text(
                    links.map { it.asStr() }.joinToString(" → "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        "quote" -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh, RoundedCornerShape(10.dp))
                    .padding(12.dp)
            ) {
                Text("“${section.str("text")}”", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
                if (section.str("cite").isNotBlank()) {
                    Spacer(Modifier.height(4.dp))
                    Text("— ${section.str("cite")}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        "code" -> {
            Text(
                section.str("text"),
                style = MaterialTheme.typography.bodySmall.copy(fontFamily = FontFamily.Monospace),
                color = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF0B1C30), RoundedCornerShape(10.dp))
                    .padding(12.dp)
            )
        }
        "proscons" -> CanvasSectionTitle(section.str("title")) {
            section.arr("pros").forEach { BulletLine("+ ${it.asStr()}", Color(0xFF16A34A)) }
            section.arr("cons").forEach { BulletLine("− ${it.asStr()}", Color(0xFFE11D48)) }
        }
        "comparison" -> {
            val headers = section.arr("headers").map { it.asStr() }
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                if (section.str("title").isNotBlank()) {
                    Text(section.str("title"), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                }
                if (headers.size >= 3) {
                    Text(headers.joinToString(" · "), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                }
                section.arr("rows").forEach { row ->
                    Text(
                        (row as? JsonArray)?.map { it.asStr() }?.joinToString(" · ") ?: row.asStr(),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                }
            }
        }
        "cards" -> CanvasSectionTitle(section.str("title")) {
            section.arr("items").forEach { item ->
                val o = item as? JsonObject ?: return@forEach
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surfaceContainerHigh, RoundedCornerShape(10.dp))
                        .padding(10.dp)
                ) {
                    Text(o.str("title"), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                    if (o.str("subtitle").isNotBlank()) {
                        Text(o.str("subtitle"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                    }
                    o.arr("bullets").forEach { BulletLine(it.asStr()) }
                    if (o.str("desc").isNotBlank()) {
                        Text(o.str("desc"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
        "references" -> {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text("References", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                section.arr("items").forEach { item ->
                    val o = item as? JsonObject ?: return@forEach
                    Text(
                        "• ${o.str("title")}${o.str("source").takeIf { it.isNotBlank() }?.let { " ($it)" } ?: ""}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
        "ask_user" -> {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(10.dp))
                    .padding(12.dp)
            ) {
                Text(section.str("question"), style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
                section.arr("options").forEach { BulletLine(it.asStr()) }
            }
        }
        "diagram" -> {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                if (section.str("title").isNotBlank()) {
                    Text(section.str("title"), style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                }
                section.arr("nodes").forEach { item ->
                    val o = item as? JsonObject ?: return@forEach
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(MaterialTheme.colorScheme.surfaceContainerHigh, RoundedCornerShape(10.dp))
                            .padding(10.dp)
                    ) {
                        Text(o.str("label"), style = MaterialTheme.typography.bodySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                        if (o.str("desc").isNotBlank()) {
                            Spacer(Modifier.width(6.dp))
                            Text(o.str("desc"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
                if (section.str("note").isNotBlank()) {
                    Text(section.str("note"), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        else -> {
            val fallback = section.str("content").ifBlank { section.str("text") }
            if (fallback.isNotBlank()) {
                MarkdownInlineText(markdown = fallback, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}

@Composable
private fun CanvasSectionTitle(title: String, content: @Composable () -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        if (title.isNotBlank()) {
            Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
        }
        content()
    }
}

@Composable
private fun BulletLine(text: String, dotColor: Color = MaterialTheme.colorScheme.primary) {
    if (text.isBlank()) return
    Row(verticalAlignment = Alignment.Top) {
        Box(Modifier.padding(top = 7.dp).size(6.dp).background(dotColor, CircleShape))
        Spacer(Modifier.width(8.dp))
        MarkdownInlineText(markdown = text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
    }
}
