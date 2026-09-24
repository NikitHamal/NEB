package com.neb.ians.ui.screens.canvas

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.Canvas
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.Stroke
import kotlin.math.max
import kotlin.math.min

@Composable
fun CanvasMinimap(
    nodes: List<CanvasNode>,
    heights: Map<String, Float>,
    viewportTx: Float,
    viewportTy: Float,
    viewportScale: Float,
    onDismiss: () -> Unit,
    onJumpTo: (targetX: Float, targetY: Float) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .width(170.dp)
            .height(130.dp)
            .shadow(12.dp, RoundedCornerShape(16.dp))
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.95f))
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
            .padding(6.dp)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "RADAR MAP",
                    style = MaterialTheme.typography.labelSmall.copy(
                        fontSize = 9.sp,
                        letterSpacing = 0.8.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    ),
                    modifier = Modifier.padding(start = 4.dp)
                )
                IconButton(
                    onClick = onDismiss,
                    modifier = Modifier.size(20.dp)
                ) {
                    Icon(
                        imageVector = Icons.Outlined.Close,
                        contentDescription = "Close Minimap",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(13.dp)
                    )
                }
            }

            val nodeFill = MaterialTheme.colorScheme.onSurfaceVariant
            val nodeStroke = MaterialTheme.colorScheme.onSurface
            val viewportTint = MaterialTheme.colorScheme.onSurface

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerLowest)
            ) {
                Canvas(
                    modifier = Modifier.fillMaxSize()
                ) {
                    if (nodes.isEmpty()) return@Canvas

                    var minX = Float.MAX_VALUE
                    var minY = Float.MAX_VALUE
                    var maxX = Float.MIN_VALUE
                    var maxY = Float.MIN_VALUE

                    nodes.forEach { n ->
                        minX = min(minX, n.x)
                        minY = min(minY, n.y)
                        val b = boundsOf(n, heights)
                        maxX = max(maxX, b.right)
                        maxY = max(maxY, b.bottom)
                    }

                    val worldWidth = max(1200f, maxX - minX + 400f)
                    val worldHeight = max(900f, maxY - minY + 400f)
                    val scaleX = size.width / worldWidth
                    val scaleY = size.height / worldHeight
                    val mapScale = min(scaleX, scaleY)

                    val offsetX = (size.width - worldWidth * mapScale) / 2f
                    val offsetY = (size.height - worldHeight * mapScale) / 2f

                    // Draw card mini rects
                    nodes.forEach { n ->
                        val rx = offsetX + (n.x - minX + 200f) * mapScale
                        val ry = offsetY + (n.y - minY + 200f) * mapScale
                        val rw = CanvasCardWidth * mapScale
                        val rh = (heights[n.id] ?: CanvasCardFallbackHeight) * mapScale

                        drawRect(
                            color = nodeFill.copy(alpha = 0.32f),
                            topLeft = Offset(rx, ry),
                            size = Size(rw, rh)
                        )
                        drawRect(
                            color = nodeStroke.copy(alpha = 0.55f),
                            topLeft = Offset(rx, ry),
                            size = Size(rw, rh),
                            style = Stroke(width = 1f)
                        )
                    }

                    // Draw current viewport frame
                    val viewW = 360f / viewportScale
                    val viewH = 640f / viewportScale
                    val viewLeft = -viewportTx / viewportScale
                    val viewTop = -viewportTy / viewportScale

                    val vx = offsetX + (viewLeft - minX + 200f) * mapScale
                    val vy = offsetY + (viewTop - minY + 200f) * mapScale
                    val vw = viewW * mapScale
                    val vh = viewH * mapScale

                    drawRect(
                        color = viewportTint.copy(alpha = 0.10f),
                        topLeft = Offset(vx, vy),
                        size = Size(vw, vh)
                    )
                    drawRect(
                        color = viewportTint,
                        topLeft = Offset(vx, vy),
                        size = Size(vw, vh),
                        style = Stroke(width = 1.5f)
                    )
                }
            }
        }
    }
}
