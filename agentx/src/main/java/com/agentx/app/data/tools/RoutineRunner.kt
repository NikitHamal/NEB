package com.agentx.app.data.tools

import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.ActivityEntity
import javax.inject.Inject
import javax.inject.Provider
import javax.inject.Singleton
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

data class StepOutcome(val tool: String, val ok: Boolean, val message: String)

@Singleton
class RoutineRunner @Inject constructor(
    private val executor: Provider<ToolExecutor>,
    private val routineDao: RoutineDao,
    private val activityDao: ActivityDao
) {
    private val json = Json { ignoreUnknownKeys = true; isLenient = true }

    fun parseSteps(raw: String): List<ToolCallSpec>? {
        return runCatching {
            val array = json.parseToJsonElement(raw).jsonArray
            array.map { element ->
                val obj = element.jsonObject
                val tool = obj["tool"]?.jsonPrimitive?.contentOrNull?.trim().orEmpty()
                if (tool.isEmpty()) throw IllegalArgumentException("A step is missing its tool name")
                val argsObj = obj["args"]?.jsonObject
                val args = argsObj?.entries?.associate { (key, value) ->
                    key to (value.jsonPrimitive.contentOrNull ?: value.toString())
                } ?: emptyMap()
                ToolCallSpec(tool, args)
            }
        }.getOrNull()
    }

    fun stepsToJson(steps: List<ToolCallSpec>): String {
        val array = buildJsonArray {
            for (step in steps) {
                add(buildJsonObject {
                    put("tool", step.name)
                    put("args", buildJsonObject {
                        for ((key, value) in step.args) put(key, value)
                    })
                })
            }
        }
        return array.toString()
    }

    suspend fun runNow(id: Long, background: Boolean): List<StepOutcome> {
        val routine = routineDao.getById(id) ?: return listOf(StepOutcome("", false, "Routine not found"))
        val steps = parseSteps(routine.stepsJson) ?: return listOf(StepOutcome("", false, "Routine steps are corrupted"))
        val outcomes = ArrayList<StepOutcome>(steps.size)
        for (step in steps) {
            val meta = ToolCatalog.metas[step.name]
            if (meta == null) {
                outcomes.add(StepOutcome(step.name, false, "Unknown tool " + step.name))
                continue
            }
            val result = executor.get().execute(step, background)
            outcomes.add(StepOutcome(step.name, result.ok, result.message))
        }
        routineDao.markRun(id, System.currentTimeMillis())
        val done = outcomes.count { it.ok }
        activityDao.insert(
            ActivityEntity(
                kind = "routine",
                label = "Ran " + routine.name + " (" + done + "/" + outcomes.size + " steps)",
                detailJson = routine.stepsJson,
                status = if (done == outcomes.size) "done" else "failed"
            )
        )
        activityDao.trim()
        return outcomes
    }
}
