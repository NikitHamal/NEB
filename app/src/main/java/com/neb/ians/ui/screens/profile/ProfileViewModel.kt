package com.neb.ians.ui.screens.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiUserPhoto
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject

private const val POSTS_PAGE_SIZE = 10

data class ProfileUiState(
    val profile: UserProfileResponse? = null,
    val isLoading: Boolean = false,
    val error: String? = null,
    val isFollowing: Boolean = false,
    val followerCount: Int = 0,
    // Tabs: 0 = Posts, 1 = About
    val selectedTab: Int = 0,
    // Posts tab (profile activity)
    val posts: List<ApiPost> = emptyList(),
    val postsLoading: Boolean = false,
    val postsHasMore: Boolean = false,
    val postsLoaded: Boolean = false,
    // Photo gallery (own profile only)
    val showPhotoGallery: Boolean = false,
    val photos: List<ApiUserPhoto> = emptyList(),
    val photosLoading: Boolean = false,
    val photoBusy: Boolean = false
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    private var currentUsername: String = ""

    fun loadProfile(username: String) {
        currentUsername = username
        viewModelScope.launch {
            _uiState.value = ProfileUiState(isLoading = true)
            try {
                val token = authRepository.getBearerToken()
                val profile = apiService.getProfile(token, username)
                var statsIsFollowing = profile.isFollowing ?: false
                var profileWithStats = profile
                try {
                    val stats = apiService.getProfileStats(token, username)
                    statsIsFollowing = stats.isFollowing
                    if (profile.isSelf == null) {
                        profileWithStats = profile.copy(isSelf = stats.isSelf)
                    }
                } catch (_: Exception) {}
                _uiState.update {
                    it.copy(
                        profile = profileWithStats,
                        isLoading = false,
                        isFollowing = statsIsFollowing,
                        followerCount = profileWithStats.followerCount
                    )
                }
                val isPrivate = profile.isLocked == 1 && profile.isSelf != true
                if (!isPrivate) {
                    loadPosts(reset = true)
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
            }
        }
    }

    fun selectTab(index: Int) {
        _uiState.update { it.copy(selectedTab = index) }
    }

    fun loadPosts(reset: Boolean = false) {
        val state = _uiState.value
        if (state.postsLoading) return
        if (!reset && state.postsLoaded && !state.postsHasMore) return
        if (currentUsername.isBlank()) return
        val username = currentUsername
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    postsLoading = true,
                    posts = if (reset) emptyList() else it.posts
                )
            }
            try {
                val token = authRepository.getBearerToken()
                val offset = if (reset) 0 else _uiState.value.posts.size
                val response = apiService.getProfileActivity(token, username, offset, POSTS_PAGE_SIZE)
                _uiState.update {
                    val merged = if (reset) response.posts
                    else (it.posts + response.posts).distinctBy { p -> p.id }
                    it.copy(
                        posts = merged,
                        postsHasMore = response.hasMore,
                        postsLoading = false,
                        postsLoaded = true
                    )
                }
            } catch (_: Exception) {
                _uiState.update { it.copy(postsLoading = false, postsLoaded = true) }
            }
        }
    }

    fun toggleFollow() {
        val profile = _uiState.value.profile ?: return
        viewModelScope.launch {
            try {
                val token = authRepository.getBearerToken() ?: return@launch
                val response = apiService.toggleFollow(token, profile.id)
                _uiState.update {
                    it.copy(
                        isFollowing = response.isFollowing,
                        followerCount = response.followerCount
                            ?: (it.followerCount + (if (response.isFollowing) 1 else -1))
                    )
                }
            } catch (_: Exception) { }
        }
    }

    // ----------------------------------------------------------------
    // Photo gallery (own profile only)
    // ----------------------------------------------------------------

    fun openPhotoGallery() {
        if (_uiState.value.profile?.isSelf != true) return
        _uiState.update { it.copy(showPhotoGallery = true) }
        loadPhotos()
    }

    fun closePhotoGallery() {
        _uiState.update { it.copy(showPhotoGallery = false) }
    }

    private fun loadPhotos() {
        viewModelScope.launch {
            _uiState.update { it.copy(photosLoading = true) }
            try {
                val token = authRepository.getBearerToken() ?: run {
                    _uiState.update { it.copy(photosLoading = false) }
                    return@launch
                }
                val photos = apiService.getUserPhotos(token)
                _uiState.update { it.copy(photos = photos, photosLoading = false) }
            } catch (_: Exception) {
                _uiState.update { it.copy(photosLoading = false) }
            }
        }
    }

    fun activatePhoto(photoId: Int) {
        if (_uiState.value.photoBusy) return
        viewModelScope.launch {
            _uiState.update { it.copy(photoBusy = true) }
            try {
                val token = authRepository.getBearerToken() ?: run {
                    _uiState.update { it.copy(photoBusy = false) }
                    return@launch
                }
                apiService.activatePhoto(token, photoId)
                // Refresh the locally cached profile (topbar avatar etc.)
                authRepository.refreshProfile()
                // Reload gallery + on-screen profile
                val photos = try { apiService.getUserPhotos(token) } catch (_: Exception) { _uiState.value.photos }
                val refreshed = try { apiService.getProfile(token, currentUsername) } catch (_: Exception) { null }
                _uiState.update {
                    it.copy(
                        photos = photos,
                        profile = refreshed ?: it.profile,
                        photoBusy = false
                    )
                }
            } catch (_: Exception) {
                _uiState.update { it.copy(photoBusy = false) }
            }
        }
    }

    fun uploadPhoto(bytes: ByteArray, mimeType: String) {
        if (_uiState.value.photoBusy) return
        viewModelScope.launch {
            _uiState.update { it.copy(photoBusy = true) }
            try {
                val requestBody = bytes.toRequestBody(mimeType.toMediaTypeOrNull())
                val filePart = MultipartBody.Part.createFormData("file", "profile_photo", requestBody)
                // AuthRepository helper also updates the cached photo URL.
                authRepository.uploadProfilePhoto(filePart)
                authRepository.refreshProfile()
                val token = authRepository.getBearerToken()
                val photos = if (token != null) {
                    try { apiService.getUserPhotos(token) } catch (_: Exception) { _uiState.value.photos }
                } else _uiState.value.photos
                val refreshed = if (token != null) {
                    try { apiService.getProfile(token, currentUsername) } catch (_: Exception) { null }
                } else null
                _uiState.update {
                    it.copy(
                        photos = photos,
                        profile = refreshed ?: it.profile,
                        photoBusy = false
                    )
                }
            } catch (_: Exception) {
                _uiState.update { it.copy(photoBusy = false) }
            }
        }
    }
}
