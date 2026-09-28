@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.nebBorderSubtle
import kotlinx.coroutines.launch

/**
 * One creator's page, in the app.
 *
 * The sections come from the owner's own arrangement (`blocks`), so this screen
 * is a renderer rather than a layout: every block type the studio can add has
 * exactly one branch here, and the order is theirs. Same contract as the web
 * storefront, which is what keeps a page looking like the same page.
 */
@Composable
fun CreatorPageScreen(
    onNavigateBack: () -> Unit,
    onCourseClick: (String) -> Unit,
    onResourceClick: (String) -> Unit,
    onOpenStudio: () -> Unit,
    viewModel: CreatorPageViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val scope = rememberCoroutineScope()
    var isRefreshing by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            text = uiState.page?.displayName ?: "Marketplace",
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                        uiState.page?.let { page ->
                            Text(
                                text = creatorKindLabel(page.kind) +
                                    if (page.verified && page.style.showVerified) " · Verified" else "",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (uiState.page?.isMine == true) {
                        NebButton(
                            text = "Edit",
                            onClick = onOpenStudio,
                            icon = Icons.Outlined.Edit,
                            tone = NebButtonTone.Text,
                            size = NebButtonSize.Small
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = isRefreshing,
            onRefresh = {
                scope.launch {
                    isRefreshing = true
                    viewModel.refresh()
                    isRefreshing = false
                }
            },
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            when {
                uiState.isLoading && uiState.page == null ->
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        NebLoader()
                    }

                uiState.error != null && uiState.page == null ->
                    Box(modifier = Modifier.fillMaxSize()) {
                        ErrorCard(
                            message = uiState.error ?: "Something went wrong",
                            onRetry = viewModel::refresh,
                            modifier = Modifier.padding(16.dp)
                        )
                    }

                uiState.page == null ->
                    NebEmptyState(
                        icon = Icons.Outlined.Storefront,
                        title = "This page is not available",
                        subtitle = "It may have been unpublished by its owner."
                    )

                else -> {
                    val page = uiState.page!!
                    CreatorPageBody(
                        page = page,
                        onCourseClick = onCourseClick,
                        onResourceClick = onResourceClick
                    )
                }
            }
        }
    }
}

@Composable
private fun CreatorPageBody(
    page: ApiCreatorPage,
    onCourseClick: (String) -> Unit,
    onResourceClick: (String) -> Unit
) {
    val accent = creatorAccent(page.accentHex)
    val style = rememberCreatorStyle(page)
    val blocks = remember(page.blocks) { page.blocks.filter { it.enabled } }
    val paid = remember(page.courses) { page.courses.filter { !it.isFree } }
    val free = remember(page.courses) { page.courses.filter { it.isFree } }
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    // A "See offerings" button in a hero is an anchor, so it scrolls to that
    // section rather than pretending to be a second page.
    val jumpTo: (String) -> Unit = { anchor ->
        val wanted = if (anchor == "offerings") "courses" else anchor
        val index = blocks.indexOfFirst { it.type == wanted }
        if (index >= 0) scope.launch { listState.animateScrollToItem(index) }
    }

    if (blocks.isEmpty()) {
        NebEmptyState(
            icon = Icons.Outlined.Storefront,
            title = "This page has no sections yet",
            subtitle = if (page.isMine) "Add your first section in the studio." else "Check back soon."
        )
        return
    }

    CompositionLocalProvider(LocalCreatorStyle provides style) {
        LazyColumn(
            state = listState,
            contentPadding = PaddingValues(bottom = 110.dp),
            verticalArrangement = Arrangement.spacedBy(0.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            itemsIndexed(blocks, key = { _, block -> block.id.ifBlank { block.type } }) { index, block ->
                // the web page draws no rule under its final section, so neither
                // does this one
                val last = index == blocks.lastIndex
                when (block.type) {
                    "hero" -> CreatorHeroBlock(page, block, accent, jumpTo)
                    "about" -> CreatorAboutBlock(page, block, last)
                    "stats" -> CreatorStatsBlock(page, block, accent, last)
                    "courses" -> CreatorCoursesBlock(block, paid, free, page.accentHex, last, onCourseClick)
                    "resources" -> CreatorResourcesBlock(block, page, accent, last, onResourceClick)
                    "documents" -> CreatorDocumentsBlock(block, page, accent, last, onResourceClick)
                    "posts" -> CreatorPostsBlock(block, page, accent, last)
                    "showcase" -> CreatorShowcaseBlock(block, accent, last)
                    "gallery" -> CreatorGalleryBlock(block, last)
                    "testimonials" -> CreatorTestimonialsBlock(block, accent, last)
                    "faq" -> CreatorFaqBlock(block, last)
                    "schedule" -> CreatorScheduleBlock(block, accent, last)
                    "links" -> CreatorLinksBlock(block, accent, last)
                    "contact" -> CreatorContactBlock(page, block, accent, last)
                    "cta" -> CreatorCtaBlock(block, accent, jumpTo)
                    else -> Unit
                }
            }
        }
    }
}


/** Opens a creator's own link. http(s) goes to the browser, anything else to
 *  whichever app claims the scheme; a link with no handler says so out loud
 *  rather than looking like a dead row. */
internal fun openCreatorLink(context: android.content.Context, url: String) {
    val trimmed = url.trim()
    if (trimmed.isEmpty() || trimmed.startsWith("#")) return
    val scheme = trimmed.substringBefore(':', "").lowercase()
    if (scheme !in setOf("http", "https", "mailto", "tel")) return
    runCatching {
        context.startActivity(
            android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(trimmed))
                .addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
        )
    }.onFailure {
        android.widget.Toast.makeText(context, "No app found to open that link", android.widget.Toast.LENGTH_SHORT).show()
    }
}

/**
 * One section: its heading, its content and the hairline that separates it from
 * the next. The vertical rhythm and the rule come from the creator's `density`
 * and `layout` choices, exactly as `.mkt-block` does on the web.
 */
@Composable
internal fun CreatorBlockShell(
    title: String?,
    subtitle: String? = null,
    isLast: Boolean = false,
    content: @Composable () -> Unit
) {
    val style = LocalCreatorStyle.current
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = style.blockPadding),
        verticalArrangement = Arrangement.spacedBy(style.itemGap)
    ) {
        if (!title.isNullOrBlank() || !subtitle.isNullOrBlank()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Bottom,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = title.orEmpty(),
                    style = MaterialTheme.typography.titleMediumEmphasized,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.weight(1f)
                )
                if (!subtitle.isNullOrBlank()) {
                    Text(
                        text = subtitle,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
        content()
        if (style.dividers && !isLast) {
            HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
        }
    }
}
