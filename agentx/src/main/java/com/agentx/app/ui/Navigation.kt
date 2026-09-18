package com.agentx.app.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.automirrored.outlined.Chat
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.outlined.Build
import androidx.compose.material.icons.outlined.History
import androidx.compose.material.icons.outlined.Repeat
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.agentx.app.ui.screens.activity.ActivityScreen
import com.agentx.app.ui.screens.assistant.AssistantScreen
import com.agentx.app.ui.screens.routines.RoutinesScreen
import com.agentx.app.ui.screens.settings.SettingsScreen
import com.agentx.app.ui.screens.setup.SetupScreen
import com.agentx.app.ui.screens.tools.ToolsScreen
import com.agentx.app.ui.theme.AxPillShape

const val ASSISTANT_ROUTE_PATTERN = "assistant?prefill={prefill}"

sealed class AxScreen(val route: String) {
    data object Setup : AxScreen("setup")
    data object Assistant : AxScreen(ASSISTANT_ROUTE_PATTERN) {
        fun route(prefill: String = "") = "assistant?prefill=" + java.net.URLEncoder.encode(prefill, "UTF-8")
    }
    data object Routines : AxScreen("routines")
    data object Tools : AxScreen("tools")
    data object Activity : AxScreen("activity")
    data object Settings : AxScreen("settings")
}

private data class BottomItem(
    val base: String,
    val label: String,
    val active: ImageVector,
    val inactive: ImageVector
)

private val bottomItems = listOf(
    BottomItem("assistant", "Assistant", Icons.AutoMirrored.Filled.Chat, Icons.AutoMirrored.Outlined.Chat),
    BottomItem("routines", "Routines", Icons.Filled.Repeat, Icons.Outlined.Repeat),
    BottomItem("tools", "Tools", Icons.Filled.Build, Icons.Outlined.Build),
    BottomItem("activity", "Activity", Icons.Filled.History, Icons.Outlined.History)
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
                Surface(
                    shape = AxPillShape,
                    tonalElevation = 3.dp,
                    shadowElevation = 18.dp,
                    modifier = Modifier
                        .padding(horizontal = 16.dp)
                        .navigationBarsPadding()
                        .padding(bottom = 12.dp)
                ) {
                    NavigationBar(containerColor = androidx.compose.ui.graphics.Color.Transparent) {
                        bottomItems.forEach { item ->
                            val selected = current == item.base
                            NavigationBarItem(
                                selected = selected,
                                onClick = {
                                    if (!selected) {
                                        controller.navigate(item.base) {
                                            popUpTo(ASSISTANT_ROUTE_PATTERN) { inclusive = false }
                                            launchSingleTop = true
                                        }
                                    }
                                },
                                icon = {
                                    Icon(
                                        if (selected) item.active else item.inactive,
                                        contentDescription = item.label
                                    )
                                },
                                label = { Text(item.label) }
                            )
                        }
                    }
                }
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
                composable(
                    route = ASSISTANT_ROUTE_PATTERN,
                    arguments = listOf(navArgument("prefill") { type = NavType.StringType; defaultValue = "" })
                ) { entry ->
                    AssistantScreen(
                        prefill = entry.arguments?.getString("prefill").orEmpty(),
                        onOpenSettings = { controller.navigate("settings") },
                        onNeedSetup = { controller.navigate("setup") }
                    )
                }
                composable("routines") { RoutinesScreen() }
                composable("tools") {
                    ToolsScreen(onTryInAssistant = { text ->
                        controller.navigate(AxScreen.Assistant.route(text))
                    })
                }
                composable("activity") { ActivityScreen() }
                composable("settings") { SettingsScreen(onBack = { controller.popBackStack() }) }
            }
        }
    }
}
