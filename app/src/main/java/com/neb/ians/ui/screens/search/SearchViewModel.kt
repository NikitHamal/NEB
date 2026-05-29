package com.neb.ians.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SearchUiState(
    val query: String = "",
    val results: List<ResourceEntity> = emptyList(),
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

@OptIn(ExperimentalCoroutinesApi::class, FlowPreview::class)
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository
) : ViewModel() {

    private val _query = MutableStateFlow("")
    private val _uiState = MutableStateFlow(SearchUiState())

    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    private var searchJob: kotlinx.coroutines.Job? = null

    init {
        viewModelScope.launch {
            _query
                .debounce(300)
                .distinctUntilChanged()
                .collect { query ->
                    if (query.length >= 2) {
                        _uiState.update { it.copy(isSearching = true, error = null) }
                        try {
                            resourceRepository.searchResources(query).first { results ->
                                _uiState.update { it.copy(results = results, isSearching = false) }
                                true
                            }
                        } catch (e: Exception) {
                            _uiState.update { it.copy(isSearching = false, error = e.message ?: "Search failed") }
                        }
                    } else {
                        _uiState.update { it.copy(results = emptyList(), isSearching = false, error = null) }
                    }
                }
        }
    }

    fun onQueryChange(query: String) {
        _query.value = query
        _uiState.update { it.copy(query = query) }
    }

    fun clearSearch() {
        _query.value = ""
        _uiState.value = SearchUiState()
    }
}