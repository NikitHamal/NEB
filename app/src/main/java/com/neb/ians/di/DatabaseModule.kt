package com.neb.ians.di

import android.content.Context
import androidx.room.Room
import com.neb.ians.data.local.dao.*
import com.neb.ians.data.local.database.NEBiansDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

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
    fun provideResourceDao(db: NEBiansDatabase): ResourceDao = db.resourceDao()

    @Provides
    fun provideAnnotationDao(db: NEBiansDatabase): AnnotationDao = db.annotationDao()

    @Provides
    fun provideForumDao(db: NEBiansDatabase): ForumDao = db.forumDao()

    @Provides
    fun provideBookmarkDao(db: NEBiansDatabase): BookmarkDao = db.bookmarkDao()
}
