package com.neb.ians.ui.screens.profile

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.outlined.AttachFile
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.Lock
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiReply
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.buildInlineAnnotatedString
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.fileSizeLabel
import com.neb.ians.ui.components.markdownToInlinePreview
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.util.TactileType
import com.neb.ians.util.formatTimeAgo

// ---------------------------------------------------------------------------
// The rows of the profile's three feeds.
//
// These used to be three different kinds of card: posts borrowed the coloured
// subject-themed feed card, replies sat in their own bordered surface, and
// resources borrowed the library card. Stacked in one list they read as three
// unrelated screens. They are rows now — hairline-separated, one indent, no
// colour — so the tabs differ by what they say, not by how loudly they say it.
// ---------------------------------------------------------------------------

private val RowIndent = 20.dp

@Composable
fun ProfilePostRow(
    post: ApiPost,
    onClick: () -> Unit,
    showDivider: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val preview = remember(post.content) { plainTextPreview(markdownToInlinePreview(post.content)) }
    val thumbnail = post.images.firstOrNull()?.imageUrl

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.985f, tactile = TactileType.ButtonTap, onClick = onClick)
                .padding(horizontal = RowIndent, vertical = 14.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = post.category.uppercase(),
                    style = MaterialTheme.typography.labelSmall,
                    color = scheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(3.dp))
                Text(
                    text = post.title,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    color = scheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                if (preview.isNotBlank()) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = preview,
                        style = MaterialTheme.typography.bodySmall,
                        color = scheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(9.dp))
                MetaRow {
                    MetaText(formatTimeAgo(post.createdAt))
                    MetaStat(Icons.Outlined.ThumbUp, post.thumbsUpCount)
                    MetaStat(Icons.Outlined.ChatBubbleOutline, post.replyCount)
                    if (post.viewCount > 0) MetaStat(Icons.Outlined.Visibility, post.viewCount)
                    if (post.poll != null) MetaText("Poll")
                }
            }

            if (thumbnail != null) {
                AsyncImage(
                    model = thumbnail,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(64.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(scheme.surfaceContainerHigh)
                )
            }
        }

        if (showDivider) {
            HorizontalDivider(
                color = scheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(start = RowIndent)
            )
        }
    }
}

/**
 * A reply, shown the way a reply actually reads: the thing being answered
 * first and quiet, the answer itself second and loud.
 *
 * The old card put "Reply on {post title}" in bold at the top and the reply
 * body underneath in grey, which inverted the two — you had to read past the
 * heading to find out what the person had said. A hairline spine now runs
 * down the left, tying the context line to the reply the way a thread does.
 */
@Composable
fun ProfileReplyRow(
    reply: ApiReply,
    onClick: () -> Unit,
    showDivider: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val preview = remember(reply.content) { markdownToInlinePreview(reply.content) }
    val body = remember(preview, scheme.onSurface) {
        buildInlineAnnotatedString(
            text = preview,
            baseColor = scheme.onSurface,
            primary = scheme.onSurface,
            codeBg = scheme.surfaceContainerHigh
        )
    }
    val context = remember(reply.postTitle, scheme.onSurfaceVariant, scheme.onSurface) {
        buildAnnotatedString {
            withStyle(SpanStyle(color = scheme.onSurfaceVariant)) { append("Replied to ") }
            withStyle(SpanStyle(color = scheme.onSurface, fontWeight = FontWeight.SemiBold)) {
                append(reply.postTitle.ifBlank { "a post" })
            }
        }
    }

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.985f, tactile = TactileType.ButtonTap, onClick = onClick)
                .height(IntrinsicSize.Min)
                .padding(horizontal = RowIndent, vertical = 14.dp)
        ) {
            // The spine: a glyph where the thread starts, then a hairline down
            // the full height of whatever the reply turned out to be.
            Column(
                modifier = Modifier
                    .width(18.dp)
                    .fillMaxHeight(),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Outlined.Reply,
                    contentDescription = null,
                    tint = scheme.onSurfaceVariant,
                    modifier = Modifier.size(15.dp)
                )
                Spacer(modifier = Modifier.height(5.dp))
                Box(
                    modifier = Modifier
                        .width(1.dp)
                        .weight(1f)
                        .background(scheme.outlineVariant.copy(alpha = 0.7f))
                )
            }

            Spacer(modifier = Modifier.width(12.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = context,
                    style = MaterialTheme.typography.bodySmall,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = body,
                    style = MaterialTheme.typography.bodyMedium,
                    color = scheme.onSurface,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(9.dp))
                MetaRow {
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

        if (showDivider) {
            HorizontalDivider(
                color = scheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(start = RowIndent + 30.dp)
            )
        }
    }
}

