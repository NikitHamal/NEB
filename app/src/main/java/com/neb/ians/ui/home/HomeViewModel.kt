package com.neb.ians.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.ResourceRepository
import com.neb.ians.data.local.ResourceEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repo: ResourceRepository,
) : ViewModel() {
    val recent: StateFlow<List<ResourceEntity>> =
        repo.recent(10).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
    val favorites: StateFlow<List<ResourceEntity>> =
        repo.favorites().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
    val all: StateFlow<List<ResourceEntity>> =
        repo.search().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
}
