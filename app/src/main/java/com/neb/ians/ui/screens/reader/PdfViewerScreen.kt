package com.neb.ians.ui.screens.reader

import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.components.NebTopBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfViewerScreen(
    onNavigateBack: () -> Unit,
    viewModel: PdfViewerViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    var showMenu by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            NebTopBar(
                showBrand = false,
                title = uiState.title.ifBlank { "Document" },
                titleFontWeight = androidx.compose.ui.text.font.FontWeight.Normal,
                onBack = onNavigateBack,
                actions = {
                    if (uiState.isLocalFileReady) {
                        Box {
                            IconButton(onClick = { showMenu = true }) {
                                Icon(Icons.Filled.MoreVert, contentDescription = "More options")
                            }
                            DropdownMenu(
                                expanded = showMenu,
                                onDismissRequest = { showMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Open in...") },
                                    onClick = {
                                        showMenu = false
                                        val localFile = viewModel.getLocalFile()
                                        if (localFile != null && localFile.exists()) {
                                            runCatching {
                                                val authority = "${context.packageName}.fileprovider"
                                                val uri = androidx.core.content.FileProvider.getUriForFile(context, authority, localFile)
                                                val intent = Intent(Intent.ACTION_VIEW).apply {
                                                    setDataAndType(uri, "application/pdf")
                                                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                                                }
                                                context.startActivity(Intent.createChooser(intent, "Open PDF with"))
                                            }.onFailure { e ->
                                                android.widget.Toast.makeText(context, "Cannot open: ${e.message}", android.widget.Toast.LENGTH_SHORT).show()
                                            }
                                        } else {
                                            android.widget.Toast.makeText(context, "File not available locally", android.widget.Toast.LENGTH_SHORT).show()
                                        }
                                    },
                                    leadingIcon = {
                                        Icon(
                                            Icons.Filled.OpenInNew,
                                            contentDescription = null
                                        )
                                    }
                                )
                            }
                        }
                    }
                }
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
                uiState.isLoading -> {
                    CircularProgressIndicator(Modifier.align(Alignment.Center))
                }
                uiState.needsDownload -> {
                    DownloadPrompt(
                        isDownloading = uiState.isDownloading,
                        progress = uiState.downloadProgress,
                        onDownload = { viewModel.download() },
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                uiState.error != null -> {
                    ErrorState(
                        message = uiState.error ?: "Unable to open document",
                        onOpenExternal = {
                            val url = viewModel.fileUrl()
                            if (url.isNotBlank()) {
                                runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) }
                            }
                        },
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
        val bmp = bitmap
        if (bmp != null) {
            Image(
                bitmap = bmp.asImageBitmap(),
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
                CircularProgressIndicator(strokeWidth = 2.dp)
            }
        }
    }
}

@Composable
private fun DownloadPrompt(
    isDownloading: Boolean,
    progress: Int,
    onDownload: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Icon(
            Icons.Filled.Download,
            contentDescription = null,
            modifier = Modifier.size(48.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Text(
            "This document needs to be downloaded before viewing.",
            style = MaterialTheme.typography.bodyMedium,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        if (isDownloading) {
            LinearProgressIndicator(
                progress = { progress / 100f },
                modifier = Modifier.fillMaxWidth()
            )
            Text("$progress%", style = MaterialTheme.typography.labelMedium)
        } else {
            Button(onClick = onDownload) {
                Icon(Icons.Filled.Download, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Download")
            }
        }
    }
}

@Composable
private fun ErrorState(
    message: String,
    onOpenExternal: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            message,
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        OutlinedButton(onClick = onOpenExternal) {
            Icon(Icons.Filled.OpenInNew, contentDescription = null)
            Spacer(Modifier.width(8.dp))
            Text("Open in browser")
        }
    }
}
