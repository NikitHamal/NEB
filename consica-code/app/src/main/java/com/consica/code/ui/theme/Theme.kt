package com.consica.code.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

/** True when the learner enabled the reduced-motion accessibility setting. */
val LocalReducedMotion = staticCompositionLocalOf { false }

/** True when the learner enabled high-contrast mode. */
val LocalHighContrast = staticCompositionLocalOf { false }

private val LightColors = lightColorScheme(
    primary = ForestGreen,
    onPrimary = CleanWhite,
    primaryContainer = LeafContainer,
    onPrimaryContainer = DeepForest,
    secondary = RiverBlue,
    onSecondary = CleanWhite,
    secondaryContainer = RiverContainer,
    onSecondaryContainer = Color(0xFF0E3A52),
    tertiary = Color(0xFFB07C00),
    onTertiary = CleanWhite,
    tertiaryContainer = SunContainer,
    onTertiaryContainer = Color(0xFF4A3A00),
    background = LeafLight,
    onBackground = SoilDark,
    surface = CleanWhite,
    onSurface = SoilDark,
    surfaceVariant = Color(0xFFF1F7F1),
    onSurfaceVariant = Color(0xFF45504A),
    outline = StoneGray,
    outlineVariant = Color(0xFFD4DFD5),
    error = ErrorRed,
    onError = CleanWhite,
    errorContainer = ErrorContainerLight,
    onErrorContainer = Color(0xFF410002),
    surfaceContainerLowest = CleanWhite,
    surfaceContainerLow = Color(0xFFF6FBF6),
    surfaceContainer = Color(0xFFF0F7F0),
    surfaceContainerHigh = Color(0xFFEAF3EA),
    surfaceContainerHighest = Color(0xFFE3EEE4),
    inverseSurface = Color(0xFF2C322C),
    inverseOnSurface = Color(0xFFEDF2ED),
    inversePrimary = NightLeaf,
    scrim = Color(0xFF000000),
)

private val HighContrastLightColors = LightColors.copy(
    primary = DeepForest,
    onPrimaryContainer = Color(0xFF0A1F08),
    onBackground = Color(0xFF000000),
    onSurface = Color(0xFF000000),
    onSurfaceVariant = Color(0xFF20281F),
    outline = Color(0xFF3C4A42),
    secondary = Color(0xFF115A82),
)

private val DarkColors = darkColorScheme(
    primary = NightLeaf,
    onPrimary = DeepForest,
    primaryContainer = Color(0xFF2A4226),
    onPrimaryContainer = Color(0xFFC4E8C7),
    secondary = Color(0xFF8FCBEC),
    onSecondary = Color(0xFF0E3A52),
    secondaryContainer = Color(0xFF1E4258),
    onSecondaryContainer = Color(0xFFCAE6F7),
    tertiary = SunYellow,
    onTertiary = Color(0xFF3C2F00),
    tertiaryContainer = Color(0xFF564500),
    onTertiaryContainer = Color(0xFFFFE08D),
    background = NightSoil,
    onBackground = NightText,
    surface = NightSurface,
    onSurface = NightText,
    surfaceVariant = NightSurfaceHigh,
    onSurfaceVariant = Color(0xFFBCC9BD),
    outline = Color(0xFF87938A),
    outlineVariant = Color(0xFF3C463D),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    surfaceContainerLowest = Color(0xFF0C120C),
    surfaceContainerLow = Color(0xFF171F17),
    surfaceContainer = Color(0xFF1B231B),
    surfaceContainerHigh = Color(0xFF243024),
    surfaceContainerHighest = Color(0xFF2E3B2E),
    inverseSurface = NightText,
    inverseOnSurface = Color(0xFF2C322C),
    inversePrimary = ForestGreen,
    scrim = Color(0xFF000000),
)

private val HighContrastDarkColors = DarkColors.copy(
    primary = Color(0xFFCDEFCF),
    onBackground = Color(0xFFFFFFFF),
    onSurface = Color(0xFFFFFFFF),
    onSurfaceVariant = Color(0xFFDDE8DE),
    outline = Color(0xFFB9C6BC),
)

@Composable
fun CcodeTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    highContrast: Boolean = false,
    reducedMotion: Boolean = false,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        darkTheme && highContrast -> HighContrastDarkColors
        darkTheme -> DarkColors
        highContrast -> HighContrastLightColors
        else -> LightColors
    }
    CompositionLocalProvider(
        LocalReducedMotion provides reducedMotion,
        LocalHighContrast provides highContrast,
    ) {
        MaterialTheme(
            colorScheme = colorScheme,
            typography = CcodeTypography,
            shapes = CcodeShapes,
            content = content,
        )
    }
}
