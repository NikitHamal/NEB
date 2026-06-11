package com.consica.code.core.model

/** Visual elements the user can grow in their biome by completing tasks. */
enum class EcosystemItemType(val id: String) {
    SPROUT("sprout"),
    FLOWER("flower"),
    TREE("tree"),
    BUTTERFLY("butterfly"),
    BIRD("bird"),
    WATER("water"),
    SUN("sun"),
    MUSHROOM("mushroom"),
    ROCK("rock");

    companion object {
        fun from(id: String?): EcosystemItemType = entries.firstOrNull { it.id == id } ?: SPROUT
    }
}
