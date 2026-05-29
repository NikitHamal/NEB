package com.neb.ians.ui.screens.reader

import android.app.Application
import android.graphics.Bitmap
import android.graphics.Paint
import android.graphics.pdf.PdfDocument
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.local.entity.AnnotationEntity
import com.neb.ians.data.local.entity.BookmarkEntity
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.AnnotationRepository
import com.neb.ians.data.repository.BookmarkRepository
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import javax.inject.Inject

enum class AnnotationMode {
    NONE, HIGHLIGHT, UNDERLINE, STICKY_NOTE
}

data class PendingAnnotationCoords(
    val startX: Float,
    val startY: Float,
    val endX: Float,
    val endY: Float
)

data class ReaderPageState(
    val resource: ResourceEntity? = null,
    val currentPage: Int = 0,
    val totalPages: Int = 0,
    val pageBitmap: Bitmap? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
    val needsDownload: Boolean = false,
    val isDownloading: Boolean = false,
    val downloadProgress: Int = 0
)

data class ReaderAnnotationState(
    val annotations: List<AnnotationEntity> = emptyList(),
    val annotationMode: AnnotationMode = AnnotationMode.NONE,
    val showAnnotationTools: Boolean = false,
    val selectedColor: Int = 0xFFFFEB3B.toInt()
)

data class ReaderDialogState(
    val stickyNoteText: String = "",
    val showStickyNoteDialog: Boolean = false,
    val showBookmarkDialog: Boolean = false,
    val pendingAnnotationCoords: PendingAnnotationCoords? = null
)

data class ReaderBookmarksState(
    val bookmarks: List<BookmarkEntity> = emptyList()
)

