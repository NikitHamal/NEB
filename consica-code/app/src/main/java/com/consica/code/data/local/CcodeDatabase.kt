package com.consica.code.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.consica.code.data.local.dao.BadgeDao
import com.consica.code.data.local.dao.CodeAttemptDao
import com.consica.code.data.local.dao.EcosystemDao
import com.consica.code.data.local.dao.ProgressDao
import com.consica.code.data.local.dao.StreakDao
import com.consica.code.data.local.dao.WorkspaceDao
import com.consica.code.data.local.entity.CodeAttemptEntity
import com.consica.code.data.local.entity.EarnedBadgeEntity
import com.consica.code.data.local.entity.EcosystemItemEntity
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.local.entity.StreakDayEntity
import com.consica.code.data.local.entity.WorkspaceEntity
import com.consica.code.data.local.entity.WorkspaceFileEntity

@Database(
    entities = [
        LessonProgressEntity::class,
        EarnedBadgeEntity::class,
        EcosystemItemEntity::class,
        StreakDayEntity::class,
        WorkspaceEntity::class,
        WorkspaceFileEntity::class,
        CodeAttemptEntity::class,
    ],
    version = 1,
    exportSchema = false,
)
abstract class CcodeDatabase : RoomDatabase() {
    abstract fun progressDao(): ProgressDao
    abstract fun badgeDao(): BadgeDao
    abstract fun ecosystemDao(): EcosystemDao
    abstract fun streakDao(): StreakDao
    abstract fun workspaceDao(): WorkspaceDao
    abstract fun codeAttemptDao(): CodeAttemptDao
}
