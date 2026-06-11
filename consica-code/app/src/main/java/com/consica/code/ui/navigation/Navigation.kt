package com.consica.code.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.consica.code.ui.screens.lesson.TerraNestScreen
import com.consica.code.ui.screens.map.BiomeMapScreen
import com.consica.code.ui.screens.onboarding.OnboardingScreen
import com.consica.code.ui.screens.path.LearningPathScreen
import com.consica.code.ui.screens.playground.PlaygroundScreen
import com.consica.code.ui.screens.puzzle.PuzzleScreen
import com.consica.code.ui.screens.rewards.RewardsScreen
import com.consica.code.ui.screens.settings.SettingsScreen
import com.consica.code.ui.screens.workspace.WorkspaceEditorScreen
import com.consica.code.ui.screens.workspace.WorkspacesScreen

object Routes {
    const val ONBOARDING = "onboarding"
    const val MAP = "map"
    const val LESSON = "lesson/{lessonId}"
    const val PLAYGROUND = "playground/{lessonId}"
    const val FREEPLAY = "freeplay/{language}"
    const val PUZZLE = "puzzle/{lessonId}"
    const val REWARDS = "rewards"
    const val PATHS = "paths"
    const val WORKSPACES = "workspaces"
    const val WORKSPACE_EDITOR = "workspace/{workspaceId}"
    const val SETTINGS = "settings"

    fun lesson(lessonId: String) = "lesson/$lessonId"
    fun playground(lessonId: String) = "playground/$lessonId"
    fun freeplay(language: String) = "freeplay/$language"
    fun puzzle(lessonId: String) = "puzzle/$lessonId"
    fun workspaceEditor(workspaceId: Long) = "workspace/$workspaceId"
}

@Composable
fun CcodeNavHost(
    navController: NavHostController,
    startDestination: String,
) {
    NavHost(navController = navController, startDestination = startDestination) {
        composable(Routes.ONBOARDING) {
            OnboardingScreen(
                onDone = {
                    navController.navigate(Routes.MAP) {
                        popUpTo(Routes.ONBOARDING) { inclusive = true }
                    }
                },
            )
        }
        composable(Routes.MAP) {
            BiomeMapScreen(
                onOpenLesson = { navController.navigate(Routes.lesson(it)) },
                onOpenRewards = { navController.navigate(Routes.REWARDS) },
                onOpenPaths = { navController.navigate(Routes.PATHS) },
                onOpenWorkspaces = { navController.navigate(Routes.WORKSPACES) },
                onOpenSettings = { navController.navigate(Routes.SETTINGS) },
                onOpenFreeplay = { navController.navigate(Routes.freeplay(it)) },
            )
        }
        composable(
            Routes.LESSON,
            arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
        ) {
            TerraNestScreen(
                onStartChallenge = { lessonId ->
                    navController.navigate(Routes.playground(lessonId)) {
                        popUpTo(Routes.MAP)
                    }
                },
                onStartPuzzle = { lessonId ->
                    navController.navigate(Routes.puzzle(lessonId)) {
                        popUpTo(Routes.MAP)
                    }
                },
                onFinished = { navController.popBackStack(Routes.MAP, inclusive = false) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(
            Routes.PLAYGROUND,
            arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
        ) {
            PlaygroundScreen(
                onLessonComplete = { navController.popBackStack(Routes.MAP, inclusive = false) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(
            Routes.FREEPLAY,
            arguments = listOf(navArgument("language") { type = NavType.StringType }),
        ) {
            PlaygroundScreen(
                onLessonComplete = { navController.popBackStack(Routes.MAP, inclusive = false) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(
            Routes.PUZZLE,
            arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
        ) {
            PuzzleScreen(
                onComplete = { navController.popBackStack(Routes.MAP, inclusive = false) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(Routes.REWARDS) {
            RewardsScreen(onBack = { navController.popBackStack() })
        }
        composable(Routes.PATHS) {
            LearningPathScreen(
                onOpenLesson = { navController.navigate(Routes.lesson(it)) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(Routes.WORKSPACES) {
            WorkspacesScreen(
                onOpenWorkspace = { navController.navigate(Routes.workspaceEditor(it)) },
                onBack = { navController.popBackStack() },
            )
        }
        composable(
            Routes.WORKSPACE_EDITOR,
            arguments = listOf(navArgument("workspaceId") { type = NavType.LongType }),
        ) {
            WorkspaceEditorScreen(onBack = { navController.popBackStack() })
        }
        composable(Routes.SETTINGS) {
            SettingsScreen(onBack = { navController.popBackStack() })
        }
    }
}
