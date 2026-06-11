package com.consica.code.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.consica.code.data.local.dao.BadgeDao
import com.consica.code.data.local.dao.ProgressDao
import com.consica.code.data.local.dao.RunHistoryDao
import com.consica.code.data.local.dao.WorkspaceDao
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.RunHistoryEntity
import com.consica.code.data.local.entity.WorkspaceEntity

@Database(
    entities = [
        LessonProgressEntity::class,
        WorkspaceEntity::class,
        EarnedBadgeEntity::class,
        RunHistoryEntity::class,
    ],
    version = 1,
    exportSchema = false,
)
abstract class CcodeDatabase : RoomDatabase() {
    abstract fun progressDao(): ProgressDao
    abstract fun workspaceDao(): WorkspaceDao
    abstract fun badgeDao(): BadgeDao
    abstract fun runHistoryDao(): RunHistoryDao

    companion object {
        @Volatile
        private var instance: CcodeDatabase? = null

        fun get(context: Context): CcodeDatabase =
            instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    CcodeDatabase::class.java,
                    "ccode.db",
                )
                    .fallbackToDestructiveMigration()
                    .build()
                    .also { instance = it }
            }
    }
}
