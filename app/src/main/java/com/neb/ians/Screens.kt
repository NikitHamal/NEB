@file:OptIn(ExperimentalMaterial3Api::class)

package com.neb.ians

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.automirrored.outlined.Reply
import androidx.compose.material.icons.automirrored.outlined.Send
import androidx.compose.material.icons.outlined.CloudDone
import androidx.compose.material.icons.outlined.DarkMode
import androidx.compose.material.icons.outlined.FilterList
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.LightMode
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LargeTopAppBar
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

private enum class SortMode(val label: String) {
    Subject("Subject"),
    Grade("Grade"),
    Type("Type"),
    Title("Title")
}

@Composable
fun HomeScreen(
    onOpenLibrary: () -> Unit,
    onOpenForum: () -> Unit,
    onOpenAnnouncements: () -> Unit,
    onOpenSettings: () -> Unit,
    onOpenPdf: (LearningResource) -> Unit
) {
    Scaffold(
        topBar = {
            LargeTopAppBar(
                title = {
                    Column {
                        Text("NEBians", fontWeight = FontWeight.SemiBold)
                        Text(
                            "Study resources for Nepali learners",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                },
                actions = {
                    IconButton(onClick = onOpenAnnouncements) {
                        Icon(Icons.Outlined.Notifications, contentDescription = "Announcements")
                    }
                    IconButton(onClick = onOpenSettings) {
                        Icon(Icons.Outlined.Settings, contentDescription = "Settings")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                ActionTile(
                    icon = Icons.AutoMirrored.Outlined.MenuBook,
                    title = "Library",
                    subtitle = "Ebooks, notes, past papers, and formula sheets",
                    onClick = onOpenLibrary
                )
            }
            item {
                ActionTile(
                    icon = Icons.Outlined.Forum,
                    title = "Discussion Forum",
                    subtitle = "Ask, answer, and reply with focused study threads",
                    onClick = onOpenForum
                )
            }
            item {
                Text(
                    text = "Continue Reading",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }
            items(SampleCatalog.resources.take(3), key = { it.id }) { resource ->
                ResourceCard(resource = resource, onOpen = { onOpenPdf(resource) })
            }
        }
    }
}

@Composable
fun LibraryScreen(onBack: () -> Unit, onOpenPdf: (LearningResource) -> Unit) {
    var query by remember { mutableStateOf("") }
    var selectedSubject by remember { mutableStateOf<Subject?>(null) }
    var selectedGrade by remember { mutableStateOf<GradeLevel?>(null) }
    var selectedType by remember { mutableStateOf<ResourceType?>(null) }
    var sortMode by remember { mutableStateOf(SortMode.Subject) }

    val filteredResources = remember(query, selectedSubject, selectedGrade, selectedType, sortMode) {
        SampleCatalog.resources
            .filter { resource ->
                val matchesQuery = query.isBlank() ||
                    resource.title.contains(query, ignoreCase = true) ||
                    resource.description.contains(query, ignoreCase = true) ||
                    resource.tags.any { it.contains(query, ignoreCase = true) }
                matchesQuery &&
                    (selectedSubject == null || resource.subject == selectedSubject) &&
                    (selectedGrade == null || resource.grade == selectedGrade) &&
                    (selectedType == null || resource.type == selectedType)
            }
            .let { resources ->
                when (sortMode) {
                    SortMode.Subject -> resources.sortedWith(compareBy({ it.subject.label }, { it.title }))
                    SortMode.Grade -> resources.sortedWith(compareBy({ it.grade.label }, { it.subject.label }))
                    SortMode.Type -> resources.sortedWith(compareBy({ it.type.label }, { it.title }))
                    SortMode.Title -> resources.sortedBy { it.title }
                }
            }
    }

    Scaffold(
        topBar = { AppTopBar(title = "Library", onBack = onBack) }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                OutlinedTextField(
                    value = query,
                    onValueChange = { query = it },
                    modifier = Modifier.fillMaxWidth(),
                    leadingIcon = { Icon(Icons.Outlined.Search, contentDescription = null) },
                    label = { Text("Search resources") },
                    singleLine = true
                )
            }
            item {
                FilterSection(
                    title = "Subject",
                    values = Subject.entries,
                    selected = selectedSubject,
                    label = { it.label },
                    onSelected = { selectedSubject = it }
                )
            }
            item {
                FilterSection(
                    title = "Grade",
                    values = GradeLevel.entries,
                    selected = selectedGrade,
                    label = { it.label },
                    onSelected = { selectedGrade = it }
                )
            }
            item {
                FilterSection(
                    title = "Type",
                    values = ResourceType.entries,
                    selected = selectedType,
                    label = { it.label },
                    onSelected = { selectedType = it }
                )
            }
            item {
                SortSection(sortMode = sortMode, onSortChange = { sortMode = it })
            }
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Outlined.FilterList, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text(
                        "${filteredResources.size} resources",
                        style = MaterialTheme.typography.titleSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            items(filteredResources, key = { it.id }) { resource ->
                ResourceCard(resource = resource, onOpen = { onOpenPdf(resource) })
            }
        }
    }
}

@Composable
fun ForumScreen(onBack: () -> Unit, onOpenThread: (ForumThread) -> Unit) {
    val threads by ForumRepository.threads.collectAsState()

    Scaffold(topBar = { AppTopBar(title = "Forum", onBack = onBack) }) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(threads, key = { it.id }) { thread ->
                ForumThreadCard(thread = thread, onOpen = { onOpenThread(thread) })
            }
        }
    }
}

@Composable
fun ThreadAnswerScreen(threadId: String, onBack: () -> Unit, onReply: () -> Unit) {
    val threads by ForumRepository.threads.collectAsState()
    val thread = threads.firstOrNull { it.id == threadId }

    if (thread == null) {
        MissingScreen(title = "Thread unavailable", onBack = onBack)
        return
    }

    Scaffold(
        topBar = { AppTopBar(title = "Answer", onBack = onBack) }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                CardSurface {
                    Text(thread.title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.height(8.dp))
                    Text(thread.body, style = MaterialTheme.typography.bodyLarge)
                    Spacer(Modifier.height(12.dp))
                    MetadataRow("${thread.grade.label} - ${thread.subject.label}", thread.author, thread.createdAt)
                    Spacer(Modifier.height(8.dp))
                    TextButton(onClick = { ForumRepository.thumbThread(thread.id) }) {
                        Icon(Icons.Outlined.ThumbUp, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(thread.thumbs.toString())
                    }
                }
            }
            item {
                Button(onClick = onReply, modifier = Modifier.fillMaxWidth()) {
                    Icon(Icons.AutoMirrored.Outlined.Reply, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Reply")
                }
            }
            items(thread.replies, key = { it.id }) { reply ->
                ReplyCard(threadId = thread.id, reply = reply)
            }
        }
    }
}

@Composable
fun ReplyComposerScreen(threadId: String, onBack: () -> Unit, onSent: () -> Unit) {
    var body by remember { mutableStateOf("") }

    Scaffold(
        topBar = { AppTopBar(title = "Reply", onBack = onBack) }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedTextField(
                value = body,
                onValueChange = { body = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                label = { Text("Answer") }
            )
            Button(
                onClick = {
                    ForumRepository.addReply(threadId, body)
                    onSent()
                },
                enabled = body.isNotBlank(),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.AutoMirrored.Outlined.Send, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("Send Reply")
            }
        }
    }
}

@Composable
fun AnnouncementsScreen(onBack: () -> Unit) {
    val context = LocalContext.current
    Scaffold(topBar = { AppTopBar(title = "Announcements", onBack = onBack) }) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(AnnouncementRepository.announcements, key = { it.id }) { announcement ->
                CardSurface {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        AssistChip(onClick = {}, label = { Text(announcement.category) })
                        Spacer(Modifier.width(8.dp))
                        Text(
                            announcement.time,
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Spacer(Modifier.height(10.dp))
                    Text(announcement.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.height(6.dp))
                    Text(announcement.body, style = MaterialTheme.typography.bodyMedium)
                }
            }
            item {
                OutlinedButton(
                    onClick = {
                        NotificationHelper.show(
                            context,
                            "NEBians update",
                            "A new study announcement is ready."
                        )
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Outlined.Notifications, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Preview Notification")
                }
            }
        }
    }
}

@Composable
fun SettingsScreen(onBack: () -> Unit) {
    val container = LocalNebiansContainer.current
    val darkMode by container.settings.darkMode.collectAsState(initial = false)
    val scope = rememberCoroutineScope()
    var cacheSize by remember { mutableStateOf("0 KB") }

    LaunchedEffect(Unit) {
        cacheSize = formatBytes(container.cache.cacheSizeBytes())
    }

    Scaffold(topBar = { AppTopBar(title = "Settings", onBack = onBack) }) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                CardSurface {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                if (darkMode) Icons.Outlined.DarkMode else Icons.Outlined.LightMode,
                                contentDescription = null,
                                tint = MaterialTheme.colorScheme.primary
                            )
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text("Dark mode", style = MaterialTheme.typography.titleMedium)
                                Text(
                                    "Use a clean low-glare theme",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                        Switch(
                            checked = darkMode,
                            onCheckedChange = { enabled ->
                                scope.launch { container.settings.setDarkMode(enabled) }
                            }
                        )
                    }
                }
            }
            item {
                CardSurface {
                    Text("Offline PDF cache", style = MaterialTheme.typography.titleMedium)
                    Spacer(Modifier.height(6.dp))
                    Text(cacheSize, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(12.dp))
                    OutlinedButton(
                        onClick = {
                            scope.launch {
                                container.cache.clearCache()
                                cacheSize = formatBytes(container.cache.cacheSizeBytes())
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Clear Cache")
                    }
                }
            }
        }
    }
}

