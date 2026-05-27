package com.neb.ians.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.neb.ians.ui.forum.ForumScreen
import com.neb.ians.ui.forum.NewThreadScreen
import com.neb.ians.ui.forum.ReplyScreen
import com.neb.ians.ui.forum.ThreadScreen
import com.neb.ians.ui.home.HomeScreen
import com.neb.ians.ui.library.LibraryScreen
import com.neb.ians.ui.reader.PdfReaderScreen
import com.neb.ians.ui.settings.SettingsScreen

@Composable
fun NebRoot() {
    val nav = rememberNavController()
    val backStack by nav.currentBackStackEntryAsState()
    val currentRoute = backStack?.destination?.route
    val showBottomBar = currentRoute in NebTabs.map { it.route }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    NebTabs.forEach { tab ->
                        val selected = backStack?.destination?.hierarchy?.any { it.route == tab.route } == true
                        NavigationBarItem(
                            selected = selected,
                            onClick = {
                                nav.navigate(tab.route) {
                                    popUpTo(nav.graph.findStartDestination().id) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = { TabIcon(if (selected) tab.filled else tab.outlined) },
                            label = { Text(tab.label) },
                            alwaysShowLabel = true,
                        )
                    }
                }
            }
        }
    ) { padding ->
        NavHost(
            navController = nav,
            startDestination = NebRoutes.HOME,
            modifier = Modifier.padding(padding),
        ) {
            composable(NebRoutes.HOME) { HomeScreen(onOpenResource = { nav.navigate(NebRoutes.reader(it)) }) }
            composable(NebRoutes.LIBRARY) { LibraryScreen(onOpenResource = { nav.navigate(NebRoutes.reader(it)) }) }
            composable(NebRoutes.FORUM) {
                ForumScreen(
                    onOpenThread = { nav.navigate(NebRoutes.thread(it)) },
                    onNewThread = { nav.navigate(NebRoutes.NEW_THREAD) },
                )
            }
            composable(NebRoutes.SETTINGS) { SettingsScreen() }

            // Standalone (full-screen) routes — NOT inside the bottom bar
            composable(
                route = NebRoutes.READER,
                arguments = listOf(navArgument("resourceId") { type = NavType.LongType })
            ) { entry ->
                val id = entry.arguments?.getLong("resourceId") ?: return@composable
                PdfReaderScreen(resourceId = id, onBack = { nav.popBackStack() })
            }
            composable(
                route = NebRoutes.THREAD,
                arguments = listOf(navArgument("threadId") { type = NavType.LongType })
            ) { entry ->
                val id = entry.arguments?.getLong("threadId") ?: return@composable
                ThreadScreen(
                    threadId = id,
                    onBack = { nav.popBackStack() },
                    onReply = { nav.navigate(NebRoutes.reply(id)) },
                )
            }
            composable(
                route = NebRoutes.REPLY,
                arguments = listOf(navArgument("threadId") { type = NavType.LongType })
            ) { entry ->
                val id = entry.arguments?.getLong("threadId") ?: return@composable
                ReplyScreen(threadId = id, onBack = { nav.popBackStack() })
            }
            composable(NebRoutes.NEW_THREAD) {
                NewThreadScreen(onBack = { nav.popBackStack() })
            }
        }
    }
}

@Composable
private fun TabIcon(image: ImageVector) {
    androidx.compose.material3.Icon(image, contentDescription = null)
}
