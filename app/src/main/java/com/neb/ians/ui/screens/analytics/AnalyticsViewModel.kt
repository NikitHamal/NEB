package com.neb.ians.ui.screens.analytics

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiPrivateAnalyticsResponse
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

val AnalyticsRanges = listOf(7, 30, 90)

data class AnalyticsUiState(
    val days: Int = 30,
    val data: ApiPrivateAnalyticsResponse? = null,
    val username: String = "",
    /** True while nothing is on screen yet. */
    val isLoading: Boolean = true,
    /** True while a range switch or a pull is fetching behind data that is already shown. */
    val isRefreshing: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class AnalyticsViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(AnalyticsUiState())
    val uiState: StateFlow<AnalyticsUiState> = _uiState.asStateFlow()

    private val cache = mutableMapOf<Int, ApiPrivateAnalyticsResponse>()
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
            try {
                val token = authRepository.getBearerToken()
                if (token.isNullOrBlank()) {
                    _uiState.update { it.copy(isLoading = false, isRefreshing = false, error = "Sign in to view analytics") }
                    return@launch
                }
                val data = apiService.getPrivateAnalytics(token, days)
                cache[days] = data
                val fallback = authRepository.userProfileFlow.first()?.username.orEmpty()
                _uiState.update {
                    if (it.days != days) it else it.copy(
                        data = data,
                        username = data.username.ifBlank { fallback },
                        isLoading = false,
                        isRefreshing = false
                    )
                }
            } catch (e: kotlinx.coroutines.CancellationException) {
                throw e
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isLoading = false, isRefreshing = false, error = if (it.data == null) ApiErrorMapper.mapException(e) else null)
                }
            }
        }
    }
}
