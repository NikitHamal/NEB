package com.neb.ians.ui.screens.reader

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.expandVertically
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.Delete
import androidx.compose.ui.res.painterResource
import com.neb.ians.R
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.neb.ians.data.local.entity.AnnotationEntity

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PdfReaderScreen(
    resourceId: String,
    onNavigateBack: () -> Unit,
    viewModel: ReaderViewModel = hiltViewModel()
) {
    val pageState by viewModel.pageState.collectAsState()
    val annotationState by viewModel.annotationState.collectAsState()
    val dialogState by viewModel.dialogState.collectAsState()
    val bookmarksState by viewModel.bookmarksState.collectAsState()

    var showOverflowMenu by remember { mutableStateOf(false) }
    var showPageJumpDialog by remember { mutableStateOf(false) }
    var showBookmarkListDialog by remember { mutableStateOf(false) }
    var pageJumpText by remember { mutableStateOf("") }
    var bookmarkTitle by remember { mutableStateOf("") }
    var annotationsExpanded by remember { mutableStateOf(false) }

    val currentPageAnnotations = remember(annotationState.annotations, pageState.currentPage) {
        annotationState.annotations.filter { it.page == pageState.currentPage }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = pageState.resource?.title ?: "PDF Reader",
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                actions = {
                    Box {
                        IconButton(onClick = { showOverflowMenu = true }) {
                            Icon(
                                imageVector = Icons.Filled.MoreVert,
                                contentDescription = "More options"
                            )
                        }
                        DropdownMenu(
                            expanded = showOverflowMenu,
                            onDismissRequest = { showOverflowMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Add Bookmark") },
                                leadingIcon = {
                                    Icon(
                                        painter = painterResource(id = R.drawable.ic_bookmark),
                                        contentDescription = null
                                    )
                                },
                                onClick = {
                                    showOverflowMenu = false
                                    bookmarkTitle = "Page ${pageState.currentPage + 1}"
                                    viewModel.showBookmarkDialog(true)
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("View Bookmarks") },
                                leadingIcon = {
                                    Icon(
                                        painter = painterResource(id = R.drawable.ic_bookmark),
                                        contentDescription = null
                                    )
                                },
                                onClick = {
                                    showOverflowMenu = false
                                    showBookmarkListDialog = true
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Jump to Page") },
                                leadingIcon = {
                                    Icon(
                                        painter = painterResource(id = R.drawable.ic_document),
                                        contentDescription = null
                                    )
                                },
                                onClick = {
                                    showOverflowMenu = false
                                    pageJumpText = ""
                                    showPageJumpDialog = true
                                }
                            )
                            DropdownMenuItem(
                                text = {
                                    Text(
                                        if (annotationState.showAnnotationTools) "Hide Annotations"
                                        else "Show Annotations"
                                    )
                                },
                                leadingIcon = {
                                    Icon(
                                        imageVector = Icons.Filled.Edit,
                                        contentDescription = null
                                    )
                                },
                                onClick = {
                                    showOverflowMenu = false
                                    viewModel.toggleAnnotationTools()
                                }
                            )
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        containerColor = MaterialTheme.colorScheme.surfaceContainerLowest
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {
                when {
                    pageState.needsDownload && !pageState.isDownloading && pageState.downloadProgress < 100 -> {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(MaterialTheme.colorScheme.surfaceContainerLowest),
                            contentAlignment = Alignment.Center
                        ) {
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(24.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceContainer
                                ),
                                shape = RoundedCornerShape(16.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(32.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.Center
                                ) {
                                    Icon(
                                        painter = painterResource(id = R.drawable.ic_document),
                                        contentDescription = null,
                                        modifier = Modifier.size(72.dp),
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text = pageState.resource?.title ?: "Document",
                                        style = MaterialTheme.typography.titleLarge,
                                        textAlign = TextAlign.Center,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                    Spacer(modifier = Modifier.height(8.dp))
                                    Text(
                                        text = "This PDF needs to be downloaded before viewing.",
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        textAlign = TextAlign.Center
                                    )
                                    Spacer(modifier = Modifier.height(24.dp))
                                    Button(
                                        onClick = { viewModel.downloadResource() },
                                        modifier = Modifier.fillMaxWidth(),
                                        shape = RoundedCornerShape(12.dp)
                                    ) {
                                        Icon(
                                            painter = painterResource(id = R.drawable.ic_download),
                                            contentDescription = null,
                                            modifier = Modifier.size(18.dp)
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text("Download PDF")
                                    }
                                }
                            }
                        }
                    }
                    pageState.isDownloading -> {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(MaterialTheme.colorScheme.surfaceContainerLowest),
                            contentAlignment = Alignment.Center
                        ) {
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(24.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceContainer
                                ),
                                shape = RoundedCornerShape(16.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(32.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.Center
                                ) {
                                    CircularProgressIndicator(
                                        modifier = Modifier.size(48.dp)
                                    )
                                    Spacer(modifier = Modifier.height(16.dp))
                                    Text(
                                        text = "Downloading...",
                                        style = MaterialTheme.typography.titleMedium,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                    Spacer(modifier = Modifier.height(8.dp))
                                    LinearProgressIndicator(
                                        progress = { pageState.downloadProgress / 100f },
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(vertical = 8.dp)
                                            .height(8.dp)
                                            .clip(RoundedCornerShape(4.dp)),
                                    )
                                    Text(
                                        text = "${pageState.downloadProgress}%",
                                        style = MaterialTheme.typography.bodyMedium,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                    Spacer(modifier = Modifier.height(16.dp))
                                    OutlinedButton(
                                        onClick = { viewModel.cancelDownload() },
                                        modifier = Modifier.fillMaxWidth(),
                                        shape = RoundedCornerShape(12.dp)
                                    ) {
                                        Text("Cancel")
                                    }
                                }
                            }
                        }
                    }
                    pageState.isLoading -> {
                        CircularProgressIndicator(
                            modifier = Modifier.align(Alignment.Center)
                        )
                    }
                    pageState.error != null -> {
                        Column(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .padding(32.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(
                                imageVector = Icons.Filled.Warning,
                                contentDescription = null,
                                modifier = Modifier.size(64.dp),
                                tint = MaterialTheme.colorScheme.error
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Text(
                                text = pageState.error ?: "Unknown error",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                textAlign = TextAlign.Center
                            )
                        }
                    }
                    pageState.pageBitmap != null -> {
                        Image(
                            bitmap = pageState.pageBitmap!!.asImageBitmap(),
                            contentDescription = "Page ${pageState.currentPage + 1}",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Fit
                        )
                    }
                    else -> {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(MaterialTheme.colorScheme.surfaceContainerHigh),
                            contentAlignment = Alignment.Center
                        ) {
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(24.dp)
                                    .aspectRatio(0.707f),
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surface
                                ),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .padding(32.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally,
                                    verticalArrangement = Arrangement.Center
                                ) {
                                    Icon(
                                        painter = painterResource(id = R.drawable.ic_document),
                                        contentDescription = null,
                                        modifier = Modifier.size(72.dp),
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                    Spacer(modifier = Modifier.height(24.dp))
                                    Text(
                                        text = pageState.resource?.title ?: "Document",
                                        style = MaterialTheme.typography.titleLarge,
                                        textAlign = TextAlign.Center,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )
                                    Spacer(modifier = Modifier.height(12.dp))
                                    Text(
                                        text = "Page ${pageState.currentPage + 1}",
                                        style = MaterialTheme.typography.bodyLarge,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                            }
                        }
                    }
                }

                if (!pageState.isLoading && pageState.error == null) {
                    AnnotationOverlay(
                        annotations = currentPageAnnotations,
                        annotationMode = annotationState.annotationMode,
                        onAnnotationCreated = { startX, startY, endX, endY ->
                            if (annotationState.annotationMode == AnnotationMode.STICKY_NOTE) {
                                viewModel.prepareStickyNote(startX, startY, endX, endY)
                            } else {
                                viewModel.addAnnotation(startX, startY, endX, endY)
                            }
                        },
                        onAnnotationTapped = { annotation ->
                            viewModel.deleteAnnotation(annotation.id)
                        },
                        modifier = Modifier.fillMaxSize()
                    )
                }
            }

            if (currentPageAnnotations.isNotEmpty()) {
                Surface(
                    tonalElevation = 1.dp,
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceContainer
                ) {
                    Column {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { annotationsExpanded = !annotationsExpanded }
                                .padding(horizontal = 16.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = "${currentPageAnnotations.size} annotation(s) on this page",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                            Icon(
                                imageVector = if (annotationsExpanded)
                                    Icons.Filled.KeyboardArrowUp else Icons.Filled.KeyboardArrowDown,
                                contentDescription = if (annotationsExpanded)
                                    "Collapse" else "Expand",
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        AnimatedVisibility(
                            visible = annotationsExpanded,
                            enter = expandVertically(),
                            exit = shrinkVertically()
                        ) {
                            LazyColumn(
                                modifier = Modifier.heightIn(max = 150.dp)
                            ) {
                                items(
                                    items = currentPageAnnotations,
                                    key = { it.id }
                                ) { annotation ->
                                    AnnotationListItem(
                                        annotation = annotation,
                                        onDelete = { viewModel.deleteAnnotation(annotation.id) }
                                    )
                                }
                            }
                        }
                    }
                }
            }

            AnimatedVisibility(
                visible = annotationState.showAnnotationTools,
                enter = expandVertically(),
                exit = shrinkVertically()
            ) {
                Surface(
                    tonalElevation = 2.dp,
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceContainer
                ) {
                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            IconToggleButton(
                                checked = annotationState.annotationMode == AnnotationMode.HIGHLIGHT,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.HIGHLIGHT)
                                }
                            ) {
                                Icon(
                                    painter = painterResource(id = R.drawable.ic_pen),
                                    contentDescription = "Highlight",
                                    tint = if (annotationState.annotationMode == AnnotationMode.HIGHLIGHT)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            IconToggleButton(
                                checked = annotationState.annotationMode == AnnotationMode.UNDERLINE,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.UNDERLINE)
                                }
                            ) {
                                Icon(
                                    painter = painterResource(id = R.drawable.ic_pen),
                                    contentDescription = "Underline",
                                    tint = if (annotationState.annotationMode == AnnotationMode.UNDERLINE)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            IconToggleButton(
                                checked = annotationState.annotationMode == AnnotationMode.STICKY_NOTE,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.STICKY_NOTE)
                                }
                            ) {
                                Icon(
                                    painter = painterResource(id = R.drawable.ic_pen),
                                    contentDescription = "Sticky Note",
                                    tint = if (annotationState.annotationMode == AnnotationMode.STICKY_NOTE)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val colors = listOf(
                                0xFFFFEB3B.toInt(),
                                0xFF4CAF50.toInt(),
                                0xFF2196F3.toInt(),
                                0xFFE91E63.toInt(),
                                0xFFFF9800.toInt()
                            )
                            colors.forEach { color ->
                                val isSelected = annotationState.selectedColor == color
                                Box(
                                    modifier = Modifier
                                        .size(28.dp)
                                        .clip(CircleShape)
                                        .background(Color(color))
                                        .then(
                                            if (isSelected) {
                                                Modifier.border(
                                                    width = 3.dp,
                                                    color = MaterialTheme.colorScheme.onSurface,
                                                    shape = CircleShape
                                                )
                                            } else {
                                                Modifier.border(
                                                    width = 1.dp,
                                                    color = MaterialTheme.colorScheme.outline
                                                        .copy(alpha = 0.3f),
                                                    shape = CircleShape
                                                )
                                            }
                                        )
                                        .clickable { viewModel.setSelectedColor(color) }
                                )
                            }
                        }
                    }
                }
            }

            Surface(
                tonalElevation = 1.dp,
                modifier = Modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.surfaceContainer
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    IconButton(
                        onClick = { viewModel.previousPage() },
                        enabled = pageState.currentPage > 0
                    ) {
                        Icon(
                            painter = painterResource(id = R.drawable.ic_chevron_left),
                            contentDescription = "Previous page"
                        )
                    }

                    Text(
                        text = if (pageState.totalPages > 0) {
                            "Page ${pageState.currentPage + 1} of ${pageState.totalPages}"
                        } else {
                            "No pages"
                        },
                        style = MaterialTheme.typography.bodyMedium
                    )

                    IconButton(
                        onClick = { viewModel.nextPage() },
                        enabled = pageState.currentPage < pageState.totalPages - 1
                    ) {
                        Icon(
                            painter = painterResource(id = R.drawable.ic_chevron_right),
                            contentDescription = "Next page"
                        )
                    }
                }
            }
        }
    }

    if (dialogState.showStickyNoteDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.showStickyNoteDialog(false) },
            title = { Text("Add Sticky Note") },
            text = {
                OutlinedTextField(
                    value = dialogState.stickyNoteText,
                    onValueChange = { viewModel.onStickyNoteTextChange(it) },
                    label = { Text("Note") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 120.dp),
                    placeholder = { Text("Enter your note...") },
                    shape = RoundedCornerShape(12.dp),
                    maxLines = 6
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.savePendingStickyNote()
                    }
                ) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        viewModel.cancelStickyNote()
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }

    if (dialogState.showBookmarkDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.showBookmarkDialog(false) },
            title = { Text("Add Bookmark") },
            text = {
                OutlinedTextField(
                    value = bookmarkTitle,
                    onValueChange = { bookmarkTitle = it },
                    label = { Text("Bookmark title") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp)
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (bookmarkTitle.isNotBlank()) {
                            viewModel.addBookmark(bookmarkTitle)
                        }
                        bookmarkTitle = ""
                        viewModel.showBookmarkDialog(false)
                    }
                ) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        bookmarkTitle = ""
                        viewModel.showBookmarkDialog(false)
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }

    if (showPageJumpDialog) {
        AlertDialog(
            onDismissRequest = { showPageJumpDialog = false },
            title = { Text("Jump to Page") },
            text = {
                OutlinedTextField(
                    value = pageJumpText,
                    onValueChange = { pageJumpText = it.filter { c -> c.isDigit() } },
                    label = { Text("Page number (1-${pageState.totalPages})") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        val page = pageJumpText.toIntOrNull()
                        if (page != null && page in 1..pageState.totalPages) {
                            viewModel.goToPage(page - 1)
                        }
                        showPageJumpDialog = false
                    }
                ) {
                    Text("Go")
                }
            },
            dismissButton = {
                TextButton(onClick = { showPageJumpDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    if (showBookmarkListDialog) {
        AlertDialog(
            onDismissRequest = { showBookmarkListDialog = false },
            title = { Text("Bookmarks") },
            text = {
                if (bookmarksState.bookmarks.isEmpty()) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 24.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                painter = painterResource(id = R.drawable.ic_bookmark),
                                contentDescription = null,
                                modifier = Modifier.size(40.dp),
                                tint = MaterialTheme.colorScheme.onSurfaceVariant
                                    .copy(alpha = 0.5f)
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "No bookmarks yet",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.heightIn(max = 300.dp)
                    ) {
                        items(
                            items = bookmarksState.bookmarks,
                            key = { it.id }
                        ) { bookmark ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        viewModel.goToPage(bookmark.page)
                                        showBookmarkListDialog = false
                                    }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(
                                        text = bookmark.title,
                                        style = MaterialTheme.typography.bodyMedium
                                    )
                                    Text(
                                        text = "Page ${bookmark.page + 1}",
                                        style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    )
                                }
                                IconButton(
                                    onClick = { viewModel.deleteBookmark(bookmark.id) },
                                    modifier = Modifier.size(32.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Filled.Delete,
                                        contentDescription = "Delete bookmark",
                                        modifier = Modifier.size(16.dp),
                                        tint = MaterialTheme.colorScheme.error
                                    )
                                }
                            }
                            HorizontalDivider()
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showBookmarkListDialog = false }) {
                    Text("Close")
                }
            }
        )
    }
}

@Composable
private fun AnnotationListItem(
    annotation: AnnotationEntity,
    onDelete: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.weight(1f)
        ) {
            Box(
                modifier = Modifier
                    .size(12.dp)
                    .clip(CircleShape)
                    .background(Color(annotation.color))
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = when (annotation.type) {
                    "STICKY_NOTE" -> annotation.content.ifEmpty { "Sticky Note" }
                    "HIGHLIGHT" -> "Highlight"
                    "UNDERLINE" -> "Underline"
                    else -> annotation.type
                },
                style = MaterialTheme.typography.bodySmall,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
        IconButton(
            onClick = onDelete,
            modifier = Modifier.size(32.dp)
        ) {
            Icon(
                imageVector = Icons.Filled.Delete,
                contentDescription = "Delete annotation",
                modifier = Modifier.size(16.dp),
                tint = MaterialTheme.colorScheme.error
            )
        }
    }
}