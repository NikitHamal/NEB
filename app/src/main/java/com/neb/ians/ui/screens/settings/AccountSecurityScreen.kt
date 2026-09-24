package com.neb.ians.ui.screens.settings

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.FiniteAnimationSpec
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.ErrorOutline
import androidx.compose.material.icons.outlined.HelpOutline
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.MailOutline
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.theme.nebFastEffectsSpec
import kotlinx.coroutines.delay

// ---------------------------------------------------------------------------
// Account security.
//
// One screen, four panels. The overview lists what an account is protected by;
// tapping either line walks into the panel that changes it, and every panel
// comes back here with a single line saying what happened. Nothing changes
// without a code or the current password, so the screen can afford to be calm
// about it -- no warnings, no red, just the step in front of you.
// ---------------------------------------------------------------------------

private const val CODE_LENGTH = 6
private const val RESEND_COOLDOWN_SECONDS = 60

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountSecurityScreen(
    onNavigateBack: () -> Unit,
    viewModel: AccountSecurityViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val onBack: () -> Unit = {
        if (state.step == SecurityStep.Overview) onNavigateBack() else viewModel.back()
    }
    // Read outside the transition lambda: that lambda is not composable.
    val fade: FiniteAnimationSpec<Float> = nebFastEffectsSpec()

    BackHandler(enabled = state.step != SecurityStep.Overview) { viewModel.back() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = when (state.step) {
                            SecurityStep.Overview -> "Account security"
                            SecurityStep.EmailForm -> "Change email"
                            SecurityStep.EmailCode -> "Confirm email"
                            SecurityStep.PasswordForm ->
                                if (state.hasPassword) "Change password" else "Set password"
                            SecurityStep.ForgotCode -> "Reset password"
                        },
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when {
                state.loading -> NebLoader(modifier = Modifier.align(Alignment.Center))

                state.loadError != null -> Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = state.loadError.orEmpty(),
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    NebButton(text = "Retry", onClick = viewModel::load)
                }

                else -> AnimatedContent(
                    targetState = state.step,
                    transitionSpec = {
                        fadeIn(animationSpec = fade) togetherWith fadeOut(animationSpec = fade)
                    },
                    label = "security_step"
                ) { step ->
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .verticalScroll(rememberScrollState())
                            .padding(vertical = 16.dp)
                    ) {
                        when (step) {
                            SecurityStep.Overview -> OverviewPanel(state, viewModel)
                            SecurityStep.EmailForm -> EmailFormPanel(state, viewModel)
                            SecurityStep.EmailCode -> EmailCodePanel(state, viewModel)
                            SecurityStep.PasswordForm -> PasswordPanel(state, viewModel)
                            SecurityStep.ForgotCode -> ForgotPanel(state, viewModel)
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                    }
                }
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Overview
// ---------------------------------------------------------------------------

@Composable
private fun OverviewPanel(
    state: AccountSecurityUiState,
    viewModel: AccountSecurityViewModel
) {
    if (state.notice != null) {
        NoticeCard(text = state.notice, tone = NoticeTone.Good)
        Spacer(modifier = Modifier.height(16.dp))
    }
    if (state.error != null) {
        NoticeCard(text = state.error, tone = NoticeTone.Bad)
        Spacer(modifier = Modifier.height(16.dp))
    }

    SettingsGroup(title = "Email") {
        SettingsRow(
            icon = Icons.Outlined.MailOutline,
            title = state.email.ifBlank { "No email yet" },
            subtitle = when {
                state.email.isBlank() -> "Add one so you can get back in"
                state.emailVerified -> "Confirmed"
                else -> "Not confirmed"
            },
            onClick = viewModel::openEmailForm
        )
    }

    if (state.pendingEmail.isNotBlank()) {
        Spacer(modifier = Modifier.height(12.dp))
        PendingEmailCard(
            pendingEmail = state.pendingEmail,
            busy = state.busy,
            onEnterCode = viewModel::openEmailCode,
            onCancel = viewModel::cancelEmailChange
        )
    }

    Spacer(modifier = Modifier.height(24.dp))

    SettingsGroup(title = "Password") {
        SettingsRow(
            icon = Icons.Outlined.Lock,
            title = if (state.hasPassword) "Change password" else "Set a password",
            subtitle = if (state.hasPassword) {
                "You'll need your current one"
            } else {
                "Sign in with an email and password too"
            },
            onClick = viewModel::openPasswordForm
        )
        SettingsDivider()
        SettingsRow(
            icon = Icons.Outlined.HelpOutline,
            title = "Forgot your password?",
            subtitle = "Get a code by email and set a new one",
            onClick = viewModel::startForgotPassword
        )
    }

    Spacer(modifier = Modifier.height(16.dp))
    FootNote(
        "Changing your email signs you out on every other device. Your posts, " +
            "replies and saved work stay exactly where they are."
    )
}

@Composable
private fun PendingEmailCard(
    pendingEmail: String,
    busy: Boolean,
    onEnterCode: () -> Unit,
    onCancel: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.Schedule,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(18.dp)
                )
                Text(
                    text = "Waiting on a code",
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "We sent six digits to $pendingEmail. Your address changes " +
                    "once you hand them back.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(14.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                NebButton(
                    text = "Enter code",
                    onClick = onEnterCode,
                    size = NebButtonSize.Small
                )
                NebButton(
                    text = "Cancel",
                    onClick = onCancel,
                    tone = NebButtonTone.Outlined,
                    size = NebButtonSize.Small,
                    loading = busy
                )
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Email
// ---------------------------------------------------------------------------

@Composable
private fun EmailFormPanel(
    state: AccountSecurityUiState,
    viewModel: AccountSecurityViewModel
) {
    var newEmail by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    PanelColumn {
        PanelHeader(
            title = "Where should we reach you?",
            body = if (state.email.isBlank()) {
                "This address signs you in and resets your password, so we'll " +
                    "confirm it with a code before it takes effect."
            } else {
                "Your account uses ${state.email}. We'll send a code to the new " +
                    "address and only switch once it comes back."
            }
        )

        SecurityField(
            value = newEmail,
            onValueChange = { newEmail = it },
            label = "New email",
            placeholder = "you@example.com",
            keyboardType = KeyboardType.Email,
            enabled = !state.busy
        )

        if (state.hasPassword) {
            SecurityField(
                value = password,
                onValueChange = { password = it },
                label = "Current password",
                isPassword = true,
                enabled = !state.busy
            )
        }

        InlineError(state.error)

        NebButton(
            text = "Send code",
            onClick = { viewModel.requestEmailChange(newEmail, password) },
            enabled = newEmail.isNotBlank() && (!state.hasPassword || password.isNotBlank()),
            loading = state.busy,
            fillWidth = true
        )

        if (state.hasPassword) {
            NebButton(
                text = "I forgot my password",
                onClick = viewModel::startForgotPassword,
                tone = NebButtonTone.Text,
                size = NebButtonSize.Small,
                enabled = !state.busy
            )
        }
    }
}

@Composable
private fun EmailCodePanel(
    state: AccountSecurityUiState,
    viewModel: AccountSecurityViewModel
) {
    var code by remember { mutableStateOf("") }

    LaunchedEffect(state.pendingEmail) {
        if (state.pendingEmail.isBlank()) viewModel.back()
    }

    PanelColumn {
        PanelHeader(
            title = "Enter the code",
            body = "Six digits are on their way to ${state.pendingEmail}. " +
                "They're good for ten minutes."
        )

        CodeField(
            code = code,
            onCodeChange = {
                code = it
                if (it.length == CODE_LENGTH) viewModel.confirmEmailChange(it)
            },
            enabled = !state.busy,
            hasError = state.error != null
        )

        InlineError(state.error)

        NebButton(
            text = "Confirm",
            onClick = { viewModel.confirmEmailChange(code) },
            enabled = code.length == CODE_LENGTH,
            loading = state.busy,
            fillWidth = true
        )

        ResendRow(
            codeSentAt = state.codeSentAt,
            enabled = !state.busy,
            onResend = { code = ""; viewModel.resendEmailCode() }
        )

        NebButton(
            text = "Cancel this change",
            onClick = viewModel::cancelEmailChange,
            tone = NebButtonTone.Text,
            size = NebButtonSize.Small,
            enabled = !state.busy
        )
    }
}

// ---------------------------------------------------------------------------
// Password
// ---------------------------------------------------------------------------

@Composable
private fun PasswordPanel(
    state: AccountSecurityUiState,
    viewModel: AccountSecurityViewModel
) {
    var current by remember { mutableStateOf("") }
    var next by remember { mutableStateOf("") }
    var confirm by remember { mutableStateOf("") }

    PanelColumn {
        PanelHeader(
            title = if (state.hasPassword) "Pick a new password" else "Pick a password",
            body = if (state.hasPassword) {
                "Eight characters or more. You'll stay signed in here."
            } else {
                "Your account signs in without one today. Setting one gives you a " +
                    "second way back in."
            }
        )

        if (state.hasPassword) {
            SecurityField(
                value = current,
                onValueChange = { current = it },
                label = "Current password",
                isPassword = true,
                enabled = !state.busy
            )
        }

        SecurityField(
            value = next,
            onValueChange = { next = it },
            label = "New password",
            isPassword = true,
            enabled = !state.busy,
            supportingText = "At least 8 characters"
        )

        SecurityField(
            value = confirm,
            onValueChange = { confirm = it },
            label = "Repeat new password",
            isPassword = true,
            enabled = !state.busy,
            isError = confirm.isNotEmpty() && confirm != next
        )

        InlineError(state.error)

        NebButton(
            text = if (state.hasPassword) "Change password" else "Set password",
            onClick = { viewModel.submitPassword(current, next, confirm) },
            enabled = next.isNotBlank() && confirm.isNotBlank() &&
                (!state.hasPassword || current.isNotBlank()),
            loading = state.busy,
            fillWidth = true
        )

        if (state.hasPassword) {
            NebButton(
                text = "I forgot my current password",
                onClick = viewModel::startForgotPassword,
                tone = NebButtonTone.Text,
                size = NebButtonSize.Small,
                enabled = !state.busy
            )
        }
    }
}

@Composable
private fun ForgotPanel(
    state: AccountSecurityUiState,
    viewModel: AccountSecurityViewModel
) {
    var code by remember { mutableStateOf("") }
    var next by remember { mutableStateOf("") }
    var confirm by remember { mutableStateOf("") }

    PanelColumn {
        PanelHeader(
            title = "Reset it with a code",
            body = "We sent six digits to ${state.email.ifBlank { "your email" }}. " +
                "Enter them with the password you'd like instead."
        )

        CodeField(
            code = code,
            onCodeChange = { code = it },
            enabled = !state.busy,
            hasError = state.error != null
        )

        SecurityField(
            value = next,
            onValueChange = { next = it },
            label = "New password",
            isPassword = true,
            enabled = !state.busy,
            supportingText = "At least 8 characters"
        )

        SecurityField(
            value = confirm,
            onValueChange = { confirm = it },
            label = "Repeat new password",
            isPassword = true,
            enabled = !state.busy,
            isError = confirm.isNotEmpty() && confirm != next
        )

        InlineError(state.error)

        NebButton(
            text = "Reset password",
            onClick = { viewModel.submitForgotReset(code, next, confirm) },
            enabled = code.length == CODE_LENGTH && next.isNotBlank() && confirm.isNotBlank(),
            loading = state.busy,
            fillWidth = true
        )

        ResendRow(
            codeSentAt = state.codeSentAt,
            enabled = !state.busy,
            onResend = { code = ""; viewModel.startForgotPassword() }
        )
    }
}

// ---------------------------------------------------------------------------
// Pieces
// ---------------------------------------------------------------------------

/** Every panel is the same column: 20dp of air, 16dp gutters. */
@Composable
private fun PanelColumn(content: @Composable () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        content()
    }
}

@Composable
private fun PanelHeader(title: String, body: String) {
    Column {
        Text(
            text = title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = body,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun SecurityField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    placeholder: String? = null,
    isPassword: Boolean = false,
    keyboardType: KeyboardType = KeyboardType.Text,
    enabled: Boolean = true,
    isError: Boolean = false,
    supportingText: String? = null
) {
    var revealed by remember { mutableStateOf(false) }

    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.fillMaxWidth(),
        enabled = enabled,
        isError = isError,
        singleLine = true,
        label = { Text(text = label, style = MaterialTheme.typography.bodyMedium) },
        placeholder = placeholder?.let {
            {
                Text(
                    text = it,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                )
            }
        },
        supportingText = supportingText?.let {
            {
                Text(
                    text = it,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        },
        visualTransformation = if (!isPassword || revealed) {
            VisualTransformation.None
        } else {
            PasswordVisualTransformation()
        },
        keyboardOptions = KeyboardOptions(
            keyboardType = if (isPassword) KeyboardType.Password else keyboardType
        ),
        trailingIcon = if (!isPassword) null else {
            {
                IconButton(onClick = { revealed = !revealed }) {
                    Icon(
                        imageVector = if (revealed) {
                            Icons.Outlined.VisibilityOff
                        } else {
                            Icons.Outlined.Visibility
                        },
                        contentDescription = if (revealed) "Hide password" else "Show password",
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        },
        textStyle = MaterialTheme.typography.bodyLarge,
        shape = RoundedCornerShape(18.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHighest,
            unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHighest,
            focusedBorderColor = MaterialTheme.colorScheme.onSurface,
            unfocusedBorderColor = Color.Transparent,
            focusedLabelColor = MaterialTheme.colorScheme.onSurface,
            unfocusedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    )
}

/**
 * Six cells over one invisible field. The keyboard types into the field; the
 * cells are only ever a picture of what it holds.
 */
@Composable
private fun CodeField(
    code: String,
    onCodeChange: (String) -> Unit,
    enabled: Boolean,
    hasError: Boolean
) {
    Box(modifier = Modifier.fillMaxWidth()) {
        BasicTextField(
            value = code,
            onValueChange = { raw ->
                val digits = raw.filter { it.isDigit() }.take(CODE_LENGTH)
                if (digits != code) onCodeChange(digits)
            },
            enabled = enabled,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
            cursorBrush = SolidColor(Color.Transparent),
            textStyle = TextStyle(color = Color.Transparent),
            modifier = Modifier
                .fillMaxWidth()
                .height(58.dp)
                .alpha(0.01f)
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            repeat(CODE_LENGTH) { index ->
                CodeCell(
                    digit = code.getOrNull(index),
                    active = code.length == index,
                    hasError = hasError,
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

@Composable
private fun CodeCell(
    digit: Char?,
    active: Boolean,
    hasError: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val borderColor by animateColorAsState(
        targetValue = when {
            hasError -> scheme.error
            active -> scheme.onSurface
            digit != null -> scheme.outline
            else -> Color.Transparent
        },
        animationSpec = nebFastEffectsSpec(),
        label = "security_code_border"
    )

    Box(
        modifier = modifier
            .height(58.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(scheme.surfaceContainerHighest)
            .border(
                width = if (active || hasError) 1.6.dp else 1.dp,
                color = borderColor,
                shape = RoundedCornerShape(16.dp)
            ),
        contentAlignment = Alignment.Center
    ) {
        if (digit != null) {
            Text(
                text = digit.toString(),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.SemiBold,
                fontSize = 22.sp,
                color = scheme.onSurface
            )
        } else {
            Box(
                modifier = Modifier
                    .size(width = 12.dp, height = 2.dp)
                    .clip(RoundedCornerShape(1.dp))
                    .background(scheme.outlineVariant)
            )
        }
    }
}

/** A minute between codes, counted down out loud so nobody taps into a 429. */
@Composable
private fun ResendRow(
    codeSentAt: Long,
    enabled: Boolean,
    onResend: () -> Unit
) {
    var remaining by remember(codeSentAt) {
        val elapsed = ((System.currentTimeMillis() - codeSentAt) / 1000L).toInt()
        mutableIntStateOf((RESEND_COOLDOWN_SECONDS - elapsed).coerceIn(0, RESEND_COOLDOWN_SECONDS))
    }

    LaunchedEffect(codeSentAt, remaining) {
        if (remaining > 0) {
            delay(1000)
            remaining--
        }
    }

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Center,
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (remaining > 0) {
            Text(
                text = "You can ask for another code in ${remaining}s",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            NebButton(
                text = "Resend code",
                onClick = onResend,
                tone = NebButtonTone.Text,
                size = NebButtonSize.Small,
                enabled = enabled
            )
        }
    }
}

@Composable
private fun InlineError(message: String?) {
    if (message.isNullOrBlank()) return
    Text(
        text = message,
        style = MaterialTheme.typography.bodyMedium,
        color = MaterialTheme.colorScheme.error
    )
}

private enum class NoticeTone { Good, Bad }

@Composable
private fun NoticeCard(text: String, tone: NoticeTone) {
    val scheme = MaterialTheme.colorScheme
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(
            containerColor = when (tone) {
                NoticeTone.Good -> scheme.surfaceContainerHigh
                NoticeTone.Bad -> scheme.errorContainer
            }
        )
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Icon(
                imageVector = when (tone) {
                    NoticeTone.Good -> Icons.Outlined.CheckCircle
                    NoticeTone.Bad -> Icons.Outlined.ErrorOutline
                },
                contentDescription = null,
                tint = when (tone) {
                    NoticeTone.Good -> scheme.onSurface
                    NoticeTone.Bad -> scheme.onErrorContainer
                },
                modifier = Modifier.size(18.dp)
            )
            Text(
                text = text,
                style = MaterialTheme.typography.bodyMedium,
                color = when (tone) {
                    NoticeTone.Good -> scheme.onSurface
                    NoticeTone.Bad -> scheme.onErrorContainer
                }
            )
        }
    }
}

@Composable
private fun FootNote(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.padding(horizontal = 22.dp)
    )
}
