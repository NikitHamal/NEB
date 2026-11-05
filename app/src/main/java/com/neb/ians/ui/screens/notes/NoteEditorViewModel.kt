package com.neb.ians.ui.screens.notes

import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.NoteEntity
import com.neb.ians.data.repository.NotesRepository
import com.neb.ians.speech.DictationState
import com.neb.ians.speech.NoteSpeechText
import com.neb.ians.speech.PhononEngine
import com.neb.ians.speech.ReadProgress
import com.neb.ians.speech.ReadState
import com.neb.ians.speech.WhistleEngine
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.NonCancellable
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class NoteEditorViewModel @Inject constructor(
    handle: SavedStateHandle,
    private val repo: NotesRepository,
    private val whistle: WhistleEngine,
    private val phonon: PhononEngine,
) : ViewModel() {
    private val noteId: String = handle.get<String>("noteId") ?: "new"
    val startDictating: Boolean = handle.get<Boolean>("dictate") ?: false

    private var note: NoteEntity? = null
    private var existsInDb = false
    private var saveJob: Job? = null

    private val _ready = MutableStateFlow(false)
    val ready: StateFlow<Boolean> = _ready.asStateFlow()
    private val _title = MutableStateFlow("")
    val title: StateFlow<String> = _title.asStateFlow()
    private val _body = MutableStateFlow(TextFieldValue(""))
    val body: StateFlow<TextFieldValue> = _body.asStateFlow()
    private val _tone = MutableStateFlow(0)
    val tone: StateFlow<Int> = _tone.asStateFlow()
    private val _tags = MutableStateFlow<List<String>>(emptyList())
    val tags: StateFlow<List<String>> = _tags.asStateFlow()
    private val _pinned = MutableStateFlow(false)
    val pinned: StateFlow<Boolean> = _pinned.asStateFlow()
    private val _archived = MutableStateFlow(false)
    val archived: StateFlow<Boolean> = _archived.asStateFlow()
    private val _trashed = MutableStateFlow(false)
    val trashed: StateFlow<Boolean> = _trashed.asStateFlow()
    private val _preview = MutableStateFlow(false)
    val preview: StateFlow<Boolean> = _preview.asStateFlow()
    private val _canUndo = MutableStateFlow(false)
    val canUndo: StateFlow<Boolean> = _canUndo.asStateFlow()
    private val _canRedo = MutableStateFlow(false)
    val canRedo: StateFlow<Boolean> = _canRedo.asStateFlow()

    val dictation: StateFlow<DictationState> = whistle.state
    val level: StateFlow<Float> = whistle.level
    val pending: StateFlow<String> = whistle.pending
    val seconds: StateFlow<Int> = whistle.seconds
    val readState: StateFlow<ReadState> = phonon.state
    val readProgress: StateFlow<ReadProgress?> = phonon.progress

    private val undoStack = ArrayDeque<TextFieldValue>()
    private val redoStack = ArrayDeque<TextFieldValue>()
    private var lastPushAt = 0L
    private var anchor = 0

    init {
        viewModelScope.launch {
            val existing = if (noteId == "new") null else repo.get(noteId)
            if (existing != null) {
                note = existing
                existsInDb = true
                _title.value = existing.title
                _body.value = TextFieldValue(existing.body, TextRange(existing.body.length))
                _tone.value = existing.tone
                _tags.value = existing.tagList
                _pinned.value = existing.pinned
                _archived.value = existing.archived
                _trashed.value = existing.isTrashed
                _preview.value = existing.body.isNotBlank()
            }
            _ready.value = true
        }
        viewModelScope.launch {
            whistle.committed.collect { insertDictated(it) }
        }
    }

    val isNew: Boolean get() = noteId == "new"
    val currentId: String get() = (note ?: repo.blank().also { note = it }).id

    // ---- text

    fun setTitle(t: String) {
        _title.value = t
        scheduleSave()
    }

    fun onBodyChange(new: TextFieldValue) {
        val old = _body.value
        if (new.text == old.text) {
            _body.value = new
            return
        }
        val next = NoteFormatting.continueList(old, new) ?: new
        pushHistory(old, force = false)
        _body.value = next
        scheduleSave()
    }

    fun format(change: (TextFieldValue) -> TextFieldValue) {
        val old = _body.value
        val next = change(old)
        if (next.text != old.text) pushHistory(old, force = true)
        _body.value = next
        scheduleSave()
    }

    private fun pushHistory(old: TextFieldValue, force: Boolean) {
        val now = System.currentTimeMillis()
        if (force || undoStack.isEmpty() || now - lastPushAt > 700) {
            undoStack.addLast(old)
            if (undoStack.size > 120) undoStack.removeFirst()
            redoStack.clear()
            lastPushAt = now
        }
        _canUndo.value = undoStack.isNotEmpty()
        _canRedo.value = redoStack.isNotEmpty()
    }

    fun undo() {
        val prev = undoStack.removeLastOrNull() ?: return
        redoStack.addLast(_body.value)
        _body.value = prev
        lastPushAt = 0
        _canUndo.value = undoStack.isNotEmpty()
        _canRedo.value = true
        scheduleSave()
    }

    fun redo() {
        val next = redoStack.removeLastOrNull() ?: return
        undoStack.addLast(_body.value)
        _body.value = next
        lastPushAt = 0
        _canUndo.value = true
        _canRedo.value = redoStack.isNotEmpty()
        scheduleSave()
    }

    fun togglePreview() {
        _preview.value = !_preview.value
    }

    fun setPreview(on: Boolean) {
        _preview.value = on
    }

    fun toggleCheck(line: Int) {
        NoteFormatting.toggleCheck(_body.value.text, line)?.let {
            _body.value = TextFieldValue(it, _body.value.selection)
            scheduleSave()
        }
    }

    // ---- meta

    fun setTone(t: Int) {
        _tone.value = t
        scheduleSave()
    }

    fun togglePin() {
        _pinned.value = !_pinned.value
        if (_pinned.value) _archived.value = false
        scheduleSave()
    }

    fun toggleArchive() {
        _archived.value = !_archived.value
        if (_archived.value) _pinned.value = false
        scheduleSave()
    }

    fun addTag(raw: String) {
        val tag = raw.trim().removePrefix("#").lowercase().replace(Regex("[^\\p{L}\\p{N}-]+"), "-").trim('-').take(24)
        if (tag.isNotEmpty() && tag !in _tags.value && _tags.value.size < 8) {
            _tags.value = _tags.value + tag
            scheduleSave()
        }
    }

    fun removeTag(tag: String) {
        _tags.value = _tags.value - tag
        scheduleSave()
    }

    // ---- persistence

    private fun scheduleSave() {
        saveJob?.cancel()
        saveJob = viewModelScope.launch {
            delay(500)
            persist()
        }
    }

    /** Called when the screen leaves composition; lets pending edits finish saving. */
    fun flush() {
        saveJob?.cancel()
        viewModelScope.launch(NonCancellable) { persist() }
    }

    private suspend fun persist() {
        if (!_ready.value) return
        val title = _title.value.trim()
        val body = _body.value.text
        val base = note ?: repo.blank()
        if (title.isBlank() && body.isBlank()) {
            if (existsInDb) {
                repo.deleteForever(listOf(base.id))
                existsInDb = false
                note = null
            }
            return
        }
        val updated = base.copy(
            title = title,
            body = body,
            tone = _tone.value,
            tags = _tags.value.joinToString(" "),
            pinned = _pinned.value,
            archived = _archived.value,
        )
        val textChanged = existsInDb && (base.title != updated.title || base.body != updated.body || base.tags != updated.tags)
        repo.save(updated, touch = !existsInDb || textChanged)
        note = updated.copy(updatedAt = if (!existsInDb || textChanged) System.currentTimeMillis() else base.updatedAt)
        existsInDb = true
    }

    fun moveToBin(onDone: () -> Unit) {
        saveJob?.cancel()
        viewModelScope.launch(NonCancellable) {
            persist()
            note?.let { repo.trash(listOf(it.id)) }
            onDone()
        }
    }

    fun restoreFromBin() {
        viewModelScope.launch {
            note?.let { repo.restore(listOf(it.id)) }
            _trashed.value = false
        }
    }

    fun deleteForever(onDone: () -> Unit) {
        saveJob?.cancel()
        viewModelScope.launch(NonCancellable) {
            note?.let { repo.deleteForever(listOf(it.id)) }
            existsInDb = false
            note = null
            _title.value = ""
            _body.value = TextFieldValue("")
            onDone()
        }
    }

    fun duplicate(onCreated: (String) -> Unit) {
        viewModelScope.launch {
            persist()
            note?.let { n -> repo.duplicate(n.id)?.let(onCreated) }
        }
    }

    fun shareText(): String {
        val t = _title.value.trim()
        val b = _body.value.text.trim()
        return if (t.isEmpty()) b else if (b.isEmpty()) t else "$t\n\n$b"
    }

    // ---- voice

    fun startDictation() {
        phonon.stop()
        _preview.value = false
        anchor = _body.value.selection.end
        whistle.start()
    }

    fun stopDictation() = whistle.stop()
    fun clearDictationError() = whistle.clearError()

    private fun insertDictated(text: String) {
        val cur = _body.value
        val pos = anchor.coerceIn(0, cur.text.length)
        val before = cur.text.substring(0, pos)
        val lead = if (before.isNotEmpty() && !before.last().isWhitespace()) " " else ""
        val piece = lead + text
        pushHistory(cur, force = false)
        _body.value = TextFieldValue(before + piece + cur.text.substring(pos), TextRange(pos + piece.length))
        anchor = pos + piece.length
        scheduleSave()
    }

    fun listen() {
        whistle.cancel()
        val segments = NoteSpeechText.segments(_title.value, _body.value.text)
        phonon.play(segments)
    }

    fun readPause() = phonon.toggle()
    fun readNext() = phonon.next()
    fun readPrevious() = phonon.previous()
    fun readStop() = phonon.stop()
    fun clearReadError() = phonon.clearError()

    override fun onCleared() {
        whistle.cancel()
        phonon.stop()
        super.onCleared()
    }
}
