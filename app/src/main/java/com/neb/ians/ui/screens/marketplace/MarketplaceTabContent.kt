@file:OptIn(androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.background
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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.lazy.items as listItems
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebChip
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.NebLoaderSize
import com.neb.ians.ui.components.NebSectionLabel
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.nebBorderSubtle
import kotlinx.coroutines.flow.distinctUntilChanged

/**
 * The marketplace shelf inside the library — the tab that sits between Library
 * and Syllabus in both the app and on the web.
 *
 * One scrollable surface: the owner's own invitation at the top (only when they
 * may have a page), the kind rail, the newest offerings as a row, then the
 * creator grid. Everything reads from the same payloads the web shelf uses.
 */
@Composable
fun MarketplaceTabContent(
    state: MarketplaceUiState,
    onRetry: () -> Unit,
    onCreatorClick: (String) -> Unit,
    onCourseClick: (String) -> Unit,
    onOpenStudio: () -> Unit,
    onKindSelected: (MarketplaceKind) -> Unit,
    onQueryChange: (String) -> Unit,
    onSubmitQuery: () -> Unit,
    onLoadMore: () -> Unit,
    modifier: Modifier = Modifier
) {
    when {
        state.isLoading -> MarketplaceShelfSkeleton(modifier)
        state.error != null && state.creators.isEmpty() && state.offerings.isEmpty() ->
            Box(modifier = modifier.fillMaxSize()) {
                ErrorCard(
                    message = state.error,
                    onRetry = onRetry,
                    modifier = Modifier.padding(16.dp)
                )
            }

        else -> MarketplaceShelf(
            state = state,
            onRetry = onRetry,
            onCreatorClick = onCreatorClick,
            onCourseClick = onCourseClick,
            onOpenStudio = onOpenStudio,
            onKindSelected = onKindSelected,
            onQueryChange = onQueryChange,
            onSubmitQuery = onSubmitQuery,
            onLoadMore = onLoadMore,
            modifier = modifier
        )
    }
}

@Composable
private fun MarketplaceShelf(
    state: MarketplaceUiState,
    onRetry: () -> Unit,
    onCreatorClick: (String) -> Unit,
    onCourseClick: (String) -> Unit,
    onOpenStudio: () -> Unit,
    onKindSelected: (MarketplaceKind) -> Unit,
    onQueryChange: (String) -> Unit,
    onSubmitQuery: () -> Unit,
    onLoadMore: () -> Unit,
    modifier: Modifier = Modifier
) {
    val gridState = rememberLazyGridState()

    LaunchedEffect(gridState, state.hasMore) {
        snapshotFlow {
            val info = gridState.layoutInfo
            (info.visibleItemsInfo.lastOrNull()?.index ?: -1) to info.totalItemsCount
        }
            .distinctUntilChanged()
            .collect { (lastVisible, total) ->
                if (state.hasMore && total > 0 && lastVisible >= total - 3) onLoadMore()
            }
    }

    LazyVerticalGrid(
        state = gridState,
        columns = GridCells.Adaptive(minSize = 320.dp),
        contentPadding = PaddingValues(start = 16.dp, top = 6.dp, end = 16.dp, bottom = 110.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = modifier.fillMaxSize()
    ) {
        if (state.canCreate) {
            item(key = "owner_banner", span = { GridItemSpan(maxLineSpan) }) {
                MarketplaceOwnerBanner(
                    pageName = state.myPage?.displayName,
                    published = state.myPage?.published == true,
                    accentHex = state.myPage?.accentHex ?: "#004BD4",
                    onOpenStudio = onOpenStudio
                )
            }
        }

        item(key = "search", span = { GridItemSpan(maxLineSpan) }) {
            MarketplaceSearchField(
                query = state.query,
                onQueryChange = onQueryChange,
                onSubmit = onSubmitQuery
            )
        }

        item(key = "kinds", span = { GridItemSpan(maxLineSpan) }) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                MarketplaceKind.entries.forEach { kind ->
                    NebChip(
                        label = kind.label,
                        selected = state.kind == kind,
                        onClick = { onKindSelected(kind) }
                    )
                }
            }
        }

        if (state.offerings.isNotEmpty()) {
            item(key = "offerings_title", span = { GridItemSpan(maxLineSpan) }) {
                ShelfHeading(
                    title = "Paid and free offerings",
                    trailing = "${state.offerings.size} shown"
                )
            }
            item(key = "offerings", span = { GridItemSpan(maxLineSpan) }) {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    contentPadding = PaddingValues(end = 4.dp)
                ) {
                    listItems(state.offerings, key = { it.id }) { course ->
                        MarketplaceCourseCard(
                            course = course,
                            onClick = { onCourseClick(course.id) },
                            showCreator = true
                        )
                    }
                }
            }
        }

        item(key = "creators_title", span = { GridItemSpan(maxLineSpan) }) {
            ShelfHeading(
                title = when {
                    state.query.isNotBlank() -> "Results for \"${state.query}\""
                    state.kind != MarketplaceKind.Everyone -> state.kind.label
                    else -> "Pages on NEBians"
                },
                trailing = "${state.total} page${if (state.total == 1) "" else "s"}"
            )
        }

        if (state.creators.isEmpty()) {
            item(key = "empty", span = { GridItemSpan(maxLineSpan) }) {
                NebEmptyState(
                    icon = Icons.Outlined.Storefront,
                    title = if (state.query.isNotBlank()) "No page matches that" else "No pages here yet",
                    subtitle = if (state.canCreate) {
                        "Tutors and institutes build these pages. Yours can be first."
                    } else {
                        "Marketplace pages appear here as teachers and institutes publish them."
                    },
                    action = if (state.canCreate) {
                        {
                            NebButton(
                                text = "Create your page",
                                onClick = onOpenStudio,
                                icon = Icons.Outlined.Add,
                                tone = NebButtonTone.Tonal,
                                size = NebButtonSize.Small
                            )
                        }
                    } else null
                )
            }
        } else {
            items(state.creators, key = { it.id }) { creator ->
                MarketplaceCreatorCard(
                    creator = creator,
                    onClick = { onCreatorClick(creator.slug) }
                )
            }
        }

        if (state.isLoadingMore) {
            item(key = "loading_more", span = { GridItemSpan(maxLineSpan) }) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 14.dp),
                    horizontalArrangement = Arrangement.Center
                ) {
                    NebLoader(size = NebLoaderSize.Small)
                }
            }
        } else if (state.error != null && state.creators.isNotEmpty()) {
            item(key = "inline_error", span = { GridItemSpan(maxLineSpan) }) {
                ErrorCard(
                    message = state.error ?: "Something went wrong",
                    onRetry = onRetry,
                    modifier = Modifier.padding(vertical = 8.dp)
                )
            }
        }
    }
}

