package com.neb.ians.ui.resources

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.db.ResourceEntity
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.data.repo.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResourcesFilter(
    val query: String = "",
    val subject: Subject? = null,
    val grade: Grade? = null,
    val type: ResourceType? = null,
)

@OptIn(ExperimentalCoroutinesApi::class, FlowPreview::class)
@HiltViewModel
class ResourcesViewModel @Inject constructor(
    private val repo: ResourceRepository,
) : ViewModel() {

    private val _filter = MutableStateFlow(ResourcesFilter())
    val filter: StateFlow<ResourcesFilter> = _filter.asStateFlow()

    val results: StateFlow<List<ResourceEntity>> =
        _filter
            .debounce(120)
            .flatMapLatest { f ->
                repo.search(f.query.trim(), f.subject?.name, f.grade?.name, f.type?.name)
            }
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun setQuery(q: String) { _filter.value = _filter.value.copy(query = q) }
    fun setSubject(s: Subject?) { _filter.value = _filter.value.copy(subject = s) }
    fun setGrade(g: Grade?) { _filter.value = _filter.value.copy(grade = g) }
    fun setType(t: ResourceType?) { _filter.value = _filter.value.copy(type = t) }

    fun toggleFavorite(id: String) {
        viewModelScope.launch { repo.toggleFavorite(id) }
    }
}
