package com.neb.ians.data.api

import androidx.compose.runtime.Immutable
import kotlinx.serialization.Serializable

/**
 * The look of a dynamic post. The same vocabulary as a note page: page colour (`tone`,
 * an index into `NoteTones`), cover (`cover` pattern, or `photo`; 0 is none), icon key, paper and type.
 * Zero and empty are the defaults, so a plain post carries no look at all.
 */
@Immutable
@Serializable
data class PostLook(
    val tone: Int = 0,
    val cover: Int = 0,
    val icon: String = "",
    val paper: Int = 0,
    val font: Int = 0,
    /** A picture cover: id of an uploaded content image. Wins over the pattern cover. */
    val photo: Int = 0,
    /** A picture behind the whole page (content image id), under a flat wash of the page colour. */
    val bg: Int = 0,
) {
    val isPlain: Boolean get() = tone == 0 && cover <= 0 && photo == 0 && icon.isEmpty() && paper == 0 && font == 0 && bg == 0

    /** A plain look is sent as null for new posts. */
    fun orNull(): PostLook? = if (isPlain) null else this

    companion object {
        const val FONT_DEFAULT = 0
        const val FONT_SERIF = 1
        const val FONT_MONO = 2
        val fontLabels = listOf("Default", "Serif", "Mono")
    }
}
