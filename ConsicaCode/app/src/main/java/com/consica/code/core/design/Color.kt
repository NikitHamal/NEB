package com.consica.code.core.design

import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.ui.graphics.Color

/**
 * Eco-Logic palette.
 * Primary: Forest Green · Background: Leaf Light · Surface: Clean White
 * Text: Soil Dark · Muted: Stone Gray · Accent: River Blue · Fun: Sun Yellow
 */
object EcoPalette {
    val ForestGreen = Color(0xFF2D5A27)
    val ForestGreenDark = Color(0xFF1E3D1A)
    val ForestGreenLight = Color(0xFF7BC67E)
    val LeafLight = Color(0xFFE8F5E9)
    val CleanWhite = Color(0xFFFFFFFF)
    val SoilDark = Color(0xFF1A1A1A)
    val StoneGray = Color(0xFF8D99AE)
    val RiverBlue = Color(0xFF4DA8DA)
    val RiverBlueDark = Color(0xFF2F7DA8)
    val SunYellow = Color(0xFFFFD54F)
    val SunYellowDeep = Color(0xFFF9A825)

    // Semantic helpers used by the ecosystem visuals
    val GrowthGreen = Color(0xFF66BB6A)
    val DryBrown = Color(0xFF9E6B3F)
    val SkyTop = Color(0xFFBFE6F2)
    val SoilStrip = Color(0xFF6D4C32)
}

/** Light (standard) Eco-Logic Material 3 scheme. */
val EcoLightColors = lightColorScheme(
    primary = EcoPalette.ForestGreen,
    onPrimary = EcoPalette.CleanWhite,
    primaryContainer = Color(0xFFB8E0B5),
    onPrimaryContainer = EcoPalette.ForestGreenDark,
    secondary = EcoPalette.RiverBlue,
    onSecondary = EcoPalette.CleanWhite,
    secondaryContainer = Color(0xFFCDEAF6),
    onSecondaryContainer = EcoPalette.RiverBlueDark,
    tertiary = EcoPalette.SunYellowDeep,
    onTertiary = EcoPalette.SoilDark,
    tertiaryContainer = Color(0xFFFFE9A8),
    onTertiaryContainer = Color(0xFF5A4300),
    background = EcoPalette.LeafLight,
    onBackground = EcoPalette.SoilDark,
    surface = EcoPalette.CleanWhite,
    onSurface = EcoPalette.SoilDark,
    surfaceVariant = Color(0xFFDCE8DC),
    onSurfaceVariant = Color(0xFF44503F),
    outline = EcoPalette.StoneGray,
    outlineVariant = Color(0xFFC4D0C2),
    error = Color(0xFFB3261E),
    onError = EcoPalette.CleanWhite,
    errorContainer = Color(0xFFF9DEDC),
    onErrorContainer = Color(0xFF410E0B),
)

/** Dark Eco-Logic scheme — also used as the code-editor surface family. */
val EcoDarkColors = darkColorScheme(
    primary = EcoPalette.ForestGreenLight,
    onPrimary = Color(0xFF0C2109),
    primaryContainer = EcoPalette.ForestGreen,
    onPrimaryContainer = Color(0xFFD7F0D5),
    secondary = Color(0xFF8BD0EC),
    onSecondary = Color(0xFF00344A),
    secondaryContainer = EcoPalette.RiverBlueDark,
    onSecondaryContainer = Color(0xFFCDEAF6),
    tertiary = EcoPalette.SunYellow,
    onTertiary = Color(0xFF3D2E00),
    tertiaryContainer = Color(0xFF6A5300),
    onTertiaryContainer = Color(0xFFFFE9A8),
    background = Color(0xFF101510),
    onBackground = Color(0xFFE2E8E0),
    surface = Color(0xFF161D16),
    onSurface = Color(0xFFE2E8E0),
    surfaceVariant = Color(0xFF333B32),
    onSurfaceVariant = Color(0xFFC4D0C2),
    outline = Color(0xFF8C9A89),
    outlineVariant = Color(0xFF44503F),
    error = Color(0xFFF2B8B5),
    onError = Color(0xFF601410),
    errorContainer = Color(0xFF8C1D18),
    onErrorContainer = Color(0xFFF9DEDC),
)

/** High-contrast light scheme — keeps the Eco identity but maximizes legibility. */
val EcoHighContrastLight = lightColorScheme(
    primary = EcoPalette.ForestGreenDark,
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = EcoPalette.ForestGreen,
    onPrimaryContainer = Color(0xFFFFFFFF),
    secondary = EcoPalette.RiverBlueDark,
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFF0A5378),
    onSecondaryContainer = Color(0xFFFFFFFF),
    tertiary = Color(0xFF5A4300),
    onTertiary = Color(0xFFFFFFFF),
    background = Color(0xFFFFFFFF),
    onBackground = Color(0xFF000000),
    surface = Color(0xFFFFFFFF),
    onSurface = Color(0xFF000000),
    surfaceVariant = Color(0xFFE9F1E9),
    onSurfaceVariant = Color(0xFF1A1A1A),
    outline = Color(0xFF1A1A1A),
    outlineVariant = Color(0xFF44503F),
    error = Color(0xFF8C0009),
    onError = Color(0xFFFFFFFF),
)

/** High-contrast dark scheme. */
val EcoHighContrastDark = darkColorScheme(
    primary = Color(0xFFB6F0B2),
    onPrimary = Color(0xFF000000),
    primaryContainer = EcoPalette.ForestGreenLight,
    onPrimaryContainer = Color(0xFF000000),
    secondary = Color(0xFFB8E4F7),
    onSecondary = Color(0xFF000000),
    background = Color(0xFF000000),
    onBackground = Color(0xFFFFFFFF),
    surface = Color(0xFF0A0F0A),
    onSurface = Color(0xFFFFFFFF),
    surfaceVariant = Color(0xFF26301F),
    onSurfaceVariant = Color(0xFFFFFFFF),
    outline = Color(0xFFEAEAEA),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF000000),
)
