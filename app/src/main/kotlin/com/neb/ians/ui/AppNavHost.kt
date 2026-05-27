package com.neb.ians.ui

import androidx.compose.animation.AnimatedContentTransitionScope.SlideDirection
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.neb.ians.ui.home.HomeScreen
import com.neb.ians.ui.resources.ResourceDetailScreen
import com.neb.ians.ui.resources.ResourcesScreen
import com.neb.ians.ui.settings.SettingsScreen

object Routes {
    const val Home = "home"
    const val Resources = "resources"
    const val ResourceDetail = "resource/{id}"
    const val Settings = "settings"
    fun resourceDetail(id: String) = "resource/$id"
}

@Composable
fun AppNavHost() {
    val nav = rememberNavController()
    NavHost(
        navController = nav,
        startDestination = Routes.Home,
        enterTransition = { slideIntoContainer(SlideDirection.Start, tween(220)) + fadeIn(tween(220)) },
        exitTransition = { slideOutOfContainer(SlideDirection.Start, tween(180)) + fadeOut(tween(180)) },
        popEnterTransition = { slideIntoContainer(SlideDirection.End, tween(220)) + fadeIn(tween(220)) },
        popExitTransition = { slideOutOfContainer(SlideDirection.End, tween(180)) + fadeOut(tween(180)) },
    ) {
        composable(Routes.Home) {
            HomeScreen(
                onOpenResources = { nav.navigate(Routes.Resources) },
                onOpenSettings = { nav.navigate(Routes.Settings) },
            )
        }
        composable(Routes.Resources) {
            ResourcesScreen(
                onBack = { nav.popBackStack() },
                onOpenResource = { id -> nav.navigate(Routes.resourceDetail(id)) },
            )
        }
        composable(Routes.ResourceDetail) { entry ->
            val id = entry.arguments?.getString("id").orEmpty()
            ResourceDetailScreen(
                resourceId = id,
                onBack = { nav.popBackStack() },
            )
        }
        composable(Routes.Settings) {
            SettingsScreen(onBack = { nav.popBackStack() })
        }
    }
}
