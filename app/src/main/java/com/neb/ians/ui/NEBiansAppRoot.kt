package com.neb.ians.ui

import androidx.compose.animation.AnimatedContentTransitionScope
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChatBubble
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LibraryBooks
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.outlined.ChatBubbleOutline
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.LibraryBooks
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.neb.ians.navigation.Routes
import com.neb.ians.ui.screens.forum.CreatePostScreen
import com.neb.ians.ui.screens.forum.ForumPostScreen
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.forum.ReplyScreen
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.pdfviewer.PdfViewerScreen
import com.neb.ians.ui.screens.profile.ProfileScreen
import com.neb.ians.ui.screens.resources.ResourcesScreen
import com.neb.ians.ui.screens.search.SearchScreen
import com.neb.ians.utils.ThemePreference
import com.neb.ians.utils.ThemeSettings

data class BottomNavItem(
    val route: String,
    val label: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector,
)

val bottomNavItems = listOf(
    BottomNavItem(Routes.HOME, "Home", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem(Routes.RESOURCES, "Resources", Icons.Filled.LibraryBooks, Icons.Outlined.LibraryBooks),
    BottomNavItem(Routes.FORUM, "Forum", Icons.Filled.ChatBubble, Icons.Outlined.ChatBubbleOutline),
    BottomNavItem(Routes.PROFILE, "Profile", Icons.Filled.Person, Icons.Outlined.Person),
)

private val bottomNavRoutes = bottomNavItems.map { it.route }.toSet()

@Composable
fun NEBiansAppRoot(
    themeSettings: ThemeSettings,
    currentTheme: ThemePreference,
) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    val showBottomBar = currentDestination?.route in bottomNavRoutes

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    bottomNavItems.forEach { item ->
                        val selected = currentDestination?.hierarchy?.any {
                            it.route == item.route
                        } == true
                        NavigationBarItem(
                            icon = {
                                Icon(
                                    if (selected) item.selectedIcon else item.unselectedIcon,
                                    contentDescription = item.label,
                                )
                            },
                            label = { Text(item.label) },
                            selected = selected,
                            onClick = {
                                navController.navigate(item.route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                        )
                    }
                }
            }
        },
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Routes.HOME,
            modifier = Modifier.padding(innerPadding),
            enterTransition = {
                fadeIn(animationSpec = tween(200))
            },
            exitTransition = {
                fadeOut(animationSpec = tween(200))
            },
        ) {
            composable(Routes.HOME) {
                HomeScreen(
                    onNavigateToResources = {
                        navController.navigate(Routes.RESOURCES) {
                            popUpTo(navController.graph.findStartDestination().id) {
                                saveState = true
                            }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    onNavigateToSearch = { navController.navigate(Routes.SEARCH) },
                    onNavigateToForum = {
                        navController.navigate(Routes.FORUM) {
                            popUpTo(navController.graph.findStartDestination().id) {
                                saveState = true
                            }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    onOpenResource = { navController.navigate(Routes.pdfViewer(it)) },
                )
            }

            composable(Routes.RESOURCES) {
                ResourcesScreen(
                    onOpenResource = { navController.navigate(Routes.pdfViewer(it)) },
                    onNavigateToSearch = { navController.navigate(Routes.SEARCH) },
                )
            }

            composable(Routes.FORUM) {
                ForumScreen(
                    onOpenPost = { navController.navigate(Routes.forumPost(it)) },
                    onCreatePost = { navController.navigate(Routes.CREATE_POST) },
                )
            }

            composable(Routes.PROFILE) {
                ProfileScreen(
                    themeSettings = themeSettings,
                    currentTheme = currentTheme,
                )
            }

            composable(Routes.SEARCH) {
                SearchScreen(
                    onBack = { navController.popBackStack() },
                    onOpenResource = { navController.navigate(Routes.pdfViewer(it)) },
                )
            }

            composable(
                Routes.PDF_VIEWER,
                arguments = listOf(navArgument("resourceId") { type = NavType.LongType }),
                enterTransition = {
                    slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.Start, tween(300))
                },
                exitTransition = {
                    slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.End, tween(300))
                },
            ) { backStackEntry ->
                val resourceId = backStackEntry.arguments?.getLong("resourceId") ?: 0L
                PdfViewerScreen(
                    resourceId = resourceId,
                    onBack = { navController.popBackStack() },
                )
            }

            composable(
                Routes.FORUM_POST,
                arguments = listOf(navArgument("postId") { type = NavType.LongType }),
                enterTransition = {
                    slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.Start, tween(300))
                },
                exitTransition = {
                    slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.End, tween(300))
                },
            ) { backStackEntry ->
                val postId = backStackEntry.arguments?.getLong("postId") ?: 0L
                ForumPostScreen(
                    postId = postId,
                    onBack = { navController.popBackStack() },
                    onReply = { pId, replyToId ->
                        navController.navigate(Routes.reply(pId, replyToId))
                    },
                )
            }

            composable(
                Routes.CREATE_POST,
                enterTransition = {
                    slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.Up, tween(300))
                },
                exitTransition = {
                    slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.Down, tween(300))
                },
            ) {
                CreatePostScreen(
                    onBack = { navController.popBackStack() },
                    onPostCreated = { navController.popBackStack() },
                )
            }

            composable(
                Routes.REPLY,
                arguments = listOf(
                    navArgument("postId") { type = NavType.LongType },
                    navArgument("replyToId") { type = NavType.LongType },
                ),
                enterTransition = {
                    slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.Up, tween(300))
                },
                exitTransition = {
                    slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.Down, tween(300))
                },
            ) { backStackEntry ->
                val postId = backStackEntry.arguments?.getLong("postId") ?: 0L
                val replyToId = backStackEntry.arguments?.getLong("replyToId") ?: -1L
                ReplyScreen(
                    postId = postId,
                    replyToId = replyToId,
                    onBack = { navController.popBackStack() },
                    onReplySent = { navController.popBackStack() },
                )
            }
        }
    }
}
