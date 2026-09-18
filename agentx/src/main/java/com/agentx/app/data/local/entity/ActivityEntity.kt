package com.agentx.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "activity_log")
data class ActivityEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val ts: Long = System.currentTimeMillis(),
    val kind: String,
    val label: String,
    val detailJson: String = "",
    val confidence: Double? = null,
    val status: String
)
