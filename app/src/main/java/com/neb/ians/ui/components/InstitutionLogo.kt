package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.AccountBalance
import androidx.compose.material.icons.outlined.School
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.compose.AsyncImagePainter

/**
 * An institution's picture: the profile photo of the account that owns it. Frameless (no ring), clipped to a rounded
 * tile. While there is no photo, or the file fails to load, the school or college glyph on a tonal tile stays.
 */
@Composable
fun InstitutionLogo(
    photoUrl: String?,
    kind: String,
    size: Dp,
    modifier: Modifier = Modifier,
    container: Color = MaterialTheme.colorScheme.primaryContainer,
    content: Color = MaterialTheme.colorScheme.onPrimaryContainer,
    corner: Dp = size * 0.32f,
) {
    val url = remember(photoUrl) { resolveMediaUrl(photoUrl) }
    var failed by remember(url) { mutableStateOf(false) }
    Box(
        modifier.size(size).clip(RoundedCornerShape(corner)).background(container),
        contentAlignment = Alignment.Center
    ) {
        if (url.isNullOrBlank() || failed) {
            Icon(
                if (kind == "school") Icons.Outlined.School else Icons.Outlined.AccountBalance, null,
                Modifier.size(size * 0.48f), tint = content
            )
        } else {
            AsyncImage(
                model = url, contentDescription = null, contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize(),
                onState = { if (it is AsyncImagePainter.State.Error) failed = true }
            )
        }
    }
}
