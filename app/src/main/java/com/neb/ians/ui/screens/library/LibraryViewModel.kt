package com.neb.ians.ui.screens.library

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class LibraryUiState(
    val resources: List<ResourceEntity> = emptyList(),
    val selectedSubject: String? = null,
    val selectedGradeLevel: String? = null,
    val selectedType: String? = null,
    val isLoading: Boolean = false,
    val subjects: List<String> = listOf(
        "Physics", "Chemistry", "Mathematics", "Biology",
        "English", "Nepali", "Computer Science", "Economics", "Accountancy"
    ),
    val gradeLevels: List<String> = listOf("Grade 11", "Grade 12"),
    val types: List<String> = listOf("Textbook", "Notes", "Past Papers", "Guide", "Solution")
)

@HiltViewModel
class LibraryViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository
) : ViewModel() {

    private val _selectedSubject = MutableStateFlow<String?>(null)
    private val _selectedGradeLevel = MutableStateFlow<String?>(null)
    private val _selectedType = MutableStateFlow<String?>(null)

    val uiState: StateFlow<LibraryUiState> = combine(
        _selectedSubject,
        _selectedGradeLevel,
        _selectedType,
        resourceRepository.getAllResources()
    ) { subject, grade, type, allResources ->
        val filtered = allResources.filter { resource ->
            (subject == null || resource.subject == subject) &&
            (grade == null || resource.gradeLevel == grade) &&
            (type == null || resource.type == type)
        }
        LibraryUiState(
            resources = filtered,
            selectedSubject = subject,
            selectedGradeLevel = grade,
            selectedType = type
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), LibraryUiState())

    fun selectSubject(subject: String?) {
        _selectedSubject.value = if (_selectedSubject.value == subject) null else subject
    }

    fun selectGradeLevel(gradeLevel: String?) {
        _selectedGradeLevel.value = if (_selectedGradeLevel.value == gradeLevel) null else gradeLevel
    }

    fun selectType(type: String?) {
        _selectedType.value = if (_selectedType.value == type) null else type
    }

    fun clearFilters() {
        _selectedSubject.value = null
        _selectedGradeLevel.value = null
        _selectedType.value = null
    }
}
