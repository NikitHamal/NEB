package com.neb.ians.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "content_items")
data class ContentItem(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val title: String,
    val description: String,
    val subject: String,      // Physics, Chemistry, Mathematics...
    val grade: String,        // Grade 11, Grade 12
    val type: String,         // Textbook, Notes, Past Papers, Solutions
    val fileUrl: String,      // Local or remote URI
    val thumbnailUrl: String? = null,
    val isDownloaded: Boolean = false,
    val localPath: String? = null,
    val addedAt: Long = System.currentTimeMillis()
)
