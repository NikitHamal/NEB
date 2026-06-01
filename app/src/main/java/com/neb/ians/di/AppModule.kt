package com.neb.ians.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import androidx.room.Room
import com.neb.ians.data.api.ApiService
import com.neb.ians.data.local.dao.AnnotationDao
import com.neb.ians.data.local.dao.BookmarkDao
import com.neb.ians.data.local.database.NEBiansDatabase
import com.neb.ians.data.repository.AuthRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
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
    fun provideApiService(authRepository: AuthRepository): ApiService {
        return ApiService.create(tokenProvider = { authRepository.getTokenSync() })
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
    fun provideAnnotationDao(db: NEBiansDatabase): AnnotationDao = db.annotationDao()

    @Provides
    fun provideBookmarkDao(db: NEBiansDatabase): BookmarkDao = db.bookmarkDao()
}