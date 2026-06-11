package com.consica.code.ui.onboarding

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.consica.code.R
import com.consica.code.core.design.Dimens
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.ExperienceLevel
import com.consica.code.core.model.GuidanceLevel
import com.consica.code.core.model.Interest
import com.consica.code.core.model.LearningGoal
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.ui.components.EcoButton
import com.consica.code.ui.components.EcoOutlinedButton
import com.consica.code.ui.components.SelectableCard
import com.consica.code.ui.mascot.Terra
import com.consica.code.ui.mascot.TerraExpression

/** Final onboarding selections handed back to the host for persistence. */
data class OnboardingResult(
    val ageGroup: AgeGroup,
    val goal: LearningGoal,
    val experience: ExperienceLevel,
    val intensity: ThemeIntensity,
    val interests: Set<Interest>,
    val guidance: GuidanceLevel,
)

private enum class Step { Welcome, Age, Goal, Experience, Intensity, Interests, Finish }

@Composable
fun OnboardingScreen(onFinish: (OnboardingResult) -> Unit) {
    var step by remember { mutableStateOf(Step.Welcome) }
    var age by remember { mutableStateOf(AgeGroup.KIDS) }
    var goal by remember { mutableStateOf(LearningGoal.BASICS) }
    var experience by remember { mutableStateOf(ExperienceLevel.NONE) }
    var intensity by remember { mutableStateOf(ThemeIntensity.BALANCED) }
    var interests by remember { mutableStateOf(setOf<Interest>()) }

    val steps = Step.entries
    val index = steps.indexOf(step)

    fun goNext() {
        val nextIndex = index + 1
        if (nextIndex < steps.size) step = steps[nextIndex]
    }
    fun goBack() {
        if (index > 0) step = steps[index - 1]
    }
    fun complete() {
        val guidance = when (age) {
            AgeGroup.KIDS -> GuidanceLevel.FULL
            AgeGroup.TWEENS -> GuidanceLevel.SOME
            AgeGroup.TEENS_PLUS -> GuidanceLevel.MINIMAL
        }
        // Beginner experience nudges toward fuller guidance regardless of age.
        val finalGuidance = if (experience == ExperienceLevel.NONE && guidance == GuidanceLevel.MINIMAL)
            GuidanceLevel.SOME else guidance
        onFinish(OnboardingResult(age, goal, experience, intensity, interests, finalGuidance))
    }

    Scaffold { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = Dimens.screenPadding),
        ) {
            // Progress (hidden on welcome).
            if (step != Step.Welcome) {
                Spacer(Modifier.height(Dimens.md))
                LinearProgressIndicator(
                    progress = { (index).toFloat() / (steps.size - 1) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp),
                    trackColor = MaterialTheme.colorScheme.surfaceVariant,
                )
            }

            Box(Modifier.weight(1f)) {
                AnimatedContent(
                    targetState = step,
                    transitionSpec = { fadeIn() togetherWith fadeOut() },
                    label = "onboarding-step",
                ) { current ->
                    Column(
                        Modifier
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                            .padding(vertical = Dimens.lg),
                    ) {
                        when (current) {
                            Step.Welcome -> WelcomeStep()
                            Step.Age -> AgeStep(age) { age = it }
                            Step.Goal -> GoalStep(goal) { goal = it }
                            Step.Experience -> ExperienceStep(experience) { experience = it }
                            Step.Intensity -> IntensityStep(intensity) { intensity = it }
                            Step.Interests -> InterestsStep(interests) { interests = it }
                            Step.Finish -> FinishStep()
                        }
                    }
                }
            }

            // Footer navigation.
            Row(
                Modifier
                    .fillMaxWidth()
                    .padding(vertical = Dimens.lg),
                horizontalArrangement = Arrangement.spacedBy(Dimens.md),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                if (step != Step.Welcome) {
                    EcoOutlinedButton(
                        text = stringResource(R.string.action_back),
                        onClick = ::goBack,
                    )
                }
                Spacer(Modifier.weight(1f))
                when (step) {
                    Step.Welcome -> EcoButton(
                        text = stringResource(R.string.action_start),
                        onClick = ::goNext,
                    )
                    Step.Finish -> EcoButton(
                        text = stringResource(R.string.onboarding_finish_cta),
                        onClick = ::complete,
                    )
                    Step.Interests -> EcoButton(
                        text = stringResource(R.string.action_continue),
                        onClick = ::goNext,
                    )
                    else -> EcoButton(
                        text = stringResource(R.string.action_next),
                        onClick = ::goNext,
                    )
                }
            }
        }
    }
}

