package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HomeUiState(
    val userName: String = "Student",
    val userPhotoUrl: String? = null,
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
                val resourcesResult = apiService.getResources(token, sort = "newest", page = 1)
                val popularResult = apiService.getResources(token, sort = "relevant", page = 1)
                val postsResult = apiService.getPosts(token)
                _recentResources.value = resourcesResult.resources
                _popularResources.value = popularResult.resources
                _recentPosts.value = postsResult.posts
            } catch (e: Exception) {
                _error.value = ApiErrorMapper.mapException(e)
            }
            _isLoading.value = false
        }
    }

    fun refresh() {
        loadData()
    }

    val uiState: StateFlow<HomeUiState> = combine(
        combine(
            authRepository.userProfileFlow.map { it?.displayName?.takeIf { name -> name.isNotBlank() } ?: it?.username ?: "Student" },
            authRepository.currentUserPhotoUrlFlow
        ) { name, photo -> Pair(name, photo) },
        _recentResources,
        _popularResources,
        _recentPosts,
        combine(_isLoading, _error) { isLoading, error -> Pair(isLoading, error) }
    ) { user, recentResources, popularResources, recentPosts, loadingError ->
        HomeUiState(
            userName = user.first,
            userPhotoUrl = user.second,
            recentResources = recentResources,
            popularResources = popularResources,
            recentPosts = recentPosts,
            isLoading = loadingError.first,
            error = loadingError.second
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}