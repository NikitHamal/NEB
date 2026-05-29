package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ForumUiState(
    val posts: List<ForumPostEntity> = emptyList(),
    val selectedCategory: String? = null,
    val searchQuery: String = "",
    val isLoading: Boolean = true,
    val error: String? = null
) {
    companion object {
        val CATEGORIES = listOf(
            "General", "Physics", "Chemistry", "Mathematics",
            "Biology", "English", "Computer Science", "Exam Tips"
        )
    }
}

@HiltViewModel
class ForumViewModel @Inject constructor(
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val _isLoading = MutableStateFlow(true)
    private val _error = MutableStateFlow<String?>(null)

    init {
        syncData()
    }

    private fun syncData() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                forumRepository.syncPosts()
            } catch (e: Exception) {
                _error.value = e.message ?: "Failed to load forum posts"
            }
            _isLoading.value = false
        }
    }

    fun refresh() {
        syncData()
    }

    private val _selectedCategory = MutableStateFlow<String?>(null)
    private val _searchQuery = MutableStateFlow("")

    @OptIn(kotlinx.coroutines.ExperimentalCoroutinesApi::class)
    val uiState: StateFlow<ForumUiState> = combine(
        _selectedCategory,
        _searchQuery.debounce(300),
        forumRepository.getAllPosts().distinctUntilChanged(),
        _isLoading,
        _error
    ) { category, query, posts, isLoading, error ->
        val filtered = posts.filter { post ->
            (category == null || post.category == category) &&
            (query.isEmpty() || post.title.contains(query, ignoreCase = true) || post.content.contains(query, ignoreCase = true))
        }.sortedByDescending { it.createdAt }
        ForumUiState(
            posts = filtered,
            selectedCategory = category,
            searchQuery = query,
            isLoading = isLoading,
            error = error
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), ForumUiState())

    fun selectCategory(category: String?) {
        _selectedCategory.value = if (_selectedCategory.value == category) null else category
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
    }

    fun toggleThumbsUp(postId: String) {
        viewModelScope.launch {
            forumRepository.toggleThumbsUp(postId)
        }
    }
}