package com.consica.code.ui.rewards

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material.icons.filled.Forest
import androidx.compose.material.icons.filled.Grass
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.MilitaryTech
import androidx.compose.material.icons.filled.Park
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.Terminal
import androidx.compose.material.icons.filled.Workspaces
import androidx.compose.ui.graphics.vector.ImageVector
import com.consica.code.core.model.EcosystemItemType

/** Maps content-layer [com.consica.code.domain.content.BadgeDef.iconKey] strings to Compose icons. */
fun badgeIcon(iconKey: String): ImageVector = when (iconKey) {
    "sprout" -> Icons.Filled.Grass
    "terminal" -> Icons.Filled.Terminal
    "language" -> Icons.Filled.Language
    "code" -> Icons.Filled.Code
    "psychology" -> Icons.Filled.Psychology
    "workspace" -> Icons.Filled.Workspaces
    "streak" -> Icons.Filled.LocalFireDepartment
    "level" -> Icons.Filled.MilitaryTech
    "lessons" -> Icons.Filled.School
    "eco" -> Icons.Filled.Forest
    else -> Icons.Filled.EmojiEvents
}

/** Fallback icon for an ecosystem item (used in compact lists; the biome uses canvas art). */
fun ecosystemIcon(type: EcosystemItemType): ImageVector = when (type) {
    EcosystemItemType.SPROUT -> Icons.Filled.Grass
    EcosystemItemType.FLOWER -> Icons.Filled.Park
    EcosystemItemType.TREE -> Icons.Filled.Forest
    EcosystemItemType.BUTTERFLY -> Icons.Filled.Bolt
    EcosystemItemType.BIRD -> Icons.Filled.Bolt
    EcosystemItemType.WATER -> Icons.Filled.Bolt
    EcosystemItemType.SUN -> Icons.Filled.Bolt
    EcosystemItemType.MUSHROOM -> Icons.Filled.Park
    EcosystemItemType.ROCK -> Icons.Filled.Park
}
