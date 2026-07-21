package com.neb.ians.ui.screens.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.filled.Upload
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.MusicNote
import androidx.compose.material.icons.outlined.Poll
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiSuggestedItem
import com.neb.ians.ui.components.ResourceArt
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.resolveMediaUrl
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo
import com.neb.ians.util.getSubjectColor

@Composable
internal fun HomeWelcomePanel(
    userName: String,
    onSearchClick: () -> Unit,
    onStudyLabClick: () -> Unit
) {
    val shape = RoundedCornerShape(30.dp)
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .shadow(10.dp, shape, ambientColor = Color.Black.copy(alpha = 0.05f), spotColor = Color.Black.copy(alpha = 0.08f))
            .clip(shape)
            .background(
                Brush.linearGradient(
                    listOf(
                        MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.88f),
                        MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.58f),
                        MaterialTheme.colorScheme.surfaceContainerLowest
                    )
                )
            )
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.42f), shape)
            .padding(20.dp)
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = "Ready to learn, ${userName.ifBlank { "Student" }}?",
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = "Find notes, continue studying, or get instant help without leaving NEBians.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
                    .clip(RoundedCornerShape(18.dp))
                    .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.78f))
                    .border(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f), RoundedCornerShape(18.dp))
                    .clickable(onClick = onSearchClick)
                    .padding(horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Filled.Search,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Text(
                    text = "Search notes, papers and discussions",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Icon(
                    imageVector = Icons.Filled.ArrowForward,
                    contentDescription = "Search",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(19.dp)
                )
            }

            Surface(
                onClick = onStudyLabClick,
                shape = RoundedCornerShape(16.dp),
                color = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 11.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(9.dp)
                ) {
                    Icon(Icons.AutoMirrored.Filled.MenuBook, contentDescription = null, modifier = Modifier.size(19.dp))
                    Text("Open Study Lab", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
internal fun HomeQuickActions(
    onStudyLabClick: () -> Unit,
    onNebyAiClick: () -> Unit,
    onForumClick: () -> Unit,
    onUploadClick: () -> Unit
) {
    val actions = listOf(
        HomeAction("Study Lab", "Create and revise", Icons.AutoMirrored.Filled.MenuBook, onStudyLabClick),
        HomeAction("Ask Neby", "Get guided help", Icons.Filled.SmartToy, onNebyAiClick),
        HomeAction("Forum", "Discuss with peers", Icons.Filled.Forum, onForumClick),
        HomeAction("Contribute", "Share a resource", Icons.Filled.Upload, onUploadClick)
    )

    Column(
        modifier = Modifier.padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            actions.take(2).forEach { action -> HomeActionCard(action, Modifier.weight(1f)) }
        }
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            actions.drop(2).forEach { action -> HomeActionCard(action, Modifier.weight(1f)) }
        }
    }
}

@Composable
private fun HomeActionCard(action: HomeAction, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(22.dp)
    Row(
        modifier = modifier
            .height(92.dp)
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.42f), shape)
            .clickable(onClick = action.onClick)
            .padding(14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(11.dp)
    ) {
        Box(
            modifier = Modifier
                .size(42.dp)
                .background(MaterialTheme.colorScheme.secondaryContainer, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = action.icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSecondaryContainer,
                modifier = Modifier.size(21.dp)
            )
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = action.title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(Modifier.height(3.dp))
            Text(
                text = action.subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
internal fun HomeSubjectStrip(
    subjects: List<String>,
    onSubjectClick: (String) -> Unit
) {
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(subjects, key = { it }) { subject ->
            val color = Color(getSubjectColor(subject))
            Row(
                modifier = Modifier
                    .clip(RoundedCornerShape(999.dp))
                    .background(color.copy(alpha = 0.11f))
                    .border(1.dp, color.copy(alpha = 0.28f), RoundedCornerShape(999.dp))
                    .clickable { onSubjectClick(subject) }
                    .padding(horizontal = 14.dp, vertical = 9.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(7.dp)
            ) {
                Box(Modifier.size(7.dp).background(color, CircleShape))
                Text(
                    text = subject,
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurface,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
    }
}

@Composable
internal fun HomeSectionTitle(
    title: String,
    subtitle: String? = null,
    actionLabel: String? = null,
    onActionClick: (() -> Unit)? = null
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.ExtraBold,
                color = MaterialTheme.colorScheme.onSurface
            )
            if (!subtitle.isNullOrBlank()) {
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        if (!actionLabel.isNullOrBlank() && onActionClick != null) {
            Surface(
                onClick = onActionClick,
                shape = RoundedCornerShape(999.dp),
                color = MaterialTheme.colorScheme.surfaceContainerHigh
            ) {
                Text(
                    text = actionLabel,
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(horizontal = 13.dp, vertical = 8.dp)
                )
            }
        }
    }
}

@Composable
internal fun HomeResourceCarousel(
    resources: List<ApiResource>,
    onResourceClick: (String) -> Unit
) {
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(resources.take(8), key = { it.id }) { resource ->
            WebResourceCard(
                resource = resource,
                onClick = { onResourceClick(resource.id) },
                minWidth = 248.dp,
                shape = RoundedCornerShape(24.dp)
            )
        }
    }
}

/**
 * "Suggested for you" — mixed deck of resource + discussion cards picked by
 * the server-side feed engine. Guaranteed non-empty while any content exists.
 * Discussion cards mirror the resource card's exact dimensions (110.dp media
 * area + identical content rows) so every card in the rail is the same height.
 */
@Composable
internal fun HomeSuggestedDeck(
    items: List<ApiSuggestedItem>,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    onLikeClick: (String) -> Unit = {}
) {
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(
            items.take(14),
            key = { item -> item.type + "_" + (item.post?.id ?: item.resource?.id ?: "") }
        ) { item ->
            when {
                item.type == "resource" && item.resource != null -> WebResourceCard(
                    resource = item.resource,
                    onClick = { onResourceClick(item.resource.id) },
                    minWidth = 248.dp,
                    shape = RoundedCornerShape(24.dp)
                )
                item.type == "post" && item.post != null -> SuggestedPostCard(
                    post = item.post,
                    onClick = { onPostClick(item.post.id) },
                    onLikeClick = { onLikeClick(item.post.id) }
                )
            }
        }
    }
}

/**
 * Full discussion card for the suggested rail: media cover (photo / video /
 * audio / poll / discussion art), floating like chip with liked/unliked state,
 * category pill, two-line title, author and reply·view stats — the same
 * building blocks and exact heights as [WebResourceCard].
 */
@Composable
private fun SuggestedPostCard(
    post: ApiPost,
    onClick: () -> Unit,
    onLikeClick: () -> Unit
) {
    val category = post.category.ifBlank { "General" }
    val categoryTheme = getSubjectTheme(category)
    val firstImage = remember(post.images) {
        post.images.minByOrNull { it.order }?.imageUrl?.let { resolveMediaUrl(it) }
    }
    val firstVideo = remember(post.attachments) { post.attachments.firstOrNull { it.kind == "video" } }
    val firstAudio = remember(post.attachments) { post.attachments.firstOrNull { it.kind == "audio" } }
    val hasPoll = post.poll != null
    val mediaLabel = when {
        firstVideo != null -> "VIDEO"
        firstAudio != null -> "AUDIO"
        hasPoll -> "POLL"
        post.images.size > 1 -> "${post.images.size} PHOTOS"
        else -> "POST"
    }
    val liked = post.isThumbedUp
    val shape = RoundedCornerShape(24.dp)

    Card(
        modifier = Modifier
            .width(248.dp)
            .clip(shape)
            .clickable(onClick = onClick),
        shape = shape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        // ----- Media cover (110.dp — same as WebResourceCard) -----
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(110.dp)
        ) {
            if (firstImage != null) {
                AsyncImage(
                    model = firstImage,
                    contentDescription = post.title,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            } else {
                ResourceArt(
                    primary = categoryTheme.color,
                    container = categoryTheme.container,
                    modifier = Modifier.fillMaxSize()
                )
            }

            // Center media affordance (mirror of the resource video overlay)
            val centerIcon = when {
                firstVideo != null -> Icons.Filled.PlayArrow
                firstAudio != null -> Icons.Outlined.MusicNote
                hasPoll -> Icons.Outlined.Poll
                else -> null
            }
            if (centerIcon != null) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = if (firstVideo != null) 0.22f else 0.08f)),
                    contentAlignment = Alignment.Center
                ) {
                    Surface(
                        shape = CircleShape,
                        color = Color.White.copy(alpha = 0.9f),
                        shadowElevation = 4.dp
                    ) {
                        Box(
                            modifier = Modifier.size(40.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = centerIcon,
                                contentDescription = null,
                                modifier = Modifier.size(if (firstVideo != null) 28.dp else 20.dp),
                                tint = Color.Black
                            )
                        }
                    }
                }
            }

            // Top-start media-type pill (mirrors the resource TYPE pill)
            Surface(
                modifier = Modifier
                    .align(Alignment.TopStart)
                    .padding(10.dp),
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest.copy(alpha = 0.92f)
            ) {
                Text(
                    text = mediaLabel,
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1
                )
            }

            // Top-end floating like chip with liked/unliked state
            Surface(
                onClick = onLikeClick,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(10.dp),
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.surfaceContainerLowest.copy(alpha = 0.92f)
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(
                        imageVector = if (liked) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                        contentDescription = if (liked) "Unlike" else "Like",
                        modifier = Modifier.size(13.dp),
                        tint = if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = compactCount(post.thumbsUpCount),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Bold,
                        color = if (liked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            // Bottom-end category disc (mirrors the resource subject disc)
            Surface(
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(10.dp)
                    .size(28.dp),
                shape = CircleShape,
                color = categoryTheme.color,
                shadowElevation = 2.dp
            ) {
                Box(
                    contentAlignment = Alignment.Center,
                    modifier = Modifier.fillMaxSize()
                ) {
                    Icon(
                        imageVector = Icons.Filled.Forum,
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = Color.White
                    )
                }
            }
        }

        // ----- Content rows (same heights/spacing as WebResourceCard) -----
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
        ) {
            Surface(
                shape = WebPillShape,
                color = categoryTheme.container
            ) {
                Text(
                    text = category.uppercase(),
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = categoryTheme.onContainer,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = post.title,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                minLines = 2,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = (if (post.isAnonymous) "Anonymous Nebian" else post.authorName) +
                    " · " + formatTimeAgo(post.createdAt),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(6.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.ChatBubbleOutline,
                    contentDescription = null,
                    modifier = Modifier.size(14.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "${post.replyCount} · ${compactCount(post.viewCount)} views",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1
                )
            }
        }
    }
}

@Immutable
private data class HomeAction(
    val title: String,
    val subtitle: String,
    val icon: ImageVector,
    val onClick: () -> Unit
)
