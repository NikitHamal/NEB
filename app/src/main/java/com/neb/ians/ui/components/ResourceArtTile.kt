package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * The library thumbnail of one resource as a small square, for list rows (downloads, saved, top resources).
 * Drawn by code from the M3X v1 art library, never a stored picture: the same piece the site and the library
 * card draw for this resource (seed = id and type, recipe = its subject family).
 */
@Composable
fun ResourceArtTile(
    resourceId: String,
    type: String,
    subject: String,
    modifier: Modifier = Modifier,
    size: Dp = 56.dp,
    corner: Dp = 16.dp
) {
    Box(
        modifier = modifier
            .size(size)
            .clip(RoundedCornerShape(corner))
            .background(MaterialTheme.colorScheme.surfaceContainer)
    ) {
        ResourceBannerArt(
            seed = "$resourceId|$type",
            subject = subject.split(",").firstOrNull()?.trim().orEmpty(),
            modifier = Modifier.fillMaxSize()
        )
    }
}
