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
    val categories: List<String> = listOf(
        "General", "Physics", "Chemistry", "Mathematics",
        "Biology", "English", "Computer Science", "Exam Tips"
    )
)

@HiltViewModel
class ForumViewModel @Inject constructor(
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val _selectedCategory = MutableStateFlow<String?>(null)
    private val _searchQuery = MutableStateFlow("")

    val uiState: StateFlow<ForumUiState> = combine(
        _selectedCategory,
        _searchQuery,
        forumRepository.getAllPosts()
    ) { category, query, posts ->
        val filtered = posts.filter { post ->
            (category == null || post.category == category) &&
            (query.isEmpty() || post.title.contains(query, ignoreCase = true) || post.content.contains(query, ignoreCase = true))
        }.sortedByDescending { it.createdAt }
        ForumUiState(
            posts = filtered,
            selectedCategory = category,
            searchQuery = query
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
