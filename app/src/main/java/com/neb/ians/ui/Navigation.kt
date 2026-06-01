package com.neb.ians.ui

import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LibraryBooks
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.LibraryBooks
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Notifications
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
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
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.home.HomeViewModel
import com.neb.ians.ui.screens.library.LibraryScreen
import com.neb.ians.ui.screens.library.LibraryViewModel
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.forum.ForumViewModel
import com.neb.ians.ui.screens.forum.ForumPostDetailScreen
import com.neb.ians.ui.screens.forum.PostDetailViewModel
import com.neb.ians.ui.screens.forum.CreatePostScreen
import com.neb.ians.ui.screens.forum.CreatePostViewModel
import com.neb.ians.ui.screens.forum.ReplyScreen
import com.neb.ians.ui.screens.forum.ReplyViewModel
import com.neb.ians.ui.screens.search.SearchScreen
import com.neb.ians.ui.screens.search.SearchViewModel
import com.neb.ians.ui.screens.profile.ProfileScreen
import com.neb.ians.ui.screens.profile.ProfileViewModel
import com.neb.ians.ui.screens.profile.EditProfileScreen
import com.neb.ians.ui.screens.notifications.NotificationsScreen
import com.neb.ians.ui.screens.notifications.NotificationsViewModel
import com.neb.ians.ui.screens.settings.SettingsScreen
import com.neb.ians.ui.screens.settings.SettingsViewModel
import com.neb.ians.ui.screens.reader.PdfReaderScreen
import com.neb.ians.ui.screens.auth.SplashScreen
import com.neb.ians.ui.screens.auth.LoginScreen
import com.neb.ians.ui.screens.auth.EmailSignupScreen
import com.neb.ians.ui.screens.auth.EmailLoginScreen
import com.neb.ians.ui.screens.auth.EmailVerificationScreen
import com.neb.ians.ui.screens.auth.ForgotPasswordScreen
import com.neb.ians.ui.screens.auth.CompleteProfileScreen
import com.neb.ians.ui.screens.auth.CompleteProfileViewModel
import dagger.hilt.EntryPoint
import dagger.hilt.InstallIn
import dagger.hilt.android.EntryPointAccessors
import dagger.hilt.components.SingletonComponent

@EntryPoint
@InstallIn(SingletonComponent::class)
interface AuthEntryPoint {
    fun authRepository(): AuthRepository
}

sealed class Screen(val route: String) {
    data object Splash : Screen("splash")
    data object Login : Screen("login")
    data object EmailSignup : Screen("email_signup")
    data object EmailLogin : Screen("email_login")
    data object EmailVerification : Screen("email_verification/{email}") {
        fun createRoute(email: String) = "email_verification/${java.net.URLEncoder.encode(email, "UTF-8")}"
    }
    data object ForgotPassword : Screen("forgot_password/{email}") {
        fun createRoute(email: String) = "forgot_password/${java.net.URLEncoder.encode(email, "UTF-8")}"
    }
    data object CompleteProfile : Screen("complete_profile")
    data object Home : Screen("home")
    data object Library : Screen("library?subject={subject}") {
        fun createRoute(subject: String? = null) = if (subject != null) "library?subject=$subject" else "library"
    }
    data object Forum : Screen("forum")
    data object Search : Screen("search")
    data object Notifications : Screen("notifications")
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
    val label: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector
)

val bottomNavItems = listOf(
    BottomNavItem(Screen.Home, "Home", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem(Screen.Library, "Library", Icons.Filled.LibraryBooks, Icons.Outlined.LibraryBooks),
    BottomNavItem(Screen.Forum, "Forum", Icons.Filled.Forum, Icons.Outlined.Forum),
    BottomNavItem(Screen.Notifications, "Alerts", Icons.Filled.Notifications, Icons.Outlined.Notifications),
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NEBiansNavHost(
    settingsViewModel: SettingsViewModel,
    navController: NavHostController = rememberNavController()
) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val authEntryPoint = remember(context) {
        EntryPointAccessors.fromApplication(context.applicationContext, AuthEntryPoint::class.java)
    }
    val authRepository = authEntryPoint.authRepository()

    val authState by settingsViewModel.authState.collectAsStateWithLifecycle()
    LaunchedEffect(authState) {
        if (authState is AuthState.Unauthenticated) {
            navController.navigate(Screen.Login.route) {
                popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
            }
        }
    }

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    val bottomBarScreens = bottomNavItems.map { it.screen.route }
    val showBottomBar = currentDestination?.route in bottomBarScreens

    Scaffold(
        containerColor = MaterialTheme.colorScheme.surface,
        bottomBar = {
            if (showBottomBar) {
                NavigationBar(
                    tonalElevation = 0.dp,
                    containerColor = MaterialTheme.colorScheme.surfaceContainer,
                ) {
                    bottomNavItems.forEach { item ->
                        val selected = currentDestination?.hierarchy?.any { it.route == item.screen.route } == true
                        NavigationBarItem(
                            icon = {
                                Icon(
                                    imageVector = if (selected) item.selectedIcon else item.unselectedIcon,
                                    contentDescription = item.label
                                )
                            },
                            label = {
                                Text(
                                    text = item.label,
                                    style = if (selected) MaterialTheme.typography.labelMedium
                                    else MaterialTheme.typography.labelSmall
                                )
                            },
                            selected = selected,
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = MaterialTheme.colorScheme.onSecondaryContainer,
                                selectedTextColor = MaterialTheme.colorScheme.onSecondaryContainer,
                                indicatorColor = MaterialTheme.colorScheme.secondaryContainer,
                                unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
                            ),
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
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Splash.route,
            modifier = Modifier.padding(
                bottom = if (showBottomBar) innerPadding.calculateBottomPadding() else 0.dp
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
                    onNavigateToEmailLogin = { navController.navigate(Screen.EmailLogin.route) }
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
                EmailLoginScreen(
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
                    onNavigateToForgotPassword = { email ->
                        navController.navigate(Screen.ForgotPassword.createRoute(email))
                    },
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.EmailVerification.route,
                arguments = listOf(navArgument("email") { type = NavType.StringType })
            ) { backStackEntry ->
                val email = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("email") ?: "", "UTF-8")
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
                val email = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("email") ?: "", "UTF-8")
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
                    }
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
                    onSearchClick = { navController.navigate(Screen.Search.route) }
                )
            }
            composable(Screen.Forum.route) {
                ForumScreen(
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onCreatePostClick = { navController.navigate(Screen.CreatePost.route) }
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
            composable(
                route = Screen.Profile.route,
                arguments = listOf(navArgument("username") { type = NavType.StringType })
            ) { backStackEntry ->
                val username = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("username") ?: "", "UTF-8")
                ProfileScreen(
                    username = username,
                    onNavigateBack = { navController.popBackStack() },
                    onEditProfile = { navController.navigate(Screen.EditProfile.route) },
                    onPostClick = { postId ->
                        navController.navigate(Screen.ForumPostDetail.createRoute(postId))
                    },
                    onFollowerClick = { userId ->
                        // Could navigate to followers modal or list
                    }
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

