package com.neb.ians.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.googlefonts.GoogleFont
import androidx.compose.ui.unit.sp
import com.neb.ians.R

private val provider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = R.array.com_google_android_gms_fonts_certs,
)

private val poppinsName = GoogleFont("Poppins")

val Poppins: FontFamily = FontFamily(
    Font(googleFont = poppinsName, fontProvider = provider, weight = FontWeight.Light, style = FontStyle.Normal),
    Font(googleFont = poppinsName, fontProvider = provider, weight = FontWeight.Normal, style = FontStyle.Normal),
    Font(googleFont = poppinsName, fontProvider = provider, weight = FontWeight.Medium, style = FontStyle.Normal),
    Font(googleFont = poppinsName, fontProvider = provider, weight = FontWeight.SemiBold, style = FontStyle.Normal),
    Font(googleFont = poppinsName, fontProvider = provider, weight = FontWeight.Bold, style = FontStyle.Normal),
)

private fun ts(
    weight: FontWeight,
    size: Int,
    line: Int,
    spacing: Double = 0.0,
) = TextStyle(
    fontFamily = Poppins,
    fontWeight = weight,
    fontSize = size.sp,
    lineHeight = line.sp,
    letterSpacing = spacing.sp,
)

val NebTypography = Typography(
    displayLarge = ts(FontWeight.Normal, 57, 64, -0.25),
    displayMedium = ts(FontWeight.Normal, 45, 52),
    displaySmall = ts(FontWeight.Normal, 36, 44),
    headlineLarge = ts(FontWeight.SemiBold, 32, 40),
    headlineMedium = ts(FontWeight.SemiBold, 28, 36),
    headlineSmall = ts(FontWeight.SemiBold, 24, 32),
    titleLarge = ts(FontWeight.SemiBold, 22, 28),
    titleMedium = ts(FontWeight.Medium, 16, 24, 0.15),
    titleSmall = ts(FontWeight.Medium, 14, 20, 0.1),
    bodyLarge = ts(FontWeight.Normal, 16, 24, 0.5),
    bodyMedium = ts(FontWeight.Normal, 14, 20, 0.25),
    bodySmall = ts(FontWeight.Normal, 12, 16, 0.4),
    labelLarge = ts(FontWeight.Medium, 14, 20, 0.1),
    labelMedium = ts(FontWeight.Medium, 12, 16, 0.5),
    labelSmall = ts(FontWeight.Medium, 11, 16, 0.5),
)
