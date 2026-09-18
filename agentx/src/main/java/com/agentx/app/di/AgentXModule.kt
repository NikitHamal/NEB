package com.agentx.app.di

import android.content.Context
import androidx.room.Room
import com.agentx.app.data.local.AxDatabase
import com.agentx.app.data.local.MIGRATION_1_2
import com.agentx.app.data.local.dao.ActivityDao
import com.agentx.app.data.local.dao.ChatDao
import com.agentx.app.data.local.dao.NoteDao
import com.agentx.app.data.local.dao.ReminderDao
import com.agentx.app.data.local.dao.RoutineDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AgentXModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AxDatabase =
        Room.databaseBuilder(context, AxDatabase::class.java, "agentx_database")
            .addMigrations(MIGRATION_1_2)
            .fallbackToDestructiveMigration()
            .build()

    @Provides
    fun provideReminderDao(db: AxDatabase): ReminderDao = db.reminderDao()

    @Provides
    fun provideRoutineDao(db: AxDatabase): RoutineDao = db.routineDao()

    @Provides
    fun provideActivityDao(db: AxDatabase): ActivityDao = db.activityDao()

    @Provides
    fun provideNoteDao(db: AxDatabase): NoteDao = db.noteDao()

    @Provides
    fun provideChatDao(db: AxDatabase): ChatDao = db.chatDao()
}
