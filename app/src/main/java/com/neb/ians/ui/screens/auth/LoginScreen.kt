package com.neb.ians.ui.screens.auth

import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository

@Composable
fun LoginScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateToEmailSignup: () -> Unit = {},
    onNavigateToEmailLogin: () -> Unit = {}
) {
    val context = LocalContext.current
    var errorMessage by remember { mutableStateOf<String?>(null) }

    val isDark = isSystemInDarkTheme()
    val bgGradient = if (isDark) {
        Brush.linearGradient(listOf(Color(0xFF0A0A0C), Color(0xFF16161A)))
    } else {
        Brush.linearGradient(listOf(Color(0xFFF5F6FA), Color(0xFFEBEEF5)))
    }
    val cardColor = if (isDark) Color(0xFF131316) else Color(0xFFFFFFFF)

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
            .statusBarsPadding(),
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
            Text(
                text = "Welcome",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Sign in or create an account",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )

            if (errorMessage != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = errorMessage!!,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = {
                    errorMessage = null
                    launchOAuth("google")
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(10.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isDark) Color(0xFF1C1C20) else Color(0xFFF9FAFB),
                    contentColor = MaterialTheme.colorScheme.onSurface
                ),
                border = androidx.compose.foundation.BorderStroke(1.dp, if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB))
            ) {
                Text(
                    text = "Continue with Google",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            Button(
                onClick = {
                    errorMessage = null
                    launchOAuth("github")
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(10.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isDark) Color(0xFF1C1C20) else Color(0xFFF9FAFB),
                    contentColor = MaterialTheme.colorScheme.onSurface
                ),
                border = androidx.compose.foundation.BorderStroke(1.dp, if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB))
            ) {
                Text(
                    text = "Continue with GitHub",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                HorizontalDivider(modifier = Modifier.weight(1f), color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB))
                Text(
                    text = "  or  ",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                HorizontalDivider(modifier = Modifier.weight(1f), color = if (isDark) Color(0xFF2A2A30) else Color(0xFFE5E7EB))
            }

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = onNavigateToEmailLogin,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                shape = RoundedCornerShape(10.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                )
            ) {
                Icon(
                    imageVector = Icons.Filled.Email,
                    contentDescription = null,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "Sign in with Email",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            TextButton(
                onClick = onNavigateToEmailSignup,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "Don't have an account? Register",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}