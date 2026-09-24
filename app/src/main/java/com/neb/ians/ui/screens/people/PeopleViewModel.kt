package com.neb.ians.ui.screens.people

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.FollowStateRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.PeopleSuggestionRepository
import com.neb.ians.data.repository.PersonSuggestion
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
    val reason: String?,
    val followsYou: Boolean,
    val isFollowing: Boolean
) {
    val followLabel: String
        get() = when {
            isFollowing -> "Following"
            followsYou -> "Follow back"
            else -> "Follow"
        }
}

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
 * Ranking and filtering live in [PeopleSuggestionRepository] so the home rail
 * and this screen show the same people for the same reasons. Typing hands over
 * to the user search endpoint, which is the one place the server knows about
 * people no signal has surfaced yet.
 */
@OptIn(FlowPreview::class)
@HiltViewModel
class PeopleViewModel @Inject constructor(
    private val forumRepository: ForumRepository,
    private val authRepository: AuthRepository,
    private val followStateRepository: FollowStateRepository,
    private val peopleSuggestionRepository: PeopleSuggestionRepository,
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
            val result = peopleSuggestionRepository.load(forceRefresh)
            _uiState.update { state ->
                state.copy(
                    suggestions = result.getOrNull().orEmpty().map { it.toCandidate() },
                    isLoading = false,
                    error = result.exceptionOrNull()?.let { ApiErrorMapper.mapException(it) }
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
            val graph = followStateRepository.graph.value
            _uiState.update { state ->
                state.copy(
                    results = results.mapNotNull { it.toCandidate(graph) },
                    isSearching = false
                )
            }
        }
    }

    fun toggleFollow(candidate: PeopleCandidate) {
        if (candidate.id.isBlank() || !pendingFollows.add(candidate.id)) return
        val optimistic = !candidate.isFollowing
        setFollowing(candidate.id, optimistic)
        followStateRepository.record(candidate.id, candidate.username, optimistic)
        peopleSuggestionRepository.record(candidate.id, candidate.username, optimistic)
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: throw IllegalStateException("Not authenticated")
                val response = apiService.toggleFollow(token, candidate.id)
                setFollowing(candidate.id, response.isFollowing)
                followStateRepository.record(candidate.id, candidate.username, response.isFollowing)
                peopleSuggestionRepository.record(candidate.id, candidate.username, response.isFollowing)
            } catch (e: Exception) {
                setFollowing(candidate.id, candidate.isFollowing)
                followStateRepository.record(candidate.id, candidate.username, candidate.isFollowing)
                peopleSuggestionRepository.record(candidate.id, candidate.username, candidate.isFollowing)
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

    private fun PersonSuggestion.toCandidate(): PeopleCandidate = PeopleCandidate(
        id = id,
        username = username,
        name = name,
        photoUrl = photoUrl,
        detail = detail,
        reason = reason,
        followsYou = followsYou,
        isFollowing = isFollowing
    )

    private fun ApiUserSearchResult.toCandidate(graph: FollowStateRepository.Graph): PeopleCandidate? {
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
            reason = null,
            followsYou = false,
            isFollowing = isFollowing == true || graph.contains(id, username)
        )
    }

}
