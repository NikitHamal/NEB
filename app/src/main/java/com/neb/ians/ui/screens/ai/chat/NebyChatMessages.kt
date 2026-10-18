package com.neb.ians.ui.screens.ai.chat

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ContentCopy
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Refresh
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.produceState
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameMillis
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiArenaMessage
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.pixel.NebyPixel
import com.neb.ians.ui.pixel.NebyState
import com.neb.ians.ui.pixel.PixelChatSprites
import com.neb.ians.ui.pixel.PixelSpriteView
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import kotlin.math.max

/** What Neby is doing with the latest message. */
enum class ChatPhase { Idle, Thinking, Reading, Writing }

@Immutable
data class ChatActions(
    val onCopy: (String) -> Unit,
    val onShare: (String) -> Unit,
    val onRegenerate: () -> Unit
)

/**
 * Streaming text arrives in bursts (a few tokens per network read). This plays it out at a
 * steady, readable pace instead: the shown length eases toward the received length, fast when
 * far behind and gently when close, and only whole frames at most 30 times a second, so a long
 * answer never re-parses its markdown more than it must.
 */
@Composable
fun rememberSmoothText(target: String, streaming: Boolean): String {
    val reduced = nebAnimationsReduced()
    var shown by remember { mutableIntStateOf(if (streaming) 0 else target.length) }
    val latest by rememberUpdatedState(target)
    LaunchedEffect(streaming, reduced) {
        if (!streaming || reduced) return@LaunchedEffect
        var last = 0L
        var carry = 0f
        while (true) {
            withFrameMillis { now ->
                val dt = if (last == 0L) 16L else (now - last).coerceIn(1L, 100L)
                if (now - last >= 33L || last == 0L) {
                    val behind = latest.length - shown
                    if (behind > 0) {
                        carry += max(42f, behind * 5.5f) * dt / 1000f
                        val step = carry.toInt()
                        if (step > 0) { carry -= step; shown = minOf(latest.length, shown + step) }
                    } else carry = 0f
                    last = now
                }
            }
        }
    }
    if (!streaming || reduced) return target
    // never stop inside a markdown marker or a word; finish the word instead
    var end = minOf(shown, target.length)
    val from = end
    while (end < target.length && end - from < 12 && !target[end].isWhitespace()) end++
    return target.substring(0, end)
}

