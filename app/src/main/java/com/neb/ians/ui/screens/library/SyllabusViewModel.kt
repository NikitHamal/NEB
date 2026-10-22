package com.neb.ians.ui.screens.library

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiSyllabusDoc
import com.neb.ians.data.api.ApiSyllabusHit
import com.neb.ians.data.api.ApiSyllabusIndex
import com.neb.ians.data.repository.StudyMark
import com.neb.ians.data.repository.StudyProgress
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

enum class SyllabusShow { All, ToStudy, Done }

data class SyllabusUiState(
    val index: ApiSyllabusIndex? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val grade: String = "12",
    val query: String = "",
    val hits: List<ApiSyllabusHit> = emptyList(),
    val hitTotal: Int = 0,
    val isSearching: Boolean = false,
    val openSubject: String? = null,
    val openGrade: String? = null,
    val doc: ApiSyllabusDoc? = null,
    val isDocLoading: Boolean = false,
    val docError: String? = null,
    val focusUnit: Int? = null,
    val expanded: Set<Int> = emptySet(),
    val show: SyllabusShow = SyllabusShow.All,
    val area: String? = null,
    val filter: String = "",
    val done: Map<String, Set<String>> = emptyMap(),
    val lastKey: String? = null,
    /** Reading progress per chapter, "<grade>/<subject>/unit<N>" -> mark (StudyProgress). */
    val marks: Map<String, StudyMark> = emptyMap(),
    /** The chapter opened most recently: key, title, "Class 11 · Physics". */
    val lastRead: Triple<String, String, String>? = null,
    val tab: SyllabusTab = SyllabusTab.Chapters
) {
    /** Chapters of one subject counted as done. */
    fun chaptersDone(grade: String, subject: String): Int =
        marks.count { (k, m) -> k.startsWith("$grade/$subject/unit") && m.isDone }

    fun mark(grade: String, subject: String, unit: Int): StudyMark? = marks["$grade/$subject/unit$unit"]
}

enum class SyllabusTab { Chapters, Bank, Exam }

/**
 * The syllabus tab: Class 8, 10, 11 and 12, as exported from the NEBians books
 * (`api/syllabus/v2/`): every unit with its full chapter, the question bank and the exam
 * pattern. Reading progress comes from [StudyProgress], keyed like the website's.
 */
