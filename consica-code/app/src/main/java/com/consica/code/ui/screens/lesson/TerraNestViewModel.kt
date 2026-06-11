package com.consica.code.ui.screens.lesson

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.Lesson
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class TerraNestState(
    val lesson: Lesson? = null,
    val stepIndex: Int = 0,
    val ageGroup: AgeGroup = AgeGroup.KIDS,
)

@HiltViewModel
class TerraNestViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val prefs: UserPreferencesRepository,
    private val progressRepository: ProgressRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        TerraNestState(lesson = LessonCatalog.byId(savedStateHandle.get<String>("lessonId").orEmpty()))
    )
    val uiState: StateFlow<TerraNestState> = _uiState

    init {
        viewModelScope.launch {
            prefs.profile.collect { profile ->
                _uiState.update { it.copy(ageGroup = profile.ageGroup) }
            }
        }
    }

    fun nextStep() = _uiState.update {
        val max = (it.lesson?.steps?.size ?: 1) - 1
        it.copy(stepIndex = (it.stepIndex + 1).coerceAtMost(max))
    }

    /** Tutorial-only lessons complete directly from the dialogue flow. */
    fun completeTutorial(onDone: () -> Unit) {
        val lesson = _uiState.value.lesson ?: return onDone()
        viewModelScope.launch {
            progressRepository.completeLesson(lesson)
            progressRepository.recordDailyActivity()
            onDone()
        }
    }
}
