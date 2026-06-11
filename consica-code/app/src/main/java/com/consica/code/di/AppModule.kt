package com.consica.code.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import androidx.room.Room
import com.consica.code.data.local.CcodeDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "ccode_prefs")

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDataStore(@ApplicationContext context: Context): DataStore<Preferences> =
        context.dataStore

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): CcodeDatabase =
        Room.databaseBuilder(context, CcodeDatabase::class.java, "ccode.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides fun provideProgressDao(db: CcodeDatabase) = db.progressDao()
    @Provides fun provideBadgeDao(db: CcodeDatabase) = db.badgeDao()
    @Provides fun provideEcosystemDao(db: CcodeDatabase) = db.ecosystemDao()
    @Provides fun provideStreakDao(db: CcodeDatabase) = db.streakDao()
    @Provides fun provideWorkspaceDao(db: CcodeDatabase) = db.workspaceDao()
    @Provides fun provideCodeAttemptDao(db: CcodeDatabase) = db.codeAttemptDao()
}
