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
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.LaunchedEffect
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
import com.neb.ians.ui.screens.reader.PdfReaderScreen
import com.neb.ians.ui.screens.reader.PdfViewerScreen
import com.neb.ians.ui.screens.resource.ResourceDetailScreen
import com.neb.ians.ui.screens.analytics.AnalyticsScreen
import com.neb.ians.ui.screens.bookmarks.BookmarksScreen
import com.neb.ians.ui.screens.ai.NebyAiScreen
import com.neb.ians.ui.screens.study.StudyLabScreen
import com.neb.ians.ui.screens.study.StudySpaceScreen
import com.neb.ians.ui.screens.auth.SplashScreen
import com.neb.ians.ui.screens.auth.LoginScreen
import com.neb.ians.ui.screens.auth.EmailSignupScreen
import com.neb.ians.ui.screens.auth.EmailLoginScreen
import com.neb.ians.ui.screens.auth.EmailVerificationScreen
import com.neb.ians.ui.screens.auth.ForgotPasswordScreen
import com.neb.ians.ui.screens.auth.CompleteProfileScreen

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
    data object Search : Screen("search")
    data object Notifications : Screen("notifications")
    data object StudyLab : Screen("study_lab")
    data object StudySpace : Screen("study_space/{spaceId}") {
        fun createRoute(spaceId: String) = "study_space/$spaceId"
    }
    data object NebyAi : Screen("neby_ai")
    data object Analytics : Screen("analytics")
    data object Bookmarks : Screen("bookmarks")
    data object Profile : Screen("profile/{username}") {
        fun createRoute(username: String) = "profile/${java.net.URLEncoder.encode(username, "UTF-8")}"
    }
    data object EditProfile : Screen("profile/edit")
    data object Settings : Screen("settings")
    data object PdfReader : Screen("reader/{resourceId}") {
        fun createRoute(resourceId: String) = "reader/$resourceId"
    }
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
    val isDarkMode by settingsViewModel.isDarkMode.collectAsStateWithLifecycle()
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

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    val currentRoute = currentDestination?.route?.substringBefore("?")
    val showBottomBar = currentRoute in glassNavItems.map { it.route }
    val navigateToOwnProfile = {
        val username = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
        if (username != null) navController.navigate(Screen.Profile.createRoute(username))
        else navController.navigate(Screen.Settings.route)
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
                    onViewAllClick = { navController.navigate(Screen.Library.route) },
                    onSubjectClick = { subject ->
                        navController.navigate(Screen.Library.createRoute(subject))
                    },
                    onForumClick = { navController.navigate(Screen.Forum.route) },
                    onStudyLabClick = { navController.navigate(Screen.StudyLab.route) },
                    onNebyAiClick = { navController.navigate(Screen.NebyAi.route) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile
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
                    onUploadClick = { navController.navigate(Screen.StudyLab.route) },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile
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
                    onFollowerClick = { userId -> },
                    onAnalyticsClick = { navController.navigate(Screen.Analytics.route) },
                    onBookmarksClick = { navController.navigate(Screen.Bookmarks.route) },
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
                    onNavigateToLogin = {
                        navController.navigate(Screen.Login.route) {
                            popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                        }
                    }
                )
            }
            composable(
                route = Screen.PdfReader.route,
                arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
            ) { backStackEntry ->
                val resourceId = backStackEntry.arguments?.getString("resourceId") ?: return@composable
                PdfReaderScreen(
                    resourceId = resourceId,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.PdfViewer.route,
                arguments = listOf(navArgument("resourceId") { type = NavType.StringType })
            ) {
                PdfViewerScreen(
                    onNavigateBack = { navController.popBackStack() },
                    isDark = isDarkMode,
                    onToggleTheme = { settingsViewModel.setDarkMode(!isDarkMode) }
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
                    },
                    isDark = isDarkMode,
                    onToggleTheme = { settingsViewModel.setDarkMode(!isDarkMode) }
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
    }
}