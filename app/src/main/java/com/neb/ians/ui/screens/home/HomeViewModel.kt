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
import javax.inject.Inject

data class HomeUiState(
    val userName: String = "Student",
    val recentResources: List<ResourceEntity> = emptyList(),
    val popularResources: List<ResourceEntity> = emptyList(),
    val recentPosts: List<ForumPostEntity> = emptyList(),
    val subjects: List<String> = listOf(
        "Physics", "Chemistry", "Mathematics", "Biology",
        "English", "Nepali", "Computer Science", "Economics", "Accountancy"
    )
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val resourceRepository: ResourceRepository,
    private val forumRepository: ForumRepository,
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    val uiState: StateFlow<HomeUiState> = combine(
        settingsRepository.userName,
        resourceRepository.getAllResources(),
        forumRepository.getAllPosts()
    ) { userName, resources, posts ->
        HomeUiState(
            userName = userName,
            recentResources = resources.sortedByDescending { it.addedAt }.take(6),
            popularResources = resources.sortedByDescending { it.viewCount }.take(6),
            recentPosts = posts.sortedByDescending { it.createdAt }.take(3)
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeUiState())
}
