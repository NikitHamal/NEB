package com.neb.ians.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SearchUiState(
    val query: String = "",
    val resources: List<ApiResource> = emptyList(),
    val posts: List<ApiPost> = emptyList(),
    val users: List<ApiUserSearchResult> = emptyList(),
    val isSearching: Boolean = false,
    val selectedSubject: String? = null,
    val selectedGradeLevel: String? = null,
    val selectedType: String? = null,
    val error: String? = null
) {
    companion object {
        val SUGGESTIONS = listOf(
            "Physics", "Chemistry", "Mathematics", "Biology",
            "English", "Notes", "Textbook", "Past Papers"
        )
    }
}

@HiltViewModel
class SearchViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    private var searchJob: Job? = null

    fun onQueryChange(query: String) {
        val normalized = query.trimStart()
        _uiState.update { it.copy(query = normalized) }
        triggerSearch(normalized)
    }

    fun selectSubject(subject: String?) {
        val newSubject = if (_uiState.value.selectedSubject == subject) null else subject
        _uiState.update { it.copy(selectedSubject = newSubject) }
        triggerSearch(_uiState.value.query)
    }

    fun selectGradeLevel(gradeLevel: String?) {
        val newGrade = if (_uiState.value.selectedGradeLevel == gradeLevel) null else gradeLevel
        _uiState.update { it.copy(selectedGradeLevel = newGrade) }
        triggerSearch(_uiState.value.query)
    }

    fun selectType(type: String?) {
        val newType = if (_uiState.value.selectedType == type) null else type
        _uiState.update { it.copy(selectedType = newType) }
        triggerSearch(_uiState.value.query)
    }

    fun clearFilters() {
        _uiState.update { it.copy(selectedSubject = null, selectedGradeLevel = null, selectedType = null) }
        triggerSearch(_uiState.value.query)
    }

    private fun triggerSearch(query: String) {
        searchJob?.cancel()
        if (query.length < 2) {
            _uiState.update {
                it.copy(
                    resources = emptyList(),
                    posts = emptyList(),
                    users = emptyList(),
                    isSearching = false,
                    error = null
                )
            }
            return
        }

        searchJob = viewModelScope.launch {
            delay(260)
            performSearch(query)
        }
    }

    private suspend fun performSearch(query: String) {
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
            if (_uiState.value.query != query) return
            _uiState.update {
                it.copy(
                    resources = response.resources,
                    posts = response.posts,
                    users = users,
                    isSearching = false
                )
            }
        } catch (e: Exception) {
            if (_uiState.value.query == query) {
                _uiState.update { it.copy(isSearching = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    override fun onCleared() {
        searchJob?.cancel()
        super.onCleared()
    }

    fun clearSearch() {
        searchJob?.cancel()
        _uiState.value = SearchUiState()
    }
}