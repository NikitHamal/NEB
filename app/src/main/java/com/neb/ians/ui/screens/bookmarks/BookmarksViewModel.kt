package com.neb.ians.ui.screens.bookmarks

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiBookmark
import com.neb.ians.data.repository.ContentBookmarkRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

enum class BookmarkFilter(val label: String, val targetType: String?) {
    ALL("All", null),
    RESOURCES("Resources", "resource"),
    POSTS("Posts", "post")
}

data class BookmarksUiState(
    val bookmarks: List<ApiBookmark> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null,
    val filter: BookmarkFilter = BookmarkFilter.ALL
)

@HiltViewModel
class BookmarksViewModel @Inject constructor(
    private val repository: ContentBookmarkRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(BookmarksUiState())
    val uiState: StateFlow<BookmarksUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun setFilter(filter: BookmarkFilter) {
        if (filter == _uiState.value.filter) return
        _uiState.update { it.copy(filter = filter) }
        load()
    }

    fun load() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            repository.getBookmarks(_uiState.value.filter.targetType)
                .onSuccess { list ->
                    _uiState.update { it.copy(bookmarks = list, isLoading = false) }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = e.message) }
                }
        }
    }

    fun removeBookmark(bookmark: ApiBookmark) {
        // Optimistic removal.
        val previous = _uiState.value.bookmarks
        _uiState.update { it.copy(bookmarks = it.bookmarks.filterNot { b -> b.id == bookmark.id }) }
        viewModelScope.launch {
            repository.toggle(bookmark.targetType, bookmark.targetId)
                .onFailure {
                    _uiState.update { it.copy(bookmarks = previous) }
                }
        }
    }
}
