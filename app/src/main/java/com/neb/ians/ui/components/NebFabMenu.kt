@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.theme.NebAccent
import com.neb.ians.ui.theme.nebAnimationsReduced
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Immutable
data class NebFabAction(
    val label: String,
    val icon: ImageVector,
    val onClick: () -> Unit,
    val accent: NebAccent? = null,
    val destructive: Boolean = false,
    val testTag: String? = null
)

/** One silhouette per row, so three actions read as three choices. */
private val TileShapes = listOf(NebGlyphShapes.Sunny, NebGlyphShapes.Clover, NebGlyphShapes.Cookie)

/**
 * Create menu: [label pill][shaped glyph tile] rows above the create button.
 *
 * Built to be cheap. Each row owns one Animatable that is read only inside graphicsLayer
 * blocks (draw phase), so opening the menu recomposes nothing per frame and re-lays out
 * nothing: the rows are composed once at full size and then only moved, scaled and faded
 * on the render thread. No blur, no animated gap, no AnimatedVisibility per row.
 */
@Composable
fun NebFabMenu(
    actions: List<NebFabAction>,
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    spacing: Dp = 14.dp,
    anchor: @Composable () -> Unit
) {
    Column(modifier = modifier, horizontalAlignment = Alignment.End) {
        NebFabMenuItems(
            actions = actions,
            expanded = expanded,
            onDismissRequest = onDismissRequest,
            bottomGap = spacing
        )
        anchor()
    }
}

@Composable
fun NebFabMenuItems(
    actions: List<NebFabAction>,
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier,
    itemSpacing: Dp = 10.dp,
    bottomGap: Dp = 0.dp
) {
    if (actions.isEmpty()) return
    val reduced = nebAnimationsReduced()
    val progress = remember(actions.size) { List(actions.size) { Animatable(0f) } }
    var shown by remember { mutableStateOf(false) }

    LaunchedEffect(expanded, reduced) {
        if (expanded) {
            shown = true
            coroutineScope {
                // closest row to the button first, then upward
                actions.indices.reversed().forEachIndexed { step, i ->
                    launch {
                        if (reduced) {
                            progress[i].snapTo(1f)
                        } else {
                            delay(step * 32L)
                            progress[i].animateTo(1f, spring(dampingRatio = 0.62f, stiffness = 520f))
                        }
                    }
                }
            }
        } else if (shown) {
            coroutineScope {
                actions.indices.forEachIndexed { step, i ->
                    launch {
                        if (reduced) {
                            progress[i].snapTo(0f)
                        } else {
                            delay(step * 18L)
                            progress[i].animateTo(0f, tween(140))
                        }
                    }
                }
            }
            shown = false
        }
    }

    if (!shown) return
    Column(
        modifier = modifier.padding(bottom = bottomGap, end = 4.dp),
        horizontalAlignment = Alignment.End,
        verticalArrangement = Arrangement.spacedBy(itemSpacing)
    ) {
        actions.forEachIndexed { index, action ->
            NebFabMenuRow(action, index, progress[index], onDismissRequest)
        }
    }
}

@Composable
private fun NebFabMenuRow(
    action: NebFabAction,
    index: Int,
    progress: Animatable<Float, *>,
    onDismissRequest: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val container = if (action.destructive) scheme.errorContainer else scheme.secondaryContainer
    val ink = if (action.destructive) scheme.onErrorContainer else scheme.onSecondaryContainer
    val tile = nebShape(TileShapes[index % TileShapes.size])

    Row(
        modifier = Modifier
            .then(action.testTag?.let { Modifier.testTag(it) } ?: Modifier)
            .graphicsLayer {
                val v = progress.value
                alpha = v.coerceIn(0f, 1f)
                val s = 0.55f + 0.45f * v
                scaleX = s
                scaleY = s
                translationY = (1f - v) * 36.dp.toPx()
                transformOrigin = TransformOrigin(1f, 1f)
            }
            .nebPressable(scale = 0.96f) {
                onDismissRequest()
                action.onClick()
            },
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Box(
            modifier = Modifier
                .heightIn(min = 40.dp)
                .clip(RoundedCornerShape(20.dp))
                .background(container)
                .padding(horizontal = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = action.label,
                style = MaterialTheme.typography.labelLargeEmphasized.copy(fontSize = 13.sp),
                color = ink,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        Box(
            modifier = Modifier
                .size(44.dp)
                .graphicsLayer { rotationZ = (1f - progress.value) * -70f }
                .clip(tile)
                .background(container),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = action.icon,
                contentDescription = null,
                tint = ink,
                modifier = Modifier
                    .size(22.dp)
                    .graphicsLayer { rotationZ = (1f - progress.value) * 70f }
            )
        }
    }
}

/** Neutral dim behind the open menu, drawn in the draw phase; no blur of the page. */
@Composable
fun NebFabMenuScrim(
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    modifier: Modifier = Modifier
) {
    val dark = MaterialTheme.colorScheme.surface.let { 0.299f * it.red + 0.587f * it.green + 0.114f * it.blue < 0.5f }
    val level by animateFloatAsState(
        targetValue = if (expanded) 1f else 0f,
        animationSpec = tween(180),
        label = "fab_scrim"
    )
    val visible by remember { derivedStateOf { level > 0.001f } }
    if (!expanded && !visible) return
    val peak = if (dark) 0.62f else 0.46f
    Box(
        modifier = modifier
            .fillMaxSize()
            .drawBehind { drawRect(Color.Black, alpha = peak * level) }
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onDismissRequest
            )
    )
}
