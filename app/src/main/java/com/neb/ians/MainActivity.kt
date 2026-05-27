package com.neb.ians

import android.Manifest
import android.content.Intent
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Article
import androidx.compose.material.icons.outlined.Campaign
import androidx.compose.material.icons.outlined.Calculate
import androidx.compose.material.icons.outlined.CheckCircle
import androidx.compose.material.icons.outlined.Close
import androidx.compose.material.icons.outlined.DarkMode
import androidx.compose.material.icons.outlined.Description
import androidx.compose.material.icons.outlined.FilterList
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.LightMode
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material.icons.outlined.PictureAsPdf
import androidx.compose.material.icons.outlined.School
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.AppSettings
import com.neb.ians.data.GradeLevel
import com.neb.ians.data.LearningResource
import com.neb.ians.data.ResourceCatalog
import com.neb.ians.data.ResourceType
import com.neb.ians.data.Subject
import com.neb.ians.notifications.NebNotificationManager
import com.neb.ians.ui.theme.NebTheme

class MainActivity : ComponentActivity() {
    private val notificationPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        NebNotificationManager.createChannels(this)
        requestNotificationsIfNeeded()
        setContent {
            val settings = remember { AppSettings(this) }
            var darkMode by remember { mutableStateOf(settings.isDarkMode()) }
            NebTheme(darkTheme = darkMode) {
                NebiansApp(
                    darkMode = darkMode,
                    onDarkModeChange = { enabled ->
                        settings.setDarkMode(enabled)
                        darkMode = enabled
                    }
                )
            }
        }
    }

    private fun requestNotificationsIfNeeded() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU && !NebNotificationManager.canNotify(this)) {
            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }
}

private enum class MainSection(val label: String, val icon: ImageVector) {
    Home("Study", Icons.Outlined.Home),
    Resources("Resources", Icons.Outlined.Description),
    Updates("Updates", Icons.Outlined.Notifications)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun NebiansApp(
    darkMode: Boolean,
    onDarkModeChange: (Boolean) -> Unit
) {
    val context = LocalContext.current
    var section by rememberSaveable { mutableStateOf(MainSection.Home.name) }
    val selectedSection = MainSection.valueOf(section)

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                ),
                title = {
                    Text(
                        text = "NEBians",
                        style = MaterialTheme.typography.titleLarge,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                },
                navigationIcon = {
                    IconButton(onClick = { context.startActivity(Intent(context, ForumActivity::class.java)) }) {
                        Icon(Icons.Outlined.Forum, contentDescription = "Open forum")
                    }
                },
                actions = {
                    IconButton(
                        onClick = {
                            NebNotificationManager.showAnnouncement(
                                context,
                                "NEBians notifications",
                                "Important announcements and community activity alerts are ready."
                            )
                        }
                    ) {
                        Icon(Icons.Outlined.Notifications, contentDescription = "Test notification")
                    }
                    IconButton(onClick = { onDarkModeChange(!darkMode) }) {
                        Icon(
                            imageVector = if (darkMode) Icons.Outlined.LightMode else Icons.Outlined.DarkMode,
                            contentDescription = "Toggle dark mode"
                        )
                    }
                }
            )
        },
        bottomBar = {
            NavigationBar(containerColor = MaterialTheme.colorScheme.surface) {
                MainSection.entries.forEach { item ->
                    NavigationBarItem(
                        selected = selectedSection == item,
                        onClick = { section = item.name },
                        icon = { Icon(item.icon, contentDescription = item.label) },
                        label = { Text(item.label) }
                    )
                }
            }
        }
    ) { padding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            color = MaterialTheme.colorScheme.background
        ) {
            when (selectedSection) {
                MainSection.Home -> StudyScreen(
                    onOpenResources = { section = MainSection.Resources.name },
                    onOpenForum = { context.startActivity(Intent(context, ForumActivity::class.java)) },
                    onOpenPdf = { resource -> openPdf(context, resource) }
                )
                MainSection.Resources -> ResourcesScreen(onOpenPdf = { resource -> openPdf(context, resource) })
                MainSection.Updates -> UpdatesScreen()
            }
        }
    }
}

