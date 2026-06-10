package com.neb.ians.ui.screens.auth

import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateToEmailSignup: () -> Unit,
    onNavigateToForgotPassword: (email: String) -> Unit,
    onNavigateToVerification: (email: String) -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    var emailOrUsername by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    // Dynamic luminance-based theme check to prevent mismatched dark/light modes
    val isDark = MaterialTheme.colorScheme.background.luminance() < 0.5f

    val bgGradient = if (isDark) {
        Brush.linearGradient(listOf(Color(0xFF0A0A0C), Color(0xFF16161A)))
    } else {
        Brush.linearGradient(listOf(Color(0xFFF5F6FA), Color(0xFFEBEEF5)))
    }

    val cardColor = if (isDark) Color(0xFF131316) else Color(0xFFFFFFFF)
    val inputBg = if (isDark) Color(0xFF1C1C20) else Color(0xFFFFFFFF)
    val inputBorder = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
    val webPrimary = Color(0xFF004AC6)

    val isFormValid = emailOrUsername.isNotBlank() && password.length >= 8

    fun launchOAuth(provider: String) {
        val url = if (provider == "google") {
            "https://nebians.consica.com.np/auth/google/login/?state=mobile_google"
        } else {
            "https://nebians.consica.com.np/auth/github/login/?mobile=1"
        }

        try {
            val customTabsIntent = CustomTabsIntent.Builder().build()
            customTabsIntent.launchUrl(context, Uri.parse(url))
        } catch (e: Exception) {
            errorMessage = "No browser available for sign-in."
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient)
            .statusBarsPadding()
            .navigationBarsPadding(),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp)
                .clip(RoundedCornerShape(24.dp))
                .background(cardColor)
                .border(1.dp, if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB), RoundedCornerShape(24.dp))
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp, vertical = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Welcome Back",
                fontSize = 28.sp,
                fontWeight = FontWeight.Bold,
                color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Enter your email and password to access your account.",
                fontSize = 14.sp,
                color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF434655),
                textAlign = TextAlign.Center
            )

            if (errorMessage != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = errorMessage!!,
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Username or Email label + field
            Column(modifier = Modifier.fillMaxWidth()) {
                Text(
                    text = "Username or email",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                )
                Spacer(modifier = Modifier.height(6.dp))
                OutlinedTextField(
                    value = emailOrUsername,
                    onValueChange = { emailOrUsername = it.trim() },
                    placeholder = { Text("username or hello@example.com", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF)) },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(10.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        unfocusedContainerColor = inputBg,
                        focusedContainerColor = inputBg,
                        unfocusedBorderColor = inputBorder,
                        focusedBorderColor = webPrimary,
                        unfocusedTextColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                        focusedTextColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    ),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Password label + field
            Column(modifier = Modifier.fillMaxWidth()) {
                Text(
                    text = "Password",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                )
                Spacer(modifier = Modifier.height(6.dp))
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    placeholder = { Text("••••••••", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF)) },
                    trailingIcon = {
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                painter = painterResource(
                                    id = if (passwordVisible) com.neb.ians.R.drawable.ic_visibility_off else com.neb.ians.R.drawable.ic_visibility
                                ),
                                contentDescription = null,
                                tint = if (isDark) Color(0xFF8D90A1) else Color(0xFF737686)
                            )
                        }
                    },
                    singleLine = true,
                    visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(10.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        unfocusedContainerColor = inputBg,
                        focusedContainerColor = inputBg,
                        unfocusedBorderColor = inputBorder,
                        focusedBorderColor = webPrimary,
                        unfocusedTextColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                        focusedTextColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    ),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Forgot password? Link
            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.CenterEnd) {
                Text(
                    text = "Forgot password?",
                    fontSize = 14.sp,
                    color = webPrimary,
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.clickable {
                        onNavigateToForgotPassword(emailOrUsername)
                    }
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Log In Button
            Button(
                onClick = {
                    scope.launch {
                        isLoading = true
                        errorMessage = null
                        when (val result = authRepository.emailLogin(emailOrUsername, password)) {
                            is EmailAuthResult.LoginSuccess -> {
                                if (result.isNewUser) {
                                    onNavigateToCompleteProfile()
                                } else {
                                    onNavigateToHome()
                                }
                            }
                            is EmailAuthResult.Failure -> {
                                if (result.message.contains("verify your email", ignoreCase = true)) {
                                    // If verification is needed, trigger verification view
                                    onNavigateToVerification(emailOrUsername)
                                } else {
                                    errorMessage = result.message
                                }
                            }
                            else -> {
                                errorMessage = "Unexpected error occurred."
                            }
                        }
                        isLoading = false
                    }
                },
                enabled = isFormValid && !isLoading,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(10.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = webPrimary,
                    contentColor = Color.White,
                    disabledContainerColor = webPrimary.copy(alpha = 0.5f),
                    disabledContentColor = Color.White.copy(alpha = 0.5f)
                )
            ) {
                if (isLoading) {
                    CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                } else {
                    Text(
                        text = "Log In",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 16.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // "Or login with" Divider
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                HorizontalDivider(
                    modifier = Modifier.weight(1f),
                    color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                )
                Text(
                    text = "  Or login with  ",
                    fontSize = 13.sp,
                    color = if (isDark) Color(0xFF8D90A1) else Color(0xFF737686)
                )
                HorizontalDivider(
                    modifier = Modifier.weight(1f),
                    color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            // Social Row (Google, GitHub side-by-side)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Google OAuth Button
                Button(
                    onClick = {
                        errorMessage = null
                        launchOAuth("google")
                    },
                    modifier = Modifier
                        .weight(1f)
                        .height(48.dp),
                    shape = RoundedCornerShape(10.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isDark) Color(0xFF1C1C20) else Color(0xFFFFFFFF),
                        contentColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    ),
                    border = androidx.compose.foundation.BorderStroke(
                        1.dp,
                        if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                    )
                ) {
                    Image(
                        painter = painterResource(id = com.neb.ians.R.drawable.ic_google),
                        contentDescription = "Google Logo",
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Google",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }

                // GitHub OAuth Button
                Button(
                    onClick = {
                        errorMessage = null
                        launchOAuth("github")
                    },
                    modifier = Modifier
                        .weight(1f)
                        .height(48.dp),
                    shape = RoundedCornerShape(10.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isDark) Color(0xFF1C1C20) else Color(0xFFFFFFFF),
                        contentColor = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    ),
                    border = androidx.compose.foundation.BorderStroke(
                        1.dp,
                        if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                    )
                ) {
                    Icon(
                        painter = painterResource(id = com.neb.ians.R.drawable.ic_github),
                        contentDescription = "GitHub Logo",
                        tint = if (isDark) Color.White else Color.Black,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "GitHub",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Footer (Register link)
            Row(
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "Don't have an account? ",
                    fontSize = 14.sp,
                    color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF434655)
                )
                Text(
                    text = "Register now.",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = webPrimary,
                    modifier = Modifier.clickable {
                        onNavigateToEmailSignup()
                    }
                )
            }
        }
    }
}