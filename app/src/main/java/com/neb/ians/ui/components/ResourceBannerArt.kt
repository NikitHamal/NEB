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

/** Deterministic 32-bit FNV-1a hash seed used by procedural/pixel views. */
fun stableSeed(s: String): Int {
    var h = 0x811c9dc5.toInt()
    for (i in 0 until s.length) {
        h = h xor s[i].code
        h *= 0x01000193
    }
    return h and 0x7FFFFFFF
}
