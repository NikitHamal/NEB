package com.neb.ians.ui.screens.home

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.SampleData
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.ResourceRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class HomeViewModel(application: Application) : AndroidViewModel(application) {

    private val db = (application as NEBiansApp).database
    private val repository = ResourceRepository(db.resourceDao(), db.bookmarkDao())

    val recentResources: StateFlow<List<ResourceEntity>> = repository.getAllResources()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        viewModelScope.launch {
            val existing = db.resourceDao().getResourceById(1)
            if (existing == null) {
                repository.insertAll(SampleData.getSampleResources())
                SampleData.getSamplePosts().forEach { post ->
                    db.forumDao().insertPost(post)
                }
            }
        }
    }
}
