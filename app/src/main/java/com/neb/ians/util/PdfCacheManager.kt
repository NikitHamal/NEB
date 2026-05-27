package com.neb.ians.util

import android.content.Context
import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.net.URL

class PdfCacheManager(private val context: Context) {
    private val cacheDir = File(context.filesDir, "pdfs").apply { mkdirs() }

    fun getCachedFile(uriString: String): File? {
        val name = uriString.hashCode().toString() + ".pdf"
        val file = File(cacheDir, name)
        return if (file.exists()) file else null
    }

    suspend fun downloadAndCache(uriString: String): File? = withContext(Dispatchers.IO) {
        try {
            val name = uriString.hashCode().toString() + ".pdf"
            val file = File(cacheDir, name)
            if (file.exists()) return@withContext file
            URL(uriString).openStream().use { input ->
                FileOutputStream(file).use { output -> input.copyTo(output) }
            }
            file
        } catch (_: Exception) {
            null
        }
    }

    fun openRenderer(file: File): PdfRenderer? {
        return try {
            val pfd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
            PdfRenderer(pfd)
        } catch (_: Exception) {
            null
        }
    }
}