@Composable
private fun StudyScreen(
    onOpenResources: () -> Unit,
    onOpenForum: () -> Unit,
    onOpenPdf: (LearningResource) -> Unit
) {
    val featured = ResourceCatalog.resources.take(3)
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp)
    ) {
        Text(
            text = "Study desk",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.onBackground
        )
        Text(
            text = "Organize Grade 11 and Grade 12 resources, cache PDFs, annotate pages, and keep forum answers close while revising.",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            AssistChip(
                onClick = onOpenResources,
                label = { Text("${ResourceCatalog.resources.size} resources") },
                leadingIcon = { Icon(Icons.Outlined.PictureAsPdf, contentDescription = null) }
            )
            AssistChip(
                onClick = onOpenForum,
                label = { Text("Forum") },
                leadingIcon = { Icon(Icons.Outlined.ThumbUp, contentDescription = null) }
            )
        }
        MetricRow()
        Text(
            text = "Continue learning",
            style = MaterialTheme.typography.titleMedium
        )
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            featured.forEach { resource ->
                ResourceCard(resource = resource, compact = true, onOpenPdf = { onOpenPdf(resource) })
            }
        }
    }
}

@Composable
private fun MetricRow() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        MetricCard(
            modifier = Modifier.weight(1f),
            label = "Subjects",
            value = ResourceCatalog.subjects.size.toString(),
            icon = Icons.Outlined.School
        )
        MetricCard(
            modifier = Modifier.weight(1f),
            label = "Offline PDFs",
            value = "Ready",
            icon = Icons.Outlined.CheckCircle
        )
    }
}

@Composable
private fun MetricCard(modifier: Modifier, label: String, value: String, icon: ImageVector) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Text(value, style = MaterialTheme.typography.titleLarge)
            Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun ResourcesScreen(onOpenPdf: (LearningResource) -> Unit) {
    var query by rememberSaveable { mutableStateOf("") }
    var selectedSubject by rememberSaveable { mutableStateOf<String?>(null) }
    var selectedGrade by rememberSaveable { mutableStateOf<String?>(null) }
    var selectedType by rememberSaveable { mutableStateOf<String?>(null) }
    val filtered by remember(query, selectedSubject, selectedGrade, selectedType) {
        derivedStateOf {
            ResourceCatalog.resources
                .filter { resource ->
                    val normalizedQuery = query.trim().lowercase()
                    val queryMatches = normalizedQuery.isBlank() ||
                        resource.title.lowercase().contains(normalizedQuery) ||
                        resource.summary.lowercase().contains(normalizedQuery) ||
                        resource.tags.any { it.lowercase().contains(normalizedQuery) }
                    val subjectMatches = selectedSubject == null || resource.subject.name == selectedSubject
                    val gradeMatches = selectedGrade == null || resource.grade.name == selectedGrade
                    val typeMatches = selectedType == null || resource.type.name == selectedType
                    queryMatches && subjectMatches && gradeMatches && typeMatches
                }
                .sortedWith(compareBy({ it.grade.label }, { it.subject.label }, { it.type.label }, { it.title }))
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            modifier = Modifier.fillMaxWidth(),
            leadingIcon = { Icon(Icons.Outlined.Search, contentDescription = null) },
            trailingIcon = {
                if (query.isNotBlank()) {
                    IconButton(onClick = { query = "" }) {
                        Icon(Icons.Outlined.Close, contentDescription = "Clear search")
                    }
                }
            },
            singleLine = true,
            label = { Text("Search ebooks, PDFs, notes, papers") }
        )
        FilterGroup(
            title = "Subject",
            icon = Icons.Outlined.FilterList,
            values = ResourceCatalog.subjects,
            selected = selectedSubject,
            label = { it.label },
            key = { it.name },
            onSelect = { selectedSubject = it }
        )
        FilterGroup(
            title = "Grade",
            values = ResourceCatalog.grades,
            selected = selectedGrade,
            label = { it.label },
            key = { it.name },
            onSelect = { selectedGrade = it }
        )
        FilterGroup(
            title = "Type",
            values = ResourceCatalog.types,
            selected = selectedType,
            label = { it.label },
            key = { it.name },
            onSelect = { selectedType = it }
        )
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "${filtered.size} result${if (filtered.size == 1) "" else "s"}",
                style = MaterialTheme.typography.titleSmall,
                modifier = Modifier.weight(1f)
            )
            TextButton(
                onClick = {
                    selectedSubject = null
                    selectedGrade = null
                    selectedType = null
                    query = ""
                }
            ) {
                Text("Clear")
            }
        }
        LazyVerticalGrid(
            columns = GridCells.Adaptive(minSize = 280.dp),
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(filtered, key = { it.id }) { resource ->
                ResourceCard(resource = resource, onOpenPdf = { onOpenPdf(resource) })
            }
        }
    }
}