@HiltViewModel
class ReaderViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val resourceRepository: ResourceRepository,
    private val annotationRepository: AnnotationRepository,
    private val bookmarkRepository: BookmarkRepository,
    private val downloadManager: ResourceDownloadManager
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""

    private val _pageState = MutableStateFlow(ReaderPageState())
    val pageState: StateFlow<ReaderPageState> = _pageState.asStateFlow()

    private val _annotationState = MutableStateFlow(ReaderAnnotationState())
    val annotationState: StateFlow<ReaderAnnotationState> = _annotationState.asStateFlow()

    private val _dialogState = MutableStateFlow(ReaderDialogState())
    val dialogState: StateFlow<ReaderDialogState> = _dialogState.asStateFlow()

    private val _bookmarksState = MutableStateFlow(ReaderBookmarksState())
    val bookmarksState: StateFlow<ReaderBookmarksState> = _bookmarksState.asStateFlow()

    private var pdfRenderer: PdfRenderer? = null
    private var fileDescriptor: ParcelFileDescriptor? = null
    private var currentBitmap: Bitmap? = null

    init {
        loadResource()
        loadAnnotations()
        loadBookmarks()
        observeDownloadProgress()
    }

    private fun observeDownloadProgress() {
        viewModelScope.launch {
            downloadManager.downloadProgress.collect { progressMap ->
                val progress = progressMap[resourceId] ?: 0
                val downloading = downloadManager.isDownloading(resourceId)
                _pageState.update {
                    it.copy(
                        downloadProgress = progress,
                        isDownloading = downloading
                    )
                }
                if (progress == 100 && downloading) {
                    _pageState.update { it.copy(isDownloading = false) }
                }
            }
        }
    }

    private fun loadResource() {
        viewModelScope.launch {
            resourceRepository.getResourceById(resourceId)
                .distinctUntilChanged()
                .collect { resource ->
                    _pageState.update { it.copy(resource = resource) }
                    if (resource != null) {
                        resourceRepository.incrementViewCount(resource.id)
                        val localFile = downloadManager.getLocalFile(resource)
                        if (localFile != null && localFile.exists()) {
                            _pageState.update { it.copy(needsDownload = false) }
                            openPdf(localFile.absolutePath)
                        } else if (resource.fileUrl.isNotBlank()) {
                            _pageState.update { it.copy(needsDownload = true, isLoading = false) }
                        } else {
                            loadSamplePdf()
                        }
                    }
                }
        }
    }

    fun downloadResource() {
        val resource = _pageState.value.resource ?: return
        if (downloadManager.isDownloading(resource.id)) return
        _pageState.update { it.copy(isDownloading = true, downloadProgress = 0) }
        downloadManager.downloadResource(resource)
        viewModelScope.launch {
            resourceRepository.getResourceById(resource.id)
                .distinctUntilChanged()
                .collect { updated ->
                    if (updated != null && updated.isDownloaded && !updated.localPath.isNullOrBlank()) {
                        val file = File(updated.localPath)
                        if (file.exists()) {
                            _pageState.update { it.copy(needsDownload = false) }
                            openPdf(updated.localPath)
                            return@collect
                        }
                    }
                }
        }
    }

    fun cancelDownload() {
        downloadManager.cancelDownload(resourceId)
        _pageState.update { it.copy(isDownloading = false, downloadProgress = 0) }
    }

    private fun loadAnnotations() {
        viewModelScope.launch {
            annotationRepository.getAnnotationsForResource(resourceId)
                .distinctUntilChanged()
                .collect { annotations ->
                    _annotationState.update { it.copy(annotations = annotations) }
                }
        }
    }

    private fun loadBookmarks() {
        viewModelScope.launch {
            bookmarkRepository.getBookmarksForResource(resourceId)
                .distinctUntilChanged()
                .collect { bookmarks ->
                    _bookmarksState.update { it.copy(bookmarks = bookmarks) }
                }
        }
    }

    private suspend fun openPdf(path: String) {
        withContext(Dispatchers.IO) {
            try {
                val file = File(path)
                if (file.exists()) {
                    fileDescriptor = ParcelFileDescriptor.open(
                        file,
                        ParcelFileDescriptor.MODE_READ_ONLY
                    )
                    pdfRenderer = PdfRenderer(fileDescriptor!!)
                    val totalPages = pdfRenderer!!.pageCount
                    _pageState.update { it.copy(totalPages = totalPages, isLoading = false) }
                    renderPage(0)
                }
            } catch (e: Exception) {
                _pageState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }

    private fun loadSamplePdf() {
        viewModelScope.launch {
            withContext(Dispatchers.IO) {
                try {
                    val sampleFile = File(application.cacheDir, "sample_${resourceId}.pdf")
                    if (!sampleFile.exists()) {
                        createSamplePdf(sampleFile)
                    }
                    fileDescriptor = ParcelFileDescriptor.open(
                        sampleFile,
                        ParcelFileDescriptor.MODE_READ_ONLY
                    )
                    pdfRenderer = PdfRenderer(fileDescriptor!!)
                    val totalPages = pdfRenderer!!.pageCount
                    _pageState.update { it.copy(totalPages = totalPages, isLoading = false) }
                    renderPage(0)
                } catch (e: Exception) {
                    _pageState.update { it.copy(isLoading = false, totalPages = 5) }
                }
            }
        }
    }

    private fun createSamplePdf(file: File) {
        val document = android.graphics.pdf.PdfDocument()
        val title = _pageState.value.resource?.title ?: "NEBians"
        val pages = listOf(
            title,
            "This is a sample document.\nOpen a real PDF to use the full reader.",
            "Features:\n- Highlight\n- Underline\n- Sticky Notes\n- Bookmarks"
        )
        val paint = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
            textSize = 24f
            color = android.graphics.Color.BLACK
        }
        for (pageText in pages) {
            val pageInfo = PdfDocument.PageInfo.Builder(612, 792, 1).create()
            val page = document.startPage(pageInfo)
            page.canvas.drawText(pageText, 72f, 700f, paint)
            document.finishPage(page)
        }
        file.outputStream().use { out -> document.writeTo(out) }
        document.close()
    }

    private suspend fun renderPage(page: Int) {
        withContext(Dispatchers.IO) {
            try {
                pdfRenderer?.let { renderer ->
                    if (page < renderer.pageCount) {
                        val oldBitmap = currentBitmap
                        val pdfPage = renderer.openPage(page)
                        val bitmap = Bitmap.createBitmap(
                            pdfPage.width * 2,
                            pdfPage.height * 2,
                            Bitmap.Config.ARGB_8888
                        )
                        pdfPage.render(
                            bitmap,
                            null,
                            null,
                            PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY
                        )
                        pdfPage.close()
                        currentBitmap = bitmap
                        oldBitmap?.recycle()
                        _pageState.update { it.copy(pageBitmap = bitmap, currentPage = page) }
                    }
                }
            } catch (e: Exception) {
                _pageState.update { it.copy(error = e.message) }
            }
        }
    }

    fun goToPage(page: Int) {
        if (page in 0 until _pageState.value.totalPages) {
            viewModelScope.launch { renderPage(page) }
        }
    }

    fun nextPage() = goToPage(_pageState.value.currentPage + 1)
    fun previousPage() = goToPage(_pageState.value.currentPage - 1)

    fun setAnnotationMode(mode: AnnotationMode) {
        _annotationState.update {
            it.copy(
                annotationMode = if (it.annotationMode == mode) AnnotationMode.NONE else mode
            )
        }
    }

    fun toggleAnnotationTools() {
        _annotationState.update { it.copy(showAnnotationTools = !it.showAnnotationTools) }
    }

    fun setSelectedColor(color: Int) {
        _annotationState.update { it.copy(selectedColor = color) }
    }

    fun addAnnotation(
        startX: Float, startY: Float, endX: Float, endY: Float, text: String = ""
    ) {
        val state = _annotationState.value
        val pageState = _pageState.value
        val annotation = AnnotationEntity(
            resourceId = resourceId,
            page = pageState.currentPage,
            type = state.annotationMode.name,
            content = if (state.annotationMode == AnnotationMode.STICKY_NOTE) _dialogState.value.stickyNoteText else "",
            startX = startX, startY = startY, endX = endX, endY = endY,
            color = state.selectedColor,
            createdAt = System.currentTimeMillis(),
            text = text
        )
        viewModelScope.launch { annotationRepository.addAnnotation(annotation) }
    }

    fun prepareStickyNote(startX: Float, startY: Float, endX: Float, endY: Float) {
        _dialogState.update {
            it.copy(
                pendingAnnotationCoords = PendingAnnotationCoords(startX, startY, endX, endY),
                stickyNoteText = "",
                showStickyNoteDialog = true
            )
        }
    }

    fun savePendingStickyNote() {
        val dialogState = _dialogState.value
        val annotationState = _annotationState.value
        val pageState = _pageState.value
        val coords = dialogState.pendingAnnotationCoords ?: return
        val annotation = AnnotationEntity(
            resourceId = resourceId,
            page = pageState.currentPage,
            type = AnnotationMode.STICKY_NOTE.name,
            content = dialogState.stickyNoteText,
            startX = coords.startX, startY = coords.startY, endX = coords.endX, endY = coords.endY,
            color = annotationState.selectedColor,
            createdAt = System.currentTimeMillis(),
            text = ""
        )
        viewModelScope.launch { annotationRepository.addAnnotation(annotation) }
        _dialogState.update {
            it.copy(pendingAnnotationCoords = null, stickyNoteText = "", showStickyNoteDialog = false)
        }
    }

    fun cancelStickyNote() {
        _dialogState.update {
            it.copy(pendingAnnotationCoords = null, stickyNoteText = "", showStickyNoteDialog = false)
        }
    }

    fun deleteAnnotation(id: Long) {
        viewModelScope.launch { annotationRepository.deleteAnnotation(id) }
    }

    fun showStickyNoteDialog(show: Boolean) {
        _dialogState.update { it.copy(showStickyNoteDialog = show) }
    }

    fun onStickyNoteTextChange(text: String) {
        _dialogState.update { it.copy(stickyNoteText = text) }
    }

    fun addBookmark(title: String) {
        viewModelScope.launch {
            bookmarkRepository.addBookmark(
                BookmarkEntity(
                    resourceId = resourceId,
                    page = _pageState.value.currentPage,
                    title = title,
                    createdAt = System.currentTimeMillis()
                )
            )
        }
    }

    fun showBookmarkDialog(show: Boolean) {
        _dialogState.update { it.copy(showBookmarkDialog = show) }
    }

    fun deleteBookmark(id: Long) {
        viewModelScope.launch { bookmarkRepository.deleteBookmark(id) }
    }

    override fun onCleared() {
        super.onCleared()
        downloadManager.cancelDownload(resourceId)
        currentBitmap?.recycle()
        currentBitmap = null
        pdfRenderer?.close()
        fileDescriptor?.close()
    }
}