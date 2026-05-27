package com.neb.ians.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "replies",
    foreignKeys = [
        ForeignKey(
            entity = ForumPost::class,
            parentColumns = ["id"],
            childColumns = ["postId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("postId")]
)
data class Reply(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val postId: Long,
    val body: String,
    val author: String,
    val thumbCount: Int = 0,
    val createdAt: Long = System.currentTimeMillis()
)
