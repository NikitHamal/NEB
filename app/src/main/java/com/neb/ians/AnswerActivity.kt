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
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ArrowBack
import androidx.compose.material.icons.outlined.Reply
import androidx.compose.material.icons.outlined.ThumbUp
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.neb.ians.data.AppSettings
import com.neb.ians.data.CommunityAnswer
import com.neb.ians.data.CommunityRepository
import com.neb.ians.data.CommunityThread
import com.neb.ians.ui.theme.NebTheme

class AnswerActivity : ComponentActivity() {
    private lateinit var repository: CommunityRepository
    private var thread by mutableStateOf<CommunityThread?>(null)
    private val threadId: String by lazy { intent.getStringExtra(ForumActivity.EXTRA_THREAD_ID).orEmpty() }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        repository = CommunityRepository(this)
        setContent {
            val settings = remember { AppSettings(this) }
            NebTheme(darkTheme = settings.isDarkMode()) {
                AnswerScreen(
                    thread = thread,
                    onBack = ::finish,
                    onReply = {
                        startActivity(
                            Intent(this, ReplyActivity::class.java)
                                .putExtra(ForumActivity.EXTRA_THREAD_ID, threadId)
                        )
                    },
                    onThumbThread = {
                        repository.thumbThread(threadId)
                        refresh()
                    },
                    onThumbAnswer = { answerId ->
                        repository.thumbAnswer(threadId, answerId)
                        refresh()
                    }
                )
            }
        }
    }

    override fun onResume() {
        super.onResume()
        refresh()
    }

    private fun refresh() {
        thread = repository.thread(threadId)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AnswerScreen(
    thread: CommunityThread?,
    onBack: () -> Unit,
    onReply: () -> Unit,
    onThumbThread: () -> Unit,
    onThumbAnswer: (String) -> Unit
) {
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
                title = { Text("Answers") }
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onReply,
                icon = { Icon(Icons.Outlined.Reply, contentDescription = null) },
                text = { Text("Reply") }
            )
        }
    ) { padding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            color = MaterialTheme.colorScheme.background
        ) {
            if (thread == null) {
                Text(
                    text = "Question not found.",
                    modifier = Modifier.padding(20.dp),
                    style = MaterialTheme.typography.bodyLarge
                )
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    item {
                        QuestionHeader(thread = thread, onThumb = onThumbThread)
                    }
                    item {
                        Text(
                            text = "Answers",
                            style = MaterialTheme.typography.titleMedium,
                            modifier = Modifier.padding(top = 4.dp)
                        )
                    }
                    items(thread.answers, key = { it.id }) { answer ->
                        AnswerCard(answer = answer, onThumb = { onThumbAnswer(answer.id) })
                    }
                }
            }
        }
    }
}

@Composable
private fun QuestionHeader(thread: CommunityThread, onThumb: () -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Text(thread.title, style = MaterialTheme.typography.titleLarge)
            Text(thread.body, style = MaterialTheme.typography.bodyMedium)
            Text(
                text = "${thread.subject.label} • ${thread.author} • ${thread.createdAt}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            AssistChip(
                onClick = onThumb,
                label = { Text(thread.thumbs.toString()) },
                leadingIcon = { Icon(Icons.Outlined.ThumbUp, contentDescription = null) }
            )
        }
    }
}

@Composable
private fun AnswerCard(answer: CommunityAnswer, onThumb: () -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainer),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row {
                Column(modifier = Modifier.weight(1f)) {
                    Text(answer.author, style = MaterialTheme.typography.titleSmall)
                    Text(answer.createdAt, style = MaterialTheme.typography.bodySmall)
                }
                AssistChip(
                    onClick = onThumb,
                    label = { Text(answer.thumbs.toString()) },
                    leadingIcon = { Icon(Icons.Outlined.ThumbUp, contentDescription = null) }
                )
            }
            Text(answer.body, style = MaterialTheme.typography.bodyMedium)
        }
    }
}
