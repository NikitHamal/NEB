package com.neb.ians

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.OpenInNew
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.neb.ians.data.AppSettings
import com.neb.ians.data.CommunityRepository
import com.neb.ians.data.CommunityThread
import com.neb.ians.data.Subject
import com.neb.ians.notifications.NebNotificationManager
import com.neb.ians.ui.theme.NebTheme

class ForumActivity : ComponentActivity() {
    private lateinit var repository: CommunityRepository
    private var threads by mutableStateOf<List<CommunityThread>>(emptyList())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        repository = CommunityRepository(this)
        setContent {
            val settings = remember { AppSettings(this) }
            NebTheme(darkTheme = settings.isDarkMode()) {
                ForumScreen(
                    threads = threads,
                    onBack = ::finish,
                    onOpenThread = { thread ->
                        startActivity(
                            Intent(this, AnswerActivity::class.java)
                                .putExtra(EXTRA_THREAD_ID, thread.id)
                        )
                    },
                    onThumbThread = { threadId ->
                        repository.thumbThread(threadId)
                        threads = repository.threads()
                    },
                    onCreateThread = { title, body, subject ->
                        repository.addThread(title, body, subject)
                        threads = repository.threads()
                        NebNotificationManager.showCommunity(
                            this,
                            "New NEBians question",
                            title
                        )
                    }
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        threads = repository.threads()
    }

    companion object {
        const val EXTRA_THREAD_ID = "thread_id"
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ForumScreen(
    threads: List<CommunityThread>,
    onBack: () -> Unit,
    onOpenThread: (CommunityThread) -> Unit,
    onThumbThread: (String) -> Unit,
    onCreateThread: (String, String, Subject) -> Unit
) {
    var showComposer by rememberSaveable { mutableStateOf(false) }
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                ),
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                title = { Text("Forum", style = MaterialTheme.typography.titleLarge) }
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = { showComposer = true },
                icon = { Icon(Icons.Outlined.Add, contentDescription = null) },
                text = { Text("Ask") }
            )
        }
    ) { padding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            color = MaterialTheme.colorScheme.background
        ) {
            LazyColumn(
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                item {
                    Text(
                        text = "Ask focused questions and upvote useful answers.",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                items(threads, key = { it.id }) { thread ->
                    ThreadCard(
                        thread = thread,
                        onOpen = { onOpenThread(thread) },
                        onThumb = { onThumbThread(thread.id) }
                    )
                }
                item { Spacer(Modifier.height(72.dp)) }
            }
        }
    }

    if (showComposer) {
        NewThreadDialog(
            onDismiss = { showComposer = false },
            onSubmit = { title, body, subject ->
                onCreateThread(title, body, subject)
                showComposer = false
            }
        )
    }
}

@Composable
private fun ThreadCard(
    thread: CommunityThread,
    onOpen: () -> Unit,
    onThumb: () -> Unit
) {
    Card(
        onClick = onOpen,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(verticalAlignment = Alignment.Top) {
                Icon(Icons.Outlined.Forum, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = thread.title,
                        style = MaterialTheme.typography.titleMedium,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = "${thread.subject.label} • ${thread.author} • ${thread.createdAt}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Icon(Icons.Outlined.OpenInNew, contentDescription = null)
            }
            Text(
                text = thread.body,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AssistChip(
                    onClick = onThumb,
                    label = { Text(thread.thumbs.toString()) },
                    leadingIcon = { Icon(Icons.Outlined.ThumbUp, contentDescription = null) }
                )
                AssistChip(
                    onClick = onOpen,
                    label = { Text("${thread.answers.size} answers") }
                )
            }
        }
    }
}

@Composable
private fun NewThreadDialog(
    onDismiss: () -> Unit,
    onSubmit: (String, String, Subject) -> Unit
) {
    var title by rememberSaveable { mutableStateOf("") }
    var body by rememberSaveable { mutableStateOf("") }
    var subject by rememberSaveable { mutableStateOf(Subject.Physics.name) }
    val canSubmit = title.isNotBlank() && body.isNotBlank()

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Ask the forum") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Question") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = body,
                    onValueChange = { body = it },
                    label = { Text("Details") },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3
                )
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Subject.entries.take(4).forEach { item ->
                        FilterChip(
                            selected = subject == item.name,
                            onClick = { subject = item.name },
                            label = { Text(item.label) }
                        )
                    }
                }
            }
        },
        confirmButton = {
            TextButton(
                enabled = canSubmit,
                onClick = { onSubmit(title, body, Subject.valueOf(subject)) }
            ) {
                Text("Post")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
