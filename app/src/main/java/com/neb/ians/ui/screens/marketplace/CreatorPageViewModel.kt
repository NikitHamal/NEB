package com.neb.ians.ui.screens.marketplace

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.MarketplaceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CreatorPageUiState(
    val slug: String = "",
    val isLoading: Boolean = true,
    val error: String? = null,
    val page: ApiCreatorPage? = null
)

@HiltViewModel
class CreatorPageViewModel @Inject constructor(
    private val repository: MarketplaceRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val slug: String = savedStateHandle.get<String>("slug").orEmpty()

    private val _uiState = MutableStateFlow(CreatorPageUiState(slug = slug))
    val uiState: StateFlow<CreatorPageUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        if (slug.isBlank()) {
            _uiState.update { it.copy(isLoading = false, error = "This page is not available") }
            return
        }
        _uiState.update { it.copy(isLoading = it.page == null, error = null) }
        viewModelScope.launch {
            repository.creatorPage(slug).fold(
                onSuccess = { page ->
                    _uiState.update { it.copy(isLoading = false, error = null, page = page) }
                },
                onFailure = { failure ->
                    _uiState.update {
                        it.copy(isLoading = false, error = ApiErrorMapper.mapException(failure))
                    }
                }
            )
        }
    }
}
