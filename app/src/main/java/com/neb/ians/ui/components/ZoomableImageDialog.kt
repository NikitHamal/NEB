package com.neb.ians.ui.components

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import coil.compose.AsyncImage
import kotlinx.coroutines.launch

/**
 * Fullscreen zoomable viewer for a single image.
 * Delegates to the multi-image viewer so every fullscreen viewer in the app
 * behaves exactly the same.
 */
@Composable
fun ZoomableImageDialog(
    imageUrl: String,
    contentDescription: String? = null,
    onDismiss: () -> Unit
) {
    ZoomableImageDialog(
        imageUrls = listOf(imageUrl),
        initialIndex = 0,
        contentDescription = contentDescription,
        onDismiss = onDismiss
    )
}

/**
 * Fullscreen zoomable image viewer with swipe-to-change support.
 *
 * Users can pinch-to-zoom and pan each image. When there are multiple images,
 * swiping horizontally moves between them (swiping is temporarily disabled
 * while an image is zoomed in so the pan gesture doesn't fight the pager).
 */
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ZoomableImageDialog(
    imageUrls: List<String>,
    initialIndex: Int = 0,
    contentDescription: String? = null,
    onDismiss: () -> Unit
) {
    if (imageUrls.isEmpty()) return
    val pagerState = rememberPagerState(
        initialPage = initialIndex.coerceIn(0, imageUrls.size - 1),
        pageCount = { imageUrls.size }
    )
    val scope = rememberCoroutineScope()
    // Zoom state kept per page so every image keeps its own pinch/pan.
    val zoomScales = remember { mutableStateMapOf<Int, Float>() }
    val zoomOffsets = remember { mutableStateMapOf<Int, Offset>() }
    val currentPageScale = zoomScales[pagerState.currentPage] ?: 1f

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.94f))
        ) {
            HorizontalPager(
                state = pagerState,
                modifier = Modifier.fillMaxSize(),
                // While zoomed in, horizontal drags belong to the pan gesture.
                userScrollEnabled = currentPageScale <= 1.05f
            ) { page ->
                val scale = zoomScales[page] ?: 1f
                val offset = zoomOffsets[page] ?: Offset.Zero
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    AsyncImage(
                        model = resolveZoomableImageUrl(imageUrls[page]),
                        contentDescription = contentDescription ?: "Image ${page + 1} of ${imageUrls.size}",
                        modifier = Modifier
                            .fillMaxSize()
                            .pointerInput(page) {
                                detectTransformGestures { _, pan, zoom, _ ->
                                    val currentScale = zoomScales[page] ?: 1f
                                    val newScale = (currentScale * zoom).coerceIn(1f, 5f)
                                    zoomScales[page] = newScale
                                    if (newScale <= 1.01f) {
                                        zoomOffsets[page] = Offset.Zero
                                    } else {
                                        val currentOffset = zoomOffsets[page] ?: Offset.Zero
                                        zoomOffsets[page] = currentOffset + pan
                                    }
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
                }
            }

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

            if (imageUrls.size > 1) {
                Row(
                    modifier = Modifier
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 26.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    if (pagerState.currentPage > 0) {
                        Surface(
                            onClick = {
                                scope.launch {
                                    pagerState.animateScrollToPage(pagerState.currentPage - 1)
                                }
                            },
                            shape = CircleShape,
                            color = Color.White.copy(alpha = 0.88f),
                            contentColor = Color.Black,
                            modifier = Modifier.size(36.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                                    contentDescription = "Previous Image",
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    }

                    Surface(
                        shape = CircleShape,
                        color = Color.White.copy(alpha = 0.88f),
                        contentColor = Color.Black
                    ) {
                        Text(
                            text = "${pagerState.currentPage + 1} / ${imageUrls.size}",
                            modifier = Modifier.padding(horizontal = 14.dp, vertical = 6.dp),
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    if (pagerState.currentPage < imageUrls.size - 1) {
                        Surface(
                            onClick = {
                                scope.launch {
                                    pagerState.animateScrollToPage(pagerState.currentPage + 1)
                                }
                            },
                            shape = CircleShape,
                            color = Color.White.copy(alpha = 0.88f),
                            contentColor = Color.Black,
                            modifier = Modifier.size(36.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                    contentDescription = "Next Image",
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    }
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
