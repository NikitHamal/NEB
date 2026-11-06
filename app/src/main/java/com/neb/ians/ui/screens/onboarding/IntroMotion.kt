package com.neb.ians.ui.screens.onboarding

import com.neb.ians.ui.theme.nebAnimationsReduced
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.text.TextStyle
import androidx.compose.material3.Text
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.graphics.shapes.RoundedPolygon
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.nebShape
import com.neb.ians.ui.theme.nebSlowSpatialSpec
import kotlinx.coroutines.delay

/**
 * Brings its content in with a spring once [active] is true, after a stagger of
 * [index] steps, and resets it when the page is left so coming back plays it again.
 */
@Composable
internal fun Reveal(
    active: Boolean,
    index: Int,
    modifier: Modifier = Modifier,
    rise: Dp = 28.dp,
    fromX: Dp = 0.dp,
    content: @Composable BoxScope.() -> Unit
) {
    val t = remember { Animatable(0f) }
    val spec = nebSlowSpatialSpec<Float>()
    val reduced = nebAnimationsReduced()
    LaunchedEffect(active) {
        if (active) {
            if (reduced) {
                t.snapTo(1f)
                return@LaunchedEffect
            }
            delay(120L + index * 80L)
            t.animateTo(1f, spec)
        } else {
            t.snapTo(0f)
        }
    }
    Box(
        modifier = modifier.graphicsLayer {
            val v = t.value
            alpha = v.coerceIn(0f, 1f)
            translationY = (1f - v) * rise.toPx()
            translationX = (1f - v) * fromX.toPx()
            val s = 0.9f + 0.1f * v
            scaleX = s
            scaleY = s
        },
        content = content
    )
}

@Composable
internal fun isDarkSurface(): Boolean = MaterialTheme.colorScheme.surface.luminance() < 0.5f

/** A white card with one hairline, like every raised surface on the site. No shadow. */
@Composable
internal fun IntroPanel(modifier: Modifier = Modifier, content: @Composable BoxScope.() -> Unit) {
    val shape = RoundedCornerShape(28.dp)
    Box(
        modifier = modifier
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape),
        content = content
    )
}

/** A tonal tile cut to one of the landing glyph silhouettes. */
@Composable
internal fun GlyphTile(
    shape: RoundedPolygon,
    tone: NebTone,
    size: Dp,
    modifier: Modifier = Modifier,
    content: @Composable BoxScope.() -> Unit
) {
    Box(
        modifier = modifier
            .size(size)
            .background(tone.container(isDarkSurface()), nebShape(shape)),
        contentAlignment = Alignment.Center,
        content = content
    )
}

/** Types [text] out once [active], like the landing hero's search box. */
@Composable
internal fun TypedText(text: String, active: Boolean, style: TextStyle, color: Color) {
    var shown by remember { mutableIntStateOf(0) }
    LaunchedEffect(active) {
        if (!active) {
            shown = 0
        } else {
            delay(520)
            for (i in 1..text.length) {
                shown = i
                delay(55)
            }
        }
    }
    Text(text = text.take(shown), style = style, color = color, maxLines = 1)
}
