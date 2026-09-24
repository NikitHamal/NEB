package com.neb.ians.ui.screens.auth

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import com.neb.ians.ui.components.NebArtSlot
import com.neb.ians.ui.components.NebAuthTopBar
import com.neb.ians.ui.components.NebAuthType
import com.neb.ians.ui.components.NebInlineNote
import com.neb.ians.ui.components.NebJourneySurface
import com.neb.ians.ui.components.NebNoteTone
import com.neb.ians.ui.components.NebPillButton
import com.neb.ians.ui.components.NebStepHeader
import com.neb.ians.ui.components.NebTextLink
import com.neb.ians.ui.components.nebKeyboardOpen
import com.neb.ians.ui.components.art.NebCodeInFlightArt
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebFastEffectsSpec
import com.neb.ians.ui.theme.nebFastSpatialSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.ui.theme.Poppins
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

private const val CODE_LENGTH = 6
private const val MAX_RESENDS = 3

/**
 * The last gate before the journey. One illustration carries the code from the
 * envelope into the slip as the digits land, so progress is visible without a
 * single extra label. Resends stay capped at three with the same cooldown
 * ladder the backend expects.
 */
@Composable
fun EmailVerificationScreen(
    email: String,
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToOnboarding: () -> Unit,
    onNavigateBack: () -> Unit
) {
    val scope = rememberCoroutineScope()
    val focusRequester = remember { FocusRequester() }

    var code by remember { mutableStateOf(TextFieldValue("")) }
    var isVerifying by remember { mutableStateOf(false) }
    var isResending by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var infoMessage by remember { mutableStateOf<String?>(null) }
    var resendAttempts by remember { mutableIntStateOf(0) }
    var resendCooldown by remember { mutableIntStateOf(59) }

    val maskedEmail = remember(email) { maskEmail(email) }
    val artHeight by animateDpAsState(
        targetValue = if (nebKeyboardOpen()) 108.dp else 160.dp,
        animationSpec = nebSpatialSpec(),
        label = "neb_verify_art"
    )

    LaunchedEffect(resendCooldown) {
        if (resendCooldown > 0) {
            delay(1000)
            resendCooldown--
        }
    }

    LaunchedEffect(Unit) {
        delay(320)
        runCatching { focusRequester.requestFocus() }
    }

    fun verify(value: String) {
        if (value.length != CODE_LENGTH || isVerifying) return
        scope.launch {
            isVerifying = true
            errorMessage = null
            infoMessage = null
            when (val result = authRepository.emailVerify(email, value)) {
                is EmailAuthResult.VerifySuccess -> {
                    if (result.isNewUser) onNavigateToOnboarding() else onNavigateToHome()
                }
                is EmailAuthResult.Failure -> {
                    errorMessage = result.message
                    code = TextFieldValue("")
                    isVerifying = false
                }
                else -> {
                    errorMessage = "That code didn't match. Check your inbox and try again."
                    code = TextFieldValue("")
                    isVerifying = false
                }
            }
        }
    }

    fun resend() {
        if (isResending || resendAttempts >= MAX_RESENDS || resendCooldown > 0) return
        scope.launch {
            isResending = true
            errorMessage = null
            infoMessage = null
            val result = authRepository.emailResendCode(email)
            if (result is EmailAuthResult.Failure) {
                errorMessage = result.message
            } else {
                resendAttempts += 1
                resendCooldown = if (resendAttempts >= MAX_RESENDS) 180 else 120
                infoMessage = "A fresh code is on its way."
            }
            isResending = false
        }
    }

    LaunchedEffect(code.text) {
        if (code.text.length == CODE_LENGTH) verify(code.text)
    }

    NebJourneySurface {
        NebAuthTopBar(onBack = onNavigateBack)

        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = NebAuthTokens.PageGutter),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            NebArtSlot(collapseOnKeyboard = false) {
                NebCodeInFlightArt(
                    filledCount = code.text.length,
                    total = CODE_LENGTH,
                    height = artHeight
                )
            }

            Spacer(modifier = Modifier.height(18.dp))

            NebStepHeader(
                title = "Check your inbox",
                subtitle = "We sent a six digit code to $maskedEmail. Enter it below and you're in.",
                align = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(6.dp))

            NebTextLink(text = "Use a different email", onClick = onNavigateBack)

            Spacer(modifier = Modifier.height(NebAuthTokens.SectionGap))

            CodeInput(
                value = code,
                onValueChange = { next ->
                    val digits = next.text.filter { it.isDigit() }.take(CODE_LENGTH)
                    code = TextFieldValue(digits, selection = androidx.compose.ui.text.TextRange(digits.length))
                    if (errorMessage != null) errorMessage = null
                },
                enabled = !isVerifying,
                hasError = errorMessage != null,
                focusRequester = focusRequester
            )

            Spacer(modifier = Modifier.height(18.dp))

            NebInlineNote(text = errorMessage, tone = NebNoteTone.Error)
            NebInlineNote(text = infoMessage, tone = NebNoteTone.Success)

            Spacer(modifier = Modifier.height(14.dp))

            NebPillButton(
                text = "Verify",
                onClick = { verify(code.text) },
                enabled = code.text.length == CODE_LENGTH && !isVerifying,
                loading = isVerifying
            )

            Spacer(modifier = Modifier.height(20.dp))

            ResendRow(
                attempts = resendAttempts,
                cooldown = resendCooldown,
                isResending = isResending,
                onResend = { resend() }
            )

            Spacer(modifier = Modifier.height(28.dp))
        }
    }
}

