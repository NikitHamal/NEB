package com.neb.ians.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import kotlin.math.abs

/** Fullscreen viewer for one picture; same viewer as the gallery. */
@Composable
fun ZoomableImageDialog(imageUrl: String, contentDescription: String? = null, onDismiss: () -> Unit) {
    ZoomableImageDialog(imageUrls = listOf(imageUrl), initialIndex = 0, contentDescription = contentDescription, onDismiss = onDismiss)
}

/**
 * The pictures of a post or reply, to the one that was tapped. Pictures written into the text come first, in reading
 * order, then [extra] (attached pictures). Falls back to the tapped picture alone.
 */
fun inlineGallery(clicked: String, content: String, extra: List<String> = emptyList()): Pair<List<String>, Int> {
    val inline = InlineImageTokens.extractIds(content).mapNotNull { resolveMediaUrl("/media/content_images/$it.webp") }
    val all = (inline + extra).distinct()
    val at = all.indexOf(clicked)
    return if (at >= 0) all to at else listOf(clicked) to 0
}

/**
 * Fullscreen viewer: swipe sideways to change picture, pinch or double tap to zoom, drag down to close, tap to hide the
 * controls. Pages next to the current one are composed ahead so a swipe never waits on a picture.
 */
@Composable
fun ZoomableImageDialog(
    imageUrls: List<String>,
    initialIndex: Int = 0,
    contentDescription: String? = null,
    onDismiss: () -> Unit
) {
    if (imageUrls.isEmpty()) return
    val pager = rememberPagerState(initialPage = initialIndex.coerceIn(0, imageUrls.size - 1), pageCount = { imageUrls.size })
    var zoom by remember { mutableFloatStateOf(1f) }
    var drag by remember { mutableFloatStateOf(0f) }
    var chrome by remember { mutableStateOf(true) }
    val zoomNow by rememberUpdatedState(zoom)
    val fade = (1f - abs(drag) / 900f).coerceIn(0.25f, 1f)

    Dialog(onDismissRequest = onDismiss, properties = DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.97f * fade))
                .pointerInput(Unit) {
                    detectVerticalDragGestures(
                        onDragEnd = { if (abs(drag) > 220f) onDismiss() else drag = 0f },
                        onDragCancel = { drag = 0f }
                    ) { change, amount ->
                        if (zoomNow <= 1.02f) { change.consume(); drag += amount }
                    }
                }
        ) {
            HorizontalPager(
                state = pager,
                modifier = Modifier.boundedWidth().fillMaxSize().graphicsLayer { translationY = drag },
                beyondViewportPageCount = 1,
                pageSpacing = 12.dp,
                userScrollEnabled = zoom <= 1.02f
            ) { page ->
                ZoomableImagePage(
                    model = resolveZoomableImageUrl(imageUrls[page]),
                    description = contentDescription ?: "Image ${page + 1} of ${imageUrls.size}",
                    active = pager.currentPage == page,
                    onScaleChange = { if (pager.currentPage == page) zoom = it },
                    onTap = { chrome = !chrome }
                )
            }
            AnimatedVisibility(
                visible = chrome && drag == 0f,
                enter = fadeIn(),
                exit = fadeOut(),
                modifier = Modifier.align(Alignment.TopStart).statusBarsPadding()
            ) {
                Box(
                    modifier = Modifier
                        .padding(14.dp)
                        .size(42.dp)
                        .clip(CircleShape)
                        .background(Color.Black.copy(alpha = 0.5f))
                        .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = onDismiss)
                        .semantics { this.contentDescription = "Close" },
                    contentAlignment = Alignment.Center
                ) { Icon(Icons.Filled.Close, null, tint = Color.White, modifier = Modifier.size(22.dp)) }
            }
            if (imageUrls.size > 1) {
                AnimatedVisibility(
                    visible = chrome && drag == 0f,
                    enter = fadeIn(),
                    exit = fadeOut(),
                    modifier = Modifier.align(Alignment.TopCenter).statusBarsPadding()
                ) {
                    Box(
                        modifier = Modifier
                            .padding(top = 18.dp)
                            .clip(CircleShape)
                            .background(Color.Black.copy(alpha = 0.5f))
                    ) {
                        Text(
                            text = "${pager.currentPage + 1} / ${imageUrls.size}",
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold,
                            style = androidx.compose.material3.MaterialTheme.typography.labelLarge,
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp)
                        )
                    }
                }
            }
        }
    }
}

fun resolveZoomableImageUrl(url: String): String {
    if (url.startsWith("content://") || url.startsWith("file://")) return url
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
