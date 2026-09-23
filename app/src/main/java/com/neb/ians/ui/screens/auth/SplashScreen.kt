package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.neb.ians.R
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.util.HideStatusBarEffect
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first

/**
 * Clean, minimal, pro-grade logo-only splash screen in pure light mode.
 * No ambient glow, strictly clean 3D logo with subtle, elegant physics.
 * Total duration: 2.0 seconds precisely.
 */
@Composable
fun SplashScreen(
    authRepository: AuthRepository,
    settingsRepository: SettingsRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit
) {
    HideStatusBarEffect()

    // Animation drivers
    val logoScale = remember { Animatable(0.85f) }
    val logoAlpha = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        // [0 - 650ms]: Gentle, silky fade & scale-in
        logoAlpha.animateTo(1f, animationSpec = tween(550, easing = FastOutSlowInEasing))
        logoScale.animateTo(
            targetValue = 1.0f,
            animationSpec = spring(
                dampingRatio = Spring.DampingRatioNoBouncy,
                stiffness = Spring.StiffnessLow
            )
        )

        // [650ms - 1700ms]: Pristine calm hold
        delay(850)

        // [1700ms - 2000ms]: Crisp forward transition into destination
        logoScale.animateTo(1.04f, animationSpec = tween(300, easing = FastOutSlowInEasing))
        logoAlpha.animateTo(0.92f, animationSpec = tween(200))

        delay(50)

        // Navigate directly based on auth status (onboarding removed)
        when (val state = authRepository.authState.first()) {
            is AuthState.Guest -> onNavigateToLogin()
            is AuthState.Authenticated -> {
                if (state.isProfileComplete) {
                    onNavigateToHome()
                } else {
                    onNavigateToCompleteProfile()
                }
            }
            else -> onNavigateToLogin()
        }
    }

    // Strictly pure light background (no dark mode, no glow)
    val bgColor = Color(0xFFFFFFFF)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(bgColor)
            .statusBarsPadding()
            .navigationBarsPadding(),
        contentAlignment = Alignment.Center
    ) {
        // Official NEBians 3D Logo (Pure, minimal, sharp, zero surrounding glow)
        Image(
            painter = painterResource(id = R.drawable.n_logo),
            contentDescription = "NEBians",
            modifier = Modifier
                .size(76.dp)
                .alpha(logoAlpha.value)
                .scale(logoScale.value)
        )
    }
}
