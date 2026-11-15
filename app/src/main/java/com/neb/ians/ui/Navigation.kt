package com.neb.ians.ui

import androidx.compose.ui.unit.IntOffset
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.VisibilityThreshold
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.imePadding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.Forum
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.saveable.rememberSaveable
import com.neb.ians.ui.components.navBarScrollSource
import com.neb.ians.ui.components.navBarScrollTransform
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
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
import com.neb.ians.data.api.AuthExpiryBus
import com.neb.ians.data.repository.AuthRepository
import com.neb.ians.data.repository.AuthState
import com.neb.ians.util.DeepLinkBus
import kotlinx.coroutines.launch
import com.neb.ians.ui.components.LiquidGlassBottomNav
import com.neb.ians.ui.components.glassSource
import androidx.compose.ui.draw.blur
import com.neb.ians.ui.components.LiquidGlassProfileSheet
import com.neb.ians.ui.components.NebFabAction
import com.neb.ians.ui.components.NebFabMenuScrim
import com.neb.ians.ui.components.AuthGate
import com.neb.ians.ui.components.GateReason
import com.neb.ians.ui.components.LocalAuthGate
import com.neb.ians.ui.components.SignInSheet
import com.neb.ians.ui.screens.pathways.PathwaysScreen
import com.neb.ians.ui.screens.lab.DynamicPostsLabScreen
import com.neb.ians.ui.components.NebNavItem
import com.neb.ians.ui.screens.home.HomeScreen
import com.neb.ians.ui.screens.library.LibraryScreen
import com.neb.ians.ui.screens.marketplace.CreatorPageScreen
import com.neb.ians.ui.screens.marketplace.CreatorStudioScreen
import com.neb.ians.ui.screens.marketplace.MarketplaceCourseScreen
import com.neb.ians.ui.screens.notes.NoteEditorScreen
import com.neb.ians.ui.screens.notes.NotesScreen
import com.neb.ians.ui.screens.notes.VoiceModelsScreen
import com.neb.ians.ui.screens.forum.ForumScreen
import com.neb.ians.ui.screens.forum.ForumPostDetailScreen
import com.neb.ians.ui.screens.forum.CreatePostScreen
import com.neb.ians.ui.screens.search.SearchScreen
import com.neb.ians.ui.screens.profile.ProfileScreen
import com.neb.ians.ui.screens.profile.edit.EditProfileScreen
import com.neb.ians.ui.screens.people.PeopleScreen
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
import com.neb.ians.ui.screens.interactive.InteractiveCourseScreen
import com.neb.ians.ui.screens.interactive.InteractiveLessonScreen
import com.neb.ians.ui.screens.auth.SplashScreen
import com.neb.ians.ui.screens.auth.LoginScreen
import com.neb.ians.ui.screens.auth.EmailAuthScreen
import com.neb.ians.ui.screens.auth.EmailVerificationScreen
import com.neb.ians.ui.screens.auth.ForgotPasswordScreen
import com.neb.ians.ui.screens.onboarding.IntroScreen
import com.neb.ians.ui.screens.onboarding.OnboardingScreen
import com.neb.ians.ui.screens.results.ResultCheckerScreen
import com.neb.ians.ui.screens.results.ToolsScreen
import com.neb.ians.ui.screens.news.NewsDetailScreen
import com.neb.ians.ui.screens.news.NewsScreen
import com.neb.ians.ui.screens.credits.NebyCreditsScreen
import androidx.compose.material.icons.outlined.SpaceDashboard
import androidx.compose.material.icons.outlined.RateReview
import androidx.compose.material.icons.outlined.CloudUpload
import androidx.activity.compose.BackHandler
import com.neb.ians.ui.theme.NebAccents

