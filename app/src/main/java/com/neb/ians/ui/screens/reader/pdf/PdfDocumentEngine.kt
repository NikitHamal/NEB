package com.neb.ians.ui.screens.reader.pdf

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.RectF
import android.graphics.pdf.PdfRenderer
import android.os.Build
import android.os.ext.SdkExtensions
import androidx.annotation.RequiresExtension
import android.os.ParcelFileDescriptor
import android.util.LruCache
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.io.Closeable
import java.io.File

/**
 * One open PDF: page geometry read once at open, pages rendered on demand through
 * [PdfRenderer] (which allows a single open page at a time, hence the mutex), and a
 * memory-bounded bitmap cache shared by full pages and thumbnails.
 *
 * Widths are bucketed so that small layout changes reuse cached bitmaps instead of
 * re-rendering, and the cache is sized from the app's heap so long books never push the
 * process towards an OutOfMemoryError.
 */
class PdfDocumentEngine private constructor(
    private val descriptor: ParcelFileDescriptor,
    private val renderer: PdfRenderer,
    /** Height / width of every page. Starts as the first page's shape for all pages; [scanShapes] corrects it in the background. */
    initialAspects: FloatArray,
    file: File
) : Closeable {

    /** Links, contents and reflowed text; opened on first use. */
    val structure = PdfStructureEngine(file, initialAspects.size)

    private val crops = object : LruCache<String, Bitmap>(12 * 1024) {
        override fun sizeOf(key: String, value: Bitmap): Int = value.allocationByteCount / 1024
    }

    fun cachedCrop(index: Int, rect: FRect, widthPx: Int): Bitmap? = crops.get(cropKey(index, rect, widthPx))

    private fun cropKey(index: Int, rect: FRect, widthPx: Int) = "$index:${rect.l},${rect.t},${rect.r},${rect.b}@${widthPx / 32}"

    /**
     * A picture cut out of a page: the page is rendered just large enough for the cut to be [widthPx] wide,
     * the part is copied out and the page left to the cache. Used by reading mode for diagrams and equations.
     */
    suspend fun crop(index: Int, rect: FRect, widthPx: Int): Bitmap? {
        if (index !in 0 until pageCount || widthPx <= 0 || rect.w <= 0.001f || rect.h <= 0.001f) return null
        val key = cropKey(index, rect, widthPx)
        crops.get(key)?.let { return it }
        // page renders are shared between crops: the width is rounded up to a step so the dozens of small
        // pictures on one page (typeset maths set inside the text) come out of one render, not one each
        val wanted = (widthPx / rect.w).toInt().coerceIn(THUMB_WIDTH, MAX_WIDTH)
        val pageWidth = (((wanted + 255) / 256) * 256).coerceAtMost(MAX_WIDTH)
        val page = render(index, pageWidth) ?: return null
        return withContext(Dispatchers.Default) {
            val x = (rect.l * page.width).toInt().coerceIn(0, page.width - 1)
            val y = (rect.t * page.height).toInt().coerceIn(0, page.height - 1)
            val w = (rect.w * page.width).toInt().coerceIn(1, page.width - x)
            val h = (rect.h * page.height).toInt().coerceIn(1, page.height - y)
            runCatching { Bitmap.createBitmap(page, x, y, w, h) }.getOrNull()?.also { crops.put(key, it) }
        }
    }

    private val aspects: FloatArray = initialAspects

    /** Height / width of every page, in document order (a snapshot; see [scanShapes]). */
    val pageAspects: List<Float> get() = aspects.toList()

    val pageCount: Int get() = aspects.size

    private val mutex = Mutex()
    @Volatile private var closed = false

    private val hiResPixels: Float = minOf(MAX_PIXELS, cacheBudgetKb() * 1024f / 4f / 2f).coerceAtLeast(BASE_PIXELS.toFloat())

    private val cache = object : LruCache<String, Bitmap>(cacheBudgetKb()) {
        override fun sizeOf(key: String, value: Bitmap): Int = value.allocationByteCount / 1024
    }

    fun cached(index: Int, widthPx: Int): Bitmap? =
        if (index in 0 until pageCount) cache.get(key(index, widthFor(index, widthPx))) else null

    suspend fun render(index: Int, widthPx: Int): Bitmap? {
        if (index !in 0 until pageCount || widthPx <= 0) return null
        val width = widthFor(index, widthPx)
        val key = key(index, width)
        cache.get(key)?.let { return it }
        return withContext(Dispatchers.IO) {
            mutex.withLock {
                cache.get(key)?.let { return@withLock it }
                if (closed) return@withLock null
                val bitmap = runCatching {
                    renderer.openPage(index).use { page ->
                        if (page.width > 0) aspects[index] = page.height.toFloat() / page.width
                        val height = (width * page.height.toFloat() / page.width).toInt().coerceAtLeast(1)
                        // zoomed renders are large: 16-bit colour halves their memory, and text stays crisp
                        val config = if (width.toLong() * height > BASE_PIXELS) Bitmap.Config.RGB_565 else Bitmap.Config.ARGB_8888
                        val bitmap = Bitmap.createBitmap(width, height, config)
                        bitmap.eraseColor(Color.WHITE)
                        page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                        bitmap
                    }
                }.getOrNull()
                // close() arrived mid-render and left the release to us
                if (closed) release() else bitmap?.let { cache.put(key, it) }
                bitmap
            }
        }
    }

    /**
     * Reads the real shape of every page without holding up rendering: the document opens knowing
     * only the first page (a 1000 page book used to open every page up front, which took ages on
     * slow phones), and this fills in the rest in small batches, releasing the renderer between
     * batches so a visible page never waits for more than a few pages. Calls [onChange] with a
     * fresh list only when some page differs from what the layout already assumes.
     */
    suspend fun scanShapes(first: Int, onChange: (List<Float>) -> Unit) {
        val order = ArrayList<Int>(pageCount)
        val start = first.coerceIn(0, (pageCount - 1).coerceAtLeast(0))
        for (i in start until pageCount) order.add(i)
        for (i in 0 until start) order.add(i)
        var changed = false
        var done = 0
        while (done < order.size && !closed) {
            val batchEnd = minOf(done + SCAN_BATCH, order.size)
            mutex.withLock {
                if (closed) return
                for (k in done until batchEnd) {
                    val index = order[k]
                    val shape = runCatching {
                        renderer.openPage(index).use { page -> if (page.width > 0) page.height.toFloat() / page.width else 0f }
                    }.getOrDefault(0f)
                    if (shape > 0f && kotlin.math.abs(shape - aspects[index]) > 0.002f) {
                        aspects[index] = shape
                        changed = true
                    }
                }
            }
            done = batchEnd
            if (changed && (done % (SCAN_BATCH * 8) == 0 || done >= order.size)) {
                changed = false
                onChange(aspects.toList())
            }
            kotlinx.coroutines.yield()
            kotlinx.coroutines.delay(4)
        }
        if (changed) onChange(aspects.toList())
    }

    suspend fun thumbnail(index: Int): Bitmap? = render(index, THUMB_WIDTH)

    /** Whether this device's PDF module can read text (Android 15, or 11+ with the PDF mainline update). */
    val canReadText: Boolean get() = TEXT_API

    /**
     * Where [query] occurs on page [index], as rectangles in page fractions (0..1), so they
     * scale with whatever width the page is drawn at. Empty when text is unavailable.
     */
    suspend fun search(index: Int, query: String): List<RectF> {
        if (!TEXT_API || query.isBlank() || index !in 0 until pageCount) return emptyList()
        return withContext(Dispatchers.IO) {
            mutex.withLock {
                if (closed) emptyList() else runCatching { TextApi.search(renderer, index, query) }.getOrDefault(emptyList())
            }
        }
    }

    /** The text of page [index], or null when the page has none or text is unavailable. */
    suspend fun pageText(index: Int): String? {
        if (!TEXT_API || index !in 0 until pageCount) return null
        return withContext(Dispatchers.IO) {
            mutex.withLock {
                if (closed) null else runCatching { TextApi.text(renderer, index) }.getOrNull()?.takeIf { it.isNotBlank() }
            }
        }
    }

    override fun close() {
        closed = true
        cache.evictAll()
        crops.evictAll()
        structure.close()
        // PdfRenderer must not be closed while a page is open; a render in flight releases it.
        if (mutex.tryLock()) {
            try { release() } finally { mutex.unlock() }
        }
    }

    private var released = false

    private fun release() {
        if (released) return
        released = true
        runCatching { renderer.close() }
        runCatching { descriptor.close() }
    }

    private fun key(index: Int, width: Int) = "$index@$width"

    /**
     * Bucketed width, lowered so one page stays within budget: [BASE_PIXELS] in full colour, or up
     * to [MAX_PIXELS] in 16-bit colour for zoomed renders, never more than a quarter of the cache.
     */
    private fun widthFor(index: Int, widthPx: Int): Int {
        val width = bucket(widthPx)
        val aspect = aspects[index].coerceAtLeast(0.1f)
        val cap = kotlin.math.sqrt(hiResPixels / aspect).toInt()
        return if (width <= cap) width else (cap / BUCKET * BUCKET).coerceAtLeast(THUMB_WIDTH)
    }

    @RequiresExtension(extension = Build.VERSION_CODES.R, version = 13)
    private object TextApi {
        fun search(renderer: PdfRenderer, index: Int, query: String): List<RectF> =
            renderer.openPage(index).use { page ->
                val w = page.width.toFloat().coerceAtLeast(1f)
                val h = page.height.toFloat().coerceAtLeast(1f)
                page.searchText(query).flatMap { match ->
                    match.bounds.map { r -> RectF(r.left / w, r.top / h, r.right / w, r.bottom / h) }
                }
            }

        fun text(renderer: PdfRenderer, index: Int): String =
            renderer.openPage(index).use { page -> page.textContents.joinToString("\n") { it.text } }
    }

    companion object {
        private val TEXT_API: Boolean =
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.R && SdkExtensions.getExtensionVersion(Build.VERSION_CODES.R) >= 13

        const val THUMB_WIDTH = 240
        /** Width of the quick first paint of a page while its sharp render is still queued. */
        const val PREVIEW_WIDTH = 320
        private const val SCAN_BATCH = 6
        private const val BUCKET = 160
        private const val MAX_WIDTH = 4200
        private const val BASE_PIXELS = 6_000_000L
        private const val MAX_PIXELS = 15_000_000f

        /** Width rounded up to a 160 px bucket and capped, so near-equal widths share a bitmap. */
        fun bucket(widthPx: Int): Int {
            if (widthPx <= THUMB_WIDTH) return THUMB_WIDTH
            val rounded = ((widthPx + BUCKET - 1) / BUCKET) * BUCKET
            return rounded.coerceAtMost(MAX_WIDTH)
        }

        private fun cacheBudgetKb(): Int {
            val maxKb = (Runtime.getRuntime().maxMemory() / 1024).toInt()
            return (maxKb / 5).coerceIn(24 * 1024, 112 * 1024)
        }

        /** Opens [file] and reads every page's size. Call off the main thread. */
        fun open(file: File): PdfDocumentEngine {
            val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
            try {
                val renderer = PdfRenderer(descriptor)
                val count = renderer.pageCount
                val firstShape = if (count > 0) {
                    renderer.openPage(0).use { page -> if (page.width > 0) page.height.toFloat() / page.width else 1.414f }
                } else 1.414f
                return PdfDocumentEngine(descriptor, renderer, FloatArray(count) { firstShape }, file)
            } catch (t: Throwable) {
                runCatching { descriptor.close() }
                throw t
            }
        }
    }
}
