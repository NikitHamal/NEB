package com.consica.code.ui.screens.playground

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Save
import androidx.compose.material.icons.filled.Spa
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.AppContainer
import com.consica.code.R
import com.consica.code.core.designsystem.PillShape
import com.consica.code.core.model.AgeGroup
import com.consica.code.core.model.CodeLanguage
import com.consica.code.core.model.Lesson
import com.consica.code.core.model.RunResult
import com.consica.code.data.content.LessonCatalog
import com.consica.code.data.prefs.UserState
import com.consica.code.runtime.ChallengeValidator
import com.consica.code.ui.common.EcoCard
import com.consica.code.ui.common.appViewModel
import com.consica.code.ui.screens.ecosystem.EcosystemResultView
import com.consica.code.util.SoundManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

data class PlaygroundUiState(
    val initialCode: String = "",
    val language: CodeLanguage = CodeLanguage.PYTHON,
    val running: Boolean = false,
    val runResult: RunResult? = null,
    val challengePassed: Boolean = false,
    val showOutput: Boolean = false,
    val showHint: Boolean = false,
    val rewardsClaimed: Boolean = false,
    val workspaceLoaded: Boolean = false,
    val savedToast: Boolean = false,
)

class PlaygroundViewModel(
    private val container: AppContainer,
    lessonId: String?,
    private val workspaceId: Long?,
) : ViewModel() {

    val lesson: Lesson? = lessonId?.let { LessonCatalog.byId[it] }

    val user: StateFlow<UserState?> = container.prefs.userState
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    private val _state = MutableStateFlow(
        PlaygroundUiState(
            initialCode = lesson?.challenge?.starterCode ?: "",
            language = lesson?.challenge?.language ?: lesson?.language ?: CodeLanguage.PYTHON,
            workspaceLoaded = workspaceId == null,
        ),
    )
    val state: StateFlow<PlaygroundUiState> = _state

    init {
        if (workspaceId != null) {
            viewModelScope.launch {
                val ws = container.workspaces.get(workspaceId)
                if (ws != null) {
                    _state.value = _state.value.copy(
                        initialCode = ws.code,
                        language = CodeLanguage.entries.firstOrNull { it.name == ws.language }
                            ?: CodeLanguage.PYTHON,
                        workspaceLoaded = true,
                    )
                } else {
                    _state.value = _state.value.copy(workspaceLoaded = true)
                }
            }
        }
    }

    fun setLanguage(language: CodeLanguage) {
        if (lesson == null) {
            _state.value = _state.value.copy(language = language)
        }
    }

    fun toggleHint() {
        _state.value = _state.value.copy(showHint = !_state.value.showHint)
    }

    fun run(code: String) {
        if (_state.value.running) return
        _state.value = _state.value.copy(running = true)
        viewModelScope.launch {
            val language = _state.value.language
            val result = withContext(Dispatchers.Default) {
                ChallengeValidator.execute(language, code)
            }
            val challenge = lesson?.challenge
            val passed = if (challenge != null) {
                ChallengeValidator.validate(challenge, code, result).passed
            } else {
                result.success
            }
            container.learning.logRun(
                language = language.name,
                code = code,
                output = result.output.take(4000),
                success = result.success,
                lessonId = lesson?.id,
                workspaceId = workspaceId,
            )
            lesson?.let { container.learning.recordAttempt(it.id, code) }
            workspaceId?.let { container.workspaces.saveCode(it, code) }

            container.sound.play(
                when {
                    challenge != null && passed -> SoundManager.Effect.GROW
                    result.success -> SoundManager.Effect.SUCCESS
                    else -> SoundManager.Effect.GENTLE_ERROR
                },
            )
            _state.value = _state.value.copy(
                running = false,
                runResult = result,
                challengePassed = passed,
                showOutput = true,
            )
        }
    }

    fun backToCode() {
        _state.value = _state.value.copy(showOutput = false)
    }

    fun claimRewards(code: String, onDone: () -> Unit) {
        val l = lesson ?: return
        if (_state.value.rewardsClaimed) return
        _state.value = _state.value.copy(rewardsClaimed = true)
        viewModelScope.launch {
            container.learning.completeLesson(l, code)
            container.sound.play(SoundManager.Effect.REWARD)
            onDone()
        }
    }

    fun saveWorkspace(name: String, code: String) {
        viewModelScope.launch {
            if (workspaceId != null) {
                container.workspaces.saveCode(workspaceId, code)
                container.workspaces.rename(workspaceId, name)
            } else {
                container.workspaces.create(name, _state.value.language, code, lesson?.id)
            }
            _state.value = _state.value.copy(savedToast = true)
        }
    }
}

