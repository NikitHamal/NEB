package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "resources")
data class ResourceEntity(
    @PrimaryKey val id: String,
    val title: String,
    val description: String,
    val subject: String,
    val gradeLevel: String,
    val type: String,  // Textbook, Notes, Past Papers, Guide, Solution
    val fileUrl: String,
    val thumbnailUrl: String = "",
    val fileSize: Long = 0,
    val localPath: String? = null,
    val isDownloaded: Boolean = false,
    val downloadProgress: Int = 0,
    val author: String = "",
    val addedAt: Long = System.currentTimeMillis(),
    val lastAccessedAt: Long = 0,
    val viewCount: Int = 0
)
