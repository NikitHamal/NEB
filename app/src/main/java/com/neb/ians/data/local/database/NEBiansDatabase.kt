package com.neb.ians.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.neb.ians.data.local.dao.ApiCacheDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.dao.NoteDao
import com.neb.ians.data.local.entity.ApiCacheEntity
import com.neb.ians.data.local.entity.BookmarkEntity
import com.neb.ians.data.local.entity.NoteEntity

@Database(
    entities = [
        BookmarkEntity::class,
        ApiCacheEntity::class,
        NoteEntity::class
    ],
    version = 3,
    exportSchema = true
)
abstract class NEBiansDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
    abstract fun bookmarkDao(): BookmarkDao
    abstract fun apiCacheDao(): ApiCacheDao
}
