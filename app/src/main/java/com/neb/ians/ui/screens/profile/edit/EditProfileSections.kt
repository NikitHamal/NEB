package com.neb.ians.ui.screens.profile.edit

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AddAPhoto
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Cake
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.ExpandMore
import androidx.compose.material.icons.outlined.PersonOutline
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.ui.components.NebLoadingIndicator
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebFieldGroupLabel
import com.neb.ians.ui.components.NebGlyphTile
import com.neb.ians.ui.components.NebOptionCard
import com.neb.ians.ui.components.NebPickerField
import com.neb.ians.ui.components.NebProgressRail
import com.neb.ians.ui.components.NebShapes
import com.neb.ians.ui.components.NebSegmentedChoice
import com.neb.ians.ui.components.NebToggleRow
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.screens.onboarding.NEB_GENDER_SEGMENTS
import com.neb.ians.ui.screens.auth.CompleteProfileUiState
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec
import java.util.Calendar

/** A titled block. Every section on the editor is one of these and nothing else. */
@Composable
internal fun EditSection(
    title: String,
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit
) {
    Column(modifier = modifier.fillMaxWidth()) {
        NebFieldGroupLabel(text = title)
        Spacer(modifier = Modifier.height(12.dp))
        content()
    }
}

/**
 * The top of the editor: the photo, the two names as they will actually appear,
 * and how far along the profile is. Everything below this is detail.
 */
@Composable
internal fun EditIdentityHeader(
    state: CompleteProfileUiState,
    strength: Float,
    onManagePhotos: () -> Unit,
    modifier: Modifier = Modifier
) {
    val palette = LocalNebAuthPalette.current
    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .size(104.dp)
                .nebPressable(onClick = onManagePhotos),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(96.dp)
                    .clip(CircleShape)
                    .background(palette.field)
                    .border(1.5.dp, palette.accentSoft, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                if (state.photoUrl.isNotBlank()) {
                    AsyncImage(
                        model = state.photoUrl,
                        contentDescription = "Profile photo",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.size(96.dp).clip(CircleShape)
                    )
                } else {
                    Text(
                        text = state.displayName.trim().take(1).uppercase()
                            .ifBlank { state.username.take(1).uppercase().ifBlank { "N" } },
                        style = NebAuthType.Headline,
                        color = palette.accent
                    )
                }
                if (state.isPhotoUploading) {
                    Box(
                        modifier = Modifier.size(96.dp).clip(CircleShape).background(palette.page.copy(alpha = 0.72f)),
                        contentAlignment = Alignment.Center
                    ) {
                        NebLoadingIndicator(
                            modifier = Modifier.size(28.dp),
                            color = palette.accent
                        )
                    }
                }
            }
            Box(
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(palette.accent),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Outlined.AddAPhoto,
                    contentDescription = null,
                    tint = palette.onAccent,
                    modifier = Modifier.size(16.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        Text(
            text = state.displayName.ifBlank { "Your name" },
            style = NebAuthType.Title,
            color = if (state.displayName.isBlank()) palette.inkFaint else palette.ink
        )
        Spacer(modifier = Modifier.height(2.dp))
        Text(
            text = "@" + state.username.ifBlank { "username" },
            style = NebAuthType.Caption,
            color = palette.accent
        )

        Spacer(modifier = Modifier.height(18.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text = "Profile strength", style = NebAuthType.Caption, color = palette.inkMuted)
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = "${(strength * 100).toInt()}%",
                style = NebAuthType.Caption,
                color = palette.accent
            )
        }
        Spacer(modifier = Modifier.height(8.dp))
        NebProgressRail(progress = strength)
    }
}

@Composable
internal fun EditRoleSection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    EditSection(title = "You on NEBians") {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            EDIT_ROLES.forEachIndexed { index, role ->
                val selected = state.role == role.key
                NebOptionCard(
                    title = role.title,
                    subtitle = role.subtitle,
                    selected = selected,
                    onClick = { viewModel.onRoleChange(role.key) },
                    leading = {
                        NebGlyphTile(selected = selected, polygon = NebShapes.option(index)) {
                            Icon(
                                imageVector = role.icon,
                                contentDescription = null,
                                tint = if (selected) palette.accent else palette.inkMuted,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    }
                )
            }
        }
    }
}

