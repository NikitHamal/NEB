package com.neb.ians.ui.screens.reader

import android.app.Application
import android.graphics.Bitmap
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

data class ReaderUiState(
    val resource: ResourceEntity? = null,
    val currentPage: Int = 0,
    val totalPages: Int = 0,
    val pageBitmap: Bitmap? = null,
    val annotations: List<AnnotationEntity> = emptyList(),
    val bookmarks: List<BookmarkEntity> = emptyList(),
    val annotationMode: AnnotationMode = AnnotationMode.NONE,
    val isLoading: Boolean = true,
    val showAnnotationTools: Boolean = false,
    val selectedColor: Int = 0xFFFFEB3B.toInt(),
    val stickyNoteText: String = "",
    val showStickyNoteDialog: Boolean = false,
    val showBookmarkDialog: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class ReaderViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val application: Application,
    private val resourceRepository: ResourceRepository,
    private val annotationRepository: AnnotationRepository,
    private val bookmarkRepository: BookmarkRepository
) : ViewModel() {

    private val resourceId: String = savedStateHandle.get<String>("resourceId") ?: ""
    private val _uiState = MutableStateFlow(ReaderUiState())
    val uiState: StateFlow<ReaderUiState> = _uiState.asStateFlow()

    private var pdfRenderer: PdfRenderer? = null
    private var fileDescriptor: ParcelFileDescriptor? = null

    init {
        loadResource()
        loadAnnotations()
        loadBookmarks()
    }

    private fun loadResource() {
        viewModelScope.launch {
            resourceRepository.getResourceById(resourceId).collect { resource ->
                _uiState.update { it.copy(resource = resource) }
                if (resource?.localPath != null) {
                    openPdf(resource.localPath)
                } else {
                    loadSamplePdf()
                }
            }
        }
    }

    private fun loadAnnotations() {
        viewModelScope.launch {
            annotationRepository.getAnnotationsForResource(resourceId).collect { annotations ->
                _uiState.update { it.copy(annotations = annotations) }
            }
        }
    }

    private fun loadBookmarks() {
        viewModelScope.launch {
            bookmarkRepository.getBookmarksForResource(resourceId).collect { bookmarks ->
                _uiState.update { it.copy(bookmarks = bookmarks) }
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
                    _uiState.update { it.copy(totalPages = totalPages, isLoading = false) }
                    renderPage(0)
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
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
                    _uiState.update { it.copy(totalPages = totalPages, isLoading = false) }
                    renderPage(0)
                } catch (e: Exception) {
                    _uiState.update { it.copy(isLoading = false, totalPages = 5) }
                }
            }
        }
    }

    private fun createSamplePdf(file: File) {
        val content = buildString {
            append("%PDF-1.4\n")
            append("1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n")
            append("2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n")
            append("3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]")
            append("/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n")
            append("4 0 obj<</Length 44>>stream\n")
            append("BT /F1 24 Tf 100 700 Td (NEBians Reader) Tj ET\n")
            append("endstream\nendobj\n")
            append("5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n")
            append("xref\n0 6\n")
            append("0000000000 65535 f \n")
            append("0000000009 00000 n \n")
            append("0000000058 00000 n \n")
            append("0000000115 00000 n \n")
            append("0000000266 00000 n \n")
            append("0000000360 00000 n \n")
            append("trailer<</Size 6/Root 1 0 R>>\nstartxref\n424\n%%EOF")
        }
        file.writeText(content)
    }

    private suspend fun renderPage(page: Int) {
        withContext(Dispatchers.IO) {
            try {
                pdfRenderer?.let { renderer ->
                    if (page < renderer.pageCount) {
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
                        _uiState.update { it.copy(pageBitmap = bitmap, currentPage = page) }
                    }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message) }
            }
        }
    }

    fun goToPage(page: Int) {
        if (page in 0 until _uiState.value.totalPages) {
            viewModelScope.launch { renderPage(page) }
        }
    }

    fun nextPage() = goToPage(_uiState.value.currentPage + 1)

    fun previousPage() = goToPage(_uiState.value.currentPage - 1)

    fun setAnnotationMode(mode: AnnotationMode) {
        _uiState.update {
            it.copy(
                annotationMode = if (it.annotationMode == mode) AnnotationMode.NONE else mode
            )
        }
    }

    fun toggleAnnotationTools() {
        _uiState.update { it.copy(showAnnotationTools = !it.showAnnotationTools) }
    }

    fun setSelectedColor(color: Int) {
        _uiState.update { it.copy(selectedColor = color) }
    }

    fun addAnnotation(
        startX: Float,
        startY: Float,
        endX: Float,
        endY: Float,
        text: String = ""
    ) {
        val state = _uiState.value
        val annotation = AnnotationEntity(
            resourceId = resourceId,
            page = state.currentPage,
            type = state.annotationMode.name,
            content = if (state.annotationMode == AnnotationMode.STICKY_NOTE) {
                state.stickyNoteText
            } else {
                ""
            },
            startX = startX,
            startY = startY,
            endX = endX,
            endY = endY,
            color = state.selectedColor,
            createdAt = System.currentTimeMillis(),
            text = text
        )
        viewModelScope.launch {
            annotationRepository.addAnnotation(annotation)
        }
    }

    fun deleteAnnotation(id: Long) {
        viewModelScope.launch {
            annotationRepository.deleteAnnotation(id)
        }
    }

    fun showStickyNoteDialog(show: Boolean) {
        _uiState.update { it.copy(showStickyNoteDialog = show) }
    }

    fun onStickyNoteTextChange(text: String) {
        _uiState.update { it.copy(stickyNoteText = text) }
    }

    fun addBookmark(title: String) {
        viewModelScope.launch {
            bookmarkRepository.addBookmark(
                BookmarkEntity(
                    resourceId = resourceId,
                    page = _uiState.value.currentPage,
                    title = title,
                    createdAt = System.currentTimeMillis()
                )
            )
        }
    }

    fun showBookmarkDialog(show: Boolean) {
        _uiState.update { it.copy(showBookmarkDialog = show) }
    }

    fun deleteBookmark(id: Long) {
        viewModelScope.launch {
            bookmarkRepository.deleteBookmark(id)
        }
    }

    override fun onCleared() {
        super.onCleared()
        pdfRenderer?.close()
        fileDescriptor?.close()
    }
}
