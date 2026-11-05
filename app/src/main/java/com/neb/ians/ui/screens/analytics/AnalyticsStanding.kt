package com.neb.ians.ui.screens.analytics

import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Check
import androidx.compose.material.icons.outlined.EmojiEvents
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiAnalyticsHelpfulness
import com.neb.ians.data.api.ApiAnalyticsLibrary
import com.neb.ians.data.api.ApiAnalyticsMilestone
import com.neb.ians.data.api.ApiAnalyticsPost
import com.neb.ians.data.api.ApiAnalyticsReach
import com.neb.ians.data.api.ApiAnalyticsResource
import com.neb.ians.data.api.ApiAnalyticsStats
import com.neb.ians.data.api.ApiAnalyticsTopic
import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.NebHairline
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.nebPressable

/** Lifetime reach of the member's posts and resources, plus readers in the range. */
@Composable
internal fun ReachCard(reach: ApiAnalyticsReach, days: Int, modifier: Modifier = Modifier) {
    if (reach.views == 0 && reach.likes == 0 && reach.uniqueReaders == 0) return
    val change = if (reach.readersPrevious > 0) {
        Math.round((reach.uniqueReaders - reach.readersPrevious) * 100f / reach.readersPrevious)
    } else null
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SectionTitle("Reach")
            StatGrid(
                listOf(
                    compactCount(reach.views) to "Total views",
                    compactCount(reach.likes) to "Likes received",
                    "${"%.1f".format(reach.engagementRate)}%" to "Engagement",
                    compactCount(reach.avgViewsPerPost) to "Views per post",
                    compactCount(reach.avgViewsPerResource) to "Views per resource",
                    compactCount(reach.resourceComments) to "Resource comments"
                )
            )
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                Text(
                    text = "${compactCount(reach.uniqueReaders)} members read your posts, last $days days",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.weight(1f)
                )
                DeltaTag(change)
            }
        }
    }
}

/** Reply kinds written and the labels they earned. Labels are tonal tags, like on the web. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
internal fun HelpfulnessCard(h: ApiAnalyticsHelpfulness, stats: ApiAnalyticsStats, modifier: Modifier = Modifier) {
    if (stats.posts == 0 && stats.replies == 0) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SectionTitle("Helpfulness")
            StatGrid(
                listOf(
                    compactCount(stats.replies) to "Replies written",
                    compactCount(h.answersWritten) to "Answers and solutions",
                    compactCount(h.goodLabels) to "Marked helpful or correct",
                    compactCount(h.solvedPosts) to "Your posts solved"
                )
            )
            if (h.labels.isNotEmpty() || h.kinds.isNotEmpty()) {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    h.labels.forEach { item ->
                        val (fill, ink) = when (item.key) {
                            "accepted", "correct", "helpful" -> cs.primaryContainer to cs.onPrimaryContainer
                            "partial" -> cs.tertiaryContainer to cs.onTertiaryContainer
                            else -> cs.errorContainer to cs.onErrorContainer
                        }
                        TonalTag("${labelName(item.key)} ${item.count}", container = fill, content = ink)
                    }
                    h.kinds.forEach { item ->
                        TonalTag("${labelName(item.key)} ${item.count}")
                    }
                }
            }
        }
    }
}

/** Followers, following, likes given and everything saved. */
@Composable
internal fun CommunityCard(stats: ApiAnalyticsStats, library: ApiAnalyticsLibrary, modifier: Modifier = Modifier) {
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SectionTitle("Community")
            StatGrid(
                listOf(
                    compactCount(stats.followers) to "Followers",
                    compactCount(stats.following) to "Following",
                    compactCount(library.likesGiven) to "Likes given",
                    compactCount(library.saved.posts + library.saved.replies + library.saved.resources) to "Saved items"
                )
            )
        }
    }
}

private fun metaLine(vararg parts: Pair<Int, String>): String =
    parts.joinToString("  |  ") { (n, noun) -> "${compactCount(n)} $noun" }

/** The five posts with the most views. Tapping one opens it. */
@Composable
internal fun TopPostsCard(posts: List<ApiAnalyticsPost>, onOpen: (String) -> Unit, modifier: Modifier = Modifier) {
    if (posts.isEmpty()) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier, contentPadding = 0) {
        Column {
            SectionTitle("Top posts", Modifier.padding(start = 20.dp, end = 20.dp, top = 20.dp, bottom = 8.dp))
            posts.forEachIndexed { i, post ->
                if (i > 0) NebHairline(Modifier.padding(horizontal = 20.dp))
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clickable { onOpen(post.id) }
                        .padding(horizontal = 20.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (post.category.isNotBlank()) {
                        TonalTag("#${post.category}", container = cs.primaryContainer, content = cs.onPrimaryContainer)
                    }
                    Text(
                        post.title.ifBlank { "Untitled post" },
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = FontWeight.Medium,
                        color = cs.onSurface,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        metaLine(post.viewCount to "views", post.likeCount to "likes", post.replyCount to "replies"),
                        style = MaterialTheme.typography.labelMedium,
                        color = cs.onSurfaceVariant
                    )
                }
            }
            Box(Modifier.height(8.dp))
        }
    }
}

