package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import java.io.FileOutputStream

/**
 * Reading what the user picked.
 *
 * Content URIs, cover images and mime types — the part of uploading that is
 * about the device rather than about the resource.
 */
object UploadMedia {

    fun uriToFile(context: Context, uri: Uri, fileName: String): File? {
        return try {
            val tempFile = File(context.cacheDir, fileName)
            context.contentResolver.openInputStream(uri)?.use { input ->
                FileOutputStream(tempFile).use { output -> input.copyTo(output) }
            }
            tempFile
        } catch (e: Exception) {
            null
        }
    }

    /** Build the "thumbnail" multipart part from a user-picked cover image. */
    fun buildThumbnailPart(context: Context, uri: Uri, baseName: String): MultipartBody.Part? {
        return try {
            val bytes = context.contentResolver.openInputStream(uri)?.use { it.readBytes() } ?: return null
            if (bytes.isEmpty() || bytes.size > 10L * 1024 * 1024) return null
            val mime = context.contentResolver.getType(uri) ?: "image/jpeg"
            val ext = when (mime) {
                "image/png" -> "png"
                "image/webp" -> "webp"
                "image/gif" -> "gif"
                else -> "jpg"
            }
            MultipartBody.Part.createFormData("thumbnail", "$baseName.$ext", bytes.toRequestBody(mime.toMediaTypeOrNull()))
        } catch (_: Exception) {
            null
        }
    }

    /** Capture a frame (~1s in, fallback first frame) from a picked video as
     * the resource cover. Returns null on any failure — never blocks upload. */
    fun videoFrameThumbnailPart(context: Context, videoUri: Uri, baseName: String): MultipartBody.Part? {
        return try {
            val retriever = android.media.MediaMetadataRetriever()
            val rawBitmap = try {
                retriever.setDataSource(context, videoUri)
                retriever.getFrameAtTime(1_000_000L, android.media.MediaMetadataRetriever.OPTION_CLOSEST_SYNC)
                    ?: retriever.frameAtTime
                        ?: retriever.getFrameAtTime(0L, android.media.MediaMetadataRetriever.OPTION_CLOSEST_SYNC)
            } catch (_: Exception) {
                null
            } finally {
                try { retriever.release() } catch (_: Exception) {}
            } ?: return null
            var bitmap: android.graphics.Bitmap = rawBitmap
            // Keep covers small — 1280px on the long edge is plenty for cards.
            val maxDim = 1280
            if (maxOf(bitmap.width, bitmap.height) > maxDim) {
                val scale = maxDim.toFloat() / maxOf(bitmap.width, bitmap.height)
                val scaled = android.graphics.Bitmap.createScaledBitmap(
                    bitmap,
                    (bitmap.width * scale).toInt().coerceAtLeast(1),
                    (bitmap.height * scale).toInt().coerceAtLeast(1),
                    true
                )
                if (scaled != bitmap) bitmap.recycle()
                bitmap = scaled
            }
            val out = java.io.ByteArrayOutputStream()
            bitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 88, out)
            bitmap.recycle()
            val bytes = out.toByteArray()
            if (bytes.isEmpty()) return null
            MultipartBody.Part.createFormData(
                "thumbnail",
                "${baseName.substringBeforeLast('.')}_cover.jpg",
                bytes.toRequestBody("image/jpeg".toMediaTypeOrNull())
            )
        } catch (_: Exception) {
            null
        }
    }

    fun contentTypeFromName(name: String): okhttp3.MediaType? {
        val ext = name.substringAfterLast('.', "").lowercase()
        val mime = android.webkit.MimeTypeMap.getSingleton().getMimeTypeFromExtension(ext)
            ?: when (ext) {
                "pdf" -> "application/pdf"
                "doc" -> "application/msword"
                "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                "ppt" -> "application/vnd.ms-powerpoint"
                "pptx" -> "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                "xls" -> "application/vnd.ms-excel"
                "xlsx" -> "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                "zip" -> "application/zip"
                "rar" -> "application/x-rar-compressed"
                "7z" -> "application/x-7z-compressed"
                "epub" -> "application/epub+zip"
                else -> "application/octet-stream"
            }
        return mime.toMediaTypeOrNull()
    }
    fun getFileInfo(context: Context, uri: Uri): Pair<String, Long>? {
        return try {
            context.contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                val nameIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                val sizeIndex = cursor.getColumnIndex(OpenableColumns.SIZE)
                if (cursor.moveToFirst() && nameIndex >= 0) {
                    val name = cursor.getString(nameIndex)
                    val size = if (sizeIndex >= 0) cursor.getLong(sizeIndex) else 0L
                    Pair(name, size)
                } else null
            }
        } catch (e: Exception) {
            null
        }
    }
}
