package com.consica.code.domain.content

import com.consica.code.domain.model.Lesson

/**
 * Aggregated catalog of every lesson in the app, ordered by biome order and
 * then by the lesson's position inside its biome.
 */
object LessonCatalog {

    private val allLessons: List<Lesson> =
        WebLessons.lessons +
            PythonLessons.lessons +
            IntermediateLessons.lessons +
            AdvancedLessons.lessons

    /** Global order: biome order first, then lesson order within the biome. */
    val lessons: List<Lesson> = BiomeCatalog.biomes.flatMap { biome ->
        allLessons.filter { it.biomeId == biome.id }.sortedBy { it.order }
    }

    private val index: Map<String, Lesson> = lessons.associateBy { it.id }

    private val byBiomeIndex: Map<String, List<Lesson>> = lessons.groupBy { it.biomeId }

    fun byId(id: String): Lesson? = index[id]

    fun byBiome(biomeId: String): List<Lesson> =
        byBiomeIndex[biomeId].orEmpty().sortedBy { it.order }
}
