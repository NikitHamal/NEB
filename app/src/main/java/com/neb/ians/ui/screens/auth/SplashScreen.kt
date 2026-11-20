package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.R
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.util.NebSystemBars
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

/**
 * The splash: the page colour, the mark, the name. Nothing else.
 *
 * The screen is the app's own surface, white in light and the deep navy in dark, following the
 * theme the member chose in settings. The N settles in on a spring (a small drop, a quarter turn
 * of tilt and a swell), then NEBians is cut in letter by letter, each rising out of its own mask
 * line, and the whole stack lifts away. No tinted wash, no big shape, no orbit: a colour field
 * behind a logo reads as a stain, so there is none, here or anywhere.
 *
 * Springs only. Every value is read in the draw phase, so no frame recomposes. The destination
 * (home, profile, intro or sign-in) is resolved in parallel, so a cold start pays nothing.
 */
@Composable
fun SplashScreen(
    authRepository: AuthRepository,
    settingsRepository: SettingsRepository,
    onNavigateToHome: () -> Unit,
    onNavigateToLogin: () -> Unit,
    onNavigateToCompleteProfile: () -> Unit,
    onNavigateToIntro: () -> Unit = onNavigateToLogin
) {
    val scheme = MaterialTheme.colorScheme
    val dark = scheme.surface.luminance() < 0.5f
    // the status bar stays where it is (hiding it moved the next screen by its height)
    NebSystemBars(darkIcons = !dark)

    val reduced = nebAnimationsReduced()
    val spatial = nebSpatialSpec<Float>()

    val mark = remember { Animatable(0f) }
    val letters = remember { List(SPLASH_WORD.length) { Animatable(0f) } }
    val exit = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        coroutineScope {
            val warmup = async {
                kotlinx.coroutines.withTimeoutOrNull(750L) {
                    runCatching { authRepository.authState.first() }.getOrNull()
                }
            }

            if (reduced) {
                mark.snapTo(1f)
                letters.forEach { it.snapTo(1f) }
                delay(180)
                warmup.await()
            } else {
                launch { mark.animateTo(1f, spring(Spring.DampingRatioLowBouncy, Spring.StiffnessLow)) }
                delay(240)
                letters.forEachIndexed { i, letter ->
                    launch {
                        delay(i * 28L)
                        letter.animateTo(1f, spatial)
                    }
                }
                delay(480)
                warmup.await()
                exit.animateTo(1f, spring(Spring.DampingRatioNoBouncy, 600f, visibilityThreshold = 0.002f))
            }

            // Zero login gate & zero onboarding prison on launch: always enter Home directly.
            onNavigateToHome()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(scheme.background),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.graphicsLayer {
                val s = 1f + 0.05f * exit.value
                scaleX = s
                scaleY = s
                translationY = -20.dp.toPx() * exit.value
                alpha = 1f - exit.value
            }
        ) {
            // The launcher icon's own foreground, whole: one drawable, no re-drawn facets.
            Image(
                painter = painterResource(R.drawable.ic_launcher_foreground),
                contentDescription = null,
                modifier = Modifier
                    .size(240.dp)
                    .graphicsLayer {
                        val t = mark.value
                        val s = 0.62f + 0.38f * t
                        scaleX = s
                        scaleY = s
                        rotationZ = (1f - t) * -14f
                        translationY = (1f - t) * -36.dp.toPx()
                        alpha = (t * 2.5f).coerceIn(0f, 1f)
                    }
            )
            Row(horizontalArrangement = Arrangement.Center, modifier = Modifier.offset(y = (-22).dp)) {
                SPLASH_WORD.forEachIndexed { i, ch ->
                    Box(Modifier.clipToBounds()) {
                        Text(
                            text = ch.toString(),
                            fontFamily = Poppins,
                            fontWeight = if (i < 3) FontWeight.ExtraBold else FontWeight.Medium,
                            fontSize = 36.sp,
                            color = if (i < 3) scheme.primary else scheme.onSurface,
                            modifier = Modifier.graphicsLayer {
                                val t = letters[i].value
                                translationY = (1f - t) * size.height * 1.1f
                            }
                        )
                    }
                }
            }
        }
    }
}

private const val SPLASH_WORD = "NEBians"
