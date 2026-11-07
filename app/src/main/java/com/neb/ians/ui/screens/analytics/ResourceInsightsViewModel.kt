package com.neb.ians.ui.screens.analytics

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiResourceInsights
import com.neb.ians.data.repository.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ResourceInsightsUiState(
    val days: Int = 30,
    val data: ApiResourceInsights? = null,
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val error: String? = null
)

/**
 * Library insights for the uploader. With a `resourceId` argument it is one resource,
 * without one it is everything the member uploaded plus their posts. The server refuses
 * anyone who is not the uploader with a 403.
 */
@HiltViewModel
class ResourceInsightsViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository
) : ViewModel() {

    private val resourceId: String? = savedStateHandle.get<String>("resourceId")?.takeIf { it.isNotBlank() }
    private val _uiState = MutableStateFlow(ResourceInsightsUiState())
    val uiState: StateFlow<ResourceInsightsUiState> = _uiState.asStateFlow()

    val isSingle: Boolean get() = resourceId != null

    private val cache = mutableMapOf<Int, ApiResourceInsights>()
    private var job: Job? = null

    init {
        load()
    }

    fun selectRange(days: Int) {
        if (days == _uiState.value.days && _uiState.value.data != null) return
        _uiState.update { it.copy(days = days, data = cache[days] ?: it.data) }
        load()
    }

    fun load() {
        job?.cancel()
        val days = _uiState.value.days
        job = viewModelScope.launch {
            val shown = _uiState.value.data != null
            _uiState.update { it.copy(isLoading = !shown, isRefreshing = shown, error = null) }
            resourceRepository.getResourceInsights(resourceId, days)
                .onSuccess { data ->
                    cache[days] = data
                    _uiState.update {
                        if (it.days != days) it else it.copy(data = data, isLoading = false, isRefreshing = false)
                    }
                }
                .onFailure { e ->
                    if (e is kotlinx.coroutines.CancellationException) throw e
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            isRefreshing = false,
                            error = if (it.data == null) ApiErrorMapper.mapException(e) else null
                        )
                    }
                }
        }
    }
}
