package com.neb.ians.ui.screens.pdf

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.net.Uri
import android.os.ParcelFileDescriptor
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.data.model.PdfAnnotation
import com.neb.ians.data.repository.AnnotationRepository
import com.neb.ians.data.repository.ContentRepository
import com.neb.ians.util.PdfCacheManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

class PdfViewerViewModel(
    private val pdfUri: String,
    private val cacheManager: PdfCacheManager,
    private val annotationRepository: AnnotationRepository
) : ViewModel() {

    var renderer: PdfRenderer? = null
        private set
    var pageCount by mutableIntStateOf(0)
        private set
    var currentPage by mutableIntStateOf(0)
        private set
    var bitmap by mutableStateOf<Bitmap?>(null)
        private set
    var isLoading by mutableStateOf(false)
        private set
    var error by mutableStateOf<String?>(null)
        private set

    var annotationMode by mutableStateOf<AnnotationMode?>(null)
    val annotations = mutableStateListOf<PdfAnnotation>()

    private var pdfFile: File? = null

    sealed class AnnotationMode(val type: AnnotationType, val color: Int) {
        data object Highlight : AnnotationMode(AnnotationType.HIGHLIGHT, android.graphics.Color.YELLOW)
        data object Underline : AnnotationMode(AnnotationType.UNDERLINE, android.graphics.Color.RED)
        data object StickyNote : AnnotationMode(AnnotationType.STICKY_NOTE, android.graphics.Color.CYAN)
    }

    init {
        loadPdf()
    }

    private fun loadPdf() {
        viewModelScope.launch {
            isLoading = true
            error = null
            try {
                val file = withContext(Dispatchers.IO) {
                    cacheManager.getCachedFile(pdfUri)
                        ?: cacheManager.downloadAndCache(pdfUri)
                }
                if (file == null || !file.exists()) {
                    error = "Failed to load PDF"
                    isLoading = false
                    return@launch
                }
                pdfFile = file
                withContext(Dispatchers.IO) {
                    val pfd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                    val r = PdfRenderer(pfd)
                    renderer = r
                    pageCount = r.pageCount
                }
                renderPage(0)
                loadAnnotations()
            } catch (e: Exception) {
                error = e.message
            } finally {
                isLoading = false
            }
        }
    }

    fun renderPage(index: Int) {
        val r = renderer ?: return
        if (index < 0 || index >= r.pageCount) return
        viewModelScope.launch {
            isLoading = true
            bitmap = withContext(Dispatchers.IO) {
                val page = r.openPage(index)
                val bmp = Bitmap.createBitmap(
                    page.width.coerceAtMost(2000),
                    page.height.coerceAtMost(3000),
                    Bitmap.Config.ARGB_8888
                )
                page.render(bmp, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                page.close()
                bmp
            }
            currentPage = index
            isLoading = false
        }
    }

    fun nextPage() = renderPage(currentPage + 1)
    fun prevPage() = renderPage(currentPage - 1)

    fun addAnnotation(x: Float, y: Float, width: Float, height: Float, note: String? = null) {
        val mode = annotationMode ?: return
        val ann = PdfAnnotation(
            pdfUri = pdfUri,
            pageIndex = currentPage,
            x = x,
            y = y,
            width = width,
            height = height,
            type = mode.type,
            color = mode.color,
            noteText = note
        )
        annotations.add(ann)
    }

    private fun loadAnnotations() {
        viewModelScope.launch {
            annotationRepository.getAnnotations(pdfUri).collect { list: List<PdfAnnotation> ->
                annotations.clear()
                annotations.addAll(list)
            }
        }
    }

    fun persistAnnotations() {
        viewModelScope.launch {
            annotations.forEach { annotationRepository.save(it) }
        }
    }

    override fun onCleared() {
        super.onCleared()
        renderer?.close()
    }
}
