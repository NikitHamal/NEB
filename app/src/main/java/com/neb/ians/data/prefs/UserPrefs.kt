package com.neb.ians.data.prefs

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.neb.ians.ui.theme.ThemeMode
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore(name = "neb_prefs")

data class UserPrefs(
    val themeMode: ThemeMode = ThemeMode.System,
    val dynamicColor: Boolean = true,
    val handle: String = "Student",
    val seededOnce: Boolean = false,
)

@Singleton
class UserPrefsRepository @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private val THEME = stringPreferencesKey("theme_mode")
    private val DYNAMIC = booleanPreferencesKey("dynamic_color")
    private val HANDLE = stringPreferencesKey("handle")
    private val SEEDED = booleanPreferencesKey("seeded_once")

    val flow: Flow<UserPrefs> = context.dataStore.data.map { p ->
        UserPrefs(
            themeMode = runCatching { ThemeMode.valueOf(p[THEME] ?: ThemeMode.System.name) }
                .getOrDefault(ThemeMode.System),
            dynamicColor = p[DYNAMIC] ?: true,
            handle = p[HANDLE] ?: "Student",
            seededOnce = p[SEEDED] ?: false,
        )
    }

    suspend fun setTheme(mode: ThemeMode) {
        context.dataStore.edit { it[THEME] = mode.name }
    }

    suspend fun setDynamic(enabled: Boolean) {
        context.dataStore.edit { it[DYNAMIC] = enabled }
    }

    suspend fun setHandle(handle: String) {
        context.dataStore.edit { it[HANDLE] = handle }
    }

    suspend fun markSeeded() {
        context.dataStore.edit { it[SEEDED] = true }
    }
}
