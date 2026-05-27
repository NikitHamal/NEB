package com.neb.ians.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey
import com.neb.ians.data.model.Grade
import com.neb.ians.data.model.ResourceType
import com.neb.ians.data.model.Subject

@Entity(
    tableName = "resources",
    indices = [Index("subject"), Index("grade"), Index("type")]
)
data class ResourceEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val author: String? = null,
    val description: String? = null,
    val subject: Subject,
    val grade: Grade,
    val type: ResourceType,
    val pageCount: Int = 0,
    val sizeBytes: Long = 0,
    val sourceUri: String,
    val localPath: String? = null,
    val coverUrl: String? = null,
    val isFavorite: Boolean = false,
    val lastOpenedAt: Long = 0,
    val cachedAt: Long = 0,
)

@Entity(
    tableName = "annotations",
    indices = [Index("resourceId"), Index(value = ["resourceId", "page"])]
)
data class AnnotationEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val resourceId: Long,
    val page: Int,
    val kind: AnnotationKind,
    val xPct: Float,
    val yPct: Float,
    val widthPct: Float,
    val heightPct: Float,
    val color: Long,
    val note: String? = null,
    val createdAt: Long = System.currentTimeMillis(),
)

enum class AnnotationKind { Highlight, Underline, StickyNote }

@Entity(tableName = "forum_threads", indices = [Index("createdAt")])
data class ForumThreadEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val body: String,
    val author: String,
    val tags: String = "",
    val likes: Int = 0,
    val replyCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
)

@Entity(tableName = "forum_replies", indices = [Index("threadId"), Index("createdAt")])
data class ForumReplyEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val threadId: Long,
    val body: String,
    val author: String,
    val likes: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
)
