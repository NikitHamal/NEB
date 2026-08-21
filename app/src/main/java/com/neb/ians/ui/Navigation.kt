package com.neb.ians.ui

import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.imePadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material3.ExperimentalMaterial3Api
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
import com.neb.ians.ui.components.LiquidGlassProfileSheet
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
import com.neb.ians.ui.screens.reader.MediaPlayerViewModel
import com.neb.ians.ui.screens.reader.MiniMediaPlayer

import com.neb.ians.ui.screens.resource.ResourceDetailScreen
import com.neb.ians.ui.screens.resource.ResourceRequestsScreen
import com.neb.ians.ui.screens.analytics.AnalyticsScreen
import com.neb.ians.ui.screens.bookmarks.BookmarksScreen
import com.neb.ians.ui.screens.downloads.DownloadsScreen
import com.neb.ians.ui.screens.upload.UploadScreen
import com.neb.ians.ui.screens.ai.NebyAiScreen
import com.neb.ians.ui.screens.localai.LocalNebyScreen
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
import com.neb.ians.ui.screens.results.ToolsScreen
import com.neb.ians.ui.screens.news.NewsDetailScreen
import com.neb.ians.ui.screens.news.NewsScreen
import com.neb.ians.ui.screens.credits.NebyCreditsScreen

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
    data object Tools : Screen("tools")
    data object Search : Screen("search?query={query}") {
        fun createRoute(query: String? = null): String = if (query.isNullOrBlank()) {
            "search"
        } else {
            "search?query=${java.net.URLEncoder.encode(query, "UTF-8")}"
        }
    }
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
    data object LocalNeby : Screen("neby_local")
    data object NebyCredits : Screen("credits")
    data object Analytics : Screen("analytics")
    data object Bookmarks : Screen("bookmarks")
    data object Downloads : Screen("downloads")
    data object Upload : Screen("upload")
    data object Profile : Screen("profile/{username}?showRequests={showRequests}") {
        fun createRoute(username: String, showRequests: Boolean = false) =
            "profile/${java.net.URLEncoder.encode(username, "UTF-8")}?showRequests=$showRequests"
    }
    data object EditProfile : Screen("profile/edit")
    data object Settings : Screen("settings")
    data object MyAvatar : Screen("my_avatar")
    data object DeleteAccount : Screen("delete_account")
    data object PdfViewer : Screen("pdf/{resourceId}") {
        fun createRoute(resourceId: String) = "pdf/$resourceId"
    }
    data object ResourceDetail : Screen("resource/{resourceId}") {
        fun createRoute(resourceId: String) = "resource/$resourceId"
    }
    data object EditResource : Screen("resource/{resourceId}/edit") {
        fun createRoute(resourceId: String) = "resource/$resourceId/edit"
    }
    data object ResourceRequests : Screen("resource/requests")
    data object ForumPostDetail : Screen("forum/post/{postId}") {
        fun createRoute(postId: String) = "forum/post/$postId"
    }
    data object CreatePost : Screen("forum/create")
    data object EditPost : Screen("forum/edit/{postId}") {
        fun createRoute(postId: String) = "forum/edit/${java.net.URLEncoder.encode(postId, "UTF-8")}"
    }
    data object Reply : Screen("forum/reply/{postId}/{replyToId}") {
        fun createRoute(postId: String, replyToId: String? = null) = "forum/reply/$postId/${replyToId ?: "none"}"
    }
    data object WebPortal : Screen("web_portal/{url}") {
        fun createRoute(url: String) = "web_portal/${java.net.URLEncoder.encode(url, "UTF-8")}"
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
    val mediaPlayerViewModel: MediaPlayerViewModel = hiltViewModel()
    val mediaPlayerState by mediaPlayerViewModel.uiState.collectAsStateWithLifecycle()
    var showMiniPlayer by remember { mutableStateOf(false) }
    val isAuthenticated = authState is AuthState.Authenticated
    LaunchedEffect(authState) {
        val state = authState
        when (state) {
            is AuthState.Unauthenticated -> {
                showMiniPlayer = false
                mediaPlayerViewModel.stopPlayback()
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
    var hideLibraryDetailChrome by remember { mutableStateOf(false) }
    LaunchedEffect(currentRoute) {
        if (currentRoute != "library") hideLibraryDetailChrome = false
    }
    val showBottomBar = currentRoute in glassNavItems.map { it.route } && !hideLibraryDetailChrome
    LaunchedEffect(currentRoute, mediaPlayerState.resource?.id, mediaPlayerState.isPlaying, mediaPlayerState.currentTimeMs) {
        showMiniPlayer = when {
            currentRoute == Screen.ResourceDetail.route -> false
            mediaPlayerState.resource == null -> false
            mediaPlayerState.isPlaying -> true
            mediaPlayerState.currentTimeMs > 0L -> true
            else -> showMiniPlayer
        }
    }
    var showProfileDropdown by remember { mutableStateOf(false) }
    val navigateToOwnProfile = {
        val username = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
        if (username != null) {
            showProfileDropdown = !showProfileDropdown
        } else {
            navController.navigate(Screen.Settings.route)
        }
    }

    Box(modifier = Modifier.fillMaxSize().imePadding()) {
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
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) },
                    onViewAllClick = { navController.navigate(Screen.Library.createRoute()) },
                    onForumClick = { navController.navigate(Screen.Forum.route) },
                    onNewsClick = { navController.navigate(Screen.News.route) },
                    onUploadClick = { navController.navigate(Screen.Upload.route) },
                    onNewsItemClick = { slug -> navController.navigate(Screen.NewsDetail.createRoute(slug)) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onEditPostClick = { editPostId ->
                        navController.navigate(Screen.EditPost.createRoute(editPostId))
                    },
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
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) },
                    onUploadClick = { navController.navigate(Screen.Upload.route) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onInteractiveCourseClick = { courseSlug ->
                        navController.navigate(Screen.InteractiveCourse.createRoute(courseSlug))
                    },
                    onSyllabusDetailChromeChanged = { hideLibraryDetailChrome = it },
                    onRequestResourceClick = { navController.navigate(Screen.ResourceRequests.route) }
                )
            }
            composable(Screen.Forum.route) {
                ForumScreen(
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onCreatePostClick = { navController.navigate(Screen.CreatePost.route) },
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onUserProfileClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    },
                    onEditPostClick = { editPostId ->
                        navController.navigate(Screen.EditPost.createRoute(editPostId))
                    }
                )
            }
            composable(Screen.News.route) {
                NewsScreen(
                    onNewsClick = { slug -> navController.navigate(Screen.NewsDetail.createRoute(slug)) },
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) },
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
            composable(Screen.Tools.route) {
                ToolsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToResultChecker = { navController.navigate(Screen.ResultChecker.route) }
                )
            }
            composable(
                route = Screen.Search.route,
                arguments = listOf(navArgument("query") { type = NavType.StringType; defaultValue = "" })
            ) { backStackEntry ->
                SearchScreen(
                    initialQuery = backStackEntry.arguments?.getString("query").orEmpty(),
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
                    onNavigateBack = { navController.popBackStack() },
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
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) }
                )
            }
            composable(
                route = Screen.StudySpace.route,
                arguments = listOf(navArgument("spaceId") { type = NavType.StringType })
            ) {
                StudySpaceScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) }
                )
            }
            composable(Screen.NebyAi.route) {
                NebyAiScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) }
                )
            }
            composable(Screen.LocalNeby.route) {
                LocalNebyScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onToolAction = { call ->
                        when (call.name) {
                            "search_resources", "find_notes" -> {
                                val query = listOfNotNull(
                                    call.argument("query"),
                                    call.argument("subject"),
                                    call.argument("grade_level"),
                                    call.argument("exam_type")
                                ).distinct().joinToString(" ")
                                navController.navigate(Screen.Search.createRoute(query))
                            }
                            "get_forum_posts" -> navController.navigate(Screen.Forum.route)
                            "get_subjects" -> navController.navigate(Screen.Library.createRoute())
                            "navigate_to" -> {
                                val route = when (call.argument("page")) {
                                    "home" -> Screen.Home.route
                                    "library" -> Screen.Library.createRoute()
                                    "forum" -> Screen.Forum.route
                                    "search" -> Screen.Search.createRoute()
                                    "news" -> Screen.News.route
                                    "settings" -> Screen.Settings.route
                                    "bookmarks" -> Screen.Bookmarks.route
                                    "upload" -> Screen.Upload.route
                                    "results" -> Screen.ResultChecker.route
                                    "tools" -> Screen.Tools.route
                                    else -> Screen.Home.route
                                }
                                navController.navigate(route)
                            }
                        }
                    }
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
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) }
                )
            }
            composable(Screen.Bookmarks.route) {
                BookmarksScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onResourceClick = { resourceId -> navController.navigate(Screen.ResourceDetail.createRoute(resourceId)) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) }
                )
            }
            composable(Screen.Downloads.route) {
                DownloadsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onOpenPdf = { resourceId -> navController.navigate(Screen.PdfViewer.createRoute(resourceId)) },
                    onOpenMedia = { resourceId -> navController.navigate(Screen.ResourceDetail.createRoute(resourceId)) }
                )
            }
            composable(Screen.Upload.route) {
                UploadScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onUploadSuccess = { navController.navigate(Screen.Library.createRoute()) }
                )
            }
            composable(Screen.NebyCredits.route) {
                NebyCreditsScreen(
                    onBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.Profile.route,
                arguments = listOf(
                    navArgument("username") { type = NavType.StringType },
                    navArgument("showRequests") { type = NavType.BoolType; defaultValue = false }
                )
            ) { backStackEntry ->
                val usernameArg = backStackEntry.arguments?.getString("username") ?: ""
                val showRequests = backStackEntry.arguments?.getBoolean("showRequests") ?: false
                val ownUsername = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
                val username = if (usernameArg == "me" || usernameArg == ownUsername) {
                    ownUsername ?: ""
                } else {
                    usernameArg
                }
                ProfileScreen(
                    username = username,
                    showRequests = showRequests,
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
                    onSearchClick = { navController.navigate(Screen.Search.createRoute()) },
                    onProfileClick = { targetUsername ->
                        navController.navigate(Screen.Profile.createRoute(targetUsername))
                    }
                )
            }
            composable(Screen.EditProfile.route) {
                EditProfileScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.WebPortal.route,
                arguments = listOf(navArgument("url") { type = NavType.StringType })
            ) { backStackEntry ->
                val url = backStackEntry.arguments?.getString("url") ?: ""
                com.neb.ians.ui.screens.web.WebPortalScreen(
                    url = url,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.Settings.route) {
                SettingsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    settingsViewModel = settingsViewModel,
                    onNavigateToEditProfile = { navController.navigate(Screen.EditProfile.route) },
                    onNavigateToBookmarks = { navController.navigate(Screen.Bookmarks.route) },
                    onNavigateToNebyCredits = { navController.navigate(Screen.NebyCredits.route) },
                    onNavigateToLocalNeby = { navController.navigate(Screen.LocalNeby.route) },
                    onNavigateToMyAvatar = { navController.navigate(Screen.MyAvatar.route) },
                    onNavigateToDeleteAccount = { navController.navigate(Screen.DeleteAccount.route) },
                    onNavigateToLogin = {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                        }
                    },
                    onNavigateToWebPortal = { url ->
                        navController.navigate(Screen.WebPortal.createRoute(url))
                    }
                )
            }
            composable(Screen.MyAvatar.route) {
                com.neb.ians.ui.screens.avatar.MyAvatarScreen(
                    onNavigateBack = { navController.popBackStack() }
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
            ) { backStackEntry ->
                val resourceId = backStackEntry.arguments?.getString("resourceId") ?: return@composable
                ResourceDetailScreen(
                    onNavigateBack = {
                        val keepPlayback = mediaPlayerState.resource?.id == resourceId &&
                            (mediaPlayerState.isPlaying || mediaPlayerState.currentTimeMs > 0L)
                        if (keepPlayback) {
                            showMiniPlayer = true
                        } else if (mediaPlayerState.resource?.id == resourceId) {
                            mediaPlayerViewModel.stopPlayback()
                        }
                        navController.popBackStack()
                    },
                    onOpenPdf = { pdfResourceId, _, _ ->
                        navController.navigate(Screen.PdfViewer.createRoute(pdfResourceId))
                    },
                    onUserProfileClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    },
                    onRelatedResourceClick = { relatedResourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(relatedResourceId)) {
                            launchSingleTop = true
                        }
                    },
                    onMinimizeVideo = {
                        showMiniPlayer = true
                        navController.popBackStack()
                    },
                    onEditResource = { id ->
                        navController.navigate(Screen.EditResource.createRoute(id))
                    },
                    mediaViewModel = mediaPlayerViewModel
                )
            }
            composable(Screen.ResourceRequests.route) {
                ResourceRequestsScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.EditResource.route,
                arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
            ) {
                // Editing reuses the very upload wizard (PATCH mode via SavedStateHandle resourceId).
                UploadScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onUploadSuccess = { navController.popBackStack() }
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
                    onEditPostClick = { editPostId ->
                        navController.navigate(Screen.EditPost.createRoute(editPostId))
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
                route = Screen.EditPost.route,
                arguments = listOf(navArgument("postId") { type = NavType.StringType })
            ) { backStackEntry ->
                val editPostId = backStackEntry.arguments?.getString("postId") ?: return@composable
                CreatePostScreen(
                    postId = editPostId,
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

        if (showMiniPlayer && currentRoute != Screen.ResourceDetail.route && mediaPlayerState.resource != null) {
            MiniMediaPlayer(
                uiState = mediaPlayerState,
                viewModel = mediaPlayerViewModel,
                onExpand = {
                    mediaPlayerState.resource?.id?.let { resourceId ->
                        showMiniPlayer = false
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId)) {
                            launchSingleTop = true
                        }
                    }
                },
                onClose = {
                    showMiniPlayer = false
                    mediaPlayerViewModel.stopPlayback()
                },
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(bottom = if (showBottomBar) 92.dp else 12.dp)
            )
        }

        if (showProfileDropdown) {
            userProfile?.let { profile ->
                val displayName = profile.displayName?.takeIf { it.isNotBlank() } ?: profile.username
                LiquidGlassProfileSheet(
                    displayName = displayName,
                    username = profile.username,
                    role = profile.role,
                    photoUrl = profile.photoUrl,
                    onDismiss = { showProfileDropdown = false },
                    onProfileClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.Profile.createRoute(profile.username))
                    },
                    onBookmarksClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.Bookmarks.route)
                    },
                    onDownloadsClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.Downloads.route)
                    },
                    onBlogClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.News.route)
                    },
                    onToolsClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.Tools.route)
                    },
                    onSettingsClick = {
                        showProfileDropdown = false
                        navController.navigate(Screen.Settings.route)
                    },
                    onSignOutClick = {
                        showProfileDropdown = false
                        settingsViewModel.logout()
                    }
                )
            }
        }
    }
}
