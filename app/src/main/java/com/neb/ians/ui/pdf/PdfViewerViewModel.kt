package com.neb.ians.ui.pdf

import android.app.Application
import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.model.AnnotationType
import com.neb.ians.data.model.PdfAnnotation
import com.neb.ians.data.repository.AnnotationRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.util.UUID

class PdfViewerViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = AnnotationRepository((application as NEBiansApp).database.pdfAnnotationDao())

    private val _pageBitmap = MutableLiveData<Bitmap?>()
    val pageBitmap: LiveData<Bitmap?> = _pageBitmap

    private val _annotations = MutableLiveData<List<PdfAnnotation>>(emptyList())
    val annotations: LiveData<List<PdfAnnotation>> = _annotations

    private val _pageInfo = MutableLiveData("1 / 1")
    val pageInfo: LiveData<String> = _pageInfo

    private var pdfRenderer: PdfRenderer? = null
    private var currentPage: PdfRenderer.Page? = null
    private var pageCount = 0
    private var currentPageIndex = 0
    private var currentPdfPath: String = ""

    fun openPdf(filePath: String) {
        currentPdfPath = filePath
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val file = File(filePath)
                if (!file.exists()) return@launch
                val descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                pdfRenderer?.close()
                pdfRenderer = PdfRenderer(descriptor)
                pageCount = pdfRenderer?.pageCount ?: 0
                currentPageIndex = 0
                withContext(Dispatchers.Main) {
                    renderPage(0)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun nextPage() {
        if (currentPageIndex < pageCount - 1) {
            renderPage(currentPageIndex + 1)
        }
    }

    fun prevPage() {
        if (currentPageIndex > 0) {
            renderPage(currentPageIndex - 1)
        }
    }

    fun renderPage(index: Int) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                currentPage?.close()
                val renderer = pdfRenderer ?: return@launch
                if (index < 0 || index >= renderer.pageCount) return@launch
                val page = renderer.openPage(index)
                currentPage = page
                currentPageIndex = index
                val bitmap = Bitmap.createBitmap(page.width, page.height, Bitmap.Config.ARGB_8888)
                page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                withContext(Dispatchers.Main) {
                    _pageBitmap.value = bitmap
                    _pageInfo.value = "${index + 1} / $pageCount"
                }
                loadAnnotations()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun loadAnnotations() {
        viewModelScope.launch(Dispatchers.IO) {
            val list = repository.getForPage(currentPdfPath, currentPageIndex)
            withContext(Dispatchers.Main) {
                _annotations.value = list
            }
        }
    }

    fun addAnnotation(
        type: AnnotationType,
        x: Float,
        y: Float,
        width: Float,
        height: Float,
        noteText: String? = null
    ) {
        viewModelScope.launch(Dispatchers.IO) {
            val annotation = PdfAnnotation(
                id = UUID.randomUUID().toString(),
                pdfPath = currentPdfPath,
                pageIndex = currentPageIndex,
                type = type,
                x = x,
                y = y,
                width = width,
                height = height,
                noteText = noteText
            )
            repository.save(annotation)
            loadAnnotations()
        }
    }

    override fun onCleared() {
        super.onCleared()
        currentPage?.close()
        pdfRenderer?.close()
    }
}
