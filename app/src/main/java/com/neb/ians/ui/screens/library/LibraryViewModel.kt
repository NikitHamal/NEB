package com.neb.ians.ui.screens.library

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.model.ContentItem
import com.neb.ians.data.repository.ContentRepository
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@OptIn(FlowPreview::class)
class LibraryViewModel(private val repository: ContentRepository) : ViewModel() {
    private val _query = MutableStateFlow("")
    val query: StateFlow<String> = _query

    private val _subjectFilter = MutableStateFlow<String?>(null)
    val subjectFilter: StateFlow<String?> = _subjectFilter

    private val _gradeFilter = MutableStateFlow<String?>(null)
    val gradeFilter: StateFlow<String?> = _gradeFilter

    private val _typeFilter = MutableStateFlow<String?>(null)
    val typeFilter: StateFlow<String?> = _typeFilter

    val items = combine(
        _query.debounce(200),
        _subjectFilter,
        _gradeFilter,
        _typeFilter,
        repository.getAll()
    ) { q, sub, gr, ty, all ->
        all.filter { item ->
            val matchesQuery = q.isBlank() || item.title.contains(q, true) || item.description.contains(q, true)
            val matchesSubject = sub.isNullOrBlank() || item.subject.equals(sub, true)
            val matchesGrade = gr.isNullOrBlank() || item.grade.equals(gr, true)
            val matchesType = ty.isNullOrBlank() || item.type.equals(ty, true)
            matchesQuery && matchesSubject && matchesGrade && matchesType
        }
    }.stateIn(viewModelScope, kotlinx.coroutines.flow.SharingStarted.WhileSubscribed(5000), emptyList())

    fun setQuery(value: String) { _query.value = value }
    fun setSubject(value: String?) { _subjectFilter.value = value }
    fun setGrade(value: String?) { _gradeFilter.value = value }
    fun setType(value: String?) { _typeFilter.value = value }
    fun clearFilters() {
        _subjectFilter.value = null
        _gradeFilter.value = null
        _typeFilter.value = null
        _query.value = ""
    }
}
