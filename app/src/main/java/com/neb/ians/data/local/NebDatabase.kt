package com.neb.ians.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters

@Database(
    entities = [
        ResourceEntity::class,
        AnnotationEntity::class,
        ForumThreadEntity::class,
        ForumReplyEntity::class,
    ],
    version = 1,
    exportSchema = false,
)
@TypeConverters(NebConverters::class)
abstract class NebDatabase : RoomDatabase() {
    abstract fun resourceDao(): ResourceDao
    abstract fun annotationDao(): AnnotationDao
    abstract fun forumDao(): ForumDao
}
