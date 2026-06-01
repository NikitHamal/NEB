package com.neb.ians.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
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

    fun onQueryChange(query: String) {
        _uiState.update { it.copy(query = query) }
        if (query.length >= 2) {
            performSearch(query)
        } else {
            _uiState.update { it.copy(resources = emptyList(), posts = emptyList(), users = emptyList(), isSearching = false, error = null) }
        }
    }

    private fun performSearch(query: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isSearching = true, error = null) }
            try {
                val token = authRepository.getBearerToken()
                val response = apiService.search(token, query)
                _uiState.update {
                    it.copy(
                        resources = response.resources,
                        posts = response.posts,
                        users = response.users,
                        isSearching = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSearching = false, error = e.message ?: "Search failed") }
            }
        }
    }

    fun clearSearch() {
        _uiState.value = SearchUiState()
    }
}