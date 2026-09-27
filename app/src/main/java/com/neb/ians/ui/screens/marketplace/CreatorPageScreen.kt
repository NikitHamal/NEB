@file:OptIn(
    androidx.compose.material3.ExperimentalMaterial3Api::class,
    androidx.compose.material3.ExperimentalMaterial3ExpressiveApi::class
)

package com.neb.ians.ui.screens.marketplace

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.outlined.Edit
import androidx.compose.material.icons.outlined.LocationOn
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Storefront
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.api.ApiCreatorBlock
import com.neb.ians.data.api.ApiCreatorBlockItem
import com.neb.ians.data.api.ApiCreatorCourse
import com.neb.ians.data.api.ApiCreatorPage
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebLoader
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.getMaterialIcon
import com.neb.ians.ui.components.nebBorderSubtle
import com.neb.ians.util.formatTimeAgo
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
                                    if (page.verified) " · Verified" else "",
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

    LazyColumn(
        state = listState,
        contentPadding = PaddingValues(bottom = 110.dp),
        verticalArrangement = Arrangement.spacedBy(0.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(blocks, key = { it.id.ifBlank { it.type } }) { block ->
            when (block.type) {
                "hero" -> CreatorHeroBlock(page, block, accent, jumpTo)
                "about" -> CreatorAboutBlock(page, block)
                "stats" -> CreatorStatsBlock(page, block, accent)
                "courses" -> CreatorCoursesBlock(block, paid, free, accent, onCourseClick)
                "resources", "documents" -> CreatorResourcesBlock(block, page, accent, onResourceClick)
                "posts" -> CreatorPostsBlock(block, page, accent)
                "showcase" -> CreatorShowcaseBlock(block, accent)
                "gallery" -> CreatorGalleryBlock(block, page)
                "testimonials" -> CreatorTestimonialsBlock(block, accent)
                "faq" -> CreatorFaqBlock(block)
                "schedule" -> CreatorScheduleBlock(block, accent)
                "links" -> CreatorLinksBlock(block, accent)
                "contact" -> CreatorContactBlock(page, block, accent)
                "cta" -> CreatorCtaBlock(block, accent, jumpTo)
                else -> Unit
            }
        }
    }
}


/** Opens a creator's own link. http(s) goes to the browser, anything else to
 *  whichever app claims the scheme; a link with no handler says so out loud
 *  rather than looking like a dead row. */
private fun openCreatorLink(context: android.content.Context, url: String) {
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

@Composable
private fun CreatorBlockShell(
    title: String?,
    subtitle: String? = null,
    content: @Composable () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
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
        HorizontalDivider(color = nebBorderSubtle(), thickness = 1.dp)
    }
}

