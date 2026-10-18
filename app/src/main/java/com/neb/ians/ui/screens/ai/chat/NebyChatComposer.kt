package com.neb.ians.ui.screens.ai.chat

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.ime
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.union
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Stop
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.screens.ai.PendingFile
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSpatialSpec

/**
 * The message box: a rounded well that grows with what you type (up to six lines), attached
 * files as chips inside it, a paperclip, and one key that is Send while you write and Stop
 * while Neby answers. The key springs in when there is something to send.
 */
@Composable
fun NebyChatComposer(
    value: String,
    onValueChange: (String) -> Unit,
    pendingFiles: List<PendingFile>,
    streaming: Boolean,
    canAttach: Boolean,
    onAttach: () -> Unit,
    onRemoveFile: (PendingFile) -> Unit,
    onSend: () -> Unit,
    onStop: () -> Unit,
    modifier: Modifier = Modifier
) {
    val ready = value.isNotBlank() || pendingFiles.isNotEmpty()
    val shape = RoundedCornerShape(26.dp)
    val ring by animateColorAsState(
        if (ready || streaming) MaterialTheme.colorScheme.onSurface.copy(alpha = 0.32f) else MaterialTheme.colorScheme.outlineVariant,
        nebEffectsSpec(), label = "ring"
    )
    Box(
        modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
            .windowInsetsPadding(WindowInsets.ime.union(WindowInsets.navigationBars))
            .padding(start = 12.dp, end = 12.dp, top = 6.dp, bottom = 10.dp)
    ) {
        Column(
            Modifier
                .fillMaxWidth()
                .clip(shape)
                .background(MaterialTheme.colorScheme.surfaceContainerLow)
                .border(1.dp, ring, shape)
                .padding(6.dp)
        ) {
            AnimatedVisibility(
                visible = pendingFiles.isNotEmpty(),
                enter = expandVertically(nebSpatialSpec()) + fadeIn(nebEffectsSpec()),
                exit = shrinkVertically(nebSpatialSpec()) + fadeOut(nebEffectsSpec())
            ) {
                Row(
                    Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(start = 6.dp, end = 6.dp, top = 4.dp, bottom = 6.dp),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) { pendingFiles.forEach { file -> FileChip(file) { onRemoveFile(file) } } }
            }
            Row(verticalAlignment = Alignment.Bottom) {
                if (canAttach) {
                    Box(
                        Modifier.size(44.dp).clip(RoundedCornerShape(16.dp)).nebPressable(enabled = !streaming, onClick = onAttach),
                        contentAlignment = Alignment.Center
                    ) { Icon(Icons.Outlined.AttachFile, contentDescription = "Attach files", tint = MaterialTheme.colorScheme.onSurfaceVariant) }
                }
                Box(
                    Modifier.weight(1f).heightIn(min = 44.dp).padding(start = if (canAttach) 2.dp else 12.dp, end = 6.dp, top = 11.dp, bottom = 11.dp)
                ) {
                    if (value.isEmpty()) {
                        Text(if (streaming) "Neby is answering…" else "Ask Neby anything", style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    BasicTextField(
                        value = value,
                        onValueChange = onValueChange,
                        textStyle = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
                        cursorBrush = SolidColor(MaterialTheme.colorScheme.onSurface),
                        maxLines = 6,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
                SendKey(ready = ready, streaming = streaming, onSend = onSend, onStop = onStop)
            }
        }
    }
}

@Composable
private fun SendKey(ready: Boolean, streaming: Boolean, onSend: () -> Unit, onStop: () -> Unit) {
    val active = ready || streaming
    val scale by animateFloatAsState(if (active) 1f else 0.86f, nebFastSpatialSpec(), label = "key")
    val bg by animateColorAsState(
        if (active) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.surfaceContainerHighest,
        nebEffectsSpec(), label = "keybg"
    )
    val fg = if (active) MaterialTheme.colorScheme.surface else MaterialTheme.colorScheme.onSurfaceVariant
    val pop = nebSpatialSpec<Float>(); val fade = nebEffectsSpec<Float>()
    Box(
        Modifier
            .size(44.dp)
            .graphicsLayer { scaleX = scale; scaleY = scale }
            .clip(RoundedCornerShape(16.dp))
            .background(bg)
            .nebPressable(enabled = active, onClick = { if (streaming) onStop() else onSend() }),
        contentAlignment = Alignment.Center
    ) {
        AnimatedContent(
            targetState = streaming,
            transitionSpec = { (scaleIn(pop) + fadeIn(fade)) togetherWith (scaleOut(pop) + fadeOut(fade)) },
            label = "sendstop"
        ) { stop ->
            Icon(
                if (stop) Icons.Outlined.Stop else Icons.AutoMirrored.Outlined.ArrowForward,
                contentDescription = if (stop) "Stop" else "Send",
                tint = fg,
                modifier = Modifier.size(22.dp)
            )
        }
    }
}

@Composable
private fun FileChip(file: PendingFile, onRemove: () -> Unit) {
    Row(
        Modifier
            .clip(RoundedCornerShape(14.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .padding(start = 10.dp, end = 4.dp, top = 4.dp, bottom = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(Icons.Outlined.Description, contentDescription = null, modifier = Modifier.size(15.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(file.name, style = MaterialTheme.typography.labelMedium, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.widthIn(max = 140.dp))
        Box(Modifier.size(26.dp).clip(RoundedCornerShape(9.dp)).nebPressable(onClick = onRemove), contentAlignment = Alignment.Center) {
            Icon(Icons.Outlined.Close, contentDescription = "Remove ${file.name}", modifier = Modifier.size(15.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
