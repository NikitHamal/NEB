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
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.FormatUnderlined
import androidx.compose.material.icons.outlined.Highlight
import androidx.compose.material.icons.outlined.StickyNote2
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
    val uiState by viewModel.uiState.collectAsState()

    var showOverflowMenu by remember { mutableStateOf(false) }
    var showPageJumpDialog by remember { mutableStateOf(false) }
    var showBookmarkListDialog by remember { mutableStateOf(false) }
    var pageJumpText by remember { mutableStateOf("") }
    var bookmarkTitle by remember { mutableStateOf("") }
    var annotationsExpanded by remember { mutableStateOf(false) }

    val currentPageAnnotations = remember(uiState.annotations, uiState.currentPage) {
        uiState.annotations.filter { it.page == uiState.currentPage }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = uiState.resource?.title ?: "PDF Reader",
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
                                        imageVector = Icons.Filled.BookmarkAdd,
                                        contentDescription = null
                                    )
                                },
                                onClick = {
                                    showOverflowMenu = false
                                    bookmarkTitle = "Page ${uiState.currentPage + 1}"
                                    viewModel.showBookmarkDialog(true)
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("View Bookmarks") },
                                leadingIcon = {
                                    Icon(
                                        imageVector = Icons.Filled.Bookmarks,
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
                                        imageVector = Icons.Filled.FindInPage,
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
                                        if (uiState.showAnnotationTools) "Hide Annotations"
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
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Main content area
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
            ) {
                if (uiState.isLoading) {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                } else if (uiState.error != null) {
                    Column(
                        modifier = Modifier
                            .align(Alignment.Center)
                            .padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Icon(
                            imageVector = Icons.Filled.ErrorOutline,
                            contentDescription = null,
                            modifier = Modifier.size(64.dp),
                            tint = MaterialTheme.colorScheme.error
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = uiState.error ?: "Unknown error",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            textAlign = TextAlign.Center
                        )
                    }
                } else if (uiState.pageBitmap != null) {
                    Image(
                        bitmap = uiState.pageBitmap!!.asImageBitmap(),
                        contentDescription = "Page ${uiState.currentPage + 1}",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    // Placeholder for current page
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(MaterialTheme.colorScheme.surfaceVariant),
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
                            shape = RoundedCornerShape(4.dp)
                        ) {
                            Column(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .padding(32.dp),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Filled.PictureAsPdf,
                                    contentDescription = null,
                                    modifier = Modifier.size(72.dp),
                                    tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f)
                                )
                                Spacer(modifier = Modifier.height(24.dp))
                                Text(
                                    text = uiState.resource?.title ?: "Document",
                                    style = MaterialTheme.typography.titleLarge,
                                    textAlign = TextAlign.Center,
                                    color = MaterialTheme.colorScheme.onSurface
                                )
                                Spacer(modifier = Modifier.height(12.dp))
                                Text(
                                    text = "Page ${uiState.currentPage + 1}",
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                }

                // Annotation overlay
                if (!uiState.isLoading && uiState.error == null) {
                    AnnotationOverlay(
                        annotations = currentPageAnnotations,
                        annotationMode = uiState.annotationMode,
                        onAnnotationCreated = { startX, startY, endX, endY ->
                            if (uiState.annotationMode == AnnotationMode.STICKY_NOTE) {
                                viewModel.addAnnotation(startX, startY, endX, endY)
                                viewModel.showStickyNoteDialog(true)
                            } else {
                                viewModel.addAnnotation(startX, startY, endX, endY)
                            }
                        },
                        onAnnotationTapped = { /* handled via annotation list */ },
                        modifier = Modifier.fillMaxSize()
                    )
                }
            }

            // Annotation list section
            if (currentPageAnnotations.isNotEmpty()) {
                Surface(
                    tonalElevation = 1.dp,
                    modifier = Modifier.fillMaxWidth()
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
                                    Icons.Filled.ExpandLess else Icons.Filled.ExpandMore,
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

            // Bottom annotation toolbar
            AnimatedVisibility(
                visible = uiState.showAnnotationTools,
                enter = expandVertically(),
                exit = shrinkVertically()
            ) {
                Surface(
                    tonalElevation = 2.dp,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        // Tool buttons row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Highlight button
                            IconToggleButton(
                                checked = uiState.annotationMode == AnnotationMode.HIGHLIGHT,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.HIGHLIGHT)
                                }
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.Highlight,
                                    contentDescription = "Highlight",
                                    tint = if (uiState.annotationMode == AnnotationMode.HIGHLIGHT)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            // Underline button
                            IconToggleButton(
                                checked = uiState.annotationMode == AnnotationMode.UNDERLINE,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.UNDERLINE)
                                }
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.FormatUnderlined,
                                    contentDescription = "Underline",
                                    tint = if (uiState.annotationMode == AnnotationMode.UNDERLINE)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }

                            // Sticky Note button
                            IconToggleButton(
                                checked = uiState.annotationMode == AnnotationMode.STICKY_NOTE,
                                onCheckedChange = {
                                    viewModel.setAnnotationMode(AnnotationMode.STICKY_NOTE)
                                }
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.StickyNote2,
                                    contentDescription = "Sticky Note",
                                    tint = if (uiState.annotationMode == AnnotationMode.STICKY_NOTE)
                                        MaterialTheme.colorScheme.primary
                                    else MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // Color picker row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceEvenly,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val colors = listOf(
                                0xFFFFEB3B.toInt(), // Yellow
                                0xFF4CAF50.toInt(), // Green
                                0xFF2196F3.toInt(), // Blue
                                0xFFE91E63.toInt(), // Pink
                                0xFFFF9800.toInt()  // Orange
                            )
                            colors.forEach { color ->
                                val isSelected = uiState.selectedColor == color
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

            // Page navigation bar
            Surface(
                tonalElevation = 1.dp,
                modifier = Modifier.fillMaxWidth()
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
                        enabled = uiState.currentPage > 0
                    ) {
                        Icon(
                            imageVector = Icons.Filled.ChevronLeft,
                            contentDescription = "Previous page"
                        )
                    }

                    Text(
                        text = if (uiState.totalPages > 0) {
                            "Page ${uiState.currentPage + 1} of ${uiState.totalPages}"
                        } else {
                            "No pages"
                        },
                        style = MaterialTheme.typography.bodyMedium
                    )

                    IconButton(
                        onClick = { viewModel.nextPage() },
                        enabled = uiState.currentPage < uiState.totalPages - 1
                    ) {
                        Icon(
                            imageVector = Icons.Filled.ChevronRight,
                            contentDescription = "Next page"
                        )
                    }
                }
            }
        }
    }

    // Sticky note creation dialog
    if (uiState.showStickyNoteDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.showStickyNoteDialog(false) },
            title = { Text("Add Sticky Note") },
            text = {
                OutlinedTextField(
                    value = uiState.stickyNoteText,
                    onValueChange = { viewModel.onStickyNoteTextChange(it) },
                    label = { Text("Note") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .heightIn(min = 120.dp),
                    placeholder = { Text("Enter your note...") },
                    maxLines = 6
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        viewModel.showStickyNoteDialog(false)
                        viewModel.onStickyNoteTextChange("")
                    }
                ) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        viewModel.onStickyNoteTextChange("")
                        viewModel.showStickyNoteDialog(false)
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }

    // Bookmark creation dialog
    if (uiState.showBookmarkDialog) {
        AlertDialog(
            onDismissRequest = { viewModel.showBookmarkDialog(false) },
            title = { Text("Add Bookmark") },
            text = {
                OutlinedTextField(
                    value = bookmarkTitle,
                    onValueChange = { bookmarkTitle = it },
                    label = { Text("Bookmark title") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
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

    // Page jump dialog
    if (showPageJumpDialog) {
        AlertDialog(
            onDismissRequest = { showPageJumpDialog = false },
            title = { Text("Jump to Page") },
            text = {
                OutlinedTextField(
                    value = pageJumpText,
                    onValueChange = { pageJumpText = it.filter { c -> c.isDigit() } },
                    label = { Text("Page number (1-${uiState.totalPages})") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        val page = pageJumpText.toIntOrNull()
                        if (page != null && page in 1..uiState.totalPages) {
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

    // Bookmark list dialog
    if (showBookmarkListDialog) {
        AlertDialog(
            onDismissRequest = { showBookmarkListDialog = false },
            title = { Text("Bookmarks") },
            text = {
                if (uiState.bookmarks.isEmpty()) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 24.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                imageVector = Icons.Filled.BookmarkBorder,
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
                            items = uiState.bookmarks,
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
