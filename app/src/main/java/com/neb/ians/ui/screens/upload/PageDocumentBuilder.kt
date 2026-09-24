package com.neb.ians.ui.screens.upload

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Matrix
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream

/**
 * Turns a stack of page photos into one PDF.
 *
 * Someone who has just photographed sixty pages of notes has made one document,
 * not sixty images, and the library should receive it that way. Each photo is
 * downscaled, straightened by its EXIF rotation, encoded once as JPEG and then
 * embedded verbatim as a DCTDecode image — so a sixty page set lands around a
 * few hundred kilobytes per page instead of the several megabytes a bitmap
 * canvas would write, which is the difference between uploading and not.
 */
object PageDocumentBuilder {

    private const val MAX_EDGE = 1800
    private const val JPEG_QUALITY = 76
    private const val PAGE_WIDTH_PT = 595f

    private val IMAGE_EXTENSIONS = setOf("jpg", "jpeg", "png", "webp", "heic", "heif", "bmp")

    fun isImage(context: Context, uri: Uri, name: String): Boolean {
        val mime = runCatching { context.contentResolver.getType(uri) }.getOrNull()
        if (!mime.isNullOrBlank()) return mime.startsWith("image/")
        return name.substringAfterLast('.', "").lowercase() in IMAGE_EXTENSIONS
    }

    /**
     * Writes [pages] into a single PDF at [destination].
     *
     * Pages that cannot be read are skipped rather than failing the upload —
     * losing one blurred photo is recoverable, losing the whole set is not.
     * [onPage] reports how many pages have been prepared so the screen can say
     * something truthful while it waits. Returns null when nothing was readable.
     */
    suspend fun combine(
        context: Context,
        pages: List<Uri>,
        destination: File,
        onPage: (Int) -> Unit = {}
    ): File? = withContext(Dispatchers.IO) {
        val scratch = File(context.cacheDir, "page_build").apply { mkdirs() }
        val prepared = mutableListOf<PreparedPage>()
        try {
            pages.forEachIndexed { index, uri ->
                prepare(context, uri, File(scratch, "page_$index.jpg"))?.let { prepared += it }
                onPage(index + 1)
            }
            if (prepared.isEmpty()) return@withContext null
            destination.parentFile?.mkdirs()
            CountingStream(BufferedOutputStream(FileOutputStream(destination))).use { out ->
                writeDocument(out, prepared)
            }
            destination
        } catch (_: Exception) {
            destination.delete()
            null
        } finally {
            prepared.forEach { it.jpeg.delete() }
            scratch.delete()
        }
    }

    private class PreparedPage(val jpeg: File, val width: Int, val height: Int)

    private fun prepare(context: Context, uri: Uri, target: File): PreparedPage? {
        val bitmap = decodeScaled(context, uri) ?: return null
        return try {
            FileOutputStream(target).use { bitmap.compress(Bitmap.CompressFormat.JPEG, JPEG_QUALITY, it) }
            if (target.length() <= 0L) null else PreparedPage(target, bitmap.width, bitmap.height)
        } catch (_: Exception) {
            null
        } finally {
            bitmap.recycle()
        }
    }

