package com.neb.ians.data.db

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [
        ResourceEntity::class,
        AnnotationEntity::class,
        ThreadEntity::class,
        PostEntity::class,
    ],
    version = 1,
    exportSchema = false,
)
abstract class NebDatabase : RoomDatabase() {
    abstract fun resourceDao(): ResourceDao
    abstract fun annotationDao(): AnnotationDao
    abstract fun forumDao(): ForumDao
}
