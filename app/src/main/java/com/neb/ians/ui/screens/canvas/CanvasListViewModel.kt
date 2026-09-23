package com.neb.ians.ui.screens.canvas

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class CanvasListViewModel @Inject constructor(
    private val repository: CanvasRepository
) : ViewModel() {

    val allBoards: StateFlow<List<CanvasBoard>> = repository.boards

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    val filteredBoards: StateFlow<List<CanvasBoard>> = combine(
        allBoards,
        _searchQuery
    ) { boards, query ->
        if (query.isBlank()) {
            boards
        } else {
            boards.filter { it.title.contains(query, ignoreCase = true) }
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )

    private val _createDialogOpen = MutableStateFlow(false)
    val createDialogOpen: StateFlow<Boolean> = _createDialogOpen.asStateFlow()

    private val _renameBoardTarget = MutableStateFlow<CanvasBoard?>(null)
    val renameBoardTarget: StateFlow<CanvasBoard?> = _renameBoardTarget.asStateFlow()

    private val _deleteBoardTarget = MutableStateFlow<CanvasBoard?>(null)
    val deleteBoardTarget: StateFlow<CanvasBoard?> = _deleteBoardTarget.asStateFlow()

    private val _isCreating = MutableStateFlow(false)
    val isCreating: StateFlow<Boolean> = _isCreating.asStateFlow()

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
    }

    fun openCreateDialog() {
        _createDialogOpen.value = true
    }

    fun closeCreateDialog() {
        _createDialogOpen.value = false
    }

    fun setRenameBoardTarget(board: CanvasBoard?) {
        _renameBoardTarget.value = board
    }

    fun setDeleteBoardTarget(board: CanvasBoard?) {
        _deleteBoardTarget.value = board
    }

    fun createCanvas(
        title: String,
        templateKey: String? = null,
        onCreated: (String) -> Unit
    ) {
        if (_isCreating.value) return
        _isCreating.value = true
        viewModelScope.launch {
            try {
                val newBoard = repository.createBoard(title, templateKey)
                _createDialogOpen.value = false
                _isCreating.value = false
                onCreated(newBoard.id)
            } catch (e: Exception) {
                e.printStackTrace()
                _isCreating.value = false
            }
        }
    }

    fun duplicateCanvas(boardId: String, onDuplicated: (String) -> Unit) {
        viewModelScope.launch {
            try {
                val copy = repository.duplicateBoard(boardId)
                onDuplicated(copy.id)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun renameCanvas(boardId: String, newTitle: String) {
        viewModelScope.launch {
            try {
                repository.renameBoard(boardId, newTitle)
                _renameBoardTarget.value = null
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun deleteCanvas(boardId: String) {
        viewModelScope.launch {
            try {
                repository.deleteBoard(boardId)
                _deleteBoardTarget.value = null
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
