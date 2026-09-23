package com.neb.ians.ui.screens.profile.edit

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Domain
import androidx.compose.material.icons.outlined.Place
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiInstitution
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebSegmentedChoice
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebOutlinePillButton
import com.neb.ians.ui.components.NebPickerRow
import com.neb.ians.ui.components.NebPickerSheet
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.components.NebSheetSurface
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec

@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun EditStudiesSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    var showClass by remember { mutableStateOf(false) }

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
                        NebSegmentedChoice(
                            options = EDIT_INSTITUTION_TYPES,
                            selected = state.institutionType.replaceFirstChar { it.uppercase() }
                                .takeIf { state.institutionType.isNotBlank() },
                            onSelect = { viewModel.onInstitutionTypeChange(it.lowercase()) }
                        )
                    }
                    "explorer" -> {
                        EditInlineHint(text = "Pick a path above whenever you want these details back.")
                    }
                    else -> {
                        EditPickerRowField(
                            label = if (role == "student") "Class" else "Class you teach",
                            value = state.classLevel,
                            placeholder = "Select a level",
                            onClick = { showClass = true }
                        )
                        EditSubjectPicker(state = state, viewModel = viewModel, teaching = role == "teacher")
                    }
                }
            }
        }
    }

    if (showClass) {
        NebPickerSheet(
            title = if (state.role == "student") "Your class" else "Class you teach",
            options = if (state.role == "student") EDIT_STUDENT_CLASSES else EDIT_TEACHER_CLASSES,
            selected = state.classLevel.takeIf { it.isNotBlank() },
            onSelect = viewModel::onClassChange,
            onDismiss = { showClass = false }
        )
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
            EDIT_SUBJECTS.forEach { subject ->
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

@Composable
internal fun EditPlaceSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    var showProvince by remember { mutableStateOf(false) }
    var showDistrict by remember { mutableStateOf(false) }
    var showInstitution by remember { mutableStateOf(false) }

    val schoolLabel = if (state.role == "institution") "Institution name" else "School or college"

    EditSection(title = "Where you are") {
        Column(verticalArrangement = Arrangement.spacedBy(NebAuthTokens.StackGap)) {
            EditPickerRowField(
                label = "Province",
                value = state.pradesh,
                placeholder = "Select a province",
                onClick = { showProvince = true }
            )
            EditPickerRowField(
                label = "District",
                value = state.district,
                placeholder = "Select a district",
                onClick = { showDistrict = true }
            )
            EditPickerRowField(
                label = schoolLabel,
                value = state.school,
                placeholder = "Institution's name",
                onClick = { showInstitution = true }
            )
        }
    }

    if (showProvince) {
        NebPickerSheet(
            title = "Province",
            options = EDIT_PROVINCES,
            selected = state.pradesh.takeIf { it.isNotBlank() },
            onSelect = viewModel::onPradeshChange,
            onDismiss = { showProvince = false }
        )
    }
    if (showDistrict) {
        NebPickerSheet(
            title = "District",
            options = EDIT_DISTRICTS,
            selected = state.district.takeIf { it.isNotBlank() },
            onSelect = viewModel::onDistrictChange,
            onDismiss = { showDistrict = false },
            searchPlaceholder = "Search districts"
        )
    }
    if (showInstitution) {
        EditInstitutionSheet(
            institutions = state.institutions,
            current = state.school,
            onSelect = { name, username -> viewModel.onSchoolChange(name, username) },
            onDismiss = { showInstitution = false }
        )
    }
}

/**
 * Institutions on the platform first, because picking one links the two profiles
 * together. Typing a name by hand stays available underneath for everywhere the
 * platform has not reached yet.
 */
@Composable
private fun EditInstitutionSheet(
    institutions: List<ApiInstitution>,
    current: String,
    onSelect: (String, String) -> Unit,
    onDismiss: () -> Unit
) {
    val palette = LocalNebAuthPalette.current
    var query by remember { mutableStateOf("") }
    var custom by remember { mutableStateOf(current) }
    val shown = remember(query, institutions) {
        if (query.isBlank()) {
            institutions
        } else {
            institutions.filter {
                it.displayName.contains(query.trim(), ignoreCase = true) ||
                    it.username.contains(query.trim(), ignoreCase = true)
            }
        }
    }

    NebSheetSurface(
        title = "Institution",
        subtitle = "Search the ones already on NEBians, or type your own.",
        onDismiss = onDismiss
    ) {
        NebAuthField(
            value = query,
            onValueChange = { query = it },
            label = "",
            placeholder = "Search institutions",
            leadingIcon = Icons.Outlined.Domain
        )

        Spacer(modifier = Modifier.height(10.dp))

        LazyColumn(modifier = Modifier.fillMaxWidth().heightIn(max = 260.dp)) {
            items(shown, key = { it.id.ifBlank { it.username } }) { institution ->
                NebPickerRow(
                    label = institution.displayName,
                    supporting = "@${institution.username}",
                    selected = institution.displayName == current,
                    onClick = {
                        onSelect(institution.displayName, institution.username)
                        onDismiss()
                    },
                    leading = {
                        if (institution.photoUrl.isBlank()) {
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(palette.accentSoft),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = institution.displayName.take(1).uppercase(),
                                    style = NebAuthType.Label,
                                    color = palette.accent
                                )
                            }
                        } else {
                            AsyncImage(
                                model = institution.photoUrl,
                                contentDescription = null,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.size(36.dp).clip(CircleShape)
                            )
                        }
                    }
                )
            }
        }

        if (shown.isEmpty()) {
            EditInlineHint(
                text = "No institution on NEBians matches that yet.",
                modifier = Modifier.padding(vertical = 12.dp)
            )
        }

        Spacer(modifier = Modifier.height(14.dp))
        Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(palette.hairline))
        Spacer(modifier = Modifier.height(14.dp))

        NebAuthField(
            value = custom,
            onValueChange = { custom = it },
            label = "Or type it yourself",
            placeholder = "Institution's name",
            leadingIcon = Icons.Outlined.Place
        )
        Spacer(modifier = Modifier.height(12.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            NebOutlinePillButton(
                text = "Use this name",
                onClick = {
                    onSelect(custom.trim(), "")
                    onDismiss()
                },
                enabled = custom.isNotBlank(),
                modifier = Modifier.weight(1f)
            )
            if (current.isNotBlank()) {
                Spacer(modifier = Modifier.width(10.dp))
                NebOutlinePillButton(
                    text = "Clear",
                    onClick = {
                        onSelect("", "")
                        onDismiss()
                    },
                    modifier = Modifier.weight(0.6f)
                )
            }
        }
    }
}
