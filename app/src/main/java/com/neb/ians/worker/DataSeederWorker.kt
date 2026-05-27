package com.neb.ians.worker

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.neb.ians.data.local.dao.ForumDao
import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.model.SampleData
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class DataSeederWorker @AssistedInject constructor(
    @Assisted private val context: Context,
    @Assisted workerParams: WorkerParameters,
    private val resourceDao: ResourceDao,
    private val forumDao: ForumDao
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        return try {
            resourceDao.insertAll(SampleData.resources)
            SampleData.forumPosts.forEach { forumDao.insertPost(it) }
            SampleData.forumReplies.forEach { forumDao.insertReply(it) }
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}