@Composable
fun PlaygroundScreen(
    lessonId: String?,
    workspaceId: Long?,
    onBack: () -> Unit,
    onLessonComplete: () -> Unit,
) {
    val viewModel = appViewModel(key = "playground_${lessonId}_$workspaceId") {
        PlaygroundViewModel(it, lessonId, workspaceId)
    }
    val state by viewModel.state.collectAsState()
    val user = viewModel.user.collectAsState().value ?: return
    val lesson = viewModel.lesson

    var codeField by remember(state.initialCode, state.workspaceLoaded) {
        mutableStateOf(TextFieldValue(state.initialCode))
    }
    var showSaveDialog by remember { mutableStateOf(false) }
    var showResetDialog by remember { mutableStateOf(false) }

    val professional = user.professionalEditor
    val isKid = user.ageGroup == AgeGroup.KIDS && !professional

    if (state.showOutput && state.runResult != null) {
        EcosystemResultView(
            runResult = state.runResult!!,
            language = state.language,
            code = codeField.text,
            user = user,
            challengePassed = state.challengePassed,
            hasChallenge = lesson?.challenge != null,
            successLabel = lesson?.challenge?.successLabel,
            rewardsClaimed = state.rewardsClaimed,
            onBackToCode = viewModel::backToCode,
            onClaimRewards = { viewModel.claimRewards(codeField.text, onLessonComplete) },
        )
        return
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .imePadding(),
    ) {
        // Top bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.action_back))
            }
            Text(
                text = lesson?.let { stringResource(it.titleRes) }
                    ?: stringResource(R.string.playground_title),
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.weight(1f),
                maxLines = 1,
            )
            if (user.proToolsUnlocked) {
                IconButton(onClick = { showSaveDialog = true }) {
                    Icon(Icons.Filled.Save, contentDescription = stringResource(R.string.playground_save_as))
                }
            }
            if (lesson?.challenge != null) {
                IconButton(onClick = { showResetDialog = true }) {
                    Icon(Icons.Filled.Refresh, contentDescription = stringResource(R.string.playground_reset_code))
                }
            }
        }

        // Language selector for free play
        if (lesson == null) {
            Row(
                modifier = Modifier.padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                CodeLanguage.entries.forEach { lang ->
                    FilterChip(
                        selected = state.language == lang,
                        onClick = { viewModel.setLanguage(lang) },
                        label = { Text(lang.name) },
                        shape = PillShape,
                    )
                }
            }
        }

        // Challenge instruction
        val challenge = lesson?.challenge
        if (challenge != null) {
            EcoCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 6.dp),
                containerColor = MaterialTheme.colorScheme.secondaryContainer,
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text(
                        stringResource(R.string.playground_challenge_goal),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                    )
                    Text(
                        stringResource(challenge.instruction.resFor(user.ageGroup)),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSecondaryContainer,
                    )
                }
            }
        }

        // Hint bubble
        if (state.showHint && challenge != null) {
            EcoCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                containerColor = MaterialTheme.colorScheme.tertiaryContainer,
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text(
                        stringResource(
                            when (user.ageGroup) {
                                AgeGroup.KIDS -> R.string.terra_hint_intro_kids
                                AgeGroup.TEENS -> R.string.terra_hint_intro_teens
                                AgeGroup.PRO -> R.string.terra_hint_intro_pro
                            },
                        ),
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onTertiaryContainer,
                    )
                    Text(
                        stringResource(challenge.hint.resFor(user.ageGroup)),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onTertiaryContainer,
                    )
                }
            }
        }

        // Editor
        CodeEditor(
            value = codeField,
            onValueChange = { codeField = it },
            language = state.language,
            showLineNumbers = professional,
            errorLine = state.runResult?.errorLine,
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 6.dp),
        )

        // Snippet keyboard
        CodingKeyboard(
            language = state.language,
            ageGroup = user.ageGroup,
            professional = professional,
            onKey = { key -> codeField = codeField.insertSnippet(key.insert, key.cursorBack) },
            modifier = Modifier.padding(horizontal = 16.dp),
        )

        // Bottom action bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            if (challenge != null) {
                IconButton(onClick = viewModel::toggleHint) {
                    Icon(
                        Icons.Filled.Lightbulb,
                        contentDescription = stringResource(R.string.playground_hint),
                        tint = MaterialTheme.colorScheme.tertiary,
                    )
                }
            }
            Button(
                onClick = { viewModel.run(codeField.text) },
                enabled = !state.running,
                shape = PillShape,
                modifier = Modifier
                    .weight(1f)
                    .height(54.dp),
            ) {
                Icon(
                    if (isKid) Icons.Filled.Spa else Icons.Filled.PlayArrow,
                    contentDescription = stringResource(R.string.a11y_run_code),
                    modifier = Modifier.width(20.dp),
                )
                Box(Modifier.width(8.dp))
                Text(
                    text = when {
                        state.running -> stringResource(R.string.playground_running)
                        isKid -> stringResource(R.string.playground_grow)
                        else -> stringResource(R.string.playground_run)
                    },
                    style = MaterialTheme.typography.labelLarge,
                )
            }
        }
    }

    if (showSaveDialog) {
        var name by remember {
            mutableStateOf(lesson?.let { "" } ?: "")
        }
        AlertDialog(
            onDismissRequest = { showSaveDialog = false },
            title = { Text(stringResource(R.string.playground_save_as)) },
            text = {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text(stringResource(R.string.playground_workspace_name)) },
                    singleLine = true,
                )
            },
            confirmButton = {
                TextButton(
                    onClick = {
                        if (name.isNotBlank()) {
                            viewModel.saveWorkspace(name.trim(), codeField.text)
                            showSaveDialog = false
                        }
                    },
                ) { Text(stringResource(R.string.action_save)) }
            },
            dismissButton = {
                TextButton(onClick = { showSaveDialog = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }

    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text(stringResource(R.string.playground_reset_code)) },
            text = { Text(stringResource(R.string.playground_reset_confirm)) },
            confirmButton = {
                TextButton(
                    onClick = {
                        codeField = TextFieldValue(lesson?.challenge?.starterCode ?: "")
                        showResetDialog = false
                    },
                ) { Text(stringResource(R.string.action_reset)) }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) {
                    Text(stringResource(R.string.action_cancel))
                }
            },
        )
    }
}
