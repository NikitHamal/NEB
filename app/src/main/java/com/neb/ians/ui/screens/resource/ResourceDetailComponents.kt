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
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.ThumbUp
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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
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
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiResourceComment
import com.neb.ians.ui.components.ExpandableText
import com.neb.ians.ui.components.NebAvatar

import com.neb.ians.util.formatTimeAgo
import com.neb.ians.util.getSubjectColor

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
fun ResourceHeroCard(
    resource: ApiResource,
    isLiked: Boolean,
    likeCount: Int,
    isBookmarked: Boolean,
    canLike: Boolean,
    canBookmark: Boolean,
    onRead: () -> Unit,
    onDownload: () -> Unit,
    onLike: () -> Unit,
    onBookmark: () -> Unit,
    onShare: () -> Unit,
    onUserProfileClick: (String) -> Unit = {}
) {
    val subject = resource.subject.split(",").firstOrNull()?.trim().orEmpty().ifBlank { "General" }
    val subjectColor = Color(getSubjectColor(subject))
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        shape = RoundedCornerShape(8.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        tonalElevation = 0.dp,
        shadowElevation = 0.dp
    ) {
        Box {
            ResourceHeroArt(subjectColor = subjectColor, modifier = Modifier.align(Alignment.TopEnd))
            Column(modifier = Modifier.padding(18.dp)) {
                ResourceChips(resource = resource, subject = subject, subjectColor = subjectColor)
                Spacer(Modifier.height(14.dp))
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    lineHeight = 31.sp,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(Modifier.height(10.dp))
                ResourceMetaBar(resource = resource, onUserProfileClick = onUserProfileClick)
                if (resource.description.isNotBlank()) {
                    Spacer(Modifier.height(18.dp))
                    ExpandableText(
                        text = resource.description,
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 15.sp
                    )
                }
                ResourceFilesSection(
                    resource = resource,
                    onRead = onRead,
                    onDownload = onDownload,
                    modifier = Modifier.padding(top = 24.dp)
                )
                ResourceActionBar(
                    isLiked = isLiked,
                    likeCount = likeCount,
                    isBookmarked = isBookmarked,
                    canLike = canLike,
                    canBookmark = canBookmark,
                    onLike = onLike,
                    onBookmark = onBookmark,
                    onShare = onShare,
                    modifier = Modifier.padding(top = 14.dp)
                )
            }
        }
    }
}

@Composable
private fun ResourceHeroArt(subjectColor: Color, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .size(width = 170.dp, height = 260.dp)
            .clip(RoundedCornerShape(bottomStart = 180.dp))
            .background(subjectColor.copy(alpha = 0.045f))
    )
}

@Composable
private fun ResourceChips(resource: ApiResource, subject: String, subjectColor: Color) {
    Row(
        modifier = Modifier.horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ResourceChip(
            text = subject,
            icon = Icons.Outlined.Description,
            contentColor = subjectColor,
            backgroundColor = subjectColor.copy(alpha = 0.06f),
            borderColor = subjectColor.copy(alpha = 0.22f)
        )
        ResourceChip(
            text = resource.type.ifBlank { "Resource" },
            icon = if (detectResourceMedia(resource.fileUrl, resource.type) == ResourceMediaType.Pdf) Icons.Outlined.Description else Icons.Outlined.Folder,
            contentColor = MaterialTheme.colorScheme.primary,
            backgroundColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.06f),
            borderColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.22f)
        )
        if (resource.gradeLevel.isNotBlank()) {
            ResourceChip(
                text = resource.gradeLevel,
                contentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                backgroundColor = MaterialTheme.colorScheme.surfaceContainerLow,
                borderColor = MaterialTheme.colorScheme.outlineVariant
            )
        }
    }
}

@Composable
private fun ResourceChip(
    text: String,
    contentColor: Color,
    backgroundColor: Color,
    borderColor: Color,
    icon: ImageVector? = null
) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(999.dp))
            .background(backgroundColor)
            .border(1.dp, borderColor, RoundedCornerShape(999.dp))
            .padding(horizontal = 10.dp, vertical = 5.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        if (icon != null) Icon(icon, null, modifier = Modifier.size(14.dp), tint = contentColor)
        Text(text, color = contentColor, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, maxLines = 1)
    }
}

