@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.resource

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.CloudUpload
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Folder
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.PlayCircle
import androidx.compose.material.icons.outlined.Headphones
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.icons.outlined.Public
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Verified
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.offset
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.ArrowForwardIos
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.QrCode2
import androidx.compose.material.icons.outlined.Info
import coil.compose.AsyncImage
import android.content.Context
import android.net.Uri
import com.neb.ians.ui.components.NebModalSheet
import java.io.File
import java.io.FileOutputStream
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.runtime.remember
import androidx.compose.ui.text.style.TextDecoration
import com.neb.ians.ui.components.ExpandableText
import com.neb.ians.ui.components.NebAvatar
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.LikePill
import com.neb.ians.ui.components.NebBadge

import com.neb.ians.util.formatTimeAgo
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.art.NebStateArt
import com.neb.ians.ui.components.art.NebStateKind

enum class ResourceMediaType { Pdf, Image, Video, Audio, Other }

fun detectResourceMedia(fileUrl: String, type: String): ResourceMediaType {
    val lowerUrl = fileUrl.lowercase()
    val lowerType = type.lowercase()
    return when {
        lowerType.contains("pdf") || lowerUrl.endsWith(".pdf") -> ResourceMediaType.Pdf
        lowerType.contains("image") || Regex("\\.(png|jpe?g|gif|webp|bmp)$", RegexOption.IGNORE_CASE).containsMatchIn(fileUrl) -> ResourceMediaType.Image
        lowerType.contains("video") || Regex("\\.(mp4|mkv|avi|mov|webm|3gp|wmv|flv)$", RegexOption.IGNORE_CASE).containsMatchIn(fileUrl) -> ResourceMediaType.Video
        lowerType.contains("audio") || Regex("\\.(mp3|wav|ogg|flac|aac|m4a|wma)$", RegexOption.IGNORE_CASE).containsMatchIn(fileUrl) -> ResourceMediaType.Audio
        else -> ResourceMediaType.Other
    }
}

@Composable
fun ResourceCommentsHeader(count: Int, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Comments",
            style = MaterialTheme.typography.titleMediumEmphasized,
            color = MaterialTheme.colorScheme.onSurface
        )
        if (count > 0) {
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                    .padding(horizontal = 9.dp, vertical = 3.dp)
            )
        }
    }
}

@Composable
fun ResourceCommentsLoading() {
    Box(modifier = Modifier.fillMaxWidth().padding(22.dp), contentAlignment = Alignment.Center) {
        NebLoader(size = NebLoaderSize.Small)
    }
}