    private fun decodeScaled(context: Context, uri: Uri): Bitmap? {
        val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
        runCatching {
            context.contentResolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, bounds) }
        }.getOrNull()
        if (bounds.outWidth <= 0 || bounds.outHeight <= 0) return null

        var sample = 1
        while (maxOf(bounds.outWidth, bounds.outHeight) / sample > MAX_EDGE * 2) sample *= 2
        val options = BitmapFactory.Options().apply { inSampleSize = sample }
        val decoded = runCatching {
            context.contentResolver.openInputStream(uri)?.use { BitmapFactory.decodeStream(it, null, options) }
        }.getOrNull() ?: return null

        val rotation = exifRotation(context, uri)
        val longEdge = maxOf(decoded.width, decoded.height)
        val scale = if (longEdge > MAX_EDGE) MAX_EDGE.toFloat() / longEdge else 1f
        if (scale == 1f && rotation == 0f) return decoded

        val matrix = Matrix().apply {
            if (scale != 1f) postScale(scale, scale)
            if (rotation != 0f) postRotate(rotation)
        }
        return try {
            val transformed = Bitmap.createBitmap(decoded, 0, 0, decoded.width, decoded.height, matrix, true)
            if (transformed != decoded) decoded.recycle()
            transformed
        } catch (_: Exception) {
            decoded
        }
    }

    @Suppress("DEPRECATION")
    private fun exifRotation(context: Context, uri: Uri): Float = try {
        context.contentResolver.openInputStream(uri)?.use { stream ->
            when (
                android.media.ExifInterface(stream).getAttributeInt(
                    android.media.ExifInterface.TAG_ORIENTATION,
                    android.media.ExifInterface.ORIENTATION_NORMAL
                )
            ) {
                android.media.ExifInterface.ORIENTATION_ROTATE_90 -> 90f
                android.media.ExifInterface.ORIENTATION_ROTATE_180 -> 180f
                android.media.ExifInterface.ORIENTATION_ROTATE_270 -> 270f
                else -> 0f
            }
        } ?: 0f
    } catch (_: Exception) {
        0f
    }

    // -- PDF container -------------------------------------------------------
    //
    // Objects are laid out catalog, page tree, then three objects per page, so
    // every object number is known before anything is written and the file can
    // stream straight to disk.

    private fun writeDocument(out: CountingStream, pages: List<PreparedPage>) {
        val offsets = mutableListOf<Long>()

        fun beginObject(number: Int) {
            offsets += out.count
            out.ascii("$number 0 obj\n")
        }

        out.ascii("%PDF-1.4\n%âãÏÓ\n")

        beginObject(1)
        out.ascii("<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

        beginObject(2)
        val kids = pages.indices.joinToString(" ") { "${3 + it * 3} 0 R" }
        out.ascii("<< /Type /Pages /Kids [$kids] /Count ${pages.size} >>\nendobj\n")

        pages.forEachIndexed { index, page ->
            val pageNumber = 3 + index * 3
            val imageNumber = pageNumber + 1
            val contentNumber = pageNumber + 2
            val widthPt = PAGE_WIDTH_PT
            val heightPt = PAGE_WIDTH_PT * page.height / page.width

            beginObject(pageNumber)
            out.ascii(
                "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${widthPt.pt()} ${heightPt.pt()}] " +
                    "/Resources << /XObject << /Im0 $imageNumber 0 R >> >> /Contents $contentNumber 0 R >>\nendobj\n"
            )

            beginObject(imageNumber)
            out.ascii(
                "<< /Type /XObject /Subtype /Image /Width ${page.width} /Height ${page.height} " +
                    "/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${page.jpeg.length()} >>\nstream\n"
            )
            page.jpeg.inputStream().use { it.copyTo(out) }
            out.ascii("\nendstream\nendobj\n")

            val content = "q ${widthPt.pt()} 0 0 ${heightPt.pt()} 0 0 cm /Im0 Do Q\n"
            beginObject(contentNumber)
            out.ascii("<< /Length ${content.length} >>\nstream\n$content" + "endstream\nendobj\n")
        }

        val xrefOffset = out.count
        out.ascii("xref\n0 ${offsets.size + 1}\n")
        out.ascii("0000000000 65535 f \n")
        offsets.forEach { out.ascii(String.format("%010d 00000 n \n", it)) }
        out.ascii("trailer\n<< /Size ${offsets.size + 1} /Root 1 0 R >>\nstartxref\n$xrefOffset\n%%EOF\n")
        out.flush()
    }

    private fun Float.pt(): String = String.format("%.2f", this)

    private class CountingStream(private val delegate: OutputStream) : OutputStream() {
        var count: Long = 0L
            private set

        override fun write(b: Int) {
            delegate.write(b)
            count++
        }

        override fun write(b: ByteArray, off: Int, len: Int) {
            delegate.write(b, off, len)
            count += len
        }

        override fun flush() = delegate.flush()
        override fun close() = delegate.close()

        fun ascii(text: String) {
            val bytes = ByteArray(text.length) { text[it].code.toByte() }
            write(bytes, 0, bytes.size)
        }
    }
}
