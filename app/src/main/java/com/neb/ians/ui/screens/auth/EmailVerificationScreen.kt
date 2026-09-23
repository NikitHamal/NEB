package com.neb.ians.ui.screens.auth

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.MarkEmailRead
import androidx.compose.material.icons.outlined.Timer
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.view.WindowCompat
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import com.neb.ians.ui.theme.Poppins
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/**
 * Clean Light-Mode OTP Verification Screen for NEBians.
 *
 * Requirements fulfilled:
 * - Rendered strictly in light mode consistent with splash and auth screens.
 * - Masks email local part hiding all characters except the first and last before the @domain (e.g. i***********l@gmail.com).
 * - Allows code resend at most 3 times.
 * - After 1st resend: 2 minutes cooldown.
 * - After 2nd resend: 2 minutes cooldown.
 * - Last (3rd) resend: 3 minutes cooldown.
 * - Beautiful segmented 6-digit pin cells with auto-submit and Poppins typography.
 */
@Composable
fun EmailVerificationScreen(
    email: String,
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateBack: () -> Unit
) {
    var otpText by remember { mutableStateOf(TextFieldValue("")) }
    var isLoading by remember { mutableStateOf(false) }
    var isResending by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var infoMessage by remember { mutableStateOf<String?>(null) }

    // Resend tracking: maximum 3 resends allowed
    val maxResends = 3
    var resendAttempts by remember { mutableIntStateOf(0) }
    var resendCooldown by remember { mutableIntStateOf(59) }

    val focusRequester = remember { FocusRequester() }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    // Ensure status bar and navigation bar have dark icons (light status bar)
    DisposableEffect(Unit) {
        var ctx: Context? = context
        while (ctx is ContextWrapper) {
            if (ctx is Activity) break
            ctx = ctx.baseContext
        }
        val activity = ctx as? Activity
        val window = activity?.window
        if (window != null) {
            val controller = WindowCompat.getInsetsController(window, window.decorView)
            controller.isAppearanceLightStatusBars = true
            controller.isAppearanceLightNavigationBars = true
        }
        onDispose {}
    }

    // Live countdown timer
    LaunchedEffect(resendCooldown) {
        if (resendCooldown > 0) {
            delay(1000)
            resendCooldown--
        }
    }

    // Auto-focus OTP input on launch
    LaunchedEffect(Unit) {
        delay(300)
        try {
            focusRequester.requestFocus()
        } catch (_: Exception) {}
    }

    // Verification handler
    val performVerification: (String) -> Unit = { codeToVerify ->
        if (codeToVerify.length == 6 && !isLoading) {
            scope.launch {
                isLoading = true
                errorMessage = null
                infoMessage = null
                when (val result = authRepository.emailVerify(email, codeToVerify)) {
                    is EmailAuthResult.VerifySuccess -> {
                        if (result.isNewUser) {
                            onNavigateToCompleteProfile()
                        } else {
                            onNavigateToHome()
                        }
                    }
                    is EmailAuthResult.Failure -> {
                        errorMessage = result.message
                        isLoading = false
                    }
                    else -> {
                        errorMessage = "Invalid verification code. Please check and try again."
                        isLoading = false
                    }
                }
            }
        }
    }

    // Auto-submit when user reaches 6 digits
    LaunchedEffect(otpText.text) {
        if (otpText.text.length == 6) {
            performVerification(otpText.text)
        }
    }

    // Clean, crisp Light Theme Palette matching Splash & Auth screens
    val primaryBrand = Color(0xFF0D5CE5)      // NEBians Sapphire Blue
    val primaryContainer = Color(0xFFDBE5FF)
    val bgColor = Color(0xFFF8F9FD)           // Off-white canvas
    val surfaceColor = Color(0xFFFFFFFF)      // Pure white cards
    val textPrimary = Color(0xFF0F172A)       // Slate 900
    val textSecondary = Color(0xFF64748B)     // Slate 500
    val borderColor = Color(0xFFE2E8F0)       // Slate 200

    val maskedEmail = remember(email) { maskEmail(email) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .statusBarsPadding()
            .navigationBarsPadding()
            .imePadding()
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Top Navigation Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 12.dp, bottom = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    onClick = onNavigateBack,
                    shape = CircleShape,
                    color = surfaceColor,
                    border = androidx.compose.foundation.BorderStroke(1.dp, borderColor),
                    modifier = Modifier.size(42.dp),
                    shadowElevation = 1.dp
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = textPrimary,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Security Badge Icon with Dual-Tone Light Glow
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.size(80.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(RoundedCornerShape(26.dp))
                        .background(
                            Brush.linearGradient(
                                colors = listOf(
                                    primaryContainer.copy(alpha = 0.8f),
                                    Color(0xFFE0EDFF)
                                )
                            )
                        )
                )
                Icon(
                    imageVector = Icons.Outlined.MarkEmailRead,
                    contentDescription = null,
                    tint = primaryBrand,
                    modifier = Modifier.size(38.dp)
                )
            }

            Spacer(modifier = Modifier.height(22.dp))

            // Headline
            Text(
                text = "Verify your email",
                fontFamily = Poppins,
                fontWeight = FontWeight.SemiBold,
                fontSize = 25.sp,
                letterSpacing = (-0.4).sp,
                color = textPrimary,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Subtitle
            Text(
                text = "We sent a 6-digit verification code to",
                fontFamily = Poppins,
                fontWeight = FontWeight.Medium,
                fontSize = 14.sp,
                color = textSecondary,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(10.dp))

            // Email Chip with masked email (all letters hidden except first and last before @domain)
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = surfaceColor,
                border = androidx.compose.foundation.BorderStroke(1.dp, borderColor),
                shadowElevation = 0.5.dp,
                onClick = onNavigateBack
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = maskedEmail,
                        fontFamily = Poppins,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = primaryBrand
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Icon(
                        imageVector = Icons.Outlined.Edit,
                        contentDescription = "Edit email",
                        tint = textSecondary,
                        modifier = Modifier.size(14.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Error Message Banner (if any)
            AnimatedVisibility(
                visible = errorMessage != null,
                enter = fadeIn() + slideInVertically(),
                exit = fadeOut()
            ) {
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = Color(0xFFFEE2E2),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFFCA5A5)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 20.dp)
                ) {
                    Text(
                        text = errorMessage ?: "",
                        fontFamily = Poppins,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFFB91C1C),
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)
                    )
                }
            }

            // Info Message Banner (e.g. resend success)
            AnimatedVisibility(
                visible = infoMessage != null,
                enter = fadeIn() + slideInVertically(),
                exit = fadeOut()
            ) {
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = Color(0xFFE0F2FE),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFBAE6FD)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 20.dp)
                ) {
                    Text(
                        text = infoMessage ?: "",
                        fontFamily = Poppins,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFF0369A1),
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp)
                    )
                }
            }

            // SEGMENTED 6-DIGIT OTP PIN INPUT
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(
                        interactionSource = remember { MutableInteractionSource() },
                        indication = null
                    ) {
                        focusRequester.requestFocus()
                    }
            ) {
                // Hidden Native Text Field handling keyboard input & paste
                BasicTextField(
                    value = otpText,
                    onValueChange = { newText ->
                        val digits = newText.text.filter { it.isDigit() }.take(6)
                        otpText = newText.copy(
                            text = digits,
                            selection = androidx.compose.ui.text.TextRange(digits.length)
                        )
                        errorMessage = null
                        infoMessage = null
                    },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
                    modifier = Modifier
                        .focusRequester(focusRequester)
                        .size(1.dp)
                )

                // 6 Distinct Visual Cells
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val codeString = otpText.text
                    for (i in 0 until 6) {
                        val isFocusedCell = i == codeString.length
                        val isFilled = i < codeString.length
                        val digit = codeString.getOrNull(i)?.toString() ?: ""

                        OtpDigitCell(
                            digit = digit,
                            isFocused = isFocusedCell && !isLoading,
                            isFilled = isFilled,
                            isError = errorMessage != null,
                            primaryBrand = primaryBrand,
                            surfaceColor = surfaceColor,
                            textPrimary = textPrimary
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Primary Verify & Continue Button
            Button(
                onClick = { performVerification(otpText.text) },
                enabled = otpText.text.length == 6 && !isLoading,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
                    .testTag("verify_otp_button"),
                shape = RoundedCornerShape(27.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = primaryBrand,
                    contentColor = Color.White,
                    disabledContainerColor = primaryBrand.copy(alpha = 0.45f),
                    disabledContentColor = Color.White.copy(alpha = 0.7f)
                ),
                elevation = ButtonDefaults.buttonElevation(
                    defaultElevation = 2.dp,
                    pressedElevation = 4.dp
                )
            ) {
                if (isLoading) {
                    CircularProgressIndicator(
                        color = Color.White,
                        modifier = Modifier.size(22.dp),
                        strokeWidth = 2.5.dp
                    )
                } else {
                    Text(
                        text = "Verify Code",
                        fontFamily = Poppins,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold,
                        letterSpacing = 0.2.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Resend Code Logic with Strict 3-Attempts Limit and 2m / 3m Cooldowns
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (resendCooldown > 0) {
                    Row(
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Timer,
                            contentDescription = null,
                            tint = textSecondary,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "Resend code in ${formatCooldown(resendCooldown)}",
                            fontFamily = Poppins,
                            fontSize = 14.sp,
                            color = textSecondary,
                            fontWeight = FontWeight.Medium
                        )
                    }

                    if (resendAttempts > 0) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Resend attempt $resendAttempts of $maxResends",
                            fontFamily = Poppins,
                            fontSize = 12.sp,
                            color = textSecondary.copy(alpha = 0.8f)
                        )
                    }
                } else {
                    if (resendAttempts < maxResends) {
                        Row(
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "Didn't receive the code? ",
                                fontFamily = Poppins,
                                fontSize = 14.sp,
                                color = textSecondary
                            )
                            Text(
                                text = if (isResending) "Sending..." else "Resend Code (${maxResends - resendAttempts} left)",
                                fontFamily = Poppins,
                                fontSize = 14.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = if (isResending) textSecondary else primaryBrand,
                                modifier = Modifier.clickable(enabled = !isResending) {
                                    scope.launch {
                                        isResending = true
                                        errorMessage = null
                                        infoMessage = null
                                        when (val result = authRepository.emailResendCode(email)) {
                                            is EmailAuthResult.Message -> {
                                                val nextAttempt = resendAttempts + 1
                                                resendAttempts = nextAttempt
                                                // After one resend: 2 mins (120s). Last resend (3rd): 3 mins (180s).
                                                resendCooldown = when (nextAttempt) {
                                                    1 -> 120 // 2 mins
                                                    2 -> 120 // 2 mins
                                                    else -> 180 // 3 mins for last resend
                                                }
                                                infoMessage = "A new verification code has been sent."
                                            }
                                            is EmailAuthResult.Failure -> {
                                                errorMessage = result.message
                                            }
                                            else -> {
                                                val nextAttempt = resendAttempts + 1
                                                resendAttempts = nextAttempt
                                                resendCooldown = when (nextAttempt) {
                                                    1 -> 120
                                                    2 -> 120
                                                    else -> 180
                                                }
                                                infoMessage = "A new verification code has been sent."
                                            }
                                        }
                                        isResending = false
                                    }
                                }
                            )
                        }
                    } else {
                        // Max resends reached (3 of 3)
                        Text(
                            text = "Maximum resends reached (3/3). Please check your spam folder or return to check your email.",
                            fontFamily = Poppins,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Medium,
                            color = textSecondary,
                            textAlign = TextAlign.Center,
                            modifier = Modifier.padding(horizontal = 12.dp)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(36.dp))

            // Pro-grade security hint
            Surface(
                shape = RoundedCornerShape(14.dp),
                color = surfaceColor,
                border = androidx.compose.foundation.BorderStroke(1.dp, borderColor),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "Tip: Please check your spam or junk folder if you do not see the message in your inbox within a few minutes.",
                    fontFamily = Poppins,
                    fontSize = 12.5.sp,
                    color = textSecondary,
                    textAlign = TextAlign.Center,
                    lineHeight = 18.sp,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 14.dp)
                )
            }
        }
    }
}

