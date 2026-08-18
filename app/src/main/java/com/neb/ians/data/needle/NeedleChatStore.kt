package com.neb.ians.data.needle

import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.serialization.Serializable
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

@Serializable
data class LocalNeedleToolCall(
    val name: String,
    val argumentsJson: String
) {
    fun argument(name: String): String? = runCatching {
        Json.parseToJsonElement(argumentsJson).jsonObject[name]?.jsonPrimitive?.contentOrNull
    }.getOrNull()
}

@Serializable
data class LocalNeedleMessage(
    val id: String,
    val isUser: Boolean,
    val text: String,
    val reasoning: String? = null,
    val confidence: Double? = null,
    val durationMs: Double? = null,
    val toolCalls: List<LocalNeedleToolCall> = emptyList(),
    val createdAt: Long = System.currentTimeMillis()
)

@Singleton
class NeedleChatStore @Inject constructor(
    @ApplicationContext context: Context
) {
    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true }
    private val file = File(context.noBackupFilesDir, "needle2/chat-history.json")
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val writeMutex = Mutex()
    private val _messages = MutableStateFlow(load())
    val messages: StateFlow<List<LocalNeedleMessage>> = _messages.asStateFlow()

    fun add(message: LocalNeedleMessage) {
        _messages.update { (it + message).takeLast(100) }
        persist()
    }

    fun remove(messageId: String) {
        _messages.update { messages -> messages.filterNot { it.id == messageId } }
        persist()
    }

    fun clear() {
        _messages.value = emptyList()
        persist()
    }

    private fun load(): List<LocalNeedleMessage> {
        if (!file.exists()) return emptyList()
        return runCatching {
            json.decodeFromString(ListSerializer(LocalNeedleMessage.serializer()), file.readText())
        }.getOrDefault(emptyList())
    }

    private fun persist() {
        scope.launch {
            writeMutex.withLock {
                val snapshot = _messages.value
                file.parentFile?.mkdirs()
                val temporary = File(file.parentFile, "${file.name}.tmp")
                temporary.writeText(json.encodeToString(ListSerializer(LocalNeedleMessage.serializer()), snapshot))
                if (file.exists()) file.delete()
                if (!temporary.renameTo(file)) {
                    temporary.copyTo(file, overwrite = true)
                    temporary.delete()
                }
            }
        }
    }
}
