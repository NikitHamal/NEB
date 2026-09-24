package com.neb.ians.ui.screens.upload

import android.content.Context
import android.net.Uri
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
    // ----- Marketplace: list this resource as paid with a price -----
    val isPaid: Boolean = false,
    val price: String = "",
    val selectedFiles: List<SelectedFile> = emptyList(),
    /** Page photos are published as one document unless the user says otherwise. */
    val combinePages: Boolean = true,
    /** Pages written so far while the document is being assembled. */
    val pagesPrepared: Int = 0,
    val isPreparing: Boolean = false,
    /** Set once the type has been chosen by hand, so picking files stops guessing. */
    val typeDirty: Boolean = false,
    /** Subject, level and place carried over from the last upload. */
    val reusedDefaults: Boolean = false,
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
) {
    /** True when the selection is a set of page photos — one document, many pages. */
    val isPageSet: Boolean
        get() = selectedFiles.size > 1 && selectedFiles.all { it.isImage }

    /** True when the upload will be assembled into a single PDF before sending. */
    val willCombine: Boolean
        get() = isPageSet && combinePages && !isEditMode

    /** What the user still has to supply, in the order the screen asks for it. */
    val missing: List<String>
        get() = buildList {
            if (!isEditMode && selectedFiles.isEmpty() && fileUrl.isBlank()) add("a file")
            if (title.isBlank()) add("a title")
            if (subject.isBlank()) add("a subject")
            if (isPaid && (price.toDoubleOrNull() ?: 0.0) <= 0.0) add("a price")
        }

    val canSubmit: Boolean
        get() = missing.isEmpty() && !isSubmitting && !isPreparing
}

data class SelectedFile(
    val uri: Uri,
    val name: String,
    val size: Long,
    val isImage: Boolean = false
)

