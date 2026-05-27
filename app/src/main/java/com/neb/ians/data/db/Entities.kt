package com.neb.ians.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "resources")
data class ResourceEntity(
    @PrimaryKey val id: String,
    val title: String,
    val subject: String,
    val grade: String,
    val type: String,
    val remoteUrl: String,
    val localPath: String? = null,
    val fileSizeBytes: Long = 0L,
    val isDownloaded: Boolean = false
)

@Entity(tableName = "forum_threads")
data class ForumThreadEntity(
    @PrimaryKey val id: String,
    val title: String,
    val body: String,
    val authorName: String = "Student",
    val likes: Int = 0,
    val repliesCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "forum_replies")
data class ForumReplyEntity(
    @PrimaryKey val id: String,
    val threadId: String,
    val body: String,
    val authorName: String = "Student",
    val likes: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "pdf_annotations")
data class PdfAnnotationEntity(
    @PrimaryKey val id: String,
    val pdfPath: String,
    val pageIndex: Int,
    val type: String,
    val x: Float,
    val y: Float,
    val width: Float,
    val height: Float,
    val noteText: String? = null,
    val color: Int = 0xFFFFEB3B.toInt(),
    val createdAt: Long = System.currentTimeMillis()
)
