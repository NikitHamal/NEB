package com.agentx.app.ui.screens.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.chat.ChatRepository
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.NeedleModelManager
import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class SettingsViewModel @Inject constructor(
    val manager: NeedleModelManager,
    private val runtime: NeedleRuntime,
    private val settings: SettingsRepository,
    private val chatRepository: ChatRepository,
    private val activityDao: ActivityDao
) : ViewModel() {

    val modelState: StateFlow<AxModelState> = manager.state

    val isDarkMode: StateFlow<Boolean> = settings.isDarkMode
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), false)

    val confirmThreshold: StateFlow<Float> = settings.confirmThreshold
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), SettingsRepository.DEFAULT_CONFIRM_THRESHOLD)

    val confirmDestructive: StateFlow<Boolean> = settings.confirmDestructive
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), true)

    fun downloadModel() = manager.download()

    fun deleteModel() {
        runtime.release(true)
        manager.deleteModel { manager.recheck() }
    }

    fun resetRuntime() {
        runtime.release(true)
        runtime.restart()
    }

    fun setDarkMode(value: Boolean) {
        viewModelScope.launch { settings.setDarkMode(value) }
    }

    fun setConfirmThreshold(value: Float) {
        viewModelScope.launch { settings.setConfirmThreshold(value) }
    }

    fun setConfirmDestructive(value: Boolean) {
        viewModelScope.launch { settings.setConfirmDestructive(value) }
    }

    fun clearChat() {
        viewModelScope.launch { chatRepository.clearAll() }
    }

    fun clearActivity() {
        viewModelScope.launch { activityDao.clear() }
    }
}
