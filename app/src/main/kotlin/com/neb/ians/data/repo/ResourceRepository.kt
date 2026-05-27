package com.neb.ians.data.repo

import android.content.Context
import com.neb.ians.data.db.AnnotationDao
import com.neb.ians.data.db.AnnotationEntity
import com.neb.ians.data.db.ResourceDao
import com.neb.ians.data.db.ResourceEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import java.io.File
import java.net.URL
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ResourceRepository @Inject constructor(
    @ApplicationContext private val ctx: Context,
    private val resourceDao: ResourceDao,
    private val annotationDao: AnnotationDao,
) {
    suspend fun seedIfEmpty() {
        if (resourceDao.observeAll().first().isNotEmpty()) return
        resourceDao.upsertAll(SeedData.resources)
    }

    fun search(query: String, subject: String?, grade: String?, type: String?): Flow<List<ResourceEntity>> =
        resourceDao.search(query, subject, grade, type)

    fun observeAll(): Flow<List<ResourceEntity>> = resourceDao.observeAll()

    fun observeById(id: String): Flow<ResourceEntity?> = resourceDao.observeById(id)

    suspend fun toggleFavorite(id: String) {
        val r = resourceDao.getById(id) ?: return
        resourceDao.setFavorite(id, !r.isFavorite)
    }

    /**
     * Downloads the PDF to the app's cacheDir/pdf folder using a content-hash filename.
     * Emits progress as Float in [0,1]; final emission carries the local file path or null on failure.
     */
    fun downloadToCache(resource: ResourceEntity): Flow<Float> = flow {
        emit(0f)
        val dir = File(ctx.cacheDir, "pdf").apply { mkdirs() }
        val outFile = File(dir, "${resource.id}.pdf")
        if (outFile.exists() && outFile.length() > 0) {
            resourceDao.markDownloaded(resource.id, outFile.absolutePath, System.currentTimeMillis())
            emit(1f); return@flow
        }
        runCatching {
            val conn = URL(resource.sourceUrl).openConnection()
            conn.connectTimeout = 15_000
            conn.readTimeout = 30_000
            val total = conn.contentLengthLong.coerceAtLeast(1L)
            conn.getInputStream().use { input ->
                outFile.outputStream().use { output ->
                    val buf = ByteArray(64 * 1024)
                    var read = 0L
                    while (true) {
                        val n = input.read(buf)
                        if (n <= 0) break
                        output.write(buf, 0, n)
                        read += n
                        emit((read.toFloat() / total).coerceIn(0f, 1f))
                    }
                }
            }
            resourceDao.markDownloaded(resource.id, outFile.absolutePath, System.currentTimeMillis())
            emit(1f)
        }.onFailure {
            outFile.delete()
            emit(-1f)
        }
    }.flowOn(Dispatchers.IO)

    fun annotations(resourceId: String): Flow<List<AnnotationEntity>> =
        annotationDao.observeForResource(resourceId)

    suspend fun saveAnnotation(a: AnnotationEntity): Long = annotationDao.insert(a)

    suspend fun deleteAnnotation(id: Long) = annotationDao.delete(id)
}
