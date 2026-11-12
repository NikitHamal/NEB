package com.neb.ians.ui.screens.analytics

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiPostInsights
import com.neb.ians.data.repository.ForumRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PostInsightsUiState(
    val days: Int = 30,
    val data: ApiPostInsights? = null,
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val error: String? = null
)

/** One post's insights, author only. The server refuses anyone else with a 403. */
@HiltViewModel
class PostInsightsViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val forumRepository: ForumRepository
) : ViewModel() {

    private val postId: String = savedStateHandle.get<String>("postId") ?: ""
    private val _uiState = MutableStateFlow(PostInsightsUiState())
    val uiState: StateFlow<PostInsightsUiState> = _uiState.asStateFlow()

    private val cache = mutableMapOf<Int, ApiPostInsights>()
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
            forumRepository.getPostInsights(postId, days)
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
