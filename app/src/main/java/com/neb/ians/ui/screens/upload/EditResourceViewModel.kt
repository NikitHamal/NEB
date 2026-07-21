package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import androidx.compose.runtime.Immutable
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import javax.inject.Inject

private val EDIT_TEXT_PLAIN: okhttp3.MediaType? = "text/plain".toMediaTypeOrNull()

private fun String.rb(): RequestBody = toRequestBody(EDIT_TEXT_PLAIN)

@Immutable
data class EditResourceUiState(
    val isLoading: Boolean = true,
    val loadError: String? = null,
    /** True when the signed-in user is not the uploader (edit is owner-only). */
    val notAllowed: Boolean = false,
    val isSubmitting: Boolean = false,
    val submitted: Boolean = false,
    val submitError: String? = null,
    val approvalStatus: String? = null,
    val resourceType: String = "",
    val currentFileLabel: String = "",
    val currentThumbnailUrl: String = "",
    // form fields (prefilled from the resource; everything upload can set)
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
    val authorName: String = "",
    val sourceLabel: String = "",
    val sourceUrl: String = "",
    // link payload (only sent when the user actually changes it)
    val fileUrl: String = "",
    val fileUrlDirty: Boolean = false,
    // cover: picked upload beats URL; clearing URL removes the cover
    val thumbnailUrl: String = "",
    val thumbnailDirty: Boolean = false,
    val thumbnailUri: Uri? = null,
    val replaceFile: SelectedFile? = null
)

@HiltViewModel
class EditResourceViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""

    private val _uiState = MutableStateFlow(EditResourceUiState())
    val uiState: StateFlow<EditResourceUiState> = _uiState

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, loadError = null) }
            val username = try { authRepository.currentUsernameHandleFlow.first() } catch (_: Exception) { "" }
            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    val owner = resource.uploadedByUsername.isNotBlank() &&
                        username.isNotBlank() &&
                        resource.uploadedByUsername.equals(username, ignoreCase = true)
                    if (!owner) {
                        _uiState.update { it.copy(isLoading = false, notAllowed = true) }
                        return@onSuccess
                    }
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            approvalStatus = resource.approvalStatus,
                            resourceType = resource.type,
                            currentFileLabel = resource.fileUrl.substringAfterLast('/').ifBlank { resource.type },
                            currentThumbnailUrl = resource.thumbnailUrl,
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
                            authorName = resource.authorName ?: "",
                            sourceLabel = resource.sourceLabel ?: "",
                            sourceUrl = resource.sourceUrl ?: "",
                            fileUrl = resource.fileUrl,
                            thumbnailUrl = resource.thumbnailUrl
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(isLoading = false, loadError = ApiErrorMapper.mapException(e))
                    }
                }
        }
    }

    fun update(block: EditResourceUiState.() -> EditResourceUiState) = _uiState.update(block)

    fun setReplaceFile(file: SelectedFile?) = _uiState.update { it.copy(replaceFile = file) }

    fun setThumbnail(uri: Uri?) = _uiState.update {
        it.copy(thumbnailUri = uri, thumbnailDirty = uri != null || it.thumbnailDirty)
    }

    fun setThumbnailUrl(url: String) = _uiState.update {
        it.copy(thumbnailUrl = url, thumbnailDirty = true)
    }

    fun setFileUrl(url: String) = _uiState.update {
        it.copy(fileUrl = url, fileUrlDirty = true)
    }

    fun save(context: Context) {
        val state = _uiState.value
        if (state.isSubmitting) return
        if (state.title.isBlank() || state.subject.isBlank()) {
            _uiState.update { it.copy(submitError = "Title and subject are required") }
            return
        }
        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, submitError = null) }
            try {
                val fields = linkedMapOf(
                    "title" to state.title.rb(),
                    "subject" to state.subject.rb(),
                    "description" to state.description.rb(),
                    "grade_level" to state.gradeLevel.rb(),
                    "type" to (state.type.ifBlank { "PDF" }).rb(),
                    "exam_type" to state.examType.rb(),
                    "faculty" to state.faculty.rb(),
                    "program" to state.program.rb(),
                    "year" to state.year.rb(),
                    "school" to state.school.rb(),
                    "pradesh" to state.pradesh.rb(),
                    "district" to state.district.rb(),
                    "tags" to state.tags.rb(),
                    "author_name" to state.authorName.rb(),
                    "source_label" to state.sourceLabel.rb(),
                    "source_url" to state.sourceUrl.rb()
                )
                if (state.fileUrlDirty) fields["file_url"] = state.fileUrl.rb()
                if (state.thumbnailDirty) fields["thumbnail_url"] = state.thumbnailUrl.rb()

                val filePart = state.replaceFile?.let { selected ->
                    uriToPart(context, selected.uri, selected.name, "file")
                        ?: throw IllegalStateException("Couldn't read the selected file")
                }
                val thumbnailPart = state.thumbnailUri?.let { uri ->
                    uriToPart(context, uri, "cover.jpg", "thumbnail")
                }

                resourceRepository.updateResource(
                    resourceId = resourceId,
                    fields = fields,
                    filePart = filePart,
                    thumbnailPart = thumbnailPart
                ).onSuccess {
                    _uiState.update { it.copy(isSubmitting = false, submitted = true) }
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

    /** Copy a picked uri into a cache file and wrap it as a multipart part. */
    private fun uriToPart(context: Context, uri: Uri, fileName: String, partName: String): MultipartBody.Part? {
        return try {
            val temp = File.createTempFile("edit_upload_", "_" + fileName.replace(Regex("[^A-Za-z0-9._-]"), "_"), context.cacheDir)
            context.contentResolver.openInputStream(uri)?.use { input ->
                temp.outputStream().use { output -> input.copyTo(output) }
            } ?: return null
            val mime = runCatching {
                context.contentResolver.getType(uri)
            }.getOrNull() ?: guessMime(fileName)
            val body = temp.asRequestBody(mime.toMediaTypeOrNull())
            MultipartBody.Part.createFormData(partName, fileName, body)
        } catch (_: Exception) {
            null
        }
    }

    private fun guessMime(name: String): String = when (name.substringAfterLast('.', "").lowercase()) {
        "pdf" -> "application/pdf"
        "jpg", "jpeg" -> "image/jpeg"
        "png" -> "image/png"
        "webp" -> "image/webp"
        "gif" -> "image/gif"
        "mp4" -> "video/mp4"
        "mkv" -> "video/x-matroska"
        "webm" -> "video/webm"
        "mp3" -> "audio/mpeg"
        "m4a" -> "audio/mp4"
        "wav" -> "audio/wav"
        else -> "application/octet-stream"
    }
}
