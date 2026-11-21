package com.neb.ians.ui.screens.profile.edit

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Place
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebChoiceTiles
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebPickerField
import com.neb.ians.ui.components.NebPickerSheet
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.components.rememberNebChoiceTiles
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec

@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun EditStudiesSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val heading = when (state.role) {
        "teacher" -> "What you teach"
        "institution" -> "About the institution"
        "explorer" -> "Studies"
        else -> "What you study"
    }

    val fade = nebEffectsSpec<Float>()
    EditSection(title = heading) {
        AnimatedContent(
            targetState = state.role,
            transitionSpec = { fadeIn(fade) togetherWith fadeOut(fade) },
            label = "neb_edit_role_fields"
        ) { role ->
            Column(verticalArrangement = Arrangement.spacedBy(NebAuthTokens.StackGap)) {
                when (role) {
                    "institution" -> {
                        NebFieldGroupLabel(text = "Type")
                        Spacer(modifier = Modifier.height(10.dp))
                        NebChoiceTiles(
                            segments = rememberNebChoiceTiles(EDIT_INSTITUTION_TYPES),
                            selected = state.institutionType.replaceFirstChar { it.uppercase() }
                                .takeIf { state.institutionType.isNotBlank() },
                            onSelect = { viewModel.onInstitutionTypeChange(it.lowercase()) }
                        )
                    }
                    "explorer" -> {
                        EditInlineHint(text = "Pick a path above whenever you want these details back.")
                    }
                    else -> {
                        val levels = remember(role) { com.neb.ians.ui.screens.onboarding.levelsForRole(role) }
                        Column(modifier = Modifier.fillMaxWidth()) {
                            NebFieldGroupLabel(text = if (role == "student") "Level" else "Level you teach")
                            Spacer(modifier = Modifier.height(10.dp))
                            FlowRow(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                levels.forEach { level ->
                                    NebSelectChip(
                                        label = level,
                                        selected = state.classLevel == level,
                                        onClick = { viewModel.onClassChange(level) }
                                    )
                                }
                            }
                        }
                        if (role == "student" && state.classLevel.isNotBlank()) EduSituation(state, viewModel)
                        EditSubjectPicker(state = state, viewModel = viewModel, teaching = role == "teacher")
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun EditSubjectPicker(
    state: CompleteProfileUiState,
    viewModel: CompleteProfileViewModel,
    teaching: Boolean
) {
    val chosen = if (teaching) state.teachingSubjects else state.subjects
    Column(modifier = Modifier.fillMaxWidth()) {
        NebFieldGroupLabel(text = if (teaching) "Subjects you teach" else "Subjects")
        Spacer(modifier = Modifier.height(10.dp))
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            com.neb.ians.ui.screens.onboarding.NEB_SUBJECTS.forEach { subject ->
                NebSelectChip(
                    label = subject,
                    selected = chosen.contains(subject),
                    onClick = {
                        if (teaching) viewModel.onTeachingSubjectToggle(subject)
                        else viewModel.onSubjectToggle(subject)
                    }
                )
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun EditPlaceSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    var showDistrict by remember { mutableStateOf(false) }

    val schoolLabel = if (state.role == "institution") "Institution name" else "School or college"

    EditSection(title = "Where you are") {
        Column(verticalArrangement = Arrangement.spacedBy(NebAuthTokens.StackGap)) {
            Column(modifier = Modifier.fillMaxWidth()) {
                NebFieldGroupLabel(text = "Province")
                Spacer(modifier = Modifier.height(10.dp))
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    com.neb.ians.ui.screens.onboarding.NEB_PRADESH.forEach { pradesh ->
                        NebSelectChip(
                            label = pradesh,
                            selected = state.pradesh == pradesh,
                            onClick = { viewModel.onPradeshChange(pradesh) }
                        )
                    }
                }
            }
            NebPickerField(
                label = "District",
                value = state.district,
                placeholder = "Select your district",
                onClick = { showDistrict = true },
                leadingIcon = Icons.Outlined.Place,
                trailingIcon = Icons.Outlined.ExpandMore
            )
            com.neb.ians.ui.screens.onboarding.CampusSelector(
                state = state,
                viewModel = viewModel,
                label = schoolLabel
            )
        }
    }

    if (showDistrict) {
        NebPickerSheet(
            title = "Select district",
            options = com.neb.ians.ui.screens.onboarding.NEB_DISTRICTS,
            selected = state.district.takeIf { it.isNotBlank() },
            onSelect = {
                viewModel.onDistrictChange(it)
                showDistrict = false
            },
            onDismiss = { showDistrict = false },
            searchPlaceholder = "Search 77 districts"
        )
    }
}
