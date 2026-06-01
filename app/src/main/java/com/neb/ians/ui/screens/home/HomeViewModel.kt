package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiHomeResponse
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HomeUiState(
    val userName: String = "Student",
    val recentResources: List<ApiResource> = emptyList(),
    val popularResources: List<ApiResource> = emptyList(),
    val recentPosts: List<ApiPost> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
) {
    companion object {
        val SUBJECTS = listOf(
            "Physics", "Chemistry", "Mathematics", "Biology",
            "English", "Nepali", "Computer Science", "Economics", "Accountancy"
        )
    }
}

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    private val _isLoading = MutableStateFlow(true)
    private val _error = MutableStateFlow<String?>(null)
    private val _recentResources = MutableStateFlow<List<ApiResource>>(emptyList())
    private val _popularResources = MutableStateFlow<List<ApiResource>>(emptyList())
    private val _recentPosts = MutableStateFlow<List<ApiPost>>(emptyList())

    init {
        loadData()
    }

    private fun loadData() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                val token = authRepository.getBearerToken()
                val homeData = apiService.getHomeData(token)
                _recentResources.value = homeData.recentResources
                _popularResources.value = homeData.popularResources
                _recentPosts.value = homeData.recentPosts
            } catch (e: Exception) {
                _error.value = e.message ?: "Failed to load data"
            }
            _isLoading.value = false
        }
    }

    fun refresh() {
        loadData()
    }

    val uiState: StateFlow<HomeUiState> = combine(
        settingsRepository.userName,
        _recentResources,
        _popularResources,
        _recentPosts,
        _isLoading,
        _error
    ) { userName, recent, popular, posts, isLoading, error ->
        HomeUiState(
            userName = userName,
            recentResources = recent,
            popularResources = popular,
            recentPosts = posts,
            isLoading = isLoading,
            error = error
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}