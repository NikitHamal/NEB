package com.neb.ians.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import androidx.room.Room
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.database.NEBiansDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDataStore(@ApplicationContext context: Context): DataStore<Preferences> {
        return context.dataStore
    }

    @Provides
    @Singleton
    fun provideApiService(
        @ApplicationContext context: Context,
        dataStore: DataStore<Preferences>
    ): ApiService {
        return ApiService.create(context, tokenProvider = {
            try {
                runBlocking(Dispatchers.IO) {
                    dataStore.data.map { it[stringPreferencesKey("auth_token")] }.first()
                }
            } catch (_: Exception) { null }
        })
    }

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): NEBiansDatabase {
        return Room.databaseBuilder(
            context,
            NEBiansDatabase::class.java,
            "nebians_database"
        ).fallbackToDestructiveMigration().build()
    }

    @Provides
    fun provideBookmarkDao(db: NEBiansDatabase): BookmarkDao = db.bookmarkDao()
}