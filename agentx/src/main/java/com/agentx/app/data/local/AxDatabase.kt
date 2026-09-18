package com.agentx.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.dao.NoteDao
import com.agentx.app.data.local.dao.ReminderDao
import com.agentx.app.data.local.dao.RoutineDao
import com.agentx.app.data.local.entity.ActivityEntity
import com.agentx.app.data.local.entity.NoteEmbeddingEntity
import com.agentx.app.data.local.entity.NoteEntity
import com.agentx.app.data.local.entity.ReminderEntity
import com.agentx.app.data.local.entity.RoutineEntity

@Database(
    entities = [
        ReminderEntity::class,
        RoutineEntity::class,
        ActivityEntity::class,
        NoteEntity::class,
        NoteEmbeddingEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AxDatabase : RoomDatabase() {
    abstract fun reminderDao(): ReminderDao
    abstract fun routineDao(): RoutineDao
    abstract fun activityDao(): ActivityDao
    abstract fun noteDao(): NoteDao
}
