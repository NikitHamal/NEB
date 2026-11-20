package com.neb.ians.ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

/**
 * The illustrated banner a library resource falls back to when it has no
 * thumbnail of its own. Delegates directly to [M3xThumb] (v3 art library).
 */
@Composable
fun ResourceBannerArt(
    seed: String,
    subject: String,
    modifier: Modifier = Modifier
) {
    M3xThumb(seed = seed, subject = subject, modifier = modifier)
}
