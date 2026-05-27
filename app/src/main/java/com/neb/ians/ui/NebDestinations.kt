package com.neb.ians.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Book
import androidx.compose.material.icons.outlined.Forum
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.rounded.Book
import androidx.compose.material.icons.rounded.Forum
import androidx.compose.material.icons.rounded.Home
import androidx.compose.material.icons.rounded.Settings
import androidx.compose.ui.graphics.vector.ImageVector

object NebRoutes {
    const val HOME = "home"
    const val LIBRARY = "library"
    const val FORUM = "forum"
    const val SETTINGS = "settings"

    const val READER = "reader/{resourceId}"
    fun reader(resourceId: Long) = "reader/$resourceId"

    const val THREAD = "thread/{threadId}"
    fun thread(threadId: Long) = "thread/$threadId"

    const val REPLY = "reply/{threadId}"
    fun reply(threadId: Long) = "reply/$threadId"

    const val NEW_THREAD = "new_thread"
}

data class TabDestination(
    val route: String,
    val label: String,
    val outlined: ImageVector,
    val filled: ImageVector,
)

val NebTabs = listOf(
    TabDestination(NebRoutes.HOME, "Home", Icons.Outlined.Home, Icons.Rounded.Home),
    TabDestination(NebRoutes.LIBRARY, "Library", Icons.Outlined.Book, Icons.Rounded.Book),
    TabDestination(NebRoutes.FORUM, "Forum", Icons.Outlined.Forum, Icons.Rounded.Forum),
    TabDestination(NebRoutes.SETTINGS, "Settings", Icons.Outlined.Settings, Icons.Rounded.Settings),
)
