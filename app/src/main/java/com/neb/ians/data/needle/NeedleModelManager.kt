package com.neb.ians.data.needle

import android.content.Context
import android.os.StatFs
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import java.io.FileOutputStream
import java.security.MessageDigest
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request

sealed interface NeedleModelState {
    data object Checking : NeedleModelState
    data object NotInstalled : NeedleModelState
    data class Downloading(val downloadedBytes: Long, val totalBytes: Long) : NeedleModelState
    data class Ready(val sizeBytes: Long) : NeedleModelState
    data class Error(val message: String, val resumableBytes: Long = 0L) : NeedleModelState
}

@Singleton
class NeedleModelManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        const val MODEL_SIZE_BYTES = 13_737_679L
        const val MODEL_SHA256 = "ca7950ac8aef26ed22d17f92c733c9374aa7f59f6c2abb0fe2ac320a04f3c3d8"
        private const val MIN_FREE_BYTES = 72L * 1024L * 1024L
        private val MODEL_URLS = listOf(
            "https://nebians.consica.com.np/static/web/js/needle2/needle2.cact?v=2",
            "https://www.nebians.consica.com.np/static/web/js/needle2/needle2.cact?v=2"
        )
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val client = OkHttpClient.Builder().retryOnConnectionFailure(true).build()
    private val modelDirectory = File(context.noBackupFilesDir, "needle2")
    val modelFile = File(modelDirectory, "needle2.cact")
    private val partialFile = File(modelDirectory, "needle2.cact.part")
    private val _state = MutableStateFlow<NeedleModelState>(NeedleModelState.Checking)
    val state: StateFlow<NeedleModelState> = _state.asStateFlow()
    private var downloadJob: Job? = null

    init {
        scope.launch { verifyInstalledModel() }
    }

    fun download() {
        if (downloadJob?.isActive == true || _state.value is NeedleModelState.Ready) return
        downloadJob = scope.launch {
            try {
                modelDirectory.mkdirs()
                if (StatFs(modelDirectory.absolutePath).availableBytes < MIN_FREE_BYTES) {
                    throw IllegalStateException("At least 72 MB of free storage is needed for setup")
                }
                var lastError: Throwable? = null
                for (url in MODEL_URLS) {
                    try {
                        downloadFrom(url)
                        verifyDownloadedModel()
                        _state.value = NeedleModelState.Ready(modelFile.length())
                        return@launch
                    } catch (error: Throwable) {
                        lastError = error
                    }
                }
                throw lastError ?: IllegalStateException("Model download failed")
            } catch (error: Throwable) {
                if (error is kotlinx.coroutines.CancellationException) throw error
                _state.value = NeedleModelState.Error(
                    message = error.message ?: "Could not download the on-device model",
                    resumableBytes = partialFile.takeIf { it.exists() }?.length() ?: 0L
                )
            }
        }
    }

    fun cancelDownload() {
        val active = downloadJob ?: return
        scope.launch {
            active.cancelAndJoin()
            downloadJob = null
            _state.value = NeedleModelState.NotInstalled
        }
    }

    fun deleteModel(onDeleted: (() -> Unit)? = null) {
        scope.launch {
            downloadJob?.cancelAndJoin()
            downloadJob = null
            modelFile.delete()
            partialFile.delete()
            _state.value = NeedleModelState.NotInstalled
            withContext(Dispatchers.Main) { onDeleted?.invoke() }
        }
    }

    private suspend fun verifyInstalledModel() {
        modelDirectory.mkdirs()
        if (!modelFile.exists() || modelFile.length() != MODEL_SIZE_BYTES) {
            if (modelFile.exists()) modelFile.delete()
            _state.value = NeedleModelState.NotInstalled
            return
        }
        _state.value = if (sha256(modelFile) == MODEL_SHA256) {
            NeedleModelState.Ready(modelFile.length())
        } else {
            modelFile.delete()
            NeedleModelState.Error("The saved model failed its integrity check")
        }
    }

    private fun downloadFrom(url: String) {
        var existing = partialFile.takeIf { it.exists() }?.length() ?: 0L
        if (existing >= MODEL_SIZE_BYTES) {
            partialFile.delete()
            existing = 0L
        }

        val requestBuilder = Request.Builder()
            .url(url)
            .header("User-Agent", "NEBians-Android/${com.neb.ians.BuildConfig.VERSION_NAME}")
        if (existing > 0L) requestBuilder.header("Range", "bytes=$existing-")

        client.newCall(requestBuilder.build()).execute().use { response ->
            if (!response.isSuccessful) throw IllegalStateException("Download server returned ${response.code}")
            val body = response.body ?: throw IllegalStateException("Download server returned no model data")
            val append = existing > 0L && response.code == 206
            if (!append) existing = 0L
            val responseTotal = if (append) existing + body.contentLength().coerceAtLeast(0L) else body.contentLength()
            val total = responseTotal.takeIf { it > 0L } ?: MODEL_SIZE_BYTES
            FileOutputStream(partialFile, append).use { output ->
                body.byteStream().use { input ->
                    val buffer = ByteArray(128 * 1024)
                    var downloaded = existing
                    var lastUpdate = 0L
                    while (true) {
                        val read = input.read(buffer)
                        if (read < 0) break
                        output.write(buffer, 0, read)
                        downloaded += read
                        val now = android.os.SystemClock.elapsedRealtime()
                        if (now - lastUpdate >= 100L) {
                            _state.value = NeedleModelState.Downloading(downloaded, total)
                            lastUpdate = now
                        }
                    }
                    output.fd.sync()
                    _state.value = NeedleModelState.Downloading(downloaded, total)
                }
            }
        }
    }

    private fun verifyDownloadedModel() {
        if (partialFile.length() != MODEL_SIZE_BYTES) {
            throw IllegalStateException("Incomplete model download (${partialFile.length()} of $MODEL_SIZE_BYTES bytes)")
        }
        if (sha256(partialFile) != MODEL_SHA256) {
            partialFile.delete()
            throw IllegalStateException("Model integrity verification failed")
        }
        if (modelFile.exists()) modelFile.delete()
        if (!partialFile.renameTo(modelFile)) {
            partialFile.copyTo(modelFile, overwrite = true)
            partialFile.delete()
        }
    }

    private fun sha256(file: File): String {
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().buffered().use { input ->
            val buffer = ByteArray(128 * 1024)
            while (true) {
                val read = input.read(buffer)
                if (read < 0) break
                digest.update(buffer, 0, read)
            }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }
}
