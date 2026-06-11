package com.consica.code.ui.screens.onboarding

import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.consica.code.R
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.CodingInterest
import com.consica.code.domain.model.ExperienceLevel
import com.consica.code.domain.model.LearningGoal
import com.consica.code.domain.model.TerraExpression
import com.consica.code.domain.model.ThemeIntensity
import com.consica.code.ui.character.TerraAvatar
import com.consica.code.ui.components.EcoCard
import com.consica.code.ui.components.PillButton

@Composable
fun OnboardingScreen(
    onDone: () -> Unit,
    viewModel: OnboardingViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsState()

    Scaffold { padding ->
        Column(
            Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 24.dp),
        ) {
            Spacer(Modifier.height(16.dp))
            Text(
                text = stringResource(R.string.onboarding_step_of, state.step + 1, OnboardingViewModel.STEP_COUNT),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(8.dp))
            LinearProgressIndicator(
                progress = { (state.step + 1f) / OnboardingViewModel.STEP_COUNT },
                modifier = Modifier.fillMaxWidth(),
            )
            Spacer(Modifier.height(24.dp))

            AnimatedContent(targetState = state.step, label = "onboardingStep") { step ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .verticalScroll(rememberScrollState()),
                ) {
                    when (step) {
                        0 -> WelcomeStep()
                        1 -> AgeStep(state.ageGroup, viewModel::setAgeGroup)
                        2 -> GoalStep(state.goal, viewModel::setGoal)
                        3 -> ExperienceStep(state.experience, viewModel::setExperience)
                        4 -> ThemeStep(state.themeIntensity, viewModel::setThemeIntensity)
                        5 -> InterestsStep(state.interests, viewModel::toggleInterest)
                        6 -> NameStep(state.displayName, viewModel::setDisplayName)
                    }
                }
            }

            Spacer(Modifier.weight(1f))
            Row(
                Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                if (state.step > 0) {
                    TextButton(onClick = viewModel::back) {
                        Text(stringResource(R.string.onboarding_back))
                    }
                }
                Spacer(Modifier.weight(1f))
                PillButton(
                    text = stringResource(
                        if (state.step == OnboardingViewModel.STEP_COUNT - 1) R.string.onboarding_start
                        else R.string.onboarding_next
                    ),
                    onClick = { viewModel.next(onDone) },
                )
            }
        }
    }
}

