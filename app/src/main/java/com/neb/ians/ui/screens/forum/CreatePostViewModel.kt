package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CreatePostUiState(
    val title: String = "",
    val content: String = "",
    val selectedCategory: String = "General",
    val isSubmitting: Boolean = false,
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
class CreatePostViewModel @Inject constructor(
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CreatePostUiState())
    val uiState: StateFlow<CreatePostUiState> = _uiState.asStateFlow()

    fun onTitleChange(title: String) {
        _uiState.update { it.copy(title = title) }
    }

    fun onContentChange(content: String) {
        _uiState.update { it.copy(content = content) }
    }

    fun onCategoryChange(category: String) {
        _uiState.update { it.copy(selectedCategory = category) }
    }

    fun submitPost(onSuccess: () -> Unit) {
        val state = _uiState.value
        if (state.title.isBlank() || state.content.isBlank()) return

        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, error = null) }
            forumRepository.createPost(
                title = state.title,
                content = state.content,
                category = state.selectedCategory
            ).onSuccess {
                _uiState.update { it.copy(isSubmitting = false) }
                onSuccess()
            }.onFailure { e ->
                _uiState.update { it.copy(isSubmitting = false, error = e.message ?: "Failed to post") }
            }
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }
}