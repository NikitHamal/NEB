package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import retrofit2.HttpException
import javax.inject.Inject

data class ForumUiState(
    val posts: List<ApiPost> = emptyList(),
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

    private val _uiState = MutableStateFlow(ForumUiState())
    val uiState: StateFlow<ForumUiState> = _uiState.asStateFlow()

    init {
        loadPosts()
    }

    private fun loadPosts() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val query = _uiState.value.searchQuery.trim().takeIf { it.length >= 2 }
            forumRepository.getPosts(
                category = _uiState.value.selectedCategory,
                search = query
            )
                .onSuccess { result ->
                    _uiState.update { it.copy(posts = result.posts, isLoading = false) }
                }
                .onFailure { e ->
                    val message = if (e is HttpException && e.code() == 401) {
                        "Sign in to view and join forum discussions."
                    } else {
                        e.message ?: "Failed to load posts"
                    }
                    _uiState.update { it.copy(isLoading = false, error = message) }
                }
        }
    }

    fun refresh() {
        loadPosts()
    }

    fun selectCategory(category: String?) {
        val newCategory = if (_uiState.value.selectedCategory == category) null else category
        _uiState.update { it.copy(selectedCategory = newCategory) }
        loadPosts()
    }

    fun onSearchQueryChange(query: String) {
        _uiState.update { it.copy(searchQuery = query) }
        if (query.isBlank() || query.trim().length >= 2) {
            loadPosts()
        }
    }

    fun toggleThumbsUp(postId: String) {
        viewModelScope.launch {
            forumRepository.toggleLikePost(postId)
                .onSuccess { response ->
                    val updatedPosts = _uiState.value.posts.map { post ->
                        if (post.id == postId) {
                            post.copy(thumbsUpCount = response.thumbsUpCount, isThumbedUp = response.isThumbedUp)
                        } else post
                    }
                    _uiState.update { it.copy(posts = updatedPosts) }
                }
        }
    }
}