sealed class Screen(val route: String) {
    data object Splash : Screen("splash")
    data object Intro : Screen("intro")
    data object Login : Screen("login")
    data object EmailAuth : Screen("email_auth")
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
    data object People : Screen("people")
    data object InteractiveCourse : Screen("interactive/course/{courseSlug}") {
        fun createRoute(courseSlug: String) = "interactive/course/$courseSlug"
    }
    data object StudyReader : Screen("study/{grade}/{subject}/{kind}/{no}") {
        fun createRoute(grade: String, subject: String, kind: String, no: Int) = "study/$grade/$subject/$kind/$no"
    }
    data object InteractiveLesson : Screen("interactive/lesson/{courseSlug}/{lessonSlug}") {
        fun createRoute(courseSlug: String, lessonSlug: String) = "interactive/lesson/$courseSlug/$lessonSlug"
    }
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
    data object About : Screen("about")
    data object Notes : Screen("notes")
    data object NoteEditor : Screen("notes/edit/{noteId}?dictate={dictate}") {
        fun createRoute(noteId: String = "new", dictate: Boolean = false) = "notes/edit/$noteId?dictate=$dictate"
    }
    data object VoiceModels : Screen("notes/voice")
    data object DeleteAccount : Screen("delete_account")
    data object AccountSecurity : Screen("account_security")
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
    data object CreatorStudio : Screen("marketplace/studio")
    data object CreatorPage : Screen("marketplace/creator/{slug}") {
        fun createRoute(slug: String) = "marketplace/creator/$slug"
    }
    data object MarketplaceCourse : Screen("marketplace/course/{courseId}") {
        fun createRoute(courseId: String) = "marketplace/course/$courseId"
    }
    data object ForumPostDetail : Screen("forum/post/{postId}") {
        fun createRoute(postId: String) = "forum/post/$postId"
    }
    data object PostInsights : Screen("forum/post/{postId}/insights") {
        fun createRoute(postId: String) = "forum/post/$postId/insights"
    }
    data object ResourceInsights : Screen("library/insights?resourceId={resourceId}") {
        fun createRoute(resourceId: String?) =
            if (resourceId.isNullOrBlank()) "library/insights" else "library/insights?resourceId=${java.net.URLEncoder.encode(resourceId, "UTF-8")}"
    }
    data object CreatePost : Screen("forum/create")
    data object EditPost : Screen("forum/edit/{postId}") {
        fun createRoute(postId: String) = "forum/edit/${java.net.URLEncoder.encode(postId, "UTF-8")}"
    }
    data object WebPortal : Screen("web_portal/{url}") {
        fun createRoute(url: String) = "web_portal/${java.net.URLEncoder.encode(url, "UTF-8")}"
    }
    data object Pathways : Screen("pathways")
    data object PostLab : Screen("forum/lab")
    data object Legal : Screen("legal/{doc}") {
        fun createRoute(doc: String) = "legal/$doc"
    }
}

/** Screens that come before the app proper; a notification target waits until the app has left them. */
private val PRE_APP_ROUTES = setOf(
    Screen.Splash.route,
    Screen.Intro.route,
    Screen.Login.route,
    Screen.EmailAuth.route,
    Screen.CompleteProfile.route,
)

