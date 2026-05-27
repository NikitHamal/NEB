package com.neb.ians.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import com.neb.ians.R

val Poppins = FontFamily(
    Font(R.font.poppins_regular, FontWeight.Normal),
    Font(R.font.poppins_medium, FontWeight.Medium),
    Font(R.font.poppins_semibold, FontWeight.SemiBold),
    Font(R.font.poppins_bold, FontWeight.Bold)
)

val NebTypography = Typography().run {
    copy(
        displayLarge = displayLarge.copy(fontFamily = Poppins),
        displayMedium = displayMedium.copy(fontFamily = Poppins),
        displaySmall = displaySmall.copy(fontFamily = Poppins),
        headlineLarge = headlineLarge.copy(fontFamily = Poppins, fontWeight = FontWeight.SemiBold),
        headlineMedium = headlineMedium.copy(fontFamily = Poppins, fontWeight = FontWeight.SemiBold),
        headlineSmall = headlineSmall.copy(fontFamily = Poppins, fontWeight = FontWeight.SemiBold),
        titleLarge = titleLarge.copy(fontFamily = Poppins, fontWeight = FontWeight.SemiBold),
        titleMedium = titleMedium.copy(fontFamily = Poppins, fontWeight = FontWeight.SemiBold),
        titleSmall = titleSmall.copy(fontFamily = Poppins, fontWeight = FontWeight.Medium),
        bodyLarge = bodyLarge.copy(fontFamily = Poppins),
        bodyMedium = bodyMedium.copy(fontFamily = Poppins),
        bodySmall = bodySmall.copy(fontFamily = Poppins),
        labelLarge = labelLarge.copy(fontFamily = Poppins, fontWeight = FontWeight.Medium),
        labelMedium = labelMedium.copy(fontFamily = Poppins, fontWeight = FontWeight.Medium),
        labelSmall = labelSmall.copy(fontFamily = Poppins, fontWeight = FontWeight.Medium)
    )
}
