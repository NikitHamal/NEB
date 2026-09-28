package com.neb.ians.ui.screens.marketplace

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorEditorSchema
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiCreatorPost
import com.neb.ians.data.api.ApiCreatorTemplate
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

    /** The look, key for key as the server stores it in `page.style`. The app
     *  holds all of them because the server replaces `style` wholesale: a key
     *  the studio cannot carry is a choice it silently erases on the next save. */
    val palette: String = "indigo",
    val scheme: String = "light",
    val font: String = "sans",
    val pattern: String = "none",
    val cardStyle: String = "elevated",
    val pageWidth: String = "standard",
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

    /** The option lists every Look control draws from, straight off the server.
     *  A palette added in `api/creator_themes.py` appears here without an app
     *  release -- and, more to the point, the web and the app can never end up
     *  offering different lists. */
    val schema: ApiCreatorEditorSchema = ApiCreatorEditorSchema(),
    val templates: List<ApiCreatorTemplate> = emptyList(),
    /** Which of the three things "use this template" can mean. See
     *  `apply_template` on the server. */
    val templateMode: String = "page",
    /** The template awaiting confirmation. Applying one rewrites work, so it is
     *  always a deliberate second tap. */
    val pendingTemplate: ApiCreatorTemplate? = null,
    val isApplyingTemplate: Boolean = false,
    val showSectionPicker: Boolean = false,

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
    palette = page.style.palette.ifBlank { "indigo" },
    scheme = page.style.scheme.ifBlank { "light" },
    font = page.style.font.ifBlank { "sans" },
    pattern = page.style.pattern.ifBlank { "none" },
    cardStyle = page.style.card.ifBlank { "elevated" },
    pageWidth = page.style.width.ifBlank { "standard" },
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
        // The option lists and the template gallery, both public reads. They are
        // fetched rather than hardcoded so the app and the web studio can never
        // drift apart on what a palette or a section is called; a failure here
        // leaves the Look tab on its built-in defaults rather than empty.
        repository.editorSchema().onSuccess { schema ->
            _uiState.update { it.copy(schema = schema) }
        }
        repository.templates(_uiState.value.kind.takeIf { it.isNotBlank() }).onSuccess { response ->
            _uiState.update { it.copy(templates = response.templates) }
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

    /**
     * Pick a palette, and move the accent with it.
     *
     * `apply_template` does exactly this on the server, and for the same reason:
     * the marketplace card and the page header read `accent_hex`, so a palette
     * change that leaves the accent behind puts a violet page behind a teal card
     * in the directory. A creator with a brand colour sets it afterwards --
     * that field is still theirs.
     */
    fun updatePalette(value: String) = _uiState.update { state ->
        val accent = state.schema.theme.palettes.firstOrNull { it.id == value }?.accent
        state.copy(palette = value, accentHex = accent ?: state.accentHex)
    }

    /** The accent back to whatever the chosen palette says, which is what almost
     *  everybody wants -- the picker exists for the one creator who does not. */
    fun resetAccentToPalette() = _uiState.update { state ->
        val accent = state.schema.theme.palettes.firstOrNull { it.id == state.palette }?.accent
        if (accent == null) state else state.copy(accentHex = accent)
    }

    fun updateScheme(value: String) = _uiState.update { it.copy(scheme = value) }
    fun updateFont(value: String) = _uiState.update { it.copy(font = value) }
    fun updatePattern(value: String) = _uiState.update { it.copy(pattern = value) }
    fun updateCardStyle(value: String) = _uiState.update { it.copy(cardStyle = value) }
    fun updatePageWidth(value: String) = _uiState.update { it.copy(pageWidth = value) }
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
                    "palette" to kotlinx.serialization.json.JsonPrimitive(state.palette),
                    "scheme" to kotlinx.serialization.json.JsonPrimitive(state.scheme),
                    "font" to kotlinx.serialization.json.JsonPrimitive(state.font),
                    "pattern" to kotlinx.serialization.json.JsonPrimitive(state.pattern),
                    "card" to kotlinx.serialization.json.JsonPrimitive(state.cardStyle),
                    "width" to kotlinx.serialization.json.JsonPrimitive(state.pageWidth),
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

    // ----- Templates -----

    fun chooseTemplateMode(mode: String) = _uiState.update { it.copy(templateMode = mode) }

    /** Ask first. A template rewrites the look, the sections or both, and an
     *  accidental tap that threw away an afternoon's writing would be the worst
     *  thing this screen could do. */
    fun previewTemplate(template: ApiCreatorTemplate) =
        _uiState.update { it.copy(pendingTemplate = template) }

    fun dismissTemplate() = _uiState.update { it.copy(pendingTemplate = null) }

    fun applyPendingTemplate() {
        val state = _uiState.value
        val template = state.pendingTemplate ?: return
        _uiState.update { it.copy(isApplyingTemplate = true) }
        viewModelScope.launch {
            repository.applyTemplate(template.id, state.templateMode).fold(
                onSuccess = { response ->
                    _uiState.update { current ->
                        // The whole studio re-reads the server's copy, because a
                        // template moves the look and the sections together --
                        // adopting half of it would leave the Look tab showing
                        // the old palette over the new sections.
                        val next = response.page?.let(current::adopt) ?: current
                        next.copy(
                            isApplyingTemplate = false,
                            pendingTemplate = null,
                            editingBlock = null,
                            transientMessage = "${template.name} applied.",
                            messageIsError = false
                        )
                    }
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isApplyingTemplate = false, pendingTemplate = null) }
                    showError(failure)
                }
            )
        }
    }

    // ----- Blocks -----

    fun openSectionPicker() = _uiState.update { it.copy(showSectionPicker = true) }
    fun closeSectionPicker() = _uiState.update { it.copy(showSectionPicker = false) }

    fun addBlock(type: String) {
        val state = _uiState.value
        if (state.blocks.size >= state.schema.maxBlocks) {
            _uiState.update {
                it.copy(
                    showSectionPicker = false,
                    transientMessage = "A page holds ${state.schema.maxBlocks} sections. Remove one first.",
                    messageIsError = true
                )
            }
            return
        }
        // A section that takes items opens with one, so the editor has something
        // to show. An empty item list reads as "this section is broken" rather
        // than "fill this in", which is what the old blank editor looked like.
        val takesItems = state.schema.blocks.firstOrNull { it.type == type }
            ?.listKey?.let { it != "images" } ?: false
        val block = ApiCreatorBlock(
            id = "b" + System.currentTimeMillis().toString(36),
            type = type,
            enabled = true,
            items = if (takesItems) listOf(ApiCreatorBlockItem()) else emptyList()
        )
        _uiState.update {
            it.copy(
                blocks = it.blocks + block,
                editingBlock = (it.blocks.size) to block,
                showSectionPicker = false,
                transientMessage = "Section added — save to publish it",
                messageIsError = false
            )
        }
    }

    /** A copy, just below the original. Two price tables or three showcase rows
     *  is the normal shape of a storefront, and rebuilding the second by hand is
     *  the kind of work a builder is supposed to remove. */
    fun duplicateBlock(index: Int) = _uiState.update { state ->
        val source = state.blocks.getOrNull(index) ?: return@update state
        val blocks = state.blocks.toMutableList()
        blocks.add(index + 1, source.copy(id = "b" + System.currentTimeMillis().toString(36)))
        state.copy(
            blocks = blocks,
            editingBlock = null,
            transientMessage = "Section duplicated.",
            messageIsError = false
        )
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
    fun updateBlockMediaUrl(index: Int, value: String) = editBlock(index) { it.copy(mediaUrl = value) }

    // ----- A section's own look -----
    //
    // Alignment, background, width and column count, per section. These are what
    // let one page have a centred quote on the accent between two plain
    // left-aligned shelves, which is the difference between a page that looks
    // designed and a page that looks like a form.
    //
    // `blocksPayload` drops any of these that still equals its default, matching
    // `sanitize_block_settings` on the server -- so a creator who never opens
    // these controls sends exactly what they sent before they existed.

    fun updateBlockAlign(index: Int, value: String) =
        editBlock(index) { it.copy(settings = it.settings.copy(align = value)) }

    fun updateBlockTone(index: Int, value: String) =
        editBlock(index) { it.copy(settings = it.settings.copy(tone = value)) }

    fun updateBlockWidth(index: Int, value: String) =
        editBlock(index) { it.copy(settings = it.settings.copy(width = value)) }

    /** 0 means "however many fit", which is what the shelves do by default. */
    fun updateBlockColumns(index: Int, value: Int) =
        editBlock(index) { it.copy(settings = it.settings.copy(columns = value.coerceIn(0, 4))) }

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

    fun addBlockItem(index: Int) = editBlock(index) { block ->
        if (block.items.size >= _uiState.value.schema.maxItems) block
        else block.copy(items = block.items + ApiCreatorBlockItem())
    }

    fun removeLastBlockItem(index: Int) = editBlock(index) {
        if (it.items.isEmpty()) it else it.copy(items = it.items.dropLast(1))
    }

    /** Remove the item a creator is looking at, not the last one. Deleting the
     *  wrong row because the only delete was "remove last" is the sort of thing
     *  that makes somebody retype a price table. */
    fun removeBlockItem(index: Int, itemIndex: Int) = editBlock(index) { block ->
        if (itemIndex !in block.items.indices) block
        else block.copy(items = block.items.toMutableList().also { it.removeAt(itemIndex) })
    }

    fun moveBlockItem(index: Int, itemIndex: Int, delta: Int) = editBlock(index) { block ->
        val target = itemIndex + delta
        if (itemIndex !in block.items.indices || target !in block.items.indices) block
        else block.copy(
            items = block.items.toMutableList().also { it.add(target, it.removeAt(itemIndex)) }
        )
    }

    fun removeBlockImage(index: Int, imageIndex: Int) = editBlock(index) { block ->
        if (imageIndex !in block.images.indices) block
        else block.copy(images = block.images.toMutableList().also { it.removeAt(imageIndex) })
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