/** Screens that need an account; a guest is stopped at the door with the sign-in sheet and sent on after. */
private fun gateReasonFor(route: String?): GateReason? = when (route) {
    Screen.Upload.route, Screen.CreatorStudio.route, Screen.ResourceRequests.route -> GateReason.Upload
    Screen.CreatePost.route, Screen.EditPost.route -> GateReason.Post
    Screen.Bookmarks.route -> GateReason.Save
    Screen.Notifications.route -> GateReason.Notifications
    Screen.Analytics.route, Screen.NebyCredits.route, Screen.EditProfile.route,
    Screen.DeleteAccount.route, Screen.AccountSecurity.route, Screen.PostInsights.route,
    Screen.ResourceInsights.route -> GateReason.Profile
    else -> null
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
        route = "notes",
        label = "Notes",
        selectedIcon = Icons.Filled.EditNote,
        unselectedIcon = Icons.Outlined.EditNote,
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
    // the player's position ticks four times a second; the host only needs to know whether there
    // is something playing, so it does not recompose with every tick (MiniPlayerSlot reads the rest)
    val playerResourceId by remember { derivedStateOf { mediaPlayerState.resource?.id } }
    val playerStarted by remember { derivedStateOf { mediaPlayerState.isPlaying || mediaPlayerState.currentTimeMs > 0L } }
    var showMiniPlayer by remember { mutableStateOf(false) }
    val isAuthenticated = authState is AuthState.Authenticated
    var gateReason by remember { mutableStateOf<GateReason?>(null) }
    // the screen a guest was trying to reach; once they are signed in they are sent there
    var pendingRoute by rememberSaveable { mutableStateOf<String?>(null) }
    val gate = remember(isAuthenticated) { AuthGate(isAuthenticated) { gateReason = it } }
    val openSignIn: () -> Unit = {
        gateReason = null
        navController.navigate(Screen.Login.route) { launchSingleTop = true }
    }
    // Leaves the sign-in screens for the screen the guest came from (never Home by default).
    val leaveAuth: () -> Unit = {
        val back = navController.popBackStack(Screen.Login.route, true)
        if (!back) {
            navController.navigate(Screen.Home.route) {
                popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
            }
        }
        pendingRoute?.let { target ->
            pendingRoute = null
            navController.navigate(target) { launchSingleTop = true }
        }
    }
    LaunchedEffect(authState) {
        val state = authState
        when (state) {
            is AuthState.Unauthenticated -> {
                showMiniPlayer = false
                mediaPlayerViewModel.stopPlayback()
                val currentRoute = navController.currentBackStackEntry?.destination?.route
                // Signed out (or a guest from the start): stay in the app, on Home.
                if (currentRoute != null &&
                    currentRoute != Screen.Splash.route &&
                    currentRoute != Screen.Intro.route &&
                    currentRoute != Screen.Login.route &&
                    currentRoute != Screen.EmailAuth.route &&
                    currentRoute != Screen.Home.route
                ) {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                    }
                }
            }
            is AuthState.Authenticated -> {
                val currentRoute = navController.currentBackStackEntry?.destination?.route
                if (currentRoute == Screen.Login.route || currentRoute == Screen.EmailAuth.route) {
                    if (state.isProfileComplete) leaveAuth()
                    else navController.navigate(Screen.CompleteProfile.route)
                }
            }
            else -> {}
        }
    }

    // A 401 anywhere means the stored bearer token no longer resolves (30-day TTL,
    // or a legacy column-only token). Rather than leaving the user in a session
    // where every authenticated call fails, sign out here; the authState effect
    // above then routes them to Login with a clean back stack.
    LaunchedEffect(Unit) {
        AuthExpiryBus.events.collect {
            authRepository.logout()
        }
    }

    val deepLinkScope = rememberCoroutineScope()
    val pendingDeepLink by DeepLinkBus.pendingDeepLink.collectAsState()
    // A tapped notification lands on a synthetic back stack (Home, then the target) so Back goes
    // to Home and never to the splash or a sign-in screen. Applied once the app is on a real screen.
    val openDeepLink: () -> Unit = openDeepLink@{
        val deepLink = DeepLinkBus.pendingDeepLink.value ?: return@openDeepLink
        DeepLinkBus.clear()
        val route = deepLink.route
        if (route != null) {
            navController.navigate(route) {
                popUpTo(Screen.Home.route) { inclusive = false }
                launchSingleTop = true
            }
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
    LaunchedEffect(currentRoute, authState) {
        if (authState !is AuthState.Unauthenticated) return@LaunchedEffect
        val reason = gateReasonFor(currentDestination?.route) ?: gateReasonFor(currentRoute) ?: return@LaunchedEffect
        pendingRoute = navBackStackEntry?.destination?.route?.takeIf { !it.contains("{") }
        navController.popBackStack()
        gateReason = reason
    }
    LaunchedEffect(pendingDeepLink, isAuthenticated, currentRoute) {
        if (!isAuthenticated || pendingDeepLink == null) return@LaunchedEffect
        val route = currentRoute ?: return@LaunchedEffect
        if (route in PRE_APP_ROUTES) return@LaunchedEffect
        openDeepLink()
    }
    var hideLibraryDetailChrome by remember { mutableStateOf(false) }
    LaunchedEffect(currentRoute) {
        if (currentRoute != "library") hideLibraryDetailChrome = false
    }
    val showBottomBar = currentRoute in glassNavItems.map { it.route } && !hideLibraryDetailChrome
    LaunchedEffect(currentRoute, playerResourceId, playerStarted) {
        showMiniPlayer = when {
            currentRoute == Screen.ResourceDetail.route -> false
            playerResourceId == null -> false
            playerStarted -> true
            else -> showMiniPlayer
        }
    }
    var showProfileDropdown by remember { mutableStateOf(false) }
    var showCreateMenu by remember { mutableStateOf(false) }
    val createMenuActions = remember(navController, isAuthenticated) {
        listOf(
            NebFabAction(
                label = "New note",
                icon = Icons.Outlined.EditNote,
                onClick = { navController.navigate(Screen.NoteEditor.createRoute()) },
                accent = NebAccents.Teal,
                testTag = "create_menu_new_note"
            ),
            NebFabAction(
                label = "Upload materials",
                icon = Icons.Outlined.CloudUpload,
                onClick = {
                    if (isAuthenticated) navController.navigate(Screen.Upload.route)
                    else { pendingRoute = Screen.Upload.route; gateReason = GateReason.Upload }
                },
                accent = NebAccents.Amber,
                testTag = "create_menu_upload_materials"
            ),
            NebFabAction(
                label = "New post",
                icon = Icons.Outlined.RateReview,
                onClick = {
                    if (isAuthenticated) navController.navigate(Screen.CreatePost.route)
                    else { pendingRoute = Screen.CreatePost.route; gateReason = GateReason.Post }
                },
                accent = NebAccents.Brand,
                testTag = "create_menu_new_post"
            )
        )
    }
    BackHandler(enabled = showCreateMenu) { showCreateMenu = false }
    BackHandler(enabled = currentRoute == Screen.Login.route) {
        pendingRoute = null
        navController.popBackStack()
    }
    LaunchedEffect(currentRoute) { showCreateMenu = false }
    val navigateToOwnProfile = {
        val username = userProfile?.username?.takeIf { it.isNotBlank() && it != "Guest" }
        if (username != null) {
            showProfileDropdown = !showProfileDropdown
        } else if (!isAuthenticated) {
            gateReason = GateReason.Profile
        } else {
            navController.navigate(Screen.Settings.route)
        }
    }

    androidx.compose.runtime.DisposableEffect(navController) {
        com.neb.ians.ui.components.PostInsightsNav.open = { id ->
            navController.navigate(Screen.PostInsights.createRoute(id))
        }
        onDispose { com.neb.ians.ui.components.PostInsightsNav.open = null }
    }

    androidx.compose.runtime.DisposableEffect(navController) {
        com.neb.ians.ui.screens.analytics.ResourceInsightsNav.open = { id ->
            navController.navigate(Screen.ResourceInsights.createRoute(id))
        }
        onDispose { com.neb.ians.ui.screens.analytics.ResourceInsightsNav.open = null }
    }

    val glassBackdrop = com.neb.ians.ui.components.rememberGlassBackdrop()
    // the page goes soft behind the open create menu (Android 12 and up draws the blur; older systems keep the frosted scrim)
    val menuBlur by androidx.compose.animation.core.animateDpAsState(
        targetValue = if (showCreateMenu && showBottomBar) 16.dp else 0.dp,
        animationSpec = com.neb.ians.ui.theme.nebEffectsSpec(),
        label = "create_menu_blur"
    )

    val navScroll = com.neb.ians.ui.components.rememberNavBarScroll()
    LaunchedEffect(currentRoute) { navScroll.show() }
    CompositionLocalProvider(LocalAuthGate provides gate) {
    Box(modifier = Modifier.fillMaxSize().navBarScrollSource(navScroll)) {
        NavHost(
            navController = navController,
            startDestination = Screen.Splash.route,
            modifier = Modifier
                .fillMaxSize()
                .then(if (menuBlur > 0.5.dp) Modifier.blur(menuBlur) else Modifier)
                .glassSource(glassBackdrop),
            // Shared-axis motion on springs: the next screen travels a short, decisive distance and
            // settles with a little life, the one behind drifts the other way and fades.
            enterTransition = {
                slideInHorizontally(
                    initialOffsetX = { (it * 0.14f).toInt() },
                    animationSpec = spring(0.82f, Spring.StiffnessMediumLow, IntOffset.VisibilityThreshold)
                ) + fadeIn(animationSpec = spring(stiffness = Spring.StiffnessMedium))
            },
            exitTransition = {
                slideOutHorizontally(
                    targetOffsetX = { -(it * 0.10f).toInt() },
                    animationSpec = spring(1f, Spring.StiffnessMediumLow, IntOffset.VisibilityThreshold)
                ) + fadeOut(animationSpec = spring(stiffness = Spring.StiffnessMedium))
            },
            popEnterTransition = {
                slideInHorizontally(
                    initialOffsetX = { -(it * 0.10f).toInt() },
                    animationSpec = spring(0.9f, Spring.StiffnessMediumLow, IntOffset.VisibilityThreshold)
                ) + fadeIn(animationSpec = spring(stiffness = Spring.StiffnessMedium))
            },
            popExitTransition = {
                slideOutHorizontally(
                    targetOffsetX = { (it * 0.14f).toInt() },
                    animationSpec = spring(1f, Spring.StiffnessMediumLow, IntOffset.VisibilityThreshold)
                ) + fadeOut(animationSpec = spring(stiffness = Spring.StiffnessMedium))
            },
        ) {
            composable(Screen.Splash.route) {
                SplashScreen(
                    authRepository = authRepository,
                    settingsRepository = settingsViewModel.settingsRepository,
                    onNavigateToHome = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                        // Opened from a notification: go straight to its screen, Home stays underneath.
                        openDeepLink()
                    },
                    onNavigateToLogin = {
                        // guests browse first; sign-in is asked for when something needs it
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                        openDeepLink()
                    },
                    onNavigateToCompleteProfile = {
                        navController.navigate(Screen.CompleteProfile.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                    },
                    onNavigateToIntro = {
                        navController.navigate(Screen.Intro.route) {
                            popUpTo(Screen.Splash.route) { inclusive = true }
                        }
                    }
                )
            }
            composable(
                Screen.Intro.route,
                enterTransition = { fadeIn(animationSpec = spring(stiffness = Spring.StiffnessMediumLow)) },
                exitTransition = { fadeOut(animationSpec = spring(stiffness = Spring.StiffnessMediumLow)) }
            ) {
                val introScope = rememberCoroutineScope()
                IntroScreen(
                    onFinish = {
                        introScope.launch { settingsViewModel.settingsRepository.setIntroSeen(true) }
                        navController.navigate(Screen.Home.route) {
                            popUpTo(Screen.Intro.route) { inclusive = true }
                        }
                    }
                )
            }
            composable(
                Screen.Login.route,
                enterTransition = { fadeIn(animationSpec = spring(stiffness = Spring.StiffnessMediumLow)) },
                popEnterTransition = { fadeIn(animationSpec = spring(stiffness = Spring.StiffnessMediumLow)) },
                exitTransition = { fadeOut(animationSpec = spring(stiffness = Spring.StiffnessMedium)) }
            ) {
                LoginScreen(
                    onNavigateToEmailAuth = { navController.navigate(Screen.EmailAuth.route) },
                    onClose = { pendingRoute = null; navController.popBackStack() }
                )
            }
            composable(Screen.EmailAuth.route) {
                EmailAuthScreen(
                    onClose = { navController.popBackStack() },
                    onNavigateToHome = leaveAuth,
                    onNavigateToOnboarding = { navController.navigate(Screen.CompleteProfile.route) },
                    onNavigateToVerification = { email ->
                        navController.navigate(Screen.EmailVerification.createRoute(email))
                    },
                    onNavigateToForgotPassword = { email ->
                        navController.navigate(Screen.ForgotPassword.createRoute(email))
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
                    onNavigateToHome = leaveAuth,
                    onNavigateToOnboarding = { navController.navigate(Screen.CompleteProfile.route) },
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
                    onNavigateToHome = leaveAuth,
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.CompleteProfile.route) {
                OnboardingScreen(
                    onFinished = leaveAuth,
                    onSignInAgain = {
                        navController.navigate(Screen.Home.route) { popUpTo(0) { inclusive = true } }
                        navController.navigate(Screen.Login.route)
                    }
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
                    onNotesClick = { navController.navigate(Screen.Notes.route) },
                    onNewsClick = { navController.navigate(Screen.News.route) },
                    onPathwaysClick = { navController.navigate(Screen.Pathways.route) },
                    onUploadClick = { navController.navigate(Screen.Upload.route) },
                    onNewsItemClick = { slug -> navController.navigate(Screen.NewsDetail.createRoute(slug)) },
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onEditPostClick = { editPostId ->
                        navController.navigate(Screen.EditPost.createRoute(editPostId))
                    },
                    onNotificationsClick = { navController.navigate(Screen.Notifications.route) },
                    onProfileClick = navigateToOwnProfile,
                    onUserProfileClick = { username -> navController.navigate(Screen.Profile.createRoute(username)) },
                    onSeeAllPeopleClick = { navController.navigate(Screen.People.route) },
                    onCreatePostClick = { navController.navigate(Screen.CreatePost.route) }
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
                    onStudyDocClick = { grade, subject, kind, no ->
                        navController.navigate(Screen.StudyReader.createRoute(grade, subject, kind, no))
                    },
                    onSyllabusDetailChromeChanged = { hideLibraryDetailChrome = it },
                    onRequestResourceClick = { navController.navigate(Screen.ResourceRequests.route) },
                    onCreatorClick = { slug -> navController.navigate(Screen.CreatorPage.createRoute(slug)) },
                    onMarketplaceCourseClick = { courseId ->
                        navController.navigate(Screen.MarketplaceCourse.createRoute(courseId))
                    },
                    onStudioClick = { navController.navigate(Screen.CreatorStudio.route) }
                )
            }
            composable(Screen.CreatorStudio.route) {
                CreatorStudioScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onViewPage = { slug -> navController.navigate(Screen.CreatorPage.createRoute(slug)) }
                )
            }
            composable(
                route = Screen.CreatorPage.route,
                arguments = listOf(navArgument("slug") { type = NavType.StringType })
            ) {
                CreatorPageScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onCourseClick = { courseId ->
                        navController.navigate(Screen.MarketplaceCourse.createRoute(courseId))
                    },
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onOpenStudio = { navController.navigate(Screen.CreatorStudio.route) }
                )
            }
            composable(
                route = Screen.MarketplaceCourse.route,
                arguments = listOf(navArgument("courseId") { type = NavType.StringType })
            ) {
                MarketplaceCourseScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onCreatorClick = { slug -> navController.navigate(Screen.CreatorPage.createRoute(slug)) },
                    onResourceClick = { resourceId ->
                        navController.navigate(Screen.ResourceDetail.createRoute(resourceId))
                    },
                    onSignInRequired = { gate.ask(GateReason.Generic) }
                )
            }
            composable(Screen.Forum.route) {
                ForumScreen(
                    onNavigateBack = { navController.popBackStack() },
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
                    onNavigateToResultChecker = { navController.navigate(Screen.ResultChecker.route) },
                    onNavigateToNotes = { navController.navigate(Screen.Notes.route) },
                    onNavigateToPathways = { navController.navigate(Screen.Pathways.route) },
                    onNavigateToPostLab = { navController.navigate(Screen.PostLab.route) }
                )
            }
            composable(Screen.Pathways.route) {
                PathwaysScreen(onNavigateBack = { navController.popBackStack() })
            }
            composable(Screen.PostLab.route) {
                DynamicPostsLabScreen(onNavigateBack = { navController.popBackStack() })
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
            composable(Screen.People.route) {
                PeopleScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onPersonClick = { username ->
                        navController.navigate(Screen.Profile.createRoute(username))
                    }
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
                route = Screen.StudyReader.route,
                arguments = listOf(
                    navArgument("grade") { type = NavType.StringType },
                    navArgument("subject") { type = NavType.StringType },
                    navArgument("kind") { type = NavType.StringType },
                    navArgument("no") { type = NavType.StringType }
                )
            ) {
                com.neb.ians.ui.screens.library.StudyReaderScreen(onBack = { navController.popBackStack() })
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
                    onPostClick = { postId -> navController.navigate(Screen.ForumPostDetail.createRoute(postId)) },
                    onResourceClick = { resourceId -> navController.navigate(Screen.ResourceDetail.createRoute(resourceId)) }
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
                route = Screen.Legal.route,
                arguments = listOf(navArgument("doc") { type = NavType.StringType })
            ) { backStackEntry ->
                val doc = backStackEntry.arguments?.getString("doc") ?: com.neb.ians.ui.screens.legal.NebLegal.PRIVACY
                com.neb.ians.ui.screens.legal.LegalScreen(
                    documentKey = doc,
                    onClose = { navController.popBackStack() }
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
            composable(Screen.About.route) {
                com.neb.ians.ui.screens.about.AboutScreen(
                    onBack = { navController.popBackStack() },
                    onOpenLibrary = { navController.navigate(Screen.Library.createRoute(null)) }
                )
            }
            composable(Screen.Settings.route) {
                SettingsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    settingsViewModel = settingsViewModel,
                    onNavigateToEditProfile = { navController.navigate(Screen.EditProfile.route) },
                    onNavigateToBookmarks = { navController.navigate(Screen.Bookmarks.route) },
                    onNavigateToNebyCredits = { navController.navigate(Screen.NebyCredits.route) },
                    onNavigateToDeleteAccount = { navController.navigate(Screen.DeleteAccount.route) },
                    onNavigateToAccountSecurity = {
                        navController.navigate(Screen.AccountSecurity.route)
                    },
                    onNavigateToLogin = {
                        navController.navigate(Screen.Home.route) {
                            popUpTo(navController.graph.findStartDestination().id) { inclusive = true }
                        }
                    },
                    onNavigateToWebPortal = { url ->
                        navController.navigate(Screen.WebPortal.createRoute(url))
                    },
                    onNavigateToLegal = { doc ->
                        navController.navigate(Screen.Legal.createRoute(doc))
                    },
                    onNavigateToAbout = { navController.navigate(Screen.About.route) },
                    onNavigateToNotes = {
                        navController.navigate(Screen.Notes.route)
                    }
                )
            }
            composable(route = Screen.Notes.route) {
                NotesScreen(
                    onOpenNote = { id -> navController.navigate(Screen.NoteEditor.createRoute(id)) },
                    onNewNote = { dictate -> navController.navigate(Screen.NoteEditor.createRoute("new", dictate)) },
                    onOpenVoice = { navController.navigate(Screen.VoiceModels.route) }
                )
            }
            composable(
                route = Screen.NoteEditor.route,
                arguments = listOf(
                    navArgument("noteId") { type = NavType.StringType },
                    navArgument("dictate") {
                        type = NavType.BoolType
                        defaultValue = false
                    }
                )
            ) {
                NoteEditorScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onOpenNote = { id ->
                        navController.navigate(Screen.NoteEditor.createRoute(id)) {
                            popUpTo(Screen.NoteEditor.route) { inclusive = true }
                        }
                    },
                    onOpenVoice = { navController.navigate(Screen.VoiceModels.route) }
                )
            }
            composable(route = Screen.VoiceModels.route) {
                VoiceModelsScreen(onNavigateBack = { navController.popBackStack() })
            }
            composable(Screen.AccountSecurity.route) {
                com.neb.ians.ui.screens.settings.AccountSecurityScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(Screen.DeleteAccount.route) {
                com.neb.ians.ui.screens.settings.DeleteAccountScreen(
                    viewModel = settingsViewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onNavigateToLegal = { doc ->
                        navController.navigate(Screen.Legal.createRoute(doc))
                    }
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
                val detailViewModel: com.neb.ians.ui.screens.resource.ResourceDetailViewModel =
                    androidx.hilt.navigation.compose.hiltViewModel()
                detailViewModel.surface = when {
                    navController.previousBackStackEntry?.destination?.route?.startsWith("library") == true -> "library"
                    navController.previousBackStackEntry?.destination?.route?.startsWith("search") == true -> "search"
                    navController.previousBackStackEntry?.destination?.route?.startsWith("profile") == true -> "profile"
                    navController.previousBackStackEntry?.destination?.route == "home" -> "home"
                    navController.previousBackStackEntry?.destination?.route?.startsWith("resource/") == true -> "related"
                    else -> ""
                }
                ResourceDetailScreen(
                    viewModel = detailViewModel,
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
                    onEditPostClick = { editPostId ->
                        navController.navigate(Screen.EditPost.createRoute(editPostId))
                    },
                    onProfileClick = { userId ->
                        navController.navigate(Screen.Profile.createRoute(userId))
                    }
                )
            }
            composable(
                route = Screen.PostInsights.route,
                arguments = listOf(navArgument("postId") { type = NavType.StringType })
            ) {
                com.neb.ians.ui.screens.analytics.PostInsightsScreen(
                    onNavigateBack = { navController.popBackStack() }
                )
            }
            composable(
                route = Screen.ResourceInsights.route,
                arguments = listOf(
                    navArgument("resourceId") {
                        type = NavType.StringType
                        nullable = true
                        defaultValue = null
                    }
                )
            ) {
                com.neb.ians.ui.screens.analytics.ResourceInsightsScreen(
                    onNavigateBack = { navController.popBackStack() },
                    onResourceClick = { id -> navController.navigate(Screen.ResourceDetail.createRoute(id)) },
                    onPostClick = { id -> navController.navigate(Screen.ForumPostDetail.createRoute(id)) }
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
        }

        NebFabMenuScrim(
            expanded = showCreateMenu && showBottomBar,
            onDismissRequest = { showCreateMenu = false }
        )

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
                onCreateClick = { showCreateMenu = !showCreateMenu },
                menuActions = createMenuActions,
                menuExpanded = showCreateMenu,
                onMenuDismiss = { showCreateMenu = false },
                backdrop = glassBackdrop,
                modifier = Modifier.align(Alignment.BottomCenter)
                    .navBarScrollTransform(navScroll, pinned = showCreateMenu)
            )
        }

        if (showMiniPlayer && currentRoute != Screen.ResourceDetail.route && playerResourceId != null) {
            MiniPlayerSlot(
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
        gateReason?.let { reason ->
            SignInSheet(
                reason = reason,
                onSignIn = openSignIn,
                onDismiss = { gateReason = null; pendingRoute = null }
            )
        }
    }
    }
}

/** The mini player, reading the player's state itself so its position ticks recompose only it. */
@Composable
private fun MiniPlayerSlot(
    viewModel: MediaPlayerViewModel,
    onExpand: () -> Unit,
    onClose: () -> Unit,
    modifier: Modifier
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    MiniMediaPlayer(uiState = uiState, viewModel = viewModel, onExpand = onExpand, onClose = onClose, modifier = modifier)
}
