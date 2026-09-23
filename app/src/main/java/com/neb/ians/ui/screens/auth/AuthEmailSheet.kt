package com.neb.ians.ui.screens.auth

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.Mail
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.util.TactileType
import com.neb.ians.util.rememberTactileFeedback
import kotlinx.coroutines.launch

/**
 * Revamped Auth Email Bottom Sheet for NEBians.
 *
 * Implements:
 * - App-consistent color palette (NEBians Sapphire Blue #0D5CE5, clean surfaces, slate text).
 * - Poppins typography (600 for bolds/titles/buttons, 500 for normal/inputs).
 * - Segmented tab switcher with high contrast and smooth visual states.
 * - Dedicated form fields for Sign In vs Register (Full name / username, email, password).
 * - Clear validation, loading state, and tactile feedback.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthEmailSheet(
    isOpen: Boolean,
    onDismiss: () -> Unit,
    isDark: Boolean,
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateToForgotPassword: (email: String) -> Unit,
    onNavigateToVerification: (email: String) -> Unit,
    onNavigateToFullSignup: () -> Unit
) {
    if (!isOpen) return

    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val scope = rememberCoroutineScope()
    val focusManager = LocalFocusManager.current
    val tactile = rememberTactileFeedback()

    var isLoginMode by remember { mutableStateOf(true) }

    // Sign In inputs
    var loginIdentifier by remember { mutableStateOf("") }

    // Register inputs
    var registerUsername by remember { mutableStateOf("") }
    var registerEmail by remember { mutableStateOf("") }

    // Shared password
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }

    var errorMessage by remember { mutableStateOf<String?>(null) }
    var isSubmitting by remember { mutableStateOf(false) }

    // Consistent NEBians color palette
    val brandSapphire = Color(0xFF0D5CE5)
    val brandSapphireContainer = Color(0xFFEBF2FE)
    val sheetBgColor = if (isDark) Color(0xFF131722) else Color(0xFFFFFFFF)
    val surfaceContainerColor = if (isDark) Color(0xFF1C2333) else Color(0xFFF1F5F9)
    val textPrimary = if (isDark) Color(0xFFF1F5F9) else Color(0xFF0F172A)
    val textSecondary = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)
    val fieldBorderColor = if (isDark) Color(0xFF2E384D) else Color(0xFFE2E8F0)
    val fieldBgColor = if (isDark) Color(0xFF181F2E) else Color(0xFFF8FAFC)

    fun performSubmit() {
        focusManager.clearFocus()

        if (isLoginMode) {
            val identifier = loginIdentifier.trim()
            val pass = password.trim()

            if (identifier.isEmpty() || pass.isEmpty()) {
                errorMessage = "Please enter both your email/username and password."
                tactile.perform(TactileType.Warning)
                return
            }

            errorMessage = null
            isSubmitting = true
            tactile.perform(TactileType.ButtonTap)

            scope.launch {
                try {
                    val result = authRepository.emailLogin(identifier, pass)
                    when (result) {
                        is EmailAuthResult.LoginSuccess -> {
                            tactile.perform(TactileType.Success)
                            onDismiss()
                            if (result.isNewUser) {
                                onNavigateToCompleteProfile()
                            } else {
                                onNavigateToHome()
                            }
                        }
                        is EmailAuthResult.Failure -> {
                            tactile.perform(TactileType.Warning)
                            errorMessage = result.message
                            if (result.message.contains("verify", ignoreCase = true) && identifier.contains("@")) {
                                onDismiss()
                                onNavigateToVerification(identifier)
                            }
                        }
                        else -> {
                            errorMessage = "Unexpected response. Please try again."
                        }
                    }
                } catch (e: Exception) {
                    errorMessage = e.message ?: "Authentication error occurred."
                } finally {
                    isSubmitting = false
                }
            }
        } else {
            // Register Mode
            val email = registerEmail.trim()
            val uname = registerUsername.trim().ifBlank {
                if (email.contains("@")) email.substringBefore("@") else email
            }
            val pass = password.trim()

            if (email.isEmpty() || pass.isEmpty()) {
                errorMessage = "Please enter your email and choose a password."
                tactile.perform(TactileType.Warning)
                return
            }

            if (!email.contains("@") || !email.contains(".")) {
                errorMessage = "Please enter a valid email address."
                tactile.perform(TactileType.Warning)
                return
            }

            if (pass.length < 8) {
                errorMessage = "Password must be at least 8 characters long."
                tactile.perform(TactileType.Warning)
                return
            }

            errorMessage = null
            isSubmitting = true
            tactile.perform(TactileType.ButtonTap)

            scope.launch {
                try {
                    val result = authRepository.emailSignup(
                        email = email,
                        password = pass,
                        username = uname,
                        role = "student"
                    )
                    when (result) {
                        is EmailAuthResult.SignupSuccess -> {
                            tactile.perform(TactileType.Success)
                            onDismiss()
                            onNavigateToVerification(email)
                        }
                        is EmailAuthResult.Failure -> {
                            tactile.perform(TactileType.Warning)
                            errorMessage = result.message
                        }
                        else -> {
                            errorMessage = "Signup failed. Please try again."
                        }
                    }
                } catch (e: Exception) {
                    errorMessage = e.message ?: "Registration error occurred."
                } finally {
                    isSubmitting = false
                }
            }
        }
    }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = sheetBgColor,
        contentColor = textPrimary,
        shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
        dragHandle = {
            BottomSheetDefaults.DragHandle(
                color = if (isDark) Color(0xFF334155) else Color(0xFFCBD5E1)
            )
        }
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp)
                .padding(bottom = 36.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Mode Switcher Tabs (Sign In vs Register)
            Surface(
                shape = RoundedCornerShape(24.dp),
                color = surfaceContainerColor,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Sign In Tab
                    Surface(
                        onClick = {
                            if (!isLoginMode) {
                                isLoginMode = true
                                errorMessage = null
                                tactile.perform(TactileType.SelectionChange)
                            }
                        },
                        shape = RoundedCornerShape(20.dp),
                        color = if (isLoginMode) sheetBgColor else Color.Transparent,
                        shadowElevation = if (isLoginMode) 1.5.dp else 0.dp,
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = "Sign In",
                                fontFamily = Poppins,
                                fontWeight = if (isLoginMode) FontWeight.SemiBold else FontWeight.Medium,
                                fontSize = 14.5.sp,
                                color = if (isLoginMode) brandSapphire else textSecondary
                            )
                        }
                    }

                    // Register Tab
                    Surface(
                        onClick = {
                            if (isLoginMode) {
                                isLoginMode = false
                                errorMessage = null
                                tactile.perform(TactileType.SelectionChange)
                            }
                        },
                        shape = RoundedCornerShape(20.dp),
                        color = if (!isLoginMode) sheetBgColor else Color.Transparent,
                        shadowElevation = if (!isLoginMode) 1.5.dp else 0.dp,
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Text(
                                text = "Create Account",
                                fontFamily = Poppins,
                                fontWeight = if (!isLoginMode) FontWeight.SemiBold else FontWeight.Medium,
                                fontSize = 14.5.sp,
                                color = if (!isLoginMode) brandSapphire else textSecondary
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Header Icon Badge
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(52.dp)
                    .clip(RoundedCornerShape(18.dp))
                    .background(if (isDark) Color(0xFF1E283D) else brandSapphireContainer)
            ) {
                Icon(
                    imageVector = if (isLoginMode) Icons.Outlined.Lock else Icons.Outlined.School,
                    contentDescription = null,
                    tint = brandSapphire,
                    modifier = Modifier.size(26.dp)
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Title
            Text(
                text = if (isLoginMode) "Welcome Back" else "Join NEBians",
                fontFamily = Poppins,
                fontWeight = FontWeight.SemiBold,
                fontSize = 22.sp,
                color = textPrimary,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(4.dp))

            // Subtitle
            Text(
                text = if (isLoginMode) {
                    "Sign in with your email or username to continue"
                } else {
                    "Create your student account to access resources & forum"
                },
                fontFamily = Poppins,
                fontWeight = FontWeight.Medium,
                fontSize = 13.5.sp,
                color = textSecondary,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 8.dp)
            )

            Spacer(modifier = Modifier.height(20.dp))

            // Error Banner
            AnimatedVisibility(
                visible = errorMessage != null,
                enter = fadeIn() + slideInVertically(),
                exit = fadeOut()
            ) {
                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = Color(0xFFFEE2E2),
                    border = BorderStroke(1.dp, Color(0xFFFCA5A5)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 14.dp)
                ) {
                    Text(
                        text = errorMessage ?: "",
                        fontFamily = Poppins,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFFB91C1C),
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)
                    )
                }
            }

            // Input Fields
            if (isLoginMode) {
                // SIGN IN: Email or Username
                OutlinedTextField(
                    value = loginIdentifier,
                    onValueChange = {
                        loginIdentifier = it
                        if (errorMessage != null) errorMessage = null
                    },
                    label = {
                        Text(
                            text = "Email or Username",
                            fontFamily = Poppins,
                            fontWeight = FontWeight.Medium
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Mail,
                            contentDescription = null,
                            tint = textSecondary
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("auth_email_input"),
                    shape = RoundedCornerShape(16.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Email,
                        imeAction = ImeAction.Next
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = brandSapphire,
                        unfocusedBorderColor = fieldBorderColor,
                        focusedContainerColor = fieldBgColor,
                        unfocusedContainerColor = fieldBgColor,
                        focusedTextColor = textPrimary,
                        unfocusedTextColor = textPrimary
                    )
                )

                Spacer(modifier = Modifier.height(12.dp))

                // SIGN IN: Password
                OutlinedTextField(
                    value = password,
                    onValueChange = {
                        password = it
                        if (errorMessage != null) errorMessage = null
                    },
                    label = {
                        Text(
                            text = "Password",
                            fontFamily = Poppins,
                            fontWeight = FontWeight.Medium
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Lock,
                            contentDescription = null,
                            tint = textSecondary
                        )
                    },
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                imageVector = if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = if (passwordVisible) "Hide password" else "Show password",
                                tint = textSecondary
                            )
                        }
                    },
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("auth_password_input"),
                    shape = RoundedCornerShape(16.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Password,
                        imeAction = ImeAction.Done
                    ),
                    keyboardActions = KeyboardActions(onDone = { performSubmit() }),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = brandSapphire,
                        unfocusedBorderColor = fieldBorderColor,
                        focusedContainerColor = fieldBgColor,
                        unfocusedContainerColor = fieldBgColor,
                        focusedTextColor = textPrimary,
                        unfocusedTextColor = textPrimary
                    )
                )

                // Forgot Password Link
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp, bottom = 12.dp),
                    horizontalArrangement = Arrangement.End
                ) {
                    Text(
                        text = "Forgot password?",
                        fontFamily = Poppins,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 13.5.sp,
                        color = brandSapphire,
                        modifier = Modifier
                            .clickable {
                                onDismiss()
                                onNavigateToForgotPassword(loginIdentifier.trim())
                            }
                            .padding(4.dp)
                            .testTag("forgot_password_button")
                    )
                }
            } else {
                // REGISTER: Username
                OutlinedTextField(
                    value = registerUsername,
                    onValueChange = {
                        registerUsername = it
                        if (errorMessage != null) errorMessage = null
                    },
                    label = {
                        Text(
                            text = "Username",
                            fontFamily = Poppins,
                            fontWeight = FontWeight.Medium
                        )
                    },
                    placeholder = {
                        Text(
                            text = "e.g. sushant12",
                            fontFamily = Poppins,
                            color = textSecondary.copy(alpha = 0.6f)
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Person,
                            contentDescription = null,
                            tint = textSecondary
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("auth_username_input"),
                    shape = RoundedCornerShape(16.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Text,
                        imeAction = ImeAction.Next
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = brandSapphire,
                        unfocusedBorderColor = fieldBorderColor,
                        focusedContainerColor = fieldBgColor,
                        unfocusedContainerColor = fieldBgColor,
                        focusedTextColor = textPrimary,
                        unfocusedTextColor = textPrimary
                    )
                )

                Spacer(modifier = Modifier.height(12.dp))

                // REGISTER: Email Address
                OutlinedTextField(
                    value = registerEmail,
                    onValueChange = {
                        registerEmail = it
                        if (errorMessage != null) errorMessage = null
                    },
                    label = {
                        Text(
                            text = "Email Address",
                            fontFamily = Poppins,
                            fontWeight = FontWeight.Medium
                        )
                    },
                    placeholder = {
                        Text(
                            text = "e.g. yourname@gmail.com",
                            fontFamily = Poppins,
                            color = textSecondary.copy(alpha = 0.6f)
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Mail,
                            contentDescription = null,
                            tint = textSecondary
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("auth_email_input"),
                    shape = RoundedCornerShape(16.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Email,
                        imeAction = ImeAction.Next
                    ),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = brandSapphire,
                        unfocusedBorderColor = fieldBorderColor,
                        focusedContainerColor = fieldBgColor,
                        unfocusedContainerColor = fieldBgColor,
                        focusedTextColor = textPrimary,
                        unfocusedTextColor = textPrimary
                    )
                )

                Spacer(modifier = Modifier.height(12.dp))

                // REGISTER: Password
                OutlinedTextField(
                    value = password,
                    onValueChange = {
                        password = it
                        if (errorMessage != null) errorMessage = null
                    },
                    label = {
                        Text(
                            text = "Password (min 8 characters)",
                            fontFamily = Poppins,
                            fontWeight = FontWeight.Medium
                        )
                    },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Outlined.Lock,
                            contentDescription = null,
                            tint = textSecondary
                        )
                    },
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                imageVector = if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = if (passwordVisible) "Hide password" else "Show password",
                                tint = textSecondary
                            )
                        }
                    },
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("auth_password_input"),
                    shape = RoundedCornerShape(16.dp),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Password,
                        imeAction = ImeAction.Done
                    ),
                    keyboardActions = KeyboardActions(onDone = { performSubmit() }),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = brandSapphire,
                        unfocusedBorderColor = fieldBorderColor,
                        focusedContainerColor = fieldBgColor,
                        unfocusedContainerColor = fieldBgColor,
                        focusedTextColor = textPrimary,
                        unfocusedTextColor = textPrimary
                    )
                )

                Spacer(modifier = Modifier.height(16.dp))
            }

            // Primary Submit Button
            Button(
                onClick = { performSubmit() },
                enabled = !isSubmitting,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
                    .testTag("auth_submit_button"),
                shape = RoundedCornerShape(27.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = brandSapphire,
                    contentColor = Color.White,
                    disabledContainerColor = brandSapphire.copy(alpha = 0.5f),
                    disabledContentColor = Color.White.copy(alpha = 0.7f)
                ),
                elevation = ButtonDefaults.buttonElevation(
                    defaultElevation = 1.dp,
                    pressedElevation = 3.dp
                )
            ) {
                if (isSubmitting) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(22.dp),
                        color = Color.White,
                        strokeWidth = 2.dp
                    )
                } else {
                    Text(
                        text = if (isLoginMode) "Sign In" else "Create Account",
                        fontFamily = Poppins,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 16.sp,
                        letterSpacing = 0.2.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Switch Mode Prompt
            Row(
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = if (isLoginMode) "Don't have an account? " else "Already have an account? ",
                    fontFamily = Poppins,
                    fontSize = 14.sp,
                    color = textSecondary
                )
                Text(
                    text = if (isLoginMode) "Create one" else "Sign In",
                    fontFamily = Poppins,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 14.sp,
                    color = brandSapphire,
                    modifier = Modifier.clickable {
                        isLoginMode = !isLoginMode
                        errorMessage = null
                        tactile.perform(TactileType.SelectionChange)
                    }
                )
            }

            if (!isLoginMode) {
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = "Prefer full student profile registration? Tap here",
                    fontFamily = Poppins,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Medium,
                    color = brandSapphire,
                    modifier = Modifier
                        .clickable {
                            onDismiss()
                            onNavigateToFullSignup()
                        }
                        .padding(4.dp)
                )
            }
        }
    }
}

