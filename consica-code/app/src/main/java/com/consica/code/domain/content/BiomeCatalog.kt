package com.consica.code.domain.content

import com.consica.code.R
import com.consica.code.domain.model.Biome
import com.consica.code.domain.model.LearningPath

/**
 * Static catalog of the six learning biomes that make up the Consica Code world map.
 * Biomes are ordered from the forest floor (absolute beginner) up to the sky canopy
 * (advanced capstone work).
 */
object BiomeCatalog {

    val biomes: List<Biome> = listOf(
        Biome(
            id = "forest_floor",
            nameRes = R.string.biome_forest_floor_name,
            taglineRes = R.string.biome_forest_floor_tagline,
            emoji = "🌱",
            order = 1,
            path = LearningPath.BEGINNER_WEB,
            colorHex = 0xFF2D5A27,
        ),
        Biome(
            id = "sunny_meadow",
            nameRes = R.string.biome_sunny_meadow_name,
            taglineRes = R.string.biome_sunny_meadow_tagline,
            emoji = "🌻",
            order = 2,
            path = LearningPath.BEGINNER_PYTHON,
            colorHex = 0xFFFFD54F,
        ),
        Biome(
            id = "river_delta",
            nameRes = R.string.biome_river_delta_name,
            taglineRes = R.string.biome_river_delta_tagline,
            emoji = "🌊",
            order = 3,
            path = LearningPath.INTERMEDIATE,
            colorHex = 0xFF4DA8DA,
        ),
        Biome(
            id = "deep_grove",
            nameRes = R.string.biome_deep_grove_name,
            taglineRes = R.string.biome_deep_grove_tagline,
            emoji = "🌳",
            order = 4,
            path = LearningPath.INTERMEDIATE,
            colorHex = 0xFF1B5E20,
        ),
        Biome(
            id = "mountain_peaks",
            nameRes = R.string.biome_mountain_peaks_name,
            taglineRes = R.string.biome_mountain_peaks_tagline,
            emoji = "🏔️",
            order = 5,
            path = LearningPath.ADVANCED,
            colorHex = 0xFF8D99AE,
        ),
        Biome(
            id = "sky_canopy",
            nameRes = R.string.biome_sky_canopy_name,
            taglineRes = R.string.biome_sky_canopy_tagline,
            emoji = "☁️",
            order = 6,
            path = LearningPath.ADVANCED,
            colorHex = 0xFF7E57C2,
        ),
    ).sortedBy { it.order }

    private val index: Map<String, Biome> = biomes.associateBy { it.id }

    fun byId(id: String): Biome? = index[id]
}
