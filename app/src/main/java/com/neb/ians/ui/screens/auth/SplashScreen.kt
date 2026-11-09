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
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
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
import com.neb.ians.ui.components.NebTone
import com.neb.ians.ui.components.drawGlyph
import com.neb.ians.ui.components.rememberGlyphPath
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.md_theme_light_primaryContainer
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.util.NebSystemBars
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlin.math.cos
import kotlin.math.sin

/**
 * The splash: the landing page's shapes arriving, then the mark, then the name.
 *
 *   A cookie blooms from nothing and morphs through clover, sunny and flower while the N
 *   assembles on it facet by facet. Four tonal tiles (azure, sky, aqua, periwinkle: the
 *   landing hero's glyphs) spring out from behind the mark and settle around it. The
 *   word NEBians then rises letter by letter. Everything pushes forward and fades into
 *   whatever comes next.
 *
 * Springs only, from the expressive motion scheme, so the overshoot is the same overshoot
 * the rest of the app has. Every value is read in the draw phase; no frame recomposes.
 * The destination (home, profile, intro or sign-in) is resolved in parallel with the
 * animation, so a cold start pays nothing for it.
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
    // the status bar stays where it is (hiding it moved the next screen by its height); dark icons on the white splash
    NebSystemBars(darkIcons = true)

    val reduced = nebAnimationsReduced()
    val spatial = nebSpatialSpec<Float>()
    val effects = nebEffectsSpec<Float>()

    val bloom = remember { Animatable(0f) }
    val morph = remember { Animatable(0f) }
    val assembly = remember { Animatable(0f) }
    val tiles = remember { List(SPLASH_TILES.size) { Animatable(0f) } }
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
                bloom.snapTo(1f)
                morph.snapTo(SPLASH_BLOB.size - 1f)
                assembly.snapTo(1f)
                tiles.forEach { it.snapTo(1f) }
                letters.forEach { it.snapTo(1f) }
                delay(300)
            } else {
                launch { bloom.animateTo(1f, spatial) }
                launch {
                    morph.animateTo(
                        SPLASH_BLOB.size - 1f,
                        spring(Spring.DampingRatioLowBouncy, Spring.StiffnessMediumLow)
                    )
                }
                delay(70)
                launch { assembly.animateTo(1f, spring(Spring.DampingRatioLowBouncy, Spring.StiffnessMedium)) }
                tiles.forEachIndexed { i, tile ->
                    launch {
                        delay(i * 50L)
                        tile.animateTo(1f, spatial)
                    }
                }
                delay(300)
                letters.forEachIndexed { i, letter ->
                    launch {
                        delay(i * 26L)
                        letter.animateTo(1f, spatial)
                    }
                }
                delay(200)
                delay(260)
                exit.animateTo(1f, spring(Spring.DampingRatioNoBouncy, 800f, visibilityThreshold = 0.002f))
            }

            val (auth, seen) = destination.await()
            when (auth) {
                is AuthState.Authenticated ->
                    if (auth.isProfileComplete) onNavigateToHome() else onNavigateToCompleteProfile()
                else -> if (seen) onNavigateToLogin() else onNavigateToIntro()
            }
        }
    }

    val tilePaths = SPLASH_TILES.map { rememberGlyphPath(it.shape) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.graphicsLayer {
                val s = 1f + 0.08f * exit.value
                scaleX = s
                scaleY = s
                alpha = 1f - exit.value
            }
        ) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(300.dp)
                    .drawBehind {
                        val c = Offset(size.width / 2f, size.height / 2f)
                        val reach = size.minDimension * 0.37f
                        SPLASH_TILES.forEachIndexed { i, spec ->
                            val t = tiles[i].value
                            val a = Math.toRadians(spec.angle.toDouble())
                            val dist = reach * t * (1f + 0.6f * exit.value)
                            drawGlyph(
                                path = tilePaths[i],
                                center = Offset(c.x + cos(a).toFloat() * dist, c.y + sin(a).toFloat() * dist),
                                side = size.minDimension * spec.size * t,
                                color = spec.tone.container(false),
                                rotation = (1f - t) * -140f * spec.spin,
                                alpha = t.coerceIn(0f, 1f)
                            )
                        }
                    }
            ) {
                NebMorphBlob(
                    shapes = SPLASH_BLOB,
                    color = md_theme_light_primaryContainer,
                    modifier = Modifier
                        .size(204.dp)
                        .graphicsLayer {
                            val s = bloom.value
                            scaleX = s
                            scaleY = s
                            alpha = s.coerceIn(0f, 1f)
                        },
                    rotation = { morph.value * 24f },
                    position = { morph.value }
                )
                // The launcher icon's own foreground, whole: one drawable, no re-drawn facets.
                Image(
                    painter = painterResource(R.drawable.ic_launcher_foreground),
                    contentDescription = null,
                    modifier = Modifier
                        .size(236.dp)
                        .graphicsLayer {
                            val t = assembly.value
                            val s = 0.55f + 0.45f * t
                            scaleX = s
                            scaleY = s
                            rotationZ = (1f - t) * -14f
                            alpha = (t * 2.5f).coerceIn(0f, 1f)
                        }
                )
            }
            Row(horizontalArrangement = Arrangement.Center) {
                SPLASH_WORD.forEachIndexed { i, ch ->
                    Text(
                        text = ch.toString(),
                        fontFamily = Poppins,
                        fontWeight = if (i < 3) FontWeight.ExtraBold else FontWeight.Medium,
                        fontSize = 34.sp,
                        color = SPLASH_INK,
                        modifier = Modifier.graphicsLayer {
                            val t = letters[i].value
                            translationY = (1f - t) * 36.dp.toPx()
                            alpha = t.coerceIn(0f, 1f)
                        }
                    )
                }
            }
        }
    }
}

private data class SplashTile(
    val shape: androidx.graphics.shapes.RoundedPolygon,
    val tone: NebTone,
    val angle: Float,
    val size: Float,
    val spin: Float
)

private val SPLASH_TILES = listOf(
    SplashTile(NebGlyphShapes.Cookie, NebTone.Azure, -145f, 0.22f, 1f),
    SplashTile(NebGlyphShapes.Sunny, NebTone.Sky, -35f, 0.2f, -1f),
    SplashTile(NebGlyphShapes.Flower, NebTone.Aqua, 38f, 0.21f, 1f),
    SplashTile(NebGlyphShapes.Gem, NebTone.Peri, 142f, 0.19f, -1f)
)

private val SPLASH_BLOB = listOf(
    NebGlyphShapes.Cookie,
    NebGlyphShapes.Clover,
    NebGlyphShapes.Sunny,
    NebGlyphShapes.Flower
)

private const val SPLASH_WORD = "NEBians"

private val SPLASH_INK = Color(0xFF06235F)
