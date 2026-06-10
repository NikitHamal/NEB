package com.neb.ians.ui.screens.study

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.neb.ians.R
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.api.ApiStudySpace
import com.neb.ians.data.api.ApiStudySpaceCreateRequest
import com.neb.ians.data.api.ApiStudySpaceJoinRequest
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.ui.components.WebChip
import com.neb.ians.ui.components.WebEmptyState
import com.neb.ians.ui.components.WebOutlinedButton
import com.neb.ians.ui.components.WebPanelShape
import com.neb.ians.ui.components.WebPrimaryButton
import com.neb.ians.ui.components.WebTopBar
import com.neb.ians.util.formatTimeAgo
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StudyLabUiState(
    val mySpaces: List<ApiStudySpace> = emptyList(),
    val publicSpaces: List<ApiStudySpace> = emptyList(),
    val selectedTab: String = "mine",
    val isLoading: Boolean = true,
    val isBusy: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class StudyLabViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(StudyLabUiState())
    val uiState: StateFlow<StudyLabUiState> = _uiState.asStateFlow()

    init {
        refresh()
    }

    fun refresh() {
        viewModelScope.launch {
            val token = authRepository.getBearerToken()
            if (token == null) {
                _uiState.update { it.copy(isLoading = false, error = "Sign in to use Study Lab") }
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val mine = apiService.getStudySpaces(token).spaces
                val public = apiService.getPublicStudySpaces(token, sort = "recent").spaces
                _uiState.update { it.copy(mySpaces = mine, publicSpaces = public, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.localizedMessage ?: "Failed to load Study Lab") }
            }
        }
    }

    fun selectTab(tab: String) {
        _uiState.update { it.copy(selectedTab = tab) }
    }

    fun createSpace(title: String, description: String, onCreated: (String) -> Unit) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isBusy = true, error = null) }
            try {
                val created = apiService.createStudySpace(token, ApiStudySpaceCreateRequest(title, description))
                _uiState.update { it.copy(isBusy = false) }
                onCreated(created.id)
            } catch (e: Exception) {
                _uiState.update { it.copy(isBusy = false, error = e.localizedMessage ?: "Could not create study space") }
            }
        }
    }

    fun joinCode(code: String, onJoined: (String) -> Unit) {
        viewModelScope.launch {
            val token = authRepository.getBearerToken() ?: return@launch
            _uiState.update { it.copy(isBusy = true, error = null) }
            try {
                val response = apiService.joinStudySpaceByCode(token, ApiStudySpaceJoinRequest(code.trim().uppercase()))
                val id = response.space?.id ?: response.spaceId
                _uiState.update { it.copy(isBusy = false) }
                if (id != null) onJoined(id) else refresh()
            } catch (e: Exception) {
                _uiState.update { it.copy(isBusy = false, error = e.localizedMessage ?: "Could not join study space") }
            }
        }
    }
}

