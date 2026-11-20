package com.neb.ians.ui.screens.library

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiInteractiveCategory
import com.neb.ians.data.api.ApiInteractiveCourseSummary
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class InteractiveUiState(
    val categories: List<ApiInteractiveCategory> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class InteractiveViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        InteractiveUiState(
            categories = cachedCategories,
            isLoading = cachedCategories.isEmpty()
        )
    )
    val uiState: StateFlow<InteractiveUiState> = _uiState.asStateFlow()
    private var loadRequested = false

    fun ensureLoaded() {
        if (loadRequested || _uiState.value.categories.isNotEmpty()) return
        loadRequested = true
        loadCategories()
    }

    fun loadCategories() {
        loadRequested = true
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = it.categories.isEmpty(), error = null) }
            try {
                val response = apiService.getInteractiveCategories()
                cachedCategories = response.categories
                _uiState.update { it.copy(categories = response.categories, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    companion object {
        @Volatile private var cachedCategories: List<ApiInteractiveCategory> = emptyList()
    }
}