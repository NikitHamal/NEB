package com.agentx.app.data.tools

import com.agentx.app.data.engine.ToolCallSpec
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.ActivityEntity
import javax.inject.Inject
import javax.inject.Provider
import javax.inject.Singleton
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
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
        val element = runCatching { json.parseToJsonElement(raw) }.getOrNull() ?: return null
        val array = when (element) {
            is JsonArray -> element
            is JsonObject -> JsonArray(listOf(element))
            is JsonPrimitive -> {
                if (!element.isString) return null
                val inner = runCatching { json.parseToJsonElement(element.content) }.getOrNull()
                    ?: return null
                when (inner) {
                    is JsonArray -> inner
                    is JsonObject -> JsonArray(listOf(inner))
                    else -> return null
                }
            }
        }
        if (array.isEmpty()) return null
        val steps = ArrayList<ToolCallSpec>()
        for (item in array) {
            val obj = item as? JsonObject ?: continue
            val tool = (obj["tool"] as? JsonPrimitive)?.contentOrNull?.trim().orEmpty()
            if (tool.isEmpty()) continue
            val argsObj = obj["args"] as? JsonObject
            val args = argsObj?.entries?.associate { (key, value) ->
                key to when (value) {
                    is JsonPrimitive -> if (value.isString) value.content else value.toString()
                    else -> value.toString()
                }
            } ?: emptyMap()
            steps.add(ToolCallSpec(tool, args))
        }
        return steps.ifEmpty { null }
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
