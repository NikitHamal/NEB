package com.neb.ians.ui.components

import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.layout
import androidx.compose.ui.unit.Constraints
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/** Inner start padding of every ghost action pill (like, reply, comments). */
val NebGhostPillInset: Dp = 12.dp

/**
 * RULE (docs/M3X_DESIGN_SYSTEM.md, "Post and comment rows"): the first icon of a ghost action row must sit exactly
 * under the left edge of the text above it, not 12dp inside it. Ghost pills keep a 12dp inner padding for a
 * 40dp+ touch target, so the row is pulled left by that amount and widened by the same amount, which leaves the
 * right edge of the row where the content ends. Use it on the Row that holds the pills; never hand-roll offsets.
 */
fun Modifier.nebGhostRowStart(inset: Dp = NebGhostPillInset): Modifier = this.layout { measurable, constraints ->
    val extra = inset.roundToPx()
    val max = if (constraints.hasBoundedWidth) constraints.maxWidth + extra else Constraints.Infinity
    val min = if (constraints.hasBoundedWidth && constraints.minWidth > 0) constraints.minWidth + extra else 0
    val p = measurable.measure(constraints.copy(minWidth = min, maxWidth = max))
    layout(constraints.constrainWidth(p.width - extra), p.height) { p.placeRelative(-extra, 0) }
}
