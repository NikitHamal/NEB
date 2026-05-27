package com.neb.ians.data.db

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(tableName = "resources")
data class ResourceEntity(
    @PrimaryKey val id: String,
    val title: String,
    val author: String?,
    val description: String,
    val subject: String,
    val grade: String,
    val type: String,
    val sourceUrl: String,
    val localPath: String?,
    val sizeBytes: Long,
    val pageCount: Int,
    val isFavorite: Boolean = false,
    val downloadedAt: Long? = null,
    val updatedAt: Long = System.currentTimeMillis(),
)

@Entity(
    tableName = "annotations",
    indices = [Index("resourceId")],
)
data class AnnotationEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val resourceId: String,
    val page: Int,
    val kind: String,           // HIGHLIGHT | UNDERLINE | NOTE
    val text: String?,           // selected text or note body
    val rectsJson: String?,      // serialized list of rects (x,y,w,h normalized 0..1)
    val color: Int,              // ARGB
    val createdAt: Long = System.currentTimeMillis(),
)

@Entity(tableName = "threads")
data class ThreadEntity(
    @PrimaryKey val id: String,
    val title: String,
    val body: String,
    val author: String,
    val subject: String?,
    val grade: String?,
    val createdAt: Long = System.currentTimeMillis(),
    val replyCount: Int = 0,
    val thumbCount: Int = 0,
    val thumbed: Boolean = false,
)

@Entity(
    tableName = "posts",
    indices = [Index("threadId")],
)
data class PostEntity(
    @PrimaryKey val id: String,
    val threadId: String,
    val parentId: String?,
    val body: String,
    val author: String,
    val createdAt: Long = System.currentTimeMillis(),
    val thumbCount: Int = 0,
    val thumbed: Boolean = false,
)
