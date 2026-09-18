package com.agentx.app.data.engine

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonPrimitive

@Serializable
data class EngineToolCall(
    val name: String = "",
    val arguments: Map<String, JsonElement> = emptyMap()
) {
    fun stringArgs(): Map<String, String> = arguments.mapValues { (_, value) ->
        runCatching { value.jsonPrimitive.contentOrNull ?: value.toString() }.getOrDefault(value.toString())
    }
}

@Serializable
data class EngineResult(
    val type: String = "",
    val success: Boolean = true,
    val function_calls: List<EngineToolCall> = emptyList(),
    val suppressed_calls: List<EngineToolCall> = emptyList(),
    val reasoning: String? = null,
    val confidence: Double? = null
)

data class ToolCallSpec(
    val name: String,
    val args: Map<String, String>
) {
    fun arg(key: String): String? = args[key]?.takeIf { it.isNotBlank() }
    fun argInt(key: String): Int? = arg(key)?.toIntOrNull()
    fun argLong(key: String): Long? = arg(key)?.toLongOrNull()
    fun argBool(key: String): Boolean? = arg(key)?.lowercase()?.let {
        when (it) {
            "true", "1", "yes", "on" -> true
            "false", "0", "no", "off" -> false
            else -> null
        }
    }
}

fun EngineToolCall.toSpec() = ToolCallSpec(name = name, args = stringArgs())

val EngineJson = Json { ignoreUnknownKeys = true; isLenient = true }

fun parseEngineResult(raw: String): EngineResult? =
    runCatching { EngineJson.decodeFromString(EngineResult.serializer(), raw) }.getOrNull()
