package com.neb.ians.ui.screens.auth

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FiniteAnimationSpec
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowForward
import androidx.compose.material.icons.outlined.AlternateEmail
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.ui.components.NebArtSlot
import com.neb.ians.ui.components.NebAuthField
import com.neb.ians.ui.components.NebAuthTopBar
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebInlineNote
import com.neb.ians.ui.components.NebJourneySurface
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.NebTextLink
import com.neb.ians.ui.components.art.NebOpenBookMark
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec

/**
 * One screen for both halves of email auth. Signing in and creating an account
 * ask for the same two things, so they are the same two fields — only the
 * headline, the helper, the primary action and the footer cross-fade between
 * them, and whatever the user has already typed survives the switch.
 */
@Composable
fun EmailAuthScreen(
    onClose: () -> Unit,
    onNavigateToHome: () -> Unit,
    onNavigateToOnboarding: () -> Unit,
    onNavigateToVerification: (email: String) -> Unit,
    onNavigateToForgotPassword: (email: String) -> Unit,
    startInCreateMode: Boolean = false,
    viewModel: EmailAuthViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val focusManager = LocalFocusManager.current

    LaunchedEffect(startInCreateMode) {
        if (startInCreateMode) viewModel.setMode(EmailAuthMode.CreateAccount)
    }

    LaunchedEffect(uiState.event) {
        when (val event = uiState.event) {
            EmailAuthEvent.GoHome -> {
                viewModel.consumeEvent()
                onNavigateToHome()
            }
            EmailAuthEvent.GoOnboarding -> {
                viewModel.consumeEvent()
                onNavigateToOnboarding()
            }
            is EmailAuthEvent.GoVerify -> {
                viewModel.consumeEvent()
                onNavigateToVerification(event.email)
            }
            is EmailAuthEvent.GoForgotPassword -> {
                viewModel.consumeEvent()
                onNavigateToForgotPassword(event.email)
            }
            null -> Unit
        }
    }

    val isCreate = uiState.mode == EmailAuthMode.CreateAccount

    NebJourneySurface {
        val palette = LocalNebAuthPalette.current
        NebAuthTopBar(onClose = onClose)

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = NebAuthTokens.PageGutter)
        ) {
            NebArtSlot {
                NebOpenBookMark(
                    modifier = Modifier.fillMaxWidth(),
                    markSize = 78.dp
                )
            }
            val modeSlide = nebSpatialSpec<IntOffset>()
            val modeFade = nebEffectsSpec<Float>()

            Spacer(modifier = Modifier.height(18.dp))

            AnimatedContent(
                targetState = isCreate,
                transitionSpec = { modeTransition(targetState, modeSlide, modeFade) },
                label = "neb_email_auth_header"
            ) { create ->
                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = if (create) "Create your account" else "Welcome back",
                        style = NebAuthType.Headline,
                        color = palette.ink
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = if (create) {
                            "Your email and a password is all we need to start. You will pick a handle next."
                        } else {
                            "Sign in with the email or username you registered with."
                        },
                        style = NebAuthType.Body,
                        color = palette.inkMuted
                    )
                }
            }

            Spacer(modifier = Modifier.height(NebAuthTokens.SectionGap))

            NebAuthField(
                value = uiState.identifier,
                onValueChange = viewModel::onIdentifierChange,
                label = if (isCreate) "Email address" else "Email or username",
                placeholder = if (isCreate) "you@example.com" else "you@example.com",
                leadingIcon = Icons.Outlined.AlternateEmail,
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next,
                onImeAction = { focusManager.moveFocus(androidx.compose.ui.focus.FocusDirection.Down) },
                enabled = !uiState.isSubmitting,
                error = uiState.identifierError
            )

            Spacer(modifier = Modifier.height(NebAuthTokens.StackGap))

            NebAuthField(
                value = uiState.password,
                onValueChange = viewModel::onPasswordChange,
                label = "Password",
                placeholder = if (isCreate) "At least 8 characters" else "Your password",
                leadingIcon = Icons.Outlined.Lock,
                isPassword = true,
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done,
                onImeAction = {
                    focusManager.clearFocus()
                    viewModel.submit()
                },
                enabled = !uiState.isSubmitting,
                error = uiState.passwordError,
                helper = if (isCreate && uiState.password.isNotEmpty() && uiState.password.length < 8) {
                    "${8 - uiState.password.length} more characters"
                } else {
                    null
                }
            )

            AnimatedVisibility(
                visible = !isCreate,
                enter = fadeIn(nebEffectsSpec()),
                exit = fadeOut(nebEffectsSpec())
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    NebTextLink(
                        text = "Forgot password?",
                        onClick = viewModel::requestForgotPassword,
                        enabled = !uiState.isSubmitting
                    )
                }
            }

            Spacer(modifier = Modifier.height(if (isCreate) 22.dp else 10.dp))

            NebInlineNote(text = uiState.formError)

            Spacer(modifier = Modifier.height(18.dp))

            AnimatedContent(
                targetState = isCreate,
                transitionSpec = { modeTransition(targetState, modeSlide, modeFade) },
                label = "neb_email_auth_action"
            ) { create ->
                NebPillButton(
                    text = if (create) "Create account" else "Sign in",
                    onClick = {
                        focusManager.clearFocus()
                        viewModel.submit()
                    },
                    enabled = uiState.canSubmit,
                    loading = uiState.isSubmitting,
                    trailingIcon = Icons.AutoMirrored.Outlined.ArrowForward
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            AnimatedContent(
                targetState = isCreate,
                transitionSpec = { modeTransition(targetState, modeSlide, modeFade) },
                label = "neb_email_auth_footer"
            ) { create ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = if (create) "Already a NEBian?" else "New to NEBians?",
                        style = NebAuthType.Body,
                        color = palette.inkMuted
                    )
                    Spacer(modifier = Modifier.width(2.dp))
                    NebTextLink(
                        text = if (create) "Sign in" else "Create account",
                        onClick = {
                            focusManager.clearFocus()
                            viewModel.toggleMode()
                        },
                        enabled = !uiState.isSubmitting
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = if (isCreate) {
                    "We will email you a six digit code to confirm it is really you."
                } else {
                    "Not verified yet? Signing in sends you straight to the code screen."
                },
                style = NebAuthType.Caption,
                color = palette.inkFaint,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

/**
 * The switch between the two modes. Create rises from below, sign in drops back
 * down — the same spatial logic in both directions, so the user can feel which
 * way they just moved.
 */
private fun modeTransition(
    toCreate: Boolean,
    slide: FiniteAnimationSpec<IntOffset>,
    fade: FiniteAnimationSpec<Float>
) = (slideInVertically(
    animationSpec = slide,
    initialOffsetY = { if (toCreate) it / 3 else -it / 3 }
) + fadeIn(fade)) togetherWith
    (slideOutVertically(
        animationSpec = slide,
        targetOffsetY = { if (toCreate) -it / 3 else it / 3 }
    ) + fadeOut(fade))
