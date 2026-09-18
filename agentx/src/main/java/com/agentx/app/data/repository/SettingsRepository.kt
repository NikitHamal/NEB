package com.agentx.app.data.repository

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.axDataStore by preferencesDataStore("agentx_settings")

@Singleton
class SettingsRepository @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        const val ACT_THRESHOLD = 0.7
        const val DEFAULT_CONFIRM_THRESHOLD = 0.35f
        private val DARK_MODE = booleanPreferencesKey("dark_mode")
        private val CONFIRM_THRESHOLD = floatPreferencesKey("confirm_threshold")
        private val CONFIRM_DESTRUCTIVE = booleanPreferencesKey("confirm_destructive")
        private val SETUP_DONE = booleanPreferencesKey("setup_done")
    }

    val isDarkMode: Flow<Boolean> = context.axDataStore.data.map { it[DARK_MODE] ?: false }
    suspend fun setDarkMode(value: Boolean) {
        context.axDataStore.edit { it[DARK_MODE] = value }
    }

    val confirmThreshold: Flow<Float> = context.axDataStore.data.map { it[CONFIRM_THRESHOLD] ?: DEFAULT_CONFIRM_THRESHOLD }
    suspend fun setConfirmThreshold(value: Float) {
        context.axDataStore.edit { it[CONFIRM_THRESHOLD] = value.coerceIn(0.1f, 0.69f) }
    }

    val confirmDestructive: Flow<Boolean> = context.axDataStore.data.map { it[CONFIRM_DESTRUCTIVE] ?: true }
    suspend fun setConfirmDestructive(value: Boolean) {
        context.axDataStore.edit { it[CONFIRM_DESTRUCTIVE] = value }
    }

    val setupDone: Flow<Boolean> = context.axDataStore.data.map { it[SETUP_DONE] ?: false }
    suspend fun setSetupDone(value: Boolean) {
        context.axDataStore.edit { it[SETUP_DONE] = value }
    }
}
