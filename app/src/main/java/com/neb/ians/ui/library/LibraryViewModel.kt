package com.neb.ians.ui.library

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.ResourceRepository
import com.neb.ians.data.local.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class LibraryFilters(
    val query: String = "",
    val subject: Subject? = null,
    val grade: Grade? = null,
    val type: ResourceType? = null,
)

@HiltViewModel
class LibraryViewModel @Inject constructor(
    private val repo: ResourceRepository,
) : ViewModel() {

    val filters = MutableStateFlow(LibraryFilters())

    @OptIn(ExperimentalCoroutinesApi::class)
    val results: StateFlow<List<ResourceEntity>> = filters
        .flatMapLatest { f -> repo.search(f.query, f.subject, f.grade, f.type) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun setQuery(q: String) = filters.update { it.copy(query = q) }
    fun setSubject(s: Subject?) = filters.update { it.copy(subject = s) }
    fun setGrade(g: Grade?) = filters.update { it.copy(grade = g) }
    fun setType(t: ResourceType?) = filters.update { it.copy(type = t) }
    fun clear() { filters.value = LibraryFilters() }

    fun toggleFavorite(r: ResourceEntity) = viewModelScope.launch {
        repo.setFavorite(r.id, !r.isFavorite)
    }
}
