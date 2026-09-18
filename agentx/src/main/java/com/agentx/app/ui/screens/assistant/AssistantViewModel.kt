package com.agentx.app.ui.screens.assistant

import android.content.Context
import com.agentx.app.data.engine.AxModelState
import com.agentx.app.data.engine.AxMessage
import com.agentx.app.data.engine.AxToolCallRecord
import com.agentx.app.data.engine.NeedleChatStore
import com.agentx.app.data.engine.NeedleModelManager
import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.engine.parseEngineResult
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.entity.ActivityEntity
import com.agentx.app.data.repository.SettingsRepository
import com.agentx.app.data.tools.ToolCatalog
import com.agentx.app.data.tools.ToolExecution
import com.agentx.app.data.tools.ToolExecutor
import com.agentx.app.util.PermissionUtils
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.UUID
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@HiltViewModel
class AssistantViewModel @Inject constructor(
    private val manager: NeedleModelManager,
    private val runtime: NeedleRuntime,
    private val store: NeedleChatStore,
    private val executor: ToolExecutor,
    private val activityDao: ActivityDao,
    private val settings: SettingsRepository,
    @ApplicationContext private val context: Context
) : androidx.lifecycle.ViewModel() {

    val modelState = manager.state
    val runtimeState = runtime.state
    val messages = store.messages

    private val _running = MutableStateFlow(false)
    val running: StateFlow<Boolean> = _running.asStateFlow()

    data class PendingConfirm(val spec: ToolCallSpec, val confidence: Double?)

    private val _pendingConfirm = MutableStateFlow<PendingConfirm?>(null)
    val pendingConfirm: StateFlow<PendingConfirm?> = _pendingConfirm.asStateFlow()

    private val _permissionAsk = MutableSharedFlow<String>(extraBufferCapacity = 1)
    val permissionAsk: SharedFlow<String> = _permissionAsk.asSharedFlow()

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
                    store.add(AxMessage(id = uuid(), isUser = false, text = "Engine error: " + message))
                }
            }
        }
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
                store.add(AxMessage(id = uuid(), isUser = true, text = input))
                val outcome = runtime.runAndAwait(uuid(), input)
                if (outcome == null) {
                    store.add(AxMessage(id = uuid(), isUser = false, text = "The engine is still starting. Try again in a moment."))
                    return@launch
                }
                val parsed = parseEngineResult(outcome.resultJson)
                if (parsed == null) {
                    store.add(AxMessage(id = uuid(), isUser = false, text = "I could not understand the engine reply. Try rephrasing."))
                    return@launch
                }
                val calls = parsed.function_calls.filter { it.name.isNotBlank() }.map { it.toSpec() }
                if (calls.isEmpty()) {
                    handleEmptyResult(parsed.suppressed_calls.map { it.toSpec() }, parsed.reasoning)
                    return@launch
                }
                handleCalls(calls, parsed.confidence, parsed.reasoning, outcome.durationMs)
            } finally {
                _running.value = false
            }
        }
    }

    private suspend fun handleCalls(
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
                store.add(AxMessage(id = uuid(), isUser = false, text = "Unknown action " + spec.name))
                continue
            }
            val conf = confidence ?: 1.0
            val mustConfirm = meta.confirmAlways && confirmDestructive
            when {
                mustConfirm -> _pendingConfirm.value = PendingConfirm(spec, confidence)
                conf >= SettingsRepository.ACT_THRESHOLD -> executeAndRecord(spec, confidence, durationMs, reasoning)
                conf >= threshold -> _pendingConfirm.value = PendingConfirm(spec, confidence)
                else -> {
                    pendingRetry = spec
                    pendingRetryConfidence = confidence
                    store.add(
                        AxMessage(
                            id = uuid(),
                            isUser = false,
                            text = "Not sure I got that. I think you want: " + meta.title + " (" + (conf * 100).toInt() + "%).",
                            reasoning = reasoning,
                            confidence = confidence,
                            options = listOf("action:force_run")
                        )
                    )
                }
            }
            if (_pendingConfirm.value != null) break
        }
    }

    private suspend fun handleEmptyResult(suppressed: List<ToolCallSpec>, reasoning: String?) {
        if (suppressed.isNotEmpty()) {
            val guess = suppressed.first()
            val meta = ToolCatalog.metas[guess.name]
            pendingRetry = guess
            pendingRetryConfidence = null
            val what = if (meta != null) meta.title else guess.name
            store.add(
                AxMessage(
                    id = uuid(),
                    isUser = false,
                    text = "I held that back - it looks off-topic for this device. My guess was: " + what + ".",
                    reasoning = reasoning,
                    options = listOf("action:force_run")
                )
            )
            return
        }
        store.add(
            AxMessage(
                id = uuid(),
                isUser = false,
                text = "I can only act on this device, fully offline: settings and sound, apps, calls and texts, alarms and timers, reminders, notes, routines and device status. Try one of those.",
                reasoning = reasoning,
                options = listOf("Show device status", "List my routines")
            )
        )
    }

    fun confirmPending() {
        val pending = _pendingConfirm.value ?: return
        _pendingConfirm.value = null
        viewModelScope.launch {
            executeAndRecord(pending.spec, pending.confidence, 0.0, null)
        }
    }

    fun dismissPending() {
        val pending = _pendingConfirm.value ?: return
        _pendingConfirm.value = null
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
            store.add(AxMessage(id = uuid(), isUser = false, text = "Skipped. Nothing was changed."))
        }
    }

    private suspend fun executeAndRecord(spec: ToolCallSpec, confidence: Double?, durationMs: Double, reasoning: String?) {
        val meta = ToolCatalog.metas[spec.name]
        val result = executor.execute(spec)
        if (result.needsPermission != null) {
            pendingRetry = spec
            pendingRetryConfidence = confidence
            if (isSpecialPermission(result.needsPermission)) {
                store.add(
                    AxMessage(
                        id = uuid(),
                        isUser = false,
                        text = result.message,
                        options = listOf("action:open_settings:" + result.needsPermission)
                    )
                )
            } else {
                store.add(
                    AxMessage(
                        id = uuid(),
                        isUser = false,
                        text = result.message + ". Grant " + (result.permissionLabel ?: "the permission") + " to continue.",
                        options = listOf("action:retry")
                    )
                )
                _permissionAsk.emit(result.needsPermission)
            }
            logActivity(spec, confidence, result, "denied")
            return
        }
        store.add(
            AxMessage(
                id = uuid(),
                isUser = false,
                text = result.message,
                reasoning = reasoning,
                confidence = confidence,
                durationMs = durationMs.takeIf { it > 0 },
                toolCalls = listOf(AxToolCallRecord(spec.name, specToJson(spec.args))),
                options = result.options
            )
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
        if (!granted) {
            viewModelScope.launch {
                store.add(
                    AxMessage(
                        id = uuid(),
                        isUser = false,
                        text = PermissionUtils.labelFor(permission) + " was denied. You can grant it later from Settings.",
                        options = listOf("action:retry")
                    )
                )
            }
            return
        }
        val spec = pendingRetry ?: return
        pendingRetry = null
        viewModelScope.launch {
            executeAndRecord(spec, pendingRetryConfidence, 0.0, null)
        }
    }

    private fun handleLocalAction(action: String) {
        viewModelScope.launch {
            when {
                action == "action:retry" -> {
                    val spec = pendingRetry ?: return@launch
                    pendingRetry = null
                    _running.value = true
                    try {
                        executeAndRecord(spec, pendingRetryConfidence, 0.0, null)
                    } finally {
                        _running.value = false
                    }
                }
                action == "action:force_run" -> {
                    val spec = pendingRetry ?: return@launch
                    _pendingConfirm.value = PendingConfirm(spec, pendingRetryConfidence)
                }
                action.startsWith("action:open_settings:") -> {
                    when (action.removePrefix("action:open_settings:")) {
                        PermissionUtils.SPECIAL_WRITE_SETTINGS -> PermissionUtils.openWriteSettings(context)
                        PermissionUtils.SPECIAL_DND_ACCESS -> PermissionUtils.openDndSettings(context)
                        PermissionUtils.SPECIAL_EXACT_ALARM -> PermissionUtils.openExactAlarmSettings(context)
                        else -> PermissionUtils.openAppSettings(context)
                    }
                    store.add(
                        AxMessage(
                            id = uuid(),
                            isUser = false,
                            text = "Settings opened. Flip the switch, come back, and tap retry.",
                            options = listOf("action:retry")
                        )
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

    private fun uuid(): String = UUID.randomUUID().toString()

    fun clearChat() = store.clear()

    fun removeMessage(id: String) = store.remove(id)
}
