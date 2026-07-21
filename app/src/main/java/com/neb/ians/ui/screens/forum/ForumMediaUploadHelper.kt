package com.neb.ians.ui.screens.forum

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import com.neb.ians.data.api.ApiMediaAttachmentInput
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

/** One attachment being staged in a composer (upload-in-flight or done). */
data class PendingForumAttachment(
    val localId: String = UUID.randomUUID().toString(),
    val name: String,
    val kind: String,             // "video" | "audio" | "file"
    val sizeBytes: Long,
    val uri: Uri,
    val uploading: Boolean = true,
    val uploaded: ApiMediaAttachmentInput? = null,
    val error: String? = null,
    val durationMs: Long = 0      // voice notes: recorded length for the preview chip
)

/**
 * Shared helpers for staging forum media attachments (posts + replies):
 * kind/size/name detection from the picked [Uri] and the actual upload to
 * /api/forum/uploads/, whose descriptor the composer echoes back inside the
 * post/reply create payload.
 */
@Singleton
class ForumMediaUploadHelper @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val forumRepository: ForumRepository
) {
    companion object {
        const val MAX_ATTACHMENTS = 4
        const val MAX_VIDEO_BYTES = 150L * 1024 * 1024
        const val MAX_AUDIO_BYTES = 40L * 1024 * 1024
        const val MAX_FILE_BYTES = 30L * 1024 * 1024

        fun limitFor(kind: String): Long = when (kind) {
            "video" -> MAX_VIDEO_BYTES
            "audio" -> MAX_AUDIO_BYTES
            else -> MAX_FILE_BYTES
        }

        fun limitLabel(kind: String): String = when (kind) {
            "video" -> "Videos are limited to 150 MB"
            "audio" -> "Audio is limited to 40 MB"
            else -> "Attachments are limited to 30 MB"
        }
    }

    fun guessKind(uri: Uri): String {
        val mime = (appContext.contentResolver.getType(uri) ?: "").lowercase()
        if (mime.startsWith("video/")) return "video"
        if (mime.startsWith("audio/")) return "audio"
        val ext = displayName(uri).substringAfterLast('.', "").lowercase()
        return when (ext) {
            "mp4", "m4v", "webm", "mov" -> "video"
            "mp3", "m4a", "aac", "ogg", "opus", "wav", "flac" -> "audio"
            else -> "file"
        }
    }

    fun displayName(uri: Uri): String {
        try {
            appContext.contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                val idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                if (idx >= 0 && cursor.moveToFirst()) {
                    val name = cursor.getString(idx)
                    if (!name.isNullOrBlank()) return name
                }
            }
        } catch (_: Exception) {}
        return uri.lastPathSegment?.substringAfterLast('/') ?: "attachment"
    }

    fun sizeOf(uri: Uri): Long {
        try {
            appContext.contentResolver.openAssetFileDescriptor(uri, "r")?.use { fd ->
                if (fd.length > 0) return fd.length
            }
        } catch (_: Exception) {}
        return 0L
    }

    /**
     * Multipart filename the server sees. Composer display names like
     * "Voice note (0:07)" carry no extension — and the server classes
     * attachments BY extension, so an extensionless name was a guaranteed
     * HTTP 400. Fall back to the picked file's real extension, then to a
     * kind-appropriate default.
     */
    private fun uploadFileName(name: String, uri: Uri, kind: String): String {
        val trimmed = name.trim().ifBlank { "attachment" }
        if (trimmed.substringAfterLast('.', "").length != trimmed.length) {
            // Has a dot-suffix — trust it (picked files keep real names).
            if (trimmed.substringAfterLast('.').length in 2..5) return trimmed
        }
        val ext = displayName(uri).substringAfterLast('.', "").lowercase()
            .takeIf { it.length in 2..5 }
            ?: when (kind) {
                "video" -> "mp4"
                "audio" -> "m4a"
                else -> "bin"
            }
        return "$trimmed.$ext"
    }

    /** Uploads one file; the returned descriptor goes into the create payload. */
    suspend fun upload(uri: Uri, kind: String, name: String): Result<ApiMediaAttachmentInput> {
        val bytes = withContext(Dispatchers.IO) {
            try {
                appContext.contentResolver.openInputStream(uri)?.use { it.readBytes() }
            } catch (_: Exception) {
                null
            }
        } ?: return Result.failure(IllegalStateException("Couldn't read $name"))

        val limit = limitFor(kind)
        if (bytes.size > limit) return Result.failure(IllegalStateException(limitLabel(kind)))

        val mime = (appContext.contentResolver.getType(uri) ?: when (kind) {
            "video" -> "video/mp4"
            "audio" -> "audio/mp4"
            else -> "application/octet-stream"
        })
        val part = MultipartBody.Part.createFormData(
            "file",
            uploadFileName(name, uri, kind),
            bytes.toRequestBody(mime.toMediaType())
        )
        // Audio note recordings live in mp4/m4a/webm containers — tell the
        // server to keep them classed as audio (it preserves the audio mime).
        val kindHint = if (kind == "audio") "audio" else null
        return forumRepository.uploadForumMedia(part, kindHint)
    }
}