@Composable
private fun StepHeader(title: String, body: String) {
    Text(title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
    Spacer(Modifier.height(Dimens.sm))
    Text(
        body,
        style = MaterialTheme.typography.bodyLarge,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
    Spacer(Modifier.height(Dimens.xl))
}

@Composable
private fun WelcomeStep() {
    Column(
        Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(Modifier.height(Dimens.xxl))
        Terra(expression = TerraExpression.Happy, size = 140.dp)
        Spacer(Modifier.height(Dimens.xl))
        Text(
            stringResource(R.string.onboarding_welcome_title),
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
        )
        Spacer(Modifier.height(Dimens.md))
        Text(
            stringResource(R.string.onboarding_welcome_body),
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )
    }
}

@Composable
private fun AgeStep(selected: AgeGroup, onSelect: (AgeGroup) -> Unit) {
    StepHeader(
        stringResource(R.string.onboarding_age_title),
        stringResource(R.string.onboarding_age_body),
    )
    val options = listOf(
        Triple(AgeGroup.KIDS, R.string.onboarding_age_8_12, R.string.onboarding_age_8_12_desc),
        Triple(AgeGroup.TWEENS, R.string.onboarding_age_13_16, R.string.onboarding_age_13_16_desc),
        Triple(AgeGroup.TEENS_PLUS, R.string.onboarding_age_16_plus, R.string.onboarding_age_16_plus_desc),
    )
    Column(verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
        options.forEach { (value, titleRes, descRes) ->
            SelectableCard(
                title = stringResource(titleRes),
                description = stringResource(descRes),
                selected = selected == value,
                onClick = { onSelect(value) },
            )
        }
    }
}

@Composable
private fun GoalStep(selected: LearningGoal, onSelect: (LearningGoal) -> Unit) {
    StepHeader(
        stringResource(R.string.onboarding_goal_title),
        stringResource(R.string.onboarding_goal_body),
    )
    val options = listOf(
        LearningGoal.BASICS to R.string.goal_learn_basics,
        LearningGoal.WEBSITES to R.string.goal_build_websites,
        LearningGoal.GAMES to R.string.goal_build_games,
        LearningGoal.PUZZLES to R.string.goal_solve_puzzles,
        LearningGoal.EXPLORE to R.string.goal_explore,
    )
    Column(verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
        options.forEach { (value, titleRes) ->
            SelectableCard(
                title = stringResource(titleRes),
                selected = selected == value,
                onClick = { onSelect(value) },
            )
        }
    }
}

@Composable
private fun ExperienceStep(selected: ExperienceLevel, onSelect: (ExperienceLevel) -> Unit) {
    StepHeader(
        stringResource(R.string.onboarding_experience_title),
        stringResource(R.string.onboarding_experience_body),
    )
    val options = listOf(
        ExperienceLevel.NONE to R.string.experience_none,
        ExperienceLevel.SOME to R.string.experience_some,
        ExperienceLevel.LOTS to R.string.experience_lots,
    )
    Column(verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
        options.forEach { (value, titleRes) ->
            SelectableCard(
                title = stringResource(titleRes),
                selected = selected == value,
                onClick = { onSelect(value) },
            )
        }
    }
}

@Composable
private fun IntensityStep(selected: ThemeIntensity, onSelect: (ThemeIntensity) -> Unit) {
    StepHeader(
        stringResource(R.string.onboarding_intensity_title),
        stringResource(R.string.onboarding_intensity_body),
    )
    val options = listOf(
        Triple(ThemeIntensity.PLAYFUL, R.string.intensity_playful, R.string.intensity_playful_desc),
        Triple(ThemeIntensity.BALANCED, R.string.intensity_balanced, R.string.intensity_balanced_desc),
        Triple(ThemeIntensity.FOCUSED, R.string.intensity_focused, R.string.intensity_focused_desc),
    )
    Column(verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
        options.forEach { (value, titleRes, descRes) ->
            SelectableCard(
                title = stringResource(titleRes),
                description = stringResource(descRes),
                selected = selected == value,
                onClick = { onSelect(value) },
            )
        }
    }
}

@Composable
private fun InterestsStep(selected: Set<Interest>, onToggle: (Set<Interest>) -> Unit) {
    StepHeader(
        stringResource(R.string.onboarding_interests_title),
        stringResource(R.string.onboarding_interests_body),
    )
    val options = listOf(
        Interest.PYTHON to R.string.interest_python,
        Interest.WEB to R.string.interest_web,
        Interest.GAMES to R.string.interest_games,
        Interest.APPS to R.string.interest_apps,
        Interest.AI to R.string.interest_ai,
        Interest.CREATIVE to R.string.interest_creative,
    )
    Column(verticalArrangement = Arrangement.spacedBy(Dimens.md)) {
        options.forEach { (value, titleRes) ->
            SelectableCard(
                title = stringResource(titleRes),
                selected = value in selected,
                onClick = {
                    onToggle(if (value in selected) selected - value else selected + value)
                },
            )
        }
    }
}

@Composable
private fun FinishStep() {
    Column(
        Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(Modifier.height(Dimens.xl))
        Terra(expression = TerraExpression.Proud, size = 140.dp)
        Spacer(Modifier.height(Dimens.xl))
        Text(
            stringResource(R.string.onboarding_finish_title),
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
        )
        Spacer(Modifier.height(Dimens.md))
        Text(
            stringResource(R.string.onboarding_finish_body),
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )
    }
}
