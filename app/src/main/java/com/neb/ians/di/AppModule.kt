package com.neb.ians.di

import android.content.Context
import androidx.room.Room
import com.neb.ians.data.local.AppDatabase
import com.neb.ians.data.repository.AnnotationRepository
import com.neb.ians.data.repository.ContentRepository
import com.neb.ians.data.repository.ForumRepository
import com.neb.ians.service.NotificationHelper
import com.neb.ians.util.PdfCacheManager

object AppModule {
    @Volatile
    private var db: AppDatabase? = null

    fun provideDatabase(context: Context): AppDatabase {
        return db ?: synchronized(this) {
            db ?: Room.databaseBuilder(
                context.applicationContext,
                AppDatabase::class.java,
                "nebians.db"
            )
                .fallbackToDestructiveMigration()
                .build()
                .also { db = it }
        }
    }

    fun provideContentRepository(context: Context): ContentRepository {
        return ContentRepository(provideDatabase(context).contentDao())
    }

    fun provideForumRepository(context: Context): ForumRepository {
        return ForumRepository(provideDatabase(context).forumDao())
    }

    fun provideAnnotationRepository(context: Context): AnnotationRepository {
        return AnnotationRepository(provideDatabase(context).annotationDao())
    }

    fun providePdfCacheManager(context: Context): PdfCacheManager {
        return PdfCacheManager(context)
    }

    fun provideNotificationHelper(context: Context): NotificationHelper {
        return NotificationHelper(context)
    }
}
