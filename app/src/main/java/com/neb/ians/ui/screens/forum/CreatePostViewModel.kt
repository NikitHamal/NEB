package com.neb.ians.ui.screens.forum

import android.content.Context
import android.net.Uri
import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiMediaAttachmentInput
import com.neb.ians.data.api.ApiPollCreate
import com.neb.ians.data.api.ApiPollOptionCreate
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.WebPostCreateRequest
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.applyMention
import com.neb.ians.ui.components.mentionQueryAt
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject

const val MAX_POST_TITLE = 200
const val MAX_POST_CONTENT = 20_000
const val MAX_POST_IMAGES = 10
const val MAX_IMAGE_BYTES = 10L * 1024 * 1024

data class PollOptionDraft(
    val text: String = "",
    val isCorrect: Boolean = false
)

data class ExistingPostImageDraft(
    val id: String,
    val imageUrl: String,
    val order: Int = 0
)

data class CreatePostUiState(
    val title: String = "",
    val content: TextFieldValue = TextFieldValue(""),
    val selectedCategory: String = "General",
    val customCategory: String = "",
    val isCustomCategory: Boolean = false,
    val showPreview: Boolean = false,
    val images: List<Uri> = emptyList(),
    val existingImages: List<ExistingPostImageDraft> = emptyList(),
    val removedExistingImageIds: Set<String> = emptySet(),
    val mediaAttachments: List<PendingForumAttachment> = emptyList(),
    val isAnonymous: Boolean = false,
    val isSubmitting: Boolean = false,
    val isLoadingPost: Boolean = false,
    val isEditMode: Boolean = false,
    val editingPostId: String? = null,
    val error: String? = null,
    // Poll builder. Existing polls are intentionally not edited here because
    // votes and answer state need server-side migration/validation semantics.
    val pollEnabled: Boolean = false,
    val pollType: String = "voting", // "voting" | "mcq"
    val pollQuestion: String = "",
    val pollOptions: List<PollOptionDraft> = listOf(PollOptionDraft(), PollOptionDraft()),
    val pollAllowMultiple: Boolean = false,
    val pollExplanation: String = "",
    val pollDurationMs: Long = 0L,
    // @mention autocomplete
    val mentionSuggestions: List<ApiUserSearchResult> = emptyList()
) {
    val effectiveCategory: String
        get() = if (isCustomCategory) customCategory.trim() else selectedCategory

    val visibleExistingImages: List<ExistingPostImageDraft>
        get() = existingImages.filterNot { it.id in removedExistingImageIds }.sortedBy { it.order }

    val activeImageCount: Int
        get() = visibleExistingImages.size + images.size

    val remainingExistingImageUrls: List<String>
        get() = visibleExistingImages.map { it.imageUrl }

    companion object {
        const val OTHER_CATEGORY = "Other..."
        val CATEGORIES = listOf(
            "General", "Physics", "Chemistry", "Mathematics",
            "Biology", "English", "Computer Science", "Exam Tips"
        )
        val POLL_DURATIONS = listOf(
            0L to "No expiry",
            3_600_000L to "1 hour",
            86_400_000L to "24 hours",
            259_200_000L to "3 days",
            604_800_000L to "7 days"
        )
    }
}