@Composable
fun ResourceEmptyComments() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 22.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        NebStateArt(kind = NebStateKind.Empty, height = 108.dp)
        Spacer(Modifier.height(10.dp))
        Text(
            text = "No comments yet",
            style = MaterialTheme.typography.titleSmallEmphasized,
            color = MaterialTheme.colorScheme.onSurface
        )
        Text(
            text = "Say what you thought of this resource",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ResourceCommentItem(
    comment: ApiResourceComment,
    canDelete: Boolean,
    onDelete: () -> Unit,
    onThumbsUpClick: () -> Unit,
    onAuthorClick: (String) -> Unit = {},
    modifier: Modifier = Modifier
) {
    val badgeLevel = remember(comment.authorBadgeInfo) {
        if (comment.authorBadgeInfo?.type == "verified") {
            when (comment.authorBadgeInfo.color?.trim()?.lowercase()) {
                "#1b9af0" -> 1
                "#2e7d32" -> 2
                "#f59e0b" -> 3
                "#1a1a1a" -> 4
                else -> 1
            }
        } else 0
    }

    Surface(
        modifier = modifier.fillMaxWidth().padding(bottom = 10.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        shape = RoundedCornerShape(8.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        tonalElevation = 0.dp
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Avatar(
                    name = comment.userName,
                    imageUrl = comment.userPhotoUrl,
                    size = 28.dp,
                    verificationLevel = badgeLevel,
                    modifier = Modifier.clickable(enabled = comment.userName.isNotBlank()) { onAuthorClick(comment.userName) }
                )
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clickable(enabled = comment.userName.isNotBlank()) { onAuthorClick(comment.userName) }
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = comment.userName,
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        comment.authorBadgeInfo?.let { badge ->
                            Spacer(modifier = Modifier.width(5.dp))
                            NebBadge(badge)
                        }
                    }
                    Text(
                        text = formatTimeAgo(comment.createdAt),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                if (canDelete) {
                    IconButton(onClick = onDelete, modifier = Modifier.size(32.dp)) {
                        Icon(
                            imageVector = Icons.Outlined.Delete,
                            contentDescription = "Delete",
                            tint = MaterialTheme.colorScheme.error,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = comment.content,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                lineHeight = 20.sp
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                LikePill(
                    count = comment.likeCount,
                    liked = comment.isLiked == true,
                    onClick = onThumbsUpClick
                )
            }
        }
    }
}

internal fun fileSizeHuman(bytes: Long): String {
    if (bytes <= 0) return ""
    val units = arrayOf("B", "KB", "MB", "GB")
    var value = bytes.toDouble()
    var unit = 0
    while (value >= 1024 && unit < units.size - 1) {
        value /= 1024
        unit++
    }
    return if (unit == 0) "${value.toInt()} ${units[unit]}" else String.format("%.1f %s", value, units[unit])
}

/**
 * Sticky "slide to buy" call-to-action shown at the very bottom of the resource
 * screen for a paid resource the viewer hasn't unlocked. The user drags the
 * thumb to the right to confirm purchase intent — a deliberate gesture that
 * avoids accidental taps on an irreversible action. Completing the slide fires
 * [onSlideComplete] exactly once; the caller owns what "buy" actually does
 * (today: open the checkout), so this component is purely the CTA + gesture.
 */
@Composable
fun SlideToBuyBar(
    price: String,
    onSlideComplete: () -> Unit,
    modifier: Modifier = Modifier
) {
    val trackColor = MaterialTheme.colorScheme.primary
    var trackWidthPx by remember { mutableFloatStateOf(0f) }
    val thumbSize = 56.dp
    var dragging by remember { mutableStateOf(false) }
    var rawProgress by remember { mutableFloatStateOf(0f) } // 0..1 while the finger is down
    var completed by remember { mutableStateOf(false) }
    var fired by remember { mutableStateOf(false) }

    // Smooth snap-back when released short, snap-to-end when the slide completes.
    val targetProgress = when {
        completed -> 1f
        dragging -> rawProgress
        else -> 0f
    }
    val animatedProgress by animateFloatAsState(
        targetValue = targetProgress,
        animationSpec = tween(if (completed) 220 else 260),
        label = "slideBuyProgress"
    )
    val progress = if (dragging) rawProgress else animatedProgress

    Surface(modifier = modifier.fillMaxWidth(), color = MaterialTheme.colorScheme.surfaceContainerLow) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(bottom = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(Icons.Filled.Lock, null, tint = trackColor, modifier = Modifier.size(16.dp))
                Text(
                    text = "This is paid content",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.weight(1f)
                )
                Text(
                    text = "Rs. $price",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.ExtraBold,
                    color = trackColor
                )
            }

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(60.dp)
                    .onSizeChanged { trackWidthPx = it.width.toFloat() }
                    .clip(RoundedCornerShape(999.dp))
                    .background(trackColor.copy(alpha = 0.14f))
                    .border(1.dp, trackColor.copy(alpha = 0.35f), RoundedCornerShape(999.dp))
            ) {
                val density = LocalDensity.current
                val thumbPx = with(density) { thumbSize.toPx() }
                val travel = (trackWidthPx - thumbPx).coerceAtLeast(1f)
                val thumbLeftPx = (progress * travel).coerceIn(0f, travel)

                // Fill that follows the thumb
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterStart)
                        .height(60.dp)
                        .fillMaxWidth(((thumbLeftPx + thumbPx) / trackWidthPx.coerceAtLeast(1f)).coerceIn(0f, 1f))
                        .background(
                            Brush.horizontalGradient(listOf(trackColor.copy(alpha = 0.85f), trackColor))
                        )
                )

                if (completed) {
                    Row(
                        modifier = Modifier.align(Alignment.Center),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(Icons.Filled.Check, null, tint = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(20.dp))
                        Text(
                            text = "Opening checkout…",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                    }
                } else {
                    // Centered hint — fades out as the thumb travels right
                    val labelAlpha = (1f - progress * 1.4f).coerceIn(0f, 1f)
                    Row(
                        modifier = Modifier.align(Alignment.Center).graphicsLayer { alpha = labelAlpha },
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(Icons.Filled.ShoppingCart, null, tint = trackColor, modifier = Modifier.size(18.dp))
                        Text(
                            text = "Slide to buy",
                            style = MaterialTheme.typography.titleSmall,
                            fontWeight = FontWeight.Bold,
                            color = trackColor
                        )
                    }
                }

                // Draggable thumb
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterStart)
                        .offset { IntOffset(x = thumbLeftPx.toInt(), y = 0) }
                        .size(thumbSize)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .border(1.dp, trackColor.copy(alpha = 0.4f), CircleShape)
                        .pointerInput(completed, trackWidthPx) {
                            if (completed || trackWidthPx <= 0f) return@pointerInput
                            detectDragGestures(
                                onDragStart = { dragging = true },
                                onDragEnd = {
                                    dragging = false
                                    if (rawProgress >= 0.92f) {
                                        completed = true
                                        if (!fired) {
                                            fired = true
                                            onSlideComplete()
                                        }
                                    }
                                },
                                onDragCancel = { dragging = false },
                                onDrag = { change, dragAmount ->
                                    change.consume()
                                    val travelLocal = (trackWidthPx - thumbPx).coerceAtLeast(1f)
                                    rawProgress = (rawProgress + dragAmount.x / travelLocal).coerceIn(0f, 1f)
                                }
                            )
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = if (completed) Icons.Filled.Check else Icons.Filled.ArrowForwardIos,
                        contentDescription = if (completed) "Purchased" else "Slide to buy",
                        tint = trackColor,
                        modifier = Modifier.size(22.dp)
                    )
                }
            }
        }
    }
}

