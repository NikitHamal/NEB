package com.neb.ians.ui.screens.interactive

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiService
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class InteractiveLessonViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(InteractiveLessonUiState())
    val uiState: StateFlow<InteractiveLessonUiState> = _uiState.asStateFlow()

    fun loadLesson(courseSlug: String, lessonSlug: String) {
        if (_uiState.value.lesson != null) return
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val response = apiService.getInteractiveLessonDetail(courseSlug, lessonSlug)
                _uiState.update { it.copy(lesson = response, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.message ?: "Failed to load lesson") }
            }
        }
    }
}