package com.neb.ians.ui.screens.search

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Clear
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SuggestionChip
import androidx.compose.material3.SuggestionChipDefaults
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.ApiUserSearchResult
import com.neb.ians.ui.components.Avatar
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.compactCount
import com.neb.ians.util.formatTimeAgo
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.Surface

private val subjectColors = mapOf(
    "Physics" to Color(0xFF1B6EF3),
    "Chemistry" to Color(0xFF006E1C),
    "Mathematics" to Color(0xFFBA1A1A),
    "Biology" to Color(0xFF006E1C),
    "English" to Color(0xFF6F5677),
    "Nepali" to Color(0xFFBA1A1A),
    "Computer Science" to Color(0xFF0061A4)
)

private fun getSubjectColor(subject: String): Color {
    return subjectColors[subject] ?: Color(0xFF565F71)
}

private fun getSubjectIcon(subject: String): Int {
    return when (subject) {
        "Physics" -> R.drawable.ic_school
        "Chemistry" -> R.drawable.ic_school
        "Mathematics" -> R.drawable.ic_book
        "Biology" -> R.drawable.ic_school
        "English" -> R.drawable.ic_book
        "Nepali" -> R.drawable.ic_book
        "Computer Science" -> R.drawable.ic_document
        else -> R.drawable.ic_document
    }
}

