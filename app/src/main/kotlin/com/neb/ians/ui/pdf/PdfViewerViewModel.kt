package com.neb.ians.ui.pdf

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.data.db.AnnotationEntity
import com.neb.ians.data.repo.ResourceRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class PdfViewerViewModel @Inject constructor(
    private val repo: ResourceRepository,
) : ViewModel() {

    private val resourceIdFlow = MutableStateFlow<String?>(null)

    @OptIn(kotlinx.coroutines.ExperimentalCoroutinesApi::class)
    val annotations: StateFlow<List<AnnotationEntity>> =
        resourceIdFlow
            .flatMapLatest { id -> if (id == null) kotlinx.coroutines.flow.flowOf(emptyList()) else repo.annotations(id) }
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun load(id: String) {
        if (resourceIdFlow.value == id) return
        resourceIdFlow.value = id
    }

    fun addRectAnnotation(resourceId: String, page: Int, rect: Rect, kind: String) {
        val color = when (kind) {
            "HIGHLIGHT" -> 0xFFFFEB3B.toInt()
            "UNDERLINE" -> 0xFF3F5AA6.toInt()
            else -> 0xFF000000.toInt()
        }
        val rects = listOf(StoredRect(rect.left, rect.top, rect.right, rect.bottom))
        viewModelScope.launch {
            repo.saveAnnotation(
                AnnotationEntity(
                    resourceId = resourceId,
                    page = page,
                    kind = kind,
                    text = null,
                    rectsJson = storedRectsJson(rects),
                    color = color,
                )
            )
        }
    }

    fun addNote(resourceId: String, page: Int, point: Offset, text: String) {
        val rects = listOf(StoredRect(point.x, point.y, point.x + 0.02f, point.y + 0.02f))
        viewModelScope.launch {
            repo.saveAnnotation(
                AnnotationEntity(
                    resourceId = resourceId,
                    page = page,
                    kind = "NOTE",
                    text = text,
                    rectsJson = storedRectsJson(rects),
                    color = 0xFFFFA000.toInt(),
                )
            )
        }
    }
}
