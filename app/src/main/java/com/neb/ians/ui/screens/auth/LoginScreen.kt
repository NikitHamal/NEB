package com.neb.ians.ui.screens.auth

import android.net.Uri
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.ui.screens.onboarding.Reveal
import androidx.compose.material.icons.outlined.Close
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.nebAuthPalette

/**
 * The auth landing: the glyph stage, the name, the three ways in.
 *
 * White page, brand blue on the one word that is the brand, springs for every entrance. The
 * hero morphs, the title and the buttons rise one beat apart, and nothing is explained
 * twice: the name and the actions are the whole screen.
 */
@Composable
fun LoginScreen(
    onNavigateToEmailAuth: () -> Unit,
    onClose: (() -> Unit)? = null
) {
    val context = LocalContext.current
    val isDark = LocalNebAuthPalette.current.isDark

    var isLoading by remember { mutableStateOf(false) }
    var loadingProvider by remember { mutableStateOf<String?>(null) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
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

    val palette = nebAuthPalette(isDark)
    val screenBg = palette.page

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxSize()
            .background(screenBg)
            .statusBarsPadding()
            .navigationBarsPadding()
    ) {
        val heroHeight = (maxHeight * 0.44f).coerceIn(260.dp, 400.dp)

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(bottom = 20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(12.dp))

            AuthHero(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(heroHeight),
                dark = isDark
            )

            Spacer(modifier = Modifier.height(8.dp))

            Reveal(active = true, index = 3) {
                Text(
                    text = buildAnnotatedString {
                        append("Welcome to ")
                        pushStyle(SpanStyle(color = palette.brand, fontWeight = FontWeight.SemiBold))
                        append("NEBians")
                        pop()
                    },
                    fontFamily = Poppins,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 28.sp,
                    letterSpacing = (-0.5).sp,
                    color = palette.ink,
                    textAlign = TextAlign.Center
                )
            }

            AnimatedVisibility(
                visible = !errorMessage.isNullOrBlank(),
                enter = fadeIn() + expandVertically(),
                exit = fadeOut() + shrinkVertically()
            ) {
                Text(
                    text = errorMessage ?: "",
                    fontFamily = Poppins,
                    fontWeight = FontWeight.Medium,
                    fontSize = 13.sp,
                    color = MaterialTheme.colorScheme.error,
                    textAlign = TextAlign.Center,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 24.dp, end = 24.dp, top = 12.dp)
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            Reveal(active = true, index = 5, rise = 40.dp, modifier = Modifier.fillMaxWidth()) {
                AuthActionButtons(
                    isDark = isDark,
                    isLoading = isLoading,
                    loadingProvider = loadingProvider,
                    onGoogleClick = { launchOAuth("google") },
                    onGitHubClick = { launchOAuth("github") },
                    onEmailClick = onNavigateToEmailAuth,
                    onTermsClick = { activeLegalSheet = LegalSheetType.TERMS },
                    onPrivacyClick = { activeLegalSheet = LegalSheetType.PRIVACY }
                )
            }
        }

        if (onClose != null) {
            androidx.compose.material3.IconButton(
                onClick = onClose,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(top = 4.dp, end = 4.dp)
            ) {
                androidx.compose.material3.Icon(
                    androidx.compose.material.icons.Icons.Outlined.Close,
                    contentDescription = "Close",
                    tint = palette.ink
                )
            }
        }

        AuthLegalSheet(
            sheetType = activeLegalSheet,
            onDismiss = { activeLegalSheet = null },
            isDark = isDark
        )
    }
}
