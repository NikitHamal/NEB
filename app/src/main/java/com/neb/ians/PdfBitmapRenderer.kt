package com.neb.ians

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import android.util.LruCache
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.Closeable
import java.io.File
import kotlin.math.roundToInt

class PdfBitmapRenderer(file: File) : Closeable {
    private val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
    private val renderer = PdfRenderer(descriptor)
    private val lock = Any()
    private val bitmapCache = object : LruCache<String, Bitmap>(24 * 1024) {
        override fun sizeOf(key: String, value: Bitmap): Int = value.byteCount / 1024
    }

    val pageCount: Int = renderer.pageCount

    suspend fun renderPage(pageIndex: Int, targetWidthPx: Int): Bitmap = withContext(Dispatchers.Default) {
        val safeWidth = targetWidthPx.coerceIn(480, 2400)
        val cacheKey = "$pageIndex-$safeWidth"
        bitmapCache.get(cacheKey)?.let { return@withContext it }

        synchronized(lock) {
            val cached = bitmapCache.get(cacheKey)
            if (cached != null) {
                cached
            } else {
                val page = renderer.openPage(pageIndex)
                try {
                    val height = (safeWidth * page.height / page.width.toFloat()).roundToInt().coerceAtLeast(1)
                    val bitmap = Bitmap.createBitmap(safeWidth, height, Bitmap.Config.ARGB_8888)
                    bitmap.eraseColor(android.graphics.Color.WHITE)
                    page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    bitmapCache.put(cacheKey, bitmap)
                    bitmap
                } finally {
                    page.close()
                }
            }
        }
    }

    override fun close() {
        bitmapCache.evictAll()
        renderer.close()
        descriptor.close()
    }
}
