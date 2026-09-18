package com.agentx.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "routines")
data class RoutineEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val stepsJson: String,
    val scheduleHour: Int = -1,
    val scheduleMinute: Int = -1,
    val scheduleDays: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis(),
    val lastRunAt: Long = 0L
)
