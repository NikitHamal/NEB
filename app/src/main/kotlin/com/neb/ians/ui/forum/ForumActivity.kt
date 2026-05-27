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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material.icons.filled.ThumbUp
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
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
import com.neb.ians.data.db.ThreadEntity
import com.neb.ians.ui.settings.SettingsViewModel
import com.neb.ians.ui.theme.NEBiansTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class ForumActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent {
            val settingsVm: SettingsViewModel = hiltViewModel()
            val prefs by settingsVm.uiState.collectAsStateWithLifecycle()
            NEBiansTheme(darkTheme = prefs.darkMode) {
                ForumScreen(
                    onBack = { finish() },
                    onOpenThread = { id ->
                        startActivity(Intent(this, ThreadActivity::class.java).apply {
                            putExtra(ThreadActivity.EXTRA_THREAD_ID, id)
                        })
                    },
                    onCreateThread = {
                        startActivity(Intent(this, NewThreadActivity::class.java))
                    }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ForumScreen(
    onBack: () -> Unit,
    onOpenThread: (String) -> Unit,
    onCreateThread: () -> Unit,
    vm: ForumViewModel = hiltViewModel(),
) {
    val threads by vm.threads.collectAsStateWithLifecycle()
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Forum") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onCreateThread,
                shape = RoundedCornerShape(18.dp),
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                elevation = androidx.compose.material3.FloatingActionButtonDefaults.elevation(0.dp, 0.dp, 0.dp, 0.dp),
            ) {
                Icon(Icons.Outlined.Add, contentDescription = "New thread")
            }
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            items(threads, key = { it.id }) { t ->
                ThreadRow(t, onClick = { onOpenThread(t.id) }, onThumb = { vm.toggleThumb(t.id) })
            }
        }
    }
}

@Composable
private fun ThreadRow(t: ThreadEntity, onClick: () -> Unit, onThumb: () -> Unit) {
    Surface(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surfaceVariant,
        tonalElevation = 0.dp,
        shadowElevation = 0.dp,
    ) {
        Column(modifier = Modifier.padding(14.dp).fillMaxWidth()) {
            Text(t.title, style = MaterialTheme.typography.titleSmall)
            Text(t.body, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2)
            Row(modifier = Modifier.padding(top = 8.dp).fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text("by ${t.author}", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Box(modifier = Modifier.weight(1f))
                IconButton(onClick = onThumb) {
                    Icon(
                        if (t.thumbed) Icons.Filled.ThumbUp else Icons.Outlined.ThumbUp,
                        contentDescription = "Thumb",
                        tint = if (t.thumbed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Text("${t.thumbCount}", style = MaterialTheme.typography.labelMedium)
                Icon(Icons.Outlined.ChatBubbleOutline, contentDescription = null, modifier = Modifier.padding(start = 12.dp).size(18.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("  ${t.replyCount}", style = MaterialTheme.typography.labelMedium)
            }
        }
    }
}
