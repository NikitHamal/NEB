package com.neb.ians.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.theme.Poppins

/**
 * Animated, role-themed profile banner — pixel-parity port of the web
 * `.pf-card-banner` presets (gradient drift + diagonal shine + uppercase
 * deco watermark text). When [bannerUrl] is set, the custom image wins.
 */

import androidx.compose.ui.graphics.RectangleShape

private val BannerTopShape = RectangleShape

/** Per-preset gradient stops — one graphite wash per role, depth instead of hue. */
private fun bannerColorsFor(bannerType: String): List<Color> = when (bannerType) {
    "gradient-admin" -> listOf(Color(0xFF000000), Color(0xFF131315), Color(0xFF26262A), Color(0xFF3A3A3F))
    "gradient-moderator" -> listOf(Color(0xFF0C0C0D), Color(0xFF1F1F21), Color(0xFF313136), Color(0xFF57575C))
    "gradient-verified" -> listOf(Color(0xFF131315), Color(0xFF26262A), Color(0xFF47474B), Color(0xFF6E6E75))
    "gradient-bot" -> listOf(Color(0xFF0A0A0B), Color(0xFF18181B), Color(0xFF2E2E32), Color(0xFF5C5C61))
    "gradient-tutor" -> listOf(Color(0xFF101012), Color(0xFF1F1F21), Color(0xFF3A3A3F), Color(0xFF5C5C61))
    "gradient-institution" -> listOf(Color(0xFF070708), Color(0xFF17171A), Color(0xFF26262A), Color(0xFF47474B))
    else -> listOf(Color(0xFF0C0C0D), Color(0xFF1F1F21), Color(0xFF2E2E32), Color(0xFF47474B))
}

/** Deco watermark text alpha per preset (web tweaks contrast per gradient). */
private fun decoAlphaFor(bannerType: String): Float = when (bannerType) {
    "gradient-tutor" -> 0.28f
    "gradient-bot", "gradient-admin" -> 0.25f
    "gradient-moderator" -> 0.22f
    "gradient-verified" -> 0.20f
    else -> 0.18f
}

private fun decoFontSizeFor(bannerType: String): TextUnit =
    if (bannerType == "gradient-tutor") 40.sp else 28.sp

private fun decoLetterSpacingFor(bannerType: String): TextUnit =
    if (bannerType == "gradient-tutor") 0.30.em else 0.22.em

/**
 * Picks the role-themed banner preset + deco text for a profile, mirroring
 * the web's `views_profile.py` default-banner priority:
 * bot → admin → moderator → verified → teacher → institution → default.
 *
 * @return Pair(bannerType, decoText)
 */
fun bannerPresetFor(profile: UserProfileResponse): Pair<String, String> = when {
    profile.isBot -> "gradient-bot" to "neby ai"
    profile.isAdmin -> "gradient-admin" to "admin"
    profile.moderatorLevel > 0 -> "gradient-moderator" to "moderator"
    profile.verificationLevel > 0 -> "gradient-verified" to "nebian"
    profile.role == "teacher" -> "gradient-tutor" to "tutor"
    profile.role == "institution" -> "gradient-institution" to "nebian"
    else -> "" to "nebian"
}

@Composable
fun ProfileBanner(
    bannerUrl: String?,
    bannerType: String,
    decoText: String,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .height(160.dp)
            .clip(BannerTopShape)
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
        } else {
            val colors = remember(bannerType) { bannerColorsFor(bannerType) }
            val transition = rememberInfiniteTransition(label = "bannerDrift")

            // Gradient drift — mirrors the web's `bannerGradientDrift` keyframes
            // (18s linear alternate) by sliding the linear gradient's start/end.
            val drift by transition.animateFloat(
                initialValue = 0f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 18_000, easing = LinearEasing),
                    repeatMode = RepeatMode.Reverse
                ),
                label = "drift"
            )

            // Diagonal shine strip — slow 9s loop, single brush, cheap to draw.
            val shine by transition.animateFloat(
                initialValue = 0f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 9_000, easing = LinearEasing),
                    repeatMode = RepeatMode.Restart
                ),
                label = "shine"
            )

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .drawBehind {
                        val w = size.width
                        val h = size.height
                        // Slide gradient anchors horizontally by up to 40% width.
                        val shift = w * 0.4f * drift
                        drawRect(
                            brush = Brush.linearGradient(
                                colors = colors,
                                start = Offset(-shift, 0f),
                                end = Offset(w * 1.4f - shift, h)
                            )
                        )
                        // Translating diagonal white shine strip at low alpha.
                        val stripWidth = w * 0.45f
                        val travel = w + stripWidth * 2f
                        val x = travel * shine - stripWidth
                        drawRect(
                            brush = Brush.linearGradient(
                                colors = listOf(
                                    Color.Transparent,
                                    Color.White.copy(alpha = 0.08f),
                                    Color.Transparent
                                ),
                                start = Offset(x, h),
                                end = Offset(x + stripWidth, 0f)
                            )
                        )
                    }
            )

            // Large uppercase deco watermark, centered.
            if (decoText.isNotBlank()) {
                Text(
                    text = decoText.uppercase(),
                    modifier = Modifier
                        .align(Alignment.Center),
                    color = Color.White.copy(alpha = decoAlphaFor(bannerType)),
                    fontFamily = Poppins,
                    fontWeight = FontWeight.ExtraBold,
                    fontSize = decoFontSizeFor(bannerType),
                    letterSpacing = decoLetterSpacingFor(bannerType),
                    maxLines = 1,
                    overflow = TextOverflow.Clip,
                    softWrap = false
                )
            }
        }
    }
}
