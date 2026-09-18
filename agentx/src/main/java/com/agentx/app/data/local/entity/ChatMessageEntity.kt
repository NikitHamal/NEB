package com.agentx.app.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "chat_messages",
    indices = [Index("conversationId")]
)
data class ChatMessageEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val conversationId: String,
    val isUser: Boolean,
    val text: String,
    val reasoning: String? = null,
    val confidence: Double? = null,
    val durationMs: Double? = null,
    val toolCallsJson: String = "[]",
    val optionsJson: String = "[]",
    val createdAt: Long = System.currentTimeMillis()
)
