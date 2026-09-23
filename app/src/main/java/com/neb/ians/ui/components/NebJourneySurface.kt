package com.neb.ians.ui.components

import android.app.Activity
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.isImeVisible
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.view.WindowCompat
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.NebMotion
import com.neb.ians.ui.theme.rememberNebAuthPalette
import com.neb.ians.ui.theme.rememberNebSurfacePalette

// ---------------------------------------------------------------------------
// The shell every journey screen sits in, and the two pieces of keyboard
// behaviour every one of them needs. Kept here rather than repeated per screen
// so sign-in, verification, reset and onboarding cannot drift apart.
// ---------------------------------------------------------------------------

/** True while the soft keyboard is on screen, at any point in its animation. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun nebKeyboardOpen(): Boolean = WindowInsets.isImeVisible

/**
 * A full-screen journey surface: the page colour, the system bar appearance that
 * goes with it, and insets handled once. The journey is light-locked — it runs
 * out of a splash and an auth landing that are both built on light artwork, so
 * nothing in between may follow the device into dark mode.
 */
@Composable
fun NebJourneySurface(
    modifier: Modifier = Modifier,
    dark: Boolean = false,
    content: @Composable ColumnScope.() -> Unit
) {
    val palette = rememberNebAuthPalette(dark)
    val context = LocalContext.current

    DisposableEffect(palette.isDark) {
        val window = (context as? Activity)?.window
        val controller = window?.let { WindowCompat.getInsetsController(it, it.decorView) }
        val previousStatus = controller?.isAppearanceLightStatusBars
        val previousNav = controller?.isAppearanceLightNavigationBars
        controller?.isAppearanceLightStatusBars = !palette.isDark
        controller?.isAppearanceLightNavigationBars = !palette.isDark
        onDispose {
            if (controller != null) {
                if (previousStatus != null) controller.isAppearanceLightStatusBars = previousStatus
                if (previousNav != null) controller.isAppearanceLightNavigationBars = previousNav
            }
        }
    }

    CompositionLocalProvider(LocalNebAuthPalette provides palette) {
        Column(
            modifier = modifier
                .fillMaxSize()
                .background(palette.page)
                .statusBarsPadding()
                .navigationBarsPadding()
                .imePadding(),
            content = content
        )
    }
}

/**
 * The same components inside the app proper, where the user's own theme choice
 * is in force. Wrap any reuse of the journey controls in this and they pick up
 * the right palette without a single colour being passed down.
 */
@Composable
fun NebComponentScope(content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalNebAuthPalette provides rememberNebSurfacePalette(), content = content)
}

/**
 * The slot a step's illustration goes in. It carries the clearance that keeps
 * the art off the top bar, and it folds away the moment the keyboard opens so
 * the field being typed into never gets squeezed against the action button.
 */
@Composable
fun NebArtSlot(
    modifier: Modifier = Modifier,
    collapseOnKeyboard: Boolean = true,
    content: @Composable () -> Unit
) {
    val hidden = collapseOnKeyboard && nebKeyboardOpen()
    AnimatedVisibility(
        visible = !hidden,
        enter = expandVertically(tween(NebMotion.Standard, easing = NebMotion.Decelerate)) +
            fadeIn(tween(NebMotion.Standard)),
        exit = shrinkVertically(tween(NebMotion.Short, easing = NebMotion.Accelerate)) +
            fadeOut(tween(NebMotion.Instant))
    ) {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .padding(top = NebAuthTokens.ArtClearance, bottom = 4.dp),
            contentAlignment = Alignment.Center,
            content = { content() }
        )
    }
}
