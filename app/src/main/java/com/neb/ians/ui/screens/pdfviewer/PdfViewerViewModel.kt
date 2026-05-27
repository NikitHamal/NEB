package com.neb.ians.ui.screens.pdfviewer

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.neb.ians.NEBiansApp
import com.neb.ians.data.local.entity.AnnotationEntity
import com.neb.ians.data.local.entity.ResourceEntity
import com.neb.ians.data.repository.AnnotationRepository
import com.neb.ians.data.repository.ResourceRepository
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class PdfViewerViewModel(application: Application) : AndroidViewModel(application) {

    private val db = (application as NEBiansApp).database
    private val resourceRepository = ResourceRepository(db.resourceDao(), db.bookmarkDao())
    private val annotationRepository = AnnotationRepository(db.annotationDao())

    private val _resource = MutableStateFlow<ResourceEntity?>(null)
    val resource: StateFlow<ResourceEntity?> = _resource.asStateFlow()

    private val resourceId = MutableStateFlow(0L)

    @OptIn(ExperimentalCoroutinesApi::class)
    val annotations: StateFlow<List<AnnotationEntity>> = resourceId
        .flatMapLatest { id ->
            if (id > 0) annotationRepository.getAnnotationsForResource(id)
            else flowOf(emptyList())
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    @OptIn(ExperimentalCoroutinesApi::class)
    val isBookmarked: StateFlow<Boolean> = resourceId
        .flatMapLatest { id ->
            if (id > 0) resourceRepository.isBookmarked(id)
            else flowOf(false)
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), false)

    fun loadResource(id: Long) {
        resourceId.value = id
        viewModelScope.launch {
            _resource.value = resourceRepository.getResourceById(id)
        }
    }

    fun addAnnotation(
        page: Int,
        type: String,
        content: String = "",
        startX: Float = 0f,
        startY: Float = 0f,
        endX: Float = 0f,
        endY: Float = 0f,
    ) {
        viewModelScope.launch {
            annotationRepository.insertAnnotation(
                AnnotationEntity(
                    resourceId = resourceId.value,
                    page = page,
                    type = type,
                    content = content,
                    startX = startX,
                    startY = startY,
                    endX = endX,
                    endY = endY,
                )
            )
        }
    }

    fun deleteAnnotation(annotation: AnnotationEntity) {
        viewModelScope.launch {
            annotationRepository.deleteAnnotation(annotation)
        }
    }

    fun toggleBookmark() {
        viewModelScope.launch {
            val currentlyBookmarked = isBookmarked.value
            resourceRepository.toggleBookmark(resourceId.value, currentlyBookmarked)
        }
    }
}