@Composable
fun MissingScreen(title: String, onBack: () -> Unit) {
    Scaffold(topBar = { AppTopBar(title = title, onBack = onBack) }) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentAlignment = Alignment.Center
        ) {
            Text(title, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun AppTopBar(title: String, onBack: () -> Unit) {
    TopAppBar(
        title = { Text(title, fontWeight = FontWeight.SemiBold) },
        navigationIcon = {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
            }
        }
    )
}

@Composable
private fun ActionTile(icon: ImageVector, title: String, subtitle: String, onClick: () -> Unit) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = MaterialTheme.shapes.large,
        color = MaterialTheme.colorScheme.surfaceContainer,
        tonalElevation = 0.dp,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.width(14.dp))
            Column(Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Text(
                    subtitle,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun ResourceCard(resource: LearningResource, onOpen: () -> Unit) {
    val container = LocalNebiansContainer.current
    val cached = remember(resource.id) { container.cache.isCached(resource) }

    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLow),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Outlined.PictureAsPdf, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(resource.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                    Text(
                        "${resource.subject.label} - ${resource.grade.label}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            Text(
                resource.description,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    AssistChip(onClick = {}, label = { Text(resource.type.label) })
                    AssistChip(
                        onClick = {},
                        label = { Text(if (cached) "Cached" else "Offline ready") },
                        leadingIcon = {
                            Icon(Icons.Outlined.CloudDone, contentDescription = null, modifier = Modifier.size(18.dp))
                        }
                    )
                }
                Button(onClick = onOpen) {
                    Text("Open")
                }
            }
        }
    }
}

