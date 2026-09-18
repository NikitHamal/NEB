package com.agentx.app.ui.screens.chat

import android.content.Context
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.chat.AxToolCallRecord
import com.agentx.app.data.chat.ChatRepository
import com.agentx.app.data.chat.UiChatMessage
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.NeedleModelManager
import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.engine.NeedleRuntimeState
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.engine.parseEngineResult
import com.agentx.app.data.engine.toSpec
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.entity.ActivityEntity
import com.agentx.app.data.repository.SettingsRepository
import com.agentx.app.data.tools.ToolCatalog
import com.agentx.app.data.tools.ToolExecution
import com.agentx.app.data.tools.ToolExecutor
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class ChatViewModel @Inject constructor(
    private val manager: NeedleModelManager,
    private val runtime: NeedleRuntime,
    private val chatRepo: ChatRepository,
    private val executor: ToolExecutor,
    private val activityDao: ActivityDao,
    private val settings: SettingsRepository,
    @ApplicationContext private val context: Context,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val argId: String = savedStateHandle["conversationId"] ?: "new"

    val modelState = manager.state
    val runtimeState = runtime.state

    private val _conversationId = MutableStateFlow<String?>(if (argId == "new") null else argId)
    val conversationId: StateFlow<String?> = _conversationId.asStateFlow()

    private val _title = MutableStateFlow("New chat")
    val title: StateFlow<String> = _title.asStateFlow()

    val messages: StateFlow<List<UiChatMessage>> = conversationId.flatMapLatest { id ->
        if (id == null) flowOf(emptyList()) else chatRepo.observeMessages(id)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    private val _running = MutableStateFlow(false)
    val running: StateFlow<Boolean> = _running.asStateFlow()

    data class PendingConfirm(val spec: ToolCallSpec, val confidence: Double?)

    private val _pendingConfirm = MutableStateFlow<PendingConfirm?>(null)
    val pendingConfirm: StateFlow<PendingConfirm?> = _pendingConfirm.asStateFlow()

    private val _permissionAsk = MutableSharedFlow<String>(extraBufferCapacity = 1)
    val permissionAsk: SharedFlow<String> = _permissionAsk.asSharedFlow()

    private val _stalled = MutableStateFlow(false)
    val stalled: StateFlow<Boolean> = _stalled.asStateFlow()
    private var stallJob: Job? = null

    private var pendingRetry: ToolCallSpec? = null
    private var pendingRetryConfidence: Double? = null

    init {
        runtime.setToolsJson(ToolCatalog.buildJson())
        viewModelScope.launch {
            manager.state.collect { state ->
                if (state is AxModelState.Ready) runtime.prepare()
            }
        }
        viewModelScope.launch {
            runtime.errors.collect { (id, message) ->
                if (id == null) {
                    _conversationId.value?.let { chatRepo.addAssistantMessage(it, "Engine error: " + message) }
                }
            }
        }
        viewModelScope.launch {
            runtime.state.collect { state ->
                stallJob?.cancel()
                stallJob = null
                _stalled.value = false
                if (state is NeedleRuntimeState.Loading) {
                    stallJob = viewModelScope.launch {
                        delay(90_000)
                        if (runtime.state.value is NeedleRuntimeState.Loading) {
                            _stalled.value = true
                        }
                    }
                }
            }
        }
        viewModelScope.launch { refreshTitle() }
    }

    fun retryEngine() {
        stallJob?.cancel()
        stallJob = null
        _stalled.value = false
        runtime.restart()
    }

    private suspend fun refreshTitle() {
        val id = _conversationId.value ?: return
        chatRepo.conversation(id)?.let { _title.value = it.title.ifBlank { "New chat" } }
    }

    private suspend fun ensureConversation(): String {
        _conversationId.value?.let { return it }
        val id = chatRepo.createConversation()
        _conversationId.value = id
        return id
    }

    fun send(rawInput: String) {
        val input = rawInput.trim()
        if (input.isEmpty() || _running.value) return
        if (input.startsWith("action:")) {
            handleLocalAction(input)
            return
        }
        viewModelScope.launch {
            _running.value = true
            try {
                val id = ensureConversation()
                val isFirst = (chatRepo.conversation(id)?.messageCount ?: 0) == 0
                chatRepo.addUserMessage(id, input)
                if (isFirst) {
                    chatRepo.retitleFromFirstMessage(id, input)
                    refreshTitle()
                }
                val runId = java.util.UUID.randomUUID().toString()
                val outcome = runtime.runAndAwait(runId, input)
                if (outcome == null) {
                    chatRepo.addAssistantMessage(id, "The engine is still starting. Try again in a moment.")
                    return@launch
                }
                val parsed = parseEngineResult(outcome.resultJson)
                if (parsed == null) {
                    chatRepo.addAssistantMessage(id, "I could not understand the engine reply. Try rephrasing.")
                    return@launch
                }
                val calls = parsed.function_calls.filter { it.name.isNotBlank() }.map { it.toSpec() }
                if (calls.isEmpty()) {
                    handleEmptyResult(id, parsed.suppressed_calls.map { it.toSpec() }, parsed.reasoning)
                    return@launch
                }
                handleCalls(id, input, calls, parsed.confidence, parsed.reasoning, outcome.durationMs)
            } finally {
                _running.value = false
            }
        }
    }

    private suspend fun handleCalls(
        conversationId: String,
        input: String,
        calls: List<ToolCallSpec>,
        confidence: Double?,
        reasoning: String?,
        durationMs: Double
    ) {
        val confirmDestructive = settings.confirmDestructive.first()
        val threshold = settings.confirmThreshold.first().toDouble()
        for (spec in calls) {
            val meta = ToolCatalog.metas[spec.name]
            if (meta == null) {
                chatRepo.addAssistantMessage(conversationId, "Unknown action " + spec.name)
                continue
            }
            val conf = confidence ?: 1.0
            val mustConfirm = meta.confirmAlways && confirmDestructive
            when {
                mustConfirm -> _pendingConfirm.value = PendingConfirm(spec, confidence)
                conf >= SettingsRepository.ACT_THRESHOLD -> {
                    var result = executor.execute(spec)
                    if (!result.ok && result.repairable) {
                        result = attemptRepair(input, result)
                    }
                    recordExecution(conversationId, spec, confidence, durationMs, reasoning, result)
                }
                conf >= threshold -> _pendingConfirm.value = PendingConfirm(spec, confidence)
                else -> {
                    pendingRetry = spec
                    pendingRetryConfidence = confidence
                    chatRepo.addAssistantMessage(
                        conversationId,
                        "Not sure I got that. I think you want: " + meta.title + " (" + (conf * 100).toInt() + "% confident).",
                        reasoning, confidence,
                        options = listOf("action:force_run")
                    )
                }
            }
            if (_pendingConfirm.value != null) break
        }
    }

    private suspend fun handleEmptyResult(conversationId: String, suppressed: List<ToolCallSpec>, reasoning: String?) {
        if (suppressed.isNotEmpty()) {
            val guess = suppressed.first()
            val meta = ToolCatalog.metas[guess.name]
            pendingRetry = guess
            pendingRetryConfidence = null
            val what = if (meta != null) meta.title else guess.name
            chatRepo.addAssistantMessage(
                conversationId,
                "I held that back - it looks off-topic for this device. My guess was: " + what + ".",
                reasoning, options = listOf("action:force_run")
            )
            return
        }
        chatRepo.addAssistantMessage(
            conversationId,
            "I can only act on this device, fully offline: settings and sound, apps, calls and texts, alarms and timers, reminders, notes, routines and device status. Try one of those.",
            reasoning,
            options = listOf("Show device status", "List my routines")
        )
    }

    fun confirmPending() {
        val pending = _pendingConfirm.value ?: return
        val id = _conversationId.value ?: return
        _pendingConfirm.value = null
        viewModelScope.launch {
            executeAndRecord(id, pending.spec, pending.confidence, 0.0, null)
        }
    }

    fun dismissPending() {
        val pending = _pendingConfirm.value ?: return
        val id = _conversationId.value
        _pendingConfirm.value = null
        if (id == null) return
        viewModelScope.launch {
            val meta = ToolCatalog.metas[pending.spec.name]
            activityDao.insert(
                ActivityEntity(
                    kind = "tool",
                    label = "Skipped " + (meta?.title ?: pending.spec.name),
                    detailJson = specToJson(pending.spec),
                    confidence = pending.confidence,
                    status = "denied"
                )
            )
            chatRepo.addAssistantMessage(id, "Skipped. Nothing was changed.")
        }
    }

    private suspend fun attemptRepair(input: String, failed: ToolExecution): ToolExecution {
        val hint = failed.repairHint ?: return failed
        val retryQuery = input + " (Correction: " + hint + " Reply with one corrected call.)"
        val outcome = runtime.runAndAwait(java.util.UUID.randomUUID().toString(), retryQuery, 60_000L)
            ?: return failed
        val parsed = parseEngineResult(outcome.resultJson) ?: return failed
        val calls = parsed.function_calls.filter { it.name.isNotBlank() }.map { it.toSpec() }
        if (calls.isEmpty()) return failed
        return executor.execute(calls.first())
    }

    private suspend fun executeAndRecord(
        conversationId: String,
        spec: ToolCallSpec,
        confidence: Double?,
        durationMs: Double,
        reasoning: String?
    ) {
        recordExecution(conversationId, spec, confidence, durationMs, reasoning, executor.execute(spec))
    }

    private suspend fun recordExecution(
        conversationId: String,
        spec: ToolCallSpec,
        confidence: Double?,
        durationMs: Double,
        reasoning: String?,
        result: ToolExecution
    ) {
        if (result.needsPermission != null) {
            pendingRetry = spec
            pendingRetryConfidence = confidence
            if (isSpecialPermission(result.needsPermission)) {
                chatRepo.addAssistantMessage(
                    conversationId, result.message,
                    options = listOf("action:open_settings:" + result.needsPermission)
                )
            } else {
                chatRepo.addAssistantMessage(
                    conversationId,
                    result.message + ". Grant " + (result.permissionLabel ?: "the permission") + " to continue.",
                    options = listOf("action:retry")
                )
                _permissionAsk.emit(result.needsPermission)
            }
            logActivity(spec, confidence, result, "denied")
            return
        }
        chatRepo.addAssistantMessage(
            conversationId,
            result.message,
            reasoning,
            confidence,
            durationMs.takeIf { it > 0 },
            toolCalls = listOf(AxToolCallRecord(spec.name, specToJson(spec.args))),
            options = result.options
        )
        logActivity(spec, confidence, result, if (result.ok) "done" else "failed")
    }

    private suspend fun logActivity(spec: ToolCallSpec, confidence: Double?, result: ToolExecution, status: String) {
        val meta = ToolCatalog.metas[spec.name]
        activityDao.insert(
            ActivityEntity(
                kind = "tool",
                label = (meta?.title ?: spec.name) + " - " + result.message.take(120),
                detailJson = specToJson(spec),
                confidence = confidence,
                status = status
            )
        )
        activityDao.trim()
    }

    fun onPermissionResult(permission: String, granted: Boolean) {
        val id = _conversationId.value
        if (!granted) {
            if (id == null) return
            viewModelScope.launch {
                chatRepo.addAssistantMessage(
                    id,
                    PermissionUtils.labelFor(permission) + " was denied. You can grant it later from Settings.",
                    options = listOf("action:retry")
                )
            }
            return
        }
        val spec = pendingRetry ?: return
        if (id == null) return
        pendingRetry = null
        viewModelScope.launch {
            executeAndRecord(id, spec, pendingRetryConfidence, 0.0, null)
        }
    }

    private fun handleLocalAction(action: String) {
        viewModelScope.launch {
            val id = _conversationId.value
            when {
                action == "action:retry" -> {
                    if (id == null) return@launch
                    val spec = pendingRetry ?: return@launch
                    pendingRetry = null
                    _running.value = true
                    try {
                        executeAndRecord(id, spec, pendingRetryConfidence, 0.0, null)
                    } finally {
                        _running.value = false
                    }
                }
                action == "action:force_run" -> {
                    val spec = pendingRetry ?: return@launch
                    _pendingConfirm.value = PendingConfirm(spec, pendingRetryConfidence)
                }
                action.startsWith("action:open_settings:") -> {
                    if (id == null) return@launch
                    when (action.removePrefix("action:open_settings:")) {
                        PermissionUtils.SPECIAL_WRITE_SETTINGS -> PermissionUtils.openWriteSettings(context)
                        PermissionUtils.SPECIAL_DND_ACCESS -> PermissionUtils.openDndSettings(context)
                        PermissionUtils.SPECIAL_EXACT_ALARM -> PermissionUtils.openExactAlarmSettings(context)
                        else -> PermissionUtils.openAppSettings(context)
                    }
                    chatRepo.addAssistantMessage(
                        id,
                        "Settings opened. Flip the switch, come back, and tap retry.",
                        options = listOf("action:retry")
                    )
                }
            }
        }
    }

    private fun isSpecialPermission(permission: String): Boolean =
        permission == PermissionUtils.SPECIAL_WRITE_SETTINGS ||
            permission == PermissionUtils.SPECIAL_DND_ACCESS ||
            permission == PermissionUtils.SPECIAL_EXACT_ALARM

    private fun specToJson(spec: ToolCallSpec): String = specToJson(spec.args)

    private fun specToJson(args: Map<String, String>): String {
        if (args.isEmpty()) return "{}"
        return "{" + args.entries.joinToString(", ") { (key, value) -> key + ": " + value } + "}"
    }
}
