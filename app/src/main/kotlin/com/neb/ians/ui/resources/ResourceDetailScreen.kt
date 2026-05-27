package com.neb.ians.ui.resources

import android.content.Intent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Bookmark
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.Download
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject
import com.neb.ians.ui.pdf.PdfViewerActivity

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResourceDetailScreen(
    resourceId: String,
    onBack: () -> Unit,
    vm: ResourceDetailViewModel = hiltViewModel(),
) {
    val ui by vm.uiState.collectAsStateWithLifecycle()
    val ctx = LocalContext.current

    androidx.compose.runtime.LaunchedEffect(resourceId) { vm.load(resourceId) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Details") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { vm.toggleFavorite() }) {
                        Icon(
                            if (ui.resource?.isFavorite == true) Icons.Outlined.Bookmark else Icons.Outlined.BookmarkBorder,
                            contentDescription = "Bookmark",
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        val r = ui.resource ?: return@Scaffold
        Column(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = MaterialTheme.colorScheme.surfaceVariant,
                tonalElevation = 0.dp,
            ) {
                Row(modifier = Modifier.padding(16.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Outlined.MenuBook, contentDescription = null, modifier = Modifier.size(36.dp), tint = MaterialTheme.colorScheme.primary)
                    Column(modifier = Modifier.padding(start = 12.dp).weight(1f)) {
                        Text(r.title, style = MaterialTheme.typography.titleMedium)
                        r.author?.let { Text(it, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant) }
                    }
                }
            }

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AssistChip(onClick = {}, label = { Text(Subject.fromName(r.subject)?.display ?: r.subject) })
                AssistChip(onClick = {}, label = { Text(Grade.fromName(r.grade)?.display ?: r.grade) })
                AssistChip(onClick = {}, label = { Text(ResourceType.fromName(r.type)?.display ?: r.type) })
            }

            Text(r.description, style = MaterialTheme.typography.bodyMedium)

            if (ui.downloading && ui.progress in 0f..1f) {
                LinearProgressIndicator(
                    progress = { ui.progress },
                    modifier = Modifier.fillMaxWidth(),
                )
                Text("Downloading… ${(ui.progress * 100).toInt()}%", style = MaterialTheme.typography.labelMedium)
            }

            if (r.localPath != null) {
                Button(
                    onClick = {
                        ctx.startActivity(
                            Intent(ctx, PdfViewerActivity::class.java).apply {
                                putExtra(PdfViewerActivity.EXTRA_RESOURCE_ID, r.id)
                                putExtra(PdfViewerActivity.EXTRA_LOCAL_PATH, r.localPath)
                                putExtra(PdfViewerActivity.EXTRA_TITLE, r.title)
                            }
                        )
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp),
                ) { Text("Open PDF") }
            } else {
                FilledTonalButton(
                    onClick = { vm.download() },
                    enabled = !ui.downloading,
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp),
                ) {
                    Icon(Icons.Outlined.Download, contentDescription = null)
                    Text("  Download for offline", style = MaterialTheme.typography.labelLarge)
                }
            }

            if (ui.error != null) {
                Text(ui.error!!, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}