@Composable
fun StudyLabScreen(
    onNavigateBack: () -> Unit,
    onOpenSpace: (String) -> Unit,
    onSearchClick: () -> Unit = {},
    viewModel: StudyLabViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showCreate by remember { mutableStateOf(false) }
    var showJoin by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            WebTopBar(
                title = "Study Lab",
                subtitle = "AI-powered spaces",
                showBack = true,
                onBackClick = onNavigateBack,
                onSearchClick = onSearchClick
            )
        },
        containerColor = MaterialTheme.colorScheme.surface
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Study Lab",
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.ExtraBold
                    )
                    Text(
                        text = "Create study spaces, organize notes, and generate summaries, mindmaps, quizzes, and flashcards.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 3,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }

            Row(
                modifier = Modifier.padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                WebPrimaryButton(text = "New Space", imageVector = Icons.Filled.Add, onClick = { showCreate = true })
                WebOutlinedButton(text = "Join Code", painter = painterResource(id = R.drawable.ic_school), onClick = { showJoin = true })
            }

            Row(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                WebChip(text = "My spaces", selected = uiState.selectedTab == "mine", onClick = { viewModel.selectTab("mine") })
                WebChip(text = "Public spaces", selected = uiState.selectedTab == "public", onClick = { viewModel.selectTab("public") })
            }

            if (uiState.error != null) {
                Text(
                    text = uiState.error ?: "",
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error
                )
            }

            when {
                uiState.isLoading -> {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(40.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        CircularProgressIndicator()
                    }
                }
                uiState.selectedTab == "mine" -> SpaceList(
                    spaces = uiState.mySpaces,
                    emptyTitle = "No study spaces yet",
                    emptyMessage = "Create a space for your notes, PDFs, quizzes, and flashcards.",
                    onOpenSpace = onOpenSpace
                )
                else -> SpaceList(
                    spaces = uiState.publicSpaces,
                    emptyTitle = "No public spaces yet",
                    emptyMessage = "Public study spaces from the community will appear here.",
                    onOpenSpace = onOpenSpace
                )
            }
        }
    }

    if (showCreate) {
        CreateSpaceDialog(
            busy = uiState.isBusy,
            onDismiss = { showCreate = false },
            onCreate = { title, description ->
                viewModel.createSpace(title, description) { id ->
                    showCreate = false
                    onOpenSpace(id)
                }
            }
        )
    }
    if (showJoin) {
        JoinCodeDialog(
            busy = uiState.isBusy,
            onDismiss = { showJoin = false },
            onJoin = { code ->
                viewModel.joinCode(code) { id ->
                    showJoin = false
                    onOpenSpace(id)
                }
            }
        )
    }
}

@Composable
private fun SpaceList(
    spaces: List<ApiStudySpace>,
    emptyTitle: String,
    emptyMessage: String,
    onOpenSpace: (String) -> Unit
) {
    if (spaces.isEmpty()) {
        WebEmptyState(
            title = emptyTitle,
            message = emptyMessage,
            icon = painterResource(id = R.drawable.ic_science),
            modifier = Modifier.padding(16.dp)
        )
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 4.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(spaces, key = { it.id }) { space ->
                StudySpaceCard(space = space, onClick = { onOpenSpace(space.id) })
            }
            item { Spacer(modifier = Modifier.height(32.dp)) }
        }
    }
}

@Composable
private fun StudySpaceCard(space: ApiStudySpace, onClick: () -> Unit) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = WebPanelShape,
        color = MaterialTheme.colorScheme.surfaceContainerLowest,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                Icon(
                    painter = painterResource(id = R.drawable.ic_science),
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(26.dp)
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = space.title,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = space.description.ifBlank { "Study space" },
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                if (space.visibility == "public") WebChip(text = "Public", selected = true)
                if (space.hasSummary) WebChip(text = "Summary")
                if (space.hasMindmap) WebChip(text = "Mindmap")
                if (space.hasQuiz) WebChip(text = "Quiz")
            }
            Text(
                text = "${space.docCount} docs - ${space.memberCount.coerceAtLeast(1)} members - ${formatTimeAgo(space.updatedAt)}",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

@Composable
private fun CreateSpaceDialog(
    busy: Boolean,
    onDismiss: () -> Unit,
    onCreate: (String, String) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("New Study Space") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it.take(200) },
                    label = { Text("Title") },
                    singleLine = true
                )
                OutlinedTextField(
                    value = description,
                    onValueChange = { description = it.take(2000) },
                    label = { Text("Description") },
                    minLines = 3
                )
            }
        },
        confirmButton = {
            TextButton(
                enabled = title.isNotBlank() && !busy,
                onClick = { onCreate(title.trim(), description.trim()) }
            ) { Text("Create") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

@Composable
private fun JoinCodeDialog(
    busy: Boolean,
    onDismiss: () -> Unit,
    onJoin: (String) -> Unit
) {
    var code by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Join Study Space") },
        text = {
            OutlinedTextField(
                value = code,
                onValueChange = { code = it.uppercase().filter(Char::isLetterOrDigit).take(12) },
                label = { Text("Invite code") },
                singleLine = true
            )
        },
        confirmButton = {
            TextButton(
                enabled = code.isNotBlank() && !busy,
                onClick = { onJoin(code) }
            ) { Text("Join") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}
