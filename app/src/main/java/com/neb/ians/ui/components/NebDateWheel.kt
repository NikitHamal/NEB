package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import java.util.Calendar
import kotlin.math.abs

// ---------------------------------------------------------------------------
// A snapping three-column date wheel. The platform dialog is a modal that lands
// on top of the journey and breaks its rhythm; a wheel lives inside the step,
// carries the palette, and gives a birthday the one thing a form field cannot —
// the feel of turning to a date.
// ---------------------------------------------------------------------------

private val MONTH_NAMES = listOf(
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
)

/** Days in [month] (1..12) of [year], via Calendar because java.time is out of reach at minSdk 24. */
fun daysInMonth(year: Int, month: Int): Int {
    val calendar = Calendar.getInstance()
    calendar.set(Calendar.YEAR, year)
    calendar.set(Calendar.MONTH, month - 1)
    calendar.set(Calendar.DAY_OF_MONTH, 1)
    return calendar.getActualMaximum(Calendar.DAY_OF_MONTH)
}

fun formatIsoDate(year: Int, month: Int, day: Int): String =
    "%04d-%02d-%02d".format(year, month, day)

/** Parses `yyyy-MM-dd` back into a triple, or null if it is blank or malformed. */
fun parseIsoDate(value: String): Triple<Int, Int, Int>? {
    val parts = value.split("-")
    if (parts.size != 3) return null
    val year = parts[0].toIntOrNull() ?: return null
    val month = parts[1].toIntOrNull() ?: return null
    val day = parts[2].toIntOrNull() ?: return null
    if (month !in 1..12 || day !in 1..31) return null
    return Triple(year, month, day)
}

@Composable
fun NebDateWheel(
    year: Int,
    month: Int,
    day: Int,
    onChange: (year: Int, month: Int, day: Int) -> Unit,
    modifier: Modifier = Modifier,
    minYear: Int = 1940,
    maxYear: Int = Calendar.getInstance().get(Calendar.YEAR) - 5,
    itemHeight: Dp = 44.dp,
    visibleCount: Int = 5
) {
    val palette = LocalNebAuthPalette.current
    val years = remember(minYear, maxYear) { (maxYear downTo minYear).map { it.toString() } }
    val dayCount = daysInMonth(year, month)
    val days = remember(dayCount) { (1..dayCount).map { it.toString() } }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(itemHeight * visibleCount),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(itemHeight)
                .clip(RoundedCornerShape(14.dp))
                .background(palette.sapphireSoft)
        )

        Row(
            modifier = Modifier.fillMaxSize(),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            NebWheelColumn(
                items = days,
                selectedIndex = (day - 1).coerceIn(0, days.lastIndex),
                onSelected = { onChange(year, month, it + 1) },
                itemHeight = itemHeight,
                visibleCount = visibleCount,
                modifier = Modifier.weight(0.9f)
            )
            NebWheelColumn(
                items = MONTH_NAMES,
                selectedIndex = (month - 1).coerceIn(0, 11),
                onSelected = { newMonth ->
                    val maxDay = daysInMonth(year, newMonth + 1)
                    onChange(year, newMonth + 1, day.coerceAtMost(maxDay))
                },
                itemHeight = itemHeight,
                visibleCount = visibleCount,
                modifier = Modifier.weight(1.1f)
            )
            NebWheelColumn(
                items = years,
                selectedIndex = (maxYear - year).coerceIn(0, years.lastIndex),
                onSelected = { index ->
                    val newYear = maxYear - index
                    val maxDay = daysInMonth(newYear, month)
                    onChange(newYear, month, day.coerceAtMost(maxDay))
                },
                itemHeight = itemHeight,
                visibleCount = visibleCount,
                modifier = Modifier.weight(1.3f)
            )
        }
    }
}

@Composable
private fun NebWheelColumn(
    items: List<String>,
    selectedIndex: Int,
    onSelected: (Int) -> Unit,
    itemHeight: Dp,
    visibleCount: Int,
    modifier: Modifier = Modifier
) {
    val palette = LocalNebAuthPalette.current
    val tactile = rememberTactileFeedback()
    val state = rememberLazyListState(initialFirstVisibleItemIndex = selectedIndex)
    val currentSelected by rememberUpdatedState(selectedIndex)
    val flingBehavior = rememberSnapFlingBehavior(lazyListState = state)
    val half = visibleCount / 2

    val centeredIndex by remember(state, items.size) {
        derivedStateOf {
            val layout = state.layoutInfo
            val viewportCenter = (layout.viewportStartOffset + layout.viewportEndOffset) / 2f
            layout.visibleItemsInfo
                .minByOrNull { abs((it.offset + it.size / 2f) - viewportCenter) }
                ?.index
                ?.coerceIn(0, items.lastIndex)
                ?: 0
        }
    }

    LaunchedEffect(state, items.size) {
        snapshotFlow { state.isScrollInProgress to centeredIndex }
            .collect { (scrolling, index) ->
                if (!scrolling && index != currentSelected) {
                    tactile.perform(TactileType.SelectionChange)
                    onSelected(index)
                }
            }
    }

    LaunchedEffect(selectedIndex) {
        if (!state.isScrollInProgress && state.firstVisibleItemIndex != selectedIndex) {
            state.scrollToItem(selectedIndex)
        }
    }

    LazyColumn(
        state = state,
        flingBehavior = flingBehavior,
        contentPadding = PaddingValues(vertical = itemHeight * half),
        modifier = modifier.fillMaxSize()
    ) {
        items(items.size) { index ->
            val distance = abs(index - centeredIndex).toFloat()
            val fade = (1f - distance / (half + 1f)).coerceIn(0.18f, 1f)
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(itemHeight)
                    .graphicsLayer {
                        alpha = fade
                        val scale = 0.82f + fade * 0.18f
                        scaleX = scale
                        scaleY = scale
                    },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = items[index],
                    style = NebAuthType.Title.copy(
                        fontSize = 17.sp,
                        fontWeight = if (distance < 0.5f) FontWeight.SemiBold else FontWeight.Medium
                    ),
                    color = if (distance < 0.5f) palette.sapphire else palette.inkMuted,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 2.dp)
                )
            }
        }
    }
}
