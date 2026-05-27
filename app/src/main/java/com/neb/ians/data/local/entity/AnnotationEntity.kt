package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "annotations")
data class AnnotationEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val resourceId: Long,
    val page: Int,
    val type: String,
    val content: String = "",
    val startX: Float = 0f,
    val startY: Float = 0f,
    val endX: Float = 0f,
    val endY: Float = 0f,
    val color: Long = 0xFFFFEB3B,
    val createdAt: Long = System.currentTimeMillis(),
)
