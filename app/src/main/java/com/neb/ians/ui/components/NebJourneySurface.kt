package com.neb.ians.ui.components

import android.app.Activity
import androidx.compose.animation.AnimatedVisibility
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
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.core.view.WindowCompat
import com.neb.ians.ui.theme.LocalNebAuthPalette
import com.neb.ians.ui.theme.NebAuthPalette
import com.neb.ians.ui.theme.NebAuthTokens
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.nebSpatialSpec
import com.neb.ians.ui.theme.rememberNebAuthPalette
import com.neb.ians.ui.theme.rememberNebColorScheme
import com.neb.ians.ui.theme.rememberNebSurfacePalette

// ---------------------------------------------------------------------------
// The shell every journey screen sits in, and the two pieces of keyboard
// behaviour every one of them needs. Kept here rather than repeated per screen
// so sign-in, verification, reset and onboarding cannot drift apart.
//
// It is also the boundary of Material 3 Expressive in this app. The journey runs
// under MaterialExpressiveTheme so its toggle buttons, button groups and loading
// indicators get the expressive motion scheme and shape defaults; the rest of
// the app keeps the theme it already had, because the feed is not being
// redesigned and must not shift underneath anyone.
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

    NebExpressiveScope(palette) {
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
 * The palette, the matching Material colour scheme and the expressive motion
 * scheme, provided together. Nothing downstream passes a colour or an animation
 * spec: journey controls read [LocalNebAuthPalette], Material's own expressive
 * components read the scheme, and both end up graphite.
 */
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun NebExpressiveScope(
    palette: NebAuthPalette,
    content: @Composable () -> Unit
) {
    CompositionLocalProvider(LocalNebAuthPalette provides palette) {
        MaterialExpressiveTheme(
            colorScheme = rememberNebColorScheme(palette),
            motionScheme = MotionScheme.expressive(),
            typography = MaterialTheme.typography,
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
    NebExpressiveScope(rememberNebSurfacePalette(), content)
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
    val size = nebSpatialSpec<IntSize>()
    val opacity = nebEffectsSpec<Float>()
    AnimatedVisibility(
        visible = !hidden,
        enter = expandVertically(size) + fadeIn(opacity),
        exit = shrinkVertically(size) + fadeOut(opacity)
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