@Composable
private fun CodeInput(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    enabled: Boolean,
    hasError: Boolean,
    focusRequester: FocusRequester
) {
    val palette = LocalNebAuthPalette.current
    Box(modifier = Modifier.fillMaxWidth()) {
        BasicTextField(
            value = value,
            onValueChange = onValueChange,
            enabled = enabled,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(Color.Transparent),
            textStyle = TextStyle(color = Color.Transparent),
            modifier = Modifier
                .fillMaxWidth()
                .height(62.dp)
                .alpha(0.01f)
                .focusRequester(focusRequester)
        )
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(9.dp)
        ) {
            repeat(CODE_LENGTH) { index ->
                CodeCell(
                    digit = value.text.getOrNull(index),
                    active = value.text.length == index,
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
    val palette = LocalNebAuthPalette.current
    val borderColor by animateColorAsState(
        targetValue = when {
            hasError -> palette.danger
            active -> palette.accent
            digit != null -> palette.hairlineStrong
            else -> palette.hairline
        },
        animationSpec = nebFastEffectsSpec(),
        label = "neb_code_border"
    )
    val scale by animateFloatAsState(
        targetValue = if (digit != null) 1f else 0.94f,
        animationSpec = nebFastSpatialSpec(),
        label = "neb_code_scale"
    )
    Box(
        modifier = modifier
            .height(62.dp)
            .clip(RoundedCornerShape(NebAuthTokens.FieldRadius))
            .background(if (digit != null) palette.accentSoft else palette.field)
            .border(
                width = if (active || hasError) 1.6.dp else NebAuthTokens.Hairline,
                color = borderColor,
                shape = RoundedCornerShape(NebAuthTokens.FieldRadius)
            ),
        contentAlignment = Alignment.Center
    ) {
        if (digit != null) {
            Text(
                text = digit.toString(),
                fontFamily = Poppins,
                fontWeight = FontWeight.SemiBold,
                fontSize = 22.sp,
                color = palette.ink,
                modifier = Modifier.graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                }
            )
        } else {
            Box(
                modifier = Modifier
                    .size(width = 14.dp, height = 2.dp)
                    .clip(RoundedCornerShape(1.dp))
                    .background(palette.hairlineStrong)
            )
        }
    }
}

@Composable
private fun ResendRow(
    attempts: Int,
    cooldown: Int,
    isResending: Boolean,
    onResend: () -> Unit
) {
    val palette = LocalNebAuthPalette.current
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        when {
            attempts >= MAX_RESENDS && cooldown > 0 -> Text(
                text = "Last code sent. You can try again in ${formatCooldown(cooldown)}.",
                style = NebAuthType.Caption,
                color = palette.inkMuted,
                textAlign = TextAlign.Center
            )
            attempts >= MAX_RESENDS -> Text(
                text = "No resends left. Go back and start again if the code never arrived.",
                style = NebAuthType.Caption,
                color = palette.inkMuted,
                textAlign = TextAlign.Center
            )
            cooldown > 0 -> Text(
                text = "Resend available in ${formatCooldown(cooldown)}",
                style = NebAuthType.Caption,
                color = palette.inkMuted
            )
            else -> Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "Didn't get it?",
                    style = NebAuthType.Caption,
                    color = palette.inkMuted
                )
                Spacer(modifier = Modifier.width(2.dp))
                NebTextLink(
                    text = if (isResending) "Sending" else "Resend code",
                    onClick = onResend,
                    enabled = !isResending
                )
            }
        }
        if (attempts in 1 until MAX_RESENDS) {
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "${MAX_RESENDS - attempts} of $MAX_RESENDS resends left",
                style = NebAuthType.Caption,
                color = palette.inkFaint
            )
        }
    }
}

private fun maskEmail(email: String): String {
    if (email.isBlank()) return "your email"
    val atIndex = email.indexOf('@')
    if (atIndex <= 0) return email
    val localPart = email.substring(0, atIndex)
    val domainPart = email.substring(atIndex)
    val maskedLocal = when {
        localPart.length > 2 -> "${localPart.first()}${"*".repeat(localPart.length - 2)}${localPart.last()}"
        localPart.length == 2 -> "${localPart.first()}*${localPart.last()}"
        else -> "$localPart*"
    }
    return "$maskedLocal$domainPart"
}

private fun formatCooldown(seconds: Int): String {
    val mins = seconds / 60
    val secs = seconds % 60
    return if (mins > 0) String.format("%d:%02d", mins, secs) else "${secs}s"
}
