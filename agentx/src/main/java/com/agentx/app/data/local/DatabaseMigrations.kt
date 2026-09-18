package com.agentx.app.data.local

import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS `conversations` (" +
                "`id` TEXT NOT NULL, `title` TEXT NOT NULL, " +
                "`lastPreview` TEXT NOT NULL, `messageCount` INTEGER NOT NULL, " +
                "`createdAt` INTEGER NOT NULL, `updatedAt` INTEGER NOT NULL, " +
                "PRIMARY KEY(`id`))"
        )
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS `chat_messages` (" +
                "`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " +
                "`conversationId` TEXT NOT NULL, `isUser` INTEGER NOT NULL, " +
                "`text` TEXT NOT NULL, `reasoning` TEXT, `confidence` REAL, " +
                "`durationMs` REAL, `toolCallsJson` TEXT NOT NULL, " +
                "`optionsJson` TEXT NOT NULL, `createdAt` INTEGER NOT NULL)"
        )
        db.execSQL(
            "CREATE INDEX IF NOT EXISTS `index_chat_messages_conversationId` " +
                "ON `chat_messages` (`conversationId`)"
        )
    }
}
