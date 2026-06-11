package com.consica.code.ui.dragdrop

import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DragIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import com.consica.code.core.design.CardShape
import com.consica.code.core.design.Dimens
import com.consica.code.core.design.codeTextStyle
import kotlinx.coroutines.flow.distinctUntilChanged

private val RowHeight = 56.dp
private val RowSpacing = 8.dp

/**
 * Native long-press drag-to-reorder list. No external library — swaps with the neighbour once the
 * dragged block crosses half a row. [onOrderChange] reports the live order so the host can check it.
 */
@Composable
fun BlockPuzzleBoard(
    blocks: List<String>,
    modifier: Modifier = Modifier,
    onOrderChange: (List<String>) -> Unit = {},
) {
    val items = remember(blocks) { mutableStateListOf<String>().apply { addAll(blocks) } }
    var draggingIndex by remember { mutableIntStateOf(-1) }
    var dragOffsetY by remember { mutableFloatStateOf(0f) }

    val density = LocalDensity.current
    val stepPx = with(density) { (RowHeight + RowSpacing).toPx() }

    // Report order changes to the host.
    androidx.compose.runtime.LaunchedEffect(items) {
        snapshotFlow { items.toList() }
            .distinctUntilChanged()
            .collect { onOrderChange(it) }
    }

    Column(modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(RowSpacing)) {
        items.forEachIndexed { index, block ->
            val isDragging = index == draggingIndex
            Surface(
                shape = CardShape,
                color = if (isDragging) MaterialTheme.colorScheme.primaryContainer
                else MaterialTheme.colorScheme.surface,
                border = androidx.compose.foundation.BorderStroke(
                    1.dp, MaterialTheme.colorScheme.outlineVariant,
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(RowHeight)
                    .zIndex(if (isDragging) 1f else 0f)
                    .graphicsLayer { translationY = if (isDragging) dragOffsetY else 0f }
                    .then(if (isDragging) Modifier.shadow(6.dp, CardShape) else Modifier)
                    .pointerInput(block) {
                        detectDragGesturesAfterLongPress(
                            onDragStart = {
                                draggingIndex = items.indexOf(block)
                                dragOffsetY = 0f
                            },
                            onDragEnd = { draggingIndex = -1; dragOffsetY = 0f },
                            onDragCancel = { draggingIndex = -1; dragOffsetY = 0f },
                            onDrag = { change, amount ->
                                change.consume()
                                dragOffsetY += amount.y
                                val cur = draggingIndex
                                if (cur < 0) return@detectDragGesturesAfterLongPress
                                if (dragOffsetY > stepPx / 2 && cur < items.lastIndex) {
                                    val tmp = items[cur]; items[cur] = items[cur + 1]; items[cur + 1] = tmp
                                    draggingIndex = cur + 1
                                    dragOffsetY -= stepPx
                                } else if (dragOffsetY < -stepPx / 2 && cur > 0) {
                                    val tmp = items[cur]; items[cur] = items[cur - 1]; items[cur - 1] = tmp
                                    draggingIndex = cur - 1
                                    dragOffsetY += stepPx
                                }
                            },
                        )
                    },
            ) {
                Row(
                    Modifier.padding(horizontal = Dimens.lg),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(
                        Icons.Filled.DragIndicator,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Spacer(Modifier.width(Dimens.md))
                    Text(
                        block,
                        style = codeTextStyle(),
                        color = MaterialTheme.colorScheme.onSurface,
                    )
                }
            }
        }
        Spacer(Modifier.heightIn(min = Dimens.xs))
    }
}
