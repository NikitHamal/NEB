package com.neb.ians.ui.screens.home

import com.neb.ians.ui.components.NebGlyphShapes
import com.neb.ians.ui.components.boundedWidth
import com.neb.ians.ui.components.nebShape
import androidx.compose.ui.graphics.SolidColor
import com.neb.ians.util.TactileType
import com.neb.ians.ui.components.nebPressable
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
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import com.neb.ians.ui.components.nebHorizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.FilterList
import androidx.compose.material.icons.filled.Whatshot
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.repository.PersonSuggestion
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.CompactPeerCard
import com.neb.ians.ui.components.KaTeXText
import com.neb.ians.ui.components.WebResourceCard

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
                shape = RoundedCornerShape(28.dp),
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
    val visible = remember(resources) { resources.take(8) }
    LazyRow(
        modifier = Modifier.boundedWidth(),
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(visible, key = { it.id }, contentType = { "resource_card" }) { resource ->
            WebResourceCard(
                resource = resource,
                onClick = { onResourceClick(resource.id) },
                minWidth = 248.dp,
                height = HomeRailCardHeight,
                shape = RoundedCornerShape(24.dp)
            )
        }
    }
}

@Composable
internal fun HomeNewResourcesRail(
    resources: List<ApiResource>,
    onViewAllClick: () -> Unit,
    onResourceClick: (String) -> Unit
) {
    if (resources.isEmpty()) return
    val visible = remember(resources) { resources.take(8) }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        HomeSectionTitle(
            title = "New in library",
            actionLabel = "See all",
            onActionClick = onViewAllClick
        )
        LazyRow(
            modifier = Modifier.boundedWidth(),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(visible, key = { "new_in_lib_" + it.id }, contentType = { "resource_card" }) { resource ->
                WebResourceCard(
                    resource = resource,
                    onClick = { onResourceClick(resource.id) },
                    minWidth = 248.dp,
                    height = HomeRailCardHeight,
                    shape = RoundedCornerShape(24.dp)
                )
            }
        }
    }
}

/**
 * Shared fixed height for every card in the home rails (suggested deck +
 * trending carousel). Pinning both resource and discussion cards to this exact
 * height keeps the whole rail perfectly aligned — no more mismatched bottoms.
 */
private val HomeRailCardHeight = 268.dp
private val LEADING_INDEX_REGEX = Regex("""^\d+[\.\)]\s*""")

@Composable
internal fun HomeFeedResourceHighlight(
    resource: ApiResource,
    onClick: () -> Unit
) {
    val color = MaterialTheme.colorScheme.onSurface
    val displaySubject = remember(resource.subject) {
        val raw = resource.subject.trim()
        when {
            raw.isBlank() -> "Study Resource"
            raw.contains(",") -> raw.split(",").first().replace(LEADING_INDEX_REGEX, "").trim()
            raw.length > 24 -> raw.take(24) + "…"
            else -> raw
        }
    }
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .clip(RoundedCornerShape(18.dp))
            .nebPressable(scale = 0.98f, tactile = TactileType.LightTap, onClick = onClick),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.16f))
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(46.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(color.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.MenuBook,
                    contentDescription = null,
                    tint = color,
                    modifier = Modifier.size(24.dp)
                )
            }
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(3.dp)
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    Surface(
                        shape = RoundedCornerShape(6.dp),
                        color = color.copy(alpha = 0.12f),
                        modifier = Modifier.widthIn(max = 160.dp)
                    ) {
                        Text(
                            text = displaySubject,
                            style = MaterialTheme.typography.labelSmall,
                            color = color,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp)
                        )
                    }
                    if (resource.gradeLevel.isNotBlank()) {
                        Text(
                            text = resource.gradeLevel,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
                KaTeXText(
                    text = resource.title,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 2
                )
                Text(
                    text = listOfNotNull(
                        resource.type.takeIf { it.isNotBlank() },
                        "Study Guide"
                    ).joinToString(", "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

@Composable
internal fun HomePostsFilterBar(
    currentSort: String,
    selectedCategory: String?,
    isRefreshing: Boolean,
    scrolled: Boolean,
    onSelectSort: (String) -> Unit,
    onOpenCategories: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surface)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                modifier = Modifier
                    .weight(1f)
                    .nebHorizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HomeSortPill("For you", "hot", Icons.Filled.Whatshot, currentSort, onSelectSort)
                HomeSortPill("New", "new", Icons.Outlined.Schedule, currentSort, onSelectSort)
                HomeSortPill("Top", "top", Icons.Outlined.ThumbUp, currentSort, onSelectSort)
                HomeSortPill("Discussed", "discussed", Icons.Outlined.ChatBubbleOutline, currentSort, onSelectSort)
            }
            val hasCategory = selectedCategory != null
            val chipShape = RoundedCornerShape(17.dp)
            Box(
                modifier = Modifier
                    .size(34.dp)
                    .clip(chipShape)
                    .background(
                        if (hasCategory) MaterialTheme.colorScheme.primaryContainer
                        else MaterialTheme.colorScheme.surfaceContainerLow
                    )
                    .then(
                        if (hasCategory) Modifier
                        else Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, chipShape)
                    )
                    .nebPressable(scale = 0.94f, tactile = TactileType.LightTap, onClick = onOpenCategories),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Filled.FilterList,
                    contentDescription = if (hasCategory) "Filtered by #$selectedCategory" else "Filter by topic",
                    modifier = Modifier.size(17.dp),
                    tint = if (hasCategory) MaterialTheme.colorScheme.onPrimaryContainer
                    else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(1.dp)
                .background(
                    if (isRefreshing) MaterialTheme.colorScheme.primary.copy(alpha = 0.45f)
                    else MaterialTheme.colorScheme.outlineVariant.copy(alpha = if (scrolled) 1f else 0.55f)
                )
        )
    }
}

