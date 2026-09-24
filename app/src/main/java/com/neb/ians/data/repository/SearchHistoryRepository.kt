package com.neb.ians.data.repository

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

/**
 * The last handful of things the user searched for, most recent first.
 *
 * Stored as one newline-joined string rather than a preference set because the
 * order is the whole point — a set would hand back the same queries shuffled.
 */
@Singleton
class SearchHistoryRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {

    val recentQueries: Flow<List<String>> = dataStore.data.map { prefs ->
        prefs[RECENT_SEARCHES].orEmpty()
            .split(SEPARATOR)
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .take(MAX_ENTRIES)
    }

    suspend fun record(query: String) {
        val cleaned = query.trim().replace(SEPARATOR, " ")
        if (cleaned.length < MIN_LENGTH) return
        dataStore.edit { prefs ->
            val existing = prefs[RECENT_SEARCHES].orEmpty()
                .split(SEPARATOR)
                .map { it.trim() }
                .filter { it.isNotEmpty() && !it.equals(cleaned, ignoreCase = true) }
            prefs[RECENT_SEARCHES] = (listOf(cleaned) + existing).take(MAX_ENTRIES).joinToString(SEPARATOR)
        }
    }

    suspend fun remove(query: String) {
        dataStore.edit { prefs ->
            val remaining = prefs[RECENT_SEARCHES].orEmpty()
                .split(SEPARATOR)
                .map { it.trim() }
                .filter { it.isNotEmpty() && !it.equals(query.trim(), ignoreCase = true) }
            prefs[RECENT_SEARCHES] = remaining.joinToString(SEPARATOR)
        }
    }

    suspend fun clear() {
        dataStore.edit { it[RECENT_SEARCHES] = "" }
    }

    private companion object {
        val RECENT_SEARCHES = stringPreferencesKey("recent_searches")
        const val SEPARATOR = "\n"
        const val MAX_ENTRIES = 10
        const val MIN_LENGTH = 2
    }
}
