package com.neb.ians.util

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.webkit.MimeTypeMap
import android.widget.Toast
import com.neb.ians.data.api.ApiClientException
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.api.WafChallengeInterceptor
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

data class DownloadedResource(
    val resourceId: String,
    val title: String,
    val type: String,
    val fileUrl: String,
    val localPath: String,
    val mimeType: String,
    val sizeBytes: Long,
    val downloadedAt: Long,
    val thumbnailUrl: String
)

@Singleton
class ResourceDownloadManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val client = OkHttpClient.Builder()
        .addInterceptor(WafChallengeInterceptor(context))
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(90, TimeUnit.SECONDS)
        .build()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val activeDownloads = mutableMapOf<String, Job>()
    private val indexLock = Any()
    private val resourceDir = File(context.filesDir, "offline_resources").apply { mkdirs() }
    private val indexFile = File(resourceDir, "downloads.json")
    private val _downloadProgress = MutableStateFlow<Map<String, Int>>(emptyMap())
    private val _downloads = MutableStateFlow(loadIndex())

    val downloadProgress: StateFlow<Map<String, Int>> = _downloadProgress.asStateFlow()
    val downloads: StateFlow<List<DownloadedResource>> = _downloads.asStateFlow()

    fun downloadResourceFromApi(resource: ApiResource) {
        if (findDownloaded(resource.id)?.let { File(it.localPath).exists() } == true) return
        val job = scope.launch(start = CoroutineStart.LAZY) {
            try {
                setProgress(resource.id, 0)
                if (resource.fileUrl.isBlank()) throw IOException("No file URL")
                client.newCall(Request.Builder().url(resource.fileUrl).build()).execute().use { response ->
                    if (!response.isSuccessful) throw IOException("HTTP ${response.code}")
                    val body = response.body ?: throw IOException("Empty response body")
                    val contentType = body.contentType()?.toString().orEmpty()
                    if (contentType.contains("text/html", true)) throw IOException("Security filter")
                    val mime = contentType.substringBefore(';').ifBlank { inferMime(resource.fileUrl, resource.type) }
                    val extension = inferExtension(resource.fileUrl, mime, resource.type)
                    val temp = File(resourceDir, "${resource.id}.$extension.part")
                    val target = File(resourceDir, "${resource.id}.$extension")
                    val total = body.contentLength()
                    var copied = 0L
                    body.byteStream().use { input ->
                        temp.outputStream().buffered().use { output ->
                            val buffer = ByteArray(DEFAULT_BUFFER_SIZE * 2)
                            while (true) {
                                val count = input.read(buffer)
                                if (count < 0) break
                                output.write(buffer, 0, count)
                                copied += count
                                if (total > 0) setProgress(resource.id, ((copied * 100) / total).toInt().coerceIn(0, 99))
                            }
                        }
                    }
                    if (target.exists()) target.delete()
                    if (!temp.renameTo(target)) {
                        temp.copyTo(target, overwrite = true)
                        temp.delete()
                    }
                    val item = DownloadedResource(
                        resourceId = resource.id,
                        title = resource.title,
                        type = resource.type,
                        fileUrl = resource.fileUrl,
                        localPath = target.absolutePath,
                        mimeType = mime,
                        sizeBytes = target.length(),
                        downloadedAt = System.currentTimeMillis(),
                        thumbnailUrl = resource.thumbnailUrl
                    )
                    synchronized(indexLock) {
                        _downloads.value = (_downloads.value.filterNot { it.resourceId == resource.id } + item)
                            .sortedByDescending { it.downloadedAt }
                        persistIndex(_downloads.value)
                    }
                }
                setProgress(resource.id, 100)
            } catch (e: CancellationException) {
                setProgress(resource.id, 0, remove = true)
                throw e
            } catch (e: Exception) {
                setProgress(resource.id, -1)
                if (e.message?.contains("Security filter") == true || e is ApiClientException) {
                    Handler(Looper.getMainLooper()).post {
                        Toast.makeText(context, "Server protected by security filter. Please try again later.", Toast.LENGTH_LONG).show()
                    }
                }
            } finally {
                synchronized(activeDownloads) { activeDownloads.remove(resource.id) }
            }
        }
        val shouldStart = synchronized(activeDownloads) {
            if (activeDownloads.containsKey(resource.id)) false
            else {
                activeDownloads[resource.id] = job
                true
            }
        }
        if (shouldStart) job.start() else job.cancel()
    }

    fun cancelDownload(resourceId: String) {
        synchronized(activeDownloads) { activeDownloads.remove(resourceId)?.cancel() }
        setProgress(resourceId, 0, remove = true)
        resourceDir.listFiles()?.filter { it.name.startsWith("$resourceId.") && it.name.endsWith(".part") }?.forEach(File::delete)
    }

    fun deleteDownload(resourceId: String) {
        synchronized(indexLock) {
            findDownloaded(resourceId)?.let { File(it.localPath).delete() }
            _downloads.value = _downloads.value.filterNot { it.resourceId == resourceId }
            persistIndex(_downloads.value)
        }
        setProgress(resourceId, 0, remove = true)
    }

    fun isDownloading(resourceId: String): Boolean = synchronized(activeDownloads) { activeDownloads.containsKey(resourceId) }

    fun findDownloaded(resourceId: String): DownloadedResource? = _downloads.value.firstOrNull { it.resourceId == resourceId }

    fun getLocalFile(resourceId: String, _fileUrl: String = ""): File? {
        findDownloaded(resourceId)?.let {
            val file = File(it.localPath)
            if (file.exists()) return file
        }
        val legacy = File(context.filesDir, "resources/$resourceId.pdf")
        return legacy.takeIf(File::exists)
    }

    private fun setProgress(resourceId: String, value: Int, remove: Boolean = false) {
        _downloadProgress.update { current ->
            current.toMutableMap().apply {
                if (remove) remove(resourceId) else this[resourceId] = value
            }
        }
    }

    private fun inferExtension(url: String, mime: String, type: String): String {
        val fromMime = MimeTypeMap.getSingleton().getExtensionFromMimeType(mime)
        if (!fromMime.isNullOrBlank()) return fromMime.lowercase()
        val fromUrl = url.substringBefore('?').substringAfterLast('.', "").lowercase().takeIf { it.matches(Regex("[a-z0-9]{2,5}")) }
        if (!fromUrl.isNullOrBlank()) return fromUrl
        return when {
            type.contains("video", true) -> "mp4"
            type.contains("audio", true) -> "mp3"
            else -> "pdf"
        }
    }

    private fun inferMime(url: String, type: String): String {
        val extension = url.substringBefore('?').substringAfterLast('.', "").lowercase()
        return MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension) ?: when {
            type.contains("video", true) -> "video/mp4"
            type.contains("audio", true) -> "audio/mpeg"
            else -> "application/pdf"
        }
    }

    private fun loadIndex(): List<DownloadedResource> = runCatching {
        val indexed = if (indexFile.exists()) {
            val array = JSONArray(indexFile.readText())
            buildList {
                for (i in 0 until array.length()) {
                    val o = array.getJSONObject(i)
                    val item = DownloadedResource(
                        resourceId = o.getString("resourceId"),
                        title = o.optString("title"),
                        type = o.optString("type"),
                        fileUrl = o.optString("fileUrl"),
                        localPath = o.getString("localPath"),
                        mimeType = o.optString("mimeType"),
                        sizeBytes = o.optLong("sizeBytes"),
                        downloadedAt = o.optLong("downloadedAt"),
                        thumbnailUrl = o.optString("thumbnailUrl")
                    )
                    if (File(item.localPath).exists()) add(item)
                }
            }
        } else emptyList()
        val indexedIds = indexed.map { it.resourceId }.toSet()
        val orphanFiles = resourceDir.listFiles()
            ?.filter { it.isFile && it.extension.matches(Regex("pdf|mp4|mp3|m4a|ogg|wav")) && !it.name.endsWith(".part") }
            ?.mapNotNull { file ->
                val id = file.nameWithoutExtension.substringBeforeLast('.')
                if (id in indexedIds) return@mapNotNull null
                DownloadedResource(
                    resourceId = id,
                    title = id,
                    type = if (file.extension == "pdf") "PDF" else if (file.extension in listOf("mp4", "webm")) "Video" else "Audio",
                    fileUrl = "",
                    localPath = file.absolutePath,
                    mimeType = if (file.extension == "pdf") "application/pdf" else "",
                    sizeBytes = file.length(),
                    downloadedAt = file.lastModified(),
                    thumbnailUrl = ""
                )
            } ?: emptyList()
        val legacyDir = File(context.filesDir, "resources")
        val legacyFiles = legacyDir.listFiles()
            ?.filter { it.isFile && it.name.endsWith(".pdf", true) }
            ?.mapNotNull { file ->
                val id = file.nameWithoutExtension
                if (id in indexedIds) return@mapNotNull null
                DownloadedResource(
                    resourceId = id,
                    title = id,
                    type = "PDF",
                    fileUrl = "",
                    localPath = file.absolutePath,
                    mimeType = "application/pdf",
                    sizeBytes = file.length(),
                    downloadedAt = file.lastModified(),
                    thumbnailUrl = ""
                )
            } ?: emptyList()
        (indexed + orphanFiles + legacyFiles).sortedByDescending { it.downloadedAt }
    }.getOrDefault(emptyList())

    private fun persistIndex(items: List<DownloadedResource>) {
        val array = JSONArray()
        items.forEach { item ->
            array.put(JSONObject().apply {
                put("resourceId", item.resourceId)
                put("title", item.title)
                put("type", item.type)
                put("fileUrl", item.fileUrl)
                put("localPath", item.localPath)
                put("mimeType", item.mimeType)
                put("sizeBytes", item.sizeBytes)
                put("downloadedAt", item.downloadedAt)
                put("thumbnailUrl", item.thumbnailUrl)
            })
        }
        indexFile.writeText(array.toString())
    }
}
