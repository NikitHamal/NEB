package com.neb.ians

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import androidx.compose.ui.graphics.Color

private val PoppinsFamily = FontFamily(
    Font(R.font.poppins_regular, FontWeight.Normal),
    Font(R.font.poppins_medium, FontWeight.Medium),
    Font(R.font.poppins_semibold, FontWeight.SemiBold)
)

private fun TextStyle.withPoppins() = copy(
    fontFamily = PoppinsFamily,
    letterSpacing = 0.sp
)

private val baseTypography = Typography()

private val NebTypography = Typography(
    displayLarge = baseTypography.displayLarge.withPoppins(),
    displayMedium = baseTypography.displayMedium.withPoppins(),
    displaySmall = baseTypography.displaySmall.withPoppins(),
    headlineLarge = baseTypography.headlineLarge.withPoppins(),
    headlineMedium = baseTypography.headlineMedium.withPoppins(),
    headlineSmall = baseTypography.headlineSmall.withPoppins(),
    titleLarge = baseTypography.titleLarge.withPoppins(),
    titleMedium = baseTypography.titleMedium.withPoppins(),
    titleSmall = baseTypography.titleSmall.withPoppins(),
    bodyLarge = baseTypography.bodyLarge.withPoppins(),
    bodyMedium = baseTypography.bodyMedium.withPoppins(),
    bodySmall = baseTypography.bodySmall.withPoppins(),
    labelLarge = baseTypography.labelLarge.withPoppins(),
    labelMedium = baseTypography.labelMedium.withPoppins(),
    labelSmall = baseTypography.labelSmall.withPoppins()
)

private val LightScheme = lightColorScheme(
    primary = Color(0xFF0E5D4E),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD4F1E5),
    onPrimaryContainer = Color(0xFF06251F),
    secondary = Color(0xFF56624F),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFDAE7CF),
    onSecondaryContainer = Color(0xFF151F12),
    tertiary = Color(0xFF476179),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFCDE5FF),
    onTertiaryContainer = Color(0xFF001D32),
    background = Color(0xFFFBFDF9),
    onBackground = Color(0xFF191C1A),
    surface = Color(0xFFFBFDF9),
    onSurface = Color(0xFF191C1A),
    surfaceVariant = Color(0xFFE0E4DC),
    onSurfaceVariant = Color(0xFF44483F),
    outline = Color(0xFF74796F)
)

private val DarkScheme = darkColorScheme(
    primary = Color(0xFFA8D8C6),
    onPrimary = Color(0xFF00382E),
    primaryContainer = Color(0xFF005144),
    onPrimaryContainer = Color(0xFFC4F4E1),
    secondary = Color(0xFFBECBAD),
    onSecondary = Color(0xFF293421),
    secondaryContainer = Color(0xFF3F4B36),
    onSecondaryContainer = Color(0xFFDAE7CF),
    tertiary = Color(0xFFAFCBE6),
    onTertiary = Color(0xFF173349),
    tertiaryContainer = Color(0xFF2F4A60),
    onTertiaryContainer = Color(0xFFCDE5FF),
    background = Color(0xFF101411),
    onBackground = Color(0xFFE1E4DE),
    surface = Color(0xFF101411),
    onSurface = Color(0xFFE1E4DE),
    surfaceVariant = Color(0xFF44483F),
    onSurfaceVariant = Color(0xFFC4C8BE),
    outline = Color(0xFF8E9388)
)

@Composable
fun NEBiansTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val context = LocalContext.current
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && darkTheme -> dynamicDarkColorScheme(context)
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> dynamicLightColorScheme(context)
        darkTheme -> DarkScheme
        else -> LightScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = NebTypography,
        content = content
    )
}
