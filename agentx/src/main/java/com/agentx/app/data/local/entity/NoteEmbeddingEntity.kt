package com.agentx.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "note_embeddings")
data class NoteEmbeddingEntity(
    @PrimaryKey val noteId: Long,
    val dim: Int,
    val vector: ByteArray,
    val textHash: String,
    val updatedAt: Long = System.currentTimeMillis()
)