/** Shown in place of the media player for a paid resource the viewer hasn't unlocked. */
@Composable
fun ResourceLockedMediaPlaceholder(
    subjectColor: Color,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(200.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(
                Brush.verticalGradient(
                    listOf(subjectColor.copy(alpha = 0.16f), MaterialTheme.colorScheme.surfaceContainerHigh)
                )
            )
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(12.dp)),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape)
                    .background(subjectColor.copy(alpha = 0.18f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Filled.Lock, null, tint = subjectColor, modifier = Modifier.size(28.dp))
            }
            Text(
                text = "Paid content",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface
            )
            Text(
                text = "Slide the bar below to unlock full access",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

/**
 * Native in-app checkout sheet for a paid resource the viewer hasn't unlocked.
 * Mirrors the website's QR checkout: shows the price + seller, lets the buyer
 * enter a transaction reference and attach a payment screenshot, then submits
 * the proof (server creates a pending PaymentVerification; an admin approves it
 * before access is granted). Reflects an existing pending/rejected submission.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourcePurchaseSheet(
    price: String,
    sellerName: String,
    purchaseStatus: String,
    submitting: Boolean,
    isAuthenticated: Boolean,
    onDismiss: () -> Unit,
    onSubmit: (transactionId: String, proofFile: File?) -> Unit,
    onSignInPrompt: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val context = LocalContext.current
    var transactionId by remember { mutableStateOf("") }
    var proofUri by remember { mutableStateOf<Uri?>(null) }

    val proofPicker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        proofUri = uri
    }

    val isPending = purchaseStatus.equals("pending", ignoreCase = true)
    val isRejected = purchaseStatus.equals("rejected", ignoreCase = true)
    val canSubmit = !submitting && (transactionId.isNotBlank() || proofUri != null)

    NebModalSheet(
        onDismiss = onDismiss,
        sheetState = sheetState
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .padding(bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Filled.Lock, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(22.dp))
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Unlock this resource",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "Rs. ${price.ifBlank { "0" }}",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.ExtraBold,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }

            // Status / instructions banner
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = when {
                    isPending -> MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f)
                    isRejected -> MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.6f)
                    else -> MaterialTheme.colorScheme.surfaceContainerLow
                },
                border = BorderStroke(
                    1.dp,
                    when {
                        isPending -> MaterialTheme.colorScheme.primary.copy(alpha = 0.25f)
                        isRejected -> MaterialTheme.colorScheme.error.copy(alpha = 0.3f)
                        else -> MaterialTheme.colorScheme.outlineVariant
                    }
                ),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(modifier = Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Icon(
                        imageVector = if (isPending) Icons.Filled.Check else if (isRejected) Icons.Outlined.Info else Icons.Outlined.QrCode2,
                        contentDescription = null,
                        tint = if (isRejected) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(20.dp)
                    )
                    Text(
                        text = when {
                            isPending -> "Payment pending verification. You'll get access once an admin approves it. You can re-submit updated proof below."
                            isRejected -> "Your previous payment couldn't be verified. Please double-check and re-submit below."
                            else -> "Pay Rs. ${price.ifBlank { "0" }} to $sellerName via eSewa, Khalti or mobile banking, then submit your transaction reference or a payment screenshot. Access unlocks after admin verification."
                        },
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            OutlinedTextField(
                value = transactionId,
                onValueChange = { transactionId = it },
                label = { Text("Transaction ID / Reference / Phone", maxLines = 1) },
                placeholder = { Text("e.g. 98XXXXXXXX or Txn #12345", maxLines = 1) },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                enabled = !submitting
            )

            // Payment proof attachment
            Surface(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .clickable(enabled = !submitting) { proofPicker.launch("image/*") },
                shape = RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.surfaceContainerLow,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
            ) {
                Row(
                    modifier = Modifier.padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    if (proofUri != null) {
                        AsyncImage(
                            model = proofUri,
                            contentDescription = "Payment proof",
                            modifier = Modifier.size(48.dp).clip(RoundedCornerShape(8.dp))
                        )
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Payment screenshot attached", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
                            Text("Tap to change", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                        }
                        IconButton(onClick = { proofUri = null }, enabled = !submitting) {
                            Icon(Icons.Filled.Close, contentDescription = "Remove", tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
                        }
                    } else {
                        Icon(Icons.Outlined.AttachFile, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(22.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Attach payment screenshot", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, maxLines = 1)
                            Text("Optional — or enter a transaction reference above", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2)
                        }
                        Icon(Icons.Outlined.CloudUpload, null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }

            NebButton(
                text = "Submit payment proof",
                onClick = {
                    if (isAuthenticated) {
                        onSubmit(transactionId, proofUri?.let { uriToCacheFile(context, it) })
                    } else {
                        onSignInPrompt()
                    }
                },
                icon = Icons.Outlined.CloudUpload,
                enabled = canSubmit,
                loading = submitting,
                size = NebButtonSize.Hero,
                fillWidth = true
            )
        }
    }
}

/** Copies a content Uri (a picked image) into a cache File for multipart upload. */
private fun uriToCacheFile(context: Context, uri: Uri): File? {
    return try {
        val tmp = File.createTempFile("payment_proof", ".jpg", context.cacheDir)
        context.contentResolver.openInputStream(uri)?.use { input ->
            FileOutputStream(tmp).use { output -> input.copyTo(output) }
        } ?: return null
        tmp
    } catch (_: Exception) {
        null
    }
}
