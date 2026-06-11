package com.consica.code.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountTree
import androidx.compose.material.icons.filled.Code
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.navigation.NavGraphBuilder
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.consica.code.R
import com.consica.code.ui.screens.EcosystemScreen
import com.consica.code.ui.screens.HomeScreen
import com.consica.code.ui.screens.LessonScreen
import com.consica.code.ui.screens.PathScreen
import com.consica.code.ui.screens.PlaygroundScreen
import com.consica.code.ui.screens.RewardsScreen
import com.consica.code.ui.screens.SettingsScreen
import com.consica.code.ui.screens.StreakScreen

/** All navigation routes in one place. */
object Routes {
    const val HOME = "home"
    const val PATH = "path"
    const val PLAYGROUND = "playground"
    const val REWARDS = "rewards"
    const val SETTINGS = "settings"

    const val LESSON = "lesson/{lessonId}"
    fun lesson(lessonId: String) = "lesson/$lessonId"

    const val ECOSYSTEM = "ecosystem"
    const val STREAK = "streak"
}

private data class TabItem(val route: String, val labelRes: Int, val icon: ImageVector)

private val tabs = listOf(
    TabItem(Routes.HOME, R.string.nav_home, Icons.Filled.Home),
    TabItem(Routes.PATH, R.string.nav_path, Icons.Filled.AccountTree),
    TabItem(Routes.PLAYGROUND, R.string.nav_playground, Icons.Filled.Code),
    TabItem(Routes.REWARDS, R.string.nav_rewards, Icons.Filled.EmojiEvents),
    TabItem(Routes.SETTINGS, R.string.nav_settings, Icons.Filled.Settings),
)

/** Root: routes between onboarding and the main shell based on persisted prefs. */
@Composable
fun ConsicaRoot(viewModel: AppViewModel) {
    val prefs by viewModel.prefs.collectAsState()
    if (!prefs.onboardingComplete) {
        com.consica.code.ui.onboarding.OnboardingScreen(onFinish = viewModel::completeOnboarding)
    } else {
        MainShell(viewModel)
    }
}

@Composable
private fun MainShell(viewModel: AppViewModel) {
    val navController = rememberNavController()
    val backStack by navController.currentBackStackEntryAsState()
    val currentRoute = backStack?.destination?.route
    val showBottomBar = currentRoute in tabs.map { it.route }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    tabs.forEach { tab ->
                        NavigationBarItem(
                            selected = currentRoute == tab.route,
                            onClick = {
                                if (currentRoute != tab.route) {
                                    navController.navigate(tab.route) {
                                        popUpTo(Routes.HOME) { saveState = true }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            },
                            icon = { Icon(tab.icon, contentDescription = null) },
                            label = { Text(stringResource(tab.labelRes)) },
                        )
                    }
                }
            }
        },
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = Routes.HOME,
            modifier = Modifier.padding(padding),
        ) {
            mainGraph(navController, viewModel)
        }
    }
}

private fun NavGraphBuilder.mainGraph(navController: NavHostController, viewModel: AppViewModel) {
    composable(Routes.HOME) {
        HomeScreen(
            viewModel = viewModel,
            onOpenLesson = { navController.navigate(Routes.lesson(it)) },
            onOpenEcosystem = { navController.navigate(Routes.ECOSYSTEM) },
            onOpenStreak = { navController.navigate(Routes.STREAK) },
            onOpenPath = { navController.navigate(Routes.PATH) },
        )
    }
    composable(Routes.PATH) {
        PathScreen(
            viewModel = viewModel,
            onOpenLesson = { navController.navigate(Routes.lesson(it)) },
        )
    }
    composable(Routes.PLAYGROUND) {
        PlaygroundScreen(viewModel = viewModel, lessonId = null, onBack = null)
    }
    composable(Routes.REWARDS) {
        RewardsScreen(viewModel = viewModel, onOpenStreak = { navController.navigate(Routes.STREAK) })
    }
    composable(Routes.SETTINGS) {
        SettingsScreen(viewModel = viewModel)
    }
    composable(
        route = Routes.LESSON,
        arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
    ) { entry ->
        val lessonId = entry.arguments?.getString("lessonId").orEmpty()
        LessonScreen(
            viewModel = viewModel,
            lessonId = lessonId,
            onBack = { navController.popBackStack() },
            onOpenLesson = { id ->
                navController.navigate(Routes.lesson(id)) {
                    popUpTo(Routes.LESSON) { inclusive = true }
                }
            },
        )
    }
    composable(Routes.ECOSYSTEM) {
        EcosystemScreen(viewModel = viewModel, onBack = { navController.popBackStack() })
    }
    composable(Routes.STREAK) {
        StreakScreen(viewModel = viewModel, onBack = { navController.popBackStack() })
    }
}
