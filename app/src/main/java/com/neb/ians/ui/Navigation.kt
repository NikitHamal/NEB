package com.neb.ians.ui

import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
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
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.library.LibraryScreen
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.forum.ForumPostDetailScreen
import com.neb.ians.ui.screens.forum.CreatePostScreen
import com.neb.ians.ui.screens.forum.ReplyScreen
import com.neb.ians.ui.screens.search.SearchScreen
import com.neb.ians.ui.screens.study.StudyLabScreen
import com.neb.ians.ui.screens.study.StudySpaceScreen
import com.neb.ians.ui.screens.ai.NebyAiScreen
import com.neb.ians.ui.screens.analytics.AnalyticsScreen
import com.neb.ians.ui.screens.bookmarks.BookmarksScreen
import com.neb.ians.ui.screens.profile.ProfileScreen
import com.neb.ians.ui.screens.profile.EditProfileScreen
import com.neb.ians.ui.screens.notifications.NotificationsScreen
import com.neb.ians.ui.screens.settings.SettingsScreen
import com.neb.ians.ui.screens.settings.SettingsViewModel
import com.neb.ians.ui.screens.reader.PdfReaderScreen
import com.neb.ians.ui.components.LiquidNavContainer
import com.neb.ians.ui.components.WebPillShape
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
    data object ForumPostDetail : Screen("forum/post/{postId}") {
        fun createRoute(postId: String) = "forum/post/$postId"
    }
    data object CreatePost : Screen("forum/create")
    data object Reply : Screen("forum/reply/{postId}/{replyToId}") {
        fun createRoute(postId: String, replyToId: String? = null) = "forum/reply/$postId/${replyToId ?: "none"}"
    }
}

data class BottomNavItem(
    val screen: Screen,
    val label: String
)

val bottomNavItems = listOf(
    BottomNavItem(
        Screen.Home,
        "Home"
    ),
    BottomNavItem(
        Screen.Library,
        "Library"
    ),
    BottomNavItem(
        Screen.Forum,
        "Forum"
    )
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
    LaunchedEffect(authState) {
        when (authState) {
            is AuthState.Unauthenticated -> {
                navController.navigate(Screen.Login.route) {
                    popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                }
            }
            is AuthState.Authenticated -> {
                val currentRoute = navController.currentBackStackEntry?.destination?.route
                if (currentRoute == Screen.Login.route || currentRoute == Screen.EmailLogin.route || currentRoute == Screen.EmailSignup.route) {
                    val dest = if (authState.isProfileComplete) Screen.Home.route else Screen.CompleteProfile.route
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

    val bottomBarScreens = bottomNavItems.map { it.screen.route }
    val showBottomBar = currentDestination?.route in bottomBarScreens
    val navigateToOwnProfile = {
        val username = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
        if (username != null) navController.navigate(Screen.Profile.createRoute(username))
        else navController.navigate(Screen.Settings.route)
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        bottomBar = {
            if (showBottomBar) {
                Box(
                    modifier = Modifier.fillMaxWidth(),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    LiquidNavContainer {
                    bottomNavItems.forEach { item ->
                        val selected = currentDestination?.hierarchy?.any { it.route == item.screen.route } == true
                        FloatingNavItem(
                            label = item.label,
                            selected = selected,
                            onClick = {
                                navController.navigate(item.screen.route) {
                                    popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        )
                    }
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Splash.route,
            modifier = Modifier.padding(
                bottom = if (showBottomBar) 86.dp else 0.dp
            ),
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
                        navController.navigate(Screen.PdfReader.createRoute(resourceId))
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
                        navController.navigate(Screen.PdfReader.createRoute(resourceId))
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
                    onProfileClick = navigateToOwnProfile
                )
            }
            composable(Screen.Search.route) {
                SearchScreen(
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.PdfReader.createRoute(resourceId))
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
                    onResourceClick = { resourceId -> navController.navigate(Screen.PdfReader.createRoute(resourceId)) },
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
                    onFollowerClick = { userId ->
                        // Could navigate to followers modal or list
                    },
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
                route = Screen.ForumPostDetail.route,
                arguments = listOf(navArgument("postId") { type = NavType.StringType })
            ) { backStackEntry ->
                val postId = backStackEntry.arguments?.getString("postId") ?: return@composable
                ForumPostDetailScreen(
                    postId = postId,
                    onNavigateBack = { navController.popBackStack() },
                    onReplyClick = { replyToId ->
                        navController.navigate(Screen.Reply.createRoute(postId, replyToId))
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
    }
}

@Composable
private fun RowScope.FloatingNavItem(
    label: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    val background = if (selected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainer.copy(alpha = 0f)
    val color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
    Box(
        modifier = Modifier
            .weight(1f)
            .widthIn(min = 92.dp)
            .heightIn(min = 42.dp)
            .clip(WebPillShape)
            .background(background)
            .clickable(onClick = onClick)
            .padding(horizontal = 18.dp, vertical = 10.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelLarge,
            color = color,
            fontWeight = if (selected) FontWeight.Bold else FontWeight.SemiBold,
            maxLines = 1
        )
    }
}
