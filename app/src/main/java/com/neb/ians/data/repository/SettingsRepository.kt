package com.neb.ians.data.repository

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SettingsRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    companion object {
        val DARK_MODE = booleanPreferencesKey("dark_mode")
        val USER_NAME = stringPreferencesKey("user_name")
        val NOTIFICATIONS_ENABLED = booleanPreferencesKey("notifications_enabled")
        val DOWNLOAD_WIFI_ONLY = booleanPreferencesKey("download_wifi_only")
    }

    val isDarkMode: Flow<Boolean> = dataStore.data.map { it[DARK_MODE] ?: false }
    val userName: Flow<String> = dataStore.data.map { it[USER_NAME] ?: "Student" }
    val notificationsEnabled: Flow<Boolean> = dataStore.data.map { it[NOTIFICATIONS_ENABLED] ?: true }
    val downloadWifiOnly: Flow<Boolean> = dataStore.data.map { it[DOWNLOAD_WIFI_ONLY] ?: true }

    suspend fun setDarkMode(enabled: Boolean) {
        dataStore.edit { it[DARK_MODE] = enabled }
    }

    suspend fun setUserName(name: String) {
        dataStore.edit { it[USER_NAME] = name }
    }

    suspend fun setNotificationsEnabled(enabled: Boolean) {
        dataStore.edit { it[NOTIFICATIONS_ENABLED] = enabled }
    }

    suspend fun setDownloadWifiOnly(enabled: Boolean) {
        dataStore.edit { it[DOWNLOAD_WIFI_ONLY] = enabled }
    }
}
