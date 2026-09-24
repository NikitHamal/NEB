package com.neb.ians.ui.screens.onboarding

import androidx.activity.compose.BackHandler
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FiniteAnimationSpec
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.NebAuthTopBar
import com.neb.ians.ui.components.NebInlineNote
import com.neb.ians.ui.components.NebJourneySurface
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.NebTextLink
import com.neb.ians.ui.components.nebKeyboardOpen
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.NebMotion
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebFastEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

/**
 * Profile creation, one question at a time. Every step owns the whole screen: an
 * illustration that answers the question with the user, one headline, and the
 * smallest control that can take the answer. The old single-form version asked
 * for fourteen things at once, which is the fastest way to lose someone who has
 * just verified their email.
 */
@Composable
fun OnboardingScreen(
    onFinished: () -> Unit,
    viewModel: CompleteProfileViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val focusManager = LocalFocusManager.current
    val context = LocalContext.current

    val steps = remember(uiState.role) { stepsForRole(uiState.role) }
    var stepIndex by rememberSaveable { mutableIntStateOf(0) }
    var movingForward by remember { mutableStateOf(true) }

    val safeIndex = stepIndex.coerceIn(0, steps.lastIndex)
    val step = steps[safeIndex]
    val keyboardOpen = nebKeyboardOpen()

    LaunchedEffect(Unit) {
        viewModel.setIsEditing(false)
        viewModel.fetchInstitutions()
    }

    LaunchedEffect(uiState.submissionResult) {
        if (uiState.submissionResult == true) onFinished()
    }

    val photoPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        uri?.let {
            val bytes = context.contentResolver.openInputStream(it)?.use { stream -> stream.readBytes() }
            if (bytes != null) {
                viewModel.uploadPhoto(bytes, context.contentResolver.getType(it) ?: "image/jpeg")
            }
        }
    }

    fun goBack() {
        focusManager.clearFocus()
        if (safeIndex > 0) {
            movingForward = false
            stepIndex = safeIndex - 1
        }
    }

    fun goNext() {
        focusManager.clearFocus()
        if (safeIndex < steps.lastIndex) {
            movingForward = true
            stepIndex = safeIndex + 1
        }
    }

    BackHandler(enabled = safeIndex > 0) { goBack() }

    NebJourneySurface {
        NebAuthTopBar(
            onBack = if (safeIndex > 0) ({ goBack() }) else null,
            progress = (safeIndex + 1).toFloat() / steps.size
        )

        val stepSlide = nebSpatialSpec<IntOffset>()
        val stepFade = nebEffectsSpec<Float>()
        AnimatedContent(
            targetState = step,
            transitionSpec = { stepTransition(movingForward, stepSlide, stepFade) },
            label = "neb_onboarding_step",
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
        ) { target ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = NebAuthTokens.PageGutter)
            ) {
                OnboardingStepContent(
                    step = target,
                    state = uiState,
                    viewModel = viewModel,
                    onPickPhoto = { photoPicker.launch("image/*") }
                )
                Spacer(modifier = Modifier.height(24.dp))
            }
        }

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = NebAuthTokens.PageGutter)
                .padding(top = 8.dp, bottom = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            NebInlineNote(text = uiState.submissionError)

            AnimatedVisibility(
                visible = uiState.submissionError != null,
                enter = fadeIn(nebFastEffectsSpec()),
                exit = fadeOut(nebFastEffectsSpec())
            ) {
                Spacer(modifier = Modifier.height(12.dp))
            }

            NebPillButton(
                text = primaryLabelFor(step),
                onClick = {
                    if (step == OnboardingStep.Finish) {
                        viewModel.submitProfile()
                    } else {
                        goNext()
                    }
                },
                enabled = isStepComplete(step, uiState),
                loading = uiState.isSubmitting
            )

            AnimatedVisibility(
                visible = isStepSkippable(step) && !keyboardOpen,
                enter = fadeIn(nebEffectsSpec()),
                exit = fadeOut(nebEffectsSpec())
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(38.dp),
                    contentAlignment = Alignment.Center
                ) {
                    NebTextLink(
                        text = "Skip for now",
                        onClick = { goNext() },
                        enabled = !uiState.isSubmitting
                    )
                }
            }
        }
    }
}

/**
 * Steps travel sideways: forward slides in from the right, back from the left.
 * The slide runs on a spatial spring so an impatient second tap retargets from
 * wherever the step currently is instead of restarting it; the crossfade runs on
 * a critically damped effects spring, because opacity must not overshoot.
 */
private fun stepTransition(
    forward: Boolean,
    slide: FiniteAnimationSpec<IntOffset>,
    fade: FiniteAnimationSpec<Float>
) = (slideInHorizontally(
    animationSpec = slide,
    initialOffsetX = { full ->
        val offset = (full * NebMotion.StepSlideFraction).toInt()
        if (forward) offset else -offset
    }
) + fadeIn(fade)) togetherWith
    (slideOutHorizontally(
        animationSpec = slide,
        targetOffsetX = { full ->
            val offset = (full * NebMotion.StepSlideFraction).toInt()
            if (forward) -offset else offset
        }
    ) + fadeOut(fade))
