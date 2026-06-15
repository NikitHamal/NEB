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
    val error: String? = null
) {
    companion object {
        val SUGGESTIONS = listOf(
            "Physics notes", "Chemistry textbook", "Math past papers",
            "Biology guide", "English grammar", "Computer Science"
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
        searchJob?.cancel()

        if (normalized.length < 2) {
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
            performSearch(normalized)
        }
    }

    private suspend fun performSearch(query: String) {
        _uiState.update { it.copy(isSearching = true, error = null) }
        try {
            val token = authRepository.getBearerToken()
            val response = apiService.search(token, query, pageSize = 30)
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