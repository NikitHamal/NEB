package com.consica.code.ui.navigation

import androidx.annotation.StringRes
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material.icons.filled.Forest
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Workspaces
import androidx.compose.material.icons.outlined.EmojiEvents
import androidx.compose.material.icons.outlined.Forest
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.Workspaces
import androidx.compose.ui.graphics.vector.ImageVector
import com.consica.code.R

object Routes {
    const val ONBOARDING = "onboarding"
    const val HOME = "home"
    const val REWARDS = "rewards"
    const val WORKSPACES = "workspaces"
    const val SETTINGS = "settings"
    const val LESSON = "lesson/{lessonId}"
    const val PUZZLE = "puzzle/{lessonId}"
    const val PLAYGROUND = "playground?lessonId={lessonId}&workspaceId={workspaceId}"

    fun lesson(lessonId: String) = "lesson/$lessonId"
    fun puzzle(lessonId: String) = "puzzle/$lessonId"
    fun playground(lessonId: String? = null, workspaceId: Long? = null) =
        "playground?lessonId=${lessonId ?: ""}&workspaceId=${workspaceId ?: -1L}"
}

data class BottomNavItem(
    val route: String,
    @StringRes val labelRes: Int,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
)

val bottomNavItems = listOf(
    BottomNavItem(Routes.HOME, R.string.nav_home, Icons.Filled.Forest, Icons.Outlined.Forest),
    BottomNavItem(Routes.WORKSPACES, R.string.nav_workspaces, Icons.Filled.Workspaces, Icons.Outlined.Workspaces),
    BottomNavItem(Routes.REWARDS, R.string.nav_rewards, Icons.Filled.EmojiEvents, Icons.Outlined.EmojiEvents),
    BottomNavItem(Routes.SETTINGS, R.string.nav_settings, Icons.Filled.Settings, Icons.Outlined.Settings),
)
