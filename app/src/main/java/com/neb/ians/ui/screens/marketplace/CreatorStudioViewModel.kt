package com.neb.ians.ui.screens.marketplace

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiCreatorPost
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiMarketplaceSale
import com.neb.ians.data.api.ApiMarketplaceWallet
import com.neb.ians.data.repository.MarketplaceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** The studio's draft of a course, kept off the network until Save. */
data class CourseDraft(
    val id: String = "",
    val title: String = "",
    val summary: String = "",
    val description: String = "",
    val isPaid: Boolean = false,
    val price: String = "",
    val level: String = "",
    val durationLabel: String = "",
    val lessonCount: String = "0",
    val seatLimit: String = "0",
    val includes: String = "",
    val tags: String = "",
    val coverUrl: String = "",
    val status: String = "draft",
    val featured: Boolean = false,
    val resourceIds: List<String> = emptyList()
)

data class PostDraft(
    val id: String = "",
    val title: String = "",
    val body: String = "",
    val mediaUrl: String = "",
    val linkUrl: String = "",
    val pinned: Boolean = false,
    val published: Boolean = true
)

data class CreatorStudioUiState(
    val isLoading: Boolean = true,
    val notEligible: Boolean = false,
    val error: String? = null,
    val isSavingPage: Boolean = false,
    val isSavingCourse: Boolean = false,
    val isSavingPost: Boolean = false,
    val transientMessage: String? = null,
    val messageIsError: Boolean = false,

    val page: ApiCreatorPage? = null,
    val displayName: String = "",
    val tagline: String = "",
    val about: String = "",
    val slug: String = "",
    val subjects: String = "",
    val location: String = "",
    val contactEmail: String = "",
    val contactPhone: String = "",
    val avatarUrl: String = "",
    val coverUrl: String = "",
    val accentHex: String = "#004BD4",
    val layout: String = "editorial",
    val heroStyle: String = "art",
    val radius: String = "round",
    val acceptingStudents: Boolean = true,
    val blocks: List<ApiCreatorBlock> = emptyList(),
    val editingBlock: Pair<Int, ApiCreatorBlock>? = null,

    val courses: List<ApiCreatorCourse> = emptyList(),
    val courseDraft: CourseDraft = CourseDraft(),
    val posts: List<ApiCreatorPost> = emptyList(),
    val postDraft: PostDraft = PostDraft(),

    val wallet: ApiMarketplaceWallet = ApiMarketplaceWallet(),
    val sales: List<ApiMarketplaceSale> = emptyList(),
    val commissionPercent: Double = 2.5,
    val nebiansPoints: Int = 0,
    val resourceOptions: List<Pair<String, String>> = emptyList()
)

