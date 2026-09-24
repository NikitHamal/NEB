package com.neb.ians.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.runtime.Immutable

// ---------------------------------------------------------------------------
// Graphite, for the whole app.
//
// One neutral ramp runs from paper to ink and every colour role is a stop on
// it. Nothing is hue-coded: a subject is not blue, a level is not green, a
// category is not purple. What separates two things on screen is tone, weight,
// shape and the icon beside them — never a colour the user has to learn.
//
// Red survives in exactly one place, the error roles, because an error that
// reads as ordinary text is not an error.
//
// The ramp is deliberately the same family as NebAuthPalette, which the sign-in
// and onboarding journey is set in, so crossing from the journey into the feed
// is not a change of material.
// ---------------------------------------------------------------------------

private object Graphite {
    val N0 = Color(0xFF000000)
    val N4 = Color(0xFF070708)
    val N6 = Color(0xFF0A0A0B)
    val N8 = Color(0xFF0C0C0D)
    val N10 = Color(0xFF101012)
    val N12 = Color(0xFF131315)
    val N14 = Color(0xFF17171A)
    val N16 = Color(0xFF18181B)
    val N20 = Color(0xFF1F1F21)
    val N24 = Color(0xFF26262A)
    val N28 = Color(0xFF2E2E32)
    val N32 = Color(0xFF313136)
    val N36 = Color(0xFF3A3A3F)
    val N40 = Color(0xFF47474B)
    val N48 = Color(0xFF57575C)
    val N52 = Color(0xFF5C5C61)
    val N60 = Color(0xFF6E6E75)
    val N66 = Color(0xFF7C7C83)
    val N72 = Color(0xFF9B9BA1)
    val N78 = Color(0xFFA1A1A8)
    val N82 = Color(0xFFC9C9CD)
    val N86 = Color(0xFFD5D5D9)
    val N88 = Color(0xFFDCDCE0)
    val N90 = Color(0xFFE3E3E7)
    val N92 = Color(0xFFE9E9EB)
    val N94 = Color(0xFFEAEAED)
    val N95 = Color(0xFFF1F1F3)
    val N96 = Color(0xFFF4F4F5)
    val N97 = Color(0xFFF7F7F9)
    val N98 = Color(0xFFFAFAFB)
    val N100 = Color(0xFFFFFFFF)
}

// Light theme — paper, with ink as the only voice of action
val md_theme_light_primary = Graphite.N10
val md_theme_light_onPrimary = Graphite.N100
val md_theme_light_primaryContainer = Graphite.N90
val md_theme_light_onPrimaryContainer = Graphite.N10
val md_theme_light_secondary = Graphite.N40
val md_theme_light_onSecondary = Graphite.N100
val md_theme_light_secondaryContainer = Graphite.N94
val md_theme_light_onSecondaryContainer = Graphite.N24
val md_theme_light_tertiary = Graphite.N52
val md_theme_light_onTertiary = Graphite.N100
val md_theme_light_tertiaryContainer = Graphite.N95
val md_theme_light_onTertiaryContainer = Graphite.N32
val md_theme_light_error = Color(0xFFB3261E)
val md_theme_light_onError = Color(0xFFFFFFFF)
val md_theme_light_errorContainer = Color(0xFFFBEDEC)
val md_theme_light_onErrorContainer = Color(0xFF7A1C16)
val md_theme_light_background = Graphite.N97
val md_theme_light_onBackground = Graphite.N6
val md_theme_light_surface = Graphite.N97
val md_theme_light_onSurface = Graphite.N6
val md_theme_light_surfaceVariant = Graphite.N92
val md_theme_light_onSurfaceVariant = Graphite.N52
val md_theme_light_outline = Graphite.N72
val md_theme_light_outlineVariant = Graphite.N92
val md_theme_light_surfaceTint = Graphite.N10
val md_theme_light_inverseOnSurface = Graphite.N96
val md_theme_light_inverseSurface = Graphite.N20
val md_theme_light_inversePrimary = Graphite.N82
val md_theme_light_scrim = Graphite.N0
val md_theme_light_surfaceDim = Graphite.N88
val md_theme_light_surfaceBright = Graphite.N100
val md_theme_light_surfaceContainerLowest = Graphite.N100
val md_theme_light_surfaceContainerLow = Graphite.N98
val md_theme_light_surfaceContainer = Graphite.N95
val md_theme_light_surfaceContainerHigh = Graphite.N94
val md_theme_light_surfaceContainerHighest = Graphite.N90

