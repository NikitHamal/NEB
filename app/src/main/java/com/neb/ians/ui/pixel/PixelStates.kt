package com.neb.ians.ui.pixel

import androidx.compose.ui.graphics.vector.ImageVector

/**
 * Which pixel sprite stands for an empty, offline or "nothing found" state. Screens already pass
 * NebEmptyState the icon that names their situation (CloudOff, SearchOff, BookmarkBorder...), so
 * the sprite is picked from that icon and no screen has to change. Anything unmapped gets Neby,
 * idling, which suits a quiet empty page.
 */
object PixelStates {
    fun forIcon(icon: ImageVector): PixelSprite {
        val name = icon.name.substringAfterLast('.')
        return when {
            name.startsWith("CloudOff") || name.startsWith("WifiOff") || name.startsWith("Error") || name.startsWith("SyncProblem") -> PixelUiSprites.rainCloud
            name.startsWith("Search") || name.startsWith("ManageSearch") || name.startsWith("FindInPage") -> PixelUiSprites.magnifier
            name.startsWith("Notifications") -> PixelUiSprites.sleepyBell
            name.startsWith("Bookmark") -> PixelUiSprites.ribbon
            name.startsWith("Download") || name.startsWith("CloudDownload") || name.startsWith("FileDownload") -> PixelUiSprites.downloadTray
            name.startsWith("Forum") || name.startsWith("Chat") || name.startsWith("QuestionAnswer") || name.startsWith("Comment") -> PixelUiSprites.typing
            name.startsWith("MenuBook") || name.startsWith("AutoStories") || name.startsWith("LibraryBooks") || name.startsWith("Description") -> PixelUiSprites.bookLoader
            name.startsWith("Inbox") || name.startsWith("Hourglass") || name.startsWith("Schedule") -> PixelUiSprites.nebySleep
            else -> PixelUiSprites.nebyIdle
        }
    }
}
