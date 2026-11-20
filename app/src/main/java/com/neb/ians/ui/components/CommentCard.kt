package com.neb.ians.ui.components

import androidx.compose.ui.layout.layout
import com.neb.ians.data.api.shownName
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
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.widthIn
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.runtime.getValue
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.luminance
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.draw.drawBehind
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiReply
import com.neb.ians.util.formatTimeAgo
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType

@OptIn(ExperimentalFoundationApi::class, androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
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
    onLabelClick: (() -> Unit)? = null,
      replyingToUsername: String? = null,
      quotedContent: String? = null,
      children: List<ApiReply> = emptyList(),
      onRepliesBarClick: (() -> Unit)? = null,
      onInlineImageClick: (String) -> Unit = {},
      pollContent: (@Composable (com.neb.ians.data.api.ApiPoll) -> Unit)? = null,
      highlighted: Boolean = false,
      modifier: Modifier = Modifier
  ) {
    val tactile = rememberTactileFeedback()
    // Flat like a web reply: no frame, one hairline under the row, the body indented past the avatar.
    val hairline = MaterialTheme.colorScheme.outlineVariant
    val scheme = MaterialTheme.colorScheme
    val dark = scheme.surface.luminance() < 0.5f
    val accepted = reply.label == "accepted"
    val acceptedFill = ReplyTones.good(dark).copy(alpha = 0.55f)
    val acceptedLine = ReplyTones.goodLine(dark)
    val everHighlighted = remember { androidx.compose.runtime.mutableStateOf(false) }
    if (highlighted) everHighlighted.value = true
    val flash = if (everHighlighted.value) {
        animateColorAsState(
            targetValue = if (highlighted) scheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent,
            animationSpec = tween(if (highlighted) 160 else 1800),
            label = "replyFlash"
        ).value
    } else androidx.compose.ui.graphics.Color.Transparent
    val dim = when (reply.label) { "spam" -> 0.72f; "incorrect" -> 0.9f; else -> 1f }
    Column(
        modifier = modifier
            .fillMaxWidth()
            .drawBehind {
                if (accepted) {
                    drawRect(acceptedFill)
                    drawRect(acceptedLine, size = androidx.compose.ui.geometry.Size(4.dp.toPx(), size.height))
                }
                if (flash.alpha > 0f) drawRect(flash)
            }
            .bottomHairline(hairline)
            .then(if (dim < 1f) Modifier.graphicsLayer { alpha = dim } else Modifier)
            .padding(horizontal = 16.dp, vertical = 14.dp)
    ) {
            Row(
                modifier = Modifier.trimSingleLineTail(6.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Box(
                    modifier = if (reply.isAnonymous) Modifier
                    else Modifier.combinedClickable(
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
                        name = reply.shownName,
                        imageUrl = reply.authorPhotoUrl,
                        size = 36.dp,
                        verificationLevel = replyLevel
                    )
                }
                Column(modifier = Modifier.weight(1f)) {
                    // the web's `.author-line`: name, badge, dot, time, then the kind and label chips on the same line
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(2.dp)
                    ) {
                        Row(
                            modifier = Modifier.height(20.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = reply.shownName,
                                style = MaterialTheme.typography.labelMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                modifier = Modifier
                                    .widthIn(max = 168.dp)
                                    .then(
                                        if (reply.isAnonymous) Modifier
                                        else Modifier.combinedClickable(
                                            onClick = { onProfileClick(reply.authorName) },
                                            onLongClick = onAuthorLongPress
                                        )
                                    )
                            )
                            if (reply.isAnonymous) {
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(
                                    imageVector = Icons.Outlined.VisibilityOff,
                                    contentDescription = "Anonymous",
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                    modifier = Modifier.size(13.dp)
                                )
                            }
                            reply.authorBadgeInfo?.let { badge ->
                                Spacer(modifier = Modifier.width(4.dp))
                                NebBadge(badge)
                            }
                            Text(
                                text = "\u00B7",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(horizontal = 6.dp)
                            )
                            val replyMeta = remember(reply.createdAt, reply.isArchived, reply.isEdited) {
                                formatTimeAgo(reply.createdAt) +
                                    (if (reply.isArchived == true) ", archived" else "") +
                                    (if (reply.isEdited == true) ", edited" else "")
                            }
                            Text(
                                text = replyMeta,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1
                            )
                        }
                        ReplyKindTag(reply.kind)
                        ReplyLabelTag(reply.label)
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

            Column(modifier = Modifier.padding(start = 48.dp)) {
            Spacer(modifier = Modifier.height(2.dp))

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
                            color = MaterialTheme.colorScheme.primary,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }

            ExpandableMarkdownText(
                markdown = reply.content,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                onMentionClick = onProfileClick,
                onLinkClick = onLinkClick,
                minimizedMaxLines = 5,
                onInlineImageClick = onInlineImageClick
            )

            if (reply.attachments.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                ForumMediaAttachments(reply.attachments)
            }

            val replyPoll = reply.poll
            if (replyPoll != null && pollContent != null) {
                pollContent(replyPoll)
            }

            Spacer(modifier = Modifier.height(2.dp))

            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth().nebGhostRowStart()
            ) {
                LikePill(
                    count = reply.thumbsUpCount,
                    liked = reply.isThumbedUp,
                    onClick = onThumbsUpClick
                )
                if (reply.canLabel && onLabelClick != null) {
                    Spacer(modifier = Modifier.width(2.dp))
                    Row(
                        modifier = Modifier
                            .clip(WebPillShape)
                            .clickable(onClick = {
                                tactile.perform(TactileType.LightTap)
                                onLabelClick()
                            })
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.CheckCircle,
                            contentDescription = "Mark reply",
                            modifier = Modifier.size(16.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Text(
                            text = if (reply.label.isNotBlank()) "Marked" else "Mark",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
                if (onReplyClick != null) {
                    Spacer(modifier = Modifier.width(2.dp))
                    Row(
                        modifier = Modifier
                            .clip(WebPillShape)
                            .clickable(onClick = {
                                tactile.perform(TactileType.LightTap)
                                onReplyClick()
                            })
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Outlined.Reply,
                            contentDescription = "Reply",
                            modifier = Modifier.size(16.dp),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "Reply",
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Medium,
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
                        .clickable(onClick = {
                            tactile.perform(TactileType.SelectionChange)
                            onRepliesBarClick()
                        })
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
                        name = firstChild.shownName,
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

/** A one-pixel line along the bottom edge, the web's divider between rows. */
private fun Modifier.bottomHairline(color: androidx.compose.ui.graphics.Color): Modifier =
    this.drawBehind {
        val h = 1.dp.toPx()
        drawRect(color, topLeft = androidx.compose.ui.geometry.Offset(0f, size.height - h), size = androidx.compose.ui.geometry.Size(size.width, h))
    }

/**
 * A one-line comment header is as tall as its avatar, which left a dead band between the name and the text.
 * When the header is that single line, report [tail] less height so the body sits right under the name.
 */
private fun Modifier.trimSingleLineTail(tail: androidx.compose.ui.unit.Dp): Modifier =
    this.layout { measurable, constraints ->
        val placeable = measurable.measure(constraints)
        val oneLine = placeable.height <= 40.dp.roundToPx()
        val trim = if (oneLine) tail.roundToPx() else 0
        layout(placeable.width, placeable.height - trim) { placeable.place(0, 0) }
    }
