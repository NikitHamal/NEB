package com.consica.code.ui.screens.path

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.model.LearningPath
import com.consica.code.domain.model.Lesson
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

data class PathSection(
    val path: LearningPath,
    val lessons: List<Lesson>,
    val completedIds: Set<String>,
) {
    val completedCount: Int get() = lessons.count { it.id in completedIds }
    val progressPercent: Int
        get() = if (lessons.isEmpty()) 0 else (completedCount * 100) / lessons.size
}

data class LearningPathUiState(
    val sections: List<PathSection> = emptyList(),
)

@HiltViewModel
class LearningPathViewModel @Inject constructor(
    progressRepository: ProgressRepository,
) : ViewModel() {

    val uiState: StateFlow<LearningPathUiState> =
        progressRepository.allProgress.map { progress ->
            val completedIds = progress.filter { it.completed }.map { it.lessonId }.toSet()
            val sections = LearningPath.entries.map { path ->
                val lessons = LessonCatalog.lessons.filter { it.path == path }
                PathSection(
                    path = path,
                    lessons = lessons,
                    completedIds = completedIds,
                )
            }.filter { it.lessons.isNotEmpty() }
            LearningPathUiState(sections = sections)
        }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), LearningPathUiState())
}
