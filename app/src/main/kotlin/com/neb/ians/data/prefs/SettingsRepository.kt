package com.neb.ians.data.prefs

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore by preferencesDataStore(name = "neb_prefs")

@Singleton
class SettingsRepository @Inject constructor(
    @ApplicationContext private val ctx: Context,
) {
    private val darkKey = booleanPreferencesKey("dark_mode")
    private val pushKey = booleanPreferencesKey("push_enabled")

    val darkMode: Flow<Boolean> = ctx.dataStore.data.map { it[darkKey] ?: false }
    val pushEnabled: Flow<Boolean> = ctx.dataStore.data.map { it[pushKey] ?: true }

    suspend fun setDarkMode(on: Boolean) { ctx.dataStore.edit { it[darkKey] = on } }
    suspend fun setPushEnabled(on: Boolean) { ctx.dataStore.edit { it[pushKey] = on } }
}
