package com.neb.ians.ui.screens.auth

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.neb.ians.R
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebAuthPalette
import com.neb.ians.util.HideStatusBarEffect
import kotlinx.coroutines.async
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

/**
 * The splash.
 *
 * A beat of empty paper, then the word "Nebians" is written by hand in the brand
 * blue, holds, gathers itself, and collapses into the logo, which carries the
 * last half second before the app opens. Just under four seconds end to end.
 *
 * The choreography is four moves, and the two small ones do most of the work:
 *
 *   The lead-in. A fifth of a second of nothing before the pen touches down.
 *   Without it the first stroke is already underway before the eye has found the
 *   screen, and the writing reads as something that was mid-way through rather
 *   than something that started.
 *
 *   The anticipation. Before the word collapses it grows by three percent and
 *   rises a few pixels — the wind-up. It costs ninety milliseconds and it is the
 *   difference between the collapse landing and the collapse merely happening.
 *
 *   The overlap. The ink is still fading when the logo starts to arrive. Playing
 *   them back to back reads as two animations; overlapping them reads as one
 *   thing becoming another, which is the entire point of the moment.
 *
 *   The settle. The logo arrives on a spring, under-damped and tilted eight
 *   degrees off true, and rights itself as it lands. A mark that snaps to its
 *   final size on a tween looks placed. This one looks like it fell into place.
 *
 * Two things about the screen are load-bearing beyond the choreography:
 *
 * The destination is resolved in parallel with the animation, not after it. The
 * auth state comes off disk, and asking for it once the logo had finished meant
 * every cold start paid for that read in visible dead time at the end. Started
 * up front it costs nothing — the answer is always waiting by the time the
 * animation is done.
 *
 * Nothing here recomposes per frame. The writing progress is handed to the
 * canvas as a State and read inside its draw lambda, and every transform is read
 * inside a graphicsLayer lambda. Both defer the state read past composition, so
 * the frames are draw-only. On the one screen where the user is waiting for the
 * app to start, that is worth the small amount of care.
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

    val writing = remember { Animatable(0f) }
    val doodleAlpha = remember { Animatable(1f) }
    val doodleScale = remember { Animatable(1f) }
    /** Vertical offset of the word, in dp. Negative is up. */
    val doodleLift = remember { Animatable(0f) }
    val logoAlpha = remember { Animatable(0f) }
    val logoScale = remember { Animatable(0.52f) }
    val logoTilt = remember { Animatable(-8f) }

    val writingProgress = remember(writing) { writing.asState() }

    LaunchedEffect(Unit) {
        val destination = async {
            runCatching { authRepository.authState.first() }.getOrNull()
        }

        if (reducedMotion) {
            // The user has asked the system not to animate. Show the finished
            // state, long enough to register, and get out of the way.
            writing.snapTo(1f)
            doodleAlpha.snapTo(0f)
            logoAlpha.snapTo(1f)
            logoScale.snapTo(1f)
            logoTilt.snapTo(0f)
            delay(400)
        } else {
            // [0 - 120ms] Empty paper.
            delay(NEB_SPLASH_LEAD_IN_MS)

            // [120 - 2420ms] The word is written. Linear on purpose: a hand
            // moves the pen at a roughly constant speed, and the rhythm you hear
            // in the writing comes from the pen lifts baked into the stroke
            // timeline, not from an easing curve laid over the top of it.
            writing.animateTo(
                targetValue = 1f,
                animationSpec = tween(NEB_DOODLE_WRITE_MS, easing = LinearEasing)
            )

            // [2420 - 2660ms] Let it sit. This beat is what makes the word read
            // as a word before it turns into a mark.
            delay(240)

            // [2660 - 2750ms] The wind-up.
            launch { doodleLift.animateTo(-7f, tween(90, easing = LinearOutSlowInEasing)) }
            doodleScale.animateTo(1.035f, tween(90, easing = LinearOutSlowInEasing))

            // [2750 - 3090ms] The collapse. The ink gathers toward the centre —
            // which is exactly where the logo is about to appear — and lets go.
            launch {
                launch { doodleAlpha.animateTo(0f, tween(280, easing = FastOutLinearInEasing)) }
                launch { doodleLift.animateTo(0f, tween(340, easing = FastOutSlowInEasing)) }
                doodleScale.animateTo(0.80f, tween(340, easing = FastOutSlowInEasing))
            }

            // [2890ms] The logo starts arriving while the ink is still there.
            delay(140)
            launch { logoAlpha.animateTo(1f, tween(240, easing = LinearOutSlowInEasing)) }
            launch {
                logoTilt.animateTo(
                    targetValue = 0f,
                    animationSpec = spring(
                        dampingRatio = 0.55f,
                        stiffness = Spring.StiffnessMediumLow
                    )
                )
            }
            logoScale.animateTo(
                targetValue = 1f,
                animationSpec = spring(
                    dampingRatio = 0.58f,
                    stiffness = Spring.StiffnessMediumLow
                )
            )

            // [~3350 - 3730ms] The mark holds on its own.
            delay(380)

            // [3730 - 3980ms] Push forward into whatever comes next.
            launch { logoAlpha.animateTo(0f, tween(250, easing = FastOutLinearInEasing)) }
            logoScale.animateTo(1.09f, tween(250, easing = FastOutSlowInEasing))
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
            .background(palette.page)
            .statusBarsPadding()
            .navigationBarsPadding(),
        contentAlignment = Alignment.Center
    ) {
        NebDoodleWordmark(
            progress = writingProgress,
            color = palette.brand,
            modifier = Modifier
                .fillMaxWidth(0.68f)
                .aspectRatio(NEB_DOODLE_ASPECT)
                .graphicsLayer {
                    alpha = doodleAlpha.value
                    scaleX = doodleScale.value
                    scaleY = doodleScale.value
                    translationY = doodleLift.value * density
                }
        )

        // Composed from the first frame at zero opacity so the vector is parsed
        // and cached while the word is still being written. Doing it lazily at
        // the handoff puts a decode on the frame that has to be the smoothest
        // one on the screen.
        Image(
            painter = painterResource(id = R.drawable.n_logo),
            contentDescription = "NEBians",
            modifier = Modifier
                .size(88.dp)
                .graphicsLayer {
                    alpha = logoAlpha.value
                    scaleX = logoScale.value
                    scaleY = logoScale.value
                    rotationZ = logoTilt.value
                }
        )
    }
}

/** The beat of empty paper before the pen touches down, in milliseconds. */
private const val NEB_SPLASH_LEAD_IN_MS = 120L
