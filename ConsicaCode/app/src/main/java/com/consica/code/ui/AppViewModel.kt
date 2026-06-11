package com.consica.code.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.consica.code.core.di.AppContainer
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.data.local.BadgeEntity
import com.consica.code.data.local.EcosystemItemEntity
import com.consica.code.data.local.LessonProgressEntity
import com.consica.code.data.local.WorkspaceEntity
import com.consica.code.data.prefs.DarkMode
import com.consica.code.data.prefs.UserPrefs
import com.consica.code.data.repository.CompletionResult
import com.consica.code.domain.content.CodeLang
import com.consica.code.domain.content.Lesson
import com.consica.code.domain.content.LessonCheck
import com.consica.code.domain.runner.RunResult
import com.consica.code.ui.onboarding.OnboardingResult
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

/**
 * Single app-scoped ViewModel that exposes all offline state as StateFlows and funnels user
 * actions to the repositories. Keeping one VM avoids prop-drilling repositories through the nav
 * graph and keeps composables declarative.
 */
class AppViewModel(private val container: AppContainer) : ViewModel() {

    private val game = container.gameRepository
    private val workspaces = container.workspaceRepository
    private val settings = container.settings
    private val python = container.pythonRunner

    val prefs: StateFlow<UserPrefs> =
        game.prefs.stateIn(viewModelScope, SharingStarted.Eagerly, UserPrefs())

    val completedLessonIds: StateFlow<Set<String>> =
        game.completedLessonIds.stateIn(viewModelScope, SharingStarted.Eagerly, emptySet())

    val lessonProgress: StateFlow<List<LessonProgressEntity>> =
        game.lessonProgress.stateIn(viewModelScope, SharingStarted.Eagerly, emptyList())

    val completedCount: StateFlow<Int> =
        game.completedCount.stateIn(viewModelScope, SharingStarted.Eagerly, 0)

    val badges: StateFlow<List<BadgeEntity>> =
        game.badges.stateIn(viewModelScope, SharingStarted.Eagerly, emptyList())

    val ecosystem: StateFlow<List<EcosystemItemEntity>> =
        game.ecosystem.stateIn(viewModelScope, SharingStarted.Eagerly, emptyList())

    val ecosystemCount: StateFlow<Int> =
        game.ecosystemCount.stateIn(viewModelScope, SharingStarted.Eagerly, 0)

    val recentWorkspaces: StateFlow<List<WorkspaceEntity>> =
        workspaces.recent(8).stateIn(viewModelScope, SharingStarted.Eagerly, emptyList())

    // ---- Onboarding & settings ----

    fun completeOnboarding(result: OnboardingResult) = launch {
        settings.completeOnboarding(
            age = result.ageGroup,
            goal = result.goal,
            experience = result.experience,
            intensity = result.intensity,
            interests = result.interests,
            guidance = result.guidance,
        )
    }

    fun setHighContrast(on: Boolean) = launch { settings.setHighContrast(on) }
    fun setReducedMotion(on: Boolean) = launch { settings.setReducedMotion(on) }
    fun setSound(on: Boolean) = launch { settings.setSound(on) }
    fun setFontScale(scale: Float) = launch { settings.setFontScale(scale) }
    fun setDarkMode(mode: DarkMode) = launch { settings.setDarkMode(mode) }
    fun setAgeGroup(age: AgeGroup) = launch { settings.setAgeGroup(age) }
    fun setIntensity(intensity: ThemeIntensity) = launch { settings.setIntensity(intensity) }
    fun setGuidance(level: GuidanceLevel) = launch { settings.setGuidance(level) }
    fun unlockPro() = launch { game.unlockPro() }
    fun resetProgress() = launch { game.resetAll() }

    // ---- Lessons ----

    fun startLesson(lessonId: String) = launch { game.startLesson(lessonId) }

    /** Run code for a lesson/playground. HTML is "rendered" by the WebView, so we just echo it. */
    fun runCode(lang: CodeLang?, code: String): RunResult = when (lang) {
        CodeLang.PYTHON -> python.run(code)
        else -> RunResult.ok(code) // HTML preview handled by the UI WebView
    }

    fun evaluate(lesson: Lesson, code: String, result: RunResult): Boolean =
        result.success && LessonCheck.passes(lesson, code, result.output)

    fun recordAttempt(lesson: Lesson, code: String, result: RunResult) =
        launch { game.recordAttempt(lesson, code, result) }

    /** Completes a lesson and returns the celebration payload via [onResult] on the main scope. */
    fun completeLesson(lesson: Lesson, code: String, onResult: (CompletionResult) -> Unit) = launch {
        val r = game.completeLesson(lesson, code)
        onResult(r)
    }

    fun touchStreak() = launch { game.touchDailyStreak() }

    // ---- Workspaces ----

    fun saveWorkspace(name: String, lang: CodeLang, content: String, lessonId: String? = null) =
        launch { workspaces.save(name, lang.id, content, lessonId) }

    fun deleteWorkspace(id: Long) = launch { workspaces.delete(id) }

    private fun launch(block: suspend () -> Unit) {
        viewModelScope.launch { block() }
    }

    class Factory(private val container: AppContainer) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T =
            AppViewModel(container) as T
    }
}
