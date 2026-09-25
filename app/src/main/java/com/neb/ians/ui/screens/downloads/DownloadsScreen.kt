package com.neb.ians.ui.screens.downloads

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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.AudioFile
import androidx.compose.material.icons.outlined.DeleteOutline
import androidx.compose.material.icons.outlined.DownloadDone
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.PlayCircleOutline
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.background
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebEmptyState
import com.neb.ians.ui.components.NebIconButton
import com.neb.ians.ui.components.nebPressable
import com.neb.ians.util.DownloadedResource
import com.neb.ians.util.TactileType
import java.text.DateFormat
import java.util.Date

// ---------------------------------------------------------------------------
// Downloads.
//
// Files already on the phone: a glyph for what kind, the name they were saved
// under, how big they are and when they arrived. No cards — a card per file
// made a short list look like a long one.
// ---------------------------------------------------------------------------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DownloadsScreen(
    onNavigateBack: () -> Unit,
    onOpenPdf: (String) -> Unit,
    onOpenMedia: (String) -> Unit,
    viewModel: DownloadsViewModel = hiltViewModel()
) {
    val downloads by viewModel.downloads.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Downloads", fontWeight = FontWeight.SemiBold)
                        Text(
                            text = savedLabel(downloads.size),
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        if (downloads.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                NebEmptyState(
                    icon = Icons.Outlined.DownloadDone,
                    title = "No offline resources",
                    subtitle = "Downloaded videos, audio and PDFs stay private inside NEBians."
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentPadding = PaddingValues(bottom = 16.dp)
            ) {
                itemsIndexed(downloads, key = { _, item -> item.resourceId }) { index, item ->
                    DownloadRow(
                        item = item,
                        onOpen = {
                            if (item.isPdf()) onOpenPdf(item.resourceId) else onOpenMedia(item.resourceId)
                        },
                        onDelete = { viewModel.delete(item.resourceId) },
                        showDivider = index < downloads.lastIndex
                    )
                }
            }
        }
    }
}

@Composable
private fun DownloadRow(
    item: DownloadedResource,
    onOpen: () -> Unit,
    onDelete: () -> Unit,
    showDivider: Boolean
) {
    val scheme = MaterialTheme.colorScheme

    Column(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .nebPressable(scale = 0.985f, tactile = TactileType.ButtonTap, onClick = onOpen)
                .padding(horizontal = 20.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(RoundedCornerShape(13.dp))
                    .background(scheme.surfaceContainerHigh),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = when {
                        item.isPdf() -> Icons.Outlined.PictureAsPdf
                        item.isAudio() -> Icons.Outlined.AudioFile
                        else -> Icons.Outlined.PlayCircleOutline
                    },
                    contentDescription = null,
                    tint = scheme.onSurfaceVariant,
                    modifier = Modifier.size(19.dp)
                )
            }

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold,
                    color = scheme.onSurface,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(3.dp))
                Text(
                    text = "${formatBytes(item.sizeBytes)} · " +
                        DateFormat.getDateInstance(DateFormat.MEDIUM).format(Date(item.downloadedAt)),
                    style = MaterialTheme.typography.labelMedium,
                    color = scheme.onSurfaceVariant,
                    maxLines = 1
                )
            }

            NebIconButton(
                icon = Icons.Outlined.DeleteOutline,
                contentDescription = "Delete download",
                onClick = onDelete,
                tint = scheme.onSurfaceVariant,
                size = 34.dp
            )
        }

        if (showDivider) {
            HorizontalDivider(
                color = scheme.outlineVariant.copy(alpha = 0.5f),
                modifier = Modifier.padding(start = 74.dp)
            )
        }
    }
}

private fun savedLabel(count: Int): String = when (count) {
    0 -> "Nothing downloaded"
    1 -> "1 file"
    else -> "$count files"
}

private fun DownloadedResource.isPdf(): Boolean =
    mimeType.contains("pdf", true) || type.contains("pdf", true) || localPath.endsWith(".pdf", true)

private fun DownloadedResource.isAudio(): Boolean =
    mimeType.startsWith("audio/") || type.contains("audio", true)

private fun formatBytes(bytes: Long): String = when {
    bytes >= 1024L * 1024L * 1024L -> "%.1f GB".format(bytes / (1024f * 1024f * 1024f))
    bytes >= 1024L * 1024L -> "%.1f MB".format(bytes / (1024f * 1024f))
    bytes >= 1024L -> "%.1f KB".format(bytes / 1024f)
    else -> "$bytes B"
}
