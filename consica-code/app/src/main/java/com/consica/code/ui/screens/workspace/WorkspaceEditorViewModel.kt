package com.consica.code.ui.screens.workspace

import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.local.entity.WorkspaceFileEntity
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.WorkspaceRepository
import com.consica.code.domain.execution.ExecutionError
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.TrackLanguage
import com.consica.code.domain.python.PythonInterpreter
import com.consica.code.ui.playground.CodeKey
import com.consica.code.ui.playground.applyCodeKey
import com.consica.code.util.AppSound
import com.consica.code.util.SoundManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import javax.inject.Inject

data class WorkspaceEditorUiState(
    val workspace: WorkspaceEntity? = null,
    val files: List<WorkspaceFileEntity> = emptyList(),
    val selectedFileId: Long? = null,
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val proEditor: Boolean = false,
    val dirty: Boolean = false,
    val justSaved: Boolean = false,
    val running: Boolean = false,
    val hasRun: Boolean = false,
    val output: String = "",
    val error: ExecutionError? = null,
) {
    val language: TrackLanguage
        get() = workspace?.language?.let { name ->
            TrackLanguage.entries.firstOrNull { it.name == name }
        } ?: TrackLanguage.PYTHON

    val selectedFile: WorkspaceFileEntity?
        get() = files.firstOrNull { it.id == selectedFileId }
}

@HiltViewModel
class WorkspaceEditorViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    prefs: UserPreferencesRepository,
    private val workspaceRepository: WorkspaceRepository,
    private val soundManager: SoundManager,
) : ViewModel() {

    private val workspaceId: Long = savedStateHandle.get<Long>("workspaceId") ?: -1L

    private val _uiState = MutableStateFlow(WorkspaceEditorUiState())
    val uiState: StateFlow<WorkspaceEditorUiState> = _uiState

    private val _code = MutableStateFlow(TextFieldValue(""))
    val code: StateFlow<TextFieldValue> = _code

    init {
        viewModelScope.launch {
            workspaceRepository.observe(workspaceId).collect { workspace ->
                _uiState.update { it.copy(workspace = workspace) }
            }
        }
        viewModelScope.launch {
            workspaceRepository.observeFiles(workspaceId).collect { files ->
                _uiState.update { state ->
                    val selected = state.selectedFileId
                        ?.takeIf { id -> files.any { it.id == id } }
                        ?: files.firstOrNull()?.id
                    state.copy(files = files, selectedFileId = selected)
                }
                if (!_uiState.value.dirty) {
                    _uiState.value.selectedFile?.let { file ->
                        if (file.content != _code.value.text) {
                            _code.value = TextFieldValue(file.content, TextRange(file.content.length))
                        }
                    }
                }
            }
        }
        viewModelScope.launch {
            prefs.profile.collect { profile ->
                _uiState.update { it.copy(ageGroup = profile.ageGroup) }
            }
        }
        viewModelScope.launch {
            kotlinx.coroutines.flow.combine(prefs.settings, prefs.stats) { settings, stats ->
                settings.professionalModeEnabled && stats.professionalModeUnlocked
            }.collect { pro ->
                _uiState.update { it.copy(proEditor = pro) }
            }
        }
    }

    fun onCodeChange(value: TextFieldValue) {
        val changed = value.text != _code.value.text
        _code.value = value
        if (changed) _uiState.update { it.copy(dirty = true, justSaved = false) }
    }

    fun onCodeKey(key: CodeKey) {
        soundManager.play(AppSound.TAP)
        val current = _code.value
        val (newText, newCursor) = applyCodeKey(current.text, current.selection.start, key)
        _code.value = TextFieldValue(newText, TextRange(newCursor))
        _uiState.update { it.copy(dirty = true, justSaved = false) }
    }

    fun selectFile(fileId: Long) {
        val state = _uiState.value
        if (fileId == state.selectedFileId) return
        viewModelScope.launch {
            saveCurrent()
            _uiState.update { it.copy(selectedFileId = fileId, dirty = false, justSaved = false) }
            _uiState.value.selectedFile?.let { file ->
                _code.value = TextFieldValue(file.content, TextRange(file.content.length))
            }
        }
    }

    fun addFile(name: String) {
        val trimmed = name.trim().take(60)
        if (trimmed.isEmpty()) return
        viewModelScope.launch {
            saveCurrent()
            val id = workspaceRepository.addFile(workspaceId, trimmed)
            _uiState.update { it.copy(selectedFileId = id, dirty = false) }
            _code.value = TextFieldValue("")
        }
    }

    fun deleteFile(fileId: Long) {
        val state = _uiState.value
        if (state.files.size <= 1) return
        viewModelScope.launch {
            workspaceRepository.deleteFile(fileId)
            if (state.selectedFileId == fileId) {
                _uiState.update { it.copy(selectedFileId = null, dirty = false) }
            }
        }
    }

    fun save() {
        viewModelScope.launch {
            saveCurrent()
            soundManager.play(AppSound.SUCCESS)
            _uiState.update { it.copy(justSaved = true) }
        }
    }

    private suspend fun saveCurrent() {
        val file = _uiState.value.selectedFile ?: return
        if (!_uiState.value.dirty && file.content == _code.value.text) return
        workspaceRepository.saveFile(file, _code.value.text)
        _uiState.update { it.copy(dirty = false) }
    }

    fun run() {
        val state = _uiState.value
        if (state.running) return
        soundManager.play(AppSound.GROW)
        _uiState.update { it.copy(running = true, error = null) }
        val codeText = _code.value.text

        viewModelScope.launch {
            saveCurrent()
            if (state.language == TrackLanguage.HTML) {
                _uiState.update {
                    it.copy(running = false, hasRun = true, output = codeText, error = null)
                }
                return@launch
            }
            val result = withContext(Dispatchers.Default) {
                PythonInterpreter().run(codeText)
            }
            if (result.error != null) soundManager.play(AppSound.GENTLE_ERROR)
            _uiState.update {
                it.copy(
                    running = false,
                    hasRun = true,
                    output = result.output,
                    error = result.error,
                )
            }
        }
    }

    fun dismissSaved() = _uiState.update { it.copy(justSaved = false) }
}
