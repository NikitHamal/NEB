package com.neb.ians.ui.theme

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember

/**
 * The journey palette expressed as a Material colour scheme, so Material's own
 * Expressive components — toggle buttons, button groups, loading indicators —
 * land in graphite without a colour argument at any call site.
 *
 * Every role that would normally carry a hue is mapped onto the ink ramp. Only
 * error keeps its red: a control that fails has to look different from a control
 * that is merely resting.
 */
@Composable
fun rememberNebColorScheme(palette: NebAuthPalette): ColorScheme = remember(palette) {
    val base = if (palette.isDark) darkColorScheme() else lightColorScheme()
    base.copy(
        primary = palette.accent,
        onPrimary = palette.onAccent,
        primaryContainer = palette.accentSoft,
        onPrimaryContainer = palette.ink,
        inversePrimary = palette.inkMuted,
        secondary = palette.ink,
        onSecondary = palette.onAccent,
        secondaryContainer = palette.field,
        onSecondaryContainer = palette.ink,
        tertiary = palette.inkMuted,
        onTertiary = palette.onAccent,
        tertiaryContainer = palette.field,
        onTertiaryContainer = palette.ink,
        background = palette.page,
        onBackground = palette.ink,
        surface = palette.page,
        onSurface = palette.ink,
        surfaceVariant = palette.field,
        onSurfaceVariant = palette.inkMuted,
        surfaceTint = palette.accent,
        inverseSurface = palette.ink,
        inverseOnSurface = palette.page,
        error = palette.danger,
        onError = palette.onAccent,
        errorContainer = palette.dangerSoft,
        onErrorContainer = palette.danger,
        outline = palette.hairlineStrong,
        outlineVariant = palette.hairline,
        surfaceDim = palette.field,
        surfaceBright = palette.page,
        surfaceContainerLowest = palette.page,
        surfaceContainerLow = palette.accentSoft,
        surfaceContainer = palette.field,
        surfaceContainerHigh = palette.accentSoft,
        surfaceContainerHighest = palette.hairline
    )
}
