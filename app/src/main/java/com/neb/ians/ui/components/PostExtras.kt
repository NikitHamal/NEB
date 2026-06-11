package com.neb.ians.ui.components

import android.content.Context
import android.content.Intent
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Flag
import androidx.compose.material.icons.outlined.FormatBold
import androidx.compose.material.icons.outlined.FormatItalic
import androidx.compose.material.icons.outlined.FormatListBulleted
import androidx.compose.material.icons.outlined.FormatListNumbered
import androidx.compose.material.icons.outlined.FormatQuote
import androidx.compose.material.icons.outlined.HowToVote
import androidx.compose.material.icons.outlined.Lightbulb
import androidx.compose.material.icons.outlined.Functions
import androidx.compose.material.icons.outlined.Link
import androidx.compose.material.icons.outlined.Poll
import androidx.compose.material.icons.outlined.Quiz
import androidx.compose.material.icons.outlined.Share
import androidx.compose.material.icons.outlined.StrikethroughS
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.outlined.Title
import androidx.compose.material.icons.outlined.Unarchive
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
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
import androidx.compose.ui.layout.ContentScale
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
import com.neb.ians.data.api.ApiEditHistory
import com.neb.ians.data.api.ApiPoll
import com.neb.ians.data.api.ApiPollVoteResponse
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

// ---------------------------------------------------------------------------
// URL + share helpers
// ---------------------------------------------------------------------------

private const val WEB_BASE = "https://nebians.consica.com.np"

