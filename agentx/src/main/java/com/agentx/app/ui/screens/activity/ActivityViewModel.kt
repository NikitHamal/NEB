package com.agentx.app.ui.screens.activity

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.entity.ActivityEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class ActivityViewModel @Inject constructor(
    private val activityDao: ActivityDao
) : ViewModel() {

    val entries: StateFlow<List<ActivityEntity>> =
        activityDao.observeRecent().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun clear() {
        viewModelScope.launch { activityDao.clear() }
    }
}
