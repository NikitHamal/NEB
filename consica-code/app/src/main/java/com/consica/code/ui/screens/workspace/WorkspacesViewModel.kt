package com.consica.code.ui.screens.workspace

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.repository.WorkspaceRepository
import com.consica.code.domain.model.TrackLanguage
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class WorkspacesUiState(
    val workspaces: List<WorkspaceEntity> = emptyList(),
)

@HiltViewModel
class WorkspacesViewModel @Inject constructor(
    private val workspaceRepository: WorkspaceRepository,
) : ViewModel() {

    val uiState: StateFlow<WorkspacesUiState> =
        workspaceRepository.workspaces
            .map { WorkspacesUiState(it) }
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), WorkspacesUiState())

    fun create(name: String, language: TrackLanguage, onCreated: (Long) -> Unit) {
        val trimmed = name.trim().take(40)
        if (trimmed.isEmpty()) return
        viewModelScope.launch {
            val initialContent = when (language) {
                TrackLanguage.HTML ->
                    "<!DOCTYPE html>\n<html>\n<body>\n\n</body>\n</html>\n"
                else -> "print(\"Hello!\")\n"
            }
            val id = workspaceRepository.create(
                name = trimmed,
                language = language,
                initialContent = initialContent,
            )
            onCreated(id)
        }
    }

    fun delete(id: Long) {
        viewModelScope.launch { workspaceRepository.delete(id) }
    }
}
