package com.neb.ians.di

import android.content.Context
import androidx.room.Room
import com.neb.ians.data.local.AnnotationDao
import com.neb.ians.data.local.ForumDao
import com.neb.ians.data.local.NebDatabase
import com.neb.ians.data.local.ResourceDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob

@Module
@InstallIn(SingletonComponent::class)
object DataModule {

    @Provides @Singleton
    fun provideDatabase(@ApplicationContext ctx: Context): NebDatabase =
        Room.databaseBuilder(ctx, NebDatabase::class.java, "nebians.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides fun provideResourceDao(db: NebDatabase): ResourceDao = db.resourceDao()
    @Provides fun provideAnnotationDao(db: NebDatabase): AnnotationDao = db.annotationDao()
    @Provides fun provideForumDao(db: NebDatabase): ForumDao = db.forumDao()

    @Provides @Singleton
    fun provideAppScope(): CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
}
