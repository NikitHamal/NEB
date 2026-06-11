package com.consica.code.ui.screens.puzzle

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.CompletionRewards
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.Lesson
import com.consica.code.domain.model.PuzzleBlock
import com.consica.code.util.AppSound
import com.consica.code.util.SoundManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject
import kotlin.random.Random

data class PuzzleUiState(
    val lesson: Lesson? = null,
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val pool: List<PuzzleBlock> = emptyList(),
    val answer: List<PuzzleBlock> = emptyList(),
    val checked: Boolean = false,
    val correct: Boolean = false,
    val showHint: Boolean = false,
    val celebration: CompletionRewards? = null,
)

@HiltViewModel
class PuzzleViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    prefs: UserPreferencesRepository,
    private val progressRepository: ProgressRepository,
    private val soundManager: SoundManager,
) : ViewModel() {

    private val lesson: Lesson? =
        savedStateHandle.get<String>("lessonId")?.let { LessonCatalog.byId(it) }

    private val _uiState = MutableStateFlow(initialState())
    val uiState: StateFlow<PuzzleUiState> = _uiState

    init {
        viewModelScope.launch {
            prefs.profile.collect { profile ->
                _uiState.update { it.copy(ageGroup = profile.ageGroup) }
            }
        }
    }

    private fun initialState(): PuzzleUiState {
        val puzzle = lesson?.puzzle ?: return PuzzleUiState(lesson = lesson)
        val shuffled = (puzzle.blocks + puzzle.distractors)
            .shuffled(Random(lesson.id.hashCode()))
        return PuzzleUiState(lesson = lesson, pool = shuffled)
    }

    fun pickFromPool(index: Int) {
        soundManager.play(AppSound.TAP)
        _uiState.update { state ->
            val block = state.pool.getOrNull(index) ?: return@update state
            state.copy(
                pool = state.pool.toMutableList().also { it.removeAt(index) },
                answer = state.answer + block,
                checked = false,
            )
        }
    }

    fun returnToPool(index: Int) {
        soundManager.play(AppSound.TAP)
        _uiState.update { state ->
            val block = state.answer.getOrNull(index) ?: return@update state
            state.copy(
                answer = state.answer.toMutableList().also { it.removeAt(index) },
                pool = state.pool + block,
                checked = false,
            )
        }
    }

    fun moveAnswer(index: Int, delta: Int) {
        _uiState.update { state ->
            val target = index + delta
            if (index !in state.answer.indices || target !in state.answer.indices) return@update state
            val list = state.answer.toMutableList()
            val item = list.removeAt(index)
            list.add(target, item)
            state.copy(answer = list, checked = false)
        }
    }

    fun toggleHint() = _uiState.update { it.copy(showHint = !it.showHint) }

    fun check() {
        val lesson = this.lesson ?: return
        val puzzle = lesson.puzzle ?: return
        val correct = _uiState.value.answer.map { it.code } == puzzle.blocks.map { it.code }

        viewModelScope.launch {
            progressRepository.recordAttempt(
                lesson = lesson,
                workspaceId = null,
                language = puzzle.language.name,
                code = _uiState.value.answer.joinToString("\n") { it.code },
                output = "",
                success = correct,
            )
            var celebration: CompletionRewards? = null
            if (correct) {
                soundManager.play(AppSound.REWARD)
                celebration = progressRepository.completeLesson(lesson)
                progressRepository.recordDailyActivity()
            } else {
                soundManager.play(AppSound.GENTLE_ERROR)
            }
            _uiState.update {
                it.copy(checked = true, correct = correct, celebration = celebration)
            }
        }
    }

    fun dismissCelebration() = _uiState.update { it.copy(celebration = null) }
}
