package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlin.math.abs
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.max
import kotlin.math.sin

enum class CanvasTool { SELECT, PAN, PEN, HIGHLIGHTER, RECT, ELLIPSE, LINE, ARROW, TEXT, STICKY, ERASER }

internal val CANVAS_DRAW_COLORS = listOf("#1f1f1f", "#e53e3e", "#dd6b20", "#d69e2e", "#38a169", "#3182ce", "#5a67d8", "#ffffff")
internal val CANVAS_DRAW_WIDTHS = listOf(2f, 4f, 8f, 14f)
internal const val HIGHLIGHTER_WIDTH = 18f
internal const val HIGHLIGHTER_ALPHA = 0.38f

internal fun drawObjectId(): String = "o_" + System.currentTimeMillis() + "_" + (0..9999).random()

internal fun JsonObject.drawType(): String = str("type")

internal fun JsonObject.drawPoints(): List<Offset> = arr("points").mapNotNull {
    val o = it as? JsonObject ?: return@mapNotNull null
    Offset(o.num("x").toFloat(), o.num("y").toFloat())
}

internal fun buildStrokeObject(type: String, points: List<Offset>, color: String, width: Float): JsonObject =
    buildJsonObject {
        put("id", JsonPrimitive(drawObjectId()))
        put("type", JsonPrimitive(type))
        put("points", buildJsonArray {
            points.forEach { add(buildJsonObject {
                put("x", JsonPrimitive(it.x.toDouble()))
                put("y", JsonPrimitive(it.y.toDouble()))
            }) }
        })
        put("color", JsonPrimitive(color))
        put("lineWidth", JsonPrimitive(width.toDouble()))
    }

internal fun buildShapeObject(
    type: String, x1: Float, y1: Float, x2: Float, y2: Float, color: String, width: Float
): JsonObject = buildJsonObject {
    put("id", JsonPrimitive(drawObjectId()))
    put("type", JsonPrimitive(type))
    if (type == "line" || type == "arrow") {
        put("x1", JsonPrimitive(x1.toDouble()))
        put("y1", JsonPrimitive(y1.toDouble()))
        put("x2", JsonPrimitive(x2.toDouble()))
        put("y2", JsonPrimitive(y2.toDouble()))
        put("stroke", JsonPrimitive(color))
    } else {
        put("x", JsonPrimitive(minOf(x1, x2).toDouble()))
        put("y", JsonPrimitive(minOf(y1, y2).toDouble()))
        put("w", JsonPrimitive(abs(x2 - x1).toDouble()))
        put("h", JsonPrimitive(abs(y2 - y1).toDouble()))
        put("stroke", JsonPrimitive(color))
    }
    put("lineWidth", JsonPrimitive(width.toDouble()))
}

internal fun buildTextObject(tool: CanvasTool, x: Float, y: Float, text: String, color: String, bg: String): JsonObject =
    buildJsonObject {
        put("id", JsonPrimitive(drawObjectId()))
        put("type", JsonPrimitive(if (tool == CanvasTool.STICKY) "sticky" else "text"))
        put("x", JsonPrimitive(x.toDouble()))
        put("y", JsonPrimitive(y.toDouble()))
        if (tool == CanvasTool.STICKY) {
            put("w", JsonPrimitive(160.0))
            put("h", JsonPrimitive(120.0))
            put("bg", JsonPrimitive(bg))
        }
        put("text", JsonPrimitive(text))
        put("color", JsonPrimitive(color))
        put("fontSize", JsonPrimitive(18.0))
    }

internal fun drawObjectBounds(o: JsonObject): androidx.compose.ui.geometry.Rect? {
    return when (o.drawType()) {
        "pen", "highlighter", "marker" -> {
            val pts = o.drawPoints()
            if (pts.isEmpty()) null
            else {
                var l = pts[0].x; var t = pts[0].y; var r = l; var b = t
                pts.forEach { l = minOf(l, it.x); t = minOf(t, it.y); r = maxOf(r, it.x); b = maxOf(b, it.y) }
                androidx.compose.ui.geometry.Rect(l, t, r, b)
            }
        }
        "rect", "ellipse", "sticky", "image", "file" ->
            androidx.compose.ui.geometry.Rect(o.num("x").toFloat(), o.num("y").toFloat(), (o.num("x") + o.num("w")).toFloat(), (o.num("y") + o.num("h")).toFloat())
        "line", "arrow" -> {
            val x1 = o.num("x1").toFloat(); val y1 = o.num("y1").toFloat()
            val x2 = o.num("x2").toFloat(); val y2 = o.num("y2").toFloat()
            androidx.compose.ui.geometry.Rect(minOf(x1, x2), minOf(y1, y2), maxOf(x1, x2), maxOf(y1, y2))
        }
        "text" -> androidx.compose.ui.geometry.Rect(o.num("x").toFloat(), o.num("y").toFloat(), o.num("x").toFloat() + 200f, o.num("y").toFloat() + 40f)
        else -> null
    }
}

