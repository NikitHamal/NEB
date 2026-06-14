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

private val BannerTopShape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)

/** Per-preset gradient color stops, matching the web CSS presets exactly. */
private fun bannerColorsFor(bannerType: String): List<Color> = when (bannerType) {
    "gradient-admin" -> listOf(Color(0xFF78350F), Color(0xFFB45309), Color(0xFFD97706), Color(0xFFF59E0B))
    "gradient-moderator" -> listOf(Color(0xFF0F766E), Color(0xFF0D9488), Color(0xFF14B8A6), Color(0xFF06B6D4))
    "gradient-verified" -> listOf(Color(0xFF0369A1), Color(0xFF0284C7), Color(0xFF0EA5E9), Color(0xFF38BDF8))
    "gradient-bot" -> listOf(Color(0xFF4A148C), Color(0xFF6200EA), Color(0xFF7C4DFF), Color(0xFFB388FF))
    "gradient-tutor" -> listOf(Color(0xFF064E3B), Color(0xFF047857), Color(0xFF10B981), Color(0xFF34D399))
    "gradient-institution" -> listOf(Color(0xFF312E81), Color(0xFF4338CA), Color(0xFF6366F1), Color(0xFF818CF8))
    // Default brand blue
    else -> listOf(Color(0xFF004AC6), Color(0xFF2563EB), Color(0xFF4F46E5), Color(0xFF0EA5E9))
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
