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
import androidx.compose.material.icons.filled.Backpack
import androidx.compose.material.icons.filled.HistoryEdu
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.TravelExplore
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
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
    val scope = rememberCoroutineScope()

    // Screen state: 1 = Role Selection, 2 = Account Details
    var currentStep by remember { mutableStateOf(1) }
    var selectedRole by remember { mutableStateOf("student") }

    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }

    var isLoading by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

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

    val isFormValid = email.isNotBlank() && username.length >= 3 && password.length >= 8

    val roleLabel = when (selectedRole) {
        "student" -> "Student"
        "teacher" -> "Teacher"
        "institution" -> "Institution"
        "explorer" -> "Explorer"
        else -> "Student"
    }

    val roleDescription = when (selectedRole) {
        "student" -> "Create your student account to get started."
        "teacher" -> "Create your teacher account to get started."
        "institution" -> "Create your institution account to get started."
        "explorer" -> "Create your explorer account to get started."
        else -> "Create your student account to get started."
    }

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
            // Header: Back Button & Step Transition
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    modifier = Modifier.clickable {
                        if (currentStep == 2) {
                            currentStep = 1
                            errorMessage = null
                        } else {
                            onNavigateBack()
                        }
                    },
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

            if (currentStep == 1) {
                // Title
                Text(
                    text = "Create account",
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                    textAlign = TextAlign.Center
                )

                Spacer(modifier = Modifier.height(6.dp))

                Text(
                    text = "Sign up with email — we'll send a verification code.",
                    fontSize = 14.sp,
                    color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF434655),
                    textAlign = TextAlign.Center
                )

                Spacer(modifier = Modifier.height(24.dp))

                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "I am a...",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    )

                    // Role Cards
                    RoleSelectionCard(
                        title = "Student",
                        description = "I'm studying for exams",
                        imageVector = Icons.Filled.Backpack,
                        isDark = isDark,
                        onClick = {
                            selectedRole = "student"
                            currentStep = 2
                        }
                    )

                    RoleSelectionCard(
                        title = "Teacher",
                        description = "I teach and create content",
                        imageVector = Icons.Filled.HistoryEdu,
                        isDark = isDark,
                        onClick = {
                            selectedRole = "teacher"
                            currentStep = 2
                        }
                    )

                    RoleSelectionCard(
                        title = "Institution",
                        description = "School, college, or academy",
                        imageVector = Icons.Filled.AccountBalance,
                        isDark = isDark,
                        onClick = {
                            selectedRole = "institution"
                            currentStep = 2
                        }
                    )

                    // Explorer Section with Divider
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        HorizontalDivider(
                            modifier = Modifier.weight(1f),
                            color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                        )
                        Text(
                            text = "  Or just exploring?  ",
                            fontSize = 13.sp,
                            color = if (isDark) Color(0xFF8D90A1) else Color(0xFF737686)
                        )
                        HorizontalDivider(
                            modifier = Modifier.weight(1f),
                            color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                        )
                    }

                    ExplorerDashedCard(
                        title = "Explorer",
                        description = "Just browsing for now",
                        imageVector = Icons.Filled.TravelExplore,
                        isDark = isDark,
                        onClick = {
                            selectedRole = "explorer"
                            currentStep = 2
                        }
                    )
                }
            } else {
                // Step 2: Account Details Fields
                Text(
                    text = "Join as $roleLabel",
                    fontSize = 28.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30),
                    textAlign = TextAlign.Center
                )

                Spacer(modifier = Modifier.height(6.dp))

                Text(
                    text = roleDescription,
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

                Spacer(modifier = Modifier.height(24.dp))

                // Username Label & Field
                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "Username",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it.trim() },
                        placeholder = { Text("nikit_07", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF), maxLines = 1, overflow = TextOverflow.Ellipsis) },
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
                        )
                    )
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Email Label & Field
                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "Email",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    OutlinedTextField(
                        value = email,
                        onValueChange = { email = it.trim() },
                        placeholder = { Text("hello@example.com", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF), maxLines = 1, overflow = TextOverflow.Ellipsis) },
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

                Spacer(modifier = Modifier.height(14.dp))

                // Password Label & Field
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
                        placeholder = { Text("At least 8 characters", color = if (isDark) Color(0xFF6B7280) else Color(0xFF9CA3AF), maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        trailingIcon = {
                            IconButton(onClick = { passwordVisible = !passwordVisible }) {
                                Icon(
                                    imageVector = if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
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

                Spacer(modifier = Modifier.height(24.dp))

                // Create Account Button
                Button(
                    onClick = {
                        scope.launch {
                            isLoading = true
                            errorMessage = null
                            when (val result = authRepository.emailSignup(email, password, username, selectedRole)) {
                                is EmailAuthResult.SignupSuccess -> {
                                    onNavigateToVerification(email)
                                }
                                is EmailAuthResult.Failure -> {
                                    errorMessage = result.message
                                }
                                else -> {
                                    errorMessage = "Signup failed. Please try again."
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
                            text = "Create account",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 16.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    HorizontalDivider(
                        modifier = Modifier.weight(1f),
                        color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                    )
                    Text(
                        text = "  or  ",
                        fontSize = 13.sp,
                        color = if (isDark) Color(0xFF8D90A1) else Color(0xFF737686)
                    )
                    HorizontalDivider(
                        modifier = Modifier.weight(1f),
                        color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB)
                    )
                }

                Spacer(modifier = Modifier.height(12.dp))

                // "Already have an account? Sign in" Button
                Button(
                    onClick = {
                        onNavigateBack()
                    },
                    modifier = Modifier
                        .fillMaxWidth()
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
                    Text(
                        text = "Already have an account? Sign in",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                // "Change role" Link
                Text(
                    text = "Change role",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = webPrimary,
                    modifier = Modifier.clickable {
                        currentStep = 1
                        errorMessage = null
                    }
                )
            }
        }
    }
}

@Composable
fun RoleSelectionCard(
    title: String,
    description: String,
    imageVector: androidx.compose.ui.graphics.vector.ImageVector,
    isDark: Boolean,
    onClick: () -> Unit
) {
    val bgColor = if (isDark) Color(0xFF181622) else Color(0xFFF1F3F9)
    val borderColor = if (isDark) Color(0xFF2D2A3F) else Color(0xFFDCDFEA)
    val webPrimary = Color(0xFF004AC6)

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(bgColor)
            .border(2.dp, borderColor, RoundedCornerShape(16.dp))
            .clickable { onClick() }
            .padding(horizontal = 18.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = imageVector,
            contentDescription = null,
            tint = webPrimary,
            modifier = Modifier.size(28.dp)
        )
        Spacer(modifier = Modifier.width(14.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = description,
                fontSize = 13.sp,
                color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF737686)
            )
        }
    }
}

@Composable
fun ExplorerDashedCard(
    title: String,
    description: String,
    imageVector: androidx.compose.ui.graphics.vector.ImageVector,
    isDark: Boolean,
    onClick: () -> Unit
) {
    val outlineColor = if (isDark) Color(0xFF8D90A1) else Color(0xFF737686)

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .drawBehind {
                val stroke = Stroke(
                    width = 2.dp.toPx(),
                    pathEffect = PathEffect.dashPathEffect(floatArrayOf(12f, 12f), 0f)
                )
                drawRoundRect(
                    color = outlineColor,
                    style = stroke,
                    cornerRadius = CornerRadius(16.dp.toPx())
                )
            }
            .clickable { onClick() }
            .padding(horizontal = 18.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = imageVector,
            contentDescription = null,
            tint = if (isDark) Color(0xFFEFB8C0) else Color(0xFF7D5260),
            modifier = Modifier.size(28.dp)
        )
        Spacer(modifier = Modifier.width(14.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = if (isDark) Color(0xFFE5EEFF) else Color(0xFF0B1C30)
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = description,
                fontSize = 13.sp,
                color = if (isDark) Color(0xFFC3C6D7) else Color(0xFF737686)
            )
        }
    }
}
