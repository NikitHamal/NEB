package com.agentx.app.data.tools

import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.RoutineEntity
import javax.inject.Inject
import javax.inject.Provider
import javax.inject.Singleton
import kotlinx.coroutines.flow.firstOrNull

@Singleton
class RoutineHandler @Inject constructor(
    private val dao: RoutineDao,
    private val runner: Provider<RoutineRunner>,
    private val scheduler: AxScheduler
) {
    suspend fun create(spec: ToolCallSpec): ToolExecution {
        val name = spec.arg("name")?.trim() ?: return ToolExecution.fail("What should the routine be called?")
        if (name.length > 60) return ToolExecution.fail("Keep the routine name under 60 characters")
        val rawSteps = spec.args["steps"]
        if (rawSteps.isNullOrBlank()) return ToolExecution.fail("A routine needs at least one step")
        val steps = runner.get().parseSteps(rawSteps)
            ?: return ToolExecution.fail("Those steps do not parse. Each step needs a tool name from the catalog.")
        if (steps.isEmpty() || steps.size > 12) {
            return ToolExecution.fail("Keep routines between 1 and 12 steps")
        }
        for (step in steps) {
            ToolCatalog.metas[step.name]
                ?: return ToolExecution.fail("Unknown tool in steps: " + step.name)
        }
        val normalized = runner.get().stepsToJson(steps)
        val id = dao.upsert(RoutineEntity(name = name, stepsJson = normalized))
        return ToolExecution.done("Routine " + name + " saved with " + steps.size + " steps (id " + id + ")")
    }

    suspend fun run(spec: ToolCallSpec, background: Boolean): ToolExecution {
        val name = spec.arg("name") ?: return ToolExecution.fail("Which routine should I run?")
        val routine = findByName(name) ?: return ToolExecution.fail("No routine named " + name)
        val outcomes = runner.get().runNow(routine.id, background)
        val done = outcomes.count { it.ok }
        val lines = StringBuilder()
        lines.appendLine(routine.name + ": " + done + "/" + outcomes.size + " steps done")
        for (outcome in outcomes) {
            lines.appendLine((if (outcome.ok) "[ok] " else "[failed] ") + outcome.tool + " - " + outcome.message)
        }
        return ToolExecution(done == outcomes.size, lines.toString().trim())
    }

    suspend fun list(): ToolExecution {
        val snapshot = dao.observeAll().firstOrNull() ?: emptyList()
        if (snapshot.isEmpty()) return ToolExecution.done("No routines saved yet")
        val lines = StringBuilder()
        for (routine in snapshot) {
            val steps = runner.get().parseSteps(routine.stepsJson)?.size ?: 0
            val schedule = if (routine.scheduleHour >= 0) {
                " daily " + routine.scheduleHour.toString().padStart(2, '0') + ":" + routine.scheduleMinute.toString().padStart(2, '0')
            } else ""
            lines.appendLine(routine.name + " - " + steps + " steps" + schedule)
        }
        return ToolExecution.done(lines.toString().trim())
    }

    suspend fun findByName(name: String): RoutineEntity? {
        val query = name.trim().lowercase()
        dao.observeAll().firstOrNull()?.forEach { routine ->
            if (routine.name.trim().lowercase() == query) return routine
        }
        return null
    }
}