@HiltViewModel
class SyllabusViewModel @Inject constructor(
    private val apiService: ApiService,
    private val progress: StudyProgress,
    application: Application
) : ViewModel() {

    private val prefs = application.getSharedPreferences(PREFS, 0)
    private val _uiState = MutableStateFlow(
        SyllabusUiState(
            grade = prefs.getString(KEY_GRADE, null) ?: "12",
            done = readDone(),
            lastKey = prefs.getString(KEY_LAST, null)
        )
    )
    val uiState: StateFlow<SyllabusUiState> = _uiState.asStateFlow()
    private var searchJob: Job? = null

    init {
        load()
        viewModelScope.launch {
            progress.version.collect {
                _uiState.update { it.copy(marks = progress.snapshot(), lastRead = progress.last()) }
            }
        }
    }

    fun setTab(tab: SyllabusTab) = _uiState.update { it.copy(tab = tab) }

    fun refresh(): Job = viewModelScope.launch {
        val open = _uiState.value
        val grade = open.openGrade
        val subject = open.openSubject
        load().join()
        if (grade != null && subject != null) fetchDoc(grade, subject, keepView = true).join()
    }

    fun load(): Job = viewModelScope.launch {
        _uiState.update { it.copy(isLoading = it.index == null, error = null) }
        try {
            val index = apiService.getSyllabusIndex()
            _uiState.update { state ->
                val grade = state.grade.takeIf { g -> index.grades.any { it.grade == g } }
                    ?: index.grades.lastOrNull()?.grade ?: state.grade
                state.copy(index = index, isLoading = false, grade = grade)
            }
        } catch (e: Exception) {
            _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
        }
    }

    fun selectGrade(grade: String) {
        prefs.edit().putString(KEY_GRADE, grade).apply()
        _uiState.update { it.copy(grade = grade) }
        if (_uiState.value.query.isNotBlank()) search(_uiState.value.query)
    }

    fun search(query: String) {
        _uiState.update { it.copy(query = query) }
        searchJob?.cancel()
        val q = query.trim()
        if (q.length < 2) {
            _uiState.update { it.copy(hits = emptyList(), hitTotal = 0, isSearching = false) }
            return
        }
        searchJob = viewModelScope.launch {
            delay(220)
            _uiState.update { it.copy(isSearching = true) }
            try {
                val result = apiService.searchSyllabus(q, _uiState.value.grade)
                _uiState.update { it.copy(hits = result.results, hitTotal = result.total, isSearching = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isSearching = false) }
            }
        }
    }

    fun openSubject(grade: String, subject: String, unit: Int? = null) {
        val key = "$grade/$subject"
        prefs.edit().putString(KEY_LAST, key).apply()
        _uiState.update {
            it.copy(
                openGrade = grade,
                openSubject = subject,
                doc = null,
                docError = null,
                focusUnit = unit,
                expanded = emptySet(),
                show = SyllabusShow.All,
                area = null,
                filter = "",
                lastKey = key,
                tab = SyllabusTab.Chapters
            )
        }
        fetchDoc(grade, subject, keepView = false)
    }

    fun openLast() {
        val key = _uiState.value.lastKey ?: return
        val parts = key.split("/")
        if (parts.size == 2) openSubject(parts[0], parts[1])
    }

    fun retryDoc() {
        val state = _uiState.value
        if (state.openGrade != null && state.openSubject != null) fetchDoc(state.openGrade, state.openSubject, keepView = true)
    }

    private fun fetchDoc(grade: String, subject: String, keepView: Boolean): Job = viewModelScope.launch {
        _uiState.update { it.copy(isDocLoading = it.doc == null || !keepView, docError = null) }
        try {
            val doc = apiService.getSyllabusDoc(grade, subject)
            _uiState.update {
                if (it.openSubject == subject && it.openGrade == grade) it.copy(doc = doc, isDocLoading = false) else it
            }
        } catch (e: Exception) {
            _uiState.update { it.copy(isDocLoading = false, docError = ApiErrorMapper.mapException(e)) }
        }
    }

    fun closeSubject() {
        _uiState.update { it.copy(openGrade = null, openSubject = null, doc = null, docError = null, focusUnit = null) }
    }

    fun consumeFocus() {
        _uiState.update { it.copy(focusUnit = null) }
    }

    fun toggleUnit(no: Int) {
        _uiState.update { it.copy(expanded = if (no in it.expanded) it.expanded - no else it.expanded + no) }
    }

    fun expandAll(open: Boolean) {
        _uiState.update { state ->
            state.copy(expanded = if (open) state.doc?.units?.map { it.no }?.toSet().orEmpty() else emptySet())
        }
    }

    fun setShow(show: SyllabusShow) = _uiState.update { it.copy(show = show) }

    fun setArea(area: String?) = _uiState.update { it.copy(area = area) }

    fun setFilter(text: String) = _uiState.update { it.copy(filter = text) }

    fun toggleTopic(key: String, topicId: String) {
        updateDone(key) { if (topicId in it) it - topicId else it + topicId }
    }

    fun setUnitDone(key: String, unitNo: Int, topicCount: Int, done: Boolean) {
        val ids = (0 until topicCount).map { "$unitNo.$it" }
        updateDone(key) { if (done) it + ids else it - ids.toSet() }
    }

    fun resetSubject(key: String) = updateDone(key) { emptySet() }

    private fun updateDone(key: String, change: (Set<String>) -> Set<String>) {
        _uiState.update { state ->
            val next = change(state.done[key].orEmpty())
            val all = if (next.isEmpty()) state.done - key else state.done + (key to next)
            prefs.edit().putStringSet(KEY_DONE_PREFIX + key, next).apply()
            state.copy(done = all)
        }
    }

    private fun readDone(): Map<String, Set<String>> =
        prefs.all.entries
            .filter { it.key.startsWith(KEY_DONE_PREFIX) }
            .mapNotNull { entry ->
                @Suppress("UNCHECKED_CAST")
                val set = (entry.value as? Set<String>)?.toSet() ?: return@mapNotNull null
                if (set.isEmpty()) null else entry.key.removePrefix(KEY_DONE_PREFIX) to set
            }
            .toMap()

    private companion object {
        const val PREFS = "neb_syllabus"
        const val KEY_GRADE = "grade"
        const val KEY_LAST = "last"
        const val KEY_DONE_PREFIX = "done:"
    }
}
