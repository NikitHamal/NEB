package com.neb.ians.ui.screens.study

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import com.neb.ians.R
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiStudyDocument
import com.neb.ians.data.api.ApiStudySpaceDetail
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebKpiCard
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebSectionHeader
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.ui.components.fileSizeLabel
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StudySpaceUiState(
    val space: ApiStudySpaceDetail? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

@HiltViewModel
class StudySpaceViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val spaceId: String = savedStateHandle.get<String>("spaceId") ?: ""
    private val _uiState = MutableStateFlow(StudySpaceUiState())
    val uiState: StateFlow<StudySpaceUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun load() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to open this Study Space") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val detail = apiService.getStudySpaceDetail(token, spaceId)
                _uiState.update { it.copy(space = detail, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Could not load Study Space") }
            }
        }
    }
}

@Composable
fun StudySpaceScreen(
    onNavigateBack: () -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: StudySpaceViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val space = uiState.space

    Scaffold(
        topBar = {
            WebTopBar(
                title = space?.title ?: "Study Space",
                subtitle = space?.memberRole ?: "Collaborative learning",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        when {
            uiState.isLoading -> {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            uiState.error != null -> {
                WebEmptyState(
                    title = "Could not open space",
                    message = uiState.error ?: "Try again later.",
                    icon = painterResource(id = R.drawable.ic_science),
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)
                )
            }
            space != null -> {
                val readyDocumentCount = space.documents.count { it.parseStatus == "ready" }
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item { StudySpaceHeader(space) }
                    item {
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                            WebKpiCard(
                                label = "Documents",
                                value = "${space.docCount}",
                                detail = "$readyDocumentCount ready",
                                painter = painterResource(id = R.drawable.ic_document),
                                modifier = Modifier.weight(1f)
                            )
                            WebKpiCard(
                                label = "Quizzes",
                                value = "${space.quizzes.size}",
                                detail = "${space.quizzes.sumOf { it.attemptCount }} attempts",
                                painter = painterResource(id = R.drawable.ic_school),
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                    item {
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                            WebKpiCard(
                                label = "Flashcards",
                                value = "${space.flashcardCount}",
                                detail = "${space.flashcards.size} loaded",
                                painter = painterResource(id = R.drawable.ic_book),
                                modifier = Modifier.weight(1f)
                            )
                            WebKpiCard(
                                label = "Members",
                                value = "${space.memberCount.coerceAtLeast(1)}",
                                detail = "${space.activeNow} active now",
                                painter = painterResource(id = R.drawable.ic_forum_outlined),
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                    item { WebSectionHeader(title = "Documents", modifier = Modifier.padding(horizontal = 0.dp)) }
                    if (space.documents.isEmpty()) {
                        item {
                            WebEmptyState(
                                title = "No documents",
                                message = "Upload and generated study material will appear here.",
                                icon = painterResource(id = R.drawable.ic_document)
                            )
                        }
                    } else {
                        items(space.documents, key = { it.id }) { doc ->
                            StudyDocumentRow(doc)
                        }
                    }
                    item { WebSectionHeader(title = "AI Outputs", modifier = Modifier.padding(horizontal = 0.dp)) }
                    item {
                        AiOutputPanel(space)
                    }
                    item { Spacer(modifier = Modifier.height(32.dp)) }
                }
            }
        }
    }
}

@Composable
private fun StudySpaceHeader(space: ApiStudySpaceDetail) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(
                text = space.title,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.ExtraBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
            if (space.description.isNotBlank()) {
                Text(
                    text = space.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis
                )
            }
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                WebChip(text = space.visibility.replaceFirstChar { it.uppercase() }, selected = space.visibility == "public")
                if (space.inviteCode.isNotBlank()) WebChip(text = "Code ${space.inviteCode}")
                WebChip(text = "Updated ${formatTimeAgo(space.updatedAt)}")
            }
        }
    }
}

@Composable
private fun StudyDocumentRow(doc: ApiStudyDocument) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Icon(
                painter = painterResource(id = R.drawable.ic_document),
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(24.dp)
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = doc.title.ifBlank { doc.fileName.ifBlank { "Untitled" } },
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = listOf(doc.parseStatus.ifBlank { "pending" }, fileSizeLabel(doc.fileSize), "${doc.parsedTextLength} chars")
                        .filter { it.isNotBlank() }
                        .joinToString(" - "),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

@Composable
private fun AiOutputPanel(space: ApiStudySpaceDetail) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                WebChip(text = "Summaries", selected = space.documents.any { it.summaryCompact.isNotBlank() || it.summaryDetailed.isNotBlank() })
                WebChip(text = "Mindmaps", selected = space.documents.any { it.mindmapJson.isNotBlank() })
                WebChip(text = "Quizzes", selected = space.quizzes.isNotEmpty())
            }
            Text(
                text = "Native generation controls are wired through the same Study Space model and can be expanded next to upload, generate, and review flows.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
