package com.agentx.app.data.chat

import android.content.Context
import com.agentx.app.data.local.dao.ChatDao
import com.agentx.app.data.local.entity.ChatMessageEntity
import com.agentx.app.data.local.entity.ConversationEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.serialization.Serializable
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.builtins.serializer
import kotlinx.serialization.json.Json

@Serializable
data class AxToolCallRecord(
    val name: String,
    val argumentsJson: String
)

data class UiChatMessage(
    val id: Long,
    val isUser: Boolean,
    val text: String,
    val reasoning: String? = null,
    val confidence: Double? = null,
    val durationMs: Double? = null,
    val toolCalls: List<AxToolCallRecord> = emptyList(),
    val options: List<String> = emptyList()
)

@Serializable
private data class LegacyAxMessage(
    val id: String = "",
    val isUser: Boolean = false,
    val text: String = "",
    val reasoning: String? = null,
    val confidence: Double? = null,
    val durationMs: Double? = null,
    val toolCalls: List<AxToolCallRecord> = emptyList(),
    val options: List<String> = emptyList()
)

@Singleton
class ChatRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val chatDao: ChatDao
) {
    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true }
    private val toolCallListSerializer = ListSerializer(AxToolCallRecord.serializer())
    private val stringListSerializer = ListSerializer(String.serializer())

    fun observeConversations(): Flow<List<ConversationEntity>> = chatDao.observeConversations()

    fun observeMessages(conversationId: String): Flow<List<UiChatMessage>> =
        chatDao.observeMessages(conversationId).map { rows -> rows.map { it.toUi() } }

    suspend fun conversation(id: String): ConversationEntity? = chatDao.conversation(id)

    suspend fun createConversation(title: String = "New chat"): String {
        val id = UUID.randomUUID().toString()
        val now = System.currentTimeMillis()
        chatDao.upsertConversation(ConversationEntity(id = id, title = title, createdAt = now, updatedAt = now))
        return id
    }

    suspend fun renameConversation(id: String, title: String) {
        val current = chatDao.conversation(id) ?: return
        chatDao.updateConversation(current.copy(title = title.take(80), updatedAt = System.currentTimeMillis()))
    }

    suspend fun deleteConversation(id: String) {
        chatDao.deleteMessagesOf(id)
        chatDao.deleteConversation(id)
    }

    suspend fun clearConversation(id: String) {
        val current = chatDao.conversation(id) ?: return
        chatDao.clearMessages(id)
        chatDao.updateConversation(
            current.copy(lastPreview = "", messageCount = 0, updatedAt = System.currentTimeMillis())
        )
    }

    suspend fun clearAll() {
        chatDao.deleteAllMessages()
        chatDao.deleteAllConversations()
    }

    suspend fun addUserMessage(conversationId: String, text: String): Long {
        val id = chatDao.insertMessage(
            ChatMessageEntity(conversationId = conversationId, isUser = true, text = text)
        )
        touch(conversationId, text, increment = 1)
        return id
    }

    suspend fun addAssistantMessage(
        conversationId: String,
        text: String,
        reasoning: String? = null,
        confidence: Double? = null,
        durationMs: Double? = null,
        toolCalls: List<AxToolCallRecord> = emptyList(),
        options: List<String> = emptyList()
    ): Long {
        val id = chatDao.insertMessage(
            ChatMessageEntity(
                conversationId = conversationId,
                isUser = false,
                text = text,
                reasoning = reasoning,
                confidence = confidence,
                durationMs = durationMs,
                toolCallsJson = json.encodeToString(toolCallListSerializer, toolCalls),
                optionsJson = json.encodeToString(stringListSerializer, options)
            )
        )
        touch(conversationId, text, increment = 1)
        return id
    }

    suspend fun retitleFromFirstMessage(conversationId: String, firstText: String) {
        val current = chatDao.conversation(conversationId) ?: return
        if (current.title != "New chat") return
        val title = firstText.trim().replace(System.lineSeparator(), " ").take(42)
        if (title.isNotBlank()) {
            chatDao.updateConversation(current.copy(title = title, updatedAt = System.currentTimeMillis()))
        }
    }

    private suspend fun touch(conversationId: String, preview: String, increment: Int) {
        val current = chatDao.conversation(conversationId) ?: return
        chatDao.updateConversation(
            current.copy(
                lastPreview = preview.trim().replace(System.lineSeparator(), " ").take(90),
                messageCount = current.messageCount + increment,
                updatedAt = System.currentTimeMillis()
            )
        )
    }

    suspend fun ensureLegacyMigrated() {
        if (chatDao.conversationCount() > 0) {
            deleteLegacyFile()
            return
        }
        val file = File(context.noBackupFilesDir, "axchat/chat-history.json")
        if (!file.exists()) return
        val imported = runCatching {
            json.decodeFromString(ListSerializer(LegacyAxMessage.serializer()), file.readText())
        }.getOrNull().orEmpty().filter { it.text.isNotBlank() }.takeLast(150)
        if (imported.isEmpty()) {
            deleteLegacyFile()
            return
        }
        val id = createConversation("Imported chat")
        for (message in imported) {
            if (message.isUser) {
                addUserMessage(id, message.text)
            } else {
                addAssistantMessage(
                    id, message.text, message.reasoning, message.confidence,
                    message.durationMs, message.toolCalls, message.options
                )
            }
        }
        deleteLegacyFile()
    }

    private fun deleteLegacyFile() {
        runCatching { File(context.noBackupFilesDir, "axchat/chat-history.json").delete() }
    }

    private fun ChatMessageEntity.toUi(): UiChatMessage {
        val calls = runCatching { json.decodeFromString(toolCallListSerializer, toolCallsJson) }.getOrDefault(emptyList())
        val opts = runCatching { json.decodeFromString(stringListSerializer, optionsJson) }.getOrDefault(emptyList())
        return UiChatMessage(
            id = id, isUser = isUser, text = text, reasoning = reasoning,
            confidence = confidence, durationMs = durationMs, toolCalls = calls, options = opts
        )
    }
}
