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
import com.neb.ians.data.api.ApiWithdrawal
import com.neb.ians.data.repository.MarketplaceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.map
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
    val kind: String = "tutor",
    /** The page types this account is allowed to be. One entry means no choice
     *  to offer, so the studio hides the row -- same rule as the web studio. */
    val allowedKinds: List<String> = emptyList(),
    val subjects: String = "",
    val languages: String = "",
    /** Handle per network, in the order the fields are drawn. Blank values are
     *  dropped on save, so clearing a field removes the link. */
    val socials: Map<String, String> = emptyMap(),
    val location: String = "",
    val contactEmail: String = "",
    val contactPhone: String = "",
    val avatarUrl: String = "",
    val coverUrl: String = "",
    val accentHex: String = "#004BD4",
    val layout: String = "editorial",
    val heroStyle: String = "art",
    val radius: String = "round",
    val density: String = "comfortable",
    val galleryColumns: Int = 3,
    val showStats: Boolean = false,
    val showContact: Boolean = true,
    val showVerified: Boolean = true,
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
    val withdrawals: List<ApiWithdrawal> = emptyList(),
    val withdrawAmount: String = "",
    val withdrawMethod: String = "esewa",
    val withdrawDetails: String = "",
    val isRequestingWithdrawal: Boolean = false,
    val resourceOptions: List<Pair<String, String>> = emptyList()
)

/**
 * Take the server's copy of the page as the truth for every editable field.
 *
 * Both loading and saving end here, because both end with a page the server
 * sanitized: `_clean_url` drops an address with no scheme, `sanitize_accent`
 * replaces a colour it cannot read, `sanitize_blocks` throws away fields a
 * section type does not have. A studio that kept showing what was typed would
 * be showing something that is not saved -- and would send it again next time.
 */
private fun CreatorStudioUiState.adopt(page: ApiCreatorPage): CreatorStudioUiState = copy(
    page = page,
    displayName = page.displayName,
    tagline = page.tagline,
    about = page.about,
    slug = page.slug,
    kind = page.kind,
    subjects = page.subjects.joinToString(", "),
    languages = page.languages.joinToString(", "),
    socials = socialFields(page.socials),
    location = page.location,
    contactEmail = page.contactEmail,
    contactPhone = page.contactPhone,
    avatarUrl = page.avatarUrl,
    coverUrl = page.coverUrl,
    accentHex = page.accentHex,
    layout = page.layout,
    heroStyle = page.style.hero.ifBlank { "art" },
    radius = page.style.radius.ifBlank { "round" },
    density = page.style.density.ifBlank { "comfortable" },
    galleryColumns = page.style.galleryColumns,
    showStats = page.style.showStats,
    showContact = page.style.showContact,
    showVerified = page.style.showVerified,
    acceptingStudents = page.acceptingStudents,
    blocks = page.blocks,
    courses = page.courses,
    resourceOptions = page.resources.take(60).map { it.id to it.title }
)

/** The networks the creator already filled in, plus the ones the web studio
 *  offers by default, so both studios show the same four empty boxes to
 *  somebody who has never added a link. */
private fun socialFields(saved: Map<String, String>): Map<String, String> {
    val fields = linkedMapOf<String, String>()
    saved.forEach { (key, value) -> fields[key] = value }
    listOf("website", "youtube", "instagram", "facebook").forEach { key -> fields.putIfAbsent(key, "") }
    return fields
}

