package com.consica.code.ui.components

import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import com.consica.code.ui.theme.LocalReducedMotion
import kotlinx.coroutines.delay

/** Rounded 24dp brand card with a subtle border instead of heavy shadows. */
@Composable
fun EcoCard(
    modifier: Modifier = Modifier,
    containerColor: Color = MaterialTheme.colorScheme.surface,
    onClick: (() -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit,
) {
    val shape = RoundedCornerShape(24.dp)
    val border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    val colors = CardDefaults.cardColors(containerColor = containerColor)
    val elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    if (onClick != null) {
        Card(
            onClick = onClick,
            modifier = modifier,
            shape = shape,
            colors = colors,
            border = border,
            elevation = elevation,
            content = content,
        )
    } else {
        Card(
            modifier = modifier,
            shape = shape,
            colors = colors,
            border = border,
            elevation = elevation,
            content = content,
        )
    }
}

/** Pill-shaped primary action button with a playful press squish. */
@Composable
fun PillButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    containerColor: Color = MaterialTheme.colorScheme.primary,
    contentColor: Color = MaterialTheme.colorScheme.onPrimary,
    leadingContent: (@Composable () -> Unit)? = null,
) {
    val reducedMotion = LocalReducedMotion.current
    val interactionSource = remember { MutableInteractionSource() }
    val pressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (pressed && !reducedMotion) 0.95f else 1f,
        animationSpec = spring(stiffness = 600f),
        label = "pillScale",
    )
    Button(
        onClick = onClick,
        modifier = modifier
            .graphicsLayer { scaleX = scale; scaleY = scale }
            .defaultMinSize(minHeight = 52.dp),
        enabled = enabled,
        shape = CircleShape,
        colors = ButtonDefaults.buttonColors(
            containerColor = containerColor,
            contentColor = contentColor,
        ),
        interactionSource = interactionSource,
    ) {
        if (leadingContent != null) {
            leadingContent()
        }
        Text(text = text, style = MaterialTheme.typography.labelLarge)
    }
}

/** Compact counter chip for XP / sun coins / water drops / streaks. */
@Composable
fun StatChip(
    emoji: String,
    value: String,
    modifier: Modifier = Modifier,
    contentDescription: String? = null,
) {
    Row(
        modifier = modifier
            .clip(CircleShape)
            .background(MaterialTheme.colorScheme.surface)
            .padding(horizontal = 12.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        Text(text = emoji, style = MaterialTheme.typography.bodyMedium)
        Text(
            text = value,
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.onSurface,
        )
    }
}

/** Reveals [text] character by character; instant when reduced motion is on. */
@Composable
fun TypewriterText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.bodyLarge,
    charDelayMs: Long = 14,
) {
    val reducedMotion = LocalReducedMotion.current
    var visibleChars by remember(text) { mutableStateOf(if (reducedMotion) text.length else 0) }
    LaunchedEffect(text) {
        if (!reducedMotion) {
            visibleChars = 0
            while (visibleChars < text.length) {
                delay(charDelayMs)
                visibleChars++
            }
        }
    }
    Box(modifier) {
        // Invisible full text reserves layout space so the bubble doesn't grow while typing.
        Text(text = text, style = style, color = Color.Transparent)
        Text(
            text = text.take(visibleChars),
            style = style,
            color = MaterialTheme.colorScheme.onSurface,
        )
    }
}

/** Soft shimmering placeholder used instead of spinners. */
@Composable
fun SkeletonBlock(
    modifier: Modifier = Modifier,
    cornerRadius: Int = 16,
) {
    val reducedMotion = LocalReducedMotion.current
    val alpha: Float = if (reducedMotion) {
        0.5f
    } else {
        val transition = androidx.compose.animation.core.rememberInfiniteTransition(label = "skeleton")
        val animated by transition.animateFloat(
            initialValue = 0.35f,
            targetValue = 0.65f,
            animationSpec = androidx.compose.animation.core.infiniteRepeatable(
                animation = androidx.compose.animation.core.tween(800),
                repeatMode = androidx.compose.animation.core.RepeatMode.Reverse,
            ),
            label = "skeletonAlpha",
        )
        animated
    }
    Box(
        modifier
            .height(20.dp)
            .fillMaxWidth()
            .clip(RoundedCornerShape(cornerRadius.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHighest.copy(alpha = alpha)),
    )
}

/** Vertical XP progress bar with rounded ends. */
@Composable
fun XpProgressBar(
    progress: Float,
    modifier: Modifier = Modifier,
) {
    Column(modifier) {
        Box(
            Modifier
                .fillMaxWidth()
                .height(10.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHighest),
        ) {
            Box(
                Modifier
                    .fillMaxWidth(progress.coerceIn(0f, 1f))
                    .height(10.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary),
            )
        }
    }
}
