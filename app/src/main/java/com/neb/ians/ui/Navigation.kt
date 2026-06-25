package com.neb.ians.ui

import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.outlined.Newspaper
import androidx.compose.material.icons.outlined.FactCheck
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import androidx.compose.ui.window.PopupProperties
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Icon
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.ExitToApp
import com.neb.ians.ui.components.NebAvatar
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import com.neb.ians.util.DeepLinkBus
import kotlinx.coroutines.launch
import com.neb.ians.ui.components.LiquidGlassBottomNav
import com.neb.ians.ui.components.NebNavItem
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.library.LibraryScreen
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.forum.ForumPostDetailScreen
import com.neb.ians.ui.screens.forum.CreatePostScreen
import com.neb.ians.ui.screens.forum.ReplyScreen
import com.neb.ians.ui.screens.search.SearchScreen
import com.neb.ians.ui.screens.profile.ProfileScreen
import com.neb.ians.ui.screens.profile.EditProfileScreen
import com.neb.ians.ui.screens.notifications.NotificationsScreen
import com.neb.ians.ui.screens.settings.SettingsScreen
import com.neb.ians.ui.screens.settings.SettingsViewModel
import com.neb.ians.ui.screens.reader.PdfViewerScreen
import com.neb.ians.ui.screens.resource.ResourceDetailScreen
import com.neb.ians.ui.screens.analytics.AnalyticsScreen
import com.neb.ians.ui.screens.bookmarks.BookmarksScreen
import com.neb.ians.ui.screens.upload.UploadScreen
import com.neb.ians.ui.screens.ai.NebyAiScreen
import com.neb.ians.ui.screens.study.StudyLabScreen
import com.neb.ians.ui.screens.study.StudySpaceScreen
import com.neb.ians.ui.screens.interactive.InteractiveCourseScreen
import com.neb.ians.ui.screens.interactive.InteractiveLessonScreen
import com.neb.ians.ui.screens.auth.SplashScreen
import com.neb.ians.ui.screens.auth.LoginScreen
import com.neb.ians.ui.screens.auth.EmailSignupScreen
import com.neb.ians.ui.screens.auth.EmailLoginScreen
import com.neb.ians.ui.screens.auth.EmailVerificationScreen
import com.neb.ians.ui.screens.auth.ForgotPasswordScreen
import com.neb.ians.ui.screens.auth.CompleteProfileScreen
import com.neb.ians.ui.screens.results.ResultCheckerScreen
import com.neb.ians.ui.screens.news.NewsDetailScreen
import com.neb.ians.ui.screens.news.NewsScreen

sealed class Screen(val route: String) {
    data object Splash : Screen("splash")
    data object Login : Screen("login")
    data object EmailSignup : Screen("email_signup")
    data object EmailLogin : Screen("email_login")
    data object EmailVerification : Screen("email_verification/{email}") {
        fun createRoute(email: String) = "email_verification/${if (email.isBlank()) "none" else java.net.URLEncoder.encode(email, "UTF-8")}"
    }
    data object ForgotPassword : Screen("forgot_password/{email}") {
        fun createRoute(email: String) = "forgot_password/${if (email.isBlank()) "none" else java.net.URLEncoder.encode(email, "UTF-8")}"
    }
    data object CompleteProfile : Screen("complete_profile")
    data object Home : Screen("home")
    data object Library : Screen("library?subject={subject}") {
        fun createRoute(subject: String? = null) = if (subject != null) "library?subject=$subject" else "library"
    }
    data object Forum : Screen("forum")
    data object News : Screen("news")
    data object NewsDetail : Screen("news/{slug}") {
        fun createRoute(slug: String) = "news/${java.net.URLEncoder.encode(slug, "UTF-8")}"
    }
    data object ResultChecker : Screen("results/check")
    data object Search : Screen("search")
    data object Notifications : Screen("notifications")
    data object StudyLab : Screen("study_lab")
    data object StudySpace : Screen("study_space/{spaceId}") {
        fun createRoute(spaceId: String) = "study_space/$spaceId"
    }
    data object InteractiveCourse : Screen("interactive/course/{courseSlug}") {
        fun createRoute(courseSlug: String) = "interactive/course/$courseSlug"
    }
    data object InteractiveLesson : Screen("interactive/lesson/{courseSlug}/{lessonSlug}") {
        fun createRoute(courseSlug: String, lessonSlug: String) = "interactive/lesson/$courseSlug/$lessonSlug"
    }
    data object NebyAi : Screen("neby_ai")
    data object Analytics : Screen("analytics")
    data object Bookmarks : Screen("bookmarks")
    data object Upload : Screen("upload")
    data object Profile : Screen("profile/{username}") {
        fun createRoute(username: String) = "profile/${java.net.URLEncoder.encode(username, "UTF-8")}"
    }
    data object EditProfile : Screen("profile/edit")
    data object Settings : Screen("settings")
    data object DeleteAccount : Screen("delete_account")
    data object PdfViewer : Screen("pdf/{resourceId}") {
        fun createRoute(resourceId: String) = "pdf/$resourceId"
    }
    data object ResourceDetail : Screen("resource/{resourceId}") {
        fun createRoute(resourceId: String) = "resource/$resourceId"
    }
    data object ForumPostDetail : Screen("forum/post/{postId}") {
        fun createRoute(postId: String) = "forum/post/$postId"
    }
    data object CreatePost : Screen("forum/create")
    data object Reply : Screen("forum/reply/{postId}/{replyToId}") {
        fun createRoute(postId: String, replyToId: String? = null) = "forum/reply/$postId/${replyToId ?: "none"}"
    }
}

