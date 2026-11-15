package com.neb.ians.ui.components

import android.content.Context
import android.content.Intent
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.material3.ripple
import androidx.compose.ui.graphics.graphicsLayer
import com.neb.ians.util.rememberTactileFeedback
import com.neb.ians.util.TactileType
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Cancel
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.outlined.Archive
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Code
import androidx.compose.material.icons.outlined.DataObject
import androidx.compose.material.icons.outlined.HorizontalRule
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.FormatBold
import androidx.compose.material.icons.outlined.FormatItalic
import androidx.compose.material.icons.outlined.FormatListBulleted
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.HowToVote
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.VisibilityOff
import androidx.compose.material.icons.outlined.Functions
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.Poll
import androidx.compose.material.icons.outlined.Insights
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.StrikethroughS
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material.icons.outlined.Title
import androidx.compose.material.icons.outlined.Unarchive
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import coil.compose.AsyncImage

import com.neb.ians.data.api.ApiPoll
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone

// ---------------------------------------------------------------------------
// URL + share helpers
// ---------------------------------------------------------------------------

private const val WEB_BASE = "https://nebians.consica.com.np"

fun resolveMediaUrl(url: String?): String? {
    if (url.isNullOrBlank()) return null
    return if (url.startsWith("http://") || url.startsWith("https://")) url
    else "$WEB_BASE${if (url.startsWith("/")) "" else "/"}$url"
}

fun isVideoMediaUrl(url: String?): String? {
    if (url.isNullOrBlank()) return null
    val clean = url.substringBefore("?").lowercase()
    return if (clean.endsWith(".mp4") || clean.endsWith(".webm") || clean.endsWith(".mov") || clean.endsWith(".m4v") || clean.endsWith(".mkv")) url else null
}

private val VideoUrlRegex = Regex("""https?://[^\s<"]+?\.(?:mp4|webm|mov|m4v|mkv)(?:\?[^\s<"]*)?""", RegexOption.IGNORE_CASE)

fun extractPostAttachments(post: ApiPost): List<com.neb.ians.data.api.ApiMediaAttachment> {
    val result = post.attachments.toMutableList()

    post.images.forEach { img ->
        if (isVideoMediaUrl(img.imageUrl) != null && result.none { it.url == img.imageUrl }) {
            result.add(
                com.neb.ians.data.api.ApiMediaAttachment(
                    id = img.id,
                    kind = "video",
                    url = img.imageUrl,
                    name = img.imageUrl.substringAfterLast("/"),
                    mimeType = "video/mp4",
                    sizeBytes = 0,
                    order = img.order
                )
            )
        }
    }

    VideoUrlRegex.findAll(post.content).forEach { match ->
        val vUrl = match.value
        if (result.none { it.url == vUrl }) {
            result.add(
                com.neb.ians.data.api.ApiMediaAttachment(
                    id = vUrl.hashCode().toString(),
                    kind = "video",
                    url = vUrl,
                    name = vUrl.substringAfterLast("/").substringBefore("?"),
                    mimeType = "video/mp4",
                    sizeBytes = 0,
                    order = 99
                )
            )
        }
    }

    return result
}

/** Share a forum post link via the system share sheet. */
fun sharePost(context: Context, postId: String) {
    try {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "$WEB_BASE/forum/post/$postId/")
        }
        context.startActivity(Intent.createChooser(intent, "Share post"))
    } catch (_: Exception) {
    }
}

/** Share arbitrary text via the system share sheet. */
fun shareText(context: Context, text: String) {
    try {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, text)
        }
        context.startActivity(Intent.createChooser(intent, "Share"))
    } catch (_: Exception) {
    }
}

