package com.neb.ians.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.neb.ians.data.model.ContentItem
import com.neb.ians.data.model.ForumPost
import com.neb.ians.data.model.PdfAnnotation
import com.neb.ians.data.model.Reply

@Database(
    entities = [ContentItem::class, PdfAnnotation::class, ForumPost::class, Reply::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun contentDao(): ContentDao
    abstract fun annotationDao(): AnnotationDao
    abstract fun forumDao(): ForumDao
}