@Composable
private fun ForumThreadCard(thread: ForumThread, onOpen: () -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLow),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onOpen)
    ) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            MetadataRow("${thread.grade.label} - ${thread.subject.label}", thread.author, thread.createdAt)
            Text(thread.title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Text(thread.body, style = MaterialTheme.typography.bodyMedium, maxLines = 2, overflow = TextOverflow.Ellipsis)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Outlined.ThumbUp, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(6.dp))
                Text(thread.thumbs.toString(), style = MaterialTheme.typography.labelLarge)
                Spacer(Modifier.width(16.dp))
                Icon(Icons.AutoMirrored.Outlined.Reply, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(6.dp))
                Text(thread.replies.size.toString(), style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}

@Composable
private fun ReplyCard(threadId: String, reply: ForumReply) {
    CardSurface {
        MetadataRow("Answer", reply.author, reply.createdAt)
        Spacer(Modifier.height(8.dp))
        Text(reply.body, style = MaterialTheme.typography.bodyLarge)
        Spacer(Modifier.height(8.dp))
        TextButton(onClick = { ForumRepository.thumbReply(threadId, reply.id) }) {
            Icon(Icons.Outlined.ThumbUp, contentDescription = null, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(8.dp))
            Text(reply.thumbs.toString())
        }
    }
}

@Composable
private fun CardSurface(content: @Composable ColumnScope.() -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLow),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            content = content
        )
    }
}

@Composable
private fun MetadataRow(primary: String, author: String, time: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        AssistChip(onClick = {}, label = { Text(primary) }, leadingIcon = {
            Icon(Icons.Outlined.School, contentDescription = null, modifier = Modifier.size(18.dp))
        })
        Spacer(Modifier.width(8.dp))
        Text(
            "$author - $time",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
private fun <T> FilterSection(
    title: String,
    values: List<T>,
    selected: T?,
    label: (T) -> String,
    onSelected: (T?) -> Unit
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(title, style = MaterialTheme.typography.labelLarge)
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            item {
                FilterChip(
                    selected = selected == null,
                    onClick = { onSelected(null) },
                    label = { Text("All") }
                )
            }
            items(values) { value ->
                FilterChip(
                    selected = selected == value,
                    onClick = { onSelected(value) },
                    label = { Text(label(value)) }
                )
            }
        }
    }
}

@Composable
private fun SortSection(sortMode: SortMode, onSortChange: (SortMode) -> Unit) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Sort by", style = MaterialTheme.typography.labelLarge)
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            items(SortMode.entries.toList()) { mode ->
                FilterChip(
                    selected = sortMode == mode,
                    onClick = { onSortChange(mode) },
                    label = { Text(mode.label) }
                )
            }
        }
    }
}

private fun formatBytes(bytes: Long): String {
    if (bytes < 1024) return "$bytes B"
    val kb = bytes / 1024.0
    if (kb < 1024) return "${kb.roundToInt()} KB"
    val mb = kb / 1024.0
    return "${(mb * 10).roundToInt() / 10.0} MB"
}
