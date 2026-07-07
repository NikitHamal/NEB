package com.neb.ians.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.neb.ians.data.local.dao.ApiCacheDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.entity.ApiCacheEntity
import com.neb.ians.data.local.entity.BookmarkEntity

@Database(
    entities = [
        BookmarkEntity::class,
        ApiCacheEntity::class
    ],
    version = 2,
    exportSchema = true
)
abstract class NEBiansDatabase : RoomDatabase() {
    abstract fun bookmarkDao(): BookmarkDao
    abstract fun apiCacheDao(): ApiCacheDao
}
