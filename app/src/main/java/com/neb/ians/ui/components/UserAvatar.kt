package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.SubcomposeAsyncImage
import coil.request.ImageRequest
import androidx.compose.ui.platform.LocalContext

/**
 * Circular user avatar. Loads [photoUrl] via Coil; while loading or when the URL is
 * blank/fails it shows the first letter of [name] on a primary-container background —
 * matching the website's avatar-with-initial fallback.
 */
@Composable
fun UserAvatar(
    photoUrl: String?,
    name: String,
    size: Dp = 40.dp,
    modifier: Modifier = Modifier,
    fontSize: TextUnit = (size.value / 2.4f).sp,
    backgroundColor: Color = MaterialTheme.colorScheme.primaryContainer,
    contentColor: Color = MaterialTheme.colorScheme.onPrimaryContainer
) {
    val initial = name.trim().firstOrNull()?.uppercase() ?: "?"
    val context = LocalContext.current

    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .background(backgroundColor),
        contentAlignment = Alignment.Center
    ) {
        if (!photoUrl.isNullOrBlank()) {
            SubcomposeAsyncImage(
                model = ImageRequest.Builder(context)
                    .data(photoUrl)
                    .crossfade(true)
                    .build(),
                contentDescription = name,
                contentScale = ContentScale.Crop,
                modifier = Modifier.size(size).clip(CircleShape),
                loading = { InitialLabel(initial, fontSize, contentColor) },
                error = { InitialLabel(initial, fontSize, contentColor) }
            )
        } else {
            InitialLabel(initial, fontSize, contentColor)
        }
    }
}

@Composable
private fun InitialLabel(initial: String, fontSize: TextUnit, contentColor: Color) {
    Text(
        text = initial,
        color = contentColor,
        fontSize = fontSize,
        fontWeight = FontWeight.SemiBold
    )
}