private val TAB_LABELS = listOf("All", "Resources", "Posts", "People")

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun SearchScreen(
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit = {},
    onProfileClick: (String) -> Unit = {},
    onNavigateBack: () -> Unit,
    viewModel: SearchViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val focusRequester = remember { FocusRequester() }
    var selectedTab by remember { mutableStateOf(0) }

    BackHandler { onNavigateBack() }

    LaunchedEffect(Unit) { focusRequester.requestFocus() }

    Scaffold(
        topBar = {
            Column {
                TopAppBar(
                    title = {
                        OutlinedTextField(
                            value = uiState.query,
                            onValueChange = { viewModel.onQueryChange(it) },
                            placeholder = {
                                Text(
                                    text = "Search resources, posts, people...",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            },
                            leadingIcon = {
                                Icon(
                                    imageVector = Icons.Outlined.Search,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            },
                            trailingIcon = {
                                if (uiState.query.isNotEmpty()) {
                                    IconButton(onClick = { viewModel.clearSearch() }) {
                                        Icon(
                                            imageVector = Icons.Outlined.Clear,
                                            contentDescription = "Clear",
                                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }
                                }
                            },
                            singleLine = true,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(end = 8.dp)
                                .focusRequester(focusRequester),
                            shape = CircleShape,
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = Color.Transparent,
                                unfocusedBorderColor = Color.Transparent,
                                disabledBorderColor = Color.Transparent,
                                focusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                                unfocusedContainerColor = MaterialTheme.colorScheme.surfaceContainerHigh
                            )
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = onNavigateBack) {
                            Icon(
                                imageVector = Icons.Outlined.ArrowBack,
                                contentDescription = "Back",
                                tint = MaterialTheme.colorScheme.onSurface
                            )
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                )
                if (uiState.query.length >= 2) {
                    TabRow(
                        selectedTabIndex = selectedTab,
                        containerColor = MaterialTheme.colorScheme.surface,
                        contentColor = MaterialTheme.colorScheme.onSurface,
                        divider = { HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant) }
                    ) {
                        TAB_LABELS.forEachIndexed { index, label ->
                            Tab(
                                selected = selectedTab == index,
                                onClick = { selectedTab = index },
                                text = {
                                    Text(
                                        label,
                                        fontWeight = if (selectedTab == index) FontWeight.Bold else FontWeight.Normal
                                    )
                                }
                            )
                        }
                    }
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            when {
                uiState.isSearching -> {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator()
                    }
                }

                uiState.error != null && uiState.query.length >= 2 -> {
                    ErrorCard(
                        message = uiState.error ?: "Search failed",
                        onRetry = { viewModel.onQueryChange(uiState.query) },
                        modifier = Modifier.padding(16.dp)
                    )
                }

                uiState.query.isEmpty() -> {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 16.dp)
                    ) {
                        Text(
                            text = "Suggestions",
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        FlowRow(
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            SearchUiState.SUGGESTIONS.forEach { suggestion ->
                                SuggestionChip(
                                    onClick = { viewModel.onQueryChange(suggestion) },
                                    label = {
                                        Text(
                                            text = suggestion,
                                            style = MaterialTheme.typography.labelLarge,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    },
                                    shape = CircleShape,
                                    colors = SuggestionChipDefaults.suggestionChipColors(
                                        containerColor = MaterialTheme.colorScheme.surfaceContainerHigh,
                                        labelColor = MaterialTheme.colorScheme.onSurface
                                    ),
                                    border = SuggestionChipDefaults.suggestionChipBorder(
                                        borderColor = MaterialTheme.colorScheme.outlineVariant,
                                        enabled = true
                                    )
                                )
                            }
                        }
                    }
                }

                uiState.query.length >= 2 -> {
                    val hasResources = uiState.resources.isNotEmpty()
                    val hasPosts = uiState.posts.isNotEmpty()
                    val hasUsers = uiState.users.isNotEmpty()
                    val hasAny = hasResources || hasPosts || hasUsers

                    if (!hasAny) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = "No results found",
                                style = MaterialTheme.typography.bodyLarge,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    } else {
                        when (selectedTab) {
                            0 -> AllResultsTab(
                                resources = uiState.resources,
                                posts = uiState.posts,
                                users = uiState.users,
                                onResourceClick = onResourceClick,
                                onPostClick = onPostClick,
                                onProfileClick = onProfileClick
                            )
                            1 -> ResourcesTab(
                                resources = uiState.resources,
                                onResourceClick = onResourceClick
                            )
                            2 -> PostsTab(
                                posts = uiState.posts,
                                onPostClick = onPostClick
                            )
                            3 -> PeopleTab(
                                users = uiState.users,
                                onProfileClick = onProfileClick
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun AllResultsTab(
    resources: List<ApiResource>,
    posts: List<ApiPost>,
    users: List<ApiUserSearchResult>,
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit,
    onProfileClick: (String) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(vertical = 8.dp)
    ) {
        if (resources.isNotEmpty()) {
            item(key = "resources_header") {
                SectionHeader("Resources")
            }
            items(resources.take(3), key = { it.id }) { resource ->
                SearchResultItem(
                    resource = resource,
                    onClick = { onResourceClick(resource.id) }
                )
            }
        }
        if (posts.isNotEmpty()) {
            item(key = "posts_header") {
                SectionHeader("Posts")
            }
            items(posts.take(3), key = { it.id }) { post ->
                PostResultItem(
                    post = post,
                    onClick = { onPostClick(post.id) }
                )
            }
        }
        if (users.isNotEmpty()) {
            item(key = "people_header") {
                SectionHeader("People")
            }
            items(users.take(3), key = { it.id }) { user ->
                UserResultItem(
                    user = user,
                    onClick = { onProfileClick(user.username) }
                )
            }
        }
    }
}

@Composable
private fun ResourcesTab(
    resources: List<ApiResource>,
    onResourceClick: (String) -> Unit
) {
    if (resources.isEmpty()) {
        EmptyTabMessage("No resources found")
    } else {
        LazyVerticalGrid(
            columns = GridCells.Adaptive(minSize = 174.dp),
            contentPadding = PaddingValues(start = 16.dp, top = 8.dp, end = 16.dp, bottom = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(resources, key = { it.id }) { resource ->
                WebResourceCard(
                    resource = resource,
                    onClick = { onResourceClick(resource.id) },
                    minWidth = null
                )
            }
        }
    }
}

@Composable
private fun PostsTab(
    posts: List<ApiPost>,
    onPostClick: (String) -> Unit
) {
    if (posts.isEmpty()) {
        EmptyTabMessage("No posts found")
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(vertical = 8.dp)
        ) {
            items(posts, key = { it.id }) { post ->
                PostResultItem(
                    post = post,
                    onClick = { onPostClick(post.id) }
                )
            }
        }
    }
}

@Composable
private fun PeopleTab(
    users: List<ApiUserSearchResult>,
    onProfileClick: (String) -> Unit
) {
    if (users.isEmpty()) {
        EmptyTabMessage("No people found")
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(vertical = 8.dp)
        ) {
            items(users, key = { it.id }) { user ->
                UserResultItem(
                    user = user,
                    onClick = { onProfileClick(user.username) }
                )
            }
        }
    }
}

@Composable
private fun SectionHeader(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleSmall,
        fontWeight = FontWeight.Bold,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
    )
}

@Composable
private fun EmptyTabMessage(message: String) {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = message,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun SearchResultItem(
    resource: ApiResource,
    onClick: () -> Unit
) {
    val subjectColor = getSubjectColor(resource.subject)

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(40.dp)
                .clip(CircleShape)
                .background(subjectColor.copy(alpha = 0.12f)),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                painter = painterResource(id = getSubjectIcon(resource.subject)),
                contentDescription = null,
                modifier = Modifier.size(20.dp),
                tint = subjectColor
            )
        }
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(start = 12.dp)
        ) {
            Text(
                text = resource.title,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = "${resource.subject} · ${resource.type} · ${resource.gradeLevel}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun PostResultItem(
    post: ApiPost,
    onClick: () -> Unit
) {
    val categoryColor = getSubjectColor(post.category)

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        tonalElevation = 1.dp,
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(12.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Avatar(
                    name = post.authorName,
                    imageUrl = post.authorPhotoUrl,
                    size = 28.dp
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = post.authorName,
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Medium
                    )
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(4.dp),
                            color = categoryColor.copy(alpha = 0.08f)
                        ) {
                            Text(
                                text = post.category,
                                modifier = Modifier.padding(horizontal = 4.dp, vertical = 1.dp),
                                style = MaterialTheme.typography.labelSmall,
                                color = categoryColor,
                                fontWeight = FontWeight.Medium
                            )
                        }
                        Text(
                            text = "·",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f)
                        )
                        Text(
                            text = formatTimeAgo(post.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = post.title,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (post.content.isNotBlank()) {
                Text(
                    text = post.content.take(100) + if (post.content.length > 100) "..." else "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
            Spacer(modifier = Modifier.height(6.dp))
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(
                        imageVector = if (post.isThumbedUp) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = if (post.isThumbedUp) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = "${post.thumbsUpCount}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Icon(
                        Icons.Outlined.ChatBubbleOutline,
                        contentDescription = null,
                        modifier = Modifier.size(14.dp),
                        tint = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = "${post.replyCount}",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
    Spacer(modifier = Modifier.height(8.dp))
}

@Composable
private fun UserResultItem(
    user: ApiUserSearchResult,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Avatar(
            name = user.displayName ?: user.username,
            imageUrl = user.photoUrl,
            size = 44.dp
        )
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(start = 12.dp)
        ) {
            Text(
                text = user.displayName ?: user.username,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = "@${user.username}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            if (!user.bio.isNullOrBlank()) {
                Text(
                    text = user.bio!!.take(80) + if (user.bio!!.length > 80) "..." else "",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
        if (user.isFollowing == true) {
            Surface(
                shape = RoundedCornerShape(16.dp),
                color = MaterialTheme.colorScheme.surfaceVariant
            ) {
                Text(
                    text = "Following",
                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
    HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))
}