/**
 * Masks the email string by hiding all characters of the local username part
 * except the first and last before the @domain (e.g. iamnikithamal@gmail.com -> i***********l@gmail.com).
 */
private fun maskEmail(email: String): String {
    if (email.isBlank()) return "your email"
    val atIndex = email.indexOf('@')
    if (atIndex <= 0) return email
    val localPart = email.substring(0, atIndex)
    val domainPart = email.substring(atIndex)

    val maskedLocal = when {
        localPart.length > 2 -> {
            val first = localPart.first()
            val last = localPart.last()
            val maskedMiddle = "*".repeat(localPart.length - 2)
            "$first$maskedMiddle$last"
        }
        localPart.length == 2 -> "${localPart.first()}*${localPart.last()}"
        else -> "$localPart*"
    }
    return "$maskedLocal$domainPart"
}

/**
 * Format seconds into mm:ss or ss string.
 */
private fun formatCooldown(seconds: Int): String {
    val mins = seconds / 60
    val secs = seconds % 60
    return if (mins > 0) {
        String.format("%d:%02d", mins, secs)
    } else {
        "${secs}s"
    }
}

/**
 * Individual segmented digit box for industry-grade OTP inputs in clean light mode.
 */
@Composable
private fun OtpDigitCell(
    digit: String,
    isFocused: Boolean,
    isFilled: Boolean,
    isError: Boolean,
    primaryBrand: Color,
    surfaceColor: Color,
    textPrimary: Color
) {
    val infiniteTransition = rememberInfiniteTransition(label = "cursor")
    val cursorAlpha by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(500, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "cursorAlpha"
    )

    val scaleAnim by animateFloatAsState(
        targetValue = if (isFilled) 1.05f else 1f,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy),
        label = "digitScale"
    )

    val borderColor = when {
        isError -> Color(0xFFEF4444)
        isFocused -> primaryBrand
        isFilled -> Color(0xFF93C5FD)
        else -> Color(0xFFE2E8F0)
    }

    val cellBackground = when {
        isFocused -> Color(0xFFF0F6FF)
        isFilled -> surfaceColor
        else -> surfaceColor
    }

    Box(
        modifier = Modifier
            .size(width = 48.dp, height = 60.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(cellBackground)
            .border(
                width = if (isFocused || isError) 2.dp else 1.2.dp,
                color = borderColor,
                shape = RoundedCornerShape(14.dp)
            ),
        contentAlignment = Alignment.Center
    ) {
        if (isFilled) {
            Text(
                text = digit,
                fontFamily = Poppins,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = textPrimary,
                modifier = Modifier.scale(scaleAnim)
            )
        } else if (isFocused) {
            // Blinking cursor bar for active empty cell
            Box(
                modifier = Modifier
                    .width(2.dp)
                    .height(24.dp)
                    .background(primaryBrand.copy(alpha = cursorAlpha))
            )
        }
    }
}

