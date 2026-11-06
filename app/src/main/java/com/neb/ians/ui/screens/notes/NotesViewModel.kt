package com.neb.ians.ui.screens.notes

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.NoteEntity
import com.neb.ians.data.repository.NotesRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

enum class NoteFilter(val label: String) { All("All"), Pinned("Pinned"), Archive("Archive"), Trash("Bin") }

enum class NoteSort(val label: String) { Edited("Last edited"), Created("Date created"), Title("Title") }

private data class Controls(
    val query: String = "",
    val filter: NoteFilter = NoteFilter.All,
    val tag: String? = null,
    val sort: NoteSort = NoteSort.Edited,
    val grid: Boolean = true,
    val selection: Set<String> = emptySet(),
    val searching: Boolean = false,
)

data class NotesUi(
    val loaded: Boolean = false,
    val notes: List<NoteEntity> = emptyList(),
    val tags: List<String> = emptyList(),
    val query: String = "",
    val filter: NoteFilter = NoteFilter.All,
    val tag: String? = null,
    val sort: NoteSort = NoteSort.Edited,
    val grid: Boolean = true,
    val selection: Set<String> = emptySet(),
    val searching: Boolean = false,
    val binCount: Int = 0,
    val totalLive: Int = 0,
)

@HiltViewModel
class NotesViewModel @Inject constructor(
    private val repo: NotesRepository,
    @ApplicationContext context: Context,
) : ViewModel() {
    private val prefs = context.getSharedPreferences("neb_notes", Context.MODE_PRIVATE)
    private val controls = MutableStateFlow(
        Controls(
            sort = NoteSort.entries.getOrElse(prefs.getInt("sort", 0)) { NoteSort.Edited },
            grid = prefs.getBoolean("grid", true),
        )
    )

    val ui: StateFlow<NotesUi> = combine(repo.notes, controls) { all, c ->
        val live = all.filter { !it.isTrashed }
        val tags = live.filter { !it.archived }.flatMap { it.tagList }.groupingBy { it }.eachCount()
            .entries.sortedByDescending { it.value }.map { it.key }
        val base = when (c.filter) {
            NoteFilter.All -> live.filter { !it.archived }
            NoteFilter.Pinned -> live.filter { it.pinned && !it.archived }
            NoteFilter.Archive -> live.filter { it.archived }
            NoteFilter.Trash -> all.filter { it.isTrashed }
        }
        val q = c.query.trim().lowercase()
        val filtered = base.filter { n ->
            (c.tag == null || c.tag in n.tagList) &&
                (q.isEmpty() || n.title.lowercase().contains(q) || n.body.lowercase().contains(q) || n.tags.contains(q.removePrefix("#")))
        }
        val sorted = when (c.sort) {
            NoteSort.Edited -> filtered.sortedByDescending { it.updatedAt }
            NoteSort.Created -> filtered.sortedByDescending { it.createdAt }
            NoteSort.Title -> filtered.sortedBy { it.title.lowercase().ifBlank { "\uFFFF" } }
        }
        val ordered = if (c.filter == NoteFilter.All) sorted.sortedByDescending { it.pinned } else sorted
        NotesUi(
            loaded = true, notes = ordered, tags = tags, query = c.query, filter = c.filter, tag = c.tag,
            sort = c.sort, grid = c.grid, selection = c.selection.intersect(ordered.map { it.id }.toSet()),
            searching = c.searching, binCount = all.count { it.isTrashed }, totalLive = live.size,
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), NotesUi())

    init {
        viewModelScope.launch { repo.purgeOldTrash() }
    }

    fun setQuery(q: String) = controls.update { it.copy(query = q) }
    fun setSearching(on: Boolean) = controls.update { it.copy(searching = on, query = if (on) it.query else "") }
    fun setFilter(f: NoteFilter) = controls.update { it.copy(filter = f, selection = emptySet()) }
    fun setTag(t: String?) = controls.update { it.copy(tag = if (it.tag == t) null else t) }

    fun setSort(s: NoteSort) {
        prefs.edit().putInt("sort", s.ordinal).apply()
        controls.update { it.copy(sort = s) }
    }

    fun toggleGrid() {
        val next = !controls.value.grid
        prefs.edit().putBoolean("grid", next).apply()
        controls.update { it.copy(grid = next) }
    }

    fun toggleSelect(id: String) = controls.update {
        it.copy(selection = if (id in it.selection) it.selection - id else it.selection + id)
    }

    fun clearSelection() = controls.update { it.copy(selection = emptySet()) }
    fun selectAll() = controls.update { c -> c.copy(selection = ui.value.notes.map { it.id }.toSet()) }

    private fun selected(): List<String> = ui.value.selection.toList()

    /** Each returns the ids it touched so the screen can offer Undo. */
    fun pinSelected(): List<String> = selected().also { ids ->
        val pin = ui.value.notes.filter { it.id in ids }.any { !it.pinned }
        viewModelScope.launch { repo.setPinned(ids, pin) }
        clearSelection()
    }

    fun archiveSelected(): List<String> = selected().also { ids ->
        val archive = ui.value.filter != NoteFilter.Archive
        viewModelScope.launch { repo.setArchived(ids, archive) }
        clearSelection()
    }

    fun trashSelected(): List<String> = selected().also { ids ->
        viewModelScope.launch { repo.trash(ids) }
        clearSelection()
    }

    fun restoreSelected(): List<String> = selected().also { ids ->
        viewModelScope.launch { repo.restore(ids) }
        clearSelection()
    }

    fun deleteSelectedForever() {
        val ids = selected()
        viewModelScope.launch { repo.deleteForever(ids) }
        clearSelection()
    }

    fun toneSelected(tone: Int) {
        val ids = selected()
        viewModelScope.launch { repo.setTone(ids, tone) }
        clearSelection()
    }

    fun restore(ids: List<String>) = viewModelScope.launch { repo.restore(ids) }
    fun archive(ids: List<String>) = viewModelScope.launch { repo.setArchived(ids, true) }
    fun unarchive(ids: List<String>) = viewModelScope.launch { repo.setArchived(ids, false) }
    fun emptyBin() = viewModelScope.launch { repo.emptyTrash() }
}
