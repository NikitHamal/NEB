@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInParent
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.layout.height
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
// Switching between sets of the same thing: a library's shelves, a profile's
// posts and replies, a notification filter.
//
// Concept tabs (NEBians-Search.html): bare label, a tonal count pill, one 3dp
// primary line under the open tab that slides, and a hairline under the row.
// No container around a tab, nothing to squeeze: the row scrolls sideways.
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
    contentPadding: PaddingValues = PaddingValues(horizontal = 12.dp)
) {
    if (tabs.isEmpty()) return

    val scheme = MaterialTheme.colorScheme
    val lineColor = accent?.resolve() ?: scheme.primary
    val hairline = scheme.outlineVariant.copy(alpha = 0.6f)
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
            .drawBehind {
                val h = 1.dp.toPx()
                drawRect(hairline, topLeft = Offset(0f, size.height - h), size = Size(size.width, h))
            }
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .nebHorizontalScroll(scrollState)
                .padding(contentPadding)
        ) {
            Spacer(
                modifier = Modifier
                    .matchParentSize()
                    .drawBehind {
                        val inset = 14.dp.toPx()
                        val width = span.value - inset * 2
                        if (width <= 0f) return@drawBehind
                        val thick = 3.dp.toPx()
                        val r = CornerRadius(thick)
                        drawRoundRect(
                            color = lineColor,
                            topLeft = Offset(travel.value + inset, size.height - thick),
                            size = Size(width, thick + r.y),
                            cornerRadius = r
                        )
                    }
            )
            Row(
                horizontalArrangement = Arrangement.spacedBy(2.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                tabs.forEachIndexed { index, tab ->
                    NebRailItem(
                        tab = tab,
                        selected = index == selectedIndex,
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
}

@Composable
private fun NebRailItem(
    tab: NebRailTab,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val ink by animateColorAsState(
        targetValue = if (selected) scheme.onSurface else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "rail_content"
    )
    val pillBg by animateColorAsState(
        targetValue = if (selected) scheme.primaryContainer else scheme.surfaceContainerHigh,
        animationSpec = nebEffectsSpec(),
        label = "rail_pill"
    )
    val pillInk by animateColorAsState(
        targetValue = if (selected) scheme.onPrimaryContainer else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "rail_pill_ink"
    )

    Row(
        modifier = modifier
            .height(44.dp)
            .clip(RoundedCornerShape(topStart = 14.dp, topEnd = 14.dp))
            .nebPressable(scale = 0.97f, tactile = TactileType.SelectionChange, onClick = onClick)
            .padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        if (tab.icon != null) {
            Icon(imageVector = tab.icon, contentDescription = null, tint = ink, modifier = Modifier.size(18.dp))
        }
        Text(
            text = tab.label,
            style = MaterialTheme.typography.labelLarge,
            fontWeight = FontWeight.SemiBold,
            color = ink,
            maxLines = 1,
            softWrap = false
        )
        if (tab.count > 0 || tab.showZero) {
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(9.dp))
                    .background(pillBg)
                    .padding(horizontal = 7.dp, vertical = 1.dp)
            ) {
                Text(
                    text = tab.count.toString(),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = pillInk,
                    maxLines = 1
                )
            }
        }
    }
}
