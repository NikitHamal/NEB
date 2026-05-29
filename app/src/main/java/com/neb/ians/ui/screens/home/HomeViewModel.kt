package com.neb.ians.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HomeUiState(
    val userName: String = "Student",
    val recentResources: List<ResourceEntity> = emptyList(),
    val popularResources: List<ResourceEntity> = emptyList(),
    val recentPosts: List<ForumPostEntity> = emptyList(),
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
    private val resourceRepository: ResourceRepository,
    private val forumRepository: ForumRepository,
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    private val _isLoading = MutableStateFlow(true)
    private val _error = MutableStateFlow<String?>(null)

    init {
        syncData()
    }

    private fun syncData() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                resourceRepository.syncResources()
            } catch (e: Exception) {
                _error.value = e.message ?: "Failed to load resources"
            }
            try {
                forumRepository.syncPosts()
            } catch (e: Exception) {
                if (_error.value == null) {
                    _error.value = e.message ?: "Failed to load forum posts"
                }
            }
            _isLoading.value = false
        }
    }

    fun refresh() {
        syncData()
    }

    val uiState: StateFlow<HomeUiState> = combine(
        settingsRepository.userName,
        resourceRepository.getAllResources().distinctUntilChanged(),
        forumRepository.getAllPosts().distinctUntilChanged(),
        _isLoading,
        _error
    ) { userName, resources, posts, isLoading, error ->
        HomeUiState(
            userName = userName,
            recentResources = resources.sortedByDescending { it.addedAt }.take(6),
            popularResources = resources.sortedByDescending { it.viewCount }.take(6),
            recentPosts = posts.sortedByDescending { it.createdAt }.take(3),
            isLoading = isLoading,
            error = error
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}