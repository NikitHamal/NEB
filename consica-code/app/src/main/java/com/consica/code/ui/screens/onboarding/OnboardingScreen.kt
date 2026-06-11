package com.consica.code.ui.screens.onboarding

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.CardShape
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.CodingInterest
import com.consica.code.core.model.ExperienceLevel
import com.consica.code.core.model.LearningGoal
import com.consica.code.core.model.TerraExpression
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.common.appViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

enum class OnboardingStep { WELCOME, AGE, GOAL, EXPERIENCE, THEME, INTERESTS, READY }

data class OnboardingState(
    val step: OnboardingStep = OnboardingStep.WELCOME,
    val ageGroup: AgeGroup? = null,
    val goal: LearningGoal? = null,
    val experience: ExperienceLevel? = null,
    val themeIntensity: ThemeIntensity? = null,
    val interests: Set<CodingInterest> = emptySet(),
    val saving: Boolean = false,
)

class OnboardingViewModel(private val container: AppContainer) : ViewModel() {

    private val _state = MutableStateFlow(OnboardingState())
    val state: StateFlow<OnboardingState> = _state

    fun next() {
        val current = _state.value.step
        val ordinal = current.ordinal
        if (ordinal < OnboardingStep.entries.lastIndex) {
            _state.value = _state.value.copy(step = OnboardingStep.entries[ordinal + 1])
        }
    }

    fun back() {
        val ordinal = _state.value.step.ordinal
        if (ordinal > 0) _state.value = _state.value.copy(step = OnboardingStep.entries[ordinal - 1])
    }

    fun setAge(value: AgeGroup) {
        _state.value = _state.value.copy(ageGroup = value)
    }

    fun setGoal(value: LearningGoal) {
        _state.value = _state.value.copy(goal = value)
    }

    fun setExperience(value: ExperienceLevel) {
        _state.value = _state.value.copy(experience = value)
    }

    fun setTheme(value: ThemeIntensity) {
        _state.value = _state.value.copy(themeIntensity = value)
    }

    fun toggleInterest(value: CodingInterest) {
        val current = _state.value.interests
        _state.value = _state.value.copy(
            interests = if (value in current) current - value else current + value,
        )
    }

    fun finish(onDone: () -> Unit) {
        val s = _state.value
        if (s.saving) return
        _state.value = s.copy(saving = true)
        viewModelScope.launch {
            container.prefs.completeOnboarding(
                ageGroup = s.ageGroup ?: AgeGroup.TEENS,
                goal = s.goal ?: LearningGoal.FOR_FUN,
                experience = s.experience ?: ExperienceLevel.BRAND_NEW,
                themeIntensity = s.themeIntensity ?: ThemeIntensity.BALANCED,
                interests = s.interests,
            )
            onDone()
        }
    }
}

@Composable
fun OnboardingScreen(onFinished: () -> Unit) {
    val viewModel = appViewModel { OnboardingViewModel(it) }
    val state by viewModel.state.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Box(Modifier.height(24.dp))
        StepDots(current = state.step.ordinal, total = OnboardingStep.entries.size)
        Box(Modifier.height(8.dp))

        AnimatedContent(targetState = state.step, label = "onboardingStep") { step ->
            when (step) {
                OnboardingStep.WELCOME -> WelcomePage(onNext = viewModel::next)
                OnboardingStep.AGE -> AgePage(state, viewModel)
                OnboardingStep.GOAL -> GoalPage(state, viewModel)
                OnboardingStep.EXPERIENCE -> ExperiencePage(state, viewModel)
                OnboardingStep.THEME -> ThemePage(state, viewModel)
                OnboardingStep.INTERESTS -> InterestsPage(state, viewModel)
                OnboardingStep.READY -> ReadyPage(state) { viewModel.finish(onFinished) }
            }
        }
        Box(Modifier.height(32.dp))
    }
}

@Composable
private fun StepDots(current: Int, total: Int) {
    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        repeat(total) { i ->
            Box(
                modifier = Modifier
                    .size(if (i == current) 10.dp else 8.dp)
                    .clip(CircleShape)
                    .background(
                        if (i <= current) MaterialTheme.colorScheme.primary
                        else MaterialTheme.colorScheme.outlineVariant,
                    ),
            )
        }
    }
}

