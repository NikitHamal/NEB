package com.neb.ians.ui.screens.reader

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiResource
import com.neb.ians.ui.components.ResourceArt
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPillShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebSectionHeader
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.compactCount
import com.neb.ians.ui.components.fileSizeLabel
import com.neb.ians.ui.theme.getSubjectTheme
import com.neb.ians.util.formatTimeAgo

@Composable
fun PdfReaderScreen(
    resourceId: String,
    onNavigateBack: () -> Unit,
    viewModel: ReaderViewModel = hiltViewModel()
) {
    val pageState by viewModel.pageState.collectAsStateWithLifecycle()
    val uriHandler = LocalUriHandler.current

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Resource",
                subtitle = pageState.resource?.title,
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = {},
                onNotificationsClick = {},
                onProfileClick = {}
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            when {
                pageState.isLoading && pageState.resource == null -> {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(260.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator()
                    }
                }
                pageState.resource == null && pageState.error != null -> {
                    WebEmptyState(
                        title = "Resource unavailable",
                        message = pageState.error ?: "Could not load this resource.",
                        icon = painterResource(id = R.drawable.ic_document),
                        modifier = Modifier.padding(16.dp)
                    )
                }
                pageState.resource != null -> {
                    val resource = pageState.resource!!
                    ResourceDetailHero(
                        resource = resource,
                        onView = {
                            resource.fileUrl.takeIf { it.isNotBlank() }?.let(uriHandler::openUri)
                        },
                        onDownload = {
                            if (resource.fileUrl.isNotBlank()) uriHandler.openUri(resource.fileUrl)
                        },
                        onLike = viewModel::toggleResourceLike,
                        onBookmark = viewModel::toggleResourceBookmark
                    )

                    MinimalPdfPreview(
                        state = pageState,
                        onDownload = viewModel::downloadResource,
                        onCancelDownload = viewModel::cancelDownload,
                        onPrevious = viewModel::previousPage,
                        onNext = viewModel::nextPage
                    )

                    WebSectionHeader(title = "Comments")
                    WebEmptyState(
                        title = "Comments are available on the web",
                        message = "The Android resource page now mirrors the web detail layout. Full threaded resource comments can be expanded in a later native pass.",
                        icon = painterResource(id = R.drawable.ic_forum_outlined),
                        modifier = Modifier.padding(horizontal = 16.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
private fun ResourceDetailHero(
    resource: ApiResource,
    onView: () -> Unit,
    onDownload: () -> Unit,
    onLike: () -> Unit,
    onBookmark: () -> Unit
) {
    val subjects = resource.subject.split(",").map { it.trim() }.filter { it.isNotBlank() }.ifEmpty { listOf("General") }
    val mainSubject = subjects.first()
    val subjectTheme = getSubjectTheme(mainSubject)

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 14.dp),
        shape = RoundedCornerShape(8.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Box {
            ResourceArt(
                primary = subjectTheme.color,
                container = MaterialTheme.colorScheme.surfaceContainerLowest,
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .width(220.dp)
                    .height(180.dp)
            )
            Column(modifier = Modifier.padding(18.dp)) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    subjects.forEach { subject ->
                        WebChip(text = subject, selected = false)
                    }
                    WebChip(text = resource.type.ifBlank { "Resource" }, selected = false)
                    WebChip(text = resource.gradeLevel.ifBlank { "General" }, selected = false)
                }
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = resource.title,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(10.dp))
                ResourceMeta(resource = resource)
                if (resource.description.isNotBlank()) {
                    Spacer(modifier = Modifier.height(14.dp))
                    Text(
                        text = resource.description,
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 8,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                Spacer(modifier = Modifier.height(16.dp))
                Spacer(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(1.dp)
                        .background(MaterialTheme.colorScheme.outlineVariant)
                )
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (resource.fileUrl.isNotBlank()) {
                        WebPrimaryButton(
                            text = "View ${resource.type.ifBlank { "File" }}",
                            painter = painterResource(id = R.drawable.ic_document),
                            onClick = onView
                        )
                        WebOutlinedButton(
                            text = "Download",
                            painter = painterResource(id = R.drawable.ic_download),
                            onClick = onDownload
                        )
                    }
                    ResourceAction(
                        text = compactCount(resource.likeCount),
                        selected = resource.isLiked == true,
                        icon = {
                            Icon(
                                imageVector = Icons.Outlined.ThumbUp,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp)
                            )
                        },
                        onClick = onLike
                    )
                    ResourceAction(
                        text = if (resource.isBookmarked == true) "Saved" else "Save",
                        selected = resource.isBookmarked == true,
                        icon = {
                            Icon(
                                painter = painterResource(id = R.drawable.ic_bookmark),
                                contentDescription = null,
                                modifier = Modifier.size(18.dp)
                            )
                        },
                        onClick = onBookmark
                    )
                }
            }
        }
    }
}

@Composable
private fun ResourceMeta(resource: ApiResource) {
    val fileSize = fileSizeLabel(resource.fileSize)
    val source = when (resource.sourceType) {
        "user" -> resource.authorName ?: "Community"
        "anonymous" -> "Anonymous"
        "external" -> resource.sourceLabel ?: "External Source"
        else -> resource.authorName ?: "NEBians Team"
    }
    val parts = buildList {
        add(source)
        if (resource.addedAt > 0) add(formatTimeAgo(resource.addedAt))
        add("${compactCount(resource.viewCount)} views")
        if (fileSize.isNotBlank()) add(fileSize)
    }
    Text(
        text = parts.joinToString(" - "),
        style = MaterialTheme.typography.labelMedium,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
        maxLines = 3,
        overflow = TextOverflow.Ellipsis
    )
}

@Composable
private fun ResourceAction(
    text: String,
    selected: Boolean,
    icon: @Composable () -> Unit,
    onClick: () -> Unit
) {
    OutlinedButton(
        onClick = onClick,
        shape = WebPillShape,
        border = BorderStroke(
            1.dp,
            if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant
        ),
        colors = ButtonDefaults.outlinedButtonColors(
            contentColor = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
        )
    ) {
        icon()
        Spacer(modifier = Modifier.width(6.dp))
        Text(text = text, maxLines = 1)
    }
}

@Composable
private fun MinimalPdfPreview(
    state: ReaderPageState,
    onDownload: () -> Unit,
    onCancelDownload: () -> Unit,
    onPrevious: () -> Unit,
    onNext: () -> Unit
) {
    WebSectionHeader(title = "Preview")
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        shape = RoundedCornerShape(8.dp),
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        when {
            state.needsDownload && !state.isDownloading -> {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_document),
                        contentDescription = null,
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(
                        text = "Download for native PDF preview",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(6.dp))
                    Text(
                        text = "The detail page works without the file. Download only when you want the simple page preview.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    WebPrimaryButton(
                        text = "Download PDF",
                        painter = painterResource(id = R.drawable.ic_download),
                        onClick = onDownload
                    )
                }
            }
            state.isDownloading -> {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    CircularProgressIndicator()
                    Spacer(modifier = Modifier.height(14.dp))
                    Text(
                        text = "Downloading ${state.downloadProgress}%",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(10.dp))
                    LinearProgressIndicator(
                        progress = { state.downloadProgress / 100f },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(8.dp)
                            .clip(WebPillShape)
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    WebOutlinedButton(text = "Cancel", onClick = onCancelDownload)
                }
            }
            state.pageBitmap != null -> {
                Column {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 360.dp, max = 640.dp)
                            .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                        contentAlignment = Alignment.Center
                    ) {
                        Image(
                            bitmap = state.pageBitmap.asImageBitmap(),
                            contentDescription = "Page ${state.currentPage + 1}",
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(0.707f)
                                .padding(10.dp),
                            contentScale = ContentScale.Fit
                        )
                    }
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        WebOutlinedButton(
                            text = "Prev",
                            imageVector = Icons.Filled.KeyboardArrowUp,
                            onClick = onPrevious
                        )
                        Text(
                            text = "Page ${state.currentPage + 1} of ${state.totalPages.coerceAtLeast(1)}",
                            style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 1
                        )
                        WebOutlinedButton(
                            text = "Next",
                            imageVector = Icons.Filled.KeyboardArrowDown,
                            onClick = onNext
                        )
                    }
                }
            }
            state.error != null -> {
                WebEmptyState(
                    title = "Preview unavailable",
                    message = state.error,
                    icon = painterResource(id = R.drawable.ic_document)
                )
            }
            else -> {
                WebEmptyState(
                    title = "No native preview",
                    message = "Use View File to open this resource in the best available viewer.",
                    icon = painterResource(id = R.drawable.ic_document)
                )
            }
        }
    }
}