@HiltViewModel
class CreatePostViewModel @Inject constructor(
    private val forumRepository: ForumRepository,
    private val mediaUploadHelper: ForumMediaUploadHelper,
    @ApplicationContext private val appContext: Context
) : ViewModel() {

    private val _uiState = MutableStateFlow(CreatePostUiState())
    val uiState: StateFlow<CreatePostUiState> = _uiState.asStateFlow()

    private var mentionJob: Job? = null
    private var loadedEditPostId: String? = null

    fun loadForEdit(postId: String) {
        if (loadedEditPostId == postId && _uiState.value.editingPostId == postId) return
        loadedEditPostId = postId
        _uiState.update {
            it.copy(
                isEditMode = true,
                editingPostId = postId,
                isLoadingPost = true,
                isSubmitting = false,
                error = null
            )
        }
        viewModelScope.launch {
            forumRepository.getPost(postId)
                .onSuccess { post ->
                    val knownCategory = post.category in CreatePostUiState.CATEGORIES
                    _uiState.update {
                        it.copy(
                            title = post.title,
                            content = TextFieldValue(post.content),
                            selectedCategory = if (knownCategory) post.category else "General",
                            customCategory = if (knownCategory) "" else post.category,
                            isCustomCategory = !knownCategory,
                            images = emptyList(),
                            existingImages = post.images.map { image ->
                                ExistingPostImageDraft(
                                    id = image.id,
                                    imageUrl = image.imageUrl,
                                    order = image.order
                                )
                            },
                            removedExistingImageIds = emptySet(),
                            pollEnabled = false,
                            isLoadingPost = false,
                            error = null
                        )
                    }
                }
                .onFailure { e ->
                    _uiState.update {
                        it.copy(
                            isLoadingPost = false,
                            error = ApiErrorMapper.mapException(e)
                        )
                    }
                }
        }
    }

    fun onTitleChange(title: String) {
        if (title.length <= MAX_POST_TITLE) _uiState.update { it.copy(title = title) }
    }

    fun onContentChange(content: TextFieldValue) {
        if (content.text.length > MAX_POST_CONTENT) return
        _uiState.update { it.copy(content = content) }
        scheduleMentionSearch(content)
    }

    private fun scheduleMentionSearch(content: TextFieldValue) {
        mentionJob?.cancel()
        val query = mentionQueryAt(content)
        if (query == null) {
            if (_uiState.value.mentionSuggestions.isNotEmpty()) {
                _uiState.update { it.copy(mentionSuggestions = emptyList()) }
            }
            return
        }
        mentionJob = viewModelScope.launch {
            delay(300)
            val results = mutableListOf<ApiUserSearchResult>()
            if (query == "all") {
                results.add(ApiUserSearchResult(id = "@all", username = "all", displayName = "Everyone"))
            }
            forumRepository.searchUsers(query)
                .onSuccess { users -> results.addAll(users.take(8)) }
            if (mentionQueryAt(_uiState.value.content) == query) {
                _uiState.update { it.copy(mentionSuggestions = results) }
            }
        }
    }

    fun selectMention(user: ApiUserSearchResult) {
        _uiState.update {
            it.copy(
                content = applyMention(it.content, user.username),
                mentionSuggestions = emptyList()
            )
        }
    }

    fun onCategoryChange(category: String) {
        if (category == CreatePostUiState.OTHER_CATEGORY) {
            _uiState.update { it.copy(isCustomCategory = true) }
        } else {
            _uiState.update { it.copy(selectedCategory = category, isCustomCategory = false) }
        }
    }

    fun onCustomCategoryChange(value: String) {
        if (value.length <= 50) _uiState.update { it.copy(customCategory = value) }
    }

    fun togglePreview(show: Boolean) {
        _uiState.update { it.copy(showPreview = show) }
    }

    // ----- Images -----

    fun addImage(uri: Uri?) {
        if (uri == null) return
        val state = _uiState.value
        if (state.activeImageCount >= MAX_POST_IMAGES) {
            _uiState.update { it.copy(error = "Maximum $MAX_POST_IMAGES images per post") }
            return
        }
        val size = imageSizeBytes(uri)
        if (size != null && size > MAX_IMAGE_BYTES) {
            _uiState.update { it.copy(error = "Image too large (max 10MB)") }
            return
        }
        _uiState.update { it.copy(images = it.images + uri, error = null) }
    }

    fun removeImage(uri: Uri) {
        _uiState.update { it.copy(images = it.images - uri) }
    }

    fun removeExistingImage(imageId: String) {
        _uiState.update { it.copy(removedExistingImageIds = it.removedExistingImageIds + imageId) }
    }

    private fun imageSizeBytes(uri: Uri): Long? {
        return try {
            appContext.contentResolver.openAssetFileDescriptor(uri, "r")?.use { it.length }
        } catch (_: Exception) {
            null
        }
    }

    // ----- Media attachments (video / audio / files) -----

    fun setAnonymous(anonymous: Boolean) {
        if (_uiState.value.isEditMode) return // anonymity is immutable after create
        _uiState.update { it.copy(isAnonymous = anonymous) }
    }

    fun addMediaAttachments(uris: List<Uri>) {
        uris.forEach { uri -> addMediaAttachment(uri) }
    }

    fun addMediaAttachment(uri: Uri?) {
        if (uri == null) return
        val state = _uiState.value
        if (state.mediaAttachments.size >= ForumMediaUploadHelper.MAX_ATTACHMENTS) {
            _uiState.update { it.copy(error = "Maximum ${ForumMediaUploadHelper.MAX_ATTACHMENTS} attachments") }
            return
        }
        val kind = mediaUploadHelper.guessKind(uri)
        if (kind == "video" && state.mediaAttachments.any { it.kind == "video" }) {
            _uiState.update { it.copy(error = "Maximum 1 video per post") }
            return
        }
        val size = mediaUploadHelper.sizeOf(uri)
        if (size > ForumMediaUploadHelper.limitFor(kind)) {
            _uiState.update { it.copy(error = ForumMediaUploadHelper.limitLabel(kind)) }
            return
        }
        val pending = PendingForumAttachment(
            name = mediaUploadHelper.displayName(uri),
            kind = kind,
            sizeBytes = size,
            uri = uri
        )
        _uiState.update { it.copy(mediaAttachments = it.mediaAttachments + pending, error = null) }
        viewModelScope.launch {
            val result = mediaUploadHelper.upload(uri, kind, pending.name)
            _uiState.update { current ->
                current.copy(mediaAttachments = current.mediaAttachments.map { att ->
                    if (att.localId != pending.localId) att
                    else result.fold(
                        onSuccess = { descriptor -> att.copy(uploading = false, uploaded = descriptor) },
                        onFailure = { e -> att.copy(uploading = false, error = e.message ?: "Upload failed") }
                    )
                })
            }
            result.exceptionOrNull()?.let { e ->
                _uiState.update { it.copy(error = e.message ?: "Couldn't upload ${pending.name}") }
            }
        }
    }

    fun removeMediaAttachment(localId: String) {
        _uiState.update { current ->
            current.copy(mediaAttachments = current.mediaAttachments.filterNot { it.localId == localId })
        }
    }

    // ----- Poll builder -----

    fun togglePoll(enabled: Boolean) {
        _uiState.update { it.copy(pollEnabled = enabled) }
    }

    fun onPollTypeChange(type: String) {
        _uiState.update { it.copy(pollType = type) }
    }

    fun onPollQuestionChange(value: String) {
        if (value.length <= 300) _uiState.update { it.copy(pollQuestion = value) }
    }

    fun onPollOptionChange(index: Int, text: String) {
        if (text.length > 200) return
        _uiState.update { state ->
            state.copy(pollOptions = state.pollOptions.mapIndexed { i, option ->
                if (i == index) option.copy(text = text) else option
            })
        }
    }

    fun togglePollOptionCorrect(index: Int) {
        _uiState.update { state ->
            state.copy(pollOptions = state.pollOptions.mapIndexed { i, option ->
                if (i == index) option.copy(isCorrect = !option.isCorrect) else option
            })
        }
    }

    fun addPollOption() {
        _uiState.update { state ->
            if (state.pollOptions.size >= 6) state
            else state.copy(pollOptions = state.pollOptions + PollOptionDraft())
        }
    }

    fun removePollOption(index: Int) {
        _uiState.update { state ->
            if (state.pollOptions.size <= 2) state
            else state.copy(pollOptions = state.pollOptions.filterIndexed { i, _ -> i != index })
        }
    }

    fun onPollAllowMultipleChange(allow: Boolean) {
        _uiState.update { it.copy(pollAllowMultiple = allow) }
    }

    fun onPollExplanationChange(value: String) {
        if (value.length <= 500) _uiState.update { it.copy(pollExplanation = value) }
    }

    fun onPollDurationChange(durationMs: Long) {
        _uiState.update { it.copy(pollDurationMs = durationMs) }
    }

    // ----- Submit -----

    fun submitPost(onSuccess: () -> Unit) {
        val state = _uiState.value
        val title = state.title.trim()
        val content = state.content.text.trim()
        val category = state.effectiveCategory

        if (title.isBlank() || content.isBlank()) return
        if (category.isBlank()) {
            _uiState.update { it.copy(error = "Choose a category") }
            return
        }
        if (state.mediaAttachments.any { it.uploading }) {
            _uiState.update { it.copy(error = "Wait for attachments to finish uploading") }
            return
        }
        val attachments: List<ApiMediaAttachmentInput> = state.mediaAttachments
            .mapNotNull { it.uploaded }

        var pollCreate: ApiPollCreate? = null
        if (!state.isEditMode && state.pollEnabled) {
            val options = state.pollOptions.filter { it.text.isNotBlank() }
            if (options.size < 2) {
                _uiState.update { it.copy(error = "Poll needs at least 2 options") }
                return
            }
            if (state.pollType == "mcq" && options.none { it.isCorrect }) {
                _uiState.update { it.copy(error = "Mark at least 1 correct answer") }
                return
            }
            pollCreate = ApiPollCreate(
                question = state.pollQuestion.trim(),
                pollType = state.pollType,
                allowMultiple = state.pollType == "voting" && state.pollAllowMultiple,
                explanation = if (state.pollType == "mcq") state.pollExplanation.trim() else "",
                durationMs = state.pollDurationMs,
                options = options.mapIndexed { index, option ->
                    ApiPollOptionCreate(
                        text = option.text.trim(),
                        isCorrect = state.pollType == "mcq" && option.isCorrect,
                        index = index
                    )
                }
            )
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, error = null) }

            val imageUrls = state.remainingExistingImageUrls.toMutableList()
            for ((index, uri) in state.images.withIndex()) {
                val result = uploadImage(uri, index)
                val url = result.getOrNull()
                if (url == null) {
                    _uiState.update {
                        it.copy(
                            isSubmitting = false,
                            error = result.exceptionOrNull()?.message ?: "Image upload failed"
                        )
                    }
                    return@launch
                }
                imageUrls.add(url)
            }

            val result = if (state.isEditMode) {
                val postId = state.editingPostId
                if (postId.isNullOrBlank()) {
                    Result.failure(IllegalStateException("Missing post id"))
                } else {
                    forumRepository.updatePost(
                        postId = postId,
                        title = title,
                        content = content,
                        category = category,
                        imageUrls = imageUrls
                    )
                }
            } else if (pollCreate != null || imageUrls.isNotEmpty() || attachments.isNotEmpty() || state.isAnonymous) {
                forumRepository.createPostWeb(
                    WebPostCreateRequest(
                        title = title,
                        content = content,
                        category = category,
                        images = imageUrls,
                        poll = pollCreate,
                        isAnonymous = state.isAnonymous,
                        attachments = attachments
                    )
                )
            } else {
                forumRepository.createPost(title = title, content = content, category = category)
            }

            result.onSuccess {
                _uiState.update { it.copy(isSubmitting = false) }
                onSuccess()
            }.onFailure { e ->
                _uiState.update { it.copy(isSubmitting = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    private suspend fun uploadImage(uri: Uri, index: Int): Result<String> {
        val bytes = withContext(Dispatchers.IO) {
            try {
                appContext.contentResolver.openInputStream(uri)?.use { it.readBytes() }
            } catch (_: Exception) {
                null
            }
        } ?: return Result.failure(IllegalStateException("Couldn't read image ${index + 1}"))

        if (bytes.size > MAX_IMAGE_BYTES) {
            return Result.failure(IllegalStateException("Image ${index + 1} is too large (max 10MB)"))
        }
        val mime = appContext.contentResolver.getType(uri) ?: "image/*"
        val extension = when (mime) {
            "image/png" -> "png"
            "image/webp" -> "webp"
            "image/gif" -> "gif"
            else -> "jpg"
        }
        val part = MultipartBody.Part.createFormData(
            "image",
            "image_$index.$extension",
            bytes.toRequestBody(mime.toMediaType())
        )
        return forumRepository.uploadPostImage(part)
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}
