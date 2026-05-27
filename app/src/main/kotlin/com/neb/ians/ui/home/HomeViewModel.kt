package com.neb.ians.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repo.ForumRepository
import com.neb.ians.data.repo.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class Announcement(val id: String, val title: String, val body: String)

data class HomeUi(
    val totalResources: Int = 0,
    val announcements: List<Announcement> = listOf(
        Announcement("a1", "Welcome to NEBians", "Find textbooks, notes and past papers for Grade 11 & 12."),
        Announcement("a2", "Annotations are here", "Highlight, underline and add notes on any PDF — offline."),
        Announcement("a3", "Join the forum", "Ask doubts and help peers in the discussion board."),
    ),
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val resourceRepo: ResourceRepository,
    private val forumRepo: ForumRepository,
) : ViewModel() {

    private val _state = MutableStateFlow(HomeUi())
    val uiState: StateFlow<HomeUi> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            resourceRepo.seedIfEmpty()
            forumRepo.seedIfEmpty()
        }
        viewModelScope.launch {
            resourceRepo.observeAll().collect { list ->
                _state.value = _state.value.copy(totalResources = list.size)
            }
        }
    }
}
