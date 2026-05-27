package com.neb.ians.ui.screens.forum

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CreatePostUiState(
    val title: String = "",
    val content: String = "",
    val selectedCategory: String = "General",
    val isSubmitting: Boolean = false,
    val categories: List<String> = listOf(
        "General", "Physics", "Chemistry", "Mathematics",
        "Biology", "English", "Computer Science", "Exam Tips"
    )
)

@HiltViewModel
class CreatePostViewModel @Inject constructor(
    private val forumRepository: ForumRepository,
    private val settingsRepository: SettingsRepository
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
            _uiState.update { it.copy(isSubmitting = true) }
            val userName = settingsRepository.userName.first()
            forumRepository.createPost(
                title = state.title,
                content = state.content,
                authorName = userName,
                category = state.selectedCategory
            )
            _uiState.update { it.copy(isSubmitting = false) }
            onSuccess()
        }
    }
}
