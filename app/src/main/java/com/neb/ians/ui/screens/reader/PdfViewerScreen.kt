package com.neb.ians.ui.screens.reader

import android.graphics.Bitmap
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CloudDownload
import androidx.compose.material.icons.filled.ErrorOutline
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebTopBar
import com.neb.ians.ui.components.NebButton
import com.neb.ians.ui.components.NebButtonSize
import com.neb.ians.ui.components.NebButtonTone
import com.neb.ians.ui.components.NebLoader

@Composable
fun PdfViewerScreen(
    onNavigateBack: () -> Unit,
    viewModel: PdfViewerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Box(Modifier.fillMaxSize()) {
        Scaffold(
            topBar = {
                NebTopBar(
                    showBrand = false,
                    title = uiState.title.ifBlank { "Document" },
                    titleFontWeight = FontWeight.Normal,
                    onBack = onNavigateBack
                )
            }
        ) { padding ->
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .background(MaterialTheme.colorScheme.surfaceVariant)
            ) {
                when {
                    uiState.isDownloading -> {
                        InternalDownloadState(
                            progress = uiState.downloadProgress,
                            modifier = Modifier.align(Alignment.Center)
                        )
                    }
                    uiState.isLoading -> NebLoader(modifier = Modifier.align(Alignment.Center))
                    uiState.error != null -> {
                        PdfErrorState(
                            message = uiState.error ?: "Unable to open document",
                            onRetry = viewModel::retry,
                            modifier = Modifier.align(Alignment.Center)
                        )
                    }
                    else -> {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(12.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            items((0 until uiState.pageCount).toList()) { index ->
                                PdfPage(index = index, render = viewModel::renderPage)
                            }
                        }
                    }
                }
            }
        }

        if (uiState.isLocalFileReady) {
            PdfAssistantOverlay(
                documentTitle = uiState.title,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

@Composable
private fun PdfPage(index: Int, render: suspend (Int) -> Bitmap?) {
    val bitmap by produceState<Bitmap?>(initialValue = null, index) {
        value = render(index)
    }
    Surface(
        tonalElevation = 1.dp,
        shadowElevation = 2.dp,
        color = androidx.compose.ui.graphics.Color.White,
        modifier = Modifier.fillMaxWidth()
    ) {
        val page = bitmap
        if (page != null) {
            Image(
                bitmap = page.asImageBitmap(),
                contentDescription = "Page ${index + 1}",
                contentScale = ContentScale.FillWidth,
                modifier = Modifier.fillMaxWidth()
            )
        } else {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(420.dp),
                contentAlignment = Alignment.Center
            ) {
                NebLoader()
            }
        }
    }
}

@Composable
private fun InternalDownloadState(progress: Int, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Icon(
            Icons.Filled.CloudDownload,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.primary
        )
        Text("Preparing for offline reading", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
        LinearProgressIndicator(
            progress = { progress.coerceIn(0, 100) / 100f },
            modifier = Modifier.fillMaxWidth()
        )
        Text("$progress% read, saved only inside NEBians", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}

@Composable
private fun PdfErrorState(message: String, onRetry: () -> Unit, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Icon(Icons.Filled.ErrorOutline, contentDescription = null, tint = MaterialTheme.colorScheme.error)
        Text(message, style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant)
        NebButton(text = "Try again", onClick = onRetry)
    }
}
