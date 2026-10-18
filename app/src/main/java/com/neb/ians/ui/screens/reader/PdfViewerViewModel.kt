package com.neb.ians.ui.screens.reader

import android.content.Context
import android.graphics.Bitmap
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.api.ApiErrorMapper
import com.neb.ians.data.api.ApiResource
import com.neb.ians.data.repository.ResourceRepository
import com.neb.ians.ui.screens.reader.pdf.PdfDocumentEngine
import com.neb.ians.ui.screens.reader.pdf.ReaderPrefs
import com.neb.ians.ui.screens.reader.pdf.ReadingLayout
import com.neb.ians.ui.screens.reader.pdf.ReadingTheme
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
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
    val error: String? = null,
    /** Height / width of each page, so the layout is right before a page is rendered. */
    val pageAspects: List<Float> = emptyList(),
    val currentPage: Int = 0,
    /** Page to restore on open; consumed once by the screen. */
    val resumePage: Int? = null,
    val bookmarks: Set<Int> = emptySet(),
    val theme: ReadingTheme = ReadingTheme.Paper,
    val layout: ReadingLayout = ReadingLayout.Scroll,
    val keepScreenOn: Boolean = true
)

@HiltViewModel
class PdfViewerViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val resourceRepository: ResourceRepository,
    private val downloadManager: ResourceDownloadManager,
    @ApplicationContext context: Context
) : ViewModel() {
    private val resourceId: String = savedStateHandle.get<String>("resourceId").orEmpty()
    private val _uiState = MutableStateFlow(PdfViewerUiState())
    val uiState: StateFlow<PdfViewerUiState> = _uiState.asStateFlow()
    private val prefs = ReaderPrefs(context)
    private var engine: PdfDocumentEngine? = null
    private var resource: ApiResource? = null
    private var downloadJob: Job? = null

    init {
        _uiState.update {
            it.copy(
                bookmarks = prefs.bookmarks(resourceId),
                theme = prefs.theme,
                layout = prefs.layout,
                keepScreenOn = prefs.keepScreenOn
            )
        }
        load()
    }

    fun onPageVisible(page: Int) {
        if (page == _uiState.value.currentPage) return
        _uiState.update { it.copy(currentPage = page) }
        prefs.setLastPage(resourceId, page)
    }

    fun consumeResume() {
        _uiState.update { it.copy(resumePage = null) }
    }

    fun toggleBookmark(page: Int = _uiState.value.currentPage) {
        val next = _uiState.value.bookmarks.let { if (page in it) it - page else it + page }
        prefs.setBookmarks(resourceId, next)
        _uiState.update { it.copy(bookmarks = next) }
    }

    fun setTheme(theme: ReadingTheme) {
        prefs.theme = theme
        _uiState.update { it.copy(theme = theme) }
    }

    fun setLayout(layout: ReadingLayout) {
        prefs.layout = layout
        _uiState.update { it.copy(layout = layout) }
    }

    fun setKeepScreenOn(on: Boolean) {
        prefs.keepScreenOn = on
        _uiState.update { it.copy(keepScreenOn = on) }
    }

    fun cachedPage(index: Int, widthPx: Int): Bitmap? = engine?.cached(index, widthPx)

    suspend fun thumbnail(index: Int): Bitmap? = engine?.thumbnail(index)

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
                engine?.close()
                engine = null
                val opened = PdfDocumentEngine.open(file)
                engine = opened
                val last = prefs.lastPage(resourceId).coerceIn(0, (opened.pageCount - 1).coerceAtLeast(0))
                _uiState.update {
                    it.copy(
                        pageCount = opened.pageCount,
                        pageAspects = opened.pageAspects,
                        currentPage = last,
                        resumePage = last.takeIf { page -> page > 0 },
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

    suspend fun renderPage(index: Int, widthPx: Int): Bitmap? = engine?.render(index, widthPx)

    override fun onCleared() {
        engine?.close()
        engine = null
        super.onCleared()
    }
}