@Composable
private fun ResourceMetaBar(resource: ApiResource, onUserProfileClick: (String) -> Unit) {
    Row(
        modifier = Modifier.horizontalScroll(rememberScrollState()),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        when (resource.sourceType) {
            "external" -> ResourceMetaItem(Icons.Outlined.Public, resource.sourceLabel ?: "External Source", highlight = Color(0xFFE37400))
            "anonymous" -> ResourceMetaItem(Icons.Outlined.Public, "Anonymous")
            "user" -> ResourceMetaItem(Icons.Outlined.CloudUpload, "Community", highlight = Color(0xFF0D652D))
            else -> ResourceMetaItem(Icons.Outlined.Verified, "NEBians Team", highlight = MaterialTheme.colorScheme.primary)
        }
        val uploadUsername = resource.uploadedByUsername.ifBlank { resource.authorName.orEmpty() }
        if (resource.sourceType == "user" && uploadUsername.isNotBlank()) {
            ResourceMetaItem(
                icon = null,
                text = uploadUsername,
                highlight = MaterialTheme.colorScheme.primary,
                onClick = { onUserProfileClick(uploadUsername) }
            )
        } else if (!resource.authorName.isNullOrBlank()) {
            ResourceMetaItem(null, resource.authorName)
        }
        ResourceDot()
        ResourceMetaItem(Icons.Outlined.Schedule, formatTimeAgo(resource.addedAt))
        ResourceDot()
        ResourceMetaItem(Icons.Outlined.Visibility, "${resource.viewCount} views")
        if (resource.fileSize > 0) {
            ResourceDot()
            ResourceMetaItem(Icons.Outlined.Folder, fileSizeHuman(resource.fileSize))
        }
    }
}

