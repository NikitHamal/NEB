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
 * The splash: the mark, and nothing else, for about a second and a quarter.
 *
 *   [0 - 80ms]      Empty paper, so the eye finds the screen before anything moves.
 *   [80 - 600ms]    The whole mark fades in and settles from 94% to full size. No facets move.
 *   [600 - 1000ms]  It holds.
 *   [1000 - 1250ms] The mark pushes forward a little and fades into whatever comes next.
 *
 * The destination is resolved in parallel, so a cold start pays nothing extra for the auth
 * read. Every animated value is read in the draw phase (graphicsLayer), so no frame recomposes.
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

    val enter = remember { Animatable(0f) }
    val exitScale = remember { Animatable(1f) }
    val exitAlpha = remember { Animatable(1f) }
    val assembled = remember { mutableFloatStateOf(1f) }
    val noShine = remember { mutableFloatStateOf(0f) }

    LaunchedEffect(Unit) {
        val destination = async {
            runCatching { authRepository.authState.first() }.getOrNull()
        }

        if (reducedMotion) {
            enter.snapTo(1f)
            delay(450)
        } else {
            delay(NEB_SPLASH_LEAD_IN_MS)
            enter.animateTo(1f, tween(durationMillis = 520, easing = FastOutSlowInEasing))
            delay(400)
            launch { exitAlpha.animateTo(0f, spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 900f)) }
            exitScale.animateTo(1.06f, spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = 700f, visibilityThreshold = 0.002f))
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
            assembly = assembled,
            shine = noShine,
            modifier = Modifier
                .size(NEB_SPLASH_LOGO_SIZE)
                .graphicsLayer {
                    val scale = (0.94f + 0.06f * enter.value) * exitScale.value
                    alpha = enter.value * exitAlpha.value
                    scaleX = scale
                    scaleY = scale
                }
        )
    }
}

/** The beat of empty paper before anything moves, in milliseconds. */
private const val NEB_SPLASH_LEAD_IN_MS = 80L

/** The mark's size. Large enough to read as the brand, small enough to stay calm. */
private val NEB_SPLASH_LOGO_SIZE = 132.dp
