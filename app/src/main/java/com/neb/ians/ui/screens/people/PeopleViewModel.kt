package com.neb.ians.ui.screens.people

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PeopleCandidate(
    val id: String,
    val username: String,
    val name: String,
    val photoUrl: String?,
    val detail: String?,
    val isFollowing: Boolean
)

data class PeopleUiState(
    val query: String = "",
    val suggestions: List<PeopleCandidate> = emptyList(),
    val results: List<PeopleCandidate> = emptyList(),
    val isLoading: Boolean = true,
    val isSearching: Boolean = false,
    val error: String? = null
) {
    val searching: Boolean get() = query.isNotBlank()
    val visible: List<PeopleCandidate> get() = if (searching) results else suggestions
}

/**
 * Everyone the app can plausibly suggest, in one place.
 *
 * There is no suggestions endpoint on the server, so the list is built the same
 * way the home rail's was — the authors of recent posts the user does not follow
 * yet — only paged deep enough to be a screen rather than a strip. Typing hands
 * over to the user search endpoint, which is the one place the server does know
 * about people the feed has never mentioned.
 */
@OptIn(FlowPreview::class)
@HiltViewModel
class PeopleViewModel @Inject constructor(
    private val forumRepository: ForumRepository,
    private val authRepository: AuthRepository,
    private val apiService: ApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(PeopleUiState())
    val uiState: StateFlow<PeopleUiState> = _uiState.asStateFlow()

    private val queryFlow = MutableStateFlow("")
    private val pendingFollows = mutableSetOf<String>()
    private var searchJob: Job? = null

    init {
        loadSuggestions()
        viewModelScope.launch {
            queryFlow
                .debounce(300)
                .distinctUntilChanged()
                .collect { q -> runSearch(q.trim()) }
        }
    }

    fun onQueryChange(value: String) {
        _uiState.update { it.copy(query = value, results = if (value.isBlank()) emptyList() else it.results) }
        queryFlow.value = value
    }

    fun refresh() = loadSuggestions(forceRefresh = true)

    private fun loadSuggestions(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val selfId = authRepository.currentUserIdFlow.first()
            val collected = LinkedHashMap<String, PeopleCandidate>()
            var failure: Throwable? = null

            for (page in 1..PAGE_DEPTH) {
                val posts = forumRepository
                    .getPosts(page = page, forceRefresh = forceRefresh && page == 1)
                    .onFailure { error -> if (collected.isEmpty()) failure = error }
                    .getOrNull() ?: break
                posts.posts.forEach { post -> post.toCandidate(selfId)?.let { collected.putIfAbsent(it.id, it) } }
                if (collected.size >= TARGET_COUNT || !posts.hasMore) break
            }

            _uiState.update {
                it.copy(
                    suggestions = collected.values.toList(),
                    isLoading = false,
                    error = failure?.let { e -> ApiErrorMapper.mapException(e) }
                )
            }
        }
    }

    private fun runSearch(query: String) {
        searchJob?.cancel()
        if (query.length < 2) {
            _uiState.update { it.copy(results = emptyList(), isSearching = false) }
            return
        }
        searchJob = viewModelScope.launch {
            _uiState.update { it.copy(isSearching = true) }
            val results = forumRepository.searchUsers(query).getOrNull().orEmpty()
            _uiState.update { state ->
                state.copy(results = results.mapNotNull { it.toCandidate() }, isSearching = false)
            }
        }
    }

    fun toggleFollow(candidate: PeopleCandidate) {
        if (candidate.id.isBlank() || !pendingFollows.add(candidate.id)) return
        val optimistic = !candidate.isFollowing
        setFollowing(candidate.id, optimistic)
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: throw IllegalStateException("Not authenticated")
                val response = apiService.toggleFollow(token, candidate.id)
                setFollowing(candidate.id, response.isFollowing)
            } catch (e: Exception) {
                setFollowing(candidate.id, candidate.isFollowing)
            } finally {
                pendingFollows.remove(candidate.id)
            }
        }
    }

    private fun setFollowing(id: String, following: Boolean) {
        _uiState.update { state ->
            state.copy(
                suggestions = state.suggestions.map { if (it.id == id) it.copy(isFollowing = following) else it },
                results = state.results.map { if (it.id == id) it.copy(isFollowing = following) else it }
            )
        }
    }

    private fun ApiPost.toCandidate(selfId: String?): PeopleCandidate? {
        if (authorId.isBlank() || authorName.isBlank()) return null
        if (authorId == selfId || isAnonymous || authorIsBot) return null
        if (authorName.contains("Anonymous", ignoreCase = true)) return null
        if (isFollowingAuthor == true) return null
        return PeopleCandidate(
            id = authorId,
            username = authorName,
            name = authorName,
            photoUrl = authorPhotoUrl,
            detail = authorBadgeInfo?.label?.takeIf { it.isNotBlank() } ?: authorBadge,
            isFollowing = false
        )
    }

    private fun ApiUserSearchResult.toCandidate(): PeopleCandidate? {
        if (isSelf == true || id.isBlank()) return null
        return PeopleCandidate(
            id = id,
            username = username,
            name = displayName?.takeIf { it.isNotBlank() } ?: username,
            photoUrl = photoUrl,
            detail = listOfNotNull(
                classLevel?.takeIf { it.isNotBlank() },
                school?.takeIf { it.isNotBlank() }
            ).joinToString(" · ").takeIf { it.isNotBlank() } ?: badgeInfo?.label?.takeIf { it.isNotBlank() },
            isFollowing = isFollowing == true
        )
    }

    private companion object {
        const val PAGE_DEPTH = 4
        const val TARGET_COUNT = 30
    }
}
