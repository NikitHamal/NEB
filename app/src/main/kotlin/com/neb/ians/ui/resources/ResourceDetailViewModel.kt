package com.neb.ians.ui.resources

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.db.ResourceEntity
import com.neb.ians.data.repo.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResourceDetailUi(
    val resource: ResourceEntity? = null,
    val downloading: Boolean = false,
    val progress: Float = 0f,
    val error: String? = null,
)

@HiltViewModel
class ResourceDetailViewModel @Inject constructor(
    private val repo: ResourceRepository,
) : ViewModel() {

    private val _state = MutableStateFlow(ResourceDetailUi())
    val uiState: StateFlow<ResourceDetailUi> = _state.asStateFlow()

    private var loaded = false

    fun load(id: String) {
        if (loaded) return
        loaded = true
        viewModelScope.launch {
            repo.observeById(id).collect { r ->
                _state.value = _state.value.copy(resource = r)
            }
        }
    }

    fun toggleFavorite() {
        val r = _state.value.resource ?: return
        viewModelScope.launch { repo.toggleFavorite(r.id) }
    }

    fun download() {
        val r = _state.value.resource ?: return
        _state.value = _state.value.copy(downloading = true, progress = 0f, error = null)
        viewModelScope.launch {
            repo.downloadToCache(r).collect { p ->
                if (p < 0f) {
                    _state.value = _state.value.copy(downloading = false, error = "Download failed. Check your connection.")
                } else {
                    _state.value = _state.value.copy(progress = p, downloading = p < 1f)
                }
            }
        }
    }
}
