package com.consica.code.core.designsystem

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

private val EcoLightColors: ColorScheme = lightColorScheme(
    primary = ForestGreen,
    onPrimary = CleanWhite,
    primaryContainer = LeafContainer,
    onPrimaryContainer = ForestGreenDeep,
    secondary = RiverBlue,
    onSecondary = CleanWhite,
    secondaryContainer = SkyMist,
    onSecondaryContainer = RiverBlueDeep,
    tertiary = SunYellowDeep,
    onTertiary = CleanWhite,
    tertiaryContainer = SunCream,
    onTertiaryContainer = SunYellowDeep,
    background = LeafLight,
    onBackground = SoilDark,
    surface = CleanWhite,
    onSurface = SoilDark,
    surfaceVariant = LeafLight,
    onSurfaceVariant = Color(0xFF44524A),
    outline = StoneGray,
    outlineVariant = OutlineSoft,
    error = ErrorRed,
    onError = CleanWhite,
    errorContainer = ErrorContainer,
    onErrorContainer = Color(0xFF410E0B),
    surfaceTint = ForestGreen,
    inverseSurface = SoilDark,
    inverseOnSurface = LeafLight,
)

private val EcoDarkColors: ColorScheme = darkColorScheme(
    primary = NightLeaf,
    onPrimary = ForestGreenDeep,
    primaryContainer = Color(0xFF2E4A2E),
    onPrimaryContainer = LeafContainer,
    secondary = RiverBlue,
    onSecondary = Color(0xFF06283C),
    secondaryContainer = Color(0xFF1E3A4C),
    onSecondaryContainer = SkyMist,
    tertiary = SunYellow,
    onTertiary = Color(0xFF3D2F00),
    tertiaryContainer = Color(0xFF4A3D10),
    onTertiaryContainer = SunCream,
    background = NightBackground,
    onBackground = NightText,
    surface = NightSurface,
    onSurface = NightText,
    surfaceVariant = NightSurfaceHigh,
    onSurfaceVariant = Color(0xFFB9C7BA),
    outline = Color(0xFF74857A),
    outlineVariant = NightOutline,
    error = Color(0xFFF2B8B5),
    onError = Color(0xFF601410),
    errorContainer = Color(0xFF8C1D18),
    onErrorContainer = ErrorContainer,
    surfaceTint = NightLeaf,
    inverseSurface = NightText,
    inverseOnSurface = NightBackground,
)

/** High contrast variants keep the Eco-Logic identity with stronger separation. */
private val EcoLightHighContrast = EcoLightColors.copy(
    primary = ForestGreenDeep,
    onSurfaceVariant = Color(0xFF1F2A23),
    outline = Color(0xFF3C474F),
    outlineVariant = Color(0xFF6B7B6C),
    background = CleanWhite,
)

private val EcoDarkHighContrast = EcoDarkColors.copy(
    primary = Color(0xFFC4EEC4),
    onBackground = CleanWhite,
    onSurface = CleanWhite,
    onSurfaceVariant = Color(0xFFDCE8DD),
    outline = Color(0xFFAEBFB3),
    background = Color(0xFF050A05),
    surface = Color(0xFF101810),
)

/** App-wide accessibility/feel flags, provided once at the root. */
data class EcoUiConfig(
    val reducedMotion: Boolean = false,
    val highContrast: Boolean = false,
    val soundEnabled: Boolean = true,
)

val LocalEcoUiConfig = staticCompositionLocalOf { EcoUiConfig() }

@Composable
fun ConsicaCodeTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    highContrast: Boolean = false,
    reducedMotion: Boolean = false,
    soundEnabled: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        darkTheme && highContrast -> EcoDarkHighContrast
        darkTheme -> EcoDarkColors
        highContrast -> EcoLightHighContrast
        else -> EcoLightColors
    }
    CompositionLocalProvider(
        LocalEcoUiConfig provides EcoUiConfig(
            reducedMotion = reducedMotion,
            highContrast = highContrast,
            soundEnabled = soundEnabled,
        )
    ) {
        MaterialTheme(
            colorScheme = colorScheme,
            typography = CcodeTypography,
            shapes = CcodeShapes,
            content = content,
        )
    }
}
