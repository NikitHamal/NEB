package com.neb.ians.ui.pdf

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.collection.LruCache
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import com.neb.ians.data.db.AnnotationEntity
import kotlinx.serialization.Serializable
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json
import java.io.File

/**
 * Wraps android.graphics.pdf.PdfRenderer with a small LRU bitmap cache for performance.
 */
class PdfRendererState private constructor(
    private val pfd: ParcelFileDescriptor,
    private val renderer: PdfRenderer,
) {
    val pageCount: Int get() = renderer.pageCount

    private val bitmapCache = object : LruCache<Int, Bitmap>(12) {
        override fun sizeOf(key: Int, value: Bitmap): Int = 1
        override fun entryRemoved(evicted: Boolean, key: Int, oldValue: Bitmap, newValue: Bitmap?) {
            if (evicted && !oldValue.isRecycled) oldValue.recycle()
        }
    }

    fun renderPage(index: Int): Bitmap {
        bitmapCache.get(index)?.let { if (!it.isRecycled) return it }
        val page = renderer.openPage(index)
        val targetWidth = 1080
        val targetHeight = (page.height.toFloat() / page.width.toFloat() * targetWidth).toInt()
        val bmp = Bitmap.createBitmap(targetWidth, targetHeight, Bitmap.Config.ARGB_8888).apply {
            eraseColor(Color.WHITE)
        }
        page.render(bmp, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
        page.close()
        bitmapCache.put(index, bmp)
        return bmp
    }

    fun close() {
        runCatching { bitmapCache.evictAll() }
        runCatching { renderer.close() }
        runCatching { pfd.close() }
    }

    companion object {
        fun open(file: File): PdfRendererState? {
            if (!file.exists() || file.length() == 0L) return null
            return runCatching {
                val pfd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                val r = PdfRenderer(pfd)
                PdfRendererState(pfd, r)
            }.getOrNull()
        }
    }
}

@Serializable
data class StoredRect(val l: Float, val t: Float, val r: Float, val b: Float)

private val json = Json { ignoreUnknownKeys = true }
private val storedRectSerializer = ListSerializer(StoredRect.serializer())

fun storedRectsJson(rects: List<StoredRect>): String = json.encodeToString(storedRectSerializer, rects)

fun parseStoredRects(s: String?): List<StoredRect> = if (s.isNullOrBlank()) emptyList() else
    runCatching { json.decodeFromString(storedRectSerializer, s) }.getOrDefault(emptyList())

fun AnnotationEntity.toRect(size: Size): Rect? {
    val rects = parseStoredRects(rectsJson)
    val first = rects.firstOrNull() ?: return null
    return Rect(
        first.l * size.width,
        first.t * size.height,
        first.r * size.width,
        first.b * size.height,
    )
}
