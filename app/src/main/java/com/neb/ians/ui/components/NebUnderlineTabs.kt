package com.neb.ians.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInParent
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.unit.toSize
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.util.TactileType
import kotlinx.coroutines.launch
import kotlin.math.max
import kotlin.math.roundToInt

// ---------------------------------------------------------------------------
// Underline tabs (search scopes only; every other tab row keeps NebTabRail).
//
// The Material 3 primary tab indicator: 3dp tall, top corners rounded, sitting
// flush on the hairline, exactly as wide as the label and count it belongs to.
// It slides between tabs; position and width live in Animatables read only in
// the draw phase, so a tab change recomposes nothing but the two labels.
// ---------------------------------------------------------------------------

private val IndicatorHeight = 3.dp
private val ItemPad = 14.dp

@Composable
fun NebUnderlineTabs(
    tabs: List<NebRailTab>,
    selectedIndex: Int,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    if (tabs.isEmpty()) return

    val scheme = MaterialTheme.colorScheme
    val lineColor = scheme.primary
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
                .padding(horizontal = 12.dp)
        ) {
            // Drawn behind the row; width is infinite inside a scroller, so it is
            // sized by matchParentSize and never by fillMaxWidth.
            val indicatorPath = remember { Path() }
            Spacer(
                modifier = Modifier
                    .matchParentSize()
                    .drawBehind {
                        val inset = ItemPad.toPx()
                        val width = span.value - inset * 2
                        if (width <= 0f) return@drawBehind
                        val h = IndicatorHeight.toPx()
                        val r = CornerRadius(h)
                        indicatorPath.rewind()
                        indicatorPath.addRoundRect(
                            RoundRect(
                                left = travel.value + inset,
                                top = size.height - h,
                                right = travel.value + inset + width,
                                bottom = size.height,
                                topLeftCornerRadius = r,
                                topRightCornerRadius = r,
                                bottomLeftCornerRadius = CornerRadius.Zero,
                                bottomRightCornerRadius = CornerRadius.Zero
                            )
                        )
                        drawPath(indicatorPath, lineColor)
                    }
            )
            Row(
                horizontalArrangement = Arrangement.spacedBy(2.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                tabs.forEachIndexed { index, tab ->
                    UnderlineTabItem(
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
private fun UnderlineTabItem(
    tab: NebRailTab,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val ink by animateColorAsState(
        targetValue = if (selected) scheme.onSurface else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "underline_ink"
    )
    val pillBg by animateColorAsState(
        targetValue = if (selected) scheme.primaryContainer else scheme.surfaceContainerHigh,
        animationSpec = nebEffectsSpec(),
        label = "underline_pill"
    )
    val pillInk by animateColorAsState(
        targetValue = if (selected) scheme.onPrimaryContainer else scheme.onSurfaceVariant,
        animationSpec = nebEffectsSpec(),
        label = "underline_pill_ink"
    )

    Row(
        modifier = modifier
            .height(44.dp)
            .clip(RoundedCornerShape(topStart = 14.dp, topEnd = 14.dp))
            .nebPressable(scale = 0.97f, tactile = TactileType.SelectionChange, onClick = onClick)
            .padding(horizontal = ItemPad),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
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
