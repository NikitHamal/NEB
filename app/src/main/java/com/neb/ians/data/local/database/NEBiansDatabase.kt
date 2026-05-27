package com.neb.ians.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.neb.ians.data.local.dao.AnnotationDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.local.entity.AnnotationEntity
import com.neb.ians.data.local.entity.BookmarkEntity
import com.neb.ians.data.local.entity.ForumPostEntity
import com.neb.ians.data.local.entity.ForumReplyEntity
import com.neb.ians.data.local.entity.ResourceEntity

@Database(
    entities = [
        ResourceEntity::class,
        AnnotationEntity::class,
        ForumPostEntity::class,
        ForumReplyEntity::class,
        BookmarkEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class NEBiansDatabase : RoomDatabase() {
    abstract fun resourceDao(): ResourceDao
    abstract fun annotationDao(): AnnotationDao
    abstract fun forumDao(): ForumDao
    abstract fun bookmarkDao(): BookmarkDao
}