@Composable
private fun WelcomeStep() {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
        TerraAvatar(expression = TerraExpression.EXCITED, modifier = Modifier.size(160.dp))
        Spacer(Modifier.height(24.dp))
        Text(
            text = stringResource(R.string.onboarding_welcome_title),
            style = MaterialTheme.typography.headlineMedium,
        )
        Spacer(Modifier.height(12.dp))
        Text(
            text = stringResource(R.string.onboarding_welcome_body),
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun ChoiceCard(
    title: String,
    selected: Boolean,
    description: String? = null,
    onClick: () -> Unit,
) {
    EcoCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
        containerColor = if (selected) MaterialTheme.colorScheme.primaryContainer
        else MaterialTheme.colorScheme.surface,
        onClick = onClick,
    ) {
        Column(Modifier.padding(16.dp)) {
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
private fun AgeStep(selected: AgeGroup?, onSelect: (AgeGroup) -> Unit) {
    Column {
        Text(stringResource(R.string.onboarding_age_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        ChoiceCard(
            stringResource(R.string.onboarding_age_kids), selected == AgeGroup.KIDS,
            stringResource(R.string.onboarding_age_kids_desc),
        ) { onSelect(AgeGroup.KIDS) }
        ChoiceCard(
            stringResource(R.string.onboarding_age_teens), selected == AgeGroup.TEENS,
            stringResource(R.string.onboarding_age_teens_desc),
        ) { onSelect(AgeGroup.TEENS) }
        ChoiceCard(
            stringResource(R.string.onboarding_age_adults), selected == AgeGroup.ADULTS,
            stringResource(R.string.onboarding_age_adults_desc),
        ) { onSelect(AgeGroup.ADULTS) }
    }
}

@Composable
private fun GoalStep(selected: LearningGoal?, onSelect: (LearningGoal) -> Unit) {
    Column {
        Text(stringResource(R.string.onboarding_goal_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        ChoiceCard(stringResource(R.string.onboarding_goal_fun), selected == LearningGoal.FUN) { onSelect(LearningGoal.FUN) }
        ChoiceCard(stringResource(R.string.onboarding_goal_school), selected == LearningGoal.SCHOOL) { onSelect(LearningGoal.SCHOOL) }
        ChoiceCard(stringResource(R.string.onboarding_goal_career), selected == LearningGoal.CAREER) { onSelect(LearningGoal.CAREER) }
        ChoiceCard(stringResource(R.string.onboarding_goal_creative), selected == LearningGoal.CREATIVE) { onSelect(LearningGoal.CREATIVE) }
    }
}

@Composable
private fun ExperienceStep(selected: ExperienceLevel?, onSelect: (ExperienceLevel) -> Unit) {
    Column {
        Text(stringResource(R.string.onboarding_experience_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        ChoiceCard(stringResource(R.string.onboarding_experience_new), selected == ExperienceLevel.BRAND_NEW) { onSelect(ExperienceLevel.BRAND_NEW) }
        ChoiceCard(stringResource(R.string.onboarding_experience_some), selected == ExperienceLevel.SOME_BASICS) { onSelect(ExperienceLevel.SOME_BASICS) }
        ChoiceCard(stringResource(R.string.onboarding_experience_confident), selected == ExperienceLevel.CONFIDENT) { onSelect(ExperienceLevel.CONFIDENT) }
    }
}

@Composable
private fun ThemeStep(selected: ThemeIntensity?, onSelect: (ThemeIntensity) -> Unit) {
    Column {
        Text(stringResource(R.string.onboarding_theme_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        ChoiceCard(
            stringResource(R.string.onboarding_theme_playful), selected == ThemeIntensity.PLAYFUL,
            stringResource(R.string.onboarding_theme_playful_desc),
        ) { onSelect(ThemeIntensity.PLAYFUL) }
        ChoiceCard(
            stringResource(R.string.onboarding_theme_balanced), selected == ThemeIntensity.BALANCED,
            stringResource(R.string.onboarding_theme_balanced_desc),
        ) { onSelect(ThemeIntensity.BALANCED) }
        ChoiceCard(
            stringResource(R.string.onboarding_theme_focused), selected == ThemeIntensity.FOCUSED,
            stringResource(R.string.onboarding_theme_focused_desc),
        ) { onSelect(ThemeIntensity.FOCUSED) }
    }
}

@Composable
private fun InterestsStep(selected: Set<CodingInterest>, onToggle: (CodingInterest) -> Unit) {
    Column {
        Text(stringResource(R.string.onboarding_interests_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        val labels = mapOf(
            CodingInterest.PYTHON to R.string.onboarding_interest_python,
            CodingInterest.WEB to R.string.onboarding_interest_web,
            CodingInterest.GAMES to R.string.onboarding_interest_games,
            CodingInterest.APPS to R.string.onboarding_interest_apps,
            CodingInterest.AI_BASICS to R.string.onboarding_interest_ai,
            CodingInterest.CREATIVE_CODING to R.string.onboarding_interest_creative,
        )
        for ((interest, labelRes) in labels) {
            ChoiceCard(stringResource(labelRes), interest in selected) { onToggle(interest) }
        }
    }
}

@Composable
private fun NameStep(name: String, onName: (String) -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
        TerraAvatar(expression = TerraExpression.HAPPY, modifier = Modifier.size(120.dp))
        Spacer(Modifier.height(16.dp))
        Text(stringResource(R.string.onboarding_name_title), style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(
            value = name,
            onValueChange = onName,
            modifier = Modifier.fillMaxWidth(),
            label = { Text(stringResource(R.string.onboarding_name_hint)) },
            singleLine = true,
        )
    }
}
