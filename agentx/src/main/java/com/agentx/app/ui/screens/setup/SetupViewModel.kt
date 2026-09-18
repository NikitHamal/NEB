package com.agentx.app.ui.screens.setup

import androidx.lifecycle.ViewModel
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.NeedleModelManager
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.StateFlow

@HiltViewModel
class SetupViewModel @Inject constructor(
    val manager: NeedleModelManager
) : ViewModel() {
    val state: StateFlow<AxModelState> = manager.state

    fun download() = manager.download()

    fun cancel() = manager.cancelDownload()
}
