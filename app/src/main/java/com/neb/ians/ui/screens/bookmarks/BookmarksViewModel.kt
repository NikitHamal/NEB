package com.neb.ians.ui.screens.bookmarks

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiBookmark
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.BookmarkToggleRequest
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

// ---------------------------------------------------------------------------
// Everything a NEBian has kept, in one list.
//
// A bookmark on the wire is only a type and an id, so each one is resolved
// against its own endpoint before it can be shown as anything a person would
// recognise. Removing one is optimistic and reversible: the row leaves
// immediately and comes back untouched if the undo is taken.
// ---------------------------------------------------------------------------

enum class BookmarkKind(val key: String, val label: String) {
    All("all", "All"),
    Posts("post", "Posts"),
    Replies("reply", "Replies"),
    Resources("resource", "Resources")
}

data class BookmarkListItem(
    val bookmark: ApiBookmark,
    val title: String,
    val excerpt: String,
    val meta: String
)

data class BookmarksUiState(
    val items: List<BookmarkListItem> = emptyList(),
    val selectedType: String = BookmarkKind.All.key,
    val totalCount: Int = 0,
    val isLoading: Boolean = true,
    val error: String? = null,
    val undoTarget: BookmarkListItem? = null,
    val message: String? = null
) {
    val visibleItems: List<BookmarkListItem>
        get() = if (selectedType == BookmarkKind.All.key) {
            items
        } else {
            items.filter { it.bookmark.targetType == selectedType }
        }

    fun countOf(kind: BookmarkKind): Int = when (kind) {
        BookmarkKind.All -> items.size
        else -> items.count { it.bookmark.targetType == kind.key }
    }
}

@HiltViewModel
class BookmarksViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(BookmarksUiState())
    val uiState: StateFlow<BookmarksUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun selectType(type: String) {
        _uiState.update { it.copy(selectedType = type) }
    }

    fun consumeMessage() {
        _uiState.update { it.copy(message = null, undoTarget = null) }
    }

    fun load(): Job {
        return viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to view bookmarks") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val page = apiService.getBookmarks(token)
                val enriched = page.bookmarks.take(60).map { bookmark ->
                    async { enrichBookmark(token, bookmark) }
                }.awaitAll()
                _uiState.update {
                    it.copy(items = enriched, totalCount = page.totalCount, isLoading = false)
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load bookmarks")
                }
            }
        }
    }

    fun remove(item: BookmarkListItem) {
        val snapshot = _uiState.value
        _uiState.update {
            it.copy(
                items = it.items.filterNot { entry -> entry.bookmark.id == item.bookmark.id },
                totalCount = (it.totalCount - 1).coerceAtLeast(0),
                undoTarget = item,
                message = "Removed from bookmarks"
            )
        }
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                apiService.toggleBookmark(
                    token,
                    BookmarkToggleRequest(item.bookmark.targetType, item.bookmark.targetId)
                )
            } catch (_: Exception) {
                _uiState.update {
                    it.copy(
                        items = snapshot.items,
                        totalCount = snapshot.totalCount,
                        undoTarget = null,
                        message = "Couldn't remove that bookmark"
                    )
                }
            }
        }
    }

    fun undoRemove() {
        val item = _uiState.value.undoTarget ?: return
        _uiState.update {
            it.copy(
                items = (it.items + item).sortedByDescending { entry -> entry.bookmark.createdAt },
                totalCount = it.totalCount + 1,
                undoTarget = null,
                message = null
            )
        }
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            try {
                apiService.toggleBookmark(
                    token,
                    BookmarkToggleRequest(item.bookmark.targetType, item.bookmark.targetId)
                )
            } catch (_: Exception) {
                _uiState.update { it.copy(message = "Couldn't restore that bookmark") }
            }
        }
    }

    private suspend fun enrichBookmark(token: String, bookmark: ApiBookmark): BookmarkListItem {
        return try {
            when (bookmark.targetType) {
                "resource" -> {
                    val resource = apiService.getResource(token, bookmark.targetId)
                    BookmarkListItem(
                        bookmark = bookmark,
                        title = resource.title,
                        excerpt = resource.description,
                        meta = listOf(resource.subject, resource.gradeLevel, resource.type)
                            .filter { it.isNotBlank() }
                            .joinToString(" · ")
                    )
                }
                "post" -> {
                    val post = apiService.getPost(token, bookmark.targetId)
                    BookmarkListItem(
                        bookmark = bookmark,
                        title = post.title,
                        excerpt = post.content,
                        meta = "${post.authorName} · ${post.replyCount} replies"
                    )
                }
                else -> BookmarkListItem(
                    bookmark = bookmark,
                    title = "Saved reply",
                    excerpt = "Open this saved reply from the discussion it belongs to.",
                    meta = "Reply"
                )
            }
        } catch (_: Exception) {
            BookmarkListItem(
                bookmark = bookmark,
                title = bookmark.targetType.replaceFirstChar { it.uppercase() },
                excerpt = "",
                meta = "Saved"
            )
        }
    }
}
