package com.neb.ians.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.neb.ians.ui.screens.forum.ForumAnswerScreen
import com.neb.ians.ui.screens.forum.ForumReplyScreen
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.library.LibraryScreen
import com.neb.ians.ui.screens.pdf.PdfViewerScreen
import com.neb.ians.ui.screens.settings.SettingsScreen

sealed class Screen(val route: String) {
    data object Home : Screen("home")
    data object Library : Screen("library")
    data object PdfViewer : Screen("pdf/{pdfUri}")
    data object Forum : Screen("forum")
    data object ForumAnswer : Screen("forum_answer/{postId}")
    data object ForumReply : Screen("forum_reply/{postId}")
    data object Settings : Screen("settings")
}

fun NavHostController.navigateToPdf(pdfUri: String) {
    navigate("pdf/${android.net.Uri.encode(pdfUri)}")
}

fun NavHostController.navigateToForumAnswer(postId: Long) {
    navigate("forum_answer/$postId")
}

fun NavHostController.navigateToForumReply(postId: Long) {
    navigate("forum_reply/$postId")
}

@Composable
fun NEBiansNavHost(
    modifier: Modifier = Modifier,
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Home.route,
        modifier = modifier
    ) {
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigate = { route -> navController.navigate(route) },
                onOpenPdf = { navController.navigateToPdf(it) }
            )
        }
        composable(Screen.Library.route) {
            LibraryScreen(
                onBack = { navController.popBackStack() },
                onOpenPdf = { navController.navigateToPdf(it) }
            )
        }
        composable(
            route = Screen.PdfViewer.route,
            arguments = listOf(navArgument("pdfUri") { type = NavType.StringType })
        ) { backStackEntry ->
            val pdfUri = backStackEntry.arguments?.getString("pdfUri") ?: ""
            PdfViewerScreen(
                pdfUri = pdfUri,
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.Forum.route) {
            ForumScreen(
                onBack = { navController.popBackStack() },
                onOpenAnswer = { navController.navigateToForumAnswer(it) },
                onOpenReply = { navController.navigateToForumReply(it) }
            )
        }
        composable(
            route = Screen.ForumAnswer.route,
            arguments = listOf(navArgument("postId") { type = NavType.LongType })
        ) { backStackEntry ->
            val postId = backStackEntry.arguments?.getLong("postId") ?: 0L
            ForumAnswerScreen(
                postId = postId,
                onBack = { navController.popBackStack() },
                onOpenReply = { navController.navigateToForumReply(it) }
            )
        }
        composable(
            route = Screen.ForumReply.route,
            arguments = listOf(navArgument("postId") { type = NavType.LongType })
        ) { backStackEntry ->
            val postId = backStackEntry.arguments?.getLong("postId") ?: 0L
            ForumReplyScreen(
                postId = postId,
                onBack = { navController.popBackStack() }
            )
        }
        composable(Screen.Settings.route) {
            SettingsScreen(onBack = { navController.popBackStack() })
        }
    }
}
