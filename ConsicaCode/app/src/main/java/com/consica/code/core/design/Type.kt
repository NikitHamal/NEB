package com.consica.code.core.design

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.LineBreak
import androidx.compose.ui.unit.sp

/**
 * Typography for the Eco-Logic system.
 *
 * Design intent: rounded friendly headings (Fredoka-style), rounded body (Nunito-style),
 * monospace code (Fira Code-style). To swap in the real typefaces, drop the TTFs into
 * res/font and replace the [FontFamily] values below — nothing else changes.
 *
 * We deliberately use [FontFamily.SansSerif]/[FontFamily.Monospace] today so the app builds
 * and runs fully offline without bundling font binaries, and so Devanagari (Nepali) falls back
 * to the system script font cleanly. Line breaking uses [LineBreak.Paragraph] so longer
 * translated strings wrap gracefully instead of clipping.
 */
object EcoFonts {
    val Heading: FontFamily = FontFamily.SansSerif
    val Body: FontFamily = FontFamily.SansSerif
    val Code: FontFamily = FontFamily.Monospace
}

private val friendlyLineBreak = LineBreak.Paragraph

/** Build a [Typography] optionally scaled (used by the in-app text-size setting). */
fun ecoTypography(scale: Float = 1f): Typography {
    fun sp(v: Float) = (v * scale).sp
    return Typography(
        displayLarge = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(40f), lineHeight = sp(48f), lineBreak = friendlyLineBreak,
        ),
        displayMedium = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(32f), lineHeight = sp(40f), lineBreak = friendlyLineBreak,
        ),
        headlineLarge = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(28f), lineHeight = sp(36f), lineBreak = friendlyLineBreak,
        ),
        headlineMedium = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(24f), lineHeight = sp(32f), lineBreak = friendlyLineBreak,
        ),
        headlineSmall = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(20f), lineHeight = sp(28f), lineBreak = friendlyLineBreak,
        ),
        titleLarge = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(20f), lineHeight = sp(28f), lineBreak = friendlyLineBreak,
        ),
        titleMedium = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.SemiBold,
            fontSize = sp(16f), lineHeight = sp(24f), lineBreak = friendlyLineBreak,
        ),
        titleSmall = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.SemiBold,
            fontSize = sp(14f), lineHeight = sp(20f), lineBreak = friendlyLineBreak,
        ),
        bodyLarge = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.SemiBold,
            fontSize = sp(16f), lineHeight = sp(24f), lineBreak = friendlyLineBreak,
        ),
        bodyMedium = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.Normal,
            fontSize = sp(14f), lineHeight = sp(22f), lineBreak = friendlyLineBreak,
        ),
        bodySmall = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.Normal,
            fontSize = sp(12f), lineHeight = sp(18f), lineBreak = friendlyLineBreak,
        ),
        labelLarge = TextStyle(
            fontFamily = EcoFonts.Heading, fontWeight = FontWeight.SemiBold,
            fontSize = sp(15f), lineHeight = sp(20f),
        ),
        labelMedium = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.SemiBold,
            fontSize = sp(13f), lineHeight = sp(16f),
        ),
        labelSmall = TextStyle(
            fontFamily = EcoFonts.Body, fontWeight = FontWeight.SemiBold,
            fontSize = sp(11f), lineHeight = sp(16f),
        ),
    )
}

/** Monospace style for code surfaces. */
fun codeTextStyle(scale: Float = 1f) = TextStyle(
    fontFamily = EcoFonts.Code,
    fontWeight = FontWeight.Medium,
    fontSize = (14f * scale).sp,
    lineHeight = (22f * scale).sp,
)
