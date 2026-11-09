package com.neb.ians.ui.screens.reader.pdf

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.calculateZoom
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.PointerEventPass
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.theme.Poppins
import kotlin.math.roundToInt

/** Something in the text that opens full screen to be pinched, panned and read closely. */
internal sealed interface RdZoomItem {
    class Figure(val block: FigureBlock) : RdZoomItem
    class Table(val block: TableBlock) : RdZoomItem
}

/**
 * Two fingers anywhere on the text change its size, live, in 5 % steps (the e-reader way: the
 * words reflow and stay sharp). One finger is left alone so the list keeps its own scrolling.
 * [onLive] reports the size while the fingers are down (null once they lift) for the badge.
 */
@Composable
internal fun Modifier.pinchTextSize(current: Float, onScale: (Float) -> Unit, onLive: (Float?) -> Unit): Modifier {
    val latest by rememberUpdatedState(current)
    val apply by rememberUpdatedState(onScale)
    val live by rememberUpdatedState(onLive)
    return this.pointerInput(Unit) {
        awaitEachGesture {
            awaitFirstDown(requireUnconsumed = false, pass = PointerEventPass.Initial)
            val base = latest
            var factor = 1f
            var applied = base
            do {
                val event = awaitPointerEvent(PointerEventPass.Initial)
                if (event.changes.count { it.pressed } >= 2) {
                    factor *= event.calculateZoom()
                    val target = ((base * factor * 20f).roundToInt() / 20f).coerceIn(0.7f, 3f)
                    if (target != applied) { applied = target; apply(target) }
                    live(target)
                    event.changes.forEach { it.consume() }
                }
            } while (event.changes.any { it.pressed })
            live(null)
        }
    }
}

/** The size badge shown while pinching. */
@Composable
internal fun RdSizeBadge(scale: Float, p: ReadingPalette, modifier: Modifier = Modifier) {
    Box(modifier.clip(RoundedCornerShape(50)).background(p.ink).padding(horizontal = 16.dp, vertical = 8.dp)) {
        Text(
            "${(scale * 100).roundToInt()}%",
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.SemiBold,
            color = p.bg
        )
    }
}

/** Full screen view of a figure (pinch, pan, double tap) or a table (pinch resizes the type, scroll both ways). */
@Composable
internal fun RdZoomDialog(
    item: RdZoomItem,
    p: ReadingPalette,
    source: ReadSource,
    onClose: () -> Unit,
    onOpenPage: (Int) -> Unit
) {
    Dialog(
        onDismissRequest = onClose,
        properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)
    ) {
        Column(Modifier.fillMaxSize().background(p.bg).windowInsetsPadding(WindowInsets.statusBars).windowInsetsPadding(WindowInsets.navigationBars)) {
            Row(Modifier.fillMaxWidth().padding(horizontal = 6.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                NebIconButton(Icons.Outlined.Close, "Close", onClose, tint = p.ink)
                Text(
                    when (item) { is RdZoomItem.Figure -> "Figure, page ${item.block.page + 1}"; is RdZoomItem.Table -> "Table" },
                    style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, color = p.ink,
                    modifier = Modifier.weight(1f).padding(horizontal = 6.dp)
                )
                if (item is RdZoomItem.Figure) {
                    NebIconButton(Icons.Outlined.PictureAsPdf, "Open the original page", { onClose(); onOpenPage(item.block.page) }, tint = p.ink)
                }
            }
            HorizontalDivider(color = p.line)
            when (item) {
                is RdZoomItem.Figure -> RdZoomFigure(item.block, p, source)
                is RdZoomItem.Table -> RdZoomTable(item.block, p)
            }
        }
    }
}

