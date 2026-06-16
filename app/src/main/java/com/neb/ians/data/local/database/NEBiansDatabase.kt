package com.neb.ians.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.entity.BookmarkEntity

@Database(
    entities = [
        BookmarkEntity::class
    ],
    version = 1,
    exportSchema = true
)
abstract class NEBiansDatabase : RoomDatabase() {
    abstract fun bookmarkDao(): BookmarkDao
}