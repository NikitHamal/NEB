package com.neb.ians.util

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.WindowInsetsSides
import androidx.compose.foundation.layout.displayCutout
import androidx.compose.foundation.layout.only
import androidx.compose.foundation.layout.systemBarsIgnoringVisibility
import androidx.compose.foundation.layout.union
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.core.view.WindowCompat

private tailrec fun Context.hostActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.hostActivity()
    else -> null
}

/**
 * Sets the colour of the status and navigation bar icons for the screen that calls it and puts the previous
 * look back when the screen leaves. [darkIcons] is true over a light background. Every screen whose top is not
 * the app's own surface (the reader's night page, a video, a photo, the splash) says what is behind the bars.
 */
@Composable
fun NebSystemBars(darkIcons: Boolean) {
    val activity = LocalContext.current.hostActivity()
    DisposableEffect(activity, darkIcons) {
        val window = activity?.window
        if (window == null) {
            onDispose { }
        } else {
            val controller = WindowCompat.getInsetsController(window, window.decorView)
            val status = controller.isAppearanceLightStatusBars
            val navigation = controller.isAppearanceLightNavigationBars
            controller.isAppearanceLightStatusBars = darkIcons
            controller.isAppearanceLightNavigationBars = darkIcons
            onDispose {
                controller.isAppearanceLightStatusBars = status
                controller.isAppearanceLightNavigationBars = navigation
            }
        }
    }
}

/**
 * Keeps touch targets clear of what sits at the left and right edge: a navigation bar in landscape (three button
 * navigation), a camera cut-out, rounded corners. The top and bottom stay with each screen, which already pads for
 * the status and navigation bars. Uses the insets as if the bars were shown, so the layout does not move when they hide.
 */
@Composable
fun Modifier.nebSafeSides(): Modifier = this.windowInsetsPadding(
    WindowInsets.systemBarsIgnoringVisibility.union(WindowInsets.displayCutout).only(WindowInsetsSides.Horizontal)
)
