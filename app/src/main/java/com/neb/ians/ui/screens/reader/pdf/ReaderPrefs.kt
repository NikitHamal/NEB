package com.neb.ians.ui.screens.reader.pdf

import android.content.Context
import android.content.SharedPreferences

enum class ReadingTheme { Paper, Sepia, Night }

enum class ReadingLayout { Scroll, Pages }

enum class ReadingFont { Serif, Sans }

/** How reading mode sets its type. [brightness] is -1 for the system's own. */
data class ReadingSettings(
    val fontScale: Float = 1f,
    val font: ReadingFont = ReadingFont.Serif,
    val lineSpacing: Float = 1f,
    val margin: Int = 1,
    val justify: Boolean = false,
    val zen: Boolean = false,
    val brightness: Float = -1f,
    /** Answer and solution cards start folded; a tap on the card opens them. */
    val hideAnswers: Boolean = false
)

/**
 * What the reader remembers. Per document: the last page and the bookmarked pages. Across
 * documents: theme, layout and whether to keep the screen on. SharedPreferences is enough
 * here: a handful of tiny values, written on page change at most once a second.
 */
class ReaderPrefs(context: Context) {
    private val prefs: SharedPreferences =
        context.applicationContext.getSharedPreferences("nebians_pdf_reader", Context.MODE_PRIVATE)

    fun lastPage(docId: String): Int = prefs.getInt("last:$docId", 0)

    fun setLastPage(docId: String, page: Int) {
        prefs.edit().putInt("last:$docId", page).apply()
    }

    fun bookmarks(docId: String): Set<Int> =
        prefs.getStringSet("marks:$docId", emptySet()).orEmpty().mapNotNull { it.toIntOrNull() }.toSet()

    fun setBookmarks(docId: String, pages: Set<Int>) {
        prefs.edit().putStringSet("marks:$docId", pages.map { it.toString() }.toSet()).apply()
    }

    var theme: ReadingTheme
        get() = runCatching { ReadingTheme.valueOf(prefs.getString("theme", null) ?: "") }.getOrDefault(ReadingTheme.Paper)
        set(value) { prefs.edit().putString("theme", value.name).apply() }

    var layout: ReadingLayout
        get() = runCatching { ReadingLayout.valueOf(prefs.getString("layout", null) ?: "") }.getOrDefault(ReadingLayout.Scroll)
        set(value) { prefs.edit().putString("layout", value.name).apply() }

    var keepScreenOn: Boolean
        get() = prefs.getBoolean("keep_screen_on", true)
        set(value) { prefs.edit().putBoolean("keep_screen_on", value).apply() }

    /** Whether this document was last read in reading mode. */
    fun readingMode(docId: String): Boolean = prefs.getBoolean("rm:$docId", false)

    fun setReadingMode(docId: String, on: Boolean) {
        prefs.edit().putBoolean("rm:$docId", on).apply()
    }

    var reading: ReadingSettings
        get() = ReadingSettings(
            fontScale = prefs.getFloat("rd_scale", 1f).coerceIn(0.7f, 3f),
            font = runCatching { ReadingFont.valueOf(prefs.getString("rd_font", null) ?: "") }.getOrDefault(ReadingFont.Serif),
            lineSpacing = prefs.getFloat("rd_line", 1f).coerceIn(0.8f, 1.6f),
            margin = prefs.getInt("rd_margin", 1).coerceIn(0, 2),
            justify = prefs.getBoolean("rd_justify", false),
            zen = prefs.getBoolean("rd_zen", false),
            brightness = prefs.getFloat("rd_bright", -1f),
            hideAnswers = prefs.getBoolean("rd_hide_ans", false)
        )
        set(v) {
            prefs.edit()
                .putFloat("rd_scale", v.fontScale).putString("rd_font", v.font.name).putFloat("rd_line", v.lineSpacing)
                .putInt("rd_margin", v.margin).putBoolean("rd_justify", v.justify).putBoolean("rd_zen", v.zen)
                .putFloat("rd_bright", v.brightness).putBoolean("rd_hide_ans", v.hideAnswers).apply()
        }

    /** The Neby AI button can be dragged away; it comes back from the menu. */
    var assistantHidden: Boolean
        get() = prefs.getBoolean("ai_hidden", false)
        set(value) { prefs.edit().putBoolean("ai_hidden", value).apply() }

    /** Where the Neby AI button rests, as fractions of the free area; negative means the default corner. */
    var assistantX: Float
        get() = prefs.getFloat("ai_x", -1f)
        set(value) { prefs.edit().putFloat("ai_x", value).apply() }

    var assistantY: Float
        get() = prefs.getFloat("ai_y", -1f)
        set(value) { prefs.edit().putFloat("ai_y", value).apply() }
}
