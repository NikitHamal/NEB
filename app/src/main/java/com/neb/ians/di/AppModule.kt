package com.neb.ians.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.room.Room
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.local.dao.ApiCacheDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.database.DatabaseMigrations
import com.neb.ians.data.local.database.NEBiansDatabase
import com.neb.ians.data.repository.SecurePrefs
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by androidx.datastore.preferences.preferencesDataStore(name = "settings")

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
        @ApplicationContext context: Context
    ): ApiService {
        return ApiService.create(context, tokenProvider = {
            SecurePrefs.getAuthToken(context)
        })
    }

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): NEBiansDatabase {
        return Room.databaseBuilder(
            context,
            NEBiansDatabase::class.java,
            "nebians_database"
        )
            .addMigrations(*DatabaseMigrations.ALL)
            .build()
    }

    @Provides
    fun provideBookmarkDao(db: NEBiansDatabase): BookmarkDao = db.bookmarkDao()

    @Provides
    fun provideApiCacheDao(db: NEBiansDatabase): ApiCacheDao = db.apiCacheDao()
}