// ---------------------------------------------------------------------------
// Forum post card — mirrors web .post-card
// ---------------------------------------------------------------------------

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ForumPostCard(
    post: ApiPost,
    isOwnPost: Boolean,
    onClick: () -> Unit,
    onLikeClick: () -> Unit,
    onBookmarkClick: () -> Unit,
    onShareClick: () -> Unit,
    onReportClick: () -> Unit,
    modifier: Modifier = Modifier,
    onEditClick: () -> Unit = {},
    onArchiveClick: () -> Unit = {},
    onDeleteClick: () -> Unit = {},
    onAuthorClick: () -> Unit = {},
    onAuthorLongPress: () -> Unit = {}
) {
    val category = post.category.ifBlank { "General" }
    // Card preview carries real markdown formatting (bold/italic/code,
    // colored links, highlighted mentions) instead of plain stripped text.
    val primary = MaterialTheme.colorScheme.primary
    val codeBg = MaterialTheme.colorScheme.surfaceContainerHigh
    val anonAccent = MaterialTheme.colorScheme.errorContainer
    val anonOnAccent = MaterialTheme.colorScheme.onErrorContainer
    val bodyColor = MaterialTheme.colorScheme.onSurfaceVariant
    val preview = remember(post.content) { markdownToInlinePreview(post.content) }
    val previewAnnotated = remember(preview, bodyColor, primary, codeBg, anonAccent, anonOnAccent) {
        buildInlineAnnotatedString(preview.clippedForCard(), bodyColor, primary, codeBg, anonAccent, anonOnAccent)
    }
    val bookmarked = post.isBookmarked == true
    var zoomImageUrlsList by remember { mutableStateOf<List<String>?>(null) }
    var zoomInitialIndex by remember { mutableStateOf(0) }

    // Flat feed row, like the web: white, no frame, one hairline under it.
    Column(modifier = modifier.fillMaxWidth()) {
    NebCard(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 8.dp, vertical = 4.dp),
        onClick = onClick,
        shape = RoundedCornerShape(20.dp),
        containerColor = MaterialTheme.colorScheme.surface,
        border = null
    ) {
        Column(modifier = Modifier.padding(start = 8.dp, end = 0.dp, top = 12.dp, bottom = 4.dp)) {
            // ----- Meta row: avatar + author + badge + "posted" + category and time -----
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Box(
                    modifier = if (post.isAnonymous) Modifier
                    else Modifier.combinedClickable(
                        onClick = onAuthorClick,
                        onLongClick = onAuthorLongPress
                    )
                ) {
                    val level = remember(post.authorBadgeInfo) {
                        if (post.authorBadgeInfo?.type == "verified") {
                            when (post.authorBadgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(name = post.authorName, imageUrl = post.authorPhotoUrl, size = 38.dp, verificationLevel = level)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = post.authorName,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier
                                .weight(1f, fill = false)
                                .then(
                                    if (post.isAnonymous) Modifier
                                    else Modifier.combinedClickable(
                                        onClick = onAuthorClick,
                                        onLongClick = onAuthorLongPress
                                    )
                                )
                        )
                        if (post.isAnonymous) {
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(
                                imageVector = Icons.Outlined.VisibilityOff,
                                contentDescription = "Anonymous",
                                tint = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.size(14.dp)
                            )
                        }
                        post.authorBadgeInfo?.let { badge ->
                            Spacer(modifier = Modifier.width(5.dp))
                            NebBadge(badge)
                        }
                    }
                    Spacer(modifier = Modifier.height(2.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = MaterialTheme.colorScheme.primaryContainer,
                            modifier = Modifier.weight(1f, fill = false)
                        ) {
                            Text(
                                text = "#$category",
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 3.dp),
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onPrimaryContainer,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = formatTimeAgo(post.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                }
                if (post.isArchived == true) {
                    Surface(
                        shape = WebPillShape,
                        color = MaterialTheme.colorScheme.surfaceContainerHigh
                    ) {
                        Text(
                            text = "Archived",
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
                PostMoreMenu(
                    isOwn = isOwnPost,
                    isBookmarked = bookmarked,
                    isArchived = post.isArchived == true,
                    onBookmark = onBookmarkClick,
                    onShare = onShareClick,
                    onReport = onReportClick,
                    onEdit = onEditClick,
                    onArchive = onArchiveClick,
                    onDelete = onDeleteClick,
                    onInsights = PostInsightsNav.open?.let { open -> { open(post.id) } }
                )
            }

            Spacer(modifier = Modifier.height(10.dp))
            KaTeXText(
                text = post.title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 3
            )
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = previewAnnotated,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // ----- Images (horizontal scrollable row for all post images up to 10) -----
            if (post.images.isNotEmpty()) {
                Spacer(modifier = Modifier.height(10.dp))
                val sortedImages = remember(post.images) { post.images.sortedBy { it.order } }
                val allResolvedUrls = remember(sortedImages) { sortedImages.mapNotNull { resolveMediaUrl(it.imageUrl) } }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .nebHorizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    sortedImages.forEachIndexed { index, image ->
                        Box(
                            modifier = Modifier
                                .size(120.dp, 86.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .clickable {
                                    zoomImageUrlsList = allResolvedUrls
                                    zoomInitialIndex = index
                                }
                        ) {
                            AsyncImage(
                                model = resolveMediaUrl(image.imageUrl),
                                contentDescription = "Image ${index + 1}",
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Crop
                            )
                        }
                    }
                }
            }

            zoomImageUrlsList?.let { urls ->
                ZoomableImageDialog(
                    imageUrls = urls,
                    initialIndex = zoomInitialIndex,
                    contentDescription = "Post image preview",
                    onDismiss = { zoomImageUrlsList = null }
                )
            }

            // ----- Poll badge -----
            post.poll?.let { poll ->
                Spacer(modifier = Modifier.height(10.dp))
                NebPollPreview(poll = remember(poll) { poll.toPollUi() })
            }

            // ----- Media attachment badges (video/audio/files) -----
            val allAttachments = remember(post.attachments, post.images, post.content) { extractPostAttachments(post) }
            if (allAttachments.isNotEmpty()) {
                Spacer(modifier = Modifier.height(10.dp))
                ForumMediaBadges(allAttachments)
            }

            Spacer(modifier = Modifier.height(12.dp))

            // ----- Action row: ghost buttons, like turns tonal -----
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(2.dp)
            ) {
                LikePill(
                    count = post.thumbsUpCount,
                    liked = post.isThumbedUp,
                    onClick = onLikeClick
                )
                PostStatButton(
                    icon = NebIcons.Comment,
                    label = compactCount(post.replyCount),
                    description = "Comments",
                    onClick = onClick
                )
                if (isOwnPost) {
                    PostStatButton(
                        icon = NebIcons.Eye,
                        label = compactCount(post.viewCount),
                        description = "Views",
                        onClick = null
                    )
                }
                Spacer(modifier = Modifier.weight(1f))
                NebIconButton(
                    icon = if (bookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                    contentDescription = if (bookmarked) "Remove bookmark" else "Bookmark",
                    onClick = onBookmarkClick,
                    tint = if (bookmarked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    size = 36.dp
                )
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .nebPressable(scale = 0.88f, onClick = onShareClick)
                        .semantics { contentDescription = "Share" },
                    contentAlignment = Alignment.Center
                ) {
                    NebIcon(NebIcons.Share, null, size = 18.dp, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
    NebHairline()
    }
}

/** Ghost stat button on a post card (icon + count), same height as [LikePill]. */
@Composable
fun PostStatButton(
    @androidx.annotation.DrawableRes icon: Int,
    label: String,
    description: String,
    onClick: (() -> Unit)?,
    modifier: Modifier = Modifier
) {
    val tone = MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = modifier
            .clip(WebPillShape)
            .then(
                if (onClick != null) Modifier.clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onClick
                ) else Modifier
            )
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .semantics { contentDescription = description },
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        NebIcon(id = icon, contentDescription = null, size = 18.dp, tint = tone)
        Text(text = label, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Medium, color = tone)
    }
}

/** Like pill: ghost, brand primary when liked (the web's `.liked`). No border, no ripple, spring motion. */
@Composable
fun LikePill(count: Int, liked: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val tactile = rememberTactileFeedback()
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.9f else 1.0f,
        animationSpec = com.neb.ians.ui.theme.nebFastSpatialSpec(),
        label = "likePillScale"
    )
    val iconScale by animateFloatAsState(
        targetValue = if (liked) 1.0f else 0.92f,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessMedium),
        label = "likePillIcon"
    )
    val background by animateColorAsState(
        targetValue = Color.Transparent,
        animationSpec = com.neb.ians.ui.theme.nebEffectsSpec(),
        label = "likePillBg"
    )
    val contentColor by animateColorAsState(
        targetValue = if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = com.neb.ians.ui.theme.nebEffectsSpec(),
        label = "likePillFg"
    )

    Row(
        modifier = modifier
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .clip(WebPillShape)
            .background(background)
            .clickable(
                interactionSource = interactionSource,
                indication = null,
                onClick = {
                    tactile.perform(if (liked) TactileType.LightTap else TactileType.Success)
                    onClick()
                }
            )
            .padding(horizontal = 12.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(
            imageVector = if (liked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
            contentDescription = if (liked) "Remove like" else "Like",
            modifier = Modifier
                .size(18.dp)
                .graphicsLayer { scaleX = iconScale; scaleY = iconScale },
            tint = contentColor
        )
        Text(
            text = compactCount(count),
            style = MaterialTheme.typography.labelLarge,
            fontWeight = if (liked) FontWeight.Bold else FontWeight.Medium,
            color = contentColor
        )
    }
}

/** Poll badge pill shown on post cards. */
@Composable
fun PollBadge(isMcq: Boolean, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        shape = WebPillShape,
        color = MaterialTheme.colorScheme.primaryContainer
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Icon(
                imageVector = if (isMcq) Icons.Outlined.Quiz else Icons.Outlined.Poll,
                contentDescription = null,
                modifier = Modifier.size(13.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Text(
                text = if (isMcq) "MCQ" else "Poll",
                style = MaterialTheme.typography.labelSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

/** Where "See insights" goes. Set by the navigation host; null means the menu hides the item. */
object PostInsightsNav {
    var open: ((String) -> Unit)? = null
}

/** Modern bottom sheet menu for posts/replies — like Instagram/Facebook. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PostMoreMenu(
    isOwn: Boolean,
    isBookmarked: Boolean,
    isArchived: Boolean,
    onBookmark: () -> Unit,
    onShare: (() -> Unit)? = null,
    onReport: () -> Unit,
    onEdit: () -> Unit,
    onArchive: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier,
    onInsights: (() -> Unit)? = null
) {
    var showSheet by remember { mutableStateOf(false) }
    Box(modifier = modifier) {
        NebIconButton(
            icon = Icons.Filled.MoreVert,
            contentDescription = "More options",
            onClick = { showSheet = true },
            size = 34.dp
        )
    }
    if (showSheet) {
        NebModalSheet(
            onDismiss = { showSheet = false }
        ) {
            Column(modifier = Modifier.padding(bottom = 8.dp)) {
                BottomSheetItem(
                    icon = if (isBookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                    label = if (isBookmarked) "Remove bookmark" else "Bookmark",
                    onClick = { showSheet = false; onBookmark() }
                )
                if (onShare != null) {
                    BottomSheetItem(
                        icon = Icons.Outlined.Share,
                        label = "Share",
                        onClick = { showSheet = false; onShare() }
                    )
                }
                if (!isOwn) {
                    BottomSheetItem(
                        icon = Icons.Outlined.Flag,
                        label = "Report",
                        onClick = { showSheet = false; onReport() }
                    )
                }
                if (isOwn) {
                    HorizontalDivider(
                        modifier = Modifier.padding(vertical = 4.dp, horizontal = 16.dp),
                        color = MaterialTheme.colorScheme.outlineVariant
                    )
                    if (onInsights != null) {
                        BottomSheetItem(
                            icon = Icons.Outlined.Insights,
                            label = "See insights",
                            onClick = { showSheet = false; onInsights() }
                        )
                    }
                    BottomSheetItem(
                        icon = Icons.Outlined.Edit,
                        label = "Edit",
                        onClick = { showSheet = false; onEdit() }
                    )
                    BottomSheetItem(
                        icon = if (isArchived) Icons.Outlined.Unarchive else Icons.Outlined.Archive,
                        label = if (isArchived) "Unarchive" else "Archive",
                        onClick = { showSheet = false; onArchive() }
                    )
                    BottomSheetItem(
                        icon = Icons.Outlined.Delete,
                        label = "Delete",
                        isDestructive = true,
                        onClick = { showSheet = false; onDelete() }
                    )
                }
            }
        }
    }
}

@Composable
private fun BottomSheetItem(
    icon: ImageVector,
    label: String,
    isDestructive: Boolean = false,
    onClick: () -> Unit
) {
    val tint = if (isDestructive) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.onSurface
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 24.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = tint,
            modifier = Modifier.size(22.dp)
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodyLarge,
            color = tint,
            fontWeight = FontWeight.Medium,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

// ---------------------------------------------------------------------------
// Report dialog
// ---------------------------------------------------------------------------

private val REPORT_REASONS = listOf(
    "spam" to "Spam",
    "abuse" to "Abuse or harassment",
    "inappropriate" to "Inappropriate content",
    "misinformation" to "Misinformation",
    "other" to "Other"
)

@Composable
fun ReportDialog(
    onDismiss: () -> Unit,
    onSubmit: (reason: String, description: String) -> Unit,
    isSubmitting: Boolean = false
) {
    var reason by rememberSaveable { mutableStateOf("spam") }
    var description by rememberSaveable { mutableStateOf("") }

    NebDialog(
        onDismissRequest = onDismiss,
        title = "Report content",
        supportingText = "Pick the closest reason. Moderators see every report.",
        icon = Icons.Outlined.Flag,
        confirm = NebDialogAction(
            label = if (isSubmitting) "Submitting…" else "Submit report",
            onClick = { onSubmit(reason, description) },
            enabled = !isSubmitting
        ),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        NebChipRow {
            REPORT_REASONS.forEach { (value, label) ->
                NebFilterChip(
                    label = label,
                    selected = reason == value,
                    onClick = { reason = value }
                )
            }
        }
        NebDialogTextField(
            value = description,
            onValueChange = { if (it.length <= 2000) description = it },
            label = "Description (optional)",
            singleLine = false,
            minLines = 2
        )
    }
}

// ---------------------------------------------------------------------------
// Edit dialogs (post: title + content / reply: content only)
// ---------------------------------------------------------------------------

@Composable
fun EditContentDialog(
    dialogTitle: String,
    initialTitle: String?,
    initialContent: String,
    onDismiss: () -> Unit,
    onSave: (title: String?, content: String) -> Unit,
    isSaving: Boolean = false
) {
    var title by rememberSaveable { mutableStateOf(initialTitle ?: "") }
    var content by rememberSaveable { mutableStateOf(initialContent) }

    NebDialog(
        onDismissRequest = onDismiss,
        title = dialogTitle,
        icon = Icons.Outlined.Edit,
        confirm = NebDialogAction(
            label = if (isSaving) "Saving…" else "Save",
            onClick = { onSave(if (initialTitle != null) title else null, content) },
            enabled = content.isNotBlank() && (initialTitle == null || title.isNotBlank()) && !isSaving
        ),
        dismiss = NebDialogAction("Cancel", onDismiss)
    ) {
        if (initialTitle != null) {
            NebDialogTextField(
                value = title,
                onValueChange = { if (it.length <= 200) title = it },
                label = "Title"
            )
        }
        NebDialogTextField(
            value = content,
            onValueChange = { if (it.length <= 20_000) content = it },
            label = "Content",
            singleLine = false,
            minLines = 4,
            modifier = Modifier.heightIn(min = 120.dp, max = 280.dp)
        )
    }
}

@Composable
fun ConfirmDeleteDialog(
    message: String,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    NebConfirmDialog(
        title = "Delete?",
        message = message,
        confirmLabel = "Delete",
        onConfirm = onConfirm,
        onDismiss = onDismiss,
        icon = Icons.Outlined.DeleteOutline,
        destructive = true
    )
}

// ---------------------------------------------------------------------------
// @mention autocomplete
// ---------------------------------------------------------------------------

/** Returns the partial @mention query at the cursor ("@ab|" -> "ab"), or null. */
fun mentionQueryAt(value: TextFieldValue): String? {
    val cursor = value.selection.start
    val text = value.text
    if (cursor <= 0 || cursor > text.length) return null
    var start = cursor
    while (start > 0 && !text[start - 1].isWhitespace()) start--
    val word = text.substring(start, cursor)
    if (!word.startsWith("@")) return null
    val query = word.drop(1)
    if (query.length < 2) return null
    if (!query.all { it.isLetterOrDigit() || it == '_' || it == '.' || it == '-' }) return null
    return query
}

/** Replaces the partial @mention at the cursor with "@username ". */
fun applyMention(value: TextFieldValue, username: String): TextFieldValue {
    val cursor = value.selection.start
    val text = value.text
    var start = cursor
    while (start > 0 && !text[start - 1].isWhitespace()) start--
    val newText = text.substring(0, start) + "@$username " + text.substring(cursor)
    val newCursor = start + username.length + 2
    return TextFieldValue(newText, TextRange(newCursor))
}

/** Dropdown card of @mention user suggestions (max 8 shown). */
@Composable
fun MentionSuggestions(
    users: List<ApiUserSearchResult>,
    onSelect: (ApiUserSearchResult) -> Unit,
    modifier: Modifier = Modifier
) {
    if (users.isEmpty()) return
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        shadowElevation = 0.dp
    ) {
        Column {
            users.take(8).forEach { user ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onSelect(user) }
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    val level = remember(user.badgeInfo) {
                        if (user.badgeInfo?.type == "verified") {
                            when (user.badgeInfo.color?.trim()?.lowercase()) {
                                "#1b9af0" -> 1
                                "#2e7d32" -> 2
                                "#f59e0b" -> 3
                                "#1a1a1a" -> 4
                                else -> 1
                            }
                        } else 0
                    }
                    Avatar(
                        name = user.displayName?.ifBlank { user.username } ?: user.username,
                        imageUrl = user.photoUrl,
                        size = 30.dp,
                        verificationLevel = level
                    )
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = user.displayName?.takeIf { it.isNotBlank() } ?: user.username,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        Text(
                            text = "@${user.username}",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Markdown toolbar
// ---------------------------------------------------------------------------

/** Wraps the selection (or inserts at the cursor) with markdown markers. */
fun insertMarkdown(value: TextFieldValue, prefix: String, suffix: String = ""): TextFieldValue {
    val start = value.selection.min
    val end = value.selection.max
    val text = value.text
    return if (start != end) {
        val selected = text.substring(start, end)
        val newText = text.substring(0, start) + prefix + selected + suffix + text.substring(end)
        TextFieldValue(newText, TextRange(start + prefix.length, start + prefix.length + selected.length))
    } else {
        val newText = text.substring(0, start) + prefix + suffix + text.substring(start)
        TextFieldValue(newText, TextRange(start + prefix.length))
    }
}

/**
 * Formatting toolbar for the composers. Each button changes the formatting of the text under the caret or selection;
 * nothing is typed into the field, so there is nothing to leak. Buttons light up where the caret is.
 */
@OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
@Composable
fun MarkdownToolbar(
    state: RichState,
    modifier: Modifier = Modifier,
    compact: Boolean = false
) {
    var linkDialog by remember { mutableStateOf(false) }
    var symbolDialog by remember { mutableStateOf(false) }
    // read so the buttons follow the caret and the text
    state.value
    state.armed
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ToolbarButton(NebIcons.Bold, "Bold", state.isActive(Fmt.BOLD)) { state.toggleInline(Fmt.BOLD) }
        ToolbarButton(NebIcons.Italic, "Italic", state.isActive(Fmt.ITALIC)) { state.toggleInline(Fmt.ITALIC) }
        ToolbarButton(NebIcons.Underline, "Underline", state.isActive(Fmt.UNDERLINE)) { state.toggleInline(Fmt.UNDERLINE) }
        ToolbarButton(NebIcons.Code, "Code", state.isActive(Fmt.CODE)) { state.toggleInline(Fmt.CODE) }
        if (!compact) {
            ToolbarButton(NebIcons.Strike, "Strikethrough", state.isActive(Fmt.STRIKE)) { state.toggleInline(Fmt.STRIKE) }
            ToolbarButton(NebIcons.Heading, "Heading", state.isLineActive(RLine.H2)) { state.toggleLine(RLine.H2) }
            ToolbarButton(NebIcons.ListBullet, "Bullet list", state.isLineActive(RLine.BULLET)) { state.toggleLine(RLine.BULLET) }
            ToolbarButton(NebIcons.ListNumber, "Numbered list", state.isLineActive(RLine.NUMBER)) { state.toggleLine(RLine.NUMBER) }
            ToolbarButton(NebIcons.Quote, "Quote", state.isLineActive(RLine.QUOTE)) { state.toggleLine(RLine.QUOTE) }
            ToolbarButton(NebIcons.Link, "Link", false) { linkDialog = true }
            ToolbarButton(NebIcons.Math, "Maths symbols", false) { symbolDialog = true }
            ToolbarButton(NebIcons.CodeBlock, "Code block", state.isLineActive(RLine.CODE)) { state.toggleLine(RLine.CODE) }
            ToolbarButton(NebIcons.Divider, "Divider", false) { state.insertDivider() }
        }
    }
    if (linkDialog) {
        var url by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { linkDialog = false },
            shape = RoundedCornerShape(28.dp),
            containerColor = com.neb.ians.ui.theme.nebFloatColor(),
            title = { Text("Add link") },
            text = {
                OutlinedTextField(
                    value = url, onValueChange = { url = it }, singleLine = true, shape = RoundedCornerShape(16.dp),
                    placeholder = { Text("Paste a link") }
                )
            },
            confirmButton = {
                TextButton(
                    onClick = { state.insertLink(url); linkDialog = false },
                    enabled = url.isNotBlank()
                ) { Text("Add") }
            },
            dismissButton = { TextButton(onClick = { linkDialog = false }) { Text("Cancel") } }
        )
    }
    if (symbolDialog) {
        AlertDialog(
            onDismissRequest = { symbolDialog = false },
            shape = RoundedCornerShape(28.dp),
            containerColor = com.neb.ians.ui.theme.nebFloatColor(),
            title = { Text("Symbols") },
            text = {
                androidx.compose.foundation.layout.FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    MathSymbols.forEach { sym ->
                        Box(
                            modifier = Modifier
                                .size(44.dp)
                                .clip(RoundedCornerShape(14.dp))
                                .background(MaterialTheme.colorScheme.secondaryContainer)
                                .clickable { state.insertSymbol(sym) },
                            contentAlignment = Alignment.Center
                        ) {
                            Text(sym, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSecondaryContainer)
                        }
                    }
                }
            },
            confirmButton = { TextButton(onClick = { symbolDialog = false }) { Text("Done") } }
        )
    }
}

/** Maths and science characters writers reach for; they are plain text, so they show everywhere. */
private val MathSymbols = listOf(
    "\u00B2", "\u00B3", "\u221A", "\u03C0", "\u00B1", "\u00D7", "\u00F7", "\u2260", "\u2264", "\u2265", "\u2248", "\u221E",
    "\u2192", "\u21CC", "\u00B0", "\u2234", "\u00BD", "\u00BC", "\u2211", "\u222B", "\u0394", "\u03B1", "\u03B2", "\u03B3",
    "\u03B8", "\u03BB", "\u03BC", "\u03C3", "\u03C6", "\u03C9", "\u03A9", "\u2082", "\u2083", "\u207F", "\u2208", "\u2229", "\u222A"
)

@Composable
private fun ToolbarButton(
    @androidx.annotation.DrawableRes icon: Int,
    contentDescription: String,
    active: Boolean = false,
    onClick: () -> Unit
) {
    // A tonal rounded square that springs under the thumb and ticks; never a bare ripple.
    Box(
        modifier = Modifier
            .size(36.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(if (active) MaterialTheme.colorScheme.primaryContainer else androidx.compose.ui.graphics.Color.Transparent)
            .nebPressable(scale = 0.88f, tactile = TactileType.LightTap, onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        NebIcon(
            id = icon,
            contentDescription = contentDescription,
            size = 19.dp,
            tint = if (active) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
