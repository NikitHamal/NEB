package com.neb.ians.ui.screens.canvas

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.CanvasBoard
import com.neb.ians.data.api.CanvasTemplate
import com.neb.ians.data.repository.CanvasRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CanvasListUiState(
    val boards: List<CanvasBoard> = emptyList(),
    val templates: List<CanvasTemplate> = emptyList(),
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val isWorking: Boolean = false,
    val error: String? = null,
    val snackbarMessage: String? = null
)

@HiltViewModel
class CanvasListViewModel @Inject constructor(
    private val repository: CanvasRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CanvasListUiState())
    val uiState: StateFlow<CanvasListUiState> = _uiState.asStateFlow()

    init { refresh() }

    fun refresh(pull: Boolean = false) {
        viewModelScope.launch {
            if (pull) {
                _uiState.update { it.copy(isRefreshing = true) }
            } else {
                _uiState.update { it.copy(isLoading = it.boards.isEmpty(), error = null) }
            }
            val boards = repository.getBoards()
            val templates = repository.getTemplates()
            _uiState.update {
                it.copy(
                    isLoading = false,
                    isRefreshing = false,
                    boards = boards.getOrDefault(it.boards),
                    templates = templates.getOrDefault(it.templates),
                    error = if (boards.isFailure && it.boards.isEmpty()) {
                        boards.exceptionOrNull()?.message
                    } else null
                )
            }
        }
    }

    fun createBoard(title: String, onCreated: (String) -> Unit) {
        viewModelScope.launch {
            _uiState.update { it.copy(isWorking = true) }
            val result = repository.createBoard(title)
            _uiState.update { it.copy(isWorking = false) }
            result.onSuccess { board ->
                _uiState.update { s -> s.copy(boards = listOf(board) + s.boards) }
                onCreated(board.id)
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message ?: "Could not create board") }
            }
        }
    }

    fun renameBoard(boardId: String, title: String) {
        viewModelScope.launch {
            repository.renameBoard(boardId, title).onSuccess { board ->
                _uiState.update { s -> s.copy(boards = s.boards.map { if (it.id == boardId) board else it }) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message ?: "Could not rename board") }
            }
        }
    }

    fun deleteBoard(boardId: String) {
        viewModelScope.launch {
            repository.deleteBoard(boardId).onSuccess {
                _uiState.update { s -> s.copy(boards = s.boards.filterNot { it.id == boardId }) }
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message ?: "Could not delete board") }
            }
        }
    }

    fun createFromTemplate(template: String, title: String, onCreated: (String) -> Unit) {
        viewModelScope.launch {
            _uiState.update { it.copy(isWorking = true) }
            val result = repository.createFromTemplate(template, title)
            _uiState.update { it.copy(isWorking = false) }
            result.onSuccess { (board, _) ->
                _uiState.update { s -> s.copy(boards = listOf(board) + s.boards) }
                onCreated(board.id)
            }.onFailure { e ->
                _uiState.update { it.copy(snackbarMessage = e.message ?: "Could not create board") }
            }
        }
    }

    fun consumeSnackbar() {
        _uiState.update { it.copy(snackbarMessage = null) }
    }
}
