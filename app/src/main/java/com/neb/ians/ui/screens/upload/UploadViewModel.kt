package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResourceUploadResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.api.ApiErrorMapper
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import java.io.FileOutputStream
import javax.inject.Inject

private val TEXT_PLAIN: okhttp3.MediaType? = "text/plain".toMediaTypeOrNull()

data class UploadFormState(
    val title: String = "",
    val subject: String = "",
    val description: String = "",
    val gradeLevel: String = "",
    val type: String = "PDF",
    val examType: String = "",
    val faculty: String = "",
    val program: String = "",
    val year: String = "",
    val school: String = "",
    val pradesh: String = "",
    val district: String = "",
    val tags: String = "",
    val fileUrl: String = "",
    val thumbnailUrl: String = "",
    val thumbnailUri: Uri? = null,
    val authorName: String = "",
    val sourceLabel: String = "",
    val sourceUrl: String = "",
    val selectedFiles: List<SelectedFile> = emptyList(),
    val titleError: String? = null,
    val subjectError: String? = null,
    val fileError: String? = null,
    val isSubmitting: Boolean = false,
    val uploadProgress: Float = 0f,
    val submitError: String? = null,
    val submitSuccess: Boolean = false,
    // ----- Edit mode (same wizard, PATCH instead of POST) -----
    val isEditMode: Boolean = false,
    val editLoading: Boolean = false,
    val editLoadError: String? = null,
    /** True when the signed-in user is not the uploader (edit is owner-only). */
    val notAllowed: Boolean = false,
    val editSuccess: Boolean = false,
    val approvalStatus: String? = null,
    /** Display label for the file/link currently stored on the server. */
    val currentFileLabel: String = "",
    /** Only sent when the user actually edits the link (blank never destroys an upload). */
    val fileUrlDirty: Boolean = false,
    /** Cover changes only PATCH when the user touched the URL or picked a new image. */
    val thumbnailDirty: Boolean = false
)

data class SelectedFile(
    val uri: Uri,
    val name: String,
    val size: Long
)

