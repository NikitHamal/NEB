package com.neb.ians.ui.screens.onboarding

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AddAPhoto
import androidx.compose.material.icons.outlined.Domain
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.Place
import androidx.compose.material3.Icon
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.ui.components.NebLoadingIndicator
import com.neb.ians.ui.components.NebArtSlot
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebOutlinePillButton
import com.neb.ians.ui.components.NebPickerField
import com.neb.ians.ui.components.NebPickerSheet
import com.neb.ians.ui.components.NebSelectChip
import com.neb.ians.ui.components.NebStepHeader
import com.neb.ians.ui.components.NebTextLink
import com.neb.ians.ui.components.art.NebApertureArt
import com.neb.ians.ui.components.art.NebArrivalArt
import com.neb.ians.ui.components.art.NebAscentArt
import com.neb.ians.ui.components.art.NebCampusArt
import com.neb.ians.ui.components.art.NebOrbitsArt
import com.neb.ians.ui.components.art.NebProvinceArt
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens

// ---------------------------------------------------------------------------
// Steps seven onward: what you study, where, and the face on it.
// ---------------------------------------------------------------------------

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun LevelStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val levels = remember(state.role) { levelsForRole(state.role) }
    val index = levels.indexOf(state.classLevel).coerceAtLeast(0)
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot(collapseOnKeyboard = false) { NebAscentArt(stepIndex = index, stepCount = levels.size) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = if (state.role == "teacher") "Which levels do you teach?" else "Where are you right now?",
            subtitle = if (state.role == "teacher") {
                "Pick the level you spend most of your time on."
            } else {
                "Your level decides which syllabus, notes and past papers surface first."
            }
        )
        Spacer(modifier = Modifier.height(20.dp))
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
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun SubjectsStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    val isTeacher = state.role == "teacher"
    val selected = if (isTeacher) state.teachingSubjects else state.subjects
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot(collapseOnKeyboard = false) { NebOrbitsArt(selectedCount = selected.size, nodeCount = 8) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = if (isTeacher) "What do you teach?" else "What are you studying?",
            subtitle = "Pick as many as apply. These drive your feed, your notes shelf and who you get matched with."
        )
        Spacer(modifier = Modifier.height(20.dp))
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NEB_SUBJECTS.forEach { subject ->
                NebSelectChip(
                    label = subject,
                    selected = selected.contains(subject),
                    onClick = {
                        if (isTeacher) viewModel.onTeachingSubjectToggle(subject)
                        else viewModel.onSubjectToggle(subject)
                    }
                )
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        Text(
            text = if (selected.isEmpty()) "Nothing picked yet" else "${selected.size} selected",
            style = NebAuthType.Caption,
            color = if (selected.isEmpty()) palette.inkFaint else palette.accent
        )
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun PlaceStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    var showDistricts by remember { mutableStateOf(false) }
    val provinceIndex = NEB_PRADESH.indexOf(state.pradesh).coerceAtLeast(0)

    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot(collapseOnKeyboard = false) { NebProvinceArt(provinceIndex = provinceIndex, provinceCount = NEB_PRADESH.size) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = "Where do you study from?",
            subtitle = "Local results, notices and study groups are found by district."
        )
        Spacer(modifier = Modifier.height(20.dp))
        NebFieldGroupLabel("Province")
        Spacer(modifier = Modifier.height(10.dp))
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            NEB_PRADESH.forEach { pradesh ->
                NebSelectChip(
                    label = pradesh,
                    selected = state.pradesh == pradesh,
                    onClick = { viewModel.onPradeshChange(pradesh) }
                )
            }
        }
        Spacer(modifier = Modifier.height(NebAuthTokens.StackGap + 4.dp))
        NebPickerField(
            label = "District",
            value = state.district,
            placeholder = "Select your district",
            onClick = { showDistricts = true },
            leadingIcon = Icons.Outlined.Place,
            trailingIcon = Icons.Outlined.ExpandMore
        )
    }

    if (showDistricts) {
        NebPickerSheet(
            title = "Select district",
            options = NEB_DISTRICTS,
            selected = state.district,
            onSelect = {
                viewModel.onDistrictChange(it)
                showDistricts = false
            },
            onDismiss = { showDistricts = false },
            searchPlaceholder = "Search 77 districts"
        )
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun CampusStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    var showRegistered by remember { mutableStateOf(false) }
    val isInstitution = state.role == "institution"
    val registeredNames = remember(state.institutions) { state.institutions.map { it.displayName } }

    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot { NebCampusArt(named = state.school.isNotBlank()) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = when (state.role) {
                "teacher" -> "Where do you teach?"
                "institution" -> "Which institution is this?"
                else -> "Which school or college?"
            },
            subtitle = "Naming it puts you on your campus board and its shared resource shelf."
        )
        Spacer(modifier = Modifier.height(20.dp))

        if (isInstitution) {
            NebFieldGroupLabel("Institution type")
            Spacer(modifier = Modifier.height(10.dp))
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                NEB_INSTITUTION_TYPES.forEach { type ->
                    NebSelectChip(
                        label = type.replaceFirstChar { it.uppercase() },
                        selected = state.institutionType == type,
                        onClick = { viewModel.onInstitutionTypeChange(type) }
                    )
                }
            }
            Spacer(modifier = Modifier.height(NebAuthTokens.StackGap + 4.dp))
        }

        NebAuthField(
            value = state.school,
            onValueChange = { viewModel.onSchoolChange(it) },
            label = "Institution name",
            placeholder = "Institution's name",
            leadingIcon = Icons.Outlined.Domain,
            imeAction = ImeAction.Done
        )

        if (registeredNames.isNotEmpty()) {
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Already on NEBians?",
                    style = NebAuthType.Caption,
                    color = palette.inkMuted
                )
                Spacer(modifier = Modifier.width(2.dp))
                NebTextLink(
                    text = "Pick from ${registeredNames.size}",
                    onClick = { showRegistered = true }
                )
            }
        }
    }

    if (showRegistered) {
        NebPickerSheet(
            title = "Registered institutions",
            options = registeredNames,
            selected = state.school,
            onSelect = { name ->
                val match = state.institutions.firstOrNull { it.displayName == name }
                viewModel.onSchoolChange(name, match?.username ?: "")
                showRegistered = false
            },
            onDismiss = { showRegistered = false },
            searchPlaceholder = "Search institutions"
        )
    }
}

