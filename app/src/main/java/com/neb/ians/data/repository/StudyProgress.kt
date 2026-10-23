package com.neb.ians.data.repository

import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject
import javax.inject.Singleton

/** How far a student has got with one chapter, question set or exam guide. */
data class StudyMark(
    /** Reading credit 0-100; grows with time on the page, so skipping ahead does not count. */
    val read: Int = 0,
    /** Where the student stopped, 0-100 of the page. */
    val place: Int = 0,
    val markedDone: Boolean = false,
    val right: Int = 0,
    val tried: Int = 0,
    val openedAt: Long = 0L,
    val title: String = ""
) {
    val isDone: Boolean get() = markedDone || read >= 96
    val isStarted: Boolean get() = !isDone && read > 3
    val isWeak: Boolean get() = tried >= 2 && right * 10 < tried * 6
}

/**
 * Study progress, kept on the device. Keys follow the website's scheme,
 * "<grade>/<subject>/unit<N>", ".../bank<N>" and ".../guide", so the two read alike.
 * [version] ticks on every write; screens collect it to repaint.
 */
@Singleton
class StudyProgress @Inject constructor(@ApplicationContext context: Context) {
    private val prefs = context.getSharedPreferences("neb_study", Context.MODE_PRIVATE)
    private val _version = MutableStateFlow(0)
    val version: StateFlow<Int> = _version.asStateFlow()

    fun get(key: String): StudyMark {
        val answers = answers(key)
        return StudyMark(
            read = prefs.getInt("r:$key", 0),
            place = prefs.getInt("y:$key", 0),
            markedDone = prefs.getBoolean("d:$key", false),
            right = answers.values.count { it },
            tried = answers.size,
            openedAt = prefs.getLong("t:$key", 0L),
            title = prefs.getString("n:$key", null).orEmpty()
        )
    }

    fun open(key: String, title: String, label: String) {
        prefs.edit()
            .putLong("t:$key", System.currentTimeMillis())
            .putString("n:$key", title)
            .putString("l:$key", label)
            .putString("last", key)
            .apply()
        bump()
    }

    fun setReading(key: String, read: Int, place: Int) {
        val best = maxOf(read.coerceIn(0, 100), prefs.getInt("r:$key", 0))
        prefs.edit().putInt("r:$key", best).putInt("y:$key", place.coerceIn(0, 100)).apply()
        bump()
    }

    fun setDone(key: String, done: Boolean) {
        prefs.edit().putBoolean("d:$key", done).apply()
        bump()
    }

    fun answers(key: String): Map<Int, Boolean> =
        prefs.getString("q:$key", null).orEmpty().split(";").mapNotNull { part ->
            val (i, v) = part.split("=").takeIf { it.size == 2 } ?: return@mapNotNull null
            i.toIntOrNull()?.let { it to (v == "1") }
        }.toMap()

    fun setAnswer(key: String, index: Int, right: Boolean) {
        val all = answers(key) + (index to right)
        prefs.edit().putString("q:$key", all.entries.joinToString(";") { "${it.key}=${if (it.value) 1 else 0}" }).apply()
        bump()
    }

    fun clearAnswers(key: String) {
        prefs.edit().remove("q:$key").apply()
        bump()
    }

    /** Every mark on the device, keyed as above. */
    fun snapshot(): Map<String, StudyMark> =
        prefs.all.keys
            .mapNotNull { k -> PREFIXES.firstOrNull { k.startsWith(it) }?.let { k.removePrefix(it) } }
            .toSet()
            .associateWith { get(it) }

    /** The chapter opened most recently: key, its title and its "Class 11 · Physics" label. */
    fun last(): Triple<String, String, String>? {
        val key = prefs.getString("last", null) ?: return null
        return Triple(key, prefs.getString("n:$key", null).orEmpty(), prefs.getString("l:$key", null).orEmpty())
    }

    private companion object {
        val PREFIXES = listOf("r:", "d:", "q:", "t:")
    }

    private fun bump() {
        _version.value = _version.value + 1
    }
}
