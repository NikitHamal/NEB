package com.neb.ians.ui.screens.reader

import android.app.Application
import android.graphics.Bitmap
import android.graphics.Color
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
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
    val needsDownload: Boolean = false,
    val isLocalFileReady: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class PdfViewerViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val resourceRepository: ResourceRepository,
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""

    private val _uiState = MutableStateFlow(PdfViewerUiState())
    val uiState: StateFlow<PdfViewerUiState> = _uiState.asStateFlow()

    private var pdfRenderer: PdfRenderer? = null
    private var fileDescriptor: ParcelFileDescriptor? = null
    private val renderMutex = Mutex()
    private var fileUrl: String = ""

    // Target render width in pixels — balances clarity against memory.
    private val targetWidthPx = 1240

    init {
        load()
    }

    private fun load() {
        viewModelScope.launch {
            resourceRepository.getResource(resourceId)
                .onSuccess { resource ->
                    fileUrl = resource.fileUrl
                    _uiState.update { it.copy(title = resource.title) }
                    resourceRepository.viewResource(resourceId)
                    val localFile = downloadManager.getLocalFile(resource.id, resource.fileUrl)
                    if (localFile != null && localFile.exists()) {
                        openPdf(localFile)
                    } else if (resource.fileUrl.isNotBlank()) {
                        _uiState.update { it.copy(needsDownload = true, isLoading = false) }
                    } else {
                        _uiState.update { it.copy(isLoading = false, error = "No file available") }
                    }
                }
                .onFailure { e ->
                    _uiState.update { it.copy(isLoading = false, error = ApiErrorMapper.mapException(e)) }
                }
        }
    }

    fun download() {
        if (downloadManager.isDownloading(resourceId)) return
        _uiState.update { it.copy(isDownloading = true, downloadProgress = 0) }
        viewModelScope.launch {
            resourceRepository.getResource(resourceId).onSuccess { resource ->
                downloadManager.downloadResourceFromApi(resource)
                downloadManager.downloadProgress.collect { progressMap ->
                    val progress = progressMap[resourceId] ?: 0
                    when {
                        progress == 100 -> {
                            val localFile = downloadManager.getLocalFile(resourceId, resource.fileUrl)
                            if (localFile != null && localFile.exists()) {
                                _uiState.update { it.copy(isDownloading = false, needsDownload = false, isLoading = true) }
                                openPdf(localFile)
                                return@collect
                            }
                        }
                        progress < 0 -> {
                            _uiState.update { it.copy(isDownloading = false, error = "Download failed") }
                            return@collect
                        }
                        else -> _uiState.update { it.copy(downloadProgress = progress) }
                    }
                }
            }
        }
    }

    private suspend fun openPdf(file: File) {
        withContext(Dispatchers.IO) {
            try {
                fileDescriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                val renderer = PdfRenderer(fileDescriptor!!)
                pdfRenderer = renderer
                _uiState.update { it.copy(pageCount = renderer.pageCount, isLoading = false, isLocalFileReady = true, error = null) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = "Unable to open PDF") }
            }
        }
    }

    suspend fun renderPage(index: Int): Bitmap? = withContext(Dispatchers.IO) {
        val renderer = pdfRenderer ?: return@withContext null
        renderMutex.withLock {
            try {
                if (index < 0 || index >= renderer.pageCount) return@withContext null
                renderer.openPage(index).use { page ->
                    val scale = targetWidthPx.toFloat() / page.width
                    val width = targetWidthPx
                    val height = (page.height * scale).toInt().coerceAtLeast(1)
                    val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
                    bitmap.eraseColor(Color.WHITE)
                    page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    bitmap
                }
            } catch (e: Exception) {
                null
            }
        }
    }

    fun fileUrl(): String = fileUrl

    fun getLocalFile(): File? {
        return downloadManager.getLocalFile(resourceId, fileUrl)
    }

    override fun onCleared() {
        super.onCleared()
        runCatching { pdfRenderer?.close() }
        runCatching { fileDescriptor?.close() }
    }
}
