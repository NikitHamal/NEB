package com.neb.ians.ui.screens.news

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PushPin
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.ui.components.ShimmerCard
import com.neb.ians.ui.components.ShimmerLine
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.ui.screens.home.newsIcon
import com.neb.ians.util.TactileType

// ---------------------------------------------------------------------------
// The blog index, read as an index.
//
// The newest piece gets the full width and a headline; everything after it is
// a line of text with a thumbnail, separated by a rule rather than boxed in a
// card. Category, author and age sit on one grey line above the title so the
// eye can skip them and go straight to the words.
// ---------------------------------------------------------------------------

@Composable
fun NewsLeadStory(
    item: NewsAnnouncement,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .nebPressable(scale = 0.99f, tactile = TactileType.ButtonTap, onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 10.dp)
    ) {
        NewsCover(
            item = item,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 10f)
                .clip(RoundedCornerShape(20.dp))
        )
        Spacer(modifier = Modifier.height(14.dp))
        NewsKicker(item)
        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = item.title,
            style = MaterialTheme.typography.headlineSmall,
            color = MaterialTheme.colorScheme.onSurface,
            maxLines = 3,
            overflow = TextOverflow.Ellipsis
        )
        if (item.summary.isNotBlank()) {
            Spacer(modifier = Modifier.height(7.dp))
            Text(
                text = item.summary,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
fun NewsIndexRow(
    item: NewsAnnouncement,
    onClick: () -> Unit,
    showDivider: Boolean,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.99f, tactile = TactileType.ButtonTap, onClick = onClick)
                .padding(horizontal = 16.dp, vertical = 14.dp),
            horizontalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Column(modifier = Modifier.weight(1f)) {
                NewsKicker(item)
                Spacer(modifier = Modifier.height(5.dp))
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
                if (item.summary.isNotBlank()) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = item.summary,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            NewsCover(
                item = item,
                modifier = Modifier
                    .size(96.dp)
                    .clip(RoundedCornerShape(16.dp))
            )
        }
        if (showDivider) {
            HorizontalDivider(
                color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(horizontal = 16.dp)
            )
        }
    }
}

@Composable
private fun NewsCover(item: NewsAnnouncement, modifier: Modifier = Modifier) {
    val scheme = MaterialTheme.colorScheme
    if (item.coverImageUrl.isNotBlank()) {
        AsyncImage(
            model = item.coverImageUrl,
            contentDescription = item.title,
            modifier = modifier.background(scheme.surfaceContainerHigh),
            contentScale = ContentScale.Crop
        )
    } else {
        Box(
            modifier = modifier.background(scheme.surfaceContainerHigh),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = item.categoryIcon.newsIcon(),
                contentDescription = null,
                tint = scheme.onSurfaceVariant.copy(alpha = 0.45f),
                modifier = Modifier.size(26.dp)
            )
        }
    }
}

@Composable
private fun NewsKicker(item: NewsAnnouncement) {
    val scheme = MaterialTheme.colorScheme
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(5.dp)
    ) {
        if (item.isPinned) {
            Icon(
                imageVector = Icons.Filled.PushPin,
                contentDescription = "Pinned",
                tint = scheme.onSurface,
                modifier = Modifier.size(12.dp)
            )
        }
        Text(
            text = kickerLine(item),
            style = MaterialTheme.typography.labelSmall,
            color = scheme.onSurfaceVariant,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis
        )
    }
}

@Composable
fun NewsIndexSkeleton(lead: Boolean) {
    Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp)) {
        if (lead) {
            ShimmerCard(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                height = 200.dp
            )
            Spacer(modifier = Modifier.height(14.dp))
            ShimmerLine(widthFraction = 0.3f, height = 9.dp)
            Spacer(modifier = Modifier.height(9.dp))
            ShimmerLine(widthFraction = 0.9f, height = 20.dp)
            Spacer(modifier = Modifier.height(8.dp))
            ShimmerLine(widthFraction = 0.7f, height = 12.dp)
        } else {
            Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                Column(modifier = Modifier.weight(1f)) {
                    ShimmerLine(widthFraction = 0.32f, height = 9.dp)
                    Spacer(modifier = Modifier.height(8.dp))
                    ShimmerLine(widthFraction = 0.94f, height = 14.dp)
                    Spacer(modifier = Modifier.height(7.dp))
                    ShimmerLine(widthFraction = 0.6f, height = 11.dp)
                }
                ShimmerCard(
                    modifier = Modifier.size(96.dp),
                    shape = RoundedCornerShape(16.dp),
                    height = 96.dp
                )
            }
        }
    }
}

private fun kickerLine(item: NewsAnnouncement): String = listOf(
    item.categoryLabel,
    item.publishedAgo.ifBlank { "" },
    item.viewCount.ifBlank { "" }
).filter { it.isNotBlank() }.joinToString(" · ")
