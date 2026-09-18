package com.agentx.app.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.outlined.AutoAwesome
import androidx.compose.material.icons.outlined.Build
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.Repeat
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.agentx.app.ui.components.AxGlassBottomNav
import com.agentx.app.ui.components.AxNavItem
import com.agentx.app.ui.screens.activity.ActivityScreen
import com.agentx.app.ui.screens.assistant.AssistantScreen
import com.agentx.app.ui.screens.chat.ChatScreen
import com.agentx.app.ui.screens.routines.RoutinesScreen
import com.agentx.app.ui.screens.settings.SettingsScreen
import com.agentx.app.ui.screens.setup.SetupScreen
import com.agentx.app.ui.screens.tools.ToolsScreen

const val ASSISTANT_ROUTE_PATTERN = "assistant"
const val CHAT_ROUTE_PATTERN = "chat/{conversationId}?prefill={prefill}"

fun chatRoute(conversationId: String, prefill: String = ""): String {
    return "chat/" + conversationId + "?prefill=" + java.net.URLEncoder.encode(prefill, "UTF-8")
}

sealed class AxScreen(val route: String) {
    data object Setup : AxScreen("setup")
    data object Assistant : AxScreen(ASSISTANT_ROUTE_PATTERN)
    data object Chat : AxScreen(CHAT_ROUTE_PATTERN)
    data object Routines : AxScreen("routines")
    data object Tools : AxScreen("tools")
    data object Activity : AxScreen("activity")
    data object Settings : AxScreen("settings")
}

private val bottomItems = listOf(
    AxNavItem("assistant", "Assistant", Icons.Filled.AutoAwesome, Icons.Outlined.AutoAwesome),
    AxNavItem("routines", "Routines", Icons.Filled.Repeat, Icons.Outlined.Repeat),
    AxNavItem("tools", "Tools", Icons.Filled.Build, Icons.Outlined.Build),
    AxNavItem("activity", "Activity", Icons.Filled.History, Icons.Outlined.History)
)

@Composable
fun Navigation() {
    val controller = rememberNavController()
    val backStack by controller.currentBackStackEntryAsState()
    val current = backStack?.destination?.route?.substringBefore("?")
    val showBar = current == "assistant" || current == "routines" || current == "tools" || current == "activity"

    Scaffold(
        bottomBar = {
            if (showBar) {
                AxGlassBottomNav(
                    items = bottomItems,
                    currentRoute = current,
                    onSelect = { item ->
                        if (current != item.route) {
                            controller.navigate(item.route) {
                                popUpTo(ASSISTANT_ROUTE_PATTERN) { inclusive = false }
                                launchSingleTop = true
                            }
                        }
                    }
                )
            }
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            NavHost(navController = controller, startDestination = ASSISTANT_ROUTE_PATTERN) {
                composable("setup") {
                    SetupScreen(onReady = {
                        controller.navigate("assistant") {
                            popUpTo("setup") { inclusive = true }
                        }
                    })
                }
                composable(route = ASSISTANT_ROUTE_PATTERN) {
                    AssistantScreen(
                        onOpenChat = { id -> controller.navigate(chatRoute(id)) },
                        onOpenSettings = { controller.navigate("settings") }
                    )
                }
                composable(
                    route = CHAT_ROUTE_PATTERN,
                    arguments = listOf(
                        navArgument("conversationId") { type = NavType.StringType },
                        navArgument("prefill") { type = NavType.StringType; defaultValue = "" }
                    )
                ) { entry ->
                    ChatScreen(
                        prefill = entry.arguments?.getString("prefill").orEmpty(),
                        onBack = { controller.popBackStack() },
                        onOpenSettings = { controller.navigate("settings") },
                        onNeedSetup = { controller.navigate("setup") }
                    )
                }
                composable("routines") { RoutinesScreen() }
                composable("tools") {
                    ToolsScreen(onTryInAssistant = { text ->
                        controller.navigate(chatRoute("new", text))
                    })
                }
                composable("activity") { ActivityScreen() }
                composable("settings") { SettingsScreen(onBack = { controller.popBackStack() }) }
            }
        }
    }
}
