package com.neb.ians.util

import android.content.Context
import com.neb.ians.data.api.ApiResource
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
    @ApplicationContext private val context: Context
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val activeDownloads = mutableMapOf<String, Job>()

    private val _downloadProgress = MutableStateFlow<Map<String, Int>>(emptyMap())
    val downloadProgress: StateFlow<Map<String, Int>> = _downloadProgress

    private val downloadedFiles = mutableMapOf<String, String>()

    fun downloadResourceFromApi(resource: ApiResource) {
        if (activeDownloads.containsKey(resource.id)) return

        val localFile = getLocalFile(resource.id, resource.fileUrl)
        if (localFile != null && localFile.exists()) return

        val job = scope.launch {
            try {
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = 0
                }

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
                            }
                        }
                    }
                }

                downloadedFiles[resource.id] = file.absolutePath
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = 100
                }
            } catch (e: Exception) {
                _downloadProgress.value = _downloadProgress.value.toMutableMap().apply {
                    this[resource.id] = -1
                }
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
    }

    fun isDownloading(resourceId: String): Boolean = activeDownloads.containsKey(resourceId)

    fun getLocalFile(resourceId: String, fileUrl: String): File? {
        downloadedFiles[resourceId]?.let { path ->
            val file = File(path)
            if (file.exists()) return file
        }
        val dir = File(context.filesDir, "resources")
        val file = File(dir, "${resourceId}.pdf")
        if (file.exists()) {
            downloadedFiles[resourceId] = file.absolutePath
            return file
        }
        return null
    }
}