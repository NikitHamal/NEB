package com.neb.ians.ui.screens.onboarding

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.PersonOutline
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebArtSlot
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebChoiceRow
import com.neb.ians.ui.components.NebDateWheel
import com.neb.ians.ui.components.NebDotTile
import com.neb.ians.ui.components.NebOptionCard
import com.neb.ians.ui.components.NebStepHeader
import com.neb.ians.ui.components.formatIsoDate
import com.neb.ians.ui.components.parseIsoDate
import com.neb.ians.ui.components.art.NebCalendarArt
import com.neb.ians.ui.components.art.NebFacetsArt
import com.neb.ians.ui.components.art.NebHandleArt
import com.neb.ians.ui.components.art.NebHandleState
import com.neb.ians.ui.components.art.NebHorizonArt
import com.neb.ians.ui.components.art.NebNameplateArt
import com.neb.ians.ui.components.art.NebPathsArt
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import java.util.Calendar

// ---------------------------------------------------------------------------
// Steps one to six: who is arriving.
// ---------------------------------------------------------------------------

@Composable
fun WelcomeStep() {
    val palette = LocalNebAuthPalette.current
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot { NebHorizonArt(height = 196.dp) }
        Spacer(modifier = Modifier.height(16.dp))
        NebStepHeader(
            title = "Welcome to NEBians",
            subtitle = "Let's build the profile Nepal's learning community will see. A few short questions — one at a time, nothing crammed."
        )
        Spacer(modifier = Modifier.height(NebAuthTokens.SectionGap))
        listOf(
            "Your handle" to "How classmates find and mention you",
            "Your level and subjects" to "So the feed carries the right notes and papers",
            "Your district and campus" to "So local resources and results reach you first"
        ).forEach { (title, detail) ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                verticalAlignment = androidx.compose.ui.Alignment.CenterVertically
            ) {
                NebDotTile(color = palette.sapphire)
                Spacer(modifier = Modifier.width(14.dp))
                Column {
                    Text(text = title, style = NebAuthType.Body, color = palette.ink)
                    Text(text = detail, style = NebAuthType.Caption, color = palette.inkMuted)
                }
            }
        }
    }
}

@Composable
fun RoleStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val selectedIndex = NEB_ROLES.indexOfFirst { it.key == state.role }
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot { NebPathsArt(selectedIndex = selectedIndex, pathCount = NEB_ROLES.size) }
        Spacer(modifier = Modifier.height(14.dp))
        NebStepHeader(
            title = "Which path is yours?",
            subtitle = "This shapes the rest of the questions and what your feed leads with."
        )
        Spacer(modifier = Modifier.height(22.dp))
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            NEB_ROLES.forEach { role ->
                NebOptionCard(
                    title = role.title,
                    subtitle = role.subtitle,
                    selected = state.role == role.key,
                    onClick = { viewModel.onRoleChange(role.key) }
                )
            }
        }
    }
}

@Composable
fun NameStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val name = state.displayName
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot {
            NebNameplateArt(
                initial = name.trim().firstOrNull(),
                progress = (name.trim().length / 16f).coerceIn(0f, 1f)
            )
        }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = "What should we call you?",
            subtitle = "Your display name appears on everything you post. You can change it later."
        )
        Spacer(modifier = Modifier.height(22.dp))
        NebAuthField(
            value = name,
            onValueChange = viewModel::onDisplayNameChange,
            label = "Display name",
            placeholder = "Aarati Sharma",
            leadingIcon = Icons.Outlined.PersonOutline,
            imeAction = ImeAction.Done
        )
    }
}

@Composable
fun HandleStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    val handleState = when {
        state.isCheckingUsername -> NebHandleState.Checking
        state.usernameError != null || state.usernameAvailable == false -> NebHandleState.Taken
        state.usernameAvailable == true -> NebHandleState.Available
        else -> NebHandleState.Idle
    }
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot { NebHandleArt(state = handleState) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = "Claim your handle",
            subtitle = "Letters, numbers and underscores. This is how people mention you in threads."
        )
        Spacer(modifier = Modifier.height(22.dp))
        NebAuthField(
            value = state.username,
            onValueChange = viewModel::onUsernameChange,
            label = "Username",
            placeholder = "aarati_np",
            leadingIcon = Icons.Outlined.AlternateEmail,
            keyboardType = KeyboardType.Ascii,
            imeAction = ImeAction.Done,
            error = state.usernameError ?: if (state.usernameAvailable == false) "That handle is taken" else null,
            helper = when {
                state.isCheckingUsername -> "Checking availability"
                state.usernameAvailable == true -> "@${state.username} is yours"
                state.username.isEmpty() -> "At least 3 characters"
                else -> null
            },
            helperTone = if (state.usernameAvailable == true) palette.success else null,
            trailing = {
                when {
                    state.isCheckingUsername -> CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        color = palette.sapphire,
                        strokeWidth = 2.dp
                    )
                    state.usernameAvailable == true -> Icon(
                        imageVector = Icons.Outlined.Check,
                        contentDescription = null,
                        tint = palette.success,
                        modifier = Modifier.size(20.dp)
                    )
                    state.usernameAvailable == false || state.usernameError != null -> Icon(
                        imageVector = Icons.Outlined.Close,
                        contentDescription = null,
                        tint = palette.danger,
                        modifier = Modifier.size(20.dp)
                    )
                    else -> Unit
                }
            }
        )
    }
}

@Composable
fun BirthdayStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val defaultYear = remember { Calendar.getInstance().get(Calendar.YEAR) - 17 }
    val parsed = parseIsoDate(state.dob)
    val year = parsed?.first ?: defaultYear
    val month = parsed?.second ?: 1
    val day = parsed?.third ?: 1

    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot(collapseOnKeyboard = false) { NebCalendarArt(dayOfMonth = parsed?.third) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = "When were you born?",
            subtitle = "We use this for age-appropriate content and nothing else. Only your age band is ever shown."
        )
        Spacer(modifier = Modifier.height(18.dp))
        NebDateWheel(
            year = year,
            month = month,
            day = day,
            onChange = { y, m, d -> viewModel.onDobChange(formatIsoDate(y, m, d)) }
        )
    }
}

@Composable
fun GenderStep(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val selectedIndex = NEB_GENDERS.indexOf(state.gender)
    Column(modifier = Modifier.fillMaxWidth()) {
        NebArtSlot(collapseOnKeyboard = false) { NebFacetsArt(selectedIndex = selectedIndex, count = NEB_GENDERS.size) }
        Spacer(modifier = Modifier.height(10.dp))
        NebStepHeader(
            title = "How do you identify?",
            subtitle = "Optional detail for your profile. Pick whichever fits."
        )
        Spacer(modifier = Modifier.height(22.dp))
        NebChoiceRow(
            options = NEB_GENDERS,
            selected = state.gender,
            onSelect = viewModel::onGenderChange
        )
    }
}
