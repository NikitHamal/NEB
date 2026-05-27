package com.neb.ians.di

import android.content.Context
import androidx.room.Room
import com.neb.ians.data.db.AnnotationDao
import com.neb.ians.data.db.ForumDao
import com.neb.ians.data.db.NebDatabase
import com.neb.ians.data.db.ResourceDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides @Singleton
    fun provideDatabase(@ApplicationContext ctx: Context): NebDatabase =
        Room.databaseBuilder(ctx, NebDatabase::class.java, "nebians.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides fun provideResourceDao(db: NebDatabase): ResourceDao = db.resourceDao()
    @Provides fun provideAnnotationDao(db: NebDatabase): AnnotationDao = db.annotationDao()
    @Provides fun provideForumDao(db: NebDatabase): ForumDao = db.forumDao()
}
