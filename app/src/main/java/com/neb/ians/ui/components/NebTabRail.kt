@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInParent
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.toSize
import com.neb.ians.ui.theme.NebAccent
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.ui.theme.resolve
import com.neb.ians.util.TactileType
import kotlinx.coroutines.launch
import kotlin.math.max
import kotlin.math.roundToInt

// ---------------------------------------------------------------------------
// Switching between sets of the same thing: the library's shelves, a profile's
// posts and replies, a notification filter.
//
// Not a bar of connected buttons — that reads as one control the user is
// operating, and it squeezes four labels into a width that fits two. Not an
// underline either, which is the platform's tab and not ours. Here the resting
// state is bare text with nothing drawn around it, and only the answer carries
// a container.
//
// There is exactly one container and it slides. A tab never grows its own pill
// while another is still fading out, so the answer is only ever in one place,
// and the labels hold still while the selection travels between them.
// ---------------------------------------------------------------------------

@Immutable
data class NebRailTab(
    val label: String,
    val icon: ImageVector? = null,
    val count: Int = 0,
    val showZero: Boolean = false
)

@Composable
fun NebTabRail(
    tabs: List<NebRailTab>,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
    accent: NebAccent? = null,
    contentPadding: PaddingValues = PaddingValues(horizontal = 14.dp, vertical = 6.dp)
) {
    if (tabs.isEmpty()) return

    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    val accentColor = accent?.resolve()
    val indicatorFill = accentColor
        ?.copy(alpha = if (isDark) 0.17f else 0.10f)
        ?.compositeOver(scheme.surfaceContainerLow)
        ?: scheme.surfaceContainerHighest
    val indicatorEdge = accentColor?.copy(alpha = 0.34f) ?: scheme.outlineVariant

    val scrollState = rememberScrollState()
    val slots = remember(tabs.size) { mutableStateMapOf<Int, Rect>() }
    val slot = slots[selectedIndex]

    val travel = remember { Animatable(0f) }
    val span = remember { Animatable(0f) }
    val motion = nebSpatialSpec<Float>()

    LaunchedEffect(slot) {
        val target = slot ?: return@LaunchedEffect
        if (span.value == 0f) {
            travel.snapTo(target.left)
            span.snapTo(target.width)
        } else {
            launch { travel.animateTo(target.left, motion) }
            span.animateTo(target.width, motion)
        }
    }

    LaunchedEffect(slot, scrollState.viewportSize) {
        val target = slot ?: return@LaunchedEffect
        val viewport = scrollState.viewportSize
        if (viewport == 0) return@LaunchedEffect
        val margin = 28
        val start = target.left.roundToInt() - margin
        val end = target.right.roundToInt() + margin
        when {
            start < scrollState.value -> scrollState.animateScrollTo(max(0, start))
            end > scrollState.value + viewport -> scrollState.animateScrollTo(end - viewport)
        }
    }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(scrollState)
            .padding(contentPadding)
    ) {
        Spacer(
            modifier = Modifier
                .matchParentSize()
                .drawBehind {
                    val width = span.value
                    val height = slot?.height ?: 0f
                    if (width <= 0f || height <= 0f) return@drawBehind
                    val top = slot?.top ?: 0f
                    val corner = CornerRadius(height / 2f)
                    drawRoundRect(
                        color = indicatorFill,
                        topLeft = Offset(travel.value, top),
                        size = Size(width, height),
                        cornerRadius = corner
                    )
                    drawRoundRect(
                        color = indicatorEdge,
                        topLeft = Offset(travel.value, top),
                        size = Size(width, height),
                        cornerRadius = corner,
                        style = Stroke(width = 1.dp.toPx())
                    )
                }
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            tabs.forEachIndexed { index, tab ->
                NebRailItem(
                    tab = tab,
                    selected = index == selectedIndex,
                    accentColor = accentColor,
                    onClick = { onSelect(index) },
                    modifier = Modifier.onGloballyPositioned { coordinates ->
                        val bounds = Rect(
                            offset = coordinates.positionInParent(),
                            size = coordinates.size.toSize()
                        )
                        if (slots[index] != bounds) slots[index] = bounds
                    }
                )
            }
        }
    }
}

@Composable
private fun NebRailItem(
    tab: NebRailTab,
    selected: Boolean,
    accentColor: Color?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val content by animateColorAsState(
        targetValue = if (selected) accentColor ?: scheme.onSurface else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "rail_content"
    )

    Row(
        modifier = modifier
            .nebPressable(scale = 0.94f, tactile = TactileType.SelectionChange, onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(7.dp)
    ) {
        if (tab.icon != null) {
            Icon(
                imageVector = tab.icon,
                contentDescription = null,
                tint = content,
                modifier = Modifier.size(18.dp)
            )
        }
        Text(
            text = tab.label,
            style = MaterialTheme.typography.labelLargeEmphasized,
            color = content,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
        if (tab.count > 0 || tab.showZero) {
            Box(
                modifier = Modifier
                    .clip(CircleShape)
                    .background(content.copy(alpha = if (selected) 0.14f else 0.10f))
                    .padding(horizontal = 7.dp, vertical = 2.dp)
            ) {
                Text(
                    text = tab.count.toString(),
                    style = MaterialTheme.typography.labelSmall,
                    color = content
                )
            }
        }
    }
}
