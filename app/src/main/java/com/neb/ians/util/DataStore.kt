package com.neb.ians.util

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore by preferencesDataStore(name = "neb_prefs")

object PreferencesKeys {
    val DARK_MODE = booleanPreferencesKey("dark_mode")
    val NOTIFICATIONS_ENABLED = booleanPreferencesKey("notifications_enabled")
}

suspend fun Context.setDarkMode(enabled: Boolean) {
    dataStore.edit { it[PreferencesKeys.DARK_MODE] = enabled }
}

val Context.darkModeFlow: Flow<Boolean>
    get() = dataStore.data.map { it[PreferencesKeys.DARK_MODE] ?: false }

suspend fun Context.setNotificationsEnabled(enabled: Boolean) {
    dataStore.edit { it[PreferencesKeys.NOTIFICATIONS_ENABLED] = enabled }
}

val Context.notificationsEnabledFlow: Flow<Boolean>
    get() = dataStore.data.map { it[PreferencesKeys.NOTIFICATIONS_ENABLED] ?: true }
