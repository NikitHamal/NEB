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
import com.neb.ians.ui.screens.reader.pdf.ReaderSearch
import com.neb.ians.ui.screens.reader.pdf.SearchHit
import com.neb.ians.util.ResourceDownloadManager
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.cancelAndJoin
import kotlinx.coroutines.delay
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
    val keepScreenOn: Boolean = true,
    /** Whether this device can read the document's text (search). */
    val canReadText: Boolean = false,
    val search: ReaderSearch = ReaderSearch()
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
    private var searchJob: Job? = null
    private var file: File? = null

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
                this@PdfViewerViewModel.file = file
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
                        canReadText = opened.canReadText,
                        error = null
                    )
                }
            }.onFailure {
                _uiState.update { state -> state.copy(isLoading = false, isDownloading = false, error = "Unable to open PDF") }
            }
        }
    }

    suspend fun renderPage(index: Int, widthPx: Int): Bitmap? = engine?.render(index, widthPx)

    suspend fun pageText(index: Int = _uiState.value.currentPage): String? = engine?.pageText(index)

    fun openSearch() {
        _uiState.update { it.copy(search = it.search.copy(open = true)) }
    }

    fun closeSearch() {
        searchJob?.cancel()
        _uiState.update { it.copy(search = ReaderSearch()) }
    }

    /**
     * Searches every page, starting at the one on screen and wrapping round, so the first hit
     * is the nearest one ahead. Hits stream in page by page; the first one is jumped to.
     */
    fun search(query: String) {
        searchJob?.cancel()
        val q = query.trim()
        _uiState.update { it.copy(search = it.search.copy(query = query, running = q.length >= 2, scanned = 0, hits = emptyList(), byPage = emptyMap(), index = -1)) }
        val eng = engine ?: return
        if (q.length < 2) return
        val start = _uiState.value.currentPage
        val n = eng.pageCount
        searchJob = viewModelScope.launch {
            delay(260)
            val hits = ArrayList<SearchHit>()
            val byPage = HashMap<Int, List<android.graphics.RectF>>()
            for (k in 0 until n) {
                val page = (start + k) % n
                val rects = eng.search(page, q)
                if (rects.isNotEmpty()) {
                    byPage[page] = rects
                    rects.sortedWith(compareBy({ it.top }, { it.left })).forEach { hits.add(SearchHit(page, it)) }
                }
                val first = hits.isNotEmpty() && _uiState.value.search.index < 0
                _uiState.update {
                    it.copy(search = it.search.copy(
                        scanned = k + 1, hits = hits.toList(), byPage = HashMap(byPage),
                        index = if (first) 0 else it.search.index,
                        jump = if (first) it.search.jump + 1 else it.search.jump
                    ))
                }
            }
            _uiState.update { it.copy(search = it.search.copy(running = false)) }
        }
    }

    fun stepSearch(delta: Int) {
        _uiState.update {
            val s = it.search
            if (s.hits.isEmpty()) it else it.copy(search = s.copy(index = Math.floorMod(s.index + delta, s.hits.size), jump = s.jump + 1))
        }
    }

    override fun onCleared() {
        engine?.close()
        engine = null
        super.onCleared()
    }
}
