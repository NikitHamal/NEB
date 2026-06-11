package com.consica.code

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.consica.code.core.designsystem.ConsicaCodeTheme
import com.consica.code.core.model.ThemeIntensity
import com.consica.code.data.prefs.UserState
import com.consica.code.ui.common.SkeletonBlock
import com.consica.code.ui.navigation.Routes
import com.consica.code.ui.navigation.bottomNavItems
import com.consica.code.ui.screens.home.BiomeMapScreen
import com.consica.code.ui.screens.lesson.TerraNestScreen
import com.consica.code.ui.screens.onboarding.OnboardingScreen
import com.consica.code.ui.screens.playground.PlaygroundScreen
import com.consica.code.ui.screens.puzzle.PuzzleScreen
import com.consica.code.ui.screens.rewards.RewardsScreen
import com.consica.code.ui.screens.settings.SettingsScreen
import com.consica.code.ui.screens.workspaces.WorkspacesScreen
import java.time.LocalDate

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val container = (application as CcodeApp).container

        setContent {
            val userState by container.prefs.userState.collectAsState(initial = null)
            val state = userState

            // Record today's activity for the streak system once per launch.
            LaunchedEffect(Unit) {
                val newStreak = container.prefs.recordDailyActivity(LocalDate.now().toEpochDay())
                if (newStreak != null) {
                    container.learning.checkStreakBadges(newStreak)
                }
            }

            if (state == null) {
                // Quick skeleton while DataStore loads (a frame or two).
                ConsicaCodeTheme {
                    Surface(modifier = Modifier.fillMaxSize()) {
                        SkeletonBlock(modifier = Modifier.fillMaxSize().padding(32.dp))
                    }
                }
            } else {
                container.sound.enabled = state.soundEnabled
                ConsicaCodeTheme(
                    darkTheme = state.darkMode,
                    highContrast = state.highContrast,
                    reducedMotion = state.reducedMotion || state.themeIntensity == ThemeIntensity.FOCUSED,
                    soundEnabled = state.soundEnabled,
                ) {
                    CcodeAppUi(state)
                }
            }
        }
    }
}

@Composable
private fun CcodeAppUi(userState: UserState) {
    val navController = rememberNavController()
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = backStackEntry?.destination?.route

    val showBottomBar = currentRoute in bottomNavItems.map { it.route }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        bottomBar = {
            if (showBottomBar) {
                NavigationBar(containerColor = MaterialTheme.colorScheme.surface) {
                    bottomNavItems.forEach { item ->
                        val selected = currentRoute == item.route
                        NavigationBarItem(
                            selected = selected,
                            onClick = { navController.navigateToTab(item.route) },
                            icon = {
                                Icon(
                                    imageVector = if (selected) item.selectedIcon else item.unselectedIcon,
                                    contentDescription = stringResource(item.labelRes),
                                )
                            },
                            label = {
                                Text(
                                    stringResource(item.labelRes),
                                    style = MaterialTheme.typography.labelSmall,
                                    maxLines = 1,
                                )
                            },
                        )
                    }
                }
            }
        },
    ) { padding ->
        NavHost(
            navController = navController,
            startDestination = if (userState.onboardingDone) Routes.HOME else Routes.ONBOARDING,
            modifier = Modifier.padding(padding),
        ) {
            composable(Routes.ONBOARDING) {
                OnboardingScreen(
                    onFinished = {
                        navController.navigate(Routes.HOME) {
                            popUpTo(Routes.ONBOARDING) { inclusive = true }
                        }
                    },
                )
            }
            composable(Routes.HOME) {
                BiomeMapScreen(
                    onOpenLesson = { lessonId, isPuzzle ->
                        if (isPuzzle) navController.navigate(Routes.puzzle(lessonId))
                        else navController.navigate(Routes.lesson(lessonId))
                    },
                    onOpenPlayground = { navController.navigate(Routes.playground()) },
                    onOpenWorkspace = { id -> navController.navigate(Routes.playground(workspaceId = id)) },
                    onOpenSettings = { navController.navigateToTab(Routes.SETTINGS) },
                )
            }
            composable(Routes.REWARDS) { RewardsScreen() }
            composable(Routes.WORKSPACES) {
                WorkspacesScreen(
                    onOpenWorkspace = { id -> navController.navigate(Routes.playground(workspaceId = id)) },
                )
            }
            composable(Routes.SETTINGS) { SettingsScreen() }

            composable(
                route = Routes.LESSON,
                arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
            ) { entry ->
                val lessonId = entry.arguments?.getString("lessonId") ?: return@composable
                TerraNestScreen(
                    lessonId = lessonId,
                    onStartCoding = { navController.navigate(Routes.playground(lessonId = lessonId)) },
                    onStartPuzzle = { navController.navigate(Routes.puzzle(lessonId)) },
                    onBack = { navController.popBackStack() },
                    onLessonComplete = { navController.popBackStack(Routes.HOME, inclusive = false) },
                    onNextLesson = { nextId, isPuzzle ->
                        navController.popBackStack(Routes.HOME, inclusive = false)
                        if (isPuzzle) navController.navigate(Routes.puzzle(nextId))
                        else navController.navigate(Routes.lesson(nextId))
                    },
                )
            }

            composable(
                route = Routes.PUZZLE,
                arguments = listOf(navArgument("lessonId") { type = NavType.StringType }),
            ) { entry ->
                val lessonId = entry.arguments?.getString("lessonId") ?: return@composable
                PuzzleScreen(
                    lessonId = lessonId,
                    onBack = { navController.popBackStack() },
                    onComplete = { navController.popBackStack(Routes.HOME, inclusive = false) },
                )
            }

            composable(
                route = Routes.PLAYGROUND,
                arguments = listOf(
                    navArgument("lessonId") {
                        type = NavType.StringType
                        defaultValue = ""
                    },
                    navArgument("workspaceId") {
                        type = NavType.LongType
                        defaultValue = -1L
                    },
                ),
            ) { entry ->
                val lessonId = entry.arguments?.getString("lessonId").orEmpty().ifEmpty { null }
                val workspaceId = (entry.arguments?.getLong("workspaceId") ?: -1L).takeIf { it >= 0 }
                PlaygroundScreen(
                    lessonId = lessonId,
                    workspaceId = workspaceId,
                    onBack = { navController.popBackStack() },
                    onLessonComplete = { navController.popBackStack(Routes.HOME, inclusive = false) },
                )
            }
        }
    }
}

private fun NavHostController.navigateToTab(route: String) {
    navigate(route) {
        popUpTo(graph.findStartDestination().id) { saveState = true }
        launchSingleTop = true
        restoreState = true
    }
}