@Composable
private fun HomeSortPill(
    label: String,
    value: String,
    icon: ImageVector,
    currentSort: String,
    onSelect: (String) -> Unit
) {
    val selected = currentSort == value
    val pillShape = RoundedCornerShape(28.dp)
    val bg = if (selected) MaterialTheme.colorScheme.secondaryContainer else Color.Transparent
    val fg = if (selected) MaterialTheme.colorScheme.onSecondaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
    Row(
        modifier = Modifier
            .height(34.dp)
            .clip(pillShape)
            .background(bg)
            .then(
                if (selected) Modifier
                else Modifier.border(1.dp, MaterialTheme.colorScheme.outlineVariant, pillShape)
            )
            .nebPressable(scale = 0.96f, tactile = TactileType.LightTap) { onSelect(value) }
            .padding(horizontal = 13.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(15.dp),
            tint = fg
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Medium,
            color = fg,
            maxLines = 1
        )
    }
}

@Composable
internal fun HomeEndOfFeedCard(
    onViewAllClick: () -> Unit,
    onCreatePostClick: () -> Unit,
    selectedCategory: String? = null,
    onClearFilters: () -> Unit = {}
) {
    val cardShape = RoundedCornerShape(28.dp)
    val pillShape = RoundedCornerShape(28.dp)
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 18.dp),
        shape = cardShape,
        color = MaterialTheme.colorScheme.surfaceContainerLow,
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 22.dp, vertical = 22.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(46.dp)
                    .background(MaterialTheme.colorScheme.primaryContainer, nebShape(NebGlyphShapes.Sunny)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Filled.Check,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onPrimaryContainer,
                    modifier = Modifier.size(22.dp)
                )
            }
            Text(
                text = "You're all caught up",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.onSurface
            )
            Text(
                text = if (selectedCategory != null) {
                    "You've seen all discussions in #$selectedCategory. Switch topics or browse study guides in the library."
                } else {
                    "Browse notes and past papers in the library, or ask a question to start a new discussion."
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
            Spacer(Modifier.height(2.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp, Alignment.CenterHorizontally),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    modifier = Modifier
                        .weight(1f)
                        .height(40.dp)
                        .clip(pillShape)
                        .background(MaterialTheme.colorScheme.secondaryContainer)
                        .nebPressable(
                            scale = 0.96f,
                            tactile = TactileType.LightTap,
                            onClick = if (selectedCategory != null) onClearFilters else onCreatePostClick
                        )
                        .padding(horizontal = 14.dp),
                    horizontalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterHorizontally),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = if (selectedCategory != null) Icons.Filled.FilterList else Icons.Filled.EditNote,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSecondaryContainer,
                        modifier = Modifier.size(17.dp)
                    )
                    Text(
                        text = if (selectedCategory != null) "All topics" else "Ask a question",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Row(
                    modifier = Modifier
                        .weight(1f)
                        .height(40.dp)
                        .clip(pillShape)
                        .background(MaterialTheme.colorScheme.primary)
                        .nebPressable(scale = 0.96f, tactile = TactileType.LightTap, onClick = onViewAllClick)
                        .padding(horizontal = 14.dp),
                    horizontalArrangement = Arrangement.spacedBy(6.dp, Alignment.CenterHorizontally),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.MenuBook,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onPrimary,
                        modifier = Modifier.size(17.dp)
                    )
                    Text(
                        text = "Browse library",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onPrimary,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}

@Composable
internal fun HomeSuggestedPeersRail(
    peers: List<PersonSuggestion>,
    onPeerClick: (String) -> Unit,
    onFollowClick: (String) -> Unit,
    onSeeAllClick: () -> Unit
) {
    if (peers.isEmpty()) return

    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        HomeSectionTitle(
            title = "People you may know",
            actionLabel = "See all",
            onActionClick = onSeeAllClick
        )
        LazyRow(
            modifier = Modifier.boundedWidth(),
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(peers, key = { it.id }) { person ->
                CompactPeerCard(
                    name = person.name,
                    authorId = person.id,
                    avatarUrl = person.photoUrl,
                    badge = person.reason.ifBlank { person.detail ?: "Contributor" },
                    isFollowing = person.isFollowing,
                    onPeerClick = { onPeerClick(person.username) },
                    onFollowToggle = { onFollowClick(person.id) },
                    followLabel = when {
                        person.isFollowing -> "Following"
                        person.followsYou -> "Follow back"
                        else -> "Follow"
                    }
                )
            }
        }
    }
}
