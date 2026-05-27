package com.neb.ians.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SearchUiState(
    val query: String = "",
    val results: List<ResourceEntity> = emptyList(),
    val isSearching: Boolean = false,
    val recentSearches: List<String> = emptyList(),
    val suggestions: List<String> = listOf(
        "Physics notes", "Chemistry textbook", "Math past papers",
        "Biology guide", "English grammar", "Computer Science"
    )
)

@HiltViewModel
class SearchViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    fun onQueryChange(query: String) {
        _uiState.update { it.copy(query = query) }
        if (query.length >= 2) {
            search(query)
        } else {
            _uiState.update { it.copy(results = emptyList(), isSearching = false) }
        }
    }

    private fun search(query: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isSearching = true) }
            resourceRepository.searchResources(query).collect { results ->
                _uiState.update { it.copy(results = results, isSearching = false) }
            }
        }
    }

    fun clearSearch() {
        _uiState.update { SearchUiState() }
    }
}
