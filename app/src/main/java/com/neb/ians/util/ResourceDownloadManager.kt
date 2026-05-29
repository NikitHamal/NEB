package com.neb.ians.util

import android.content.Context
import com.neb.ians.data.local.dao.ResourceDao
import com.neb.ians.data.local.entity.ResourceEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ResourceDownloadManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val resourceDao: ResourceDao
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val activeDownloads = mutableMapOf<String, Job>()

    private val _downloadProgress = MutableStateFlow<Map<String, Int>>(emptyMap())
    val downloadProgress: StateFlow<Map<String, Int>> = _downloadProgress

    fun downloadResource(resource: ResourceEntity) {
        if (activeDownloads.containsKey(resource.id)) return
        if (resource.isDownloaded && !resource.localPath.isNullOrEmpty()) {
            val file = File(resource.localPath)
            if (file.exists()) return
        }

        val job = scope.launch {
            try {
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = 0
                }
                resourceDao.updateDownloadProgress(resource.id, 0)

                val url = resource.fileUrl
                if (url.isBlank()) {
                    _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                        this[resource.id] = -1
                    }
                    return@launch
                }

                val request = Request.Builder().url(url).build()
                val response = client.newCall(request).execute()

                if (!response.isSuccessful) {
                    _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                        this[resource.id] = -1
                    }
                    return@launch
                }

                val body = response.body ?: run {
                    _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                        this[resource.id] = -1
                    }
                    return@launch
                }

                val dir = File(context.filesDir, "resources")
                if (!dir.exists()) dir.mkdirs()
                val file = File(dir, "${resource.id}.pdf")

                val contentLength = body.contentLength()
                var bytesDownloaded = 0L
                val buffer = ByteArray(8192)

                body.byteStream().use { input ->
                    file.outputStream().use { output ->
                        while (true) {
                            val read = input.read(buffer)
                            if (read == -1) break
                            output.write(buffer, 0, read)
                            bytesDownloaded += read
                            if (contentLength > 0) {
                                val progress = ((bytesDownloaded * 100) / contentLength).toInt()
                                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                                    this[resource.id] = progress
                                }
                                if (progress % 10 == 0) {
                                    resourceDao.updateDownloadProgress(resource.id, progress)
                                }
                            }
                        }
                    }
                }

                resourceDao.updateDownloadStatus(resource.id, true, file.absolutePath)
                resourceDao.updateDownloadProgress(resource.id, 100)
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = 100
                }
            } catch (e: Exception) {
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = -1
                }
                resourceDao.updateDownloadProgress(resource.id, -1)
            } finally {
                activeDownloads.remove(resource.id)
            }
        }
        activeDownloads[resource.id] = job
    }

    fun cancelDownload(resourceId: String) {
        activeDownloads[resourceId]?.cancel()
        activeDownloads.remove(resourceId)
        _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
            remove(resourceId)
        }
        scope.launch {
            resourceDao.updateDownloadProgress(resourceId, 0)
        }
    }

    fun isDownloading(resourceId: String): Boolean = activeDownloads.containsKey(resourceId)

    fun getLocalFile(resource: ResourceEntity): File? {
        if (!resource.isDownloaded) return null
        val path = resource.localPath ?: return null
        val file = File(path)
        return if (file.exists()) file else null
    }

    suspend fun deleteDownload(resourceId: String) {
        cancelDownload(resourceId)
        val resource = resourceDao.getByIdSync(resourceId) ?: return
        val path = resource.localPath
        if (!path.isNullOrEmpty()) {
            val file = File(path)
            if (file.exists()) file.delete()
        }
        resourceDao.updateDownloadStatus(resourceId, false, null)
        resourceDao.updateDownloadProgress(resourceId, 0)
    }
}