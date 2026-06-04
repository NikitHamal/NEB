package com.neb.ians.ui.screens.home

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.ShimmerHomeScreen
import com.neb.ians.ui.components.WebPostCard
import com.neb.ians.ui.components.WebResourceCard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onResourceClick: (String) -> Unit,
    onPostClick: (String) -> Unit = {},
    onSearchClick: () -> Unit,
    onViewAllClick: () -> Unit,
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
                    Column {
                        Text(
                            text = "Hello, ${uiState.userName}",
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "What would you like to study today?",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
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

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(horizontal = 16.dp, vertical = 8.dp),
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

                    SectionHeader(
                        title = "Recent Resources",
                        onViewAllClick = onViewAllClick
                    )

                    if (uiState.recentResources.isEmpty()) {
                        EmptyResourceRow(message = "No resources yet. Check the Library to explore.")
                    } else {
                        LazyRow(
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(uiState.recentResources, key = { it.id }) { resource ->
                                WebResourceCard(
                                    resource = resource,
                                    modifier = Modifier.width(168.dp),
                                    onClick = { onResourceClick(resource.id) }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    SectionHeader(
                        title = "Popular Resources",
                        onViewAllClick = onViewAllClick
                    )

                    if (uiState.popularResources.isEmpty()) {
                        EmptyResourceRow(message = "Popular resources will appear here.")
                    } else {
                        LazyRow(
                            contentPadding = PaddingValues(horizontal = 16.dp),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items(uiState.popularResources, key = { it.id }) { resource ->
                                WebResourceCard(
                                    resource = resource,
                                    modifier = Modifier.width(168.dp),
                                    onClick = { onResourceClick(resource.id) }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    SectionHeader(
                        title = "Forum Activity",
                        onViewAllClick = null
                    )

                    if (uiState.recentPosts.isEmpty()) {
                        EmptyForumSection()
                    } else {
                        Column(
                            modifier = Modifier.padding(horizontal = 16.dp)
                        ) {
                            uiState.recentPosts.forEach { post ->
                                WebPostCard(
                                    post = post,
                                    onClick = { onPostClick(post.id) },
                                    onThumbsUpClick = {}
                                )
                                Spacer(modifier = Modifier.height(10.dp))
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
