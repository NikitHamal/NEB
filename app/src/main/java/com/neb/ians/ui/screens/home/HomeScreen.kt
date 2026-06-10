package com.neb.ians.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiPost
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NEBiansLogoWordmark
import com.neb.ians.ui.components.ShimmerHomeScreen
import com.neb.ians.ui.components.StudyLabHeroCard
import com.neb.ians.ui.components.WebHero
import com.neb.ians.ui.components.WebResourceCard
import com.neb.ians.ui.components.WebSectionHeader
import com.neb.ians.ui.theme.getSubjectTheme

private fun getTypeIcon(type: String): Int {
    return when (type.lowercase()) {
        "textbook" -> R.drawable.ic_book
        "notes" -> R.drawable.ic_document
        "past papers" -> R.drawable.ic_document
        "guide" -> R.drawable.ic_book
        "solution" -> R.drawable.ic_school
        else -> R.drawable.ic_document
    }
}

private fun getSubjectIcon(subject: String): Int {
    return when (subject) {
        "Physics" -> R.drawable.ic_science
        "Chemistry" -> R.drawable.ic_science
        "Mathematics" -> R.drawable.ic_science
        "Biology" -> R.drawable.ic_science
        "English" -> R.drawable.ic_globe
        "Nepali" -> R.drawable.ic_globe
        "Computer Science" -> R.drawable.ic_science
        "Economics" -> R.drawable.ic_globe
        "Accountancy" -> R.drawable.ic_book
        else -> R.drawable.ic_document
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
    onStudyLabClick: () -> Unit = {},
    onNebyAiClick: () -> Unit = {},
    onSubjectClick: (String) -> Unit = {},
    viewModel: HomeViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = {
                    NEBiansLogoWordmark()
                },
                actions = {
                    FilledTonalIconButton(onClick = onSearchClick) {
                        Icon(
                            imageVector = Icons.Outlined.Search,
                            contentDescription = "Search"
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.largeTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    scrolledContainerColor = MaterialTheme.colorScheme.surfaceContainer
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(innerPadding)
        ) {
            if (uiState.isLoading) {
                ShimmerHomeScreen()
            } else if (uiState.error != null && uiState.recentResources.isEmpty() && uiState.popularResources.isEmpty()) {
                Column(
                    modifier = Modifier
                        .fillMaxSize(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    ErrorCard(
                        message = uiState.error ?: "Something went wrong",
                        onRetry = { viewModel.refresh() }
                    )
                }
            } else {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                ) {
                    if (uiState.error != null) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = { viewModel.refresh() },
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                    }

                    WebHero(
                        title = "Hello, ${uiState.userName}!",
                        body = "Discover study resources, join discussions, and connect with learners and teachers of all classes and faculties.",
                        primaryText = "Browse Library",
                        primaryIconRes = R.drawable.ic_book,
                        onPrimaryClick = onViewAllClick,
                        secondaryText = "Neby AI",
                        secondaryIconRes = R.drawable.ic_science,
                        onSecondaryClick = onNebyAiClick
                    )

                    StudyLabHeroCard(onClick = onStudyLabClick)

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(horizontal = 24.dp, vertical = 12.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        HomeUiState.SUBJECTS.forEach { subject ->
                            SuggestionChip(
                                onClick = { onSubjectClick(subject) },
                                label = {
                                    Text(
                                        text = subject,
                                        style = MaterialTheme.typography.labelLarge,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis
                                    )
                                },
                                shape = RoundedCornerShape(50),
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

                    WebSectionHeader(
                        title = "Recent Resources",
                        onActionClick = onViewAllClick
                    )

                    if (uiState.recentResources.isEmpty()) {
                        EmptyResourceRow(message = "No resources yet. Check the Library to explore.")
                    } else {
                        LazyRow(
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(uiState.recentResources, key = { it.id }) { resource ->
                                ResourceCard(
                                    resource = resource,
                                    onClick = { onResourceClick(resource.id) }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    WebSectionHeader(
                        title = "Popular Resources",
                        onActionClick = onViewAllClick
                    )

                    if (uiState.popularResources.isEmpty()) {
                        EmptyResourceRow(message = "Popular resources will appear here.")
                    } else {
                        LazyRow(
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(uiState.popularResources, key = { it.id }) { resource ->
                                ResourceCard(
                                    resource = resource,
                                    onClick = { onResourceClick(resource.id) }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    WebSectionHeader(
                        title = "Trending Discussions",
                        actionLabel = null,
                        onActionClick = null
                    )

                    if (uiState.recentPosts.isEmpty()) {
                        EmptyForumSection()
                    } else {
                        Column(
                            modifier = Modifier.padding(horizontal = 16.dp)
                        ) {
                            uiState.recentPosts.forEach { post ->
                                ForumPostItem(post = post)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                }
            }
        }
    }
}

@Composable
private fun SectionHeader(
    title: String,
    onViewAllClick: (() -> Unit)?
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface
        )
        if (onViewAllClick != null) {
            TextButton(onClick = onViewAllClick) {
                Text(
                    text = "View all",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
private fun ResourceCard(
    resource: ApiResource,
    onClick: () -> Unit
) {
    WebResourceCard(
        resource = resource,
        onClick = onClick,
        modifier = Modifier.width(184.dp)
    )
}

@Composable
private fun ForumPostItem(post: ApiPost) {
    ListItem(
        headlineContent = {
            Text(
                text = post.title,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        supportingContent = {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = post.authorName,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = post.category,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        },
        leadingContent = {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = post.authorName.firstOrNull()?.uppercase() ?: "?",
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
        },
        trailingContent = {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Icon(
                    imageVector = Icons.Outlined.ThumbUp,
                    contentDescription = "Likes",
                    modifier = Modifier.size(16.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "${post.thumbsUpCount}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        },
        colors = ListItemDefaults.colors(
            containerColor = MaterialTheme.colorScheme.surfaceContainerLow
        ),
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 2.dp)
            .clip(RoundedCornerShape(12.dp))
    )
}

@Composable
private fun EmptyResourceRow(message: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 24.dp),
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
private fun EmptyForumSection() {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 24.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "No forum posts yet. Start a discussion!",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
