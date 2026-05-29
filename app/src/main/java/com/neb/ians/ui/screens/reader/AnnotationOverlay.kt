package com.neb.ians.ui.screens.reader

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import com.neb.ians.data.local.entity.AnnotationEntity

@Composable
fun AnnotationOverlay(
    annotations: List<AnnotationEntity>,
    annotationMode: AnnotationMode,
    onAnnotationCreated: (startX: Float, startY: Float, endX: Float, endY: Float) -> Unit,
    onAnnotationTapped: (AnnotationEntity) -> Unit,
    modifier: Modifier = Modifier
) {
    var dragStart by remember { mutableStateOf<Offset?>(null) }
    var dragEnd by remember { mutableStateOf<Offset?>(null) }
    var isDragging by remember { mutableStateOf(false) }

    val cachedAnnotations = remember(annotations) { annotations }

    Canvas(
        modifier = modifier
            .fillMaxSize()
            .pointerInput(annotationMode) {
                if (annotationMode != AnnotationMode.NONE) {
                    if (annotationMode == AnnotationMode.STICKY_NOTE) {
                        detectTapGestures { offset ->
                            onAnnotationCreated(
                                offset.x,
                                offset.y,
                                offset.x + 100f,
                                offset.y + 100f
                            )
                        }
                    } else {
                        detectDragGestures(
                            onDragStart = { offset ->
                                dragStart = offset
                                isDragging = true
                            },
                            onDrag = { change, _ ->
                                change.consume()
                                dragEnd = change.position
                            },
                            onDragEnd = {
                                val start = dragStart
                                val end = dragEnd
                                if (start != null && end != null) {
                                    onAnnotationCreated(
                                        start.x,
                                        start.y,
                                        end.x,
                                        end.y
                                    )
                                }
                                dragStart = null
                                dragEnd = null
                                isDragging = false
                            },
                            onDragCancel = {
                                dragStart = null
                                dragEnd = null
                                isDragging = false
                            }
                        )
                    }
                }
            }
            .pointerInput(annotationMode) {
                if (annotationMode == AnnotationMode.NONE) {
                    detectTapGestures { offset ->
                        for (annotation in cachedAnnotations) {
                            val inBoundsX = offset.x in annotation.startX..annotation.endX
                            val inBoundsY = offset.y in annotation.startY..annotation.endY
                            if (inBoundsX && inBoundsY) {
                                onAnnotationTapped(annotation)
                                break
                            }
                        }
                    }
                }
            }
    ) {
        cachedAnnotations.forEach { annotation ->
            val color = Color(annotation.color)
            when (annotation.type) {
                "HIGHLIGHT" -> {
                    drawRect(
                        color = color.copy(alpha = 0.35f),
                        topLeft = Offset(annotation.startX, annotation.startY),
                        size = Size(
                            annotation.endX - annotation.startX,
                            annotation.endY - annotation.startY
                        )
                    )
                }
                "UNDERLINE" -> {
                    drawLine(
                        color = color,
                        start = Offset(annotation.startX, annotation.endY),
                        end = Offset(annotation.endX, annotation.endY),
                        strokeWidth = 3f
                    )
                }
                "STICKY_NOTE" -> {
                    drawRect(
                        color = color.copy(alpha = 0.8f),
                        topLeft = Offset(annotation.startX, annotation.startY),
                        size = Size(80f, 80f)
                    )
                    drawRect(
                        color = color,
                        topLeft = Offset(annotation.startX, annotation.startY),
                        size = Size(80f, 80f),
                        style = Stroke(width = 2f)
                    )
                    drawLine(
                        color = color.copy(alpha = 0.6f),
                        start = Offset(annotation.startX + 60f, annotation.startY),
                        end = Offset(annotation.startX + 80f, annotation.startY + 20f),
                        strokeWidth = 1.5f
                    )
                }
            }
        }

        if (isDragging && dragStart != null && dragEnd != null) {
            val start = dragStart!!
            val end = dragEnd!!
            when (annotationMode) {
                AnnotationMode.HIGHLIGHT -> {
                    drawRect(
                        color = Color.Yellow.copy(alpha = 0.3f),
                        topLeft = Offset(
                            minOf(start.x, end.x),
                            minOf(start.y, end.y)
                        ),
                        size = Size(
                            kotlin.math.abs(end.x - start.x),
                            kotlin.math.abs(end.y - start.y)
                        )
                    )
                }
                AnnotationMode.UNDERLINE -> {
                    drawLine(
                        color = Color.Red,
                        start = Offset(start.x, end.y),
                        end = Offset(end.x, end.y),
                        strokeWidth = 3f
                    )
                }
                else -> {}
            }
        }
    }
}