@HiltViewModel
class UploadViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val resourceRepository: ResourceRepository,
    private val draftStore: UploadDraftStore
) : ViewModel() {

    /** Present when the wizard was opened as an edit (owner editing own resource). */
    private val editResourceId: String? = savedStateHandle.get<String>("resourceId")?.takeIf { it.isNotBlank() }

    private val _uiState = MutableStateFlow(UploadFormState())
    val uiState: StateFlow<UploadFormState> = _uiState.asStateFlow()

    init {
        if (editResourceId != null) loadEditResource(editResourceId) else restoreDefaults()
    }

    /** Offer back the subject, level and place the last upload used. */
    private fun restoreDefaults() {
        viewModelScope.launch {
            val defaults = draftStore.lastUsed()
            if (defaults.isEmpty) return@launch
            _uiState.update { state ->
                if (state.subject.isNotBlank() || state.gradeLevel.isNotBlank()) return@update state
                state.copy(
                    subject = defaults.subject,
                    gradeLevel = defaults.gradeLevel,
                    school = defaults.school,
                    pradesh = defaults.pradesh,
                    district = defaults.district,
                    tags = defaults.tags,
                    reusedDefaults = true
                )
            }
        }
    }

    /** Drop the carried-over answers when this upload is about something else. */
    fun clearReusedDefaults() {
        _uiState.update {
            it.copy(
                subject = "",
                gradeLevel = "",
                school = "",
                pradesh = "",
                district = "",
                tags = "",
                reusedDefaults = false
            )
        }
    }

    /** Prefill the wizard with everything the existing resource stores. */
    fun loadEditResource(resourceId: String? = editResourceId) {
        val id = resourceId ?: return
        viewModelScope.launch {
            _uiState.update { it.copy(isEditMode = true, editLoading = true, editLoadError = null) }
            val username = try { authRepository.currentUsernameHandleFlow.first() } catch (_: Exception) { "" }
            resourceRepository.getResource(id)
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
                            isPaid = resource.isPaid,
                            price = resource.price,
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
        _uiState.update { it.copy(type = type, typeDirty = true) }
    }

    fun setCombinePages(combine: Boolean) {
        _uiState.update { it.copy(combinePages = combine) }
        refreshDerivedType()
    }

    fun reorderFiles(from: Int, to: Int) {
        val current = _uiState.value.selectedFiles
        if (from !in current.indices || to !in current.indices || from == to) return
        val moved = current.toMutableList().apply { add(to, removeAt(from)) }
        _uiState.update { it.copy(selectedFiles = moved) }
    }

    /** Keep the type honest about what was picked, until the user overrides it. */
    private fun refreshDerivedType() {
        _uiState.update { state ->
            if (state.typeDirty || state.selectedFiles.isEmpty()) return@update state
            state.copy(type = UploadAutofill.typeFor(state.selectedFiles.map { it.name }, state.willCombine))
        }
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
            state.selectedFiles.any { UploadOptions.isVideoFileName(it.name) }
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

    fun updateIsPaid(isPaid: Boolean) {
        _uiState.update { it.copy(isPaid = isPaid) }
    }

    fun updatePrice(price: String) {
        // Keep it numeric — digits only, no negatives/letters.
        val sanitized = price.filter { it.isDigit() || it == '.' }.trim()
        _uiState.update { it.copy(price = sanitized) }
    }

    fun addFiles(files: List<SelectedFile>) {
        // Edit mode replaces the single stored file — only the first pick counts.
        if (_uiState.value.isEditMode) {
            val replacement = files.firstOrNull() ?: return
            _uiState.update { it.copy(selectedFiles = listOf(replacement), fileError = null) }
            return
        }
        val current = _uiState.value.selectedFiles
        val incoming = files.filterNot { f -> current.any { it.uri == f.uri } }
        if (incoming.isEmpty()) return
        val merged = (current + incoming).take(UploadOptions.MAX_PAGES)
        val dropped = current.size + incoming.size - merged.size
        _uiState.update { state ->
            val firstName = merged.first().name
            state.copy(
                selectedFiles = merged,
                title = state.title.ifBlank { UploadAutofill.titleFrom(firstName) },
                subject = state.subject.ifBlank { UploadAutofill.subjectFrom(firstName, UploadOptions.SUBJECTS) },
                titleError = null,
                subjectError = null,
                fileError = if (dropped > 0) "One upload holds up to ${UploadOptions.MAX_PAGES} pages — the rest were left out." else null
            )
        }
        refreshDerivedType()
    }

    fun removeFileAt(index: Int) {
        val current = _uiState.value.selectedFiles
        if (index in current.indices) {
            _uiState.update { it.copy(selectedFiles = current.toMutableList().apply { removeAt(index) }) }
            refreshDerivedType()
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
        if (state.isPaid && (state.price.toDoubleOrNull() ?: 0.0) <= 0.0) {
            _uiState.update { it.copy(submitError = "Enter a price greater than Rs. 0 for paid resources") }
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
                when {
                    state.willCombine -> uploadCombinedPages(context, bearerToken, files, state)
                    files.isNotEmpty() -> uploadMultipleFiles(context, bearerToken, files, state)
                    else -> uploadWithUrl(context, bearerToken, state)
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapExceptionVerbose(e, "Upload resource")) }
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
                    "source_url" to state.sourceUrl.toRequestBody(TEXT_PLAIN),
                    "is_paid" to (if (state.isPaid) "true" else "false").toRequestBody(TEXT_PLAIN),
                    "price" to (state.price.ifBlank { "0" }).toRequestBody(TEXT_PLAIN)
                )
                // Link: only PATCH when edited — a blank untouched field must never wipe an upload.
                if (state.fileUrlDirty) fields["file_url"] = state.fileUrl.toRequestBody(TEXT_PLAIN)
                // Cover: manual upload wins; then a fresh URL; a cleared URL removes the cover.
                if (state.thumbnailDirty) fields["thumbnail_url"] = state.thumbnailUrl.toRequestBody(TEXT_PLAIN)

                val replacement = state.selectedFiles.firstOrNull()
                val filePart = replacement?.let { selected ->
                    val file = UploadMedia.uriToFile(context, selected.uri, selected.name)
                        ?: throw IllegalStateException("Couldn't read the selected file")
                    MultipartBody.Part.createFormData("file", file.name, file.asRequestBody(UploadMedia.contentTypeFromName(file.name)))
                }
                val thumbnailPart = state.thumbnailUri?.let { uri ->
                    UploadMedia.buildThumbnailPart(context, uri, "cover")
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
                        it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapExceptionVerbose(e, "Edit resource"))
                    }
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isSubmitting = false, submitError = ApiErrorMapper.mapExceptionVerbose(e, "Edit resource"))
                }
            }
        }
    }

    /**
     * Page photos leave as one PDF.
     *
     * The old path posted every picked file as its own resource, which turned a
     * set of note pages into a shelf of single-page junk. Here the pages are
     * assembled first, uploaded once, and the first page doubles as the cover.
     */
    private suspend fun uploadCombinedPages(
        context: Context,
        bearerToken: String,
        files: List<SelectedFile>,
        state: UploadFormState
    ) {
        _uiState.update { it.copy(isPreparing = true, pagesPrepared = 0) }
        val destination = File(context.cacheDir, "uploads/${documentFileName(state.title)}")
        val document = PageDocumentBuilder.combine(context, files.map { it.uri }, destination) { done ->
            _uiState.update { it.copy(pagesPrepared = done, uploadProgress = done.toFloat() / files.size * 0.5f) }
        }
        _uiState.update { it.copy(isPreparing = false) }
        if (document == null) {
            _uiState.update {
                it.copy(isSubmitting = false, submitError = "Couldn't read those pages. Try picking them again.")
            }
            return
        }
        if (document.length() > UploadOptions.MAX_FILE_SIZE) {
            document.delete()
            _uiState.update {
                it.copy(
                    isSubmitting = false,
                    submitError = "That document came to ${document.length() / (1024 * 1024)} MB, over the 50 MB limit. " +
                        "Split it into two uploads."
                )
            }
            return
        }

        val filePart = MultipartBody.Part.createFormData(
            "file",
            document.name,
            document.asRequestBody("application/pdf".toMediaTypeOrNull())
        )
        val thumbnailPart = when {
            state.thumbnailUri != null -> UploadMedia.buildThumbnailPart(context, state.thumbnailUri, "cover")
            state.thumbnailUrl.isBlank() -> UploadMedia.buildThumbnailPart(context, files.first().uri, "cover")
            else -> null
        }
        _uiState.update { it.copy(uploadProgress = 0.6f) }

        val response = apiService.uploadResource(
            bearerToken = bearerToken,
            file = filePart,
            thumbnail = thumbnailPart,
            title = state.title.toRequestBody(TEXT_PLAIN),
            subject = state.subject.toRequestBody(TEXT_PLAIN),
            description = state.description.toRequestBody(TEXT_PLAIN),
            gradeLevel = state.gradeLevel.toRequestBody(TEXT_PLAIN),
            type = state.type.ifBlank { "Note" }.toRequestBody(TEXT_PLAIN),
            examType = state.examType.toRequestBody(TEXT_PLAIN),
            faculty = state.faculty.toRequestBody(TEXT_PLAIN),
            program = state.program.toRequestBody(TEXT_PLAIN),
            year = state.year.toRequestBody(TEXT_PLAIN),
            school = state.school.toRequestBody(TEXT_PLAIN),
            pradesh = state.pradesh.toRequestBody(TEXT_PLAIN),
            district = state.district.toRequestBody(TEXT_PLAIN),
            tags = state.tags.toRequestBody(TEXT_PLAIN),
            fileUrl = null,
            thumbnailUrl = state.thumbnailUrl.toRequestBody(TEXT_PLAIN),
            authorName = state.authorName.toRequestBody(TEXT_PLAIN),
            sourceLabel = state.sourceLabel.toRequestBody(TEXT_PLAIN),
            sourceUrl = state.sourceUrl.toRequestBody(TEXT_PLAIN),
            isPaid = (if (state.isPaid) "true" else "false").toRequestBody(TEXT_PLAIN),
            price = (state.price.ifBlank { "0" }).toRequestBody(TEXT_PLAIN)
        )
        document.delete()

        if (response.error != null) {
            _uiState.update { it.copy(isSubmitting = false, submitError = response.error) }
        } else {
            rememberDefaults(state)
            _uiState.update { it.copy(isSubmitting = false, uploadProgress = 1f, submitSuccess = true) }
        }
    }

    private fun documentFileName(title: String): String {
        val stem = title.trim().replace(Regex("[^A-Za-z0-9\\u0900-\\u097F ]"), "").replace(' ', '_')
        return (stem.take(48).ifBlank { "notes" }) + ".pdf"
    }

    private fun rememberDefaults(state: UploadFormState) {
        viewModelScope.launch {
            draftStore.remember(
                UploadDefaults(
                    subject = state.subject,
                    gradeLevel = state.gradeLevel,
                    school = state.school,
                    pradesh = state.pradesh,
                    district = state.district,
                    tags = state.tags
                )
            )
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
            val file = UploadMedia.uriToFile(context, selectedFile.uri, selectedFile.name) ?: continue
            val requestBody = file.asRequestBody(UploadMedia.contentTypeFromName(file.name))
            val multipartPart = MultipartBody.Part.createFormData("file", file.name, requestBody)

            // Cover image: manual pick wins; videos get an auto frame when the
            // user supplied neither an upload nor a URL.
            val thumbnailPart = when {
                state.thumbnailUri != null -> UploadMedia.buildThumbnailPart(context, state.thumbnailUri, "cover")
                state.thumbnailUrl.isBlank() && UploadOptions.isVideoFileName(selectedFile.name) ->
                    UploadMedia.videoFrameThumbnailPart(context, selectedFile.uri, selectedFile.name)
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
                sourceUrl = (state.sourceUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
                isPaid = (if (state.isPaid) "true" else "false").toRequestBody(TEXT_PLAIN),
                price = (state.price.ifBlank { "0" }).toRequestBody(TEXT_PLAIN)
            )

            if (response.error != null) {
                _uiState.update { it.copy(isSubmitting = false, submitError = response.error) }
                return
            }

            _uiState.update { it.copy(uploadProgress = (index + 1).toFloat() / totalFiles) }
        }
        rememberDefaults(state)
        _uiState.update { it.copy(isSubmitting = false, submitSuccess = true) }
    }

    private suspend fun uploadWithUrl(
        context: Context,
        bearerToken: String,
        state: UploadFormState
    ) {
        val thumbnailPart = state.thumbnailUri?.let { UploadMedia.buildThumbnailPart(context, it, "cover") }
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
            sourceUrl = (state.sourceUrl.takeIf { it.isNotBlank() } ?: "").toRequestBody(TEXT_PLAIN),
            isPaid = (if (state.isPaid) "true" else "false").toRequestBody(TEXT_PLAIN),
            price = (state.price.ifBlank { "0" }).toRequestBody(TEXT_PLAIN)
        )

        if (response.error != null) {
            _uiState.update { it.copy(isSubmitting = false, submitError = response.error) }
        } else {
            rememberDefaults(state)
            _uiState.update { it.copy(isSubmitting = false, submitSuccess = true) }
        }
    }

    fun resetSuccess() {
        _uiState.update {
            UploadFormState(
                subject = it.subject,
                gradeLevel = it.gradeLevel,
                school = it.school,
                pradesh = it.pradesh,
                district = it.district,
                tags = it.tags,
                reusedDefaults = true
            )
        }
    }

    fun dismissError() {
        _uiState.update { it.copy(submitError = null, fileError = null) }
    }

}