@Composable
internal fun EditBasicsSection(
    state: CompleteProfileUiState,
    viewModel: CompleteProfileViewModel,
    usernameServerError: String?,
    displayNameServerError: String?
) {
    val palette = LocalNebAuthPalette.current
    val handleHelper = when {
        state.usernameAvailable == true -> "That handle is free"
        else -> null
    }
    val handleError = when {
        state.usernameError != null -> state.usernameError
        state.usernameAvailable == false -> "That handle is already taken"
        usernameServerError != null -> usernameServerError
        else -> null
    }

    EditSection(title = "The basics") {
        Column(verticalArrangement = Arrangement.spacedBy(NebAuthTokens.StackGap)) {
            NebAuthField(
                value = state.displayName,
                onValueChange = viewModel::onDisplayNameChange,
                label = "Display name",
                placeholder = "Your full name",
                leadingIcon = Icons.Outlined.PersonOutline,
                error = displayNameServerError
            )
            NebAuthField(
                value = state.username,
                onValueChange = viewModel::onUsernameChange,
                label = "Username",
                placeholder = "username",
                leadingIcon = Icons.Outlined.AlternateEmail,
                error = handleError,
                helper = handleHelper,
                helperTone = palette.success,
                trailing = {
                    when {
                        state.isCheckingUsername -> NebLoadingIndicator(
                            modifier = Modifier.size(20.dp),
                            color = palette.inkFaint
                        )
                        state.usernameAvailable == true -> Icon(
                            imageVector = Icons.Outlined.Check,
                            contentDescription = null,
                            tint = palette.success,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            )
            NebAuthField(
                value = state.email,
                onValueChange = viewModel::onEmailChange,
                label = "Email",
                placeholder = "you@example.com",
                leadingIcon = Icons.Outlined.AlternateEmail,
                keyboardType = KeyboardType.Email
            )
            EditBioField(state = state, viewModel = viewModel)
        }
    }
}

@Composable
private fun EditBioField(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    val limit = 160
    Column(modifier = Modifier.fillMaxWidth()) {
        NebAuthField(
            value = state.bio,
            onValueChange = { if (it.length <= limit + 40) viewModel.onBioChange(it) },
            label = "Bio",
            placeholder = "A line or two about you",
            singleLine = false,
            imeAction = ImeAction.Default,
            minHeight = 112.dp
        )
        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = "${state.bio.length} / $limit",
            style = NebAuthType.Caption,
            color = if (state.bio.length > limit) palette.danger else palette.inkFaint,
            modifier = Modifier.align(Alignment.End)
        )
    }
}

@Composable
internal fun EditPersonalSection(
    state: CompleteProfileUiState,
    viewModel: CompleteProfileViewModel,
    dobServerError: String?
) {
    val context = LocalContext.current
    val defaultYear = remember { Calendar.getInstance().get(Calendar.YEAR) - 17 }

    EditSection(title = "Personal") {
        Column(verticalArrangement = Arrangement.spacedBy(NebAuthTokens.StackGap)) {
            NebPickerField(
                label = "Date of birth",
                value = state.dob,
                placeholder = "YYYY-MM-DD",
                leadingIcon = Icons.Outlined.Cake,
                error = dobServerError,
                onClick = {
                    val parts = state.dob.split("-").mapNotNull { it.toIntOrNull() }
                    val now = Calendar.getInstance()
                    android.app.DatePickerDialog(
                        context,
                        { _, year, month, day ->
                            viewModel.onDobChange(
                                "%04d-%02d-%02d".format(year, month + 1, day)
                            )
                        },
                        parts.getOrNull(0) ?: defaultYear,
                        (parts.getOrNull(1)?.minus(1)) ?: now.get(Calendar.MONTH),
                        parts.getOrNull(2) ?: now.get(Calendar.DAY_OF_MONTH)
                    ).show()
                }
            )

            Column {
                NebFieldGroupLabel(text = "Gender")
                Spacer(modifier = Modifier.height(10.dp))
                NebSegmentedChoice(
                    segments = NEB_GENDER_SEGMENTS,
                    selected = state.gender.takeIf { it.isNotBlank() },
                    onSelect = viewModel::onGenderChange
                )
            }
        }
    }
}

@Composable
internal fun EditPrivacySection(state: CompleteProfileUiState, viewModel: CompleteProfileViewModel) {
    val palette = LocalNebAuthPalette.current
    EditSection(title = "Privacy") {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(androidx.compose.foundation.shape.RoundedCornerShape(NebAuthTokens.CardRadius))
                .background(palette.field)
        ) {
            NebToggleRow(
                title = "Private profile",
                subtitle = "Only people you approve can see your posts and details",
                checked = state.isLocked,
                onCheckedChange = viewModel::onLockedChange
            )
        }
        AnimatedVisibility(
            visible = state.isLocked,
            enter = fadeIn(nebEffectsSpec()),
            exit = fadeOut(nebEffectsSpec())
        ) {
            Text(
                text = "Your name, photo and handle stay visible so people can find and request you.",
                style = NebAuthType.Caption,
                color = palette.inkFaint,
                modifier = Modifier.padding(top = 10.dp, start = 4.dp, end = 4.dp)
            )
        }
    }
}

@Composable
internal fun EditPickerRowField(
    label: String,
    value: String,
    placeholder: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    error: String? = null
) {
    NebPickerField(
        label = label,
        value = value,
        placeholder = placeholder,
        onClick = onClick,
        modifier = modifier,
        trailingIcon = Icons.Outlined.ExpandMore,
        error = error
    )
}

@Composable
internal fun EditInlineHint(text: String, modifier: Modifier = Modifier) {
    val palette = LocalNebAuthPalette.current
    Row(modifier = modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Box(
            modifier = Modifier
                .size(4.dp)
                .clip(CircleShape)
                .background(palette.inkFaint)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(text = text, style = NebAuthType.Caption, color = palette.inkFaint)
    }
}
