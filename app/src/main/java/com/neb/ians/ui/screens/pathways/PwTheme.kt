package com.neb.ians.ui.screens.pathways

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/** One flat colour family: container, its ink, and the strong version used for fills and bars. */
internal data class PwTone(val bg: Color, val fg: Color, val solid: Color, val onSolid: Color)

@Composable
internal fun pwTone(i: Int): PwTone {
    val c = MaterialTheme.colorScheme
    val dark = c.surface.luminance() < 0.5f
    val all = remember(c, dark) {
        listOf(
            PwTone(c.primaryContainer, c.onPrimaryContainer, c.primary, c.onPrimary),
            if (dark) PwTone(Color(0xFF5B2146), Color(0xFFFFD8EE), Color(0xFFFFB0DA), Color(0xFF3A0A2A))
            else PwTone(Color(0xFFFFD6EE), Color(0xFF3A0A2E), Color(0xFF4A0F3C), Color.White),
            if (dark) PwTone(Color(0xFF574500), Color(0xFFFFE08C), Color(0xFFFFD34D), Color(0xFF2F2400))
            else PwTone(Color(0xFFFFE08A), Color(0xFF332600), Color(0xFF332600), Color(0xFFFFE08A)),
            PwTone(c.secondaryContainer, c.onSecondaryContainer, c.secondary, c.onSecondary),
        )
    }
    return all[((i % 4) + 4) % 4]
}

internal val GROUP_LABEL = mapOf(
    "school" to "School", "tech" to "Engineering and IT", "sci" to "Science", "health" to "Health sciences", "biz" to "Business",
    "arts" to "Arts and media", "edu" to "Education", "law" to "Law", "ag" to "Agriculture", "gov" to "Government", "abroad" to "Abroad",
)

/** Small mono caption, the one typographic accent of the screen. */
@Composable
internal fun PwMono(text: String, modifier: Modifier = Modifier, color: Color = MaterialTheme.colorScheme.primary) {
    Text(text.uppercase(), modifier, color = color, fontFamily = FontFamily.Monospace, fontSize = 11.sp, letterSpacing = 0.8.sp, fontWeight = FontWeight.Medium, maxLines = 1)
}

/** Flat card. Clickable ones sink a little on press and stay rounded. */
@Composable
internal fun PwSurface(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.surfaceContainer,
    radius: Dp = 24.dp,
    border: BorderStroke? = null,
    onClick: (() -> Unit)? = null,
    content: @Composable () -> Unit,
) {
    val shape = RoundedCornerShape(radius)
    if (onClick == null) {
        Surface(modifier, shape = shape, color = color, border = border, content = content)
        return
    }
    val src = remember { MutableInteractionSource() }
    val pressed by src.collectIsPressedAsState()
    val s by animateFloatAsState(if (pressed) 0.975f else 1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMedium), label = "press")
    Surface(
        onClick = onClick, modifier = modifier.graphicsLayer { scaleX = s; scaleY = s }, shape = shape, color = color,
        border = border, interactionSource = src, content = content,
    )
}

@Composable
internal fun PwChip(label: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val c = MaterialTheme.colorScheme
    PwSurface(modifier, color = if (selected) c.primary else c.surfaceContainerHigh, radius = 20.dp, onClick = onClick) {
        Box(Modifier.height(40.dp), contentAlignment = Alignment.Center) {
            Text(
                label, Modifier.padding(horizontal = 18.dp), maxLines = 1, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold,
                color = if (selected) c.onPrimary else c.onSurface,
            )
        }
    }
}

@Composable
internal fun PwTile(text: String, tone: PwTone, size: Dp = 44.dp, solid: Boolean = false) {
    Box(
        Modifier.size(size).clip(RoundedCornerShape(size / 3)).drawBehind { drawRect(if (solid) tone.solid else tone.bg) },
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text, color = if (solid) tone.onSolid else tone.fg, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold,
            fontSize = if (text.length > 3) 10.sp else 13.sp, maxLines = 1,
        )
    }
}

@Composable
internal fun PwIconTile(icon: ImageVector, tone: PwTone, size: Dp = 44.dp, solid: Boolean = false) {
    Box(
        Modifier.size(size).clip(RoundedCornerShape(size / 3)).drawBehind { drawRect(if (solid) tone.solid else tone.bg) },
        contentAlignment = Alignment.Center,
    ) { Icon(icon, null, Modifier.size(size / 2), tint = if (solid) tone.onSolid else tone.fg) }
}

@Composable
internal fun PwIconButton(icon: ImageVector, description: String, onClick: () -> Unit, tint: Color = MaterialTheme.colorScheme.onSurface) {
    PwSurface(color = MaterialTheme.colorScheme.surfaceContainerHigh, radius = 22.dp, onClick = onClick) {
        Box(Modifier.size(44.dp), contentAlignment = Alignment.Center) { Icon(icon, description, Modifier.size(22.dp), tint = tint) }
    }
}

/** Meter drawn in the draw phase, grows once when it appears. */
@Composable
internal fun PwBar(fraction: Float, color: Color, track: Color, modifier: Modifier = Modifier.fillMaxWidth(), height: Dp = 6.dp) {
    val a = remember { Animatable(0f) }
    LaunchedEffect(fraction) { a.animateTo(fraction.coerceIn(0f, 1f), tween(650, easing = FastOutSlowInEasing)) }
    Box(
        modifier.height(height).clip(RoundedCornerShape(height / 2)).drawBehind {
            drawRect(track)
            drawRect(color, size = Size(size.width * a.value, size.height))
        },
    )
}
