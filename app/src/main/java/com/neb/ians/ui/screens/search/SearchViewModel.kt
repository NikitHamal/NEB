package com.neb.ians.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SearchHistoryRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

enum class SearchScope(val label: String) {
    All("All"),
    Resources("Resources"),
    Posts("Posts"),
    People("People")
}

data class SearchUiState(
    val query: String = "",
    val resources: List<ApiResource> = emptyList(),
    val posts: List<ApiPost> = emptyList(),
    val users: List<ApiUserSearchResult> = emptyList(),
    val recentQueries: List<String> = emptyList(),
    val scope: SearchScope = SearchScope.All,
    val isSearching: Boolean = false,
    val hasSearched: Boolean = false,
    val selectedSubject: String? = null,
    val selectedGradeLevel: String? = null,
    val selectedType: String? = null,
    val error: String? = null
) {
    val activeFilterCount: Int
        get() = listOfNotNull(selectedSubject, selectedGradeLevel, selectedType).size

    val totalCount: Int get() = resources.size + posts.size + users.size

    val isEmptyResult: Boolean
        get() = hasSearched && !isSearching && error == null && totalCount == 0

    fun countFor(scope: SearchScope): Int = when (scope) {
        SearchScope.All -> totalCount
        SearchScope.Resources -> resources.size
        SearchScope.Posts -> posts.size
        SearchScope.People -> users.size
    }

    companion object {
        val SUGGESTIONS = listOf(
            "Physics", "Chemistry", "Mathematics", "Biology",
            "English", "Notes", "Textbook", "Past Papers"
        )
        const val MIN_QUERY_LENGTH = 2
    }
}

