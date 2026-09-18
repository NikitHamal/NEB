package com.agentx.app.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.agentx.app.data.local.entity.NoteEmbeddingEntity
import com.agentx.app.data.local.entity.NoteEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface NoteDao {
    @Query("SELECT * FROM notes ORDER BY updatedAt DESC")
    fun observeAll(): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes ORDER BY updatedAt DESC LIMIT :limit")
    suspend fun recent(limit: Int): List<NoteEntity>

    @Query("SELECT * FROM notes WHERE title LIKE '%' || :q || '%' OR body LIKE '%' || :q || '%' ORDER BY updatedAt DESC LIMIT 20")
    suspend fun keywordSearch(q: String): List<NoteEntity>

    @Query("SELECT * FROM notes WHERE id = :id")
    suspend fun getById(id: Long): NoteEntity?

    @Insert
    suspend fun insert(note: NoteEntity): Long

    @Update
    suspend fun update(note: NoteEntity)

    @Query("DELETE FROM notes WHERE id = :id")
    suspend fun delete(id: Long)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertEmbedding(embedding: NoteEmbeddingEntity)

    @Query("SELECT * FROM note_embeddings WHERE noteId = :noteId")
    suspend fun embeddingFor(noteId: Long): NoteEmbeddingEntity?

    @Query("SELECT * FROM note_embeddings")
    suspend fun allEmbeddings(): List<NoteEmbeddingEntity>

    @Query("DELETE FROM note_embeddings WHERE noteId = :noteId")
    suspend fun deleteEmbedding(noteId: Long)
}