@HiltViewModel
class CreatorStudioViewModel @Inject constructor(
    private val repository: MarketplaceRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CreatorStudioUiState())
    val uiState: StateFlow<CreatorStudioUiState> = _uiState.asStateFlow()

    init {
        load()
        // Every message clears itself after a few seconds, the way the web
        // studio's toast does -- otherwise "Section added" stays pinned above
        // the earnings tab for the rest of the session.
        viewModelScope.launch {
            _uiState.map { it.transientMessage }.distinctUntilChanged().collectLatest { message ->
                if (message != null) {
                    delay(MESSAGE_VISIBLE_MS)
                    _uiState.update { if (it.transientMessage == message) it.copy(transientMessage = null) else it }
                }
            }
        }
    }

    fun load() {
        viewModelScope.launch { refresh() }
    }

    /** The same load, awaitable, so the pull-to-refresh spinner lasts as long as
     *  the requests do. */
    suspend fun refresh() {
        _uiState.update { it.copy(isLoading = it.page == null, error = null) }
        repository.myPage().fold(
            onSuccess = { response ->
                if (!response.eligible || response.page == null) {
                    _uiState.update {
                        it.copy(isLoading = false, notEligible = !response.eligible, page = response.page)
                    }
                    return@fold
                }
                _uiState.update { current ->
                    current.adopt(response.page).copy(
                        isLoading = false,
                        notEligible = false,
                        error = null,
                        allowedKinds = response.yourKinds
                    )
                }
            },
            onFailure = { failure ->
                _uiState.update {
                    it.copy(isLoading = false, error = ApiErrorMapper.mapException(failure))
                }
            }
        )
        // `page_payload` caps its posts at 12 for everybody, so the studio asks
        // for its own list -- an owner with forty updates has to be able to reach
        // the older ones to edit or delete them.
        repository.myPosts().onSuccess { response ->
            _uiState.update { it.copy(posts = response.posts) }
        }
        loadDashboard()
    }

    private suspend fun loadDashboard() {
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
        repository.withdrawals().onSuccess { response ->
            _uiState.update { it.copy(withdrawals = response.withdrawals) }
        }
    }

    // ----- Withdrawals -----

    fun updateWithdrawAmount(value: String) =
        _uiState.update { it.copy(withdrawAmount = value.filter { c -> c.isDigit() || c == '.' }) }

    fun updateWithdrawMethod(value: String) = _uiState.update { it.copy(withdrawMethod = value) }
    fun updateWithdrawDetails(value: String) = _uiState.update { it.copy(withdrawDetails = value) }

    fun requestWithdrawal() {
        val state = _uiState.value
        val amount = state.withdrawAmount.trim().toBigDecimalOrNull()
        val minimum = state.wallet.withdrawMin.toBigDecimalOrNull()
        // The server checks all of this again; catching it here just saves the
        // creator a round trip to be told their own numbers.
        if (amount == null || amount.signum() <= 0) {
            _uiState.update { it.copy(transientMessage = "Enter the amount you want to withdraw", messageIsError = true) }
            return
        }
        if (minimum != null && amount < minimum) {
            _uiState.update {
                it.copy(transientMessage = "Withdrawals start at Rs. ${state.wallet.withdrawMin}", messageIsError = true)
            }
            return
        }
        val available = state.wallet.currentBalance.toBigDecimalOrNull()
        if (available != null && amount > available) {
            _uiState.update {
                it.copy(
                    transientMessage = "You have Rs. ${state.wallet.currentBalance} available right now",
                    messageIsError = true
                )
            }
            return
        }
        if (state.withdrawDetails.isBlank()) {
            _uiState.update { it.copy(transientMessage = "Add the account we should pay into", messageIsError = true) }
            return
        }
        _uiState.update { it.copy(isRequestingWithdrawal = true) }
        viewModelScope.launch {
            repository.requestWithdrawal(
                amount = state.withdrawAmount.trim(),
                payoutMethod = state.withdrawMethod,
                payoutDetails = state.withdrawDetails.trim()
            ).fold(
                onSuccess = { withdrawal ->
                    _uiState.update {
                        it.copy(
                            isRequestingWithdrawal = false,
                            withdrawAmount = "",
                            withdrawDetails = "",
                            transientMessage = withdrawal.message.ifBlank {
                                "Withdrawal requested. Funds arrive within 7 days."
                            },
                            messageIsError = false
                        )
                    }
                    loadDashboard()
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isRequestingWithdrawal = false) }
                    showError(failure)
                }
            )
        }
    }

    // ----- Page fields -----

    fun updateDisplayName(value: String) = _uiState.update { it.copy(displayName = value) }
    fun updateTagline(value: String) = _uiState.update { it.copy(tagline = value) }
    fun updateAbout(value: String) = _uiState.update { it.copy(about = value) }
    fun updateSlug(value: String) = _uiState.update { it.copy(slug = value.lowercase().filter { c -> c.isLetterOrDigit() || c == '-' }) }
    fun updateSubjects(value: String) = _uiState.update { it.copy(subjects = value) }
    fun updateLanguages(value: String) = _uiState.update { it.copy(languages = value) }
    fun updateKind(value: String) = _uiState.update { it.copy(kind = value) }
    fun updateSocial(network: String, value: String) =
        _uiState.update { it.copy(socials = it.socials + (network to value)) }
    fun updateLocation(value: String) = _uiState.update { it.copy(location = value) }
    fun updateContactEmail(value: String) = _uiState.update { it.copy(contactEmail = value) }
    fun updateContactPhone(value: String) = _uiState.update { it.copy(contactPhone = value) }
    fun updateAvatarUrl(value: String) = _uiState.update { it.copy(avatarUrl = value) }
    fun updateCoverUrl(value: String) = _uiState.update { it.copy(coverUrl = value) }
    fun updateAccent(value: String) = _uiState.update { it.copy(accentHex = value) }
    fun updateLayout(value: String) = _uiState.update { it.copy(layout = value) }
    fun updateHeroStyle(value: String) = _uiState.update { it.copy(heroStyle = value) }
    fun updateRadius(value: String) = _uiState.update { it.copy(radius = value) }
    fun updateDensity(value: String) = _uiState.update { it.copy(density = value) }
    fun updateGalleryColumns(value: Int) = _uiState.update { it.copy(galleryColumns = value.coerceIn(2, 4)) }
    fun updateShowStats(value: Boolean) = _uiState.update { it.copy(showStats = value) }
    fun updateShowContact(value: Boolean) = _uiState.update { it.copy(showContact = value) }
    fun updateShowVerified(value: Boolean) = _uiState.update { it.copy(showVerified = value) }
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
                kind = state.kind.takeIf { it.isNotBlank() && it in state.allowedKinds },
                subjects = state.subjects.split(',').map { it.trim() }.filter { it.isNotEmpty() },
                languages = state.languages.split(',').map { it.trim() }.filter { it.isNotEmpty() },
                blocks = repository.blocksPayload(state.page!!.copy(blocks = state.blocks)),
                acceptingStudents = state.acceptingStudents,
                // The server replaces `page.style` wholesale, so every key the
                // studio does not send is a key the creator loses. These are the
                // values loaded from their page, edited here, sent back whole --
                // saving from the app must not undo a choice made on the web.
                style = mapOf(
                    "hero" to kotlinx.serialization.json.JsonPrimitive(state.heroStyle),
                    "radius" to kotlinx.serialization.json.JsonPrimitive(state.radius),
                    "density" to kotlinx.serialization.json.JsonPrimitive(state.density),
                    "show_stats" to kotlinx.serialization.json.JsonPrimitive(state.showStats),
                    "show_contact" to kotlinx.serialization.json.JsonPrimitive(state.showContact),
                    "show_verified" to kotlinx.serialization.json.JsonPrimitive(state.showVerified),
                    "gallery_columns" to kotlinx.serialization.json.JsonPrimitive(state.galleryColumns)
                ),
                socials = state.socials
            ).fold(
                onSuccess = { response ->
                    _uiState.update { current ->
                        // The server sanitizes as it saves -- a URL without a
                        // scheme is dropped, an accent it cannot parse goes back
                        // to the default. Adopting its copy is how the creator
                        // finds that out, instead of the field still showing
                        // what they typed under a "Page saved".
                        val next = response.page?.let(current::adopt) ?: current
                        next.copy(
                            isSavingPage = false,
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
                // The editor addresses its section by position, so a reorder has
                // to move the editor with it -- otherwise the next keystroke
                // rewrites whichever section took this slot.
                val editing = state.editingBlock?.let { (editingIndex, block) ->
                    when (editingIndex) {
                        index -> target to block
                        in minOf(index, target)..maxOf(index, target) ->
                            (if (target > index) editingIndex - 1 else editingIndex + 1) to block
                        else -> editingIndex to block
                    }
                }
                state.copy(blocks = blocks, editingBlock = editing)
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
    fun updateBlockImageUrl(index: Int, value: String) = editBlock(index) { it.copy(imageUrl = value) }

    // A gallery is a list of picture URLs rather than a list of items, so it gets
    // its own three calls instead of sharing the item ones.
    fun addBlockImage(index: Int) = editBlock(index) { it.copy(images = it.images + "") }

    fun removeLastBlockImage(index: Int) = editBlock(index) {
        if (it.images.isEmpty()) it else it.copy(images = it.images.dropLast(1))
    }

    fun updateBlockImage(index: Int, imageIndex: Int, value: String) = editBlock(index) { block ->
        val images = block.images.toMutableList()
        if (imageIndex !in images.indices) return@editBlock block
        images[imageIndex] = value
        block.copy(images = images)
    }

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
                featured = course.featured,
                // Without this the picker would open with nothing ticked and the
                // save would detach every note the offering already had.
                resourceIds = course.resourceIds
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

    private companion object {
        /** Matches the web studio's toast (`_toastTimer`, 4.2s). */
        const val MESSAGE_VISIBLE_MS = 4_200L
    }

    private fun showError(failure: Throwable) {
        _uiState.update {
            it.copy(transientMessage = ApiErrorMapper.mapException(failure), messageIsError = true)
        }
    }

}