/** Resolve a possibly-relative media URL against the web origin (same as Avatar). */
fun resolveMediaUrl(url: String?): String? {
    if (url.isNullOrBlank()) return null
    return if (url.startsWith("http://") || url.startsWith("https://")) url
    else "$WEB_BASE${if (url.startsWith("/")) "" else "/"}$url"
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
// Poll UI model (local state, kept in ViewModels; updated after voting)
// ---------------------------------------------------------------------------

data class PollOptionUi(
    val id: String,
    val text: String,
    val correct: Boolean,
    val votes: Int
)

data class PollUi(
    val id: String,
    val question: String,
    val pollType: String,
    val allowMultiple: Boolean,
    val explanation: String,
    val totalVotes: Int,
    val isExpired: Boolean,
    val options: List<PollOptionUi>,
    val votedIds: Set<String>
) {
    val hasVoted: Boolean get() = votedIds.isNotEmpty()
    val isMcq: Boolean get() = pollType == "mcq"
}

fun ApiPoll.toPollUi(): PollUi = PollUi(
    id = id,
    question = question,
    pollType = pollType,
    allowMultiple = allowMultiple,
    explanation = explanation,
    totalVotes = totalVotes,
    isExpired = isExpired,
    options = options.sortedBy { it.order }.map { PollOptionUi(it.id, it.text, it.correct, it.votes) },
    votedIds = userVoteIds.toSet()
)

fun ApiPollVoteResponse.toPollUi(votedIds: Set<String>): PollUi = PollUi(
    id = id,
    question = question,
    pollType = pollType,
    allowMultiple = allowMultiple,
    explanation = explanation,
    totalVotes = totalVotes,
    isExpired = isExpired,
    options = options.sortedBy { it.order }.map { PollOptionUi(it.id, it.text, it.isCorrect, it.voteCount) },
    votedIds = votedIds
)

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
    val categoryTheme = getSubjectTheme(category)
    val preview = remember(post.content) { markdownToPlainPreview(post.content) }
    val bookmarked = post.isBookmarked == true

    NebCard(
        modifier = modifier.fillMaxWidth(),
        onClick = onClick,
        shape = WebPanelShape
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            // ----- Meta row: avatar + author + badge + "posted" + category · time -----
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Box(
                    modifier = Modifier.combinedClickable(
                        onClick = onAuthorClick,
                        onLongClick = onAuthorLongPress
                    )
                ) {
                    Avatar(name = post.authorName, imageUrl = post.authorPhotoUrl, size = 38.dp)
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
                                .combinedClickable(
                                    onClick = onAuthorClick,
                                    onLongClick = onAuthorLongPress
                                )
                        )
                        post.authorBadgeInfo?.let { badge ->
                            Spacer(modifier = Modifier.width(5.dp))
                            NebBadge(badge)
                        }
                        Text(
                            text = "  posted",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                    Spacer(modifier = Modifier.height(2.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(shape = WebPillShape, color = categoryTheme.container) {
                            Text(
                                text = category,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = categoryTheme.onContainer,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        Text(
                            text = " · ",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
                        )
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
            }

            Spacer(modifier = Modifier.height(10.dp))
            Text(
                text = post.title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
            if (preview.isNotBlank()) {
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = preview,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // ----- Images (max 3 thumbnails) -----
            if (post.images.isNotEmpty()) {
                Spacer(modifier = Modifier.height(10.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    post.images.sortedBy { it.order }.take(3).forEach { image ->
                        AsyncImage(
                            model = resolveMediaUrl(image.imageUrl),
                            contentDescription = null,
                            modifier = Modifier
                                .weight(1f)
                                .height(80.dp)
                                .clip(RoundedCornerShape(8.dp)),
                            contentScale = ContentScale.Crop
                        )
                    }
                }
            }

            // ----- Poll badge -----
            post.poll?.let { poll ->
                Spacer(modifier = Modifier.height(10.dp))
                PollBadge(isMcq = poll.pollType == "mcq")
            }

            Spacer(modifier = Modifier.height(12.dp))

            // ----- Action row -----
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                LikePill(
                    count = post.thumbsUpCount,
                    liked = post.isThumbedUp,
                    onClick = onLikeClick
                )
                Surface(
                    shape = WebPillShape,
                    color = Color.Transparent,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(5.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.ChatBubbleOutline,
                            contentDescription = null,
                            modifier = Modifier.size(15.dp),
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Text(
                            text = "${post.replyCount} Replies",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                    }
                }
                Spacer(modifier = Modifier.weight(1f))
                NebIconButton(
                    icon = if (bookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                    contentDescription = if (bookmarked) "Remove bookmark" else "Bookmark",
                    onClick = onBookmarkClick,
                    tint = if (bookmarked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    size = 34.dp
                )
                NebIconButton(
                    icon = Icons.Outlined.Share,
                    contentDescription = "Share",
                    onClick = onShareClick,
                    size = 34.dp
                )
                PostMoreMenu(
                    isOwn = isOwnPost,
                    isBookmarked = bookmarked,
                    isArchived = post.isArchived == true,
                    onBookmark = onBookmarkClick,
                    onShare = onShareClick,
                    onReport = onReportClick,
                    onEdit = onEditClick,
                    onArchive = onArchiveClick,
                    onDelete = onDeleteClick
                )
            }
        }
    }
}

/** Like pill matching web .post-action (ThumbUp + compact count). */
@Composable
fun LikePill(count: Int, liked: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .clip(WebPillShape)
            .border(
                1.dp,
                if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant,
                WebPillShape
            )
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        Icon(
            imageVector = if (liked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
            contentDescription = if (liked) "Remove like" else "Like",
            modifier = Modifier.size(15.dp),
            tint = if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = compactCount(count),
            style = MaterialTheme.typography.labelMedium,
            color = if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
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

/** Three-dot dropdown menu for posts/replies. */
@Composable
fun PostMoreMenu(
    isOwn: Boolean,
    isBookmarked: Boolean,
    isArchived: Boolean,
    onBookmark: () -> Unit,
    onShare: () -> Unit,
    onReport: () -> Unit,
    onEdit: () -> Unit,
    onArchive: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    Box(modifier = modifier) {
        NebIconButton(
            icon = Icons.Filled.MoreVert,
            contentDescription = "More options",
            onClick = { expanded = true },
            size = 34.dp
        )
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            DropdownMenuItem(
                text = { Text(if (isBookmarked) "Remove bookmark" else "Bookmark") },
                leadingIcon = {
                    Icon(
                        if (isBookmarked) Icons.Filled.Bookmark else Icons.Filled.BookmarkBorder,
                        contentDescription = null
                    )
                },
                onClick = { expanded = false; onBookmark() }
            )
            DropdownMenuItem(
                text = { Text("Share") },
                leadingIcon = { Icon(Icons.Outlined.Share, contentDescription = null) },
                onClick = { expanded = false; onShare() }
            )
            if (!isOwn) {
                DropdownMenuItem(
                    text = { Text("Report") },
                    leadingIcon = { Icon(Icons.Outlined.Flag, contentDescription = null) },
                    onClick = { expanded = false; onReport() }
                )
            }
            if (isOwn) {
                HorizontalDivider()
                DropdownMenuItem(
                    text = { Text("Edit") },
                    leadingIcon = { Icon(Icons.Outlined.Edit, contentDescription = null) },
                    onClick = { expanded = false; onEdit() }
                )
                DropdownMenuItem(
                    text = { Text(if (isArchived) "Unarchive" else "Archive") },
                    leadingIcon = {
                        Icon(
                            if (isArchived) Icons.Outlined.Unarchive else Icons.Outlined.Archive,
                            contentDescription = null
                        )
                    },
                    onClick = { expanded = false; onArchive() }
                )
                DropdownMenuItem(
                    text = { Text("Delete", color = MaterialTheme.colorScheme.error) },
                    leadingIcon = {
                        Icon(Icons.Outlined.Delete, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                    },
                    onClick = { expanded = false; onDelete() }
                )
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Poll view — replicates web .fp-poll
// ---------------------------------------------------------------------------

@Composable
fun PollView(
    poll: PollUi,
    isVoting: Boolean,
    onVote: (List<String>) -> Unit,
    modifier: Modifier = Modifier
) {
    val showResults = poll.hasVoted || poll.isExpired

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            // Header
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                Icon(
                    imageVector = if (poll.isMcq) Icons.Outlined.Quiz else Icons.Outlined.HowToVote,
                    contentDescription = null,
                    modifier = Modifier.size(17.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = if (poll.isMcq) "MCQ Quiz" else "Poll",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                if (poll.allowMultiple) {
                    Text(
                        text = "· Multiple choice",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            if (poll.question.isNotBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = poll.question,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            if (!showResults) {
                if (poll.allowMultiple) {
                    var selected by remember(poll.id) { mutableStateOf(setOf<String>()) }
                    poll.options.forEach { option ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 3.dp)
                                .clip(RoundedCornerShape(10.dp))
                                .border(
                                    1.dp,
                                    if (option.id in selected) MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.outlineVariant,
                                    RoundedCornerShape(10.dp)
                                )
                                .clickable(enabled = !isVoting) {
                                    selected = if (option.id in selected) selected - option.id else selected + option.id
                                }
                                .padding(horizontal = 10.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Checkbox(
                                checked = option.id in selected,
                                onCheckedChange = { checked ->
                                    selected = if (checked) selected + option.id else selected - option.id
                                },
                                enabled = !isVoting
                            )
                            Text(
                                text = option.text,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(
                        onClick = { onVote(selected.toList()) },
                        enabled = selected.isNotEmpty() && !isVoting,
                        shape = WebPillShape
                    ) {
                        if (isVoting) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp,
                                color = MaterialTheme.colorScheme.onPrimary
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                        }
                        Text("Vote")
                    }
                } else {
                    poll.options.forEach { option ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 3.dp)
                                .clip(RoundedCornerShape(10.dp))
                                .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(10.dp))
                                .clickable(enabled = !isVoting) { onVote(listOf(option.id)) }
                                .padding(horizontal = 14.dp, vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = option.text,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    }
                }
            } else {
                // Results view with animated fill bars
                poll.options.forEach { option ->
                    PollResultRow(poll = poll, option = option)
                }
                if (poll.isMcq && poll.explanation.isNotBlank()) {
                    Spacer(modifier = Modifier.height(10.dp))
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.surfaceContainerHigh
                    ) {
                        Row(
                            modifier = Modifier.padding(10.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Lightbulb,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.primary
                            )
                            Text(
                                text = poll.explanation,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "${poll.totalVotes} ${if (poll.totalVotes == 1) "vote" else "votes"}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                if (poll.isExpired) {
                    Text(
                        text = " · Poll ended",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun PollResultRow(poll: PollUi, option: PollOptionUi) {
    val total = poll.totalVotes.coerceAtLeast(1)
    val fraction = option.votes.toFloat() / total
    val animatedFraction by animateFloatAsState(
        targetValue = fraction,
        animationSpec = tween(durationMillis = 500),
        label = "pollFill"
    )
    val isUserChoice = option.id in poll.votedIds
    val showCorrect = poll.isMcq && poll.hasVoted

    val fillColor = when {
        showCorrect && option.correct -> Color(0xFF16A34A).copy(alpha = 0.18f)
        showCorrect && isUserChoice && !option.correct -> MaterialTheme.colorScheme.error.copy(alpha = 0.15f)
        else -> MaterialTheme.colorScheme.primary.copy(alpha = 0.14f)
    }
    val borderColor = when {
        showCorrect && option.correct -> Color(0xFF16A34A)
        showCorrect && isUserChoice && !option.correct -> MaterialTheme.colorScheme.error
        isUserChoice -> MaterialTheme.colorScheme.primary
        else -> MaterialTheme.colorScheme.outlineVariant
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 3.dp)
            .clip(RoundedCornerShape(10.dp))
            .border(1.dp, borderColor, RoundedCornerShape(10.dp))
            .heightIn(min = 44.dp)
    ) {
        // Fill bar
        Box(
            modifier = Modifier
                .matchParentSize()
                .padding(0.dp)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(animatedFraction)
                    .background(fillColor)
            )
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            if (showCorrect && option.correct) {
                Icon(
                    imageVector = Icons.Filled.CheckCircle,
                    contentDescription = "Correct",
                    modifier = Modifier.size(16.dp),
                    tint = Color(0xFF16A34A)
                )
            } else if (showCorrect && isUserChoice && !option.correct) {
                Icon(
                    imageVector = Icons.Filled.Cancel,
                    contentDescription = "Incorrect",
                    modifier = Modifier.size(16.dp),
                    tint = MaterialTheme.colorScheme.error
                )
            }
            Text(
                text = option.text,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface,
                fontWeight = if (isUserChoice) FontWeight.SemiBold else FontWeight.Normal,
                modifier = Modifier.weight(1f)
            )
            val pct = if (poll.totalVotes > 0) (option.votes * 100 / poll.totalVotes) else 0
            Text(
                text = "${option.votes} · $pct%",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
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

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Report content", fontWeight = FontWeight.Bold) },
        text = {
            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                REPORT_REASONS.forEach { (value, label) ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .clickable { reason = value }
                            .padding(vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(selected = reason == value, onClick = { reason = value })
                        Text(label, style = MaterialTheme.typography.bodyMedium)
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = description,
                    onValueChange = { if (it.length <= 2000) description = it },
                    label = { Text("Description (optional)") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 2,
                    maxLines = 4,
                    shape = RoundedCornerShape(12.dp)
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onSubmit(reason, description) },
                enabled = !isSubmitting,
                shape = WebPillShape
            ) {
                Text(if (isSubmitting) "Submitting..." else "Submit report")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

// ---------------------------------------------------------------------------
// Edit history dialog
// ---------------------------------------------------------------------------

data class EditHistoryState(
    val entries: List<ApiEditHistory> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class EditHistoryViewModel @Inject constructor(
    private val forumRepository: ForumRepository
) : ViewModel() {
    private val _state = MutableStateFlow(EditHistoryState())
    val state: StateFlow<EditHistoryState> = _state.asStateFlow()

    fun load(targetType: String, targetId: String) {
        _state.value = EditHistoryState(isLoading = true)
        viewModelScope.launch {
            forumRepository.getEditHistory(targetType, targetId)
                .onSuccess { _state.value = EditHistoryState(entries = it, isLoading = false) }
                .onFailure { _state.value = EditHistoryState(isLoading = false, error = "Couldn't load edit history") }
        }
    }
}

@Composable
fun EditHistoryDialog(
    targetType: String,
    targetId: String,
    onDismiss: () -> Unit,
    viewModel: EditHistoryViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()
    LaunchedEffect(targetType, targetId) { viewModel.load(targetType, targetId) }

    Dialog(onDismissRequest = onDismiss) {
        Surface(
            shape = WebPanelShape,
            color = MaterialTheme.colorScheme.surfaceContainerLowest,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(18.dp)) {
                Text(
                    text = "Edit history",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(10.dp))
                when {
                    state.isLoading -> Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(110.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator(modifier = Modifier.size(26.dp), strokeWidth = 3.dp)
                    }
                    state.error != null -> Text(
                        text = state.error ?: "",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    state.entries.isEmpty() -> Text(
                        text = "No edit history recorded.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    else -> LazyColumn(
                        modifier = Modifier.heightIn(max = 420.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(state.entries, key = { it.id }) { entry ->
                            Column {
                                Text(
                                    text = entry.field.replaceFirstChar { it.uppercase() },
                                    style = MaterialTheme.typography.labelLarge,
                                    fontWeight = FontWeight.Bold
                                )
                                Spacer(modifier = Modifier.height(3.dp))
                                if (entry.oldValue.isNotBlank()) {
                                    Text(
                                        text = entry.oldValue,
                                        style = MaterialTheme.typography.bodySmall.copy(textDecoration = TextDecoration.LineThrough),
                                        color = MaterialTheme.colorScheme.error,
                                        maxLines = 4,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                }
                                Text(
                                    text = entry.newValue,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.primary,
                                    maxLines = 4,
                                    overflow = TextOverflow.Ellipsis
                                )
                                Spacer(modifier = Modifier.height(3.dp))
                                Text(
                                    text = "${entry.editedByUsername} · ${formatTimeAgo(entry.editedAt)}",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                    TextButton(onClick = onDismiss) { Text("Close") }
                }
            }
        }
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

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(dialogTitle, fontWeight = FontWeight.Bold) },
        text = {
            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                if (initialTitle != null) {
                    OutlinedTextField(
                        value = title,
                        onValueChange = { if (it.length <= 200) title = it },
                        label = { Text("Title") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp)
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                }
                OutlinedTextField(
                    value = content,
                    onValueChange = { if (it.length <= 20_000) content = it },
                    label = { Text("Content") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 120.dp, max = 280.dp),
                    shape = RoundedCornerShape(12.dp)
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onSave(if (initialTitle != null) title else null, content) },
                enabled = content.isNotBlank() && (initialTitle == null || title.isNotBlank()) && !isSaving,
                shape = WebPillShape
            ) {
                Text(if (isSaving) "Saving..." else "Save")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

/** Confirmation dialog for destructive deletes. */
@Composable
fun ConfirmDeleteDialog(
    message: String,
    onDismiss: () -> Unit,
    onConfirm: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Delete?", fontWeight = FontWeight.Bold) },
        text = { Text(message) },
        confirmButton = {
            Button(
                onClick = onConfirm,
                shape = WebPillShape,
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.error,
                    contentColor = MaterialTheme.colorScheme.onError
                )
            ) { Text("Delete") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
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
        shadowElevation = 4.dp
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
                    Avatar(
                        name = user.displayName?.ifBlank { user.username } ?: user.username,
                        imageUrl = user.photoUrl,
                        size = 30.dp
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
 * Markdown formatting toolbar. Full mode: Bold, Italic, Code, Strikethrough,
 * H2, Bullet list, Numbered list, Quote, Link. Compact mode: Bold/Italic/Code.
 */
@Composable
fun MarkdownToolbar(
    value: TextFieldValue,
    onValueChange: (TextFieldValue) -> Unit,
    modifier: Modifier = Modifier,
    compact: Boolean = false
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        ToolbarButton(Icons.Outlined.FormatBold, "Bold") { onValueChange(insertMarkdown(value, "**", "**")) }
        ToolbarButton(Icons.Outlined.FormatItalic, "Italic") { onValueChange(insertMarkdown(value, "*", "*")) }
        ToolbarButton(Icons.Outlined.Code, "Code") { onValueChange(insertMarkdown(value, "`", "`")) }
        if (!compact) {
            ToolbarButton(Icons.Outlined.StrikethroughS, "Strikethrough") { onValueChange(insertMarkdown(value, "~~", "~~")) }
            ToolbarButton(Icons.Outlined.Title, "Heading") { onValueChange(insertMarkdown(value, "\n## ")) }
            ToolbarButton(Icons.Outlined.FormatListBulleted, "Bullet list") { onValueChange(insertMarkdown(value, "\n- ")) }
            ToolbarButton(Icons.Outlined.FormatListNumbered, "Numbered list") { onValueChange(insertMarkdown(value, "\n1. ")) }
            ToolbarButton(Icons.Outlined.FormatQuote, "Quote") { onValueChange(insertMarkdown(value, "\n> ")) }
            ToolbarButton(Icons.Outlined.Link, "Link") { onValueChange(insertMarkdown(value, "[text](", ")")) }
            ToolbarButton(Icons.Outlined.Functions, "Math formula") { onValueChange(insertMarkdown(value, "$$", "$$")) }
        }
    }
}

@Composable
private fun ToolbarButton(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    contentDescription: String,
    onClick: () -> Unit
) {
    IconButton(onClick = onClick, modifier = Modifier.size(34.dp)) {
        Icon(
            imageVector = icon,
            contentDescription = contentDescription,
            modifier = Modifier.size(19.dp),
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
