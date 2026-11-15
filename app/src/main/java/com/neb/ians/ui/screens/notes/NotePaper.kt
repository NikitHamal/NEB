package com.neb.ians.ui.screens.notes

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

/** Flat page paper drawn under the blocks. Lines are a tint of the page ink, never a gradient or a shadow. */
object NotePaper {
    const val NONE = 0
    const val LINES = 1
    const val GRID = 2
    const val DOTS = 3
    val labels = listOf("Plain", "Lines", "Grid", "Dots")
}

fun Modifier.notePaper(kind: Int, ink: Color): Modifier = if (kind == NotePaper.NONE) this else drawBehind {
    val step = 28.dp.toPx()
    val tint = ink.copy(alpha = 0.10f)
    val w = size.width
    val h = size.height
    when (kind) {
        NotePaper.LINES -> {
            var y = step * 3
            while (y < h) { drawLine(tint, Offset(0f, y), Offset(w, y), strokeWidth = 1.dp.toPx()); y += step }
        }
        NotePaper.GRID -> {
            var y = step
            while (y < h) { drawLine(tint, Offset(0f, y), Offset(w, y), strokeWidth = 1.dp.toPx()); y += step }
            var x = step
            while (x < w) { drawLine(tint, Offset(x, 0f), Offset(x, h), strokeWidth = 1.dp.toPx()); x += step }
        }
        NotePaper.DOTS -> {
            val dot = ink.copy(alpha = 0.22f)
            var y = step
            while (y < h) {
                var x = step
                while (x < w) { drawCircle(dot, radius = 1.4.dp.toPx(), center = Offset(x, y)); x += step }
                y += step
            }
        }
    }
}

/** One row of four paper choices; the picked one is a tonal chip, the rest keep a hairline. */
@Composable
fun PaperPicker(current: Int, onPick: (Int) -> Unit) {
    val c = MaterialTheme.colorScheme
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        NotePaper.labels.forEachIndexed { index, label ->
            val on = index == current
            Surface(
                modifier = Modifier.weight(1f).height(44.dp).clickable { onPick(index) },
                shape = RoundedCornerShape(22.dp),
                color = if (on) c.secondaryContainer else c.surfaceContainerLowest,
                border = if (on) null else BorderStroke(1.dp, c.outlineVariant),
                tonalElevation = 0.dp, shadowElevation = 0.dp,
            ) {
                Box(Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                    Text(label, style = MaterialTheme.typography.labelLarge, color = if (on) c.onSecondaryContainer else c.onSurface)
                }
            }
        }
    }
}
