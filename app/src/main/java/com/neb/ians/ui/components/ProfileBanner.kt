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
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.statusBars
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
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.neb.ians.data.api.UserProfileResponse
import com.neb.ians.ui.theme.Poppins
import com.neb.ians.ui.theme.nebAnimationsReduced
import com.neb.ians.util.rememberIsLowEndDevice

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

/** Width over height of the cover frame: 2.4 : 1 on phones, 3 : 1 from 600dp (the site's `--cover-ratio`). One rectangle, never clamped. */
fun profileCoverRatio(width: androidx.compose.ui.unit.Dp): Float = if (width.value >= 600f) 3f else 2.4f

/**
 * The profile cover frame: an exact rectangle of [profileCoverRatio], the art only. The status bar is not part of it: the frame
 * starts below the bar, so it is the same rectangle on the profile, in Edit profile and in the picker. [statusTop] is kept for
 * callers that still pass it; it no longer changes the height.
 */
@Suppress("UNUSED_PARAMETER")
fun profileCoverHeight(width: androidx.compose.ui.unit.Dp, statusTop: androidx.compose.ui.unit.Dp): androidx.compose.ui.unit.Dp =
    width / profileCoverRatio(width)

/** Width over height of the cover frame at [width]. Picker tiles use it so a tile is the cover as it will look. */
fun profileCoverAspect(width: androidx.compose.ui.unit.Dp): Float = profileCoverRatio(width)

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
    modifier: Modifier = Modifier,
    coverArt: String? = null
) {
    BoxWithConstraints(modifier = modifier) {
        val statusTop = WindowInsets.statusBars.asPaddingValues().calculateTopPadding()
        val coverHeight = profileCoverHeight(maxWidth, statusTop)

        Box(Modifier.fillMaxWidth().padding(top = statusTop)) {
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
                // The member's pick from the M3X art library (v7 covers), else a stable one from the
                // username. Drawn by code (M3xArt.kt); it settles once when it first shows, then stays still.
                M3xCover(coverId = coverArt, username = seedKey, modifier = Modifier.fillMaxSize(), live = true)
            }
        }
        }
    }
}
