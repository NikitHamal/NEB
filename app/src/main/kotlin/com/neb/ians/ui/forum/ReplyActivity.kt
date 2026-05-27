package com.neb.ians.ui.forum

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Send
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.ui.settings.SettingsViewModel
import com.neb.ians.ui.theme.NEBiansTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class ReplyActivity : ComponentActivity() {
    companion object {
        const val EXTRA_THREAD_ID = "threadId"
        const val EXTRA_PARENT_ID = "parentId"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        val threadId = intent.getStringExtra(EXTRA_THREAD_ID).orEmpty()
        val parentId = intent.getStringExtra(EXTRA_PARENT_ID)
        setContent {
            val settingsVm: SettingsViewModel = hiltViewModel()
            val prefs by settingsVm.uiState.collectAsStateWithLifecycle()
            NEBiansTheme(darkTheme = prefs.darkMode) {
                ReplyScreen(
                    threadId = threadId,
                    parentId = parentId,
                    onBack = { finish() },
                    onSubmitted = { finish() }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ReplyScreen(
    threadId: String,
    parentId: String?,
    onBack: () -> Unit,
    onSubmitted: () -> Unit,
    vm: ReplyViewModel = hiltViewModel(),
) {
    var text by remember { mutableStateOf("") }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (parentId == null) "Reply" else "Reply to comment") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                placeholder = { Text("Write your reply") },
                modifier = Modifier.fillMaxWidth(),
                minLines = 6,
                shape = RoundedCornerShape(16.dp),
            )
            Button(
                onClick = { vm.reply(threadId, text, parentId, onSubmitted) },
                enabled = text.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(14.dp),
            ) {
                Icon(Icons.Outlined.Send, contentDescription = null)
                Text("  Post reply")
            }
        }
    }
}
