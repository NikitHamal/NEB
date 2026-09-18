package com.agentx.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "reminders")
data class ReminderEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val note: String = "",
    val triggerAt: Long,
    val createdAt: Long = System.currentTimeMillis(),
    val fired: Boolean = false,
    val requestCode: Int = 0
)
