package com.consica.code.ui.screens.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.CodingInterest
import com.consica.code.domain.model.ExperienceLevel
import com.consica.code.domain.model.LearningGoal
import com.consica.code.domain.model.OnboardingProfile
import com.consica.code.domain.model.ThemeIntensity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class OnboardingState(
    val step: Int = 0,
    val ageGroup: AgeGroup? = null,
    val goal: LearningGoal? = null,
    val experience: ExperienceLevel? = null,
    val themeIntensity: ThemeIntensity? = null,
    val interests: Set<CodingInterest> = emptySet(),
    val displayName: String = "",
)

@HiltViewModel
class OnboardingViewModel @Inject constructor(
    private val prefs: UserPreferencesRepository,
) : ViewModel() {

    companion object {
        const val STEP_COUNT = 7
    }

    private val _state = MutableStateFlow(OnboardingState())
    val state: StateFlow<OnboardingState> = _state

    fun setAgeGroup(value: AgeGroup) = _state.update { it.copy(ageGroup = value) }
    fun setGoal(value: LearningGoal) = _state.update { it.copy(goal = value) }
    fun setExperience(value: ExperienceLevel) = _state.update { it.copy(experience = value) }
    fun setThemeIntensity(value: ThemeIntensity) = _state.update { it.copy(themeIntensity = value) }
    fun setDisplayName(value: String) = _state.update { it.copy(displayName = value) }

    fun toggleInterest(interest: CodingInterest) = _state.update {
        it.copy(interests = if (interest in it.interests) it.interests - interest else it.interests + interest)
    }

    fun back() = _state.update { it.copy(step = (it.step - 1).coerceAtLeast(0)) }

    fun next(onDone: () -> Unit) {
        val current = _state.value
        // Selection steps require a choice before advancing.
        val canAdvance = when (current.step) {
            1 -> current.ageGroup != null
            2 -> current.goal != null
            3 -> current.experience != null
            4 -> current.themeIntensity != null
            else -> true
        }
        if (!canAdvance) return

        if (current.step < STEP_COUNT - 1) {
            _state.update { it.copy(step = it.step + 1) }
        } else {
            viewModelScope.launch {
                prefs.completeOnboarding(
                    OnboardingProfile(
                        ageGroup = current.ageGroup ?: AgeGroup.KIDS,
                        goal = current.goal ?: LearningGoal.FUN,
                        experience = current.experience ?: ExperienceLevel.BRAND_NEW,
                        themeIntensity = current.themeIntensity ?: ThemeIntensity.PLAYFUL,
                        interests = current.interests,
                    )
                )
                if (current.displayName.isNotBlank()) {
                    prefs.setDisplayName(current.displayName.trim())
                }
                onDone()
            }
        }
    }
}
