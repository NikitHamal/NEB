package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiAnalyticsHeatCell
import kotlin.math.max

/**
 * Vertical bars, one per value. [selected] draws in the brand primary, the rest in a tonal
 * wash of it; a tap reports the bar under the finger. No gradient, no shadow.
 */
@Composable
internal fun BarChart(
    values: List<Int>,
    modifier: Modifier = Modifier,
    selected: Int? = null,
    onSelect: ((Int) -> Unit)? = null,
    height: Dp = 132.dp,
    gap: Dp = 3.dp,
    description: String = "Bar chart"
) {
    val cs = MaterialTheme.colorScheme
    val primary = cs.primary
    val wash = cs.primary.copy(alpha = 0.32f)
    val grid = cs.outlineVariant
    val empty = cs.surfaceContainerHighest
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(height)
            .semantics { contentDescription = description }
            .pointerInput(values, onSelect) {
                if (onSelect != null && values.isNotEmpty()) {
                    detectTapGestures { p ->
                        val slot = size.width / values.size.toFloat()
                        onSelect((p.x / slot).toInt().coerceIn(0, values.lastIndex))
                    }
                }
            }
    ) {
        if (values.isEmpty()) return@Canvas
        val gapPx = gap.toPx()
        val slot = size.width / values.size
        val barW = (slot - gapPx).coerceAtLeast(1.5f)
        val peak = max(values.max(), 1)
        val usable = size.height - 2.dp.toPx()
        val radius = CornerRadius(minOf(barW / 2f, 4.dp.toPx()))
        // baseline and one mid line
        drawLine(grid, Offset(0f, size.height), Offset(size.width, size.height), strokeWidth = 1.dp.toPx())
        drawLine(grid.copy(alpha = 0.5f), Offset(0f, size.height / 2f), Offset(size.width, size.height / 2f), strokeWidth = 1.dp.toPx())
        values.forEachIndexed { i, v ->
            val x = i * slot + gapPx / 2f
            val h = if (v <= 0) 3.dp.toPx() else (v.toFloat() / peak * usable).coerceAtLeast(6.dp.toPx())
            val color = when {
                v <= 0 -> empty
                selected == null || selected == i -> primary
                else -> wash
            }
            drawRoundRect(color, Offset(x, size.height - h - 1.dp.toPx()), Size(barW, h), radius)
        }
    }
}

/** A thin trend line for a KPI tile. A flat run is drawn as a quiet baseline. */
@Composable
internal fun Sparkline(series: List<Int>, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val line = cs.primary
    val flat = cs.outlineVariant
    Canvas(modifier.width(64.dp).height(28.dp)) {
        if (series.size < 2) return@Canvas
        val peak = series.max()
        val low = series.min()
        val stroke = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round)
        if (peak == low) {
            val y = size.height - 3.dp.toPx()
            drawLine(if (peak == 0) flat else line, Offset(0f, y), Offset(size.width, y), strokeWidth = stroke.width, cap = StrokeCap.Round)
            return@Canvas
        }
        val pad = 3.dp.toPx()
        val stepX = size.width / (series.size - 1)
        val path = Path()
        series.forEachIndexed { i, v ->
            val y = pad + (1f - (v - low).toFloat() / (peak - low)) * (size.height - pad * 2)
            if (i == 0) path.moveTo(0f, y) else path.lineTo(i * stepX, y)
        }
        drawPath(path, line, style = stroke)
        val lastY = pad + (1f - (series.last() - low).toFloat() / (peak - low)) * (size.height - pad * 2)
        drawCircle(line, 3.dp.toPx(), Offset(size.width - 1.dp.toPx(), lastY))
    }
}

/**
 * The contribution calendar: [weeks] Monday-first columns of seven rounded cells. Level 0
 * is the empty tone, 1 to 4 step the brand primary up; -1 (a day to come) is not drawn.
 * A tap reports the cell index.
 */
@Composable
internal fun HeatmapGrid(
    cells: List<ApiAnalyticsHeatCell>,
    weeks: Int,
    selected: Int?,
    onSelect: (Int) -> Unit,
    modifier: Modifier = Modifier,
    cell: Dp = 18.dp,
    gap: Dp = 4.dp
) {
    val cs = MaterialTheme.colorScheme
    val tones = listOf(
        cs.surfaceContainerHighest,
        cs.primary.copy(alpha = 0.28f),
        cs.primary.copy(alpha = 0.52f),
        cs.primary.copy(alpha = 0.78f),
        cs.primary
    )
    val ring = cs.onSurface
    val rows = 7
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(cell * rows + gap * (rows - 1))
            .semantics { contentDescription = "Activity calendar" }
            .pointerInput(cells, weeks) {
                detectTapGestures { p ->
                    val slot = size.width / weeks.toFloat()
                    val rowH = size.height / rows.toFloat()
                    val col = (p.x / slot).toInt().coerceIn(0, weeks - 1)
                    val row = (p.y / rowH).toInt().coerceIn(0, rows - 1)
                    val index = col * rows + row
                    if (index in cells.indices && cells[index].level >= 0) onSelect(index)
                }
            }
    ) {
        if (cells.isEmpty()) return@Canvas
        val slot = size.width / weeks
        val rowH = size.height / rows
        val side = minOf(slot, rowH) - gap.toPx()
        val radius = CornerRadius(side * 0.32f)
        cells.forEachIndexed { i, c ->
            if (c.level < 0) return@forEachIndexed
            val col = i / rows
            val row = i % rows
            val x = col * slot + (slot - side) / 2f
            val y = row * rowH + (rowH - side) / 2f
            drawRoundRect(tones[c.level.coerceIn(0, 4)], Offset(x, y), Size(side, side), radius)
            if (selected == i) {
                drawRoundRect(ring, Offset(x, y), Size(side, side), radius, style = Stroke(2.dp.toPx()))
            }
        }
    }
}

/** A small stateful wrapper: which bar of a trend is picked, defaulting to the newest. */
@Composable
internal fun rememberPicked(count: Int, key: Any? = null): Pair<Int, (Int) -> Unit> {
    var picked by remember(key) { mutableIntStateOf(-1) }
    val index = if (picked in 0 until count) picked else count - 1
    return index to { i: Int -> picked = i }
}