@Composable
fun CanvasDrawOverlay(
    tool: CanvasTool,
    objects: List<JsonObject>,
    colorHex: String,
    width: Float,
    scale: Float,
    viewX: Float,
    viewY: Float,
    density: Density,
    onCommit: (JsonObject) -> Unit,
    onEraseAt: (Offset) -> Unit,
    onTapAnnotate: (CanvasTool, Offset) -> Unit,
    modifier: Modifier = Modifier
) {
    val textMeasurer = rememberTextMeasurer()
    var previewPoints by remember(tool) { mutableStateOf<List<Offset>>(emptyList()) }
    var previewShape by remember(tool) { mutableStateOf<Pair<Offset, Offset>?>(null) }

    fun toWorld(px: Offset): Offset =
        Offset((px.x - viewX) / scale / density.density, (px.y - viewY) / scale / density.density)

    fun drawActive(): Boolean = tool != CanvasTool.SELECT && tool != CanvasTool.PAN

    Canvas(
        modifier = modifier.then(
            if (drawActive()) {
                Modifier.pointerInput(tool, scale, viewX, viewY, colorHex, width) {
                    detectDragGestures(
                        onDragStart = { offset ->
                            val world = toWorld(offset)
                            when (tool) {
                                CanvasTool.ERASER -> onEraseAt(world)
                                CanvasTool.TEXT, CanvasTool.STICKY -> onTapAnnotate(tool, world)
                                else -> {
                                    previewPoints = listOf(world)
                                    previewShape = world to world
                                }
                            }
                        },
                        onDrag = { change, _ ->
                            change.consume()
                            val world = toWorld(change.position)
                            when (tool) {
                                CanvasTool.ERASER -> onEraseAt(world)
                                CanvasTool.PEN, CanvasTool.HIGHLIGHTER -> previewPoints = previewPoints + world
                                else -> previewShape = previewShape?.let { it.first to world }
                            }
                        },
                        onDragEnd = {
                            when (tool) {
                                CanvasTool.PEN, CanvasTool.HIGHLIGHTER -> {
                                    if (previewPoints.size > 1) {
                                        onCommit(buildStrokeObject(
                                            if (tool == CanvasTool.HIGHLIGHTER) "highlighter" else "pen",
                                            previewPoints, colorHex, if (tool == CanvasTool.HIGHLIGHTER) HIGHLIGHTER_WIDTH else width
                                        ))
                                    }
                                    previewPoints = emptyList()
                                }
                                CanvasTool.RECT, CanvasTool.ELLIPSE, CanvasTool.LINE, CanvasTool.ARROW -> {
                                    val shape = previewShape
                                    if (shape != null) {
                                        val (a, b) = shape
                                        val dist = kotlin.math.hypot((b.x - a.x) * scale * density.density, (b.y - a.y) * scale * density.density)
                                        if (dist > 8f) {
                                            onCommit(buildShapeObject(
                                                tool.name.lowercase(), a.x, a.y, b.x, b.y, colorHex, width
                                            ))
                                        }
                                    }
                                    previewShape = null
                                }
                                else -> Unit
                            }
                        },
                        onDragCancel = {
                            previewPoints = emptyList()
                            previewShape = null
                        }
                    )
                }
            } else Modifier
        )
    ) {
        withTransform({
            translate(left = viewX, top = viewY)
            scale(scale, scale, Offset.Zero)
        }) {
            val d = density.density
            objects.forEach { o -> drawDrawObject(o, textMeasurer, d) }
            if (previewPoints.size > 1) {
                val path = Path().apply {
                    moveTo(previewPoints[0].x * d, previewPoints[0].y * d)
                    previewPoints.drop(1).forEach { lineTo(it.x * d, it.y * d) }
                }
                val isHl = tool == CanvasTool.HIGHLIGHTER
                drawPath(
                    path,
                    colorHex.toComposeColor(Color.Black),
                    style = Stroke((if (isHl) HIGHLIGHTER_WIDTH else width) * d, cap = StrokeCap.Round, join = StrokeJoin.Round),
                    alpha = if (isHl) HIGHLIGHTER_ALPHA else 1f
                )
            }
            previewShape?.let { (a, b) ->
                if (tool == CanvasTool.RECT || tool == CanvasTool.ELLIPSE || tool == CanvasTool.LINE || tool == CanvasTool.ARROW) {
                    drawPreviewShape(tool.name.lowercase(), a * d, b * d, colorHex.toComposeColor(Color.Black), width * d)
                }
            }
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawDrawObject(
    o: JsonObject,
    textMeasurer: androidx.compose.ui.text.TextMeasurer,
    d: Float
) {
    val type = o.drawType()
    val stroke = (o.str("stroke").ifBlank { o.str("color") }).toComposeColor(Color.Black)
    val w = o.num("lineWidth").toFloat().takeIf { it > 0 } ?: 4f
    when (type) {
        "pen", "marker" -> {
            val pts = o.drawPoints()
            if (pts.size > 1) {
                drawPath(
                    Path().apply {
                        moveTo(pts[0].x * d, pts[0].y * d)
                        pts.drop(1).forEach { lineTo(it.x * d, it.y * d) }
                    },
                    stroke, style = Stroke(w * d, cap = StrokeCap.Round, join = StrokeJoin.Round)
                )
            }
        }
        "highlighter" -> {
            val pts = o.drawPoints()
            if (pts.size > 1) {
                drawPath(
                    Path().apply {
                        moveTo(pts[0].x * d, pts[0].y * d)
                        pts.drop(1).forEach { lineTo(it.x * d, it.y * d) }
                    },
                    stroke, style = Stroke(w * d, cap = StrokeCap.Round, join = StrokeJoin.Round), alpha = HIGHLIGHTER_ALPHA
                )
            }
        }
        "rect" -> drawRect(stroke, Offset(o.num("x").toFloat() * d, o.num("y").toFloat() * d),
            androidx.compose.ui.geometry.Size(o.num("w").toFloat() * d, o.num("h").toFloat() * d),
            style = Stroke(w * d, cap = StrokeCap.Round))
        "ellipse" -> drawOval(stroke, Offset(o.num("x").toFloat() * d, o.num("y").toFloat() * d),
            androidx.compose.ui.geometry.Size(o.num("w").toFloat() * d, o.num("h").toFloat() * d),
            style = Stroke(w * d, cap = StrokeCap.Round))
        "line" -> drawLine(stroke, Offset(o.num("x1").toFloat() * d, o.num("y1").toFloat() * d),
            Offset(o.num("x2").toFloat() * d, o.num("y2").toFloat() * d), strokeWidth = w * d, cap = StrokeCap.Round)
        "arrow" -> {
            val a = Offset(o.num("x1").toFloat() * d, o.num("y1").toFloat() * d)
            val b = Offset(o.num("x2").toFloat() * d, o.num("y2").toFloat() * d)
            drawLine(stroke, a, b, strokeWidth = w * d, cap = StrokeCap.Round)
            drawArrowHead(a, b, stroke, w * d)
        }
        "text" -> {
            val text = o.str("text")
            if (text.isNotBlank()) {
                val layout = textMeasurer.measure(
                    text, TextStyle(color = o.str("color").toComposeColor(Color.Black), fontSize = 18.sp)
                )
                drawText(layout, topLeft = Offset(o.num("x").toFloat() * d, o.num("y").toFloat() * d))
            }
        }
        "sticky" -> {
            val x = o.num("x").toFloat() * d; val y = o.num("y").toFloat() * d
            val ww = (o.num("w").toFloat().takeIf { it > 0 } ?: 160f) * d
            val hh = (o.num("h").toFloat().takeIf { it > 0 } ?: 120f) * d
            drawRoundRect(o.str("bg").toComposeColor(Color(0xFFFFF9C4)),
                Offset(x, y), androidx.compose.ui.geometry.Size(ww, hh), androidx.compose.ui.geometry.CornerRadius(8f * d))
            val text = o.str("text")
            if (text.isNotBlank()) {
                val layout = textMeasurer.measure(
                    text,
                    TextStyle(color = o.str("color").toComposeColor(Color.Black), fontSize = 14.sp),
                    constraints = androidx.compose.ui.unit.Constraints(
                        maxWidth = (ww - 16f * d).toInt().coerceAtLeast(40)
                    )
                )
                drawText(layout, topLeft = Offset(x + 8f * d, y + 8f * d))
            }
        }
        "image", "file" -> {
            val x = o.num("x").toFloat() * d; val y = o.num("y").toFloat() * d
            val ww = (o.num("w").toFloat().takeIf { it > 0 } ?: 220f) * d
            val hh = (o.num("h").toFloat().takeIf { it > 0 } ?: 64f) * d
            drawRoundRect(Color.Gray.copy(alpha = 0.25f), Offset(x, y),
                androidx.compose.ui.geometry.Size(ww, hh), androidx.compose.ui.geometry.CornerRadius(10f * d))
            val label = o.str("title").ifBlank { type }
            val layout = textMeasurer.measure(label, TextStyle(color = Color.DarkGray, fontSize = 13.sp))
            drawText(layout, topLeft = Offset(x + 10f * d, y + 10f * d))
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawPreviewShape(
    type: String, a: Offset, b: Offset, color: Color, widthPx: Float
) {
    when (type) {
        "rect" -> drawRect(color, Offset(minOf(a.x, b.x), minOf(a.y, b.y)),
            androidx.compose.ui.geometry.Size(abs(b.x - a.x), abs(b.y - a.y)), style = Stroke(widthPx, cap = StrokeCap.Round))
        "ellipse" -> drawOval(color, Offset(minOf(a.x, b.x), minOf(a.y, b.y)),
            androidx.compose.ui.geometry.Size(abs(b.x - a.x), abs(b.y - a.y)), style = Stroke(widthPx, cap = StrokeCap.Round))
        "line" -> drawLine(color, a, b, strokeWidth = widthPx, cap = StrokeCap.Round)
        "arrow" -> {
            drawLine(color, a, b, strokeWidth = widthPx, cap = StrokeCap.Round)
            drawArrowHead(a, b, color, widthPx)
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawArrowHead(
    a: Offset, b: Offset, color: Color, widthPx: Float
) {
    val angle = atan2(b.y - a.y, b.x - a.x)
    val h = max(12f, widthPx * 4f)
    val a1 = angle + Math.PI.toFloat() * 0.85f
    val a2 = angle - Math.PI.toFloat() * 0.85f
    drawLine(color, b, Offset(b.x + h * cos(a1), b.y + h * sin(a1)), strokeWidth = widthPx, cap = StrokeCap.Round)
    drawLine(color, b, Offset(b.x + h * cos(a2), b.y + h * sin(a2)), strokeWidth = widthPx, cap = StrokeCap.Round)
}

@Composable
fun CanvasPaintDock(
    colorHex: String,
    onColor: (String) -> Unit,
    width: Float,
    onWidth: (Float) -> Unit,
    tool: CanvasTool,
    modifier: Modifier = Modifier
) {
    if (tool != CanvasTool.PEN && tool != CanvasTool.HIGHLIGHTER && tool != CanvasTool.RECT &&
        tool != CanvasTool.ELLIPSE && tool != CanvasTool.LINE && tool != CanvasTool.ARROW &&
        tool != CanvasTool.TEXT && tool != CanvasTool.STICKY
    ) return
    Column(
        modifier = modifier
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(20.dp))
            .padding(10.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CANVAS_DRAW_COLORS.forEach { hex ->
            val selected = hex.equals(colorHex, ignoreCase = true)
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clip(CircleShape)
                    .background(hex.toComposeColor(Color.Black))
                    .then(if (selected) Modifier.border(2.dp, MaterialTheme.colorScheme.primary, CircleShape) else Modifier)
                    .clickable { onColor(hex) }
            )
        }
        if (tool != CanvasTool.HIGHLIGHTER && tool != CanvasTool.TEXT && tool != CanvasTool.STICKY) {
            Spacer(Modifier.height(2.dp))
            CANVAS_DRAW_WIDTHS.forEach { w ->
                val selected = w == width
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(26.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (selected) MaterialTheme.colorScheme.primaryContainer else Color.Transparent)
                        .clickable { onWidth(w) },
                    contentAlignment = Alignment.Center
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(0.7f)
                            .height(w.dp.coerceAtMost(14.dp))
                            .background(
                                if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                                CircleShape
                            )
                    )
                }
            }
        }
    }
}
