package com.neb.ians.ui.screens.auth

import android.app.Activity
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Pin
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.core.view.WindowCompat
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthTopBar
import com.neb.ians.ui.components.NebInlineNote
import com.neb.ians.ui.components.NebNoteTone
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebStepHeader
import com.neb.ians.ui.components.NebTextLink
import com.neb.ians.ui.components.art.NebCodeInFlightArt
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.NebMotion
import com.neb.ians.ui.theme.rememberNebAuthPalette
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/**
 * Two phases on one surface: ask for the address, then take the code and the new
 * password. The header and the fields cross-fade in place rather than pushing the
 * user to a second destination, which matches the sign-in screen next door.
 */
@Composable
fun ForgotPasswordScreen(
    initialEmail: String,
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateBack: () -> Unit
) {
    val palette = rememberNebAuthPalette()
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    var email by remember { mutableStateOf(initialEmail) }
    var code by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var codeSent by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var isResending by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var infoMessage by remember { mutableStateOf<String?>(null) }
    var resendCooldown by remember { mutableIntStateOf(0) }

    DisposableEffect(palette.isDark) {
        val window = (context as? Activity)?.window
        val previous = window?.let {
            WindowCompat.getInsetsController(it, it.decorView).isAppearanceLightStatusBars
        }
        window?.let {
            WindowCompat.getInsetsController(it, it.decorView).isAppearanceLightStatusBars = !palette.isDark
        }
        onDispose {
            if (window != null && previous != null) {
                WindowCompat.getInsetsController(window, window.decorView).isAppearanceLightStatusBars = previous
            }
        }
    }

    LaunchedEffect(resendCooldown) {
        if (resendCooldown > 0) {
            delay(1000)
            resendCooldown--
        }
    }

    val emailLooksValid = email.contains("@") && email.contains(".")
    val canSendCode = emailLooksValid && !isLoading
    val canReset = code.length >= 4 &&
        newPassword.length >= 8 &&
        newPassword == confirmPassword &&
        !isLoading

    fun sendCode(resend: Boolean) {
        scope.launch {
            if (resend) isResending = true else isLoading = true
            errorMessage = null
            infoMessage = null
            val result = authRepository.emailForgotPassword(email)
            if (result is EmailAuthResult.Failure) {
                errorMessage = result.message
            } else {
                codeSent = true
                resendCooldown = 60
                if (resend) infoMessage = "A fresh code is on its way."
            }
            isLoading = false
            isResending = false
        }
    }

    fun resetPassword() {
        scope.launch {
            isLoading = true
            errorMessage = null
            infoMessage = null
            when (val result = authRepository.emailResetPassword(email, code, newPassword)) {
                is EmailAuthResult.ResetSuccess -> onNavigateToHome()
                is EmailAuthResult.Failure -> {
                    errorMessage = result.message
                    isLoading = false
                }
                else -> {
                    errorMessage = "That didn't work. Check the code and try again."
                    isLoading = false
                }
            }
        }
    }

    CompositionLocalProvider(LocalNebAuthPalette provides palette) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(palette.page)
                .statusBarsPadding()
                .navigationBarsPadding()
                .imePadding()
        ) {
            NebAuthTopBar(onBack = onNavigateBack)

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = NebAuthTokens.PageGutter),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                NebCodeInFlightArt(filledCount = if (codeSent) code.length else 0, total = 6)

                Spacer(modifier = Modifier.height(16.dp))

                AnimatedContent(
                    targetState = codeSent,
                    transitionSpec = { phaseTransition(targetState) },
                    label = "neb_forgot_header"
                ) { sent ->
                    NebStepHeader(
                        title = if (sent) "Set a new password" else "Reset your password",
                        subtitle = if (sent) {
                            "Enter the code we emailed you, then choose a password of at least eight characters."
                        } else {
                            "Tell us the email on your account and we'll send a reset code."
                        },
                        align = TextAlign.Center
                    )
                }

                Spacer(modifier = Modifier.height(NebAuthTokens.SectionGap))

                NebAuthField(
                    value = email,
                    onValueChange = { email = it; errorMessage = null },
                    label = "Email",
                    placeholder = "you@example.com",
                    leadingIcon = Icons.Outlined.AlternateEmail,
                    keyboardType = KeyboardType.Email,
                    imeAction = ImeAction.Next,
                    enabled = !codeSent && !isLoading
                )

                AnimatedVisibility(
                    visible = codeSent,
                    enter = fadeIn(tween(NebMotion.Standard)),
                    exit = fadeOut(tween(NebMotion.Quick))
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))
                        NebAuthField(
                            value = code,
                            onValueChange = { code = it.filter { c -> c.isDigit() }.take(6); errorMessage = null },
                            label = "Reset code",
                            placeholder = "123456",
                            leadingIcon = Icons.Outlined.Pin,
                            keyboardType = KeyboardType.NumberPassword,
                            imeAction = ImeAction.Next
                        )
                        Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))
                        NebAuthField(
                            value = newPassword,
                            onValueChange = { newPassword = it; errorMessage = null },
                            label = "New password",
                            placeholder = "At least 8 characters",
                            leadingIcon = Icons.Outlined.Lock,
                            isPassword = true,
                            imeAction = ImeAction.Next,
                            helper = if (newPassword.isNotEmpty() && newPassword.length < 8) "8 characters minimum" else null
                        )
                        Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))
                        NebAuthField(
                            value = confirmPassword,
                            onValueChange = { confirmPassword = it; errorMessage = null },
                            label = "Confirm password",
                            placeholder = "Type it once more",
                            leadingIcon = Icons.Outlined.Lock,
                            isPassword = true,
                            imeAction = ImeAction.Done,
                            onImeAction = { if (canReset) resetPassword() },
                            error = if (confirmPassword.isNotEmpty() && confirmPassword != newPassword) {
                                "Those don't match yet"
                            } else {
                                null
                            }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(18.dp))

                NebInlineNote(text = errorMessage, tone = NebNoteTone.Error)
                NebInlineNote(text = infoMessage, tone = NebNoteTone.Success)

                Spacer(modifier = Modifier.height(12.dp))

                AnimatedContent(
                    targetState = codeSent,
                    transitionSpec = { phaseTransition(targetState) },
                    label = "neb_forgot_action"
                ) { sent ->
                    NebPillButton(
                        text = if (sent) "Reset password" else "Send reset code",
                        onClick = { if (sent) resetPassword() else sendCode(resend = false) },
                        enabled = if (sent) canReset else canSendCode,
                        loading = isLoading
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                AnimatedVisibility(
                    visible = codeSent,
                    enter = fadeIn(tween(NebMotion.Standard)),
                    exit = fadeOut(tween(NebMotion.Instant))
                ) {
                    if (resendCooldown > 0) {
                        Text(
                            text = "You can request another code in ${resendCooldown}s",
                            style = NebAuthType.Caption,
                            color = palette.inkMuted
                        )
                    } else {
                        NebTextLink(
                            text = if (isResending) "Sending" else "Send another code",
                            onClick = { sendCode(resend = true) },
                            enabled = !isResending
                        )
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }
}

private fun phaseTransition(toSent: Boolean) =
    (slideInVertically(tween(NebMotion.Standard, easing = NebMotion.Decelerate)) {
        if (toSent) it / 3 else -it / 3
    } + fadeIn(tween(NebMotion.Standard))) togetherWith
        (slideOutVertically(tween(NebMotion.Short, easing = NebMotion.Accelerate)) {
            if (toSent) -it / 3 else it / 3
        } + fadeOut(tween(NebMotion.Quick)))