@Composable
private fun RdZoomFigure(b: FigureBlock, p: ReadingPalette, source: ReadSource) {
    val bitmap by produceState(source.cachedCrop(b.page, b.rect, 1800), b) {
        source.loadCrop(b.page, b.rect, 1800)?.let { value = it }
    }
    var scale by remember { mutableFloatStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    var box by remember { mutableStateOf(IntSize.Zero) }
    fun clamp(o: Offset, s: Float) = Offset(
        o.x.coerceIn(box.width * (1f - s), 0f),
        o.y.coerceIn(box.height * (1f - s), 0f)
    )
    Box(
        Modifier
            .fillMaxSize()
            .clipToBounds()
            .onSizeChanged { box = it }
            .pointerInput(Unit) {
                detectTransformGestures { centroid, pan, zoom, _ ->
                    val next = (scale * zoom).coerceIn(1f, 8f)
                    offset = clamp(centroid - (centroid - offset) * (next / scale) + pan, next)
                    scale = next
                }
            }
            .pointerInput(Unit) {
                detectTapGestures(onDoubleTap = { at ->
                    if (scale > 1.05f) { scale = 1f; offset = Offset.Zero }
                    else { scale = 2.5f; offset = clamp(at - (at) * 2.5f, 2.5f) }
                })
            },
        contentAlignment = Alignment.Center
    ) {
        val image = remember(bitmap) { bitmap?.asImageBitmap() }
        if (image != null) {
            Image(
                image, "Figure from page ${b.page + 1}",
                Modifier.fillMaxSize().graphicsLayer {
                    transformOrigin = TransformOrigin(0f, 0f)
                    scaleX = scale; scaleY = scale
                    translationX = offset.x; translationY = offset.y
                },
                contentScale = ContentScale.Fit, colorFilter = p.filter
            )
        } else {
            Text("Loading", style = MaterialTheme.typography.bodyMedium, color = p.muted)
        }
    }
}

@Composable
private fun RdZoomTable(b: TableBlock, p: ReadingPalette) {
    val cols = b.rows.maxOfOrNull { it.cells.size } ?: return
    var zoom by remember { mutableFloatStateOf(1f) }
    Box(
        Modifier
            .fillMaxSize()
            .pointerInput(Unit) { detectTransformGestures { _, _, z, _ -> zoom = (zoom * z).coerceIn(0.8f, 3f) } }
            .verticalScroll(rememberScrollState())
            .horizontalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Column(Modifier.clip(RoundedCornerShape(18.dp)).background(p.tonal)) {
            b.rows.forEachIndexed { i, row ->
                Row(Modifier.padding(horizontal = 14.dp, vertical = 12.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    for (c in 0 until cols) {
                        Text(
                            row.cells.getOrElse(c) { "" },
                            style = androidx.compose.ui.text.TextStyle(
                                fontFamily = Poppins, fontSize = (15f * zoom).sp, lineHeight = (21f * zoom).sp,
                                fontWeight = if (b.header && i == 0) FontWeight.SemiBold else FontWeight.Normal,
                                color = p.ink, textAlign = TextAlign.Start
                            ),
                            modifier = Modifier.widthIn(min = (110f * zoom).dp, max = (240f * zoom).dp)
                        )
                    }
                }
                if (i < b.rows.lastIndex) HorizontalDivider(color = p.line)
            }
        }
    }
}

/** True when a list marker is a lettered choice: (a) a. A) (B) and so on. */
internal fun isOptionMarker(marker: String): Boolean = OptionMarker.matches(marker.trim())
private val OptionMarker = Regex("^\\(?[A-Ha-h]\\)?[.):]?$")

/** How many list items from [start] form one run of lettered choices that begins at a (at least two). */
internal fun optionRunLength(blocks: List<Block>, start: Int): Int {
    val first = blocks.getOrNull(start) as? ItemBlock ?: return 0
    if (!isOptionMarker(first.marker) || first.marker.trim().trim('(', ')', '.', ':').lowercase() != "a") return 0
    var n = 0
    while (start + n < blocks.size) {
        val b = blocks[start + n] as? ItemBlock ?: break
        if (!isOptionMarker(b.marker)) break
        n++
    }
    return if (n >= 2) n else 0
}

/** Labels that open a worked answer, hint, note or definition; shown as a tonal card instead of a plain paragraph. */
internal val CalloutPattern = Regex(
    "^(Answer|Ans|Solution|Hint|Note|Example|Definition|Remember|Tip|Caution|Warning|Key point|Explanation|Formula)s?\\s*(?:\\d+\\s*)?[:.\\u2013\\u2014-]\\s*",
    RegexOption.IGNORE_CASE
)
