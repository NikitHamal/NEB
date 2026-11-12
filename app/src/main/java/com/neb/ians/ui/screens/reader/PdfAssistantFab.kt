package com.neb.ians.ui.screens.reader

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animate
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.FloatingActionButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlin.math.hypot
import kotlin.math.roundToInt

/**
 * The Neby AI button. It can be dragged anywhere (it settles against the nearest side), and dragging
 * it onto the target that appears at the bottom dismisses it; the reader's menu brings it back.
 * [x] and [y] are where it rests as fractions of the free area (negative: the default corner).
 */
@Composable
fun AssistantFab(
    x: Float,
    y: Float,
    onClick: () -> Unit,
    onMoved: (Float, Float) -> Unit,
    onDismissed: () -> Unit,
    modifier: Modifier = Modifier
) {
    BoxWithConstraints(modifier.fillMaxSize()) {
        val density = LocalDensity.current
        val fab = with(density) { 56.dp.toPx() }
        val margin = with(density) { 18.dp.toPx() }
        val width = constraints.maxWidth.toFloat()
        val height = constraints.maxHeight.toFloat()
        val minX = margin
        val maxX = (width - fab - margin).coerceAtLeast(minX)
        val minY = margin
        val maxY = (height - fab - margin).coerceAtLeast(minY)
        var px by remember { mutableFloatStateOf(-1f) }
        var py by remember { mutableFloatStateOf(-1f) }
        var dragging by remember { mutableStateOf(false) }
        var overTarget by remember { mutableStateOf(false) }
        val scope = rememberCoroutineScope()
        val targetX = width / 2f
        val targetY = height - with(density) { 28.dp.toPx() + 32.dp.toPx() }

        LaunchedEffect(width, height) {
            px = if (x < 0f) maxX else minX + x.coerceIn(0f, 1f) * (maxX - minX)
            py = if (y < 0f) maxY else minY + y.coerceIn(0f, 1f) * (maxY - minY)
        }

        AnimatedVisibility(
            visible = dragging,
            modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 28.dp),
            enter = fadeIn() + scaleIn(),
            exit = fadeOut() + scaleOut()
        ) {
            Box(
                Modifier
                    .size(if (overTarget) 72.dp else 60.dp)
                    .clip(CircleShape)
                    .background(if (overTarget) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Filled.Close, contentDescription = "Dismiss Neby AI",
                    tint = if (overTarget) MaterialTheme.colorScheme.onError else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        if (px >= 0f) {
            Box(
                Modifier
                    .offset { IntOffset(px.roundToInt(), py.roundToInt()) }
                    .graphicsLayer {
                        val s = if (overTarget) 0.78f else if (dragging) 1.08f else 1f
                        scaleX = s; scaleY = s
                    }
                    .pointerInput(width, height) {
                        detectDragGestures(
                            onDragStart = { dragging = true },
                            onDrag = { change, drag ->
                                change.consume()
                                px = (px + drag.x).coerceIn(-fab / 2f, width - fab / 2f)
                                py = (py + drag.y).coerceIn(-fab / 2f, height - fab / 2f)
                                overTarget = hypot(px + fab / 2f - targetX, py + fab / 2f - targetY) < with(density) { 64.dp.toPx() }
                            },
                            onDragEnd = {
                                dragging = false
                                if (overTarget) {
                                    overTarget = false
                                    onDismissed()
                                } else {
                                    val endX = if (px + fab / 2f < width / 2f) minX else maxX
                                    val endY = py.coerceIn(minY, maxY)
                                    val fromX = px
                                    val fromY = py
                                    scope.launch {
                                        launch { animate(fromX, endX, animationSpec = spring(dampingRatio = 0.75f, stiffness = 400f)) { v, _ -> px = v } }
                                        animate(fromY, endY, animationSpec = spring(dampingRatio = 0.75f, stiffness = 400f)) { v, _ -> py = v }
                                    }
                                    onMoved(
                                        if (maxX > minX) (endX - minX) / (maxX - minX) else 1f,
                                        if (maxY > minY) (endY - minY) / (maxY - minY) else 1f
                                    )
                                }
                            },
                            onDragCancel = { dragging = false; overTarget = false }
                        )
                    }
            ) {
                FloatingActionButton(
                    onClick = onClick,
                    shape = CircleShape,
                    containerColor = MaterialTheme.colorScheme.primary,
                    elevation = FloatingActionButtonDefaults.elevation(0.dp, 0.dp, 0.dp, 0.dp)
                ) {
                    Icon(Icons.Filled.AutoAwesome, contentDescription = "Ask AI about this PDF")
                }
            }
        }
    }
}
