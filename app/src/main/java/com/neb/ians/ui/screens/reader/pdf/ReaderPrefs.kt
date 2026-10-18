package com.neb.ians.ui.screens.reader.pdf

import android.content.Context
import android.content.SharedPreferences

enum class ReadingTheme { Paper, Sepia, Night }

enum class ReadingLayout { Scroll, Pages }

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
}
