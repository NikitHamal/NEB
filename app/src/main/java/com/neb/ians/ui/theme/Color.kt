package com.neb.ians.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.runtime.Immutable

// ---------------------------------------------------------------------------
// The NEBians palette.
//
// The app spent a release in pure graphite. The ramp is still here and still
// carries most of every screen — but the brand is a blue, the web has been that
// blue since the Django rewrite, and an app that drops it stops looking like the
// same product. So the hue is back, and it is the same hue the site ships:
// --md-primary in web/static/web/css/material3/01-tokens-typography.css.
//
// Three families, and a rule for each.
//
//   Brand   the blue. Primary, links, selection, the create button — anything
//           the user is meant to press or has just chosen. One hue, so pressing
//           always looks the same.
//   Steel   the blue's quieter relative, for secondary surfaces that should
//           belong to the brand without competing with it.
//   Violet  tertiary. Spent on the few places that need a third voice.
//
// Neutrals are no longer hue-free: they carry a few degrees of the brand's blue,
// which is what makes a grey card look like it belongs on a blue-accented page
// instead of sitting on it. Error keeps its red, for the reason it always did —
// an error that reads as ordinary text is not an error.
//
// What has NOT come back is hue as information. A subject still reads by its
// icon and its words first; the tint below is decoration on top of a label that
// already works in grey. And the sign-in journey's illustrations stay strictly
// ink-on-paper — see NebAuthPalette, where the art ramp is deliberately neutral.
// ---------------------------------------------------------------------------

/** The brand blue and its tonal neighbours. `B40` is the brand itself. */
private object Brand {
    val B10 = Color(0xFF00174B)
    val B20 = Color(0xFF002D78)
    val B30 = Color(0xFF003EA8)
    val B40 = Color(0xFF004AC6)
    val B50 = Color(0xFF0053DB)
    val B60 = Color(0xFF2E6BEA)
    val B70 = Color(0xFF6E9BFF)
    val B80 = Color(0xFFB4C5FF)
    val B90 = Color(0xFFDBE1FF)
    val B95 = Color(0xFFEDF0FF)
    val B98 = Color(0xFFF7F9FF)
}

/** The brand desaturated — secondary roles that should recede, not recolour. */
private object Steel {
    val S10 = Color(0xFF101C33)
    val S20 = Color(0xFF22324C)
    val S30 = Color(0xFF3F5A8A)
    val S40 = Color(0xFF4E6592)
    val S60 = Color(0xFF7B90B8)
    val S70 = Color(0xFF9CB7E8)
    val S80 = Color(0xFFC3D2EC)
    val S90 = Color(0xFFDDE6F6)
    val S95 = Color(0xFFEDF2FA)
}

/** The third voice. Used sparingly; never as the only cue for anything. */
private object Violet {
    val V20 = Color(0xFF3B1478)
    val V30 = Color(0xFF5B21B6)
    val V40 = Color(0xFF7C3AED)
    val V70 = Color(0xFFC4B5FD)
    val V90 = Color(0xFFEDE9FE)
    val V95 = Color(0xFFF5F2FF)
}

/**
 * The neutral ramp, carrying a few degrees of the brand's blue.
 *
 * `N0`..`N100` runs ink to paper as before, so the tonal relationships the mono
 * release established still hold — only the temperature changed.
 */
private object Neutral {
    val N0 = Color(0xFF000000)
    val N4 = Color(0xFF060A12)
    val N6 = Color(0xFF080D17)
    val N8 = Color(0xFF0B1220)
    val N10 = Color(0xFF0B1C30)
    val N12 = Color(0xFF111A2A)
    val N14 = Color(0xFF141E30)
    val N16 = Color(0xFF18233A)
    val N20 = Color(0xFF1D2A42)
    val N24 = Color(0xFF243149)
    val N28 = Color(0xFF2B3A55)
    val N32 = Color(0xFF30405D)
    val N36 = Color(0xFF394A69)
    val N40 = Color(0xFF43536F)
    val N48 = Color(0xFF52627E)
    val N52 = Color(0xFF5A6B88)
    val N60 = Color(0xFF6C7D9A)
    val N66 = Color(0xFF7B8CA8)
    val N72 = Color(0xFF97A5BC)
    val N78 = Color(0xFFAAB6C9)
    val N82 = Color(0xFFC4CDDC)
    val N86 = Color(0xFFD2D9E4)
    val N88 = Color(0xFFDADFE9)
    val N90 = Color(0xFFE1E6EE)
    val N92 = Color(0xFFE6EAF1)
    val N94 = Color(0xFFEAEEF4)
    val N95 = Color(0xFFEEF1F6)
    val N96 = Color(0xFFF1F3F7)
    val N97 = Color(0xFFF5F6F8)
    val N98 = Color(0xFFFAFBFC)
    val N100 = Color(0xFFFFFFFF)
}