// Dark theme — ink, with paper as the only voice of action
val md_theme_dark_primary = Color(0xFFF5F5F6)
val md_theme_dark_onPrimary = Graphite.N6
val md_theme_dark_primaryContainer = Graphite.N28
val md_theme_dark_onPrimaryContainer = Graphite.N90
val md_theme_dark_secondary = Graphite.N82
val md_theme_dark_onSecondary = Graphite.N20
val md_theme_dark_secondaryContainer = Graphite.N24
val md_theme_dark_onSecondaryContainer = Graphite.N88
val md_theme_dark_tertiary = Graphite.N78
val md_theme_dark_onTertiary = Graphite.N14
val md_theme_dark_tertiaryContainer = Graphite.N20
val md_theme_dark_onTertiaryContainer = Graphite.N86
val md_theme_dark_error = Color(0xFFF2716A)
val md_theme_dark_onError = Color(0xFF4A0F0B)
val md_theme_dark_errorContainer = Color(0xFF2A1614)
val md_theme_dark_onErrorContainer = Color(0xFFFFDAD6)
val md_theme_dark_background = Graphite.N8
val md_theme_dark_onBackground = Color(0xFFF5F5F6)
val md_theme_dark_surface = Graphite.N8
val md_theme_dark_onSurface = Color(0xFFF5F5F6)
val md_theme_dark_surfaceVariant = Graphite.N24
val md_theme_dark_onSurfaceVariant = Graphite.N78
val md_theme_dark_outline = Graphite.N60
val md_theme_dark_outlineVariant = Graphite.N24
val md_theme_dark_surfaceTint = Color(0xFFF5F5F6)
val md_theme_dark_inverseOnSurface = Graphite.N14
val md_theme_dark_inverseSurface = Color(0xFFE7E7E9)
val md_theme_dark_inversePrimary = Graphite.N40
val md_theme_dark_scrim = Graphite.N0
val md_theme_dark_surfaceDim = Graphite.N6
val md_theme_dark_surfaceBright = Graphite.N36
val md_theme_dark_surfaceContainerLowest = Graphite.N4
val md_theme_dark_surfaceContainerLow = Graphite.N12
val md_theme_dark_surfaceContainer = Graphite.N16
val md_theme_dark_surfaceContainerHigh = Graphite.N24
val md_theme_dark_surfaceContainerHighest = Graphite.N32

// Fixed accents — identical in both themes, for anything that must not flip
val md_theme_primaryFixed = Graphite.N90
val md_theme_primaryFixedDim = Graphite.N82
val md_theme_onPrimaryFixed = Graphite.N6
val md_theme_onPrimaryFixedVariant = Graphite.N40
val md_theme_secondaryFixed = Graphite.N94
val md_theme_secondaryFixedDim = Graphite.N86
val md_theme_onSecondaryFixed = Graphite.N12
val md_theme_onSecondaryFixedVariant = Graphite.N40
val md_theme_tertiaryFixed = Graphite.N95
val md_theme_tertiaryFixedDim = Graphite.N88
val md_theme_onTertiaryFixed = Graphite.N20
val md_theme_onTertiaryFixedVariant = Graphite.N52

/**
 * How a subject, category or level is dressed.
 *
 * It used to be a hue per subject — Physics blue, Chemistry green, Mathematics
 * red — which meant eleven colours competing on one screen and a legend the
 * user had to hold in their head. Every subject now wears the same ink, and
 * what tells them apart is the icon and the words, which were already there.
 */
data class SubjectTheme(
    val color: Color,
    val container: Color,
    val onContainer: Color
)

@Composable
@ReadOnlyComposable
fun getSubjectTheme(subject: String): SubjectTheme {
    val scheme = MaterialTheme.colorScheme
    return SubjectTheme(
        color = scheme.onSurface,
        container = scheme.surfaceContainerHigh,
        onContainer = scheme.onSurface
    )
}

@Composable
@ReadOnlyComposable
fun getSubjectColor(subject: String): Color = MaterialTheme.colorScheme.onSurface

/**
 * The same accent where there is no composition to read it from — a media
 * notification, a service, a value cached in a view model. Chosen to hold up on
 * both paper and ink, since whatever reads it cannot know which one it is on.
 */
val SubjectAccentStatic: Color = Graphite.N48

fun subjectAccentArgb(): Long = 0xFF57575CL

// ---------------------------------------------------------------------------
// Accents, spent sparingly.
//
// The ramp above still carries the app. These four hues exist for the few
// places where several choices are presented at once and the user is picking
// between them rather than reading them — the create menu is the case that
// asked for them. Each is desaturated enough to sit on graphite without
// shouting, and carries a light and a dark value so the contrast against a
// tinted container holds either way.
//
// They are never load-bearing: nothing is only knowable by its hue.
// ---------------------------------------------------------------------------

@Immutable
data class NebAccent(val light: Color, val dark: Color)

object NebAccents {
    val Indigo = NebAccent(Color(0xFF4A42D6), Color(0xFFA9A3FF))
    val Amber = NebAccent(Color(0xFF8F5507), Color(0xFFE5A84C))
    val Teal = NebAccent(Color(0xFF0B6A62), Color(0xFF4FD3C0))
    val Rose = NebAccent(Color(0xFFA8271F), Color(0xFFFF9186))
}

@Composable
fun NebAccent.resolve(): Color =
    if (MaterialTheme.colorScheme.surface.luminance() < 0.5f) dark else light
