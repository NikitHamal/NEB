package com.agentx.app.data.engine

import android.content.Context
import android.os.StatFs
import com.agentx.app.BuildConfig
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

sealed interface AxModelState {
    data object Checking : AxModelState
    data object NotInstalled : AxModelState
    data class Downloading(val downloadedBytes: Long, val totalBytes: Long) : AxModelState
    data class Verifying(val downloadedBytes: Long) : AxModelState
    data class Ready(val sizeBytes: Long) : AxModelState
    data class Error(val message: String, val resumableBytes: Long = 0L) : AxModelState
}

@Singleton
class NeedleModelManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        const val MODEL_SIZE_BYTES = 35_335_380L
        const val MODEL_SHA256 = "c9d915eca282ed42d1a09b143b592adb4cc6744ffe2d294adf5cfc5548170c38"
        const val MODEL_VERSION = "needle3-full-20L"
        private const val MIN_FREE_BYTES = 220L * 1024L * 1024L
        private val MODEL_URLS = listOf(
            "https://nebians.consica.com.np/static/web/js/needle3/needle3.cact?v=3",
            "https://www.nebians.consica.com.np/static/web/js/needle3/needle3.cact?v=3"
        )
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val client = OkHttpClient.Builder().retryOnConnectionFailure(true).build()
    private val modelDirectory = File(context.noBackupFilesDir, "axmodels")
    val modelFile = File(modelDirectory, "needle3.cact")
    private val partialFile = File(modelDirectory, "needle3.cact.part")
    private val _state = MutableStateFlow<AxModelState>(AxModelState.Checking)
    val state: StateFlow<AxModelState> = _state.asStateFlow()
    private var downloadJob: Job? = null

    init {
        scope.launch { verifyInstalledModel() }
    }

    fun recheck() {
        scope.launch { verifyInstalledModel() }
    }

    fun download() {
        if (downloadJob?.isActive == true || _state.value is AxModelState.Ready) return
        downloadJob = scope.launch {
            try {
                modelDirectory.mkdirs()
                if (StatFs(modelDirectory.absolutePath).availableBytes < MIN_FREE_BYTES) {
                    throw IllegalStateException("At least 220 MB of free storage is needed (model plus runtime snapshot)")
                }
                var lastError: Throwable? = null
                for (url in MODEL_URLS) {
                    try {
                        downloadFrom(url)
                        verifyDownloadedModel()
                        _state.value = AxModelState.Ready(modelFile.length())
                        return@launch
                    } catch (error: Throwable) {
                        lastError = error
                    }
                }
                throw lastError ?: IllegalStateException("Model download failed")
            } catch (error: Throwable) {
                if (error is kotlinx.coroutines.CancellationException) throw error
                _state.value = AxModelState.Error(
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
            _state.value = AxModelState.NotInstalled
        }
    }

    fun deleteModel(onDeleted: (() -> Unit)? = null) {
        scope.launch {
            downloadJob?.cancelAndJoin()
            downloadJob = null
            modelFile.delete()
            partialFile.delete()
            _state.value = AxModelState.NotInstalled
            withContext(Dispatchers.Main) { onDeleted?.invoke() }
        }
    }

    private suspend fun verifyInstalledModel() {
        modelDirectory.mkdirs()
        if (!modelFile.exists() || modelFile.length() != MODEL_SIZE_BYTES) {
            if (modelFile.exists()) modelFile.delete()
            _state.value = AxModelState.NotInstalled
            return
        }
        _state.value = if (sha256(modelFile) == MODEL_SHA256) {
            AxModelState.Ready(modelFile.length())
        } else {
            modelFile.delete()
            AxModelState.Error("The saved model failed its integrity check")
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
            .header("User-Agent", "AgentX-Android/" + BuildConfig.VERSION_NAME)
        if (existing > 0L) requestBuilder.header("Range", "bytes=$existing-")
        client.newCall(requestBuilder.build()).execute().use { response ->
            if (!response.isSuccessful) throw IllegalStateException("Download server returned " + response.code)
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
                            _state.value = AxModelState.Downloading(downloaded, total)
                            lastUpdate = now
                        }
                    }
                    output.fd.sync()
                    _state.value = AxModelState.Downloading(downloaded, total)
                }
            }
        }
    }

    private fun verifyDownloadedModel() {
        if (partialFile.length() != MODEL_SIZE_BYTES) {
            throw IllegalStateException("Incomplete model download (" + partialFile.length() + " of $MODEL_SIZE_BYTES bytes)")
        }
        _state.value = AxModelState.Verifying(partialFile.length())
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
            val buffer = ByteArray(256 * 1024)
            while (true) {
                val read = input.read(buffer)
                if (read < 0) break
                digest.update(buffer, 0, read)
            }
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }
}
