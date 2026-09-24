@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class,
    androidx.compose.foundation.layout.ExperimentalLayoutApi::class
)

package com.neb.ians.ui.screens.resource

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Bookmark
import androidx.compose.material.icons.rounded.BookmarkBorder
import androidx.compose.material.icons.rounded.Description
import androidx.compose.material.icons.rounded.Download
import androidx.compose.material.icons.rounded.Folder
import androidx.compose.material.icons.rounded.Headphones
import androidx.compose.material.icons.rounded.Image
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.MenuBook
import androidx.compose.material.icons.rounded.OpenInNew
import androidx.compose.material.icons.rounded.PlayCircle
import androidx.compose.material.icons.rounded.Share
import androidx.compose.material.icons.rounded.ThumbUp
import androidx.compose.material.icons.rounded.Verified
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.compositeOver
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.ExpandableText
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.theme.NebAccent
import com.neb.ians.ui.theme.NebAccents
import com.neb.ians.ui.theme.nebEffectsSpec
import com.neb.ians.ui.theme.resolve
import com.neb.ians.util.formatTimeAgo

// ---------------------------------------------------------------------------
// The head of a resource page: what it is, who put it there, and the one
// button that opens it.
//
// No card around the whole thing — the page itself is the card. The only
// container is the file, because that is the thing being handed over. Colour
// appears twice and only where it carries meaning: amber on a paid resource,
// rose on a like that is yours.
// ---------------------------------------------------------------------------

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
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 6.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        ResourceTagRow(resource)

        Text(
            text = resource.title,
            style = MaterialTheme.typography.headlineSmallEmphasized,
            color = MaterialTheme.colorScheme.onSurface
        )

        ResourceByline(resource = resource, onUserProfileClick = onUserProfileClick)

        if (resource.description.isNotBlank()) {
            ExpandableText(
                text = resource.description,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 15.sp
            )
        }

        ResourceFactsStrip(resource)

        if (resource.fileUrl.isNotBlank()) {
            ResourceFileCard(resource = resource, onRead = onRead, onDownload = onDownload)
        }

        ResourceActionBar(
            isLiked = isLiked,
            likeCount = likeCount,
            isBookmarked = isBookmarked,
            canLike = canLike,
            canBookmark = canBookmark,
            onLike = onLike,
            onBookmark = onBookmark,
            onShare = onShare
        )
    }
}

@Composable
private fun ResourceTagRow(resource: ApiResource) {
    val subjects = resource.subject.split(",").map { it.trim() }.filter { it.isNotBlank() }
    FlowRow(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        subjects.take(3).forEach { ResourceTag(text = it) }
        if (resource.gradeLevel.isNotBlank()) ResourceTag(text = resource.gradeLevel)
        if (resource.isPaid) {
            ResourceTag(
                text = "Rs. ${resource.price.ifBlank { "0" }}",
                icon = Icons.Rounded.Lock,
                accent = NebAccents.Amber
            )
        }
    }
}