@Composable
private fun WelcomePage(onNext: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(Modifier.height(24.dp))
        TerraAvatar(expression = TerraExpression.EXCITED, size = 140.dp)
        Box(Modifier.height(24.dp))
        Text(
            stringResource(R.string.onboarding_welcome_title),
            style = MaterialTheme.typography.headlineMedium,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
        )
        Box(Modifier.height(12.dp))
        Text(
            stringResource(R.string.onboarding_welcome_body),
            style = MaterialTheme.typography.bodyLarge,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Box(Modifier.height(32.dp))
        Button(
            onClick = onNext,
            shape = PillShape,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.onboarding_lets_go), style = MaterialTheme.typography.labelLarge)
        }
    }
}

@Composable
private fun ChoiceCard(
    title: String,
    description: String?,
    selected: Boolean,
    onClick: () -> Unit,
) {
    Card(
        onClick = onClick,
        shape = CardShape,
        colors = CardDefaults.cardColors(
            containerColor = if (selected) MaterialTheme.colorScheme.primaryContainer
            else MaterialTheme.colorScheme.surface,
        ),
        border = BorderStroke(
            width = if (selected) 2.dp else 1.dp,
            color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant,
        ),
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
    ) {
        Column(Modifier.padding(20.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            if (description != null) {
                Text(
                    description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun PageScaffold(
    title: String,
    subtitle: String,
    nextEnabled: Boolean,
    onNext: () -> Unit,
    onBack: () -> Unit,
    content: @Composable () -> Unit,
) {
    Column {
        Box(Modifier.height(16.dp))
        Text(title, style = MaterialTheme.typography.headlineSmall)
        Box(Modifier.height(4.dp))
        Text(
            subtitle,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Box(Modifier.height(16.dp))
        content()
        Box(Modifier.height(24.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            TextButton(onClick = onBack) {
                Text(stringResource(R.string.action_back))
            }
            Box(Modifier.weight(1f))
            Button(
                onClick = onNext,
                enabled = nextEnabled,
                shape = PillShape,
                modifier = Modifier.height(52.dp),
            ) {
                Text(stringResource(R.string.action_next), style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}

@Composable
private fun AgePage(state: OnboardingState, viewModel: OnboardingViewModel) {
    PageScaffold(
        title = stringResource(R.string.onboarding_age_title),
        subtitle = stringResource(R.string.onboarding_age_subtitle),
        nextEnabled = state.ageGroup != null,
        onNext = viewModel::next,
        onBack = viewModel::back,
    ) {
        ChoiceCard(
            stringResource(R.string.onboarding_age_kids),
            stringResource(R.string.onboarding_age_kids_desc),
            state.ageGroup == AgeGroup.KIDS,
        ) { viewModel.setAge(AgeGroup.KIDS) }
        ChoiceCard(
            stringResource(R.string.onboarding_age_teens),
            stringResource(R.string.onboarding_age_teens_desc),
            state.ageGroup == AgeGroup.TEENS,
        ) { viewModel.setAge(AgeGroup.TEENS) }
        ChoiceCard(
            stringResource(R.string.onboarding_age_pro),
            stringResource(R.string.onboarding_age_pro_desc),
            state.ageGroup == AgeGroup.PRO,
        ) { viewModel.setAge(AgeGroup.PRO) }
    }
}

@Composable
private fun GoalPage(state: OnboardingState, viewModel: OnboardingViewModel) {
    PageScaffold(
        title = stringResource(R.string.onboarding_goal_title),
        subtitle = stringResource(R.string.onboarding_goal_subtitle),
        nextEnabled = state.goal != null,
        onNext = viewModel::next,
        onBack = viewModel::back,
    ) {
        ChoiceCard(stringResource(R.string.onboarding_goal_fun), null, state.goal == LearningGoal.FOR_FUN) {
            viewModel.setGoal(LearningGoal.FOR_FUN)
        }
        ChoiceCard(stringResource(R.string.onboarding_goal_school), null, state.goal == LearningGoal.SCHOOL) {
            viewModel.setGoal(LearningGoal.SCHOOL)
        }
        ChoiceCard(stringResource(R.string.onboarding_goal_career), null, state.goal == LearningGoal.FUTURE_CAREER) {
            viewModel.setGoal(LearningGoal.FUTURE_CAREER)
        }
        ChoiceCard(stringResource(R.string.onboarding_goal_build), null, state.goal == LearningGoal.BUILD_THINGS) {
            viewModel.setGoal(LearningGoal.BUILD_THINGS)
        }
    }
}

@Composable
private fun ExperiencePage(state: OnboardingState, viewModel: OnboardingViewModel) {
    PageScaffold(
        title = stringResource(R.string.onboarding_experience_title),
        subtitle = stringResource(R.string.onboarding_experience_subtitle),
        nextEnabled = state.experience != null,
        onNext = viewModel::next,
        onBack = viewModel::back,
    ) {
        ChoiceCard(
            stringResource(R.string.onboarding_exp_new),
            stringResource(R.string.onboarding_exp_new_desc),
            state.experience == ExperienceLevel.BRAND_NEW,
        ) { viewModel.setExperience(ExperienceLevel.BRAND_NEW) }
        ChoiceCard(
            stringResource(R.string.onboarding_exp_some),
            stringResource(R.string.onboarding_exp_some_desc),
            state.experience == ExperienceLevel.SOME_BASICS,
        ) { viewModel.setExperience(ExperienceLevel.SOME_BASICS) }
        ChoiceCard(
            stringResource(R.string.onboarding_exp_confident),
            stringResource(R.string.onboarding_exp_confident_desc),
            state.experience == ExperienceLevel.CONFIDENT,
        ) { viewModel.setExperience(ExperienceLevel.CONFIDENT) }
    }
}

@Composable
private fun ThemePage(state: OnboardingState, viewModel: OnboardingViewModel) {
    PageScaffold(
        title = stringResource(R.string.onboarding_theme_title),
        subtitle = stringResource(R.string.onboarding_theme_subtitle),
        nextEnabled = state.themeIntensity != null,
        onNext = viewModel::next,
        onBack = viewModel::back,
    ) {
        ChoiceCard(
            stringResource(R.string.onboarding_theme_playful),
            stringResource(R.string.onboarding_theme_playful_desc),
            state.themeIntensity == ThemeIntensity.PLAYFUL,
        ) { viewModel.setTheme(ThemeIntensity.PLAYFUL) }
        ChoiceCard(
            stringResource(R.string.onboarding_theme_balanced),
            stringResource(R.string.onboarding_theme_balanced_desc),
            state.themeIntensity == ThemeIntensity.BALANCED,
        ) { viewModel.setTheme(ThemeIntensity.BALANCED) }
        ChoiceCard(
            stringResource(R.string.onboarding_theme_focused),
            stringResource(R.string.onboarding_theme_focused_desc),
            state.themeIntensity == ThemeIntensity.FOCUSED,
        ) { viewModel.setTheme(ThemeIntensity.FOCUSED) }
    }
}

@Composable
private fun InterestsPage(state: OnboardingState, viewModel: OnboardingViewModel) {
    PageScaffold(
        title = stringResource(R.string.onboarding_interests_title),
        subtitle = stringResource(R.string.onboarding_interests_subtitle),
        nextEnabled = true,
        onNext = viewModel::next,
        onBack = viewModel::back,
    ) {
        val labels = mapOf(
            CodingInterest.PYTHON to R.string.interest_python,
            CodingInterest.WEB to R.string.interest_web,
            CodingInterest.GAMES to R.string.interest_games,
            CodingInterest.APPS to R.string.interest_apps,
            CodingInterest.AI_BASICS to R.string.interest_ai,
            CodingInterest.CREATIVE to R.string.interest_creative,
        )
        Column {
            labels.entries.chunked(2).forEach { rowItems ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    rowItems.forEach { (interest, labelRes) ->
                        FilterChip(
                            selected = interest in state.interests,
                            onClick = { viewModel.toggleInterest(interest) },
                            label = { Text(stringResource(labelRes)) },
                            shape = PillShape,
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                            ),
                            modifier = Modifier.weight(1f),
                        )
                    }
                    if (rowItems.size == 1) Box(Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun ReadyPage(state: OnboardingState, onEnter: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(Modifier.height(16.dp))
        TerraAvatar(expression = TerraExpression.PROUD, size = 120.dp)
        Box(Modifier.height(20.dp))
        Text(
            stringResource(R.string.onboarding_ready_title),
            style = MaterialTheme.typography.headlineMedium,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
        )
        Box(Modifier.height(12.dp))
        val bodyRes = when (state.ageGroup) {
            AgeGroup.KIDS -> R.string.onboarding_ready_body_kids
            AgeGroup.PRO -> R.string.onboarding_ready_body_pro
            else -> R.string.onboarding_ready_body_teens
        }
        Text(
            stringResource(bodyRes),
            style = MaterialTheme.typography.bodyLarge,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Box(Modifier.height(28.dp))
        Button(
            onClick = onEnter,
            enabled = !state.saving,
            shape = PillShape,
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
        ) {
            Text(stringResource(R.string.onboarding_enter_app), style = MaterialTheme.typography.labelLarge)
        }
    }
}
