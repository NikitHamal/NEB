package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
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
            val token = authRepository.getBearerToken()
            val resourceError = runCatching {
                val resourcesResult = apiService.getResources(token, sort = "newest", page = 1)
                _recentResources.value = resourcesResult.resources
            }.exceptionOrNull()

            runCatching {
                val popularResult = apiService.getResources(token, sort = "relevant", page = 1)
                _popularResources.value = popularResult.resources
            }.onFailure {
                _popularResources.value = _recentResources.value
            }

            runCatching {
                val postsResult = apiService.getPosts(token)
                _recentPosts.value = postsResult.posts
            }.onFailure {
                _recentPosts.value = emptyList()
            }

            if (resourceError != null && _recentResources.value.isEmpty()) {
                _error.value = resourceError.message ?: "Failed to load resources"
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
        combine(_isLoading, _error) { isLoading, error -> Pair(isLoading, error) }
    ) { userName, recentResources, popularResources, recentPosts, loadingError ->
        HomeUiState(
            userName = userName,
            recentResources = recentResources,
            popularResources = popularResources,
            recentPosts = recentPosts,
            isLoading = loadingError.first,
            error = loadingError.second
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}