@Composable
private fun ShelfHeading(title: String, trailing: String? = null) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 10.dp, bottom = 2.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        if (trailing != null) {
            Text(
                text = trailing,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

/** The creator's own doorway into the studio, shown only to eligible accounts. */
@Composable
private fun MarketplaceOwnerBanner(
    pageName: String?,
    published: Boolean,
    accentHex: String,
    onOpenStudio: () -> Unit
) {
    val accent = creatorAccent(accentHex)
    val shape = WebPanelShape

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceContainerLow)
            .clickable(onClick = onOpenStudio)
            .padding(14.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .size(38.dp)
                .clip(CircleShape)
                .background(accent.copy(alpha = 0.18f)),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Outlined.Storefront,
                contentDescription = null,
                tint = accent,
                modifier = Modifier.size(20.dp)
            )
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = pageName?.takeIf { it.isNotBlank() } ?: "Your marketplace page",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = when {
                    pageName.isNullOrBlank() -> "Teachers, institutes and admins can list courses and get paid."
                    published -> "Your page is live. Add a course or post an update."
                    else -> "Your page is a draft — publish it when it is ready."
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2
            )
        }
        Text(
            text = if (pageName.isNullOrBlank()) "Create" else "Studio",
            style = MaterialTheme.typography.labelLarge,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onSurface
        )
    }
}

@Composable
private fun MarketplaceSearchField(
    query: String,
    onQueryChange: (String) -> Unit,
    onSubmit: () -> Unit
) {
    var text by remember(query) { mutableStateOf(query) }

    OutlinedTextField(
        value = text,
        onValueChange = {
            text = it
            onQueryChange(it)
        },
        modifier = Modifier.fillMaxWidth(),
        placeholder = { Text("Search tutors, institutes, subjects", maxLines = 1) },
        leadingIcon = {
            Icon(Icons.Outlined.Search, contentDescription = null, modifier = Modifier.size(20.dp))
        },
        trailingIcon = {
            if (text.isNotBlank()) {
                TextButton(onClick = onSubmit) { Text("Search") }
            }
        },
        singleLine = true,
        shape = RoundedCornerShape(WebCardShape.topStart),
        keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(imeAction = ImeAction.Search),
        keyboardActions = androidx.compose.foundation.text.KeyboardActions(onSearch = { onSubmit() })
    )
}

@Composable
private fun MarketplaceShelfSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Spacer(Modifier.height(6.dp))
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(40.dp)
                .clip(WebCardShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        )
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            repeat(3) {
                Box(
                    modifier = Modifier
                        .width(84.dp)
                        .height(32.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerHigh)
                )
            }
        }
        CreatorCardSkeleton()
        CreatorCardSkeleton()
    }
}

