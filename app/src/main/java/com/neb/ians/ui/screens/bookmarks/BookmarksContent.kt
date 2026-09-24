package com.neb.ians.ui.screens.bookmarks

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.ShimmerCircle
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.util.TactileType
import com.neb.ians.util.formatTimeAgo

// ---------------------------------------------------------------------------
// The rows of the bookmark list.
//
// A saved thing is already familiar to the person who saved it, so the row
// carries no card, no border and no badge — a glyph to say what kind it is,
// the title it was saved under, one line of what it said, and the filled
// bookmark that takes it back out again.
// ---------------------------------------------------------------------------

@Composable
fun BookmarkSectionHeader(label: String) {
    Text(
        text = label,
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        modifier = Modifier.padding(start = 4.dp, top = 16.dp, bottom = 6.dp)
    )
}

@Composable
fun BookmarkRow(
    item: BookmarkListItem,
    onClick: () -> Unit,
    onRemove: () -> Unit,
    showDivider: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.985f, tactile = TactileType.ButtonTap, onClick = onClick)
                .padding(vertical = 12.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(RoundedCornerShape(13.dp))
                    .background(scheme.surfaceContainerHigh),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = glyphFor(item.bookmark.targetType),
                    contentDescription = null,
                    tint = scheme.onSurfaceVariant,
                    modifier = Modifier.size(19.dp)
                )
            }

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = kickerFor(item),
                    style = MaterialTheme.typography.labelSmall,
                    color = scheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleSmall,
                    color = scheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                if (item.excerpt.isNotBlank()) {
                    Spacer(modifier = Modifier.height(3.dp))
                    Text(
                        text = item.excerpt,
                        style = MaterialTheme.typography.bodySmall,
                        color = scheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }

            NebIconButton(
                icon = Icons.Filled.Bookmark,
                contentDescription = "Remove bookmark",
                onClick = onRemove,
                tint = scheme.onSurfaceVariant,
                size = 34.dp
            )
        }

        if (showDivider) {
            HorizontalDivider(
                color = scheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(start = 54.dp)
            )
        }
    }
}

@Composable
fun BookmarkRowSkeleton() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        ShimmerCircle(size = 42.dp)
        Column(modifier = Modifier.weight(1f)) {
            ShimmerLine(widthFraction = 0.28f, height = 9.dp)
            Spacer(modifier = Modifier.height(8.dp))
            ShimmerLine(widthFraction = 0.72f, height = 13.dp)
            Spacer(modifier = Modifier.height(7.dp))
            ShimmerLine(widthFraction = 0.94f, height = 10.dp)
        }
    }
}

private fun glyphFor(type: String): ImageVector = when (type) {
    "post" -> Icons.Outlined.Forum
    "reply" -> Icons.Outlined.ChatBubbleOutline
    else -> Icons.Outlined.Description
}

private fun kickerFor(item: BookmarkListItem): String {
    val kind = when (item.bookmark.targetType) {
        "post" -> "Post"
        "reply" -> "Reply"
        "resource" -> "Resource"
        else -> item.bookmark.targetType.replaceFirstChar { it.uppercase() }
    }
    val saved = formatTimeAgo(item.bookmark.createdAt)
    return if (item.meta.isBlank()) "$kind · $saved" else "$kind · $saved · ${item.meta}"
}
