package com.neb.ians.ui.screens.library

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiSyllabusCategory
import com.neb.ians.data.api.ApiSyllabusSubject
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.repository.AppCache
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** A sort option for the library (web parity with the /library/ sort dropdown). */
data class LibrarySortOption(val key: String, val label: String)

data class LibraryUiState(
    val resources: List<ApiResource> = emptyList(),
    val totalCount: Int = 0,
    val currentPage: Int = 1,
    val totalPages: Int = 1,
    val hasMore: Boolean = false,
    val sort: String = "relevant",
    val selectedSubject: String? = null,
    val selectedGradeLevel: String? = null,
    val selectedType: String? = null,
    val syllabusCategories: List<ApiSyllabusCategory> = emptyList(),
    val isSyllabusLoading: Boolean = false,
    val syllabusError: String? = null,
    val isLoading: Boolean = true,
    val isLoadingMore: Boolean = false,
    val error: String? = null
) {
    companion object {
        val SUBJECTS = listOf(
            "Accountancy", "Biology", "Chemistry", "Computer Science", "Economics",
            "English", "Exam Tips", "Mathematics", "Microbiology", "Nepali",
            "Physics", "Physics - Technical Stream", "Science", "Social Studies",
            "Software Engineering", "Software Engineering and Project Management",
            "Visual Programming", "Zoology", "सामाजिक अध्ययन"
        )
        val GRADE_LEVELS = listOf(
            "Bachelor", "Class 10 / SEE", "Class 11", "Class 12", "Class 8",
            "Entrance Prep", "Other"
        )
        val TYPES = listOf(
            "Guide", "Image", "Notes", "Past Paper", "Past Papers", "PDF", "Solution", "Textbook"
        )

        /** Exactly mirrors the web sort dropdown options. */
        val SORT_OPTIONS = listOf(
            LibrarySortOption("relevant", "Most Relevant"),
            LibrarySortOption("trending", "Trending"),
            LibrarySortOption("newest", "Newest"),
            LibrarySortOption("liked", "Most Liked"),
            LibrarySortOption("oldest", "Oldest")
        )
    }
}

@HiltViewModel
class LibraryViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository,
    private val apiService: ApiService,
    private val appCache: AppCache,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        LibraryUiState(
            resources = appCache.libraryResources,
            totalCount = appCache.libraryTotalCount,
            totalPages = appCache.libraryTotalPages,
            hasMore = appCache.libraryHasMore,
            isLoading = appCache.libraryResources.isEmpty()
        )
    )

    val uiState: StateFlow<LibraryUiState> = _uiState.asStateFlow()

    init {
        val initialSubject = savedStateHandle.get<String>("subject")
        if (!initialSubject.isNullOrBlank()) {
            _uiState.update { it.copy(selectedSubject = initialSubject) }
        }
        loadResources()
        loadSyllabusCategories()
    }

    fun loadSyllabusCategories() {
        viewModelScope.launch {
            _uiState.update { it.copy(isSyllabusLoading = true, syllabusError = null) }
            try {
                val response = apiService.getSyllabusCategories()
                val categories = response.categories.ifEmpty { fallbackSyllabusCategories() }
                _uiState.update {
                    it.copy(
                        syllabusCategories = categories.sortedBy { category -> category.order },
                        isSyllabusLoading = false
                    )
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(
                        syllabusCategories = fallbackSyllabusCategories(),
                        isSyllabusLoading = false,
                        syllabusError = ApiErrorMapper.mapException(e)
                    )
                }
            }
        }
    }

    private fun fallbackSyllabusCategories(): List<ApiSyllabusCategory> {
        return LibraryUiState.GRADE_LEVELS.mapIndexed { index, grade ->
            ApiSyllabusCategory(
                grade = grade.replace("Grade", "Class"),
                order = index,
                subjects = LibraryUiState.SUBJECTS.map { subject -> ApiSyllabusSubject(name = subject) }
            )
        }
    }

    private fun loadResources() {
        viewModelScope.launch {
            val state = _uiState.value
            val isDefaultQuery = state.selectedSubject == null && state.selectedGradeLevel == null && state.selectedType == null && state.sort == "relevant"
            _uiState.update { it.copy(isLoading = if (isDefaultQuery) it.resources.isEmpty() else true, error = null) }
            
            resourceRepository.getResources(
                subject = state.selectedSubject,
                grade = state.selectedGradeLevel,
                type = state.selectedType,
                sort = state.sort,
                page = 1
            ).onSuccess { result ->
                _uiState.update {
                    it.copy(
                        resources = result.resources,
                        totalCount = result.totalCount,
                        currentPage = 1,
                        totalPages = result.totalPages,
                        hasMore = result.resources.size < result.totalCount,
                        isLoading = false
                    )
                }
                if (isDefaultQuery) {
                    appCache.libraryResources = result.resources
                    appCache.libraryTotalCount = result.totalCount
                    appCache.libraryTotalPages = result.totalPages
                    appCache.libraryHasMore = result.resources.size < result.totalCount
                }
            }.onFailure { e ->
                if (_uiState.value.resources.isEmpty()) {
                    _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
                } else {
                    _uiState.update { it.copy(isLoading = false) }
                }
            }
        }
    }

    /** Infinite scroll: appends the next page when the grid reaches the end. */
    fun loadNextPage() {
        val state = _uiState.value
        if (state.isLoading || state.isLoadingMore || !state.hasMore) return
        viewModelScope.launch {
            _uiState.update { it.copy(isLoadingMore = true) }
            val nextPage = state.currentPage + 1
            resourceRepository.getResources(
                subject = state.selectedSubject,
                grade = state.selectedGradeLevel,
                type = state.selectedType,
                sort = state.sort,
                page = nextPage,
                append = true
            ).onSuccess { result ->
                _uiState.update { current ->
                    val existingIds = current.resources.mapTo(HashSet()) { it.id }
                    val merged = current.resources + result.resources.filterNot { it.id in existingIds }
                    current.copy(
                        resources = merged,
                        totalCount = result.totalCount,
                        currentPage = nextPage,
                        totalPages = result.totalPages,
                        hasMore = result.resources.isNotEmpty() && merged.size < result.totalCount,
                        isLoadingMore = false
                    )
                }
            }.onFailure {
                _uiState.update { it.copy(isLoadingMore = false) }
            }
        }
    }

    fun refresh() {
        loadResources()
    }

    /** Changes the sort key and reloads from page 1 (filters preserved). */
    fun selectSort(sortKey: String) {
        if (_uiState.value.sort == sortKey) return
        _uiState.update { it.copy(sort = sortKey, currentPage = 1) }
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
}
