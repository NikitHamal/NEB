package com.neb.ians.ui.screens.canvas

import androidx.compose.runtime.Immutable
import kotlin.math.abs

const val CanvasCardWidth = 340f
const val CanvasCardFallbackHeight = 420f
const val CanvasCardMaxBodyHeight = 340f
const val CanvasGapX = 48f
const val CanvasGapY = 56f

@Immutable
data class CanvasBounds(
    val left: Float,
    val top: Float,
    val width: Float,
    val height: Float
) {
    val right: Float get() = left + width
    val bottom: Float get() = top + height
    val centerX: Float get() = left + width / 2f
    val centerY: Float get() = top + height / 2f
}

enum class CanvasSide { Top, Bottom, Left, Right }

@Immutable
data class CanvasAnchor(val x: Float, val y: Float, val side: CanvasSide)

fun boundsOf(node: CanvasNode, heights: Map<String, Float>): CanvasBounds = CanvasBounds(
    left = node.x,
    top = node.y,
    width = CanvasCardWidth,
    height = heights[node.id] ?: CanvasCardFallbackHeight
)

fun CanvasBounds.anchor(side: CanvasSide): CanvasAnchor = when (side) {
    CanvasSide.Top -> CanvasAnchor(centerX, top, side)
    CanvasSide.Bottom -> CanvasAnchor(centerX, bottom, side)
    CanvasSide.Left -> CanvasAnchor(left, centerY, side)
    CanvasSide.Right -> CanvasAnchor(right, centerY, side)
}

fun CanvasSide.opposite(): CanvasSide = when (this) {
    CanvasSide.Top -> CanvasSide.Bottom
    CanvasSide.Bottom -> CanvasSide.Top
    CanvasSide.Left -> CanvasSide.Right
    CanvasSide.Right -> CanvasSide.Left
}

fun routeSides(from: CanvasBounds, to: CanvasBounds): Pair<CanvasSide, CanvasSide> {
    val dx = to.centerX - from.centerX
    val dy = to.centerY - from.centerY
    val spanX = from.width + to.width
    val spanY = from.height + to.height
    val horizontal = abs(dx) * spanY >= abs(dy) * spanX
    val side = when {
        horizontal && dx >= 0f -> CanvasSide.Right
        horizontal -> CanvasSide.Left
        dy >= 0f -> CanvasSide.Bottom
        else -> CanvasSide.Top
    }
    return side to side.opposite()
}

fun childOrigin(
    parent: CanvasBounds,
    direction: String,
    siblingIndex: Int
): Pair<Float, Float> = when (direction.lowercase()) {
    "right" -> parent.right + CanvasGapX to parent.top + siblingIndex * (CanvasGapY + 24f)
    "left" -> parent.left - CanvasCardWidth - CanvasGapX to parent.top + siblingIndex * (CanvasGapY + 24f)
    "top" -> parent.left + siblingIndex * (CanvasCardWidth + CanvasGapX) to
        parent.top - CanvasCardFallbackHeight - CanvasGapY
    else -> parent.left + siblingIndex * (CanvasCardWidth + CanvasGapX) to parent.bottom + CanvasGapY
}
