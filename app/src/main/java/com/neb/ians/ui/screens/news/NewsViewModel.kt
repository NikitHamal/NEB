package com.neb.ians.ui.screens.news

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.repository.NewsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class NewsUiState(
    val items: List<NewsAnnouncement> = emptyList(),
    val selectedCategory: String? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class NewsViewModel @Inject constructor(
    private val newsRepository: NewsRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(NewsUiState())
    val uiState: StateFlow<NewsUiState> = _uiState.asStateFlow()

    init {
        loadNews()
    }

    fun selectCategory(category: String?) {
        if (_uiState.value.selectedCategory == category) return
        _uiState.update { it.copy(selectedCategory = category, isLoading = true, error = null, items = emptyList()) }
        loadNews(forceRefresh = false)
    }

    fun retry() {
        loadNews(forceRefresh = true)
    }

    private fun loadNews(forceRefresh: Boolean = false) {
        val category = _uiState.value.selectedCategory
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            newsRepository.getAnnouncements(category, forceRefresh)
                .onSuccess { items ->
                    _uiState.update { it.copy(items = items, isLoading = false, error = null) }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message ?: "Couldn't load blog posts. Please try again."
                        )
                    }
                }
        }
    }
}
