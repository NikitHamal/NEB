package com.neb.ians

import android.net.Uri
import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

object Routes {
    const val Home = "home"
    const val Library = "library"
    const val Forum = "forum"
    const val Announcements = "announcements"
    const val Settings = "settings"
    const val PdfPattern = "pdf/{resourceId}"
    const val ThreadPattern = "forum/thread/{threadId}"
    const val ReplyPattern = "forum/thread/{threadId}/reply"

    fun pdf(resourceId: String) = "pdf/${Uri.encode(resourceId)}"
    fun thread(threadId: String) = "forum/thread/${Uri.encode(threadId)}"
    fun reply(threadId: String) = "forum/thread/${Uri.encode(threadId)}/reply"
}

@Composable
fun NEBiansApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Routes.Home) {
        composable(Routes.Home) {
            HomeScreen(
                onOpenLibrary = { navController.navigate(Routes.Library) },
                onOpenForum = { navController.navigate(Routes.Forum) },
                onOpenAnnouncements = { navController.navigate(Routes.Announcements) },
                onOpenSettings = { navController.navigate(Routes.Settings) },
                onOpenPdf = { navController.navigate(Routes.pdf(it.id)) }
            )
        }
        composable(Routes.Library) {
            LibraryScreen(
                onBack = { navController.popBackStack() },
                onOpenPdf = { navController.navigate(Routes.pdf(it.id)) }
            )
        }
        composable(
            route = Routes.PdfPattern,
            arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
        ) { entry ->
            val resourceId = entry.arguments?.getString("resourceId").orEmpty()
            val resource = SampleCatalog.resources.firstOrNull { it.id == resourceId }
            if (resource == null) {
                MissingScreen(title = "Resource unavailable", onBack = { navController.popBackStack() })
            } else {
                PdfViewerScreen(resource = resource, onBack = { navController.popBackStack() })
            }
        }
        composable(Routes.Forum) {
            ForumScreen(
                onBack = { navController.popBackStack() },
                onOpenThread = { navController.navigate(Routes.thread(it.id)) }
            )
        }
        composable(
            route = Routes.ThreadPattern,
            arguments = listOf(navArgument("threadId") { type = NavType.StringType })
        ) { entry ->
            val threadId = entry.arguments?.getString("threadId").orEmpty()
            ThreadAnswerScreen(
                threadId = threadId,
                onBack = { navController.popBackStack() },
                onReply = { navController.navigate(Routes.reply(threadId)) }
            )
        }
        composable(
            route = Routes.ReplyPattern,
            arguments = listOf(navArgument("threadId") { type = NavType.StringType })
        ) { entry ->
            val threadId = entry.arguments?.getString("threadId").orEmpty()
            ReplyComposerScreen(
                threadId = threadId,
                onBack = { navController.popBackStack() },
                onSent = {
                    navController.popBackStack()
                }
            )
        }
        composable(Routes.Announcements) {
            AnnouncementsScreen(onBack = { navController.popBackStack() })
        }
        composable(Routes.Settings) {
            SettingsScreen(onBack = { navController.popBackStack() })
        }
    }
}
