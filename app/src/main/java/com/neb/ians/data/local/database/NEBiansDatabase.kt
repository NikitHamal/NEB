package com.neb.ians.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.neb.ians.data.local.dao.AnnotationDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.entity.AnnotationEntity
import com.neb.ians.data.local.entity.BookmarkEntity

@Database(
    entities = [
        AnnotationEntity::class,
        BookmarkEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class NEBiansDatabase : RoomDatabase() {
    abstract fun annotationDao(): AnnotationDao
    abstract fun bookmarkDao(): BookmarkDao
}