package com.consica.code.core.designsystem

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.consica.code.R

/** Fredoka — rounded, friendly. Headings + buttons. */
val Fredoka = FontFamily(
    Font(R.font.fredoka_regular, FontWeight.Normal),
    Font(R.font.fredoka_medium, FontWeight.Medium),
    Font(R.font.fredoka_semibold, FontWeight.SemiBold),
    Font(R.font.fredoka_semibold, FontWeight.Bold),
)

/** Nunito — rounded, readable. Body text. */
val Nunito = FontFamily(
    Font(R.font.nunito_regular, FontWeight.Normal),
    Font(R.font.nunito_semibold, FontWeight.SemiBold),
    Font(R.font.nunito_bold, FontWeight.Bold),
    Font(R.font.nunito_extrabold, FontWeight.ExtraBold),
)

/** Fira Code — monospace for all code surfaces. */
val FiraCode = FontFamily(
    Font(R.font.firacode_regular, FontWeight.Normal),
    Font(R.font.firacode_medium, FontWeight.Medium),
)

val CcodeTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 48.sp, lineHeight = 56.sp,
    ),
    displayMedium = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 40.sp, lineHeight = 48.sp,
    ),
    displaySmall = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 34.sp, lineHeight = 42.sp,
    ),
    headlineLarge = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 30.sp, lineHeight = 38.sp,
    ),
    headlineMedium = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 26.sp, lineHeight = 34.sp,
    ),
    headlineSmall = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 22.sp, lineHeight = 30.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 28.sp,
    ),
    titleMedium = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.Medium, fontSize = 17.sp, lineHeight = 24.sp,
    ),
    titleSmall = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.Medium, fontSize = 15.sp, lineHeight = 22.sp,
    ),
    bodyLarge = TextStyle(
        fontFamily = Nunito, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 24.sp,
    ),
    bodyMedium = TextStyle(
        fontFamily = Nunito, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, lineHeight = 21.sp,
    ),
    bodySmall = TextStyle(
        fontFamily = Nunito, fontWeight = FontWeight.SemiBold, fontSize = 12.sp, lineHeight = 18.sp,
    ),
    labelLarge = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.SemiBold, fontSize = 15.sp, lineHeight = 20.sp,
    ),
    labelMedium = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.Medium, fontSize = 13.sp, lineHeight = 18.sp,
    ),
    labelSmall = TextStyle(
        fontFamily = Fredoka, fontWeight = FontWeight.Medium, fontSize = 11.sp, lineHeight = 16.sp,
    ),
)

/** Style for code blocks and the editor. */
val CodeTextStyle = TextStyle(
    fontFamily = FiraCode,
    fontWeight = FontWeight.Normal,
    fontSize = 14.sp,
    lineHeight = 22.sp,
)
