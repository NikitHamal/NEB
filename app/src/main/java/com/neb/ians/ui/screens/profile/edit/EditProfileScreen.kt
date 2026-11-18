package com.neb.ians.ui.screens.profile.edit

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebComponentScope
import com.neb.ians.ui.components.NebInlineNote
import com.neb.ians.ui.components.NebNoteTone
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.nebKeyboardOpen
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.screens.profile.PhotoGalleryDialog
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec

/**
 * The profile editor. One scroll, six titled sections, and a save that is always
 * within reach — docked above the keyboard rather than hiding at the bottom of a
 * long form. It is built out of the same controls the onboarding journey uses, so
 * a field the user already filled in once looks and behaves the same coming back
 * to change it.
 */
@Composable
fun EditProfileScreen(
    onNavigateBack: () -> Unit,
    viewModel: CompleteProfileViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val scrollState = rememberScrollState()

    LaunchedEffect(Unit) {
        viewModel.setIsEditing(true)
        viewModel.fetchInstitutions()
    }

    LaunchedEffect(uiState.submissionResult) {
        if (uiState.submissionResult == true) onNavigateBack()
    }

    val strength = remember(uiState) { profileStrength(uiState) }
    val canSave = isProfileValid(uiState) && !uiState.isSubmitting

    val error = uiState.submissionError
    val usernameServerError = error?.takeIf { it.contains("username", ignoreCase = true) }
    val displayNameServerError = error?.takeIf { it.contains("display name", ignoreCase = true) }
    val dobServerError = error?.takeIf {
        it.contains("date of birth", ignoreCase = true) || it.contains("dob", ignoreCase = true)
    }
    val generalError = error?.takeIf {
        it != usernameServerError && it != displayNameServerError && it != dobServerError
    }

    NebComponentScope {
        val palette = LocalNebAuthPalette.current
        val keyboardOpen = nebKeyboardOpen()

        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(palette.page)
                .navigationBarsPadding()
                .imePadding()
        ) {
            Box(Modifier.fillMaxWidth().weight(1f)) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(scrollState)
            ) {
                EditProfileHero(
                    state = uiState,
                    viewModel = viewModel,
                    strength = strength
                )
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = NebAuthTokens.PageGutter)
                        .padding(top = NebAuthTokens.SectionGap),
                    verticalArrangement = Arrangement.spacedBy(NebAuthTokens.SectionGap)
                ) {
                EditBasicsSection(
                    state = uiState,
                    viewModel = viewModel,
                    usernameServerError = usernameServerError,
                    displayNameServerError = displayNameServerError
                )
                EditRoleSection(state = uiState, viewModel = viewModel)
                if (uiState.role != "institution") {
                    EditPersonalSection(
                        state = uiState,
                        viewModel = viewModel,
                        dobServerError = dobServerError
                    )
                }
                EditPortfolioSection(state = uiState, viewModel = viewModel)
                EditStudiesSection(state = uiState, viewModel = viewModel)
                EditPlaceSection(state = uiState, viewModel = viewModel)
                EditLinksSection(state = uiState, viewModel = viewModel)
                EditPrivacySection(state = uiState, viewModel = viewModel)

                Spacer(modifier = Modifier.height(8.dp))
                }
            }
            // sticky: Back and Save stay on screen however far the page is scrolled
            val density = androidx.compose.ui.platform.LocalDensity.current
            val screenW = androidx.compose.ui.platform.LocalConfiguration.current.screenWidthDp.dp
            val barPx = with(density) { (WindowInsets.statusBars.getTop(density) + 60.dp.toPx()) }
            val coverPx = with(density) { com.neb.ians.ui.components.profileCoverHeight(screenW, 0.dp).toPx() }
            val range = editBarRange(coverPx, barPx)
            EditProfileTopBar(
                progress = { ((scrollState.value - range * 0.55f) / (range * 0.45f)).coerceIn(0f, 1f) },
                canSave = canSave,
                onBack = onNavigateBack,
                onSave = viewModel::submitProfile,
                modifier = Modifier.align(Alignment.TopCenter)
            )
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(palette.page)
                    .padding(horizontal = NebAuthTokens.PageGutter)
                    .padding(top = 12.dp, bottom = 14.dp)
            ) {
                AnimatedVisibility(
                    visible = generalError != null && !keyboardOpen,
                    enter = fadeIn(nebEffectsSpec()),
                    exit = fadeOut(nebEffectsSpec())
                ) {
                    NebInlineNote(text = generalError, tone = NebNoteTone.Error)
                }
                NebPillButton(
                    text = "Save changes",
                    onClick = viewModel::submitProfile,
                    enabled = canSave,
                    loading = uiState.isSubmitting
                )
            }
        }
    }

    if (uiState.showPhotoGallery) {
        PhotoGalleryDialog(
            photos = uiState.photos,
            isLoading = uiState.photosLoading,
            isBusy = uiState.photoBusy || uiState.isPhotoUploading,
            onDismiss = viewModel::closePhotoGallery,
            onActivatePhoto = viewModel::activatePhoto,
            onUploadPhoto = viewModel::uploadPhoto
        )
    }
}

private fun isProfileValid(state: CompleteProfileUiState): Boolean =
    state.username.length >= 3 &&
        state.usernameAvailable != false &&
        state.usernameError == null &&
        state.displayName.isNotBlank() &&
        (state.role == "institution" || state.dob.isNotBlank()) &&
        (state.role != "student" || state.classLevel.isNotBlank()) &&
        (state.role != "teacher" || state.teachingSubjects.isNotEmpty()) &&
        (state.role != "institution" || state.school.isNotBlank())

private fun profileStrength(state: CompleteProfileUiState): Float {
    val filled = listOf(
        state.displayName.isNotBlank(),
        state.username.length >= 3,
        state.photoUrl.isNotBlank(),
        state.bio.isNotBlank(),
        state.dob.isNotBlank(),
        state.gender.isNotBlank(),
        state.district.isNotBlank(),
        state.school.isNotBlank(),
        state.subjects.isNotEmpty() || state.teachingSubjects.isNotEmpty() || state.role == "explorer",
        state.socialLinks.isNotEmpty()
    ).count { it }
    return filled / 10f
}
