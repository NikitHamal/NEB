package com.consica.code.ui.screens.map

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.consica.code.data.local.entity.LessonProgressEntity
import com.consica.code.data.prefs.AppSettings
import com.consica.code.data.prefs.UserPreferencesRepository
import com.consica.code.data.repository.ProgressRepository
import com.consica.code.domain.content.BiomeCatalog
import com.consica.code.domain.content.LessonCatalog
import com.consica.code.domain.model.AgeGroup
import com.consica.code.domain.model.Biome
import com.consica.code.domain.model.Lesson
import com.consica.code.domain.model.PlayerStats
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

data class LessonNode(
    val lesson: Lesson,
    val completed: Boolean,
    val unlocked: Boolean,
)

data class BiomeSection(
    val biome: Biome,
    val unlocked: Boolean,
    val lessons: List<LessonNode>,
) {
    val completedCount: Int get() = lessons.count { it.completed }
}

data class MapUiState(
    val loading: Boolean = true,
    val stats: PlayerStats = PlayerStats(),
    val ageGroup: AgeGroup = AgeGroup.KIDS,
    val settings: AppSettings = AppSettings(),
    val biomes: List<BiomeSection> = emptyList(),
    val nextLesson: Lesson? = null,
)

@HiltViewModel
class BiomeMapViewModel @Inject constructor(
    prefs: UserPreferencesRepository,
    progressRepository: ProgressRepository,
) : ViewModel() {

    val uiState: StateFlow<MapUiState> = combine(
        prefs.stats,
        prefs.profile,
        prefs.settings,
        progressRepository.allProgress,
    ) { stats, profile, settings, progress ->
        val sections = buildSections(progress)
        MapUiState(
            loading = false,
            stats = stats,
            ageGroup = profile.ageGroup,
            settings = settings,
            biomes = sections,
            nextLesson = sections.asSequence()
                .filter { it.unlocked }
                .flatMap { it.lessons }
                .firstOrNull { it.unlocked && !it.completed }
                ?.lesson,
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), MapUiState())

    private fun buildSections(progress: List<LessonProgressEntity>): List<BiomeSection> {
        val completedIds = progress.filter { it.completed }.map { it.lessonId }.toSet()
        val sections = mutableListOf<BiomeSection>()
        var previousBiomeUnlockedEnough = true
        for (biome in BiomeCatalog.biomes) {
            val lessons = LessonCatalog.byBiome(biome.id)
            val biomeUnlocked = previousBiomeUnlockedEnough
            var previousCompleted = true
            val nodes = lessons.map { lesson ->
                val completed = lesson.id in completedIds
                val unlocked = biomeUnlocked && previousCompleted
                previousCompleted = completed
                LessonNode(lesson = lesson, completed = completed, unlocked = unlocked)
            }
            sections += BiomeSection(biome = biome, unlocked = biomeUnlocked, lessons = nodes)
            val completedInBiome = nodes.count { it.completed }
            previousBiomeUnlockedEnough =
                lessons.isEmpty() || completedInBiome.toFloat() / lessons.size >= 0.6f
        }
        return sections
    }
}