@HiltViewModel
class UploadViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val resourceRepository: ResourceRepository
) : ViewModel() {

    /** Present when the wizard was opened as an edit (owner editing own resource). */
    private val editResourceId: String? = savedStateHandle.get<String>("resourceId")?.takeIf { it.isNotBlank() }

    private val _uiState = MutableStateFlow(UploadFormState())
    val uiState: StateFlow<UploadFormState> = _uiState.asStateFlow()

    init {
        editResourceId?.let { loadEditResource(it) }
    }

    /** Prefill the wizard with everything the existing resource stores. */
    fun loadEditResource(resourceId: String = editResourceId ?: return) {
        viewModelScope.launch {
            _uiState.update { it.copy(isEditMode = true, editLoading = true, editLoadError = null) }
            val username = try { authRepository.currentUsernameHandleFlow.first() } catch (_: Exception) { "" }
            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    val owner = resource.uploadedByUsername.isNotBlank() &&
                        username.isNotBlank() &&
                        resource.uploadedByUsername.equals(username, ignoreCase = true)
                    if (!owner) {
                        _uiState.update { it.copy(editLoading = false, notAllowed = true) }
                        return@onSuccess
                    }
                    _uiState.update {
                        it.copy(
                            editLoading = false,
                            approvalStatus = resource.approvalStatus,
                            currentFileLabel = resource.fileUrl.substringAfterLast('/')
                                .ifBlank { resource.type.ifBlank { "Link" } },
                            title = resource.title,
                            subject = resource.subject,
                            description = resource.description,
                            gradeLevel = resource.gradeLevel,
                            type = resource.type.ifBlank { "PDF" },
                            examType = resource.examType,
                            faculty = resource.faculty,
                            program = resource.program,
                            year = resource.year,
                            school = resource.school,
                            pradesh = resource.pradesh,
                            district = resource.district,
                            tags = resource.tags,
                            fileUrl = resource.fileUrl,
                            thumbnailUrl = resource.thumbnailUrl,
                            authorName = resource.authorName ?: "",
                            sourceLabel = resource.sourceLabel ?: "",
                            sourceUrl = resource.sourceUrl ?: "",
                            fileUrlDirty = false,
                            thumbnailDirty = false
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(editLoading = false, editLoadError = ApiErrorMapper.mapException(e))
                    }
                }
        }
    }

    companion object {
        val VIDEO_EXTENSIONS = setOf("mp4", "mkv", "mov", "webm", "avi", "m4v", "3gp", "wmv", "flv")

        fun isVideoFileName(name: String): Boolean =
            name.substringAfterLast('.', "").lowercase() in VIDEO_EXTENSIONS

        val SUBJECTS = listOf(
            "Accountancy", "Biology", "Chemistry", "Computer Science", "Economics",
            "English", "Exam Tips", "Mathematics", "Microbiology", "Nepali",
            "Physics", "Physics - Technical Stream", "Science", "Social Studies",
            "Software Engineering", "Software Engineering and Project Management",
            "Visual Programming", "Zoology", "सामाजिक अध्ययन"
        )
        val GRADE_LEVELS = listOf(
            "Bachelor", "Class 10 / SEE", "Class 11", "Class 12", "Class 8",
            "Entrance Prep", "Other"
        )
        val RESOURCE_TYPES = listOf(
            "PDF", "Note", "Video", "Audio", "Image", "Link", "Textbook",
            "Past Paper", "Model Paper", "Guide", "Solution", "Presentation"
        )
        val EXAM_TYPES = listOf(
            "Final", "Midterm", "Board", "Entrance", "SEE", "Mock", "Assignment", "Notes", "Reference", "Other"
        )
        val PROVINCES = listOf(
            "Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"
        )
        val COMMON_TAGS = listOf(
            "NEB", "SEE", "Class 11", "Class 12", "Important Questions",
            "Past Paper", "Notes", "Solution", "Guide", "Textbook",
            "Formula", "Practical", "Project", "Tips", "Revision"
        )
        val MAX_FILE_SIZE = 50L * 1024 * 1024
        val MAX_FILES = 5
    }

    fun updateTitle(title: String) {
        _uiState.update { it.copy(title = title, titleError = null) }
    }

    fun updateSubject(subject: String) {
        _uiState.update { it.copy(subject = subject, subjectError = null) }
    }

    fun updateDescription(description: String) {
        _uiState.update { it.copy(description = description) }
    }

    fun updateGradeLevel(gradeLevel: String) {
        _uiState.update { it.copy(gradeLevel = gradeLevel) }
    }

    fun updateType(type: String) {
        _uiState.update { it.copy(type = type) }
    }

    fun updateExamType(examType: String) {
        _uiState.update { it.copy(examType = examType) }
    }

    fun updateFaculty(faculty: String) {
        _uiState.update { it.copy(faculty = faculty) }
    }

    fun updateProgram(program: String) {
        _uiState.update { it.copy(program = program) }
    }

    fun updateYear(year: String) {
        _uiState.update { it.copy(year = year) }
    }

    fun updateSchool(school: String) {
        _uiState.update { it.copy(school = school) }
    }

    fun updatePradesh(pradesh: String) {
        _uiState.update { it.copy(pradesh = pradesh) }
    }

    fun updateDistrict(district: String) {
        _uiState.update { it.copy(district = district) }
    }

    fun updateTags(tags: String) {
        _uiState.update { it.copy(tags = tags) }
    }

    fun updateFileUrl(fileUrl: String) {
        _uiState.update { it.copy(fileUrl = fileUrl, fileError = null, fileUrlDirty = it.isEditMode || it.fileUrlDirty) }
    }

    fun setFileError(message: String?) {
        _uiState.update { it.copy(fileError = message) }
    }

    fun updateThumbnailUrl(thumbnailUrl: String) {
        _uiState.update { it.copy(thumbnailUrl = thumbnailUrl, thumbnailDirty = it.isEditMode || it.thumbnailDirty) }
    }

    /** Manually picked cover image (overrides the auto video frame). */
    fun setThumbnail(uri: Uri?) {
        _uiState.update { it.copy(thumbnailUri = uri, thumbnailDirty = it.isEditMode || it.thumbnailDirty) }
    }

    /** Videos get a cover frame captured automatically — used for UI hints. */
    fun hasAutoCoverCandidate(): Boolean {
        val state = _uiState.value
        return state.thumbnailUri == null &&
            state.thumbnailUrl.isBlank() &&
            state.selectedFiles.any { isVideoFileName(it.name) }
    }

    fun updateAuthorName(authorName: String) {
        _uiState.update { it.copy(authorName = authorName) }
    }

    fun updateSourceLabel(sourceLabel: String) {
        _uiState.update { it.copy(sourceLabel = sourceLabel) }
    }

    fun updateSourceUrl(sourceUrl: String) {
        _uiState.update { it.copy(sourceUrl = sourceUrl) }
    }

    fun addFiles(files: List<SelectedFile>) {
        // Edit mode replaces the single stored file — only the first pick counts.
        if (_uiState.value.isEditMode) {
            val replacement = files.firstOrNull() ?: return
            _uiState.update { it.copy(selectedFiles = listOf(replacement), fileError = null) }
            return
        }
        val current = _uiState.value.selectedFiles
        val newFiles = files.filterNot { f -> current.any { it.name == f.name && it.size == f.size } }
        if (current.size + newFiles.size > MAX_FILES) return
        _uiState.update { it.copy(selectedFiles = current + newFiles, fileError = null) }
    }

    fun removeFileAt(index: Int) {
        val current = _uiState.value.selectedFiles
        if (index in current.indices) {
            _uiState.update { it.copy(selectedFiles = current.toMutableList().apply { removeAt(index) }) }
        }
    }

    fun clearFiles() {
        _uiState.update { it.copy(selectedFiles = emptyList()) }
    }

    fun submit(context: Context) {
        val state = _uiState.value
        var hasError = false

        if (state.title.isBlank()) {
            _uiState.update { it.copy(titleError = "Title is required") }
            hasError = true
        }
        if (state.subject.isBlank()) {
            _uiState.update { it.copy(subjectError = "Subject is required") }
            hasError = true
        }
        // Edit mode keeps the stored file unless a replacement/link is provided.
        if (!state.isEditMode && state.selectedFiles.isEmpty() && state.fileUrl.isBlank()) {
            _uiState.update { it.copy(fileError = "Please upload a file or provide a file URL") }
            hasError = true
        }
        if (hasError) return

        if (state.isEditMode) {
            submitEdit(context, state)
            return
        }

        _uiState.update { it.copy(isSubmitting = true, submitError = null, uploadProgress = 0f) }

        viewModelScope.launch {
            try {
                val token = authRepository.getToken()
                if (token.isNullOrBlank()) {
                    _uiState.update { it.copy(isSubmitting = false, submitError = "Please sign in to upload resources") }
                    return@launch
                }
                val bearerToken = "Bearer $token"

                val files = state.selectedFiles
                if (files.isNotEmpty()) {
                    uploadMultipleFiles(context, bearerToken, files, state)
                } else {
                    uploadWithUrl(context, bearerToken, state)
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    /** Edit mode submit — one multipart PATCH covering everything the wizard can set. */
    private fun submitEdit(context: Context, state: UploadFormState) {
        val resourceId = editResourceId ?: return
        _uiState.update { it.copy(isSubmitting = true, submitError = null, uploadProgress = 0f) }
        viewModelScope.launch {
            try {
                val fields = linkedMapOf<String, RequestBody>(
                    "title" to state.title.toRequestBody(TEXT_PLAIN),
                    "subject" to state.subject.toRequestBody(TEXT_PLAIN),
                    "description" to state.description.toRequestBody(TEXT_PLAIN),
                    "grade_level" to state.gradeLevel.toRequestBody(TEXT_PLAIN),
                    "type" to state.type.ifBlank { "PDF" }.toRequestBody(TEXT_PLAIN),
                    "exam_type" to state.examType.toRequestBody(TEXT_PLAIN),
                    "faculty" to state.faculty.toRequestBody(TEXT_PLAIN),
                    "program" to state.program.toRequestBody(TEXT_PLAIN),
                    "year" to state.year.toRequestBody(TEXT_PLAIN),
                    "school" to state.school.toRequestBody(TEXT_PLAIN),
                    "pradesh" to state.pradesh.toRequestBody(TEXT_PLAIN),
                    "district" to state.district.toRequestBody(TEXT_PLAIN),
                    "tags" to state.tags.toRequestBody(TEXT_PLAIN),
                    "author_name" to state.authorName.toRequestBody(TEXT_PLAIN),
                    "source_label" to state.sourceLabel.toRequestBody(TEXT_PLAIN),
                    "source_url" to state.sourceUrl.toRequestBody(TEXT_PLAIN)
                )
                // Link: only PATCH when edited — a blank untouched field must never wipe an upload.
                if (state.fileUrlDirty) fields["file_url"] = state.fileUrl.toRequestBody(TEXT_PLAIN)
                // Cover: manual upload wins; then a fresh URL; a cleared URL removes the cover.
                if (state.thumbnailDirty) fields["thumbnail_url"] = state.thumbnailUrl.toRequestBody(TEXT_PLAIN)

                val replacement = state.selectedFiles.firstOrNull()
                val filePart = replacement?.let { selected ->
                    val file = uriToFile(context, selected.uri, selected.name)
                        ?: throw IllegalStateException("Couldn't read the selected file")
                    MultipartBody.Part.createFormData("file", file.name, file.asRequestBody(contentTypeFromName(file.name)))
                }
                val thumbnailPart = state.thumbnailUri?.let { uri ->
                    buildThumbnailPart(context, uri, "cover")
                }

                resourceRepository.updateResource(
                    resourceId = resourceId,
                    fields = fields,
                    filePart = filePart,
                    thumbnailPart = thumbnailPart
                ).onSuccess {
                    _uiState.update { it.copy(isSubmitting = false, uploadProgress = 1f, editSuccess = true) }
                }.onFailure { e ->
                    _uiState.update {
                        it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapException(e))
                    }
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapException(e))
                }
            }
        }
    }

    private suspend fun uploadMultipleFiles(
        context: Context,
        bearerToken: String,
        files: List<SelectedFile>,
        state: UploadFormState
    ) {
        val totalFiles = files.size
        for ((index, selectedFile) in files.withIndex()) {
            val file = uriToFile(context, selectedFile.uri, selectedFile.name) ?: continue
            val requestBody = file.asRequestBody(contentTypeFromName(file.name))
            val multipartPart = MultipartBody.Part.createFormData("file", file.name, requestBody)

            // Cover image: manual pick wins; videos get an auto frame when the
            // user supplied neither an upload nor a URL.
            val thumbnailPart = when {
                state.thumbnailUri != null -> buildThumbnailPart(context, state.thumbnailUri, "cover")
                state.thumbnailUrl.isBlank() && isVideoFileName(selectedFile.name) ->
                    videoFrameThumbnailPart(context, selectedFile.uri, selectedFile.name)
                else -> null
            }

            val response = apiService.uploadResource(
                bearerToken = bearerToken,
                file = multipartPart,
                thumbnail = thumbnailPart,
                title = state.title.toRequestBody(TEXT_PLAIN),
                subject = state.subject.toRequestBody(TEXT_PLAIN),
                description = (state.description.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                gradeLevel = (state.gradeLevel.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                type = (state.type.takeIf { it.isNotBlank() } ?: "PDF").toRequestBody(TEXT_PLAIN),
                examType = (state.examType.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                faculty = (state.faculty.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                program = (state.program.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                year = (state.year.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                school = (state.school.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                pradesh = (state.pradesh.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                district = (state.district.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                tags = (state.tags.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                fileUrl = null,
                thumbnailUrl = (state.thumbnailUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                authorName = (state.authorName.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                sourceLabel = (state.sourceLabel.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                sourceUrl = (state.sourceUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN)
            )

            if (response.error != null) {
                _uiState.update { it.copy(isSubmitting = false, submitError = response.error) }
                return
            }

            _uiState.update { it.copy(uploadProgress = (index + 1).toFloat() / totalFiles) }
        }
        _uiState.update { it.copy(isSubmitting = false, submitSuccess = true) }
    }

    private suspend fun uploadWithUrl(
        context: Context,
        bearerToken: String,
        state: UploadFormState
    ) {
        val thumbnailPart = state.thumbnailUri?.let { buildThumbnailPart(context, it, "cover") }
        val response = apiService.uploadResource(
            bearerToken = bearerToken,
            file = null,
            thumbnail = thumbnailPart,
            title = state.title.toRequestBody(TEXT_PLAIN),
            subject = state.subject.toRequestBody(TEXT_PLAIN),
            description = (state.description.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            gradeLevel = (state.gradeLevel.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            type = (state.type.takeIf { it.isNotBlank() } ?: "PDF").toRequestBody(TEXT_PLAIN),
            examType = (state.examType.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            faculty = (state.faculty.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            program = (state.program.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            year = (state.year.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            school = (state.school.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            pradesh = (state.pradesh.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            district = (state.district.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            tags = (state.tags.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            fileUrl = state.fileUrl.toRequestBody(TEXT_PLAIN),
            thumbnailUrl = (state.thumbnailUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            authorName = (state.authorName.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            sourceLabel = (state.sourceLabel.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            sourceUrl = (state.sourceUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN)
        )

        if (response.error != null) {
            _uiState.update { it.copy(isSubmitting = false, submitError = response.error) }
        } else {
            _uiState.update { it.copy(isSubmitting = false, submitSuccess = true) }
        }
    }

    fun resetSuccess() {
        _uiState.update { it.copy(submitSuccess = false, submitError = null) }
    }

    private fun uriToFile(context: Context, uri: Uri, fileName: String): File? {
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
    private fun buildThumbnailPart(context: Context, uri: Uri, baseName: String): MultipartBody.Part? {
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
    private fun videoFrameThumbnailPart(context: Context, videoUri: Uri, baseName: String): MultipartBody.Part? {
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

    private fun contentTypeFromName(name: String): okhttp3.MediaType? {
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