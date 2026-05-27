package com.neb.ians.ui.forum

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Reply
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.data.db.PostEntity
import com.neb.ians.data.db.ThreadEntity
import com.neb.ians.ui.settings.SettingsViewModel
import com.neb.ians.ui.theme.NEBiansTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class ThreadActivity : ComponentActivity() {
    companion object { const val EXTRA_THREAD_ID = "threadId" }

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        val id = intent.getStringExtra(EXTRA_THREAD_ID).orEmpty()
        setContent {
            val settingsVm: SettingsViewModel = hiltViewModel()
            val prefs by settingsVm.uiState.collectAsStateWithLifecycle()
            NEBiansTheme(darkTheme = prefs.darkMode) {
                ThreadScreen(
                    threadId = id,
                    onBack = { finish() },
                    onReply = { parentId ->
                        startActivity(Intent(this, ReplyActivity::class.java).apply {
                            putExtra(ReplyActivity.EXTRA_THREAD_ID, id)
                            putExtra(ReplyActivity.EXTRA_PARENT_ID, parentId)
                        })
                    }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ThreadScreen(
    threadId: String,
    onBack: () -> Unit,
    onReply: (String?) -> Unit,
    vm: ThreadViewModel = hiltViewModel(),
) {
    LaunchedEffect(threadId) { vm.load(threadId) }
    val thread by vm.thread.collectAsStateWithLifecycle()
    val posts by vm.posts.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Thread") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = { onReply(null) },
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                elevation = androidx.compose.material3.FloatingActionButtonDefaults.elevation(0.dp, 0.dp, 0.dp, 0.dp),
                shape = RoundedCornerShape(18.dp),
            ) {
                Icon(Icons.Outlined.Reply, contentDescription = null)
                Text("  Reply")
            }
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            thread?.let { t ->
                item { ThreadHeader(t, onThumb = { vm.toggleThreadThumb(t.id) }) }
            }
            items(posts, key = { it.id }) { p ->
                PostRow(p, onThumb = { vm.togglePostThumb(p) }, onReply = { onReply(p.id) })
            }
        }
    }
}

@Composable
private fun ThreadHeader(t: ThreadEntity, onThumb: () -> Unit) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceVariant,
        tonalElevation = 0.dp,
    ) {
        Column(modifier = Modifier.padding(14.dp).fillMaxWidth()) {
            Text(t.title, style = MaterialTheme.typography.titleMedium)
            Text("by ${t.author}", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(t.body, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(top = 8.dp))
            Row(modifier = Modifier.padding(top = 8.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onThumb) {
                    Icon(
                        if (t.thumbed) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                        contentDescription = "Thumb",
                        tint = if (t.thumbed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Text("${t.thumbCount}", style = MaterialTheme.typography.labelMedium)
            }
        }
    }
}

@Composable
private fun PostRow(p: PostEntity, onThumb: () -> Unit, onReply: () -> Unit) {
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 0.dp,
    ) {
        Column(modifier = Modifier.padding(12.dp).fillMaxWidth()) {
            Text(p.author, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary)
            Text(p.body, style = MaterialTheme.typography.bodyMedium)
            Row(modifier = Modifier.padding(top = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onThumb) {
                    Icon(
                        if (p.thumbed) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                        contentDescription = "Thumb",
                        tint = if (p.thumbed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Text("${p.thumbCount}", style = MaterialTheme.typography.labelMedium)
                Box(modifier = Modifier.weight(1f)) {}
                IconButton(onClick = onReply) {
                    Icon(Icons.Outlined.Reply, contentDescription = "Reply", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