@Composable
private fun ResourceMetaItem(icon: ImageVector?, text: String, highlight: Color? = null, onClick: (() -> Unit)? = null) {
    val color = highlight ?: MaterialTheme.colorScheme.onSurfaceVariant
    val modifier = if (onClick != null) {
        Modifier
            .clip(RoundedCornerShape(999.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 3.dp, vertical = 2.dp)
    } else {
        Modifier
    }
    Row(modifier = modifier, verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        if (icon != null) Icon(icon, null, tint = color, modifier = Modifier.size(16.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            color = color,
            fontWeight = if (highlight != null) FontWeight.SemiBold else FontWeight.Medium
        )
    }
}

@Composable
private fun ResourceDot() {
    Text("·", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.45f))
}

@Composable
private fun ResourceFilesSection(resource: ApiResource, onRead: () -> Unit, onDownload: () -> Unit, modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxWidth()) {
        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
        Row(
            modifier = Modifier.padding(top = 20.dp, bottom = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(Icons.Outlined.Description, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
            Text("Available Files (${if (resource.fileUrl.isBlank()) 0 else 1})", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.Bold)
        }
        if (resource.fileUrl.isNotBlank()) {
            ResourceFileCard(resource = resource, onRead = onRead, onDownload = onDownload)
        }
    }
}

@Composable
private fun ResourceFileCard(resource: ApiResource, onRead: () -> Unit, onDownload: () -> Unit) {
    val mediaType = detectResourceMedia(resource.fileUrl, resource.type)
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        shape = RoundedCornerShape(12.dp),
        tonalElevation = 0.dp
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Box(
                    modifier = Modifier
                        .size(46.dp)
                        .clip(RoundedCornerShape(9.dp))
                        .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                    contentAlignment = Alignment.Center
                ) {
                    val cardIcon = when (mediaType) {
                        ResourceMediaType.Pdf -> Icons.Outlined.Description
                        ResourceMediaType.Image -> Icons.Outlined.Image
                        ResourceMediaType.Video -> Icons.Outlined.PlayCircle
                        ResourceMediaType.Audio -> Icons.Outlined.Headphones
                        else -> Icons.Outlined.Folder
                    }
                    Icon(
                        imageVector = cardIcon,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(25.dp)
                    )
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = resource.title,
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(Modifier.height(4.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            resource.type.ifBlank { "File" }.uppercase(),
                            modifier = Modifier
                                .clip(RoundedCornerShape(5.dp))
                                .background(MaterialTheme.colorScheme.surfaceContainerHighest)
                                .padding(horizontal = 6.dp, vertical = 2.dp),
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                        if (resource.fileSize > 0) Text("· ${fileSizeHuman(resource.fileSize)}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 13.sp)
                    }
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
                Button(
                    onClick = onRead,
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(999.dp),
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 14.dp, vertical = 10.dp)
                ) {
                    val buttonIcon = when (mediaType) {
                        ResourceMediaType.Pdf -> Icons.Filled.MenuBook
                        ResourceMediaType.Image -> Icons.Outlined.Image
                        ResourceMediaType.Video, ResourceMediaType.Audio -> Icons.Outlined.PlayCircle
                        else -> Icons.Filled.OpenInNew
                    }
                    val buttonText = when (mediaType) {
                        ResourceMediaType.Pdf -> "Read"
                        ResourceMediaType.Image -> "View"
                        ResourceMediaType.Video, ResourceMediaType.Audio -> "Play"
                        else -> "Open"
                    }
                    Icon(buttonIcon, null, modifier = Modifier.size(17.dp))
                    Spacer(Modifier.width(7.dp))
                    Text(buttonText, fontWeight = FontWeight.Bold)
                }
                Button(
                    onClick = onDownload,
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(999.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.secondaryContainer,
                        contentColor = MaterialTheme.colorScheme.onSecondaryContainer
                    ),
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 14.dp, vertical = 10.dp)
                ) {
                    Icon(Icons.Filled.Download, null, modifier = Modifier.size(17.dp))
                    Spacer(Modifier.width(7.dp))
                    Text("Download", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
private fun ResourceActionBar(
    isLiked: Boolean,
    likeCount: Int,
    isBookmarked: Boolean,
    canLike: Boolean,
    canBookmark: Boolean,
    onLike: () -> Unit,
    onBookmark: () -> Unit,
    onShare: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(10.dp, Alignment.End),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ResourcePillAction(
            icon = if (isLiked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
            text = likeCount.toString(),
            selected = isLiked,
            enabled = canLike,
            onClick = onLike
        )
        ResourceIconAction(
            icon = if (isBookmarked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
            selected = isBookmarked,
            enabled = canBookmark,
            contentDescription = "Bookmark",
            onClick = onBookmark
        )
        ResourceIconAction(icon = Icons.Filled.Share, selected = false, contentDescription = "Share", onClick = onShare)
    }
}

@Composable
private fun ResourcePillAction(icon: ImageVector, text: String, selected: Boolean, enabled: Boolean, onClick: () -> Unit) {
    val color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(999.dp))
            .border(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(999.dp))
            .background(if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.07f) else Color.Transparent)
            .clickable(enabled = enabled, onClick = onClick)
            .padding(horizontal = 14.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, null, tint = color, modifier = Modifier.size(18.dp))
        Text(text, color = color, fontWeight = FontWeight.Bold, fontSize = 13.sp)
    }
}

@Composable
private fun ResourceIconAction(icon: ImageVector, selected: Boolean, contentDescription: String, enabled: Boolean = true, onClick: () -> Unit) {
    val color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = Modifier
            .size(38.dp)
            .clip(CircleShape)
            .border(1.dp, if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant, CircleShape)
            .background(if (selected) MaterialTheme.colorScheme.primary.copy(alpha = 0.07f) else Color.Transparent)
            .clickable(enabled = enabled, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Icon(icon, contentDescription, tint = color, modifier = Modifier.size(20.dp))
    }
}

@Composable
fun ResourceCommentsHeader(count: Int, modifier: Modifier = Modifier) {
    Row(modifier = modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Comments", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold)
        Text("($count)", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
fun ResourceCommentsLoading() {
    Box(modifier = Modifier.fillMaxWidth().padding(22.dp), contentAlignment = Alignment.Center) {
        CircularProgressIndicator(modifier = Modifier.size(24.dp), strokeWidth = 2.5.dp)
    }
}

@Composable
fun ResourceEmptyComments() {
    Column(
        modifier = Modifier.fillMaxWidth().padding(vertical = 34.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(Icons.Outlined.ChatBubbleOutline, null, tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.45f), modifier = Modifier.size(38.dp))
        Text("No comments yet. Be the first!", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
fun ResourceCommentItem(
    comment: ApiResourceComment,
    canDelete: Boolean,
    onDelete: () -> Unit,
    onAuthorClick: (String) -> Unit = {}
) {
    Surface(
        modifier = Modifier.fillMaxWidth().padding(bottom = 10.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        shape = RoundedCornerShape(8.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        tonalElevation = 0.dp
    ) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                NebAvatar(
                    photoUrl = comment.userPhotoUrl,
                    name = comment.userName,
                    size = 34.dp,
                    modifier = Modifier.clickable(enabled = comment.userName.isNotBlank()) { onAuthorClick(comment.userName) }
                )
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clickable(enabled = comment.userName.isNotBlank()) { onAuthorClick(comment.userName) }
                ) {
                    Text(comment.userName, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text(formatTimeAgo(comment.createdAt), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (canDelete) {
                    IconButton(onClick = onDelete, modifier = Modifier.size(32.dp)) {
                        Icon(Icons.Outlined.Delete, contentDescription = "Delete", tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(18.dp))
                    }
                }
            }
            Text(comment.content, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface, lineHeight = 20.sp)
        }
    }
}

private fun fileSizeHuman(bytes: Long): String {
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
