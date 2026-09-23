package com.neb.ians.ui.screens.onboarding

import androidx.compose.runtime.Composable
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel

@Composable
fun OnboardingStepContent(
    step: OnboardingStep,
    state: CompleteProfileUiState,
    viewModel: CompleteProfileViewModel,
    onPickPhoto: () -> Unit
) {
    when (step) {
        OnboardingStep.Welcome -> WelcomeStep()
        OnboardingStep.Role -> RoleStep(state, viewModel)
        OnboardingStep.Name -> NameStep(state, viewModel)
        OnboardingStep.Handle -> HandleStep(state, viewModel)
        OnboardingStep.Birthday -> BirthdayStep(state, viewModel)
        OnboardingStep.Gender -> GenderStep(state, viewModel)
        OnboardingStep.Level -> LevelStep(state, viewModel)
        OnboardingStep.Subjects -> SubjectsStep(state, viewModel)
        OnboardingStep.Place -> PlaceStep(state, viewModel)
        OnboardingStep.Campus -> CampusStep(state, viewModel)
        OnboardingStep.Portrait -> PortraitStep(state, onPickPhoto)
        OnboardingStep.Bio -> BioStep(state, viewModel)
        OnboardingStep.Finish -> FinishStep(state)
    }
}
