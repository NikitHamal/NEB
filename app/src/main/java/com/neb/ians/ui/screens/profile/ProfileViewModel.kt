package com.neb.ians.ui.screens.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserStats
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.data.repository.AuthRepository

data class ProfileUiState(
    val profile: UserProfileResponse? = null,
    val stats: ApiUserStats? = null,
    val isLoading: Boolean = false,
    val error: String? = null,
    val isFollowing: Boolean = false,
    val isSelf: Boolean = false,
    val followerCount: Int = 0
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    fun loadProfile(username: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            try {
                val token = authRepository.getBearerToken()
                val profile = apiService.getProfile(token, username)
                val stats = try {
                    apiService.getProfileStats(token, username)
                } catch (_: Exception) {
                    null
                }
                _uiState.value = _uiState.value.copy(
                    profile = profile,
                    stats = stats,
                    isLoading = false,
                    isFollowing = stats?.isFollowing ?: profile.isFollowing ?: false,
                    isSelf = stats?.isSelf ?: profile.isSelf ?: false,
                    followerCount = stats?.followerCount ?: profile.followerCount
                )
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isLoading = false, error = e.localizedMessage)
            }
        }
    }

    fun toggleFollow() {
        val profile = _uiState.value.profile ?: return
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                val response = apiService.toggleFollow(token, profile.id)
                _uiState.value = _uiState.value.copy(
                    isFollowing = response.isFollowing,
                    followerCount = response.followerCount ?: (_uiState.value.followerCount + (if (response.isFollowing) 1 else -1))
                )
            } catch (_: Exception) { }
        }
    }
}