@Composable
fun PortraitStep(state: CompleteProfileUiState, onPickPhoto: () -> Unit) {
    val palette = LocalNebAuthPalette.current
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        NebArtSlot {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(164.dp),
                contentAlignment = Alignment.Center
            ) {
                if (state.photoUrl.isBlank()) {
                    NebApertureArt(hasPhoto = false, height = 164.dp)
                } else {
                    AsyncImage(
                        model = state.photoUrl,
                        contentDescription = "Your profile photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .size(128.dp)
                            .clip(CircleShape)
                            .border(2.dp, palette.accent, CircleShape)
                    )
                }
                if (state.isPhotoUploading) {
                    Box(
                        modifier = Modifier
                            .size(60.dp)
                            .clip(CircleShape)
                            .background(palette.page.copy(alpha = 0.86f)),
                        contentAlignment = Alignment.Center
                    ) {
                        NebLoadingIndicator(
                            modifier = Modifier.size(30.dp),
                            color = palette.accent
                        )
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        NebStepHeader(
            title = "Put a face to the name",
            subtitle = "Profiles with a photo get more replies. You can skip this and add one later.",
            align = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(22.dp))
        NebOutlinePillButton(
            text = if (state.photoUrl.isBlank()) "Choose a photo" else "Choose another",
            onClick = onPickPhoto,
            enabled = !state.isPhotoUploading,
            leadingIcon = Icons.Outlined.AddAPhoto
        )
    }
}

@Composable
fun BioStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    val limit = 160
    Column(modifier = Modifier.fillMaxWidth()) {
        Spacer(modifier = Modifier.height(NebAuthTokens.ArtClearance))
        NebStepHeader(
            title = "Say something about you",
            subtitle = "One or two lines. What you are working towards, what you like helping with."
        )
        Spacer(modifier = Modifier.height(22.dp))
        NebAuthField(
            value = state.bio,
            onValueChange = { if (it.length <= limit) viewModel.onBioChange(it) },
            label = "Bio",
            placeholder = "Class 12 science, aiming for engineering. Happy to explain calculus.",
            singleLine = false,
            minHeight = 132.dp,
            imeAction = ImeAction.Default
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "${state.bio.length} / $limit",
            style = NebAuthType.Caption,
            color = if (state.bio.length >= limit) palette.danger else palette.inkFaint,
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.End
        )
    }
}

@Composable
fun FinishStep(state: CompleteProfileUiState) {
    val palette = LocalNebAuthPalette.current
    val role = NEB_ROLES.firstOrNull { it.key == state.role }?.title ?: state.role
    val subjects = if (state.role == "teacher") state.teachingSubjects else state.subjects

    val rows = buildList {
        add("Handle" to "@${state.username}")
        add("Name" to state.displayName)
        add("Path" to role)
        if (state.classLevel.isNotBlank() && state.role != "institution") add("Level" to state.classLevel)
        if (subjects.isNotEmpty()) add("Subjects" to subjects.joinToString(", "))
        add("District" to "${state.district}, ${state.pradesh}")
        if (state.school.isNotBlank()) add("Campus" to state.school)
    }

    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot { NebArrivalArt(height = 172.dp) }
        Spacer(modifier = Modifier.height(12.dp))
        NebStepHeader(
            title = "That's your profile",
            subtitle = "Check it over. Everything here can be edited from your profile later.",
            align = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(22.dp))
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(NebAuthTokens.CardRadius))
                .background(palette.card)
                .border(
                    NebAuthTokens.Hairline,
                    palette.hairline,
                    RoundedCornerShape(NebAuthTokens.CardRadius)
                )
                .padding(horizontal = 18.dp, vertical = 6.dp)
        ) {
            rows.forEachIndexed { index, (label, value) ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 13.dp),
                    verticalAlignment = Alignment.Top
                ) {
                    Text(
                        text = label,
                        style = NebAuthType.Caption,
                        color = palette.inkMuted,
                        modifier = Modifier.width(86.dp)
                    )
                    Text(
                        text = value.ifBlank { "—" },
                        style = NebAuthType.Body.copy(fontWeight = FontWeight.SemiBold, fontSize = 14.sp),
                        color = palette.ink,
                        modifier = Modifier.fillMaxWidth()
                    )
                }
                if (index != rows.lastIndex) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(NebAuthTokens.Hairline)
                            .background(palette.hairline)
                    )
                }
            }
        }
    }
}