/**
 * The brand blue, for the rare caller that has no composition to read a scheme
 * from. Prefer `MaterialTheme.colorScheme.primary` everywhere else — it flips
 * with the theme and this does not.
 */
val NebBrandBlue: Color = Brand.B40

/** The brand blue as it must appear on a dark surface. */
val NebBrandBlueOnDark: Color = Brand.B80

/** The brand blue resolved against whatever surface the caller is sitting on. */
@Composable
@ReadOnlyComposable
fun nebBrand(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) NebBrandBlueOnDark else NebBrandBlue

// Light theme — paper, with the brand blue as the voice of action
val md_theme_light_primary = Brand.B40
val md_theme_light_onPrimary = Neutral.N100
val md_theme_light_primaryContainer = Brand.B90
val md_theme_light_onPrimaryContainer = Brand.B10
val md_theme_light_secondary = Steel.S30
val md_theme_light_onSecondary = Neutral.N100
val md_theme_light_secondaryContainer = Steel.S90
val md_theme_light_onSecondaryContainer = Steel.S10
val md_theme_light_tertiary = Violet.V40
val md_theme_light_onTertiary = Neutral.N100
val md_theme_light_tertiaryContainer = Violet.V90
val md_theme_light_onTertiaryContainer = Violet.V20
val md_theme_light_error = Color(0xFFBA1A1A)
val md_theme_light_onError = Color(0xFFFFFFFF)
val md_theme_light_errorContainer = Color(0xFFFFDAD6)
val md_theme_light_onErrorContainer = Color(0xFF93000A)
val md_theme_light_background = Neutral.N97
val md_theme_light_onBackground = Neutral.N10
val md_theme_light_surface = Neutral.N97
val md_theme_light_onSurface = Neutral.N10
val md_theme_light_surfaceVariant = Neutral.N92
val md_theme_light_onSurfaceVariant = Neutral.N52
val md_theme_light_outline = Neutral.N72
val md_theme_light_outlineVariant = Neutral.N90
val md_theme_light_surfaceTint = Brand.B50
val md_theme_light_inverseOnSurface = Color(0xFFEAF1FF)
val md_theme_light_inverseSurface = Color(0xFF213145)
val md_theme_light_inversePrimary = Brand.B80
val md_theme_light_scrim = Neutral.N0
val md_theme_light_surfaceDim = Neutral.N88
val md_theme_light_surfaceBright = Neutral.N100
val md_theme_light_surfaceContainerLowest = Neutral.N100
val md_theme_light_surfaceContainerLow = Neutral.N98
val md_theme_light_surfaceContainer = Neutral.N95
val md_theme_light_surfaceContainerHigh = Neutral.N94
val md_theme_light_surfaceContainerHighest = Neutral.N90

