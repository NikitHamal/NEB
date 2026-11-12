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
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import com.neb.ians.data.repository.SettingsRepository
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebMorphBlob
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.md_theme_light_primaryContainer
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.util.NebSystemBars
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

/**
 * The splash: one shape takes over the screen, the mark lands on it, the name is cut in.
 *
 *   A cookie blooms from the middle of a white screen and morphs through clover, sunny and
 *   flower while it grows until the tonal blue fills every edge. The N drops onto it with a
 *   springy tilt. NEBians is then revealed letter by letter, each rising out of its own
 *   mask line. Last, the colour drains back to white and the whole stack lifts away.
 *
 * Nothing sits around the logo: the shape is the stage. Springs only, from the expressive
 * motion scheme. Every value is read in the draw phase; no frame recomposes. The destination
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
    // the status bar stays where it is (hiding it moved the next screen by its height); dark icons on the splash
    NebSystemBars(darkIcons = true)

    val reduced = nebAnimationsReduced()
    val spatial = nebSpatialSpec<Float>()

    val fill = remember { Animatable(0f) }
    val morph = remember { Animatable(0f) }
    val mark = remember { Animatable(0f) }
    val letters = remember { List(SPLASH_WORD.length) { Animatable(0f) } }
    val exit = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        coroutineScope {
            val destination = async {
                val auth = runCatching { authRepository.authState.first() }.getOrNull()
                val seen = runCatching { settingsRepository.isIntroSeen.first() }.getOrDefault(true)
                auth to seen
            }

            if (reduced) {
                fill.snapTo(1f)
                morph.snapTo(SPLASH_BLOB.size - 1f)
                mark.snapTo(1f)
                letters.forEach { it.snapTo(1f) }
                delay(300)
            } else {
                launch { fill.animateTo(1f, spring(Spring.DampingRatioNoBouncy, 110f, visibilityThreshold = 0.002f)) }
                launch {
                    morph.animateTo(
                        SPLASH_BLOB.size - 1f,
                        spring(Spring.DampingRatioNoBouncy, Spring.StiffnessVeryLow)
                    )
                }
                delay(260)
                launch { mark.animateTo(1f, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessLow)) }
                delay(280)
                letters.forEachIndexed { i, letter ->
                    launch {
                        delay(i * 34L)
                        letter.animateTo(1f, spatial)
                    }
                }
                delay(560)
                exit.animateTo(1f, spring(Spring.DampingRatioNoBouncy, 700f, visibilityThreshold = 0.002f))
            }

            val (auth, seen) = destination.await()
            when (auth) {
                is AuthState.Authenticated ->
                    if (auth.isProfileComplete) onNavigateToHome() else onNavigateToCompleteProfile()
                else -> if (seen) onNavigateToLogin() else onNavigateToIntro()
            }
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        // The stage: the blob is as wide as the screen and scales past its corners.
        NebMorphBlob(
            shapes = SPLASH_BLOB,
            color = md_theme_light_primaryContainer,
            modifier = Modifier
                .fillMaxSize()
                .graphicsLayer {
                    val s = fill.value * SPLASH_REACH
                    scaleX = s
                    scaleY = s
                    alpha = 1f - exit.value
                },
            rotation = { morph.value * 34f + fill.value * 50f },
            position = { morph.value }
        )

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.graphicsLayer {
                val s = 1f + 0.06f * exit.value
                scaleX = s
                scaleY = s
                translationY = -24.dp.toPx() * exit.value
                alpha = 1f - exit.value
            }
        ) {
            // The launcher icon's own foreground, whole: one drawable, no re-drawn facets.
            Image(
                painter = painterResource(R.drawable.ic_launcher_foreground),
                contentDescription = null,
                modifier = Modifier
                    .size(250.dp)
                    .graphicsLayer {
                        val t = mark.value
                        val s = 0.3f + 0.7f * t
                        scaleX = s
                        scaleY = s
                        rotationZ = (1f - t) * -24f
                        translationY = (1f - t) * -60.dp.toPx()
                        alpha = (t * 3f).coerceIn(0f, 1f)
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
                            color = SPLASH_INK,
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

private val SPLASH_BLOB = listOf(
    NebGlyphShapes.Cookie,
    NebGlyphShapes.Clover,
    NebGlyphShapes.Sunny,
    NebGlyphShapes.Flower
)

/** How many screen widths the blob ends up: enough that no corner of a tall phone stays white. */
private const val SPLASH_REACH = 4.4f

private const val SPLASH_WORD = "NEBians"

private val SPLASH_INK = Color(0xFF06235F)