@Composable
private fun CreatorHeroBlock(
    page: ApiCreatorPage,
    block: ApiCreatorBlock,
    accent: Color,
    onJumpTo: (String) -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .padding(top = 12.dp, bottom = 18.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(132.dp)
                .clip(WebPanelShape)
                .background(MaterialTheme.colorScheme.surfaceContainerHigh)
        ) {
            when {
                page.coverUrl.isNotBlank() -> AsyncImage(
                    model = page.coverUrl,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )

                else -> Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(accent.copy(alpha = 0.20f))
                )
            }
        }

        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(
                modifier = Modifier
                    .size(72.dp)
                    .clip(CircleShape)
                    .background(accent),
                contentAlignment = Alignment.Center
            ) {
                if (page.avatarUrl.isNotBlank()) {
                    AsyncImage(
                        model = page.avatarUrl,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Text(
                        text = page.displayName.take(1).ifBlank { "N" },
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.surface
                    )
                }
            }
            Column(verticalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.weight(1f)) {
                Text(
                    text = creatorKindLabel(page.kind).uppercase(),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = accent
                )
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(
                        text = block.title.ifBlank { page.displayName },
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    if (page.verified) {
                        Icon(
                            imageVector = Icons.Filled.Verified,
                            contentDescription = "Verified",
                            tint = accent,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }
        }

        val tagline = block.subtitle.ifBlank { page.tagline }
        if (tagline.isNotBlank()) {
            Text(
                text = tagline,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        if (page.subjects.isNotEmpty() || page.location.isNotBlank()) {
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                page.subjects.take(3).forEach { subject ->
                    Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.surfaceContainer) {
                        Text(
                            text = subject,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 9.dp, vertical = 3.dp)
                        )
                    }
                }
                if (page.location.isNotBlank()) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
                        Icon(
                            imageVector = Icons.Outlined.LocationOn,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(14.dp)
                        )
                        Text(
                            text = page.location,
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }

        if (block.ctaLabel.isNotBlank()) {
            val context = LocalContext.current
            val target = block.ctaUrl.ifBlank { "#offerings" }
            NebButton(
                text = block.ctaLabel,
                onClick = {
                    if (target.startsWith("#")) {
                        // an in-page jump: the offerings sit further down this list
                        onJumpTo("offerings")
                    } else {
                        openCreatorLink(context, target)
                    }
                },
                tone = NebButtonTone.Primary,
                size = NebButtonSize.Small,
                icon = Icons.Outlined.OpenInNew
            )
        }
    }
}

@Composable
private fun CreatorAboutBlock(page: ApiCreatorPage, block: ApiCreatorBlock) {
    val body = block.body.ifBlank { page.about }
    if (body.isBlank()) return
    CreatorBlockShell(title = block.title.ifBlank { "About" }) {
        Text(
            text = body,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface
        )
    }
}

@Composable
private fun CreatorStatsBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color) {
    val items = block.items.ifEmpty {
        listOf(
            ApiCreatorBlockItem(label = "Offerings", value = page.courseCount.toString()),
            ApiCreatorBlockItem(label = "Views", value = compactCount(page.viewCount)),
            ApiCreatorBlockItem(label = "Resources", value = page.resources.size.toString())
        )
    }
    CreatorBlockShell(title = block.title.ifBlank { "Numbers" }) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
            items.take(3).forEach { item ->
                Column(
                    modifier = Modifier
                        .weight(1f)
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(12.dp),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    Text(
                        text = item.value,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = accent
                    )
                    Text(
                        text = item.label,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        }
    }
}

@Composable
private fun CreatorCoursesBlock(
    block: ApiCreatorBlock,
    paid: List<ApiCreatorCourse>,
    free: List<ApiCreatorCourse>,
    accent: Color,
    onCourseClick: (String) -> Unit
) {
    CreatorBlockShell(title = block.title.ifBlank { "Courses and classes" }, subtitle = block.subtitle) {
        if (paid.isEmpty() && free.isEmpty()) {
            Text(
                text = "Nothing listed yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                if (paid.isNotEmpty()) {
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(paid, key = { it.id }) { course ->
                            MarketplaceCourseCard(
                                course = course,
                                onClick = { onCourseClick(course.id) },
                                accentHex = "#1F2937"
                            )
                        }
                    }
                }
                if (free.isNotEmpty()) {
                    if (paid.isNotEmpty()) {
                        Text(
                            text = "Free",
                            style = MaterialTheme.typography.labelMediumEmphasized,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(free, key = { it.id }) { course ->
                            MarketplaceCourseCard(
                                course = course,
                                onClick = { onCourseClick(course.id) },
                                accentHex = "#1F2937"
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorResourcesBlock(
    block: ApiCreatorBlock,
    page: ApiCreatorPage,
    accent: Color,
    onResourceClick: (String) -> Unit
) {
    CreatorBlockShell(title = block.title.ifBlank { "Resources" }, subtitle = block.subtitle) {
        if (page.resources.isEmpty()) {
            Text(
                text = "No library resources yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                page.resources.take(8).forEach { resource ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(WebCardShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .clickable { onResourceClick(resource.id) }
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                            Text(
                                text = resource.title,
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = listOf(resource.subject.ifBlank { "General" }, resource.gradeLevel)
                                    .filter { it.isNotBlank() }
                                    .joinToString(" · "),
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        if (resource.isPaid) {
                            Surface(shape = WebPillShape, color = accent) {
                                Text(
                                    text = "Rs. ${resource.price}",
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.surface,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorPostsBlock(block: ApiCreatorBlock, page: ApiCreatorPage, accent: Color) {
    CreatorBlockShell(title = block.title.ifBlank { "Updates" }, subtitle = block.subtitle) {
        if (page.posts.isEmpty()) {
            Text(
                text = "No updates posted yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                page.posts.forEach { post ->
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(WebCardShape)
                            .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                            .padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        if (post.pinned) {
                            Text(
                                text = "PINNED",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = accent
                            )
                        }
                        if (post.title.isNotBlank()) {
                            Text(
                                text = post.title,
                                style = MaterialTheme.typography.titleSmall,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                        if (post.body.isNotBlank()) {
                            Text(
                                text = post.body,
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        if (post.mediaUrl.isNotBlank()) {
                            AsyncImage(
                                model = post.mediaUrl,
                                contentDescription = null,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(160.dp)
                                    .clip(WebCardShape)
                            )
                        }
                        Text(
                            text = formatTimeAgo(post.createdAt),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorShowcaseBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Showcase" }, subtitle = block.subtitle) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (item.imageUrl.isNotBlank()) {
                        AsyncImage(
                            model = item.imageUrl,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(150.dp)
                                .clip(WebCardShape)
                        )
                    }
                    if (item.badge.isNotBlank()) {
                        Surface(shape = WebPillShape, color = accent) {
                            Text(
                                text = item.badge,
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.surface,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                            )
                        }
                    }
                    if (item.title.isNotBlank()) {
                        Text(item.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    }
                    if (item.subtitle.isNotBlank()) {
                        Text(
                            item.subtitle,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorGalleryBlock(block: ApiCreatorBlock, page: ApiCreatorPage) {
    if (block.images.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Gallery" }, subtitle = block.subtitle) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.images.chunked(2).forEach { row ->
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                    row.forEach { image ->
                        AsyncImage(
                            model = image,
                            contentDescription = null,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier
                                .weight(1f)
                                .height(130.dp)
                                .clip(WebCardShape)
                        )
                    }
                    if (row.size == 1) Spacer(Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun CreatorTestimonialsBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "What students say" }) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text(
                        text = "“${item.quote}”",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (item.avatarUrl.isNotBlank()) {
                            AsyncImage(
                                model = item.avatarUrl,
                                contentDescription = null,
                                contentScale = ContentScale.Crop,
                                modifier = Modifier
                                    .size(28.dp)
                                    .clip(CircleShape)
                            )
                        }
                        Column {
                            Text(
                                item.name,
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                color = accent
                            )
                            if (item.role.isNotBlank()) {
                                Text(
                                    item.role,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorFaqBlock(block: ApiCreatorBlock) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Questions" }) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            block.items.forEach { item ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .padding(14.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    Text(item.q, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                    Text(
                        item.a,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}

@Composable
private fun CreatorScheduleBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Schedule" }) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.items.forEach { item ->
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.Top,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Text(
                        text = listOf(item.day, item.time).filter { it.isNotBlank() }.joinToString(" · "),
                        style = MaterialTheme.typography.labelMedium,
                        color = accent,
                        modifier = Modifier.width(96.dp)
                    )
                    Column(modifier = Modifier.weight(1f)) {
                        Text(item.title, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
                        if (item.note.isNotBlank()) {
                            Text(
                                item.note,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorLinksBlock(block: ApiCreatorBlock, accent: Color) {
    if (block.items.isEmpty()) return
    CreatorBlockShell(title = block.title.ifBlank { "Links" }) {
        val context = LocalContext.current
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            block.items.forEach { item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(WebCardShape)
                        .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                        .clickable { openCreatorLink(context, item.url) }
                        .padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    Icon(
                        imageVector = getMaterialIcon(item.icon.ifBlank { "link" }),
                        contentDescription = null,
                        tint = accent,
                        modifier = Modifier.size(18.dp)
                    )
                    Text(
                        text = item.label.ifBlank { item.url },
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.weight(1f),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Icon(
                        imageVector = Icons.Outlined.OpenInNew,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun CreatorContactBlock(page: ApiCreatorPage, block: ApiCreatorBlock, accent: Color) {
    val rows = buildList {
        if (page.contactEmail.isNotBlank()) add("Email" to page.contactEmail)
        if (page.contactPhone.isNotBlank()) add("Phone" to page.contactPhone)
        page.socials.forEach { (key, value) ->
            if (value.isNotBlank()) add(key.replaceFirstChar { it.uppercase() } to value)
        }
    }
    CreatorBlockShell(title = block.title.ifBlank { "Get in touch" }, subtitle = block.subtitle) {
        if (block.body.isNotBlank()) {
            Text(block.body, style = MaterialTheme.typography.bodyMedium)
        }
        if (rows.isEmpty()) {
            Text(
                text = "No contact details published yet.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            val context = LocalContext.current
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                rows.forEach { (label, value) ->
                    val href = when (label.lowercase()) {
                        "email" -> "mailto:$value"
                        "phone" -> "tel:$value"
                        else -> value
                    }
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(WebCardShape)
                            .clickable { openCreatorLink(context, href) }
                            .padding(horizontal = 10.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelMedium,
                            color = accent,
                            modifier = Modifier.width(84.dp)
                        )
                        Text(
                            text = value,
                            style = MaterialTheme.typography.bodyMedium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun CreatorCtaBlock(block: ApiCreatorBlock, accent: Color, onJumpTo: (String) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 14.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(WebPanelShape)
                .background(MaterialTheme.colorScheme.surfaceContainerLowest)
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = block.title.ifBlank { "Ready to start?" },
                style = MaterialTheme.typography.titleMediumEmphasized,
                fontWeight = FontWeight.SemiBold,
                color = accent
            )
            if (block.subtitle.isNotBlank()) {
                Text(
                    text = block.subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            if (block.ctaLabel.isNotBlank()) {
                val context = LocalContext.current
                NebButton(
                    text = block.ctaLabel,
                    onClick = {
                        if (block.ctaUrl.startsWith("#")) {
                            onJumpTo(block.ctaUrl.removePrefix("#"))
                        } else {
                            openCreatorLink(context, block.ctaUrl)
                        }
                    },
                    tone = NebButtonTone.Primary,
                    size = NebButtonSize.Small,
                    icon = Icons.Outlined.OpenInNew
                )
            }
        }
    }
}
