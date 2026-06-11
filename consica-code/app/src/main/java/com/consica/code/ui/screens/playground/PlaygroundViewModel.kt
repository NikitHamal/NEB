package com.consica.code.ui.screens.playground

import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.TextFieldValue
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.CompletionRewards
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.execution.ChallengeValidator
import com.consica.code.domain.execution.ExecutionError
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.GuidanceLevel
import com.consica.code.domain.model.Lesson
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

data class PlaygroundUiState(
    val lesson: Lesson? = null,
    val language: TrackLanguage = TrackLanguage.PYTHON,
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val guidanceLevel: GuidanceLevel = GuidanceLevel.FULL,
    val proEditor: Boolean = false,
    val running: Boolean = false,
    val hasRun: Boolean = false,
    val output: String = "",
    val error: ExecutionError? = null,
    val challengePassed: Boolean = false,
    val showHint: Boolean = false,
    val celebration: CompletionRewards? = null,
) {
    val isLessonMode: Boolean get() = lesson?.challenge != null
}

@HiltViewModel
class PlaygroundViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    prefs: UserPreferencesRepository,
    private val progressRepository: ProgressRepository,
    private val soundManager: SoundManager,
) : ViewModel() {

    private val lesson: Lesson? =
        savedStateHandle.get<String>("lessonId")?.let { LessonCatalog.byId(it) }

    private val language: TrackLanguage = lesson?.challenge?.language
        ?: lesson?.language
        ?: savedStateHandle.get<String>("language")
            ?.let { name -> TrackLanguage.entries.find { it.name == name } }
        ?: TrackLanguage.PYTHON

    private val _uiState = MutableStateFlow(PlaygroundUiState(lesson = lesson, language = language))
    val uiState: StateFlow<PlaygroundUiState> = _uiState

    private val _code = MutableStateFlow(TextFieldValue(initialCode()))
    val code: StateFlow<TextFieldValue> = _code

    init {
        viewModelScope.launch {
            prefs.profile.collect { profile ->
                _uiState.update { it.copy(ageGroup = profile.ageGroup) }
            }
        }
        viewModelScope.launch {
            kotlinx.coroutines.flow.combine(prefs.settings, prefs.stats) { settings, stats ->
                settings.guidanceLevel to (settings.professionalModeEnabled && stats.professionalModeUnlocked)
            }.collect { (guidance, pro) ->
                _uiState.update { it.copy(guidanceLevel = guidance, proEditor = pro) }
            }
        }
    }

    private fun initialCode(): String =
        lesson?.challenge?.starterCode ?: when (language) {
            TrackLanguage.HTML -> "<h1>Hello, forest!</h1>\n"
            else -> "print(\"Hello, forest!\")\n"
        }

    fun onCodeChange(value: TextFieldValue) {
        _code.value = value
    }

    fun onCodeKey(key: CodeKey) {
        soundManager.play(AppSound.TAP)
        val current = _code.value
        val (newText, cursor) = applyCodeKey(current.text, current.selection.start, key)
        _code.value = TextFieldValue(newText, TextRange(cursor))
    }

    fun resetCode() {
        _code.value = TextFieldValue(initialCode())
        _uiState.update {
            it.copy(output = "", error = null, hasRun = false, challengePassed = false)
        }
    }

    fun toggleHint() = _uiState.update { it.copy(showHint = !it.showHint) }

    fun run() {
        if (_uiState.value.running) return
        soundManager.play(AppSound.GROW)
        _uiState.update { it.copy(running = true) }
        val codeText = _code.value.text

        viewModelScope.launch {
            val (output, error) = withContext(Dispatchers.Default) {
                when (language) {
                    TrackLanguage.HTML -> codeText to null
                    else -> {
                        val result = PythonInterpreter().run(
                            code = codeText,
                            stdin = lesson?.challenge?.stdin ?: emptyList(),
                        )
                        result.output to result.error
                    }
                }
            }

            val challenge = lesson?.challenge
            val passed = error == null && challenge != null &&
                ChallengeValidator.validate(challenge.validation, codeText, output)

            progressRepository.recordAttempt(
                lesson = lesson,
                workspaceId = null,
                language = language.name,
                code = codeText,
                output = output,
                success = error == null && (challenge == null || passed),
            )

            var celebration: CompletionRewards? = null
            if (passed && lesson != null) {
                celebration = progressRepository.completeLesson(lesson)
                progressRepository.recordDailyActivity()
            }

            when {
                error != null -> soundManager.play(AppSound.GENTLE_ERROR)
                passed -> soundManager.play(AppSound.REWARD)
                else -> if (challenge == null) soundManager.play(AppSound.SUCCESS)
            }

            _uiState.update {
                it.copy(
                    running = false,
                    hasRun = true,
                    output = output,
                    error = error,
                    challengePassed = passed,
                    celebration = celebration ?: it.celebration,
                )
            }
        }
    }

    fun dismissCelebration() = _uiState.update { it.copy(celebration = null) }
}
