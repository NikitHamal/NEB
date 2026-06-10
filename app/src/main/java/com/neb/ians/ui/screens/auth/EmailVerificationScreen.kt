package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EmailVerificationScreen(
    email: String,
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateBack: () -> Unit
) {
    var code by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var isResending by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var resendCooldown by remember { mutableStateOf(0) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(resendCooldown) {
        if (resendCooldown > 0) {
            delay(1000)
            resendCooldown--
        }
    }

    // Dynamic luminance-based theme check
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

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(cardColor)
            .statusBarsPadding()
            .navigationBarsPadding(),
        contentAlignment = Alignment.TopCenter
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp, vertical = 28.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Header: Back
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    modifier = Modifier.clickable { onNavigateBack() },
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.Default.ArrowBack,
                        contentDescription = "Back",
                        tint = webPrimary,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "Back",
                        fontSize = 15.sp,
                        color = webPrimary,
                        fontWeight = FontWeight.Medium
                    )
                }
            }

            Text(
                text = "Verify your email",
                fontSize = 28.sp,
                fontWeight = FontWeight.Bold,
                color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(6.dp))

            Text(
                text = "We sent a 6-digit verification code to $email",
                fontSize = 14.sp,
                color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF434655),
                textAlign = TextAlign.Center
            )

            if (errorMessage != null) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = errorMessage!!,
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Code Label & Input
            Column(modifier = Modifier.fillMaxWidth()) {
                Text(
                    text = "Verification code",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                )
                Spacer(modifier = Modifier.height(6.dp))
                OutlinedTextField(
                    value = code,
                    onValueChange = { input -> code = input.filter { it.isDigit() }.take(6) },
                    placeholder = { Text("000000", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF), maxLines = 1, overflow = TextOverflow.Ellipsis) },
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
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Verify & Continue Button
            Button(
                onClick = {
                    scope.launch {
                        isLoading = true
                        errorMessage = null
                        when (val result = authRepository.emailVerify(email, code)) {
                            is EmailAuthResult.VerifySuccess -> {
                                if (result.isNewUser) {
                                    onNavigateToCompleteProfile()
                                } else {
                                    onNavigateToHome()
                                }
                            }
                            is EmailAuthResult.Failure -> {
                                errorMessage = result.message
                            }
                            else -> {
                                errorMessage = "Verification failed. Please try again."
                            }
                        }
                        isLoading = false
                    }
                },
                enabled = code.length == 6 && !isLoading,
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
                        text = "Verify & continue",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        fontSize = 16.sp
                    )
                }
            }

            Spacer(modifier = Modifier.height(28.dp))

            // Footer Resend
            Row(
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "Didn't get a code? ",
                    fontSize = 14.sp,
                    color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF434655)
                )
                val resendText = if (resendCooldown > 0) "Resend in ${resendCooldown}s" else "Resend"
                Text(
                    text = resendText,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (resendCooldown > 0 || isResending) Color(0xFF737686) else webPrimary,
                    modifier = Modifier.clickable(enabled = resendCooldown == 0 && !isResending) {
                        scope.launch {
                            isResending = true
                            errorMessage = null
                            when (val result = authRepository.emailResendCode(email)) {
                                is EmailAuthResult.Message -> {
                                    resendCooldown = 60
                                }
                                is EmailAuthResult.Failure -> {
                                    errorMessage = result.message
                                }
                                else -> {}
                            }
                            isResending = false
                        }
                    }
                )
            }
        }
    }
}