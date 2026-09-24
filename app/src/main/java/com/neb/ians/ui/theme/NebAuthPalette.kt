package com.neb.ians.ui.theme

import androidx.compose.animation.core.CubicBezierEasing
import androidx.compose.animation.core.Easing
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

// ---------------------------------------------------------------------------
// Graphite — the mono palette the sign-in and onboarding journey is set in.
//
// The app proper runs on MaterialTheme. The journey does not: it is the only
// place where every surface, hairline and illustration has to agree pixel for
// pixel, so it carries its own flat palette instead of reaching into the
// colour scheme. Three rules hold it together.
//
//   Paper is the page, ink is the single voice of action, and every
//   illustration is drawn from one neutral ramp. There is no hue anywhere in
//   the journey except the one red kept for errors, because an error that
//   reads as ordinary text is not an error.
// ---------------------------------------------------------------------------

@Immutable
data class NebAuthPalette(
    val isDark: Boolean,
    val page: Color,
    val card: Color,
    val field: Color,
    val ink: Color,
    val inkMuted: Color,
    val inkFaint: Color,
    val hairline: Color,
    val hairlineStrong: Color,
    val accent: Color,
    val accentSoft: Color,
    val onAccent: Color,
    val artInk: Color,
    val artLine: Color,
    val artMid: Color,
    val artSoft: Color,
    val artFaint: Color,
    val danger: Color,
    val dangerSoft: Color,
    val success: Color,
    val successSoft: Color
) {
    /** The art ramp, darkest first, so an illustration can index a tone instead of naming one. */
    val artTones: List<Color> get() = listOf(artInk, artLine, artMid, artSoft, artFaint)
}

private val LightAuthPalette = NebAuthPalette(
    isDark = false,
    page = Color(0xFFFFFFFF),
    card = Color(0xFFFFFFFF),
    field = Color(0xFFF4F4F5),
    ink = Color(0xFF0A0A0B),
    inkMuted = Color(0xFF5C5C61),
    inkFaint = Color(0xFF9B9BA1),
    hairline = Color(0xFFE9E9EB),
    hairlineStrong = Color(0xFFD5D5D9),
    accent = Color(0xFF101012),
    accentSoft = Color(0xFFF1F1F3),
    onAccent = Color(0xFFFFFFFF),
    artInk = Color(0xFF141416),
    artLine = Color(0xFF6B6B72),
    artMid = Color(0xFFA3A3AA),
    artSoft = Color(0xFFD9D9DE),
    artFaint = Color(0xFFF0F0F2),
    danger = Color(0xFFB3261E),
    dangerSoft = Color(0xFFFBEDEC),
    success = Color(0xFF18181B),
    successSoft = Color(0xFFF1F1F3)
)

private val DarkAuthPalette = NebAuthPalette(
    isDark = true,
    page = Color(0xFF0C0C0D),
    card = Color(0xFF131315),
    field = Color(0xFF17171A),
    ink = Color(0xFFF5F5F6),
    inkMuted = Color(0xFFA1A1A8),
    inkFaint = Color(0xFF6E6E75),
    hairline = Color(0xFF222225),
    hairlineStrong = Color(0xFF313136),
    accent = Color(0xFFF5F5F6),
    accentSoft = Color(0xFF1C1C1F),
    onAccent = Color(0xFF0A0A0B),
    artInk = Color(0xFFE7E7E9),
    artLine = Color(0xFF9A9AA1),
    artMid = Color(0xFF64646B),
    artSoft = Color(0xFF2E2E33),
    artFaint = Color(0xFF1B1B1E),
    danger = Color(0xFFF2716A),
    dangerSoft = Color(0xFF2A1614),
    success = Color(0xFFE7E7E9),
    successSoft = Color(0xFF1C1C1F)
)

val LocalNebAuthPalette = staticCompositionLocalOf { LightAuthPalette }

fun nebAuthPalette(isDark: Boolean): NebAuthPalette =
    if (isDark) DarkAuthPalette else LightAuthPalette

/**
 * The palette for a journey screen. The journey is light by default and stays
 * light whatever the device is set to, because it runs straight out of the
 * splash and the auth landing, and both of those are locked to the light
 * artwork they are built around. Nothing between them may flip.
 */
@Composable
@ReadOnlyComposable
fun rememberNebAuthPalette(dark: Boolean = false): NebAuthPalette = nebAuthPalette(dark)

/**
 * The same palette for journey components reused inside the app proper, where
 * the user's own theme choice is in force. Derived from the Material surface so
 * a screen never has to thread a flag down to a control.
 */
@Composable
@ReadOnlyComposable
fun rememberNebSurfacePalette(): NebAuthPalette =
    nebAuthPalette(MaterialTheme.colorScheme.surface.luminance() < 0.5f)

private fun Color.luminance(): Float = 0.299f * red + 0.587f * green + 0.114f * blue

// ---------------------------------------------------------------------------
// Motion — one duration ladder and three curves, so a fade in one step and a
// slide in the next read as the same hand.
// ---------------------------------------------------------------------------

object NebMotion {
    const val Instant = 120
    const val Quick = 180
    const val Short = 240
    const val Standard = 320
    const val Emphasized = 400
    const val Slow = 560

    /** Entering: fast out of the gate, long settle. */
    val Decelerate: Easing = CubicBezierEasing(0.05f, 0.7f, 0.1f, 1f)

    /** Leaving: reluctant start, quick exit. */
    val Accelerate: Easing = CubicBezierEasing(0.3f, 0f, 0.8f, 0.15f)

    /** Both directions, for anything that moves without appearing. */
    val Standard_: Easing = CubicBezierEasing(0.2f, 0f, 0f, 1f)

    /** How far a step slides in from. Short enough to read as a shift, not a page. */
    const val StepSlideFraction = 0.22f

    /** A pressed control shrinks by this much. */
    const val PressScale = 0.97f

    /** Per-item delay when a list of fields arrives together. */
    const val StaggerStepMs = 45
    const val StaggerMaxItems = 7
}

// ---------------------------------------------------------------------------
// Geometry — the journey is built from three radii and one hairline.
// ---------------------------------------------------------------------------

object NebAuthTokens {
    val Hairline = 1.dp
    val FieldRadius = 16.dp
    val CardRadius = 20.dp
    val PillRadius = 28.dp
    val ControlHeight = 56.dp
    val FieldHeight = 58.dp
    val PageGutter = 24.dp
    val ArtClearance = 18.dp
    val StackGap = 14.dp
    val SectionGap = 28.dp
}
