package com.neb.ians.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.res.painterResource
import com.neb.ians.R

/**
 * Rune Icons (https://www.runeicons.com/)
 * Open-source SVG icon library with consistent stroke weight and modern geometry.
 * Seamlessly mixed alongside Material 3 symbols and icons.
 */
object RuneIcons {
    val Plus: Painter
        @Composable
        get() = painterResource(id = R.drawable.ic_rune_plus)

    val Upload: Painter
        @Composable
        get() = painterResource(id = R.drawable.ic_rune_upload)
}