@Composable
fun UserMessage(message: ApiArenaMessage, onCopy: (String) -> Unit, modifier: Modifier = Modifier) {
    Column(modifier.fillMaxWidth(), horizontalAlignment = Alignment.End) {
        if (message.attachments.isNotEmpty()) {
            Row(
                Modifier.horizontalScroll(rememberScrollState()).padding(bottom = 6.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) { message.attachments.forEach { AttachmentPill(it.fileName.ifBlank { "Attachment" }) } }
        }
        val shape = RoundedCornerShape(22.dp, 22.dp, 6.dp, 22.dp)
        Box(
            Modifier
                .widthIn(max = 320.dp)
                .clip(shape)
                .background(MaterialTheme.colorScheme.inverseSurface)
                .combinedClickable(onClick = {}, onLongClick = { onCopy(message.content) })
                .padding(horizontal = 16.dp, vertical = 11.dp)
        ) {
            Text(message.content.ifBlank { "…" }, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.inverseOnSurface)
        }
    }
}

/**
 * Neby's answer: a header with pixel Neby (thinking, talking, then idle), the answer streamed
 * smoothly with a pixel caret, and the actions once it has landed.
 */
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun AssistantMessage(
    message: ApiArenaMessage,
    phase: ChatPhase,
    isLast: Boolean,
    modelLabel: String?,
    actions: ChatActions,
    modifier: Modifier = Modifier
) {
    val streaming = phase != ChatPhase.Idle
    val text = rememberSmoothText(message.content, streaming)
    var landed by remember { mutableStateOf(false) }
    var wasStreaming by remember { mutableStateOf(streaming) }
    LaunchedEffect(streaming) {
        if (wasStreaming && !streaming && message.content.isNotBlank()) landed = true
        wasStreaming = streaming
    }
    Column(modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Box(contentAlignment = Alignment.Center) {
                NebyPixel(
                    state = when (phase) {
                        ChatPhase.Thinking -> NebyState.Think
                        ChatPhase.Reading -> NebyState.Read
                        ChatPhase.Writing -> NebyState.Talk
                        ChatPhase.Idle -> NebyState.Idle
                    },
                    size = 30.dp,
                    avatar = true,
                    ambient = isLast
                )
                if (landed) {
                    PixelSpriteView(PixelChatSprites.sparkle, Modifier.size(30.dp).graphicsLayer { translationX = 16.dp.toPx(); translationY = -14.dp.toPx() })
                    LaunchedEffect(Unit) { kotlinx.coroutines.delay(900); landed = false }
                }
            }
            Text("Neby", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
            if (!modelLabel.isNullOrBlank()) {
                Text(modelLabel, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
        }
        Spacer(Modifier.height(6.dp))
        if (message.content.isBlank() && streaming) {
            NebyStatus(phase, Modifier.padding(start = 38.dp, top = 2.dp, bottom = 4.dp))
        } else {
            Box(
                Modifier
                    .padding(start = 38.dp)
                    .combinedClickable(onClick = {}, onLongClick = { if (message.content.isNotBlank()) actions.onCopy(message.content) })
            ) {
                Column {
                    MarkdownText(markdown = text.ifBlank { message.content }, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurface)
                    if (streaming) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(top = 6.dp)) {
                            PixelSpriteView(PixelChatSprites.caret, Modifier.size(width = 6.dp, height = 18.dp))
                            PixelSpriteView(PixelChatSprites.writing, Modifier.size(width = 36.dp, height = 22.dp))
                        }
                    }
                }
            }
        }
        AnimatedVisibility(
            visible = !streaming && message.content.isNotBlank(),
            enter = fadeIn(nebEffectsSpec()) + expandVertically(nebSpatialSpec()),
            exit = fadeOut(nebEffectsSpec())
        ) {
            Row(Modifier.padding(start = 30.dp, top = 4.dp), horizontalArrangement = Arrangement.spacedBy(2.dp)) {
                MessageAction(Icons.Outlined.ContentCopy, "Copy") { actions.onCopy(message.content) }
                MessageAction(Icons.Outlined.Share, "Share") { actions.onShare(message.content) }
                if (isLast) MessageAction(Icons.Outlined.Refresh, "Regenerate", actions.onRegenerate)
            }
        }
    }
}

@Composable
private fun MessageAction(icon: ImageVector, label: String, onClick: () -> Unit) {
    Row(
        Modifier
            .clip(RoundedCornerShape(12.dp))
            .nebPressable(onClick = onClick)
            .padding(horizontal = 8.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(icon, contentDescription = label, modifier = Modifier.size(16.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

/** The pixel loader with what Neby is doing, its label breathing while it waits. */
@Composable
fun NebyStatus(phase: ChatPhase, modifier: Modifier = Modifier, label: String? = null) {
    val reduced = nebAnimationsReduced()
    val clock by produceState(0L, reduced) { if (!reduced) while (true) withFrameMillis { value = it } }
    Row(modifier, verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        val fade = nebEffectsSpec<Float>()
        AnimatedContent(
            targetState = phase,
            transitionSpec = { fadeIn(fade) togetherWith fadeOut(fade) },
            label = "loader"
        ) { p ->
            when (p) {
                ChatPhase.Reading -> PixelSpriteView(PixelChatSprites.reading, Modifier.size(width = 26.dp, height = 30.dp))
                else -> PixelSpriteView(PixelChatSprites.thinking, Modifier.size(width = 45.dp, height = 21.dp))
            }
        }
        Text(
            label ?: when (phase) { ChatPhase.Reading -> "Reading your files"; ChatPhase.Writing -> "Writing"; else -> "Thinking" },
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.graphicsLayer { alpha = if (reduced) 1f else 0.7f + 0.3f * kotlin.math.sin(clock / 260f) }
        )
    }
}

@Composable
private fun AttachmentPill(name: String) {
    Row(
        Modifier
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(Icons.Outlined.Description, contentDescription = null, modifier = Modifier.size(15.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(name, style = MaterialTheme.typography.labelMedium, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.widthIn(max = 160.dp))
    }
}

/** A new message slides up and fades in once, the first time it is shown. */
@Composable
fun Modifier.enterOnce(key: Any, enabled: Boolean): Modifier {
    if (!enabled || nebAnimationsReduced()) return this
    val a = remember(key) { Animatable(0f) }
    val spec = nebSpatialSpec<Float>()
    LaunchedEffect(key) { a.animateTo(1f, spec) }
    return this.graphicsLayer {
        alpha = a.value.coerceIn(0f, 1f)
        translationY = (1f - a.value) * 18.dp.toPx()
    }
}

