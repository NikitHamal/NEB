package com.neb.ians.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.googlefonts.Font
import androidx.compose.ui.text.googlefonts.GoogleFont
import androidx.compose.ui.unit.sp
import com.neb.ians.R

private val googleFontProvider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = R.array.com_google_android_gms_fonts_certs
)

private val poppins = GoogleFont("Poppins")

val PoppinsFamily = FontFamily(
    Font(googleFont = poppins, fontProvider = googleFontProvider, weight = FontWeight.Light, style = FontStyle.Normal),
    Font(googleFont = poppins, fontProvider = googleFontProvider, weight = FontWeight.Normal, style = FontStyle.Normal),
    Font(googleFont = poppins, fontProvider = googleFontProvider, weight = FontWeight.Medium, style = FontStyle.Normal),
    Font(googleFont = poppins, fontProvider = googleFontProvider, weight = FontWeight.SemiBold, style = FontStyle.Normal),
    Font(googleFont = poppins, fontProvider = googleFontProvider, weight = FontWeight.Bold, style = FontStyle.Normal),
)

private fun s(size: Int, weight: FontWeight, lineHeight: Int, letterSpacing: Double = 0.0): TextStyle = TextStyle(
    fontFamily = PoppinsFamily,
    fontWeight = weight,
    fontSize = size.sp,
    lineHeight = lineHeight.sp,
    letterSpacing = letterSpacing.sp,
)

val NebTypography = Typography(
    displayLarge = s(57, FontWeight.SemiBold, 64),
    displayMedium = s(45, FontWeight.SemiBold, 52),
    displaySmall = s(36, FontWeight.SemiBold, 44),
    headlineLarge = s(32, FontWeight.SemiBold, 40),
    headlineMedium = s(28, FontWeight.SemiBold, 36),
    headlineSmall = s(24, FontWeight.SemiBold, 32),
    titleLarge = s(22, FontWeight.Medium, 28),
    titleMedium = s(16, FontWeight.Medium, 24, 0.15),
    titleSmall = s(14, FontWeight.Medium, 20, 0.1),
    bodyLarge = s(16, FontWeight.Normal, 24, 0.5),
    bodyMedium = s(14, FontWeight.Normal, 20, 0.25),
    bodySmall = s(12, FontWeight.Normal, 16, 0.4),
    labelLarge = s(14, FontWeight.Medium, 20, 0.1),
    labelMedium = s(12, FontWeight.Medium, 16, 0.5),
    labelSmall = s(11, FontWeight.Medium, 16, 0.5),
)
