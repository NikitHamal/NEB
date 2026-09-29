@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.MarketplaceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** The three shelves the marketplace tab offers, in the owner's own words. */
enum class MarketplaceKind(val key: String?, val label: String) {
    Everyone(null, "Everyone"),
    Tutors("tutor", "Tutors"),
    Institutes("institute", "Institutes"),
    Official("admin", "Official")
}

data class MarketplaceUiState(
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val isLoadingMore: Boolean = false,
    val error: String? = null,
    val creators: List<ApiCreatorPage> = emptyList(),
    val offerings: List<ApiCreatorCourse> = emptyList(),
    val kind: MarketplaceKind = MarketplaceKind.Everyone,
    val query: String = "",
    val total: Int = 0,
    val hasMore: Boolean = false,
    val page: Int = 1,
    val myPage: ApiCreatorPage? = null,
    val canCreate: Boolean = false,
    val commissionPercent: Double = 2.5
) {
    val isEmpty: Boolean get() = !isLoading && creators.isEmpty() && error == null
}

@HiltViewModel
class MarketplaceViewModel @Inject constructor(
    private val repository: MarketplaceRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MarketplaceUiState())
    val uiState: StateFlow<MarketplaceUiState> = _uiState.asStateFlow()

    private var loadJob: Job? = null

    init {
        load(reset = true)
    }

    fun retry() = load(reset = true)

    fun refresh() = load(reset = true, refreshing = true)

    fun selectKind(kind: MarketplaceKind) {
        if (_uiState.value.kind == kind) return
        _uiState.update { it.copy(kind = kind) }
        load(reset = true)
    }

    fun updateQuery(query: String) = _uiState.update { it.copy(query = query) }

    fun submitQuery() = load(reset = true)

    fun loadNextPage() {
        val state = _uiState.value
        if (state.isLoading || state.isRefreshing || state.isLoadingMore || !state.hasMore) return
        load(reset = false)
    }

    private fun load(reset: Boolean, refreshing: Boolean = false) {
        loadJob?.cancel()
        val state = _uiState.value
        val nextPage = if (reset) 1 else state.page + 1

        _uiState.update {
            it.copy(
                isLoading = reset && !refreshing,
                isRefreshing = refreshing,
                isLoadingMore = !reset,
                error = if (reset) null else it.error
            )
        }

        loadJob = viewModelScope.launch {
            val result = repository.creators(
                kind = state.kind.key,
                query = state.query,
                page = nextPage,
                pageSize = PAGE_SIZE
            )
            result.fold(
                onSuccess = { response ->
                    _uiState.update { current ->
                        current.copy(
                            isLoading = false,
                            isRefreshing = false,
                            isLoadingMore = false,
                            error = null,
                            creators = if (reset) response.creators else current.creators + response.creators,
                            total = response.total,
                            hasMore = response.hasMore,
                            page = response.page,
                            canCreate = response.youAreEligible,
                            myPage = if (response.youAreEligible) current.myPage else null
                        )
                    }
                    if (reset) loadStudioContext()
                    loadOfferings()
                },
                onFailure = { failure ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            isRefreshing = false,
                            isLoadingMore = false,
                            error = ApiErrorMapper.mapException(failure)
                        )
                    }
                }
            )
        }
    }

    /** The owner's own page, so the tab can offer the studio instead of guessing. */
    private fun loadStudioContext() {
        viewModelScope.launch {
            repository.myPage().onSuccess { response ->
                _uiState.update {
                    it.copy(
                        canCreate = response.eligible,
                        myPage = response.page ?: it.myPage
                    )
                }
            }
        }
    }

    /** Two lines of course cards are enough above the creator list. */
    private fun loadOfferings() {
        val state = _uiState.value
        viewModelScope.launch {
            repository
                .recentCourses(kind = state.kind.key, query = state.query, limit = 8)
                .onSuccess { response ->
                    _uiState.update { it.copy(offerings = response.courses) }
                }
        }
    }

    private companion object {
        const val PAGE_SIZE = 12
    }
}