// Dark theme — deep navy ink, with the brand's light blue as the voice of action
val md_theme_dark_primary = Brand.B80
val md_theme_dark_onPrimary = Brand.B20
val md_theme_dark_primaryContainer = Brand.B30
val md_theme_dark_onPrimaryContainer = Brand.B90
val md_theme_dark_secondary = Steel.S70
val md_theme_dark_onSecondary = Steel.S10
val md_theme_dark_secondaryContainer = Steel.S20
val md_theme_dark_onSecondaryContainer = Color(0xFFD6E3FF)
val md_theme_dark_tertiary = Violet.V70
val md_theme_dark_onTertiary = Violet.V20
val md_theme_dark_tertiaryContainer = Violet.V30
val md_theme_dark_onTertiaryContainer = Violet.V90
val md_theme_dark_error = Color(0xFFFFB4AB)
val md_theme_dark_onError = Color(0xFF690005)
val md_theme_dark_errorContainer = Color(0xFF93000A)
val md_theme_dark_onErrorContainer = Color(0xFFFFDAD6)
val md_theme_dark_background = Neutral.N10
val md_theme_dark_onBackground = Color(0xFFE5EEFF)
val md_theme_dark_surface = Neutral.N10
val md_theme_dark_onSurface = Color(0xFFE5EEFF)
val md_theme_dark_surfaceVariant = Neutral.N28
val md_theme_dark_onSurfaceVariant = Neutral.N82
val md_theme_dark_outline = Neutral.N60
val md_theme_dark_outlineVariant = Neutral.N28
val md_theme_dark_surfaceTint = Brand.B80
val md_theme_dark_inverseOnSurface = Neutral.N10
val md_theme_dark_inverseSurface = Color(0xFFE5EEFF)
val md_theme_dark_inversePrimary = Brand.B40
val md_theme_dark_scrim = Neutral.N0
val md_theme_dark_surfaceDim = Neutral.N8
val md_theme_dark_surfaceBright = Neutral.N32
val md_theme_dark_surfaceContainerLowest = Neutral.N4
val md_theme_dark_surfaceContainerLow = Neutral.N12
val md_theme_dark_surfaceContainer = Neutral.N16
val md_theme_dark_surfaceContainerHigh = Neutral.N24
val md_theme_dark_surfaceContainerHighest = Neutral.N32

// Fixed accents — identical in both themes, for anything that must not flip
val md_theme_primaryFixed = Brand.B90
val md_theme_primaryFixedDim = Brand.B80
val md_theme_onPrimaryFixed = Brand.B10
val md_theme_onPrimaryFixedVariant = Brand.B30
val md_theme_secondaryFixed = Steel.S90
val md_theme_secondaryFixedDim = Steel.S80
val md_theme_onSecondaryFixed = Steel.S10
val md_theme_onSecondaryFixedVariant = Steel.S30
val md_theme_tertiaryFixed = Violet.V90
val md_theme_tertiaryFixedDim = Violet.V70
val md_theme_onTertiaryFixed = Violet.V20
val md_theme_onTertiaryFixedVariant = Violet.V30

/**
 * How a subject, category or level is dressed.
 *
 * The tint is a second cue, never the only one. Every place that reads this also
 * shows the subject's icon and its name, which is what the user actually reads —
 * so nobody has to learn that teal means Biology. Unknown subjects fall back to
 * the brand, which is why the map needs no default entry per screen.
 */
data class SubjectTheme(
    val color: Color,
    val container: Color,
    val onContainer: Color
)

private data class SubjectHue(
    val light: Color,
    val lightContainer: Color,
    val onLightContainer: Color,
    val dark: Color,
    val darkContainer: Color,
    val onDarkContainer: Color
)

/**
 * One entry per subject the curriculum actually has. Light values are the web's
 * subject classes; dark values are the same hue lifted into the range that stays
 * legible on navy, because the light ones do not.
 */
