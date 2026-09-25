package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.ui.components.ShimmerCircle
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPostCard
import com.neb.ians.ui.components.buildInlineAnnotatedString
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.markdownToInlinePreview
import com.neb.ians.util.formatTimeAgo

// ---------------------------------------------------------------------------
// The cards of the profile's three feeds.
//
// Posts and resources are the same cards the forum and the library show, so
// something you saw there looks the same here. Replies have no card anywhere
// else in the app, so they get one of their own, built to the same rules:
// panel shape, hairline border, lowest surface, 14dp of padding.
// ---------------------------------------------------------------------------

/** A post, shown exactly as the forum shows it. */
@Composable
fun ProfilePostCard(
    post: ApiPost,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    WebPostCard(
        post = post,
        onClick = onClick,
        onLikeClick = {},
        modifier = modifier,
        compact = true
    )
}

/**
 * A reply.
 *
 * A reply is two things at once -- the thing being answered and the answer --
 * and the card says so in that order. The question sits at the top inside a
 * quote block: held behind a rule, on a raised fill, in the grey this app
 * reserves for context. The answer follows on the card's own surface at full
 * weight, because the answer is what the reader came for, and the old card
 * buried it in grey under a bold "Reply on ..." heading.
 */
@Composable
fun ProfileReplyCard(
    reply: ApiReply,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val preview = remember(reply.content) { markdownToInlinePreview(reply.content) }
    val body = remember(preview, scheme.onSurface, scheme.surfaceContainerHigh) {
        buildInlineAnnotatedString(
            text = preview,
            baseColor = scheme.onSurface,
            primary = scheme.onSurface,
            codeBg = scheme.surfaceContainerHigh
        )
    }

    Card(
        modifier = modifier
            .fillMaxWidth()
            .clip(WebPanelShape)
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(containerColor = scheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, scheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {

            // The quote block: a rule, then what was asked.
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(IntrinsicSize.Min)
                    .clip(RoundedCornerShape(10.dp))
                    .background(scheme.surfaceContainerHigh)
            ) {
                Box(
                    modifier = Modifier
                        .width(3.dp)
                        .fillMaxHeight()
                        .background(scheme.onSurfaceVariant.copy(alpha = 0.4f))
                )
                Row(
                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 9.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(7.dp)
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Outlined.Reply,
                        contentDescription = null,
                        tint = scheme.onSurfaceVariant,
                        modifier = Modifier.size(14.dp)
                    )
                    Text(
                        text = reply.postTitle.ifBlank { "a discussion" },
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = scheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }

            // The answer.
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(11.dp))
                Text(
                    text = body,
                    style = MaterialTheme.typography.bodyMedium,
                    color = scheme.onSurface,
                    maxLines = 5,
                    overflow = TextOverflow.Ellipsis
                )
            }

            Spacer(modifier = Modifier.height(12.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(13.dp)
            ) {
                MetaText(formatTimeAgo(reply.createdAt))
                MetaStat(Icons.Outlined.ThumbUp, reply.thumbsUpCount)
                if (reply.replyCount > 0) MetaStat(Icons.Outlined.ChatBubbleOutline, reply.replyCount)
                if (reply.attachments.isNotEmpty()) {
                    MetaStat(Icons.Outlined.AttachFile, reply.attachments.size)
                }
                if (reply.isEdited == true) MetaText("Edited")
            }
        }
    }
}

// --- shared meta line -------------------------------------------------------

@Composable
private fun MetaText(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.labelSmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        maxLines = 1
    )
}

@Composable
private fun MetaStat(icon: ImageVector, count: Int) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(13.dp)
        )
        Text(
            text = compactCount(count),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            maxLines = 1
        )
    }
}

// --- skeletons --------------------------------------------------------------

/** Placeholder for a post or resource card while the tab is loading. */
@Composable
fun ProfileCardSkeleton(modifier: Modifier = Modifier) {
    SkeletonCard(modifier = modifier) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            ShimmerCircle(size = 38.dp)
            Column(modifier = Modifier.weight(1f)) {
                ShimmerLine(widthFraction = 0.42f, height = 11.dp)
                Spacer(modifier = Modifier.height(6.dp))
                ShimmerLine(widthFraction = 0.28f, height = 9.dp)
            }
        }
        Spacer(modifier = Modifier.height(12.dp))
        ShimmerLine(widthFraction = 0.82f, height = 14.dp)
        Spacer(modifier = Modifier.height(8.dp))
        ShimmerLine(widthFraction = 0.96f, height = 10.dp)
        Spacer(modifier = Modifier.height(6.dp))
        ShimmerLine(widthFraction = 0.6f, height = 10.dp)
        Spacer(modifier = Modifier.height(12.dp))
        ShimmerLine(widthFraction = 0.4f, height = 24.dp, shape = RoundedCornerShape(12.dp))
    }
}

/** Placeholder for a reply card: a quote block, then the answer. */
@Composable
fun ProfileReplySkeleton(modifier: Modifier = Modifier) {
    SkeletonCard(modifier = modifier) {
        ShimmerLine(height = 32.dp, shape = RoundedCornerShape(10.dp))
        Spacer(modifier = Modifier.height(11.dp))
        ShimmerLine(widthFraction = 0.98f, height = 11.dp)
        Spacer(modifier = Modifier.height(6.dp))
        ShimmerLine(widthFraction = 0.72f, height = 11.dp)
        Spacer(modifier = Modifier.height(12.dp))
        ShimmerLine(widthFraction = 0.35f, height = 9.dp)
    }
}

@Composable
private fun SkeletonCard(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = WebPanelShape,
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
        ),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) { content() }
    }
}
