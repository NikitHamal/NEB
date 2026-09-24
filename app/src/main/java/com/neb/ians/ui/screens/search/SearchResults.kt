@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.search

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowForward
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.NebBadge
import com.neb.ians.ui.components.WebPostCard
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.nebPressable

private const val PREVIEW_PER_SECTION = 3

/**
 * The result list for whichever scope is active.
 *
 * "All" is a preview of each kind with a way into the rest, so the first screen
 * of results answers what the query found before it asks the user to choose a
 * scope. The three narrow scopes are plain lists of the cards those results
 * already have elsewhere in the app, so a resource looks the same here as it
 * does in the library.
 */
@Composable
fun SearchResultsList(
    state: SearchUiState,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit,
    onScopeChange: (SearchScope) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(top = 4.dp, bottom = 28.dp),
        verticalArrangement = Arrangement.spacedBy(2.dp)
    ) {
        when (state.scope) {
            SearchScope.All -> {
                if (state.resources.isNotEmpty()) {
                    item(key = "h_resources") {
                        SearchSectionHeader(
                            title = "Resources",
                            count = state.resources.size,
                            onSeeAll = if (state.resources.size > PREVIEW_PER_SECTION) {
                                { onScopeChange(SearchScope.Resources) }
                            } else null
                        )
                    }
                    items(state.resources.take(PREVIEW_PER_SECTION), key = { "r_${it.id}" }) { resource ->
                        WebResourceCard(
                            resource = resource,
                            onClick = { onResourceClick(resource.id) },
                            minWidth = null,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)
                        )
                    }
                }
                if (state.posts.isNotEmpty()) {
                    item(key = "h_posts") {
                        SearchSectionHeader(
                            title = "Posts",
                            count = state.posts.size,
                            onSeeAll = if (state.posts.size > PREVIEW_PER_SECTION) {
                                { onScopeChange(SearchScope.Posts) }
                            } else null
                        )
                    }
                    items(state.posts.take(PREVIEW_PER_SECTION), key = { "p_${it.id}" }) { post ->
                        WebPostCard(
                            post = post,
                            onClick = { onPostClick(post.id) },
                            onLikeClick = {},
                            compact = true,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)
                        )
                    }
                }
                if (state.users.isNotEmpty()) {
                    item(key = "h_people") {
                        SearchSectionHeader(
                            title = "People",
                            count = state.users.size,
                            onSeeAll = if (state.users.size > PREVIEW_PER_SECTION) {
                                { onScopeChange(SearchScope.People) }
                            } else null
                        )
                    }
                    items(state.users.take(PREVIEW_PER_SECTION), key = { "u_${it.id}" }) { user ->
                        UserResultRow(user = user, onClick = { onProfileClick(user.username) })
                    }
                }
            }

            SearchScope.Resources -> {
                if (state.resources.isEmpty()) {
                    item(key = "empty_resources") { ScopeEmptyMessage("No resources match this search.") }
                } else {
                    items(state.resources, key = { it.id }) { resource ->
                        WebResourceCard(
                            resource = resource,
                            onClick = { onResourceClick(resource.id) },
                            minWidth = null,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)
                        )
                    }
                }
            }

            SearchScope.Posts -> {
                if (state.posts.isEmpty()) {
                    item(key = "empty_posts") { ScopeEmptyMessage("No posts match this search.") }
                } else {
                    items(state.posts, key = { it.id }) { post ->
                        WebPostCard(
                            post = post,
                            onClick = { onPostClick(post.id) },
                            onLikeClick = {},
                            compact = false,
                            modifier = Modifier.padding(horizontal = 16.dp, vertical = 5.dp)
                        )
                    }
                }
            }

            SearchScope.People -> {
                if (state.users.isEmpty()) {
                    item(key = "empty_people") { ScopeEmptyMessage("No one matches this search.") }
                } else {
                    items(state.users, key = { it.id }) { user ->
                        UserResultRow(user = user, onClick = { onProfileClick(user.username) })
                    }
                }
            }
        }
    }
}

@Composable
private fun SearchSectionHeader(
    title: String,
    count: Int,
    onSeeAll: (() -> Unit)?
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(start = 18.dp, end = 10.dp, top = 14.dp, bottom = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleSmallEmphasized,
            color = MaterialTheme.colorScheme.onSurface
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = count.toString(),
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier
                .clip(RoundedCornerShape(50))
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                .padding(horizontal = 8.dp, vertical = 2.dp)
        )
        Spacer(modifier = Modifier.weight(1f))
        if (onSeeAll != null) {
            Row(
                modifier = Modifier
                    .heightIn(min = 36.dp)
                    .nebPressable(onClick = onSeeAll)
                    .clip(RoundedCornerShape(50))
                    .padding(horizontal = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Text(
                    text = "All",
                    style = MaterialTheme.typography.labelLargeEmphasized,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Icon(
                    imageVector = Icons.AutoMirrored.Rounded.ArrowForward,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.size(15.dp)
                )
            }
        }
    }
}

@Composable
private fun ScopeEmptyMessage(message: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp, vertical = 48.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun UserResultRow(
    user: ApiUserSearchResult,
    onClick: () -> Unit
) {
    val subtitle = listOfNotNull(
        "@${user.username}".takeIf { user.username.isNotBlank() },
        user.classLevel?.takeIf { it.isNotBlank() },
        user.school?.takeIf { it.isNotBlank() }
    ).joinToString(", ")

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 2.dp)
            .heightIn(min = 64.dp)
            .nebPressable(onClick = onClick)
            .clip(RoundedCornerShape(22.dp))
            .padding(horizontal = 8.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Avatar(
            name = user.displayName ?: user.username,
            imageUrl = user.photoUrl,
            size = 46.dp
        )
        Column(modifier = Modifier.weight(1f)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = user.displayName?.takeIf { it.isNotBlank() } ?: user.username,
                    style = MaterialTheme.typography.titleSmallEmphasized,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                user.badgeInfo?.let { badge ->
                    Spacer(modifier = Modifier.width(6.dp))
                    NebBadge(badge)
                }
            }
            if (subtitle.isNotBlank()) {
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Text(
                text = "${compactCount(user.followerCount)} followers",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1
            )
        }
        UserStateTag(user = user)
    }
}

@Composable
private fun UserStateTag(user: ApiUserSearchResult) {
    val label = when {
        user.isSelf == true -> "You"
        user.isFollowing == true -> "Following"
        else -> return
    }
    Text(
        text = label,
        style = MaterialTheme.typography.labelMediumEmphasized,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        maxLines = 1,
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            .padding(horizontal = 12.dp, vertical = 6.dp)
    )
}
