package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResourceUploadResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import java.io.FileOutputStream
import javax.inject.Inject

private val TEXT_PLAIN: okhttp3.MediaType? = try { "text/plain".toMediaType() } catch (_: Exception) { null }

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
    val submitSuccess: Boolean = false
)

data class SelectedFile(
    val uri: Uri,
    val name: String,
    val size: Long
)

@HiltViewModel
class UploadViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UploadFormState())
    val uiState: StateFlow<UploadFormState> = _uiState.asStateFlow()

    companion object {
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
        _uiState.update { it.copy(fileUrl = fileUrl, fileError = null) }
    }

    fun updateThumbnailUrl(thumbnailUrl: String) {
        _uiState.update { it.copy(thumbnailUrl = thumbnailUrl) }
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
        if (state.selectedFiles.isEmpty() && state.fileUrl.isBlank()) {
            _uiState.update { it.copy(fileError = "Please upload a file or provide a file URL") }
            hasError = true
        }
        if (hasError) return

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
                    uploadWithUrl(bearerToken, state)
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSubmitting = false, submitError = e.message ?: "Upload failed") }
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

            val response = apiService.uploadResource(
                bearerToken = bearerToken,
                file = multipartPart,
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

    private suspend fun uploadWithUrl(bearerToken: String, state: UploadFormState) {
        val response = apiService.uploadResource(
            bearerToken = bearerToken,
            file = null,
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

    private fun contentTypeFromName(name: String): String {
        val ext = name.substringAfterLast('.', "").lowercase()
        return when (ext) {
            "pdf" -> "application/pdf"
            "doc" -> "application/msword"
            "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            "ppt" -> "application/vnd.ms-powerpoint"
            "pptx" -> "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            "xls" -> "application/vnd.ms-excel"
            "xlsx" -> "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            "jpg", "jpeg" -> "image/jpeg"
            "png" -> "image/png"
            "gif" -> "image/gif"
            "webp" -> "image/webp"
            "mp4" -> "video/mp4"
            "mp3" -> "audio/mpeg"
            "zip" -> "application/zip"
            else -> "application/octet-stream"
        }
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