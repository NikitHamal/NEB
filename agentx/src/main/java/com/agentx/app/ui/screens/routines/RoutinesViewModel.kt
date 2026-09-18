package com.agentx.app.ui.screens.routines

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.RoutineEntity
import com.agentx.app.data.engine.NeedleRuntime
import com.agentx.app.data.tools.AxScheduler
import com.agentx.app.data.tools.RoutineHandler
import com.agentx.app.data.tools.RoutineRunner
import com.agentx.app.data.tools.ToolCatalog
import dagger.hilt.android.lifecycle.HiltViewModel
import java.util.UUID
import javax.inject.Inject
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

@HiltViewModel
class RoutinesViewModel @Inject constructor(
    private val routineDao: RoutineDao,
    private val routineHandler: RoutineHandler,
    private val runner: RoutineRunner,
    private val scheduler: AxScheduler,
    private val runtime: NeedleRuntime
) : ViewModel() {

    val routines: StateFlow<List<RoutineEntity>> =
        routineDao.observeAll().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    private val _busy = MutableStateFlow(false)
    val busy: StateFlow<Boolean> = _busy.asStateFlow()

    private val _message = MutableSharedFlow<String>(extraBufferCapacity = 1)
    val message: SharedFlow<String> = _message

    data class Draft(val name: String, val steps: List<ToolCallSpec>)

    private val _draft = MutableStateFlow<Draft?>(null)
    val draft: StateFlow<Draft?> = _draft.asStateFlow()

    fun generateDraft(name: String, description: String) {
        if (name.isBlank() || description.isBlank() || _busy.value) return
        viewModelScope.launch {
            _busy.value = true
            try {
                val cleanName = name.trim()
                val prompt = "Define the device routine named " + cleanName + ". The user wants: " +
                    description.trim() + ". Steps is a JSON array; each step has a tool name from the catalog " +
                    "and an args object. Reply with exactly one create_routine call for this routine."
                var draft = requestDraft(prompt, cleanName)
                if (draft == null) {
                    val repair = "Your last create_routine call had steps I could not parse. " +
                        "Steps must be a JSON array of objects, each with a tool name and an args object. " +
                        "Reply with exactly one corrected create_routine call for routine " + cleanName + "."
                    draft = requestDraft(repair, cleanName)
                }
                if (draft == null) {
                    _message.emit("I could not turn that into routine steps. Try a simpler description with concrete actions.")
                    return@launch
                }
                _draft.value = draft
            } finally {
                _busy.value = false
            }
        }
    }

    private suspend fun requestDraft(prompt: String, fallbackName: String): Draft? {
        val outcome = runtime.runAndAwait(UUID.randomUUID().toString(), prompt, 90_000L) ?: return null
        val parsed = com.agentx.app.data.engine.parseEngineResult(outcome.resultJson) ?: return null
        val call = parsed.function_calls.firstOrNull { it.name == "create_routine" } ?: return null
        val args = call.stringArgs()
        val stepsRaw = args["steps"].orEmpty()
        if (stepsRaw.isBlank()) return null
        val steps = runner.parseSteps(stepsRaw) ?: return null
        val draftName = args["name"]?.takeIf { it.isNotBlank() } ?: fallbackName
        return Draft(draftName, steps)
    }

    fun stepTitle(step: ToolCallSpec): String {
        val meta = ToolCatalog.metas[step.name] ?: return step.name
        val hint = step.args.values.firstOrNull { it.isNotBlank() }?.take(28)
        return if (hint != null) meta.title + " - " + hint else meta.title
    }

    fun saveDraft(hour: Int = -1, minute: Int = 0, days: Int = 0) {
        val current = _draft.value ?: return
        viewModelScope.launch {
            _busy.value = true
            try {
                val spec = ToolCallSpec(
                    "create_routine",
                    mapOf("name" to current.name, "steps" to runner.stepsToJson(current.steps))
                )
                val result = routineHandler.create(spec)
                if (!result.ok) {
                    _message.emit(result.message)
                    return@launch
                }
                if (hour >= 0) {
                    routineHandler.findByName(current.name)?.let { saved ->
                        val updated = saved.copy(scheduleHour = hour, scheduleMinute = minute, scheduleDays = days)
                        routineDao.update(updated)
                        scheduler.scheduleRoutine(updated)
                    }
                }
                _draft.value = null
                _message.emit("Routine " + current.name + " saved")
            } finally {
                _busy.value = false
            }
        }
    }

    fun clearDraft() {
        _draft.value = null
    }

    fun run(id: Long) {
        if (_busy.value) return
        viewModelScope.launch {
            _busy.value = true
            try {
                val outcomes = runner.runNow(id, background = false)
                val done = outcomes.count { it.ok }
                _message.emit(done.toString() + "/" + outcomes.size + " steps done")
            } finally {
                _busy.value = false
            }
        }
    }

    fun delete(routine: RoutineEntity) {
        viewModelScope.launch {
            scheduler.cancelRoutine(routine.id)
            routineDao.delete(routine.id)
        }
    }

    fun saveSchedule(routine: RoutineEntity, hour: Int, minute: Int, days: Int) {
        viewModelScope.launch {
            val updated = routine.copy(scheduleHour = hour, scheduleMinute = minute, scheduleDays = days)
            routineDao.update(updated)
            scheduler.scheduleRoutine(updated)
            _message.emit("Schedule saved")
        }
    }

    fun clearSchedule(routine: RoutineEntity) {
        viewModelScope.launch {
            scheduler.cancelRoutine(routine.id)
            routineDao.update(routine.copy(scheduleHour = -1, scheduleMinute = -1, scheduleDays = 0))
            _message.emit("Schedule cleared")
        }
    }
}
