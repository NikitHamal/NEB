package com.agentx.app.ui.screens.setup

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.NeedleModelManager
import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.tools.ToolCatalog
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

@HiltViewModel
class SetupViewModel @Inject constructor(
    val manager: NeedleModelManager,
    private val runtime: NeedleRuntime
) : ViewModel() {
    val state: StateFlow<AxModelState> = manager.state

    init {
        runtime.setToolsJson(ToolCatalog.buildJson())
        viewModelScope.launch {
            manager.state.collect { state ->
                if (state is AxModelState.Ready) runtime.prepare()
            }
        }
    }

    fun download() = manager.download()

    fun cancel() = manager.cancelDownload()
}
