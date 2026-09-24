package com.neb.ians.ui.screens.canvas

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.outlined.Bolt
import androidx.compose.material.icons.outlined.Language
import androidx.compose.material.icons.outlined.Psychology
import androidx.compose.material3.Icon
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec

// ---------------------------------------------------------------------------
// The prompt.
//
// One sheet at the bottom of the board: what you want on the first line, how
// you want it thought about on the second. The send key is a circle while the
// line is empty and squares off the moment there is something to send — the
// only movement here, and it means something.
// ---------------------------------------------------------------------------

@Composable
fun CanvasPromptBar(
    prompt: String,
    isGenerating: Boolean,
    speedMode: String,
    webSearch: Boolean,
    onPromptChange: (String) -> Unit,
    onSpeedModeChange: (String) -> Unit,
    onWebSearchChange: (Boolean) -> Unit,
    onSubmit: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    val canSend = prompt.isNotBlank() && !isGenerating
    val deep = speedMode.equals("deep", ignoreCase = true)

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .imePadding(),
        shape = RoundedCornerShape(26.dp),
        color = if (isDark) scheme.surfaceContainerHigh else Color.White,
        border = BorderStroke(1.dp, scheme.outlineVariant.copy(alpha = 0.8f)),
        shadowElevation = 3.dp
    ) {
        Column(modifier = Modifier.padding(start = 16.dp, end = 8.dp, top = 12.dp, bottom = 8.dp)) {
            BasicTextField(
                value = prompt,
                onValueChange = onPromptChange,
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 24.dp, max = 120.dp),
                textStyle = LocalTextStyle.current.merge(
                    MaterialTheme.typography.bodyMedium.copy(color = scheme.onSurface)
                ),
                cursorBrush = SolidColor(scheme.onSurface),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                keyboardActions = KeyboardActions(onSend = { if (canSend) onSubmit() }),
                decorationBox = { inner ->
                    if (prompt.isEmpty()) {
                        Text(
                            text = "Ask Neby to add a card…",
                            style = MaterialTheme.typography.bodyMedium,
                            color = scheme.onSurfaceVariant.copy(alpha = 0.7f)
                        )
                    }
                    inner()
                }
            )

            Spacer(modifier = Modifier.size(10.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                PromptToggle(
                    label = if (deep) "Deep" else "Fast",
                    icon = if (deep) Icons.Outlined.Psychology else Icons.Outlined.Bolt,
                    selected = deep,
                    onClick = { onSpeedModeChange(if (deep) "fast" else "deep") }
                )
                PromptToggle(
                    label = "Web",
                    icon = Icons.Outlined.Language,
                    selected = webSearch,
                    onClick = { onWebSearchChange(!webSearch) }
                )

                Spacer(modifier = Modifier.weight(1f))

                SendKey(canSend = canSend, isGenerating = isGenerating, onSubmit = onSubmit)
            }
        }
    }
}

@Composable
private fun PromptToggle(
    label: String,
    icon: ImageVector,
    selected: Boolean,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val background by animateColorAsState(
        targetValue = if (selected) scheme.onSurface else Color.Transparent,
        animationSpec = nebEffectsSpec(),
        label = "promptToggleBg"
    )
    val foreground by animateColorAsState(
        targetValue = if (selected) scheme.surface else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "promptToggleFg"
    )

    Row(
        modifier = Modifier
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(99.dp))
            .background(background)
            .border(
                width = 1.dp,
                color = if (selected) Color.Transparent else scheme.outlineVariant,
                shape = RoundedCornerShape(99.dp)
            )
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = foreground,
            modifier = Modifier.size(15.dp)
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Medium),
            color = foreground
        )
    }
}

@Composable
private fun SendKey(
    canSend: Boolean,
    isGenerating: Boolean,
    onSubmit: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val corner by animateDpAsState(
        targetValue = if (canSend) 14.dp else 21.dp,
        animationSpec = nebFastSpatialSpec(),
        label = "sendCorner"
    )
    val background by animateColorAsState(
        targetValue = if (canSend) scheme.onSurface else scheme.onSurface.copy(alpha = 0.10f),
        animationSpec = nebEffectsSpec(),
        label = "sendBg"
    )
    val foreground by animateColorAsState(
        targetValue = if (canSend) scheme.surface else scheme.onSurface.copy(alpha = 0.35f),
        animationSpec = nebEffectsSpec(),
        label = "sendFg"
    )

    Box(
        modifier = Modifier
            .nebPressable(enabled = canSend, onClick = onSubmit)
            .size(42.dp)
            .clip(RoundedCornerShape(corner))
            .background(background),
        contentAlignment = Alignment.Center
    ) {
        if (isGenerating) {
            NebLoader(size = NebLoaderSize.Inline, color = scheme.onSurfaceVariant)
        } else {
            Icon(
                imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                contentDescription = "Send prompt",
                tint = foreground,
                modifier = Modifier.size(19.dp)
            )
        }
    }
}
