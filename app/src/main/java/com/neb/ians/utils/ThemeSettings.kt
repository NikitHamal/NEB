package com.neb.ians.utils

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

enum class ThemePreference { LIGHT, DARK, SYSTEM }

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class ThemeSettings(private val context: Context) {

    private val themeKey = stringPreferencesKey("theme_preference")

    val themePreference: Flow<ThemePreference> = context.dataStore.data.map { prefs ->
        when (prefs[themeKey]) {
            "light" -> ThemePreference.LIGHT
            "dark" -> ThemePreference.DARK
            else -> ThemePreference.SYSTEM
        }
    }

    suspend fun setTheme(preference: ThemePreference) {
        context.dataStore.edit { prefs ->
            prefs[themeKey] = when (preference) {
                ThemePreference.LIGHT -> "light"
                ThemePreference.DARK -> "dark"
                ThemePreference.SYSTEM -> "system"
            }
        }
    }
}
