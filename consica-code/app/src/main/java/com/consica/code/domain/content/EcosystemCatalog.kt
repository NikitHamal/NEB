package com.consica.code.domain.content

import com.consica.code.R
import com.consica.code.domain.model.EcosystemItemDef

/**
 * Decorative ecosystem items learners unlock by completing lessons.
 * Together they grow into a living digital ecosystem.
 */
object EcosystemCatalog {

    val items: List<EcosystemItemDef> = listOf(
        EcosystemItemDef(id = "sprout", nameRes = R.string.eco_sprout_name, emoji = "🌱"),
        EcosystemItemDef(id = "fern", nameRes = R.string.eco_fern_name, emoji = "🌿"),
        EcosystemItemDef(id = "mushroom", nameRes = R.string.eco_mushroom_name, emoji = "🍄"),
        EcosystemItemDef(id = "sunflower", nameRes = R.string.eco_sunflower_name, emoji = "🌻"),
        EcosystemItemDef(id = "bee", nameRes = R.string.eco_bee_name, emoji = "🐝"),
        EcosystemItemDef(id = "butterfly", nameRes = R.string.eco_butterfly_name, emoji = "🦋"),
        EcosystemItemDef(id = "river_stone", nameRes = R.string.eco_river_stone_name, emoji = "🪨"),
        EcosystemItemDef(id = "fish", nameRes = R.string.eco_fish_name, emoji = "🐟"),
        EcosystemItemDef(id = "lily", nameRes = R.string.eco_lily_name, emoji = "🪷"),
        EcosystemItemDef(id = "pine", nameRes = R.string.eco_pine_name, emoji = "🌲"),
        EcosystemItemDef(id = "owl_friend", nameRes = R.string.eco_owl_friend_name, emoji = "🦉"),
        EcosystemItemDef(id = "waterfall", nameRes = R.string.eco_waterfall_name, emoji = "💦"),
        EcosystemItemDef(id = "eagle", nameRes = R.string.eco_eagle_name, emoji = "🦅"),
        EcosystemItemDef(id = "snow_lotus", nameRes = R.string.eco_snow_lotus_name, emoji = "❄️"),
        EcosystemItemDef(id = "cloud_lantern", nameRes = R.string.eco_cloud_lantern_name, emoji = "🏮"),
        EcosystemItemDef(id = "rainbow", nameRes = R.string.eco_rainbow_name, emoji = "🌈"),
    )

    private val index: Map<String, EcosystemItemDef> = items.associateBy { it.id }

    fun byId(id: String): EcosystemItemDef? = index[id]
}
