package com.neb.ians.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "bookmarks")
data class BookmarkEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val resourceId: String,
    val page: Int,
    val title: String,
    val createdAt: Long
)
