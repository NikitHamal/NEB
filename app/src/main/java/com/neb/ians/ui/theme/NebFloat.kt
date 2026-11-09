package com.neb.ians.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.ReadOnlyComposable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance

/**
 * The fill of everything that floats above a page: menus, popovers, dialogs, bottom sheets.
 * White in light (the web's `--x-float`), a raised tonal step in dark. Never a blue-tinted
 * container role. Every floating surface in the app reads this and nothing else.
 */
@Composable
@ReadOnlyComposable
fun nebFloatColor(): Color {
    val scheme = MaterialTheme.colorScheme
    return if (scheme.surface.luminance() > 0.5f) Color.White else scheme.surfaceContainerHigh
}

/** The hairline around a floating surface (the web's `--x-float-line`). */
@Composable
@ReadOnlyComposable
fun nebFloatLine(): Color = MaterialTheme.colorScheme.outlineVariant
