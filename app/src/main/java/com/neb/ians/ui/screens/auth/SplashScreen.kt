package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.unit.dp
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.ui.components.NebLogoMark
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebAuthPalette
import com.neb.ians.util.HideStatusBarEffect
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

/**
 * The splash: the mark, and nothing else, for about a second and a half.
 *
 *   [0 - 80ms]      Empty paper, so the eye finds the screen before anything moves.
 *   [80 - ~900ms]   The facets of the "N" assemble: the long ribbon rises, the two pillars
 *                   drop into place, the light facet slides in. One critically damped spring
 *                   drives the whole assembly; each facet takes its own window of it.
 *   [~820 - 1240ms] A band of light crosses the finished mark, once.
 *   [1240 - 1500ms] The mark pushes forward and fades into whatever comes next.
 *
 * The destination is resolved in parallel, so a cold start pays nothing extra for the auth
 * read. Every animated value is read in the draw phase (NebLogoMark's Canvas, graphicsLayer),
 * so no frame recomposes. The handwritten wordmark that used to sit under the logo lives on
 * as [com.neb.ians.ui.components.NebDoodleWordmark] for use elsewhere.
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

    // The splash is always light, like the rest of the auth journey.
    val palette = nebAuthPalette(isDark = false)
    val reducedMotion = nebAnimationsReduced()

    val assembly = remember { Animatable(0f) }
    val shine = remember { Animatable(0f) }
    val exitScale = remember { Animatable(1f) }
    val exitAlpha = remember { Animatable(1f) }
    val assemblyState = remember(assembly) { assembly.asState() }
    val shineState = remember(shine) { shine.asState() }

    LaunchedEffect(Unit) {
        val destination = async {
            runCatching { authRepository.authState.first() }.getOrNull()
        }

        if (reducedMotion) {
            assembly.snapTo(1f)
            shine.snapTo(1f)
            delay(450)
        } else {
            delay(NEB_SPLASH_LEAD_IN_MS)
            launch {
                assembly.animateTo(
                    targetValue = 1f,
                    animationSpec = spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 120f, visibilityThreshold = 0.002f)
                )
            }
            delay(740)
            shine.animateTo(1f, spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 60f, visibilityThreshold = 0.004f))
            launch { exitAlpha.animateTo(0f, spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 900f)) }
            exitScale.animateTo(1.14f, spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 700f, visibilityThreshold = 0.002f))
        }

        when (val state = destination.await()) {
            is AuthState.Authenticated -> {
                if (state.isProfileComplete) onNavigateToHome() else onNavigateToCompleteProfile()
            }
            else -> onNavigateToLogin()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(palette.page),
        contentAlignment = Alignment.Center
    ) {
        NebLogoMark(
            assembly = assemblyState,
            shine = shineState,
            modifier = Modifier
                .size(NEB_SPLASH_LOGO_SIZE)
                .graphicsLayer {
                    alpha = exitAlpha.value
                    scaleX = exitScale.value
                    scaleY = exitScale.value
                }
        )
    }
}

/** The beat of empty paper before anything moves, in milliseconds. */
private const val NEB_SPLASH_LEAD_IN_MS = 80L

/** The mark's size. Large enough to read as the brand, small enough to stay calm. */
private val NEB_SPLASH_LOGO_SIZE = 132.dp
