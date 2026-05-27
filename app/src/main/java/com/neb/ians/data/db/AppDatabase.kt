package com.neb.ians.data.db

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverter
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import android.content.Context

@Database(
    entities = [ResourceEntity::class, ForumThreadEntity::class, ForumReplyEntity::class, PdfAnnotationEntity::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun resourceDao(): ResourceDao
    abstract fun forumThreadDao(): ForumThreadDao
    abstract fun forumReplyDao(): ForumReplyDao
    abstract fun pdfAnnotationDao(): PdfAnnotationDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "nebians_database"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}

class Converters {
    @TypeConverter
    fun fromList(value: List<String>?): String? = value?.joinToString(",")

    @TypeConverter
    fun toList(value: String?): List<String> = value?.split(",") ?: emptyList()
}