/** The five resources with the most views. Tapping one opens it. */
@Composable
internal fun TopResourcesCard(items: List<ApiAnalyticsResource>, onOpen: (String) -> Unit, modifier: Modifier = Modifier) {
    if (items.isEmpty()) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier, contentPadding = 0) {
        Column {
            SectionTitle("Top resources", Modifier.padding(start = 20.dp, end = 20.dp, top = 20.dp, bottom = 8.dp))
            items.forEachIndexed { i, item ->
                if (i > 0) NebHairline(Modifier.padding(horizontal = 20.dp))
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clickable { onOpen(item.id) }
                        .padding(horizontal = 20.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        if (item.type.isNotBlank()) TonalTag(item.type)
                        val subject = item.subject.substringBefore(',').trim()
                        if (subject.isNotBlank()) {
                            TonalTag(subject, container = cs.tertiaryContainer, content = cs.onTertiaryContainer, modifier = Modifier.weight(1f, fill = false))
                        }
                    }
                    Text(
                        item.title.ifBlank { "Untitled resource" },
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = FontWeight.Medium,
                        color = cs.onSurface,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        metaLine(item.viewCount to "views", item.likeCount to "likes", item.commentCount to "comments"),
                        style = MaterialTheme.typography.labelMedium,
                        color = cs.onSurfaceVariant
                    )
                }
            }
            Box(Modifier.height(8.dp))
        }
    }
}

/** Where the member writes (post categories) and shares (resource subjects). */
@Composable
internal fun TopicsCard(categories: List<ApiAnalyticsTopic>, subjects: List<ApiAnalyticsTopic>, modifier: Modifier = Modifier) {
    if (categories.isEmpty() && subjects.isEmpty()) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
            if (categories.isNotEmpty()) {
                SectionTitle("Post topics")
                categories.forEach { BarRow(it.label.ifBlank { "General" }, it.count, it.width / 100f) }
            }
            if (subjects.isNotEmpty()) {
                if (categories.isNotEmpty()) Box(Modifier.height(4.dp))
                SectionTitle("Resource subjects")
                subjects.forEach { BarRow(it.label, it.count, it.width / 100f) }
            }
        }
    }
}

/** Goals with progress; finished ones turn to a tonal check. */
@Composable
internal fun MilestonesCard(items: List<ApiAnalyticsMilestone>, modifier: Modifier = Modifier) {
    if (items.isEmpty()) return
    val cs = MaterialTheme.colorScheme
    AnalyticsCard(modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
            SectionTitle(
                "Milestones",
                trailing = { TonalTag("${items.count { it.done }} of ${items.size}", icon = Icons.Outlined.EmojiEvents) }
            )
            items.forEach { m ->
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) {
                    if (m.done) {
                        GlyphTile(Icons.Outlined.Check, size = 36, polygon = NebGlyphShapes.Cookie, container = cs.primary, tint = cs.onPrimary)
                    } else {
                        Box(
                            Modifier
                                .size(36.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(cs.surfaceContainerHighest),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                "${(m.progress * 100 / m.target.coerceAtLeast(1))}%",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.SemiBold,
                                color = cs.onSurfaceVariant
                            )
                        }
                    }
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text(
                                m.title,
                                style = MaterialTheme.typography.bodyMedium,
                                fontWeight = if (m.done) FontWeight.Medium else FontWeight.Normal,
                                color = cs.onSurface,
                                modifier = Modifier.weight(1f)
                            )
                            Text(
                                "${compactCount(m.progress)}/${compactCount(m.target)}",
                                style = MaterialTheme.typography.labelMedium,
                                color = cs.onSurfaceVariant
                            )
                        }
                        Box(
                            Modifier
                                .fillMaxWidth()
                                .height(6.dp)
                                .clip(WebPillShape)
                                .background(cs.surfaceContainerHighest)
                        ) {
                            Box(
                                Modifier
                                    .fillMaxWidth((m.progress.toFloat() / m.target.coerceAtLeast(1)).coerceIn(if (m.progress > 0) 0.04f else 0f, 1f))
                                    .height(6.dp)
                                    .clip(WebPillShape)
                                    .background(cs.primary)
                            )
                        }
                    }
                }
            }
        }
    }
}
