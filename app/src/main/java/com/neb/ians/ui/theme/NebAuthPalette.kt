package com.neb.ians.ui.theme

import androidx.compose.animation.core.CubicBezierEasing
import androidx.compose.animation.core.Easing
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

// ---------------------------------------------------------------------------
// Sapphire & Snow — the palette the sign-in and onboarding journey is set in.
//
// The app proper runs on MaterialTheme. The journey does not: it is the only
// place where every surface, hairline and illustration has to agree pixel for
// pixel, so it carries its own flat palette instead of reaching into the
// colour scheme. Three rules hold it together.
//
//   Snow is the page, sapphire is the single voice of action, and the four
//   landscape accents (everest, rhododendron, marigold, dusk) belong to
//   illustrations only — never to text, never to a control.
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
    val sapphire: Color,
    val sapphireSoft: Color,
    val onSapphire: Color,
    val everest: Color,
    val rhododendron: Color,
    val marigold: Color,
    val dusk: Color,
    val danger: Color,
    val dangerSoft: Color,
    val success: Color,
    val successSoft: Color
) {
    /** Illustration accents in drawing order, so art can index instead of naming. */
    val accents: List<Color> get() = listOf(sapphire, everest, rhododendron, marigold, dusk)
}

private val LightAuthPalette = NebAuthPalette(
    isDark = false,
    page = Color(0xFFFFFFFF),
    card = Color(0xFFFFFFFF),
    field = Color(0xFFF7F9FC),
    ink = Color(0xFF0B1220),
    inkMuted = Color(0xFF5B6B85),
    inkFaint = Color(0xFF94A3B8),
    hairline = Color(0xFFE7ECF4),
    hairlineStrong = Color(0xFFD3DCE8),
    sapphire = Color(0xFF0D5CE5),
    sapphireSoft = Color(0xFFEBF2FE),
    onSapphire = Color(0xFFFFFFFF),
    everest = Color(0xFF0E9F8F),
    rhododendron = Color(0xFFE0396B),
    marigold = Color(0xFFF5A524),
    dusk = Color(0xFF7C3AED),
    danger = Color(0xFFDC2626),
    dangerSoft = Color(0xFFFEF0F0),
    success = Color(0xFF16A34A),
    successSoft = Color(0xFFEDFBF1)
)

private val DarkAuthPalette = NebAuthPalette(
    isDark = true,
    page = Color(0xFF0B0F17),
    card = Color(0xFF131A25),
    field = Color(0xFF151D2A),
    ink = Color(0xFFEEF3FA),
    inkMuted = Color(0xFF9BABC4),
    inkFaint = Color(0xFF64748B),
    hairline = Color(0xFF1F2836),
    hairlineStrong = Color(0xFF2D3A4D),
    sapphire = Color(0xFF7CA8FF),
    sapphireSoft = Color(0xFF14243F),
    onSapphire = Color(0xFF041A42),
    everest = Color(0xFF3ED8C5),
    rhododendron = Color(0xFFFF7FA3),
    marigold = Color(0xFFFFC65C),
    dusk = Color(0xFFC4B5FD),
    danger = Color(0xFFFF8A80),
    dangerSoft = Color(0xFF2A1618),
    success = Color(0xFF4ADE80),
    successSoft = Color(0xFF12241A)
)

val LocalNebAuthPalette = staticCompositionLocalOf { LightAuthPalette }

fun nebAuthPalette(isDark: Boolean): NebAuthPalette =
    if (isDark) DarkAuthPalette else LightAuthPalette

/**
 * The palette for a journey screen. Pass [forceLight] on the screens that are
 * locked to light mode regardless of the device (splash, auth landing) so they
 * stay identical to the hero artwork they sit under.
 */
@Composable
@ReadOnlyComposable
fun rememberNebAuthPalette(forceLight: Boolean = false): NebAuthPalette =
    if (forceLight) LightAuthPalette else nebAuthPalette(isSystemInDarkTheme())

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
    val StackGap = 14.dp
    val SectionGap = 28.dp
}
