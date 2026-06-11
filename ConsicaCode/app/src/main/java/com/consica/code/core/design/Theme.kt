package com.consica.code.core.design

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf

/** Exposes the user's reduced-motion preference to every composable. */
val LocalReducedMotion = staticCompositionLocalOf { false }

/** Exposes high-contrast so custom-drawn visuals (ecosystem, mascot) can adapt too. */
val LocalHighContrast = staticCompositionLocalOf { false }

/**
 * Root theme for Consica Code. Selects the standard or high-contrast Eco-Logic scheme, applies
 * the rounded typography (optionally text-scaled), and publishes reduced-motion / high-contrast
 * so individual components can respect accessibility settings.
 */
@Composable
fun ConsicaTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    highContrast: Boolean = false,
    reducedMotion: Boolean = false,
    fontScale: Float = 1f,
    content: @Composable () -> Unit,
) {
    val colors = when {
        highContrast && darkTheme -> EcoHighContrastDark
        highContrast -> EcoHighContrastLight
        darkTheme -> EcoDarkColors
        else -> EcoLightColors
    }
    CompositionLocalProvider(
        LocalReducedMotion provides reducedMotion,
        LocalHighContrast provides highContrast,
    ) {
        MaterialTheme(
            colorScheme = colors,
            typography = ecoTypography(fontScale),
            shapes = EcoShapes,
            content = content,
        )
    }
}
