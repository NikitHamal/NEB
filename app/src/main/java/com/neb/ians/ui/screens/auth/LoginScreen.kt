package com.neb.ians.ui.screens.auth

import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.util.HideStatusBarEffect

@Composable
fun LoginScreen(
    authRepository: AuthRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateToEmailSignup: () -> Unit,
    onNavigateToForgotPassword: (email: String) -> Unit,
    onNavigateToVerification: (email: String) -> Unit
) {
    // Hide status bar on auth screen as requested
    HideStatusBarEffect()

    val context = LocalContext.current
    // Auth screen is consistently displayed in light mode
    val isDark = false

    var isLoading by remember { mutableStateOf(false) }
    var loadingProvider by remember { mutableStateOf<String?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var isEmailSheetOpen by remember { mutableStateOf(false) }
    var activeLegalSheet by remember { mutableStateOf<LegalSheetType?>(null) }

    fun launchOAuth(provider: String) {
        isLoading = true
        loadingProvider = provider
        errorMessage = null

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
        } finally {
            isLoading = false
            loadingProvider = null
        }
    }

    val screenBgColor = if (isDark) Color(0xFF0F172A) else Color(0xFFFFFFFF)
    val brandBlue = Color(0xFF2563EB)
    val titleTextColor = if (isDark) Color(0xFFF8FAFC) else Color(0xFF0F172A)
    val subtitleTextColor = if (isDark) Color(0xFF94A3B8) else Color(0xFF64748B)

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxSize()
            .background(screenBgColor)
            .navigationBarsPadding()
    ) {
        val screenHeight = maxHeight
        val heroHeight = (screenHeight * 0.48f).coerceIn(280.dp, 440.dp)

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(bottom = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 1. Top Hero Image (Exact artwork from uploaded image, zero animations, no logo/header)
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(heroHeight)
            ) {
                Image(
                    painter = painterResource(id = R.drawable.auth_hero_sky),
                    contentDescription = "Open Book in Sky",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )

                // Seamless gradient fade from image to screen background
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(110.dp)
                        .align(Alignment.BottomCenter)
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(
                                    Color.Transparent,
                                    screenBgColor.copy(alpha = 0.45f),
                                    screenBgColor.copy(alpha = 0.85f),
                                    screenBgColor
                                )
                            )
                        )
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            // 2. "Welcome to NEBians" (Poppins 600 bold, blue "NEBians")
            val welcomeText = buildAnnotatedString {
                append("Welcome to ")
                val startBrand = length
                append("NEBians")
                val endBrand = length
                addStyle(
                    style = SpanStyle(
                        color = brandBlue,
                        fontWeight = FontWeight.SemiBold
                    ),
                    start = startBrand,
                    end = endBrand
                )
            }

            Text(
                text = welcomeText,
                fontFamily = Poppins,
                fontWeight = FontWeight.SemiBold, // Poppins 600
                fontSize = 27.sp,
                letterSpacing = (-0.4).sp,
                color = titleTextColor,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(10.dp))

            // Subtitle in Poppins 500
            Text(
                text = "The open learning community for Nepal. Connect, learn, share study materials, and explore together.",
                fontFamily = Poppins,
                fontWeight = FontWeight.Medium, // Poppins 500
                fontSize = 14.5.sp,
                lineHeight = 21.sp,
                color = subtitleTextColor,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 32.dp)
            )

            if (!errorMessage.isNullOrBlank()) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = errorMessage ?: "",
                    fontFamily = Poppins,
                    fontWeight = FontWeight.Medium,
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 24.dp)
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            // 3. Action Buttons (Google, GitHub, Email, Terms - Poppins 600/500, no shadows)
            AuthActionButtons(
                isDark = isDark,
                isLoading = isLoading,
                loadingProvider = loadingProvider,
                onGoogleClick = { launchOAuth("google") },
                onGitHubClick = { launchOAuth("github") },
                onEmailClick = { isEmailSheetOpen = true },
                onTermsClick = { activeLegalSheet = LegalSheetType.TERMS },
                onPrivacyClick = { activeLegalSheet = LegalSheetType.PRIVACY }
            )
        }

        // Email Sign-In & Quick Register Bottom Sheet
        AuthEmailSheet(
            isOpen = isEmailSheetOpen,
            onDismiss = { isEmailSheetOpen = false },
            isDark = isDark,
            authRepository = authRepository,
            onNavigateToHome = onNavigateToHome,
            onNavigateToCompleteProfile = onNavigateToCompleteProfile,
            onNavigateToForgotPassword = onNavigateToForgotPassword,
            onNavigateToVerification = onNavigateToVerification,
            onNavigateToFullSignup = {
                isEmailSheetOpen = false
                onNavigateToEmailSignup()
            }
        )

        // Terms of Service & Privacy Policy Bottom Sheet
        AuthLegalSheet(
            sheetType = activeLegalSheet,
            onDismiss = { activeLegalSheet = null },
            isDark = isDark
        )
    }
}
