package com.neb.ians.ui.screens.reader.pdf

import android.graphics.Bitmap
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.PagerState
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ColorFilter
import androidx.compose.ui.graphics.ColorMatrix
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/** Where page bitmaps come from: the cache (synchronous) and the renderer. */
@Immutable
class PageSource(
    val cached: (index: Int, widthPx: Int) -> Bitmap?,
    val render: suspend (index: Int, widthPx: Int) -> Bitmap?
)

/** How a reading theme paints: the backdrop, the page before it loads, and the page filter. */
@Immutable
data class ReaderLook(val canvas: Color, val paper: Color, val filter: ColorFilter?, val shadow: Boolean)

@Composable
fun readerLook(theme: ReadingTheme): ReaderLook {
    val canvas = MaterialTheme.colorScheme.surfaceContainerHighest
    return remember(theme, canvas) {
        when (theme) {
            ReadingTheme.Paper -> ReaderLook(canvas, Color.White, null, shadow = true)
            ReadingTheme.Sepia -> ReaderLook(Color(0xFFE6DCC6), Color(0xFFF4ECD8), ColorFilter.colorMatrix(SEPIA), shadow = true)
            ReadingTheme.Night -> ReaderLook(Color(0xFF050505), Color(0xFF141414), ColorFilter.colorMatrix(NIGHT), shadow = false)
        }
    }
}

/** White becomes warm paper, black stays ink. */
private val SEPIA = ColorMatrix(
    floatArrayOf(
        0.957f, 0f, 0f, 0f, 0f,
        0f, 0.925f, 0f, 0f, 0f,
        0f, 0f, 0.847f, 0f, 0f,
        0f, 0f, 0f, 1f, 0f
    )
)

/**
 * Inverts lightness but keeps hue (invert, then rotate hue by 180 degrees), so diagrams and
 * photos keep their colours. White paper lands on near-black, black ink on soft white.
 */
private val NIGHT: ColorMatrix = run {
    val h = floatArrayOf(
        -0.574f, 1.430f, 0.144f,
        0.426f, 0.430f, 0.144f,
        0.426f, 1.430f, -0.856f
    )
    val k = 0.83f
    val offset = 255f * k + 20f
    ColorMatrix(
        floatArrayOf(
            -k * h[0], -k * h[1], -k * h[2], 0f, offset,
            -k * h[3], -k * h[4], -k * h[5], 0f, offset,
            -k * h[6], -k * h[7], -k * h[8], 0f, offset,
            0f, 0f, 0f, 1f, 0f
        )
    )
}

/**
 * One page. Its box has the page's real proportions from the start, so the list never jumps
 * when bitmaps arrive. When the requested width changes (zoom settles, rotation) the previous
 * bitmap stays on screen until the sharper one is ready.
 */
@Composable
fun PdfPage(index: Int, aspect: Float, widthPx: Int, look: ReaderLook, source: PageSource, modifier: Modifier = Modifier) {
    val bitmap by produceState(initialValue = source.cached(index, widthPx), index, widthPx) {
        source.render(index, widthPx)?.let { value = it }
    }
    val image = remember(bitmap) { bitmap?.asImageBitmap() }
    Box(
        modifier
            .aspectRatio(1f / aspect.coerceAtLeast(0.1f))
            .then(if (look.shadow) Modifier.shadow(1.5.dp, RectangleShape, clip = false) else Modifier)
            .background(look.paper)
    ) {
        if (image != null) {
            Image(
                bitmap = image,
                contentDescription = "Page ${index + 1}",
                contentScale = ContentScale.FillBounds,
                colorFilter = look.filter,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

private val PageGutter = 10.dp

/** Continuous vertical reading. */
@Composable
fun ScrollReader(
    aspects: List<Float>,
    listState: LazyListState,
    zoom: ReaderZoomState,
    look: ReaderLook,
    source: PageSource,
    contentPadding: PaddingValues,
    onTap: () -> Unit
) {
    val scope = rememberCoroutineScope()
    val zoomedIn by remember(zoom) { derivedStateOf { zoom.isZoomed } }
    val scrollList = remember(listState) { { dy: Float -> listState.dispatchRawDelta(dy); Unit } }
    val flingBy = remember(listState) {
        val fling: suspend (Float) -> Unit = { velocity -> listState.scroll { decayFling(velocity) { scrollBy(it) } } }
        fling
    }
    BoxWithConstraints(
        Modifier
            .fillMaxSize()
            .background(look.canvas)
            .clipToBounds()
            .onSizeChanged { zoom.size = it }
            .zoomGestures(zoom, scope, onTap, scrollList, flingBy)
    ) {
        val density = LocalDensity.current
        val pageWidthPx = with(density) { (maxWidth - PageGutter * 2).roundToPx() }
        val renderWidth = (pageWidthPx * zoom.renderScale).toInt()
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize().zoomed(zoom),
            contentPadding = contentPadding,
            verticalArrangement = Arrangement.spacedBy(PageGutter),
            userScrollEnabled = !zoomedIn
        ) {
            items(count = aspects.size, key = { it }, contentType = { 0 }) { index ->
                PdfPage(
                    index = index,
                    aspect = aspects[index],
                    widthPx = renderWidth,
                    look = look,
                    source = source,
                    modifier = Modifier.fillMaxWidth().padding(horizontal = PageGutter)
                )
            }
        }
    }
}

/** One page at a time, each fitted to the screen. */
@Composable
fun PagedReader(
    aspects: List<Float>,
    pagerState: PagerState,
    zoom: ReaderZoomState,
    look: ReaderLook,
    source: PageSource,
    verticalInset: Dp,
    onTap: () -> Unit
) {
    val scope = rememberCoroutineScope()
    val zoomedIn by remember(zoom) { derivedStateOf { zoom.isZoomed } }
    LaunchedEffect(pagerState.settledPage) { zoom.reset() }
    HorizontalPager(
        state = pagerState,
        modifier = Modifier.fillMaxSize().background(look.canvas),
        beyondViewportPageCount = 1,
        userScrollEnabled = !zoomedIn,
        key = { it }
    ) { page ->
        val active = page == pagerState.currentPage
        BoxWithConstraints(
            Modifier
                .fillMaxSize()
                .clipToBounds()
                .then(
                    if (active) {
                        Modifier
                            .onSizeChanged { zoom.size = it }
                            .zoomGestures(zoom, scope, onTap, scrollBy = null, flingBy = null)
                    } else {
                        Modifier.pointerInput(Unit) { detectTapGestures(onTap = { onTap() }) }
                    }
                ),
            contentAlignment = Alignment.Center
        ) {
            val aspect = aspects[page].coerceAtLeast(0.1f)
            val availableHeight = maxHeight - verticalInset * 2
            val fitWidth = minOf(maxWidth - PageGutter * 2, availableHeight / aspect)
            val density = LocalDensity.current
            val scale = if (active) zoom.renderScale else 1f
            val widthPx = (with(density) { fitWidth.roundToPx() } * scale).toInt()
            Box(
                Modifier.fillMaxSize().then(if (active) Modifier.zoomed(zoom) else Modifier),
                contentAlignment = Alignment.Center
            ) {
                PdfPage(page, aspect, widthPx, look, source, Modifier.width(fitWidth))
            }
        }
    }
}
