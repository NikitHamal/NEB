package com.neb.ians.ui.screens.news

import android.content.Intent
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Visibility
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.neb.ians.data.news.NewsAnnouncement
import com.neb.ians.data.news.NewsComment
import com.neb.ians.data.news.toSafeColor
import com.neb.ians.ui.components.ErrorCard
import com.neb.ians.ui.components.NebCommentComposerBar
import com.neb.ians.ui.components.MarkdownText
import com.neb.ians.ui.components.WebCardShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.screens.home.NewsCategoryBadge
import com.neb.ians.ui.screens.home.newsIcon
import com.neb.ians.util.formatTimeAgo

@Composable
fun NewsDetailScreen(
    slug: String,
    onNavigateBack: () -> Unit,
    onRelatedNewsClick: (String) -> Unit = {},
    viewModel: NewsDetailViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val uriHandler = LocalUriHandler.current
    var showMoreMenu by remember { mutableStateOf(false) }
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(uiState.snackbarMessage) {
        val message = uiState.snackbarMessage ?: return@LaunchedEffect
        snackbarHostState.showSnackbar(message)
        viewModel.consumeSnackbar()
    }

    Scaffold(
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 4.dp, vertical = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
                Spacer(Modifier.weight(1f))
                uiState.detail?.let { detail ->
                    Box {
                        IconButton(onClick = { showMoreMenu = true }) {
                            Icon(Icons.Filled.MoreVert, contentDescription = "More")
                        }
                        DropdownMenu(
                            expanded = showMoreMenu,
                            onDismissRequest = { showMoreMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Share") },
                                onClick = {
                                    showMoreMenu = false
                                    val intent = Intent(Intent.ACTION_SEND).apply {
                                        type = "text/plain"
                                        putExtra(Intent.EXTRA_SUBJECT, detail.announcement.title)
                                        putExtra(Intent.EXTRA_TEXT, detail.announcement.url)
                                    }
                                    context.startActivity(Intent.createChooser(intent, "Share Post"))
                                },
                                leadingIcon = { Icon(Icons.Filled.Share, null) }
                            )
                        }
                    }
                }
            }
        },
        bottomBar = {
            if (uiState.detail != null) {
                NebCommentComposerBar(
                    value = uiState.commentDraft,
                    onValueChange = viewModel::onCommentDraftChange,
                    placeholder = "Join the discussion",
                    enabled = !uiState.isPostingComment,
                    canSend = uiState.commentDraft.isNotBlank(),
                    posting = uiState.isPostingComment,
                    onSend = viewModel::postComment
                )
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) },
        containerColor = MaterialTheme.colorScheme.surface
    ) { innerPadding ->
        when {
            uiState.isLoading -> {
                NewsDetailSkeleton(modifier = Modifier.padding(innerPadding))
            }
            uiState.error != null -> {
                ErrorCard(
                    message = uiState.error ?: "Couldn't load blog post",
                    onRetry = viewModel::retry,
                    modifier = Modifier
                        .padding(innerPadding)
                        .padding(16.dp)
                )
            }
            uiState.detail != null -> {
                val detail = uiState.detail!!
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                        .verticalScroll(rememberScrollState())
                ) {
                    NewsArticleHeader(item = detail.announcement)

                    if (detail.announcement.coverImageUrl.isNotBlank()) {
                        AsyncImage(
                            model = detail.announcement.coverImageUrl,
                            contentDescription = detail.announcement.title,
                            modifier = Modifier
                                .padding(horizontal = 16.dp)
                                .fillMaxWidth()
                                .aspectRatio(16f / 9f)
                                .clip(WebPillShape),
                            contentScale = ContentScale.Crop
                        )
                        Spacer(modifier = Modifier.height(18.dp))
                    }

                    MarkdownText(
                        markdown = detail.content.ifBlank { detail.announcement.summary.ifBlank { detail.announcement.title } },
                        modifier = Modifier.padding(horizontal = 16.dp),
                        style = MaterialTheme.typography.bodyLarge,
                        onLinkClick = { url -> safeOpenUri(uriHandler, context, url) }
                    )

                    Spacer(modifier = Modifier.height(16.dp))
                    HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(12.dp))

                    OutlinedButton(
                        onClick = {
                            val intent = Intent(Intent.ACTION_SEND).apply {
                                type = "text/plain"
                                putExtra(Intent.EXTRA_SUBJECT, detail.announcement.title)
                                putExtra(Intent.EXTRA_TEXT, detail.announcement.url)
                            }
                            context.startActivity(Intent.createChooser(intent, "Share Post"))
                        },
                        modifier = Modifier
                            .padding(horizontal = 16.dp)
                            .fillMaxWidth(),
                        shape = WebPillShape
                    ) {
                        Icon(Icons.Filled.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Share this article")
                    }

                    if (detail.externalUrl.isNotBlank()) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(
                            onClick = { safeOpenUri(uriHandler, context, detail.externalUrl) },
                            modifier = Modifier
                                .padding(horizontal = 16.dp)
                                .fillMaxWidth(),
                            shape = WebPillShape
                        ) {
                            Icon(Icons.Filled.OpenInNew, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("View Original Source")
                        }
                    }

                    Spacer(modifier = Modifier.height(28.dp))
                    BlogCommentsSection(
                        comments = uiState.comments,
                        isLoading = uiState.commentsLoading,
                        modifier = Modifier.padding(horizontal = 16.dp)
                    )

                    if (detail.related.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(28.dp))
                        Text(
                            text = "Related",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        detail.related.forEach { related ->
                            RelatedNewsCard(
                                item = related,
                                onClick = { onRelatedNewsClick(related.slug) },
                                modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}


@Composable
private fun BlogCommentsSection(
    comments: List<NewsComment>,
    isLoading: Boolean,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "Comments",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            Spacer(Modifier.width(8.dp))
            Surface(
                shape = WebPillShape,
                color = MaterialTheme.colorScheme.surfaceContainerHigh
            ) {
                Text(
                    text = comments.size.toString(),
                    style = MaterialTheme.typography.labelMedium,
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp)
                )
            }
        }
        Spacer(Modifier.height(12.dp))
        when {
            isLoading -> {
                repeat(2) {
                    Surface(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 5.dp),
                        shape = WebCardShape,
                        color = MaterialTheme.colorScheme.surfaceContainerLow
                    ) {
                        Row(modifier = Modifier.padding(14.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Box(
                                Modifier
                                    .size(38.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceContainerHighest)
                            )
                            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Box(Modifier.fillMaxWidth(0.35f).height(12.dp).clip(WebPillShape).background(MaterialTheme.colorScheme.surfaceContainerHighest))
                                Box(Modifier.fillMaxWidth().height(14.dp).clip(WebPillShape).background(MaterialTheme.colorScheme.surfaceContainerHighest))
                            }
                        }
                    }
                }
            }
            comments.isEmpty() -> {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = WebCardShape,
                    color = MaterialTheme.colorScheme.surfaceContainerLow,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
                ) {
                    Column(
                        modifier = Modifier.padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Icon(Icons.Outlined.Forum, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Text("No comments yet", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                        Text(
                            "Be the first NEBian to share a thought.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
            else -> comments.forEach { comment ->
                BlogCommentCard(comment = comment)
                Spacer(Modifier.height(10.dp))
            }
        }
    }
}

@Composable
private fun BlogCommentCard(comment: NewsComment) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebCardShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.Top
        ) {
            if (comment.authorPhoto.isNotBlank()) {
                AsyncImage(
                    model = comment.authorPhoto,
                    contentDescription = comment.authorName,
                    modifier = Modifier
                        .size(38.dp)
                        .clip(androidx.compose.foundation.shape.CircleShape),
                    contentScale = ContentScale.Crop
                )
            } else {
                Surface(
                    modifier = Modifier.size(38.dp),
                    shape = androidx.compose.foundation.shape.CircleShape,
                    color = MaterialTheme.colorScheme.primaryContainer
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Text(
                            comment.authorInitials.take(2),
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }
            }
            Column(Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(comment.authorName, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.width(8.dp))
                    Text(
                        formatTimeAgo(comment.createdAt),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Spacer(Modifier.height(5.dp))
                Text(comment.text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}

@Composable
private fun NewsArticleHeader(item: NewsAnnouncement) {
    val accent = remember(item.categoryColorHex) { item.categoryColorHex.toSafeColor() }
    Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 16.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
            NewsCategoryBadge(label = item.categoryLabel, icon = item.categoryIcon.newsIcon(), accent = accent)
            if (item.isPinned) {
                Surface(shape = WebPillShape, color = MaterialTheme.colorScheme.primary.copy(alpha = 0.10f)) {
                    Row(modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Filled.PushPin, contentDescription = null, modifier = Modifier.size(13.dp), tint = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Pinned", style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(14.dp))
        Text(item.title, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.onSurface)
        if (item.summary.isNotBlank()) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(item.summary, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, lineHeight = MaterialTheme.typography.bodyLarge.lineHeight)
        }
        Spacer(modifier = Modifier.height(14.dp))
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(item.authorName, style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold)
            Text("•", color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(item.publishedAgo.ifBlank { "Latest" }, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            if (item.viewCount.isNotBlank()) {
                Text("•", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Icon(Icons.Outlined.Visibility, contentDescription = null, modifier = Modifier.size(15.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("${item.viewCount} views", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun RelatedNewsCard(item: NewsAnnouncement, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val accent = remember(item.categoryColorHex) { item.categoryColorHex.toSafeColor() }
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clip(WebCardShape)
            .clickable(onClick = onClick),
        shape = WebCardShape,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(modifier = Modifier.padding(12.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(72.dp)
                    .clip(WebCardShape)
                    .background(Brush.linearGradient(listOf(accent.copy(alpha = 0.18f), accent.copy(alpha = 0.06f))))
            ) {
                Icon(item.categoryIcon.newsIcon(), contentDescription = null, modifier = Modifier.align(Alignment.Center).size(32.dp), tint = accent.copy(alpha = 0.8f))
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(item.title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                Spacer(modifier = Modifier.height(6.dp))
                Text(item.publishedAgo.ifBlank { item.categoryLabel }, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun NewsDetailSkeleton(modifier: Modifier = Modifier) {
    Column(modifier = modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        repeat(5) { index ->
            Box(
                modifier = Modifier
                    .fillMaxWidth(if (index == 0) 0.45f else 1f)
                    .height(if (index == 1) 34.dp else 18.dp)
                    .clip(WebPillShape)
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            )
        }
        HorizontalDivider()
        repeat(8) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(16.dp)
                    .clip(WebPillShape)
                    .background(MaterialTheme.colorScheme.surfaceContainerHigh)
            )
        }
    }
}

private fun safeOpenUri(uriHandler: androidx.compose.ui.platform.UriHandler, context: android.content.Context, url: String) {
    if (url.isBlank()) return
    val trimmed = url.trim()
    try {
        val uri = android.net.Uri.parse(trimmed)
        val scheme = uri.scheme?.lowercase() ?: ""
        if (scheme == "http" || scheme == "https") {
            uriHandler.openUri(trimmed)
        } else {
            val intent = Intent(Intent.ACTION_VIEW, uri).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            if (intent.resolveActivity(context.packageManager) != null) {
                context.startActivity(intent)
            } else {
                android.widget.Toast.makeText(context, "No app found to open link", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    } catch (e: Exception) {
        try {
            android.widget.Toast.makeText(context, "Invalid link", android.widget.Toast.LENGTH_SHORT).show()
        } catch (_: Exception) {}
    }
}
