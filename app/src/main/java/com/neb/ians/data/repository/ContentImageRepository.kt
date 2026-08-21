package com.neb.ians.data.repository

import android.content.Context
import android.graphics.BitmapFactory
import android.net.Uri
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.InlineImageUploadResponse
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject
import javax.inject.Singleton

/** Max bytes accepted by the backend for one inline image. */
const val INLINE_IMAGE_MAX_BYTES = 10L * 1024 * 1024

/**
 * Uploads inline text-image chips (Meta-style `[[img:ID]]` tokens) to
 * `/api/content-images/upload/`. The server normalises to WebP, derives
 * deterministic media URLs from the row id and deduplicates by content hash.
 */
@Singleton
class ContentImageRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    @ApplicationContext private val appContext: Context
) {
    /** Image dimensions without decoding pixels (for chip aspect ratio). */
    fun decodeBounds(uri: Uri): Pair<Int, Int>? {
        return runCatching {
            val opts = BitmapFactory.Options().apply { inJustDecodeBounds = true }
            appContext.contentResolver.openInputStream(uri)?.use { stream ->
                BitmapFactory.decodeStream(stream, null, opts)
            }
            if (opts.outWidth <= 0 || opts.outHeight <= 0) null
            else opts.outWidth to opts.outHeight
        }.getOrNull()
    }

    fun sizeOf(uri: Uri): Long {
        return try {
            appContext.contentResolver.openAssetFileDescriptor(uri, "r")?.use { it.length } ?: -1L
        } catch (_: Exception) {
            -1L
        }
    }

    suspend fun upload(uri: Uri): Result<InlineImageUploadResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val token = authRepository.getBearerToken()
                    ?: return@withContext Result.failure(IllegalStateException("Not authenticated"))

                val size = sizeOf(uri)
                if (size > INLINE_IMAGE_MAX_BYTES) {
                    return@withContext Result.failure(IllegalStateException("Image too large (max 10MB)"))
                }

                val bytes = appContext.contentResolver.openInputStream(uri)?.use { it.readBytes() }
                    ?: return@withContext Result.failure(IllegalStateException("Couldn't read image"))

                if (bytes.size > INLINE_IMAGE_MAX_BYTES) {
                    return@withContext Result.failure(IllegalStateException("Image too large (max 10MB)"))
                }

                val mime = appContext.contentResolver.getType(uri)?.takeIf { it.startsWith("image/") } ?: "image/jpeg"
                val extension = when (mime) {
                    "image/png" -> "png"
                    "image/webp" -> "webp"
                    "image/gif" -> "gif"
                    else -> "jpg"
                }
                val part = MultipartBody.Part.createFormData(
                    name = "image",
                    filename = "inline_$extension.$extension",
                    body = bytes.toRequestBody(mime.toMediaType())
                )
                val response = apiService.uploadContentImage(token, part)
                if (response.id > 0) {
                    Result.success(response)
                } else {
                    Result.failure(IllegalStateException(response.error ?: "Upload failed"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }
}
