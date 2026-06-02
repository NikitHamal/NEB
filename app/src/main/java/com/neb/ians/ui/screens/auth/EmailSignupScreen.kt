package com.neb.ians.ui.screens.auth

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.EmailAuthResult
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EmailSignupScreen(
    authRepository: AuthRepository,
    onNavigateToVerification: (email: String) -> Unit,
    onNavigateBack: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }
    var confirmPasswordVisible by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()

    val isFormValid = email.isNotBlank() && username.length >= 3 && password.length >= 8 && password == confirmPassword

    val isDark = isSystemInDarkTheme()
    val bgGradient = if (isDark) {
        Brush.linearGradient(listOf(Color(0xFF0A0A0C), Color(0xFF16161A)))
    } else {
        Brush.linearGradient(listOf(Color(0xFFF5F6FA), Color(0xFFEBEEF5)))
    }
    val cardColor = if (isDark) Color(0xFF131316) else Color(0xFFFFFFFF)
    val inputBg = if (isDark) Color(0xFF1C1C20) else Color(0xFFFFFFFF)
    val inputBorder = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgGradient)
            .systemBarsPadding(),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .clip(RoundedCornerShape(24.dp))
                .background(cardColor)
                .padding(32.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Start
            ) {
                IconButton(onClick = onNavigateBack, modifier = Modifier.offset(x = (-16).dp, y = (-16).dp)) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }

            Text(
                text = "Sign Up",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Create an account using your email.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            OutlinedTextField(
                value = username,
                onValueChange = { username = it.trim() },
                label = { Text("Username") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(10.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = inputBg,
                    focusedContainerColor = inputBg,
                    unfocusedBorderColor = inputBorder,
                ),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text)
            )

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = email,
                onValueChange = { email = it.trim() },
                label = { Text("Email") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(10.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = inputBg,
                    focusedContainerColor = inputBg,
                    unfocusedBorderColor = inputBorder,
                ),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
            )

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                trailingIcon = {
                    IconButton(onClick = { passwordVisible = !passwordVisible }) {
                        Icon(
                            painter = androidx.compose.ui.res.painterResource(
                                id = if (passwordVisible) com.neb.ians.R.drawable.ic_visibility_off else com.neb.ians.R.drawable.ic_visibility
                            ),
                            contentDescription = null
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
                ),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)
            )

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("Confirm Password") },
                trailingIcon = {
                    IconButton(onClick = { confirmPasswordVisible = !confirmPasswordVisible }) {
                        Icon(
                            painter = androidx.compose.ui.res.painterResource(
                                id = if (confirmPasswordVisible) com.neb.ians.R.drawable.ic_visibility_off else com.neb.ians.R.drawable.ic_visibility
                            ),
                            contentDescription = null
                        )
                    }
                },
                singleLine = true,
                visualTransformation = if (confirmPasswordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(10.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = inputBg,
                    focusedContainerColor = inputBg,
                    unfocusedBorderColor = inputBorder,
                ),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                isError = confirmPassword.isNotBlank() && password != confirmPassword,
                supportingText = {
                    if (confirmPassword.isNotBlank() && password != confirmPassword) {
                        Text("Passwords don't match", color = MaterialTheme.colorScheme.error)
                    }
                }
            )

            if (errorMessage != null) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = errorMessage!!,
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.bodySmall
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    scope.launch {
                        isLoading = true
                        errorMessage = null
                        when (val result = authRepository.emailSignup(email, password, username)) {
                            is EmailAuthResult.SignupSuccess -> {
                                onNavigateToVerification(email)
                            }
                            is EmailAuthResult.Failure -> {
                                errorMessage = result.message
                            }
                            else -> {
                                errorMessage = "Unexpected error"
                            }
                        }
                        isLoading = false
                    }
                },
                enabled = isFormValid && !isLoading,
                modifier = Modifier.fillMaxWidth().height(48.dp),
                shape = RoundedCornerShape(10.dp)
            ) {
                if (isLoading) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(24.dp))
                } else {
                    Text("Create Account", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                }
            }
        }
    }
}