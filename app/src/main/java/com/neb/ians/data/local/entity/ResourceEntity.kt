package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "resources")
data class ResourceEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val description: String,
    val subject: String,
    val grade: String,
    val type: String,
    val fileUrl: String,
    val localPath: String? = null,
    val thumbnailUrl: String? = null,
    val fileSize: Long = 0,
    val author: String = "",
    val addedAt: Long = System.currentTimeMillis(),
    val isCached: Boolean = false,
    val downloadProgress: Int = 0,
)