@Composable
private fun <T> FilterGroup(
    title: String,
    values: List<T>,
    selected: String?,
    label: (T) -> String,
    key: (T) -> String,
    onSelect: (String?) -> Unit,
    icon: ImageVector? = null
) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            if (icon != null) {
                Icon(icon, contentDescription = null, modifier = Modifier.padding(end = 6.dp))
            }
            Text(title, style = MaterialTheme.typography.labelLarge)
        }
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            item {
                FilterChip(
                    selected = selected == null,
                    onClick = { onSelect(null) },
                    label = { Text("All") }
                )
            }
            items(values.size) { index ->
                val item = values[index]
                val itemKey = key(item)
                FilterChip(
                    selected = selected == itemKey,
                    onClick = { onSelect(if (selected == itemKey) null else itemKey) },
                    label = { Text(label(item)) }
                )
            }
        }
    }
}

@Composable
private fun ResourceCard(
    resource: LearningResource,
    compact: Boolean = false,
    onOpenPdf: () -> Unit
) {
    Card(
        onClick = onOpenPdf,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(verticalAlignment = Alignment.Top) {
                Icon(
                    imageVector = resourceIcon(resource.type),
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
                Spacer(Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = resource.title,
                        style = MaterialTheme.typography.titleMedium,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "${resource.grade.label} • ${resource.subject.label} • ${resource.type.label}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Icon(Icons.Outlined.OpenInNew, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            if (!compact) {
                Text(
                    text = resource.summary,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AssistChip(onClick = onOpenPdf, label = { Text("${resource.pages} pages") })
                AssistChip(onClick = onOpenPdf, label = { Text("Offline cache") })
            }
        }
    }
}

@Composable
private fun UpdatesScreen() {
    val context = LocalContext.current
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Text("Announcements", style = MaterialTheme.typography.headlineMedium)
        ResourceCatalog.announcements.forEach { announcement ->
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = if (announcement.important) {
                        MaterialTheme.colorScheme.primaryContainer
                    } else {
                        MaterialTheme.colorScheme.surfaceContainer
                    }
                ),
                elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Outlined.Campaign, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(10.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(announcement.title, style = MaterialTheme.typography.titleMedium)
                            Text(announcement.time, style = MaterialTheme.typography.bodySmall)
                        }
                    }
                    Text(announcement.body, style = MaterialTheme.typography.bodyMedium)
                    if (announcement.important) {
                        OutlinedButton(
                            onClick = {
                                NebNotificationManager.showAnnouncement(
                                    context,
                                    announcement.title,
                                    announcement.body
                                )
                            }
                        ) {
                            Icon(Icons.Outlined.Notifications, contentDescription = null)
                            Spacer(Modifier.width(8.dp))
                            Text("Notify")
                        }
                    }
                }
            }
        }
    }
}

private fun resourceIcon(type: ResourceType): ImageVector = when (type) {
    ResourceType.Textbook -> Icons.Outlined.Article
    ResourceType.Notes -> Icons.Outlined.Description
    ResourceType.PastPapers -> Icons.Outlined.PictureAsPdf
    ResourceType.FormulaSheet -> Icons.Outlined.Calculate
}

private fun openPdf(context: android.content.Context, resource: LearningResource) {
    context.startActivity(
        Intent(context, PdfViewerActivity::class.java)
            .putExtra(PdfViewerActivity.EXTRA_RESOURCE_ID, resource.id)
    )
}