val glassNavItems = listOf(
    NebNavItem(
        route = Screen.Home.route,
        label = "Home",
        selectedIcon = Icons.Filled.Home,
        unselectedIcon = Icons.Outlined.Home,
    ),
    NebNavItem(
        route = "library",
        label = "Library",
        selectedIcon = Icons.AutoMirrored.Filled.MenuBook,
        unselectedIcon = Icons.AutoMirrored.Outlined.MenuBook,
    ),
    NebNavItem(
        route = Screen.Forum.route,
        label = "Forum",
        selectedIcon = Icons.Filled.Forum,
        unselectedIcon = Icons.Outlined.Forum,
    ),
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NEBiansNavHost(
    settingsViewModel: SettingsViewModel,
    navController: NavHostController = rememberNavController(),
    authRepository: AuthRepository
) {
    val authState by settingsViewModel.authState.collectAsStateWithLifecycle()
    val userProfile by settingsViewModel.userProfile.collectAsStateWithLifecycle()
    val isAuthenticated = authState is AuthState.Authenticated
    LaunchedEffect(authState) {
        val state = authState
        when (state) {
            is AuthState.Unauthenticated -> {
                navController.navigate(Screen.Login.route) {
                    popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                }
            }
            is AuthState.Authenticated -> {
                val currentRoute = navController.currentBackStackEntry?.destination?.route
                if (currentRoute == Screen.Login.route || currentRoute == Screen.EmailLogin.route) {
                    val dest = if (state.isProfileComplete) Screen.Home.route else Screen.CompleteProfile.route
                    navController.navigate(dest) {
                        popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                    }
                }
            }
            else -> {}
        }
    }

    val deepLinkScope = rememberCoroutineScope()
    val pendingDeepLink by DeepLinkBus.pendingDeepLink.collectAsState()
    LaunchedEffect(pendingDeepLink, isAuthenticated) {
        if (!isAuthenticated) return@LaunchedEffect
        val deepLink = pendingDeepLink ?: return@LaunchedEffect
        DeepLinkBus.clear()
        val route = deepLink.route ?: return@LaunchedEffect

        navController.navigate(route) {
            launchSingleTop = true
        }

        if (!deepLink.notificationId.isNullOrBlank()) {
            deepLinkScope.launch {
                try {
                    authRepository.markNotificationRead(deepLink.notificationId)
                } catch (_: Exception) {}
            }
        }
    }

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    val currentRoute = currentDestination?.route?.substringBefore("?")
    val showBottomBar = currentRoute in glassNavItems.map { it.route }
    var showProfileDropdown by remember { mutableStateOf(false) }
    val navigateToOwnProfile = {
        val username = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
        if (username != null) {
            showProfileDropdown = !showProfileDropdown
        } else {
            navController.navigate(Screen.Settings.route)
        }
    }

    Box(modifier = Modifier.fillMaxSize()) {
        NavHost(
            navController = navController,
            startDestination = Screen.Splash.route,
            modifier = Modifier.fillMaxSize(),
            enterTransition = { fadeIn(animationSpec = tween(220)) + slideInHorizontally(initialOffsetX = { it / 4 }) },
            exitTransition = { fadeOut(animationSpec = tween(90)) },
        ) {
            composable(Screen.Splash.route) {
                SplashScreen(
                    authRepository = authRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                    },
                    onNavigateToLogin = {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                    }
                )
            }
            composable(Screen.Login.route) {
                LoginScreen(
                    authRepository = authRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Login.route) { inclusive = true }
                        }
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.Login.route) { inclusive = true }
                        }
                    },
                    onNavigateToEmailSignup = { navController.navigate(Screen.EmailSignup.route) },
                    onNavigateToForgotPassword = { email ->
                        navController.navigate(Screen.ForgotPassword.createRoute(email))
                    },
                    onNavigateToVerification = { email ->
                        navController.navigate(Screen.EmailVerification.createRoute(email))
                    }
                )
            }
            composable(Screen.EmailSignup.route) {
                EmailSignupScreen(
                    authRepository = authRepository,
                    onNavigateToVerification = { email ->
                        navController.navigate(Screen.EmailVerification.createRoute(email))
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.EmailLogin.route) {
                LoginScreen(
                    authRepository = authRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.EmailLogin.route) { inclusive = true }
                        }
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.EmailLogin.route) { inclusive = true }
                        }
                    },
                    onNavigateToEmailSignup = { navController.navigate(Screen.EmailSignup.route) },
                    onNavigateToForgotPassword = { email ->
                        navController.navigate(Screen.ForgotPassword.createRoute(email))
                    },
                    onNavigateToVerification = { email ->
                        navController.navigate(Screen.EmailVerification.createRoute(email))
                    }
                )
            }
            composable(
                route = Screen.EmailVerification.route,
                arguments = listOf(navArgument("email") { type = NavType.StringType })
            ) { backStackEntry ->
                val emailArg = backStackEntry.arguments?.getString("email") ?: ""
                val email = if (emailArg == "none") "" else emailArg
                EmailVerificationScreen(
                    email = email,
                    authRepository = authRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.EmailVerification.route) { inclusive = true }
                        }
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.EmailVerification.route) { inclusive = true }
                        }
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.ForgotPassword.route,
                arguments = listOf(navArgument("email") { type = NavType.StringType })
            ) { backStackEntry ->
                val emailArg = backStackEntry.arguments?.getString("email") ?: ""
                val email = if (emailArg == "none") "" else emailArg
                ForgotPasswordScreen(
                    initialEmail = email,
                    authRepository = authRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.ForgotPassword.route) { inclusive = true }
                        }
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.ForgotPassword.route) { inclusive = true }
                        }
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.CompleteProfile.route) {
                CompleteProfileScreen(
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.CompleteProfile.route) { inclusive = true }
                        }
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Home.route) {
                HomeScreen(
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onSearchClick = { navController.navigate(Screen.Search.route) },
                    onViewAllClick = { navController.navigate(Screen.Library.createRoute()) },
                    onSubjectClick = { subject ->
                        navController.navigate(Screen.Library.createRoute(subject))
                    },
                    onForumClick = { navController.navigate(Screen.Forum.route) },
                    onStudyLabClick = { navController.navigate(Screen.StudyLab.route) },
                    onNebyAiClick = { navController.navigate(Screen.NebyAi.route) },
                    onNewsClick = { navController.navigate(Screen.News.route) },
                    onResultCheckerClick = { navController.navigate(Screen.ResultChecker.route) },
                    onNewsItemClick = { slug -> navController.navigate(Screen.NewsDetail.createRoute(slug)) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onUserProfileClick = { username -> navController.navigate(Screen.Profile.createRoute(username)) }
                )
            }
            composable(
                route = Screen.Library.route,
                arguments = listOf(navArgument("subject") { type = NavType.StringType; nullable = true; defaultValue = null })
            ) { backStackEntry ->
                LibraryScreen(
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onSearchClick = { navController.navigate(Screen.Search.route) },
                    onUploadClick = { navController.navigate(Screen.Upload.route) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onInteractiveCourseClick = { courseSlug ->
                        navController.navigate(Screen.InteractiveCourse.createRoute(courseSlug))
                    }
                )
            }
            composable(Screen.Forum.route) {
                ForumScreen(
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onCreatePostClick = { navController.navigate(Screen.CreatePost.route) },
                    onSearchClick = { navController.navigate(Screen.Search.route) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onUserProfileClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    }
                )
            }
            composable(Screen.News.route) {
                NewsScreen(
                    onNewsClick = { slug -> navController.navigate(Screen.NewsDetail.createRoute(slug)) },
                    onResultCheckerClick = { navController.navigate(Screen.ResultChecker.route) },
                    onSearchClick = { navController.navigate(Screen.Search.route) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile
                )
            }
            composable(
                route = Screen.NewsDetail.route,
                arguments = listOf(navArgument("slug") { type = NavType.StringType })
            ) { backStackEntry ->
                val slug = backStackEntry.arguments?.getString("slug") ?: return@composable
                NewsDetailScreen(
                    slug = slug,
                    onNavigateBack = { navController.popBackStack() },
                    onRelatedNewsClick = { relatedSlug -> navController.navigate(Screen.NewsDetail.createRoute(relatedSlug)) }
                )
            }
            composable(Screen.ResultChecker.route) {
                ResultCheckerScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Search.route) {
                SearchScreen(
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onProfileClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Notifications.route) {
                NotificationsScreen(
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onProfileClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    },
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    }
                )
            }
            composable(Screen.StudyLab.route) {
                StudyLabScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onOpenSpace = { spaceId -> navController.navigate(Screen.StudySpace.createRoute(spaceId)) },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(
                route = Screen.StudySpace.route,
                arguments = listOf(navArgument("spaceId") { type = NavType.StringType })
            ) {
                StudySpaceScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(Screen.NebyAi.route) {
                NebyAiScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(
                route = Screen.InteractiveCourse.route,
                arguments = listOf(navArgument("courseSlug") { type = NavType.StringType })
            ) { backStackEntry ->
                val courseSlug = backStackEntry.arguments?.getString("courseSlug") ?: return@composable
                InteractiveCourseScreen(
                    courseSlug = courseSlug,
                    onLessonClick = { cs, ls ->
                        navController.navigate(Screen.InteractiveLesson.createRoute(cs, ls))
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.InteractiveLesson.route,
                arguments = listOf(
                    navArgument("courseSlug") { type = NavType.StringType },
                    navArgument("lessonSlug") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val courseSlug = backStackEntry.arguments?.getString("courseSlug") ?: return@composable
                val lessonSlug = backStackEntry.arguments?.getString("lessonSlug") ?: return@composable
                InteractiveLessonScreen(
                    courseSlug = courseSlug,
                    lessonSlug = lessonSlug,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Analytics.route) {
                AnalyticsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(Screen.Bookmarks.route) {
                BookmarksScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onResourceClick = { resourceId -> navController.navigate(Screen.ResourceDetail.createRoute(resourceId)) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(Screen.Upload.route) {
                UploadScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onUploadSuccess = { navController.navigate(Screen.Library.createRoute()) }
                )
            }
            composable(
                route = Screen.Profile.route,
                arguments = listOf(navArgument("username") { type = NavType.StringType })
            ) { backStackEntry ->
                val username = backStackEntry.arguments?.getString("username") ?: ""
                ProfileScreen(
                    username = username,
                    onNavigateBack = { navController.popBackStack() },
                    onEditProfile = { navController.navigate(Screen.EditProfile.route) },
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onFollowerClick = { targetUsername ->
                        navController.navigate(Screen.Profile.createRoute(targetUsername))
                    },
                    onAnalyticsClick = { navController.navigate(Screen.Analytics.route) },
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(Screen.EditProfile.route) {
                EditProfileScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Settings.route) {
                SettingsScreen(
                    settingsViewModel = settingsViewModel,
                    onNavigateToEditProfile = { navController.navigate(Screen.EditProfile.route) },
                    onNavigateToBookmarks = { navController.navigate(Screen.Bookmarks.route) },
                    onNavigateToDeleteAccount = { navController.navigate(Screen.DeleteAccount.route) },
                    onNavigateToLogin = {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                        }
                    }
                )
            }
            composable(Screen.DeleteAccount.route) {
                com.neb.ians.ui.screens.settings.DeleteAccountScreen(
                    viewModel = settingsViewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            }

            composable(
                route = Screen.PdfViewer.route,
                arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
            ) {
                PdfViewerScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.ResourceDetail.route,
                arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
            ) {
                ResourceDetailScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onOpenPdf = { resourceId, fileUrl, title ->
                        navController.navigate(Screen.PdfViewer.createRoute(resourceId))
                    }
                )
            }
            composable(
                route = Screen.ForumPostDetail.route,
                arguments = listOf(navArgument("postId") { type = NavType.StringType })
            ) { backStackEntry ->
                val postId = backStackEntry.arguments?.getString("postId") ?: return@composable
                ForumPostDetailScreen(
                    postId = postId,
                    onNavigateBack = { navController.popBackStack() },
                    onReplyClick = { replyToId ->
                        navController.navigate(Screen.Reply.createRoute(postId, replyToId))
                    },
                    onProfileClick = { userId ->
                        navController.navigate(Screen.Profile.createRoute(userId))
                    }
                )
            }
            composable(Screen.CreatePost.route) {
                CreatePostScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onPostCreated = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.Reply.route,
                arguments = listOf(
                    navArgument("postId") { type = NavType.StringType },
                    navArgument("replyToId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val postId = backStackEntry.arguments?.getString("postId") ?: return@composable
                val replyToId = backStackEntry.arguments?.getString("replyToId")?.takeIf { it != "none" }
                ReplyScreen(
                    postId = postId,
                    replyToId = replyToId,
                    onNavigateBack = { navController.popBackStack() },
                    onReplySubmitted = { navController.popBackStack() }
                )
            }
        }

        if (showBottomBar) {
            LiquidGlassBottomNav(
                items = glassNavItems,
                currentRoute = currentRoute,
                onSelect = { item ->
                    navController.navigate(item.route) {
                        popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                        launchSingleTop = true
                        restoreState = true
                    }
                },
                modifier = Modifier.align(Alignment.BottomCenter)
            )
        }

        if (showProfileDropdown) {
            val profile = userProfile
            if (profile != null) {
                val density = LocalDensity.current
                val offsetX = with(density) { (-16).dp.roundToPx() }
                val offsetY = with(density) { 60.dp.roundToPx() }

                Popup(
                    alignment = Alignment.TopEnd,
                    offset = IntOffset(offsetX, offsetY),
                    onDismissRequest = { showProfileDropdown = false },
                    properties = PopupProperties(focusable = true)
                ) {
                    Column(
                        modifier = Modifier
                            .width(224.dp)
                            .shadow(12.dp, RoundedCornerShape(16.dp))
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surfaceContainer)
                            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(16.dp))
                            .padding(8.dp)
                    ) {
                        // Header
                        Row(
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            val name = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username
                            NebAvatar(
                                name = name.ifEmpty { "N" },
                                photoUrl = profile.photoUrl,
                                size = 38.dp
                            )
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    text = profile.username,
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.onSurface,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                                val roleText = when (profile.role) {
                                    "teacher" -> "Teacher"
                                    "institution" -> "Institution"
                                    "explorer" -> "Explorer"
                                    else -> "Student"
                                }
                                Text(
                                    text = roleText,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }

                        HorizontalDivider(
                            modifier = Modifier.padding(vertical = 4.dp),
                            color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                        )

                        // View Profile
                        ProfileDropdownItem(
                            icon = Icons.Outlined.Person,
                            text = "View Profile",
                            onClick = {
                                showProfileDropdown = false
                                navController.navigate(Screen.Profile.createRoute(profile.username))
                            }
                        )

                        // Bookmarks
                        ProfileDropdownItem(
                            icon = Icons.Filled.Bookmark,
                            text = "Bookmarks",
                            onClick = {
                                showProfileDropdown = false
                                navController.navigate(Screen.Bookmarks.route)
                            }
                        )

                        // News
                        ProfileDropdownItem(
                            icon = Icons.Outlined.Newspaper,
                            text = "News & Announcements",
                            onClick = {
                                showProfileDropdown = false
                                navController.navigate(Screen.News.route)
                            }
                        )

                        // Check Results
                        ProfileDropdownItem(
                            icon = Icons.Outlined.FactCheck,
                            text = "Check Results",
                            onClick = {
                                showProfileDropdown = false
                                navController.navigate(Screen.ResultChecker.route)
                            }
                        )

                        // Settings
                        ProfileDropdownItem(
                            icon = Icons.Outlined.Settings,
                            text = "Settings",
                            onClick = {
                                showProfileDropdown = false
                                navController.navigate(Screen.Settings.route)
                            }
                        )

                        HorizontalDivider(
                            modifier = Modifier.padding(vertical = 4.dp),
                            color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
                        )

                        // Sign Out
                        ProfileDropdownItem(
                            icon = Icons.Outlined.ExitToApp,
                            text = "Sign Out",
                            textColor = MaterialTheme.colorScheme.error,
                            iconColor = MaterialTheme.colorScheme.error,
                            onClick = {
                                showProfileDropdown = false
                                settingsViewModel.logout()
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ProfileDropdownItem(
    icon: ImageVector,
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    iconColor: Color = MaterialTheme.colorScheme.onSurfaceVariant,
    textColor: Color = MaterialTheme.colorScheme.onSurface
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(8.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 12.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(20.dp),
            tint = iconColor
        )
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium,
            color = textColor
        )
    }
}

private fun Color.luminanceIsDark(): Boolean {
    val l = 0.299f * red + 0.587f * green + 0.114f * blue
    return l < 0.5f
}