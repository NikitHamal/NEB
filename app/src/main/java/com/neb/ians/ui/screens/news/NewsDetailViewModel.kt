package com.neb.ians.ui.screens.news

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.news.NewsDetail
import com.neb.ians.data.repository.NewsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.net.URLDecoder
import javax.inject.Inject

data class NewsDetailUiState(
    val slug: String = "",
    val detail: NewsDetail? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class NewsDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val newsRepository: NewsRepository
) : ViewModel() {
    private val slug: String = savedStateHandle.get<String>("slug")?.let { URLDecoder.decode(it, "UTF-8") }.orEmpty()
    private val _uiState = MutableStateFlow(NewsDetailUiState(slug = slug))
    val uiState: StateFlow<NewsDetailUiState> = _uiState.asStateFlow()

    init { load() }

    fun retry() = load(forceRefresh = true)

    private fun load(forceRefresh: Boolean = false) {
        if (slug.isBlank()) {
            _uiState.update { it.copy(isLoading = false, error = "Blog post not found") }
            return
        }
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            newsRepository.getAnnouncementDetail(slug, forceRefresh)
                .onSuccess { detail -> _uiState.update { it.copy(detail = detail, isLoading = false, error = null) } }
                .onFailure { error -> _uiState.update { it.copy(isLoading = false, error = error.message ?: "Couldn't load blog post") } }
        }
    }
}
