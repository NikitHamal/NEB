package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "annotations")
data class AnnotationEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val resourceId: String,
    val page: Int,
    val type: String,  // HIGHLIGHT, UNDERLINE, STICKY_NOTE
    val content: String,  // For sticky note text
    val startX: Float,
    val startY: Float,
    val endX: Float,
    val endY: Float,
    val color: Int,
    val createdAt: Long,
    val text: String  // The highlighted/underlined text
)
