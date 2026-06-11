package com.consica.code.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [
        LessonProgressEntity::class,
        BadgeEntity::class,
        WorkspaceEntity::class,
        CodeAttemptEntity::class,
        EcosystemItemEntity::class,
    ],
    version = 1,
    exportSchema = false,
)
abstract class ConsicaDatabase : RoomDatabase() {
    abstract fun lessonProgressDao(): LessonProgressDao
    abstract fun badgeDao(): BadgeDao
    abstract fun workspaceDao(): WorkspaceDao
    abstract fun codeAttemptDao(): CodeAttemptDao
    abstract fun ecosystemDao(): EcosystemDao

    companion object {
        @Volatile private var INSTANCE: ConsicaDatabase? = null

        fun get(context: Context): ConsicaDatabase = INSTANCE ?: synchronized(this) {
            INSTANCE ?: Room.databaseBuilder(
                context.applicationContext,
                ConsicaDatabase::class.java,
                "consica-code.db",
            ).fallbackToDestructiveMigration().build().also { INSTANCE = it }
        }
    }
}
