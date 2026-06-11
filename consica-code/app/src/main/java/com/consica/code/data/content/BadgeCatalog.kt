package com.consica.code.data.content

import com.consica.code.R
import com.consica.code.core.model.BadgeDef

object BadgeCatalog {

    const val FIRST_SPROUT = "first_sprout"
    const val WEB_GARDENER = "web_gardener"
    const val FIRST_PRINT = "first_print"
    const val BLOCK_WIZARD = "block_wizard"
    const val BUG_CATCHER = "bug_catcher"
    const val RIVER_BUILDER = "river_builder"
    const val CANOPY_MASTER = "canopy_master"
    const val STREAK_3 = "streak_3"
    const val STREAK_7 = "streak_7"
    const val STREAK_30 = "streak_30"
    const val PRO_CODER = "pro_coder"

    val all: List<BadgeDef> = listOf(
        BadgeDef(FIRST_SPROUT, R.string.badge_first_sprout, R.string.badge_first_sprout_desc, "🌱"),
        BadgeDef(FIRST_PRINT, R.string.badge_first_print, R.string.badge_first_print_desc, "🐍"),
        BadgeDef(BLOCK_WIZARD, R.string.badge_block_wizard, R.string.badge_block_wizard_desc, "🧩"),
        BadgeDef(WEB_GARDENER, R.string.badge_web_gardener, R.string.badge_web_gardener_desc, "🌿"),
        BadgeDef(BUG_CATCHER, R.string.badge_bug_catcher, R.string.badge_bug_catcher_desc, "🐞"),
        BadgeDef(RIVER_BUILDER, R.string.badge_river_builder, R.string.badge_river_builder_desc, "🌊"),
        BadgeDef(CANOPY_MASTER, R.string.badge_canopy_master, R.string.badge_canopy_master_desc, "🏆", professional = true),
        BadgeDef(STREAK_3, R.string.badge_streak_3, R.string.badge_streak_3_desc, "☀️"),
        BadgeDef(STREAK_7, R.string.badge_streak_7, R.string.badge_streak_7_desc, "🌳"),
        BadgeDef(STREAK_30, R.string.badge_streak_30, R.string.badge_streak_30_desc, "🌲"),
        BadgeDef(PRO_CODER, R.string.badge_pro_coder, R.string.badge_pro_coder_desc, "💼", professional = true),
    )

    fun byId(id: String): BadgeDef? = all.firstOrNull { it.id == id }
}
