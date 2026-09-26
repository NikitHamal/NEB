package com.neb.ians.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.theme.Poppins

/**
 * The profile cover.
 *
 * Three things changed from the old one. The art is generative and seeded by
 * the username, so two people with the same role do not get the same picture
 * ([ProfileCoverArt]). The height is a proportion of the cover's own width
 * instead of a fixed 160dp, so a tablet gets a cover rather than a letterbox.
 * And the deco word moved out of the middle — it was competing with the
 * avatar that hangs over the bottom-left — into a small tracked lockup in the
 * bottom-right, where it reads as a mark rather than as a headline.
 *
 * A custom [bannerUrl] still wins over all of it; the art is the default, not
 * an override.
 */

/** Cover aspect. Wide enough to be a cover, short enough not to eat the fold. */
private const val CoverAspect = 0.42f
private val CoverMin = 148.dp
private val CoverMax = 232.dp

/**
 * Picks the cover role + deco text for a profile, mirroring the web's
 * `views_profile.py` default-banner priority:
 * bot → admin → moderator → verified → teacher → institution → default.
 */
fun bannerPresetFor(profile: UserProfileResponse): Pair<CoverRole, String> = when {
    profile.isBot -> CoverRole.BOT to "neby ai"
    profile.isAdmin -> CoverRole.ADMIN to "admin"
    profile.moderatorLevel > 0 -> CoverRole.MODERATOR to "moderator"
    profile.verificationLevel > 0 -> CoverRole.VERIFIED to "nebian"
    profile.role == "teacher" -> CoverRole.TUTOR to "tutor"
    profile.role == "institution" -> CoverRole.INSTITUTION to "institution"
    else -> CoverRole.MEMBER to "nebian"
}

@Composable
fun ProfileBanner(
    bannerUrl: String?,
    role: CoverRole,
    decoText: String,
    seedKey: String,
    modifier: Modifier = Modifier
) {
    BoxWithConstraints(modifier = modifier) {
        val coverHeight = (maxWidth * CoverAspect).coerceAtLeast(CoverMin).coerceAtMost(CoverMax)

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(coverHeight)
                .clipToBounds()
        ) {
            val resolvedUrl = remember(bannerUrl) {
                when {
                    bannerUrl.isNullOrBlank() -> null
                    bannerUrl.startsWith("http://") || bannerUrl.startsWith("https://") -> bannerUrl
                    else -> "https://nebians.consica.com.np${if (bannerUrl.startsWith("/")) "" else "/"}$bannerUrl"
                }
            }

            if (resolvedUrl != null) {
                AsyncImage(
                    model = resolvedUrl,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
                // Even a user's own image needs the foot darkened: the avatar
                // ring below is white, and a bright photo swallows it.
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .drawBehind {
                            drawRect(
                                brush = Brush.verticalGradient(
                                    colors = listOf(
                                        Color.Transparent,
                                        Color.Black.copy(alpha = 0.30f)
                                    ),
                                    startY = size.height * 0.55f,
                                    endY = size.height
                                )
                            )
                        }
                )
            } else {
                val palette = remember(role) { coverPalette(role) }
                val seed = remember(seedKey, role) { stableSeed("cover|$seedKey|$role") }

                // The art reads no animated state, so it is rasterised once
                // and left alone while the sheen above it runs.
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val rng = Rng(seed)
                    drawCoverGround(palette, rng)
                    drawCoverMotif(role, palette, rng)
                    drawCoverFinish(palette, rng)
                }

                val transition = rememberInfiniteTransition(label = "coverSheen")
                val sheen by transition.animateFloat(
                    initialValue = 0f,
                    targetValue = 1f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(durationMillis = 11_000, easing = LinearEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "sheen"
                )

                // One slow diagonal pass of light. It is the only thing that
                // moves, and it is the only thing invalidated per frame.
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val w = size.width
                    val h = size.height
                    val band = w * 0.40f
                    val travel = w + band * 2.4f
                    val x = travel * sheen - band * 1.2f
                    drawRect(
                        brush = Brush.linearGradient(
                            colors = listOf(
                                Color.Transparent,
                                palette.ink.copy(alpha = 0.07f),
                                Color.Transparent
                            ),
                            start = Offset(x, h),
                            end = Offset(x + band, 0f)
                        )
                    )
                }

                if (decoText.isNotBlank()) {
                    // A rule and a tracked word, bottom-right: the corner the
                    // avatar and the primary action both leave empty.
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomEnd)
                            .padding(end = 18.dp, bottom = 16.dp),
                        horizontalAlignment = Alignment.End,
                        verticalArrangement = Arrangement.Bottom
                    ) {
                        Box(
                            modifier = Modifier
                                .width(26.dp)
                                .height(1.dp)
                                .drawBehind {
                                    drawRect(color = palette.accent.copy(alpha = 0.55f))
                                }
                        )
                        Text(
                            text = decoText.uppercase(),
                            modifier = Modifier.padding(top = 6.dp),
                            color = palette.ink.copy(alpha = 0.60f),
                            fontFamily = Poppins,
                            fontWeight = FontWeight.SemiBold,
                            fontSize = 10.sp,
                            letterSpacing = 0.34.em,
                            maxLines = 1,
                            overflow = TextOverflow.Clip,
                            softWrap = false
                        )
                    }
                }
            }
        }
    }
}