private val SubjectHues: Map<String, SubjectHue> = mapOf(
    "Physics" to SubjectHue(
        Color(0xFF1D4ED8), Color(0xFFDBE7FE), Color(0xFF1B3FA8),
        Color(0xFF9DBBFF), Color(0xFF1B2A4D), Color(0xFFD6E3FF)
    ),
    "Chemistry" to SubjectHue(
        Color(0xFF15803D), Color(0xFFDCFCE7), Color(0xFF14602F),
        Color(0xFF7CD9A0), Color(0xFF14301F), Color(0xFFD3F5DF)
    ),
    "Mathematics" to SubjectHue(
        Color(0xFFB91C1C), Color(0xFFFEE2E2), Color(0xFF8F1717),
        Color(0xFFFF9C93), Color(0xFF3A1A18), Color(0xFFFFDAD6)
    ),
    "Biology" to SubjectHue(
        Color(0xFF0F766E), Color(0xFFCCFBF1), Color(0xFF0C5B55),
        Color(0xFF5FD3C4), Color(0xFF10302D), Color(0xFFCDF3ED)
    ),
    "English" to SubjectHue(
        Color(0xFF7E22CE), Color(0xFFF3E8FF), Color(0xFF631AA3),
        Color(0xFFD3B4FE), Color(0xFF2C1A44), Color(0xFFEDE0FF)
    ),
    "Nepali" to SubjectHue(
        Color(0xFF9A6206), Color(0xFFFEF3C7), Color(0xFF7A4E05),
        Color(0xFFE8B457), Color(0xFF32260E), Color(0xFFF7E6C2)
    ),
    "Computer Science" to SubjectHue(
        Color(0xFF0E7490), Color(0xFFCFFAFE), Color(0xFF0B5A70),
        Color(0xFF5CC8E0), Color(0xFF0E2C36), Color(0xFFC9EFF8)
    ),
    "Economics" to SubjectHue(
        Color(0xFFC2410C), Color(0xFFFFEDD5), Color(0xFF9A330A),
        Color(0xFFFFA76B), Color(0xFF3A2013), Color(0xFFFFE0CB)
    ),
    "Accountancy" to SubjectHue(
        Color(0xFF9D174D), Color(0xFFFCE7F3), Color(0xFF7D1240),
        Color(0xFFF79CC0), Color(0xFF3A1428), Color(0xFFFBDCE9)
    ),
    "Exam Tips" to SubjectHue(
        Color(0xFF6D28D9), Color(0xFFEDE9FE), Color(0xFF56209F),
        Color(0xFFC4B5FD), Color(0xFF261C46), Color(0xFFE6E0FF)
    )
)

private val BrandSubjectHue = SubjectHue(
    Brand.B40, Brand.B90, Brand.B10,
    Brand.B80, Steel.S20, Brand.B90
)

private fun subjectHue(subject: String): SubjectHue =
    SubjectHues[subject]
        ?: SubjectHues.entries.firstOrNull { it.key.equals(subject, ignoreCase = true) }?.value
        ?: BrandSubjectHue

@Composable
@ReadOnlyComposable
fun getSubjectTheme(subject: String): SubjectTheme {
    val hue = subjectHue(subject)
    return if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) {
        SubjectTheme(hue.dark, hue.darkContainer, hue.onDarkContainer)
    } else {
        SubjectTheme(hue.light, hue.lightContainer, hue.onLightContainer)
    }
}

@Composable
@ReadOnlyComposable
fun getSubjectColor(subject: String): Color = getSubjectTheme(subject).color

/**
 * The brand where there is no composition to read it from — a media
 * notification, a service, a value cached in a view model. The brand blue rather
 * than a subject's own hue, because whatever reads this cannot know which
 * surface it will be drawn on and the blue is the one that holds up on both.
 */
val SubjectAccentStatic: Color = Brand.B40

fun subjectAccentArgb(): Long = 0xFF004AC6L

// ---------------------------------------------------------------------------
// Accents.
//
// The brand blue is the voice of action and the ramp carries the page. These
// hues are for the places where several choices sit side by side and the user is
// picking between them rather than reading them — the create menu is the case
// that asked for them, and the resource actions followed.
//
// Each carries a light and a dark value so the contrast holds either way, and
// none of them is load-bearing: nothing is knowable only by its hue.
// ---------------------------------------------------------------------------

@Immutable
data class NebAccent(val light: Color, val dark: Color)

object NebAccents {
    /** The brand itself, for the accent slot that should read as "the app". */
    val Brand = NebAccent(Color(0xFF004AC6), Color(0xFFB4C5FF))
    val Indigo = NebAccent(Color(0xFF4F46E5), Color(0xFFB4B0FF))
    val Violet = NebAccent(Color(0xFF7C3AED), Color(0xFFC9B6FE))
    val Amber = NebAccent(Color(0xFF9A6206), Color(0xFFE8B457))
    val Teal = NebAccent(Color(0xFF0F766E), Color(0xFF5FD3C4))
    val Green = NebAccent(Color(0xFF15803D), Color(0xFF7CD9A0))
    val Cyan = NebAccent(Color(0xFF0E7490), Color(0xFF5CC8E0))
    val Rose = NebAccent(Color(0xFFB3261E), Color(0xFFFF9186))
    val Pink = NebAccent(Color(0xFF9D174D), Color(0xFFF79CC0))
}

@Composable
fun NebAccent.resolve(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) dark else light