@HiltViewModel
class SearchViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val searchHistoryRepository: SearchHistoryRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            searchHistoryRepository.recentQueries.collect { recents ->
                _uiState.update { it.copy(recentQueries = recents) }
            }
        }
        viewModelScope.launch {
            try {
                val profile = authRepository.userProfileFlow.first()
                if (profile != null && !isGlobalUser(profile)) {
                    val gradePref = mapProfileGrade(profile.classLevel)
                    if (gradePref != null) {
                        _uiState.update { it.copy(selectedGradeLevel = gradePref) }
                    }
                }
            } catch (_: Exception) {}
        }
    }

    private fun isGlobalUser(profile: com.neb.ians.data.repository.UserProfileCache): Boolean {
        val role = profile.role?.trim()?.lowercase() ?: ""
        if (role in listOf("teacher", "institution", "explorer")) return true
        val classLevel = profile.classLevel?.trim()?.lowercase() ?: ""
        val globalClasses = setOf("+2 passout", "+2 passout / bachelor", "bachelor", "bachelor's", "master", "master's", "phd", "diploma")
        if (classLevel in globalClasses) return true
        return false
    }

    private fun mapProfileGrade(classLevel: String?): String? {
        if (classLevel.isNullOrBlank()) return null
        val clean = classLevel.trim().lowercase()
        return when (clean) {
            "11", "grade 11", "class 11" -> "Class 11"
            "12", "grade 12", "class 12" -> "Class 12"
            "10", "see", "class 10", "class 10 / see" -> "Class 10 / SEE"
            "9", "class 9" -> "Class 9"
            "8", "class 8" -> "Class 8"
            else -> null
        }
    }

    private var searchJob: Job? = null
    private var lastRequest: String? = null

    fun onQueryChange(query: String) {
        val normalized = query.trimStart()
        if (normalized == _uiState.value.query) return
        _uiState.update { it.copy(query = normalized) }
        triggerSearch(normalized)
    }

    fun onScopeChange(scope: SearchScope) {
        if (_uiState.value.scope == scope) return
        _uiState.update { it.copy(scope = scope) }
    }

    fun submitQuery() {
        val query = _uiState.value.query.trim()
        if (query.length < SearchUiState.MIN_QUERY_LENGTH) return
        viewModelScope.launch { searchHistoryRepository.record(query) }
        if (lastRequest != requestKey(query)) triggerSearch(query, immediate = true)
    }

    fun removeRecent(query: String) {
        viewModelScope.launch { searchHistoryRepository.remove(query) }
    }

    fun clearRecents() {
        viewModelScope.launch { searchHistoryRepository.clear() }
    }

    fun selectSubject(subject: String?) {
        val newSubject = if (_uiState.value.selectedSubject == subject) null else subject
        _uiState.update { it.copy(selectedSubject = newSubject) }
        triggerSearch(_uiState.value.query, immediate = true)
    }

    fun selectGradeLevel(gradeLevel: String?) {
        val newGrade = if (_uiState.value.selectedGradeLevel == gradeLevel) null else gradeLevel
        _uiState.update { it.copy(selectedGradeLevel = newGrade) }
        triggerSearch(_uiState.value.query, immediate = true)
    }

    fun selectType(type: String?) {
        val newType = if (_uiState.value.selectedType == type) null else type
        _uiState.update { it.copy(selectedType = newType) }
        triggerSearch(_uiState.value.query, immediate = true)
    }

    fun clearFilters() {
        _uiState.update { it.copy(selectedSubject = null, selectedGradeLevel = null, selectedType = null) }
        triggerSearch(_uiState.value.query, immediate = true)
    }

    fun retry() {
        triggerSearch(_uiState.value.query, immediate = true)
    }

    private fun requestKey(query: String): String {
        val state = _uiState.value
        return listOf(
            query.trim().lowercase(),
            state.selectedSubject.orEmpty(),
            state.selectedGradeLevel.orEmpty(),
            state.selectedType.orEmpty()
        ).joinToString("|")
    }

    private fun triggerSearch(query: String, immediate: Boolean = false) {
        searchJob?.cancel()
        val trimmed = query.trim()
        if (trimmed.length < SearchUiState.MIN_QUERY_LENGTH) {
            lastRequest = null
            _uiState.update {
                it.copy(
                    resources = emptyList(),
                    posts = emptyList(),
                    users = emptyList(),
                    isSearching = false,
                    hasSearched = false,
                    error = null
                )
            }
            return
        }

        searchJob = viewModelScope.launch {
            if (!immediate) delay(DEBOUNCE_MS)
            performSearch(trimmed)
        }
    }

    private suspend fun performSearch(query: String) {
        val key = requestKey(query)
        lastRequest = key
        _uiState.update { it.copy(isSearching = true, error = null) }
        try {
            val token = authRepository.getBearerToken()
            val state = _uiState.value
            val response = apiService.search(
                bearerToken = token,
                query = query,
                subject = state.selectedSubject,
                grade = state.selectedGradeLevel,
                type = state.selectedType,
                pageSize = 30
            )
            val users = response.users.ifEmpty {
                runCatching { apiService.searchUsers(token, query) }.getOrDefault(emptyList())
            }
            if (lastRequest != key) return
            _uiState.update {
                it.copy(
                    resources = response.resources,
                    posts = response.posts,
                    users = users,
                    isSearching = false,
                    hasSearched = true
                )
            }
        } catch (e: Exception) {
            if (lastRequest != key) return
            _uiState.update {
                it.copy(
                    isSearching = false,
                    hasSearched = true,
                    error = ApiErrorMapper.mapException(e)
                )
            }
        }
    }

    override fun onCleared() {
        searchJob?.cancel()
        super.onCleared()
    }

    fun clearSearch() {
        searchJob?.cancel()
        lastRequest = null
        _uiState.update {
            it.copy(
                query = "",
                resources = emptyList(),
                posts = emptyList(),
                users = emptyList(),
                scope = SearchScope.All,
                isSearching = false,
                hasSearched = false,
                error = null
            )
        }
    }

    private companion object {
        const val DEBOUNCE_MS = 240L
    }
}