@HiltViewModel
class CreatorStudioViewModel @Inject constructor(
    private val repository: MarketplaceRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CreatorStudioUiState())
    val uiState: StateFlow<CreatorStudioUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun load() {
        _uiState.update { it.copy(isLoading = it.page == null, error = null) }
        viewModelScope.launch {
            repository.myPage().fold(
                onSuccess = { response ->
                    if (!response.eligible || response.page == null) {
                        _uiState.update {
                            it.copy(isLoading = false, notEligible = !response.eligible, page = response.page)
                        }
                        return@fold
                    }
                    val page = response.page
                    _uiState.update { current ->
                        current.copy(
                            isLoading = false,
                            notEligible = false,
                            error = null,
                            page = page,
                            displayName = page.displayName,
                            tagline = page.tagline,
                            about = page.about,
                            slug = page.slug,
                            subjects = page.subjects.joinToString(", "),
                            location = page.location,
                            contactEmail = page.contactEmail,
                            contactPhone = page.contactPhone,
                            avatarUrl = page.avatarUrl,
                            coverUrl = page.coverUrl,
                            accentHex = page.accentHex,
                            layout = page.layout,
                            heroStyle = page.style.hero.ifBlank { "art" },
                            radius = page.style.radius.ifBlank { "round" },
                            acceptingStudents = page.acceptingStudents,
                            blocks = page.blocks,
                            courses = page.courses,
                            resourceOptions = page.resources.take(60).map { it.id to it.title }
                        )
                    }
                },
                onFailure = { failure ->
                    _uiState.update {
                        it.copy(isLoading = false, error = ApiErrorMapper.mapException(failure))
                    }
                }
            )
            loadDashboard()
        }
    }

    private fun loadDashboard() {
        viewModelScope.launch {
            repository.dashboard().onSuccess { dashboard ->
                _uiState.update {
                    it.copy(
                        wallet = dashboard.wallet,
                        sales = dashboard.sales,
                        commissionPercent = dashboard.commissionPercent.toDoubleOrNull() ?: 2.5,
                        nebiansPoints = dashboard.nebiansPoints
                    )
                }
            }
        }
    }

    // ----- Page fields -----

    fun updateDisplayName(value: String) = _uiState.update { it.copy(displayName = value) }
    fun updateTagline(value: String) = _uiState.update { it.copy(tagline = value) }
    fun updateAbout(value: String) = _uiState.update { it.copy(about = value) }
    fun updateSlug(value: String) = _uiState.update { it.copy(slug = value.lowercase().filter { c -> c.isLetterOrDigit() || c == '-' }) }
    fun updateSubjects(value: String) = _uiState.update { it.copy(subjects = value) }
    fun updateLocation(value: String) = _uiState.update { it.copy(location = value) }
    fun updateContactEmail(value: String) = _uiState.update { it.copy(contactEmail = value) }
    fun updateContactPhone(value: String) = _uiState.update { it.copy(contactPhone = value) }
    fun updateAvatarUrl(value: String) = _uiState.update { it.copy(avatarUrl = value) }
    fun updateCoverUrl(value: String) = _uiState.update { it.copy(coverUrl = value) }
    fun updateAccent(value: String) = _uiState.update { it.copy(accentHex = value) }
    fun updateLayout(value: String) = _uiState.update { it.copy(layout = value) }
    fun updateHeroStyle(value: String) = _uiState.update { it.copy(heroStyle = value) }
    fun updateRadius(value: String) = _uiState.update { it.copy(radius = value) }
    fun updateAccepting(value: Boolean) = _uiState.update { it.copy(acceptingStudents = value) }

    fun setPublished(published: Boolean) {
        viewModelScope.launch {
            repository.savePage(published = published).fold(
                onSuccess = { response ->
                    _uiState.update { current ->
                        current.copy(
                            page = response.page ?: current.page,
                            transientMessage = if (published) "Your page is live." else "Your page is a draft again.",
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure -> showError(failure) }
            )
        }
    }

    fun savePage() {
        val state = _uiState.value
        if (state.displayName.isBlank()) {
            _uiState.update { it.copy(transientMessage = "Your page needs a name", messageIsError = true) }
            return
        }
        _uiState.update { it.copy(isSavingPage = true) }

        viewModelScope.launch {
            repository.savePage(
                displayName = state.displayName,
                tagline = state.tagline,
                about = state.about,
                slug = state.slug.takeIf { it.isNotBlank() },
                avatarUrl = state.avatarUrl,
                coverUrl = state.coverUrl,
                accentHex = state.accentHex,
                layout = state.layout,
                location = state.location,
                contactEmail = state.contactEmail,
                contactPhone = state.contactPhone,
                subjects = state.subjects.split(',').map { it.trim() }.filter { it.isNotEmpty() },
                blocks = repository.blocksPayload(state.page!!.copy(blocks = state.blocks)),
                acceptingStudents = state.acceptingStudents,
                style = mapOf(
                    "hero" to kotlinx.serialization.json.JsonPrimitive(state.heroStyle),
                    "radius" to kotlinx.serialization.json.JsonPrimitive(state.radius),
                    "density" to kotlinx.serialization.json.JsonPrimitive("comfortable"),
                    "show_stats" to kotlinx.serialization.json.JsonPrimitive(true),
                    "show_contact" to kotlinx.serialization.json.JsonPrimitive(true),
                    "gallery_columns" to kotlinx.serialization.json.JsonPrimitive(3)
                ),
                socials = state.page.socials
            ).fold(
                onSuccess = { response ->
                    _uiState.update { current ->
                        current.copy(
                            isSavingPage = false,
                            page = response.page ?: current.page,
                            slug = response.page?.slug ?: current.slug,
                            blocks = response.page?.blocks ?: current.blocks,
                            transientMessage = "Page saved",
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isSavingPage = false) }
                    showError(failure)
                }
            )
        }
    }

    // ----- Blocks -----

    fun addBlock(type: String) {
        val block = ApiCreatorBlock(
            id = "b" + System.currentTimeMillis().toString(36),
            type = type,
            enabled = true,
            items = when (type) {
                "stats" -> listOf(ApiCreatorBlockItem())
                "faq" -> listOf(ApiCreatorBlockItem())
                "schedule" -> listOf(ApiCreatorBlockItem())
                else -> emptyList()
            }
        )
        _uiState.update {
            it.copy(
                blocks = it.blocks + block,
                editingBlock = (it.blocks.size) to block,
                transientMessage = "Section added — save to publish it",
                messageIsError = false
            )
        }
    }

    fun moveBlock(index: Int, delta: Int) {
        _uiState.update { state ->
            val target = index + delta
            if (target < 0 || target > state.blocks.lastIndex) {
                state
            } else {
                val blocks = state.blocks.toMutableList()
                val moved = blocks.removeAt(index)
                blocks.add(target, moved)
                state.copy(blocks = blocks)
            }
        }
    }

    fun removeBlock(index: Int) = _uiState.update { state ->
        val blocks = state.blocks.toMutableList()
        if (index in blocks.indices) blocks.removeAt(index)
        state.copy(blocks = blocks, editingBlock = null)
    }

    fun toggleBlock(index: Int) = _uiState.update { state ->
        val blocks = state.blocks.toMutableList()
        val block = blocks.getOrNull(index) ?: return@update state
        blocks[index] = block.copy(enabled = !block.enabled)
        state.copy(blocks = blocks)
    }

    fun openBlockEditor(index: Int) = _uiState.update { state ->
        val block = state.blocks.getOrNull(index) ?: return@update state
        state.copy(editingBlock = index to block)
    }

    fun closeBlockEditor() = _uiState.update { it.copy(editingBlock = null) }

    private fun editBlock(index: Int, transform: (ApiCreatorBlock) -> ApiCreatorBlock) {
        _uiState.update { state ->
            val blocks = state.blocks.toMutableList()
            val block = blocks.getOrNull(index) ?: return@update state
            val updated = transform(block)
            blocks[index] = updated
            state.copy(blocks = blocks, editingBlock = index to updated)
        }
    }

    fun updateBlockTitle(index: Int, value: String) = editBlock(index) { it.copy(title = value) }
    fun updateBlockSubtitle(index: Int, value: String) = editBlock(index) { it.copy(subtitle = value) }
    fun updateBlockBody(index: Int, value: String) = editBlock(index) { it.copy(body = value) }
    fun updateBlockCtaLabel(index: Int, value: String) = editBlock(index) { it.copy(ctaLabel = value) }
    fun updateBlockCtaUrl(index: Int, value: String) = editBlock(index) { it.copy(ctaUrl = value) }

    fun addBlockItem(index: Int) = editBlock(index) { it.copy(items = it.items + ApiCreatorBlockItem()) }

    fun removeLastBlockItem(index: Int) = editBlock(index) {
        if (it.items.isEmpty()) it else it.copy(items = it.items.dropLast(1))
    }

    fun updateBlockItem(index: Int, itemIndex: Int, transform: (ApiCreatorBlockItem) -> ApiCreatorBlockItem) {
        editBlock(index) { block ->
            val items = block.items.toMutableList()
            val item = items.getOrNull(itemIndex) ?: return@editBlock block
            items[itemIndex] = transform(item)
            block.copy(items = items)
        }
    }

    // ----- Courses -----

    fun newCourse() = _uiState.update { it.copy(courseDraft = CourseDraft(), transientMessage = null) }

    fun editCourse(course: ApiCreatorCourse) = _uiState.update {
        it.copy(
            courseDraft = CourseDraft(
                id = course.id,
                title = course.title,
                summary = course.summary,
                description = course.description,
                isPaid = !course.isFree,
                price = if (course.isFree) "" else course.price,
                level = course.level,
                durationLabel = course.durationLabel,
                lessonCount = course.lessonCount.toString(),
                seatLimit = course.seatLimit.toString(),
                includes = course.includes.joinToString("\n"),
                tags = course.tags.joinToString(", "),
                coverUrl = course.coverUrl,
                status = course.status,
                featured = course.featured
            ),
            transientMessage = null
        )
    }

    fun updateCourseDraft(transform: (CourseDraft) -> CourseDraft) = _uiState.update {
        it.copy(courseDraft = transform(it.courseDraft))
    }

    fun saveCourse() {
        val state = _uiState.value
        val draft = state.courseDraft
        if (draft.title.isBlank()) {
            _uiState.update { it.copy(transientMessage = "Give the course a title", messageIsError = true) }
            return
        }
        if (draft.isPaid && (draft.price.toDoubleOrNull() ?: 0.0) <= 0.0) {
            _uiState.update { it.copy(transientMessage = "A paid course needs a price above Rs. 0", messageIsError = true) }
            return
        }
        _uiState.update { it.copy(isSavingCourse = true) }

        viewModelScope.launch {
            repository.saveCourse(
                id = draft.id.takeIf { it.isNotBlank() },
                title = draft.title,
                summary = draft.summary,
                description = draft.description,
                isFree = !draft.isPaid,
                price = draft.price.takeIf { draft.isPaid },
                level = draft.level,
                durationLabel = draft.durationLabel,
                lessonCount = draft.lessonCount.toIntOrNull() ?: 0,
                seatLimit = draft.seatLimit.toIntOrNull() ?: 0,
                includes = draft.includes.split('\n').map { it.trim() }.filter { it.isNotEmpty() },
                tags = draft.tags,
                coverUrl = draft.coverUrl,
                status = draft.status,
                featured = draft.featured,
                resourceIds = draft.resourceIds
            ).fold(
                onSuccess = { response ->
                    val saved = response.course
                    _uiState.update { current ->
                        val courses = if (saved == null) {
                            current.courses
                        } else if (current.courses.any { it.id == saved.id }) {
                            current.courses.map { if (it.id == saved.id) saved else it }
                        } else {
                            current.courses + saved
                        }
                        current.copy(
                            isSavingCourse = false,
                            courses = courses,
                            courseDraft = CourseDraft(),
                            transientMessage = response.message.ifBlank { "Course saved" },
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isSavingCourse = false) }
                    showError(failure)
                }
            )
        }
    }

    fun deleteCourse(courseId: String) {
        viewModelScope.launch {
            repository.deleteCourse(courseId).fold(
                onSuccess = {
                    _uiState.update { current ->
                        current.copy(
                            courses = current.courses.filterNot { it.id == courseId },
                            transientMessage = "Course removed",
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure -> showError(failure) }
            )
        }
    }

    // ----- Updates -----

    fun newPost() = _uiState.update { it.copy(postDraft = PostDraft(), transientMessage = null) }

    fun editPost(post: ApiCreatorPost) = _uiState.update {
        it.copy(
            postDraft = PostDraft(
                id = post.id,
                title = post.title,
                body = post.body,
                mediaUrl = post.mediaUrl,
                linkUrl = post.linkUrl,
                pinned = post.pinned,
                published = post.published
            ),
            transientMessage = null
        )
    }

    fun updatePostDraft(transform: (PostDraft) -> PostDraft) = _uiState.update {
        it.copy(postDraft = transform(it.postDraft))
    }

    fun savePost() {
        val draft = _uiState.value.postDraft
        if (draft.body.isBlank() && draft.title.isBlank()) {
            _uiState.update { it.copy(transientMessage = "Write something first", messageIsError = true) }
            return
        }
        _uiState.update { it.copy(isSavingPost = true) }
        viewModelScope.launch {
            repository.savePost(
                id = draft.id.takeIf { it.isNotBlank() },
                title = draft.title,
                body = draft.body,
                mediaUrl = draft.mediaUrl,
                linkUrl = draft.linkUrl,
                pinned = draft.pinned,
                published = draft.published
            ).fold(
                onSuccess = { response ->
                    val saved = response.post
                    _uiState.update { current ->
                        val posts = if (saved == null) {
                            current.posts
                        } else if (current.posts.any { it.id == saved.id }) {
                            current.posts.map { if (it.id == saved.id) saved else it }
                        } else {
                            listOf(saved) + current.posts
                        }
                        current.copy(
                            isSavingPost = false,
                            posts = posts,
                            postDraft = PostDraft(),
                            transientMessage = response.message.ifBlank { "Update posted" },
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isSavingPost = false) }
                    showError(failure)
                }
            )
        }
    }

    fun deletePost(postId: String) {
        viewModelScope.launch {
            repository.deletePost(postId).fold(
                onSuccess = {
                    _uiState.update { current ->
                        current.copy(
                            posts = current.posts.filterNot { it.id == postId },
                            transientMessage = "Update removed",
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure -> showError(failure) }
            )
        }
    }

    private fun showError(failure: Throwable) {
        _uiState.update {
            it.copy(transientMessage = ApiErrorMapper.mapException(failure), messageIsError = true)
        }
    }
}
