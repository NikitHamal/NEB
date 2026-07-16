package com.neb.ians.ui.screens.reader

import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.filterNotNull
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import java.io.File
import javax.inject.Inject

data class PdfViewerUiState(
    val title: String = "",
    val pageCount: Int = 0,
    val isLoading: Boolean = true,
    val isDownloading: Boolean = false,
    val downloadProgress: Int = 0,
    val isLocalFileReady: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class PdfViewerViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {
    private val resourceId: String = savedStateHandle.get<String>("resourceId").orEmpty()
    private val _uiState = MutableStateFlow(PdfViewerUiState())
    val uiState: StateFlow<PdfViewerUiState> = _uiState.asStateFlow()
    private var pdfRenderer: PdfRenderer? = null
    private var fileDescriptor: ParcelFileDescriptor? = null
    private val renderMutex = Mutex()
    private var resource: ApiResource? = null
    private var downloadJob: Job? = null
    private val targetWidthPx = 1240

    init { load() }

    fun retry() {
        resource?.let { startDownload(it) } ?: load()
    }

    private fun load() {
        viewModelScope.launch {
            val downloaded = downloadManager.findDownloaded(resourceId)
            val localFile = downloaded?.let { File(it.localPath) }?.takeIf(File::exists)
            if (localFile != null) {
                _uiState.update { it.copy(title = downloaded.title, isLoading = true, error = null) }
                openPdf(localFile)
                return@launch
            }
            _uiState.update { it.copy(isLoading = true, error = null) }
            resourceRepository.getResource(resourceId)
                .onSuccess { loaded ->
                    resource = loaded
                    _uiState.update { it.copy(title = loaded.title) }
                    resourceRepository.viewResource(resourceId)
                    val localFile = downloadManager.getLocalFile(loaded.id, loaded.fileUrl)
                    if (localFile?.exists() == true) {
                        openPdf(localFile)
                    } else if (loaded.fileUrl.isNotBlank()) {
                        startDownload(loaded)
                    } else {
                        _uiState.update { it.copy(isLoading = false, error = "No PDF file is available") }
                    }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(error)) }
                }
        }
    }

    private fun startDownload(item: ApiResource) {
        if (downloadJob?.isActive == true) return
        downloadJob = viewModelScope.launch {
            downloadManager.getLocalFile(item.id, item.fileUrl)?.takeIf(File::exists)?.let {
                openPdf(it)
                return@launch
            }
            _uiState.update {
                it.copy(isLoading = false, isDownloading = true, downloadProgress = 0, error = null)
            }
            if (!downloadManager.isDownloading(item.id)) {
                downloadManager.downloadResourceFromApi(item)
            }
            downloadManager.getLocalFile(item.id, item.fileUrl)?.takeIf(File::exists)?.let {
                _uiState.update { state -> state.copy(isDownloading = false, isLoading = true, downloadProgress = 100) }
                openPdf(it)
                return@launch
            }
            val progressJob = launch {
                downloadManager.downloadProgress
                    .map { it[item.id] }
                    .filterNotNull()
                    .collect { progress ->
                        if (progress in 0..99) {
                            _uiState.update { it.copy(downloadProgress = progress) }
                        }
                    }
            }
            val terminal = downloadManager.downloadProgress
                .map { it[item.id] }
                .filterNotNull()
                .first { it >= 100 || it < 0 }
            progressJob.cancelAndJoin()
            if (terminal >= 100) {
                val localFile = downloadManager.getLocalFile(item.id, item.fileUrl)
                if (localFile?.exists() == true) {
                    _uiState.update { it.copy(isDownloading = false, isLoading = true, downloadProgress = 100) }
                    openPdf(localFile)
                } else {
                    _uiState.update { it.copy(isDownloading = false, error = "Downloaded PDF could not be found") }
                }
            } else {
                _uiState.update { it.copy(isDownloading = false, error = "The PDF download failed") }
            }
        }
    }

    private suspend fun openPdf(file: File) {
        withContext(Dispatchers.IO) {
            runCatching {
                runCatching { pdfRenderer?.close() }
                runCatching { fileDescriptor?.close() }
                val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                val renderer = PdfRenderer(descriptor)
                fileDescriptor = descriptor
                pdfRenderer = renderer
                _uiState.update {
                    it.copy(
                        pageCount = renderer.pageCount,
                        isLoading = false,
                        isDownloading = false,
                        isLocalFileReady = true,
                        error = null
                    )
                }
            }.onFailure {
                _uiState.update { state -> state.copy(isLoading = false, isDownloading = false, error = "Unable to open PDF") }
            }
        }
    }

    suspend fun renderPage(index: Int): Bitmap? = withContext(Dispatchers.IO) {
        val renderer = pdfRenderer ?: return@withContext null
        renderMutex.withLock {
            runCatching {
                if (index !in 0 until renderer.pageCount) return@runCatching null
                renderer.openPage(index).use { page ->
                    val scale = targetWidthPx.toFloat() / page.width
                    val height = (page.height * scale).toInt().coerceAtLeast(1)
                    val bitmap = Bitmap.createBitmap(targetWidthPx, height, Bitmap.Config.ARGB_8888)
                    bitmap.eraseColor(Color.WHITE)
                    page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    bitmap
                }
            }.getOrNull()
        }
    }

    override fun onCleared() {
        runCatching { pdfRenderer?.close() }
        runCatching { fileDescriptor?.close() }
        super.onCleared()
    }
}