@Composable
fun ProfileResourceRow(
    resource: ApiResource,
    onClick: () -> Unit,
    showDivider: Boolean,
    modifier: Modifier = Modifier
) {
    val scheme = MaterialTheme.colorScheme
    val subtitle = remember(resource) {
        listOf(resource.subject, resource.gradeLevel, resource.type.uppercase())
            .filter { it.isNotBlank() }
            .joinToString(" · ")
    }

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.985f, tactile = TactileType.ButtonTap, onClick = onClick)
                .padding(horizontal = RowIndent, vertical = 14.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(13.dp))
                    .background(scheme.surfaceContainerHigh),
                contentAlignment = Alignment.Center
            ) {
                if (resource.thumbnailUrl.isNotBlank()) {
                    AsyncImage(
                        model = resource.thumbnailUrl,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Icon(
                        imageVector = resourceGlyph(resource.type),
                        contentDescription = null,
                        tint = scheme.onSurfaceVariant,
                        modifier = Modifier.size(19.dp)
                    )
                }
            }

            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = resource.title,
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = scheme.onSurface,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    if (resource.isPaid && !resource.hasAccess) {
                        Spacer(modifier = Modifier.width(6.dp))
                        Icon(
                            imageVector = Icons.Outlined.Lock,
                            contentDescription = "Locked",
                            tint = scheme.onSurfaceVariant,
                            modifier = Modifier.size(13.dp)
                        )
                    }
                }
                if (subtitle.isNotBlank()) {
                    Spacer(modifier = Modifier.height(3.dp))
                    Text(
                        text = subtitle,
                        style = MaterialTheme.typography.bodySmall,
                        color = scheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                MetaRow {
                    if (resource.addedAt > 0) MetaText(formatTimeAgo(resource.addedAt))
                    if (resource.fileSize > 0) MetaText(fileSizeLabel(resource.fileSize))
                    if (resource.viewCount > 0) MetaStat(Icons.Outlined.Visibility, resource.viewCount)
                    if (resource.likeCount > 0) MetaStat(Icons.Outlined.ThumbUp, resource.likeCount)
                    if (resource.isPaid && resource.price.isNotBlank()) {
                        MetaText("Rs. ${resource.price}")
                    }
                    val pending = resource.approvalStatus == "pending"
                    if (pending) MetaText("Pending review")
                }
            }
        }

        if (showDivider) {
            HorizontalDivider(
                color = scheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(start = RowIndent + 56.dp)
            )
        }
    }
}

// --- shared meta line -------------------------------------------------------

@Composable
private fun MetaRow(content: @Composable () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(13.dp)
    ) { content() }
}

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

private fun resourceGlyph(type: String): ImageVector = when (type.lowercase()) {
    "video" -> Icons.Outlined.PlayCircleOutline
    "question", "questions", "mcq", "quiz" -> Icons.Outlined.Quiz
    "book", "textbook", "guide" -> Icons.Outlined.MenuBook
    "image", "photo" -> Icons.Outlined.Image
    else -> Icons.Outlined.Description
}

// --- skeletons --------------------------------------------------------------

/** Placeholder for a post or resource row while the tab is loading. */
@Composable
fun ProfileRowSkeleton(leading: Boolean = false, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = RowIndent, vertical = 14.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        if (leading) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(13.dp))
            ) { ShimmerLine(height = 44.dp, shape = RoundedCornerShape(13.dp)) }
        }
        Column(modifier = Modifier.weight(1f)) {
            ShimmerLine(widthFraction = 0.26f, height = 9.dp)
            Spacer(modifier = Modifier.height(8.dp))
            ShimmerLine(widthFraction = 0.8f, height = 13.dp)
            Spacer(modifier = Modifier.height(7.dp))
            ShimmerLine(widthFraction = 0.95f, height = 10.dp)
            Spacer(modifier = Modifier.height(9.dp))
            ShimmerLine(widthFraction = 0.4f, height = 9.dp)
        }
    }
}

/** Placeholder for a reply row: narrower spine column, taller body. */
@Composable
fun ProfileReplySkeleton(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = RowIndent, vertical = 14.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(modifier = Modifier.width(18.dp)) {
            ShimmerLine(height = 15.dp, shape = CircleShape)
        }
        Column(modifier = Modifier.weight(1f)) {
            ShimmerLine(widthFraction = 0.55f, height = 10.dp)
            Spacer(modifier = Modifier.height(9.dp))
            ShimmerLine(widthFraction = 0.98f, height = 11.dp)
            Spacer(modifier = Modifier.height(6.dp))
            ShimmerLine(widthFraction = 0.72f, height = 11.dp)
            Spacer(modifier = Modifier.height(9.dp))
            ShimmerLine(widthFraction = 0.35f, height = 9.dp)
        }
    }
}
