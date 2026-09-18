package com.agentx.app.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.agentx.app.data.local.entity.ChatMessageEntity
import com.agentx.app.data.local.entity.ConversationEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ChatDao {
    @Query("SELECT * FROM conversations ORDER BY updatedAt DESC")
    fun observeConversations(): Flow<List<ConversationEntity>>

    @Query("SELECT * FROM conversations WHERE id = :id")
    suspend fun conversation(id: String): ConversationEntity?

    @Query("SELECT COUNT(*) FROM conversations")
    suspend fun conversationCount(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertConversation(conversation: ConversationEntity)

    @Update
    suspend fun updateConversation(conversation: ConversationEntity)

    @Query("DELETE FROM conversations WHERE id = :id")
    suspend fun deleteConversation(id: String)

    @Query("SELECT * FROM chat_messages WHERE conversationId = :conversationId ORDER BY id ASC")
    fun observeMessages(conversationId: String): Flow<List<ChatMessageEntity>>

    @Insert
    suspend fun insertMessage(message: ChatMessageEntity): Long

    @Query("DELETE FROM chat_messages WHERE conversationId = :conversationId")
    suspend fun clearMessages(conversationId: String)

    @Query("DELETE FROM chat_messages WHERE conversationId = :conversationId")
    suspend fun deleteMessagesOf(conversationId: String)

    @Query("DELETE FROM conversations")
    suspend fun deleteAllConversations()

    @Query("DELETE FROM chat_messages")
    suspend fun deleteAllMessages()
}
