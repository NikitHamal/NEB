package com.neb.ians.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiReply
import com.neb.ians.util.formatTimeAgo

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun CommentCard(
    reply: ApiReply,
    isOwn: Boolean,
    onThumbsUpClick: () -> Unit,
    onProfileClick: (String) -> Unit,
    onLinkClick: (String) -> Unit,
    onAuthorLongPress: () -> Unit,
    onReplyClick: (() -> Unit)? = null,
    onBookmarkClick: (() -> Unit)? = null,
    onReportClick: (() -> Unit)? = null,
    onEditClick: (() -> Unit)? = null,
    onArchiveClick: (() -> Unit)? = null,
    onDeleteClick: (() -> Unit)? = null,
    replyingToUsername: String? = null,
    quotedContent: String? = null,
    children: List<ApiReply> = emptyList(),
    onRepliesBarClick: (() -> Unit)? = null,
    modifier: Modifier = Modifier
) {
    Surface(
        shape = RoundedCornerShape(8.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Box(
                    modifier = Modifier.combinedClickable(
                        onClick = { onProfileClick(reply.authorName) },
                        onLongClick = onAuthorLongPress
                    )
                ) {
                    val replyLevel = remember(reply.authorBadgeInfo) {
                        if (reply.authorBadgeInfo?.type == "verified") {
                            when (reply.authorBadgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(
                        name = reply.authorName,
                        imageUrl = reply.authorPhotoUrl,
                        size = 28.dp,
                        verificationLevel = replyLevel
                    )
                }
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = reply.authorName,
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier
                                .weight(1f, fill = false)
                                .combinedClickable(
                                    onClick = { onProfileClick(reply.authorName) },
                                    onLongClick = onAuthorLongPress
                                )
                        )
                        reply.authorBadgeInfo?.let { badge ->
                            Spacer(modifier = Modifier.width(5.dp))
                            NebBadge(badge)
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = formatTimeAgo(reply.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        if (reply.isArchived == true) {
                            Text(
                                text = " · archived",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        if (reply.isEdited == true) {
                            Text(
                                text = " · edited",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
                if (onBookmarkClick != null || onReportClick != null || onEditClick != null || onArchiveClick != null || onDeleteClick != null) {
                    PostMoreMenu(
                        isOwn = isOwn,
                        isBookmarked = reply.isBookmarked == true,
                        isArchived = reply.isArchived == true,
                        onBookmark = onBookmarkClick ?: {},
                        onReport = onReportClick ?: {},
                        onEdit = onEditClick ?: {},
                        onArchive = onArchiveClick ?: {},
                        onDelete = onDeleteClick ?: {}
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (!quotedContent.isNullOrBlank()) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text(
                            text = "\u201C",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = quotedContent,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }

            if (!replyingToUsername.isNullOrBlank() && quotedContent.isNullOrBlank()) {
                Surface(
                    shape = RoundedCornerShape(4.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    modifier = Modifier.padding(bottom = 6.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Replying to ",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "@$replyingToUsername",
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }

            MarkdownText(
                markdown = reply.content,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                onMentionClick = onProfileClick,
                onLinkClick = onLinkClick
            )

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                LikePill(
                    count = reply.thumbsUpCount,
                    liked = reply.isThumbedUp,
                    onClick = onThumbsUpClick
                )
                if (onReplyClick != null) {
                    Spacer(modifier = Modifier.width(12.dp))
                    Row(
                        modifier = Modifier
                            .clip(WebPillShape)
                            .clickable(onClick = onReplyClick)
                            .padding(horizontal = 8.dp, vertical = 5.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Outlined.Reply,
                            contentDescription = "Reply",
                            modifier = Modifier.size(16.dp),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "Reply",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                Spacer(modifier = Modifier.weight(1f))
            }

            if (children.isNotEmpty() && onRepliesBarClick != null) {
                Spacer(modifier = Modifier.height(8.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f))
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .clickable(onClick = onRepliesBarClick)
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    val firstChild = children.first()
                    val childLevel = remember(firstChild.authorBadgeInfo) {
                        if (firstChild.authorBadgeInfo?.type == "verified") {
                            when (firstChild.authorBadgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(
                        name = firstChild.authorName,
                        imageUrl = firstChild.authorPhotoUrl,
                        size = 20.dp,
                        verificationLevel = childLevel
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "${children.size} ${if (children.size == 1) "reply" else "replies"}",
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.weight(1f))
                    Icon(
                        imageVector = Icons.Outlined.ChatBubbleOutline,
                        contentDescription = "View thread",
                        modifier = Modifier.size(16.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
}
