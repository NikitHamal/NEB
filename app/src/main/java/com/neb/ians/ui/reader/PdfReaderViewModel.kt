package com.neb.ians.ui.reader

import android.app.Application
import android.graphics.Bitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.AnnotationRepository
import com.neb.ians.data.ResourceRepository
import com.neb.ians.data.local.AnnotationEntity
import com.neb.ians.data.local.AnnotationKind
import com.neb.ians.data.local.ResourceEntity
import com.neb.ians.pdf.PdfPageCache
import dagger.hilt.android.lifecycle.HiltViewModel
import java.io.File
import javax.inject.Inject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext

enum class ToolMode { None, Highlight, Underline, StickyNote }

data class ReaderState(
    val resource: ResourceEntity? = null,
    val pageCount: Int = 0,
    val ready: Boolean = false,
    val tool: ToolMode = ToolMode.None,
)

@HiltViewModel
class PdfReaderViewModel @Inject constructor(
    app: Application,
    savedStateHandle: SavedStateHandle,
    private val resources: ResourceRepository,
    private val annotations: AnnotationRepository,
    private val cache: PdfPageCache,
) : AndroidViewModel(app) {

    private val resourceId: Long = savedStateHandle["resourceId"] ?: 0L

    private val _state = MutableStateFlow(ReaderState())
    val state: StateFlow<ReaderState> = _state.asStateFlow()

    private val fileMutex = Mutex()
    @Volatile private var file: File? = null

    val annotationsFlow: StateFlow<List<AnnotationEntity>> = annotations.forResource(resourceId)
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    init {
        viewModelScope.launch {
            val r = resources.get(resourceId) ?: return@launch
            _state.value = _state.value.copy(resource = r)
            val ctx = getApplication<Application>()
            val f = withContext(Dispatchers.IO) {
                cache.ensureLocalCopy(ctx, r.sourceUri, r.id)
            }
            fileMutex.withLock { file = f }
            val count = withContext(Dispatchers.IO) { cache.pageCount(f) }
            _state.value = _state.value.copy(pageCount = count, ready = true)
            resources.touch(r.id)
        }
    }

    suspend fun renderPage(page: Int, widthPx: Int): Bitmap? {
        val f = file ?: return null
        return cache.renderPage(f, page, widthPx)
    }

    fun setTool(tool: ToolMode) {
        _state.value = _state.value.copy(tool = if (_state.value.tool == tool) ToolMode.None else tool)
    }

    fun addAnnotation(page: Int, xPct: Float, yPct: Float, wPct: Float, hPct: Float, note: String? = null) {
        val kind = when (_state.value.tool) {
            ToolMode.Highlight -> AnnotationKind.Highlight
            ToolMode.Underline -> AnnotationKind.Underline
            ToolMode.StickyNote -> AnnotationKind.StickyNote
            ToolMode.None -> return
        }
        val color = when (kind) {
            AnnotationKind.Highlight -> 0xFFFFEB3B
            AnnotationKind.Underline -> 0xFFE53935
            AnnotationKind.StickyNote -> 0xFFFFC107
        }
        viewModelScope.launch {
            annotations.add(
                AnnotationEntity(
                    resourceId = resourceId,
                    page = page,
                    kind = kind,
                    xPct = xPct,
                    yPct = yPct,
                    widthPct = wPct,
                    heightPct = hPct,
                    color = color,
                    note = note,
                )
            )
        }
    }

    fun removeAnnotation(id: Long) = viewModelScope.launch { annotations.delete(id) }

    fun updateNote(item: AnnotationEntity, note: String) = viewModelScope.launch {
        annotations.update(item.copy(note = note))
    }
}
