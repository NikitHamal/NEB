package com.neb.ians.pdf

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import android.util.LruCache
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

data class RenderedPdfPage(
    val bitmap: Bitmap,
    val pageIndex: Int,
    val pageCount: Int
)

object PdfPageRenderer {
    private val bitmapCache = object : LruCache<String, Bitmap>(48 * 1024) {
        override fun sizeOf(key: String, value: Bitmap): Int = value.byteCount / 1024
    }

    suspend fun pageCount(file: File): Int = withContext(Dispatchers.IO) {
        ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY).use { descriptor ->
            PdfRenderer(descriptor).use { renderer -> renderer.pageCount }
        }
    }

    suspend fun render(file: File, pageIndex: Int, targetWidth: Int): RenderedPdfPage = withContext(Dispatchers.IO) {
        val width = targetWidth.coerceAtLeast(1080)
        val cacheKey = "${file.absolutePath}:${file.lastModified()}:$pageIndex:$width"
        bitmapCache.get(cacheKey)?.let { cached ->
            val count = pageCount(file)
            return@withContext RenderedPdfPage(cached, pageIndex, count)
        }

        ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY).use { descriptor ->
            PdfRenderer(descriptor).use { renderer ->
                val safePage = pageIndex.coerceIn(0, renderer.pageCount - 1)
                renderer.openPage(safePage).use { page ->
                    val height = (width * (page.height.toFloat() / page.width.toFloat())).toInt().coerceAtLeast(1)
                    val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
                    bitmap.eraseColor(Color.WHITE)
                    val matrix = Matrix().apply {
                        setScale(width / page.width.toFloat(), height / page.height.toFloat())
                    }
                    page.render(bitmap, null, matrix, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    bitmapCache.put(cacheKey, bitmap)
                    RenderedPdfPage(bitmap, safePage, renderer.pageCount)
                }
            }
        }
    }
}