@Composable
private fun ResourceTag(text: String, icon: ImageVector? = null, accent: NebAccent? = null) {
    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    val accentColor = accent?.resolve()
    val content = accentColor ?: scheme.onSurface
    val fill = accentColor
        ?.copy(alpha = if (isDark) 0.17f else 0.10f)
        ?.compositeOver(scheme.surface)
        ?: scheme.surfaceContainerHigh

    Row(
        modifier = Modifier
            .clip(CircleShape)
            .background(fill)
            .padding(horizontal = 11.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        if (icon != null) {
            Icon(icon, contentDescription = null, tint = content, modifier = Modifier.size(13.dp))
        }
        Text(
            text = text,
            style = MaterialTheme.typography.labelMedium,
            color = content,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
private fun ResourceByline(resource: ApiResource, onUserProfileClick: (String) -> Unit) {
    val name = resource.uploadedByName
        .ifBlank { resource.uploadedByUsername }
        .ifBlank { resource.authorName.orEmpty() }
        .ifBlank { "NEBians" }
    val isOfficial = name.equals("NEBians", ignoreCase = true)
    val isAnon = resource.isAnonymous || name.equals("Anonymous", ignoreCase = true)
    val username = resource.uploadedByUsername.ifBlank { resource.authorUsernameSnake.orEmpty() }
    val openable = username.isNotBlank() && !isAnon

    Row(
        modifier = Modifier
            .then(
                if (openable) Modifier.nebPressable(onClick = { onUserProfileClick(username) })
                else Modifier
            )
            .clip(RoundedCornerShape(18.dp)),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Avatar(name = name, imageUrl = resource.uploadedByPhoto, size = 36.dp)
        Column {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(5.dp)
            ) {
                Text(
                    text = name,
                    style = MaterialTheme.typography.titleSmallEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                if (isOfficial) {
                    Icon(
                        imageVector = Icons.Rounded.Verified,
                        contentDescription = "Official",
                        tint = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.size(14.dp)
                    )
                }
            }
            Text(
                text = formatTimeAgo(resource.addedAt),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

/** Views, size, downloads — the numbers, read as numbers. */
@Composable
private fun ResourceFactsStrip(resource: ApiResource) {
    val facts = buildList {
        add("Views" to resource.viewCount.toString())
        if (resource.fileSize > 0) add("Size" to fileSizeHuman(resource.fileSize))
        if (resource.type.isNotBlank()) add("Format" to resource.type.uppercase())
    }
    if (facts.isEmpty()) return

    val shape = RoundedCornerShape(22.dp)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        facts.forEachIndexed { index, (label, value) ->
            Column(
                modifier = Modifier.weight(1f),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = value,
                    style = MaterialTheme.typography.titleMediumEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = label,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (index != facts.lastIndex) {
                Box(
                    modifier = Modifier
                        .width(1.dp)
                        .height(28.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                )
            }
        }
    }
}

@Composable
private fun ResourceFileCard(resource: ApiResource, onRead: () -> Unit, onDownload: () -> Unit) {
    val mediaType = detectResourceMedia(resource.fileUrl, resource.type)
    val shape = RoundedCornerShape(24.dp)

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, shape)
            .padding(14.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(46.dp)
                    .clip(RoundedCornerShape(15.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainerHighest),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = when (mediaType) {
                        ResourceMediaType.Pdf -> Icons.Rounded.Description
                        ResourceMediaType.Image -> Icons.Rounded.Image
                        ResourceMediaType.Video -> Icons.Rounded.PlayCircle
                        ResourceMediaType.Audio -> Icons.Rounded.Headphones
                        else -> Icons.Rounded.Folder
                    },
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.size(22.dp)
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.titleSmallEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = listOfNotNull(
                        resource.type.ifBlank { "File" }.uppercase(),
                        fileSizeHuman(resource.fileSize).takeIf { it.isNotBlank() }
                    ).joinToString(", "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            NebButton(
                text = when (mediaType) {
                    ResourceMediaType.Pdf -> "Read"
                    ResourceMediaType.Image -> "View"
                    ResourceMediaType.Video, ResourceMediaType.Audio -> "Play"
                    else -> "Open"
                },
                onClick = onRead,
                icon = when (mediaType) {
                    ResourceMediaType.Pdf -> Icons.Rounded.MenuBook
                    ResourceMediaType.Image -> Icons.Rounded.Image
                    ResourceMediaType.Video, ResourceMediaType.Audio -> Icons.Rounded.PlayCircle
                    else -> Icons.Rounded.OpenInNew
                },
                modifier = Modifier.weight(1f)
            )
            if (mediaType != ResourceMediaType.Pdf) {
                NebButton(
                    text = "Download",
                    onClick = onDownload,
                    icon = Icons.Rounded.Download,
                    tone = NebButtonTone.Outlined,
                    modifier = Modifier.weight(1f)
                )
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
    onShare: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ResourceAction(
            icon = Icons.Rounded.ThumbUp,
            label = if (likeCount > 0) likeCount.toString() else "Like",
            selected = isLiked,
            enabled = canLike,
            accent = NebAccents.Rose,
            onClick = onLike
        )
        ResourceAction(
            icon = if (isBookmarked) Icons.Rounded.Bookmark else Icons.Rounded.BookmarkBorder,
            label = if (isBookmarked) "Saved" else "Save",
            selected = isBookmarked,
            enabled = canBookmark,
            accent = NebAccents.Amber,
            onClick = onBookmark
        )
        Spacer(modifier = Modifier.weight(1f))
        ResourceAction(
            icon = Icons.Rounded.Share,
            label = "Share",
            selected = false,
            enabled = true,
            accent = null,
            onClick = onShare
        )
    }
}

@Composable
private fun ResourceAction(
    icon: ImageVector,
    label: String,
    selected: Boolean,
    enabled: Boolean,
    accent: NebAccent?,
    onClick: () -> Unit
) {
    val scheme = MaterialTheme.colorScheme
    val isDark = scheme.surface.luminance() < 0.5f
    val accentColor = accent?.resolve()

    val content by animateColorAsState(
        targetValue = when {
            !enabled -> scheme.onSurfaceVariant.copy(alpha = 0.5f)
            selected -> accentColor ?: scheme.onSurface
            else -> scheme.onSurfaceVariant
        },
        animationSpec = nebEffectsSpec(),
        label = "resource_action_content"
    )
    val fill by animateColorAsState(
        targetValue = if (selected && accentColor != null) {
            accentColor.copy(alpha = if (isDark) 0.17f else 0.10f).compositeOver(scheme.surface)
        } else {
            scheme.surfaceContainerHigh
        },
        animationSpec = nebEffectsSpec(),
        label = "resource_action_fill"
    )

    Row(
        modifier = Modifier
            .nebPressable(enabled = enabled, onClick = onClick)
            .clip(CircleShape)
            .background(if (enabled) fill else scheme.surfaceContainerHigh.copy(alpha = 0.6f))
            .padding(horizontal = 14.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(7.dp)
    ) {
        Icon(icon, contentDescription = label, tint = content, modifier = Modifier.size(17.dp))
        Text(text = label, style = MaterialTheme.typography.labelLarge, color = content, maxLines = 1)
    }
}
