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
import com.neb.ians.ui.components.NEB_DOODLE_ASPECT
import com.neb.ians.ui.components.NEB_DOODLE_WRITE_MS
import com.neb.ians.ui.components.NebDoodleWordmark
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
 * The mark drops in first, and then the word is written by hand underneath it,
 * in the brand blue. They are a lockup, not a substitution: the logo sits above
 * the doodle for the whole screen and the two leave together. The previous
 * version had the word collapse and the logo replace it, which meant the two
 * halves of the brand were never on screen at the same time — you saw a word,
 * then you saw a mark, and nothing told you they belonged to each other.
 *
 * Three moves, and the small one does most of the work:
 *
 *   The drop. The logo arrives on an under-damped spring, tilted eight degrees
 *   off true and a few pixels high, and rights itself as it lands. A mark that
 *   snaps to its final size on a tween looks placed. This one looks like it fell
 *   into place.
 *
 *   The overlap. The pen touches down while the logo is still settling. Playing
 *   them back to back reads as two animations; overlapping them reads as one
 *   event with two parts, which is what a lockup is.
 *
 *   The settle. When the last stroke lands the whole lockup lifts five pixels on
 *   a soft spring — one breath — and holds. Without it the word simply stops,
 *   and stopping is not the same as finishing.
 *
 * About three seconds end to end, down from just under four. The time came off
 * the handoff, which no longer exists, and a little off the writing itself.
 *
 * Two things beyond the choreography are load-bearing:
 *
 * The destination is resolved in parallel with the animation, not after it. The
 * auth state comes off disk, and asking for it once the animation had finished
 * meant every cold start paid for that read in visible dead time at the end.
 * Started up front it costs nothing.
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
    val logoAlpha = remember { Animatable(0f) }
    val logoScale = remember { Animatable(0.62f) }
    val logoTilt = remember { Animatable(-8f) }
    /** Vertical offset of the mark during its drop, in dp. Negative is up. */
    val logoDrop = remember { Animatable(-14f) }
    /** Vertical offset of the whole lockup once the word has landed, in dp. */
    val lockupLift = remember { Animatable(0f) }
    val lockupAlpha = remember { Animatable(1f) }
    val lockupScale = remember { Animatable(1f) }

    val writingProgress = remember(writing) { writing.asState() }

    LaunchedEffect(Unit) {
        val destination = async {
            runCatching { authRepository.authState.first() }.getOrNull()
        }

        if (reducedMotion) {
            // The user has asked the system not to animate. Show the finished
            // lockup, long enough to register, and get out of the way.
            writing.snapTo(1f)
            logoAlpha.snapTo(1f)
            logoScale.snapTo(1f)
            logoTilt.snapTo(0f)
            logoDrop.snapTo(0f)
            delay(400)
        } else {
            // [0 - 90ms] Empty paper. Without it the first frame of motion is
            // already underway before the eye has found the screen.
            delay(NEB_SPLASH_LEAD_IN_MS)

            // [90 - ~520ms] The mark drops in.
            launch { logoAlpha.animateTo(1f, tween(200, easing = LinearOutSlowInEasing)) }
            launch {
                logoTilt.animateTo(
                    targetValue = 0f,
                    animationSpec = spring(dampingRatio = 0.55f, stiffness = Spring.StiffnessMediumLow)
                )
            }
            launch {
                logoDrop.animateTo(
                    targetValue = 0f,
                    animationSpec = spring(dampingRatio = 0.62f, stiffness = Spring.StiffnessMediumLow)
                )
            }
            launch {
                logoScale.animateTo(
                    targetValue = 1f,
                    animationSpec = spring(dampingRatio = 0.58f, stiffness = Spring.StiffnessMediumLow)
                )
            }

            // [280 - 2330ms] The pen touches down while the mark is still
            // settling, and writes. Linear on purpose: a hand moves the pen at a
            // roughly constant speed, and the rhythm you hear comes from the pen
            // lifts baked into the stroke timeline, not from an easing curve.
            delay(190)
            writing.animateTo(
                targetValue = 1f,
                animationSpec = tween(NEB_DOODLE_WRITE_MS, easing = LinearEasing)
            )

            // [2330 - 2760ms] One breath, then the lockup holds.
            launch {
                lockupLift.animateTo(
                    targetValue = -5f,
                    animationSpec = spring(dampingRatio = 0.6f, stiffness = Spring.StiffnessLow)
                )
            }
            delay(430)

            // [2760 - 3000ms] Push forward into whatever comes next.
            launch { lockupAlpha.animateTo(0f, tween(240, easing = FastOutLinearInEasing)) }
            lockupScale.animateTo(1.07f, tween(240, easing = FastOutSlowInEasing))
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
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .graphicsLayer {
                    alpha = lockupAlpha.value
                    scaleX = lockupScale.value
                    scaleY = lockupScale.value
                    translationY = lockupLift.value * density
                },
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // The mark, above the word. Composed from the first frame so the
            // vector is parsed and cached before it is needed, rather than
            // paying for the decode on a frame that has to be smooth.
            Image(
                painter = painterResource(id = R.drawable.n_logo),
                contentDescription = "NEBians",
                modifier = Modifier
                    .size(NEB_SPLASH_LOGO_SIZE)
                    .graphicsLayer {
                        alpha = logoAlpha.value
                        scaleX = logoScale.value
                        scaleY = logoScale.value
                        rotationZ = logoTilt.value
                        translationY = logoDrop.value * density
                    }
            )

            Spacer(modifier = Modifier.height(20.dp))

            NebDoodleWordmark(
                progress = writingProgress,
                color = palette.brand,
                modifier = Modifier
                    .fillMaxWidth(0.62f)
                    .aspectRatio(NEB_DOODLE_ASPECT)
            )
        }
    }
}

/** The beat of empty paper before anything moves, in milliseconds. */
private const val NEB_SPLASH_LEAD_IN_MS = 90L

/** The mark's size in the lockup. Set against the 62%-width wordmark below it. */
private val NEB_SPLASH_LOGO_SIZE = 76.dp
