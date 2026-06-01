package com.neb.ians.ui.screens.library

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class LibraryUiState(
    val resources: List<ApiResource> = emptyList(),
    val totalCount: Int = 0,
    val currentPage: Int = 1,
    val totalPages: Int = 1,
    val selectedSubject: String? = null,
    val selectedGradeLevel: String? = null,
    val selectedType: String? = null,
    val isLoading: Boolean = true,
    val error: String? = null
) {
    companion object {
        val SUBJECTS = listOf(
            "Physics", "Chemistry", "Mathematics", "Biology",
            "English", "Nepali", "Computer Science", "Economics", "Accountancy"
        )
        val GRADE_LEVELS = listOf("Grade 11", "Grade 12")
        val TYPES = listOf("Textbook", "Notes", "Past Papers", "Guide", "Solution")
    }
}

@HiltViewModel
class LibraryViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(LibraryUiState())

    val uiState: StateFlow<LibraryUiState> = _uiState.asStateFlow()

    init {
        val initialSubject = savedStateHandle.get<String>("subject")
        if (!initialSubject.isNullOrBlank()) {
            _uiState.update { it.copy(selectedSubject = initialSubject) }
        }
        loadResources()
    }

    private fun loadResources() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val state = _uiState.value
            resourceRepository.getResources(
                subject = state.selectedSubject,
                grade = state.selectedGradeLevel,
                type = state.selectedType,
                page = state.currentPage
            ).onSuccess { result ->
                _uiState.update {
                    it.copy(
                        resources = result.resources,
                        totalCount = result.totalCount,
                        currentPage = result.page,
                        totalPages = result.totalPages,
                        isLoading = false
                    )
                }
            }.onFailure { e ->
                _uiState.update { it.copy(isLoading = false, error = e.message ?: "Failed to load resources") }
            }
        }
    }

    fun refresh() {
        loadResources()
    }

    fun selectSubject(subject: String?) {
        val newSubject = if (_uiState.value.selectedSubject == subject) null else subject
        _uiState.update { it.copy(selectedSubject = newSubject, currentPage = 1) }
        loadResources()
    }

    fun selectGradeLevel(gradeLevel: String?) {
        val newGrade = if (_uiState.value.selectedGradeLevel == gradeLevel) null else gradeLevel
        _uiState.update { it.copy(selectedGradeLevel = newGrade, currentPage = 1) }
        loadResources()
    }

    fun selectType(type: String?) {
        val newType = if (_uiState.value.selectedType == type) null else type
        _uiState.update { it.copy(selectedType = newType, currentPage = 1) }
        loadResources()
    }

    fun clearFilters() {
        _uiState.update { it.copy(selectedSubject = null, selectedGradeLevel = null, selectedType = null, currentPage = 1) }
        loadResources()
    }

    fun loadPage(page: Int) {
        _uiState.update { it.copy(currentPage = page) }
        loadResources()
    }
}