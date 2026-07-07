package com.neb.ians.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import coil.compose.AsyncImage

@Composable
fun ZoomableImageDialog(
    imageUrl: String,
    contentDescription: String? = null,
    onDismiss: () -> Unit
) {
    var scale by remember(imageUrl) { mutableFloatStateOf(1f) }
    var offset by remember(imageUrl) { mutableStateOf(Offset.Zero) }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.94f))
        ) {
            AsyncImage(
                model = resolveZoomableImageUrl(imageUrl),
                contentDescription = contentDescription,
                modifier = Modifier
                    .fillMaxSize()
                    .pointerInput(imageUrl) {
                        detectTransformGestures { _, pan, zoom, _ ->
                            scale = (scale * zoom).coerceIn(1f, 5f)
                            offset = if (scale <= 1.01f) Offset.Zero else offset + pan
                        }
                    }
                    .graphicsLayer(
                        scaleX = scale,
                        scaleY = scale,
                        translationX = offset.x,
                        translationY = offset.y
                    ),
                contentScale = ContentScale.Fit
            )
            Surface(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(18.dp)
                    .size(44.dp),
                shape = CircleShape,
                color = Color.White.copy(alpha = 0.92f),
                contentColor = Color.Black
            ) {
                IconButton(onClick = onDismiss) {
                    Icon(Icons.Filled.Close, contentDescription = "Close")
                }
            }
        }
    }
}

fun resolveZoomableImageUrl(url: String): String {
    val cleanUrl = if (url.startsWith("http://") || url.startsWith("https://")) {
        url
    } else {
        "https://nebians.consica.com.np${if (url.startsWith("/")) "" else "/"}$url"
    }
    
    // Upgrade Google profile pictures to original resolution (s0)
    if (cleanUrl.contains("googleusercontent.com")) {
        val suffixRegex = "(=s\\d+(-[c])?)$".toRegex()
        if (suffixRegex.containsMatchIn(cleanUrl)) {
            return cleanUrl.replace(suffixRegex, "=s0")
        }
        val pathRegex = "/s\\d+(-[c])?/".toRegex()
        if (pathRegex.containsMatchIn(cleanUrl)) {
            return cleanUrl.replace(pathRegex, "/s0/")
        }
    } 
    // Upgrade GitHub profile pictures to high resolution (s=512)
    else if (cleanUrl.contains("avatars.githubusercontent.com")) {
        return if (cleanUrl.contains("?")) {
            if (cleanUrl.contains("s=")) {
                cleanUrl.replace("s=\\d+".toRegex(), "s=512")
            } else {
                "$cleanUrl&s=512"
            }
        } else {
            "$cleanUrl?s=512"
        }
    }
    
    return cleanUrl
}
